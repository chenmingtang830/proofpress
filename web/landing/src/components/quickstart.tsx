import { useState } from "react";

const installCommand = `uv tool install "git+https://github.com/chenmingtang830/proofpress.git"`;

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
      <div className="nextCommand"><span>Then run</span><code>proofpress demo</code></div>
      <p>The terminal demo shows what is admitted, what is blocked, and what still needs human review.</p>
    </div>
  );
}
