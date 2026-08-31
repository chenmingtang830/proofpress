const { readFileSync, existsSync } = require("node:fs");
const { resolve } = require("node:path");
const test = require("node:test");
const assert = require("node:assert/strict");

const root = resolve(__dirname, "..");
const html = readFileSync(resolve(root, "site/index.html"), "utf8");

test("landing page includes the required narrative sections", () => {
  for (const id of ["why", "how", "film", "partner"]) {
    assert.match(html, new RegExp(`id=["']${id}["']`));
  }

  assert.match(html, /Knowledge worth building on\./);
  assert.match(html, /governance layer for agent-produced knowledge/i);
  assert.match(html, /Only human approval authorizes downstream reuse\./);
});

test("landing page links to GitHub and preserves a real partner flow", () => {
  assert.match(html, /https:\/\/github\.com\/chenmingtang830\/proofpress/);
  assert.match(html, /id="partner-form"/);
  assert.match(html, /name="workflow"/);
  assert.match(html, /name="decision"/);
  assert.match(html, /confidential, privileged, personal, or customer data/);
});

test("landing page local assets and scripts exist", () => {
  for (const file of ["site/styles.css", "site/script.js", "assets/logo-on-dark.svg"]) {
    assert.equal(existsSync(resolve(root, file)), true, `${file} should exist`);
  }
});
