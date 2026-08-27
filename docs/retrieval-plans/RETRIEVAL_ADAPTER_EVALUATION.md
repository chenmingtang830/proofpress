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
`zai/glm-5.3-flash`; the independent coverage critic uses `gpt-5.6-sol`;
PageIndex and the primary executor use `deepseek/deepseek-v4-flash`; the
sensitivity executor uses GLM; and the native grader uses Gemini 3.1 Pro.
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
12 eligible tasks and 65 frozen rubric atoms. v8 uses lifecycle-aware GLM
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

[//]: # (ob:3c58ee7a)
## Bounded private result

[//]: # (ob:a0a50b36)
The 12-task v8 construction run produced candidate artifacts, but every task
remained `insufficient_after_repairs` at the independent critic gate, so the
authoritative completion denominator is 0/12. Diagnostic receipt scoring found
100% evidence binding and receipt validity, 95.76% macro locator-set coverage,
and complete evidence-set success for 10/11 tasks with locator silver. No
equivalent frozen PR #36 v7 comparator was available, so replacement remains
inconclusive.

[//]: # (ob:7438b197)
The deterministic disclosure and assimilation panel completed 24/24 cases:
claim selection, traversal, gap detection, PageIndex invocation, and
recommendation metrics were 1.0; blocked leakage, automatic admission,
unauthorized mutation, and covered-query PageIndex calls were zero. These two
safety gates pass their preregistered rules.

[//]: # (ob:68d24e11)
The frozen-gap panel had ten tasks with gaps but zero silver locators inside
the sidecar's 28-PDF custody subset, and the attempted PageIndex builds were
inconclusive. The corrected scored denominator is zero and all PageIndex,
hybrid, latency, cost, and stability quality metrics are null rather than zero.
Supported-adapter promotion therefore remains inconclusive.

[//]: # (ob:cae8c609)
The corrected workflow runner bound staged claims to exact construction
retrieval receipts and supplied non-empty graph contexts within the 24,000
token cap. The final panel scored 4/20 cells; 4 lacked an equivalent PR #36
context, 7 executor calls failed closed, and 5 artifacts had fewer than three
valid blind grades. The four scored cells were DeepSeek-only and do not form a
complete paired panel, so legal workflow value remains inconclusive.

[//]: # (ob:98d41f66)
Retained Gateway receipts establish a known cost floor of $11.97131760 against
the $100 cap. Failed, timed-out, or interrupted calls lack complete cost
telemetry, so the exact budget result remains inconclusive. This private,
staged result does not establish public PageIndex support or alter admission
policy.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzUxNTM4OTg1MDI5OTJjN2IxNTc2MWYxOSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjViNmRkZjM5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82OGJjYWE2OTM2YmJlZDJkYzcwOGIyYjIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzgzZGY0ZDJiMDhmNGZjNTQzNGYzY2RkNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfelu5Eh27qsQ6hl4xpML90WFi-tyL4OCZylUlz33YtSQgoygxCkmmUMypVJ3NeBffgDDb-D3uQ_hJ7nnnIggg6lMSpWqXsYm0KiWMslYTpw45zurvjtjTVfkLOsuC352frbdXgZO4MVJHNhukrhZlDpBFDq5k5wtztKa31_y4lq0HTzb3jA3CM_9JPCE7aV2JBLfZSH3vJiznIepIyIu7CTlDs-zNOROmonEy9IssCPXzkWU-1nKYFxetFl9K5r7s_Pv8JfusmPXMEPJOpxqAT-kooQP_kU0RV6wtBRWI26Ltqgr6waer5t7K723Xjd1nW8b0bbwzpZl79i1wE2NPm7qvwjY7q7BAW-6btuer9fXRXezS1dZvVlnN6LaFNV1x6rr2LPXo7cb8dddAT9f7lrRXGZ11YoKaNE1O_H94uxGMCRiAHvluYcUw08uxS09BMQVl2GcZoyFiRemqeAuzyI7Tt3UxZXVTYdbuyyLSsDK9YmUl7HHc5-7qR3nfp4FvufnXsZ5JLejVneZsW27K2HDLq4zqxvenp3_-bszNf13Z3DKddPiT_JrwS9TIPmfz7Kai_dn38AONDfAxLzO2nUjuqYQt6xcbktWtes3X7598-rLf3n5u8uXX7x8_fbLN5f4yz-_fPvqj39YbfjZ4qP4iXUwerrr4BgvU9YWLXKVKPNL1gJ5O0Hj7bqbusFFvysqHLK9bzuxgW8qtsHTlYtfwIst8sPZebUrS9hKdgMHKCQJ0rLO3sGzbh4xJpIYHoez68R73OgbvUeLcbbtRGPhLzuGy7L-61__wwLyNuK6IE5Ui2Cc0-q2yIbiDj75zHr6OPA_biFBYYTufou7QEYBpjv7fjGsNhWJE8V2MFrtFyKTfN8B45sztLstclA7ucjPrKe8P7EmlrssCX37063p7d47HAbjorXubkR3A0Rk1mu4DK8qOOVlCncaSKfpWwxr3bKGjYnnBbZtZ-looZ_XG3gQRpBM9BitDjw-dVxwVg5Iv5NnfHsjTEI0u6oFigqrBUa38qb-VlRWUW13nQW3d7trF1bH2nfWX3cgFScoEfq-44osOXldH6yv6SHrg_U5q3jBQSxb16ISjVzoB2AqsbXg5oJglR98-X4LP8Pww7pIto0WFvEsYzy1T17YH2pLbECM4lG0FrxlwaudVeeSEYuq6Aq4jhkNWbR1tbJe5cBQrdiwCYJFnuO7WeyP1vWVQX-Yq-KggUD48l1WpEVZdPeP8NJT3p9grjjiIDQ_5Zq-ZNkN8pildMX5FEWCLA495n262ZeKh60Nq4octPy51da7JhPWP795tQBlDiwmkcbC2gheMAvXtqBphoWWKJTNhbpuZsdsj9eftVC8lGqp-CbdOL1myXMAXFD4oVxSuq9dWS8t0D9T4inPo8DP8tFCf48aJHtMKg1PTfCLyPMkc_yPHv-NQIENYgjQGBAen7fuABxZ1W6D971uFiChqxoQkvxFvM_KHe6_XUxsN_AFs52P3-4HtVuSMTldaJIvf7q5t4oODqIDPdBaHy6qD9ZyubRG_07KngwQah6mH7ugl5W1q9gtK0pCoZJnF_BZA4dAH-VFCR_UjXVdl3xJyNVim7S43k3QRzAQhr495tuX_C87XmRSyCLzsaorlqVgiGstfK6py8e45cmDTCn9yONBEDqfeHW_BQJZMAUykrxKGVARtUYq8rqRGF_cwWqUMrDqXUd3-O5mgpZgYICtkbBPvNrPpRBQUkrKppEKFvCbRiYwYA4nrhQknxKt3PN55Luj1YIhs6kVCADGnT7hBw9PnKSbBEkcBumJs_VIDG4eiAew2RCXbEAIbIEAG7AzDPTb1Rr_EWSboEHM0yBkfnTiqpyVVdXASHcwKRcwNQgnUAwgNUC1iWLbASxoWwsOQ7y4qNwVIAB4GXBmCTw3oUzsMAydJAlPXBZqjkaK082u7az2pr4jPAcaYgd0AomagvBCXbGtW5Bst_g8mHCd1UwQy3VD182Z2EPgJbzeoAB63AAYPTrBLIlwcpvRCB8_01Ij1qPKE85iaYHe1JsmIW0BI1nV_qF8s9BW7JnStpdKVJypb7S5KS4jMFBs1_MjJ42zOEq8SAg3d9CKquqOSKoMbUsZ2qCqRfZuWxdVR36DhmZCM1L_hlbkN2ihl0V2b4xgWu3GIOQPONGgb-u8uwRNdy2abVMov0GbOudBmiWRxwQwZewEYZSA0GBuFDk84yLNOY9Z4KWRGzEeJxFzAQWFuZsyWwQO4wGN3bGO7H95XOeuD3YyfnLm2m64tOOlG7517XPPOw_i39j2uY3YXFEctXjkC0cEOXDJ8Ol3P7LTgLhTmvU3rL2B5_3UzUSYJsxJ8ERoDMPSV4z7CQ10NW-WCzvNU9vP4ljPa9jset6TbW41je34QZIHeRoHoZ7GMMPVNM8xozeAhm8Fvg6vVJm4qEgr4zCgh0lmpfUOXuWGi826q5t3Zc24BXBwd32D8v4vIOeK_N6qt2QbguIuutVF9aqzeA3jw_1T6zKWtak5IqSqRfENewB5AWIbYP_wCEgfBTLhgYuK8U3RtkWqcFb_XHXfbwlk7Q7ARXpPkv9mB0JHoYnVAdGqCB3A2hLbBg3ppf15Dm6E4Tyf5hdQo6Z55kVpIODuOv2og6ugP77TbX8CHmTVkLa7qFqQRRuwmG4aeTA3jRCoo0F6FV15b6HnrF_8-XGCgPoDK4KJwBOBXrrhTVBLf457QKG_IwBe_otfXZXiPaC3cpnd7Kp361vnCr4d63r1BHBatkMkYrUZYsgPFhwpvAZbywiZ4QCttGny4j2sAT3PJdvCk1e4o8t2y6orNe0W7kxBd6YDGqp5BxTUyh3Rl_ALa8Ck_oD6rC5vkcJqw3g4OFKLc6gP1TSwd5pkNOvNfdoUXM0mF6l39xuL5tpVGoE8oAPIMFa920OgH8h8HugNhlN2g_eTeIxORkizWKBHW710yIBSrOEmHmN-CJqWc80ahj9HscZzHDQVbgaW2g9wUSnFIuUEyCyATbgn4DcwRMEchE8ZSKxdg_aqwePytAswHOq7St2mi2pMITyjjFUoopAh7poCuBio02p80k5Ijjj2w8jzMs_2e01geJEGyXGiF0hN4-RhZkdwH52I6WkMx5Ca5imOHX3BM557gBLs1O9Vi-HrUQM-x1ezlebVDu4jyOkGVItl9eYzIcARKISRJTSjT199sSAJd78gC4N4VFvcODha2IbSsnr2hv-YafBhLEh0NJ3WEMgfOCxIBe3BWSAD1BXdsxFzyNlGH-Fscs806obhdRLL3gtwNQRmDDyk10pXW4nrlnQsOVxwUHh416AzKdOydEF6s65AcONtBXsYRCvNesdKkIiIh-gSVBkQSp0MHgrdkQxWILjcAbOU0YObAYsEpEi3OmAAaXwDGNpOsjhnPO9x1eBgMzTXqQ4yQLl8bFEvLip14nS45D4hLT--rcAlDY5uVeJuT2-inYdwoIPhL6pUoJTLYSyYCeB0TcZfUTemF2viZvtJmEYI0LMg67X34LsbbvakV04Nxv3YDxywRkTm6sEMR10fjzrdBTcwqroTsGXRIOSl22exLYIA5NCJPecgDlzfSXiQ9rLdcOD1av8Zrjn8sFfUcBGAkf_hHXxJh64YAtYKGhW1BPF9XjTAsu-Ge4HaFH6y-usFP6How4eb4vqm62f433JCLR2M-dhw38YKUoECCcJGckbNWnQPpgODIRNqrr_uwNa0UsAOyH_oeiBgoOaib1u8GIiW2TUrKtgbjFQAo5esQNUFVCbI8lAtSzBN8yr_Bs5DewEiADeA6aj3DIBPicBGGyEfBtlIg2t5o57EkVmnTROahu40rctaW0C60QDDezDwbV3wlhgQGBI33p8NcbAeVJ7_tKuG6KUkJMsysSXHoJSBn3mJ9Nmh9F4DRCg6uRf1_Ae4N6zdAdW0KVJXsAa8DNeg2O_lAraBDS9vk0BLT3hPVHzZ1UtRGQLY2AUfAJU5MElTQjWiVzCS_PgFujSIhB8G-Yt8VqJce_n61fAUAqFS4FbU8xv2Do-6YVws6zxvexQ_Cc4SO88D3wd8FvdyxnB4a5foM1zZSENAW9K9hYIdzLKrotKG2q24GjAXDAfI7oUCaBXhtxZGrtAUIZCO76MlCFYdzIY4D12LXPoWkaZPk9VxkCZMZCHPnd4PYDjWB1n9HJ-4Rk4BY7bPAs8TPeIz3ORqrud4uFFc50A6tHNXIFURskpDdgRt6BQoKQWUvBwOxW4rhMT2SpZqzZyCBYlwAr5DQ1o5AIC-HR4pCkcwHlbWWxK4FclUurGtQGqj0NqzuuTmLiqSZXpRdHD6ssNir0nO4yLoGw4wvAU7hm0svSOy6AH_Hz_dzE15kgme2azHqoarvw8fn-6l1w8TLId_6g2Y0kJweXLSDlPnNigkxcAAPADTVCCeAFTBce5a0Rp46wLMxVtR1ltpmcId7l7QIDcCblZNZr22gehIAcfUqGxY_nCh6AORRsyUMyNO8yx1hJfY2WCg9bGG4TI8JXygxvSc3I_dPPdZGPWAcIgoaA_5M4IE8kPCukUOogd4fo9K0vmBAEMI1AygjZTgBZBX1ndS64BAR3d6V4NYeuA6mDCIeMBTP0jcJCeLSlpYQ3RC7fBZAQcO71bLSlzLJUoUjCBnH568QEa8qDyaDKUy3W3UcteNzHXCtx4q-IWp0hR2lvoF7QslBsR9jSIBlfsNjHYDgqrVfiaS3L3e11h-wlAIfQ8wcZqmQdLzmhE8MQyFU-MhYMlugHNwjWjd41ak2dwppU40IB3TexrZrqsBheLZAzspOhv-S-nNJ4WD8qcjB-LgapwyCoI4Dzlz_DD3B8OoD8uYjt_HYi3aSRh7LA7gWjlOb9kb4ZfeEH9GTMX0h2xhi8Cedz2_9oaZtJGtHFABwCerFPya5A-Kd7hZJKbx_wDO0acDN7ECXFQM2GshudayTDQAWArkoRobzr2RfmDi4Q0oe7TnyF38ToitVGOtRB4AvQoUvsoNrSTEA1785nsk5oFMR8GLbj_PkbImgXcefn44L1KmfQJ5-y8w-_NvJV8SpDHFtU5Jl_R4nngB2wuAFrcIigcfP3kZABk_HqieenMiEMmDMI7sB1Hrk9ZBUmhXVfJisAogLdCnuafIHanWq7YDeCXaNduK90si3xKPdG0u80FYFmBIKACMfKo1KlwxKFO87NIxDMvubnrYR_dCmhMtALn9JQL3kuV29GT3VqFipGTSKytzq3ahpcwCRcdSIlWJllqG5v-3gi-VgM9AwNf8XoaNWHO_Onaeh2d_Iz2Xmgi4r4w1escIIaTwQzGFDjB0A3eiFOgtubeAk3kJxF4dO6DDk_4TyJ7W-h3YRDo00qNeCWBQP-S7DuXiW9E06KauSE8hdCZWWkl66_P_7uzu5r7fDtFSvBfZTkllRdaXr7_8P4oTe-4A_F_QI2D3N7eSceTThujPEFNU0oMu6Y07fnqkPIndIHa9QLh-4qe5HdkcDBg77ElihsDN8K8ZFv9ulhz_fSXH01Mr9lMLvO8PJw48lkXxSVIlwEThdgYWegTmYp5x30sEiz3Hy5wwcUKRCA44K7IdGyx2xw5dHsHiOMsSP3e4lx3ZzzhTInpr2-dBfB74BzIlWOiFjNlzpsScKTFnSsyZEnOmxJwpMWdKzJkSc6bEnCkxZ0rMmRJzpsScKTFnSsyZEnOmxJwpMWdKzJkSc6bEnCkxZ0rMmRI_QqaEQUkh0jAMsjgafJZG3M6Uex8ZfdOeL1u4SZwIsAB7zW8E5ExmPzWsptDmpdrtGga6VJHSSxmR3d5fraxXnQLGyAnAxJQjgfHqB7Ft6YrRGyaIAeoO3ex1c_8CMFlBJjPguxoddQWJXYXv4CbCQxIS9OOhwdFaf6qbkvtusKZgr9S5LWL0B36hi8p0DPWmzRKptWffLFCSqTi8cgIoALXoGV45CeSikMwYy9kQ2ByYulV6BI1-MmmOEQBIB-OSx68l56MKj_fxfy22EBmCqUZwjTa7pmWsaZXIHgAuUNP3YLVd9DeMfGDwey-XUSjLHY1vCj03JXyiKI0DHqV-2KNcI9hq8N-pIVNMSiCN_ZlvL4i1eqvjCm5LxYr19bZbBqtwWYIFcWWpRKKFdfXH11_-4eWrSzBqLv_py_97pW13OKIOND8MVN0WTV0hCNAuqasc5DNGpLD7HD8H0VO2Asdst9iIbmX9XskchelUUgAQ2sgUUGYMuVAX_SbgQnd1VpeLh9pwyKso5O0ZHYIWfyh2evKtFekM_xJyyy4Fzd_tpP2JQnd1CHMsDsUSJAlMdz9YPsBgPQuWwJtScMOH0iGkmVg6d1-grJ5M3pC6NhUgWik0pJmbGE-bY9u6BkmvFX-h8kVU8sd-AH1OSjuWlEbGzJCUBkdfgaXznC5-WkmVABdLC4cjjbzcFluBSQXa9zlkT2xqDnaY4D9sw7uHszxIAPEFdwMm4k_ZU0-rUrqzhPwatFEHFa5RxQMQObHQHB0jYLgf6q4l6d5Tu6kf70Qy_ebEmWRpKGwRx59iHS9L9HbloiGPJWrymiTUEBIeQWEwTq2Xr6zfAqvdfXR_r9d4JBKMbvZbTT2NG9NM5L4XxE8e9lAPH-QLR5nRoMdfv7E-80LrNlKOS-xq2jU7GZAlQXcbk5fX6qa6LjHbAyTJnr0yVwYnx9Yidogta_RTrkGsFJuilJcBzf262ZjpJwf6H7I04Sx89so8mWxAWEmZF9fo-JYO3Kt04wZLVF1jLTaV-ZVFPgvF80_T1wICjlNeAEw5ycHutkAwl-SwAklyB-YDKg2JBP40sbIkyDIWJtEzVvYDdZL7qA5WTxC-H9V76uF4D5pGnZ7Nd2yxRzJ4ByX48P0-jRb1q46e5w39Ymb07gnLQcusjunAo3OZCcNwK5ZDJOChzqEFoW-n92YeSRQ2NOPhnN2XHB0d5G-k7Cjs1ozRp2Zd1UsNl6USWB1TZRMjS2fZrjlOKKlm9wY39NN0dvUgiw2Ra_g3Kbe6KFH2HiaQoQ-mZzomTqVpcVCkZmJ1TMJPz_WPvwdD94Ex8ObNV8gYQ4hodUxKT49-RL7BsjkFVvfOwpCxh8f9CkyMb0WrXCmmEbjtpcDg-VsdE5OHB_-6DwZgZtfXQrzDu7eBcyTC__Z3vx_ZIcNV6TNpjiSU02UGs9ORAaHtE9Fvr9Kfpl5blgtY1jXtABc8EOfBUT497zywA5_HXpA7mcNAmKd-EMWO6x7LO--TaZ-Qdz6bBrNpMJsGs2kwmwazafA_wjR4ek3XfklLvBjGPQ-_P1y-8qPU6_hOAnDA5rYfpbEnwpxFwk4zP7Nt7nu5HSTCcZiT21kAwjPH5JVE-FjIE2S274qnbO5B8U54bgfnXnCgeCfnSZRzX_zMindsL8tiO0vc1IilHijeef0RWPBnXMvjpVnieLEtwvSRWh4Nfo0pOkqp1fUuA2otUCSLfFdaTCbs_f0Ix_79Beg3zGyqc0Oz_52SnEuZqTmQtMcSFGEsVDAdQ7RgqpV1heVBsDPRpDVrOEnH51T3XFSj8h7redU9FxVBQc0UWLTUEN1waKBQaXHWsSVQYTNkdFIMh6Ii__Vv_64CjBxTDiRORI6Cz4d8QOm4oA-1GlpjlpNYl-zuHhfbewDoRXz8orpu2PaGPtDFVIbBih-PDk2OTnW1QAX8BRbTLYdXLioTGEyl87oca5CyJLX7NG4DgRsBw1MRdNlRqo-u_oIjpZoMa7tLQciuhxIHHQtfUB6aYi35lEUJ8zJQO-JsGE0WE2EWx4NcoamEMe4K5jk2Z3GfrWQA-gdFGU-H5TrNMs9yPwObL7SjISOtR-o6zfIZePteAggmnUGU80J-IOVqsrQvaIViyWBXNkpflZUylFmwZUWDsuKiuvoWw7jlZhmsvGVewo6uZEYahii3AqPYncz7oJzIpkBUSlltVzr429bl1YuLahxfVo44cgb07AvvWVccK9GFeLfWPyxvfXNmDE4OTgPz3RZdCi_64SuZOXWNWbH6e4HI2fJWDtISpIAOGpP8wZQCSbhFT7IFvAgLN0LDVDJxOEI8Dg-vjQL9uZxwLiecywnncsK5nHAuJ5zLCedywkdKVGy40jZzQbCl0WQ54UHX00RlIcCKOLLD1Bvkp-E6Nf1ZJ3pCNXhIAC0WJVwPnfxpNFByPDovhR-iAOiXohcMiLKBM4KxCKyV8Hh2n5Viye7wQAHc7dlbCzLVlnDdwOC8ptAbXf21VoH9HVhQtGkP4S5kRidZMQOY_bouB0CLwZ-V9cZYn6Q1wsWlWd4mA5UAgmTCJwmgUUWPQlN9ocZAQALppF9E1SkadpTbBki-t7FfK7CsjpnGNFpCqXKARS-Ylq0YgDnstDeJlvoM1Vcy3RMuCpiN0rTEgV4gjKgp6NpPWSCy5XCmu2E0K1dp-dLYXRCREPAhUpZljQu6RYACO8pzlYaokeJ6AffjnRiqUkc1BPs3QwRRGEaRLdhQQ2C42EccfJrHPJOnLvna9UFjY1K69SsimKyekq8se55ZEMBATAEERMF5S7YrikjB13dNXV0vARdu8Rw0LdagW7Aaaw2kBEkluBwarA0U5P0fhZZEEVuA1mjbrvmOKnM74HFg-j3r_tco4HL2TujU1rX0q8jywEGZYbFSvz7Qd_ALOuwXppGGTCDzkmVJhT61dpdiEYQ28tWpqQIAFDmtVG9gXH0tA6hG5Qgy7beiqfu5VTHdYqjCGJwiqkRgZ2asb3adKuFQx6FtEZm_Kq8RLn2AyxPMxFjgpAkIv8DLB0ujj4qMmOm0IMd-Fi8Y1BJmL5smJ338K1I4CmcDvwKQua5qZFU4zXEygUWFxCpT1iIPW1dvl65toQ59oXO2uVj2XKJL3NbK3NhShjSAfinHUM7CkjA74X9Z_-8_nfWvQvs3COR_fTVyKVhdIZYpwAyq-UNTIMczNWwS3CWdLxwYwmNEFwiqCF6-sNJdAdt0JIIeUgDo49Zy1x6xBrl5ZI4xltuAPdk098ttgawik_i3IymIw6HIOijz_iGYOPkw4C4Pcjuw_d48NqJOo5M_LYik1R5pOnn0jmtJx9-y7e5LoqFYotCx8Blyo_YqlxRb74NcgAoGBQzADm4UkIXDVQU1afyOWpM8h0vkUHkp-4-wjmc5XAjrt-RixMrKjtoJXlTol8MikbZVFfmWCtJoBChtegNfakEqgIU37L0y96XUuADQdNuXnbdrqZlcf2Hb9nBYegYp_X-t_TYVuYGkhSjzR8ZCTutkLGKn7UmxQpgNOYd82Hw5wLM1JVtJGdKRT2hKv4RxErAw9_y8R0hG0O9T9F5QVQNIJtNd9KArg3VKU4a5d8TcO2LuHTH3jph7R8y9I-beEXPviL-13hF5IlIRe4EbuckP0TsCzYX9_hEXVV1Zz-4fMbIAJ7zftpM7aZYEwg2Syd4RStWsdTvxQW3B6Tm2_UvZNGLCACL_R4dGNgUqK1QAGRIHszewwry1bgBWACmksUeNH9AzBoRKgl9an79S3SsoE2FoZkE1rWjHD70nDoAAFbffSGaGN8goeLgELCe_I1N3QQu4Y81mSe5YUpxyDxvUX06gvFLqBjHlpTPeID03vEID_sJe2e7cl2LuSzH3pZj7Usx9KX7avhQ5d2PhiMTJXPbj96WYSC7S7SlGGVcSkY3zri6qIfFq7k4x7k7Ru7U_tkPFigJ0fTaX4nGK32A8cZmzTYGDmLlfSklMtKgQDyvP1PbmdhWn_g2ln3G7CiPBbZjsQNrc06sgjLyz00YcHCd6SCNf6RMt8qOLn8wCZola4cz-fOYg4RwX-PXPZxGijzA4--ab4_N6WRALEY1Lm_5RJS0P1xvv2yMVb0dfmipAtFlgp174zNlR0zjuknDobTyOzKOJrG-64avr0ebEmUS-F6fOXqHQaat7evWyBGrawzfF1jF3feE4n2B1EtJT5oCc_oZxsjVl4IsEMQVK0S1EsV-ZKjFZMifiLLSTT7A6VUeAGkHH7BTekiatDBbpTH1AWjI1K5sqAYu57-Thc_nujUAsBq_oFO4e9glKRitajL6SqJXKHhaPijG3fuFMrM6I9QyrG9ah3J4_WEHa6e0aPpfKQ_piddiGYBwqwqWKuwMKwPRRyqeCj3WQOj1I_tUx5XB0EV9jkkarsscBrSyVwWl4ztotWH65ssoJmlPLh_5PoB1WHse3LRlUzpntaQEcv09qMpOZxnF38xsqsxkJjKEDweqYHjq-upKhy1WogI1OU1DZzOiyHNIVZKLKkHerECAgOUSyMvX2AJEeNnF4hEjKhwBA4ZoqRQzWRHo57hByt8JxbplydcraA4EpOY0sWOn9plIP9Ay-Ona3HlynvunIhv5EErP6FAxtfsFMSzNhCy8Mxa9Xx5TqRG8O1md57__lpakrYKjM6T89KAs8TLOOCjuW1zIcN9KRAwjPSsEauBUUxWl707HPWDOTW1bHtOXjCxsiWE_XjEYvB6O7xGGN-PgKSI31DDhcRpMVKasPC8lMS4te_OuOUdKIosvqmO6bXseg2TC9QWy2MGKv45Tob3WqsTKlR1Jcl8mMzlkntPQ1XMdU3-NEkqpr8B9oFbbovXCD-ar7uyyG5jhmvoZFyXOP_31JJRr0FZB4ZOzPMP9oJogm4CWM1tDqxos4gBx6L7uq-8W_iFbSZe7bBj29D0gYpxljYeKFKYhMl2eRHaduerQPSF-X-zPrAzLbXLPNNdtcs80121w_oc319B5T-60iQrNVRLDoF3vufH-4K8SP0xMjSx0nzJjDw1R4UWInIvWTNExDkQUulrbGCc-jIBOZx4HyIhRRlnmxl8BMGf_oje73x3CSc9c-dw71xwjSkPPcS35m_TFy5kRIFS9PnE_aHwOtbErVVrdtSk3MTTLmJhlzk4y5ScbcJGNukvG30CQj5FEYOJw5WeRNN8kYoPbPo0dGLPLY8UUqnMj9iXtkjPIeH_SFeFigqxtkYBawNPFU8Tv1qtClu09tWvFTtsrokx10uwza36hXBhUYFJiZBeCAOmTkUjkf6EPb19h9-r4Zkc1EEESM-x47uW-G2S8D7wRWtzfWKElEJ-jhLTciAxi8meqxYT3eYgM0tJFM8mifDetYm42Lau6zMffZmPtszH02fsg-GxkoZjfOvNxm9k_VZ2Nl_bESZmxTHt4da6UziQ-lJioQusBKgVvqeeS4Q3xrFE5V4nXu2DF37Jg7dswdO-aOHXPHjrljx9yxY-7YcXLHjrkVxtwKY26FMbfCmFthzK0w5lYYcyuMuRXG3ApjboUxt8KYW2HMrTDmVhhzK4y5FcbcCuNHbYVhWLaeZ6ciC1hi9z5XowBlkMAfU0uix04SDyS5nzhxj_2M8hKD-U-tFJGJkZLCUtTIk4CnwXhudzkYUAXmzRPqv5QRxvZK5_2Ocvdkyt41xevbWtlzoxI15Uwg08YoA4TTsNcOYNMvhnQYLUh0_WmO1LuoEMcOfi_tzDLSxyzSz3QjkmAVhb_ExISm1lJ1P34ofZPSxTGGxe1OOo7xOjiwPMcsHNE-ORkfXVl_AESPwgUmVyXZiFuMUDWZUvQKxpZ7FwcRCoiKbjrleETq7-X_TXCfJ7idp5ljh37PIUaJj8Ehp1brcMv1164vMc05CCByuvXpcAt0BWF6A0aj0bbAedQ3RlptdVtnQyIJcpkZgOtjsXfoYnBW9ounhdKOhNG0y5lCaQro74UA5Uxok5BWRdf8HZzh6M-ZkwElPaDjv4CJVumUzrID143SMPNzu0_ENCqbjEM5tUhp8OAAsxQYvCbPilQBf9dabrx8_cVXWm2QvBbdUM6KjvANeS8Hsqig1R1lKI24zxoXLD2sk8ULTIsjVjKjlHBCUtAfRAJ9JG2_3FeGzQ4VBmP8tQ_5a8N82_sL8GHtxqKLZD3xHiVh5vlOZLthkA8B-L7ca5zoc1LlliGV-z-XRc4s7VDGd3cYDBmVK8skfl2rTByhog8y8KTSDICrt6aPTHKTOiq4v7aVCWD7F5YPB0EXCwhqSCwpqiiOjxMtrGhQrvLCIDygfdV9MlUw6BFi3Fz01j7FzS6UsZSWGAyg9OlWLRJgjV4dLUzeR619ZScLWehBxq0MJ-LylKhWXgeV3A9CdC-EiWGyj2YCn4NVCxeVs6i_t0ZVXR8lO71AzlklkeM5UWjrEIu8ub8AvSaP8CsiM0hVjLigXUDwjWJmzY6urDwOPMVBc2Xku-jxnda_ivdSLBXpBu_CAaJYZgnQQtXvaHA3OBmGHaoiCiOLWPlWMfGw7MyalItK-h4O9RP75vv_D1JUd1k)
