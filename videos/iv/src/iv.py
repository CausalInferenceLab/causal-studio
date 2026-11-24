"""Load scenes from ../scenes/ for existing Manim commands."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scenes"))

from videos.iv.scenes import (
    scene_01_snow_pumps,
    scene_02_rct_recap_break,
    scene_03_three_types,
    scene_04_iv_machinery,
    scene_05_three_assumptions,
    scene_06_draft_lottery,
    scene_07_outro,
)


class Scene01_SnowPumps(scene_01_snow_pumps.Scene01_SnowPumps):
    pass


class Scene02_RctRecapBreak(scene_02_rct_recap_break.Scene02_RctRecapBreak):
    pass


class Scene03_ThreeTypes(scene_03_three_types.Scene03_ThreeTypes):
    pass


class Scene04_IvMachinery(scene_04_iv_machinery.Scene04_IvMachinery):
    pass


class Scene05_ThreeAssumptions(scene_05_three_assumptions.Scene05_ThreeAssumptions):
    pass


class Scene06_DraftLottery(scene_06_draft_lottery.Scene06_DraftLottery):
    pass


class Scene07_Outro(scene_07_outro.Scene07_Outro):
    pass
