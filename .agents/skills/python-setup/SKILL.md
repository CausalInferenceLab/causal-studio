---
name: python-setup
description: |
  Create the repo virtual environment and install Python dependencies from requirements files.
  Use when setting up this repo on a new machine, when .venv is missing, or when the user asks for initial Python environment setup.
---

# Python Setup

## Workflow

### 기본 설치 (로컬 전체 작업용)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Book 전용 환경 (배포/빌드 최소 의존성)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-book.txt
```

## 확인

```bash
test -d .venv && source .venv/bin/activate && python --version && pip --version
```

## 원칙

- 항상 저장소 루트에서 실행한다.
- 가상환경 이름은 `.venv`로 고정한다.
- `.venv`가 이미 있으면 재사용한다.
- `requirements.txt` — 로컬 전체 작업용.
- `requirements-book.txt` — book 빌드/배포용 최소 의존성.
- 설치 완료 후 영상 제작 자산이 필요하면 `video-assets-setup` 스킬을 이어서 실행한다.
