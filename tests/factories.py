"""Builders for the small documents the tests run against."""

from __future__ import annotations

from kdp.schema import Block, BlockKind, Document


def para(text: str, page: int | None = None, **meta) -> Block:
    return Block(kind=BlockKind.PARAGRAPH, text=text, page=page, meta=meta)


def heading(text: str, level: int = 2, page: int | None = None) -> Block:
    return Block(kind=BlockKind.HEADING, text=text, level=level, page=page)


def table(latex: str, page: int | None = None, **meta) -> Block:
    return Block(kind=BlockKind.TABLE, latex=latex, text=latex, page=page, meta=meta)


def equation(latex: str, page: int | None = None, **meta) -> Block:
    return Block(kind=BlockKind.EQUATION, latex=latex, text=latex, page=page, meta=meta)


def document(*blocks: Block, doc_id: str = "doc", source_type: str = "pdf") -> Document:
    return Document(
        doc_id=doc_id,
        source_path=f"raw/{doc_id}.pdf",
        source_type=source_type,
        blocks=list(blocks),
    )
