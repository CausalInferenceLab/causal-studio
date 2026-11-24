from manim import *

from fuzzy_rdd_common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene01RecapHook(Scene):
    """
    Scene 01: recap_hook
    스크립트: videos/fuzzy_rdd/src/scripts/01_recap_hook.txt
    build/audio/01_recap_hook.timings.json 기준 타이밍 (총 62.18s, 9 chunks)

    Beat1 chunk1-2 ( 0.00~15.51s)  Sharp RDD 복습: 헤드라인(구문형) → 예시 + 계단함수 그래프
    Beat2 chunk3   (15.51~20.02s)  "현실은 깔끔하지 않다" 헤드라인
    Beat3 chunk4-5 (20.02~32.18s)  현실 사례 대립: 371점(통과인데 미지급) ↔ 369점(미달인데 지급)
    Beat4 chunk6-7 (32.18~47.42s)  Fuzzy RDD로의 일반화 → 정의(2줄+화살표)
    Beat5 chunk8-9 (47.42~62.68s)  Fuzzy RDD 그래프(부분 점프) → 마무리 (WAIT_TAIL 포함)

    ipynb 범위: fz000001(제목) ~ fz100001(Recap, Sharp/Fuzzy 수식·비교표) 핵심 내용,
                74a9226c/cd4eff27(plot_rdd_type)의 Fuzzy 쪽 곡선 형태 참고,
                Section 1(fz200001) 시작 직전까지.
    참고 코드: videos/rdd/scenes/scene_02_sharp_vs_fuzzy.py의 Scene02SharpVsFuzzy._make_axes

    직전 Scene(rdd_basic 08_outro) 마지막 문장: "이번 영상에서는 Sharp RDD 위주로
        다뤘으니, 다음 영상에서 Fuzzy RDD를 다뤄보도록 하겠습니다."
    현재 Scene 첫 문장: "지난 영상에서, 점수가 기준점을 넘는 순간 처치 여부가
        완전히 결정되는 구조를 살펴봤습니다."

    1차 피드백 반영:
    - 오프닝 "다음 영상에서 → Fuzzy RDD" 예고 화면 제거 (바로 Recap으로 시작)
    - 370/371/369점 → 스크립트에서 "삼백칠십(일/구)점"으로 발음 풀어씀
    - 학생 카드는 점수+결과 텍스트로 단순화, 369점 카드는 해당 내레이션
      타이밍에 맞춰 등장

    2차 피드백 반영:
    - chunk3 수식 아래에 계단함수(스텝) 그래프를 추가해 D=1[X>=c]를 시각화
    - chunk9의 "0<점프 크기<1 숫자선" 시각화를 제거하고, Fuzzy RDD 그래프를
      더 일찍 등장시켜 유지

    3차 피드백 반영 (스크립트 재작성: chunk2/3 통합으로 "수식 D=1[X>=c]" 문장 제거,
        chunk9 "점프 크기 0~1" 문장 제거 → 9 chunks로 축소, 전체 65.63s):
    - chunk1 마지막 줄: "기준점 → 처치 완전 결정" → "기준점이 넘을 경우 100% 처치"
    - chunk2(예시+Sharp RDD 정리)에서 예시 텍스트와 계단함수 그래프 사이
      여백을 키우고 텍스트를 더 위쪽에 배치
    - chunk4-5의 "현실 사례" 라벨을 화면 위쪽 가장자리보다 아래로 이동
    - 메인 컬러를 TEAL_MAIN(#4DD0C4)/GOLD_MAIN(#C8A630)으로 교체
      (why_causal_inference 썸네일의 Treatment/Outcome 컬러와 통일)
    - Fuzzy RDD 그래프를 chunk8부터 등장시켜 chunk8 내레이션("부분적으로만
      점프, 15%→65%")과 그래프 등장 타이밍을 맞춤

    4차 피드백 반영 (스크립트 일부 수정 → 재생성, 전체 62.18s):
    - chunk1 "점수가 기준점을 넘는 순간" → "기준점을 넘는 순간"으로 축약 (사용자 수정)
    - chunk4-5(현실 사례)를 단순 나열이 아니라 "극명한 대립"으로 재구성:
      스크립트를 "기준점을 넘은 371점인데도 미지급 / 못 미친 369점인데도 지급"으로
      바꿔 기대-결과의 역설을 부각하고, 화면도 _make_case_card로 거울형 카드 2장 +
      상태(통과/미달)·결과(미지급/지급) 색 교차로 시각 대립을 강화
    """

    def construct(self):
        # ── Beat 1 (chunk1-2: 0~16.16s) ────────────────────────
        # 새로 등장: "지난 영상 Recap / Sharp RDD / 기준점이 넘을 경우 100% 처치"
        #            → "Sharp RDD" 소제목 + 예시 2줄 + 계단함수 그래프
        # 비워 두는 영역: 좌/우 (중앙 텍스트만)
        # 단일 핵심 시선: chunk1은 헤드라인 구문, chunk2는 예시+그래프
        recap_title = VGroup(
            Text("지난 영상 Recap", font=FONT, font_size=22, color=GRAY_MID),
            Text("Sharp RDD", font=FONT, font_size=46, color=TEAL_MAIN),
            Text("기준점이 넘을 경우 100% 처치", font=FONT, font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.6)

        self.play(FadeIn(recap_title, shift=UP * 0.2), run_time=0.7)
        self.wait(6.548 - 0.7)  # chunk1 end ~6.55s

        # chunk2: 예시(370점 이상/미만) + Sharp RDD 계단함수 그래프
        # 텍스트는 위쪽, 그래프는 아래쪽에 큰 여백을 두고 배치
        sharp_label = Text("Sharp RDD", font=FONT, font_size=30, color=TEAL_MAIN)
        example_label = Text("(예시)", font=FONT, font_size=20, color=GRAY_MID)
        example_lines = VGroup(
            Text("370점 이상 → 장학금 받음", font=FONT, font_size=24, color=TEAL_MAIN),
            Text("370점 미만 → 받지 못함", font=FONT, font_size=24, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        example_group = VGroup(sharp_label, example_label, example_lines).arrange(DOWN, buff=0.25)

        step_graph = self._make_step_graph()
        content2 = VGroup(example_group, step_graph).arrange(DOWN, buff=0.9).move_to(ORIGIN)

        self.play(FadeOut(recap_title, run_time=0.5), FadeIn(content2, shift=UP * 0.15, run_time=0.8))
        self.wait(15.511 - 6.548 - 0.8)  # chunk2 end ~15.51s

        self.play(FadeOut(content2), run_time=0.5)

        # ── Beat 2 (chunk3: 16.16~21.18s) ──────────────────────
        # 남는 요소: 없음
        # 새로 등장: "현실은 깔끔하지 않다" 헤드라인
        # 비워 두는 영역: 상/하
        # 단일 핵심 시선: "현실은 이렇게 깔끔하지 않습니다"
        headline2 = Text(
            "그런데, 현실은 이렇게 깔끔하지 않습니다", font=FONT, font_size=30, color=WHITE,
        ).move_to(ORIGIN)

        self.play(FadeIn(headline2, shift=UP * 0.2), run_time=0.6)
        self.wait(20.016 - 15.511 - 0.5 - 0.6)  # chunk3 end ~20.02s (FadeOut 0.5 + FadeIn 0.6)

        # ── Beat 3 (chunk4-5: 20.02~32.18s) ────────────────────
        # 남는 요소: headline2 → 상단(가장자리보다 살짝 아래) 라벨로 축소되어 유지
        # 새로 등장: 좌(371점=기준점 통과인데 미지급) ↔ 우(369점=기준점 미달인데 지급)
        #            두 카드를 거울처럼 마주 보게 배치하고, "통과/미달"(상태)과
        #            "지급/미지급"(결과) 색을 교차시켜(통과=TEAL+미지급=RED,
        #            미달=GOLD+지급=GREEN) 기대와 결과가 어긋나는 대립을 강조
        # 비워 두는 영역: 두 카드 사이 중앙 여백 + 상단 라벨 영역
        # 단일 핵심 시선: 좌측 카드(chunk4) → 우측 카드(chunk5) — 내레이션과 등장 타이밍 일치
        top_label = Text("현실 사례", font=FONT, font_size=22, color=GRAY_MID).to_edge(UP, buff=1.3)

        # 좌: 기준점을 "넘었는데도" 장학금 미지급 (기대와 반대)
        left_card = self._make_case_card(
            score="371점", status="기준점 통과", status_color=TEAL_MAIN,
            result="장학금 미지급", result_color=RED_MAIN, reason="신청 기간 놓침",
        ).move_to(LEFT * 3.4 + DOWN * 0.25)
        # 우: 기준점에 "못 미쳤는데도" 장학금 지급 (기대와 반대)
        right_card = self._make_case_card(
            score="369점", status="기준점 미달", status_color=GOLD_MAIN,
            result="장학금 지급", result_color=GREEN_MAIN, reason="재심사로 받음",
        ).move_to(RIGHT * 3.4 + DOWN * 0.25)

        self.play(
            Transform(headline2, top_label),
            FadeIn(left_card, shift=RIGHT * 0.2),
            run_time=0.7,
        )
        self.wait(26.564 - 20.016 - 0.7)  # chunk4 end ~26.56s

        self.play(FadeIn(right_card, shift=LEFT * 0.2), run_time=0.6)
        self.wait(32.183 - 26.564 - 0.6)  # chunk5 end ~32.18s

        self.play(FadeOut(VGroup(headline2, left_card, right_card)), run_time=0.5)

        # ── Beat 4 (chunk6-7: 32.18~47.42s) ────────────────────
        # 남는 요소: 없음
        # 새로 등장: 일반화 헤드라인 → Fuzzy RDD 정의(2줄+화살표)
        # 비워 두는 영역: 상/하
        # 단일 핵심 시선: "→ Fuzzy RDD"
        headline3 = VGroup(
            Text("기준점을 넘었다고 모두가 처치를 받는 것도 아니고,", font=FONT, font_size=24, color=WHITE),
            Text("못 넘었다고 모두가 처치를 못 받는 것도 아닙니다", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeIn(headline3, shift=UP * 0.2), run_time=0.7)
        self.wait(39.149 - 32.183 - 0.5 - 0.7)  # chunk6 end ~39.15s (FadeOut 0.5 + FadeIn 0.7)

        fuzzy_def = VGroup(
            Text("기준점이 처치 확률에 불연속적인 영향을 주지만", font=FONT, font_size=22, color=WHITE),
            Text("완전히 결정하지는 않는 경우", font=FONT, font_size=22, color=WHITE),
            Text("Fuzzy RDD", font=FONT, font_size=30, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeOut(headline3, run_time=0.4), FadeIn(fuzzy_def, shift=UP * 0.2, run_time=0.7))
        self.wait(47.462 - 39.149 - 0.7)  # chunk7 end ~47.46s

        # ── Beat 5 (chunk8-9: 48.81~63.57s) ────────────────────
        # 남는 요소: 없음
        # 새로 등장: Fuzzy RDD 그래프(부분 점프 15%→65%, chunk8) → 마무리 헤드라인(chunk9)
        # 비워 두는 영역: 좌/우
        # 단일 핵심 시선: chunk8은 그래프의 부분 점프, chunk9는 마무리 문장
        graph_title = Text("Fuzzy RDD", font=FONT, font_size=32, color=GOLD_MAIN).to_edge(UP, buff=0.7)
        axes, cutoff_line = self._make_axes()
        fuzzy_curve = self._make_fuzzy_curve(axes)
        ax_x_lbl = Text("점수 (X)", font=FONT, font_size=16, color=GRAY_MID)
        ax_x_lbl.next_to(axes.x_axis.get_right(), RIGHT, buff=0.12)
        ax_y_lbl = Text("처치 확률 (D)", font=FONT, font_size=16, color=GRAY_MID)
        ax_y_lbl.next_to(axes.y_axis.get_top(), UP, buff=0.1)
        jump_label = Text("부분 점프: 15% → 65%", font=FONT, font_size=22, color=WHITE)
        # AppleGothic 폰트에서 "Sharp RDD" 사이 공백이 거의 보이지 않아 별도 Text로 분리
        sharp_note = VGroup(
            Text("(Sharp", font=FONT, font_size=16, color=GRAY_MID),
            Text("RDD라면 0% → 100%)", font=FONT, font_size=16, color=GRAY_MID),
        ).arrange(RIGHT, buff=0.1)
        labels = VGroup(jump_label, sharp_note).arrange(DOWN, buff=0.15)

        graph_group = VGroup(axes, cutoff_line, fuzzy_curve, ax_x_lbl, ax_y_lbl).move_to(DOWN * 0.4)
        labels.next_to(graph_group, DOWN, buff=0.35)
        fuzzy_graph_group = VGroup(graph_title, graph_group, labels)

        self.play(FadeOut(fuzzy_def, run_time=0.5), FadeIn(fuzzy_graph_group, shift=UP * 0.15, run_time=0.8))
        self.wait(55.310 - 47.462 - 0.8)  # chunk8 end ~55.31s

        closing = Text(
            "Fuzzy RDD, 어떻게 다뤄야 할까?", font=FONT, font_size=34, color=WHITE,
        ).move_to(ORIGIN)

        self.play(FadeOut(fuzzy_graph_group), FadeIn(closing, shift=UP * 0.2), run_time=0.7)
        # WAIT_TAIL = (mp3 61.904 + 0.5) - 56.010 = 6.394
        self.wait(6.394)

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _make_case_card(self, score, status, status_color, result, result_color, reason) -> VGroup:
        """현실 사례 카드 한 장.

        위→아래로 점수(흰색) → 상태 배지(외곽선, 통과/미달) → 결과 알약(채움, 지급/미지급)
        → 사유(회색) 순으로 쌓는다. 두 카드가 같은 크기 프레임을 갖도록 RoundedRectangle을
        고정 크기로 두고, 프레임 색은 결과(result_color)에 맞춰 좌/우 대립을 강조한다.
        """
        score_t = Text(score, font=FONT, font_size=40, color=WHITE)

        status_t = Text(status, font=FONT, font_size=19, color=status_color)
        status_box = SurroundingRectangle(
            status_t, color=status_color, buff=0.12, corner_radius=0.08, stroke_width=1.5,
        )
        status_g = VGroup(status_box, status_t)

        result_t = Text(result, font=FONT, font_size=24, color=WHITE)
        result_box = SurroundingRectangle(
            result_t, color=result_color, fill_color=result_color, fill_opacity=0.9,
            buff=0.14, corner_radius=0.1, stroke_width=0,
        )
        result_g = VGroup(result_box, result_t)

        reason_t = Text(reason, font=FONT, font_size=16, color=GRAY_MID)

        inner = VGroup(score_t, status_g, result_g, reason_t).arrange(DOWN, buff=0.24)
        frame = RoundedRectangle(
            width=3.8, height=3.2, corner_radius=0.15, color=result_color, stroke_width=2.5,
        )
        inner.move_to(frame.get_center())
        return VGroup(frame, inner)

    def _make_step_graph(self) -> VGroup:
        """Sharp RDD 수식 D=1[X>=c]를 보여주는 계단함수 그래프."""
        axes = Axes(
            x_range=[0, 10, 10],
            y_range=[0, 1.2, 1],
            x_length=3.8,
            y_length=2.0,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_tip": False},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": [0, 1]},
            tips=False,
        )
        for label in axes.y_axis.numbers:
            label.set(font_size=14)

        c_x = 5
        cutoff_line = DashedLine(
            axes.c2p(c_x, 0), axes.c2p(c_x, 1.15),
            color=YELLOW_MAIN, dash_length=0.06, stroke_width=2,
        )
        left_line = axes.plot(lambda x: 0, x_range=[0, c_x], color=GOLD_MAIN, stroke_width=5)
        right_line = axes.plot(lambda x: 1, x_range=[c_x, 10], color=TEAL_MAIN, stroke_width=5)
        open_dot = Circle(radius=0.06, color=GOLD_MAIN, fill_opacity=0, stroke_width=2.5).move_to(axes.c2p(c_x, 0))
        closed_dot = Dot(axes.c2p(c_x, 1), radius=0.06, color=TEAL_MAIN)
        c_label = Text("c", font=FONT, font_size=18, color=YELLOW_MAIN).next_to(cutoff_line, DOWN, buff=0.1)

        x_lbl = Text("점수 (X)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_right(), RIGHT, buff=0.12)
        y_lbl = Text("처치 여부 (D)", font=FONT, font_size=14, color=GRAY_MID)
        y_lbl.next_to(axes.y_axis.get_top(), UP, buff=0.1)

        return VGroup(axes, cutoff_line, left_line, right_line, open_dot, closed_dot, c_label, x_lbl, y_lbl)

    def _make_axes(self):
        """Fuzzy 그래프용 축 (x: 340~400, cutoff 370)."""
        axes = Axes(
            x_range=[340, 401, 30],
            y_range=[0, 1.01, 0.5],
            x_length=4.5,
            y_length=2.6,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_tip": False},
            x_axis_config={"numbers_to_include": [340, 370, 400]},
            y_axis_config={"numbers_to_include": [0, 1]},
            tips=False,
        )
        for label in axes.x_axis.numbers:
            label.set(font_size=16)
        for label in axes.y_axis.numbers:
            label.set(font_size=16)
        cutoff_line = DashedLine(
            axes.c2p(370, 0), axes.c2p(370, 1.05),
            color=YELLOW_MAIN, dash_length=0.08, stroke_width=2,
        )
        return axes, cutoff_line

    def _make_fuzzy_curve(self, axes: Axes) -> VGroup:
        """Fuzzy RDD: 370점에서 0.15→0.65 부분 점프."""
        left_line = axes.plot(
            lambda x: 0.05 + (0.15 - 0.05) / 30 * (x - 340),
            x_range=[340, 370], color=GOLD_MAIN, stroke_width=5,
        )
        right_line = axes.plot(
            lambda x: 0.65 + (0.85 - 0.65) / 30 * (x - 370),
            x_range=[370, 400], color=TEAL_MAIN, stroke_width=5,
        )
        jump_line = DashedLine(
            axes.c2p(370, 0.15), axes.c2p(370, 0.65),
            color=GRAY_MID, stroke_width=2, dash_length=0.08, stroke_opacity=0.8,
        )
        dot_open   = Circle(radius=0.07, color=GOLD_MAIN, fill_opacity=0, stroke_width=2.5).move_to(axes.c2p(370, 0.15))
        dot_closed = Dot(axes.c2p(370, 0.65), radius=0.07, color=TEAL_MAIN, fill_opacity=1)
        return VGroup(left_line, right_line, jump_line, dot_open, dot_closed)
