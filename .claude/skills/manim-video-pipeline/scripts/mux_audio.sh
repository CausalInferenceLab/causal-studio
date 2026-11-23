#!/bin/bash
# Mux video and audio files together
# This script does not read *.timings.json or retime scenes.
# Use it only after the scene render has already been adjusted to the mp3 timing.
# Usage: ./mux_audio.sh <video.mp4> <audio.mp3> <output.mp4> [--shortest]
# Example: ./mux_audio.sh preview/code/01_scene_code.mp4 build/audio/01_scene.mp3 preview/mux/01_scene_mux.mp4

VIDEO="$1"
AUDIO="$2"
OUTPUT="$3"
MODE="${4:---full}"

if [ -z "$VIDEO" ] || [ -z "$AUDIO" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <video.mp4> <audio.mp3> <output.mp4> [--shortest|--full]"
    echo "  --shortest: Cut to shorter of video/audio (default)"
    echo "  --full: Keep full video, audio may be shorter"
    exit 1
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT")"

# Get durations for info
VIDEO_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO")
AUDIO_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$AUDIO")

echo "Video duration: ${VIDEO_DUR}s"
echo "Audio duration: ${AUDIO_DUR}s"

if [ "$MODE" = "--shortest" ]; then
    ffmpeg -y -i "$VIDEO" -i "$AUDIO" \
        -c:v copy -c:a aac \
        -map 0:v:0 -map 1:a:0 \
        -shortest \
        "$OUTPUT"
else
    ffmpeg -y -i "$VIDEO" -i "$AUDIO" \
        -c:v copy -c:a aac \
        -map 0:v:0 -map 1:a:0 \
        "$OUTPUT"
fi

echo "Output: $OUTPUT"
OUTPUT_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$OUTPUT")
echo "Output duration: ${OUTPUT_DUR}s"
