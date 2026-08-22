import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { runBenchmark } from "../lib/runner.mjs";

test("TEST-ONLY H4 calibration enforces parity and a genuine cold worker boundary", async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "relaybench-h4-test-"));
  const output = path.join(root, "test-only");
  t.after(async () => fs.rm(root, { recursive: true, force: true }));
  const { runSet, records } = await runBenchmark({
    adapter: "deterministic-test",
    testOnly: true,
    pairedReplicates: 1,
    output,
  });
  assert.equal(runSet.episodes, 2);
  assert.equal(runSet.stage_records, 8);
  assert.equal(runSet.cold_boundaries, 2);
  assert.ok(records.every((record) => record.test_only && !record.publishable));
  assert.ok(records.every((record) => record.stages.map((stage) => stage.stage_id).join(",") === "S1,S2,S3,S4"));
  assert.ok(records.every((record) => record.information_parity.passed));
  assert.ok(records.every((record) => record.workspace_boundaries.length === 1 && record.workspace_boundaries[0].valid));
  assert.ok(records.every((record) => record.workspace_boundaries[0].worker_pid_changed));
  assert.ok(records.every((record) => record.workspace_boundaries[0].sender_worker_exited));
  assert.ok(records.every((record) => record.workspace_boundaries[0].sender_workspace_removed));
  assert.ok(records.every((record) => record.workspace_boundaries[0].pre_transfer_inventory.length === 0));
  assert.ok(records.every((record) => record.workspace_boundaries[0].prohibited_entries_found.length === 0));
  assert.ok(records.every((record) => record.deterministic_score.state_consistency.all_pass));
  assert.ok(records.every((record) => record.deterministic_score.eligible_for_benchmark_metrics === false));
  assert.equal(records.find((record) => record.condition === "C2_PROOFPRESS").verifier.status, "ok");
  assert.equal(records.find((record) => record.condition === "C1_ORDINARY_PORTABLE").verifier.status, "not_available_in_C1");
});

test("TEST-ONLY execution cannot escape its path or expand its replicate count", async () => {
  await assert.rejects(
    runBenchmark({adapter:"deterministic-test",testOnly:true,pairedReplicates:1,output:path.join(os.tmpdir(),"relaybench-publishable-forbidden")}),
    /test-only directory segment/,
  );
  await assert.rejects(
    runBenchmark({adapter:"deterministic-test",testOnly:true,pairedReplicates:2,output:path.join(os.tmpdir(),"test-only","relaybench-two")}),
    /exactly one/,
  );
});

test("real adapter scaffold remains blocked before invocation", async () => {
  await assert.rejects(
    runBenchmark({adapter:path.resolve("bench/adapters/provider-template.mjs"),testOnly:false,output:path.join(os.tmpdir(),"relaybench-real")}),
    /unresolved freeze gates/,
  );
});
