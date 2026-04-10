Investigate the following topic as a literature review: $@

Derive a short slug from the topic (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.

## Workflow

1. **Plan** — Outline the scope: key questions, source types to search (papers, web, repos), time period, expected sections, and a small task ledger plus verification log. Write the plan to `outputs/.plans/<slug>.md`. Present the plan to the user and confirm before proceeding.

2. **Gather** — Use the researcher agent (see `../deep-research/references/agents/researcher.md`) when the sweep is wide enough to benefit from delegated paper triage before synthesis. For narrow topics, search directly with WebSearch and WebFetch. Researcher outputs go to `outputs/<slug>-research-*.md`. Do not silently skip assigned questions; mark them `done`, `blocked`, or `superseded`.

3. **Synthesize** — Separate consensus, disagreements, and open questions. When useful, propose concrete next experiments or follow-up reading. Generate charts by writing a Python script and running it with Bash (matplotlib/seaborn) for quantitative comparisons across papers. Use Mermaid diagrams for taxonomies or method pipelines. Before finishing the draft, sweep every strong claim against the verification log and downgrade anything that is inferred or single-source critical.

4. **Cite** — Spawn a verifier agent (see `../deep-research/references/agents/verifier.md`) via the Agent tool to add inline citations and verify every source URL in the draft.

5. **Verify** — Spawn a reviewer agent (see `../deep-research/references/agents/reviewer.md`) via the Agent tool to check the cited draft for unsupported claims, logical gaps, and single-source critical findings. Fix FATAL issues before delivering. Note MAJOR issues in Open Questions. If FATAL issues were found, run one more verification pass after the fixes.

6. **Deliver** — Save the final literature review to `outputs/<slug>.md`. Write a provenance record alongside it as `outputs/<slug>.provenance.md` listing: date, sources consulted vs. accepted vs. rejected, verification status, and intermediate research files used.
