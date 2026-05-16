#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import process from "node:process";
import { spawn } from "node:child_process";

import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

const VOICE_ID = "7Nah3cbXKVmGX7gQUuwz";
const MODEL_ID = "eleven_multilingual_v2";
const OUTPUT_FORMAT = "mp3_44100_128";

function printUsage() {
  console.log(`Usage:
  node scripts/generate_elevenlabs_audio.mjs --topic TOPIC --scene 01 --name scene_name [--script PATH]
  node scripts/generate_elevenlabs_audio.mjs --topic TOPIC --scene 01 --name scene_name --text "..."

Options:
  --topic      topic directory under videos/
  --scene      scene number, e.g. 01
  --name       scene snake_case name
  --script     explicit script file path
  --text       direct text input instead of a script file
  --dry-run    validate paths and print output target without API call
  --help       show this message`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) {
      throw new Error(`Unexpected argument: ${token}`);
    }
    const key = token.slice(2);
    if (key === "dry-run" || key === "help") {
      args[key] = true;
      continue;
    }
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${key}`);
    }
    args[key] = value;
    i += 1;
  }
  return args;
}

async function readText(scriptPath, directText) {
  if (directText) {
    return directText.trim();
  }
  const raw = await fs.readFile(scriptPath, "utf8");
  return raw.trim();
}

function splitIntoChunks(text, maxChars = 650) {
  const paragraphs = text
    .split(/\n\s*\n/g)
    .map((part) => part.replace(/\s+/g, " ").trim())
    .filter(Boolean);

  const chunks = [];
  for (const paragraph of paragraphs) {
    if (paragraph.length <= maxChars) {
      chunks.push(paragraph);
      continue;
    }

    const sentences = paragraph
      .split(/(?<=[.!?])\s+/)
      .map((sentence) => sentence.trim())
      .filter(Boolean);

    let current = "";
    for (const sentence of sentences) {
      const next = current ? `${current} ${sentence}` : sentence;
      if (next.length <= maxChars) {
        current = next;
      } else {
        if (current) chunks.push(current);
        current = sentence;
      }
    }
    if (current) chunks.push(current);
  }
  return chunks;
}

async function ensureEnv(repoRoot) {
  const envPath = path.join(repoRoot, ".env");
  process.loadEnvFile(envPath);
  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) {
    throw new Error(`ELEVENLABS_API_KEY not found in ${envPath}`);
  }
  return apiKey;
}

async function streamToBuffer(stream) {
  const reader = stream.getReader();
  const chunks = [];
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(Buffer.from(value));
  }
  return Buffer.concat(chunks);
}

async function runFfmpeg(fileListPath, outputPath) {
  await new Promise((resolve, reject) => {
    const child = spawn(
      "ffmpeg",
      ["-y", "-f", "concat", "-safe", "0", "-i", fileListPath, "-c", "copy", outputPath],
      { stdio: ["ignore", "ignore", "pipe"] },
    );
    let stderr = "";
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("close", (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(stderr || `ffmpeg failed with code ${code}`));
      }
    });
  });
}

async function probeDurationSeconds(filePath) {
  return new Promise((resolve, reject) => {
    const child = spawn(
      "ffprobe",
      [
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        filePath,
      ],
      { stdio: ["ignore", "pipe", "pipe"] },
    );

    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });
    child.on("close", (code) => {
      if (code !== 0) {
        reject(new Error(stderr || `ffprobe failed with code ${code}`));
        return;
      }
      const duration = Number.parseFloat(stdout.trim());
      if (Number.isNaN(duration)) {
        reject(new Error(`Unable to parse duration for ${filePath}`));
        return;
      }
      resolve(duration);
    });
  });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printUsage();
    return;
  }

  const topic = args.topic;
  const scene = args.scene;
  const sceneName = args.name;
  const dryRun = Boolean(args["dry-run"]);

  if (!topic || !scene || !sceneName) {
    printUsage();
    throw new Error("--topic, --scene, and --name are required");
  }

  const repoRoot = path.resolve(path.dirname(new URL(import.meta.url).pathname), "../../../..");
  const topicDir = path.join(repoRoot, "videos", topic);
  const scriptPath =
    args.script || path.join(topicDir, "src", "scripts", `${scene}_${sceneName}.txt`);
  const outputPath = path.join(topicDir, "build", "audio", `${scene}_${sceneName}.mp3`);
  const timingsPath = path.join(topicDir, "build", "audio", `${scene}_${sceneName}.timings.json`);

  const text = await readText(scriptPath, args.text);
  if (!text) {
    throw new Error("Input text is empty");
  }
  const chunks = splitIntoChunks(text);
  if (chunks.length === 0) {
    throw new Error("No valid text chunks found");
  }

  await fs.mkdir(path.dirname(outputPath), { recursive: true });

  if (dryRun) {
    console.log(JSON.stringify({
      topic,
      scene,
      sceneName,
      scriptPath,
      outputPath,
      timingsPath,
      voiceId: VOICE_ID,
      modelId: MODEL_ID,
      outputFormat: OUTPUT_FORMAT,
      charCount: text.length,
      chunkCount: chunks.length,
      chunks,
    }, null, 2));
    return;
  }

  const apiKey = await ensureEnv(repoRoot);
  const client = new ElevenLabsClient({ apiKey });
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), "elevenlabs-scene-"));
  const chunkPaths = [];

  for (let i = 0; i < chunks.length; i += 1) {
    const audioStream = await client.textToSpeech.convert(VOICE_ID, {
      text: chunks[i],
      modelId: MODEL_ID,
      outputFormat: OUTPUT_FORMAT,
    });
    const buffer = await streamToBuffer(audioStream);
    const chunkPath = path.join(tempDir, `${String(i + 1).padStart(2, "0")}.mp3`);
    await fs.writeFile(chunkPath, buffer);
    chunkPaths.push(chunkPath);
  }

  if (chunkPaths.length === 1) {
    await fs.copyFile(chunkPaths[0], outputPath);
  } else {
    const fileListPath = path.join(tempDir, "concat.txt");
    const fileList = chunkPaths.map((chunkPath) => `file '${chunkPath}'`).join("\n");
    await fs.writeFile(fileListPath, fileList);
    await runFfmpeg(fileListPath, outputPath);
  }

  const timingChunks = [];
  let cursor = 0;
  for (let i = 0; i < chunkPaths.length; i += 1) {
    const duration = await probeDurationSeconds(chunkPaths[i]);
    const start = cursor;
    const end = start + duration;
    timingChunks.push({
      index: i + 1,
      text: chunks[i],
      duration,
      start,
      end,
    });
    cursor = end;
  }

  const mergedDuration = await probeDurationSeconds(outputPath);
  await fs.writeFile(
    timingsPath,
    JSON.stringify(
      {
        topic,
        scene,
        sceneName,
        scriptPath,
        outputPath,
        voiceId: VOICE_ID,
        modelId: MODEL_ID,
        outputFormat: OUTPUT_FORMAT,
        totalDuration: mergedDuration,
        chunkCount: timingChunks.length,
        chunks: timingChunks,
      },
      null,
      2,
    ),
  );

  console.log(outputPath);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
