"""Format dispatch for extraction."""

from __future__ import annotations

import logging
from pathlib import Path

from ..config import Config
from ..schema import Document

logger = logging.getLogger(__name__)

PDF_SUFFIXES = {".pdf"}
DOCX_SUFFIXES = {".docx", ".docm"}
LEGACY_WORD_SUFFIXES = {".doc", ".rtf", ".odt", ".dot", ".wps"}
SUPPORTED_SUFFIXES = PDF_SUFFIXES | DOCX_SUFFIXES | LEGACY_WORD_SUFFIXES
#: recognized, but no extractor yet - reported instead of silently skipped
KNOWN_UNSUPPORTED = {".hwp", ".hwpx", ".pptx", ".ppt", ".xlsx", ".xls"}


class UnsupportedFormat(RuntimeError):
    pass


def iter_source_files(root: str | Path, recursive: bool = True) -> list[Path]:
    root = Path(root)
    if root.is_file():
        return [root]
    pattern = "**/*" if recursive else "*"
    files = [
        path
        for path in sorted(root.glob(pattern))
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES and not path.name.startswith("~$")
    ]
    skipped = [
        path
        for path in sorted(root.glob(pattern))
        if path.is_file() and path.suffix.lower() in KNOWN_UNSUPPORTED
    ]
    for path in skipped:
        logger.warning("no extractor for %s (%s)", path.name, path.suffix)
    return files


class Extractor:
    """Keeps heavy PDF models loaded across a whole batch of files."""

    def __init__(self, config: Config) -> None:
        self.cfg = config
        self._pdf = None

    def extract(self, path: str | Path) -> Document:
        path = Path(path)
        suffix = path.suffix.lower()
        if suffix in PDF_SUFFIXES:
            return self._pdf_extractor().extract(path)
        if suffix in DOCX_SUFFIXES:
            from .docx_ooxml import extract_docx

            return extract_docx(path, self.cfg)
        if suffix in LEGACY_WORD_SUFFIXES:
            from .doc_legacy import extract_legacy_doc

            return extract_legacy_doc(path, self.cfg)
        raise UnsupportedFormat(
            f"{path.name}: no extractor for '{suffix}'"
            + (" (HWP support is not implemented yet)" if suffix in {".hwp", ".hwpx"} else "")
        )

    def _pdf_extractor(self):
        if self._pdf is None:
            from .pdf_image import PdfLayoutExtractor

            self._pdf = PdfLayoutExtractor(self.cfg)
        return self._pdf
