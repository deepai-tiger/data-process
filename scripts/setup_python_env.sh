#!/usr/bin/env bash
# Create .venv and install the pipeline with CPU-only torch.
# Usage: scripts/setup_python_env.sh [--gpu]
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"
if [ ! -d .venv ]; then
  "$PYTHON" -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip wheel

if [ "${1:-}" = "--gpu" ]; then
  echo "installing CUDA torch"
  pip install torch torchvision
else
  echo "installing CPU-only torch (use --gpu on a CUDA machine)"
  pip install -r requirements-torch-cpu.txt
fi

pip install -r requirements.txt
# optional model-backed extras: Korean spacing repair + equation recognition
pip install kiwipiepy==0.22.2 pix2tex==0.1.4
pip install -e .

echo
kdp doctor || true
