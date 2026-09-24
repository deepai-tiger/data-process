from dataclasses import dataclass

from kdp.extract.paddleocr_lines import document_from_paddleocr, line_join_separator
from kdp.schema import BlockKind


@dataclass
class _Token:
    start: int
    len: int


class _Analyzer:
    def analyze(self, text: str, top_n: int = 1):
        if text == "움직이는것이":
            return [([_Token(0, 4), _Token(4, 3)], 10.0)]
        if text == "움직이 는것이":
            return [([], 2.0)]
        if text == "충분한운동을":
            return [([_Token(0, 3), _Token(3, 3)], 5.0)]
        if text == "충분한 운동을":
            return [([], 5.0)]
        return [([], 0.0)]


def test_line_join_uses_morphological_boundary_without_respell() -> None:
    analyzer = _Analyzer()
    assert line_join_separator("몸을 움직이", "는것이 중요하다", analyzer) == ""
    assert line_join_separator("충분한", "운동을 한다", analyzer) == " "
    assert line_join_separator("직접 련", "결되여있다", analyzer) == ""


def test_document_adapter_preserves_dprk_forms_and_drops_page_number() -> None:
    payload = {
        "pages": [
            {
                "page": 8,
                "lines": [
                    {
                        "text": "머리말",
                        "confidence": 0.99,
                        "bbox": [400, 100, 560, 145],
                    },
                    {
                        "text": "승강기를 빈번히 리용하는 사람들은 생활화되여",
                        "confidence": 0.98,
                        "bbox": [160, 250, 880, 280],
                    },
                    {
                        "text": "있습니다. <기분좋다!>",
                        "confidence": 0.97,
                        "bbox": [105, 290, 500, 320],
                    },
                    {
                        "text": "6",
                        "confidence": 0.99,
                        "bbox": [480, 1380, 495, 1405],
                    },
                ],
            }
        ]
    }

    doc = document_from_paddleocr(
        payload,
        source_path="raw/pdf/no-copy.pdf",
        doc_id="trial",
    )

    assert doc.meta["orthography_normalized"] is False
    assert doc.blocks[0].kind is BlockKind.HEADING
    prose = "\n".join(block.text for block in doc.blocks)
    assert "리용" in prose
    assert "되여" in prose
    assert "《기분좋다!》" in prose
    assert all(block.text != "6" for block in doc.blocks)
