"""Structure-preserving .docx extraction, driven by hand-built OOXML."""

from __future__ import annotations

import zipfile

import pytest

from kdp.config import Config
from kdp.extract.docx_ooxml import extract_docx
from kdp.extract.omml import M_NS, W_NS
from kdp.schema import BlockKind

NSDECL = f'xmlns:w="{W_NS}" xmlns:m="{M_NS}"'

DEFAULT_STYLES = f"""<w:styles {NSDECL}>
  <w:style w:styleId="Heading1"><w:name w:val="heading 1"/></w:style>
  <w:style w:styleId="Heading2"><w:name w:val="heading 2"/></w:style>
  <w:style w:styleId="Title"><w:name w:val="Title"/></w:style>
  <w:style w:styleId="Caption"><w:name w:val="caption"/></w:style>
  <w:style w:styleId="TOC1"><w:name w:val="toc 1"/></w:style>
  <w:style w:styleId="Header"><w:name w:val="header"/></w:style>
  <w:style w:styleId="Outlined"><w:name w:val="본문개요"/>
    <w:pPr><w:outlineLvl w:val="2"/></w:pPr></w:style>
</w:styles>"""


def build_docx(tmp_path, body: str, styles: str = DEFAULT_STYLES, core: str | None = None, name="t.docx"):
    path = tmp_path / name
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", f"<w:document {NSDECL}><w:body>{body}</w:body></w:document>")
        zf.writestr("word/styles.xml", styles)
        if core is not None:
            zf.writestr("docProps/core.xml", core)
    return path


def p(text: str, style: str | None = None, extra: str = "") -> str:
    ppr = f"<w:pPr><w:pStyle w:val='{style}'/></w:pPr>" if style else ""
    run = f"<w:r><w:t>{text}</w:t></w:r>" if text else ""
    return f"<w:p>{ppr}{run}{extra}</w:p>"


def extract(tmp_path, body: str, **kwargs):
    return extract_docx(build_docx(tmp_path, body, **kwargs))


# ------------------------------------------------------------------ structure


def test_paragraphs_and_headings_keep_their_roles(tmp_path):
    doc = extract(tmp_path, p("제1장 서론", "Heading1") + p("본문입니다.") + p("1.1 배경", "Heading2"))
    assert [(b.kind, b.level) for b in doc.blocks] == [
        (BlockKind.HEADING, 1),
        (BlockKind.PARAGRAPH, None),
        (BlockKind.HEADING, 2),
    ]


def test_a_style_with_an_outline_level_is_a_heading(tmp_path):
    doc = extract(tmp_path, p("사용자 정의 제목", "Outlined"))
    assert doc.blocks[0].kind is BlockKind.HEADING
    assert doc.blocks[0].level == 3


def test_the_title_style_becomes_the_document_title(tmp_path):
    doc = extract(tmp_path, p("한국어 문서", "Title") + p("본문입니다."))
    assert doc.blocks[0].kind is BlockKind.TITLE
    assert doc.title == "한국어 문서"


def test_core_properties_win_over_the_title_style(tmp_path):
    core = (
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"'
        ' xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>메타데이터 제목</dc:title></cp:coreProperties>'
    )
    doc = extract(tmp_path, p("본문 제목", "Title"), core=core)
    assert doc.title == "메타데이터 제목"


def test_captions_are_recognized(tmp_path):
    doc = extract(tmp_path, p("표 1. 물리 상수", "Caption"))
    assert doc.blocks[0].kind is BlockKind.CAPTION


def test_list_paragraphs_carry_their_indent_level(tmp_path):
    body = (
        "<w:p><w:pPr><w:numPr><w:ilvl w:val='0'/></w:numPr></w:pPr><w:r><w:t>첫째</w:t></w:r></w:p>"
        "<w:p><w:pPr><w:numPr><w:ilvl w:val='1'/></w:numPr></w:pPr><w:r><w:t>둘째</w:t></w:r></w:p>"
    )
    doc = extract(tmp_path, body)
    assert [(b.kind, b.level) for b in doc.blocks] == [
        (BlockKind.LIST_ITEM, 1),
        (BlockKind.LIST_ITEM, 2),
    ]


def test_empty_paragraphs_are_skipped(tmp_path):
    assert extract(tmp_path, "<w:p/>" + p("본문입니다.") + "<w:p/>").counts() == {"paragraph": 1}


def test_content_inside_a_structured_document_tag_is_not_lost(tmp_path):
    body = f"<w:sdt><w:sdtContent>{p('본문입니다.')}</w:sdtContent></w:sdt>"
    assert extract(tmp_path, body).counts() == {"paragraph": 1}


# ------------------------------------------------------------ page artifacts


@pytest.mark.parametrize("style", ["TOC1", "Header"])
def test_table_of_contents_and_running_headers_are_marked_as_artifacts(tmp_path, style):
    doc = extract(tmp_path, p("제1장 서론\t3", style) + p("본문입니다."))
    assert doc.blocks[0].kind is BlockKind.PAGE_ARTIFACT
    assert "제1장 서론" not in doc.to_markdown()


# -------------------------------------------------------------------- inline


def test_line_breaks_and_tabs_survive_as_whitespace(tmp_path):
    body = "<w:p><w:r><w:t>왼쪽</w:t><w:tab/><w:t>오른쪽</w:t><w:br/><w:t>다음 줄</w:t></w:r></w:p>"
    assert extract(tmp_path, body).blocks[0].text == "왼쪽 오른쪽\n다음 줄"


def test_hyperlink_text_is_kept(tmp_path):
    body = "<w:p><w:hyperlink><w:r><w:t>링크 텍스트</w:t></w:r></w:hyperlink></w:p>"
    assert extract(tmp_path, body).blocks[0].text == "링크 텍스트"


def test_deleted_revision_text_is_discarded(tmp_path):
    body = (
        "<w:p><w:r><w:t>남는 문장.</w:t></w:r>"
        "<w:del><w:r><w:delText>지운 문장.</w:delText></w:r></w:del></w:p>"
    )
    assert extract(tmp_path, body).blocks[0].text == "남는 문장."


def test_inserted_revision_text_is_kept(tmp_path):
    body = "<w:p><w:ins><w:r><w:t>추가된 문장.</w:t></w:r></w:ins></w:p>"
    assert extract(tmp_path, body).blocks[0].text == "추가된 문장."


def test_images_are_skipped_but_counted(tmp_path):
    body = "<w:p><w:r><w:drawing/><w:t>그림 옆의 설명입니다.</w:t></w:r></w:p>"
    doc = extract(tmp_path, body)
    assert doc.blocks[0].text == "그림 옆의 설명입니다."
    assert doc.meta["images_skipped"] == 1


def test_legacy_equation_objects_are_reported_rather_than_silently_lost(tmp_path):
    body = "<w:p><w:r><w:object/><w:t>수식 설명입니다.</w:t></w:r></w:p>"
    doc = extract(tmp_path, body)
    assert doc.meta["ole_objects"] == 1
    assert any("OLE object" in w for w in doc.warnings)


def test_symbol_font_glyphs_are_dropped(tmp_path):
    body = "<w:p><w:r><w:sym w:font='Wingdings' w:char='F06C'/><w:t>본문</w:t></w:r></w:p>"
    assert extract(tmp_path, body).blocks[0].text == "본문"


# ----------------------------------------------------------------- equations


def omath(text: str) -> str:
    return f"<m:oMath><m:r><m:t>{text}</m:t></m:r></m:oMath>"


def test_an_inline_equation_is_embedded_in_the_sentence(tmp_path):
    body = f"<w:p><w:r><w:t>식은 </w:t></w:r>{omath('x+y')}<w:r><w:t> 이다.</w:t></w:r></w:p>"
    doc = extract(tmp_path, body)
    assert doc.blocks[0].text == "식은 $x+y$ 이다."
    assert doc.meta["inline_equations"] == 1


def test_a_paragraph_holding_only_a_formula_becomes_a_display_equation(tmp_path):
    doc = extract(tmp_path, f"<w:p>{omath('E=mc^2')}</w:p>")
    assert doc.blocks[0].kind is BlockKind.EQUATION
    assert doc.blocks[0].latex == "E=mc^2"
    assert doc.meta["display_equations"] == 1
    assert doc.meta["inline_equations"] == 0


def test_an_omath_para_is_a_display_equation(tmp_path):
    body = f"<w:p><m:oMathPara>{omath('a=b')}</m:oMathPara></w:p>"
    doc = extract(tmp_path, body)
    assert [b.kind for b in doc.blocks] == [BlockKind.EQUATION]
    assert doc.blocks[0].latex == "a=b"


def test_a_fraction_becomes_latex(tmp_path):
    frac = (
        "<m:oMath><m:f><m:num><m:r><m:t>a</m:t></m:r></m:num>"
        "<m:den><m:r><m:t>b</m:t></m:r></m:den></m:f></m:oMath>"
    )
    doc = extract(tmp_path, f"<w:p>{frac}</w:p>")
    assert doc.blocks[0].latex == r"\frac{a}{b}"


# -------------------------------------------------------------------- tables


def tc(text: str, props: str = "") -> str:
    return f"<w:tc><w:tcPr>{props}</w:tcPr><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:tc>"


def test_a_table_becomes_latex_with_its_cells_preserved(tmp_path):
    body = (
        "<w:tbl>"
        f"<w:tr>{tc('항목')}{tc('값')}</w:tr>"
        f"<w:tr>{tc('중력가속도')}{tc('9.8')}</w:tr>"
        "</w:tbl>"
    )
    doc = extract(tmp_path, body)
    block = doc.blocks[0]
    assert block.kind is BlockKind.TABLE
    assert r"\begin{tabular}" in block.latex
    assert r"중력가속도 & 9.8 \\" in block.latex
    assert block.meta["num_rows"] == 2
    assert block.meta["num_cols"] == 2
    assert doc.meta["tables"] == 1
    # the plain-text grid is kept so the SFT stage can pose the inverse task
    assert [c["text"] for c in block.meta["cells"]] == ["항목", "값", "중력가속도", "9.8"]


def test_the_first_row_is_treated_as_a_header(tmp_path):
    body = f"<w:tbl><w:tr>{tc('항목')}{tc('값')}</w:tr><w:tr>{tc('가')}{tc('1')}</w:tr></w:tbl>"
    assert r"\textbf{항목}" in extract(tmp_path, body).blocks[0].latex


def test_horizontal_merges_become_multicolumn(tmp_path):
    body = (
        "<w:tbl>"
        f"<w:tr>{tc('머리글', '<w:gridSpan w:val=\"2\"/>')}</w:tr>"
        f"<w:tr>{tc('가')}{tc('나')}</w:tr>"
        "</w:tbl>"
    )
    assert r"\multicolumn{2}" in extract(tmp_path, body).blocks[0].latex


def test_vertical_merges_become_multirow(tmp_path):
    body = (
        "<w:tbl>"
        f"<w:tr>{tc('구분')}{tc('값')}</w:tr>"
        f"<w:tr>{tc('왼쪽', '<w:vMerge w:val=\"restart\"/>')}{tc('가')}</w:tr>"
        f"<w:tr>{tc('', '<w:vMerge/>')}{tc('나')}</w:tr>"
        "</w:tbl>"
    )
    latex = extract(tmp_path, body).blocks[0].latex
    assert r"\multirow{2}{*}{왼쪽}" in latex
    assert latex.count("왼쪽") == 1


def test_an_entirely_empty_table_is_dropped(tmp_path):
    body = f"<w:tbl><w:tr>{tc('')}{tc('')}</w:tr></w:tbl>"
    assert extract(tmp_path, body).blocks == []


def test_an_equation_inside_a_cell_is_kept_as_latex(tmp_path):
    cell = f"<w:tc><w:tcPr/><w:p>{omath('x^2')}</w:p></w:tc>"
    body = f"<w:tbl><w:tr>{tc('제곱')}{cell}</w:tr><w:tr>{tc('가')}{tc('나')}</w:tr></w:tbl>"
    assert "$x^2$" in extract(tmp_path, body).blocks[0].meta["cells"][1]["text"]


# ----------------------------------------------------------------- footnotes


def test_footnotes_are_appended_once_and_only_when_referenced(tmp_path):
    footnotes = (
        f"<w:footnotes {NSDECL}>"
        '<w:footnote w:id="0" w:type="separator"><w:p><w:r><w:t>---</w:t></w:r></w:p></w:footnote>'
        '<w:footnote w:id="2"><w:p><w:r><w:t>출처: 물리학 교과서</w:t></w:r></w:p></w:footnote>'
        '<w:footnote w:id="3"><w:p><w:r><w:t>참조되지 않는 각주</w:t></w:r></w:p></w:footnote>'
        "</w:footnotes>"
    )
    path = tmp_path / "f.docx"
    body = '<w:p><w:r><w:t>본문입니다.</w:t><w:footnoteReference w:id="2"/></w:r></w:p>'
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/document.xml", f"<w:document {NSDECL}><w:body>{body}</w:body></w:document>")
        zf.writestr("word/styles.xml", DEFAULT_STYLES)
        zf.writestr("word/footnotes.xml", footnotes)

    doc = extract_docx(path)
    notes = [b for b in doc.blocks if b.kind is BlockKind.FOOTNOTE]
    assert [b.text for b in notes] == ["출처: 물리학 교과서"]

    without = extract_docx(path, Config.model_validate({"word": {"include_footnotes": False}}))
    assert not [b for b in without.blocks if b.kind is BlockKind.FOOTNOTE]


# ------------------------------------------------------------------- failure


def test_a_file_that_is_not_a_docx_is_rejected(tmp_path):
    path = tmp_path / "broken.docx"
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("hello.txt", "not a word file")
    with pytest.raises(ValueError, match="missing word/document.xml"):
        extract_docx(path)


def test_the_extractor_records_its_own_provenance(tmp_path):
    doc = extract(tmp_path, p("본문입니다."))
    assert doc.meta["extractor"] == "docx_ooxml"
    assert doc.source_type == "docx"
    assert doc.doc_id == "t"
