from manim import *

from videos.fuzzy_rdd.shared.common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
    YELLOW_MAIN,
)
from videos.fuzzy_rdd.shared.recap import show_cutoff_comparison


class Scene01RecapHook(Scene):
    """
    Scene 01: recap_hook (English port of videos/fuzzy_rdd/ko/scenes/scene_01_recap_hook.py)
    스크립트: narration/01_recap_hook.txt
    타이밍: build/audio/01_recap_hook.timings.json (총 51.51s, 9 chunks)

    한국어 버전과 문단 구조(9 chunks)가 1:1로 대응하고, 모든 wait() 체크포인트가
    청크 경계와 정확히 일치하므로, run_time들은 그대로 두고 wait() 인자만
    영어 오디오의 새 청크 경계 시간으로 교체했다. 시각 구조·색·레이아웃은 원본과 동일.

    Beat1 chunk1-2 ( 0.00~14.54s)  Sharp RDD recap: headline → example + step function graph
    Beat2 chunk3   (14.54~16.90s)  "reality isn't this clean" headline
    Beat3 chunk4-5 (16.90~29.40s)  contrasting real cases: 371(above cutoff, no scholarship) vs 369(below, got it)
    Beat4 chunk6-7 (29.40~40.36s)  generalize → Fuzzy RDD definition (2 lines + name)
    Beat5 chunk8-9 (40.36~51.51s)  Fuzzy RDD graph (partial jump) → closing question (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1-2: 0~14.54) ──────────────────────────
        recap_title = VGroup(
            Text("Recap: Last Video", font=FONT, font_size=22, color=GRAY_MID),
            Text("Sharp RDD", font=FONT, font_size=46, color=TEAL_MAIN),
            Text("Cutoff crossed → 100% treatment", font=FONT, font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.6)

        self.play(FadeIn(recap_title, shift=UP * 0.2), run_time=0.7)
        self.wait(5.387 - 0.7)  # chunk1 end

        # chunk2: example (score >= / < 370) + Sharp RDD step function graph
        sharp_label = Text("Sharp RDD", font=FONT, font_size=30, color=TEAL_MAIN)
        example_label = Text("(Example)", font=FONT, font_size=20, color=GRAY_MID)
        example_lines = VGroup(
            Text("Score >= 370 -> gets scholarship", font=FONT, font_size=24, color=TEAL_MAIN),
            Text("Score < 370 -> gets nothing", font=FONT, font_size=24, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        example_group = VGroup(sharp_label, example_label, example_lines).arrange(DOWN, buff=0.25)

        step_graph = self._make_step_graph()
        content2 = VGroup(example_group, step_graph).arrange(DOWN, buff=0.9).move_to(ORIGIN)

        self.play(FadeOut(recap_title, run_time=0.5), FadeIn(content2, shift=UP * 0.15, run_time=0.8))
        self.wait(14.5357 - 5.387 - 0.8)  # chunk2 end

        self.play(FadeOut(content2), run_time=0.5)

        # ── Beat 2 (chunk3: 14.54~16.90) ────────────────────────
        headline2 = Text(
            "But reality isn't this clean", font=FONT, font_size=30, color=WHITE,
        ).move_to(ORIGIN)

        self.play(FadeIn(headline2, shift=UP * 0.2), run_time=0.6)
        self.wait(16.9041 - 14.5357 - 0.5 - 0.6)  # chunk3 end

        # ── Beat 3 (chunk4-5: 16.90~29.40) ──────────────────────
        top_label = Text("Real-World Cases", font=FONT, font_size=22, color=GRAY_MID).to_edge(UP, buff=1.3)

        left_card = self._make_case_card(
            score="371", status="Above cutoff", status_color=TEAL_MAIN,
            result="No scholarship", result_color=RED_MAIN, reason="Missed deadline",
        ).move_to(LEFT * 3.4 + DOWN * 0.25)
        right_card = self._make_case_card(
            score="369", status="Below cutoff", status_color=GOLD_MAIN,
            result="Got scholarship", result_color=GREEN_MAIN, reason="Secondary review",
        ).move_to(RIGHT * 3.4 + DOWN * 0.25)

        self.play(
            Transform(headline2, top_label),
            FadeIn(left_card, shift=RIGHT * 0.2),
            run_time=0.7,
        )
        self.wait(22.5698 - 16.9041 - 0.7)  # chunk4 end

        self.play(FadeIn(right_card, shift=LEFT * 0.2), run_time=0.6)
        self.wait(29.3965 - 22.5698 - 0.6)  # chunk5 end

        self.play(FadeOut(VGroup(headline2, left_card, right_card)), run_time=0.5)

        # ── Beat 4 (chunk6-7: 29.40~40.36) ──────────────────────
        headline3 = VGroup(
            Text("Crossing the cutoff doesn't mean everyone gets treated,", font=FONT, font_size=24, color=WHITE),
            Text("and falling short doesn't mean no one does", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeIn(headline3, shift=UP * 0.2), run_time=0.7)
        self.wait(33.7154 - 29.3965 - 0.5 - 0.7)  # chunk6 end

        fuzzy_def = VGroup(
            Text("When the cutoff has a discontinuous effect on treatment", font=FONT, font_size=22, color=WHITE),
            Text("probability without fully determining it", font=FONT, font_size=22, color=WHITE),
            Text("Fuzzy RDD", font=FONT, font_size=30, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeOut(headline3, run_time=0.4), FadeIn(fuzzy_def, shift=UP * 0.2, run_time=0.7))
        self.wait(40.3563 - 33.7154 - 0.7)  # chunk7 end

        # Beat 5 compares the two probability jumps on the same score axis.
        fuzzy_graph_group = show_cutoff_comparison(
            self, fuzzy_def, score_label="Score", probability_label="Treatment probability",
            duration=46.9972 - 40.3563,
        )

        closing = Text(
            "How do we handle Fuzzy RDD?", font=FONT, font_size=34, color=WHITE,
        ).move_to(ORIGIN)

        self.play(FadeOut(fuzzy_graph_group), FadeIn(closing, shift=UP * 0.2), run_time=0.7)
        # WAIT_TAIL = (51.513 + 0.5) - (46.997 + 0.7) = 4.316
        self.wait(4.316)

    # ── 헬퍼 (원본과 동일 구조, 라벨만 영어) ─────────────────────

    def _make_case_card(self, score, status, status_color, result, result_color, reason) -> VGroup:
        score_t = Text(score, font=FONT, font_size=40, color=WHITE)

        status_t = Text(status, font=FONT, font_size=19, color=status_color)
        status_box = SurroundingRectangle(
            status_t, color=status_color, buff=0.12, corner_radius=0.08, stroke_width=1.5,
        )
        status_g = VGroup(status_box, status_t)

        result_t = Text(result, font=FONT, font_size=24, color=WHITE)
        result_box = SurroundingRectangle(
            result_t, color=result_color, fill_color=result_color, fill_opacity=0.9,
            buff=0.14, corner_radius=0.1, stroke_width=0,
        )
        result_g = VGroup(result_box, result_t)

        reason_t = Text(reason, font=FONT, font_size=16, color=GRAY_MID)

        inner = VGroup(score_t, status_g, result_g, reason_t).arrange(DOWN, buff=0.24)
        frame = RoundedRectangle(
            width=3.8, height=3.2, corner_radius=0.15, color=result_color, stroke_width=2.5,
        )
        inner.move_to(frame.get_center())
        return VGroup(frame, inner)

    def _make_step_graph(self) -> VGroup:
        axes = Axes(
            x_range=[0, 10, 10],
            y_range=[0, 1.2, 1],
            x_length=3.8,
            y_length=2.0,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_tip": False},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": [0, 1]},
            tips=False,
        )
        for label in axes.y_axis.numbers:
            label.set(font_size=14)

        c_x = 5
        cutoff_line = DashedLine(
            axes.c2p(c_x, 0), axes.c2p(c_x, 1.15),
            color=YELLOW_MAIN, dash_length=0.06, stroke_width=2,
        )
        left_line = axes.plot(lambda x: 0, x_range=[0, c_x], color=GOLD_MAIN, stroke_width=5)
        right_line = axes.plot(lambda x: 1, x_range=[c_x, 10], color=TEAL_MAIN, stroke_width=5)
        open_dot = Circle(radius=0.06, color=GOLD_MAIN, fill_opacity=0, stroke_width=2.5).move_to(axes.c2p(c_x, 0))
        closed_dot = Dot(axes.c2p(c_x, 1), radius=0.06, color=TEAL_MAIN)
        c_label = Text("c", font=FONT, font_size=18, color=YELLOW_MAIN).next_to(cutoff_line, DOWN, buff=0.1)

        x_lbl = Text("Score (X)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_right(), RIGHT, buff=0.12)
        y_lbl = Text("Treatment (D)", font=FONT, font_size=14, color=GRAY_MID)
        y_lbl.next_to(axes.y_axis.get_top(), UP, buff=0.1)

        return VGroup(axes, cutoff_line, left_line, right_line, open_dot, closed_dot, c_label, x_lbl, y_lbl)
