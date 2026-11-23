"""Read, render, and narrate an educational Manim project."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import tomllib

from speech import add_audio_arguments, generate_audio, media_duration


ROOT = Path(__file__).resolve().parents[4]
SOURCE_TYPES = {".md", ".txt", ".ipynb"}


def init_project(args):
    project = args.project.resolve()
    if args.source:
        source = args.source.resolve()
        if source.suffix.lower() not in SOURCE_TYPES or not source.is_file():
            raise ValueError("Provide an existing Markdown, text, or Jupyter notebook source.")
    else:
        source = project / "lesson.md"
    project.mkdir(parents=True, exist_ok=True)
    manifest = project / "project.toml"
    with manifest.open("x", encoding="utf-8") as output:
        output.write(
            f"source = {json.dumps(os.path.relpath(source, project), ensure_ascii=False)}\n"
            'scene_file = "scenes/scene_01.py"\n'
            'scene_class = "Scene01"\n'
        )
    if not args.source and not source.exists():
        source.write_text(f"# {project.name}\n\n{args.brief or 'Write your lesson here.'}\n", encoding="utf-8")
    for directory in ("scenes", "narration"):
        (project / directory).mkdir(exist_ok=True)
    plan = project / "scene_plan.md"
    if not plan.exists():
        plan.write_text(
            "# Scene 01\n\n| Beat | Narration cue | Visual change | What leaves the frame |\n"
            "|---|---|---|---|\n| 1 | | | |\n",
            encoding="utf-8",
        )
    print(manifest)


def read_source(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() != ".ipynb":
        return text
    parts = []
    for index, cell in enumerate(json.loads(text)["cells"], 1):
        kind = cell["cell_type"]
        if kind in {"markdown", "code"}:
            parts.append(f"[Cell {index} · {kind}]\n{''.join(cell['source'])}")
    return "\n\n".join(parts)


def render(args, project, config):
    file = args.file.resolve() if args.file else project / config["scene_file"]
    scripts = str(Path(__file__).resolve().parent)
    pythonpath = os.pathsep.join(filter(None, (scripts, os.environ.get("PYTHONPATH"))))
    subprocess.run(
        [sys.executable, "-m", "manim", f"-q{args.quality}", "--disable_caching",
         "--media_dir", str(project / "build" / "manim"),
         str(file), args.scene or config["scene_class"]],
        cwd=project,
        env={**os.environ, "PYTHONPATH": pythonpath},
        check=True,
    )


def mux(args):
    if args.output.suffix.lower() != ".mp4":
        raise ValueError("Set an .mp4 output path.")
    if args.output.resolve() in {args.video.resolve(), args.audio.resolve()}:
        raise ValueError("Choose a separate output path for the muxed preview.")
    video = media_duration(args.video)
    audio = media_duration(args.audio)
    if video + 0.02 < audio:
        raise ValueError(f"Video ({video:.2f}s) ends before narration ({audio:.2f}s). Retiming the scene is required.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=args.output.parent) as directory:
        preview = Path(directory) / "preview.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(args.video), "-i", str(args.audio),
             "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
             "-af", "apad", "-shortest", str(preview)],
            check=True,
        )
        preview.replace(args.output)
    print(args.output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    init = commands.add_parser("init", help="Create a lesson project")
    init.add_argument("project", type=Path)
    inputs = init.add_mutually_exclusive_group()
    inputs.add_argument("--source", type=Path, help="Existing .md, .txt, or .ipynb file")
    inputs.add_argument("--brief", help="Start a lesson from a description")
    source = commands.add_parser("source", help="Print the lesson without executing notebook cells")
    source.add_argument("project", type=Path)
    preview = commands.add_parser("render", help="Render a Manim scene")
    preview.add_argument("project", type=Path)
    preview.add_argument("--file", type=Path, help="Override the scene file (relative to the working directory)")
    preview.add_argument("--scene", help="Override the Manim class")
    preview.add_argument("--quality", choices=("l", "m", "h", "p", "k"), default="l")
    add_audio_arguments(commands.add_parser("audio", help="Generate MP3 and beat timings"), ROOT)
    combine = commands.add_parser("mux", help="Attach narration and preserve the visual tail")
    for field in ("video", "audio", "output"):
        combine.add_argument(field, type=Path)
    args = parser.parse_args()

    if args.action == "init":
        init_project(args)
    elif args.action == "audio":
        generate_audio(args)
    elif args.action == "mux":
        mux(args)
    else:
        project = args.project.resolve()
        with (project / "project.toml").open("rb") as manifest:
            config = tomllib.load(manifest)
        if args.action == "source":
            print(read_source(project / config["source"]))
        else:
            render(args, project, config)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.CalledProcessError) as error:
        sys.exit(f"Error: {error}")
