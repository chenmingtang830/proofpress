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
until `propose → evaluate → judge → lawyer review → admit` completes.

[//]: # (ob:54ace136)
The implementation is a local Go sidecar, `tools/pageindex-sidecar`. Its
JSON request schema is `proofpress/pageindex-sidecar/v1`; it receives only
sources enumerated by the caller's corpus manifest, verifies every source
SHA-256 before indexing, and caches a tree under the source digest plus the
configuration digest. It has no hosted-retrieval fallback. PageIndex may use a
locally supplied OpenAI Platform credential to build or search its tree, but
the key is read only from the sidecar process environment and is not a
protocol field, receipt field, log field, or repository artifact.

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
makes no quality or cost claim for PageIndex.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzk2ZmI4ODgyNDBkYWQ5NjNiYzAzZGIwMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjFlMDk1NTc4IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kYTVlNzFkZDczMGY2MTA1ZGE5NzMyMmQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzE3ZDE3MjA1Yzk3ZjY3Njc3ZWQxYTE2NiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXXtz28p1_yo7un-0nZIU3iDkv5TavVXmNtfj62Q6E3nIxe5CRAQCDB6SFdsz_asfoNNPmE_Sc_YFgKIoWXKcNMVMJpFJYPfsef7OY5lPJ7Ru84yydpXzk7OT3W6VRFm6XC69wOGUJ5GfMsfnqeOdzE7Sit-teH4lmhaebTbUC6OzJPWypeMLh_s88JgXiySOlwEP_GXIPeZHsVgmgnI_zKLIyQKHukGauJ7nupTzNIJ1ed6w6kbUdydnn_Af7aqlV7BDQVvcagZ_pKKAD34n6jzLaVoIUoubvMmrkmzg-aq-I-kdeVtXVbarRdPAOzvKrumVwEONPq6rPwg4blfjgpu23TVnp6dXebvp0gWrtqdsI8ptXl61tLxa-s7p6O1a_LHL4e9V14h6xaqyESXwoq078WV2soFjwqKucJIwjJcn6pOVuJEPAXPFitNQxC7nse9kkeuEnCax73kcKavqFo-2KvJSAOVGIsXKjbkbe07IkjiL4iiOBXepG0XqOJq6FaO7pivgwB7SyaqaNydnv_90orf_dAJSruoG_1JfC75KgeW_P2EVFx9PPsAJjDbAxrxizWkt2joXN7SY7wpaNqdvz398c_Gb12_-Y_Xuzft3F29-d_7T6vz1-dv3b94ttniIr1En2sLiadeCFFcpbfIGlUoU2Yo2wN1WyPW6dlPVSPN1XuKSzV3Tii18U9ItClfRPoMXG1SHk7OyKwo4CduA_ITiQFpU7Bqe9SPmBs4ygcdBdK34iOd8C6y-KGERYg9LKKe7VtTkz__5PyTf7gqxBRZSeE0TAYorqduhFopb-OQH8vR18MAECaiR07OT9m6HJ0FdAb07-TLrKXaTKFpSJx1R_Ass0TWElpyA3cC7x-j6gRx4_MiOdBlGNObJs3d8DwZJ4D-UcNHkV6V8a-_wqEwkq2rSboRlUruhPWk7WtMRXZ4fM84C7wV02a3-oSFVWdyBoJodmHCe5kXe3iHRDJbKObgdYn0Srn6ErsBLXcbomK6Lcte1zSNysQ8dkUaYeUsRiq9dfXBWQhkTuxblIVco2zk8jw5DcAI23qFUSFN1NRMzeKg9claHJUHoZ8EzqIHns_yqq5X8t13TEuWEpAr0tqO99ukWzLogN-IINZETeKEbjjX1XVe2-VaQBhy1KNljtnHg8WPWGMYQs7zls3d0F0SGsDt5asV0CFwQ5Qi9onkJXFmrTxdaWDrcrheXZU9bASFvRFjihJ4XcjYmTDCR71qypbsdnuQRTtx7-ggjhAghfIv0uft9Hki86lpQIPJ5EL1RNeRSWS4KDl-9FqDJEJTh3HlPmYyWI7qWkR9w6vIRXW8-7oqc5S0pq3J-VdHiMcM8-MIRbvB0GXg-Yy_YdU5eV_AkMu96aA6UlOIWTHmby-hGVDgEZwX6YN85ohiB4JEbemOLPZcegYKuEsRXjfXEe176ETY9dZm37x6JODzOlmBa35zGOfkxB-yjbI1urcEpk5JRY-SWZqB3OwHOH-LVEZ5ylzk08sb0_mtVFNXtHCjCwN8p4tKqKzkFWHuckY-9e4R3qcN5mETs29AyDBu3eVGQFB33FjwvsOQWILJkJevqGmNGIT7mDJAh23TlNdl31B9mBnieQBRF5V2xWjL3RH9jIKJYuVnGReoJ4TIRhGHkUF9knu8gyqtauabGxkRjYwIonV3vqrxsJdSv5U4I_cy_EPl9QFANVng3WGEItAeLSAj_TAzeVFm7ykA0ot7VuYb6TeqepWEqYp75LuRAjh_5PsuY5ycuJECeH0Fsj9Iggg_ipfB913XizM9imkap8Dn1Y9SwBvRcQnYlrTM3BmyLn5x4jhfNneXci957zpnvn7n-PzvOmYNc0xxHZaV86QpQkC-DTz99X5wvlVUh8Q1tNqh6NA65GyVp6mTwgFxjAM61Hn9jTK33zrgfZEmWRn4szN4DmG32fipu1qsKDuDI8zPOErvqAErrVV-CjSEaSrtu8IvLspcYWC9H4GGjpmHDgly0uBsgqTwV4OMEYF4MGLCBSrFwP1z6suw5jeQVYKkcADEAEloUgs-MJ8E_gTRwGZmo0SvkQHBd8Y7hWosDaE3zJwqc2OF-5vgSPkn-DCC95c_zMToBLaOQ4F6WA4LGoGKLEKtfEdwJ8jnfbjvlXPY52cwugSU99GAEOHllSJHeo5kR5WIknN2CGLmOJUjSptsir034PsIf8CmJnyyZ47HA8GeQWvRaeSxr0GstY9d3w5Byl1Oz1iCRuM_rr84RaHNNAO3Wd-qYtLwszVKjiLog7zf7YTdvVBwHTrfIRhOYznDhWgjg-Q49PMBIo2sYnkCLa4jmnGR1tQXVsOvJXKKEiFJjuKpFh0SjXCmo-kbUR5i-jNM0TEQaZbFvGDXIcQaMem76Ih3uTJ6LpF1e8MuyEW0LAgPFkRwk-OgMTvsx33ZbyCIKwRCBNEJqcKM4fO9rZFEDIPCilQZRlRiKDUtSVEXIKdbWSSzUAUw2gWaLhGs9P8IiBjoI0SmhNEoMiwaJV6-XT8ukDONdl4vIh5jqp9YH98mVXvVF2ZK3IL9ChqMKFRUFJTUsVdK4FnfAxvROuVb13itgJVg1gZWAbbBLDXpaAvtykBshBAG4Vbu82dKWbWArf0F-EbRmCh7J1S1Y6k1FyhEE0tUlqWl53cu492go0WABuVhTFTdAB1ADbqZqAMRa4iup_HCqbVVbrkh1kDsA69D3qyABNIuP-C_r2f7YAaBSNiSZOtQngnwHCsIFebOFzAX3WfcFxtP7Ief0xl3bsLMDC7TryX3OJAVzkJIiftXsaLkmtxsDyvWZrC-QsVZ_aFA6HJLe0LxAD_3KLIjkDleToQI_nBfgCQqMSQAxZfqA8eze-3hS_b5yFZpPVZaBfaJ59EalOQqH0vyJUN4lH1oQ_F1X3dVmyK-e6RDhAVeuX0HwHUQvbaWSJHRbMgRdl9UtBFwQBtpTIfcAnN2gyxjCeRtd5n1yuKPtRq7WdODPBW8WB7IYbYHuMklcb-k5aeQaCxxUEQZ2_ZS6gF40CIWfAkj2_aX1p4NSgV70Jck_U1GXfL4sP5P5fE5G_40fjtzE54ccBHzzy7-dz70wIuCvIDnXMkKjVAtYnVSraqUswVmTi9e4sIYbC6PbOcdVMdsX2x28h2yyoESt0uuUWQ9AWA7u5U9KqAdWvU-vYQ_qglDr1spfaCuusfA9XEsZSwuQfU1Ote2A_uKiu6rJWwirGGkhwJol0DLU0tYvoMeBvEo-NFf7CJSXxa37GxrK4T1lbk86Sq8avdM0ERO36COa_F4eaC-2fdas73HdwBvITQxWqcFb0UaM19VfypV1AH9szUMlKW0STuCweMl9znybFwyqVL2dPbXopNdNQua7gkd-FDCz7qAOpdd9UVmpxXRdgzIiYx2kAdtUcKQFU6Jaqg1RWEcKQbk72rs-dEeQEYsrXBwfhu8YAD6IEwQcCvAQOD7Ys8kLUCjw5RnF8gOgKRWr-uBtDAriIOhoV8rWYGEiznAt2FcmAkAQIDHsfRHwuzRFiQMZgHTQ34OHxQihNeLtuyM-k3NI6CPBWOJwi9H7Alsvy5dWxsx-gZcFNBRLX_Q5ZV8sszJ-fpULlUEGFgj3jYEMapFRaAZXXDcawCiTVas3kt_nRDXb-ND5Wriv8BOCG1U9QoTFlVJJ2miJwpK4nQAVSEFVWMdpdtjHxTrrRNAziMFU4h7yg5_YJFg7dkW9ynUJyB5SG0VPb_krk_WtCb8fcjQd0mKAYyZFwZiI6L0AEW97fy8NQ2EtSZU-JSQoMt0B7UUy2lG62-OMPc-aAXoBsykAB3JJxhsDCHQJTp7t5_c_ve0hB2KBRjIhL8G3grXcVvU12IsW1RE19xi4LObFfpraVH1Q8-zV_Bl1S-O9vFA4SRY4XmCz3UEp80CG-rXlSLRyrOEpZJhDgqoAJ-Y3rejLSXOzweAI4ASIrNTY1DeX4AG-A690d1miN20QzCF00I6NVaDsrKD5Vlq79bX3cqsPX5ARB5ryguftfkteNvhRz-99friFryYUwO7sFzio8H-ktQ8sk-XcZ3T2w4Ay4frRi7rDe95Z1unQngvyYwWRiQtGwbDXbVUVzSk6AOk_582RHiVjvu_6srrQ0_Uj1qxKLK3kDVp1BylOBpb0SJvgyGtHJwio69GYv5iCYWajXxNrU82RopuDdkh3iNXDuUrJ6uoK3jjW13cyGogoeTF9qkyz3aK4s7wGaxx5cbRchWKErixKy5vLit4R-kQs_DDNli-m72e5J0KWrZBouqwwU9VFIIpO6qa6FnsFJaV2R-j7Rt0zAHEY5fl-WACPIp3a2NwGle377-uWDVqfjrHKiLQFqagPLhw9KnzMuqateF8HXIwHIHrD3uOs3ua1yMDNq32utFjmA7Hoaq94YP2BgR5e_5edYHiyZh8USFevYIlJyOUWCAJU82jxkCE-sJMOTo3WjL7lYaO6xMLmlETLW5Vg-xrzA9Z1eNN3alBMso9XWCCfl6IDIKLiWqa-6Nl5_vZi8VCH-UFVOOewA6KYuQIxkmLMcwYZSK-xsqSv2PdhoNSfTm43d5bisTZr4FXcMxylbZZj2h01AJiHOmKxIoKKqmsVnkWAdShFwlbak1ub1FlmfpbFNBbU9x2axixKWJJY5gx7lsN-3bCP-WmKeVPMm2Led4x5Tx9Q2G_Qh7N-3TP3y-Fe_GODCd9k-iAIfI8nNGUZY6kPJhEvIyehCeVR4Mdp4CQR5FwedZNlGEQuz3xOIx_QvEcz7nL_KYcbTyLE7x3nLAzP_EOTCL4nkiyj2TSJME0iTJMIf7uTCLEPfiJxEgYex04P9FBjwJ_nYgf1zRqVorksf_3Lz78humoB6r0B3uBSw8bjvXex7_iK5K1iz42Obpelqj82RJTdVqqZ7vBi2RG0B0UJ4HEHtgTcyDPYcYZNeoXvhZSfWuKyND2KVGSVbAOrUulMFy1lSNW1cQT99bBHrUufu6LTJjIeH1BfS5sAnmMdaVNhxWbeuxYsf2P1ezFwPBgvsUhKL0vJZVDJpoPgAM6Y_LwT5fkFeVvQFguRw_yqrdTkAVpLo9rUstiLoxbwTasqY9dCajRam9L2vkWsgTTIg8muZnmT11Up62LSaTTKkqW2txWrCtW5m40beTNQjSvzp-wlyd4T3twxHnwaj5nGY6bxmGk8ZhqPmcZj_srjMZyHkCCx0I2YZyxwUNfo7frrChQmmiVumiaJ7zGX9sDf1iz06i8pPuxVuMCtdjU8LCTo6MNZBsY4l4DBhCummpc71exS6YaqodV0twHtA75BCJIaoQcW7iGqcSkUW8sS6plhnxxkOrSbA1VbNJyZ8hK2Zbc2z610zr8GOtY6U4an1waDC7xxq1QLP76iuwb_V-Z-guOfVMUO_FMqU71CIa3lubhG0acqJNhG98MxQGTg75ep64SJDZODCs8oTD6vVIOaj3rcgpUBmJT1-BmqATprimHUvqSfmhH7Yi0KaRON5KeNbLpLeFlKSTUKioA8ukLakipvm9sWIOvKNMytuQGDGCBcjOCIb7SZKfHfy19AA0pLUinyqw3sW6sYYtvdgmscD3Gn2lEg8d78ASX6CjYnSoqvkKgcXCu2GxCINWMCKGo_AlRjQvyIKNMg9cAs05S5oR1g64thWpQvqWrVij9KWCpKKwCuEpQ5euYcDceYE4Y7DIrw0V6cwMGqgaM3nAZZ2MA3L-lNfqVc4gb2LURfFsMNZYkbPYkU_52UhhmoAeMCtq2M1a1nOm1FM8azHDJIQMMyGbitc7BYZVtE1tIabVx2EAKduwLUWolkE12WuQdVd1OQHyqeTDRQH8mf_-u_bTlA_uMPHYYG_Es5f42N0fPrln4_FtLs9TsgGv8krsDnYUQsexeoLAG2zPICkGhftei2OxWey0FNCLP-3o8dUbVpAHMawJwGMKcBzGkA8293ADNOBM-EEwuHRtMA5jSAaQcwz03Ss1ftGDGbDln9Ci1IV1LtSIrhBg684fNaegZgIXV9VlVJFVmbyjD-AhE_QzNtMM2B00odwuVoaejoQ_n-CV736aqyEC62QFMrUy2Zepyq3A9QD3BHMtnkdDqTmlsYLyWqfldJ6rdNDVX2N1MAuW8PKZdhq-mQ9oP_AzAGssal9goDsx6CQbSkhTxs38mYBmKngdi_04FYmcT0A7EgxrK6Lf-SP3ZVyAwILLE9NibxDX436v6iL_3FpyesyCGTdwQLRyv-OxxWqrt2FE2XGjdYDifGHplUeuoyslkC36i28HGeLv0oiuMk_eb0vrcFB1mvUPUo1SUcVua2civrt-cQWWlxhL-huwR0Jmua35hebBNwrBmofElXeG2xeD6OELKOYVzbEXqfOSf2BE175gTVU3Q4SxMnC-g3nW0DJwSRGn9uca3a-DYuAD_b4ajkFXy4OPRjLwemhAfm9vjsbgaejGyfakQz2TmaY_54Q0sTZ4aW9cC878CkHhxX_e2uR8uDo2PzUrTjYVE7rDozlVjEJxLpCkw02vpOlVGaxUOW8iAZr3WwbYDpO5LCYwqFjdFXLfPVnky9-0aNLOywYICNeiNg5IyU4UNKdVhScoLXwjpe383rTtkgiAibYY2AUAX4rbElOwvpRrPJhyZ6L0xSRn4InEEIOqgJGg3ODRgdetZ9Lgw5sK_IBzny9LneI7_jeXCu106_PT7XOwXuKXBPgXsK3N8pcD_9wsL-NHAwnAYOvxwe9v0uo87U88EFQ8bF_cSNqBNmIU3ACGOPO75I44DFLg1SFkCOLbIgzUQkqMOWnpcEWRDRpxzu3qhzdOYEZ2F8YNTZ_gD039Socxa4nDE3ckU_Q_ecUedRgAZocugmzV9h7tlx_ET4mWBiGTw-93ygGGyBnSkW94xAAGZYoDrol6Vkw1yzoZ9L2eU7WWd58cjzQ5PNslGv_02wT6EM3zRj5bCp7Bedv73AoUEJrLHuTsBtbO3wm6k2yuHaU9sOszDrsjyAsFW_3sZBfZPLDB3YKZ_RmAAW3nTzV5aeOvizuZWtroLe3uF4ZXON86j5FXaLDa6zE9XHRpXTEFCYI0DE0fcc5QbJ8kqouVfsYgAo3uGrUlD5FpKOAwnJDFlPuwZUp5MVbEDNbUUUwlSFO8Vi9OY1kXOa8L1qacOzt1UHUR4rfnnNuoLWC1Ccl82Uj8vsl-VfbKZcJHSZhbEfOI4daBxgut7ivyUYM9VbytzMd2lCnb4B2OOz4XjOM4FVdSUH_VBpwHoLLIeqor02MT1co5_Vk7GgiaDxOU4Y_PbdxelW8JzKHuepbs6eYhMH3Ux5BQa01xEZGe24W9HIVLRs5FgXcA0vaIy6GbpzNMORGdQLs8zFaz1Nq9sQ_eyI8WV0cNljIBo0qTNUUaXLshBshpQYreWsqKrxqx7nzFoPqFwpo8jelVZFh7UxNU4ibxLLkZIFOS_NpP5c9rrQQu2p53p0S0-TDHsy2ELZYwfu1Dtg2bI5oslJALrseVSkoXU5A_RstOkFsBd07yO22Vo9wvxeHhtDbgFKxe5YoX_9FtsUKBV7CQC8xWhPOd5P6i6tczYDHuN4tfK9RtB5gTprOn2SDOA3sFcTYdope-qmVQAn0cHzSL1v1XgbBNS213RNmZ0oUX3YrK7-JEozxyUrHK_2YiDKp77Rg-ojELsDY_oX66u1x9SDSV1p5jDAxcrx0PUTJoV0ENKjQviJjGdre5xmuiwzXZaZLstMl2WmyzLTZZnpssx0WWa6LPM9L8swwZwodpyQh2K6LPOiyzKmWSkvvvQXZ2zn8mtu0cByD12jOXyDRud0trpiG6RgBa9FRruiVYxQvpID1zfEmxEvsMkkLhCRnsL-dsl0O-f_w-2cOMiWie8ngSum2zl_Z7dz3iA-uW_a0gGakV31I290pweNVcUYC-TAoV8pxzTUXmUXSppaYS9eN-qke3raSEW909i_EPR6oLIzhUAaNWWrVffY1R4f_89NHZF6gc2ZBt2_AxHra9t4F5gyjMa6MdHB8RSbSJ7aQWhb1tRFSf2De7PRmK9y2TOtFZclenJQmA7DFuwhfTn82Sq2KDNR4cok_bS80zcRZDkdlVTqLf5wifLu6udm9OzIuKBM_nEtdhuBdYhihQJbz-6NAYNvHRd-ZsRSNZoNFg1sL5f9pwWR7sCG3_V8rgZW1peljJjSUZjpeTy0StO5gD0hC2B3MtmXbkNS0VOFBqFq95iy9rWnHpXJogv8S2uV9P5oVNJ52_EYjC17l9Muy_u308hzL6cNa7ajatp0OW26nDZdTpsup02X06bLadPltOly2nQ5bbqcNl1Ou3857cOX_wVKwnFx)
