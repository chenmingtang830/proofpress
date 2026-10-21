import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
import {once} from 'node:events';
import {fileURLToPath} from 'node:url';
import {mkdir} from 'node:fs/promises';
import {chromium} from 'playwright';

const root=fileURLToPath(new URL('../../../',import.meta.url));
const fixture=spawn(process.env.PYTHON || 'python3',[fileURLToPath(new URL('onboarding-fixture.py',import.meta.url))],{
  cwd:root,env:{...process.env,PYTHONPATH:`${root}/src`},stdio:['pipe','pipe','pipe'],
});
let diagnostics=''; fixture.stderr.on('data',chunk=>{diagnostics+=chunk;});
const lines=createInterface({input:fixture.stdout});
const nextLine=async()=>JSON.parse((await Promise.race([
  once(lines,'line'),once(fixture,'exit').then(([code])=>{throw new Error(`Fixture exited ${code}: ${diagnostics}`);}),
  new Promise((_,reject)=>{const timer=setTimeout(()=>reject(new Error('Fixture timed out')),20000);timer.unref();}),
]))[0]);
let browser;
try {
  const {base}=await nextLine();
  browser=await chromium.launch();
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  page.setDefaultTimeout(10000);
  await page.addInitScript(()=>{
    window.__policyTools=[];
    Object.defineProperty(document,'modelContext',{configurable:true,value:{registerTool:async tool=>window.__policyTools.push(tool)}});
  });
  const writes=[];const errors=[];
  page.on('request',request=>{if(request.method()==='POST')writes.push(request.url());});
  page.on('pageerror',error=>errors.push(error.message));
  await page.goto(`${base}/admin?section=rules`);
  await page.getByRole('button',{name:'Version history',exact:true}).click();
  await page.getByText('No saved versions yet. Defaults and unsaved drafts are not part of version history.',{exact:true}).waitFor();
  const seeded=nextLine();fixture.stdin.write('history\n');await seeded;
  await page.reload();
  const captureDraft=(await page.getByRole('textbox',{name:'Capture rules',exact:true}).inputValue()).replace('Capture purpose version 12','Unsaved capture draft');
  await page.getByRole('textbox',{name:'Capture rules',exact:true}).fill(captureDraft);
  await page.getByRole('button',{name:'Version history',exact:true}).click();
  const capture=page.getByRole('region',{name:'Capture rules version history',exact:true});
  const captureVersion=capture.getByRole('combobox',{name:'Capture rules saved version',exact:true});
  await captureVersion.selectOption('11');
  await capture.getByText('Saved by human:test-owner',{exact:false}).waitFor();
  await capture.getByRole('button',{name:'Compare with current saved version',exact:true}).click();
  assert.match(await capture.getByRole('region',{name:'Capture rules historical content',exact:true}).innerText(),/Capture purpose version 11/);
  assert.match(await capture.getByRole('region',{name:'Capture rules current saved content',exact:true}).innerText(),/Capture purpose version 12/);
  assert.doesNotMatch(await capture.getByRole('region',{name:'Capture rules current saved content',exact:true}).innerText(),/Unsaved capture draft/);
  await capture.getByRole('button',{name:'Load older versions',exact:true}).click();
  await captureVersion.selectOption('1');
  assert.match(await capture.getByRole('region',{name:'Capture rules historical content',exact:true}).innerText(),/Capture purpose version 1\n/);
  assert.equal(await page.getByRole('textbox',{name:'Capture rules',exact:true}).inputValue(),captureDraft);
  for(const width of [1440,390]) {
    await page.setViewportSize({width,height:1000});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width);
    if(process.env.QA_SCREENSHOTS){await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});await capture.screenshot({path:`${process.env.QA_SCREENSHOTS}/capture-history-${width}.png`});}
  }
  await page.getByRole('button',{name:'Version history',exact:true}).click();
  await page.route('**/owner/api/capture-policy/history',route=>route.fulfill({status:503,json:{ok:false,error:{message:'Synthetic history unavailable'}}}));
  await page.getByRole('button',{name:'Version history',exact:true}).click();
  await capture.getByRole('alert').getByText('Synthetic history unavailable',{exact:false}).waitFor();
  await page.unroute('**/owner/api/capture-policy/history');
  await capture.getByRole('button',{name:'Retry history',exact:true}).click();
  await captureVersion.waitFor();
  assert.equal(await page.getByRole('textbox',{name:'Capture rules',exact:true}).inputValue(),captureDraft);

  await page.getByRole('tab',{name:'Verification settings',exact:true}).click();
  await page.getByRole('textbox',{name:'Review criteria',exact:true}).fill('Unsaved criteria draft');
  await page.getByRole('button',{name:'Version history',exact:true}).click();
  const criteria=page.getByRole('region',{name:'Review criteria version history',exact:true});
  const criteriaVersion=criteria.getByRole('combobox',{name:'Review criteria saved version',exact:true});
  await criteriaVersion.selectOption('12');
  await criteria.getByText('Version numbers follow verification settings. Some versions may contain the same criteria text.',{exact:true}).waitFor();
  await criteria.getByRole('button',{name:'Compare with current saved version',exact:true}).click();
  await criteria.getByText('Text matches the saved version loaded in this editor.',{exact:true}).waitFor();
  await criteria.getByRole('button',{name:'Load older versions',exact:true}).click();
  await criteriaVersion.selectOption('1');
  assert.match(await criteria.getByRole('region',{name:'Review criteria historical content',exact:true}).innerText(),/Require evidence version 1\./);
  assert.match(await criteria.getByRole('region',{name:'Review criteria current saved content',exact:true}).innerText(),/Require evidence version 12\./);
  assert.equal(await page.getByRole('textbox',{name:'Review criteria',exact:true}).inputValue(),'Unsaved criteria draft');
  assert.equal(await page.getByRole('switch',{name:'AI-assisted checks',exact:true}).isChecked(),false);
  for(const width of [1440,390]) {
    await page.setViewportSize({width,height:1000});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width);
    if(process.env.QA_SCREENSHOTS)await criteria.screenshot({path:`${process.env.QA_SCREENSHOTS}/criteria-history-${width}.png`});
  }
  await page.waitForFunction(()=>window.__policyTools.some(tool=>tool.name==='get_policy_history'));
  const history=await page.evaluate(async()=>{
    const tool=window.__policyTools.find(tool=>tool.name==='get_policy_history');
    return JSON.parse((await tool.execute({kind:'criteria',limit:2,before_version:4})).content[0].text);
  });
  assert.deepEqual(history.versions.map(row=>row.version),[3,2]);
  assert.equal(history.next_before_version,2);
  for(const query of ['limit=0','limit=51','before_version=wrong','before_version=0']) {
    const response=await page.request.get(`${base}/owner/api/review-criteria/history?${query}`);
    assert.equal(response.status(),400);
  }
  const anonymous=await browser.newContext();
  assert.equal((await anonymous.request.get(`${base}/owner/api/capture-policy/history`)).status(),401);
  await anonymous.close();
  const active=(await (await page.request.get(`${base}/owner/api/review-policy`)).json()).result;
  assert.equal(active.version,13);assert.equal(active.settings.criteria,'Require evidence version 12.');
  assert.equal(active.settings.mode,'off');assert.equal(active.settings.external_consent,false);
  assert.deepEqual(writes,[],'History never submits a policy or changes credentials');
  assert.deepEqual(errors,[]);
  console.log('PASS: immutable policy histories, pagination, metadata, comparison against saved text, draft preservation, failure/retry, auth, WebMCP and desktop/mobile.');
} finally {await browser?.close();fixture.stdin.end();fixture.kill('SIGTERM');lines.close();}
