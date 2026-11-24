from pathlib import Path
from manim import *

TEAL_NODE   = "#4DD0C4"
YELLOW_NODE = "#C8A630"
GREY_NODE   = "#AAAAAA"
ASSET_DIR   = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"


def make_node(pos, color, label_str, r=0.52):
    c = Circle(
        radius=r,
        stroke_color=color,
        stroke_width=4,
        fill_color=color,
        fill_opacity=0.18,
    ).move_to(pos)
    lbl = Tex(label_str, font_size=56, color=color).move_to(pos)
    return VGroup(c, lbl)


class Thumbnail(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # ── 노드 위치 ──────────────────────────────────────────
        z_pos = LEFT * 3.5 + UP * 1.8
        x_pos = LEFT * 5.5 + DOWN * 1.2
        y_pos = LEFT * 1.5 + DOWN * 1.2

        z_node = make_node(z_pos, GREY_NODE,   r"$Z$")
        x_node = make_node(x_pos, TEAL_NODE,   r"$X$")
        y_node = make_node(y_pos, YELLOW_NODE, r"$Y$")

        # ── 화살표 ─────────────────────────────────────────────
        # Z → X (회색, 얇음)
        z_to_x = Arrow(
            z_node.get_center(), x_node.get_center(),
            stroke_width=3.5, color=GREY_NODE, buff=0.54,
            tip_length=0.22,
        )
        # Z → Y (회색, 얇음)
        z_to_y = Arrow(
            z_node.get_center(), y_node.get_center(),
            stroke_width=3.5, color=GREY_NODE, buff=0.54,
            tip_length=0.22,
        )
        # X → Y (핵심 인과, 굵음)
        x_to_y = Arrow(
            x_node.get_center(), y_node.get_center(),
            stroke_width=6, color=TEAL_NODE, buff=0.54,
            tip_length=0.28,
        )

        # ── 노드 아래 라벨 ─────────────────────────────────────
        z_lbl = Tex(r"\small Confounder", font_size=28, color=GREY_NODE)
        z_lbl.next_to(z_node, UP, buff=0.18)
        x_lbl = Tex(r"\small Treatment", font_size=28, color=TEAL_NODE)
        x_lbl.next_to(x_node, DOWN, buff=0.2)
        y_lbl = Tex(r"\small Outcome", font_size=28, color=YELLOW_NODE)
        y_lbl.next_to(y_node, DOWN, buff=0.2)

        # ── 제목 (오른쪽, 3b1b CM 세리프) ─────────────────────
        title = VGroup(
            Tex(r"\textbf{Why}", font_size=148, color=WHITE),
            Tex(r"\textbf{Causal}", font_size=148, color=WHITE),
            Tex(r"\textbf{Inference?}", font_size=108, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        title.move_to(RIGHT * 2.8 + UP * 0.15)

        # ── 조립 ───────────────────────────────────────────────
        self.add(z_to_x, z_to_y, x_to_y)
        self.add(x_node, y_node, z_node)
        self.add(z_lbl, x_lbl, y_lbl)
        self.add(title)
        # 출력: build/thumbnail.png  (manim -s → build/manim/images/thumbnail/ 후 복사)
