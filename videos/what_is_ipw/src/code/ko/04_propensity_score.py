from manim import *
import numpy as np

ICON = "/Users/jhkim/Desktop/personal_study/causal/causal-studio/videos/assets/tabler-icons/icons/outline"

SEVERE = "#b07cff"
MILD = "#39d98a"


class PropensityScore(Scene):
    """
    씬 04 — 성향점수와 로지스틱 회귀로 확률 추정.

    흐름: (직접 셈의 한계) → 변수 多 → 성향점수 e(X) → 로지스틱 회귀 + 시그모이드 → 추정 ê(X)
          → IPW 동일 적용 → 모델이 틀리면(나이 누락) → 정보 선택이 중요.
    피드백: ⑦"문제가 있습니다" ⑧변수 아이콘 ⑩ML 시각화+ê(X) ⑪시그모이드 ⑫큰 박스 ⑬회귀식+나이누락 ⑯강조 최소.
    이전 씬(03): w = T/e(X) + (1-T)/(1-e(X)). 다음 씬(05): 요약.
    타이밍 기준: build/audio/04_propensity_score.timings.json (총 104.03s)
    """

    def construct(self):
        self.camera.background_color = "#0a0a0a"
        self.t = 0.0

        def go_to(target_time):
            dt = target_time - self.t
            if dt > 0:
                self.wait(dt)
                self.t += dt

        def play_at(target_time, *anims, run_time=0.5):
            go_to(target_time)
            self.play(*anims, run_time=run_time)
            self.t += run_time

        def icon(name, color, height=1.0):
            m = SVGMobject(f"{ICON}/{name}.svg")
            m.set_stroke(color, width=3)
            m.set_fill(color, opacity=0)
            m.scale_to_fit_height(height)
            return m

        # ============================================================
        # Beat 1 — 직접 셈의 한계 → 문제 제기 (chunk 0~1, 0.00~8.13)
        # ============================================================
        recap = VGroup(
            VGroup(Text("중증", font_size=28, color=SEVERE, weight=BOLD),
                   MathTex(r"\tfrac{5}{6}", color=SEVERE).scale(0.95)).arrange(RIGHT, buff=0.25),
            VGroup(Text("경증", font_size=28, color=MILD, weight=BOLD),
                   MathTex(r"\tfrac{2}{4}", color=MILD).scale(0.95)).arrange(RIGHT, buff=0.25),
        ).arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        recap_lbl = Text("직접 세어 구한 확률", font_size=26, color=GRAY_B, weight=BOLD).next_to(recap, UP, buff=0.5)
        problem = Text("그런데, 문제가 있습니다.", font_size=40, color=YELLOW, weight=BOLD).move_to(DOWN * 1.6)

        play_at(0.40, FadeIn(recap_lbl), FadeIn(recap), run_time=0.5)          # chunk1
        play_at(5.95, FadeIn(problem, shift=UP * 0.1), run_time=0.5)           # chunk2
        play_at(8.00, FadeOut(recap_lbl, recap, problem), run_time=0.3)

        # ============================================================
        # Beat 2 — 현실엔 변수가 많다 (아이콘) (chunk 2~3, 8.13~19.50)
        # ============================================================
        def var_icon(name, label, color):
            ic = icon(name, color, height=0.95)
            lb = Text(label, font_size=24, color=color, weight=BOLD)
            return VGroup(ic, lb).arrange(DOWN, buff=0.25)

        v1 = var_icon("gender-bigender", "성별", BLUE_B)
        v2 = var_icon("calendar", "나이", TEAL_B)
        v3 = var_icon("weight", "체중", GOLD_B)
        v4 = var_icon("stethoscope", "기저질환", RED_B)
        vars_row = VGroup(v1, v2, v3, v4).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        hard = Text("교란변수가 많으면 손으로 셀 수 없다", font_size=30, color=GRAY_A, weight=BOLD).move_to(DOWN * 2.2)

        play_at(8.33, LaggedStartMap(FadeIn, vars_row, lag_ratio=0.25), run_time=1.6)  # chunk3
        play_at(13.81, FadeIn(hard, shift=UP * 0.1), run_time=0.5)             # chunk4
        play_at(18.56, FadeOut(vars_row, hard), run_time=0.3)                  # chunk5

        # ============================================================
        # Beat 3 — 성향점수 정의: e(X) 먼저, '성향점수' 이름은 목소리에 맞춰 뒤에 (chunk6~7)
        # ============================================================
        ps_title = Text("성향점수", font_size=44, color=ORANGE, weight=BOLD).move_to(UP * 1.3)
        ps_eq = MathTex(r"e(X) = P(\,T=1 \mid X\,)", color=WHITE).scale(1.0).move_to(UP * 0.1)
        ps_gloss = Text("환자 정보를 고려한, 약을 먹을 확률", font_size=28, color=GRAY_A, weight=BOLD).move_to(DOWN * 1.1)

        play_at(21.40, Write(ps_eq), run_time=0.7)                            # chunk6: e(X) 먼저
        play_at(23.40, FadeIn(ps_gloss), run_time=0.5)
        play_at(25.60, FadeIn(ps_title, shift=DOWN * 0.1), run_time=0.5)       # '성향점수라고 부릅니다'
        play_at(27.23, Indicate(ps_eq, color=ORANGE, scale_factor=1.1), run_time=0.7)  # chunk7
        play_at(30.16, FadeOut(ps_title, ps_eq, ps_gloss), run_time=0.3)

        # ============================================================
        # Beat 4 — 모델 흐름 + 시그모이드 (chunk 8~13, 32.60~67.06)
        # 환자 정보·약 먹을 확률 먼저, '로지스틱 회귀'는 나중에 채워 넣는다.
        # ============================================================
        in_node = Text("환자 정보", font_size=26, color=GRAY_A, weight=BOLD).move_to(LEFT * 4.3)
        box_rect = RoundedRectangle(width=3.4, height=1.3, corner_radius=0.2, stroke_color=ORANGE, stroke_width=2.5)
        out_node = Text("약 먹을 확률", font_size=26, color=WHITE, weight=BOLD).move_to(RIGHT * 4.3)
        flow = VGroup(in_node, box_rect, out_node).arrange(RIGHT, buff=0.9).move_to(UP * 2.2)
        ar1 = Arrow(in_node.get_right(), box_rect.get_left(), color=GRAY_B, stroke_width=4, buff=0.2)
        ar2 = Arrow(box_rect.get_right(), out_node.get_left(), color=GRAY_B, stroke_width=4, buff=0.2)
        box_q = Text("?", font_size=40, color=GRAY_B, weight=BOLD).move_to(box_rect.get_center())
        box_lbl = Text("로지스틱 회귀", font_size=26, color=ORANGE, weight=BOLD).move_to(box_rect.get_center())

        # chunk8 (30.46): 환자 정보 → ? → 약 먹을 확률 (모델은 아직 비워 둠)
        play_at(30.66, FadeIn(in_node, out_node), Create(box_rect), FadeIn(box_q),
                GrowArrow(ar1), GrowArrow(ar2), run_time=0.7)
        # chunk9 (35.76): 그 모델이 '로지스틱 회귀'
        play_at(35.96, ReplacementTransform(box_q, box_lbl), run_time=0.6)

        # (b) 시그모이드 그래프
        ax = Axes(x_range=[-6, 6, 3], y_range=[0, 1, 0.5], x_length=5.2, y_length=2.3,
                  axis_config={"include_tip": False, "stroke_color": GRAY_B},
                  y_axis_config={"include_numbers": True, "font_size": 20}).move_to(DOWN * 1.0)
        sig = ax.plot(lambda x: 1 / (1 + np.exp(-x)), x_range=[-6, 6], color=ORANGE, stroke_width=4)
        line0 = DashedLine(ax.c2p(-6, 0), ax.c2p(6, 0), color=GRAY_D, stroke_width=1.5)
        line1 = DashedLine(ax.c2p(-6, 1), ax.c2p(6, 1), color=GRAY_D, stroke_width=1.5)
        sig_name = Text("sigmoid", font_size=26, color=ORANGE, weight=BOLD, slant=ITALIC).next_to(ax, UP, buff=0.12)

        # chunk10 (38.41): 성별·증상 정보 → 시그모이드가 0~1로
        play_at(38.61, Create(ax), FadeIn(line0, line1, sig_name), run_time=0.8)
        play_at(39.80, Create(sig), run_time=2.0)

        # chunk11 (48.39): 입력 작을 때 0, 클 때 1 — 양 끝 강조 (라벨은 곡선 밖으로)
        lo_dot = Dot(ax.c2p(-5, 1 / (1 + np.exp(5))), color=BLUE_B, radius=0.09)
        hi_dot = Dot(ax.c2p(5, 1 / (1 + np.exp(-5))), color=GREEN_B, radius=0.09)
        lo_lbl = Text("입력 작음 → 0", font_size=16, color=BLUE_B, weight=BOLD).move_to(ax.c2p(-3.0, 0)).shift(DOWN * 0.50)
        hi_lbl = Text("입력 큼 → 1", font_size=16, color=GREEN_B, weight=BOLD).move_to(ax.c2p(3.0, 1)).shift(UP * 0.40)
        play_at(45.80, FadeIn(lo_dot), Flash(lo_dot, color=BLUE_B), FadeIn(lo_lbl, shift=UP * 0.08), run_time=0.7)  # chunk11
        play_at(47.80, FadeIn(hi_dot), Flash(hi_dot, color=GREEN_B), FadeIn(hi_lbl, shift=DOWN * 0.08), run_time=0.7)

        out_lbl = Text("출력은 항상 0 ~ 1 = 확률", font_size=26, color=GREEN_B, weight=BOLD).to_edge(DOWN, buff=0.4)
        play_at(51.28, FadeIn(out_lbl, shift=UP * 0.1), run_time=0.5)          # chunk12
        # chunk13 (57.21): 추정된 성향점수 ê(X)
        ehat = MathTex(r"\hat{e}(X)", color=ORANGE).scale(1.0).next_to(out_node, DOWN, buff=0.25)
        ehat_lbl = Text("추정된 성향점수", font_size=22, color=GRAY_A, weight=BOLD).next_to(ehat, DOWN, buff=0.12)
        play_at(57.41, FadeIn(ehat), FadeIn(ehat_lbl), run_time=0.6)           # chunk13
        play_at(61.00, FadeOut(in_node, out_node, box_rect, box_lbl, ar1, ar2, ax, sig, line0, line1,
                               sig_name, lo_dot, hi_dot, lo_lbl, hi_lbl, out_lbl, ehat, ehat_lbl), run_time=0.4)

        # ============================================================
        # Beat 5 — 추정 성향점수로 IPW (큰 박스) (chunk 13, 63.95~72.26)
        # ============================================================
        big_box = RoundedRectangle(width=9.0, height=2.6, corner_radius=0.25,
                                   stroke_color=GRAY_B, stroke_width=2, fill_opacity=0).move_to(UP * 0.1)
        ipw_eq = MathTex(r"\hat{w} = \frac{T}{\hat{e}(X)} + \frac{1-T}{1-\hat{e}(X)}", color=WHITE).scale(1.15).move_to(UP * 0.1)
        same = Text("그다음은 앞에서 본 그대로..", font_size=28, color=GRAY_A, weight=BOLD).next_to(big_box, UP, buff=0.4)

        play_at(61.55, FadeIn(same), Create(big_box), run_time=0.6)           # chunk14
        play_at(63.50, Write(ipw_eq), run_time=1.0)
        play_at(69.00, FadeOut(same, big_box, ipw_eq), run_time=0.35)

        # ============================================================
        # Beat 6 — 모델이 틀리면: 나이 누락 회귀식 + 그래프 (chunk 14~18, 72.26~98.50)
        # ============================================================
        warn = Text("성향점수를 잘 추정했을 때만 통한다", font_size=30, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.55)
        # 회귀식 (나이 항 빠짐) — 위는 완성된 모델식, 아래는 누락 정보를 분리해 시선 경쟁을 줄인다.
        reg = MathTex(r"\text{logit}\,\hat{e}(X) = \beta_0 + \beta_1 x_1 + \beta_2 x_2", color=WHITE).scale(0.88).move_to(UP * 1.6)
        reg_legend = Text("x₁ : 성별    x₂ : 증상", font_size=22, color=GRAY_A, weight=BOLD).next_to(reg, DOWN, buff=0.25)
        miss_expr = VGroup(
            MathTex(r"x_3", color=RED_B).scale(0.76),
            Text("= 나이", font_size=22, color=RED_B, weight=BOLD),
        ).arrange(RIGHT, buff=0.08)
        miss = VGroup(
            Text("누락된 변수", font_size=22, color=RED_B, weight=BOLD),
            miss_expr,
        ).arrange(RIGHT, buff=0.25).next_to(reg_legend, DOWN, buff=0.28)
        miss_cross = Cross(miss_expr, stroke_color=RED, stroke_width=4)

        # 회귀 그래프: 점들 + 잘못 맞춘 직선
        ax2 = Axes(x_range=[0, 6, 2], y_range=[0, 6, 2], x_length=4.6, y_length=2.55,
                   axis_config={"include_tip": False, "stroke_color": GRAY_B, "include_numbers": False}).move_to(DOWN * 1.55)
        # 실제 패턴은 산처럼 휘어 있는데(나이 효과), 직선은 그것을 전혀 못 맞춘다
        pts_x = [0.5, 1.3, 2.1, 3.0, 3.9, 4.7, 5.4]
        pts_y = [1.0, 3.0, 5.0, 5.3, 4.6, 2.4, 1.0]
        dots = VGroup(*[Dot(ax2.c2p(x, y), color=TEAL_B, radius=0.08) for x, y in zip(pts_x, pts_y)])
        bad_line = Line(ax2.c2p(0, 1.3), ax2.c2p(6, 4.6), color=RED_B, stroke_width=3)
        graph_lbl = Text("실제 확률과 크게 어긋남", font_size=24, color=RED_B, weight=BOLD).next_to(ax2, RIGHT, buff=0.3)

        play_at(69.67, FadeIn(warn), run_time=0.4)                            # chunk15~16
        play_at(75.71, FadeIn(reg), FadeIn(reg_legend), run_time=0.5)         # chunk17 (성별·증상만)
        play_at(80.50, FadeIn(miss), Create(miss_cross), run_time=0.7)        # chunk17 (나이 누락)
        play_at(85.50, Create(ax2), LaggedStartMap(FadeIn, dots, lag_ratio=0.1), run_time=0.9)
        play_at(91.08, Create(bad_line), FadeIn(graph_lbl), run_time=0.7)     # chunk18 (확률 어긋남)

        # ============================================================
        # Beat 7 — 마무리: 텍스트 추가 없이 기존 화면을 유지하고 문제점만 강조 (chunk19, 96.83~)
        # ============================================================
        play_at(97.03, Indicate(VGroup(ax2, dots, bad_line, graph_lbl), color=RED_B, scale_factor=1.05), run_time=1.0)
        play_at(99.30, Indicate(miss, color=RED_B, scale_factor=1.25), run_time=0.9)

        go_to(103.80)
