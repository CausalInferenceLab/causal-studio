from manim import *

from videos.fuzzy_rdd.shared.common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


class Scene07Recap(Scene):
    """
    Scene 07: recap  (구 07_visualization + 08_examples + 09_outro 통합·간략화)
    스크립트: narration/07_recap.txt (메디케어·장학금 예시 모두 삭제, 3문단으로 재압축 — 2026-07-21 개정)
    타이밍: build/audio/07_recap.timings.json (총 30.31s, 3 chunks)

    개정 이력:
    - 1차: 메디케어 예시 삭제, 시뮬레이션 CI 복원(참값 0.5)도 Scene03/06과
      중복이라 "왈드는 점추정만, 2SLS는 신뢰구간까지"로 압축.
    - 2차(사용자 직접 스크립트 수정): 장학금 예시(370점/0.91 계산)까지 전부
      삭제하고, "정의 → 왈드 형태로 점추정+2SLS로 신뢰구간 → 마무리"의
      3문단·30초 순수 복습으로 재압축. 구체적 숫자(0.91) 예시가 사라졌으므로,
      Beat2 시각도 숫자 대신 Scene03에서 쓴 것과 같은 추상 기호 τ̂로 표현한다.
      (τ̂ 표기: Scene03 "formula[0] = MathTex(r'\\hat{\\tau}_{Fuzzy}', ...)"와 통일)
    - LATE 한글 명칭도 04_complier_late.txt("국소 평균 처치 효과, 즉 LATE")와
      맞춰 "국소범위의 처치효과"(1차 오기)에서 "국소 평균 처치 효과"로 수정.

    Beat1 chunk1 ( 0.00~12.40)  Fuzzy RDD 한 줄 정의 (복습)
    Beat2 chunk2 (12.40~21.08)  왈드(점추정 τ̂, CI 불가) → 2SLS(같은 점 + CI)
        Scene06 Beat3/4 시각 문법 재사용: TEAL 점=점추정치, RED=CI 불가,
        GOLD 막대+캡=CI, TEAL 점선=같은 점을 중심으로 한 구간이라는 connector.
        16.35 왈드→2SLS 전환 (문장 길이 비례 추정)
    Beat3 chunk3 (21.08~30.31)  마무리: Sharp✓ Fuzzy✓ → 다음 영상 (WAIT_TAIL)
    """

    def construct(self):
        import numpy as np

        # ── Beat 1 (chunk1, 0→12.40) Fuzzy RDD 한 줄 정의(복습) ─────────
        defn = VGroup(
            Text("Fuzzy RDD", font=FONT, font_size=40, color=TEAL_MAIN),
            Text("기준점이 처치를 완전히 결정하지 않을 때", font=FONT, font_size=24, color=WHITE),
            Text("자격을 도구변수로 삼아", font=FONT, font_size=24, color=GOLD_MAIN),
            Text("순응자에 대한 LATE 추정", font=FONT, font_size=24, color=WHITE,
                 t2c={"LATE": GOLD_MAIN}),
        ).arrange(DOWN, buff=0.38).move_to(ORIGIN)
        self.play(FadeIn(defn[0], shift=UP * 0.2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in defn[1:]], lag_ratio=0.4), run_time=1.4)
        self.wait(10.399)

        # ── Beat 2 (chunk2, 12.40→21.08) 왈드(점) → 2SLS(점+CI) ─────────
        # Scene06 Beat3/4의 시각 문법을 그대로 재활용(복습이니 새 언어를 쓰지 않는다):
        #   TEAL 점 = 점 추정치, RED 텍스트 = "신뢰구간 불가", GOLD 막대+캡 = 신뢰구간,
        #   TEAL 점선 = "그 점을 중심으로 한 구간"임을 잇는 connector.
        # 장학금 예시가 빠졌으므로 값은 숫자(0.91) 대신 Scene03과 같은 τ̂ 기호로 추상화.
        # 라벨은 영문 표기(Wald Estimator / 2SLS)로 통일. 시리즈 마지막 시각이라
        # 점 좌우에 "점 추정치"/τ̂ 캡션을 더하고, CI 등장 때 Flash로 강조해 더 풍성하게 마무리.
        # 남는 요소: 없음(defn 전부 정리) / 새 요소: label(+밑줄)+point(τ̂)+점 추정치 캡션+red 문구
        # 이 Beat의 핵심 시선: 점 하나 — 위치·색·값은 안 바뀌고, 그 주변 표시만 바뀐다
        # 라벨은 화면 맨 위(to_edge)가 아니라 점(UP*0.5)에 조금 더 가깝게 UP*1.7에 두고,
        # 밑줄을 달아 "제목처럼 멀리 떨어진 느낌"을 줄인다.
        label = Text("Wald Estimator", font=FONT, font_size=32, color=TEAL_MAIN).move_to(UP * 1.7)
        underline = Line(label.get_corner(DL), label.get_corner(DR), color=TEAL_MAIN, stroke_width=2.5).shift(DOWN * 0.12)
        point = Dot(UP * 0.5, radius=0.13, color=TEAL_MAIN)
        value_lab = MathTex(r"\hat{\tau}", font_size=36).set_color(TEAL_MAIN).next_to(point, RIGHT, buff=0.35)
        dot_cap = Text("점 추정치", font=FONT, font_size=16, color=TEAL_MAIN).next_to(point, LEFT, buff=0.35)
        blocked = Text("신뢰구간은 구할 수 없다", font=FONT, font_size=22, color=RED_MAIN).next_to(point, DOWN, buff=0.9)
        self.play(FadeOut(defn, run_time=0.4),
                  FadeIn(label, run_time=0.5), Create(underline, run_time=0.5), FadeIn(point, run_time=0.5),
                  FadeIn(value_lab, run_time=0.5), FadeIn(dot_cap, run_time=0.5),
                  FadeIn(blocked, run_time=0.5))
        self.wait(3.447)
        # 16.35: 왈드→2SLS. 점·값·캡션(TEAL)은 그대로 두고, 라벨은 즉시 Transform하지 않고
        # "지우고(밑줄과 함께 fade) → 다시 쓰는(Write)" 2단계로 나눠 전환에 무게를 싣는다.
        # (좌우 배치 대신, 시간축으로 펼쳐서 "옹졸하지 않게" 만드는 방식)
        label2 = Text("2SLS", font=FONT, font_size=32, color=GOLD_MAIN).move_to(label)
        underline2 = Line(label2.get_corner(DL), label2.get_corner(DR), color=GOLD_MAIN, stroke_width=2.5).shift(DOWN * 0.12)
        self.play(FadeOut(VGroup(label, underline), shift=UP * 0.15, run_time=0.4))
        self.play(Write(label2, run_time=0.5), Create(underline2, run_time=0.5))
        # red 문구만 GOLD CI 막대+TEAL 점선 connector로 대체. CI 막대는 굵고 넓게,
        # "신뢰구간" 캡션과 Flash를 더해 마지막답게 풍성히 마무리.
        cx, py = point.get_center()[0], point.get_center()[1]
        ci_cy = py - 1.0  # blocked 텍스트가 있던 자리와 거의 같은 높이
        ci_half = 0.85
        ci_bar = Line(np.array([cx - ci_half, ci_cy, 0]), np.array([cx + ci_half, ci_cy, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_capL = Line(np.array([cx - ci_half, ci_cy - 0.16, 0]), np.array([cx - ci_half, ci_cy + 0.16, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_capR = Line(np.array([cx + ci_half, ci_cy - 0.16, 0]), np.array([cx + ci_half, ci_cy + 0.16, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_center = Dot(np.array([cx, ci_cy, 0]), radius=0.09, color=TEAL_MAIN)
        connector = DashedLine(point.get_bottom() + DOWN * 0.05, np.array([cx, ci_cy + 0.2, 0]),
                               color=TEAL_MAIN, stroke_width=1.6, dash_length=0.08)
        ci_fig = VGroup(ci_bar, ci_capL, ci_capR, ci_center)
        ci_cap = Text("신뢰구간", font=FONT, font_size=18, color=GOLD_MAIN).next_to(ci_bar, DOWN, buff=0.28)
        self.play(FadeOut(blocked, run_time=0.3),
                  Create(connector, run_time=0.5), Create(ci_fig, run_time=0.6), FadeIn(ci_cap, run_time=0.6),
                  Flash(point, color=GOLD_MAIN, flash_radius=0.4, line_length=0.22, num_lines=10, run_time=0.6))
        # 남은 시간: 4.737(=21.084-16.347) - 0.4(erase) - 0.5(write) - 0.6(CI reveal) = 3.237
        self.wait(3.237)

        # ── Beat 3 (chunk3, 21.08→30.31) 마무리 (WAIT_TAIL) ────────────
        done = VGroup(
            Text("Sharp RDD  ✓", font=FONT, font_size=32, color=GREEN_MAIN),
            Text("Fuzzy RDD  ✓", font=FONT, font_size=32, color=GREEN_MAIN),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        nextv = Text("다음 영상에서 또 다른 인과추론 방법으로 만나요", font=FONT, font_size=24, color=GRAY_MID).move_to(DOWN * 1.3)
        self.play(FadeOut(VGroup(label2, underline2, point, value_lab, dot_cap, connector, ci_fig, ci_cap), run_time=0.4),
                  FadeIn(done, shift=UP * 0.15, run_time=0.6))
        self.wait(5.251)
        self.play(FadeIn(nextv, shift=UP * 0.1, run_time=0.5))
        # WAIT_TAIL = (30.308 + 0.45) - 26.935 - 0.5 = 3.323
        self.wait(3.323)
