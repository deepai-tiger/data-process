"""The intermediate document representation and its Markdown rendering."""

from __future__ import annotations

import json

from kdp.schema import Block, BlockKind, Document, render_block, slugify

from factories import document, equation, heading, para, table


def test_a_paragraph_renders_as_plain_text():
    assert render_block(para("본문입니다.")) == "본문입니다."


def test_headings_render_at_their_level():
    assert render_block(heading("서론", level=1)) == "# 서론"
    assert render_block(heading("배경", level=3)) == "### 배경"


def test_heading_levels_are_clamped_to_markdown_range():
    assert render_block(heading("깊은 절", level=9)).startswith("###### ")


def test_a_display_equation_renders_as_block_math():
    assert render_block(equation("E = mc^{2}")) == "$$\nE = mc^{2}\n$$"


def test_an_inline_equation_renders_inline():
    block = equation("x^{2}", inline=True)
    assert render_block(block) == "$x^{2}$"


def test_a_table_renders_as_its_latex():
    latex = "\\begin{tabular}{|c|}\n가 \\\\\n\\end{tabular}"
    assert render_block(table(latex)) == latex


def test_a_list_item_gets_a_bullet():
    assert render_block(Block(kind=BlockKind.LIST_ITEM, text="첫째")) == "- 첫째"


def test_code_keeps_its_language_fence():
    block = Block(kind=BlockKind.CODE, text="int a = 1;", meta={"language": "cpp"})
    assert render_block(block) == "```cpp\nint a = 1;\n```"


def test_a_footnote_is_labelled():
    assert render_block(Block(kind=BlockKind.FOOTNOTE, text="출처")) == "[각주] 출처"


def test_page_artifacts_are_excluded_from_markdown():
    artifact = Block(kind=BlockKind.PAGE_ARTIFACT, text="- 12 -")
    doc = document(para("본문입니다."), artifact)
    assert "- 12 -" not in doc.to_markdown()
    assert "- 12 -" in doc.to_markdown(include_artifacts=True)


def test_blocks_are_separated_by_a_blank_line():
    doc = document(heading("서론", level=1), para("본문입니다."))
    assert doc.to_markdown() == "# 서론\n\n본문입니다.\n"


def test_the_latex_payload_is_what_counts_towards_length():
    block = table("\\begin{tabular}{|c|}\\end{tabular}")
    assert block.payload == block.latex
    assert block.char_count == len(block.latex)


def test_page_artifacts_do_not_count_towards_document_length():
    artifact = Block(kind=BlockKind.PAGE_ARTIFACT, text="- 12 -")
    assert document(para("본문"), artifact).char_count() == 2


def test_block_counts_are_grouped_by_kind():
    doc = document(heading("서론"), para("가"), para("나"))
    assert doc.counts() == {"heading": 1, "paragraph": 2}


def test_pages_are_iterated_in_reading_order():
    doc = document(para("가", page=1), para("나", page=1), para("다", page=2))
    assert [(page, len(blocks)) for page, blocks in doc.iter_pages()] == [(1, 2), (2, 1)]


def test_a_document_round_trips_through_json(tmp_path):
    original = document(
        heading("제1장", level=1),
        para("본문입니다.", page=2),
        equation("E = mc^{2}", page=2),
        table("\\begin{tabular}{|c|}\\end{tabular}", page=3, cells=[{"text": "가"}]),
    )
    original.title = "테스트 문서"
    original.n_pages = 3
    original.warn("12 picture region(s) skipped by design")
    original.meta["extractor"] = "pdf_image_layout"

    path = original.save(tmp_path / "doc.json")
    restored = Document.load(path)

    assert restored.to_dict() == original.to_dict()
    assert restored.title == "테스트 문서"
    assert restored.warnings == ["12 picture region(s) skipped by design"]
    assert restored.blocks[3].meta["cells"] == [{"text": "가"}]


def test_korean_is_stored_unescaped_on_disk(tmp_path):
    path = document(para("한국어")).save(tmp_path / "doc.json")
    assert "한국어" in path.read_text(encoding="utf-8")
    assert json.loads(path.read_text(encoding="utf-8"))["blocks"][0]["text"] == "한국어"


def test_optional_block_fields_are_omitted_from_the_json():
    assert set(para("본문").to_dict()) == {"kind", "text"}


def test_warnings_are_not_duplicated():
    doc = document()
    doc.warn("같은 경고")
    doc.warn("같은 경고")
    assert doc.warnings == ["같은 경고"]


def test_slugify_keeps_hangul_and_lowercases_latin():
    assert slugify("제1장 서론.PDF") == "제1장-서론.pdf"


def test_slugify_falls_back_for_an_unusable_name():
    assert slugify("///") == "doc"
