# Manim video pipeline

Use Claude Code or Codex to turn your own topic, notes, or notebook into a Manim video. This checkout contains the shared skill and its render, narration, and setup tools.

```bash
git clone --branch skill-only --single-branch --depth 1 https://github.com/CausalInferenceLab/causal-studio.git causal-studio-skill
```

Open `causal-studio-skill` in Claude Code or Codex and ask for a first scene.

> Use manim-video-pipeline to make the first scene of a middle-school explainer on photosynthesis. Set up the video environment and show me a silent MP4.

Give the agent a file path if you have Markdown, text, or a Jupyter notebook. After reviewing the preview, ask for OpenAI or ElevenLabs narration if you want it. The first silent render needs no text-to-speech API key.

The skill is in `.claude/skills/manim-video-pipeline/SKILL.md`. [Causal Studio videos and notebooks](https://github.com/CausalInferenceLab/causal-studio)
