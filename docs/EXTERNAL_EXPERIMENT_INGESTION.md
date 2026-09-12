# External experiment evidence ingestion

Proofpress can bind selected evidence from Fireworks, another hosted RL
environment, or an internal experiment system without owning that runtime or
copying its raw trajectories. The generic v0 manifest is an offline ingestion
boundary. A provider-specific connector may produce this manifest later.

## Implemented contract

| Manifest field | Existing Proofpress object | Stored meaning |
| --- | --- | --- |
| `binding.proofpress_run_id` | `Run.id` | The local or hosted run receiving the external evidence |
| `source.{system,run_id,uri}` | `Evidence.external_experiment.source` | External system identity and stable run locator |
| `source.{capture_mode,provenance_status,coverage,known_omissions}` | `Evidence.external_experiment.source` | What the adapter observed and what it did not capture |
| `binding.{work_item_id,code_revision,dataset_refs}` | `Evidence.external_experiment.binding` | Optional experiment context; no new authority semantics |
| `binding.config_digest` | `retrieval_receipt.retrieval.config_digest` | Content-addressed adapter configuration; raw configuration is not retained |
| `evidence[].source_uri` and `source_digest` | `retrieval_source` | Owner-controlled source pointer and exact source revision digest |
| `evidence[].locator` and `observation` | `retrieval_evidence` | Bounded, reviewer-readable projection |
| `adapter.{name,version}` | `retrieval_receipt.retrieval` | Adapter identity and version |
| authenticated workspace and actor | selected event store and operation actor | Workspace isolation and ingestion identity |

No database migration is required. Evidence and source records use the existing
append-only event store. The new relationship is additive: imported evidence
records carry `run_id` and `external_experiment`, and `run.get` returns them in
`external_evidence`.

## Trust boundary

- The source system remains the system of record.
- `capture_mode` is one of `instrumented_sdk`, `provider_api`, `webhook`,
  `exported_bundle`, or `manual_submission`.
- `provenance_status` is one of `directly_observed`, `provider_attested`,
  `importer_attested`, or `user_asserted`.
- `coverage` is `full`, `partial`, or `unknown`. Partial coverage requires at
  least one declared omission; full coverage cannot declare an omission.
- Import creates evidence only. It never creates or approves a claim.
- The run actor must perform the import. Hosted transports derive that actor
  from the authenticated credential and isolate lookup to its workspace.
- The schema has no credential or raw-payload field. Credential-shaped URI
  query parameters are rejected. Provider credentials belong in the existing
  hosted secret boundary, not manifests, events, receipts, logs, or exports.

## CLI

First start a Proofpress run, then place its ID in the manifest:

```bash
proofpress run --actor agent:researcher start "Evaluate external RL run"
proofpress experiment --actor agent:researcher ingest external-run.json \
  --idempotency-key external-run-42-v1
```

For a hosted HTTPS service, use the same operation contract:

```bash
proofpress experiment \
  --base-url https://proofpress.example.com \
  --token-env PROOFPRESS_TOKEN \
  --actor agent:researcher \
  ingest external-run.json \
  --idempotency-key external-run-42-v1
```

The server ignores a spoofed hosted `actor` and binds the authenticated agent
identity. Existing restricted credentials are not silently expanded; issue or
reissue an agent credential with `experiment.ingest` permission when needed.

## Python

```python
import json
from proofpress import ProofpressClient

client = ProofpressClient.in_process(".")
manifest = json.load(open("external-run.json", encoding="utf-8"))
result = client.ingest_external_experiment(
    manifest,
    actor="agent:researcher",
    idempotency_key="external-run-42-v1",
)
```

The generic HTTP endpoint is still `POST /v1/operations`, with operation
`experiment.ingest` and parameters `payload` plus `actor`.

## Why the first implementation is offline

This release deliberately adds no Fireworks API client, provider credential,
webhook, or network fetch. It proves the stable evidence contract first. Build
one live connector only after a committed research workflow establishes which
provider fields are material; the connector should map those fields into this
manifest rather than changing admission semantics.
