# Causal Studio projects

The lesson and any related data live under `book/`. For an existing project, read its `project.toml` when available. It records the notebook and the default Manim scene. To work on a different scene, select its numbered file under `scenes/` and pass its class to the render command. Older `src/` entry points and `src/scripts/` narration paths still work.

For a bilingual topic, read the notebook and narration for the requested language. Keep established paths for timings which existing scenes read, including language subfolders. Pass those paths explicitly to the audio command. For existing hard-coded WAIT values, adjust only the scene in scope after listening to regenerated audio.

Some scenes read Tabler SVGs, local notebook datasets, or a specific font. Run the repository video asset setup when such a scene actually needs those assets. The project's repository conventions cover book builds and YouTube embedding.

Use an explicit 3Blue1Brown reference when supplied. Look for a similar educational beat in the optional local reference clone if useful. Credit the file and explain what technique is reused. Implement the scene in Manim Community Edition, using the reference for rhythm, transitions, and emphasis.
