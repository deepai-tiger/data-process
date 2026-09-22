"""Heuristic quality filters for Korean document text.

The filters are deliberately explainable: every drop carries a reason string so
that ``out/reports/`` shows exactly why content disappeared, which is what you
need when tuning a corpus. Rules follow the usual pretraining-corpus playbook
(Gopher/C4-style) adapted to Hangul.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Sequence

from ..config import QualityConfig
from ..schema import Block, BlockKind, Document

_HANGUL_RE = re.compile(r"[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f]")
_CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
_KANA_RE = re.compile(r"[\u3040-\u30ff]")
_LATIN_RE = re.compile(r"[A-Za-z]")
_DIGIT_RE = re.compile(r"[0-9]")
_LETTERISH_RE = re.compile(r"[^\W\d_]", re.UNICODE)
_SYMBOL_RE = re.compile(r"[^\w\s\uac00-\ud7a3.,!?;:'\"()\[\]{}\-%/&\u00b7\u2026]", re.UNICODE)
_TOC_RE = re.compile(r"(?:\.\s*){5,}\d|\.{4,}\s*\d|\u2026{2,}\s*\d")
_URLISH_RE = re.compile(r"https?://|www\.|@[A-Za-z0-9_]+")
#: leftovers of a dot leader: "---- (23)", "..... 41", "- ㅡ (122)"
_LEADER_RE = re.compile(r"[-\u2014\u2015\u3161.\u00b7]{3,}|\(\s*\d{1,4}\s*\)\s*$|^\s*\d{1,4}\s*$")

_MATH_ENV_RE = re.compile(r"\\begin\{[^}]*\}.*?\\end\{[^}]*\}", re.S)
_DISPLAY_MATH_RE = re.compile(r"\$\$.*?\$\$", re.S)
_INLINE_MATH_RE = re.compile(r"\$[^$\n]*\$")
_LATEX_CMD_RE = re.compile(r"\\[A-Za-z]+(?:\[[^\]]*\])?(?:\{[^{}]*\})*")


def strip_latex(text: str) -> str:
    """Remove LaTeX payloads so prose metrics are not skewed by markup.

    Without this, a page with three tables looks like "50% duplicate lines"
    because every row ends with ``\\hline``.
    """
    without = _MATH_ENV_RE.sub(" ", text)
    without = _DISPLAY_MATH_RE.sub(" ", without)
    without = _INLINE_MATH_RE.sub(" ", without)
    without = _LATEX_CMD_RE.sub(" ", without)
    without = re.sub(r"[&\\]", " ", without)
    return re.sub(r"[ \t]{2,}", " ", without)


#: minimum characters before the noise heuristics are meaningful
_MIN_NOISE_CHARS = 8
#: distinct characters relative to sqrt(length); grows with real vocabulary,
#: stays near zero when the same few glyphs repeat
_MIN_CHAR_DIVERSITY = 2.0


def token_stats(text: str) -> dict[str, float]:
    """Statistics that expose OCR noise such as "아 아 애 아 애 아"."""
    tokens = [t for t in re.split(r"\s+", text.strip()) if t]
    letters = re.sub(r"\s+", "", text)
    if not tokens or not letters:
        return {
            "tokens": 0.0,
            "mean_token_len": 0.0,
            "top_token_ratio": 0.0,
            "char_diversity": 0.0,
        }
    top_count = Counter(tokens).most_common(1)[0][1]
    return {
        "tokens": float(len(tokens)),
        "mean_token_len": sum(len(t) for t in tokens) / len(tokens),
        "top_token_ratio": top_count / len(tokens),
        "char_diversity": len(set(letters)) / (len(letters) ** 0.5),
    }


def is_ocr_noise(text: str) -> bool:
    """True for text that is mostly mis-read decorations rather than words.

    Dot leaders in a table of contents are the usual source: the Korean model
    reads them as "아 아 애 아 애 아", the Latin model as "eee cece eee".

    Note what is *not* used as a signal: Tesseract's Korean model splits normal
    text into single syllables, so a high single-character token ratio says
    nothing about quality here.
    """
    letters = re.sub(r"\s+", "", text)
    if len(letters) < _MIN_NOISE_CHARS:
        return False
    stats = token_stats(text)
    if stats["tokens"] >= 8 and stats["top_token_ratio"] >= 0.4:
        return True
    if stats["char_diversity"] < _MIN_CHAR_DIVERSITY:
        return True
    leader_chars = sum(len(m.group(0)) for m in _LEADER_RE.finditer(text))
    return leader_chars / len(text) > 0.4


def table_drop_reason(block: Block) -> str | None:
    """Reject "tables" that are really diagrams, or whose cells are OCR junk.

    The layout model sometimes labels a technical drawing as a table; the
    resulting grid is mostly empty cells with stray glyphs, which is worse than
    no table at all.
    """
    cells = block.meta.get("cells") or []
    if not cells:
        return None if (block.latex or "").strip() else "empty_latex"

    texts = [str(cell.get("text", "")).strip() for cell in cells]
    filled = [t for t in texts if t]
    if len(filled) / len(texts) < 0.5:
        return "sparse_table"
    meaningful = [t for t in filled if (len(t) >= 2 and _LETTERISH_RE.search(t)) or t.isdigit()]
    if len(meaningful) / len(texts) < 0.4:
        return "noisy_table"
    if is_ocr_noise(" ".join(filled)):
        return "noisy_table"
    if block.meta.get("num_rows", 0) < 2 or block.meta.get("num_cols", 0) < 2:
        return "degenerate_table"
    return None


def looks_like_toc_table(cells: Sequence[dict[str, object]]) -> bool:
    """Table-of-contents pages are detected as tables; they are not content."""
    texts = [str(cell.get("text", "")).strip() for cell in cells]
    filled = [t for t in texts if t]
    if len(filled) < 4:
        return False
    leaders = sum(1 for t in filled if _LEADER_RE.search(t))
    noisy = sum(1 for t in filled if is_ocr_noise(t))
    return (leaders + noisy) / len(filled) >= 0.3


#: drop reasons that indicate a genuinely unusable region (as opposed to a
#: short fragment or a page number), used for the page-level verdict
_NOISE_REASONS = frozenset(
    {
        "ocr_noise",
        "toc_line",
        "toc_table",
        "wrong_script",
        "low_hangul_ratio",
        "symbol_ratio",
        "char_repetition",
        "noisy_table",
        "sparse_table",
    }
)


@dataclass
class QualityReport:
    kept_blocks: int = 0
    dropped_blocks: int = 0
    reasons: Counter = field(default_factory=Counter)
    doc_reason: str | None = None
    scores: dict[str, float] = field(default_factory=dict)
    noisy_pages: list[int] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "kept_blocks": self.kept_blocks,
            "dropped_blocks": self.dropped_blocks,
            "reasons": dict(self.reasons),
            "doc_reason": self.doc_reason,
            "noisy_pages": self.noisy_pages,
            "scores": {k: round(v, 4) for k, v in self.scores.items()},
        }


def script_profile(text: str) -> dict[str, float]:
    """Character-class ratios used by both filters and the dataset card."""
    if not text:
        return {"hangul": 0.0, "cjk": 0.0, "kana": 0.0, "latin": 0.0, "digit": 0.0, "symbol": 0.0}
    total = len(text)
    letterish = len(_LETTERISH_RE.findall(text)) or 1
    return {
        "hangul": len(_HANGUL_RE.findall(text)) / letterish,
        "cjk": len(_CJK_RE.findall(text)) / letterish,
        "kana": len(_KANA_RE.findall(text)) / letterish,
        "latin": len(_LATIN_RE.findall(text)) / letterish,
        "digit": len(_DIGIT_RE.findall(text)) / total,
        "symbol": len(_SYMBOL_RE.findall(text)) / total,
    }


def hangul_ratio(text: str) -> float:
    return script_profile(text)["hangul"]


def repetition_ratios(text: str) -> dict[str, float]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    dup_line_ratio = 0.0
    if len(lines) > 1:
        counts = Counter(lines)
        dup_line_ratio = 1.0 - (len(counts) / len(lines))

    words = text.split()
    top_ngram_ratio = 0.0
    if len(words) >= 20:
        grams = Counter(" ".join(words[i : i + 3]) for i in range(len(words) - 2))
        top, count = grams.most_common(1)[0]
        top_ngram_ratio = (count * len(top.split())) / len(words)

    char_dup = 0.0
    if len(text) >= 40:
        char_dup = max(
            (len(match.group(0)) / len(text) for match in re.finditer(r"(.{2,20}?)\1{2,}", text)),
            default=0.0,
        )
    return {
        "dup_line_ratio": dup_line_ratio,
        "top_ngram_ratio": top_ngram_ratio,
        "char_repeat_ratio": char_dup,
    }


def looks_like_toc(text: str) -> bool:
    if _TOC_RE.search(text):
        return True
    stripped = text.strip()
    if len(stripped) < 200 and re.search(r"\s\.{3,}\s*\d{1,4}\s*$", stripped):
        return True
    return False


def block_drop_reason(block: Block, cfg: QualityConfig) -> str | None:
    """Return why this block should be dropped, or ``None`` to keep it."""
    if block.kind is BlockKind.PAGE_ARTIFACT:
        return "page_artifact"
    if block.kind in (BlockKind.TABLE, BlockKind.EQUATION):
        payload = (block.latex or "").strip()
        if not payload:
            return "empty_latex"
        if block.kind is BlockKind.EQUATION and len(payload) < 2:
            return "equation_too_short"
        if block.kind is BlockKind.TABLE:
            if looks_like_toc_table(block.meta.get("cells", [])):
                return "toc_table"
            return table_drop_reason(block)
        return None
    if block.kind is BlockKind.CODE:
        return None if block.text.strip() else "empty"

    text = block.text.strip()
    if not text:
        return "empty"
    if block.kind in (BlockKind.TITLE, BlockKind.HEADING, BlockKind.CAPTION):
        # headings are short by nature; only obvious garbage is dropped
        if len(text) < 2:
            return "too_short"
        if looks_like_toc(text):
            return "toc_line"
        if is_ocr_noise(text):
            return "ocr_noise"
        return None
    if len(text) < cfg.min_block_chars:
        return "too_short"
    if looks_like_toc(text):
        return "toc_line"
    if is_ocr_noise(text):
        return "ocr_noise"

    profile = script_profile(text)
    if profile["symbol"] > cfg.max_symbol_ratio:
        return "symbol_ratio"
    if profile["digit"] > cfg.max_digit_ratio:
        return "digit_ratio"
    hangul = profile["hangul"]
    if hangul < cfg.min_hangul_ratio:
        latin_only = profile["latin"] > 0.6
        if not (latin_only and cfg.keep_latin_only_blocks):
            # Japanese/Chinese output on a Korean page is the classic signature
            # of a broken PDF text layer or a mis-configured OCR language.
            if profile["kana"] > 0.1 or profile["cjk"] > 0.5:
                return "wrong_script"
            return "low_hangul_ratio"

    repeats = repetition_ratios(text)
    if repeats["char_repeat_ratio"] > 0.5:
        return "char_repetition"
    return None


def filter_document(doc: Document, cfg: QualityConfig) -> tuple[Document, QualityReport]:
    report = QualityReport()
    kept: list[Block] = []
    page_kept: Counter = Counter()
    page_noise: Counter = Counter()

    for block in doc.blocks:
        reason = block_drop_reason(block, cfg)
        if reason is None:
            kept.append(block)
            report.kept_blocks += 1
            page_kept[block.page] += 1
        else:
            report.dropped_blocks += 1
            report.reasons[reason] += 1
            if reason in _NOISE_REASONS:
                page_noise[block.page] += 1

    # A page where most regions were noise is a cover/TOC page: whatever
    # survived on it is almost certainly noise too. Only genuine noise counts
    # here - short fragments and page numbers are normal on any page.
    noisy_pages = {
        page
        for page in page_noise
        if page is not None
        and page_noise[page] >= 3
        and page_noise[page] / (page_noise[page] + page_kept[page]) >= 0.6
    }
    if noisy_pages:
        survivors = [b for b in kept if b.page not in noisy_pages]
        report.reasons["noisy_page"] += len(kept) - len(survivors)
        report.dropped_blocks += len(kept) - len(survivors)
        report.kept_blocks = len(survivors)
        report.noisy_pages = sorted(noisy_pages)
        kept = survivors

    doc.blocks = kept

    text = doc.to_markdown()
    prose = strip_latex(text)
    report.scores = {
        **script_profile(prose),
        **repetition_ratios(prose),
        "chars": float(len(text)),
        "prose_chars": float(len(prose.strip())),
    }
    report.doc_reason = _document_drop_reason(prose, report.scores, cfg)
    doc.meta.setdefault("quality", {}).update(report.as_dict())
    return doc, report


def _document_drop_reason(text: str, scores: dict[str, float], cfg: QualityConfig) -> str | None:
    if len(text.strip()) < cfg.min_doc_chars:
        return "doc_too_short"
    if scores["dup_line_ratio"] > cfg.max_dup_line_ratio:
        return "doc_duplicate_lines"
    if scores["top_ngram_ratio"] > cfg.max_top_ngram_ratio:
        return "doc_ngram_repetition"
    if scores["hangul"] < cfg.min_hangul_ratio and scores["latin"] < 0.6:
        return "doc_not_korean"
    return None


def text_quality_reason(text: str, cfg: QualityConfig) -> str | None:
    """Chunk-level gate applied right before a sample enters the dataset.

    Judged on prose only: a chunk that is mostly a LaTeX table is valuable
    training data, but its markup would fail every prose heuristic.
    """
    prose = strip_latex(text)
    stripped = prose.strip()
    min_chars = cfg.min_doc_chars // 4
    if len(stripped) < min_chars:
        # tables/equations with little surrounding prose are still kept
        return None if len(text.strip()) >= min_chars * 2 else "chunk_too_short"
    profile = script_profile(stripped)
    repeats = repetition_ratios(stripped)
    if profile["symbol"] > cfg.max_symbol_ratio:
        return "chunk_symbol_ratio"
    if profile["hangul"] < cfg.min_hangul_ratio and profile["latin"] < 0.6:
        return "chunk_not_korean"
    if repeats["dup_line_ratio"] > cfg.max_dup_line_ratio:
        return "chunk_duplicate_lines"
    if repeats["top_ngram_ratio"] > cfg.max_top_ngram_ratio:
        return "chunk_ngram_repetition"
    if repeats["char_repeat_ratio"] > 0.4:
        return "chunk_char_repetition"
    return None
