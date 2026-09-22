"""Token-aware chunking of a cleaned document."""

from __future__ import annotations

import pytest

from kdp.config import ChunkConfig
from kdp.dataset.chunk import TokenCounter, chunk_document

from factories import document, equation, heading, para, table

PROSE = (
    "물체의 운동을 기술하기 위해서는 위치와 시간의 관계를 알아야 한다. "
    "속도는 위치의 시간에 대한 변화율이며, 가속도는 속도의 변화율이다."
)


@pytest.fixture
def counter() -> TokenCounter:
    """Character heuristic: deterministic and needs no model download."""
    return TokenCounter(None)


@pytest.fixture
def cfg() -> ChunkConfig:
    return ChunkConfig(max_tokens=200, min_tokens=20)


def test_the_character_heuristic_is_used_when_no_tokenizer_is_named(counter):
    assert not counter.exact
    assert counter.name == "char-heuristic"
    assert counter.count("가나다라마바사아") == 5


def test_an_unavailable_tokenizer_falls_back_instead_of_failing():
    counter = TokenCounter("definitely/not-a-real-model-id")
    assert not counter.exact
    assert "char-heuristic" in counter.name
    assert counter.count("가나다") > 0


def test_a_short_document_becomes_one_chunk(cfg, counter):
    chunks = chunk_document(document(para(PROSE)), cfg, counter)
    assert len(chunks) == 1
    assert chunks[0].chunk_id == "doc#00000"
    assert chunks[0].n_tokens == counter.count(chunks[0].text)


def test_chunks_stay_within_the_token_budget(cfg, counter):
    doc = document(*[para(f"{i}번 문단입니다. {PROSE}") for i in range(20)])
    chunks = chunk_document(doc, cfg, counter)
    assert len(chunks) > 1
    assert all(c.n_tokens <= cfg.max_tokens * 1.3 for c in chunks)


def test_chunks_break_on_headings(cfg, counter):
    doc = document(
        heading("제1장 서론", level=1),
        para(PROSE * 2),
        heading("제2장 본론", level=1),
        para(PROSE * 2),
    )
    chunks = chunk_document(doc, cfg, counter)
    assert len(chunks) == 2
    assert chunks[0].heading_path == ["제1장 서론"]
    assert chunks[1].heading_path == ["제2장 본론"]


def test_nested_headings_all_reach_the_chunks_heading_path(cfg, counter):
    doc = document(
        heading("제1장 서론", level=1),
        heading("1.1 배경", level=2),
        para(PROSE * 2),
    )
    assert chunk_document(doc, cfg, counter)[0].heading_path == ["제1장 서론", "1.1 배경"]


def test_a_chunk_does_not_repeat_the_headings_it_already_renders(cfg, counter):
    doc = document(heading("제1장 서론", level=1), para(PROSE * 2))
    text = chunk_document(doc, cfg, counter)[0].text
    assert text.startswith("# 제1장 서론")
    assert text.count("제1장 서론") == 1


def test_a_continuation_chunk_carries_its_section_as_a_prefix(counter):
    cfg = ChunkConfig(max_tokens=120, min_tokens=20)
    doc = document(
        heading("제1장 서론", level=1),
        heading("1.1 배경", level=2),
        *[para(f"{i}번 문단입니다. {PROSE}") for i in range(6)],
    )
    chunks = chunk_document(doc, cfg, counter)
    assert len(chunks) > 1
    # the first chunk spells the headings out, later ones only get the path
    assert chunks[-1].text.startswith("제1장 서론 > 1.1 배경\n\n")


def test_the_heading_path_can_be_omitted(counter):
    cfg = ChunkConfig(max_tokens=120, min_tokens=20, prepend_heading_path=False)
    doc = document(
        heading("제1장 서론", level=1),
        *[para(f"{i}번 문단입니다. {PROSE}") for i in range(6)],
    )
    assert not chunk_document(doc, cfg, counter)[-1].text.startswith("제1장 서론\n\n")


def test_a_deeper_heading_extends_the_path_and_a_sibling_replaces_it(cfg, counter):
    doc = document(
        heading("제1장", level=1),
        para(PROSE * 2),
        heading("1.1 절", level=2),
        para(PROSE * 2),
        heading("제2장", level=1),
        para(PROSE * 2),
    )
    paths = [c.heading_path for c in chunk_document(doc, cfg, counter)]
    assert paths == [["제1장"], ["제1장", "1.1 절"], ["제2장"]]


def test_an_oversized_paragraph_is_split_on_sentence_boundaries(cfg, counter):
    doc = document(para(PROSE * 12))
    chunks = chunk_document(doc, cfg, counter)
    assert len(chunks) > 1
    # no chunk ends mid-sentence
    assert all(c.text.rstrip().endswith(("다.", "이다.")) for c in chunks)


def test_an_oversized_table_is_never_split(counter):
    cfg = ChunkConfig(max_tokens=50, min_tokens=10)
    rows = "".join(f"항목{i} & 값{i} \\\\\n\\hline\n" for i in range(40))
    latex = f"\\begin{{tabular}}{{|c|c|}}\n\\hline\n{rows}\\end{{tabular}}"
    chunks = chunk_document(document(table(latex)), cfg, counter)
    assert len(chunks) == 1
    assert chunks[0].text.count(r"\begin{tabular}") == 1
    assert chunks[0].n_tokens > cfg.max_tokens


def test_equations_render_as_display_math_inside_a_chunk(cfg, counter):
    doc = document(para(PROSE), equation("E = mc^{2}"))
    text = chunk_document(doc, cfg, counter)[0].text
    assert "$$\nE = mc^{2}\n$$" in text


def test_block_kinds_and_pages_are_recorded(cfg, counter):
    doc = document(para(PROSE, page=3), equation("E = mc^{2}", page=4))
    chunk = chunk_document(doc, cfg, counter)[0]
    assert chunk.pages == [3, 4]
    assert chunk.block_kinds == {"paragraph": 1, "equation": 1}
    assert chunk.has_latex()


def test_page_artifacts_are_excluded_from_chunks(cfg, counter):
    from kdp.schema import Block, BlockKind

    artifact = Block(kind=BlockKind.PAGE_ARTIFACT, text="- 12 -", page=1)
    chunks = chunk_document(document(para(PROSE, page=1), artifact), cfg, counter)
    assert "- 12 -" not in chunks[0].text


def test_overlap_carries_trailing_sentences_into_the_next_chunk(counter):
    cfg = ChunkConfig(max_tokens=120, min_tokens=20, overlap_tokens=40)
    doc = document(*[para(f"{i}번 문단입니다. {PROSE}") for i in range(8)])
    chunks = chunk_document(doc, cfg, counter)
    assert len(chunks) > 1
    tail = chunks[0].text.strip().split(". ")[-1]
    assert tail in chunks[1].text


def test_chunks_do_not_overlap_by_default(cfg, counter):
    import re

    doc = document(*[para(f"{i}번 문단입니다. {PROSE}") for i in range(8)])
    chunks = chunk_document(doc, cfg, counter)
    assert len(chunks) > 1
    seen = [set(re.findall(r"(\d+)번 문단입니다", c.text)) for c in chunks]
    assert seen[0].isdisjoint(seen[1])


def test_an_empty_document_produces_no_chunks(cfg, counter):
    assert chunk_document(document(), cfg, counter) == []


def test_chunk_indices_are_contiguous(cfg, counter):
    doc = document(*[para(f"{i}번 문단입니다. {PROSE}") for i in range(20)])
    chunks = chunk_document(doc, cfg, counter)
    assert [c.index for c in chunks] == list(range(len(chunks)))
