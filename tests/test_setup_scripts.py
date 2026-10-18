"""Exercise setup orchestration with local Git remotes and a fake Python runtime."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]


class SetupScriptsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="causal-setup-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo with spaces"
        self.root.mkdir()
        shutil.copytree(SOURCE / "scripts", self.root / "scripts")
        (self.root / "Pipfile").write_text('[requires]\npython_version = "3.11"\n')
        for name in ("requirements.txt", "requirements-book.txt"):
            (self.root / name).touch()
        self.env = os.environ.copy()
        # Keep all Git configuration and network routing local to the fixture.
        self.env.update({
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_COUNT": "2",
            "SETUP_TEST_LOG": str(self.base / "python.log"),
            "GIT_AUTHOR_NAME": "Setup Test",
            "GIT_AUTHOR_EMAIL": "setup@example.invalid",
            "GIT_COMMITTER_NAME": "Setup Test",
            "GIT_COMMITTER_EMAIL": "setup@example.invalid",
        })
        for i, (upstream, marker) in enumerate((
            ("https://github.com/3b1b/videos.git", "_2020/covid.py"),
            ("https://github.com/tabler/tabler-icons.git", "icons/outline/device-tablet.svg"),
        )):
            remote = self.base / f"remote-{i}"
            subprocess.run(["git", "init", "-q", str(remote)], check=True, env=self.env_without_routes())
            required = remote / marker
            required.parent.mkdir(parents=True)
            required.touch()
            for args in (("add", "."), ("commit", "-qm", "fixture")):
                subprocess.run(["git", "-C", str(remote), *args], check=True, env=self.env_without_routes())
            self.env[f"GIT_CONFIG_KEY_{i}"] = f"url.{remote.as_uri()}.insteadOf"
            self.env[f"GIT_CONFIG_VALUE_{i}"] = upstream

        # Simulate Python installation/import results; exercise the actual Bash
        # orchestration and real Git operations without installing packages.
        self.python = self.base / "python3.11"
        self.python.write_text('''#!/usr/bin/env bash
set -eu
echo "$*" >> "$SETUP_TEST_LOG"
if [ "${1:-}" = "-m" ] && [ "${2:-}" = "venv" ]; then
  mkdir -p "$3/bin"
  cp "$0" "$3/bin/python"
elif [ "${1:-}" = "-m" ] && [ "${2:-}" = "pip" ] && [ "${3:-}" = "check" ]; then
  exit "${SETUP_TEST_PIP_FAILURE:-0}"
elif [ "${1:-}" = "-" ]; then
  cat >/dev/null
  exit "${SETUP_TEST_IMPORT_FAILURE:-0}"
fi
''')
        self.python.chmod(0o755)
        self.env["PYTHON_BIN"] = str(self.python)

    def env_without_routes(self):
        return {key: value for key, value in self.env.items() if not key.startswith("GIT_CONFIG_") or key in ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM")}

    def run_script(self, script="setup_environment.sh", *args, ok=True):
        # Run outside the repository to verify path resolution.
        result = subprocess.run(
            ["bash", str(self.root / "scripts" / script), *args],
            cwd=self.base, env=self.env, text=True, capture_output=True,
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("ready:", result.stdout)
        return result

    def test_default_setup_includes_both_assets_and_can_be_repeated(self):
        self.run_script()
        for marker in ("3b1b/_2020/covid.py", "videos/assets/tabler-icons/icons/outline/device-tablet.svg"):
            self.assertTrue((self.root / marker).is_file())
        self.assertIn("-m pip install -r requirements.txt", (self.base / "python.log").read_text())
        self.run_script()  # Exercise pull --ff-only for existing clones.
        checked = self.run_script("setup_environment.sh", "--check")
        self.assertIn("ready: full Python environment", checked.stdout)

    def test_book_only_skips_assets_and_uses_book_requirements(self):
        result = self.run_script("setup_environment.sh", "--book-only")
        self.assertFalse((self.root / "3b1b").exists())
        self.assertFalse((self.root / "videos").exists())
        self.assertIn("-m pip install -r requirements-book.txt", (self.base / "python.log").read_text())
        self.assertIn("ready: book-only", result.stdout)

    def test_check_does_not_create_a_venv(self):
        self.run_script("setup_environment.sh", "--check", ok=False)
        self.assertFalse((self.root / ".venv").exists())

    def test_full_check_rejects_python_only_setup_without_installing(self):
        self.run_script("setup_environment.sh", "--book-only")
        (self.base / "python.log").write_text("")
        self.run_script("setup_environment.sh", "--check", ok=False)
        self.assertNotIn("pip install", (self.base / "python.log").read_text())
        self.assertFalse((self.root / "3b1b").exists())

    def test_invalid_existing_asset_is_not_overwritten_or_skipped(self):
        dest = self.root / "videos/assets/tabler-icons"
        dest.mkdir(parents=True)
        (dest / "user-file").write_text("keep")
        self.run_script("setup_video_assets.sh", ok=False)
        self.assertEqual((dest / "user-file").read_text(), "keep")
        self.assertFalse((self.root / "3b1b").exists())

    def test_missing_marker_fails_validation(self):
        self.run_script("setup_video_assets.sh")
        (self.root / "3b1b/_2020/covid.py").unlink()
        self.run_script("setup_video_assets.sh", "--check", ok=False)

    def test_dependency_and_import_failures_cannot_report_ready(self):
        for variable in ("SETUP_TEST_PIP_FAILURE", "SETUP_TEST_IMPORT_FAILURE"):
            with self.subTest(variable=variable):
                self.env[variable] = "1"
                self.run_script(ok=False)
                self.assertFalse((self.root / "3b1b").exists())
                del self.env[variable]


if __name__ == "__main__":
    unittest.main()
