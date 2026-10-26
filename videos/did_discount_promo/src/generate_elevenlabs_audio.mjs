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
const config = {
  voiceId,
  modelId: 'eleven_multilingual_v2',
  voiceSettings: { speed: 0.95, stability: 0.55, similarity_boost: 0.75 },
};
const scripts = (await fs.readdir(path.join(topic, 'src', 'scripts', 'ko')))
  .filter((name) => name.endsWith('.txt')).sort();
const audioDir = path.join(topic, 'build', 'audio');
await fs.mkdir(audioDir, { recursive: true });
const configPath = path.join(audioDir, 'elevenlabs_config.json');
const oldConfig = await fs.readFile(configPath, 'utf8').catch(() => '');
const sameConfig = oldConfig === JSON.stringify(config);

const beats = [];
for (let sceneIndex = 0; sceneIndex < scripts.length; sceneIndex += 1) {
  const scene = sceneIndex + 1;
  const scriptPath = path.join(topic, 'src', 'scripts', 'ko', scripts[sceneIndex]);
  const scriptStat = await fs.stat(scriptPath);
  const lines = (await fs.readFile(scriptPath, 'utf8')).split(/\r?\n/)
    .map((line) => line.trim()).filter(Boolean);
  for (let beatIndex = 0; beatIndex < lines.length; beatIndex += 1) {
    const beat = beatIndex + 1;
    const text = lines[beatIndex];
    const filename = `${String(scene).padStart(2, '0')}_${String(beat).padStart(2, '0')}.mp3`;
    const target = path.join(audioDir, filename);
    const outputStat = await fs.stat(target).catch(() => null);
    if (!(sameConfig && outputStat && outputStat.mtimeMs >= scriptStat.mtimeMs)) {
      const response = await fetch(
        `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_128`,
        {
          method: 'POST',
          headers: { 'xi-api-key': apiKey, 'Content-Type': 'application/json' },
          body: JSON.stringify({ text, model_id: config.modelId, voice_settings: config.voiceSettings }),
        },
      );
      if (!response.ok) {
        const error = (await response.text()).slice(0, 400);
        throw new Error(`ElevenLabs ${response.status} (${filename}): ${error}`);
      }
      await fs.writeFile(target, Buffer.from(await response.arrayBuffer()));
    }
    beats.push({ scene, beat, text, file: filename });
    console.log(`${filename}: ${text.slice(0, 24)}`);
  }
}
await fs.writeFile(configPath, JSON.stringify(config));
await fs.writeFile(path.join(audioDir, 'beat_manifest.json'), JSON.stringify(beats, null, 2));
