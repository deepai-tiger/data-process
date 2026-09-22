# data-process — 한국어 LLM 학습 데이터셋 파이프라인

PDF / DOC / DOCX 원본을 받아 Qwen · Llama · DeepSeek 같은 오픈소스 파운데이션 모델을
학습시킬 수 있는 **정제된 한국어 데이터셋**을 만드는 파이프라인입니다.

- 본문 · **수식** · **표**를 모두 추출하고, 수식과 표는 **LaTeX**로 변환합니다.
- 그림/사진은 요구사항에 따라 제외하되, 몇 개를 건너뛰었는지 기록합니다.
- PDF는 **텍스트 레이어를 읽지 않습니다.** 한 페이지를 한 장의 이미지로 만들고
  레이아웃 분석 + OCR로 내용을 복원합니다.
- 결과물은 사전학습용(`pretrain`)과 지시학습용(`sft`) JSONL/Parquet 두 벌입니다.

```
raw/*.pdf|doc|docx  →  extract  →  clean  →  build  →  out/dataset/*.jsonl
```

---

## 왜 PDF를 이미지로 처리하는가

`raw/pdf`의 세 파일에서 텍스트 레이어를 그대로 읽어 문자 구성을 세어 보면
이렇습니다.

| 파일 | 쪽 | 한글 | 한자·가나 | 사용자정의영역 |
| --- | --- | --- | --- | --- |
| `no-copy.pdf` | 147 | **0.0%** | 55.9% | 0.0% |
| `story1.pdf` | 290 | 69.0% | 0.0% | 0.0% |
| `science1.pdf` | 199 | 42.8% | 0.1% | **4.6%** |

`no-copy.pdf`는 cmap이 깨져 있어 복사하면 한글이 **한 글자도** 나오지 않고
전부 한자·가나로 둔갑합니다. `science1.pdf`는 본문은 읽히지만 수식이 사용자
정의 영역 글자로 쏟아지고 읽기 순서도 뒤엉킵니다(아래는 실제 추출 결과입니다).

```
20 \uf0fa\uf0fa\uf0fb\uf0f9\uf0ea\uf0ea\uf0eb\uf0e9\uf02d\uf03d ) ( cos 0 ) ( sin 0 1 ...
```

`story1.pdf`만은 텍스트 레이어가 멀쩡합니다. 그래도 이미지로 처리합니다.
**어느 쪽인지는 이렇게 재보기 전에는 알 수 없고**, 깨진 글자는 조용히 말뭉치를
오염시킨 뒤 나중에 걸러내기도 어렵기 때문입니다. 한 가지 경로로만 처리하면
품질이 원본 파일의 운에 좌우되지 않습니다.

그래서 **PyMuPDF로 페이지를 PNG로 렌더링한 뒤**, 그 이미지에만 레이아웃 분석과
OCR을 적용합니다. 원본 텍스트 레이어는 어떤 경로로도 참조하지 않습니다.

---

## 파이프라인

### 1단계 `extract` — 원본 → 구조화 JSON

**PDF** (`src/kdp/extract/pdf_image.py`)

```
PDF 페이지 ─PyMuPDF(200dpi)→ PNG ─docling 레이아웃 모델→ 영역별 분기
                                    ├ 본문   : Tesseract OCR (kor+eng, 전면 OCR)
                                    ├ 표     : TableFormer 구조 인식 → LaTeX tabular
                                    ├ 수식   : 영역 잘라내기 → pix2tex → LaTeX
                                    └ 그림   : 폐기. 단, 그림 영역 안에 인쇄된
                                               글(번호 붙은 설명 등)은 살려냄
```

#### Tesseract 페이지 분할 모드 (`ocr.psm`)

Tesseract의 기본 분할 모드(psm 3)는 한국어 본문을 **세로쓰기로 오인**해 페이지
대부분을 낱글자 조각으로 되돌려줍니다. psm 6(하나의 균일한 텍스트 블록)으로
바꾸면 같은 이미지에서 한글이 1.3~3.3배 더 나옵니다.

| 문서 | 쪽 | psm 3 | psm 6 |
| --- | --- | --- | --- |
| `no-copy.pdf` | 8 | 367자 | **488자** |
| `no-copy.pdf` | 22 | 25자 | **70자** |
| `story1.pdf` | 20 | 325자 | **472자** |
| `science1.pdf` | 30 | 113자 | **370자** |

글자 수만 늘어난 것이 아닙니다. `science1.pdf` 29쪽에서 psm 3이 내놓은 것은
`Wo oH / 애 배 / RP ay / ca` 같은 잔해였고, psm 6은 같은 자리에서
`가공품병진보내기 b_f(t)가 여기에 속한다.`로 시작하는 온전한 문단을 돌려주었습니다.
그래서 기본값은 6이며, 다단 편집 스캔이라면 4로 낮추십시오.

#### 그림 안에 인쇄된 글

레이아웃 모델은 삽화와 겹친 글을 그림 영역에 흡수시켜 버립니다. 실기 서적은
설명이 그림 위에 인쇄되므로(`1. 그림에 있는 침혈위치를 확인한다...`) 그림을
버리면 본문도 함께 사라집니다. 그래서 그림 영역 **안쪽의 텍스트 클러스터**만
따로 건져내되, 도면에서 잘못 읽힌 획이 섞이지 않도록 낱글자·부분그림 번호
(`~`, `12`, `FDRG`)는 문구 기준(두 단어 이상, 10자 이상)으로 걸러냅니다.

수식 영역은 그냥 인식기에 넣지 않습니다. 한국어 교과서의 "수식 영역"은 대개
여러 식이 세로로 쌓인 덩어리에 오른쪽 끝 수식 번호가 붙어 있는데, 인식기는 식
하나를 가정하고 학습돼 있기 때문입니다. 그래서 먼저 가로 여백을 기준으로
**쌓인 식을 분리**하고, 오른쪽 끝의 **수식 번호를 떼어내** `\tag{}`로 옮긴 뒤
한 식씩 인식합니다. 결과 LaTeX는 괄호 균형·환경 짝·디코딩 루프 여부를 검사해
통과한 것만 남깁니다. 잘못된 수식은 없는 수식보다 나쁘기 때문입니다.

**DOCX** (`src/kdp/extract/docx_ooxml.py`)

Word 파일은 이미 구조화돼 있으므로 OCR 없이 OOXML 트리를 직접 걷습니다. 단순
텍스트 덤프가 버리는 것들을 지키는 게 핵심입니다.

- 표 → `w:tbl`의 `gridSpan`/`vMerge`를 `\multicolumn`/`\multirow`로 변환
- 수식 → **OMML을 LaTeX로 직접 변환** (`src/kdp/extract/omml.py`, 분수·근호·
  적분·행렬·악센트·첨자 등)
- 목차/머리글/바닥글 스타일 문단은 `page_artifact`로 표시해 본문에서 제외
- 그림은 건너뛰되 개수를 기록. 변환할 수 없는 구형 수식 개체(Equation 3.0)는
  경고로 남겨 조용히 사라지지 않게 함

**DOC (구형 바이너리)** (`src/kdp/extract/doc_legacy.py`)

헤드리스 LibreOffice로 `.docx`로 변환한 뒤 위 경로를 재사용합니다. 변환마다
독립된 사용자 프로필을 써서 병렬 변환이 안전합니다.

산출물은 원본 한 개당 JSON 하나(`out/interim/docjson/<doc_id>.json`)입니다.
블록마다 종류·페이지·좌표·LaTeX·신뢰도를 담고 있어 이후 단계는 원본 포맷을
전혀 몰라도 됩니다. 페이지 단위 캐시가 있어 재실행은 OCR을 다시 하지 않습니다.

### 2단계 `clean` — 정규화 · 품질 필터 · 비식별화

순서가 중요합니다.

1. **정규화** — NFC 통일, 제어/서식/사용자정의영역 문자 제거, 따옴표·대시·전각
   기호 정리, 줄바꿈으로 끊긴 문단 잇기, 영문 하이픈 복원, 반복되는 머리글·
   바닥글·쪽번호를 `page_artifact`로 강등, 페이지 경계에서 잘린 문단 봉합
2. **품질 필터** — 아래 참조
3. **띄어쓰기 교정** — Tesseract 한국어 모델은 "널리 리용한다"를 "널리 리 용 한다"로
   음절 단위로 쪼갭니다. Kiwi의 통계 띄어쓰기 모델로 복원하되, 인라인 LaTeX
   구간은 한 글자도 건드리지 않습니다
4. **PII 마스킹** — 이메일·전화번호·**주민등록번호**·**사업자등록번호**·카드번호
5. **중복 제거** — 문서/청크 단위 exact + MinHash LSH 근사 중복, 문서 사이에
   반복되는 문단(판권지·공통 안내문) 제거

품질 필터가 띄어쓰기 교정보다 **먼저** 오는 것은 의도적입니다. 목차의 점선을
OCR이 잘못 읽은 "아 아 애 아 애 아" 같은 잡음은 음절이 떨어져 있는 상태에서
가장 잘 드러나고, 띄어쓰기를 고쳐 놓으면 평범한 단어처럼 위장되기 때문입니다.

품질 필터(`src/kdp/clean/quality.py`)가 보는 것:

| 대상 | 판정 |
| --- | --- |
| 블록 | 길이, 한글/라틴/숫자/기호 비율, 목차 줄, OCR 잡음, 문자 반복 |
| 표 | 빈 셀 비율, 의미 있는 셀 비율, 1행/1열 퇴화, 목차가 표로 잡힌 경우 |
| 페이지 | 한 페이지의 영역 대부분이 잡음이면 페이지째 폐기 (표지·목차 페이지) |
| 문서 | 총 길이, 중복 줄 비율, 상위 3-gram 비율, 한국어 여부 |

산문 지표는 **LaTeX를 걷어낸 뒤** 계산합니다. 그렇게 하지 않으면 표가 세 개
들어간 페이지가 모든 행 끝의 `\hline` 때문에 "중복 줄 50%"로 보여 멀쩡한 문서가
통째로 버려집니다.

모든 폐기에는 이유 문자열이 붙고 `out/reports/clean.json`에 집계됩니다.

### 3단계 `build` — 학습용 데이터셋

**사전학습 청크** — 섹션 경계에서 끊고, 표/수식 LaTeX는 절대 반으로 자르지
않으며, 제목 경로("제1장 > 1.1절")를 함께 실어 모델이 사람과 같은 맥락을 보게
합니다. 길이는 실제 토크나이저(기본 `Qwen/Qwen2.5-7B`)로 셉니다. 토크나이저를
받을 수 없는 오프라인 환경에서는 문자 기반 추정으로 자동 대체됩니다.

**SFT 샘플** — 교사 LLM을 쓰지 않습니다. 모든 정답은 원문에 그대로 있는 문자열이고
모든 질문은 문서 구조에서 만들어집니다. 환각이 섞일 여지가 없고, 저작권상 지위도
원문과 동일합니다.

| 과제 | 입력 → 출력 |
| --- | --- |
| `summarize_title` | 절 본문 → 그 절의 제목 |
| `continuation` | 절의 앞부분 → 뒷부분 |
| `table_to_latex` | 표의 평문 격자 → LaTeX `tabular` |
| `equation_to_latex` | 수식을 소개하는 문장 → 그 수식의 LaTeX |
| `qa_definition` | "X란 무엇인가?" → 원문의 정의 문장 |

`qa_definition`의 용어는 정규식이 아니라 Kiwi의 형태소 분석으로 찾습니다.
"…은/는"을 글자로 맞추면 단어 속의 같은 글자와 구별할 수 없어("석탄 **또는**"이
"석탄 또"+"는"으로 읽힘) 문장 조각을 용어로 물어보게 됩니다. 그래서 주제 조사
앞이 **명사구인 경우에만** 용어로 인정하며, 질문의 "이란/란"도 받침에 맞춰
고릅니다. Kiwi가 없으면 이 과제만 건너뜁니다.

**출력 형식**

```
out/dataset/
├── pretrain/train.jsonl       {"id", "text", "meta"}
├── pretrain/train.parquet
├── sft/train.jsonl            {"id", "messages", "meta"}   ← 모델 중립 형식
├── sft/train.qwen.jsonl       {"id", "text", "meta"}       ← ChatML 적용
├── sft/train.llama3.jsonl                                  ← Llama 3 형식
├── sft/train.deepseek.jsonl                                ← DeepSeek 형식
├── stats.json
└── dataset_card.md
```

`messages` 형식은 Axolotl · LLaMA-Factory · TRL이 그대로 받습니다. 템플릿이
적용된 `text` 필드는 원시 문자열을 요구하는 학습기를 위한 것입니다.
`hf:<model_id>`를 지정하면 해당 모델의 `chat_template`으로 렌더링합니다.

학습/검증 분할은 **문서 단위**라서 같은 문서의 내용이 양쪽에 걸치지 않습니다.

---

## 설치

```bash
make system-deps   # tesseract(+kor), libreoffice-writer, poppler-utils, fonts-nanum
make setup         # .venv 생성, CPU 전용 torch, 패키지 설치
make prefetch      # 모델 가중치 미리 받기 (오프라인 실행용, 선택)
make doctor        # 의존성 점검
```

GPU 머신이라면 `bash scripts/setup_python_env.sh --gpu`를 쓰십시오.

`make doctor`는 빠진 것을 설치 명령과 함께 알려줍니다.

```
[OK  ] tesseract              /usr/bin/tesseract
[OK  ] tesseract kor data     kor
[OK  ] libreoffice            /usr/bin/soffice
[OK  ] docling                importable
[WARN] pix2tex                not installed (optional)
       -> pip install pix2tex  (equation -> LaTeX)
```

---

## 사용법

```bash
make run                       # raw/ 전체를 세 단계 모두 실행
make demo                      # 각 PDF 앞 6쪽만 (빠른 확인용)

kdp run --pages 1-20 --dpi 300 # 페이지/해상도 지정
kdp extract --raw raw/pdf/science1.pdf   # 파일 하나만
kdp clean                      # 추출 결과를 그대로 두고 정제만 다시
kdp build --max-tokens 4096    # 청크 크기만 바꿔 다시 패키징
kdp inspect science1 --markdown          # 추출 결과 확인
kdp stats                      # 마지막 빌드 통계
```

추출이 가장 비싼 단계이고 페이지 단위로 캐시되므로, 정제·패키징 설정을 바꿔가며
반복할 때는 `kdp clean` / `kdp build`만 다시 돌리면 됩니다.

설정은 전부 `configs/default.yaml`에 있습니다. 복사해서 `--config configs/mine.yaml`로
넘기거나 위처럼 CLI 플래그로 덮어쓸 수 있습니다.

### 알아둘 만한 설정

| 키 | 기본값 | 의미 |
| --- | --- | --- |
| `pdf.mode` | `page_images` | 페이지를 이미지로 만들어 분석. `docling_native`는 docling이 PDF를 직접 열되 전면 OCR은 유지 |
| `pdf.dpi` | `200` | 300으로 올리면 작은 글자 인식률이 오르고 처리 시간이 배로 |
| `pdf.formula_engine` | `pix2tex` | CPU에서 식당 1~2초. `docling`은 CodeFormula VLM으로 품질은 낫지만 GPU가 사실상 필수 |
| `ocr.engine` | `tesseract_cli` | `easyocr`는 띄어쓰기가 낫지만 본 샘플에서 텍스트 누락이 많았음 |
| `ocr.psm` | `6` | 페이지 분할 모드. 기본값 3은 한국어를 세로쓰기로 오인함(위 표 참조). 다단이면 4 |
| `normalize.spacing_engine` | `kiwi` | OCR 텍스트 띄어쓰기 복원. Word 원본에는 적용하지 않음 |
| `chunk.tokenizer` | `Qwen/Qwen2.5-7B` | 빈 문자열이면 문자 기반 추정(오프라인) |
| `dataset.render_templates` | `[qwen, llama3, deepseek]` | `hf:<model_id>`도 가능 |

---

## 출력물 둘러보기

```
out/
├── work/pages/<doc_id>/p0001.png   렌더링된 페이지 이미지 (OCR 결과 눈으로 대조용)
├── work/pagecache/                 페이지 단위 추출 캐시
├── work/converted/                 .doc → .docx 변환 결과
├── interim/docjson/<doc_id>.json   추출 원형
├── interim/clean/<doc_id>.json     정제 후
├── interim/markdown/<doc_id>.md    사람이 읽기 위한 Markdown
├── reports/extract.json            문서별 블록 수, 경고, 엔진 정보, 소요 시간
├── reports/clean.json              단계별 폐기 사유 집계
└── dataset/                        최종 데이터셋 + stats.json + dataset_card.md
```

무엇이 왜 사라졌는지 확인하려면 `out/reports/clean.json`을 보십시오. 폐기 사유가
블록·페이지·문서 단위로 모두 세어져 있습니다.

### 샘플 5개를 돌린 결과

`make run` 한 번(4코어 CPU, 약 40분)으로 나온 수치입니다.

| 원본 | 쪽 | 추출 문자 | 청크 | SFT |
| --- | --- | --- | --- | --- |
| `no-copy.pdf` | 147 | 42,401 | 107 | 51 |
| `story1.pdf` | 290 | 249,716 | 132 | 200 |
| `science1.pdf` | 199 | 201,368 | 124 | 200 |
| `qt-prog.docx` | - | 233,566 | 96 | 200 |
| `13.DOC` | - | 6,951 | 3 | 4 |

합계 **462개 청크 / 379,735 토큰**(Qwen2.5 토크나이저), **SFT 637개**
(제목 240 · 이어쓰기 152 · 정의 QA 118 · 수식 101 · 표 26).
문자 구성은 한글 62.9%, 라틴 37.1%, 한자·가나 0.0%입니다. 한자·가나가 0이라는
것이 중요합니다. 텍스트 레이어를 읽었다면 `no-copy.pdf` 한 권만으로 55.9%가
한자로 들어왔을 것입니다.

---

## 테스트

```bash
make test    # 392개, 5초, 모델 가중치·tesseract·LibreOffice 없이 실행됨
make lint
```

DOCX 테스트는 OOXML을 손으로 조립하고, 수식 테스트는 합성 이미지에 잉크 띠를
그려 넣습니다. 그래서 네트워크와 외부 바이너리 없이 전체 로직을 검증합니다.

---

## 한계

- OCR 기반이므로 오탈자가 남습니다. `out/work/pages/`의 페이지 이미지와
  `interim/markdown/`의 결과를 나란히 놓고 표본 검수하는 것을 권합니다.
- 수식/표 LaTeX는 인식 모델의 출력입니다. 괄호 균형 등 기본 검증만 통과한
  상태이므로 원본과 다를 수 있습니다.
- HWP/HWPX는 아직 추출기가 없습니다. 발견하면 건너뛰고 경고를 남깁니다.
- 학습에 쓰기 전에 원본 문서의 저작권·이용 조건을 확인하십시오.
