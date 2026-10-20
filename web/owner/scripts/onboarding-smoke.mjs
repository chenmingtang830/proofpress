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
  await page.getByRole('button',{name:'Issue API key',exact:true}).click();
  await page.getByRole('region',{name:'New credential'}).waitFor();
  assert.ok(await page.locator('.secretReveal .issuedCredentialToken').first().textContent(),'One-time token survives list refresh failure');
  await page.getByText('Synthetic credential list unavailable',{exact:true}).waitFor();
  assert.equal(await page.locator('.secretReveal .agentConnectionInstructions').count(),1);
  // Inspect the issued state itself: the old last-child rule squeezed all
  // connection content into adjacent columns, which disappeared after Done.
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);
  await page.getByRole('button',{name:'Copy key',exact:true}).click();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),await page.locator('.issuedCredentialToken').textContent());
  await page.getByRole('button',{name:'Copy commands',exact:true}).first().click();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),`codex mcp add proofpress --url ${base}/mcp\ncodex mcp login proofpress`);
  for (const width of [1440,1024,768,390]) {
    await page.setViewportSize({width,height:width===390?844:1000});
    const reveal = page.getByRole('region',{name:'New credential'});
    const steps = reveal.locator('.connectionSteps > li');
    assert.equal(await steps.first().evaluate(node=>getComputedStyle(node).listStyleType),'decimal','Connection order remains visible despite CSS resets');
    const boxes = await Promise.all([0,1,2].map(index=>steps.nth(index).boundingBox()));
    assert.ok(boxes[1].y>=boxes[0].y+boxes[0].height && boxes[2].y>=boxes[1].y+boxes[1].height,`Connection steps read vertically at ${width}`);
    const code = reveal.locator('pre code');
    assert.equal(await code.evaluate(node=>getComputedStyle(node).whiteSpace),'pre','Commands preserve terminal lines');
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width,`Issued key has no page overflow at ${width}`);
    if (process.env.QA_SCREENSHOTS) {
      await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
      await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/issued-key-${width}.png`,fullPage:true});
    }
  }
  await page.setViewportSize({width:1440,height:1000});
  await page.unroute('**/v1/owner/credentials');
  await page.unroute('**/owner/api/graph');
  await page.getByRole('button',{name:'Done',exact:true}).click();
  assert.equal(await page.locator('.issuedCredentialToken').count(),0,'Done removes the one-time key from the DOM');
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
  await page.getByRole('tab',{name:'Verification settings',exact:true}).click();
  // Activating this policy is a deliberate human action; no API key or provider consent is needed.
  const policyRequest = page.waitForRequest(request=>request.url().endsWith('/owner/api/review-policy') && request.method()==='POST');
  await page.getByRole('button',{name:'Use manual review',exact:true}).click();
  const submitted=(await policyRequest).postDataJSON();
  assert.equal(submitted.settings.mode,'off');
  assert.equal(submitted.settings.require_judge,false);
  assert.equal(submitted.settings.external_consent,false);
  assert.equal(submitted.settings.auto_admit_new_claims,false);
  await page.getByText('Settings saved.',{exact:true}).waitFor();
  await page.reload();
  await page.getByRole('tab',{name:'Verification settings',exact:true}).click();
  await page.getByRole('switch',{name:'AI-assisted checks',exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Save changes',exact:true}).count(),0,'Unchanged settings need no save action');
  assert.equal(await page.getByRole('button',{name:'Use manual review',exact:true}).count(),0,'Saved manual review needs no activation');
  await page.getByRole('tab',{name:'Knowledge rules',exact:true}).click();
  assert.equal(await page.getByRole('button',{name:'Use manual review',exact:true}).count(),0,'Capture settings have no duplicate verification controls');
  if (process.env.QA_SCREENSHOTS) {
    for (const width of [1440,390]) {
      await page.setViewportSize({width,height:width===390?844:1000});
      await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/knowledge-rules-${width}.png`,fullPage:true});
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width);
    }
  }
  assert.equal(await page.getByRole('alert').count(),0);
  assert.equal(await page.getByRole('heading',{name:'Bring your first finding into Proofpress'}).count(),0,'Configured Admin does not repeat setup');
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);
  await page.getByRole('button',{name:'Copy prompt',exact:true}).click();
  const prompt=await page.evaluate(()=>navigator.clipboard.readText());
  assert.match(prompt,/Ask up to three focused questions/);
  const draft={purpose:'Track evidence-backed market findings.',capture:['Dated market observations','Explicit conditional forecasts'],exclude:['Duplicate findings']};
  const readableDraft='## Purpose\n'+draft.purpose+'\n\n## Capture\n'+draft.capture.map(rule=>'- '+rule).join('\n')+'\n\n## Leave out\n- Duplicate findings';
  await page.getByLabel('Capture rules',{exact:true}).fill(readableDraft);
  assert.equal(await page.getByRole('button',{name:'Load draft for review',exact:true}).count(),0);
  const notSaved=(await (await page.request.get(`${base}/owner/api/capture-policy`)).json()).result;
  assert.equal(notSaved.version,0,'Pasting rules never saves or activates them');
  await page.getByRole('button',{name:'Save capture rules',exact:true}).click();
  await page.getByText('Capture rules v1 saved.',{exact:false}).waitFor();
  await page.reload();
  await page.getByRole('tab',{name:'Knowledge rules',exact:true}).click();
  assert.equal(await page.getByLabel('Capture rules',{exact:true}).inputValue(),readableDraft);
  await page.getByRole('tab',{name:'Verification settings',exact:true}).click();
  assert.equal(await page.getByLabel('API key',{exact:true}).isVisible(),false,'Model configuration is hidden while model advice is off');
  await page.getByRole('switch',{name:'AI-assisted checks',exact:true}).click();
  assert.equal(await page.getByRole('switch',{name:'AI-assisted checks',exact:true}).getAttribute('aria-checked'),'true');
  assert.equal(await page.getByText('Approval options',{exact:true}).count(),0,'Default review does not expose advanced approval options');
  await page.getByText('AI provides an assessment. You make the final approval.',{exact:true}).waitFor();
  assert.equal(await page.getByRole('combobox',{name:'Model advice',exact:true}).count(),0);
  assert.equal(await page.getByRole('checkbox',{name:'Allow external model processing for this workspace',exact:true}).count(),0);
  await page.getByText('By saving, you authorize this processing for this workspace.',{exact:false}).waitFor();
  assert.equal((await (await page.request.get(`${base}/owner/api/review-policy`)).json()).result.settings.external_consent,false,'Opening AI setup does not grant provider consent');
  await page.getByLabel('API key',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Copy prompt',exact:true}).click();
  assert.match(await page.evaluate(()=>navigator.clipboard.readText()),/without JSON/);
  assert.equal(await page.getByLabel('Agent response',{exact:true}).count(),0);
  assert.equal(await page.getByRole('button',{name:'Load for review',exact:true}).count(),0);
  await page.getByLabel('Review criteria',{exact:true}).fill('Require a dated source and state uncertainty.');
  assert.equal(await page.getByLabel('Review criteria',{exact:true}).inputValue(),'Require a dated source and state uncertainty.');
  await page.getByRole('button',{name:'Preview',exact:true}).click();
  await page.getByRole('region',{name:'Review criteria preview',exact:true}).getByText('Require a dated source and state uncertainty.',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Edit',exact:true}).click();
  assert.equal(await page.getByLabel('Review criteria',{exact:true}).inputValue(),'Require a dated source and state uncertainty.');
  await page.getByRole('switch',{name:'AI-assisted checks',exact:true}).click();
  assert.equal(await page.getByLabel('API key',{exact:true}).isVisible(),false);
  assert.equal(await page.getByRole('tab',{name:'Hosting & recovery',exact:true}).count(),0);
  const activeSession=(await (await page.request.get(`${base}/owner/api/session`)).json()).result;
  assert.equal(activeSession.review_policy_configured,true);
  const submittedFinding=nextLine(); fixture.stdin.write('submit\n');
  const {claim_id,capture_version,capture_rules}=await submittedFinding;
  assert.equal(capture_version,1);
  assert.equal(capture_rules,2,'Agent reads both saved capture rules through MCP');
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
