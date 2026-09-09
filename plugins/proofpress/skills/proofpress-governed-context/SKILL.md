---
name: proofpress-governed-context
description: Use Proofpress governed context when a task must rely on or hand off durable agent-produced knowledge, including evidence-backed decisions, experiment results, integration contracts, or incident learnings. Retrieve eligible context before relying on it; submit bounded proposals and receipts when a durable outcome is produced. Do not use for routine code edits, transient debugging, or unvalidated hypotheses.
---

# Proofpress governed context

Use this skill to make downstream reliance explicit: what is eligible to reuse,
what evidence supports a new candidate, and which authorized human must approve
it. Proofpress is not a replacement for the agent runtime, its memory, or raw
private traces.

## Customer context policy

Before deciding whether to propose, look for
`.proofpress/context-policy.yaml` in the current repository. If it exists,
apply its repository- or workflow-specific `propose_when`, `do_not_propose`,
evidence, and applicability guidance. If it does not exist, use the core rules
in this skill.

The customer file is an agent-side proposal-selection policy, not an
authorization policy. It may narrow what the agent proposes, but it may never
override this skill's safety rules, server-side checks, credential boundaries,
or Human Approval. Treat unknown schema versions or conflicting rules as
`Draft only` and report the policy problem instead of guessing.

Start from the maintained template at `assets/context-policy.yaml` in this
skill. Customers should copy it to `.proofpress/context-policy.yaml`, then
configure and version that file rather than fork this core skill.

## Initialize a repository policy

Initialize a policy only when the user explicitly asks to set up, initialize,
or add a Proofpress policy for the current repository. A missing policy alone
is never permission to write one.

1. Resolve the current repository root and inspect
   `.proofpress/context-policy.yaml` without modifying it.
2. If the file is absent and the bundled helper exists, run
   `python3 scripts/initialize_policy.py --workspace <repository-root>` to
   show the proposed addition. After the explicit request to initialize, run
   it again with `--apply` to create the template unchanged. If the helper is
   not bundled, show the proposed addition from `assets/context-policy.yaml`
   and create that template unchanged only after the same explicit request.
   State that the customer should review, narrow, version, and commit the copy.
3. If the file exists, make no change. If its `schema_version` is unknown or
   malformed, report that policy initialization is blocked and keep the task in
   `Draft only`; never replace, merge, or repair the file automatically.
4. Do not create the policy during plugin installation, do not use lifecycle
   hooks for it, and do not treat the file as authorization. Server invariants
   and Human Approval remain authoritative.

Keep LM Judge configuration separate from this intake policy. When a workspace
uses advisory evaluation, start from `assets/judge-criteria.md` and save the
adapted criteria in Hosted Admin. The Judge evaluates evidence support; it does
not decide what enters Proofpress or authorize reuse.

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
- `Proofpress proposal: No proposal —` why the outcome was routine, incomplete,
  out of scope, or blocked. Keep the `Proofpress proposal` prefix so readers
  unfamiliar with the workflow understand what was not created.

Do not say that downstream reuse is authorized unless the read-back status
records authorized human approval.
