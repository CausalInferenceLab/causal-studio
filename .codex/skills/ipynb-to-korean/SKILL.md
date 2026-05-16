---
name: ipynb-to-korean
description: Translate English Jupyter notebooks (.ipynb) to natural Korean without requiring an API key. Use when asked to convert an English notebook to Korean, translate English cells in a notebook, or create a `_ko.ipynb` version.
---

# ipynb-to-korean

Translate English text in a Jupyter notebook to natural Korean while preserving notebook structure.

## Workflow

1. Identify the input `.ipynb` file from the user's request.
2. Set the output path by appending `_ko` before `.ipynb`.
   - Example: `analysis.ipynb` -> `analysis_ko.ipynb`
3. Read the notebook JSON and translate only notebook cell sources.
4. Add a language switcher to the first markdown cell so each notebook can navigate to its counterpart.
   - If the notebook is standalone, sibling `.ipynb` links are fine.
   - English notebook: `**🌐 Language:** **English** | [한국어 →](./file_ko.ipynb)`
   - Korean notebook: `**🌐 언어:** [← English](./file.ipynb) | **한국어**`
   - If the notebook is published in this repo's book, use the final built page slug instead of the source `.ipynb` path.
   - English notebook in book: `**🌐 Language:** **English** | [한국어 →](/why-causal-inference-ko/)`
   - Korean notebook in book: `**🌐 언어:** [← English](/why-causal-inference-en/) | **한국어**`
5. If the notebook is part of the book, update `book/myst.yml` so the pair appears together in the TOC.
   - Follow the current `why_causal_inference` pattern used in this repo.
   - Give only the primary entry a `title:`.
   - Place the translated sibling immediately after it with `file:` and `hidden: true`.
   - This keeps language pair navigation available while avoiding duplicate visible sidebar titles.
   - If the deployed sidebar still shows the secondary Korean page, also update `book/custom.css` with `a.myst-toc-item[href$=\"/...-ko/\"]` style selectors that match the built page slug under GitHub Pages.
6. Preserve notebook structure, outputs, metadata, and execution counts unless the user asks otherwise.
7. Report the input path, output path, whether `myst.yml` was updated, and how many cells were translated.

## Translation Rules

- **Markdown cells**: Translate English prose to natural Korean. Keep headings, lists, links, LaTeX, and code fences intact.
- **Code cells**: Translate English comments and English user-facing string literals only. Do not change Python syntax, variable names, function names, library calls, or file paths unless the English text is part of a displayed label or message.
- **Outputs / metadata / kernelspec**: Do not modify.

## Editing Notes

- Prefer creating a sibling notebook with the `_ko.ipynb` suffix instead of overwriting the source notebook.
- For small or medium notebooks, translate directly and then write the new notebook file.
- For large notebooks, work cell by cell and keep a count of modified cells.
- When updating the first markdown cell, keep the original title and body content below the language switcher.
- When editing `book/myst.yml`, preserve existing order unless the user asks to move the notebook elsewhere.
- In this repo's MyST setup, a secondary language entry should use `hidden: true`; omitting `title:` alone is not enough to keep it out of the sidebar.
- For this repo's deployed site, verify the hidden page is not still exposed by path-based sidebar links. If needed, patch `book/custom.css` with `href$=` selectors that include the final built slug such as `/intro-ko/` or `/why-causal-inference-ko/`.
- For pages published in this repo's GitHub Pages site, do not leave language switcher links pointing at `.md` or `.ipynb` source files. Use root-based built routes such as `/`, `/intro-ko/`, or `/why-causal-inference-en/`.
