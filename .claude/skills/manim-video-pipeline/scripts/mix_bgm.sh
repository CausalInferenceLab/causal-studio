#!/bin/bash
# Mix background music into a final video while keeping narration intelligible.
# Usage:
#   ./mix_bgm.sh <video.mp4> <bgm_audio> <output.mp4> [--bgm-volume 0.12] [--voice-gain 1.0]

set -euo pipefail

VIDEO="${1:-}"
BGM="${2:-}"
OUTPUT="${3:-}"
shift $(( $# >= 3 ? 3 : $# ))

BGM_VOLUME="0.12"
VOICE_GAIN="1.0"

while [ "$#" -gt 0 ]; do
    case "$1" in
        --bgm-volume)
            BGM_VOLUME="$2"
            shift 2
            ;;
        --voice-gain)
            VOICE_GAIN="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

if [ -z "$VIDEO" ] || [ -z "$BGM" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <video.mp4> <bgm_audio> <output.mp4> [--bgm-volume 0.12] [--voice-gain 1.0]"
    exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"

VIDEO_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO")
BGM_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$BGM")

echo "Video duration: ${VIDEO_DUR}s"
echo "BGM duration: ${BGM_DUR}s"
echo "BGM volume: ${BGM_VOLUME}"
echo "Voice gain: ${VOICE_GAIN}"

ffmpeg -y \
    -i "$VIDEO" \
    -stream_loop -1 -i "$BGM" \
    -filter_complex "[0:a]volume=${VOICE_GAIN}[voice];[1:a]volume=${BGM_VOLUME}[bgm];[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[mix]" \
    -map 0:v:0 -map "[mix]" \
    -c:v copy -c:a aac -shortest \
    "$OUTPUT"

echo "Output: $OUTPUT"
OUTPUT_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT")
echo "Output duration: ${OUTPUT_DUR}s"
