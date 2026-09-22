"""OMML (Word equation) -> LaTeX conversion."""

from __future__ import annotations

import pytest
from lxml import etree

from kdp.extract.omml import M_NS, W_NS, omml_to_latex

NSMAP = f'xmlns:m="{M_NS}" xmlns:w="{W_NS}"'


def convert(inner_xml: str) -> str:
    return omml_to_latex(etree.fromstring(f"<m:oMath {NSMAP}>{inner_xml}</m:oMath>"))


def run(text: str) -> str:
    return f"<m:r><m:t>{text}</m:t></m:r>"


def test_plain_run():
    assert convert(run("x+y")) == "x+y"


def test_fraction():
    latex = convert(f"<m:f><m:num>{run('a')}</m:num><m:den>{run('b')}</m:den></m:f>")
    assert latex == r"\frac{a}{b}"


def test_linear_fraction():
    xml = (
        '<m:f><m:fPr><m:type m:val="lin"/></m:fPr>'
        f"<m:num>{run('a')}</m:num><m:den>{run('b')}</m:den></m:f>"
    )
    assert convert(xml) == "a/b"


def test_superscript_and_subscript():
    assert convert(f"<m:sSup><m:e>{run('x')}</m:e><m:sup>{run('2')}</m:sup></m:sSup>") == "x^{2}"
    assert convert(f"<m:sSub><m:e>{run('a')}</m:e><m:sub>{run('i')}</m:sub></m:sSub>") == "a_{i}"


def test_subsuperscript():
    xml = f"<m:sSubSup><m:e>{run('x')}</m:e><m:sub>{run('i')}</m:sub><m:sup>{run('2')}</m:sup></m:sSubSup>"
    assert convert(xml) == "x_{i}^{2}"


def test_radical_with_degree():
    xml = f"<m:rad><m:deg>{run('3')}</m:deg><m:e>{run('x')}</m:e></m:rad>"
    assert convert(xml) == r"\sqrt[3]{x}"


def test_radical_hidden_degree():
    xml = f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{run("2")}</m:e></m:rad>'
    assert convert(xml) == r"\sqrt{2}"


def test_nary_sum_with_limits():
    xml = (
        '<m:nary><m:naryPr><m:chr m:val="\u2211"/><m:limLoc m:val="undOvr"/></m:naryPr>'
        f"<m:sub>{run('i=1')}</m:sub><m:sup>{run('n')}</m:sup><m:e>{run('a')}</m:e></m:nary>"
    )
    latex = convert(xml)
    assert latex.startswith(r"\sum\limits_{i=1}^{n}")
    assert latex.endswith("a")


def test_integral_default_operator():
    xml = f"<m:nary><m:naryPr/><m:sub/><m:sup/><m:e>{run('f')}</m:e></m:nary>"
    assert convert(xml) == r"\int f"


def test_delimiters_default_parentheses():
    xml = f"<m:d><m:e>{run('x')}</m:e></m:d>"
    assert convert(xml) == r"\left( x \right)"


def test_delimiters_custom_chars():
    xml = f'<m:d><m:dPr><m:begChr m:val="["/><m:endChr m:val="]"/></m:dPr><m:e>{run("v")}</m:e></m:d>'
    assert convert(xml) == r"\left[ v \right]"


def test_matrix():
    xml = (
        "<m:m>"
        f"<m:mr><m:e>{run('1')}</m:e><m:e>{run('0')}</m:e></m:mr>"
        f"<m:mr><m:e>{run('0')}</m:e><m:e>{run('1')}</m:e></m:mr>"
        "</m:m>"
    )
    assert convert(xml) == r"\begin{matrix} 1 & 0 \\ 0 & 1 \end{matrix}"


def test_accent_and_bar():
    assert convert(f'<m:acc><m:accPr><m:chr m:val="\u20d7"/></m:accPr><m:e>{run("v")}</m:e></m:acc>') == r"\vec{v}"
    assert convert(f"<m:bar><m:barPr/><m:e>{run('x')}</m:e></m:bar>") == r"\overline{x}"


def test_function_name_gets_macro():
    xml = f"<m:func><m:fName>{run('sin')}</m:fName><m:e>{run('x')}</m:e></m:func>"
    assert convert(xml) == r"\sin{x}"


def test_greek_and_operator_symbols():
    assert r"\theta" in convert(run("\u03b8"))
    assert r"\leq" in convert(run("\u2264"))
    assert r"\times" in convert(run("\u00d7"))


def test_korean_text_is_kept_upright():
    latex = convert(run("\ub2e8\uc704\ud589\ub82c"))
    assert latex == r"\text{단위행렬}"


def test_script_style_double_struck():
    xml = '<m:r><m:rPr><m:scr m:val="double-struck"/></m:rPr><m:t>R</m:t></m:r>'
    assert convert(xml) == r"\mathbb{R}"


def test_unknown_element_degrades_to_children():
    xml = f"<m:unknownThing>{run('z')}</m:unknownThing>"
    assert convert(xml) == "z"


def test_special_characters_are_escaped():
    assert convert(run("50%")) == r"50\%"


def test_equation_array():
    xml = f"<m:eqArr><m:e>{run('a=1')}</m:e><m:e>{run('b=2')}</m:e></m:eqArr>"
    assert convert(xml) == r"\begin{aligned} a=1 \\ b=2 \end{aligned}"
