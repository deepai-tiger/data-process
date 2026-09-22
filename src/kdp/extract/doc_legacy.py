"""Legacy binary Word (.doc) and .rtf/.odt support via LibreOffice.

The binary .doc format is not worth parsing by hand, so we convert to OOXML with
headless LibreOffice and reuse the .docx extractor. Each conversion runs in its
own LibreOffice user profile, which is what makes parallel conversions safe.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from pathlib import Path

from ..config import Config, WordConfig
from ..schema import Document, slugify
from .docx_ooxml import extract_docx

logger = logging.getLogger(__name__)

CONVERTIBLE_SUFFIXES = {".doc", ".rtf", ".odt", ".wps", ".dot"}


class ConversionError(RuntimeError):
    pass


def convert_to_docx(path: str | Path, out_dir: str | Path, word_cfg: WordConfig | None = None) -> Path:
    """Convert a legacy word-processor file to .docx and return the new path."""
    word_cfg = word_cfg or WordConfig()
    path = Path(path).resolve()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{path.stem}.docx"
    if target.exists() and target.stat().st_mtime >= path.stat().st_mtime:
        return target

    soffice = shutil.which(word_cfg.soffice_bin) or shutil.which("libreoffice")
    if soffice is None:
        raise ConversionError(
            f"'{word_cfg.soffice_bin}' not found - install LibreOffice "
            "(scripts/install_system_deps.sh) to process legacy .doc files"
        )

    with tempfile.TemporaryDirectory(prefix="kdp-soffice-") as profile_dir:
        cmd = [
            soffice,
            f"-env:UserInstallation=file://{profile_dir}",
            "--headless",
            "--norestore",
            "--convert-to",
            "docx:MS Word 2007 XML",
            "--outdir",
            str(out_dir),
            str(path),
        ]
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=word_cfg.convert_timeout_s, check=False
            )
        except subprocess.TimeoutExpired as exc:
            raise ConversionError(f"LibreOffice timed out converting {path.name}") from exc

    if not target.exists():
        raise ConversionError(
            f"LibreOffice failed to convert {path.name}: "
            f"{(proc.stderr or proc.stdout or '').strip()[:400]}"
        )
    logger.debug("converted %s -> %s", path.name, target.name)
    return target


def extract_legacy_doc(path: str | Path, config: Config | None = None, work_dir: str | Path | None = None) -> Document:
    path = Path(path)
    cfg = config or Config()
    work_dir = Path(work_dir) if work_dir else cfg.paths.work_dir / "converted"
    converted = convert_to_docx(path, work_dir, cfg.word)
    doc = extract_docx(converted, cfg)
    doc.doc_id = slugify(path.stem)
    doc.source_path = str(path)
    doc.source_type = path.suffix.lower().lstrip(".") or "doc"
    doc.meta["extractor"] = "libreoffice+docx_ooxml"
    doc.meta["converted_from"] = str(path)
    doc.meta["converted_docx"] = str(converted)
    if not cfg.word.keep_converted:
        converted.unlink(missing_ok=True)
    return doc
