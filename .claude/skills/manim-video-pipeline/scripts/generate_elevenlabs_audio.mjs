#!/usr/bin/env node

// Compatibility entry point for old Causal Studio commands. The CLI historically used OpenAI.
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scripts = path.dirname(fileURLToPath(import.meta.url));
const localPython = path.resolve(scripts, "../../../../.venv/bin/python");
const python = process.env.MANIM_PYTHON || (existsSync(localPython) ? localPython : "python3");
const result = spawnSync(python, [path.join(scripts, "pipeline.py"), "audio", ...process.argv.slice(2)], {
  stdio: "inherit",
});
if (result.error) console.error(result.error.message);
process.exitCode = result.status ?? 1;
