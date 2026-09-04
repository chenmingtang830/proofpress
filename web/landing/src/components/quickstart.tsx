import { useState } from "react";

const skillCommand = `SKILL_DIR=.agents/skills/proofpress-governed-context
mkdir -p "$SKILL_DIR"
curl -fsSL \\
  https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/SKILL.md \\
  -o "$SKILL_DIR/SKILL.md"`;
const installCommand = `uv tool install --with "mcp>=2,<3" "git+https://github.com/chenmingtang830/proofpress.git"`;
const quickstartCommand = `proofpress quickstart`;

function CopyButton({ command, label }: { command: string; label: string }) {
  const [copyStatus, setCopyStatus] = useState<"idle" | "copied" | "failed">("idle");

  async function copyCommand() {
    try {
      await navigator.clipboard.writeText(command);
      setCopyStatus("copied");
    } catch {
      setCopyStatus("failed");
    }
    window.setTimeout(() => setCopyStatus("idle"), 2200);
  }

  return (
    <button type="button" onClick={copyCommand} aria-live="polite">
      {copyStatus === "copied" ? "Copied" : copyStatus === "failed" ? "Select manually" : label}
    </button>
  );
}

function QuickstartStep({ number, title, description, command }: {
  number: string;
  title: string;
  description: string;
  command: string;
}) {
  return (
    <div className="quickstartStep">
      <div className="quickstartStepIntro">
        <span>{number}</span>
        <div><strong>{title}</strong><p>{description}</p></div>
        <CopyButton command={command} label="Copy" />
      </div>
      <pre><code>{command}</code></pre>
    </div>
  );
}

export function Quickstart() {
  return (
    <>
      <div className="quickstartPanel">
        <QuickstartStep number="01" title="Give your agent the governance workflow" description="Install the project-level skill so the agent knows when to retrieve, propose, and stop for Human Approval." command={skillCommand} />
        <QuickstartStep number="02" title="Install the local MCP and CLI" description="One install provides the safe agent tools and the local Proofpress commands." command={installCommand} />
        <QuickstartStep number="03" title="Create a governed workspace" description="Seeds synthetic evidence and prints a ready-to-copy local MCP configuration. No account or model call required." command={quickstartCommand} />
      </div>
      <div className="contributionCallout">
        <div><span>CONTRIBUTE</span><p>Developing Proofpress itself is a separate setup.</p></div>
        <a href="https://github.com/chenmingtang830/proofpress/blob/main/CONTRIBUTING.md">Read the contribution guide →</a>
      </div>
    </>
  );
}
