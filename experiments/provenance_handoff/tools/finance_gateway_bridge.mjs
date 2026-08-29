// Local-only, fixed-route Vercel AI Gateway bridge for Finance qualification.
// It persists hashes and terminal telemetry, never prompts or model outputs.
import { createHash } from 'node:crypto';
import { appendFileSync } from 'node:fs';
import http from 'node:http';
import { createGateway, generateText, jsonSchema, tool } from 'ai';

const model = process.env.PROOFPRESS_FINANCE_MODEL;
const provider = process.env.PROOFPRESS_FINANCE_PROVIDER;
const reasoning = process.env.PROOFPRESS_FINANCE_REASONING || 'none';
const port = Number(process.env.PROOFPRESS_FINANCE_PORT || 0);
const timeoutMs = Number(process.env.PROOFPRESS_FINANCE_TIMEOUT_MS || 180000);
const receipts = process.env.PROOFPRESS_FINANCE_RECEIPTS;
const sha = value => createHash('sha256').update(String(value)).digest('hex');
const append = row => {
  if (receipts) appendFileSync(receipts, JSON.stringify(row) + '\n', { encoding: 'utf8', mode: 0o600 });
};
const reply = (res, status, body) => {
  res.writeHead(status, { 'content-type': 'application/json' });
  res.end(JSON.stringify(body));
};
const readBody = req => new Promise((resolve, reject) => {
  let raw = '';
  req.setEncoding('utf8');
  req.on('data', chunk => {
    raw += chunk;
    if (raw.length > 4_000_000) req.destroy(new Error('request_too_large'));
  });
  req.on('end', () => { try { resolve(JSON.parse(raw)); } catch (error) { reject(error); } });
  req.on('error', reject);
});

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') {
    return reply(res, 200, { ok: true, model, provider, reasoning });
  }
  if (req.method !== 'POST' || req.url !== '/v1/chat/completions') {
    return reply(res, 404, { error: { type: 'not_found' } });
  }
  const started = process.hrtime.bigint();
  let requestSha = null;
  let terminalWritten = false;
  let signal = null;
  const terminal = row => {
    if (terminalWritten) return;
    terminalWritten = true;
    append({
      schema_version: 'proofpress/finance-gateway-receipt/v1',
      requested_model: model || null,
      requested_provider: provider || null,
      requested_reasoning: reasoning,
      fallback_used: false,
      request_sha256: requestSha,
      terminal: true,
      latency_ms: Number(process.hrtime.bigint() - started) / 1e6,
      ...row,
    });
  };
  try {
    const input = await readBody(req);
    requestSha = sha(JSON.stringify({ model: input.model, messages: input.messages,
                                      response_schema: input.response_schema || null }));
    if (!model || !provider || input.model !== model || !Array.isArray(input.messages)) {
      terminal({ status: 'inconclusive', error_type: 'frozen_route_required',
                 resolved_model: null, resolved_provider: null,
                 input_tokens: null, output_tokens: null, cost_usd: null });
      return reply(res, 400, { error: { type: 'frozen_route_required' } });
    }
    if (!process.env.AI_GATEWAY_API_KEY) {
      terminal({ status: 'inconclusive', error_type: 'missing_gateway_key',
                 resolved_model: null, resolved_provider: null,
                 input_tokens: null, output_tokens: null, cost_usd: null });
      return reply(res, 503, { error: { type: 'missing_gateway_key' } });
    }
    signal = AbortSignal.timeout(Number.isFinite(timeoutMs) && timeoutMs > 0 ? timeoutMs : 180000);
    const schema = input.response_schema && typeof input.response_schema === 'object'
      ? jsonSchema(input.response_schema) : null;
    const toolName = 'emit_finance_output';
    const common = {
      model: createGateway({ apiKey: process.env.AI_GATEWAY_API_KEY })(model),
      system: input.messages.filter(row => row.role === 'system').map(row => String(row.content || '')).join('\n'),
      messages: input.messages.filter(row => row.role !== 'system').map(row => ({
        role: row.role === 'assistant' ? 'assistant' : 'user', content: String(row.content || ''),
      })),
      maxOutputTokens: Number(input.max_tokens || 4096),
      reasoning: reasoning === 'none' ? undefined : reasoning,
      abortSignal: signal,
      maxRetries: 0,
      providerOptions: { gateway: { only: [provider], order: [provider] } },
    };
    const result = schema
      ? await generateText({ ...common,
          tools: { [toolName]: tool({ description: 'Emit the schema-bound Finance output exactly once.', inputSchema: schema }) },
          toolChoice: { type: 'tool', toolName },
        })
      : await generateText(common);
    const usage = result.usage || {};
    const gateway = result.providerMetadata?.gateway || {};
    const routing = gateway.routing || {};
    const resolvedProvider = routing.resolvedProvider || null;
    const resolvedModel = routing.canonicalSlug || routing.originalModelId || model;
    const cost = Number.isFinite(Number(gateway.cost)) ? Number(gateway.cost) : null;
    const structured = schema ? result.toolCalls?.find(row => row.toolName === toolName)?.input : null;
    if (schema && (!structured || typeof structured !== 'object')) {
      const error = new Error('schema_bound_tool_call_missing');
      error.name = 'StructuredOutputMissingError';
      throw error;
    }
    if (resolvedProvider !== provider || resolvedModel !== model || routing.modelAttemptCount > 1
        || routing.totalProviderAttemptCount > 1) {
      const error = new Error('resolved_route_mismatch');
      error.name = 'ResolvedRouteMismatchError';
      throw error;
    }
    terminal({ status: 'ok', error_type: null, resolved_model: resolvedModel,
               resolved_provider: resolvedProvider,
               input_tokens: usage.inputTokens ?? null,
               output_tokens: usage.outputTokens ?? null, cost_usd: cost,
               model_attempt_count: routing.modelAttemptCount ?? null,
               provider_attempt_count: routing.totalProviderAttemptCount ?? null });
    return reply(res, 200, {
      model,
      choices: [{ message: { role: 'assistant', content: schema ? JSON.stringify(structured) : (result.text || '') },
                  finish_reason: result.finishReason || null }],
      usage: { prompt_tokens: usage.inputTokens ?? null, completion_tokens: usage.outputTokens ?? null,
               total_tokens: (usage.inputTokens || 0) + (usage.outputTokens || 0), cost_usd: cost },
    });
  } catch (error) {
    const errorType = signal?.aborted ? 'GatewayTimeoutError' : (error?.name || 'Error');
    terminal({ status: 'inconclusive', error_type: errorType,
               error_digest: sha(error?.message || ''), resolved_model: null,
               resolved_provider: null, input_tokens: null, output_tokens: null, cost_usd: null });
    return reply(res, 502, { error: { type: 'gateway_bridge_failed', message_sha256: sha(error?.message || '') } });
  }
});

server.listen(port, '127.0.0.1', () => process.stdout.write(JSON.stringify({
  type: 'ready', port: server.address().port, model, provider, reasoning,
}) + '\n'));
