# Contributing

This project mixes a Jupyter Book and local-only Manim video workflows. Keep changes small, explicit, and compatible with both local development and hosted book environments.

## Core Rules

1. Use the repo skills first.
   - Codex workflows live in `.codex/skills/`.
   - Claude bridge workflows live in `.claude/skills/` when the task matches the documented trigger.

2. Keep book and video dependencies separated.
   - `requirements.txt` is the full local environment for book + video work.
   - `requirements-book.txt` is the minimal runtime for book, Binder, and GitHub Pages style builds.
   - If a notebook under `book/` imports a package at runtime, update `requirements-book.txt` too.
   - If Binder needs a system package, update `binder/apt.txt`.

3. Write Binder-safe notebook paths.
   - Do not assume the current working directory is the notebook directory.
   - Prefer paths that work from repo root as well as notebook-local execution.
   - For packaged data in the book, prefer `pathlib.Path` with a repo-root path and a local fallback when appropriate.

4. Treat local-only assets as local-only.
   - `3b1b/` and `videos/assets/tabler-icons/` are setup assets, not core repo content.
   - Do not commit generated caches, renders, or machine-local settings unless the change explicitly requires it.

5. Verify the path you changed.
   - Book changes: build or otherwise verify the affected book content.
   - Binder-facing changes: check Binder config and notebook runtime assumptions together.
   - Video pipeline changes: prefer the bundled skill scripts instead of ad hoc shell rewrites.

## Commit Scope

- Keep unrelated changes out of the same commit.
- Avoid committing `.env`, local settings, or other machine-specific files.
- If a change affects published notebooks, include the dependency/config updates in the same PR.
