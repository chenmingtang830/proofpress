[//]: # (ob:2f7aae98)
# Private legal knowledge-pipeline evaluation — plan and bounded result

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
`inclusionai/ling-3.0-flash-fin` through Novita with high reasoning; the
independent coverage critic uses `gpt-5.6-sol`; PageIndex and the primary
executor use `deepseek/deepseek-v4-flash`; Ling is also the explicitly labelled
same-family sensitivity executor; and the native grader uses Gemini 3.1 Pro.
Missing model, provider, fallback, usage, latency, bytes, or cost telemetry is
inconclusive/fail-closed.

[//]: # (ob:b35000cb)
## Compared systems

[//]: # (ob:b7801d33)
The gap panel runs the same frozen input corpus, task queries, and receipt
schema through three explicitly named systems:

[//]: # (ob:64412ec9)
| System | Candidate generation | Deep selection | Expected locator |
| --- | --- | --- | --- |
| `bm25-page/v1` | deterministic full-catalog BM25 score | ranked canonical pages/sections | `section_span` or `page_span` |
| `pageindex-tree/v1` | PageIndex section-tree search | resolved section and pages | `section_span` or `page_span` |
| `hybrid-rrf/v1` | fixed BM25 + tree union | reciprocal-rank fusion with deterministic tie-break | typed locator matching the selected representation |

[//]: # (ob:7dccadb0)
No embeddings are part of this comparison. The older lexical-chunk system is
diagnostic only. If a semantic or embedding retriever is proposed later, it is
a separately named system with its own frozen configuration and cannot
overwrite these results.

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
World425 manifest. One development task was excluded before scoring, leaving
12 eligible tasks and 65 frozen rubric atoms. v8 uses lifecycle-aware Ling
decomposition, full-catalog BM25 page/section retrieval, Ling proposal/repair,
and an independent Sol coverage gate. The comparator is an independently run,
frozen PR #36 v7 protocol over the exact same task set and catalog. Rubric atoms
and model-adjudicated silver source/page locators never enter either tested
pipeline; post-output Sol semantic labels are reported separately from
pre-output locator silver. Primary metrics are requirement recall,
evidence-set coverage, supported-claim coverage, and honest-gap recall;
secondary metrics include unsupported factual claims, atomicity, binding,
conflicts, relations, latency, tokens, and cost.

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
12 lawyer-style free-form asks. It compares full-catalog BM25 prefetch, frozen
PR36-v7 prefetch, v8 prefetch, v8 graph-only, and v8 graph-plus-PageIndex. Two
diagnostic-only oracle controls isolate claim-graph construction from retrieval:
an oracle claim graph and v8 graph plus direct frozen gap evidence. Graph
treatments may access matter context only through `proofpress disclose` (max
three calls, five receipts/call, 24,000 conservative context-token upper bound)
and then use the separate assimilation gate. Real graphs are labelled
staged-evaluation/non-authoritative; oracle controls are excluded from product
promotion decisions.

[//]: # (ob:95cca697)
Report every metric with numerator, denominator, exclusions, failures,
inconclusives, and confidence interval where applicable.

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
named in every private record. Ling executor output is a same-family
sensitivity result and is never pooled with the DeepSeek primary result.

[//]: # (ob:3c58ee7a)
## Bounded private result

[//]: # (ob:a0a50b36)
The reasoning-wired Ling v8 construction run completed 12/12 tasks with 167
requirements, 236 candidate claims, 390 relations, and 649 evidence bindings;
all terminal routes were fixed and fallback-free. Independent post-output Sol
adjudication completed the exact 12-task v7/v8 pair. Both systems reached 1.0
rubric-atom requirement recall, so the required ten-point lift was absent.
Relative to v7, v8 evidence-set coverage fell 0.61 percentage points,
unsupported factual claim rate rose 5.76 points, and honest-gap recall was
0.7455 versus 0.8242. Evidence binding remained 1.0. v8 therefore fails the
pre-registered replacement rule; the earlier Ling result that silently omitted
Novita reasoning is invalidated diagnostic evidence only.

[//]: # (ob:7438b197)
The deterministic disclosure and assimilation panel completed 24/24 cases:
claim selection, traversal, gap detection, PageIndex invocation, and
recommendation metrics were 1.0; blocked leakage, automatic admission,
unauthorized mutation, and covered-query PageIndex calls were zero. These two
safety gates pass their preregistered rules.

[//]: # (ob:68d24e11)
The corrected frozen-gap panel used the 93-source mixed-format catalog and
froze 27 gaps with 25 eligible locators across nine scored tasks. All 27
fresh-cache builds completed; receipt validity was 1.0 and mean cross-build
locator Jaccard was 0.9316. At k=5, BM25 evidence-set coverage was 0.8056,
PageIndex was 0.6852, and hybrid was 0.5741. PageIndex minus BM25 was -0.1204
with paired 95% CI [-0.3426, 0]. A fully cached replay hit 180/180 source-cache
lookups but had 25.464-second p50 and 71.108-second p95 latency; mean query cost
was $0.002506. Receipt and cost gates pass, but efficacy and latency gates fail,
so PageIndex does not become a supported gap adapter.

[//]: # (ob:cae8c609)
The corrected workflow qualification completed 28/28 cells with 112/112
terminal model receipts and no inconclusives, including Ling high-reasoning
structured output. The frozen scored block then completed 27/28 cells; one
Ling full-catalog baseline executor exhausted the fixed two-retry policy and
failed closed. DeepSeek graph-plus-PageIndex scored 0.2778 rubric fraction
versus 0.4233 for full-catalog BM25 prefetch, with higher unsupported-claim,
citation-error, and authority-error counts. Because the Ling baseline has only
one of two task artifacts, the paired workflow decision is fail-closed
inconclusive rather than extrapolated from available cells. Oracle controls
remain diagnostic and do not repair the product result.

[//]: # (ob:98d41f66)
Retained Gateway receipts and explicit later reports establish a known cost
floor of $38.040025755 against the $50 cap. Failed, timed-out, or interrupted
calls without terminal cost telemetry remain unknown rather than zero, so the
exact budget decision is inconclusive even though the known floor is below the
cap. Final decisions are: disclosure default API pass; assimilation gate pass;
v8 claim-construction replacement fail; supported PageIndex adapter fail;
legal workflow value inconclusive; exact budget inconclusive. This private,
staged result does not establish public PageIndex support or alter admission
policy.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzUxNTM4OTg1MDI5OTJjN2IxNTc2MWYxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImZiMGIzNDJjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ZjkzOWRlYzY1MTZhNTE1NWI3YmY2YWMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgzZGY0ZDJiMDhmNGZjNTQzNGYzY2RkNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfely5MiR5qvAKMlGGuWB-yBtbKfUaslqptUqq64Z7VqzjQwAARKqTCAFIMmiutpsf-0DrO0b7PvsQ8yTrLvHgUAeIJmsvmZgNtMqZgKBQISH--fXl9-esaYrC5Z1V2V-dn622VwFTuDFSRzYbpK4WZQ6QRQ6hZOczc7SOn-4yssb3nZwbXvL3CA8zzwvYJ5vx0HqeWmSFQ6LeZLGLEnTvCjc2PeLMIrT1IujwnODLI3yIg6DII1tu3BtGDcv26y-483D2fm3-Ed31bEbeMKKdfioGfwj5Sv44N95UxYlS1fcavhd2ZZ1Zd3C9XXzYKUP1pumrotNw9sW7tmw7D274fhSg4-b-q8cXnfb4IC3Xbdpz5fLm7K73aaLrF4vs1tercvqpmPVTezZy8HdDf_btoR_X21b3lxlddXyCtaia7b8u9nZLWe4iEVqp57vZmfikyt-RxfB4vKrpEi8JOdZGDghg6UO0igtQobXbuqmw1e7WpUVh5mrHVldxV5e-Lmb2nHhF1nge37hZXkeideRs7vK2KbdruCFXZxnVjd5e3b-9bdn8vHfnsEu102L_xJf8_wqhSX_-iyrc_7h7Bt4AyUN8OC8ztplw7um5HdsNd-sWNUu337-7u3rz__91RdXr37_6s27z99e4R__9urd6z9_uVjnZ7NnyRPrYPR028E2XqWsLVuUKr4qrlgLy9txGm_b3dYNTvp9WeGQ7UPb8TV8U7E17q6Y_AxubFEezs6r7WoFr5LdwgZysQTpqs7ew7VuETHGkxguh73r-Ad80bfqHS2Ws03HGwv_2DKclvUf__P_WLC8Db8pSRLlJFie0-w2KIb8Hj75hfX0ceB_cgsXFEboHjb4FigoIHRn38362aY8caLYDgaz_T3PhNx3IPjmE9rtBiWoHZ3kL6yn3D8yJ1a4LAl9-9PN6d3OPXA4ypy31v0t725hEZn1Bg7D6wp2eZ7CmYalU-tb9nPdsIYNF88LbNvO0sFEP6vXcCGMIITosbU6cPnYdsFeObnnnfzEd7fcXIhmW7WwotxqQdCtoqn_ziurrDbbzoLTu9m2M6tj7Xvrb1vQiiMrEfq-4_IsOXleH62v6CLro_UZq_IyB7Vs3fCKN2KiH0Go-MaCkwuKVXzw-YcN_BuG7-dFum0wsSjPMpan9skT-7K2-DrlOW5Fa8FdFtzaWXUhBLGsyq6E45jRkGVbVwvrdQEC1fI1G1mwyHNAe8f-YF5_MNYfnlXlYIFA-ebbrEzLVdk9PCJLT7l_RLjiKAel-Snn9DnLblHGLGkrzsdWJMji0GPep3v6XMqwtWZVWYCVP7faettk3Pq3t69nYMxBxATSmFlrnpfMwrnN6DH9RFeolM2Jum5mx2xH1l80UTyUcqp4J504NWchcwBcUPmhXpK2r11YryywP2PqqSiiwM-KwUT_hBYke0wr9VeNyAsviiRz_GeP_5ajwgY1BGgMFh6vt-4BHFnVdo3nvW5moKGrGhCS-IN_yFZbfP92NvK6gc-Z7Tz_dT_KtyUdU9CBJv3yl9sHq-xgIzqwA6318bL6aM3nc2vw31HdkxV5WITpcyf0qrK2Fbtj5YpQqJDZGXzWwCbQR0W5gg_qxrqpV_mckKvF1ml5sx1ZH85AGfr2UG5f5X_d5mUmlCwKH6u6cr7iDHGthdc19eoxaXnyIGNGP_LyIAidTzy7P8ICWfAIFCRxlDJYRbQaKS_qRmB8fg-zkcbAqrcdneH725G1zNIszJ2EfeLZfiaUgNRSQjcNTDCHvxQygQEL2HFpIPMx1Zp7fh757mC24MisawkCQHDHd3jv4pGddJMgAd8rPfFpGonByQP1AD4b4pI1KIENLMAa_AwD_Xa1wn8E2UbWIM7TIGR-dOKsnIVV1SBI9_DQnMOjQTmBYQCtAaaNl5sOYEHbWrAZ_OKycheAAOBmwJkrkLkRY2KHYegkSXjitNByNEKdrrdtZ7W39T3hObAQW1gn0KgpKC-0FZu6Bc12h9eDC9dZzchiuW7ougXjOwh8Bbc3qIAedwAGl44IS8KdwmY0wvOfNFeI9ajxhL2YW2A31UuTkrZAkKxqd1O-mSkv9kxa2yupKs7kN8rd5FcROCi26_mRk8ZZHCVexLlbOOhFVXVHSyodbUs62mCqefZ-U5dVR3GDhp6EbqT6C73Ib9BDX5XZgzGC6bUbg1A84ESHvq2L7gos3Q1vNk0p4wZt6pwHaZZEHuMglLEThFECSoO5UeTkWc7TIs9jFnhp5EYsj5OIuYCCwsJNmc0Dh-UBjd2xjvx_sV3nrg9-Mn5y5tpuOLfjuRu-c-1zzzsP4t_a9rmN2FyuOFrxyOcODwqQkv7Tb3_goAFJp3Drb1l7C9f7qZvxME2Yk-CO0BiGpy8F9xM66PK5WcHttEhtP4tj9VzDZ1fPPdnnlo-xHT9IiqBI4yBUjzHccPmYl7jRa0DDdxxvh1uqjF9WZJVxGLDDpLPSegu35kaIzbqvm_ermuUWwMHtzS3q-7-CniuLB6vekG8IhrvsFpfV687Kaxgfzp-clzGtdZ0jQqpaVN_wDqAvQG0D7O8vAe0jQSZccFmxfF22bZlKnKWvqx70K4Gu3QK4SB9I899uQelINLE4oFrlQgcwt8S2wUJ6qd7PPozQ7-fT4gJy1LTIvCgNOJxdR4_ahwr09p3u-xPwIK-GrN1l1YIuWoPHdNuIjbltOEcbDdqr7FYPFkbO9OTPjy8ImD_wIhgPPB6oqRvRBDn1l4QHJPo7AuDFf_Gr6xX_AOhtNc9ut9X75Z1zDd8Obb28AiQt2yISsdoMMeRHC7YUboNXywiZ4QCt8GmK8gPMASPPK7aBK6_xja7aDauu5WM3cGZKOjMdrKF8bo-CWvFG9CX8wRpwqT-iPatXd7jC8oVxc3CkFp8hP5SPgXenhwyeevuQNmUunyYmqd7utxY9a1spBLK3DqDDWPV-B4F-JPe5X29wnLJbPJ8kY7QzXLjFHCPa8qZDDpQUDTfxGPNDsLR5rkTDiOdI0XhJgKbCl4Gp6gEuK2lYhJ4AnQWwCd8J5A0cUXAH4VMGGmvboL9qyLjY7RIch_q-kqfpshquEO5RxipUUSgQ900JUgyr0yp80o5ojjj2w8jzMs_2tSUwoki95jgxCiQf4xRhZkdwHp2IqccYgSH5mKcEdtQBz_LCA5Rgp742LUasRw74kljNRrhXWziPoKcbMC2Wpd1nQoADUAgjC2hGn77-_Yw03MOMPAySUeVx4-DoYRtGy9LiDf_HTIcPc0G8o8cpC4HygcOCVlARnBkKQF3RORsIh3ja4CN8mnhnGnXN8DjxuY4CXPeJGQMPqbnS0ZbquiUbSwEXHBQu3jYYTMqULp2R3awrUNx4WsEfBtVKT71nK9CIiIfoEFQZLJTcGdwUOiMZzIDn4g2YJZ0efBnwSECLdIsDDpDCN4Ch7SSLC5YXGlf1ATbDcp0aIAOUmw896tllJXecNpfCJ2Tlh6cVpKTB0a2K3-_YTfTzEA50MPxllXLUcgWMBU8COF2T81fWjRnFGjnZfhKmEQL0LMi09e5jd_3JHo3KycFyP_YDB7wRnrlqMCNQp_NRp4fgekGVZwJemTcIeen0WWyDIAAldOSdC1AHru8keZBq3W4E8LTZf0FoDj_UhhoOAgjyP7-HL2nTpUDAXMGiopUguS_KBkT2fX8u0JrCvyx9vOBfqPrw4qa8ue30E_6beKDSDsbzWH_ehgZSggIBwgZ6Rj617PYeBw5DxuWz_rYFX9NKATug_GHogYCBfBZ92-LBQLTMblhZwbvBSCUI-oqVaLpglQmy7JtlAabpuTK-gc-hd4FFAGkA11G9MwA-qQIb5YR87HUjDa70jbwSR2adck3oMXSmaV7W0oKlGwzQ3wcD39Vl3pIAgkDii-u9IQlWg4r9Hw_V0HpJDcmyjG8oMCh04C-8RMTsUHsvASKUnXgXef1HODes3cKqKVekrmAOeBhuwLA_iAlsAhtu3iSB0p5wH6_yeVfPeWUoYOMt8h5QmQOTNiVUw7WBEcuPX2BIg5bwY69_Uc5WqNdevXndX4VAaMXxVeT1a_Yet7phOZ_XRdFqFD8KzhK7KALfB3wWaz1jBLxVSPQFoWxcQ0BbIryFih3csuuyUo7aHb_uMRcMB8juQgK0ivBbCyNX6IoQSMf70RMErw6ehjgPQ4u5iC3imj5NV8dBmjCehXnh6DiAEVjvdfVLYuIKOQWM2T4LPI9rxGeEyeWzXhLhRnVdwNKhn7sArYqQVTiyA2hDu0BFKWDkxXCodlvOBbaXulRZ5hQ8SIQT8B060jIAAOvb4ZaicgTnYWG9I4VbkU6lE9tyXG1UWjtel3i5y4p0mZoUbZw67DDZG9LzOAn6JgcY3oIfw9aWeiPy6AH_H9_dzE3zJON5ZjONVY1Qv04fnx6lVxcTLIf_1GtwpTnPxc4JP0zuW2-QpAAD8ABMU4F6AlAF27lteWvgrUtwF-_4qt4IzxTOcHdBg9xyOFk1ufXKB6ItBRxTo7Fhxf5EMQYinJixYEacFlnqcC-xs95B07mG_jA8JX0gx_Scwo_dovBZGGlA2GcUVIT8BUkC8SFh3bIA1QMyv7NKIviBAINztAxgjaTiBZC3qu-F1QGFjuH0rga1tBc6GHGI8iBP_SBxk4I8KuFh9dkJ-YYvSjjkcG81r_iNmKJAwQhyduHJBQriZeXRw1Ar09lGK3fTiFonvGvfwM9Mkyaxs7Av6F9INcAfalQJaNxvYbRbUFStijOR5tZ2X2H5EUch9D3AxGmaBomWNSN5YjgKp-ZDwJNdg-TgHNG7x1cRbnMnjTqtAdkYHWlk264GFIp7D-Ik19mIX4poPhkc1D8dBRD7UOOYUxDERZgzxw8Lv3eMdFrGDPw-lmtRQcLYY3EAx8pxtGdvpF-0I_6CnIoZD9nAK4J43mt51Y6Z8JGtAlABwCdrxfMb0j-o3uFkkZrG_wVwjjEdOIkV4KKyx14zIbWWZaIBwFKgD-XYsO-NiAOTDK_B2KM_R-Hi95xvhBlrBfIA6FWi8pVhaKkh9mTxm-9wMQ9UOvK87HbrHKlqEmRn__PDdZGi7BOWV3-B1Z8_l3pJ0MaU1zqlXNLLi8QL2E4CtLxDUNzH-CnKAMj48UT12J0jicg8COPI3stanzQP0kLbqhIHg1UAaWF9mgfK3JFpvW47gFe8XbIN_zCn5Zvjli7Nae6lZQGGhBzAyKeao8QVvTHFwy4CwzDt7lbDPjoXwp1oAcjtThGklzy3ozu7MwuZIyWXXnqZG_kWSsvMUHXMBVIVaKll6P7_nedzqeAzUPB1_iDSRqx5WBzbz8NPfysil2oR8L0y1qg3RgghlB-qKQyAYRi44yuO0ZIHCyQ5X8FiL45t0OGH_ivontb6AnwilRrRqFcAGLQPxbZDvfiONw2GqSuyUwidSZQWYr3V_n97dn_7oF-H1pJ_4NlWamW5rK_efP7fpSRq6QD8X9Il4Pc3d0JwxNWG6s8QU1Qigi7WG9_46ZnyJHaD2PUC7vqJnxZ2ZOfgwNihXhIzBW6mf820-LeT5vjPqzmeXlqxW1rgfXe4cOCxKopPUioBLkpuZ-ChR-AuFlnuewlnsed4mRMmTsgTngPOimzHBo_dsUM3j2ByOcsSv3ByLzvyPsNKieidbZ8H8XngH6iUYKEXMmZPlRJTpcRUKTFVSkyVElOlxFQpMVVKTJUSU6XEVCkxVUpMlRJTpcRUKTFVSkyVElOlxFQpMVVKTJUSU6XEVCkxVUr8AJUSxkpynoZhkMVRH7M08nam3ntm9k1FvmzuJnHCwQPUlt9IyJnCfmpaTaLNK_m2SxjoSmZKr0RGdvNwvbBedxIYoySAEFONBOar93LbIhSjXpggBpg7DLPXzcMFYLKSXGbAdzUG6kpSuxLfwUmEiwQk0OOhw9Faf6mbVe67wZKSvcLmtojR9-JCl5UZGNKuzRxXa8e_maEmk3l4GQSQAGqmBV4GCcSkcJkxl7MmsNkLdSvtCDr95NIcWwBYOhiXIn4tBR9lelzn_5XaQmQIrhrBNXrZJU1jSbNE8QBwgZZeg9V2pk8YxcDgb62XUSmLNxqeFLpuTPlEURoHeZT6oUa5RrLVkL9TU6ZYlEAW-xe-PSPR0l7HNZyWipXLm003DxbhfAUexLUlC4lm1vWf33z-5avXV-DUXP3r5__jWvnusEUdWH4YqLorm7pCEKBCUtcF6GfMSCH7XH4OqmfVchyz3SAR3cL6k9Q5EtPJogBYaKNSQLoxFEKd6ZeAA93VWb2a7VvDvq6iFKdnsAlK_aHa0cu3lEtnxJdQWrYpWP5uK_xPVLqLQ5hjdiiXIJbADPeD5wMCpkVwBbIpFDd8KAJCSohFcPcCdfVo8YawtSkH1UqpISXcJHjKHdvUNWh6ZfhLWS8iiz92E-hTUdqxojRyZvqiNNj6Cjydl7D4KSO1Ari4snA4ssjzTbnhWFSgYp999cS6zsEP4_n3S3i3_5S9AhCf527AePwpOfWUKaUzS8ivQR-1N-EKVeyByJGJFhgYAcf9ELuWWHe92k39OBPJ-J0je5KlIbd5HH-KebxaYbSr4A1FLNGS16Sh-pTwAAqDc2q9em39EUTt_tn8Xm9wSwQYXe9STT1NGtOMF74XxE8e9hCHD8qFI91osONv3lq_8ELrLpKBS2Q17ZqtSMiSoruLKcprdWOsS8z2AEmyF8_MFcnJobeIDLGrGuOUS1Ar5bpcicOA7n7drM3ykwP8hyxNcha-eGaeKDYgrCTdixsMfIsA7nW6doM5mq6hFRur_Moin4X85bvpKwUB2ykOAJacFOB3W6CYVxSwAk1yD-4DGg2BBP4yMrMkyDIWJtELZvY9Mck9i8HqCcr3WdxT--PtkUadXs13bLJHKnh7I7h_vy6jRfuqsudFQ3-YFb07yrK3MotjNvDos8yCYTgV8z4TsG9zaEIY29HRzCOFwoZlPFyz-yrHQAfFG6k6CtmaMfvULKt6ruCyMAKLY6ZsZGQRLNs2xxdKmNmdwQ37NF5d3etiQ-Ua8U2qrS5XqHsPL5BhD8afdEydCtfioErN-OKYhh9_1u_-BI7unjPw9u0fUDD6FNHimJYeH_2IfoNp55RY3dkLQ8ceHvcP4GL8nbcylGI6gRutBfrI3-KYmjw8-Fc6GYCVXV9x_h7P3hr2kRb-j1_8aeCH9EdFV9IcKSinwwxupyMSQpsnol9t0p9mXltWcJjWDb0BTrhfnL2tfHrdeWAHfh57QeFkDgNlnvpBFDuue6zuXBfTPqHufHINJtdgcg0m12ByDSbX4L-Ea_D0nq7dlpZ41o97Hn53uH3lB-nX8Z0E4ICd236Uxh4PCxZxO838zLZz3yvsIOGOw5zCzgJQngUWryTcx0aeILN9lz_l5faad8JzOzj3ggPNO0WeREXu859Y847tZVlsZ4mbGrnUA807b56BBX_CvTxemiWOF9s8TB_p5VHg13hERyW1qt-lR60lqmRebFcWEwV7_zjAsf94CfYNK5vqwrDs_yA151xUavZLqrEEZRhLmUzHFC24aqu6wvYgeDPepDVrctKOL-nuuawG7T3Wy7p7LiuCgkoosGmpoXXDoWGFVlbOOjaHVVj3FZ2Uw6GsyH_8r_8tE4w5lhwInIgSBZ_39YAicEEfKjO0xConvlyx-wecrI4A0I14-WV107DNLX2gmqkMhxU_HmyaGJ36amEV8A-YTDfvb7msTGAwVs7r5tiDlCWprcu4DQRuJAxPRdCrjkp9VPcXbCn1ZFibbQpKdtm3OKhc-Izq0KRoiassKpgXidqBZMNoopkIqzj2aoXGCsZylzPPsXMW62olA9DvNWU8HZarMssiK_wMfL7QjvqKNI3UVZnlC_D2gwAQTASDqOaF4kAy1GSpWNAC1ZIhrmxQvio6ZaiyYMPKBnXFZXX9d0zjrtbzYOHNixW80bWoSMMU5YZjFrsTdR9UE9mUiEqpqu1aJX_benV9cVkN88syEEfBAC2-cJ91nWMnOufvl-of8zvffDImJ_uggXlviyGFCz18JSqnbrAqVn3PETlb3sLBtQQtoJLGpH-wpEAs3Ewv2QxuhIkbqWFqmTicIR6mh5dGg_7UTji1E07thFM74dROOLUTTu2EUzvhIy0qNhxpm7mg2NJotJ3wYOhppLMQYEUc2WHq9frTCJ2a8awTI6EKPCSAFssVHA9V_GkQKDke7ZfED1EA65diFAwWZQ17BGMRWFvB5dlDtuJzdo8bCuBux9-akas2h-MGDucNpd7o6C-VCdRnYEbZph2EOxMVneTF9GD2q3rVA1pM_iyst8b8xFojXJyb7W0iUQkgSBR8kgIadPRINKUbNfoFJJBO9oVXnVzDjmrbAMlrH_uNBMtym2lMgxJKtgPMtGKat7wH5vCm2iWaqz2UX4lyTzgo4DYK1xIHukAYUVPSVT-yRGSbw55u-9GsQpblC2d3RouEgA-RsmhrnNEpAhTYUZ2rcESNEtdLOB_ved-VOugh2D0ZPIjCMIpszvoeAiPEPpDg0yLmmdh1IdeuDxYbi9KtX9OCie4pcctcy8yMAAZiClhAVJx35LuiiuT58r6pq5s54MIN7oNaiyXYFuzGWsJSgqbiuRgavA1U5PpHocWi8A1Aa_Rtl_mWOnM7kHEQ-h3v_jeo4Ar2nqvS1qWIq4j2wN6YYbOSnh_YO_gDA_Yz00lDIRB1yaKlQu1au02xCUI5-XLXZAMAqpxWmDdwrr4SCVSjcwSF9u-8qfWzZTPdrO_C6IMiskVga1asr7edbOGQ26F8EVG_Ko4RTr2HyyPCxFjgpAkov8Arek9DZ0UGwnRakmO3ihccagGz501TkD3-NRkcibNBXgHI3FQ1iirs5rCYwKJGYlkpa1GEras3c9e20IZeqJrtnM-1lKgWt6V0NzZUIQ2gX-gx1LMwJaxO-Cfr__1fZ_nr0P4tAvnfXA9CClZX8nkKMIN6_tAVKHBPDZ8E35L2FzYM4TGiCwRVBC8vrHRbwms6AkH3JQD0cWu5S49Eg8I8osYY223An2yah_mmRFERRfybgRbE4VBlHdR5_xyM7HwY5G4eFHZg-9o9NrJOg50_LYmkzB5ZOrH1jmuJwN-87R5WtIZ8jkrHwmsojKpNLhk2HYOcgQkGAwzADk4ULEsORxXMpPE3Wk2KHM5RQsWh1B9hH8-8PxDWHynEiJ2VHdEJXlYYl8MmkbaVHfmWTNIoBCh8egNfKkXKQYTX7IN094XWuATQdKfbztulsEyuP7Ntu98s9QSh_X-j4jYVhYGEhyjqR4ZKTtlkbGKn1xNqhTAbSg7FsPN5D8-WVGwldEhHMaEx-xLGScDCwvMLjZCMpN-n4F6QXQO4TGa4aI-VwTqFlGHijpi4IybuiIk7YuKOmLgjJu6IiTvi58YdUSQ85bEXuJGbfB_cEegu7PJHXFZ1Zb2YP2LgAY5Ev22ncNIsCbgbJKPcEdLULBWdeG-2YPcc2_6VII0YcYAo_tGhk02JygoNQIaLg9Ub2GHeWrcAK2AphLNHxA8YGYOFSoJfWZ-9luwVVInQk1lQTyv68T33xAEQIPP2ayHMcAc5BftTwHbye3J1ZzSBe9as5xSOJcMp3mGN9ssJZFRKniAmo3TGHWTn-ltowF_aC9udeCkmXoqJl2LipZh4KX5cXooid2Pu8MTJXPbD81KMFBcpeopBxZVAZMO6q8uqL7ya2CmG7BQ6rP1chooFJeh0NZeUccrfYD5xXrB1iYOYtV_SSIxQVPD9zjP5ehNdxam_ofQTpqswCtz6hx0om3t6F4RRd3baiH3gRA1p1Ct9okk-u_nJbGAWqBX27OszBxfOcUFevz6LEH2Ewdk33xx_rpcFMefRsLXpd7JouT_eeN4e6Xg7etNYA6LNAjv1whc-HS2N484Jh97Fw8w8usjqpBuxOo02R_Yk8r04dXYahU6b3dO7lwVQUxG-MbGOc9fnjvMJZicgPVUOiMffspx8TZH4IkVMiVIMC1HuV5RKjLbM8TgL7eQTzE72EaBFUDk7ibeESyuSRapSH5CWKM3KxlrA4tx3ivClcveWIxaDW1QJt4Z9nIrRyhazr6RqhbGHyaNhLKxfOiOzM3I9_ez6eciw5_fWkHY6XcNnwniIWKxK2xCMQ0M4l3l3QAFYPkr1VPCxSlKnB5d_ccw4HJ3EV1ik0crqcUArc-lwGpGzdgOeXyG9coLmRPmgfwLtsPE4_tpCQMUzsx0rgOProiazmGmYdze_oTabgcLoGQgWx-zQ8dmtGIZcuUzYqDIFWc2MIcu-XEEUqvR1txIBApJDJCtKbw8s0j6JwyOLJGMIABRuqFPEEE1cL8ftU-5WOKwtk6FO0XvAsSSnEQ0rOm4q7IAW8MWxs7V3nDTpyJp-IolZugRDuV_wpLlZsIUHhvLXi2NGdYSbg-kq791fXho7AobJHP_pQdHgYbp11NgxvxHpuIGN7EF4tuKsgVNBWZxWu466Ys0sblkcs5aPT6zPYD3dMhpcDga7xGGL-PgMyIxpAewPoymKVNWHjWSmp0U3_m3LqGhErsvimO0bn0dv2bC8ga83MKK2cVL1t6rUWLrSAy2u2mQG-6wKWnQP1zHT9_giCdPVxw-UCZvpKFzvvip-l1lPjmPWa1hUPPf470tK1aCOgMAjw3iG-aOZoJpAljBbQ7MbTuIActBRdtn3i7-ItqLDrGmDns4DEsZpxliYeGEKKtPNs8iOUzc9ygOi-3J_Yjwgk881-VyTzzX5XJPP9SP6XE_nmNqlighNqohgpid77nx3mBXih-HEyFLHCTPm5GHKvSixE576SRqmIc8CF1tb4yQvoiDjmZfDyvOQR1nmxV4CT8ryZ7_oLj-Gk5y79rlziB8jSMM8L7zkJ8aPUTAnwlXxisT5pPwY6GVTqbY8bWNmYiLJmEgyJpKMiSRjIsmYSDJ-DiQZYR6FgZMzJ4u8cZKMHmr_NDgyYl7Ejs9T7kTuj8yRMah73OOF2G_QVQQZWAUsXDzZ_E5cFap196mkFT8mVYYudlB0GfR-A64MajAosTILwAExZBTCOB_godU9dp-eNyOyGQ-CiOW-x07mzTD5MvBMYHd7Yw2KRFSBHp5yIzOAyZsxjg3rcYoNsNBGMcmjPBvWMZqNy2ri2Zh4NiaejYln4_vk2cjAMLtx5hU2s38sno2F9eeKm7lNsXn3rBXBpLxvNZGJ0Bl2CtwR55Hj9vmtQTpVqteJsWNi7JgYOybGjomxY2LsmBg7JsaOibHjZMaOiQpjosKYqDAmKoyJCmOiwpioMCYqjIkKY6LCmKgwJiqMiQpjosKYqDAmKoyJCmOiwvhBqTAMz9bz7JRnAUtsHXM1GlB6DfycXhI1dpJ4oMn9xIk19jPaSwzhP7VTRBRGihUWqkbsBFwNznO7LcCBKrFunlD_lcgwtteq7ndQuydK9m4oX9_W0p8btKjJYAK5NkYbIOyGvXQAm_6-L4dRikT1nxa4epcV4tg-7qWCWUb5mEX2mU5EEiyi8FdYmNDUSqvu5g9FbFKEOIawuN2KwDEeBwem55iNIyomJ_KjC-tLQPSoXODhsiUbcYuRqiZXim7B3LIOcdBCwaJimE4GHnH1d-r_RqTP47ldpJljh76WEKPFx5CQU7t1csv1l64vMM05KCAKuulyuBmGgrC8AbPR6Fvgc-Q3RlltdVdnfSEJSpmZgNO52HsMMTgL--JpqbQjaTQVcqZUmgT6OylA8ST0SciqYmj-HvZw8HPm5ECJCOjwFzDRKx2zWXbgulEaZn5h60JMo7PJ2JRTm5T6CA4IS4nJa4qsCBPwD63lxvM3v_-DMhukr3nXt7NiIHxN0ct-WWTS6p4qlAbSZw0blvb7ZPEA0-RIlMwsJeyQUPQHkYDOpO22-4q02aHGYMy_6pS_csw3Ol6AF6swFh0k64nnKAkzz3ci2w2Dok_A63avYaHPSZ1bhlbWP5dFwSwVUMZ7t5gMGbQriyJ-1atMEiGzDyLxJMsMQKo3ZoxMSJPcKji_tpVxEPsLy4eNoIMFC2poLKGqKI-PD5pZUW9cxYFBeEDvVetiqqC3IyS4BdfePuXNLqWzlK4wGUDl062cJMAaNTuamDiPyvoKJgvR6EHOrUgn4vSkqpZRB1ncD0p0J4WJabJnC4Gfg1cLBzVnkT63RledzpKd3iDnLJLI8ZwotFWKRZzcX4JdE1v4B1pm0KqYcUG_gOAb5cyaLR1ZsR24i73lyih2ofGdsr9S9lJsFen66MKBRbHMFqCZ7N9R4K4PMvRvKJsojCpiGVvFwsNVZ_akXFYi9nAinxj5iufHWMV2vt3hFtv7dsgwRqHec9A4t6zJOwbg66dBN8aru7KpqzUBr05UTR1iHaP5n8o6ZnSO9B2Z460p423aWC9rjzZmv6Qh_NiYRn3Dpxvzk_8O-0v7w59CCXBK7_QTxj2p6_kJ457Ur3xE9EzNCl_90osXtm_bbhAFAdEGoILFL4IDAnqYj8k4Hkc5dwxaDZFSRP6ae7JMXyi_hEICc91IJUrX6ECpMI30zrqh8X4-A5AxG6H3De8MzCm6gnfRkjxE7Y1QpAz7_KQHrVoP5oOMnmL9WBw7eUfn9CoXE6oblq24RDNk2CkchchXl4SbPEkYtS9FDl-CVkDhutxEcl4p2Lc4dnhHlopcLrHmAthgPGEQLcCuuT4wICI7tKtGgGH_jsfIhEa3rfe5lD8vcc4xNiE5d9hT04k8TEyzz94zOhcJrue6xLnC6n6aVG_0Jf7K6lW-xKyK0rYzc3Y9PD88sX06n9GJoVuG26CxHjkPhZk8J3gcLd14QGVDhbCrYeZ-nLlndB6BDbhotWKNwlc9N44Af5LJp4-6ZeAoM-n7iJOu0wLgnh2l7hGiSoWx6IiuSpy9Dk21vYz24rOrjQ6IkeGez8wy4Zle2JksZqSX05Wxz2PwSYrES-DeMHBCBigoSKO0CFl2jMFHMwc8zuAz4ZcJv0z45SC3yQhvlqb86Ik-4u8Oc3f8ICwmIYuTIoo9p4izyEn9pLAL5qaeHXgJLECUZT68jZ_4vhfHUeLHLIgT7qZhgUnIxD7-SkO-kvidHZ07zrkfHuArKVIQaN_NJr6Sia9k4iuZ-EomvpJPwleS23kS88DlXsp-fnwlpTp0rFyuEEp7C1vk_udgyK71_L6ER3ZMTATL43rwLVlGnklwYh3lN8HKhCcTnJCriuKx0rFgzaChukow4XXYl1UPmkhQJhKUiQRlIkGZSFAmEpSJBGUiQZlIUD4tCUqagINv-5wXLv8vTILyBY11MgvKFzKaeRINyjv9oyKqlml4j0idzVSDk7H2qtS2X2n5SwK43rSGWEgoTAq9xZBzRUzwGOmKdZBzxWRUkWXsu6QqF4OEHr6wNqXyRycEyYr0Ew1biVk19KF0PfpumeMT2VrATzlI12I9l60F63eP0LVYz2Rr6SlKDtO1WBNby8TWMrG1TGwtPyBbSxbbPI0TJyq8ny5by9AAS2qWmRQ_OKxvvXBOtlB9YzC4PI-_5R1WYPeiJ4pAZeGI6oCH1a5XOsQ819WxPfqh0hCNDc7RyOpByOj0NShqJqJBUFSkGOdKb6mklgFJ19wy1oupZbDws-eWsUaoZfD1kDFFtlDQU-ai6hcsoCo8_o2AEwepZqxnMM2o2s9RqpmLvX3BITRaVOU52LFKQdmd-o92oqqZqGomqpqJqmaiqpmoaiaqmomqZqKqmahqJqqaiapmoqqZqGomqpqJquZnSVXjZYkX-06ROvFEVTNR1fRUNZSe_M_OVWPDGDa3PcZCPs5Vc7BV8hBxjdkOt3RckxTDCSP0dHXqEc6v64V7JcgzCxC8me6j5LSf7FHIoAlEJCy8M_TcsAhV0hKIoyI62sRZmGPYHPS8kVneSboidDEcTSM2odPEmrOHmjIRnC5g4THQI6r6RIgM335hw8tS5niOqc2Dv5AhqzyVO4ugeC5s2qosOkE7k6IuB_l_28N7eDpF6Q_ibHChYU3sRejsg9vZyA9mCCzf1C23kINH3XE4y4tTu6zsReQHAdWIAAKyF7Hrgwfw-S7Tj2YngjWhcoKe8QOVQitcc7RTJl-LSbADbppwHjlrViUcqy_EuAKVUfBOhVdqERm7rGSJrxZcPJMSXlE8wqhg04JFpWwTcc_PirjH5XnIYscu8pyNE_f0LDB7FD6UekQBS7y5tIlr6gGn1H6nakHEctLdlhuJPK5I9wd9RU0f_crgNLXUg6vQQycSdlg-70Y4Em9v5xlqDJXS1JJwsceORfoA9ksWKoGppAfM6c7LSgXy_wVgLPaw4NX2IvGcEB7YWe__KZiJhOBhtSEuj-0gHKTzxcdhHLgzE_GIj4PIdxbGboPEgyKgh-AFc3vhuLZ_WdEaDT35r-FLz3fDmWV_Q9UHW_IrhfKkw_9g3QJGcmJ7Cf8vkYpYK3zX-v1WUiwhi40bLPzQnwt3nMLcONfIWTh2rD_tw94XYvl6Hx2mCPNFz9x2AzvETJt05WRliSGlkn4NWdZYJtLRKpouLkKlhnQstbEy2o9O8SxyAjkHgkBj0UAAZl4epnmRPZ_taNhubWibGBuuJZsP2Wi02o6LvDTSqEryA5PyqKqtnRycKPBBLUuaGcM4c615LyVE2OL2C2sr463C_5Zng5SQyIUaE4z0BC9E5QI9YJDlTkFZipY5Bdf4h1u2bTtN0ECVCPf1vCF0KkMV4iybDEmLHp4dynaridoLN4piVSVXoPNFVaXaDvqu5xHOHUvG694T7MzY_U0sROIyhDXnTYPJULIcMp_7ID5U7o31OzDKKn9M66OXBISHrBoGFalXDssNCMEYdIKiQ59Op5aY3IibGV0cO6DexO3kh24o0y-j3n2qhTZwYf15mIBWxIWmLTYIpGRnj2imEeGpR9Gyj79M56ZB4STJKXRQVDSl_DPR8CXc1WNMUSBCmirK7AA2c5zWL4OnMkVh1Zg6jBj61cdwx8OSCyfZg_Yo13oyxwGblLmpg33EXmQLnygdTYMMAa8VMVEaT7zGgAiBsgXnJsrJecEQmmGqD1XmxX4xg_icfjtIlIXs0GX06A-l78JQl4YHLiPndAU2cB6gEzNf82LIrfWTINP65rv_D6ZmpHo)
