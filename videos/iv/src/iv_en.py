"""Load scenes for the en edition for existing Manim commands."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from videos.iv.en.scenes import (
    scene_01_snow_pumps,
    scene_02_rct_recap_break,
    scene_03_three_types,
    scene_04_iv_machinery,
    scene_05_three_assumptions,
    scene_06_draft_lottery,
    scene_07_outro,
)


class Scene01_SnowPumpsEN(scene_01_snow_pumps.Scene01_SnowPumpsEN):
    pass


class Scene02_RctRecapBreakEN(scene_02_rct_recap_break.Scene02_RctRecapBreakEN):
    pass


class Scene03_ThreeTypesEN(scene_03_three_types.Scene03_ThreeTypesEN):
    pass


class Scene04_IvMachineryEN(scene_04_iv_machinery.Scene04_IvMachineryEN):
    pass


class Scene05_ThreeAssumptionsEN(scene_05_three_assumptions.Scene05_ThreeAssumptionsEN):
    pass


class Scene06_DraftLotteryEN(scene_06_draft_lottery.Scene06_DraftLotteryEN):
    pass


class Scene07_OutroEN(scene_07_outro.Scene07_OutroEN):
    pass
