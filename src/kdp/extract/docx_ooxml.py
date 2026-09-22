"""Structure-preserving .docx extraction.

Word files are already structured, so there is nothing to OCR here: we walk the
OOXML tree directly. What matters is not losing the parts a naive text dump
throws away, namely tables (-> LaTeX ``tabular``) and equations (OMML -> LaTeX).
Images are skipped by design; only a counter is kept for traceability.
"""

from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

from lxml import etree

from ..config import Config, WordConfig
from ..schema import Block, BlockKind, Document, slugify
from .latex_table import TableCell, TableGrid, grid_to_latex
from .omml import M_NS, W_NS, omml_to_latex

NS = {
    "w": W_NS,
    "m": M_NS,
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}

_HEADING_PATTERNS = (
    re.compile(r"^heading\s*([1-9])$", re.I),
    re.compile(r"^제목\s*([1-9])$"),
    re.compile(r"^개요\s*([1-9])$"),
    re.compile(r"^\uc81c\ubaa9\s*([1-9])$"),
)
_TITLE_STYLES = {"title", "제목", "subtitle", "부제"}
_CAPTION_STYLES = {"caption", "표제", "그림설명", "캡션"}
_CODE_STYLES = {"code", "sourcecode", "htmlcode", "plaintext", "본문코드"}
#: table-of-contents / running header styles: structure, not content
_ARTIFACT_STYLE_RE = re.compile(r"^(?:toc\d*|목차\d*|차례|header|footer|머리글|바닥글|index\d*)$")


def _w(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


def _m_tag(tag: str) -> str:
    return f"{{{M_NS}}}{tag}"


@dataclass
class _StyleInfo:
    style_id: str
    name: str = ""
    outline_level: int | None = None
    based_on: str | None = None


@dataclass
class _Stats:
    images_skipped: int = 0
    ole_objects: int = 0
    inline_equations: int = 0
    display_equations: int = 0
    tables: int = 0


@dataclass
class _Ctx:
    styles: dict[str, _StyleInfo]
    footnotes: dict[str, str]
    stats: _Stats = field(default_factory=_Stats)
    warnings: list[str] = field(default_factory=list)
    used_footnotes: list[str] = field(default_factory=list)


def extract_docx(path: str | Path, config: Config | None = None) -> Document:
    path = Path(path)
    word_cfg = (config.word if config else WordConfig()) if config else WordConfig()
    with zipfile.ZipFile(path) as zf:
        document_xml = _read_xml(zf, "word/document.xml")
        if document_xml is None:
            raise ValueError(f"{path.name}: missing word/document.xml (not a .docx?)")
        ctx = _Ctx(
            styles=_parse_styles(_read_xml(zf, "word/styles.xml")),
            footnotes=_parse_footnotes(_read_xml(zf, "word/footnotes.xml")),
        )
        core_props = _parse_core_properties(_read_xml(zf, "docProps/core.xml"))

    body = document_xml.find(_w("body"))
    if body is None:
        raise ValueError(f"{path.name}: empty document body")

    doc = Document(
        doc_id=slugify(path.stem),
        source_path=str(path),
        source_type="docx",
        title=core_props.get("title") or None,
    )
    for block in _walk_body(body, ctx):
        doc.add(block)

    if word_cfg.include_footnotes:
        for note_id in ctx.used_footnotes:
            text = ctx.footnotes.get(note_id, "").strip()
            if text:
                doc.add(Block(kind=BlockKind.FOOTNOTE, text=text, meta={"footnote_id": note_id}))

    if not doc.title:
        first_title = next((b for b in doc.blocks if b.kind is BlockKind.TITLE), None)
        doc.title = first_title.text if first_title else None

    doc.meta.update(
        {
            "extractor": "docx_ooxml",
            "core_properties": core_props,
            "images_skipped": ctx.stats.images_skipped,
            "ole_objects": ctx.stats.ole_objects,
            "inline_equations": ctx.stats.inline_equations,
            "display_equations": ctx.stats.display_equations,
            "tables": ctx.stats.tables,
        }
    )
    for warning in ctx.warnings:
        doc.warn(warning)
    if ctx.stats.ole_objects:
        doc.warn(
            f"{ctx.stats.ole_objects} embedded OLE object(s) (e.g. Equation 3.0) cannot be "
            "converted to LaTeX from OOXML; re-save the file with modern Word equations or "
            "route the page through the PDF/image pipeline to recover them"
        )
    return doc


def _read_xml(zf: zipfile.ZipFile, name: str):
    try:
        data = zf.read(name)
    except KeyError:
        return None
    return etree.fromstring(data)


def _parse_styles(root) -> dict[str, _StyleInfo]:
    styles: dict[str, _StyleInfo] = {}
    if root is None:
        return styles
    for style in root.findall(_w("style")):
        style_id = style.get(_w("styleId")) or ""
        info = _StyleInfo(style_id=style_id)
        name_el = style.find(_w("name"))
        if name_el is not None:
            info.name = name_el.get(_w("val")) or ""
        based_on = style.find(_w("basedOn"))
        if based_on is not None:
            info.based_on = based_on.get(_w("val"))
        ppr = style.find(_w("pPr"))
        if ppr is not None:
            outline = ppr.find(_w("outlineLvl"))
            if outline is not None:
                try:
                    info.outline_level = int(outline.get(_w("val")) or "")
                except ValueError:
                    info.outline_level = None
        styles[style_id] = info
    return styles


def _parse_footnotes(root) -> dict[str, str]:
    notes: dict[str, str] = {}
    if root is None:
        return notes
    for note in root.findall(_w("footnote")):
        note_id = note.get(_w("id")) or ""
        if note.get(_w("type")) in ("separator", "continuationSeparator", "continuationNotice"):
            continue
        text = " ".join(t.text or "" for t in note.iter(_w("t")))
        notes[note_id] = re.sub(r"\s+", " ", text).strip()
    return notes


def _parse_core_properties(root) -> dict[str, str]:
    if root is None:
        return {}
    props: dict[str, str] = {}
    for el in root:
        if not isinstance(el.tag, str):
            continue
        key = etree.QName(el).localname
        if el.text and el.text.strip():
            props[key] = el.text.strip()
    return props


def _walk_body(node, ctx: _Ctx) -> Iterator[Block]:
    for child in node:
        if not isinstance(child.tag, str):
            continue
        if child.tag == _w("p"):
            yield from _convert_paragraph(child, ctx)
        elif child.tag == _w("tbl"):
            block = _convert_table(child, ctx)
            if block is not None:
                yield block
        elif child.tag in (_w("sdt"), _w("sdtContent")):
            target = child.find(_w("sdtContent")) if child.tag == _w("sdt") else child
            if target is not None:
                yield from _walk_body(target, ctx)


def _style_of(node, ctx: _Ctx) -> _StyleInfo | None:
    ppr = node.find(_w("pPr"))
    if ppr is None:
        return None
    style_el = ppr.find(_w("pStyle"))
    if style_el is None:
        return None
    style_id = style_el.get(_w("val")) or ""
    return ctx.styles.get(style_id, _StyleInfo(style_id=style_id, name=style_id))


def _heading_level(style: _StyleInfo | None, ctx: _Ctx) -> int | None:
    if style is None:
        return None
    seen: set[str] = set()
    current: _StyleInfo | None = style
    while current is not None and current.style_id not in seen:
        seen.add(current.style_id)
        for candidate in (current.name, current.style_id):
            for pattern in _HEADING_PATTERNS:
                match = pattern.match((candidate or "").strip())
                if match:
                    return int(match.group(1))
        if current.outline_level is not None and current.outline_level < 9:
            return current.outline_level + 1
        current = ctx.styles.get(current.based_on or "") if current.based_on else None
    return None


def _normalized_style_key(style: _StyleInfo | None) -> str:
    if style is None:
        return ""
    return re.sub(r"\s+", "", (style.name or style.style_id)).lower()


def _is_list_paragraph(node) -> int | None:
    ppr = node.find(_w("pPr"))
    if ppr is None:
        return None
    numpr = ppr.find(_w("numPr"))
    if numpr is None:
        return None
    ilvl = numpr.find(_w("ilvl"))
    try:
        return int(ilvl.get(_w("val")) or 0) if ilvl is not None else 0
    except ValueError:
        return 0


def _convert_paragraph(node, ctx: _Ctx) -> Iterator[Block]:
    style = _style_of(node, ctx)
    style_key = _normalized_style_key(style)

    display_math = [omml_to_latex(el) for el in node.findall(_m_tag("oMathPara"))]
    text = _paragraph_text(node, ctx)
    stripped = text.strip()

    if display_math and not stripped:
        for latex in display_math:
            if latex:
                ctx.stats.display_equations += 1
                yield Block(kind=BlockKind.EQUATION, text=latex, latex=latex, meta={"source": "omml"})
        return

    if not stripped:
        return

    # A paragraph whose entire content is one inline formula is a display equation.
    only_math = re.fullmatch(r"\$(?P<latex>.+)\$", stripped, re.S)
    if only_math and len(node.findall(_m_tag("oMath"))) == 1:
        latex = only_math.group("latex").strip()
        ctx.stats.display_equations += 1
        ctx.stats.inline_equations = max(0, ctx.stats.inline_equations - 1)
        yield Block(kind=BlockKind.EQUATION, text=latex, latex=latex, meta={"source": "omml"})
        return

    level = _heading_level(style, ctx)
    list_level = _is_list_paragraph(node)

    if _ARTIFACT_STYLE_RE.match(style_key):
        yield Block(kind=BlockKind.PAGE_ARTIFACT, text=stripped, meta={"artifact": "style", "style": style_key})
    elif style_key in _TITLE_STYLES:
        yield Block(kind=BlockKind.TITLE, text=stripped, level=1, meta={"style": style_key})
    elif level is not None:
        yield Block(kind=BlockKind.HEADING, text=stripped, level=level, meta={"style": style_key})
    elif style_key in _CAPTION_STYLES:
        yield Block(kind=BlockKind.CAPTION, text=stripped, meta={"style": style_key})
    elif style_key in _CODE_STYLES:
        yield Block(kind=BlockKind.CODE, text=text.rstrip(), meta={"style": style_key})
    elif list_level is not None:
        yield Block(
            kind=BlockKind.LIST_ITEM, text=stripped, level=list_level + 1, meta={"style": style_key}
        )
    else:
        yield Block(kind=BlockKind.PARAGRAPH, text=stripped, meta={"style": style_key} if style_key else {})

    for latex in display_math:
        if latex:
            ctx.stats.display_equations += 1
            yield Block(kind=BlockKind.EQUATION, text=latex, latex=latex, meta={"source": "omml"})


def _paragraph_text(node, ctx: _Ctx) -> str:
    pieces: list[str] = []
    for child in node:
        if not isinstance(child.tag, str):
            continue
        if child.tag in (_w("pPr"), _m_tag("oMathPara")):
            continue
        pieces.append(_inline_text(child, ctx))
    text = "".join(pieces)
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text)


def _inline_text(node, ctx: _Ctx) -> str:
    tag = node.tag
    if tag == _w("t"):
        return node.text or ""
    if tag == _w("tab"):
        return "\t"
    if tag in (_w("br"), _w("cr")):
        return "\n"
    if tag == _w("noBreakHyphen"):
        return "-"
    if tag == _w("softHyphen"):
        return ""
    if tag == _w("sym"):
        return _symbol_char(node)
    if tag == _m_tag("oMath"):
        latex = omml_to_latex(node)
        if not latex:
            return ""
        ctx.stats.inline_equations += 1
        return f"${latex}$"
    if tag in (_w("drawing"), _w("pict")):
        ctx.stats.images_skipped += 1
        return ""
    if tag == _w("object"):
        ctx.stats.ole_objects += 1
        return ""
    if tag == _w("footnoteReference"):
        note_id = node.get(_w("id")) or ""
        if note_id and note_id not in ctx.used_footnotes:
            ctx.used_footnotes.append(note_id)
        return ""
    if tag in (_w("delText"), _w("del"), _w("rPr"), _w("commentReference"), _w("proofErr")):
        return ""
    if tag in (
        _w("r"),
        _w("hyperlink"),
        _w("ins"),
        _w("smartTag"),
        _w("fldSimple"),
        _w("sdt"),
        _w("sdtContent"),
        _w("ruby"),
        _w("rubyBase"),
        _w("bdo"),
        _w("dir"),
    ):
        return "".join(_inline_text(child, ctx) for child in node if isinstance(child.tag, str))
    return ""


def _symbol_char(node) -> str:
    char = node.get(_w("char"))
    if not char:
        return ""
    try:
        code = int(char, 16)
    except ValueError:
        return ""
    if 0xF000 <= code <= 0xF0FF:  # symbol fonts (Wingdings & co) carry no text meaning
        return ""
    return chr(code)


def _convert_table(node, ctx: _Ctx) -> Block | None:
    cells: list[TableCell] = []
    vmerge_origin: dict[int, TableCell] = {}
    rows = node.findall(_w("tr"))
    n_cols = 0
    for row_idx, row in enumerate(rows):
        col = 0
        header_row = _is_header_row(row) or row_idx == 0
        for tc in row.findall(_w("tc")):
            tc_pr = tc.find(_w("tcPr"))
            span = 1
            vmerge: str | None = None
            if tc_pr is not None:
                grid_span = tc_pr.find(_w("gridSpan"))
                if grid_span is not None:
                    try:
                        span = max(1, int(grid_span.get(_w("val")) or 1))
                    except ValueError:
                        span = 1
                vmerge_el = tc_pr.find(_w("vMerge"))
                if vmerge_el is not None:
                    vmerge = vmerge_el.get(_w("val")) or "continue"
            if vmerge == "continue":
                origin = vmerge_origin.get(col)
                if origin is not None:
                    origin.row_span += 1
                col += span
                continue
            cell = TableCell(
                text=_cell_text(tc, ctx),
                row=row_idx,
                col=col,
                row_span=1,
                col_span=span,
                is_header=header_row,
            )
            cells.append(cell)
            if vmerge == "restart":
                vmerge_origin[col] = cell
            else:
                vmerge_origin.pop(col, None)
            col += span
        n_cols = max(n_cols, col)

    grid = TableGrid(cells=cells, num_rows=len(rows), num_cols=n_cols).normalize()
    if grid.is_degenerate():
        return None
    latex = grid_to_latex(grid)
    if not latex:
        return None
    ctx.stats.tables += 1
    return Block(
        kind=BlockKind.TABLE,
        text=latex,
        latex=latex,
        meta={
            "source": "ooxml",
            "num_rows": grid.num_rows,
            "num_cols": grid.num_cols,
            "cells": [
                {
                    "text": c.text,
                    "row": c.row,
                    "col": c.col,
                    "row_span": c.row_span,
                    "col_span": c.col_span,
                    "is_header": c.is_header,
                }
                for c in grid.cells
            ],
        },
    )


def _is_header_row(row) -> bool:
    tr_pr = row.find(_w("trPr"))
    if tr_pr is None:
        return False
    return tr_pr.find(_w("tblHeader")) is not None


def _cell_text(tc, ctx: _Ctx) -> str:
    parts: list[str] = []
    for child in tc:
        if not isinstance(child.tag, str):
            continue
        if child.tag == _w("p"):
            math = [omml_to_latex(el) for el in child.findall(_m_tag("oMathPara"))]
            text = _paragraph_text(child, ctx).strip()
            for latex in math:
                if latex:
                    ctx.stats.display_equations += 1
                    text = f"{text} ${latex}$".strip()
            if text:
                parts.append(text)
        elif child.tag == _w("tbl"):
            nested = _convert_table(child, ctx)
            if nested is not None:
                ctx.warnings.append("nested table flattened into the parent cell")
                parts.append(nested.latex or "")
    return re.sub(r"\s+", " ", " ".join(parts)).strip()
