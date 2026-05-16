import json
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *


TOPIC_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]

ACCENT = YELLOW_E
WEIGHTED = TEAL_C
UNWEIGHTED = ORANGE
POINT_COLOR = BLUE_D
SOFT = GREY_B


def load_scene_timing_durations(scene_basename: str) -> list[float]:
    payload = json.loads((TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json").read_text())
    return [float(chunk["duration"]) for chunk in payload["chunks"]]


def load_grouped_regression_data():
    wage = (
        pd.read_csv(REPO_ROOT / "book" / "regression" / "data" / "wage.csv")
        .dropna(subset=["wage", "hours", "educ", "IQ", "lhwage"])
        .assign(hwage=lambda d: d["wage"] / d["hours"])
        .copy()
    )
    sample = wage.sort_values(["educ", "IQ"]).groupby("educ", group_keys=False).head(12)
    grouped = wage.groupby("educ", as_index=False).agg(lhwage=("lhwage", "mean"), count=("lhwage", "size"))
    individual = np.polyfit(sample["educ"], sample["lhwage"], 1)
    weighted = np.polyfit(grouped["educ"], grouped["lhwage"], 1, w=grouped["count"])
    unweighted = np.polyfit(grouped["educ"], grouped["lhwage"], 1)
    return sample, grouped, individual, weighted, unweighted


def make_line(axes: Axes, slope: float, intercept: float, color: str):
    x0, x1 = axes.x_range[0], axes.x_range[1]
    return Line(
        axes.c2p(x0, slope * x0 + intercept),
        axes.c2p(x1, slope * x1 + intercept),
        color=color,
        stroke_width=5,
    )


class Scene01_GroupedRegressionWeights(Scene):
    """
    Scene 01: Grouped Regression Needs Weights

    Core Claim:
    집계 데이터에서도 집단 평균과 집단 크기가 있으면 회귀의 핵심 구조를 복원할 수 있고,
    이때는 가중치가 필수다.

    Expected Misconception:
    그룹화된 점을 모두 같은 무게로 두어도 회귀선이 비슷할 것이라고 느끼기 쉽다.

    Visual Pivot:
    개별자료 산점도가 교육연수별 큰 버블로 압축되고,
    마지막에 가중 선과 비가중 선의 기울기 차이가 한 화면에서 갈라진다.

    Notebook Reference:
    book/regression/06-Grouped-and-Dummy-Regression_minimal_ko.ipynb
    - Cell 0: grouped regression 도입
    - Cell 2: wage.csv 범위
    - Cell 4-6: grouped regression, weighted vs unweighted 비교

    Script Reference:
    src/scripts/01_grouped_regression_weights.txt

    3Blue1Brown Reference:
    3b1b/_2020/covid.py - IntroQuestion
    Reason:
    한 화면의 비교 구조를 점진적으로 쌓고 마지막 대비를 크게 남기는 리듬을 참고했다.

    Script-to-Beat Mapping:
    1. chunk 1-2: grouped regression과 데이터 범위 도입
    2. chunk 3-4: 개별자료와 그룹화된 자료의 대응
    3. chunk 5-7: 같은 점이 아니라는 설명과 큰 집단 강조
    4. chunk 8-10: 가중 선과 비가중 선 비교
    5. chunk 11: 결론 정리
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("01_grouped_regression_weights")
        sample, grouped, individual_fit, weighted_fit, unweighted_fit = load_grouped_regression_data()

        axes = Axes(
            x_range=[8, 18, 2],
            y_range=[0.5, 2.0, 0.25],
            x_length=8.4,
            y_length=4.6,
            axis_config={"include_numbers": False, "stroke_width": 2.4, "color": GREY_C},
        )
        axes.move_to(DOWN * 0.45)
        x_label = Text("교육연수", font_size=24, color=SOFT).next_to(axes.x_axis, DOWN, buff=0.28)
        y_label = Text("로그 시간당 임금", font_size=24, color=SOFT).rotate(PI / 2).next_to(axes.y_axis, LEFT, buff=0.28)
        title = Text("그룹화 회귀에는 가중치가 필요하다", font_size=34, weight=BOLD, color=ACCENT)
        title.to_edge(UP)

        intro = Text("집단 평균 + 집단 크기", font_size=28, color=ACCENT)
        intro.next_to(title, DOWN, buff=0.25)
        scope = Text("wage.csv", font_size=28, weight=BOLD, color=WHITE)
        scope.next_to(intro, DOWN, buff=0.2)

        dots = VGroup(
            *[
                Dot(axes.c2p(row.educ, row.lhwage), radius=0.045, color=POINT_COLOR, fill_opacity=0.45, stroke_opacity=0.45)
                for row in sample.itertuples()
            ]
        )
        individual_line = make_line(axes, float(individual_fit[0]), float(individual_fit[1]), color=WHITE)

        bubble_mobs = VGroup()
        for row in grouped.itertuples():
            bubble = Circle(radius=0.12 + 0.004 * row.count, color=WEIGHTED, stroke_width=3)
            bubble.set_fill(WEIGHTED, opacity=0.16)
            bubble.move_to(axes.c2p(row.educ, row.lhwage))
            bubble_mobs.add(bubble)

        weighted_line = make_line(axes, float(weighted_fit[0]), float(weighted_fit[1]), WEIGHTED)
        unweighted_line = make_line(axes, float(unweighted_fit[0]), float(unweighted_fit[1]), UNWEIGHTED)

        big_label = Text("큰 집단 = 더 안정적", font_size=26, color=WEIGHTED, weight=BOLD)
        big_label.move_to(RIGHT * 3.0 + UP * 2.3)
        equal_weight = Text("같은 무게로 두면 안 된다", font_size=26, color=UNWEIGHTED, weight=BOLD)
        equal_weight.move_to(RIGHT * 2.6 + UP * 2.3)

        legend = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.7, color=WEIGHTED, stroke_width=5), Text("가중 선", font_size=22)).arrange(RIGHT, buff=0.2),
            VGroup(Line(ORIGIN, RIGHT * 0.7, color=UNWEIGHTED, stroke_width=5), Text("비가중 선", font_size=22)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR).shift(DOWN * 0.6 + LEFT * 0.1)

        close_text = Text("mean과 count를 함께 주면 된다", font_size=30, weight=BOLD, color=ACCENT)
        close_text.move_to(UP * 0.35)
        close_sub = Text("weighted regression keeps the slope honest", font_size=22, color=SOFT)
        close_sub.next_to(close_text, DOWN, buff=0.25)

        # Beat 1
        # 남는 요소: 제목
        # 새로 등장: 제목, 범위 문구
        # 비워 두는 영역: 중앙 전체
        # 핵심 시선 대상: 집단 평균 + 집단 크기 문구
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        self.play(FadeIn(intro, shift=UP * 0.12), run_time=0.7)
        self.wait(max(0.2, durations[0] - 1.5))
        self.play(FadeIn(scope, shift=UP * 0.1), run_time=0.7)
        self.wait(max(0.2, durations[1] - 0.7))

        # Beat 2
        # 남는 요소: 제목, 축
        # 새로 등장: 개별자료 점, 개별자료 회귀선, 그룹 버블
        # 비워 두는 영역: 우상단 일부
        # 핵심 시선 대상: 개별자료 산점도
        self.play(
            FadeOut(intro),
            FadeOut(scope),
            Create(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(dots, lag_ratio=0.02),
            run_time=1.4,
        )
        self.play(Create(individual_line), run_time=1.0)
        self.wait(max(0.2, durations[2] - 2.4))
        self.play(ReplacementTransform(dots.copy(), bubble_mobs), run_time=1.2)
        self.wait(max(0.2, durations[3] - 1.2))

        # Beat 3
        # 남는 요소: 제목, 축, 버블
        # 새로 등장: 큰 집단 강조 문구
        # 비워 두는 영역: 좌상단
        # 핵심 시선 대상: 버블 크기 차이
        self.play(FadeOut(dots), FadeOut(individual_line), run_time=0.7)
        self.wait(max(0.2, durations[4] - 0.7))
        biggest = bubble_mobs[grouped["count"].idxmax()]
        self.play(Indicate(biggest, color=WEIGHTED), FadeIn(big_label, shift=UP * 0.1), run_time=1.0)
        self.wait(max(0.2, durations[5] - 1.0))
        self.play(Circumscribe(biggest, color=WEIGHTED), run_time=0.9)
        self.wait(max(0.2, durations[6] - 0.9))

        # Beat 4
        # 남는 요소: 제목, 축, 버블
        # 새로 등장: 가중 선, 비가중 선, 범례
        # 비워 두는 영역: 좌하단 일부
        # 핵심 시선 대상: 두 선의 기울기 차이
        self.play(FadeOut(big_label), Create(weighted_line), run_time=1.0)
        self.wait(max(0.2, durations[7] - 1.0))
        self.play(Create(unweighted_line), FadeIn(equal_weight, shift=UP * 0.1), run_time=1.0)
        self.wait(max(0.2, durations[8] - 1.0))
        self.play(FadeIn(legend, shift=LEFT * 0.1), run_time=0.8)
        self.wait(max(0.2, durations[9] - 0.8))

        # Beat 5
        # 남는 요소: 제목
        # 새로 등장: 결론 문구
        # 비워 두는 영역: 하단 일부
        # 핵심 시선 대상: 결론 문구
        self.play(
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(bubble_mobs),
            FadeOut(weighted_line),
            FadeOut(unweighted_line),
            FadeOut(equal_weight),
            FadeOut(legend),
            FadeIn(close_text, shift=UP * 0.15),
            FadeIn(close_sub, shift=UP * 0.15),
            run_time=1.2,
        )
        self.wait(max(0.2, durations[10] - 1.2))
        self.wait(self.WAIT_TAIL)
