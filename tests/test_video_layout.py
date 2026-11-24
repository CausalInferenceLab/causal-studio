"""Keep the published video catalog on the same layout as newly created projects."""

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".claude/skills/manim-video-pipeline/scripts"))
from project_layout import TOPIC_SLUG, check_project


class VideoLayoutTest(unittest.TestCase):
    def test_every_topic_has_numbered_language_editions(self):
        names = subprocess.check_output(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "videos"], cwd=ROOT,
        ).decode().split("\0")
        files = {Path(name) for name in names if name and (ROOT / name).is_file()}
        editions = {path.parent for path in files if path.name == "project.toml"}
        self.assertTrue(editions)
        for edition in sorted(editions):
            with self.subTest(edition=edition):
                check_project(ROOT / edition)

        topics = {path.parent for path in editions}
        for path in sorted(files):
            with self.subTest(file=path):
                if path.parts[1] == "assets":
                    continue
                topic = Path(*path.parts[:2])
                self.assertIn(topic, topics)
                self.assertTrue(TOPIC_SLUG.fullmatch(topic.name))
                if path.parent == topic:
                    self.assertEqual(path.name, "README.md")
                elif path.parts[2] not in {"assets", "shared", "tools"}:
                    edition = Path(*path.parts[:3])
                    self.assertIn(edition, editions)
                    if path.parent == edition:
                        self.assertIn(path.name, {"project.toml", "scene_plan.md", "lesson.md", "README.md"})
                    else:
                        self.assertIn(path.parts[3], {"assets", "scenes", "narration", "tools"})


if __name__ == "__main__":
    unittest.main()
