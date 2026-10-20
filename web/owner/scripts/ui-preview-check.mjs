import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const base = process.env.PREVIEW_URL || 'http://127.0.0.1:7335';
const directory = fileURLToPath(new URL('../../../work/ui-polish-20261013/verification/',import.meta.url));
await mkdir(directory,{recursive:true});
const browser = await chromium.launch();
const errors=[], findings=[], checks=[];
const page = await browser.newPage();
page.on('pageerror',error=>errors.push(error.message));
const routes = [
  ['home','/home','.homeClaimNode'],
  ['review','/review?claim_id=clm_preview_handoff&view=full','.fullStatement'],
  ['queue','/review?claim_id=clm_preview_handoff','.reviewTable'],
  ['knowledge','/ledger','.claimMap'],
  ['runs','/runs','.runList button'],
  ['activity','/activity','.activityTable'],
  ['admin','/admin?section=models','.verificationModelMode'],
];
async function capture(name){
  await page.evaluate(()=>document.fonts.ready);
  await page.screenshot({path:`${directory}/${name}.png`});
  const metrics=await page.evaluate(()=>({width:innerWidth,body:document.body.scrollWidth,fonts:document.fonts.check('16px "DM Sans"')}));
  if(metrics.body>metrics.width) findings.push({name,overflow:metrics});
  checks.push(name);
}
try {
  for(const width of (process.env.WIDTHS || '1512,1024,390').split(',').map(Number)) {
    await page.setViewportSize({width,height:width===390?844:982});
    for(const [name,path,ready] of routes){
      await page.goto(base+path);
      if(name==='queue' && width<900) await page.getByRole('button',{name:'Close details',exact:true}).click();
      await page.locator(ready).first().waitFor();
      await capture(`${name}-${width}`);
      if(name==='review'){
        assert.equal(await page.locator('.reviewFactsGrid').count(),1);
        assert.equal(await page.locator('.fullStatement').textContent(),'Keep evidence attached to every handoff');
        await page.getByRole('tab',{name:'Checks',exact:true}).click();
        await page.locator('.checkList').waitFor();
        await page.getByRole('tab',{name:'Evidence',exact:true}).click();
        await page.getByRole('button',{name:'Applicability & conditions',exact:true}).click();
        await page.getByText('Re-evaluate when the underlying source or task changes.',{exact:true}).waitFor();
        await page.getByRole('button',{name:'Approve',exact:true}).click();
        await page.getByRole('dialog',{name:'Approve this claim?'}).waitFor();
        assert.equal(await page.getByRole('button',{name:'Cancel',exact:true}).evaluate(e=>document.activeElement===e),true);
        await capture(`decision-dialog-${width}`);
        await page.keyboard.press('Escape');
        assert.equal(await page.getByRole('dialog').count(),0);
      }
      if(name==='knowledge'){
        assert.equal(await page.getByRole('button',{name:'Map',exact:true}).getAttribute('aria-pressed'),'true');
        checks.push(`knowledge-default-map-${width}`);
        await page.getByRole('button',{name:'List',exact:true}).click();
        await page.getByRole('searchbox').fill('source');
        assert.ok(await page.locator('.knowledgeList > li').count()>0);
        await page.getByRole('searchbox').fill('no-matching-preview-record');
        await page.getByRole('heading',{name:'No matching claims'}).waitFor();
        await page.getByRole('button',{name:'Clear filters'}).click();
        await page.locator('.knowledgeList > li > button').first().click();
        await page.locator('article.knowledgeRecord h2').waitFor();
        await capture(`knowledge-record-${width}`);
        await page.getByRole('button',{name:'Close record'}).click();
        await page.getByRole('button',{name:'Map',exact:true}).click();
        await capture(`knowledge-map-${width}`);
      }
      if(name==='runs'){
        await page.locator('.runList button').first().click();
        await page.locator('.runDetail h2').waitFor();
        await capture(`run-record-${width}`);
      }
    }
  }
  await page.setViewportSize({width:1512,height:982});
  await page.context().addCookies([{name:'pp-preview-scenario',value:'empty',url:base}]);
  for(const path of ['/home','/review','/ledger','/runs','/activity']) {
    await page.goto(base+path);await page.waitForFunction(()=>document.querySelector('.shell')?.getAttribute('aria-busy')==='false');
    await capture(`empty-${path.slice(1)}`);
  }
  await page.context().addCookies([{name:'pp-preview-scenario',value:'error',url:base}]);
  await page.goto(base+'/ledger');await page.getByRole('button',{name:'Reload workspace'}).waitFor();
  await capture('error-knowledge');
  await page.context().clearCookies();
  await page.getByRole('button',{name:'Reload workspace'}).click();await page.locator('.claimMap').waitFor();
  checks.push('error-recovery');
  await page.goto(base+'/review?claim_id=clm_preview_handoff&view=full');await page.locator('.fullStatement').waitFor();
  await page.keyboard.press('Tab');assert.equal(await page.locator('.skipLink').evaluate(e=>document.activeElement===e),true);
  await page.keyboard.press('Enter');assert.equal(await page.locator('.stage').evaluate(e=>document.activeElement===e),true);
  checks.push('keyboard-skip-link');
  const receipt=await (await page.request.get(base+'/owner/api/claims/clm_preview_handoff')).json();
  await page.route('**/owner/api/claims/clm_preview_handoff',route=>route.fulfill({json:{...receipt,result:{...receipt.result,review_policy:{...receipt.result.review_policy,checks_current:false}}}}));
  await page.reload();await page.getByText('Recheck required',{exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Approve',exact:true}).isDisabled(),true);
  checks.push('stale-checks-block-approval');
  await capture('review-checks-required');
  await page.unroute('**/owner/api/claims/clm_preview_handoff');
  await page.goto(base+'/review?claim_id=missing-preview-record&view=full');
  await page.getByText('Claim not found',{exact:true}).waitFor();
  assert.equal(await page.getByRole('button',{name:'Approve',exact:true}).count(),0);
  checks.push('missing-record-no-substitute');
  const contrast=await page.evaluate(()=>{
    const tokens=getComputedStyle(document.documentElement);
    const luminance=hex=>{const values=hex.trim().replace('#','').match(/.{2}/g).map(v=>parseInt(v,16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return values[0]*.2126+values[1]*.7152+values[2]*.0722;};
    return [['--ink','--paper'],['--ink-2','--wash'],['--ink-3','--paper'],['--paper','--accent'],['--accent','--accent-soft']].map(([fg,bg])=>{const a=luminance(tokens.getPropertyValue(fg)),b=luminance(tokens.getPropertyValue(bg));return {fg,bg,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};});
  });
  assert.ok(contrast.every(pair=>pair.ratio>=4.5),JSON.stringify(contrast));
  checks.push('core-text-contrast-AA');
  const blocked=await page.request.post(base+'/owner/api/reviews',{data:{claim_id:'clm_preview_handoff',decision:'admit'}});
  assert.equal(blocked.status(),409);checks.push('preview-mutation-blocked');
  assert.equal(errors.length,0,errors.join('\n'));
  assert.equal(findings.length,0,JSON.stringify(findings));
} finally {
  await writeFile(`${directory}/results.json`,JSON.stringify({checks,errors,findings},null,2));
  await browser.close();
}
console.log(`PASS: ${checks.length} route, responsive, interaction, state, and preview checks. No browser errors or page overflow.`);
