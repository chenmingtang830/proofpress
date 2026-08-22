#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { aggregateRecords } from "../bench/scoring/score.mjs";
import { loadRunRecords } from "../bench/lib/results.mjs";

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  await main();
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.input || !args.output) {
    process.stderr.write("Usage: node scripts/bench-score.mjs --input <result-directory> --output <score.json>\n");
    process.exitCode = 2;
    return;
  }
  try {
    const records = await loadRunRecords(path.resolve(args.input));
    const report = aggregateRecords(records);
    await fs.mkdir(path.dirname(path.resolve(args.output)), { recursive: true });
    await fs.writeFile(path.resolve(args.output), `${JSON.stringify(report, null, 2)}\n`, { flag: "wx" });
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } catch (error) {
    process.stderr.write(`RelayBench scoring failed: ${error.message}\n`);
    process.exitCode = 1;
  }
}

function parseArgs(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--input") values.input = argv[++index];
    else if (argv[index] === "--output") values.output = argv[++index];
    else throw new Error(`Unknown argument: ${argv[index]}`);
  }
  return values;
}
