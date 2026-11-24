<h1 align="center">Causal Studio</h1>

<p align="center"><strong>Turn challenging concepts in math and statistics into 3Blue1Brown-inspired videos.</strong></p>

<p align="center">An open-source Manim skill developed for Causal Studio’s causal inference series.<br>Describe the video you want to make in Claude Code or Codex.</p>

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

1. Clone the `skill-only` branch to get the video tools.

   ```bash
   git clone -b skill-only https://github.com/CausalInferenceLab/causal-studio
   ```

2. Open the `causal-studio` folder in Claude Code or Codex and try this prompt.

   ```text
   Use manim-video-pipeline to make a 75-second introduction to A/B testing.
   In five scenes, use a button color experiment to show why a before-and-after comparison
   can mislead, how to assign visitors at random, how to compare click rates, what the
   confidence interval tells us, and how to decide whether to switch.
   ```

If you have a script or Jupyter notebook, include its path in your prompt. A notebook with explanations and plots can guide what appears on screen and in what order. [Example RDD notebook](./book/rdd/01_rdd_basic_en.ipynb)

You can preview a key scene without a voice API key.

## How the video comes together

![Write the script, generate narration, then finish the MP4 with Manim animation and audio](./docs/assets/manim-workflow.png)

1. **Plan the scenes and draft the script.** The skill finds relevant 3Blue1Brown scenes and their Manim code to decide what each scene should show and how to present it. Edit the draft or ask the agent to revise it.
2. **Add narration.** If you want a voice, the agent generates an MP3 for each scene with OpenAI or ElevenLabs and records paragraph timing in `*.timings.json`. [Environment variables](./.env.example) · [Voice setup guide](./docs/manim-starter.md#3-review-and-add-narration-if-you-want-it)
3. **Animate in Manim and render the MP4.** The agent writes the Manim code and refines the framing and motion after reviewing the renders. It syncs any narration and joins the scenes into one MP4.

## Files and scene revisions

Each scene has its own script and Manim file. An A/B testing video can be organized like this.

```text
videos/ab-test/
├── project.toml           # Lesson source and default scene
├── lesson.md              # Lesson notes created when you start with a topic
├── scene_plan.md          # Visual references and storyboard
├── assets/                # Icons and other visual assets, if used
├── narration/
│   ├── 01_question.txt
│   ├── 02_assignment.txt
│   ├── 03_rates.txt
│   ├── 04_interval.txt
│   └── 05_decision.txt
├── scenes/
│   ├── scene_01.py
│   ├── scene_02.py
│   ├── scene_03.py
│   ├── scene_04.py
│   ├── scene_05.py
│   └── style.py           # Shared colors and graphics
└── build/
    ├── audio/             # Scene MP3s and timing files
    ├── manim/             # Manim renders
    ├── final/             # Individual scenes with audio
    ├── ab-test.mp4        # Complete video
    └── ab-test.ko.srt     # Optional subtitles
```

To revise a scene, tell Claude Code or Codex its number and what to change.

> In scene 3, hold the click-rate comparison a little longer and render that scene again.

## Explore Causal Studio

See the [English](./videos/rdd/en/) and [Korean](./videos/rdd/ko/) RDD projects for examples of the scene code and scripts used in the course. To work on the book or existing videos, clone the full repository, which includes the same skill.

```bash
git clone https://github.com/CausalInferenceLab/causal-studio
```

[View the skill](./.claude/skills/manim-video-pipeline/SKILL.md) · [Contribute](./CONTRIBUTING.md)

---

If the skill helps you make a video, give Causal Studio a star.

MIT. External assets such as the 3Blue1Brown references and Tabler Icons retain their upstream licenses.
