import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import { mkdir } from 'node:fs/promises';
import assert from 'node:assert/strict';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3',[fileURLToPath(new URL('owner-fixture.py',import.meta.url))],{cwd:root,env:{...process.env,PYTHONPATH:`${root}/src`,PROOFPRESS_TEST_JUDGE:'1'},stdio:['pipe','pipe','pipe']});
let diagnostics='';fixture.stderr.on('data',data=>diagnostics+=data);
let browser;
try {
  const data = await new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>reject(new Error('Fixture startup timeout')),20000);
    createInterface({input:fixture.stdout}).once('line',line=>{clearTimeout(timer);resolve(JSON.parse(line));});
    fixture.once('exit',code=>{clearTimeout(timer);reject(new Error(`Fixture failed ${code}: ${diagnostics}`));});
  });
  browser=await chromium.launch();
  const page=await browser.newPage({viewport:{width:1536,height:1024}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  page.on('dialog',()=>{throw new Error('Native dialog must not be used for LM review');});
  await page.goto(`${data.base}/review`);
  await page.locator('input[name=token]').fill(data.owner);
  await Promise.all([page.waitForNavigation(),page.locator('button[type=submit]').click()]);
  const screen=async name=>{if(process.env.QA_SCREENSHOTS){await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/${name}.png`});}};
  await page.goto(`${data.base}/review?conclusion_id=${data.ids[0]}&view=full`);
  await page.getByRole('button',{name:'Run LM review',exact:true}).click();
  await page.getByRole('dialog',{name:'Review evidence with LM'}).waitFor();
  await screen('lm-confirm');
  await page.getByRole('button',{name:'Run LM review',exact:true}).click();
  await page.getByText('Reviewing bound evidence… You can keep reading this conclusion.').waitFor();
  await page.getByText('LM advice recorded. See Checks for the reasoning.').waitFor();
  await page.getByRole('tab',{name:'Checks',exact:true}).click();
  await page.getByText('fixture/offline-judge · judge:fixture',{exact:true}).waitFor();
  await screen('lm-advice');
  assert.equal(await page.getByRole('button',{name:'Approve for reuse',exact:true}).isEnabled(),true);
  // Reproduce the cloud failure shape: an experiment claim bound only to retrieved prose.
  const propose=await page.request.post(`${data.base}/v1/operations`,{headers:{Authorization:`Bearer ${data.agent}`},data:{schema_version:'proofpress/local-operation/v1alpha1',operation:'conclusion.propose',parameters:{statement:'Experiment result without typed metrics',evidence_refs:[],scope:'browser-test',proposer:'agent:fixture'}}});
  const proposal=await propose.json();
  assert.equal(proposal.ok,true);
  const cid=proposal.result.conclusion.id;
  await page.goto(`${data.base}/review?conclusion_id=${cid}&view=full`);
  await page.getByRole('button',{name:'Run deterministic checks',exact:true}).click();
  await page.locator('.shell[aria-busy="false"]').waitFor();
  await page.getByRole('complementary',{name:'Conclusion details'}).getByText(/^blocked$/i).waitFor();
  assert.equal(await page.getByRole('button',{name:'Approve for reuse',exact:true}).count(),0);
  assert.equal(await page.getByRole('button',{name:'Run LM review',exact:true}).count(),0);
  await screen('blocked-before-model-or-human-review');
  await page.goto(`${data.base}/review?conclusion_id=${data.ids[3]}&view=full`);
  await page.getByRole('button',{name:'Run LM review',exact:true}).click();
  await page.getByRole('button',{name:'Run LM review',exact:true}).click();
  await page.getByText('LM review did not complete. You can retry; no approval was recorded.').waitFor();
  await screen('lm-failed');
  await page.getByRole('button',{name:'Admin',exact:true}).click();
  await page.getByRole('heading',{name:'Judge & policy',exact:true}).waitFor();
  await page.waitForTimeout(300);
  await screen('admin-policy-loading');
  const policyResponse=await page.request.get(`${data.base}/owner/api/review-policy`);
  assert.equal(policyResponse.status(),200);
  assert.ok((await policyResponse.json()).result.settings);
  await page.getByLabel('LM review',{exact:true}).selectOption('off');
  await page.getByRole('button',{name:'Save & activate',exact:true}).click();
  await page.getByText('Policy v1 is active',{exact:true}).waitFor();
  await page.reload();
  assert.equal(await page.getByLabel('LM review',{exact:true}).inputValue(),'off');
  for(const width of [1536,1024,390]) {
    await page.setViewportSize({width,height:1024});await screen(`admin-policy-${width}`);
    assert.equal(await page.evaluate(()=>document.body.scrollWidth),width);
  }
  await page.setViewportSize({width:1536,height:1024});
  await page.getByRole('button',{name:'Activity',exact:true}).click();
  await page.getByText('Updated review policy',{exact:true}).waitFor();
  await screen('semantic-activity');
  await page.getByRole('button',{name:'Technical logs',exact:true}).click();
  await page.getByRole('columnheader',{name:'Operation',exact:true}).waitFor();
  await screen('technical-logs');
  assert.deepEqual(errors,[]);
  console.log('PASS: offline LM dialog, success, failure, blocked approval, persistent policy, semantic activity and responsive admin');
} finally {await browser?.close();fixture.stdin.end('\n');fixture.kill('SIGTERM');}
