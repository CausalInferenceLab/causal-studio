# Manim Code Patterns

## Visual design and icons

### Reference study and adaptation

#### Find the passage and its source

- Search the 3Blue1Brown lesson catalog or channel for the relationship the viewer needs to see. Use the visual relationship in the query, such as `3Blue1Brown vector addition tip to tail` or `site:3blue1brown.com Gaussian surface slice`.
- Start from the official lesson's **Source** link. In `3b1b/`, use `rg -n` on the linked module for a distinctive label, scene name, or object from the passage. Match the code's visible objects and their order to the rendered sequence. Follow imported helpers and configuration when placement or styling lives outside the scene class.
  - For a distribution or a changing curve, pair the [central limit theorem lesson](https://www.3blue1brown.com/lessons/clt/) with [`TransitionToSkewDistribution`](https://github.com/3b1b/videos/blob/31f8ffe785e860477a6051fde983c02c7d165bc2/_2023/clt/main.py#L815). Track the same plotting region and transform the plotted objects and labels to their next values.
  - For proportions and conditional probabilities, pair the [Bayes' theorem lesson](https://www.3blue1brown.com/lessons/bayes-theorem/) with [`BayesDiagram.set_prior` and `general_set_likelihood`](https://github.com/3b1b/videos/blob/31f8ffe785e860477a6051fde983c02c7d165bc2/_2019/bayes/part1.py#L160-L196). Find the geometry that represents the quantity and keep the comparison edges anchored as it changes.
  - For a surface or a geometric relation in three dimensions, pair the [Gaussian integral lesson](https://www.3blue1brown.com/lessons/gaussian-integral/) with [`TalkAboutSignOfConstant3D`](https://github.com/3b1b/videos/blob/31f8ffe785e860477a6051fde983c02c7d165bc2/_2023/gauss_int/herschel.py#L1176). It ties a parameter to both a surface and a visible slice. Use 3D when depth, a cross-section, a projection, or a spatial transform carries the explanation. Keep labels fixed in the frame and move the camera when the change of view reveals information.

#### Read the whole frame

Pause on the opening, the key change, and the result. For a multi-scene video, also inspect how the source lesson opens and how the chosen passage connects to the scenes around it. Compare what the viewer sees at a cut with what they were just looking at. Trace the decisions in the code.

| Look at the rendered passage | Trace it in the source |
|---|---|
| **Sequence.** What question or example opens the passage? What stays, moves, or leaves? When do the result and the general rule appear? | Scene order, groups that survive a transition, reveal order, and holds. |
| **Composition.** What draws your eye first? How large is it, what space is left around it, and where do supporting objects or labels sit? Does the view move closer or widen, and what information does that reveal? | Group construction, anchoring and alignment, relative scale, label placement, and camera framing. |
| **Color and contrast.** Identify the background, quiet guides, data roles, and the strongest accent. Note when emphasis shifts and whether shape, position, or a line style also conveys the distinction. | Palette constants, style helpers, opacity, strokes, and any colors inherited from shared configuration. |
| **Typography.** Which words, symbols, and numbers need to be read? Look at their size, weight, proximity to the objects, and room at phone width. | Text and math objects, size relationships, how labels move with objects, and where they are cleared. |

In [Vectors around 5:25–5:45](https://www.youtube.com/watch?v=fNk_zzaMoSs&t=325s), the grid and origin anchor the frame, each short label sits near its arrow, and a separate color marks the sum when it appears. [`VectorAddition`](https://github.com/3b1b/videos/blob/31f8ffe785e860477a6051fde983c02c7d165bc2/_2016/eola/chapter1.py#L656-L676) sets up the plane, labels, colors, reveal, and hold. For a comparison over time, adapt the fixed guides, local labels, and result-only accent along with the translated line.

#### Apply the visual decisions

- In `scene_plan.md`, write what to carry into the new passage and where it changes the story or the viewer's attention. Give colors stable jobs across related shots. Check the actual reference frame and its matching source if you carry over a color value. Adapt the framing and text hierarchy to the new content, language, and aspect ratio.
- Translate the relevant mechanism into Manim Community Edition primitives. Use `Transform` for a pair of states, a `ValueTracker` and updaters for a continuous parameter, or `ThreeDScene` for spatial relationships. Link and credit the source and check its license before copying code or assets.
- Preserve object identity whenever it helps the viewer follow the argument. Keep comparison colors and axes fixed, transform or move objects viewers already recognize, and reveal derived values where they come from. Give the result a short hold after the motion.
- For icons, look under `videos/assets/tabler-icons/icons/outline/`. In a `skill-only` checkout, you can copy the needed SVGs from [Tabler Icons](https://github.com/tabler/tabler-icons/tree/main/icons/outline) and keep their license with the project assets. Load them with `SVGMobject` from a path relative to the scene or project. Match their stroke weight and color roles, and check them at the smallest size in the render. Use icons for entities such as visitors, clicks, and dates. Keep numeric evidence in the graph or diagram itself.

### From a reference sequence to a scene

In the [dice simulation at 6:15–6:42](https://www.youtube.com/watch?v=zeJD6dqJ5lo&t=375s), the die distribution appears first. A few rolls yield a visible sum, and successive sums build another distribution. [`show_sample_sum`](https://github.com/3b1b/videos/blob/31f8ffe/_2023/clt/main.py#L766) shows how the highlighted inputs and numeric result are coordinated. The viewer gets a worked example before the repetitions speed up.

- Use that order when it fits the concept. In an A/B test, show a worked pair of click counts and move their computed difference onto the axis. Give the first example a hold before the repetitions accelerate. When teaching binary search, carry the same sorted row through each comparison and eliminate the rejected half in place. This lets the viewer see where the next search range comes from.
- Where a single parameter changes the outcome, show the old and new states on the same scale. For example, keep the observed difference fixed as a larger sample pulls both confidence interval endpoints inward. Show the new values after the movement, with a brief hold to compare them.
- Inspect the transition at its actual pace. If the viewer can't tell where a result came from, stage one concrete example more slowly. Keep quantitative motion, color, text, and camera changes tied to what the viewer should notice.

## Staging and text

- Start close to the object or comparison the narration opens with. Give it enough space to read on a small screen. Reveal a second object only when there is something to compare. Arrange related beats around the same positions or axis so the audience keeps its bearings at the cut.
- Let the opening pose a concrete question with a visible example. Introduce names or formulas when the viewer has a reason to use them. Save camera moves, SVG icons, and highlights for actions that reveal a relationship or guide the eye.
- Move the object that creates the next result. For example, keep the colored parts of two count bars, move them onto a percentage axis, then draw a bracket between their heights. Show the value when the bracket lands. Hold the result long enough to read it before the next change.
- Put labels next to what they identify. A bar can carry `13%`, a dot can identify the estimate, and an interval can carry its endpoints. Use one typographic hierarchy for quantities, labels, and ticks. Remove repeated scene titles, boxed captions, and prose that restates what the viewer hears. Retain a short question, definition, or formula when the viewer needs to read it.

### Review the motion

Compare the preview's opening, key change, and result frames to the reference's visual hierarchy. Play the passage at normal speed and phone width with the sound off. Check where your eye goes, where text loses contrast or room, and how the frame changes when the idea advances. Use the first failure to choose what to change.

| What a viewer needs to see | If it is hard to follow |
|---|---|
| Which object matters as the beat opens | Start with the example in view. Move supporting labels near the object and delay details that matter later. |
| Where the result came from | Slow down one concrete example. Keep a stable anchor and transform the input, a marked copy, or its measurement into the result. |
| What changed and what stayed fixed | Keep shared axes, scale, and color meanings stable during the comparison. Bring in new labels when their values become readable. |
| Why the change answers the opening question | Hold both the result and the relevant comparison. Use the same example to lead into the general rule. |

Review the assembled video with sound at normal speed. Check motion against the words it illustrates, hold results through the relevant phrase, and play across cuts. For subtitles, check that they leave essential labels clear.

## Layout and caption safe area

1. When providing subtitles, leave the lower roughly 15% of a 16:9 frame clear of essential visuals and confirm the clearance in the target player. For burned-in captions, use a dedicated caption zone with edge padding. Without subtitles or captions, use the frame naturally, with comfortable edge margins.
2. For every beat record what stays, what enters, what leaves, and which object receives attention. Build a graph and its labels as a VGroup and fit the whole group into the body region. Group a caption with its background before measuring it.
3. Check bounding boxes after layout at target scale. For example, require `body.get_bottom()[1] >= caption.get_top()[1] + 0.25` at preview size. Verify transformed targets too, especially axis labels that extend beyond a plot and captions that wrap to two lines.
4. Render and sample the first and last frame of busy transitions and at least one hold frame per beat. Inspect physical intersections, minimum gap, competing focal points, information density, then timing. If an overlap appears, clear obsolete elements or split the beat first.
5. In a narrated video, keep explanatory sentences in the voice track and provide subtitles separately when needed. For a silent video or requested burned-in captions, use short, reviewed phrases that fit the frame. Match stable colors to the same semantic roles across beats.

## 1. Scene 클래스 구조

```python
class Scene{NN}_{ClassName}(Scene):
    """
    Scene {NN}: {핵심 주장}

    Visual Pivot: {시각적 전환점}
    Reference: {lesson.md 또는 source.ipynb} - {관련 문단/셀/섹션}
    Ref Video: {참조 영상 경로} — {선택 이유}

    Script: narration/{NN}_{scene_name}.txt
    Beat mapping:
      Beat 1 → 문단 1-2 (0.0~12.3s)
      Beat 2 → 문단 3   (12.3~20.1s)
      Beat 3 → 문단 4-5 (20.1~끝)
    """

    WAIT_TAIL = 1.0       # 마지막 여백
    RUN_TIME_SCALE = 1.0  # 전체 속도 조절

    def construct(self):
        # ─── Beat 1: T_i를 먼저 소개해 첫 화면 정보량을 제한한다 ───
        # 스크립트 문단 1-2 처리. 동시 노출은 핵심 그룹 1개로 제한.
        ...
        self.wait(0.5)

        # ─── Beat 2: 같은 학생을 두 세계로 나눠 Y_{1i}, Y_{0i}를 시각화한다 ───
        # 이전 Beat의 T_i를 상단에 남기고, 아래에 분기 구조를 추가한다.
        ...
        self.wait(0.5)

        # ─── Beat 3: factual / counterfactual 대비로 관찰 불가를 정리한다 ───
        ...
        self.wait(self.WAIT_TAIL)
```

## 2. 타이밍

`.timings.json` chunk → Beat 대응 기본값: chunk 1개 또는 인접 몇 개 = Beat 1개.

```python
# 일반적인 run_time
self.play(FadeIn(obj), run_time=0.5)      # 빠른 등장
self.play(Transform(a, b), run_time=1.0)  # 표준 변환
self.play(Write(text), run_time=1.5)      # 텍스트 작성
self.wait(0.3)                            # 짧은 호흡
self.wait(0.8)                            # 표준 호흡
```

**길이 조정 우선순위** (영상이 짧은 경우):
1. `WAIT_TAIL` 조정
2. Beat 사이 `self.wait()` 추가/제거
3. 개별 `run_time` 조정
4. Beat 경계 재분할 후 재렌더

화면은 오디오보다 약간 늦게 끝나는 편이 낫다.

## 3. 레이아웃

### Beat 설계 전 체크 (코드 작성 전 주석으로 남길 것)

```
# 남는 요소: T_i 라벨 (상단)
# 새로 등장: Y_1i 박스 (좌), Y_0i 박스 (우)
# 비워 두는 영역: 하단
```

동시 노출 핵심 그룹: **원칙 1개, 최대 2개**. 3개 이상이면 Beat 분리.

### 화면 구획

```python
title.to_edge(UP)
formula.to_edge(DOWN)
left_group.to_edge(LEFT, buff=1)
right_group.to_edge(RIGHT, buff=1)
label.to_corner(UR)
```

### 정렬

```python
VGroup(a, b, c).arrange(DOWN, buff=0.5)
VGroup(a, b, c).arrange(RIGHT, buff=0.3)
group.move_to(ORIGIN)
group.next_to(reference, DOWN, buff=0.5)
```

### 렌더 후 QA 순서

1. 물리적 겹침 확인 (최우선)
2. 간격 부족 확인 (겹치지 않아도 한 덩어리처럼 보이면 실패)
3. 시선 경쟁 구역 확인
4. 이전 Beat 잔상이 남아 경쟁하는지 확인

**과밀 Scene 수정 순서**: 요소 삭제 → Beat 분리 → 조기 FadeOut → 위치 조정 → 크기 조정 (이 순서 고정)

## 4. 색상

```python
HIGHLIGHT = YELLOW
POSITIVE = GREEN
NEGATIVE = RED
NEUTRAL = BLUE

TREATMENT = "#4CAF50"  # 처치군 (초록)
CONTROL = "#2196F3"    # 대조군 (파랑)
EFFECT = "#FF9800"     # 효과 (주황)
```

## 5. 텍스트·수식·아이콘

### 수식

```python
formula = MathTex(r"E[Y_1 - Y_0]")

# 부분 색상
formula_colored = MathTex(r"E[Y_1", r"-", r"Y_0]")
formula_colored[0].set_color(GREEN)
formula_colored[2].set_color(RED)
```

### 한글 텍스트

```python
text = Text("효과 추정", font="NanumGothic")  # 또는 시스템 기본 폰트
```

### 공용 SVG 아이콘

```python
from pathlib import Path

ICON_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
icon = SVGMobject(str(ICON_DIR / "device-tablet.svg"))
icon.set_stroke(color=TEAL_D, width=2.6)
icon.set_fill(opacity=0)
```

### 하이라이트 박스

```python
box = SurroundingRectangle(target, color=YELLOW, buff=0.1)
self.play(Create(box))
```

## 6. 애니메이션 패턴

```python
# 순차 등장
for item in items:
    self.play(FadeIn(item, shift=UP*0.2), run_time=0.3)

# 동시 변환
self.play(Transform(a, a_new), Transform(b, b_new), run_time=1.0)

# 강조
self.play(Indicate(target))
self.play(Flash(target, color=YELLOW))
self.play(Circumscribe(target))

# 페이드 전환
self.play(FadeOut(old_group), FadeIn(new_group))
```

## 7. 3D Scene

```python
class Scene{NN}(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

        axes = ThreeDAxes(
            x_range=[-3, 3], y_range=[-3, 3], z_range=[-3, 3],
            x_length=6, y_length=6, z_length=6
        )

        self.move_camera(phi=60*DEGREES, theta=-30*DEGREES, run_time=2)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        self.add_fixed_in_frame_mobjects(label)  # HUD 요소
```

## 8. 데이터 시각화

```python
# 표
table = Table(
    [["A", "B"], ["1", "2"]],
    col_labels=[Text("X"), Text("Y")],
    include_outer_lines=True
)

# 막대 그래프
chart = BarChart(values=[3, 5, 2], bar_names=["A", "B", "C"], y_range=[0, 6, 1])

# 좌표평면
axes = Axes(x_range=[0, 10], y_range=[0, 10])
dot = Dot(axes.c2p(5, 7), color=RED)
```

## 9. 렌더 명령어

```bash
manim -pql --media_dir build/manim {file}.py Scene{NN}_{Name}  # 저화질
manim -pqh --media_dir build/manim {file}.py Scene{NN}_{Name}  # 고화질
```

## 10. 흔한 실수

| 실수 | 해결 |
|-----|------|
| 텍스트·수식 겹침 | `buff` 조정, `next_to()` 사용 |
| 애니메이션 너무 빠름 | `run_time` 증가 |
| 3D에서 레이블 회전 | `add_fixed_in_frame_mobjects()` |
| 한글 깨짐 | 시스템 한글 폰트 지정 |
| 표 위에 긴 박스 추가 | Beat 분리로 해결 |
