from manim import *

from videos.fuzzy_rdd.shared.common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    TEAL_MAIN,
    WHITE,
)


class Scene03Wald(Scene):
    """
    Scene 03: wald  (ipynb §2 "어떻게 효과를 추정하는가")
    스크립트: narration/03_wald.txt
    타이밍: build/audio/03_wald.timings.json (총 61.70s, 6 chunks)

    직전 Scene(02_variables) 마지막 문장: "...자격은 처치에 영향을 주지만,
        처치를 완전히 결정하지는 않습니다."
    현재 Scene 첫 문장: "그렇다면 Fuzzy RDD에서는 처치 효과를 어떻게 추정할까요?"

    Beat1 chunk1   ( 0.00~ 4.34)  질문 헤드라인
    Beat2 chunk2   ( 4.34~17.01)  Fuzzy 부분 점프: 처치율 10%→65% 막대
    Beat3 chunk3   (17.01~28.76)  Y 0.5점 증가 캡션
    Beat4 chunk4-5 (28.76~47.71)  Wald 추정량 = ΔY/ΔD = 0.5/0.55 ≈ 0.91 + 분자·분모 명명 (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1) 질문 ───────────────────────────────
        q = Text("Fuzzy RDD에서 효과를 어떻게 추정할까?", font=FONT, font_size=34, color=WHITE).move_to(ORIGIN)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.wait(4.336 - 0.6)

        # ── Beat 2 (chunk2) Fuzzy 부분 점프: 막대 ──────────────
        head = VGroup(
            Text("Fuzzy RDD: 기준점을 넘어도 일부만 처치", font=FONT, font_size=24, color=WHITE),
            Text("(막대 = 장학금 수혜 확률)", font=FONT, font_size=18, color=GRAY_MID),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.7)
        bar0 = self._prob_bar(0.10, "자격 없음", "10%", GOLD_MAIN, "(수능 370점 미만)").move_to(LEFT * 2.3 + DOWN * 0.1)
        bar1 = self._prob_bar(0.65, "자격 있음", "65%", TEAL_MAIN, "(수능 370점 이상)").move_to(RIGHT * 2.3 + DOWN * 0.1)
        delta = Text("+55%p", font=FONT, font_size=26, color=WHITE).move_to(UP * 0.9)
        bars = VGroup(bar0, bar1, delta)
        self.play(FadeOut(q, run_time=0.4), FadeIn(head, run_time=0.5), FadeIn(bars, shift=UP * 0.15, run_time=0.7))
        self.wait(17.014 - 4.336 - 0.7)

        # ── Beat 3 (chunk3) Y 증가 캡션 ────────────────────────
        y_caption = VGroup(
            Text("학점(Y) 0.5점 증가", font=FONT, font_size=24, color=WHITE),
            Text("= 모두가 아니라 추가 수혜자(55%)가 만든 결과", font=FONT, font_size=20, color=GRAY_MID),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(y_caption, shift=UP * 0.15, run_time=0.6))
        self.wait(28.764 - 17.014 - 0.6)

        # ── Beat 4 (chunk4-5) Wald 추정량 ──────────────────────
        self.play(FadeOut(VGroup(head, bars, y_caption)), run_time=0.5)
        formula = MathTex(
            r"\hat{\tau}_{Fuzzy}", r"=", r"\frac{\Delta Y}{\Delta D}", r"=",
            r"\frac{0.5}{0.55}", r"\approx", r"0.91", font_size=52,
        ).move_to(UP * 0.6)
        formula[2].set_color(WHITE)
        formula[6].set_color(GOLD_MAIN)
        self.play(FadeIn(formula, shift=UP * 0.15, run_time=0.7))
        self.wait(39.677 - 28.764 - 0.5 - 0.7)

        label_y = self._wald_label("분자 (", r"ITT_Y", ") : 자격이 결과(Y)에 일으킨 변화량", GOLD_MAIN)
        label_d = self._wald_label("분모 (", r"ITT_D", ") : 자격이 처치(D)에 일으킨 변화량", TEAL_MAIN)
        label_d.next_to(label_y, DOWN, buff=0.3)
        labels = VGroup(label_y, label_d)
        labels.next_to(formula, DOWN, buff=0.9)
        self.play(FadeIn(labels, shift=UP * 0.15, run_time=0.6))
        # WAIT_TAIL = (47.818 + 1.0) - 39.677 - 0.6 = 8.541
        self.wait(8.541)

    def _wald_label(self, prefix: str, sub: str, suffix: str, color) -> VGroup:
        """분자·분모 레이블: 'prefix (ITT_Y) suffix' 형태로 아랫첨자 MathTex 포함."""
        t1 = Text(prefix, font=FONT, font_size=22, color=color)
        t2 = MathTex(sub, font_size=26).set_color(color)
        t3 = Text(suffix, font=FONT, font_size=22, color=color)
        row = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.05)
        t2.set_y(t1.get_center()[1])
        return row

    def _prob_bar(self, frac, label, pct, color, sublabel=None) -> VGroup:
        """처치율 막대: 0~100%를 높이 2.6으로 표현."""
        H = 2.6
        track = Rectangle(width=0.9, height=H, stroke_color=GRAY_MID, stroke_width=1.5, fill_opacity=0)
        fill = Rectangle(width=0.9, height=H * frac, stroke_width=0, fill_color=color, fill_opacity=0.9)
        fill.align_to(track, DOWN)
        pct_t = Text(pct, font=FONT, font_size=24, color=color).next_to(fill, UP, buff=0.15)
        lab = Text(label, font=FONT, font_size=20, color=WHITE).next_to(track, DOWN, buff=0.2)
        parts = VGroup(track, fill, pct_t, lab)
        if sublabel:
            sub = Text(sublabel, font=FONT, font_size=14, color=GRAY_MID).next_to(lab, DOWN, buff=0.1)
            parts.add(sub)
        return parts
