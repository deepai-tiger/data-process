"""kdp - Korean document data-processing pipeline.

Turns raw PDF/DOC/DOCX documents into a clean, trainable Korean dataset:

    raw files -> extract (layout analysis + OCR + LaTeX) -> clean -> dataset

See ``README.md`` for the CLI, or use the pieces directly:

    from kdp.config import load_config
    from kdp.pipeline import run_pipeline
"""

from __future__ import annotations

__version__ = "0.1.0"

from .schema import Block, BlockKind, Document

__all__ = ["Block", "BlockKind", "Document", "__version__"]
