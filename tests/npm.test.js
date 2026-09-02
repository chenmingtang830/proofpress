"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawn, spawnSync } = require("node:child_process");
const test = require("node:test");

const ROOT = path.resolve(__dirname, "..");
const BIN = path.join(ROOT, "bin", "proofpress.js");

function run(args, cwd = ROOT) {
  return spawnSync(process.execPath, [BIN, ...args], {
    cwd,
    encoding: "utf8"
  });
}

test("hosted owner UI production bundle parses", () => {
  const staticRoot = path.join(ROOT, "src/proofpress/hosted/static");
  const html = fs.readFileSync(path.join(staticRoot, "index.html"), "utf8");
  const scriptPath = html.match(/<script[^>]+src="([^"]+\.js)"/)[1];
  const stylesheetPath = html.match(/<link[^>]+href="([^"]+\.css)"/)[1];
  assert.equal(html.includes('<div id="root"></div>'), true);
  assert.equal(fs.existsSync(path.join(staticRoot, scriptPath)), true);
  assert.equal(fs.existsSync(path.join(staticRoot, stylesheetPath)), true);
  const result = spawnSync(
    process.execPath,
    ["--check", path.join(staticRoot, scriptPath)],
    { encoding: "utf8" }
  );
  assert.equal(result.status, 0, result.stderr);
});

test("npm launcher exposes the same version as package.json", () => {
  const { version } = JSON.parse(
    fs.readFileSync(path.join(ROOT, "package.json"), "utf8")
  );
  const result = run(["--version"]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), `proofpress ${version}`);
});

test("npm launcher exposes the verified-knowledge ledger commands", () => {
  const result = run(["knowledge", "--help"]);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /\{ingest,propose,policy-review,review,supersede,policy-set,context,view,verify,materialize\}/);
  assert.match(result.stdout, /policy-review/);
  assert.match(result.stdout, /materialize/);
});

test("npm launcher exposes the flat local-MVP commands", () => {
  for (const args of [
    ["evidence", "import", "--help"], ["propose", "--help"],
    ["evaluate", "--help"], ["judge", "--help"], ["review", "--help"],
    ["supersede", "--help"], ["context", "--help"], ["ui", "--help"],
    ["import-v1", "--help"]
  ]) {
    const result = run(args);
    assert.equal(result.status, 0, `${args.join(" ")}\n${result.stderr}`);
  }
});

test("GitHub Action defaults to its bundled Proofpress CLI", () => {
  const action = fs.readFileSync(path.join(ROOT, "action.yml"), "utf8");
  assert.match(
    action,
    /proofpress-path:\s+description: "Deprecated 0\.6 path[\s\S]*?default: ""/
  );
  assert.match(action, /python3 -m proofpress\.cli legacy/);
  assert.match(action, /GITHUB_ACTION_PATH\/src/);
  assert.doesNotMatch(action, /default: "proofpress\.py"/);
});

test("npm release workflow closes the GitHub Release conditional", () => {
  const workflow = fs.readFileSync(
    path.join(ROOT, ".github", "workflows", "npm-stage.yml"),
    "utf8"
  );
  assert.match(
    workflow,
    /gh release create "\$tag" \\\n[\s\S]*?--generate-notes\n\s+fi\s*$/
  );
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
