# Causal Studio projects

The lesson and any related data live under `book/`. For a bilingual topic, open `videos/<topic>/ko` or `videos/<topic>/en`. The `project.toml` in that folder selects the notebook and default Manim scene for that language. Use matching numbered files in `scenes/` and `narration/`. Import helpers from `videos.<topic>.shared.common` and render with the repository launcher. Older topic-level manifests and scene collection entry points under `src/` are kept for rendering.

Generate audio into the language edition's `build/audio/` using the narration filename stem. New timing files take priority. IV and Why Causal Inference can also read their existing timing files under the topic's old `build/audio/` layout. For hard-coded waits, adjust the scene after listening to regenerated audio.

Some scenes read Tabler SVGs, local notebook datasets, or a specific font. Run the repository video asset setup when such a scene actually needs those assets. The project's repository conventions cover book builds and YouTube embedding.

Use an explicit 3Blue1Brown reference when supplied. Look for a similar educational beat in the optional local reference clone if useful. Credit the file and explain what technique is reused. Implement the scene in Manim Community Edition, using the reference for rhythm, transitions, and emphasis.
