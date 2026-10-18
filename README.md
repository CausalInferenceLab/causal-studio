<a id="top"></a>

# Causal Studio

🌐 Language: English | [한국어](./README-ko_kr.md)

A platform providing educational videos and executable notebooks on causal inference.

- Book: <https://causalinferencelab.github.io/causal-studio/>
- YouTube: <https://www.youtube.com/@CausalStudio>

Project working rules: [CONTRIBUTING.md](./CONTRIBUTING.md) | [한국어](./CONTRIBUTING-ko_kr.md)

## How to Learn

1. Watch the videos: Learn each chapter through clear visual explanations.
2. Run and explore the notebooks: Practice hands-on in Binder or Colab, then build a deeper understanding with the notebook code and explanations.

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
Set up Python environment      → python-setup skill (Python + both video assets)
Update local video assets      → video-assets-setup skill
```

Run the complete setup from the repository root:

```bash
bash scripts/setup_environment.sh
source .venv/bin/activate
```

The script reuses `.venv`, selects the Python version specified in `Pipfile`
(currently 3.11; override its executable with `PYTHON_BIN`), installs
`requirements.txt`, and prepares both asset repositories. Install the matching
Python version first; Manim also requires system Cairo/Pango development libraries
and `pkg-config` when wheels are unavailable.

Use `bash scripts/setup_environment.sh --book-only` only for a Book-only setup
with `requirements-book.txt` and no video assets. Use `--check` (optionally with
`--book-only`) to validate without installing or updating. Full setup reports
success only after dependency, import, and required asset file checks pass.

Both setup skills use shared scripts. The following repos are cloned locally
(not git-tracked):

- `3b1b/` — 3b1b/videos reference
- `videos/assets/tabler-icons/` — Tabler Icons

## CI/CD

Pushing changes under `book/**` to `main` triggers GitHub Actions to automatically deploy to GitHub Pages.

Deploy dependencies: `requirements-book.txt`

## License

MIT. External assets (3b1b, Tabler Icons) follow their respective upstream licenses.
