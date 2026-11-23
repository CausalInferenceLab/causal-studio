"""Export the Causal Studio video starter from the same source used in this checkout."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(".claude/skills/manim-video-pipeline")
EXAMPLE = Path("videos/binary-search")
CODEX_ENTRY = """---
name: manim-video-pipeline
description: Plan and render educational Manim videos from a brief, lesson, or optional notebook. Includes caption layout, narration timing, and OpenAI or ElevenLabs TTS.
---

Read and follow [the shared Manim video pipeline](../../../.claude/skills/manim-video-pipeline/SKILL.md). Run its commands from the repository root.
"""


def starter_files():
    yield Path("README.md"), (ROOT / "docs/manim-starter.md").read_bytes()
    yield Path(".agents/skills/manim-video-pipeline/SKILL.md"), CODEX_ENTRY.encode()
    for name in (".gitignore", "video.py", "requirements-video.txt", "scripts/setup_environment.sh", "LICENSE"):
        file = ROOT / name
        if file.is_file():
            yield Path(name), file.read_bytes()
    for directory in (SKILL, EXAMPLE):
        for file in sorted((ROOT / directory).rglob("*")):
            relative = file.relative_to(ROOT)
            if not file.is_file() or set(relative.parts) & {"build", "preview", "__pycache__", "node_modules"}:
                continue
            if file.suffix not in {".md", ".toml", ".txt", ".py", ".json", ".mjs", ".sh"}:
                continue
            yield relative, file.read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    targets = parser.add_mutually_exclusive_group(required=True)
    targets.add_argument("--zip", type=Path, help="Write a ZIP file")
    targets.add_argument("--directory", type=Path, help="Populate a new standalone starter directory")
    args = parser.parse_args()

    if args.zip:
        with ZipFile(args.zip, "x", compression=ZIP_DEFLATED) as archive:
            for relative, data in starter_files():
                archive.writestr((Path("causal-studio-starter") / relative).as_posix(), data)
        print(args.zip)
    else:
        args.directory.mkdir(parents=True)
        for relative, data in starter_files():
            target = args.directory / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        print(args.directory)


if __name__ == "__main__":
    main()
