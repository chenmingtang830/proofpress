import { ArrowRight01Icon } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { ButtonLink } from "./components/button";

const repoUrl = "https://github.com/chenmingtang830/proofpress";
const handoffUrl = `${repoUrl}/issues/new?template=design_partner.yml`;

function Arrow() {
  return <HugeiconsIcon icon={ArrowRight01Icon} size={18} strokeWidth={1.6} aria-hidden="true" />;
}

const steps = [
  ["Propose", "An agent submits a bounded candidate conclusion."],
  ["Verify", "Evidence, integrity checks, and policy advice stay inspectable."],
  ["Human approval", "The configured human decides whether the conclusion is admitted."],
  ["Rely", "Only admitted, current, in-scope knowledge reaches the next actor."],
];

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
          <a href="#available">What exists</a>
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
              <ButtonLink href={handoffUrl}>Bring a real handoff <Arrow /></ButtonLink>
              <ButtonLink href={repoUrl} variant="secondary">View GitHub</ButtonLink>
            </div>
          </div>
          <div className="heroFoot" aria-label="Proofpress principle">
            <p>Knowledge worth building on.</p>
            <div className="sealLine" aria-hidden="true"><span /></div>
          </div>
        </section>

        <section className="handoff" aria-labelledby="handoff-title">
          <h2 id="handoff-title">When output becomes input, trust has to travel with it.</h2>
          <div className="handoffArgument">
            <p>
              Retrieval can find an old conclusion. A trace can show how it was produced. Neither
              decides whether anyone is authorized to rely on it now.
            </p>
            <p>
              Proofpress makes that transition explicit: what supports the conclusion, where it
              applies, what changed, and who accepted responsibility for its reuse.
            </p>
          </div>
        </section>

        <section className="mechanism" id="how" aria-labelledby="mechanism-title">
          <div className="sectionIntro">
            <h2 id="mechanism-title">A visible path to reliance.</h2>
            <p>Checks and model advice can support a decision. Only human approval admits knowledge.</p>
          </div>
          <ol className="trustPath">
            {steps.map(([title, detail], index) => (
              <li key={title} className={index === 2 ? "humanGate" : ""}>
                <span className="stepIndex">{String(index + 1).padStart(2, "0")}</span>
                <h3>{title}</h3>
                <p>{detail}</p>
              </li>
            ))}
          </ol>
        </section>

        <section className="available" id="available" aria-labelledby="available-title">
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
        </section>

        <section className="finalCta" aria-labelledby="cta-title">
          <h2 id="cta-title">Bring the handoff your team cannot afford to get wrong.</h2>
          <p>Start with one real workflow. Do not include confidential, privileged, personal, or customer data.</p>
          <div className="heroActions">
            <ButtonLink href={handoffUrl}>Bring a real handoff <Arrow /></ButtonLink>
            <ButtonLink href={repoUrl} variant="secondary">Explore the repository</ButtonLink>
          </div>
        </section>
      </main>

      <footer>
        <a className="brand" href="#top" aria-label="Back to top">
          <img src="/logo.svg" alt="" width="28" height="28" />
          <span>Proofpress</span>
        </a>
        <p>The governance layer for agent-produced knowledge.</p>
        <a href={repoUrl}>GitHub</a>
      </footer>
    </div>
  );
}
