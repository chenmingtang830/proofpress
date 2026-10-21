# Request changes

In the hosted Review page, a reviewer enters a bounded correction and clicks
**Request changes**. With hosted GMI AI checks enabled and processing consent
saved, the page discloses that this sends the note and already-bound evidence to
GMI to draft a new candidate. The request returns immediately; Review shows
progress and a **Review revised claim** button when the job completes.

The cloud worker is not the customer's Codex agent. It cannot read local reports,
fetch prices, run tools, or obtain new evidence. If the correction needs missing
inputs, it records **More evidence needed** with a reason and offers the existing
agent handoff. Other providers, disabled AI checks, and legacy clients retain the
manual handoff. No existing request is retroactively sent to a provider.

## Invariants

- Preserve the original claim and review. Propose a separate candidate linked by
  `revision_of` and the exact `revision_request_ref`.
- Preserve evidence versions, source filename/field descriptions, scope,
  applicability, expiry, and existing qualifiers, including temporal metadata.
  This first version revises statement/title, not those protected fields.
- Re-run deterministic checks. Advisory review follows the workspace's existing
  automatic/manual mode and includes the recorded requested change.
- Requested revisions require human approval, even if automatic admission is
  otherwise enabled. A model cannot approve its correction.
- One durable job per workspace/request. Duplicate enqueue does not call the
  model twice. The worker rechecks the request and policy before committing.
  Concurrent human decisions or an existing successor prevent a stale proposal.
- Resume queued jobs on startup. Interrupted running jobs are shown explicitly;
  do not silently repeat a potentially paid provider call. Linked proposals remain
  discoverable if a restart happened after the proposal commit.
- Provider failures preserve the request, expose a safe error, and offer manual
  handoff. They do not fabricate a new claim or expose raw provider errors.

## API boundary

The existing authenticated, CSRF-protected `POST /owner/api/reviews` accepts
`automatic_revision: true` only alongside `decision: request_changes`. The server
checks current review authority, active request/lineage and provider consent;
agent credentials cannot enqueue this Owner UI action. Receipt reads include
`revision_automation.available` and a request-specific `revision_job` with state,
detail and optional successor ID. The original MCP proposal API remains usable
for manual revisions requiring new evidence.

## Acceptance before release

Test the click → progress → linked candidate flow in a non-production workspace
with an authorized GMI credential, including a missing-evidence request. The
repository tests use a stubbed provider; they do not demonstrate live model
quality. Merge/deploy and partner acceptance are separate from PR creation.
