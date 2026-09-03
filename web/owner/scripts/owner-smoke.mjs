import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3', [fileURLToPath(new URL('owner-fixture.py', import.meta.url))], {
  cwd: root, env: {...process.env, PYTHONPATH: `${root}/src`}, stdio: ['pipe','pipe','pipe'],
});
let diagnostics = '';
fixture.stderr.on('data', c => { diagnostics += c; });
let browser;
try {
  const data = await new Promise((resolve,reject) => {
    const timer=setTimeout(()=>reject(new Error('Fixture startup timed out')),20000);
    createInterface({input:fixture.stdout}).once('line',line=>{clearTimeout(timer);resolve(JSON.parse(line));});
    fixture.once('exit',code=>{clearTimeout(timer);reject(new Error(`Fixture exited ${code}: ${diagnostics}`));});
  });
  browser = await chromium.launch();
  const page = await browser.newPage({viewport:{width:1536,height:1024}});
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);
  page.setDefaultTimeout(15000);
  page.on('dialog',dialog=>dialog.accept());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`${data.base}/review?conclusion_id=${data.ids[0]}`);
  await page.locator('input[name=token]').fill(data.owner);
  await Promise.all([page.waitForNavigation(),page.locator('button[type=submit]').click()]);
  assert.equal((await page.request.get(`${data.base}/logo.svg`)).status(),200);
  await page.waitForFunction(()=>[...document.querySelectorAll('.brandMark img')].every(img=>img.complete && img.naturalWidth>0));
  for (const width of [1024,390]) {
    await page.setViewportSize({width,height:900});
    await page.getByRole('button',{name:'Close details',exact:true}).click();
    assert.equal(await page.locator('.inspector').count(),0);
    const opener = page.locator('tbody tr').filter({hasText:data.ids[0]}).getByRole('button');
    await opener.focus();
    await opener.press('Enter');
    await page.locator('.inspector h2').waitFor();
    assert.equal(await page.getByRole('button',{name:'Close details',exact:true}).evaluate(el=>document.activeElement===el),true);
    assert.equal(await page.locator('.work').isVisible(),false);
    await page.getByRole('button',{name:'Open full review',exact:true}).click();
    await page.getByRole('button',{name:'Approve',exact:true}).scrollIntoViewIfNeeded();
    assert.equal(await page.evaluate(()=>document.body.scrollWidth),width);
    if(process.env.QA_SCREENSHOTS) {
      await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
      await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/review-long-${width}.png`});
    }
    await page.getByRole('button',{name:'Back to review',exact:true}).click();
    await page.getByRole('button',{name:'Close details',exact:true}).press('Escape');
    await page.waitForFunction(()=>document.activeElement?.classList.contains('conclusionSelect'));
    await opener.click();
  }
  await page.setViewportSize({width:1536,height:1024});
  await page.locator('tbody tr').filter({hasText:data.ids[0]}).click();
  await page.getByRole('button',{name:'Open full review',exact:true}).click();
  assert.match(page.url(), /view=full/);
  await page.reload();
  await page.locator('.evidenceRow > p').filter({hasText:'Browser fixture approve:'}).waitFor();
  for(const tab of ['Checks','History','Evidence']) await page.getByRole('tab',{name:tab,exact:true}).click();
  if(process.env.QA_SCREENSHOTS) {
    await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
    await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/review.png`});
  }
  await page.getByRole('button',{name:'Approve',exact:true}).click();
  await page.getByRole('dialog',{name:'Approve this conclusion?'}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Cancel',exact:true}).evaluate(el=>document.activeElement===el),true);
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/approval-dialog.png`});
  await page.getByRole('button',{name:'Cancel',exact:true}).click();
  await page.waitForFunction(()=>document.activeElement?.textContent === 'Approve');
  assert.equal(await page.getByRole('button',{name:'Approve',exact:true}).evaluate(el=>document.activeElement===el),true);
  assert.equal(await page.getByText('Decision recorded',{exact:true}).count(),0);
  await page.setViewportSize({width:390,height:844});
  await page.getByRole('button',{name:'Approve',exact:true}).click();
  assert.equal(await page.evaluate(()=>document.body.scrollWidth),390);
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/approval-dialog-mobile.png`});
  await page.getByRole('button',{name:'Cancel',exact:true}).press('Escape');
  assert.equal(await page.getByRole('dialog').count(),0);
  await page.setViewportSize({width:1536,height:1024});
  await page.getByRole('button',{name:'Approve',exact:true}).click();
  await page.getByRole('button',{name:'Confirm approval',exact:true}).click();
  await page.getByText('Approved for reuse',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Ledger',exact:true}).click();
  const tabGeometry = () => page.locator('.ledgerViews button').evaluateAll(nodes=>nodes.map(el=>{const r=el.getBoundingClientRect(); const s=getComputedStyle(el);return {x:r.x,y:r.y,width:r.width,height:r.height,weight:s.fontWeight};}));
  const beforeTab = await tabGeometry();
  await page.getByRole('button',{name:'Current knowledge',exact:true}).click();
  assert.deepEqual(await tabGeometry(),beforeTab,'Tab geometry and weight must not change on selection');
  await page.locator('tbody tr').filter({hasText:data.ids[0]}).waitFor();
  assert.equal(await page.locator('tbody tr').count(),1);
  assert.equal(await page.getByRole('textbox',{name:'Ledger scope'}).count(),0);
  await page.getByRole('button',{name:'Lineage',exact:true}).click();
  await page.locator('.conclusionNode').filter({hasText:'fixture approve:'}).click();
  await page.locator('.graphNode').getByText('Scope: browser-test',{exact:true}).waitFor();
  assert.equal(await page.locator('.graphPlane .technicalDetails').count(),0);
  await page.locator('.graphNode.evidence').first().click();
  await page.locator('.graphInspector .technicalDetails').waitFor();
  await page.getByRole('button',{name:'Back to overview',exact:true}).click();
  assert.equal(await page.locator('.inspector').count(),0);
  await page.setViewportSize({width:390,height:900});
  await page.locator('.mobileConclusion').filter({hasText:'fixture approve:'}).waitFor();
  assert.equal(await page.locator('.globalGraph').isVisible(),false);
  await page.getByRole('button',{name:'Explore graph',exact:true}).click();
  assert.equal(await page.locator('.globalGraph').isVisible(),true);
  await page.getByRole('button',{name:'Conclusion list',exact:true}).click();
  await page.locator('.mobileConclusion').filter({hasText:'fixture approve:'}).click();
  await page.getByRole('button',{name:'Close details',exact:true}).click();
  assert.equal(await page.locator('.inspector').count(),0);
  await page.setViewportSize({width:1536,height:1024});
  await page.getByRole('checkbox',{name:'Show history and unavailable conclusions'}).check();
  assert.equal(await page.locator('.conclusionNode').count(),3);
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/lineage-overview.png`});
  await page.locator('.conclusionNode').filter({hasText:'fixture reject:'}).click();
  await page.locator('.graphNode').getByText('Not reusable: needs review',{exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Approve',exact:true}).count(),0);
  await page.getByRole('checkbox',{name:'Show history and unavailable conclusions'}).uncheck();
  assert.equal(await page.locator('.conclusionNode').count(),1);
  await page.locator('.conclusionNode').filter({hasText:'fixture approve:'}).click();
  await page.locator('.graphNode').getByText('Scope: browser-test',{exact:true}).waitFor();
  await page.locator('.graphNode.evidence').first().click();
  await page.getByRole('complementary',{name:'Selected node details'}).getByText('fixture://approve',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Back to conclusion',exact:true}).click();
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/lineage.png`});
  await page.getByRole('button',{name:'Review',exact:true}).click();
  assert.equal(await page.locator('tbody tr').filter({hasText:data.ids[0]}).count(),0);
  await page.route(`**/owner/api/conclusions/${data.ids[1]}`, async route => {
    const response = await route.fetch();
    await new Promise(resolve=>setTimeout(resolve,250));
    await route.fulfill({response});
  });
  await page.locator('tbody tr').filter({hasText:data.ids[1]}).click();
  await page.locator('tbody tr').filter({hasText:data.ids[2]}).click();
  await page.locator('.inspector h2').filter({hasText:'fixture clarify:'}).waitFor();
  await page.waitForLoadState('networkidle');
  assert.match(await page.locator('.inspector h2').textContent(),/fixture clarify:/);
  await page.unroute(`**/owner/api/conclusions/${data.ids[1]}`);
  await page.route(`**/owner/api/conclusions/${data.ids[1]}`,route=>route.fulfill({status:503,json:{ok:false,error:{message:'Fixture unavailable; retry.'}}}));
  await page.locator('tbody tr').filter({hasText:data.ids[1]}).click();
  await page.getByText('Fixture unavailable; retry.',{exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Approve',exact:true}).count(),0);
  await page.unroute(`**/owner/api/conclusions/${data.ids[1]}`);
  await page.locator('tbody tr').filter({hasText:data.ids[1]}).click();
  await page.getByRole('button',{name:'Open full review',exact:true}).click();
  await page.getByRole('button',{name:'Reject',exact:true}).click();
  await page.getByRole('button',{name:'Confirm rejection',exact:true}).click();
  await page.locator('.decisionNotice').getByText('Rejected',{exact:true}).waitFor();
  await page.waitForLoadState('networkidle');
  await page.locator('.shell[aria-busy="false"]').waitFor();
  await page.getByRole('button',{name:'Back to review',exact:true}).click();
  await page.getByRole('button',{name:'Needs review',exact:true}).click();
  assert.equal(await page.getByRole('complementary',{name:'Conclusion details'}).count(),0);
  await page.locator('tbody tr').filter({hasText:data.ids[2]}).click();
  await page.locator('.inspector h2').filter({hasText:'fixture clarify:'}).waitFor();
  await page.getByRole('button',{name:'Open full review',exact:true}).click();
  await page.getByRole('button',{name:'Request changes',exact:true}).click();
  await page.getByText('Describe the bounded change',{exact:false}).waitFor();
  await page.locator('.decision textarea').fill('Verify this bounded assertion.');
  await page.getByRole('button',{name:'Request changes',exact:true}).click();
  const handoffDialog = page.getByRole('dialog');
  await handoffDialog.getByRole('heading',{name:'Changes requested',exact:true}).waitFor();
  await handoffDialog.getByText('Copied to clipboard. Paste into your agent.',{exact:true}).waitFor();
  assert.equal(await handoffDialog.getByRole('button',{name:'Copy instructions for agent'}).count(),0);
  assert.match(await page.evaluate(() => navigator.clipboard.readText()),/revision_request_ref/);
  if(process.env.QA_SCREENSHOTS) {
    await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/revision-handoff.png`});
    await page.setViewportSize({width:390,height:844});
    await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/revision-handoff-mobile.png`});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth),false);
    await page.setViewportSize({width:1440,height:1000});
  }
  await handoffDialog.getByRole('status').waitFor();
  await handoffDialog.getByRole('button',{name:'View revision request'}).click();
  await page.locator('.inspector > .decisionNotice').getByText('Changes requested',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Back to review',exact:true}).click();
  await page.getByRole('button',{name:'Copy instructions for agent',exact:true}).waitFor();
  await page.getByRole('button',{name:'View revision request',exact:true}).click();
  await page.evaluate(() => { window.savedClipboardWrite = navigator.clipboard.writeText.bind(navigator.clipboard); navigator.clipboard.writeText = async () => { throw new Error('Test clipboard denial'); }; });
  await page.getByRole('button',{name:'Copy instructions for agent',exact:true}).click();
  await page.getByRole('button',{name:'Select instructions',exact:true}).click();
  assert.equal(await page.getByRole('textbox',{name:'Revision instructions'}).evaluate(el => el.selectionEnd === el.value.length),true);
  await page.evaluate(() => { navigator.clipboard.writeText = window.savedClipboardWrite; delete window.savedClipboardWrite; });
  const context = await page.request.post(`${data.base}/v1/operations`,{headers:{Authorization:`Bearer ${data.agent}`},data:{schema_version:'proofpress/local-operation/v1alpha1',operation:'context.get',parameters:{scope:'browser-test'}}});
  const projected=await context.json();
  assert.equal(projected.ok,true,JSON.stringify(projected));
  assert.deepEqual(projected.result.knowledge.map(r=>r.id),[data.ids[0]]);
  const originalReceipt = await (await page.request.get(`${data.base}/owner/api/conclusions/${data.ids[2]}`)).json();
  const original = originalReceipt.result;
  const operation = async (operation,parameters) => {
    const response = await page.request.post(`${data.base}/v1/operations`,{headers:{Authorization:`Bearer ${data.agent}`},data:{schema_version:'proofpress/local-operation/v1alpha1',operation,parameters}});
    const body = await response.json(); assert.equal(body.ok,true,JSON.stringify(body)); return body.result;
  };
  const revision = await operation('conclusion.propose',{statement:'Revised finding: evidence supports population A only.',evidence_refs:original.conclusion.evidence_refs,scope:'browser-test',proposer:'agent:browser-test',qualifiers:{revision_of:data.ids[2],revision_request_ref:original.revision_request.event_id}});
  await operation('conclusion.evaluate',{conclusion_id:revision.conclusion.id});
  await page.reload();
  await page.getByRole('heading',{name:'Requested change',exact:true}).waitFor();
  assert.equal(await page.getByText('Waiting for a new proposal.',{exact:true}).count(),0);
  await page.getByRole('button',{name:/Revised finding: evidence supports population A only/}).click();
  await page.getByRole('heading',{name:'Revision of previous conclusion',exact:true}).waitFor();
  await page.getByRole('button',{name:'Approve',exact:true}).click();
  await page.getByRole('button',{name:'Confirm approval',exact:true}).click();
  await page.getByText('Approved for reuse',{exact:true}).waitFor();
  const revisedContext = await operation('context.get',{scope:'browser-test'});
  assert.deepEqual(new Set(revisedContext.knowledge.map(row=>row.id)),new Set([data.ids[0],revision.conclusion.id]));
  for(const name of ['Home','Review','Ledger','Activity','Admin']) {
    await page.getByRole('button',{name,exact:true}).click();
    await page.locator('h1').waitFor();
  }
  await page.goBack();
  await page.getByRole('heading',{name:'Activity',exact:true}).waitFor();
  for (const [operation,parameters,code] of [
    ['conclusion.review',{conclusion_id:data.ids[0],decision:'admit'},'operation_forbidden'],
    ['conclusion.review',{conclusion_id:data.ids[0],decision:'admit',expected_head:'deliberately-stale'},'ledger_head_conflict'],
  ]) {
    const response = await page.request.post(`${data.base}/v1/operations`,{headers:{Authorization:`Bearer ${code === 'ledger_head_conflict' ? data.owner : data.agent}`},data:{schema_version:'proofpress/local-operation/v1alpha1',operation,parameters}});
    assert.equal((await response.json()).error.code,code);
  }
  await page.reload();
  await page.getByText('operation_forbidden',{exact:true}).waitFor();
  await page.getByText('ledger_head_conflict',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Important events',exact:true}).click();
  await page.getByText('operation_forbidden',{exact:true}).waitFor();
  assert.equal(await page.locator('tbody tr').filter({hasText:'graph · get'}).count(),0);
  await page.getByRole('button',{name:'All activity',exact:true}).click();
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/activity-outcomes.png`});
  for(const name of ['Time','Operation','Actor','Result']) assert.equal(await page.getByRole('columnheader',{name,exact:true}).count(),1);
  await page.goForward();
  await page.getByRole('heading',{name:'Admin',exact:true}).waitFor();
  const controlTops = await page.locator('.issueForm input, .issueForm > button').evaluateAll(nodes=>nodes.map(el=>el.getBoundingClientRect().top));
  assert.ok(Math.max(...controlTops)-Math.min(...controlTops)<=1,'Admin controls must align');
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/admin-aligned.png`});
  await page.locator('.issueForm input').nth(0).fill('agent:temporary-browser');
  await page.locator('.issueForm input').nth(1).fill('Temporary browser credential');
  await page.getByRole('button',{name:'Issue credential',exact:true}).click();
  await page.locator('.secretReveal code').waitFor();
  const token=await page.locator('.secretReveal code').textContent();
  assert.equal((await page.request.get(`${data.base}/v1/capabilities`,{headers:{Authorization:`Bearer ${token}`}})).status(),200);
  await page.getByRole('button',{name:'Done',exact:true}).click();
  const credential=page.locator('.credentialList > div').filter({hasText:'Temporary browser credential'});
  await page.reload();
  await credential.waitFor();
  await page.setViewportSize({width:390,height:900});
  assert.equal(await credential.getByRole('button',{name:'Rotate',exact:true}).isVisible(),true);
  assert.equal(await credential.getByRole('button',{name:'Revoke',exact:true}).isVisible(),true);
  await page.getByRole('textbox',{name:'Agent identity',exact:true}).focus();
  assert.notEqual(await page.getByRole('textbox',{name:'Agent identity',exact:true}).evaluate(el=>getComputedStyle(el).outlineStyle),'none');
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/admin-mobile.png`});
  await credential.getByRole('button',{name:'Rotate',exact:true}).click();
  await page.locator('.secretReveal code').waitFor();
  const rotated=await page.locator('.secretReveal code').textContent();
  assert.notEqual(rotated,token);
  assert.equal((await page.request.get(`${data.base}/v1/capabilities`,{headers:{Authorization:`Bearer ${token}`}})).status(),401);
  assert.equal((await page.request.get(`${data.base}/v1/capabilities`,{headers:{Authorization:`Bearer ${rotated}`}})).status(),200);
  await page.getByRole('button',{name:'Done',exact:true}).click();
  const activeCredential=page.locator('.credentialList > div').filter({hasText:'agent:temporary-browser'}).filter({has:page.getByRole('button',{name:'Revoke',exact:true})});
  await Promise.all([
    page.waitForResponse(r=>r.url().endsWith('/v1/owner/credentials') && r.request().method()==='POST'),
    activeCredential.getByRole('button',{name:'Revoke',exact:true}).click(),
  ]);
  await page.waitForLoadState('networkidle');
  assert.equal((await page.request.get(`${data.base}/v1/capabilities`,{headers:{Authorization:`Bearer ${rotated}`}})).status(),401);
  await page.getByRole('button',{name:'Home',exact:true}).click();
  assert.equal(await page.getByText('Ask Proofpress',{exact:true}).count(),0);
  assert.equal(await page.getByRole('textbox',{name:'Search conclusions'}).count(),0);
  for (const width of [1536,1024,390]) {
    await page.setViewportSize({width,height:1024});
    for (const name of ['Home','Review','Ledger','Activity','Admin']) {
      await page.getByRole('button',{name,exact:true}).click();
      await page.locator('h1').waitFor();
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width,`${name} overflow at ${width}`);
      if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/audit-${name}-${width}.png`,fullPage:true});
    }
  }
  await page.getByRole('button',{name:'Home',exact:true}).click();
  for(const width of [1536,1024,390]) {
    await page.setViewportSize({width,height:900});
    assert.equal(await page.evaluate(()=>document.body.scrollWidth),width);
    if(process.env.QA_SCREENSHOTS) {
      await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
      await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/home-${width}.png`});
    }
  }
  await page.setViewportSize({width:1280,height:900});
  await page.route('**/owner/api/context?*',route=>route.fulfill({status:503,json:{error:'Context unavailable'}}));
  await page.goto(`${data.base}/ledger`);
  await page.getByRole('button',{name:'Current knowledge',exact:true}).click();
  await page.getByText('Current knowledge could not be loaded.',{exact:false}).waitFor();
  assert.equal(await page.locator('.conclusionNode').count(),0);
  await page.unroute('**/owner/api/context?*');
  await page.getByRole('button',{name:'Reload workspace',exact:true}).click();
  await page.getByRole('button',{name:'Lineage',exact:true}).click();
  await page.locator('.conclusionNode').filter({hasText:'fixture approve:'}).waitFor();
  await page.route(`**/owner/api/conclusions/${data.ids[0]}`,route=>route.fulfill({status:503,json:{error:'Detail unavailable'}}));
  await page.locator('.conclusionNode').filter({hasText:'fixture approve:'}).click();
  await page.getByRole('button',{name:'Retry details',exact:true}).waitFor();
  assert.equal(await page.locator('.inspector').count(),0);
  await page.unroute(`**/owner/api/conclusions/${data.ids[0]}`);
  await page.getByRole('button',{name:'Retry details',exact:true}).click();
  await page.locator('.inspector h2').waitFor();
  await page.route('**/owner/api/graph',route=>route.fulfill({status:401,json:{error:'owner_session_required'}}));
  await page.goto(`${data.base}/review`);
  await page.getByRole('link',{name:'Sign in again',exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Approve',exact:true}).count(),0);
  await page.unroute('**/owner/api/graph');
  await page.getByRole('link',{name:'Sign in again',exact:true}).click();
  await page.locator('.shell[aria-busy="false"]').waitFor();
  assert.equal(await page.getByRole('link',{name:'Sign in again',exact:true}).count(),0);
  await page.getByRole('button',{name:'Activity',exact:true}).click();
  await page.getByRole('columnheader',{name:'Operation',exact:true}).waitFor();
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/activity-columns.png`});
  assert.deepEqual(errors,[]);
  console.log('PASS isolated real browser: evidence quote, tabs, approve/reject/request changes submission, canonical scope projection, successor read, selection race/error safety, navigation, credential issue/rotate/revoke, responsive Home. No production data or model calls.');
} finally {
  await browser?.close();
  fixture.stdin.end('\n');
}
