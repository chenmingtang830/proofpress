#!/usr/bin/env node
import path from "node:path";
import { prepareRealPacket } from "../bench/real/prepare.mjs";

const args = parse(process.argv.slice(2));
if (!args.harveyCheckout || !args.output) throw new Error("--harvey-checkout and --output are required");
const result = await prepareRealPacket({
  manifestPath: path.resolve(args.manifest ?? "bench/experiments/proofpress-pareto-v1.json"),
  harveyCheckout: path.resolve(args.harveyCheckout), output: path.resolve(args.output),
});
process.stdout.write(`${JSON.stringify({ prepared: true, payable_calls_made: 0, output: result.output,
  task: result.packet.harvey.task_id, criteria: result.packet.harvey.official_public_criteria }, null, 2)}\n`);

function parse(argv) { const out = {}; for (let i = 0; i < argv.length; i += 1) {
  if (argv[i] === "--manifest") out.manifest = argv[++i];
  else if (argv[i] === "--harvey-checkout") out.harveyCheckout = argv[++i];
  else if (argv[i] === "--output") out.output = argv[++i];
  else throw new Error(`unknown argument: ${argv[i]}`);
} return out; }
