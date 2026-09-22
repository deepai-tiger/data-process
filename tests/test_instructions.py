"""Deterministic SFT sample synthesis."""

from __future__ import annotations

import pytest

from kdp.config import SftConfig
from kdp.dataset.instructions import build_sft_samples

from factories import document, equation, heading, para, table

PROSE = (
    "물체의 운동을 기술하기 위해서는 위치와 시간의 관계를 알아야 한다. "
    "속도는 위치의 시간에 대한 변화율이며, 가속도는 속도의 변화율이다."
)


def only(task: str) -> SftConfig:
    return SftConfig(tasks=[task])


def paragraphs(count: int, length: int = 2):
    return [para(f"{i}번 문단입니다. {PROSE * length}") for i in range(count)]


# ------------------------------------------------------------ title synthesis


def test_a_section_body_becomes_a_title_prompt():
    doc = document(heading("제2절 운동의 법칙"), *paragraphs(3))
    samples = build_sft_samples(doc, only("summarize_title"))
    assert len(samples) == 1
    assert samples[0].output == "제2절 운동의 법칙"
    assert "0번 문단입니다." in samples[0].input


def test_a_very_long_section_is_truncated_rather_than_skipped():
    doc = document(heading("제2절 운동의 법칙"), *paragraphs(60))
    samples = build_sft_samples(doc, only("summarize_title"))
    assert len(samples) == 1
    assert len(samples[0].input) <= 6000


def test_a_section_with_too_little_body_is_skipped():
    doc = document(heading("제2절 운동의 법칙"), para("짧은 한 줄."))
    assert build_sft_samples(doc, only("summarize_title")) == []


def test_a_one_word_heading_is_not_worth_predicting():
    doc = document(heading("표"), *paragraphs(3))
    assert build_sft_samples(doc, only("summarize_title")) == []


# ----------------------------------------------------- continuation synthesis


def test_a_section_is_split_into_prompt_and_continuation():
    doc = document(heading("제1장 서론"), *paragraphs(4))
    samples = build_sft_samples(doc, only("continuation"))
    assert len(samples) == 1
    assert "0번 문단입니다." in samples[0].input
    assert "2번 문단입니다." in samples[0].output
    assert "2번 문단입니다." not in samples[0].input
    assert samples[0].input.startswith("[제1장 서론]\n")


def test_a_section_with_too_few_paragraphs_yields_no_continuation():
    doc = document(heading("제1장 서론"), *paragraphs(3))
    assert build_sft_samples(doc, only("continuation")) == []


# ------------------------------------------------------------ table synthesis


def table_block():
    cells = [
        {"text": t, "row": r, "col": c, "row_span": 1, "col_span": 1, "is_header": r == 0}
        for r, row in enumerate([["항목", "값"], ["중력가속도", "9.8"], ["광속", "3.0e8"]])
        for c, t in enumerate(row)
    ]
    latex = "\\begin{tabular}{|c|c|}\n\\hline\n항목 & 값 \\\\\n\\hline\n\\end{tabular}"
    return table(latex, page=7, cells=cells, num_rows=3, num_cols=2, caption="표 1. 물리 상수")


def test_a_table_becomes_a_plain_text_to_latex_pair():
    samples = build_sft_samples(document(table_block()), only("table_to_latex"))
    assert len(samples) == 1
    assert samples[0].output.startswith(r"\begin{tabular}")
    assert "항목 | 값" in samples[0].input
    assert samples[0].input.startswith("표 제목: 표 1. 물리 상수\n")
    assert samples[0].pages == [7]


def test_a_table_without_recognized_cells_is_skipped():
    doc = document(table("\\begin{tabular}{|c|}\\end{tabular}"))
    assert build_sft_samples(doc, only("table_to_latex")) == []


# --------------------------------------------------------- equation synthesis


def test_an_equation_is_paired_with_the_sentence_that_introduces_it():
    doc = document(
        para("질량과 에너지의 관계는 다음과 같이 주어진다."),
        equation("E = mc^{2}", page=5),
    )
    samples = build_sft_samples(doc, only("equation_to_latex"))
    assert len(samples) == 1
    assert samples[0].input == "질량과 에너지의 관계는 다음과 같이 주어진다."
    assert samples[0].output == "$$\nE = mc^{2}\n$$"
    assert samples[0].pages == [5]


def test_an_equation_without_context_is_skipped():
    assert build_sft_samples(document(equation("E = mc^{2}")), only("equation_to_latex")) == []


def test_a_heading_can_serve_as_equation_context():
    doc = document(heading("아인슈타인의 질량-에너지 등가원리"), equation("E = mc^{2}"))
    samples = build_sft_samples(doc, only("equation_to_latex"))
    assert samples[0].input == "아인슈타인의 질량-에너지 등가원리"


# ------------------------------------------------------- definition synthesis


def test_a_definition_sentence_becomes_a_question():
    text = (
        "가속도란 단위 시간당 속도의 변화량을 나타내는 물리량이다. "
        "국제단위계에서는 초당 미터매초로 나타낸다. 방향을 가지는 벡터량이다."
    )
    samples = build_sft_samples(document(para(text)), only("qa_definition"))
    assert len(samples) == 1
    assert "가속도" in samples[0].instruction
    assert samples[0].output.startswith("가속도란 단위 시간당")


def test_the_same_term_is_only_asked_about_once():
    text = (
        "가속도란 단위 시간당 속도의 변화량을 나타내는 물리량이다. "
        "국제단위계에서는 초당 미터매초로 나타낸다. 방향을 가지는 벡터량이다."
    )
    doc = document(para(text), para(text))
    assert len(build_sft_samples(doc, only("qa_definition"))) == 1


def test_a_narrative_paragraph_yields_no_definition():
    doc = document(para("그는 아침 일찍 일어나 창문을 열고 바깥 풍경을 바라보았다. 날씨가 맑았다."))
    assert build_sft_samples(doc, only("qa_definition")) == []


# ----------------------------------------------------------------- the driver


def test_generation_is_reproducible_for_a_given_seed():
    doc = document(heading("제1장 서론"), *paragraphs(4), table_block())
    cfg = SftConfig()
    first = build_sft_samples(doc, cfg)
    second = build_sft_samples(doc, cfg)
    assert [(s.task, s.instruction, s.output) for s in first] == [
        (s.task, s.instruction, s.output) for s in second
    ]


def test_a_different_seed_reshuffles_the_prompts():
    doc = document(heading("제1장 서론"), *paragraphs(4))
    a = build_sft_samples(doc, SftConfig(seed=1))
    b = build_sft_samples(doc, SftConfig(seed=2))
    assert {s.output for s in a} == {s.output for s in b}


def test_the_per_document_cap_is_honoured():
    blocks = []
    for i in range(30):
        blocks.append(heading(f"제{i}절 운동의 법칙"))
        blocks.extend(paragraphs(4))
    samples = build_sft_samples(document(*blocks), SftConfig(max_samples_per_doc=5))
    assert len(samples) == 5


def test_synthesis_can_be_switched_off():
    doc = document(heading("제1장 서론"), *paragraphs(4))
    assert build_sft_samples(doc, SftConfig(enabled=False)) == []


def test_messages_carry_the_system_prompt_and_merge_the_input():
    doc = document(heading("제2절 운동의 법칙"), *paragraphs(3))
    sample = build_sft_samples(doc, only("summarize_title"))[0]
    messages = sample.messages("시스템 지침")
    assert [m["role"] for m in messages] == ["system", "user", "assistant"]
    assert messages[1]["content"].startswith(sample.instruction)
    assert sample.input in messages[1]["content"]
    assert messages[2]["content"] == sample.output


def test_messages_omit_the_system_turn_when_no_prompt_is_configured():
    doc = document(heading("제2절 운동의 법칙"), *paragraphs(3))
    sample = build_sft_samples(doc, only("summarize_title"))[0]
    assert [m["role"] for m in sample.messages()] == ["user", "assistant"]


@pytest.mark.parametrize(
    "task",
    ["summarize_title", "continuation", "table_to_latex", "equation_to_latex", "qa_definition"],
)
def test_every_answer_is_text_that_exists_in_the_document(task):
    doc = document(
        heading("제1장 서론"),
        *paragraphs(4),
        para("가속도란 단위 시간당 속도의 변화량을 나타내는 물리량이다. 벡터량이다."),
        para("질량과 에너지의 관계는 다음과 같다."),
        equation("E = mc^{2}"),
        table_block(),
    )
    markdown = doc.to_markdown()
    for sample in build_sft_samples(doc, only(task)):
        # no teacher model is involved, so every answer must be verbatim source
        assert sample.output.strip("$\n") in markdown
