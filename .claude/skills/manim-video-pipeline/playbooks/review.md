# Review a rendered scene or cut

Use for a scene preview, transition check, or assembled video. Return findings with timestamps and any requested contact sheets. A review-only request ends with the findings. The lead assigns fixes separately.

- For an independent first pass, give the reviewer the video and target screen size. Withhold the intended reveal and implementation until after their first muted viewing. At normal speed, have them report what changed, what the relationship means, and where they lost track of the subject.
- Inspect the opening, key action, and held result. Check collisions, caption space, contrast, pacing, camera movement, and continuity between scenes. For a vertical clip, inspect at phone width. Compare with the storyboard and the [visual review guide](../references/manim-code-patterns.md#review-the-motion) after the blind pass.
- For a narrated cut, replay the relevant passages with sound when available. Check that the picture changes on the words that give it meaning and that the captions are legible and in sync. Report which parts you could verify.
- To isolate a transition, use scene-relative times for a scene and edit-relative times for the assembled cut. Take before, during, and after frames around the move.

```bash
.venv-video/bin/python video.py review "$SCENE_MP4" --transition 2.1 3.4 \
  --output videos/my_topic/en/build/review/03_comparison
```
