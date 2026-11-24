# Make a Manim video with an AI agent

## 1. Clone Causal Studio and open it in your agent

```bash
git clone https://github.com/CausalInferenceLab/causal-studio.git
cd causal-studio
```

Open this folder in Claude Code or Codex. If you already have a checkout or unpacked a Causal Studio starter archive, open that folder.

## 2. Start with a request

Copy this prompt to try the included demo.

> Use `manim-video-pipeline` to render the binary search example. Set up the video environment if it is missing and open or link the resulting MP4.

Or start with your own topic.

> Use `manim-video-pipeline` to show why averages vary less with larger samples. Draw repeated samples of 5 and 50 from the same population and compare the distributions of their sample means. Give me a silent MP4 preview.

If you have a Markdown lesson, plain-text script, or Jupyter notebook, tell the agent which file to use. Give just the topic when starting from an idea. The agent prepares a video-only environment, creates the scene plan and code for a new topic, and renders the preview. If a required system tool is missing and the agent needs your help, it will identify the specific tool.

## 3. Review and add narration if you want it

After watching the preview, ask for a concrete change.

> Hold the two distributions on screen a little longer. Keep the caption below the plots and render the scene again.

When the scene is ready, you can ask for a narrated version.

> Add ElevenLabs narration. Make the script one paragraph per visual beat, use the measured timings to align the animation, and give me the merged MP4.

If you’re setting up narration for the first time, copy `.env.example` to `.env` in the repository root. For ElevenLabs, fill in `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID`. For OpenAI, fill in `OPENAI_API_KEY` and ask for OpenAI narration. The agent can render a silent preview before you set up narration.

The [Causal Studio repository](https://github.com/CausalInferenceLab/causal-studio) includes the original videos and notebooks. To revise an existing scene, tell the agent its topic, such as `videos/rdd_en`, and describe the change you want.
