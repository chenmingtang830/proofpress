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
              Proofpress is the governance layer for agent-produced knowledge. It keeps evidence,
              scope, and authority attached before a conclusion becomes a premise for the next
              agent or human.
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
                The more work agents complete, the more their conclusions become premises for the
                next agent, decision, or system.
              </p>
              <p>
                Retrieval can find an old answer. A trace can show how it was produced. Neither
                decides whether anyone is authorized to rely on it now.
              </p>
            </div>
          </div>
          <KnowledgeChart />
        </section>

        <section className="architecture" id="how" aria-labelledby="architecture-heading">
          <div className="sectionIntro">
            <h2 id="architecture-heading">Proofpress governs the handoff—not the agent.</h2>
            <p>
              Your runtimes keep doing the work. Proofpress receives bounded evidence and candidate
              conclusions, preserves the review record, and filters what may be reused downstream.
            </p>
          </div>
          <ArchitectureDiagram />
        </section>

        <section className="quickstart" id="quickstart" aria-labelledby="quickstart-title">
          <div className="sectionIntro">
            <h2 id="quickstart-title">See the admission boundary locally.</h2>
            <p>
              Run a synthetic demo in a fresh temporary Git repository. No account, customer data,
              or external model call is required.
            </p>
          </div>
          <Quickstart />
        </section>

        <section className="available" aria-labelledby="available-title">
          <div className="sectionIntro">
            <h2 id="available-title">Built for your agents. Governed by your owner.</h2>
            <p>
              Proofpress is open source and provider-neutral. The current implementation supports
              a Python SDK, HTTP and MCP access, bounded evidence and proposals, and a single-owner
              workspace for review, lineage, credentials, and current governed context.
            </p>
          </div>
          <dl className="capabilityList">
            <div><dt>Agents</dt><dd>Submit evidence, propose conclusions, inspect lineage, and retrieve eligible context.</dd></div>
            <div><dt>Automated checks</dt><dd>Verify declared requirements and provide advisory evaluation without admission authority.</dd></div>
            <div><dt>Human owner</dt><dd>Approves, requests changes, rejects, and controls what becomes reusable.</dd></div>
          </dl>
          <p className="boundaryNote">Current scope: local and experimental single-owner hosted operation. Design-partner outcomes remain unvalidated.</p>
          <div className="deploymentShapes" aria-label="Current deployment shapes">
            <div><strong>Local / offline</strong><span>Git-backed ledger and local review.</span></div>
            <div><strong>Experimental self-hosted</strong><span>Private, SQLite-backed, single-owner instance—not Proofpress Cloud.</span></div>
          </div>
        </section>

        <section className="finalCta" aria-labelledby="cta-title">
          <h2 id="cta-title">Tell us where downstream reliance matters.</h2>
          <p>Share one workflow through our short Notion form. Do not include confidential, privileged, personal, or customer data.</p>
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
