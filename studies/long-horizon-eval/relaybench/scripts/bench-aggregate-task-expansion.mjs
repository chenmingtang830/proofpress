#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

const args = parse(process.argv.slice(2));
const protocol = JSON.parse(await fs.readFile(args.protocol, "utf8"));
const rows = [];
const invalid = [];
for (const item of protocol.scenarios) {
  const slug = `${item.family}-${item.scenario}`;
  const taskRoot = path.join(args.root, slug);
  const run = path.join(taskRoot, "run");
  const scorePath = path.join(run, "PUBLIC_RUBRIC_SCORES.json");
  const statePath = path.join(run, "RUN_STATE.json");
  if (await exists(scorePath) && await exists(statePath)) {
    const scores = JSON.parse(await fs.readFile(scorePath, "utf8"));
    const state = JSON.parse(await fs.readFile(statePath, "utf8"));
    const raw = scores.C1_ORDINARY_PORTABLE;
    const proofpress = scores.C2_PROOFPRESS;
    rows.push({ family: item.family, scenario: item.scenario, task_id: item.task_id,
      title: item.title, criteria: item.criteria, run: `${slug}/run`,
      quality: {
        raw: metric(raw), proofpress: metric(proofpress),
        delta_criteria: proofpress.criteria_passed - raw.criteria_passed,
        delta_percentage_points: 100 * (proofpress.criteria_passed - raw.criteria_passed) / raw.criteria_total,
        raw_floor_below_25_percent: raw.criterion_pass_rate < 0.25,
      },
      proof_price: proofPrice(state),
      cap_utilization: capUtilization(state),
      receipts: { run_state_sha256: await digest(statePath), public_rubric_sha256: await digest(scorePath),
        evaluator: { raw: raw.telemetry, proofpress: proofpress.telemetry } },
    });
  }
  for (const entry of await fs.readdir(taskRoot, { withFileTypes: true })) {
    if (!entry.isDirectory() || !entry.name.startsWith("run-invalid-")) continue;
    const dir = path.join(taskRoot, entry.name);
    const markers = (await fs.readdir(dir)).filter((name) => /^INVALID_ATTEMPT_.*\.json$/.test(name));
    const details = [];
    for (const marker of markers) {
      const value = JSON.parse(await fs.readFile(path.join(dir, marker), "utf8"));
      details.push({ marker, phase: value.phase, error: value.error?.message ?? null });
    }
    invalid.push({ family: item.family, scenario: item.scenario, path: `${slug}/${entry.name}`, details });
  }
}

const families = [...new Set(protocol.scenarios.map((item) => item.family))];
const result = {
  schema_version: 1,
  generated_at: new Date().toISOString(),
  model: protocol.model.resolved_model,
  provider_only: protocol.model.provider_only,
  frozen_protocol: path.relative(process.cwd(), args.protocol),
  claim_boundary: {
    benchmark: "Public LAB Contracts tasks and public criteria; not an official Harvey private leaderboard result.",
    design: "One clean paired run per frozen scenario. This is a task-breadth estimate, not receiver-repeat uncertainty.",
    floor: "Raw pass rates below 25% are flagged descriptively and retained; the threshold was not a preregistered exclusion rule.",
    invalid: "Provider/model invalid task attempts are excluded from quality estimates; harness/setup attempts remain visible separately.",
  },
  completion: { planned_tasks: protocol.scenarios.length, valid_tasks: rows.length,
    invalid_task_count: protocol.scenarios.filter((item) => !rows.some((row) => row.task_id === item.task_id)).length,
    valid_task_rate: rows.length / protocol.scenarios.length, all_tasks_observed: rows.length === protocol.scenarios.length },
  quality: {
    overall: summarize(rows),
    non_floor_sensitivity: summarize(rows.filter((row) => !row.quality.raw_floor_below_25_percent)),
    by_family: Object.fromEntries(families.map((family) => [family, summarize(rows.filter((row) => row.family === family))])),
  },
  proof_price: summarizePrice(rows),
  valid_runs: rows,
  invalid_attempts: invalid,
};
await fs.writeFile(args.out, `${JSON.stringify(result, null, 2)}\n`);
process.stdout.write(`${JSON.stringify({ completion: result.completion, quality: result.quality,
  proof_price: result.proof_price, invalid_attempts: invalid.length }, null, 2)}\n`);

function metric(value) { return { passed: value.criteria_passed, total: value.criteria_total,
  rate: value.criterion_pass_rate }; }
function summarize(items) {
  if (!items.length) return { tasks: 0, estimate_available: false };
  const raw = sum(items.map((row) => row.quality.raw.passed));
  const pp = sum(items.map((row) => row.quality.proofpress.passed));
  const total = sum(items.map((row) => row.quality.raw.total));
  const deltas = items.map((row) => row.quality.delta_percentage_points);
  return { tasks: items.length, estimate_available: true,
    raw: { passed: raw, total, rate: raw / total }, proofpress: { passed: pp, total, rate: pp / total },
    weighted_delta_criteria: pp - raw, weighted_delta_percentage_points: 100 * (pp - raw) / total,
    macro_paired_delta_percentage_points: { values: deltas, ...meanTInterval(deltas) },
    direction: { positive: items.filter((row) => row.quality.delta_criteria > 0).length,
      tie: items.filter((row) => row.quality.delta_criteria === 0).length,
      negative: items.filter((row) => row.quality.delta_criteria < 0).length },
    raw_floor_tasks_below_25_percent: items.filter((row) => row.quality.raw_floor_below_25_percent)
      .map((row) => `${row.family}-${row.scenario}`),
  };
}
function proofPrice(state) {
  const rawS4 = state.episodes.C1_ORDINARY_PORTABLE.stages.find((stage) => stage.stage_id === "S4")?.telemetry;
  const ppS4 = state.episodes.C2_PROOFPRESS.stages.find((stage) => stage.stage_id === "S4")?.telemetry;
  const trace = state.episodes.C2_PROOFPRESS.trace_lookup ?? {};
  const ppCalls = unique([ppS4, state.episodes.C2_PROOFPRESS.judge_transaction?.telemetry,
    trace.telemetry, trace.compiler_telemetry, trace.completeness_telemetry,
    ...(state.episodes.C2_PROOFPRESS.proposals ?? []).map((proposal) => proposal.individual_review?.telemetry)]);
  const rawCalls = unique([rawS4]);
  const raw = sumTelemetry(rawCalls); const pp = sumTelemetry(ppCalls);
  return { definition: "Proofpress receiver/governance calls minus ordinary S4; shared sender and evaluators excluded",
    raw_receiver: raw, proofpress_receiver_and_governance: pp, delta: subtract(pp, raw),
    request_ids: { raw: rawCalls.map((x) => x.request_id), proofpress: ppCalls.map((x) => x.request_id) } };
}
function summarizePrice(rows) {
  const keys = ["model_calls", "input_tokens", "output_tokens", "reasoning_tokens", "total_tokens",
    "provider_cost_usd", "wall_clock_latency_ms"];
  return { tasks: rows.length, delta: Object.fromEntries(keys.map((key) => {
    const values = rows.map((row) => row.proof_price.delta[key]);
    return [key, { total: sum(values), mean: mean(values), median: median(values), values }];
  })) };
}
function capUtilization(state) {
  const calls = [state.episodes.C2_PROOFPRESS.judge_transaction?.telemetry,
    ...Object.values(state.episodes).flatMap((episode) => episode.stages.map((stage) => stage.telemetry)),
    ...Object.values(state.episodes.C2_PROOFPRESS.trace_lookup ?? {}).filter((value) => value?.output_cap_tokens),
    ...(state.episodes.C2_PROOFPRESS.proposals ?? []).map((proposal) => proposal.individual_review?.telemetry)].filter(Boolean);
  const values = calls.filter((value) => value.output_cap_tokens).map((value) => value.output_tokens / value.output_cap_tokens);
  return { maximum: values.length ? Math.max(...values) : null };
}
function unique(values) { const seen = new Set(); return values.filter(Boolean).filter((value) => {
  const key = value.request_id ?? JSON.stringify(value); if (seen.has(key)) return false; seen.add(key); return true; }); }
function sumTelemetry(values) { const out = { model_calls: 0, input_tokens: 0, output_tokens: 0, reasoning_tokens: 0,
  total_tokens: 0, provider_cost_usd: 0, wall_clock_latency_ms: 0 }; for (const value of values) {
  out.model_calls += value.model_calls ?? 1; out.input_tokens += value.input_tokens ?? 0;
  out.output_tokens += value.output_tokens ?? 0; out.reasoning_tokens += value.reasoning_tokens ?? 0;
  out.total_tokens += value.total_tokens ?? ((value.input_tokens ?? 0) + (value.output_tokens ?? 0));
  out.provider_cost_usd += value.provider_cost_usd ?? 0; out.wall_clock_latency_ms += value.wall_clock_latency_ms ?? 0;
} return out; }
function subtract(a, b) { return Object.fromEntries(Object.keys(a).map((key) => [key, a[key] - b[key]])); }
function meanTInterval(values) { if (values.length < 2) return { mean: mean(values), interval_available: false,
  reason: "at least two valid tasks are required" }; const m = mean(values);
  const sd = Math.sqrt(sum(values.map((x) => (x - m) ** 2)) / (values.length - 1));
  const t = [null, null, 12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.16][values.length] ?? 1.96;
  const margin = t * sd / Math.sqrt(values.length); return { mean: m, interval_available: true,
    confidence: 0.95, lower: m - margin, upper: m + margin, method: "descriptive paired t interval over frozen tasks" }; }
function sum(values) { return values.reduce((a, b) => a + b, 0); }
function mean(values) { return values.length ? sum(values) / values.length : null; }
function median(values) { const sorted = [...values].sort((a, b) => a - b); const m = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[m] : (sorted[m - 1] + sorted[m]) / 2; }
async function digest(file) { return `sha256:${crypto.createHash("sha256").update(await fs.readFile(file)).digest("hex")}`; }
async function exists(file) { try { await fs.access(file); return true; } catch { return false; } }
function parse(argv) { const out = {}; for (let i = 0; i < argv.length; i += 1) {
  if (argv[i] === "--root") out.root = path.resolve(argv[++i]);
  else if (argv[i] === "--protocol") out.protocol = path.resolve(argv[++i]);
  else if (argv[i] === "--out") out.out = path.resolve(argv[++i]);
  else throw new Error(`unknown argument ${argv[i]}`);
} if (!out.root || !out.protocol || !out.out) throw new Error("--root --protocol --out are required"); return out; }
