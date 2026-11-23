"""Run the shared Manim video workflow from a Causal Studio checkout or starter."""

from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    scripts = Path(__file__).resolve().parent / ".claude/skills/manim-video-pipeline/scripts"
    sys.path.insert(0, str(scripts))
    runpy.run_path(str(scripts / "pipeline.py"), run_name="__main__")
