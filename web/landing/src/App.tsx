import {
  AiChemistry01Icon,
  AiInnovation01Icon,
  AlertDiamondIcon,
  ArrowDataTransferHorizontalIcon,
  ArrowRight01Icon,
  LinkOffIcon,
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
            <h1 id="hero-title">When output is infinite, trust is the bottleneck.</h1>
            <p className="heroLead">
              Proofpress verifies and governs agent-produced knowledge so other people and agents can rely on it.
            </p>
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
          <h2 id="why-title">Agent work compounds. Trust has to keep up.</h2>
          <KnowledgeChart />
        </section>

        <section className="problems" aria-labelledby="problems-title">
          <div className="sectionIntro">
            <h2 id="problems-title">Trust breaks at the handoff.</h2>
            <p>Agents inherit conclusions faster than they can verify them.</p>
          </div>
          <div className="handoffProblems" aria-label="Problems Proofpress addresses">
            <div className="handoffProblem">
              <HugeiconsIcon className="problemIcon" icon={ArrowDataTransferHorizontalIcon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>Lost reasoning</h3>
              <p>The conclusion survives. The reasoning does not.</p>
            </div>
            <div className="handoffProblem">
              <HugeiconsIcon className="problemIcon" icon={LinkOffIcon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>Scattered evidence</h3>
              <p>Sources, scope, and review decisions live apart.</p>
            </div>
            <div className="handoffProblem">
              <HugeiconsIcon className="problemIcon" icon={AlertDiamondIcon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>Errors propagate</h3>
              <p>One bad claim shapes every step that follows.</p>
            </div>
          </div>
        </section>

        <section className="stackGap" id="stack-gap" aria-labelledby="stack-gap-title">
          <div className="sectionIntro">
            <h2 id="stack-gap-title">Retrieval is not a trust decision.</h2>
            <p>Your stack holds the knowledge. Your organization still needs to decide what agents may rely on.</p>
          </div>
          <div className="stackGrid" aria-label="Limits of existing agent infrastructure">
            <div className="stackItem">
              <h3>Traces</h3>
              <p>Record what happened.</p><small>Which conclusions should carry forward?</small>
            </div>
            <div className="stackItem">
              <h3>Memory</h3>
              <p>Retrieve past work.</p><small>Is this claim still fit for this use?</small>
            </div>
            <div className="stackItem">
              <h3>Knowledge graphs</h3>
              <p>Structure and govern enterprise knowledge.</p><small>Who admits a new agent-produced claim?</small>
            </div>
          </div>
        </section>

        <section className="product" id="product" aria-labelledby="product-title">
          <div className="productIntro">
            <div>
              <span className="eyebrow">How Proofpress works</span>
              <h2 id="product-title">Turn agent output into governed knowledge.</h2>
            </div>
            <p>Bind proof. Run checks. Require human admission.</p>
          </div>
          <div className="mechanismSteps" aria-label="Proofpress governance lifecycle">
            <div><span>01</span><h3>Bind evidence</h3><p>Keep the source, scope, and version.</p></div>
            <div><span>02</span><h3>Propose a claim</h3><p>State what others may rely on.</p></div>
            <div><span>03</span><h3>Human gate</h3><p>Admit, reject, or request revision.</p></div>
            <div><span>04</span><h3>Govern reuse</h3><p>Return admitted knowledge within its limits.</p></div>
          </div>
          <div className="handoffExample" aria-labelledby="handoff-example-title">
            <div className="exampleContext">
              <h3 id="handoff-example-title">One finding.<br />More than one team.</h3>
              <p>A research agent finds a result. A specialist reviews its evidence and sets the limits. A planning team can then use that finding within those limits.</p>
              <span>Illustrative workflow · synthetic evidence</span>
            </div>
            <article className="claimSpecimen">
              <div className="claimHeading"><span>Research → Planning</span><span className="claimState">Admitted for a limited use</span></div>
              <h4>Protocol B reduced processing time in the pilot.</h4>
              <dl>
                <div><dt>Proposed by</dt><dd>Research agent</dd></div>
                <div><dt>Admitted by</dt><dd>Research lead · after evidence review</dd></div>
                <div><dt>May support</dt><dd>Planning the next pilot</dd></div>
                <div><dt>Does not support</dt><dd>A production rollout or a claim of clinical benefit</dd></div>
              </dl>
              <details className="specimenEvidence">
                <summary>Inspect the attached evidence <span aria-hidden="true">+</span></summary>
                <p>Pilot report v2 · 12 synthetic runs · identical test conditions. The observed result applies only to this pilot protocol.</p>
              </details>
              <p className="claimFoot">The next team receives the finding, its evidence, and its limits together.</p>
            </article>
          </div>
        </section>

        <section className="architecture" id="architecture" aria-labelledby="architecture-title">
          <div className="sectionIntro">
            <h2 id="architecture-title">From evidence to trusted reuse.</h2>
            <p>One governed path. Four ways to connect.</p>
          </div>
          <div className="simpleArchitecture" aria-label="Evidence passes through three Proofpress gates, then reaches agents and human teams through four interfaces">
            <div className="architectureNode evidenceNode">
              <span>Input</span>
              <h3>Evidence</h3>
              <i aria-hidden="true" />
              <p>Source · scope · version</p>
            </div>
            <div className="architectureArrow" aria-hidden="true">→</div>
            <div className="proofpressNode">
              <div className="architectureNodeHead">
                <h3>Proofpress</h3>
                <span>Three gates</span>
              </div>
              <ol>
                <li>Policy checks</li>
                <li>Model review <small>Advisory</small></li>
                <li>Human admission</li>
              </ol>
              <p>Only a human admits.</p>
            </div>
            <div className="architectureArrow" aria-hidden="true">→</div>
            <div className="architectureNode interfaceNode">
              <span>Interfaces</span>
              <div className="interfaceGrid" aria-label="Supported interfaces">
                <b>MCP</b><b>Python</b><b>CLI</b><b>HTTP</b>
              </div>
            </div>
            <div className="architectureArrow" aria-hidden="true">→</div>
            <div className="architectureNode receiverNode">
              <span>Reuse</span>
              <h3>Agents +<br />human teams</h3>
              <i aria-hidden="true" />
              <p>Admitted · current · in scope</p>
            </div>
          </div>
        </section>

        <section className="teams" id="teams" aria-labelledby="teams-title">
          <div className="sectionIntro">
            <h2 id="teams-title">Built for teams where trust has consequences.</h2>
            <p>Our current focus is work that crosses agent–human boundaries and carries material cost when it is wrong.</p>
          </div>
          <div className="icpGrid" aria-label="Current target teams">
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={AiInnovation01Icon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>AI NeoLabs</h3>
              <p>Long-horizon, multi-agent research where findings compound across runs.</p>
            </div>
            <div className="icpItem">
              <HugeiconsIcon className="problemIcon" icon={ServiceIcon} size={30} strokeWidth={1.5} aria-hidden="true" />
              <h3>AI-native professional services</h3>
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
          <div className="evidenceIntro">
            <div>
              <span className="evidenceEyebrow">Harvey-style relay test</span>
              <h2 id="evidence-title">
                Higher completion.<br />Less unsafe propagation.
              </h2>
            </div>
            <p>
              Seven models. Three legal task families. We compared ordinary handoffs with Proofpress’s governed claims ledger in a frozen, paired study.
            </p>
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

        <section className="partners" id="partners" aria-labelledby="partners-title">
          <div className="partnerInvitation">
            <h2 id="partners-title">Build your first governed workflow with us.</h2>
            <p>We’re looking for early design partners: teams whose agent work becomes someone else’s next decision.</p>
            <ButtonLink href={contactUrl}>Contact us <Arrow /></ButtonLink>
            <small>Tell us about your workflow to start a conversation.</small>
          </div>
          <div className="partnerAgenda">
            <h3>Start with one consequential handoff.</h3>
            <p>We can discuss the evidence your team needs, who should review it, and what downstream use should be allowed.</p>
            <dl>
              <div><dt>Hosted &amp; managed</dt><dd>Explore a managed deployment with our team.</dd></div>
              <div><dt>Self-hosted</dt><dd>Explore running Proofpress in your environment.</dd></div>
            </dl>
          </div>
        </section>

        <section className="quickstart" id="quickstart" aria-labelledby="quickstart-title">
          <div className="compactIntro">
            <h2 id="quickstart-title">Evaluate Proofpress in your environment.</h2>
            <p>Run a local, synthetic workflow. No account or model call required.</p>
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
          <h2 id="film-title">Our vision: Knowledge worth building on.</h2>
          <video controls playsInline preload="metadata" poster="/proofpress-brand-film-poster.webp">
            <source src="/proofpress-brand-film.mp4" type="video/mp4" />
            Your browser does not support embedded video.
          </video>
        </section>

        <section className="finalCta" aria-labelledby="cta-title">
          <h2 id="cta-title">What will your next team rely on?</h2>
          <p>Bring one consequential workflow. Let’s discuss how your organization can govern it.</p>
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
