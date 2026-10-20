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
evidence.retrieval_receipt.quote = "**Scenario table**\n\n- **Flat week:** -$2.4bn\n- **Short-term pivot:** 5,200\n\n[Original source](https://example.test/source)\n\n<script>alert('untrusted source')</script>";
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
    const row = page.locator(".fullReview .evidenceRow");
    await row.locator("b").filter({hasText: "daily-research-example.md"}).waitFor();
    await row.locator(".evidenceSourceExcerpt strong").first().waitFor();
    assert.equal(await row.locator(".evidenceSourceFields dt").first().textContent(), "US · flat week");
    assert.equal(await row.locator(".technicalDetails pre").isVisible(), false, "Technical JSON must be collapsed initially");
    assert.equal(await row.locator(".evidenceSourceExcerpt script").count(), 0);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, "No horizontal page overflow");
    await row.scrollIntoViewIfNeeded();
    await page.screenshot({path: `${out}/report-${name}.png`});
    await row.getByRole("button", {name: "Technical receipt", exact: true}).click();
    assert.equal(await row.locator(".technicalDetails pre").isVisible(), true, "Full receipt must remain available on demand");
    await row.getByRole("button", {name: "Technical receipt", exact: true}).click();
    assert.equal(await row.locator(".technicalDetails pre").isVisible(), false);
  }
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
    await row.getByRole("button", {name: "Show all source rows"}).click();
    assert.equal(await row.getByRole("columnheader", {name: "Source cell"}).count(), 1);
    assert.equal(await row.getByRole("cell", {name: "Data!F4", exact: true}).count(), 1);
    assert.equal(await row.locator(".technicalDetails pre").isVisible(), false);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await row.scrollIntoViewIfNeeded();
    await page.screenshot({path: `${out}/prices-${name}.png`});
  }
  console.log("PASS report and spreadsheet sources: filename, fields, safe Markdown, source cells, collapsed receipts, desktop/mobile.");
} finally {
  await browser.close();
  preview?.kill("SIGTERM");
}
