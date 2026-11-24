<h1 align="center">Causal Studio</h1>

<p align="center"><strong>어려운 수학·통계 개념을 3Blue1Brown 스타일의 영상으로 만들어 보세요.</strong></p>

<p align="center">Causal Studio의 인과추론 시리즈에 쓰인 오픈소스 Manim 스킬입니다.<br>Claude Code나 Codex에 원하는 영상을 한 문장으로 설명하면 됩니다.</p>

<p align="center">
  <a href="#첫-영상-만들기"><strong>영상 만들기</strong></a> ·
  <a href="https://www.youtube.com/@CausalStudio">YouTube에서 보기</a> ·
  <a href="https://causalinferencelab.github.io/causal-studio/">인과추론 교재</a> ·
  <a href="./README.md">English</a>
</p>

<p align="center">
  <a href="https://www.youtube.com/watch?v=65C9J1yJwhc">
    <picture>
      <source media="(prefers-reduced-motion: reduce)" srcset="./docs/assets/rdd-preview.jpg">
      <img src="./docs/assets/rdd-animation.gif" width="820" alt="장학금 기준인 370점 양쪽에 GPA 산점도와 회귀선이 차례로 나타나고, 두 회귀선의 차이를 표시하는 애니메이션.">
    </picture>
  </a><br>
  <sub><a href="https://www.youtube.com/watch?v=65C9J1yJwhc">예시 영상 보기</a> · 회귀불연속설계</sub>
</p>

## 첫 영상 만들기

1. 터미널에서 아래 명령을 실행하세요.

   ```bash
   git clone -b skill-only https://github.com/CausalInferenceLab/causal-studio
   ```

2. Claude Code나 Codex에서 `causal-studio` 폴더를 열고 아래 요청을 보내세요.

   ```text
   manim-video-pipeline으로 1분 15초짜리 A/B 테스트 입문 영상을 만들어줘.
   버튼 색을 바꾼 사례로 변경 전후 비교의 함정, 무작위 배정, 클릭률 차이,
   신뢰구간 해석, 새 버튼을 적용할 기준을 다섯 장면으로 보여줘.
   ```

대본이나 Jupyter Notebook 등 영상에 참고할 파일이 있다면 경로도 함께 알려주세요. 미리보기는 음성 API 키 없이 만들 수 있습니다.

Causal Studio의 인과추론 작업처럼 `.ipynb`에 설명과 시각화 코드를 먼저 정리해 두면, 원하는 설명 순서와 그래프를 영상에 반영하기 쉽습니다. [RDD 노트북 예시](./book/rdd/01_rdd_basic_ko.ipynb)

## 내레이션 영상 제작 흐름

![대본을 쓰고 음성을 만든 뒤, Manim 영상과 합쳐 MP4로 완성하는 순서](./docs/assets/manim-workflow-ko.png)

1. **대본 쓰기.** AI가 쓴 초안을 직접 고치거나 수정을 요청할 수 있습니다. 다듬은 대본이 음성과 화면 구성의 기준이 됩니다.
2. **음성 만들기.** OpenAI나 ElevenLabs로 대본을 음성으로 바꿉니다. 장면마다 MP3를 만들고 문단별 시작과 끝을 `*.timings.json`에 기록합니다.
3. **영상 완성하기.** 내레이션에 맞춰 그래프와 도형을 움직이고, 화면에는 필요한 숫자와 라벨을 남깁니다. 음성을 붙인 장면을 한 편의 MP4로 합칩니다.

음성을 추가할 때는 [`.env.example`](./.env.example)과 [음성 설정 가이드](./docs/manim-starter.md#3-review-and-add-narration-if-you-want-it)를 참고하세요.

## 작업 폴더 예시

A/B 테스트 예시의 대본과 Manim 코드는 장면마다 파일 하나씩입니다. 수정할 때는 Claude Code나 Codex에 장면 번호와 바꾸고 싶은 내용을 알려주세요.

> 3번 장면에서 두 막대의 클릭률 차이를 조금 더 오래 보여줘. 그 장면만 다시 렌더링해줘.

```text
videos/ab-test/
├── project.toml           # 참고 자료와 기본 렌더 장면
├── lesson.md              # 주제로 시작할 때 생성 (.md, .txt, .ipynb도 입력 가능)
├── scene_plan.md          # 장면마다 화면에 보여줄 변화
├── assets/                # 영상에 쓰는 아이콘과 이미지
├── narration/             # 장면별 대본
│   ├── 01_question.txt
│   ├── 02_assignment.txt
│   ├── 03_rates.txt
│   ├── 04_interval.txt
│   └── 05_decision.txt
├── scenes/                # 장면별 Manim 코드
│   ├── scene_01.py
│   ├── scene_02.py
│   ├── scene_03.py
│   ├── scene_04.py
│   ├── scene_05.py
│   └── style.py           # 공통 색상과 그래픽
└── build/
    ├── audio/             # 장면별 MP3와 타이밍
    ├── manim/             # Manim 렌더
    ├── final/             # 음성을 붙인 장면별 MP4
    ├── ab-test.mp4        # 전체 영상
    └── ab-test.ko.srt     # 선택 자막
```

## Causal Studio 둘러보기

애니메이션과 실행 가능한 노트북으로 인과추론을 공부할 수 있습니다. 교재, 노트북, 기존 영상의 Manim 코드를 수정하려면 전체 프로젝트를 클론하세요. 같은 영상 스킬이 들어 있습니다.

```bash
git clone https://github.com/CausalInferenceLab/causal-studio
```

[RDD 영상의 장면별 Manim 코드](./videos/rdd/scenes/)에서 실제 강의 영상 구조를 볼 수 있습니다.

[YouTube에서 강의 보기](https://www.youtube.com/@CausalStudio) · [인과추론 교재](https://causalinferencelab.github.io/causal-studio/) · [스킬 보기](./.claude/skills/manim-video-pipeline/SKILL.md) · [기여하기](./CONTRIBUTING-ko_kr.md)

---

스킬이 영상 제작에 도움이 됐다면 Causal Studio에 스타를 눌러주세요.

MIT. 3Blue1Brown 레퍼런스와 Tabler Icons 같은 외부 자산은 각자의 라이선스를 따릅니다.
