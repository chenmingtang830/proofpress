import path from "node:path";
import { spawn } from "node:child_process";
import readline from "node:readline";
import { PROJECT_ROOT } from "./core.mjs";

export function createTestWorkerSession(workspace) {
  const child = spawn(process.execPath, [path.join(PROJECT_ROOT, "bench/workers/deterministic-test-worker.mjs")], {
    cwd: workspace,
    env: minimalEnvironment(),
    stdio: ["pipe", "pipe", "pipe"],
  });
  const pending = new Map();
  let sequence = 0;
  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const lines = readline.createInterface({ input: child.stdout, crlfDelay: Infinity });
  lines.on("line", (line) => {
    let message;
    try { message = JSON.parse(line); } catch { return; }
    const item = pending.get(message.request_id);
    if (!item) return;
    pending.delete(message.request_id);
    if (message.ok) item.resolve(message);
    else item.reject(new Error(message.error ?? "TEST-ONLY worker failed"));
  });
  child.once("error", (error) => {
    for (const item of pending.values()) item.reject(error);
    pending.clear();
  });
  child.once("exit", (code, signal) => {
    if (pending.size) {
      const error = new Error(`TEST-ONLY worker exited before response (code=${code}, signal=${signal}, stderr=${stderr})`);
      for (const item of pending.values()) item.reject(error);
      pending.clear();
    }
  });

  return {
    pid: child.pid,
    environment_keys: Object.keys(minimalEnvironment()).sort(),
    invoke({ stageId, verifierEvidence = null }) {
      const requestId = `${child.pid}-${++sequence}`;
      return new Promise((resolve, reject) => {
        pending.set(requestId, { resolve, reject });
        child.stdin.write(`${JSON.stringify({ request_id: requestId, stage_id: stageId, verifier_evidence: verifierEvidence })}\n`);
      });
    },
    async close() {
      child.stdin.end();
      const result = await new Promise((resolve, reject) => {
        child.once("error", reject);
        child.once("exit", (code, signal) => resolve({ code, signal }));
      });
      lines.close();
      return { ...result, stderr };
    },
  };
}

function minimalEnvironment() {
  const env = {};
  for (const key of ["PATH", "LANG", "LC_ALL", "TMPDIR"]) {
    if (typeof process.env[key] === "string") env[key] = process.env[key];
  }
  env.RELAYBENCH_TEST_ONLY = "1";
  return env;
}
