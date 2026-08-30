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

test("npm launcher exposes the same version as package.json", () => {
  const { version } = JSON.parse(
    fs.readFileSync(path.join(ROOT, "package.json"), "utf8")
  );
  const result = run(["--version"]);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), `proofpress ${version}`);
});

test("claim gateway writes a terminal receipt when credentials are missing", async () => {
  const cwd = fs.mkdtempSync(path.join(os.tmpdir(), "proofpress-claim-gateway-"));
  const receipts = path.join(cwd, "receipts.jsonl");
  const env = { ...process.env,
    PROOFPRESS_CLAIM_MODEL: "test/model", PROOFPRESS_CLAIM_PROVIDER: "test-provider",
    PROOFPRESS_CLAIM_PORT: "0", PROOFPRESS_CLAIM_RECEIPTS: receipts,
  };
  delete env.AI_GATEWAY_API_KEY;
  const child = spawn(process.execPath,
    [path.join(ROOT, "tools/claim-construction-gateway/gateway_openai_server.mjs")],
    { cwd: ROOT, env, stdio: ["ignore", "pipe", "pipe"] });
  try {
    const ready = await new Promise((resolve, reject) => {
      let stdout = "";
      child.stdout.on("data", chunk => {
        stdout += chunk;
        const newline = stdout.indexOf("\n");
        if (newline >= 0) resolve(JSON.parse(stdout.slice(0, newline)));
      });
      child.once("error", reject);
      child.once("exit", code => reject(new Error(`gateway exited ${code}`)));
    });
    const response = await fetch(`http://127.0.0.1:${ready.port}/v1/chat/completions`, {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ model: "test/model", messages: [{ role: "user", content: "x" }] }),
    });
    assert.equal(response.status, 503);
    assert.equal(ready.reasoning, "none");
    const rows = fs.readFileSync(receipts, "utf8").trim().split("\n").map(JSON.parse);
    assert.equal(rows.length, 1);
    assert.equal(rows[0].terminal, true);
    assert.equal(rows[0].status, "inconclusive");
    assert.equal(rows[0].error_type, "missing_gateway_key");
    assert.equal(rows[0].requested_reasoning, "none");
    assert.equal(typeof rows[0].latency_ms, "number");
  } finally {
    child.kill();
  }
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
    /proofpress-path:\s+description: "Optional path[\s\S]*?default: ""/
  );
  assert.match(action, /PP="\$GITHUB_ACTION_PATH\/proofpress\.py"/);
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
