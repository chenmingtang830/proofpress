---
name: proofpress-governed-context
description: Use Proofpress governed context when a task must rely on or hand off durable agent-produced knowledge, including evidence-backed decisions, experiment results, integration contracts, or incident learnings. Retrieve eligible context before relying on it; submit bounded proposals and receipts when a durable outcome is produced. Do not use for routine code edits, transient debugging, or unvalidated hypotheses.
---

# Proofpress governed context

Use this skill to make downstream reliance explicit: what is eligible to reuse,
what evidence supports a new candidate, and which authorized human must approve
it. Proofpress is not a replacement for the agent runtime, its memory, or raw
private traces.

## Preconditions

Require a configured Proofpress MCP server or a supported Python, CLI, or HTTP
client with an agent-scoped token. Use the configured review base URL when one
is available. Do not request, copy, print, or store owner or recovery
credentials.

If the client cannot reach Proofpress or cannot authenticate, continue the
primary task without claiming governed reuse or proposal submission. Report the
missing integration as a blocker; do not silently substitute local memory as
approved context.

## Decide the action

Choose exactly one mode for each knowledge-bearing outcome:

- **Reference only** — retrieve eligible, in-scope governed context before
  relying on it; state its scope and any limits in the task result.
- **Draft only** — keep a working hypothesis or incomplete finding in the task
  output; do not submit it as a reusable candidate.
- **Propose** — submit a bounded candidate when the task produces a durable
  decision, evidence-backed conclusion, reproducible experiment result,
  integration contract, or incident learning that a later agent or person could
  rely on.

Do not propose routine code edits, an unverified debugging theory, duplicated
context, broad raw traces, credentials, or a claim whose scope cannot be stated.
When the user explicitly asks to propose, submit the candidate if the evidence
and scope are sufficient; otherwise explain what is missing.

## Reference governed context

1. Discover the configured capability surface first. For MCP, inspect its tools
   and use context or graph retrieval. For CLI, SDK, or HTTP, use the matching
   context operation rather than inventing an endpoint.
2. Query the narrowest useful scope. Treat only results explicitly marked
   eligible for reuse as inherited knowledge.
3. Preserve the result's identifier, scope, status, evidence limits, and
   supersession or conflict state in the working record. A previous proposal,
   rejected candidate, expired item, or unresolved conflict is not reusable
   context.

## Submit a bounded proposal

1. State one precise candidate conclusion or relation. Include its intended
   reuse scope, not an open-ended generalization.
2. Submit only the minimum evidence projection needed to support it: stable
   artifact references, test or experiment receipts, observed outputs, and
   relevant provenance. Exclude secrets, tokens, raw prompts, private source
   material, and unnecessary traces.
3. Use the configured proposal operation (`conclusion.propose` or
   `relation.propose`) and bind the submitted evidence. Use an idempotency key
   when the client supports one.
4. Read back the proposal and obtain its review summary or receipt. Report its
   identifier, scope, evidence references, status, and review URL or receipt.

An agent may run deterministic checks or an advisory evaluation when available,
but neither is approval. Never call an owner approval action, never approve a
proposal you created, and never describe a candidate as governed context until
an authorized human has approved it.

## Completion record

End the task with one of these explicit records:

- `Governed context used:` identifiers and reuse limits.
- `Proofpress proposal:` identifier, candidate, scope, evidence references,
  status, and receipt or review URL.
- `No proposal:` why the outcome was routine, incomplete, out of scope, or
  blocked.

Do not say that downstream reuse is authorized unless the read-back status
records authorized human approval.
