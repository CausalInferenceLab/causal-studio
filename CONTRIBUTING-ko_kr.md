# Contributing

[English](./CONTRIBUTING.md) | 한국어

이 프로젝트는 실행 가능한 Jupyter Book과 로컬 전용 Manim 영상 워크플로우를 함께 다룹니다. 변경은 작고 명확하게 유지하고, 로컬 환경과 Binder/book 환경에서 모두 재현 가능하도록 작성합니다.

## 로컬 환경 설정

저장소 루트에서 전체 환경을 준비합니다.

```bash
bash scripts/setup_environment.sh
source .venv/bin/activate
```

스크립트는 `Pipfile`의 Python 버전을 사용하고, 기존 `.venv`를 재사용합니다. `requirements.txt`를 설치하고 3Blue1Brown 레퍼런스와 Tabler Icons를 로컬에 준비합니다. Python 실행 파일은 `PYTHON_BIN`으로 지정할 수 있습니다. Manim wheel을 사용할 수 없는 환경에서는 Cairo, Pango, `pkg-config`도 설치합니다.

책만 작업할 때는 `--book-only`, Manim 미리보기만 필요할 때는 `--video-only`를 사용합니다. 영상 전용 환경은 `.venv-video`에 생성됩니다. `--check`를 붙이면 패키지 설치나 에셋 갱신 없이 선택한 환경을 검증합니다.

## 핵심 규칙

1. 저장소 스킬을 우선 사용합니다.
   - Codex 워크플로우는 `.codex/skills/`를 사용합니다.
   - 해당 트리거가 있는 작업은 `.claude/skills/`를 운영 기준으로 삼습니다.

2. 의존성 범위를 분리합니다.
   - `requirements.txt`: book + video 전체 로컬 작업용
   - `requirements-book.txt`: book, Binder, 배포용 최소 런타임
   - `requirements-video.txt`: Manim 미리보기 전용
   - `binder/apt.txt`: Binder에서 필요한 시스템 패키지

3. Binder-safe한 노트북을 작성합니다.
   - 현재 작업 디렉터리가 노트북 위치라고 가정하지 않습니다.
   - 저장소 루트와 노트북 로컬 실행에서 모두 동작하는 경로를 사용합니다.
   - `book/` 노트북이 새 패키지를 import하면 `requirements-book.txt`도 함께 갱신합니다.

4. 로컬 전용 자산은 커밋하지 않습니다.
   - `.env`, 로컬 설정, 생성 캐시, 렌더 결과물은 기본적으로 제외합니다.
   - `3b1b/`, `videos/assets/tabler-icons/`는 로컬 설정 자산으로 취급합니다.

## 노트북 작성 기준

영상화 전 노트북은 영상의 초안이면서, 노트북만으로도 학습 가치가 있어야 합니다.

- 설명이 충분해야 합니다. 개념, 가정, 코드 결과, 그래프 해석을 독자에게 떠넘기지 않습니다.
- 셀 단위로 읽고 실행하기 쉬워야 합니다. `.py` 파일처럼 앞쪽에 함수와 클래스를 많이 정의해두고 뒤에서 호출하는 구조는 피합니다.
- 학습 흐름을 위해 필요한 정도의 코드 중복은 허용합니다. 과도한 추상화보다 이해하기 쉬운 전개를 우선합니다.
- 직접 구현보다 검증된 라이브러리 사용을 우선합니다.
- 영상으로 만들었을 때 시각화를 통해 더 잘 설명될 만한 내용인지 확인합니다.
- 위에서 아래로 실행했을 때 오류 없이 완료되어야 합니다.

## 검증과 커밋

- 수정한 book 콘텐츠는 빌드하거나 그에 준해 검증합니다.
- Binder 관련 변경은 의존성, 경로, 실행 시간을 함께 점검합니다.
- 관련 없는 변경은 같은 커밋에 섞지 않습니다.
- 배포 노트북에 영향을 주는 변경은 관련 설정 변경도 같은 PR에 포함합니다.
- `main`의 `book/` 변경은 GitHub Pages 배포를 실행합니다.

## 영상 스타터 배포

배포할 버전에서 `python scripts/export_manim_starter.py --zip causal-studio-starter.zip`을 실행합니다. ZIP을 새 폴더에 풀고 README에 따라 예제를 렌더한 뒤, Causal Studio의 GitHub Release에 해당 ZIP을 첨부합니다. 이 명령은 현재 작업 중인 버전의 스킬, 실행 파일, 예제를 묶습니다.
