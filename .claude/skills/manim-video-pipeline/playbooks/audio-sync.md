# Record narration or repair sync

Use the requested scene's script, existing MP3, and adjacent timing file. Return the requested voice or synchronization result.

- **Record.** Choose the requested provider and voice. Use the [narration guide](../references/narration-sync.md) to generate the MP3 and timing file as a pair. Listen for correct wording, pronunciation, pace, and pauses. An audio-only request ends with these two files.
- **Synchronize.** Compare the animation against the existing verified audio and timing file before deciding what must change. When narration stays the same, reuse its audio and adjust the affected visual beats. When rerecording is in scope, generate fresh audio and timings together. Use measured beat boundaries and keep at least 0.5 seconds of visual tail after the narration.
- **Deliver the requested scene.** Render it with the [single-scene playbook](scene.md) only when a synced video is requested. Use `video.py mux SCENE.mp4 NARRATION.mp3 OUTPUT.mp4` to hear it in context and check the relevant spoken cues.

Use the [caption playbook](captions.md) for a change confined to words or timestamps in subtitles.
