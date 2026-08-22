import assert from "node:assert/strict";
import test from "node:test";
import { StageController } from "../controller/stage-controller.mjs";

const schedule = [
  {stage_id:"S1",cold_boundary_before:false,release_file:"S1.json"},
  {stage_id:"S2",cold_boundary_before:false,release_file:"S2.json"},
  {stage_id:"S3",cold_boundary_before:true,release_file:"S3.json"},
  {stage_id:"S4",cold_boundary_before:false,release_file:"S4.json"},
];

function validBoundary() {
  return {
    valid: true,
    pre_transfer_inventory_empty: true,
    only_declared_transfer_package: true,
    sender_worker_exited: true,
    sender_workspace_removed: true,
    worker_pid_changed: true,
    previous_git_absent: true,
    sender_ledger_absent: true,
    session_state_absent: true,
    transcript_absent: true,
    conversation_absent: true,
    hidden_memory_absent: true,
    orchestrator_state_absent: true,
  };
}

test("controller permits only S1-S4 with one boundary before S3", () => {
  const controller = new StageController(schedule);
  assert.equal(controller.releaseNext({sessionToken:"worker-a"}).stage_id, "S1");
  assert.equal(controller.releaseNext({sessionToken:"worker-a"}).stage_id, "S2");
  assert.equal(controller.releaseNext({sessionToken:"worker-b",boundaryEvidence:validBoundary()}).stage_id, "S3");
  assert.equal(controller.releaseNext({sessionToken:"worker-b"}).stage_id, "S4");
  assert.equal(controller.state.complete, true);
  assert.deepEqual(controller.state.sessions_used, ["worker-a", "worker-b"]);
  assert.throws(() => controller.releaseNext({sessionToken:"worker-b"}), /complete/);
});

test("controller rejects early, missing, reused, or third worker sessions", () => {
  const early = new StageController(schedule);
  early.releaseNext({sessionToken:"worker-a"});
  assert.throws(() => early.releaseNext({sessionToken:"worker-b"}), /S1 and S2/);

  const reused = new StageController(schedule);
  reused.releaseNext({sessionToken:"worker-a"});
  reused.releaseNext({sessionToken:"worker-a"});
  assert.throws(() => reused.releaseNext({sessionToken:"worker-a",boundaryEvidence:validBoundary()}), /fresh worker/);

  const missing = new StageController(schedule);
  missing.releaseNext({sessionToken:"worker-a"});
  missing.releaseNext({sessionToken:"worker-a"});
  assert.throws(() => missing.releaseNext({sessionToken:"worker-b"}), /cold-boundary/);

  const third = new StageController(schedule);
  third.releaseNext({sessionToken:"worker-a"});
  third.releaseNext({sessionToken:"worker-a"});
  third.releaseNext({sessionToken:"worker-b",boundaryEvidence:validBoundary()});
  assert.throws(() => third.releaseNext({sessionToken:"worker-c"}), /S3 and S4/);
});
