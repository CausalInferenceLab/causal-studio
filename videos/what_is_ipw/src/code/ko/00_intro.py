from manim import *

# 씬 00 — 시작 표지 (약 5초). 오늘의 주제 IPW 소개.
# 타이밍 기준: build/audio/00_intro.timings.json (총 7.89s)
#   chunk0 0.00~3.30 "오늘의 주제는, 역확률 가중치. 아이피더블유입니다."
#   chunk1 3.30~7.85 "관찰 데이터만으로 진짜 원인을 가려내는 방법을..."


class Intro(Scene):
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

        topic = Text("오늘의 주제", font_size=34, color=GRAY_A, weight=BOLD)
        ipw = Text("IPW", font_size=150, color=ORANGE, weight=BOLD)
        kr = Text("역확률 가중치", font_size=46, color=WHITE, weight=BOLD)
        en = Text("Inverse Probability Weighting", font_size=30, color=GRAY_B, weight=BOLD)
        title = VGroup(topic, ipw, kr, en).arrange(DOWN, buff=0.38).move_to(UP * 0.1)

        # 밑줄 악센트
        rule = Line(LEFT * 2.7, RIGHT * 2.7, color=ORANGE, stroke_width=3).next_to(ipw, DOWN, buff=0.18)

        # chunk0 — 주제 + IPW
        play_at(0.30, FadeIn(topic, shift=DOWN * 0.1), run_time=0.4)
        play_at(0.90, Write(ipw), run_time=0.7)
        play_at(1.90, GrowFromCenter(rule), FadeIn(kr, shift=UP * 0.1), run_time=0.5)
        # chunk1 — 영문 병기
        play_at(3.60, FadeIn(en), run_time=0.5)

        go_to(8.10)
