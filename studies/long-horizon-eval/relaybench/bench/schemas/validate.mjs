const REQUIRED_PATHS = Object.freeze([
  "run_id",
  "invocation_id",
  "condition",
  "horizon",
  "stress_track",
  "matter.candidate_id",
  "stages",
  "stage_controller.complete",
  "workspace_boundaries",
  "information_parity.passed",
  "transferred_file_manifest",
  "verifier.commands",
  "evaluation.legal_rubric.status",
  "deterministic_score.eligible_for_benchmark_metrics",
  "timestamps.episode_completed_at",
  "model.provider",
  "model.route",
  "model.resolved_model",
  "telemetry.wall_clock_latency_ms",
  "telemetry.input_tokens",
  "telemetry.output_tokens",
  "telemetry.provider_cost_usd",
  "invalid.is_invalid",
]);

export function validateRunRecord(record) {
  const errors = [];
  if (record?.record_type !== "h4_calibration_episode") errors.push("record_type must be h4_calibration_episode");
  if (record?.schema_version !== 2) errors.push("schema_version must be 2");
  for (const required of REQUIRED_PATHS) {
    if (!hasPath(record, required)) errors.push(`missing required field: ${required}`);
  }
  if (!['C1_ORDINARY_PORTABLE', 'C2_PROOFPRESS'].includes(record?.condition)) errors.push("unknown condition");
  if (record?.horizon !== "H4" || record?.stress_track !== "EVOLVING_NEGOTIATION_STATE") errors.push("scope must be H4 evolving negotiation state");
  if (record?.test_only !== true || record?.publishable !== false) errors.push("calibration record must be TEST-ONLY and non-publishable");
  if (!Array.isArray(record?.stages) || record.stages.length !== 4) errors.push("episode must contain exactly four stages");
  if (record?.stages?.map((stage) => stage.stage_id).join(",") !== "S1,S2,S3,S4") errors.push("stage order must be S1,S2,S3,S4");
  if (!Array.isArray(record?.workspace_boundaries) || record.workspace_boundaries.length !== 1 || record.workspace_boundaries[0]?.valid !== true) errors.push("episode requires exactly one valid cold boundary");
  if (record?.information_parity?.passed !== true) errors.push("information parity must pass");
  if (record?.condition === "C2_PROOFPRESS" && (record?.verifier?.required !== true || record?.verifier?.status !== "ok" || !record.verifier.commands.length)) errors.push("C2 requires ok verifier evidence before receiver action");
  if (record?.condition === "C1_ORDINARY_PORTABLE" && (record?.verifier?.required !== false || record.verifier.commands.length !== 0)) errors.push("C1 cannot invent verifier evidence");
  if (record?.deterministic_score?.eligible_for_benchmark_metrics !== false) errors.push("TEST-ONLY calibration cannot be metric-eligible");
  if (record?.invalid?.is_invalid === true && !record.invalid.reason) errors.push("invalid record requires a reason");
  if (record?.invalid?.is_invalid === false && record.invalid.reason !== null) errors.push("valid record reason must be null");
  return { valid: errors.length === 0, errors };
}

function hasPath(value, dotted) {
  let current = value;
  for (const segment of dotted.split(".")) {
    if (current === null || typeof current !== "object" || !(segment in current)) return false;
    current = current[segment];
  }
  return true;
}
