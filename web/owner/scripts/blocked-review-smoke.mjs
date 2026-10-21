import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import { mkdir } from 'node:fs/promises';
import assert from 'node:assert/strict';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3', [fileURLToPath(new URL('owner-fixture.py', import.meta.url))], {
  cwd: root, env: {...process.env, PYTHONPATH: `${root}/src`}, stdio: ['pipe', 'pipe', 'pipe'],
});
let diagnostics = '';
fixture.stderr.on('data', data => diagnostics += data);
let browser;
try {
  const data = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Fixture startup timeout')), 20000);
    createInterface({input: fixture.stdout}).once('line', line => { clearTimeout(timer); resolve(JSON.parse(line)); });
    fixture.once('exit', code => { clearTimeout(timer); reject(new Error(`Fixture failed ${code}: ${diagnostics}`)); });
  });
  browser = await chromium.launch();
  const page = await browser.newPage({viewport: {width: 1536, height: 1024}});
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(`${data.base}/review`);
  await page.locator('input[name=token]').fill(data.owner);
  await Promise.all([page.waitForNavigation(), page.locator('button[type=submit]').click()]);
  for (const decision of ['request_changes', 'reject']) {
    const response = await page.request.post(`${data.base}/v1/operations`, {
      headers: {Authorization: `Bearer ${data.agent}`},
      data: {schema_version: 'proofpress/local-operation/v1alpha1', operation: 'claim.propose',
        parameters: {title: `Blocked ${decision}`, statement: `Unsupported ${decision}`, evidence_refs: [], scope: 'browser-test', proposer: 'agent:browser-test'}},
    });
    const proposal = await response.json();
    assert.equal(proposal.ok, true);
    const cid = proposal.result.claim.id;
    await page.goto(`${data.base}/review?claim_id=${cid}&view=full`);
    // A fresh candidate must be evaluated before its state becomes blocked.
    const evaluate = page.getByRole('button', {name: 'Run deterministic checks', exact: true});
    if (await evaluate.count()) await evaluate.click();
    await page.getByRole('heading', {name: 'Approval blocked by failed checks', exact: true}).waitFor();
    assert.equal(await page.getByRole('button', {name: 'Approve', exact: true}).isEnabled(), false);
    assert.equal(await page.getByRole('button', {name: 'Reject', exact: true}).isEnabled(), true);
    assert.equal(await page.getByRole('button', {name: 'Request changes', exact: true}).isEnabled(), true);
    assert.equal(await page.getByRole('button', {name: 'Run optional model review', exact: true}).count(), 0);
    for (const width of [1536, 390]) {
      await page.setViewportSize({width, height: 1024});
      assert.equal(await page.evaluate(() => document.body.scrollWidth), width);
      if (process.env.QA_SCREENSHOTS) {
        await mkdir(process.env.QA_SCREENSHOTS, {recursive: true});
        await page.screenshot({path: `${process.env.QA_SCREENSHOTS}/blocked-review-${width}.png`, fullPage: true});
      }
    }
    await page.setViewportSize({width: 1536, height: 1024});
    await page.getByRole('textbox', {name: 'Decision note, required for rejection or bounded clarification requests'}).fill('Provide bounded evidence and fix the failed checks.');
    const recorded = page.waitForResponse(response => response.url().endsWith('/owner/api/reviews') && response.request().method() === 'POST', {timeout: 20000});
    await page.getByRole('button', {name: decision === 'reject' ? 'Reject' : 'Request changes', exact: true}).click();
    if (decision === 'reject') await page.getByRole('button', {name: 'Confirm rejection', exact: true}).click();
    const receipt = await (await recorded).json();
    assert.equal(receipt.ok, true, JSON.stringify(receipt));
    assert.equal(receipt.result.state, decision === 'reject' ? 'rejected' : 'needs_revision');
    const readback = await (await page.request.get(`${data.base}/owner/api/claims/${cid}`)).json();
    assert.equal(readback.result.state, receipt.result.state);
  }
  assert.deepEqual(errors, []);
  console.log('PASS: blocked claims expose correction decisions, prevent approval, and persist both decisions; desktop/mobile fit');
} finally {
  await browser?.close();
  fixture.stdin.end('\n');
  fixture.kill('SIGTERM');
}
