---
name: video-assets-setup
description: |
  Set up local-only video reference assets by cloning or updating 3Blue1Brown source files and Tabler Icons into ignored paths.
  Use when a new machine clones the repo, when 3b1b references are missing, or when videos/assets/tabler-icons is absent.
---

# Video Assets Setup

로컬 전용 영상 제작 참조 자산을 준비한다.

준비 대상:
- `3b1b/` — 3Blue1Brown 참조 코드
- `videos/assets/tabler-icons/` — 공용 SVG 아이콘 라이브러리

## 실행

```bash
bash .claude/skills/video-assets-setup/scripts/setup_video_assets.sh
```

이미 디렉터리가 있으면 `git pull --ff-only`로 갱신한다.

## 확인

```bash
test -f 3b1b/_2020/covid.py && echo "3b1b OK"
test -f videos/assets/tabler-icons/icons/outline/device-tablet.svg && echo "tabler OK"
```

## 원칙

- 두 경로는 `.gitignore`로 관리되는 로컬 전용이다.
- 새 환경에서는 먼저 `python-setup` → 이 스킬 순서로 실행한다.
- 준비 완료 후 `manim-video-pipeline` 스킬을 사용한다.
