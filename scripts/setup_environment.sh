#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOK_ONLY=false
CHECK_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --book-only) BOOK_ONLY=true ;;
    --check) CHECK_ONLY=true ;;
    --help|-h)
      echo "Usage: bash scripts/setup_environment.sh [--book-only] [--check]"
      echo "Default: prepare .venv, full requirements, and both local video assets."
      echo "--book-only: use requirements-book.txt and skip video assets."
      echo "--check: validate the selected environment without installing or updating."
      exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

cd "$ROOT_DIR"
PYTHON_VERSION="$(awk -F '"' '/^[[:space:]]*python_version[[:space:]]*=/ {print $2; exit}' Pipfile)"
if [ -z "$PYTHON_VERSION" ]; then
  echo "Missing python_version in Pipfile" >&2
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  if "$CHECK_ONLY" || [ -e .venv ]; then
    echo "Missing or unusable .venv/bin/python; no existing environment was replaced." >&2
    exit 1
  fi
  SETUP_PYTHON="${PYTHON_BIN:-python${PYTHON_VERSION}}"
  if ! command -v "$SETUP_PYTHON" >/dev/null 2>&1; then
    echo "Install Python ${PYTHON_VERSION}, or set PYTHON_BIN to its executable." >&2
    exit 1
  fi
  "$SETUP_PYTHON" -c 'import sys; assert sys.version_info[:2] == tuple(map(int, sys.argv[1].split("."))), "Python version must match Pipfile"' "$PYTHON_VERSION"
  "$SETUP_PYTHON" -m venv .venv
fi

.venv/bin/python -c 'import sys; assert sys.version_info[:2] == tuple(map(int, sys.argv[1].split("."))), "Existing .venv Python version must match Pipfile"' "$PYTHON_VERSION"

REQUIREMENTS=requirements.txt
if "$BOOK_ONLY"; then
  REQUIREMENTS=requirements-book.txt
fi
if ! "$CHECK_ONLY"; then
  .venv/bin/python -m pip install -r "$REQUIREMENTS"
fi
.venv/bin/python -m pip check

# Check imports as well as metadata: native libraries can be missing even when
# pip reports a consistent dependency graph.
.venv/bin/python - "$BOOK_ONLY" <<'PY'
import importlib
import sys

modules = [
    "jupyter_book", "numpy", "pandas", "scipy", "matplotlib", "seaborn",
    "sklearn", "statsmodels.api", "duckdb", "dowhy", "graphviz",
    "econml.dml", "sklift", "kagglehub",
]
if sys.argv[1] == "false":
    modules += [
        "jupyterlab", "manim", "linearmodels", "ipywidgets", "pypdf",
        "pdfplumber", "reportlab", "pdf2image", "pytesseract", "PIL",
    ]
for module in modules:
    importlib.import_module(module)
    print(f"[ok] import {module}", flush=True)
PY

if ! "$BOOK_ONLY"; then
  if "$CHECK_ONLY"; then
    bash scripts/setup_video_assets.sh --check
  else
    bash scripts/setup_video_assets.sh
  fi
fi

.venv/bin/python --version
.venv/bin/python -m pip --version
if "$BOOK_ONLY"; then
  echo "ready: book-only Python environment (video assets excluded by --book-only)"
else
  echo "ready: full Python environment + 3b1b/ + videos/assets/tabler-icons/"
fi
