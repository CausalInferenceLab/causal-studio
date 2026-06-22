# FFmpeg Recipes

## 길이 확인

```bash
# 단일 파일
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {FILE}

# video + audio 비교
echo "Video:" && ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {VIDEO}
echo "Audio:" && ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {AUDIO}
```

허용 오차: ±0.5~1초. 초과 시 mux 옵션이 아니라 Scene 코드 타이밍 조정.

## 최신 렌더 파일 찾기

```bash
find build/manim/videos/ -name "*.mp4" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-
```

## Mux (video + audio 합성)

```bash
# Manim scene mux — 비디오 길이 기준 (기본값 --full)
../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh {VIDEO} {AUDIO} {OUTPUT}
```

Manim scene은 `WAIT_TAIL + fade-out tail` 구조상 video가 항상 audio보다 길다.
`-shortest`를 쓰면 오디오 종료 시점에서 화면이 잘려 fade-out이 사라지므로 절대 사용하지 않는다.
오디오가 영상보다 긴 경우는 mux 옵션으로 해결하지 않고 Scene 코드 타이밍을 먼저 조정한다.

mux는 타이밍 보정 단계가 아님. 화면이 오디오보다 먼저 끝나면 Scene 코드로 돌아가 수정.

## 길이 불일치 수정

**영상이 짧은 경우** (우선순위 순):
1. `WAIT_TAIL` 상수 증가
2. Beat 사이 `self.wait()` 추가
3. 애니메이션 `run_time` 증가
4. `.timings.json` chunk 기준 Beat 재분할

**영상이 긴 경우**: `WAIT_TAIL` 감소 → `self.wait()` 제거 → `run_time` 감소

## 전체 합본

```bash
# Step 1: 파일 리스트 생성
ls build/final/*_hq.mp4 2>/dev/null | sort | while read f; do echo "file '$f'"; done > /tmp/filelist.txt

# Step 2-A: 무손실 (동일 코덱·해상도)
ffmpeg -f concat -safe 0 -i /tmp/filelist.txt -c copy build/final/{TOPIC}_full.mp4

# Step 2-B: 재인코딩 (해상도·프레임레이트 다를 때)
ffmpeg -f concat -safe 0 -i /tmp/filelist.txt \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30" \
  -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k \
  build/final/{TOPIC}_full.mp4

# Step 2-C: filter_complex (가장 안정적)
ffmpeg -f concat -safe 0 -i /tmp/filelist.txt \
  -filter_complex "[0:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k \
  build/final/{TOPIC}_full.mp4
```

## 전체 합본 + BGM

```bash
# narration이 이미 포함된 최종 합본에 bgm을 낮은 볼륨으로 섞기
../../.claude/skills/manim-video-pipeline/scripts/mix_bgm.sh \
  build/final/{TOPIC}_full.mp4 \
  path/to/bgm.mp3 \
  build/final/{TOPIC}_full_bgm.mp4 \
  --bgm-volume 0.12
```

기본값:
- `--bgm-volume 0.12`: 내레이션을 해치지 않는 낮은 배경음
- `--voice-gain 1.0`: 원본 보이스오버 유지

원칙:
- BGM은 내레이션보다 항상 훨씬 작아야 한다.
- 말이 많은 교육 영상은 보통 `0.08 ~ 0.15` 범위에서 시작한다.
- BGM 파일이 짧으면 loop해서 영상 길이에 맞춘다.

## 합본 검증

```bash
# 합본 길이
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 build/final/{TOPIC}_full.mp4

# 개별 영상 길이 합계
for f in build/final/*_hq.mp4; do
  ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f"
done | awk '{sum+=$1} END {print sum}'
```

## mux 후 QA 체크리스트

- [ ] 말이 끝나기 전에 화면이 넘어가는가?
- [ ] 화면이 멈췄는데 말이 계속되는가?
- [ ] 핵심 Transform이 말의 포인트와 어긋나는가?
- [ ] 늘어진 정적 구간이 있는가?

## 흔한 오류

| 오류 | 원인 | 해결 |
|-----|------|-----|
| `Discarding packets` | 시작점 불일치 | `-shortest` 사용 |
| `Non-monotonous DTS` | 타임스탬프 이상 | 재인코딩 |
| 합본 후 오디오 끊김 | 코덱/샘플레이트 불일치 | 재인코딩 합치기 |
| 해상도 불일치 | Scene별 렌더 설정 다름 | filter_complex로 통일 |
