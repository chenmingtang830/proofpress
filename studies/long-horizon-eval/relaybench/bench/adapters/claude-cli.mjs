import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { validateAdapter, validateAdapterResult } from "./adapter-contract.mjs";

const execFileAsync = promisify(execFile);

export async function preflightClaudeCli(config, env = process.env) {
  const binary = config.binary ?? "claude";
  try {
    const { stdout, stderr } = await execFileAsync(binary, ["--version"], { env, timeout: 10_000 });
    return { passed: true, binary, version: `${stdout}${stderr}`.trim(), model: config.resolved_model };
  } catch (error) {
    return { passed: false, binary, model: config.resolved_model, error: error.message };
  }
}

export function createClaudeCliAdapter(config, deps = {}) {
  const run = deps.execFileAsync ?? execFileAsync;
  return validateAdapter({
    id: "claude-cli",
    testOnly: false,
    metadata: () => ({
      provider: "Anthropic",
      route: "local Claude CLI",
      resolved_model: config.resolved_model,
      cli_version: config.cli_version,
      provider_fallback: false,
      cross_provider_retries: false,
      timeout_ms: config.timeout_ms,
    }),
    async invoke(request, context = {}) {
      const args = ["-p", request.prompt, "--model", config.resolved_model, "--output-format", "json",
        "--safe-mode", "--tools", "", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
        "--disable-slash-commands"];
      const started = performance.now();
      let stdout = ""; let stderr = ""; let invocationError = null;
      try {
        ({ stdout, stderr } = await run(config.binary ?? "claude", args, {
          cwd: context.workspace,
          env: context.env ?? process.env,
          timeout: config.timeout_ms,
          maxBuffer: config.max_buffer_bytes ?? 16 * 1024 * 1024,
        }));
      } catch (error) {
        invocationError = error;
        stdout = error.stdout ?? "";
        stderr = error.stderr ?? "";
      }
      const elapsed = Math.round(performance.now() - started);
      let envelope;
      try { envelope = JSON.parse(stdout); } catch { envelope = { result: stdout }; }
      const result = validateAdapterResult({
        raw_output: String(envelope.result ?? envelope.content ?? stdout),
        telemetry: {
          route: "local Claude CLI", model: config.resolved_model, wall_clock_latency_ms: elapsed,
          input_tokens: envelope.usage?.input_tokens ?? null,
          cached_input_tokens: envelope.usage?.cache_read_input_tokens ?? null,
          output_tokens: envelope.usage?.output_tokens ?? null,
          reasoning_tokens: envelope.usage?.reasoning_tokens ?? null,
          provider_cost_usd: envelope.total_cost_usd ?? null,
          actual_incremental_cash_usd: null, model_calls: 1, retries: 0,
          stderr: stderr || null,
          invocation_error: invocationError ? {
            code: invocationError.code ?? null,
            signal: invocationError.signal ?? null,
            killed: invocationError.killed ?? false,
            provider_error: envelope.is_error ? String(envelope.result ?? envelope.error ?? "Claude CLI error") : null,
          } : null,
        },
      });
      if (invocationError && !result.raw_output.trim()) {
        const concise = envelope.result ?? envelope.error ?? stderr ?? invocationError.code ?? "unknown error";
        throw new Error(`Claude CLI invocation failed: ${String(concise).slice(0, 500)}`);
      }
      return result;
    },
  });
}
