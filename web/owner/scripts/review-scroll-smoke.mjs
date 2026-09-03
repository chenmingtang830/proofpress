import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3', [fileURLToPath(new URL('owner-fixture.py', import.meta.url))], {
  cwd: root, env: {...process.env, PYTHONPATH: `${root}/src`}, stdio: ['pipe','pipe','pipe'],
});
let browser;
try {
  const data = await new Promise((resolve,reject) => {
    const timer=setTimeout(()=>reject(new Error('Fixture startup timed out')),20000);
    createInterface({input:fixture.stdout}).once('line',line=>{clearTimeout(timer);resolve(JSON.parse(line));});
  });
  const operation = async (operation, parameters) => {
    const response = await fetch(`${data.base}/v1/operations`, {method:'POST', headers:{Authorization:`Bearer ${data.agent}`,'Content-Type':'application/json'}, body:JSON.stringify({schema_version:'proofpress/local-operation/v1alpha1',operation,parameters})});
    const body=await response.json(); assert.equal(body.ok,true,JSON.stringify(body)); return body.result;
  };
  const original = await operation('review.receipt',{conclusion_id:data.ids[0]});
  const ids=[];
  for(let i=0;i<24;i++) {
    const proposal=await operation('conclusion.propose',{statement:`Scroll regression candidate ${String(i+1).padStart(2,'0')}: inspector remains visible.`,evidence_refs:original.conclusion.evidence_refs,scope:'browser-test',proposer:'agent:browser-test'});
    ids.push(proposal.conclusion.id);
  }
  browser=await chromium.launch();
  const page=await browser.newPage({viewport:{width:1280,height:560}});
  await page.goto(`${data.base}/review`);
  await page.locator('input[name=token]').fill(data.owner);
  await Promise.all([page.waitForNavigation(),page.locator('button[type=submit]').click()]);
  await page.locator('tbody tr').filter({hasText:'Scroll regression candidate 24'}).waitFor();
  await page.locator('.shell[aria-busy="false"]').waitFor();
  const work=page.locator('.reviewWorkspace > .work');
  const inspector=page.locator('.reviewWorkspace > .inspector');
  assert.equal(await work.evaluate(el=>el.scrollHeight>el.clientHeight),true,'Review queue must have its own scrollbar');
  await work.evaluate(el=>{el.scrollTop=el.scrollHeight;});
  await page.locator('tbody tr').filter({hasText:'Scroll regression candidate 24'}).click();
  await inspector.locator('h2').filter({hasText:'Scroll regression candidate 24'}).waitFor();
  assert.ok((await inspector.boundingBox()).y < 80,'Inspector must stay pinned beside the scrolled queue');
  await inspector.evaluate(el=>{el.scrollTop=200;});
  await page.locator('tbody tr').filter({hasText:'Scroll regression candidate 23'}).click();
  await inspector.locator('h2').filter({hasText:'Scroll regression candidate 23'}).waitFor();
  assert.equal(await inspector.evaluate(el=>el.scrollTop),0,'A new selection must reset inspector scroll');
  console.log('PASS review queue and inspector scroll independently; low-row selection remains visible and resets details.');
} finally {
  await browser?.close();
  fixture.stdin.end('\n');
}
