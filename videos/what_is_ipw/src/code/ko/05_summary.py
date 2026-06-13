from manim import *
import numpy as np

ICON = "/Users/jhkim/Desktop/personal_study/causal/causal-studio/videos/assets/tabler-icons/icons/outline"

SEVERE = "#b07cff"
MILD = "#39d98a"


class IPWSummary(Scene):
    """
    씬 05 — 요약.

    흐름: 문제(교란) → IPW 핵심(두 그룹을 '=' 로 같게) → 실제 데이터(로지스틱 회귀·ê(X)) → 장점/한계 → takeaway.
    피드백: ⑭'두 그룹을 같게'를 '=' 등호로 ⑮로지스틱 회귀·ê(X) 언급 ⑯강조 최소.
    데이터: 진짜 효과 = 하루(복용 5 < 미복용 6).
    타이밍 기준: build/audio/05_summary.timings.json (총 71.29s)
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

        def dot(color, r=0.13):
            return Circle(radius=r, stroke_color=color, stroke_width=2).set_fill(color, opacity=0.9)

        def people_block(n_sev, n_mild, cols=5, r=0.13, buff=0.12):
            g = VGroup(*[dot(SEVERE, r) for _ in range(n_sev)], *[dot(MILD, r) for _ in range(n_mild)])
            rows = int(np.ceil(len(g) / cols))
            g.arrange_in_grid(rows=rows, cols=cols, buff=buff)
            return g

        def badge(m, txt, color=ORANGE, fs=14):
            return Text(txt, font_size=fs, color=color, weight=BOLD).next_to(m, DOWN, buff=0.04)

        # ============================================================
        # Beat 1 — 문제 요약: 교란 (chunk1~5, 0.00~21.78)
        # ============================================================
        head = Text("정리해 보면", font_size=32, color=GRAY_A, weight=BOLD).to_edge(UP, buff=0.55)
        legend = VGroup(
            dot(SEVERE), Text("중증", font_size=24, color=SEVERE, weight=BOLD),
            dot(MILD), Text("경증", font_size=24, color=MILD, weight=BOLD),
        ).arrange(RIGHT, buff=0.25).next_to(head, DOWN, buff=0.3)
        ques = Text("약은 정말 회복을 앞당길까?", font_size=32, color=YELLOW, weight=BOLD).move_to(UP * 0.9)
        treat = people_block(5, 2, cols=4).move_to(LEFT * 3.3 + DOWN * 0.3)
        treat_l = Text("약 복용", font_size=26, color=BLUE_B, weight=BOLD).next_to(treat, UP, buff=0.3)
        ctrl = people_block(1, 2, cols=3).move_to(RIGHT * 3.3 + DOWN * 0.3)
        ctrl_l = Text("약 미복용", font_size=26, color=RED_B, weight=BOLD).next_to(ctrl, UP, buff=0.3)
        confound = Text("교란 변수 (중증/경증)가 진짜 효과를 가린다", font_size=28, color=PURPLE_A, weight=BOLD).move_to(DOWN * 2.5)

        play_at(0.40, FadeIn(head), run_time=0.4)
        # chunk2 (2.97): 중증/경증 표시(범례)를 띄운다
        play_at(2.97, FadeIn(legend, shift=DOWN * 0.05), FadeIn(ques), run_time=0.5)
        # chunk3 (6.36): 그냥 비교하면 안 됐다 → 두 그룹
        play_at(6.36, FadeOut(ques), FadeIn(treat_l, treat), FadeIn(ctrl_l, ctrl), run_time=0.6)
        # chunk4 (10.36): 복용엔 중증, 미복용엔 경증 — 양쪽 모두 강조
        treat_box = SurroundingRectangle(VGroup(treat_l, treat), color=BLUE_B, buff=0.2, corner_radius=0.12)
        ctrl_box = SurroundingRectangle(VGroup(ctrl_l, ctrl), color=RED_B, buff=0.2, corner_radius=0.12)
        play_at(10.56, Create(treat_box),
                *[Indicate(treat[i], color=SEVERE, scale_factor=1.4) for i in range(5)], run_time=1.2)
        play_at(12.90, ReplacementTransform(treat_box, ctrl_box),
                *[Indicate(ctrl[i], color=MILD, scale_factor=1.4) for i in range(1, 3)], run_time=1.2)
        play_at(14.90, FadeOut(ctrl_box), run_time=0.3)
        play_at(15.76, FadeIn(confound, shift=UP * 0.1), run_time=0.5)               # chunk5
        play_at(20.40, FadeOut(head, legend, treat, treat_l, ctrl, ctrl_l, confound), run_time=0.35)

        # ============================================================
        # Beat 2 — IPW: 가중치를 곱해 두 그룹을 같게 + 진짜 효과 (chunk6~8, 21.78~37.15)
        # ============================================================
        ipw_head = Text("IPW : 가중치를 곱해 두 그룹을 같게", font_size=32, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.5)
        # 원래 구성 (서로 다름)
        bt0 = people_block(5, 2, cols=4, buff=0.32).move_to(LEFT * 3.7 + UP * 0.75)
        bc0 = people_block(1, 2, cols=3, buff=0.32).move_to(RIGHT * 3.7 + UP * 0.75)
        bt_l = Text("복용", font_size=24, color=BLUE_B, weight=BOLD).next_to(bt0, UP, buff=0.25)
        bc_l = Text("미복용", font_size=24, color=RED_B, weight=BOLD).next_to(bc0, UP, buff=0.25)
        bc_l.match_y(bt_l)   # '복용'/'미복용' 텍스트 높이를 맞춘다 (블록 높이가 달라도 동일선상)
        # 개인별 ×가중치 배지
        bt_badges = VGroup(*[badge(bt0[i], "×1.2") for i in range(5)], *[badge(bt0[i], "×2") for i in range(5, 7)])
        bc_badges = VGroup(badge(bc0[0], "×6", YELLOW, 15), *[badge(bc0[i], "×2") for i in range(1, 3)])
        mul_note = Text("× 가중치", font_size=26, color=ORANGE, weight=BOLD).move_to(UP * 0.75)
        # 가중치 적용 후 (같은 구성)
        bt1 = people_block(6, 4, cols=5).move_to(LEFT * 3.7 + UP * 0.75)
        bc1 = people_block(6, 4, cols=5).move_to(RIGHT * 3.7 + UP * 0.75)
        approx = MathTex(r"\approx", color=GREEN_B).scale(1.6).move_to(UP * 0.75)
        UNIT = 0.5
        eff_t = VGroup(Text("복용", font_size=22, color=BLUE_B, weight=BOLD),
                       RoundedRectangle(width=5 * UNIT, height=0.36, corner_radius=0.06, stroke_color=BLUE,
                                        stroke_width=2, fill_color=BLUE, fill_opacity=0.5),
                       Text("5일", font_size=22, color=BLUE_B, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.5 + LEFT * 0.4)
        eff_c = VGroup(Text("미복용", font_size=22, color=RED_B, weight=BOLD),
                       RoundedRectangle(width=6 * UNIT, height=0.36, corner_radius=0.06, stroke_color=RED,
                                        stroke_width=2, fill_color=RED, fill_opacity=0.5),
                       Text("6일", font_size=22, color=RED_B, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.3 + LEFT * 0.4)
        eff_lbl = Text("약의 진짜 효과: 하루 단축 ✓", font_size=26, color=GREEN_B, weight=BOLD).to_edge(DOWN, buff=0.4)

        play_at(20.91, FadeIn(ipw_head), FadeIn(bt_l, bt0, bc_l, bc0), run_time=0.5)  # chunk6
        # chunk7 (23.96): 개인별 ×가중치 → 두 그룹 구성 같아짐
        play_at(24.16, LaggedStartMap(FadeIn, bt_badges, shift=DOWN * 0.05, lag_ratio=0.05),
                LaggedStartMap(FadeIn, bc_badges, shift=DOWN * 0.05, lag_ratio=0.05), FadeIn(mul_note), run_time=1.0)
        play_at(26.00, FadeOut(bt_badges, bc_badges, mul_note),
                ReplacementTransform(bt0, bt1), ReplacementTransform(bc0, bc1), FadeIn(approx), run_time=1.0)
        # chunk8 (29.91): 진짜 효과
        play_at(30.11, FadeIn(eff_t, eff_c), run_time=0.5)
        play_at(32.00, FadeIn(eff_lbl, shift=UP * 0.1), run_time=0.5)
        play_at(36.90, FadeOut(ipw_head, bt1, bt_l, bc1, bc_l, approx, eff_t, eff_c, eff_lbl), run_time=0.35)

        # ============================================================
        # Beat 3 — 실제 데이터: 시그모이드 그림 + 개인별 가중치 (chunk9~13, 37.15~61.95)
        # 텍스트를 줄이고 그림으로 채운다.
        # ============================================================
        real_head = Text("실제 데이터에서는", font_size=30, color=GRAY_A, weight=BOLD).to_edge(UP, buff=0.5)
        # 왼쪽: 모델(시그모이드)  /  오른쪽: 개인별 가중치 — 서로 겹치지 않게 좌우로 분리
        ax = Axes(x_range=[-6, 6, 3], y_range=[0, 1, 1], x_length=4.4, y_length=2.1,
                  axis_config={"include_tip": False, "stroke_color": GRAY_B, "include_numbers": False}).move_to(LEFT * 3.7 + UP * 0.25)
        sig = ax.plot(lambda x: 1 / (1 + np.exp(-x)), x_range=[-6, 6], color=ORANGE, stroke_width=4)
        sig_name = Text("로지스틱 회귀", font_size=24, color=ORANGE, weight=BOLD).next_to(ax, UP, buff=0.15)
        ehat = MathTex(r"\hat{e}(X)", color=ORANGE).scale(0.95).next_to(ax, DOWN, buff=0.3)
        ehat_lbl = Text("추정된 성향점수", font_size=20, color=GRAY_A, weight=BOLD).next_to(ehat, DOWN, buff=0.12)

        play_at(37.35, FadeIn(real_head), Create(ax), Create(sig), FadeIn(sig_name), run_time=0.9)  # chunk9
        play_at(42.83, Write(ehat), FadeIn(ehat_lbl), run_time=0.6)                 # chunk10
        # chunk11 (46.35): 각 개인별로 가중치 부여 (우측)
        ppl = VGroup(dot(SEVERE), dot(SEVERE), dot(MILD), dot(SEVERE), dot(MILD)).arrange(RIGHT, buff=0.45).move_to(RIGHT * 3.3 + UP * 0.6)
        ppl_badges = VGroup(*[badge(ppl[i], "×w", ORANGE, 16) for i in range(len(ppl))])
        indiv_lbl = Text("각 개인별로 가중치", font_size=24, color=ORANGE, weight=BOLD).next_to(ppl, DOWN, buff=0.45)
        play_at(46.13, FadeIn(ppl), LaggedStartMap(FadeIn, ppl_badges, shift=DOWN * 0.05, lag_ratio=0.08),
                FadeIn(indiv_lbl), run_time=1.0)                                     # chunk11
        # chunk12 (50.81): 두 그룹 구성 같게
        balanced = Text("두 그룹 구성을 똑같이 ✓", font_size=24, color=GREEN_B, weight=BOLD).next_to(indiv_lbl, DOWN, buff=0.3)
        play_at(51.01, FadeIn(balanced, shift=UP * 0.08), run_time=0.5)
        # chunk13 (55.45): 모델 부정확하면 신중
        caution = Text("모델이 부정확하면 IPW도 흔들린다 → 정보 선택이 중요", font_size=26, color=YELLOW, weight=BOLD).to_edge(DOWN, buff=0.5)
        play_at(55.65, FadeIn(caution, shift=UP * 0.1), run_time=0.5)
        play_at(61.45, FadeOut(real_head, ax, sig, sig_name, ehat, ehat_lbl, ppl, ppl_badges, indiv_lbl, balanced, caution), run_time=0.4)

        # ============================================================
        # Beat 4 — 장점 / 한계 + takeaway(같은 화면에서 마무리) (chunk14~16, 61.95~81.45)
        # ============================================================
        sig_title = Text("IPW의 의의", font_size=44, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.8)
        merit = VGroup(
            Text("✓", font_size=34, color=GREEN_B, weight=BOLD),
            Text("실험 없이 관찰 데이터만으로 인과효과 추정", font_size=30, color=GREEN_B, weight=BOLD),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        limit = VGroup(
            Text("△", font_size=32, color=GRAY_B, weight=BOLD),
            Text("측정하지 못한 교란 변수가 있으면 한계", font_size=30, color=GRAY_A, weight=BOLD),
        ).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.8)

        play_at(61.92, FadeIn(sig_title, shift=DOWN * 0.1), FadeIn(merit, shift=UP * 0.1), run_time=0.6)  # chunk14
        play_at(69.49, FadeIn(limit, shift=UP * 0.1), run_time=0.5)               # chunk15
        # chunk16 (73.33): 별도 텍스트 없이 제목을 한 번 강조하며 마무리
        play_at(73.53, Indicate(sig_title, color=ORANGE, scale_factor=1.12), run_time=1.0)

        go_to(80.30)
