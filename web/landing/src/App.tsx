import {
  AiInnovation01Icon,
  ArrowRight01Icon,
  GitCompareIcon,
  Shield02Icon,
} from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { ButtonLink } from "./components/button";
import { KnowledgeChart } from "./components/knowledge-chart";
import posts from "./content/post-index.json";

const repoUrl = "https://github.com/chenmingtang830/proofpress";
const contactUrl = "https://ancient-ball-940.notion.site/eacf21eef9b54c3287f72892cd024a1c?pvs=105";

const writing = [...posts]
  .sort((a, b) => Date.parse(b.date) - Date.parse(a.date))
  .slice(0, 3);

function Arrow() {
  return <HugeiconsIcon icon={ArrowRight01Icon} size={18} strokeWidth={1.6} aria-hidden="true" />;
}

function closeMobileNav(event: React.MouseEvent<HTMLAnchorElement>) {
  event.currentTarget.closest("details")?.removeAttribute("open");
}

function LedgerDetails({ mobile = false }: { mobile?: boolean }) {
  const details = (
    <>
      <div className="ledgerFacts">
        <div><span>EVIDENCE</span><strong>4 sources</strong></div>
        <div><span>EVALUATION</span><strong>2 assessments</strong></div>
        <div><span>SCOPE</span><strong>Tested model, dataset &amp; harness</strong></div>
      </div>
      <div className="ledgerHumanGate"><span>HUMAN APPROVAL</span><strong>Admitted for declared reuse: next-experiment planning</strong></div>
      <div className="ledgerSignals">
        <div><span>USED</span><strong>12 runs</strong></div>
        <div><span>OUTCOMES</span><strong>5 observations</strong></div>
      </div>
    </>
  );

  return mobile ? (
    <details className="ledgerDisclosure">
      <summary>View evidence and reuse scope</summary>
      <div className="ledgerDisclosureBody">{details}</div>
    </details>
  ) : <div className="ledgerDesktopDetails">{details}</div>;
}

const formatArticleDate = (date: string) => new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
  year: "numeric",
  timeZone: "UTC",
}).format(new Date(date));

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
          <a href="#product">How it works</a>
          <a href="#teams">For teams</a>
          <a href="/blog">Blog</a>
          <a href={`${repoUrl}#quick-start`}>Docs</a>
          <a className="navContact" href="#partners">Let’s talk <Arrow /></a>
        </nav>
        <details className="mobileNav">
          <summary aria-label="Open navigation">Menu</summary>
          <nav aria-label="Mobile navigation">
            <a href="#product" onClick={closeMobileNav}>How it works</a>
            <a href="#teams" onClick={closeMobileNav}>For teams</a>
            <a href="/blog" onClick={closeMobileNav}>Blog</a>
            <a href={`${repoUrl}#quick-start`} onClick={closeMobileNav}>Docs</a>
          </nav>
        </details>
      </header>

      <main id="main">
        <section className="hero" id="top" aria-labelledby="hero-title">
          <div className="heroCopy">
            <h1 id="hero-title">
              Verified knowledge<br /> infrastructure.
            </h1>
            <p className="heroAudience">For agent-native research teams.</p>
            <p className="heroLead">Turn research output into knowledge your team can build on.</p>
            <div className="heroActions" aria-label="Get started">
              <ButtonLink href="#partners">Explore a design partnership <Arrow /></ButtonLink>
              <ButtonLink href={repoUrl} variant="secondary">Explore open source on GitHub</ButtonLink>
            </div>
          </div>
          <div className="heroFoot" aria-label="Proofpress product attributes">
            <span>Open source</span>
            <span>Self-hostable</span>
            <span>Human-gated</span>
          </div>
        </section>

        <section className="why" aria-labelledby="why-title">
          <h2 id="why-title">Agents produce more knowledge than researchers can verify—or keep.</h2>
          <div className="problemFrame">
            <KnowledgeChart />
            <div className="handoffProblems" aria-label="Two failures behind the intelligence gap">
              <div className="handoffProblem">
                <span>UNVERIFIED</span>
                <h3>Output scales. Verification doesn’t.</h3>
                <p>Claims travel without evidence, review, or clear limits.</p>
              </div>
              <div className="handoffProblem">
                <span>SCATTERED</span>
                <h3>Agents learn. Research teams forget.</h3>
                <p>Dead ends disappear. Teams repeat them.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="stackGap" id="stack-gap" aria-labelledby="stack-gap-title">
          <div className="sectionIntro sectionIntroSolo">
            <h2 id="stack-gap-title">The research stack captures the work. It still loses the learning.</h2>
          </div>
          <div className="stackGrid" aria-label="Where research learning is lost across the existing stack">
            <div className="stackItem">
              <h3>Observability</h3>
              <p>Raw traces and execution details.</p><small>More activity creates a larger sea of signals.</small>
            </div>
            <div className="stackItem">
              <h3>Experiment trackers</h3>
              <p>Runs, metrics, and artifacts.</p><small>They organize experiments—not what the team learned.</small>
            </div>
            <div className="stackItem">
              <h3>Papers &amp; reports</h3>
              <p>Selected, distilled findings.</p><small>Much of the failed work, scope, and decision history is left behind.</small>
            </div>
          </div>
          <p className="stackConclusion">Across the gaps, valuable learnings and dead ends disappear before the next research cycle can build on them.</p>
        </section>

        <section className="product" id="product" aria-labelledby="product-title">
          <div className="productIntro productIntroSolo">
            <div>
              <h2 id="product-title">The Intelligence Ledger for agent-native research labs.</h2>
            </div>
          </div>
          <figure className="productSystem" aria-labelledby="ledger-system-title" aria-describedby="ledger-system-note">
            <div className="productMechanism">
              <svg className="mechanismLoop mechanismLoopDesktop" viewBox="0 0 600 500" aria-hidden="true">
                <defs><marker id="mechanism-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto"><path d="M0 0L10 5L0 10Z" /></marker></defs>
                <path d="M0 185C150 20 450 20 600 185" markerEnd="url(#mechanism-arrow)" />
                <path d="M600 315C450 480 150 480 0 315" markerEnd="url(#mechanism-arrow)" />
              </svg>
              <svg className="mechanismLoop mechanismLoopMobile" viewBox="0 0 320 900" preserveAspectRatio="none" aria-hidden="true">
                <defs><marker id="mechanism-arrow-mobile" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" /></marker></defs>
                <path d="M52 170C10 260 10 650 58 730" markerEnd="url(#mechanism-arrow-mobile)" />
                <path d="M262 730C310 650 310 260 268 170" markerEnd="url(#mechanism-arrow-mobile)" />
              </svg>
              <div className="mechanismLabel mechanismLabelPropose"><div className="mechanismActions"><span>Propose claims</span><span>Attach evidence</span></div><div className="agentInterfaces"><b>MCP</b><b>CLI</b><b>Python</b><b>HTTP</b></div></div>
              <span className="mechanismLabel mechanismLabelGoverned">Governed context</span>
              <div className="productAgents">
                <span>ANY AGENT</span>
                <strong>Experimentation</strong><strong>Evaluation</strong><strong>Analysis</strong>
              </div>
              <div className="mechanismValue">Research cycle</div>
              <div className="ledgerStack" aria-label="A growing stack of governed intelligence records">
                <span className="ledgerGhost ledgerGhostOne" aria-hidden="true" />
                <span className="ledgerGhost ledgerGhostTwo" aria-hidden="true" />
                <span className="ledgerGhost ledgerGhostThree" aria-hidden="true" />
                <div className="ledgerPanel">
                  <div className="ledgerPanelHead"><img src="/logo.svg" alt="" width="28" height="28" /><span>INTELLIGENCE LEDGER</span><small>LIVE RECORD</small></div>
                  <div className="ledgerRecordMeta"><span>LR-204 · VERSION 03</span><b>ADMITTED</b></div>
                  <h3 id="ledger-system-title">Harness B improved performance on the evaluated task set.</h3>
                  <LedgerDetails />
                  <LedgerDetails mobile />
                </div>
              </div>
            </div>
            <div className="productSystemFooter">
              <p className="productClosingStatement">Verified. Governed. Cumulative.</p>
              <figcaption id="ledger-system-note">Evidence, scope, approval, use, and outcomes stay attached to the claim. · Illustrative record</figcaption>
            </div>
          </figure>
          <div className="verificationFlow">
            <h3>Verification informs the decision. Human Approval authorizes reuse.</h3>
            <div className="stackGrid">
              <div className="stackItem"><h3>Deterministic checks</h3><p>Reproducible checks against evidence and explicit requirements.</p></div>
              <div className="stackItem"><h3>LM as a judge</h3><p>Assess findings against your organization’s configured review criteria.</p></div>
              <div className="stackItem"><h3>Human review &amp; approval</h3><p>Decide which findings may be reused, and where.</p></div>
            </div>
          </div>
        </section>

        <section className="intelligenceLoop" id="intelligence-loop" aria-labelledby="intelligence-loop-title">
          <div className="loopIntro loopIntroSolo">
            <h2 id="intelligence-loop-title">The learning loop.</h2>
          </div>
          <svg className="compoundingGraph" viewBox="0 0 1440 620" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
            <g className="graphEdges">
              <path d="M80 402L188 336L252 438L188 506L80 402M188 336L252 438" />
              <path d="M252 438L418 318L514 404L604 276L706 384L790 250" />
              <path d="M418 318L484 220L604 276M514 404L620 502L706 384M604 276L690 180L790 250" />
              <path d="M790 250L906 192L982 286L1080 178L1174 268L1296 202L1372 292" />
              <path d="M706 384L850 442L982 286L1062 404L1174 268L1248 430L1372 292" />
              <path d="M850 442L942 524L1062 404L1144 516L1248 430L1354 506" />
              <path d="M906 192L970 112L1080 178L1162 96L1296 202M982 286L1080 178M1062 404L1174 268M1144 516L1248 430" />
            </g>
            <g className="graphNodes">
              <circle cx="80" cy="402" r="7" /><circle cx="188" cy="336" r="9" /><circle cx="252" cy="438" r="8" /><circle cx="188" cy="506" r="6" />
              <circle cx="418" cy="318" r="8" /><circle cx="484" cy="220" r="6" /><circle cx="514" cy="404" r="10" /><circle cx="604" cy="276" r="8" /><circle cx="620" cy="502" r="6" /><circle cx="690" cy="180" r="7" /><circle cx="706" cy="384" r="11" /><circle cx="790" cy="250" r="8" />
              <circle cx="850" cy="442" r="8" /><circle cx="906" cy="192" r="10" /><circle cx="942" cy="524" r="6" /><circle cx="970" cy="112" r="7" /><circle cx="982" cy="286" r="12" /><circle cx="1062" cy="404" r="9" /><circle cx="1080" cy="178" r="11" /><circle cx="1144" cy="516" r="7" /><circle cx="1162" cy="96" r="6" /><circle cx="1174" cy="268" r="13" /><circle cx="1248" cy="430" r="11" /><circle cx="1296" cy="202" r="9" /><circle cx="1354" cy="506" r="7" /><circle cx="1372" cy="292" r="10" />
            </g>
          </svg>
          <div className="organizationStory" aria-label="The long-term outcome of continuous organizational learning">
            <div><span>01 USE GOVERNED CONTEXT</span><strong>Agents build new work and claims on admitted knowledge.</strong></div>
            <div><span>02 EVALUATE OUTCOMES</span><strong>Connect results to the knowledge and claims that shaped them.</strong></div>
            <div><span>03 REFINE KNOWLEDGE</span><strong>Use new evidence to reinforce, revise, or retire findings.</strong></div>
          </div>
          <p className="organizationOutcome">A trusted foundation for recursive self-improvement.</p>
        </section>

        <section className="teams" id="teams" aria-labelledby="teams-title">
          <div className="sectionIntro sectionIntroSolo">
            <h2 id="teams-title">For teams advancing AI.</h2>
            <p className="narrativeLead">Produce knowledge the next researcher or agent can build on.</p>
          </div>
          <div className="icpGrid" aria-label="Current target teams">
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={AiInnovation01Icon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>AI research labs</h3>
              <p>Carry findings across researchers, agents, and experiments.</p>
            </div>
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={GitCompareIcon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>Benchmark &amp; evaluation teams</h3>
              <p>Preserve evaluation conclusions as models, datasets, and harnesses change.</p>
            </div>
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={Shield02Icon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>Post-training teams</h3>
              <p>Keep fine-tuning findings, model decisions, and failed approaches available for the next cycle.</p>
            </div>
          </div>
        </section>

        <section className="writing" id="writing" aria-labelledby="writing-title">
          <div className="compactIntro">
            <h2 id="writing-title">Writing from the field.</h2>
            <a href="/blog">Read the blog <Arrow /></a>
          </div>
          <div className="writingGrid">
            {writing.map((item) => (
              <a className="writingCard" href={`/blog/${item.slug}`} key={item.slug}>
                <div className="writingImage">
                  <img
                    src={item.image}
                    alt=""
                    width={1600}
                    height={900}
                    loading="lazy"
                    decoding="async"
                  />
                </div>
                <span>{item.label} · {formatArticleDate(item.date)}</span>
                <h3>{item.title}</h3>
                <small>Read article <Arrow /></small>
              </a>
            ))}
          </div>
        </section>

        <section className="film" aria-labelledby="film-title">
          <span className="eyebrow">Our mission</span>
          <h2 id="film-title">Knowledge worth building on.</h2>
          <video controls playsInline preload="metadata" poster="/proofpress-shoulders-poster-20260910.webp">
            <source src="/proofpress-shoulders-film-20260910-1080p.mp4" type="video/mp4" />
            Your browser does not support embedded video.
          </video>
        </section>

        <section className="finalCta" id="partners" aria-labelledby="cta-title">
          <div>
            <span className="eyebrow">Your experiments already produce learnings</span>
            <h2 id="cta-title">Don’t waste your intelligence.</h2>
          </div>
          <div className="finalCtaAction">
            <p>Show us one research workflow—and where its findings get lost between runs.</p>
            <ButtonLink href={contactUrl}>Share a research workflow <Arrow /></ButtonLink>
          </div>
        </section>
      </main>

      <footer>
        <a className="brand" href="#top" aria-label="Back to top">
          <img src="/logo-on-dark.svg" alt="" width="28" height="28" />
          <span>Proofpress</span>
        </a>
        <div className="footerIdentity">
          <small>by <span>Only Then Labs</span></small>
        </div>
        <a href={repoUrl}>GitHub</a>
      </footer>
    </div>
  );
}
