Compare sources for: $@

**Language:** Detect the language from the user's request (`$@`). Write all output documents (plan, comparison matrix) in that same language. Source titles and URLs stay in their original language.

Derive a short slug from the comparison topic (lowercase, hyphens, no filler words, ≤5 words). All artifacts for this run live under `research/<slug>/`. Use this same slug for all artifacts in this run.

## Workflow

1. **Plan** — Outline the comparison plan: which sources to compare, which dimensions to evaluate, expected output structure. Write the plan to `research/<slug>/plan.md`. Present the plan to the user and confirm before proceeding.

2. **Gather** — Use the researcher agent (see `../deep-research/references/agents/researcher.md`) via the Agent tool to gather source material when the comparison set is broad. For 2-3 items you can search directly with WebSearch and WebFetch.

3. **Compare** — Build a comparison matrix covering: source, key claim, evidence type, caveats, confidence. Distinguish agreement, disagreement, and uncertainty clearly. Generate charts by writing a Python script and running it with Bash (matplotlib/seaborn) when the comparison involves quantitative metrics. Use Mermaid for method or architecture comparisons.

4. **Cite** — Spawn a verifier agent (see `../deep-research/references/agents/verifier.md`) via the Agent tool to verify sources and add inline citations to the final matrix.

5. **Deliver** — Save exactly one comparison to `research/<slug>/comparison.md`. End with a `Sources` section containing direct URLs for every source used.
