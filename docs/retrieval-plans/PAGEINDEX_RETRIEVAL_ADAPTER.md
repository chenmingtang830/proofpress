[//]: # (ob:36c14089)
# PageIndex retrieval adapter — legal matter gap-disclosure contract

[//]: # (ob:19668a0b)
## Status and scope

[//]: # (ob:a856a7d9)
This is the implementation contract for the PageIndex gap adapter in the
legal-matter knowledge pipeline. It is deliberately not an assertion that
PageIndex is already preferred in production. The product goal is a governed
context API: a full data room becomes a source/page/section substrate,
task-relevant claims are constructed and admitted through the existing path,
and only unanswered lawyer asks trigger bounded discovery.

[//]: # (ob:237cdc42)
The adapter's only responsibility is candidate discovery and locator
production. It does not participate in primary claim construction, because
using it to create the claims later used to judge it would be circular.
Proofpress remains responsible for immutable evidence receipts, deterministic
eligibility checks, policy recommendation, and human admission.

[//]: # (ob:de350ec5)
## Matter evidence substrate and progressive construction

[//]: # (ob:8366779b)
The caller may first build `proofpress/matter-evidence-catalog/v1` over all
manifest sources. The catalog records original URI/media type/SHA-256/byte
length, deterministic page/section representations, transform and
representation digests, stable section IDs, and source navigation. It is a
retrieval substrate only: it creates no claims, carries no authority, does not
enter governed context, and does not write the ledger. Any source-byte or
transform-config change invalidates its representation and PageIndex cache.

[//]: # (ob:5186ec1a)
Task decomposition and candidate-claim proposal are separate fixed stages.
The legal lifecycle checklist is supplied to decomposition, but rubric, gold
answers, and silver locators are not. A fixed lexical page/section retrieval
pass over the complete catalog supplies receipts for frozen requirements;
PageIndex is reserved for disclosure gaps. Candidate claims remain unresolved
until `propose → evaluate → judge → lawyer review → admit` completes. The
private v8 decomposition/proposal/critic runner lives in the stacked evaluation
PR; #40 exposes the domain-neutral catalog, disclosure, assimilation, and
sidecar contracts rather than a public legal task-construction command.

[//]: # (ob:54ace136)
The implementation is a local Go sidecar, `tools/pageindex-sidecar`. Its
JSON request schema is `proofpress/pageindex-sidecar/v1`; it receives only
sources enumerated by the caller's corpus manifest, verifies every source
SHA-256 before indexing, and caches a tree under the source digest plus the
configuration digest. It has no hosted-retrieval fallback. PageIndex may use a
runtime-supplied Proofpress dev AI Gateway credential to build or search its
tree, with the model/provider route fixed by configuration. The key is read
only from the sidecar process environment and is not a protocol field, receipt
field, log field, or repository artifact.

[//]: # (ob:42b1cca2)
## Inputs

[//]: # (ob:5f28e5e2)
The adapter accepts a content-addressed document source, a task query, and an
adapter configuration. The source digest is the identity boundary: a tree,
page map, or preview derived from one digest must never be reused for another.

[//]: # (ob:0c9453f4)
The configuration must record the PageIndex package/model version, tree build
settings, query mode, maximum selected sections, and maximum selected pages.
Its canonical digest becomes `retrieval.config_digest` in the receipt.

[//]: # (ob:60425159)
## Runtime sequence

[//]: # (ob:1571ad28)
1. Verify the source bytes against `source.content_digest`.
2. Build or load a section tree keyed by that digest; cache entries are invalid
   on a digest mismatch.
3. Search the tree with the task query and return ranked section candidates.
4. Resolve each chosen section to one or more source pages and extract the
   exact evidence quote from the selected page text.
5. Emit one `proofpress/retrieval-evidence/v1` receipt per selected quote:
   - `section_span` when the section identity and section digest are available;
   - `page_span` when only page-level provenance is available;
   - `text_span` for an exact offset in canonical extracted text.
6. Send the receipt through `proofpress evidence import`; no candidate becomes
   reusable knowledge until the existing evaluation and human-admission path
   succeeds.

[//]: # (ob:cc331373)
## Governed disclosure flow

[//]: # (ob:19a12a7d)
`proofpress disclose` is the agent-facing, read-only progressive-disclosure
surface. It accepts a free-form query, actor, optional scope and graph seeds,
an explicit corpus manifest, and bounded limits. Its output is
`proofpress/governed-disclosure/v1`, with separate `governed_context`,
`coverage`, `lineage`, `traversal`, `discovered_evidence`, `gaps`, `blocked`,
`actions`, `ledger_head`, policy/config digests, and discovery telemetry.
Default bounds are depth 2, 24 claims, and 6 discovered receipts.

[//]: # (ob:20fa4e69)
The command first deterministically matches only actor-eligible admitted
claims, then traverses only admitted, eligible relations within the requested
bounds. The resulting claim lineage exposes the existing conclusion,
admission, and evidence receipts. Ineligible neighbours are represented only
by opaque identifiers and a required action; their statements and evidence are
not disclosed.

[//]: # (ob:e7e35bf8)
Only an unmet or novel query may invoke the PageIndex sidecar, and only against
the caller-provided manifest. Returned `section_span` or `page_span` receipts
are source-navigation handles for the calling agent. They are labelled
`not_governed`, remain outside `governed_context`, do not write ledger events,
and cannot become a conclusion or change admission without the existing
propose → evaluate → judge → human-review path. Each discovered receipt is
bound to the gap that triggered it. Blocked neighbours expose only opaque IDs
and required actions; they never leak statements, quotes, or evidence.

[//]: # (ob:dfb90f4a)
`proofpress assimilate` is a separate post-disclosure gate. It revalidates the
packet, receipt/locator, caller manifest custody, actor/scope policy, ledger
head, duplicate/conflict state, and limits before any model is called. The
default is a dry-run recommendation (`ephemeral_only`, evidence import,
candidate claim, conflict proposal, or escalation). Only explicit `--submit`
with an unchanged head and idempotency key may import evidence or create an
unresolved candidate; it can never admit a claim automatically. This contract
is domain-neutral: Legal is an optional claim profile, not an assumption in
retrieval or disclosure.

[//]: # (ob:905225dc)
## Receipt mapping

[//]: # (ob:ee5211eb)
| PageIndex output | Proofpress receipt field | Deterministic check |
| --- | --- | --- |
| source bytes | `source.content_digest` | SHA-256 equals imported source identity |
| section node ID | `locator.section_id` | non-empty typed locator |
| canonical section serialization | `locator.section_digest` | SHA-256 receipt value |
| resolved page range | `locator.page_start` / `page_end` | positive, ordered page span |
| page text or rendered-page representation | `locator.page_digest` or `text_digest` | SHA-256 receipt value |
| PageIndex query and settings | `retrieval.query` / `config_digest` | typed immutable provenance |
| adapter release | `retrieval.adapter` / `version` | typed immutable provenance |

[//]: # (ob:8634da1d)
## Explicit non-goals

[//]: # (ob:db8423cc)
- Do not make PageIndex a new admission authority.
- Do not treat a tree match, embedding score, or model confidence as evidence
  integrity or as counsel approval.
- Do not silently fall back from a section locator to an unlabelled quote.
- Do not introduce a vector database as part of this adapter PR.

[//]: # (ob:4ed61524)
## Acceptance tests for the implementation PR

[//]: # (ob:ad7f8157)
- Given the same source digest and configuration, repeated indexing emits the
  same section identifiers and receipt digests.
- A changed source byte digest invalidates the cached tree and cannot reuse its
  old locators.
- A selected section produces a receipt that the #39 contract imports and that
  passes the `retrieval_receipts` deterministic check.
- A missing page mapping, malformed locator, or quote that cannot be bound to
  the adapter's extracted representation fails closed.
- A corpus digest mismatch invalidates a cached tree; a sidecar response that
  names a source outside the manifest, omits `fallback_used: false`, or emits
  an invalid receipt fails closed.
- Disclosure tests demonstrate actor/scope filtering, bounded blocked-neighbour
  projection, explicit limits, novel-evidence labelling, and no automatic
  evidence import, claim proposal, or admission.
- Existing lexical and OTLP evidence paths continue to work unchanged.

[//]: # (ob:d1c0a627)
## Follow-on evaluation boundary

[//]: # (ob:b0dd596c)
The adapter will be compared with the current lexical-chunk baseline only in
the separate retrieval-adapter evaluation PR. This document intentionally
makes no general quality claim for PageIndex. The corrected private panel used
all 93 authorized mixed-format canonical representations, froze 27 gaps with
25 eligible locators over nine scored tasks, and completed 27/27 fresh-cache
builds with 100% receipt/custody validity. PageIndex nevertheless trailed BM25
by 12.04 percentage points on evidence-set coverage@5, with paired 95% CI
[-34.26pp, 0], and its fully cached replay had 71.108-second p95 latency.
PageIndex therefore remains an experimental gap adapter; the negative efficacy
result does not change this implementation's source-custody or admission
boundary.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzk2ZmI4ODgyNDBkYWQ5NjNiYzAzZGIwMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjYxNmNiNjdkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV80ZDA0OTVkZWE0NmEzNGEyODdlYTAzYzMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzE3ZDE3MjA1Yzk3ZjY3Njc3ZWQxYTE2NiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXXtv3MiR_yqEFsHd4WYkvjmU_zkndvZ02GQNrxMcEC2kJrupYcwhJ3xIVnYN3F_3AQ73CfNJrqr6QXI0GsmS19nsNbBIRjOc7urqetevxj8csbYvC5b3FyU_Oj3abi_SuMhWq5UfupzxNA6y3A145vpHi6Os4bcXvLwSXQ_PdmvmR_Gpn-bC42xVZH7BXJ7EYhUyHgsvXHEWx15QxB6PUuYHoecXacaTjAWRy3xWpDn3EliXl13eXIv29uj0B_yjv-jZFexQsR63WsCLTFTwxh9FWxYlyyrhtOK67MqmdtbwfNPeOtmt86ZtmmLbiq6D72xZ_p5dCTzU7O22-bOA4w4tLrju-213enJyVfbrITvOm81Jvhb1pqyvelZfrQL3ZPbtVvxlKOH1xdCJ9iJv6k7UwIu-HcTHxdFaMGRi7MV5Fif8SL5zIa7pIWCuuAi5G6YRFyyMWRAyf5UI5gZ5gJQ1bY9Hu6jKWgDl-kaqCy8BPvlulKdJESdxkgjuMS-O5XEUdRc523ZDBQf2kc68aXl3dPqnH47U9j8cwS03bYev5MeCX2TA8j8d5Q0XH46-hxNoaYCNeZN3J63o21Jcs2q5rVjdnbx5-fXrs9-_ev2fF29fv3t79vqPL7-5ePnq5Zt3r98eb_DAnyJOrIfFs6GHW7zIWFd2KFSiKi5YB9ztBa039OumRZrflzUu2d12vdjAJzXb4OVK2hfwxQ7F4ei0HqoKTpKv4f6E5EBWNfl7eDaIcy90Vyk8DlfXiw94zjfA6rMaFnHMYR3G2bYXrfO3__pfp9xsK7EBFjL4miKCcU7UbVEKxQ2885Xz-HXwwA4S0CKnF0f97RZPgrICcnf0cTFS7KVxvGJuNqP4O1hi6BxWcwf0Br57iK6vnD2PH9iRraKYJTx98o7vQCEd-I85XHTlVU3f2jk8CpNTNK3Tr4VhUr9mI2lb1rIZXX6Q5DwP_WfQZbb6p85p6uoWLqrbggqXWVmV_S0SncNSJQez4xibhKsfoCv0My_P2Zyus3o79N0D92IeOnAbUeGvRCQ-dfXJWR2W52Lb433QCnW_hOfRYAjugI4PeCtO1wxtLhbwUH_grG6ehlFQhE-gBp4vyquhlfe_GbrekUaIRGDUHWW1Tzag1pVzLQ5QE7uhH3nRXFLfDnVfboTTgaEWdf6Qbux5_JA2RonHuL968o7esUMu7JZOLZkOjgu8nMOuWFkDVy7lu8fqspS7vTw-r0faKnB5M8JSN_L9iOdzwkQuym3vbNh2iyd5gBN3nj7ACCEi3_NE9tT9fpzceDP0IEDOjxPvjaJBSxWlqDh89EqAJINThnOXI2XkLWd0reIg5MzjM7pef9hWZV72Tt3Uy6uGVQ8p5t4vHOAGz1ahH-T5M3ZdOq8aeBKZ936qDsypxQ2o8qYk7-ZIdwjGCuTBfOeAYISCx17kzzX2JVkEBrLqYHzVGUu8Y6UfYNNjl3nz9gGPw5NiBar12WlcOl-XEPtIXWMbo3BSpchrzMzSAuRuK8D4g786wFPu5S6L_Tm9v22qqrlZAkXo-AdJXNYMNWcQ1h5m5EPfPcC7zOUQW8f556Fl6jZuyqpyMjTcG7C8wJIbCJGJlfnQtugzKvGhzCEyzNdD_d7ZNdTfL3TgeQReFIX3Im-JuUfqEx0iiguvKLjIfCG8XIRRFLssEIUfuBjlNT2tqWJjR8XGDkTp-fttU9Y9hfot7YShn_4LI7_vMagGLbydrDANtCeLUAj_xBi8a4r-ooCrEe22LVWo32XeaRZlIuFF4MWJcIM4CPIi94PU88LMD2Lw7XEWxvBGshJB4HluUgRFwrI4EwFnQYIS1oGcU8gub-vUSyC2xXeOfNePl-5q6cfvfPc0CE694F9d99RFrimOo7AyvvIECMjHybs_fNk4n4RVRuJr1q1R9FgScS9Os8wt4AFaYxKcKzn-zDG12rvgQVikRRYHidB7T8Jsvfdj42a1quAQHPlBwfPUrDoJpdWqz4mNwRuSXnf4wXk93hhoL8fAw3hNzYZj56zH3SCSKjMBNk5AzIsOAzaQKRbuh0uf1yOnkbwKNJVDQAwBCasqwRfakuBLIA1MRiFatAolENw2fMhxreM90ZriTxy6icuDwg0ofCL-TEJ6w5-nx-gOSBmDBPe8nhA0Dyo2GGKNK4I5QT6Xm80gjcsuJ7vFObBkDD1yBzh5pUkh69EtHGliKJzdwDVy5UuQpPWwQV5r932AP2BT0iBd5a6fh5o_k9RilMpDWYNaa5V4gRdFjHuc6bUmicRdXn9yjsC69w5Eu-2tPCarz2u91MyjHjvv1rtut-ykHwdO98hG7ZhOceFWCOD5Fi08hJFa1tA9gRS34M25U7TNBkTDrEe5RA0epUV31YoBicZ7ZSDqa9EeYPoqybIoFVlcJIFm1CTHmTDqqekLGdwFncvJhrLi53Un-h4uDASHOOjgows47YdyM2wgi6hEjhFIJ0iCO8nhOx8jizoIAs96UoimRlesWZKhKEJOcWmMxLE8gM4mUG2RcCXnB1iUgwyCd0oZi1PNokniNcrl4zIpzXjP4yIOwKcGmbHBY3KlVn1WtuQfO79GhqMIVQ0DIdUslbfxXtwCG7NbaVrl914AK0GrHVgJ2Aa7tCCnNbCvhHtzHAcDcCN2Zbdhfb6GrYJj5zvB2lyGR7S6CZZGVaF7hAsZ2tppWf1-vOPRouGNhseQi3VNdQ10ADVgZpoOglhDfEPCD6faNK3hCokD7QCsQ9svnQTQLD7gX8ay_WWAgErqEDF1Kk8O8h0oiI6d1xvIXHCfy7HAeHLX5Zxce5fG7WxBA816tM8pUbCEW5LEX3RbVl86N2sdlKszGVtAvla9qaN0OCS7ZmWFFvqFXhDJna5GrgLfXFZgCSr0SRBiUvqA_uzO9_Gk6vvSVCg-NUUB-onqMSqV4igcSvEnxvuu-VSD4HXbDFfrKb9GpoOHh7jy8gU434n3UlpKJKHZIhf0vm5uwOHCZaA-VbQHxNkdmoxpOG-8y3JMDresX9Nq3QD2XPDueE8WozTQW6Wp5698N4s9rYGTKsJErx9TF1CLhpEIMgiSg2Bl7OmkVKAWfU7yn0uv6_x4Xv_oLJdLZ_a_-ObMTPx4n4GAT77795dLP4odsFeQnKs7QqWUCxiZlKsqoazBWDtnr3BhFW4ca9kuOa6K2b7YbOF7yCYTlMhVRpnS60EQVoJ5-au81D2r3qVXswdlQch1W2kvlBa3WPieriWVpYeQ_dI5UboD8ouLbpuu7MGtoqcFB6uXQM2QSxu7gBYH8ip6aCn3EXhfJm7d3VBTDt-T6vaoo4yiMRpN7TFxi9Gj0ed0oB3f9qNi_RjXTawBbaJjlRasFevEfF31Ia2sHPhDa-4rSSmVcEM3T1Y84Hlg8oJJlWrUs8cWndS6aZQHnuBxEIe5XndSh1LrPqus1GO6roIyh3wdpAGbTHCkBVOilsTGkbEOXYI0d2w0fWiOICMWV7g4Pgyf5RDwgZ9wwKAAD4Hjkz27sgKBAlteMCw_QDQlfdXovLVCgR8EGR1qag1W2uNM14J9KREAgiASw96XA3aXZXjjQAZEOmjvwcKih1AS8ebtAZvJOST0scjz1OUmRh8LbONdPrcypvcL_SJkkVgFYswpx2KZueOnV7lQGMixgLvvdMggF5m5ZjDFbacCGKmycvWO-P3Skc02PjW-JtyX8RMGN7J6hBEWl0JFtLEaL4vidgeoQAqayhhOvcNuXKyyTgx6Jj6YUdzjfBWkJglWhl1SL3NdB-4eUhtJz6j5Fzrru3T4XZej6CCNAY7pFAV9IkbvFVzxZrT3pBgy1iKq1CkhQaF0B6QXyehn6e4YZ-xY1gKiF1CbCuJATmS81gGBKsHR2b59982bMeTAWKAjJpQ12FbQlpumfQ_6oq7qgJj7OZis3E-CLDOp-qTmOYr5E-qW2nr5kXDTInT90GS7k1Lmngz1U8uRqOVYw5ORYQkJqgw4Mb_pxVhOWuoNJkcAI-BQpcakviUFD_AZWKXb8xqtaYfBHIYOyrDlDQh7XrFyQ9pubO2d3Or7j8iIPU15wct-tyVPDX6U8zvv72_hS4QC6J35AIEK_yCtfWAZlXOf0NmPQpYLL4if1R3esc5Up0N9rpyvG_BMXOQMFPuyb5qqO0EDQPZz2R3oUeZ5EHgBVRdGur7GmlWNpZWyQ60eIMUpQJMeaBMc-NpBBAHzfJbwZ1MwzWzU18SlrubQ1S1BOsgcYvVwKVOytrmCbxzq67sFC0WcPps-WabZbPC6i7IFbZxZcdRcGcUIVVkkzVtSRe8AfSIRQZQVq2fT9y3tiSHLRlA0XTeYqaoiEEMjdd28FzsFJSl2B-j7TN0zCOLQy_NdtwAWhYzaXN0mle2731ctG9Q-5WOlEikNkl4fTDhaVHg7H7q-4WMd8HgOgBgVe4ezaptXogAzL_e5UteynFyLqvaKe9afKOj-9b_bihxP1u0GBWTqZViiE3LaAoMA2Tw6vk8R79lJOadOScbY8jBenWJhfUpH3bcswY415nu0a_-mbyVQjNjHGyyQL2sxQCAi_VohPxjZ-fLN2fF9HeZ7ReElhx0wilnKIIYoxjxnkoGMEkslfcm-7ydC_cPRzfrWUDyXZhV4VXcUR0qb4ZgyRx0EzFMZMbEiBhXN0Mt4FgOsfSkSttIe3dpk7qoIiiJhiWBB4LIsyeM0T1PDnGnPctqvm_Yxf7A-z_o86_O-oM97PEBht0EfLcZ1T72P-3vxDwETPgv6IAwDn6csy4s8zwJQiWQVuylLGY_DIMlCN40h5_KZl66iMPZ4EXAWBxDN-6zgHg8ec7g5EiF557qnUXQa7EMiBL5Ii4IVFolgkQgWifDzRSIkAdiJ1NWzGRI9MIYaE_48NXaQn1yiUHTn9X989-3vHVW1APFeA29wqWnj8c53se_4wil7yZ5r5d3Oa1l_7BxRDxsSM9XhxbIjSA9eJQSPW9Al4EZZwI4LbNLL-F7Q_cklzmvdo8hE0VAbWJZKF6poSS5V1cYx6G-nPWpV-txWg1KROXxAfkw6ATzHOtK6wYrNcjQtWP7G6vfxxPCgv8QiKTuvicsgkt0AzgGMsfPtVtQvz5w3FeuxEDnNr_pGIg9QWzrZpqZiL0It4JNeVsbeC5Jo1DYp7WOLWAXScB85dTXr67JtaqqLkdHopCaTtPdN3lSyc7eYN_IWIBpX-iX1kqj3hJM72oJbeIyFx1h4jIXHWHiMhcf8neExnEeQIOWRF-e-1sBJXWPU608rUGhvlnpZlqaBn3tsDPxNzUKt_pziw06FC8zq0MLDgoKO0Z0VoIxLChi0u8pl83Irm10y3ZA1tJZt1yB9wDdwQSQRCrBwJ6Kal0KxtUyhngb7lHCnU73ZU7VFxVlIK2Fadpf6uQuV818CHZcqU4anL3UMLnDiVooWvn3Fth3-P-V-guNLJn0HviRhai_wki7pXFxF0SfSJZhG9_0-QBRg71eZ50apcZOTCs_MTT6tVIOSj3Lcg5ZBMEn1-AWKARprhm7UfEk9tXDMF1tRkU50xE_j2VSX8Lymm-pkKAL3MVSkS7K8ract4K4b3TA36gYMyiHCRQ-O8Y1SM3n9d_IXkIDakFSL8moN-7bSh5h2t-Aqjge_02wZkHgHf8AcNYLNHXmLL5CoEkwrthswEOvmBDCUfgxQtQrxA1eZhZkPaplluRcZANtYDFNX-ZyqViv5Iy9LemkZgMsEZYmWuUTF0eqE7g6dIry14ycQWDUx9JrTcBfG8S1rdl1eSZO4hn0rMZbFcEMqcaMloeu_pdvQgBpQLmDbhda6y4VKW1GN8Sz7FBKiYUoGbtoSNFbqlkO1tE4plwFCoHGXAbUSImqiU5l7UnXXBfmp4FGigfLo_O2__8eUA-iPPw_oGvCVNP4qNkbLr1r6Iyyk2-l3gDf-RlyBzUOPWI8mUGoCbFmUFUSiY9Vi2Gyle64nNSHM-kc7dkDULADTAjAtANMCMC0A8-cLwExSwQvhJsJlsQVgWgCmAWC-1EnPTrVjxmw2ZfUL1CBVSTWQFM0NBLzh8-r2dICF1I1ZVUMicqkrw_gLRPwU1bTDNAdOSzKEy7Fa0zG68t0TvBrTVakhXGyApp5SLUo9TmTuB1EPcIeYrHM6lUktTRhPNyp_V4nk26SGMvtbyAB5bA9Jk2Gq6ZD2g_2DYAzuGpfaKQwsxhAMvCWr6LBjJ8MCYi0g9hcKiKUkZgTEwjXWzU39U_7YVUUZEGhifwgm8Rl-N-ruos_9xadHrMghk3dFHs1W_B0clsRdGYpuyLQZrKeIsQeQSo9dhpol8IlsCx_m6SqI4yRJs89O7ztTcKB6haxHyS7htDK3oa2M3V6CZ2XVAf5G3gqiM6ppfmZ6sU3AsWYg8yVV4TXF4uXcQ1AdQ5u2A_Q-ESf2CEl7IoLqMTJcZKlbhOyzYtvACIGnxp9bvJRtfOMXgJ_9FCp5BW8e7_uxlz0o4Ym6PYzdLcCSOZvHKtGCOkdLzB-vWa39zFSz7sH7TlTqXrjqH7ZjtDw5OjYvRT8Hixqw6kJXYjE-oUhXYKLRt7eyjNId36cp95LxSjnbDpi-dTJ4TEZh8-irpXx1JFPtvpaQhS0WDLBRry8YOUN3eJ9Q7b8pQvCasI63t8t2kDoIV4TNsE6Aq4L4rTMlOxPSzbDJ-xC9Zzopc74K3YkL2isJKhpc6mB0all3uTDlwK4g7-XI43G9nEUi8ThPAreIPTfiLE0C3-f34XoN-u1hXK913NZxW8dtHfcXctyPH1jYRQOHUzRw9HE_2PeLQJ2ZH4AJhoyLB6kXMzcqIpaCEiY-dwORJWGeeCzM8hBybFGEWSFiwdx85ftpWIQxe8zh7kCd41M3PI2SPVBnD3L5KEpWPy-ocxF6PM-92BMjhu4pUOeZg4bQZN8kzd8B9-y6QSqCQuRiFT6Me95TDDaBnS4Wj4zAAEyzQHbQz2tiw1KxYcSlbMst1VmeDXm-D9lMjXr1t4N9Cqn4uhlLYFPqF718c4agQQqsse7ugNnYGPCbrjYSuPbEtMNMmHVe74mwZb_e-EE1yaVBBwblM4MJYOFNNX-p9DTAy-6GWl0Vu7lFeGX3HvGo5RV2i3VcZxDVh6DKWQRRmCvgiuMvCeWGm-WNkLhX7GJAULzFr9JFlRtIOvYkJAtkPRs6EJ2BKtgQNfeNIyNMWbiTLEZr3jqE04TPZUsbnr1pBvDyWPEr23yoWHsMgvM8TPm8zH5e_2SYcpGyVRElQei6BtA4ielGjf-cwZiu3rLcKwKPpcwdG4BjfDaF5zwxsGquCOiHQgPaW2E5VBbtlYopcI16ViFjQRJB4ktEGPzh7dnJRvCSUY_zRDVnT7CJg2amvgIF2umIzJR23q3oKBWtO4J1AddwQGPWzVCdowVCZlAu9DJnrxSaVrUhRuyItmVsMuwxuRpUqVMUUSnLVAjWIKWctYQVlTV-2eNcGO0BkavJi-yMtEo6jI5JOAlNEhOk5Nh5WWuk_pJ6Xaih5tRLBd1SaJJpTwZbKDvswJ1GA0wtmwOSnIYgy77PRBYZkzOJnrU0PSPsBdn7gG22XkGY39Gx0eVWIFT5bV6pX7_FNgXeihkCAGsx25Pg_U47ZG2ZL4DHCK-WtldfdFmhzOpOH5EB_Ab2KiJ0O2VH3JQIIBIdLA_JfS_hbeBQ-1HSFWUGUSL7sEXb_FXUGsdFFY4XOz4Q76e9VkD1WRC7BWX6jbHVymIqYNJQaxwGmFiCh14-AimknJCCCuE75M8uzXE6Oyxjh2XssIwdlrHDMnZYxg7L2GEZOyzzJYdlcpG7ceK6EY-EHZZ51rCMblbS4Ms4OGM6l58yRQPL3TdGs3-CRuV0prpiGqSgBa9EwYaql4yQtpID19eOv3D80CSTuEDsjBSO0yV2Ouf_w3ROEharNAjS0BN2OucXNp3zGuOTu6pNBlBDduWPvLGtAhrLijEWyIFDv5aGaSq9Ui_kbSqBPXvVyZPuyGlHgnqrYv9KsPcTkV3ICKSTKFsluodGewLf9zxXZH5ocqZJ92-Px_rUNt4ZpgwzWDcmOghPMYnkiQFCm7KmKkqqH9xbzGC-0mQvlFSc12jJQWAGdFuwB9lyeNlLtkg1ke5KJ_2svlWTCFRORyElucUfLpHWXf7cjMKOzAvKzj9fiu1aYB2iusALu1zcgQGDbZ0XfhaOoWqGDRYdbE_L_suxQ-bAuN_L5VICVi7Pa_KYZCg0eh4PLdN0LmBPyALyW0r2yWwQFSNVqBCydo8p61h7GqMyKrrAX0qqyPqjUpHxNvAY9C07w2nn9d3pNOepw2nTmu2smmaH0-xwmh1Os8NpdjjNDqfZ4TQ7nGaH0-xwmh1Os8NpT_vXGj5tOO0zAY4fAbvd-yvZP8lOz_m3mO9bfv9gzWOmR35TMdWqJxcjESTXq_mMTNNiRbNvDSZh25bXyIYJsSirzs0aQi9ZMntLUxrbIavQ-TVUIZTQs3nG-tDv-N8_d6Nd0aQvL-uyH7DtDw4IjXR9NVDyIYtCkwSRi2vn5ZnzNSx1w6hQO1D5dqDi4j0Xdi9N09_H1y6mrHVd7FoYjo1ZAxZpTWkMjA-V8WapizRDdLH3jMTI25PNyhF5eLJHhnTcpfvH41yMpGuK5iXKWCFb6wRuQdrkjZ58FXoK3pHLfvsnzcOkUeSnWZJmK_BDRSSSwHNFUdz7O_cGIv2I37m3tuKxtuLxQ0oG7j6C3IOP-zHsXwTBH_EQEyiP-1kMSWqeFTzIQq9YBW4g3CDKVn4gYo9q__EqLHiRuiJfCeaFjGVpeP-RdnH7Xnrqu6detAe3z4rMB7-YWty-xe1b3L7F7VvcvsXtW9z-LwK3L-JQsDSA2GKEZ1rc_i8cty_bzzoTguR3xuYTfY0nOcgpKGc71DWylTDyCooD10mwgjEihyO_fUE58BR3M899NScX858kmPzkwEKquEl1VQwDPGEINMYAAwGiKs2WckSOfZa_K8jSAbkPgtjlGUTLKz-2Awo_zwGFVsKdl8Yg3F_NeHBUAc0pziqYgiv1304UcAnUhcon0koAM_cg7CfDDef106YbnHuGG85rO91gpxvsdIOdbrDTDXa6wU432OkGO91gpxvsdIOdbrDTDXa6wU432OkGO91gpxvsdIOdbrDTDXa6wU432OkGO91gpxt-4ukGkbuB6wdpFhTBL326gQotsgKku-IQ7YA_kuk1Jt4zcLNCPhH8QrX_MUE1wAOEg8105s2r38rio0rDsNqYYZ2Y8g5YZfTD1ORBNeYSjzX6K1If8rEcdKMG7atxuxfIN9ZrHLNBmajEfY-PmQrrCJheiz3ZwePmPKhecXrftMfOpzszH3c-nU9-UNHgtC3hNC0H_3n18xgDmbR4LxBD1f0U_1TRl5uceBzkH3ibS4FqMsguBEEEJ2phpHwC9p8habiTBkvlUjY0toAuEmR3FH9RINA-V2hFJrNxcFLlgX8o4-3YSB13mq2_O40gtVti8Ei4DwNoMdzED29pLmDs1cL7zafPBITcDdOICxbGLAiZv0oEc4M8uG8mwMCvH54J-DL4-QNDDXvA5t7H_VjyL4KfD3xW5CxdJcyPQ7EKReFHwOzC89w0YlnKkpz5ES9iv_CKyPXdFY-4H3mrLInczD9wpDl-fvXOTU497zQM9-DnYy_OszjhFj9v8fMWP2_x8xY_b_HzFj9v8fMWP2_x8xY_b_HzFj9v8fMWP2_x8xY_b_HzFj9v8fMWP2_x8xY_b_HzFj9v8fMWP2_x8xY_b_HzFj9v8fMWP2_x8xY_b_HzFj9v8fMWP_8zx8-vojTmobdy02L1j4yfh1Qa84v5z3Pvw8-D_rSqlD3D0KNUn-OqThpor_jXXYDuGMbdQa8QPsDxE-r2E0_Oaz8ai0EGrkDAgxoZokDyWPpXBbARF-wnJ7BWAXusl6TNkClLyD2x23PdX5lsUCV9EnqPrnzi7yk9AYZXGF-DkpXoMH_9Oz-iUo_nH7shFuRzPAniAJsS6zgkSAoshHVuXVz8t0gVI7eMEuw0-pXzm7Pz-k_LIDz24-124bjfL8y4AIL4brUxahGYfeusIQ1LvGPPXcHKoBVwD2mkIdTHU0QFNuVk-qlRYrLYCkaBHGk1BThSjg-nxZILdkQUPhsTpHvmDcpuxymDIVa1G83QqbqrSgXbA-37_iP893-roiTl)
