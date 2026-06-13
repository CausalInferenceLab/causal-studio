from manim import *
import numpy as np

# 공용 tabler 아이콘 경로 (outline 세트)
ICON = "/Users/jhkim/Desktop/personal_study/causal/causal-studio/videos/assets/tabler-icons/icons/outline"


class MedicineQuestionSynced(Scene):
    """
    씬 01 — 감기약은 정말 회복을 앞당기는가? (심슨의 역설 도입)

    핵심: 전체만 보면 약이 해로워 보이지만, 중증/경증으로 나누면 약은 항상 도움이 된다.
    이번 개정 포인트:
      - 비교 대상(회복 기간의 '차이')을 명시적으로 보여 준다.
      - "더 오래 아팠다?"에 표정 아이콘을 같이 띄운다.
      - 그룹(복용이 짧음) → 전체(복용이 김)로 막대가 '직접 뒤집히는' 애니메이션.
      - 장면 사이 블랙아웃 없이 겹쳐서 전환.
      - IPW 영문(Inverse Probability Weighting) 병기.
    타이밍 기준: build/audio/01_medicine_question.timings.json (총 93.45s)
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

        def icon(name, color, height=1.1):
            m = SVGMobject(f"{ICON}/{name}.svg")
            m.set_stroke(color, width=3)
            m.set_fill(color, opacity=0)
            m.scale_to_fit_height(height)
            return m

        UNIT = 0.62  # 1일당 막대 길이

        def make_bar(days, color, y, x0, unit=UNIT):
            bar = RoundedRectangle(width=days * unit, height=0.42, corner_radius=0.07,
                                   stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.5)
            bar.move_to([x0 + days * unit / 2, y, 0])
            return bar

        def bar_row(label, days, color, y, x0, fs=24, unit=UNIT):
            lab = Text(label, font_size=fs, color=color, weight=BOLD)
            lab.move_to([x0 - 0.3 - lab.width / 2, y, 0])
            bar = make_bar(days, color, y, x0, unit)
            val = Text(f"{days:g}일", font_size=fs + 2, color=color, weight=BOLD).next_to(bar, RIGHT, buff=0.18)
            return VGroup(lab, bar, val)

        # ============================================================
        # Beat A — 아픈 사람 → 약 → 회복, 정말 약 때문? (chunk1~2, 0.00~8.03)
        # ============================================================
        sick = icon("mood-sick", RED_B, height=1.5).move_to(LEFT * 3.4 + UP * 0.2)
        happy = icon("mood-happy", GREEN_B, height=1.5).move_to(RIGHT * 3.4 + UP * 0.2)
        rec_arrow = Arrow(sick.get_right(), happy.get_left(), color=WHITE, stroke_width=6, buff=0.5)
        pill = icon("pill", BLUE_B, height=0.95).move_to(UP * 1.45)
        pill_lbl = Text("약", font_size=26, color=BLUE_B, weight=BOLD).next_to(pill, RIGHT, buff=0.15)
        qbig = Text("?", font_size=120, color=RED, weight=BOLD).move_to(DOWN * 1.7)

        play_at(2.00, FadeIn(sick, shift=UP * 0.15), run_time=0.4)            # chunk2
        play_at(3.80, GrowArrow(rec_arrow), FadeIn(happy, shift=UP * 0.15), run_time=0.5)
        play_at(5.20, FadeIn(pill, shift=DOWN * 0.15), FadeIn(pill_lbl), run_time=0.4)
        play_at(7.90, FadeIn(qbig, scale=1.2), run_time=0.4)   # chunk3 "정말 약 때문?"
        beatA = VGroup(sick, happy, rec_arrow, pill, pill_lbl, qbig)

        # ============================================================
        # Beat B — 제목 (chunk4) — 블랙아웃 없이 겹쳐 전환
        # ============================================================
        title = Text("진짜 원인을 가려내려면?", font_size=40, color=YELLOW, weight=BOLD).move_to(UP * 0.3)
        play_at(10.50, FadeOut(beatA), FadeIn(title), run_time=0.5)            # chunk4

        # ============================================================
        # Beat C — 무엇을 비교? 회복 기간의 '차이' (chunk5~6)
        # ============================================================
        hint = Text("약을 먹으면 더 빨리 나을 것 같습니다.", font_size=30, color=GRAY_A, weight=BOLD).move_to(DOWN * 0.4)
        play_at(15.85, title.animate.scale(0.85).to_edge(UP, buff=0.6), FadeIn(hint, shift=UP * 0.1), run_time=0.5)  # chunk5

        g_treat = icon("users", BLUE_B, height=1.2).move_to(LEFT * 3.4 + UP * 0.35)
        t_lbl = Text("약 복용", font_size=26, color=BLUE_B, weight=BOLD).next_to(g_treat, DOWN, buff=0.25)
        g_ctrl = icon("users", RED_B, height=1.2).move_to(RIGHT * 3.4 + UP * 0.35)
        c_lbl = Text("약 미복용", font_size=26, color=RED_B, weight=BOLD).next_to(g_ctrl, DOWN, buff=0.25)
        # 비교 대상 = 회복 기간, 그 '차이'를 본다
        metric = Text("회복 기간 차이?", font_size=30, color=YELLOW, weight=BOLD).move_to(DOWN * 1.0)
        diff_arrow = DoubleArrow(LEFT * 1.7 + DOWN * 1.65, RIGHT * 1.7 + DOWN * 1.65, color=YELLOW,
                                 stroke_width=5, tip_length=0.22, buff=0.1)

        play_at(18.70, FadeOut(hint),
                FadeIn(g_treat, t_lbl), FadeIn(g_ctrl, c_lbl), run_time=0.5)   # chunk6
        play_at(21.50, FadeIn(metric, shift=UP * 0.08), GrowFromCenter(diff_arrow), run_time=0.5)
        beatC = VGroup(g_treat, t_lbl, g_ctrl, c_lbl, metric, diff_arrow)

        # ============================================================
        # Beat D — 전체 환자 막대: 복용 5.6 > 미복용 4.7 (chunk6~8, 24.71~41.89)
        # ============================================================
        c_title = Text("전체 환자", font_size=34, color=GRAY_A, weight=BOLD).to_edge(UP, buff=0.6)
        c_x0 = -1.6
        c_treat = bar_row("약 복용", 5.6, BLUE, y=0.8, x0=c_x0, fs=26)
        c_ctrl = bar_row("약 미복용", 4.7, RED, y=-0.5, x0=c_x0, fs=26)
        harm = Text("약 먹은 쪽이 더 오래 아팠다?", font_size=32, color=RED_B, weight=BOLD).move_to(DOWN * 2.0)
        harm_face = icon("mood-confuzed", RED_B, height=0.7).next_to(harm, LEFT, buff=0.25)

        play_at(24.70, FadeOut(beatC), ReplacementTransform(title, c_title), run_time=0.5)  # chunk7
        play_at(26.60, GrowFromEdge(c_treat[1], LEFT), FadeIn(c_treat[0], c_treat[2]), run_time=0.6)  # chunk8
        play_at(30.20, GrowFromEdge(c_ctrl[1], LEFT), FadeIn(c_ctrl[0], c_ctrl[2]), run_time=0.6)
        play_at(34.90, FadeIn(harm, shift=UP * 0.1), FadeIn(harm_face, shift=UP * 0.1), run_time=0.5)  # chunk9

        # ============================================================
        # Beat E — 함정 + 중증/경증으로 나눠서 (chunk9~10, 41.89~51.08)
        # ============================================================
        trap = Text("정말 그럴까요?", font_size=28, color=YELLOW, weight=BOLD).move_to(DOWN * 2.0)
        play_at(41.72, FadeOut(harm, harm_face), FadeIn(trap, shift=UP * 0.08), run_time=0.45)  # chunk10

        split_title = Text("중증 / 경증으로 나눠 보면?", font_size=34, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.55)
        # 전체 막대를 정리하고(겹쳐서) 그룹 레이아웃으로 전환 — 블랙아웃 없음
        play_at(45.43, FadeOut(c_treat, c_ctrl, trap),
                ReplacementTransform(c_title, split_title), run_time=0.5)      # chunk11

        # ============================================================
        # Beat F — 중증(7/8), 경증(2/3): 각 그룹에서 복용이 더 짧다 (chunk11~13, 51.08~80.39)
        # ============================================================
        d_x0 = -1.9
        sev_head = Text("중증", font_size=28, color=BLUE_D, weight=BOLD).move_to(LEFT * 5.0 + UP * 1.55)
        sev_t = bar_row("복용", 7, BLUE, y=1.95, x0=d_x0, fs=22)
        sev_c = bar_row("미복용", 8, RED, y=1.15, x0=d_x0, fs=22)
        mild_head = Text("경증", font_size=28, color=PINK, weight=BOLD).move_to(LEFT * 5.0 + DOWN * 1.15)
        mild_t = bar_row("복용", 2, BLUE, y=-0.75, x0=d_x0, fs=22)
        mild_c = bar_row("미복용", 3, RED, y=-1.55, x0=d_x0, fs=22)
        sev_ok = Text("약이 1일 단축 ✓", font_size=24, color=GREEN_B, weight=BOLD).next_to(sev_c, RIGHT, buff=0.5)
        mild_ok = Text("약이 1일 단축 ✓", font_size=24, color=GREEN_B, weight=BOLD).next_to(mild_c, RIGHT, buff=0.5)

        # chunk12 중증
        play_at(49.40, FadeIn(sev_head), GrowFromEdge(sev_t[1], LEFT), FadeIn(sev_t[0], sev_t[2]), run_time=0.55)
        play_at(52.80, GrowFromEdge(sev_c[1], LEFT), FadeIn(sev_c[0], sev_c[2]), run_time=0.55)
        play_at(55.80, FadeIn(sev_ok, shift=LEFT * 0.1), run_time=0.4)
        # chunk13 경증
        play_at(60.30, FadeIn(mild_head), GrowFromEdge(mild_t[1], LEFT), FadeIn(mild_t[0], mild_t[2]), run_time=0.55)
        play_at(63.60, GrowFromEdge(mild_c[1], LEFT), FadeIn(mild_c[0], mild_c[2]), run_time=0.55)
        play_at(66.60, FadeIn(mild_ok, shift=LEFT * 0.1), run_time=0.4)
        # chunk14 — 그룹 안에선 약이 분명히 좋다
        both_ok = Text("그룹 안에서는 약이 분명히 좋다 ✓", font_size=28, color=GREEN_B, weight=BOLD).to_edge(DOWN, buff=0.45)
        play_at(71.70, FadeIn(both_ok, shift=UP * 0.1), run_time=0.5)

        # ============================================================
        # Beat G — 역전: 그룹(복용 짧음) → 전체(복용 김)로 막대가 직접 뒤집힌다 (chunk14, 80.39~86.52)
        # ============================================================
        rev_title = Text("그런데 전체로 합치면…", font_size=34, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.55)
        ov_x0 = -1.6
        ov_treat = make_bar(5.6, BLUE, y=0.7, x0=ov_x0)
        ov_ctrl = make_bar(4.7, RED, y=-0.6, x0=ov_x0)
        ov_t_lbl = Text("약 복용", font_size=26, color=BLUE_B, weight=BOLD)
        ov_t_lbl.move_to([ov_x0 - 0.3 - ov_t_lbl.width / 2, 0.7, 0])
        ov_c_lbl = Text("약 미복용", font_size=26, color=RED_B, weight=BOLD)
        ov_c_lbl.move_to([ov_x0 - 0.3 - ov_c_lbl.width / 2, -0.6, 0])
        ov_t_val = Text("5.6일", font_size=28, color=BLUE_B, weight=BOLD).next_to(ov_treat, RIGHT, buff=0.18)
        ov_c_val = Text("4.7일", font_size=28, color=RED_B, weight=BOLD).next_to(ov_ctrl, RIGHT, buff=0.18)
        flip = Text("약 복용이 오히려 해롭습니다 ✗", font_size=30, color=RED_B, weight=BOLD).to_edge(DOWN, buff=0.5)

        # 두 복용(파랑) 막대가 하나의 긴 파랑 막대로, 두 미복용(빨강)이 짧은 빨강으로 합쳐진다
        play_at(77.90,
                FadeOut(sev_head, mild_head, sev_ok, mild_ok, both_ok,
                        sev_t[0], sev_t[2], sev_c[0], sev_c[2], mild_t[0], mild_t[2], mild_c[0], mild_c[2]),
                ReplacementTransform(split_title, rev_title), run_time=0.45)   # chunk15
        play_at(78.90,
                ReplacementTransform(VGroup(sev_t[1], mild_t[1]), ov_treat),
                ReplacementTransform(VGroup(sev_c[1], mild_c[1]), ov_ctrl),
                FadeIn(ov_t_lbl, ov_c_lbl, ov_t_val, ov_c_val), run_time=1.3)
        play_at(81.10, FadeIn(flip, shift=UP * 0.1), run_time=0.5)

        # ============================================================
        # Beat H — 왜? → IPW (영문 병기) (chunk16~17)
        # ============================================================
        why = Text("왜 이런 일이 벌어질까요?", font_size=36, color=YELLOW, weight=BOLD).move_to(DOWN * 2.6)
        play_at(83.50, FadeIn(why, scale=1.1), run_time=0.4)                   # chunk16

        ipw = Text("IPW", font_size=96, color=ORANGE, weight=BOLD)
        ipw_kr = Text("역확률 가중치", font_size=40, color=WHITE, weight=BOLD)
        ipw_en = Text("Inverse Probability Weighting", font_size=28, color=GRAY_B, weight=BOLD)
        ipw_group = VGroup(ipw, ipw_kr, ipw_en).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        play_at(85.40,
                FadeOut(rev_title, ov_treat, ov_ctrl, ov_t_lbl, ov_c_lbl, ov_t_val, ov_c_val, flip, why),
                run_time=0.35)                                                # chunk17
        play_at(85.85, Write(ipw), run_time=0.6)
        play_at(87.10, FadeIn(ipw_kr, shift=UP * 0.1), run_time=0.4)
        play_at(88.00, FadeIn(ipw_en, shift=UP * 0.1), run_time=0.4)

        go_to(91.30)
