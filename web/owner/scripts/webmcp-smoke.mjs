import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
import {once} from 'node:events';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';

const root=fileURLToPath(new URL('../../../',import.meta.url));
const fixture=spawn(process.env.PYTHON || 'python3',[fileURLToPath(new URL('onboarding-fixture.py',import.meta.url))],{
  cwd:root,env:{...process.env,PYTHONPATH:`${root}/src`},stdio:['pipe','pipe','pipe'],
});
let diagnostics='';fixture.stderr.on('data',chunk=>{diagnostics+=chunk;});
const lines=createInterface({input:fixture.stdout});
let browser;
try {
  const line=await Promise.race([
    once(lines,'line').then(([line])=>line),
    once(fixture,'exit').then(([code])=>{throw new Error(`Fixture exited ${code}: ${diagnostics}`);}),
    new Promise((_,reject)=>{const timer=setTimeout(()=>reject(new Error(`Fixture timed out: ${diagnostics}`)),20000);timer.unref();}),
  ]);
  const {base}=JSON.parse(line);
  browser=await chromium.launch();
  const page=await browser.newPage();
  page.setDefaultTimeout(12000);
  await page.addInitScript(()=>{
    window.syntheticTools={};
    document.modelContext={registerTool(tool){window.syntheticTools[tool.name]=tool;}};
  });
  const writes=[];
  page.on('request',request=>{if(request.method()!=='GET') writes.push({url:request.url(),method:request.method()});});
  await page.goto(`${base}/home`);
  await page.waitForFunction(()=>window.syntheticTools.get_capture_policy);
  const call=(name,input={})=>page.evaluate(async ({name,input})=>{
    const result=await window.syntheticTools[name].execute(input);
    return {isError:!!result.isError,...JSON.parse(result.content[0].text)};
  },{name,input});
  const summary=await call('get_workspace_summary');
  assert.equal(summary.isError,false);
  assert.equal(summary.partial,true,'Fresh workspace has explicit unavailable sections');
  assert.equal(summary.current_governed_context_count,null,'Unknown is not zero');
  assert.ok(summary.unavailable.some(section=>section.code==='workspace_policy_missing'));
  const identity=await call('get_workspace_identity');
  assert.equal(identity.workspace_id,'workspace:onboarding-test');
  assert.equal(identity.role,'owner');
  assert.equal('csrf' in identity,false);
  const initialAccess=await call('get_agent_access');
  const initial=await call('get_capture_policy');
  assert.equal(initial.version,0);
  const draft={purpose:'Preserve bounded synthetic findings.',capture:['One observation with evidence and limits.'],exclude:['Secrets and raw traces.']};
  assert.equal((await call('prepare_capture_policy_change',draft)).activated,false);
  await page.getByLabel('Capture rules',{exact:true}).waitFor();
  await page.waitForFunction(()=>document.querySelector('.captureRules textarea')?.value.includes('bounded synthetic'));
  assert.equal(new URL(page.url()).searchParams.get('section'),'rules');
  assert.equal((await call('get_capture_policy')).version,0,'Preparation did not save server policy');
  // Already-open tab must consume a second prepared draft without a reload.
  await call('prepare_capture_policy_change',{...draft,purpose:'Second synthetic draft.'});
  await page.waitForFunction(()=>document.querySelector('.captureRules textarea')?.value.includes('Second synthetic draft'));
  assert.equal((await call('prepare_capture_policy_change',{...draft,api_key:'synthetic-never-store'})).isError,true);
  assert.equal(await page.evaluate(()=>JSON.stringify(sessionStorage).includes('synthetic-never-store')),false);
  const policy=await call('get_review_policy');
  for(const provider of ['managed_gmi','openai_decisions']) {
    assert.ok(provider in policy.providers);
    const prepared=await call('prepare_review_policy_change',{
      ...policy.settings,provider,endpoint:'',model:policy.providers[provider].default_model,
      criteria:`Synthetic criteria for ${provider}`,mode:'automatic',require_judge:true,
      external_consent:false,auto_admit_new_claims:false,
    });
    assert.equal(prepared.isError,false);
    assert.equal(prepared.activated,false);
    await page.getByRole('tab',{name:'Verification settings',exact:true}).waitFor();
    await page.getByRole('switch',{name:'AI-assisted checks',exact:true}).waitFor();
    await page.waitForFunction(provider=>document.querySelector('[aria-label="Model provider"]')?.value===provider,provider);
    assert.equal(await page.getByLabel('Model provider',{exact:true}).inputValue(),provider);
    assert.equal((await call('get_review_policy')).version,0,'Provider preparation never saves policy or processing consent');
  }
  const manualCriteria='Preserve these synthetic criteria while AI is off.';
  await call('prepare_review_policy_change',{
    ...policy.settings,provider:'managed_gmi',endpoint:'',model:policy.providers.managed_gmi.default_model,
    criteria:manualCriteria,mode:'off',require_judge:false,external_consent:false,auto_admit_new_claims:false,
  });
  await page.getByRole('button',{name:'Use manual review',exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Use manual review',exact:true}).isEnabled(),true,
    'Manual-first policy remains usable without any provider credential');
  await call('prepare_agent_credential_issue',{principal_id:'agent:synthetic-first',label:'First draft'});
  await page.getByLabel('Agent identity',{exact:true}).waitFor();
  await page.waitForFunction(()=>document.querySelector('[aria-label="Agent identity"]')?.value==='agent:synthetic-first');
  await call('prepare_agent_credential_issue',{principal_id:'agent:synthetic-second',label:'Second draft'});
  await page.waitForFunction(()=>document.querySelector('[aria-label="Agent identity"]')?.value==='agent:synthetic-second');
  assert.deepEqual((await call('get_agent_access')).credentials,initialAccess.credentials,'Draft does not issue credentials');
  assert.deepEqual(writes,[],'All read/prepare tools leave server state untouched');
  // Only synthetic human interactions may save. Off mode must retain authored
  // review criteria without granting provider consent or enabling AI.
  await page.getByRole('tab',{name:'Verification settings',exact:true}).click();
  await page.getByRole('button',{name:'Use manual review',exact:true}).click();
  await page.getByText('Settings saved.',{exact:true}).waitFor();
  const manual=await call('get_review_policy');
  assert.equal(manual.version,1);
  assert.equal(manual.settings.criteria,manualCriteria);
  assert.equal(manual.settings.mode,'off');
  assert.equal(manual.settings.external_consent,false);
  assert.equal(manual.settings.auto_admit_new_claims,false);
  // Exercise the real capture API, CSRF, parsing and version readback too.
  await call('prepare_capture_policy_change',draft);
  await page.getByRole('button',{name:'Save capture rules',exact:true}).click();
  await page.getByText('Capture rules v1 saved. Agents will use them on their next run.',{exact:true}).waitFor();
  assert.equal((await call('get_capture_policy')).version,1);
  assert.equal(writes.length,2);
  assert.ok(writes[0].url.endsWith('/owner/api/review-policy'));
  assert.ok(writes[1].url.endsWith('/owner/api/capture-policy'));
  console.log('PASS: WebMCP reads and preparation, live providers, repeated drafts, setup errors and human-only save verified on synthetic localhost.');
} finally {
  await browser?.close();
  fixture.stdin.end('quit\n');
  fixture.kill();
  lines.close();
}
