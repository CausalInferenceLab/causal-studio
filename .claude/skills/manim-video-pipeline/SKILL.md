---
name: manim-video-pipeline
description: Design and render Manim Community Edition educational videos in any domain from a short brief, Markdown, text, or an optional Jupyter notebook. Use for scene planning, narration, OpenAI or ElevenLabs TTS, layout and caption checks, audio timing, rendering, and muxing.
---

# Manim video pipeline

Use this workflow from the repository root when a user asks in natural language to make or edit a video. Execute the setup, project creation, and render steps with your tools. Return the preview MP4 path and a brief summary of the scene. Ask the user only for input or setup you cannot supply, such as their lesson or chosen voice provider credentials.

## Prepare the preview environment

For the demo or a standalone video, check the video-only environment. Set it up if missing, then use its interpreter for the commands below.

```bash
bash scripts/setup_environment.sh --video-only --check
# Run this when the video-only environment needs setup:
bash scripts/setup_environment.sh --video-only
```

Use `.venv-video/bin/python` for the demo and standalone projects. For an existing Causal Studio scene with additional datasets or assets, use the project's environment with those dependencies and check the scene's imports and asset paths. Python 3.11 or 3.12 and Manim CE are sufficient for the demo. Narration and muxing also need FFmpeg/ffprobe.

If the user asks to try the pipeline or see the demo, render the supplied example and return the resulting MP4.

```bash
.venv-video/bin/python video.py render videos/binary-search
```

## Start or resume a project

```bash
.venv-video/bin/python video.py init videos/my-topic --brief "Explain binary search to a beginner"
.venv-video/bin/python video.py init videos/my-topic --source path/to/lesson.ipynb
```

Choose one input. `--source` accepts Markdown, plain text, or an existing notebook. A short prompt can serve as the entire brief. Generate a notebook only when the user requests one. If the project already exists, read its `project.toml`; it records the source and default Manim class relative to the topic folder. The `source` command prints the lesson, including notebook code cells as text. It never executes notebook cells.

Use `videos/<topic>/scene_plan.md` for the scene plan, `scenes/` for Manim files, `narration/` for one text file per scene, and `build/` for previews and generated audio. If the existing files live under `src/`, use their paths from the manifest. Project-specific guidance is in [Causal Studio projects](references/causal-studio.md).

## Work one scene at a time

1. Read the source and locate the smallest coherent teaching unit. Preserve the source's numbers, definitions, observed and unobserved values, and examples. Check the prior scene's last line and the new scene's first line when continuing a series.
2. Fill a plan row for each beat with the narration cue, on-screen action, what disappears, and where the focal object and captions sit. Use one focal idea per beat. For narration, use one short paragraph per beat, separated by a blank line. Read the [narration guide](references/script-writing-guide.md).
3. For a narrated scene, review the narration, then generate the MP3 and its adjacent `*.timings.json`. Read and listen to both before locking animation timing. For a silent preview, use provisional beat lengths. See [narration and sync](references/narration-sync.md).
4. Read the [Manim code patterns](references/manim-code-patterns.md) before writing code. Reserve a dedicated caption strip, size the body to its own region, and check the rendered bounding boxes. Keep palette meaning consistent. Split crowded beats and remove obsolete objects before moving or shrinking the rest. Use 3Blue1Brown clips or Tabler icons as optional references when relevant.
5. Render low quality and inspect frames at entrances, exits, and dense moments. Verify physical overlaps, spacing, focal point, readability, then timing. A duration check alone does not catch a caption or graph covering another layer. Fix timing in the Scene before muxing.

```bash
.venv-video/bin/python video.py render videos/my-topic
```

For narrated output, connect each measured chunk to its matching Manim beat. Put the animation on the key phrase, leave enough reading time, and keep at least 0.5 seconds of visual tail after the audio. For existing scenes with hand-tuned waits, review those waits against the new timeline before changing them. Finish with the commands in [FFmpeg recipes](references/ffmpeg-recipes.md).

The [binary search example](../../../videos/binary-search/scene_plan.md) demonstrates the same scheme without a notebook, external assets, or an API key for its first preview.
