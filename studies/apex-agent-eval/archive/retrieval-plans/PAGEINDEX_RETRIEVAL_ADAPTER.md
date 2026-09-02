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

[//]: # (ob:d85c0ae6)
[//]: # (ob:v9evidencefirst)
The follow-on v9 construction contract is evidence-first: each frozen
requirement retrieves exact evidence, extracts typed
`proofpress/evidence-atom/v1` records, and passes a deterministic claimability
gate before any proposer is called. Invalid custody, locators, unbound
subject/predicate/value fields, prompt-derived facts, or unresolved
conflicts produce `partial`, `gap`, `conflict`, or `needs_legal_analysis`.
They do not enter a semantic repair loop. An independent critic assigns one
fixed verdict per candidate, and only `supported` candidates may continue to
evaluate/judge/review as unresolved claims.

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
3. For thematic or unknown-location questions, search the tree for typed
   document/subtree routes. Exact date, amount, clause, and quoted-text
   questions bypass tree routing and use global BM25.
4. Run BM25 inside valid routes while retaining a global-BM25 safety lane.
   PageIndex supplies only route IDs, hierarchy paths, confidence, and a
   configuration digest; it never supplies the final quote.
5. Deterministically combine normalized BM25 score, route bonus, exact-heading
   bonus, and source-diversity bonus. PageIndex may not remove a global
   candidate, and at least two of the top five positions are reserved for the
   global safety lane. Timeout, malformed, empty, or low-confidence routing
   degrades to global BM25.
6. Resolve each chosen BM25 span to canonical source pages and extract the
   exact evidence quote from the selected representation.
7. Emit one `proofpress/retrieval-evidence/v1` receipt per selected quote:
   - `section_span` when the section identity and section digest are available;
   - `page_span` when only page-level provenance is available;
   - `text_span` for an exact offset in canonical extracted text.
8. Send the receipt through `proofpress evidence import`; no candidate becomes
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
- Hierarchical-hybrid tests demonstrate exact-query bypass, two global safety
  slots in the top five, deterministic route bonuses, global recovery after a
  route miss, and degradation to global BM25 for every invalid route state.
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzk2ZmI4ODgyNDBkYWQ5NjNiYzAzZGIwMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjM3YWFjN2ViIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84ZmI0MzBhZTgzMDk3MzNhYjdkODZiMGYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzE3ZDE3MjA1Yzk3ZjY3Njc3ZWQxYTE2NiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfXtv3EiS51ch1FjcLq5K4vsh_3OetqdXi9kdw-1dHDBqSElmUsU1i6wlWZI13Qbur_sAh_uE-0kuIvJBslRVkiW3t6cvgcF0uR6ZkZHxjl9QP5-wbqhKVgxXFT85P9lsrrK4zNM09UOXM57FQV64Ac9d_2Rxkrf8_opXN6If4Lv9ivlRfJ5HaRTGnlt4IoVvM9_3ilKkoef6sXBZ4WVpUbh-kfheIELhh2HKmRsGaexlXuCGsC6v-qK9Fd39yfnP-I_hamA3sEPNBtxqAS9yUcMb_ya6qqxYXgunE7dVX7WNs4Lvt929k98777q2LTed6Hv4zYYVH9mNwEPN3u7afxdw3G2HC66GYdOfn53dVMNqm58W7fqsWIlmXTU3A2tu0sA9m_26E_-xreD11bYX3VXRNr1ogBdDtxWfFycrwZCJQcJYkYj8RL5zJW7pS8BccZWWeRi4TMDKWRIELE94GuduiZS13YBHu6qrRgDl-kbqKy_hXuK7UZElZZzESSK4x7w4lsdR1F0VbNNvaziwj3QWbcf7k_O__Hyitv_5BG657Xp8JT8W_CoHlv_lpGi5-HTyE5xASwNszNuiP-vE0FXiltXLTc2a_uzd6x_eXvzLm7f_8-r92w_vL97-2-s_Xb1-8_rdh7fvT9f8ZPFF4sQGWDzfDnCLVznrqx6FStTlFeuBu4Og9bbDqu2Q5o9Vg0v29_0g1vBJw9Z4uZL2BfywR3E4OW-2dQ0nKVZwf0JyIK_b4iNeTFx4oZtm8HW4ukF8wnO-A1ZfNLCIYw7rMM42g-ic__xf_9ep1ptarIGFDH6miGCcE3UblEJxB-985zx9HTywgwR0yOnFyXC_wZOgrIDcnXxejBR7WRynzM1nFP8IS2x7hzXcAb2B3x6j6ztnz9eP7MjSKGYJz5694wdQSAf-xxwu-uqmoV_tHB6FySnbzhlWwjBpWLGRtA3r2IwuP0gKXoT-C-gyW_233mmb-h4uqt-ACld5VVfDPRJdwFIVB7PjGJuEqx-hK_RzryjYnK6LZrMd-kfuxXzpyG1EpZ-KSHzp6pOzOqwoxGbA-6AVmmEJ30eDIbgDOr7FW3H6dtsVYgFfGo6c1S2yMArK8BnUwPfL6mbbyftfb_vBkUaIRGDUHWW1z9ag1rVzK45QE7uhH3nRXFLfb5uhWgunB0MtmuIx3djz9WPaGCUe43767B29U4dc2D2dWjIdHBd4OYfdsKoBrlzLd0_VZSl3e3162Yy01eDyZoRlbuT7ES_mhIlCVJvBWbPNBk_yCCcefPsII4SIfM8T-XP3-2Vy4-12AAFyfpl4bxQNWqqsRM3hozcCJBmcMpy7GikjbzmjCwKQkDOPz-h6-2lTV0U1OE3bLG9aVj-mmHt_cIQbPE9DPyiKF-y6dN608E1k3sepOjCnEXegyuuKvJsj3SEYK5AH85sjghEKHnuRP9fY12QRGMiqg_FVbyzxjpV-hE1PXebd-0c8Dk_KFFTrq9O4dH6oIPaRusbWRuGkSpHXmJmlBcjdRoDxB391hKfcK1wW-3N6_9jWdXu3BIrQ8W8lcXm7bTiDsPY4Ix_77RHe5S7nURYXX4eWqdu4q-raydFwr8HyAkvuIEQmVhbbrkOfUYtPVQGRYbHaNh-dXUP900IHnifgRVF4r4qOmHuiPtEhorjyypKL3BfCK0QYRbHLAlH6gYtRXjvQmio2dlRs7ECUXnzctFUzUKjf0U4Y-ul_YeT3EwbVoIX3kxWmgfZkEQrhnxmD9205XJVwNaLbdJUK9fvcg9QoFwkvAy9OhBvEQVCUhR9knhfmfhCDb4_zMIY3klQEgee5SRmUCcvjXAScBQlKWA9yTiG7vK1zL4HYFt858SG_Wrrp0o8_-O55EJx7wX933XMXuaY4jsLKeOoJEJDPk3d__rZxPgmrjMRXrF-h6LEk4l6c5TLzoTUmwbmS468cU6u9Sx6EZVbmcZAIvfckzNZ7PzVuVqsKDsGRH5S8yMyqk1BarfqS2Bi8Iel1jx9cNuONgfZyDDyM19RsOHUuBtwNIqkqF2DjBMS86DBgA5li4X649GUzchrJq0FTOQTEEJCwuhZ8oS0JvgTSwGSUokOrUAHBXcu3Ba51uidaU_yJQzdxeVC6AYVPxJ9JSG_48_wY3QEpY5DgXjYTguZBxRpDrHFFMCfI52q93krjssvJfnEJLBlDj8IBTt5oUsh69AtHmhgKZ9dwjVz5EiRptV0jr7X7PsIfsClZkKVYKAk1fyapxSiVx7IGtVaaeIEXRYx7nOm1JonEQ15_cY7A-o8ORLvdvTwmay4bvdTMo546H1a7brfqpR8HTg_IRu2YznHhTgjg-QYtPISRWtbQPYEUd-DNuVN27RpEw6xHuUQDHqVDd9WJLRKN98pA1FeiO8L0NMnzKBN5XCaBZtQkx5kw6rnpCxncBZ3LybdVzS-bXgwDXBgIDnHQwa8u4LSfqvV2DVlELQqMQHpBEtxLDj_4GFnUQxB4MZBCtA26Ys2SHEURcoprYyRO5QF0NoFqi4QrOT_CogJkELxTxlicaRZNEq9RLp-WSWnGex4XcQA-NciNDR6TK7Xqi7Il_9T5AzIcRahuGQipZqm8jY_iHtiY30vTKn_3ClgJWu3ASsA22KUDOW2AfRXcm-M4GIAbsav6NRuKFWwVnDo_CtYVMjyi1U2wNKoK3SNcyLZrnI41H8c7Hi0a3mh4CrlY39a3QAdQA2am7SGINcS3JPxwqnXbGa6QONAOwDq0_dJJAM3iE_7LWLb_2EJAJXWImDqVJwf5DhREp87bNWQuuM_1WGA8e-hyzm69a-N2NqCBZj3a55woWMItSeKv-g1rrp27lQ7K1ZmMLSBfq97UUTockt2yqkYL_UoviOROVyNXgW8ua7AENfokCDEpfUB_9uD3eFL1e2kqFJ_asgT9RPUYlUpxFA6l-BPjfTd8qkHwumu3N6spv0amg4eHuPL6FTjfifdSWkokodkiF_Sxae_A4cJloD7VtAfE2T2ajGk4b7zLckwON2xY0Wr9Fuy54P3pnixGaaCXZpnnp76bx57WwEkVYaLXT6kLqEXDSAQ5BMlBkBp7OikVqEVfkvwX0us6v1w2vzjL5dKZ_T--OTMTvxwyEPDJj__4eulHsQP2CpJzdUeolHIBI5NyVSWUDRhr5-INLqzCjVMt2xXHVTHbF-sN_A7ZZIISucooU3o9CMIqMC9_lZe6Z9WH9Gr2oCwIuW4n7YXS4g4L39O1pLIMELJfO2dKd0B-cdFN21cDuFX0tOBg9RKoGXJpYxfQ4kBeRV9ayn0E3peJW3c31JTD76S6Pekoo2iMRlN7TNxi9Gj0OR1ox7f9olg_xnUTa0Cb6FilA2vFejFfV31IKysH_tia-0pSSiXc0C2SlAe8CExeMKlSjXr21KKTWjeLisATPA7isNDrTupQat0XlZUGTNdVUOaQr4M0YJ0LjrRgStSR2Dgy1qFLkOaOjaYPzRFkxOIGF8cvw2cFBHzgJxwwKMBD4Phkz76qQaDAlpcMyw8QTUlfNTpvrVDgB0FGtw21BmvtcaZrwb6UCABBEIlh78sBu8tyvHEgAyIdtPdgYdFDKIl49_6IzeQcEvpYFEXmchOjjwW28S5fWhnT-4V-GbJIpIEYc8qxWGbu-PlVLhQGcizg7nsdMshFZq4ZTHHXqwBGqqxcvSd-v3Zks41Pja8J92X8hMGNrB5hhMWlUBFtrMHLorjdASqQgrY2hlPvsBsXq6wTg56JD2YU9zjfBZlJgpVhl9TLXNeBu4fURtIzav6VzvquHf7Q5Sg6SGOAYzpFQZ-I0XsNV7we7T0phoy1iCp1SkhQKN0B6UUyhlm6O8YZO5a1hOgF1KaGOJATGW91QKBKcHS2P3_407sx5MBYoCcmVA3YVtCWu7b7CPqiruqImPsFmKzCT4I8N6n6pOY5ivkz6pbaevmRcLMydP3QZLuTUuaeDPVLy5Go5VjDk5FhBQmqDDgxvxnEWE5a6g0mRwAj4FClxqS-FQUP8BlYpfvLBq1pj8Echg7KsBUtCHtRs2pN2m5s7YPc6qfPyIg9TXnBq2G3JU8NfpTzB-_vb-FLhALonfkAgQp_I619YBmVc5_R2Y9CVggviF_UHd6xzlSnQ32unR9a8ExcFAwU-3po27o_QwNA9nPZH-lRFkUQeAFVF0a6fsCaVYOllapHrd5CilOCJj3SJjjys6MIAub5LOEvpmCa2aifiWtdzaGrW4J0kDnE6uFSpmRdewO_ONbXd0sWijh7MX2yTLNe43WXVQfaOLPiqLkyihGqskiat6SK3hH6RCKCKC_TF9P3Z9oTQ5a1oGi6aTFTVUUghkbqtv0odgpKUuyO0PeVumcQxKGX57tuASwKGbW5uk0q2w9_r1o2qH3Kx0olUhokvT6YcLSo8Hax7YeWj3XA0zkAYlTsHc6qbd6IEsy83OdGXctyci2q2isOrD9R0P3r_7gRBZ6s3w0KyNTLsEQn5LQFBgGyeXR6SBEP7KScU68kY2x5GK9OsbA-paPuW5ZgxxrzAe3av-l7CRQj9vEWC-TLRmwhEJF-rZQfjOx8_e7i9FCH-aAovOawA0YxSxnEEMWY50wykFFiqaQv2ffTRKh_Prlb3RuK59KsAq_6geJIaTMcU-aoh4B5KiMmVsSgot0OMp7FAGtfioSttCe3NpmblkFZJiwRLAhclidFnBVZZpgz7VlO-3XTPubP1udZn2d93jf0eU8HKOw26KPFuO6593l_L_4xYMJXQR-EYeDzjOVFWRR5ACqRpLGbsYzxOAySPHSzGHIun3kZAbh5GXAWBxDN-6zkHg-ecrg5EiH54LrnUXQe7EMiBL7IypKVFolgkQgWifDbRSIkAdiJzM0KsDgGPTCGGhP-PDd2kJ9co1D0l80__fjnf3FU1QLEewW8waWmjccHv8W-4yunGiR7bpV3u2xk_bF3RLNdk5ipDi-WHUF68CoheNyALgE3qhJ2XGCTXsb3gu5PLnHZ6B5FLsqW2sCyVLpQRUtyqao2jkF_N-1Rq9Lnpt4qFZnDB-THpBPAc6wjrVqs2CxH04Llb6x-n04MD_pLLJKyy4a4DCLZb8E5gDF2_rwRzesL513NBixETvOroZXIA9SWXrapqdiLUAv4ZJCVsY-CJBq1TUr72CJWgTTcR0Fdzea26tqG6mJkNHqpySTtQ1u0tezcLeaNvAWIxo1-Sb0k6j3h5I624BYeY-ExFh5j4TEWHmPhMf_F8BjOI0iQisiLC19r4KSuMer1lxUotDfLvDzPssAvPDYG_qZmoVZ_SfFhp8IFZnXbwZcFBR2jOytBGZcUMGh3Vcjm5UY2u2S6IWtoHdusQPqAb-CCSCIUYOFBRDUvhWJrmUI9Dfap4E6nerOnaouKs5BWwrTsrvX3rlTOfw10XKtMGb59rWNwgRO3UrTw7Ru26fG_lPsJji-Z9B34koSpu8JLuqZzcRVFn0mXYBrdh32AKMHep7nnRplxk5MKz8xNPq9Ug5KPcjyAlkEwSfX4BYoBGmuGbtT8SH1r4ZgfdqImneiJn8azqS7hZUM31ctQBO5jW5MuyfK2nraAu251w9yoGzCogAgXPTjGN0rN5PU_yF9AAhpDUiOqmxXs20kfYtrdgqs4HvxOu2FA4gP8AXPUCDZ35C2-QqIqMK3YbsBArJ8TwFD6MUDVKsSPXGUe5j6oZZ4XXmQAbGMxTF3lS6paneSPvCzppWUALhOUJVrmChVHqxO6O3SK8NaOn0Bg1cTQa07DXRjHt2zYbXUjTeIK9q3FWBbDDanEjZaErv-ebkMDakC5gG1XWuuuFyptRTXGs-xTSIiGKRm46yrQWKlbDtXSeqVcBgiBxl0G1EqIqIlOZe5J1V0X5KeCR4kGyqPzn__7_5hyAP3j37foGvCVNP4qNkbLr1r6Iyyk3-l3gDf-k7gBm4cesRlNoNQE2LKsaohEx6rFdr2R7rmZ1IQw6x_t2BFRswBMC8C0AEwLwLQAzN8uADPJBC-FmwiXxRaAaQGYBoD5Wic9O9WOGbPZlNWvUINUJdVAUjQ3EPCG31e3pwMspG7MqloSkWtdGcYnEPFzVNMe0xw4LckQLscaTcfoyndP8GZMV6WGcLEGmgZKtSj1OJO5H0Q9wB1iss7pVCa1NGE83ah8rhLJt0kNZfa3kAHy2B6SJsNU0yHtB_sHwRjcNS61UxhYjCEYeEtW02HHToYFxFpA7O8UEEtJzAiIhWts2rvm13zYVU0ZEGjicAwm8RWeG_Vw0Zc-8ekJK3LI5F1RRLMV_xkOS-KuDEW_zbUZbKaIsUeQSk9dhpol8IlsCx_naRrEcZJk-Ven94MpOFC9QtajZJdwWplb01bGbi_Bs7L6CH8jL4XojGqaX5lebBNwrBnIfElVeE2xeDn3EFTH0KbtCL3PxIk9QdKeiaB6igyXeeaWIfuq2DYwQuCp8XGL17KNb_wC8HOYQiVv4M3TfQ972YMSnqjb49jdEiyZs36qEi2oc7TE_PGWNdrPTDXrAN53olIH4ar_uhmj5cnRsXkphjlY1IBVF7oSi_EJRboCE42hu5dllP70kKYcJOONcrY9MH3j5PA1GYXNo6-O8tWRTLX7SkIWNlgwwEa9vmDkDN3hIaHaf1OE4DVhHe_ul91W6iBcETbDegGuCuK33pTsTEg3wybvQ_Re6KTM-S50Jy5orySoaHCpg9GpZd3lwpQDu4K8lyNPx_VyFonE4zwJ3DL23IizLAl8nx_C9Rr02-O4Xuu4reO2jts67m_kuJ8-sLCLBg6naODo836w7zeBOjM_ABMMGRcPMi9mblRGLAMlTHzuBiJPwiLxWJgXIeTYogzzUsSCuUXq-1lYhjF7yuEeQJ3jczc8j5I9UGcPcvkoStLfFtS5DD1eFF7siRFD9xyo88xBQ2iyb5LmvwD37LpBJoJSFCINH8c97ykGm8BOF4tHRmAAplkgO-iXDbFhqdgw4lI21YbqLC-GPB9CNlOjXv3bwT6FVHzdjCWwKfWLXr-7QNAgBdZYd3fAbKwN-E1XGwlce2baYSbMumz2RNiyX2_8oJrk0qADg_KZwQSw8Kaav1R62sLL_o5aXTW7u0d4Zf8R8ajVDXaLdVxnENXHoMp5BFGYK-CK428J5Yab5a2QuFfsYkBQvMGf0kVVa0g69iQkC2Q92_YgOluqYEPUPLSOjDBl4U6yGK155xBOEz6XLW347l27BS-PFb-qK7Y1605BcF6GKZ-X2S-bXw1TLjKWllEShK5rAI2TmG7U-K8ZjOnqLSu8MvBYxtyxATjGZ1N4zjMDq_aGgH4oNKC9NZZDZdFeqZgC16jvKmQsSCJIfIUIg399f3G2Frxi1OM8U83ZM2zioJlpbkCBdjoiM6Wddyt6SkWbnmBdwDUc0Jh1M1TnaIGQGZQLvczFG4WmVW2IETuibRmbDHtMrgZV6hxFVMoyFYI1SKlgHWFFZY1f9jgXRntA5BryIjsjrZIOo2MSTkKTxAQpOXVeNxqpv6ReF2qoOfVSQbcUmmTak8EWyg47cKfRAFPL5ogkZyHIsu8zkUfG5EyiZy1NLwh7QfY-YZttUBDmD3RsdLk1CFVxX9Tq6bfYpsBbMUMAYC1mexK83-m2eVcVC-Axwqul7dUXXdUos7rTR2QAv4G9igjdTtkRNyUCiEQHy0NyP0h4GzjUYZR0RZlBlMg-bNm1fxWNxnFRhePVjg_E--luFVB9FsRuQJm-N7ZaWUwFTNo2GocBJpbgoddPQAopJ6SgQvgO-bNrc5zeDsvYYRk7LGOHZeywjB2WscMydljGDst8y2GZQhRunLhuxCNhh2VeNCyjm5U0-DIOzpjO5ZdM0cByh8Zo9k_QqJzOVFdMgxS04I0o2bYeJCOkreTA9ZXjLxw_NMkkLhA7I4XjdImdzvn_YTonCcs0C4Is9ISdzvmdTee8xfjkoWqTAdSQXfmQN7ZRQGNZMcYCOXDoD9IwTaVX6oW8TSWwF296edIdOe1JUO9V7F8L9nEisgsZgfQSZatE99hoT-D7nueK3A9NzjTp_u3xWF_axrvAlGEG68ZEB-EpJpE8M0BoU9ZURUn1wL3FDOYrTfZCScVlg5YcBGaLbgv2IFsOLwfJFqkm0l3ppJ8192oSgcrpKKQkt_jgEmnd5eNmFHZkXlB2_v5abFYC6xD1FV7Y9eIBDBhs67zws3AMVTNssOhhe1r2H04dMgfG_V4vlxKwcn3ZkMckQ6HR83homaZzAXtCFlDcU7JPZoOoGKlChZC1e0xZx9rTGJVR0QX-paSKrD8qFRlvA49B37IznHbZPJxOc547nDat2c6qaXY4zQ6n2eE0O5xmh9PscJodTrPDaXY4zQ6n2eE0O5z2vL_W8GXDaV8JcPwE2O3ep2T_Kju95G8xH1p-_2DNU6ZHvq-ZatWTi5EIktt0PiPTdljRHDqDSdh01S2yYUIsyqpzt4LQS5bM3tOUxmab1-j8WqoQSujZPGN97Dn-h-dutCua9OVlXfYTtv3BAaGRbm62lHzIotAkQeTi1nl94fwAS90xKtRuqXy7peLigQs7SNP0-fjaxVSNrovdCsOxMWvAIq0pjYHxoTLeLHWRZogu9sBIjLw92awckYdne2RIx126fzzOxUi6pmheooyVsrVO4BakTd7o2Xehp-Adhey3f9E8TBZFfpYnWZ6CHyojkQSeK8ry4HPuDUT6Cc-5t7biqbbi6UNKBu4-gtyDz_sx7N8EwR_xEBMoj_t5DElqkZc8yEOvTAM3EG4Q5akfiNij2n-chiUvM1cUqWBeyFiehYePtIvb97Jz3z33oj24fVbmPvjFzOL2LW7f4vYtbt_i9i1u3-L2fxe4fRGHgmUBxBYjPNPi9n_nuH3ZftaZECS_Mzaf6Ws8K0BOQTm7bdMgWwkjr6A4cJ0EKxgjcjjy-1eUA09xN_PcV3NyMX8kweSRAwup4ibVVTEM8IQh0BgDDASIqjRbyhE59ln-riBLR-Q-CGKX5xAtp35sBxR-mwMKnYQ7L41BOFzNeHRUAc0pziqYgiv1384UcAnUhcon0koAM_cg7CfDDZfN86YbnAPDDZeNnW6w0w12usFON9jpBjvdYKcb7HSDnW6w0w12usFON9jpBjvdYKcb7HSDnW6w0w12usFON9jpBjvdYKcb7HSDnW6w0w2_8nSDKNzA9YMsD8rg9z7dQIUWWQHSXXGIdsAfyfQaE-8ZuFkhnwh-odr_mKAa4AHCwWY68-7NH2XxUaVhWG3MsU5MeQesMvphavKgGnOJxxr9FakP-VgOutGA9jW43SvkGxs0jtmgTFTivsfHTIV1BEyvxJ7s4GlzHlSvOD807bHz6c7Mx4NP55MfVDQ47yo4TcfBf978NsZAJi3eK8RQ9b_Gnyr6dpMTT4P8A28LKVBtDtmFIIjgRC2MlE_A_jMkDXeyYKlcyprGFtBFguyO4i9KBNoXCq3IZDYOTqo68ocy3o-N1HGn2fq70whSuyUGj4T7OIAWw0388J7mAsZeLbzffvlMQMjdMIu4YGHMgpD5aSKYGxTBoZkAA79-fCbg2-Dnjww17AGbe5_3Y8m_CX4-8FlZsCxNmB-HIg1F6UfA7NLz3CxiecaSgvkRL2O_9MrI9d2UR9yPvDRPIjf3jxxpjp9PP7jJueedh-Ee_HzsxUUeJ9zi5y1-3uLnLX7e4uctft7i5y1-3uLnLX7e4uctft7i5y1-3uLnLX7e4uctft7i5y1-3uLnLX7e4uctft7i5y1-3uLnLX7e4uctft7i5y1-3uLnLX7e4uctft7i5y1-3uLnf-P4-TTKYh56qZuV6d8yfh5Sacwv5o_n3oefB_3pVCl7hqFHqb7EVZ0s0F7xr7sA3TGMe4BeIXyA4yfU7SeeXDZ-NBaDDFyBgAcNMkSB5LH0rwpgIy7YT85grRL2WC1JmyFTlpB7Yrfnun9nskGV9EnoPbryib-n9AQYXmN8DUpWocP8wz_7EZV6PP_UDbEgX-BJEAfYVljHIUFSYCGsc-vi4v-IVDFywyjBzqK_c76_uGz-sgzCUz_ebBaO-9PCjAsgiO9eG6MOgdn3zgrSsMQ79dwUVgatgHvIIg2hPp0iKrApJ9NPjRKTxVYwCuRI6ynAkXJ8OC2WXLAjovDZmCAdmDeo-h2nDIZY1W40Q6fqrioVbA-072nTB98fmDv4_sDEwfeHZg3eyykD58NvZszg0b828aL5Ap5GYPLES5_rzjgn4lSfGN75y9nZT-fOd87ft_n5baaXohLxP0gEU2ns6m02_9sLxZHHw086lCPBe_qeBxHtxg_oFSex37jiU2PNx3faP20x4fsOC9WoxY8bUdB6o7GQ9XUwdGtpz3BVprCZ2A2SOJIVBJXYByVLurrPOwwYIPigoiimfawUw_0ShBe7Xyt2W0FqeYjFj02CYF8CLf4swcTwTAaWutY5BZArUuTtK6iIsfxoPGUXcEnJMqXgWz1fsffODpL4mhNoeBZzzpijg64HbGE7l39g5uTtp0F3ICc54AjBkIEynX_nDmdXR13EKV1PYNEe5jx9-CQt8zAA4UsDN0uCgOUJT-PcLQ8Nn5jZhceHT6w5-Qbm5OmzRGZuRTL03FtMJlj8z_sHVL7JUI6XsSwr_NALiyDgqRtiTs5SoCHLcDqHefgHOvwy9oXvJrHrRRCtZ2GaxR4QGjzpcA_Gc7JzPz73vD3jOUHCWJGI3I7n2PEcO55jx3PseI4dz7HjOXY8x47n2PGcv9HxnDyASDrlOU9901abpGdK7l-UV5leUL-T4J5L1LSUGzRBRnC0LOIYzQwUvdCNml72hOfoTbM8Vj804BltslQL1Xhiux2mSZp92dxIvK_B3ChJ66awmwvVYTFQH61pC5BVCnTosS3YEwEhAg9AGB_ZaCdgBfrfDiRtWJpRCTwTdTem0q4BOL15uss1xSUSSwpag__RX5KdoOsGYbFXJBFXDNzQfV_119Le3GuImrTO2NcF8SDRFlhOhnO0GzTC1JzcIOAAI0Qp_SidNw0GWgLHaNCMgIHgBA_CSoZW3gnG7xoNBQE7rifAeXLEk2YMOAulwWekvWdKZVnvTGE_ZBLsoJkdNLODZnbQzA6a_e4GzRI_y8qgZFGUx7-LQbM_ynITQRukY6eW25KCBdyTXIe8z35nKI1KVTLAgT20up1BUEEfk22D-PUtBUfK665BaSRgAsRdigh1WfgSeUcLmR3hkBTjm9V03wcN9U3d5qqFoIbcto1sKFQUkKoHzEki1F82B6kC7su_1C1_v5QtCGqY4J8bR3gYkDCZCdBZhCzdkLmmXFW3Oe4lcGMxgbcp20Ir7XNO5Fyl4pvlB3pkX0PIBIlSi07nuFaaPwH1yBES0CDOoCbggTyBxNpJ-vK22fYL1XtSQkzEqA_GNHvJK1J1smbw2a5HlLirNSRZhmPyVPM4iv7yPAPZGu5aCZjDkGkDB7oVjs5U9CTJJLnSM4XqLqfX4HwAnYTTTJBTiC3cYAJPinG3nOAJlXBIORQ3HePI0nZHSOL9k5BjF2popwDcrzQJOc_4gYzEjkMeHYdM7TikHYe045B2HNKOQ9pxSDsOacch7TikHYe045B2HNKOQ9pxSDsOacchD_cPyjiMsizxiiSx45B2HPJ3NA75jxNU_VKNQjyci5QlX-kIZPF8QTXZWYGVRLZuBwMP0aXaXZzXpJqMkb5aBKNUiVAsqQOHy8lv4lWrkgbVYJl-wNykDEuaLZvB5sz0Ywqi7eSnnfy0k5928vN3OPn50-f_B1zjly8)
