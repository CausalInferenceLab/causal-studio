<a id="top"></a>

# Causal Studio

🌐 Language: English | [한국어](./README-ko_kr.md)

**Turn a lesson, a notebook, or a short prompt into a Manim explainer with Claude Code or Codex.**

We use the same workflow to make Causal Studio's animated causal inference lessons and share runnable companion notebooks.

**[Make your own video](./docs/manim-starter.md)** · [Watch the RDD example](https://www.youtube.com/watch?v=Rpd3k6Boftk) · [Explore the notebooks](https://causalinferencelab.github.io/causal-studio/)

[![An RDD scatter plot shows fitted GPA trends below and above the 370-point scholarship cutoff](./docs/assets/rdd-preview.jpg)](https://www.youtube.com/watch?v=Rpd3k6Boftk)

## Try the Manim skill

Clone this repository and open the folder in Claude Code or Codex. Give the agent a lesson or start with this prompt.

> Use `manim-video-pipeline` to make the first scene of a video explaining photosynthesis to middle-school students. Set up the video environment if needed and show me a silent preview.

The agent plans the scene, writes editable Manim code, and renders the preview. Add narration with OpenAI or ElevenLabs when you're ready. [Quickstart](./docs/manim-starter.md)

## How to Learn

1. Watch the videos: Learn each chapter through clear visual explanations.
2. Run and explore the notebooks: Practice hands-on in Binder or Colab, then build a deeper understanding with the notebook code and explanations.

Browse more [Causal Studio videos](https://www.youtube.com/@CausalStudio). If this workflow helps you make an explainer, a GitHub star is appreciated.

## Repository Structure

```text
causal_studio/
├── book/
│   └── why_causal_inference/        Korean & English notebooks
├── videos/
│   ├── binary-search/              Starter example and caption/timing demo
│   └── why_causal_inference/
│       └── src/                     Scene code + narration scripts
├── .codex/skills/                   Codex skills
├── .claude/skills/                  Claude Code skills
├── requirements.txt                 Full dependencies (book + video)
├── requirements-video.txt           Starter preview dependencies
└── requirements-book.txt            Book-only (CI/deploy)
```

## Contributor setup

Project working rules are in [CONTRIBUTING.md](./CONTRIBUTING.md) and [한국어](./CONTRIBUTING-ko_kr.md).

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
