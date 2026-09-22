"""Assemble cleaned documents into trainable dataset files.

Outputs (under ``out/dataset/``)::

    pretrain/train.jsonl      {"id", "text", "meta"}          continued pretraining
    pretrain/val.jsonl
    sft/train.jsonl           {"id", "messages", "meta"}      instruction tuning
    sft/val.jsonl
    sft/train.qwen.jsonl      {"id", "text", "meta"}          chat template applied
    sft/train.llama3.jsonl
    sft/train.deepseek.jsonl
    *.parquet                 same records, columnar
    stats.json, dataset_card.md

Splits are assigned per source document, so no document contributes to both
train and validation.
"""

from __future__ import annotations

import hashlib
import logging
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Sequence

from ..clean import dedup as dedup_mod
from ..clean.quality import is_ocr_noise, script_profile, text_quality_reason
from ..config import Config
from ..schema import Document
from .chunk import Chunk, TokenCounter, chunk_document
from .instructions import SftSample, build_sft_samples
from .templates import get_renderer
from .writers import WriteResult, write_json, write_jsonl, write_parquet, write_text

logger = logging.getLogger(__name__)


@dataclass
class BuildStats:
    documents: int = 0
    chunks: int = 0
    chunks_dropped: dict[str, int] = field(default_factory=dict)
    sft_samples: int = 0
    sft_dropped: dict[str, int] = field(default_factory=dict)
    tokens: int = 0
    tasks: dict[str, int] = field(default_factory=dict)
    per_document: list[dict[str, Any]] = field(default_factory=list)
    files: list[dict[str, Any]] = field(default_factory=list)
    tokenizer: str = ""
    script_profile: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "documents": self.documents,
            "chunks": self.chunks,
            "chunks_dropped": self.chunks_dropped,
            "sft_samples": self.sft_samples,
            "sft_dropped": self.sft_dropped,
            "tokens": self.tokens,
            "tasks": self.tasks,
            "tokenizer": self.tokenizer,
            "script_profile": {k: round(v, 4) for k, v in self.script_profile.items()},
            "per_document": self.per_document,
            "files": self.files,
        }


def build_dataset(documents: Sequence[Document], config: Config) -> BuildStats:
    cfg = config.dataset
    stats = BuildStats(documents=len(documents))
    counter = TokenCounter(config.chunk.tokenizer or None)
    stats.tokenizer = counter.name

    deduper = dedup_mod.Deduper(config.dedup)
    pretrain: list[dict[str, Any]] = []
    sft_records: list[dict[str, Any]] = []
    dropped_chunks: Counter[str] = Counter()
    dropped_sft: Counter[str] = Counter()
    tasks: Counter[str] = Counter()
    corpus_text_sample: list[str] = []

    for doc in documents:
        chunks = chunk_document(doc, config.chunk, counter)
        kept_chunks = 0
        for chunk in chunks:
            reason = text_quality_reason(chunk.text, config.quality)
            if reason:
                dropped_chunks[reason] += 1
                continue
            duplicate = deduper.check(chunk.chunk_id, chunk.text)
            if duplicate is not None:
                dropped_chunks["duplicate"] += 1
                continue
            pretrain.append(_pretrain_record(doc, chunk, counter))
            stats.tokens += chunk.n_tokens
            kept_chunks += 1
            if len(corpus_text_sample) < 400:
                corpus_text_sample.append(chunk.text)

        samples = build_sft_samples(doc, config.sft)
        kept_samples = 0
        for index, sample in enumerate(samples):
            reason = _sft_drop_reason(sample, config)
            if reason:
                dropped_sft[reason] += 1
                continue
            sft_records.append(_sft_record(doc, sample, index, config))
            tasks[sample.task] += 1
            kept_samples += 1

        stats.per_document.append(
            {
                "doc_id": doc.doc_id,
                "source_path": doc.source_path,
                "source_type": doc.source_type,
                "pages": doc.n_pages,
                "blocks": doc.counts(),
                "chars": doc.char_count(),
                "chunks": kept_chunks,
                "sft_samples": kept_samples,
                "warnings": doc.warnings,
            }
        )

    stats.chunks = len(pretrain)
    stats.sft_samples = len(sft_records)
    stats.chunks_dropped = dict(dropped_chunks)
    stats.sft_dropped = dict(dropped_sft)
    stats.tasks = dict(tasks)
    stats.script_profile = script_profile("\n".join(corpus_text_sample))

    out_dir = config.paths.dataset_dir
    _write_split(pretrain, out_dir / "pretrain", "pretrain", config, stats, chat_templates=False)
    _write_split(sft_records, out_dir / "sft", "sft", config, stats, chat_templates=True)

    write_json(
        {"config": config.dump(), "stats": stats.as_dict(), "dedup": deduper.report.as_dict()},
        out_dir / "stats.json",
    )
    write_text(render_dataset_card(stats, config), out_dir / "dataset_card.md")
    logger.info(
        "dataset: %d pretrain chunks (%d tokens), %d sft samples -> %s",
        stats.chunks,
        stats.tokens,
        stats.sft_samples,
        out_dir,
    )
    return stats


def _pretrain_record(doc: Document, chunk: Chunk, counter: TokenCounter) -> dict[str, Any]:
    return {
        "id": chunk.chunk_id,
        "text": chunk.text,
        "meta": {
            "doc_id": doc.doc_id,
            "source_path": doc.source_path,
            "source_type": doc.source_type,
            "pages": chunk.pages,
            "heading_path": chunk.heading_path,
            "n_tokens": chunk.n_tokens,
            "tokenizer": counter.name,
            "block_kinds": chunk.block_kinds,
            "has_latex": chunk.has_latex(),
            "extractor": doc.meta.get("extractor"),
            "ocr_engine": doc.meta.get("ocr_engine"),
        },
    }


def _sft_record(doc: Document, sample: SftSample, index: int, config: Config) -> dict[str, Any]:
    messages = sample.messages(config.sft.system_prompt)
    return {
        "id": f"{doc.doc_id}#sft{index:05d}",
        "messages": messages,
        "meta": {
            "task": sample.task,
            "doc_id": doc.doc_id,
            "source_path": doc.source_path,
            "source_type": doc.source_type,
            "pages": sample.pages,
            "heading_path": sample.heading_path,
        },
    }


#: an acceptable answer length depends on the task: a generated title is a few
#: words, a continuation is a few paragraphs
_MIN_OUTPUT_CHARS = {"summarize_title": 4, "qa_definition": 30, "continuation": 200}


def _sft_drop_reason(sample: SftSample, config: Config) -> str | None:
    output = sample.output.strip()
    if not output:
        return "empty_output"
    if sample.task in ("table_to_latex", "equation_to_latex"):
        return None  # LaTeX answers are already validated at extraction time
    if len(output) < _MIN_OUTPUT_CHARS.get(sample.task, 50):
        return "output_too_short"
    if sample.task == "continuation":
        return text_quality_reason(output, config.quality)
    return "ocr_noise" if is_ocr_noise(output) else None


def _split_for(doc_id: str, val_ratio: float, seed: int) -> str:
    if val_ratio <= 0:
        return "train"
    digest = hashlib.sha1(f"{seed}:{doc_id}".encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) / 0xFFFFFFFF
    return "val" if bucket < val_ratio else "train"


def _write_split(
    records: Sequence[dict[str, Any]],
    out_dir: Path,
    name: str,
    config: Config,
    stats: BuildStats,
    chat_templates: bool,
) -> None:
    if not records:
        logger.warning("no %s records to write", name)
        return
    cfg = config.dataset
    buckets: dict[str, list[dict[str, Any]]] = {"train": [], "val": []}
    for record in records:
        doc_id = record["meta"]["doc_id"]
        buckets[_split_for(doc_id, cfg.val_ratio, cfg.seed)].append(record)

    for split, split_records in buckets.items():
        if not split_records:
            continue
        result = write_jsonl(split_records, out_dir / f"{split}.jsonl", cfg.shard_size)
        stats.files.append({"dataset": name, "split": split, "format": "jsonl", **result.as_dict()})
        if cfg.write_parquet:
            parquet = write_parquet(split_records, out_dir / f"{split}.parquet")
            if parquet:
                stats.files.append(
                    {
                        "dataset": name,
                        "split": split,
                        "format": "parquet",
                        "path": str(parquet),
                        "records": len(split_records),
                    }
                )
        if chat_templates:
            for template in cfg.render_templates:
                rendered = _render_template(split_records, template)
                if rendered is None:
                    continue
                result = write_jsonl(rendered, out_dir / f"{split}.{_safe_name(template)}.jsonl", cfg.shard_size)
                stats.files.append(
                    {
                        "dataset": name,
                        "split": split,
                        "format": f"jsonl:{template}",
                        **result.as_dict(),
                    }
                )


def _render_template(records: Sequence[dict[str, Any]], template: str) -> list[dict[str, Any]] | None:
    try:
        renderer = get_renderer(template)
    except Exception as exc:
        logger.warning("chat template '%s' unavailable: %s", template, exc)
        return None
    return [
        {"id": record["id"], "text": renderer(record["messages"]), "meta": {**record["meta"], "template": template}}
        for record in records
    ]


def _safe_name(template: str) -> str:
    return template.replace("hf:", "").replace("/", "_")


def render_dataset_card(stats: BuildStats, config: Config) -> str:
    profile = stats.script_profile
    lines = [
        f"# {config.dataset.name}",
        "",
        "한국어 LLM 학습용 데이터셋. `data-process` 파이프라인이 PDF/DOC/DOCX 원본에서 자동 생성했습니다.",
        "",
        "## 규모",
        "",
        "| 항목 | 값 |",
        "| --- | --- |",
        f"| 원본 문서 수 | {stats.documents} |",
        f"| 사전학습 청크 | {stats.chunks} |",
        f"| 토큰 수 ({stats.tokenizer}) | {stats.tokens:,} |",
        f"| SFT 샘플 | {stats.sft_samples} |",
        "",
        "## 생성 방법",
        "",
        f"- PDF: 페이지를 {config.pdf.dpi} DPI 이미지로 변환 후 레이아웃 분석 + OCR"
        f" (`{config.ocr.engine}`, 언어 {'+'.join(config.ocr.languages)}). PDF 텍스트 레이어는 사용하지 않음.",
        f"- 표: TableFormer(`{config.pdf.table_mode}`) 구조 인식 후 LaTeX `tabular` 변환.",
        f"- 수식: `{config.pdf.formula_engine}` 기반 LaTeX 변환, Word 문서는 OMML -> LaTeX 직접 변환.",
        "- 그림/사진: 요구사항에 따라 제외.",
        f"- 한국어 띄어쓰기 교정: `{config.normalize.spacing_engine}`.",
        f"- 중복 제거: exact + MinHash(threshold={config.dedup.threshold}).",
        f"- 개인정보 마스킹: {'활성' if config.pii.enabled else '비활성'}"
        " (이메일/전화번호/주민등록번호/카드번호).",
        "",
        "## 문자 구성 (표본)",
        "",
        "| 분류 | 비율 |",
        "| --- | --- |",
        f"| 한글 | {profile.get('hangul', 0):.1%} |",
        f"| 라틴 | {profile.get('latin', 0):.1%} |",
        f"| 한자 | {profile.get('cjk', 0):.1%} |",
        f"| 숫자 | {profile.get('digit', 0):.1%} |",
        "",
        "## SFT 과제 구성",
        "",
    ]
    if stats.tasks:
        lines += ["| 과제 | 샘플 수 |", "| --- | --- |"]
        lines += [f"| {task} | {count} |" for task, count in sorted(stats.tasks.items())]
    else:
        lines.append("_SFT 샘플이 생성되지 않았습니다._")
    lines += [
        "",
        "## 사용 예",
        "",
        "```python",
        "from datasets import load_dataset",
        "",
        'ds = load_dataset("json", data_files={',
        '    "train": "out/dataset/pretrain/train.jsonl",',
        '    "validation": "out/dataset/pretrain/val.jsonl",',
        "})",
        "```",
        "",
        "## 한계 및 주의사항",
        "",
        "- OCR 기반이므로 오탈자가 남아 있습니다. 문자 오류율이 중요한 경우 `out/reports/`의",
        "  품질 지표와 페이지 이미지(`out/work/pages/`)를 비교해 검수하십시오.",
        "- 수식/표 LaTeX는 인식 모델 출력이며 원본과 다를 수 있습니다. 괄호 균형 등",
        "  기본 검증만 통과한 상태입니다.",
        "- 학습 데이터로 사용하기 전에 원본 문서의 저작권/이용 조건을 확인하십시오"
        f" (현재 설정: {config.dataset.license}).",
        "",
    ]
    return "\n".join(lines)
