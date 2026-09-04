import { readFile } from "node:fs/promises";

const [html, app, chart, modelResults, quickstart, css] = await Promise.all([
  readFile(new URL("../index.html", import.meta.url), "utf8"),
  readFile(new URL("../src/App.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/knowledge-chart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/model-results-chart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/quickstart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/index.css", import.meta.url), "utf8"),
]);

const requirements = [
  [html.includes("seed 1a5ba422"), "direction contract survives in source"],
  [app.includes("Make agent knowledge safe to reuse."), "hero promise is present"],
  [app.includes("Agent work compounds. Trust has to keep up."), "trust framing connects compounding work to the product promise"],
  [app.includes("Humans decide.") && app.includes("Only approved knowledge moves forward."), "human authority is explicit"],
  [app.includes("Higher rubric completion. No observed unsafe propagation.") && app.includes("Across 126 paired runs") && app.includes("Proofpress’s governed knowledge ledger") && app.includes("Proofpress-composed") && app.includes("Harvey LAB-derived legal task families") && app.includes("version-pinned public materials") && app.includes("not an official Harvey benchmark") && !app.includes("three public Harvey LAB Contracts task families"), "study result, method, and claim boundary are explicit"],
  [app.includes('loading="lazy"') && app.includes('decoding="async"'), "below-fold editorial images load lazily"],
  [app.includes("ancient-ball-940.notion.site") && app.includes("Contact us"), "contact CTA routes to the public Notion form"],
  [app.includes('href="#quickstart"') && quickstart.includes("proofpress quickstart") && quickstart.includes("fresh synthetic Git workspace") && quickstart.includes("local MCP config") && app.includes("No account, hosted credential, or model call required."), "hero routes to an isolated local MCP quickstart"],
  [app.includes("https://github.com/chenmingtang830/proofpress"), "repository link is present"],
  [app.includes("proofpress-brand-film.mp4") && app.includes("Knowledge worth building on"), "brand film is present"],
  [app.includes("2093774242429206969") && app.includes("2093431690379317346"), "published X articles are linked"],
  [chart.includes("Illustrative model — not measured data"), "conceptual chart is not presented as measured evidence"],
  [modelResults.indexOf("Claude Opus 4.8") < modelResults.indexOf("Qwen 3.8 27B") && modelResults.includes("Ordered by uplift; zoomed 75–100% scale") && !app.includes("harvey-study.png"), "frozen per-model results are ordered by uplift on a disclosed zoomed scale"],
  [css.includes("--accent: #0e6675"), "PR #113 accent token is used"],
  [css.includes("prefers-reduced-motion"), "reduced motion is supported"],
];

const failed = requirements.filter(([ok]) => !ok);
if (failed.length) {
  for (const [, label] of failed) console.error(`FAIL ${label}`);
  process.exit(1);
}
for (const [, label] of requirements) console.log(`PASS ${label}`);
