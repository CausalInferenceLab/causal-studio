from manim import Create, Dot, DOWN, FadeIn, FadeOut, Line, RIGHT, VGroup

from videos.r_learner.shared.common import (
    BACKGROUND, EXAMPLE, GUIDE, LARGE, LARGE_FIT, LearnerScene, MUTED, OUTCOME, ResidualPlot,
    SMALL, SMALL_FIT, TREATMENT, at, label, large_summary, math,
)


class Effects(LearnerScene):
    script = "04_effects"
    preview_durations = (10.0, 10.0, 10.4)

    def explain(self):
        plot = ResidualPlot()
        previous_summary = large_summary()
        sample = plot.dots([EXAMPLE], OUTCOME)
        points = plot.dots([point for point in LARGE if point != EXAMPLE])
        small_points = plot.dots(SMALL, SMALL_FIT, squares=True)
        large_line = plot.fit(16)
        small_line = plot.fit(8, SMALL_FIT, domain=(-0.82, 0.92))
        self.add(plot.frame, large_line, points, sample, previous_summary)

        x = 4.85
        small_label = VGroup(label("작은 매장", 31), math("8", size=64, color=SMALL_FIT)).arrange(DOWN, buff=0.13)
        large_label = VGroup(label("큰 매장", 31), math("16", size=64, color=LARGE_FIT)).arrange(DOWN, buff=0.13)
        comparison = VGroup(small_label, large_label).arrange(RIGHT, buff=0.60).move_to(at(x, 0.94))
        units = label("쿠폰 효과 · 주문 건수", 26, MUTED).move_to(at(x, -0.23))
        caption = VGroup(label("효과 함수", 32), math(r"\tau(X)", size=55)).arrange(RIGHT, buff=0.24).move_to(at(x, 2.13))

        train = VGroup(*(Dot(radius=0.075, color=MUTED) for _ in range(4))).arrange(RIGHT, buff=0.23).move_to(at(4.3, 0.43))
        withheld = Dot(at(5.77, 0.43), radius=0.093, color=TREATMENT).set_fill(BACKGROUND, opacity=1).set_stroke(TREATMENT, 2.5)
        divider = Line(at(5.18, 0.73), at(5.18, 0.12), color=GUIDE, stroke_width=1.8)
        cross_labels = VGroup(
            label("학습에 사용", 24, MUTED).next_to(train, DOWN, buff=0.23),
            label("잔차 계산", 24, TREATMENT).next_to(withheld, DOWN, buff=0.23),
        )
        cross_title = label("교차 적합", 33).move_to(at(x, 1.19))
        crossfit = VGroup(train, withheld, divider, cross_labels, cross_title)

        treated = Dot(radius=0.087, color=TREATMENT)
        untreated = Dot(radius=0.087, color=TREATMENT).set_fill(BACKGROUND, opacity=1).set_stroke(TREATMENT, 2.1)
        overlap = VGroup(
            VGroup(treated, label("지급", 27)).arrange(RIGHT, buff=0.13),
            VGroup(untreated, label("미지급", 27)).arrange(RIGHT, buff=0.13),
        ).arrange(RIGHT, buff=0.40).move_to(at(x, 0.38))
        same_x = label("같은 특성에서 비교", 33).move_to(at(x, 1.25))
        final_title = label("R-learner", 40).move_to(at(x, 2.17))

        with self.clock.beat() as beat:
            self.play(FadeIn(small_points), Create(small_line), run_time=1.20)
            self.wait(beat * 0.16)
            self.play(FadeOut(previous_summary), FadeIn(comparison), FadeIn(units), run_time=0.83)

        with self.clock.beat() as beat:
            self.play(FadeOut(comparison), FadeOut(units), FadeIn(caption), run_time=0.79)
            self.wait(beat * 0.32)
            self.play(FadeIn(train), FadeIn(cross_title), run_time=0.74)
            self.play(Create(divider), FadeIn(withheld), FadeIn(cross_labels), run_time=0.77)

        with self.clock.beat() as beat:
            self.play(FadeOut(crossfit), FadeOut(caption), FadeIn(final_title), FadeIn(same_x), run_time=0.77)
            self.wait(beat * 0.26)
            self.play(FadeIn(overlap), run_time=0.73)
            self.wait(beat * 0.23)
            comparison.move_to(at(x, -0.65))
            units.move_to(at(x, -1.78))
            self.play(FadeIn(comparison), FadeIn(units), run_time=0.79)
