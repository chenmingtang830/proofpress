#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";

const args = parse(process.argv.slice(2));
const tasks = {
  credit: "tasks/contracts/financing/credit-lending-playbook-escalation/scenario-02/task.json",
  msa: "tasks/contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation/scenario-04/task.json",
  license: "tasks/contracts/ip-licensing/license-agreement-playbook-escalation/scenario-03/task.json",
};
const taskNames = args.tasks.split(",").map((x) => x.trim());
const armNames = args.arms.split(",").map((x) => x.trim());
const repeatNumbers = args.repeats.split(",").map(Number);
for (const task of taskNames) if (!tasks[task]) throw new Error(`unknown task ${task}`);
for (const arm of armNames) if (!["clean", "stress"].includes(arm)) throw new Error(`unknown arm ${arm}`);
for (const repeat of repeatNumbers) if (![1, 2, 3].includes(repeat)) throw new Error(`unknown repeat ${repeat}`);

for (const task of taskNames) {
  const sender = await resolveSender(args.senderRoot ?? args.root, task);
  for (const repeat of repeatNumbers) for (const arm of armNames) {
    const output = path.join(args.root, `repeat-${repeat}`, arm, task, "run");
    const publicScores = path.join(output, "PUBLIC_RUBRIC_SCORES.json");
    const trustScores = path.join(output, "TRUST_ENDPOINT_SCORES_attempt-1.json");
    if (await exists(publicScores) && (arm === "clean" || await exists(trustScores))) {
      process.stdout.write(`SKIP complete ${args.track} ${task} ${arm} repeat-${repeat}\n`);
      continue;
    }
    const packet = path.join(arm === "clean" ? args.cleanPackets : args.stressPackets, task, "packet");
    let completed = false;
    for (let attempt = 1; attempt <= args.maxAttempts && !completed; attempt += 1) {
      if (await exists(output)) await preserveAttempt(output, attempt);
      process.stdout.write(`START ${args.track} ${task} ${arm} repeat-${repeat} explicit-attempt-${attempt}\n`);
      await fs.mkdir(path.dirname(output), { recursive: true });
      try {
        await run("node", ["scripts/bench-run-real.mjs", "--phase", "prepare", "--packet", packet,
          "--output", output, "--track", args.track, "--shared-sender-from", sender,
          "--env-file", args.envFile, "--authorize-real-calls"]);
        await run("node", ["scripts/bench-run-real.mjs", "--phase", "resume", "--output", output,
          "--env-file", args.envFile, "--authorize-real-calls"]);
        await run("node", ["scripts/bench-evaluate-real.mjs", "--output", output,
          "--task", path.join(args.harveyCheckout, tasks[task]), "--env-file", args.envFile,
          "--authorize-real-calls"]);
        if (arm === "stress") await run("node", ["scripts/bench-evaluate-trust-stress.mjs",
          "--output", output, "--manifest", "bench/experiments/proofpress-pareto-v1.json",
          "--env-file", args.envFile, "--authorize-real-calls"]);
        completed = true;
        process.stdout.write(`DONE ${args.track} ${task} ${arm} repeat-${repeat} explicit-attempt-${attempt}\n`);
      } catch (error) {
        const failure = {
          schema_version: 1,
          classification: "INVALID_OPERATIONAL_ATTEMPT",
          track_id: args.track,
          task,
          arm,
          repeat,
          explicit_attempt: attempt,
          recorded_at: new Date().toISOString(),
          error: String(error?.stack ?? error),
          treatment_estimate_eligible: false,
        };
        await fs.mkdir(output, { recursive: true });
        await fs.writeFile(path.join(output, "INVALID_ATTEMPT.json"), `${JSON.stringify(failure, null, 2)}\n`);
        process.stderr.write(`INVALID ${args.track} ${task} ${arm} repeat-${repeat} explicit-attempt-${attempt}: ${error.message}\n`);
      }
    }
    if (!completed) throw new Error(`exhausted ${args.maxAttempts} explicit attempts: ${args.track} ${task} ${arm} repeat-${repeat}`);
  }
}

async function resolveSender(root, task) {
  const cell = path.join(root, "repeat-1", "clean", task);
  const entries = await fs.readdir(cell, { withFileTypes: true });
  const candidates = entries.filter((entry) => entry.isDirectory() && entry.name.startsWith("run"))
    .map((entry) => path.join(cell, entry.name));
  for (const candidate of candidates.sort((a, b) => a === path.join(cell, "run") ? -1 : b === path.join(cell, "run") ? 1 : a.localeCompare(b))) {
    const stateFile = path.join(candidate, "RUN_STATE.json");
    if (!await exists(stateFile)) continue;
    const state = JSON.parse(await fs.readFile(stateFile, "utf8"));
    const stages = state?.episodes?.C1_ORDINARY_PORTABLE?.stages ?? [];
    if (["POLICY_GATE_COMPLETE", "READY_FOR_LAB_EVALUATION", "COMPLETE"].includes(state.status)
      && ["S1", "S2", "S3"].every((id) => stages.some((stage) => stage.stage_id === id))) return candidate;
  }
  throw new Error(`missing reusable frozen sender for ${task}: ${cell}`);
}

async function preserveAttempt(output, nextAttempt) {
  const parent = path.dirname(output);
  let suffix = Math.max(1, nextAttempt - 1);
  let destination;
  do {
    destination = path.join(parent, `run-invalid-explicit-attempt-${suffix}`);
    suffix += 1;
  } while (await exists(destination));
  await fs.rename(output, destination);
  process.stdout.write(`PRESERVE ${output} -> ${destination}\n`);
}

function run(command, argv) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, argv, { stdio: "inherit" });
    child.once("error", reject);
    child.once("exit", (code, signal) => code === 0 ? resolve()
      : reject(new Error(`${command} ${argv.join(" ")} failed (${signal ?? code})`)));
  });
}
async function exists(file) { try { await fs.access(file); return true; } catch { return false; } }
async function requireFile(file, label) { if (!await exists(file)) throw new Error(`missing ${label}: ${file}`); }
function parse(argv) {
  const out = { arms: "clean,stress", repeats: "1,2,3", maxAttempts: 3 };
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i]; const value = argv[++i];
    if (key === "--track") out.track = value;
    else if (key === "--root") out.root = path.resolve(value);
    else if (key === "--tasks") out.tasks = value;
    else if (key === "--clean-packets") out.cleanPackets = path.resolve(value);
    else if (key === "--stress-packets") out.stressPackets = path.resolve(value);
    else if (key === "--harvey-checkout") out.harveyCheckout = path.resolve(value);
    else if (key === "--env-file") out.envFile = path.resolve(value);
    else if (key === "--sender-root") out.senderRoot = path.resolve(value);
    else if (key === "--max-attempts") out.maxAttempts = Number(value);
    else if (key === "--arms") out.arms = value;
    else if (key === "--repeats") out.repeats = value;
    else throw new Error(`unknown argument ${key}`);
  }
  for (const key of ["track", "root", "tasks", "cleanPackets", "stressPackets", "harveyCheckout", "envFile"])
    if (!out[key]) throw new Error(`missing --${key.replace(/[A-Z]/g, (x) => `-${x.toLowerCase()}`)}`);
  if (!Number.isInteger(out.maxAttempts) || out.maxAttempts < 1) throw new Error("--max-attempts must be a positive integer");
  return out;
}
