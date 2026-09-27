#!/usr/bin/env python3
"""Recognize selected formula/table crops with PaddleOCR-VL."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image

from kdp.extract.rasterize import rasterize_pdf


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--page-dir", type=Path, default=Path("out/work/paddleocr-vl-pages"))
    return parser.parse_args()


def strip_display_math(markdown: str) -> str:
    """Remove only an outer ``$$`` pair from a VLM formula response."""
    return re.sub(r"^\s*\$\$\s*|\s*\$\$\s*$", "", markdown.strip()).strip()


def load_manifest(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not payload.get("source_pdf") or not payload.get("regions"):
        raise ValueError("manifest requires source_pdf and a non-empty regions list")
    for region in payload["regions"]:
        if region.get("prompt") not in {"formula", "table"}:
            raise ValueError(f"invalid prompt for region {region.get('id')!r}")
        bbox = region.get("bbox") or []
        if len(bbox) != 4 or bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
            raise ValueError(f"invalid bbox for region {region.get('id')!r}")
    return payload


def main() -> None:
    args = _arguments()
    manifest = load_manifest(args.manifest)
    pages = sorted({int(region["page"]) for region in manifest["regions"]})
    rendered = {
        image.page_no: image
        for image in rasterize_pdf(
            manifest["source_pdf"],
            args.page_dir,
            pages=pages,
            dpi=int(manifest.get("dpi", 200)),
        )
    }

    os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
    from paddleocr import PaddleOCRVL

    pipeline = PaddleOCRVL(
        pipeline_version=manifest.get("pipeline_version", "v1.6"),
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_layout_detection=False,
    )

    records: list[dict[str, Any]] = []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for index, region in enumerate(manifest["regions"], 1):
        page_no = int(region["page"])
        image = rendered[page_no]
        with Image.open(image.path) as page_image:
            crop = page_image.crop(tuple(int(value) for value in region["bbox"]))
            [result] = pipeline.predict(
                np.asarray(crop),
                prompt_label=region["prompt"],
                format_block_content=True,
            )
        markdown = result.markdown["markdown_texts"].strip()
        records.append(
            {
                **region,
                "model": "PaddleOCR-VL-1.6-0.9B",
                "raw_markdown": markdown,
                "content": strip_display_math(markdown)
                if region["prompt"] == "formula"
                else markdown,
            }
        )
        args.output.write_text(
            json.dumps({"regions": records}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"{index}/{len(manifest['regions'])}: page {page_no} {region['id']}", flush=True)


if __name__ == "__main__":
    main()
