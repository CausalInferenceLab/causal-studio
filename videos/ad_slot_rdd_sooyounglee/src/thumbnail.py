import sys
from pathlib import Path

from manim import *

# 본편 Scene 파일의 색·폰트·거북이 그리기 함수를 그대로 가져와 영상과 톤을 맞춘다.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ad_slot_rdd_sooyounglee import (  # noqa: E402
    AD_B_COLOR,
    ASSET_DIR,
    HIGHLIGHT_COLOR,
    INK,
    make_turtle,
)


class Thumbnail(Scene):
    """
    썸네일: "따봉거북아 고마워"

    '따봉도치야 고마워' 밈을 영상의 금색 거북이 B로 바꿨다.
    스킬 기본값(검정 배경 + CM 세리프) 대신 본편과 같은 회백색 배경 + Pretendard + 주황 강조를 쓴다.

    레이아웃: 왼쪽 거북이 B + 들어 올린 따봉 / 오른쪽 두 줄 문구 (따봉거북아 주황, 고마워 진회색)
    """

    def construct(self):
        turtle = make_turtle(AD_B_COLOR, height=2.6)
        turtle.move_to(LEFT * 4.2 + DOWN * 0.5)
        head = turtle[5]

        thumb = SVGMobject(str(ASSET_DIR.parent / "filled" / "thumb-up.svg"))
        thumb.set_fill(HIGHLIGHT_COLOR, opacity=1).set_stroke(width=0)
        thumb.height = 1.35
        # 머리 바로 오른쪽 아래에서 앞으로 내민 따봉 (머리·글자와 겹치지 않게)
        thumb.rotate(-8 * DEGREES).next_to(head, RIGHT, buff=0.12).shift(DOWN * 0.15)

        sparkles = VGroup(*[
            SVGMobject(str(ASSET_DIR.parent / "filled" / "sparkles.svg")).set_fill(color, opacity=1).set_stroke(width=0)
            .scale_to_fit_height(size).move_to(pos)
            for color, size, pos in (
                ("#F2B33D", 0.65, LEFT * 2.3 + UP * 1.9),
                ("#F2B33D", 0.45, LEFT * 0.9 + UP * 1.25),
                ("#F2B33D", 0.4, LEFT * 5.9 + UP * 1.0),
            )
        ])

        line_1 = Text("따봉거북아", font_size=104, weight=BOLD, color=HIGHLIGHT_COLOR)
        line_2 = Text("고마워", font_size=104, weight=BOLD, color=INK)
        title = VGroup(line_1, line_2).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        title.move_to(RIGHT * 3.7)

        self.add(sparkles, turtle, thumb, title)
