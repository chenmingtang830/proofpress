#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const run = path.resolve(process.argv[2] ?? "");
if (!process.argv[2]) throw new Error("usage: bench-summarize-real-run.mjs RUN_DIR");
const state = JSON.parse(await fs.readFile(path.join(run, "RUN_STATE.json")));
const packet = JSON.parse(await fs.readFile(path.join(state.packet_dir, "RUN_PACKET.json")));
const scores = JSON.parse(await fs.readFile(path.join(run, "PUBLIC_RUBRIC_SCORES.json")));

const boundaryIndex = packet.stages.findIndex((x) => x.stage_id === packet.cold_boundary_before);
if (boundaryIndex < 0) throw new Error(`cold boundary ${packet.cold_boundary_before} is not in packet stages`);
const sharedStageIds = new Set(packet.stages.slice(0, boundaryIndex).map((x) => x.stage_id));
const receiverStageIds = new Set(packet.stages.slice(boundaryIndex).map((x) => x.stage_id));
const shared = state.episodes.C1_ORDINARY_PORTABLE.stages.filter((x) => sharedStageIds.has(x.stage_id))
  .map((x) => x.telemetry);
const raw = state.episodes.C1_ORDINARY_PORTABLE.stages.filter((x) => receiverStageIds.has(x.stage_id))
  .map((x) => x.telemetry);
const proofpressEpisode = state.episodes.C2_PROOFPRESS;
const proofpress = proofpressEpisode.stages.filter((x) => receiverStageIds.has(x.stage_id)).map((x) => x.telemetry);
for (const telemetry of [proofpressEpisode.judge_transaction?.telemetry,
  ...proofpressEpisode.proposals.map((x) => x.individual_review?.telemetry),
  proofpressEpisode.trace_lookup?.telemetry, proofpressEpisode.trace_lookup?.compiler_telemetry,
  proofpressEpisode.completeness?.telemetry, proofpressEpisode.completeness?.compiler_telemetry])
  if (telemetry) proofpress.push(telemetry);

const c1 = scores.C1_ORDINARY_PORTABLE; const c2 = scores.C2_PROOFPRESS;
const rawResources = resources(raw); const proofpressResources = resources(proofpress);
const result = {
  schema_version: 1,
  run,
  classification: packet.study_arm,
  official_harvey_result: false,
  task_id: packet.harvey.task_id,
  track_id: state.track_id,
  sender_reuse: state.sender_reuse,
  cold_boundary_before: packet.cold_boundary_before,
  stage_partition: { shared_sender: [...sharedStageIds], receiver: [...receiverStageIds] },
  public_rubric: {
    evaluator_claim_boundary: "frozen public-rubric evaluator; not an official Harvey private leaderboard score",
    raw: { passed: c1.criteria_passed, total: c1.criteria_total,
      rate: c1.criteria_passed / c1.criteria_total },
    proofpress: { passed: c2.criteria_passed, total: c2.criteria_total,
      rate: c2.criteria_passed / c2.criteria_total },
    paired_delta_criteria: c2.criteria_passed - c1.criteria_passed,
    paired_delta_percentage_points: 100 * (c2.criteria_passed - c1.criteria_passed) / c1.criteria_total,
  },
  shared_sender_resources: resources(shared),
  receiver_resources: {
    raw: rawResources,
    proofpress: proofpressResources,
    proof_price: subtract(proofpressResources, rawResources),
  },
  output_bytes: {
    raw: (await fs.stat(path.join(run, "receiver/C1_ORDINARY_PORTABLE/escalation-approval-memo.md"))).size,
    proofpress: (await fs.stat(path.join(run, "receiver/C2_PROOFPRESS/escalation-approval-memo.md"))).size,
  },
  governance: {
    proposed: proofpressEpisode.proposals.length,
    admitted: proofpressEpisode.proposals.filter((x) => x.admitted).length,
    blocked: proofpressEpisode.proposals.filter((x) => !x.admitted).length,
    batch_judge_calls: proofpressEpisode.judge_transaction ? 1 : 0,
    individual_re_reviews: proofpressEpisode.proposals.filter((x) => x.individual_review).length,
  },
  graph_retrieval: {
    initial_knowledge_receipts: proofpressEpisode.trace_lookup?.knowledge_ids?.length ?? null,
    initial_evidence_files: proofpressEpisode.trace_lookup?.evidence_files?.length ?? null,
    supplemental_knowledge_receipts: proofpressEpisode.completeness?.selected_knowledge_ids?.length ?? null,
    supplemental_evidence_files: proofpressEpisode.completeness?.evidence_files?.length ?? null,
  },
};
process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);

function resources(rows) {
  const unique = new Map();
  for (const row of rows.filter(Boolean)) unique.set(row.request_id ?? `missing-${unique.size}`, row);
  const values = [...unique.values()];
  return { model_calls: values.reduce((n, x) => n + (x.model_calls ?? 1), 0),
    input_tokens: values.reduce((n, x) => n + (x.input_tokens ?? 0), 0),
    cached_input_tokens: values.reduce((n, x) => n + (x.cached_input_tokens ?? 0), 0),
    output_tokens: values.reduce((n, x) => n + (x.output_tokens ?? 0), 0),
    reasoning_tokens: values.reduce((n, x) => n + (x.reasoning_tokens ?? 0), 0),
    total_tokens: values.reduce((n, x) => n + (x.input_tokens ?? 0) + (x.output_tokens ?? 0), 0),
    provider_cost_usd: values.reduce((n, x) => n + (x.provider_cost_usd ?? 0), 0),
    sequential_model_latency_ms: values.reduce((n, x) => n + (x.wall_clock_latency_ms ?? 0), 0),
    retries: values.reduce((n, x) => n + (x.retries ?? 0), 0),
    request_ids: values.map((x) => x.request_id ?? null) };
}
function subtract(a, b) {
  return Object.fromEntries(["model_calls", "input_tokens", "cached_input_tokens", "output_tokens",
    "reasoning_tokens", "total_tokens", "provider_cost_usd", "sequential_model_latency_ms", "retries"]
    .map((key) => [key, a[key] - b[key]]));
}
