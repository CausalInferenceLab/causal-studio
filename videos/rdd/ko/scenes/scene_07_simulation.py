from manim import *

from videos.rdd.shared.common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene07Simulation(Scene):
    """
    Scene 07: simulation
    스크립트: videos/rdd/ko/narration/07_simulation.txt
    build/audio/07_simulation.timings.json 기준 타이밍 (총 61.18s)

    Beat1 chunk1  ( 0.00~ 2.09s)  타이틀 (2.09s)
    Beat2 chunk2  ( 2.09~16.49s)  설정 소개: cutoff=370, τ=0.5, N=500 (14.40s)
    Beat3 chunk3  (16.49~35.53s)  500명 산점도 + DGP 공식 (19.04s)
    Beat4 chunk4  (35.53~45.14s)  좌우 회귀선 적합 (9.61s)
    Beat5 chunk5  (45.14~58.28s)  결과: 절편 2.02·2.50, τ̂=0.48 (13.14s)
    Beat6 chunk6  (58.28~64.90s)  마무리: RDD 복원 성공 (6.61s)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~2.09s) ────────────────────────
        title = VGroup(
            Text("시뮬레이션", font=FONT, font_size=44, color=WHITE),
            Text("RDD가 처치 효과를 복원할 수 있을까?", font=FONT, font_size=26, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.5)
        self.wait(0.59)
        self.play(FadeOut(title), run_time=0.3)  # chunk1 end ~2.09s

        # ── Beat 2 (chunk2: 2.09~15.09s, 13.0s) ────────────
        # 새로 등장: 설정 소개 카드 4개
        # 핵심 시선: cutoff=70, 진짜 τ=0.5, N=500
        # 지워질 요소: FadeOut → Beat3
        setup_header = Text("시뮬레이션 설정", font=FONT, font_size=30, color=WHITE).move_to(UP * 1.7)
        setup_items = VGroup(
            self._setup_row("Cutoff", "370점  (이상 장학금 지급)", YELLOW_MAIN),
            self._setup_row("실제 처치 효과", "학점 0.5점 상승", GREEN_MAIN),
            self._setup_row("표본 크기 N", "500명", BLUE_MAIN),
            self._setup_row("Running Variable", "수능 점수", GRAY_MID),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(setup_header, DOWN, buff=0.45)

        self.play(FadeIn(setup_header, shift=DOWN * 0.15), run_time=0.5)
        for item in setup_items:
            self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(10.22)
        self.play(FadeOut(VGroup(setup_header, setup_items)), run_time=0.5)  # chunk2 end ~14.91s

        # ── 공통 그래프 구성 (Beat3~6 유지) ─────────────────
        axes = Axes(
            x_range=[340, 401, 10], y_range=[1.0, 4.0, 0.5],
            x_length=8.5, y_length=4.5,
            axis_config={
                "color": GRAY_MID, "stroke_width": 1.2,
                "include_tip": True, "tip_width": 0.12, "tip_height": 0.12,
            },
            x_axis_config={"numbers_to_include": [340, 350, 360, 370, 380, 390, 400]},
            y_axis_config={"numbers_to_include": [1.5, 2.0, 2.5, 3.0, 3.5]},
        ).move_to(RIGHT * 0.3 + UP * 0.4)

        y_lbl = Text("성적(GPA)", font=FONT, font_size=12, color=GRAY_MID)
        y_lbl.next_to(axes, LEFT, buff=0.1)
        x_lbl = Text("수능 점수 (점)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_center(), DOWN, buff=0.55)

        cutoff_line = DashedLine(
            axes.c2p(370, 1.0), axes.c2p(370, 4.0),
            color=YELLOW_MAIN, stroke_width=2.5, dash_length=0.12,
        )
        cutoff_lbl = Text("Cutoff (370점)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
            axes.c2p(370, 4.0), UR, buff=0.05
        )

        rng = np.random.default_rng(42)
        n = 500
        xs = rng.uniform(340, 400, n)
        treated = (xs >= 370).astype(float)
        ys = 2.0 + 0.015 * (xs - 370) + 0.5 * treated + rng.normal(0, 0.3, n)

        scatter_left = VGroup(*[
            Dot(axes.c2p(x, y), color=RED_MAIN, radius=0.04, fill_opacity=0.55)
            for x, y in zip(xs, ys) if x < 370 and 1.0 <= y <= 4.0
        ])
        scatter_right = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE_MAIN, radius=0.04, fill_opacity=0.55)
            for x, y in zip(xs, ys) if x >= 370 and 1.0 <= y <= 4.0
        ])

        legend = VGroup(
            VGroup(
                Dot(color=RED_MAIN, radius=0.09),
                Text("미수혜 (<370점)", font=FONT, font_size=16, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Dot(color=BLUE_MAIN, radius=0.09),
                Text("수혜 (≥370점)", font=FONT, font_size=16, color=BLUE_MAIN),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend.move_to(axes.get_corner(UR) + LEFT * 1.5 + DOWN * 0.4)

        # ── Beat 3 (chunk3: 15.09~32.09s, 17.0s) ───────────
        # 새로 등장: 축·cutoff·DGP 공식·산점도·범례 순차 등장
        # 핵심 시선: 데이터 생성 공식 → 산점도 등장
        # 지워질 요소: dgp_formula FadeOut → Beat4
        dgp_formula = VGroup(
            MathTex(
                r"y_i = 2.0 + 0.015(x_i - 370) + 0.5 \cdot T_i + \varepsilon_i",
                font_size=26, color=WHITE,
            ),
            MathTex(r"T_i = 1 \;(x_i \geq 370), \quad \varepsilon \sim \mathcal{N}(0,\,0.09)",
                    font_size=16, color=GRAY_MID),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 3.1)

        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=0.8)
        self.play(Create(cutoff_line), FadeIn(cutoff_lbl), run_time=0.5)
        self.play(FadeIn(dgp_formula), run_time=0.7)
        self.play(FadeIn(scatter_left), run_time=2.0)
        self.play(FadeIn(scatter_right), run_time=2.0)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(11.49)
        self.play(FadeOut(dgp_formula), run_time=0.4)  # chunk3 end ~33.30s

        # ── Beat 4 (chunk4: 32.09~41.70s, 9.61s) ───────────
        # 남는 요소: 축·cutoff·산점도·범례
        # 새로 등장: 좌우 회귀선 + 하단 설명
        # 핵심 시선: 기준점 70에서 좌·우 각각 독립 추정
        # 지워질 요소: reg_desc FadeOut → Beat5
        left_line = axes.plot(
            lambda x: 2.02 + 0.015 * (x - 370), x_range=[340, 370],
            color=RED_MAIN, stroke_width=4.5,
        )
        right_line = axes.plot(
            lambda x: 2.50 + 0.015 * (x - 370), x_range=[370, 400],
            color=BLUE_MAIN, stroke_width=4.5,
        )
        reg_desc = Text(
            "기준점 좌·우에 각각 독립적으로 회귀선 적합",
            font=FONT, font_size=19, color=WHITE,
        ).move_to(DOWN * 3.1)

        self.play(Create(left_line), run_time=0.9)
        self.play(Create(right_line), run_time=0.9)
        self.play(FadeIn(reg_desc), run_time=0.5)
        self.wait(6.91)
        self.play(FadeOut(reg_desc), run_time=0.4)  # chunk4 end ~41.70s

        # ── Beat 5 (chunk5: 41.70~54.57s, 12.87s) ───────────
        # 남는 요소: 축·cutoff·산점도·범례·회귀선
        # 새로 등장: 절편 점 + 레이블 + 점프 화살표 + 결과 박스
        # 핵심 시선: τ̂=0.47 ≈ 0.5 (진짜 처치 효과)
        left_dot = Dot(axes.c2p(370, 2.02), color=RED_MAIN, radius=0.12)
        right_dot = Dot(axes.c2p(370, 2.50), color=BLUE_MAIN, radius=0.12)
        left_dot_lbl = Text("2.02", font=FONT, font_size=18, color=WHITE).next_to(
            axes.c2p(370, 2.02), LEFT, buff=0.14
        )
        right_dot_lbl = Text("2.50", font=FONT, font_size=18, color=WHITE).next_to(
            axes.c2p(370, 2.50), LEFT, buff=0.14
        )

        jump_arrow = DoubleArrow(
            axes.c2p(370, 2.02), axes.c2p(370, 2.50),
            color=YELLOW_MAIN, buff=0, stroke_width=4, tip_length=0.15,
        )
        jump_lbl = VGroup(
            Text("처치 효과 추정 ", font=FONT, font_size=17, color=YELLOW_MAIN),
            MathTex(r"\hat{\tau}", font_size=22, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.08).next_to(jump_arrow, RIGHT, buff=0.15)

        result_desc = VGroup(
            Text("왼쪽 절편: 2.02   |   오른쪽 절편: 2.50", font=FONT, font_size=18, color=WHITE),
            VGroup(
                Text("추정 처치 효과 ", font=FONT, font_size=18, color=YELLOW_MAIN),
                MathTex(r"\hat{\tau} = 0.48", font_size=22, color=YELLOW_MAIN),
                Text("  (실제: τ = 0.5)", font=FONT, font_size=16, color=GREEN_MAIN),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 3.1)

        self.play(
            FadeIn(left_dot), FadeIn(left_dot_lbl),
            FadeIn(right_dot), FadeIn(right_dot_lbl),
            run_time=0.7,
        )
        self.play(Create(jump_arrow), FadeIn(jump_lbl), run_time=0.7)
        self.play(FadeIn(result_desc), run_time=0.6)
        self.wait(9.84)   # chunk5 end ~54.75s

        # ── Beat 6 (chunk6: 54.57~61.02s, 6.45s) ───────────
        # 남는 요소: 축·산점도·회귀선·점프 화살표
        # 새로 등장: 결론 문구 (초록)
        # 핵심 시선: RDD가 처치 효과를 잘 복원한다
        conclusion = Text(
            "기준점 좌우 회귀식 적합 → RDD로 처치 효과 복원 가능",
            font=FONT, font_size=20, color=GREEN_MAIN,
        ).move_to(DOWN * 3.1)

        self.play(FadeOut(result_desc), FadeIn(conclusion), run_time=0.6)
        self.wait(13.66)  # chunk6 end ~68.93s (mp3 재생성 후 길이 반영)

    def _setup_row(self, key: str, val: str, color: str) -> VGroup:
        return VGroup(
            Text(f"{key}: ", font=FONT, font_size=19, color=GRAY_MID),
            Text(val, font=FONT, font_size=19, color=color),
        ).arrange(RIGHT, buff=0.12)
