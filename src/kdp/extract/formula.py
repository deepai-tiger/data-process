"""Equation region -> LaTeX.

The layout model gives us formula *regions*; this module turns each region into
LaTeX. Two things matter in practice:

* A "formula region" on a Korean textbook page is often a stack of several
  equations plus a right-aligned equation number. Recognizers are trained on a
  single equation, so the region is split before recognition.
* Recognizer output has to be gated. A hallucinated formula is worse than a
  missing one in a training corpus, so implausible LaTeX is rejected.
"""

from __future__ import annotations

import logging
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

logger = logging.getLogger(__name__)

_MAX_LATEX_CHARS = 4000


@dataclass
class FormulaResult:
    latex: str
    tag: str | None = None
    confidence: float | None = None
    engine: str = ""
    parts: int = 1


class FormulaRecognizer(Protocol):
    name: str

    def recognize(self, image) -> tuple[str, float | None]:
        """Return ``(latex, confidence)`` for a single-equation image."""


class NoopRecognizer:
    name = "none"

    def recognize(self, image) -> tuple[str, float | None]:
        return "", None


class Pix2TexRecognizer:
    """LaTeX-OCR (pix2tex): ~100 MB, ~1-2 s per equation on CPU."""

    name = "pix2tex"

    def __init__(self) -> None:
        try:
            from pix2tex.cli import LatexOCR
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "pix2tex is not installed; `pip install pix2tex` or set pdf.formula_engine=none"
            ) from exc
        self._model = LatexOCR()

    def recognize(self, image) -> tuple[str, float | None]:
        latex = self._model(image)
        return (latex or "").strip(), None


def build_recognizer(engine: str) -> FormulaRecognizer:
    if engine in ("none", "docling", "ocr_text"):
        return NoopRecognizer()
    if engine == "pix2tex":
        return Pix2TexRecognizer()
    raise ValueError(f"unknown formula engine: {engine}")


def recognize_region(
    image,
    recognizer: FormulaRecognizer,
    split_stacked: bool = True,
    strip_equation_number: bool = True,
    collapse_letter_runs: bool = True,
) -> FormulaResult | None:
    """Recognize one formula region, which may contain stacked equations."""
    parts = _split_stacked_equations(image) if split_stacked else [image]

    tag: str | None = None
    latex_parts: list[str] = []
    for part in parts:
        # the equation number sits on one line only, so strip it per equation
        if strip_equation_number:
            part, part_tag = _split_equation_number(part)
            tag = tag or part_tag
        latex, _ = recognizer.recognize(part)
        latex = postprocess_latex(latex, collapse_letter_runs=collapse_letter_runs)
        if latex and is_plausible_latex(latex):
            latex_parts.append(latex)
    if not latex_parts:
        return None

    if len(latex_parts) == 1:
        latex = latex_parts[0]
    else:
        body = " \\\\\n".join(latex_parts)
        latex = f"\\begin{{aligned}}\n{body}\n\\end{{aligned}}"
    if tag:
        latex = f"{latex} \\tag{{{tag}}}"
    return FormulaResult(latex=latex, tag=tag, engine=recognizer.name, parts=len(latex_parts))


def postprocess_latex(latex: str, collapse_letter_runs: bool = True) -> str:
    if not latex:
        return ""
    latex = latex.strip()
    latex = re.sub(r"^\$+|\$+$", "", latex).strip()
    latex = re.sub(r"^\\\[|\\\]$", "", latex).strip()
    latex = re.sub(r"[ \t]{2,}", " ", latex)
    if collapse_letter_runs:
        latex = _collapse_letter_runs(latex)
    return latex.strip()


_ENV_SPEC_RE = re.compile(r"\\begin\{(?:array|tabular|tabularx)\}\{[^}]*\}")


def _collapse_letter_runs(latex: str) -> str:
    """``T r a n s(x)`` -> ``\\mathrm{Trans}(x)``.

    Recognizers emit function names as separate italic variables; upright text
    is both more faithful to the source and easier for a model to learn.
    Column specifications such as ``\\begin{array}{c c c}`` look exactly like a
    letter run, so they are masked out first.
    """
    protected: list[str] = []

    def hide(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"\x00{len(protected) - 1}\x00"

    masked = _ENV_SPEC_RE.sub(hide, latex)

    def repl(match: re.Match[str]) -> str:
        letters = re.sub(r"\s+", "", match.group(0))
        return rf"\mathrm{{{letters}}}"

    collapsed = re.sub(r"(?<![A-Za-z\\])(?:[A-Za-z] ){2,}[A-Za-z](?![A-Za-z])", repl, masked)
    return re.sub(r"\x00(\d+)\x00", lambda m: protected[int(m.group(1))], collapsed)


def is_plausible_latex(latex: str) -> bool:
    """Reject recognizer hallucinations before they reach the dataset."""
    if not latex or len(latex) > _MAX_LATEX_CHARS:
        return False
    if latex.count("{") != latex.count("}"):
        return False
    if latex.count(r"\begin") != latex.count(r"\end"):
        return False
    if re.search(r"(\\not){3,}", latex):
        return False
    # the same macro repeated many times in a row is a degenerate decode loop
    macros = re.findall(r"\\[A-Za-z]+", latex)
    if macros:
        longest = 1
        current = 1
        for previous, macro in zip(macros, macros[1:]):
            current = current + 1 if macro == previous else 1
            longest = max(longest, current)
        if longest >= 12:
            return False
    letters = re.sub(r"[^A-Za-z0-9]", "", re.sub(r"\\[A-Za-z]+", "", latex))
    return bool(letters) or bool(re.search(r"\\(frac|sqrt|sum|int|begin)", latex))


def _column_profile(image, dark_threshold: int = 200):
    import numpy as np

    array = np.array(image.convert("L"))
    return (array < dark_threshold).sum(axis=0), array


def _column_islands(filled, min_gap: int) -> list[tuple[int, int]]:
    """Runs of ink columns, merging runs closer together than ``min_gap``.

    Merging matters: the glyphs of "(1-26)" are separated by blank columns, so
    without it the equation number looks like several tiny islands.
    """
    islands: list[tuple[int, int]] = []
    start: int | None = None
    for index, value in enumerate(filled):
        if value and start is None:
            start = index
        elif not value and start is not None:
            islands.append((start, index))
            start = None
    if start is not None:
        islands.append((start, len(filled)))

    merged: list[tuple[int, int]] = []
    for island in islands:
        if merged and island[0] - merged[-1][1] < min_gap:
            merged[-1] = (merged[-1][0], island[1])
        else:
            merged.append(island)
    return merged


def _split_equation_number(image, min_gap_ratio: float = 0.04, max_tag_ratio: float = 0.28):
    """Cut a right-aligned equation number, e.g. ``(1-26)``, off the region."""
    columns, _ = _column_profile(image)
    width = len(columns)
    if width < 80:
        return image, None

    min_gap = max(8, int(width * min_gap_ratio))
    islands = _column_islands(columns > 0, min_gap)
    if len(islands) < 2:
        return image, None

    tag_start, tag_end = islands[-1]
    if (tag_end - tag_start) > width * max_tag_ratio:
        return image, None

    # the separating gap must be the widest one in the region, otherwise the
    # "island" is just the closing bracket of a wide matrix
    gaps = [right[0] - left[1] for left, right in zip(islands, islands[1:])]
    if gaps[-1] < max(min_gap, max(gaps[:-1] or [0])):
        return image, None

    cut = (islands[-2][1] + tag_start) // 2
    tag = _read_equation_tag(image.crop((cut, 0, width, image.height)))
    if tag is None:
        # unreadable island: keep the region intact rather than risk cutting math
        return image, None
    return image.crop((0, 0, cut, image.height)), tag


_TAG_RE = re.compile(r"^[\(\[]?[0-9A-Za-z][0-9A-Za-z.\-\u2013]{0,10}[\)\]]?$")


def _read_equation_tag(image) -> str | None:
    """OCR the tiny equation-number crop with a restricted character set."""
    tesseract = shutil.which("tesseract")
    if tesseract is None:
        return None
    with tempfile.TemporaryDirectory(prefix="kdp-tag-") as tmp:
        src = Path(tmp) / "tag.png"
        image.save(src)
        cmd = [
            tesseract,
            str(src),
            "stdout",
            "--psm",
            "7",
            "-c",
            "tessedit_char_whitelist=0123456789().-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        except (OSError, subprocess.TimeoutExpired):
            return None
    raw = (proc.stdout or "").strip().replace(" ", "")
    raw = raw.replace("\u2212", "-")
    if not raw or not _TAG_RE.match(raw):
        return None
    return raw.strip("()[]") or None


def _split_stacked_equations(
    image,
    dark_threshold: int = 200,
    min_gap: int = 8,
    min_band: int = 12,
    pad: int = 4,
    max_parts: int = 12,
):
    """Split a region on blank horizontal bands (one equation per band)."""
    import numpy as np

    array = np.array(image.convert("L"))
    rows = (array < dark_threshold).sum(axis=1) > 0
    bands: list[tuple[int, int]] = []
    start: int | None = None
    for index, filled in enumerate(rows):
        if filled and start is None:
            start = index
        elif not filled and start is not None:
            if index - start >= min_band:
                bands.append((start, index))
            start = None
    if start is not None:
        bands.append((start, len(rows)))
    if not bands:
        return [image]

    merged: list[tuple[int, int]] = []
    for band in bands:
        if merged and band[0] - merged[-1][1] < min_gap:
            merged[-1] = (merged[-1][0], band[1])
        else:
            merged.append(band)
    if len(merged) <= 1 or len(merged) > max_parts:
        return [image]

    height = array.shape[0]
    return [
        image.crop((0, max(0, top - pad), image.width, min(height, bottom + pad)))
        for top, bottom in merged
    ]
