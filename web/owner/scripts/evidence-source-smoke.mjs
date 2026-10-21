import { chromium } from "playwright";
import assert from "node:assert/strict";
import { mkdir } from "node:fs/promises";
import { spawn } from "node:child_process";
import { createInterface } from "node:readline";
import { receipts } from "./ui-preview-data.mjs";

const base = process.env.PROOFPRESS_PREVIEW_URL || "http://127.0.0.1:7356";
const out = process.env.PROOFPRESS_EVIDENCE_SCREENSHOTS || "/tmp/proofpress-evidence-source";
await mkdir(out, {recursive: true});
const id = Object.keys(receipts)[0];
const fixture = structuredClone(receipts[id]);
const evidence = fixture.evidence[0];
fixture.evidence = [evidence];
fixture.claim.evidence_refs = [evidence.id];
evidence.retrieval_receipt.source = {uri: "urn:synthetic:report:" + "a".repeat(64), media_type: "text/markdown"};
evidence.retrieval_receipt.quote = "# Executive summary\n\n**Scenario table**\n\n- **Flat week:** -$2.4bn\n- **Short-term pivot:** 5,200\n\n[Original source](https://example.test/source)\n\n<script>alert('untrusted source')</script>";
fixture.evidence_details = {[evidence.id]: {details: {filename: "daily-research-example.md",
  location: "Appendix · scenario table", fields: [{name: "US · flat week", value: "-$2.4bn"}, {name: "Short-term pivot", value: "5,200"}]},
  actor: "agent:synthetic-preview", authority: "presentation_only"}};
const preview = process.env.PROOFPRESS_PREVIEW_URL ? null : spawn(process.execPath, ["scripts/ui-preview.mjs"], {
  env: {...process.env, PROOFPRESS_UI_PORT: "7356"}, stdio: ["ignore", "pipe", "inherit"],
});
if (preview) await new Promise((resolve, reject) => {
  const timer = setTimeout(() => reject(new Error("Preview startup timed out")), 20000);
  const lines = createInterface({input: preview.stdout});
  lines.on("line", line => { if (line.includes("Proofpress UI preview:")) { clearTimeout(timer); resolve(); } });
  preview.once("exit", code => { clearTimeout(timer); reject(new Error("Preview exited: " + code)); });
});
const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  await page.route("**/owner/api/claims/" + id, route => route.fulfill({json: {ok: true, result: fixture}}));
  for (const [name, width, height] of [["desktop", 1440, 1050], ["mobile", 390, 900]]) {
    await page.setViewportSize({width, height});
    await page.goto(`${base}/review?claim_id=${id}&view=full`);
    const tabs = page.getByRole("tablist", {name: "Claim evidence, checks and history"});
    const evidenceTab = tabs.getByRole("tab", {name: "Evidence", exact: true});
    await evidenceTab.waitFor();
    assert.equal(await evidenceTab.getAttribute("aria-selected"), "true");
    await tabs.getByRole("tab", {name: "Checks", exact: true}).click();
    assert.equal(await page.getByRole("tabpanel", {name: "Checks", exact: true}).isVisible(), true);
    assert.equal(await page.getByRole("tabpanel", {name: "Evidence", exact: true}).count(), 0);
    await page.keyboard.press("ArrowRight");
    await tabs.getByRole("tab", {name: "History", exact: true, selected: true}).waitFor();
    assert.equal(await tabs.getByRole("tab", {name: "History", exact: true}).getAttribute("aria-selected"), "true");
    assert.equal(await page.getByRole("tabpanel", {name: "History", exact: true}).isVisible(), true);
    await page.keyboard.press("Home");
    await tabs.getByRole("tab", {name: "Evidence", exact: true, selected: true}).waitFor();
    assert.equal(await evidenceTab.getAttribute("aria-selected"), "true");
    const tabLayout = await tabs.getByRole("tab").evaluateAll(elements => elements.map(element => {
      const box = element.getBoundingClientRect(), style = getComputedStyle(element);
      return {height: box.height, top: box.top, shadow: style.boxShadow, radius: style.borderRadius};
    }));
    assert.equal(tabLayout.length, 3);
    assert.ok(tabLayout.every(tab => tab.height >= 44 && tab.top === tabLayout[0].top));
    assert.ok(tabLayout.every(tab => tab.shadow === "none" && tab.radius === "0px"), "Review tabs must not inherit raised button styling");
    const row = page.locator(".fullReview .evidenceRow");
    await row.locator("b").filter({hasText: "daily-research-example.md"}).waitFor();
    await row.locator(".evidenceSourceExcerpt strong").first().waitFor();
    assert.equal(await row.locator(".evidenceSourceFields dt").first().textContent(), "US · flat week");
    assert.equal(await row.locator(".technicalDetails pre").isVisible(), false, "Technical JSON must be collapsed initially");
    assert.equal(await row.locator(".evidenceSourceExcerpt script").count(), 0);
    assert.match(await row.locator(".evidenceSourceExcerpt").textContent(), /Executive summary/);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, "No horizontal page overflow");
    await row.scrollIntoViewIfNeeded();
    await page.screenshot({path: `${out}/report-${name}.png`});
    await row.getByRole("button", {name: "Technical receipt", exact: true}).click();
    assert.equal(await row.locator(".technicalDetails pre").isVisible(), true, "Full receipt must remain available on demand");
    await row.getByRole("button", {name: "Technical receipt", exact: true}).click();
    assert.equal(await row.locator(".technicalDetails pre").isVisible(), false);
  }
  evidence.external_experiment = {source: {system: "Synthetic experiment", run_id: "run:example", coverage: "example only"}};
  await page.reload();
  let evidenceRow = page.locator(".fullReview .evidenceRow");
  await evidenceRow.locator(".evidenceSourceFields").getByText("US · flat week", {exact: true}).waitFor();
  await evidenceRow.getByText("Synthetic experiment", {exact: true}).waitFor();
  await evidenceRow.getByRole("button", {name: "Technical receipt", exact: true}).click();
  await evidenceRow.getByText(/Source labels were supplied by agent:synthetic-preview/).waitFor();
  assert.match(await evidenceRow.locator(".technicalDetails pre").textContent(), /source_description/);
  delete evidence.external_experiment;
  evidence.retrieval_receipt.source.media_type = "application/json";
  evidence.retrieval_receipt.quote = JSON.stringify({records: [
    {date: "2026-10-15", symbol: "SPX", close: 5200, daily_return: null, source_locator: {sheet: "Data", close_cell: "F3"}},
    {date: "2026-10-16", symbol: "SPX", close: 5148, daily_return: -0.01, source_locator: {sheet: "Data", close_cell: "F4"}}
  ]});
  fixture.evidence_details[evidence.id].details = {filename: "market-prices-example.xlsx", location: "Data!F3:F4 · derived close-to-close comparison",
    fields: [{name: "Source fields", value: "date, symbol, close, daily_return"}, {name: "SPX · daily change", value: "-1.00%"}]};
  for (const [name, width, height] of [["desktop", 1440, 1050], ["mobile", 390, 900]]) {
    await page.setViewportSize({width, height});
    await page.reload();
    const row = page.locator(".fullReview .evidenceRow");
    await row.locator("b").filter({hasText: "market-prices-example.xlsx"}).waitFor();
    await row.getByRole("button", {name: "Show source rows", exact: true}).click();
    assert.equal(await row.getByRole("columnheader", {name: "Source cell"}).count(), 1);
    assert.equal(await row.getByRole("cell", {name: "Data!F4", exact: true}).count(), 1);
    assert.equal(await row.locator(".technicalDetails pre").isVisible(), false);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await row.scrollIntoViewIfNeeded();
    await page.screenshot({path: `${out}/prices-${name}.png`});
  }
  evidence.retrieval_receipt.quote = JSON.stringify({records: Array.from({length: 101}, (_, index) => ({
    date: "2026-10-16", symbol: "EXAMPLE" + index, close: 100 + index, daily_return: 0,
  }))});
  await page.reload();
  evidenceRow = page.locator(".fullReview .evidenceRow");
  await evidenceRow.getByRole("button", {name: "Show first 100 source rows", exact: true}).click();
  assert.equal(await evidenceRow.locator(".evidenceSourceTable tbody tr").count(), 100);
  assert.match(await evidenceRow.locator("caption").textContent(), /showing 100 of 101/);
  await evidenceRow.getByRole("button", {name: "Technical receipt", exact: true}).click();
  assert.match(await evidenceRow.locator(".technicalDetails pre").textContent(), /EXAMPLE100/);
  console.log("PASS review tab mouse/keyboard switching and flat hit targets; report/spreadsheet sources, collapsed receipts and desktop/mobile layout.");
} finally {
  await browser.close();
  preview?.kill("SIGTERM");
}
