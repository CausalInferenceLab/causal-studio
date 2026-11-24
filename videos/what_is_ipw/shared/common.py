"""Graphics shared by the Korean and English IPW scenes."""

from functools import cache
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

from manim import SVGMobject


ICONS = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"


@cache
def _load_icon(name):
    source = ICONS / f"{name}.svg"
    # Manim preprocesses SVGs beside the input. Keep that work local to this render.
    with TemporaryDirectory() as directory:
        private_svg = Path(directory) / source.name
        copyfile(source, private_svg)
        return SVGMobject(str(private_svg), use_svg_cache=False)


def icon(name, color, height=1.0):
    graphic = _load_icon(name).copy()
    graphic.set_stroke(color, width=3)
    graphic.set_fill(color, opacity=0)
    return graphic.scale_to_fit_height(height)
