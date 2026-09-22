"""Convert recognized table structures into LaTeX ``tabular`` code.

Every table engine we support (docling TableFormer, and HTML-emitting engines
such as RapidOCR/PP-Structure) is reduced to a list of :class:`TableCell`
objects, so the LaTeX serializer stays engine agnostic.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Iterable, Literal, Sequence

Rules = Literal["all", "header", "none"]

_LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(text: str) -> str:
    return "".join(_LATEX_ESCAPES.get(ch, ch) for ch in text)


@dataclass
class TableCell:
    text: str
    row: int
    col: int
    row_span: int = 1
    col_span: int = 1
    is_header: bool = False


@dataclass
class TableGrid:
    cells: list[TableCell] = field(default_factory=list)
    num_rows: int = 0
    num_cols: int = 0
    caption: str | None = None

    def normalize(self) -> "TableGrid":
        self.num_rows = max([self.num_rows] + [c.row + c.row_span for c in self.cells])
        self.num_cols = max([self.num_cols] + [c.col + c.col_span for c in self.cells])
        return self

    def header_rows(self) -> int:
        """Number of leading rows that consist only of header cells."""
        rows_with_cells = {c.row for c in self.cells}
        count = 0
        for row in range(self.num_rows):
            if row not in rows_with_cells:
                break
            row_cells = [c for c in self.cells if c.row == row]
            if row_cells and all(c.is_header for c in row_cells):
                count += 1
            else:
                break
        return count

    def to_text_grid(self) -> list[list[str]]:
        """Plain 2D view, used for prompts and quality heuristics."""
        grid = [["" for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for cell in self.cells:
            for r in range(cell.row, min(cell.row + cell.row_span, self.num_rows)):
                for c in range(cell.col, min(cell.col + cell.col_span, self.num_cols)):
                    grid[r][c] = cell.text
        return grid

    def is_degenerate(self) -> bool:
        if self.num_rows < 1 or self.num_cols < 1:
            return True
        return not any(c.text.strip() for c in self.cells)


def grid_to_latex(
    grid: TableGrid,
    rules: Rules = "all",
    escape: bool = True,
    environment: str = "table",
    align: str = "c",
    label: str | None = None,
) -> str:
    """Serialize a :class:`TableGrid` to a LaTeX table.

    Uses ``\\multicolumn``/``\\multirow`` for merged cells, so the rendered
    output needs the ``multirow`` package.
    """
    grid = grid.normalize()
    if grid.is_degenerate():
        return ""

    origins: dict[tuple[int, int], TableCell] = {(c.row, c.col): c for c in grid.cells}
    covered: dict[tuple[int, int], TableCell] = {}
    for cell in grid.cells:
        for r in range(cell.row, cell.row + cell.row_span):
            for c in range(cell.col, cell.col + cell.col_span):
                if (r, c) != (cell.row, cell.col):
                    covered[(r, c)] = cell

    vline = "|" if rules == "all" else ""
    col_spec = vline + vline.join([align] * grid.num_cols) + vline

    lines: list[str] = [f"\\begin{{tabular}}{{{col_spec}}}"]
    if rules in ("all", "header"):
        lines.append("\\hline")

    n_header = grid.header_rows()
    for row in range(grid.num_rows):
        tokens: list[str] = []
        col = 0
        while col < grid.num_cols:
            origin = origins.get((row, col))
            if origin is not None:
                body = escape_latex(origin.text.strip()) if escape else origin.text.strip()
                if origin.is_header and body:
                    body = f"\\textbf{{{body}}}"
                if origin.row_span > 1:
                    body = f"\\multirow{{{origin.row_span}}}{{*}}{{{body}}}"
                if origin.col_span > 1:
                    inner = align if rules != "all" else f"{align}|"
                    body = f"\\multicolumn{{{origin.col_span}}}{{{inner}}}{{{body}}}"
                tokens.append(body)
                col += origin.col_span
                continue
            cover = covered.get((row, col))
            span = cover.col_span if cover is not None else 1
            if span > 1:
                inner = align if rules != "all" else f"{align}|"
                tokens.append(f"\\multicolumn{{{span}}}{{{inner}}}{{}}")
            else:
                tokens.append("")
            col += span
        lines.append(" & ".join(tokens) + " \\\\")
        if rules == "all":
            lines.append("\\hline")
        elif rules == "header" and row + 1 == n_header and n_header:
            lines.append("\\hline")
    if rules == "header":
        lines.append("\\hline")
    lines.append("\\end{tabular}")
    tabular = "\n".join(lines)

    if not environment:
        return tabular
    parts = [f"\\begin{{{environment}}}[htbp]", "\\centering"]
    if grid.caption:
        caption = escape_latex(grid.caption.strip()) if escape else grid.caption.strip()
        parts.append(f"\\caption{{{caption}}}")
    if label:
        parts.append(f"\\label{{{label}}}")
    parts.append(tabular)
    parts.append(f"\\end{{{environment}}}")
    return "\n".join(parts)


class _HtmlTableParser(HTMLParser):
    """Minimal ``<table>`` reader that honours rowspan/colspan."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.cells: list[TableCell] = []
        self.caption: str | None = None
        self._row = -1
        self._occupied: set[tuple[int, int]] = set()
        self._cell: TableCell | None = None
        self._buffer: list[str] = []
        self._in_caption = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): (v or "") for k, v in attrs}
        if tag == "tr":
            self._row += 1
        elif tag in ("td", "th"):
            if self._row < 0:
                self._row = 0
            col = 0
            while (self._row, col) in self._occupied:
                col += 1
            row_span = max(1, _to_int(attr.get("rowspan"), 1))
            col_span = max(1, _to_int(attr.get("colspan"), 1))
            self._cell = TableCell("", self._row, col, row_span, col_span, is_header=tag == "th")
            for r in range(self._row, self._row + row_span):
                for c in range(col, col + col_span):
                    self._occupied.add((r, c))
            self._buffer = []
        elif tag == "caption":
            self._in_caption = True
            self._buffer = []
        elif tag == "br" and self._cell is not None:
            self._buffer.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in ("td", "th") and self._cell is not None:
            self._cell.text = _squeeze("".join(self._buffer))
            self.cells.append(self._cell)
            self._cell = None
            self._buffer = []
        elif tag == "caption":
            self.caption = _squeeze("".join(self._buffer)) or None
            self._in_caption = False
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None or self._in_caption:
            self._buffer.append(data)


def html_table_to_grid(table_html: str, caption: str | None = None) -> TableGrid:
    parser = _HtmlTableParser()
    parser.feed(html.unescape(table_html) if "&" in table_html else table_html)
    parser.close()
    grid = TableGrid(cells=parser.cells, caption=caption or parser.caption)
    return grid.normalize()


def cells_to_grid(
    cells: Iterable[TableCell], num_rows: int = 0, num_cols: int = 0, caption: str | None = None
) -> TableGrid:
    return TableGrid(cells=list(cells), num_rows=num_rows, num_cols=num_cols, caption=caption).normalize()


def grid_to_plain_text(grid: TableGrid, sep: str = " | ") -> str:
    """Tab/pipe rendering used as the *question* side of table->LaTeX samples."""
    rows = grid.to_text_grid()
    return "\n".join(sep.join(_squeeze(cell) for cell in row) for row in rows)


def _to_int(value: str | None, default: int) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _squeeze(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
