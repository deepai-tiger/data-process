"""Text normalization for Korean OCR / Word output.

Order matters: character-level repairs first, then line joining, then
page-structure repairs (running headers, footers, cross-page paragraphs).
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field

from ..config import NormalizeConfig
from ..schema import Block, BlockKind, Document

HANGUL = r"\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f"
CJK = r"\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff"

_PRIVATE_USE = re.compile(r"[\ue000-\uf8ff\U000f0000-\U000ffffd]")
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_FORMAT = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff\u00ad]")
_REPLACEMENT = re.compile(r"[\ufffd\ufffc]")

_PUNCT_MAP = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201a": "'",
    "\u201b": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u201e": '"',
    "\u2032": "'",
    "\u2033": '"',
    "\u2010": "-",
    "\u2011": "-",
    "\u2012": "-",
    "\u2013": "-",
    "\u2014": "-",
    "\u2015": "-",
    "\u2212": "-",
    "\uff0d": "-",
    "\u00b7": "\u00b7",
    "\u30fb": "\u00b7",
    "\uff0e": ".",
    "\uff0c": ",",
    "\uff1a": ":",
    "\uff1b": ";",
    "\uff01": "!",
    "\uff1f": "?",
    "\uff05": "%",
    "\uff08": "(",
    "\uff09": ")",
    "\uff5e": "~",
    "\u223c": "~",
    "\u2026": "...",
    "\u22ef": "...",
    "\u00a0": " ",
    "\u3000": " ",
    "\u2009": " ",
    "\u202f": " ",
}
_PUNCT_RE = re.compile("|".join(re.escape(k) for k in _PUNCT_MAP))

_PAGE_NUMBER_RE = re.compile(
    r"""^[\s\-\u2013\u2014\u2015\[\(<]*            # decorations before
        (?:page\s*)?(?:\d{1,4}|[ivxlcdm]{1,6})     # arabic or roman page number
        (?:\s*/\s*\d{1,4})?                        # 12 / 345
        [\s\-\u2013\u2014\u2015\]\)>\.]*$          # decorations after
    """,
    re.IGNORECASE | re.VERBOSE,
)
_DOT_LEADER_RE = re.compile(r"[.\u00b7\u2027\u2219\u22ef\uff0e]{5,}")
_SENTENCE_END_RE = re.compile(r'[.!?。\u3002]["\'\u201d\u2019\)\]]?\s*$|[다라요음임함됨))]\.?\s*$')


@dataclass
class NormalizeReport:
    blocks_in: int = 0
    blocks_out: int = 0
    page_artifacts: int = 0
    merged_paragraphs: int = 0
    repeated_lines_removed: int = 0
    details: dict[str, int] = field(default_factory=dict)

    def as_dict(self) -> dict[str, int | dict[str, int]]:
        return {
            "blocks_in": self.blocks_in,
            "blocks_out": self.blocks_out,
            "page_artifacts": self.page_artifacts,
            "merged_paragraphs": self.merged_paragraphs,
            "repeated_lines_removed": self.repeated_lines_removed,
            "details": self.details,
        }


def normalize_text(text: str, cfg: NormalizeConfig, keep_newlines: bool = False) -> str:
    if not text:
        return ""
    text = unicodedata.normalize(cfg.unicode_form, text)
    if cfg.strip_control_chars:
        text = _CONTROL.sub("", text)
        text = _FORMAT.sub("", text)
        text = _PRIVATE_USE.sub("", text)
        text = _REPLACEMENT.sub("", text)
    if cfg.normalize_punctuation:
        text = _PUNCT_RE.sub(lambda m: _PUNCT_MAP[m.group(0)], text)
        text = _DOT_LEADER_RE.sub(" ... ", text)
    if cfg.dehyphenate:
        # English words split across OCR lines: "recog-\nnition" -> "recognition"
        text = re.sub(r"([A-Za-z])-[ \t]*\n[ \t]*([a-z])", r"\1\2", text)
    if cfg.join_wrapped_lines and not keep_newlines:
        text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
    else:
        text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r" ([,.!?%\)\]}])", r"\1", text)
    text = re.sub(r"([\(\[{]) ", r"\1", text)
    return text.strip()


def normalize_document(doc: Document, cfg: NormalizeConfig) -> tuple[Document, NormalizeReport]:
    report = NormalizeReport(blocks_in=len(doc.blocks))

    for block in doc.blocks:
        if block.kind in (BlockKind.TABLE, BlockKind.EQUATION):
            # LaTeX payloads are normalized structurally, never re-wrapped
            if block.latex:
                block.latex = _normalize_latex(block.latex, cfg)
                block.text = block.latex
            if block.kind is BlockKind.TABLE:
                _drop_noisy_caption(block)
            continue
        keep_newlines = block.kind is BlockKind.CODE
        block.text = normalize_text(block.text, cfg, keep_newlines=keep_newlines)

    blocks = [b for b in doc.blocks if b.payload.strip() or b.kind is BlockKind.PAGE_ARTIFACT]

    if cfg.drop_page_numbers or cfg.header_footer_page_ratio > 0:
        blocks, marked = _mark_page_artifacts(blocks, cfg)
        report.page_artifacts = marked

    blocks, removed = _drop_repeated_short_lines(blocks)
    report.repeated_lines_removed = removed

    if cfg.merge_page_continuations:
        blocks, merged = _merge_continuations(blocks)
        report.merged_paragraphs = merged

    doc.blocks = blocks
    report.blocks_out = len(blocks)
    doc.meta.setdefault("normalize", {}).update(report.as_dict())
    return doc, report


def _normalize_latex(latex: str, cfg: NormalizeConfig) -> str:
    latex = unicodedata.normalize("NFC", latex)
    latex = _CONTROL.sub("", latex)
    latex = _FORMAT.sub("", latex)
    latex = _PRIVATE_USE.sub("", latex)
    latex = re.sub(r"[ \t]{2,}", " ", latex)
    return re.sub(r"\n{3,}", "\n\n", latex).strip()


def _drop_noisy_caption(block: Block) -> None:
    """Remove a table caption that OCR turned into gibberish."""
    from .quality import is_ocr_noise

    caption = (block.meta.get("caption") or "").strip()
    if not caption or not is_ocr_noise(caption):
        return
    block.meta["caption_rejected"] = caption
    block.meta["caption"] = None
    if block.latex:
        block.latex = re.sub(r"\n?\\caption\{[^\n]*\}", "", block.latex)
        block.text = block.latex


def _page_signature(text: str) -> str:
    """Header/footer text with volatile parts (numbers) blanked out."""
    signature = re.sub(r"\d+", "#", text.strip())
    return re.sub(r"\s+", " ", signature).lower()


def _mark_page_artifacts(blocks: list[Block], cfg: NormalizeConfig) -> tuple[list[Block], int]:
    pages = sorted({b.page for b in blocks if b.page is not None})
    marked = 0

    if cfg.drop_page_numbers:
        for block in blocks:
            if block.kind in (BlockKind.TABLE, BlockKind.EQUATION, BlockKind.CODE):
                continue
            text = block.text.strip()
            if text and len(text) <= 16 and _PAGE_NUMBER_RE.match(text):
                block.kind = BlockKind.PAGE_ARTIFACT
                block.meta["artifact"] = "page_number"
                marked += 1

    if len(pages) >= 3 and cfg.header_footer_page_ratio > 0:
        candidates: Counter[str] = Counter()
        by_page: dict[int, list[Block]] = {}
        for block in blocks:
            if block.page is None:
                continue
            by_page.setdefault(block.page, []).append(block)
        for page_blocks in by_page.values():
            edges = [b for b in (page_blocks[0], page_blocks[-1]) if b.kind not in (BlockKind.TABLE, BlockKind.EQUATION)]
            for block in edges:
                text = block.text.strip()
                if 0 < len(text) <= 80:
                    candidates[_page_signature(text)] += 1
        threshold = max(2, int(len(pages) * cfg.header_footer_page_ratio))
        repeated = {sig for sig, count in candidates.items() if count >= threshold}
        if repeated:
            for page_blocks in by_page.values():
                for block in (page_blocks[0], page_blocks[-1]):
                    if block.kind in (BlockKind.TABLE, BlockKind.EQUATION, BlockKind.PAGE_ARTIFACT):
                        continue
                    if _page_signature(block.text) in repeated:
                        block.kind = BlockKind.PAGE_ARTIFACT
                        block.meta["artifact"] = "running_header_footer"
                        marked += 1
    return blocks, marked


def _drop_repeated_short_lines(blocks: list[Block]) -> tuple[list[Block], int]:
    """Remove consecutive duplicate short blocks (OCR stutter on decorations)."""
    out: list[Block] = []
    removed = 0
    for block in blocks:
        if (
            out
            and block.kind is out[-1].kind
            and block.kind in (BlockKind.PARAGRAPH, BlockKind.LIST_ITEM, BlockKind.CAPTION)
            and block.text == out[-1].text
            and len(block.text) <= 40
        ):
            removed += 1
            continue
        out.append(block)
    return out, removed


#: Korean document headings, in order of decreasing scope
_HEADING_PATTERNS: tuple[tuple[re.Pattern[str], int], ...] = (
    (re.compile(r"^제\s*\d+\s*(?:편|부)\b"), 1),
    (re.compile(r"^제\s*\d+\s*장\b"), 1),
    (re.compile(r"^제\s*\d+\s*절\b"), 2),
    (re.compile(r"^제\s*\d+\s*(?:항|조)\b"), 3),
    (re.compile(r"^\d+\.\d+\.\d+\.?\s+\S"), 4),
    (re.compile(r"^\d+\.\d+\.?\s+\S"), 3),
    (re.compile(r"^\d+\.\s+\S"), 2),
    (re.compile(r"^\(\d+\)\s+\S"), 3),
    (re.compile(r"^[\u3131-\u314e]\.\s+\S"), 3),
)
_MAX_HEADING_CHARS = 60


def infer_structure(doc: Document, cfg: NormalizeConfig) -> Document:
    """Promote heading-looking paragraphs to real headings.

    Legacy .doc files and OCR output often carry no style information, so
    "제 13 절 중독" arrives as a plain paragraph. Recovering the hierarchy is
    what lets chunking follow section boundaries later.
    """
    if not cfg.infer_headings:
        return doc
    promoted = 0
    for block in doc.blocks:
        if block.kind is not BlockKind.PARAGRAPH:
            continue
        text = block.text.strip()
        if not text or len(text) > _MAX_HEADING_CHARS or "\n" in text:
            continue
        if _SENTENCE_END_RE.search(text) and not re.match(r"^제\s*\d+\s*[장절편부항조]", text):
            continue
        for pattern, level in _HEADING_PATTERNS:
            if pattern.match(text):
                block.kind = BlockKind.HEADING
                block.level = level
                block.meta["heading_source"] = "inferred"
                promoted += 1
                break
    if promoted:
        doc.meta.setdefault("normalize", {})["headings_inferred"] = promoted
    return doc


def sanitize_title(doc: Document) -> Document:
    """Drop a document title that is mojibake (wrong legacy code page).

    Binary .doc metadata is frequently stored in a code page unrelated to the
    body text, so the title comes back as CJK garbage while the body is fine.
    """
    from .quality import script_profile

    title = (doc.title or "").strip()
    if title:
        profile = script_profile(title)
        if profile["hangul"] < 0.3 and (profile["cjk"] > 0.3 or profile["kana"] > 0.1):
            doc.meta["title_rejected"] = title
            doc.title = None
    if not doc.title:
        for block in doc.blocks:
            if block.kind in (BlockKind.TITLE, BlockKind.HEADING):
                doc.title = block.text.strip()
                break
    return doc


def _merge_continuations(blocks: list[Block]) -> tuple[list[Block], int]:
    """Join a paragraph that was split by a page or column break."""
    out: list[Block] = []
    merged = 0
    for block in blocks:
        if (
            out
            and block.kind is BlockKind.PARAGRAPH
            and out[-1].kind is BlockKind.PARAGRAPH
            and out[-1].page is not None
            and block.page is not None
            and block.page != out[-1].page
            and not _SENTENCE_END_RE.search(out[-1].text)
            and block.text[:1] not in ("", "-", "\u2022")
            and not re.match(rf"^[{HANGUL}]?\s*\d+[.)]", block.text)
        ):
            previous = out[-1]
            previous.text = f"{previous.text} {block.text}".strip()
            previous.meta.setdefault("merged_pages", [previous.page])
            previous.meta["merged_pages"].append(block.page)
            merged += 1
            continue
        out.append(block)
    return out, merged
