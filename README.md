# Causal Studio

English | [한국어](./README-ko_kr.md)

A repository for managing a causal inference codebook (Jupyter Book) and Manim educational videos together.

## Repository Structure

```text
causal_studio/
├── book/
│   └── why_causal_inference/        Korean & English notebooks
├── videos/
│   └── why_causal_inference/
│       └── src/                     Scene code + narration scripts
├── .codex/skills/                   Codex skills
├── .claude/skills/                  Claude Code skills
├── requirements.txt                 Full dependencies (book + video)
└── requirements-book.txt            Book-only (CI/deploy)
```

## Setup

On a fresh clone:

```text
Set up Python environment      → python-setup skill
Install local video assets     → video-assets-setup skill
```

`video-assets-setup` clones the following repos locally (not git-tracked):
- `3b1b/` — 3b1b/videos reference
- `videos/assets/tabler-icons/` — Tabler Icons

## Skills

| Skill | Description |
|---|---|
| `python-setup` | Create `.venv` and install initial dependencies |
| `video-assets-setup` | Install/update `3b1b/` and `tabler-icons/` local assets |
| `pip-install` | Install package in `.venv` and sync `requirements.txt` |
| `book-serve` | Run Jupyter Book local server |
| `book-publish` | Add notebook to book TOC and verify build |
| `ipynb-to-english` | Translate Korean notebook to English `_en.ipynb` |
| `manim-video-pipeline` | Scene design / script / render / audio / mux / concat |
| `git-commit` | Analyze changes and commit |
| `git-pr` | Create pull request |
| `skill-creator` | Create or update project skills |

## CI/CD

Pushing changes under `book/**` to `main` triggers GitHub Actions to automatically deploy to GitHub Pages.

Deploy dependencies: `requirements-book.txt`

## License

MIT. External assets (3b1b, Tabler Icons) follow their respective upstream licenses.
