"""Exact and near-duplicate removal.

Two levels are needed for scanned books: whole documents/chunks (a file
processed twice, a reprinted chapter) and single paragraphs (running blurbs,
copyright notices, repeated captions). Near-duplicates use MinHash over
character shingles, which suits Korean better than word shingles because
Hangul word boundaries are unreliable in OCR output.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence

import xxhash

from ..config import DedupConfig
from ..schema import Block, BlockKind, Document

_WS_RE = re.compile(r"\s+")


def canonical(text: str) -> str:
    """Whitespace/punctuation-insensitive form used for hashing only."""
    return _WS_RE.sub(" ", re.sub(r"[^\w\uac00-\ud7a3]+", " ", text)).strip().lower()


def text_hash(text: str) -> str:
    return xxhash.xxh3_64_hexdigest(canonical(text))


def shingles(text: str, size: int) -> set[str]:
    canon = canonical(text).replace(" ", "")
    if len(canon) <= size:
        return {canon} if canon else set()
    return {canon[i : i + size] for i in range(len(canon) - size + 1)}


@dataclass
class DedupReport:
    exact_duplicates: int = 0
    near_duplicates: int = 0
    paragraphs_removed: int = 0
    kept: int = 0
    duplicate_of: dict[str, str] = field(default_factory=dict)

    def as_dict(self) -> dict[str, object]:
        return {
            "kept": self.kept,
            "exact_duplicates": self.exact_duplicates,
            "near_duplicates": self.near_duplicates,
            "paragraphs_removed": self.paragraphs_removed,
        }


class Deduper:
    """Incremental deduplicator: feed texts in, ask whether to keep each."""

    def __init__(self, cfg: DedupConfig) -> None:
        self.cfg = cfg
        self._exact: dict[str, str] = {}
        self._lsh = None
        self._minhashes: dict[str, object] = {}
        self.report = DedupReport()
        if cfg.near:
            try:
                from datasketch import MinHashLSH

                self._lsh = MinHashLSH(threshold=cfg.threshold, num_perm=cfg.num_perm)
            except ImportError:  # pragma: no cover - optional dependency
                self._lsh = None

    def _minhash(self, text: str):
        from datasketch import MinHash

        minhash = MinHash(num_perm=self.cfg.num_perm)
        for shingle in shingles(text, self.cfg.shingle_size):
            minhash.update(shingle.encode("utf-8"))
        return minhash

    def check(self, key: str, text: str) -> str | None:
        """Return the key of an earlier duplicate, or ``None`` if ``text`` is new."""
        if self.cfg.exact:
            digest = text_hash(text)
            previous = self._exact.get(digest)
            if previous is not None:
                self.report.exact_duplicates += 1
                self.report.duplicate_of[key] = previous
                return previous
            self._exact[digest] = key

        if self._lsh is not None and len(canonical(text)) >= self.cfg.shingle_size:
            minhash = self._minhash(text)
            matches = self._lsh.query(minhash)
            if matches:
                previous = str(matches[0])
                self.report.near_duplicates += 1
                self.report.duplicate_of[key] = previous
                return previous
            self._lsh.insert(key, minhash)
            self._minhashes[key] = minhash

        self.report.kept += 1
        return None


def dedup_texts(items: Sequence[tuple[str, str]], cfg: DedupConfig) -> tuple[list[str], DedupReport]:
    """Filter ``(key, text)`` pairs, returning the keys that survive."""
    deduper = Deduper(cfg)
    kept = [key for key, text in items if deduper.check(key, text) is None]
    return kept, deduper.report


class ParagraphDeduper:
    """Drops paragraphs already seen in another document (corpus-wide)."""

    def __init__(self, cfg: DedupConfig) -> None:
        self.cfg = cfg
        self._seen: dict[str, str] = {}
        self.removed = 0

    def filter_document(self, doc: Document) -> int:
        if not self.cfg.paragraph_level:
            return 0
        kept: list[Block] = []
        removed = 0
        for block in doc.blocks:
            if block.kind not in (BlockKind.PARAGRAPH, BlockKind.LIST_ITEM):
                kept.append(block)
                continue
            text = block.text
            if len(canonical(text)) < self.cfg.min_paragraph_chars_for_dedup:
                kept.append(block)
                continue
            digest = text_hash(text)
            owner = self._seen.get(digest)
            if owner is not None and owner != doc.doc_id:
                removed += 1
                continue
            self._seen.setdefault(digest, doc.doc_id)
            kept.append(block)
        doc.blocks = kept
        self.removed += removed
        if removed:
            doc.meta.setdefault("dedup", {})["paragraphs_removed"] = removed
        return removed
