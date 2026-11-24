from manim import Create, DOWN, FadeIn, FadeOut, TransformFromCopy, VGroup

from videos.r_learner.visuals import (
    LearnerScene, MUTED, OUTCOME, at, label, math, outcome_ruler, store_title,
)


class Question(LearnerScene):
    script = "01_question"
    preview_durations = (9.3, 7.3, 9.0)

    def explain(self):
        small = VGroup(math("48", size=115, color=OUTCOME), label("작은 매장", 35)).arrange(DOWN, buff=0.23)
        large = VGroup(math("80", size=115, color=OUTCOME), label("큰 매장", 35)).arrange(DOWN, buff=0.23)
        small.move_to(at(-2.8, 0.24))
        large.move_to(at(2.8, 0.24))
        context = label("쿠폰을 받은 매장의 주문량", size=29, color=MUTED).move_to(at(0.0, 2.16))
        question = label("쿠폰 효과는 어디가 더 클까?", size=40).move_to(at(0.0, -1.70))
        baseline_orders = label("평소 주문량", 29, MUTED).move_to(at(-1.65, -1.73))
        coupon_chance = label("쿠폰 지급 확률", 29, MUTED).move_to(at(1.65, -1.73))
        ruler = outcome_ruler()
        title = store_title()

        with self.clock.beat() as beat:
            self.play(FadeIn(context), run_time=0.55)
            self.wait(beat * 0.20)
            self.play(FadeIn(small, shift=DOWN * 0.12), run_time=0.65)
            self.wait(beat * 0.15)
            self.play(FadeIn(large, shift=DOWN * 0.12), run_time=0.65)
            self.wait(beat * 0.13)
            self.play(FadeIn(question), run_time=0.55)

        with self.clock.beat() as beat:
            self.play(FadeOut(question), FadeIn(baseline_orders), run_time=0.65)
            self.wait(beat * 0.35)
            self.play(FadeIn(coupon_chance), run_time=0.62)

        with self.clock.beat() as beat:
            self.play(
                FadeOut(small), FadeOut(context), FadeOut(large[1]),
                FadeOut(baseline_orders), FadeOut(coupon_chance),
                Create(ruler.baseline), FadeIn(ruler.title), FadeIn(title), run_time=0.88,
            )
            self.play(
                TransformFromCopy(large[0], ruler.actual[1]), FadeOut(large[0]),
                FadeIn(ruler.actual[0]), FadeIn(ruler.actual[2]), run_time=0.92,
            )
            self.wait(beat * 0.28)
            self.play(FadeIn(ruler.expected), run_time=0.67)
