---
name: notebook-references
description: >
  Jupyter 노트북의 마지막 셀에 참고 자료를 추가하거나 수정할 때 사용.
  "참고 자료 추가해줘", "references 넣어줘", "참고문헌 업데이트" 등을 요청할 때 트리거.
  한국어 노트북과 영어 노트북 모두 동일한 인용 형식 컨벤션을 적용.
---

# notebook-references

Causal Studio 노트북의 참고 자료 셀 작성 컨벤션.

## 형식

마지막 셀을 찾아 아래 형식으로 작성한다. NotebookEdit으로 셀을 수정하거나, 없으면 새 셀을 추가한다.

### 영어 노트북 (`_en.ipynb`)

```markdown
## References

This notebook draws on <주요 참고 자료 1–2개>.

- **Author, A., & Author, B. (Year)**. Title of paper or book. *Journal or Publisher*.
  [URL](URL)

- **Author, C. (Year)**. *Book Title*. Online book.
  [URL](URL)

- **Dataset Name — Description**.
  [URL](URL)
```

### 한국어 노트북 (`_ko.ipynb`)

```markdown
## 참고 자료

이 노트북은 <주요 참고 자료 1–2개>를 주요 참고 자료로 작성되었습니다.

- **Author, A., & Author, B. (Year)**. Title of paper or book. *Journal or Publisher*.
  [URL](URL)

- **Author, C. (Year)**. *Book Title*. Online book.
  [URL](URL)

- **데이터셋 이름 — 설명**.
  [URL](URL)
```

## 규칙

- 저자·연도·제목은 **굵게** (볼드)
- 저널명·책 제목은 *이탤릭*
- URL은 별도 줄에 두 칸 들여쓰기 후 `[URL](URL)` 형식
- 논문: `Author (Year). Title. *Journal*.`
- 책: `Author (Year). *Title*. Online book.` 또는 Publisher
- 데이터셋: `**이름 — 설명**.` (저자/연도 없이)
- 한국어 노트북에서도 저자명·제목은 영어 그대로 유지

## 기존 노트북 예시

FDC 노트북 (`frontdoor_criterion_ko.ipynb`) 참고:
```markdown
## 참고 자료

이 노트북은 Matheus Facure의 *Causal Inference for the Brave and True*와 Bellemare & Bloem (2024)을 주요 참고 자료로 작성되었습니다.

- **Bellemare, M. F., & Bloem, J. R. (2024)**. The Paper of How: Estimating Treatment Effects Using the Front-Door Criterion. *Oxford Bulletin of Economics and Statistics*.
  [https://...](https://...)

- **Facure, M. (2022)**. *Causal Inference for the Brave and True*. Online book.
  [https://matheusfacure.github.io/python-causality-handbook/](https://matheusfacure.github.io/python-causality-handbook/)

- **NYC TLC — 2023 High Volume For-Hire Vehicle Trip Records**.
  [https://...](https://...)
```
