[//]: # (ob:168bc323)
# Governed Workflow v10: Private Legal Evaluation Decision

[//]: # (ob:a46dfb2b)
## Decision boundary

[//]: # (ob:a0c8368a)
This memo records a private, staged, model-adjudicated evaluation. The evaluated graphs are non-authoritative fixtures. Candidate claims, critic verdicts, silver locators, executor outputs, and evaluation scores are not lawyer admissions or matter authority. Licensed corpus content, quotations, prompts, trees, credentials, and private paths are excluded from this artifact.

[//]: # (ob:cfb573f0)
## Product decisions

[//]: # (ob:bb53029e)
| Product question | Decision | Evidence-bound reason |
| --- | --- | --- |
| Replace PR36 v7 claim construction with v10.1 | Do not promote | v10.1 materially reduced unsupported factual claims and improved honest gaps, but supported factual claim coverage fell materially. The preregistered construction gate stopped the full 12-task Legal E2E panel. |
| Replace PR36 v7 claim construction with the v11 v7-preservation compiler | Promote for the staged workflow | The formal 12-task majority adjudication retained v7's requirement coverage while improving supported factual coverage, unsupported factual rate, and honest-gap recall. The compiler may preserve, source-bound repair, or reject a v7 candidate, but may not add claims and has no admission authority. |
| Make progressive disclosure the default agent-facing matter-context API | Promote with executor qualification caveat | The 24-case deterministic safety panel passed all cases with zero blocked leakage, automatic admission, or unauthorized mutation. In the v11 fidelity rerun, DeepSeek and GLM completed all ten two-task context cells, while Qwen remained route-inconclusive; the result therefore supports bounded disclosure mechanics but not a complete three-executor panel average. |
| Let the executor choose graph traversal and gap retrieval through bounded tools | Implemented; formal promotion withheld | DeepSeek and GLM passed route and workflow qualification, but the 72-cell formal attempt failed its preregistered gate when one DeepSeek ask exhausted the three-call tool budget. All formal-attempt aggregates remain diagnostics, not a promoted panel score. |
| Ship the post-disclosure assimilation gate | Promote | Recommendation accuracy, dry-run immutability, valid submit state, stale-head rejection, duplicate rejection, and idempotency all passed the deterministic panel. Submission still creates only imported evidence or unresolved candidates and never admission. |
| Make PageIndex the default gap retriever | Do not promote | PageIndex and the hierarchical prior added no coverage at five over global BM25, recovered no global-BM25 misses, had no unique correct evidence at five, exceeded the latency threshold, and had incomplete cost telemetry. |
| Default gap retriever | Global BM25 | It matched or exceeded the hierarchical candidates in the frozen component panel and avoided PageIndex latency and telemetry failures. |

[//]: # (ob:c9c38e76)
## Claim-construction result

[//]: # (ob:0877724b)
The paired 12-task majority adjudication produced the following post-output metrics:

[//]: # (ob:69377aad)
| Metric | PR36 v7 | v10.1 |
| --- | ---: | ---: |
| Requirement recall | 100.00% | 100.00% |
| Unsupported factual claim rate | 29.94% | 13.15% |
| Honest-gap recall | 70.70% | 82.89% |
| Supported factual claim coverage | 82.18% | 43.44% |

[//]: # (ob:a4b0fec1)
The unsupported-rate and honest-gap improvements are meaningful, but they do not compensate for the supported-coverage loss. Development ablations did not identify a promotable repair:

[//]: # (ob:cd607272)
- multi-query RRF with a larger section set increased noise and reduced blinded supported coverage;
- a task-wide BM25 safety lane did not recover coverage;
- frozen v7 decomposition plus type-only normalization and the evidence-first pipeline still lost requirement and supported coverage;
- the loss is concentrated before or at claimability, not primarily in the layered critic.

[//]: # (ob:3ce974eb)
The full PR36-style 12-task Legal E2E panel was therefore not run. This is a preregistered safety stop, not missing data represented as a score.

[//]: # (ob:3cbcd334)
## v11 claim-preservation repair

[//]: # (ob:9f216f28)
The next qualification preserved the frozen PR36 v7 decomposition, retrieval, and candidate set, then applied a source-bound compiler that could keep a claim, remove unsupported clauses, or reject it. The compiler could not introduce a new claim, requirement, evidence ID, rubric atom, gold answer, or silver locator. Its outputs remained unresolved, non-authoritative candidates.

[//]: # (ob:5ea618db)
The four-task development gate passed before formal expansion. The formal run then completed all 12 paired tasks, preserving 266 of 277 input candidates with 41 of 41 terminal compiler receipts. Three new blinded semantic adjudications produced the following majority metrics:

[//]: # (ob:e2a2fbbc)
| Metric | PR36 v7 | v11 v7-preservation |
| --- | ---: | ---: |
| Requirement recall | 100.00% | 100.00% |
| Unsupported factual claim rate | 37.03% | 8.28% |
| Honest-gap recall | 54.85% | 63.39% |
| Supported factual claim coverage | 77.89% | 82.87% |

[//]: # (ob:a2d7d34b)
The mean paired supported-coverage delta was `+4.98pp`; its 95% bootstrap interval was `[0, +12.15pp]`. This passed the preregistered construction gate and unlocked the formal Legal E2E panel. These are post-output model-adjudicated development measurements, not human gold or lawyer admission.

[//]: # (ob:edc06532)
## Progressive-disclosure workflow result

[//]: # (ob:508131fc)
The frozen panel contained 12 lawyer-style asks across graph-covered, relation-dependent, partial-gap, and novel categories. It ran four conditions with two executors, producing 16 of 16 scored cells and zero inconclusives. Every model call had a terminal receipt. Total model cost was `$1.9346`; the diagnostic PageIndex call cost `$0.0022`.

[//]: # (ob:b42b3adc)
| Context condition | DeepSeek rubric | Ling rubric | Context upper bound |
| --- | ---: | ---: | ---: |
| PR36 v7 prefetched context | 24.60% | 23.81% | 20,255 tokens |
| Claim graph only | 29.37% | 25.66% | 18,063 tokens |
| Graph plus global BM25 | 25.13% | 15.87% | 23,998 tokens |
| Graph plus hierarchical hybrid | 24.60% | 15.87% | 23,976 tokens |

[//]: # (ob:25411a7d)
Graph-only context produced zero unsupported-claim, citation, and authority errors for both executors. Adding retrieval increased context and did not improve rubric performance. This panel supports progressive disclosure as the agent-facing API, but it does not support unconditional retrieval for every free-form ask: covered questions should remain graph-only, and retrieval should remain gap-triggered.

[//]: # (ob:bcaa3ae0)
### v11 disclosure-fidelity rerun

[//]: # (ob:f9748db7)
This is a panel of 12 follow-up lawyer asks over two APEX tasks, not 12 independent APEX tasks. It used the formal v11 preserved graph, five context conditions, high reasoning for DeepSeek V4 Flash, Qwen 3.8 27B, and GLM 5.3 Flash, and three blind grades per completed artifact. DeepSeek and GLM each completed 10 of 10 cells. Qwen completed 5 of 10 cells on the initial run and 7 of 10 on a bounded artifact-preserving resume; three Qwen cells remained executor-inconclusive. The three-executor panel is therefore incomplete and has no overall panel score.

[//]: # (ob:b09ac6da)
| Executor | v7 prefetch | v11 graph-only | global BM25 | hierarchical hybrid | full-graph control |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash, high | 12.96% | 29.36% | 18.52% | 25.66% | 20.37% |
| GLM 5.3 Flash, high | 20.37% | 29.36% | 24.60% | 34.39% | 33.33% |
| Qwen 3.8 27B, high | incomplete | incomplete | incomplete | incomplete | 0.00% on 2/2 completed cells |

[//]: # (ob:0cdfac80)
Across the six asks with mapped claim atoms, full-graph supported factual coverage was 66.67%. Graph-only, global-BM25, and hierarchical packets each disclosed 58.33%, an 8.33-point loss; full-graph control preserved 66.67%. Retrieval did not restore the missing mapped claim because retrieval adds segregated evidence rather than selecting an omitted governed claim. Full-graph control did not consistently beat progressive graph-only at the executor rubric: DeepSeek favored graph-only, while GLM favored hierarchical and full graph. This two-task result is diagnostic and does not establish a universal best executor or context.

[//]: # (ob:ecf4167f)
### v12 agentic-disclosure attempt

[//]: # (ob:7c4b0604)
The executor now receives a small initial governed disclosure and may autonomously call two bounded, read-only tools: admitted-graph traversal and global-BM25 gap search. Traversal is restricted to already disclosed seed claims. Gap-search results remain explicitly `not_governed` candidate evidence and cannot enter the admitted graph. The host permits at most three tool calls with at most five results per call; only qualification fixtures force representative tool use, while the formal attempt leaves every tool decision to the executor.

[//]: # (ob:e15137ef)
The frozen executor matrix was DeepSeek V4 Flash, GLM 5.3 Flash, Ling 3.0 Flash Fin, and Muse Spark 1.2, each on an exact provider route with fallback forbidden. Qwen was excluded because its prior long-context route was unstable. Serial route canaries passed 4 of 4 calls for DeepSeek, GLM, and Ling. Muse produced 4 of 4 HTTP inconclusives without complete terminal telemetry and was excluded without a capability judgment. Workflow qualification then passed all 12 of 12 cells for DeepSeek and GLM. Ling scored 12 of 12 cells but failed the separate workflow gate because two asks exhausted the bounded tool loop without answering; it was also excluded without converting the failure into a model-quality score.

[//]: # (ob:45999d63)
The resulting formal attempt contained 12 lawyer asks, three context conditions, and the two qualified executors: 72 of 72 artifacts were graded, with 153 of 153 model calls carrying terminal receipts and zero transport inconclusives. The panel nevertheless failed its preregistered formal gate: on `novel-3`, DeepSeek used three gap searches and then requested a fourth gap-search call, so the host stopped it at `tool_budget_exhausted`. DeepSeek was executor-ready on 11 of 12 agentic asks; GLM was ready on 12 of 12. Because every formal cell was required to be executor-ready, there is no promotable v12 panel score.

[//]: # (ob:39c133ab)
Exploratory failed-run diagnostics suggest that agentic disclosure reduced context and unsupported claims relative to full-graph control, but they do not establish a performance promotion. Agentic context averaged 9,794 tokens for DeepSeek and 11,201 for GLM, versus 20,455 tokens for full graph. The paired rubric deltas versus full graph were `+6.30pp` for DeepSeek and `+7.85pp` for GLM; both bootstrap intervals crossed zero. Unsupported-claim deltas were `-0.75` and `-1.86` claims per ask, respectively. These aggregates describe the failed attempt only and must not be reported as a successful formal score.

[//]: # (ob:10827ee7)
## Historical JSON-only 12-task rehearsal after the v11 gate

[//]: # (ob:3c3528a4)
The gate-passing v11 construction previously ran across all 12 legal task prompts under two contexts using a uniform structured JSON answer schema. All 72 cells scored and all 288 model calls had terminal receipts. However, this runner did not create or edit native artifacts for `make_new_doc` and `edit_existing_doc`; these numbers are a JSON-only workflow rehearsal, not a complete native APEX Legal E2E score.

[//]: # (ob:ddfd7148)
| Executor | PR36 v7 context | v11 graph-only | Paired delta | 95% bootstrap interval |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash, high reasoning | 13.34% | 11.30% | -2.04pp | [-9.37pp, +4.90pp] |
| GLM 5.3 Flash, high reasoning | 12.85% | 11.16% | -1.69pp | [-7.24pp, +3.11pp] |
| Qwen 3.8 27B, high reasoning | 3.17% | 12.76% | +9.59pp | [+2.31pp, +18.45pp] |

[//]: # (ob:08e2584d)
Qwen was the only executor with a clearly positive paired context signal in that JSON-only rehearsal. DeepSeek and GLM confidence intervals crossed zero. These values cannot establish native document completion or compare console, new-document, and edit-document task types.

[//]: # (ob:26c2586c)
### Native typed E2E qualification

[//]: # (ob:59805781)
The corrected runner grouped the frozen tasks as six `message_in_console`, five `make_new_doc`, and one `edit_existing_doc`. Qualification selected one task of each type for each of the three executors under v11 graph-only, materialized DOCX output for document tasks, copied the protected SPA before edits, performed deterministic format/digest/change checks, and required three blind grades plus complete terminal telemetry. Only 2 of 9 qualification cells scored; seven were inconclusive, and only 22 of 25 calls had terminal receipts. The formal 12-task native panel was therefore not run. This is a construction gate stop, not an unreported score.

[//]: # (ob:0b80db42)
Muse Spark 1.2 was present in the live Gateway model catalog but its fixed `meta` provider route failed every structured-output canary under none, medium, and high reasoning. It therefore remained inconclusive and was not represented as a scored executor. Gemini 3.1 Pro passed the fixed `google` provider canary used for grading.

[//]: # (ob:f8934a39)
## PageIndex result

[//]: # (ob:475d6c05)
On nine tasks with frozen gaps, evidence-set coverage at five was 80.56% for global BM25, 68.52% for PageIndex tree retrieval, and 80.56% for the PageIndex-prior BM25 candidate. The prior-minus-BM25 paired mean was zero with a `[0, 0]` bootstrap interval. PageIndex contributed zero unique correct evidence at five and recovered zero of thirteen global-BM25 misses. Warm-query p95 was 82.16 seconds, and seven calls lacked cost telemetry.

[//]: # (ob:f10cdad5)
PageIndex remains a diagnostic adapter. Its top-down document/section routing is architecturally distinct from bottom-up BM25 span search, but this panel did not demonstrate incremental product value.

[//]: # (ob:dcf77705)
## Default model roles

[//]: # (ob:64858abf)
The frozen, qualified development route remains:

[//]: # (ob:d9eeebd3)
| Workflow role | Route | Boundary |
| --- | --- | --- |
| Requirement decomposition | Qwen 3.8 27B, high reasoning | Candidate requirements only; no rubric, gold, or silver input |
| Evidence-atom extraction | DeepSeek V4 Flash, batch size four | Exact source-bound atoms only |
| Evidence-to-claim proposal | DeepSeek V4 Flash | Unresolved candidates only |
| Layered evidence critic | GPT-5.6 Sol | Verdict reference, not admission authority |
| Primary workflow executor | DeepSeek V4 Flash | Cross-model primary |
| Sensitivity executor | Ling 3.0 Flash Fin, high reasoning | Sensitivity result only |
| Native artifact grader | Gemini 3.1 Pro | Blind post-output grader |

[//]: # (ob:a4058ae4)
All model calls use fixed providers through the Proofpress development AI Gateway with fallback forbidden. Missing terminal model, provider, fallback, usage, or cost telemetry remains inconclusive.

[//]: # (ob:d4006a73)
## Preserved architecture

[//]: # (ob:a721d6d1)
The product architecture remains domain-neutral at its core:

[//]: # (ob:d9def285)
```text
source corpus
→ evidence substrate
→ requirements
→ evidence atoms
→ deterministic claimability
→ unresolved candidate claims
→ evaluate / policy judge / authorized human review
→ admitted claim graph
→ claim-bounded progressive disclosure
→ gap-triggered retrieval
→ executor synthesis
→ explicit post-disclosure assimilation
```

[//]: # (ob:baa3e879)
The Legal profile supplies lifecycle categories, legal claim taxonomy, conflict/version rules, and lawyer admission policy. Retrieval receipts and valid evidence atoms never grant authority. `disclose` remains read-only; `assimilate --submit` remains explicit, authorized, stale-head protected, idempotent, and unable to admit a claim.

[//]: # (ob:6b806606)
## Result provenance

[//]: # (ob:0f0187ce)
The machine-readable decision report binds the frozen construction-majority, supported-coverage, hierarchical-retrieval, disclosure-conformance, and lawyer-workflow reports by SHA-256 digest. This Markdown memo contains only sanitized aggregates and product decisions; private raw artifacts remain in the authorized evaluation workspace and are not embedded in the portable capsule.

[//]: # (ob:fdff801c)
## Next construction experiment

[//]: # (ob:0fece524)
Future construction work should target evidence sufficiency and claimability coverage while retaining the v10 safety gains. It should not relax the human-admission boundary, remove honest gaps, or use PageIndex in primary claim construction. Any new route must qualify on a frozen development split before another formal or E2E panel is started.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZhZDMzM2RlNDQzZjM5MGM5MjBhNzNkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjBjNThlMTI0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9lMDQ4MDc1MTY0OGNiMTM4NGNlZjRkY2IiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY3MjYzNmJlZWNhMTNjMzE1ZWU3Y2ExNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfel240aS7qvgVE-fuXNMsrAv8i_vXXPttsfl6Z5z2j5SAkhIcJEABwClUrv89z7AfcT7JDcickGCBCmWJC89nf5Rlkggl8jI2OPTTy9YN9QVK4bLunxx8WK7vYxZGQRBycMwqILMLTLfZUlQhi8WL_K2vL8s62veD_Bsf8P8KL5I_arwPRb5ZeblReXBf2lSxUlWJDEP_KKIXb9kXp67nMe5W8UlC_3YTWBoFrhJAuOWdV-0t7y7f3HxE_4yXA7sGmZYswGnWsAPOV_DB3_hXV3VLF9zp-O3dV-3jXMDz7fdvZPfO990bVttO9738M6WFW_YNcdNTT7u2h85bHfX4YA3w7DtL16-vK6Hm12-KtrNy-KGN5u6uR5Yc50G7svJ2x3_710NP1_uet5dFm3T8wZoMXQ7_vPixQ1nSES3iFLu-Ugx_OSS39JDQFx-yd0wdZPIi8O0yL0gDQtehWWR48rabsCtXa7rhsPK1YmsL-PEj4M457xgXlAEXsR5Aj_GYjtydZcF2_a7NWzYx3UWbVf2Ly7-9tMLOf1PL-CU267Hn8TXvLzMgeR_e7Fr3jTtXfPiB9iD4gc84GFX1rx_ybb87RIW1AxLfsvWL7_4-i-fffvnzz69_OvX3_7vz7_8-q-Xf_Hcy08_--TV61df_3m1KV8s3out2DB0db4b4DQvc9bXPc7N19Ul64HKA6fxdsNN2-Ha39QNDtnf9wPfwDcN2-Ahqz0s4NUeGePFRbNbr2FHxQ2cJBe0yNdt8Qae9uI0LwI_gMfhEAf-Fvf7BfJgw0vnr233plq3d86t514AV9W3wIjOl_yarZ3Pbhm8JBfBypJWt0Vu5HfwyR-cc0dZ7xju2PmUF8TIMMxwv8WtINMAA774eTEumIVxWeV-PlmwetXJ211TMrg_p1b2B2fu-VNzukUaxCl7_JzfweV0NnzTOpIhHeZsBSEWTg-XnJcLZ9OWfL1k5Y_AbQV8UzrIZbtxbVvWscnCiiqPkqByJwuDy1_uisEp5QL7B4gx9_wJYuR5FLh-xh8_5zs95X_vQKwhDd-NR_IOeKIueVPwJVEWKMZ6_Pz75p2zXI6LIxkxJUdWBClP4snSPlmzerNECQXCqaDZQErs1sMDZDn13gnyuGmSJH6YP30N391wZ8tAyJaO5y8H1r9xNuzHtquHe0czCQ61JWrCYwO8UbVruGoneCbOgiRhrHz6At85X3EQWAUc2TffBrFzm8BPcMdXnjqspUP_Xuj_4cffCtVx6iBZCPqRF97zEHHX9LstKhVeLjsUPQy46qZtgPeW12zr1Bug4C3fgFyHe9lxuKiswXM9cfFKUNx-4j99gUtnA0_US7gKoLu__fZz5w5UMIiHNeuueef0XIzU88GpmwIvA5x009Y9d8YFrkH3TxYYFDxLQv5MbFiBAqEzXvbDPdgcih-lDPc_A0Zt-Nq5Yz0yYcerFsjYtCcoyMvCjaPA3xcj16jC61u-RFto3fY7GOhOKZCzLu7Zg5y4xZGbeoFXFc-8OqJl1_6dN5JgODirG7ricOJ397yTJAbyAjMWXdv3znXHtjcnaJmHfh6w8rlX-875RIyGyyxrLaj59jXnb5xul4vL_yVQb_xNvHPqdvtR6HksKZ95uV8glZZts7535LCjZPw779qJHCjwKiycoh5Ihp4gbpVmQciCbLpa0NivmpK_PZMlDx8_wXxhEpVx4UaPnvHrxgH5xZ2BmIjkieQ6EHf9AswKqWBRqJDDAYM7bHCq-vYUJTy3KFn5-HWZz26A7dEKKmt23bRgBRSg1Nh24N3KeQVyeGi3yxLsWKdsix2I5hPrKosKdO4evT7lFYPlCKPK6do17x80CufeOHFO4LpEKcurp8w7SoQFWENsDV4dsGsJrsq63aJGgiF2A1cEuzhFhoxznpfBU5bzbjTW8Vm4zt_S9O-cj6WVu6fa1b-k2E-rdBeIxcOnrO4j0ELi0YKt170Dview7FsgGCpw4OkO1Q8Q7PqGbKHRDXbKU4QLXTcGH2xPHnHwuW5hbNYVN_UAanhHRstp1XPkpVPOReJ7ZVx6T5ydrEVpVpvv6KtWtvj_ZcN3QwdKG257DdcMnBF-mqlKXvlp9MTVXV1d4bvfN3276wqO0253_ffN__s__1dLI6ff5WCYgIEmPpchBjLLxCfjOgvggqkKZCzgaZI9AxWFUQO0rOo1Lmq7XYPz78DV5MV9AR-hb3YNdjgHUbqmh0mbnJKcZVWlrjdV0H-WmnU0xvjbLe9q3PADfPbAq6fcE9gEj_zwWVby-Y44bPImKmynv2l3a_BH0IQdzAOuqrqo4ed7Z59aPyxUfOYF6CP0BC_R2BVBD_pGRVD4ZVZkSemGLC9SXmR55idpGfgxXqGmHWhMGUJyZAjJKW548Wbb1rQhmJFmwriI-g3DIj9g7GldF_fGCGY8yhiEIl2PDFX1bTVcVnAyvNt2tYyI9bl3kTCeh1WWl16eFF6ae2lWpmFeVG7uxamf5WGa-ayIeFn6bhZkVeCGaRrDO0kShDEa-z3YMxTZEqd14ac_A6ExkOS7frx006WffeeFF653EYYfuO6Fi8EDSXE8ZD_Kmc8TYJrx059-i2AYcawIVt2w_kY4XWFauF5YkTyiMYz4lWTm5w48yckp7MS8ysvJLaXJjViUmvzs2JIc1nXhbPM04bB3PewYbpLDPiV8RHtcOSjZ5O_wDXkUwtlt2mYpgopkC9-SSsV73a-cT8BTrkskGkk4kHcFPAWmGhAYJhngg75ewy8OHBbDoCoYl295sYMfHTActjt8BN3tcSlOjzpHzT1IrweMv01N4cregXc3bBjwQ7mu-xU4GQVv0PUVqkOY-M2AVlMrbHiYCYT2ZotTDh3ntFoOkmeo2VouQxINvK9Bbp-_LdY7uCpohW3AaqjxY8GlqxmJrlix4kHu8STixHp0bEYwbuSGM4NrcljG3DTyotjzglINa8Tb5LBPip_N2W18u2YgnlUQh856T6qjDyFDO86nLR0cErsl21B8AWcGOgMMs3uYUrhdhsflIEV3Slf2dBoy8KKCMdI7yXeDc-S10VmpONqCekbB36CZOn5d9_ApMYqxgWs89R6ciq2Kk2FI40gcYyXo8hV7QzaV8ksdwy_FIUppvQohCAtFP1hw7lJ5oB9988qh85KkwmX64bJgPb4PT27qpibvp2cVH-5lXGCLEX8wW9Zo6vZcOnHkxZJchO_WnGFaZ4GXBEw74UDJO7TAO7Rr5PX5Ozy92Q2GIIB947a1c62CEZvtmgvBgcGoAmmM53R96FnLSA-QtGsxqTA4mKFSkgXvHxvQfJCkfH1Tb-n5Lbh6pn8P-6w39ZqNh2RS61uQdhsYphTfs6LYday4Xzhld7_sdg1wEG4sr9cgIxYOyJi6RDNyUw8oFqV0XPMl3jXgyh9FMA3e34FRh0LS_JBYsuSbLUyOJgpSXx6EOG7zuCSjvMbJiOYwU43HRUYLCDGkFjC44GJtAtG5AD-1a-T7QslXcR8apPt4iiYbjq6zyXkYvewwBksvztzM8TUcH1-9qeECoTVckJFbtzhhSSHF_VAArBaHvV63OTz78Vd-tCD9c0vXC54X3yzxGwfXjCL3htFXu6YG4YTCGt4wTEA5MqqJgvNSkhbzm0hxcN442I7rUhwGjlU3ii1hMGKzNbgEQ3cvqfPpEVJ8Ma4afns14MUE-63EE5jMPSGIcSB1I-SECJzgIkBIgT8u7gouj922NY4yElntg4itFgoirF4LffpuzkPWKiUNSx6ECfjJWqWMCY1RpbxnYkIOn4ZuHnKXZVGUqOGNXIU2NB6fc0DpR9dbKH5nQ8mB2ZCFtqmyMHKLMI5SbfwY6Qmt7p6SZhAxFI4BA_jac92V6_7R_Amf_c9jesrphEjys1UW0mvByovkW38aUwh6gsRdJTR-6q_STD74-iFtRo97Kb4XBqsQZzrBKcAkZQgeRZaSjShNUZ0xMY7ysZkPUI5CD8Pp3julkCp4BcAEw2EquEQk_cd4qtoKyHVg9E-NABYsX9hnoD9LGqkmo6y6JysWRZUsZEDOO8UuWR7xvMpz8H_0DRkTMXLfT0moMDKXBGPn4NLh7R45Q-3xw--bJYyHt2N5B3sRQkbq7zWIB71RKS2nb0qJAmxcchIrvQitb9dg1uLWhaZt2m4D-uzvUvVJ8a1Dt1XdgTTc1luOrqdUPmuUkEbchF47sgGSu5hdqMmYBuuaYi-wcZG9QcUwCEbVClYoF_igq1G7NVJ43wt7i1yD1UxSSp5fUIWR52deWhSFOj8jT2Xw7WPzTbD5HZk4NW2L7VmE8ojQDBR7IUULYgskPkP-w3hRgzRg-DI5KiecgJQFZVQFVeWXWqQaaa2JE_DojJTyDNKCR0FZ8DQN1VxGksqk3SPzS0up2FHHiwu7LDlc-JK8rC06RaDrQWoI3dzA02sjFIZRe5CWDciGXTcmjKTlOty12jEUfhpcMqS8Fztthf8SsUuyOYUxRMYuav8GHDQkHUzxGdmlYwiYLAS4iWSXAWfAfeP1FozO70Cm6FgxXgrklKt_8VZZEMZXHwojasw8jBqcRqU3rv4FFYTvX53ggKBM0qpyszzJdVDASMZpBfb4PNrgwO0FCSJcuWP6zlB7SkUCLwOzk8WjbHZQY-EqJu3kB6vUox_chR9FztC-AdEuRiD7QtrxJIlI_QUJPR6t4pj0YLpw42DyHuXfhBS7nhhf8JIX0EvRKhXDBIssS4-9PbHIbu6BHqW59skoSaxHOaExvcSviswtg8LT7rqRhVRlT09IIIpLoeMVDu864HRSlHkLF0Az_8r5qCzpoIWxClsctZCaFsfSylLoaMUYwAwVagYQ2FLQiZsuV9Yfc1ilvzbxVcE5FWoe3KWyBZsX55MDwWY1t9LNUqvFLQn_sOo46CFYDAqTC0c5Bioo0aswsMhAGF7kQipaNeTec2y7hG-ur3G0E5cv9PLc4y4Ho0CbA0ay1hC_Z2Vf5ailm5YlmMmMkxCnUY2ErBz1KRlWTsIodVcR3CSk5sTBitNV5IvPDZ8PKD3SS5DPGIByXerhpXDq6O5pd0bFR-CbJYjKXS-cNmnqo9VHiyIul-bS1d_cheP-cAX82w6YlwFzEbizgwWsTIEJLEtFi-MlOen5yaNXzEKvgAYYbmq4Vki_A59y5fyVdRtpz22zSJAP7OUYbTngURnb6zFLIDODa0Yxkj2P8Tgv-ZHre36Ru3mqBYSR7p7Jdb9v_np4qQxPTOji7aNIo05LUdwMS35BGgwiGAmCY2g3y91WGphw0WGT-I4yzvXtV8Ki5BvyC9FIJ7GCM4tsFgUMMQp70qTJPebmScD9PFd0MNLrZpT7zGS5uqw-6Eg_88Mq0tfKyJ8f2C-PzobrAy3C0s_LgLNYb2RMkGvN_JR0t2FnTy35d85_3AErgo51_OTjBSi06xsZhsWDf2fE1c0kJ2nbDzF6ImT9wrmmUAjcZhllrxt0rGl2HeRlwCOgXuDMi33L4i-h8_ka6AHsgsEPGOXvXNhn8P5beN4R6VgZKMaRZOBqOsXQCnWHbASbZOu5SRx0o-ciW-OAX0pPQcsEmU0A7f_Nd0swLZzXLY79F5FdcNCE6fBBYa3rwJihZ4XNQy7J_WhQ6xzE_Do_Qat3KVh3K98VjjoYErCiW9Lg4xhkmAUrVw7wed3MnKn5rtAzxs7_LDIrKrOAurAUYSqOEUUY3EMvARkP3c5JHEU9e8K-CbMkjTKwcHhajhEBXXAhuf0p5RPGFfzolfMFHOwdu5eKDwbLQd6iKsrrEk525XwlHSttmdO8Cz3RQr-1gGVQGLvt9sS1FrKmE3BCdnlVUqZACT_OtDFulHaY7tj5VRpKnOSxX1Wly8ug0gQeCzfM6Nnz1WCowGCRZUFS5nlShaMo02UZcu7nqbAwtDXIAvHZNO5tBgTE93PxbJnlUYOKtKPz0hHpdefHXXmNvxoJipsd2LSOKC0Qr-F1HyhsMTok4hv6QAgtwbwzBq94cmJLjhaUXJe64f19A_ze12q9bzE5ADbxqWTF9w1QfKYgRR4auISpl4F37qWjZzjWqBgM89hyE7A937ZNuwFrGq5HBSseXsqMPeiPNZdW0X56VR7BCtSXMr-l1yzcbpFDmfKBTEzACWBIaczJXkna8CvN4SARy6XQY1eaXByUpsjKjA8qIi8MJphka4AieH3wU52UGcSedg0FDIdW8AhYYUSRE7LBjXiWV6HLwP3X9t1YlDPKhvevrFG3lIdh5mVlASaHjq-PxTZyhqdUzODOzds3-hV3NzXFTzHUQ1IX2OrWc1W86xoJTvEZOYsITa6ZSCbRzVuODKLqFjAQtEHPc5KdxQRWb-aj6kbr0MPEMXi7zT2wz5003Da7fpCW3b2Dily5TaaC6YEzBhWGZLDYG2A-cnrXOP0Y_gPzFxgG3fGDo__hZzybmY4vDi6t7vcib_gC7-7bFz9QDxl5-_Pf7vWKHXxLfq_-mqh6AVbcDetKbKH7PTWV8ea27toGqX2J-er-SG8ZbeKxrWVxnrpx7E67cb4VlhGFNBoMYjxQ6Tb3_MnyNtdLk4I_fk4UyRsGurvhSxRmJGlU9QbGiDE2ksPb_TQ9iDw_U9Mm9OAxuuytQhavfVSq3GS3v3JHbnp1bNfzI34rWdcRPau0fhQUKqvQswZMV5DAL1WBjLZUlTRYie0oov704u4Gy-Q-rveHGIlFBUsgpIc5kkpKigX1UoRthWWmZJhaTMfulnMLeo-SwThwK5a4hR8WmZdwHnq-W6Yp1zQyawHNOjizPvAny-fH-Pz8Cs2DCsWf5-sPHyrGfJaKy5Qx18cawiyJKzCq4R_PBWcqTPIyyFIv9uMyjhKv9HgCv1a-H7h-EPCoyuO0yPmR_cwVXIYXYTZTcBnnRZkGiWcLLm3BpS24tAWXtuDSFlzagktbcGkLLm3BpS24tAWXtuDSFlzagktbcGkLLm3BpS24tAWXtuDSFlzagktbcGkLLm3BpS24tAWXtuDSFlzagktbcPk7K7hMsiyL4zT0MlffIaNQZpQNZxa-qGHjAlyQjEfcLccqS10LY5zyY2tbRIB_qYLwi5mQ62LiMC8NN2FkXUwXKLfR5IulEYMS7mN-77z-00dLP4plMZT0Mr9i3RuyZ6kMQcaVpHIfi63YNVzFa53Q2u5nvz80i6i0OuyV6ycjioZYMOoGcKlgAxfChVDlA3yD4WBeqnc11JqE3bdVuLYK9_2qcI_V3x6rvD1ac_s7rbZ98E84PKnM9n3x-MEwJC_vFFhrUORwg4IpSuSt50lDQJZpMpkKxaDGA-WND717otQxq3wvBtPredaCqqFB6SK9XZ1dVRaqoRBUZFf5micAPiPwer20zJ9vkeg1ihyMeSmvRS0VlUjIqymvJAhIBv7QSch1n_lVnhfPs8gjWWIPfpgONRdDP4kU7JdJGYTPSEsKt8nQ20wGFRylgYmExQfhKku326sPyU84QUvPTf2EU33wuMjPxVEcJs9YhcV1QiF4zvUDl-XcYYAXTl-doAgiP2Xhsy8SiYrTL5EVUdfR8UwKJFijkl2M6r4Un65PgQ2XVZl4Yfrs68Xoiw4u6Ko7naWh98dcBFbxEK8QY5xiVTflfpSG5bMvmMJZquSLFqV9JxktBkeFdfC5iIHd6iqS4pQEcMECL_PQf_b1foXWyGuY743jrXxauczt6qQ1rlGFMVRQBJyP9vq8rglDzR0qsoPGiUPmPJQd-7YyMGrbXPdYXyB6L2QiV1S-qKdWxxTlQ70cJyWYKpJYHVN9D_R1UG2IGVp8w_l2IQcnc1GU3VFNCZip3aSNYlaPnTFjNeUcPTZYzS1GoZBd0V5WlR37BU1g6u0w4X9EST1EUcnxcJXJjwb6ygVNJJGsilod0zHnUPaIzljoBM1CaGbFJMLjO6wPnye6oUse2nJ17K7O8o8h_8_YZeIvqQAVhyt5X183Rm35GHjt-YDZlH6hwxhitxhLXB0T56f2peZY9lsgX4XF7sl-FazMxYowr8z_yeNXR7B3woZofmDvKGv_tR8FKe6crcfeKMpyYdpsSSUTlIIEcbaRiejVMQl7Bsn3xKbwzmT1IiaQzUCsXpCMYMsodcEa1qkA-JEmLTHn2YJxcn3UrOA9wjnsGlkMfZQRhWjfMLh0b-mcYE_ObourpWrtEz0TeJStjp_pqNd79XllWZayAqN-bl7GWVTQn1v0vGN9Xrr95uE-L-toWUfLOlrW0bKOlnW0_qc4Wud3Se-3uXruYtRwF97P8z2tv0oTb1n4eZ76nuf7Zcji0k1K36sYD1xepTwI3biI8jyMiijNitjLfD-MSw4b8_w0jKrzdnfQ0ptcePFFGM-09Ial57muG9uWXtvSa1t6f-2W3hQGLMEHyEBj2Jbe37ql91y6KOW3b9PqmNLYpap7oejOjjVootd3zzGdb6YbY3vJv_aT_p29bK6gLoU9DqmpywHmjqgjubLX_iW61gSh9c42oKeVW7SYRvEO43eMiKhEijhoHECU65UmZ8B9wNLGmSI-225t261tu7Vtt7bt1rbd2rZb23Zr225t263nanjTwss87rvBWExpJCxGif2IpIOq2g4DFhd5VXiVvupGHsIg2WNzCbWwffZ6-ca6ebgmC3wfWJAKwbG9eWKDazt9uEF-odJNzK6rImhdoGl6AfDNjsyF0XKvhz27v9BVoDWwJqkbGBOrNPW4mtHHBkfn1acLlQ7FWnHRswSb6u94Z7YuyWiCaI6TcQRZ9ktepTLSFjPRi9FMONXCV4ScsaTyXa7PzkjPmOz-yBSLtOblp2gP00GNdryMeEuNTr2hCxNE0o-p291PEtnJZdg_JDVDD7-Hf3XfjD4eld3GNWA3KB6MlplAxkZ4JKPN0B8zGrSF8bDF4MdJmIMOSFxXt70Y2aTTFsN5GaFfxH4IkpVLHefpyk9PmA9RuErRvHDiYBW8h_mQJMLaILMjOW0--FUceswLfKCbNh_GVJfZI_DIdFUGWzhs0hVPYhPvBx5YO9F2-8OV7hjXXtZD8RXRbiF9YKPk4yC8AhtAjd7xqVF6EMA0rxxsGL1SsoeEhhBdQCRCQHTsxxEtFofF4rBYHBaLw2Jx_N6wONIwDv0E5aKnfUWjVGIUv0-ucZATVrxkXgZqNc3D0RnQZQ-GDH5svQKtTOB7YJ9pR3Jzqi5VBmgJUhqIR_F6Ypr-Yt_-VyJA14YKB8UI9Y78sZrr4P_iy6-caBWoX3EYE2SAVo-bIRE_bU4HWc1wZtV8TpJZ-CloSZIVud-ITuV8eEFg2MRHvQD_CoUgtMNCgoUAISaaQV4-eM1P00m7OeqHfe0AM3y1rxgiUAxJAIph1AR3rJeeyS0ImFOMGLGgYp6feFGpw3pGeYnWAo-vC4FfjxhcD2gEQzHMnO8BnoAHJqmIgXmrgITt0l-54XYLP_1tiUpgC-ofLUEXTDspuKdMcjimL-1dGNMj3bH0VnEmx0xWfkhjAhN4eswHoCzgWVIAMHRCI36QrSI54gf-KvBoRC9dhRENeUozYHFEHlZhWRZjzFRX2size0qJjDhgUVG7gMcb2gTF3sVNp87YlkQFuKHmTcRvkLzYSCtdX13q65AAkZpp5Ri6S8SJpD0lsG4aWcKLoDd3fK2nHmW52g9m32iXe8FnqtDXOgIEPBCy7mHnObjQWLJLsmsphhGvoPzkvTAM9Qu8n0YEi8NINybVVaIGY4jYmU4HIOnfCMUsOj31OYzhDNxUteuoWVMXVldtsetlqvTEVeZpGGBtRlUUrmaHsZBJssNTKpCkvu0lCsYVOMTsSmNUGPXPOkcnKAMyulQejix4FioCeWYBbk1Z7zYyp7IniV8NRgRNhz8OCquVwJsPko1F6qt9uW24dnJT1217vebGttSKe1E37chaaIu0ZZG2LNKWRdqySFsWacsibVmkLYu0ZZG2LNKWRdqySFsWacsibVmkLfv3bv-JEbjyAjQq4-5Bb64h-DAsuhY2ebdrTve6iiKtUy-faG-tsiRMyzx5nsUY1WvE1ZgC92W5DEYElFrH8BNVF2Ie6KNvPvsvx-wRPWi5zN2MFXHJnmeRk4SFmU6aSVZME7439clG1qIERk6f6Vw_Eok0KlWt3zpjxG7DqElHCCgydBZUdCjyX6Rp37fn-k9gJIPmwrT0v7_--s9i8yqt2HHgmw7dZ3aKz8_unX6OyQ6bcueaiH-Rmfy4gJniKQCAdJTxnZKE-qSa8aHr--DbJ0gcZakbJWStP8dyRBUjxUDR89g1DVnQ7W47LcWUGZ6eePNqA5KUPSPY03_oIJooq5pN_B9gPOlmM6PvgiJapK9Xx2TwOeBOxrTTGzwPzmMI1QeQYjjFs4ghySbCtiUDYqnXxdPGnijTvNRu4DzwkCEyH1gCmITjYLr-UuAFqWLU0T5WsC8Vw28YhYRFEksYcPtQPaNMfGAZVDeNnuCuV-TWUm5MRUzKKyiwv0Vb8fAIDoGXDtnsW7Abc77WbIYJCDxTSg6NEmOUFB0j-20AQ8FpxB3TRRcPwTMdTv_JmnWCy-9u7o0l6OIA2bwwJiWbvXicPK1DpKIDgKTD2T-WcYhxXjpGFbOC-yT_vPsMIVbHJOJDd2kULc1JETV_rQxZdw6Cmcg1-su2WmZ7w-tyTGGKL2Wp0dBuj8AsveYo0wauJQIYLrLs-ahooGzIZJ9jhc5kObqu2bzmS-FlmMJAJoxglWb1qGzq0iU_ckbaoqDB-8Es5UkeIgO5Ac-C2M2zKK_KIHSPwSxpSITfBmbJWtPWmrbWtLWm_wms6fPx8PYxb2IT8ib8eR7R5lcB9CnCIAQFE6dxnLqJV_l-VYKeCaPY557L3SqLee55cZWnVVQVKKkqP_K9IINfc8rCP7i5Azyf9CLyL8JsBs8nLxMvyKvI4vlYPB-L5_Nr4_kEng93P03TOMwsno_F87F4Pr8eng8dpRZeU_e4YLfgHP4uIH9eNZrfptb-Yq6c3GweHtCwUl66ogEFVhaSY0RwUNUNk7-9NKt2PpRg8ZRbHyuNdUeSKuUwzmLD0e-ti55Om07aORa4k4674EwLNmTBhizYkAUbsmBDFmzIgg1ZsCELNmTBhizYkAUbsmBDFmzIgg1ZsCELNmTBhizYkAUbem6woThlBUuzokoL3U1ilNRo8fuoshg5R57mYOBFhZ-FGnzCqJQxk36PrHYhew3pDm-gZSUlrvE1SdZdP9WFuKXR-CfSLkRAr9iXNf1B7ywe4UzP8rSHWoWm99CGTLAggQ6ELGkapCondxjl5og_ND7puUQpVwj9lariU19H5rfYpiKKSWvUQ6LYEYZN5EPUxaKi2moJS8MORh27obg4rl9MRQNrf0ADk0zaX8n8ng1_16ZjasQwjawImVFrVej2kLOZhn4ZVLEfpYnW8UbF0xxo0XtWLc3JVaNkiKAl2nMRjM4AMiI8oIwUBqoQqTkIb8PQJb4rtMsx6KLxiXEUrQ2CUFjRTgDmdPDHo2BF78wjOvsX4QAAc_kvfYM1Beec0jgxCI6SuTkrCl0BYdSFqQbxJ9R2zacJydCJ41Wc_NFEIFqYgXwFSWNmCRC-A5QH3dCxhjlKkab4vIM_LbctWPoUUvpwjm9GgaRWMPa8jvEyrMUSqT8Vm5nsNgdHCXvbRvXAyhJ0CZeF3EamxSxq7vkao34wGvzSykbma1VfItpVnc8P16zWhW4IuiTNADcnxxyiqUiNW8UGEaXTf4OW9PLFeAcqdkumrKnvRNYOmVt9OyE_1fNiQIzekXpdZwBlGq_uJ9gnaCLMgD9hWgbLgWDUHDP1Y5FHp1TDKbAlLwajyC88L-QnAfzOLal7Pzi_onCTwGWhmyTsKXB-VMfW7noscDhA9hsh_VQVioHsp5D7QOESLyE5ycQZIZ9owzLaBDL9BvSHBsgzofHeFwHvT-0d2lULUdoiS-40e1LOkTJboNX3y-mFoXm1YW_4ZcPvLsu2uKLpr_DpS_6WYG6u6XNyfuB-NbtNjgAU6D6bPQOGVypPcbGfDZazk4li_LHnB9SbxeT7x8XkY15RZGnq-jwMfnlMPpF2AEE718DxKCw-ESkiMKYeI6CzzSkKOMpoTnFkYxGT7eLtGqFx-N1SPStr5uCW6Y-EaEFKngodx1UexWnEg9zV3otRUmx4L4-pClbuS5Z6hRcjmIl2X4xCYUOePrbWl1_WzaWkzJX0QKZySFCobficMAKjf695Zi1W0UqsNzTvySjBTQrfE38jADNpl4--tZTjUxmx0MVnVJ_z6def_JfMBdBwk1PDQsR2a3TvCUAM5_U3H6n4PO4BI1jCDSfJY9aMkHs2vBRIDi9FJ4kDOqJ40yuvl2LO847UmsolVc2NUhFGPcTXeBcIh3W_L8jUPB9KaLYjqKx0oXwahSDrTuikmVo3eVnOzM7Nl_ZJjdJQDkZasg-pD4sDaXEgLQ6kxYG0OJAWB9LiQFocSIsDaXEgLQ6kxYG0OJAWB9LiQFocSIsD-Y-OA3kMAfIY9uNR1EeL9_hMCDWB78deFj8TksnfXr784cL5g_O_2vzi1vMF-etCi8J_O4G2wYsq9OKk2luJ76hBTGsBjJfNdngYLOeBt0-gbSRFmLuxGz7Tco5RhmI8wHH_9n3znZlzbkhv0J_v6p1TVPMiL0h49Qsvk3yMXi5SihC91g2Dm_DWuTuxzDACK6GMg194mUJoyWUKT1FWQ23IJ9g794NlBlnhBQHLf-FljoEtJOnnFG-mTljjC-f5EAtHiDNdPnW4nQPEQgOBjKL681B-hvyYhz17pdo-FGDhKWLOQ6sZkuEMaDW1R7hWskoCd4LeigjwgW3birLpjnAljlz6c0Dc5u8BRWFJ-1JgX1mB02QOfF-0m31EQuM2nzF_4gsgxCl76y4z3OcyR3dwGAHX8K8OHruZ81MqdLlSJkYOGJUCqpMmQLkgme85csEe2KAR_JVXcaFjd8JR2avUFQUCMmMgQAL6I4B5YpK5G2F6vCZ_1pixo4CvKAUmaEyJgjc52H6h6T9tgjCvkjwIjVcpSEc9bEbIW9v77weR5yZFGviBV6ReBLcz85OE5UUWHoPI0yhDvw1EnjVArAFiDZB_EAPkfDTOkzho3s_zMGe_CshbWOReFAVlFgc5C-MwjllSJmUeR1lSlWFQRq4fugzYmodRnpdVknlFlSaF78ZVVPJzNrcP8ub7F25y4aVzIG9p5ed5GFiQNwvyZkHefm2QNy9KIhbxxEuSwoK8WZA3C_JmQd7-uUHevuR73S_FTdv2sj_mMKhiNPGo-gYdgGlbbKFyXinfGctWFS688Hjlhb7h69KsJ1HklKf6UDBFoxwdi4jIis6aemdNiUVC6g7hNrAaeZwfzou_vWE7zDiMZchLah2n8JEIq4imEOnZ6_DLmKeTqTfDqFaNFlKUl5O-QYuyZ1H2LMqeRdmzKHsWZc-i7FmUPYuyZ1H2LMqeRdmzKHsWZc-i7FmUPYuyZ1H2LMqeRdmzKHsWZc-i7FmUPYuyZ1H2LMre7xJlL2JF5YdV4ruFNpSMSlfJto-pVlUpkNwrWOzFLEp0PsAoYJ0o7fevQVXmXliAW5bzPA_15TPKUh_YxVmVpczpNyjZlT7SnGYuFY4IyxYwcd-0G4H6J3KxoP8n6eYL3dq8nE1YG1k4DCaIjgDgE_0U4vLBcQMnUuq3ddga-0rvjcvcc3URQNd-MfYVCPbSWV_VhQtrvQLeulQ7uzIihmOuTwQSiQcbBaiou7Q1N2NvIIay0U_DNAQ66ZjoI10s-hoIfkCE8eW3ZM2oxZGNAc98KFySaRRU1aGhYVPwMcor4clwfJAo6hYaVpTKfa85w0MVZi09r9tJgJTmdT8VKw6D0nMZT6JsDFyNVcYPcN1ZhcIg22dU7Z7OnIOmwHOaAlAtJFwZmlGiLWAfT-ookoMG09MlcUpmi0oFTDiv2-Za18_I8RjCoJGkArPqNRVkya8I6Qlb3GWUKKSQpGQK01qlzYrtfEkwVbQp7aXJ9_703XffTEMHumXhBIaZxrPS21IvMewcVt20CFSA0aPVWDU65UYK0BqFPZ4vHQJhNUyMb2kZr8ShyRjI3gvooMlKEOREHTUS3U2S8ihRyHyY1n-YQgbOpN2Oe6JoOcyK8TzaNlv37eHegYhwKwbVLqxaQMAOgAllrI32j1mXh7IpSeyzPIvcLNYem1Hg_sANOatGfS7i5QgnS0ibOfdIdx4BEUeMIe2yXyB-KpwI_Du2pxOCHTlA5UJcFS8K6NzgfyakSsG67n4CfDIBV6DAAkj7pievey_gJZL16DxQ4Qgsco3YK0cLgyQxkDUu8G5fUZhuGVwZRV_SlURijLpElqcQ7-qmZWy7bnfdcDPKaKzdEzUVKKJVnSQCLgzOFT51KUqMLjUfXhmOoLhd0s0S-gkW6XmS31UzE57XhyTW8IXxOXkvVs7HkutlHEJsmiqoxAsKyBC0LN-bcCGcNlSY4KAZuelbyqKc46dVJQvClIVlHms_zWiAeICNz-ph6HfXCLQgEm6KLIZpoTLYZsBoL_mGFZIikks6cMZeP8z_m3akEWgay95WzkdyMXpm4XeUTrZIslAF4w6EnOctfNejz0mCo9my6zH8GI7hR_x2agbrUhUZ_ZK9cvLt8VlxHa8-iFeBu91eHc5_9UGySiP1FSzhQxGXO8xh7AO0_ufRhj2acumukkhCGi-9VRpfKeJvheTBeHq_Rd8EbuK9TlqM1XYl74uuzrmWr3jxpDQTHgfakQiIgEeUc0cDU4oU9q4oQCYALfb6Fy2UtoXStlDaFkrbQmlbKG0LpW2htC2UtoXStlDaFkrbQmlbKG0LpW2htC2UtoXStlDaFkrbQmlbKG0LpW2htC2UtoXStlDav28o7SeBKx7CWj4vKuIZ4z8JzvCM8Z-EQ3jO-HOon-MI4vY-EdpzHjD5ELB4nExj0NIHWJbD1ipw3bEKg7DFDZWRdW_QWqF8LViT4FxhbpemkM9QQRD4yFqBSvg0R3BjeRSZlsQWFfWenFvITaMuH18Zl2I4Reaqep1m3V_X-2HMhikv_NKPeVZVbuGDyxGEjFP7yDzGrAI5fBhj1t7Mf4qbeT5osQbbHCE2w4Vexz6WqEbT_FWwRHkS55kXua6bwZl4WYEAB35ehEEZp1lUgsGd-RkHW6YIysqHz9PcLV0PHPU49Yv8vO3NoYlmF142gybKkhTo5zGLJmrRRC2aqEUTtWiiFk3UoolaNFGLJmrRRC2aqEUTtWiiFk3UoolaNFGLJmrRRC2aqEUTtWiiFk3UoolaNFGLJmrRRC2aqEUTtWiiFk3UoolaNFGLJmrRRC2aqEUTtWiivwc00V8F7DN0I8YTjzFvhBM6BPu0SJ4WyfNsJE9whPMwDVM3quLjSJ4WqNMCdf4PBerMUwxFe37ARpl6CNRpcTgtDudvicPpezGPwsrNS48dx-G0CJsWYdMibFqETYuwaRE2LcKmRdi0CJsWYdMibFqETYuwaRE2LcKmRdi0CJsWYdMibFqETYuwaRE2LcKmRdi0CJsWYdMibFqETYuwaRE2LY7fr4PjNw95aRzF4fsS8_KTNeuEl02ZDm0SHUK0yBo5lLvK8tLKXpTurY4d1LmzC3EwDSgfB2yhpfQcKTCITOzeCoyjPLqC11tQTeMKqJRI9rrJkhHpVlPhkBQ712PJIIErHTvgo7N-yXKuypyqsb7C0J5G7SETv7Udds_em0UYR8BEBVXvZbgVvS95YEtR_iL_Pvti0uEwJS0tYiHL5VTSniLmohlGLUGcPiK_7HqZZZ-6C7A1xAAAXhoHh91QGSasSZdkSpRTTMw1u61ES-3fD52Uu2HqJpGHcIO5F6RhwauwJLTFWXRSDZpo0Ul_r1LtfPzZOTzNn-chMn8ViFC_TMPYq4o0jfOszLM4yOMQVuvmnh8kgV8lZZHEPPHdLE2jmIdeHoQVGKRuVcQVlSYc2dIMLKjnXgRzsKBuEaXcA1vTwoJaWFALC2phQS0sqIUFtbCgFhbUwoJaWFALC2phQS0sqIUFtbCgFhbUwoJaWFALC2phQS0sqIUFtbCgFhbUwoJaWFALC2phQS0sqIUFtbCgFhbUwoJaWFALC2phQS0s6D8LLGicBWB3BWkRVtFvCgu62C8ztgih__gIoXkWYbtm5PIssAihFiH0cQihuvj_HxgqtEzBogSnN4rCzEKF_o6gQveaPCxgKEZjospzucuFoXEEMPQzo1mlsuChFjzUgoda8FALHmrBQy14qAUPteChFjzUgoda8FALHmrBQy14qAUPteChFjzUgoda8FALHmrBQy14qAUPteChFjzUgoda8NDfJXjoDz__fy3RDss)
