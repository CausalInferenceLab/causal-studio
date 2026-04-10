#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

clone_or_update() {
  local repo_url="$1"
  local dest_dir="$2"

  if [ -d "${dest_dir}/.git" ]; then
    echo "[update] ${dest_dir}"
    git -C "${dest_dir}" pull --ff-only
  elif [ -d "${dest_dir}" ]; then
    echo "[skip] ${dest_dir} exists but is not a git repo"
  else
    echo "[clone] ${repo_url} -> ${dest_dir}"
    git clone --depth 1 "${repo_url}" "${dest_dir}"
  fi
}

mkdir -p "${ROOT_DIR}/videos/assets"

clone_or_update "https://github.com/3b1b/videos.git" "${ROOT_DIR}/3b1b"
clone_or_update "https://github.com/tabler/tabler-icons.git" "${ROOT_DIR}/videos/assets/tabler-icons"

echo ""
echo "ready:"
echo "  ${ROOT_DIR}/3b1b"
echo "  ${ROOT_DIR}/videos/assets/tabler-icons"
