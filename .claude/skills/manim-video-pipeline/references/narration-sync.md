# Narration and timing

## Generate a timing track

The same command supports OpenAI and ElevenLabs. Run one provider per language/voice version. If you need to create the repository root's ignored `.env`, copy `.env.example` and fill in the settings for your chosen provider. Shell environment variables also work.

| Provider | Required setting | Optional setting |
|---|---|---|
| `openai` | `OPENAI_API_KEY` | `OPENAI_TTS_VOICE` (defaults to `coral`), `OPENAI_TTS_INSTRUCTIONS` |
| `elevenlabs` | `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID` | `--voice` overrides the configured voice ID |

```bash
PIPELINE=.claude/skills/manim-video-pipeline/scripts/pipeline.py
python "$PIPELINE" audio --provider openai \
  --script videos/my_topic/en/narration/01_intro.txt \
  --output videos/my_topic/en/build/audio/01_intro.mp3
```

Use `--provider elevenlabs` for ElevenLabs. Add `--dry-run` to inspect chunks and paths without a key or provider request. Use `--gap 0.2` if the script benefits from a short pause between beats. Regenerate audio and timings together when the script, language, provider, voice, or speed changes.

## Build a Scene against the measured audio

- A blank line starts a new beat. Put a single visual action or claim in each paragraph. Keep it short enough to say naturally before the action ends. The command splits very long paragraphs into multiple chunks, so check the chunk count before creating the visual timeline.
- The tool measures each decoded audio chunk and places it on the exact PCM sample timeline before encoding the combined MP3. JSON includes `chunks[].text/start/end/duration`, `totalDuration`, and provider settings. An optional gap is reflected in subsequent start times. The fields mark paragraph boundaries, so place word-specific actions by listening to that chunk.
- Write down the correspondence in the scene plan. For example, Beat 2 says “discard the left half”, the highlight sits on the midpoint at the start, the left cells dim at that phrase, and the comparison caption leaves before Beat 3.
- Use `BeatClock` from `scripts/manim_timing.py` to wait until measured beat boundaries. The preview path uses provisional durations. Fit `self.play(..., run_time=...)` before the next boundary and use the remaining time as a hold. The render command disables partial-animation caching so timing uses actual rendered frame counts. If a beat runs over, remove a distracting action or split the beat and regenerate the timing track. Review at 480p and at the final frame rate.
- Keep the rendered visual tail at least 0.5 s beyond narration. The mux command checks that the voice fits and pads the audio track to preserve the tail. Watch the combined preview around the first and last words of each beat before final assembly.

Use the SRT from `video.py package` for selectable captions. It wraps the transcript at 38 display columns per line, with up to two lines per cue, and divides each measured beat by the amount of text in each cue. Pauses between beats stay clear. Play the cut with subtitles on and adjust boundaries that fall on the wrong words. Use a listening or word-alignment pass when a cue needs precise placement.
