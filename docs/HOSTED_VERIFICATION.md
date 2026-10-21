# Hosted verification and customer keys

Fresh Owner setup preselects **Proofpress hosted · GMI Cloud**. AI-assisted
checks stay **off** until an Owner saves the disclosed processing choice. Existing
workspace provider choices, credentials and consent are preserved. Deterministic
checks require no model provider and still run automatically on proposal.

The hosted adapter uses **GMI Cloud GPT-6 Luna** (`openai/gpt-6-luna`) at
`https://api.gmi-serving.com/v1/chat/completions`. This is JSON LLM review,
not Jev or the Decisions API. The operator provisions
`PROOFPRESS_MANAGED_GMI_API_KEY` in the deployment's secret manager. An absent
key displays “awaiting operator setup” and blocks activation. No key is returned
to the browser, included in a policy, or taken from another workspace.

The endpoint and hosted model are fixed. Bounded packets request an error rather
than silent context truncation. An invalid response records no advice. There is
no silent cross-provider fallback: changing the recipient requires a new Owner
policy save. The optional OpenAI Decisions BYOK adapter uses a separate OpenAI
credential and endpoint; GMI credentials are never sent there.

## Owner flow

1. Open **Admin → Verification**, turn on **AI-assisted checks** and inspect the
   named recipient, model and review criteria.
2. Keep the hosted provider or select a provider with your own key. BYOK keys are
   encrypted using the existing workspace secret store. BYOK never falls back to
   a platform credential if authentication fails.
3. Save to authorize external processing. Automatic mode reviews existing
   pending findings as well as future findings; this can consume provider usage.
4. Review advice and make the approval decision. Hosted GMI review is advisory
   and cannot be combined with automatic approval. Turning AI checks off stops
   future model review; it does not retract previously approved knowledge.

GMI receives the bounded finding, evidence and workspace criteria. It returns
accept/reject/escalate advice and an explanation. These are model judgments,
not calibrated truth scores or authorization. Deterministic checks run first;
the Owner decides whether a supported finding may be reused.

## Research over time

**Admin → Knowledge rules → Load research over time template** loads a draft.
It changes nothing until the Owner reviews and saves it. Customize topic keys,
sources, date cutoffs, comparison criteria and exclusions for the customer.
Rules guide the agent; they do not create schedules or backfill old documents.
The existing daily task must read the capture policy, retrieve time-bounded
context before writing, then submit material changes and later outcomes.

Before calling a pilot operational, verify a real customer task run, a later
context read, source freshness, duplicate handling, backup restoration and
credential revocation. Operator usage caps and workspace budget enforcement are
not implemented by this setting; configure provider limits before broad rollout.

Protocol reference: [GMI LLM API](https://docs.gmicloud.ai/inference-engine/api-reference/llm-api-reference).
