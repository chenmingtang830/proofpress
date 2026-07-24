/**
 * Proofpress deterministic layer for Pi — UNTESTED SKELETON.
 *
 * Pi extensions are in-process TypeScript subscribing to AgentSession
 * lifecycle events (25+ hooks; see pi's extension docs — the API surface
 * moves fast, verify event names against your installed version).
 *
 * Intent: on session end, run best-effort capture across Git candidates and
 * current paths already admitted to the ledger. The hook records only
 * recorded_by, never an inferred author or reason. Content-addressed duplicate
 * runs are no-ops.
 */
import { execFileSync } from "node:child_process";

export default function proofpress(session: any) {
  session.on("session_end", () => {
    try {
      execFileSync("test", ["-f", "proofpress.py"]);
      execFileSync("python3", [
        "proofpress.py", "capture", "--recorder", "pi-hook",
      ], { stdio: "inherit" });
    } catch { /* no proofpress.py here, or nothing changed — fine */ }
  });
}
