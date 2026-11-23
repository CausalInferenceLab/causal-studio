#!/bin/bash
# Mix background music into a final video while keeping narration intelligible.
# Adds a fade-to-black ending and BGM tail so the video doesn't cut abruptly.
#
# Usage:
#   ./mix_bgm.sh <video.mp4> <bgm_audio> <output.mp4> [options]
#
# Options:
#   --bgm-volume 0.10    BGM volume relative to narration (default 0.12)
#   --voice-gain 1.0     Narration volume gain (default 1.0)
#   --video-fade 1.5     Seconds of fade-to-black at end of content (default 1.5)
#   --bgm-tail 3.0       Seconds of black screen + BGM after content ends (default 3.0)
#   --bgm-fade 3.0       Seconds of BGM fade-out at the very end (default 3.0)
#
# Output duration = VIDEO_DUR + bgm-tail
# The last (bgm-tail) seconds are black with BGM only, then BGM fades to silence.

set -euo pipefail

VIDEO="${1:-}"
BGM="${2:-}"
OUTPUT="${3:-}"
shift $(( $# >= 3 ? 3 : $# ))

BGM_VOLUME="0.12"
VOICE_GAIN="1.0"
VIDEO_FADE="1.5"
BGM_TAIL="3.0"
BGM_FADE="3.0"

while [ "$#" -gt 0 ]; do
    case "$1" in
        --bgm-volume)  BGM_VOLUME="$2"; shift 2 ;;
        --voice-gain)  VOICE_GAIN="$2"; shift 2 ;;
        --video-fade)  VIDEO_FADE="$2"; shift 2 ;;
        --bgm-tail)    BGM_TAIL="$2";   shift 2 ;;
        --bgm-fade)    BGM_FADE="$2";   shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

if [ -z "$VIDEO" ] || [ -z "$BGM" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <video.mp4> <bgm_audio> <output.mp4> [options]"
    echo "  --bgm-volume FLOAT  (default 0.12)"
    echo "  --voice-gain FLOAT  (default 1.0)"
    echo "  --video-fade SECS   fade-to-black at end of content (default 1.5)"
    echo "  --bgm-tail   SECS   black screen + BGM after content (default 3.0)"
    echo "  --bgm-fade   SECS   BGM fade-out duration at very end (default 3.0)"
    exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"

VIDEO_DUR=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$VIDEO")

TOTAL_DUR=$(python3 -c "print(${VIDEO_DUR} + ${BGM_TAIL})")
VIDEO_FADE_ST=$(python3 -c "print(max(0, ${VIDEO_DUR} - ${VIDEO_FADE}))")
BGM_FADE_ST=$(python3 -c "print(max(0, ${TOTAL_DUR} - ${BGM_FADE}))")

echo "Video duration   : ${VIDEO_DUR}s"
echo "Total duration   : ${TOTAL_DUR}s  (tail: ${BGM_TAIL}s)"
echo "Video fade-to-blk: ${VIDEO_FADE}s (starts at ${VIDEO_FADE_ST}s)"
echo "BGM fade-out     : ${BGM_FADE}s   (starts at ${BGM_FADE_ST}s)"
echo "BGM volume       : ${BGM_VOLUME}"
echo "Voice gain       : ${VOICE_GAIN}"

# filter_complex 설명:
#   [vpad]  : 컨텐츠 마지막을 fade-to-black 후 black tail 추가
#   [voice] : 나레이션에 gain 적용 + black tail 구간을 무음으로 패딩
#   [bgm]   : BGM을 TOTAL_DUR만큼 루프 후 마지막 BGM_FADE동안 fade-out
#   [mix]   : voice + bgm 믹스
ffmpeg -y \
    -i "$VIDEO" \
    -stream_loop -1 -i "$BGM" \
    -filter_complex "
        [0:v]fade=t=out:st=${VIDEO_FADE_ST}:d=${VIDEO_FADE},
             tpad=stop_mode=clone:stop_duration=${BGM_TAIL}[vpad];
        [0:a]volume=${VOICE_GAIN},apad=pad_dur=${BGM_TAIL}[voice];
        [1:a]volume=${BGM_VOLUME},
             atrim=duration=${TOTAL_DUR},
             afade=t=out:st=${BGM_FADE_ST}:d=${BGM_FADE}[bgm];
        [voice][bgm]amix=inputs=2:duration=longest:dropout_transition=2[mix]
    " \
    -map "[vpad]" -map "[mix]" \
    -t "${TOTAL_DUR}" \
    -c:v libx264 -preset fast -crf 18 \
    -c:a aac \
    "$OUTPUT"

echo "Output: $OUTPUT"
OUTPUT_DUR=$(ffprobe -v error -show_entries format=duration \
    -of default=noprint_wrappers=1:nokey=1 "$OUTPUT")
echo "Output duration: ${OUTPUT_DUR}s"
