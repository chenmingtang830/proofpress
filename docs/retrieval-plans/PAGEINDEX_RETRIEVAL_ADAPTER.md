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
makes no quality or cost claim for PageIndex. The first private panel remained
inconclusive because its frozen gap locators were outside the PDF-only custody
subset and its PageIndex builds did not produce a valid scored denominator;
that result does not change the implementation or admission boundary here.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzk2ZmI4ODgyNDBkYWQ5NjNiYzAzZGIwMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImFmYjIzYmM5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85NTUyOWI3OWI4YmI4ZjVlNzMxMGVmZjkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzE3ZDE3MjA1Yzk3ZjY3Njc3ZWQxYTE2NiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXetu5EZ2fpWC_CMJ0i3xzqbm1-zOxFGwWQ_Gs4sAK0MqsopqrthkLy_SaMcD5FceIMgT7pPknFMXkq1WSyONvY5DwLBb3eyqU6fO_Xyn_emIN12R86y7KMTR6dF2e5FEebparbzAEVwkkZ9mji9SxztaHKW1uLsQxZVsO3i2XXMvjE5jx1sFq0AE3irN_Dxx_SBdpWkYCDfLEo_7Po-l8LzEjZ08cz0_T_MslXEa-VHqhStYVxRtVt_I5u7o9BP-0V10_Ap2KHmHWy3gRSpLeOOPsinygqelZI28Kdqirtganq-bO5besXdNXefbRrYtfGfLs2t-JfFQk7eb-s8Sjts3uOC667bt6cnJVdGt-_Q4qzcn2VpWm6K66nh1tfKdk8m3G_mXvoDXF30rm4usrlpZAS-6ppefF0dryZGJPE89YFtypN65kDf0EDBXXiRh6CVpnCCLVnkoY991ZJ7js9u66fBoF2VRSaDc3Eh54cbCjT0nzJI4j-IoBn663I0idRxN3UXGt21fwoE9pDOrG9Eenf7p05He_tMR3HLdtPhKfSzFRQos_9NRVgv58egHOIGRBthY1Fl70siuKeQNL5fbklftybvX3749-_2bt_9x8f7th_dnb__4-ncXr9-8fvfh7fvjjThafJE48Q4WT_sObvEi5W3RolDJMr_gLXC3k7Re363rBmm-Lipcsr1rO7mBTyq-wctVtC_giy2Kw9Fp1ZclnCRbw_1JxYG0rLNreNaPMjdwVshsuLpOfsRzvgNWn1WwCLOHZVzwbScb9rf__B9WbLal3AALOXxNE8GFIOq2KIXyFt75hj19HTwwQwIa5PTiqLvb4klQVkDujj4vBordJIpW3EknFH8PS_Qt45VgoDfw3UN0fcP2PH5gR74KIx6L5Nk7fgCFZPAPZ0K2xVVF39o5PAoTy-uGdWtpmdSt-UDaljd8Qpfnx5nIAu8FdNmt_qFldVXewUW1W1DhIi3KortDojNYqhBgdpi1Sbj6AboCLwU7x6d0nVXbvmsfuRf70IHbCHNvJUP5pauPzsp4lslth_dBK1TdEp5HgyEFAx3v8VZYW_dNJhfwUHfgrE6WBKGfB8-gBp7Pi6u-Ufe_6duOKSNEIjDojrbaJxtQ65LdyAPURE7ghW44ldT3fdUVG8laMNSyyh7TjT2PH9LGMHa58FbP3tE9ZuTC7ujUiunguMDLMX7Fiwq4cqnePdaXpd3t5fF5NdBWgsubEJY4oeeFIpsSJjNZbDu24dstnuQRTtx7-gAjpAw915Xpc_f7cXTjdd-BALEfR94bRYOWygtZCvjojQRJBqcM5y4GyshbTuhaRX4guCsmdL39uC2LrOhYVVfLq5qXjynm3i8c4IZIV4HnZ9kLdl2yNzU8icy7HqsDZ5W8BVXeFOTdmHKHYKxAHux3DghGIEXkht5UY1-TReAgqwzjq9Za4h0r_QibnrrMu_ePeBwR5ytQra9O45J9W0Dso3SNb6zCKZUirzExSwuQu60E4w_-6gBPIa51eORN6f2Xuizr2yVQhI6_V8SldV8JDmHtYUY-9t0DvEsdIcIkyr4OLWO3cVuUJUvRcG_A8gJLbiFEJlZmfdOgzyjlxyKDyDBb99U12zXUPyxM4HkEXhSF9yJriLlH-hMTIsoLN8-FTD0p3UwGYRg53Je55zsY5dUdraljY6ZjYwZRena9rYuqo1C_oZ0w9DN_YeT3AwbVoIV3oxXGgfZoEQrhnxmDt3XeXeRwNbLZNoUO9dvUPU1DyHNE7rtRLB0_8v0szzw_cd0AEoQIfHuUBhG8Ea-k77uuE-d-HvM0SqUvuB-jhLUg5xSyq9s6dWOIbfGdI8_xoqWzWnrRB8859f1T1_9nxzl1kGua4yisXKxcCQLyefTup583zidhVZH4mrdrFD0eh8KNkjR1cniA1hgF51qOv3JMrffOhR_kSQ7pZyzN3qMw2-z91LhZryoFBEeQ24ossauOQmm96ktiY_CGpNctfnBeDTcG2isw8LBe07DhmJ11uBtEUkUqwcZJiHnRYcAGKsXC_XDp82rgNJJXgqYKCIghIOFlKcXCWBJ8CaSBychlg1ahAIKbWvQZrnW8J1rT_IkCJ3aEnzs-hU_En1FIb_nz_BidgZRxSHDPqxFB06BigyHWsCKYE-Rzsdn0yrjscrJdnANLhtAjY8DJK0MKWY92wZSJoXB2A9cotC9Bktb9Bnlt3PcB_oBNSfxklTleFhj-jFKLQSoPZQ16rVXs-m4YcuEKbtYaJRL3ef3FOQJvrxlEu82dOiavziuz1MSjHrMP6123W7TKjwOnO2SjcUynuHAjJfB8ixYewkgja-ieQIob8OaC5U29AdGw61EuUYFHadBdNbJHovFeOYj6WjYHmL6K0zRMZBrlsW8YNcpxRox6bvpCBndB52JpX5TivGpl18GFgeAQBxk-uoDTfiw2_QayiFJmGIG0kiS4VRy-9zGyqIUg8KwjhagrdMWGJSmKIuQUl9ZIHKsDmGwC1RYJ13J-gEUZyCB4p4TzKDEsGiVeg1w-LZMyjHddISMffKqfWhs8JFd61RdlS94x-w0yHEWorDkIqWGpuo1reQdsTO-UaVXfewWsBK1msBKwDXZpQE4rYF8B98YYwwDcil3RbniXrWEr_5h9L3mTqfCIVrfB0qAqdI9wIX1TsYZX18MdDxYNbzQ4hlysrcsboAOoATNTtxDEWuJrEn441aZuLFdIHGgHYB3afuUkgGb5Ef-ylu0vPQRUSoeIqWN5Ysh3oCA8Zm83kLngPpdDgfHkvss5uXEvrdvZggba9WifU6JgCbekiL9ot7y6ZLdrE5TrM1lbQL5Wv2midDgkv-FFiRb6lVkQyR2vRq4C31yWYAlK9EkQYlL6gP7s3vfxpPr7ylRoPtV5DvqJ6jEoleYoHErzJ8L7rsRYg-B1U_dX6zG_BqaDh4e48vIVON-R99JaSiSh2SIXdF3Vt-Bw4TJQn0raA-LsFk3GOJy33mU5JIdb3q1ptbYHey5Fe7wni9Ea6K6SxPVWnpNGrtHAURVhpNdPqQvoRYNQ-ikEyb6_svZ0VCrQi74k-c-U12U_nlc_suVyySb_xjcnZuLHhwwEfPL9v75eemHEwF5Bcq7vCJVSLWBlUq2qhbICY83O3uDCOtw4NrJdCFwVs3252cL3kE02KFGrDDJl1oMgrADz8ld1qXtWvU-vYQ_KglTrNspeaC1usPA9XkspSwch-yU70boD8ouLbuu26MCtoqcFB2uWQM1QS1u7gBYH8ip6aKn2kXhfNm7d3dBQDt9T6vakowyiMRhN4zFxi8Gj0ed0oB3f9qNm_RDXjawBbWJilQasFW_ldF39Ia2sHfhja-4rSWmVcAIni1fCF5lv84JRlWrQs6cWnfS6SZj5rhSRHwWZWXdUh9Lrvqis1GG6roMyRr4O0oBNKgXSgilRQ2LDVKxDl6DMHR9MH5ojyIjlFS6OD8NnGQR84CcYGBTgIXB8tGdblCBQYMtzjuUHiKaUrxqct1Eo8IMgo31FrcHSeJzxWrAvJQJAEERi2PtiYHd5ijcOZECkg_YeLCx6CC0R794fsJlCQEIfySxLHGFj9KHANtzlSytjZr_AywMeypUvh5xyKJbZO35-lQuFgRwLuPvWhAxqkYlrBlPctDqAUSqrVm-J36-ZaraJsfG14b6KnzC4UdUjjLCEEiqijVd4WRS3M6ACKahLazjNDrtxsc46MegZ-WBOcQ_7xk9sEqwNu6Je5boM7h5SG0XPoPkXJuu7ZOK-y9F0kMYAx0yKgj4Ro_cSrngz2HtSDBVrEVX6lJCgULoD0otkdJN0d4gzdixrDtELqE0JcaAgMt6agECX4Ohs33343bsh5MBYoCUmFBXYVtCW27q5Bn3RV3VAzL0MTFbmxX6a2lR9VPMcxPwZdUtjvbxQOkkeOF5gs91RKXNPhvql5UjUcqzhqciwgARVBZyY33RyKCctzQajI4ARYFSpsalvQcEDfAZW6e68QmvaYjCHoYM2bFkNwp6VvNiQtltbey-3-uEzMmJPU16KotttyVODH-X83vv7W_gKoQB6Zz9AoML_kdY-sIzKuc_o7IcBz6TrRy_qDu9YZ6rToT6X7NsaPJOQGQfFvuzqumxP0ACQ_Vy2B3qUWeb7rk_VhYGub7FmVWFppWhRq3tIcXLQpEfaBAe-dhBBwF2Px-LFFIwzG_01eWmqOXR1S5AOModYPVyqlKypr-Abh_r6Ts4DGSUvpk-VaTYbvO68aEAbJ1YcNVdFMVJXFknzllTRO0CfjKUfpvnqxfR9R3tiyLKRFE1XNWaqugjE0Ujd1Ndyp6CkxO4AfV-pewZBHHp5sesWwKKQUZuq26iyff_7umWD2qd9rFIirUHK64MJR4sKb2d929ViqAMeTwEQg2LvcFZv80bmYObVPlf6Wpaja9HVXvnA-iMF3b_-91uZ4cna3aCATL0KS0xCTltgEKCaR8cPKeIDO2nn1GrJGFoe1qtTLGxOyfR9qxLsUGN-QLv2b_peAcWIfaLGAvmykj0EIsqv5eqDgZ2v350dP9RhflAUXgvYAaOYpQpiiGLMc0YZyCCxVNJX7PthJNSfjm7Xd5biqTTrwKu8pzhK2izHtDlqIWAey4iNFTGoqPtOxbMYYO1LkbCV9uTWJndWuZ_nMY8l932Hp3EWJVmSWOaMe5bjft24j_lp9nmzz5t93s_o854OUNht0IeLYd1T9_P-XvxjwISvgj4IAt8TCU-zPMtSH1QiXkVOwhMuosCP08BJIsi5PO4mqzCIXJH7gkc-RPMez4Ur_KccbopEiD84zmkYnvr7kAi-J5M85_mMRJiRCDMS4ZeLRIh9sBOJk2RgcSx6YAg1Rvx5buygPrlEoWjPq3_7_rvfM121APFeA29wqXHj8d53se_4ihWdYs-N9m7nlao_tkxW_YbETHd4sewI0oNXCcHjFnQJuFHksOMCm_Qqvpd0f2qJ88r0KFKZ19QGVqXShS5akkvVtXEM-ptxj1qXPrdlr1VkCh9QH5NOAM-xjrSusWKzHEwLlr-x-n08MjzoL7FIys8r4jKIZNuDcwBjzL7byur1GXtX8g4LkeP8qqsV8gC1pVVtair2ItQCPulUZexakkSjtilpH1rEOpCG-8ioq1ndFE1dUV2MjEarNJmkvauzulSdu8W0kbcA0bgyL6mXRL0nnNwxFnyGx8zwmBkeM8NjZnjMDI_5O8NjhAghQcpCN8o8o4Gjusag119WoDDeLHHTNEl8L3P5EPjbmoVe_SXFh50KF5jVvoGHJQUdgzvLQRmXFDAYd5Wp5uVWNbtUuqFqaA3frkH6gG_ggkgiNGDhXkQ1LYVia5lCPQP2KeBOx3qzp2qLirNQVsK27C7Ncxc6578EOi51pgxPX5oYXOLErRItfPuKb1v8L-V-UuBLrnwHviRhai7wki7pXEJH0SfKJdhG98M-QOZg71ep64SJdZOjCs_ETT6vVIOSj3LcgZZBMEn1-AWKARprjm7Ufkk_tWD2i40sSSda4qf1bLpLeF7RTbUqFIH76EvSJVXeNtMWcNe1aZhbdQMGZRDhogfH-Earmbr-e_kLSEBlSapkcbWGfRvlQ2y7Wwodx4PfqbccSLyHP-BMj2ALpm7xFRJVgGnFdgMGYu2UAI7SjwGqUSFx4CrTIPVALdM0c0MLYBuKYfoqX1LVahR_1GUpL60CcJWgLNEyF6g4Rp3Q3aFThLd2_AQCq0aG3nAa7sI6vmXFb4orZRLXsG8ph7IYbkglbrQkdP13dBsGUAPKBWy7MFp3udBpK6oxnmWfQkI0TMnAbVOAxirdYlRLa7VyWSAEGncVUGshoiY6lblHVXdTkB8LHiUaKI_sb__137YcQH_8uUfXgK-U8dexMVp-3dIfYCHtTr8DvPHv5BXYPPSI1WAClSbAlnlRQiQ6VC36zVa552pUE8Ksf7BjB0RtBmDOAMwZgDkDMGcA5i8XgBknUuTSiaXDoxmAOQMwLQDztUl6dqodE2bzMatfoQbpSqqFpBhuIOANn9e3ZwIspG7IqmoSkUtTGcZfIBKnqKYtpjlwWpIhXI5Xho7Ble-e4M2QrioNEXIDNHWUalHqcaJyP4h6gDvEZJPT6UxqacN4ulH1u0ok3zY1VNnfQgXIQ3tImQxbTYe0H-wfBGNw17jUTmFgMYRg4C15SYcdOhkzIHYGxP5KAbGUxAyAWLjGqr6tfsofuyopAwJN7A7BJL7C70bdX_Slv_j0hBUFZPKOzMLJiv8OhyVx14ai7VNjBqsxYuwRpNJTl6FmCXyi2sKHebryoyiOk_Sr0_vBFhyoXqHqUapLOK7MbWgra7eX4Fl5eYC_obuC6Ixqml-ZXmwTCKwZqHxJV3htsXg59RBUxzCm7QC9z8SJPUHSnomgeooM52ni5AH_qtg2MELgqfHnFi9VG9_6BeBnN4ZKXsGbx_t-7GUPSnikbo9jd3OwZGzzVCVaUOdoifnjDa-Mnxlr1gN435FKPQhX_cN2iJZHR8fmpeymYFELVl2YSizGJxTpSkw0uuZOlVHa44c05UEy3mhn2wLTtyyFx1QUNo2-GspXBzL17msFWdhiwQAb9eaCkTN0hw8J1f6bIgSvDetEc7dseqWDcEXYDGsluCqI31pbsrMh3QSbvA_Re2aSMvZN4Ixc0F5J0NHg0gSjY8u6y4UxB3YFeS9Hno7rFTyUsStE7Dt55Dqh4Ense554CNdr0W-P43pnxz077tlxz477Z3LcTx9Y2EUDB2M0cPh5P9j3Z4E6c88HEwwZl_ATN-JOmIc8ASWMPeH4Mo2DLHZ5kGYB5NgyD9JcRpI72crzkiAPIv6Uw92DOkenTnAaxnugzi7k8mEYr35ZUOc8cEWWuZErBwzdc6DOEwcNocm-SZq_A-7ZcfxE-rnM5Cp4HPe8pxhsAztTLB4YgQGYYYHqoJ9XxIalZsOAS9kWW6qzvBjy_BCymRr1-m-GfQql-KYZS2BT6he9fneGoEEKrLHuzsBsbCz4zVQbCVx7YtthNsw6r_ZE2Kpfb_2gnuQyoAOL8pnABLDwppu_VHrq4WV7S62ukt_eIbyyvUY8anGF3WIT11lE9SGochpCFOZIuOLo54Ryw82KWircK3YxICje4lfpoooNJB17EpIFsp73LYhOTxVsiJq7mqkIUxXuFIvRmjeMcJrwuWppw7O3dQ9eHit-RZP1JW-OQXBehimfltnPq58MUy4TvsrD2A8cxwIaRzHdoPFfMxgz1Vueubnv8oQ7QwNwiM_G8JxnBlb1FQH9UGhAe0ssh6qivVYxDa7Rz2pkLEgiSHyBCIM_vD872UhRcOpxnujm7Ak2cdDMVFegQDsdkYnSTrsVLaWiVUuwLuAaDmhMuhm6c7RAyAzKhVnm7I1G0-o2xIAdMbaMj4Y9RleDKnWKIqpkmQrBBqSU8YawoqrGr3qcC6s9IHIVeZGdkVZFh9UxBSehSWKClByz15VB6i-p14Uaak-91NAtjSYZ92SwhbLDDtxpMMDUsjkgyUkAsux5XKahNTmj6NlI0wvCXpC9j9hm6zSE-QMdG11uCUKV3WWl_vVbbFPgrdghALAWkz0J3s-aPm2KbAE8Rni1sr3moosSZdZ0-ogM4DewVxNh2ik74qZFAJHoYHlI7jsFbwOH2g2SrimziBLVh82b-q-yMjguqnC82vGBeD_NjQaqT4LYLSjTb62t1hZTA5P6yuAwwMQSPPTyCUgh7YQ0VAjfIX92aY_TzsMy87DMPCwzD8vMwzLzsMw8LDMPy8zDMj_nsEwmMyeKHScUoZyHZV40LGOalTT4MgzO2M7ll0zRwHIPjdHsn6DROZ2trtgGKWjBG5nzvuwUI5StFMD1NfMWzAtsMokLRGygcJgumadz_j9M58RBvkp8PwlcOU_n_Mqmc95ifHJftckAGsiu-pE3vtVAY1UxxgI5cOg3yjCNpVfphbpNLbBnb1p10h05bUlQ73TsX0p-PRLZhYpAWoWy1aJ7aLTH9zzXdWTqBTZnGnX_9nisL23jnWHKMIF1Y6KD8BSbSJ5YILQta-qipP7BvcUE5qtM9kJLxXmFlhwEpke3BXuQLYeXnWKLUhPlrkzSz6s7PYlA5XQUUpJb_OESZd3Vz81o7Mi0oMz-8VJu1xLrEOUFXtjl4h4MGGzrtPCzYJaqCTZYtrA9LftPx4zMgXW_l8ulAqxcnlfkMclQGPQ8Hlql6ULCnpAFZHeU7JPZICoGqlAhVO0eU9ah9jREZVR0gb-0VJH1R6Ui423hMehbdobTzqv702nsucNp45rtpJo2D6fNw2nzcNo8nDYPp83DafNw2jycNg-nzcNp83DaPJz2vP9bw5cNp30lwPETYLd7fyX7J9npJf8v5oeW3z9Y85Tpkd-WXLfqycUoBMnNajojUzdY0ewai0nYNsUNsmFELMoqu11D6KVKZu9pSmPbpyU6v5oqhAp6Ns1YH_sd_4fnbowrGvXlVV32I7b9wQGhka6ueko-VFFolCAKecNen7FvYalbToXansq3PRUXH7iwB2ka_z6-cTFFZepiN9JybMgasEhrS2NgfKiMN0ldlBmii31gJEbdnmpWDsjDkz0yZOIu0z8e5mIUXWM0L1HGc9VaJ3AL0qZu9OSbwNXwjkz1279oHiYJQy9J4yRdgR_KQxn7riPz_MHfubcQ6Sf8zv1sK55qK54-pGTh7gPI3f-8H8P-syD4QxFgAuUKL40gSc3SXPhp4OYr3_Gl44fpyvNl5FLtP1oFucgTR2Yryd2A8zQJHj7SLm7fTU4959QN9-D2eZ564BeTGbc_4_Zn3P6M259x-zNuf8bt_ypw-zIKJE98iC0GeOaM2_-V4_ZV-9lkQpD8Tth8Yq7xJAM5BeVs-qpCthJGXkNx4DoJVjBE5HDk968oBx7jbqa5r-HkYvqTBKOfHFgoFbepro5hgCccgcYYYCBAVKfZSo7IsU_ydw1ZOiD3vh85IoVoeeVF84DCL3NAoVFw56U1CA9XMx4dVUBzirMKtuBK_bcTDVwCdaHyibISwMw9CPvRcMN59bzpBvbAcMN5NU83zNMN83TDPN0wTzfM0w3zdMM83TBPN8zTDfN0wzzdME83zNMN83TDPN0wTzfM0w3zdMM83TBPN8zTDfN0wzzdME83zNMNP_F0g8wc3_H8JPVz_9c-3UCFFlUBMl1xiHbAH6n0GhPvCbhZI58IfqHb_5igWuABwsEmOvPuzb-o4qNOw7DamGKdmPIOWGXww9TkQTUWCo81-CtSH_KxAnSjAu2rcLtXyDfeGRyzRZnoxH2PjxkL6wCYXss92cEPn-Gf_wU6owb2)
