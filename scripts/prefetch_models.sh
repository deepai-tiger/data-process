#!/usr/bin/env bash
# Download every model weight the pipeline needs, so later runs work offline.
#
#   docling layout (heron)        ~165 MB
#   docling TableFormer           ~340 MB
#   pix2tex LaTeX-OCR             ~120 MB
#   kiwipiepy Korean LM            ~40 MB
#   docling CodeFormulaV2         ~610 MB  (only with --formula-vlm)
set -euo pipefail

cd "$(dirname "$0")/.."
# shellcheck disable=SC1091
[ -d .venv ] && source .venv/bin/activate

WITH_VLM=""
[ "${1:-}" = "--formula-vlm" ] && WITH_VLM="1"

python - "$WITH_VLM" <<'PY'
import sys

with_vlm = bool(sys.argv[1])

from docling.utils.model_downloader import download_models

print("downloading docling models ...")
download_models(with_layout=True, with_tableformer=True, with_code_formula=with_vlm)

print("downloading pix2tex weights ...")
try:
    from pix2tex.cli import LatexOCR

    LatexOCR()
except Exception as exc:  # pragma: no cover
    print(f"  skipped: {exc}")

print("downloading kiwipiepy model ...")
try:
    from kiwipiepy import Kiwi

    Kiwi().space("띄어쓰기 준비")
except Exception as exc:  # pragma: no cover
    print(f"  skipped: {exc}")

print("done")
PY
