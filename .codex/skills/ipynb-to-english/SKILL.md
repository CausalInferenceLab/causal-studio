---
name: ipynb-to-english
description: Translate Korean Jupyter notebooks (.ipynb) to natural English without requiring an API key. Use when asked to convert a Korean notebook to English, translate Korean cells in a notebook, or create an `_en.ipynb` version.
---

# ipynb-to-english

Translate Korean text in a Jupyter notebook to natural English while preserving notebook structure.

## Workflow

1. Identify the input `.ipynb` file from the user's request.
2. Set the output path by appending `_en` before `.ipynb`.
   - Example: `analysis.ipynb` -> `analysis_en.ipynb`
3. Read the notebook JSON and translate only notebook cell sources.
4. Add a language switcher to the first markdown cell so each notebook can navigate to its counterpart.
   - Korean notebook: `**🌐 언어:** [← English](./file_en.ipynb) | **한국어**`
   - English notebook: `**🌐 Language:** **English** | [한국어 →](./file_ko.ipynb)`
5. If the notebook is part of the book, update `book/myst.yml` so the pair appears together in the TOC.
   - Follow the current `why_causal_inference` pattern used in this repo.
   - Give only the primary entry a `title:`.
   - Place the translated sibling immediately after it with `file:` and `hidden: true`.
   - This keeps language pair navigation available while avoiding duplicate visible sidebar titles.
   - If the deployed sidebar still shows the secondary Korean page, also update `book/custom.css` with `a.myst-toc-item[href$=\"/...-ko/\"]` style selectors that match the built page slug under GitHub Pages.
6. Preserve notebook structure, outputs, metadata, and execution counts unless the user asks otherwise.
7. Report the input path, output path, whether `myst.yml` was updated, and how many cells were translated.

## Translation Rules

- **Markdown cells**: Translate Korean prose to natural English. Keep headings, lists, links, LaTeX, and code fences intact.
- **Code cells**: Translate Korean comments and Korean user-facing string literals only. Do not change Python syntax, variable names, function names, library calls, or file paths unless the Korean text is part of a displayed label/message.
- **Outputs / metadata / kernelspec**: Do not modify.

## Editing Notes

- Prefer creating a sibling notebook with the `_en.ipynb` suffix instead of overwriting the source notebook.
- For small or medium notebooks, translate directly and then write the new notebook file.
- For large notebooks, work cell by cell and keep a count of modified cells.
- When updating the first markdown cell, keep the original title and body content below the language switcher.
- When editing `book/myst.yml`, preserve existing order unless the user asks to move the notebook elsewhere.
- In this repo's MyST setup, a secondary language entry should use `hidden: true`; omitting `title:` alone is not enough to keep it out of the sidebar.
- For this repo's deployed site, verify the hidden page is not still exposed by path-based sidebar links. If needed, patch `book/custom.css` with `href$=` selectors that include the final built slug such as `/intro-ko/` or `/why-causal-inference-ko/`.
