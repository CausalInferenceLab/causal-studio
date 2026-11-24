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

If the user asks to try the pipeline and `videos/binary-search/project.toml` exists, render the supplied example and return the resulting MP4.

```bash
.venv-video/bin/python video.py render videos/binary-search
```

In a skill-only checkout, initialize a new topic and build a short first scene using the steps below. If the user asks for a demo without a topic, use binary search as the brief.

## Start or resume a project

```bash
.venv-video/bin/python video.py init videos/my-topic --brief "Explain binary search to a beginner"
.venv-video/bin/python video.py init videos/my-topic --source path/to/lesson.ipynb
```

Choose one input. `--source` accepts Markdown, plain text, or an existing notebook. A short prompt can serve as the entire brief. Generate a notebook only when the user requests one. If the project already exists, read its `project.toml`; it records the source and default Manim class relative to the topic folder. The `source` command prints the lesson, including notebook code cells as text. It never executes notebook cells.

Use `videos/<topic>/scene_plan.md` for the scene plan, `scenes/` for Manim files, `narration/` for scripts, and `build/` for generated files. Give each scene one Python file and one script with the same scene number. Put colors, icons, or graph helpers used by several scenes in a shared module within that topic. Use the manifest and existing paths when revising a project. Read `references/causal-studio.md` when it exists and you are editing a Causal Studio scene.

## Choose how to show the idea

When planning a math or statistics video or reworking how an idea is shown, study a relevant 3Blue1Brown lesson or source scene before writing Manim code. Choose a technique that helps explain this topic, such as moving existing objects into a graph or changing a distribution on fixed axes. Record the reference and the planned on-screen action in `scene_plan.md`. Use Tabler SVG icons when a repeated entity, such as a visitor or a click, is easier to recognize as a symbol. See [visual design and icons](references/manim-code-patterns.md#visual-design-and-icons) for sources and examples.

Keep the explanation in motion and narration. Plan one visual change the viewer should notice per beat. Use on-screen text for the quantities, units, or short labels needed to interpret that change. Leave out recurring headers and sentences that repeat the narration. For a narrated video, prefer selectable subtitles when captions are needed. For a silent video, include the short cues needed to follow it without audio. See [staging and text](references/manim-code-patterns.md#staging-and-text).

## Work one scene at a time

1. Read the source and locate the smallest coherent teaching unit. Preserve the source's numbers, definitions, observed and unobserved values, and examples. Check the prior scene's last line and the new scene's first line when continuing a series.
2. Fill a plan row for each beat with the narration cue, what the viewer sees change, what stays or leaves, and the exact labels that appear. For narration, use one short paragraph per beat, separated by a blank line. Read the [narration guide](references/script-writing-guide.md).
3. For a narrated scene, review the narration, then generate the MP3 and its adjacent `*.timings.json`. Read and listen to both before locking animation timing. For a silent preview, use provisional beat lengths. See [narration and sync](references/narration-sync.md).
4. Read the [Manim code patterns](references/manim-code-patterns.md) before writing code. Give the visual idea most of the frame, keep its colors and geometry stable across related beats, and reserve clearance where captions may appear. Clear obsolete objects before shrinking any labels.
5. Render a preview and inspect frames before, during, and after each key change. Check that the intended change is visible at phone size, with the sound off, and that labels stay legible throughout the motion. With sound on, check the cue and the hold on the result. Check continuity across cuts in the assembled video.

```bash
.venv-video/bin/python video.py render videos/my-topic
```

To render a different scene in isolation, select its file and class.

```bash
.venv-video/bin/python video.py render videos/my-topic \
  --file videos/my-topic/scenes/scene_02.py --scene Scene02
```

For narrated output, connect each measured chunk to its matching Manim beat. Put the animation on the key phrase, leave enough reading time, and keep at least 0.5 seconds of visual tail after the audio. For existing scenes with hand-tuned waits, review those waits against the new timeline before changing them. Finish with the commands in [FFmpeg recipes](references/ffmpeg-recipes.md).
