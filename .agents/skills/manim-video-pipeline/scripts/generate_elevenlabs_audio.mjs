#!/usr/bin/env node

// Compatibility entry point: this command historically used OpenAI already.
// Actual ElevenLabs experiments live in gen_en_slow.mjs, not this alias.
console.warn("Deprecated name: this command uses OpenAI TTS. Use generate_openai_audio.mjs or npm run openai-audio.");
await import("./generate_openai_audio.mjs");
