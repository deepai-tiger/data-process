#!/usr/bin/env python3
"""Normalize PaddleOCR trial JSON and package a small review dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from kdp.clean import clean_document
from kdp.clean.normalize import infer_structure, sanitize_title
from kdp.config import load_config
from kdp.dataset.build import build_dataset
from kdp.dataset.writers import write_json, write_text
from kdp.extract.paddleocr_lines import document_from_paddleocr


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ocr_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", default="raw/pdf/no-copy.pdf")
    parser.add_argument("--title", default="1분간 건강단련법")
    parser.add_argument("--max-tokens", type=int, default=512)
    return parser.parse_args()


def main() -> None:
    args = _arguments()
    payload = json.loads(args.ocr_json.read_text(encoding="utf-8"))
    document = document_from_paddleocr(
        payload,
        source_path=args.source,
        doc_id="no-copy-pages-8-22",
        title=args.title,
    )

    config = load_config(
        overrides={
            "paths.out_dir": args.output,
            "normalize.spacing_engine": "none",
            "normalize.spacing_ocr_only": True,
            "normalize.infer_headings": False,
            "chunk.max_tokens": args.max_tokens,
            "chunk.min_tokens": 32,
            "quality.min_block_chars": 2,
            "dataset.val_ratio": 0.0,
            "dataset.write_parquet": False,
            "dataset.name": "north-korean-ocr-trial",
            "sft.tasks": ["summarize_title", "continuation"],
            "sft.max_samples_per_doc": 50,
        }
    )
    document = infer_structure(document, config.normalize)
    result = clean_document(document, config)
    if result.dropped:
        raise RuntimeError(f"normalized trial was rejected: {result.drop_reason}")
    document = sanitize_title(result.document)

    write_json(document.to_dict(), args.output / "normalized.docjson.json")
    write_text(document.to_markdown(), args.output / "normalized.md")
    write_json(result.reports, args.output / "normalization-report.json")
    stats = build_dataset([document], config)
    print(
        f"{stats.chunks} pretraining chunks, {stats.tokens} tokens, "
        f"{stats.sft_samples} SFT samples -> {args.output}"
    )


if __name__ == "__main__":
    main()
