"""Token-aware chunking of a cleaned document.

Chunks are the unit of pretraining data. Three properties are worth the extra
code: chunks break on section boundaries (so a chunk is about one topic), a
table or equation is never split in half (half a ``tabular`` is noise), and the
heading path is carried along so the model sees the context a human would.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from ..config import ChunkConfig
from ..schema import LATEX_KINDS, Block, BlockKind, Document, render_block

logger = logging.getLogger(__name__)

#: Korean sentences end with a predicate ending + punctuation
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?。])\s+|(?<=[다요까죠음임함])\.\s+")
#: rough tokens-per-character for mixed Korean/Latin text, used without a tokenizer
_CHARS_PER_TOKEN = 1.6


class TokenCounter:
    """Counts tokens with a real tokenizer when available, else by characters."""

    def __init__(self, tokenizer_name: str | None = None) -> None:
        self.name = tokenizer_name or "char-heuristic"
        self._tokenizer = None
        if tokenizer_name:
            try:
                from transformers import AutoTokenizer

                self._tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, trust_remote_code=False)
            except Exception as exc:  # network/offline/missing dependency
                logger.warning(
                    "tokenizer '%s' unavailable (%s); falling back to a character heuristic",
                    tokenizer_name,
                    type(exc).__name__,
                )
                self.name = f"char-heuristic (wanted {tokenizer_name})"

    @property
    def exact(self) -> bool:
        return self._tokenizer is not None

    def count(self, text: str) -> int:
        if not text:
            return 0
        if self._tokenizer is not None:
            return len(self._tokenizer.encode(text, add_special_tokens=False))
        return max(1, int(len(text) / _CHARS_PER_TOKEN))


@dataclass
class Chunk:
    doc_id: str
    index: int
    text: str
    n_tokens: int
    pages: list[int] = field(default_factory=list)
    heading_path: list[str] = field(default_factory=list)
    block_kinds: dict[str, int] = field(default_factory=dict)

    @property
    def chunk_id(self) -> str:
        return f"{self.doc_id}#{self.index:05d}"

    def has_latex(self) -> bool:
        return bool(self.block_kinds.get("table") or self.block_kinds.get("equation"))


@dataclass
class _Pending:
    parts: list[str] = field(default_factory=list)
    tokens: int = 0
    pages: set[int] = field(default_factory=set)
    kinds: dict[str, int] = field(default_factory=dict)
    heading_path: list[str] = field(default_factory=list)

    def add(self, text: str, tokens: int, block: Block | None) -> None:
        self.parts.append(text)
        self.tokens += tokens
        if block is not None:
            if block.page is not None:
                self.pages.add(block.page)
            self.kinds[block.kind.value] = self.kinds.get(block.kind.value, 0) + 1

    @property
    def empty(self) -> bool:
        return not self.parts


def chunk_document(doc: Document, cfg: ChunkConfig, counter: TokenCounter) -> list[Chunk]:
    chunks: list[Chunk] = []
    heading_stack: list[tuple[int, str]] = []
    pending = _Pending(heading_path=[])

    def flush() -> None:
        nonlocal pending
        if pending.empty:
            return
        body = "\n\n".join(part for part in pending.parts if part.strip())
        if not body.strip():
            pending = _Pending(heading_path=[h for _, h in heading_stack])
            return
        prefix = ""
        if cfg.prepend_heading_path and pending.heading_path:
            prefix = " > ".join(pending.heading_path) + "\n\n"
        text = f"{prefix}{body}".strip()
        chunks.append(
            Chunk(
                doc_id=doc.doc_id,
                index=len(chunks),
                text=text,
                n_tokens=counter.count(text),
                pages=sorted(pending.pages),
                heading_path=list(pending.heading_path),
                block_kinds=dict(pending.kinds),
            )
        )
        carry = _overlap_text(body, cfg.overlap_tokens, counter) if cfg.overlap_tokens else ""
        pending = _Pending(heading_path=[h for _, h in heading_stack])
        if carry:
            pending.add(carry, counter.count(carry), None)

    for block in doc.blocks:
        if block.kind is BlockKind.PAGE_ARTIFACT:
            continue
        rendered = render_block(block)
        if not rendered.strip():
            continue

        if block.kind in (BlockKind.TITLE, BlockKind.HEADING):
            level = block.level or (1 if block.kind is BlockKind.TITLE else 2)
            if pending.tokens >= cfg.min_tokens:
                flush()
            heading_stack = [(lvl, text) for lvl, text in heading_stack if lvl < level]
            heading_stack.append((level, block.text.strip()))
            if pending.empty:
                pending.heading_path = [text for _, text in heading_stack]
            pending.add(rendered, counter.count(rendered), block)
            continue

        tokens = counter.count(rendered)
        if tokens > cfg.max_tokens:
            flush()
            for piece in _split_oversized(block, rendered, cfg, counter):
                pending.add(piece, counter.count(piece), block)
                flush()
            continue

        if pending.tokens + tokens > cfg.max_tokens and pending.tokens >= cfg.min_tokens:
            flush()
        pending.add(rendered, tokens, block)

    flush()
    return chunks


def _split_oversized(block: Block, rendered: str, cfg: ChunkConfig, counter: TokenCounter) -> list[str]:
    """Split a single over-long block, keeping LaTeX payloads atomic."""
    if block.kind in LATEX_KINDS and cfg.keep_latex_atomic:
        return [rendered]
    sentences = [s for s in _SENTENCE_SPLIT_RE.split(rendered) if s.strip()]
    if len(sentences) <= 1:
        return _hard_wrap(rendered, cfg.max_tokens, counter)

    pieces: list[str] = []
    current: list[str] = []
    current_tokens = 0
    for sentence in sentences:
        tokens = counter.count(sentence)
        if current and current_tokens + tokens > cfg.max_tokens:
            pieces.append(" ".join(current))
            current, current_tokens = [], 0
        current.append(sentence)
        current_tokens += tokens
    if current:
        pieces.append(" ".join(current))
    return pieces


def _hard_wrap(text: str, max_tokens: int, counter: TokenCounter) -> list[str]:
    approx_chars = max(200, int(max_tokens * _CHARS_PER_TOKEN))
    return [text[i : i + approx_chars] for i in range(0, len(text), approx_chars)]


def _overlap_text(body: str, overlap_tokens: int, counter: TokenCounter) -> str:
    sentences = [s for s in _SENTENCE_SPLIT_RE.split(body) if s.strip()]
    carry: list[str] = []
    total = 0
    for sentence in reversed(sentences):
        tokens = counter.count(sentence)
        if total + tokens > overlap_tokens:
            break
        carry.insert(0, sentence)
        total += tokens
    return " ".join(carry)
