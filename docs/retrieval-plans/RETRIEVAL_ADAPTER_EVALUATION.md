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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzUxNTM4OTg1MDI5OTJjN2IxNTc2MWYxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImU4MjhhNDIyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81ODliOTdlNWIyNzNjNTQzYmJhMzViODciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgzZGY0ZDJiMDhmNGZjNTQzNGYzY2RkNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfemS5MaR5qvAWqSNOMrMwn1U29hOD0XJeoaSaM0eaddYtOoAEKiCOhNIAcgqlkia7a99gLV9g32ffYh5knX3OBDIA3U1KVIKsxmqKxMIBCI83D-_vvz2BeuGumLFcFmXL85fbLeXkRcFaZZGrp9lfpHkXpTEXuVlLxYv8ra8uyzrK94PcG1_zfwoPvdd3yviIi8C33eDLIKLWZhzN83zrCxy3628iLOo4j5389ALoyQoXLcseBX5jFcljFvWfdHe8O7uxfm3-MdwObAreMKaDfioBfwj52v44I-8q6ua5WvudPym7uu2ca7h-ra7c_I754uubattx_se7tmy4j274vhSk4-79s8cXnfX4YDXw7Dtz8_OrurhepevinZzVlzzZlM3VwNrrtLAPZvc3fG_7Gr49-Wu591l0TY9b2Athm7Hv1-8uOYMF5GnfspC338hPrnkN3QRLC6_jNIszxIe5T4sQxQGec6CKE8TnFnbDfhql-u64TBztSPryzQoq7D0czetwgrvCqugKMtEvI6c3WXBtv1uDS_s4zyLtiv7F-dffftCPv7bF7DLbdfjv8TXvLzMYcm_elG0Jf_mxdfwBkoa4MFlW_RnHR-6mt-w9XK7Zk1_9uazt29ef_bHV59fvvr1qy_efvbmEv_4z1dvX__h96sN7uVj5IkNMHq-G2AbL3PW1z1KFV9Xl6yH5R04jbcbrtsOJ_2-bnDI_q4f-Aa-adgGd1dMfgE39igPL86b3XoNr1JcwwZysQT5ui3ew7V-lTDGsxQuh70b-Df4om_UOzqsZNuBdw7-sWM4Lee__uf_cWB5O35VkyTKSbCypNltUQz5LXzyC-fh48D_lA4uKIww3G3xLVBQQOhefL8YZ5vzzEtSN5rM9te8EHI_gOCbT-h3W5SgfnaSv3Aecv_MnFjlsywO3Q83p7d795QwWMl75_aaD9ewiMz5Ag7D6wZ2eZnDmYalU-tbj3Pdso5NFy-IXNct8slEP203cCGMIITovrU6cvncdsFeeWUQPPmJb6-5uRDdrulhRbnTg6A7Vdf-lTdO3Wx3gwOnd7vrF87A-vfOX3agFWdWIg5Dz-dF9uR5fed8SRc53zmfsqasS1DLzhVveCcm-h0IFd86cHJBsYoPPvtmC_-G4cd5kW6bTCwpi4KVufvkif2-dfgm5yVuRe_AXQ7cOjhtJQSxbuqhhuNY0JB13zYr53UFAtXzDZtZsCTwQr9Iw8m8fmOsPzyrKcECgfItd0Wd1-t6uLtHlh5y_4xwpUkJSvNDzukzVlyjjDnSVpzPrUhUpHHAgg_39KWUYWfDmroCK3_u9O2uK7jzn29eL8CYg4gJpLFwNrysmYNzW9BjxomuUSmbE_X9wk3Znqw_a6J4KOVU8U46cWrOQuYAuKDyQ70kbV-_cl45YH_m1FNVJVFYVJOJ_g4tSHGfVhqvmpEXXlVZ4YWPHv8NR4UNagjQGCw8Xu_cAjhymt0Gz3vbLUBDNy0gJPEH_6ZY7_D9-8XM60YhZ673-Nf9Tr4t6ZiKDjTplz9d3zn1ABsxgB3one8umu-c5XLpTP47q3uKqoyrOH_shF41zq5hN6xeEwoVMruAzzrYBPqoqtfwQds5V-26XBJyddgmr692M-vDGSjD0J3K7avyz7uyLoSSReFjzVAv15whrnXwuq5d3yctDx5kzugnQRkBsP_As_stLJADj0BBEkepgFVEq5Hzqu0Exue3MBtpDJx2N9AZvr2eWUtwReLSy9gHnu2nQglILSV008QEc_hLIRMYsIIdlwaynFOtZRCWSehPZguOzKaVIAAEd36HDy6e2Uk_i7I0jvInPk0jMTh5oB7AZ0NcsgElsIUF2ICfYaDfoVX4jyDbzBqkZR7FLEyeOCtv5TQtCNItPLTk8GhQTmAYQGuAaeP1dgBY0PcObAZ_edH4K0AAcDPgzDXI3IwxceM49rIsfuK00HJ0Qp1udv3g9NftLeE5sBA7WCfQqDkoL7QV27YHzXaD14MLNzjdzGL5fuz7FeN7CHwNt3eogO53ACaXzghLxr3KZTTC45-0VIj1pPGEvVg6YDfVS5OSdkCQnGZ_U75eKC_2hbS2l1JVvJDfKHeTXybgoLh-ECZenhZpkgUJ537loRfVtAMtqXS0Helog6nmxfttWzcDxQ06ehK6keov9CK_Rg99XRd3xgim124MQvGAJzr0fVsNl2Dprni37WoZN-hz7zzKiywJGAehTL0oTjJQGsxPEq8sSp5XZZmyKMgTP2FlmiXMBxQUV37OXB55rIxo7IEN5P-L7Tr3Q_CT8ZMXvuvHSzdd-vFb3z0PgvMo_ZXrnruIzeWKoxVPQu7xqAIpGT_99kcOGpB0Crf-mvXXcH2Y-wWP84x5Ge4IjWF4-lJwP6CDLp9bVNzNq9wNizRVzzV8dvXcJ_vc8jGuF0ZZFVV5GsXqMYYbLh_zHDd6A2j4huPtcEtT8IuGrDIOA3aYdFbe7uDW0gixObdt937dstIBOLi7ukZ9_2fQc3V157Rb8g3BcNfD6qJ5PThlC-PD-ZPzMqa1aUtESE2P6hveAfQFqG2A_eMloH0kyIQLLhpWbuq-r3OJs_R1zZ1-JdC1OwAX-R1p_usdKB2JJlZHVKtc6AjmlrkuWMgg1_s5hhHG_XxYXECOmldFkOQRh7Pr6VHHUIHevqf7_gQ8yKsha3fR9KCLNuAxXXdiY647ztFGg_aqh_Wdg5EzPfnz0wsC5g-8CMajgEdq6kY0QU79OeEBif5OAHjxX_zq3Zp_A-htvSyud837sxvvHXw7tfXyCpC0YodIxOkLxJDfObClcBu8WkHIDAfohU9T1d_AHDDyvGZbuPIdvtFlv2XNO_nYLZyZms7MAGsonzuioF68EX0Jf7AOXOrv0J616xtcYfnCuDk4Uo_PkB_Kx8C700MmT72-y7u6lE8Tk1Rv9yuHnrVrFAI5WAfQYax5v4dAvyP3eVxvcJyKazyfJGO0M1y4xRwj2vKmYw6UFA0_CxgLY7C0ZalEw4jnSNF4ToCmwZeBqeoBLhppWISeAJ0FsAnfCeQNHFFwB-FTBhpr16G_asi42O0aHIf2tpGn6aKZrhDuUcEaVFEoELddDVIMq9MrfNLPaI40DeMkCIrADbUlMKJIo-Z4YhRIPsar4sJN4Dx6CVOPMQJD8jEPCeyoA16UVQAowc1DbVqMWI8c8Dmxmq1wr3ZwHkFPd2BaHEe7z4QAJ6AQRhbQjD59_esFabi7BXkYJKPK48bB0cM2jJajxRv-j5kOH-aC-ECPUxYC5QOHBa2gIjgLFIC2oXM2EQ7xtMlH-DTxzjTqhuFx4ksdBXg3JmYMPKTmSkdbquuebCwFXHBQuHjXYTCpULp0QXazbUBx42kFfxhUKz31lq1BIyIeokPQFLBQcmdwU-iMFDADXoo3YI50evBlwCMBLTKsjjhACt8AhnazIq1YWWlcNQbYDMv11AAZoNxy6lEvLhq547S5FD4hKz89rSAlHY7uNPx2z26in4dwYIDhL5qco5arYCx4EsDplpy_uu3MKNbMyQ6zOE8QoBdRoa33GLsbT_ZsVE4OVoZpGHngjfDCV4MZgTqdj3p6CG4UVHkm4JV5h5CXTp_DtggCUEJn3rkCdeCHXlZGudbtRgBPm_1nhObwQ22o4SCAIP_re_iSNl0KBMwVLCpaCZL7qu5AZN-P5wKtKfzL0ccL_oWqDy_u6qvrQT_hv4kHKu1gPI-N521qICUoECBsomfkU-vh4HHgMBRcPusvO_A1nRywA8ofhh4IGMhn0bc9HgxEy-yK1Q28G4xUg6CvWY2mC1aZIMuhWRZgmp4r4xv4HHoXWASQBnAd1TsD4JMqsFNOyHejbqTBlb6RV-LIbFCuCT2GzjTNyzlzYOkmA4z3wcA3bV32JIAgkPjiem9IgtWgYv_nQzW0XlJDsqLgWwoMCh34iyATMTvU3mcAEepBvIu8_js4N6zfwaopV6RtYA54GK7AsN-JCWwjF27eZpHSnnAfb8rl0C55Yyhg4y3KEVCZA5M2JVTDtYERy49fYEiDlvC7Uf-inK1Rr7364vV4FQKhNcdXkddv2Hvc6o6VfNlWVa9R_Cw4y9yqisIQ8Fmq9YwR8FYh0WeEsnENAW2J8BYqdnDL3tWNctRu-LsRc8FwgOxeSoDWEH7rYeQGXREC6Xg_eoLg1cHTEOdhaLEUsUVc04fp6jTKM8aLuKw8HQcwAuujrn5OTFwhp4gxN2RREHCN-IwwuXzWcyLcqK4rWDr0c1egVRGyCkd2Am1oF6goBYy8GA7Vbs-5wPZSlyrLnIMHiXACvkNHWgYAYH0H3FJUjuA8rJy3pHAb0ql0YnuOq41Ka8_rEi930ZAuU5OijVOHHSZ7RXoeJ0HflADDe_Bj2MZRb0QePeD_07tb-HmZFbwsXKaxqhHq1-njp0fp1cUEy-E_7QZcac5LsXPCD5P7NhokKcAAPADTNKCeAFTBdu563ht46wLcxRu-brfCM4UzPLykQa45nKyW3HrlA9GWAo5p0diw6nCiGAMRTsxcMCPNqyL3eJC5xeig6VzDeBgekj6QYwZeFaZ-VYUsTjQgHDMKKkL-jCSB-JCwbl2B6gGZ31slEfxAgME5WgawRlLxAshbt7fC6oBCx3D60IJaOggdzDhEZVTmYZT5WUUelfCwxuyEfMNnJRxKuLdZNvxKTFGgYAQ5-_DkJQriRRPQw1Ar09lGK3fViVonvOvQwC9Mkyaxs7Av6F9INcDvWlQJaNyvYbRrUFS9ijOR5tZ2X2H5GUchDgPAxHmeR5mWNSN5YjgKT82HgCe7AcnBOaJ3j68i3OZBGnVaA7IxOtLIdkMLKBT3HsRJrrMRvxTRfDI4qH8GCiCOocY5pyBKq7hkXhhX4egY6bSMGfi9L9eigoRpwNIIjpXnac_eSL9oR_wZORUzHrKFVwTxvNXyqh0z4SM7FaACgE_OmpdXpH9QvcPJIjWN_wvgHGM6cBIbwEX1iL0WQmodx0QDgKVAH8qxYd87EQcmGd6AsUd_jsLF7znfCjPWC-QB0KtG5SvD0FJDHMji19_jYh6pdORlPezXOVLVJMjO4efH6yJF2Scsr_4Cqz9_LvWSoI0pr_WUcsmgrLIgYnsJ0PoGQfEY46coAyDj-xPVc3fOJCLLKE4T9yBr_aR5kBbaNY04GKwBSAvr091R5o5M67t-AHjF-zO25d8safmWuKVn5jQP0rIAQ2IOYORDzVHiitGY4mEXgWGY9nCtYR-dC-FO9ADk9qcI0kue28md3ZuFzJGSSy-9zK18C6VlFqg6lgKpCrTUM3T__8rLpVTwBSj4trwTaSPW3a1O7efxp78RkUu1CPheBevUGyOEEMoP1RQGwDAMPPA1x2jJnQOSXK5hsVenNuj4Q_8DdE_vfA4-kUqNaNQrAAzah2o3oF58y7sOw9QN2SmEziRKK7Heav-_fXF7fadfh9aSf8OLndTKcllfffHZf5eSqKUD8H9Nl4Df390IwRFXG6q_QEzRiAi6WG9844dnyrPUj1I_iLgfZmFeuYlbggPjxnpJzBS4mf410-LfWs3x96s5Hl5asV9aEHx_vHDgviqKD1IqAS5K6RbgoSfgLlZFGQYZZ2ngBYUXZ17MM14CzkpczwWP3XNjv0xgciUrsrDyyqA48T7TSonkreueR-l5FB6plGBxEDPm2koJWylhKyVspYStlLCVErZSwlZK2EoJWylhKyVspYStlLCVErZSwlZK2EoJWylhKyVspYStlLCVErZSwlZK_AiVEsZKcp7HcVSkyRizNPJ2pt57ZPZNRb5c7mdpxsED1JbfSMiZwv7UtJpEm5fybc9goEuZKb0UGdnt3buV83qQwBglAYSYaiQwX32Q2xahGPXCBDHA3GGYve3uXgImq8llBnzXYqCuJrUr8R2cRLhIQAI9HjocvfOntluXoR-dUbJX2NweMfpBXOiiMQND2rVZ4mrt-TcL1GQyDy-DABJALbTAyyCBmBQuM-ZyNgQ2R6HupR1Bp59cmlMLAEsH41LEr6fgo0yP6_y_UluIDMFVI7hGL3tG0zijWaJ4ALhAS6_Bar_QJ4xiYPC31suolMUbTU8KXTenfJIkT6MyycNYo1wj2WrI31NTpliUQBb7F6G7INHSXsc7OC0Nq8-utsMyWsXLNXgQ7xxZSLRw3v3hi89-_-r1JTg1l__x2f94p3x32KIBLD8M1NzUXdsgCFAhqXcV6GfMSCH7XHkOqmfdcxyz3yIR3cr5ndQ5EtPJogBYaKNSQLoxFEJd6JeAAz20RbteHFrDsa6iFqdnsglK_aHa0ct3JpfOiC-htOxysPzDTvifqHRXxzDH4lguQSyBGe4HzwcETIvgGmRTKG74UASElBCL4O5L1NWzxRvC1uYcVCulhpRwk-Apd2zbtqDpleGvZb2ILP7YT6DborRTRWnkzIxFabD1DXg6z2HxU0ZqDXBx7eBwZJGX23rLsahAxT7H6olNW4IfxssflvDu8CkHBSAhL_2I8fRDcuopU0pnlpBfhz7qaMIVqjgAkTMTrTAwAo77MXYtse56tbv2fiaS-Ttn9qTIY-7yNP0Q83i1xmhXxTuKWKIlb0lDjSnhCRQG59R59dr5LYja7aP5vb7ALRFgdLNPNfUwacwLXoVBlD542GMcPigXnnSjwY5_8cb5RRA7N4kMXCKr6dDtREKWFN1NSlFeZ5hjXWJuAEiSPXtmvkhOTr1FZIhdtxinPAO1Um_qtTgM6O633cYsPznCf8jyrGTxs2cWiGIDwkrSvbjCwLcI4L7LN360RNM1tWJzlV9FErKYP383Q6UgYDvFAcCSkwr8bgcU85oCVqBJbsF9QKMhkMCfZmaWRUXB4ix5xsx-ICa5RzFYPUD5Pop76nC8A9Kop1fznZrsiQre0Qge3q_LaNG-qux51dEfZkXvnrIcrczqlA08-SyzYBhOxXLMBBzaHJoQxnZ0NPNEobBhGY_X7L4qMdBB8UaqjkK2Zsw-dWdNu1RwWRiB1SlTNjOyCJbtutMLJczs3uCGfZqvrh51saFyjfgm1VbXa9S9xxfIsAfzTzqlToVrcVSlFnx1SsPPP-vffgeO7oEz8ObNb1AwxhTR6pSWnh_9hH6DaZeUWN3bC0PHHh_3N-Bi_JX3MpRiOoFbrQXGyN_qlJo8PviXOhmAlV1fcv4ez94G9pEW_ref_27ih4xHRVfSnCgop8MMbqcnEkLbB6JfbdIfZl57VnGY1hW9AU54XJyDrXx43XnkRmGZBlHlFR4DZZ6HUZJ6xJd-tO5cF9M-oO7cugbWNbCugXUNrGtgXYN_CNfg4T1d-y0t6WIc9zz-_nj7yo_SrxN6GcABt3TDJE8DHlcs4W5ehPg7MWFQuVHGPY95lVtEoDwrLF7JeIiNPFHhhj5_yMsdNO_E5250HkRHmneqMkuqMuQ_seYdNyiK1C0yPzdyqUead754BBb8CffyBHmReUHq8ji_p5dHgV_jEQOV1Kp-lxG11qiSebVbO0wU7P3zBMf-8wXYN6xsaivDsv-T1JxLUak5LqnGEpRhrGUyHVO04Kqt2wbbg-DNeJe3rCtJOz6nu-eimbT3OM_r7rloCAoqocCmpY7WDYeGFVo7JRvYElZhM1Z0Ug6HsiL_9b_-t0wwllhyIHAiShR8PtYDisAFfajM0BlWOfGzNbu9w8nqCADdiJdfNFcd217TB6qZynBY8ePJponRqa8WVgH_gMkMy_GWi8YEBnPlvH6JPUhFlru6jNtA4EbC8KkIej1QqY_q_oItpZ4MZ7vLQcmejS0OKhe-oDo0KVriKocK5kWidiLZMJpoJsIqjoNaobmCsdLnLPDckqW6WskA9AdNGQ-H5arMsiqqsACfL3aTsSJNI3VVZvkMvH0nAAQTwSCqeaE4kAw1OSoWtEK1ZIgrm5Svik4ZqizYsrpDXXHRvPsrpnHXm2W0CpbVGt7onahIwxTllmMWexB1H1QT2dWISqmq7Z1K_vbt-t3Li2aaX5aBOAoGaPGF-5x3JXaic_7-TP1jeROaT8bk5Bg0MO_tMaTwUg_fiMqpK6yKVd9zRM5OsPJwLUELqKQx6R8sKRALt9BLtoAbYeJGaphaJo5niKfp4TOjQd-2E9p2QttOaNsJbTuhbSe07YS2nfCeFhUXjrTLfFBseTLbTng09DTTWQiwIk3cOA9G_WmETs141hMjoQo8ZIAW6zUcD1X8aRAoeQHtl8QPSQTrl2MUDBZlA3sEYxFYW8PlxV2x5kt2ixsK4G7P31qQq7aE4wYO5xWl3ujonykTqM_AgrJNewh3ISo6yYsZweyX7XoEtJj8WTlvjPmJtUa4uDTb20SiEkCQKPgkBTTp6JFoSjdqjAtIIJ3sC28GuYYD1bYBktc-9hcSLMttpjENSijZDrDQimnZ8xGYw5tql2ip9lB-Jco94aCA2yhcSxzoJcKIlpKu-pE1ItsS9nQ3juZUsixfOLsLWiQEfIiURVvjgk4RoMCB6lyFI2qUuF7A-XjPx67USQ_B_sngURLHSeJyNvYQGCH2iQQ_LWJeiF0Xcu2HYLGxKN35JS2Y6J4Styy1zCwIYCCmgAVExXlDviuqSF6e3XZtc7UEXLjFfVBrcQa2BbuxzmApQVPxUgwN3gYqcv2j0GJR-BagNfq2Z-WOOnMHkHEQ-j3v_hNUcBV7z1Vp65mIq4j2wNGYYbOSnh_YO_gDA_YL00lDIRB1yaKlQu1av8uxCUI5-XLXZAMAqpxemDdwrr4UCVSjcwSF9q-8a_WzZTPdYuzCGIMiskVgZ1asb3aDbOGQ26F8EVG_Ko4RTn2EyzPCxFjk5RkovyioRk9DZ0UmwvS0JMd-FS841AJmL7uuInv8SzI4EmeDvAKQuWpaFFXYzWkxgUONxLJS1qEI29Bul77roA19qWq2S77UUqJa3M6ku7GlCmkA_UKPoZ6FKWF1wr84_-__eme_jN1fIZD_5N0kpOAMNV_mADOo5w9dgQr31PBJ8C1pf2HDEB4jukBQRfDypZPvanhNTyDosQSAPu4d_ywg0aAwj6gxxnYb8Ce77m65rVFURBH_dqIFcThUWUd13r9GMzsfR6VfRpUbuaF2j42s02Tnn5ZEUmaPLJ3Yes93ROBv2Q93a1pDvkSl4-A1FEbVJpcMm45BLsAEgwEGYAcnCpalhKMKZtL4G60mRQ6XKKHiUOqPsI9nOR4I57cUYsTOyoHoBC8ajMthk0jfy458RyZpFAIUPr2BL5Ui5SDCG_aNdPeF1rgA0HSj2877M2GZ_HDhuu64WeoJQvt_ouI2DYWBhIco6kemSk7ZZGxip9cTaoUwG0oOxbDL5QjPzqjYSuiQgWJCc_YlTrOIxVUQVhohGUm_D8G9ILsGcJnMcNEBK4PzFFIGyx1huSMsd4TljrDcEZY7wnJHWO6Inxt3RJXxnKdB5Cd-9kNwR6C7sM8fcdG0jfNs_oiJBzgT_Xa9ysuLLOJ-lM1yR0hTc6boxEezBbvnue7HgjRixgGi-MeATjYlKhs0AAUuDlZvYId571wDrIClEM4eET9gZAwWKos-dj59LdkrqBJhJLOgnlb040fuiSMgQObtN0KY4Q5yCg6ngO3kt-TqLmgCt6zbLCkcS4ZTvMMG7ZcXyaiUPEFMRumMO8jOjbfQgB-5K9e3vBSWl8LyUlheCstL8bflpahKP-Uez7zCZz8-L8VMcZGip5hUXAlENq27umjGwivLTjFlp9Bh7ccyVKwoQaeruaSMU_4G84nLim1qHMSs_ZJGYoaigh92nsnXs3QVT_0NpZ8wXYVR4DY-7EjZ3MO7IIy6s6eNOAZO1JBGvdIHmuSjm5_MBmaBWmHPvnrh4cJ5PsjrVy8SRB9x9OLrr08_NyiilPNk2tr0b7JoeTzeeN7u6Xg7edNcA6LLIjcP4mc-HS2N5y8Jh96k08w8usjqpBuxOo02Z_YkCYM09_YahZ42u4d3LwugpiJ8c2Kdln7IPe8DzE5AeqocEI-_ZiX5miLxRYqYEqUYFqLcryiVmG2Z42kRu9kHmJ3sI0CLoHJ2Em8Jl1Yki1SlPiAtUZpVzLWApWXoVfFz5e4NRywGt6gSbg37OBWj1T1mX0nVCmMPk0fDWDkfeTOzM3I94-zGeciw5w_WkPZ0uoZPhfEQsViVtiEYh4ZwKfPugAKwfJTqqeBjlaTOjy7_6pRxODmJL7FIo5fV44BWltLhNCJn_RY8v0p65QTNifJB_wTaceNx-rWFgIpnFntWAMfXRU1mMdM0725-Q202E4UxMhCsTtmh07NbMwy5cpmwUWUKspoZQ5ZjuYIoVBnrbiUCBCSHSFaU3h5ZpEMSh3sWScYQAChcUaeIIZq4Xp4_ptydeFpbJkOdoveAY0lOJxpWdNxU2AEt4KtTZ-vgOGnSkQ39RBJzdAmGcr_gSUuzYAsPDOWvV6eM6gw3B9NV3vu_vDR3BAyTOf_Tg6LBw3TrqLFjeSXScRMbOYLwYs1ZB6eCsji9dh11xZpZ3LI6ZS3vn9iYwXq4ZTS4HAx2ieMW8f4ZkBnTAjgeRlMUqaoPG8lMT4tu_MuOUdGIXJfVKds3P4_RsmF5A99sYURt46Tq71WpsXSlJ1pctclM9lkVtOgerlOm7_5FEqZrjB8oE7bQUbjRfVX8LouRHMes13CoeO7-35eUqkEdAYFHpvEM80czQTWBLGG2hmY3ncQR5KCj7LLvF38RbU2HWdMGPZwHJE7zgrE4C-IcVKZfFomb5n5-kgdE9-X-xHhArM9lfS7rc1mfy_pcf0Of6-EcU_tUEbFJFREt9GTPve-Ps0L8OJwYRe55ccG8Ms55kGRuxvMwy-M85kXkY2trmpVVEhW8CEpYeR7zpCiCNMjgSUX56Bfd58fwsnPfPfeO8WNEeVyWVZD9xPgxKuYluCpBlXkflB8DvWwq1Zanbc5MWJIMS5JhSTIsSYYlybAkGT8Hkoy4TOLIK5lXJME8ScYItX8aHBkpr1Iv5Dn3Ev9vzJExqXs84IU4bNBVBBlYBSxcPNn8TlwVqnX3oaQVf0uqDF3soOgy6P0mXBnUYFBjZRaAA2LIqIRxPsJDq3vsPjxvRuIyHkUJK8OAPZk3w-TLwDOB3e2dMykSUQV6eMqNzAAmb-Y4Npz7KTbAQhvFJPfybDinaDYuGsuzYXk2LM-G5dn4IXk2CjDMfloElcvcvxXPxsr5Q8PN3KbYvFvWi2BSObaayEToAjsFbojzyPPH_NYknSrVq2XssIwdlrHDMnZYxg7L2GEZOyxjh2XseDJjh6XCsFQYlgrDUmFYKgxLhWGpMCwVhqXCsFQYlgrDUmFYKgxLhWGpMCwVhqXCsFQYPyoVhuHZBoGb8yJimatjrkYDyqiBH9NLosbOsgA0eZh5qcZ-RnuJIfxP7RQRhZFihYWqETsBV4Pz3O8qcKBqrJsn1H8pMoz9O1X3O6ndEyV7V5Sv71vpz01a1GQwgVwbow0QdsM98wCb_nosh1GKRPWfVrh6Fw3i2DHupYJZRvmYQ_aZTkQWrZL4YyxM6FqlVffzhyI2KUIcU1jc70TgGI-DB9PzzMYRFZMT-dGV83tA9Khc4OGyJRtxi5GqJleKbsHcsg5x0ELBomKYTgYecfX36v9mpC_gpVvlhefGoZYQo8XHkJCnduuUjh-e-aHANOeggCjopsvhFhgKwvIGzEajb4HPkd8YZbXNTVuMhSQoZWYCTudibzHE4K3clw9LpZ1Io6mQM6XSJNDfSwGKJ6FPQlYVQ_O3sIeTnzMnB0pEQKe_gIle6ZzNciPfT_K4CCtXF2IanU3Gpjy1SWmM4ICw1Ji8psiKMAH_1Dt-uvzi179RZoP0NR_GdlYMhG8oejkui0xa3VKF0kT6nGnD0mGfLB5gmhyJkpmlhB0Siv4oEtCZtP12X5E2O9YYjPlXnfJXjvlWxwvwYhXGooPkPPAcZXERhF7i-nFUjQl43e41LfR5UueWoZX1z2VRMEsFlPHeHSZDJu3Koohf9SqTRMjsg0g8yTIDkOqtGSMT0iS3Cs6v6xQcxP6lE8JG0MGCBTU0llBVlMfHBy2cZDSu4sAgPKD3anUxVTTaERLcimtvn_JmF9JZyteYDKDy6V5OEmCNmh1NTJxHZX0Fk4Vo9CDnVqQTcXpSVcuogyzuByW6l8LENNmjhSAswauFg1qyRJ9bo6tOZ8me3iDnrbLEC7wkdlWKRZzcj8CuiS38DS0zaFXMuKBfQPCNcmbdjo6s2A7cxdFyFRS70PhO2V8pezm2igxjdOHIojhmC9BC9u8ocDcGGcY3lE0URhWxjK1i4eF6MHtSLhoRe3ginxj5iuenWMX2vt3jFjv4dsowRqHec9A416wrBwbg66dBN8abm7prmw0Br0FUTR1jHaP5P5V1zOgcGTsy51tT5tu0sV7WnW3Mfk5D-KkxjfqGDzfmB_8d9uf2hz-EEuApvdMPGPdJXc8PGPdJ_conRM_UrPDVR0G6ckPX9aMkiog2ABUsfhEdEdDjfEzG8TjJuWPQaoiUIvLX3JJl-lz5JRQSWOpGKlG6RgdKhWmkdzZMjffjGYCM2Qi9b3hnYE7RFbxJzshD1N4IRcqwz0960Kr1YDnJ6CnWj9Wpk3dyTq9KMaG2Y8WaSzRDhp3CUYh8dUm4yZOEUfta5PAlaAUUrstNJOeVgn2rU4d3ZqnI5RJrLoANxhMm0QLsmhsDAyKyQ7tqBBgO77iPTGh220afS_nzEuecYhOSc4c9NZ3I48Q0h-w9s3OR4HqpS5wbrO6nSY1GX-Kvol2XZ5hVUdp2Yc5uhOfHJ3ZI5zM7MXTLcBs01iPnoTKT5wSPkzM_nVDZUCHsepq5n2fumZ1H5AIuWq9Zp_DVyI0jwJ9k8hmjbgU4ykz6PuKk67QAuGcnqXuEqFJhLDqi6xpnr0NT_Sijo_jsa6MjYmS45wuzTHihF3Yhixnp5XRl7OMYfLIqCzK4N468mAEKivIkr2JWnGLw0cwB9zP4WPxi8YvFL0e5TWZ4szTlx0j0kX5_nLvjR2ExiVmaVUkaeFVaJF4eZpVbMT8P3CjIYAGSogjhbcIsDIM0TbIwZVGacT-PK0xCZu7pV5rylaRv3eTc887D-AhfSZWDQId-YflKLF-J5SuxfCWWr-SD8JWUbpmlPPJ5kLOfH19JrQ4dq8_WCKWDlSty_0swZO_0_H4PjxyYmAiWx43gW7KMPJLgxDnJb4KVCQ8mOCFXFcVjrWPBmkFDdZVgwuu4L6seZElQLAmKJUGxJCiWBMWSoFgSFEuCYklQPiwJSp6Bg--GnFc-_wcmQfmcxnoyC8rnMpr5JBqUt_pHRVQt0_QekTpbqAYnY-1Vqe240vKXBHC9aQ2xkFCYFHqLKeeKmOAp0hXnKOeKyagiy9j3SVVeThJ6-MLalMofnRAkK9JPNGwlZtXQh9L16Ptljg9kawE_5Shdi_NYthas3z1B1-I8kq1lpCg5TtfiWLYWy9Zi2VosW8uPyNZSpC7P08xLquCny9YyNcCSmmUhxQ8O65sgXpItVN8YDC6P4295ixXYo-iJIlBZOKI64GG127UOMS91deyIfqg0RGODczSyehAyOmMNipqJaBAUFSnGudJbKqllQNI1t4zzbGoZLPwcuWWcGWoZfD1kTJEtFPSUpaj6BQuoCo8_EXDiKNWM8wimGVX7OUs18_JgX3AIjRZVeQ52rFJQdq_-o7dUNZaqxlLVWKoaS1VjqWosVY2lqrFUNZaqxlLVWKoaS1VjqWosVY2lqvlZUtUERRakoVflXmqpaixVzUhVQ-nJv3euGhfGcLkbMBbzea6ao62Sx4hrzHa4M883STG8OEFPV6ce4fz6QXxQgrxwAMGb6T5KTofZAYUMmkBEwsI7Q88Ni1AlLYE4KqKjTZyFJYbNQc8bmeW9pCtCF8PRNGITOk2sOXuoKRPB6QoWHgM9oqpPhMjw7VcuvCxljpeY2jz6CxmyylO5swiKl8KmretqELQzOepykP83I7yHp1OU_ijOBhca1sRdxd4huF3M_GCGwPJd23MHOXjUHcezvDi1i8ZdJWEUUY0IICB3lfoheACf7TP9aHYiWBMqJxgZP1Ap9MI1Rztl8rWYBDvgpgnnkbNuXcOx-lyMK1AZBe9UeKUVkbGLRpb4asHFMynhFcUjjAo2LVhUymaJe35WxD0-L2OWem5VlmyeuGdkgTmg8KHUIwpYFiylTdxQDzil9gdVCyKWk-52_ETkcUW6PxorasboVwGnqaceXIUeBpGww_J5P8GReH-9LFBjqJSmloSXB-xYpA9gv2ShEphKesCS7rxoVCD_3wHGYg8LXu2ussCL4YGD8_5fooVICB5XG-Ly1I3iSTpffBynkb8wEY_4OEpCb2XsNkg8KAJ6CF6wdFee74YXDa3R1JP_Cr4MQj9eOO7XVH2wI79SKE86_HfONWAkL3XP4P8lUhFrhe_avt9JiiVksfGjVRiHS-GOU5gb55p4K89N9adj2PulWL7RR4cpwnzRM3f9yI0x0yZdOVlZYkippF9DljVWiHS0iqaLi1CpIR1La6yM9qNzPIucQM6RINBcNBCAWVDGeVkVj2c7mrZbG9omxYZryeZDNhqttucjL400qpL8wKQ8alpnLwcnCnxQy5JmxjDOUmveCwkRdrj9wtrKeKvwv-XZICUkcqHGBBM9wZeicoEeMMly56AsRcucgmv8m2u26wdN0ECVCLftsiN0KkMV4iybDEmrEZ4dy3ariborP0lSVSVXofNFVaXaDoZ-EBDOnUvG694T7MzY_00sROIyhLXkXYfJULIcMp97Jz5U7o3zb2CUVf6Y1kcvCQgPWTUMKlKvHJYbEIIx6ARFhz6dTi0xpRE3M7o49kC9idvJD91Spl9GvcdUC23gyvnDNAGtiAtNW2wQSMnOHtFMI8JT96LlEH-Zzs-jysuyp9BBUdGU8s9Ew5dwV08xRYEIaaooswPYzHE6H0UPZYrCqjF1GDH0q4_hnoclF06yBx1Qro1kjhM2KXNTJ_uIvcgOPlE6mgYZAl4rYqI0nniNCRECZQvOTZRT8oohNMNUH6rMl4fFDOJz-u0gURayR5cxoj-UvpeGujQ8cBk5pyuwgfMInZj5mi-n3Fo_FzKtT0_QaH16gkDr01PUWW8EaZbz9qfDmgVqqroESeDdD0GXlZShG8E0HszTwMqSprEVeUX45Kuzs6_PnV84v2zz85vsGpwPbDPCQAQhx09Eb26D5T2iH1kASorBdfMUElWe0MM-zNS4j90oYLc2ck4iM7SE03STOfIrmcIDODBHFlHmlReF7ENObeQGgtm9rvYACeoCLg2R589Mzci9mSQZe_m8h_NBGJmup4ynw-V66Yqw4GnIHzTefcuma7BgyZRTvRQbCDu6IbMleGZuEjDyc68Z-3ESUBvkw2kv7puebPgWt0mZg3khTaSIkZgJ4L_s5nbVAwcuzsIPOj3hqExmhw0n5gk2yly2Lx5EMGYolL1pjNxZMOfJQ7SFWIrmFfKiQA0vBVuV0QFjEGgp-99xjKQLTN2DdaARZaxpdUqhzE1t6lwLzYANed0RSiZ44JZkdnVKP8w9Sb8NzFiFzT7zP6OR4W9iykKthHr85sQ6rE6drrkHw0vRGhubsFSB-slR3BveOCXHh38j7azmOhhlHZ45XT8V7patoGMSY1zZ48xaxmF44Cz8hCIZJyT7kHlsXATyV1enNOxJQq1PZfeXROaKx5d1iKpEvYuoyzXKvNv5Q4HO0eqUaj7NVCepd8VETMHG5L4MpR6TA91aoBq4qWfCjNGeYPb6o-iHE8HIA518Suymsi2K-MSD0Q-hwbRIGeRnU4nSrayP4fIKKs6qIE-Zn_peWhQ-S8uojKNTXF6aVed-Li8Lriy4suDKgqungauHcw5qqjAxqfN4YZCG-d8f5wT7UXjQvLLwGM-zKiqKKAuqoor9LK_KqvDLNMx4FYZ57MObcT_NeOIWiR-Baiqi0s8YD6KHvNwBI1p27sfnbnaEES3hXpi4GbeMaJYRzTKiWUY0y4hmGdEsI5plRLOMaJYRzTKiWUY0y4hmGdEsI5plRLOMaJYRzTKiWUY0y4hmGdEsI5plRHseI1ru-rEXFHEVsGj0tXRqWO78szK9N0T-01KBM67YYSmMAIQlLADWNwOMEtXYAqcZ5SSmNI01OEsUORIh_J2uQR67JW6usNjIqDBukGwzk31-B36f8QjCZuPoBBoomEYuM1HAYHJJ0zaBBsvpK7pxIesD8LKrdZsD5BYRBaEM1rBCusGHrFcvexkFj4mkRRJKRZpAQIzUfkBFGqN_IIbdMvqV475dU40m5QX0-o_EDbDAYjb6x8xkCQPWtBCpguq6gwOB4TJ8qryDHkQO6tjqTr_A54AzLpCsjDTDyirPdZil_bCMfJaRzzLyHXTFFb6blDwOi4Abp0JVxRzVyo8scsESE1I5k-KJiRThSdcex_HaBWIGWqhg2_EGIhIz1ZpDK0EVi73K-ynncM_zMlwrhNILIbm6ox0HpaZfmcRQlVkr50sdIK57ASha2uK6OCfKGQo2HOL2TnQOUE8PXHLgCCwc9dVpD4IETz6D8PtYnWJG1nVvLWG1nAsCHkk1clA5htWG0vCoQkz5u5qT3cLxsUBTpPBnWy6TKE2w6TLXjC1GXdMp4XpMmZL80VJUi0LD4sTGXllSrDcJuXlKlc6oWRJf4w9Tmao_SX1dNIahkorW_H5a4SJQom5r2v-hXBjM_KVco7r3sO1JQIfPbkRDorxQ5q8QWE7z1EovGtks-nVVxTJAp0HovUMVByL1atRpRypxxTJrPkHZHQ7-FB89NqMRmV5zJFoyzp3Sykqng5Ohfsf0oA9aFjxT_ryhPPSYXddtb5aC1FKQWgpSS0FqKUgtBamlILUUpP8IFKRBkJdJ4QdhEISnKUhPB50eRkkqDrzo2gY4h-pAlSgoXlLnSbSkONJIXPRgWtKozF0v8vzQz39UWtITpKAfipdUAE8zmEcwR3QCkiom1aITJCd5TGkOj-EypQN2ksuUhhv5TGfS6FlShjmL4iBLXK2Dx8aMo77fI3stQNzECZxIm_IJdcQOGU8x-6i2jplNXzJhiyCPjKm-ync_PvRHdLslU5xdpERqDLDeXoPZnPj7ol1d-AR6g4iQo9-j6bhoxMeK0aJGfj2GBHwHJFnkyEu_EMV2cRg_uGiUt6_fxl1lripNIXlUrofK4rSSGXaDtUU1mRbh54Hav2iwehCeghyaGyxzFPlPtRjocpufm9hD7BJq20KNQbFjkwAPUxC087Oljpbu1tLdWrpbS3dr6W4t3a2lu7V0t5bu1tLdWrpbS3dr6W4t3a2lu7V0t5bu1tLdWrrbk3S3ceUHLIyqWCcdDT6ao9HYR1LLHD9JOYJAKdCqHosq8vcJ7HDE5RpHnB6ilQI1gwJLYfLxqCUUFtD62iwBG-_y_VWAsVIpi2m6coOPdcBHbjLWCSkJWZmDCO0LViCJjmA-fCLNERR_jBF0emcKqWOEg1PwlXTgS_EV9ahTTJlLg2WifxmMv0lGbassnYgh7ON9DVjEYThVcSbhxphygJOZCKWtQjP7FH9jCbiJPDTb3whYCaYiUQ_6FqMzkB36Qaq_fnQ2MNPU0KnRpVsvZWSI_MpjlWoLSUKiIoVY-S7A4A0fwe79x6JwgzyokirwXN0-b_AgHa9Jfxyl0aQ8vTSqrpJJTwOuix9dNIdwibqtjoEliV3MimnR7nAyxSekD-bIb4Q8A6pxTjQvgTaP0TE9zCzhdzF8p0853dnvqDxXyCCisX2YRqIEgiLOmj6vYEXBHcGbEAGNFVG8k74l7KfIjUlqCFEjJHA1-FpnXjDJk6FIyKL7SqXZdk0NmEYBAKPQ2MRzHTaDZQKhpf7Ki8Ppr_b1xH0tgPuakV9wgnRbvulEIkZvft_LU4hpoekFjRgSbegYQBJAStR3bqji38zTWrpzS3du6c4t3fm9dOc8ToPC2-OWfC7VH0qv0UmHxcMHBf2yUWC3deqH8SgbM72H5HYYHacgXiKwpmL-pUwDST5ls7J_OZ4lA2iLUkiU8uUawxQqpaJ1zGLCJYedaCZB7zEuWDHHCXvrk6ZGET3CBViemo02lCYqSiE0OJSDS9rghxPBRmmWZwmPcj8JkN4wz1kQ5USZdZQIVpMJ3k8E-xMVu4cz4e6TMHrfH6dV_FFIJXNQHyz2MlaVeZEkzMsjVuZxztKKsTjI_LTKAtcv0iwKK58FVZGkKY-4m8Vhwaj79tj77PNIeu556J577hEeSZ76KQt93_JIWh5JyyNpeSQtj6TlkbQ8kpZH0vJIWh5JyyNpeSQtj6TlkbQ8kpZH0vJIWh5JyyNpeSQtj6TlkbQ8kpZH0vJIWh5JyyNpeSQtj6TlkbQ8kpZH0vJIWh5JyyNpeSQtj6TlkbQ8kpZH0vJIWh5JyyNpeSQtj6TlkbQ8kpZH0vJIWh5JyyNpeSQtj6TlkbQ8kpZH0vJIWh5JyyNpeSQtj6TlkbQ8kpZH0vJIWh5JyyNpeSQtj6TlkbQ8kpZH0vJI_mA8kjyKqiQJABeNoX-D1uuooD-SoauXJk7UWZNvr4nSeueXn1MjpVKqsl3xy3b9iSokoepso_DW0Y5uL3NrAFhUs78RLxIqCwbE3j9YvrIuBCxdOCDd07gKWdG9yqaxPk1AuZUIeYwVXiL1oKOT1MxIpiPyzw6eUCieDcIxIV1RYfZHz5hOeiY_J8OBin7N9Luhx6-6O0VfnEoHSi46jsB8REZmBEUfK1EW3zq-i0_6ZRCtEu_jT85hzlNjQ72VeJAknBCL6YSZanrCA4QlwOTcal0hMti6AVEqdVEgTTUB0uy6woBMyPCU-CtGPDIHFMzGAM9IiYcLrfeB9E49YggZnOmv2ZaLTBNlbgBXgsID40C0EKMhlHIBUiLSq3vxakp_tmtOkXwxEsovYXzxBsQXOB5iQTlFQEbYN9mEqbigRNhfNpk6Y3RFCA-aK6wy0T2M4i7s26aVkbMlTh2GL0NYWDxLLKxehv6WbVUSVRAu1VSJJy2oSOSQYx3EAmMJr2ZEaCSowhcQgcKFSSWEf1w0ys6eUHhCAj7yV76XRYkPcjdIZjZBKmv4QRTTQuO5odUY-GY7WP5by3_798J_-_X3_x8Jp503)
