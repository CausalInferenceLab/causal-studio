<a id="top"></a>

# Causal Studio

🌐 Language: [English](./README.md) | 한국어

인과추론에 관한 교육 영상과 실행 가능한 노트북을 제공하는 플랫폼입니다.

- Book: <https://causalinferencelab.github.io/causal-studio/>
- YouTube: <https://www.youtube.com/@CausalStudio>

작업 규칙: [English](./CONTRIBUTING.md) | [한국어](./CONTRIBUTING-ko_kr.md)

## 학습 방법

1. 영상을 먼저 보기: 각 장을 명확한 시각 자료로 이해합니다.
2. 노트북 실행과 탐구: Binder 또는 Colab에서 직접 코드를 실행해 보며 실습하고, 노트북의 코드와 설명으로 더 깊이 이해합니다.

## 저장소 구조

```text
causal_studio/
├── book/
│   └── why_causal_inference/        한·영 노트북
├── videos/
│   └── why_causal_inference/
│       └── src/                     Scene 코드 + 나레이션 스크립트
├── .codex/skills/                   Codex 스킬
├── .claude/skills/                  Claude Code 스킬
├── requirements.txt                 전체 의존성 (book + video)
└── requirements-book.txt            book 전용 (CI/배포)
```

## 환경 세팅

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
