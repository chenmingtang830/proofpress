import { useState } from "react";

const installCommand = `uv tool install --with "mcp>=2,<3" "git+https://github.com/chenmingtang830/proofpress.git"`;

export function Quickstart() {
  const [copyStatus, setCopyStatus] = useState<"idle" | "copied" | "failed">("idle");

  async function copyCommand() {
    try {
      await navigator.clipboard.writeText(installCommand);
      setCopyStatus("copied");
    } catch {
      setCopyStatus("failed");
    }
    window.setTimeout(() => setCopyStatus("idle"), 2200);
  }

  return (
    <div className="quickstartPanel">
      <div className="commandBar">
        <span>From GitHub · Python 3.11+ · requires uv</span>
        <button type="button" onClick={copyCommand} aria-live="polite">
          {copyStatus === "copied" ? "Copied" : copyStatus === "failed" ? "Select manually" : "Copy install command"}
        </button>
      </div>
      <pre><code>{installCommand}</code></pre>
      <div className="nextCommand"><span>Then run</span><code>proofpress quickstart</code></div>
      <p>Creates a fresh synthetic Git workspace and prints a ready-to-copy local MCP config. Add <code>--ui</code> to open local review.</p>
    </div>
  );
}
