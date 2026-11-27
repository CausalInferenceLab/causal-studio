# Produce a multi-scene lesson

Use this flow when a source needs several scenes. A scene covers one idea the viewer can follow and has its own render and, when narrated, its own audio and timing file. Several related scenes can form a chapter.

## Plan the complete story

1. Set the audience, language, target duration, aspect ratio, and narration preference. Describe what the viewer should understand by the end. Keep the aspect ratio consistent across every scene.
2. Read the source together with its examples and available figures. For a notebook, use `video.py source` to read its Markdown and code as text. Inspect saved outputs directly when they contain a figure or number you need. Record the source cell, data, and assumptions for key claims. Label illustrative quantities and flag any required figures whose source data are missing.
3. Write the full narration draft before final production. Give each scene a teaching goal, estimated duration, the relevant part of the source, and a final image or sentence that hands off to the next scene. Read the script straight through so the examples, terminology, and conclusions follow naturally. Record the scene order, visual rules, and durations in `scene_plan.md`.

## Prototype, then produce by scene

1. Render a short silent excerpt of the hardest explanation with its opening, key movement, and held result. Check the transition frames and play the excerpt at normal speed in the target format. Fix framing, motion, and readability while the rest of the video is still a draft. Use a short narrated sample when voice, delivery, or sync needs an early check.
2. Once the story and sample are clear, finalize the narration by scene. Use a consistent voice and delivery. Generate an MP3 and `*.timings.json` per narrated scene, then use the measured beat lengths for its final animation. If a revision changes one scene's narration, regenerate its audio and timing together and review the cuts next to it.
3. Render scene previews at low quality. Review the content, motion, captions, and audio timing throughout each scene. Independent scenes can render in parallel. Group scenes with a shared camera or visual subject so the same positions and scale carry across the cut.
4. Assemble and watch a low-quality cut with narration before the final renders. Check the story from start to finish, actual runtime, rhythm across scenes, consistent sound and graphics, and transitions. Update only the affected scenes, then render at the delivery quality and package the MP4, thumbnail, and narrated SRT. Check the packaged playback and subtitle alignment.

## Share work and reviews

| Role | Responsibility |
|---|---|
| **Lead** | Own the run of show, shared visual rules, voice settings, scene interfaces, and final edit. Assign scene files and durations. Resolve discrepancies between the scene drafts and the complete cut. |
| **Source and script reviewer** | Map the narrative to the source and verify figures, assumptions, and observed versus hypothetical values before recording the narration. |
| **Reference researcher and visual designer** | Develop the shared look and prototype the hardest passage. Record what should carry across each cut. |
| **Scene producers** | Implement and render assigned scenes using the agreed script and measured narration. Return the render path, duration, log, and any issue that affects a neighboring scene. |
| **Independent reviewer** | Watch the sample with fresh eyes. Review scene previews and highlight failures with timestamps. Then review the complete cut for continuity and accuracy. |

Use as many people or agents as the video needs. The lead can take several roles, and the same review passes can run in sequence. When delegating, give each producer a distinct set of scene and narration files. Route shared helper and storyboard changes through the lead. If the user wants approvals, agree on checkpoints. Share the full script and a representative sample together before full production, then share the complete review cut. Inspect each scene during production and follow any review cadence the user requests.

## Example outline for a ten-minute introduction

This example uses the Why Causal Inference? notebook. The times are planning estimates. Update them once narration has been measured.

| Time | Scene goal |
|---|---|
| 00:00–00:45 | Why a school might consider buying tablets and what the 125-point observed gap seems to suggest. |
| 00:45–02:10 | Show the same schools with and without tablets, then hide the outcomes that are unavailable in real life. |
| 02:10–03:35 | Unpack the observed gap as the −75-point effect for the two treated schools plus a 200-point baseline difference. |
| 03:35–04:45 | Show how school resources can influence both tablet adoption and test scores. |
| 04:45–06:15 | Show what random assignment changes about the comparison, including chance imbalance in a single draw. |
| 06:15–08:20 | Walk through the notebook's online class experiment and its reported estimates. |
| 08:20–10:00 | Return to the tablet decision and ask which comparison would approximate the ideal experiment. |

Prototype the move from the observed groups to the same schools’ hypothetical scores. Keep the observed marks traceable as the alternate outcomes appear.
