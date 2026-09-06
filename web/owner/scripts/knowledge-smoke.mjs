import assert from 'node:assert/strict';
import { mkdir } from 'node:fs/promises';

export async function inspectKnowledge(page, data) {
  if (process.env.QA_SCREENSHOTS) await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
  const list = page.locator('.knowledgeList > li > button');
  const first = list.filter({hasText:'Browser fixture approve:'});
  const record = page.getByRole('article',{name:'Knowledge record'});
  await first.waitFor();
  assert.equal(await list.count(),1,'Only the admitted, eligible claim belongs in Knowledge');
  const search = page.getByRole('searchbox',{name:'Search current claims'});
  const applicability = page.getByLabel('Applicability',{exact:true});
  await search.fill('fixture approve');
  assert.equal(await list.count(),1);
  await applicability.selectOption({label:'browser-test'});
  await search.fill('unmatched synthetic search phrase');
  await page.getByRole('heading',{name:'No matching claims',exact:true}).waitFor();
  assert.equal(await list.count(),0);
  await page.getByRole('button',{name:'Clear filters',exact:true}).click();
  assert.equal(await search.inputValue(),'');
  assert.equal(await applicability.inputValue(),'');
  await page.getByLabel('Sort by',{exact:true}).selectOption('statement');
  await first.focus();
  await first.press('Enter');
  await record.locator('h2').filter({hasText:'Browser fixture approve:'}).waitFor();
  assert.match(await record.locator('.knowledgeAttribution').textContent(),/human:browser-test/);
  assert.match(await record.textContent(),/No explicit validity conditions recorded/);
  assert.equal(await record.getByRole('button',{name:'Approve',exact:true}).count(),0);
  const evidence = record.locator('details').filter({has:page.locator('summary').filter({hasText:'Supporting evidence'})});
  assert.equal(await evidence.getAttribute('open'),null);
  await evidence.locator(':scope > summary').click();
  await evidence.locator('.technicalDetails').waitFor();
  assert.match(await evidence.textContent(),/Browser fixture approve:/);
  await evidence.locator(':scope > summary').click();
  await record.getByRole('button',{name:'Close record',exact:true}).press('Escape');
  await page.waitForFunction(()=>document.activeElement?.closest('.knowledgeList') !== null);
  assert.equal(await record.count(),0);
  for (const width of [1536,1024,390]) {
    await page.setViewportSize({width,height:width === 390 ? 844 : 1024});
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width,`Knowledge list overflow at ${width}`);
    const librarySize = await page.locator('.knowledgeLibrary').evaluate(el=>({scroll:el.scrollWidth,client:el.clientWidth}));
    assert.ok(librarySize.scroll <= librarySize.client,`Knowledge library clipped overflow at ${width}: ${JSON.stringify(librarySize)}`);
    if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/knowledge-list-${width}.png`});
    await first.click();
    await record.locator('h2').waitFor();
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth),width,`Knowledge record overflow at ${width}`);
    const recordSize = await record.evaluate(el=>({scroll:el.scrollWidth,client:el.clientWidth}));
    assert.ok(recordSize.scroll <= recordSize.client,`Knowledge record clipped overflow at ${width}: ${JSON.stringify(recordSize)}`);
    if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/knowledge-record-${width}.png`});
    if(width === 390) {
      assert.equal(await record.getByRole('button',{name:'Close record',exact:true}).evaluate(el=>document.activeElement===el),true);
      await record.locator('.knowledgeEvidence summary').first().click();
      await record.locator('.knowledgeEvidence').first().scrollIntoViewIfNeeded();
      if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/knowledge-evidence-${width}.png`});
    }
    await record.getByRole('button',{name:'View lineage',exact:true}).click();
    await page.locator('.graphNode.evidence').first().waitFor();
    if (width === 390) {
      const graph = page.getByLabel('Lineage: evidence, claim, and governed context',{exact:true});
      const geometry = await graph.evaluate(el=>{
        const bounds=el.getBoundingClientRect();
        return {left:bounds.left,right:bounds.right,scroll:el.scrollWidth,client:el.clientWidth,nodes:[...el.querySelectorAll('.graphNode')].map(node=>{const r=node.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom};})};
      });
      assert.equal(geometry.nodes.length,3,'Mobile lineage must expose evidence, claim, and governed context');
      assert.ok(geometry.scroll<=geometry.client,'Mobile lineage must fit horizontally');
      geometry.nodes.forEach((node,index)=>{
        assert.ok(node.left>=geometry.left && node.right<=geometry.right,`Mobile lineage node ${index} must fit inside the graph`);
        if(index) assert.ok(node.top>=geometry.nodes[index-1].bottom,'Mobile lineage must read evidence, claim, then governed context vertically');
      });
    }
    assert.equal(await page.locator('.graphPlane .technicalDetails').count(),0,'Source internals stay in disclosure, not the graph');
    await page.locator('.graphNode.evidence').first().click();
    await page.locator('.knowledgeGraphEvidence .technicalDetails').waitFor();
    if(process.env.QA_SCREENSHOTS) await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/knowledge-lineage-${width}.png`});
    await page.getByRole('button',{name:'Back to claims',exact:true}).click();
    if (await record.isVisible()) await record.getByRole('button',{name:'Close record',exact:true}).click();
    await first.waitFor();
  }
  await page.setViewportSize({width:1536,height:1024});
}

// Bounded follow-up for visual changes after the complete owner workflow passed.
if (process.argv.includes('--standalone')) {
  const { chromium } = await import('playwright');
  const { spawn } = await import('node:child_process');
  const { createInterface } = await import('node:readline');
  const { fileURLToPath } = await import('node:url');
  const root = fileURLToPath(new URL('../../../',import.meta.url));
  const fixture = spawn(process.env.PYTHON || 'python3',[fileURLToPath(new URL('owner-fixture.py',import.meta.url))],{cwd:root,env:{...process.env,PYTHONPATH:`${root}/src`},stdio:['pipe','pipe','pipe']});
  let browser;
  try {
    const data = await new Promise((resolve,reject)=>{
      const timeout=setTimeout(()=>reject(new Error('Fixture startup timed out')),20000);
      createInterface({input:fixture.stdout}).once('line',line=>{clearTimeout(timeout);resolve(JSON.parse(line));});
      fixture.once('exit',code=>{clearTimeout(timeout);reject(new Error(`Fixture exited ${code}`));});
    });
    browser=await chromium.launch();
    const page=await browser.newPage({viewport:{width:1536,height:1024}});
    await page.goto(`${data.base}/home`);
    await page.locator('input[name=token]').fill(data.owner);
    await Promise.all([page.waitForNavigation(),page.locator('button[type=submit]').click()]);
    await page.locator('.nextClaim h3').waitFor();
    if(process.env.QA_SCREENSHOTS) {
      await mkdir(process.env.QA_SCREENSHOTS,{recursive:true});
      for(const width of [1536,1024,390]) {
        await page.setViewportSize({width,height:width===390?844:1024});
        await page.screenshot({path:`${process.env.QA_SCREENSHOTS}/home-pending-${width}.png`});
      }
      await page.setViewportSize({width:1536,height:1024});
    }
    await page.goto(`${data.base}/review?claim_id=${data.ids[0]}&view=full`);
    await page.getByRole('button',{name:'Approve',exact:true}).click();
    await page.getByRole('button',{name:'Confirm approval',exact:true}).click();
    await page.getByText('Approved for reuse',{exact:true}).waitFor();
    await page.getByRole('button',{name:'Knowledge',exact:true}).click();
    await inspectKnowledge(page,data);
    console.log('PASS Knowledge: search, filters, authorizer, evidence, keyboard return, inner/outer responsive overflow, complete vertical mobile lineage. Isolated synthetic fixture only.');
  } finally {
    await browser?.close();
    fixture.stdin.end('\n');
  }
}

export async function inspectKnowledgeRace(page, data) {
  const list = page.locator('.knowledgeList > li > button');
  await list.first().waitFor();
  assert.equal(await list.count(),2);
  let finishDelayedSelection;
  const delayedSelectionFinished = new Promise(resolve=>{ finishDelayedSelection=resolve; });
  await page.route(`**/owner/api/claims/${data.ids[0]}`,async route => {
    const response = await route.fetch();
    await new Promise(resolve=>setTimeout(resolve,300));
    await route.fulfill({response});
    finishDelayedSelection();
  });
  await list.filter({hasText:'Browser fixture approve:'}).click();
  await list.filter({hasText:'Revised finding:'}).click();
  await page.locator('.knowledgeRecord h2').filter({hasText:'Revised finding:'}).waitFor();
  await delayedSelectionFinished;
  await page.waitForLoadState('networkidle');
  assert.match(await page.locator('.knowledgeRecord h2').textContent(),/Revised finding:/,'A late response must not replace the selected claim');
  await page.unroute(`**/owner/api/claims/${data.ids[0]}`);
  await page.getByRole('button',{name:'Close record',exact:true}).click();
}
