from manim import *

from rdd_common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene02SharpVsFuzzy(Scene):
    """
    Scene 02: sharp_vs_fuzzy
    build/audio/02_sharp_vs_fuzzy.timings.json 기준 타이밍 (총 50.71s)

    Beat1 chunk1  ( 0.00~ 5.34s)  소개 타이틀 (5.34s)
    Beat2 chunk2  ( 5.34~20.39s)  Sharp RDD 그래프 — 0→1 완전 점프 (15.05s)
    Beat3 chunk3  (20.39~43.19s)  Fuzzy RDD 그래프 — 꺾임형 부분 점프 (22.80s)
    Beat4 chunk4  (43.19~50.71s)  요약: Sharp RDD 중심 + 별도 영상 예고 (7.52s)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~5.34s) ────────────────────────
        # 새로 등장: 소개 타이틀
        # 핵심 시선: "Sharp vs Fuzzy"
        # 지워질 요소: FadeOut → Beat2
        intro = VGroup(
            Text("RDD의 두 가지 형태", font=FONT, font_size=38, color=WHITE),
            VGroup(
                Text("Sharp", font=FONT, font_size=34, color=BLUE_MAIN),
                Text(" vs ", font=FONT, font_size=34, color=WHITE),
                Text("Fuzzy", font=FONT, font_size=34, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(intro[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(intro[1], shift=UP * 0.2), run_time=0.8)
        self.wait(3.24)
        self.play(FadeOut(intro), run_time=0.5)  # chunk1 end ~5.34s

        # ── Beat 2 (chunk2: 5.34~20.39s, 15.05s) ────────────
        # 새로 등장: Sharp RDD 제목 + 처치확률 그래프 (완전 0→1 점프)
        # 핵심 시선: 기준점에서 처치 확률이 0→1로 완전 결정
        # 지워질 요소: FadeOut → Beat3
        sharp_title = Text("Sharp Design", font=FONT, font_size=36, color=BLUE_MAIN)
        sharp_desc  = Text(
            "기준점을 넘으면 처치 확률이 0 → 1로 완전히 결정",
            font=FONT, font_size=22, color=WHITE,
        )
        sharp_header = VGroup(sharp_title, sharp_desc).arrange(DOWN, buff=0.3).move_to(UP * 2.8)

        axes_s, step_s, cutoff_s = self._make_sharp_graph()
        graph_s = VGroup(axes_s, step_s, cutoff_s).scale(0.9).move_to(DOWN * 0.3)

        self.play(FadeIn(sharp_header, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(axes_s), run_time=0.8)
        self.play(Create(cutoff_s), run_time=0.5)
        self.play(Create(step_s), run_time=1.0)
        self.wait(11.95)  # chunk2 end ~20.39s

        # ── Beat 3 (chunk3: 20.39~43.19s, 22.80s) ───────────
        # 제거: Sharp 내용
        # 새로 등장: Fuzzy RDD 제목 + 꺾임형 처치확률 그래프 (부분 점프)
        # 핵심 시선: 기준점에서 뛰어오르지만 0→1이 아님, 좌우 기울기가 꺾임
        self.play(FadeOut(VGroup(sharp_header, graph_s)), run_time=0.6)

        fuzzy_title = Text("Fuzzy Design", font=FONT, font_size=36, color=RED_MAIN)
        fuzzy_desc  = Text(
            "기준점에서 처치 확률이 뛰어오르지만, 0 → 1이 아님",
            font=FONT, font_size=22, color=WHITE,
        )
        fuzzy_header = VGroup(fuzzy_title, fuzzy_desc).arrange(DOWN, buff=0.3).move_to(UP * 2.8)

        axes_f, step_f, cutoff_f = self._make_fuzzy_graph()
        graph_f = VGroup(axes_f, step_f, cutoff_f).scale(0.9).move_to(DOWN * 0.3)

        self.play(FadeIn(fuzzy_header, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(axes_f), run_time=0.8)
        self.play(Create(cutoff_f), run_time=0.5)
        self.play(Create(step_f), run_time=1.2)
        self.wait(18.90)  # chunk3 end ~43.19s

        # ── Beat 4 (chunk4: 43.19~50.71s, 7.52s) ───────────
        # 제거: Fuzzy 내용
        # 새로 등장: 요약 (Sharp RDD 중심)
        # 핵심 시선: "이 영상은 Sharp RDD 중심, Fuzzy는 별도 영상"
        self.play(FadeOut(VGroup(fuzzy_header, graph_f)), run_time=0.6)

        summary = VGroup(
            Text("이 영상의 초점", font=FONT, font_size=26, color=WHITE),
            Text("Sharp RDD", font=FONT, font_size=52, color=BLUE_MAIN),
            Text("Fuzzy RDD → 별도 영상에서", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)

        self.play(FadeIn(summary, shift=UP * 0.3), run_time=0.8)
        self.wait(6.12)  # chunk4 + tail

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _make_axes(self):
        """Sharp/Fuzzy 공통 축 (x: 340~400, 기준점 370점)"""
        axes = Axes(
            x_range=[340, 401, 10],
            y_range=[-0.15, 1.35, 0.5],
            x_length=7.5,
            y_length=4.0,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_tip": False},
            x_axis_config={"numbers_to_include": [350, 360, 370, 380, 390]},
            y_axis_config={"numbers_to_include": [0, 0.5, 1]},
        )
        x_title = Text("수능 점수 (점)", font=FONT, font_size=18, color=WHITE).next_to(
            axes.x_axis.get_right(), RIGHT, buff=0.12
        )
        y_title = (
            Text("처치 확률", font=FONT, font_size=16, color=WHITE)
            .rotate(PI / 2)
            .next_to(axes.y_axis.get_top(), UP, buff=0.1)
        )
        cutoff_line = DashedLine(
            axes.c2p(370, -0.05), axes.c2p(370, 1.2),
            color=YELLOW_MAIN, dash_length=0.12, stroke_width=2.5,
        )
        cutoff_label = Text("Cutoff (370점)", font=FONT, font_size=16, color=YELLOW_MAIN).next_to(
            axes.c2p(370, 1.2), UP, buff=0.05
        )
        return VGroup(axes, x_title, y_title), VGroup(cutoff_line, cutoff_label), axes

    def _make_sharp_graph(self):
        """Sharp RDD: 처치 확률이 370점에서 0→1로 완전 점프 (수평선 + 수직 점프)"""
        axes_vg, cutoff_vg, axes = self._make_axes()
        left_line  = Line(axes.c2p(340, 0.0), axes.c2p(370, 0.0), color=RED_MAIN,  stroke_width=5)
        right_line = Line(axes.c2p(370, 1.0), axes.c2p(400, 1.0), color=BLUE_MAIN, stroke_width=5)
        jump_line  = Line(axes.c2p(370, 0.0), axes.c2p(370, 1.0), color=GRAY_MID,  stroke_width=2, stroke_opacity=0.7)
        dot_open   = Circle(radius=0.10, color=RED_MAIN,  fill_opacity=0, stroke_width=3).move_to(axes.c2p(370, 0.0))
        dot_closed = Dot(axes.c2p(370, 1.0), radius=0.10, color=BLUE_MAIN, fill_opacity=1)
        step_vg = VGroup(left_line, right_line, jump_line, dot_open, dot_closed)
        return axes_vg, step_vg, cutoff_vg

    def _make_fuzzy_graph(self):
        """Fuzzy RDD: 기준점에서 꺾이듯 부분 점프 (0.2→0.7), 좌우 기울기 다름"""
        axes_vg, cutoff_vg, axes = self._make_axes()
        # 왼쪽: 완만한 상승 추세 (340에서 0.1, 370에서 0.2)
        left_line  = axes.plot(
            lambda x: 0.1 + (0.2 - 0.1) / 30 * (x - 340),
            x_range=[340, 370], color=RED_MAIN, stroke_width=5,
        )
        # 오른쪽: 점프 후 더 가파른 상승 추세 (370에서 0.7, 400에서 0.85)
        right_line = axes.plot(
            lambda x: 0.7 + (0.85 - 0.7) / 30 * (x - 370),
            x_range=[370, 400], color=BLUE_MAIN, stroke_width=5,
        )
        jump_line  = DashedLine(
            axes.c2p(370, 0.2), axes.c2p(370, 0.7),
            color=GRAY_MID, stroke_width=2, dash_length=0.1, stroke_opacity=0.8,
        )
        dot_open   = Circle(radius=0.10, color=RED_MAIN,  fill_opacity=0, stroke_width=3).move_to(axes.c2p(370, 0.2))
        dot_closed = Dot(axes.c2p(370, 0.7), radius=0.10, color=BLUE_MAIN, fill_opacity=1)
        step_vg = VGroup(left_line, right_line, jump_line, dot_open, dot_closed)
        return axes_vg, step_vg, cutoff_vg
