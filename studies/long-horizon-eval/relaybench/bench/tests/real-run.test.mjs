import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { prepareRealPacket } from "../real/prepare.mjs";
import { aggregateSegmentTelemetry, deterministicTraceSelection, normalizeEvidenceFileNames,
  runPrepare, runResume } from "../real/run.mjs";

test("real runner cannot make a call without the explicit payable-call flag", async () => {
  await assert.rejects(runPrepare({
    packetDir: "/unused", output: "/unused", root: "/unused", trackId: "A_HARVEY_COMPARABLE",
    authorizeRealCalls: false, manifest: { real_calls_authorized: false },
  }), /authorize-real-calls/);
});

test("evidence filenames accept exact names, unique basenames, or a bounded annotation", () => {
  const available = ["second-line-risk-review.docx", "counter-proposed-term-sheet.docx"];
  assert.deepEqual(normalizeEvidenceFileNames([
    "credit/packet/source/S3/second-line-risk-review.docx",
    "counter-proposed-term-sheet.docx",
    "credit-policy-manual.docx (Rev. 2024-03)",
    "credit/packet/source/S3/second-line-risk-review.docx",
  ], [...available, "credit-policy-manual.docx"]),
  ["second-line-risk-review.docx", "counter-proposed-term-sheet.docx", "credit-policy-manual.docx"]);
  assert.throws(() => normalizeEvidenceFileNames(["invented.docx"], available), /unknown or ambiguous/);
  assert.throws(() => normalizeEvidenceFileNames(["credit-policy-manual.docx arbitrary suffix"],
    [...available, "credit-policy-manual.docx"]), /unknown or ambiguous/);
  assert.throws(() => normalizeEvidenceFileNames(["x/shared.docx"], ["S1/shared.docx", "S2/shared.docx"]), /unknown or ambiguous/);
});

test("deterministic graph selection emits only real current ledger ids", () => {
  const trusted = { knowledge: [
    { id: "knw_2", statement: "second" },
    { id: "knw_1", statement: "first" },
    { id: "knw_3", statement: "third" },
  ] };
  assert.deepEqual(deterministicTraceSelection(trusted, 2, ["knw_2"]), {
    knowledge_ids: ["knw_1", "knw_3"],
    checklist: [{ requirement: "Current admitted governed knowledge at the receiver boundary",
      knowledge_ids: ["knw_1", "knw_3"], coverage: "covered" }],
    rationale: "Deterministic ledger-order selection: 2/2 current admitted receipts.",
  });
});

test("planned S4 segment telemetry preserves every request and the aggregate cap", () => {
  const telemetry = aggregateSegmentTelemetry([
    { telemetry: { request_id: "r1", finish_reason: "stop", input_tokens: 10, output_tokens: 4,
      output_cap_hit: false, wall_clock_latency_ms: 100, reasoning_tokens: 2,
      provider_cost_usd: 0.01, actual_incremental_cash_usd: null, model_calls: 1, retries: 0 } },
    { telemetry: { request_id: "r2", finish_reason: "stop", input_tokens: 12, output_tokens: 5,
      output_cap_hit: false, wall_clock_latency_ms: 120, reasoning_tokens: 3,
      provider_cost_usd: 0.02, actual_incremental_cash_usd: null, model_calls: 1, retries: 0 } },
  ], 20, "memo-halves-v1");
  assert.deepEqual(telemetry.segment_request_ids, ["r1", "r2"]);
  assert.equal(telemetry.request_id, "segments:r1|r2");
  assert.equal(telemetry.input_tokens, 22);
  assert.equal(telemetry.output_tokens, 9);
  assert.equal(telemetry.output_cap_tokens, 20);
  assert.equal(telemetry.output_cap_hit, false);
  assert.equal(telemetry.model_calls, 2);
  assert.equal(telemetry.provider_cost_usd, 0.03);
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
  const stressFixturePath = path.join(root, "stress.json");
  await fs.writeFile(stressFixturePath, JSON.stringify({ schema_version: 1, id: "stress-test",
    task_id: "contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation/scenario-01",
    artifact_filename: "boundary-memory.json", statement: "Expired memory claim",
    raw_handoff_text: "Expired memory claim; revalidate before reliance.",
    expires_at: "2026-01-01T00:00:00Z", expected_proofpress_disposition: "expired_and_blocked_from_context" }));
  const packet = path.join(root, "packet"); await prepareRealPacket({ manifestPath, harveyCheckout: checkout,
    output: packet, stressFixturePath });
  const prompts = [];
  const adapter = { metadata: () => ({ id: "mock", max_output_tokens: 300,
    final_stage_max_output_tokens: 600, s4_segment_count: 3,
    s4_segment_strategy: "memo-thirds-v1" }), invoke: async ({ prompt, max_output_tokens }) => {
    prompts.push(prompt);
    if (prompt.includes("Select only the knowledge receipts")) {
      const id = prompt.match(/knw_[a-f0-9]+/)[0];
      return { raw_output: JSON.stringify({ checklist: [{ requirement: "bound term", knowledge_ids: [id], coverage: "covered" }],
        selected_knowledge_ids: [id], rationale: "inspect bound source" }),
        telemetry: { model_calls: 1 } };
    }
    if (prompt.startsWith("You are planning the evidence-complete working set")
      || prompt.startsWith("You are the completeness gate")) {
      const id = prompt.match(/knw_[a-f0-9]+/)[0];
      return { raw_output: JSON.stringify({ checklist: [{ requirement: "bound term", knowledge_ids: [id], coverage: "covered" }],
        selected_knowledge_ids: [id], rationale: "coverage complete" }), telemetry: { model_calls: 1 } };
    }
    if (prompt.includes("Compile a concise, evidence-complete working set")) {
      const id = prompt.match(/knw_[a-f0-9]+/)[0];
      const file = prompt.match(/deal-economics-summary\.xlsx/)?.[0] ?? "deal-economics-summary.xlsx";
      return { raw_output: JSON.stringify({ requirements: [{ requirement: "bound term",
        synthesis: "Supported term", knowledge_ids: [id], evidence_files: [file] }], open_gaps: [] }),
        telemetry: { model_calls: 1 } };
    }
    const stage = prompt.match(/Current stage: (S\d)/)[1];
    if (stage === "S4") return { raw_output: `## Planned fragment ${prompts.length}`,
      telemetry: { request_id: `segment-${prompts.length}`, finish_reason: "stop",
        input_tokens: 10, output_tokens: 5, output_cap_tokens: max_output_tokens,
        output_cap_hit: false, wall_clock_latency_ms: 1, reasoning_tokens: 0,
        provider_cost_usd: 0, actual_incremental_cash_usd: null, model_calls: 1, retries: 0 } };
    return { raw_output: JSON.stringify({ stage_id: stage, summary: `summary-${stage}`,
      conclusions: stage === "S1" ? [
        { statement: "Bound conclusion", evidence_files: ["deal-economics-summary.xlsx"] },
        { statement: "Unsupported conclusion", evidence_files: ["deal-economics-summary.xlsx"] },
      ] : [],
      final_markdown: stage === "S4" ? "# Escalation memo\n\nApproved content." : "" }), telemetry: { model_calls: 1 } };
  }};
  const output = path.join(root, "run");
  const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../../..");
  const judgePrompts = [];
  const judge = { metadata: () => ({ id: "mock-judge" }), invoke: async ({ prompt }) => {
    judgePrompts.push(prompt);
    const ids = [...prompt.matchAll(/"conclusion_id":"(knw_[a-f0-9]+)"/g)].map((x) => x[1]);
    return { raw_output: JSON.stringify({ verdicts: ids.map((id, index) => ({ conclusion_id: id,
      recommendation: index === 1 ? "reject" : "accept", risk_level: "low",
      rationale: index === 1 ? "contradicted" : "explicit support" })) }), telemetry: { model_calls: 1 } };
  } };
  const prepared = await runPrepare({ packetDir: packet, output, manifest, trackId: "A_HARVEY_COMPARABLE",
    authorizeRealCalls: true, root: repoRoot, adapterOverride: adapter, judgeOverride: judge });
  assert.equal(prepared.status, "POLICY_GATE_COMPLETE");
  assert.equal(prepared.episodes.C1_ORDINARY_PORTABLE.sender_state, "SHARED_SENDER");
  assert.equal(prepared.episodes.C2_PROOFPRESS.sender_state, "SHARED_SENDER");
  assert.deepEqual(prepared.episodes.C1_ORDINARY_PORTABLE.stages, prepared.episodes.C2_PROOFPRESS.stages);
  assert.equal(prompts.filter((x) => x.includes("Current stage: S1")).length, 1);
  assert.equal(prompts.filter((x) => x.includes("Current stage: S2")).length, 1);
  assert.deepEqual(prepared.episodes.C2_PROOFPRESS.proposals.map((x) => x.admitted), [true, false, false]);
  assert.match(prepared.episodes.C1_ORDINARY_PORTABLE.raw_handoff, /Expired memory claim/);
  const stressProposal = prepared.episodes.C2_PROOFPRESS.proposals.find((x) => x.stress_fixture_id === "stress-test");
  assert.equal(stressProposal.evaluation.checks.not_expired, false);
  assert.equal(stressProposal.admitted, false);
  assert.equal(judgePrompts.length, 1);
  assert.equal(prepared.episodes.C2_PROOFPRESS.judge_transaction.conclusion_count, 3);
  assert.ok(prompts.filter((x) => x.includes("Current stage: S1")).every((x) => !x.includes("business-team-update.docx")));
  const resumed = await runResume({ output, manifest, authorizeRealCalls: true, root: repoRoot, adapterOverride: adapter });
  assert.equal(resumed.status, "READY_FOR_LAB_EVALUATION");
  const inherited = JSON.parse(await fs.readFile(path.join(output, "receiver/C2_PROOFPRESS/INHERITED_CONTEXT.json")));
  const rawInherited = JSON.parse(await fs.readFile(path.join(output, "receiver/C1_ORDINARY_PORTABLE/INHERITED_CONTEXT.json")));
  assert.equal(rawInherited.boundary_memory_artifact.id, "stress-test");
  assert.equal(inherited.proofpress_governed_working_set.requirements.length, 1);
  assert.deepEqual(inherited.proofpress_trace_expansion.selected_knowledge_ids,
    inherited.proofpress_governed_working_set.requirements[0].knowledge_ids);
  assert.equal(inherited.proofpress_trace_expansion.evidence_refs_resolved.length, 1);
  await assert.rejects(fs.access(path.join(output, "receiver/C1_ORDINARY_PORTABLE/matter/S1")));
  await assert.rejects(fs.access(path.join(output, "receiver/C2_PROOFPRESS/matter/S2")));
  assert.ok(prompts.filter((x) => x.includes("Current stage: S3") && x.includes("Condition: C1_ORDINARY_PORTABLE"))
    .every((x) => !x.includes("S1:deal-economics-summary.xlsx")));
  assert.ok(prompts.filter((x) => x.includes("Current stage: S3") && x.includes("Condition: C2_PROOFPRESS"))
    .every((x) => x.includes("Bound conclusion") && !x.includes("S1:deal-economics-summary.xlsx")));
  assert.ok(prompts.filter((x) => x.includes("Current stage: S4"))
    .every((x) => x.includes("S3:akintola-business-case-email.eml")
      && x.includes("S4:tsao-escalation-request-email.eml")));
  assert.equal(prompts.filter((x) => x.includes("Current stage: S4")).length, 6);
  for (const condition of ["C1_ORDINARY_PORTABLE", "C2_PROOFPRESS"]) {
    await fs.access(resumed.episodes[condition].deliverable);
    assert.equal(resumed.episodes[condition].stages.find((x) => x.stage_id === "S4").telemetry.model_calls, 3);
    for (const segment of [1, 2, 3])
      await fs.access(path.join(output, `receiver/${condition}/MODEL_RESPONSE_S4_SEGMENT_${segment}.json`));
  }
  const reusedOutput = path.join(root, "run-reused-sender");
  const senderPromptCount = prompts.filter((x) => /Current stage: S[12]/.test(x)).length;
  const reused = await runPrepare({ packetDir: packet, output: reusedOutput, manifest,
    trackId: "A_HARVEY_COMPARABLE", authorizeRealCalls: true, root: repoRoot,
    adapterOverride: adapter, judgeOverride: judge, sharedSenderFrom: output });
  assert.equal(reused.sender_reuse.source_run, output);
  assert.equal(reused.episodes.C2_PROOFPRESS.governance_reuse.source_run, output);
  assert.equal(reused.episodes.C2_PROOFPRESS.governance_reuse.source_judge_receipt,
    prepared.episodes.C2_PROOFPRESS.judge_transaction.receipt);
  assert.deepEqual(reused.episodes.C2_PROOFPRESS.proposals, prepared.episodes.C2_PROOFPRESS.proposals);
  assert.equal(reused.episodes.C2_PROOFPRESS.judge_transaction, undefined);
  assert.equal(judgePrompts.length, 1);
  assert.deepEqual(reused.episodes.C1_ORDINARY_PORTABLE.stages,
    resumed.episodes.C1_ORDINARY_PORTABLE.stages.filter((x) => ["S1", "S2"].includes(x.stage_id)));
  assert.equal(prompts.filter((x) => /Current stage: S[12]/.test(x)).length, senderPromptCount);
});
