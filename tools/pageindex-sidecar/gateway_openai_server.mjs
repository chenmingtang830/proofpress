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
  return rows.map(row => ({ role: row.role === 'assistant' ? 'assistant' : 'user', content: String(row.content || '') }));
}
function appendReceipt(row) {
  if (!receipts) return;
  // The output location is caller-owned private storage.
  appendFileSync(receipts, JSON.stringify(row) + '\n', { encoding: 'utf8', mode: 0o600 });
}
const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') return reply(res, 200, { ok: true, model, provider });
  if (req.method !== 'POST' || req.url !== '/v1/chat/completions') return reply(res, 404, { error: { type: 'not_found' } });
  try {
    const input = await requestBody(req);
    if (input.model !== model || !Array.isArray(input.messages)) return reply(res, 400, { error: { type: 'frozen_model_required' } });
    const apiKey = process.env.AI_GATEWAY_API_KEY;
    if (!apiKey) return reply(res, 503, { error: { type: 'missing_gateway_key' } });
    const result = await generateText({
      model: createGateway({ apiKey })(model), messages: messages(input.messages),
      maxOutputTokens: input.max_tokens || 4096, maxRetries: 0,
      providerOptions: { gateway: { only: [provider], order: [provider] } },
    });
    const usage = result.usage || {}, meta = result.providerMetadata?.gateway || {};
    appendReceipt({ model, provider, fallback_used: false, request_sha256: sha(JSON.stringify({ model: input.model, messages: input.messages })),
      input_tokens: usage.inputTokens ?? null, output_tokens: usage.outputTokens ?? null,
      cost_usd: typeof meta.cost === 'number' ? meta.cost : null });
    return reply(res, 200, { id: result.response?.id || null, object: 'chat.completion', model,
      choices: [{ message: { role: 'assistant', content: result.text || '' }, finish_reason: result.finishReason || null }],
      usage: { prompt_tokens: usage.inputTokens ?? null, completion_tokens: usage.outputTokens ?? null, total_tokens: (usage.inputTokens || 0) + (usage.outputTokens || 0) } });
  } catch (error) {
    return reply(res, 502, { error: { type: 'gateway_bridge_failed', message_sha256: sha(String(error?.message || '')) } });
  }
});
server.listen(port, '127.0.0.1', () => process.stdout.write(JSON.stringify({ type: 'ready', port: server.address().port, model, provider }) + '\n'));
