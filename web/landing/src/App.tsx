import { ArrowRight01Icon } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { ButtonLink } from "./components/button";
import { ArchitectureDiagram } from "./components/architecture-diagram";
import { KnowledgeChart } from "./components/knowledge-chart";
import { Quickstart } from "./components/quickstart";

const repoUrl = "https://github.com/chenmingtang830/proofpress";
const contactUrl = "https://ancient-ball-940.notion.site/eacf21eef9b54c3287f72892cd024a1c?pvs=105";

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
          <a href="#how">How it works</a>
          <a href="#quickstart">Quick start</a>
          <a href={repoUrl}>GitHub</a>
        </nav>
      </header>

      <main id="main">
        <section className="hero" id="top" aria-labelledby="hero-title">
          <div className="heroCopy">
            <h1 id="hero-title">Govern what your agents learn.</h1>
            <p className="heroLead">
              Proofpress keeps evidence, scope, and authority attached before an agent’s
              conclusion becomes someone else’s premise.
            </p>
            <div className="heroActions" aria-label="Get started">
              <ButtonLink href="#quickstart">Run the local demo <Arrow /></ButtonLink>
              <ButtonLink href={repoUrl} variant="secondary">View GitHub</ButtonLink>
            </div>
          </div>
          <div className="heroFoot" aria-label="Proofpress principle">
            <p>Knowledge worth building on.</p>
            <div className="sealLine" aria-hidden="true"><span /></div>
          </div>
        </section>

        <section className="handoff" aria-labelledby="handoff-title">
          <div className="handoffHeading">
            <h2 id="handoff-title">Agent output is becoming organizational knowledge.</h2>
            <div className="handoffArgument">
              <p>
                As agents do more work, their conclusions become inputs to the next agent,
                decision, or system.
              </p>
              <p>
                Retrieval finds an answer. A trace shows its origin. Neither authorizes reuse.
              </p>
            </div>
          </div>
          <KnowledgeChart />
        </section>

        <section className="architecture" id="how" aria-labelledby="architecture-heading">
          <div className="sectionIntro">
            <h2 id="architecture-heading">Proofpress governs the handoff—not the agent.</h2>
            <p>
              Your runtimes do the work. Proofpress governs which conclusions may be reused.
            </p>
          </div>
          <ArchitectureDiagram />
        </section>

        <section className="quickstart" id="quickstart" aria-labelledby="quickstart-title">
          <div className="sectionIntro">
            <h2 id="quickstart-title">See the admission boundary locally.</h2>
            <p>
              Run a synthetic demo locally—no account, customer data, or model call required.
            </p>
          </div>
          <Quickstart />
        </section>

        <section className="available" aria-labelledby="available-title">
          <div className="sectionIntro">
            <h2 id="available-title">Built for your agents. Governed by your owner.</h2>
            <p>
              Open source and provider-neutral, with Python, HTTP, MCP, and a single-owner review workspace.
            </p>
          </div>
          <dl className="capabilityList">
            <div><dt>Agents</dt><dd>Submit evidence, propose conclusions, and retrieve eligible context.</dd></div>
            <div><dt>Automated checks</dt><dd>Verify requirements and advise—without admission authority.</dd></div>
            <div><dt>Human owner</dt><dd>Controls what becomes reusable.</dd></div>
          </dl>
          <p className="boundaryNote">Current scope: local and experimental single-owner hosted operation. Design-partner outcomes remain unvalidated.</p>
          <div className="deploymentShapes" aria-label="Current deployment shapes">
            <div><strong>Local / offline</strong><span>Git-backed ledger and local review.</span></div>
            <div><strong>Experimental self-hosted</strong><span>Private, SQLite-backed, single-owner instance—not Proofpress Cloud.</span></div>
          </div>
        </section>

        <section className="finalCta" aria-labelledby="cta-title">
          <h2 id="cta-title">Tell us what your company is trying to solve.</h2>
          <p>Share your industry, the problem, and how Proofpress might help. Please omit sensitive data.</p>
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
