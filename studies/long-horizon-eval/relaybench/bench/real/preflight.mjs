import fs from "node:fs/promises";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { readJson } from "../lib/core.mjs";
import { preflightClaudeCli } from "../adapters/claude-cli.mjs";
import { preflightVercelGateway } from "../adapters/vercel-ai-gateway.mjs";

const execFileAsync = promisify(execFile);

export async function preflightRealStudy({ manifestPath, harveyCheckout, trackId = null, env = process.env }) {
  const manifest = await readJson(manifestPath);
  const checks = [];
  checks.push(check("real calls remain opt-in", manifest.real_calls_authorized === false,
    "manifest must remain false; the runner additionally requires --authorize-real-calls"));
  checks.push(check("task selection frozen", manifest.task_selection.selection_status.startsWith("FROZEN_")
    && manifest.task_selection.task_ids.length > 0));
  checks.push(check("automated policy gate frozen", ["research_only_automated_fail_closed",
    "research_only_transaction_batch_fail_closed"].includes(manifest.policy_gate?.mode)
    && manifest.policy_gate?.admission_rule === "deterministic_eligible AND frozen_judge_accept"));
  checks.push(check("policy executor is not proposer", manifest.policy_gate?.proposer !== manifest.policy_gate?.executor));
  checks.push(check("policy judge frozen", manifest.policy_gate?.judge?.resolved_model === "google/gemini-3.7-flash"
    && manifest.policy_gate?.judge?.provider_only === "google" && manifest.policy_gate?.judge?.fallback === false));
  checks.push(check("matched execution limits", manifest.budget_policy.matched_execution_limits_required === true));
  checks.push(check("Proofpress overhead counted", manifest.budget_policy.count_all_proofpress_overhead === true));
  checks.push(check("public-rubric evaluator frozen", manifest.evaluator?.status === "FROZEN_PUBLIC_RUBRIC_EVALUATOR" && Boolean(manifest.evaluator?.model)));

  const selected = manifest.tracks.find((track) => track.id === (trackId ?? "A_HARVEY_COMPARABLE"));
  checks.push(check("selected track exists", Boolean(selected), trackId ?? "A_HARVEY_COMPARABLE"));
  let route = null;
  if (selected?.route === "local Claude CLI") {
    route = await preflightClaudeCli(selected.adapter, env);
    checks.push(check(`selected track ${selected.id}`, route.passed, route.error ?? route.version));
  } else if (selected) {
    route = preflightVercelGateway(selected.adapter, env);
    checks.push(check(`selected track ${selected.id}`, route.passed, route.errors.join("; ")));
  }
  checks.push(check("evaluator credential", Boolean(env[manifest.evaluator.api_key_env]),
    env[manifest.evaluator.api_key_env] ? "present" : `missing ${manifest.evaluator.api_key_env}`));
  checks.push(check("policy judge credential", Boolean(env[manifest.policy_gate.judge.api_key_env]),
    env[manifest.policy_gate.judge.api_key_env] ? "present" : `missing ${manifest.policy_gate.judge.api_key_env}`));

  if (harveyCheckout) {
    let commit = null;
    try { commit = (await execFileAsync("git", ["-C", harveyCheckout, "rev-parse", "HEAD"])).stdout.trim(); } catch {}
    checks.push(check("Harvey checkout pinned", commit === manifest.task_selection.commit, commit ?? "not a git checkout"));
    for (const taskId of manifest.task_selection.task_ids) {
      const root = taskId.replace(/^contracts\//, "tasks/contracts/");
      for (const suffix of ["task.json", "documents"]) {
        const relative = path.join(root, suffix);
        try { await fs.access(path.join(harveyCheckout, relative)); checks.push(check(`Harvey source ${relative}`, true)); }
        catch { checks.push(check(`Harvey source ${relative}`, false, "missing")); }
      }
    }
  } else checks.push(check("Harvey checkout supplied", false, "pass --harvey-checkout"));

  const blockers = checks.filter((item) => !item.passed).map((item) => item.name);
  return { schema_version: 1, experiment_id: manifest.id, ready: blockers.length === 0,
    payable_calls_made: 0, blockers, checks, routes: { selected: route } };
}

function check(name, passed, detail = null) { return { name, passed: Boolean(passed), detail }; }
