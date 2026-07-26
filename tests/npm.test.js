"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const test = require("node:test");

const ROOT = path.resolve(__dirname, "..");
const BIN = path.join(ROOT, "bin", "proofpress.js");

function run(args, cwd = ROOT) {
  return spawnSync(process.execPath, [BIN, ...args], {
    cwd,
    encoding: "utf8"
  });
}

test("npm launcher exposes the same version as package.json", () => {
  const { version } = JSON.parse(
    fs.readFileSync(path.join(ROOT, "package.json"), "utf8")
  );
  const result = run(["--version"]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), `proofpress ${version}`);
});

test("GitHub Action defaults to its bundled Proofpress CLI", () => {
  const action = fs.readFileSync(path.join(ROOT, "action.yml"), "utf8");
  assert.match(
    action,
    /proofpress-path:\s+description: "Optional path[\s\S]*?default: ""/
  );
  assert.match(action, /PP="\$GITHUB_ACTION_PATH\/proofpress\.py"/);
  assert.doesNotMatch(action, /default: "proofpress\.py"/);
});

test("setup installs an idempotent Codex contract, manifest, and badge", () => {
  const cwd = fs.mkdtempSync(path.join(os.tmpdir(), "proofpress-npm-"));
  fs.writeFileSync(path.join(cwd, "README.md"), "# Example\n\nBody.\n");

  const args = [
    "setup", "--agent", "codex", "--badge", "README.md", "--skip-git-config"
  ];
  const first = run(args, cwd);
  assert.equal(first.status, 0, first.stderr);
  const agentsOnce = fs.readFileSync(path.join(cwd, "AGENTS.md"), "utf8");
  const readmeOnce = fs.readFileSync(path.join(cwd, "README.md"), "utf8");
  const manifest = JSON.parse(
    fs.readFileSync(path.join(cwd, ".proofpress", "manifest.json"), "utf8")
  );

  assert.match(agentsOnce, /proofpress:setup:start/);
  assert.match(agentsOnce, /npx --no-install proofpress policy/);
  assert.doesNotMatch(agentsOnce, /python3 proofpress\.py/);
  assert.match(readmeOnce, /Proofpress: verifiable revision history/);
  assert.deepEqual(manifest.adapters, ["codex"]);

  const second = run(args, cwd);
  assert.equal(second.status, 0, second.stderr);
  assert.equal(fs.readFileSync(path.join(cwd, "AGENTS.md"), "utf8"), agentsOnce);
  assert.equal(fs.readFileSync(path.join(cwd, "README.md"), "utf8"), readmeOnce);
});

test("setup installs package-aware Claude and Cursor skills", () => {
  const cwd = fs.mkdtempSync(path.join(os.tmpdir(), "proofpress-skills-"));
  const result = run([
    "setup", "--agent", "claude", "--agent", "cursor", "--skip-git-config"
  ], cwd);
  assert.equal(result.status, 0, result.stderr);

  for (const target of [
    path.join(cwd, ".claude", "skills", "proofpress", "SKILL.md"),
    path.join(cwd, ".agents", "skills", "proofpress", "SKILL.md")
  ]) {
    const skill = fs.readFileSync(target, "utf8");
    assert.match(skill, /npx --no-install proofpress snapshot/);
    assert.match(skill, /Never\s+download or execute it without explicit consent/);
    assert.doesNotMatch(skill, /proofpress:meta:/);
  }
});
