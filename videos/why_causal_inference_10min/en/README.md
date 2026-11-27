# Why Causal Inference? · 10-minute edition

This seven-scene English lesson follows the tablet decision from the [course notebook](../../../book/why_causal_inference/why_causal_inference_en.ipynb). The [scene plan](scene_plan.md) lists the chapters, source cells, and original edit times. In `narration/` and `scenes/`, matching numbers identify each chapter's script and Manim code.

From the repository root, prepare the video environment and Tabler icons, then render the opening chapter.

```bash
bash scripts/setup_environment.sh --video-only
bash scripts/setup_video_assets.sh --ensure
.venv-video/bin/python video.py render videos/why_causal_inference_10min/en --scene Scene01
```

To make a narrated version, use the [narration guide](../../../.claude/skills/manim-video-pipeline/references/narration-sync.md) to record each script into `build/audio/` before rendering its scene. The scenes read their matching timing files when present. The original edit used ElevenLabs. A new voice or delivery can change the runtime.
