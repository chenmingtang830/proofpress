# Experimental Jev advisory judge

Jev can optionally evaluate existing claims and relations through **Vercel AI Gateway**.
This is the usable trial path while TypeSafe direct keys are invite-only. The optional
bridge uses Node 22+ and pinned official `ai@7.0.105` / `@ai-sdk/gateway@4.0.85` packages.
Install its locked dependencies after installing Proofpress (including in deployment images):

```sh
npm ci --ignore-scripts --prefix "$(python -c 'from pathlib import Path; import proofpress.hosted.jev as j; print(Path(j.__file__).with_name("jev_gateway"))')"
```

From a source checkout use `npm ci --ignore-scripts --prefix src/proofpress/hosted/jev_gateway`.
The Render Blueprint includes this step; applying it still requires a separate release.
There is no runtime dependency download. Missing Node/packages fail closed. Existing
non-Jev providers and direct TypeSafe calls do not invoke Node.
TypeSafe direct remains an optional Python-only transport for accounts with access.
The current OpenRouter default and all saved workspace configurations remain unchanged.

## Boundaries

`evaluate` and `relation evaluate` remain deterministic and offline. `judge`,
`relation judge`, and `judge --batch --scope …` use the configured advisory backend.
Jev checks an **already proposed relation**, including its type and direction;
it never discovers neighbors, proposes edges, edits statements, or approves anything.
An accepting judge result is not human admission. A proposed `contradicts` relation
has no quarantine effect until an authorized human admits it. Raw graph/review
surfaces may show candidates; governed context excludes unadmitted candidates.

The Gateway transport uses the official SDK's experimental `evaluate` API with
`gateway.evaluationModel('typesafe-ai/jev')`, not an OpenAI-compatible chat endpoint.
See [Vercel's evaluation announcement](https://vercel.com/changelog/typesafe-ai-jev-now-available-on-ai-gateway).
Gateway Boolean `probability` becomes the internal Noul value; Choice confidence comes
only from `providerMetadata.typesafe.confidence[question_id]`. Missing confidence fails
closed, rather than being replaced by the highest choice probability. Retries are disabled.
The requested ZDR setting is sent as `providerOptions.gateway.zeroDataRetention`.

The direct transport follows [TypeSafe's API](https://docs.typesafe.ai/api):
`POST https://api.typesafe.ai/v1/systemone`, Bearer auth, `state`, `model`, and a
question-id map. Each item gets one Choice (`accept`, `reject`, `escalate`) and
three Noul questions for evidence support, scope, and workspace/reproposal criteria.
Question instructions identify the item explicitly; the model does not see question IDs.

Mapping version `jev-conservative/v1` requires choice probability >= 0.9 and
Choice distribution confidence >= 0.8 for accept/reject. Accept additionally
requires all three Noul values >= 0.9. All other valid answers become `escalate`.
These are experimental engineering defaults, **not calibrated accuracy guarantees**.
Confidence describes the answer distribution, not edge strength. Noul has no
separate confidence. Rationale is an explicitly labeled code-generated template.

## Local CLI trial

Use an isolated repository with synthetic evidence. Install this worktree into a
separate virtual environment, or set `PYTHONPATH` to its absolute `src` directory.
Existing explicit `judge.command` policy configuration takes precedence over env opt-in.

```sh
export PROOFPRESS_JUDGE_PROVIDER=vercel_jev
export PROOFPRESS_JUDGE_MODEL=typesafe-ai/jev
# Supply AI_GATEWAY_API_KEY securely in your shell; never paste it into source or logs.
python -m proofpress.cli demo
python -m proofpress.cli judge CLAIM_ID
python -m proofpress.cli relation judge RELATION_ID
python -m proofpress.cli judge --batch --scope demo
```

Use a `needs_review` claim ID returned by the synthetic demo. Demo creation is local;
`judge` makes a billable external request, so use only the intended synthetic packet.
To test a relation, propose it between two demo IDs with
`python -m proofpress.cli relation propose CLAIM_A --to CLAIM_B --type supports --proposer agent:trial`
and use its returned relation ID. Check `relation propose --help` for the full command.

`AI_GATEWAY_API_KEY` (Gateway) or `TYPESAFE_API_KEY` (direct) is the local fallback only when `PROOFPRESS_JUDGE_API_KEY` is absent.
An explicitly empty injected key blocks all fallback. OpenRouter keys are never
sent to TypeSafe. Changing opt-in settings changes the policy digest and can make
previous approvals require revalidation; do this in the isolated test repository.

## Hosted trial and UI

In a separate test workspace, open Admin → Review policy, select
**Vercel AI Gateway · Jev (experimental)**, keep `typesafe-ai/jev`, provide a Gateway key using
the existing encrypted workspace credential field, and explicitly allow external
processing. Enable the Gateway ZDR checkbox. Start with **Run when requested** and **Human decision anytime**.
Changing provider requires a matching replacement key; the host's local
`AI_GATEWAY_API_KEY` / `TYPESAFE_API_KEY` is intentionally not used as a shared tenant fallback.

Run deterministic checks, then request model review. The review page shows the
Jev template summary and an expandable structured-advice panel with probabilities,
confidence, model, latency, and mapping version. After manual validation, the existing
**After checks pass** mode can schedule the same adapter. That setting controls
when advice runs; it does not enable automatic admission. Direct TypeSafe integration
does not claim or send a Vercel/OpenRouter ZDR flag.

The CLI and operation API return the same additive `decision_audit` on the existing
`judge_recommended` / `relation_judge_recommended` events. It includes the bounded
question map, validated typed answers, requested/returned model IDs, request digest,
question/mapping versions, mapped recommendation, UTC timestamp, latency and available
token usage. No new raw evidence copy or API key is placed in audit metadata.
Claim/relation and policy digests remain bound by the outer event. The Jev contract
version is also bound into its generated judge policy. Old judge receipts remain valid. Gateway uses audit v2, adding a validated transport
record with SDK pins, ZDR request, and normalization contract. Its `response_model`
is explicitly a Gateway route identifier, not proof of an immutable underlying model revision.
Direct TypeSafe audit v1 remains supported.

Batch judging makes one shared-state call for at most 32 claims and has the same
128 KB request/response ceiling as single-item judging. These are Proofpress bounds,
not Jev's 255-option Choice cardinality limit. Every item has a separate answer map;
batch usage and latency describe the **whole request**, so do not sum repeated usage
across its receipts. A malformed or missing answer rejects the whole batch before
recommendation events are recorded. Larger batches fail explicitly; use individual
calls. Jev escalation remains recorded for human attention and does not trigger a
second identical paid call. Existing LM batch follow-up behavior is unchanged.

Missing keys, failed deterministic checks, oversized packets, timeouts, upstream
errors, missing answers, unknown enum values, booleans/NaN in numeric fields, and
invalid probability distributions fail closed. No accepting recommendation or
admission is synthesized. Fix configuration or evidence, then retry explicitly.

## Verification and production gate

```sh
node --test src/proofpress/hosted/jev_gateway/bridge.test.mjs
PYTHONPATH=src python -m unittest discover -s tests -p 'test_jev_judge.py' -v
PYTHONPATH=src python -m unittest discover -s tests -v
npm ci --prefix web/owner
npm --prefix web/owner test
npm --prefix web/owner run build
npm --prefix web/owner run test:jev
```

The unit/integration and browser tests use fake Gateway/TypeSafe answers with synthetic data;
they verify transport wiring, failure handling, credential separation, audit persistence,
and unchanged human authority. They do **not** establish real Jev availability or quality.
A small synthetic live Gateway canary on 2026-09-17 confirmed the documented
`typesafe-ai/jev` route, Boolean answers, keyed Choice confidence, usage, and acceptance
of a ZDR request. That proves connectivity, not calibrated review quality or provider retention behavior.
Before production, compare the same labeled evidence/relations
with the incumbent judge, inspect false accepts and escalation cases, and record observed
latency/cost. Review the localhost UI and explicitly approve release separately.
No live workspace migration, deployment, or default switch is part of this integration.
Rollback for a test workspace is selecting its previous provider/model and matching key;
old audit events stay intact and policy-dependent advice must be refreshed.
