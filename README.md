# Causal Studio

인과추론 코드북과 Manim 교육 영상을 함께 관리하는 저장소입니다.

이 저장소는 skill-first 운영을 전제로 합니다.
- Codex는 repo 스코프 스킬인 `.codex/skills/*`를 우선 사용합니다.
- 영상 작업은 `.claude/skills/manim-video-pipeline/`를 브리지로 사용합니다.

## 먼저 할 일

새 환경에서 처음 이 저장소를 받았으면 아래 순서로 시작합니다.

1. Python 의존성 설치
2. 로컬 전용 영상 참조 자산 설치
3. Book 또는 video 작업 시작

### 1) Python 의존성 설치

Codex 기준:
```bash
$python-setup
```

자연어 예시:
```text
이 저장소 Python 환경부터 세팅해줘
```

추가 패키지를 넣을 때는 초기 세팅 스킬이 아니라 `pip-install`을 사용합니다.

예시:
```text
jupyter-book 설치해줘
manim 패키지 설치해줘
```

### 2) 로컬 전용 영상 자산 설치

영상 제작은 아래 두 외부 저장소를 로컬에 준비해 둬야 합니다.

- 3Blue1Brown videos: `https://github.com/3b1b/videos.git`
- Tabler Icons: `https://github.com/tabler/tabler-icons.git`

이 둘은 git tracked 자산이 아니라 로컬 참조 자산입니다.

Codex 기준:
```bash
$video-assets-setup
```

자연어 예시:
```text
영상 작업용 로컬 자산 설치해줘
```

설치 결과:
- `3b1b/`
- `videos/assets/tabler-icons/`

## 저장소 구조

```text
book/                      Jupyter Book 소스
videos/
  assets/                 공용 로컬 영상 자산
  {topic}/
    src/                  scene 코드 + scene script
    preview/              저화질 확인본
    build/
      audio/              scene mp3
      manim/              manim 캐시/중간 산출물
      final/              승인된 hq scene + full video
.codex/skills/            Codex repo 스코프 스킬
.claude/skills/           Claude 스킬 원본 및 브리지 대상
3b1b/                     로컬 참조용 3Blue1Brown clone
```

## Book 작업

로컬 서버:

Codex:
```bash
$book-serve
```

자연어 예시:
```text
book 로컬 서버 실행해줘
```

프로덕션 빌드:
```text
book 빌드 검증해줘
```

페이지/노트북 반영은 `book-publish` 스킬을 사용합니다.

## 영상 작업

직접 셸 명령보다 `manim-video-pipeline` 스킬 호출을 기본으로 사용합니다.

전제:
- 먼저 `$video-assets-setup` 을 실행해 `3b1b/` 와 `videos/assets/tabler-icons/` 를 준비해야 합니다.

Codex:
```bash
$manim-video-pipeline
```

자연어 예시:
```text
why_causal_inference_ko.ipynb 기준으로 scene 01만 만들어줘
```

3b1b 참조를 명시하는 예시:
```text
why_causal_inference 토픽으로 진행하고 ref_video=3b1b/videos/_2020/covid.py 참고해서 scene 01 설계해줘
```

현재 video 산출물 규칙:
- `videos/{topic}/preview/code/`: 저화질 코드 확인본
- `videos/{topic}/preview/mux/`: 저화질 오디오 합성 확인본
- `videos/{topic}/build/audio/`: scene mp3
- `videos/{topic}/build/manim/`: manim 내부 캐시
- `videos/{topic}/build/final/`: hq scene, full video

## 주요 스킬

| 스킬 | 용도 |
|---|---|
| `python-setup` | `.venv` 생성 및 Python 의존성 초기 설치 |
| `pip-install` | `.venv`에 패키지 설치 후 `requirements.txt` 동기화 |
| `video-assets-setup` | 3b1b와 Tabler Icons 로컬 자산 설치/업데이트 |
| `book-serve` | Jupyter Book 로컬 서버 실행 |
| `book-publish` | 페이지/노트북을 book에 반영하고 빌드 검증 |
| `git-commit` | 변경 분석 및 커밋 |
| `git-pr` | PR 생성 워크플로우 |
| `manim-video-pipeline` | scene 설계, script, render, audio, mux, final |

## 권장 사용 방식

- 가능하면 직접 셸 명령보다 Codex 스킬 호출을 우선 사용합니다.
- 짧은 명령형 요청이나 자연어 요청 모두 괜찮습니다.
- 직접 실행은 스킬이 없거나, 디버깅 때문에 명령 자체가 필요한 경우에만 씁니다.

예시:
- `$python-setup`
- `jupyter-book 설치해줘`
- `numpy랑 pandas 설치해줘`
- `$video-assets-setup`
- `$book-serve`
- `$manim-video-pipeline`
- `scene 01만 다시 렌더해줘`
- `git 커밋 준비해줘`

## 로컬 전용 경로

아래 경로는 로컬 참조 또는 산출물 영역입니다.
- `3b1b/`
- `videos/assets/tabler-icons/`
- `videos/*/preview/`
- `videos/*/build/`
- `book/_build/`

## 라이선스

이 저장소 자체는 MIT입니다.  
외부 자산은 각 upstream 라이선스를 따릅니다.
