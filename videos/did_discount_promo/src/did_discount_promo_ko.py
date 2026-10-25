"""할인 기획전 DID 5컷 영상 초안. 각 컷의 음성 길이는 build/durations.json에서 읽는다."""

import json
from pathlib import Path

from manim import ImageMobject, Scene, config


config.frame_width = 16
config.frame_height = 9
ROOT = Path(__file__).resolve().parents[1]


class DIDDiscountPromoDraft(Scene):
    def construct(self):
        durations = json.loads((ROOT / "build" / "durations.json").read_text())
        for number, duration in enumerate(durations, 1):
            self.clear()
            slide = ImageMobject(str(ROOT / "build" / "slides" / f"{number:02d}.png"))
            slide.set(width=config.frame_width)
            self.add(slide)
            self.wait(duration)
