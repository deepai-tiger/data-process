"""Typed configuration for the whole pipeline (YAML file + CLI overrides)."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "default.yaml"


class PathsConfig(BaseModel):
    raw_dir: Path = Path("raw")
    out_dir: Path = Path("out")

    @property
    def work_dir(self) -> Path:
        return self.out_dir / "work"

    @property
    def docjson_dir(self) -> Path:
        return self.out_dir / "interim" / "docjson"

    @property
    def markdown_dir(self) -> Path:
        return self.out_dir / "interim" / "markdown"

    @property
    def clean_dir(self) -> Path:
        return self.out_dir / "interim" / "clean"

    @property
    def dataset_dir(self) -> Path:
        return self.out_dir / "dataset"

    @property
    def report_dir(self) -> Path:
        return self.out_dir / "reports"


class OcrConfig(BaseModel):
    #: ``tesseract_cli`` needs the ``tesseract`` binary + ``tesseract-ocr-kor``;
    #: ``easyocr`` and ``rapidocr`` download their weights on first use.
    engine: Literal["tesseract_cli", "easyocr", "rapidocr"] = "tesseract_cli"
    #: engine-specific language codes (tesseract: kor/eng, easyocr: ko/en)
    languages: list[str] = Field(default_factory=lambda: ["kor", "eng"])
    #: always OCR the full page image instead of trusting any embedded text
    force_full_page: bool = True
    #: drop OCR cells below this confidence (engine dependent, 0 disables)
    min_confidence: float = 0.0


class PdfConfig(BaseModel):
    #: ``page_images`` rasterizes every page to PNG first and never touches the
    #: PDF text layer; ``docling_native`` lets docling load the PDF and forces
    #: full-page OCR on top of it (faster, but reads the file directly).
    mode: Literal["page_images", "docling_native"] = "page_images"
    dpi: int = 200
    #: 1-based inclusive page range, e.g. "1-20,35"; empty means all pages
    pages: str = ""
    max_pages: int | None = None
    #: TableFormer structure model; ``accurate`` is slower but handles
    #: multi-row/colspan layouts far better
    table_mode: Literal["fast", "accurate"] = "accurate"
    do_tables: bool = True
    #: turn detected equation regions into LaTeX
    do_formulas: bool = True
    #: ``pix2tex`` (~1-2 s/equation on CPU) or ``docling``'s CodeFormula VLM
    #: (better on messy scans, but needs a GPU to be practical)
    formula_engine: Literal["pix2tex", "docling", "none"] = "pix2tex"
    #: stacked equations inside one region are recognized one by one
    formula_split_stacked: bool = True
    formula_strip_equation_number: bool = True
    #: keep the rendered page PNGs after extraction (useful for debugging)
    keep_page_images: bool = True
    #: cache per-page extraction results so re-runs resume instead of redoing OCR
    cache: bool = True


class WordConfig(BaseModel):
    #: LibreOffice binary used to convert legacy .doc/.hwp-style binaries to OOXML
    soffice_bin: str = "soffice"
    convert_timeout_s: int = 240
    keep_converted: bool = True
    include_footnotes: bool = True
    include_headers_footers: bool = False


class NormalizeConfig(BaseModel):
    #: Korean word-spacing repair for OCR text; ``kiwi`` needs ``kiwipiepy``
    spacing_engine: Literal["kiwi", "none"] = "kiwi"
    #: only re-space OCR-sourced documents (Word text is already spaced)
    spacing_ocr_only: bool = True
    unicode_form: Literal["NFC", "NFKC"] = "NFC"
    strip_control_chars: bool = True
    #: collapse the soft line breaks OCR introduces inside one paragraph
    join_wrapped_lines: bool = True
    dehyphenate: bool = True
    normalize_punctuation: bool = True
    #: stitch a paragraph that continues onto the next page back together
    merge_page_continuations: bool = True
    #: recover the section hierarchy in files without heading styles
    #: (e.g. "제1장", "제2절", "1.1") so chunking can follow it
    infer_headings: bool = True
    #: drop running headers/footers that repeat on at least this share of pages
    header_footer_page_ratio: float = 0.5
    drop_page_numbers: bool = True


class QualityConfig(BaseModel):
    min_doc_chars: int = 200
    min_block_chars: int = 10
    #: minimum share of Hangul among letter-ish characters for a text block
    min_hangul_ratio: float = 0.25
    #: blocks/documents above these ratios look like OCR garbage
    max_symbol_ratio: float = 0.30
    max_digit_ratio: float = 0.50
    #: Gopher-style repetition guards
    max_dup_line_ratio: float = 0.30
    max_top_ngram_ratio: float = 0.20
    #: a Hangul-free block is kept only when it is code/LaTeX-ish
    keep_latin_only_blocks: bool = True


class DedupConfig(BaseModel):
    exact: bool = True
    near: bool = True
    #: MinHash Jaccard threshold on character shingles
    threshold: float = 0.85
    num_perm: int = 128
    shingle_size: int = 5
    #: also drop paragraph-level duplicates shared across documents
    paragraph_level: bool = True
    min_paragraph_chars_for_dedup: int = 80


class PiiConfig(BaseModel):
    enabled: bool = True
    mask_email: bool = True
    mask_phone: bool = True
    #: 주민등록번호 / 사업자등록번호 style identifiers
    mask_rrn: bool = True
    mask_card: bool = True
    mask_url: bool = False
    placeholder_prefix: str = "[MASKED_"


class ChunkConfig(BaseModel):
    #: tokenizer used for length control; falls back to a char heuristic when
    #: transformers/the model is unavailable offline
    tokenizer: str = "Qwen/Qwen2.5-7B"
    max_tokens: int = 2048
    min_tokens: int = 64
    overlap_tokens: int = 0
    #: never split a table/equation across chunks
    keep_latex_atomic: bool = True
    #: prepend the heading path ("장 > 절") to every chunk
    prepend_heading_path: bool = True


class SftConfig(BaseModel):
    enabled: bool = True
    tasks: list[
        Literal["summarize_title", "continuation", "table_to_latex", "equation_to_latex", "qa_definition"]
    ] = Field(
        default_factory=lambda: [
            "summarize_title",
            "continuation",
            "table_to_latex",
            "equation_to_latex",
            "qa_definition",
        ]
    )
    system_prompt: str = "당신은 한국어 문서를 정확하게 이해하고 답변하는 유용한 AI 어시스턴트입니다."
    max_samples_per_doc: int = 200
    seed: int = 20240501


class DatasetConfig(BaseModel):
    name: str = "korean-doc-corpus"
    #: chat templates rendered next to the raw conversations
    render_templates: list[Literal["qwen", "llama3", "deepseek", "chatml"]] = Field(
        default_factory=lambda: ["qwen", "llama3", "deepseek"]
    )
    val_ratio: float = 0.02
    seed: int = 20240501
    write_parquet: bool = True
    shard_size: int = 20000
    license: str = "unknown - inherit from the source documents"


class Config(BaseModel):
    paths: PathsConfig = Field(default_factory=PathsConfig)
    ocr: OcrConfig = Field(default_factory=OcrConfig)
    pdf: PdfConfig = Field(default_factory=PdfConfig)
    word: WordConfig = Field(default_factory=WordConfig)
    normalize: NormalizeConfig = Field(default_factory=NormalizeConfig)
    quality: QualityConfig = Field(default_factory=QualityConfig)
    dedup: DedupConfig = Field(default_factory=DedupConfig)
    pii: PiiConfig = Field(default_factory=PiiConfig)
    chunk: ChunkConfig = Field(default_factory=ChunkConfig)
    sft: SftConfig = Field(default_factory=SftConfig)
    dataset: DatasetConfig = Field(default_factory=DatasetConfig)
    workers: int = 1
    log_level: str = "INFO"

    def dump(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: str | Path | None = None, overrides: dict[str, Any] | None = None) -> Config:
    """Load YAML config, falling back to ``configs/default.yaml`` then defaults."""
    raw: dict[str, Any] = {}
    candidate = Path(path) if path else DEFAULT_CONFIG_PATH
    if candidate.exists():
        raw = yaml.safe_load(candidate.read_text(encoding="utf-8")) or {}
    elif path:
        raise FileNotFoundError(f"config file not found: {candidate}")
    if overrides:
        raw = _deep_merge(raw, _expand_dotted(overrides))
    return Config.model_validate(raw)


def _expand_dotted(flat: dict[str, Any]) -> dict[str, Any]:
    """Turn ``{"pdf.dpi": 300}`` into ``{"pdf": {"dpi": 300}}``."""
    nested: dict[str, Any] = {}
    for key, value in flat.items():
        if value is None:
            continue
        cursor = nested
        parts = key.split(".")
        for part in parts[:-1]:
            cursor = cursor.setdefault(part, {})
        cursor[parts[-1]] = value
    return nested


def parse_page_spec(spec: str, n_pages: int) -> list[int]:
    """Parse ``"1-3,7"`` into ``[1, 2, 3, 7]`` (1-based, clamped to n_pages)."""
    if not spec.strip():
        return list(range(1, n_pages + 1))
    pages: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, _, end_s = part.partition("-")
            start = int(start_s or 1)
            end = int(end_s or n_pages)
        else:
            start = end = int(part)
        for page in range(max(1, start), min(n_pages, end) + 1):
            if page not in pages:
                pages.append(page)
    return sorted(pages)
