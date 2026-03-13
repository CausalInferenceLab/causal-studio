---
name: book-publish
description: Publish a notebook or page into this Jupyter Book by adding it to book/myst.yml and building the book to verify output. Use when asked to publish a notebook, include a page in the book, update the TOC, or run a production-style Jupyter Book build.
---

# Book Publish

Use this when a user wants a notebook or page to appear in the built book.

## Workflow

1. Confirm the target file exists under `book/`.
2. Edit `book/myst.yml` and add the page under `project.toc`.
3. Keep the title concise. If the notebook already has a clear top-level heading, prefer a short English title in the TOC unless the user asks otherwise.
4. If the new page adds runtime imports, sync book runtime dependencies before building.
   - Python packages needed by published notebooks belong in `requirements-book.txt`.
   - Binder uses `binder/requirements.txt`, which should continue to point at `../requirements-book.txt`.
   - If a notebook needs a system package on Binder, add it to `binder/apt.txt`.
5. Build the book to verify it renders:

```bash
if [ -d book ]; then
  cd book
elif [ -f myst.yml ]; then
  :
else
  echo "book directory or myst.yml not found" >&2
  exit 1
fi

if [ -f ../.venv/bin/activate ]; then
  source ../.venv/bin/activate
elif [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
else
  echo ".venv not found" >&2
  exit 1
fi

jupyter-book build --site
```

## Notes

- Do not create a second copy of the notebook just for publishing unless the user asks.
- If the build fails, fix the notebook or TOC issue and rebuild.
- When the page should run on MyBinder, treat Binder compatibility as part of publish verification, especially for packages with native/system dependencies.
- If the user only wants local preview, use the `book-serve` skill instead.
