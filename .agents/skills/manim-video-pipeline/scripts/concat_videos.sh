#!/bin/bash
# Concatenate multiple mp4 files into one
# Usage: ./concat_videos.sh <input_dir> <output.mp4> [--reencode]
# Example: ./concat_videos.sh build/final/ build/final/topic_full.mp4

INPUT_DIR="$1"
OUTPUT="$2"
MODE="${3:-}"

if [ -z "$INPUT_DIR" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <input_dir> <output.mp4> [--reencode]"
    echo "  --reencode: Re-encode to normalize resolution/fps (use if direct concat fails)"
    exit 1
fi

# Create file list (sorted by filename)
FILELIST="/tmp/concat_filelist_$$.txt"

# Find all mp4 files — absolute paths so ffmpeg resolves correctly from /tmp/
ls "${INPUT_DIR}"/*_debug.mp4 "${INPUT_DIR}"/*.mp4 2>/dev/null | \
    sort -t'/' -k2 | uniq | \
    while read f; do
        echo "file '$(realpath "$f")'"
    done > "$FILELIST"

echo "Files to concatenate:"
cat "$FILELIST"
echo ""

# Count files
FILE_COUNT=$(wc -l < "$FILELIST")
echo "Total files: $FILE_COUNT"

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "Error: No mp4 files found in $INPUT_DIR"
    rm -f "$FILELIST"
    exit 1
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT")"

if [ "$MODE" = "--reencode" ]; then
    echo "Re-encoding to normalize resolution and framerate..."
    ffmpeg -y -f concat -safe 0 -i "$FILELIST" \
        -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p" \
        -c:v libx264 -preset medium -crf 23 \
        -c:a aac -b:a 128k \
        "$OUTPUT"
else
    echo "Attempting direct concat (no re-encoding)..."
    if ! ffmpeg -y -f concat -safe 0 -i "$FILELIST" -c copy "$OUTPUT" 2>/dev/null; then
        echo ""
        echo "Direct concat failed. Trying with re-encoding..."
        ffmpeg -y -f concat -safe 0 -i "$FILELIST" \
            -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p" \
            -c:v libx264 -preset medium -crf 23 \
            -c:a aac -b:a 128k \
            "$OUTPUT"
    fi
fi

# Cleanup
rm -f "$FILELIST"

# Show result
echo ""
echo "Output: $OUTPUT"
OUTPUT_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT")
echo "Total duration: ${OUTPUT_DUR}s"
