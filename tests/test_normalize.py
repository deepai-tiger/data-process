"""Text normalization and page-structure repair."""

from __future__ import annotations

import pytest

from kdp.clean.normalize import (
    infer_structure,
    normalize_document,
    normalize_text,
    sanitize_title,
)
from kdp.config import NormalizeConfig
from kdp.schema import Block, BlockKind

from factories import document, heading, para


@pytest.fixture
def cfg() -> NormalizeConfig:
    return NormalizeConfig()


def test_control_and_zero_width_characters_are_removed(cfg):
    assert normalize_text("한\u200b국\ufeff어\x07", cfg) == "한국어"


def test_private_use_and_replacement_characters_are_removed(cfg):
    # broken legacy code pages leave these behind in .doc conversions
    assert normalize_text("본문\ue000\ufffd 끝", cfg) == "본문 끝"


def test_unicode_is_composed_to_nfc(cfg):
    decomposed = "\u1112\u1161\u11ab"  # ㅎ + ㅏ + ㄴ
    assert normalize_text(decomposed, cfg) == "한"


def test_typographic_punctuation_is_folded(cfg):
    assert normalize_text("\u201c인용\u201d \u2013 끝\u2026", cfg) == '"인용" - 끝...'


def test_full_width_punctuation_becomes_ascii(cfg):
    assert normalize_text("가\uff0c나\uff0e", cfg) == "가,나."


def test_dot_leaders_collapse(cfg):
    assert "..." in normalize_text("제1장 서론 ............ 3", cfg)
    assert "........" not in normalize_text("제1장 서론 ............ 3", cfg)


def test_wrapped_lines_are_joined_into_one_paragraph(cfg):
    assert normalize_text("첫 줄\n둘째 줄", cfg) == "첫 줄 둘째 줄"


def test_hyphenated_latin_word_is_rejoined(cfg):
    assert normalize_text("recog-\nnition", cfg) == "recognition"


def test_korean_hyphen_line_break_is_not_rejoined(cfg):
    # only Latin words hyphenate across lines; a Korean dash is meaningful
    assert normalize_text("가-\n나", cfg) == "가- 나"


def test_code_blocks_keep_their_line_breaks(cfg):
    assert normalize_text("int a;\nint b;", cfg, keep_newlines=True) == "int a;\nint b;"


def test_space_before_punctuation_is_removed(cfg):
    assert normalize_text("문장 입니다 . 다음 ( 괄호 )", cfg) == "문장 입니다. 다음 (괄호)"


def test_page_numbers_become_artifacts(cfg):
    doc = document(para("본문입니다.", page=1), para("- 12 -", page=1))
    doc, report = normalize_document(doc, cfg)
    assert report.page_artifacts == 1
    assert doc.blocks[1].kind is BlockKind.PAGE_ARTIFACT
    # artifacts stay in the document for traceability but never render
    assert "- 12 -" not in doc.to_markdown()


def test_running_header_repeated_across_pages_is_dropped(cfg):
    blocks = []
    for page in range(1, 5):
        blocks.append(para("한국 물리 교과서", page=page))
        blocks.append(para(f"{page}쪽의 실제 본문 내용이 여기에 이어집니다.", page=page))
    doc, report = normalize_document(document(*blocks), cfg)
    assert report.page_artifacts >= 4
    assert "한국 물리 교과서" not in doc.to_markdown()


def test_a_heading_that_appears_once_survives(cfg):
    blocks = [para("고유한 제목", page=1)]
    for page in range(1, 5):
        blocks.append(para(f"{page}쪽 본문 내용이 충분히 길게 이어지는 문단입니다.", page=page))
    doc, _ = normalize_document(document(*blocks), cfg)
    assert "고유한 제목" in doc.to_markdown()


def test_paragraph_split_by_a_page_break_is_stitched(cfg):
    doc = document(
        para("이 문장은 페이지 끝에서 잘렸고", page=1),
        para("다음 쪽에서 이어집니다.", page=2),
    )
    doc, report = normalize_document(doc, cfg)
    assert report.merged_paragraphs == 1
    assert doc.blocks[0].text == "이 문장은 페이지 끝에서 잘렸고 다음 쪽에서 이어집니다."
    assert doc.blocks[0].meta["merged_pages"] == [1, 2]


def test_a_finished_sentence_is_not_merged_with_the_next_page(cfg):
    doc = document(para("문장이 끝났습니다.", page=1), para("새 문단입니다.", page=2))
    doc, report = normalize_document(doc, cfg)
    assert report.merged_paragraphs == 0


def test_consecutive_duplicate_short_lines_are_dropped(cfg):
    doc = document(para("표 1", page=1), para("표 1", page=1), para("본문", page=1))
    doc, report = normalize_document(doc, cfg)
    assert report.repeated_lines_removed == 1


def test_latex_payloads_are_not_rewrapped(cfg):
    latex = "\\begin{tabular}{|c|}\n\\hline\n가 \\\\\n\\hline\n\\end{tabular}"
    block = Block(kind=BlockKind.TABLE, latex=latex, text=latex, page=1)
    doc, _ = normalize_document(document(block), cfg)
    assert doc.blocks[0].latex == latex


def test_noisy_table_caption_is_stripped_from_latex(cfg):
    caption = "아 아 애 아 애 아 아 애"
    latex = f"\\begin{{table}}[htbp]\n\\caption{{{caption}}}\n\\begin{{tabular}}{{|c|}}\n\\end{{table}}"
    block = Block(
        kind=BlockKind.TABLE, latex=latex, text=latex, page=1, meta={"caption": caption}
    )
    doc, _ = normalize_document(document(block), cfg)
    assert doc.blocks[0].meta["caption"] is None
    assert doc.blocks[0].meta["caption_rejected"] == caption
    assert "\\caption" not in doc.blocks[0].latex


def test_a_good_caption_is_kept(cfg):
    caption = "표 2. 주요 물리 상수의 값"
    latex = f"\\begin{{table}}[htbp]\n\\caption{{{caption}}}\n\\end{{table}}"
    block = Block(
        kind=BlockKind.TABLE, latex=latex, text=latex, page=1, meta={"caption": caption}
    )
    doc, _ = normalize_document(document(block), cfg)
    assert doc.blocks[0].meta["caption"] == caption


@pytest.mark.parametrize(
    "text,level",
    [
        ("제 1 장 서론", 1),
        ("제2절 운동의 법칙", 2),
        ("제 3 조 적용 범위", 3),
        ("1.2 단위와 차원", 3),
        ("1.2.3 유효숫자", 4),
        ("ㄱ. 첫째 조건", 3),
    ],
)
def test_heading_shapes_are_recovered_from_plain_paragraphs(cfg, text, level):
    doc = infer_structure(document(para(text)), cfg)
    assert doc.blocks[0].kind is BlockKind.HEADING
    assert doc.blocks[0].level == level
    assert doc.blocks[0].meta["heading_source"] == "inferred"


def test_a_numbered_sentence_is_not_mistaken_for_a_heading(cfg):
    doc = infer_structure(document(para("1. 이것은 번호가 붙은 완결된 문장입니다.")), cfg)
    assert doc.blocks[0].kind is BlockKind.PARAGRAPH


def test_a_long_line_is_not_mistaken_for_a_heading(cfg):
    long_line = "제1장 " + "아주 긴 제목처럼 보이지만 사실은 문단입니다 " * 3
    doc = infer_structure(document(para(long_line)), cfg)
    assert doc.blocks[0].kind is BlockKind.PARAGRAPH


def test_heading_inference_can_be_switched_off():
    cfg = NormalizeConfig(infer_headings=False)
    doc = infer_structure(document(para("제 1 장 서론")), cfg)
    assert doc.blocks[0].kind is BlockKind.PARAGRAPH


def test_mojibake_title_from_a_legacy_doc_is_rejected():
    doc = document(heading("제1장 건강"), doc_id="13")
    doc.title = "犬掘顧莫" * 3
    sanitize_title(doc)
    assert doc.title == "제1장 건강"
    assert doc.meta["title_rejected"].startswith("犬")


def test_a_korean_title_is_kept():
    doc = document(heading("제1장 건강"))
    doc.title = "1분간 건강단련법"
    sanitize_title(doc)
    assert doc.title == "1분간 건강단련법"


def test_a_missing_title_falls_back_to_the_first_heading():
    doc = document(para("머리말"), heading("제1장 서론"))
    sanitize_title(doc)
    assert doc.title == "제1장 서론"
