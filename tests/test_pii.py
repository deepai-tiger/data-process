"""PII redaction, including the Korean-specific identifier formats."""

from __future__ import annotations

import pytest

from kdp.clean.pii import mask_document, mask_text
from kdp.config import PiiConfig
from kdp.schema import BlockKind

from factories import document, equation, para, table


@pytest.fixture
def cfg() -> PiiConfig:
    return PiiConfig()


def test_email_is_masked(cfg):
    assert mask_text("문의: hong.gil-dong@example.co.kr 입니다.", cfg) == "문의: [MASKED_EMAIL] 입니다."


@pytest.mark.parametrize(
    "phone",
    ["010-1234-5678", "02-123-4567", "+82 10 1234 5678", "(02)123-4567"],
)
def test_phone_shapes_are_masked(cfg, phone):
    assert "[MASKED_PHONE]" in mask_text(f"연락처는 {phone} 입니다.", cfg)


def test_resident_registration_number_is_masked(cfg):
    assert mask_text("주민등록번호 900101-1234567", cfg) == "주민등록번호 [MASKED_RRN]"


def test_business_number_is_masked(cfg):
    assert mask_text("사업자등록번호 123-45-67890", cfg) == "사업자등록번호 [MASKED_BIZNO]"


def test_card_number_is_masked(cfg):
    assert mask_text("카드 1234-5678-9012-3456", cfg) == "카드 [MASKED_CARD]"


def test_urls_are_kept_by_default(cfg):
    assert "https://example.com" in mask_text("출처 https://example.com/a", cfg)


def test_urls_can_be_masked():
    cfg = PiiConfig(mask_url=True)
    assert mask_text("출처 https://example.com/a", cfg) == "출처 [MASKED_URL]"


def test_ordinary_numbers_survive(cfg):
    text = "1950년에 2,500명이 참가했고 온도는 36.5도였다."
    assert mask_text(text, cfg) == text


def test_a_year_range_is_not_a_phone_number(cfg):
    assert mask_text("1910-1945년 사이", cfg) == "1910-1945년 사이"


def test_masking_can_be_disabled():
    cfg = PiiConfig(enabled=False)
    assert mask_text("hong@example.com", cfg) == "hong@example.com"


def test_report_counts_each_kind(cfg):
    doc = document(para("hong@example.com 그리고 010-1234-5678 로 연락 바랍니다."))
    _, report = mask_document(doc, cfg)
    assert report.counts["email"] == 1
    assert report.counts["phone"] == 1
    assert report.total == 2


def test_table_cells_are_masked_alongside_the_latex(cfg):
    latex = "\\begin{tabular}{|c|}\n담당자 hong@example.com \\\\\n\\end{tabular}"
    block = table(latex, cells=[{"text": "hong@example.com", "row": 0, "col": 0}])
    doc, report = mask_document(document(block), cfg)
    assert "[MASKED_EMAIL]" in doc.blocks[0].latex
    assert doc.blocks[0].meta["cells"][0]["text"] == "[MASKED_EMAIL]"
    assert doc.blocks[0].text == doc.blocks[0].latex


def test_equations_are_left_alone(cfg):
    # a subscripted variable can look like an identifier; math is never PII
    latex = r"x_{1234} - 5678 - 9012 - 3456"
    doc, _ = mask_document(document(equation(latex)), cfg)
    assert doc.blocks[0].latex == latex


def test_masked_document_records_the_report(cfg):
    doc, _ = mask_document(document(para("hong@example.com")), cfg)
    assert doc.meta["pii"]["counts"] == {"email": 1}


def test_placeholder_prefix_is_configurable():
    cfg = PiiConfig(placeholder_prefix="<<")
    assert mask_text("hong@example.com", cfg) == "<<EMAIL]"
