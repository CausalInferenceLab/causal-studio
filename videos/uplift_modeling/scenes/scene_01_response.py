from manim import DOWN, FadeIn, FadeOut, ReplacementTransform

from videos.uplift_modeling.visuals import (
    AUDIENCES, MUTED, UpliftScene, at, cohort_cells, label, opening_comparison, title,
)


class Response(UpliftScene):
    script = "01_response"
    preview_durations = (7.5, 8.8, 7.6)

    def explain(self):
        blocks, header, relation = opening_comparison()
        left_waiting, right_waiting = (cohort_cells(audience, 0) for audience in AUDIENCES)
        question = title("쿠폰을 누구에게 보낼까?")
        unit = label("각 고객군 100명", 26, MUTED).move_to(at(0, -2.70))

        with self.clock.beat() as beat:
            self.play(FadeIn(question), run_time=0.70)
            self.wait(beat * 0.15)
            self.play(FadeIn(left_waiting, lag_ratio=0.02), FadeIn(blocks[0][2], shift=DOWN * 0.10), run_time=0.74)
            self.wait(beat * 0.14)
            self.play(FadeIn(right_waiting, lag_ratio=0.02), FadeIn(blocks[1][2], shift=DOWN * 0.10), FadeIn(unit), run_time=0.76)

        with self.clock.beat() as beat:
            self.play(FadeOut(question), FadeIn(header), run_time=0.50)
            self.wait(beat * 0.10)
            self.play(ReplacementTransform(left_waiting, blocks[0][0]), FadeIn(blocks[0][1]), run_time=1.13)
            self.wait(beat * 0.14)
            self.play(ReplacementTransform(right_waiting, blocks[1][0]), FadeIn(blocks[1][1]), run_time=1.13)

        with self.clock.beat() as beat:
            self.play(FadeIn(relation), run_time=0.57)
            self.wait(beat * 0.20)
            followup = label("쿠폰 없이도 살 사람은?", 33).move_to(at(0, -2.70))
            self.play(FadeOut(unit), FadeIn(followup), run_time=0.70)
