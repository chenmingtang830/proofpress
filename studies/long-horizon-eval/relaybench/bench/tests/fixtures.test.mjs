import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { PROJECT_ROOT, readJson } from "../lib/core.mjs";

const root = path.join(PROJECT_ROOT, "bench/fixtures/h4-msa-escalation-candidate");

test("candidate slot is pinned but explicitly approval-blocked", async () => {
  const candidate = await readJson(path.join(root, "candidate.json"));
  assert.equal(candidate.candidate_status, "REQUIRES_RICHARD_TOMMY_APPROVAL");
  assert.equal(candidate.official_harvey_score_claimed, false);
  assert.equal(candidate.harvey_lab.commit, "7be41d57fd5a6e97b5f246a029e810f83d09cd96");
  assert.equal(candidate.harvey_lab.final_rubric_criteria, 72);
  assert.equal(candidate.source_manifest, "bench/fixtures/h4-msa-escalation-candidate/HARVEY_SOURCE_MANIFEST.json");
  assert.equal(candidate.proposed_intermediate_rubric, "bench/fixtures/h4-msa-escalation-candidate/proposed-intermediate-rubrics.json");
  assert.equal(candidate.proposed_h4_release_schedule.length, 4);
  assert.equal(candidate.proposed_h4_release_schedule.filter((stage) => stage.cold_boundary_before).length, 1);
});

test("Harvey source identity is exact and synthetic inputs are not represented as Harvey material", async () => {
  const source = await readJson(path.join(root, "HARVEY_SOURCE_MANIFEST.json"));
  assert.equal(source.commit, "7be41d57fd5a6e97b5f246a029e810f83d09cd96");
  assert.equal(source.license.spdx, "MIT");
  assert.equal(source.license.sha256, "f92627d2ebe80fc0add3b171b2d7eee5e28a98dd0d0a4a5ee5829314243bb3b9");
  assert.equal(source.scenario.files.length, 11);
  assert.ok(source.scenario.files.every((file) => /^[a-f0-9]{40}$/.test(file.git_blob_sha)));
  assert.ok(source.scenario.files.every((file) => /^[a-f0-9]{64}$/.test(file.sha256)));
  assert.match(source.acquisition.synthetic_fixture_relationship, /not constructed/);
  const packet = await fs.readFile(path.join(PROJECT_ROOT, "PHASE_ZERO_FREEZE_PACKET.md"), "utf8");
  const sourceSection = packet.match(/## 2\. Harvey source identity, hashes, and license([\s\S]*?)## 3\. Complete proposed H4 release chain/);
  assert.ok(sourceSection, "freeze packet Harvey source section is missing");

  const displayed = [...sourceSection[1].matchAll(/^\| `([^`]+)` \| [^|]+ \| `([^`]+)` \|$/gm)]
    .map((match) => ({ path: match[1], sha256: match[2] }));
  const displayedPaths = displayed.map((entry) => entry.path);
  assert.equal(new Set(displayedPaths).size, displayed.length, "freeze packet contains a duplicated Harvey source path");
  assert.ok(displayed.every((entry) => /^[a-f0-9]{64}$/.test(entry.sha256)), "every displayed Harvey SHA-256 must be 64 lowercase hexadecimal characters");

  const prefix = `${source.scenario.base_path}/`;
  const expected = source.scenario.files.map((file) => {
    assert.ok(file.path.startsWith(prefix), `manifest source path is outside scenario base: ${file.path}`);
    return { path: file.path.slice(prefix.length), sha256: file.sha256 };
  });
  const byPath = (left, right) => left.path.localeCompare(right.path);
  assert.deepEqual(displayed.sort(byPath), expected.sort(byPath));
});

test("every H4 stage has a proposed approval-blocked intermediate rubric", async () => {
  const rubric = await readJson(path.join(root, "proposed-intermediate-rubrics.json"));
  assert.equal(rubric.status, "PROPOSED_REQUIRES_RICHARD_TOMMY_APPROVAL");
  assert.equal(rubric.official_harvey_rubric, false);
  assert.deepEqual(rubric.stages.map((stage) => stage.stage_id), ["S1", "S2", "S3", "S4"]);
  assert.ok(rubric.stages.every((stage) => stage.status === "APPROVAL_BLOCKED"));
  assert.ok(rubric.stages.every((stage) => stage.criteria.length === 4));
});

test("synthetic releases are deterministic H4 evolving-state inputs", async () => {
  const releases = [];
  for (const stage of ["S1", "S2", "S3", "S4"]) {
    const file = path.join(root, "test-double/releases", `${stage}.json`);
    const first = await fs.readFile(file, "utf8");
    const second = await fs.readFile(file, "utf8");
    assert.equal(first, second);
    const parsed = JSON.parse(first);
    assert.equal(parsed.test_only, true);
    assert.equal(parsed.stage_id, stage);
    assert.equal(parsed.event_type.includes("CORRUPT"), false);
    releases.push(parsed);
  }
  assert.deepEqual(releases.map((item) => item.operative_version), ["v1", "v2", "v3", "v4"]);
  assert.equal(releases[3].updates.find((item) => item.issue_id === "data_rights").reopened, true);
});
