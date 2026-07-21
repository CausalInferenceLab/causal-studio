from manim import *
import numpy as np

BG     = "#080E18"
C_RED  = "#FF5C5C"
C_BLUE = "#00BFFF"
C_GOLD = "#FFD700"
WHITE  = "#FFFFFF"
FONT   = "Apple SD Gothic Neo"


class ThumbnailRDDKorean(Scene):
    """
    3B1B 스타일 RDD 썸네일 v4
    — 그래프 없음: 불연속(step) 자체를 추상 시각화
    — 두 개의 수평 글로우 선 + 점프 화살표
    — 축, 산점도, 격자 일절 없음
    manim -s -qh --media_dir build/manim src/thumbnail.py ThumbnailRDDKorean
    """

    def construct(self):
        self.camera.background_color = BG

        cx   = 2.8   # 컷오프 x — 텍스트(좌)와 그래프(우) 분리
        y_lo = -2.0  # 아래 선 y
        y_hi = +1.5  # 위 선 y

        # ── 컷오프 glow band ─────────────────────────────────────
        band = Rectangle(
            width=1.0, height=9.2,
            fill_color=C_GOLD, fill_opacity=0.07, stroke_width=0,
        ).move_to([cx, 0, 0])

        # ── 수평 불연속 선 (3겹 glow) ────────────────────────────
        def h_glow_line(x0, x1, y, color):
            return VGroup(
                Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=55, stroke_opacity=0.05),
                Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=22, stroke_opacity=0.14),
                Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=8,  stroke_opacity=0.50),
                Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3.5, stroke_opacity=1.0),
            )

        left_line  = h_glow_line(-8.5, cx, y_lo, C_RED)
        right_line = h_glow_line(cx, 8.5, y_hi, C_BLUE)

        # ── 절편 강조 점 ─────────────────────────────────────────
        dot_lo = VGroup(
            Dot([cx, y_lo, 0], color=C_RED,  radius=0.36, fill_opacity=0.15),
            Dot([cx, y_lo, 0], color=C_RED,  radius=0.20, fill_opacity=1.0),
        )
        dot_hi = VGroup(
            Dot([cx, y_hi, 0], color=C_BLUE, radius=0.36, fill_opacity=0.15),
            Dot([cx, y_hi, 0], color=C_BLUE, radius=0.20, fill_opacity=1.0),
        )

        # ── 컷오프 수직 점선 ─────────────────────────────────────
        cutoff_glow = Line(
            [cx, -4.8, 0], [cx, 4.8, 0],
            color=C_GOLD, stroke_width=18, stroke_opacity=0.10,
        )
        cutoff_line = DashedLine(
            [cx, -4.8, 0], [cx, 4.8, 0],
            color=C_GOLD, stroke_width=2.5, stroke_opacity=0.85,
            dash_length=0.22,
        )

        # ── 점프 화살표 (영웅 요소, 3겹 glow) ───────────────────
        p_lo = [cx, y_lo + 0.22, 0]
        p_hi = [cx, y_hi - 0.22, 0]
        jump = VGroup(
            DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                        stroke_width=60, stroke_opacity=0.06, tip_length=0.58),
            DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                        stroke_width=24, stroke_opacity=0.18, tip_length=0.58),
            DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                        stroke_width=8,  stroke_opacity=1.0,  tip_length=0.58),
        )

        # ── τ̂ 레이블 ─────────────────────────────────────────────
        tau = MathTex(r"\hat{\tau}", font_size=96, color=C_GOLD)
        tau.move_to([cx + 1.4, (y_lo + y_hi) / 2, 0])

        # ── 텍스트 ───────────────────────────────────────────────
        title    = Text("RDD", font=FONT, font_size=168, color=WHITE, weight=BOLD)
        fullname = Text("Regression Discontinuity Design",
                        font=FONT, font_size=32, color=WHITE, weight=BOLD)
        subtitle = Text("회귀 불연속 설계", font=FONT, font_size=32, color=C_BLUE, weight=BOLD)
        text_grp = VGroup(title, fullname, subtitle).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        text_grp.to_corner(UL, buff=0.44).shift(RIGHT * 1.0 + DOWN * 0.6)

        # ── 조립 ─────────────────────────────────────────────────
        self.add(
            band,
            left_line, right_line,
            cutoff_glow, cutoff_line,
            dot_lo, dot_hi,
            jump, tau,
            text_grp,
        )
        self.wait(0.1)


def _build_scene(scene, cx, y_lo, y_hi, title_lines):
    """한국어/영어 공용 씬 빌더"""
    scene.camera.background_color = BG

    band = Rectangle(
        width=1.0, height=9.2,
        fill_color=C_GOLD, fill_opacity=0.07, stroke_width=0,
    ).move_to([cx, 0, 0])

    def h_glow_line(x0, x1, y, color):
        return VGroup(
            Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=55, stroke_opacity=0.05),
            Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=22, stroke_opacity=0.14),
            Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=8,  stroke_opacity=0.50),
            Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=3.5, stroke_opacity=1.0),
        )

    left_line  = h_glow_line(-8.5, cx, y_lo, C_RED)
    right_line = h_glow_line(cx, 8.5, y_hi, C_BLUE)

    dot_lo = VGroup(
        Dot([cx, y_lo, 0], color=C_RED,  radius=0.36, fill_opacity=0.15),
        Dot([cx, y_lo, 0], color=C_RED,  radius=0.20, fill_opacity=1.0),
    )
    dot_hi = VGroup(
        Dot([cx, y_hi, 0], color=C_BLUE, radius=0.36, fill_opacity=0.15),
        Dot([cx, y_hi, 0], color=C_BLUE, radius=0.20, fill_opacity=1.0),
    )

    cutoff_glow = Line([cx, -4.8, 0], [cx, 4.8, 0],
                       color=C_GOLD, stroke_width=18, stroke_opacity=0.10)
    cutoff_line = DashedLine([cx, -4.8, 0], [cx, 4.8, 0],
                             color=C_GOLD, stroke_width=2.5, stroke_opacity=0.85,
                             dash_length=0.22)

    p_lo = [cx, y_lo + 0.22, 0]
    p_hi = [cx, y_hi - 0.22, 0]
    jump = VGroup(
        DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                    stroke_width=60, stroke_opacity=0.06, tip_length=0.58),
        DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                    stroke_width=24, stroke_opacity=0.18, tip_length=0.58),
        DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                    stroke_width=8,  stroke_opacity=1.0,  tip_length=0.58),
    )

    tau = MathTex(r"\hat{\tau}", font_size=96, color=C_GOLD)
    tau.move_to([cx + 1.4, (y_lo + y_hi) / 2, 0])

    text_grp = VGroup(*title_lines).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    text_grp.to_corner(UL, buff=0.44).shift(RIGHT * 1.0 + DOWN * 0.6)

    scene.add(band, left_line, right_line,
              cutoff_glow, cutoff_line,
              dot_lo, dot_hi, jump, tau,
              text_grp)
    scene.wait(0.1)


class ThumbnailRDDEnglish(Scene):
    """
    RDD 영어 썸네일
    manim -s -qh --media_dir build/manim src/thumbnail.py ThumbnailRDDEnglish
    """

    def construct(self):
        _build_scene(
            self, cx=2.8, y_lo=-2.0, y_hi=1.5,
            title_lines=[
                Text("RDD", font=FONT, font_size=168, color=WHITE, weight=BOLD),
                Text("Regression Discontinuity Design",
                     font=FONT, font_size=32, color=C_BLUE, weight=BOLD),
            ],
        )
