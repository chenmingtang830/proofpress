// Local-only OpenAI-compatible endpoint for PageIndex. It fixes the gateway
// route and exposes only aggregate telemetry; request and completion content
// never leaves this process as logs or receipts.
import { createHash } from 'node:crypto';
import { appendFileSync } from 'node:fs';
import http from 'node:http';
import { createGateway, generateText } from 'ai';

const model = process.env.PROOFPRESS_PAGEINDEX_MODEL || 'deepseek/deepseek-v4-flash-0731';
const provider = process.env.PROOFPRESS_PAGEINDEX_PROVIDER || 'fireworks';
const port = Number(process.env.PROOFPRESS_PAGEINDEX_PORT || 0);
const receipts = process.env.PROOFPRESS_PAGEINDEX_RECEIPTS;

function sha(value) { return createHash('sha256').update(value).digest('hex'); }
function reply(res, status, value) { res.writeHead(status, { 'content-type': 'application/json' }); res.end(JSON.stringify(value)); }
function requestBody(req) {
  return new Promise((resolve, reject) => {
    let raw = ''; req.setEncoding('utf8');
    req.on('data', chunk => { raw += chunk; if (raw.length > 4_000_000) req.destroy(); });
    req.on('end', () => { try { resolve(JSON.parse(raw)); } catch (error) { reject(error); } });
    req.on('error', reject);
  });
}
function messages(rows) {
  return rows.filter(row => row.role !== 'system').map(row => ({ role: row.role === 'assistant' ? 'assistant' : 'user', content: String(row.content || '') }));
}
function normalizedPageIndexJson(content) {
  if (typeof content !== 'string') return content;
  const firstArray = content.indexOf('['), lastArray = content.lastIndexOf(']');
  const firstObject = content.indexOf('{'), lastObject = content.lastIndexOf('}');
  const candidates = [
    firstArray >= 0 && lastArray > firstArray ? content.slice(firstArray, lastArray + 1) : null,
    firstObject >= 0 && lastObject > firstObject ? content.slice(firstObject, lastObject + 1) : null,
  ].filter(Boolean);
  for (const candidate of candidates) {
    try {
      let value = JSON.parse(candidate);
      normalizePageIndexTypes(value);
      if (!Array.isArray(value) && Array.isArray(value.node_ids)) value = value.node_ids;
      if (Array.isArray(value) && value.every(item => typeof item === 'number')) value = value.map(String);
      return JSON.stringify(value);
    } catch { /* Keep trying bounded JSON candidates. */ }
  }
  return content;
}
function normalizePageIndexTypes(value) {
  if (Array.isArray(value)) { for (const item of value) normalizePageIndexTypes(item); return value; }
  if (!value || typeof value !== 'object') return value;
  // The PageIndex parser has mixed legacy/current representations: its first
  // tree pass documents a tagged string, while the complete tree processor
  // requires an integer. Normalize the tag at the local protocol boundary.
  if (typeof value.physical_index === 'string') {
    const match = value.physical_index.match(/^<physical_index_(\d+)>$/);
    if (match) value.physical_index = Number(match[1]);
    if (value.physical_index === 'None') value.physical_index = null;
  }
  for (const child of Object.values(value)) normalizePageIndexTypes(child);
  return value;
}
function appendReceipt(row) {
  if (!receipts) return;
  // The output location is caller-owned private storage.
  appendFileSync(receipts, JSON.stringify(row) + '\n', { encoding: 'utf8', mode: 0o600 });
}
const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') return reply(res, 200, { ok: true, model, provider });
  if (req.method !== 'POST' || req.url !== '/v1/chat/completions') return reply(res, 404, { error: { type: 'not_found' } });
  let input, requestSha;
  const startedAt = Date.now();
  try {
    input = await requestBody(req);
    requestSha = sha(JSON.stringify({ model: input.model, messages: input.messages }));
    if (input.model !== model || !Array.isArray(input.messages)) {
      appendReceipt({ model, provider, fallback_used: false, request_sha256: requestSha,
        status: 'inconclusive', terminal: true, input_tokens: null, output_tokens: null,
        cost_usd: null, latency_ms: Date.now() - startedAt, error_type: 'FrozenRouteMismatch' });
      return reply(res, 400, { error: { type: 'frozen_model_required' } });
    }
    const apiKey = process.env.AI_GATEWAY_API_KEY;
    if (!apiKey) {
      appendReceipt({ model, provider, fallback_used: false, request_sha256: requestSha,
        status: 'inconclusive', terminal: true, input_tokens: null, output_tokens: null,
        cost_usd: null, latency_ms: Date.now() - startedAt, error_type: 'MissingGatewayKey' });
      return reply(res, 503, { error: { type: 'missing_gateway_key' } });
    }
    const system = input.messages.filter(row => row.role === 'system').map(row => String(row.content || '')).join('\n');
    let result, content, parseError;
    // PageIndex's client does not declare structured output. Retry only an
    // incomplete/invalid JSON completion on the same frozen route; never
    // substitute another provider or treat partial JSON as a tree.
    for (let attempt = 0; attempt < 3; attempt += 1) {
      result = await generateText({
        model: createGateway({ apiKey })(model), system: `${system}\nReturn only syntactically valid JSON of the exact top-level type requested.`, messages: messages(input.messages),
        maxOutputTokens: input.max_tokens || 16384, reasoning: 'medium', maxRetries: 0,
        providerOptions: { gateway: { only: [provider], order: [provider] } },
      });
      content = normalizedPageIndexJson(result.text || '');
      try { JSON.parse(content); parseError = null; break; } catch (error) { parseError = error; }
    }
    if (parseError) throw new Error('invalid-pageindex-json-after-fixed-route-retries');
    const usage = result.usage || {}, meta = result.providerMetadata?.gateway || {};
    const cost = Number.isFinite(Number(meta.cost)) ? Number(meta.cost) : null;
    appendReceipt({ model, provider, fallback_used: false, request_sha256: requestSha, status: 'ok', terminal: true,
      input_tokens: usage.inputTokens ?? null, output_tokens: usage.outputTokens ?? null,
      cost_usd: cost, latency_ms: Date.now() - startedAt });
    return reply(res, 200, { id: result.response?.id || null, object: 'chat.completion', model,
      choices: [{ message: { role: 'assistant', content }, finish_reason: result.finishReason || null }],
      usage: { prompt_tokens: usage.inputTokens ?? null, completion_tokens: usage.outputTokens ?? null,
        total_tokens: (usage.inputTokens || 0) + (usage.outputTokens || 0), cost_usd: cost } });
  } catch (error) {
    appendReceipt({ model, provider, fallback_used: false, request_sha256: requestSha || null,
      status: 'inconclusive', terminal: true, input_tokens: null, output_tokens: null,
      cost_usd: null, latency_ms: Date.now() - startedAt,
      error_type: error?.constructor?.name || 'Error', message_sha256: sha(String(error?.message || '')) });
    return reply(res, 502, { error: { type: 'gateway_bridge_failed', message_sha256: sha(String(error?.message || '')) } });
  }
});
server.listen(port, '127.0.0.1', () => process.stdout.write(JSON.stringify({ type: 'ready', port: server.address().port, model, provider }) + '\n'));
