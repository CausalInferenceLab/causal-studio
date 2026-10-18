---
name: python-setup
description: Set up this repository on a new machine or prepare its Python environment, including .venv, full local dependencies, 3Blue1Brown references, and Tabler Icons by default. Use for initial setup, Python environment setup, or a missing .venv. Use Book-only mode only when explicitly requested.
---

# Python Setup

저장소 루트에서 공통 초기 세팅 스크립트를 실행한다.

```bash
bash scripts/setup_environment.sh
```

- 기본 초기 세팅에 `.venv`, `requirements.txt`, `3b1b/`, `videos/assets/tabler-icons/`를 모두 포함한다. 영상 에셋을 선택 사항으로 처리하지 않는다.
- 새 가상환경은 `Pipfile`의 Python 버전으로 만든다. 기본 실행 파일은 `python3.11`이며 다른 위치는 `PYTHON_BIN`으로 지정한다. 기존 `.venv`는 재사용하고 버전 불일치나 손상이 있으면 임의로 삭제하지 말고 보고한다.
- 사용자가 Book 전용 환경을 명시한 경우에만 `bash scripts/setup_environment.sh --book-only`를 실행한다. 이 모드는 `requirements-book.txt`를 사용하고 영상 에셋을 제외한다.
- 설치 명령을 수동으로 재구현하지 않는다. 공통 스크립트는 Python 설치 후 `video-assets-setup`의 공통 스크립트를 반드시 실행한다.
- Python이나 Manim 시스템 라이브러리가 없으면 필요한 도구를 확인하고 실패 원인과 남은 단계를 보고한다. 의존성 파일의 범위를 임의로 바꾸지 않는다.

## 완료 검증

```bash
bash scripts/setup_environment.sh --check
# Book 전용으로 요청받은 경우:
# bash scripts/setup_environment.sh --book-only --check
```

의존성 충돌 검사, 주요 패키지 import, 두 에셋의 Git 저장소 및 아래 파일 검증을 모두 통과해야 전체 초기 세팅 완료로 보고한다.

- `3b1b/_2020/covid.py`
- `videos/assets/tabler-icons/icons/outline/device-tablet.svg`

실패하거나 일부만 설치되면 전체 완료로 표현하지 않는다. 최종 보고에 Python 버전, 의존성 검사 결과, 두 에셋 상태를 포함한다. Book 전용 모드에서는 영상 에셋 제외를 명시한다. 활성화 명령은 `source .venv/bin/activate`다.
