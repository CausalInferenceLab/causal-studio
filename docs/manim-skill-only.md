# Manim video pipeline

**Turn challenging concepts in math and statistics into 3Blue1Brown-inspired videos.** The open-source Manim skill behind Causal Studio’s causal inference series. Start with one prompt in Claude Code or Codex.

[Watch on YouTube](https://www.youtube.com/@CausalStudio) · [Read the Causal Studio book](https://causalinferencelab.github.io/causal-studio/)

## Make your first video

1. Run this command in your terminal.

   ```bash
   git clone -b skill-only https://github.com/CausalInferenceLab/causal-studio
   ```

2. Open the `causal-studio` folder in Claude Code or Codex and send this prompt.

   ```text
   Use manim-video-pipeline to make a 75-second introduction to A/B testing.
   In five scenes, use a button color experiment to show why a before-and-after comparison
   can mislead, how to assign visitors at random, how to compare click rates, what the
   confidence interval tells us, and how to decide whether to switch.
   ```

If the video should draw on a file, such as a script or a Jupyter Notebook, include its path in your request. You can make a preview without a voice API key.

To guide the explanation and visuals, outline the lesson and include the plotting code in an `.ipynb` first. Causal Studio uses this approach for its causal inference videos. [Example RDD notebook](https://github.com/CausalInferenceLab/causal-studio/blob/main/book/rdd/01_rdd_basic_en.ipynb)

## From script to narrated video

![Write the script, generate narration, then finish the MP4 with Manim animation and audio](./assets/manim-workflow.png)

1. **Write the script.** Edit the agent’s draft yourself or ask for revisions. The revised script guides the narration and what appears on screen.
2. **Generate narration.** OpenAI or ElevenLabs reads the script. Each scene gets an MP3 and a `*.timings.json` file with the start and end of each paragraph.
3. **Animate and assemble.** Time the animation to the narration, keep the numbers and labels viewers need, then join the scenes into one MP4.

For narration, copy the root `.env.example` to `.env` if you’re setting it up for the first time. Fill in the settings for your chosen provider and name that provider in your request.

## Example project folder

Each scene has its own script and Manim file. Ask Claude Code or Codex to work on a specific scene when you want to revise it.

> In scene 3, hold the click-rate comparison a little longer and render that scene again.

```text
videos/ab-test/
├── project.toml           # Lesson source and default scene
├── lesson.md              # Created from a topic prompt (.md, .txt, or .ipynb also accepted)
├── scene_plan.md          # What changes on screen in each scene
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

[View the skill](https://github.com/CausalInferenceLab/causal-studio/blob/skill-only/.claude/skills/manim-video-pipeline/SKILL.md) · [See example prompts and voice setup](https://github.com/CausalInferenceLab/causal-studio/blob/main/docs/manim-starter.md#3-review-and-add-narration-if-you-want-it) · [Explore the full Causal Studio project](https://github.com/CausalInferenceLab/causal-studio)
