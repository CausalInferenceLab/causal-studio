# FFmpeg Recipes

렌더된 Manim 영상과 오디오 합성, 최종 합본을 위한 ffmpeg 레시피.

기본 원칙:
- Scene별 debug render와 mux 확인을 먼저 끝낸 뒤 다음 Scene으로 진행한다.
- Manim이 자동 생성하는 중간 산출물은 항상 `build/manim/` 아래에 둔다.
- scene별 code-only 산출물은 `preview/code/` 아래에 둔다.
- scene별 mux 산출물은 `preview/mux/` 아래에 둔다.
- scene별 hq 산출물은 `build/final/` 아래에 둔다.
- 전체 합본은 여러 Scene이 검수된 뒤 마지막 단계에서만 수행한다.
- `build/final/`은 scene별 hq와 전체 합본만 저장한다.

## 1. 렌더된 mp4 찾기

### 최신 렌더 파일 찾기
```bash
find build/manim/videos/ -name "*.mp4" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-
```

### Scene 이름으로 찾기
```bash
find build/manim/videos/*{SCENE_NAME}* -name "*.mp4" | head -1
```

## 2. 오디오 합성 (Mux)

### 기본 합성
```bash
ffmpeg -i {VIDEO} -i {AUDIO} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {OUTPUT}
```

### 오디오가 더 긴 경우 (영상 길이에 맞춤)
```bash
ffmpeg -i {VIDEO} -i {AUDIO} -c:v copy -c:a aac -shortest {OUTPUT}
```

### 영상이 더 긴 경우 (무음 패딩)
```bash
ffmpeg -i {VIDEO} -i {AUDIO} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {OUTPUT}
```

## 3. 길이 측정

### 영상/오디오 길이 확인
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {FILE}
```

### 둘 다 확인
```bash
echo "Video:" && ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {VIDEO}
echo "Audio:" && ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {AUDIO}
```

## 4. 전체 합본

### Step 1: 파일 리스트 생성
```bash
ls build/final/*_hq.mp4 preview/mux/*_mux.mp4 preview/code/*_code.mp4 2>/dev/null | sort -t'/' -k2 | uniq | while read f; do echo "file '$f'"; done > /tmp/filelist.txt
```

### Step 2-A: 무손실 합치기 (동일 코덱/해상도)
```bash
ffmpeg -f concat -safe 0 -i /tmp/filelist.txt -c copy build/final/{TOPIC}_full.mp4
```

### Step 2-B: 재인코딩 합치기 (해상도/프레임레이트 다를 때)
```bash
ffmpeg -f concat -safe 0 -i /tmp/filelist.txt \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  build/final/{TOPIC}_full.mp4
```

### Step 2-C: filter_complex 사용 (가장 안정적)
```bash
ffmpeg -f concat -safe 0 -i /tmp/filelist.txt \
  -filter_complex "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k \
  build/final/{TOPIC}_full.mp4
```

## 5. 검증

### 합본 길이 확인
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 build/final/{TOPIC}_full.mp4
```

### 개별 영상 길이 합계
```bash
for f in build/final/*_hq.mp4 preview/mux/*_mux.mp4 preview/code/*_code.mp4; do
  ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f"
done | awk '{sum+=$1} END {print sum}'
```

## 6.5 Scene별 저장 규칙

- 코드만으로 생성한 480p 테스트 영상: `preview/code/{NN}_{scene_name}_code.mp4`
- 코드+음성 480p 테스트 영상: `preview/mux/{NN}_{scene_name}_mux.mp4`
- 사용자가 만족한 뒤 저장하는 고화질 scene 영상: `build/final/{NN}_{scene_name}_hq.mp4`

## 6. 길이 불일치 수정 전략

영상과 오디오 길이가 다를 때:

### 영상이 짧은 경우
1. `WAIT_TAIL` 상수 증가
2. Beat 사이 `self.wait()` 추가/증가
3. 애니메이션 `run_time` 증가

### 영상이 긴 경우
1. `WAIT_TAIL` 상수 감소
2. 불필요한 `self.wait()` 제거
3. 애니메이션 `run_time` 감소

### 허용 오차
- ±0.5~1초는 허용
- 그 이상이면 코드 타이밍 조정

## 7. 디버깅 체크리스트

합성 후 확인 사항:
- [ ] 말이 끝나기 전에 화면이 넘어가는지
- [ ] 화면이 멈췄는데 말이 계속되는지
- [ ] 핵심 Transform이 말의 포인트와 어긋나는지
- [ ] 늘어진 느낌의 정적 구간이 있는지

## 8. 흔한 오류

| 오류 | 원인 | 해결 |
|-----|------|-----|
| `Discarding packets` | 영상/오디오 시작점 불일치 | `-shortest` 옵션 사용 |
| `Non-monotonous DTS` | 타임스탬프 이상 | 재인코딩 |
| 합본 후 오디오 끊김 | 코덱/샘플레이트 불일치 | 재인코딩 합치기 사용 |
| 해상도 불일치 | Scene별 렌더 설정 다름 | filter_complex로 통일 |
