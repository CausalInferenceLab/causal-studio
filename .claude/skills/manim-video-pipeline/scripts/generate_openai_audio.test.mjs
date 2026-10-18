import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

const sourceDir = path.dirname(fileURLToPath(import.meta.url));

function fixture(t) {
  // Copy into an isolated repo: never read the developer's .env or use real keys.
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "tts test 한글-"));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const scripts = path.join(root, ".claude/skills/manim-video-pipeline/scripts");
  fs.mkdirSync(scripts, { recursive: true });
  for (const filename of ["generate_openai_audio.mjs", "generate_elevenlabs_audio.mjs"]) {
    fs.copyFileSync(path.join(sourceDir, filename), path.join(scripts, filename));
  }
  const env = Object.fromEntries(Object.entries(process.env).filter(([key]) =>
    !key.startsWith("OPENAI_") && !key.startsWith("ELEVENLABS_") && key !== "NODE_OPTIONS"));
  const baseArgs = ["--topic", "demo", "--scene", "01", "--name", "intro"];
  return {
    root,
    write(relativePath, text) {
      const target = path.join(root, relativePath);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, text);
    },
    run(args = [], extraEnv = {}, { mock, legacy = false } = {}) {
      return spawnSync(process.execPath, [
        ...(mock ? ["--import", path.join(root, mock)] : []),
        path.join(scripts, legacy ? "generate_elevenlabs_audio.mjs" : "generate_openai_audio.mjs"),
        ...baseArgs, ...args,
      ], { cwd: root, env: { ...env, ...extraEnv }, encoding: "utf8", timeout: 20000 });
    },
  };
}

test("dry-run needs no key or .env, resolves --lang, and creates no build directory", (t) => {
  const f = fixture(t);
  f.write("videos/demo/src/scripts/en/01_intro.txt", "# Do not narrate\nA question.\n\nAnother thought.");
  const result = f.run(["--lang", "en", "--dry-run"]);
  assert.equal(result.status, 0, result.stderr);
  const data = JSON.parse(result.stdout);
  assert.deepEqual(data.chunks, ["A question.", "Another thought."]);
  assert.match(data.scriptPath, /scripts\/en\/01_intro.txt$/);
  assert.equal(fs.existsSync(path.join(f.root, "videos/demo/build")), false);
});

test("dotenv voice is loaded before configuration and shell values take priority", (t) => {
  const f = fixture(t);
  f.write(".env", "OPENAI_API_KEY=test-dotenv-key\nOPENAI_TTS_VOICE=nova\n");
  const fromFile = f.run(["--text", "설명", "--dry-run"]);
  assert.equal(fromFile.status, 0, fromFile.stderr);
  assert.equal(JSON.parse(fromFile.stdout).voice, "nova");
  const fromShell = f.run(["--text", "설명", "--dry-run"], { OPENAI_TTS_VOICE: "sage" });
  assert.equal(JSON.parse(fromShell.stdout).voice, "sage");
  assert.doesNotMatch(fromShell.stdout + fromFile.stdout, /test-dotenv-key/);
});

test("language defaults to ko while legacy scripts remain usable", (t) => {
  const f = fixture(t);
  f.write("videos/demo/src/scripts/01_intro.txt", "Legacy script.");
  assert.equal(JSON.parse(f.run(["--dry-run"]).stdout).chunks[0], "Legacy script.");
  f.write("videos/demo/src/scripts/ko/01_intro.txt", "한국어 스크립트.");
  assert.equal(JSON.parse(f.run(["--dry-run"]).stdout).chunks[0], "한국어 스크립트.");
  f.write("custom.txt", "Explicit script.");
  assert.equal(JSON.parse(f.run(["--script", "custom.txt", "--dry-run"]).stdout).chunks[0], "Explicit script.");
  assert.notEqual(f.run(["--lang", "en", "--dry-run"]).status, 0);
});

test("legacy alias still works and explicitly identifies OpenAI", (t) => {
  const f = fixture(t);
  const result = f.run(["--text", "안내", "--dry-run"], {}, { legacy: true });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(JSON.parse(result.stdout).provider, "openai");
  assert.match(result.stderr, /Deprecated name.*OpenAI TTS/);
});

test("missing key and invalid speed fail without an API request", (t) => {
  const f = fixture(t);
  assert.match(f.run(["--text", "안내"]).stderr, /Set OPENAI_API_KEY/);
  for (const speed of ["bad", "1abc", "0.5", "1.3"]) {
    assert.match(f.run(["--text", "안내", "--speed", speed, "--dry-run"]).stderr, /--speed must/);
  }
});

test("shell-only key generates mp3 and cumulative chunk timings using mocked OpenAI", (t) => {
  const f = fixture(t);
  const audio = path.join(f.root, "fixture.mp3");
  const generated = spawnSync("ffmpeg", ["-v", "error", "-f", "lavfi", "-i",
    "anullsrc=r=24000:cl=mono", "-t", "0.4", "-c:a", "libmp3lame", audio]);
  assert.equal(generated.status, 0, generated.stderr?.toString());
  f.write("mock.mjs", `
    import assert from 'node:assert/strict';
    import fs from 'node:fs/promises';
    const requests = [];
    globalThis.fetch = async (url, options) => {
      assert.equal(url, 'https://api.openai.com/v1/audio/speech');
      assert.equal(options.headers.Authorization, 'Bearer test-shell-only-key');
      requests.push(JSON.parse(options.body));
      await fs.writeFile('requests.json', JSON.stringify(requests));
      return new Response(await fs.readFile('fixture.mp3'));
    };
  `);
  const result = f.run(["--text", "첫 설명.\n\n두 번째 설명.", "--speed", "0.9"], {
    OPENAI_API_KEY: "test-shell-only-key", OPENAI_TTS_VOICE: "sage",
    OPENAI_TTS_INSTRUCTIONS: "차분하게 설명",
  }, { mock: "mock.mjs" });
  assert.equal(result.status, 0, result.stderr);
  assert.doesNotMatch(result.stdout + result.stderr, /test-shell-only-key/);
  const requests = JSON.parse(fs.readFileSync(path.join(f.root, "requests.json")));
  assert.equal(requests.length, 2);
  assert.equal(requests[0].model, "gpt-4o-mini-tts");
  assert.equal(requests[0].voice, "sage");
  assert.equal(requests[0].instructions, "차분하게 설명");
  assert.equal(requests[0].speed, 0.9);
  assert.equal(requests[0].response_format, "mp3");
  const outputBase = path.join(f.root, "videos/demo/build/audio/01_intro");
  assert.ok(fs.statSync(`${outputBase}.mp3`).size > 0);
  const timings = JSON.parse(fs.readFileSync(`${outputBase}.timings.json`));
  assert.equal(timings.provider, "openai");
  assert.equal(timings.timingGranularity, "chunk");
  assert.equal(timings.chunkCount, 2);
  assert.equal(timings.chunks[0].start, 0);
  assert.equal(timings.chunks[1].start, timings.chunks[0].end);
  assert.ok(timings.chunks.every((chunk) => chunk.duration > 0 && chunk.end > chunk.start));
  assert.ok(Math.abs(timings.totalDuration - timings.chunks[1].end) < 0.1);
  // dotenv settings must also reach the actual request, with shell key precedence.
  f.write(".env", "OPENAI_API_KEY=test-dotenv-key\nOPENAI_TTS_VOICE=sage\nOPENAI_TTS_INSTRUCTIONS=차분하게 설명\n");
  fs.unlinkSync(path.join(f.root, "requests.json"));
  const fromFile = f.run(["--text", "설명"], { OPENAI_API_KEY: "test-shell-only-key" }, { mock: "mock.mjs" });
  assert.equal(fromFile.status, 0, fromFile.stderr);
  const fileRequest = JSON.parse(fs.readFileSync(path.join(f.root, "requests.json")))[0];
  assert.equal(fileRequest.voice, "sage");
  assert.equal(fileRequest.instructions, "차분하게 설명");
});

test("API error messages redact the API key", (t) => {
  const f = fixture(t);
  f.write("mock-error.mjs", `
    globalThis.fetch = async (url, options) =>
      new Response(options.headers.Authorization, {status: 401});
  `);
  const result = f.run(["--text", "설명"], { OPENAI_API_KEY: "test-secret-value" }, { mock: "mock-error.mjs" });
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /OpenAI TTS failed \(401\)/);
  assert.match(result.stderr, /REDACTED/);
  assert.doesNotMatch(result.stderr, /test-secret-value/);
});
