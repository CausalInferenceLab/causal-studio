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
- 기본 플로우는 반드시 `script 작성 -> 사용자 확인 -> mp3/.timings.json 생성 -> 사용자 확인 -> scene code 작성` 순서를 따른다.
- 사용자가 명시적으로 "바로 다음 단계 진행"이라고 승인하기 전에는 다음 단계 파일을 만들지 않는다.
- `scene_outline.md`는 필수가 아니다. 기본적으로 만들지 않는다.
- Scene의 핵심 주장, 오해, visual pivot, 참고 영상, 선정 이유, script-to-beat mapping은 `src/{topic}.py`의 Scene docstring/주석에 남긴다.
- 새 Scene를 만들기 전에는 반드시 "직전 Scene의 마지막 스크립트 문장", "현재 Scene의 첫 스크립트 문장", "ipynb에서 해당하는 셀/문단 범위"를 먼저 확인한다.
- Scene 경계는 설명 단위가 자연스럽게 끊기는 지점에 둔다. 개념 정의 한가운데, 수식 도입 직전/직후, 예시 설명 중간처럼 애매한 지점에서 자르지 않는다.
- 이미 만든 Scene과 다음 Scene의 내용이 겹치거나, 다음 Scene이 앞 Scene 내용을 건너뛰지 않도록 경계를 먼저 검수한다.
- Scene docstring과 코드 주석은 기본적으로 한국어로 작성한다.
- 코드 주석은 단순히 `Beat 1`, `Beat 2`만 적지 말고, 해당 Beat가 스크립트의 어떤 설명을 화면에서 어떻게 처리하는지 드러내야 한다.
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
- 레이아웃은 "렌더 후 발견"이 아니라 "코드 작성 시점"에 먼저 검토한다. 새 Beat를 추가하기 전에는 각 요소가 어느 화면 영역을 쓰는지 먼저 정하고, 이전 Beat 요소가 남아 있으면 겹치지 않게 정리한 뒤 다음 요소를 올린다.
- 같은 Beat 안에서 새로 등장하는 핵심 덩어리는 기본적으로 2개를 넘기지 않는다. 3개 이상이 필요하면 Beat를 더 쪼갠다.
- 수식, 아이콘, 박스, 라벨을 함께 쓰는 장면에서는 최소 간격을 먼저 확보한다. 작은 화면 기준으로도 읽히지 않으면 실패로 보고 바로 레이아웃을 다시 짠다.
- 겹침이 반복되는 Scene은 "요소 수를 유지한 채 위치만 미세조정"하지 말고, 먼저 장면 구조를 줄이거나 Beat를 분리한다.
- Scene 코드 작성 전에는 반드시 Beat별로 아래 3가지를 먼저 메모한다: `지금 화면에 동시에 남아 있을 핵심 그룹 수`, `각 그룹의 화면 구획(상/중/하 또는 좌/우)`, `이 Beat 시작 전에 반드시 지워질 이전 요소`.
- Scene 코드 작성 전에는 반드시 Beat별로 아래 4가지를 먼저 메모한다: `지금 화면에 동시에 남아 있을 핵심 그룹 수`, `각 그룹의 화면 구획(상/중/하 또는 좌/우)`, `이 Beat 시작 전에 반드시 지워질 이전 요소`, `이 Beat에서 사용자가 실제로 읽어야 하는 단 하나의 핵심 대상`.
- 한 Beat에서 동시에 읽어야 하는 대상은 원칙적으로 1개, 최대 2개다. 큰 표/큰 수식/큰 카드 중 하나가 이미 있으면, 같은 Beat에 다른 큰 요소를 추가하지 않는다.
- 한 Beat에서 큰 요소는 원칙적으로 1개만 유지한다. 예외적으로 2개까지 허용되지만, 그 경우에도 서로 다른 화면 구획을 차지해야 하며 시선 경쟁이 없어야 한다.
- "설명 박스 + 긴 문장 + 큰 수식 + 아이콘 묶음"처럼 서로 다른 타입의 큰 요소 3개 이상을 동시에 유지하는 구성은 금지한다. 필요하면 연속 Beat로 분리한다.
- 이전 Beat의 큰 요소를 명시적으로 지우기 전에 다음 큰 요소를 추가하는 것은 금지한다. `FadeOut`, `Transform`, 축소 후 구석 이동 중 하나로 기존 요소의 역할이 정리되지 않았으면 다음 핵심 요소를 올리지 않는다.
- 새 Beat를 만들 때는 먼저 `무엇을 추가할지`가 아니라 `무엇을 제거할지`부터 정한다. 제거 대상이 불명확하면 그 Beat는 아직 설계가 끝난 것이 아니다.
- 렌더 전 자체 점검에서 `이 Beat의 주 시선이 즉시 한 곳으로 모이는가?`, `잔상 때문에 경쟁하는 구역이 없는가?`, `모든 요소가 480p에서도 구분되는가?`를 통과하지 못하면 렌더 전에 구조를 다시 짠다.
- 첫 debug 렌더에서 겹침/과밀이 보인 Scene은 다음 수정 때 위치 미세조정부터 하지 않는다. 우선 `요소 삭제`, `Beat 분리`, `이전 요소 조기 FadeOut` 중 하나를 먼저 적용한다.
- 첫 debug 렌더에서 물리적 겹침, 과밀, 시선 경쟁 중 하나라도 보이면 그 Scene은 "미완료" 상태다. 이 상태에서는 mux나 다음 Scene으로 진행하지 않는다.
- 첫 debug 렌더 실패 후에는 같은 구조를 유지한 채 좌표만 옮겨 다시 렌더하는 접근을 금지한다. 반드시 `요소 수 감소`, `Beat 분할`, `기존 요소 제거 시점 앞당김` 중 최소 1개를 먼저 적용한다.
- anatomy/레퍼런스 이미지를 참고할 때는 그림 전체를 한 Beat에 한꺼번에 옮기지 않는다. 한 컷당 핵심 구조 하나만 차용하고, 나머지는 다음 Beat로 분리한다.
- Beat 시각화 방식이 여러 가지로 가능할 때는 코드를 바로 작성하지 말고, AskUserQuestion 도구로 사용자에게 선택지를 제시한다. 선택지마다 `markdown` 필드에 ASCII 스케치(아이콘/화살표/박스 배치)를 넣어 시각적으로 비교할 수 있게 한다. 예: DAG, 분기 화살표, Before/After 카드, 산점도, 표 등 구체적인 레이아웃을 보여준다.

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

1. 현재 작업 Scene이 ipynb의 어디서 시작하고 어디서 끝나는지 경계를 먼저 정한다.
2. 현재 작업 Scene의 스크립트 파일 하나만 작성하거나 갱신한다.
3. 스크립트만 먼저 사용자에게 보여주고 확인을 받는다.
4. 승인된 스크립트로 mp3와 `.timings.json`을 만든다.
5. mp3와 `.timings.json`을 사용자에게 보여주고 확인을 받는다.
6. 승인된 스크립트와 타이밍을 기준으로 `src/{topic}.py`에 해당 Scene 클래스 하나만 작성하거나 갱신한다.
7. Scene docstring/주석에 핵심 주장, 오해, visual pivot, 참고 영상, 선정 이유, script-to-beat mapping과 scene 경계를 적는다.
8. `.timings.json` 기준으로 Scene 타이밍을 맞춘 뒤 저화질 code-only debug 렌더를 만든다.
9. code-only 영상 길이와 mp3 길이가 대체로 맞으면 scene별 mux 확인본을 만든다.
10. 사용자가 확인하고 수정 요청을 주면, 그 Scene만 반복 수정한다.
11. Scene이 확정된 뒤에만 다음 Scene으로 넘어간다.

중요:
- 사용자가 전체 일괄 생성을 명시적으로 요청하지 않으면, 여러 Scene의 스크립트/코드를 한꺼번에 만들지 않는다.
- 현재 Scene이 확인되지 않은 상태에서 다음 Scene으로 건너뛰지 않는다.
- 스크립트 단계에서는 `src/scripts/{NN}_{scene_name}.txt`까지만 만들고, 사용자 확인 전에는 mp3나 Scene 코드를 만들지 않는다.
- mp3와 `.timings.json` 단계에서는 `build/audio/{NN}_{scene_name}.mp3`, `build/audio/{NN}_{scene_name}.timings.json`까지만 만들고, 사용자 확인 전에는 Scene 코드를 만들지 않는다.
- mp3가 아직 없으면 mux 단계는 건너뛰고, 렌더 가능한 debug 영상까지 만든다.
- 기본 흐름은 항상 `script -> 사용자 확인 -> mp3/timings.json -> 사용자 확인 -> scene code -> render -> mux` 순서다.
- `.timings.json`이 아직 없는데 Scene 코드를 먼저 길게 밀어붙이지 않는다. 임시 코드는 가능하지만, 본격 타이밍 조정은 mp3와 `.timings.json` 생성 뒤에만 한다.
- mux는 "타이밍을 맞추는 단계"가 아니라, 이미 맞춘 video/audio를 합쳐 확인하는 단계다.
- `build/audio/{NN}_{scene_name}.timings.json`이 있으면, mux 전에 반드시 그 chunk 시간표를 Scene 코드의 Beat/wait/run_time 조정 기준으로 먼저 사용한다.
- mux 전에 code-only 영상 길이와 mp3 길이를 먼저 확인한다. 화면이 오디오보다 먼저 끝나면 mux 옵션으로 덮지 말고 Scene 코드로 돌아가 수정한다.
- 사용자가 "Scene 01부터"처럼 지정하지 않으면 첫 미완성 Scene부터 진행한다.
- 별도 요청이 없으면 `scene_outline.md`를 만들지 않는다.
- 다음 Scene 아이디어가 있더라도 파일로 길게 쌓아두지 말고, 필요하면 답변에서만 짧게 언급한다.
- Scene 코드를 수정한 뒤에는 같은 턴에서 바로 `preview/code/{NN}_{scene_name}_code.mp4`를 다시 생성해 결과를 확인한다.
- Scene 내부 주석은 한국어로 쓰고, "왜 이 화면이 필요한가", "어떤 스크립트 문단을 처리하는가", "다음 Beat로 왜 넘어가는가"가 보이게 적는다.
- 새 Scene를 시작할 때는 답변이나 docstring에 최소한 아래를 남긴다:
  - 직전 Scene 마지막 문장
  - 현재 Scene 첫 문장
  - ipynb 기준 시작/끝 셀 또는 문단
- 새 아이콘이 필요하면 토픽별 `videos/{topic}/assets/`보다 먼저 공용 `videos/assets/`에 두어 다른 영상에서도 재사용 가능하게 한다.
- `build/` 루트에는 사람이 직접 확인하는 결과물만 둔다. Manim이 자동 생성하는 `Tex/`, `texts/`, `images/`, `videos/`는 모두 `build/manim/` 아래로 모은다.
- 빠른 확인용 산출물은 `build/`가 아니라 `preview/` 아래에 둔다. 즉 test 결과물은 `preview/code/`, `preview/mux/`를 사용한다.
- 렌더 전에 Beat별 화면 스케치를 코드 주석 수준으로라도 남긴다. 예: "상단은 제목, 좌측은 T_i, 우측 위/아래는 분기"처럼 미리 공간 점유를 적고 시작한다.
- 렌더 전에 Beat별 주석에는 최소한 `남는 요소`, `새로 등장하는 요소`, `비워 두는 화면 영역`, `이 Beat의 단일 핵심 시선 대상`을 적는다. 이 넷 중 하나라도 빠지면 레이아웃 검토가 불충분한 것으로 본다.
- 코드 작성이 끝난 뒤 렌더 전에 Beat 주석만 따로 읽었을 때, 각 Beat에서 "무엇을 먼저 지우고 무엇만 읽게 하는지"가 즉시 드러나지 않으면 아직 렌더 단계로 넘어가면 안 된다.
- 렌더 후 QA에서 겹침이 보이면, 다음 수정은 항상 "무엇을 지울지 / 무엇을 다음 Beat로 보낼지"부터 결정하고 나서 위치 조정을 한다.
- QA에서 첫 확인 항목 순서는 반드시 `물리적 겹침 -> 최소 간격 -> 시선 경쟁 -> 정보 과밀 -> 타이밍`이다. 앞 단계에서 실패하면 뒤 단계 판단은 보류한다.
- 물리적 겹침이 1개라도 있거나, 480p에서 한 Beat의 주 시선 대상이 즉시 구분되지 않으면 그 렌더는 실패다. "대체로 괜찮다"로 처리하지 않는다.

현재 Scene 작업 산출물:
- `src/scripts/{NN}_{scene_name}.txt`
- 사용자 승인 후 `build/audio/{NN}_{scene_name}.mp3`
- 사용자 승인 후 `build/audio/{NN}_{scene_name}.timings.json`
- `src/{topic}.py`의 해당 Scene 클래스
- `preview/code/{NN}_{scene_name}_code.mp4`
- mp3가 있으면 `preview/mux/{NN}_{scene_name}_mux.mp4`
- 사용자가 만족하면 `build/final/{NN}_{scene_name}_hq.mp4`
- 여러 scene이 확정되면 `build/final/{topic}_full.mp4`

권장 응답 방식:
- 지금 작업 중인 Scene 번호와 이름을 명확히 말한다.
- 방금 만든 파일, 아직 없는 파일, 다음 확인 포인트를 짧게 정리한다.
- 스크립트 단계에서는 "이 스크립트로 mp3 생성 진행할지"를 확인 포인트로 둔다.
- 오디오 단계에서는 "이 mp3/.timings.json 기준으로 코드 작성 진행할지"를 확인 포인트로 둔다.

### 1. 스크립트 작성
Scene 구조 기반 내레이션 스크립트 생성 (한국어).
→ `references/script-writing-guide.md` 참조

기본값:
- 원본 `ipynb`의 논리 전개, 예시, 수식 도입 순서를 최대한 보존한다.
- Scene를 나눌 때는 한 Scene 안에서 하나의 설명 단위가 마무리되도록 자른다.
- 특히 "정의 -> 해석", "예시 제시 -> 예시 해석", "수식 제시 -> 수식 의미 설명"은 가능하면 같은 Scene에 둔다.
- 새 Scene 첫 문장은 ipynb에서 실제로 다음 설명이 시작되는 문장이어야 한다. 임의 요약 문장이나 앞뒤 문단을 섞은 시작은 피한다.
- 스크립트를 지나치게 요약하지 않는다. 단순 개요 수준 문장 몇 개로 끝내지 않는다.
- Scene마다 원본의 핵심 설명, 오해 교정, 수식 의미, 예시 해석이 살아 있어야 한다.
- 줄이는 대상은 중복 표현이지, 개념 설명 자체가 아니다.
- 이 단계의 종료 조건은 스크립트 파일 저장이 아니라 사용자 승인이다.
- 사용자가 승인하기 전에는 mp3 생성이나 Scene 코드 작성으로 넘어가지 않는다.

### 2. 오디오 생성 (외부)
스크립트를 TTS(ElevenLabs/Piper)로 mp3 변환.
- 기본 ElevenLabs 생성 스크립트: `scripts/generate_elevenlabs_audio.mjs`
- API 키는 repo root `.env`의 `ELEVENLABS_API_KEY`를 사용한다.
- voice_id는 `7Nah3cbXKVmGX7gQUuwz`를 고정으로 사용한다.
- model은 `eleven_multilingual_v2`, output format은 `mp3_44100_128`을 사용한다.
- 출력: `videos/{topic}/build/audio/{NN}_{scene_name}.mp3`
- 동시에 chunk별 timing 메타데이터를 `videos/{topic}/build/audio/{NN}_{scene_name}.timings.json`에 저장한다.
- 스크립트 파일을 그대로 읽어 음성을 만들고, 파일명은 scene 번호와 scene 이름을 유지한다.
- 긴 스크립트는 문단 단위로 나눠 여러 번 생성한 뒤 하나의 mp3로 합쳐, 말 꼬임이나 글리치를 줄인다.
- `.timings.json`에는 chunk별 `text`, `start`, `end`, `duration`이 들어가며, 이후 Scene 타이밍 조정의 1차 기준으로 사용한다.
- 이 파일은 mux 스크립트의 입력이 아니라, mux 전에 Scene 코드 타이밍을 맞추기 위한 기준 데이터다.
- 이 단계가 끝나면 mp3와 `.timings.json`을 사용자에게 공유하고 승인을 받는다.
- 사용자가 승인하기 전에는 Scene 코드를 작성하지 않는다.

### 3. Scene 코드 작성
스크립트+오디오 길이에 맞춰 Manim Scene 클래스 구현.
→ `references/manim-code-patterns.md` 참조

기본값:
- Scene 코드는 승인된 스크립트와 승인된 mp3, `.timings.json`이 준비된 뒤에만 작성한다.
- Scene 코드를 쓰기 전에는 반드시 아래 4가지를 먼저 읽고 메모한다:
  - `build/audio/{NN}_{scene_name}.timings.json`
  - 현재 Scene에 해당하는 ipynb의 markdown 셀
  - 그 설명 바로 앞뒤의 ipynb code 셀과 거기서 쓰는 표/데이터 값
  - 직전 Scene 클래스 코드
- 즉, 현재 Scene 코드 작성은 스크립트만 보고 바로 시작하지 말고, ipynb의 "설명 + 코드 + 데이터"와 직전 Scene의 마지막 화면 상태를 함께 확인한 뒤 시작한다.
- `src/{topic}.py`는 현재 Scene 하나씩 점진적으로 확장한다.
- 기존 Scene이 있으면 그 아래에 다음 Scene 클래스를 추가한다.
- 아직 확정되지 않은 뒤쪽 Scene의 코드를 미리 대량 생성하지 않는다.
- 3b1b 참조 영상이 있으면 장면 전환, 강조, 레이아웃 리듬을 참고하되 CE 문법으로 다시 쓴다.
- Scene 메타정보는 별도 outline 파일 대신 Scene docstring/주석에 남긴다.
- `src/scripts/{NN}_{scene_name}.txt`를 먼저 읽고, 코드의 Beat 구성은 그 스크립트 순서와 정보량을 따라야 한다.
- ipynb에 같은 장면의 표 생성 코드나 예시 데이터가 있으면, Scene 코드의 숫자/행/열/결측 표현은 그 원본과 일치시킨다.
- ipynb code 셀에 `pd.DataFrame(...)`, dict, numpy 배열, csv 로드 코드가 있으면 해당 값과 컬럼명을 직접 확인하고 사용한다.
- ipynb에서 `np.nan`처럼 결측을 쓴 경우, 화면에서도 "비어 있음 / hidden / 가려짐"이 아니라 "관찰 불가"라는 의미가 유지되도록 표현을 정한다.
- 직전 Scene이 사용한 표 구조, 색 의미, 레이아웃 축을 특별한 이유 없이 버리지 않는다. 다음 Scene은 가능한 한 그 화면 문법을 이어받아 자연스럽게 변형한다.
- 새 Scene 시작 2~5초 안에는 사용자가 "직전 Scene에서 무엇이 어떻게 바뀌었는지"를 알아볼 수 있어야 한다.
- 스크립트에 있는 핵심 설명, 예시, 질문, 수식 해석이 화면에서 빠지지 않도록 장면 수와 전환을 설계한다.
- 스크립트보다 코드가 지나치게 짧거나, 스크립트 문단 여러 개를 화면 한 컷으로 뭉개지 않는다.
- mp3가 없더라도, debug render만 보고 "너무 빠르다"는 피드백이 나오지 않도록 충분한 정지 구간과 단계적 전환을 넣는다.
- on-screen text는 가능한 한 짧게 유지한다. 문단을 화면에 그대로 올리는 방식은 기본적으로 피한다.
- 설명량이 많아도 화면은 도형, 수식, 관계선, 강조 박스, 간단한 라벨 중심으로 설계한다.
- 텍스트를 줄였다고 정보가 빠지면 안 된다. 빠진 정보는 시각 구조와 beat 수로 보완한다.
- 아이콘이 필요한 경우에는 손그림보다 `videos/assets/tabler-icons/icons/outline/*.svg` 같은 공용 라이브러리 자산을 우선 사용한다.
- `build/audio/{NN}_{scene_name}.timings.json`이 있으면, 먼저 그 chunk 시간표를 읽고 Beat 길이의 초안을 잡는다.
- 기본적으로는 `.timings.json` 없이 Scene 코드를 확정하지 않는다.
- 문단/문장 chunk와 Beat를 대략 1:1 또는 소수의 chunk 묶음으로 대응시키고, 화면 전환 시점이 오디오보다 먼저 끝나지 않게 한다.
- 자동 타이밍은 출발점일 뿐이다. 최종적으로는 mux 결과를 보고 어색한 구간만 미세 조정한다.
- code-only 영상 길이가 mp3보다 짧으면, `WAIT_TAIL`, Beat 사이 `self.wait()`, 개별 `run_time`, Beat 분할을 먼저 조정한다. `mux_audio.sh --full` 같은 방식으로 문제를 가리지 않는다.
- 레이아웃 초안 단계에서 각 Mobject의 예상 자리와 크기를 먼저 잡고, 한 화면 안에서 위/가운데/아래 또는 좌/우 구획 중 어디를 쓰는지 명시한다.
- 같은 시간에 보이는 그룹끼리는 바운딩 박스가 겹치지 않아야 한다. 겹칠 가능성이 있으면 `scale`, `arrange`, `next_to`, `to_edge`만 미세 조정하지 말고 장면을 둘로 나눈다.
- 표, 수식, 설명 박스가 함께 있는 장면은 표를 기준축으로 두고 나머지 요소 수를 줄인다. 표 위에 또 다른 큰 박스나 긴 문장을 동시에 올리는 구성은 기본적으로 금지한다.
- 현재 Scene이 직전 Scene의 표/그래프를 이어받는 경우, 기본값은 "새로 만들기"가 아니라 "직전 구조를 남긴 채 일부 열을 숨기거나 강조를 바꾸는 변형"이다.
- Scene 코드 작성 전에 답변 또는 docstring에 최소한 아래를 남긴다:
  - 참고한 ipynb 셀 번호
  - 참고한 ipynb code 셀의 핵심 데이터/수식
  - 직전 Scene에서 이어받는 시각 요소
  - `.timings.json` 기준으로 어떤 chunk를 어떤 Beat에 대응시킬지

### 4. 렌더 + 오디오 싱크
개별 Scene 렌더 후 오디오 합성.
→ `references/ffmpeg-recipes.md` 참조

기본값:
- 먼저 저화질 debug 렌더로 화면 리듬과 레이아웃을 확인한다.
- debug render 직후 반드시 혼잡도 QA를 수행한다.
- 텍스트 겹침, 시선 분산, 한 화면 동시 정보 과다, 너무 빠른 전환이 보이면 바로 코드로 돌아가 수정한다.
- QA를 통과하지 못한 render는 다음 단계로 넘기지 않는다.
- QA에서 첫 확인 항목은 "물리적 겹침"이다. 하나라도 겹치면 다른 판단보다 우선해서 수정한다.
- 물리적 겹침이 없더라도 서로 너무 가까워 읽기 어려우면 실패로 본다. 최소 간격이 부족하면 동일 Beat 내 요소 수를 줄인다.
- mp3를 받은 뒤에만 mux를 수행한다.
- mux 전에 `ffprobe`로 code-only 영상과 mp3 길이를 먼저 비교한다.
- 길이 차이가 크면 mux를 바로 만들지 말고 Scene 코드로 돌아가 `.timings.json` 기준으로 다시 맞춘 뒤 렌더를 재생성한다.
- scene별 code-only 결과물은 `preview/code/{NN}_{scene_name}_code.mp4`
- scene별 mux 결과물은 `preview/mux/{NN}_{scene_name}_mux.mp4`
- 기본 mux는 480p 테스트용이며, 타이밍 보정 기능은 없다. 단순히 video/audio를 합쳐 검수용 mp4를 만든다.
- 사용자가 해당 scene 결과에 만족하면, 고화질로 다시 렌더하거나 mux해서 `build/final/{NN}_{scene_name}_hq.mp4`로 따로 저장한다.
- `build/final/`에는 scene별 hq 결과와 전체 합본만 둔다.
- Manim 렌더는 항상 `--media_dir build/manim`으로 실행해 중간 산출물이 `build/` 루트에 흩어지지 않게 한다.
- mux 결과를 확인한 뒤 다음 Scene으로 넘어간다.

### 5. 전체 합본
개별 debug mp4들을 순서대로 합쳐 최종 영상 생성.
→ `references/ffmpeg-recipes.md` 참조

기본값:
- scene별 `build/final/{NN}_{scene_name}_hq.mp4`가 준비되면 `scripts/concat_videos.sh`로 `build/final/{topic}_full.mp4`를 만든다.
- 사용자가 최종 영상에 배경음악을 원하면, 합본 완료 후에만 `scripts/mix_bgm.sh`로 `build/final/{topic}_full_bgm.mp4`를 추가 생성한다.
- BGM은 내레이션보다 항상 훨씬 작아야 하며, 교육 영상 기본 시작값은 `--bgm-volume 0.08 ~ 0.12` 범위다.
- BGM은 scene별 mux 단계에 미리 넣지 않는다. 최종 합본 단계에서 한 번만 넣는다.

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

### 최종 합본 + BGM
```bash
cd videos/{topic} && ../../.claude/skills/manim-video-pipeline/scripts/mix_bgm.sh \
  build/final/{topic}_full.mp4 \
  path/to/bgm.mp3 \
  build/final/{topic}_full_bgm.mp4 \
  --bgm-volume 0.10
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

배경음악까지 넣는 경우:
```bash
cd videos/{topic} && ../../.claude/skills/manim-video-pipeline/scripts/mix_bgm.sh \
  build/final/{topic}_full.mp4 \
  path/to/bgm.mp3 \
  build/final/{topic}_full_bgm.mp4 \
  --bgm-volume 0.10
```

## 단계별 상세 가이드

각 단계의 상세 지침은 references/ 하위 파일 참조:

| 작업 | 참조 파일 |
|-----|----------|
| 스크립트 작성 | `references/script-writing-guide.md` |
| Manim 코드 작성 | `references/manim-code-patterns.md` |
| 렌더/합성/합본 | `references/ffmpeg-recipes.md` |
