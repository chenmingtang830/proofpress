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
  const sender = path.join(args.root, "repeat-1", "clean", task, "run");
  await requireFile(path.join(sender, "RUN_STATE.json"), `frozen sender run for ${task}`);
  for (const repeat of repeatNumbers) for (const arm of armNames) {
    const output = path.join(args.root, `repeat-${repeat}`, arm, task, "run");
    const publicScores = path.join(output, "PUBLIC_RUBRIC_SCORES.json");
    const trustScores = path.join(output, "TRUST_ENDPOINT_SCORES_attempt-1.json");
    if (await exists(publicScores) && (arm === "clean" || await exists(trustScores))) {
      process.stdout.write(`SKIP complete ${args.track} ${task} ${arm} repeat-${repeat}\n`);
      continue;
    }
    if (await exists(output)) throw new Error(`incomplete or invalid attempt requires audit before continuing: ${output}`);
    const packet = path.join(arm === "clean" ? args.cleanPackets : args.stressPackets, task, "packet");
    process.stdout.write(`START ${args.track} ${task} ${arm} repeat-${repeat}\n`);
    await fs.mkdir(path.dirname(output), { recursive: true });
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
    process.stdout.write(`DONE ${args.track} ${task} ${arm} repeat-${repeat}\n`);
  }
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
  const out = { arms: "clean,stress", repeats: "1,2,3" };
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i]; const value = argv[++i];
    if (key === "--track") out.track = value;
    else if (key === "--root") out.root = path.resolve(value);
    else if (key === "--tasks") out.tasks = value;
    else if (key === "--clean-packets") out.cleanPackets = path.resolve(value);
    else if (key === "--stress-packets") out.stressPackets = path.resolve(value);
    else if (key === "--harvey-checkout") out.harveyCheckout = path.resolve(value);
    else if (key === "--env-file") out.envFile = path.resolve(value);
    else if (key === "--arms") out.arms = value;
    else if (key === "--repeats") out.repeats = value;
    else throw new Error(`unknown argument ${key}`);
  }
  for (const key of ["track", "root", "tasks", "cleanPackets", "stressPackets", "harveyCheckout", "envFile"])
    if (!out[key]) throw new Error(`missing --${key.replace(/[A-Z]/g, (x) => `-${x.toLowerCase()}`)}`);
  return out;
}
