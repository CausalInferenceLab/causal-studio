#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECK_ONLY=false
case "${1:-}" in
  "") ;;
  --check) CHECK_ONLY=true ;;
  --help|-h)
    echo "Usage: bash scripts/setup_video_assets.sh [--check]"
    exit 0 ;;
  *) echo "Unknown option: $1" >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then
  echo "Too many arguments" >&2
  exit 2
fi

REPOS=("https://github.com/3b1b/videos.git" "https://github.com/tabler/tabler-icons.git")
DESTS=("$ROOT_DIR/3b1b" "$ROOT_DIR/videos/assets/tabler-icons")
REQUIRED=("_2020/covid.py" "icons/outline/device-tablet.svg")

# A directory inside the parent repository is not necessarily an asset clone.
# Check all existing destinations before cloning or updating either asset.
for dest in "${DESTS[@]}"; do
  if [ -e "$dest" ]; then
    if [ ! -e "$dest/.git" ] || ! git -C "$dest" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      echo "Invalid asset repository: $dest. Inspect or move it before retrying." >&2
      exit 1
    fi
  fi
done

for i in "${!DESTS[@]}"; do
  dest="${DESTS[$i]}"
  if ! "$CHECK_ONLY"; then
    if [ -e "$dest/.git" ]; then
      echo "[update] $dest"
      git -C "$dest" pull --ff-only
    else
      mkdir -p "$(dirname "$dest")"
      echo "[clone] ${REPOS[$i]} -> $dest"
      git clone --depth 1 "${REPOS[$i]}" "$dest"
    fi
  fi
  if [ ! -f "$dest/${REQUIRED[$i]}" ]; then
    echo "Missing required asset: $dest/${REQUIRED[$i]}" >&2
    exit 1
  fi
  echo "[ok] $dest/${REQUIRED[$i]}"
done

echo "ready: 3b1b/ + videos/assets/tabler-icons/"
