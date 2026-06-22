---
name: manim-thumbnail
description: |
  Manim CE로 YouTube 썸네일 PNG를 생성하는 스킬.
  3Blue1Brown 스타일 (검정 배경 + CM 세리프 + 수학 시각 요소)을 기본으로 한다.

  트리거: "썸네일 만들어줘", "thumbnail 만들어줘", "썸네일 생성", "thumbnail 이미지"
---

# Manim Thumbnail

Manim CE로 3b1b 스타일의 YouTube 썸네일(1920×1080 PNG)을 생성하는 워크플로우.

## 파일 구조

```text
videos/{topic}/
├── src/
│   └── thumbnail.py        # 썸네일 Manim Scene
└── build/
    └── thumbnail.png       # 최종 출력물 (src/나 루트에 두지 않음)
```

## 렌더 명령어

```bash
cd videos/{topic}
manim -s --resolution 1920,1080 --media_dir build/manim src/thumbnail.py Thumbnail
# build/manim/images/thumbnail/ 안의 PNG 파일명을 ls로 확인 후 복사
cp build/manim/images/thumbnail/*.png build/thumbnail.png
```

## 작업 순서

1. 토픽의 핵심 개념 하나를 시각화할 방법을 먼저 정한다
2. 레이아웃 스케치: 시각 요소와 텍스트의 화면 구획을 먼저 잡는다
3. `src/thumbnail.py` 작성
4. 렌더 후 `build/thumbnail.png` 확인
5. 필요하면 레이아웃/색상 조정 후 재렌더

## 디자인 원칙

**배경·폰트**
- 배경: 순수 검정(`#000000`)
- 제목은 `Tex(r"\textbf{...}")`으로 LaTeX CM 세리프 사용 — 3b1b 특유의 세리프 느낌
- 텍스트 색은 기본 흰색

**시각 요소**
- 토픽을 대표하는 수학적 오브젝트 하나에 집중 (DAG, 그래프, 수식, 도형, 격자 등)
- 색상은 2~3개만 사용. 밝고 선명한 색 대비
- 한 번에 전달할 메시지는 하나 — 요소를 욕심껏 넣지 않는다

**레이아웃**
- 좌(시각) + 우(제목), 제목 중앙 + 시각 배경, 시각 중심 + 제목 코너 중 토픽에 맞는 것을 선택
- 요소가 화면 끝에 붙지 않도록 충분한 패딩
- 썸네일은 정적 이미지이므로 `-s` 플래그로 애니메이션 없이 마지막 프레임만 저장

## 프로젝트 공통 색상

| 역할 | Manim 상수 | 헥스 |
|------|-----------|------|
| 처치/주요 강조 | `TEAL_D` | `#4DD0C4` |
| 결과/보조 강조 | `YELLOW_E` | `#C8A630` |
| 교란/중립 | `GREY_B` | `#AAAAAA` |

이 팔레트는 의무가 아니다. 토픽이 다르면 다른 색을 써도 된다.
