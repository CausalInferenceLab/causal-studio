---
name: quiz-authoring
description: Create and maintain interactive MyST `{quiz}` exercises for this Jupyter Book. Use when asked to add a quiz to a topic/notebook, design quiz questions from an ipynb, develop a rough quiz idea into final multiple-choice content, create or update topic-level `quizzes.json` banks, or wire a quiz into a notebook with the local `quiz.mjs` directive.
---

# Quiz Authoring

Use this skill to add topic-specific interactive quizzes to notebooks in `book/`.

## Repository Contract

- Shared quiz runtime: `book/assets/quiz/quiz.html`
- MyST directive plugin: `book/quiz.mjs`
- Topic quiz banks: `book/<topic>/quizzes.json`
- Notebook embed syntax:

~~~md
```{quiz} question-id
:single:
:bank: topic/quizzes.json
:lang: ko
```
~~~

Do not add demo pages or global demo question banks. Keep quiz content with the topic it teaches.

## Workflow

1. Identify the target notebook.
   - If the user names a notebook or topic, locate the matching `.ipynb` under `book/`.
   - If unclear, inspect `book/myst.yml` and ask only if multiple plausible targets remain.

2. Develop the quiz topic.
   - If the user gives a rough idea, sharpen it into one concrete learning objective.
   - If the user only says “add a quiz” or similar, read the notebook headings, nearby explanation cells, and key results; propose 2-4 candidate quiz points, choose the strongest if the user did not ask to decide.
   - Prefer questions that test interpretation, assumptions, decision rules, or common pitfalls, not rote recall.

3. Author one high-signal multiple-choice question unless the user asks for more.
   - Use 3 options by default.
   - Make exactly one answer correct.
   - Make distractors plausible and tied to mistakes a learner could make from the notebook.
   - Write Korean for Korean notebooks and English for English notebooks. Include both `ko` and `en` fields when practical so the bank is reusable.
   - Keep explanations short and corrective: state why the correct option is right and, if useful, why the tempting wrong option is wrong.

4. Store the question in the topic bank.
   - Create `book/<topic>/quizzes.json` if missing.
   - Use this schema:

```json
{
  "sets": {},
  "question-id": {
    "question": {"ko": "...", "en": "..."},
    "options": [
      {"ko": "...", "en": "..."},
      {"ko": "...", "en": "..."},
      {"ko": "...", "en": "..."}
    ],
    "answer": 1,
    "explanation": {"ko": "...", "en": "..."}
  }
}
```

   - `answer` is zero-based.
   - Use stable kebab-case IDs such as `policy-learning-targeting`.
   - Preserve existing questions and sets.

5. Embed the quiz in the notebook.
   - Insert a Markdown cell immediately after the concept/result it tests.
   - Use the topic-relative bank path from the book root, for example:

~~~md
```{quiz} policy-learning-targeting
:single:
:bank: policy_learning/quizzes.json
:lang: ko
```
~~~

6. Validate.
   - Run JSON validation for the quiz bank and notebook:

```bash
python -m json.tool book/<topic>/quizzes.json >/dev/null
python -m json.tool book/<topic>/<notebook>.ipynb >/dev/null
```

   - Run the plugin syntax check when `quiz.mjs` changed:

```bash
node --check book/quiz.mjs
```

   - If the preview server is running, fetch the target page and confirm the rendered iframe payload contains the question ID and does not contain unrelated topic question IDs.

## Placement Heuristics

- Put quizzes after a learner has enough context to answer, not before the concept is introduced.
- Avoid placing a quiz inside a long code/output run unless it directly checks that output.
- Prefer transition points: after “methodology”, after “evaluation interpretation”, or before “next section”.
- One quiz should reinforce one idea. Split multi-idea checks into separate questions.

## Quality Bar

A good quiz question:

- tests a decision the learner must make,
- has one defensible answer,
- catches a likely misconception,
- can be answered from the notebook context,
- does not require running additional code,
- uses terminology already introduced nearby.

Avoid:

- trivia about exact numeric output unless the number is the concept,
- vague “which is best?” wording without a clear criterion,
- all-of-the-above or none-of-the-above,
- duplicate options with cosmetic differences,
- adding global/demo quiz content.
