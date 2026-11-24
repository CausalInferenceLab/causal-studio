# Causal Studio projects

Course notebooks and related data live under `book/`. Open the requested edition in `videos/<topic_slug>/<language>/`. Its `project.toml` selects the notebook and default numbered scene. Import topic helpers from `videos.<topic_slug>.shared.common` and render with `video.py render videos/<topic_slug>/<language>`. To select a different class, pass `--scene`; use `--file` for a thumbnail or other auxiliary file under `tools/`.

Older `video.py source` and `video.py render` calls that name a topic without a language still resolve to its edition. A former `_en` topic name resolves to the English edition, for example `videos/rdd_en` to `videos/rdd/en`. Use the edition path when documenting new commands. Run `video.py check` on that path after moving or adding scenes.

Generate audio into the language edition's `build/audio/` using the narration filename stem. New timing files take priority. IV and Why Causal Inference can also read their existing timing files under the topic's old `build/audio/` layout. For hard-coded waits, adjust the scene after listening to regenerated audio.

Some scenes read Tabler SVGs, local notebook datasets, or a specific font. Run the repository video asset setup when such a scene actually needs those assets. The project's repository conventions cover book builds and YouTube embedding.

Use an explicit 3Blue1Brown reference when supplied. Look for a similar educational beat in the optional local reference clone if useful. Credit the file and explain what technique is reused. Implement the scene in Manim Community Edition, using the reference for rhythm, transitions, and emphasis.
