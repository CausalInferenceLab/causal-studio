---
name: minimal-ipynb
description: Simplify an existing Jupyter notebook into a concise, minimal, runnable `.ipynb` with only the essential data loading, transformations, analysis, and outputs. Use when the input notebook is verbose, repetitive, theory-heavy, or hard to read; when the user wants a cleaner notebook built from an existing `.ipynb` plus one or more CSV paths; or when the user wants to keep only a selected subset of CSV files and remove all content tied to the others. Write the simplified notebook in the same directory as the source notebook unless the user gives a different output path.
---

# minimal-ipynb

Turn a complicated notebook into a compact working notebook.
Optimize for execution, readability, and directness. Do not preserve theory, long prose, exploratory dead ends, or redundant code unless the user explicitly asks for them.

## Workflow

1. Lock the scope.
- Identify the source `.ipynb`.
- Identify the CSV files that must remain in scope.
- If the original notebook uses more CSV files than the user wants, treat every non-selected CSV as out of scope and remove its related cells, variables, plots, joins, and commentary.

2. Read the notebook top to bottom.
- Extract the minimum path from raw data to final result.
- Keep only cells required for:
  - imports
  - loading the selected CSV files
  - essential cleaning or feature preparation
  - the core analysis or visualization the user still needs
  - a short result summary when needed

3. Rewrite, do not merely trim.
- Prefer rebuilding the notebook structure over preserving the old cell layout.
- Merge fragmented code cells when that improves flow.
- Split oversized code cells only when it improves readability.
- Replace long markdown with one or two short markdown cells at most.
- Avoid “background”, “theory”, “interpretation”, and “next steps” sections unless directly required.

4. Keep the notebook runnable.
- Preserve required imports and file paths.
- Remove unused imports, helper functions, intermediate DataFrames, and abandoned experiments.
- Do not leave references to deleted CSVs.
- If the original notebook depends on multiple files but the user wants only some of them, adjust the logic so the remaining notebook still runs cleanly with only those files.
- Prefer explicit, local variables over clever abstractions.

5. Keep explanations minimal.
- Use short markdown headings such as `Load data`, `Prepare`, `Analyze`, `Result`.
- Keep prose to the minimum needed to orient the reader.
- Let the code show the workflow.
- Prefer small comments inside code only when they prevent confusion.

6. Write the output beside the source notebook.
- Default naming: append `_minimal` before `.ipynb`.
- Example: `analysis.ipynb` -> `analysis_minimal.ipynb`
- If the user specifies an output filename, use it.

7. Validate before finishing.
- Check notebook JSON validity.
- Run the notebook when the environment allows.
- If full execution is not possible, at least verify that cell order, imports, and file references are coherent and state what was not executed.

## Editing Rules

- Prefer `pandas` code that is direct and easy to scan.
- Remove duplicate plots; keep the one that best answers the task.
- Keep outputs lightweight; avoid huge tables unless the final result depends on them.
- Replace exploratory print spam with one concise display or summary.
- Keep naming practical; do not preserve cryptic temporary variable chains if they can be simplified safely.
- Preserve semantics. Do not silently change the business question or statistical logic just to make the notebook shorter.

## CSV Selection Rules

- If the user names the CSV files to keep, load only those files in the new notebook.
- Remove cells that inspect, merge, clean, or visualize dropped CSV files.
- If a dropped CSV provided columns later used by the notebook, either:
  - remove the dependent analysis entirely, or
  - replace it with an equivalent path that uses only the kept CSV files
- Never leave dead code that assumes removed files still exist.

## Structure Target

Prefer this shape:

1. Title markdown cell
2. Short setup/imports code cell
3. Short load-data code cell
4. One or two preparation code cells
5. One or two analysis or visualization code cells
6. Optional short conclusion markdown cell

Do not add extra sections unless they materially improve comprehension.

## Reference

Use [.codex/skills/jupyter-notebook/SKILL.md](/Users/edgar/Repository/causal-studio/.codex/skills/jupyter-notebook/SKILL.md) only as a secondary reference for safe notebook editing and notebook structure. Follow this skill first whenever brevity and pragmatism are the goal.
