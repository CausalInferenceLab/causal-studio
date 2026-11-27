# Work on captions only

Use for an SRT draft, a wording or timing edit, or a subtitle export from an existing cut. Deliver a timestamped SRT. Read the existing video, captions or transcript, and available timing data as inputs. Keep the video, audio, and scene code intact.

1. When a matching SRT exists, edit its requested wording or cues. Keep unaffected text and timing. To extract the first embedded text track, run `ffmpeg -i "$VIDEO" -map 0:s:0 extracted.srt`. Select the requested track if there are several.
2. To generate an SRT from rendered scenes and measured narration, use `video.py captions`. List the same scene files in the same order as the cut. Include silent scenes as video-only entries so later cues keep their offsets. Each MP3 needs adjacent `*.timings.json`. This command only probes existing media and writes an SRT. Use a supported Python interpreter and FFprobe.
3. If you have only a final video and a transcript, use its existing audio to establish cue timings. Report any alignment limits.
4. Check the captions against playback, keeping cues short, in order, and clear of drawings. The command splits captions into at most two lines and estimates cue boundaries within each measured beat. Fine-tune the boundaries by listening when needed.

```bash
python3 video.py captions \
  --scene "$OPENING_MP4" \
  --scene "$SCENE_MP4" videos/my_topic/en/build/audio/02_comparison.mp3 \
  --output videos/my_topic/en/build/final/my_topic.srt
```

A captions-only request ends with the SRT. Attaching or burning it into a video requires a request for a new video file.
