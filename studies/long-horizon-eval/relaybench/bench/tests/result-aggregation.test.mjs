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
