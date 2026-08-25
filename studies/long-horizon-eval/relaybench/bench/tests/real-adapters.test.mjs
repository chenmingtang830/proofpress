import assert from "node:assert/strict";
import test from "node:test";
import { createClaudeCliAdapter, preflightClaudeCli } from "../adapters/claude-cli.mjs";
import { createVercelGatewayAdapter, preflightVercelGateway } from "../adapters/vercel-ai-gateway.mjs";
import { assertResponseEligible } from "../real/response-eligibility.mjs";

test("Claude adapter pins model and records usage without fallback", async () => {
  const adapter = createClaudeCliAdapter({ resolved_model: "claude-opus-4.8", cli_version: "test", timeout_ms: 1000 }, {
    execFileAsync: async (_bin, args) => ({ stdout: JSON.stringify({ result: "ok", usage: { input_tokens: 3, output_tokens: 2 } }), stderr: "" }),
  });
  const result = await adapter.invoke({ prompt: "x" }, { workspace: process.cwd() });
  assert.equal(result.raw_output, "ok");
  assert.equal(result.telemetry.input_tokens, 3);
  assert.equal(adapter.metadata().provider_fallback, false);
});

test("Vercel adapter refuses missing key/provider and hard-pins provider", async () => {
  const config = { endpoint: "https://example.test/v1/chat/completions", resolved_model: "moonshotai/kimi-k3", provider_only: "test-provider", api_key_env: "K", timeout_ms: 1000, temperature: 0, max_output_tokens: 8000 };
  assert.equal(preflightVercelGateway(config, {}).passed, false);
  let sent;
  const adapter = createVercelGatewayAdapter(config, { fetch: async (_url, init) => {
    sent = JSON.parse(init.body);
    return { ok: true, status: 200, headers: new Headers(), json: async () => ({ model: "moonshotai/kimi-k3", choices: [{ message: { content: "ok" } }], usage: { prompt_tokens: 4, completion_tokens: 2 } }) };
  }});
  const result = await adapter.invoke({ prompt: "x", max_output_tokens: 12000 }, { env: { K: "secret" } });
  assert.deepEqual(sent.providerOptions.gateway.only, ["test-provider"]);
  assert.equal(sent.max_tokens, 12000);
  assert.equal(result.telemetry.serving_provider_requested, "test-provider");
  assert.equal(result.telemetry.serving_provider_reported, null);
  assert.equal(result.telemetry.input_tokens, 4);
});

test("Claude preflight is non-payable and reports missing binary", async () => {
  const result = await preflightClaudeCli({ binary: "definitely-not-a-real-claude-binary", resolved_model: "claude-opus-4.8" }, {});
  assert.equal(result.passed, false);
});

test("response eligibility accepts a response below the guardrail", () => {
  const response = { telemetry: { output_tokens: 7999, model_reported: "model-a",
    serving_provider_reported: "provider-a" } };
  assert.equal(assertResponseEligible(response, { label: "worker", outputCap: 8000,
    requestedModel: "model-a", requestedProvider: "provider-a" }), response);
});

test("response eligibility invalidates an exact cap hit", () => {
  assert.throws(() => assertResponseEligible({ telemetry: { output_tokens: 8000 } },
    { label: "worker", outputCap: 8000 }), /output token cap hit \(8000\/8000\)/);
});

test("response eligibility invalidates model or provider identity mismatch", () => {
  assert.throws(() => assertResponseEligible({ telemetry: { model_reported: "model-b" } },
    { label: "worker", requestedModel: "model-a" }), /model identity mismatch/);
  assert.throws(() => assertResponseEligible({ telemetry: { serving_provider_reported: "provider-b" } },
    { label: "worker", requestedProvider: "provider-a" }), /provider identity mismatch/);
});

test("response eligibility invalidates provider invocation failures", () => {
  assert.throws(() => assertResponseEligible({ telemetry: { invocation_error: "socket closed" } },
    { label: "worker" }), /provider invocation failed/);
});

test("response eligibility invalidates a provider truncation finish reason", () => {
  assert.throws(() => assertResponseEligible({ telemetry: { finish_reason: "length" } },
    { label: "worker" }), /provider reported truncated output/);
});
