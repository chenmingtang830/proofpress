import { useState } from "react";

const skillCommand = `SKILL_DIR=.agents/skills/proofpress-governed-context
mkdir -p "$SKILL_DIR"
curl -fsSL \\
  https://raw.githubusercontent.com/chenmingtang830/proofpress/main/.agents/skills/proofpress-governed-context/SKILL.md \\
  -o "$SKILL_DIR/SKILL.md"`;
const installCommand = `uv tool install --with "mcp>=2,<3" \\
  "git+https://github.com/chenmingtang830/proofpress.git"`;
const quickstartCommand = `proofpress quickstart`;

function CopyButton({ command, title }: { command: string; title: string }) {
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
    <div className="copyControl">
      <span role="status">{copyStatus === "copied" ? "Copied" : copyStatus === "failed" ? "Copy failed. Select the command below." : ""}</span>
      <button type="button" onClick={copyCommand} aria-label={`Copy command: ${title}`}>Copy</button>
    </div>
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
      </div>
      <div className="quickstartCode">
        <div className="quickstartCodeBar">
          <span>Terminal</span>
          <CopyButton command={command} title={title} />
        </div>
        <pre tabIndex={0} aria-label={`${title} command`}><code>{command}</code></pre>
      </div>
    </div>
  );
}

export function Quickstart() {
  return (
    <>
      <p className="evaluationPrereqs">Before you begin: use a macOS or Linux shell with Git, curl, and <a href="https://docs.astral.sh/uv/getting-started/installation/">uv installed</a>. Run these commands from your project directory.</p>
      <div className="quickstartPanel">
        <QuickstartStep number="01" title="Add the governance workflow" description="Install the project-level skill agents use to retrieve, propose, and stop for human admission." command={skillCommand} />
        <QuickstartStep number="02" title="Install the local MCP and CLI" description="One install provides the safe agent tools and the local Proofpress commands." command={installCommand} />
        <QuickstartStep number="03" title="Create a governed workspace" description="Seeds synthetic evidence and prints a ready-to-copy local MCP configuration. No account or model call required." command={quickstartCommand} />
      </div>
      <div className="evaluationOutcome"><strong>What you’ll get</strong><p>A workspace with synthetic evidence and a local MCP configuration to connect your agent. This is a local demonstration, not a production deployment.</p></div>
      <div className="contributionCallout">
        <div><span>CONTRIBUTE</span><p>Developing Proofpress itself is a separate setup.</p></div>
        <a href="https://github.com/chenmingtang830/proofpress/blob/main/CONTRIBUTING.md">Read the contribution guide →</a>
      </div>
    </>
  );
}
