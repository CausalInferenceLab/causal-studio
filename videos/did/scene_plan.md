# 차분의 차분 (DiD)

## The idea

- 처음 인과추론을 접하는 시청자. 두 시점의 평균과 그래프는 읽을 수 있다고 가정한다.
- 야간버스를 늘린 구의 하루 평균 탑승객이 100명에서 160명으로 늘었다. 늘어난 60명을 모두 증편 효과로 볼 수 있을까?
- 가상의 예시. 증편 지역은 100 → 160명, 비교 지역은 80 → 100명. 증편이 없었다면 두 지역의 평균 탑승객이 같은 폭으로 변했을 것이라고 가정한다. 그러면 반사실은 120명, 효과 추정치는 40명이다. 다른 변화폭을 가정하면 같은 관측값에서도 추정치는 달라진다.
- 통계 참고 자료는 [Difference-in-Differences Fundamentals](https://mixtape.scunning.com/09-difference_in_differences).

## Reference study

| Video and time range | Source permalink and class or function | What happens before, during, and after the move | How the move explains this topic |
|---|---|---|---|
| [3Blue1Brown, Vectors](https://www.youtube.com/watch?v=fNk_zzaMoSs&t=325s), 5:25–5:45 | [`VectorAddition.define_addition`](https://github.com/3b1b/videos/blob/31f8ffe785e860477a6051fde983c02c7d165bc2/_2016/eola/chapter1.py#L656-L676) | 첫 번째 화살표를 유지하고 두 번째 화살표를 같은 길이와 방향으로 옮겨 새 끝점을 보여준다. | 비교 지역 선의 복사본과 +20 괄호를 같은 높이만큼 위로 옮긴다. 복사본이 닿는 120을 점선으로 남긴다. |
| [3Blue1Brown, Bayes' theorem 공식 강의의 도식](https://www.3blue1brown.com/lessons/bayes-theorem/) | [`CreateFormulaFromDiagram`](https://github.com/3b1b/videos/blob/31f8ffe785e860477a6051fde983c02c7d165bc2/_2019/bayes/part1.py#L2485-L2510) | 도식에서 의미가 드러난 수량을 복제해 식으로 옮긴다. | +60, +20, +40 괄호에서 숫자가 각각 60 − 20 = 40의 자리로 이동한다. |

색은 [3Blue1Brown Manim 팔레트](https://github.com/3b1b/manim/blob/master/manimlib/default_config.yml#L140-L188)에서 검정과 흰색, 비교 지역의 `BLUE_C`, 효과의 `YELLOW_C`를 사용한다.

## Storyboard

| Scene and cue | Starting image | Main move and resulting image | What stays, what leaves, and what to read |
|---|---|---|---|
| 01 · 관측된 변화 | 전후 탑승객 숫자 두 개 | 앞뒤의 정류점을 데이터 점으로 옮기고 두 점을 잇는다. 비교 지역이 들어올 때 이름을 선 옆에 붙인다. | 증편 지역은 흰색, 비교 지역은 파란색으로 유지한다. |
| 02 · 보이지 않는 값 | 두 관측선과 증가량 | 비교 지역의 선과 +20 괄호를 증편 지역의 시작 높이로 옮긴다. 120부터 160까지의 +40을 노란색으로 드러낸다. | 비교 지역의 관측선은 그대로 두고, 추정한 경로만 점선으로 바꾼다. |
| 03 · 가정 | 실제 160과 추정 120 | 각각의 괄호에서 수를 꺼내 식을 완성한다. 관측점을 고정하고 가정한 점선의 끝을 140으로 올려 차이가 20이 되는 경우를 보여준다. | 마지막에는 120으로 돌아와 두 지역의 평행한 선을 함께 보여준다. |

## Key transition preview

- 02에서 파란 변화분을 옮기기 직전부터 점선이 남고 +40을 읽기까지.
- 소리 없이 비교 지역 선이 복제된다는 점, 길이와 기울기가 유지되는 점, 120이 추정값이라는 점, +40이 두 끝점의 거리라는 점을 확인한다.
- 480픽셀 시안에서 +20이 복사되는 동안 화면에 두 개로 보여, 선은 복제하되 +20 괄호 자체를 옮기도록 고쳤다. 이동이 끝나면 오른쪽에서 +20과 +40을 이어 읽을 수 있다.
