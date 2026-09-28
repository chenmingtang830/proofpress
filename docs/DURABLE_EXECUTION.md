# Durable execution envelope for hosted pilots

## Inventory before this slice

| Existing path | Durable state | Restart and retry behavior |
|---|---|---|
| Local/hosted operation idempotency | SQLite `idempotency` rows scoped to workspace, principal, and caller key; the result is committed with kernel events | An identical keyed request replays its result. Reusing the key with changed parameters conflicts. The local file-backed path uses a separate JSON store. |
| Automatic Judge | `hosted_judge_jobs` keyed by workspace, claim digest, and policy digest; `hosted_judge_attempts` covers manual provider failures | Startup reconciles running jobs and current policy. Advice and Owner-policy admission remain distinct events. |
| External experiment ingestion | Content-addressed evidence and a caller idempotency key | The kernel can deduplicate writes, but there was no durable attempt/failure record for the external trigger. |
| Evidence submission and deterministic claim evaluation | Kernel events plus optional operation idempotency | No common execution record joined a retry, version identifiers, output IDs, and a later review outcome. |

## Covered pilot workflows

Keyed hosted `evidence.submit`, `experiment.ingest`, and `claim.evaluate`
operations now create a versioned `proofpress/hosted-execution/v1` record in
`hosted_executions` and one
`hosted_execution_attempts` row per explicit call. Existing unkeyed calls keep
their prior behavior. A pilot connector should derive a stable key from its
external trigger ID and source version, then submit the same bounded payload
with that key on retry. `proofpress.execution.external_trigger_key(operation,
source_system, trigger_id, source_version)` defines the canonical
`trigger-v1-` SHA-256 key over that tuple without embedding the source ID.
Changed payloads or execution versions require a new key. The request key is
scoped to a workspace and authenticated principal;
hosted identity is server-derived.

The record stores an operation fingerprint, applicable schema, adapter,
verification profile, policy and configuration identifiers, opaque run/claim
links, output evidence/evaluation IDs, state, error code, and attempt times.
Model/tool versions are not applicable to these deterministic operations;
automatic Judge retains its policy-bound job path. The record stores no raw
evidence, claim text, provider response, executable diagnostic, or credential.

States are `running`, `succeeded`, `retryable_failed`, `terminal_failed`, and
`interrupted`. A running request at service startup becomes interrupted and
waits for explicit resubmission. A transient I/O or ledger-head failure may
be retried with the same key; a terminal validation failure needs a corrected
request and new key. Concurrent use of one key fails closed. The kernel event
and idempotency transaction remains the source of truth: if a crash occurs
after that transaction but before execution bookkeeping finishes, retrying
the same request replays the result without adding governed events.

Owner-only `GET /owner/api/executions` returns bounded records and attempts.
`/owner/api/activity` also shows failed or interrupted attempts. The
inspection result resolves evidence IDs to current claim IDs and shows their
review decision and admission authority basis where present. These are links
to the governed ledger, not a second admission decision. An Agent cannot use
the Owner inspection path or gain approval authority from an execution row.

This slice does not persist external source payloads for unattended replay or
turn every connector into a background job. Connectors resubmit the bounded
payload after restart. Add a new job type only when a validated pilot requires
server-owned extraction or scheduled verification work.
