import React from "react";
import { Button } from "./ui/button";
import { Disclosure, DisclosureContent, DisclosureTrigger } from "./ui/disclosure";
import { Label } from "./ui/label";
import { NativeSelect } from "./ui/native-select";

type AgentClient = "codex" | "claude" | "cursor";
const clientNames = { codex: "Codex", claude: "Claude Code", cursor: "Cursor" };

function skillInstallation(client: AgentClient) {
  const directory = { codex: ".agents", claude: ".claude", cursor: ".cursor" }[client];
  return `skill_root=${directory}/skills/proofpress-governed-context
skill_source=https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context
mkdir -p "$skill_root/assets" "$skill_root/scripts"
for file in SKILL.md assets/context-policy.yaml assets/judge-criteria.md scripts/initialize_policy.py; do
  curl -fsSL "$skill_source/$file" -o "$skill_root/$file" || break
done`;
}

function ConnectionCommand({commands, label}: {commands: string; label: string}) {
  const [status, setStatus] = React.useState("");
  return <div className="connectionCommand">
    <Button variant="outline" size="sm" onClick={async () => {
      try { await navigator.clipboard.writeText(commands); setStatus("Copied"); }
      catch { setStatus("Copy failed. Select the commands and copy them manually."); }
    }}>{label}</Button>
    <pre><code>{commands}</code></pre>
    {status && <p role="status">{status}</p>}
  </div>;
}

export function AgentConnectionInstructions({client = "codex", installationOpen = false}: {client?: AgentClient; installationOpen?: boolean}) {
  const origin = typeof location === "undefined" ? "https://your-workspace.example" : location.origin;
  const commands = client === "codex" ? `codex mcp add proofpress --url ${origin}/mcp\ncodex mcp login proofpress`
    : client === "claude" ? `claude mcp add --transport http --scope user proofpress ${origin}/mcp`
    : JSON.stringify({mcpServers: {proofpress: {url: `${origin}/mcp`}}}, null, 2);
  return <section className="agentConnectionInstructions" aria-label={`Connect ${clientNames[client]}`}>
    <h3>Connect {clientNames[client]}</h3>
    <ol className="connectionSteps">
      <li><h4>Install the skill in your project</h4><p>The skill tells your agent how to use Proofpress. Open a terminal in your project’s root folder, then run the installation commands.</p>
        <Disclosure defaultOpen={installationOpen} className="skillInstallDisclosure"><DisclosureTrigger>Skill installation commands</DisclosureTrigger><DisclosureContent>
          <ConnectionCommand key={client} commands={skillInstallation(client)} label="Copy installation commands" />
          <p>These commands download the skill and its supporting files into <code>{client === "codex" ? ".agents" : client === "claude" ? ".claude" : ".cursor"}/skills/proofpress-governed-context</code>. If you already have this skill installed, skip this step.</p>
        </DisclosureContent></Disclosure></li>
      <li><h4>{client === "cursor" ? "Add the MCP server" : "Connect this workspace"}</h4>
        <p>{client === "cursor" ? "Add this configuration to .cursor/mcp.json in your project. Merge it with any existing servers." : "Run these commands in the same terminal after installing the skill."}</p>
        <ConnectionCommand key={commands} commands={commands} label={client === "cursor" ? "Copy configuration" : "Copy commands"} /></li>
      <li><h4>Authorize in the browser</h4><p>{client === "claude" ? "Open Claude Code and run /mcp to authorize Proofpress. " : client === "cursor" ? "Enable the Proofpress MCP server in Cursor and follow its authorization prompt. " : "Keep the terminal open. "}Use this agent’s API key when the authorization page opens. After connecting, start a fresh agent conversation so it can load the skill and tools.</p></li>
    </ol>
    {!installationOpen && <a className="otherClientsLink" href="/connect" target="_blank" rel="noreferrer">Setup for Claude Code or Cursor</a>}
  </section>;
}

export function ConnectionGuidePage() {
  const [client, setClient] = React.useState<AgentClient>("codex");
  return <main className="connectionGuidePage">
    <header className="connectionGuideBrand"><img src="/logo.svg" alt="" /><strong>Proofpress</strong></header>
    <h1>Connect your agent</h1>
    <p className="connectionGuideIntro">Install the skill, connect this workspace, then authorize with your agent’s API key. You do not need to run a Proofpress server locally.</p>
    <Label className="connectionClientChoice">Your agent client<NativeSelect aria-label="Your agent client" value={client} onChange={event=>setClient(event.target.value as AgentClient)}><option value="codex">Codex</option><option value="claude">Claude Code</option><option value="cursor">Cursor</option></NativeSelect></Label>
    <AgentConnectionInstructions key={client} client={client} installationOpen />
    <footer><p>Need an API key? Ask your workspace owner to issue one in Admin → API keys &amp; credentials. Use a separate key for each agent or device.</p><a href="/admin?section=access">Open workspace Admin</a></footer>
  </main>;
}

export function WorkspaceSetup({canManage, compact = false, policyConfigured = false, hasAgent, agentAccessReady = true, onConnect, onPolicy, onRefresh}: {
  canManage: boolean; compact?: boolean; policyConfigured?: boolean; hasAgent: boolean; agentAccessReady?: boolean;
  onConnect: () => void; onPolicy: () => void; onRefresh?: () => void;
}) {
  if (compact) return <section className="workspaceSetup workspaceSetup--compact" aria-labelledby="workspace-setup-title">
    <div><h2 id="workspace-setup-title">Confirm your review policy</h2>
      <p>You can create agent credentials now. Confirm verification settings below before submitting findings.</p></div>
    <Button variant="outline" onClick={onPolicy}>Set up verification</Button>
  </section>;
  return <section className="workspaceSetup" aria-labelledby="workspace-setup-title">
    <h1 id="workspace-setup-title">Bring your first finding into Proofpress</h1>
    <p>Connect your agent, confirm how findings are reviewed, then review a real candidate.</p>
    {!canManage ? <p role="status">{policyConfigured ? "No findings yet. Ask an agent to submit one with evidence, then review it here." : "Your workspace owner needs to confirm the review policy before knowledge work can begin."}</p> : <ol className="setupSteps">
      <li><div><h2>Create agent access</h2><p>{!agentAccessReady ? "Check which agents already have access before issuing a new key." : hasAgent ? "An agent credential is available. Complete the connection in your client." : "Give your agent its own revocable credential and connect it to this workspace."}</p></div>
        <Button variant={hasAgent || !agentAccessReady ? "outline" : "default"} onClick={onConnect}>{!agentAccessReady ? "Check agent access" : hasAgent ? "Manage agent access" : "Create agent credential"}</Button></li>
      <li><div><h2>Confirm verification settings</h2><p>{policyConfigured ? "Your verification settings are active. Only eligible findings can become reusable knowledge." : "Start with a human decision for each finding. Model review can be configured later."}</p></div>
        {!policyConfigured && <Button variant="outline" onClick={onPolicy}>Set up verification</Button>}
        {policyConfigured && <span className="setupStatus">Policy active</span>}</li>
      <li><div><h2>Review your first finding</h2><p>Ask your connected agent to submit one real finding with bounded evidence. After your approval, ask a later run to retrieve it.</p></div>
        {policyConfigured && onRefresh && <Button variant="outline" onClick={onRefresh}>Check for a finding</Button>}</li>
    </ol>}
    {canManage && <Disclosure><DisclosureTrigger>Connection instructions</DisclosureTrigger><DisclosureContent><AgentConnectionInstructions /></DisclosureContent></Disclosure>}
  </section>;
}
