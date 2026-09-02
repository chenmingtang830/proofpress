[//]: # (ob:3eba833f)
# Proofpress Product

[//]: # (ob:f598c9f1)
<!-- impeccable:product-schema 1 -->

[//]: # (ob:599097ed)
## Platform

[//]: # (ob:90cca906)
web

[//]: # (ob:cb0968a8)
## Users

[//]: # (ob:54dc4824)
The primary user is the owner of a knowledge workspace who works through multiple coding agents and devices. Agents submit bounded evidence and candidate conclusions; the owner reviews what may become reusable knowledge; successor agents read only governed context.

[//]: # (ob:f1f48c9c)
## Product Purpose

[//]: # (ob:40636aeb)
Proofpress is the governance layer for agent-produced knowledge. It records evidence, proposals, checks, human decisions, receipts, and the current context that downstream agents are allowed to rely on.

[//]: # (ob:feb10e3b)
## Positioning

[//]: # (ob:3bc86ca8)
Proofpress is not a generic knowledge graph, RAG system, or chat memory. Its distinct mechanism is an explicit admission boundary: agents may propose and automated systems may verify or recommend, but only configured human authority admits knowledge for reuse.

[//]: # (ob:c7b3273d)
## Operating Context

[//]: # (ob:5784f531)
The current product is a Python-first local and single-owner hosted control plane. Agents connect through the Python SDK, HTTP, or MCP. The owner uses a web workspace to review candidates, inspect evidence and lineage, administer credentials, and ask bounded questions about the governed state.

[//]: # (ob:47fc435f)
## Capabilities and Constraints

[//]: # (ob:966cc484)
- One owner authorizes admission in the current hosted workspace.
- Agent credentials can submit evidence, propose conclusions, and read governed context but cannot approve, reject, supersede, or change policy.
- The hosted assistant is advisory and may not perform admission decisions.
- Verification and model recommendations are inputs to review, never authority.
- Current scope excludes multi-owner governance, general OCR/RAG, Notion ingestion, multi-repository ingestion, and customer VPC deployment.

[//]: # (ob:ee682932)
## Brand Commitments

[//]: # (ob:6006a6d0)
The product name is always one word: **Proofpress**. The operating experience is precise, calm, evidence-forward, and deliberately free of generic AI-product decoration. Product vocabulary includes Evidence, Candidate Conclusion, Review, Approve/Admit, Receipt, Ledger, Lineage, and Governed Context.

[//]: # (ob:3aad66a1)
## Evidence on Hand

[//]: # (ob:d5d61527)
The repository contains the canonical governance kernel, Python SDK, HTTP and MCP transports, single-owner hosted service, owner review workflow, persisted audit data, experiment evidence profile, credential lifecycle, and integration tests. The internal Render deployment is the dogfood environment; design-partner outcomes remain separate evidence.

[//]: # (ob:ee31884d)
## Product Principles

[//]: # (ob:7fdb0a67)
1. Make authority visible: a user can always distinguish evidence, checks, recommendations, and human decisions.
2. Preserve bounded provenance: every reusable conclusion remains connected to evidence and receipts.
3. Project only admitted, current, in-scope knowledge to successor agents.
4. Integrate with customer-owned agents rather than replacing their runtime.
5. Prefer one coherent product surface and contract over parallel interfaces with different semantics.

[//]: # (ob:184e98cb)
## Accessibility & Inclusion

[//]: # (ob:88f6f2cd)
The web workspace must support keyboard operation, visible focus, reduced motion, semantic status text independent of color, responsive layouts, and WCAG AA contrast.
