"""Load scenes for the ko edition for existing Manim commands."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from videos.rdd.ko.scenes import (
    scene_01_rdd_intro,
    scene_02_sharp_vs_fuzzy,
    scene_03_key_assumptions,
    scene_04_components,
    scene_05_formula,
    scene_06_visualization,
    scene_07_simulation,
    scene_08_outro,
)


class Scene01RddIntro(scene_01_rdd_intro.Scene01RddIntro):
    pass


class Scene02SharpVsFuzzy(scene_02_sharp_vs_fuzzy.Scene02SharpVsFuzzy):
    pass


class Scene03KeyAssumptions(scene_03_key_assumptions.Scene03KeyAssumptions):
    pass


class Scene04Components(scene_04_components.Scene04Components):
    pass


class Scene05Formula(scene_05_formula.Scene05Formula):
    pass


class Scene06Visualization(scene_06_visualization.Scene06Visualization):
    pass


class Scene07Simulation(scene_07_simulation.Scene07Simulation):
    pass


class Scene08Outro(scene_08_outro.Scene08Outro):
    pass
