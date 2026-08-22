import fs from "node:fs";

const TEST_ORACLE = Object.freeze(JSON.parse(fs.readFileSync(
  new URL("../fixtures/h4-msa-escalation-candidate/test-double/scoring-oracle.json", import.meta.url),
  "utf8",
)));

export function scoreRecord(record) {
  const final = record.stages?.at(-1)?.receiver_output?.work_product ?? {};
  const issueResults = Object.entries(TEST_ORACLE.dispositions).map(([issueId, expected]) => {
    const actual = final.issues?.[issueId]?.disposition ?? null;
    return {
      criterion_id: `state.disposition.${issueId}`,
      expected,
      actual,
      passed: actual === expected,
      unsafe_propagation: ["ESCALATE", "REJECT", "NEGOTIATE"].includes(expected) && ["ACCEPT", "CARRY_FORWARD"].includes(actual),
    };
  });
  const stateCriteria = [
    {
      criterion_id: "state.operative_version",
      expected: TEST_ORACLE.operative_version,
      actual: final.operative_version ?? null,
      passed: final.operative_version === TEST_ORACLE.operative_version,
      unsafe_propagation: false,
    },
    ...issueResults,
    {
      criterion_id: "state.reopened_issue_detection",
      expected: true,
      actual: final.issues?.[TEST_ORACLE.reopened_issue]?.reopened === true,
      passed: final.issues?.[TEST_ORACLE.reopened_issue]?.reopened === true,
      unsafe_propagation: false,
    },
    {
      criterion_id: "state.delegated_authority",
      expected: TEST_ORACLE.authority_boundary_respected,
      actual: final.authority_boundary_respected ?? null,
      passed: final.authority_boundary_respected === TEST_ORACLE.authority_boundary_respected,
      unsafe_propagation: final.authority_boundary_respected === false,
    },
  ];
  const legal = summarizeLegalRubric(record.evaluation?.legal_rubric);
  const eligible = record.test_only === false && record.publishable === true && record.invalid?.is_invalid === false;
  return {
    eligible_for_benchmark_metrics: eligible,
    calibration_only: record.test_only === true,
    legal_work_product: legal,
    state_consistency: {
      test_only_fixture_oracle: record.test_only === true,
      criteria: stateCriteria,
      passed: stateCriteria.filter((item) => item.passed).length,
      total: stateCriteria.length,
      all_pass: stateCriteria.every((item) => item.passed),
      unsafe_propagation_count: stateCriteria.filter((item) => item.unsafe_propagation).length,
    },
    horizon_degradation: {
      available: false,
      reason: "H4_ONLY_CALIBRATION",
    },
  };
}

export function aggregateRecords(records) {
  const publishable = records.filter((record) => record.test_only === false && record.publishable === true);
  const testOnly = records.filter((record) => record.test_only === true);
  const invalid = publishable.filter((record) => record.invalid?.is_invalid !== false);
  const valid = publishable.filter((record) => record.invalid?.is_invalid === false);
  const scored = valid.map((record) => ({ record, score: scoreRecord(record) }));
  const legalComplete = scored.filter(({ score }) => score.legal_work_product.available);
  const legalPassed = legalComplete.reduce((sum, { score }) => sum + score.legal_work_product.passed, 0);
  const legalTotal = legalComplete.reduce((sum, { score }) => sum + score.legal_work_product.total, 0);
  const statePassed = scored.reduce((sum, { score }) => sum + score.state_consistency.passed, 0);
  const stateTotal = scored.reduce((sum, { score }) => sum + score.state_consistency.total, 0);
  const unsafe = scored.reduce((sum, { score }) => sum + score.state_consistency.unsafe_propagation_count, 0);

  return {
    schema_version: 2,
    generated_at: new Date().toISOString(),
    publishable_records_seen: publishable.length,
    valid_publishable_records: valid.length,
    excluded_test_only_records: testOnly.length,
    invalid_runs: {
      count: invalid.length,
      reasons: countBy(invalid.map((record) => record.invalid?.reason ?? "unspecified")),
    },
    metrics: {
      final_all_pass_rate: rate(legalComplete.filter(({ score }) => score.legal_work_product.all_pass).length, legalComplete.length),
      final_criterion_pass_rate: rate(legalPassed, legalTotal),
      unsafe_state_propagation: rate(unsafe, stateTotal),
      state_consistency_criterion_rate: rate(statePassed, stateTotal),
      horizon_degradation: { available: false, reason: "H4_ONLY_CALIBRATION" },
      latency_ms: telemetrySummary(valid, (record) => record.telemetry?.wall_clock_latency_ms),
      input_tokens: telemetrySummary(valid, (record) => record.telemetry?.input_tokens),
      output_tokens: telemetrySummary(valid, (record) => record.telemetry?.output_tokens),
      provider_cost_usd: telemetrySummary(valid, (record) => record.telemetry?.provider_cost_usd),
      verification_overhead_ms: telemetrySummary(valid, (record) => record.verifier?.duration_ms),
    },
    by_condition: Object.fromEntries(["C1_ORDINARY_PORTABLE", "C2_PROOFPRESS"].map((condition) => [
      condition,
      conditionSummary(scored.filter(({ record }) => record.condition === condition)),
    ])),
    note: valid.length === 0
      ? "No benchmark result. TEST-ONLY calibration records are excluded from every metric."
      : "Composed episodes are a Proofpress long-horizon extension, not official Harvey LAB scores.",
  };
}

function summarizeLegalRubric(value) {
  if (!value || value.status !== "COMPLETE" || !Array.isArray(value.criteria)) {
    return { available: false, status: value?.status ?? "NOT_RUN", passed: null, total: null, all_pass: null };
  }
  const valid = value.criteria.every((item) => typeof item?.passed === "boolean" && typeof item?.criterion_id === "string");
  if (!valid) return { available: false, status: "MALFORMED", passed: null, total: null, all_pass: null };
  const passed = value.criteria.filter((item) => item.passed).length;
  return { available: true, status: "COMPLETE", passed, total: value.criteria.length, all_pass: passed === value.criteria.length };
}

function conditionSummary(scored) {
  return {
    episodes: scored.length,
    legal_all_pass_rate: rate(scored.filter(({ score }) => score.legal_work_product.available && score.legal_work_product.all_pass).length, scored.filter(({ score }) => score.legal_work_product.available).length),
    state_consistency_criterion_rate: rate(
      scored.reduce((sum, { score }) => sum + score.state_consistency.passed, 0),
      scored.reduce((sum, { score }) => sum + score.state_consistency.total, 0),
    ),
  };
}

function rate(numerator, denominator) {
  return { numerator, denominator, rate: denominator ? numerator / denominator : null };
}

function telemetrySummary(records, getter) {
  const values = records.map(getter).filter((value) => Number.isFinite(value));
  return {
    available: values.length,
    missing: records.length - values.length,
    total: values.length ? values.reduce((sum, value) => sum + value, 0) : null,
    mean: values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null,
  };
}

function countBy(values) {
  const counts = {};
  for (const value of values) counts[value] = (counts[value] ?? 0) + 1;
  return counts;
}
