from manim import *

TEAL_MAIN   = "#4DD0C4"
GOLD_MAIN   = "#C8A630"
GRAY_DARK   = "#374151"
GRAY_MID    = "#9CA3AF"
GRAY_LIGHT  = "#F3F4F6"
GREEN_MAIN  = "#22C55E"
RED_MAIN    = "#EF4444"
YELLOW_MAIN = "#EAB308"
WHITE       = "#FFFFFF"

FONT = "AppleGothic"


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
    참고 코드: videos/rdd/src/rdd.py Scene02SharpVsFuzzy._make_axes (그래프 구조 축소 재사용)

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


class Scene02Variables(Scene):
    """
    Scene 02: variables  (ipynb §1 "Fuzzy RDD란?")
    스크립트: src/scripts/02_variables.txt
    타이밍: build/audio/02_variables.timings.json (총 65.09s, 7 chunks)

    직전 Scene(01_recap_hook) 마지막 문장: "이번 영상에서는, 이 부분적인 점프를
        가진 Fuzzy RDD를 어떻게 다뤄야 하는지 살펴보겠습니다."
    현재 Scene 첫 문장: "앞서 봤듯이, Fuzzy RDD는 기준점이 처치를 백 퍼센트
        강제하지 않을 때의 RDD입니다."

    Beat1 chunk1   ( 0.00~ 6.27)  한 줄 정의 헤드라인
    Beat2 chunk2-3 ( 6.27~30.33)  장학금 예시 + 자격≠수혜 현실 사례 4종
    Beat3 chunk4   (30.33~35.39)  "네 가지 변수를 구분하자" 전환
    Beat4 chunk5-6 (35.39~52.52)  변수 4개 표: X→Z→D→Y 한 행씩 순차 등장
                                  (나레이션 문장 내 글자 수 비율로 Z/Y 등장 시점 추정:
                                   Z ≈41.02s, Y ≈49.81s)
    Beat5 chunk7   (52.52~65.57)  Z=D(Sharp) vs Z≠D(Fuzzy) 대비 (WAIT_TAIL)
                                  변수 표는 삭제하지 않고 좌측에 축소·반투명으로 유지 +
                                  우측에 Z/D 재확인 caption 배치 (4차 피드백)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~6.27) 한 줄 정의 ──────────────────
        # 단일 핵심 시선: 정의 문장 / 비워두는 영역: 상하
        title = VGroup(
            Text("Fuzzy RDD 란?", font=FONT, font_size=40, color=TEAL_MAIN),
            Text("기준점이 처치를 100% 강제하지 않는 RDD", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        self.wait(6.269 - 0.7)

        # ── Beat 2 (chunk2-3: 6.27~30.33) 장학금 예시 + 현실 사례 ──
        # 남는 요소: 없음 / 새 요소: 자격 규칙(상단) + 사례 칩(하단)
        # 단일 핵심 시선: chunk2=자격 규칙, chunk3=현실 사례 목록
        rule = VGroup(
            Text("수능 370점 이상", font=FONT, font_size=26, color=WHITE),
            Text("→ 장학금 신청 자격", font=FONT, font_size=26, color=TEAL_MAIN),
        ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.1)
        rule_note = Text("Sharp RDD라면 자격 = 모두 수혜", font=FONT, font_size=18, color=GRAY_MID).next_to(rule, DOWN, buff=0.3)

        self.play(FadeOut(title, run_time=0.5), FadeIn(VGroup(rule, rule_note), shift=UP * 0.15, run_time=0.7))
        self.wait(17.043 - 6.269 - 0.5 - 0.7)

        # chunk3: 현실 사례 (자격 있어도 미수혜 / 자격 없어도 수혜)
        cases_pos = VGroup(
            Text("371점 · 신청 기간 놓침", font=FONT, font_size=20, color=RED_MAIN),
            Text("372점 · 서류 미비 탈락", font=FONT, font_size=20, color=RED_MAIN),
            Text("375점 · 형편 넉넉, 신청 안 함", font=FONT, font_size=20, color=RED_MAIN),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        case_neg = Text("368점 · 재심사로 받음", font=FONT, font_size=20, color=GREEN_MAIN)
        cases = VGroup(cases_pos, case_neg).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.6)

        self.play(FadeIn(cases, shift=UP * 0.15, lag_ratio=0.2, run_time=0.9))
        self.wait(30.325 - 17.043 - 0.9)

        # ── Beat 3 (chunk4: 30.33~35.39) 전환 ──────────────────
        bridge = Text("네 가지 변수를 구분하자", font=FONT, font_size=32, color=WHITE).move_to(ORIGIN)
        self.play(FadeOut(VGroup(rule, rule_note, cases), run_time=0.4), FadeIn(bridge, shift=UP * 0.2, run_time=0.6))
        self.wait(35.387 - 30.325 - 0.4 - 0.6)

        # ── Beat 4 (chunk5-6: 35.39~52.52) 변수 4개 표: X→Z→D→Y 순차 등장 ──
        # arrange(DOWN) 시 x 센터 정렬로 열 위치 깨짐 방지:
        # 각 행은 절대 x 좌표 유지, y만 shift로 배치
        # 나레이션 순서(먼저 X는... / 지는 도구변수로... / D는... / Y는...)에 맞춰
        # 한 행씩 등장시킨다. chunk 내 등장 시점은 문장 글자 수 비율로 추정.
        header = self._var_row_header()
        row_x = self._var_row("X", "독립변수", "수능 점수", TEAL_MAIN)
        row_z = self._var_row("Z", "도구변수", "자격 여부(370점 이상)", GOLD_MAIN)
        row_d = self._var_row("D", "처치변수", "실제 장학금 수혜 여부", TEAL_MAIN)
        row_y = self._var_row("Y", "결과변수", "학점 (GPA)", GOLD_MAIN)

        header.shift(UP * 2.1)
        row_x.shift(UP * 1.1)
        row_z.shift(UP * 0.1)
        row_d.shift(DOWN * 1.0)
        row_y.shift(DOWN * 2.0)

        hline = Line(LEFT * 5.0, RIGHT * 4.5, color=GRAY_MID, stroke_width=0.8).set_y(1.6)

        full_table = VGroup(header, row_x, row_z, row_d, row_y)

        # chunk5 전반부 "먼저 X는 독립변수를..." → 헤더 + 구분선 + X 행
        self.play(FadeOut(bridge, run_time=0.4), FadeIn(VGroup(header, hline, row_x), shift=UP * 0.15, run_time=0.7))
        self.wait(41.024 - 35.387 - 0.4 - 0.7)
        # chunk5 후반부 "지는 도구변수로..." → Z 행
        self.play(FadeIn(row_z, shift=UP * 0.15, run_time=0.5))
        self.wait(45.743 - 41.024 - 0.5)
        # chunk6 전반부 "D는 처치변수로..." → D 행
        self.play(FadeIn(row_d, shift=UP * 0.15, run_time=0.5))
        self.wait(49.811 - 45.743 - 0.5)
        # chunk6 후반부 "Y는 결과변수..." → Y 행
        self.play(FadeIn(row_y, shift=UP * 0.15, run_time=0.5))
        self.wait(52.524 - 49.811 - 0.5)
        self.wait(0.8)  # 표 전환 전 brief pause

        # ── Beat 5 (chunk7: 52.52~65.57) Z=D vs Z≠D ────────────
        # 8차 피드백: 비교/문장/캡션이 3개의 독립된 텍스트 덩어리로 떠 있어 난잡함
        # → Scene01의 카드 패턴(RoundedRectangle 프레임)을 재사용해 Sharp/Fuzzy를
        # 나란한 카드 두 개로 통합. "자격은 처치에 영향을 주지만..." 설명은 Fuzzy
        # 카드에 속한 문장으로 카드 안에 넣는다.
        # 9차 피드백: 처음부터 Fuzzy 카드 아래에 빈 공간을 남겨두지 말고, Sharp와
        # 같은 높이로 시작했다가 문장이 추가될 때 위쪽 모서리는 고정한 채 아래로만
        # 자라나게 한다 (RoundedRectangle을 Transform으로 키움).
        self.play(FadeOut(VGroup(full_table, hline), run_time=0.5))

        sharp_top = VGroup(
            Text("Sharp RDD", font=FONT, font_size=24, color=GRAY_MID),
            MathTex(r"Z = D", font_size=44).set_color(GRAY_MID),
        ).arrange(DOWN, buff=0.35)
        CARD_H = 2.6
        sharp_frame = RoundedRectangle(width=3.6, height=CARD_H, corner_radius=0.15, color=GRAY_MID, stroke_width=2)
        sharp_top.move_to(sharp_frame.get_center())
        sharp_card = VGroup(sharp_frame, sharp_top)

        fuzzy_top = VGroup(
            Text("Fuzzy RDD", font=FONT, font_size=24, color=TEAL_MAIN),
            MathTex(r"Z \neq D", font_size=44).set_color(TEAL_MAIN),
        ).arrange(DOWN, buff=0.35)
        FUZZY_W = 5.6
        # 처음엔 Sharp와 동일한 높이(CARD_H)로 시작
        fuzzy_frame = RoundedRectangle(width=FUZZY_W, height=CARD_H, corner_radius=0.15, color=TEAL_MAIN, stroke_width=2)
        fuzzy_top.move_to(fuzzy_frame.get_center())
        fuzzy_card = VGroup(fuzzy_frame, fuzzy_top)

        cards = VGroup(sharp_card, fuzzy_card).arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to(UP * 0.3)

        # 하단 참고 캡션: 작은 폰트 + 회색 톤으로 "본문이 아니라 각주"처럼 보이게
        z_ref = VGroup(
            MathTex("Z", font_size=22).set_color(GOLD_MAIN),
            Text("= 도구변수 (자격 여부)", font=FONT, font_size=17, color=GRAY_MID),
        ).arrange(RIGHT, buff=0.15)
        d_ref = VGroup(
            MathTex("D", font_size=22).set_color(TEAL_MAIN),
            Text("= 처치변수 (실제 수혜)", font=FONT, font_size=17, color=GRAY_MID),
        ).arrange(RIGHT, buff=0.15)
        zd_recap = VGroup(z_ref, d_ref).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(sharp_card, shift=UP * 0.15, run_time=0.7), FadeIn(fuzzy_card, shift=UP * 0.15, run_time=0.7), FadeIn(zd_recap, run_time=0.5))
        self.wait(59.0 - 52.524 - 0.8 - 0.5 - 0.7)

        # 문장이 들어갈 만큼 키운 Fuzzy 프레임(윗변 고정, 아래로만 확장)으로 Transform
        fuzzy_frame_grown = RoundedRectangle(
            width=FUZZY_W, height=3.6, corner_radius=0.15, color=TEAL_MAIN, stroke_width=2,
        )
        fuzzy_frame_grown.move_to(fuzzy_frame.get_center())
        fuzzy_frame_grown.align_to(fuzzy_frame, UP)  # 윗변을 원래 프레임과 맞춰 아래로만 자라는 것처럼 보이게

        fuzzy_note = VGroup(
            Text("자격은 처치에 영향을 주지만,", font=FONT, font_size=17, color=WHITE),
            Text("완전히 결정하지는 않습니다", font=FONT, font_size=17, color=WHITE),
        ).arrange(DOWN, buff=0.12)
        # 늘어난 프레임에서 fuzzy_top 아래 남는 공간의 세로 중앙에 배치
        note_zone_y = (fuzzy_top.get_bottom()[1] + fuzzy_frame_grown.get_bottom()[1]) / 2
        fuzzy_note.move_to([fuzzy_frame.get_center()[0], note_zone_y, 0])

        self.play(
            Transform(fuzzy_frame, fuzzy_frame_grown, run_time=0.6),
            FadeIn(fuzzy_note, shift=UP * 0.1, run_time=0.6),
        )
        # WAIT_TAIL = (65.573 + 0.5) - 59.0 - 0.6 = 6.473 (+ 보정 1.39)
        self.wait(7.863)

    def _var_row_header(self) -> VGroup:
        """변수 표 헤더 행: 표기 / 의미 / 예시."""
        s = Text("표기", font=FONT, font_size=18, color=GRAY_MID).move_to(LEFT * 4.3)
        n = Text("의미", font=FONT, font_size=18, color=GRAY_MID).move_to(LEFT * 2.4, aligned_edge=LEFT)
        d = Text("예시", font=FONT, font_size=18, color=GRAY_MID).move_to(RIGHT * 0.3, aligned_edge=LEFT)
        return VGroup(s, n, d)

    def _var_row(self, sym, name, desc, sym_color) -> VGroup:
        """변수 표 한 행: [기호] [이름] — [설명], 고정 x좌표로 열 정렬."""
        s = MathTex(sym + "_i", font_size=40).set_color(sym_color).move_to(LEFT * 4.3)
        n = Text(name, font=FONT, font_size=24, color=WHITE).move_to(LEFT * 2.4, aligned_edge=LEFT)
        d = Text(desc, font=FONT, font_size=22, color=GRAY_MID).move_to(RIGHT * 0.3, aligned_edge=LEFT)
        return VGroup(s, n, d)


class Scene03Wald(Scene):
    """
    Scene 03: wald  (ipynb §2 "어떻게 효과를 추정하는가")
    스크립트: src/scripts/03_wald.txt
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


class Scene04ComplierLate(Scene):
    """
    Scene 04: complier_late  (ipynb §3 "추정된 효과는 무엇을 의미하는가")
    스크립트: src/scripts/04_complier_late.txt
    타이밍: build/audio/04_complier_late.timings.json (총 55.58s, 7 chunks)

    직전 Scene(03_wald) 마지막 문장: "...왈드 추정량이라고 합니다."
    현재 Scene 첫 문장: "방금 우리는 왈드 추정량으로 처치 효과를 계산했습니다..."

    Beat1 chunk1-2 ( 0.00~20.81)  맥락 설명 + "누구에 대한 효과?" 질문
    Beat2 chunk3-4 (20.81~36.78)  행동이 바뀐 사람만 잡힌다
    Beat3 chunk5-7 (36.78~63.53)  네 유형 표 (항상/절대 제외 → 위반자 배제)
    Beat4 chunk8   (63.53~75.10)  순응자 = 추정 대상, LATE (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1) 맥락 설명 ─────────────────────────
        ctx = VGroup(
            Text("Wald 추정량으로 처치 효과를 계산했습니다.", font=FONT, font_size=26, color=WHITE),
            VGroup(
                Text("자격이 생겨도 일부는 처치를 받을 수 없고,", font=FONT, font_size=22, color=GRAY_MID),
                Text("자격이 없더라도 일부는 처치를 받을 수 있습니다.", font=FONT, font_size=22, color=GRAY_MID),
            ).arrange(DOWN, buff=0.2),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        self.play(FadeIn(ctx, shift=UP * 0.2), run_time=0.7)
        self.wait(12.121 - 0.7)

        # ── Beat 1 (chunk2) 질문 ───────────────────────────────
        q = VGroup(
            Text("그 효과는", font=FONT, font_size=30, color=WHITE),
            Text("'누구'에 대한 효과일까?", font=FONT, font_size=38, color=TEAL_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.play(FadeOut(ctx, run_time=0.4), FadeIn(q, shift=UP * 0.15, run_time=0.6))
        self.wait(20.944 - 12.121 - 0.4 - 0.6)

        # ── Beat 2 (chunk3) 잡히지 않는 두 케이스 ───────────────
        b2 = VGroup(
            Text("Case 1.  수능 370점 미만이어도 장학금 받는 학생", font=FONT, font_size=22, color=GRAY_MID),
            Text("Case 2.  수능 370점 이상이어도 장학금 못 받는 학생", font=FONT, font_size=22, color=GRAY_MID),
            Text("→ Wald 추정량에 잡히지 않음", font=FONT, font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.5)
        self.play(FadeOut(q, run_time=0.4), FadeIn(b2, shift=UP * 0.15, run_time=0.7))
        self.wait(30.824 - 20.944 - 0.4 - 0.7)

        # ── Beat 2 (chunk4) Wald 식 + 반영 대상 ─────────────────
        formula_wald = MathTex(r"\hat{\tau}_{Fuzzy} = \frac{\Delta Y}{\Delta D}", font_size=52).move_to(UP * 0.5)
        b2c = Text("오직 '자격 때문에 행동이 바뀐 사람'만 반영", font=FONT, font_size=24, color=GOLD_MAIN)
        b2c.next_to(formula_wald, DOWN, buff=0.7)
        self.play(FadeOut(b2, run_time=0.4), FadeIn(VGroup(formula_wald, b2c), shift=UP * 0.1, run_time=0.6))
        self.wait(45.592 - 30.824 - 0.6)

        # ── Beat 3 (chunk5) 네 유형 표 ─────────────────────────
        self.play(FadeOut(VGroup(formula_wald, b2c)), run_time=0.5)
        header = self._type_row("유형", "자격 X", "자격 O", 2.05, GRAY_MID, header=True)
        r_comp = self._type_row("순응자 (Complier)",          "처치 X", "처치 O",  1.15, WHITE)
        r_at   = self._type_row("항상 수혜자 (Always-taker)",  "처치 O", "처치 O",  0.35, WHITE)
        r_nt   = self._type_row("절대 비수혜자 (Never-taker)", "처치 X", "처치 X", -0.45, WHITE)
        r_def  = self._type_row("위반자 (Defier)",             "처치 O", "처치 X", -1.25, WHITE)
        table = VGroup(header, r_comp, r_at, r_nt, r_def)
        hline = Line(LEFT * 4.3, RIGHT * 4.3, color=GRAY_MID, stroke_width=1).move_to(UP * 1.62)
        table_g = VGroup(table, hline).move_to(UP * 0.3)
        cap = Text("자격(Z)에 따라 처치(D)가 어떻게 달라지나", font=FONT, font_size=24, color=WHITE).to_edge(UP, buff=0.7)
        self.play(FadeIn(VGroup(table_g, cap), run_time=0.7))
        self.wait(51.815 - 45.592 - 0.5 - 0.7)

        # chunk6: 항상/절대 수혜자 설명 (하얗게 강조, 나머지 흐리게)
        self.play(r_comp.animate.set_opacity(0.35), r_def.animate.set_opacity(0.35), run_time=0.5)
        self.wait(65.376 - 51.815 - 0.5)

        # chunk6 끝: 항상/절대 dim + 빨간줄, 위반자 복원
        strike_at = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_at.get_center())
        strike_nt = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_nt.get_center())
        self.play(
            r_at.animate.set_opacity(0.35), r_nt.animate.set_opacity(0.35),
            Create(strike_at), Create(strike_nt),
            r_def.animate.set_opacity(1.0),
            run_time=0.5,
        )

        # chunk7: 위반자 설명 (위반자만 하얀글씨, 빨간줄 없음)
        self.wait(72.342 - 65.376 - 0.5)

        # chunk7 끝: 위반자 dim + 빨간줄, 순응자 복원
        strike_def = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_def.get_center())
        self.play(
            r_def.animate.set_opacity(0.35), Create(strike_def),
            r_comp.animate.set_opacity(1.0),
            run_time=0.5,
        )

        # ── Beat 4 (chunk8) 순응자 = LATE ──────────────────────
        box = SurroundingRectangle(r_comp, color=TEAL_MAIN, buff=0.18, corner_radius=0.08, stroke_width=3)
        label_comp = Text("추정 대상 →", font=FONT, font_size=20, color=TEAL_MAIN)
        label_comp.next_to(box, LEFT, buff=0.2)
        cap4 = Text("순응자들에 대한 국소 평균 처치 효과 (LATE)", font=FONT, font_size=22, color=WHITE).to_edge(DOWN, buff=1.5)
        self.play(Create(box), FadeOut(cap, run_time=0.3), FadeIn(cap4, shift=UP * 0.1, run_time=0.6), FadeIn(label_comp, run_time=0.6))
        # WAIT_TAIL = (84.950 + 1.0) - 72.342 - 0.5 - 0.6 = 12.508
        self.wait(12.508)

    def _type_row(self, name, v0, v1, y, name_color, header=False) -> VGroup:
        """네 유형 표 한 행: 이름(좌) + Z=0열 + Z=1열, 고정 x로 정렬."""
        import numpy as np
        fs = 22 if header else 20
        n = Text(name, font=FONT, font_size=fs, color=name_color).move_to(np.array([-4.2, y, 0]), aligned_edge=LEFT)
        c0 = Text(v0, font=FONT, font_size=fs, color=name_color).move_to(np.array([1.4, y, 0]))
        c1 = Text(v1, font=FONT, font_size=fs, color=name_color).move_to(np.array([3.6, y, 0]))
        return VGroup(n, c0, c1)


class Scene05Assumptions(Scene):
    """
    Scene 05: assumptions  (ipynb §4 "핵심 가정")
    스크립트: src/scripts/05_assumptions.txt
    타이밍: build/audio/05_assumptions.timings.json (총 79.82s, 6 chunks)

    직전 Scene(04_complier_late) 마지막 문장: "...국소 평균 처치 효과인 LATE입니다."
    현재 Scene 첫 문장: "사실 우리가 지렛대로 삼은 자격 지는, 정확히 말하면 도구변수입니다..."

    Beat1 chunk1-2 ( 0.00~13.75)  Z = 도구변수(IV) → 유효 조건 3가지 (좌측 리스트 등장)
    Beat2 chunk3   (13.75~40.31)  관련성: Cov(Z,D)≠0, 분모≠0, F>10
    Beat3 chunk4   (40.31~59.63)  배제 제약: Z→D→Y, 직접 경로 없음
    Beat4 chunk5   (59.63~72.68)  단조성: 위반자 없음, D(Z=1)≥D(Z=0)
    Beat5 chunk6   (72.68~79.64)  3가지 성립 → Wald = LATE (WAIT_TAIL)
    """

    def construct(self):
        import numpy as np
        # ── Beat 1 (chunk1-2) IV → 3조건 리스트 ────────────────
        head = VGroup(
            Text("자격 Z = 도구변수 (IV)", font=FONT, font_size=36, color=TEAL_MAIN),
            Text("Fuzzy RDD는 본질적으로 도구변수 추정 문제", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(head, shift=UP * 0.2), run_time=0.6)
        self.wait(10.263 - 0.6)

        top = Text("유효한 도구변수의 3가지 조건", font=FONT, font_size=24, color=GRAY_MID).to_edge(UP, buff=0.8)
        t1 = Text("1. 관련성", font=FONT, font_size=27, color=GRAY_MID)
        t2 = Text("2. 배제 제약", font=FONT, font_size=27, color=GRAY_MID)
        t3 = Text("3. 단조성", font=FONT, font_size=27, color=GRAY_MID)
        titles = VGroup(t1, t2, t3).arrange(DOWN, buff=0.9, aligned_edge=LEFT).move_to(LEFT * 4.0)
        sep = Line(UP * 1.9, DOWN * 1.9, color=GRAY_MID, stroke_width=1).move_to(LEFT * 1.6)

        self.play(FadeOut(head, run_time=0.4), FadeIn(top, run_time=0.5), FadeIn(titles, shift=RIGHT * 0.1, run_time=0.6), Create(sep, run_time=0.5))
        self.wait(13.746 - 10.263 - 0.4 - 0.6)

        detail_pos = RIGHT * 2.4

        # ── Beat 2 (chunk3) 관련성 ─────────────────────────────
        d1 = VGroup(
            Text("자격이 생기면 처치 확률이 실제로 ↑", font=FONT, font_size=22, color=WHITE),
            MathTex(r"\mathrm{Cov}(Z, D) \neq 0", font_size=34).set_color(TEAL_MAIN),
            Text("= Wald 분모 ≠ 0", font=FONT, font_size=20, color=GRAY_MID),
            Text("F통계량 > 10 → 강한 도구변수", font=FONT, font_size=20, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.4).move_to(detail_pos)
        self.play(t1.animate.set_color(TEAL_MAIN), FadeIn(d1, shift=UP * 0.1, run_time=0.6))
        self.wait(40.310 - 13.746 - 0.6)

        # ── Beat 3 (chunk4) 배제 제약 ──────────────────────────
        diagram = self._iv_diagram_icons()
        d2 = VGroup(
            Text("자격은 오직 처치를 통해서만 결과에 영향", font=FONT, font_size=22, color=WHITE),
            diagram,
            Text("Z → Y 직접 경로는 없어야 함", font=FONT, font_size=20, color=RED_MAIN),
        ).arrange(DOWN, buff=0.45).move_to(detail_pos)
        self.play(t1.animate.set_color(GRAY_MID), t2.animate.set_color(TEAL_MAIN),
                  FadeOut(d1), FadeIn(d2, shift=UP * 0.1), run_time=0.5)
        self.wait(59.629 - 40.310 - 0.5)

        # ── Beat 4 (chunk5) 단조성 ─────────────────────────────
        d3 = VGroup(
            Text("자격이 생기면 거부하는 사람(위반자) 없음", font=FONT, font_size=22, color=WHITE),
            MathTex(r"D_i(Z{=}1) \geq D_i(Z{=}0)", font_size=32).set_color(TEAL_MAIN),
            Text("늘어난 처치 = 전부 순응자", font=FONT, font_size=20, color=GRAY_MID),
        ).arrange(DOWN, buff=0.45).move_to(detail_pos)
        self.play(t2.animate.set_color(GRAY_MID), t3.animate.set_color(TEAL_MAIN),
                  FadeOut(d2), FadeIn(d3, shift=UP * 0.1), run_time=0.5)
        self.wait(72.678 - 59.629 - 0.5)

        # ── Beat 5 (chunk6) 결론 ───────────────────────────────
        concl = VGroup(
            Text("3가지 가정이 성립하면", font=FONT, font_size=24, color=WHITE),
            Text("Wald 추정량 = LATE", font=FONT, font_size=32, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(detail_pos)
        self.play(t3.animate.set_color(GRAY_MID),
                  t1.animate.set_color(TEAL_MAIN), t2.animate.set_color(TEAL_MAIN),
                  FadeOut(d3), FadeIn(concl, shift=UP * 0.1), run_time=0.6)
        self.play(t3.animate.set_color(TEAL_MAIN), run_time=0.3)
        # WAIT_TAIL = (79.821 + 0.5) - 72.678 - 0.6 - 0.3 = 6.743
        self.wait(6.743)

    def _iv_diagram(self) -> VGroup:
        """Z → D → Y 경로 다이어그램 (배제 제약 시각화)."""
        import numpy as np
        def node(lbl, color, x):
            c = Circle(radius=0.32, color=color, stroke_width=2.5, fill_opacity=0).move_to(np.array([x, 0, 0]))
            t = MathTex(lbl, font_size=28).set_color(color).move_to(c.get_center())
            return VGroup(c, t)
        z = node("Z", GOLD_MAIN, -1.7)
        d = node("D", TEAL_MAIN, 0.0)
        y = node("Y", WHITE, 1.7)
        a1 = Arrow(z.get_right(), d.get_left(), buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.25, color=GRAY_MID)
        a2 = Arrow(d.get_right(), y.get_left(), buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.25, color=GRAY_MID)
        return VGroup(z, d, y, a1, a2)

    def _iv_diagram_icons(self) -> VGroup:
        """Z→D→Y 아이콘 다이어그램 (임상시험 예시, 배제 제약 시각화)."""
        from pathlib import Path
        import numpy as np

        ICONS = Path(__file__).parent.parent.parent / "assets" / "tabler-icons" / "icons" / "outline"
        xs     = [-2.2,  0.0,  2.2]
        svgs   = ["vaccine-bottle.svg", "pill.svg", "heartbeat.svg"]
        vars_  = ["Z", "D", "Y"]
        colors = [GOLD_MAIN, TEAL_MAIN, WHITE]
        subs   = ["임상 배정", "약 복용", "건강 회복"]

        nodes = []
        for x, svg, var, color, sub in zip(xs, svgs, vars_, colors, subs):
            ico = SVGMobject(str(ICONS / svg), height=0.75)
            ico.set_stroke(color=color, width=2.0, family=True).set_fill(opacity=0)
            ico.move_to(np.array([x, 0.1, 0]))
            v = MathTex(var, font_size=24).set_color(color).next_to(ico, UP, buff=0.12)
            s = Text(sub, font=FONT, font_size=14, color=GRAY_MID).next_to(ico, DOWN, buff=0.12)
            nodes.append(VGroup(ico, v, s))

        a1 = Arrow(np.array([xs[0]+0.52, 0.1, 0]), np.array([xs[1]-0.52, 0.1, 0]),
                   buff=0, stroke_width=2.5, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        a2 = Arrow(np.array([xs[1]+0.52, 0.1, 0]), np.array([xs[2]-0.52, 0.1, 0]),
                   buff=0, stroke_width=2.5, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)

        arc = CurvedArrow(np.array([xs[0]+0.1, 0.85, 0]), np.array([xs[2]-0.1, 0.85, 0]),
                          angle=-PI / 4, color=RED_MAIN, stroke_width=2.5)
        cross = Text("✕", font=FONT, font_size=22, color=RED_MAIN).move_to(np.array([0.0, 1.45, 0]))

        return VGroup(*nodes, a1, a2, arc, cross)


class Scene06TwoSLS(Scene):
    """
    Scene 06: twosls
    스크립트: src/scripts/06_twosls.txt
    타이밍: build/audio/06_twosls.timings.json (총 101.19s, 8 chunks)

    chunk1:   0.00 →   4.09  질문: 실제 데이터에선 Wald Estimator를 어떻게 계산?
    chunk2:   4.09 →  14.44  Wald 수식(가운데) + 분자/분모 변화량 라벨
    chunk3:  14.44 →  36.32  점선 구분 + 우측 "How to Compute It?": 분자·분모 각각→분수→점 추정치, red "신뢰구간 불가"
    chunk4:  36.32 →  50.02  "2SLS": 1)점 추정치 동일(●) 2)신뢰구간(막대, 점선으로 점과 연결)
    chunk5:  50.02 →  61.53  참고: 2SLS는 일반 IV 추정법 (Z→D→Y 일반 체인)
    chunk6:  61.53 →  70.91  우리 Fuzzy RDD: Z=자격(IV), D=처치(내생) 라벨 부여
    chunk7:  70.91 →  87.45  1단계: Z→D̂ (스테이지 카드)
    chunk8:  87.45 → 100.91  2단계: D̂→Y, β̂1=레이트 (스테이지 카드, 마지막·WAIT_TAIL)

    변경 이력:
    - 스크립트 재구성(9 chunk): 질문→Wald→분자/분모(점OK·CI어려움)→2SLS해결→
      참고(일반 IV)→Fuzzy RDD 연결→1·2단계→결론. Z/D 카드가 2SLS 설명 뒤로 이동.
    - Beat3/4: "분자·분모 따로 구하면 점추정치는 쉽지만 비율의 신뢰구간은 까다롭다 →
      2SLS가 그 [?]를 회귀 한 번으로 채운다"를 점·[?]·CI 막대로 시각화.
    - Beat5/6: 일반 IV 체인(Z→D→Y)을 먼저 보이고, 같은 체인에 Fuzzy RDD 라벨을 덧붙임.
    - 1·2단계: 표 제거, 수식 1개 주인공 스테이지 카드 + D̂ 전달 화살표.
      2단계 D̂는 1단계와 같은 하늘색(TEAL)으로 칠해 '그대로 대입' 강조.
    - 내레이션 Y/Z/D는 한글 음차(와이/제트/디), LATE는 '레이트'로 작성.
      (_endogeneity_dag / _medical_eg_diagram / _bias_diagram 헬퍼는 현재 미사용)
    """

    def construct(self):
        import numpy as np

        # ── Beat 1 (chunk1, 0→4.365) 질문 ───────────────────────────────
        # 섹션5(왈드=레이트) 다음, "그럼 실제로 어떻게 계산?"이라는 질문만 던진다.
        question = Text("실제 데이터에선 Wald Estimator를 어떻게 계산할까?",
                        font=FONT, font_size=28, color=GOLD_MAIN,
                        t2c={"Wald Estimator": TEAL_MAIN}).move_to(ORIGIN)
        self.play(FadeIn(question, shift=UP * 0.1, run_time=0.6))
        self.wait(4.087 - 0.6)

        # ── Beat 2 (chunk2, 4.365→14.489) Wald 수식 + 분자/분모 변화량 라벨 ──
        # "앞서 말했듯이" 왈드 수식을 가운데에 다시 보이고, 분자/분모가 무엇인지 라벨.
        wald_title = Text("Wald Estimator", font=FONT, font_size=24, color=TEAL_MAIN).move_to(UP * 2.6)
        eq_main = MathTex(r"\hat{\tau}", r"=", r"\frac{\Delta Y}{\Delta D}", font_size=80)
        eq_main[0].set_color(TEAL_MAIN)
        eq_main[2].set_color(TEAL_MAIN)
        eq_main.move_to(UP * 0.2)
        num_lbl = Text("결과의 변화량", font=FONT, font_size=18, color=GRAY_MID).next_to(eq_main, RIGHT, buff=1.3).shift(UP * 0.65)
        den_lbl = Text("처치 확률의 변화량", font=FONT, font_size=18, color=GRAY_MID).next_to(eq_main, RIGHT, buff=1.3).shift(DOWN * 0.65)
        arr_num = Arrow(num_lbl.get_left(), eq_main[2].get_top() + RIGHT * 0.25, buff=0.12,
                        stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        arr_den = Arrow(den_lbl.get_left(), eq_main[2].get_bottom() + RIGHT * 0.25, buff=0.12,
                        stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        numden = VGroup(num_lbl, den_lbl, arr_num, arr_den)
        self.play(FadeOut(question, run_time=0.4),
                  FadeIn(wald_title, shift=UP * 0.1, run_time=0.5),
                  FadeIn(eq_main, shift=UP * 0.2, run_time=0.7))
        self.play(FadeIn(numden, run_time=0.5))
        self.wait(14.443 - 4.087 - 0.7 - 0.5)

        # ── Beat 3 (chunk3, 14.489→35.712) 분자·분모 각각 구해 점 추정치 / CI 불가 ──
        # 우측에 "분자(ΔY)·분모(ΔD)를 각각 구해 ÷ → 점 추정치 하나"를 시각화하고,
        # 중하단부에 빨간 글씨로 "신뢰구간은 구할 수 없다"를 둔다. (하단 bcap 제거)
        vx = 3.2
        divider = DashedLine(np.array([-1.8, 2.25, 0]), np.array([-1.8, -2.25, 0]),
                             color=GRAY_MID, stroke_width=1.4, dash_length=0.12)
        rhead = Text("How to Compute It?", font=FONT, font_size=24, color=GOLD_MAIN).move_to(np.array([2.6, 1.95, 0]))
        # 분자·분모를 각각 구해서 → 나눠서 → 점 추정치 하나
        num = VGroup(Text("분자", font=FONT, font_size=15, color=GRAY_MID),
                     MathTex(r"\Delta Y", font_size=30).set_color(TEAL_MAIN)).arrange(RIGHT, buff=0.18).move_to(np.array([0.45, 0.95, 0]))
        den = VGroup(Text("분모", font=FONT, font_size=15, color=GRAY_MID),
                     MathTex(r"\Delta D", font_size=30).set_color(GOLD_MAIN)).arrange(RIGHT, buff=0.18).move_to(np.array([0.45, -0.25, 0]))
        # 분자·분모를 실제 분수 ΔY/ΔD 로 '합쳐' 보여준다 (가운데 ÷ 기호만 덩그러니 두지 않음)
        frac = MathTex(r"\frac{\Delta Y}{\Delta D}", font_size=46,
                       substrings_to_isolate=[r"\Delta Y", r"\Delta D"]).move_to(np.array([2.15, 0.35, 0]))
        frac.set_color_by_tex(r"\Delta Y", TEAL_MAIN)
        frac.set_color_by_tex(r"\Delta D", GOLD_MAIN)
        a_n = Arrow(num.get_right(), frac.get_left() + UP * 0.20, buff=0.16,
                    stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        a_d = Arrow(den.get_right(), frac.get_left() + DOWN * 0.20, buff=0.16,
                    stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        pt_dot = Dot(np.array([4.0, 0.35, 0]), radius=0.12, color=TEAL_MAIN)
        a_eq = Arrow(frac.get_right(), pt_dot.get_left(), buff=0.18,
                     stroke_width=2.0, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        pt_label = Text("점 추정치", font=FONT, font_size=18, color=TEAL_MAIN).next_to(pt_dot, UP, buff=0.22)
        compute_grp = VGroup(num, den, frac, a_n, a_d, a_eq, pt_label)
        nocl = Text("하지만 신뢰구간은 구할 수 없다", font=FONT, font_size=20, color=RED_MAIN).move_to(np.array([2.3, -1.55, 0]))
        self.play(
            FadeOut(numden, run_time=0.3),
            wald_title.animate.move_to(np.array([-4.1, 1.5, 0])),
            eq_main.animate.scale(0.72).move_to(np.array([-4.1, 0.1, 0])),
            Create(divider, run_time=0.6),
            FadeIn(rhead, run_time=0.5),
            run_time=0.7,
        )
        # 17.8 "분자인 ... 나누면 되니까요": 분자/분모→분수→점 추정치
        # 26.0 "이 값을 얼마나 믿을 수 있는지": 그제야 red "신뢰구간 구할 수 없다"
        T3_NUMDEN, T3_NOCL = 17.8, 26.0
        self.wait(T3_NUMDEN - 14.443 - 0.7)
        self.play(FadeIn(num, run_time=0.45), FadeIn(den, run_time=0.45))
        self.play(GrowArrow(a_n, run_time=0.4), GrowArrow(a_d, run_time=0.4), FadeIn(frac, run_time=0.45))
        self.play(GrowArrow(a_eq, run_time=0.4), FadeIn(pt_dot, run_time=0.4), FadeIn(pt_label, run_time=0.4))
        self.wait(T3_NOCL - T3_NUMDEN - 0.45 - 0.45 - 0.4)
        self.play(FadeIn(nocl, run_time=0.5))
        self.wait(36.316 - T3_NOCL - 0.5)

        # ── Beat 4 (chunk4, 36.316→50.016) 2SLS가 두 가지를 해결 ──────────
        # 36.316 "2SLS를 씁니다": Beat3 우측(분자/분모·점·CI불가)을 '한꺼번에' 지우고
        #   헤더 아래에 답 "2SLS"만 띄운다(겹침 방지).
        # 40.0 "점 추정치는 ... 정확히 같으면서": 1) 줄 + 점 추정치(●) + 화살표.
        # 45.7 "표준오차와 신뢰구간 또한 구할 수 있다는 장점": 2) 줄 + 신뢰구간 막대.
        #   막대는 점 추정치 바로 아래에 세로 정렬하고 점선으로 연결해 '같은 추정치의 구간'임을 보인다.
        T4_LINE1, T4_LINE2, T4_END = 40.0, 45.7, 50.016
        ans_2sls = Text('"2SLS"', font=FONT, font_size=36, weight=BOLD, color=GOLD_MAIN).move_to(np.array([2.55, 1.15, 0]))
        sub_2sls = Text("(2단계 최소제곱법)", font=FONT, font_size=16, color=GRAY_MID).next_to(ans_2sls, DOWN, buff=0.14)
        line1 = Text("1)  분자·분모 각각 구한 값과 동일", font=FONT, font_size=19, color=WHITE,
                     t2c={"분자·분모 각각 구한 값": TEAL_MAIN}).move_to(np.array([-0.85, -0.55, 0]), aligned_edge=LEFT)
        line2 = Text("2)  신뢰구간도 구할 수 있다", font=FONT, font_size=19, color=WHITE,
                     t2c={"신뢰구간": GOLD_MAIN}).move_to(np.array([-0.85, -1.85, 0]), aligned_edge=LEFT)
        # 오른쪽 시각 요소 앵커 x: 두 줄 중 더 긴 쪽 오른쪽 끝 + 여유
        anchor_x = max(line1.get_right()[0], line2.get_right()[0]) + 1.0
        # 1) 점 추정치 dot
        dotpos = np.array([anchor_x, line1.get_center()[1], 0])
        est_dot = Dot(dotpos, radius=0.11, color=TEAL_MAIN)
        dot_cap = Text("점 추정치", font=FONT, font_size=15, color=TEAL_MAIN).move_to(dotpos + UP * 0.4)
        arr1 = Arrow(line1.get_right() + RIGHT * 0.1, dotpos + LEFT * 0.22, buff=0.08,
                     stroke_width=2.0, color=TEAL_MAIN, max_tip_length_to_length_ratio=0.28)
        # 2) 신뢰구간 막대 — 점 추정치 바로 아래(같은 x). 중앙점은 점 추정치와 같은 색,
        #    점선 connector로 위 점과 연결해 '그 점을 중심으로 한 구간'임을 표현.
        ci_cy = line2.get_center()[1]
        ci_half = 0.72
        ci_bar = Line(np.array([anchor_x - ci_half, ci_cy, 0]), np.array([anchor_x + ci_half, ci_cy, 0]),
                      color=GOLD_MAIN, stroke_width=4)
        ci_capL = Line(np.array([anchor_x - ci_half, ci_cy - 0.14, 0]), np.array([anchor_x - ci_half, ci_cy + 0.14, 0]),
                       color=GOLD_MAIN, stroke_width=4)
        ci_capR = Line(np.array([anchor_x + ci_half, ci_cy - 0.14, 0]), np.array([anchor_x + ci_half, ci_cy + 0.14, 0]),
                       color=GOLD_MAIN, stroke_width=4)
        ci_center = Dot(np.array([anchor_x, ci_cy, 0]), radius=0.08, color=TEAL_MAIN)
        connector = DashedLine(est_dot.get_bottom() + DOWN * 0.02, np.array([anchor_x, ci_cy + 0.18, 0]),
                               color=TEAL_MAIN, stroke_width=1.6, dash_length=0.08)
        ci_fig = VGroup(ci_bar, ci_capL, ci_capR, ci_center)
        # 36.316: Beat3 우측 정리 + "2SLS" 등장
        self.play(
            FadeOut(compute_grp, run_time=0.45), FadeOut(pt_dot, run_time=0.45), FadeOut(nocl, run_time=0.45),
            FadeIn(ans_2sls, scale=1.1, run_time=0.5), FadeIn(sub_2sls, run_time=0.5),
        )
        self.wait(T4_LINE1 - 36.316 - 0.5)
        # 39.6: 1) 점 추정치 동일
        self.play(FadeIn(line1, run_time=0.5), FadeIn(est_dot, run_time=0.5), FadeIn(dot_cap, run_time=0.5))
        self.play(GrowArrow(arr1, run_time=0.4))
        self.wait(T4_LINE2 - T4_LINE1 - 0.5 - 0.4)
        # 45.0: 2) 신뢰구간 — 점 추정치를 중심으로 한 구간(점선 연결)
        self.play(FadeIn(line2, run_time=0.5), Create(connector, run_time=0.5), Create(ci_fig, run_time=0.6))
        compare_grp = VGroup(wald_title, eq_main, divider, rhead, ans_2sls, sub_2sls,
                             est_dot, dot_cap, line1, arr1, line2, connector, ci_fig)
        self.wait(T4_END - T4_LINE2 - 0.6)

        # ── Beat 5 (chunk5, 48.344→60.325) 참고: 2SLS는 일반 IV 추정법 ────
        # 일반 도구변수 체인 Z→D→Y를 보여 "Fuzzy RDD 전용이 아님"을 전달.
        nZ = MathTex(r"Z", font_size=48).set_color(GOLD_MAIN)
        nD = MathTex(r"D", font_size=48).set_color(TEAL_MAIN)
        nY = MathTex(r"Y", font_size=48).set_color(WHITE)
        chain = VGroup(nZ, nD, nY).arrange(RIGHT, buff=2.6).move_to(UP * 0.1)
        ar1 = Arrow(nZ.get_right(), nD.get_left(), buff=0.25, stroke_width=2.5,
                    color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        ar2 = Arrow(nD.get_right(), nY.get_left(), buff=0.25, stroke_width=2.5,
                    color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        roleZ = Text("도구변수", font=FONT, font_size=17, color=GOLD_MAIN).next_to(nZ, DOWN, buff=0.3)
        roleD = Text("내생변수", font=FONT, font_size=17, color=TEAL_MAIN).next_to(nD, DOWN, buff=0.3)
        roleY = Text("결과", font=FONT, font_size=17, color=WHITE).next_to(nY, DOWN, buff=0.3)
        chain_grp = VGroup(chain, ar1, ar2, roleZ, roleD, roleY)
        ref_title = Text("참고 · 2SLS는 일반적인 도구변수 추정법", font=FONT, font_size=23, color=GRAY_MID).move_to(UP * 2.6)
        ref_cap = Text("Fuzzy RDD 에서만 쓰는 방법이 아니다", font=FONT, font_size=18, color=WHITE).move_to(DOWN * 2.0)
        self.play(FadeOut(compare_grp, run_time=0.4),
                  FadeIn(ref_title, run_time=0.5),
                  FadeIn(chain_grp, shift=UP * 0.1, run_time=0.6),
                  FadeIn(ref_cap, run_time=0.5))
        self.wait(61.533 - 50.016 - 0.6)

        # ── Beat 6 (chunk6, 61.533→70.914) 우리 Fuzzy RDD: Z=자격, D=처치 ──
        # 같은 체인에 Fuzzy RDD 라벨을 덧붙여 일반→특수로 자연스럽게 연결.
        nameZ = Text("자격 여부", font=FONT, font_size=17, color=GOLD_MAIN).next_to(nZ, UP, buff=0.3)
        nameD = Text("처치 여부", font=FONT, font_size=17, color=TEAL_MAIN).next_to(nD, UP, buff=0.3)
        fuzzy_title = Text("우리 Fuzzy RDD 에서는", font=FONT, font_size=24, color=TEAL_MAIN).move_to(UP * 2.6)
        fuzzy_cap = Text("자격 = 도구변수,   처치 = 내생변수", font=FONT, font_size=18, color=WHITE).move_to(DOWN * 2.0)
        self.play(FadeOut(ref_title, run_time=0.3), FadeIn(fuzzy_title, run_time=0.5),
                  FadeIn(nameZ, shift=DOWN * 0.05, run_time=0.5), FadeIn(nameD, shift=DOWN * 0.05, run_time=0.5),
                  FadeOut(ref_cap, run_time=0.3), FadeIn(fuzzy_cap, run_time=0.5))
        self.wait(70.914 - 61.533 - 0.5)

        # ── Beat 7 (chunk7, 70.914→87.446) 1단계 ─────────────────────────
        # 표 제거. 수식 1개를 주인공으로 두는 위/아래 스테이지 카드 구조.
        # 상단 카드=1단계(활성), 하단 카드=2단계(미리보기 dim), 사이 D̂ 전달 화살표.
        def _stage(label, eq_parts, accent, eq_color):
            box = RoundedRectangle(width=6.8, height=1.35, corner_radius=0.14,
                                   stroke_color=accent, stroke_width=2.6, fill_opacity=0)
            lab = Text(label, font=FONT, font_size=22, color=accent)
            eq = MathTex(*eq_parts, font_size=40).set_color(eq_color)
            VGroup(lab, eq).arrange(RIGHT, buff=0.5).move_to(box.get_center())
            return box, lab, eq

        # 1단계 카드 (활성) — 산출물 D̂는 하늘색(TEAL)으로 칠해 다음 단계와 연결
        s1_box, s1_lab, s1_eq = _stage(
            "1단계", [r"\hat{D}_i", r"=", r"\hat{\alpha}_0 +", r"\hat{\alpha}_1 Z_i"], TEAL_MAIN, WHITE)
        s1_eq[0].set_color(TEAL_MAIN)  # D̂
        stage1 = VGroup(s1_box, s1_lab, s1_eq).move_to(UP * 2.0)
        s2d_box, s2d_lab, s2d_eq = _stage(
            "2단계", [r"Y_i =", r"\hat{\beta}_0 +", r"\hat{\beta}_1", r"\hat{D}_i"], GRAY_MID, GRAY_MID)
        stage2_dim = VGroup(s2d_box, s2d_lab, s2d_eq).move_to(DOWN * 0.1).set_opacity(0.4)
        flow_arrow = Arrow(stage1.get_bottom(), stage2_dim.get_top(), buff=0.12,
                           stroke_width=2.8, color=TEAL_MAIN, max_tip_length_to_length_ratio=0.28)
        flow_lbl = MathTex(r"\hat{D}", font_size=30).set_color(TEAL_MAIN).next_to(flow_arrow, RIGHT, buff=0.2)
        cap1 = VGroup(
            Text("자격 Z로 처치의 외생적 부분만 예측", font=FONT, font_size=19, color=TEAL_MAIN),
            MathTex(r"\rightarrow \hat{D}", font_size=26).set_color(TEAL_MAIN),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 1.75)
        self.play(
            FadeOut(VGroup(chain_grp, nameZ, nameD, fuzzy_title, fuzzy_cap), run_time=0.4),
            FadeIn(stage1, shift=UP * 0.1, run_time=0.5),
            FadeIn(stage2_dim, run_time=0.5),
            GrowArrow(flow_arrow, run_time=0.5),
            FadeIn(flow_lbl, run_time=0.4),
        )
        self.play(FadeIn(cap1, run_time=0.4))
        self.wait(87.446 - 70.914 - 0.5 - 0.4)

        # ── Beat 8 (chunk8, 87.446→100.914) 2단계 (마지막·WAIT_TAIL) ──────
        # 1단계 카드 dim, 2단계 카드 활성화(β̂1 강조). D̂는 1단계와 같은 하늘색.
        # 결론 문장이 삭제되어 이 2단계가 마지막 Beat. β̂1=레이트로 마무리.
        s2a_box, s2a_lab, s2a_eq = _stage(
            "2단계", [r"Y_i =", r"\hat{\beta}_0 +", r"\hat{\beta}_1", r"\hat{D}_i"], GOLD_MAIN, WHITE)
        stage2_act = VGroup(s2a_box, s2a_lab, s2a_eq).move_to(DOWN * 0.1)
        s2a_eq[2].set_color(GOLD_MAIN)  # β̂1 강조
        s2a_eq[3].set_color(TEAL_MAIN)  # D̂ — 1단계 산출물과 같은 색
        beta_box = SurroundingRectangle(s2a_eq[2], color=GOLD_MAIN, buff=0.06,
                                        stroke_width=2.2, corner_radius=0.04)
        cap2 = MathTex(r"\hat{\beta}_1 = \text{LATE}", font_size=34).set_color(GOLD_MAIN).move_to(DOWN * 1.75)
        self.play(
            stage1.animate.set_opacity(0.4),
            FadeOut(stage2_dim, run_time=0.3),
            FadeIn(stage2_act, run_time=0.5),
            FadeOut(cap1, run_time=0.3),
            FadeIn(cap2, run_time=0.5),
        )
        self.play(Create(beta_box, run_time=0.4))
        # 마지막 Beat — WAIT_TAIL로 오디오 끝까지 2단계 카드 유지.
        # WAIT_TAIL = (101.187 + 0.4) - 87.446 - 0.5 - 0.4 = 13.241
        self.wait(13.241)

    # ── helper: 의료급여 아이콘 다이어그램 ──────────────────────
    def _medical_eg_diagram(self) -> VGroup:
        from pathlib import Path
        import numpy as np
        ICONS = Path(__file__).parent.parent.parent / "assets" / "tabler-icons" / "icons" / "outline"

        def ico(name, color, h=0.9):
            o = SVGMobject(str(ICONS / name), height=h)
            o.set_stroke(color=color, width=2.2, family=True).set_fill(opacity=0)
            return o

        # 1) 소득 낮음
        ic_coin = ico("coins.svg", TEAL_MAIN).move_to(np.array([-4.5, 0.3, 0]))
        ic_user = ico("user-dollar.svg", TEAL_MAIN, 0.7).move_to(np.array([-4.5, -0.8, 0]))
        lb_coin = Text("소득 기준선 이하", font=FONT, font_size=14, color=TEAL_MAIN).next_to(ic_coin, DOWN, buff=0.05)

        # 2) 자격 발생 (Z=1)
        ic_cert = ico("certificate.svg", GOLD_MAIN).move_to(np.array([-0.5, 0.3, 0]))
        lb_cert = Text("자격 발생  Z = 1", font=FONT, font_size=14, color=GOLD_MAIN).next_to(ic_cert, DOWN, buff=0.05)

        a1 = Arrow(np.array([-3.5, 0.3, 0]), np.array([-1.6, 0.3, 0]), buff=0,
                   stroke_width=2.5, color=TEAL_MAIN, max_tip_length_to_length_ratio=0.2)

        # 3) 분기: 실제 수급(D) 불확실
        q = Text("?", font=FONT, font_size=30, color=RED_MAIN).move_to(np.array([1.6, 0.3, 0]))
        a_fork = Arrow(np.array([0.55, 0.3, 0]), np.array([1.3, 0.3, 0]), buff=0,
                       stroke_width=2.0, color=GRAY_MID, max_tip_length_to_length_ratio=0.3)

        # 수급 O
        ic_check = ico("user-check.svg", GREEN_MAIN, 0.75).move_to(np.array([4.0, 1.0, 0]))
        ic_hosp  = ico("building-hospital.svg", GREEN_MAIN, 0.65).move_to(np.array([5.2, 1.0, 0]))
        lb_recv  = Text("D=1  수급", font=FONT, font_size=14, color=GREEN_MAIN).move_to(np.array([4.6, 0.2, 0]))

        # 수급 X
        ic_cancel = ico("user-cancel.svg", RED_MAIN, 0.75).move_to(np.array([4.0, -0.8, 0]))
        ic_ban    = ico("ban.svg", RED_MAIN, 0.65).move_to(np.array([5.2, -0.8, 0]))
        lb_nrecv  = Text("D=0  미수급", font=FONT, font_size=14, color=RED_MAIN).move_to(np.array([4.6, -1.6, 0]))

        a_up = Arrow(np.array([1.9, 0.5, 0]), np.array([3.5, 1.0, 0]), buff=0,
                     stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        a_dn = Arrow(np.array([1.9, 0.1, 0]), np.array([3.5, -0.8, 0]), buff=0,
                     stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.25)

        note = Text("자격 있어도 미신청·자격 없어도 다른 경로 수급 가능",
                    font=FONT, font_size=14, color=GRAY_MID).move_to(np.array([0.0, -2.1, 0]))

        return VGroup(ic_coin, ic_user, lb_coin, ic_cert, lb_cert, a1,
                      q, a_fork, a_up, a_dn,
                      ic_check, ic_hosp, lb_recv,
                      ic_cancel, ic_ban, lb_nrecv,
                      note)

    # ── helper: 수급자 vs 비수급자 선택 편향 ─────────────────────
    def _bias_diagram(self) -> VGroup:
        from pathlib import Path
        import numpy as np
        ICONS = Path(__file__).parent.parent.parent / "assets" / "tabler-icons" / "icons" / "outline"

        def ico(name, color, h=0.72):
            o = SVGMobject(str(ICONS / name), height=h)
            o.set_stroke(color=color, width=2.2, family=True).set_fill(opacity=0)
            return o

        # ── Left: 수급자 (D=1) ─────────────────────────────
        lbl_l = Text("수급자  D = 1", font=FONT, font_size=18, color=RED_MAIN).move_to(np.array([-3.4, 2.5, 0]))
        u_l   = ico("user.svg", RED_MAIN, 0.85).move_to(np.array([-4.5, 1.4, 0]))
        dn_l  = ico("trending-down.svg", RED_MAIN, 0.65).move_to(np.array([-2.8, 1.7, 0]))
        sd_l  = ico("mood-sad.svg", RED_MAIN, 0.72).move_to(np.array([-4.5, 0.1, 0]))
        hb_l  = ico("heartbeat.svg", RED_MAIN, 0.6).move_to(np.array([-2.8, 0.4, 0]))
        t_dn  = Text("소득 낮음", font=FONT, font_size=14, color=RED_MAIN).next_to(dn_l, DOWN, buff=0.08)
        t_sd  = Text("건강 나쁨", font=FONT, font_size=14, color=RED_MAIN).next_to(sd_l, DOWN, buff=0.08)
        t_hb  = Text("(원래부터)", font=FONT, font_size=13, color=RED_MAIN).next_to(hb_l, DOWN, buff=0.08)

        # ── Right: 비수급자 (D=0) ─────────────────────────────
        lbl_r = Text("비수급자  D = 0", font=FONT, font_size=18, color=GREEN_MAIN).move_to(np.array([3.4, 2.5, 0]))
        u_r   = ico("user.svg", GREEN_MAIN, 0.85).move_to(np.array([2.2, 1.4, 0]))
        up_r  = ico("trending-up.svg", GREEN_MAIN, 0.65).move_to(np.array([3.8, 1.7, 0]))
        hp_r  = ico("mood-happy.svg", GREEN_MAIN, 0.72).move_to(np.array([2.2, 0.1, 0]))
        ht_r  = ico("heart.svg", GREEN_MAIN, 0.6).move_to(np.array([3.8, 0.4, 0]))
        t_up  = Text("소득 높음", font=FONT, font_size=14, color=GREEN_MAIN).next_to(up_r, DOWN, buff=0.08)
        t_hp  = Text("건강 좋음", font=FONT, font_size=14, color=GREEN_MAIN).next_to(hp_r, DOWN, buff=0.08)
        t_ht  = Text("(원래부터)", font=FONT, font_size=13, color=GREEN_MAIN).next_to(ht_r, DOWN, buff=0.08)

        sep  = DashedLine(UP * 3.0, DOWN * 0.5, color=GRAY_MID, stroke_width=0.9)
        warn = Text("단순 비교 → 의료급여 효과인지, 원래 달랐기 때문인지 구분 불가",
                    font=FONT, font_size=15, color=RED_MAIN).move_to(np.array([0.0, -1.4, 0]))

        return VGroup(lbl_l, u_l, dn_l, sd_l, hb_l, t_dn, t_sd, t_hb,
                      lbl_r, u_r, up_r, hp_r, ht_r, t_up, t_hp, t_ht,
                      sep, warn)

    # ── helper: 내생성 DAG ───────────────────────────────────────
    def _endogeneity_dag(self) -> VGroup:
        from pathlib import Path
        import numpy as np
        ICONS = Path(__file__).parent.parent.parent / "assets" / "tabler-icons" / "icons" / "outline"

        def ico(name, color, h=0.5):
            o = SVGMobject(str(ICONS / name), height=h)
            o.set_stroke(color=color, width=2.0, family=True).set_fill(opacity=0)
            return o

        pu = np.array([0.0, 1.2, 0])
        pd = np.array([-3.0, -0.9, 0])
        py = np.array([3.0, -0.9, 0])
        r  = 0.58

        def node(pos, label, color):
            c = Circle(radius=r, color=color, stroke_width=2.5).move_to(pos)
            t = Text(label, font=FONT, font_size=22, color=color).move_to(pos)
            return VGroup(c, t)

        nu = node(pu, "U", GRAY_MID)
        nd = node(pd, "D", TEAL_MAIN)
        ny = node(py, "Y", WHITE)

        # 각 노드에 아이콘 추가 (노드 바깥 근처)
        ic_u = ico("user-dollar.svg", GRAY_MID, 0.52).next_to(nu, RIGHT, buff=0.7)
        ic_d = ico("pill.svg", TEAL_MAIN, 0.52).next_to(nd, LEFT, buff=0.7)
        ic_y = ico("heart.svg", WHITE, 0.52).next_to(ny, RIGHT, buff=0.7)

        lu = VGroup(
            Text("교란 요인 U", font=FONT, font_size=14, color=GRAY_MID),
            Text("소득·건강 기초 상태", font=FONT, font_size=13, color=GRAY_MID),
        ).arrange(DOWN, buff=0.05).next_to(nu, UP, buff=0.12)
        ld = VGroup(
            Text("처치 D", font=FONT, font_size=14, color=TEAL_MAIN),
            Text("의료급여 수급", font=FONT, font_size=13, color=TEAL_MAIN),
        ).arrange(DOWN, buff=0.05).next_to(nd, DOWN, buff=0.12)
        ly = VGroup(
            Text("결과 Y", font=FONT, font_size=14, color=WHITE),
            Text("건강 개선", font=FONT, font_size=13, color=WHITE),
        ).arrange(DOWN, buff=0.05).next_to(ny, DOWN, buff=0.12)

        def edge_pt(frm, to, rad):
            d = to - frm
            d = d / np.linalg.norm(d)
            return frm + rad * d, to - rad * d

        s_ud, e_ud = edge_pt(pu, pd, r)
        s_uy, e_uy = edge_pt(pu, py, r)
        s_dy, e_dy = edge_pt(pd, py, r)

        aUD = Arrow(s_ud, e_ud, buff=0, stroke_width=2.5, color=RED_MAIN, max_tip_length_to_length_ratio=0.2)
        aUY = Arrow(s_uy, e_uy, buff=0, stroke_width=2.5, color=RED_MAIN, max_tip_length_to_length_ratio=0.2)
        aDY = Arrow(s_dy, e_dy, buff=0, stroke_width=2.5, color=TEAL_MAIN, max_tip_length_to_length_ratio=0.2)

        conf = Text("편향 유발", font=FONT, font_size=14, color=RED_MAIN).move_to(np.array([-1.8, 0.35, 0]))
        want = Text("추정하고 싶은 인과 효과", font=FONT, font_size=14, color=TEAL_MAIN).move_to(np.array([0.0, -1.6, 0]))

        # 내생성 설명 박스
        expl = VGroup(
            Text("내생성:", font=FONT, font_size=15, color=RED_MAIN),
            Text("D가 U와 뒤엉켜 있어 단순 회귀 결과에 편향 발생", font=FONT, font_size=14, color=WHITE),
        ).arrange(RIGHT, buff=0.15).move_to(np.array([0.0, -2.5, 0]))

        return VGroup(nu, nd, ny, ic_u, ic_d, ic_y,
                      lu, ld, ly, aUD, aUY, aDY,
                      conf, want, expl)

    # ── helper: 표 한 행 ─────────────────────────────────────────
    def _reg_row(self, name, path_tex, role, y, header=False) -> VGroup:
        import numpy as np
        if header:
            n = Text(name, font=FONT, font_size=22, color=GRAY_MID).move_to(np.array([-4.7, y, 0]), aligned_edge=LEFT)
            p = Text("경로", font=FONT, font_size=22, color=GRAY_MID).move_to(np.array([0.2, y, 0]))
            r = Text(role, font=FONT, font_size=22, color=GRAY_MID).move_to(np.array([3.7, y, 0]))
        else:
            n = Text(name, font=FONT, font_size=24, color=WHITE).move_to(np.array([-4.7, y, 0]), aligned_edge=LEFT)
            p = MathTex(path_tex, font_size=34).set_color(TEAL_MAIN).move_to(np.array([0.2, y, 0]))
            r = Text(role, font=FONT, font_size=22, color=GOLD_MAIN).move_to(np.array([3.7, y, 0]))
        return VGroup(n, p, r)


class Scene07Recap(Scene):
    """
    Scene 07: recap  (구 07_visualization + 08_examples + 09_outro 통합·간략화)
    스크립트: src/scripts/07_recap.txt (메디케어·장학금 예시 모두 삭제, 3문단으로 재압축 — 2026-07-21 개정)
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
