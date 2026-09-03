# Proofpress — WebMCP Challenge submission kit

Submission deadline: September 3, 2026 at 1:00 PM PDT.

## One-line pitch

Proofpress lets an agent inspect evidence, run checks, and prepare governance work directly inside the browser—while preserving the one boundary that must remain human: authorization to make knowledge reusable.

## Why WebMCP

Agent-produced knowledge normally breaks at the browser boundary. An agent can generate a conclusion, but the person must manually find the right record, inspect its evidence, run the right checks, configure policy, and return context to a successor agent. Generic browser automation can click through that flow, but it cannot express the product's authority model.

Proofpress exposes the signed-in workspace as a semantic WebMCP surface. The agent can orient itself, retrieve the review queue, inspect exact evidence and lineage, execute deterministic checks, prepare policy and credential forms, and navigate the owner to the precise review. The tool surface deliberately does not expose approval. Once the owner approves in the UI, the agent can retrieve the newly admitted, current, in-scope governed context.

## What people and agents do together

1. The agent calls `get_workspace_summary` and `list_review_queue`.
2. It selects a candidate and calls `get_review_state` plus `get_lineage`.
3. It calls `run_deterministic_checks`; the resulting receipt records no Human Approval.
4. If policy or access needs configuration, it calls `prepare_review_policy_change` or `prepare_agent_credential_issue`. The prepared form is visible but inactive.
5. It calls `open_review` to hand control to the owner.
6. The owner approves, rejects, or requests changes in the UI. `prepare_review_response` hands a requested revision to the separately credentialed agent path without pretending it was submitted.
7. The agent calls `get_current_context` and receives only admitted, current, eligible knowledge.

This was difficult before WebMCP because the agent either needed a separate privileged admin API or had to infer meaning from pixels. WebMCP lets the page expose the same product concepts the person sees, while the browser and application retain the authority boundary.

## Implementation

- React owner workspace registers imperative tools through `document.modelContext`, with `navigator.modelContext` compatibility.
- JSON Schema constrains every tool input.
- Read tools carry `readOnlyHint`; ledger-derived content carries `untrustedContentHint`.
- Tools reuse the same-origin authenticated owner APIs and existing operation kernel.
- Provider keys and credential secrets are never returned to agents.
- Policy and credential changes are prepared in `sessionStorage`, rendered in Admin, and require an explicit owner action.
- Approval/admission has no WebMCP tool.

## Live and source

- Live app: https://proofpress-personal-hosted.onrender.com
- Source: https://github.com/chenmingtang830/proofpress
- WebMCP contract: [`docs/WEBMCP.md`](WEBMCP.md)

The Devpost submission form may include the owner credential for judges. Do not place it in this repository, the video, screenshots, or submission description.

## Demo video storyboard — under three minutes

### 0:00–0:20 — The problem

Show the Review queue. Say: “Agents create conclusions faster than people can decide what future agents may rely on. Proofpress turns that into a governed handoff.”

### 0:20–0:55 — Agent orientation

In ChatGPT's in-app browser, ask: “Summarize this workspace and find one conclusion that needs review.” Show `get_workspace_summary` and `list_review_queue` returning structured state.

### 0:55–1:25 — Evidence and checks

Ask: “Inspect its evidence and lineage, then run deterministic checks.” Show `get_review_state`, `get_lineage`, and `run_deterministic_checks`. Emphasize that checks append evidence but do not approve.

### 1:25–1:50 — Agent prepares; human authorizes

Ask the agent to open the exact review. In the UI, inspect the readable evidence and click Approve. Say: “Approval is intentionally not a WebMCP tool.”

### 1:50–2:20 — Trusted continuation

Ask: “What can the next agent rely on in this scope?” Show `get_current_context` returning the newly admitted conclusion and compact provenance.

### 2:20–2:45 — Governance beyond one claim

Ask the agent to prepare a policy or agent credential configuration. Show the prefilled Admin form and the notice that nothing is active or issued until the owner confirms.

### 2:45–2:55 — Close

“WebMCP makes the whole governance workflow agent-native without making authority agent-owned.”

## Submission checklist

- [ ] Merge the WebMCP release PR after required checks pass.
- [ ] Confirm the Render deploy is healthy and serves the merged commit.
- [ ] Test the live URL in ChatGPT's in-app browser.
- [ ] Confirm every registered tool returns structured output.
- [ ] Confirm no tool can approve, reveal a provider key, or reveal an agent credential.
- [ ] Seed one bounded demo candidate and one already admitted conclusion.
- [ ] Record and publish an under-three-minute YouTube video with audio.
- [ ] Add the live URL, public repository, text below, video URL, and judge credential to Devpost.
- [ ] Re-run the hero flow after submission and retain the test receipt.

## Devpost description

Proofpress is the governance layer for agent-produced knowledge: what may be relied on, why, in what scope, and under whose authority.

Its WebMCP-enabled owner workspace gives agents a semantic way to inspect a real review queue, trace conclusions to bounded evidence, run deterministic checks, prepare review policy and credential configuration, and route a person to the exact decision surface. Humans keep the consequential authority: approval is deliberately absent from the tool list. After an owner approves, a successor agent can retrieve only admitted, current, in-scope knowledge.

The result is a human-agent workflow that ordinary browser automation cannot express safely. The agent handles discovery, evidence navigation, verification, and setup; the person makes the accountable reuse decision; the next agent inherits a compact governed context instead of raw traces or an unreviewed memory dump.

Proofpress uses React, TypeScript, Python, Render, MCP, and the imperative WebMCP API. All WebMCP calls reuse the product's canonical operation kernel and append-only receipts. Tool annotations distinguish read-only calls and untrusted ledger content. Secrets never enter tool results, and prepared policy or credential changes remain visibly inactive until the owner confirms them.

## Judging alignment

- **Usefulness:** reduces the human bottleneck around reviewing agent-produced knowledge without removing accountability.
- **Originality:** applies WebMCP to authority-aware knowledge governance rather than generic page automation.
- **Execution:** runs against a real hosted ledger, review UI, policy system, credentials, and successor-context projection.
- **Thoughtful WebMCP use:** tools expose semantic product actions, annotations identify risk, and the missing approval tool is an intentional security property.
- **Human-agent experience:** the agent does the tedious evidence work; the person sees the exact consequential decision; the agent continues from the authorized result.
