"""JSONL / Parquet output with optional sharding."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

logger = logging.getLogger(__name__)


@dataclass
class WriteResult:
    path: Path
    records: int
    bytes_written: int
    shards: list[Path]

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": str(self.path),
            "records": self.records,
            "bytes": self.bytes_written,
            "shards": [str(p) for p in self.shards],
        }


def write_jsonl(records: Sequence[dict[str, Any]], path: str | Path, shard_size: int = 0) -> WriteResult:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not shard_size or len(records) <= shard_size:
        written = _dump(records, path)
        return WriteResult(path, len(records), written, [path])

    shards: list[Path] = []
    total = 0
    n_shards = (len(records) + shard_size - 1) // shard_size
    for index in range(n_shards):
        shard = path.with_name(f"{path.stem}-{index:05d}-of-{n_shards:05d}{path.suffix}")
        total += _dump(records[index * shard_size : (index + 1) * shard_size], shard)
        shards.append(shard)
    return WriteResult(path, len(records), total, shards)


def _dump(records: Iterable[dict[str, Any]], path: Path) -> int:
    written = 0
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            line = json.dumps(record, ensure_ascii=False)
            handle.write(line + "\n")
            written += len(line) + 1
    return written


def write_parquet(records: Sequence[dict[str, Any]], path: str | Path) -> Path | None:
    """Parquet keeps HF ``datasets``/Spark loading fast for large corpora."""
    if not records:
        return None
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError:  # pragma: no cover - optional dependency
        logger.warning("pyarrow not installed; skipping parquet output")
        return None

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    flattened = [{**record, "meta": json.dumps(record.get("meta", {}), ensure_ascii=False)} for record in records]
    if "messages" in flattened[0]:
        for record in flattened:
            record["messages"] = json.dumps(record["messages"], ensure_ascii=False)
    pq.write_table(pa.Table.from_pylist(flattened), path, compression="zstd")
    return path


def write_json(payload: Any, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_text(text: str, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path
