<h1 align="center">Causal Studio</h1>

<p align="center"><strong>Make complex ideas clear with animation.</strong></p>

<p align="center">The open-source Manim skill behind Causal Studio’s causal inference videos.<br>Start with a topic, script, or notebook and ask Claude Code or Codex to make a video.</p>

<p align="center">
  <a href="#make-your-first-video"><strong>Make a video</strong></a> ·
  <a href="https://www.youtube.com/@CausalStudio">Watch on YouTube</a> ·
  <a href="https://causalinferencelab.github.io/causal-studio/">Read the book</a> ·
  <a href="./README-ko_kr.md">한국어</a>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=Rpd3k6Boftk">
    <picture>
      <source media="(prefers-reduced-motion: reduce)" srcset="./docs/assets/rdd-preview.jpg">
      <img src="./docs/assets/rdd-animation.gif" width="820" alt="An animated scatter plot draws fitted GPA trends on each side of the 370-point scholarship cutoff and highlights the gap between them.">
    </picture>
  </a><br>
  <sub><a href="https://www.youtube.com/watch?v=Rpd3k6Boftk">Watch the example</a> · Regression discontinuity</sub>
</p>

## Make your first video

**Clone the Manim skill.** It works with any lesson topic.

```bash
git clone -b skill-only https://github.com/CausalInferenceLab/causal-studio
```

**Open `causal-studio` in Claude Code or Codex** and paste this request.

```text
Use the manim-video-pipeline skill to explain photosynthesis to middle-school
students. Plan the first scene, show light hitting a leaf, and keep the caption
below the diagram. Set up the video environment and show me a silent MP4 preview.
```

Watch the preview, then ask for a change in plain language. You can start from a topic alone or give the agent a path to Markdown, plain text, or a Jupyter notebook.

## How the skill works

| Stage | What you get |
| --- | --- |
| Plan | A scene plan connecting each narration cue to an on-screen action |
| Animate | An editable Manim scene and a silent MP4 preview, with captions placed below the visuals |
| Narrate | Optional OpenAI or ElevenLabs voiceover, with measured beat timings in `*.timings.json` to sync the animation |

Voice API keys are only needed when adding narration. Use [`.env.example`](./.env.example) and the [voice setup guide](./docs/manim-starter.md#3-review-and-add-narration-if-you-want-it).

## Explore Causal Studio

Study causal inference with animated lessons and runnable notebooks. Clone the full project to work on the book, notebooks, or original Manim scenes. It includes the same video skill.

```bash
git clone https://github.com/CausalInferenceLab/causal-studio
```

[Watch the lessons on YouTube](https://www.youtube.com/@CausalStudio) · [Read the book](https://causalinferencelab.github.io/causal-studio/) · [View the skill](./.claude/skills/manim-video-pipeline/SKILL.md) · [Contribute](./CONTRIBUTING.md)

---

If the skill helps you make a video, give Causal Studio a star.

MIT. External assets such as the 3Blue1Brown references and Tabler Icons retain their upstream licenses.
