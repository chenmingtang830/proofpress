# Task run tracking

Proofpress task runs connect authorized knowledge retrieval to explicit usage,
external outputs, and later observations. They are an append-only operational
record. They do not change claim review, LM Judge advice, or Human Approval.

## Operation contract

All surfaces use `proofpress/local-operation/v1alpha1` through `/v1/operations`.
Hosted requests derive `actor` from the authenticated credential.

| Operation | Required input | Result |
| --- | --- | --- |
| `run.start` | `purpose`, `actor` | running `proofpress/run/v1alpha1` |
| `run.finish` | `run_id`, `status`, `actor` | terminal run; status is `completed`, `failed`, or `aborted` |
| `run.get` | `run_id` | run plus receipts, reliance, outputs, and observations |
| `run.list` | none | newest-first run summaries and per-kind counts |
| `context.capture` | `run_id`, `actor` | `proofpress/context-receipt/v1alpha1` containing exact returned claim IDs and digests |
| `reliance.record` | run, receipt, exact claim ID/digest, purpose, actor | explicit `proofpress/reliance/v1alpha1` declaration |
| `output.record` | run, external reference, SHA-256 content digest, actor | `proofpress/output-reference/v1alpha1` |
| `observation.record` | run, kind, source, meaning, actor | append-only `proofpress/observation/v1alpha1` |

Observation kinds are `test`, `human`, `external_evaluation`, and `outcome`.
Optional run metadata must be a JSON object no larger than 8 KiB.
Proofpress stores each observation independently and does not calculate an
overall score. Output content remains in its source system; only a bounded
summary, reference, media type, digest, and reliance links are stored.

`context.capture` runs the existing authorized governed-context path. Its
receipt freezes the claim statement, content digest, evidence references,
admission receipt, policy digest, and ledger head seen at capture time. Later
policy or claim lifecycle changes do not rewrite the historical receipt.

## Permissions and identity

The eight run operations are safe agent operations, separate from owner-only
review and admission operations. New agent credentials may be issued with all
safe operations or an explicit subset. Existing persisted credentials keep
their stored subset during migration; run permissions are never added to an
old restricted credential. Every reference is resolved inside the authenticated
workspace's event store.

MCP exposes matching `proofpress_*` tools without actor arguments. Python SDK
methods use the operation names directly. The thin CLI is isolated under
`proofpress run` so the legacy portable workflow remains unchanged:

```sh
export PROOFPRESS_PRINCIPAL=agent:codex
proofpress run --workspace . start "Implement task-run tracking" --idempotency-key run-001
proofpress run --workspace . capture RUN_ID --task "task-run tracking"
proofpress run --workspace . rely RUN_ID RECEIPT_ID CLAIM_ID CLAIM_DIGEST "Applied the recorded contract"
proofpress run --workspace . output RUN_ID repo://path sha256:... --reliance RELIANCE_ID
proofpress run --workspace . observe RUN_ID test "targeted unittest" "Assertions passed" --output OUTPUT_ID
proofpress run --workspace . finish RUN_ID completed --summary "Implementation verified"
```

The Owner workspace exposes `/runs`, backed by `GET /owner/api/runs` and
`GET /owner/api/runs/{run_id}`.
