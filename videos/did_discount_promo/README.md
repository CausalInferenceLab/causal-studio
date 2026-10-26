# 할인 기획전 예약 순증분 — 인과추론 2분 영상 초안

예약 서비스의 할인 기획전을 예시로, 관찰된 예약 증가와 기획전의 인과 효과가 왜 다른지 설명하는 한국어 영상 초안입니다. DID는 반사실을 추정한 뒤 마지막에 이름과 계산식으로 소개합니다. 모든 예약 수치는 교육용 가상 수치입니다.

질문 → 단순 전후 비교의 함정 → 대조군 비교 → 평행추세 가정의 근거와 한계 → 반사실과 2주 순증분 1,000건. 다섯 장의 정지 화면 대신 21개 음성 문장에 맞춰 그래프와 숫자가 단계적으로 나타납니다. 문장별 화면 변화는 [`src/storyboard.md`](src/storyboard.md)에 기록했습니다.

- 참여 매장 100곳: 이전 2주 10,000건, 진행 2주 12,000건
- 대조군 매장 100곳: 이전 2주 8,000건, 진행 2주 9,000건
- DID = (12,000 - 10,000) - (9,000 - 8,000) = 1,000건
- 진행 2주 반사실 추정 예약 11,000건

`src/scripts/ko/`에 문장별 내레이션, `src/did_discount_promo_ko.py`에 Manim 애니메이션 원본이 있습니다. `src/slides.py`는 이전 정지 화면 초안의 기록이며 현재 렌더에는 사용하지 않습니다. 미리보기는 `preview/did_discount_promo_draft.mp4`입니다. 색상은 기존 Causal Studio RDD/Fuzzy RDD 영상에 맞추고, 한글 글꼴은 Pretendard Variable을 사용합니다. 어두운 배경은 3Blue1Brown의 신경망 입문 영상에서 참고했습니다. 음성은 ElevenLabs의 한국어 음성 Anna Kim과 `eleven_multilingual_v2` 모델로 생성했습니다.

재현 명령(저장소 루트에서):

```bash
.venv/bin/python videos/did_discount_promo/build_draft.py
```

이 명령은 문장별 ElevenLabs 음성 생성 → 타이밍 계산 → Manim 렌더 → 음성 합성을 진행합니다. 현재 길이는 약 1분 53초로, 2분 20초 상한 안에 있습니다. ElevenLabs 속도는 0.95이며 후처리 가속은 하지 않습니다. 음성만 다시 만들 때는 `--audio-only`, 저장된 타이밍으로 화면만 다시 만들 때는 `--render-only`를 사용합니다. `build/`는 Git에 포함하지 않습니다. 저장소 루트의 무시된 `.env`에 `ELEVENLABS_API_KEY`가 필요하며, Node.js, FFmpeg, 저장소 `.venv`, [Pretendard Variable](https://github.com/orioncactus/pretendard)이 설치되어 있어야 합니다. 음성을 바꾸려면 `ELEVENLABS_VOICE_ID` 환경변수를 설정합니다.

## 디자인 및 음성 참고

- [3Blue1Brown의 신경망 입문 영상](https://www.youtube.com/watch?v=aircAruvnKk): 어두운 바탕과 선명한 수학 시각화의 방향을 참고했습니다. 화면과 그래프는 이 프로젝트 수치로 새로 제작했습니다.
- Causal Studio `videos/rdd/src/rdd.py`, `videos/fuzzy_rdd/src/fuzzy_rdd.py`: 청록/금색/회색 강조색을 맞췄습니다. [Pretendard Variable](https://github.com/orioncactus/pretendard)은 한글 가독성을 위해 이 영상에 새로 적용했습니다.
- [ElevenLabs TTS API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert), [한국어 음성 안내](https://elevenlabs.io/text-to-speech/korean): 한국어 내레이션 생성에 사용했습니다. 저장소의 기존 `elevenlabs-audio` 명령은 실제로 OpenAI API를 호출하므로 이 영상에서는 사용하지 않습니다.
