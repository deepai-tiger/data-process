"""Logging setup shared by the CLI and the library."""

from __future__ import annotations

import logging
import os
import warnings

_NOISY_LOGGERS = (
    "docling",
    "docling_core",
    "docling_ibm_models",
    "transformers",
    "urllib3",
    "PIL",
    "matplotlib",
    "easyocr",
    "timm",
)


def setup_logging(level: str = "INFO", quiet_dependencies: bool = True) -> None:
    # force=True: importing docling/transformers already installs a root
    # handler, which would make basicConfig a silent no-op and leave
    # --log-level with no effect at all.
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        force=True,
    )
    if not quiet_dependencies:
        return
    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.ERROR)
    # Tesseract's orientation detection gives up on near-blank pages ("Too few
    # characters"); docling recovers by assuming no rotation and OCRs the page
    # anyway, so reporting it as an error only makes a healthy run look broken.
    logging.getLogger("docling.models.stages.ocr.tesseract_ocr_cli_model").setLevel(logging.CRITICAL)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    # keep third-party model code from oversubscribing the CPU
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    os.environ.setdefault("NO_ALBUMENTATIONS_UPDATE", "1")
