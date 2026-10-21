# Hosted verification and customer keys

Fresh Owner setup preselects **Proofpress hosted · OpenAI Decisions**. AI-assisted
checks stay **off** until an Owner saves the disclosed processing choice. Existing
workspace provider choices, credentials and consent are preserved. Deterministic
checks require no model provider and still run automatically on proposal.

The current hosted adapter uses `https://api.openai.com/v1/decisions` and
`gpt-6-luna`, not Chat Completions. The operator provisions
`PROOFPRESS_MANAGED_OPENAI_API_KEY` in the deployment's secret manager. It must be
an OpenAI credential. An absent key displays “awaiting operator setup” and blocks
activation. No key is returned to the browser, included in a policy, or taken
from another workspace. Do not reuse GMI credentials at OpenAI.

GMI-hosted Jev is the preferred future route if a supported deployment is
available. It is not advertised as connected merely because the GMI catalog
contains GPT-6 Luna. Model identity does not establish Decisions protocol support.
Until an authenticated typed request succeeds against a supported GMI endpoint,
OpenAI Decisions is the implemented fallback. There is no silent cross-provider
fallback after a customer has consented: changing the recipient requires a new
Owner policy save.

## Owner flow

1. Open **Admin → Verification**, turn on **AI-assisted checks** and inspect the
   named recipient, model and review criteria.
2. Keep the hosted provider or select a provider with your own key. BYOK keys are
   encrypted using the existing workspace secret store. BYOK never falls back to
   a platform credential if authentication fails.
3. Save to authorize external processing. Automatic mode reviews existing
   pending findings as well as future findings; this can consume provider usage.
4. Review advice and make the approval decision. OpenAI Decisions is advisory
   and cannot be combined with automatic approval. Turning AI checks off stops
   future model review; it does not retract previously approved knowledge.

The adapter asks three typed predicates: evidence support, scope validity and
workspace criteria. All three must be at least 0.90 for supporting advice;
otherwise it escalates. Refusals escalate. Missing, duplicate, unknown or invalid
answers fail without a recommendation. Estimates are not calibrated truth scores.
The explanation is a fixed summary of those estimates, not model-generated prose.
The first version supports individual findings, not relation or batch review.

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

Protocol reference: [OpenAI Decisions](https://developers.openai.com/api/docs/guides/decisions).
