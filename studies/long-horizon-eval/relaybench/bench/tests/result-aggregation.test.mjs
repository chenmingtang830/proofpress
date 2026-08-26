import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");

test("cross-model aggregation preserves complete, incomplete, and unavailable evidence tiers", () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "relaybench-model-summary-"));
  const output = path.join(tmp, "summary.json");
  execFileSync(process.execPath, ["scripts/bench-aggregate-model-ladder.mjs", output], {
    cwd: root,
    stdio: "ignore",
  });
  const summary = JSON.parse(fs.readFileSync(output, "utf8"));
  assert.equal(summary.complete_panel_count, 2);
  assert.equal(summary.tracks.find(({ id }) => id === "deepseek_anchor").evidence_tier, "complete_frozen_panel");
  assert.equal(summary.tracks.find(({ id }) => id === "opus48_gateway").evidence_tier, "complete_frozen_panel");
  assert.equal(summary.tracks.find(({ id }) => id === "glm52").evidence_tier, "incomplete_descriptive_only");
  assert.equal(summary.tracks.find(({ id }) => id === "gpt56_sol").evidence_tier, "route_unavailable");
  assert.equal(summary.tracks.find(({ id }) => id === "deepseek_anchor").protection.raw_unsafe, 4);
});

test("committed task expansion reports floor sensitivity and missing cells explicitly", () => {
  const result = JSON.parse(fs.readFileSync(
    path.join(root, "results/deepseek-v9-14-task-expansion-2026-08-25.json"),
    "utf8",
  ));
  assert.deepEqual(result.completion, {
    planned_tasks: 14,
    valid_tasks: 12,
    invalid_task_count: 2,
    valid_task_rate: 12 / 14,
    all_tasks_observed: false,
  });
  assert.equal(result.quality.overall.tasks, 12);
  assert.equal(result.quality.non_floor_sensitivity.tasks, 9);
  assert.deepEqual(result.quality.overall.direction, { positive: 10, tie: 1, negative: 1 });
  assert.equal(result.quality.overall.raw_floor_tasks_below_25_percent.length, 3);
});

test("replication aggregation counts reused governance once across cells", () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "relaybench-shared-governance-"));
  const source = path.join(tmp, "senders/credit/run");
  const run = path.join(tmp, "repeat-1/clean/credit/run");
  fs.mkdirSync(source, { recursive: true });
  fs.mkdirSync(run, { recursive: true });
  fs.writeFileSync(path.join(source, "RUN_STATE.json"), JSON.stringify({
    episodes: { C2_PROOFPRESS: { judge_transaction: { telemetry: telemetry("shared", 100, 20) } } },
  }));
  fs.writeFileSync(path.join(run, "RUN_STATE.json"), JSON.stringify({
    status: "READY_FOR_LAB_EVALUATION",
    episodes: {
      C1_ORDINARY_PORTABLE: { stages: [{ stage_id: "S4", telemetry: telemetry("raw", 10, 5) }] },
      C2_PROOFPRESS: {
        stages: [{ stage_id: "S4", telemetry: telemetry("proofpress", 12, 6) }],
        judge_transaction: null,
        governance_reuse: { source_run: source },
        trace_lookup: {},
      },
    },
  }));
  fs.writeFileSync(path.join(run, "PUBLIC_RUBRIC_SCORES.json"), JSON.stringify({
    C1_ORDINARY_PORTABLE: { criteria_passed: 8, criteria_total: 10, criterion_pass_rate: 0.8,
      telemetry: telemetry("eval-raw", 3, 1) },
    C2_PROOFPRESS: { criteria_passed: 9, criteria_total: 10, criterion_pass_rate: 0.9,
      telemetry: telemetry("eval-proofpress", 3, 1) },
  }));
  const output = path.join(tmp, "aggregate.json");
  execFileSync(process.execPath, ["scripts/bench-aggregate-replication.mjs",
    "--root", tmp, "--model", "test/model", "--track", "TEST", "--out", output], { cwd: root });
  const result = JSON.parse(fs.readFileSync(output, "utf8"));
  assert.equal(result.proof_price.shared_governance.source_transactions, 1);
  assert.equal(result.proof_price.shared_governance.resources.model_calls, 1);
  assert.equal(result.proof_price.shared_governance.resources.total_tokens, 120);
  assert.equal(result.proof_price.full_panel.incremental.total_tokens, 3);
  assert.equal(result.proof_price.full_panel.all_in.total_tokens, 123);
});

function telemetry(requestId, inputTokens, outputTokens) {
  return { request_id: requestId, model_calls: 1, input_tokens: inputTokens,
    output_tokens: outputTokens, reasoning_tokens: 0, provider_cost_usd: 0,
    wall_clock_latency_ms: 1 };
}
