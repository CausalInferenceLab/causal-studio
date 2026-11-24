from manim import *

from fuzzy_rdd_common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


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
        fraction_template = TexTemplate()
        fraction_template.add_to_preamble(r"\usepackage{xcolor}")
        numerator = rf"\textcolor[HTML]{{{TEAL_MAIN[1:]}}}{{\Delta Y}}"
        denominator = rf"\textcolor[HTML]{{{GOLD_MAIN[1:]}}}{{\Delta D}}"
        frac = MathTex(rf"\frac{{{numerator}}}{{{denominator}}}", font_size=46,
                       tex_template=fraction_template).move_to(np.array([2.15, 0.35, 0]))
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
