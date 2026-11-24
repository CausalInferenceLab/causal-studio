from manim import *

from videos.rdd.shared.common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene05Formula(Scene):
    """
    Scene 05: formula (LATE와 회귀식)
    스크립트: videos/rdd/ko/narration/05_formula.txt
    참조 ipynb: book/rdd/01_rdd_basic_ko.ipynb §5 수식으로 이해하는 RDD (cell 10–11)
    총 길이: 79.05s (레이트 발음 반영 재생성)

    ipynb cell 12 핵심 파라미터:
        β₀=2.0, β₁=0.015, β₂=0.5, β₃=0.005, c=70

    직전 Scene04 마지막 화면: 새 화면 시작
    참조: 3b1b/_2019/clacks/simple_scenes.py — 수식 순서 설명·하이라이트 리듬

    .timings.json → Beat 대응:
      Beat1 chunk1 ( 0.00~ 6.92s) LATE 헤더 + 직관 그래프 (점프=LATE)
      Beat2 chunk2 ( 6.92~19.13s) 그래프(상)+산점도: E[Y|c+]·E[Y|c-] 점 / 수식(하): τ 한 줄
      Beat3 chunk3 (19.13~29.07s) 회귀선 다이어그램 (좌빨/우파/점프)
      Beat4 chunk4 (29.07~31.21s) 회귀식 전체 등장 (상단 고정)
      Beat5 chunk5 (31.21~37.57s) 회귀식 + 소형 그래프 + β₀ 주석
      Beat6 chunk6 (37.57~43.70s) 회귀식 + 소형 그래프 + β₂ 주석
      Beat7 chunk7 (43.70~51.08s) 회귀식 + 소형 그래프 + β₁·β₃ 주석
      Beat8 chunk8 (51.08~60.60s) 그래프+수식 유지 → 좌극한·우극한·τ=β̂₂ 오버레이
      Beat9 chunk9 (60.60~79.05s) 국소적 효과 한계 (수능 370점 예시)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~7.20s) ────────────────────────
        # 새로 등장: LATE 헤더(상) + 직관 그래프(중하, 점프=LATE)
        # 핵심 시선: 기준점에서의 점프 = LATE
        # 지워질 요소: FadeOut → Beat2
        late_header = VGroup(
            Text("LATE", font=FONT, font_size=30, color=BLUE_MAIN),
            Text("Local Average Treatment Effect", font=FONT, font_size=20, color=GRAY_MID),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.8)

        ax1, ll1, rl1, cl1 = self._make_rdd_graph(6.5, 3.0, DOWN * 0.2)
        jump1 = Arrow(ax1.c2p(70, 2.0), ax1.c2p(70, 2.5), buff=0,
                      color=YELLOW_MAIN, stroke_width=3, max_tip_length_to_length_ratio=0.22)
        late_lbl = MathTex(r"\text{LATE} = \hat{\tau}", font_size=26, color=YELLOW_MAIN).next_to(jump1, RIGHT, buff=0.12)

        self.play(FadeIn(late_header, shift=DOWN * 0.2), run_time=0.7)
        self.play(Create(ax1), Create(ll1), Create(rl1), run_time=1.0)
        self.play(Create(cl1), GrowArrow(jump1), FadeIn(late_lbl), run_time=0.6)
        self.wait(4.4)
        self.play(FadeOut(VGroup(late_header, ax1, ll1, rl1, cl1, jump1, late_lbl)), run_time=0.5)
        # chunk1 end ~7.20s

        # ── Beat 2 (chunk2: 7.20~20.39s) ────────────────────
        # 제거: Beat1 전부
        # 새로 등장: 그래프+산점도(상) + E[Y|c+]·E[Y|c-] 점 + τ수식(중하) + 연속성 줄글(최하)
        # 핵심 시선: 두 기대값의 차이 = 처치 효과
        ax2, ll2, rl2, cl2 = self._make_rdd_graph(6.0, 2.5, UP * 1.2)

        rng2 = np.random.default_rng(42)
        xs_l = rng2.uniform(42, 68, 14)
        ys_l = 2.0 + 0.015 * (xs_l - 70) + rng2.normal(0, 0.18, 14)
        xs_r = rng2.uniform(72, 98, 14)
        ys_r = 2.5 + 0.02 * (xs_r - 70) + rng2.normal(0, 0.18, 14)
        scatter2 = VGroup(
            *[Dot(ax2.c2p(x, y), color=RED_MAIN, radius=0.045, fill_opacity=0.5)
              for x, y in zip(xs_l, ys_l) if 1.5 <= y <= 4.5],
            *[Dot(ax2.c2p(x, y), color=BLUE_MAIN, radius=0.045, fill_opacity=0.5)
              for x, y in zip(xs_r, ys_r) if 1.5 <= y <= 4.5],
        )

        e_r_dot = Dot(ax2.c2p(70, 2.5), color=BLUE_MAIN, radius=0.09)
        e_r_lbl = MathTex(r"\mathbb{E}[Y \mid X\!=\!c^+]", font_size=20, color=BLUE_MAIN).next_to(e_r_dot, UP + RIGHT, buff=0.05)
        e_l_dot = Dot(ax2.c2p(70, 2.0), color=RED_MAIN, radius=0.09)
        e_l_lbl = MathTex(r"\mathbb{E}[Y \mid X\!=\!c^-]", font_size=20, color=RED_MAIN).next_to(e_l_dot, DOWN + RIGHT, buff=0.05)

        tau_eq = MathTex(
            r"\tau_{SRD} = ",
            r"\mathbb{E}[Y \mid X = c^+]",
            r"\;-\;",
            r"\mathbb{E}[Y \mid X = c^-]",
            font_size=28, color=WHITE,
        )
        tau_eq[1].set_color(BLUE_MAIN)
        tau_eq[3].set_color(RED_MAIN)
        tau_eq.move_to(DOWN * 1.5)

        # 요청 1: 연속성 assumption 줄글로
        assumption_note = Text(
            "앞서 말한 가정이 성립한다면, 이 차이는 순수한 처치 효과라고 볼 수 있다.",
            font=FONT, font_size=20, color=WHITE,
        ).move_to(DOWN * 2.6)

        self.play(Create(ax2), Create(ll2), Create(rl2), Create(cl2),
                  FadeIn(scatter2), run_time=0.8)
        self.play(FadeIn(e_r_dot), FadeIn(e_r_lbl), run_time=0.5)
        self.play(FadeIn(e_l_dot), FadeIn(e_l_lbl), run_time=0.5)
        self.wait(2.0)
        self.play(FadeIn(tau_eq, shift=UP * 0.1), run_time=0.6)
        self.wait(3.5)
        self.play(FadeIn(assumption_note, shift=UP * 0.1), run_time=0.6)
        self.wait(2.04)
        self.play(FadeOut(VGroup(ax2, ll2, rl2, cl2, scatter2,
                                 e_r_dot, e_r_lbl, e_l_dot, e_l_lbl,
                                 tau_eq, assumption_note)), run_time=0.6)
        # chunk2 end ~17.74s (new: 10.54s duration, was 13.19s)

        # ── Beat 3 (chunk3: 17.74~28.10s) ───────────────────
        # 새로 등장: 회귀선 다이어그램 (큰 화면, 절편 차이 = τ̂)
        # 핵심 시선: 기준점 c에서 두 회귀선의 점프
        # 끝: 그래프 FadeOut + 회귀식 가운데 FadeIn 동시 → Beat4로 자연 전환
        ax3, ll3, rl3, cl3 = self._make_rdd_graph(7.0, 4.2, ORIGIN + LEFT * 0.2)
        x_lbl = Text("점수 (X)", font=FONT, font_size=18, color=GRAY_MID).next_to(ax3.x_axis, DOWN, buff=0.2)
        y_lbl = Text("GPA", font=FONT, font_size=18, color=GRAY_MID).next_to(ax3.y_axis, LEFT, buff=0.1)
        jump3 = Arrow(ax3.c2p(70, 2.0), ax3.c2p(70, 2.5), buff=0,
                      color=YELLOW_MAIN, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        jump3_lbl = MathTex(r"\hat{\tau}", font_size=26, color=YELLOW_MAIN).next_to(jump3, RIGHT, buff=0.1)
        lbl_left = Text("미처치", font=FONT, font_size=17, color=RED_MAIN).move_to(ax3.c2p(52, 4.1))
        lbl_right = Text("처치", font=FONT, font_size=17, color=BLUE_MAIN).move_to(ax3.c2p(87, 4.1))

        # Beat4~9에서 사용할 회귀식: center 크기(36pt)로 생성, Beat5에서 위로 이동
        formula = MathTex(
            r"Y_i = ", r"\beta_0", r" + ", r"\beta_1",
            r"(X_i - c) + ", r"\beta_2", r"D_i + ", r"\beta_3",
            r"D_i(X_i - c) + \varepsilon_i",
            font_size=36, color=WHITE,
        ).move_to(ORIGIN)

        self.play(Create(ax3), FadeIn(x_lbl, y_lbl), run_time=1.0)
        self.play(Create(ll3), Create(rl3), run_time=1.0)
        self.play(Create(cl3), GrowArrow(jump3), FadeIn(jump3_lbl), run_time=0.6)
        self.play(FadeIn(lbl_left, lbl_right), run_time=0.4)
        self.wait(6.05)
        # "두 절편의 차이를 측정하면 되겠죠" 끝나자마자 그래프 out + 회귀식 in
        self.play(
            FadeOut(VGroup(ax3, x_lbl, y_lbl, ll3, rl3, cl3,
                           jump3, jump3_lbl, lbl_left, lbl_right)),
            FadeIn(formula, shift=UP * 0.15),
            run_time=0.7,
        )
        # chunk3 end ~30.74s

        # ── Beat 4 (chunk4: 30.74~42.63s) ───────────────────
        # 남는 요소: formula (ORIGIN, 큰 크기) — 시청자가 전체 회귀식을 읽을 수 있도록
        # 비워 두는 구역: 위·아래 (formula가 시선 독점)
        # 핵심 시선: 회귀식 전체 구조 — "이 식을 적합하면 두 직선을 알 수 있다"
        self.wait(11.89)
        # chunk4 end ~42.63s

        # ── Beat 5 (chunk5: 42.63~44.63s) ───────────────────
        # 남는 요소: formula
        # 새로 등장: formula → UP*2.8으로 자연스럽게 이동 + 소형 그래프 등장
        # 핵심 시선: "회귀식을 천천히 살펴봅시다" — 수식이 위로 고정됨
        self.play(
            formula.animate.move_to(UP * 2.8).scale(0.833),  # 36pt → 상단 30pt 상당
            run_time=1.0,
        )
        self.wait(1.0)
        # chunk5 end ~44.63s

        # ── Beats 6~8 공유: 소형 그래프 (formula 아래, 설명 위) ──
        sax, sll, srl, scl = self._make_rdd_graph(6.0, 2.5, DOWN * 0.7)

        # ── Beat 6 (chunk6: 44.63~51.08s) ───────────────────
        # 남는 요소: formula(상단) / 새로: 소형 그래프 + β₀ 주석
        # 핵심 시선: β₀ = 절편값
        b0_dot = Dot(sax.c2p(70, 2.0), color=RED_MAIN, radius=0.10)
        b0_h = DashedLine(sax.c2p(40, 2.0), sax.c2p(70, 2.0),
                          color=BLUE_MAIN, stroke_width=1.5, dash_length=0.08)
        b0_ann_lbl = MathTex(r"\beta_0", font_size=22, color=BLUE_MAIN).next_to(
            b0_h.get_center(), UP, buff=0.1)
        b0_ann = VGroup(b0_dot, b0_h, b0_ann_lbl)

        b0_desc = VGroup(
            MathTex(r"\beta_0", font_size=36, color=BLUE_MAIN),
            Text(": 기준점 바로 아래 기대 결과 (미처치 절편)", font=FONT, font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.6)

        self.play(Create(sax), Create(sll), Create(srl), Create(scl), run_time=0.8)
        self.play(FadeIn(b0_ann), run_time=0.5)
        self.play(formula[1].animate.set_color(BLUE_MAIN), FadeIn(b0_desc), run_time=0.5)
        self.wait(4.15)
        self.play(formula[1].animate.set_color(WHITE), FadeOut(VGroup(b0_ann, b0_desc)), run_time=0.5)
        # chunk6 end ~51.08s

        # ── Beat 7 (chunk7: 51.08~56.98s) ───────────────────
        # 남는 요소: formula + 소형 그래프 / 새로: β₂ 점프 화살표 주석
        # 핵심 시선: β₂ = 점프 = 처치 효과 (이 씬의 핵심)
        b2_arrow = Arrow(sax.c2p(70, 2.0), sax.c2p(70, 2.5), buff=0,
                         color=YELLOW_MAIN, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        b2_ann_lbl = MathTex(r"\beta_2", font_size=22, color=YELLOW_MAIN).next_to(b2_arrow, RIGHT, buff=0.1)
        b2_ann = VGroup(b2_arrow, b2_ann_lbl)

        b2_desc = VGroup(
            MathTex(r"\beta_2", font_size=36, color=YELLOW_MAIN),
            Text(": 기준점에서의 점프 = 처치 효과", font=FONT, font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.6)

        self.play(GrowArrow(b2_arrow), FadeIn(b2_ann_lbl), run_time=0.6)
        self.play(formula[5].animate.set_color(YELLOW_MAIN), FadeIn(b2_desc), run_time=0.5)
        self.wait(4.30)
        self.play(formula[5].animate.set_color(WHITE), FadeOut(VGroup(b2_ann, b2_desc)), run_time=0.5)
        # chunk7 end ~56.98s

        # ── Beat 8 (chunk8: 56.98~64.97s) ───────────────────
        # 남는 요소: formula + 소형 그래프 / 새로: β₁(좌선 점) + β₁+β₃(우선 점) 주석
        # 핵심 시선: 두 선의 기울기 차이 = β₃
        mid_l = Dot(sax.c2p(55, 2.0 + 0.015*(55-70)), color=RED_MAIN, radius=0.08)
        b1_ann_lbl = VGroup(
            MathTex(r"\beta_1", font_size=18, color=RED_MAIN),
            Text("(기울기)", font=FONT, font_size=14, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.05).next_to(mid_l, UP + LEFT, buff=0.05)
        b1_ann = VGroup(mid_l, b1_ann_lbl)

        mid_r = Dot(sax.c2p(85, 2.5 + 0.02*(85-70)), color=BLUE_MAIN, radius=0.08)
        b3_ann_lbl = VGroup(
            MathTex(r"\beta_1\!+\!\beta_3", font_size=18, color=BLUE_MAIN),
            Text("(기울기)", font=FONT, font_size=14, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.05).next_to(mid_r, UP + RIGHT, buff=0.05)
        b3_ann = VGroup(mid_r, b3_ann_lbl)

        b13_desc = VGroup(
            VGroup(
                MathTex(r"\beta_1", font_size=32, color=RED_MAIN),
                Text(": 미처치 기울기", font=FONT, font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                MathTex(r"\beta_3", font_size=32, color=BLUE_MAIN),
                Text(": 처치 후 기울기 추가 변화", font=FONT, font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.55)

        self.play(FadeIn(b1_ann), FadeIn(b3_ann), run_time=0.7)
        self.play(
            formula[3].animate.set_color(RED_MAIN),
            formula[7].animate.set_color(BLUE_MAIN),
            FadeIn(b13_desc),
            run_time=0.5,
        )
        self.wait(6.29)
        self.play(
            formula[3].animate.set_color(WHITE),
            formula[7].animate.set_color(WHITE),
            FadeOut(VGroup(b1_ann, b3_ann, b13_desc)),
            run_time=0.5,
        )
        # chunk8 end ~64.97s

        # ── Beat 9 (chunk9: 64.97~76.86s) ───────────────────
        # 남는 요소: formula(상단 UP*2.8) + sax 소형 그래프(하단 DOWN*0.7)
        # 새로 등장: limits_group(중상 UP*2.0) + tau_result(중 UP*1.05)
        # 핵심 시선: τ = β̂₂
        limits_group = VGroup(
            MathTex(r"\lim_{x \to c^-} = \beta_0", font_size=24, color=RED_MAIN),
            MathTex(r"\lim_{x \to c^+} = \beta_0 + \beta_2", font_size=24, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.6).move_to(UP * 2.0)

        tau_result = MathTex(
            r"\therefore \quad \hat{\tau}_{SRD} = \hat{\beta}_2",
            font_size=40, color=YELLOW_MAIN,
        ).move_to(UP * 1.5)

        self.play(FadeIn(limits_group, shift=UP * 0.12), run_time=0.7)
        self.play(Write(tau_result), run_time=0.7)
        self.wait(10.49)
        # chunk9 end ~76.86s

        # ── Beat 10 (chunk10: 76.86~92.65s) ─────────────────
        # 제거: sax + formula + limits + tau / 새로: 국소적 효과 경고 + 예시
        # 핵심 시선: RDD는 기준점 근방의 국소적 효과만 추정
        self.play(
            FadeOut(VGroup(sax, sll, srl, scl, formula, limits_group, tau_result)),
            run_time=0.7,
        )

        local_header = Text(
            "국소적 효과 (Local Effect)", font=FONT, font_size=30, color=YELLOW_MAIN,
        ).move_to(UP * 1.8)

        local_desc = Text(
            "RDD는 기준점 근방 개체들에 한정된 효과만 추정합니다.",
            font=FONT, font_size=22, color=WHITE,
        ).move_to(UP * 0.6)

        example_text = VGroup(
            Text("장학금 기준이 수능 370점이라고 했을 때,", font=FONT, font_size=19, color=GRAY_MID),
            Text("200점대 학생들에게 장학금이 어떤 효과를 낼지는 RDD로 알 수 없습니다.", font=FONT, font_size=19, color=GRAY_MID),
        ).arrange(DOWN, buff=0.15).move_to(DOWN * 0.6)

        self.play(FadeIn(local_header, shift=DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(local_desc, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(example_text, shift=UP * 0.1), run_time=0.6)
        self.wait(13.19)  # chunk10 end ~92.65s + tail

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _make_rdd_graph(self, x_length, y_length, position):
        """axes + 좌우 회귀선(β₀=2.0, β₁=0.015, β₂=0.5, β₃=0.005) + cutoff 점선 반환."""
        axes = Axes(
            x_range=[40, 100, 10], y_range=[1.5, 4.5, 1.0],
            x_length=x_length, y_length=y_length,
            axis_config={
                "color": GRAY_MID, "stroke_width": 1.2,
                "include_tip": True, "tip_width": 0.12, "tip_height": 0.12,
            },
        ).move_to(position)
        left_line = axes.plot(
            lambda x: 2.0 + 0.015*(x - 70), x_range=[40, 70],
            color=RED_MAIN, stroke_width=2.5,
        )
        right_line = axes.plot(
            lambda x: 2.5 + 0.02*(x - 70), x_range=[70, 100],
            color=BLUE_MAIN, stroke_width=2.5,
        )
        cutoff = DashedLine(
            axes.c2p(70, 1.5), axes.c2p(70, 4.5),
            color=GRAY_MID, stroke_width=1.2, dash_length=0.1,
        )
        return axes, left_line, right_line, cutoff
