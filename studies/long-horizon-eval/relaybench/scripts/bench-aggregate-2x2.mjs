#!/usr/bin/env node
import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

const args = parse(process.argv.slice(2));
const index = JSON.parse(await fs.readFile(path.resolve(args.index), "utf8"));
const rows = [];
for (const entry of index.runs) {
  const run = path.resolve(entry.run);
  const summaryPath = path.join(run, "RUN_SUMMARY.json");
  const summary = JSON.parse(await fs.readFile(summaryPath, "utf8"));
  const rubric = JSON.parse(await fs.readFile(path.join(run, "PUBLIC_RUBRIC_SCORES.json"), "utf8"));
  const row = { ...entry, task_id: summary.task_id, public_rubric: summary.public_rubric,
    receiver_resources: summary.receiver_resources,
    proof_price: summary.receiver_resources.proof_price,
    rubric_evaluator_receipts: Object.fromEntries(Object.entries(rubric).map(([condition, score]) =>
      [condition, score.telemetry])),
    receipts: { run_summary_sha256: await digest(summaryPath),
      public_rubric_sha256: await digest(path.join(run, "PUBLIC_RUBRIC_SCORES.json")) } };
  if (entry.arm === "stress") {
    const trustPath = path.join(run, "TRUST_ENDPOINT_SCORES_attempt-1.json");
    const trust = JSON.parse(await fs.readFile(trustPath, "utf8"));
    row.trust_evaluator_receipt = trust.evaluator.telemetry;
    row.trust = Object.fromEntries(Object.entries(trust.results).map(([condition, result]) =>
      [condition, { disposition: result.disposition, unsafe_claim_propagated: result.unsafe_claim_propagated,
        conflict_recognized: result.conflict_recognized,
        revalidation_or_escalation_preserved: result.revalidation_or_escalation_preserved,
        memo_digest: result.memo_digest } ]));
    row.receipts.trust_endpoint_sha256 = await digest(trustPath);
  }
  rows.push(row);
}

const clean = rows.filter((x) => x.arm === "clean");
const stress = rows.filter((x) => x.arm === "stress");
const result = {
  schema_version: 1,
  classification: "Proofpress 2x2 handoff study",
  frozen_protocol: index.frozen_protocol,
  model: index.model,
  repetitions: index.repetitions,
  claim_boundary: {
    clean: "unmodified public LAB tasks scored by a frozen public-rubric evaluator; not an official Harvey private leaderboard result",
    stress: "LAB-derived controlled handoff stress test; not an official Harvey benchmark result",
    inference: "repeated-run descriptive uncertainty over this three-task frozen panel; not a population estimate",
  },
  clean_quality: quality(clean, index.noninferiority_margin_percentage_points),
  stress_quality: quality(stress, null),
  protection: protection(stress),
  proof_price: { clean: price(clean), stress: price(stress), all: price(rows) },
  task_results: rows,
  invalid_attempts: index.invalid_attempts,
};
process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);

function quality(items, margin) {
  const deltas = items.map((x) => x.public_rubric.paired_delta_percentage_points);
  const rawPassed = sum(items, (x) => x.public_rubric.raw.passed);
  const proofpressPassed = sum(items, (x) => x.public_rubric.proofpress.passed);
  const total = sum(items, (x) => x.public_rubric.raw.total);
  const ci = meanTInterval(deltas);
  return { pairs: items.length, raw: { passed: rawPassed, total, rate: rawPassed / total },
    proofpress: { passed: proofpressPassed, total, rate: proofpressPassed / total },
    weighted_delta_criteria: proofpressPassed - rawPassed,
    weighted_delta_percentage_points: 100 * (proofpressPassed - rawPassed) / total,
    paired_delta_percentage_points: { values: deltas, ...ci },
    ...(margin == null ? {} : { preregistered_noninferiority_margin_percentage_points: margin,
      descriptive_noninferiority_met: ci.lower_95 > margin }) };
}

function protection(items) {
  const pairs = items.map((x) => ({ repeat: x.repeat, task: x.task,
    ordinary_unsafe: x.trust.C1_ORDINARY_PORTABLE.unsafe_claim_propagated,
    proofpress_unsafe: x.trust.C2_PROOFPRESS.unsafe_claim_propagated }));
  const rawUnsafe = pairs.filter((x) => x.ordinary_unsafe).length;
  const proofpressUnsafe = pairs.filter((x) => x.proofpress_unsafe).length;
  const protectedOnly = pairs.filter((x) => x.ordinary_unsafe && !x.proofpress_unsafe).length;
  const harmedOnly = pairs.filter((x) => !x.ordinary_unsafe && x.proofpress_unsafe).length;
  const discordant = protectedOnly + harmedOnly;
  return { pairs: pairs.length, ordinary_unsafe: rawUnsafe, proofpress_unsafe: proofpressUnsafe,
    ordinary_unsafe_rate: rawUnsafe / pairs.length, proofpress_unsafe_rate: proofpressUnsafe / pairs.length,
    observed_protection_effect_percentage_points: 100 * (rawUnsafe - proofpressUnsafe) / pairs.length,
    discordant_pairs: { protected_only: protectedOnly, harmed_only: harmedOnly, total: discordant,
      exact_two_sided_mcnemar_p: exactBinomialTwoSided(Math.min(protectedOnly, harmedOnly), discordant) },
    task_breakdown: Object.fromEntries([...new Set(pairs.map((x) => x.task))].map((task) => {
      const group = pairs.filter((x) => x.task === task);
      return [task, { pairs: group.length, ordinary_unsafe: group.filter((x) => x.ordinary_unsafe).length,
        proofpress_unsafe: group.filter((x) => x.proofpress_unsafe).length }];
    })), pairs_detail: pairs };
}

function price(items) {
  const keys = ["model_calls", "input_tokens", "output_tokens", "reasoning_tokens", "total_tokens",
    "provider_cost_usd", "sequential_model_latency_ms"];
  return Object.fromEntries(keys.map((key) => {
    const values = items.map((x) => x.proof_price[key]);
    return [key, { total: values.reduce((a, b) => a + b, 0), mean: mean(values), median: median(values), values }];
  }));
}

function meanTInterval(values) {
  const center = mean(values); const n = values.length;
  const variance = values.reduce((s, x) => s + (x - center) ** 2, 0) / (n - 1);
  const standardError = Math.sqrt(variance / n);
  const critical = n === 9 ? 2.306 : 1.96;
  return { mean: center, sample_standard_deviation: Math.sqrt(variance), standard_error: standardError,
    lower_95: center - critical * standardError, upper_95: center + critical * standardError,
    method: n === 9 ? "paired t interval, df=8" : "normal approximation" };
}
function exactBinomialTwoSided(k, n) {
  if (n === 0) return 1;
  let tail = 0; for (let i = 0; i <= k; i += 1) tail += choose(n, i) * 0.5 ** n;
  return Math.min(1, 2 * tail);
}
function choose(n, k) { let out = 1; for (let i = 1; i <= k; i += 1) out = out * (n - k + i) / i; return out; }
function mean(xs) { return xs.reduce((a, b) => a + b, 0) / xs.length; }
function median(xs) { const s = [...xs].sort((a, b) => a - b); return s.length % 2 ? s[(s.length - 1) / 2] : (s[s.length / 2 - 1] + s[s.length / 2]) / 2; }
function sum(xs, fn) { return xs.reduce((n, x) => n + fn(x), 0); }
async function digest(file) { return `sha256:${crypto.createHash("sha256").update(await fs.readFile(file)).digest("hex")}`; }
function parse(argv) { const out = {}; for (let i = 0; i < argv.length; i += 1) {
  if (argv[i] === "--index") out.index = argv[++i]; else throw new Error(`unknown argument: ${argv[i]}`);
} if (!out.index) throw new Error("--index is required"); return out; }
