<h1 align="center">Causal Studio</h1>

<p align="center"><strong>Turn challenging math and statistics concepts into 3Blue1Brown-style videos.</strong></p>

<p align="center">An open-source Manim skill built while producing Causal Studio’s causal inference series.<br>Simply describe the video you want to create in Claude Code or Codex.</p>

<p align="center">
  <a href="#make-your-first-video"><strong>Make a video</strong></a> ·
  <a href="https://www.youtube.com/@CausalStudio">Watch on YouTube</a> ·
  <a href="https://causalinferencelab.github.io/causal-studio/">Read the book</a> ·
  <a href="./README-ko_kr.md">한국어</a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="./docs/assets/did-preview.jpg">
    <img src="./docs/assets/did-animation.gif" width="820" alt="Two city deposit trends align to a shared baseline, revealing the difference in post-campaign growth.">
  </picture><br>
  <sub>Difference-in-differences · Billboard campaign example</sub>
</p>

## Make your first video

1. Clone the `skill-only` branch.

   ```bash
   git clone -b skill-only https://github.com/CausalInferenceLab/causal-studio
   ```

2. Open the folder in Claude Code or Codex and describe your video.

   ```text
   Use manim-video-pipeline to explain why A/B tests need randomization in a 45-second video.
   Show two ticket checkouts that start with skewed groups of shoppers, leading to a biased result.
   Use three scenes to show the initial bias, a coin flip assigning each shopper,
   and the fair comparison afterward.
   ```

If you have a script or a Jupyter notebook with explanations and plots, pass its file path to the agent. Otherwise, a single-sentence topic is enough to get started. [Example notebook](./book/rdd/01_rdd_basic_en.ipynb)

You can render the initial preview without a voice API key.

## How the video comes together

1. **Plan the explanation.** The agent studies a relevant 3Blue1Brown passage and its Manim code, drafts the script, and maps out camera movements and key visual reveals.
2. **Preview key transitions.** Inspect frames before, during, and after major transitions. Ask the agent to fix any clipping, overlapping text, or jarring motion and re-render only that scene.
3. **Add narration and export.** OpenAI or ElevenLabs turns your script into voiceover audio. The agent uses `*.timings.json` to sync the final animation and outputs an MP4, thumbnail, and SRT subtitles (when narrated). [Voice setup](./docs/manim-starter.md#3-review-and-add-narration-if-you-want-it)

If your tool supports sub-agent delegation, you can ask the agent to split reference research, scene design, and visual review across separate agents.

## Project structure and scene revisions

Each scene has its own Manim script and, when narrated, a corresponding text file.

```text
videos/ab_test/en/
├── project.toml              # References and default scene configuration
├── lesson.md                 # Production brief generated when starting from a topic
├── scene_plan.md             # References, framing, and storyboard
├── narration/                # Scene-by-scene scripts
│   ├── 01_question.txt
│   ├── 02_assignment.txt
│   └── 03_comparison.txt
├── scenes/                   # Manim source files
│   ├── scene_01_question.py
│   ├── scene_02_assignment.py
│   └── scene_03_comparison.py
└── build/
    ├── audio/                # MP3 narration and timing files
    ├── logs/                 # Logs per render attempt
    ├── manim/                # Rendered individual scenes
    ├── review/               # Transition frames and contact sheets
    └── final/                # Final MP4, thumbnail PNG, and optional SRT
```

> In scene 2, keep the first group visible on screen while the assignment changes, then re-render just that scene.

## Explore Causal Studio

Check out the [English](./videos/rdd/en/) and [Korean](./videos/rdd/ko/) RDD projects to see real examples of scene code and scripts from the course. To work on the book or existing course videos, clone the full repository, which includes the same skill:

```bash
git clone https://github.com/CausalInferenceLab/causal-studio
```

[View the skill](./.claude/skills/manim-video-pipeline/SKILL.md) · [Contribute](./CONTRIBUTING.md)

---

If this skill helps you make a video, consider giving Causal Studio a star.

MIT License. External assets such as 3Blue1Brown references and Tabler Icons remain subject to their respective licenses.
