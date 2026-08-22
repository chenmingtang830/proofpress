#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";
import { PROJECT_ROOT } from "../bench/lib/core.mjs";

const files = await walk(PROJECT_ROOT);
const sourceFiles = files.filter((file) => file.endsWith(".mjs"));
const jsonFiles = files.filter((file) => file.endsWith(".json"));
const errors = [];

for (const file of sourceFiles) {
  const result = await run(process.execPath, ["--check", file]);
  if (result.exitCode !== 0) errors.push(`${path.relative(PROJECT_ROOT, file)}: ${result.stderr.trim()}`);
}
for (const file of jsonFiles) {
  try {
    JSON.parse(await fs.readFile(file, "utf8"));
  } catch (error) {
    errors.push(`${path.relative(PROJECT_ROOT, file)}: invalid JSON (${error.message})`);
  }
}
const forbiddenName = /(^|\/)(\.env[^/]*|credentials?|secrets?|tokens?|node_modules|\.git|\.cache|dist|coverage)(\/|$)/i;
for (const file of files) {
  const relative = path.relative(PROJECT_ROOT, file);
  if (forbiddenName.test(relative) && relative !== ".gitignore") errors.push(`${relative}: forbidden project artifact`);
}

const publishableResults = files.filter((file) =>
  file.includes(`${path.sep}bench${path.sep}results${path.sep}publishable${path.sep}`),
);
if (publishableResults.length) errors.push("Publishable result files exist before a real approved run");

if (errors.length) {
  process.stderr.write(`${errors.join("\n")}\n`);
  process.exitCode = 1;
} else {
  process.stdout.write(`RelayBench lint passed: ${sourceFiles.length} JavaScript files, ${jsonFiles.length} JSON files, no forbidden artifacts.\n`);
}

async function walk(root) {
  const output = [];
  async function visit(directory) {
    for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) await visit(absolute);
      else if (entry.isFile()) output.push(absolute);
      else output.push(absolute);
    }
  }
  await visit(root);
  return output;
}

async function run(program, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(program, args, { cwd: PROJECT_ROOT });
    let stderr = "";
    child.stderr.setEncoding("utf8");
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.once("error", reject);
    child.once("close", (exitCode) => resolve({ exitCode, stderr }));
  });
}
