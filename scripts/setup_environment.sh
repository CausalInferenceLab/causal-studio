#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE=full
CHECK_ONLY=false

for arg in "$@"; do
  case "$arg" in
    --book-only|--video-only)
      if [ "$MODE" != full ] && [ "$MODE" != "${arg#--}" ]; then
        echo "Choose only one of --book-only and --video-only." >&2
        exit 2
      fi
      MODE="${arg#--}" ;;
    --check) CHECK_ONLY=true ;;
    --help|-h)
      echo "Usage: bash scripts/setup_environment.sh [--book-only | --video-only] [--check]"
      echo "Default: prepare .venv, full requirements, and both local video assets."
      echo "--book-only: use requirements-book.txt and skip video assets."
      echo "--video-only: prepare .venv-video with requirements-video.txt for Manim previews."
      echo "--check: validate the selected environment without installing or updating."
      exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

cd "$ROOT_DIR"
VENV=.venv
REQUIREMENTS=requirements.txt
if [ "$MODE" = video-only ]; then
  VENV=.venv-video
  REQUIREMENTS=requirements-video.txt
  PYTHON_VERSIONS="3.11 3.12"
  DEFAULT_PYTHON=python3.11
  if ! command -v "$DEFAULT_PYTHON" >/dev/null 2>&1; then
    DEFAULT_PYTHON=python3.12
  fi
else
  PYTHON_VERSIONS="$(awk -F '"' '/^[[:space:]]*python_version[[:space:]]*=/ {print $2; exit}' Pipfile)"
  if [ -z "$PYTHON_VERSIONS" ]; then
    echo "Missing python_version in Pipfile" >&2
    exit 1
  fi
  DEFAULT_PYTHON="python${PYTHON_VERSIONS}"
  if [ "$MODE" = book-only ]; then
    REQUIREMENTS=requirements-book.txt
  fi
fi

check_python() {
  "$1" -c 'import sys; version = ".".join(map(str, sys.version_info[:2])); sys.exit(0 if version in sys.argv[1].split() else f"Python {version} is unsupported here. Use one of {sys.argv[1]}.")' "$PYTHON_VERSIONS"
}

if [ ! -x "$VENV/bin/python" ]; then
  if "$CHECK_ONLY" || [ -e "$VENV" ]; then
    echo "Missing or unusable $VENV/bin/python; no existing environment was replaced." >&2
    exit 1
  fi
  SETUP_PYTHON="${PYTHON_BIN:-$DEFAULT_PYTHON}"
  if ! command -v "$SETUP_PYTHON" >/dev/null 2>&1; then
    echo "Install a supported Python version ($PYTHON_VERSIONS), or set PYTHON_BIN to its executable." >&2
    exit 1
  fi
  check_python "$SETUP_PYTHON"
  "$SETUP_PYTHON" -m venv "$VENV"
fi

check_python "$VENV/bin/python"
if ! "$CHECK_ONLY"; then
  "$VENV/bin/python" -m pip install -r "$REQUIREMENTS"
fi
"$VENV/bin/python" -m pip check

# Check imports as well as metadata: native libraries can be missing even when
# pip reports a consistent dependency graph.
"$VENV/bin/python" - "$MODE" <<'PY'
import importlib
import sys

modules = [
    "jupyter_book", "numpy", "pandas", "scipy", "matplotlib", "seaborn",
    "sklearn", "statsmodels.api", "duckdb", "dowhy", "graphviz",
    "econml.dml", "sklift", "kagglehub",
]
if sys.argv[1] == "video-only":
    modules = ["manim"]
elif sys.argv[1] == "full":
    modules += [
        "jupyterlab", "manim", "linearmodels", "ipywidgets", "pypdf",
        "pdfplumber", "reportlab", "pdf2image", "pytesseract", "PIL",
    ]
for module in modules:
    importlib.import_module(module)
    print(f"[ok] import {module}", flush=True)
PY

if [ "$MODE" = full ]; then
  if "$CHECK_ONLY"; then
    bash scripts/setup_video_assets.sh --check
  else
    bash scripts/setup_video_assets.sh
  fi
fi

"$VENV/bin/python" --version
"$VENV/bin/python" -m pip --version
case "$MODE" in
  book-only) echo "ready: book-only Python environment (video assets excluded by --book-only)" ;;
  video-only) echo "ready: video-only Python environment (.venv-video)" ;;
  full) echo "ready: full Python environment + 3b1b/ + videos/assets/tabler-icons/" ;;
esac
