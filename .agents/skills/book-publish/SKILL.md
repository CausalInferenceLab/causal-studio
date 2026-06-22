---
name: book-publish
description: |
  Publish a notebook or page into this Jupyter Book by adding it to book/myst.yml and building the book to verify output.
  Use when asked to publish a notebook, include a page in the book, update the TOC, or run a production-style Jupyter Book build.
---

# Book Publish

## Workflow

1. Confirm the target file exists under `book/`.
2. Edit `book/myst.yml` — add the page under `project.toc` with a concise English title.
3. Sync dependencies if the notebook adds new imports:
   - Runtime packages → `requirements-book.txt`
   - Binder reads `binder/requirements.txt` (points to `../requirements-book.txt`)
   - System packages on Binder → `binder/apt.txt`
4. Build to verify:

```bash
cd book && source ../.venv/bin/activate && jupyter-book build --site
```

5. If the build fails, fix the notebook or TOC issue and rebuild.

## Notes

- Do not duplicate the notebook; publish the original path.
- Prefer short English titles in the TOC unless the user specifies otherwise.
- For local preview only, use the `book-serve` skill instead.
- Treat Binder compatibility as part of publish verification when the page must run on MyBinder.
