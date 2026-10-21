[//]: # (ob:056e3eef)
# WebMCP surface

[//]: # (ob:edd8d768)
Proofpress exposes a same-origin owner page as both a human governance UI and a WebMCP tool host.

[//]: # (ob:51b77f3b)
Use the URL for your own Proofpress deployment when exercising this surface.

[//]: # (ob:1bbd4ca5)
## What agents may do

[//]: # (ob:fee53950)
Registered on the signed-in owner page via `document.modelContext.registerTool` (fallback: `navigator.modelContext`):

[//]: # (ob:6c1ab1db)
- `get_workspace_identity()` — safe workspace/principal/role and configuration metadata, without CSRF or credentials
- `get_workspace_summary()` — queue, state counts, and current knowledge; unavailable sections are explicit and their counts are `null`
- `get_workspace_dashboard()` — the same bounded Home dashboard
- `list_runs(status?, limit?)` and `get_run(run_id)` — recorded runs without executing or scheduling work
- `get_claim_graph(scope?)` — read the bounded evidence, claim, lifecycle, and relation graph
- `list_review_queue(state?, scope?, limit?)` — enumerate the bounded work requiring attention
- `get_current_context(scope, task?)` — read eligible governed claims
- `get_review_state(claim_id)` — inspect checks, policy/LM recommendation, human-decision state
- `get_lineage(claim_id)` — evidence, relations, lifecycle impact, history, and current exposure state
- `open_claim_lifecycle(claim_id, action)` — navigate the owner to withdrawal or reassessment without recording a decision
- `prepare_review_response(claim_id, response)` — prepare a bounded revision handoff for the connected agent MCP/CLI
- `run_deterministic_checks(claim_id)` — execute non-authorizing integrity and prerequisite checks
- `open_review(claim_id, full?)` — load and display the exact requested receipt before returning `opened: true` and `receipt_claim_id`; missing, mismatched or superseded requests return errors
- `get_activity(limit?)` — inspect semantic proposal, review, policy, and context-retrieval activity
- `get_technical_logs(limit?)` — content-minimized technical operation metadata
- `get_executions(limit?)` — recorded execution receipts
- `get_capture_policy()` — versioned capture rules and their limits
- `prepare_capture_policy_change(purpose, capture, exclude)` — stage validated capture rules in Admin → Knowledge rules for human save
- `get_review_policy()` — read the active safe policy projection and provider configuration status
- `prepare_review_policy_change(...)` — load a complete policy draft into Admin for explicit human review
- `get_agent_access()` — inspect agent identities and credential lifecycle metadata without secrets
- `prepare_agent_credential_issue(principal_id, label)` — commit the identity, key label and Agent recipient into the actual Admin form before returning, without issuing or exposing a key

[//]: # (ob:0d65efbf)
## What agents may not do

[//]: # (ob:2123724d)
`approve` / `admit` / `withdraw` / `reassess` are not registered as decision tools. Human authority stays in the owner UI; WebMCP may only inspect or navigate to those surfaces.

[//]: # (ob:86eecbb5)
## How to exercise it

[//]: # (ob:bb8d98c9)
1. Open your deployment URL in Chrome with WebMCP enabled, or ChatGPT's in-app browser.
2. Human: sign in privately with your own Owner or Reviewer credential. Agents must not collect credentials or inspect one-time secret reveals.
3. Ask the agent to call `get_workspace_summary`, then `list_review_queue`.
4. Ask it to inspect one candidate with `get_review_state` and `get_lineage`.
5. Let it run `run_deterministic_checks`, then `open_review` for the owner.
6. Human: Request changes. Agent: `prepare_review_response`, then submits the revision through its agent MCP/CLI. Human: Approve.
7. Call `get_current_context` again and confirm only the admitted claim is returned.

[//]: # (ob:86d90f67)
Agents that need to propose still use the hosted `/v1/operations` credential path (`evidence.submit`, `claim.propose`). That path also cannot admit.

## Agent-native product rule

Every user-visible Proofpress capability must have an agent-addressable MCP or
CLI path. Agent-addressable does not mean agent-authorized. Reads and bounded
candidate writes may execute under an agent principal; policy, credential,
retention, recovery, and admission mutations become reviewable change requests.

`prepare_review_policy_change` and `prepare_capture_policy_change` write no server state and receive no provider
secret. It opens Admin with a clearly labeled draft. The signed-in human owner
must inspect it and select `Use manual review`, `Enable AI checks`, or `Save changes`; Human Approval remains available
only in the owner UI.

## Keeping feature coverage current

The registry is in `web/owner/src/webmcp.ts`; its semantic behavior is tested by
`webmcp.test.ts` and `npm --prefix web/owner run test:webmcp`. The browser smoke
uses an isolated synthetic localhost workspace and asserts that every exercised
read/preparation makes zero server writes until a synthetic human clicks Save.
Navigation tests inspect the actual URL, rendered receipt claim ID, title and
decision-note ID in the same browser evaluation that awaits tool completion.
They cover an already-selected different claim, compact/full views, absent or
mismatched receipts and overlapping requests. Credential tests check the actual
mounted identity, label and Agent recipient at completion, including a form
previously set to Reviewer and a fresh Admin mount. These completion boundaries
use React's [synchronous integration commit](https://react.dev/reference/react-dom/flushSync)
only for the external tool calls; ordinary workspace refreshes remain batched.
Tool failures return structured text with `isError: true` instead of opaque
browser exceptions. A summary can return useful sections while another section
is unavailable, including an unconfigured workspace.

The provider schema accepts live IDs from `get_review_policy().providers`
instead of a duplicated enum. Preparation validates that the provider exists;
new hosted providers do not silently become unselectable. Optional roundtrip
`rubric` must match the current version. Drafts are validated and visible even
when Admin is already open and remain intact when switching Admin tabs. Saving
manual review preserves authored criteria with AI, provider consent and automatic
admission off. Preparation never saves processing consent or admission settings. Capture limits match the server: 1,000-character purpose, up to 30
rules per list, 500 characters per rule, and at least one capture rule.

`web/owner/webmcp-coverage.json` maps current capabilities to tools and records
human-only exceptions. `python3 scripts/check_webmcp_coverage.py` detects changed,
new and removed Owner source files and hosted Python modules, plus
tool-inventory drift. In normal feature CI, source drift produces a warning
(`--allow-stale-sources`); missing/duplicate inventory and authority metadata
still fail. This allows a feature to merge before the post-main repair runs.
Fingerprints are an audit reminder, not proof of semantic completeness. The
[maintenance skill](../.agents/skills/proofpress-webmcp-maintenance/SKILL.md)
requires inspecting the changed behavior and testing authority boundaries
before refreshing fingerprints.

## Optional automatic maintenance PRs

`.github/workflows/webmcp-maintenance.yml` audits relevant pushes to `main` and
supports a manual dispatch on `main`. It adds missing safe tools and tests,
updates the capability map, and opens or updates one **draft** PR on
`codex/webmcp-maintenance` when a validated patch exists. Updating a previously
ready PR restores draft status before pushing the new patch. It never merges
or deploys. It does not run against arbitrary PR branches or fork content.

A repository maintainer enables it by configuring:

- Repository secret `OPENAI_API_KEY` for the Codex GitHub Action.
- Repository Actions variable `WEBMCP_AUTOFIX_ENABLED=true` after approving model
  usage and the associated API spend. Until then, the generation job is skipped.
- GitHub Actions permission to create pull requests. The workflow requests
  `contents: write` / `pull-requests: write` only for the publishing job.

No provider or partner credential belongs in the skill, manifest or workflow.
Missing model credentials fail with a configuration message; no other secret or
interactive user login is used as a fallback. Enabling the workflow is separate
from checking it into the repository, and requires the maintainer's choice.

Generation has repository read permission, checkout credentials are not
persisted, and the API key is supplied only to the pinned Codex action. The
model uses a workspace permission profile and `drop-sudo`. This follows the
[official Codex automation pattern](https://learn.chatgpt.com/docs/non-interactive-mode#example-autofix-ci-failures-in-github-actions)
and [action security guidance](https://github.com/openai/codex-action/blob/bdf19a4a223ec2549a3e2274a0cf61556bc07675/docs/security.md).

A fresh read-only validation job rejects patches outside the allowlist or
containing executable/symlink modes, then runs inventory, unit, build and browser
checks without the model secret or a write token. A third runner applies the
validated patch and uses Git/GitHub CLI only; it never installs dependencies or
runs patched source with write credentials. Changes to workflows, package
files, guard scripts or authorization backend require a separate manual PR.
If `main` advances during validation, publication stops for a newer run.
Concurrent runs are replaced by the latest run, and repeat runs update the same
PR. No generated diff means no PR. A bounded failure remains visible in Actions
for maintainer review; there is no retry loop or widening of scope.

The workflow's validation job is the observed test receipt for generated code.
GitHub may suppress additional workflow runs from a `GITHUB_TOKEN`-created PR;
a maintainer may need to start required CI checks before merging. Static source
hashes and successful tests cannot guarantee every future user-visible feature
has been correctly modeled, so the draft still requires semantic human review.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1YTUwMjYxMTU2N2ZkYTA0OWRlZDQzMCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
