#!/usr/bin/env python3
"""Run a page-image-only Korean OCR trial on a selected PDF page range."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from kdp.config import parse_page_spec
from kdp.extract.rasterize import page_count, rasterize_pdf

DETECTION_MODEL = "PP-OCRv5_mobile_det"
RECOGNITION_MODEL = "korean_PP-OCRv5_mobile_rec"


def _keep_line(text: str, score: float, box: list[int], min_confidence: float) -> bool:
    if not text.strip() or score < min_confidence:
        return False
    # Fine strokes in illustrations (drawer handles in the trial document) are
    # occasionally recognized as high-confidence one-digit lines. Real list
    # markers are visibly wider at this DPI.
    return not (re.fullmatch(r"\d", text.strip()) and int(box[2]) - int(box[0]) < 20)


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rasterize selected PDF pages and OCR them with PP-OCRv5 Korean."
    )
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--pages", default="8-22", help="1-based page range (default: 8-22)")
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.8,
        help="Drop lower-confidence OCR lines (default: 0.8; use 0 for raw output)",
    )
    parser.add_argument("--output", type=Path, required=True, help="Markdown output path")
    parser.add_argument("--json-output", type=Path, help="Optional line/bbox/confidence JSON")
    parser.add_argument("--page-dir", type=Path, default=Path("out/work/paddleocr-trial"))
    return parser.parse_args()


def _build_ocr():
    # Skip an unnecessary host availability probe while still allowing the
    # official model downloader to fetch missing weights.
    os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
    from paddleocr import PaddleOCR

    return PaddleOCR(
        text_detection_model_name=DETECTION_MODEL,
        text_recognition_model_name=RECOGNITION_MODEL,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        # Paddle 3.3.1's oneDNN path cannot execute an ArrayAttribute used by
        # the detector on CPU. The plain CPU kernels work correctly.
        enable_mkldnn=False,
    )


def main() -> None:
    args = _arguments()
    pages = parse_page_spec(args.pages, page_count(args.pdf))
    page_images = rasterize_pdf(args.pdf, args.page_dir, pages=pages, dpi=args.dpi)
    ocr = _build_ocr()

    structured_pages: list[dict[str, object]] = []
    markdown = [
        f"# {args.pdf.name} OCR trial",
        "",
        f"- Pages: {args.pages} (1-based)",
        f"- Input: page PNGs rasterized at {args.dpi} DPI; the PDF text layer was not read",
        f"- OCR: {DETECTION_MODEL} + `{RECOGNITION_MODEL}`",
        f"- Minimum line confidence: {args.min_confidence}",
        "- Spelling/spacing post-processing: none (North Korean forms are preserved)",
        "",
    ]

    for image in page_images:
        result = next(iter(ocr.predict(str(image.path))))
        data = result.json["res"]
        lines = [
            {
                "text": text,
                "confidence": round(float(score), 6),
                "bbox": [int(value) for value in box],
            }
            for text, score, box in zip(
                data["rec_texts"], data["rec_scores"], data["rec_boxes"], strict=True
            )
            if _keep_line(text, float(score), box, args.min_confidence)
        ]
        structured_pages.append({"page": image.page_no, "lines": lines})
        markdown.extend(
            [f"## Page {image.page_no}", "", *(str(line["text"]) for line in lines), ""]
        )
        print(f"page {image.page_no}: {len(lines)} lines")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(markdown), encoding="utf-8")
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps({"pages": structured_pages}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
