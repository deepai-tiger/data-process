"""PDF extraction through layout analysis of page images.

Pipeline per page:

    PDF page -> PNG (PyMuPDF) -> layout model -> per-region handling
                                              |-> text  : OCR (Korean)
                                              |-> table : TableFormer -> LaTeX
                                              |-> formula: crop -> LaTeX
                                              |-> picture: dropped

The PDF text layer is never read. Two of the three sample PDFs in ``raw/pdf``
show why: one is a scan, and the other two return CJK mojibake or private-use
glyphs when copied, which would silently poison a Korean corpus.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from ..config import Config, parse_page_spec
from ..schema import Block, BlockKind, Document, slugify
from .formula import FormulaRecognizer, build_recognizer, is_plausible_latex, postprocess_latex, recognize_region
from .latex_table import TableCell, TableGrid, grid_to_latex
from .rasterize import PageImage, page_count, pdf_metadata, rasterize_pdf

logger = logging.getLogger(__name__)

CACHE_VERSION = 3


@dataclass
class _PageResult:
    blocks: list[Block]
    stats: dict[str, int]


class PdfLayoutExtractor:
    """Stateful extractor: docling models and the formula model load once."""

    def __init__(self, config: Config) -> None:
        self.cfg = config
        self._converter = None
        self._formula: FormulaRecognizer | None = None

    # ------------------------------------------------------------------ setup
    def _build_converter(self):
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import (
            EasyOcrOptions,
            OcrMode,
            PdfPipelineOptions,
            RapidOcrOptions,
            TableFormerMode,
            TesseractCliOcrOptions,
        )
        from docling.document_converter import DocumentConverter, ImageFormatOption, PdfFormatOption

        ocr_cfg = self.cfg.ocr
        mode = OcrMode.FULL_PAGE if ocr_cfg.force_full_page else OcrMode.LAYOUT_REGIONS
        if ocr_cfg.engine == "tesseract_cli":
            ocr_options: Any = TesseractCliOcrOptions(lang=list(ocr_cfg.languages), mode=mode)
        elif ocr_cfg.engine == "easyocr":
            ocr_options = EasyOcrOptions(
                lang=list(ocr_cfg.languages), mode=mode, confidence_threshold=ocr_cfg.min_confidence
            )
        elif ocr_cfg.engine == "rapidocr":
            ocr_options = RapidOcrOptions(lang=list(ocr_cfg.languages), mode=mode)
        else:  # pragma: no cover - validated by pydantic
            raise ValueError(f"unknown OCR engine: {ocr_cfg.engine}")

        options = PdfPipelineOptions()
        options.do_ocr = True
        options.ocr_options = ocr_options
        options.do_table_structure = self.cfg.pdf.do_tables
        options.table_structure_options.mode = (
            TableFormerMode.ACCURATE if self.cfg.pdf.table_mode == "accurate" else TableFormerMode.FAST
        )
        options.table_structure_options.do_cell_matching = True
        options.do_formula_enrichment = self.cfg.pdf.do_formulas and self.cfg.pdf.formula_engine == "docling"
        options.do_picture_classification = False
        options.do_picture_description = False
        options.generate_picture_images = False
        options.generate_page_images = self.cfg.pdf.mode == "docling_native"
        return DocumentConverter(
            format_options={
                InputFormat.IMAGE: ImageFormatOption(pipeline_options=options),
                InputFormat.PDF: PdfFormatOption(pipeline_options=options),
            }
        )

    @property
    def converter(self):
        if self._converter is None:
            logger.info("loading docling models (ocr=%s, tables=%s)", self.cfg.ocr.engine, self.cfg.pdf.do_tables)
            self._converter = self._build_converter()
        return self._converter

    @property
    def formula_recognizer(self) -> FormulaRecognizer:
        if self._formula is None:
            engine = self.cfg.pdf.formula_engine if self.cfg.pdf.do_formulas else "none"
            self._formula = build_recognizer(engine)
        return self._formula

    # ------------------------------------------------------------- extraction
    def extract(self, path: str | Path) -> Document:
        path = Path(path)
        started = time.time()
        total_pages = page_count(path)
        pages = parse_page_spec(self.cfg.pdf.pages, total_pages)
        if self.cfg.pdf.max_pages:
            pages = pages[: self.cfg.pdf.max_pages]

        doc = Document(
            doc_id=slugify(path.stem),
            source_path=str(path),
            source_type="pdf",
            n_pages=total_pages,
        )
        pdf_meta = pdf_metadata(path)
        doc.title = pdf_meta.get("title") or None

        page_dir = self.cfg.paths.work_dir / "pages" / doc.doc_id
        images = rasterize_pdf(path, page_dir, pages=pages, dpi=self.cfg.pdf.dpi)
        logger.info("%s: rasterized %d/%d pages at %d dpi", path.name, len(images), total_pages, self.cfg.pdf.dpi)

        stats: dict[str, int] = {}
        if self.cfg.pdf.mode == "docling_native":
            result = self._convert_pdf_native(path, images)
            doc.blocks.extend(result.blocks)
            stats.update(result.stats)
        else:
            cache_dir = self.cfg.paths.work_dir / "pagecache" / doc.doc_id
            for index, image in enumerate(images, start=1):
                result = self._page_blocks(image, cache_dir)
                doc.blocks.extend(result.blocks)
                for key, value in result.stats.items():
                    stats[key] = stats.get(key, 0) + value
                if index % 5 == 0 or index == len(images):
                    logger.info("%s: %d/%d pages processed", path.name, index, len(images))

        if not self.cfg.pdf.keep_page_images:
            for image in images:
                image.path.unlink(missing_ok=True)

        doc.meta.update(
            {
                "extractor": "pdf_image_layout",
                "mode": self.cfg.pdf.mode,
                "dpi": self.cfg.pdf.dpi,
                "ocr_engine": self.cfg.ocr.engine,
                "ocr_languages": list(self.cfg.ocr.languages),
                "formula_engine": self.cfg.pdf.formula_engine if self.cfg.pdf.do_formulas else "none",
                "table_mode": self.cfg.pdf.table_mode,
                "pages_processed": [img.page_no for img in images],
                "pdf_metadata": pdf_meta,
                "region_stats": stats,
                "elapsed_s": round(time.time() - started, 2),
            }
        )
        if stats.get("pictures_skipped"):
            doc.warn(f"{stats['pictures_skipped']} picture region(s) skipped by design")
        if stats.get("formulas_rejected"):
            doc.warn(f"{stats['formulas_rejected']} formula region(s) produced implausible LaTeX and were dropped")
        return doc

    # --------------------------------------------------------------- internals
    def _params_hash(self) -> str:
        payload = json.dumps(
            {
                "cache": CACHE_VERSION,
                "dpi": self.cfg.pdf.dpi,
                "ocr": self.cfg.ocr.model_dump(mode="json"),
                "tables": self.cfg.pdf.do_tables,
                "table_mode": self.cfg.pdf.table_mode,
                "formulas": self.cfg.pdf.do_formulas,
                "formula_engine": self.cfg.pdf.formula_engine,
                "split_stacked": self.cfg.pdf.formula_split_stacked,
            },
            sort_keys=True,
        )
        return hashlib.sha1(payload.encode("utf-8")).hexdigest()[:12]

    def _page_blocks(self, image: PageImage, cache_dir: Path) -> _PageResult:
        cache_file = cache_dir / f"p{image.page_no:04d}.{self._params_hash()}.json"
        if self.cfg.pdf.cache and cache_file.exists():
            raw = json.loads(cache_file.read_text(encoding="utf-8"))
            return _PageResult([Block.from_dict(b) for b in raw["blocks"]], raw.get("stats", {}))

        result = self._convert_page(image)
        if self.cfg.pdf.cache:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(
                json.dumps(
                    {"blocks": [b.to_dict() for b in result.blocks], "stats": result.stats},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        return result

    def _convert_page(self, image: PageImage) -> _PageResult:
        from PIL import Image

        started = time.time()
        docling_doc = self.converter.convert(image.path).document
        with Image.open(image.path) as pil_image:
            page_image = pil_image.convert("L")
            blocks, stats = self._map_items(
                docling_doc,
                page_images={n: page_image for n in docling_doc.pages},
                page_no_map={n: image.page_no for n in docling_doc.pages},
            )
        logger.debug("page %d converted in %.1fs", image.page_no, time.time() - started)
        return _PageResult(blocks, stats)

    def _convert_pdf_native(self, path: Path, images: list[PageImage]) -> _PageResult:
        """Let docling open the PDF itself, with full-page OCR forced on top."""
        from PIL import Image

        first, last = images[0].page_no, images[-1].page_no
        docling_doc = self.converter.convert(path, page_range=(first, last)).document
        page_images: dict[int, Any] = {}
        for image in images:
            page = docling_doc.pages.get(image.page_no)
            rendered = getattr(getattr(page, "image", None), "pil_image", None)
            page_images[image.page_no] = rendered or Image.open(image.path).convert("L")
        return _PageResult(
            *self._map_items(
                docling_doc,
                page_images=page_images,
                page_no_map={n: n for n in docling_doc.pages},
            )
        )

    def _map_items(
        self,
        docling_doc,
        page_images: dict[int, Any],
        page_no_map: dict[int, int],
    ) -> tuple[list[Block], dict[str, int]]:
        from docling_core.types.doc import DocItemLabel
        from docling_core.types.doc.document import PictureItem, TableItem, TextItem

        stats: dict[str, int] = {}
        blocks: list[Block] = []
        default_page = next(iter(docling_doc.pages), 1)
        # captions attached to a table/picture are rendered inside the table
        # LaTeX (or dropped with the picture), so skip them as standalone text
        attached_captions = _attached_caption_refs(docling_doc)

        for item, _level in docling_doc.iterate_items():
            if getattr(item, "self_ref", None) in attached_captions:
                stats["captions_attached"] = stats.get("captions_attached", 0) + 1
                continue
            dl_page = item.prov[0].page_no if getattr(item, "prov", None) else default_page
            page_no = page_no_map.get(dl_page, dl_page)
            page = docling_doc.pages.get(dl_page)
            page_image = page_images.get(dl_page)
            scale_x = page_image.width / page.size.width if page and page_image else 1.0
            scale_y = page_image.height / page.size.height if page and page_image else 1.0
            page_height = page.size.height if page else 0.0

            if isinstance(item, PictureItem):
                stats["pictures_skipped"] = stats.get("pictures_skipped", 0) + 1
                continue
            if isinstance(item, TableItem):
                block = self._table_block(item, docling_doc, page_no)
                if block is None:
                    stats["tables_empty"] = stats.get("tables_empty", 0) + 1
                    continue
                stats["tables"] = stats.get("tables", 0) + 1
                blocks.append(block)
                continue
            if not isinstance(item, TextItem):
                continue

            label = item.label
            bbox = self._bbox_px(item, page_height, scale_x, scale_y)
            if label == DocItemLabel.FORMULA:
                block = self._formula_block(item, page_image, bbox, page_no)
                if block is None:
                    stats["formulas_rejected"] = stats.get("formulas_rejected", 0) + 1
                    continue
                stats["formulas"] = stats.get("formulas", 0) + 1
                blocks.append(block)
                continue

            kind, level = _map_label(label, item)
            if kind is None:
                stats["regions_skipped"] = stats.get("regions_skipped", 0) + 1
                continue
            text = (item.text or "").strip()
            if not text:
                continue
            blocks.append(
                Block(
                    kind=kind,
                    text=text,
                    level=level,
                    page=page_no,
                    bbox=bbox,
                    meta={"label": str(label.value if hasattr(label, "value") else label)},
                )
            )
            stats["text_regions"] = stats.get("text_regions", 0) + 1
        return blocks, stats

    @staticmethod
    def _bbox_px(item, page_height: float, scale_x: float, scale_y: float):
        if not getattr(item, "prov", None):
            return None
        bbox = item.prov[0].bbox
        if page_height:
            bbox = bbox.to_top_left_origin(page_height=page_height)
        return (
            round(bbox.l * scale_x, 1),
            round(bbox.t * scale_y, 1),
            round(bbox.r * scale_x, 1),
            round(bbox.b * scale_y, 1),
        )

    def _formula_block(self, item, page_image, bbox, page_no: int) -> Block | None:
        engine = self.cfg.pdf.formula_engine if self.cfg.pdf.do_formulas else "none"
        if engine == "docling":
            latex = postprocess_latex(item.text or "")
            if not latex or not is_plausible_latex(latex):
                return None
            return Block(
                kind=BlockKind.EQUATION,
                text=latex,
                latex=latex,
                page=page_no,
                bbox=bbox,
                meta={"source": "docling_codeformula"},
            )
        if engine == "none" or bbox is None:
            return None

        crop = page_image.crop(_inflate(bbox, page_image.size, margin=6))
        result = recognize_region(
            crop,
            self.formula_recognizer,
            split_stacked=self.cfg.pdf.formula_split_stacked,
            strip_equation_number=self.cfg.pdf.formula_strip_equation_number,
        )
        if result is None:
            return None
        meta: dict[str, Any] = {"source": result.engine, "parts": result.parts}
        if result.tag:
            meta["equation_number"] = result.tag
        return Block(
            kind=BlockKind.EQUATION,
            text=result.latex,
            latex=result.latex,
            page=page_no,
            bbox=bbox,
            meta=meta,
        )

    def _table_block(self, item, docling_doc, page_no: int) -> Block | None:
        cells = [
            TableCell(
                text=_clean_cell_text(cell.text),
                row=cell.start_row_offset_idx,
                col=cell.start_col_offset_idx,
                row_span=max(1, cell.end_row_offset_idx - cell.start_row_offset_idx),
                col_span=max(1, cell.end_col_offset_idx - cell.start_col_offset_idx),
                is_header=bool(cell.column_header),
            )
            for cell in item.data.table_cells
        ]
        caption = item.caption_text(docling_doc) or None
        grid = TableGrid(
            cells=cells, num_rows=item.data.num_rows, num_cols=item.data.num_cols, caption=caption
        ).normalize()
        if grid.is_degenerate():
            return None
        latex = grid_to_latex(grid)
        if not latex:
            return None
        return Block(
            kind=BlockKind.TABLE,
            text=latex,
            latex=latex,
            page=page_no,
            meta={
                "source": "tableformer",
                "num_rows": grid.num_rows,
                "num_cols": grid.num_cols,
                "caption": caption,
                "cells": [
                    {
                        "text": c.text,
                        "row": c.row,
                        "col": c.col,
                        "row_span": c.row_span,
                        "col_span": c.col_span,
                        "is_header": c.is_header,
                    }
                    for c in grid.cells
                ],
            },
        )


def _clean_cell_text(text: str | None) -> str:
    """Strip cell-border artifacts that OCR reads as text (``|``, ``ㅣ``, ``丨``)."""
    cleaned = re.sub(r"[|\uff5c\u4e28\u3163]", " ", text or "")
    return re.sub(r"\s+", " ", cleaned).strip()


def _attached_caption_refs(docling_doc) -> set[str]:
    refs: set[str] = set()
    for collection in (docling_doc.tables, docling_doc.pictures):
        for item in collection or []:
            for caption in getattr(item, "captions", None) or []:
                ref = getattr(caption, "cref", None)
                if ref:
                    refs.add(ref)
    return refs


def _map_label(label, item) -> tuple[BlockKind | None, int | None]:
    from docling_core.types.doc import DocItemLabel

    if label == DocItemLabel.TITLE:
        return BlockKind.TITLE, 1
    if label == DocItemLabel.SECTION_HEADER:
        return BlockKind.HEADING, int(getattr(item, "level", 2) or 2) + 1
    if label == DocItemLabel.LIST_ITEM:
        return BlockKind.LIST_ITEM, None
    if label == DocItemLabel.CAPTION:
        return BlockKind.CAPTION, None
    if label == DocItemLabel.FOOTNOTE:
        return BlockKind.FOOTNOTE, None
    if label == DocItemLabel.CODE:
        return BlockKind.CODE, None
    if label in (DocItemLabel.PAGE_HEADER, DocItemLabel.PAGE_FOOTER, DocItemLabel.DOCUMENT_INDEX):
        return BlockKind.PAGE_ARTIFACT, None
    if label in (DocItemLabel.TEXT, DocItemLabel.PARAGRAPH, DocItemLabel.REFERENCE, DocItemLabel.HANDWRITTEN_TEXT):
        return BlockKind.PARAGRAPH, None
    return None, None


def _inflate(bbox, size: tuple[int, int], margin: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = bbox
    width, height = size
    return (
        max(0, int(left) - margin),
        max(0, int(top) - margin),
        min(width, int(right) + margin),
        min(height, int(bottom) + margin),
    )


def extract_pdf(path: str | Path, config: Config) -> Document:
    """One-shot helper; prefer :class:`PdfLayoutExtractor` for many files."""
    return PdfLayoutExtractor(config).extract(path)
