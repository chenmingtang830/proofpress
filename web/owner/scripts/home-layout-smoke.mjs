import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import { mkdir } from 'node:fs/promises';
import assert from 'node:assert/strict';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const fixture = spawn(process.env.PYTHON || 'python3', [fileURLToPath(new URL('owner-fixture.py', import.meta.url))], {
  cwd: root, env: {...process.env, PYTHONPATH: `${root}/src`, PROOFPRESS_TEST_WIDE_HOME:'1', PROOFPRESS_TEST_LONG_CONTENT:'1'},
  stdio: ['pipe', 'pipe', 'pipe'],
});
let diagnostics = '';
fixture.stderr.on('data', chunk => { diagnostics += chunk; });
let browser;
try {
  const data = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Fixture startup timed out')), 20000);
    createInterface({input:fixture.stdout}).once('line', line => {clearTimeout(timer); resolve(JSON.parse(line));});
    fixture.once('exit', code => {clearTimeout(timer); reject(new Error(`Fixture exited ${code}: ${diagnostics}`));});
  });
  browser = await chromium.launch();
  const page = await browser.newPage({viewport:{width:1440,height:1080}});
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(`${data.base}/home`);
  await page.locator('input[name=token]').fill(data.owner);
  await Promise.all([page.waitForNavigation(), page.locator('button[type=submit]').click()]);
  await page.locator('.homeClaimNode').first().click();
  await page.getByRole('complementary', {name:'Claim preview'}).waitFor();
  let previousWidth = 0;
  for (const width of [1440,1920,2560,3440,1200,1024,768,390]) {
    await page.setViewportSize({width,height:width < 700 ? 844 : 1080});
    const box = await page.evaluate(() => {
      const rect = selector => {const {x,y,width,height,right,bottom} = document.querySelector(selector).getBoundingClientRect();return {x,y,width,height,right,bottom};};
      const home = document.querySelector('.workspaceHome');
      const style = getComputedStyle(home);
      const node = document.querySelector('.homeClaimNode');
      return {home:rect('.workspaceHome'),graph:rect('.homeClaimNetwork'),viewport:rect('.homeNetworkViewport'),
        preview:rect('.homeClaimDetail'),node:rect('.homeClaimNode'),
        parent:home.parentElement.getBoundingClientRect().width,padding:parseFloat(style.paddingLeft)+parseFloat(style.paddingRight),
        pageOverflow:document.documentElement.scrollWidth > innerWidth,
        titleClamped:getComputedStyle(node.querySelector('strong')).webkitLineClamp};
    });
    assert.equal(box.pageOverflow,false,`No page-level overflow at ${width}`);
    assert.ok(Math.abs(box.home.width-box.parent) <= 2,`Home fills the main workspace at ${width}`);
    assert.ok(Math.abs(box.graph.width-(box.home.width-box.padding)) <= 2,`Graph fills Home at ${width}`);
    assert.equal(box.titleClamped,'2');
    if (width > 1200) {
      assert.ok(box.graph.width > previousWidth,`Graph grows as the screen widens to ${width}`);
      previousWidth = box.graph.width;
      assert.ok(box.preview.width >= 320 && box.preview.width <= 521,`Readable preview width at ${width}`);
      assert.ok(box.preview.x >= box.viewport.right-1,`Preview does not cover graph at ${width}`);
      assert.ok(box.node.right <= box.viewport.right,`Claim is visible beside preview at ${width}`);
    } else {
      assert.ok(box.preview.y >= box.viewport.bottom-1,`Preview stacks below graph at ${width}`);
    }
    if (process.env.QA_SCREENSHOTS && [1440,2560,3440,390].includes(width)) {
      await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
      await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/home-selected-${width}.png`,fullPage:true});
    }
  }
  await page.setViewportSize({width:2560,height:1080});
  await page.getByRole('button',{name:'Close claim preview'}).click();
  assert.equal(await page.locator('.homeClaimDetail').count(),0);
  const openWidth = await page.locator('.homeNetworkViewport').evaluate(el => el.getBoundingClientRect().width);
  const graphWidth = await page.locator('.homeClaimNetwork').evaluate(el => el.getBoundingClientRect().width);
  assert.ok(Math.abs(openWidth-graphWidth) < 3,'Graph reclaims preview space on close');
  assert.deepEqual(errors,[]);
  console.log('PASS: Home fills 1440–3440px screens; preview has its own column, stacks through 1200px, and mobile does not overflow.');
} finally {
  await browser?.close();
  fixture.stdin.end('\n');
  fixture.kill();
}
