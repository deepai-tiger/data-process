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

#: packages that log on the root logger instead of one of their own
_NOISY_ROOT_CALLERS = ("pix2tex",)


class ThirdPartyRootNoiseFilter(logging.Filter):
    """Drop stray records third-party code writes straight to the root logger.

    pix2tex calls ``logging.info(ratio, size, size)`` per recognised crop. The
    trailing values are not format arguments, so formatting the record raises
    and the handler prints a traceback in its place - once per equation. The
    root logger carries our own output too, so these cannot be silenced by
    level; they are matched by the file that emitted them instead.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        pathname = record.pathname or ""
        return not any(pkg in pathname for pkg in _NOISY_ROOT_CALLERS)


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
    for handler in logging.getLogger().handlers:
        handler.addFilter(ThirdPartyRootNoiseFilter())
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
