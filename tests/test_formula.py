"""Formula recognition: region splitting, post-processing and plausibility."""

from __future__ import annotations

import pytest

from kdp.extract.formula import (
    NoopRecognizer,
    _collapse_letter_runs,
    _column_islands,
    _split_stacked_equations,
    build_recognizer,
    is_plausible_latex,
    postprocess_latex,
    recognize_region,
)

PIL = pytest.importorskip("PIL")
from PIL import Image, ImageDraw  # noqa: E402


# -------------------------------------------------------------- post-process


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("$E = mc^2$", "E = mc^2"),
        ("$$E = mc^2$$", "E = mc^2"),
        (r"\[E = mc^2\]", "E = mc^2"),
        ("  E  =  mc^2  ", "E = mc^2"),
    ],
)
def test_delimiters_and_padding_are_stripped(raw, expected):
    assert postprocess_latex(raw) == expected


def test_spaced_out_function_names_become_upright_text():
    assert _collapse_letter_runs("T r a n s(x)") == r"\mathrm{Trans}(x)"


def test_a_single_variable_is_left_alone():
    assert _collapse_letter_runs("x + y") == "x + y"


def test_array_column_specifications_are_not_collapsed():
    latex = r"\begin{array}{c c c} a & b & c \end{array}"
    assert _collapse_letter_runs(latex) == latex


def test_a_letter_run_next_to_an_array_spec_still_collapses():
    latex = r"\begin{array}{c c} s i n(x) & b \end{array}"
    collapsed = _collapse_letter_runs(latex)
    assert r"{c c}" in collapsed
    assert r"\mathrm{sin}(x)" in collapsed


def test_collapsing_can_be_switched_off():
    assert postprocess_latex("T r a n s", collapse_letter_runs=False) == "T r a n s"


# ------------------------------------------------------------- plausibility


@pytest.mark.parametrize(
    "latex",
    [
        "E = mc^{2}",
        r"\frac{a}{b}",
        r"\sqrt{x + 1}",
        r"\begin{aligned} a &= b \\ c &= d \end{aligned}",
        r"\int_{0}^{1} f(x) dx",
    ],
)
def test_well_formed_latex_is_accepted(latex):
    assert is_plausible_latex(latex)


@pytest.mark.parametrize(
    "latex",
    [
        "",
        r"\frac{a}{b",  # unbalanced braces
        r"\begin{aligned} a = b",  # unclosed environment
        r"\not\not\not\not x",  # decode loop
        r"\alpha " * 20,  # the same macro 20 times in a row
        "x" * 5000,  # implausibly long
        "+ - =",  # no symbols and no structure
    ],
)
def test_hallucinated_latex_is_rejected(latex):
    assert not is_plausible_latex(latex)


def test_a_structural_macro_alone_is_enough():
    assert is_plausible_latex(r"\frac{}{}")


# ------------------------------------------------------------ region splits


def strip_image(bands: list[tuple[int, int]], width: int = 400, height: int = 200):
    """White canvas with a black bar drawn across each given row band."""
    image = Image.new("L", (width, height), color=255)
    draw = ImageDraw.Draw(image)
    for top, bottom in bands:
        draw.rectangle([20, top, width - 20, bottom], fill=0)
    return image


def test_stacked_equations_are_split_on_blank_bands():
    image = strip_image([(10, 40), (90, 120), (160, 190)])
    parts = _split_stacked_equations(image)
    assert len(parts) == 3
    assert all(p.width == image.width for p in parts)


def test_a_single_equation_is_returned_unsplit():
    image = strip_image([(10, 40)])
    assert _split_stacked_equations(image) == [image]


def test_a_blank_region_is_returned_unsplit():
    image = Image.new("L", (400, 200), color=255)
    assert _split_stacked_equations(image) == [image]


def test_too_many_bands_are_left_alone():
    # 20 thin bands is a rasterized paragraph, not a stack of equations
    bands = [(i * 14, i * 14 + 12) for i in range(20)]
    image = strip_image(bands, height=300)
    assert _split_stacked_equations(image) == [image]


def test_column_islands_merge_across_narrow_gaps():
    filled = [True] * 10 + [False] * 3 + [True] * 10 + [False] * 30 + [True] * 5
    assert _column_islands(filled, min_gap=8) == [(0, 23), (53, 58)]


def test_column_islands_keep_wide_gaps_apart():
    filled = [True] * 10 + [False] * 30 + [True] * 10
    assert _column_islands(filled, min_gap=8) == [(0, 10), (40, 50)]


# ----------------------------------------------------------- the noop engine


def test_the_noop_engine_produces_nothing():
    assert NoopRecognizer().recognize(None) == ("", None)
    assert recognize_region(strip_image([(10, 40)]), NoopRecognizer()) is None


@pytest.mark.parametrize("engine", ["none", "docling", "ocr_text"])
def test_engines_without_a_local_model_fall_back_to_noop(engine):
    assert isinstance(build_recognizer(engine), NoopRecognizer)


def test_an_unknown_engine_is_rejected():
    with pytest.raises(ValueError, match="unknown formula engine"):
        build_recognizer("magic")


def test_loading_pix2tex_does_not_silence_the_rest_of_the_run(monkeypatch):
    import logging
    import sys
    import types

    module = types.ModuleType("pix2tex.cli")

    class LatexOCR:
        def __init__(self):
            logging.getLogger().setLevel(logging.FATAL)  # what pix2tex really does

        def __call__(self, image):
            return "x"

    module.LatexOCR = LatexOCR
    monkeypatch.setitem(sys.modules, "pix2tex", types.ModuleType("pix2tex"))
    monkeypatch.setitem(sys.modules, "pix2tex.cli", module)

    root = logging.getLogger()
    original = root.level
    try:
        root.setLevel(logging.INFO)
        build_recognizer("pix2tex")
        assert root.level == logging.INFO
    finally:
        root.setLevel(original)


# ----------------------------------------------------- stitching the results


class FakeRecognizer:
    """Returns a canned answer per call, so the stitching logic can be tested."""

    name = "fake"

    def __init__(self, *answers: str) -> None:
        self.answers = list(answers)

    def recognize(self, image):
        return (self.answers.pop(0) if self.answers else ""), None


def test_one_equation_is_returned_as_is():
    result = recognize_region(strip_image([(10, 40)]), FakeRecognizer("E = mc^{2}"))
    assert result.latex == "E = mc^{2}"
    assert result.parts == 1
    assert result.engine == "fake"


def test_stacked_equations_are_stitched_into_an_aligned_block():
    image = strip_image([(10, 40), (90, 120)])
    result = recognize_region(image, FakeRecognizer("a = b", "c = d"))
    assert result.latex == "\\begin{aligned}\na = b \\\\\nc = d\n\\end{aligned}"
    assert result.parts == 2


def test_implausible_parts_are_dropped_from_the_stack():
    image = strip_image([(10, 40), (90, 120)])
    result = recognize_region(image, FakeRecognizer("a = b", r"\frac{x"))
    assert result.latex == "a = b"
    assert result.parts == 1


def test_a_region_nobody_can_read_yields_nothing():
    assert recognize_region(strip_image([(10, 40)]), FakeRecognizer("")) is None


def test_splitting_can_be_switched_off():
    image = strip_image([(10, 40), (90, 120)])
    result = recognize_region(image, FakeRecognizer("a = b"), split_stacked=False)
    assert result.parts == 1
