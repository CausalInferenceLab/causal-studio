"""Resolve older video project paths and validate the layout for new editions."""

import ast
from pathlib import Path
import re
import tomllib


SOURCE_TYPES = {".md", ".txt", ".ipynb"}
TOPIC_SLUG = re.compile(r"[a-z0-9]+(?:_[a-z0-9]+)*")
LANGUAGE_TAG = re.compile(r"[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*")
SCENE_STEM = re.compile(r"scene_(\d{2})_[a-z0-9]+(?:_[a-z0-9]+)*")


def resolve_project(project, language=None):
    if language is None and (project / "project.toml").is_file():
        return project
    if project.parent.name != "videos":
        return project

    normalized = project.with_name(project.name.replace("-", "_"))
    topic = normalized if normalized.is_dir() else project
    english_topic = topic.with_name(topic.name.removesuffix("_en") or topic.name)
    if english_topic != topic and (english_topic / "en/project.toml").is_file():
        topic = english_topic
        language = language or "en"
    if language:
        edition = topic / language
        return edition if (edition / "project.toml").is_file() else project
    if not topic.is_dir():
        return project
    editions = {p.parent.name: p.parent for p in sorted(topic.glob("*/project.toml"))}
    return editions.get("ko") or editions.get("en") or next(iter(editions.values()), project)


def scene_classes(path):
    body = ast.parse(path.read_text(encoding="utf-8"), filename=str(path)).body
    return {node.name for node in body if isinstance(node, ast.ClassDef)}


def check_project(project):
    if not (project.parent.parent.name == "videos" and TOPIC_SLUG.fullmatch(project.parent.name)
            and LANGUAGE_TAG.fullmatch(project.name)):
        raise ValueError(f"Use videos/<topic_slug>/<language>/ for the project: {project}")
    with (project / "project.toml").open("rb") as manifest:
        config = tomllib.load(manifest)
    source = Path(config["source"])
    if source.is_absolute() or source.suffix.lower() not in SOURCE_TYPES or not (project / source).is_file():
        raise ValueError(f"Point source to an existing relative Markdown, text, or notebook file: {source}")
    if not (project / "scene_plan.md").is_file():
        raise ValueError(f"Missing scene_plan.md in {project}")

    scenes = sorted(p for p in (project / "scenes").glob("*.py") if p.name != "__init__.py")
    numbers = set()
    stems = set()
    for scene in scenes:
        matched = SCENE_STEM.fullmatch(scene.stem)
        if matched is None:
            raise ValueError(f"Use scene_NN_name.py for scene files: {scene.name}")
        if matched[1] in numbers:
            raise ValueError(f"Duplicate scene number in {project}: {matched[1]}")
        numbers.add(matched[1])
        stems.add(scene.stem.removeprefix("scene_"))

    for narration in sorted((project / "narration").glob("*.txt")):
        if narration.stem not in stems:
            raise ValueError(f"No matching scenes/scene_{narration.stem}.py for narration/{narration.name}")

    default_scene = Path(config["scene_file"])
    if default_scene.parent != Path("scenes") or project / default_scene not in scenes:
        raise ValueError(f"Point scene_file to a numbered file under scenes/: {default_scene}")
    if config["scene_class"] not in scene_classes(project / default_scene):
        raise ValueError(f"No class {config['scene_class']} in {default_scene}")
