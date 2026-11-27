# Manim video pipeline

**Turn challenging math and statistics concepts into 3Blue1Brown-style videos.** An open-source Manim skill built while producing Causal Studio’s causal inference series. Simply describe the video you want to create in Claude Code or Codex.

[Watch on YouTube](https://www.youtube.com/@CausalStudio) · [Read the Causal Studio book](https://causalinferencelab.github.io/causal-studio/)

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

If you have a script or a Jupyter notebook with explanations and plots, pass its file path to the agent. Otherwise, a single-sentence topic is enough to get started. [Example notebook](https://github.com/CausalInferenceLab/causal-studio/blob/main/book/rdd/01_rdd_basic_en.ipynb)

You can render the initial preview without a voice API key.

## How the video comes together

1. **Plan the explanation.** The agent studies a relevant 3Blue1Brown passage and its Manim code, drafts the script, and maps out camera movements and key visual reveals.
2. **Preview key transitions.** Inspect frames before, during, and after major transitions. Ask the agent to fix any clipping, overlapping text, or jarring motion and re-render only that scene.
3. **Add narration and export.** OpenAI or ElevenLabs turns your script into voiceover audio. The agent uses `*.timings.json` to sync the final animation and outputs an MP4, thumbnail, and SRT subtitles (when narrated). [Voice setup](https://github.com/CausalInferenceLab/causal-studio/blob/main/docs/manim-starter.md#3-review-and-add-narration-if-you-want-it)

Ask the same skill for just a script, a scene revision, or an SRT. For a full video, it delegates research, scene production, and independent review when sub-agents are available.

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

[View the skill](https://github.com/CausalInferenceLab/causal-studio/blob/skill-only/.claude/skills/manim-video-pipeline/SKILL.md) · [Voice setup guide](https://github.com/CausalInferenceLab/causal-studio/blob/main/docs/manim-starter.md#3-review-and-add-narration-if-you-want-it) · [Explore the full Causal Studio project](https://github.com/CausalInferenceLab/causal-studio)
