"""OMML (Office Math Markup Language) to LaTeX conversion.

Word stores equations as ``m:oMath`` trees, not as text, so a plain text dump of
a .docx silently drops every formula. This module walks the OMML tree and emits
LaTeX, which keeps equations in the training data.

Only the constructs Word's equation editor can actually produce are handled;
anything unknown degrades to the concatenated text of its children instead of
raising, so extraction never fails on an exotic document.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Callable

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _m(tag: str) -> str:
    return f"{{{M_NS}}}{tag}"


def _w(tag: str) -> str:
    return f"{{{W_NS}}}{tag}"


NARY_OPERATORS = {
    "\u2211": r"\sum",
    "\u220f": r"\prod",
    "\u2210": r"\coprod",
    "\u222b": r"\int",
    "\u222c": r"\iint",
    "\u222d": r"\iiint",
    "\u222e": r"\oint",
    "\u22c3": r"\bigcup",
    "\u22c2": r"\bigcap",
    "\u22c0": r"\bigwedge",
    "\u22c1": r"\bigvee",
    "\u2a01": r"\bigoplus",
    "\u2a02": r"\bigotimes",
}

ACCENTS = {
    "\u0302": r"\hat",
    "\u0303": r"\tilde",
    "\u0304": r"\bar",
    "\u0305": r"\bar",
    "\u0307": r"\dot",
    "\u0308": r"\ddot",
    "\u030c": r"\check",
    "\u0300": r"\grave",
    "\u0301": r"\acute",
    "\u20d7": r"\vec",
    "\u20d6": r"\overleftarrow",
    "\u23de": r"\overbrace",
    "\u23df": r"\underbrace",
}

GROUP_CHARS = {
    "\u23de": (r"\overbrace", True),
    "\u23df": (r"\underbrace", False),
    "\u23b4": (r"\overbracket", True),
    "\u23b5": (r"\underbracket", False),
}

DELIMITERS = {
    "(": "(",
    ")": ")",
    "[": "[",
    "]": "]",
    "{": r"\{",
    "}": r"\}",
    "|": "|",
    "\u2016": r"\|",
    "\u2308": r"\lceil",
    "\u2309": r"\rceil",
    "\u230a": r"\lfloor",
    "\u230b": r"\rfloor",
    "\u27e8": r"\langle",
    "\u27e9": r"\rangle",
    "": ".",
}

#: Unicode math characters Word writes literally inside ``m:t`` runs.
SYMBOLS = {
    "\u03b1": r"\alpha",
    "\u03b2": r"\beta",
    "\u03b3": r"\gamma",
    "\u03b4": r"\delta",
    "\u03b5": r"\epsilon",
    "\u03b6": r"\zeta",
    "\u03b7": r"\eta",
    "\u03b8": r"\theta",
    "\u03b9": r"\iota",
    "\u03ba": r"\kappa",
    "\u03bb": r"\lambda",
    "\u03bc": r"\mu",
    "\u03bd": r"\nu",
    "\u03be": r"\xi",
    "\u03c0": r"\pi",
    "\u03c1": r"\rho",
    "\u03c3": r"\sigma",
    "\u03c2": r"\varsigma",
    "\u03c4": r"\tau",
    "\u03c5": r"\upsilon",
    "\u03c6": r"\varphi",
    "\u03d5": r"\phi",
    "\u03c7": r"\chi",
    "\u03c8": r"\psi",
    "\u03c9": r"\omega",
    "\u0393": r"\Gamma",
    "\u0394": r"\Delta",
    "\u0398": r"\Theta",
    "\u039b": r"\Lambda",
    "\u039e": r"\Xi",
    "\u03a0": r"\Pi",
    "\u03a3": r"\Sigma",
    "\u03a6": r"\Phi",
    "\u03a8": r"\Psi",
    "\u03a9": r"\Omega",
    "\u221e": r"\infty",
    "\u2202": r"\partial",
    "\u2207": r"\nabla",
    "\u2208": r"\in",
    "\u2209": r"\notin",
    "\u220b": r"\ni",
    "\u2205": r"\emptyset",
    "\u2229": r"\cap",
    "\u222a": r"\cup",
    "\u2282": r"\subset",
    "\u2283": r"\supset",
    "\u2286": r"\subseteq",
    "\u2287": r"\supseteq",
    "\u00b1": r"\pm",
    "\u2213": r"\mp",
    "\u00d7": r"\times",
    "\u00f7": r"\div",
    "\u22c5": r"\cdot",
    "\u2218": r"\circ",
    "\u2260": r"\neq",
    "\u2264": r"\leq",
    "\u2265": r"\geq",
    "\u226a": r"\ll",
    "\u226b": r"\gg",
    "\u2248": r"\approx",
    "\u2245": r"\cong",
    "\u2261": r"\equiv",
    "\u221d": r"\propto",
    "\u2192": r"\rightarrow",
    "\u2190": r"\leftarrow",
    "\u2194": r"\leftrightarrow",
    "\u21d2": r"\Rightarrow",
    "\u21d0": r"\Leftarrow",
    "\u21d4": r"\Leftrightarrow",
    "\u2200": r"\forall",
    "\u2203": r"\exists",
    "\u00ac": r"\neg",
    "\u2227": r"\wedge",
    "\u2228": r"\vee",
    "\u22ef": r"\cdots",
    "\u2026": r"\ldots",
    "\u22ee": r"\vdots",
    "\u22f1": r"\ddots",
    "\u221a": r"\sqrt{}",
    "\u2220": r"\angle",
    "\u00b0": r"^\circ",
    "\u2032": r"'",
    "\u2033": r"''",
    "\u210f": r"\hbar",
    "\u2113": r"\ell",
    "\u211c": r"\Re",
    "\u2111": r"\Im",
    "\u2135": r"\aleph",
    "\u2af7": r"\lll",
    "\u27f6": r"\longrightarrow",
    "\u00a0": " ",
}

MATH_FUNCTIONS = {
    "sin",
    "cos",
    "tan",
    "cot",
    "sec",
    "csc",
    "sinh",
    "cosh",
    "tanh",
    "coth",
    "arcsin",
    "arccos",
    "arctan",
    "log",
    "ln",
    "lg",
    "exp",
    "min",
    "max",
    "det",
    "dim",
    "gcd",
    "lim",
    "sup",
    "inf",
    "deg",
    "arg",
    "mod",
}

SCRIPT_STYLES = {
    "double-struck": r"\mathbb",
    "script": r"\mathcal",
    "fraktur": r"\mathfrak",
    "sans-serif": r"\mathsf",
    "monospace": r"\mathtt",
    "roman": r"\mathrm",
}

_TEXT_ESCAPES = {
    "\\": r"\backslash ",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "&": r"\&",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
}

_CJK_RUN = re.compile(r"[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f\u4e00-\u9fff\u3040-\u30ff]+")


def omml_to_latex(element) -> str:
    """Convert an ``m:oMath`` / ``m:oMathPara`` element into a LaTeX string."""
    latex = _convert(element)
    return _tidy(latex)


def iter_math_elements(element):
    """Yield every top-level ``m:oMath``/``m:oMathPara`` inside ``element``."""
    for child in element.iter():
        if child.tag in (_m("oMath"), _m("oMathPara")):
            parent = child.getparent()
            while parent is not None:
                if parent.tag in (_m("oMath"), _m("oMathPara")):
                    break
                parent = parent.getparent()
            else:
                yield child


def _children(element) -> list:
    return [child for child in element if isinstance(child.tag, str)]


def _convert(element) -> str:
    handler = _HANDLERS.get(element.tag)
    if handler is not None:
        return handler(element)
    return "".join(_convert(child) for child in _children(element))


def _find(element, tag: str):
    return element.find(_m(tag))


def _convert_child(element, tag: str, default: str = "") -> str:
    child = _find(element, tag)
    if child is None:
        return default
    return _convert(child)


def _brace(latex: str) -> str:
    latex = latex.strip()
    if not latex:
        return "{}"
    if len(latex) == 1 or re.fullmatch(r"\\[A-Za-z]+", latex):
        return latex if len(latex) == 1 else f"{{{latex}}}"
    return f"{{{latex}}}"


def _handle_text(element) -> str:
    return _escape_math_text(element.text or "")


def _escape_math_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    out: list[str] = []
    for ch in text:
        if ch in SYMBOLS:
            out.append(SYMBOLS[ch] + " " if SYMBOLS[ch].startswith("\\") else SYMBOLS[ch])
        elif ch in _TEXT_ESCAPES:
            out.append(_TEXT_ESCAPES[ch])
        else:
            out.append(ch)
    latex = "".join(out)
    # Korean/CJK inside a formula is prose, not variables: keep it upright.
    latex = _CJK_RUN.sub(lambda m: rf"\text{{{m.group(0)}}}", latex)
    return _wrap_functions(latex)


def _wrap_functions(latex: str) -> str:
    def repl(match: re.Match[str]) -> str:
        word = match.group(0)
        return rf"\{word} " if word in MATH_FUNCTIONS else word

    return re.sub(r"[A-Za-z]{2,7}", repl, latex)


def _handle_run(element) -> str:
    body = "".join(_convert(child) for child in _children(element) if child.tag != _m("rPr"))
    props = _find(element, "rPr")
    if props is None:
        return body
    scr = props.find(_m("scr"))
    sty = props.find(_m("sty"))
    if scr is not None:
        macro = SCRIPT_STYLES.get(scr.get(_m("val")) or "")
        if macro:
            body = f"{macro}{_brace(body)}"
    if sty is not None:
        val = sty.get(_m("val")) or ""
        if val == "b":
            body = rf"\mathbf{_brace(body)}"
        elif val == "p":
            body = rf"\mathrm{_brace(body)}"
        elif val == "bi":
            body = rf"\boldsymbol{_brace(body)}"
    return body


def _handle_fraction(element) -> str:
    num = _convert_child(element, "num")
    den = _convert_child(element, "den")
    props = _find(element, "fPr")
    kind = ""
    if props is not None:
        type_el = props.find(_m("type"))
        kind = (type_el.get(_m("val")) if type_el is not None else "") or ""
    if kind == "lin":
        return f"{_brace(num)}/{_brace(den)}"
    if kind == "skw":
        return rf"{_brace(num)}\,/\,{_brace(den)}"
    if kind == "noBar":
        return rf"\binom{_brace(num)}{_brace(den)}"
    return rf"\frac{_brace(num)}{_brace(den)}"


def _handle_superscript(element) -> str:
    base = _convert_child(element, "e")
    sup = _convert_child(element, "sup")
    return f"{_brace(base)}^{_brace(sup)}"


def _handle_subscript(element) -> str:
    base = _convert_child(element, "e")
    sub = _convert_child(element, "sub")
    return f"{_brace(base)}_{_brace(sub)}"


def _handle_subsuperscript(element) -> str:
    base = _convert_child(element, "e")
    sub = _convert_child(element, "sub")
    sup = _convert_child(element, "sup")
    return f"{_brace(base)}_{_brace(sub)}^{_brace(sup)}"


def _handle_prescript(element) -> str:
    base = _convert_child(element, "e")
    sub = _convert_child(element, "sub")
    sup = _convert_child(element, "sup")
    return f"{{}}_{_brace(sub)}^{_brace(sup)}{_brace(base)}"


def _handle_radical(element) -> str:
    body = _convert_child(element, "e")
    degree = _convert_child(element, "deg")
    props = _find(element, "radPr")
    hide_degree = False
    if props is not None:
        hide = props.find(_m("degHide"))
        hide_degree = hide is not None and (hide.get(_m("val")) or "1") not in ("0", "false")
    if degree.strip() and not hide_degree:
        return rf"\sqrt[{degree}]{_brace(body)}"
    return rf"\sqrt{_brace(body)}"


def _handle_nary(element) -> str:
    props = _find(element, "naryPr")
    char = "\u222b"
    sub_hide = sup_hide = False
    limit_loc = ""
    if props is not None:
        chr_el = props.find(_m("chr"))
        if chr_el is not None:
            char = chr_el.get(_m("val")) or char
        sub_hide = _flag(props, "subHide")
        sup_hide = _flag(props, "supHide")
        loc_el = props.find(_m("limLoc"))
        limit_loc = (loc_el.get(_m("val")) if loc_el is not None else "") or ""
    operator = NARY_OPERATORS.get(char, rf"\operatorname{{{char}}}")
    sub = "" if sub_hide else _convert_child(element, "sub")
    sup = "" if sup_hide else _convert_child(element, "sup")
    body = _convert_child(element, "e")
    limits = ""
    if sub.strip():
        limits += f"_{_brace(sub)}"
    if sup.strip():
        limits += f"^{_brace(sup)}"
    if limit_loc == "undOvr" and operator.startswith("\\"):
        limits = r"\limits" + limits
    return f"{operator}{limits} {body}".rstrip()


def _handle_delimiter(element) -> str:
    props = _find(element, "dPr")
    beg, end, sep = "(", ")", "|"
    if props is not None:
        beg = _char_of(props, "begChr", beg)
        end = _char_of(props, "endChr", end)
        sep = _char_of(props, "sepChr", sep)
    bodies = [_convert(child) for child in element.findall(_m("e"))]
    left = DELIMITERS.get(beg, beg or ".")
    right = DELIMITERS.get(end, end or ".")
    joiner = DELIMITERS.get(sep, sep)
    inner = f" {joiner} ".join(b.strip() for b in bodies) if len(bodies) > 1 else (bodies[0] if bodies else "")
    return rf"\left{left} {inner} \right{right}"


def _handle_function(element) -> str:
    name = _convert_child(element, "fName").strip()
    body = _convert_child(element, "e").strip()
    if name and not name.startswith("\\") and name.strip("\\ ") in MATH_FUNCTIONS:
        name = "\\" + name
    return f"{name}{_brace(body)}" if name else body


def _handle_limit_low(element) -> str:
    base = _convert_child(element, "e").strip()
    lim = _convert_child(element, "lim").strip()
    if base.startswith("\\lim"):
        return rf"{base}_{_brace(lim)}"
    return rf"\underset{_brace(lim)}{_brace(base)}"


def _handle_limit_upp(element) -> str:
    base = _convert_child(element, "e").strip()
    lim = _convert_child(element, "lim").strip()
    return rf"\overset{_brace(lim)}{_brace(base)}"


def _handle_matrix(element) -> str:
    rows: list[str] = []
    for row in element.findall(_m("mr")):
        cells = [_convert(cell).strip() for cell in row.findall(_m("e"))]
        rows.append(" & ".join(cells))
    body = " \\\\ ".join(rows)
    return rf"\begin{{matrix}} {body} \end{{matrix}}"


def _handle_eq_array(element) -> str:
    rows = [_convert(cell).strip() for cell in element.findall(_m("e"))]
    body = " \\\\ ".join(rows)
    return rf"\begin{{aligned}} {body} \end{{aligned}}"


def _handle_accent(element) -> str:
    props = _find(element, "accPr")
    char = _char_of(props, "chr", "\u0302") if props is not None else "\u0302"
    macro = ACCENTS.get(char, r"\hat")
    return f"{macro}{_brace(_convert_child(element, 'e'))}"


def _handle_bar(element) -> str:
    props = _find(element, "barPr")
    pos = _char_of(props, "pos", "top") if props is not None else "top"
    macro = r"\underline" if pos == "bot" else r"\overline"
    return f"{macro}{_brace(_convert_child(element, 'e'))}"


def _handle_group_char(element) -> str:
    props = _find(element, "groupChrPr")
    char = _char_of(props, "chr", "\u23df") if props is not None else "\u23df"
    macro, _ = GROUP_CHARS.get(char, (r"\underbrace", False))
    return f"{macro}{_brace(_convert_child(element, 'e'))}"


def _handle_box(element) -> str:
    return _convert_child(element, "e")


def _handle_border_box(element) -> str:
    return rf"\boxed{_brace(_convert_child(element, 'e'))}"


def _handle_phantom(element) -> str:
    return rf"\phantom{_brace(_convert_child(element, 'e'))}"


def _handle_w_text(element) -> str:
    """Plain Word text inside ``m:oMathPara`` (e.g. equation numbers)."""
    return _escape_math_text(element.text or "")


def _handle_break(element) -> str:
    return r" \\ "


def _handle_skip(element) -> str:
    return ""


def _flag(props, tag: str) -> bool:
    el = props.find(_m(tag))
    if el is None:
        return False
    return (el.get(_m("val")) or "1") not in ("0", "false", "off")


def _char_of(props, tag: str, default: str) -> str:
    el = props.find(_m(tag))
    if el is None:
        return default
    return el.get(_m("val")) or ""


_HANDLERS: dict[str, Callable[[object], str]] = {
    _m("t"): _handle_text,
    _m("r"): _handle_run,
    _m("f"): _handle_fraction,
    _m("sSup"): _handle_superscript,
    _m("sSub"): _handle_subscript,
    _m("sSubSup"): _handle_subsuperscript,
    _m("sPre"): _handle_prescript,
    _m("rad"): _handle_radical,
    _m("nary"): _handle_nary,
    _m("d"): _handle_delimiter,
    _m("func"): _handle_function,
    _m("limLow"): _handle_limit_low,
    _m("limUpp"): _handle_limit_upp,
    _m("m"): _handle_matrix,
    _m("eqArr"): _handle_eq_array,
    _m("acc"): _handle_accent,
    _m("bar"): _handle_bar,
    _m("groupChr"): _handle_group_char,
    _m("box"): _handle_box,
    _m("borderBox"): _handle_border_box,
    _m("phant"): _handle_phantom,
    _m("rPr"): _handle_skip,
    _m("ctrlPr"): _handle_skip,
    _m("argPr"): _handle_skip,
    _w("t"): _handle_w_text,
    _w("br"): _handle_break,
    _w("rPr"): _handle_skip,
    _w("pPr"): _handle_skip,
}


def _tidy(latex: str) -> str:
    latex = re.sub(r"[ \t]+", " ", latex)
    latex = re.sub(r"\s+([_^])\s+", r"\1", latex)
    latex = re.sub(r"\\text\{([^}]*)\}\s*\\text\{([^}]*)\}", r"\\text{\1\2}", latex)
    return latex.strip()
