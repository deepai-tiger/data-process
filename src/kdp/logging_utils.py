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
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    if not quiet_dependencies:
        return
    for name in _NOISY_LOGGERS:
        logging.getLogger(name).setLevel(logging.ERROR)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    # keep third-party model code from oversubscribing the CPU
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    os.environ.setdefault("NO_ALBUMENTATIONS_UPDATE", "1")
