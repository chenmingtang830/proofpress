#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { runPrepare, runResume } from "../bench/real/run.mjs";
import { loadEnvFile } from "../bench/real/env.mjs";

const args = parse(process.argv.slice(2));
const manifest = JSON.parse(await fs.readFile(path.resolve(args.manifest ?? "bench/experiments/proofpress-pareto-v1.json")));
const common = { output: path.resolve(args.output), manifest, authorizeRealCalls: args.authorizeRealCalls,
  root: path.resolve(import.meta.dirname, "../../../.."), env: await loadEnvFile(args.envFile && path.resolve(args.envFile)) };
try {
  const result = args.phase === "prepare"
    ? await runPrepare({ ...common, packetDir: path.resolve(args.packet), trackId: args.track,
        sharedSenderFrom: args.sharedSenderFrom && path.resolve(args.sharedSenderFrom) })
    : await runResume(common);
  process.stdout.write(`${JSON.stringify({ status: result.status, output: common.output, track: result.track_id }, null, 2)}\n`);
} catch (error) {
  await fs.mkdir(common.output, { recursive: true });
  const marker = path.join(common.output, `INVALID_ATTEMPT_${args.phase}_${Date.now()}.json`);
  await fs.writeFile(marker, `${JSON.stringify({ schema_version: 1, classification: "INVALID_PAIRED_RUN",
    phase: args.phase, output: common.output, track: args.track ?? null,
    error: { name: error.name, message: error.message, stack: error.stack },
    recorded_at: new Date().toISOString() }, null, 2)}\n`, { flag: "wx" });
  throw error;
}

function parse(argv) { const out = { authorizeRealCalls: false }; for (let i = 0; i < argv.length; i += 1) {
  const key = argv[i];
  if (key === "--phase") out.phase = argv[++i]; else if (key === "--packet") out.packet = argv[++i];
  else if (key === "--output") out.output = argv[++i]; else if (key === "--track") out.track = argv[++i];
  else if (key === "--manifest") out.manifest = argv[++i]; else if (key === "--authorize-real-calls") out.authorizeRealCalls = true;
  else if (key === "--env-file") out.envFile = argv[++i];
  else if (key === "--shared-sender-from") out.sharedSenderFrom = argv[++i];
  else throw new Error(`unknown argument: ${key}`);
  } if (!["prepare", "resume"].includes(out.phase) || !out.output) throw new Error("--phase prepare|resume and --output are required");
  if (out.phase === "prepare" && (!out.packet || !out.track)) throw new Error("prepare requires --packet and --track"); return out; }
