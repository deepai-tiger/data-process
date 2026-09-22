"""``kdp`` command line interface."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Optional

import typer

from .config import Config, load_config
from .logging_utils import setup_logging

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Build a clean Korean LLM training dataset from PDF/DOC/DOCX sources.",
)

ConfigOption = typer.Option(None, "--config", "-c", help="YAML config file (default: configs/default.yaml)")
RawOption = typer.Option(None, "--raw", help="Input directory or single file")
OutOption = typer.Option(None, "--out", "-o", help="Output directory (default: out/)")
PagesOption = typer.Option(None, "--pages", help="1-based page selection, e.g. '1-20,35'")
MaxPagesOption = typer.Option(None, "--max-pages", help="Process at most N pages per PDF")
DpiOption = typer.Option(None, "--dpi", help="Page rasterization DPI (default 200)")
OcrOption = typer.Option(None, "--ocr", help="OCR engine: tesseract_cli | easyocr | rapidocr")
FormulaOption = typer.Option(None, "--formula", help="Equation engine: pix2tex | docling | none")
LogOption = typer.Option(None, "--log-level", help="DEBUG | INFO | WARNING | ERROR")


def _config(
    config: Optional[Path],
    raw: Optional[Path] = None,
    out: Optional[Path] = None,
    pages: Optional[str] = None,
    max_pages: Optional[int] = None,
    dpi: Optional[int] = None,
    ocr: Optional[str] = None,
    formula: Optional[str] = None,
    log_level: Optional[str] = None,
    **extra: object,
) -> Config:
    overrides: dict[str, object] = {
        "paths.raw_dir": raw,
        "paths.out_dir": out,
        "pdf.pages": pages,
        "pdf.max_pages": max_pages,
        "pdf.dpi": dpi,
        "ocr.engine": ocr,
        "pdf.formula_engine": formula,
        "log_level": log_level,
        **extra,
    }
    cfg = load_config(config, overrides={k: v for k, v in overrides.items() if v is not None})
    setup_logging(cfg.log_level)
    return cfg


@app.command()
def extract(
    config: Optional[Path] = ConfigOption,
    raw: Optional[Path] = RawOption,
    out: Optional[Path] = OutOption,
    pages: Optional[str] = PagesOption,
    max_pages: Optional[int] = MaxPagesOption,
    dpi: Optional[int] = DpiOption,
    ocr: Optional[str] = OcrOption,
    formula: Optional[str] = FormulaOption,
    log_level: Optional[str] = LogOption,
    force: bool = typer.Option(False, "--force", help="Re-extract documents that already have output"),
) -> None:
    """Stage 1: layout analysis + OCR + LaTeX, one JSON document per source file."""
    from .pipeline import run_extract

    cfg = _config(config, raw, out, pages, max_pages, dpi, ocr, formula, log_level)
    inputs = [Path(raw)] if raw and Path(raw).is_file() else None
    summary = run_extract(cfg, inputs=inputs, force=force)
    typer.echo(
        f"extracted {len(summary.documents)} document(s) in {summary.elapsed_s:.1f}s "
        f"-> {cfg.paths.docjson_dir}"
    )
    for failure in summary.failures:
        typer.secho(f"  failed: {failure['path']}: {failure['error']}", fg=typer.colors.RED)
    if summary.failures:
        raise typer.Exit(code=1)


@app.command()
def clean(
    config: Optional[Path] = ConfigOption,
    out: Optional[Path] = OutOption,
    log_level: Optional[str] = LogOption,
) -> None:
    """Stage 2: spacing repair, normalization, quality filters, PII masking, dedup."""
    from .pipeline import run_clean

    cfg = _config(config, out=out, log_level=log_level)
    documents = run_clean(cfg)
    typer.echo(f"cleaned {len(documents)} document(s) -> {cfg.paths.clean_dir}")


@app.command()
def build(
    config: Optional[Path] = ConfigOption,
    out: Optional[Path] = OutOption,
    max_tokens: Optional[int] = typer.Option(None, "--max-tokens", help="Chunk size in tokens"),
    tokenizer: Optional[str] = typer.Option(None, "--tokenizer", help="HF tokenizer id for length control"),
    log_level: Optional[str] = LogOption,
) -> None:
    """Stage 3: chunk, synthesize instructions, write JSONL/Parquet + dataset card."""
    from .pipeline import run_build

    extra = {}
    if max_tokens is not None:
        extra["chunk.max_tokens"] = max_tokens
    if tokenizer is not None:
        extra["chunk.tokenizer"] = tokenizer
    cfg = _config(config, out=out, log_level=log_level, **extra)
    stats = run_build(cfg)
    typer.echo(
        f"{stats.chunks} pretrain chunks ({stats.tokens:,} tokens, {stats.tokenizer}), "
        f"{stats.sft_samples} SFT samples -> {cfg.paths.dataset_dir}"
    )


@app.command("run")
def run_all(
    config: Optional[Path] = ConfigOption,
    raw: Optional[Path] = RawOption,
    out: Optional[Path] = OutOption,
    pages: Optional[str] = PagesOption,
    max_pages: Optional[int] = MaxPagesOption,
    dpi: Optional[int] = DpiOption,
    ocr: Optional[str] = OcrOption,
    formula: Optional[str] = FormulaOption,
    log_level: Optional[str] = LogOption,
    force: bool = typer.Option(False, "--force", help="Re-extract documents that already have output"),
) -> None:
    """Run all three stages end to end."""
    from .pipeline import run_pipeline

    cfg = _config(config, raw, out, pages, max_pages, dpi, ocr, formula, log_level)
    inputs = [Path(raw)] if raw and Path(raw).is_file() else None
    result = run_pipeline(cfg, inputs=inputs, force=force)
    typer.echo(
        f"documents: {len(result.documents)} | pretrain chunks: {result.build.chunks} "
        f"({result.build.tokens:,} tokens) | SFT samples: {result.build.sft_samples}"
    )
    typer.echo(f"dataset: {cfg.paths.dataset_dir}")


@app.command()
def inspect(
    target: Path = typer.Argument(..., help="A docjson file, or a doc_id present in out/"),
    config: Optional[Path] = ConfigOption,
    markdown: bool = typer.Option(False, "--markdown", "-m", help="Print the rendered Markdown"),
    limit: int = typer.Option(20, "--limit", "-n", help="How many blocks to show"),
) -> None:
    """Show what was extracted from one document."""
    from .schema import Document

    cfg = _config(config)
    path = target if target.exists() else cfg.paths.docjson_dir / f"{target}.json"
    if not path.exists():
        typer.secho(f"not found: {path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    doc = Document.load(path)
    typer.echo(f"doc_id     : {doc.doc_id}")
    typer.echo(f"source     : {doc.source_path} ({doc.source_type}, {doc.n_pages} pages)")
    typer.echo(f"title      : {doc.title}")
    typer.echo(f"blocks     : {json.dumps(doc.counts(), ensure_ascii=False)}")
    typer.echo(f"characters : {doc.char_count():,}")
    if doc.warnings:
        typer.echo("warnings   :")
        for warning in doc.warnings:
            typer.echo(f"  - {warning}")
    if markdown:
        typer.echo("\n" + doc.to_markdown())
        return
    typer.echo("")
    for block in doc.blocks[:limit]:
        payload = (block.payload or "").replace("\n", " ")
        typer.echo(f"[{block.kind.value:<13} p{block.page}] {payload[:160]}")


@app.command()
def doctor(config: Optional[Path] = ConfigOption) -> None:
    """Check system dependencies and model availability."""
    cfg = _config(config)
    ok = True

    def report(name: str, detail: str, healthy: bool, hint: str = "") -> None:
        nonlocal ok
        mark = "OK  " if healthy else "MISS"
        colour = typer.colors.GREEN if healthy else typer.colors.RED
        typer.secho(f"[{mark}] {name:<22} {detail}", fg=colour)
        if not healthy and hint:
            typer.echo(f"       -> {hint}")
        ok = ok and healthy

    report("python", sys.version.split()[0], sys.version_info >= (3, 10), "python >= 3.10 required")

    tesseract = shutil.which("tesseract")
    report(
        "tesseract",
        tesseract or "not found",
        bool(tesseract) or cfg.ocr.engine != "tesseract_cli",
        "sudo apt-get install tesseract-ocr tesseract-ocr-kor",
    )
    if tesseract:
        import subprocess

        langs = subprocess.run(
            [tesseract, "--list-langs"], capture_output=True, text=True, check=False
        ).stdout.split()
        report("tesseract kor data", "kor" if "kor" in langs else "missing", "kor" in langs,
               "sudo apt-get install tesseract-ocr-kor")

    soffice = shutil.which(cfg.word.soffice_bin) or shutil.which("libreoffice")
    report("libreoffice", soffice or "not found", bool(soffice), "sudo apt-get install libreoffice-writer")

    for module, hint, optional in (
        ("docling", "pip install docling", False),
        ("pymupdf", "pip install pymupdf", False),
        ("kiwipiepy", "pip install kiwipiepy  (Korean spacing repair)", True),
        ("pix2tex", "pip install pix2tex  (equation -> LaTeX)", True),
        ("transformers", "pip install transformers  (tokenizer-accurate chunking)", True),
    ):
        try:
            __import__(module)
            report(module, "importable", True)
        except ImportError:
            if optional:
                typer.secho(f"[WARN] {module:<22} not installed (optional)", fg=typer.colors.YELLOW)
                typer.echo(f"       -> {hint}")
            else:
                report(module, "not installed", False, hint)

    typer.echo("")
    typer.echo(f"raw dir : {cfg.paths.raw_dir} ({'exists' if cfg.paths.raw_dir.exists() else 'MISSING'})")
    typer.echo(f"out dir : {cfg.paths.out_dir}")
    if not ok:
        raise typer.Exit(code=1)


@app.command()
def stats(config: Optional[Path] = ConfigOption) -> None:
    """Print the dataset statistics produced by the last build."""
    cfg = _config(config)
    path = cfg.paths.dataset_dir / "stats.json"
    if not path.exists():
        typer.secho(f"no stats at {path}; run `kdp build` first", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    payload = json.loads(path.read_text(encoding="utf-8"))["stats"]
    typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))


def main() -> None:  # pragma: no cover - console entry point
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
