#!/usr/bin/env node
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { PROJECT_ROOT, readJson, sha256File } from "../bench/lib/core.mjs";

const execFileAsync = promisify(execFile);

const checkout = process.argv[2] ? path.resolve(process.argv[2]) : null;
if (!checkout) {
  process.stderr.write("Usage: node scripts/bench-verify-harvey-source.mjs <harvey-labs-checkout>\n");
  process.exit(2);
}

const manifestPath = path.join(
  PROJECT_ROOT,
  "bench/fixtures/h4-msa-escalation-candidate/HARVEY_SOURCE_MANIFEST.json",
);
const manifest = await readJson(manifestPath);
let actualCommit = null;
try {
  const result = await execFileAsync("git", ["-C", checkout, "rev-parse", "HEAD"], { encoding: "utf8" });
  actualCommit = result.stdout.trim();
} catch {
  actualCommit = null;
}
const checks = [];
for (const file of manifest.scenario.files) {
  const absolute = path.join(checkout, file.path);
  let actual = null;
  try {
    actual = await sha256File(absolute);
  } catch (error) {
    checks.push({ path: file.path, passed: false, expected_sha256: file.sha256, actual_sha256: null, error: error.message });
    continue;
  }
  checks.push({ path: file.path, passed: actual === file.sha256, expected_sha256: file.sha256, actual_sha256: actual });
}
const output = {
  verification_type: "PINNED_HARVEY_SOURCE_SHA256",
  expected_commit: manifest.commit,
  actual_commit: actualCommit,
  commit_matches: actualCommit === manifest.commit,
  files_checked: checks.length,
  passed: actualCommit === manifest.commit && checks.every((item) => item.passed),
  checks,
};
process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
if (!output.passed) process.exitCode = 1;
