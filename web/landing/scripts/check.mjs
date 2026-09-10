import { access, readFile } from "node:fs/promises";

const [html, app, chart, css, socialCard] = await Promise.all([
  readFile(new URL("../index.html", import.meta.url), "utf8"),
  readFile(new URL("../src/App.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/knowledge-chart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/index.css", import.meta.url), "utf8"),
  readFile(new URL("../public/og-proofpress.png", import.meta.url)),
]);

const socialCardWidth = socialCard.readUInt32BE(16);
const socialCardHeight = socialCard.readUInt32BE(20);

const requirements = [
  [html.includes("seed 1a5ba422"), "direction contract survives in source"],
  [app.includes("For agent-native research teams") && app.includes("AI research labs") && app.includes("Post-training teams") && app.includes("Benchmark &amp; evaluation teams"), "the research audience and target team types are explicit"],
  [app.indexOf('className="productClosingStatement"') > app.indexOf('className="productMechanism"') && app.indexOf('className="productClosingStatement"') < app.indexOf('id="ledger-system-note"') && app.indexOf('className="productClosingStatement"') < app.indexOf('className="verificationFlow"') && app.includes("Verified. Governed. Cumulative.") && !app.includes('className="productOutcomes"') && !app.slice(0, app.indexOf('className="why"')).includes("RSI"), "the concise product promise sits below the ledger and above its illustrative note without adding another explanatory block"],
  [app.includes("Self-hostable") && app.includes("Human-gated") && !app.includes("Provider-neutral") && !app.includes("Human-approved"), "hero signals enterprise deployment control and the human gate"],
  [app.includes('className="productSystem"') && app.includes('className="ledgerStack"') && app.includes('className="ledgerGhost ledgerGhostThree"') && app.includes("M0 185C150 20 450 20 600 185") && app.includes("M600 315C450 480 150 480 0 315") && app.includes("ANY AGENT") && app.includes('className="mechanismActions"') && app.includes("Propose claims") && app.includes("Attach evidence") && !app.includes("Attach evidence via") && app.includes('className="mechanismValue">Research cycle') && app.includes("Human Approval") && app.includes("Governed context") && !app.includes("Governed context + feedback") && app.includes("EVIDENCE") && app.includes("EVALUATION") && app.includes("SCOPE") && app.includes("Admitted for declared reuse") && app.includes("USED") && app.includes("OUTCOMES") && app.includes("MCP") && app.includes("Python") && app.includes("CLI") && app.includes("HTTP") && !app.includes("OTHER AGENTS REUSE") && !app.includes('className="architecture"'), "the product mechanism has a concrete governed research cycle and a growing stack of intelligence records"],
  [app.includes('className="mobileNav"') && app.includes("View evidence and reuse scope") && app.includes("Human Approval") && app.includes("02 EVALUATE OUTCOMES") && app.includes("03 REFINE KNOWLEDGE") && !app.includes('className="loopReturn"'), "mobile disclosure and the separate learning-loop section preserve the complete research story without a redundant return strip"],
  [!app.includes("Current MVP") && !app.includes("Product direction") && !app.includes("future evaluator"), "the public narrative stays focused on the long-term product story"],
  [app.indexOf('className="why"') < app.indexOf('className="stackGap"') && app.indexOf('className="stackGap"') < app.indexOf('className="product"'), "the story moves from the combined problem frame to the stack gap to the ledger"],
  [app.includes('loading="lazy"') && app.includes('decoding="async"'), "below-fold editorial images load lazily"],
  [app.includes('href={`${repoUrl}#quick-start`}') && !app.includes("<Quickstart"), "setup is delegated to current documentation instead of duplicated on the landing page"],
  [app.includes("https://github.com/chenmingtang830/proofpress"), "repository link is present"],
  [app.includes("<small>by <span>Only Then Labs</span></small>") && !app.includes("Proofpress by <span>Only Then Labs</span>.") && !app.includes("The Intelligence Ledger for agent-native research teams."), "the footer closes with concise Only Then Labs attribution"],
  [app.includes("public.blob.vercel-storage.com/films/proofpress-shoulders-20260910-1080p.mp4") && app.includes('<span className="eyebrow">Our mission</span>') && app.match(/Knowledge worth building on\./g)?.length === 1, "the mission label and brand line appear only with the externally hosted film"],
  [app.includes('import posts from "./content/post-index.json"') && app.includes('href={`/blog/${item.slug}`}') && app.includes(".slice(0, 3)"), "latest imported articles link to native blog pages without bundling full article bodies"],
  [app.includes("Human Approval authorizes reuse") && app.includes("01 USE GOVERNED CONTEXT") && app.includes("knowledge and claims that shaped them") && app.includes("03 REFINE KNOWLEDGE") && !app.includes("UPDATE TRUST WEIGHTS"), "the learning loop connects governed context, downstream claims, outcomes, and evidence-led refinement without implying automatic trust weighting"],
  [chart.includes("Illustrative model — not measured data"), "conceptual chart is not presented as measured evidence"],
  [!app.includes("harvey-study.png") && !app.includes("ModelResultsChart"), "the removed Harvey study is not presented as landing-page evidence"],
  [css.includes("--accent: #0e6675"), "PR #113 accent token is used"],
  [css.includes("prefers-reduced-motion"), "reduced motion is supported"],
  [html.includes('<link rel="canonical" href="https://proofpress.dev/"') && html.includes('<link rel="icon" href="/logo.svg" type="image/svg+xml"'), "canonical URL and favicon are declared"],
  [html.includes('property="og:url" content="https://proofpress.dev/"') && html.includes('property="og:image" content="https://proofpress.dev/og-proofpress.png"') && html.includes('property="og:image:width" content="1200"') && html.includes('property="og:image:height" content="630"') && html.includes('property="og:image:alt"'), "complete Open Graph image metadata is declared"],
  [html.includes('name="twitter:card" content="summary_large_image"') && html.includes('name="twitter:title"') && html.includes('name="twitter:description"') && html.includes('name="twitter:image" content="https://proofpress.dev/og-proofpress.png"') && html.includes('name="twitter:image:alt"'), "complete Twitter large-image metadata is declared"],
  [socialCard.subarray(1, 4).toString("ascii") === "PNG" && socialCardWidth === 1200 && socialCardHeight === 630, "social card is a real 1200 by 630 PNG"],
  [html.includes("Proofpress — Verified knowledge infrastructure for agent-native research teams") && html.includes("Turn research output into knowledge your team can build on."), "page and social text metadata use the current research positioning"],
];

await Promise.all([
  access(new URL("../public/logo.svg", import.meta.url)),
  access(new URL("../public/og-proofpress.png", import.meta.url)),
]);

const failed = requirements.filter(([ok]) => !ok);
if (failed.length) {
  for (const [, label] of failed) console.error(`FAIL ${label}`);
  process.exit(1);
}
for (const [, label] of requirements) console.log(`PASS ${label}`);
