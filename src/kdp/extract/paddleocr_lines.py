"""Turn PaddleOCR line JSON into the pipeline's structured document schema.

This adapter is intentionally conservative: it repairs page-image line wraps
and document structure, but it never substitutes recognized Korean characters
or converts North Korean words to South Korean spelling.
"""

from __future__ import annotations

import re
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from ..schema import Block, BlockKind, Document

_HANGUL_WORD = re.compile(r"[가-힣]+")
_LIST_MARKER = re.compile(r"^(?:[①-⑳]|\d+[.)]|\d+(?=\s|$)|[*•])\s*")
_PAGE_NUMBER = re.compile(r"^\d{1,3}$")
_STANDALONE_ONE_SYLLABLE_WORDS = frozenset({"이", "그", "저", "한", "또", "더", "매"})


@dataclass(frozen=True)
class OcrLine:
    text: str
    confidence: float
    bbox: tuple[int, int, int, int]

    @property
    def left(self) -> int:
        return self.bbox[0]

    @property
    def top(self) -> int:
        return self.bbox[1]

    @property
    def right(self) -> int:
        return self.bbox[2]

    @property
    def bottom(self) -> int:
        return self.bbox[3]

    @property
    def height(self) -> int:
        return self.bottom - self.top


def document_from_paddleocr(
    payload: dict[str, Any],
    *,
    source_path: str,
    doc_id: str,
    title: str | None = None,
    min_confidence: float = 0.8,
) -> Document:
    """Build a :class:`Document` from ``paddleocr_trial.py`` JSON output."""
    pages = payload.get("pages") or []
    doc = Document(
        doc_id=doc_id,
        source_path=source_path,
        source_type="pdf",
        title=title,
        n_pages=len(pages),
        meta={
            "extractor": "paddleocr_page_images",
            "ocr_engine": "paddleocr",
            "ocr_model": "korean_PP-OCRv5_mobile_rec",
            "pages_processed": [int(page["page"]) for page in pages],
            "orthography_normalized": False,
        },
    )
    analyzer = _load_kiwi()
    for page in pages:
        page_no = int(page["page"])
        raw_lines = [_line_from_dict(raw) for raw in page.get("lines") or []]
        lines = _filter_lines(raw_lines, min_confidence)
        doc.blocks.extend(_page_blocks(lines, page_no, analyzer))
    doc.blocks = _merge_page_continuations(doc.blocks, analyzer)
    return doc


def line_join_separator(left_text: str, right_text: str, analyzer: Any = None) -> str:
    """Choose ``""`` for a word split by a page line, otherwise ``" "``.

    Existing spaces inside each OCR line are untouched. When Kiwi is present,
    only its token-boundary score is consulted; ``Kiwi.space`` is deliberately
    not used because it can impose South Korean spacing on North Korean words.
    """
    left_match = list(_HANGUL_WORD.finditer(left_text))
    right_match = _HANGUL_WORD.search(right_text)
    if not left_match or right_match is None:
        return " "
    left_word = left_match[-1].group(0)
    right_word = right_match.group(0)
    if analyzer is None:
        return ""

    joined = left_word + right_word
    spaced = f"{left_word} {right_word}"
    try:
        joined_tokens, joined_score = analyzer.analyze(joined, top_n=1)[0]
        _, spaced_score = analyzer.analyze(spaced, top_n=1)[0]
    except Exception:
        return ""
    if joined_score > spaced_score + 0.05:
        return ""
    if spaced_score > joined_score + 0.05:
        return " "

    boundary = len(left_word)
    if any(token.start < boundary < token.start + token.len for token in joined_tokens):
        return ""
    if len(left_word) == 1 and left_word in _STANDALONE_ONE_SYLLABLE_WORDS:
        return " "
    # Unknown one-syllable North Korean word fragments (e.g. 련+결) receive
    # equal scores and separate tokens in a South Korean analyzer.
    return "" if len(left_word) == 1 else " "


def _line_from_dict(raw: dict[str, Any]) -> OcrLine:
    box = raw.get("bbox") or [0, 0, 0, 0]
    return OcrLine(
        text=str(raw.get("text") or "").strip(),
        confidence=float(raw.get("confidence") or 0.0),
        bbox=tuple(int(value) for value in box),
    )


def _filter_lines(lines: list[OcrLine], min_confidence: float) -> list[OcrLine]:
    kept: list[OcrLine] = []
    for index, line in enumerate(lines):
        if not line.text or line.confidence < min_confidence:
            continue
        if _PAGE_NUMBER.fullmatch(line.text) and line.bottom >= 1360:
            continue
        if _PAGE_NUMBER.fullmatch(line.text) and line.right - line.left < 20:
            continue
        next_top = lines[index + 1].top if index + 1 < len(lines) else line.bottom
        if len(line.text) <= 6 and line.top < 600 and next_top - line.bottom > 200:
            # Isolated labels and strokes in a large illustration.
            continue
        kept.append(line)
    return _merge_same_row_markers(kept)


def _merge_same_row_markers(lines: list[OcrLine]) -> list[OcrLine]:
    merged: list[OcrLine] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if (
            index + 1 < len(lines)
            and _LIST_MARKER.fullmatch(line.text)
            and abs(line.top - lines[index + 1].top) <= 12
        ):
            following = lines[index + 1]
            merged.append(
                OcrLine(
                    text=f"{line.text} {following.text}",
                    confidence=min(line.confidence, following.confidence),
                    bbox=(
                        min(line.left, following.left),
                        min(line.top, following.top),
                        max(line.right, following.right),
                        max(line.bottom, following.bottom),
                    ),
                )
            )
            index += 2
            continue
        merged.append(line)
        index += 1
    return merged


def _page_blocks(lines: list[OcrLine], page_no: int, analyzer: Any) -> list[Block]:
    if not lines:
        return []
    prose_heights = [line.height for line in lines if len(line.text) > 2]
    median_height = statistics.median(prose_heights) if prose_heights else 30
    blocks: list[Block] = []
    pending: list[OcrLine] = []
    pending_kind = BlockKind.PARAGRAPH

    def flush() -> None:
        nonlocal pending
        if not pending:
            return
        text = _join_lines(pending, analyzer)
        text = _normalize_dprk_punctuation(text)
        blocks.append(
            Block(
                kind=pending_kind,
                text=text,
                page=page_no,
                bbox=(
                    min(line.left for line in pending),
                    min(line.top for line in pending),
                    max(line.right for line in pending),
                    max(line.bottom for line in pending),
                ),
                confidence=round(min(line.confidence for line in pending), 6),
                meta={"source": "paddleocr_lines", "line_count": len(pending)},
            )
        )
        pending = []

    for index, line in enumerate(lines):
        previous = lines[index - 1] if index else None
        following = lines[index + 1] if index + 1 < len(lines) else None
        if _is_heading(line, median_height, previous, following):
            flush()
            blocks.append(
                Block(
                    kind=BlockKind.HEADING,
                    text=_normalize_dprk_punctuation(line.text),
                    level=2,
                    page=page_no,
                    bbox=line.bbox,
                    confidence=line.confidence,
                    meta={"source": "paddleocr_lines"},
                )
            )
            continue

        kind = BlockKind.LIST_ITEM if _LIST_MARKER.match(line.text) else BlockKind.PARAGRAPH
        starts_paragraph = line.left >= 145
        large_gap = bool(pending and line.top - pending[-1].bottom > median_height * 2)
        if pending_kind is BlockKind.LIST_ITEM and kind is BlockKind.PARAGRAPH:
            # OCR emits the marker only on the first physical line.
            if large_gap:
                flush()
                pending_kind = BlockKind.PARAGRAPH
            else:
                kind = BlockKind.LIST_ITEM
        if pending and (
            (kind is not pending_kind)
            or (kind is not BlockKind.LIST_ITEM and starts_paragraph)
            or (kind is BlockKind.LIST_ITEM and _LIST_MARKER.match(line.text))
        ):
            flush()
        pending_kind = kind
        pending.append(line)
    flush()
    return blocks


def _is_heading(
    line: OcrLine,
    median_height: float,
    previous: OcrLine | None,
    following: OcrLine | None,
) -> bool:
    text = line.text.strip()
    if _LIST_MARKER.match(text) or re.search(r"[!?。]|\.$", text):
        return False
    compact_length = len(re.sub(r"\s+", "", text))
    if compact_length < 3 or compact_length > 35:
        return False
    if re.match(r"^제\s*\d+\s*장(?:\s|[.:·-]|$)", text):
        return True
    previous_gap = line.top - previous.bottom if previous is not None else 0
    following_gap = following.top - line.bottom if following is not None else 0
    separated = max(previous_gap, following_gap) >= median_height
    average_glyph_width = (line.right - line.left) / compact_length
    first_line_title = (
        previous is None
        and following_gap >= median_height
        and compact_length <= 25
        and average_glyph_width >= 35
    )
    return (
        first_line_title
        or bool(re.match(r"^건강단련법\s*\d+", text))
        or (average_glyph_width >= 35 and separated)
    )


def _join_lines(lines: Iterable[OcrLine], analyzer: Any) -> str:
    materialized = list(lines)
    if not materialized:
        return ""
    text = materialized[0].text
    for line in materialized[1:]:
        separator = line_join_separator(text, line.text, analyzer)
        text = f"{text}{separator}{line.text}"
    return text


def _merge_page_continuations(blocks: list[Block], analyzer: Any) -> list[Block]:
    merged: list[Block] = []
    for block in blocks:
        if (
            merged
            and block.kind is BlockKind.PARAGRAPH
            and merged[-1].kind is BlockKind.PARAGRAPH
            and block.page != merged[-1].page
            and not re.search(r"[.!?。》]\s*$", merged[-1].text)
        ):
            previous = merged[-1]
            separator = line_join_separator(previous.text, block.text, analyzer)
            previous.text = f"{previous.text}{separator}{block.text}"
            previous.meta.setdefault("merged_pages", [previous.page])
            previous.meta["merged_pages"].append(block.page)
            previous.confidence = min(
                value for value in (previous.confidence, block.confidence) if value is not None
            )
            continue
        merged.append(block)
    return merged


def _normalize_dprk_punctuation(text: str) -> str:
    text = text.replace("<", "《").replace(">", "》").replace("»", "》")
    text = re.sub(r"([.!?])(?=[가-힣《])", r"\1 ", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def _load_kiwi() -> Any:
    try:
        from kiwipiepy import Kiwi
    except ImportError:
        return None
    return Kiwi()
