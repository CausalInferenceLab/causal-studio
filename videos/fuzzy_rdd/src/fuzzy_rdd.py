"""Load scenes for the ko edition for existing Manim commands."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from videos.fuzzy_rdd.ko.scenes import (
    scene_01_recap_hook,
    scene_02_variables,
    scene_03_wald,
    scene_04_complier_late,
    scene_05_assumptions,
    scene_06_twosls,
    scene_07_recap,
)


class Scene01RecapHook(scene_01_recap_hook.Scene01RecapHook):
    pass


class Scene02Variables(scene_02_variables.Scene02Variables):
    pass


class Scene03Wald(scene_03_wald.Scene03Wald):
    pass


class Scene04ComplierLate(scene_04_complier_late.Scene04ComplierLate):
    pass


class Scene05Assumptions(scene_05_assumptions.Scene05Assumptions):
    pass


class Scene06TwoSLS(scene_06_twosls.Scene06TwoSLS):
    pass


class Scene07Recap(scene_07_recap.Scene07Recap):
    pass
