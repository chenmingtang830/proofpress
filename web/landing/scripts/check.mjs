import { access, readFile } from "node:fs/promises";

const [html, app, chart, modelResults, quickstart, css, socialCard, socialCardMeta] = await Promise.all([
  readFile(new URL("../index.html", import.meta.url), "utf8"),
  readFile(new URL("../src/App.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/knowledge-chart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/model-results-chart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/components/quickstart.tsx", import.meta.url), "utf8"),
  readFile(new URL("../src/index.css", import.meta.url), "utf8"),
  readFile(new URL("../public/og-proofpress.png", import.meta.url)),
  readFile(new URL("../public/og-proofpress.png.json", import.meta.url), "utf8"),
]);

const socialCardWidth = socialCard.readUInt32BE(16);
const socialCardHeight = socialCard.readUInt32BE(20);

const requirements = [
  [html.includes("seed 1a5ba422"), "direction contract survives in source"],
  [app.includes("Own your intelligence.") && app.includes("Verified. Governed. Cumulative.") && app.includes("Trust infrastructure for RSI."), "hero states the ownership promise and RSI position"],
  [app.indexOf("Trust infrastructure for RSI.") < app.indexOf("The Intelligence Ledger for agent-native organizations."), "product category is revealed after the hero"],
  [app.includes("Agents produce more knowledge than organizations can trust—or keep."), "trust and accumulation gaps share one problem frame"],
  [app.includes('className="problemFrame"') && app.includes("UNVERIFIED") && app.includes("SCATTERED") && app.includes("Output scales. Verification doesn’t.") && app.includes("Agents learn. Organizations forget."), "the curve and two intelligence failures share one problem frame"],
  [app.indexOf("<h3>Observability</h3>") < app.indexOf("<h3>Memory</h3>") && app.includes("<h3>Knowledge graphs &amp; ontologies</h3>") && app.includes("Records activity.") && app.includes("Recalls history.") && app.includes("Maps relationships.") && app.includes("Recall, not durable learning.") && app.includes("Structure, not verified knowledge.") && !app.includes("<h3>Evaluation</h3>") && !app.includes("<h3>Agent platforms</h3>") && app.includes("The missing layer is a governed record"), "the stack gap distinguishes three adjacent infrastructure categories without a competitive table"],
  [app.includes("AI NeoLabs") && app.includes("findings compound across runs") && app.includes("AI-native services") && app.includes("reviewed across agents, experts, and clients") && app.includes("Regulated vertical AI") && app.includes("strict review and accountability") && app.includes("Knowledge-intensive R&amp;D") && app.includes("evidence moves from experiments to decisions"), "four current ICP groups and their work patterns are explicit"],
  [app.indexOf('className="teams"') < app.indexOf('className="evidence"'), "bounded evidence follows the ICP section"],
  [app.includes("Self-hostable") && app.includes("Human-gated") && !app.includes("Provider-neutral") && !app.includes("Human-approved"), "hero signals enterprise deployment control and the human gate"],
  [app.includes('className="productSystem"') && app.includes('className="ledgerStack"') && app.includes('className="ledgerGhost ledgerGhostThree"') && app.includes("M0 185C150 20 450 20 600 185") && app.includes("M600 315C450 480 150 480 0 315") && app.includes("ANY AGENT") && app.includes("Propose + evidence") && app.includes("Evaluate") && app.includes("Govern") && app.includes("Improve") && app.includes("Governed context + feedback") && app.includes("EVIDENCE") && app.includes("EVALUATION") && app.includes("SCOPE") && app.includes("HUMAN ADMISSION") && app.includes("Authorized for declared reuse") && app.includes("USED") && app.includes("OUTCOMES") && app.includes("MCP") && app.includes("Python") && app.includes("CLI") && app.includes("HTTP") && !app.includes("OTHER AGENTS REUSE") && !app.includes('className="architecture"'), "the product mechanism has a two-way agent-to-ledger loop and a growing stack of intelligence records with trust, use, and outcomes attached"],
  [app.includes("compoundingGraph") && app.includes("organizationStory") && app.includes("START AHEAD") && app.includes("LEARN FROM WORK") && app.includes("KEEP WHAT COMPOUNDS") && app.includes("The intelligence stays with the organization."), "the continuous learning section pairs a compounding claim graph with plain organizational outcomes"],
  [!app.includes("Current MVP") && !app.includes("Product direction") && !app.includes("future evaluator"), "the public narrative stays focused on the long-term product story"],
  [app.indexOf('className="why"') < app.indexOf('className="stackGap"') && app.indexOf('className="stackGap"') < app.indexOf('className="product"'), "the story moves from the combined problem frame to the stack gap to the ledger"],
  [app.includes("Harvey-style relay test") && app.includes("126 paired runs") && app.includes("63 controlled stress pairs") && app.includes("Three legal task families") && !app.includes("126 agent handoffs") && app.includes("not an official Harvey benchmark"), "study populations and claim boundaries remain explicit"],
  [app.includes('loading="lazy"') && app.includes('decoding="async"'), "below-fold editorial images load lazily"],
  [app.includes('id="partners"') && app.includes('href="#partners"') && app.includes("Don’t waste your intelligence.") && app.includes("Become a design partner") && app.includes("ancient-ball-940.notion.site"), "the final call to action creates urgency and a clear design-partner next step"],
  [app.includes("Evaluate Proofpress in your environment.") && quickstart.includes("proofpress quickstart") && quickstart.includes("synthetic evidence") && quickstart.includes("local MCP configuration"), "the local quickstart is framed as enterprise technical evaluation"],
  [quickstart.includes(".agents/skills/proofpress-governed-context") && quickstart.includes('uv tool install --with "mcp>=2,<3"'), "quickstart installs both the agent skill and local MCP runtime"],
  [quickstart.includes("CONTRIBUTE") && quickstart.includes("CONTRIBUTING.md") && quickstart.includes("separate setup"), "product use and repository contribution are separate paths"],
  [app.includes("https://github.com/chenmingtang830/proofpress"), "repository link is present"],
  [app.includes("proofpress-brand-film.mp4") && app.includes('<span className="eyebrow">Our mission</span>') && app.match(/Knowledge worth building on\./g)?.length === 1, "the mission label and brand line appear only with the film"],
  [app.includes("2093774242429206969") && app.includes("2093431690379317346"), "published X articles are linked"],
  [chart.includes("Illustrative model — not measured data"), "conceptual chart is not presented as measured evidence"],
  [modelResults.indexOf("Claude Opus 4.8") < modelResults.indexOf("Qwen 3.8 27B") && modelResults.includes("const scaleFloor = 85") && modelResults.includes("Ordered by uplift; zoomed 85–100% scale") && !app.includes("harvey-study.png"), "frozen per-model results are ordered by uplift on a disclosed 85-to-100 scale"],
  [css.includes("--accent: #0e6675"), "PR #113 accent token is used"],
  [css.includes("prefers-reduced-motion"), "reduced motion is supported"],
  [html.includes('<link rel="canonical" href="https://proofpress.dev/"') && html.includes('<link rel="icon" href="/logo.svg" type="image/svg+xml"'), "canonical URL and favicon are declared"],
  [html.includes('property="og:url" content="https://proofpress.dev/"') && html.includes('property="og:image" content="https://proofpress.dev/og-proofpress.png"') && html.includes('property="og:image:width" content="1200"') && html.includes('property="og:image:height" content="630"') && html.includes('property="og:image:alt"'), "complete Open Graph image metadata is declared"],
  [html.includes('name="twitter:card" content="summary_large_image"') && html.includes('name="twitter:title"') && html.includes('name="twitter:description"') && html.includes('name="twitter:image" content="https://proofpress.dev/og-proofpress.png"') && html.includes('name="twitter:image:alt"'), "complete Twitter large-image metadata is declared"],
  [socialCard.subarray(1, 4).toString("ascii") === "PNG" && socialCardWidth === 1200 && socialCardHeight === 630, "social card is a real 1200 by 630 PNG"],
  [html.includes("Trust infrastructure for RSI") && html.includes("Verified. Governed. Cumulative.") && socialCardMeta.includes("Own your intelligence") && socialCardMeta.includes("Trust infrastructure for RSI"), "page metadata and the social-card copy share the concise positioning"],
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
