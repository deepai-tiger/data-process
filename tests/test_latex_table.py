"""Recognized table grids -> LaTeX tabular."""

from __future__ import annotations

from kdp.extract.latex_table import (
    TableCell,
    TableGrid,
    cells_to_grid,
    escape_latex,
    grid_to_latex,
    grid_to_plain_text,
    html_table_to_grid,
)


def simple_grid() -> TableGrid:
    return cells_to_grid(
        [
            TableCell("항목", 0, 0, is_header=True),
            TableCell("값", 0, 1, is_header=True),
            TableCell("질량", 1, 0),
            TableCell("9.8", 1, 1),
        ]
    )


def test_grid_dimensions_are_inferred_from_cells():
    grid = simple_grid()
    assert (grid.num_rows, grid.num_cols) == (2, 2)
    assert grid.header_rows() == 1


def test_tabular_has_one_row_per_source_row():
    latex = grid_to_latex(simple_grid(), environment="")
    assert latex.startswith(r"\begin{tabular}{|c|c|}")
    assert latex.endswith(r"\end{tabular}")
    assert r"\textbf{항목} & \textbf{값} \\" in latex
    assert r"질량 & 9.8 \\" in latex


def test_rules_none_drops_every_line():
    latex = grid_to_latex(simple_grid(), rules="none", environment="")
    assert r"\hline" not in latex
    assert r"\begin{tabular}{cc}" in latex


def test_rules_header_rules_only_the_header():
    latex = grid_to_latex(simple_grid(), rules="header", environment="")
    # top rule, below the header row, bottom rule
    assert latex.count(r"\hline") == 3


def test_row_and_column_spans_use_multirow_multicolumn():
    grid = cells_to_grid(
        [
            TableCell("머리글", 0, 0, col_span=2, is_header=True),
            TableCell("왼쪽", 1, 0, row_span=2),
            TableCell("a", 1, 1),
            TableCell("b", 2, 1),
        ]
    )
    latex = grid_to_latex(grid, environment="")
    assert r"\multicolumn{2}{c|}{\textbf{머리글}}" in latex
    assert r"\multirow{2}{*}{왼쪽}" in latex
    # the cell covered by the rowspan is an empty slot, not a repeat
    assert latex.count("왼쪽") == 1


def test_table_environment_wraps_tabular_with_caption_and_label():
    grid = simple_grid()
    grid.caption = "표 1. 물리 상수"
    latex = grid_to_latex(grid, label="tab:const")
    assert latex.startswith(r"\begin{table}[htbp]")
    assert r"\caption{표 1. 물리 상수}" in latex
    assert r"\label{tab:const}" in latex
    assert r"\begin{tabular}" in latex


def test_latex_special_characters_are_escaped():
    assert escape_latex("100% & $5_a") == r"100\% \& \$5\_a"


def test_cell_text_is_escaped_inside_the_table():
    grid = cells_to_grid([TableCell("50% 증가", 0, 0), TableCell("A&B", 0, 1)])
    assert r"50\% 증가 & A\&B \\" in grid_to_latex(grid, environment="")


def test_escaping_can_be_disabled_for_pre_escaped_text():
    grid = cells_to_grid([TableCell(r"\alpha", 0, 0), TableCell("x", 0, 1)])
    assert r"\alpha & x \\" in grid_to_latex(grid, escape=False, environment="")


def test_empty_grid_produces_no_latex():
    assert grid_to_latex(cells_to_grid([])) == ""
    assert grid_to_latex(cells_to_grid([TableCell("", 0, 0)])) == ""


def test_html_table_is_parsed_with_spans_and_caption():
    grid = html_table_to_grid(
        "<table><caption>결과</caption>"
        "<tr><th colspan='2'>구분</th></tr>"
        "<tr><td rowspan='2'>가</td><td>1</td></tr>"
        "<tr><td>2</td></tr></table>"
    )
    assert grid.caption == "결과"
    assert (grid.num_rows, grid.num_cols) == (3, 2)
    spanning = next(c for c in grid.cells if c.text == "가")
    assert spanning.row_span == 2
    assert spanning.col == 0


def test_html_entities_are_decoded():
    grid = html_table_to_grid("<table><tr><td>a &amp; b</td></tr></table>")
    assert grid.cells[0].text == "a & b"


def test_plain_text_rendering_fills_spanned_cells():
    grid = cells_to_grid(
        [TableCell("가", 0, 0, row_span=2), TableCell("1", 0, 1), TableCell("2", 1, 1)]
    )
    assert grid_to_plain_text(grid) == "가 | 1\n가 | 2"
