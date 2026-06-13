from manim import *

# what_is_ipw 유튜브 썸네일 (1920×1080)
# 컨셉: 동그라미(환자)로 '서로 다르던 두 그룹이 IPW로 똑같이 균형 맞춰진다'만 강조.
# 디자인: 점 격자를 45도 기울인 다이아몬드 배치로 감각 있게.

SEVERE = "#b07cff"  # 중증
MILD = "#39d98a"    # 경증
ORG = "#F5A623"
GOOD = "#7CE38B"
GOLD = "#F4C95D"


class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        def cluster(n_p, n_g, cols, r=0.16, buff=0.14):
            g = VGroup(*[Dot(color=SEVERE, radius=r) for _ in range(n_p)],
                       *[Dot(color=MILD, radius=r) for _ in range(n_g)])
            g.arrange_in_grid(cols=cols, buff=buff)
            g.rotate(45 * DEGREES)   # 45도 기울인 다이아몬드 배치
            return g

        # ===== 상단 타이틀 =====
        ipw = Tex(r"\textbf{IPW}", color=ORG).scale(2.4)
        ipw_en = Text("Inverse Probability Weighting", font_size=42, color=WHITE, weight=BOLD)
        title = VGroup(ipw, ipw_en).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.55)

        # ===== 위: 서로 다른 두 그룹 (작게, 흐리게) =====
        b0 = cluster(5, 2, 4, r=0.1, buff=0.1)
        c0 = cluster(1, 2, 3, r=0.1, buff=0.1)
        neq = Tex(r"$\neq$", color=GREY_B).scale(1.4)
        before = VGroup(b0, neq, c0).arrange(RIGHT, buff=0.55).set_opacity(0.55)
        before_grp = VGroup(before).arrange(DOWN, buff=0.3).move_to(UP * 1.35)

        # ===== IPW 화살표 =====
        arrow = Arrow(UP * 0.55, DOWN * 0.55, color=ORG, stroke_width=10,
                      max_tip_length_to_length_ratio=0.35).move_to(UP * 0.05)
        arrow_lbl = Text("IPW", font_size=34, color=ORG, weight=BOLD).next_to(arrow, RIGHT, buff=0.25)
        step = VGroup(arrow, arrow_lbl)

        # ===== 아래: 균형 맞춰진 두 그룹 (크게, 강조) =====
        b1 = cluster(6, 4, 5)
        c1 = cluster(6, 4, 5)
        eq = Tex(r"$=$", color=GOOD).scale(2.6)
        after = VGroup(b1, eq, c1).arrange(RIGHT, buff=0.9)
        glow = SurroundingRectangle(after, color=GOOD, stroke_width=3, corner_radius=0.25, buff=0.4)
        after_lbl = Text("Balance", font_size=40, color=GOOD, weight=BOLD)
        after_grp = VGroup(VGroup(after, glow), after_lbl).arrange(DOWN, buff=0.35).move_to(DOWN * 1.7)

        self.add(title, before_grp, step, after_grp)

