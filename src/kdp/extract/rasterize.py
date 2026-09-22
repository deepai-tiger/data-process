"""Turn every PDF page into a page image.

The rest of the PDF pipeline only ever sees these images: we deliberately never
read the PDF text layer, because scanned documents have none and many Korean
PDFs carry a broken ToUnicode mapping (copying yields mojibake or CJK garbage).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PageImage:
    page_no: int  # 1-based
    path: Path
    width: int
    height: int
    dpi: int

    @property
    def scale(self) -> float:
        """Points-per-pixel factor, for mapping bboxes back to PDF coordinates."""
        return 72.0 / float(self.dpi)


def page_count(pdf_path: str | Path) -> int:
    import pymupdf

    with pymupdf.open(pdf_path) as doc:
        return doc.page_count


def pdf_metadata(pdf_path: str | Path) -> dict[str, str]:
    import pymupdf

    with pymupdf.open(pdf_path) as doc:
        return {k: v for k, v in (doc.metadata or {}).items() if v}


def rasterize_pdf(
    pdf_path: str | Path,
    out_dir: str | Path,
    pages: list[int] | None = None,
    dpi: int = 200,
    grayscale: bool = True,
    overwrite: bool = False,
) -> list[PageImage]:
    """Render ``pages`` (1-based) of a PDF to PNG files under ``out_dir``."""
    import pymupdf

    pdf_path = Path(pdf_path)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    colorspace = pymupdf.csGRAY if grayscale else pymupdf.csRGB

    rendered: list[PageImage] = []
    with pymupdf.open(pdf_path) as doc:
        targets = pages or list(range(1, doc.page_count + 1))
        for page_no in targets:
            if not 1 <= page_no <= doc.page_count:
                logger.warning("page %s out of range for %s", page_no, pdf_path.name)
                continue
            dest = out_dir / f"p{page_no:04d}.png"
            if dest.exists() and not overwrite:
                from PIL import Image

                with Image.open(dest) as img:
                    rendered.append(PageImage(page_no, dest, img.width, img.height, dpi))
                continue
            pix = doc[page_no - 1].get_pixmap(dpi=dpi, colorspace=colorspace)
            pix.save(dest)
            rendered.append(PageImage(page_no, dest, pix.width, pix.height, dpi))
    return rendered
