import { validateAdapter, validateAdapterResult } from "./adapter-contract.mjs";

export function preflightVercelGateway(config, env = process.env) {
  const keyName = config.api_key_env ?? "AI_GATEWAY_API_KEY";
  const errors = [];
  if (!env[keyName]) errors.push(`missing ${keyName}`);
  if (!config.provider_only) errors.push("provider_only must pin exactly one serving provider");
  if (config.resolved_model !== "moonshotai/kimi-k3") errors.push("resolved_model must be moonshotai/kimi-k3 for Track B");
  return { passed: errors.length === 0, endpoint: config.endpoint, model: config.resolved_model,
    provider_only: config.provider_only, credential_present: Boolean(env[keyName]), errors };
}

export function createVercelGatewayAdapter(config, deps = {}) {
  const fetchImpl = deps.fetch ?? fetch;
  return validateAdapter({
    id: "vercel-ai-gateway",
    testOnly: false,
    metadata: () => ({
      provider: "Vercel AI Gateway", route: config.endpoint, resolved_model: config.resolved_model,
      serving_provider_only: config.provider_only, provider_fallback: false,
      cross_provider_retries: false, timeout_ms: config.timeout_ms,
    }),
    async invoke(request, context = {}) {
      const keyName = config.api_key_env ?? "AI_GATEWAY_API_KEY";
      const apiKey = (context.env ?? process.env)[keyName];
      if (!apiKey) throw new Error(`missing ${keyName}`);
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), config.timeout_ms);
      const started = performance.now();
      let response;
      try {
        response = await fetchImpl(config.endpoint, {
          method: "POST", signal: controller.signal,
          headers: { "authorization": `Bearer ${apiKey}`, "content-type": "application/json" },
          body: JSON.stringify({
            model: config.resolved_model,
            messages: [{ role: "user", content: request.prompt }],
            temperature: config.temperature,
            max_tokens: config.max_output_tokens,
            providerOptions: { gateway: { only: [config.provider_only] } },
          }),
        });
      } finally { clearTimeout(timer); }
      const body = await response.json();
      if (!response.ok) throw new Error(`Vercel AI Gateway ${response.status}: ${JSON.stringify(body)}`);
      return validateAdapterResult({
        raw_output: body.choices?.[0]?.message?.content ?? "",
        telemetry: {
          route: config.endpoint, model: body.model ?? config.resolved_model,
          serving_provider: response.headers.get("x-ai-gateway-provider") ?? config.provider_only,
          request_id: response.headers.get("x-vercel-id") ?? body.id ?? null,
          wall_clock_latency_ms: Math.round(performance.now() - started),
          input_tokens: body.usage?.prompt_tokens ?? null,
          cached_input_tokens: body.usage?.prompt_tokens_details?.cached_tokens ?? null,
          output_tokens: body.usage?.completion_tokens ?? null,
          reasoning_tokens: body.usage?.completion_tokens_details?.reasoning_tokens ?? null,
          provider_cost_usd: body.usage?.cost ?? null,
          actual_incremental_cash_usd: null, model_calls: 1, retries: 0,
        },
      });
    },
  });
}
