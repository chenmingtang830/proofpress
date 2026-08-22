#!/usr/bin/env node
import path from "node:path";
import { runBenchmark } from "../bench/lib/runner.mjs";

const args = parseArgs(process.argv.slice(2));
if (args.help) {
  process.stdout.write(usage());
  process.exit(0);
}
if (!args.adapter || !args.output) {
  process.stderr.write(`${usage()}\nError: --adapter and --output are required.\n`);
  process.exit(2);
}

try {
  const result = await runBenchmark({
    manifest: args.manifest,
    adapter: args.adapter,
    output: path.resolve(args.output),
    testOnly: args.testOnly,
    pairedReplicates: args.pairedReplicates,
  });
  process.stdout.write(`${JSON.stringify(result.runSet, null, 2)}\n`);
} catch (error) {
  process.stderr.write(`RelayBench run refused: ${error.message}\n`);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const output = { testOnly: false };
  for (let index = 0; index < argv.length; index += 1) {
    const value = argv[index];
    if (value === "--help" || value === "-h") output.help = true;
    else if (value === "--test-only") output.testOnly = true;
    else if (value === "--adapter") output.adapter = argv[++index];
    else if (value === "--output") output.output = argv[++index];
    else if (value === "--manifest") output.manifest = argv[++index];
    else if (value === "--paired-replicates") output.pairedReplicates = Number(argv[++index]);
    else throw new Error(`Unknown argument: ${value}`);
  }
  return output;
}

function usage() {
  return [
    "RelayBench runner",
    "",
    "H4 TEST-ONLY mechanics calibration:",
    "  node scripts/bench-run.mjs --adapter deterministic-test --test-only --paired-replicates 1 --output /tmp/relaybench-h4/test-only",
    "",
    "Real execution is intentionally blocked until Richard/Tommy and provider-dependent freeze gates resolve.",
  ].join("\n");
}
