---
name: manim-video-pipeline
description: Design and render educational videos in Manim Community Edition from a brief, lesson, or optional notebook. Use for 3Blue1Brown reference study, visual storyboards, animation prototypes, OpenAI or ElevenLabs narration, and final renders.
---

# Manim video pipeline

Use this workflow from the repository root when a user asks in natural language to make or edit a video. Execute the setup, project creation, and render steps with your tools. Return the MP4 path and summarize the visual idea, including the reference moment you adapted and any viewing limitations. Ask the user only for input or setup you cannot supply, such as their lesson or chosen voice provider credentials.

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

In a skill-only checkout, initialize a topic and follow the design steps below. For a demo without a topic, use binary search as the brief.

## Start or resume a project

```bash
.venv-video/bin/python video.py init videos/my-topic --brief "Explain binary search to a beginner"
.venv-video/bin/python video.py init videos/my-topic --source path/to/lesson.ipynb
```

Choose one input. `--source` accepts Markdown, plain text, or an existing notebook. A short prompt can serve as the entire brief. Generate a notebook only when the user requests one. If the project already exists, read its `project.toml`; it records the source and default Manim class relative to the topic folder. The `source` command prints the lesson, including notebook code cells as text. It never executes notebook cells.

Use `videos/<topic>/scene_plan.md` for the scene plan, `scenes/` for Manim files, `narration/` for scripts, and `build/` for generated files. Give each scene one Python file and one script with the same scene number. Put colors, icons, or graph helpers used by several scenes in a shared module within that topic. Use the manifest and existing paths when revising a project. Read `references/causal-studio.md` when it exists and you are editing a Causal Studio scene.

For multilingual videos, use `videos/<topic>/<language>/` as the project folder. Each language has its own `project.toml`, `scenes/`, `narration/`, and `build/`. Match scene and script names across languages. Keep reusable graphics in the topic's `shared/` folder. Pass the language folder to the same commands, for example `video.py render videos/my-topic/en`.

## Choose how to show the idea

When designing or revising a visual explanation, prepare the local source and SVG assets in both the full repo and a fresh skill-only checkout.

```bash
bash scripts/setup_video_assets.sh --ensure
```

1. **Find the visual question.** Write what a first-time viewer should understand by the end. Pick one concrete example or contrast that makes that insight visible. Sketch the opening state, the change, and the result. For an existing project, use the [scene plan template](templates/scene_plan.md) to fill gaps in its plan.
2. **Study the whole 3Blue1Brown passage and its source.** Search for a sequence that explains the same kind of relationship. Watch the setup, the key change, and how the result is framed and held. Record what draws the eye in those frames, how the layout evolves, and what the background, accent colors, and text are doing. Follow the official lesson's source link or search `3b1b/` for the scene, then trace the helpers that set the layout, camera, and palette as well as the animation. Save the video range and code permalinks in `scene_plan.md`. If playback fails, try another sequence or official lesson visuals and record what you inspected. If asset setup fails, use the upstream source. Follow [reference study and adaptation](references/manim-code-patterns.md#reference-study-and-adaptation).
3. **Set the visual direction and storyboard.** Choose the first focal point, the space supporting labels and diagrams need, and the color roles and text hierarchy that will carry across scenes. Mark where the composition needs to change to make the next idea visible. Carry an object or relationship from one beat to the next, and let a concrete example produce its result before introducing the general rule. Map each action to a narration cue or the corresponding cue in a silent video.
4. **Prototype a complete teaching passage.** Render the setup, hardest transition, and result with provisional timing and the planned colors and layout. Compare those frames with the reference and play the passage muted at phone width and normal speed. Check where the eye lands first, what stays legible during the change, and whether the result reads clearly. Fix the first point where attention or understanding breaks, rerender it, and note the revision before full production. Follow [the visual review guide](references/manim-code-patterns.md#review-the-motion).

## Work one scene at a time

1. Read the source and locate the smallest coherent teaching unit. Preserve the source's numbers, definitions, observed and unobserved values, and examples. Check the prior scene's last line and the new scene's first line when continuing a series.
2. Map each planned beat to the final words and labels. For narration, use one short paragraph per beat, separated by a blank line. Read the [narration guide](references/script-writing-guide.md).
3. For a narrated scene, review the narration, then generate the MP3 and its adjacent `*.timings.json`. Read and listen to both before locking animation timing. For a silent preview, use provisional beat lengths. See [narration and sync](references/narration-sync.md).
4. Read the [Manim code patterns](references/manim-code-patterns.md) before writing code. Give the visual idea most of the frame, keep its colors and geometry stable across related beats, and reserve clearance where captions may appear. Clear obsolete objects before shrinking any labels.
5. Review the assembled preview at normal speed with the narration when present. Check whether each visual event lands on the words that give it meaning and whether the result stays long enough to read. At each cut, verify that shared objects, positions, and colors still make sense. Use selectable subtitles for narrated videos when captions are needed and short on-screen cues for silent videos.

```bash
.venv-video/bin/python video.py render videos/my-topic
```

To render a different scene in isolation, select its file and class.

```bash
.venv-video/bin/python video.py render videos/my-topic \
  --file videos/my-topic/scenes/scene_02.py --scene Scene02
```

For narrated output, connect each measured chunk to its matching Manim beat. Put the animation on the key phrase, leave enough reading time, and keep at least 0.5 seconds of visual tail after the audio. For existing scenes with hand-tuned waits, review those waits against the new timeline before changing them. Finish with the commands in [FFmpeg recipes](references/ffmpeg-recipes.md).
