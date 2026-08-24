#!/usr/bin/env node
import path from "node:path";
import { preflightRealStudy } from "../bench/real/preflight.mjs";
import { loadEnvFile } from "../bench/real/env.mjs";

const args = parse(process.argv.slice(2));
const manifest = path.resolve(args.manifest ?? "bench/experiments/proofpress-pareto-v1.json");
const env = await loadEnvFile(args.envFile && path.resolve(args.envFile));
const result = await preflightRealStudy({ manifestPath: manifest,
  harveyCheckout: args.harveyCheckout && path.resolve(args.harveyCheckout), trackId: args.track, env });
process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
if (!result.ready) process.exitCode = 1;

function parse(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === "--manifest") out.manifest = argv[++i];
    else if (argv[i] === "--track") out.track = argv[++i];
    else if (argv[i] === "--harvey-checkout") out.harveyCheckout = argv[++i];
    else if (argv[i] === "--env-file") out.envFile = argv[++i];
    else throw new Error(`unknown argument: ${argv[i]}`);
  }
  return out;
}
