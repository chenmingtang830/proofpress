import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { evaluatePublicRubric } from "../evaluation/public-rubric.mjs";

const execFileAsync = promisify(execFile);
test("public rubric evaluator preserves the non-official claim boundary", async () => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "rubric-test-"));
  const task = path.join(root, "task.json"); await fs.writeFile(task, JSON.stringify({ criteria: [{ id: "C-1" }, { id: "C-2" }] }));
  const md = path.join(root, "memo.md"), docx = path.join(root, "memo.docx"); await fs.writeFile(md, "# Memo\n");
  await execFileAsync("pandoc", [md, "-o", docx]);
  const adapter = { invoke: async () => ({ raw_output: JSON.stringify({ criteria: [{ id: "C-1", passed: true, rationale: "x" }, { id: "C-2", passed: false, rationale: "y" }] }), telemetry: { model_calls: 1 } }) };
  const score = await evaluatePublicRubric({ taskPath: task, deliverable: docx,
    evaluator: { status: "FROZEN_PUBLIC_RUBRIC_EVALUATOR", claim_boundary: "not official" }, adapterOverride: adapter });
  assert.equal(score.criteria_passed, 1); assert.equal(score.criterion_pass_rate, 0.5); assert.equal(score.claim_boundary, "not official");
});
