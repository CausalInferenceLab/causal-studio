"""Read, render, and narrate an educational Manim project."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory
import tomllib

from project_layout import LANGUAGE_TAG, SOURCE_TYPES, TOPIC_SLUG, check_project, resolve_project, scene_classes
from speech import add_audio_arguments, generate_audio, media_duration
from video_outputs import export_captions, package, review, video_info


ROOT = Path(__file__).resolve().parents[4]


def init_project(args):
    project = args.project.resolve()
    scene_file = "scenes/scene_01.py"
    if args.lang:
        if not LANGUAGE_TAG.fullmatch(args.lang):
            raise ValueError("Use a language tag such as en, ko, or en-US.")
        project = project / args.lang
    if args.lang or (project.parent.parent.name == "videos" and LANGUAGE_TAG.fullmatch(project.name)):
        if not TOPIC_SLUG.fullmatch(project.parent.name):
            raise ValueError("Use a lowercase topic slug with underscores, such as binary_search.")
        scene_file = "scenes/scene_01_intro.py"
    if args.source:
        source = args.source.resolve()
        if source.suffix.lower() not in SOURCE_TYPES or not source.is_file():
            raise ValueError("Provide an existing Markdown, text, or Jupyter notebook source.")
    else:
        source = project / "lesson.md"
    plan = project / "scene_plan.md"
    if not plan.exists():
        template = Path(__file__).resolve().parents[1] / "templates" / "scene_plan.md"
        scene_plan = template.read_text(encoding="utf-8")
    else:
        scene_plan = None
    project.mkdir(parents=True, exist_ok=True)
    manifest = project / "project.toml"
    with manifest.open("x", encoding="utf-8") as output:
        output.write(
            f"source = {json.dumps(os.path.relpath(source, project), ensure_ascii=False)}\n"
            f'scene_file = "{scene_file}"\n'
            'scene_class = "Scene01"\n'
        )
    if not args.source and not source.exists():
        source.write_text(f"# {project.name}\n\n{args.brief or 'Write your lesson here.'}\n", encoding="utf-8")
    for directory in ("scenes", "narration"):
        (project / directory).mkdir(exist_ok=True)
    if scene_plan is not None:
        plan.write_text(scene_plan, encoding="utf-8")
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


def select_scene_file(args, project, config):
    file = args.file.resolve() if args.file else project / config["scene_file"]
    if args.file is None and args.scene and args.scene != config["scene_class"]:
        matches = [p for p in (project / "scenes").glob("scene_*.py") if args.scene in scene_classes(p)]
        if len(matches) > 1:
            raise ValueError(f"Found {args.scene} in multiple files. Select one with --file.")
        if matches:
            file = matches[0]
    return file


def render(args, project):
    scripts = Path(__file__).resolve().parent
    pythonpath = os.pathsep.join(filter(None, (str(scripts), str(ROOT), os.environ.get("PYTHONPATH"))))
    result = {"ok": False, "scene": args.scene, "log": None}
    try:
        if not project.is_dir():
            raise ValueError(f"Video project not found: {project}")
        media = project / "build/manim"
        logs = project / "build/logs"
        media.mkdir(parents=True, exist_ok=True)
        logs.mkdir(parents=True, exist_ok=True)
        with (NamedTemporaryFile(mode="w", encoding="utf-8", prefix="render-", suffix=".log",
                                 dir=logs, delete=False) as log,
              TemporaryDirectory(prefix=".render-", dir=media) as stage):
            stage = Path(stage)
            result["log"] = log.name
            try:
                with (project / "project.toml").open("rb") as manifest:
                    config = tomllib.load(manifest)
                scene = args.scene or config["scene_class"]
                if not scene.isidentifier():
                    raise ValueError(f"Use a Python class name for the scene: {scene}")
                result["scene"] = scene
                file = select_scene_file(args, project, config)
                command = [sys.executable, "-m", "manim", f"-q{args.quality}", "--disable_caching",
                           "--media_dir", str(stage), "--format", "mp4", "-o", scene, str(file), scene]
                log.write(f"Rendering {scene} from {file}\n")
                with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      text=True, errors="replace", cwd=project,
                                      env={**os.environ, "PYTHONPATH": pythonpath}) as process:
                    for line in process.stdout:
                        log.write(line)
                        log.flush()
                        if not args.json:
                            print(line, end="", file=sys.stderr)
                    result["exit_code"] = process.wait()
                if result["exit_code"]:
                    raise RuntimeError(f"Manim exited with status {result['exit_code']}")
                candidates = [path for path in stage.rglob(f"{scene}.mp4")
                              if "partial_movie_files" not in path.relative_to(stage).parts]
                if len(candidates) != 1:
                    raise RuntimeError(f"Expected one fresh MP4 for {scene}, found {len(candidates)}")
                rendered = candidates[0]
                duration, *_ = video_info(rendered)
                destination = media / rendered.relative_to(stage)
                destination.parent.mkdir(parents=True, exist_ok=True)
                rendered.replace(destination)
                result.update(ok=True, video=str(destination), duration=round(duration, 6))
            except (OSError, ValueError, KeyError, RuntimeError, SyntaxError) as error:
                log.write(f"\nError: {error}\n")
                raise
    except (OSError, ValueError, KeyError, RuntimeError, SyntaxError) as error:
        result["error"] = str(error)

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    elif result["ok"]:
        print(f"Rendered {result['video']} ({result['duration']:.3f}s)\nRender log: {result['log']}")
    else:
        log_hint = f"\nRender log: {result['log']}" if result["log"] else ""
        print(f"Error: {result['error']}{log_hint}", file=sys.stderr)
    if not result["ok"]:
        sys.exit(1)


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
    init.add_argument("--lang", help="Create a language edition under the topic, such as en or ko")
    inputs = init.add_mutually_exclusive_group()
    inputs.add_argument("--source", type=Path, help="Existing .md, .txt, or .ipynb file")
    inputs.add_argument("--brief", help="Start a lesson from a description")
    source = commands.add_parser("source", help="Print the lesson without executing notebook cells")
    source.add_argument("project", type=Path)
    check = commands.add_parser("check", help="Verify a project's folder, manifest, scene names, and narration")
    check.add_argument("project", type=Path)
    preview = commands.add_parser("render", help="Render a Manim scene")
    preview.add_argument("project", type=Path)
    preview.add_argument("--file", type=Path, help="Override the scene file (relative to the working directory)")
    preview.add_argument("--scene", help="Override the Manim class")
    preview.add_argument("--quality", choices=("l", "m", "h", "p", "k"), default="l")
    preview.add_argument("--json", action="store_true", help="Print the result and log path as JSON")
    frames = commands.add_parser("review", help="Extract before, during, and after frames for transitions")
    frames.add_argument("video", type=Path)
    frames.add_argument("--transition", type=float, nargs=2, action="append", required=True,
                        metavar=("START", "END"), help="Transition time range in seconds. Repeat for more transitions.")
    frames.add_argument("--output", type=Path, help="Directory for the PNG frames and contact sheet")
    publish = commands.add_parser("package", help="Assemble a final MP4, thumbnail, and narration SRT")
    captions = commands.add_parser("captions", help="Write an SRT from existing scene renders and narration timings")
    for command, extension in ((publish, "MP4"), (captions, "SRT")):
        command.add_argument("--scene", type=Path, nargs="+", action="append", required=True,
                             metavar="FILE", help="VIDEO [NARRATION.mp3]. Repeat in playback order.")
        command.add_argument("--output", type=Path, required=True, help=f"Output {extension} path")
    publish.add_argument("--thumbnail-at", type=float, help="Thumbnail time in seconds. Defaults to the middle.")
    add_audio_arguments(commands.add_parser("audio", help="Generate MP3 and beat timings"), ROOT)
    combine = commands.add_parser("mux", help="Attach narration and preserve the visual tail")
    for field in ("video", "audio", "output"):
        combine.add_argument(field, type=Path)
    args = parser.parse_args()

    if args.action == "init":
        init_project(args)
    elif args.action == "check":
        check_project(args.project.resolve())
        print(f"Valid video project: {args.project}")
    elif args.action == "audio":
        generate_audio(args)
    elif args.action == "mux":
        mux(args)
    elif args.action == "review":
        print(json.dumps(review(args.video, args.transition, args.output), ensure_ascii=False))
    elif args.action == "package":
        print(json.dumps(package(args.scene, args.output, args.thumbnail_at), ensure_ascii=False))
    elif args.action == "captions":
        print(json.dumps({"captions": str(export_captions(args.scene, args.output))}, ensure_ascii=False))
    elif args.action == "render":
        render(args, resolve_project(args.project.resolve()))
    else:
        project = resolve_project(args.project.resolve())
        with (project / "project.toml").open("rb") as manifest:
            config = tomllib.load(manifest)
        print(read_source(project / config["source"]))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, SyntaxError, subprocess.CalledProcessError) as error:
        sys.exit(f"Error: {error}")
