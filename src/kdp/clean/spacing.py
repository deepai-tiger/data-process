"""Korean word-spacing (띄어쓰기) repair for OCR text.

Tesseract's Korean model segments text syllable by syllable, so a line comes
back as "널리 리 용 한다" instead of "널리 리용한다". Left alone, this teaches a
model broken spacing, so OCR-sourced text is re-spaced with Kiwi's statistical
spacing model before anything else looks at it.

Word-sourced text is already correctly spaced and is left untouched.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

from ..schema import Block, BlockKind, Document

logger = logging.getLogger(__name__)

_SYLLABLE_SPACE_RE = re.compile(r"(?:[\uac00-\ud7a3]\s){2,}[\uac00-\ud7a3]")
_MATH_SPAN_RE = re.compile(r"\$[^$]*\$")


@dataclass
class SpacingReport:
    blocks_processed: int = 0
    blocks_changed: int = 0
    engine: str = "none"

    def as_dict(self) -> dict[str, object]:
        return {
            "engine": self.engine,
            "blocks_processed": self.blocks_processed,
            "blocks_changed": self.blocks_changed,
        }


class KiwiSpacer:
    """Wraps :mod:`kiwipiepy`'s spacing model (CPU, ~40 MB, fast)."""

    name = "kiwi"

    def __init__(self) -> None:
        try:
            from kiwipiepy import Kiwi
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise RuntimeError(
                "kiwipiepy is not installed; `pip install kiwipiepy` or set clean.spacing_engine=none"
            ) from exc
        self._kiwi = Kiwi()

    def fix(self, text: str) -> str:
        return self._kiwi.space(text, reset_whitespace=True)


class NoopSpacer:
    name = "none"

    def fix(self, text: str) -> str:
        return text


def build_spacer(engine: str):
    if engine == "kiwi":
        return KiwiSpacer()
    if engine == "none":
        return NoopSpacer()
    raise ValueError(f"unknown spacing engine: {engine}")


def needs_spacing_fix(text: str, min_syllable_runs: int = 1) -> bool:
    """True when the text shows the syllable-splitting signature of OCR."""
    return len(_SYLLABLE_SPACE_RE.findall(text)) >= min_syllable_runs


def fix_spacing(text: str, spacer) -> str:
    """Re-space Korean text, leaving inline LaTeX spans byte-identical."""
    if not text.strip():
        return text
    spans = list(_MATH_SPAN_RE.finditer(text))
    if not spans:
        return spacer.fix(text)
    out: list[str] = []
    cursor = 0
    for span in spans:
        segment = text[cursor : span.start()]
        out.append(spacer.fix(segment) if segment.strip() else segment)
        out.append(span.group(0))
        cursor = span.end()
    tail = text[cursor:]
    out.append(spacer.fix(tail) if tail.strip() else tail)
    return re.sub(r"\s{2,}", " ", "".join(out)).strip()


def respace_document(doc: Document, engine: str = "kiwi", only_ocr: bool = True) -> tuple[Document, SpacingReport]:
    report = SpacingReport(engine=engine)
    if engine == "none":
        return doc, report
    if only_ocr and doc.source_type != "pdf":
        report.engine = "skipped(non-ocr source)"
        return doc, report

    spacer = build_spacer(engine)
    for block in doc.blocks:
        if block.kind in (BlockKind.TABLE, BlockKind.EQUATION, BlockKind.CODE):
            continue
        original = block.text
        if not needs_spacing_fix(original):
            continue
        report.blocks_processed += 1
        fixed = fix_spacing(original, spacer)
        if fixed and fixed != original:
            block.text = fixed
            block.meta["respaced"] = True
            report.blocks_changed += 1

    for block in doc.blocks:
        if block.kind is BlockKind.TABLE and block.meta.get("cells"):
            _respace_table_cells(block, spacer, report)

    doc.meta.setdefault("spacing", {}).update(report.as_dict())
    return doc, report


def _respace_table_cells(block: Block, spacer, report: SpacingReport) -> None:
    """Re-space table cell text and rebuild the LaTeX from the fixed cells."""
    from ..extract.latex_table import TableCell, TableGrid, grid_to_latex

    changed = False
    cells: list[TableCell] = []
    for raw in block.meta["cells"]:
        text = raw["text"]
        if needs_spacing_fix(text):
            report.blocks_processed += 1
            fixed = fix_spacing(text, spacer)
            if fixed and fixed != text:
                raw["text"] = fixed
                text = fixed
                changed = True
        cells.append(
            TableCell(
                text=text,
                row=raw["row"],
                col=raw["col"],
                row_span=raw["row_span"],
                col_span=raw["col_span"],
                is_header=raw["is_header"],
            )
        )

    caption = block.meta.get("caption")
    if caption and needs_spacing_fix(caption):
        fixed = fix_spacing(caption, spacer)
        report.blocks_processed += 1
        if fixed and fixed != caption:
            block.meta["caption"] = caption = fixed
            changed = True

    if not changed:
        return
    grid = TableGrid(
        cells=cells,
        num_rows=block.meta.get("num_rows", 0),
        num_cols=block.meta.get("num_cols", 0),
        caption=caption,
    ).normalize()
    latex = grid_to_latex(grid)
    if latex:
        block.latex = latex
        block.text = latex
        block.meta["respaced"] = True
        report.blocks_changed += 1
