import { ArrowRight01Icon } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { ButtonLink } from "./components/button";
import { KnowledgeChart } from "./components/knowledge-chart";
import { ModelResultsChart } from "./components/model-results-chart";
import { Quickstart } from "./components/quickstart";

const repoUrl = "https://github.com/chenmingtang830/proofpress";
const resultsUrl = `${repoUrl}/tree/main/studies/long-horizon-eval/relaybench`;
const contactUrl = "https://ancient-ball-940.notion.site/eacf21eef9b54c3287f72892cd024a1c?pvs=105";

const writing = [
  {
    label: "ARTICLE",
    title: "Agents Are Creating a New Knowledge Layer—and We Need to Govern It",
    href: "https://x.com/richardt830/status/2093774242429206969",
    image: "/article-knowledge-layer.webp",
    width: 1672,
    height: 941,
  },
  {
    label: "ARTICLE",
    title: "What May the Next Agent Rely On?",
    href: "https://x.com/richardt830/status/2093431690379317346",
    image: "/article-agent-rely.webp",
    width: 1536,
    height: 1024,
  },
  {
    label: "FIELD NOTE",
    title: "Proofpress for the WebMCP Challenge",
    href: "https://x.com/richardt830/status/2095598146546229263",
    image: "/article-webmcp.png",
    width: 1440,
    height: 1050,
  },
];

function Arrow() {
  return <HugeiconsIcon icon={ArrowRight01Icon} size={18} strokeWidth={1.6} aria-hidden="true" />;
}

export function App() {
  return (
    <div className="siteShell">
      <a className="skipLink" href="#main">Skip to content</a>
      <header className="siteHeader">
        <a className="brand" href="#top" aria-label="Proofpress home">
          <img src="/logo.svg" alt="" width="32" height="32" />
          <span>Proofpress</span>
        </a>
        <nav aria-label="Primary navigation">
          <a href="#evidence">Evidence</a>
          <a href="#writing">Writing</a>
          <a href={repoUrl}>GitHub</a>
        </nav>
      </header>

      <main id="main">
        <section className="hero" id="top" aria-labelledby="hero-title">
          <div className="heroCopy">
            <h1 id="hero-title">Make agent knowledge safe to reuse.</h1>
            <p className="heroLead">
              Proofpress keeps evidence and human approval attached to the conclusions your agents create.
            </p>
            <div className="heroActions" aria-label="Get started">
              <ButtonLink href="#quickstart">Install Proofpress <Arrow /></ButtonLink>
              <ButtonLink href="#evidence" variant="secondary">See the evidence</ButtonLink>
            </div>
          </div>
          <div className="heroFoot" aria-label="Proofpress product attributes">
            <span>Open source</span>
            <span>Provider-neutral</span>
            <span>Human-approved</span>
          </div>
        </section>

        <section className="why" aria-labelledby="why-title">
          <h2 id="why-title">Agent work compounds. Trust has to keep up.</h2>
          <KnowledgeChart />
        </section>

        <section className="value" aria-labelledby="value-title">
          <h2 id="value-title">
            Evidence stays attached.<br />
            Humans decide.<br />
            <span>Only approved knowledge moves forward.</span>
          </h2>
        </section>

        <section className="evidence" id="evidence" aria-labelledby="evidence-title">
          <div className="evidenceIntro">
            <h2 id="evidence-title">
              Higher rubric completion. No observed unsafe propagation.
            </h2>
            <p>
              Across 126 paired runs, we used Proofpress’s governed knowledge ledger to compare ordinary
              portable handoffs with governed context across seven models and three Proofpress-composed,
              Harvey LAB-derived legal task families built from version-pinned public materials.
            </p>
          </div>
          <div className="study">
            <ModelResultsChart />
            <div className="studySummary">
              <div><strong>89.3 → 93.4%</strong><span>Rubric completion</span></div>
              <div><strong>8 → 0</strong><span>Observed unsafe propagation · 63 stress pairs</span></div>
              <p>Bounded mechanism evidence—not an official Harvey benchmark or a general efficacy claim.</p>
              <a href={resultsUrl}>Read the public results <Arrow /></a>
            </div>
          </div>
        </section>

        <section className="quickstart" id="quickstart" aria-labelledby="quickstart-title">
          <div className="compactIntro">
            <h2 id="quickstart-title">Install and run Proofpress.</h2>
            <p>Install once, then run locally. No account, hosted credential, or model call required.</p>
          </div>
          <Quickstart />
        </section>

        <section className="writing" id="writing" aria-labelledby="writing-title">
          <div className="compactIntro">
            <h2 id="writing-title">Writing from the field.</h2>
            <a href="https://x.com/richardt830">Follow on X <Arrow /></a>
          </div>
          <div className="writingGrid">
            {writing.map((item) => (
              <a className="writingCard" href={item.href} key={item.href}>
                <div className="writingImage">
                  <img
                    src={item.image}
                    alt=""
                    width={item.width}
                    height={item.height}
                    loading="lazy"
                    decoding="async"
                  />
                </div>
                <span>{item.label}</span>
                <h3>{item.title}</h3>
                <small>Read on X <Arrow /></small>
              </a>
            ))}
          </div>
        </section>

        <section className="film" aria-labelledby="film-title">
          <h2 id="film-title">Our vision: Knowledge worth building on.</h2>
          <video controls playsInline preload="metadata" poster="/proofpress-brand-film-poster.webp">
            <source src="/proofpress-brand-film.mp4" type="video/mp4" />
            Your browser does not support embedded video.
          </video>
        </section>

        <section className="finalCta" aria-labelledby="cta-title">
          <h2 id="cta-title">Keep agent knowledge under human control.</h2>
          <p>Start with one workflow where a wrong conclusion could spread.</p>
          <div className="heroActions">
            <ButtonLink href={contactUrl}>Contact us <Arrow /></ButtonLink>
            <ButtonLink href={repoUrl} variant="secondary">Explore the repository</ButtonLink>
          </div>
        </section>
      </main>

      <footer>
        <a className="brand" href="#top" aria-label="Back to top">
          <img src="/logo-on-dark.svg" alt="" width="28" height="28" />
          <span>Proofpress</span>
        </a>
        <p>The governance layer for agent-produced knowledge.</p>
        <a href={repoUrl}>GitHub</a>
      </footer>
    </div>
  );
}
