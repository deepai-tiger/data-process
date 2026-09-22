"""Dataset stage: chunking, instruction synthesis, packaging."""

from .build import BuildStats, build_dataset, render_dataset_card
from .chunk import Chunk, TokenCounter, chunk_document
from .instructions import SftSample, build_sft_samples
from .templates import BUILTIN_TEMPLATES, get_renderer

__all__ = [
    "BuildStats",
    "build_dataset",
    "render_dataset_card",
    "Chunk",
    "TokenCounter",
    "chunk_document",
    "SftSample",
    "build_sft_samples",
    "BUILTIN_TEMPLATES",
    "get_renderer",
]
