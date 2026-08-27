// Local-only OpenAI-compatible endpoint for private claim construction.
// It fixes one model/provider route and logs only hashes plus aggregate usage.
import { createHash } from 'node:crypto';
import { appendFileSync } from 'node:fs';
import http from 'node:http';
import { createGateway, generateText } from 'ai';

const model = process.env.PROOFPRESS_CLAIM_MODEL;
const provider = process.env.PROOFPRESS_CLAIM_PROVIDER;
const port = Number(process.env.PROOFPRESS_CLAIM_PORT || 0);
const receipts = process.env.PROOFPRESS_CLAIM_RECEIPTS;
const errors = process.env.PROOFPRESS_CLAIM_ERROR_LOG;
const reasoning = process.env.PROOFPRESS_CLAIM_REASONING || 'none';

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

const server = http.createServer(async (req, res) => {
  if (req.method === 'GET' && req.url === '/health') return reply(res, 200, { ok: true, model, provider });
  if (req.method !== 'POST' || req.url !== '/v1/chat/completions') return reply(res, 404, { error: { type: 'not_found' } });
  try {
    const input = await requestBody(req);
    if (!model || !provider || input.model !== model || !Array.isArray(input.messages)) {
      return reply(res, 400, { error: { type: 'frozen_route_required' } });
    }
    const apiKey = process.env.AI_GATEWAY_API_KEY;
    if (!apiKey) return reply(res, 503, { error: { type: 'missing_gateway_key' } });
    const result = await generateText({
      model: createGateway({ apiKey })(model),
      system: input.messages.filter(row => row.role === 'system').map(row => String(row.content || '')).join('\n'),
      messages: input.messages.filter(row => row.role !== 'system').map(row => ({
        role: row.role === 'assistant' ? 'assistant' : 'user', content: String(row.content || ''),
      })),
      maxOutputTokens: input.max_tokens || 4096,
      reasoning,
      maxRetries: 0,
      providerOptions: { gateway: { only: [provider], order: [provider] } },
    });
    const usage = result.usage || {};
    const metadata = result.providerMetadata?.gateway || {};
    const cost = Number.isFinite(Number(metadata.cost)) ? Number(metadata.cost) : null;
    append(receipts, {
      model, provider, fallback_used: false,
      request_sha256: sha(JSON.stringify({ model: input.model, messages: input.messages })),
      input_tokens: usage.inputTokens ?? null, output_tokens: usage.outputTokens ?? null,
      cost_usd: cost,
    });
    return reply(res, 200, {
      id: result.response?.id || null, object: 'chat.completion', model,
      choices: [{ message: { role: 'assistant', content: result.text || '' },
                  finish_reason: result.finishReason || null }],
      usage: { prompt_tokens: usage.inputTokens ?? null,
               completion_tokens: usage.outputTokens ?? null,
               total_tokens: (usage.inputTokens || 0) + (usage.outputTokens || 0),
               cost_usd: cost },
    });
  } catch (error) {
    append(errors, { name: error?.name || 'Error', message_sha256: sha(String(error?.message || '')) });
    return reply(res, 502, { error: { type: 'gateway_bridge_failed',
                                     message_sha256: sha(String(error?.message || '')) } });
  }
});

server.listen(port, '127.0.0.1', () => process.stdout.write(JSON.stringify({
  type: 'ready', port: server.address().port, model, provider,
}) + '\n'));
