# Contributing

[한국어](./CONTRIBUTING-ko_kr.md)

## Set up

Run these commands from the repository root.

```bash
bash scripts/setup_environment.sh
source .venv/bin/activate
```

For a smaller setup, pass `--book-only` or `--video-only`. Video-only setup uses `.venv-video`.

## Open a pull request

- Create a branch from `main` and keep the PR focused.
- **Book** — Run edited notebooks from top to bottom, verify the book output, and keep paths and dependencies compatible with Binder.
- **Video** — Render and review the affected scene. For shared Manim skill changes, follow the [maintenance guide](./.claude/skills/manim-skill-maintenance/SKILL.md).
- Describe the change and how you verified it in the PR.

Keep API keys and generated outputs local. See the [repository guidelines](./AGENTS.md) for dependency files and repo skills.
