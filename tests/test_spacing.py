"""Korean word-spacing repair for OCR text.

Kiwi's statistical model is replaced by a spacer that simply closes up every
space, which is enough to tell what gets handed to it and what does not.
"""

from __future__ import annotations

import pytest

from kdp.clean.spacing import (
    build_spacer,
    fix_spacing,
    needs_spacing_fix,
    respace_document,
)
from kdp.schema import BlockKind

from factories import document, equation, para, table


class GlueSpacer:
    """Closes up every space, so any text it touched is obvious."""

    name = "glue"

    def __init__(self) -> None:
        self.seen: list[str] = []

    def fix(self, text: str) -> str:
        self.seen.append(text)
        return text.replace(" ", "")


@pytest.fixture
def spacer(monkeypatch):
    glue = GlueSpacer()
    monkeypatch.setattr("kdp.clean.spacing.build_spacer", lambda engine: glue)
    return glue


# ------------------------------------------------------------- detection


@pytest.mark.parametrize(
    "text",
    [
        "널 리 리 용 한다",
        "체 육 을 전 문 으로 하는 사람",
    ],
)
def test_syllable_by_syllable_ocr_output_is_detected(text):
    assert needs_spacing_fix(text)


@pytest.mark.parametrize(
    "text",
    [
        "널리 리용한다",
        "이 책은 건강단련법을 다룬다",
        "A B C D E",
        "",
    ],
)
def test_normally_spaced_text_is_left_alone(text):
    assert not needs_spacing_fix(text)


# --------------------------------------------------------------- math spans


def test_inline_math_survives_respacing_byte_for_byte():
    fixed = fix_spacing("속 도 는 $v = x / t$ 로 주 어 진다", GlueSpacer())
    assert "$v = x / t$" in fixed


def test_text_on_both_sides_of_the_math_is_respaced():
    # each side is respaced on its own, so the spacer also decides whether a
    # space survives next to the formula
    fixed = fix_spacing("여 기 서 $a$ 는 가 속 도 이다", GlueSpacer())
    assert fixed == "여기서$a$는가속도이다"


def test_an_unknown_engine_is_rejected():
    with pytest.raises(ValueError, match="unknown spacing engine"):
        build_spacer("magic")


def test_switching_the_engine_off_changes_nothing():
    doc = document(para("널 리 리 용 한다"))
    doc, report = respace_document(doc, engine="none")
    assert doc.blocks[0].text == "널 리 리 용 한다"
    assert report.blocks_changed == 0


# -------------------------------------------------------------- documents


def test_ocr_paragraphs_are_respaced(spacer):
    doc = document(para("널 리 리 용 한다"))
    doc, report = respace_document(doc, engine="glue")
    assert doc.blocks[0].text == "널리리용한다"
    assert doc.blocks[0].meta["respaced"] is True
    assert report.blocks_changed == 1


def test_word_documents_are_not_touched(spacer):
    doc = document(para("널 리 리 용 한다"), source_type="docx")
    doc, report = respace_document(doc, engine="glue")
    assert doc.blocks[0].text == "널 리 리 용 한다"
    assert report.engine == "skipped(non-ocr source)"
    assert spacer.seen == []


def test_equations_are_never_handed_to_the_spacer(spacer):
    doc = document(equation("a = b + c"), para("이 는 다 음 과 같다"))
    respace_document(doc, engine="glue")
    assert "a = b + c" not in spacer.seen


# ----------------------------------------------------------------- tables


def cells(*texts: str) -> list[dict]:
    return [
        {
            "text": text,
            "row": index // 2,
            "col": index % 2,
            "row_span": 1,
            "col_span": 1,
            "is_header": index < 2,
        }
        for index, text in enumerate(texts)
    ]


def test_table_cells_are_respaced_and_the_latex_rebuilt(spacer):
    block = table(
        "stale latex",
        cells=cells("항목", "값", "중 력 가 속도", "9.8"),
        num_rows=2,
        num_cols=2,
        caption="표 1. 물리 상수",
    )
    doc = document(block)
    respace_document(doc, engine="glue")

    assert block.meta["cells"][2]["text"] == "중력가속도"
    assert "중력가속도" in block.latex
    assert block.text == block.latex


def test_a_broken_caption_is_repaired_even_when_the_cells_are_clean(spacer):
    block = table(
        "stale latex",
        cells=cells("항목", "값", "중력가속도", "9.8"),
        num_rows=2,
        num_cols=2,
        caption="표 1. 물 리 상 수",
    )
    doc = document(block)
    respace_document(doc, engine="glue")

    assert block.meta["caption"] == "표1.물리상수"
    assert "표1.물리상수" in block.latex


def test_a_table_that_needs_nothing_keeps_its_latex(spacer):
    block = table(
        "\\begin{tabular}{|c|c|}\\end{tabular}",
        cells=cells("항목", "값", "중력가속도", "9.8"),
        num_rows=2,
        num_cols=2,
    )
    doc = document(block)
    _, report = respace_document(doc, engine="glue")

    assert block.latex == "\\begin{tabular}{|c|c|}\\end{tabular}"
    assert report.blocks_changed == 0


def test_the_report_lands_in_the_document_metadata(spacer):
    doc = document(para("널 리 리 용 한다"))
    doc, _ = respace_document(doc, engine="glue")
    assert doc.meta["spacing"]["engine"] == "glue"
    assert doc.meta["spacing"]["blocks_changed"] == 1


def test_headings_are_respaced_too(spacer):
    from factories import heading

    doc = document(heading("건 강 단 련 법 27"))
    doc, _ = respace_document(doc, engine="glue")
    assert doc.blocks[0].kind is BlockKind.HEADING
    assert doc.blocks[0].text == "건강단련법27"
