# Manim Code Patterns

## Visual design and icons

- Start with the visual question. Identify what the viewer can see change to answer it. For example, move the same visitors into two groups, then carry the group colors into the click-rate comparison.
- For 3Blue1Brown-inspired work, pick a reference by the technique you need. Use the local `3b1b/` checkout when available. For distributions and sampling, see the [central limit theorem source scene](https://github.com/3b1b/videos/blob/master/_2023/clt/main.py) for updating a plot in place, varying a parameter, and drawing attention to one statistic at a time. Note the specific technique and your adaptation in the scene plan, then write it for Manim Community Edition.
- Preserve object identity whenever it helps the viewer follow the argument. Keep comparison colors and axes fixed, transform or move objects viewers already recognize, and reveal derived values where they come from. Give the result a short hold after the motion.
- For icons, look under `videos/assets/tabler-icons/icons/outline/`. In a `skill-only` checkout, you can copy the needed SVGs from [Tabler Icons](https://github.com/tabler/tabler-icons/tree/main/icons/outline) and keep their license with the project assets. Load them with `SVGMobject` from a path relative to the scene or project. Match their stroke weight and color roles, and check them at the smallest size in the render. Use icons for entities such as visitors, clicks, and dates. Keep numeric evidence in the graph or diagram itself.
- Inspect at least one frame from the beginning, middle, and end of each key motion. Verify the viewer can track what moved, understand the resulting comparison, and read the caption while it is on screen. For a full video, also sample the last frame of one scene and the first frame of the next.

## Staging and text

- Start close to the object or comparison the narration opens with. Give it enough space to read on a small screen. Reveal a second object only when there is something to compare. Arrange related beats around the same positions or axis so the audience keeps its bearings at the cut.
- Move the object that creates the next result. For example, keep the colored parts of two count bars, move them onto a percentage axis, then draw a bracket between their heights. Show the value when the bracket lands. Hold the result long enough to read it before the next change.
- Put labels next to what they identify. A bar can carry `13%`, a dot can identify the estimate, and an interval can carry its endpoints. Use one typographic hierarchy for quantities, labels, and ticks. Remove repeated scene titles, boxed captions, and prose that restates what the viewer hears. Retain a short question, definition, or formula when the viewer needs to read it.
- Check the preview at a phone-sized width. With sound off, confirm the change and the quantities are apparent. With sound on, confirm the change lands on the relevant phrase. If subtitles are available, turn them on once to check that the lowest labels stay clear of the player subtitle area.

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
