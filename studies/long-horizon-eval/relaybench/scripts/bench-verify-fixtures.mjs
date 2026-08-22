#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { PROJECT_ROOT, readJson, sha256 } from "../bench/lib/core.mjs";
import { loadManifest } from "../bench/lib/manifest.mjs";
import { validateSchedule } from "../bench/controller/stage-controller.mjs";

const manifest = await loadManifest();
validateSchedule(manifest.horizon.stage_schedule);
const candidate = await readJson(path.join(PROJECT_ROOT, manifest.candidate_matter.definition));
const sourceManifest = await readJson(path.join(PROJECT_ROOT, manifest.candidate_matter.source_manifest));
const proposedRubric = await readJson(path.join(PROJECT_ROOT, manifest.candidate_matter.proposed_intermediate_rubric));
const results = [];
for (const stage of manifest.horizon.stage_schedule) {
  const content = await fs.readFile(path.join(PROJECT_ROOT, stage.release_file));
  const parsed = JSON.parse(content.toString("utf8"));
  results.push({
    stage_id: stage.stage_id,
    test_only: parsed.test_only,
    event_type: parsed.event_type,
    sha256: sha256(content),
    passed: parsed.test_only === true && parsed.stage_id === stage.stage_id && !parsed.event_type.includes("CORRUPT"),
  });
}
const output = {
  verification_type: "TEST-ONLY_H4_FIXTURE_MECHANICS",
  candidate_status: candidate.candidate_status,
  harvey_task_json_sha256: candidate.harvey_lab.task_json_sha256,
  harvey_commit: sourceManifest.commit,
  harvey_source_files: sourceManifest.scenario.files.length,
  harvey_license: sourceManifest.license.spdx,
  synthetic_fixture_is_harvey_content: false,
  intermediate_rubric_status: proposedRubric.status,
  intermediate_rubric_stages: proposedRubric.stages.map((stage) => ({
    stage_id: stage.stage_id,
    status: stage.status,
    criteria: stage.criteria.length,
  })),
  official_harvey_score_claimed: false,
  stages: results,
};
process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
if (
  results.some((item) => !item.passed) ||
  sourceManifest.commit !== manifest.harvey_lab.candidate_commit ||
  sourceManifest.scenario.files.length !== 11 ||
  sourceManifest.scenario.files.some((file) => !/^[a-f0-9]{64}$/.test(file.sha256)) ||
  proposedRubric.status !== "PROPOSED_REQUIRES_RICHARD_TOMMY_APPROVAL" ||
  proposedRubric.stages.some((stage) => stage.status !== "APPROVAL_BLOCKED" || !stage.criteria.length)
) process.exitCode = 1;
