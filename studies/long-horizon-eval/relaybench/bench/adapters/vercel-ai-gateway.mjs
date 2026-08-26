import { validateAdapter, validateAdapterResult } from "./adapter-contract.mjs";
import https from "node:https";
import { Agent, fetch as undiciFetch } from "undici";

export function preflightVercelGateway(config, env = process.env) {
  const keyName = config.api_key_env ?? "AI_GATEWAY_API_KEY";
  const errors = [];
  if (!env[keyName]) errors.push(`missing ${keyName}`);
  if (!config.provider_only) errors.push("provider_only must pin exactly one serving provider");
  if (!/^[^/]+\/[^/]+$/.test(config.resolved_model ?? "")) errors.push("resolved_model must use provider/model format");
  return { passed: errors.length === 0, endpoint: config.endpoint, model: config.resolved_model,
    provider_only: config.provider_only, credential_present: Boolean(env[keyName]), errors };
}

export function createVercelGatewayAdapter(config, deps = {}) {
  const dispatcher = new Agent({ headersTimeout: config.timeout_ms, bodyTimeout: config.timeout_ms,
    connectTimeout: Math.min(config.timeout_ms, 60_000) });
  const fetchImpl = deps.fetch ?? (config.stream === true ? null
    : (url, init) => undiciFetch(url, { ...init, dispatcher }));
  return validateAdapter({
    id: "vercel-ai-gateway",
    testOnly: false,
    metadata: () => ({
      provider: "Vercel AI Gateway", route: config.endpoint, resolved_model: config.resolved_model,
      serving_provider_only: config.provider_only, provider_fallback: false,
      cross_provider_retries: false, timeout_ms: config.timeout_ms,
      stream: config.stream === true,
      max_output_tokens: config.max_output_tokens,
      final_stage_max_output_tokens: config.final_stage_max_output_tokens ?? config.max_output_tokens,
      s4_segment_count: config.s4_segment_count ?? 1,
      s4_segment_strategy: config.s4_segment_strategy ?? null,
    }),
    async invoke(request, context = {}) {
      const keyName = config.api_key_env ?? "AI_GATEWAY_API_KEY";
      const apiKey = (context.env ?? process.env)[keyName];
      if (!apiKey) throw new Error(`missing ${keyName}`);
      const started = performance.now();
      const reasoningEffort = Object.hasOwn(request, "reasoning_effort")
        ? request.reasoning_effort : config.reasoning_effort;
      const responseFormat = Object.hasOwn(request, "response_format")
        ? request.response_format : config.response_format;
      const outputCap = request.max_output_tokens ?? config.max_output_tokens;
      const requestBody = {
            model: config.resolved_model,
            messages: [{ role: "user", content: request.prompt }],
            temperature: config.temperature,
            max_tokens: outputCap,
            ...(reasoningEffort ? { reasoning: { effort: reasoningEffort } } : {}),
            ...(responseFormat ? { response_format: responseFormat } : {}),
            providerOptions: { gateway: { only: [config.provider_only] } },
          };
      const response = fetchImpl
        ? await fetchImpl(config.endpoint, {
            method: "POST",
            headers: { "authorization": `Bearer ${apiKey}`, "content-type": "application/json" },
            body: JSON.stringify(requestBody),
          })
        : await postJson(config.endpoint, requestBody, apiKey, config.timeout_ms,
          config.stream === true);
      const body = await response.json();
      if (!response.ok) throw new Error(`Vercel AI Gateway ${response.status}: ${JSON.stringify(body)}`);
      return validateAdapterResult({
        raw_output: body.choices?.[0]?.message?.content ?? "",
        telemetry: {
          route: config.endpoint, model: body.model ?? config.resolved_model,
          model_requested: config.resolved_model,
          model_reported: body.model ?? null,
          serving_provider_requested: config.provider_only,
          serving_provider_reported: response.headers.get("x-ai-gateway-provider") ?? null,
          request_id: response.headers.get("x-vercel-id") ?? body.id ?? null,
          wall_clock_latency_ms: Math.round(performance.now() - started),
          input_tokens: body.usage?.prompt_tokens ?? null,
          cached_input_tokens: body.usage?.prompt_tokens_details?.cached_tokens ?? null,
          output_tokens: body.usage?.completion_tokens ?? null,
          output_cap_tokens: outputCap,
          output_cap_utilization: Number.isFinite(body.usage?.completion_tokens) && Number.isFinite(outputCap)
            ? body.usage.completion_tokens / outputCap : null,
          output_cap_hit: Number.isFinite(body.usage?.completion_tokens) && Number.isFinite(outputCap)
            ? body.usage.completion_tokens >= outputCap : null,
          finish_reason: body.choices?.[0]?.finish_reason ?? null,
          reasoning_tokens: body.usage?.completion_tokens_details?.reasoning_tokens ?? null,
          provider_cost_usd: body.usage?.cost ?? null,
          actual_incremental_cash_usd: null, model_calls: 1, retries: 0,
        },
      });
    },
  });
}

// Node's built-in fetch currently inherits Undici's 300-second headers timeout,
// which can terminate a valid long model generation before the study's frozen
// timeout. Use the standard HTTPS client for real calls so the configured
// timeout is the only transport guardrail. Tests may still inject fetch.
function postJson(endpoint, body, apiKey, timeoutMs, stream) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint);
    // Stream real Gateway responses so long-running generations transmit data
    // throughout the request instead of depending on a single long-idle TLS
    // connection. The adapter reconstructs the same OpenAI-compatible body.
    const payload = JSON.stringify(stream
      ? { ...body, stream: true, stream_options: { include_usage: true } }
      : body);
    let deadline;
    const request = https.request(url, {
      method: "POST",
      headers: {
        authorization: `Bearer ${apiKey}`,
        "content-type": "application/json",
        "content-length": Buffer.byteLength(payload),
      },
    }, (response) => {
      const chunks = [];
      let pending = "";
      let content = "";
      let model = null;
      let id = null;
      let usage = null;
      let finishReason = null;
      const consumeLine = (line) => {
        if (!line.startsWith("data:")) return;
        const data = line.slice(5).trim();
        if (!data || data === "[DONE]") return;
        const chunk = JSON.parse(data);
        model = chunk.model ?? model;
        id = chunk.id ?? id;
        usage = chunk.usage ?? usage;
        finishReason = chunk.choices?.[0]?.finish_reason ?? finishReason;
        const delta = chunk.choices?.[0]?.delta;
        if (typeof delta?.content === "string") content += delta.content;
      };
      response.on("data", (chunk) => {
        chunks.push(chunk);
        if (!stream || response.statusCode < 200 || response.statusCode >= 300) return;
        pending += chunk.toString("utf8");
        const lines = pending.split(/\r?\n/);
        pending = lines.pop() ?? "";
        try { for (const line of lines) consumeLine(line); } catch (error) { request.destroy(error); }
      });
      response.on("end", () => {
        clearTimeout(deadline);
        const raw = Buffer.concat(chunks).toString("utf8");
        if (stream && response.statusCode >= 200 && response.statusCode < 300) {
          try { consumeLine(pending); } catch (error) { reject(error); return; }
        }
        const reconstructed = { id, model,
          choices: [{ message: { content }, finish_reason: finishReason }], usage };
        resolve({
          ok: response.statusCode >= 200 && response.statusCode < 300,
          status: response.statusCode,
          headers: { get: (name) => response.headers[String(name).toLowerCase()] ?? null },
          json: async () => stream && response.statusCode >= 200 && response.statusCode < 300
            ? reconstructed : JSON.parse(raw),
        });
      });
    });
    // `request.setTimeout` is an inactivity timeout and SSE keepalive frames
    // can reset it forever. The frozen experiment timeout is a wall-clock
    // eligibility boundary, so enforce it independently of socket activity.
    deadline = setTimeout(() => request.destroy(
      new Error(`Gateway request exceeded absolute timeout after ${timeoutMs}ms`)), timeoutMs);
    request.setTimeout(timeoutMs, () => request.destroy(new Error(`Gateway request timed out after ${timeoutMs}ms`)));
    request.setSocketKeepAlive(true, 30_000);
    request.on("error", (error) => { clearTimeout(deadline); reject(error); });
    request.end(payload);
  });
}
