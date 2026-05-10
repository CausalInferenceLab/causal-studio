<a id="top"></a>

# Causal Studio

🌐 Language: English | [한국어](./README-ko_kr.md)

A platform providing educational videos and executable notebooks on causal inference.

- Book: <https://causalinferencelab.github.io/causal-studio/>
- YouTube: <https://www.youtube.com/@CausalStudio>

Project working rules: [CONTRIBUTING.md](./CONTRIBUTING.md) | [한국어](./CONTRIBUTING-ko_kr.md)

## How to Learn

1. Watch the videos: Understand concepts visually through clear animations for each chapter.
2. Run the code: Practice hands-on by running code directly in Binder or Colab.
3. Go deeper: Build a thorough understanding with the detailed code and explanations in the notebooks.

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

## CI/CD

Pushing changes under `book/**` to `main` triggers GitHub Actions to automatically deploy to GitHub Pages.

Deploy dependencies: `requirements-book.txt`

## Our Contributors

<a href="https://github.com/CausalInferenceLab/causal-studio/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=CausalInferenceLab/causal-studio" />
</a>

<p align="right">
  <a href="#top">⬆️ Back to Top</a>
</p>

## License

MIT. External assets (3b1b, Tabler Icons) follow their respective upstream licenses.
