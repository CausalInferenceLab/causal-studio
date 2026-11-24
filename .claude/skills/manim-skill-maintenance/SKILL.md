---
name: manim-skill-maintenance
description: Maintain the shared Causal Studio Manim skill. Use when editing manim-video-pipeline or a packaged helper, checking its Claude Code and Codex entry points, verifying the starter export, or preparing a skill-only branch update.
---

# Manim skill maintenance

## Locate the change

Read the [canonical Manim skill](../manim-video-pipeline/SKILL.md) and inspect the relevant code paths before editing. Make shared changes on `main` or a working branch based on it. The `.agents/skills/` and `.codex/skills/` entries for Manim resolve to the same `.claude/skills/manim-video-pipeline/` directory. Edit the canonical files and keep both entries pointing there.

Classify the change before preparing a distribution update.

- **Shared** includes skill guidance, layout and caption checks, setup for the video-only environment, rendering, optional TTS, timing, muxing, and the exported launcher and dependencies. Check the [exporter](../../../scripts/export_manim_starter.py) to see which files the current starter ships. Update any affected examples or instructions.
- **Causal Studio content** includes the book, datasets, existing causal inference videos, their narration, and project-specific automation. Keep the working content in Causal Studio. If a shared change affects an existing scene, verify it against that scene.
- **Other development skills** have their own scope. This procedure applies when their work touches the Manim skill or distributed tools.

## Verify the change

- Inspect the diff and resolve the Claude Code and Codex entry paths to the canonical directory. Verify relative links and commands from the place the skill uses them.
- Use a supported Python interpreter to run `python -m unittest discover -s tests -v` for runtime, setup, or export changes. For speech or timing changes, check the provider and timing tests with mocked requests. Render a demo for changes that affect visual output or first use.
- For changes affecting external use, export into a new directory with `python scripts/export_manim_starter.py --directory <new-directory>`. Run checks from that directory so imports and resources resolve from the exported files. For an execution smoke test, prepare its video-only environment with `bash scripts/setup_environment.sh --video-only` and render the included demo with `.venv-video/bin/python video.py render videos/binary_search/en`.
- Review the exported files. Confirm they contain the resources required by the exported instructions and exclude personal credentials, caches, render outputs, and project work outside the selected distribution. Preserve the natural-language quickstart in [the onboarding guide](../../../docs/manim-starter.md).

## Update the public snapshot when releasing

Treat `skill-only` as a snapshot generated from a reviewed `main` commit. Make fixes in the source and regenerate the snapshot. Record the source commit in the snapshot commit message so a later maintainer can compare the two.

Generate the minimal snapshot with `python scripts/export_manim_starter.py --skill-only --directory <new-directory>`. Review the exporter's file selection when adding a shared dependency. Run `python -m unittest discover -s tests/e2e -v` to confirm first use from a fresh Git clone. Keep book content, existing videos, and project-specific scripts in Causal Studio.

When a request includes publishing, review the snapshot diff and follow the project's Git workflow for the branch update. Report the source commit, checks run, and published branch or local snapshot. For an ordinary source edit, report whether it affects the public snapshot so the next release can pick it up.
