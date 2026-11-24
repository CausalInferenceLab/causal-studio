"""Sharp-to-fuzzy comparison on one probability axis."""

from manim import (
    BLACK, DOWN, LEFT, ORIGIN, RIGHT, UP, Axes, Circle, DashedLine, Dot,
    FadeIn, FadeOut, Line, Succession, Text, Transform, VGroup, Wait,
)

from videos.fuzzy_rdd.shared.common import FONT, GOLD_MAIN, GRAY_MID, TEAL_MAIN, WHITE, YELLOW_MAIN


def _probability_lines(axes, left_bounds, right_bounds):
    left_limit, right_limit = axes.c2p(370, left_bounds[1]), axes.c2p(370, right_bounds[0])
    left = Line(axes.c2p(340, left_bounds[0]), left_limit, color=GOLD_MAIN, stroke_width=6)
    right = Line(right_limit, axes.c2p(400, right_bounds[1]), color=TEAL_MAIN, stroke_width=6)
    gap = DashedLine(left_limit, right_limit, dash_length=0.065, color=YELLOW_MAIN, stroke_width=3)
    lower = Circle(radius=0.086, color=GOLD_MAIN, fill_color=BLACK, fill_opacity=1,
                   stroke_width=3).move_to(left_limit)
    upper = Dot(right_limit, radius=0.082, color=TEAL_MAIN)
    graph = VGroup(left, right, gap, lower, upper)
    labels = VGroup(
        Text(f"{left_bounds[1]:.0%}", font_size=31, color=GOLD_MAIN).next_to(lower, UP + LEFT, buff=0.17),
        Text(f"{right_bounds[0]:.0%}", font_size=31, color=TEAL_MAIN).next_to(upper, DOWN + RIGHT, buff=0.17),
    )
    return graph, labels


def show_cutoff_comparison(scene, definition, *, score_label, probability_label, duration):
    """Keep score and cutoff fixed while the treatment probabilities change."""
    axes = Axes(
        x_range=[340, 400, 15], y_range=[0, 1, 0.25], x_length=8.6, y_length=3.45,
        axis_config={"color": GRAY_MID, "stroke_width": 1.6, "include_ticks": False},
        tips=False,
    ).move_to(ORIGIN + DOWN * 0.35)
    guides = VGroup(*(
        Line(axes.c2p(340, p), axes.c2p(400, p), color=GRAY_MID,
             stroke_width=1.0, stroke_opacity=0.27)
        for p in (0.50, 1.0)
    ))
    cutoff = DashedLine(axes.c2p(370, 0), axes.c2p(370, 1), color=YELLOW_MAIN,
                        stroke_width=1.8, dash_length=0.087, stroke_opacity=0.42)
    score_ticks = VGroup(*(
        Text(str(score), font_size=23, color=YELLOW_MAIN if score == 370 else GRAY_MID)
        .next_to(axes.c2p(score, 0), DOWN, buff=0.24)
        for score in (340, 370, 400)
    ))
    probability_ticks = VGroup(
        Text("50%", font_size=22, color=GRAY_MID).next_to(axes.c2p(340, 0.5), LEFT, buff=0.19),
        Text("100%", font_size=22, color=GRAY_MID).next_to(axes.c2p(340, 1), LEFT, buff=0.19),
        Text("0%", font_size=22, color=GRAY_MID).next_to(axes.c2p(340, 0), LEFT, buff=0.19),
    )
    score = Text(score_label, font=FONT, font_size=26, color=GRAY_MID)
    score.next_to(axes.c2p(400, 0), RIGHT, buff=0.32)
    probability = Text(probability_label, font=FONT, font_size=25, color=GRAY_MID)
    probability.move_to(axes.c2p(340, 1) + UP * 0.39, aligned_edge=LEFT)
    fixed = VGroup(guides, axes, cutoff, score_ticks, probability_ticks, score, probability)
    sharp_title = Text("Sharp RDD", font=FONT, font_size=35, color=WHITE).move_to(UP * 2.75)
    fuzzy_title = Text("Fuzzy RDD", font=FONT, font_size=35, color=WHITE).move_to(sharp_title)
    plot, numbers = _probability_lines(axes, (0, 0), (1, 1))
    target, updated_numbers = _probability_lines(axes, (0.05, 0.15), (0.65, 0.85))

    # Adapted from the in-place plot update in 3Blue1Brown's TransitionToSkewDistribution.
    scene.play(FadeOut(definition), FadeIn(fixed), FadeIn(sharp_title),
               FadeIn(plot), FadeIn(numbers), run_time=0.8)
    scene.wait(0.9)
    scene.play(
        Transform(plot, target, run_time=1.45),
        Succession(
            FadeOut(VGroup(numbers, sharp_title), run_time=0.28),
            Wait(0.70),
            FadeIn(VGroup(updated_numbers, fuzzy_title), run_time=0.47),
        ),
    )
    scene.wait(duration - 3.15)
    return VGroup(fixed, plot, updated_numbers, fuzzy_title)
