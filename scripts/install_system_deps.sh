#!/usr/bin/env bash
# System packages required by the pipeline (Debian/Ubuntu).
#
#   tesseract-ocr{,-kor,-eng} : OCR engine used on page images
#   libreoffice-writer        : legacy .doc/.rtf -> .docx conversion
#   poppler-utils             : pdftoppm, handy as a rasterizer fallback
#   fonts-nanum               : Korean fonts, so rendered page images are legible
set -euo pipefail

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  SUDO="sudo"
fi

$SUDO apt-get update
$SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  tesseract-ocr \
  tesseract-ocr-kor \
  tesseract-ocr-eng \
  libreoffice-writer \
  poppler-utils \
  fonts-nanum \
  python3-venv \
  python3-pip

echo
echo "installed:"
tesseract --version | head -1
tesseract --list-langs | tail -n +2 | tr '\n' ' '
echo
soffice --version | head -1
