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


class Scene02Variables(Scene):
    """
    Scene 02: variables  (ipynb §1 "Fuzzy RDD란?")
    스크립트: narration/02_variables.txt
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
