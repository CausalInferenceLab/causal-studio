// MyST plugin: `{quiz}` directive.
//
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

// Renders book/assets/quiz/quiz.html inside an iframe. The directive embeds
// the question bank into a data URL so it works in local MyST dev and static
// builds without depending on server-specific static asset routing.
//
// Why an iframe: the MyST/jupyter-book static renderer strips <script>, inline
// event handlers, <style>, and <form>/<input> elements during sanitization, so
// interactive JS cannot run on the page itself. An iframe loads a separate
// document whose JS runs freely.
//
// Height: the book theme wraps every iframe in a fixed 60%-aspect-ratio box.
// We wrap ours in `<div class="quiz-embed" style="height:NNNpx">` and override
// that box in custom.css so the iframe gets a real pixel height instead.
//
const quizHtml = readFileSync(new URL('./assets/quiz/quiz.html', import.meta.url), 'utf8');
const bookDir = fileURLToPath(new URL('.', import.meta.url));

function escapeAttribute(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('"', '&quot;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function scriptSafeJson(value) {
  return JSON.stringify(value)
    .replaceAll('<', '\\u003c')
    .replaceAll('>', '\\u003e')
    .replaceAll('&', '\\u0026')
    .replaceAll('\u2028', '\\u2028')
    .replaceAll('\u2029', '\\u2029');
}

function loadQuizData(bank) {
  if (!bank) {
    throw new Error('Quiz directive requires a :bank: option, for example :bank: policy_learning/quizzes.json');
  }
  const bankPath = path.resolve(bookDir, bank);
  const rel = path.relative(bookDir, bankPath);
  if (rel.startsWith('..') || path.isAbsolute(rel)) {
    throw new Error(`Quiz bank must stay inside the book directory: ${bank}`);
  }
  return JSON.parse(readFileSync(bankPath, 'utf8'));
}

function buildQuizSrcdoc(arg, opts) {
  const embed = {
    lang: opts.lang || undefined,
    oneId: opts.single ? arg : undefined,
    setId: opts.single ? undefined : arg,
    data: loadQuizData(opts.bank),
  };
  const bootstrap = `<script>window.__QUIZ_EMBED__=${scriptSafeJson(embed)};</script>`;
  return quizHtml.replace('</head>', `${bootstrap}\n</head>`);
}

const quizDirective = {
  name: 'quiz',
  doc: 'Embed an interactive multiple-choice quiz.',
  arg: { type: String, doc: 'Quiz set name (default) or single question id with :single:.' },
  options: {
    height: { type: Number, doc: 'Iframe height in pixels (default 460).' },
    bank: { type: String, doc: 'Quiz bank JSON path relative to the book directory, for example policy_learning/quizzes.json.' },
    lang: { type: String, doc: 'Force language: "ko" or "en". Defaults to the quiz app default.' },
    single: { type: Boolean, doc: 'Treat the argument as a single question id instead of a set.' },
  },
  run(data) {
    const arg = (data.arg || '').trim();
    const opts = data.options || {};
    const height = Number(opts.height) > 0 ? Math.round(Number(opts.height)) : 460;
    const src = `data:text/html;charset=utf-8,${encodeURIComponent(buildQuizSrcdoc(arg, opts))}`;
    const html =
      `<div class="quiz-embed" style="height:${height}px">` +
      `<iframe src="${escapeAttribute(src)}" title="quiz" loading="lazy"></iframe>` +
      `</div>`;
    return [{ type: 'html', value: html }];
  },
};

const plugin = { name: 'Quiz', directives: [quizDirective] };
export default plugin;
