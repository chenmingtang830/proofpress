import {
  AiChemistry01Icon,
  AiInnovation01Icon,
  ArrowRight01Icon,
  ServiceIcon,
  Shield02Icon,
} from "@hugeicons/core-free-icons";
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
          <a href="#product">How it works</a>
          <a href="#teams">For teams</a>
          <a href="#evidence">Evidence</a>
          <a href="#quickstart">Evaluate</a>
          <a className="navContact" href="#partners">Let’s talk <Arrow /></a>
        </nav>
      </header>

      <main id="main">
        <section className="hero" id="top" aria-labelledby="hero-title">
          <div className="heroCopy">
            <h1 id="hero-title">
              Own your intelligence.
              <span className="heroQualifier">Verified. Governed. Cumulative.</span>
            </h1>
            <p className="heroLead">Trust infrastructure for RSI.</p>
            <div className="heroActions" aria-label="Get started">
              <ButtonLink href="#partners">Join as an early design partner <Arrow /></ButtonLink>
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
          <h2 id="why-title">Agents produce more knowledge than organizations can trust—or keep.</h2>
          <div className="problemFrame">
            <KnowledgeChart />
            <div className="handoffProblems" aria-label="Two failures behind the intelligence gap">
              <div className="handoffProblem">
                <span>UNVERIFIED</span>
                <h3>Output scales. Verification doesn’t.</h3>
                <p>Unsupported claims become the next agent’s premise.</p>
              </div>
              <div className="handoffProblem">
                <span>SCATTERED</span>
                <h3>Agents learn. Organizations forget.</h3>
                <p>Learnings disappear across runs, chats, traces, and documents.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="stackGap" id="stack-gap" aria-labelledby="stack-gap-title">
          <div className="sectionIntro sectionIntroSolo">
            <h2 id="stack-gap-title">Today’s stack captures pieces—not trusted intelligence.</h2>
          </div>
          <div className="stackGrid" aria-label="Limits of existing agent infrastructure">
            <div className="stackItem">
              <h3>Observability</h3>
              <p>Records activity.</p><small>Activity, not reusable knowledge.</small>
            </div>
            <div className="stackItem">
              <h3>Memory</h3>
              <p>Recalls history.</p><small>Recall, not durable learning.</small>
            </div>
            <div className="stackItem">
              <h3>Knowledge graphs &amp; ontologies</h3>
              <p>Maps relationships.</p><small>Structure, not verified knowledge.</small>
            </div>
          </div>
          <p className="stackConclusion">The missing layer is a governed record of what agents learned—and what future agents may trust and reuse.</p>
        </section>

        <section className="product" id="product" aria-labelledby="product-title">
          <div className="productIntro productIntroSolo">
            <div>
              <span className="eyebrow">Proofpress</span>
              <h2 id="product-title">The Intelligence Ledger for agent-native organizations.</h2>
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
              <div className="mechanismLabel mechanismLabelPropose"><span>Propose + evidence</span><div className="agentInterfaces"><b>MCP</b><b>CLI</b><b>Python</b><b>HTTP</b></div></div>
              <span className="mechanismLabel mechanismLabelGoverned">Governed context + feedback</span>
              <div className="productAgents">
                <span>ANY AGENT</span>
                <strong>Research</strong><strong>Code</strong><strong>Operations</strong>
              </div>
              <div className="mechanismValue"><span>Evaluate</span><span>Govern</span><span>Improve</span></div>
              <div className="ledgerStack" aria-label="A growing stack of governed intelligence records">
                <span className="ledgerGhost ledgerGhostOne" aria-hidden="true" />
                <span className="ledgerGhost ledgerGhostTwo" aria-hidden="true" />
                <span className="ledgerGhost ledgerGhostThree" aria-hidden="true" />
                <div className="ledgerPanel">
                  <div className="ledgerPanelHead"><img src="/logo.svg" alt="" width="28" height="28" /><span>INTELLIGENCE LEDGER</span><small>LIVE RECORD</small></div>
                  <div className="ledgerRecordMeta"><span>LR-204 · VERSION 03</span><b>ADMITTED</b></div>
                  <h3 id="ledger-system-title">Protocol B reduced processing time.</h3>
                  <div className="ledgerFacts">
                    <div><span>EVIDENCE</span><strong>4 sources</strong></div>
                    <div><span>EVALUATION</span><strong>2 assessments</strong></div>
                    <div><span>SCOPE</span><strong>Research workflows</strong></div>
                  </div>
                  <div className="ledgerHumanGate"><span>HUMAN ADMISSION</span><strong>Authorized for declared reuse</strong></div>
                  <div className="ledgerSignals">
                    <div><span>USED</span><strong>12 runs</strong></div>
                    <div><span>OUTCOMES</span><strong>5 observations</strong></div>
                  </div>
                </div>
              </div>
            </div>
            <figcaption id="ledger-system-note">Trust, use, and outcomes stay attached as intelligence moves across agents. · Illustrative record</figcaption>
          </figure>
        </section>

        <section className="intelligenceLoop" id="intelligence-loop" aria-labelledby="intelligence-loop-title">
          <div className="loopIntro loopIntroSolo">
            <h2 id="intelligence-loop-title">The engine for <span>continuous organizational learning.</span></h2>
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
            <div><span>START AHEAD</span><strong>Every agent begins with what the organization has learned.</strong></div>
            <div><span>LEARN FROM WORK</span><strong>Validated learnings improve the next run.</strong></div>
            <div><span>KEEP WHAT COMPOUNDS</span><strong>The intelligence stays with the organization.</strong></div>
          </div>
        </section>

        <section className="teams" id="teams" aria-labelledby="teams-title">
          <div className="sectionIntro sectionIntroSolo">
            <h2 id="teams-title">Built for teams where trust has consequences.</h2>
          </div>
          <div className="icpGrid" aria-label="Current target teams">
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={AiInnovation01Icon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>AI NeoLabs</h3>
              <p>Long-horizon, multi-agent research where findings compound across runs.</p>
            </div>
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={ServiceIcon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>AI-native services</h3>
              <p>Legal, accounting, and consulting work reviewed across agents, experts, and clients.</p>
            </div>
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={Shield02Icon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>Regulated vertical AI</h3>
              <p>Banking, insurance, and healthcare workflows with strict review and accountability.</p>
            </div>
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={AiChemistry01Icon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>Knowledge-intensive R&amp;D</h3>
              <p>Pharmaceuticals and biotech, where evidence moves from experiments to decisions.</p>
            </div>
          </div>
        </section>

        <section className="evidence" id="evidence" aria-labelledby="evidence-title">
          <div className="evidenceIntro evidenceIntroSolo">
            <div>
              <span className="evidenceEyebrow">Initial promising evidence · Harvey-style relay test</span>
              <h2 id="evidence-title">
                Higher completion.<br />Less unsafe propagation.
              </h2>
              <p className="evidenceMeta">Seven models · Three legal task families · Frozen paired study</p>
            </div>
          </div>
          <div className="study">
            <ModelResultsChart />
            <div className="studySummary">
              <div><strong>89.3 → 93.4%</strong><span>Rubric completion · 126 paired runs</span></div>
              <div><strong>8 → 0</strong><span>Observed unsafe propagation · 63 controlled stress pairs</span></div>
              <p>Proofpress-composed tasks derived from Harvey LAB public materials. Bounded mechanism evidence—not an official Harvey benchmark or a general efficacy claim.</p>
              <a href={resultsUrl}>Read the public results <Arrow /></a>
            </div>
          </div>
        </section>

        <section className="quickstart" id="quickstart" aria-labelledby="quickstart-title">
          <div className="compactIntro">
            <h2 id="quickstart-title">Evaluate Proofpress in your environment.</h2>
          </div>
          <details className="evaluationDisclosure">
            <summary><span>Run the local evaluation</span><span className="evaluationMeta">3 steps <span aria-hidden="true">+</span></span></summary>
            <Quickstart />
          </details>
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
          <span className="eyebrow">Our mission</span>
          <h2 id="film-title">Knowledge worth building on.</h2>
          <video controls playsInline preload="metadata" poster="/proofpress-brand-film-poster.webp">
            <source src="/proofpress-brand-film.mp4" type="video/mp4" />
            Your browser does not support embedded video.
          </video>
        </section>

        <section className="finalCta" id="partners" aria-labelledby="cta-title">
          <div>
            <span className="eyebrow">Your agents are already learning</span>
            <h2 id="cta-title">Don’t waste your intelligence.</h2>
          </div>
          <div className="finalCtaAction">
            <p>Bring us one consequential agent workflow. We’ll help you turn its learnings into governed intelligence.</p>
            <ButtonLink href={contactUrl}>Become a design partner <Arrow /></ButtonLink>
          </div>
        </section>
      </main>

      <footer>
        <a className="brand" href="#top" aria-label="Back to top">
          <img src="/logo-on-dark.svg" alt="" width="28" height="28" />
          <span>Proofpress</span>
        </a>
        <p>The Intelligence Ledger for agent-native organizations.</p>
        <a href={repoUrl}>GitHub</a>
      </footer>
    </div>
  );
}
