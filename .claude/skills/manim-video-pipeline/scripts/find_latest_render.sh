#!/bin/bash
# Find the latest rendered mp4 file in build/manim/videos/
# Usage: ./find_latest_render.sh [search_dir] [scene_pattern]
# Example: ./find_latest_render.sh build/manim/videos Scene01

SEARCH_DIR="${1:-build/manim/videos}"
PATTERN="${2:-}"

if [ -n "$PATTERN" ]; then
    # Search with pattern
    find "$SEARCH_DIR" -name "*.mp4" -path "*${PATTERN}*" -type f -print0 2>/dev/null | \
        xargs -0 ls -t 2>/dev/null | head -1
else
    # Find most recent mp4
    find "$SEARCH_DIR" -name "*.mp4" -type f -print0 2>/dev/null | \
        xargs -0 ls -t 2>/dev/null | head -1
fi
