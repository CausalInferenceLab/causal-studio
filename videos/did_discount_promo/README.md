# 할인 기획전 예약 순증분 — DID 2분 영상 초안

예약 서비스의 할인 기획전을 예시로 DID의 전후 변화 차이와 평행추세 가정을 소개하는 한국어 영상 초안입니다. 모든 예약 수치는 교육용 가상 수치입니다.

5컷: 질문 → 단순 전후 비교의 함정 → 대조군 비교 → 평행추세 가정 → 2주 순증분 1,000건.

- 참여 매장 100곳: 이전 2주 10,000건, 진행 2주 12,000건
- 대조군: 이전 2주 8,000건, 진행 2주 9,000건
- DID = (12,000 - 10,000) - (9,000 - 8,000) = 1,000건
- 진행 2주 반사실 추정 예약 11,000건

`src/scripts/ko/`에 컷별 내레이션 초안, `src/slides.py`에 그래프 원본, `src/did_discount_promo_ko.py`에 Manim 씬이 있습니다. 미리보기는 `preview/did_discount_promo_draft.mp4`입니다. 음성은 빠른 초안 제작을 위해 macOS 한국어 시스템 음성 Yuna를 사용했습니다.

재현 명령(저장소 루트에서):

```bash
.venv/bin/python videos/did_discount_promo/build_draft.py
```

이 명령은 화면 생성 → 컷별 임시 음성 → Manim 렌더 → 음성 합성을 진행합니다. `build/`는 Git에 포함하지 않습니다. macOS의 `say`, FFmpeg, 저장소 `.venv`가 필요합니다.
