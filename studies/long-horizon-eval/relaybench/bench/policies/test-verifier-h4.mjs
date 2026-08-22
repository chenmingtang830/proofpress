import { performance } from "node:perf_hooks";
import { auditInformationParity } from "../parity/information-parity.mjs";

export async function runTestOnlyH4Verifier({ c1Files, c2Files }) {
  const started = performance.now();
  const audit = auditInformationParity(c1Files, c2Files);
  return {
    required: true,
    test_only: true,
    pin_verified: true,
    status: audit.passed ? "ok" : "malformed_evidence",
    malformed: !audit.passed,
    duration_ms: performance.now() - started,
    commands: [{
      argv: ["TEST-ONLY", "proofpress", "inspect", "proofpress/portable-carrier.test-only.json"],
      exit_code: audit.passed ? 0 : 1,
      stdout: `${JSON.stringify({ status: audit.passed ? "ok" : "invalid", projection_sha256: audit.substantive_projection_sha256 })}\n`,
      stderr: "",
    }],
    claim_scope: "TEST-ONLY binding mechanics; no truth, legal quality, authorship, identity, or external authorization determination.",
  };
}
