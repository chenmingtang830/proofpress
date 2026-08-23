Verified Knowledge Ledger

Presentation
------------

Run from the repository root:

  python3 -m http.server 8766

Open:

  http://127.0.0.1:8766/examples/verified-knowledge-ledger/demo.partner-style.html

The light, eight-beat presentation is the primary product story. It includes
the interactive governed-knowledge graph, the existing Proofpress handoff
study, the finance workflow, and the agentic-commerce extension. The earlier
dark workbench is retained only as a historical reference in archive/.

Backend fixture
---------------

Run from the repository root:

  python3 proofpress.py knowledge ingest examples/verified-knowledge-ledger/demo.otlp.json -o /tmp/coframe-ledger.json --scope coframe-demo --proposer agent:experiment-runner
  python3 proofpress.py knowledge policy-review /tmp/coframe-ledger.json --claim <claim-id>
  python3 proofpress.py knowledge review /tmp/coframe-ledger.json --claim <claim-id> --decision accept --reviewer human:demo
  python3 proofpress.py knowledge context /tmp/coframe-ledger.json --scope coframe-demo
  python3 proofpress.py knowledge view /tmp/coframe-ledger.json --scope coframe-demo
  python3 proofpress.py knowledge materialize /tmp/coframe-ledger.json -o /tmp/current-knowledge.md --scope coframe-demo
  python3 proofpress.py knowledge verify /tmp/coframe-ledger.json

The fixture contains two complete experiments and one failed experiment. The
ledger separately records immutable source events, selected evidence, claims,
policy recommendations, and append-only admission decisions. The failed
candidate cannot pass the deterministic gate; a proposer cannot self-approve.

Fresh-agent context contains only admitted claims in the requested scope. It
excludes rejected, unresolved, expired, and superseded claims. `view` emits the
stable graph read model for a frontend; the frontend must not invent graph
relationships or review state locally.
