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

Use `.venv-video/bin/python` for the demo and standalone projects. For an existing Causal Studio scene with additional datasets or assets, use the project's environment with those dependencies and check the scene's imports and asset paths. Python 3.11 or 3.12 and Manim CE are sufficient for the demo. Narration, frame review, and publishing also need FFmpeg and ffprobe.

If the user asks to try the pipeline and `videos/binary_search/en/project.toml` exists, render the supplied example and return the resulting MP4.

```bash
.venv-video/bin/python video.py render videos/binary_search/en
```

In a skill-only checkout, initialize a topic and follow the design steps below. For a demo without a topic, use binary search as the brief.

## Start or resume a project

```bash
.venv-video/bin/python video.py init videos/my_topic --lang en --brief "Explain binary search to a beginner"
.venv-video/bin/python video.py init videos/my_topic --lang ko --source path/to/lesson.ipynb
```

Choose one input. `--source` accepts Markdown, plain text, or an existing notebook. A short prompt can serve as the entire brief. Generate a notebook only when the user requests one. If the project already exists, read its `project.toml` for the source path, the default scene file, and the Manim class. Paths in the manifest are relative to the language edition. The `source` command prints the lesson, including notebook code cells as text. It never executes notebook cells.

Use `videos/<topic_slug>/<language>/` for every video, including single-language videos. Use lowercase topic slugs with underscores, such as `binary_search`. Each edition has its own `project.toml`, `scene_plan.md`, `scenes/`, and optional `narration/`. Name each scene `scenes/scene_NN_name.py` and its script `narration/NN_name.txt`, with the same number and name across editions of the same scene. A silent scene can omit its script.

Keep reusable Python helpers in the topic's `shared/`, SVGs and images in topic or edition `assets/`, and thumbnails or production tools in `tools/`. Write audio, raw renders, and final MP4s under the edition's `build/audio/`, `build/manim/`, and `build/final/`. Pass the edition path to `video.py source`, `video.py render`, and `video.py check`. Before handing off a new or moved video, run `video.py check videos/my_topic/en` to catch missing plans, bad paths, and mismatched scene and narration names. Read `references/causal-studio.md` when working on an existing Causal Studio lesson.

## Choose how to show the idea

When designing or revising a visual explanation, prepare the local source and SVG assets in both the full repo and a fresh skill-only checkout.

```bash
bash scripts/setup_video_assets.sh --ensure
```

1. **Start with what the viewer sees.** Pick one concrete example and one visual subject that can carry the explanation. Before writing on-screen copy, sketch the subject at the opening, the revealing movement, and the held result. Put the example in the first shot. Use the [scene plan template](templates/scene_plan.md) to make these decisions visible.
2. **Study a complete reference passage and trace its source.** Start with a clip the user supplied, then find a 3Blue1Brown passage that solves the same visual problem. Watch the setup, the move, and the hold. For each state, map the focal point, scale, unused space, contrast, and when labels enter and leave. Trace layout, palette, and timing in the official source. Record the clip range, code permalink, and the decisions you will adapt. When the exact source is unavailable, identify any related implementation as a separate reference. When playback is unavailable, try a playable clip from the official lesson and record what you could inspect. Follow [reference study and adaptation](references/manim-code-patterns.md#reference-study-and-adaptation).
3. **Storyboard the movement before adding text.** Carry the same object, viewpoint, or coordinate system across related beats. When reframing, specify the object the eye follows, where it lands, and what the new view reveals. Give dense comparisons a steady view and the result time to read. Leave the corners empty by default. Each label needs a reason, an object or comparison it identifies, and a cue to enter and leave. Keep explanatory sentences in audio and captions. Follow [camera movement](references/manim-code-patterns.md#camera-movement-and-reframing).
4. **Review the passage against the reference.** Render the opening, hardest move, and result before producing the full video. Use `video.py review` to compare the frames at phone width and play the passage muted at normal speed. If the focal point is ambiguous, the relationship is unclear, or a header carries the meaning, revise the composition and render again. Save what changed in the scene plan. Follow [the visual review guide](references/manim-code-patterns.md#review-the-motion).

### Work with specialist agents

When collaboration is requested and the host supports delegation, let the lead own `scene_plan.md`, scene edits, and final delivery. Give the visual designer and reference researcher the same audience, question, and source constraints. Start their work in parallel when possible.

- **Visual designer:** Sketch the opening, the key movement, and the held result. Specify the visual anchor, framing, labels, and how the frame fits the target screen.
- **Reference researcher:** Verify the actual passage, trace its source, and return timestamped observations and one or two changes the designer can apply.
- **Independent reviewer:** Give this agent the rendered preview and target screen, withholding the intended reveal on its first pass. Have it watch once muted at normal speed, report what changed and why, and mark any break in attention or comprehension with a timestamp. Then share the plan and reference for comparison. For narrated output, review again with sound to catch mistimed cues or a claim the picture overstates.

The lead merges the design and research, tests the hardest transition as a short silent preview, and rerenders the affected scene or beat after review. For a simple video, the lead can handle design and use separate agents for research and review. When delegation is unavailable, run the same passes in sequence and describe the review accurately.

## Work one scene at a time

1. Read the source and locate the smallest coherent teaching unit. Preserve the source's numbers, definitions, observed and unobserved values, and examples. Check the prior scene's last line and the new scene's first line when continuing a series.
2. Map each planned beat to the final words and labels. For narration, use one short paragraph per beat, separated by a blank line. Read the [narration guide](references/script-writing-guide.md).
3. For a narrated scene, review the narration, then generate the MP3 and its adjacent `*.timings.json`. Read and listen to both before locking animation timing. For a silent preview, use provisional beat lengths. See [narration and sync](references/narration-sync.md).
4. Read the [Manim code patterns](references/manim-code-patterns.md) before writing code. Give the visual idea most of the frame, keep its colors and geometry stable across related beats, and reserve clearance where captions may appear. Clear obsolete objects before shrinking any labels.
5. Review the assembled preview at normal speed with the narration when present. Check that each event lands on the words that give it meaning. Compare frames directly before and after cuts. When a composition carries through a cut, preserve its position, scale, style, and visible labels. Verify that any jump has a clear job. Use selectable subtitles for narrated videos and short, local cues for silent videos.

```bash
.venv-video/bin/python video.py render videos/my_topic/en --json
```

To render a different scene in isolation, select its file and class.

```bash
.venv-video/bin/python video.py render videos/my_topic/en \
  --file videos/my_topic/en/scenes/scene_02_comparison.py --scene Scene02 --json
```

Use the `video`, `duration`, and `log` fields from the render result. Each attempt has its own log under `build/logs/`. On `ok: false`, open the log, fix the reported scene or timing error, and rerender that scene. Use the returned MP4 paths from successful attempts to review or assemble the video.

## Review transitions and assemble the video

Use the scene-relative start and end of the animation you want to inspect. Repeat `--transition` for more than one change. Open the contact sheet and correct any overlap, clipping, or abrupt change before proceeding.

```bash
.venv-video/bin/python video.py review "$SCENE_MP4" --transition 2.1 3.4 \
  --output videos/my_topic/en/build/review/01_intro
```

For narration, connect each measured chunk to its matching Manim beat and keep at least 0.5 seconds of visual tail after the audio. Review hand-tuned waits against the new timeline. Pass the successful render paths in playback order, with the narration MP3 after each narrated scene. Each MP3 uses its adjacent `*.timings.json` for subtitle timing. Pass a video path alone for a silent scene.

```bash
.venv-video/bin/python video.py package \
  --scene "$SCENE_1_MP4" videos/my_topic/en/build/audio/01_intro.mp3 \
  --scene "$SCENE_2_MP4" videos/my_topic/en/build/audio/02_comparison.mp3 \
  --output videos/my_topic/en/build/final/my_topic.mp4 --thumbnail-at 8.5
```

`package` returns the MP4, thumbnail PNG, and SRT paths. `--thumbnail-at` uses time in the assembled video and defaults to its midpoint. Silent projects receive the MP4 and PNG. Open the assembled review frames and confirm the focal subject, the purpose of each visible label, continuity across cuts, and subtitle clearance. Rerender any beat that fails this review before delivering the generated links. See [FFmpeg recipes](references/ffmpeg-recipes.md) for separate muxing, subtitle embedding, and background music.
