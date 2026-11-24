from manim import *

from videos.iv.shared.common import (
    ACCENT,
    ALWAYS_TAKER,
    COIN_COLOR,
    COMPLIER,
    CONTROL_COLOR,
    INSTRUMENT,
    NEVER_TAKER,
    TREAT_COLOR,
    load_scene_timing_durations,
)


class Scene03_ThreeTypes(Scene):
    """
    Scene 03: 비순응의 세 유형 + LATE.

    Core Claim:
    동전이 움직이는 사람은 순응자뿐이다.
    따라서 도구변수가 짚어 내는 효과는 전체 평균 처치 효과(ATE)가 아니라,
    순응자에 한정된 국소 평균 처치 효과(LATE)이다.

    Visual Pivot:
    동전이 처치/통제로 떨어지는 두 세계를 평행 트랙으로 보여줘서,
    같은 사람이 두 세계에서 어떻게 행동하는지를 한 번에 비교.

    Script: narration/03_three_types.txt — 6 chunks, 70.3s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("03_three_types", language="ko")
        # durations ≈ [8.02, 11.86, 13.01, 10.20, 16.06, 11.16]

        # Beat 1 (0~8.02s): 세 유형 소개
        title = Text("동전이 움직이는 세 유형", font_size=30, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.4)
        type_names = ["순응자", "언제나 받음", "절대 안 받음"]
        type_colors = [COMPLIER, ALWAYS_TAKER, NEVER_TAKER]
        cards = VGroup()
        for name, color in zip(type_names, type_colors):
            frame = RoundedRectangle(width=3.4, height=1.1, corner_radius=0.16,
                                       stroke_color=color, stroke_width=2.5)
            label = Text(name, font_size=24, weight=BOLD, color=color).move_to(frame.get_center())
            cards.add(VGroup(frame, label))
        cards.arrange(RIGHT, buff=0.4).move_to(UP * 0.6)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.25), run_time=1.6)
        self.wait(8.02 - 2.2)

        # Beat 2 (8.02~19.88s): 순응자 — 동전 따라감
        # 두 평행 트랙: 배정 처치 / 배정 통제, 각 트랙 위에 순응자가 어떻게 행동하는지
        # 작은 카드 상단 유지는 480p에서 가독성이 떨어지므로 FadeOut으로 정리한다.
        # 타입 식별은 dot 색 + 캡션이 담당한다.

        track_label_z1 = Text("배정 = 처치", font_size=20, color=COIN_COLOR)
        track_label_z0 = Text("배정 = 통제", font_size=20, color=COIN_COLOR)
        track_z1 = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY_C, stroke_width=2)
        track_z0 = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY_C, stroke_width=2)
        track1_block = VGroup(track_label_z1, track_z1).arrange(RIGHT, buff=0.4)
        track0_block = VGroup(track_label_z0, track_z0).arrange(RIGHT, buff=0.4)
        tracks = VGroup(track1_block, track0_block).arrange(DOWN, aligned_edge=LEFT, buff=1.0).move_to(DOWN * 0.6)

        complier_z1_dot = Dot(radius=0.18, color=TREAT_COLOR).move_to(track_z1.get_center())
        complier_z0_dot = Dot(radius=0.18, color=CONTROL_COLOR).move_to(track_z0.get_center())
        complier_caption = Text("순응자: 동전이 가리키는 대로 행동", font_size=24, color=COMPLIER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(cards), run_time=0.5)
        self.play(FadeIn(tracks, shift=DOWN * 0.1), run_time=0.8)
        self.play(FadeIn(complier_z1_dot, scale=0.7), FadeIn(complier_z0_dot, scale=0.7), run_time=0.8)
        self.play(Write(complier_caption), run_time=1.2)
        self.wait(11.86 - 3.3)

        # Beat 3 (19.88~32.89s): 언제나 받음 — 두 트랙 모두 처치색
        always_z1 = Dot(radius=0.18, color=ALWAYS_TAKER).move_to(track_z1.get_center() + RIGHT * 0.8)
        always_z0 = Dot(radius=0.18, color=ALWAYS_TAKER).move_to(track_z0.get_center() + RIGHT * 0.8)
        always_caption = Text("언제나 받음: 동전과 무관하게 처치", font_size=24, color=ALWAYS_TAKER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(complier_caption), run_time=0.4)
        self.play(FadeIn(always_z1, scale=0.7), FadeIn(always_z0, scale=0.7), run_time=0.8)
        self.play(Write(always_caption), run_time=1.2)
        self.wait(13.01 - 2.4)

        # Beat 4 (32.89~43.09s): 절대 안 받음 — 두 트랙 모두 통제색
        never_z1 = Dot(radius=0.18, color=NEVER_TAKER).move_to(track_z1.get_center() - RIGHT * 0.8)
        never_z0 = Dot(radius=0.18, color=NEVER_TAKER).move_to(track_z0.get_center() - RIGHT * 0.8)
        never_caption = Text("절대 안 받음: 동전과 무관하게 비처치", font_size=24, color=NEVER_TAKER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(always_caption), run_time=0.4)
        self.play(FadeIn(never_z1, scale=0.7), FadeIn(never_z0, scale=0.7), run_time=0.8)
        self.play(Write(never_caption), run_time=1.2)
        self.wait(10.20 - 2.4)

        # Beat 5 (43.09~59.15s): 핵심 — 순응자만 동전에 반응
        # 다른 dot들은 적당히 약화(0.45), complier만 박스로 강조.
        self.play(FadeOut(never_caption), run_time=0.4)
        reveal = Text("동전 결과에 따라 움직이는 건 순응자뿐", font_size=26, weight=BOLD, color=COMPLIER).to_edge(DOWN, buff=0.5)
        complier_box_top = SurroundingRectangle(complier_z1_dot, color=COMPLIER, buff=0.15, stroke_width=3)
        complier_box_bot = SurroundingRectangle(complier_z0_dot, color=COMPLIER, buff=0.15, stroke_width=3)
        self.play(
            always_z1.animate.set_opacity(0.45), always_z0.animate.set_opacity(0.45),
            never_z1.animate.set_opacity(0.45), never_z0.animate.set_opacity(0.45),
            run_time=0.7,
        )
        self.play(Create(complier_box_top), Create(complier_box_bot), run_time=0.9)
        self.play(Write(reveal), run_time=1.4)
        self.wait(16.06 - 3.4)

        # Beat 6 (59.15~70.31s): LATE 정의 카드
        late_box = RoundedRectangle(width=8.0, height=2.0, corner_radius=0.2,
                                      stroke_color=INSTRUMENT, stroke_width=3)
        late_title = Text("LATE", font_size=42, weight=BOLD, color=INSTRUMENT)
        late_sub = Text("Local Average Treatment Effect\n순응자에 한정된 평균 처치 효과", font_size=22,
                         color=WHITE, line_spacing=0.95)
        late_stack = VGroup(late_title, late_sub).arrange(DOWN, buff=0.25).move_to(late_box.get_center())
        late_group = VGroup(late_box, late_stack).move_to(ORIGIN)

        prior = VGroup(tracks, complier_z1_dot, complier_z0_dot,
                        complier_box_top, complier_box_bot,
                        always_z1, always_z0, never_z1, never_z0, reveal, title)
        self.play(FadeOut(prior), run_time=0.7)
        self.play(Create(late_box), run_time=0.9)
        self.play(FadeIn(late_stack, shift=UP * 0.2), run_time=1.4)
        self.wait(11.16 - 3.0)
        self.wait(self.WAIT_TAIL)
