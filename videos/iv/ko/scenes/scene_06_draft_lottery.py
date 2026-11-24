from manim import *

from videos.iv.shared.common import (
    ACCENT,
    CONTROL_COLOR,
    FORBIDDEN,
    INSTRUMENT,
    SOFT,
    TREAT_COLOR,
    load_scene_timing_durations,
)


class Scene06_DraftLottery(Scene):
    """
    Scene 06: 1969 베트남 징집 추첨 = 국가 규모 IV.

    Core Claim:
    스노우의 수도 회사 트릭은 한 도시 위생 연구에 머무르지 않았다.
    한 세기 뒤 미국에서, 빙고 추첨이라는 자연의 동전이 군 복무가
    평생 소득에 미친 효과를 추정하는 도구변수로 쓰였다.

    Visual Pivot:
    빙고볼이 떨어지며 생일 번호가 결정되는 순간 — 우연이 사람을
    움직였다. 스노우의 수도 배관과 같은 구조다.

    Script: narration/06_draft_lottery.txt — 5 chunks, 66.10s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("06_draft_lottery", language="ko")
        # durations ≈ [6.72, 22.97, 10.56, 11.40, 14.45]

        # Beat 1 (0~6.72s): 국가 규모로 작동
        title = Text("같은 트릭, 국가 규모", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        scale_up = Text("작은 실험만이 아니다", font_size=24, color=SOFT).move_to(ORIGIN + UP * 0.2)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(scale_up), run_time=1.2)
        self.wait(6.72 - 1.9)

        # Beat 2 (6.72~29.69s): 1969 베트남 징집 추첨
        self.play(FadeOut(scale_up), run_time=0.4)
        date_label = Text("1969년 · 미국", font_size=28, weight=BOLD, color=SOFT).to_edge(UP, buff=1.4)
        # 빙고볼 시뮬레이션: 3개 공
        balls = VGroup()
        ball_nums = ["73", "144", "012"]
        for i, num in enumerate(ball_nums):
            ball = Circle(radius=0.5, color=ACCENT, stroke_width=3, fill_color=YELLOW_A, fill_opacity=0.9)
            ball_num = Text(num, font_size=22, weight=BOLD, color=BLACK).move_to(ball)
            balls.add(VGroup(ball, ball_num))
        balls.arrange(RIGHT, buff=0.5).move_to(UP * 0.2)
        ball_caption = Text("생일 365일이 적힌 공을 무작위로 추첨", font_size=22, color=WHITE).next_to(balls, DOWN, buff=0.5)
        rule = Text("낮은 번호 → 입대", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(DOWN * 1.5)
        independence_note = Text("태어난 날짜는 학력, 직업과 무관", font_size=20, color=SOFT).next_to(rule, DOWN, buff=0.3)

        self.play(FadeIn(date_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2, scale=0.7) for b in balls], lag_ratio=0.2), run_time=1.4)
        self.play(Write(ball_caption), run_time=1.4)
        self.play(Write(rule), run_time=1.0)
        self.play(FadeIn(independence_note, shift=UP * 0.1), run_time=0.9)
        self.wait(22.97 - 5.4)

        # Beat 3 (29.69~40.25s): 앵그리스트의 질문
        prior = VGroup(date_label, balls, ball_caption, rule, independence_note)
        self.play(FadeOut(prior), run_time=0.6)
        angrist = Text("조슈아 앵그리스트의 질문", font_size=26, weight=BOLD, color=ACCENT).to_edge(UP, buff=1.2)
        question = Text("\"군 복무가 평생 소득에 어떤 영향을 줄까?\"", font_size=26, color=WHITE).move_to(ORIGIN + UP * 0.4)
        # T → Y
        t_q = Text("군 복무", font_size=24, color=TREAT_COLOR)
        y_q = Text("평생 소득", font_size=24, color=CONTROL_COLOR)
        arrow_q = Arrow(LEFT * 1.0, RIGHT * 1.0, buff=0.05, color=WHITE, stroke_width=4)
        chain = VGroup(t_q, arrow_q, y_q).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.0)

        self.play(FadeIn(angrist, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(question), run_time=1.4)
        self.play(FadeIn(chain, shift=UP * 0.1), run_time=1.0)
        self.wait(10.56 - 3.1)

        # Beat 4 (40.25~51.65s): 단순 비교는 편향 — 참전 선택의 차이
        # chain을 작게 위로 정리, 편향 경고
        bias_warn = Text("참전 군인 vs 비참전 군인 단순 비교 → 편향", font_size=24, color=FORBIDDEN).to_edge(DOWN, buff=2.2)
        bias_reason = Text("참전을 선택한 사람과 회피한 사람은 애초에 다르다", font_size=20, color=SOFT).next_to(bias_warn, DOWN, buff=0.25)
        self.play(FadeIn(bias_warn, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(bias_reason, shift=UP * 0.05), run_time=0.9)
        self.wait(11.40 - 1.9)

        # Beat 5 (51.65~66.10s): 추첨을 도구변수로 → 스노우 회귀
        prior2 = VGroup(angrist, question, chain, bias_warn, bias_reason)
        self.play(FadeOut(prior2), run_time=0.6)
        title_fix = Text("추첨 번호 = 도구변수", font_size=30, weight=BOLD, color=INSTRUMENT).to_edge(UP, buff=1.2)
        # DAG: Z(추첨) → T(복무) → Y(소득)
        z6 = Circle(radius=0.4, color=INSTRUMENT, stroke_width=3)
        z6t = Text("추첨", font_size=20, color=INSTRUMENT, weight=BOLD).move_to(z6)
        z6g = VGroup(z6, z6t).move_to(LEFT * 3.5 + DOWN * 0.2)
        t6 = Circle(radius=0.4, color=TREAT_COLOR, stroke_width=3)
        t6t = Text("복무", font_size=20, color=TREAT_COLOR, weight=BOLD).move_to(t6)
        t6g = VGroup(t6, t6t).move_to(ORIGIN + DOWN * 0.2)
        y6 = Circle(radius=0.4, color=CONTROL_COLOR, stroke_width=3)
        y6t = Text("소득", font_size=20, color=CONTROL_COLOR, weight=BOLD).move_to(y6)
        y6g = VGroup(y6, y6t).move_to(RIGHT * 3.5 + DOWN * 0.2)
        zt6 = Arrow(z6g.get_right(), t6g.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        ty6 = Arrow(t6g.get_right(), y6g.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        callback = Text("한 세기 전 런던의 수도 회사 트릭이\n미국 노동시장에서도 통했다", font_size=22, color=SOFT, line_spacing=0.95).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(title_fix, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(z6g), FadeIn(t6g), FadeIn(y6g), run_time=0.9)
        self.play(GrowArrow(zt6), GrowArrow(ty6), run_time=0.9)
        self.play(Indicate(z6g, color=INSTRUMENT), run_time=0.8)
        self.play(Write(callback), run_time=1.6)
        self.wait(14.45 - 4.9)
        self.wait(self.WAIT_TAIL)
