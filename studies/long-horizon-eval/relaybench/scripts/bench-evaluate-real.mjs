#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { evaluatePublicRubric } from "../bench/evaluation/public-rubric.mjs";
import { loadEnvFile } from "../bench/real/env.mjs";

const args = parse(process.argv.slice(2));
if (!args.authorize) throw new Error("evaluator model call requires --authorize-real-calls");
const manifest = JSON.parse(await fs.readFile(path.resolve(args.manifest ?? "bench/experiments/proofpress-pareto-v1.json")));
const statePath = path.join(path.resolve(args.output), "RUN_STATE.json"); const state = JSON.parse(await fs.readFile(statePath));
if (state.status !== "READY_FOR_LAB_EVALUATION") throw new Error(`run state is ${state.status}`);
const packet = JSON.parse(await fs.readFile(path.join(state.packet_dir, "RUN_PACKET.json")));
const upstreamTask = path.resolve(args.task);
const env = await loadEnvFile(args.envFile && path.resolve(args.envFile));
const expectedS4Cap = state.adapter?.final_stage_max_output_tokens;
const observedS4Caps = packet.conditions.map((condition) => state.episodes[condition].stages
  .find((stage) => stage.stage_id === "S4")?.telemetry?.output_cap_tokens);
if (!Number.isFinite(expectedS4Cap) || observedS4Caps.some((cap) => cap !== expectedS4Cap))
  throw new Error(`paired run has missing or mismatched S4 caps: expected ${expectedS4Cap}; observed ${observedS4Caps.join(",")}`);
const scores = {};
for (const condition of packet.conditions) scores[condition] = await evaluatePublicRubric({
  taskPath: upstreamTask, deliverable: state.episodes[condition].deliverable,
  evaluator: manifest.evaluator, env,
  rawResponsePath: path.join(path.resolve(args.output), `EVALUATOR_RESPONSE_${condition}_attempt-${args.attempt}.json`),
});
await fs.writeFile(path.join(path.resolve(args.output), "PUBLIC_RUBRIC_SCORES.json"), `${JSON.stringify(scores, null, 2)}\n`, { flag: "wx" });
process.stdout.write(`${JSON.stringify(Object.fromEntries(Object.entries(scores).map(([k,v]) => [k, { criteria_passed: v.criteria_passed, criteria_total: v.criteria_total, all_pass: v.all_pass }])), null, 2)}\n`);

function parse(argv) { const out = { attempt: 1 }; for (let i = 0; i < argv.length; i += 1) {
  if (argv[i] === "--output") out.output = argv[++i]; else if (argv[i] === "--task") out.task = argv[++i];
  else if (argv[i] === "--manifest") out.manifest = argv[++i]; else if (argv[i] === "--authorize-real-calls") out.authorize = true;
  else if (argv[i] === "--env-file") out.envFile = argv[++i];
  else if (argv[i] === "--attempt") out.attempt = Number(argv[++i]);
  else throw new Error(`unknown argument: ${argv[i]}`);
  } if (!out.output || !out.task) throw new Error("--output and --task are required");
  if (!Number.isInteger(out.attempt) || out.attempt < 1) throw new Error("--attempt must be a positive integer"); return out; }
