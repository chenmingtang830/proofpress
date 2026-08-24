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
  const audit = JSON.parse(await fs.readFile(path.join(output, "BLIND_POST_RUN_AUDIT.template.json")));
  assert.equal(audit.role, "blind_post_run_error_analysis_only");
  assert.equal(audit.signed_at, null);
});
