OpenWiki current-evidence conflict gate
=======================================

Run from the Proofpress repository root:

  python3 examples/openwiki-conflict-gate/run_demo.py

For a machine-readable receipt:

  python3 examples/openwiki-conflict-gate/run_demo.py --json

The command materializes a frozen bundle produced through OpenWiki 0.4.2's
real HostSessionManager lifecycle, confirms that its recorded preflight had
zero issues, independently recomputes every persisted evidence-range version,
imports the OKF page and claim sidecar into Proofpress, and launches each
Proofpress step as a separate process. The final process reads the frozen
worktree policy plus the append-only knowledge ref.

The adversarial handoff deliberately promotes a preserved historical quotation
as an unqualified candidate. OpenWiki's current bundle also contains the
structured replacement claim. A human admits that these candidates contradict.
Proofpress then proves that:

  1. both candidates are admitted before the relation is admitted;
  2. neither appears in governed context while the conflict is unresolved;
  3. explicit supersession releases only the current structured claim; and
  4. a fresh successor receives the winner plus evidence, policy, relation,
     resolution, supersession, and Git-ledger receipts.

Truth boundary
--------------

OpenWiki proves claim-to-file freshness in the frozen bundle. It does not prove
the aggregate gravitational record is physically correct. Proofpress does not
infer the semantic contradiction or winner. Humans admit both decisions.
Resolver identity is recorded as self_asserted; the allowlist is not
authentication. The fixture contains one initial condition and supports only
the stated energy-invariant scope. CLE is not evaluated here.
