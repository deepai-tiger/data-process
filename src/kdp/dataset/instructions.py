"""Deterministic Korean instruction/response synthesis.

No teacher LLM is involved: every answer is text that literally exists in the
source document, and every prompt is built from the document's own structure.
That keeps the SFT split free of hallucinations and legally identical in
provenance to the pretraining split.

Five task families are generated:

``summarize_title``    body -> its section heading (title generation)
``continuation``       first half of a section -> the rest
``table_to_latex``     plain-text table -> LaTeX ``tabular``
``equation_to_latex``  the sentence introducing a formula -> its LaTeX
``qa_definition``      "X란 무엇인가?" -> the defining sentence(s) from the text
"""

from __future__ import annotations

import logging
import random
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator, Sequence

from ..config import SftConfig
from ..extract.latex_table import TableCell, TableGrid, grid_to_plain_text
from ..schema import Block, BlockKind, Document, render_block

logger = logging.getLogger(__name__)

_TITLE_PROMPTS = (
    "다음 글의 내용을 가장 잘 나타내는 제목을 한국어로 작성하시오.",
    "아래 본문에 알맞은 소제목을 한 줄로 제시하시오.",
    "다음 단락들이 속한 절의 제목을 지으시오.",
)
_CONTINUATION_PROMPTS = (
    "다음 글에 이어질 내용을 원문의 문체를 유지하여 계속 작성하시오.",
    "아래 문서의 뒷부분을 이어서 써 주시오.",
)
_TABLE_PROMPTS = (
    "다음 표를 LaTeX 표(tabular) 형식으로 변환하시오.",
    "아래 표 내용을 LaTeX 코드로 작성하시오.",
)
_EQUATION_PROMPTS = (
    "다음 설명에 해당하는 수식을 LaTeX 형식으로 작성하시오.",
    "아래 문맥에서 제시된 수식을 LaTeX 코드로 표현하시오.",
)
_QA_DESCRIBE_PROMPT = "{term}에 대하여 설명하시오."
_QA_WHAT_IS_PROMPT = "{term}{particle} 무엇인가?"

#: "...이다" / "...라고 한다" - a sentence that asserts what something is
_DEFINITION_END_RE = re.compile(r"(?:이다|입니다|라고 한다|라고 부른다|말한다|한다)\.\s*$")
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")

#: Tags a definiendum may be made of: a noun phrase and nothing else. Matching
#: the topic markers 은/는 as text instead cannot tell them apart from the same
#: syllables inside a word - "석탄 또는 ..." reads as the term "석탄 또" plus
#: "는" - nor from any sentence that merely opens with a topic, which is how
#: "체육을 전문으로 하에 대하여 설명하시오" gets asked.
_TERM_TAGS = frozenset({"NNG", "NNP", "SL", "SH", "SN", "XSN", "XPN"})
#: a term needs a head noun, so a bare number or a stray letter is not one
_TERM_HEAD_TAGS = frozenset({"NNG", "NNP", "SL", "SH"})
_MAX_TERM_CHARS = 30
#: the definition itself has to say something
_MIN_DEFINITION_CHARS = 20


def _ran_particle(term: str) -> str | None:
    """``이란`` after a final consonant, ``란`` after a vowel.

    The alternation is decided by the last syllable, which only works out for
    a Hangul ending: after "Graphics View" the right form depends on how the
    name is read aloud, so those terms get the prompt that needs no particle.
    """
    last = term.strip()[-1:]
    if not ("\uac00" <= last <= "\ud7a3"):
        return None
    return "이란" if (ord(last) - 0xAC00) % 28 else "란"


def _definition_prompt(term: str, rng: random.Random) -> str:
    particle = _ran_particle(term)
    describe = _QA_DESCRIBE_PROMPT.format(term=term)
    if particle is None:
        return describe
    return rng.choice((_QA_WHAT_IS_PROMPT.format(term=term, particle=particle), describe))


_ANALYZER: Any = None


def _analyzer():
    """Kiwi, or ``None`` when it is not installed.

    Telling a definition apart from a sentence that merely opens with a topic
    needs morphology, so without Kiwi the task is skipped rather than filled
    with questions about sentence fragments.
    """
    global _ANALYZER
    if _ANALYZER is None:
        try:
            from kiwipiepy import Kiwi
        except ImportError:  # pragma: no cover - optional dependency
            logger.warning(
                "kiwipiepy is not installed; skipping the qa_definition task "
                "(`pip install kiwipiepy` to enable it)"
            )
            _ANALYZER = False
        else:
            _ANALYZER = Kiwi()
    return _ANALYZER or None


def _is_definition_marker(tokens: Sequence[Any], index: int) -> bool:
    """Whether the token at ``index`` introduces a definition.

    Either a topic particle (``운동축은``) or the copula that carries the
    definition marker 란 (``가속도란``, analysed as 가속도 + 이/VCP + 란/ETM).
    """
    token = tokens[index]
    if token.tag == "JX":
        return True
    following = tokens[index + 1] if index + 1 < len(tokens) else None
    return token.tag == "VCP" and following is not None and following.tag == "ETM"


def _definiendum(sentence: str, analyzer) -> str | None:
    """The term a sentence defines, or ``None`` if it defines nothing.

    Only the first marker is considered: the topic of a definition comes at
    the front, so a marker further in belongs to a subordinate clause.
    """
    tokens = analyzer.tokenize(sentence)
    for index, token in enumerate(tokens):
        if not _is_definition_marker(tokens, index):
            continue
        head = tokens[:index]
        if not head:
            return None
        tags = {t.tag for t in head}
        if not tags <= _TERM_TAGS or not tags & _TERM_HEAD_TAGS:
            return None
        term = sentence[head[0].start : head[-1].end].strip()
        return term if 2 <= len(term) <= _MAX_TERM_CHARS else None
    return None


@dataclass
class SftSample:
    task: str
    instruction: str
    output: str
    doc_id: str
    input: str = ""
    pages: list[int] = field(default_factory=list)
    heading_path: list[str] = field(default_factory=list)

    def messages(self, system_prompt: str | None = None) -> list[dict[str, str]]:
        user = self.instruction if not self.input else f"{self.instruction}\n\n{self.input}"
        messages = [{"role": "user", "content": user}, {"role": "assistant", "content": self.output}]
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        return messages


def build_sft_samples(doc: Document, cfg: SftConfig) -> list[SftSample]:
    if not cfg.enabled:
        return []
    rng = random.Random(f"{cfg.seed}:{doc.doc_id}")
    samples: list[SftSample] = []
    sections = list(_iter_sections(doc))

    for task in cfg.tasks:
        if task == "summarize_title":
            samples.extend(_title_samples(doc, sections, rng))
        elif task == "continuation":
            samples.extend(_continuation_samples(doc, sections, rng))
        elif task == "table_to_latex":
            samples.extend(_table_samples(doc, rng))
        elif task == "equation_to_latex":
            samples.extend(_equation_samples(doc, rng))
        elif task == "qa_definition":
            samples.extend(_definition_samples(doc, rng, _analyzer()))

    rng.shuffle(samples)
    return samples[: cfg.max_samples_per_doc]


@dataclass
class _Section:
    heading: str | None
    heading_path: list[str]
    blocks: list[Block]

    @property
    def body(self) -> str:
        return "\n\n".join(render_block(b) for b in self.blocks if render_block(b).strip())

    @property
    def pages(self) -> list[int]:
        return sorted({b.page for b in self.blocks if b.page is not None})


def _iter_sections(doc: Document) -> Iterator[_Section]:
    stack: list[tuple[int, str]] = []
    current: _Section | None = None
    for block in doc.blocks:
        if block.kind is BlockKind.PAGE_ARTIFACT:
            continue
        if block.kind in (BlockKind.TITLE, BlockKind.HEADING):
            if current is not None and current.blocks:
                yield current
            level = block.level or (1 if block.kind is BlockKind.TITLE else 2)
            stack = [(lvl, text) for lvl, text in stack if lvl < level]
            stack.append((level, block.text.strip()))
            current = _Section(heading=block.text.strip(), heading_path=[t for _, t in stack], blocks=[])
            continue
        if current is None:
            current = _Section(heading=None, heading_path=[], blocks=[])
        current.blocks.append(block)
    if current is not None and current.blocks:
        yield current


#: a title-generation prompt is truncated rather than dropped when the section
#: is long, so book-sized sections still produce samples
_MAX_TITLE_INPUT_CHARS = 6000


def _title_samples(doc: Document, sections: Sequence[_Section], rng: random.Random) -> list[SftSample]:
    samples: list[SftSample] = []
    for section in sections:
        if not section.heading or len(section.heading) < 4:
            continue
        body = section.body
        if len(body) < 200:
            continue
        if len(body) > _MAX_TITLE_INPUT_CHARS:
            body = body[:_MAX_TITLE_INPUT_CHARS].rsplit("\n\n", 1)[0]
        samples.append(
            SftSample(
                task="summarize_title",
                instruction=rng.choice(_TITLE_PROMPTS),
                input=body,
                output=section.heading,
                doc_id=doc.doc_id,
                pages=section.pages,
                heading_path=section.heading_path,
            )
        )
    return samples


def _continuation_samples(doc: Document, sections: Sequence[_Section], rng: random.Random) -> list[SftSample]:
    samples: list[SftSample] = []
    for section in sections:
        paragraphs = [render_block(b) for b in section.blocks if b.kind is BlockKind.PARAGRAPH]
        paragraphs = [p for p in paragraphs if len(p) > 80]
        if len(paragraphs) < 4:
            continue
        split = len(paragraphs) // 2
        prompt_text = "\n\n".join(paragraphs[:split])
        answer = "\n\n".join(paragraphs[split:])
        if len(prompt_text) < 200 or len(answer) < 200 or len(answer) > 4000:
            continue
        heading = f"[{' > '.join(section.heading_path)}]\n" if section.heading_path else ""
        samples.append(
            SftSample(
                task="continuation",
                instruction=rng.choice(_CONTINUATION_PROMPTS),
                input=f"{heading}{prompt_text}",
                output=answer,
                doc_id=doc.doc_id,
                pages=section.pages,
                heading_path=section.heading_path,
            )
        )
    return samples


def _table_samples(doc: Document, rng: random.Random) -> list[SftSample]:
    samples: list[SftSample] = []
    for block in doc.blocks:
        if block.kind is not BlockKind.TABLE or not block.latex:
            continue
        cells = block.meta.get("cells")
        if not cells:
            continue
        grid = TableGrid(
            cells=[
                TableCell(
                    text=c["text"],
                    row=c["row"],
                    col=c["col"],
                    row_span=c["row_span"],
                    col_span=c["col_span"],
                    is_header=c["is_header"],
                )
                for c in cells
            ],
            num_rows=block.meta.get("num_rows", 0),
            num_cols=block.meta.get("num_cols", 0),
            caption=block.meta.get("caption"),
        ).normalize()
        plain = grid_to_plain_text(grid)
        if len(plain.strip()) < 20 or grid.num_rows < 2:
            continue
        caption = block.meta.get("caption")
        header = f"표 제목: {caption}\n" if caption else ""
        samples.append(
            SftSample(
                task="table_to_latex",
                instruction=rng.choice(_TABLE_PROMPTS),
                input=f"{header}{plain}",
                output=block.latex,
                doc_id=doc.doc_id,
                pages=[block.page] if block.page else [],
            )
        )
    return samples


def _equation_samples(doc: Document, rng: random.Random) -> list[SftSample]:
    samples: list[SftSample] = []
    for index, block in enumerate(doc.blocks):
        if block.kind is not BlockKind.EQUATION or not block.latex:
            continue
        context = _preceding_sentence(doc.blocks, index)
        if not context or len(context) < 15:
            continue
        samples.append(
            SftSample(
                task="equation_to_latex",
                instruction=rng.choice(_EQUATION_PROMPTS),
                input=context,
                output=f"$$\n{block.latex}\n$$",
                doc_id=doc.doc_id,
                pages=[block.page] if block.page else [],
            )
        )
    return samples


def _preceding_sentence(blocks: Sequence[Block], index: int) -> str | None:
    for block in reversed(blocks[:index]):
        if block.kind in (BlockKind.PARAGRAPH, BlockKind.CAPTION, BlockKind.LIST_ITEM):
            sentences = [s for s in _SENTENCE_RE.split(block.text.strip()) if s.strip()]
            if sentences:
                return sentences[-1].strip()
        if block.kind in (BlockKind.TITLE, BlockKind.HEADING):
            return block.text.strip()
    return None


def _definition_samples(doc: Document, rng: random.Random, analyzer) -> list[SftSample]:
    if analyzer is None:
        return []
    samples: list[SftSample] = []
    seen: set[str] = set()
    for block in doc.blocks:
        if block.kind is not BlockKind.PARAGRAPH or len(block.text) < 60:
            continue
        sentences = [s.strip() for s in _SENTENCE_RE.split(block.text.strip()) if s.strip()]
        if not sentences:
            continue
        opening = sentences[0]
        if not _DEFINITION_END_RE.search(opening):
            continue
        term = _definiendum(opening, analyzer)
        if term is None or term in seen:
            continue
        if len(opening) - len(term) < _MIN_DEFINITION_CHARS:
            continue
        seen.add(term)
        answer = " ".join(sentences[: min(3, len(sentences))])
        samples.append(
            SftSample(
                task="qa_definition",
                instruction=_definition_prompt(term, rng),
                output=answer,
                doc_id=doc.doc_id,
                pages=[block.page] if block.page else [],
            )
        )
    return samples
