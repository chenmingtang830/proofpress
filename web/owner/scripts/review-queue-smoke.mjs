import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
import {fileURLToPath} from 'node:url';
import {mkdir} from 'node:fs/promises';
import {chromium} from 'playwright';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3', [fileURLToPath(new URL('owner-fixture.py', import.meta.url))], {
  cwd: root, env: {...process.env, PYTHONPATH: `${root}/src`}, stdio: ['pipe','pipe','pipe'],
});
let diagnostics = '', browser, page;
fixture.stderr.on('data', chunk => diagnostics += chunk);
try {
  const data = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Fixture startup timed out')), 20000);
    createInterface({input: fixture.stdout}).once('line', line => {clearTimeout(timer); resolve(JSON.parse(line));});
    fixture.once('exit', code => {clearTimeout(timer); reject(new Error(`Fixture exited ${code}: ${diagnostics}`));});
  });
  browser = await chromium.launch();
  page = await browser.newPage();
  await page.addInitScript(() => {
    window.__queueTools = [];
    Object.defineProperty(document, 'modelContext', {configurable: true, value: {
      registerTool: async tool => window.__queueTools.push(tool),
    }});
  });
  page.setDefaultTimeout(12000);
  const errors = [], writes = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(`${data.base}/review`);
  await page.locator('input[name=token]').fill(data.owner);
  await Promise.all([page.waitForNavigation(), page.locator('button[type=submit]').click()]);
  page.on('request', request => {if (request.method() !== 'GET') writes.push(request.url());});
  const graph = (await (await page.request.get(`${data.base}/owner/api/graph`)).json()).result;
  assert.ok(graph.nodes.filter(node => node.type === 'claim').every(node => node.model_review && node.model_review.recommendation === null));
  let scenario = 'advice', requests = 0;
  await page.route('**/owner/api/graph*', route => {
    requests++;
    const result = structuredClone(graph);
    result.nodes.filter(node => node.type === 'claim').forEach((node, index) => {
      node.model_review = {state: 'current', recommendation: ['accept','escalate','reject'][index], model: 'synthetic/offline'};
      if (scenario === 'pending' && index === 0) node.model_review = {state: requests > 1 ? 'current' : 'running', recommendation: 'reject'};
      if (scenario === 'stale' && index === 0) node.model_review = {state: 'stale', recommendation: 'accept'};
      if (scenario === 'history' && index === 0) node.state = 'admitted';
    });
    return route.fulfill({json: {ok: true, result}});
  });
  for (const width of [1512, 1024, 768, 390]) {
    await page.setViewportSize({width, height: width === 390 ? 844 : 982});
    await page.goto(`${data.base}/review?claim_id=${data.ids[0]}`);
    const table = page.locator('.reviewTable');
    if (width < 900) await page.getByRole('button', {name: 'Close details', exact: true}).click();
    else await page.getByRole('button', {name: 'Needs review', exact: true}).click();
    for (const label of ['Suggest approve','Suggest escalate','Suggest reject']) await table.getByText(label, {exact: true}).waitFor();
    assert.equal(await table.locator('td[data-label="Status"]').count(), 0);
    assert.equal(await table.locator('td[data-label="LLM recommendation"]').count(), 3);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth), width);
    if (process.env.QA_SCREENSHOTS) {
      await mkdir(process.env.QA_SCREENSHOTS, {recursive: true});
      await page.getByRole('heading', {name: 'Review', exact: true}).click();
      await page.evaluate(() => document.fonts.ready);
      await page.screenshot({path: `${process.env.QA_SCREENSHOTS}/review-queue-${width}.png`, fullPage: true});
    }
  }
  const queueResult = await page.evaluate(async () => {
    const tool = window.__queueTools.find(tool => tool.name === 'list_review_queue');
    return JSON.parse((await tool.execute({})).content[0].text);
  });
  assert.deepEqual(queueResult.claims.map(claim => claim.model_review.recommendation).sort(), ['accept','escalate','reject']);
  assert.ok(queueResult.claims.every(claim => claim.state === 'needs_review'));
  await page.setViewportSize({width: 1512, height: 982});
  scenario = 'stale'; requests = 0;
  await page.reload();
  await page.locator('.reviewTable').getByText('Refresh required', {exact: true}).waitFor();
  assert.equal(await page.locator('.reviewTable').getByText('Suggest approve', {exact: true}).count(), 0);
  scenario = 'pending'; requests = 0;
  await page.reload();
  await page.locator('.reviewTable').getByText('Reviewing…', {exact: true}).waitFor();
  await page.locator('.reviewTable').getByText('Suggest reject', {exact: true}).nth(1).waitFor();
  assert.ok(requests >= 2, 'A running queue refreshes without selecting a claim');
  scenario = 'history';
  await page.reload();
  await page.getByRole('button', {name: 'Decision history', exact: true}).click();
  await page.locator('.reviewTable td[data-label="Status"]').getByText('admitted', {exact: true}).waitFor();
  assert.equal(await page.locator('.reviewTable td[data-label="LLM recommendation"]').count(), 0);
  assert.deepEqual(writes, []);
  assert.deepEqual(errors, []);
  console.log('PASS: queue advice, four viewport widths, stale advice, background refresh and separate decision history; no mutations.');
} catch (error) {
  console.error('Review queue fixture UI:', page?.url(), await page?.locator('body').innerText());
  throw error;
} finally {
  await browser?.close();
  fixture.stdin.end('\n');
  fixture.kill();
}
