import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { createInterface } from 'node:readline';
import { once } from 'node:events';
import { fileURLToPath } from 'node:url';
import { mkdir } from 'node:fs/promises';
import { chromium } from 'playwright';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3', [fileURLToPath(new URL('onboarding-fixture.py', import.meta.url))], {
  cwd:root, env:{...process.env,PYTHONPATH:`${root}/src`,PROOFPRESS_SECRET_ENCRYPTION_KEY:''}, stdio:['pipe','pipe','pipe'],
});
let diagnostics=''; fixture.stderr.on('data',chunk=>{diagnostics+=chunk;});
const lines=createInterface({input:fixture.stdout});
const nextLine=async()=>JSON.parse((await Promise.race([
  once(lines,'line'),
  once(fixture,'exit').then(([code])=>{throw new Error(`Fixture exited ${code}: ${diagnostics}`);}),
  new Promise((_,reject)=>{const timer=setTimeout(()=>reject(new Error('Fixture timed out')),20000);timer.unref();}),
]))[0]);
let browser;
try {
  const {base}=await nextLine();
  browser=await chromium.launch();
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  page.setDefaultTimeout(12000);
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.context().grantPermissions(['clipboard-read','clipboard-write']);
  await page.goto(`${base}/admin?section=models`);
  await page.getByLabel('Review criteria',{exact:true}).fill('Require a source, method and bounded conclusion.');
  await page.getByRole('button',{name:'Save review criteria',exact:true}).click();
  await page.getByText('Review criteria saved.',{exact:true}).waitFor();
  await page.getByRole('switch',{name:'AI-assisted checks',exact:true}).click();
  await page.getByLabel('Model provider',{exact:true}).selectOption('openai');
  const keyInput=page.getByLabel('API key',{exact:true});
  assert.equal(await keyInput.isDisabled(),true);
  const setup=page.getByRole('region',{name:'Set up local encrypted storage'});
  await setup.waitFor();
  const policy=(await (await page.request.get(`${base}/owner/api/review-policy`)).json()).result;
  assert.ok(policy.local_setup,'Local setup survives a criteria save');
  await setup.getByRole('button',{name:'Copy setup commands',exact:true}).click();
  const commands=await page.evaluate(()=>navigator.clipboard.readText());
  assert.ok(commands.includes(policy.local_setup.database));
  assert.ok(commands.includes(`--port ${new URL(base).port}`));
  assert.match(commands,/PROOFPRESS_SECRET_ENCRYPTION_KEY/);
  assert.equal(spawnSync('bash',['-n'],{input:commands,encoding:'utf8'}).status,0,'Copied shell commands parse');
  const python=commands.match(/python3 - <<'PY'\n([\s\S]*?)\nPY/)[1];
  assert.equal(spawnSync(process.env.PYTHON || 'python3',['-c','import sys; compile(sys.stdin.read(), "setup", "exec")'],{input:python,encoding:'utf8'}).status,0,'Copied Python initializer parses');
  const scriptRequests=[];
  page.on('request',request=>{if(request.method()==='POST')scriptRequests.push(request.url());});
  await page.evaluate(()=>{navigator.clipboard.writeText=async()=>{throw new Error('Synthetic clipboard denied');};});
  await setup.getByRole('button',{name:'Copied',exact:true}).click();
  await setup.getByText('Copy unavailable. Select and copy the commands below.',{exact:true}).waitFor();
  assert.equal(await setup.getByRole('button',{name:'Copy setup commands',exact:true}).isVisible(),true);
  await setup.getByLabel('Encrypted storage terminal commands').waitFor();
  assert.deepEqual(scriptRequests,[],'Copying setup commands never changes server state');
  for(const width of [1440,390]) {
    await page.setViewportSize({width,height:width===390?844:1000});
    await page.evaluate(()=>document.activeElement?.blur());
    await setup.scrollIntoViewIfNeeded();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width,`No page overflow at ${width}`);
    if(process.env.QA_SCREENSHOTS) {
      await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
      await setup.screenshot({path:`${process.env.QA_SCREENSHOTS}/byok-storage-${width}.png`});
    }
  }
  await page.setViewportSize({width:1440,height:1000});
  await page.getByLabel('Model',{exact:true}).selectOption('__custom__');
  await page.getByLabel('Custom model ID',{exact:true}).fill('synthetic-test-model');
  await page.getByLabel('Review criteria',{exact:true}).fill('Keep this unsaved criteria draft.');
  await setup.getByRole('button',{name:'Check storage again',exact:true}).click();
  await setup.getByText('Encrypted storage is still unavailable.',{exact:false}).waitFor();
  await page.route('**/owner/api/review-policy',route=>route.fulfill({status:503,json:{ok:false,error:{message:'Synthetic server restarting'}}}));
  await setup.getByRole('button',{name:'Check storage again',exact:true}).click();
  await setup.getByText('Could not reach Proofpress.',{exact:false}).waitFor();
  await page.unroute('**/owner/api/review-policy');
  const ready=nextLine();fixture.stdin.write('storage-ready\n');
  assert.equal((await ready).storage_ready,true);
  await setup.getByRole('button',{name:'Check storage again',exact:true}).click();
  await page.getByText('Encrypted storage is ready.',{exact:false}).waitFor();
  assert.equal(await keyInput.isEnabled(),true);
  assert.equal(await page.getByLabel('Model provider',{exact:true}).inputValue(),'openai');
  assert.equal(await page.getByLabel('Custom model ID',{exact:true}).inputValue(),'synthetic-test-model');
  assert.equal(await page.getByLabel('Review criteria',{exact:true}).inputValue(),'Keep this unsaved criteria draft.');
  const providerKey='synthetic-provider-key-1234';
  await keyInput.fill(providerKey);
  await page.getByRole('button',{name:'Enable AI checks',exact:true}).click();
  await page.getByText('Settings saved.',{exact:true}).waitFor();
  const saved=(await (await page.request.get(`${base}/owner/api/review-policy`)).json()).result;
  assert.equal(saved.credential.configured,true);
  assert.equal(saved.credential.last_four,'1234');
  assert.equal(saved.settings.provider,'openai');
  assert.equal(saved.settings.auto_admit_new_claims,false);
  assert.equal(saved.settings.criteria,'Require a source, method and bounded conclusion.','AI save does not save an unrelated criteria draft');
  assert.equal(JSON.stringify(saved).includes(providerKey),false);
  const missing=nextLine();fixture.stdin.write('storage-missing\n');await missing;
  await page.reload();
  await page.getByRole('heading',{name:'Restore access to your saved API key',exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Copy setup commands',exact:true}).count(),0);
  await page.getByRole('button',{name:'Terminal restart commands',exact:true}).click();
  assert.equal((await page.getByLabel('Encrypted storage terminal commands').textContent()).includes('os.urandom'),false,'Saved credentials never get replacement-key generation');
  assert.deepEqual(errors,[]);
  console.log('PASS: localhost BYOK recovery, exact-instance commands, desktop/mobile, clipboard fallback, restart failure, draft preservation, encrypted save and original-key recovery.');
} finally {
  await browser?.close();fixture.stdin.end();fixture.kill('SIGTERM');lines.close();
}
