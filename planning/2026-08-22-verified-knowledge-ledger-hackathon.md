[//]: # (ob:7a3f0e21)
# Hackathon plan: verified knowledge ledger for autonomous AI agents

[//]: # (ob:5e9d1c42)
**Status:** proposed build plan for the Coframe / AGI House Long Horizon Agents event

[//]: # (ob:93a8b4f7)
**Product position:** Proofpress is the verified knowledge ledger for autonomous AI agents.

[//]: # (ob:2d47c8a1)
> Telemetry is the source. Claims are the unit. Admission is the product. Artifacts are portable views of the ledger.

[//]: # (ob:6fb1a924)
## Executive decision

[//]: # (ob:c43d8f15)
Build a narrow end-to-end vertical slice that turns existing agent and experiment telemetry into candidate claims, sends those claims through deterministic and review gates, and gives a fresh agent only the currently admitted organizational knowledge. The demo should show that a new session can continue from a compact, governed state without rereading a full trace or blindly trusting a generated summary.

[//]: # (ob:e7a3056b)
The product is not a generic knowledge base, an observability backend, or a truth oracle. It is the semantic and admission layer above execution systems. OpenTelemetry is an input adapter; a CLI drives the workflow; a graph UI makes the trust chain inspectable; portable Markdown or static HTML artifacts remain an output and exchange format.

[//]: # (ob:81b96d30)
## Why this is the right wedge

[//]: # (ob:a1c943e8)
Long-horizon agents already produce logs, commits, runs, traces, evaluations, and experiment metrics. Systems such as Coframe also maintain experiment state and learn from performance. The missing layer is not “memory” in the broad sense. It is a defensible answer to: **Which conclusions may a future agent rely on, within what scope, based on which evidence, approved by whom or what policy, and until when?**

[//]: # (ob:cb4ae812)
The attached ARA product exploration describes a ladder in which each lower unit becomes evidence for the unit above it:

[//]: # (ob:fd2c51a9)
1. **Commit / run / trace:** what happened.
2. **Claim:** what the result is asserted to mean.
3. **Verified finding:** what the organization has admitted and may build on.

[//]: # (ob:b936de40)
This build operationalizes that ladder for autonomous agents. It extends Proofpress beyond an artifact-bound interaction model without discarding the existing artifact provenance implementation.

[//]: # (ob:33b83ec5)
## Relationship to the production ARA lifecycle

[//]: # (ob:bf0ff8c5)
The production repository already defines a five-stage research lifecycle: **Design → Freeze → Execute → Admit → Synthesize**. The hackathon product should consume and expose that lifecycle rather than invent a parallel research system:

[//]: # (ob:d73561a8)
- `SourceEvent` and `Evidence` are produced during Execute and checked against the frozen protocol.
- `Claim` is the explicit semantic unit entering Admit and Synthesize.
- `Admission` records whether a result or claim may contribute to governed knowledge.
- `context` projects the latest admitted synthesis for downstream agents.

[//]: # (ob:eb6216c1)
The existing Long Horizon Eval ARA remains a research lifecycle record and is currently Phase Zero, with no real-model efficacy result. The hackathon work is a product demonstration built on those semantics—not a new benchmark result, Harvey LAB evaluation, or validation of long-horizon effectiveness.

[//]: # (ob:1c7a84df)
## What “verified” means

[//]: # (ob:3ef62190)
For the MVP, a verified claim is not guaranteed to be universally true. It is a claim that:

[//]: # (ob:6b82e14c)
- is bound to inspectable evidence and its provenance;
- satisfies declared deterministic checks;
- has a recorded review decision from an authorized human or policy agent;
- carries explicit scope, status, and expiry or supersession semantics; and
- can be traced backward and revised without erasing prior decisions.

[//]: # (ob:40d56bc7)
The interface must keep three questions separate: **Is the record intact? Does the evidence support the claim under the declared method? Has the organization admitted the claim for reuse?** Proofpress can prove the first, encode evidence for the second, and govern the third. It must not collapse them into “the claim is objectively true.”

[//]: # (ob:d0e3b879)
## Product hierarchy

[//]: # (ob:49a21c6e)
| Level | Unit | Core question | MVP treatment |
|---|---|---|---|
| L0 Telemetry | logs, commits, tool calls, traces, spans | What happened? | Import a bounded OTLP JSON fixture and existing file/Git evidence. |
| L1 Evidence | experiment result, test output, metric window, document block | What observation can be inspected? | Normalize selected source events into addressable evidence records. |
| L2 Claims | scoped semantic assertions | What do we think the evidence means? | CLI creates candidate claims with evidence references and qualifiers. |
| L3 Admission | accepted, rejected, unresolved, superseded, expired | May an agent rely on this claim? | Deterministic gate, policy-agent recommendation, and human decision. |
| L4 Governed knowledge | current reusable organizational state | What should the next agent inherit? | Query and materialize only admitted, non-expired claims. |

[//]: # (ob:715ee263)
The implementation should be graph-native internally and artifact-friendly externally. The graph represents relationships across runs, claims, decisions, and outputs. Artifacts remain portable projections that can travel outside the service and retain a checkable accepted history.

[//]: # (ob:97c5d041)
## Minimal ledger model

[//]: # (ob:dfa73c68)
### Nodes

[//]: # (ob:f91bc7e2)
- `SourceEvent`: an imported trace span, commit, tool event, or evaluation record.
- `Evidence`: a selected, immutable observation with a digest and source pointer.
- `Claim`: a scoped assertion proposed from one or more evidence records.
- `Admission`: an append-only decision about a claim under a named policy version.
- `Artifact`: a materialized or imported carrier such as Markdown, static HTML, or a report.

[//]: # (ob:6304a5ed)
### Edges

[//]: # (ob:214ff9c7)
- `derived_from`: evidence or claim was derived from an upstream record.
- `supports` / `refutes`: evidence bears on a claim without implying final truth.
- `admitted_by`: a claim is governed by an admission event.
- `supersedes`: a newer claim or decision replaces an older one without deleting it.
- `materialized_in`: governed knowledge appears in a portable artifact.

[//]: # (ob:8db51a36)
### Required claim fields

[//]: # (ob:9b6312a4)
`claim_id`, statement, scope, evidence references, proposer, creation time, confidence or uncertainty, policy version, current admission state, reviewer identity, rationale, expiry, and superseded-by reference. IDs and digests must be stable; absent evidence and inconclusive results remain visible rather than being coerced into success.

[//]: # (ob:ea6420fd)
## MVP components

[//]: # (ob:0d86fb7a)
### 1. OpenTelemetry ingest adapter

[//]: # (ob:c85214e3)
Accept a prebuilt OTLP JSON export containing three website experiments. Preserve trace and span IDs, timestamps, selected attributes, source identity, and a canonical digest. Map only allow-listed fields and keep raw prompt bodies, secrets, user payloads, and high-cardinality noise out of the ledger by default.

[//]: # (ob:507b918f)
The hackathon build does not run an OpenTelemetry Collector or compete with a trace store. It demonstrates that existing telemetry can become provenance for higher-level claims.

[//]: # (ob:4bf15ca0)
### 2. CLI workflow

[//]: # (ob:98d06f37)
Expose one coherent happy path:

[//]: # (ob:e15fa48c)
```text
proofpress ingest demo/experiments.otlp.json
proofpress propose --from-trace TRACE_ID --claims demo/claims.json
proofpress review CLAIM_ID --policy demo/policy.yaml
proofpress admit CLAIM_ID --reviewer human:richard --why "..."
proofpress reject CLAIM_ID --reviewer agent:policy-reviewer --why "..."
proofpress context --scope coframe-demo --format json
proofpress materialize --scope coframe-demo --output current-knowledge.md
```

[//]: # (ob:f81099a6)
The exact production command surface may evolve. For the demo, commands may be thin wrappers around one local ledger, but their output must use stable IDs and machine-readable JSON so another agent can consume it.

[//]: # (ob:e3d0b749)
### 3. Review gates

[//]: # (ob:b316f5e8)
Run gates in order:

[//]: # (ob:04e93bc6)
1. **Deterministic verification:** schema validity, digest integrity, required evidence, sample-size floor, metric and guardrail checks.
2. **Agent policy review:** a separate policy agent recommends accept, reject, or unresolved and cites the evidence and rule it used.
3. **Human review:** a reviewer sees the claim, evidence, automated checks, and recommendation, then makes the final admission decision for high-impact knowledge.

[//]: # (ob:ee532af0)
The proposer must not self-approve by default. Agent review is a policy decision, not proof of semantic truth. Every gate records its identity, version, inputs, outcome, and rationale.

[//]: # (ob:5a97c213)
### 4. Frontend graph

[//]: # (ob:81743ed6)
Provide three zoom levels:

[//]: # (ob:1653cf2a)
- **Runs / traces:** source events and experiment measurements.
- **Claims / experiments:** candidate interpretations and their support or refutation links.
- **Governed knowledge:** accepted, current claims available to agents.

[//]: # (ob:3472dc81)
Default to the governed-knowledge view. A user can click a claim to traverse its admission and evidence back to a source span. Color communicates state, not truth: candidate, accepted, rejected, unresolved, superseded, or expired.

[//]: # (ob:6973d48c)
### 5. Agent context endpoint

[//]: # (ob:c6ba2715)
Return only current, in-scope knowledge by default, along with compact provenance handles and policy metadata. A fresh agent should receive the minimum sufficient state, not the entire event history. It can request deeper evidence when uncertainty or policy requires it.

[//]: # (ob:b9a76204)
## End-to-end demo script

[//]: # (ob:99d357ae)
1. Import one OTLP JSON fixture containing three prior website experiments.
2. Generate three candidate claims from those experiments.
3. Apply deterministic policy: one claim passes; one remains unresolved because the sample is insufficient; one is rejected because a guardrail metric regressed.
4. Display all three candidates and their evidence edges in the graph.
5. Let a human accept or reject the reviewable claim.
6. Append the admission events to the ledger.
7. Materialize `current-knowledge.md` from accepted, non-expired knowledge.
8. Start a fresh agent session with only `proofpress context` or the materialized artifact.
9. Ask the fresh agent to choose the next experiment and explain which admitted knowledge it used.
10. Traverse the chosen claim back to the original experiment span.

[//]: # (ob:4b6110c2)
**Hero moment:** “Thousands of agent events became three candidate claims. Only one became organizational knowledge. A fresh agent continued from that governed knowledge—not from the raw trace.”

[//]: # (ob:36a8c209)
## Build plan

[//]: # (ob:8d9e3f40)
### Phase 0 — freeze the contract

[//]: # (ob:302741ba)
- Define the five node types, six edge types, admission states, and minimal JSON schema.
- Write the policy semantics and the precise meaning of “verified.”
- Freeze the three-experiment fixture and expected outcomes.

[//]: # (ob:e36da479)
### Phase 1 — vertical slice

[//]: # (ob:3f6c980e)
- Implement OTLP JSON import and deterministic canonical IDs.
- Implement claim proposal, policy review, admission events, and current-context query.
- Reuse existing Proofpress artifact digests, actor fields, reasons, claims, and append-only event concepts where compatible.
- Materialize a portable Markdown view without making the artifact the database.

[//]: # (ob:a63295c7)
### Phase 2 — demo UI

[//]: # (ob:7ce0a431)
- Build the three-level graph and claim detail drawer.
- Add a human Accept / Reject / Mark unresolved action.
- Show policy version, reviewer, evidence coverage, expiry, and supersession.

[//]: # (ob:15bf08cf)
### Phase 3 — continuity proof

[//]: # (ob:268f7a35)
- Launch a fresh agent with no prior session transcript.
- Give it only governed context and provenance handles.
- Capture whether it selects the intended next experiment and refuses to rely on rejected or unresolved claims.
- Present this as a demo acceptance check, not as a scientific study or broad efficacy result.

[//]: # (ob:73ce08a1)
## Acceptance criteria

[//]: # (ob:9ea724d0)
- The same fixture produces deterministic evidence and claim identifiers on repeated import.
- Every claim can be traced to one or more immutable evidence records and source-event pointers.
- A claim cannot enter current context without a valid admission event.
- Rejected, unresolved, expired, and superseded claims never appear as current knowledge by default.
- The proposer cannot approve its own claim under the default policy.
- Changing evidence, claim text, or policy inputs invalidates or creates a new review decision rather than silently mutating history.
- A fresh agent receives only current governed knowledge and can request the supporting chain.
- The UI never labels integrity, evidence support, or admission as universal truth.
- Raw prompts, secrets, and full trace payloads are excluded from portable materialization.

[//]: # (ob:0317bd62)
## Non-goals for the hackathon

[//]: # (ob:4ce19b83)
- No full OpenTelemetry Collector, storage backend, or real-time trace viewer.
- No generic RAG or “company brain.”
- No ingestion of every prompt, transcript, or tool payload.
- No semantic truth oracle or automatic natural-language-to-formal equivalence claim.
- No complex RBAC, enterprise tenancy, or multi-user real-time collaboration.
- No arbitrary policy language or broad connector marketplace.
- No full migration away from existing artifact-centric Proofpress behavior.
- No Harvey or Cold Handoff study rerun; collaborator research remains a separate evidence track.

[//]: # (ob:072b3e94)
## Backward-compatible product evolution

[//]: # (ob:f1c48520)
Current Proofpress records accepted artifact versions, computed block changes, actor roles, reasons, consequential rejections, and portable history. Those primitives become one projection of the broader ledger:

[//]: # (ob:d81e4fc3)
- existing artifact events remain valid `Artifact` and `Admission` records;
- artifact claims can reference new ledger `Claim` IDs;
- existing digests and actor roles are reused rather than replaced;
- portable capsules carry a bounded view or references, not the entire telemetry graph;
- existing `verify` continues to report integrity and claim-to-diff consistency, while a new admission view reports governance state.

[//]: # (ob:b33f1860)
This is an upgrade in product center of gravity: from “the ledger travels with each artifact” to “the ledger governs claims across sources, and artifacts are portable views.” It should be implemented as additive schema and commands so the existing release remains usable.

[//]: # (ob:4528f6a9)
## Design-partner motion at the event

[//]: # (ob:693a41c2)
Offer hosts and participating teams a **Trusted Continuation Track**:

[//]: # (ob:05d6b48f)
1. Bring one completed or paused long-horizon run with existing telemetry.
2. Select two to five claims that a future agent would need.
3. Bind them to evidence and run the review gate.
4. Start a fresh session or model from the governed context.
5. Compare the continuation decision with the team's intended next step.

[//]: # (ob:17dd4ec7)
The design-partner question is not “Do you need memory?” Ask instead: **Which conclusion from a prior run would be costly or dangerous for a new agent to trust incorrectly, and who is allowed to approve it?** A promising partner has multi-session work, meaningful claims, real handoffs, and consequences for reusing an invalid conclusion.

[//]: # (ob:66f904d8)
For Coframe specifically, position Proofpress as complementary to its experimentation loop: Coframe generates and evaluates variants; Proofpress makes selected conclusions portable, scoped, evidence-backed, revisable, and safe for a fresh session or model to inherit. Do not claim Coframe lacks experiment memory or telemetry.

[//]: # (ob:5bfe8a93)
## Risks and open questions

[//]: # (ob:c2d173a0)
- **Unit boundary:** when should multiple metric observations become one claim rather than several claims?
- **Policy ownership:** which decisions may be agent-reviewed, and which require a human?
- **Revocation:** should expiry be time-based, evidence-based, or both?
- **Privacy:** which source fields may be stored locally, shared with reviewers, or materialized into portable artifacts?
- **Identity:** what attests that a named agent or human actually made a decision?
- **External trust:** when is an external witness or signature required beyond the current tamper-evident local chain?
- **Value proof:** does governed context materially improve safe continuation for a real partner workflow? The hackathon demo can expose this question but cannot answer it broadly.

[//]: # (ob:4be65d1f)
## Immediate owner split

[//]: # (ob:ad27f5c8)
- **Proofpress core:** ledger schema, admission state machine, provenance, CLI, context projection, and portable materialization.
- **Demo frontend:** graph navigation, evidence drawer, review action, and fresh-session launch.
- **Coframe / partner adapter:** bounded OTLP fixture and mapping from experiment spans to evidence.
- **Harvey collaborator:** continue the separate research and handoff work; provide lessons or reusable fixtures only where their evidence scope is explicit.

[//]: # (ob:f7c1246a)
## Sources

[//]: # (ob:b17e9034)
- `ara-product-exploration.html` (local attachment supplied for this planning request), especially “the structure layer” and the distinction between traces, claims, and verified findings.
- `README.md` and `docs/PORTABLE_ARTIFACT_SPEC.md` for current Proofpress behavior and trust boundaries.
- `studies/long-horizon-eval/ara/` for the production Design / Freeze / Execute / Admit / Synthesize lifecycle, Phase Zero boundary, claim register, and evidence policy.
- `studies/LONG_HORIZON_EVAL_FLOW.md` for the cold-boundary intervention and the separation of safe continuation from general agent capability.
- `rit-hub-demo/DECISIONS.md` and `experiments/provenance_handoff/README.md` in the development checkout for the verification / process / admission separation and the Harvey research boundary; these files are supporting context, not part of this PR base.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzg2MmUyNmNjYmQ1ZDUzY2Y5ZjJjYzY5ZCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
