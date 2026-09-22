import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateRequest, boundedFetch, GatewayFailure } from './bridge.mjs';
const body = { model: 'typesafe-ai/jev', state: { synthetic: true }, questions: {
  item_0_recommendation: { type: 'choice', instructions: 'Decide', criteria: { accept: 'Yes', reject: 'No', escalate: 'Unsure' } },
  item_0_support: { type: 'boolean', instructions: 'Supported?' },
}, providerOptions: { gateway: { zeroDataRetention: true } } };
const response = { answers: {
  item_0_recommendation: { type: 'choice', choice: 'accept', probabilities: { accept: .98, reject: .01, escalate: .01 } },
  item_0_support: { type: 'boolean', probability: .99 },
}, providerMetadata: { typesafe: { confidence: { item_0_recommendation: .95 }, private: 'must-not-cross' } },
usage: { inputTokens: 12, outputTokens: 4 } };
test('official SDK wire contract, explicit key, normalization, bounded metadata', async () => {
  let calls = 0;
  const r = await evaluateRequest(body, 'workspace-test-key', async (url, options) => {
    calls++;
    assert.equal(url, 'https://ai-gateway.vercel.sh/v4/ai/evaluation-model');
    assert.equal(new Headers(options.headers).get('authorization'), 'Bearer workspace-test-key');
    const wire = JSON.parse(options.body);
    assert.deepEqual(wire, { state: body.state, questions: body.questions, providerOptions: body.providerOptions });
    return Response.json(response);
  });
  assert.equal(calls, 1);
  assert.equal(r.answers.item_0_recommendation.confidence, .95);
  assert.deepEqual(r.answers.item_0_support, { type: 'noul', noul: .99 });
  assert.deepEqual(r.usage, { input_tokens: 12, output_tokens: 4 });
  assert.ok(!JSON.stringify(r).includes('must-not-cross'));
});
test('missing keys and wrong model fail before network', async () => {
  const noCall = () => assert.fail('Unexpected request');
  await assert.rejects(evaluateRequest(body, '', noCall));
  await assert.rejects(evaluateRequest({ ...body, model: 'other' }, 'test', noCall));
});
test('no retry on provider failure; malformed answers fail SDK validation', async () => {
  let calls = 0;
  await assert.rejects(evaluateRequest(body, 'test', async () => { calls++; return new Response('secret provider body', { status: 503 }); }),
    error => error instanceof GatewayFailure && error.code === 'http_503' && !String(error).includes('secret'));
  assert.equal(calls, 1);
  await assert.rejects(evaluateRequest(body, 'test', async () => Response.json({ ...response, answers: {} })),
    error => error instanceof GatewayFailure && error.code === 'evaluation');
});
test('Gateway authentication status is classified without its response body', async () => {
  await assert.rejects(evaluateRequest(body, 'test', async () => new Response('secret key detail', { status: 401 })),
    error => error instanceof GatewayFailure && error.code === 'http_401' && !String(error).includes('secret'));
});
test('provider bodies are bounded before parsing', async () => {
  const prior = globalThis.fetch;
  globalThis.fetch = async () => new Response('x'.repeat(128001));
  try { await assert.rejects(boundedFetch('https://example.test', {}), /exceeds limit/); }
  finally { globalThis.fetch = prior; }
});
