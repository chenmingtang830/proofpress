import fs from "node:fs/promises";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { createVercelGatewayAdapter } from "../adapters/vercel-ai-gateway.mjs";

const execFileAsync = promisify(execFile);

export async function evaluatePublicRubric({ taskPath, deliverable, evaluator, env = process.env, adapterOverride = null }) {
  const task = JSON.parse(await fs.readFile(taskPath));
  const { stdout: memo } = await execFileAsync("pandoc", [deliverable, "-t", "plain"], { maxBuffer: 16 * 1024 * 1024 });
  const adapter = adapterOverride ?? createVercelGatewayAdapter({ resolved_model: evaluator.model,
    endpoint: evaluator.endpoint, provider_only: evaluator.provider_only, temperature: evaluator.temperature,
    api_key_env: evaluator.api_key_env, timeout_ms: evaluator.timeout_ms });
  const prompt = `You are a strict rubric grader. Grade each criterion independently against the memo. Return ONLY JSON {"criteria":[{"id":"...","passed":true,"rationale":"brief evidence"}]}. Include every criterion exactly once.\n\nCRITERIA:\n${JSON.stringify(task.criteria)}\n\nMEMO:\n${memo}`;
  const result = await adapter.invoke({ prompt }, { env });
  let parsed; try { parsed = JSON.parse(result.raw_output); } catch { throw new Error("rubric evaluator returned invalid JSON"); }
  const expected = new Set(task.criteria.map((x) => x.id));
  if (!Array.isArray(parsed.criteria) || parsed.criteria.length !== expected.size || parsed.criteria.some((x) => !expected.has(x.id) || typeof x.passed !== "boolean"))
    throw new Error("rubric evaluator must return every public criterion exactly once");
  const passed = parsed.criteria.filter((x) => x.passed).length;
  return { schema_version: 1, evaluator_status: evaluator.status, claim_boundary: evaluator.claim_boundary,
    criteria_total: expected.size, criteria_passed: passed, criterion_pass_rate: passed / expected.size,
    all_pass: passed === expected.size, criteria: parsed.criteria, telemetry: result.telemetry };
}
