import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEX_REVIEW = ROOT / "examples" / "science1-pages-1-30.latex.md"
OCR_REVIEW = ROOT / "examples" / "science1-pages-1-30.ocr.md"
REGION_MANIFEST = ROOT / "examples" / "science1-pages-1-30.regions.json"


def test_science_trial_has_every_numbered_equation_once() -> None:
    text = LATEX_REVIEW.read_text(encoding="utf-8")
    equation_numbers = re.findall(r"\\tag\{(1-\d+)\}", text)
    assert equation_numbers == [f"1-{number}" for number in range(1, 21)]
    equations_section = text.partition("## Tables")[0]
    assert [
        equations_section.count(f"### Page {page}")
        for page in (11, 12, 18, 19, 21, 22, 23, 24, 25)
    ] == [1] * 9


def test_science_trial_has_three_semantic_tables_and_balanced_latex() -> None:
    text = LATEX_REVIEW.read_text(encoding="utf-8")
    assert re.findall(r"\\tag\{표 (1-\d+)\}", text) == ["1-1", "1-2", "1-3"]
    assert "Page 4 — Table" not in text
    for block in re.findall(r"\\\[(.*?)\\\]", text, flags=re.DOTALL):
        assert block.count("{") == block.count("}")
        assert block.count(r"\begin") == block.count(r"\end")


def test_science_trial_covers_thirty_page_images_and_formula_regions() -> None:
    ocr = OCR_REVIEW.read_text(encoding="utf-8")
    assert re.findall(r"^## Page (\d+)$", ocr, flags=re.MULTILINE) == [
        str(page) for page in range(1, 31)
    ]
    manifest = json.loads(REGION_MANIFEST.read_text(encoding="utf-8"))
    assert manifest["source_pdf"] == "raw/pdf/science1.pdf"
    assert len(manifest["regions"]) == 24
    assert all(region["prompt"] == "formula" for region in manifest["regions"])
