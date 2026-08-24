import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { prepareRealPacket } from "../real/prepare.mjs";
import { runPrepare, runResume } from "../real/run.mjs";

test("real runner cannot make a call without the explicit payable-call flag", async () => {
  await assert.rejects(runPrepare({
    packetDir: "/unused", output: "/unused", root: "/unused", trackId: "A_HARVEY_COMPARABLE",
    authorizeRealCalls: false, manifest: { real_calls_authorized: false },
  }), /authorize-real-calls/);
});

test("mocked payable path uses automated policy admission then reaches LAB evaluation", async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "relaybench-real-run-"));
  const checkout = path.join(root, "harvey");
  const taskRoot = path.join(checkout, "tasks/contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation/scenario-01");
  await fs.mkdir(path.join(taskRoot, "documents"), { recursive: true });
  const candidate = JSON.parse(await fs.readFile(new URL("../fixtures/h4-msa-escalation-candidate/candidate.json", import.meta.url)));
  await fs.writeFile(path.join(taskRoot, "task.json"), JSON.stringify({ title: "t", instructions: "i", criteria: Array(72).fill({}) }));
  for (const stage of candidate.proposed_h4_release_schedule) for (const file of stage.release)
    await fs.writeFile(path.join(taskRoot, "documents", file), `${stage.stage_id}:${file}`);
  const manifestPath = new URL("../experiments/proofpress-pareto-v1.json", import.meta.url).pathname;
  const manifest = JSON.parse(await fs.readFile(manifestPath));
  const packet = path.join(root, "packet"); await prepareRealPacket({ manifestPath, harveyCheckout: checkout, output: packet });
  const prompts = [];
  const adapter = { metadata: () => ({ id: "mock" }), invoke: async ({ prompt }) => {
    prompts.push(prompt);
    const stage = prompt.match(/Current stage: (S\d)/)[1];
    return { raw_output: JSON.stringify({ stage_id: stage, summary: `summary-${stage}`,
      conclusions: stage === "S1" ? [
        { statement: "Bound conclusion", evidence_files: ["deal-economics-summary.xlsx"] },
        { statement: "Unsupported conclusion", evidence_files: ["deal-economics-summary.xlsx"] },
      ] : [],
      ...(stage === "S4" ? { final_markdown: "# Escalation memo\n\nApproved content." } : {}) }), telemetry: { model_calls: 1 } };
  }};
  const output = path.join(root, "run");
  const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../../..");
  const judge = { metadata: () => ({ id: "mock-judge" }), invoke: async ({ prompt }) => ({
    raw_output: JSON.stringify(prompt.includes("Unsupported conclusion")
      ? { recommendation: "reject", rationale: "contradicted" }
      : { recommendation: "accept", rationale: "explicit support" }), telemetry: { model_calls: 1 },
  }) };
  const prepared = await runPrepare({ packetDir: packet, output, manifest, trackId: "A_HARVEY_COMPARABLE",
    authorizeRealCalls: true, root: repoRoot, adapterOverride: adapter, judgeOverride: judge });
  assert.equal(prepared.status, "POLICY_GATE_COMPLETE");
  assert.deepEqual(prepared.episodes.C2_PROOFPRESS.proposals.map((x) => x.admitted), [true, false]);
  assert.ok(prompts.filter((x) => x.includes("Current stage: S1")).every((x) => !x.includes("business-team-update.docx")));
  const resumed = await runResume({ output, manifest, authorizeRealCalls: true, root: repoRoot, adapterOverride: adapter });
  assert.equal(resumed.status, "READY_FOR_LAB_EVALUATION");
  const inherited = JSON.parse(await fs.readFile(path.join(output, "receiver/C2_PROOFPRESS/INHERITED_CONTEXT.json")));
  assert.equal(inherited.proofpress_trusted_context.knowledge.length, 1);
  for (const condition of ["C1_ORDINARY_PORTABLE", "C2_PROOFPRESS"])
    await fs.access(resumed.episodes[condition].deliverable);
});
