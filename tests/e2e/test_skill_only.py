"""Render and narrate a first scene from a clean clone of the skill-only export."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCENE = """from pathlib import Path

from manim import BLUE, GOLD, RIGHT, FadeIn, Indicate, Rectangle, Scene, VGroup
from manim_timing import BeatClock


class Scene01(Scene):
    def construct(self):
        timing_path = Path(__file__).resolve().parents[1] / "build/audio/01_intro.timings.json"
        clock = BeatClock(self, timing_path, (0.9, 0.9))
        bars = VGroup(Rectangle(width=0.6, height=1, color=BLUE),
                      Rectangle(width=0.6, height=1.4, color=GOLD)).arrange(RIGHT)
        with clock.beat() as seconds:
            self.play(FadeIn(bars), run_time=seconds / 2)
        with clock.beat() as seconds:
            self.play(Indicate(bars[1]), run_time=seconds / 2)
        clock.finish()
"""

MOCK_TTS = """import io
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path('.claude/skills/manim-video-pipeline/scripts').resolve()))
import speech

fixture = subprocess.check_output([
    'ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'sine=duration=1.25',
    '-c:a', 'libmp3lame', '-f', 'mp3', '-',
])
with patch.object(speech, 'urlopen', side_effect=lambda *_args, **_kwargs: io.BytesIO(fixture)):
    runpy.run_path('video.py', run_name='__main__')
"""


def probe_video(path):
    output = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,height:format=duration",
         "-of", "json", str(path)],
        text=True,
    )
    return json.loads(output)


class SkillOnlyE2E(unittest.TestCase):
    def test_fresh_clone_renders_preview_and_narrated_scene(self):
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
            self.assertEqual((checkout / "assets/manim-workflow.png").read_bytes(),
                             (ROOT / "docs/assets/manim-workflow.png").read_bytes())
            self.assertTrue((checkout / "scripts/setup_video_assets.sh").is_file())
            subprocess.run(["git", "check-ignore", "-q", ".env"], cwd=checkout, check=True, env=git_env)
            self.assertTrue((checkout / ".agents/skills/manim-video-pipeline/SKILL.md").is_file())
            self.assertTrue((checkout / ".claude/skills/manim-video-pipeline/SKILL.md").is_file())

            env = {key: value for key, value in os.environ.items()
                   if key not in {"OPENAI_API_KEY", "ELEVENLABS_API_KEY"}}
            env.update(PYTHON_BIN=sys.executable, PIP_DISABLE_PIP_VERSION_CHECK="1", PIP_PROGRESS_BAR="off")
            subprocess.run(["bash", "scripts/setup_environment.sh", "--video-only"], cwd=checkout, env=env, check=True)
            python = checkout / ".venv-video/bin/python"
            launcher = [str(python), "video.py"]
            topic = "videos/ab-test"
            brief = "Explain how a button color A/B test compares click rates."
            subprocess.run([*launcher, "init", topic, "--brief", brief], cwd=checkout, env=env, check=True)
            lesson = subprocess.check_output([*launcher, "source", topic], cwd=checkout, env=env, text=True)
            self.assertIn(brief, lesson)
            project = checkout / topic
            self.assertFalse(list(project.glob("*.ipynb")))
            self.assertEqual(
                (project / "scene_plan.md").read_bytes(),
                (ROOT / ".claude/skills/manim-video-pipeline/templates/scene_plan.md").read_bytes(),
            )
            (project / "scenes/scene_01.py").write_text(SCENE, encoding="utf-8")
            subprocess.run([*launcher, "render", topic], cwd=checkout, env=env, check=True)

            previews = list((project / "build/manim/videos").glob("**/Scene01.mp4"))
            self.assertEqual(len(previews), 1)
            preview = previews[0]
            media = probe_video(preview)
            self.assertEqual(media["streams"], [{"codec_type": "video", "height": 480}])
            preview_duration = float(media["format"]["duration"])
            self.assertGreater(preview_duration, 0)

            script = project / "narration/01_intro.txt"
            paragraphs = ["Assign visitors to two groups at random.", "Compare the click rates."]
            script.write_text("\n\n".join(paragraphs) + "\n", encoding="utf-8")
            audio = project / "build/audio/01_intro.mp3"
            subprocess.run(
                [str(python), "-c", MOCK_TTS, "audio", "--provider", "elevenlabs", "--voice", "test-voice",
                 "--gap", "0.2", "--script", str(script), "--output", str(audio)],
                cwd=checkout, env={**env, "ELEVENLABS_API_KEY": "test-fixture"}, check=True,
            )
            timing_path = project / "build/audio/01_intro.timings.json"
            timing = json.loads(timing_path.read_text(encoding="utf-8"))
            self.assertEqual([chunk["text"] for chunk in timing["chunks"]], paragraphs)
            first, second = timing["chunks"]
            self.assertAlmostEqual(second["start"] - first["end"], 0.2, places=2)
            subprocess.run([*launcher, "render", topic], cwd=checkout, env=env, check=True)
            final = project / "build/final/01_intro.mp4"
            subprocess.run([*launcher, "mux", str(preview), str(audio), str(final)],
                           cwd=checkout, env=env, check=True)

            for name in ("project.toml", "lesson.md", "scene_plan.md", "narration/01_intro.txt",
                         "scenes/scene_01.py", "build/audio/01_intro.mp3",
                         "build/audio/01_intro.timings.json", "build/final/01_intro.mp4"):
                self.assertTrue((project / name).is_file(), name)
            media = probe_video(final)
            self.assertEqual(media["streams"], [{"codec_type": "video", "height": 480}, {"codec_type": "audio"}])
            duration = float(media["format"]["duration"])
            self.assertGreater(duration, preview_duration)
            self.assertAlmostEqual(duration - timing["totalDuration"], 0.5, delta=0.08)


if __name__ == "__main__":
    unittest.main()
