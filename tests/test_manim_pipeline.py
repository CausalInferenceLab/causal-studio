"""Regression checks for provider routing, timing output, and starter parity."""

import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude/skills/manim-video-pipeline"
CLI = SKILL / "scripts/pipeline.py"
sys.path.insert(0, str(CLI.parent))
import pipeline


class ManimPipelineTests(unittest.TestCase):
    def test_brief_and_notebook_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            notebook = root / "lesson file.ipynb"
            notebook.write_text(json.dumps({
                "cells": [{"cell_type": "markdown", "source": ["# A notebook"]},
                          {"cell_type": "code", "source": ["raise RuntimeError()"]}],
            }))
            for name, args, expected in (
                ("brief", ["--brief", "Explain the midpoint."], "Explain the midpoint."),
                ("notebook", ["--source", str(notebook)], "# A notebook"),
            ):
                project = root / name
                subprocess.run([sys.executable, str(CLI), "init", str(project), *args], check=True, capture_output=True)
                result = subprocess.check_output([sys.executable, str(CLI), "source", str(project)], text=True)
                self.assertIn(expected, result)
                self.assertEqual((project / "lesson.md").exists(), name == "brief")
                self.assertFalse(list(project.glob("*.ipynb")))
                self.assertEqual((project / "scene_plan.md").read_bytes(),
                                 (SKILL / "templates/scene_plan.md").read_bytes())

    def test_init_preserves_a_written_scene_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            plan = project / "scene_plan.md"
            plan.write_text("# Existing storyboard\n", encoding="utf-8")
            subprocess.run([sys.executable, str(CLI), "init", str(project), "--brief", "Explain the midpoint."],
                           check=True, capture_output=True)
            self.assertEqual(plan.read_text(encoding="utf-8"), "# Existing storyboard\n")

    def test_legacy_audio_flags_resolve_to_language_editions(self):
        command = [sys.executable, str(CLI), "audio", "--dry-run"]
        for flags, language, stem in (
            (["--topic", "fuzzy_rdd_en", "--scene", "01", "--name", "recap_hook_en"], "en", "01_recap_hook"),
            (["--topic", "fuzzy_rdd", "--scene", "01", "--name", "recap_hook"], "ko", "01_recap_hook"),
        ):
            with self.subTest(language=language):
                data = json.loads(subprocess.check_output([*command, *flags]))
                base = ROOT / "videos" / "fuzzy_rdd" / language
                self.assertEqual(Path(data["outputPath"]), base / "build" / "audio" / f"{stem}.mp3")
                self.assertGreater(data["chunkCount"], 0)

    def test_old_topic_paths_find_the_moved_projects(self):
        for old, edition in (("binary-search", "binary_search/en"), ("did", "did/ko"),
                             ("rdd_en", "rdd/en"), ("fuzzy_rdd", "fuzzy_rdd/ko")):
            with self.subTest(topic=old):
                self.assertEqual(pipeline.resolve_project(ROOT / "videos" / old), ROOT / "videos" / edition)

    def test_layout_check_reports_mismatched_narration(self):
        with tempfile.TemporaryDirectory() as directory:
            topic = Path(directory) / "videos" / "test_topic"
            subprocess.run([sys.executable, str(CLI), "init", str(topic), "--lang", "en"],
                           check=True, capture_output=True)
            edition = topic / "en"
            (edition / "scenes/scene_01_intro.py").write_text("class Scene01:\n    pass\n")
            (edition / "narration/01_other.txt").write_text("Narration.\n")
            result = subprocess.run([sys.executable, str(CLI), "check", str(edition)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("No matching scenes/scene_01_other.py", result.stderr)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg is required")
    def test_each_provider_writes_the_same_timing_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "fixture.mp3"
            subprocess.run(
                ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "sine=duration=1.25",
                 "-c:a", "libmp3lame", str(fixture)],
                check=True,
            )
            for provider in ("openai", "elevenlabs"):
                with self.subTest(provider=provider):
                    output = root / f"{provider}.mp3"
                    args = [
                        str(CLI), "audio", "--provider", provider, "--voice", "test-voice",
                        "--text", "First beat.\n\nSecond beat.", "--output", str(output),
                        "--gap", "0.2", "--env-file", str(root / "no-env"),
                    ]
                    with (patch.object(sys, "argv", args),
                          patch.dict(os.environ, {"OPENAI_API_KEY": "openai-test", "ELEVENLABS_API_KEY": "elevenlabs-test"}),
                          patch("speech.urlopen", side_effect=lambda *a, **k: io.BytesIO(fixture.read_bytes())) as request,
                          contextlib.redirect_stdout(io.StringIO())):
                        pipeline.main()
                    self.assertEqual(request.call_count, 2)
                    first_request = request.call_args_list[0].args[0]
                    headers = {key.lower(): value for key, value in first_request.headers.items()}
                    body = json.loads(first_request.data)
                    if provider == "openai":
                        self.assertEqual(first_request.host, "api.openai.com")
                        self.assertEqual(headers["authorization"], "Bearer openai-test")
                        self.assertEqual(body["input"], "First beat.")
                    else:
                        self.assertEqual(first_request.host, "api.elevenlabs.io")
                        self.assertEqual(headers["xi-api-key"], "elevenlabs-test")
                        self.assertEqual(body["text"], "First beat.")
                    self.assertTrue(output.is_file())
                    timings = json.loads(output.with_suffix(".timings.json").read_text())
                    first, second = timings["chunks"]
                    self.assertEqual(timings["provider"], provider)
                    self.assertAlmostEqual(first["duration"], 1.25, places=2)
                    self.assertAlmostEqual(second["start"] - first["end"], 0.2)
                    self.assertLess(abs(timings["totalDuration"] - second["end"]), 0.06)

    def test_export_keeps_the_shared_pipeline_and_omits_course_materials(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "starter.zip"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts/export_manim_starter.py"), "--zip", str(target)],
                check=True, capture_output=True,
            )
            with ZipFile(target) as archive:
                entries = [Path(name).relative_to("causal-studio-starter") for name in archive.namelist()]
                self.assertFalse(any(entry.parts[0] in {"book", "binder"} or "build" in entry.parts for entry in entries))
                self.assertEqual({entry.parts[1] for entry in entries if entry.parts[0] == "videos"}, {"binary_search"})
                self.assertIn(Path("videos/binary_search/en/project.toml"), entries)
                self.assertEqual(archive.read("causal-studio-starter/video.py"), (ROOT / "video.py").read_bytes())
                self.assertEqual(archive.read("causal-studio-starter/assets/manim-workflow.png"),
                                 (ROOT / "docs/assets/manim-workflow.png").read_bytes())
                self.assertEqual(archive.read("causal-studio-starter/scripts/setup_environment.sh"),
                                 (ROOT / "scripts/setup_environment.sh").read_bytes())
                shared = [entry for entry in entries if entry.is_relative_to(SKILL.relative_to(ROOT))]
                self.assertIn(CLI.relative_to(ROOT), shared)
                for entry in shared:
                    self.assertEqual(archive.read(f"causal-studio-starter/{entry}"), (ROOT / entry).read_bytes())

    def test_skill_only_export_keeps_tools_without_project_files(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "skill.zip"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts/export_manim_starter.py"),
                 "--skill-only", "--zip", str(target)],
                check=True, capture_output=True,
            )
            prefix = "causal-studio-skill/"
            with ZipFile(target) as archive:
                entries = {Path(name.removeprefix(prefix)) for name in archive.namelist()}
                self.assertTrue(all(name.startswith(prefix) for name in archive.namelist()))
                self.assertEqual(archive.read(prefix + "assets/manim-workflow.png"),
                                 (ROOT / "docs/assets/manim-workflow.png").read_bytes())
                self.assertFalse(any(entry.parts[0] in {"book", "videos", "binder"} for entry in entries))
                self.assertFalse(any(entry.name in {"gen_en_slow.mjs", "causal-studio.md"} for entry in entries))
                for entry in entries:
                    if entry.is_relative_to(SKILL.relative_to(ROOT)):
                        self.assertEqual(archive.read(prefix + str(entry)), (ROOT / entry).read_bytes())
                self.assertIn(CLI.relative_to(ROOT), entries)
                self.assertIn(Path("scripts/setup_environment.sh"), entries)
                self.assertEqual(archive.read(prefix + "scripts/setup_video_assets.sh"),
                                 (ROOT / "scripts/setup_video_assets.sh").read_bytes())


if __name__ == "__main__":
    unittest.main()
