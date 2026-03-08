---
name: manim-video-pipeline
description: |
  Manim Community Edition 기반 교육 영상 제작 파이프라인.
  ipynb/개념 문서를 Scene 구조로 설계하고, 내레이션 스크립트 작성,
  Manim 코드 생성, 오디오 싱크, 최종 합본까지 전 과정을 지원한다.

  트리거: "manim 영상", "scene 설계", "scene 구조", "스크립트 작성",
  "scene 렌더", "영상 합치기", "오디오 싱크", "debug 영상", "full video"
---

# Manim Video Pipeline

Manim CE 기반 교육 영상 제작 워크플로우.

기본 모드는 "전체를 한 번에 생성"이 아니라 "Scene 단위 반복"이다.
별도 요청이 없으면 항상 현재 Scene 하나만 완성 가능한 상태까지 진행하고,
사용자 확인 후 다음 Scene으로 넘어간다.

가장 중요한 운영 규칙:
- `scene_outline.md`는 필수가 아니다. 기본적으로 만들지 않는다.
- Scene의 핵심 주장, 오해, visual pivot, 참고 영상, 선정 이유, script-to-beat mapping은 `src/{topic}.py`의 Scene docstring/주석에 남긴다.
- 아직 작업하지 않는 다음 Scene들을 미리 script/code에 길게 쌓아두지 않는다.
- 사용자가 참고할 3b1b 영상을 주면, 그 영상을 직접 참조해 script와 code를 만든다.
- 사용자가 참고 영상을 주지 않으면, 로컬 `3b1b/videos` 안에서 현재 ipynb 주제, scene 목표, 연출 방식과 가장 비슷한 파일을 골라 참조한다.
- 3b1b 코드는 복붙하지 말고, 현재 Manim CE 버전에 맞게 구조와 표현만 참고해 재구현한다.
- 화면 글자는 기본적으로 최소화한다. 자세한 설명은 mp3/스크립트가 맡고, 화면은 앵커 단어, 짧은 수식, 도형, 색, 위치 변화로 전달한다.
- 같은 내용을 긴 문장 자막으로 다시 쓰지 않는다. 문장이 필요해도 헤드라인 수준으로 제한한다.
- 설명 가능한 경우 텍스트보다 도형, 아이콘, 화살표, 표, 그래프, 수식을 우선 사용한다.
- 코드가 수정되면 그 턴 안에 반드시 최소 1회 렌더까지 수행한다. 코드만 바꾸고 렌더 확인 없이 끝내지 않는다.
- 아이콘이 필요하면 직접 그리지 말고 공용 오픈소스 아이콘 라이브러리를 우선 사용한다.
- 기본 공용 경로는 `videos/assets/tabler-icons/`이고, Scene 코드에서는 여기의 SVG를 `SVGMobject`로 불러온다.
- `3b1b/` 또는 `videos/assets/tabler-icons/`가 없으면 먼저 repo 스코프 `video-assets-setup` 스킬로 로컬 자산을 준비한다.

## 프로젝트 구조

```text
videos/{topic}/
├── src/
│   ├── {topic}.py              # Manim Scene 클래스 모음
│   └── scripts/
│       ├── 01_{scene_name}.txt # 씬별 내레이션 스크립트
│       └── ...
├── preview/
│   ├── code/
│   │   ├── 01_{scene_name}_code.mp4
│   │   └── ...
│   └── mux/
│       ├── 01_{scene_name}_mux.mp4
│       └── ...
└── build/
    ├── manim/                  # Manim 내부 캐시/중간 산출물 전용
    │   ├── Tex/
    │   ├── texts/
    │   ├── images/
    │   └── videos/
    ├── audio/
    │   ├── 01_{scene_name}.mp3 # 씬별 오디오 (TTS 생성)
    │   └── ...
    └── final/
        ├── 01_{scene_name}_hq.mp4
        └── {topic}_full.mp4
```

## 관련 코드북 노트북

```text
book/{topic}/{topic}.ipynb
```

- 영상의 원본 콘텐츠 (개념, 수식, 코드)
- 영상 완성 후 YouTube ID를 이 노트북에 임베드

## 3Blue1Brown 참고 입력 (선택)

아래 인자를 함께 전달하면 3b1b 스타일 참조를 명시적으로 반영한다.

- `topic`: 작업 토픽명 (예: `why_causal_inference`, `iv`)
- `ref_video`: 3b1b Manim 코드 경로 (예: `3b1b/videos/_2020/covid.py`)
- `ref_transcript`: 3b1b 자막 경로 (예: `3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt`)
- `ref_sentence_timings`: 문장 타이밍 경로 (예: `3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json`)

Codex 호출 예:
```bash
$manim-video-pipeline topic=iv ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json
```

Claude 호출 예:
```bash
/manim-video-pipeline topic=iv ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json
```

자연어 호출 예:

```text
iv 토픽으로 진행하고 ref_video=3b1b/videos/_2020/covid.py ref_transcript=3b1b/captions/2020/exponential-and-epidemics/english/transcript.txt ref_sentence_timings=3b1b/captions/2020/exponential-and-epidemics/english/sentence_timings.json 참고해서 scene 구조 설계해줘
```

참조 영상 규칙:
- `ref_video`가 주어지면 그 파일을 우선 참조한다.
- `ref_video`가 없으면 로컬 `3b1b/videos`에서 현재 ipynb 주제, scene의 핵심 메시지, 필요한 연출 타입이 가장 비슷한 파일을 고른다.
- 단순 랜덤 선택은 금지한다.
- 선택 이유를 한 줄로 남긴다. 예: "질문 나열형 인트로 구조가 유사해서", "표/수식 전개 리듬이 유사해서"
- 참조 대상을 정했으면, 현재 Scene의 코드 docstring/주석에 어떤 파일을 참조했는지 명시한다.
- 참조는 화면 구성, 전환 리듬, 강조 방식에 한정한다.
- 현재 프로젝트 코드는 Manim CE 기준으로 새로 작성한다.

## 워크플로우 단계

## 기본 작업 모드: Scene 단위 반복

기본 순서는 아래와 같다.

1. 현재 작업 Scene의 스크립트 파일 하나만 작성하거나 갱신한다.
2. `src/{topic}.py`에 해당 Scene 클래스 하나만 작성하거나 갱신한다.
3. Scene docstring/주석에 핵심 주장, 오해, visual pivot, 참고 영상, 선정 이유, script-to-beat mapping을 적는다.
4. 저화질 code-only debug 렌더를 만든다.
5. 사용자가 해당 Scene용 mp3를 제공하면 scene별 mux 확인본을 만든다.
6. 사용자가 확인하고 수정 요청을 주면, 그 Scene만 반복 수정한다.
7. Scene이 확정된 뒤에만 다음 Scene으로 넘어간다.

중요:
- 사용자가 전체 일괄 생성을 명시적으로 요청하지 않으면, 여러 Scene의 스크립트/코드를 한꺼번에 만들지 않는다.
- 현재 Scene이 확인되지 않은 상태에서 다음 Scene으로 건너뛰지 않는다.
- mp3가 아직 없으면 mux 단계는 건너뛰고, 렌더 가능한 debug 영상까지 만든다.
- 사용자가 "Scene 01부터"처럼 지정하지 않으면 첫 미완성 Scene부터 진행한다.
- 별도 요청이 없으면 `scene_outline.md`를 만들지 않는다.
- 다음 Scene 아이디어가 있더라도 파일로 길게 쌓아두지 말고, 필요하면 답변에서만 짧게 언급한다.
- Scene 코드를 수정한 뒤에는 같은 턴에서 바로 `preview/code/{NN}_{scene_name}_code.mp4`를 다시 생성해 결과를 확인한다.
- 새 아이콘이 필요하면 토픽별 `videos/{topic}/assets/`보다 먼저 공용 `videos/assets/`에 두어 다른 영상에서도 재사용 가능하게 한다.
- `build/` 루트에는 사람이 직접 확인하는 결과물만 둔다. Manim이 자동 생성하는 `Tex/`, `texts/`, `images/`, `videos/`는 모두 `build/manim/` 아래로 모은다.
- 빠른 확인용 산출물은 `build/`가 아니라 `preview/` 아래에 둔다. 즉 test 결과물은 `preview/code/`, `preview/mux/`를 사용한다.

현재 Scene 작업 산출물:
- `src/scripts/{NN}_{scene_name}.txt`
- `src/{topic}.py`의 해당 Scene 클래스
- `preview/code/{NN}_{scene_name}_code.mp4`
- mp3가 있으면 `preview/mux/{NN}_{scene_name}_mux.mp4`
- 사용자가 만족하면 `build/final/{NN}_{scene_name}_hq.mp4`
- 여러 scene이 확정되면 `build/final/{topic}_full.mp4`

권장 응답 방식:
- 지금 작업 중인 Scene 번호와 이름을 명확히 말한다.
- 방금 만든 파일, 아직 없는 파일, 다음 확인 포인트를 짧게 정리한다.

### 1. 스크립트 작성
Scene 구조 기반 내레이션 스크립트 생성 (한국어).
→ `references/script-writing-guide.md` 참조

기본값:
- 원본 `ipynb`의 논리 전개, 예시, 수식 도입 순서를 최대한 보존한다.
- 스크립트를 지나치게 요약하지 않는다. 단순 개요 수준 문장 몇 개로 끝내지 않는다.
- Scene마다 원본의 핵심 설명, 오해 교정, 수식 의미, 예시 해석이 살아 있어야 한다.
- 줄이는 대상은 중복 표현이지, 개념 설명 자체가 아니다.

### 2. 오디오 생성 (외부)
스크립트를 TTS(ElevenLabs/Piper)로 mp3 변환.
- 기본 ElevenLabs 생성 스크립트: `scripts/generate_elevenlabs_audio.mjs`
- API 키는 repo root `.env`의 `ELEVENLABS_API_KEY`를 사용한다.
- voice_id는 `7Nah3cbXKVmGX7gQUuwz`를 고정으로 사용한다.
- model은 `eleven_multilingual_v2`, output format은 `mp3_44100_128`을 사용한다.
- 출력: `videos/{topic}/build/audio/{NN}_{scene_name}.mp3`
- 스크립트 파일을 그대로 읽어 음성을 만들고, 파일명은 scene 번호와 scene 이름을 유지한다.
- 긴 스크립트는 문단 단위로 나눠 여러 번 생성한 뒤 하나의 mp3로 합쳐, 말 꼬임이나 글리치를 줄인다.

### 3. Scene 코드 작성
스크립트+오디오 길이에 맞춰 Manim Scene 클래스 구현.
→ `references/manim-code-patterns.md` 참조

기본값:
- `src/{topic}.py`는 현재 Scene 하나씩 점진적으로 확장한다.
- 기존 Scene이 있으면 그 아래에 다음 Scene 클래스를 추가한다.
- 아직 확정되지 않은 뒤쪽 Scene의 코드를 미리 대량 생성하지 않는다.
- 3b1b 참조 영상이 있으면 장면 전환, 강조, 레이아웃 리듬을 참고하되 CE 문법으로 다시 쓴다.
- Scene 메타정보는 별도 outline 파일 대신 Scene docstring/주석에 남긴다.
- `src/scripts/{NN}_{scene_name}.txt`를 먼저 읽고, 코드의 Beat 구성은 그 스크립트 순서와 정보량을 따라야 한다.
- 스크립트에 있는 핵심 설명, 예시, 질문, 수식 해석이 화면에서 빠지지 않도록 장면 수와 전환을 설계한다.
- 스크립트보다 코드가 지나치게 짧거나, 스크립트 문단 여러 개를 화면 한 컷으로 뭉개지 않는다.
- mp3가 없더라도, debug render만 보고 "너무 빠르다"는 피드백이 나오지 않도록 충분한 정지 구간과 단계적 전환을 넣는다.
- on-screen text는 가능한 한 짧게 유지한다. 문단을 화면에 그대로 올리는 방식은 기본적으로 피한다.
- 설명량이 많아도 화면은 도형, 수식, 관계선, 강조 박스, 간단한 라벨 중심으로 설계한다.
- 텍스트를 줄였다고 정보가 빠지면 안 된다. 빠진 정보는 시각 구조와 beat 수로 보완한다.
- 아이콘이 필요한 경우에는 손그림보다 `videos/assets/tabler-icons/icons/outline/*.svg` 같은 공용 라이브러리 자산을 우선 사용한다.

### 4. 렌더 + 오디오 싱크
개별 Scene 렌더 후 오디오 합성.
→ `references/ffmpeg-recipes.md` 참조

기본값:
- 먼저 저화질 debug 렌더로 화면 리듬과 레이아웃을 확인한다.
- debug render 직후 반드시 혼잡도 QA를 수행한다.
- 텍스트 겹침, 시선 분산, 한 화면 동시 정보 과다, 너무 빠른 전환이 보이면 바로 코드로 돌아가 수정한다.
- QA를 통과하지 못한 render는 다음 단계로 넘기지 않는다.
- mp3를 받은 뒤에만 mux를 수행한다.
- scene별 code-only 결과물은 `preview/code/{NN}_{scene_name}_code.mp4`
- scene별 mux 결과물은 `preview/mux/{NN}_{scene_name}_mux.mp4`
- 기본 mux는 480p 테스트용이다.
- 사용자가 해당 scene 결과에 만족하면, 고화질로 다시 렌더하거나 mux해서 `build/final/{NN}_{scene_name}_hq.mp4`로 따로 저장한다.
- `build/final/`에는 scene별 hq 결과와 전체 합본만 둔다.
- Manim 렌더는 항상 `--media_dir build/manim`으로 실행해 중간 산출물이 `build/` 루트에 흩어지지 않게 한다.
- mux 결과를 확인한 뒤 다음 Scene으로 넘어간다.

### 5. 전체 합본
개별 debug mp4들을 순서대로 합쳐 최종 영상 생성.
→ `references/ffmpeg-recipes.md` 참조

### 6. YouTube 업로드 + 노트북 임베드
완성 영상을 YouTube에 업로드하고, `book/{topic}/{topic}.ipynb`에 임베드.

## 빠른 명령어

### Scene 렌더
```bash
cd videos/{topic} && manim -pql --media_dir build/manim src/{topic}.py Scene{NN}_{ClassName}
```

### 오디오 합성
```bash
../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh {video.mp4} {audio.mp3} {output.mp4}
```

### ElevenLabs 오디오 생성
```bash
cd .claude/skills/manim-video-pipeline && \
npm run elevenlabs-audio -- --topic {topic} --scene 01 --name {scene_name}
```

직접 script 경로를 줄 수도 있다:
```bash
cd .claude/skills/manim-video-pipeline && \
npm run elevenlabs-audio -- --topic {topic} --scene 01 --name {scene_name} \
  --script ../../../videos/{topic}/src/scripts/01_{scene_name}.txt
```

### 현재 Scene 반복 루프 예시
```bash
# 1) Scene 01 코드 작성 후 debug 렌더
cd videos/{topic} && manim -pql --media_dir build/manim src/{topic}.py Scene01_{ClassName}

# 2) code-only 480p 테스트 영상 정리
mkdir -p preview/code && \
cp build/manim/videos/{topic}/480p15/{scene01_video}.mp4 preview/code/01_{scene_name}_code.mp4

# 3) mp3를 받은 뒤 480p 테스트 mux
../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh \
  preview/code/01_{scene_name}_code.mp4 \
  build/audio/01_{scene_name}.mp3 \
  preview/mux/01_{scene_name}_mux.mp4

# 4) 사용자가 만족하면 고화질 저장
manim -pqh --media_dir build/manim src/{topic}.py Scene01_{ClassName}
# 또는 고화질 렌더 결과와 오디오를 mux하여
# build/final/01_{scene_name}_hq.mp4 로 저장
```

### 전체 합본
```bash
cd videos/{topic} && ../../.claude/skills/manim-video-pipeline/scripts/concat_videos.sh build/final/ build/final/{topic}_full.mp4
```

## 단계별 상세 가이드

각 단계의 상세 지침은 references/ 하위 파일 참조:

| 작업 | 참조 파일 |
|-----|----------|
| 스크립트 작성 | `references/script-writing-guide.md` |
| Manim 코드 작성 | `references/manim-code-patterns.md` |
| 렌더/합성/합본 | `references/ffmpeg-recipes.md` |
