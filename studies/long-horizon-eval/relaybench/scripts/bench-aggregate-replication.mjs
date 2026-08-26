#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

const args = parse(process.argv.slice(2));
const tasks = ["credit", "msa", "license"];
const arms = ["clean", "stress"];
const rows = [];

for (let repeat = 1; repeat <= 3; repeat += 1) for (const arm of arms) for (const task of tasks) {
  const run = path.join(args.root, `repeat-${repeat}`, arm, task, "run");
  const rubricPath = path.join(run, "PUBLIC_RUBRIC_SCORES.json");
  const statePath = path.join(run, "RUN_STATE.json");
  if (!await exists(rubricPath) || !await exists(statePath)) continue;
  const state = JSON.parse(await fs.readFile(statePath, "utf8"));
  const rubric = JSON.parse(await fs.readFile(rubricPath, "utf8"));
  const raw = rubric.C1_ORDINARY_PORTABLE;
  const proofpress = rubric.C2_PROOFPRESS;
  const row = {
    repeat, arm, task, run: path.relative(args.root, run),
    status: state.status,
    quality: {
      raw: { passed: raw.criteria_passed, total: raw.criteria_total, rate: raw.criterion_pass_rate },
      proofpress: { passed: proofpress.criteria_passed, total: proofpress.criteria_total,
        rate: proofpress.criterion_pass_rate },
      delta_criteria: proofpress.criteria_passed - raw.criteria_passed,
      delta_percentage_points: 100 * (proofpress.criteria_passed - raw.criteria_passed) / raw.criteria_total,
    },
    proof_price: await proofPrice(run, state),
    receipts: {
      run_state_sha256: await digest(statePath),
      public_rubric_sha256: await digest(rubricPath),
      public_rubric_evaluator: {
        raw: raw.telemetry,
        proofpress: proofpress.telemetry,
      },
    },
  };
  if (arm === "stress") {
    const trustPath = path.join(run, "TRUST_ENDPOINT_SCORES_attempt-1.json");
    if (!await exists(trustPath)) continue;
    const trust = JSON.parse(await fs.readFile(trustPath, "utf8"));
    row.receipts.trust_endpoint_sha256 = await digest(trustPath);
    row.receipts.trust_evaluator = trust.evaluator.telemetry;
    row.trust = Object.fromEntries(Object.entries(trust.results).map(([key, value]) => [key, {
      disposition: value.disposition,
      unsafe_claim_propagated: value.unsafe_claim_propagated,
      conflict_recognized: value.conflict_recognized,
      revalidation_or_escalation_preserved: value.revalidation_or_escalation_preserved,
      memo_digest: value.memo_digest,
    }]));
  }
  rows.push(row);
}

const invalidAttempts = await findInvalid(args.root);
const sharedGovernance = await sharedGovernanceSummary(rows, args.root);
const incrementalProofPrice = Object.fromEntries(arms.map((arm) =>
  [arm, priceSummary(rows.filter((x) => x.arm === arm))]));
const result = {
  schema_version: 1,
  generated_at: new Date().toISOString(),
  model: args.model,
  track: args.track,
  result_root_label: path.basename(args.root),
  frozen_protocol: "bench/experiments/cross-model-replication-v1.json",
  claim_boundary: {
    benchmark: "Public LAB Contracts tasks and public criteria; not an official Harvey private leaderboard result.",
    stress: "LAB-derived controlled handoff stress test; not an official Harvey benchmark result.",
    uncertainty: "Descriptive paired repeated-run uncertainty on a fixed task panel; not a population estimate.",
    invalid: "Invalid attempts are retained but excluded from treatment estimates.",
  },
  completion: {
    planned_pairs: 18,
    valid_pairs: rows.length,
    invalid_attempt_directories: invalidAttempts.length,
    complete: rows.length === 18,
  },
  quality: Object.fromEntries(arms.map((arm) => [arm, qualitySummary(rows.filter((x) => x.arm === arm))])),
  protection: protectionSummary(rows.filter((x) => x.arm === "stress")),
  proof_price: {
    definition: "Per-cell receiver/governance deltas plus each frozen shared governance transaction exactly once.",
    ...incrementalProofPrice,
    incremental_by_arm: incrementalProofPrice,
    shared_governance: sharedGovernance,
    full_panel: fullPanelPrice(rows, sharedGovernance),
  },
  valid_runs: rows,
  invalid_attempts: invalidAttempts,
};

const text = `${JSON.stringify(result, null, 2)}\n`;
if (args.out) await fs.writeFile(args.out, text);
else process.stdout.write(text);

async function proofPrice(run, state) {
  const c1S4 = state.episodes.C1_ORDINARY_PORTABLE.stages.find((x) => x.stage_id === "S4")?.telemetry;
  const c2S4 = state.episodes.C2_PROOFPRESS.stages.find((x) => x.stage_id === "S4")?.telemetry;
  const trace = state.episodes.C2_PROOFPRESS.trace_lookup ?? {};
  const extras = [state.episodes.C2_PROOFPRESS.judge_transaction?.telemetry, trace.telemetry,
    trace.compiler_telemetry, trace.completeness_telemetry];
  const sender = path.join(run, "sender", "SHARED_SENDER");
  if (await exists(sender)) for (const name of await fs.readdir(sender)) {
    if (!/^JUDGE_REVIEW_.*\.json$/.test(name)) continue;
    const value = JSON.parse(await fs.readFile(path.join(sender, name), "utf8"));
    extras.push(value.telemetry);
  }
  const c2Calls = uniqueTelemetry([c2S4, ...extras]);
  const c1Calls = uniqueTelemetry([c1S4]);
  const c2 = sumTelemetry(c2Calls);
  const c1 = sumTelemetry(c1Calls);
  return {
    definition: "Proofpress receiver-side calls minus ordinary S4 receiver; shared S1-S3 sender and evaluators excluded",
    raw_receiver: c1,
    proofpress_receiver_and_governance: c2,
    delta: subtractTelemetry(c2, c1),
    request_ids: { raw: c1Calls.map((x) => x.request_id),
      proofpress: c2Calls.map((x) => x.request_id) },
  };
}

async function sharedGovernanceSummary(rows, root) {
  const sources = new Map();
  for (const row of rows) {
    const statePath = path.join(root, row.run, "RUN_STATE.json");
    const state = JSON.parse(await fs.readFile(statePath, "utf8"));
    const sourceRun = state.episodes.C2_PROOFPRESS.governance_reuse?.source_run;
    if (!sourceRun) continue;
    const resolved = path.resolve(sourceRun);
    if (!sources.has(resolved)) sources.set(resolved, { tasks: new Set(), cells: 0 });
    sources.get(resolved).tasks.add(row.task);
    sources.get(resolved).cells += 1;
  }
  const details = [];
  for (const [sourceRun, usage] of sources) {
    const statePath = path.join(sourceRun, "RUN_STATE.json");
    if (!await exists(statePath)) throw new Error(`missing shared governance state ${statePath}`);
    const state = JSON.parse(await fs.readFile(statePath, "utf8"));
    const telemetry = [state.episodes.C2_PROOFPRESS.judge_transaction?.telemetry];
    const sender = path.join(sourceRun, "sender", "SHARED_SENDER");
    if (await exists(sender)) for (const name of await fs.readdir(sender)) {
      if (!/^JUDGE_REVIEW_.*\.json$/.test(name)) continue;
      const value = JSON.parse(await fs.readFile(path.join(sender, name), "utf8"));
      telemetry.push(value.telemetry);
    }
    const calls = uniqueTelemetry(telemetry);
    details.push({
      source_run: path.relative(root, sourceRun),
      tasks: [...usage.tasks].sort(),
      reused_by_valid_cells: usage.cells,
      resources: sumTelemetry(calls),
      request_ids: calls.map((x) => x.request_id),
      run_state_sha256: await digest(statePath),
    });
  }
  const resources = sumTelemetry(details.map((x) => x.resources));
  return {
    source_transactions: details.length,
    resources,
    details: details.sort((a, b) => a.source_run.localeCompare(b.source_run)),
  };
}

function fullPanelPrice(rows, sharedGovernance) {
  const incremental = sumTelemetry(rows.map((x) => x.proof_price.delta));
  return {
    valid_pairs: rows.length,
    incremental,
    shared_governance: sharedGovernance.resources,
    all_in: addTelemetry(incremental, sharedGovernance.resources),
  };
}

function qualitySummary(items) {
  const byTask = Object.fromEntries(tasks.map((task) => [task, summarizeQuality(items.filter((x) => x.task === task))]));
  return { ...summarizeQuality(items), by_task: byTask };
}
function summarizeQuality(items) {
  if (!items.length) return { pairs: 0, estimate_available: false };
  const rawPassed = sum(items.map((x) => x.quality.raw.passed));
  const proofpressPassed = sum(items.map((x) => x.quality.proofpress.passed));
  const total = sum(items.map((x) => x.quality.raw.total));
  const deltas = items.map((x) => x.quality.delta_percentage_points);
  return {
    pairs: items.length,
    estimate_available: true,
    raw: { passed: rawPassed, total, rate: rawPassed / total },
    proofpress: { passed: proofpressPassed, total, rate: proofpressPassed / total },
    weighted_delta_criteria: proofpressPassed - rawPassed,
    weighted_delta_percentage_points: 100 * (proofpressPassed - rawPassed) / total,
    paired_delta_percentage_points: { values: deltas, ...meanTInterval(deltas) },
  };
}
function protectionSummary(items) {
  if (!items.length) return { pairs: 0, estimate_available: false };
  const pairs = items.map((x) => ({ repeat: x.repeat, task: x.task,
    raw_unsafe: x.trust.C1_ORDINARY_PORTABLE.unsafe_claim_propagated,
    proofpress_unsafe: x.trust.C2_PROOFPRESS.unsafe_claim_propagated }));
  const rawUnsafe = pairs.filter((x) => x.raw_unsafe).length;
  const proofpressUnsafe = pairs.filter((x) => x.proofpress_unsafe).length;
  const protectedOnly = pairs.filter((x) => x.raw_unsafe && !x.proofpress_unsafe).length;
  const harmedOnly = pairs.filter((x) => !x.raw_unsafe && x.proofpress_unsafe).length;
  return { pairs: pairs.length, estimate_available: true, raw_unsafe: rawUnsafe,
    proofpress_unsafe: proofpressUnsafe,
    observed_effect_percentage_points: 100 * (rawUnsafe - proofpressUnsafe) / pairs.length,
    discordant: { protected_only: protectedOnly, harmed_only: harmedOnly,
      exact_two_sided_mcnemar_p: exactBinomialTwoSided(Math.min(protectedOnly, harmedOnly), protectedOnly + harmedOnly) },
    by_task: Object.fromEntries(tasks.map((task) => {
      const group = pairs.filter((x) => x.task === task);
      return [task, { pairs: group.length, raw_unsafe: group.filter((x) => x.raw_unsafe).length,
        proofpress_unsafe: group.filter((x) => x.proofpress_unsafe).length }];
    })), details: pairs };
}
function priceSummary(items) {
  if (!items.length) return { pairs: 0, estimate_available: false };
  const keys = ["model_calls", "input_tokens", "output_tokens", "reasoning_tokens", "total_tokens",
    "provider_cost_usd", "wall_clock_latency_ms"];
  return { pairs: items.length, estimate_available: true,
    delta: Object.fromEntries(keys.map((key) => {
      const values = items.map((x) => x.proof_price.delta[key]);
      return [key, { total: sum(values), mean: mean(values), median: median(values), values }];
    })) };
}

function uniqueTelemetry(values) {
  const seen = new Set();
  return values.filter(Boolean).filter((value) => {
    const key = value.request_id ?? JSON.stringify(value);
    if (seen.has(key)) return false;
    seen.add(key); return true;
  });
}
function sumTelemetry(values) {
  const out = { model_calls: 0, input_tokens: 0, output_tokens: 0, reasoning_tokens: 0,
    total_tokens: 0, provider_cost_usd: 0, wall_clock_latency_ms: 0 };
  for (const value of values) {
    out.model_calls += value.model_calls ?? 1;
    out.input_tokens += value.input_tokens ?? 0;
    out.output_tokens += value.output_tokens ?? 0;
    out.reasoning_tokens += value.reasoning_tokens ?? 0;
    out.provider_cost_usd += value.provider_cost_usd ?? 0;
    out.wall_clock_latency_ms += value.wall_clock_latency_ms ?? 0;
  }
  out.total_tokens = out.input_tokens + out.output_tokens;
  return out;
}
function subtractTelemetry(a, b) {
  return Object.fromEntries(Object.keys(a).map((key) => [key, a[key] - b[key]]));
}
function addTelemetry(a, b) {
  return Object.fromEntries(Object.keys(a).map((key) => [key, a[key] + (b[key] ?? 0)]));
}
function meanTInterval(values) {
  if (values.length < 2) return { mean: mean(values), interval_available: false,
    reason: "at least two valid pairs are required" };
  const center = mean(values);
  const variance = sum(values.map((x) => (x - center) ** 2)) / (values.length - 1);
  const standardError = Math.sqrt(variance / values.length);
  const critical = ({ 2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571,
    7: 2.447, 8: 2.365, 9: 2.306 })[values.length] ?? 1.96;
  return { mean: center, interval_available: true, sample_standard_deviation: Math.sqrt(variance),
    standard_error: standardError, lower_95: center - critical * standardError,
    upper_95: center + critical * standardError,
    method: `paired t interval, df=${values.length - 1}` };
}
function exactBinomialTwoSided(k, n) {
  if (n === 0) return 1;
  let tail = 0; for (let i = 0; i <= k; i += 1) tail += choose(n, i) * 0.5 ** n;
  return Math.min(1, 2 * tail);
}
function choose(n, k) { let out = 1; for (let i = 1; i <= k; i += 1) out = out * (n - k + i) / i; return out; }
function mean(xs) { return sum(xs) / xs.length; }
function median(xs) { const s = [...xs].sort((a, b) => a - b); return s.length % 2
  ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2; }
function sum(xs) { return xs.reduce((a, b) => a + b, 0); }
async function findInvalid(root) {
  const out = [];
  async function walk(dir) {
    if (!await exists(dir)) return;
    for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue;
      const child = path.join(dir, entry.name);
      if (entry.name.startsWith("run-invalid-")) out.push({ path: path.relative(root, child),
        reason_slug: entry.name.slice("run-invalid-".length) });
      else await walk(child);
    }
  }
  await walk(root);
  return out.sort((a, b) => a.path.localeCompare(b.path));
}
async function exists(file) { try { await fs.access(file); return true; } catch { return false; } }
async function digest(file) { return `sha256:${crypto.createHash("sha256").update(await fs.readFile(file)).digest("hex")}`; }
function parse(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i]; const value = argv[++i];
    if (key === "--root") out.root = path.resolve(value);
    else if (key === "--model") out.model = value;
    else if (key === "--track") out.track = value;
    else if (key === "--out") out.out = path.resolve(value);
    else throw new Error(`unknown argument ${key}`);
  }
  for (const key of ["root", "model", "track"]) if (!out[key]) throw new Error(`missing --${key}`);
  return out;
}
