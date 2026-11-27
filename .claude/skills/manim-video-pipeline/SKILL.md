---
name: manim-video-pipeline
description: Plan, design, render, review, or caption educational Manim videos from a brief, script, or optional Jupyter notebook. Use for script-only work, 3Blue1Brown reference study, a single scene, narration and sync, subtitle edits, or an entire video.
---

# Manim video pipeline

Use the requested deliverable to choose a playbook. Read that playbook first and open its supporting references as needed. An explicit scope such as “only,” “first,” or a numbered scene takes precedence over the broader project. For a request covering several named tasks, run just those playbooks and stop at the last requested deliverable.

| The user asks for | Playbook | Deliver |
|---|---|---|
| “Write the script first” / “대본만” | [Script](playbooks/script.md) | The requested draft or revised narration |
| “Find a 3Blue1Brown reference” / “Show me the key visual” | [Visual design](playbooks/visual-design.md) | Reference notes, storyboard, or a requested prototype |
| “Generate the narration” / “Match this scene to the voice” | [Audio and sync](playbooks/audio-sync.md) | MP3 and timing file, with a synced render when requested |
| “Rerender scene 3” / “장면 하나만” | [Single scene](playbooks/scene.md) | The selected scene and its render result |
| “Review this cut” / “Check the transitions” | [Review](playbooks/review.md) | Timestamped findings and any requested review frames |
| “Fix the subtitles only” / “자막만” | [Captions](playbooks/captions.md) | The revised timestamped SRT |
| “Assemble these existing scenes” | [Package](playbooks/package.md) | The assembled MP4, thumbnail, and SRT when narrated |
| “Make the full video” / “영상 전체를 만들어줘” | [Full video](playbooks/full-video.md) | The requested review checkpoint or a verified final cut |

A request to try the skill is a demo. Make a small preview for the requested topic. If the user leaves the topic open, use binary search and render the supplied scene when available. Follow the single-scene playbook and return the preview.

## Shared project conventions

- Accept a short topic, an existing Markdown or text file, or a Jupyter notebook. Read notebook cells and saved outputs without executing the notebook. Create a notebook when the user asks for one.
- Use 16:9 for a new lesson and 9:16 for a short explicitly intended for a vertical feed. Use the requested aspect ratio or keep the existing project's dimensions for revisions.
- Use `videos/<topic_slug>/<language>/` for a video project. Read its `project.toml` for the source, default scene file, and Manim class. Number matching files as `scenes/scene_NN_name.py` and `narration/NN_name.txt`. A silent scene can omit its narration. Keep the storyboard in `scene_plan.md` and shared code under the topic's `shared/`.
- Write rendered media under the edition's `build/`. When editing an existing Causal Studio lesson in the full repository, read `references/causal-studio.md`.
- For Manim renders, use the project's working environment or the video-only Python environment described in the [single-scene playbook](playbooks/scene.md). Run project setup and invoke render or audio tools only when needed by the selected playbook.
