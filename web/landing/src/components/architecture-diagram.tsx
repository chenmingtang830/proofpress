const surfaces = ["Python SDK", "CLI", "HTTP", "MCP"];

export function ArchitectureDiagram() {
  return (
    <figure className="architectureFigure" aria-labelledby="architecture-title architecture-note">
      <div className="architectureDiagram">
        <div className="architectureOrigin">
          <p className="diagramLabel">CUSTOMER-OWNED WORK</p>
          <div className="originFlow">
            <div>
              <strong>Documents, code, runs, systems</strong>
              <span>Raw work stays with you</span>
            </div>
            <span className="diagramArrow" aria-hidden="true">→</span>
            <div>
              <strong>Your agents and runtimes</strong>
              <span>Any provider or orchestrator</span>
            </div>
          </div>
        </div>

        <div className="projectionBridge">
          <span>bounded evidence projection</span>
          <i aria-hidden="true" />
        </div>

        <div className="proofpressKernel">
          <div className="kernelHeader">
            <div>
              <p className="diagramLabel">PROOFPRESS</p>
              <h3 id="architecture-title">One governance contract.</h3>
            </div>
            <div className="surfaceRail" aria-label="Current interfaces">
              {surfaces.map((surface) => <span key={surface}>{surface}</span>)}
            </div>
          </div>

          <ol className="kernelFlow">
            <li><span>01</span><strong>Evidence</strong><p>Bounded support, not raw traces.</p></li>
            <li><span>02</span><strong>Candidate conclusion</strong><p>A scoped claim with provenance.</p></li>
            <li><span>03</span><strong>Checks + advice</strong><p>Verification remains advisory.</p></li>
            <li className="ownerNode"><span>04 · AUTHORITY</span><strong>Human owner review</strong><p>The only step that can admit knowledge.</p></li>
            <li className="admittedNode"><span>05 · FILTER</span><strong>Governed context</strong><p>Only eligible knowledge.</p></li>
          </ol>

          <div className="kernelExit">
            <i aria-hidden="true" />
            <strong>Successor agent or human</strong>
            <span>Receives only eligible context</span>
          </div>
        </div>
      </div>
      <figcaption id="architecture-note">
        Agents can propose and read. Approval remains owner-only.
      </figcaption>
    </figure>
  );
}
