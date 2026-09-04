import { useState } from "react";

const quickstart = `git clone https://github.com/chenmingtang830/proofpress.git
cd proofpress
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

DEMO_DIR="$(mktemp -d)"
git -C "$DEMO_DIR" init -q
git -C "$DEMO_DIR" config user.name "Proofpress Demo"
git -C "$DEMO_DIR" config user.email "demo@example.invalid"
cd "$DEMO_DIR"
proofpress demo
proofpress context --scope demo --actor agent:successor`;

export function Quickstart() {
  const [copyStatus, setCopyStatus] = useState<"idle" | "copied" | "failed">("idle");

  async function copyCommand() {
    try {
      await navigator.clipboard.writeText(quickstart);
      setCopyStatus("copied");
    } catch {
      setCopyStatus("failed");
    }
    window.setTimeout(() => setCopyStatus("idle"), 2200);
  }

  return (
    <div className="quickstartPanel">
      <div className="codeHeader">
        <span>Python 3.11+ · synthetic local demo</span>
        <button type="button" onClick={copyCommand} aria-live="polite">
          {copyStatus === "copied" ? "Copied" : copyStatus === "failed" ? "Select manually" : "Copy commands"}
        </button>
      </div>
      <pre><code>{quickstart}</code></pre>
      <p className="quickstartResult">
        The demo creates admitted, needs-review, and rejected synthetic conclusions. The final
        context read returns only the admitted, current, in-scope conclusion.
      </p>
    </div>
  );
}
