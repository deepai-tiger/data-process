"""End-to-end dataset assembly, from cleaned documents to JSONL on disk."""

from __future__ import annotations

import json

import pytest

from kdp.config import Config
from kdp.dataset.build import build_dataset, render_dataset_card

from factories import document, equation, heading, para, table

PROSE = (
    "물체의 운동을 기술하기 위해서는 위치와 시간의 관계를 알아야 한다. "
    "속도는 위치의 시간에 대한 변화율이며, 가속도는 속도의 변화율이다."
)


def sample_document(doc_id: str = "physics"):
    cells = [
        {"text": t, "row": r, "col": c, "row_span": 1, "col_span": 1, "is_header": r == 0}
        for r, row in enumerate([["항목", "값"], ["중력가속도", "9.8"], ["광속", "3.0e8"]])
        for c, t in enumerate(row)
    ]
    latex = "\\begin{tabular}{|c|c|}\n\\hline\n항목 & 값 \\\\\n\\hline\n\\end{tabular}"
    return document(
        heading("제1장 운동의 법칙", level=1),
        *[para(f"{i}번 문단입니다. {PROSE}", page=1 + i // 3) for i in range(8)],
        para("가속도란 단위 시간당 속도의 변화량을 나타내는 물리량이다. 벡터량이다.", page=3),
        para("질량과 에너지의 관계는 다음과 같이 주어진다.", page=3),
        equation("E = mc^{2}", page=3),
        table(latex, page=4, cells=cells, num_rows=3, num_cols=2),
        doc_id=doc_id,
    )


@pytest.fixture
def config(tmp_path) -> Config:
    # char-heuristic tokenizer and no parquet keeps the test offline and fast
    return Config.model_validate(
        {
            "paths": {"out_dir": str(tmp_path / "out")},
            "chunk": {"tokenizer": "", "max_tokens": 200, "min_tokens": 20},
            "dataset": {"write_parquet": False, "val_ratio": 0.0},
        }
    )


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_both_splits_are_written(config):
    stats = build_dataset([sample_document()], config)
    out = config.paths.dataset_dir
    assert (out / "pretrain" / "train.jsonl").exists()
    assert (out / "sft" / "train.jsonl").exists()
    assert stats.chunks > 0
    assert stats.sft_samples > 0


def test_pretrain_records_carry_provenance(config):
    build_dataset([sample_document()], config)
    record = read_jsonl(config.paths.dataset_dir / "pretrain" / "train.jsonl")[0]
    assert record["id"].startswith("physics#")
    assert record["text"]
    assert record["meta"]["doc_id"] == "physics"
    assert record["meta"]["source_type"] == "pdf"
    assert record["meta"]["pages"]
    assert record["meta"]["n_tokens"] > 0


def test_sft_records_are_conversations_with_the_system_prompt(config):
    build_dataset([sample_document()], config)
    record = read_jsonl(config.paths.dataset_dir / "sft" / "train.jsonl")[0]
    roles = [m["role"] for m in record["messages"]]
    assert roles == ["system", "user", "assistant"]
    assert record["messages"][0]["content"] == config.sft.system_prompt
    assert record["meta"]["task"] in set(config.sft.tasks)


def test_one_rendered_file_per_requested_chat_template(config):
    build_dataset([sample_document()], config)
    sft_dir = config.paths.dataset_dir / "sft"
    for template in config.dataset.render_templates:
        records = read_jsonl(sft_dir / f"train.{template}.jsonl")
        assert records
        assert records[0]["meta"]["template"] == template
        assert isinstance(records[0]["text"], str)


def test_qwen_rendering_uses_chatml_markers(config):
    build_dataset([sample_document()], config)
    record = read_jsonl(config.paths.dataset_dir / "sft" / "train.qwen.jsonl")[0]
    assert record["text"].startswith("<|im_start|>system")


def test_a_duplicate_document_contributes_no_extra_chunks(config):
    stats = build_dataset([sample_document("a"), sample_document("b")], config)
    single = build_dataset([sample_document("a")], config)
    assert stats.chunks == single.chunks


def test_documents_are_split_between_train_and_validation(tmp_path):
    config = Config.model_validate(
        {
            "paths": {"out_dir": str(tmp_path / "out")},
            "chunk": {"tokenizer": "", "max_tokens": 200, "min_tokens": 20},
            "dataset": {"write_parquet": False, "val_ratio": 0.5},
            "dedup": {"exact": False, "near": False},
        }
    )
    docs = [sample_document(f"doc{i}") for i in range(12)]
    build_dataset(docs, config)
    train = read_jsonl(config.paths.dataset_dir / "pretrain" / "train.jsonl")
    val = read_jsonl(config.paths.dataset_dir / "pretrain" / "val.jsonl")
    train_docs = {r["meta"]["doc_id"] for r in train}
    val_docs = {r["meta"]["doc_id"] for r in val}
    assert val_docs
    # a document never straddles the split boundary
    assert train_docs.isdisjoint(val_docs)


def test_stats_json_records_the_configuration_and_the_outcome(config):
    build_dataset([sample_document()], config)
    stats = json.loads((config.paths.dataset_dir / "stats.json").read_text(encoding="utf-8"))
    assert stats["config"]["chunk"]["max_tokens"] == 200
    assert stats["stats"]["documents"] == 1
    assert stats["stats"]["per_document"][0]["doc_id"] == "physics"
    assert stats["dedup"]["kept"] > 0


def test_latex_tasks_reach_the_sft_split(config):
    build_dataset([sample_document()], config)
    tasks = {r["meta"]["task"] for r in read_jsonl(config.paths.dataset_dir / "sft" / "train.jsonl")}
    assert "table_to_latex" in tasks
    assert "equation_to_latex" in tasks


def test_an_empty_corpus_writes_no_dataset_files(config, caplog):
    stats = build_dataset([], config)
    assert stats.chunks == 0
    assert not (config.paths.dataset_dir / "pretrain").exists()
    # the card is still written so the run leaves a record of itself
    assert (config.paths.dataset_dir / "dataset_card.md").exists()


def test_the_dataset_card_reports_the_pipeline_settings(config):
    stats = build_dataset([sample_document()], config)
    card = (config.paths.dataset_dir / "dataset_card.md").read_text(encoding="utf-8")
    assert card.startswith(f"# {config.dataset.name}")
    assert str(config.pdf.dpi) in card
    assert config.ocr.engine in card
    assert config.pdf.formula_engine in card
    assert f"| 사전학습 청크 | {stats.chunks} |" in card


def test_the_card_says_so_when_no_sft_samples_were_produced(config):
    config.sft.enabled = False
    stats = build_dataset([sample_document()], config)
    assert "_SFT 샘플이 생성되지 않았습니다._" in render_dataset_card(stats, config)


def test_parquet_is_written_alongside_jsonl(tmp_path):
    pytest.importorskip("pyarrow")
    config = Config.model_validate(
        {
            "paths": {"out_dir": str(tmp_path / "out")},
            "chunk": {"tokenizer": "", "max_tokens": 200, "min_tokens": 20},
            "dataset": {"write_parquet": True, "val_ratio": 0.0},
        }
    )
    build_dataset([sample_document()], config)
    assert (config.paths.dataset_dir / "pretrain" / "train.parquet").exists()
