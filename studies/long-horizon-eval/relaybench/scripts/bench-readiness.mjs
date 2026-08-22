#!/usr/bin/env node
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { PROJECT_ROOT, readJson } from "../bench/lib/core.mjs";
import { loadManifest, realRunBlockers, verifyFrozenFiles } from "../bench/lib/manifest.mjs";
import { runBenchmark } from "../bench/lib/runner.mjs";
import { aggregateRecords } from "../bench/scoring/score.mjs";
import { renderReport } from "./bench-report.mjs";

const manifest = await loadManifest();
const checks = [];
const frozen = await verifyFrozenFiles(manifest);
check("frozen_files", frozen.valid && manifest.frozen_files.length > 0, frozen.valid ? `${manifest.frozen_files.length} frozen file hashes match` : JSON.stringify(frozen.mismatches));

const decisions = manifest.freeze_status.decision_register;
const classifications = new Set([
  "Defined by Richard's plan",
  "Safe implementation detail",
  "Requires Richard/Tommy approval",
  "Provider-dependent",
  "Deferred beyond H4 calibration",
]);
check("freeze_decision_count", manifest.freeze_status.decision_count === 12 && decisions.length === 12, "exactly 12 freeze decisions are declared");
check("freeze_decision_classification", decisions.every((item) => classifications.has(item.classification)), "all 12 decisions use an allowed classification");
check("scientific_freeze_blocked", manifest.freeze_status.scientific_freeze_approved === false && manifest.freeze_status.real_run_ready === false, "scientific freeze and real execution remain blocked");
check("canonical_scope", manifest.scope.horizon === "H4" && manifest.scope.stress_track === "EVOLVING_NEGOTIATION_STATE" && manifest.scope.conditions.join(",") === "C1_ORDINARY_PORTABLE,C2_PROOFPRESS", "scope is H4 evolving state, C1 versus C2 only");
check("phase_zero_only", manifest.scope.phase === "PHASE_ZERO" && manifest.scope.real_model_calls === false && manifest.scope.pilot_runs === false, "scope is Phase Zero mechanics only");
check("one_registered_boundary", manifest.horizon.stages === 4 && manifest.horizon.cold_boundaries === 1 && manifest.horizon.stage_schedule.filter((stage) => stage.cold_boundary_before).map((stage) => stage.stage_id).join(",") === "S3", "four stages and one boundary before S3");
check("candidate_not_silently_frozen", manifest.candidate_matter.status === "REQUIRES_RICHARD_TOMMY_APPROVAL", "recommended Harvey matter remains approval-blocked");
check("fallback_disabled", manifest.model.provider_fallback === false && manifest.model.cross_provider_retries === false, "provider fallback and cross-provider retries disabled");
check("proofpress_base_pin", manifest.proofpress_integration.base_commit === "10ee8c4c9a6d56dfedf563a0679e6a5bb167fa0a" && manifest.canonical_research_plan.head_commit === manifest.proofpress_integration.base_commit, "stacked base and canonical PR head are exactly 10ee8c4");
check("richard_files_untouched", manifest.proofpress_integration.richard_plan_files_modified === false && manifest.proofpress_integration.proofpress_engine_modified === false, "Richard's plan/flow and Proofpress engine are declared untouched");

const sourceManifest = await readJson(path.join(PROJECT_ROOT, manifest.candidate_matter.source_manifest));
check("harvey_source_identity", sourceManifest.commit === "7be41d57fd5a6e97b5f246a029e810f83d09cd96" && sourceManifest.scenario.files.length === 11 && sourceManifest.scenario.files.every((file) => /^[a-f0-9]{64}$/.test(file.sha256)), "Harvey acquisition manifest pins one commit and 11 path-level SHA-256 hashes");
check("harvey_license_identity", sourceManifest.license.spdx === "MIT" && sourceManifest.license.sha256 === "f92627d2ebe80fc0add3b171b2d7eee5e28a98dd0d0a4a5ee5829314243bb3b9", "Harvey MIT license identity is pinned");
check("synthetic_boundary_honest", sourceManifest.acquisition.synthetic_fixture_relationship.includes("not constructed") && manifest.candidate_matter.test_double_is_harvey_content === false, "synthetic test fixture is not represented as Harvey material");

const proposedRubric = await readJson(path.join(PROJECT_ROOT, manifest.candidate_matter.proposed_intermediate_rubric));
check("intermediate_rubrics_blocked", proposedRubric.status === "PROPOSED_REQUIRES_RICHARD_TOMMY_APPROVAL" && proposedRubric.stages.map((stage) => stage.stage_id).join(",") === "S1,S2,S3,S4" && proposedRubric.stages.every((stage) => stage.status === "APPROVAL_BLOCKED" && stage.criteria.length > 0), "every H4 stage has a proposed approval-blocked rubric");

const resultFiles = await listFiles(path.join(PROJECT_ROOT, "bench/results"));
check("no_publishable_results", resultFiles.every((file) => !file.includes(`${path.sep}publishable${path.sep}`)), "no publishable result record exists");
check("no_retained_test_output", resultFiles.filter((file) => file.endsWith(".json")).length === 0, "repository contains no generated TEST-ONLY JSON records");

const temporaryRoot = await fs.mkdtemp(path.join(os.tmpdir(), "relaybench-readiness-"));
try {
  const output = path.join(temporaryRoot, "test-only");
  const { runSet, records } = await runBenchmark({adapter:"deterministic-test",testOnly:true,pairedReplicates:1,output});
  const score = aggregateRecords(records);
  const report = renderReport(score);
  check("test_only_e2e_shape", runSet.episodes === 2 && runSet.stage_records === 8 && runSet.cold_boundaries === 2, "paired TEST-ONLY H4 run produced 2 episodes, 8 stages, and 2 per-condition boundary records");
  check("information_parity", records.every((record) => record.information_parity.passed && record.information_parity.c1_substantive_projection_sha256 === record.information_parity.c2_substantive_projection_sha256), "C1/C2 substantive projections are machine-equal");
  check("cold_worker_boundary", records.every((record) => {
    const boundary = record.workspace_boundaries[0];
    return boundary.valid && boundary.worker_pid_changed && boundary.sender_worker_exited && boundary.sender_workspace_removed && boundary.pre_transfer_inventory_empty && boundary.only_declared_transfer_package;
  }), "fresh process/workspace boundary is enforced before S3");
  check("test_only_excluded", score.publishable_records_seen === 0 && score.excluded_test_only_records === 2 && score.metrics.final_all_pass_rate.rate === null, "both TEST-ONLY episodes are excluded from metrics");
  check("no_simulated_lab_score", records.every((record) => record.evaluation.legal_rubric.status === "NOT_RUN_TEST_ONLY") && report.includes("Harvey LAB evaluator was not run or simulated"), "no Harvey score or benchmark result is simulated");
} finally {
  await fs.rm(temporaryRoot, { recursive: true, force: true });
}

const blockers = realRunBlockers(manifest);
check("real_calls_blocked", blockers.length > 0, `${blockers.length} machine-enforced real-run blockers remain`);

for (const item of checks) process.stdout.write(`${item.passed ? "PASS" : "FAIL"} ${item.id}: ${item.note}\n`);
process.stdout.write(`\nH4 TEST-ONLY mechanics readiness: ${checks.every((item) => item.passed) ? "PASS" : "FAIL"}\n`);
process.stdout.write("Scientific freeze: BLOCKED pending Richard/Tommy and provider-dependent decisions\n");
process.stdout.write("Real benchmark execution: BLOCKED; no result claimed\n");
if (checks.some((item) => !item.passed)) process.exitCode = 1;

function check(id, passed, note) {
  checks.push({ id, passed: Boolean(passed), note });
}

async function listFiles(root) {
  const output = [];
  async function visit(directory) {
    let entries;
    try {
      entries = await fs.readdir(directory, { withFileTypes: true });
    } catch (error) {
      if (error.code === "ENOENT") return;
      throw error;
    }
    for (const entry of entries) {
      const absolute = path.join(directory, entry.name);
      if (entry.isDirectory()) await visit(absolute);
      else if (entry.isFile()) output.push(absolute);
    }
  }
  await visit(root);
  return output;
}
