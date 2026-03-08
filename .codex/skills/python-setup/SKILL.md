---
name: python-setup
description: Create the repo virtual environment and install Python dependencies from requirements files. Use when setting up this repo on a new machine, when .venv is missing, or when the user asks for initial Python environment setup.
---

# Python Setup

이 저장소의 기본 Python 작업 환경을 준비한다.

목표:
- `.venv` 생성
- `requirements.txt` 설치
- 필요 시 `requirements-book.txt`도 사용

기본 원칙:
- 항상 저장소 루트에서 실행한다.
- 가상환경 이름은 `.venv`로 고정한다.
- 이미 `.venv`가 있으면 재사용한다.
- `requirements.txt`는 전체 로컬 작업용이다.
- `requirements-book.txt`는 book 빌드/배포용 최소 의존성이다.

## 기본 실행

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Book 전용 환경일 때

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-book.txt
```

## 확인

```bash
test -d .venv
source .venv/bin/activate
python --version
pip --version
```

새 환경에서 이 스킬을 먼저 실행한 뒤, 필요하면 `video-assets-setup`을 이어서 실행한다.
