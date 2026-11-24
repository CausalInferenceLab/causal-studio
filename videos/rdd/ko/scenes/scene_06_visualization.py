from manim import *

from videos.rdd.shared.common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene06Visualization(Scene):
    """
    Scene 06: visualization
    스크립트: videos/rdd/ko/narration/06_visualization.txt
    build/audio/06_visualization.timings.json 기준 타이밍 (총 76.72s)

    Beat1 chunk1  ( 0.00~ 4.23s)  타이틀: RDD 시각화
    Beat2 chunk2  ( 4.23~10.59s)  세 가지 정보 소개 (산점도·회귀선·불연속 점프구간)
    Beat3 chunk3  (10.59~19.13s)  산점도 등장 (처치/미처치 색 구분)
    Beat4 chunk4  (19.13~26.56s)  회귀선 등장 (좌·우 독립 추정)
    Beat5 chunk5  (26.56~35.06s)  점프 강조 → 처치 효과
    Beat6 chunk6  (35.06~45.37s)  핵심 확인 + 주의사항 예고 (10.31s)
    Beat7 chunk7  (45.37~61.16s)  기준점 근방만 인과 해석 가능 (15.79s)
    Beat8 chunk8  (61.16~76.44s)  좌우 기울기 달라도 무방 (15.28s)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~4.23s) ────────────────────────
        # 새로 등장: 타이틀 2줄
        # 핵심 시선: "RDD 시각화"
        # 지워질 요소: FadeOut → Beat2
        title = VGroup(
            Text("RDD 시각화", font=FONT, font_size=44, color=WHITE),
            Text("그래프로 직관적으로 이해하기", font=FONT, font_size=26, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.6)
        self.wait(2.33)
        self.play(FadeOut(title), run_time=0.5)  # chunk1 end ~4.23s

        # ── Beat 2 (chunk2: 4.23~10.59s) ────────────────────
        # 새로 등장: 세 가지 정보 헤더 + 칩 3개 순차 등장
        # 핵심 시선: 산점도·회귀선·불연속 점프구간 세 키워드
        # 지워질 요소: FadeOut → Beat3
        info_header = Text("세 가지 정보", font=FONT, font_size=34, color=WHITE).move_to(UP * 1.3)
        chips = VGroup(
            self._chip("① 산점도", GRAY_MID),
            self._chip("② 회귀선", BLUE_MAIN),
            self._chip("③ 불연속 점프구간", YELLOW_MAIN),
        ).arrange(DOWN, buff=0.35).next_to(info_header, DOWN, buff=0.5)

        self.play(FadeIn(info_header, shift=DOWN * 0.2), run_time=0.6)
        for chip in chips:
            self.play(FadeIn(chip, shift=RIGHT * 0.2), run_time=0.45)
        self.wait(4.0)
        self.play(FadeOut(VGroup(info_header, chips)), run_time=0.5)  # chunk2 end ~10.59s

        # ── 공통 그래프 구성 (Beat3~8 유지) ─────────────────
        # x축: 수능 점수 340~400점, cutoff=370점
        axes = Axes(
            x_range=[340, 401, 10], y_range=[1.5, 4.5, 0.5],
            x_length=8.0, y_length=4.5,
            axis_config={
                "color": GRAY_MID, "stroke_width": 1.2,
                "include_tip": True, "tip_width": 0.12, "tip_height": 0.12,
            },
            x_axis_config={"numbers_to_include": [340, 360, 380, 400]},
            y_axis_config={"numbers_to_include": [2.0, 2.5, 3.0, 3.5, 4.0]},
        ).move_to(RIGHT * 0.3 + UP * 0.4)

        # Y축 레이블: 회전 없이 숫자 왼쪽에 수평 배치
        y_lbl = Text("성적(GPA)", font=FONT, font_size=12, color=GRAY_MID)
        y_lbl.next_to(axes, LEFT, buff=0.1)

        # X축 레이블: 축 아래 중앙
        x_lbl = Text("수능 점수 (점)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_center(), DOWN, buff=0.55)

        cutoff_line = DashedLine(
            axes.c2p(370, 1.5), axes.c2p(370, 4.5),
            color=YELLOW_MAIN, stroke_width=2.5, dash_length=0.12,
        )
        cutoff_lbl = Text("Cutoff (370점)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
            axes.c2p(370, 4.5), UR, buff=0.05
        )

        rng = np.random.default_rng(42)
        xs_l = rng.uniform(342, 368, 40)
        ys_l = 2.0 + 0.015 * (xs_l - 370) + rng.normal(0, 0.22, 40)
        xs_r = rng.uniform(372, 398, 40)
        ys_r = 2.5 + 0.02 * (xs_r - 370) + rng.normal(0, 0.22, 40)

        scatter_left = VGroup(*[
            Dot(axes.c2p(x, y), color=RED_MAIN, radius=0.055, fill_opacity=0.75)
            for x, y in zip(xs_l, ys_l) if 1.5 <= y <= 4.5
        ])
        scatter_right = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE_MAIN, radius=0.055, fill_opacity=0.75)
            for x, y in zip(xs_r, ys_r) if 1.5 <= y <= 4.5
        ])

        legend = VGroup(
            VGroup(
                Dot(color=RED_MAIN, radius=0.09),
                Text("미수혜 (<370점)", font=FONT, font_size=16, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Dot(color=BLUE_MAIN, radius=0.09),
                Text("수혜 (≥370점)", font=FONT, font_size=16, color=BLUE_MAIN),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend.move_to(axes.get_corner(UR) + LEFT * 1.6 + DOWN * 0.4)

        # ── Beat 3 (chunk3: 10.59~19.13s) ───────────────────
        # 새로 등장: 축·컷오프·산점도·범례
        # 핵심 시선: 색으로 구분된 두 집단 점들
        # 지워질 요소: 없음 → Beat4에서 회귀선 추가
        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=0.8)
        self.play(Create(cutoff_line), FadeIn(cutoff_lbl), run_time=0.5)
        self.play(FadeIn(scatter_left), run_time=0.7)
        self.play(FadeIn(scatter_right), run_time=0.7)
        self.play(FadeIn(legend), run_time=0.6)
        self.wait(5.84)  # chunk3 end ~19.13s

        # ── Beat 4 (chunk4: 19.13~26.56s) ───────────────────
        # 남는 요소: 축·산점도·범례
        # 새로 등장: 좌우 회귀선 + 하단 설명
        # 핵심 시선: 기준점 좌·우 각각의 독립 회귀선
        # 지워질 요소: reg_desc FadeOut → Beat5
        left_line = axes.plot(
            lambda x: 2.0 + 0.015 * (x - 370), x_range=[340, 370],
            color=RED_MAIN, stroke_width=4.5,
        )
        right_line = axes.plot(
            lambda x: 2.5 + 0.02 * (x - 370), x_range=[370, 400],
            color=BLUE_MAIN, stroke_width=4.5,
        )
        reg_desc = Text(
            "기준점 좌·우에 각각 독립적으로 적합된 회귀선",
            font=FONT, font_size=19, color=WHITE,
        ).move_to(DOWN * 3.0)

        self.play(Create(left_line), run_time=0.8)
        self.play(Create(right_line), run_time=0.8)
        self.play(FadeIn(reg_desc), run_time=0.5)
        self.wait(4.53)  # chunk4 end ~26.56s
        self.play(FadeOut(reg_desc), run_time=0.4)

        # ── Beat 5 (chunk5: 26.56~35.06s) ───────────────────
        # 남는 요소: 축·산점도·범례·회귀선
        # 새로 등장: 점프 화살표 + 처치효과 레이블(MathTex τ̂) + 하단 설명
        # 핵심 시선: 기준점 370에서의 수직 점프 = τ̂
        # 지워질 요소: jump_desc FadeOut → Beat6
        jump_arrow = DoubleArrow(
            axes.c2p(370, 2.05), axes.c2p(370, 2.45),
            color=YELLOW_MAIN, buff=0, stroke_width=4, tip_length=0.18,
        )
        # τ̂ hat 렌더링: Text에서 MathTex 분리로 정확하게 표시
        jump_lbl = VGroup(
            Text("처치 효과 ", font=FONT, font_size=17, color=YELLOW_MAIN),
            MathTex(r"\hat{\tau}", font_size=22, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.08).next_to(jump_arrow, RIGHT, buff=0.15)

        jump_desc = Text(
            "두 회귀선의 절편 차이 = 처치 효과 추정량",
            font=FONT, font_size=19, color=YELLOW_MAIN,
        ).move_to(DOWN * 3.0)

        self.play(Create(jump_arrow), FadeIn(jump_lbl), run_time=0.8)
        self.play(FadeIn(jump_desc), run_time=0.5)
        self.wait(6.8)  # chunk5 end ~35.06s
        self.play(FadeOut(jump_desc), run_time=0.4)

        # ── Beat 6 (chunk6: 35.06~45.37s, 10.31s) ───────────
        # 남는 요소: 축·산점도·범례·회귀선·점프 화살표
        # 새로 등장: 주의 예고 문구 (하단)
        # 핵심 시선: "하지만 주의해야 할 것들이 있습니다"
        # 지워질 요소: caution_hint + jump 관련 → Beat7
        caution_hint = Text(
            "그래프를 볼 때 주의할 것들이 있습니다",
            font=FONT, font_size=20, color=YELLOW_MAIN,
        ).move_to(DOWN * 3.0)

        self.play(FadeIn(caution_hint, shift=UP * 0.15), run_time=0.6)
        self.wait(9.21)  # chunk6 end ~45.37s
        self.play(FadeOut(VGroup(caution_hint, jump_arrow, jump_lbl)), run_time=0.5)

        # ── Beat 7 (chunk7: 45.37~61.16s, 15.79s) ───────────
        # 남는 요소: 축·산점도·범례·회귀선
        # 새로 등장: 근방 강조 구간(초록, 365~375점) + 인과 해석 경고
        # 핵심 시선: 초록 구간 = 인과 해석 가능 / 원거리 점들 = 주의
        # 지워질 요소: near_region·near_lbl·caution_desc → Beat8
        r_l = axes.c2p(365, 1.5)
        r_r = axes.c2p(375, 4.5)
        near_w = r_r[0] - r_l[0]
        near_h = r_r[1] - r_l[1]
        near_cx = (r_l[0] + r_r[0]) / 2
        near_cy = (r_l[1] + r_r[1]) / 2

        near_region = Rectangle(
            width=near_w, height=near_h,
            fill_color=GREEN_MAIN, fill_opacity=0.14,
            stroke_color=GREEN_MAIN, stroke_width=1.8,
        ).move_to([near_cx, near_cy, 0])
        near_lbl = Text("인과 해석\n가능 구간", font=FONT, font_size=14, color=GREEN_MAIN).next_to(
            near_region, DOWN, buff=0.08
        )

        caution_desc = VGroup(
            Text("기준점 근방에서만 인과적 해석이 가능합니다", font=FONT, font_size=19, color=WHITE),
            Text("340점대·390점대 차이 → 장학금 효과가 아닌 능력 차이일 수 있음", font=FONT, font_size=17, color=RED_MAIN),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 3.0)

        self.play(FadeIn(near_region), FadeIn(near_lbl), run_time=0.7)
        self.play(FadeIn(caution_desc), run_time=0.6)
        self.wait(14.0)  # chunk7 end ~61.16s
        self.play(FadeOut(VGroup(near_region, near_lbl, caution_desc)), run_time=0.5)

        # ── Beat 8 (chunk8: 61.16~76.44s, 15.28s) ───────────
        # 남는 요소: 축·산점도·범례·회귀선
        # 새로 등장: 좌우 기울기 레이블 + 하단 설명
        # 핵심 시선: β₁ (미처치 기울기) vs β₁+β₃ (처치 기울기)
        slope_l_lbl = VGroup(
            Text("기울기: ", font=FONT, font_size=15, color=RED_MAIN),
            MathTex(r"\beta_1", font_size=20, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.08).move_to(axes.c2p(350, 2.0 + 0.015 * (350 - 370) + 0.45))

        slope_r_lbl = VGroup(
            Text("기울기: ", font=FONT, font_size=15, color=BLUE_MAIN),
            MathTex(r"\beta_1 + \beta_3", font_size=20, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.08).move_to(axes.c2p(390, 2.5 + 0.02 * (390 - 370) + 0.48))

        slope_note = VGroup(
            Text("좌우 회귀선의 기울기가 달라도 됩니다", font=FONT, font_size=20, color=BLUE_MAIN),
            Text("처치 여부에 따라 성적 향상 경향이 다를 수 있습니다", font=FONT, font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 3.0)

        self.play(FadeIn(slope_l_lbl), FadeIn(slope_r_lbl), run_time=0.7)
        self.play(FadeIn(slope_note), run_time=0.6)
        self.wait(13.98)  # chunk8 end ~76.44s + tail

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _chip(self, label: str, color: str) -> VGroup:
        bg = RoundedRectangle(
            corner_radius=0.18, width=4.2, height=0.65,
            fill_color=color, fill_opacity=0.12,
            stroke_color=color, stroke_width=1.8,
        )
        txt = Text(label, font=FONT, font_size=22, color=color)
        txt.move_to(bg.get_center())
        return VGroup(bg, txt)
