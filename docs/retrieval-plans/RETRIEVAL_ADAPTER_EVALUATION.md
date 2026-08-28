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

[//]: # (ob:7d40592c)
[//]: # (ob:v9hierarchicalpanel)
The next-stage panel preserves those three historical systems and adds two new
versioned conditions. `pageindex-hard-route-bm25/v1` limits exact-span BM25 to
PageIndex routes and is diagnostic only. `pageindex-prior-bm25/v1` uses the
tree as a soft document/subtree prior, retains a global-BM25 safety lane, and
requires every final excerpt and locator to come from canonical BM25 span
resolution. It reserves at least two global results in the top five and falls
back to global BM25 on an invalid route. No prior result is overwritten.

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

[//]: # (ob:dc7fb7ed)
[//]: # (ob:v9e2eprogram)
The follow-on v9 program first qualifies evidence-first construction on a
frozen four-task development split, comparing Ling high-reasoning and DeepSeek
proposers under the same decomposition, retrieval, atom, claimability, and Sol
critic contract. Selection is lexicographic: lowest unsupported factual rate,
highest honest-gap recall, highest supported-claim coverage, then lowest cost.
Evidence and receipt binding must be 100%; a failed qualification stops the
12-task formal construction and E2E blocks.

[//]: # (ob:adbf154a)
[//]: # (ob:v9e2econditions)
If qualification passes, the 12-task PR36-style E2E panel compares v7
prefetch, full-catalog BM25 prefetch, v9 prefetch, v9 graph-only, v9 graph plus
global BM25, and v9 graph plus hierarchical hybrid. Oracle graph and direct
gap-evidence conditions remain diagnostic only. Every condition executes
decomposition through native grading with the same 24,000-token upper bound.
A separate 12-ask progressive panel measures claim reuse, relation traversal,
gap precision, retrieval calls, context reduction, and assimilation without
granting admission authority.

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
`pageindex-prior-bm25/v1` may move from experimental adapter to the default gap
retriever only if, on the held-out corpus, it meets all of the following
relative to `bm25-page/v1`:

[//]: # (ob:8db56a47)
1. receipt/custody pass rate is 100%;
2. gap evidence-set coverage@5 is at least five percentage points higher with a
   paired 95% CI lower bound no lower than zero; and
3. every global-BM25 gold route miss is recovered, citation precision is not
   more than five percentage points below BM25, and warm-query p95 is at most
   15 seconds.

[//]: # (ob:ac4ce84e)
[//]: # (ob:v9promotion)
Evidence-first v9 may replace v7 only after the held-out 12-task workflow shows
at least a five-point rubric gain, or at least 20% context reduction without a
rubric decline, while unsupported assertions, citation errors, and authority
errors do not increase. Evidence binding must remain 100%, honest-gap recall
must be at least 0.90, and paired intervals must not show material regression.
Component improvement without E2E improvement is reported only as a component
result and is not promoted.

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

[//]: # (ob:86267373)
[//]: # (ob:v9boundedresult)
The v9 four-task development qualification completed both frozen proposer
conditions without task-level inconclusives. Ling retained 1.47% supported
claim coverage and DeepSeek retained 22.30%, versus 88.03% for the paired v7
baseline. DeepSeek reached 0.875 honest-gap recall and Ling 0.5625, both below
the 0.90 gate; both also reduced mean requirements below v7. Receipt validity
and evidence binding were 1.0, and unsupported factual rates were lower than
v7, but neither proposer qualified. The preregistered stop rule therefore
prevented a 12-task v9 construction run and the dependent expensive E2E panel;
this is a failed qualification, not a missing or selectively omitted result.

[//]: # (ob:21a81694)
[//]: # (ob:v9hybridresult)
The new hierarchical retrieval panel preserved the same 27 frozen gaps and 25
eligible locators over nine scored tasks. At k=5, global BM25 and
`pageindex-prior-bm25/v1` both achieved 0.8056 evidence-set coverage, 0.2667
citation precision, 0.6667 complete-set success, and 1.0 receipt validity. The
paired coverage delta and 95% interval were exactly zero; the prior recovered
0/13 global-BM25 misses and found no unique correct evidence. PageIndex warm
p95 was 82.164 seconds, and seven calls lacked terminal cost telemetry. The
hierarchical candidate therefore fails efficacy, recovery, latency, and
telemetry gates and remains experimental.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzUxNTM4OTg1MDI5OTJjN2IxNTc2MWYxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjdlMTQ3MDllIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8zZmVhZjNiOGEyODIxOGNjMmE4ZDVkNjUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgzZGY0ZDJiMDhmNGZjNTQzNGYzY2RkNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfemS5MaR5qvAWqKNNMrMwn1U29hOD9WS9Qwl0Zo90q6xaNUBIFAFdSaQApBVLJE021_7AGv7Bvs--xDzJOvucSCQB-pqUqQUZjNUVyYQCER4uH9-ffnNC9YNdcWK4bIuX5y_2G4vIy8K0iyNXD_L_CLJvSiJvcrLXixe5G15d1nWV7wf4Nr-mvlRfJ5nQeVWbl7wOHTD2E_yOIl5EvpBXCXcY1XiRrHrRSFPIi_0yohV8FVclhF8HLMSxi3rvmhveHf34vwb_GO4HNgVPGHNBnzUAv6R8zV88Efe1VXN8jV3On5T93XbONdwfdvdOfmd83nXttW2430P92xZ8YFdcXypycdd-2cOr7vrcMDrYdj252dnV_VwvctXRbs5K655s6mbq4E1V2ngnk3u7vhfdjX8-3LX8-6yaJueN7AWQ7fj3y1eXHOGiwhvHSZuxl-ITy75DV0Ei8svg4qzKshT5qe-lxaFz9IyKuMIZ9Z2A77a5bpuOMxc7cj6Mg3KKiz93E2rsCqiMAiroCjLRLyOnN1lwbb9bg0v7OM8i7Yr-xfnX37zQj7-mxewy23X47_E17y8zGHJv3xRtCX_-sVX8AZKGuDBZVv0Zx0fuprfsPVyu2ZNf_b29bu3b17_8dVnl69-_erzd6_fXuIf__nq3Zs__H61wb18jDyxAUbPdwNs42XO-rpHqeLr6pL1sLwDp_F2w3Xb4aQ_1A0O2d_1A9_ANw3b4O6KyS_gxh7l4cV5s1uv4VWKa9hALpYgX7fFB7jWrxLGeJbC5bB3A_8aX_StekeHlWw78M7BP3YMp-X81__8Pw4sb8evapJEOQlWljS7LYohv4VPfuY8fBz4n9LBBYURhrstvgUKCgjdi-8W42xznnlJ6kaT2f6aF0LuBxB88wn9bosS1M9O8mfOQ-6fmRMcXpbBQf94c3q3d08Jg5W8d26v-XANi8icz-EwvGlgl5c5nGlYOrW-9TjXLevYdPGCyHXdIp9M9NN2AxfCCEKI7lurI5fPbRfslVcGwZOf-O6amwvR7ZoeVpQ7PQi6U3XtX3nj1M12Nzhwere7fuEMrP_g_GUHWnFmJeIw9HxeZE-e17fOF3SR863zKWvKugS17Fzxhndiot-CUPGtAycXFKv44PXXW_g3DD_Oi3TbZGJJWRSszN0nT-z3rcM3OS9xK3oH7nLg1sFpKyGIdVMPNRzHgoas-7ZZOW8qEKieb9jMgiWBF_pFGk7m9Rtj_eFZTQkWCJRvuSvqvF7Xw909svSQ-2eEK01KUJofc06vWXGNMuZIW3E-tyJRkcYBCz7e05dShp0Na-oKrPy507e7ruDOf759swBjDiImkMbC2fCyZg7ObUGPGSe6RqVsTtT3Czdle7L-rInioZRTxTvpxKk5C5kD4ILKD_WStH39ynnlgP2ZU09VlURhUU0m-ju0IMV9Wmm8akZeeFVlhRc-evy3HBU2qCFAY7DweL1zC-DIaXYbPO9ttwAN3bSAkMQf_OtivcP37xczrwvoj7ne41_3W_m2pGMqOtCkX_50fefUA2zEAHagd769aL51lsulM_nvrO4pqjKu4vyxE3rVOLuG3bB6TShUyOwCPutgE-ijql7DB23nXLXrcknI1WGbvL7azawPZ6AMQ3cqt6_KP-_KuhBKFoWPNUO9XHOGuNbB67p2fZ-0PHiQOaOfBIjWvY88u9_CAjnwCBQkcZQKWEW0Gjmv2k5gfH4Ls5HGwGl3A53h2-uZtSzyIi69jH3k2X4qlIDUUkI3TUwwh78UMoEBK9hxaSDLOdVaBmEJ3tJktuDIbFoJAtb8nh0-uHhmJ_0sytI4yp_4NI3E4OSBegCfDXHJBpTAFhZgA36GgX6HVuE_gmwza5CWeRSzMHnirLyV07QgSLfw0JLDo0E5gWEArQGmjdfbAWBB3zuwGfzlReOvAAHAzYAz1yBzM8bEjePYy7L4idNCy9EJdbrZ9YPTX7e3hOfAQuxgnUCj5qC80FZs2x402w1eDy7c4HQzi-X7se9XjO8h8DXc3qECut8BmFw6IywZ9yqX0QiPf9JSIdaTxhP2YumA3VQvTUraAUFymv1N-WqhvNgX0tpeSlXxQn6j3E1-mYCD4vpBmHh5WqRJFiSc-5WHXlTTDrSk0tF2pKMNppoXH7Zt3QwUN-joSehGqr_Qi_wKPfR1XdwZI5heuzEIxQOe6ND3bTVcgqW74t22q2XcoM-98ygvsiRgHIQy9aI4yUBpMD9JvLIoeV6VZcqiIE_8hJVpljAfUFBc-TlzeeSxMqKxBzaQ_y-269wPwU_GT174rh8v3XTpx-989zwIzqP0V6577iI2lyuOVjwJucejCqRk_PSbHzhoQNIp3Ppr1l_D9WHuFzzOM-ZRzIXGMDx9Kbgf0UGXzy0q7uZV7oZFmqrnGj67eu6TfW75GNcLo6yKqjyNYvUYww2Xj3mOG70BNHzD8Xa4pSn4RUNWGYcBO0w6K293cGtphNic27b7sG5Z6QAc3F1do77_M-i5urpz2i35hmC462F10bwZnLKF8eH8yXkZ09q0JSKkpkf1De8A-gLUNsD-8RLQPhJkwgUXDSs3dd_XucRZ-rrmTr8S6NodgIv8jjT_9Q6UjkQTqyOqVS50BHPLXBcsZJDr_RzDCON-PiwuIEfNqyJI8ojD2fX0qGOoQG_f031_Ah7k1ZC1u2h60EUb8JiuO7Ex1x3naKNBe9XD-s7ByJme_PnpBQHzB14E41HAIzV1I5ogp_6c8IBEfycAvPgvfvV-zb8G9LZeFte75sPZjfcevp3aenkFSFqxQyTi9AViyG8d2FK4DV6tIGSGA_TCp6nqr2EOGHlesy1c-R7f6LLfsua9fOwWzkxNZ2aANZTPHVFQL96IvoQ_WAcu9bdoz9r1Da6wfGHcHBypx2fID-Vj4N3pIZOnXt_lXV3Kp4lJqrf7lUPP2jUKgRysA-gw1nzYQ6Dfkvs8rjc4TsU1nk-SMdoZLtxijhFtedMxB0qKhp8FjIUxWNqyVKJhxHOkaDwnQNPgy8BU9QAXjTQsQk-AzgLYhO8E8gaOKLiD8CkDjbXr0F81ZFzsdg2OQ3vbyNN00UxXCPeoYA2qKBSI264GKYbV6RU-6Wc0R5qGcRIEReCG2hIYUaRRczwxCiQf41Vx4SZwHr2EqccYgSH5mIcEdtQBL8oqAJTg5qE2LUasRw74nFjNVrhXOziPoKc7MC2Oo91nQoATUAgjC2hGn7759YI03N2CPAySUeVx4-DoYRtGy9HiDf_HTIcPc0F8oMcpC4HygcOCVlARnAUKQNvQOZsIh3ja5CN8mnhnGnXD8DjxpY4CvB8TMwYeUnOloy3VdU82lgIuOChcvOswmFQoXbogu9k2oLjxtII_DKqVnnrL1qAREQ_RIWgKWCi5M7gpdEYKmAEvxRswRzo9-DLgkYAWGVZHHCCFbwBDu1mRVqysNK4aA2yG5XpqgAxQbjn1qBcXjdxx2lwKn5CVn55WkJIOR3cafrtnN9HPQzgwwPAXTc5Ry1UwFjwJ4HRLzl_ddmYUa-Zkh1mcJwjQi6jQ1nuM3Y0nezYqJwcrwzSMPPBGeOGrwYxAnc5HPT0ENwqqPBPwyrxDyEunz2FbBAEooTPvXIE68EMvK6Nc63YjgKfN_jNCc_ihNtRwEECQ__UDfEmbLgUC5goWFa0EyX1VdyCyH8ZzgdYU_uXo4wX_QtWHF3f11fWgn_DfxAOVdjCex8bzNjWQEhQIEDbRM_Kp9XDwOHAYCi6f9Zcd-JpODtgB5Q9DDwQM5LPo2x4PBqJldsXqBt4NRqpB0NesRtMFq0yQ5dAsCzBNz5XxDXwOvQssAkgDuI7qnQHwSRXYKSfk21E30uBK38grcWQ2KNeEHkNnmublnDmwdJMBxvtg4Ju2LnsSQBBIfHG9NyTBalCx__OhGlovqSFZUfAtBQaFDvxZkImYHWrvM4AI9SDeRV7_LZwb1u9g1ZQr0jYwBzwMV2DY78QEtpELN2-zSGlPuI835XJol7wxFLDxFuUIqMyBSZsSquHawIjlxy8wpEFL-O2of1HO1qjXXn3-ZrwKgdCa46vI6zfsA251x0q-bKuq1yh-FpxlblVFYQj4LNV6xgh4q5DoM0LZuIaAtkR4CxU7uGXv60Y5ajf8_Yi5YDhAdi8lQGsIv_UwcoOuCIF0vB89QfDq4GmI8zC0WIrYIq7pw3R1GuUZ40VcVp6OAxiB9VFXPycmrpBTxJgbsigIuEZ8RphcPus5EW5U1xUsHfq5K9CqCFmFIzuBNrQLVJQCRl4Mh2q351xge6lLlWXOwYNEOAHfoSMtAwCwvgNuKSpHcB5WzjtSuA3pVDqxPcfVRqW153WJl7toSJepSdHGqcMOk70iPY-ToG9KgOE9-DFs46g3Io8e8P_p3S38vMwKXhYu01jVCPXr9PHTo_TqYoLl8J92A64056XYOeGHyX0bDZIUYAAegGkaUE8AqmA7dz3vDbx1Ae7iDV-3W-GZwhkeXtIg1xxOVktuvfKBaEsBx7RobFh1OFGMgQgnZi6YkeZVkXs8yNxidNB0rmE8DA9JH8gxA68KU7-qQhYnGhCOGQUVIX9GkkB8SFi3rkD1gMzvrZIIfiDA4BwtA1gjqXgB5K3bW2F1QKFjOH1oQS0dhA5mHKIyKvMwyvysIo9KeFhjdkK-4bMSDiXc2ywbfiWmKFAwgpx9ePISBfGiCehhqJXpbKOVu-pErRPedWjgF6ZJk9hZ2Bf0L6Qa4HctqgQ07tcw2jUoql7FmUhza7uvsPyMoxCHAWDiPM-jTMuakTwxHIWn5kPAk92A5OAc0bvHVxFu8yCNOq0B2RgdaWS7oQUUinsP4iTX2Yhfimg-GRzUPwMFEMdQ45xTEKVVXDIvjKtwdIx0WsYM_N6Xa1FBwjRgaQTHyvO0Z2-kX7Qj_oycihkP2cIrgnjeannVjpnwkZ0KUAHAJ2fNyyvSP6je4WSRmsb_BXCOMR04iQ3gonrEXgshtY5jogHAUqAP5diw752IA5MMb8DYoz9H4eIPnG-FGesF8gDoVaPylWFoqSEOZPGr73Axj1Q68rIe9uscqWoSZOfw8-N1kaLsE5ZXf4HVnz-VeknQxpTXekq5ZFBWWRCxvQRofYOgeIzxU5QBkPH9ieq5O2cSkWUUp4l7kLV-0jxIC-2aRhwM1gCkhfXp7ihzR6b1fT8AvOL9Gdvyr5e0fEvc0jNzmgdpWYAhMQcw8rHmKHHFaEzxsIvAMEx7uNawj86FcCd6AHL7UwTpJc_t5M7uzULmSMmll17mVr6F0jILVB1LgVQFWuoZuv9_5eVSKvgCFHxb3om0EevuVqf28_jT34rIpVoEfK-CdeqNEUII5YdqCgNgGAYe-JpjtOTOAUku17DYq1MbdPyh_wG6p3c-A59IpUY06hUABu1DtRtQL77jXYdh6obsFEJnEqWVWG-1_9-8uL2-069Da8m_5sVOamW5rK8-f_3fpSRq6QD8X9Ml4Pd3N0JwxNWG6i8QUzQigi7WG9_44ZnyLPWj1A8i7odZmFdu4pbgwLixXhIzBW6mf820-DdWc_z9ao6Hl1bslxYE3x0vHLiviuKjlEqAi1K6BXjoCbiLVVGGQcZZGnhB4cWZF_OMl4CzEtdzwWP33NgvE5hcyYosrLwyKE68z7RSInnnuudReh6FRyolWBzEjLm2UsJWSthKCVspYSslbKWErZSwlRK2UsJWSthKCVspYSslbKWErZSwlRK2UsJWSthKCVspYSslbKWErZSwlRI_QKWEsZKc53EcFWkyxiyNvJ2p9x6ZfVORL5f7WZpx8AC15TcScqawPzWtJtHmpXzbMxjoUmZKL0VGdnv3fuW8GSQwRkkAIaYaCcxXH-S2RShGvTBBDDB3GGZvu7uXgMlqcpkB37UYqKtJ7Up8BycRLhKQQI-HDkfv_Knt1mXoR2eU7BU2t0eMfhAXumjMwJB2bZa4Wnv-zQI1mczDyyCABFALLfAySCAmhcuMuZwNgc1RqHtpR9DpJ5fm1ALA0sG4FPHrKfgo0-M6_6_UFiJDcNUIrtHLntE0zmiWKB4ALtDSa7DaL_QJoxgY_K31Mipl8UbTk0LXzSmfJMnTqEzyMNYo10i2GvL31JQpFiWQxf5Z6C5ItLTX8R5OS8Pqs6vtsIxW8XINHsR7RxYSLZz3f_j89e9fvbkEp-byP17_j_fKd4ctGsDyw0DNTd21DYIAFZJ6X4F-xowUss-V56B61j3HMfstEtGtnN9JnSMxnSwKgIU2KgWkG0Mh1IV-CTjQQ1u068WhNRzrKmpxeiaboNQfqh29fGdy6Yz4EkrLLgfLP-yE_4lKd3UMcyyO5RLEEpjhfvB8QMC0CK5BNoXihg9FQEgJsQjuvkRdPVu8IWxtzkG1UmpICTcJnnLHtm0Lml4Z_lrWi8jij_0Eui1KO1WURs7MWJQGW9-Ap_McFj9lpNYAF9cODkcWebmttxyLClTsc6ye2LQl-GG8_H4J7w6fclAAEvLSjxhPPyannjKldGYJ-XXoo44mXKGKAxA5M9EKAyPguB9j1xLrrle7a-9nIpm_c2ZPijzmLk_TjzGPV2uMdlW8o4glWvKWNNSYEp5AYXBOnVdvnN-CqN0-mt_rc9wSAUY3-1RTD5PGvOBVGETpg4c9xuGDcuFJNxrs-OdvnZ8FsXOTyMAlspoO3U4kZEnR3aQU5XWGOdYl5gaAJNmzZ-aL5OTUW0SG2HWLccozUCv1pl6Lw4DuftttzPKTI_yHLM9KFj97ZoEoNiCsJN2LKwx8iwDu-3zjR0s0XVMrNlf5VSQhi_nzdzNUCgK2UxwALDmpwO92QDGvKWAFmuQW3Ac0GgIJ_GlmZllUFCzOkmfM7HtiknsUg9UDlO-juKcOxzsgjXp6Nd-pyZ6o4B2N4OH9uowW7avKnlcd_WFW9O4py9HKrE7ZwJPPMguG4VQsx0zAoc2hCWFsR0czTxQKG5bxeM3uqxIDHRRvpOooZGvG7FN31rRLBZeFEVidMmUzI4tg2a47vVDCzO4Nbtin-erqURcbKteIb1Jtdb1G3Xt8gQx7MP-kU-pUuBZHVWrBV6c0_Pyz_u134OgeOANv3_4GBWNMEa1Oaen50U_oN5h2SYnVvb0wdOzxcX8DLsZfeS9DKaYTuNVaYIz8rU6pyeODf6GTAVjZ9QXnH_DsbWAfaeF_-9nvJn7IeFR0Jc2JgnI6zOB2eiIhtH0g-tUm_WHmtWcVh2ld0RvghMfFOdjKh9edR24UlmkQVV7hMVDmeRglqef7p-rOdTHtA-rOrWtgXQPrGljXwLoG1jX4h3ANHt7Ttd_Ski7Gcc_j7463r_wg_TqhlwEccEs3TPI04HHFEu7mRVi4bhkGlRtl3POYV7lFBMqzwuKVjIfYyBMVbujzh7zcQfNOfO5G50F0pHmnKrOkKkP-I2vecYOiSN0i83Mjl3qkeefzR2DBH3EvT5AXmRekLo_ze3p5FPg1HjFQSa3qdxlRa40qmVe7tcNEwd4_T3DsP1-AfcPKprYyLPs_Sc25FJWa45JqLEEZxlom0zFFC67aum2wPQjejHd5y7qStONzunsumkl7j_O87p6LhqCgEgpsWupo3XBoWKG1U7KBLWEVNmNFJ-VwKCvyX__rf8sEY4klBwInokTB52M9oAhc0IfKDJ1hlRM_W7PbO5ysjgDQjXj5RXPVse01faCaqQyHFT-ebJoYnfpqYRXwD5jMsBxvuWhMYDBXzuuX2INUZLmry7gNBG4kDJ-KoNcDlfqo7i_YUurJcLa7HJTs2djioHLhC6pDk6IlrnKoYF4kaieSDaOJZiKs4jioFZorGCt9zgLPLVmqq5UMQH_QlPFwWK7KLKuiCgvw-WI3GSvSNFJXZZbPwNt3AkAwEQyimheKA8lQk6NiQStUS4a4skn5quiUocqCLas71BUXzfu_Yhp3vVlGq2BZreGN3ouKNExRbjlmsQdR90E1kV2NqJSq2t6r5G_frt-_vGim-WUZiKNggBZfuM95X2InOucfztQ_ljeh-WRMTo5BA_PeHkMKL_XwjaicusKqWPU9R-TsBCsP1xK0gEoak_7BkgKxcAu9ZAu4ESZupIapZeJ4hniaHj4zGvRtO6FtJ7TthLad0LYT2nZC205o2wnvaVFx4Ui7zAfFliez7YRHQ08znYUAK9LEjfNg1J9G6NSMZz0xEqrAQwZosV7D8VDFnwaBkhfQfkn8kESwfjlGwWBRNrBHMBaBtTVcXtwVa75kt7ihAO72_K0FuWpLOG7gcF5R6o2O_pkygfoMLCjbtIdwF6Kik7yYEcx-0a5HQIvJn5Xz1pifWGuEi0uzvU0kKgEEiYJPUkCTjh6JpnSjxriABNLJvvBmkGs4UG0bIHntY38uwbLcZhrToISS7QALrZiWPR-BObypdomWag_lV6LcEw4KuI3CtcSBXiKMaCnpqh9ZI7ItYU9342hOJcvyhbO7oEVCwIdIWbQ1LugUAQocqM5VOKJGiesFnI8PfOxKnfQQ7J8MHiVxnCQuZ2MPgRFin0jw0yLmhdh1Idd-CBYbi9KdX9CCie4pcctSy8yCAAZiClhAVJw35LuiiuTl2W3XNldLwIVb3Ae1FmdgW7Ab6wyWEjQVL8XQ4G2gItc_Ci0WhW8BWqNve1buqDN3ABkHod_z7n-JCq5iH7gqbT0TcRXRHjgaM2xW0vMDewd_YMB-YTppKASiLlm0VKhd63c5NkEoJ1_ummwAQJXTC_MGztUXIoFqdI6g0P6Vd61-tmymW4xdGGNQRLYI7MyK9c1ukC0ccjuULyLqV8UxwqmPcHlGmBiLvDwD5RcF1ehp6KzIRJieluTYr-IFh1rA7GXXVWSPf0EGR-JskFcAMldNi6IKuzktJnCokVhWyjoUYRva7dJ3HbShL1XNdsmXWkpUi9uZdDe2VCENoF_oMdSzMCWsTvgX5__9X-_sF7H7KwTyv3w_CSk4Q82XOcAM6vlDV6DCPTV8EnxL2l_YMITHiC4QVBG8fOnkuxpe0xMIeiwBoI97xz8LSDQozCNqjLHdBvzJrrtbbmsUFVHEv51oQRwOVdZRnfev0czOx1Hpl1HlRm6o3WMj6zTZ-aclkZTZI0sntt7zHRH4W_bD3ZrWkC9R6Th4DYVRtcklw6ZjkAswwWCAAdjBiYJlKeGogpk0_karSZHDJUqoOJT6I-zjWY4HwvkthRixs3IgOsGLBuNy2CTS97Ij35FJGoUAhU9v4EulSDmI8IZ9Ld19oTUuADTd6Lbz_kxYJj9cuK47bpZ6gtD-v1Rxm4bCQMJDFPUjUyWnbDI2sdPrCbVCmA0lh2LY5XKEZ2dUbCV0yEAxoTn7EqdZxOIqCCuNkIyk38fgXpBdA7hMZrjogJXBeQopg-WOsNwRljvCckdY7gjLHWG5Iyx3xE-NO6LKeM7TIPITP_s-uCPQXdjnj7ho2sZ5Nn_ExAOciX67XuXlRRZxP8pmuSOkqTlTdOKj2YLd81z3E0EaMeMAUfxjQCebEpUNGoACFwerN7DDvHeuAVbAUghnj4gfMDIGC5VFnzifvpHsFVSJMJJZUE8r-vEj98QRECDz9hshzHAHOQWHU8B28ltydRc0gVvWbZYUjiXDKd5hg_bLi2RUSp4gJqN0xh1k58ZbaMCfuyvXt7wUlpfC8lJYXgrLS_G35aWoSj_lHs-8wmc_PC_FTHGRoqeYVFwJRDatu7poxsIry04xZafQYe3HMlSsKEGnq7mkjFP-BvOJy4ptahzErP2SRmKGooIfdp7J17N0FU_9DaUfMV2FUeA2PuxI2dzDuyCMurOnjTgGTtSQRr3SR5rko5ufzAZmgVphz7584eHCeT7I65cvEkQfcfTiq69OPzcoopTzZNra9G-yaHk83nje7ul4O3nTXAOiyyI3D-JnPh0tjecvCYfepNPMPLrI6qQbsTqNNmf2JAmDNPf2GoWeNruHdy8LoKYifHNinZZ-yD3vI8xOQHqqHBCPv2Yl-Zoi8UWKmBKlGBai3K8olZhtmeNpEbvZR5id7CNAi6BydhJvCZdWJItUpT4gLVGaVcy1gKVl6FXxc-XuLUcsBreoEm4N-zgVo9U9Zl9J1QpjD5NHw1g5P_dmZmfkesbZjfOQYc_vrSHt6XQNnwrjIWKxKm1DMA4N4VLm3QEFYPko1VPBxypJnR9d_tUp43ByEl9gkUYvq8cBrSylw2lEzvoteH6V9MoJmhPlg_4JtOPG4_RrCwEVzyz2rACOr4uazGKmad7d_IbabCYKY2QgWJ2yQ6dnt2YYcuUyYaPKFGQ1M4Ysx3IFUagy1t1KBAhIDpGsKL09skiHJA73LJKMIQBQuKJOEUM0cb08f0y5O_G0tkyGOkXvAceSnE40rOi4qbADWsBXp87WwXHSpCMb-okk5ugSDOV-wZOWZsEWHhjKX69OGdUZbg6mq7z3f3lp7ggYJnP-pwdFg4fp1lFjx_JKpOMmNnIE4cWasw5OBWVxeu066oo1s7hldcpa3j-xMYP1cMtocDkY7BLHLeL9MyAzpgVwPIymKFJVHzaSmZ4W3fiXHaOiEbkuq1O2b34eo2XD8ga-2cKI2sZJ1d-rUmPpSk-0uGqTmeyzKmjRPVynTN_9iyRM1xg_UCZsoaNwo_uq-F0WIzmOWa_hUPHc_b8vKVWDOgICj0zjGeaPZoJqAlnCbA3NbjqJI8hBR9ll3y_-ItqaDrOmDXo4D0ic5gVjcRbEOahMvywSN839_CQPiO7L_ZHxgFify_pc1ueyPpf1uf6GPtfDOab2qSJikyoiWujJnnvfHWeF-GE4MYrc8-KCeWWc8yDJ3IznYZbHecyLyMfW1jQrqyQqeBGUsPI85klRBGmQwZOK8tEvus-P4WXnvnvuHePHiPK4LKsg-5HxY1TMS3BVgirzPio_BnrZVKotT9ucmbAkGZYkw5JkWJIMS5JhSTJ-CiQZcZnEkVcyr0iCeZKMEWr_ODgyUl6lXshz7iX-35gjY1L3eMALcdigqwgysApYuHiy-Z24KlTr7kNJK_6WVBm62EHRZdD7TbgyqMGgxsosAAfEkFEJ43yEh1b32H183ozEZTyKElaGAXsyb4bJl4FnArvbO2dSJKIK9PCUG5kBTN7McWw491NsgIU2iknu5dlwTtFsXDSWZ8PybFieDcuz8X3ybBRgmP20CCqXuX8rno2V84eGm7lNsXm3rBfBpHJsNZGJ0AV2CtwQ55Hnj_mtSTpVqlfL2GEZOyxjh2XssIwdlrHDMnZYxg7L2PFkxg5LhWGpMCwVhqXCsFQYlgrDUmFYKgxLhWGpMCwVhqXCsFQYlgrDUmFYKgxLhWGpMH5QKgzDsw0CN-dFxDJXx1yNBpRRAz-ml0SNnWUBaPIw81KN_Yz2EkP4n9opIgojxQoLVSN2Aq4G57nfVeBA1Vg3T6j_UmQY-_eq7ndSuydK9q4oX9-30p-btKjJYAK5NkYbIOyGe-YBNv31WA6jFInqP61w9S4axLFj3EsFs4zyMYfsM52ILFol8SdYmNC1Sqvu5w9FbFKEOKawuN-JwDEeBw-m55mNIyomJ_KjK-f3gOhRucDDZUs24hYjVU2uFN2CuWUd4qCFgkXFMJ0MPOLq79X_zUhfwEu3ygvPjUMtIUaLjyEhT-3WKR0_PPNDgWnOQQFR0E2Xwy0wFITlDZiNRt8CnyO_Mcpqm5u2GAtJUMrMBJzOxd5iiMFbuS8flko7kUZTIWdKpUmgv5cCFE9Cn4SsKobmb2EPJz9nTg6UiIBOfwETvdI5m-VGvp_kcRFWri7ENDqbjE15apPSGMEBYakxeU2RFWEC_ql3_HT5-a9_o8wG6Ws-jO2sGAjfUPRyXBaZtLqlCqWJ9DnThqXDPlk8wDQ5EiUzSwk7JBT9USSgM2n77b4ibXasMRjzrzrlrxzzrY4X4MUqjEUHyXngOcriIgi9xPXjqBoT8Lrda1ro86TOLUMr65_LomCWCijjvTtMhkzalUURv-pVJomQ2QeReJJlBiDVWzNGJqRJbhWcX9cpOIj9SyeEjaCDBQtqaCyhqiiPjw9aOMloXMWBQXhA79XqYqpotCMkuBXX3j7lzS6ks5SvMRlA5dO9nCTAGjU7mpg4j8r6CiYL0ehBzq1IJ-L0pKqWUQdZ3A9KdC-FiWmyRwtBWIJXCwe1ZIk-t0ZXnc6SPb1BzltliRd4SeyqFIs4uT8Huya28De0zKBVMeOCfgHBN8qZdTs6smI7cBdHy1VQ7ELjO2V_pezl2CoyjNGFI4vimC1AC9m_o8DdGGQY31A2URhVxDK2ioWH68HsSbloROzhiXxi5Cuen2IV2_t2j1vs4NspwxiFes9B41yzrhwYgK8fB90Yb27qrm02BLwGUTV1jHWM5v9U1jGjc2TsyJxvTZlv08Z6WXe2Mfs5DeGnxjTqGz7emB_9d9if2x_-EEqAp_ROP2DcJ3U9P2DcJ_UrnxA9U7PCVz8P0pUbuq4fJVFEtAGoYPGL6IiAHudjMo7HSc4dg1ZDpBSRv-aWLNNnyi-hkMBSN1KJ0jU6UCpMI72zYWq8H88AZMxG6H3DOwNziq7gTXJGHqL2RihShn1-0oNWrQfLSUZPsX6sTp28k3N6VYoJtR0r1lyiGTLsFI5C5KtLwk2eJIza1yKHL0EroHBdbiI5rxTsW506vDNLRS6XWHMBbDCeMIkWYNfcGBgQkR3aVSPAcHjHfWRCs9s2-lzKn5c45xSbkJw77KnpRB4npjlk75mdiwTXS13i3GB1P01qNPoSfxXtujzDrIrStgtzdiM8Pz6xQzqf2YmhW4bboLEeOQ-VmTwneJyc-emEyoYKYdfTzP08c8_sPCIXcNF6zTqFr0ZuHAH-JJPPGHUrwFFm0vcRJ12nBcA9O0ndI0SVCmPREV3XOHsdmupHGR3FZ18bHREjwz1fmGXCC72wC1nMSC-nK2Mfx-CTVVmQwb1x5MUMUFCUJ3kVs-IUg49mDrifwcfiF4tfLH45ym0yw5ulKT9Goo_0u-PcHT8Ii0nM0qxK0sCr0iLx8jCr3Ir5eeBGQQYLkBRFCG8TZmEYpGmShSmL0oz7eVxhEjJzT7_SlK8kfecm5553HsZH-EqqHAQ69AvLV2L5SixfieUrsXwlH4WvpHTLLOWRz4Oc_fT4Smp16Fh9tkYoHaxckftfgiF7r-f3e3jkwMREsDxuBN-SZeSRBCfOSX4TrEx4MMEJuaooHmsdC9YMGqqrBBNex31Z9SBLgmJJUCwJiiVBsSQolgTFkqBYEhRLgvJxSVDyDBx8N-S88vk_MAnKZzTWk1lQPpPRzCfRoLzTPyqiapmm94jU2UI1OBlrr0ptx5WWvySA601riIWEwqTQW0w5V8QET5GuOEc5V0xGFVnGvk-q8nKS0MMX1qZU_uiEIFmRfqJhKzGrhj6UrkffL3N8IFsL-ClH6Vqcx7K1YP3uCboW55FsLSNFyXG6FseytVi2FsvWYtlafkC2liJ1eZ5mXlIFP162lqkBltQsCyl-cFjfBvGSbKH6xmBweRx_yzuswB5FTxSBysIR1QEPq92udYh5qatjR_RDpSEaG5yjkdWDkNEZa1DUTESDoKhIMc6V3lJJLQOSrrllnGdTy2Dh58gt48xQy-DrIWOKbKGgpyxF1S9YQFV4_EsBJ45SzTiPYJpRtZ-zVDMvD_YFh9BoUZXnYMcqBWX36j96S1VjqWosVY2lqrFUNZaqxlLVWKoaS1VjqWosVY2lqrFUNZaqxlLVWKqanyRVTVBkQRp6Ve6llqrGUtWMVDWUnvx756pxYQyXuwFjMZ_nqjnaKnmMuMZshzvzfJMUw4sT9HR16hHOrx_EByXICwcQvJnuo-R0mB1QyKAJRCQsvDP03LAIVdISiKMiOtrEWVhi2Bz0vJFZ3ku6InQxHE0jNqHTxJqzh5oyEZyuYOEx0COq-kSIDN9-5cLLUuZ4ianNo7-QIas8lTuLoHgpbNq6rgZBO5OjLgf5fzvCe3g6RemP4mxwoWFN3FXsHYLbxcwPZggs37U9d5CDR91xPMuLU7to3FUSRhHViAACclepH4IH8Hqf6UezE8GaUDnByPiBSqEXrjnaKZOvxSTYATdNOI-cdesajtVnYlyByih4p8IrrYiMXTSyxFcLLp5JCa8oHmFUsGnBolI2S9zzkyLu8XkZs9Rzq7Jk88Q9IwvMAYUPpR5RwLJgKW3ihnrAKbU_qFoQsZx0t-MnIo8r0v3RWFEzRr8KOE099eAq9DCIhB2Wz_sJjsT762WBGkOlNLUkvDxgxyJ9APslC5XAVNIDlnTnRaMC-f8OMBZ7WPBqd5UFXgwPHJwP_xItRELwuNoQl6duFE_S-eLjOI38hYl4xMdREnorY7dB4kER0EPwgqW78nw3vGhojaae_JfwZRD68cJxv6Lqgx35lUJ50uG_c64BI3mpewb_L5GKWCt81_bDTlIsIYuNH63COFwKd5zC3DjXxFt5bqo_HcPeL8XyjT46TBHmi56560dujJk26crJyhJDSiX9GrKssUKko1U0XVyESg3pWFpjZbQfneNZ5ARyjgSB5qKBAMyCMs7Lqng829G03drQNik2XEs2H7LRaLU9H3lppFGV5Acm5VHTOns5OFHgg1qWNDOGcZZa815IiLDD7RfWVsZbhf8tzwYpIZELNSaY6Am-FJUL9IBJljsHZSla5hRc419fs10_aIIGqkS4bZcdoVMZqhBn2WRIWo3w7Fi2W03UXflJkqoquQqdL6oq1XYw9IOAcO5cMl73nmBnxv5vYiESlyGsJe86TIaS5ZD53DvxoXJvnH8Do6zyx7Q-eklAeMiqYVCReuWw3IAQjEEnKDr06XRqiSmNuJnRxbEH6k3cTn7oljL9Muo9plpoA1fOH6YJaEVcaNpig0BKdvaIZhoRnroXLYf4y3R-HlVelj2FDoqKppR_Jhq-hLt6iikKREhTRZkdwGaO0_l59FCmKKwaU4cRQ7_6GO55WHLhJHvQAeXaSOY4YZMyN3Wyj9iL7OATpaNpkCHgtSImSuOJ15gQIVC24NxEOSWvGEIzTPWhynx5WMwgPqffDhJlIXt0GSP6Q-l7aahLwwOXkXO6Ahs4j9CJma_5csqt9VMh0_r0BI3WpycItD49RZ31VpBmOe9-PKxZoKaqS5AE3n0fdFlJGboRTOPBPA2sLGkaW5FXhE--PDv76tz5mfOLNj-_ya7B-cA2IwxEEHL8pejNbbC8R_QjC0BJMbhunkKiyhN62MeZGvexGwXs1kbOSWSGlnCabjJHfiVTeAAH5sgiyrzyopB9zKmN3EAwuzfVHiBBXcClIfL8makZuTeTJGMvn_dwPggj0_WU8XS4XC9dERY8DfmDxrtv2XQNFiyZcqqXYgNhRzdktgTPzE0CRn7uNWM_TgJqg3w47cV905MN3-I2KXMwL6SJFDESMwH8l93crnrgwMVZ-FGnJxyVyeyw4cQ8wUaZy_bFgwjGDIWyN42ROwvmPHmIthBL0bxCXhSo4aVgqzI6YAwCLWX_O46RdIGpe7AONKKMNa1OKZS5qU2da6EZsCGvO0LJBA_cksyuTumHuSfpt4EZq7DZa_81jQx_E1MWaiXU4zcn1mF16nTNPRheitbY2ISlCtRPjuLe8MYpOT78W2lnNdfBKOvwzOn6qXC3bAUdkxjjyh5n1jIOwwNn4ScUyTgh2YfMY-MikL-6OqVhTxJqfSq7vyQyVzy-rENUJepdRF2uUebdzh8KdI5Wp1TzaaY6Sb0rJmIKNib3ZSj1mBzo1gLVwE09E2aM9gSz1x9FP5wIRh7o5FNiN5VtUcQnHox-CA2mRcogP5tKlG5lfQyXV1BxVgV5yvzU99Ki8FlaRmUcneLy0qw693N5WXBlwZUFVxZcPQ1cPZxzUFOFiUmdxwuDNMz_7jgn2A_Cg-aVhcd4nlVRUURZUBVV7Gd5VVaFX6ZhxqswzGMf3oz7acYTt0j8CFRTEZV-xngQPeTlDhjRsnM_PnezI4xoCffCxM24ZUSzjGiWEc0yollGNMuIZhnRLCOaZUSzjGiWEc0yollGNMuIZhnRLCOaZUSzjGiWEc0yollGNMuIZhnRLCPa8xjRctePvaCIq4BFo6-lU8Ny55-V6b0h8p-WCpxxxQ5LYQQgLGEBsL4ZYJSoxhY4zSgnMaVprMFZosiRCOHvdA3y2C1xc4XFRkaFcYNkm5ns8zvw-4xHEDYbRyfQQME0cpmJAgaTS5q2CTRYTl_RjQtZH4CXXa3bHCC3iCgIZbCGFdINPmS9etnLKHhMJC2SUCrSBAJipPYDKtIY_QMx7JbRrxz37ZpqNCkvoNd_JG6ABRaz0T9mJksYsKaFSBVU1x0cCAyX4VPlHfQgclDHVnf6BT4HnHGBZGWkGVZWea7DLO2HZeSzjHyWke-gK67w3aTkcVgE3DgVqirmqFZ-ZJELlpiQypkUT0ykCE-69jiO1y4QM9BCBduONxCRmKnWHFoJqljsVd5POYd7npfhWiGUXgjJ1R3tOCg1_cokhqrMWjlf6ABx3QtA0dIW18U5Uc5QsOEQt3eic4B6euCSA0dg4aivTnsQJHjyGYTfx-oUM7Kue2sJq-VcEPBIqpGDyjGsNpSGRxViyt_VnOwWjo8FmiKFP9tymURpgk2XuWZsMeqaTgnXY8qU5I-WoloUGhYnNvbKkmK9ScjNU6p0Rs2S-Bp_mMpU_Unq66IxDJVUtOb30woXgRJ1W9P-D-XCYOYv5RrVvYdtTwI6vL4RDYnyQpm_QmA5zVMrvWhks-jXVRXLAJ0GofcOVRyI1KtRpx2pxBXLrPkEZXc4-FN89NiMRmR6zZFoyTh3SisrnQ5Ohvod04M-aFnwTPnzhvLQY3Zdt71ZClJLQWopSC0FqaUgtRSkloLUUpD-I1CQBkFeJoUfhEEQnqYgPR10ehglqTjwomsb4ByqA1WioHhJnSfRkuJII3HRg2lJozJ3vcjzQz__QWlJT5CCfixeUgE8zWAewRzRCUiqmFSLTpCc5DGlOTyGy5QO2EkuUxpu5DOdSaNnSRnmLIqDLHG1Dh4bM476fo_stQBxEydwIm3KJ9QRO2Q8xeyj2jpmNn3JhC2CPDKm-irf_eTQH9HtlkxxdpESqTHAensNZnPi74t2deET6A0iQo5-j6bjohEfK0aLGvn1GBLwHZBkkSMv_UIU28Vh_OCiUd6-fht3lbmqNIXkUbkeKovTSmbYDdYW1WRahJ8Hav-iwepBeApyaG6wzFHkP9VioMttfm5iD7FLqG0LNQbFjk0CPExB0M7PljpaultLd2vpbi3draW7tXS3lu7W0t1aultLd2vpbi3draW7tXS3lu7W0t1aultLd2vpbk_S3caVH7AwqmKddDT4aI5GYx9JLXP8JOUIAqVAq3osqsjfJ7DDEZdrHHF6iFYK1AwKLIXJJ6OWUFhA62uzBGy8y_dXAcZKpSym6coNPtEBH7nJWCekJGRlDiK0L1iBJDqC-fCJNEdQ_DFG0OmdKaSOEQ5OwVfSgS_FV9SjTjFlLg2Wif5lMP4mGbWtsnQihrCP9zVgEYfhVMWZhBtjygFOZiKUtgrN7FP8jSXgJvLQbH8jYCWYikQ96FuMzkB26Aep_vrR2cBMU0OnRpduvZSRIfIrj1WqLSQJiYoUYuW7AIM3fAS79x-Lwg3yoEqqwHN1-7zBg3S8Jv1xlEaT8vTSqLpKJj0NuC5-dNEcwiXqtjoGliR2MSumRbvDyRSfkD6YI78R8gyoxjnRvATaPEbH9DCzhN_F8J0-5XRnv6PyXCGDiMb2YRqJEgiKOGv6vIIVBXcEb0IENFZE8U76lrCfIjcmqSFEjZDA1eBrnXnBJE-GIiGL7iuVZts1NWAaBQCMQmMTz3XYDJYJhJb6Ky8Op7_a1xP3tQDua0Z-wQnSbfmmE4kYvfl9L08hpoWmFzRiSLShYwBJAClR37mhin8zT2vpzi3d-d8L3flX3_1_3ycL3w)
