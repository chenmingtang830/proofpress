# Baseten training evidence adapter

Proofpress can project selected evidence from Baseten Training Jobs or Loops
into the generic external-experiment ingestion contract. Baseten remains the
system of record. The adapter runs locally, computes digests over exported
provider records, verifies selected JSON pointers, and sends only bounded
observations to Proofpress.

## Supported upstream records

The v0 bundle accepts two Baseten product shapes:

- `training_jobs`: requires the Baseten training project ID and job ID. Exported
  records can bind job state, metrics, checkpoint metadata, evaluations, or a
  selected log summary.
- `loops`: requires the Loops session ID and run ID. Exported records can bind
  trainer/sampler state, a policy-version observation, an evaluation, or a
  stable `bt://loops:...` checkpoint reference.

Baseten exposes Training Jobs APIs for job metadata, logs, infrastructure
metrics, and checkpoints. Loops exposes sessions, runs, trainers, samplers, and
checkpoint resources. The adapter does not fetch those APIs itself and never
accepts a Baseten credential. Export provider responses into a local JSON bundle
first, then select only the observations a reviewer needs.

## Bundle and ingestion

Start a Proofpress task run, replace `binding.proofpress_run_id` in the example,
then ingest it:

```bash
proofpress run --actor agent:researcher start "Review Baseten training evidence"
proofpress experiment --actor agent:researcher \
  ingest-baseten tests/fixtures/baseten_training_v0.json \
  --idempotency-key baseten-job-42-v1
```

Each record has a stable `source_uri`, its exact exported JSON `payload`, and a
non-empty list of selected JSON pointers. For each selection the adapter:

1. verifies that the pointer resolves in the record;
2. hashes the canonical record payload with SHA-256;
3. binds the pointer, digest, bounded observation, artifact type, and selection
   reason into `proofpress.external_experiment.v0`;
4. computes a separate digest over the adapter selection plan; and
5. discards the raw provider payload before calling Proofpress ingestion.

The adapter also checks Baseten identity consistency on every selected record.
Each Training Job record must contain a `training_job` whose job and project
IDs match the declared source. Each Loops record must contain a `run` whose run
and session IDs match. Records without that per-record binding are rejected
instead of being attributed to the declared run.

## Trust boundary

- Raw logs, rollouts, training examples, optimizer state, and checkpoint bytes
  stay outside Proofpress. Declare uncaptured material in `known_omissions`.
- Do not place API keys, authorization headers, presigned checkpoint URLs, raw
  prompts, or private trajectories in the bundle or resulting observations.
- A provider-reported `SUCCEEDED` state proves only that Baseten reported that
  job state. It does not establish model quality or scientific validity.
- A checkpoint record binds provider metadata or a stable checkpoint URI; it
  does not validate checkpoint contents unless the exported source record
  itself contains and binds a content digest.
- Import creates evidence only. A separate candidate claim, deterministic
  evaluation, and authorized Human Approval are still required before reuse.

The fixture at `tests/fixtures/baseten_training_v0.json` documents the complete
v0 bundle shape.
