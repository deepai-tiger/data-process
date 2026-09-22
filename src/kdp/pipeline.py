"""Stage orchestration: extract -> clean -> build.

Each stage persists its output, so stages can be run (and re-run) separately:
extraction is the expensive part and is cached per page, while cleaning and
dataset packaging are cheap enough to iterate on.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from .clean import clean_document
from .clean.dedup import ParagraphDeduper
from .clean.normalize import infer_structure, sanitize_title
from .config import Config
from .dataset.build import BuildStats, build_dataset
from .extract import Extractor, iter_source_files
from .schema import Document
from .dataset.writers import write_json, write_text

logger = logging.getLogger(__name__)


@dataclass
class ExtractSummary:
    documents: list[Path] = field(default_factory=list)
    failures: list[dict[str, str]] = field(default_factory=list)
    elapsed_s: float = 0.0
    per_document: list[dict[str, Any]] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "documents": [str(p) for p in self.documents],
            "failures": self.failures,
            "elapsed_s": round(self.elapsed_s, 2),
            "per_document": self.per_document,
        }


def run_extract(config: Config, inputs: Sequence[Path] | None = None, force: bool = False) -> ExtractSummary:
    started = time.time()
    files = list(inputs) if inputs else iter_source_files(config.paths.raw_dir)
    if not files:
        logger.warning("no supported source files under %s", config.paths.raw_dir)
    summary = ExtractSummary()
    extractor = Extractor(config)

    for path in files:
        target = config.paths.docjson_dir / f"{_doc_id(path)}.json"
        if target.exists() and not force:
            logger.info("skip %s (already extracted: %s)", path.name, target.name)
            summary.documents.append(target)
            continue
        logger.info("extracting %s", path)
        try:
            doc = extractor.extract(path)
        except Exception as exc:
            logger.exception("failed to extract %s", path)
            summary.failures.append({"path": str(path), "error": f"{type(exc).__name__}: {exc}"})
            continue
        doc.save(target)
        write_text(doc.to_markdown(), config.paths.markdown_dir / f"{doc.doc_id}.md")
        summary.documents.append(target)
        summary.per_document.append(
            {
                "doc_id": doc.doc_id,
                "path": str(path),
                "source_type": doc.source_type,
                "blocks": doc.counts(),
                "chars": doc.char_count(),
                "warnings": doc.warnings,
                "meta": {k: v for k, v in doc.meta.items() if k != "core_properties"},
            }
        )

    summary.elapsed_s = time.time() - started
    write_json(summary.as_dict(), config.paths.report_dir / "extract.json")
    return summary


def run_clean(config: Config) -> list[Document]:
    docjson_files = sorted(config.paths.docjson_dir.glob("*.json"))
    if not docjson_files:
        raise FileNotFoundError(
            f"no extracted documents in {config.paths.docjson_dir}; run `kdp extract` first"
        )
    paragraph_deduper = ParagraphDeduper(config.dedup)
    cleaned: list[Document] = []
    reports: dict[str, Any] = {}

    for path in docjson_files:
        doc = Document.load(path)
        doc = infer_structure(doc, config.normalize)
        result = clean_document(doc, config)
        doc = result.document
        sanitize_title(doc)
        removed = paragraph_deduper.filter_document(doc)
        reports[doc.doc_id] = {
            **result.reports,
            "cross_document_paragraphs_removed": removed,
            "dropped": result.dropped,
            "drop_reason": result.drop_reason,
        }
        if result.dropped:
            logger.warning("dropping document %s (%s)", doc.doc_id, result.drop_reason)
            continue
        doc.save(config.paths.clean_dir / f"{doc.doc_id}.json")
        write_text(doc.to_markdown(), config.paths.markdown_dir / f"{doc.doc_id}.clean.md")
        cleaned.append(doc)

    write_json(
        {"documents": reports, "paragraphs_removed_total": paragraph_deduper.removed},
        config.paths.report_dir / "clean.json",
    )
    logger.info("cleaned %d/%d documents", len(cleaned), len(docjson_files))
    return cleaned


def run_build(config: Config, documents: Sequence[Document] | None = None) -> BuildStats:
    if documents is None:
        files = sorted(config.paths.clean_dir.glob("*.json"))
        if not files:
            raise FileNotFoundError(f"no cleaned documents in {config.paths.clean_dir}; run `kdp clean` first")
        documents = [Document.load(path) for path in files]
    return build_dataset(list(documents), config)


@dataclass
class PipelineResult:
    extract: ExtractSummary
    documents: list[Document]
    build: BuildStats


def run_pipeline(config: Config, inputs: Sequence[Path] | None = None, force: bool = False) -> PipelineResult:
    extract = run_extract(config, inputs=inputs, force=force)
    documents = run_clean(config)
    stats = run_build(config, documents)
    return PipelineResult(extract=extract, documents=documents, build=stats)


def _doc_id(path: Path) -> str:
    from .schema import slugify

    return slugify(path.stem)
