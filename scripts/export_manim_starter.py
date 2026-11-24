"""Export the Causal Studio video starter from the same source used in this checkout."""

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(".claude/skills/manim-video-pipeline")
EXAMPLE = Path("videos/binary-search")
SKILL_ONLY_FILES = (
    "SKILL.md",
    "references/ffmpeg-recipes.md",
    "references/manim-code-patterns.md",
    "references/narration-sync.md",
    "references/script-writing-guide.md",
    "scripts/concat_videos.sh",
    "scripts/find_latest_render.sh",
    "scripts/manim_timing.py",
    "scripts/mix_bgm.sh",
    "scripts/mux_audio.sh",
    "scripts/pipeline.py",
    "scripts/speech.py",
    "templates/scene_plan.md",
)
CODEX_ENTRY = """---
name: manim-video-pipeline
description: Design and render educational Manim videos from a brief, lesson, or optional notebook. Includes 3Blue1Brown reference study, animation prototypes, and OpenAI or ElevenLabs narration.
---

Read and follow [the shared Manim video pipeline](../../../.claude/skills/manim-video-pipeline/SKILL.md). Run its commands from the repository root.
"""


def starter_files(skill_only=False):
    guide = "manim-skill-only.md" if skill_only else "manim-starter.md"
    yield Path("README.md"), (ROOT / "docs" / guide).read_bytes()
    workflow_image = Path("assets/manim-workflow.png")
    yield workflow_image, (ROOT / "docs" / workflow_image).read_bytes()
    yield Path(".agents/skills/manim-video-pipeline/SKILL.md"), CODEX_ENTRY.encode()
    for name in (
        ".env.example", ".gitignore", "video.py", "requirements-video.txt",
        "scripts/setup_environment.sh", "scripts/setup_video_assets.sh", "LICENSE",
    ):
        file = ROOT / name
        if file.is_file():
            yield Path(name), file.read_bytes()
    if skill_only:
        for name in SKILL_ONLY_FILES:
            relative = SKILL / name
            yield relative, (ROOT / relative).read_bytes()
        return
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
    parser.add_argument("--skill-only", action="store_true", help="Export shared tools without project or demo sources")
    args = parser.parse_args()

    if args.zip:
        folder = Path("causal-studio-skill" if args.skill_only else "causal-studio-starter")
        with ZipFile(args.zip, "x", compression=ZIP_DEFLATED) as archive:
            for relative, data in starter_files(args.skill_only):
                archive.writestr((folder / relative).as_posix(), data)
        print(args.zip)
    else:
        args.directory.mkdir(parents=True)
        for relative, data in starter_files(args.skill_only):
            target = args.directory / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        print(args.directory)


if __name__ == "__main__":
    main()
