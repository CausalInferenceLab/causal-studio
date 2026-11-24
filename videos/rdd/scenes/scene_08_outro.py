from manim import *

from rdd_common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    GREEN_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene08Outro(Scene):
    """
    Scene 08: outro
    스크립트: videos/rdd/src/scripts/08_outro.txt
    build/audio/08_outro.timings.json 기준 타이밍 (총 30.78s)

    Beat1 chunk1  ( 0.00~ 2.51s)  타이틀 "Sharp RDD 핵심 정리" (2.51s)
    Beat2 chunk2  ( 2.51~16.95s)  요약 카드 3개 순차 등장 (14.44s)
                                  — Running Variable/Cutoff, 연속성 가정, β̂₂ = LATE
    Beat3 chunk3  (16.95~24.89s)  Sharp vs Fuzzy 비교 도식 (7.94s)
    Beat4 chunk4  (24.89~30.70s)  "Fuzzy RDD" 예고 타이틀 (5.80s)

    ipynb 범위: 해당 없음 (영상 마무리 + 다음 편 예고)
    참고 3b1b: 없음 — 카드 나열 + 예고 구조
    직전 Scene 마지막 문장: "기준점 좌우 회귀식 적합 → RDD로 처치 효과 복원 가능"
    현재 Scene 첫 문장: "Sharp RDD를 정리해봅시다."
    """

    def _summary_card(self, icon_tex: str, body: str, accent: str) -> VGroup:
        """
        왼쪽 컬러 세로선 + 아이콘 수식 + 본문 텍스트 한 줄짜리 카드.
        icon_tex: LaTeX 수식 문자열, body: 한국어 설명 문자열, accent: 강조색
        """
        bar = Rectangle(width=0.07, height=0.55, fill_opacity=1,
                         fill_color=accent, stroke_width=0).set_stroke(width=0)
        label = MathTex(icon_tex, font_size=22, color=accent)
        desc = Text(body, font=FONT, font_size=18, color=WHITE)
        row = VGroup(label, desc).arrange(RIGHT, buff=0.25)
        return VGroup(bar, row).arrange(RIGHT, buff=0.22)

    def construct(self):
        # ── Beat 1 (chunk1: 0~2.51s) ────────────────────────
        # 새로 등장: 섹션 타이틀
        # 핵심 시선: "Sharp RDD 핵심 정리"
        # 지워질 요소: FadeOut → Beat2
        title = VGroup(
            Text("Sharp RDD", font=FONT, font_size=46, color=WHITE),
            Text("핵심 정리", font=FONT, font_size=28, color=GRAY_MID),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.25), run_time=0.6)
        self.play(FadeIn(title[1], shift=UP * 0.15), run_time=0.5)
        self.wait(1.11)
        self.play(FadeOut(title), run_time=0.3)
        # chunk1 end ~2.51s

        # ── Beat 2 (chunk2: 2.51~16.95s, 14.44s) ────────────
        # 새로 등장: 요약 카드 3개 (상→중→하 순차)
        # 핵심 시선: ① 처치 확정 구조, ② 연속성 가정, ③ β̂₂ = LATE
        # 지워질 요소: FadeOut → Beat3
        card1 = self._summary_card(
            r"X_i \geq c \Rightarrow D_i = 1",
            "기준점 초과 시 처치 확정 (Sharp)",
            YELLOW_MAIN,
        )
        card2 = self._summary_card(
            r"\text{Continuity Assumption}",
            "기준점 근방 → 준무작위 배정",
            BLUE_MAIN,
        )
        card3 = self._summary_card(
            r"\hat{\beta}_2 = \text{LATE}",
            "기준점 점프 크기 = 국소 처치 효과",
            GREEN_MAIN,
        )
        cards = VGroup(card1, card2, card3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        cards.move_to(ORIGIN)

        self.play(FadeIn(card1, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(3.8)
        self.play(FadeIn(card2, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(3.8)
        self.play(FadeIn(card3, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(4.84)
        self.play(FadeOut(cards), run_time=0.5)
        # chunk2 end ~16.95s

        # ── Beat 3 (chunk3: 16.95~24.89s, 7.94s) ────────────
        # 새로 등장: Sharp vs Fuzzy 비교 패널 (좌/우)
        # 핵심 시선: "현실에서는 처치가 확정되지 않는다" → Fuzzy 개념 예고
        # 지워질 요소: FadeOut → Beat4

        # 좌: Sharp 박스
        sharp_box = VGroup(
            Text("Sharp RDD", font=FONT, font_size=20, color=YELLOW_MAIN),
            MathTex(r"D_i = \mathbf{1}(X_i \geq c)", font_size=22, color=WHITE),
            Text("기준점 초과 → 반드시 처치", font=FONT, font_size=16, color=GRAY_MID),
        ).arrange(DOWN, buff=0.22)
        sharp_frame = SurroundingRectangle(sharp_box, color=YELLOW_MAIN,
                                           buff=0.28, corner_radius=0.12, stroke_width=1.5)
        sharp_panel = VGroup(sharp_frame, sharp_box).move_to(LEFT * 3.1)

        # 우: Fuzzy 박스 (물음표 처리)
        fuzzy_box = VGroup(
            Text("Fuzzy RDD", font=FONT, font_size=20, color=BLUE_MAIN),
            MathTex(r"P(D_i{=}1 \mid X_i) \uparrow \text{ at } c",
                    font_size=22, color=WHITE),
            Text("기준점 초과 → 처치 확률 증가", font=FONT, font_size=16, color=GRAY_MID),
        ).arrange(DOWN, buff=0.22)
        fuzzy_frame = SurroundingRectangle(fuzzy_box, color=BLUE_MAIN,
                                           buff=0.28, corner_radius=0.12, stroke_width=1.5)
        fuzzy_panel = VGroup(fuzzy_frame, fuzzy_box).move_to(RIGHT * 3.1)

        vs_lbl = Text("vs", font=FONT, font_size=22, color=GRAY_MID).move_to(ORIGIN)

        self.play(
            FadeIn(sharp_panel, shift=RIGHT * 0.2),
            FadeIn(vs_lbl),
            FadeIn(fuzzy_panel, shift=LEFT * 0.2),
            run_time=0.7,
        )
        self.wait(6.74)
        self.play(FadeOut(VGroup(sharp_panel, vs_lbl, fuzzy_panel)), run_time=0.5)
        # chunk3 end ~24.89s

        # ── Beat 4 (chunk4: 24.89~30.70s, 5.80s) ────────────
        # 새로 등장: Fuzzy RDD 예고 타이틀
        # 핵심 시선: "다음 영상에서"
        next_label = Text("다음 영상에서", font=FONT, font_size=22, color=GRAY_MID)
        fuzzy_title = Text("Fuzzy RDD", font=FONT, font_size=52, color=BLUE_MAIN)
        arrow = Text("→", font=FONT, font_size=30, color=GRAY_MID)
        teaser = VGroup(next_label, fuzzy_title).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(next_label, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(fuzzy_title, shift=UP * 0.25), run_time=0.6)
        self.wait(7.26)
