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

[//]: # (ob:e683c14a)
[//]: # (ob:v9gatediagnostic)
A frozen four-task follow-up isolated three atom extractors (Ling, DeepSeek,
and Sol) from three claimability placements while fixing the DeepSeek proposer,
Sol verdict gate, 56 requirements, and deterministic retrieval receipts. Sol
extracted valid explicit atoms for 52/56 requirements, compared with 42/56 for
DeepSeek and 29/56 for Ling. Relaxing the pre-proposal gate increased the best
supported-requirement coverage only to 20/56 (35.71%): 52 requirements entered
the proposer, 49 produced normalized evidence-bound claims, and the critic
retained 20. The diagnostic therefore locates the dominant loss after atom
extraction, in proposer claim shape plus the all-or-nothing supported verdict,
not in PageIndex and not solely in the atom model. The next candidate should
construct atomic claims directly from validated atoms or split partial claims
before verdicting; another unconstrained proposer swap is not justified by
this panel. All 36 task-cells completed with fixed routes, no fallback, no
missing terminal cost telemetry, and $2.219572 total known cost including the
resumed attempt.

[//]: # (ob:4177427c)
### Model-routing and deterministic-claim follow-up

[//]: # (ob:4d595ee7)
A further frozen four-task development qualification separated the workflow by
model role instead of swapping one end-to-end proposer. The tested route used
Luna for lifecycle-aware decomposition, DeepSeek V4 Flash for high-volume atom
extraction, deterministic atom-to-statement construction, Luna for type-only
assignment and requirement completeness, and a task-aware Sol claim verdict
gate. Risk signals and legal conclusions were segregated as analysis-only
records rather than admission-eligible factual claims. No model could rewrite
the deterministic statement or its evidence binding.

[//]: # (ob:5d3e6e23)
The component results support the architecture but not promotion. Deterministic
construction raised Sol-reference requirement coverage from the old free-form
proposer's 35.71% to 62.50%. Luna type assignment reached 87.50%, compared with
69.64% for DeepSeek and 91.07% for Sol. Under a fixed Luna-type/Sol-critic route,
DeepSeek atoms reached 75.00% Sol-reference coverage, versus 48.21% for Ling and
85.71% for Sol. Luna requirement completeness recovered 98.21% of Sol-reference
open gaps at roughly one tenth of Sol's coverage-gate cost.

[//]: # (ob:1193170b)
The final blinded paired semantic result retained 100% requirement recall, 39
governed candidate claims, and 14 analysis-only candidates. Honest-gap recall
was 83.33%, below the 90% gate. Unsupported factual claim rate was 27.78%
versus 32.82% for the paired v7 judgment, but the paired 95% interval
`[-0.1670, 0.1124]` did not exclude regression. The preregistered stop rule
therefore prevented the formal 12-task E2E panel. This is a failed development
qualification, not evidence that the E2E workflow improved.

[//]: # (ob:4a6c9c6f)
Across the new routing experiments, retained terminal receipts establish a
known cost floor of $7.243647. One early failed attempt was resumed without a
complete aggregate terminal-cost total, so exact total cost remains
inconclusive rather than being imputed as zero. The sanitized decision record
is `MODEL_ROUTING_EVALUATION_V1.json`; private claims, quotes, prompts, source
paths, credentials, and adjudication labels remain outside the repository.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzUxNTM4OTg1MDI5OTJjN2IxNTc2MWYxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImU4M2E4MDA3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83NWFlMDhhZjZkMjRkYjgyYTE0YWIwMWEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgzZGY0ZDJiMDhmNGZjNTQzNGYzY2RkNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfeuS48aV5qsgWlbYHpMs3C_VMbHTI8te7ci2oiV7dsOl6E4AiSq6WQBNkFUqW4rYX_sAG_sG-z77EPMkey6ZiQQvqKtkeZwRM3IXCSQSmSfP-c7t419fic122Yhq-25Zvzp_tV6_S4Ikyos88cOiCKusDJIsDZqgeDV7VXb13bt6eSn7LVzbX4kwSc_zTGZlFhZJWskkC9IwEmHa-FUUZJHf1BUMntZBEpRpJkJRiCDLwjquojwXWZxGDYxbL_uqu5Gbu1fnf8U_tu-24hKesBJbfNQM_lHKFXzwB7lZNktRrqS3kTfLftm13hVc323uvPLO-2LTdc16I_se7lmL6oO4lPhSo4833Z8kvO5ugwNebbfr_vzs7HK5vdqVi6q7PquuZHu9bC-3or3MI_9sdPdG_nm3hH-_2_Vy867q2l62sBbbzU5-N3t1JQUuoswjkft-9oo_eSdv6CJYXPkuS4T0c9GkdRjXZR6KIBalHwicWbfZ4qu9Wy1bCTPXO7J6l0d1E9dh6edN3FRJHMVNVNV1xq-jZveuEut-t4IXDnGeVbep-1fnf_zrK_X4v76CXe42Pf6Lv5b1uxKW_I-vqq6W37z6Gt5ASwM8uO6q_mwjt5ulvBGr-Xol2v7s7adfvf3s0z-8-fzdm1---eKrT9--wz9-_-arz37328V1_Wr2KHkSWxi93G1hG9-Vol_2KFVy1bwTPSzvVtJ4u-1Vt8FJf1i2OGR_12_lNXzTimvcXZ78DG7sUR5enbe71QpepbqCDZS8BOWqqz7AtWGTCSGLHC6HvdvKb_BF3-p39EQt1lu58fCPncBpef_xP_-PB8u7kZdLkkQ1CVHXNLs1iqG8hU8-8h4-DvxP7eGCwgjbuzW-BQoKCN2r72bDbEtZBFnuJ6PZ_lJWLPdbEHz7Cf1ujRLUT07yI-8h90_MSTRwhtPYf7k5fbV3Tw2D1bL3bq_k9goWUXhfwGH4rIVdnpdwpmHp9Pouh7muxUaMFy9KfN-vytFEP-mu4UIYgYXovrU6cvnUdsFeBXUUPfmJX11JeyE2u7aHFZVeD4LuNZvuL7L1lu16t_Xg9K53_czbiv6D9-cdaMWJlUjjOAhlVTx5Xt96X9JF3rfeJ6KtlzWoZe9StnLDE_0WhEquPTi5oFj5g0-_WcO_YfhhXqTbRhPL6qoSdek_eWK_7Tx5Xcoat6L34C4Pbt16XcOCuGyX2yUcx4qGXPZdu_A-a0CgenktJhYsi4I4rPJ4NK9fWesPz2prsECgfOtdtSyXq-X27h5Zesj9E8KVZzUozZec06eiukIZ85StOJ9akaTK00hEL_f0uZJh71q0ywas_LnXd7tNJb3fv_1sBsYcRIyRxsy7lvVSeDi3GT1mmOgKlbI90TCswLruyfqzJoqHUk0V76QTp-fMMgfABZUf6iVl-_qF98YD-zOlnpomS-KqGU30N2hBqvu00nDVhLzIpimqIH70-G8lKmxQQ4DGYOHxeu8WwJHX7q7xvHebGWjotgOExH_Ib6rVDt-_n028bhJL4QePf91v1duSjmnoQJN--ferO2-5hY3Ygh3ovW8v2m-9-Xzujf47qXuqpk6btHzshN603q4VN2K5IhTKMjuDzzawCfRRs1zBB93Gu-xW9ZyQqyeuy-XlbmJ9pABlGPtjuX1T_2lXLytWsih8ot0u5yspENd6eN2mW90nLQ8eZMroZ1GdJGnwwrP7NSyQB49AQeKjVMEqotUoZdNtGOPLW5iNMgZet9vSGb69mljLqkSHoxAvPNtPWAkoLcW6aWSCJfylkQkM2MCOKwNZT6nWOorrLA5HswVH5rpTIAAEd3qHDy6e2Elw04o8TconPs0gMTh5oB7AZ0Nccg1KYA0LcA1-hoV-t53GfwTZJtYgr8skFXH2xFkFC6_tQJBu4aG1hEeDcgLDAFoDTJtcrrcAC_reg82Qry_acAEIAG4GnLkCmZswJn6apkFRpE-cFlqODavT612_9fqr7pbwHFiIHawTaNQSlBfainXXg2a7wevBhdt6m4nFCsM0DBsh9xD4Cm7foAK63wEYXTohLIUMGl_QCI9_0lwj1pPGE_Zi7oHd1C9NStoDQfLa_U35eqa92FfK2r5TquKV-ka7m-Bhg4Pih1GcBWVe5VkRZVKGTYBeVNttaUmVo-0pRxtMtaw-rLtlu6W4wYaehG6k_gu9yK_RQ18tqztrBNtrtwaheMATHfq-a7bvwNJdys16s1Rxg74MzpOyKrJISBDKPEjSrAClIcIsC-qqlmVT17lIojILM1HnBYZaqiJtwlL4MglEndDYW7El_5-36zyMwU_GT16FfpjO_Xwepl-F_nkUnSf5L3z_3EdsrlYcrXgWy0AmDUjJ8Olff-CgAUknu_VXor-C6-MyrGRaFiIocEdoDMvTV4L7gg66em7VSL9sSj-u8lw_1_LZ9XOf7HOrx_hBnBRN0pR5kurHWG64esxz3OhrQMM3Em-HW9pKXrRklXEYsMOks8puB7fWVojNu-02H1adqD2Ag7vLK9T3fwI9t2zuvG5NviEY7uV2cdF-tvXqDsaH86fmZU3ruqsRIbU9qm94B9AXoLYB9g-XgPZRIBMuuGhFfb3s-2WpcJa5rr0zrwS6dgfgorwjzX-1A6Wj0MTiiGpVC53A3ArfBwsZlWY_hzDCsJ8PiwuoUcumirIykXB2AzPqECow2_d035-AB3k1ZO0u2h500TV4TFcb3pirjZRoo0F7LberOw8jZ2by56cXBMwfeBFCJpFM9NStaIKa-nPCAwr9nQDw_F_86v1KfgPobTWvrnbth7Ob4D18O7b16gqQtGqHSMTrK8SQ33qwpXAbvFpFyAwH6NmnaZbfwBww8rwSa7jyPb7Ru34t2vfqsWs4M0s6M1tYQ_XcAQX1_Eb0JfwhNuBSf4v2rFvd4AqrF8bNwZF6fIb6UD0G3p0eMnrq1V25WdbqaTxJ_Xa_8OhZu1YjkIN1AB0m2g97CPRbcp-H9QbHqbrC80kyRjsj2S2WGNFWNx1zoJRohEUkRJyCpa1rLRpWPEeJxnMCNC2-DEzVDHDRKsPCegJ0FsAmfCeQN3BEwR2ETwVorN0G_VVLxnm3l-A4dLetOk0X7XiFcI8q0aKKQoG43SxBimF1eo1P-gnNkedxmkVRFfmxsQRWFGnQHE-MAqnHBE1a-RmcxyAT-jFWYEg95iGBHX3Aq7qJACX4ZWxMixXrUQM-J1azZvdqB-cR9PQGTIvnGfeZEOAIFMLIDM3o089-OSMNdzcjD4NkVHvcODh62JbR8ox4w_8J2-HDXJDc0uO0hUD5wGFBK-gIzgwFoGvpnI2Eg582-gifxu9Mo14LPE5ybqIA74fEjIWH9FzpaCt13ZONpYALDgoX7zYYTKq0Lp2R3exaUNx4WsEfBtVKT70VK9CIiIfoELQVLJTaGdwUOiMVzEDW_AbCU04Pvgx4JKBFtosjDpDGN4Ch_aLKG1E3BlcNATbLcj01QAYotx571LOLVu04bS6FT8jKj08rSMkGR_daebtnN9HPQziwheEv2lKilmtgLHgSwOmOnL9lt7GjWBMnOy7SMkOAXiWVsd5D7G442ZNROTVYHedxEoA3IqtQD2YF6kw-6ukhuEFQ1ZmAV5YbhLx0-jyxRhCAEjrxzg2ogzAOijopjW63AnjG7D8jNIcfGkMNBwEE-V8-wJe06UogYK5gUdFKkNw3yw2I7IfhXKA1hX955njBv1D14cWb5eXV1jzhv_ADtXawnieG8zY2kAoUMAgb6Rn11OX24HHgMFRSPevPO_A1vRKwA8ofhh4IGKhn0bc9HgxEy-JSLFt4NxhpCYK-Eks0XbDKBFkOzTKDaXquim_gc-hdYBFAGsB11O8MgE-pwI12Qr4ddCMNrvWNuhJHFlvtmtBj6EzTvLwzD5ZuNMBwHwx80y3rngQQBBJf3OwNSbAelPd_OlRD66U0pKgquabAIOvAj6KCY3aovc8AIiy3_C7q-m_h3Ih-B6umXZGuhTngYbgEw37HE1gnPty8LhKtPeE-2dbzbTeXraWArbeoB0BlD0zalFCNNAaGlx-_wJAGLeG3g_5FOVuhXnvzxWfDVQiEVhJfRV1_LT7gVm9ELedd0_QGxU-Cs8JvmiSOAZ_lRs9YAW8dEn1GKBvXENAWh7dQsYNb9n7ZakftRr4fMBcMB8jutQJoLeG3HkZu0RUhkI73oycIXh08DXEehhZrji3imj5MV-dJWQhZpXUTmDiAFVgfdPVzYuIaOSVC-LFIokgaxGeFydWznhPhRnXdwNKhn7sArYqQlR3ZEbShXaCiFDDyPByq3V5KxvZKl2rLXIIHiXACvkNHWgUAYH23uKWoHMF5WHhfkcJtSafSie0lrjYqrT2vi1_uoiVdpidFG6cPO0z2kvQ8ToK-qQGG9-DHiGtPvxF59ID_T-9uFZZ1Ucm68oXBqlao36SPnx6l1xcTLIf_dNfgSktZ886xH6b2bTBISoABeACmaUE9AaiC7dz1srfw1gW4izdy1a3ZM4UzvH1Ng1xJOFkdufXaB6ItBRzTobERzeFEMQbCTsxUMCMvm6oMZFT41eCgmVzDcBgekj5QY0ZBE-dh08QizQwgHDIKOkL-jCQBf0hYd9mA6gGZ31slDn4gwJASLQNYI6V4AeStulu2OqDQMZy-7UAtHYQOJhyiOqnLOCnCoiGPij2sITuh3vBZCYca7m3nrbzkKTIKRpCzD09eoyBetBE9DLUynW20cpcbrnXCuw4N_Mw2aQo7s31B_0KpAXnXoUpA434Fo12Boup1nIk0t7H7GstPOAppHAEmLssyKYysWckTy1F4aj4EPNlrkBycI3r3-CrsNm-VUac1IBtjIo1it-0AheLegzipdbbilxzNJ4OD-mdLAcQh1DjlFCR5k9YiiNMmHhwjk5axA7_35Vp0kBBLBhM4VkFgPHsr_WIc8WfkVOx4yBpeEcTz1sircczYR_YaQAUAn7yVrC9J_6B6h5NFahr_F8A5xnTgJLaAi5YD9pqx1HqejQYAS4E-VGPDvm84DkwyfA3GHv05Chd_kHLNZqxn5AHQa4nKV4WhlYY4kMWvv8PFPFLpKOvldr_OkaomQXYOPz9eF8lln7C85gus_vx7qZcEbUx5raeUS0Z1U0SJ2EuALm8QFA8xfooyADK-P1E9dedEIrJO0jzzD7LWT5oHaaFd2_LBEC1AWlifzR1l7si0vu-3AK9kfybW8ps5Ld8ct_TMnuZBWhZgSCoBjLzUHBWuGIwpHnYODMO0t1cG9tG5YHeiByC3P0WQXvLcTu7s3ixUjpRceuVlrtVbaC0zQ9UxZ6TKaKkX6P7_RdZzpeArUPBdfcdpI7G5W5zaz-NPf8uRS70I-F6V2Og3RgjByg_VFAbAMAy8lSuJ0ZI7DyS5XsFiL05t0PGH_hvont77HHwinRoxqJcBDNqHZrdFvfiV3GwwTN2SnULoTKK04PXW-__XV7dXd-Z1aC3lN7LaKa2slvXNF5_-dyWJRjoA_y_pEvD7NzcsOHy1pforxBQtR9B5vfGNH54pL_IwycMokWFcxGXjZ34NDoyfmiWxU-B2-tdOi__VaY7_vJrj4aUV-6UF0XfHCwfuq6J4kVIJcFFqvwIPPQN3sanqOCqkyKMgqoK0CFJZyBpwVuYHPnjsgZ-GdQaTq0VVxE1QR9WJ9xlXSmRf-f55kp8n8ZFKCZFGqRC-q5RwlRKuUsJVSrhKCVcp4SolXKWEq5RwlRKuUsJVSrhKCVcp4SolXKWEq5RwlRKuUsJVSrhKCVcp4SolXKXED1ApYa2klGWaJlWeDTFLK29n671HZt905MuXYZEXEjxAY_mthJwt7E9Nqym0-U697RkM9E5lSt9xRnZ9937hfbZVwBglAYSYaiQwX32Q2-ZQjH5hghhg7jDM3m3uXgMmW5LLDPiuw0DdktSuwndwEuEihgRmPHQ4eu_fu82qjsPkjJK9bHN7xOgHcaGL1g4MGddmjqu159_MUJOpPLwKAigANTMCr4IEPClcZszlXBPYHIS6V3YEnX5yaU4tACwdjEsRv56Cjyo9bvL_Wm0hMgRXjeAavewZTeOMZoniAeACLb0Bq_3MnDCKgcHfRi-jUuY3Gp8Uum5K-WRZmSd1VsapQblWstWSv6emTLEogSz2R7E_I9EyXsd7OC2tWJ5drrfzZJHOV-BBvPdUIdHMe_-7Lz797ZvP3oFT8-7fPv0f77XvDlu0BcsPA7U3y03XIgjQIan3DehnzEgh-1x9Dqpn1Uscs18jEd3C-43SOQrTqaIAWGirUkC5MRRCnZmXgAO97apuNTu0hkNdxZJPz2gTtPpDtWOW70wtnRVfQmnZlWD5tzv2P1HpLo5hjtmxXAIvgR3uB88HBMyI4ApkkxU3fMgBIS3EHNx9jbp6sniDbW0pQbVSakgLNwmedsfWXQeaXhv-paoXUcUf-wl0V5R2qiiNnJmhKA22vgVP5zksftpIrQAurjwcjizyfL1cSywq0LHPoXriuqvBD5P190t4d_iUgwKQWNZhImT-kpx62pTSmSXkt0EfdTDhGlUcgMiJiTYYGAHH_Ri7Fq-7We1Ndz8TyfSdE3tSlan0ZZ6_xDzerDDa1cgNRSzRknekoYaU8AgKg3PqvfnM-zWI2u2j-b2-wC1hMHq9TzX1MGksK9nEUZI_eNhjHD4oF4Fyo8GOf_HW-yhKvZtMBS6R1XS72XFClhTdTU5RXm87xbok_AiQpHj2zEJOTo69RWSIXXUYpzwDtbK8Xq74MKC7322u7fKTI_yHoixqkT57ZhEXGxBWUu7FJQa-OYD7vrwOkzmarrEVm6r8qrJYpPL5uxlrBQHbyQcAS04a8Ls9UMwrCliBJrkF9wGNBiOBf5-YWZFUlUiL7Bkz-56Y5B7FYPUA5fso7qnD8Q5Io55ezXdqsicqeAcjeHi_KaNF-6qz582G_rAreveU5WBlFqds4Mln2QXDcCrmQybg0ObQhDC2Y6KZJwqFLct4vGb3TY2BDoo3UnUUsjVj9mlz1nZzDZfZCCxOmbKJkTlYttucXig2s3uDW_Zpurp60MWWyrXim1RbvVyh7j2-QJY9mH7SKXXKrsVRlVrJxSkNP_2sf_0NOLoHzsDbt79CwRhSRItTWnp69BP6DaZdU2J1by8sHXt83F-Bi_EX2atQiu0Ero0WGCJ_i1Nq8vjgX5pkAFZ2fSnlBzx717CPtPC__vw3Iz9kOCqmkuZEQTkdZnA7A04IrR-Ifo1Jf5h57UUjYVqX9AY44WFxDrby4XXniZ_EdR4lTVAFApR5GSdZHoThqbpzU0z7gLpz5xo418C5Bs41cK6Bcw3-IVyDh_d07be05LNh3PP0u-PtKz9Iv04cFAAH_NqPszKPZNqITPplFVe-X8dR4yeFDAIRNH6VgPJssHilkDE28iSVH4fyIS930LyTnvvJeZQcad5p6iJr6lj-yJp3_Kiqcr8qwtLKpR5p3vniEVjwR9zLE5VVEUS5L9Pynl4eDX6tR2yppFb3uwyodYkqWTa7lSe4YO-fRjj2ny7AvmFlU9dYlv2nSnPOuVJzWFKDJSjDuFTJdEzRgqu26lpsD4I3k5uyE5uatONzunsu2lF7j_e87p6LlqCgFgpsWtrQuuHQsEIrrxZbMYdVuB4qOimHQ1mR__hf_1slGGssOWCciBIFnw_1gBy4oA-1GTrDKid5thK3dzhZEwGgG_Hyi_ZyI9ZX9IFuprIcVvx4tGk8OvXVwirgHzCZ7Xy45aK1gcFUOW9YYw9SVZS-KeO2ELiVMHwqgl5tqdRHd3_BllJPhrfelaBkz4YWB50Ln1EdmhItvsqjgnlO1I4kG0bjZiKs4jioFZoqGKtDKaLAr0VuqpUsQH_QlPFwWK7LLJuqiSvw-VI_GyrSDFLXZZbPwNt3DCAEB4Oo5oXiQCrU5OlY0ALVkiWuYlS-yp0yVFmwFssN6oqL9v1fMI27up4ni2jerOCN3nNFGqYo1xKz2Fuu-6CayM0SUSlVtb3Xyd--W71_fdGO88sqEEfBACO-cJ_3vsZOdCk_nOl_zG9i-8mYnByCBva9PYYUXpvhW66cusSqWP29ROTsRYsA1xK0gE4ak_7BkgJeuJlZshncCBO3UsPUMnE8QzxOD59ZDfqundC1E7p2QtdO6NoJXTuhayd07YT3tKj4cKR9EYJiK7PJdsKjoaeJzkKAFXnmp2U06E8rdGrHs54YCdXgoQC0uFzB8dDFnxaBUhDRfin8kCWwfiVGwWBRrmGPYCwCayu4vLqrVnIubnFDAdzt-VszctXmcNzA4byk1Bsd_TNtAs0ZmFG2aQ_hzriik7yYAcx-2a0GQIvJn4X31pofrzXCxbnd3saJSgBBXPBJCmjU0aPQlGnUGBaQQDrZF9lu1RpuqbYNkLzxsb9QYFltM41pUUKpdoCZUUzzXg7AHN7UuERzvYfqKy73hIMCbiO7ljjQa4QRHSVdzSOXiGxr2NPdMJrXqLJ8dnZntEgI-BApc1vjjE4RoMAt1bmyI2qVuF7A-fggh67UUQ_B_smQSZamWeZLMfQQWCH2kQQ_LWJe8a6zXIcxWGwsSvd-RgvG3VN8y9zIzIwABmIKWEBUnDfku6KKlPXZ7aZrL-eAC9e4D3otzsC2YDfWGSwlaCpZ89DgbaAiNz8KzYsi1wCt0bc9q3fUmbsFGQeh3_Puf44KrhEfpC5tPeO4CrcHDsYMm5XM_MDewR8YsJ_ZThoKAdclc0uF3rV-V2IThHby1a6pBgBUOT2bN3CuvuQEqtU5gkL7F7npzLNVM91s6MIYgiKqRWBnV6xf77aqhUNth_ZFuH6VjxFOfYDLE8IkRBKUBSi_JGoGT8NkRUbC9LQkx34VLzjUDLPnm01D9vhnZHAUzgZ5BSBz2XYoqrCb42ICjxqJVaWsRxG2bbeeh76HNvS1rtmu5dxIiW5xO1PuxpoqpAH0sx5DPQtTwuqEf_b-3_8Nzn6W-r9AIP_z96OQgrddynkJMIN6_tAVaHBPLZ8E35L2FzYM4TGiCwRVBC9fe-VuCa8ZMIIeSgDo494LzyISDQrzcI0xttuAP7nZ3M3XSxQVLuJfj7QgDocq66jO-5dkYufTpA7rpPETPzbusZV1Gu3805JI2uyRpeOtD0KPA3_zfnu3ojWUc1Q6Hl5DYVRjcsmwmRjkDEwwGGAAdnCiYFlqOKpgJq2_0WpS5HCOEsqH0nyEfTzz4UB4v6YQI3ZWbolO8KLFuBw2ifS96sj3VJJGI0D26S18qRWpBBG-Ft8od5-1xgWAphvTdt6fsWUK45nv-8Nm6Sew9v-5jtu0FAZiD5HrR8ZKTttkbGKn12O1QpgNJYdi2PV8gGdnVGzFOmRLMaEp-5LmRSLSJoobg5CspN9LcC-orgFcJjtcdMDK4D2FlMFxRzjuCMcd4bgjHHeE445w3BGOO-LvjTuiKWQp8ygJs7D4Prgj0F3Y54-4aLvWezZ_xMgDnIh--0ETlFWRyDApJrkjlKk503Tig9mC3Qt8_2MmjZhwgCj-sUUnmxKVLRqAChcHqzeww7z3rgBWwFKws0fEDxgZg4Uqko-9Tz5T7BVUiTCQWVBPK_rxA_fEERCg8vbXLMxwBzkFh1PAdvJbcnVnNIFbsbmeUziWDCe_wzXaryBRUSl1goSK0ll3kJ0bbqEBf-Iv_NDxUjheCsdL4XgpHC_F35aXoqnDXAayCKpQ_PC8FBPFRZqeYlRxxYhsXHd10Q6FV46dYsxOYcLaj2WoWFCCzlRzKRmn_A3mE-eNuF7iIHbtlzISExQV8rDzTL2eo6t46m8o_YjpKqwCt-FhR8rmHt4FYdWdPW3EIXCih7TqlV5oko9ufrIbmBm1wp798VWACxeEIK9_fJUh-kiTV19_ffq5UZXkUmbj1qZ_VUXLw_HG83ZPx9vJm6YaEH2R-GWUPvPpaGmCcE449CYfZ-bRRdYn3YrVGbQ5sSdZHOVlsNco9LTZPbx7mYGajvBNiXVeh7EMgheYHUN6qhzgx1-JmnxNTnyRIqZEKYaFKPfLpRKTLXMyr1K_eIHZqT4CtAg6Z6fwFru0nCzSlfqAtLg0q5pqAcvrOGjS58rdW4lYDG7RJdwG9kkqRlv2mH0lVcvGHiaPhrHxfhJMzM7K9QyzG-ahwp7fW0Pa0-kaPmHjwbFYnbYhGIeGcK7y7oACsHyU6qngY52kLo8u_-KUcTg5iS-xSKNX1eOAVubK4bQiZ_0aPL9GeeUEzYnywfwE2nHjcfq1WUD5mdWeFcDxTVGTXcw0zrvb31CbzUhhDAwEi1N26PTsVgJDrlIlbHSZgqpmxpDlUK7AhSpD3a1CgIDkEMly6e2RRTokcbhnkVQMAYDCJXWKWKKJ6xWEQ8rdS8e1ZSrUyb0HEktyNtywYuKmbAeMgC9Ona2D42RIR67pJ5KEZ0owtPsFT5rbBVt4YCh_vThlVCe4OYSp8t7_5aWpI2CZzOmfHuQGD9uto8aO-SWn40Y2cgDh1UqKDZwKyuL0xnU0FWt2ccvilLW8f2JDBuvhltHicrDYJY5bxPtnQGbMCOBwGG1RpKo-bCSzPS268c87QUUjal0Wp2zf9DwGy4blDfJ6DSMaG6dUf69LjZUrPdLiuk1mtM-6oMX0cJ0yffcvEpuuIX6gTdjMROEG91Xzu8wGchy7XsOj4rn7f19SqQZ9BBiPjOMZ9o9mgmoCWcJsDc1uPIkjyMFE2VXfL_4i2ooOs6ENejgPSJqXlRBpEaUlqMywrjI_L8PyJA-I6cv9kfGAOJ_L-VzO53I-l_O5_oY-18M5pvapIlKbKiKZmcmeB98dZ4X4YTgxqjII0koEdVrKKCv8QpZxUaZlKqskxNbWvKibLKlkFdWw8jKVWVVFeVTAk6r60S-6z48RFOehfx4c48dIyrSum6j4kfFjNCLIcFWipghelB8DvWwq1VanbcpMOJIMR5LhSDIcSYYjyXAkGX8PJBlpnaVJUIugyqJpkowBav84ODJy2eRBLEsZZOHfmCNjVPd4wAtx2KCrCTKwCphdPNX8TlwVunX3oaQVf0uqDFPsoOky6P1GXBnUYLDEyiwAB8SQ0bBxPsJDa3rsXp43I_OFTJJM1HEknsybYfNl4JnA7vaNNyoS0QV6eMqtzAAmb6Y4Nrz7KTbAQlvFJPfybHinaDYuWsez4Xg2HM-G49n4Pnk2KjDMYV5FjS_8vxXPxsL7XSvt3CZv3q3oOZhUD60mKhE6w06BG-I8CsIhvzVKpyr16hg7HGOHY-xwjB2OscMxdjjGDsfY4Rg7nszY4agwHBWGo8JwVBiOCsNRYTgqDEeF4agwHBWGo8JwVBiOCsNRYTgqDEeF4agwHBXGD0qFYXm2UeSXskpE4ZuYq9WAMmjgx_SS6LGLIgJNHhdBbrCf1V5iCf9TO0W4MJJXmFUN7wRcDc5zv2vAgVpi3Tyh_necYezf67rfUe0el-xdUr6-75Q_N2pRU8EEcm2sNkDYDf8sAGz6y6EcRisS3X_a4OpdtIhjh7iXDmZZ5WMe2Wc6EUWyyNKPsTBh02mtup8_5NgkhzjGsLjfceAYj0MA0wvsxhEdk-P86ML7LSB6VC7wcNWSjbjFSlWTK0W3YG7ZhDhooWBRMUynAo-4-nv1fxPSF8nab8oq8NPYSIjV4mNJyFO7dWovjM_CmDHNOSggCrqZcrgZhoKwvAGz0ehb4HPUN1ZZbXvTVUMhCUqZnYAzudhbDDEEC__1w1JpJ9JoOuRMqTQF9PdSgPwk9EnIqmJo_hb2cPRz5uRAcQR0_AuY6JVO2Sw_CcOsTKu48U0hptXZZG3KU5uUhggOCMsSk9cUWWET8NPeC_P5F7_8lTYbpK_ldmhnxUD4NUUvh2VRSatbqlAaSZ83blg67JPFA0yTI1Gys5SwQ6zojyIBk0nbb_fltNmxxmDMv5qUv3bM1yZegBfrMBYdJO-B56hIqygOMj9Mk2ZIwJt2r3Ghz5M6tyytbH4ui4JZOqCM9-4wGTJqV-Yift2rTBKhsg-ceFJlBiDVaztGxtKktgrOr-9VEsT-tRfDRtDBggW1NBarKsrj44NmXjYYVz4wCA_ovTpTTJUMdoQEt5HG26e82YVylsoVJgOofLpXkwRYo2dHE-PzqK0vM1lwowc5t5xOxOkpVa2iDqq4H5ToXgoT02SPFoK4Bq8WDmotMnNura46kyV7eoNcsCiyIAqy1NcpFj65PwG7xlv4K1pm0KqYcUG_gOAb5cw2OzqyvB24i4Plqih2YfCdtr9K9kpsFdkO0YUji-LZLUAz1b-jwd0QZBjeUDVRWFXEKraKhYerrd2TctFy7OGJfGLkK56fYhXb-3aPW-zg2zHDGIV6z0HjXIlNvRUAvn4cdGOyvVluuvaagNeWq6aOsY7R_J_KOmZ1jgwdmdOtKdNt2lgv6082Zj-nIfzUmFZ9w8uN-eK_w_7c_vCHUAI8pXf6AeM-qev5AeM-qV_5hOjZmhW--kmUL_zY98MkSxKiDUAFi18kRwT0OB-TdTxOcu5YtBqcUkT-mluyTJ9rv4RCAnPTSMWla3SgdJhGeWfbsfF-PAOQNRvW-5Z3BuYUXcGb7Iw8ROONUKQM-_yUB61bD-ajjJ5m_VicOnkn5_Sm5gl1G1GtpEIzZNgpHIXI15SE2zxJGLVfcg5fgVZA4abcRHFeadi3OHV4J5aKXC5ecwY2GE8YRQuwa24IDHBkh3bVCjAc3nEfmdDktg0-l_bnFc45xSak5g57ajuRx4lpDtl7JueiwPXclDi3WN1PkxqMvsJfVbeqzzCrorXtzJ7dAM-PT-yQzmdyYuiW4TYYrEfOQ2MnzwkeZ2dhPqKyoULY1ThzP83cMzmPxAdctFqJjcZXAzcOgz_F5DNE3SpwlIXyffikm7QAuGcnqXtYVKkwFh3R1RJnb0JT_SCjg_jsa6MjYmS55zO7THhmFnamihnp5Uxl7OMYfIqmiAq4N02CVAAKSsqsbFJRnWLwMcwB9zP4OPzi8IvDL0e5TSZ4swzlx0D0kX93nLvjB2ExSUVeNFkeBU1eZUEZF43fiLCM_CQqYAGyqorhbeIijqM8z4o4F0leyLBMG0xCFv7pVxrzleRf-dl5EJzH6RG-kqYEgY7DyvGVOL4Sx1fi-EocX8mL8JXUfl3kMgllVIq_P76SpT50Ynm2QigdLXzO_c_BkL038_stPHIreCJYHjeAb8Uy8kiCE-8kvwlWJjyY4IRcVRSPlYkFGwYN3VWCCa_jvqx-kCNBcSQojgTFkaA4EhRHguJIUBwJiiNBeVkSlLIAB9-PpWxC-Q9MgvI5jfVkFpTPVTTzSTQoX5kfFdG1TON7OHU20w1O1trrUtthpdUvCeB60xpiISGbFHqLMecKT_AU6Yp3lHPFZlRRZez7pCqvRwk9fGFjStWPTjDJivITLVuJWTX0oUw9-n6Z4wPZWsBPOUrX4j2WrQXrd0_QtXiPZGsZKEqO07V4jq3FsbU4thbH1vIDsrVUuS_LvAiyJvrxsrWMDbCiZpkp8YPD-jZK52QL9TcWg8vj-Fu-wgrsQfS4CFQVjugOeFjtbmVCzHNTHTugHyoNMdjgHI2sGYSMzlCDomfCDYJckWKdK7OliloGJN1wy3jPppbBws-BW8aboJbB10PGFNVCQU-Zc9UvWEBdePxzhhNHqWa8RzDN6NrPSaqZ1wf7gkMYtKjLc7BjlYKye_UfvaOqcVQ1jqrGUdU4qhpHVeOoahxVjaOqcVQ1jqrGUdU4qhpHVeOoahxVzd8lVU1UFVEeB00Z5I6qxlHVDFQ1lJ78z85V48MYvvQjIVI5zVVztFXyGHGN3Q53FoQ2KUaQZujpmtQjnN8wSg9KkGceIHg73UfJ6bg4oJBBE4hImL0z9NywCFXREvBR4Y42PgtzDJuDnrcyy3tJV4QulqNpxSZMmthw9lBTJoLTBSw8Bnq4qo9DZPj2Cx9eljLHc0xtHv2FDFXlqd1ZBMVztmmrZbNl2pkSdTnI_9sB3sPTKUp_FGeDCw1r4i_S4BDcziZ-MIOx_KbrpYccPPqO41lenNpF6y-yOEmoRgQQkL_Iwxg8gE_3mX4MOxGsCZUTDIwfqBR6ds3RTtl8LTbBDrhp7DxKsVkt4Vh9zuMyKqPgnQ6vdBwZu2hVia8RXDyTCl5RPMKqYDOCRaVsjrjn74q4J5R1KvLAb-paTBP3DCwwBxQ-lHpEASuiubKJ19QDTqn9ra4F4eWku70w4zwup_uToaJmiH5VcJp66sHV6GHLCTssnw8zHEn2V_MKNYZOaRpJeH3AjkX6APZLFSqBqaQHzOnOi1YH8v8bwFjsYcGr_UURBSk8cOt9-OdkxgnB42qDL8_9JB2l8_njNE_CmY14-OMki4OFtdsg8aAI6CF4wdxfBKEfX7S0RmNP_o_wZRSH6czzv6bqgx35law86fDfeVeAkYLcP4P_V0iF1wrftfuwUxRLyGITJos4jefsjlOYG-eaBYvAz82nQ9j7NS_f4KPDFGG-6Jn7YeKnmGlTrpyqLLGkVNGvIcuaqDgdraPpfBEqNaRj6ayVMX50iWdREsg5EgSaigYCMIvqtKyb6vFsR-N2a0vb5Nhwrdh8yEaj1Q5C5KVRRlWRH9iUR23n7eXguMAHtSxpZgzjzI3mvVAQYYfbz9ZWxVvZ_1Zng5QQ50KtCWZmgq-5coEeMMpyl6AsuWVOwzX5zZXY9VtD0ECVCLfdfEPoVIUq-CzbDEmLAZ4dy3brifqLMMtyXSXXoPNFVaXGDsZhFBHOnUrGm94T7MzY_00sROIqhDWXmw0mQ8lyqHzuHX-o3RvvX8Eo6_wxrY9ZEhAesmoYVKReOSw3IARj0Qlyhz6dTiMxtRU3s7o49kC9jdvJD11Tpl9FvYdUC23gwvvdOAGtiQttW2wRSKnOHm6m4fDUvWg5xl-mC8ukCYriKXRQVDSl_TNu-GJ39RRTFIiQoYqyO4DtHKf3k-ShTFFYNaYPI4Z-zTHc87DUwin2oAPKtYHMccQmZW_qaB-xF9nDJypH0yJDwGs5Jkrj8WuMiBAoW3Buo5xaNgKhGab6UGW-Pixm4M_pt4O4LGSPLmNAfyh9ry11aXngKnJOV2AD5xE6Mfs1X4-5tf5eyLQ-OUGj9ckJAq1PTlFnvWXSLO-rHw9rFqip5h1Igtx8H3RZWR37CUzjwTwNoq5pGmvOK8Infzw7-_rc-8j7WVee3xRX4HxgmxEGIgg5_px7c1ss7-F-ZAaUFIPbTFNINGVGD3uZqckQu1HAbl2rOXFmaA6n6abw1FcqhQdwYIosoi6bIInFS05t4AaC2X3W7AES1AVSGaIgnJialXuzSTL28nkP54OwMl1PGc-Ey83SVXEl81g-aLz7ls3UYMGSaad6zhsIO3pNZot5Zm4yMPJTr5mGaRZRG-TDaS_um55q-ObblMzBvJAmkmMkdgL4z7upXQ3AgUuL-EWnx47KaHbYcGKfYKvMZf3qQQRjlkLZm8bAnQVzHj3EWIg5N6-QFwVqeM5sVVYHjEWgpe3_RmIknTF1D9aBRlSxpsUphTI1tbFzzZoBG_I2RyiZ4IFrktnFKf0w9STzNjBjHTb7NPyURoa_iSkLtRLq8ZsT67A4dbqmHgwvRWtsbcJcB-pHR3FveOuUHB_-rbKzhutgkHV45nj9dLhbtYIOSYxhZY8za1mH4YGzCDOKZJyQ7EPmsWERyF9dnNKwJwm1PlHdXwqZax5fsUFUxfUuXJdrlXl304cCnaPFKdV8mqlOUe_yRGzBxuS-CqUekwPTWqAbuKlnwo7RnmD2-gP3w3Ew8kAnnxK7sWxzER8_GP0QGsyIlEV-NpYo08r6GC6vqJGiicpchHkY5FUVirxO6jQ5xeVlWHXu5_Jy4MqBKweuHLh6Grh6OOegoQrjSZ2nM4s0LPzuOCfYD8KDFtRVIGRZNElVJUXUVE0aFmVTN1VY53Ehmzgu0xDeTIZ5ITO_ysIEVFOV1GEhZJQ85OUOGNGK8zA994sjjGiZDOLML6RjRHOMaI4RzTGiOUY0x4jmGNEcI5pjRHOMaI4RzTGiOUY0x4jmGNEcI5pjRHOMaI4RzTGiOUY0x4jmGNEcI9rzGNFKP0yDqEqbSCSDr2VSw2rnn5XpvSHyn44KnHHFDkthGBDWsABY3wwwiquxGadZ5SS2NA01OHMUORIh_J2urTp2c9xcttjIqDBskGozU31-B36f9QjCZsPoBBoomEYuM1HAYHLJ0DaBBivpK7pxpuoD8LLLVVcC5OaIAiuDFayQafAh69WrXkbmMVG0SKxUlAkExEjtB1SkMfgHPOxa0K8c992KajQpL2DWfyBugAXm2ZgfM1MlDFjTQqQKuusODgSGy_Cp6g56EDmoQ6s7_QKfB844I1kVaYaV1Z7rdpL2wzHyOUY-x8h30BVXhX5WyzSuImmdCl0Vc1QrP7LIBUtMSOWMiidGUoQn3Xgcx2sXiBlopoNtxxuISMx0aw6tBFUs9jrvp53DPc_Lcq0QSs9Yck1HOw5KTb8qiaErsxbelyZAvOwZUHS0xcvqnChnKNhwiNs33DlAPT1wyYEjMPP0V6c9CBI89QzC70N1ih1ZN721hNVKyQQ8imrkoHIMqw2V4dGFmOp3NUe7heNjgSan8CdbLrMkz7DpsjSMLVZd0ynhekyZkvrRUlSLrGFxYkOvLCnWm4zcPK1KJ9Qsia_1h61M9Z-kvi5ay1ApRWt_P65wYZRo2pr2fygXBrN_Kdeq7j1se2Lo8OkNNySqC1X-CoHlOE-t9aKVzaJfV9UsA3QaWO8dqjgQqTeDTjtSicvLbPgEVXc4-FNy8NisRmR6zYFoyTp3WitrnQ5Ohv4d04M-aFXwTPnzlvLQQ3bdtL05ClJHQeooSB0FqaMgdRSkjoLUUZD-I1CQRlFZZ1UYxVEUn6YgPR10ehglKR947toGOIfqQJcoaF5S70m0pDjSQFz0YFrSpC79IAnCOCx_UFrSE6SgL8VLysDTDuYRzOFOQFLFpFpMguQkjynN4TFcpnTATnKZ0nADn-lEGr3I6rgUSRoVmW908NCYcdT3e2SvBYgbn8CRtGmf0ETskPEUs49664Td9KUStgjyyJiaq0L_40N_xLRbCs3ZRUpkiQHW2yswmyN_n9vV2ScwG0SEHP0eTcdFyx9rRosl8usJJOA7IMkiR175hSi2s8P4wUWrvX3zNv6i8HVpCsmjdj10FqdTzLDXWFu0JNPCfh6o_YsWqwfhKciheY1ljpz_1IuBLrf9uY09eJdQ21Z6DIod2wR4mIKgnZ8sdXR0t47u1tHdOrpbR3fr6G4d3a2ju3V0t47u1tHdOrpbR3fr6G4d3a2ju3V0t47u1tHdnqS7TZswEnHSpCbpaPHRHI3GPpJa5vhJKhEEKoHW9VhUkb9PYIcjzlc44vgQLTSo2WqwFGcfD1pCYwGjr-0SsOGuMFxEGCtVspjnCz_62AR81CZjnZCWkIU9CGtfsAJZcgTz4RNpjqD4U4yg0ztTSB0jHJKCr6QDX_NX1KNOMWWpDJaN_lUw_iYbtK22dBxD2Mf7BrDwYThVcabgxpBygJOZsdLWoZl9ir-hBNxGHobtbwCsBFORqAd9i8EZKA79IN1fPzgbmGlq6dSY0q3XKjJEfuWxSrWZIiHRkUKsfGcweCMHsHv_saj8qIyarIkC37TPWzxIx2vSH0dpNCpPr62qq2zU04DrEiYX7SFcom6rY2BJYRe7YprbHU6m-Fj6YI7yhuUZUI13onkJtHmKjulhZgm_S-E7c8rpzn5H5bksg4jG9mEaiRIICp81c17BioI7gjchAhoqouRG-Zawn5wbU9QQXCPEuBp8rbMgGuXJUCRU0X2j02y7dgmYRgMAq9DYxnMbbAYrGKHl4SJI4_Gv9vXEfc3AfSXILzhBuq3edCQRgze_7-VpxDQz9IJWDIk2dAggMZDi-s5rqvi387SO7tzRnTu6c0d3fi_duUzzqAr2uCWfS_WH0mt10mHx8EFBv2oU2K295cN4lK2Z3kNyux0cpyidI7CmYv65SgMpPmW7sn8-nCULaHMpJEr5fIVhCp1SMTpmNuKSw040m6D3GBcsz3HE3vqkqVFEj3ABlqcWgw2liXIphAGHanBFG_xwItgkL8oik0kZZhHSG5aliJKSKLOOEsEaMsH7iWB_pGL3cCbcfRLG4LvjtIo_CKlkCepDpEEhmrqsskwEZSLqMi1F3giRRkWYN0Xkh1VeJHETiqipsjyXifSLNK4Edd8ee599HsnAP4_988A_wiMp8zAXcRg6HknHI-l4JB2PpOORdDySjkfS8Ug6HknHI-l4JB2PpOORdDySjkfS8Ug6HknHI-l4JB2PpOORdDySjkfS8Ug6HknHI-l4JB2PpOORdDySjkfS8Ug6HknHI-l4JB2PpOORdDySjkfS8Ug6HknHI-l4JB2PpOORdDySjkfS8Ug6HknHI-l4JB2PpOORdDySjkfS8Ug6HknHI-l4JB2PpOORdDySjkfS8Ug6HknHI-l4JB2PpOORdDySjkfS8Ug6HsnvjUdSJkmTZRHgoiH0b9F6HRX0RzJ09crEcZ01-faGKK33fvY5NVJqparaFb_sVj_XhSRUnW0V3nrG0e1Vbg0Ai272t-JFrLJgQOz9g-WrlxXD0pkH0j2Oq5AV3atsGurTGMotOOQxVHhx6sFEJ6mZkUxHEp4dPKHSPBuEY2K6osHsj5kxnfRCfU6GAxX9Sph3Q49fd3dyX5xOByouOonAfEBGdgTFHCsui--80Mcn_SxKFlnw8c_PYc5jY0O9lXiQFJzgxfTiQjc94QHCEmBybo2u4Ay2aUBUSp0LpKkmQJldnw3IiAxPi79mxCNzQMFsDPAMlHi40GYfSO8sBwyhgjP9lVhLzjRR5gZwJSg8MA5ECzEYQiUXICWcXt2LV1P6s1tJiuTzSCi_hPH5DYgvcDjETDlFQIbtm2rC1FxQHPZXTabeEF1h4UFzhVUmpoeR78K-bVoZNVvi1BH4MoSF-Vm8sGYZ-lux1klUJlxaUiWesqCcyCHHOkoZY7FXMyA0ElT2BThQOLOphPCPi1bb2RMKjyXgJ-EiDIokC0HutoqZjUllLT-IYlpoPK9pNbbyer11_LeO__YfiP-2OsF_W53gv61O8d9umP92--Ohv5XtzXLTtbjP7_Bw998HC24cZFkcZtWIjvQ3xCuACkz3AY3svOqfabopgtKPPvrIe-g4CvYcTyOZmdZJkUiZvfhM3-gKFW-yZ2qvu4ezfEeUrZ5vUkcylWH04vPVpBNcQ6TbQe0qdgLKGLRHfaPrYKkqaGK-QVBEQUau28vPlytsQSlw9pDdFsMtYWqGdFjC9z9mZDUx31ikVVGlzcvLA4fUt8oX1YMNzkE_G6Y65AXJSj6M0Nk6dMcJnd9QUzWWb4zeZ18EDbPx0VMyxRXNo9sgSIVgkZhRobgWwDBzWBFAFeCLnRLwU49icGCxUg9yO34XlS5anJLIBzyAIxssaEayxk_RvXYUdLH4qo9L1f3rZ4EyggMWQTZAmhspVLmIspxzpEe1F_Menmy1ZhMyMLMWVC0hl6mYp-gJ2DGno0vwcHLsLBHSz0WT1mFcl3kowO0tfXKFj5JjG4bk-8mxnTVy1shZo-_TGj2c6H6fFz357jjt-Q_C8w6LmydhmEdNBnIcxVlaVnmYFknRiKJpiiKrhZ-KRIay9JPMB80E7nMkszQqmyCtTrzPAc97eO4H50l-lOc9ErnvZ47n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vjeXc8747n3fG8O553x_PueN4dz7vmfqh9Pw2LTCQDz7vFrGmivC9EianRcppVVVTVgUhNja3FkqlL9J5Bb6mOsnErcMMG2loPK05hWuiY4AZTCyE6KlYBpJYAFk_uilb1ITtySD7ftYJUzH73-V73g1FMf4i9X2GOhW4iV_WmW-2u5ZGDONah-D1OC_OrWg0NsG_mmZngis_Z7cJg32VrKs_GOoxFszVwQrDk8vSpp502Ux0TrCunFpsltqDDqEIxEnDn1pBsVwi4x8qGSz6OeKFY3fXLXs1LsYeMMy861jc36Gzcgk1dabx9FVHRKbZh1qrjxRoWCbvvt_0BnJ-iZajDJiubJE0H4hKLDXUU63gajSn38_3SnrGl5AjEiyUaItiFOfrsTGN21ASZAlFMXJrGt6Et56e9x2YJ7VQaLhL_4wXLCr6-Z0mI9sDyDC_aM7IXbVos0pi9uZGVLQCGZvw5THfh_Z66gHR_LT5pjk86w3dRvT10gGa2tSaFrSeQJQtkUB2__ICZlXcZ56AIPzbmnUFczq9qJkMvekrsB4TrFTwYaILRUy_abm18h61HuVD0fFrUBSB26oaf9mZ6c4IS9_T6l2Xd-ElRZZU0TZIWf60lYU8lnt1L9UQFHF-c4Yj8ZYQsgnh8SK0mg4X3Xw-LnwjAR4soAkkxv2jhFTAB1hO_n0714O1htsjyj03oKgoXeXgkXGCqZ9mNtr6zfRnwyDCqG6SZj65TEITx1--pTYF-aYK7-Ox6qymfm1SKAlCDz82VlNSppZ1v40yrn7ywfWnLPGGRw4FjbVQS5ZBwcBzNGCtV6zVVrBWVfhQnRZqHoSmQsXiFtQV9BiHw-JdaLtp9AnP6pZZsEcZRGmfM-YJZsju9Bgp70HZrPGJV9-nT6IlLZS3MBOYMfhDjUKqSM6CMeegr5ZtNxASZnwfWcaeskEkCWfUgJtTINgmG6733v_ndLz_9_N3b3_3-q89--2uLgPfdH4LFn_quff_aJLr1GeJ-FuInvKbaKc4ZoCu-vUKXxdQ2aHNrZ3sViYqKSMLqYMWDSs-auh33Qz3uh3r-k_xQz9ff_X8X1PRu)
