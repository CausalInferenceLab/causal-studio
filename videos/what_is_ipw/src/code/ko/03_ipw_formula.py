from manim import *
import numpy as np

ICON = "/Users/jhkim/Desktop/personal_study/causal/causal-studio/videos/assets/tabler-icons/icons/outline"

SEVERE = "#b07cff"
MILD = "#39d98a"


class IPWFormula(Scene):
    """
    씬 03 — IPW 가중치를 수식으로 일반화.

    흐름: 한 사람을 기준으로 기호(T, X, e(X)) 정의 → 가중치 = 1/확률 (두 경우) → 한 식으로 합치기(underbrace).
    피드백: ①일반화는 그림으로 ②기호 정의 슬라이드 없이 바로 ③가중치 박스 크게 ⑤underbrace ⑥균형 파트 삭제 ⑯강조 최소.
    데이터/표기: e(X)=P(T=1|X). 복용 w=1/e(X), 미복용 w=1/(1-e(X)).
    이전 씬(02): 역확률 가중치(IPW) 명명·재가중. 다음 씬(04): 확률을 모델로 추정(성향점수).
    타이밍 기준: build/audio/03_ipw_formula.timings.json (총 61.77s)
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
        # Beat 1~2 — 한 사람을 기준으로 기호 정의 (chunk 0~4, 0.00~20.15)
        # 일반화를 '한 사람 그림'으로 표현하고, 그 사람에 T·X·e(X) 를 붙인다.
        # ============================================================
        person = icon("user", WHITE, height=1.5).move_to(LEFT * 1.6 + UP * 2.0)

        # 기호 정의를 왼쪽으로 충분히 옮긴다 (이전엔 우측으로 치우쳐 보였음)
        LEFT_ANCHOR = -4.6

        def define(sym, gloss, color, y):
            m = MathTex(sym, color=color).scale(1.05)
            colon = Text(":", font_size=30, color=GRAY_B)
            g = Text(gloss, font_size=26, color=GRAY_A, weight=BOLD)
            row = VGroup(m, colon, g).arrange(RIGHT, buff=0.28)
            row.move_to([0, y, 0])
            row.shift(RIGHT * (LEFT_ANCHOR - m.get_left()[0]))
            return row, m

        T_def, T_sym = define("T", "약 복용  ( 1 / 0 )", BLUE_B, 0.55)
        X_def, X_sym = define("X", "환자 상태 ( 중증 / 경증 )", SEVERE, -0.55)
        e_def, e_sym = define("e(X)=P(T=1|X)", "약을 먹을 확률", ORANGE, -1.65)

        play_at(0.50, FadeIn(person, shift=DOWN * 0.1), run_time=0.5)
        play_at(6.10, FadeIn(T_def, shift=RIGHT * 0.1), run_time=0.5)          # chunk3
        play_at(11.40, FadeIn(X_def, shift=RIGHT * 0.1), run_time=0.5)         # chunk4
        play_at(15.60, FadeIn(e_def, shift=RIGHT * 0.1), run_time=0.5)         # chunk5

        # ============================================================
        # Beat 3 — 가중치 = 확률의 역수, 두 경우 (chunk6~9, 20.90~44.44)
        # (역수 뒤집기 애니메이션은 렌더 행 이슈로 제거)
        # ============================================================
        play_at(20.30, FadeOut(person, T_def, X_def), run_time=0.4)            # chunk6
        play_at(20.90, e_def.animate.scale(0.85).to_edge(UP, buff=0.5), run_time=0.5)  # e(X) 위로
        rule = Text("규칙: 확률의 역수를 가중치로", font_size=30, color=ORANGE, weight=BOLD).move_to(UP * 1.55)
        play_at(22.30, FadeIn(rule), run_time=0.5)

        # 두 경우의 가중치 식
        case_t = VGroup(
            Text("약 복용", font_size=28, color=BLUE_B, weight=BOLD),
            MathTex(r"(T=1)", color=BLUE_B).scale(0.65),
            MathTex(r"w = \frac{1}{e(X)}", color=BLUE_B).scale(1.2),
        ).arrange(RIGHT, buff=0.4).move_to(UP * 0.55)
        case_c = VGroup(
            Text("약 미복용", font_size=28, color=RED_B, weight=BOLD),
            MathTex(r"(T=0)", color=RED_B).scale(0.65),
            MathTex(r"w = \frac{1}{1 - e(X)}", color=RED_B).scale(1.2),
        ).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.1)
        rare = Text("드물게 일어난 일일수록 가중치가 커짐", font_size=26, color=YELLOW, weight=BOLD).to_edge(DOWN, buff=0.55)

        play_at(27.50, FadeIn(case_t, shift=UP * 0.08), run_time=0.6)         # chunk7
        play_at(31.60, FadeIn(case_c, shift=UP * 0.08), run_time=0.5)          # chunk8
        play_at(39.50, FadeIn(rare), run_time=0.45)                           # chunk9
        play_at(43.10, FadeOut(e_def, rule, case_t, case_c, rare), run_time=0.35)

        # ============================================================
        # Beat 4 — 한 식으로 합치기 (underbrace) (chunk 9~12, 43.75~61.77)
        # ============================================================
        combined = MathTex("w", "=", r"\frac{T}{e(X)}", "+", r"\frac{1-T}{1-e(X)}").scale(1.25)
        combined.move_to(UP * 0.9)
        combined[2].set_color(BLUE_B)
        combined[4].set_color(RED_B)

        brace_t = Brace(combined[2], DOWN, color=BLUE_B)
        brace_c = Brace(combined[4], DOWN, color=RED_B)
        lbl_t = Text("왼쪽은 약 복용", font_size=24, color=BLUE_B, weight=BOLD).next_to(brace_t, DOWN, buff=0.15)
        lbl_c = Text("오른쪽은 약 미복용", font_size=24, color=RED_B, weight=BOLD).next_to(brace_c, DOWN, buff=0.15)
        # chunk12 — T에 숫자를 직접 대입해서 보여 준다 (0이 되는 항은 회색)
        sub1 = MathTex(r"T=1:", r"\ w =", r"\frac{1}{e(X)}", r"+", r"\frac{0}{1-e(X)}").scale(0.82)
        sub1[0].set_color(BLUE_B)
        sub1[4].set_color(GRAY_D)
        sub0 = MathTex(r"T=0:", r"\ w =", r"\frac{0}{e(X)}", r"+", r"\frac{1}{1-e(X)}").scale(0.82)
        sub0[0].set_color(RED_B)
        sub0[2].set_color(GRAY_D)
        subs = VGroup(sub1, sub0).arrange(DOWN, buff=0.45).move_to(DOWN * 0.7)
        # chunk13 — 누구에게나 가중치 '하나씩' (개인별)
        one = icon("user", WHITE, height=0.55)
        one_w = MathTex("w", color=ORANGE).scale(0.8)
        one_arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, color=GRAY_B, stroke_width=4, buff=0.05)
        closing = VGroup(one, one_arrow, one_w,
                         Text(" 자기 몫의 가중치 하나씩", font_size=26, color=ORANGE, weight=BOLD)
                         ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.5)

        play_at(44.60, Write(combined), run_time=0.8)                         # chunk10
        # chunk11 (47.14): 왼쪽/오른쪽 항
        play_at(47.34, GrowFromCenter(brace_t), FadeIn(lbl_t),
                GrowFromCenter(brace_c), FadeIn(lbl_c), run_time=0.6)
        # chunk12 (52.80): T=1이면 왼쪽만, T=0이면 오른쪽만 → 숫자 대입
        play_at(53.00, FadeOut(brace_t, brace_c, lbl_t, lbl_c),
                combined.animate.to_edge(UP, buff=1.4).scale(0.9), run_time=0.5)
        play_at(53.70, FadeIn(sub1, shift=UP * 0.08), run_time=0.45)
        play_at(54.80, FadeIn(sub0, shift=UP * 0.08), run_time=0.45)
        # chunk13 (57.21): 자기 경우에 맞는 가중치 하나씩
        play_at(57.41, FadeIn(closing, shift=UP * 0.1), run_time=0.5)

        go_to(61.75)
