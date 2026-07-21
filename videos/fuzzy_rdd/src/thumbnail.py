from manim import *
import numpy as np

BG     = "#080E18"
C_RED  = "#FF5C5C"
C_BLUE = "#00BFFF"
C_GOLD = "#FFD700"
WHITE  = "#FFFFFF"
FONT   = "Apple SD Gothic Neo"


def _build_scene(scene, cx, y_lo, y_hi, title_lines):
    """
    Sharp RDD 썸네일(videos/rdd/src/thumbnail.py)의 시각 문법을 그대로 물려받되,
    Fuzzy RDD의 핵심 차이 두 가지를 추가한다.
      1) 완만한 기울기: Sharp는 좌우 라인이 완전히 수평(flat)인 계단함수였다면,
         Fuzzy는 컷오프 폭(y_lo/y_hi, Sharp와 동일)은 유지한 채 두 라인 각각에
         약간의 우상향 기울기를 준다. 완전히 평평한 계단이 아니라 "추세선 위에
         불연속이 얹힌" 진짜 RDD 플롯처럼 보이게 하는 것이 포인트.
         (사용자 피드백: "폭이 줄어드는 게 아니라 약간의 기울기가 있는 게 포인트")
      2) 규정 위반자(non-compliers) 표현: 컷오프 양옆에 반대 색 stray dot을 각 2개씩 얹어,
         "왼쪽인데 파랑(처치)", "오른쪽인데 빨강(미처치)"이 섞여 있음을 보여준다.
         Sharp 썸네일엔 없는 요소 — 이게 Fuzzy와 Sharp를 한눈에 구분 짓는 지점.
    """
    scene.camera.background_color = BG

    band = Rectangle(
        width=1.0, height=9.2,
        fill_color=C_GOLD, fill_opacity=0.07, stroke_width=0,
    ).move_to([cx, 0, 0])

    def h_glow_line(p0, p1, color):
        return VGroup(
            Line(p0, p1, color=color, stroke_width=55, stroke_opacity=0.05),
            Line(p0, p1, color=color, stroke_width=22, stroke_opacity=0.14),
            Line(p0, p1, color=color, stroke_width=8,  stroke_opacity=0.50),
            Line(p0, p1, color=color, stroke_width=3.5, stroke_opacity=1.0),
        )

    # 왼쪽 라인: x=-8.5 → cx까지, y가 (y_lo-LEFT_RISE)에서 y_lo로 완만히 상승
    # 오른쪽 라인: x=cx → 8.5까지, y가 y_hi에서 (y_hi+RIGHT_RISE)로 완만히 상승
    # 컷오프(x=cx)에서는 여전히 y_lo→y_hi 수직 점프가 존재 (점프 폭 자체는 Sharp와 동일)
    X0, X1 = -8.5, 8.5
    LEFT_RISE, RIGHT_RISE = 0.9, 0.6

    def left_y(x):
        return y_lo - LEFT_RISE + LEFT_RISE * (x - X0) / (cx - X0)

    def right_y(x):
        return y_hi + RIGHT_RISE * (x - cx) / (X1 - cx)

    left_line  = h_glow_line([X0, left_y(X0), 0], [cx, y_lo, 0], C_RED)
    right_line = h_glow_line([cx, y_hi, 0], [X1, right_y(X1), 0], C_BLUE)

    dot_lo = VGroup(
        Dot([cx, y_lo, 0], color=C_RED,  radius=0.36, fill_opacity=0.15),
        Dot([cx, y_lo, 0], color=C_RED,  radius=0.20, fill_opacity=1.0),
    )
    dot_hi = VGroup(
        Dot([cx, y_hi, 0], color=C_BLUE, radius=0.36, fill_opacity=0.15),
        Dot([cx, y_hi, 0], color=C_BLUE, radius=0.20, fill_opacity=1.0),
    )

    # ── 산포(scatter) stray dot ──────────────────────────────────────
    # 각 라인과 같은 색으로, 라인에서 살짝 벗어난 점들을 흩뿌려 "깔끔한 계단이 아니라
    # 노이즈가 있는 실제 데이터"라는 fuzzy한 느낌을 준다. (이전엔 반대색으로 비순응자를
    # 표현했지만, 썸네일에서 한눈에 읽히지 않아 같은 색 산포로 단순화)
    # 라인이 기울어졌으므로, 각 stray dot은 그 x위치에서의 라인 높이(left_y/right_y)를
    # 기준으로 띄운다 — 그래야 기울어진 라인에서 자연스럽게 튀어나온 것처럼 보인다.
    def stray(x, y, color):
        return VGroup(
            Dot([x, y, 0], color=color, radius=0.22, fill_opacity=0.15),
            Dot([x, y, 0], color=color, radius=0.13, fill_opacity=1.0),
        )
    strays = VGroup(
        stray(cx - 1.7, left_y(cx - 1.7) + 0.42, C_RED),
        stray(cx - 3.6, left_y(cx - 3.6) - 0.30, C_RED),
        stray(cx + 1.7, right_y(cx + 1.7) - 0.42, C_BLUE),
        stray(cx + 3.6, right_y(cx + 3.6) + 0.30, C_BLUE),
    )

    cutoff_glow = Line([cx, -4.8, 0], [cx, 4.8, 0],
                       color=C_GOLD, stroke_width=18, stroke_opacity=0.10)
    cutoff_line = DashedLine([cx, -4.8, 0], [cx, 4.8, 0],
                             color=C_GOLD, stroke_width=2.5, stroke_opacity=0.85,
                             dash_length=0.22)

    p_lo = [cx, y_lo + 0.22, 0]
    p_hi = [cx, y_hi - 0.22, 0]
    jump = VGroup(
        DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                    stroke_width=60, stroke_opacity=0.06, tip_length=0.5),
        DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                    stroke_width=24, stroke_opacity=0.18, tip_length=0.5),
        DoubleArrow(p_lo, p_hi, color=C_GOLD, buff=0,
                    stroke_width=8,  stroke_opacity=1.0,  tip_length=0.5),
    )

    tau = MathTex(r"\hat{\tau}", font_size=88, color=C_GOLD)
    tau.move_to([cx + 1.5, (y_lo + y_hi) / 2, 0])

    text_grp = VGroup(*title_lines).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    text_grp.to_corner(UL, buff=0.44).shift(RIGHT * 1.0 + DOWN * 0.6)

    scene.add(band, left_line, right_line,
              cutoff_glow, cutoff_line,
              dot_lo, dot_hi, strays, jump, tau,
              text_grp)
    scene.wait(0.1)


class ThumbnailFuzzyRDDKorean(Scene):
    """
    Fuzzy RDD 썸네일 (한국어) — Sharp RDD 썸네일과 짝을 이루는 시리즈 썸네일.
    manim -s --resolution 1920,1080 --media_dir build/manim src/thumbnail.py ThumbnailFuzzyRDDKorean
    """

    def construct(self):
        _build_scene(
            self, cx=2.8, y_lo=-2.0, y_hi=1.5,
            title_lines=[
                Text("Fuzzy RDD", font=FONT, font_size=105, color=WHITE, weight=BOLD),
                Text("Fuzzy Regression Discontinuity Design",
                     font=FONT, font_size=28, color=WHITE, weight=BOLD),
                Text("퍼지 회귀 불연속 설계", font=FONT, font_size=32, color=C_BLUE, weight=BOLD),
            ],
        )


class ThumbnailFuzzyRDDEnglish(Scene):
    """
    Fuzzy RDD 썸네일 (영어)
    manim -s --resolution 1920,1080 --media_dir build/manim src/thumbnail.py ThumbnailFuzzyRDDEnglish
    """

    def construct(self):
        _build_scene(
            self, cx=2.8, y_lo=-2.0, y_hi=1.5,
            title_lines=[
                Text("Fuzzy RDD", font=FONT, font_size=105, color=WHITE, weight=BOLD),
                Text("Fuzzy Regression Discontinuity Design",
                     font=FONT, font_size=32, color=C_BLUE, weight=BOLD),
            ],
        )
