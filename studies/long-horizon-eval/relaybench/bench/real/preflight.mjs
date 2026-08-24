import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { readJson } from "../lib/core.mjs";
import { preflightClaudeCli } from "../adapters/claude-cli.mjs";
import { preflightVercelGateway } from "../adapters/vercel-ai-gateway.mjs";

const execFileAsync = promisify(execFile);

export async function preflightRealStudy({ manifestPath, harveyCheckout, env = process.env }) {
  const manifest = await readJson(manifestPath);
  const checks = [];
  checks.push(check("real calls remain opt-in", manifest.real_calls_authorized === false,
    "manifest must remain false; the runner additionally requires --authorize-real-calls"));
  checks.push(check("task selection frozen", manifest.task_selection.selection_status === "FROZEN_CALIBRATION" && manifest.task_selection.task_ids.length > 0));
  checks.push(check("automated policy gate frozen", manifest.policy_gate?.mode === "research_only_automated_fail_closed"
    && manifest.policy_gate?.admission_rule === "deterministic_eligible AND frozen_judge_accept"));
  checks.push(check("policy executor is not proposer", manifest.policy_gate?.proposer !== manifest.policy_gate?.executor));
  checks.push(check("policy judge frozen", manifest.policy_gate?.judge?.resolved_model === "google/gemini-3.7-flash"
    && manifest.policy_gate?.judge?.provider_only === "google" && manifest.policy_gate?.judge?.fallback === false));
  checks.push(check("matched execution limits", manifest.budget_policy.matched_execution_limits_required === true));
  checks.push(check("Proofpress overhead counted", manifest.budget_policy.count_all_proofpress_overhead === true));
  checks.push(check("public-rubric evaluator frozen", manifest.evaluator?.status === "FROZEN_PUBLIC_RUBRIC_EVALUATOR" && Boolean(manifest.evaluator?.model)));

  const claude = await preflightClaudeCli(manifest.tracks.find((x) => x.id === "A_HARVEY_COMPARABLE").adapter, env);
  checks.push(check("Track A Claude CLI", claude.passed, claude.error ?? claude.version));
  const vercel = preflightVercelGateway(manifest.tracks.find((x) => x.id === "B_OPEN_WEIGHT_COST").adapter, env);
  checks.push(check("Track B Vercel gateway", vercel.passed, vercel.errors.join("; ")));
  const gemini = manifest.tracks.find((x) => x.id === "C_GEMINI_3_7_FLASH")?.adapter;
  checks.push(check("Track C Gemini 3.7 gateway", gemini?.resolved_model === "google/gemini-3.7-flash"
    && gemini?.provider_only === "google" && gemini?.fallback === false && Boolean(env[gemini?.api_key_env]),
    gemini ? `${gemini.resolved_model} via ${gemini.provider_only}` : "missing track"));
  checks.push(check("evaluator credential", Boolean(env[manifest.evaluator.api_key_env]),
    env[manifest.evaluator.api_key_env] ? "present" : `missing ${manifest.evaluator.api_key_env}`));
  checks.push(check("policy judge credential", Boolean(env[manifest.policy_gate.judge.api_key_env]),
    env[manifest.policy_gate.judge.api_key_env] ? "present" : `missing ${manifest.policy_gate.judge.api_key_env}`));

  if (harveyCheckout) {
    let commit = null;
    try { commit = (await execFileAsync("git", ["-C", harveyCheckout, "rev-parse", "HEAD"])).stdout.trim(); } catch {}
    checks.push(check("Harvey checkout pinned", commit === manifest.task_selection.commit, commit ?? "not a git checkout"));
    for (const relative of manifest.task_selection.required_paths) {
      try { await fs.access(path.join(harveyCheckout, relative)); checks.push(check(`Harvey source ${relative}`, true)); }
      catch { checks.push(check(`Harvey source ${relative}`, false, "missing")); }
    }
  } else checks.push(check("Harvey checkout supplied", false, "pass --harvey-checkout"));

  const blockers = checks.filter((item) => !item.passed).map((item) => item.name);
  return { schema_version: 1, experiment_id: manifest.id, ready: blockers.length === 0,
    payable_calls_made: 0, blockers, checks, routes: { claude, vercel } };
}

function check(name, passed, detail = null) { return { name, passed: Boolean(passed), detail }; }
