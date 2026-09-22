PY := .venv/bin/python
KDP := .venv/bin/kdp

.PHONY: help setup system-deps prefetch doctor extract clean-stage build run demo test lint clean-out

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

system-deps: ## Install OS packages (tesseract+kor, libreoffice, poppler)
	bash scripts/install_system_deps.sh

setup: ## Create .venv and install the pipeline (CPU torch)
	bash scripts/setup_python_env.sh

prefetch: ## Download model weights for offline runs
	bash scripts/prefetch_models.sh

doctor: ## Check dependencies
	$(KDP) doctor

extract: ## Stage 1: raw/ -> out/interim/docjson
	$(KDP) extract

clean-stage: ## Stage 2: normalize/filter/dedup -> out/interim/clean
	$(KDP) clean

build: ## Stage 3: chunk + SFT + JSONL/Parquet -> out/dataset
	$(KDP) build

run: ## All three stages over raw/
	$(KDP) run

demo: ## Small end-to-end demo (first 6 pages of each PDF)
	$(KDP) run --max-pages 6 --log-level INFO

test: ## Unit tests (no model downloads required)
	.venv/bin/pytest -q

lint: ## Byte-compile every module as a syntax check
	$(PY) -m compileall -q src/kdp

clean-out: ## Delete generated output (keeps the page-image cache)
	rm -rf out/dataset out/interim out/reports
