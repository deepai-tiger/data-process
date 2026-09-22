"""Redact personal data before it becomes training data.

Korean-specific formats matter here: 주민등록번호 (resident registration
numbers) and 사업자등록번호 (business numbers) have fixed shapes that are easy
to match and legally sensitive to keep.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from ..config import PiiConfig
from ..schema import BlockKind, Document

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
#: 010-1234-5678, 02)123-4567, +82 10 1234 5678
_PHONE_RE = re.compile(
    r"(?<![0-9])(?:\+?82[\s\-]?)?(?:0\d{1,2}|\(0\d{1,2}\)|0\d{1,2}\))[\s\-.]?\d{3,4}[\s\-.]\d{4}(?![0-9])"
)
#: 주민등록번호: YYMMDD-#######
_RRN_RE = re.compile(r"(?<![0-9])\d{6}\s?-\s?[1-4]\d{6}(?![0-9])")
#: 사업자등록번호: ###-##-#####
_BIZ_RE = re.compile(r"(?<![0-9])\d{3}-\d{2}-\d{5}(?![0-9])")
_CARD_RE = re.compile(r"(?<![0-9])(?:\d{4}[\s\-]){3}\d{4}(?![0-9])")
_URL_RE = re.compile(r"https?://[^\s\)\]\}>\"']+")


@dataclass
class PiiReport:
    counts: Counter = field(default_factory=Counter)

    @property
    def total(self) -> int:
        return sum(self.counts.values())

    def as_dict(self) -> dict[str, object]:
        return {"total": self.total, "counts": dict(self.counts)}


def mask_text(text: str, cfg: PiiConfig, report: PiiReport | None = None) -> str:
    if not cfg.enabled or not text:
        return text
    report = report if report is not None else PiiReport()

    def apply(pattern: re.Pattern[str], label: str, value: str) -> None:
        nonlocal text
        text, count = pattern.subn(f"{cfg.placeholder_prefix}{label}]", text)
        if count:
            report.counts[value] += count

    if cfg.mask_email:
        apply(_EMAIL_RE, "EMAIL", "email")
    if cfg.mask_rrn:
        apply(_RRN_RE, "RRN", "rrn")
        apply(_BIZ_RE, "BIZNO", "business_number")
    if cfg.mask_card:
        apply(_CARD_RE, "CARD", "card")
    if cfg.mask_phone:
        apply(_PHONE_RE, "PHONE", "phone")
    if cfg.mask_url:
        apply(_URL_RE, "URL", "url")
    return text


def mask_document(doc: Document, cfg: PiiConfig) -> tuple[Document, PiiReport]:
    report = PiiReport()
    if not cfg.enabled:
        return doc, report
    for block in doc.blocks:
        if block.kind is BlockKind.EQUATION:
            continue
        if block.kind is BlockKind.TABLE:
            if block.latex:
                block.latex = mask_text(block.latex, cfg, report)
                block.text = block.latex
            for cell in block.meta.get("cells", []):
                cell["text"] = mask_text(cell["text"], cfg, report)
            continue
        block.text = mask_text(block.text, cfg, report)
    if report.total:
        doc.meta.setdefault("pii", {}).update(report.as_dict())
    return doc, report
