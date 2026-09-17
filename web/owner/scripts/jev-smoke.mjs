import { chromium } from 'playwright';
import { spawn, execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3', [fileURLToPath(new URL('jev-fixture.py', import.meta.url))], {
  cwd:root, env:{...process.env,PYTHONPATH:`${root}/src`}, stdio:['pipe','pipe','pipe'],
});
let browser;
let diagnostics = '';
fixture.stderr.on('data', c => { diagnostics += c; });
try {
  const data = await new Promise((resolve,reject) => {
    const timer = setTimeout(()=>reject(new Error('Fixture startup timed out')),20000);
    createInterface({input:fixture.stdout}).once('line',line=>{clearTimeout(timer);resolve(JSON.parse(line));});
    fixture.once('exit', code=>{clearTimeout(timer);reject(new Error(`Fixture exited ${code}: ${diagnostics}`));});
  });
  if (process.env.QA_AGENT_BROWSER) {
    const exec = promisify(execFile);
    const args = ['--yes','agent-browser','--session','proofpress-jev-fixture'];
    await exec('npx',[...args,'open',`${data.base}/home`],{timeout:30000});
    const snapshot = await exec('npx',[...args,'snapshot','-i'],{timeout:30000});
    assert.match(snapshot.stdout,/sign in|token|credential/i);
    await exec('npx',[...args,'close'],{timeout:30000});
  }
  browser = await chromium.launch({headless:process.env.QA_KEEP_OPEN !== '1'});
  const page = await browser.newPage({viewport:{width:1536,height:1024}});
  page.setDefaultTimeout(15000);
  const errors = [];
  page.on('pageerror',error=>errors.push(error.message));
  await page.goto(`${data.base}/home`);
  await page.locator('input[name=token]').fill(data.owner);
  await Promise.all([page.waitForNavigation(),page.locator('button[type=submit]').click()]);
  await page.goto(`${data.base}/admin`);
  await page.getByLabel('Model provider',{exact:true}).selectOption('typesafe');
  assert.equal(await page.getByLabel('Model',{exact:true}).inputValue(),'jev-latest');
  await page.getByLabel('LM review',{exact:true}).selectOption('manual');
  await page.getByLabel('Human decision anytime',{exact:false}).check();
  await page.getByLabel('API key',{exact:true}).fill('synthetic-jev-browser-key');
  await page.getByLabel('Allow external model processing for this workspace').check();
  await page.getByRole('button',{name:'Save & activate'}).click();
  await page.getByText('Policy v1 is active',{exact:true}).waitFor();
  await page.reload();
  await page.getByLabel('Model provider',{exact:true}).waitFor();
  assert.equal(await page.getByLabel('Model provider',{exact:true}).inputValue(),'typesafe');
  assert.equal(await page.getByLabel('API key',{exact:true}).inputValue(),'');
  assert.ok(!(await page.locator('body').innerText()).includes('synthetic-jev-browser-key'));
  await page.goto(`${data.base}/review?claim_id=${data.ids[0]}`);
  await page.getByRole('button',{name:'Run deterministic checks',exact:true}).click();
  await page.getByRole('button',{name:'Run optional LM review',exact:true}).click();
  await page.getByRole('button',{name:'Run LM review',exact:true}).click();
  await page.getByRole('button',{name:'Jev structured advice · experimental',exact:true}).waitFor();
  await page.getByRole('button',{name:'Jev structured advice · experimental',exact:true}).click();
  await page.getByText('Distribution confidence',{exact:true}).waitFor();
  const text = await page.locator('body').innerText();
  assert.match(text,/jev-OFFLINE-FIXTURE/);
  assert.match(text,/Human Approval remains required/);
  assert.match(text,/98\.0%/);
  assert.match(text,/0\.950/);
  const screenshots = process.env.QA_SCREENSHOTS;
  if (screenshots) await mkdir(screenshots,{recursive:true});
  for (const width of [1536,1024,390]) {
    await page.setViewportSize({width,height:width === 390 ? 844 : 1024});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth),true);
    await page.getByText('Distribution confidence',{exact:true}).scrollIntoViewIfNeeded();
    if (screenshots) await page.screenshot({path:`${screenshots}/jev-review-${width}.png`,fullPage:true});
  }
  await page.setViewportSize({width:1536,height:1024});
  const disclosure = page.getByRole('button',{name:'Jev structured advice · experimental',exact:true});
  await disclosure.focus();
  await page.keyboard.press('Space');
  assert.equal(await disclosure.getAttribute('aria-expanded'),'false');
  await page.keyboard.press('Space');
  assert.equal(await disclosure.getAttribute('aria-expanded'),'true');
  for (const route of ['home','ledger','runs','activity','admin']) {
    await page.goto(`${data.base}/${route}`);
    assert.ok((await page.locator('body').innerText()).length > 30);
  }
  assert.deepEqual(errors,[]);
  assert.equal((await page.request.get(`${data.base}/readyz`)).status(),200);
  console.log(JSON.stringify({ok:true,mode:'offline synthetic Jev',viewports:[1536,1024,390],browserErrors:errors}));
  if (process.env.QA_KEEP_OPEN === '1') {
    await page.goto(`${data.base}/review?claim_id=${data.ids[0]}`);
    console.log(`Synthetic preview open at ${data.base}. Press Enter to close.`);
    await new Promise(resolve => process.stdin.once('data',resolve));
  }
} finally {
  await browser?.close();
  fixture.stdin.end('\n');
}
