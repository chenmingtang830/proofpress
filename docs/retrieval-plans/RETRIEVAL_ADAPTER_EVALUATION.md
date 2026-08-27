[//]: # (ob:2f7aae98)
# Private legal knowledge-pipeline evaluation — preregistered plan

[//]: # (ob:be917805)
## Decision this evaluation supports

[//]: # (ob:af2a9640)
This private evaluation tests whether PageIndex is useful at the *gap retrieval*
stage of Proofpress's legal-matter knowledge pipeline. It is not a standalone
leaderboard and does not decide whether a model answer is correct, whether a
conclusion is admissible, or whether any adapter should bypass human review.
The pipeline under test is full data-room evidence substrate → task
decomposition → candidate claims → evaluate/judge/lawyer admission → claim
graph → bounded disclosure → gap retrieval → executor → post-disclosure
assimilation.

[//]: # (ob:4ed25ae8)
The panel is an internal operating decision. A positive result may justify a
later public/reproducible panel, but is not public proof that PageIndex is a
generally supported adapter.

[//]: # (ob:ffd6fd55)
## Frozen legal pipeline roles

[//]: # (ob:cb6e0e88)
All inference is routed through the Proofpress dev AI Gateway with a fixed
provider and no fallback. Decomposition and candidate proposal/repair use
`zai/glm-5.3-flash`; the independent coverage critic uses `gpt-5.6-sol`;
PageIndex and the primary executor use `deepseek/deepseek-v4-flash`; the
sensitivity executor uses GLM; and the native grader uses Gemini 3.1 Pro.
Missing model, provider, fallback, usage, latency, bytes, or cost telemetry is
inconclusive/fail-closed.

[//]: # (ob:b35000cb)
## Compared systems

[//]: # (ob:b7801d33)
The evaluation runs the same frozen input corpus, task queries, and receipt
schema through three explicitly named systems:

[//]: # (ob:64412ec9)
| System | Candidate generation | Deep selection | Expected locator |
| --- | --- | --- | --- |
| `lexical-chunk/v1` | deterministic lexical document score | 900-character chunks with fixed overlap | `text_span` |
| `pageindex-tree/v1` | PageIndex section-tree search | resolved section and pages | `section_span` or `page_span` |
| `hybrid/v1` | fixed lexical + tree union rule | deterministic rerank configuration | typed locator matching the selected representation |

[//]: # (ob:7dccadb0)
No embeddings are part of this initial comparison. If a semantic or embedding
retriever is proposed later, it is a fourth named system with its own frozen
configuration and cannot overwrite these results.

[//]: # (ob:73142c84)
## Frozen inputs and reproducibility

[//]: # (ob:87d1f184)
Each run records:

[//]: # (ob:75c863a3)
- corpus manifest: source URI, byte digest, media type, and page count where
  available;
- task manifest: stable task ID, query, expected source, and gold evidence
  locator or adjudication packet;
- adapter name, exact version, canonical configuration, and configuration
  digest;
- machine-readable `proofpress/retrieval-evidence/v1` receipts for every
  returned candidate, not only the winner;
- wall-clock latency, source bytes processed, and a declared cost unit.

[//]: # (ob:22c08ac9)
The corpus and task manifests are versioned artifacts. A changed source digest,
query, gold label, or configuration starts a new evaluation run rather than
being folded into a prior denominator.

[//]: # (ob:bff754cf)
## Panels and metrics

[//]: # (ob:bcef4358)
Panel 1 compares PR #36 v7 claim construction with v8 over the same 93-file
World425 manifest, 13 tasks, and 75 rubric atoms. v8 uses lifecycle-aware GLM
decomposition, full-catalog BM25 page/section retrieval, GLM proposal/repair,
and an independent Sol coverage gate. Rubric atoms and model-adjudicated silver
source/page locators are frozen after construction and never enter the tested
pipeline. Primary metrics are requirement recall, evidence-set coverage,
supported-claim coverage, and honest-gap recall; secondary metrics include
unsupported factual claims, atomicity, binding, conflicts, relations, latency,
tokens, and cost.

[//]: # (ob:ca0387ea)
Panel 2 is a deterministic disclosure/assimilation conformance gate with 24
cases (covered, relation-dependent, partial gap, novel, blocked/wrong-scope,
conflict/expired/superseded, reusable discovery, and ephemeral/duplicate/stale
assimilation). A fake sidecar/model makes expected seeds, blocked IDs, gaps,
PageIndex calls, recommendations, submit decisions, and ledger heads exact.
Safety thresholds are zero blocked leakage, automatic admission, and
unauthorized mutation; covered queries must never call PageIndex.

[//]: # (ob:64ab9da6)
Panel 3 runs only frozen gaps using `bm25-page/v1`, `pageindex-tree/v1`, and
`hybrid-rrf/v1` (old lexical is diagnostic). BM25/PageIndex each produce one
top-20 list; hybrid de-duplicates source/overlapping spans and uses
`RRF = Σ1/(60+rank)` with a fixed tie-break. Three fresh PageIndex trees are
used for stability; build 1 is primary and builds 2/3 are not pooled or
cherry-picked. The primary metric is gap evidence-set coverage@5.

[//]: # (ob:dc74a6e8)
Panel 4 evaluates legal workflow utility on two sequential World425 tasks and
12 lawyer-style free-form asks. It compares full-data-room, PR36 prefetched,
v8 prefetched, v8 graph-only, and v8 graph-plus-PageIndex. Graph treatments
may access matter context only through `proofpress disclose` (max three calls,
five receipts/call, 24,000 evidence-context tokens) and then use the separate
assimilation gate. Real graphs are labelled staged-evaluation/non-authoritative.

[//]: # (ob:95cca697)
Report every metric with numerator, denominator, exclusions, failures,
inconclusives, and confidence interval where applicable.

[//]: # (ob:eff9c14f)
Report every metric with numerator, denominator, exclusions, and confidence
interval where applicable.

[//]: # (ob:54ea01cf)
| Metric | Definition | Why it matters |
| --- | --- | --- |
| document recall@k | gold source appears in the first k candidates | did retrieval reach the right document? |
| locator recall@k | a returned typed locator overlaps the gold evidence | did it reach the right place? |
| quote binding rate | returned quotes verify against their claimed extracted representation | does the receipt bind a real excerpt? |
| citation precision | adjudicated returned citations that support the task claim / all adjudicated citations | avoids confusing retrieval with support |
| deterministic receipt pass rate | receipts accepted by the #39 contract / emitted receipts | measures operational integrity |
| p50 / p95 latency | end-to-end candidate retrieval duration | operational cost of the adapter |
| cost per task | declared local or API cost per completed task | makes trade-offs explicit |

[//]: # (ob:7cfd6f6b)
An unavailable source, unreadable file, or gold-label ambiguity is reported as
`inconclusive` with its reason; it is never silently scored as a miss or
removed from the denominator.

[//]: # (ob:ea7dc409)
## Adjudication and anti-leakage controls

[//]: # (ob:a73d5561)
Gold locators are created before reviewing system outputs where feasible. When
human adjudication is required, reviewers see the source and task but not the
adapter identity or rank. The final report separates deterministic locator
verification from support judgment and from downstream human admission.

[//]: # (ob:cbc6d19a)
Corpus source digests, task queries, adapter configuration digests, and random
seeds are fixed before the first scored run. Any tuning uses a declared
development split; the held-out comparison is run once after configuration is
frozen.

[//]: # (ob:7d34d742)
## Promotion rule

[//]: # (ob:2959865b)
PageIndex may move from experimental adapter to supported gap adapter only if,
on the held-out corpus, it meets all of the following relative to
`bm25-page/v1`:

[//]: # (ob:8db56a47)
1. receipt/custody pass rate is 100%;
2. gap evidence-set coverage@5 is at least ten percentage points higher with a
   paired 95% CI lower bound no lower than zero; and
3. citation precision is not more than five percentage points below BM25,
   warm-query p95 is at most 15 seconds, and average warm-query cost is at most
   $0.02.

[//]: # (ob:06661996)
The report must show the actual numbers. A positive result recommends further
product integration; it does not automatically change Proofpress policy or
admit any conclusion.

[//]: # (ob:22622fae)
## Deliverables

[//]: # (ob:9e1f0aed)
- frozen corpus and task manifests;
- one result table per named system plus raw receipt artifacts;
- a failure ledger covering missing mappings, invalid receipts, and
  inconclusive cases;
- a short decision memo stating keep, revise, or retire for the adapter.

[//]: # (ob:23df935a)
## Private operating procedure

[//]: # (ob:d568705b)
The runnable panel entrypoint is
`studies/apex-agent-eval/retrieval_adapter/run_private_panel.py`. It accepts an
authorized private manifest and private output directory; neither belongs in
this repository. The manifest binds World425/APEX sources by URI, byte digest,
media type, extracted-text representation, pre-output gold locators, and task
query. The runner emits raw receipts only into that private output directory
and writes a separate sanitized report containing source/query/gold hashes,
denominators, receipt counts, latency, cost, and inconclusive counts.

[//]: # (ob:d196e6d1)
The scored PageIndex and hybrid paths require the local sidecar from #40, an
explicit `deepseek/deepseek-v4-flash` request through the fixed Proofpress dev
AI Gateway, and a `fallback_used: false` response. Missing source custody,
credential availability, sidecar protocol, latency, or cost telemetry is an
inconclusive failure for PageIndex/hybrid rather than a substituted result.
`lexical-chunk/v1`, `pageindex-tree/v1`, and `hybrid-rrf/v1` remain separately
named in every private record. GLM executor output is a same-family
sensitivity result and is never pooled with the DeepSeek primary result.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzUxNTM4OTg1MDI5OTJjN2IxNTc2MWYxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImZkOTdmZDRlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81MDU0ZDgzNWYxYzFhOTg2YjQ1NzgxMjIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgzZGY0ZDJiMDhmNGZjNTQzNGYzY2RkNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXety5MZ1fpUuKq74MsPBfQBupeKNLKu2bNlbq7WdlKkiG-gGByYGGAMYcimtqvIrD5DKG-R98hB-knzndOMyvMxyybXiJFOlkjgzQF9On_7Ody7d-u5INl2Ry6w7K9TRydFmcxa6oR8nceh4SeJly9QNl5Gbu8nR7Cit1c2ZKi502-HZdiW9MDpRbu5pvXR8L47zKA3DVAdJIhMnSaLEzaNYKYWGkiQPUulny1ireJlpGbmur5Jcol1VtFl9pZubo5Pv6EN31skL9FDKjrqa4Y9Ul_ji97op8kKmpRaNviraoq7ECs_XzY1Ib8Trpq7zTaPbFu9sZHYpLzRNaufrpv6TxnS3DTW46rpNe7JYXBTdapseZ_V6ka10tS6qi05WF7HvLHbebvSftwX-Ptu2ujnL6qrVFWTRNVv9_exopSUJMVfJMleBPjLfnOkrfgjC1WehEwYq9sPczVyZxFEahMvY9TwaWd10NLWzsqg0Rt6vSHkW-yoPlJc6cR7kWRj4Qe5nSi3NdOzozjK5abclJuzROLO6Ue3RyR-_O7Ldf3eEVa6blv4yP2t1lkLkfzzKaqXfHX2DGfTagI5VnbWLRndNoa9kOd-UsmoXb754--bVF79_-euzl794-frtF2_O6MPvXr599dvfHK_V0eyj9El2aD3ddljGs1S2RUtapcv8TLYQb6e5vW23qhsa9GVRUZPtTdvpNX6p5JpW1wx-hhdb0oejk2pblphKtsICaiOCtKyzSzzr5UspdRLjcaxdp9_RRN_0cxRSyU2nG0EftpKGJf7yr_8hIN5GXxSsiXYQUike3YbUUF_jm8_E49vBf5QggaKF7mZDsyBFgdIdfT8bR5vqxF3GTrgz2l_ozOh9B8Wf9tBuN6RB7d5BfiYe8_6eMcnck0kUOJ9uTG9vvaPQmNKtuF7pbgUhSvEam-FVhVWep9jTEF0v32Ic60Y2cld4fug4TpbuDPTzeo0H0YJRog_J6p7H9y0X1spVvv_kHt-u9FQQzbZqIVEtWii6yJv6W12JotpsO4Hdu9m2M9HJ9lL8eQtU3COJKAhcT2fJk8f1XnzND4n34nNZqUIBlsWFrnRjBvoeSqU3AjsXwGq--OLdBn-j-XFcjG07A1uqLJMqdZ48sN_UQq9TrWgpWoG3BF7tRJ0bRSyqoiuwHTNusmjr6li8yqFQrV7LPQJb-m7gZXGwM65fTuSPvioFCwTwVdusSIuy6G4-oEuPeX-PcsVL2Fn3U47pC5mtSMeEtRUn-yQSZnHkS__T9T63OizWsipyWPkT0dbbJtPid29ezWDMoWKGaczEWqtCChrbjLsZB1oSKE8H6nmZE8tbuv6sgdKmtEOlN3nH9WM2OgfiQuBHuGRtX3ssXgrYn33wlOfLMMjynYF-RRYk-xAqjU_t0Red50nmBh_d_htNgA0YAhuD4Ol5cQ1yJKrtmvZ73cyA0FUNhmQ-6HdZuaX5t7M90w0DLR3346f73s6WMSbnDc348ofVjSg6LEQHO9CK96fVezGfz8XOv_diT5arCHT1Ywf0shLbSl7JomQWanR2hu8aLAJ_lRclvqgbcVGXas7MVch1Wlxs98hHS4Bh4Ozq7Uv1p60qMgOypHyy6op5qSXxWkHPNXX5IW15dCP7jP7SV2EYuZ94dF9CQAJdkCKZrZRBimQ1Up3XjeH4-hqjscZA1NuO9_D1ao8sszSLlJvITzzazw0IWJQy2LRjgjU-9cwEDeZYcWsg1T5oVX6gloG3M1o4MuvakoBSf2CF7zy8ZyW9JITTEaZP7G1gYth5gAf4bMRL1gCBDQSwhp8xYb9d3fM_pmx7ZBCrNIxksHziqNxjUdVQpGt0qjS6BjjBMAA1YNp0selAC9pWYDH0i9PKOwYDwMvgmSV0bo8xcaIocuHFPnFYZDkaA6frbduJdlVfM5-DhdhCTkDUFOBFtmJTt0C2K3oeLlwnmj3C8rzI83KpbzHwEq83BEAfdgB2Ht2jLIl2c0dyCx_f07xnrA8aT6zFXMBu9pNmkBZQJFHdXpRvZr0Xe2St7ZmFiiP7S-9u6rMlHBTH84Olm8ZZvEz8pdZe7pIXVdUdi9Q62sI62jDVOrvc1EXVcdyg4Z7Ijew_kRf5DXnoZZHdTFqYeu2TRjge8ESHvq3z7gyW7kI3m6awcYM2dU_CNEuWvtRQytgNo2UC0JDecumqTOk0VyqWoZ8uvaVUcbKUHlhQlHupdHToShVy253s2P83y3XiBfCT6Zsjz_GiuRPPveit55z4_kkY_8xxThzi5lbiZMWXgXZ1mENLxm-_-4GDBqydxq1fyXaF54PUy3SUJtJNaEW4jYmnbxX3Ezrott8s106ap06QxXHf78Rn7_t9ss9tu3HcIEzyME_jMOq7mbjhtpvnuNFrsOErTa_jlSrTpxVbZWoGdpgxK623eFVNQmzium4uy1oqATq4vVgR3v8JOFfkN6LesG8Iw110x6fVq06oGu1j_9lxTYa1rhUxpKol-MYcgBeAbdD-8RGgjyWZeOC0kmpdtG2RWp41PFfdDFMC1m5BLtIbRv7VFqBj2cTxPdBqBR1ibInjwEL66bCeYxhhXM_HxQVsq2me-cs01Ni77tDqGCoYlu_pvj8TD_Zq2NqdVi2waA2PadWYhVk1WpONBnoVXXkjKHI2DP7kYYHA_MGLkDr0ddgPfRJNsEN_TnjAsr8HCLz5N_10Xup3YG_lPFttq8vFlXuOX3dtvX0CmpZtiYmINiMO-V5gSfEappYxM6MGWuPT5MU7jIEiz6Xc4MlzmtFZu5HVue12gz1T8J7pIEPb78iCWjMj_hEfZAOX-j3Zs7q8IgnbCdPiUEst9WG_tN1g7tzJTq-rm7QplO3NDLKf3c8E97WtegZyRw7AMFld3mKg79l9HuUNxylb0f5kHeOV0cYt1hTRti_d50BZ1fASX8oggqVVqleNSTzHqsZzAjQVTQZDHRo4raxhMTgBzAJtojlB3-CIwh3EtxKItW3IX53ouFntAo5DfV3Z3XRa7UqI1iiTFUEUKcR1U0CLIZ225yftHuSI4yBa-n7mO8FgCSZRpBE5nhgFst24eZQ5S-xHdyn7biaBIdvNYwI7_QbPVO6DJThpMJiWSazHNvicWM3GuFdb7EfgdAPTIsTgPjMD3CGFaNlQM_721S9mjHA3M_YwWEd7j5saJw97YrTEoN74R04dPsoF6Y676y0E6Qc1C1ToIzgzUoC64n22oxymt52vqDczZ251LWk76fkQBTgfEzMTPtSPlbe2heuWbSwHXKhRPLxtKJiU9Vg6Y7tZVwBu2q3whwGt3Ou1LIGIxId4E1QZBGVXhhaF90iGEWhlZiCFdXpoMvBIgCLd8T0OUM9vwKGdJItzqfKBV40BtonlemqADCxX7XrUs9PKrjgvLodP2Mrv7lZoSUOti0pf37Kb5OcRHejQ_GmVakK5HG2hJ9Dpmp2_om6mUaw9OztIonRJBD0Ls8F6j7G7cWfvjcrZxlQQB6ELb0RnXt_YJFA35KOeHoIbFdXuCUxZN0R5efcJuSESQBq6Z8454MAL3ESF6YDtkwDeYPafEZqjLwdDjY0ARf75JX7kRbcKgbHCopKVYL3PiwYqeznuC7Km-EsM2wt_EfTRw01xseqGHv7RdNijw6Q_Oe63XQNpSYEhYTs4Y3stujvdwWHItO3rz1v4miIFdyD9o9ADEwPbF__a0sYgtiwvZFFhbmipgKKXsiDTBSkzZblrlg2Z5n5tfIP64blACNAGuI79nEH4LAQ2vRPyfsRGbrzHG_sktSy73jXhbnhP87jEQkB0Ow2M76Hhq7pQLSsgFJImPqwNa3DfqFn__aEalpdFSJllesOBQYOBn_mJidkRei9AEYrOzMU-_x77RrZbSK13ReoKY6DNcAHDfmMGsAkdvLxJwh498Z6u1Lyr57qaAPBkFmokVNOGGU2Z1ejBwBjx0w8U0mARvh_xl_SsJFx7-frV-BQRoVLTVOzza3lJS91Iped1nrcDi99LzhInz8MgAD-LB5yZBLz7kOgzQtkkQ7AtE94iYIdbdl5UvaN2pc9HzoXmwOxeWIJWMX9r0XJFrgiTdHqfPEF4deiNeB6FFpWJLZJMH4fVcZgmUmeRyt0hDjAJrI9Y_ZyYeM-cQimdQIa-rwfGNwmT276eE-EmuM4hOvJzj4GqRFmNI7tDbXgVuCgFRt40R7Dbam24vcXS3jKn8CCJTuA3cqRtAADy7WhJCRzhPByLtwy4FWMq79hWk7QJtG55XWZypxVjWT8oXrh-s2OwF4zzNAj-RYGGt_Bj5Fr0M2KPHvz_4dXNvFQlmVaZIweuOgn1D-njp0fp-4eZluNf9RqutNbKrJzxw-y6jQbJKjCIBzhNBXgCqcJyblvdTvjWKdzFK13WG-OZYg93L7iRlcbOqtmt730gXlLwmJqMjczvDpRiIMaJ2RfMiNM8S13tJ042OmhDrmHcDI9JH9g2fTcPYi_PAxktB0I4ZhT6CPkzkgTmS-a6RQ7ogc7fkpIJfhDB0JosA6yRBV6QvLK-NlYHgE7h9K4GLN0JHexxiFSo0iBMvCRnj8p4WGN2ws7wWQkHhXereaUvzBANCyaSc5uevCBFPK187oxQmfc2WbmLxtQ60Vt3DfxsatIsdzb2hfwLCwP6piZIIOO-QmsrAFXbx5kYuQe733P5PY5CFPjgxGmahsmga5PkycRReGo-BJ7sGppDYyTvnqZi3ObOGnWWAduYIdIot10NFkprD3Wycp7EL000nw0O4U_HAcQx1LjPKQjjPFLSDaI8GB2jIS0zDfx-KNfSBwljX8YhtpXrDp79JP0yOOLPyKlM4yEbTBHqeT3o6-CYGR9Z5GAFoE-i1OqC8YfgHTuLYZr-C3JOMR3sxAq8qBi518xorRBTNgAuBTy0bWPdGxMHZh1ew9iTP8fh4kutN8aMtYZ5gHoVBL42DG0R4o4ufvM9CfOeSketiu52nSNXTUJ37n5_f12kKfuEeIcfqPrzf0u9JNCY81pPKZf0VZ74obyVAC2uiBSPMX6OMoAZfzhRve_NPYlIFUbx0rmTtX7SOBiFtlVlNoasQGkhn-aGM3dsWs_bDvRKtwu50e_mLL45LeliOsw7aVnQkEiDjHyqMVpeMRpT2uwmMIxhd6uB9vG-MO5ECyJ3e4jQXvbcHlzZW6OwOVJ26a2XubGz6FFmRtAxN0zVsKVWkvv_rVZzC_AZAL5WNyZtJJub44fW8_7e35jIZS8Emlcmm37GRCEM-BFMUQCMwsCdLjVFS24ENFmVEPbxQwt0f6e_Ava04tfwifrUyMB6DYEh-5BvO8LFt7ppKExdsZ0i6syqdGzk3a__d0fXq5thOixL_U5nW4vKVqwvX3_xz1YTB-0A_y_4Efj9zZVRHPP0BPoz4hSViaAbedOMH58pT2IvjD0_1F6QBGnuLB0FB8aJBpFMU-DT9O80Lf7dATn-7yLH40srbpcW-N_fXzjwoSqKT1IqARdFORk89CXcxTxTgZ9oGfuun7lR4kY60Qo8a-m4Djx214k8tcTglMySIHeVnz0wn91KieVbxzkJ45MwuKdSQkZ-JKVzqJQ4VEocKiUOlRKHSolDpcShUuJQKXGolDhUShwqJQ6VEodKiUOlxKFS4lApcaiUOFRKHColDpUSh0qJQ6XEoVLiUCnxA1RKTCSpdRpFYRYvx5jlJG83xb2PzL71kS9He0mcaHiAg-WfJOSmyv7UtJplm2d2tgs0dGYzpWcmI7u5OT8WrzpLjEkToMRcI0H56ju5bROK6SfMFAPmjsLsdXPzApysYJcZ_K6mQF3BsGv5HXYiHjKUYGiPHI5W_KFuShV44YKTvcbmtsTR78SFTqtpYGhwbeYkrVv-zYyQzObhbRDAEqjZoPA2SGAGRWKmXM6ayeao1K21I-T0s0vzkAAgOrTLEb-Wg482PT7k_3vYImYIV43pGk92wcNY8ChJPUAuyNIPZLWdDTuMY2D4POAygbKZ0e5O4ef2gc9ymcahWqZBNLDcSbJ1on9PTZlSUQJb7M8CZ8aqNXgd59gtlSwWF5tuHh5H8xIexLmwhUQzcf7b11_85uWrMzg1Z7_64l_Oe98dS9TB8qOh6qpo6opIQB-SOs-Bz5SRotvn1Amgp2w1tdlu6CK6Y_GVxRzL6WxRAAQ9qRSwbgyHUGfDJLChuzqry9ldazjWVRRm9-wsQg9_BDuD-BZWdJP4EmnLNoXl77bG_yTQPb6Pc8zuyyUYEUzD_fB8oGCDCpbQTQPc-NIEhHolNsHdF4TVe4s3jK1NNaCVU0O9crPi9e7Ypq6B9L3hL2y9iC3-uJ1APxSlPVSUxs7MWJSGpa_g6TznFr_eSJWgi6Wg5tgizzfFRlNRQR_7HKsn1rWCH6bVX_fCu7u93CkACbTyQqnjT3mnXm9Kec8y82vIRx1NeM8q7pDIPQPNKTACx_2-27WM3AdpN_WHbyLZ_-aeNcnSSDs6jj_FOF6WFO3KdcMRS7LkNSPUmBLeocJwTsXLV-JLqNr1R9_v9ZqWxJDR9e2rph6njWmm88AP40c3e98dPqQXrnWjYcdfvxGf-ZG4WtrAJd1q2jVbk5BloLuKOcorun23LknHB5OUzx6ZZ5KTu94i3RBb1hSnXABWinVRms1A7n7drKflJ_fcfyjTRMno2SPzTbEBcyXrXlxQ4NsEcM_TtRfOyXTtWrF9lV_ZMpCRfv5qBj1AYDnNBqCSkxx-twAwlxywApJcw30go2GYwB_2jCwJs0xGyfIZI_sr3ST3UTdYPQJ8P-ruqbvt3bk06unVfA8N9oEK3tEI3n1_KKMl-9pnz_OGP0wrem-B5Whljh-ygQ_2NS0Yxq6Yj5mAuzaHB0SxnSGa-UCh8MQy3l-z-1JRoIPjjVwdRbc1U_apWVT1vKfLxggcP2TK9rRsgmXb5mFBGTN7q_GJfdpfXT1i8QRyJ_FNrq0uSsLe-wU0sQf7e3oITo1rcS-kZvr4IYTf39c_fQVH944z8ObNL0kxxhTR8UMovb_1B_ANw1acWL21FhOMvb_dX8LF-Fa3NpQydQI3AwqMkb_jh2Dy_sa_HpIBVNn1tdaXtPfWWEcW_Je__mrHDxm3ylBJ80BBOW9muJ2uSQhtHsl-B5P-OPPaylxjWBc8AxrwKJw7S_n4uvM9d6DfW3c-FNM-ou784BocXIODa3BwDQ6uwcE1-H_hGjz-TNftIy3xbGz3JPr-_uMrP8h5ncBNQAcc5QTLNPZ1lMuldtIsyBxHBX7uhIl2XenmThYCPHMqXkl0QAd5wswJPP2Yyd05vBOdOOGJH95zeGf4_7f8bR3ecfwsi50s8dJJLvWewzuvP4IL_g2f5fHTLHH92NFR-oGzPD35nXTRcUltf95lZK0FQbLOt6WQpmDvpzs89qensG9U2VTnE8v-9xY556ZScxTpwCU4w1jYZDqlaOGqlXVFx4MwM92ktWwUo-NzTvecVjvHe8TzTvecVkwFe6WgQ0sNy42ahoRKoWQn55DCeqzo5BwOZ0X-8m__bhOMikoODE8kjcL3Yz2gCVzwl70ZWlCVk16U8vqGBjtEAPhFevy0umjkZsVf9IepJg4rfb2zaKZ1PlcLKdAHDKabj6-cVlNisK-c11N0BilLUmco454w8EnC8KkMuuy41Kc__YUl5TMZYrNNAbKL8YhDnwufcR2aVS3zlOCCeZOo3dFstGYOE1EVx51aoX0FY8rT0ncdJeOhWmlC6O8cyng8Le_LLPMsDzL4fJGzHCvSBqbel1k-g2_fGAIhTTCIa144DmRDTaKPBR0TLE3UVe6Ur5qTMlxZsJFFQ1hxWp1_S2nccj0Pj_15XmJG56YijVKUG01Z7M7UfXBNZFMQK-WqtvM--dvW5fmL02o3v2wDcRwMGNQX74lzRSfRtb5c9H_Mr4Jpz5ScHIMG03dbCim8GJqvTOXUBVXF9r9rYs7CP3ZJlkCBPmnM-EMlBUZws0FkM7yIgU9Sw3xk4v4M8W56eDE5oH84Tng4Tng4Tng4Tng4Tng4Tng4Tng4TviBIyoOtrQjPQBbutx7nPDe0NOek4WgFfHSiVJ_xM9J6HQaz3piJLQnDwnYYlFie_TFn5MLlFyf18vyh2UI-aUUBYNQ1lgjtMVkrcTj2U1W6rm8pgUFubvlb83YVZtju8HhvODUG2_9RW8Chz0w42zTLYY7MxWd7MWMZPbruhwJLSV_jsWbyfiMrIkuzqfH20yiEiTIFHwyAO2c6LFsajioMQqQSTrbF111VoYd17aByQ8-9mtLlu0yc5uTK6HscYDZAEzzVo_EHDMdXKJ5v4b2J1PuiY0Ct9G4ltTQC6IRNSddhy4LYrYKa7odWxO5Lcs3zu6MhUSEj5iyOdY4410EFthxnatxRCclrqfYH5d6PJW6c4bg9s7Q4TKKlktHy_EMwSTEvqPBT4uYZ2bVjV57ASw2FaWLH7PAzOkp88p80JkZEwziFBAgAecV-64EkVotrpu6upiDF25oHXpZLGBb6DTWAqIEUmllmoa3QUA-_E-hjVD0BtSafNuF2vLJ3A46DqW_5d3_hAAul5e6L21dmLiKOR44GjM6rDSMD_YOHyhgP5s6aaQEpi7ZHKnoV63dpnQIonfy7arZAwAEOa0xb3CuvjYJ1MnJEVLab3VTD33bw3Sz8RTGGBSxRwS204r19bazRzjscvS-iKlfNduIhj7S5T3KJGXopgnAL_Tz0dMYsiI7yvS0JMftKl441IZmz5smZ3v8YzY4lmdDX0FkLqqaVBWruVtMIPggsa2UFRxh6-rN3HME2dAXfc220vNBS_ojbgvrbmy4Qhqk3-AY4SyGRNUJ_yD-6z_dxY8j52dE5H9yvhNSEF2h5yloBp_5I1cgpzWd-CQ0S15fLBjRY2IXRKqYXr4Q6bbANF3DoMcSAP66Fd7CZ9XgMI-pMabjNvAnm-ZmvilIVUwR_2YHBak5gqx7Me_n4Z6Vj0LlqTB3QicY3ONJ1mln5Z-WROrNHls6s_SuJ0zgb952NyXLUM8JdAQ9w2HUweSyYRtikDOYYBhgEDvsKIhFYavCTE4-k9XkyOGcNNRsyuErOsczHzeE-JJDjHSysuPrBE8risvRIZG2tSfyhU3S9AzQ-PQTftkDqYYKr-U76-4b1DgFaboajp23C2OZvGDmOM64WH0PBv1_0sdtKg4DGQ_R1I_sglxvk-kQO0_PwApzNtIcjmGr-UjPFlxsZTCk45jQPvsSxUkoo9wP8oEhTZJ-n-LuBXtqgMQ0DRfduZVBPOVShsPdEYe7Iw53RxzujjjcHXG4O-Jwd8Th7oj_bXdH5IlOdeyH3tJL_hp3R5C7cPv-iNOqrsSz74_Y8QD3RL8dN3fTLAm1FyZ7746wpmbRXyc-mi2snus4PzKXRuxxgDj-0ZGTzYnKigxARsKh6g06Yd6KFWgFRGGcPb74gSJjEFQS_kh8_sreXsGVCONlFnymlfz48e6Je0iAzduvjTLjDXYK7g6BjpNfs6s74wFcy2Y953AsG04zhzXZLze0USm7g6SN0k3eYDs3vsIN_p1z7HiHeykO91Ic7qU43EtxuJfif_Zeilx5sXZ14mae_OHvpdhTXNRfT7FTcWUY2W7d1Wk1Fl4dbqfYvZ1iCGt_7A0Vx5ygG6q5rI5z_obyifNcrgtqZFr7ZY3Enisq9N2TZ3Z691xX8c33_w04Avo5)
