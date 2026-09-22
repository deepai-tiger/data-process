# korean-doc-corpus

한국어 LLM 학습용 데이터셋. `data-process` 파이프라인이 PDF/DOC/DOCX 원본에서 자동 생성했습니다.

## 규모

| 항목 | 값 |
| --- | --- |
| 원본 문서 수 | 5 |
| 사전학습 청크 | 462 |
| 토큰 수 (Qwen/Qwen2.5-7B) | 379,735 |
| SFT 샘플 | 637 |

## 생성 방법

- PDF: 페이지를 200 DPI 이미지로 변환 후 레이아웃 분석 + OCR (`tesseract_cli`, 언어 kor+eng). PDF 텍스트 레이어는 사용하지 않음.
- 표: TableFormer(`accurate`) 구조 인식 후 LaTeX `tabular` 변환.
- 수식: `pix2tex` 기반 LaTeX 변환, Word 문서는 OMML -> LaTeX 직접 변환.
- 그림/사진: 요구사항에 따라 제외.
- 한국어 띄어쓰기 교정: `kiwi`.
- 중복 제거: exact + MinHash(threshold=0.85).
- 개인정보 마스킹: 활성 (이메일/전화번호/주민등록번호/카드번호).

## 문자 구성 (표본)

| 분류 | 비율 |
| --- | --- |
| 한글 | 62.9% |
| 라틴 | 37.1% |
| 한자 | 0.0% |
| 숫자 | 2.5% |

## SFT 과제 구성

| 과제 | 샘플 수 |
| --- | --- |
| continuation | 152 |
| equation_to_latex | 101 |
| qa_definition | 118 |
| summarize_title | 240 |
| table_to_latex | 26 |

## 사용 예

```python
from datasets import load_dataset

ds = load_dataset("json", data_files={
    "train": "out/dataset/pretrain/train.jsonl",
})
```

## 한계 및 주의사항

- OCR 기반이므로 오탈자가 남아 있습니다. 문자 오류율이 중요한 경우 `out/reports/`의
  품질 지표와 페이지 이미지(`out/work/pages/`)를 비교해 검수하십시오.
- 수식/표 LaTeX는 인식 모델 출력이며 원본과 다를 수 있습니다. 괄호 균형 등
  기본 검증만 통과한 상태입니다.
- 학습 데이터로 사용하기 전에 원본 문서의 저작권/이용 조건을 확인하십시오 (현재 설정: unknown - inherit from the source documents).
