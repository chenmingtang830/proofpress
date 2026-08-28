// Local-only OpenAI-compatible endpoint for private claim construction.
// It fixes one model/provider route and logs only hashes plus aggregate usage.
import { createHash } from 'node:crypto';
import { appendFileSync } from 'node:fs';
import http from 'node:http';
import { createGateway, generateText, jsonSchema, tool } from 'ai';
import { safeParseJSON } from '@ai-sdk/provider-utils';

const model = process.env.PROOFPRESS_CLAIM_MODEL;
const provider = process.env.PROOFPRESS_CLAIM_PROVIDER;
const port = Number(process.env.PROOFPRESS_CLAIM_PORT || 0);
const receipts = process.env.PROOFPRESS_CLAIM_RECEIPTS;
const errors = process.env.PROOFPRESS_CLAIM_ERROR_LOG;
const reasoning = process.env.PROOFPRESS_CLAIM_REASONING || 'none';
const timeoutMs = Number(process.env.PROOFPRESS_CLAIM_TIMEOUT_MS || 115000);

const sha = value => createHash('sha256').update(value).digest('hex');
const reply = (res, status, value) => {
  res.writeHead(status, { 'content-type': 'application/json' });
  res.end(JSON.stringify(value));
};
function append(path, row) {
  if (path) appendFileSync(path, JSON.stringify(row) + '\n', { encoding: 'utf8', mode: 0o600 });
}
function requestBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    req.setEncoding('utf8');
    req.on('data', chunk => { raw += chunk; if (raw.length > 4_000_000) req.destroy(); });
    req.on('end', () => { try { resolve(JSON.parse(raw)); } catch (error) { reject(error); } });
    req.on('error', reject);
  });
}
async function recoverStructuredText(text, schema) {
  const raw = String(text || '').trim();
  const candidates = [raw];
  const unfenced = raw.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '');
  if (unfenced !== raw) candidates.push(unfenced);
  const start = raw.indexOf('{');
  const end = raw.lastIndexOf('}');
  if (start >= 0 && end > start) candidates.push(raw.slice(start, end + 1));
  for (const candidate of [...new Set(candidates)].filter(Boolean)) {
    const parsed = await safeParseJSON({ text: candidate, schema });
    if (parsed.success) return parsed.value;
  }
  return null;
}

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') return reply(res, 200, { ok: true, model, provider });
  if (req.method !== 'POST' || req.url !== '/v1/chat/completions') return reply(res, 404, { error: { type: 'not_found' } });
  const started = process.hrtime.bigint();
  let requestSha = null;
  let terminalWritten = false;
  let upstreamSignal = null;
  const terminal = row => {
    if (terminalWritten) return;
    terminalWritten = true;
    append(receipts, {
      model: model || null, provider: provider || null, fallback_used: false,
      requested_reasoning: reasoning,
      request_sha256: requestSha, terminal: true,
      latency_ms: Number(process.hrtime.bigint() - started) / 1e6,
      ...row,
    });
  };
  try {
    const input = await requestBody(req);
    requestSha = sha(JSON.stringify({ model: input.model, messages: input.messages }));
    if (!model || !provider || input.model !== model || !Array.isArray(input.messages)) {
      terminal({ status: 'inconclusive', error_type: 'frozen_route_required',
                 input_tokens: null, output_tokens: null, cost_usd: null });
      return reply(res, 400, { error: { type: 'frozen_route_required' } });
    }
    const apiKey = process.env.AI_GATEWAY_API_KEY;
    if (!apiKey) {
      terminal({ status: 'inconclusive', error_type: 'missing_gateway_key',
                 input_tokens: null, output_tokens: null, cost_usd: null });
      return reply(res, 503, { error: { type: 'missing_gateway_key' } });
    }
    upstreamSignal = AbortSignal.timeout(Number.isFinite(timeoutMs) && timeoutMs > 0 ? timeoutMs : 115000);
    const common = {
      model: createGateway({ apiKey })(model),
      system: input.messages.filter(row => row.role === 'system').map(row => String(row.content || '')).join('\n'),
      messages: input.messages.filter(row => row.role !== 'system').map(row => ({
        role: row.role === 'assistant' ? 'assistant' : 'user', content: String(row.content || ''),
      })),
      maxOutputTokens: input.max_tokens || 4096,
      // AI SDK v4's Gateway contract takes a scalar effort at the top level.
      // Provider-specific options silently dropped reasoning for routes such
      // as Novita, making the recorded configuration differ from inference.
      reasoning: reasoning === 'none' ? undefined : reasoning,
      abortSignal: upstreamSignal,
      maxRetries: 0,
      providerOptions: {
        gateway: { only: [provider], order: [provider] },
      },
    };
    const structured = input.response_schema && typeof input.response_schema === 'object';
    const toolName = 'emit_proofpress_output';
    const structuredSchema = structured ? jsonSchema(input.response_schema) : null;
    const result = structured
      ? await generateText({ ...common,
          tools: { [toolName]: tool({
            description: `Emit ${String(input.response_schema_name || 'Proofpress output')} exactly once.`,
            inputSchema: structuredSchema,
          }) },
          toolChoice: { type: 'tool', toolName },
        })
      : await generateText(common);
    const usage = result.usage || {};
    const metadata = result.providerMetadata?.gateway || {};
    const cost = Number.isFinite(Number(metadata.cost)) ? Number(metadata.cost) : null;
    let structuredObject = structured ? result.toolCalls?.find(call => call.toolName === toolName)?.input : null;
    let structuredMode = structured ? 'tool_call' : null;
    if (structured && (!structuredObject || typeof structuredObject !== 'object')) {
      const recoveryText = [result.text, result.reasoningText,
        ...(Array.isArray(result.content) ? result.content
          .filter(part => part?.type === 'text' || part?.type === 'reasoning')
          .map(part => part.text) : [])].filter(Boolean).join('\n');
      structuredObject = await recoverStructuredText(recoveryText, structuredSchema);
      structuredMode = structuredObject ? 'deterministic_text_recovery' : 'missing';
    }
    if (structured && (!structuredObject || typeof structuredObject !== 'object')) {
      const error = new Error('provider returned no schema-bound tool call');
      error.name = 'StructuredToolCallMissingError';
      error.finishReason = result.finishReason || null;
      error.structuredMode = structuredMode;
      error.outputBytes = Buffer.byteLength(String(result.text || ''));
      error.reasoningBytes = Buffer.byteLength(String(result.reasoningText || ''));
      error.inputTokens = usage.inputTokens ?? null;
      error.outputTokens = usage.outputTokens ?? null;
      error.costUsd = cost;
      throw error;
    }
    terminal({
      status: 'ok', error_type: null,
      structured_mode: structuredMode,
      input_tokens: usage.inputTokens ?? null, output_tokens: usage.outputTokens ?? null,
      cost_usd: cost,
    });
    return reply(res, 200, {
      id: result.response?.id || null, object: 'chat.completion', model,
      choices: [{ message: { role: 'assistant', content: structured ? JSON.stringify(structuredObject) : (result.text || '') },
                  finish_reason: result.finishReason || null }],
      proofpress: { structured_output_mode: structuredMode },
      usage: { prompt_tokens: usage.inputTokens ?? null,
               completion_tokens: usage.outputTokens ?? null,
               total_tokens: (usage.inputTokens || 0) + (usage.outputTokens || 0),
               cost_usd: cost },
    });
  } catch (error) {
    const errorType = upstreamSignal?.aborted ? 'GatewayTimeoutError' : (error?.name || 'Error');
    terminal({ status: 'inconclusive', error_type: errorType,
               error_digest: sha(String(error?.message || '')),
               finish_reason: error?.finishReason || null,
               structured_mode: error?.structuredMode || null,
               output_bytes: Number.isFinite(error?.outputBytes) ? error.outputBytes : null,
               reasoning_bytes: Number.isFinite(error?.reasoningBytes) ? error.reasoningBytes : null,
               input_tokens: error?.inputTokens ?? null,
               output_tokens: error?.outputTokens ?? null,
               cost_usd: Number.isFinite(error?.costUsd) ? error.costUsd : null });
    append(errors, { name: errorType, message_sha256: sha(String(error?.message || '')) });
    return reply(res, 502, { error: { type: 'gateway_bridge_failed',
                                     message_sha256: sha(String(error?.message || '')) } });
  }
});

server.listen(port, '127.0.0.1', () => process.stdout.write(JSON.stringify({
  type: 'ready', port: server.address().port, model, provider, reasoning,
}) + '\n'));
