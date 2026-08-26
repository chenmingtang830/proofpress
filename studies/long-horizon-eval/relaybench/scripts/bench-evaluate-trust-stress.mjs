#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { createVercelGatewayAdapter } from "../bench/adapters/vercel-ai-gateway.mjs";
import { loadEnvFile } from "../bench/real/env.mjs";
import { assertResponseEligible } from "../bench/real/response-eligibility.mjs";
import { blindMemos, parseTrustStress, trustStressPrompt } from "../bench/evaluation/trust-stress.mjs";

const execFileAsync = promisify(execFile);
const args = parse(process.argv.slice(2));
if (!args.output || !args.manifest || !args.authorizeRealCalls)
  throw new Error("--output, --manifest, and --authorize-real-calls are required");
const output = path.resolve(args.output);
const manifest = JSON.parse(await fs.readFile(path.resolve(args.manifest)));
if (manifest.real_calls_authorized !== false) throw new Error("manifest safety invariant changed");
const state = JSON.parse(await fs.readFile(path.join(output, "RUN_STATE.json")));
if (state.status !== "READY_FOR_LAB_EVALUATION" && state.status !== "EVALUATED")
  throw new Error(`run is not ready for trust evaluation: ${state.status}`);
const packet = JSON.parse(await fs.readFile(path.join(state.packet_dir, "RUN_PACKET.json")));
if (packet.study_arm !== "LAB_DERIVED_CONTROLLED_HANDOFF_STRESS" || !packet.stress)
  throw new Error("trust-stress evaluator requires a frozen stress packet");
const memos = Object.fromEntries(await Promise.all(packet.conditions.map(async (condition) => [condition,
  await fs.readFile(path.join(output, "receiver", condition, "escalation-approval-memo.md"), "utf8")])));
const blinded = blindMemos(memos);
const evidencePaths = packet.stress.conflicts_with.map((name) => {
  const stage = packet.stages.find((x) => x.release.includes(name));
  if (!stage) throw new Error(`stress conflict file is not in the frozen task release: ${name}`);
  return path.join(state.packet_dir, "source", stage.stage_id, name);
});
const root = path.resolve(import.meta.dirname, "../../../..");
const { stdout } = await execFileAsync("python3", [path.join(root,
  "studies/long-horizon-eval/relaybench/bench/real/extract-evidence.py"),
  JSON.stringify({ paths: evidencePaths, max_chars_per_file: 12000 })], { maxBuffer: 16 * 1024 * 1024 });
const currentEvidence = JSON.parse(stdout);
const adapter = createVercelGatewayAdapter({ ...manifest.evaluator,
  resolved_model: manifest.evaluator.model, api_key_env: manifest.evaluator.api_key_env,
  response_format: { type: "json_object" } });
const env = await loadEnvFile(args.envFile && path.resolve(args.envFile));
const response = await adapter.invoke({ prompt: trustStressPrompt({ fixture: packet.stress,
  currentEvidence, blinded }), max_output_tokens: 6000, reasoning_effort: "none" }, { workspace: output, env });
const attempt = args.attempt ?? "1";
await fs.writeFile(path.join(output, `TRUST_EVALUATOR_RESPONSE_attempt-${attempt}.json`),
  `${JSON.stringify(response, null, 2)}\n`, { flag: "wx" });
assertResponseEligible(response, { label: "trust endpoint evaluator", outputCap: 6000,
  requestedModel: manifest.evaluator.model, requestedProvider: manifest.evaluator.provider_only });
const scores = { schema_version: 1, classification: "LAB-derived controlled handoff stress test",
  official_harvey_result: false, fixture_id: packet.stress.id, task_id: packet.harvey.task_id,
  evaluator: { model: response.telemetry.model, requested_model: response.telemetry.model_requested,
    provider: response.telemetry.serving_provider_requested, telemetry: response.telemetry },
  blinded_order: blinded.map(({ blind_id, digest }) => ({ blind_id, digest })),
  results: parseTrustStress(response.raw_output, blinded) };
await fs.writeFile(path.join(output, `TRUST_ENDPOINT_SCORES_attempt-${attempt}.json`),
  `${JSON.stringify(scores, null, 2)}\n`, { flag: "wx" });
process.stdout.write(`${JSON.stringify(scores.results, null, 2)}\n`);

function parse(argv) { const out = { authorizeRealCalls: false }; for (let i = 0; i < argv.length; i += 1) {
  if (argv[i] === "--output") out.output = argv[++i];
  else if (argv[i] === "--manifest") out.manifest = argv[++i];
  else if (argv[i] === "--env-file") out.envFile = argv[++i];
  else if (argv[i] === "--attempt") out.attempt = argv[++i];
  else if (argv[i] === "--authorize-real-calls") out.authorizeRealCalls = true;
  else throw new Error(`unknown argument: ${argv[i]}`);
} return out; }
