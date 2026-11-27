# Assemble existing scenes

Use for an edit made from existing rendered scenes and narration. Confirm the requested playback order and output settings. Read the successful render paths and corresponding MP3s with adjacent timing files. Pass a silent scene as a video path alone.

```bash
.venv-video/bin/python video.py package \
  --scene "$SCENE_1_MP4" videos/my_topic/en/build/audio/01_intro.mp3 \
  --scene "$SCENE_2_MP4" videos/my_topic/en/build/audio/02_comparison.mp3 \
  --output videos/my_topic/en/build/final/my_topic.mp4 --thumbnail-at 8.5
```

The command returns an MP4, a thumbnail PNG, and an SRT when there is timed narration. `--thumbnail-at` uses time in the full edit and defaults to its midpoint. Inspect continuity across cuts, keep caption space clear, and check the actual runtime, playback, and audio sync. Use the [review playbook](review.md) as needed. Assemble with the existing inputs for a package-only request and identify missing inputs before scheduling production work. See [FFmpeg recipes](../references/ffmpeg-recipes.md) for optional sound mixing and subtitle embedding.
