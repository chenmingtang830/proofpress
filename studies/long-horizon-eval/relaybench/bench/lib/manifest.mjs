import path from "node:path";
import { PROJECT_ROOT, readJson, sha256File } from "./core.mjs";

export async function loadManifest(manifestPath = path.join(PROJECT_ROOT, "BENCHMARK_MANIFEST.json")) {
  return readJson(path.resolve(manifestPath));
}

export async function verifyFrozenFiles(manifest) {
  const mismatches = [];
  for (const item of manifest.frozen_files ?? []) {
    const absolute = path.join(PROJECT_ROOT, item.path);
    let actual = null;
    try {
      actual = await sha256File(absolute);
    } catch (error) {
      mismatches.push({ path: item.path, expected: item.sha256, actual: null, error: error.message });
      continue;
    }
    if (actual !== item.sha256) mismatches.push({ path: item.path, expected: item.sha256, actual });
  }
  return { valid: mismatches.length === 0, mismatches };
}

export function realRunBlockers(manifest) {
  const blockers = (manifest.freeze_status?.decision_register ?? [])
    .filter((item) => item.status !== "RESOLVED")
    .map((item) => item.id);
  if (manifest.freeze_status?.scientific_freeze_approved !== true) blockers.push("scientific_freeze_not_approved");
  if (manifest.freeze_status?.real_run_ready !== true) blockers.push("real_run_ready_false");
  if (!manifest.harvey_lab?.runtime_checkout) blockers.push("harvey_lab.runtime_checkout");
  if (!manifest.upstream_proofpress?.formal_runtime_checkout) blockers.push("upstream_proofpress.formal_runtime_checkout");
  for (const field of ["provider", "route", "resolved_model", "reasoning_effort"]) {
    if (!manifest.model?.[field]) blockers.push(`model.${field}`);
  }
  if (manifest.model?.temperature?.supported === null) blockers.push("model.temperature.supported");
  if (manifest.model?.seed?.supported === null) blockers.push("model.seed.supported");
  if (manifest.model?.provider_fallback !== false) blockers.push("model.provider_fallback_must_be_false");
  if (manifest.model?.cross_provider_retries !== false) blockers.push("model.cross_provider_retries_must_be_false");
  if (!Number.isInteger(manifest.execution?.timeout_ms) || manifest.execution.timeout_ms < 1) blockers.push("execution.timeout_ms");
  if (!Number.isInteger(manifest.execution?.max_attempts) || manifest.execution.max_attempts < 1) blockers.push("execution.max_attempts");
  if (!Number.isInteger(manifest.run_plan?.real_repeats) || manifest.run_plan.real_repeats < 1) blockers.push("run_plan.real_repeats");
  return [...new Set(blockers)].sort();
}

export function assertAdapterMetadataFrozen(manifest, metadata) {
  const expected = {
    provider: manifest.model.provider,
    route: manifest.model.route,
    resolved_model: manifest.model.resolved_model,
    reasoning_effort: manifest.model.reasoning_effort,
    temperature: manifest.model.temperature,
    seed: manifest.model.seed,
    provider_fallback: false,
    cross_provider_retries: false,
  };
  const mismatches = Object.keys(expected).filter((field) => JSON.stringify(metadata[field]) !== JSON.stringify(expected[field]));
  if (mismatches.length) throw new Error(`Adapter metadata differs from frozen manifest: ${mismatches.join(", ")}`);
}
