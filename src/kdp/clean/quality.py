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


@dataclass
class QualityReport:
    kept_blocks: int = 0
    dropped_blocks: int = 0
    reasons: Counter = field(default_factory=Counter)
    doc_reason: str | None = None
    scores: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return {
            "kept_blocks": self.kept_blocks,
            "dropped_blocks": self.dropped_blocks,
            "reasons": dict(self.reasons),
            "doc_reason": self.doc_reason,
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
        return None
    if len(text) < cfg.min_block_chars:
        return "too_short"
    if looks_like_toc(text):
        return "toc_line"

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
    for block in doc.blocks:
        reason = block_drop_reason(block, cfg)
        if reason is None:
            kept.append(block)
            report.kept_blocks += 1
        else:
            report.dropped_blocks += 1
            report.reasons[reason] += 1
    doc.blocks = kept

    text = doc.to_markdown()
    report.scores = {**script_profile(text), **repetition_ratios(text), "chars": float(len(text))}
    report.doc_reason = _document_drop_reason(text, report.scores, cfg)
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
    """Chunk-level gate applied right before a sample enters the dataset."""
    stripped = text.strip()
    if len(stripped) < cfg.min_doc_chars // 4:
        return "chunk_too_short"
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
