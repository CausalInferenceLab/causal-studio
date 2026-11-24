# Manim video pipeline

**Turn challenging concepts in math and statistics into 3Blue1Brown-inspired videos.** The open-source Manim skill behind Causal Studio’s causal inference series. Start with one prompt in Claude Code or Codex.

[Watch on YouTube](https://www.youtube.com/@CausalStudio) · [Read the Causal Studio book](https://causalinferencelab.github.io/causal-studio/)

## Make your first video

```bash
git clone -b skill-only https://github.com/CausalInferenceLab/causal-studio
```

**Open `causal-studio` in Claude Code or Codex** and paste this request.

```text
Use the manim-video-pipeline skill to show why averages vary less with larger
samples. Draw repeated samples of 5 and 50 from the same population and compare
the distributions of their sample means. Give me a silent MP4 preview.
```

Use your own topic or point the agent to a Markdown, text, or Jupyter notebook file. After reviewing the preview, ask for a layout change or add OpenAI or ElevenLabs narration. The skill writes measured beat timings to `*.timings.json` so the animation can follow the voiceover. Voice API keys are only needed when adding narration.

For narration, copy the root `.env.example` to `.env` if you’re setting it up for the first time. Fill in the settings for your chosen provider and name that provider in your request.

[View the skill](https://github.com/CausalInferenceLab/causal-studio/blob/skill-only/.claude/skills/manim-video-pipeline/SKILL.md) · [See example prompts and voice setup](https://github.com/CausalInferenceLab/causal-studio/blob/main/docs/manim-starter.md#3-review-and-add-narration-if-you-want-it) · [Explore the full Causal Studio project](https://github.com/CausalInferenceLab/causal-studio)
