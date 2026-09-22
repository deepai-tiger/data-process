"""Intermediate document representation shared by every extractor.

Extraction and dataset building are decoupled through this schema: an extractor
only has to emit a ``Document`` of ``Block`` objects in reading order, and every
downstream stage (cleaning, chunking, dataset packaging) works on that.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterator, Sequence

SCHEMA_VERSION = "1.0"


class BlockKind(str, Enum):
    TITLE = "title"
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST_ITEM = "list_item"
    TABLE = "table"
    EQUATION = "equation"
    CAPTION = "caption"
    CODE = "code"
    FOOTNOTE = "footnote"
    #: repeated running headers/footers, page numbers - kept for traceability,
    #: never rendered into training text
    PAGE_ARTIFACT = "page_artifact"


#: blocks whose payload is LaTeX rather than prose
LATEX_KINDS = frozenset({BlockKind.TABLE, BlockKind.EQUATION})

TEXT_KINDS = frozenset(
    {
        BlockKind.TITLE,
        BlockKind.HEADING,
        BlockKind.PARAGRAPH,
        BlockKind.LIST_ITEM,
        BlockKind.CAPTION,
        BlockKind.CODE,
        BlockKind.FOOTNOTE,
    }
)


@dataclass
class Block:
    kind: BlockKind
    text: str = ""
    #: LaTeX payload for tables/equations (``text`` mirrors it for convenience)
    latex: str | None = None
    #: heading depth, 1-based
    level: int | None = None
    #: 1-based source page, ``None`` for formats without pagination
    page: int | None = None
    #: ``(left, top, right, bottom)`` in the coordinate space of the page image
    bbox: tuple[float, float, float, float] | None = None
    #: OCR / model confidence when the producer reports one
    confidence: float | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def payload(self) -> str:
        return self.latex if self.kind in LATEX_KINDS and self.latex else self.text

    @property
    def char_count(self) -> int:
        return len(self.payload)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"kind": self.kind.value, "text": self.text}
        if self.latex is not None:
            out["latex"] = self.latex
        if self.level is not None:
            out["level"] = self.level
        if self.page is not None:
            out["page"] = self.page
        if self.bbox is not None:
            out["bbox"] = list(self.bbox)
        if self.confidence is not None:
            out["confidence"] = self.confidence
        if self.meta:
            out["meta"] = self.meta
        return out

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Block":
        bbox = raw.get("bbox")
        return cls(
            kind=BlockKind(raw["kind"]),
            text=raw.get("text", ""),
            latex=raw.get("latex"),
            level=raw.get("level"),
            page=raw.get("page"),
            bbox=tuple(bbox) if bbox else None,
            confidence=raw.get("confidence"),
            meta=raw.get("meta", {}) or {},
        )


@dataclass
class Document:
    doc_id: str
    source_path: str
    source_type: str
    blocks: list[Block] = field(default_factory=list)
    title: str | None = None
    n_pages: int | None = None
    warnings: list[str] = field(default_factory=list)
    #: extraction provenance: engines, dpi, model versions, timings
    meta: dict[str, Any] = field(default_factory=dict)
    schema_version: str = SCHEMA_VERSION

    def add(self, block: Block) -> None:
        self.blocks.append(block)

    def warn(self, message: str) -> None:
        if message not in self.warnings:
            self.warnings.append(message)

    def counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for block in self.blocks:
            counts[block.kind.value] = counts.get(block.kind.value, 0) + 1
        return counts

    def char_count(self) -> int:
        return sum(b.char_count for b in self.blocks if b.kind is not BlockKind.PAGE_ARTIFACT)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "doc_id": self.doc_id,
            "source_path": self.source_path,
            "source_type": self.source_type,
            "title": self.title,
            "n_pages": self.n_pages,
            "warnings": self.warnings,
            "meta": self.meta,
            "blocks": [b.to_dict() for b in self.blocks],
        }

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Document":
        return cls(
            doc_id=raw["doc_id"],
            source_path=raw["source_path"],
            source_type=raw["source_type"],
            blocks=[Block.from_dict(b) for b in raw.get("blocks", [])],
            title=raw.get("title"),
            n_pages=raw.get("n_pages"),
            warnings=list(raw.get("warnings", [])),
            meta=raw.get("meta", {}) or {},
            schema_version=raw.get("schema_version", SCHEMA_VERSION),
        )

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: str | Path) -> "Document":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def to_markdown(self, include_artifacts: bool = False) -> str:
        return render_markdown(self.blocks, include_artifacts=include_artifacts)

    def iter_pages(self) -> Iterator[tuple[int | None, list[Block]]]:
        """Yield ``(page, blocks)`` groups in reading order."""
        bucket: list[Block] = []
        current: int | None = None
        for block in self.blocks:
            if not bucket:
                current = block.page
            elif block.page != current:
                yield current, bucket
                current, bucket = block.page, []
            bucket.append(block)
        if bucket:
            yield current, bucket


def render_block(block: Block) -> str:
    """Render one block as training-ready Markdown + LaTeX."""
    if block.kind is BlockKind.EQUATION:
        latex = (block.latex or block.text).strip()
        if not latex:
            return ""
        if block.meta.get("inline"):
            return f"${latex}$"
        return f"$$\n{latex}\n$$"
    if block.kind is BlockKind.TABLE:
        return (block.latex or "").strip()
    if block.kind in (BlockKind.TITLE, BlockKind.HEADING):
        level = block.level or (1 if block.kind is BlockKind.TITLE else 2)
        return f"{'#' * max(1, min(level, 6))} {block.text.strip()}"
    if block.kind is BlockKind.LIST_ITEM:
        return f"- {block.text.strip()}"
    if block.kind is BlockKind.CODE:
        lang = block.meta.get("language", "")
        return f"```{lang}\n{block.text.rstrip()}\n```"
    if block.kind is BlockKind.FOOTNOTE:
        return f"[각주] {block.text.strip()}"
    return block.text.strip()


def render_markdown(blocks: Sequence[Block], include_artifacts: bool = False) -> str:
    parts: list[str] = []
    for block in blocks:
        if block.kind is BlockKind.PAGE_ARTIFACT and not include_artifacts:
            continue
        rendered = render_block(block)
        if rendered:
            parts.append(rendered)
    text = "\n\n".join(parts)
    return re.sub(r"\n{4,}", "\n\n\n", text).strip() + "\n" if text else ""


def slugify(name: str) -> str:
    slug = re.sub(r"[^0-9A-Za-z\uac00-\ud7a3._-]+", "-", name).strip("-.")
    return slug.lower() or "doc"
