import { useState } from "react";

const demoCommand = `DEMO_DIR="$(mktemp -d)" && git -C "$DEMO_DIR" init -q
(cd "$DEMO_DIR" && proofpress demo)`;

const setup = `git clone https://github.com/chenmingtang830/proofpress.git
cd proofpress
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .`;

export function Quickstart() {
  const [copyStatus, setCopyStatus] = useState<"idle" | "copied" | "failed">("idle");

  async function copyCommand() {
    try {
      await navigator.clipboard.writeText(demoCommand);
      setCopyStatus("copied");
    } catch {
      setCopyStatus("failed");
    }
    window.setTimeout(() => setCopyStatus("idle"), 2200);
  }

  return (
    <div className="quickstartPanel">
      <div className="commandBar">
        <span>Already installed</span>
        <button type="button" onClick={copyCommand} aria-live="polite">
          {copyStatus === "copied" ? "Copied" : copyStatus === "failed" ? "Select manually" : "Copy command"}
        </button>
      </div>
      <pre><code>{demoCommand}</code></pre>
      <details>
        <summary>First time? Show setup</summary>
        <pre><code>{setup}</code></pre>
      </details>
      <p>Creates a synthetic admitted result and blocks the conclusions that still need review.</p>
    </div>
  );
}
