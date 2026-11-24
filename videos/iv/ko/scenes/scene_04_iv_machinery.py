from manim import *

from videos.iv.shared.common import (
    ACCENT,
    COIN_COLOR,
    COMPLIER,
    CONTROL_COLOR,
    INSTRUMENT,
    SOFT,
    TREAT_COLOR,
    load_scene_timing_durations,
)


class Scene04_IvMachinery(Scene):
    """
    Scene 04: 와알드 추정량 = ITT / 순응자 비율.

    Core Claim:
    LATE를 숫자로 구하는 식은 ITT(배정 결과 차이)를 순응자 비율로
    나눈 비율이다. 분자는 동전이 만든 총 효과, 분모는 동전이 실제로
    움직인 비율, 둘을 나누면 "한 명의 순응자에게 처치가 만든 효과"가 된다.

    Visual Pivot:
    분자와 분모가 처음에는 따로 등장해 의미가 명확히 분리된 뒤,
    마지막에 분수선 위/아래로 합쳐지며 한 식으로 수렴.

    Script: narration/04_iv_machinery.txt — 6 chunks, 79.51s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("04_iv_machinery", language="ko")
        # durations ≈ [7.42, 16.85, 18.12, 5.95, 14.57, 16.61]

        # Beat 1 (0~7.42s): "식은 간단하다" 인트로
        title = Text("LATE를 숫자로 구하기", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        intro = Text("식은 의외로 간단합니다", font_size=26, color=SOFT).move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(intro), run_time=1.2)
        self.wait(7.42 - 1.9)

        # Beat 2 (7.42~24.27s): 분자 — 배정별 평균 점수 차이
        # 라벨은 title 바로 아래에 두어 "이 차이" 위쪽 텍스트와 충돌 방지.
        numerator_label = Text("분자: 배정으로 만든 점수 차이", font_size=24, color=COIN_COLOR).next_to(title, DOWN, buff=0.4)
        score_z1 = Text("처치 배정\n평균 점수", font_size=20, color=TREAT_COLOR, line_spacing=0.9)
        score_z0 = Text("통제 배정\n평균 점수", font_size=20, color=CONTROL_COLOR, line_spacing=0.9)
        # 바 높이를 축소해 위쪽 라벨과 간격 확보.
        bar_z1 = Rectangle(width=0.8, height=1.7, color=TREAT_COLOR, fill_opacity=0.7, stroke_width=0)
        bar_z0 = Rectangle(width=0.8, height=1.3, color=CONTROL_COLOR, fill_opacity=0.7, stroke_width=0)
        bar_block_z1 = VGroup(bar_z1, score_z1).arrange(DOWN, buff=0.25)
        bar_block_z0 = VGroup(bar_z0, score_z0).arrange(DOWN, buff=0.25)
        # 바닥선 정렬로 바 차트 느낌, 위치는 좀 더 아래로 내려 vertical 여백 확보.
        bars = VGroup(bar_block_z1, bar_block_z0).arrange(RIGHT, buff=1.4, aligned_edge=DOWN).move_to(DOWN * 1.1)
        diff_brace = Brace(VGroup(bar_z1, bar_z0), direction=UP, buff=0.25, color=COIN_COLOR)
        diff_text = Text("이 차이", font_size=22, color=COIN_COLOR).next_to(diff_brace, UP, buff=0.2)

        self.play(FadeOut(intro), run_time=0.4)
        self.play(FadeIn(numerator_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(bars, shift=UP * 0.15), run_time=1.2)
        self.play(GrowFromCenter(diff_brace), FadeIn(diff_text, shift=DOWN * 0.1), run_time=1.0)
        self.wait(16.85 - 3.3)

        # Beat 3 (24.27~42.39s): 작게 나오는 이유 — 순응자만 움직임
        explain = Text("이 차이는 순응자만이 만든다", font_size=26, weight=BOLD, color=COMPLIER).move_to(DOWN * 2.5)
        complier_note = Text("(언제나 받음 / 절대 안 받음 학교는 동전에 무반응)", font_size=18, color=SOFT).next_to(explain, DOWN, buff=0.2)
        # 분자 차이를 살짝 줄여서 시각적으로 강조
        self.play(FadeIn(explain, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(complier_note, shift=UP * 0.05), run_time=0.7)
        # 박스로 분자 묶기 (buff 키워 내용 튀어나옴 방지)
        numer_box = SurroundingRectangle(VGroup(bars, diff_brace, diff_text), color=COIN_COLOR, buff=0.4)
        self.play(Create(numer_box), run_time=1.0)
        self.wait(18.12 - 2.7)

        # Beat 4 (42.39~48.34s): "그래서 비율로 나눠야 한다"
        divide_caption = Text("→ 순응자 비율로 나눠 환산한다", font_size=26, color=ACCENT).move_to(DOWN * 3.3)
        self.play(FadeOut(complier_note), run_time=0.3)
        self.play(FadeIn(divide_caption, shift=UP * 0.1), run_time=1.0)
        self.wait(5.95 - 1.3)

        # Beat 5 (48.34~62.91s): 분모 — 실제 사용 비율 차이 = 순응자 비율
        # 화면 정리 후 새 분모 시각화
        previous = VGroup(numerator_label, bars, diff_brace, diff_text,
                          explain, numer_box, divide_caption)
        self.play(FadeOut(previous), run_time=0.7)
        denom_label = Text("분모: 동전이 움직인 비율", font_size=24, color=INSTRUMENT).move_to(UP * 1.6)
        # 두 그룹: 처치 배정 중 실제 사용 비율 / 통제 배정 중 실제 사용 비율
        ratio_block_left = self._make_ratio_block("처치 배정 중\n실제 사용", filled=6, total=8, color=TREAT_COLOR)
        ratio_block_right = self._make_ratio_block("통제 배정 중\n실제 사용", filled=2, total=8, color=CONTROL_COLOR)
        ratios = VGroup(ratio_block_left, ratio_block_right).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.2)
        complier_pct = Text("≈ 순응자 비율 (6/8 − 2/8 = 50%)", font_size=22, color=COMPLIER).move_to(DOWN * 2.5)

        self.play(FadeIn(denom_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(ratios, shift=UP * 0.15), run_time=1.5)
        self.play(Write(complier_pct), run_time=1.4)
        self.wait(14.57 - 3.6)

        # Beat 6 (62.91~79.52s): 와알드 추정량 = 분자 / 분모
        self.play(FadeOut(VGroup(denom_label, ratios, complier_pct)), run_time=0.7)
        wald_title = Text("와알드 추정량 (Wald Estimator)", font_size=28, weight=BOLD, color=INSTRUMENT).to_edge(UP, buff=1.2)
        numer_line = Text("배정으로 만든 점수 차이", font_size=26, color=COIN_COLOR)
        bar = Line(LEFT * 3.2, RIGHT * 3.2, color=WHITE, stroke_width=3)
        denom_line = Text("순응자 비율", font_size=26, color=INSTRUMENT)
        fraction = VGroup(numer_line, bar, denom_line).arrange(DOWN, buff=0.25).move_to(ORIGIN + UP * 0.1)
        equals = Text("=  LATE", font_size=30, weight=BOLD, color=COMPLIER).next_to(fraction, DOWN, buff=0.5)
        meaning = Text("한 순응자에게 처치가 만든 효과", font_size=22, color=SOFT).next_to(equals, DOWN, buff=0.3)

        self.play(FadeIn(wald_title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(numer_line, shift=UP * 0.1), run_time=0.9)
        self.play(Create(bar), run_time=0.5)
        self.play(FadeIn(denom_line, shift=DOWN * 0.1), run_time=0.9)
        self.play(Write(equals), run_time=1.0)
        self.play(FadeIn(meaning, shift=UP * 0.05), run_time=0.9)
        self.wait(16.61 - 4.9)
        self.wait(self.WAIT_TAIL)

    @staticmethod
    def _make_ratio_block(title_text: str, filled: int, total: int, color: str) -> VGroup:
        title = Text(title_text, font_size=20, color=color, line_spacing=0.9)
        dots = VGroup()
        for i in range(total):
            d = Dot(radius=0.13, color=color if i < filled else GREY_D)
            if i >= filled:
                d.set_fill(opacity=0.3)
            dots.add(d)
        dots.arrange(RIGHT, buff=0.18)
        ratio_text = Text(f"{filled}/{total}", font_size=24, weight=BOLD, color=color)
        block = VGroup(title, dots, ratio_text).arrange(DOWN, buff=0.25)
        return block
