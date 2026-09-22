"""Mapping docling's page layout onto our blocks.

The model-driven parts need weights and a page image, so what is tested here is
the plumbing around them: reassembling OCR cells, deciding which text found
inside an illustration is content, and pairing a picture with its cluster.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from kdp.extract.pdf_image import (
    _bbox_key,
    _clean_cell_text,
    _inflate,
    _is_enclosed_prose,
    _join_cells,
    _text_inside_pictures,
)

pytest.importorskip("docling_core")
from docling_core.types.doc import DocItemLabel  # noqa: E402


# ------------------------------------------------------------- doubles


@dataclass
class FakeCell:
    text: str


@dataclass
class FakeBBox:
    l: float  # noqa: E741 - docling's field name
    t: float
    r: float
    b: float

    def to_top_left_origin(self, page_height: float) -> "FakeBBox":
        return FakeBBox(l=self.l, t=page_height - self.t, r=self.r, b=page_height - self.b)


@dataclass
class FakeCluster:
    label: DocItemLabel
    bbox: FakeBBox = field(default_factory=lambda: FakeBBox(0, 0, 100, 100))
    cells: list[FakeCell] = field(default_factory=list)
    children: list["FakeCluster"] = field(default_factory=list)


@dataclass
class FakeProv:
    bbox: FakeBBox


@dataclass
class FakeItem:
    prov: list[FakeProv]


def conversion(clusters: list[FakeCluster], page_no: int = 1):
    layout = type("Layout", (), {"clusters": clusters})()
    predictions = type("Predictions", (), {"layout": layout})()
    page = type("Page", (), {"page_no": page_no, "predictions": predictions})()
    return type("Conversion", (), {"pages": [page]})()


def picture(children: list[FakeCluster], bbox: FakeBBox | None = None) -> FakeCluster:
    return FakeCluster(
        label=DocItemLabel.PICTURE,
        bbox=bbox or FakeBBox(40.4, 121.0, 319.2, 464.0),
        children=children,
    )


def text_cluster(words: list[str], label: DocItemLabel = DocItemLabel.TEXT) -> FakeCluster:
    return FakeCluster(label=label, cells=[FakeCell(w) for w in words])


# ------------------------------------------------------------ cell joining


def test_ocr_cells_are_joined_into_one_line():
    cells = [FakeCell("절삭"), FakeCell("운동의"), FakeCell("경우")]
    assert _join_cells(cells) == "절삭 운동의 경우"


def test_empty_cells_do_not_leave_double_spaces():
    assert _join_cells([FakeCell("가"), FakeCell("  "), FakeCell("나")]) == "가 나"


def test_the_parser_placeholder_becomes_a_hyphen():
    assert _join_cells([FakeCell("algo\x02"), FakeCell("rithm")]) == "algo- rithm"


def test_cell_borders_read_as_text_are_stripped():
    assert _clean_cell_text("|  9.8 \uff5c") == "9.8"


# --------------------------------------------------- text inside a picture


@pytest.mark.parametrize(
    "text",
    [
        "1. 그림에 있는 침혈위치를 확인한다.",
        "2. 《아프다!》 든가 《기분좋다!》 고 느껴지는데를 찾아낸다.",
        "Figure axis label spelled out",
    ],
)
def test_a_phrase_printed_over_a_drawing_is_content(text):
    assert _is_enclosed_prose(text)


@pytest.mark.parametrize("text", ["~", "아파", "FDRG", "12 13", "ae,", "1. 2. 3. 4.", ""])
def test_misread_artwork_is_not_content(text):
    assert not _is_enclosed_prose(text)


def test_the_numbered_steps_printed_on_an_illustration_are_recovered():
    step = text_cluster("1. 그림에 있는 침혈위치를 확인한다.".split(), DocItemLabel.LIST_ITEM)
    glyph = text_cluster(["~"])
    found = _text_inside_pictures(conversion([picture([step, glyph])]))

    entries = found[1][(40.4, 121.0, 319.2, 464.0)]
    assert [e.label for e in entries] == [DocItemLabel.LIST_ITEM]
    assert entries[0].text == "1. 그림에 있는 침혈위치를 확인한다."


def test_a_picture_holding_nothing_but_stray_glyphs_is_left_out():
    only_noise = picture([text_cluster(["~"]), text_cluster(["12"]), text_cluster(["ae,"])])
    assert _text_inside_pictures(conversion([only_noise])) == {}


def test_text_outside_pictures_is_not_collected_twice():
    # body text is already in the converted document; only pictures are mined
    body = text_cluster("가공품 병진보내기가 여기에 속한다.".split())
    assert _text_inside_pictures(conversion([body])) == {}


def test_a_page_without_layout_predictions_is_skipped():
    page = type("Page", (), {"page_no": 1, "predictions": type("P", (), {"layout": None})()})()
    assert _text_inside_pictures(type("C", (), {"pages": [page]})()) == {}


# ----------------------------------------------------------- picture identity


def test_a_picture_item_and_its_cluster_agree_on_one_key():
    # the item measures from the bottom of the page, the cluster from the top
    page_height = 535.3
    item = FakeItem(prov=[FakeProv(FakeBBox(l=40.4, t=414.3, r=319.2, b=71.3))])
    assert _bbox_key(item, page_height) == (40.4, 121.0, 319.2, 464.0)


def test_an_item_without_provenance_has_no_key():
    assert _bbox_key(FakeItem(prov=[]), 535.3) == ()


# ------------------------------------------------------------------ cropping


def test_a_crop_is_inflated_without_leaving_the_page():
    assert _inflate((10.0, 20.0, 50.0, 60.0), (100, 100), margin=6) == (4, 14, 56, 66)
    assert _inflate((2.0, 2.0, 98.0, 98.0), (100, 100), margin=6) == (0, 0, 100, 100)
