// One-off: regenerate English narration with slower speed + inter-chunk pauses.
// Outputs build/audio/{NN}_{name}.mp3 + .timings.json (same names as before).
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import dotenv from "dotenv";
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

const VOICE_ID = "7Nah3cbXKVmGX7gQUuwz";
const MODEL_ID = "eleven_multilingual_v2";
const OUTPUT_FORMAT = "mp3_44100_128";
const SPEED = 0.9;
const GAP = 0.25; // seconds of silence between chunks

const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../../../..");
const topicDir = path.join(repoRoot, "videos", "what_is_ipw");
dotenv.config({ path: path.join(repoRoot, ".env") });
const client = new ElevenLabsClient({ apiKey: process.env.ELEVENLABS_API_KEY });

const SCENES = [
  ["02", "ipw_application_en"],
  ["03", "ipw_formula_en"],
  ["04", "propensity_score_en"],
  ["05", "summary_en"],
];

function splitIntoChunks(text, maxChars = 650) {
  const paras = text.split(/\n\s*\n/g).map((p) => p.replace(/\s+/g, " ").trim()).filter(Boolean);
  const chunks = [];
  for (const p of paras) {
    if (p.length <= maxChars) { chunks.push(p); continue; }
    let cur = "";
    for (const s of p.split(/(?<=[.!?])\s+/).map((x) => x.trim()).filter(Boolean)) {
      if ((cur + " " + s).trim().length > maxChars) { if (cur) chunks.push(cur); cur = s; }
      else cur = (cur + " " + s).trim();
    }
    if (cur) chunks.push(cur);
  }
  return chunks;
}

async function streamToBuffer(stream) {
  const reader = stream.getReader();
  const out = [];
  while (true) { const { done, value } = await reader.read(); if (done) break; out.push(Buffer.from(value)); }
  return Buffer.concat(out);
}

function ff(args) {
  return new Promise((res, rej) => {
    const p = spawn("ffmpeg", args, { stdio: "ignore" });
    p.on("close", (c) => (c === 0 ? res() : rej(new Error("ffmpeg " + c))));
  });
}
function probe(file) {
  return new Promise((res, rej) => {
    const p = spawn("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file]);
    let o = ""; p.stdout.on("data", (d) => (o += d)); p.on("close", (c) => (c === 0 ? res(parseFloat(o)) : rej(new Error("ffprobe"))));
  });
}

for (const [scene, name] of SCENES) {
  const scriptPath = path.join(topicDir, "src", "scripts", `${scene}_${name}.txt`);
  const outMp3 = path.join(topicDir, "build", "audio", `${scene}_${name}.mp3`);
  const outTim = path.join(topicDir, "build", "audio", `${scene}_${name}.timings.json`);
  const text = (await fs.readFile(scriptPath, "utf8")).trim();
  const chunks = splitIntoChunks(text);
  const tmp = await fs.mkdtemp(path.join(os.tmpdir(), "en-slow-"));

  const silence = path.join(tmp, "sil.mp3");
  await ff(["-y", "-f", "lavfi", "-i", `anullsrc=channel_layout=mono:sample_rate=44100`, "-t", String(GAP), "-c:a", "libmp3lame", "-b:a", "128k", silence]);

  const chunkPaths = [];
  for (let i = 0; i < chunks.length; i++) {
    const stream = await client.textToSpeech.convert(VOICE_ID, {
      text: chunks[i], modelId: MODEL_ID, outputFormat: OUTPUT_FORMAT,
      voiceSettings: { speed: SPEED },
    });
    const buf = await streamToBuffer(stream);
    const cp = path.join(tmp, `c${String(i).padStart(2, "0")}.mp3`);
    await fs.writeFile(cp, buf);
    chunkPaths.push(cp);
  }

  // interleave silence between chunks
  const listItems = [];
  for (let i = 0; i < chunkPaths.length; i++) {
    listItems.push(`file '${chunkPaths[i]}'`);
    if (i < chunkPaths.length - 1) listItems.push(`file '${silence}'`);
  }
  const listPath = path.join(tmp, "list.txt");
  await fs.writeFile(listPath, listItems.join("\n"));
  await ff(["-y", "-f", "concat", "-safe", "0", "-i", listPath, "-c:a", "libmp3lame", "-b:a", "128k", outMp3]);

  // timings: chunk i speech start = sum(prev durations) + i*GAP
  const durs = [];
  for (const cp of chunkPaths) durs.push(await probe(cp));
  let acc = 0; const tchunks = [];
  for (let i = 0; i < durs.length; i++) {
    const start = acc + i * GAP;
    tchunks.push({ index: i + 1, text: chunks[i], duration: durs[i], start, end: start + durs[i] });
    acc += durs[i];
  }
  const total = await probe(outMp3);
  await fs.writeFile(outTim, JSON.stringify({ topic: "what_is_ipw", scene, sceneName: name, speed: SPEED, gap: GAP, totalDuration: total, chunkCount: chunks.length, chunks: tchunks }, null, 2));
  console.log(`${scene}_${name}: ${chunks.length} chunks, total ${total.toFixed(2)}s`);
}
