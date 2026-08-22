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
    process.stderr.write("Usage: node scripts/bench-report.mjs --input <result-directory> --output <report.md>\n");
    process.exitCode = 2;
    return;
  }
  try {
    const records = await loadRunRecords(path.resolve(args.input));
    const score = aggregateRecords(records);
    const markdown = renderReport(score);
    await fs.mkdir(path.dirname(path.resolve(args.output)), { recursive: true });
    await fs.writeFile(path.resolve(args.output), markdown, { flag: "wx" });
    process.stdout.write(markdown);
  } catch (error) {
    process.stderr.write(`RelayBench report failed: ${error.message}\n`);
    process.exitCode = 1;
  }
}

export function renderReport(score) {
  const lines = [
    "# RelayBench H4 result report",
    "",
    `Generated: \`${score.generated_at}\``,
    "",
    `Publishable episodes: **${score.publishable_records_seen}**`,
    `Valid publishable episodes: **${score.valid_publishable_records}**`,
    `Excluded TEST-ONLY records: **${score.excluded_test_only_records}**`,
    `Invalid publishable records: **${score.invalid_runs.count}**`,
    "",
  ];
  if (score.valid_publishable_records === 0) {
    lines.push(
      "## No benchmark result",
      "",
      "No valid publishable episodes were present. RelayBench does not compute or display performance rates from TEST-ONLY or invalid records.",
      "",
      "The Harvey LAB evaluator was not run or simulated. This file is a harness-output check, not a model, condition, or product comparison.",
      "",
    );
    return `${lines.join("\n")}\n`;
  }
  lines.push(
    "## Metrics",
    "",
    "| Metric | Numerator | Denominator | Rate |",
    "|---|---:|---:|---:|",
  );
  for (const id of [
    "final_all_pass_rate",
    "final_criterion_pass_rate",
    "unsafe_state_propagation",
    "state_consistency_criterion_rate",
  ]) {
    const metric = score.metrics[id];
    lines.push(`| ${id} | ${metric.numerator} | ${metric.denominator} | ${metric.rate === null ? "unavailable" : metric.rate.toFixed(4)} |`);
  }
  lines.push(
    "",
    "Outcome families remain separate. These rates describe only a frozen real run set and do not establish legal intelligence, factual truth, authorship, authorization, or official Harvey LAB performance.",
    "",
  );
  return `${lines.join("\n")}\n`;
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
