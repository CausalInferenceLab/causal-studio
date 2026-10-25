// Korean draft narration through ElevenLabs. The API key stays in the repo's ignored .env.
import fs from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const topic = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repo = path.resolve(topic, '..', '..');
process.loadEnvFile(path.join(repo, '.env'));
const apiKey = process.env.ELEVENLABS_API_KEY;
if (!apiKey) throw new Error('ELEVENLABS_API_KEY가 필요합니다.');

// ElevenLabs Korean voice: Anna Kim, Tender, Calm and Clear.
const voiceId = process.env.ELEVENLABS_VOICE_ID || 'Xb7hH8MSUJpSbSDYk0k2';
const scripts = (await fs.readdir(path.join(topic, 'src', 'scripts', 'ko')))
  .filter((name) => name.endsWith('.txt')).sort();
const audioDir = path.join(topic, 'build', 'audio');
await fs.mkdir(audioDir, { recursive: true });

for (let i = 0; i < scripts.length; i += 1) {
  const scriptPath = path.join(topic, 'src', 'scripts', 'ko', scripts[i]);
  const target = path.join(audioDir, `${String(i + 1).padStart(2, '0')}.mp3`);
  const scriptStat = await fs.stat(scriptPath);
  const outputStat = await fs.stat(target).catch(() => null);
  if (outputStat && outputStat.mtimeMs >= scriptStat.mtimeMs) {
    console.log(`${scripts[i]} -> ${path.basename(target)} (cached)`);
    continue;
  }
  const text = (await fs.readFile(scriptPath, 'utf8')).trim();
  const response = await fetch(
    `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_128`,
    {
      method: 'POST',
      headers: { 'xi-api-key': apiKey, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        model_id: 'eleven_multilingual_v2',
        voice_settings: { speed: 1.05, stability: 0.55, similarity_boost: 0.75 },
      }),
    },
  );
  if (!response.ok) {
    const error = (await response.text()).slice(0, 400);
    throw new Error(`ElevenLabs ${response.status} (${scripts[i]}): ${error}`);
  }
  await fs.writeFile(target, Buffer.from(await response.arrayBuffer()));
  console.log(`${scripts[i]} -> ${path.basename(target)}`);
}
