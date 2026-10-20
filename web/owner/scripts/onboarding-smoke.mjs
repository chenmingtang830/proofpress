import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { once } from 'node:events';
import { fileURLToPath } from 'node:url';
import { mkdir } from 'node:fs/promises';
import { chromium } from 'playwright';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3', [fileURLToPath(new URL('onboarding-fixture.py', import.meta.url))], {
  cwd:root, env:{...process.env,PYTHONPATH:`${root}/src`}, stdio:['pipe','pipe','pipe'],
});
let diagnostics = '';
fixture.stderr.on('data', chunk => { diagnostics += chunk; });
const lines = createInterface({input:fixture.stdout});
const nextLine = async () => JSON.parse((await Promise.race([
  once(lines, 'line'),
  once(fixture, 'exit').then(([code]) => {throw new Error(`Fixture exited ${code}: ${diagnostics}`);}),
  new Promise((_, reject) => {const timer=setTimeout(()=>reject(new Error('Fixture timed out')),20000);timer.unref();}),
]))[0]);
let browser;
try {
  const {base} = await nextLine();
  browser = await chromium.launch();
  const page = await browser.newPage({viewport:{width:1440,height:1000}});
  page.setDefaultTimeout(12000);
  const errors=[]; page.on('pageerror', error => errors.push(error.message));
  await page.goto(`${base}/home`);
  await page.getByRole('heading',{name:'Bring your first finding into Proofpress'}).waitFor();
  assert.equal(await page.getByRole('alert').count(),0,'Fresh workspace is a setup state, not a failure');
  const session = (await (await page.request.get(`${base}/owner/api/session`)).json()).result;
  assert.equal(session.review_policy_configured,false);
  assert.ok(session.csrf);
  const graph = await page.request.get(`${base}/owner/api/graph`);
  assert.equal((await graph.json()).error.code,'workspace_policy_missing','Backend gate remains enforced');
  // A background graph failure must not remove the owner identity or prevent issuance.
  await page.route('**/owner/api/graph', route=>route.fulfill({status:503,json:{ok:false,error:{message:'Synthetic graph unavailable'}}}));
  await page.getByRole('button',{name:'Create agent credential',exact:true}).click();
  await page.getByLabel('Agent identity',{exact:true}).fill('agent:onboarding-codex');
  await page.getByLabel('Key name',{exact:true}).fill('Synthetic Codex');
  // Fail list refresh only after the successful POST has committed.
  await page.route('**/v1/owner/credentials', async route => {
    if (route.request().method()==='POST') {
      const response=await route.fetch();
      await route.fulfill({response});
    } else await route.fulfill({status:503,json:{ok:false,error:{message:'Synthetic credential list unavailable'}}});
  });
  await page.getByRole('button',{name:'Issue agent credential',exact:true}).click();
  await page.getByRole('region',{name:'New credential'}).waitFor();
  assert.ok(await page.locator('.secretReveal .issuedCredentialToken').first().textContent(),'One-time token survives list refresh failure');
  await page.getByText('Synthetic credential list unavailable',{exact:true}).waitFor();
  assert.equal(await page.locator('.secretReveal .agentConnectionInstructions').count(),1);
  await page.unroute('**/v1/owner/credentials');
  await page.unroute('**/owner/api/graph');
  await page.getByRole('button',{name:'Done',exact:true}).click();
  await page.getByRole('button',{name:'Reload credentials',exact:true}).click();
  assert.equal(await page.getByRole('alert').count(),0);
  for (const width of [1440,390]) {
    await page.setViewportSize({width,height:width===390?844:1000});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width,`No onboarding overflow at ${width}`);
    if (process.env.QA_SCREENSHOTS) {
      await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
      await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/onboarding-admin-${width}.png`,fullPage:true});
    }
  }
  // Activating this policy is a deliberate human action; no API key or provider consent is needed.
  const policyRequest = page.waitForRequest(request=>request.url().endsWith('/owner/api/review-policy') && request.method()==='POST');
  await page.getByRole('button',{name:'Use human review',exact:true}).click();
  const submitted=(await policyRequest).postDataJSON();
  assert.equal(submitted.settings.mode,'off');
  assert.equal(submitted.settings.require_judge,false);
  assert.equal(submitted.settings.external_consent,false);
  assert.equal(submitted.settings.auto_admit_new_claims,false);
  await page.getByText('Policy v1 is active',{exact:true}).waitFor();
  await page.reload();
  await page.getByText('Policy v1',{exact:true}).waitFor();
  assert.equal(await page.getByRole('alert').count(),0);
  assert.equal(await page.getByRole('heading',{name:'Bring your first finding into Proofpress'}).count(),0,'Configured Admin does not repeat setup');
  const activeSession=(await (await page.request.get(`${base}/owner/api/session`)).json()).result;
  assert.equal(activeSession.review_policy_configured,true);
  const submittedFinding=nextLine(); fixture.stdin.write('submit\n');
  const {claim_id}=await submittedFinding;
  await page.goto(`${base}/review?claim_id=${claim_id}&view=full`);
  await page.getByRole('button',{name:'Approve',exact:true}).click();
  await page.getByRole('dialog').getByRole('button',{name:'Confirm approval',exact:true}).click();
  await page.getByRole('heading',{name:'Approval recorded',exact:true}).waitFor();
  const reuse=nextLine(); fixture.stdin.write('reuse\n');
  assert.equal((await reuse).governed_count,1,'Successor retrieves the human-approved finding');
  assert.deepEqual(errors,[]);
  console.log('PASS: fresh workspace → credential despite refresh failure → explicit human policy → review → successor reuse; desktop/mobile.');
} finally {
  await browser?.close(); fixture.stdin.end(); fixture.kill('SIGTERM'); lines.close();
}
