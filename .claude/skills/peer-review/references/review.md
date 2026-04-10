Review this research artifact: $@

**Language:** Detect the language from the user's request (`$@`). Write all output documents (plan, review) in that same language. Quoted passages from the artifact stay as-is.

Derive a short slug from the artifact name (lowercase, hyphens, no filler words, ≤5 words). All artifacts for this run live under `research/<slug>-review/`. Use this same slug for all artifacts in this run.

## Workflow

1. **Plan** — Before starting, outline what will be reviewed, the review criteria (novelty, empirical rigor, baselines, reproducibility, etc.), and any verification-specific checks needed for claims, figures, and reported metrics. Write the plan to `research/<slug>-review/plan.md`. Present the plan to the user and confirm before proceeding.

2. **Gather evidence** — Spawn a researcher agent (see `../deep-research/references/agents/researcher.md`) via the Agent tool to inspect the artifact, cited work, and any linked experimental artifacts. Save to `research/<slug>-review/research.md`. For small or simple artifacts where evidence gathering is overkill, read the artifact directly and proceed to review.

3. **Review** — Spawn a reviewer agent (see `../deep-research/references/agents/reviewer.md`) via the Agent tool with the research file to produce the final peer review with inline annotations.

4. **Fix and re-review** — If the first review finds FATAL issues, fix them and run one more reviewer pass before delivering.

5. **Deliver** — Save exactly one review artifact to `research/<slug>-review/review.md`. End with a `Sources` section containing direct URLs for every inspected external source.
