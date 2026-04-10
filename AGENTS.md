# Codex Routing Rules For This Repo

## 1) Skill-First Operation

Use REPO skills in `.codex/skills` instead of project command files.

Project skills for previous command workflows:
- `book-serve`: local Jupyter Book server
- `git-commit`: change analysis and commit workflow
- `git-pr`: pull request workflow

## 2) Claude Skill Bridge

When request intent matches below topics, use `.claude/skills/*` as the operational source:
- `manim-video-pipeline`: scene design/script/render/audio mux/full concat
- `pip-install`: install package in `.venv` and sync `requirements.txt`
- `skill-creator`: create/update project skill package
- `deep-research`: 심층 조사, deep research, 종합 분석, in-depth report → outputs/ 에 저장
- `literature-review`: 문헌 조사, lit review, 논문 survey, state of the art
- `peer-review`: 동료 검토 시뮬레이션, 논문/노트북/분석 결과 리뷰
- `source-comparison`: 여러 소스·방법론·도구 비교 매트릭스

How to execute:
1. Read the target `SKILL.md`.
2. Resolve relative paths from the skill directory first.
3. Prefer bundled scripts in `scripts/` over re-implementing logic.
4. Load only required files in `references/`.

Priority:
- In this repository, REPO scope skills (`.codex/skills/*`) take precedence over USER/ADMIN/SYSTEM skills when names overlap.

## Project Working Rules

- Treat `.codex/skills/*` and `.claude/skills/*` as the default operating procedures for recurring tasks.
- Keep dependency scopes separated:
  - `requirements.txt` for full local book + video work
  - `requirements-book.txt` for book, Binder, and deploy runtime
  - `binder/apt.txt` for Binder system packages
- When editing notebooks under `book/`, use Binder-safe paths and do not assume the current working directory is the notebook folder.
- Do not commit local machine artifacts such as `.env`, local settings, generated caches, or render outputs unless the user explicitly asks for that.
- Prefer small, task-coherent commits that include related config/dependency updates together.
