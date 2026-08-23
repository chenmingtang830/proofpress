[//]: # (ob:87dd93fc)
# Verified Knowledge Ledger

[//]: # (ob:b71e5de6)
> Status: implemented developer wedge in `proofpress@0.4.0`. This overview
> describes the current CLI and fixture. It is not yet a frozen interchange
> specification or a claim of general long-horizon agent efficacy.

[//]: # (ob:24505103)
## What it is

[//]: # (ob:1e12da99)
The verified knowledge ledger turns **bounded** agent telemetry or artifacts
into candidate knowledge that a later human or agent can inspect before relying
on it. It is the trust layer above observability and memory:

[//]: # (ob:e2507278)
| Layer | Primary question |
|---|---|
| Logs, traces, commits, artifacts | What happened? |
| Memory and ontology | What does the system remember and how is it structured? |
| Proofpress | What may be relied on, why, by whom, and within what scope? |

[//]: # (ob:a0ce3955)
**Memory is retrieval. Ontology is structure. Proofpress is trust.**

[//]: # (ob:5e5ed818)
The ledger does not make a claim universally true. It records the source,
selected evidence, declared policy, review receipt, lifecycle state, scope, and
expiry or supersession semantics that determine whether an organization may
reuse it.

[//]: # (ob:7a1cac9c)
## Current workflow

[//]: # (ob:c3d2a28d)
```text
bounded OTLP-style telemetry or artifact
  → immutable source events and selected evidence
  → candidate claims
  → deterministic checks + policy recommendation + human review
  → governed current context for a fresh human or agent
```

[//]: # (ob:2ef561dc)
The reference fixture is
[`examples/verified-knowledge-ledger/demo.otlp.json`](../examples/verified-knowledge-ledger/demo.otlp.json).

[//]: # (ob:5c8c136b)
```sh
proofpress knowledge ingest demo.otlp.json -o ledger.json \
  --scope demo --proposer agent:experiment-runner
proofpress knowledge policy-review ledger.json --claim CLAIM_ID
proofpress knowledge review ledger.json --claim CLAIM_ID \
  --decision accept --reviewer human:reviewer
proofpress knowledge context ledger.json --scope demo
proofpress knowledge verify ledger.json
```

[//]: # (ob:58bffc74)
`context` returns only admitted, current, in-scope knowledge. Rejected,
unresolved, expired, and superseded candidates remain in the audit history but
are excluded by default. `view` emits a stable graph read model; `materialize`
writes a Markdown projection.

[//]: # (ob:5d269544)
## Relationship to artifact provenance

[//]: # (ob:1acc88ee)
Artifact provenance remains the portable trust primitive: it binds a durable
artifact to revision history, evidence, actors, and decisions. The knowledge
ledger generalizes the same trust semantics across bounded workflow activity so
that a fresh agent can start from governed conclusions rather than raw context.

[//]: # (ob:067a97a0)
The two surfaces are compatible. A portable artifact can be a materialized view
of governed knowledge; it does not need to carry the full telemetry graph.

[//]: # (ob:d228259c)
## Non-goals

[//]: # (ob:9a909f30)
- Not a full OpenTelemetry collector or real-time trace backend.
- Not a generic RAG, company brain, or replacement for memory.
- Not a semantic truth oracle or a guarantee that every relevant event was
  captured.
- Not a complete RBAC, connector marketplace, or hosted governance service.
- Not evidence of general agent capability improvement.

[//]: # (ob:b47338ab)
## Evidence boundary and current focus

[//]: # (ob:b324002e)
In the published controlled agent-handoff study, ordinary handoff reused stale
work in 12/12 trials and Proofpress-assisted handoff did so in 0/12; both
conditions continued unchanged work correctly in 12/12 trials. This supports a
version-checking mechanism on that task, not a general product-efficacy claim.
See the [open study package](../studies/agent-handoff-artifact-provenance/README.md).

[//]: # (ob:c8235573)
The next public proof point is a design-partner workflow: select two to five
conclusions from a real long-horizon or multi-agent run, bind them to evidence,
apply the review path, and measure whether governed context changes the next
decision. Until then, finance and agentic-commerce interfaces are illustrative
product fixtures, not customer validation.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzQ0NTQ2YTFiZjE4NzUyZGIzNGJjMWViNyIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
