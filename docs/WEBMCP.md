[//]: # (ob:056e3eef)
# WebMCP surface

[//]: # (ob:edd8d768)
Proofpress exposes a same-origin owner page as both a human governance UI and a WebMCP tool host.

[//]: # (ob:51b77f3b)
Live demo: https://proofpress-personal-hosted.onrender.com

[//]: # (ob:1bbd4ca5)
## What agents may do

[//]: # (ob:fee53950)
Registered on the signed-in owner page via `document.modelContext.registerTool` (fallback: `navigator.modelContext`):

[//]: # (ob:6c1ab1db)
- `get_workspace_summary()` — orient the agent to queue, state counts, and current knowledge
- `list_review_queue(state?, scope?, limit?)` — enumerate the bounded work requiring attention
- `get_current_context(scope, task?)` — read eligible governed conclusions
- `get_review_state(conclusion_id)` — inspect checks, policy/LM recommendation, human-decision state
- `get_lineage(conclusion_id)` — evidence, history, whether the ledger currently exposes the conclusion
- `prepare_review_response(conclusion_id, response)` — prepare a bounded revision handoff for the connected agent MCP/CLI
- `run_deterministic_checks(conclusion_id)` — execute non-authorizing integrity and prerequisite checks
- `open_review(conclusion_id, full?)` — route the owner to the right decision surface
- `get_activity(limit?)` — inspect semantic proposal, review, policy, and context-retrieval activity
- `get_review_policy()` — read the active safe policy projection and provider configuration status
- `prepare_review_policy_change(...)` — load a complete policy draft into Admin for explicit human review
- `get_agent_access()` — inspect agent identities and credential lifecycle metadata without secrets
- `prepare_agent_credential_issue(principal_id, label)` — fill an owner-reviewed credential request without issuing or exposing a key

[//]: # (ob:0d65efbf)
## What agents may not do

[//]: # (ob:2123724d)
`approve` / `admit` is not registered. Human Approval stays on the owner decision bar.

[//]: # (ob:86eecbb5)
## How to exercise it

[//]: # (ob:bb8d98c9)
1. Open the live URL in Chrome with WebMCP enabled, or ChatGPT's in-app browser.
2. Sign in with the owner credential from the submission form.
3. Ask the agent to call `get_workspace_summary`, then `list_review_queue`.
4. Ask it to inspect one candidate with `get_review_state` and `get_lineage`.
5. Let it run `run_deterministic_checks`, then `open_review` for the owner.
6. Human: Request changes. Agent: `prepare_review_response`, then submits the revision through its agent MCP/CLI. Human: Approve.
7. Call `get_current_context` again and confirm only the admitted conclusion is returned.

[//]: # (ob:86d90f67)
Agents that need to propose still use the hosted `/v1/operations` credential path (`evidence.submit`, `conclusion.propose`). That path also cannot admit.

## Agent-native product rule

Every user-visible Proofpress capability must have an agent-addressable MCP or
CLI path. Agent-addressable does not mean agent-authorized. Reads and bounded
candidate writes may execute under an agent principal; policy, credential,
retention, recovery, and admission mutations become reviewable change requests.

`prepare_review_policy_change` writes no server state and receives no provider
secret. It opens Admin with a clearly labeled draft. The signed-in human owner
must inspect it and select `Save & activate`; Human Approval remains available
only in the owner UI.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1YTUwMjYxMTU2N2ZkYTA0OWRlZDQzMCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
