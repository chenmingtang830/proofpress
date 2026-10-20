import React from "react";
import { Button } from "./ui/button";
import { Disclosure, DisclosureContent, DisclosureTrigger } from "./ui/disclosure";

export function AgentConnectionInstructions() {
  const origin = typeof location === "undefined" ? "https://your-workspace.example" : location.origin;
  return <div className="agentConnectionInstructions">
    <h3>Connect Codex</h3>
    <p>Install the Proofpress governed-context skill in your project, then run:</p>
    <pre><code>{`codex mcp add proofpress --url ${origin}/mcp\ncodex mcp login proofpress`}</code></pre>
    <p>Keep the terminal open. In the browser, authorize with this agent’s credential.</p>
    <a href="/connect" target="_blank" rel="noreferrer">Skill installation and other clients</a>
  </div>;
}

export function WorkspaceSetup({canManage, compact = false, policyConfigured = false, hasAgent, onConnect, onPolicy, onRefresh}: {
  canManage: boolean; compact?: boolean; policyConfigured?: boolean; hasAgent: boolean;
  onConnect: () => void; onPolicy: () => void; onRefresh?: () => void;
}) {
  if (compact) return <section className="workspaceSetup workspaceSetup--compact" aria-labelledby="workspace-setup-title">
    <div><h2 id="workspace-setup-title">Confirm your review policy</h2>
      <p>You can create agent credentials now. Confirm human review below before submitting findings.</p></div>
    <Button variant="outline" onClick={onPolicy}>Choose review policy</Button>
  </section>;
  return <section className="workspaceSetup" aria-labelledby="workspace-setup-title">
    <h1 id="workspace-setup-title">Bring your first finding into Proofpress</h1>
    <p>Connect your agent, confirm how findings are reviewed, then review a real candidate.</p>
    {!canManage ? <p role="status">Your workspace owner needs to confirm the review policy before knowledge work can begin.</p> : <ol className="setupSteps">
      <li><div><h2>Create agent access</h2><p>{hasAgent ? "An agent credential is available. Complete the connection in your client." : "Give your agent its own revocable credential and connect it to this workspace."}</p></div>
        <Button variant={hasAgent ? "outline" : "default"} onClick={onConnect}>{hasAgent ? "Manage agent access" : "Create agent credential"}</Button></li>
      <li><div><h2>Confirm human review</h2><p>{policyConfigured ? "Your review policy is active. Only eligible findings can become reusable knowledge." : "Start with a human decision for each finding. Model review can be configured later."}</p></div>
        {!policyConfigured && <Button variant="outline" onClick={onPolicy}>Choose review policy</Button>}
        {policyConfigured && <span className="setupStatus">Policy active</span>}</li>
      <li><div><h2>Review your first finding</h2><p>Ask your connected agent to submit one real finding with bounded evidence. After your approval, ask a later run to retrieve it.</p></div>
        {policyConfigured && onRefresh && <Button variant="outline" onClick={onRefresh}>Check for a finding</Button>}</li>
    </ol>}
    {canManage && <Disclosure><DisclosureTrigger>Connection instructions</DisclosureTrigger><DisclosureContent><AgentConnectionInstructions /></DisclosureContent></Disclosure>}
  </section>;
}
