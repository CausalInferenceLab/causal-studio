# Contributing

English | [한국어](./CONTRIBUTING-ko_kr.md)

This project combines an executable Jupyter Book with local-only Manim video workflows. Keep changes small and explicit, and make them reproducible in both local and Binder/book environments.

## Core Rules

1. Use repo skills first.
   - Use `.codex/skills/` for Codex workflows.
   - Use `.claude/skills/` as the operating source when a task matches one of its triggers.

2. Keep dependency scopes separated.
   - `requirements.txt`: full local environment for book + video work
   - `requirements-book.txt`: minimal runtime for book, Binder, and deployed builds
   - `binder/apt.txt`: system packages needed on Binder

3. Write Binder-safe notebooks.
   - Do not assume the current working directory is the notebook directory.
   - Use paths that work from both the repo root and notebook-local execution.
   - If a `book/` notebook imports a new package, update `requirements-book.txt` too.

4. Do not commit local-only assets.
   - Exclude `.env`, local settings, generated caches, and rendered outputs by default.
   - Treat `3b1b/` and `videos/assets/tabler-icons/` as local setup assets.

## Notebook Writing Criteria

Pre-video notebooks are video drafts, but they should also have learning value on their own.

- Explain enough. Do not leave core concepts, assumptions, code results, or chart interpretation for the reader to infer.
- Keep the notebook easy to read and run cell by cell. Avoid `.py`-style structures where many functions and classes are defined far above their use.
- Allow modest code repetition when it supports the learning flow. Prefer understandable progression over heavy abstraction.
- Prefer proven libraries over custom implementations.
- Check whether the topic can be explained better through visualization when made into a video.
- The notebook should run from top to bottom without errors.

## Verification And Commits

- Build or otherwise verify changed book content.
- For Binder-facing changes, check dependencies, paths, and runtime together.
- Keep unrelated changes out of the same commit.
- If a change affects published notebooks, include related config changes in the same PR.
