import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { prepareRealPacket } from "../real/prepare.mjs";

test("real packet freezes paired conditions and a blind post-run audit without model calls", async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "relaybench-prepare-test-"));
  const checkout = path.join(root, "harvey");
  const taskRoot = path.join(checkout, "tasks/contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation/scenario-01");
  await fs.mkdir(path.join(taskRoot, "documents"), { recursive: true });
  const candidate = JSON.parse(await fs.readFile(new URL("../fixtures/h4-msa-escalation-candidate/candidate.json", import.meta.url)));
  await fs.writeFile(path.join(taskRoot, "task.json"), JSON.stringify({ title: "t", instructions: "i", criteria: Array(72).fill({}) }));
  for (const stage of candidate.proposed_h4_release_schedule) for (const file of stage.release)
    await fs.writeFile(path.join(taskRoot, "documents", file), `${stage.stage_id}:${file}`);
  const output = path.join(root, "packet");
  const manifestPath = new URL("../experiments/proofpress-pareto-v1.json", import.meta.url).pathname;
  const result = await prepareRealPacket({ manifestPath, harveyCheckout: checkout, output });
  assert.deepEqual(result.packet.conditions, ["C1_ORDINARY_PORTABLE", "C2_PROOFPRESS"]);
  assert.equal(result.packet.payable_calls_authorized, false);
  assert.equal(result.packet.copied_sources.length, 10);
  assert.equal(result.packet.harvey.knowledge_scope,
    "legal:lab:contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation/scenario-01");
  assert.match(result.packet.parity_contract, /neither receiver can reopen pre-boundary sources/);
  const audit = JSON.parse(await fs.readFile(path.join(output, "BLIND_POST_RUN_AUDIT.template.json")));
  assert.equal(audit.role, "blind_post_run_error_analysis_only");
  assert.equal(audit.signed_at, null);
});

test("stress packet preserves the LAB task and freezes one separate boundary artifact", async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "relaybench-stress-prepare-test-"));
  const checkout = path.join(root, "harvey");
  const taskId = "contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation/scenario-01";
  const taskRoot = path.join(checkout, "tasks", taskId);
  await fs.mkdir(path.join(taskRoot, "documents"), { recursive: true });
  const candidate = JSON.parse(await fs.readFile(new URL("../fixtures/h4-msa-escalation-candidate/candidate.json", import.meta.url)));
  await fs.writeFile(path.join(taskRoot, "task.json"), JSON.stringify({ title: "t", instructions: "i", criteria: Array(72).fill({}) }));
  for (const stage of candidate.proposed_h4_release_schedule) for (const file of stage.release)
    await fs.writeFile(path.join(taskRoot, "documents", file), `${stage.stage_id}:${file}`);
  const fixturePath = path.join(root, "stress.json");
  await fs.writeFile(fixturePath, JSON.stringify({ schema_version: 1, id: "stress-test", task_id: taskId,
    artifact_filename: "boundary-memory.json", statement: "Expired memory claim",
    raw_handoff_text: "Expired memory claim; revalidate before reliance.",
    expires_at: "2026-01-01T00:00:00Z", expected_proofpress_disposition: "expired_and_blocked_from_context" }));
  const manifestPath = new URL("../experiments/proofpress-pareto-v1.json", import.meta.url).pathname;
  const output = path.join(root, "packet");
  const result = await prepareRealPacket({ manifestPath, harveyCheckout: checkout, output,
    stressFixturePath: fixturePath, coldBoundaryBefore: "S4" });
  assert.equal(result.packet.study_arm, "LAB_DERIVED_CONTROLLED_HANDOFF_STRESS");
  assert.equal(result.packet.cold_boundary_before, "S4");
  assert.equal(result.packet.stages.find((x) => x.cold_boundary_before).stage_id, "S4");
  assert.equal(result.packet.stress.id, "stress-test");
  assert.match(result.packet.parity_contract, /same frozen boundary perturbation artifact/);
  await fs.access(path.join(output, result.packet.stress.artifact_path));
});
