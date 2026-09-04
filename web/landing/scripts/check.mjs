import { readFile } from "node:fs/promises";

const [html, app, architecture, chart, quickstart, css] = await Promise.all([
  readFile(new URL("../index.html", import.meta.url), "utf8"),
  readFile(new URL("../src/App.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/architecture-diagram.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/knowledge-chart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/quickstart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/index.css", import.meta.url), "utf8"),
]);

const requirements = [
  [html.includes("seed 1a5ba422"), "direction contract survives in source"],
  [app.includes("Govern what your agents learn."), "hero promise is present"],
  [architecture.includes("only step that can admit knowledge"), "human authority is explicit"],
  [app.includes("ancient-ball-940.notion.site") && app.includes("Contact us"), "contact CTA routes to the public Notion form"],
  [app.includes('href="#quickstart"') && quickstart.includes("proofpress demo"), "hero routes to a runnable local demo"],
  [app.includes("https://github.com/chenmingtang830/proofpress"), "repository link is present"],
  [chart.includes("Illustrative model — not measured data"), "conceptual chart is not presented as measured evidence"],
  [css.includes("--accent: #0e6675"), "PR #113 accent token is used"],
  [css.includes("prefers-reduced-motion"), "reduced motion is supported"],
];

const failed = requirements.filter(([ok]) => !ok);
if (failed.length) {
  for (const [, label] of failed) console.error(`FAIL ${label}`);
  process.exit(1);
}
for (const [, label] of requirements) console.log(`PASS ${label}`);
