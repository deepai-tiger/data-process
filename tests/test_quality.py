"""Quality heuristics: OCR noise, junk tables, script profiling, page verdicts."""

from __future__ import annotations

import pytest

from kdp.clean.quality import (
    block_drop_reason,
    filter_document,
    is_ocr_noise,
    looks_like_toc,
    looks_like_toc_table,
    repetition_ratios,
    script_profile,
    strip_latex,
    table_drop_reason,
    text_quality_reason,
)
from kdp.config import QualityConfig
from kdp.schema import Block, BlockKind

from factories import document, equation, heading, para, table

PROSE = (
    "물체의 운동을 기술하기 위해서는 위치와 시간의 관계를 알아야 한다. "
    "속도는 위치의 시간에 대한 변화율이며, 가속도는 속도의 변화율이다."
)


@pytest.fixture
def cfg() -> QualityConfig:
    return QualityConfig()


# ------------------------------------------------------------------ profiling


def test_script_profile_of_korean_prose():
    profile = script_profile(PROSE)
    assert profile["hangul"] > 0.95
    assert profile["latin"] == 0.0


def test_script_profile_of_an_empty_string_is_all_zero():
    assert set(script_profile("").values()) == {0.0}


def test_repetition_ratios_catch_a_repeated_line():
    ratios = repetition_ratios("같은 줄\n같은 줄\n같은 줄\n다른 줄")
    assert ratios["dup_line_ratio"] == pytest.approx(0.5)


def test_repetition_ratios_catch_a_repeated_trigram():
    text = " ".join(["가 나 다"] * 10)
    assert repetition_ratios(text)["top_ngram_ratio"] > 0.9


# ----------------------------------------------------------------- OCR noise


@pytest.mark.parametrize(
    "noise",
    [
        "아 아 애 아 애 아 아 애 아",  # Korean model reading a dot leader
        "eee cece eee cece eee",  # Latin model reading the same leader
        "ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ ㅡ",
        "...................",
    ],
)
def test_dot_leader_mush_is_recognized_as_noise(noise):
    assert is_ocr_noise(noise)


@pytest.mark.parametrize(
    "text",
    [
        PROSE,
        # Tesseract splits Korean into syllables; that alone is not noise
        "물 체 의 운 동 을 기 술 하 기 위 해 서 는 위 치 와 시 간 이 필 요 하 다",
        "The quick brown fox jumps over the lazy dog near the river bank",
        "제1장 서론",
    ],
)
def test_real_text_is_not_flagged_as_noise(text):
    assert not is_ocr_noise(text)


def test_very_short_strings_are_never_judged():
    # too little evidence either way; the length filters handle these
    assert not is_ocr_noise("가 나")


# ---------------------------------------------------------------- LaTeX strip


def test_strip_latex_removes_a_tabular_but_keeps_surrounding_prose():
    text = "표는 다음과 같다.\n\\begin{tabular}{|c|}\n\\hline\n가 \\\\\n\\end{tabular}\n끝."
    stripped = strip_latex(text)
    assert "tabular" not in stripped
    assert "hline" not in stripped
    assert "표는 다음과 같다." in stripped
    assert "끝." in stripped


def test_strip_latex_removes_display_math():
    assert "frac" not in strip_latex("식은 $$\\frac{a}{b}$$ 이다.")


def test_hline_heavy_tables_no_longer_read_as_duplicated_lines():
    rows = "\\hline\n가 & 나 \\\\\n" * 10
    latex = f"\\begin{{tabular}}{{|c|c|}}\n{rows}\\end{{tabular}}"
    assert repetition_ratios(latex)["dup_line_ratio"] > 0.5
    assert repetition_ratios(strip_latex(latex))["dup_line_ratio"] < 0.3


# --------------------------------------------------------------------- tables


def good_cells() -> list[dict[str, object]]:
    return [
        {"text": "항목", "row": 0, "col": 0},
        {"text": "값", "row": 0, "col": 1},
        {"text": "중력가속도", "row": 1, "col": 0},
        {"text": "9.8", "row": 1, "col": 1},
    ]


def test_a_well_formed_table_is_kept():
    block = table("\\begin{tabular}{|c|c|}\\end{tabular}", cells=good_cells(), num_rows=2, num_cols=2)
    assert table_drop_reason(block) is None


def test_a_mostly_empty_grid_is_a_diagram_not_a_table():
    cells = [{"text": "", "row": r, "col": c} for r in range(3) for c in range(3)]
    cells[0]["text"] = "가"
    block = table("\\begin{tabular}{|c|}\\end{tabular}", cells=cells, num_rows=3, num_cols=3)
    assert table_drop_reason(block) == "sparse_table"


def test_a_diagram_is_rejected_even_when_only_its_filled_cells_are_listed():
    # docling reports the cells it found, not the empty ones, so the four stray
    # glyphs it read off a technical drawing look like a complete 2x2 table
    # unless the declared grid is taken into account
    cells = [
        {"text": "가", "row": 0, "col": 0},
        {"text": "나", "row": 2, "col": 3},
        {"text": "다", "row": 4, "col": 1},
        {"text": "라", "row": 5, "col": 4},
    ]
    block = table("\\begin{tabular}{|c|}\\end{tabular}", cells=cells, num_rows=6, num_cols=5)
    assert table_drop_reason(block) == "sparse_table"


def test_merged_cells_count_towards_the_area_they_cover():
    cells = [
        {"text": "항목", "row": 0, "col": 0, "col_span": 2},
        {"text": "2024년", "row": 1, "col": 0, "row_span": 2},
        {"text": "12.5", "row": 1, "col": 1},
        {"text": "13.0", "row": 2, "col": 1},
    ]
    block = table("\\begin{tabular}{|c|c|}\\end{tabular}", cells=cells, num_rows=3, num_cols=2)
    assert table_drop_reason(block) is None


def test_a_grid_of_stray_glyphs_is_rejected():
    cells = [{"text": ".", "row": r, "col": c} for r in range(2) for c in range(3)]
    block = table("\\begin{tabular}{|c|}\\end{tabular}", cells=cells, num_rows=2, num_cols=3)
    assert table_drop_reason(block) == "noisy_table"


def test_a_single_column_grid_is_degenerate():
    cells = [{"text": "항목", "row": 0, "col": 0}, {"text": "값입니다", "row": 1, "col": 0}]
    block = table("\\begin{tabular}{|c|}\\end{tabular}", cells=cells, num_rows=2, num_cols=1)
    assert table_drop_reason(block) == "degenerate_table"


def test_a_table_of_contents_detected_as_a_table_is_rejected():
    cells = [
        {"text": "제1장 서론", "row": 0, "col": 0},
        {"text": "...........", "row": 0, "col": 1},
        {"text": "제2장 본론", "row": 1, "col": 0},
        {"text": "(23)", "row": 1, "col": 1},
    ]
    assert looks_like_toc_table(cells)


def test_a_data_table_is_not_mistaken_for_a_table_of_contents():
    assert not looks_like_toc_table(good_cells())


# ------------------------------------------------------------- block verdicts


def test_prose_paragraph_is_kept(cfg):
    assert block_drop_reason(para(PROSE), cfg) is None


def test_short_paragraph_is_dropped(cfg):
    assert block_drop_reason(para("짧다"), cfg) == "too_short"


def test_page_artifacts_never_reach_the_dataset(cfg):
    block = Block(kind=BlockKind.PAGE_ARTIFACT, text="- 12 -")
    assert block_drop_reason(block, cfg) == "page_artifact"


def test_table_of_contents_line_is_dropped(cfg):
    assert block_drop_reason(para("제1장 서론 ......... 12"), cfg) == "toc_line"
    assert looks_like_toc("제1장 서론 ......... 12")


def test_japanese_text_on_a_korean_page_signals_a_broken_text_layer(cfg):
    assert block_drop_reason(para("これは日本語のテキストです。とても長い文章。"), cfg) == "wrong_script"


def test_latin_only_block_is_kept_by_default(cfg):
    assert block_drop_reason(para("This paragraph is entirely in English."), cfg) is None


def test_latin_only_block_can_be_rejected(cfg):
    strict = QualityConfig(keep_latin_only_blocks=False)
    assert block_drop_reason(para("This paragraph is entirely in English."), strict) == "low_hangul_ratio"


def test_an_empty_equation_is_dropped(cfg):
    assert block_drop_reason(equation(""), cfg) == "empty_latex"


def test_a_one_character_equation_is_dropped(cfg):
    assert block_drop_reason(equation("x"), cfg) == "equation_too_short"


def test_a_real_equation_is_kept(cfg):
    assert block_drop_reason(equation(r"E = mc^{2}"), cfg) is None


def test_headings_are_judged_leniently(cfg):
    # far below min_block_chars, but a heading is supposed to be short
    assert block_drop_reason(heading("서론"), cfg) is None


# -------------------------------------------------------------- page verdicts


def test_a_page_of_mostly_noise_is_dropped_whole(cfg):
    blocks = [para("아 아 애 아 애 아 아 애 아", page=3) for _ in range(4)]
    # a single plausible-looking survivor on the same page
    blocks.append(para("제1장 서론에 대한 안내 문단입니다.", page=3))
    blocks.append(para(PROSE, page=4))
    doc, report = filter_document(document(*blocks), cfg)
    assert report.noisy_pages == [3]
    assert [b.page for b in doc.blocks] == [4]


def test_a_page_with_one_bad_block_keeps_the_rest(cfg):
    blocks = [para(PROSE, page=1) for _ in range(3)]
    blocks.append(para("아 아 애 아 애 아 아 애 아", page=1))
    doc, report = filter_document(document(*blocks), cfg)
    assert report.noisy_pages == []
    assert len(doc.blocks) == 3


def test_documents_without_pages_are_unaffected_by_the_page_rule(cfg):
    blocks = [para("아 아 애 아 애 아 아 애 아") for _ in range(4)] + [para(PROSE)]
    doc, report = filter_document(document(*blocks), cfg)
    assert report.noisy_pages == []
    assert len(doc.blocks) == 1


# ---------------------------------------------------------- document verdicts


def test_a_short_document_is_dropped(cfg):
    _, report = filter_document(document(para("본문이 너무 짧습니다. 한 문장뿐입니다.")), cfg)
    assert report.doc_reason == "doc_too_short"


def test_a_long_korean_document_is_kept(cfg):
    blocks = [para(f"{i}번째 문단입니다. {PROSE}") for i in range(5)]
    _, report = filter_document(document(*blocks), cfg)
    assert report.doc_reason is None


def test_a_table_heavy_document_survives_the_repetition_guard(cfg):
    rows = "\\hline\n" + "".join(f"항목{i} & {i} \\\\\n\\hline\n" for i in range(12))
    latex = f"\\begin{{tabular}}{{|c|c|}}\n{rows}\\end{{tabular}}"
    cells = [
        {"text": f"항목{i}" if c == 0 else str(i), "row": i, "col": c}
        for i in range(12)
        for c in range(2)
    ]
    blocks = [para(f"{i}번 설명입니다. {PROSE}") for i in range(3)]
    blocks += [table(latex, cells=cells, num_rows=12, num_cols=2) for _ in range(3)]
    _, report = filter_document(document(*blocks), cfg)
    assert report.doc_reason is None


# ------------------------------------------------------------- chunk verdicts


def test_a_prose_chunk_passes(cfg):
    assert text_quality_reason(PROSE * 2, cfg) is None


def test_a_tiny_chunk_is_rejected(cfg):
    assert text_quality_reason("짧은 조각", cfg) == "chunk_too_short"


def test_a_chunk_that_is_almost_all_latex_is_kept(cfg):
    latex = "$$\n" + " + ".join(f"x_{{{i}}}" for i in range(30)) + "\n$$"
    assert text_quality_reason(latex, cfg) is None


def test_a_repetitive_chunk_is_rejected(cfg):
    assert text_quality_reason("같은 문장이 반복됩니다. " * 30, cfg) is not None
