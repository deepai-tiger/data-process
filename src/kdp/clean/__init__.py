"""Cleaning stage: normalize -> re-space -> quality filter -> PII masking."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

from ..config import Config
from ..schema import Document
from .dedup import Deduper, DedupReport, ParagraphDeduper, dedup_texts, text_hash
from .normalize import (
    NormalizeReport,
    infer_structure,
    normalize_document,
    normalize_text,
    sanitize_title,
)
from .pii import PiiReport, mask_document, mask_text
from .quality import QualityReport, filter_document, script_profile, text_quality_reason
from .spacing import SpacingReport, respace_document

logger = logging.getLogger(__name__)

__all__ = [
    "CleanResult",
    "clean_document",
    "Deduper",
    "DedupReport",
    "ParagraphDeduper",
    "dedup_texts",
    "text_hash",
    "infer_structure",
    "mask_text",
    "normalize_text",
    "sanitize_title",
    "script_profile",
    "text_quality_reason",
]


@dataclass
class CleanResult:
    document: Document
    dropped: bool
    drop_reason: str | None = None
    reports: dict[str, Any] = field(default_factory=dict)


def clean_document(doc: Document, config: Config) -> CleanResult:
    """Run the per-document cleaning stages in order.

    Quality filtering happens *before* spacing repair on purpose: OCR noise
    ("아 아 애 아 애") is easiest to recognize while the syllables are still
    separated, and re-spacing would disguise it as ordinary words.
    """
    doc, normalized = normalize_document(doc, config.normalize)
    doc, quality = filter_document(doc, config.quality)
    doc, spacing = respace_document(
        doc, engine=config.normalize.spacing_engine, only_ocr=config.normalize.spacing_ocr_only
    )
    doc, pii = mask_document(doc, config.pii)

    reports = {
        "spacing": spacing.as_dict(),
        "normalize": normalized.as_dict(),
        "quality": quality.as_dict(),
        "pii": pii.as_dict(),
    }
    if quality.doc_reason:
        logger.warning("%s dropped by quality filter: %s", doc.doc_id, quality.doc_reason)
    return CleanResult(
        document=doc,
        dropped=quality.doc_reason is not None,
        drop_reason=quality.doc_reason,
        reports=reports,
    )
