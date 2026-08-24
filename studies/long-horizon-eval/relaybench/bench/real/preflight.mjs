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
  checks.push(check("human gate frozen", manifest.review_gate?.mode === "pause_for_authorized_human" && Boolean(manifest.review_gate?.reviewer_role)));
  checks.push(check("no proposer self approval", manifest.review_gate?.proposer !== manifest.review_gate?.reviewer_role));
  checks.push(check("matched execution limits", manifest.budget_policy.matched_execution_limits_required === true));
  checks.push(check("Proofpress overhead counted", manifest.budget_policy.count_all_proofpress_overhead === true));
  checks.push(check("public-rubric evaluator frozen", manifest.evaluator?.status === "FROZEN_PUBLIC_RUBRIC_EVALUATOR" && Boolean(manifest.evaluator?.model)));

  const claude = await preflightClaudeCli(manifest.tracks.find((x) => x.id === "A_HARVEY_COMPARABLE").adapter, env);
  checks.push(check("Track A Claude CLI", claude.passed, claude.error ?? claude.version));
  const vercel = preflightVercelGateway(manifest.tracks.find((x) => x.id === "B_OPEN_WEIGHT_COST").adapter, env);
  checks.push(check("Track B Vercel gateway", vercel.passed, vercel.errors.join("; ")));
  checks.push(check("evaluator credential", Boolean(env[manifest.evaluator.api_key_env]), `missing ${manifest.evaluator.api_key_env}`));

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
