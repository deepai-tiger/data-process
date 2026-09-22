"""Exact and near-duplicate removal."""

from __future__ import annotations

import pytest

from kdp.clean.dedup import (
    Deduper,
    ParagraphDeduper,
    canonical,
    dedup_texts,
    shingles,
    text_hash,
)
from kdp.config import DedupConfig

from factories import document, heading, para

PROSE = (
    "물체의 운동을 기술하기 위해서는 위치와 시간의 관계를 알아야 한다. "
    "속도는 위치의 시간에 대한 변화율이며, 가속도는 속도의 변화율이다."
)


@pytest.fixture
def cfg() -> DedupConfig:
    return DedupConfig()


def test_canonical_form_ignores_spacing_and_punctuation():
    assert canonical("한국어, 텍스트!") == canonical("한국어  텍스트")


def test_hash_is_stable_across_formatting_differences():
    assert text_hash("가나다 라마바.") == text_hash("가나다\n라마바")


def test_hash_differs_for_different_content():
    assert text_hash("가나다") != text_hash("라마바")


def test_shingles_slide_over_the_canonical_string():
    assert shingles("abcdef", 4) == {"abcd", "bcde", "cdef"}


def test_short_text_yields_one_shingle():
    assert shingles("abc", 5) == {"abc"}


def test_exact_duplicates_are_reported(cfg):
    deduper = Deduper(cfg)
    assert deduper.check("a", PROSE) is None
    assert deduper.check("b", PROSE) == "a"
    assert deduper.report.exact_duplicates == 1


def test_near_duplicates_are_caught(cfg):
    deduper = Deduper(cfg)
    original = PROSE * 3
    assert deduper.check("a", original) is None
    # one word changed out of a long passage: an OCR-level difference
    assert deduper.check("b", original.replace("가속도", "가속력", 1)) == "a"
    assert deduper.report.near_duplicates == 1


def test_unrelated_texts_are_both_kept(cfg):
    deduper = Deduper(cfg)
    assert deduper.check("a", PROSE) is None
    assert deduper.check("b", "전혀 다른 주제의 문단으로 역사와 문화를 다룬다. " * 3) is None
    assert deduper.report.kept == 2


def test_near_duplicate_detection_can_be_disabled():
    cfg = DedupConfig(near=False)
    deduper = Deduper(cfg)
    deduper.check("a", PROSE)
    assert deduper.check("b", PROSE.replace("가속도", "가속력")) is None


def test_dedup_texts_returns_the_surviving_keys(cfg):
    kept, report = dedup_texts([("a", PROSE), ("b", PROSE), ("c", "다른 내용의 긴 문단입니다. " * 5)], cfg)
    assert kept == ["a", "c"]
    assert report.exact_duplicates == 1


def test_paragraphs_repeated_across_documents_are_removed(cfg):
    boilerplate = "이 책의 무단 전재와 복제를 금합니다. 저작권은 발행처에 있습니다. " * 4
    deduper = ParagraphDeduper(cfg)

    first = document(para(boilerplate), para(PROSE), doc_id="a")
    assert deduper.filter_document(first) == 0

    second = document(para(boilerplate), para("다른 본문입니다. " * 10), doc_id="b")
    assert deduper.filter_document(second) == 1
    assert boilerplate not in second.to_markdown()
    assert second.meta["dedup"]["paragraphs_removed"] == 1


def test_a_paragraph_repeated_inside_one_document_is_kept(cfg):
    # intra-document repetition is the chunker's problem, not dedup's
    text = "같은 문단이 한 문서 안에서 두 번 나옵니다. " * 4
    deduper = ParagraphDeduper(cfg)
    doc = document(para(text), para(text), doc_id="a")
    assert deduper.filter_document(doc) == 0


def test_short_paragraphs_are_exempt(cfg):
    deduper = ParagraphDeduper(cfg)
    deduper.filter_document(document(para("짧은 문구"), doc_id="a"))
    second = document(para("짧은 문구"), doc_id="b")
    assert deduper.filter_document(second) == 0


def test_headings_are_never_deduplicated(cfg):
    long_heading = "제1장 " + "긴 제목이 반복됩니다 " * 6
    deduper = ParagraphDeduper(cfg)
    deduper.filter_document(document(heading(long_heading), doc_id="a"))
    second = document(heading(long_heading), doc_id="b")
    assert deduper.filter_document(second) == 0


def test_paragraph_dedup_can_be_disabled():
    cfg = DedupConfig(paragraph_level=False)
    text = "반복되는 공통 문단입니다. " * 6
    deduper = ParagraphDeduper(cfg)
    deduper.filter_document(document(para(text), doc_id="a"))
    assert deduper.filter_document(document(para(text), doc_id="b")) == 0
