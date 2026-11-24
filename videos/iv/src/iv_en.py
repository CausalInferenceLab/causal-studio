"""Load scenes from ../scenes/ for existing Manim commands."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scenes"))

from videos.iv.scenes import (
    scene_01_snow_pumps_en,
    scene_02_rct_recap_break_en,
    scene_03_three_types_en,
    scene_04_iv_machinery_en,
    scene_05_three_assumptions_en,
    scene_06_draft_lottery_en,
    scene_07_outro_en,
)


class Scene01_SnowPumpsEN(scene_01_snow_pumps_en.Scene01_SnowPumpsEN):
    pass


class Scene02_RctRecapBreakEN(scene_02_rct_recap_break_en.Scene02_RctRecapBreakEN):
    pass


class Scene03_ThreeTypesEN(scene_03_three_types_en.Scene03_ThreeTypesEN):
    pass


class Scene04_IvMachineryEN(scene_04_iv_machinery_en.Scene04_IvMachineryEN):
    pass


class Scene05_ThreeAssumptionsEN(scene_05_three_assumptions_en.Scene05_ThreeAssumptionsEN):
    pass


class Scene06_DraftLotteryEN(scene_06_draft_lottery_en.Scene06_DraftLotteryEN):
    pass


class Scene07_OutroEN(scene_07_outro_en.Scene07_OutroEN):
    pass
