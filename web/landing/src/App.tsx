import { useEffect, useRef, useState } from "react";
import {
  AiInnovation01Icon,
  ArrowRight01Icon,
  GitCompareIcon,
  Shield02Icon,
} from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { Button, ButtonLink } from "./components/button";
import { KnowledgeChart } from "./components/knowledge-chart";
import posts from "./content/post-index.json";

const repoUrl = "https://github.com/chenmingtang830/proofpress";
const contactUrl = "https://ancient-ball-940.notion.site/eacf21eef9b54c3287f72892cd024a1c?pvs=105";
// Public media lives in Vercel Blob; source footage and renders stay out of Git.
const brandFilmUrl = "https://qj4v3hgnvu4pvbdd.public.blob.vercel-storage.com/films/proofpress-shoulders-20260910-1080p.mp4";

const featuredSlug = "agents-create-a-new-knowledge-layer";
const writing = [...posts].sort((a, b) => {
  if (a.slug === featuredSlug) return -1;
  if (b.slug === featuredSlug) return 1;
  return Date.parse(b.date) - Date.parse(a.date);
});

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
  const writingRail = useRef<HTMLDivElement>(null);
  const [railEdges, setRailEdges] = useState({ start: true, end: false });
  const syncRail = () => {
    const rail = writingRail.current;
    if (rail) setRailEdges({ start: rail.scrollLeft < 2, end: rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 2 });
  };
  useEffect(() => {
    const rail = writingRail.current;
    if (!rail) return;
    const observer = new ResizeObserver(syncRail);
    observer.observe(rail);
    syncRail();
    return () => observer.disconnect();
  }, []);
  const moveWriting = (direction: number) => {
    const rail = writingRail.current;
    const card = rail?.firstElementChild as HTMLElement | null;
    if (rail && card) rail.scrollBy({ left: direction * (card.offsetWidth + 24), behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
  };
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
          <table className="stackComparison">
            <thead><tr><th scope="col">Research tools</th><th scope="col">What they capture</th><th scope="col">What gets lost</th></tr></thead>
            <tbody>
              <tr><th scope="row">Observability</th><td data-label="What they capture">Traces &amp; execution</td><td data-label="What gets lost">Findings within the noise</td></tr>
              <tr><th scope="row">Experiment trackers</th><td data-label="What they capture">Runs, metrics &amp; artifacts</td><td data-label="What gets lost">What the team learned</td></tr>
              <tr><th scope="row">Papers &amp; reports</th><td data-label="What they capture">Selected findings</td><td data-label="What gets lost">Dead ends &amp; decision history</td></tr>
            </tbody>
          </table>
        </section>

        <section className="product" id="product" aria-labelledby="product-title">
          <div className="productIntro productIntroSolo">
            <div>
              <h2 id="product-title">The Intelligence Ledger for agent-native research teams.</h2>
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
            <div className="verificationDecision">
              <div className="verificationInputs">
                <p className="verificationRole">Inputs to the decision</p>
                <div><h4>Deterministic checks</h4><p>Reproducible checks against evidence and explicit requirements.</p></div>
                <div><h4>LM as a judge</h4><p>Assess findings against your organization’s configured review criteria.</p></div>
              </div>
              <div className="verificationConnector" aria-hidden="true"><Arrow /></div>
              <div className="verificationAuthority">
                <p className="verificationRole">Permission to reuse</p>
                <h4>Human review &amp; approval</h4>
                <p>Decide which findings may be reused, and where.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="intelligenceLoop" id="intelligence-loop" aria-labelledby="intelligence-loop-title">
          <div className="loopIntro loopIntroSolo">
            <h2 id="intelligence-loop-title">The learning loop.</h2>
            <p className="loopAnalogy">Self-evolving knowledge.</p>
          </div>
          <div className="learningSteps" aria-label="The learning cycle">
            <details name="learning-cycle" open>
              <summary><span className="learningNumber">01</span><h3>Use governed context</h3><span className="learningToggle" aria-hidden="true" /></summary>
              <p>Agents build new work and claims on admitted knowledge.</p>
            </details>
            <details name="learning-cycle">
              <summary><span className="learningNumber">02</span><h3>Evaluate outcomes</h3><span className="learningToggle" aria-hidden="true" /></summary>
              <p>Connect results to the knowledge and claims that shaped them.</p>
            </details>
            <details name="learning-cycle">
              <summary><span className="learningNumber">03</span><h3>Refine knowledge</h3><span className="learningToggle" aria-hidden="true" /></summary>
              <p>Use new evidence to reinforce, revise, or retire findings.</p>
            </details>
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
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={AiInnovation01Icon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>Applied AI teams</h3>
              <p>Carry evaluation conclusions and workflow learnings forward as systems and deployments evolve.</p>
            </div>
          </div>
        </section>

        <section className="writing" id="writing" aria-labelledby="writing-title">
          <div className="compactIntro">
            <h2 id="writing-title">Writing from the field.</h2>
            <a href="/blog">Read the blog <Arrow /></a>
          </div>
          <div className="writingNavigation" aria-label="Browse articles">
            <Button variant="secondary" aria-label="Previous articles" aria-controls="writing-rail" disabled={railEdges.start} onClick={() => moveWriting(-1)}><span className="previousArrow"><Arrow /></span></Button>
            <Button variant="secondary" aria-label="Next articles" aria-controls="writing-rail" disabled={railEdges.end} onClick={() => moveWriting(1)}><Arrow /></Button>
          </div>
          <div className="writingGrid" id="writing-rail" ref={writingRail} onScroll={syncRail} tabIndex={0} role="region" aria-label="Articles, featured first; scroll horizontally">
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
            <source src={brandFilmUrl} type="video/mp4" />
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
