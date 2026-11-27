# Why Causal Inference?

English · 16:9 · 10:00 target · narrated lesson for viewers who know how to read a mean

The viewer should be able to identify which counterfactual a decision needs, explain how selection can reverse an observed association, and say what random assignment adds to the comparison.

[Scene narration](narration/) · [Source notebook](../../../book/why_causal_inference/why_causal_inference_en.ipynb)

| Target | Scene | Screen progression | Source cells (zero-based) |
|---|---|---|---|
| 0:00–0:45 | The purchase | Place a tablet and a stack of books on a school budget sheet. Replace it with four schools on a single score ruler. Pair the schools by tablet adoption and end on the observed +125 gap. | 3, 5, 10, 13 |
| 0:45–2:10 | Same schools, different choice | Keep the two teal schools. Let the gray schools leave. Add the two hollow no-tablet alternatives on separate lanes and gather their mean at 750. Hold the −75 contrast, then let the hollow marks recede. | 8–14, 17 |
| 2:10–3:35 | Two distances | Keep 675 fixed. Walk along the same ruler from 550 to 750 and back to 675. Mark the first distance as selection and the second as the effect for the two treated schools. | 17, 23–27 |
| 3:35–4:45 | A common cause | Bring in school resources between tablets and test scores. Draw the two paths out from resources, then show the tablet-to-score path the viewer wants to isolate. | 19–20 |
| 4:45–6:15 | What random assignment changes | Shuffle a larger set of schools with visible resource differences. Show two possible assignments with opposite small imbalances. Resolve to what the mean difference estimates across assignments. | 28–34 |
| 6:15–8:20 | The online classroom experiment | Deal students into three formats. Keep blended visible while lining up fully online and in-person means. Show the estimated −4.91-point exam gap and hold before discussing chance variation. | 36–40 |
| 8:20–10:00 | The comparison you need | Return to the budget sheet. Visually distinguish a tablet-versus-no-tablet trial from a trial of tablets versus a library upgrade. Close on the original score ruler and the counterfactual question. | 3, 42 |

## Preview passage

The rendered excerpt joins the observed-gap hold at the end of Scene 01 to the same-schools reveal in Scene 02. It does not reproduce Scene 02 in full. English text offers just enough context to read the silent comparison. The final cut retimes each animation to the spoken narration.

- Keep the score ruler and teal 675 average through both comparisons. Individual teal marks separate vertically when school identity becomes important.
- Let both school scores contribute visible copies to their average. The observed comparison can then leave the frame while the treated mean stays.
- Use a short camera move between the two dense holds. During the reveal, hollow marks move away from the original scores to show the imagined outcomes of the same two schools. The violet average then replaces the gray comparison.
- Let the new gold arrow read leftward, from 750 to 675. Reserve the lower margin for captions and leave open corners around the graph.

## References and checks

- In [The Lattice Bacteria Puzzle at 0:31–0:35](https://www.youtube.com/watch?v=d0ai33oqqDE&t=31s), the composition widens while keeping a mark traceable. Use a score anchor through the reframe. The exact source of the short was unavailable.
- The official [Central Limit Theorem transformation](https://github.com/3b1b/videos/blob/31f8ffe785e860477a6051fde983c02c7d165bc2/_2023/clt/main.py#L815-L850) aligns two states on one plot, staggers nearby labels, and pauses before further reframing. Keep the position of the ruler through the new comparison. This is a separate implementation reference.
- Notebook Cell 14 labels the observed +125 as ATE. The script follows Cells 10–13 and 17, where +125 is the observed gap, and −75 is the hypothetical average effect for the treated schools. Scores for the same schools under the other assignment are toy values.
- The actual experiment compares the unrounded group means 73.635263 and 78.547485. The spoken one-decimal means are 73.6 and 78.5. The unrounded difference is about −4.91. The draft scopes this estimate to the experiment.

The independent silent screening found two temporary label collisions, an overshooting dashed guide, and an ambiguous subtraction direction. The revision separates the labels, attaches each guide to its moving ring, and names the subtraction in the final hold.

## Final edit

The completed edit runs 10:04 with seven chapters. The opening draft expanded by three worked examples. Scene 02 contrasts the effect for two tablet schools with the four-school average. Scene 05 applies two random assignments to fixed toy scores. Scene 07 compares two hypothetical before-and-after trends. Narration uses ElevenLabs. Each beat is timed to its audio, and English subtitle cues use the recorded word positions.

| Start | Chapter |
|---|---|
| 0:00 | The Purchase |
| 0:34 | Same Schools, Different Choice |
| 2:31 | Two Distances |
| 3:34 | A Common Cause |
| 4:23 | What Random Assignment Changes |
| 6:26 | The Online Classroom Experiment |
| 7:58 | The Comparison You Need |
