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
  page.setDefaultTimeout(15000);
  page.on('dialog',dialog=>dialog.accept());
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`${data.base}/review?conclusion_id=${data.ids[0]}`);
  await page.locator('input[name=token]').fill(data.owner);
  await Promise.all([page.waitForNavigation(),page.locator('button[type=submit]').click()]);
  await page.locator('tbody tr').filter({hasText:data.ids[0]}).click();
  await page.getByRole('button',{name:'View details',exact:true}).click();
  await page.locator('.evidenceRow > p').filter({hasText:'Browser fixture approve:'}).waitFor();
  for(const tab of ['Checks','History','Evidence']) await page.getByRole('tab',{name:tab,exact:true}).click();
  if(process.env.QA_SCREENSHOTS) {
    await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
    await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/review.png`});
  }
  await page.getByRole('button',{name:'Approve',exact:true}).click();
  await page.getByText('Decision recorded',{exact:true}).waitFor();
  await page.getByRole('button',{name:'Ledger',exact:true}).click();
  await page.getByRole('button',{name:'Current knowledge',exact:true}).click();
  await page.locator('tbody tr').filter({hasText:data.ids[0]}).waitFor();
  assert.equal(await page.locator('tbody tr').count(),1);
  assert.equal(await page.getByRole('textbox',{name:'Ledger scope'}).count(),0);
  await page.getByRole('button',{name:'Lineage',exact:true}).click();
  await page.locator('.conclusionNode').filter({hasText:'fixture approve:'}).click();
  await page.getByText('Available to your owner identity',{exact:true}).waitFor();
  assert.equal(await page.locator('.lineageFlow .technicalDetails').count(),0);
  await page.getByRole('button',{name:'Expand 1 evidence',exact:true}).click();
  await page.locator('.lineageFlow .technicalDetails').waitFor();
  await page.getByRole('button',{name:'Back to overview',exact:true}).click();
  await page.getByRole('checkbox',{name:'Show history and unavailable conclusions'}).check();
  assert.equal(await page.locator('.conclusionNode').count(),3);
  if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/lineage-overview.png`});
  await page.locator('.conclusionNode').filter({hasText:'fixture reject:'}).click();
  await page.locator('.lineageFlow').getByText('Excluded from current context',{exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Approve',exact:true}).count(),0);
  await page.getByRole('checkbox',{name:'Show history and unavailable conclusions'}).uncheck();
  assert.equal(await page.locator('.conclusionNode').count(),1);
  await page.locator('.conclusionNode').filter({hasText:'fixture approve:'}).click();
  await page.getByText('Available to your owner identity',{exact:true}).waitFor();
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
  await page.getByRole('button',{name:'Reject',exact:true}).click();
  await page.getByText('Decision recorded',{exact:true}).waitFor();
  await page.waitForLoadState('networkidle');
  await page.locator('.shell[aria-busy="false"]').waitFor();
  await page.locator('tbody tr').filter({hasText:data.ids[2]}).click();
  await page.locator('.inspector h2').filter({hasText:'fixture clarify:'}).waitFor();
  await page.getByRole('button',{name:'Request changes',exact:true}).click();
  await page.getByText('Describe the bounded change',{exact:false}).waitFor();
  await page.locator('.decision textarea').fill('Verify this bounded assertion.');
  await page.getByRole('button',{name:'Request changes',exact:true}).click();
  await page.getByText('Decision recorded',{exact:true}).waitFor();
  const context = await page.request.post(`${data.base}/v1/operations`,{headers:{Authorization:`Bearer ${data.agent}`},data:{schema_version:'proofpress/local-operation/v1alpha1',operation:'context.get',parameters:{scope:'browser-test'}}});
  const projected=await context.json();
  assert.equal(projected.ok,true,JSON.stringify(projected));
  assert.deepEqual(projected.result.knowledge.map(r=>r.id),[data.ids[0]]);
  for(const name of ['Home','Review','Ledger','Activity','Admin']) {
    await page.getByRole('button',{name,exact:true}).click();
    await page.locator('h1').waitFor();
  }
  await page.locator('.issueForm input').nth(0).fill('agent:temporary-browser');
  await page.locator('.issueForm input').nth(1).fill('Temporary browser credential');
  await page.getByRole('button',{name:'Issue credential',exact:true}).click();
  await page.locator('.secretReveal code').waitFor();
  const token=await page.locator('.secretReveal code').textContent();
  assert.equal((await page.request.get(`${data.base}/v1/capabilities`,{headers:{Authorization:`Bearer ${token}`}})).status(),200);
  await page.getByRole('button',{name:'Done',exact:true}).click();
  const credential=page.locator('.credentialList > div').filter({hasText:'Temporary browser credential'});
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
  for(const width of [1536,1024,390]) {
    await page.setViewportSize({width,height:900});
    assert.equal(await page.evaluate(()=>document.body.scrollWidth),width);
    if(process.env.QA_SCREENSHOTS) {
      await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
      await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/home-${width}.png`});
    }
  }
  assert.deepEqual(errors,[]);
  console.log('PASS isolated real browser: evidence quote, tabs, approve/reject/request changes submission, canonical scope projection, successor read, selection race/error safety, navigation, credential issue/rotate/revoke, responsive Home. No production data or model calls.');
} finally {
  await browser?.close();
  fixture.stdin.end('\n');
}
