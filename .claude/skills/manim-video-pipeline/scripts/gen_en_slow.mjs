#!/usr/bin/env node

// Legacy IPW batch example. Individual scenes can use the generic audio command.
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const audio = fileURLToPath(new URL("./generate_elevenlabs_audio.mjs", import.meta.url));
for (const [scene, name] of [
  ["02", "ipw_application_en"],
  ["03", "ipw_formula_en"],
  ["04", "propensity_score_en"],
  ["05", "summary_en"],
]) {
  const result = spawnSync(process.execPath, [
    audio, "--provider", "elevenlabs", "--topic", "what_is_ipw", "--scene", scene,
    "--name", name, "--lang", "en", "--speed", "0.9", "--gap", "0.25",
    "--script", fileURLToPath(new URL(`../../../../videos/what_is_ipw/src/scripts/en/${scene}_${name.replace(/_en$/, "")}.txt`, import.meta.url)),
    "--output", fileURLToPath(new URL(`../../../../videos/what_is_ipw/build/audio/${scene}_${name}.mp3`, import.meta.url)),
    ...process.argv.slice(2),
  ], { stdio: "inherit" });
  if (result.error) console.error(result.error.message);
  if (result.status !== 0) process.exit(result.status ?? 1);
}
