---
name: ipynb-youtube-embed
description: |
  Jupyter 노트북에 YouTube 영상을 임베드하는 스킬.
  Jupyter Book(GitHub Pages)에서 iframe이 올바르게 렌더링되도록
  출력(outputs)까지 함께 저장한다.

  트리거: "유튜브 임베드", "YouTube 임베드", "영상 노트북에 추가", "embed video"
---

# ipynb-youtube-embed

Jupyter Book으로 배포되는 `.ipynb`에 YouTube iframe을 삽입하는 워크플로우.

## 핵심 원칙

Jupyter Book은 노트북을 **실행하지 않고** 저장된 `outputs`를 그대로 렌더링한다.
따라서 코드 셀을 삽입할 때 `outputs`에 HTML 출력을 **미리 저장**해야 iframe이 표시된다.
`outputs`가 비어 있으면 코드만 보이고 iframe은 렌더링되지 않는다.

## 삽입 방법

### 1. YouTube에서 iframe 코드 복사

YouTube 영상 → 공유 → 퍼가기 → `<iframe ...>` 전체 복사

### 2. 노트북 JSON에 코드 셀 + 출력 삽입

```python
import json

NOTEBOOK = "book/{topic}/{notebook}.ipynb"
IFRAME = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{VIDEO_ID}" ...></iframe>'

with open(NOTEBOOK) as f:
    nb = json.load(f)

cell = {
    "cell_type": "code",
    "execution_count": 1,
    "metadata": {"tags": ["hide-input"]},
    "source": [
        "from IPython.display import HTML\n",
        f"HTML('''{IFRAME}''')"
    ],
    "outputs": [
        {
            "data": {
                "text/html": [IFRAME],
                "text/plain": ["<IPython.core.display.HTML object>"]
            },
            "execution_count": 1,
            "metadata": {},
            "output_type": "execute_result"
        }
    ]
}

# 제목 셀(Cell 0) 바로 아래 삽입
nb['cells'].insert(1, cell)

with open(NOTEBOOK, 'w') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
```

## 태그 선택 기준

| 태그 | 효과 | 사용 시점 |
|------|------|-----------|
| `hide-input` | 코드 접힘, 출력(iframe)만 표시 | 기본값 — 독자에게 Python 코드가 불필요할 때 |
| `remove-input` | 코드 완전 제거, 출력만 표시 | 코드 존재 자체를 숨기고 싶을 때 |
| (없음) | 코드 + 출력 모두 표시 | 코드 노출이 필요할 때 |

## 삽입 위치 기준

- **제목 바로 아래(Cell 1)**: 영상이 해당 노트북 전체를 커버하는 경우 (기본값)
- **특정 섹션 아래**: 영상이 특정 개념만 다루는 경우

## 주의사항

- `outputs`를 빈 배열로 두면 Jupyter Book에서 iframe이 **절대 렌더링되지 않는다**.
- `text/html` 값은 반드시 **리스트 형태** (`["<iframe ...>"]`)여야 한다.
- 언어별 노트북이 분리된 경우(`_ko.ipynb`, `_en.ipynb`), 각각 따로 삽입한다.
