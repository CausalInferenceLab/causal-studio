# Causal Studio

English | [한국어](./README-ko_kr.md)

A repository for managing a causal inference codebook (Jupyter Book) and Manim educational videos together.

Project working rules: [CONTRIBUTING.md](./CONTRIBUTING.md) | [한국어](./CONTRIBUTING-ko_kr.md)

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

### Research

| Skill | Description |
|---|---|
| `deep-research` | Multi-agent deep investigation on any topic — outputs a cited research brief to `outputs/` with provenance record |
| `literature-review` | Paper-focused literature survey with consensus, disagreements, and open questions |
| `peer-review` | Simulate peer review with FATAL / MAJOR / MINOR severity classification and a revision plan |
| `source-comparison` | Compare multiple sources, methods, or tools and produce a grounded comparison matrix |

### Book & Notebook

| Skill | Description |
|---|---|
| `book-serve` | Run Jupyter Book local server |
| `book-publish` | Add notebook to book TOC and verify build |
| `ipynb-to-english` | Translate Korean notebook to English `_en.ipynb` |
| `ipynb-youtube-embed` | Embed a YouTube iframe into a notebook (with pre-stored output for Jupyter Book) |

### Video

| Skill | Description |
|---|---|
| `manim-video-pipeline` | Scene design / script / render / audio / mux / concat |
| `manim-thumbnail` | Generate a 3b1b-style YouTube thumbnail PNG with Manim |

### Environment & Project

| Skill | Description |
|---|---|
| `python-setup` | Create `.venv` and install initial dependencies |
| `video-assets-setup` | Install/update `3b1b/` and `tabler-icons/` local assets |
| `pip-install` | Install package in `.venv` and sync `requirements.txt` |
| `git-commit` | Analyze changes and commit |
| `git-pr` | Create pull request |
| `skill-creator` | Create or update project skills |

## CI/CD

Pushing changes under `book/**` to `main` triggers GitHub Actions to automatically deploy to GitHub Pages.

Deploy dependencies: `requirements-book.txt`

## License

MIT. External assets (3b1b, Tabler Icons) follow their respective upstream licenses.
