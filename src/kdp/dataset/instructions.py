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

import random
import re
from dataclasses import dataclass, field
from typing import Iterable, Iterator, Sequence

from ..config import SftConfig
from ..extract.latex_table import TableCell, TableGrid, grid_to_plain_text
from ..schema import Block, BlockKind, Document, render_block

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
_QA_PROMPT_TEMPLATES = (
    "{term}이란 무엇인가?",
    "{term}에 대하여 설명하시오.",
)

#: "X란 ...이다" / "X는 ...을 말한다" style definition sentences
_DEFINITION_RE = re.compile(
    r"^\s*(?P<term>[\uac00-\ud7a3A-Za-z0-9()\u00b7\-/ ]{2,40}?)"
    r"(?:이란|란|이라고 하는것은|은|는)\s+"
    r"(?P<body>.{20,}?(?:이다|입니다|라고 한다|라고 부른다|말한다|한다)\.)\s*$"
)
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


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
            samples.extend(_definition_samples(doc, rng))

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


def _title_samples(doc: Document, sections: Sequence[_Section], rng: random.Random) -> list[SftSample]:
    samples: list[SftSample] = []
    for section in sections:
        if not section.heading or len(section.heading) < 4:
            continue
        body = section.body
        if len(body) < 300 or len(body) > 6000:
            continue
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


def _definition_samples(doc: Document, rng: random.Random) -> list[SftSample]:
    samples: list[SftSample] = []
    seen: set[str] = set()
    for block in doc.blocks:
        if block.kind is not BlockKind.PARAGRAPH:
            continue
        sentences = [s.strip() for s in _SENTENCE_RE.split(block.text.strip()) if s.strip()]
        if not sentences:
            continue
        match = _DEFINITION_RE.match(sentences[0])
        if not match:
            continue
        term = match.group("term").strip()
        if len(term) < 2 or term in seen or len(block.text) < 60:
            continue
        seen.add(term)
        answer = " ".join(sentences[: min(3, len(sentences))])
        samples.append(
            SftSample(
                task="qa_definition",
                instruction=rng.choice(_QA_PROMPT_TEMPLATES).format(term=term),
                output=answer,
                doc_id=doc.doc_id,
                pages=[block.page] if block.page else [],
            )
        )
    return samples
