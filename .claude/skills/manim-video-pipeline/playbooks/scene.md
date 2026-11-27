# Make, revise, or render one scene

Identify the requested scene by its number, filename, or class. Read the edition's manifest, relevant source, and neighboring opening or closing frames as needed for continuity. For a single-scene request, limit writes and renders to that scene and its requested artifacts. A render-only request uses the existing scene code as input. When a shared change would affect other scenes, keep the fix local if possible and explain any necessary expansion.

## Set up the render

Use the project's working environment when the scene has additional dependencies. For a standalone scene, run `bash scripts/setup_environment.sh --video-only --check` and use `bash scripts/setup_environment.sh --video-only` if setup is needed. Use its `.venv-video/bin/python`. For a new video project, initialize from a brief or source file.

```bash
.venv-video/bin/python video.py init videos/my_topic --lang en --brief "Explain binary search"
.venv-video/bin/python video.py init videos/my_topic --lang ko --source path/to/lesson.ipynb
```

## Work on the selected scene

1. Preserve the relevant source claims, numbers, and observed versus hypothetical values. Use the [visual design playbook](visual-design.md) for a new visual idea and the [Manim patterns](../references/manim-code-patterns.md) for code. For an existing scene, keep coordinate systems, camera scale, and persistent objects consistent across the cut.
2. Reuse the matching `*.timings.json` when revising animation against recorded narration. For a silent scene or prototype, use provisional timing. Generate or replace audio only when the user asks for it or requests a newly narrated result.
3. Render the requested file and class. Use `--quality l` for a rough cut. In the JSON result, use `video`, `duration`, and `log`. When a render fails, read the returned log, fix the selected scene, and retry.

```bash
.venv-video/bin/python video.py render videos/my_topic/en \
  --file videos/my_topic/en/scenes/scene_03_comparison.py --scene Scene03 --json
```

Use the [review playbook](review.md) to check the selected scene as needed. Run `video.py check` when creating or moving a project edition. Deliver the selected scene's result and stop at that scene. Assembling the full cut is a separate request.
