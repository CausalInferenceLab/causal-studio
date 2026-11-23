<a id="top"></a>

# Causal Studio

🌐 Language: [English](./README.md) | 한국어

**Claude Code나 Codex에 원고, 노트북, 또는 한 문장을 주고 Manim 설명 영상을 만들어 보세요.**

Causal Studio는 이 방식으로 인과추론 영상을 만들고, 같은 개념을 직접 실습할 수 있는 노트북을 함께 제공합니다.

**[내 주제로 영상 만들기](./docs/manim-starter.md)** · [RDD 영상 보기](https://www.youtube.com/watch?v=65C9J1yJwhc) · [노트북으로 학습하기](https://causalinferencelab.github.io/causal-studio/)

[![장학금 기준인 370점 양쪽의 GPA 산점도와 회귀선을 보여주는 RDD 장면](./docs/assets/rdd-preview.jpg)](https://www.youtube.com/watch?v=65C9J1yJwhc)

## Manim 스킬 써보기

저장소를 클론해 Claude Code나 Codex에서 폴더를 엽니다. 원고를 주거나 아래처럼 요청하세요.

> `manim-video-pipeline`으로 중학생 대상 광합성 영상의 첫 장면을 만들어줘. 영상 환경도 준비하고 무음 미리보기를 보여줘.

에이전트가 장면을 설계하고 수정 가능한 Manim 코드를 작성한 뒤 렌더합니다. 화면을 검토하고 나면 OpenAI나 ElevenLabs로 내레이션을 붙일 수 있습니다. [빠른 시작](./docs/manim-starter.md)

## 학습 방법

1. 영상을 먼저 보기: 각 장을 명확한 시각 자료로 이해합니다.
2. 노트북 실행과 탐구: Binder 또는 Colab에서 직접 코드를 실행해 보며 실습하고, 노트북의 코드와 설명으로 더 깊이 이해합니다.

[Causal Studio 영상 더 보기](https://www.youtube.com/@CausalStudio). 이 방식으로 영상 제작에 도움을 받았다면 GitHub 스타로 알려주세요.

## 저장소 구조

```text
causal_studio/
├── book/
│   └── why_causal_inference/        한·영 노트북
├── videos/
│   ├── binary-search/              스타터 예제와 자막·타이밍 예시
│   └── why_causal_inference/
│       └── src/                     Scene 코드 + 나레이션 스크립트
├── .codex/skills/                   Codex 스킬
├── .claude/skills/                  Claude Code 스킬
├── requirements.txt                 전체 의존성 (book + video)
└── requirements-book.txt            book 전용 (CI/배포)
```

## 기여자 환경 설정

작업 규칙은 [한국어](./CONTRIBUTING-ko_kr.md)와 [English](./CONTRIBUTING.md)로 제공합니다.

새 환경에서 처음 클론한 경우:

```text
이 저장소 Python 환경 세팅해줘      → python-setup 스킬 (Python + 영상 에셋 2종)
영상 작업용 로컬 자산 갱신해줘      → video-assets-setup 스킬
```

저장소 루트에서 전체 초기 세팅을 실행합니다.

```bash
bash scripts/setup_environment.sh
source .venv/bin/activate
```

기존 `.venv`는 재사용합니다. 새 가상환경은 `Pipfile`의 Python 버전(현재 3.11,
실행 파일은 `PYTHON_BIN`으로 지정 가능)으로 만들고, `requirements.txt`와 두 에셋
저장소를 준비합니다. 해당 Python 버전은 먼저 설치해야 합니다. Manim의 wheel이
없는 경우 시스템 Cairo/Pango 개발 라이브러리와 `pkg-config`도 필요합니다.

Book 전용 세팅을 명시적으로 원할 때만 `bash scripts/setup_environment.sh --book-only`를
사용합니다. 이 경우 `requirements-book.txt`를 설치하고 영상 에셋은 제외합니다.
`--check`는 설치·갱신 없이 검증만 수행하며 `--book-only`와 함께 사용할 수 있습니다.
전체 세팅은 의존성 충돌 검사, 주요 import, 두 에셋의 필수 파일 검증을 모두 통과해야
완료로 보고합니다.

두 스킬은 공통 스크립트를 사용하며, 아래 두 저장소를 로컬에 clone합니다 (git 미추적).

- `3b1b/` — 3b1b/videos 참조용
- `videos/assets/tabler-icons/` — Tabler Icons 아이콘셋

## CI/CD

`main` 브랜치에 `book/**` 변경사항이 push되면 GitHub Actions가 자동으로 GitHub Pages에 배포합니다.

배포 의존성: `requirements-book.txt`

## 라이선스

이 저장소는 MIT입니다. 외부 자산(3b1b, Tabler Icons)은 각 upstream 라이선스를 따릅니다.
