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

const productStory = await readFile(new URL("../src/components/living-research.tsx", import.meta.url), "utf8");

const requirements = [
  [html.includes("seed 1a5ba422"), "the accepted visual direction remains documented"],
  [app.includes('id="main"') && app.includes('href="#main"') && app.includes('aria-label="Primary navigation"'), "the homepage retains landmarks, a skip link and native navigation"],
  [app.includes('href={`${repoUrl}#quick-start`}') && app.includes("https://github.com/chenmingtang830/proofpress"), "current setup and repository entry points remain available"],
  [productStory.includes("Human Approval authorizes reuse") && productStory.includes("Illustrative finding history") && !app.includes("UPDATE TRUST WEIGHTS"), "review authority and the illustrative lifecycle remain explicit"],
  [app.includes("<ModelResultsChart />") && app.includes("Proofpress-run study") && app.includes("20 paired chains") && app.includes("1,600 numeric slots per arm") && app.includes("excludes upstream preparation") && app.includes("separate two-task APEX pilot"), "research results retain their attribution, scope and token-accounting boundaries"],
  [app.includes('import posts from "./content/post-index.json"') && app.includes('href={`/blog/${item.slug}`}') && !app.includes(".slice(0, 3)"), "all imported articles retain their native blog destinations"],
  [app.includes('preload="metadata"') && app.includes('playsInline') && app.includes('/films/proofpress-continuara-20261021-1080p.mp4'), "the revised film remains playable without autoplay"],
  [app.includes('<small>by <span>Continuara Labs</span></small>') && app.includes('href={contactUrl}'), "the company attribution and existing contact destination are retained"],
  [css.includes("--accent: #0e6675"), "PR #113 accent token is used"],
  [css.includes("prefers-reduced-motion"), "reduced motion is supported"],
  [html.includes('<link rel="canonical" href="https://proofpress.dev/"') && html.includes('<link rel="icon" href="/logo.svg" type="image/svg+xml"'), "canonical URL and favicon are declared"],
  [html.includes('property="og:url" content="https://proofpress.dev/"') && html.includes('property="og:image" content="https://proofpress.dev/og-proofpress-20261023.png"') && html.includes('property="og:image:width" content="1200"') && html.includes('property="og:image:height" content="630"') && html.includes('property="og:image:alt"'), "complete Open Graph image metadata is declared"],
  [html.includes('name="twitter:card" content="summary_large_image"') && html.includes('name="twitter:title"') && html.includes('name="twitter:description"') && html.includes('name="twitter:image" content="https://proofpress.dev/og-proofpress-20261023.png"') && html.includes('name="twitter:image:alt"'), "complete Twitter large-image metadata is declared"],
  [socialCard.subarray(1, 4).toString("ascii") === "PNG" && socialCardWidth === 1200 && socialCardHeight === 630, "social card is a real 1200 by 630 PNG"],
  [html.includes("Proofpress — Build on every discovery") && html.includes("research findings"), "page and social text metadata use the current agent knowledge positioning"],
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
