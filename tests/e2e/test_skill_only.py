"""Render a first scene from a clean clone of the skill-only export."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCENE = """from pathlib import Path

from manim import Circle, Create, Scene
from manim_timing import BeatClock


class Scene01(Scene):
    def construct(self):
        timing_path = Path(__file__).resolve().parents[1] / "build/audio/01_intro.timings.json"
        clock = BeatClock(self, timing_path, (0.9,))
        with clock.beat() as seconds:
            self.play(Create(Circle()), run_time=seconds / 2)
        clock.finish()
"""


class SkillOnlyE2E(unittest.TestCase):
    def test_fresh_clone_renders_a_silent_scene_from_a_brief(self):
        with tempfile.TemporaryDirectory(prefix="manim-skill-e2e-") as directory:
            scratch = Path(directory)
            snapshot = scratch / "snapshot"
            checkout = scratch / "checkout"
            subprocess.run(
                [sys.executable, str(ROOT / "scripts/export_manim_starter.py"),
                 "--skill-only", "--directory", str(snapshot)],
                check=True,
            )

            git_env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
            git_env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
            subprocess.run(["git", "init", "-q", "-b", "skill-only", str(snapshot)], check=True, env=git_env)
            subprocess.run(["git", "add", "."], cwd=snapshot, check=True, env=git_env)
            subprocess.run(
                ["git", "-c", "user.name=Manim E2E", "-c", "user.email=manim-e2e@example.invalid",
                 "commit", "-qm", "Test skill-only snapshot"],
                cwd=snapshot, check=True, env=git_env,
            )
            subprocess.run(
                ["git", "clone", "-q", "--branch", "skill-only", "--single-branch", "--depth", "1",
                 snapshot.as_uri(), str(checkout)],
                check=True, env=git_env,
            )
            for name in ("book", "binder", "videos", ".venv", ".venv-video", ".env"):
                self.assertFalse((checkout / name).exists(), name)
            self.assertEqual((checkout / ".env.example").read_bytes(), (ROOT / ".env.example").read_bytes())
            subprocess.run(["git", "check-ignore", "-q", ".env"], cwd=checkout, check=True, env=git_env)
            self.assertTrue((checkout / ".agents/skills/manim-video-pipeline/SKILL.md").is_file())
            self.assertTrue((checkout / ".claude/skills/manim-video-pipeline/SKILL.md").is_file())

            env = {key: value for key, value in os.environ.items()
                   if key not in {"OPENAI_API_KEY", "ELEVENLABS_API_KEY"}}
            env.update(PYTHON_BIN=sys.executable, PIP_DISABLE_PIP_VERSION_CHECK="1", PIP_PROGRESS_BAR="off")
            subprocess.run(["bash", "scripts/setup_environment.sh", "--video-only"], cwd=checkout, env=env, check=True)
            python = checkout / ".venv-video/bin/python"
            launcher = [str(python), "video.py"]
            topic = "videos/circle-test"
            brief = "Explain how to draw a circle."
            subprocess.run([*launcher, "init", topic, "--brief", brief], cwd=checkout, env=env, check=True)
            lesson = subprocess.check_output([*launcher, "source", topic], cwd=checkout, env=env, text=True)
            self.assertIn(brief, lesson)
            self.assertFalse(list((checkout / topic).glob("*.ipynb")))
            (checkout / topic / "scenes/scene_01.py").write_text(SCENE, encoding="utf-8")
            subprocess.run([*launcher, "render", topic], cwd=checkout, env=env, check=True)

            previews = list((checkout / topic / "build/manim/videos").glob("**/Scene01.mp4"))
            self.assertEqual(len(previews), 1)
            probe = subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,height:format=duration",
                 "-of", "json", str(previews[0])],
                text=True,
            )
            media = json.loads(probe)
            self.assertEqual(media["streams"], [{"codec_type": "video", "height": 480}])
            self.assertGreater(float(media["format"]["duration"]), 0)


if __name__ == "__main__":
    unittest.main()
