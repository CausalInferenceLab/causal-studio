---
name: pip-install
description: |
  패키지 설치 후 requirements.txt 자동 동기화.
  가상환경(.venv)에 패키지를 설치하고 requirements.txt를 업데이트한다.

  트리거: "pip install", "패키지 설치", "install package"
---

# pip-install

패키지 설치 + requirements 동기화 워크플로우.

## 사용법

### 사용자 요청

```
"jupyter-book 설치해줘"
"pandas랑 numpy 설치해줘"
```

### Claude 작업

1. 가상환경 활성화 후 패키지 설치
2. 용도에 맞는 requirements 파일 업데이트

## 설치 명령어

```bash
# 1. 가상환경 활성화 + 패키지 설치
source .venv/bin/activate && pip install {package_name}

# 2. requirements 업데이트 (기존 내용 유지하며 추가)
# 로컬 전체 작업용 패키지면 requirements.txt에 추가
# 책/노트북 실행에도 필요한 패키지면 requirements-book.txt에도 추가

# 방법 B: 전체 freeze (카테고리 정보 손실)
# pip freeze > requirements.txt
```

## requirements.txt 형식

카테고리별로 정리하여 관리:

```txt
# Jupyter Book
jupyter-book>=1.0.0

# Video Production
manim>=0.18.0

# Data Science
numpy
pandas
matplotlib
seaborn

# 신규 설치 패키지
{new_package}
```

## 주의사항

- 항상 `.venv` 가상환경에서 설치
- 책(`book/`)에서 import하거나 Binder/GitHub Pages 빌드에 필요한 패키지는 `requirements-book.txt`에도 반영
- Binder에서 시스템 패키지가 필요한 라이브러리면 `binder/apt.txt`도 함께 점검
- `pip freeze`는 모든 의존성을 나열하므로, 직접 설치한 패키지만 requirements.txt에 추가 권장
- 버전 명시가 필요한 경우 `>=` 또는 `==` 사용
