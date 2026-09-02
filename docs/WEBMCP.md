# WebMCP surface

Proof Press exposes a same-origin owner page as both a human governance UI and a WebMCP tool host.

Live demo: https://proofpress-personal-hosted.onrender.com

## What agents may do

Registered on the signed-in owner page via `document.modelContext.registerTool` (fallback: `navigator.modelContext`):

- `get_current_context(scope, task?)` — read eligible governed conclusions
- `get_review_state(conclusion_id)` — inspect checks, policy/LM recommendation, human-decision state
- `get_lineage(conclusion_id)` — evidence, history, whether the ledger currently exposes the conclusion
- `respond_to_review(conclusion_id, response)` — record a clarification response

## What agents may not do

`approve` / `admit` is not registered. Human Approval stays on the owner decision bar.

## How to exercise it

1. Open the live URL in Chrome with WebMCP enabled, or ChatGPT's in-app browser.
2. Sign in with the owner credential from the submission form.
3. Confirm the page badge reads `WebMCP live · approve is not exposed`.
4. Ask the agent to call `get_current_context` for a scope that already has admitted knowledge.
5. Ask it to inspect a `needs_review` candidate with `get_review_state` and `get_lineage`.
6. Human: Request changes. Agent: `respond_to_review`. Human: Approve.
7. Call `get_current_context` again and confirm the admitted conclusion is now returned.

Agents that need to propose still use the hosted `/v1/operations` credential path (`evidence.submit`, `conclusion.propose`). That path also cannot admit.
