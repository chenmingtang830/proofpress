#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";

const output = path.resolve(process.argv[2] ?? "results/cross-model-ladder-summary-2026-08-26.json");
const inputs = [
  { id: "deepseek_anchor", files: ["results/deepseek-v9-s4-2x2-results-2026-08-24.json"] },
  { id: "opus48_gateway", files: ["results/opus48-gateway-v9-replication-2026-08-25.json"] },
  { id: "glm52", files: ["results/glm52-gateway-v10-replication-2026-08-26.json"] },
  { id: "muse_spark11", files: ["results/muse-spark11-gateway-v10-replication-2026-08-26.json"] },
  { id: "qwen38_27b", files: [
    "results/qwen38-27b-gateway-v10-replication-2026-08-26.json",
    "results/qwen38-27b-gateway-v9-replication-2026-08-25.json",
  ] },
  { id: "inkling", files: ["results/inkling-gateway-v10-replication-2026-08-26.json"] },
  { id: "gpt56_sol", files: [
    "results/gpt56-sol-gateway-v10-replication-2026-08-26.json",
    "results/gpt56-sol-gateway-v9-frontier-confirmation-2026-08-25.json",
  ] },
];
const tracks = [];
for (const { id, files } of inputs) {
  const file = await firstExisting(files);
  const result = JSON.parse(await fs.readFile(file, "utf8"));
  const completion = result.completion ?? {};
  // The original DeepSeek anchor predates the replication-result envelope.
  // Normalize its explicit clean/stress fields rather than silently dropping it.
  const clean = result.quality?.clean ?? result.clean_quality ?? null;
  const stress = result.quality?.stress ?? result.stress_quality ?? null;
  const complete = completion.complete === true || (id === "deepseek_anchor" && clean?.pairs === 9 && stress?.pairs === 9);
  const normalizedCompletion = id === "deepseek_anchor" ? {
    planned_pairs: 18,
    valid_pairs: (clean?.pairs ?? 0) + (stress?.pairs ?? 0),
    invalid_attempt_directories: result.invalid_attempts?.length ?? 0,
    complete,
  } : completion;
  tracks.push({ id, model: result.model ?? (id === "deepseek_anchor" ? "deepseek/deepseek-v4-flash-0731" : null),
    evidence_tier: complete ? "complete_frozen_panel" : (normalizedCompletion.valid_pairs > 0 ? "incomplete_descriptive_only" : "route_unavailable"),
    completion: normalizedCompletion,
    clean: clean ? quality(clean) : null,
    stress: stress ? quality(stress) : null,
    protection: result.protection ? { pairs: result.protection.pairs,
      raw_unsafe: result.protection.raw_unsafe ?? result.protection.ordinary_unsafe,
      proofpress_unsafe: result.protection.proofpress_unsafe,
      observed_effect_percentage_points: result.protection.observed_effect_percentage_points
        ?? result.protection.observed_protection_effect_percentage_points } : null,
    source: file });
}
const kimiTerminationFile = "bench/experiments/kimi-termination-v1.json";
const kimiTermination = JSON.parse(await fs.readFile(kimiTerminationFile, "utf8"));
tracks.splice(2, 0, {
  id: "kimi_k3",
  model: kimiTermination.model,
  evidence_tier: "user_terminated_unavailable",
  completion: {
    planned_pairs: 18,
    valid_pairs: 0,
    invalid_attempt_directories: kimiTermination.preserved_evidence.v10_invalid_attempts
      + kimiTermination.preserved_evidence.v11_invalid_attempts,
    complete: false,
    disposition: kimiTermination.result_disposition.three_task_replication_estimate,
  },
  clean: null,
  stress: null,
  protection: null,
  source: kimiTerminationFile,
});
const summary = {
  schema_version: 1,
  generated_at: new Date().toISOString(),
  claim_boundary: "Only complete_frozen_panel tracks support panel treatment estimates. Incomplete valid cells are descriptive route signals. User-terminated and route-unavailable tracks do not imply zero effect.",
  complete_panel_count: tracks.filter((track) => track.evidence_tier === "complete_frozen_panel").length,
  tracks,
  optional_track_decision: "GPT-5.6 Luna and Grok 4.6 were not run; the completed Sol panel closes the predeclared frontier-confirmation scope without adding an outcome-selected scaling track."
};
await fs.writeFile(output, `${JSON.stringify(summary, null, 2)}\n`);
process.stdout.write(`${JSON.stringify(summary, null, 2)}\n`);

function quality(value) { return { pairs: value.pairs, raw: value.raw ?? null,
  proofpress: value.proofpress ?? null, weighted_delta_criteria: value.weighted_delta_criteria ?? null,
  weighted_delta_percentage_points: value.weighted_delta_percentage_points ?? null,
  paired_delta_percentage_points: value.paired_delta_percentage_points ?? null }; }

async function firstExisting(files) {
  for (const file of files) {
    try {
      await fs.access(file);
      return file;
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
  }
  throw new Error(`No result artifact exists for candidates: ${files.join(", ")}`);
}
