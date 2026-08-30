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
| Let the executor choose graph traversal and gap retrieval through bounded tools | Promote the v12.1 workflow contract | The host still permits at most three bounded, read-only tool calls, then forces final synthesis from the evidence already obtained instead of allowing an unbounded fourth search. DeepSeek and GLM both passed new workflow qualification and separate 36-cell formal panels with complete terminal telemetry. This promotes the agentic disclosure contract, not universal model superiority. |
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

[//]: # (ob:3a0e7bbe)
### v12.1 bounded-finalization result

[//]: # (ob:8abcfb00)
v12.1 retained the same three-call tool budget and evidence boundaries but changed the terminal behavior: when the executor requests another tool after exhausting the budget, the host blocks that request and requires final synthesis from the current governed context and segregated candidate evidence. This is a new preregistered workflow contract, not a retrospective rescore of v12. The final executor call remains unable to traverse, retrieve, mutate the graph, or admit a claim.

[//]: # (ob:dfe87bc2)
DeepSeek, GLM, and GPT-5.6 Sol each passed a fresh four-ask workflow qualification before formal scoring. DeepSeek completed 12 of 12 qualification cells with 44 of 44 terminal receipts; GLM completed 12 of 12 with 56 of 56; Sol completed 12 of 12 with 57 of 57. The models then ran as separate single-worker formal panels to avoid shared-provider load. Each formal panel contained the same 12 lawyer asks and three conditions, producing 36 of 36 scored cells with zero inconclusives. DeepSeek had 71 of 71 terminal receipts; GLM had 76 of 76; Sol had 173 of 173. One GLM relation ask reached `executor_ready_forced_finalization`; all other agentic asks reached `executor_ready` without forced finalization.

[//]: # (ob:e4329246)
| Executor and condition | Rubric | Mean context | Unsupported claims per ask | Citation errors per ask | Authority errors per ask |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek v12.1 agentic disclosure | 39.90% | 7,273 tokens | 0.000 | 0.000 | 0.000 |
| DeepSeek full-graph control | 38.01% | 20,455 tokens | 0.750 | 1.417 | 0.333 |
| DeepSeek static baseline | 33.33% | 23,985 tokens | 0.000 | 0.056 | 0.000 |
| GLM v12.1 agentic disclosure | 43.69% | 12,379 tokens | 0.389 | 0.417 | 0.167 |
| GLM full-graph control | 36.33% | 20,455 tokens | 1.861 | 8.917 | 0.194 |
| GLM static baseline | 42.64% | 23,985 tokens | 0.000 | 0.556 | 0.028 |
| GPT-5.6 Sol v12.1 agentic disclosure | 37.65% | 13,454 tokens | 0.000 | 0.000 | 0.139 |
| GPT-5.6 Sol full-graph control | 29.63% | 20,455 tokens | 0.028 | 0.000 | 0.000 |
| GPT-5.6 Sol static baseline | 37.04% | 23,985 tokens | 0.000 | 0.028 | 0.000 |

[//]: # (ob:989b7acb)
For DeepSeek, agentic disclosure exceeded full graph by `+1.90pp` with a 95% bootstrap interval of `[-6.79pp, +10.23pp]`, and exceeded static disclosure by `+6.57pp` with `[-6.13pp, +19.84pp]`; neither contrast was statistically resolved. Its context was 35.74% of full graph and 30.32% of static disclosure. For GLM, agentic disclosure exceeded full graph by `+7.36pp` with `[+0.04pp, +14.64pp]`, while its `+1.06pp` delta over static disclosure had `[-10.71pp, +12.39pp]`. Its context was 61.22% of full graph and 51.61% of static disclosure. For Sol, agentic disclosure exceeded full graph by `+8.02pp` with `[-4.06pp, +18.30pp]`, but exceeded static disclosure by only `+0.62pp` with `[-9.13pp, +10.36pp]`; neither contrast was statistically resolved. Its context was 66.11% of full graph and 56.09% of static disclosure. Sol's agentic score was below GLM and DeepSeek on this panel, so the sensitivity run does not support executor scale as the primary remedy for the low absolute rubric coverage. The result supports bounded agentic disclosure as a qualified workflow for these three executors on this two-task, 12-ask panel; it does not establish a universal executor ranking or a complete native 12-task Legal E2E score.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZhZDMzM2RlNDQzZjM5MGM5MjBhNzNkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjUzNjZkODFiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xMGZjMzk5NjFhNTExYzYxMzA5NTQ0MDciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY3MjYzNmJlZWNhMTNjMzE1ZWU3Y2ExNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfemSG0eS5qukcaatd0wAmPdR_MXW1ZqVWhpS0z1m3bKqyMzIKjRRSAwSKLJa1N99gH3EfZJ19zgyEkgcrCpR0rSbzKgCkBmnh9_-xY_PxHozb0S1uZzXzy6erVaXqaijKKplHEdNVPhVEfoii-r42eRZ2db3l_X8WnYbeLa7EWGSXvh5GQdhViZ15fsiLWQTRGEc-EEexCJPfL8ReZDJqiyqtJRpXpVZUYWyCsJAyKQood163lXtnVzfP7v4ET9sLjfiGnpYiA12NYE_SrmAL_4s1_NmLsqF9Nbybt7N26V3A8-363uvvPe-W7dts1rLroN3VqJ6I64lTmrw9br9u4TpbtfY4M1ms-ounj-_nm9utuWsam-fVzdyeTtfXm_E8jqP_OeDt9fyv7dz-Pty28n1ZdUuO7mEtdist_KnybMbKXARkyhN6zzAmeE3l_KOHoLFlZeB31RRUaSBSIKgSoPIL5I49jMcWbve4NQuF_OlhJGbHVlcplmYRrB4shJBVEVBImUGf6ZqOnp0l5VYddsFTDjEcVbtuu6eXfz1x2e6-x-fwS636w7_Uj_L-rKEJf_rs-3yzbJ9u3z2A8zB0ANu8GZbz2X3XKzkuykMaLmZyjuxeP7lt3_-_NWfPv_s8i_fvvrfX3z97V8u_xz4l599_ulXr7_69k-z2_rZ5IPISmw263m53cBuXpaim3fYt1w0l6KDVd5Iam-7uWnXOPY38yU22d13G3kLvyzFLW6ymcMEXu2QMJ5dLLeLBcyouoGdlGotykVbvYGngzQvqyiM4HHYxI18h_P9EmlwKWvvL-36TbNo33p3gX8BVDW_A0L0vpbXYuF9fifgJT0IUdc0uhVSo3wL3_yLd24ri63AGXufyYoIGZrZ3K9wKkg0QIDPfpr0AxZxWjdlWA4GbF71yna7rAWcn2Mj-xdv7PljffpVHqW5eHif38Ph9G7lbetpgvSEt1ILMfE6OOSynni3bS0XU1H_Haitgl9qD6ls249tJdZiMLCqKZMsavzBwODw19tq49V6gN2JxRh7_shilGUS-WEhH97ne9vlf2-BreEavu-35D3QxLyWy0pOaWVhxUSH3_9t-d6bTvvBEY8YLkdRRbnM0sHQPl2I-e0UORQwp4p6Ay6xXWxOLMux944sj59nWRbG5ePH8P2N9FYCmGztBeF0I7o33q34e7ueb-49SyTY1IpWEx7bwBtNu4CjdoRm0iLKMiHqxw_wvfeNBIZVwZZ99ypKvbsM_oIzPgvMZk09-vfC_g-_fqVEx7GNFHHpNyAZn2YRt8tuu0KhIuvpGlmPAKq6aZdAe9NrsfLmt7CCd_IW-Dqcy7WEgyqWuK9HDl6d-lmYhY8f4NS7hSfmUzgKILtfvfrCewsiGNjDQqyv5drrpGqpkxtvvqzwMMBOL9t5J71-gAuQ_YMBRpUsslg-ERk2IEBoj6fd5h50DkOPmoeHnwOhLuXCeys6JMK1bFpYxmV7ZAUlaElpEoW7bOQaRfj8Tk5RF1q03RYaemsEyFkH9-xGjpzixM-DKGiqJx4dreW6_Ydc6gXDxsV8SUccdvztvVzrJYblBWKs1m3Xeddrsbo5spZlHJaRqJ96tO-9T1VrOMx6bhm1XL2W8o233pbq8H8Nq9d_Uu8cO91hEgeByOonHu6XuErTdrm493SzPWf8h1y3Az5Q4VGYeNV8Qzz0yOI2eRHFIiqGowWJ_dWylu_OJMn9x48QX5wldVr5yYN7_HbpAf-S3oaIiPiJpjpgd90E1AotYJGpkMEBjXti4zXzu2MrEfhVLeqHj8t99hbIHrWgei6uly1oARUINbHayPXM-wr48KZdTWvQY726rbbAmo-Mq64akLk76_WZbAQMRylV3rpdyO6kUjj2xpF9SuM8yUXZPKbfniNMQBsSC7DqgFxrMFUW7QolEjSx3UizYBfHlqGQUpZ19JjhvO-VdXwWjvMr6v699wet5e6IdvMvCfbjIt2HxZLxY0b3EqSQerQSi0Xnge0JJPsOFgwFOND0GsUPLNj1DelCvRns1ccWLvb9FGywHX4kwea6g7bFurqZb0AMb0lpOS56Drx0zLjIwqBO6-CRvZO2qNVq9x171OoW_z9dyu1mDUIbTvscjhkYI_I4UdWyCfPkkaO7urrCd_-27NrtupLY7Wrb_W35__7P_7XcyOu2JSgmoKCp77WLgdQy9U0_zgqoYCgChYhknhVPsIpKqYG1bOYLHNRqtQDj34OjKav7Cr5C2-wa9HAJrHRBD5M0OcY566bJ_WAooP-kJWuvjMl3K7me44RP0NmJV4-ZJzAJmYTxk4zkiy1R2OBNFNhed9NuF2CPoAq7cTe4aebVHP6-93ZX64eJ8c88A3mEluAlKrvK6UG_GA-KvCyqIqv9WJRVLquiLMIsr6MwxSO0bDfUpnYhedqF5FU3snqzauc0IeiRekK_iPmEbpEf0Pe0mFf3TguuP8pphDxdD3RVdW2zuWxgZ-R6tZ5rj1hXBheZkGXcFGUdlFkV5GWQF3Uel1Xjl0Gah0UZ50UoqkTWdegXUdFEfpznKbyTZVGcorLfgT5Dni21Wxdh_hMsNDqSQj9Mp34-DYvvg_jCDy7i-BPfv_DReaBXHDc5TEoRygyIpv_2x1_CGUYUq5xVN6K7UUZXnFd-EDfEj6gNx3-lifmpHU-6c3I7iaAJSjJLqXPHF2U6P9u3pJv1fdjbMs8kzN0227ubdLOPcR_RHGcecjb9GX4hi0IZu8t2OVVORdKF70ik4rnuZt6nYCnPa1w04nDA7yp4ClQ1WGDoZANfdPMFfPBgswQ6VUG5fCerLfzpgeKw2uIjaG73Q_E6lDmm7422ekD5u52Tu7Lz4N1bsdngl3pc9zMwMiq5RNNXiQ6l4i83qDW1SoeHnoBp366wy81aShqtBM6zmYuFHoZeNLC-Nnr68l212MJRQS3sFrSGOX6tqHQ2wtENKTYyKgOZJZJIj7bNccb11HCmc003K4SfJ0GSBkFUm2Ydf5tu9lH-szG9Ta4WAtizceLQXu9wdbQhtGvH-6yljcPFbkk3VD_AnoHMAMXsHrpUZpdjcXm4olsjKzvaDe14Mc4YbZ2U24134LXeWGkk6oK2R0XfIJnW8nrewbdEKM4ErnHXOzAqVsZPhi6NA36MmVqXb8Qb0qmMXeo5dik2UWvtVTFBGCjawYpyp8YCffndVx7tl14qHGYYTyvR4fvw5O18OSfrpxON3Nxrv8AKPf6gtixQ1e2kNuLIiiW-CL8tpMCwzgQPCah2yoDSZ2iCZ2i71MfnH_D07XbjMAKYN07bGtfGGXG7WkjFONAZVeEa4z5d71vW2tMDS7puMaiw8TBCZTgLnj-xQfVBL-Xrm_mKnl-Bqefa9zDP-e18IfpNclfrFXC7W2imVr-LqtquRXU_8er1_XS9XQIF4cTK-QJ4xMQDHjOvUY28nW-QLWruuJBTPGtAlX9XzjR4fwtKHTJJ90siyVrerqBzVFFw9fVGqO12t0sTymvsjNYceprjdpHSAkwMVwsIXFGxVYFoX4Ce2gXSfWX4qzoPS1z3fhddMuxNZ5fy0Hu5Rh8svThyMvvXsH189WYOBwi14YqU3HmLHdbkUtx1BcBosdnrRVvCs3_4JkwmJH_u6HjB8-qXKf7i4ZiR5d4I-mm7nANzQmYNbzgqoG4ZxUQlZa2XFuObuOJgvEnQHRe12gxsa740ZAmNEZktwCTYrO_16nx2YCm-7EcNn77a4MEE_a3GHRj0PVgQZ0PmS8UnlOMEBwFMCuxxdVZweOKunWMr_SKbedBim4ECC5svlDx9P2YhW5GSx7WM4gzsZCtS-oBGL1I-MDChm89jv4ylL4okyUzzTqzCKhoPjzkg96PjrQS_d0vBgVGXhdWpijjxqzhNcqv8OOEJK-4eE2ZQPhSJDgP4OfD9me__zv0Ln_3PQ3LKWyuWFBazIqbXolmQ6Lf-2IcQbAeZP8uo_Tyc5YV-8PUpaUaPBzm-F0ezGHs6QilAJHUMFkWRk46oVVEbMXG28qGRDxCOSg7D7t57teIqeARABcNmGjhExP17f6qZCvB1IPTPHAcWDF_pZyA_a2ppTkpZc09aLLIqnciAlHeMXIoykWVTlmD_2BPSB2L0vB8TUBGkLinCLsGkw9PdU4aZ44u_LafQHp6O6VuYi2IyWn4vgD3YiWpuOXxTcxQg41oSW-mUa321ALUWp64k7bJd34I8-4cWfZp9W9dtM18DN1zNVxJNTy18FsghHb8JvXZgAsR3MbowJ2UatGvyvcDEVfQGBcNGEaoVsEq4wBfrOUq3pWbe90rfItNgNhKU0vsXNXEShEWQV1Vl9s-JUzl0-9B4E0x-SyrOnKYldjRCvUWoBqq5kKAFtgUcXyD9ob9oiWsg8GUyVI4YAbmI6qSJmiasLUt1wloDI-DBESljGeSVTKK6knkem76cIJW7dg-ML021YEcZrw7stJZw4GuyslZoFIGsB66hZPMSnl44rjD02gO3XAJv2K77gJHWXDdvW2sYKjsNDhmufJB6bYP_0mLXpHMqZYiUXZT-SzDQcOmgi89JL-1dwKQhwEkkvQwoA86bnK9A6fweeIr1FeOhQEq5-tdgVkRxevVCKVF95KGX4NQqvXH1ryggwvDqCAVEdZY3jV-UWWmdAk4wzgqwh8fRNh6cXuAgypQ7JO8csWdEJNAyEDtpPEZnBzEWz1KSTmE0ywP6w5-ESeJt2jfA2lULpF9oPZ44EYm_KKPHk1makhzMJ34aDd6j-JviYtcD5QteCiJ6KZnlqploUhT5obcHGtnNPaxH7Y590EqW2laOSMwgC5uq8OuoCqy57kQhTdrTIwKI6lBYf4Un12ugdBKUZQsHwBL_zHtZ17TRSlmFKfZSyHSLbVlhqWS0IQwghgYlAzBszejUSdcj6w4ZrNpeG9iqYJwqMQ_mUt2Czov96YZgspZa6WSZ0eKUlH3YrCXIIRgMMpMLzxgGxinRGTewikA4VuREC1rT5M5zYjWFX66vsbUjhy8OyjKQvgSlwKoDTrDWYb9nRV91q7Wf1zWoyUISE6dWnYCsbvUxEVZJzCj3ZwmcJFzNgYGV5rMkVN87Nh-sdL9eavmcBijWZR6eKqOOzp41Z4x_BH6ZAqvcdspo06o-an00KKJyrS5d_dWfeP4PV0C_7QbjMqAuAnWuYQAzl2ECyVLSYn9Ijlp-eusNsdArIAE2N3M4Vrh-ezblzPuLWN9qfW5VJGr5QF9OUZcDGtW-vQ6jBDoyuBDkI9mxGA_TUpj4YRBWpV_mlkE44e6RWPeHxq83z43iiQFdPH3kabRhKfKbYcovcIONckYC49i0t9PtSiuYcNBhkviOUc7t6TfMopa3ZBeikk5sBXtW0SxyGKIX9qhKUwbCL7NIhmVp1sEJr7te7jOD5eawhiAjwyKMm8QeKyd-vqe_PDgabje0iuuwrCMpUjuRPkBuJfNjwt2Onj3U5N97__EWSBFkrBdmf5iAQLu-0W5Y3Pj3jl_dDXKStH2B3hPF6yfeNblC4DRrL_t8iYY19W6dvAJoBMQL7Hm1q1n8Ofa-WMB6ALmg8wNa-YdU-hm8_w6e91Q4VjuKsSXtuBp2sWmVuEMygkmKxVgnHprRY56tvsGvtaVgeYKOJoD0_-77KagW3usW2_6zii54qMKs8UGlrVvHmCNnlc5DJsl9r1DbGMT4OD9FrXeqSHel31WGOigSMKI7kuB9G6SYRTNfN_DFfDmyp-67Ss44M_-TiqyYyALKwlq5qSR6FKHxAK0EJDw0Owd-FPPsEf0mLrI8KUDDkXndewRswoWm9sekTzhH8OVX3pewsW_FvRZ80FgJ_BZFUTmvYWdn3jfasLKaOfU7sR1N7FsTGAa5sdv1Dru2TNY1Ao7wrqDJ6hxWIkwLq4w7qR2uOXZ-loZhJ2UaNk3tyzpq7AL3iRuu9-zpcjCMY7AqiiiryzJr4p6V2bQM3ffTZFg40hp4gfpu6Pd2HQLq9zF_to7ymEZV2NF77qnwuvf3bX2NH50Axc0WdFpPpRao1_C4b8ht0Rsk6hf6QjEtRbwjCq96cqBL9hqUHpc54d39Eui9m5vxvsPgAOjEx4IVf1vCio8kpOhNA5MwDwqwzoO8twz7HBWHYB6abgK657t22d6CNg3Ho4ERb57riD3Ij4XUWtFueFVvwQzEl1G_tdWszG4VQxnSgQ5MwA6gS6mPyV7ptZFXlsKBI9ZTJceu7HJJEJoqKtM_aBZ54hDBIFoDK4LHB7-1QZmNmtN2SQ7DTatoBLQwWpEjvMFPZFE2sS_A_Lf6XZ-U0_OGD8-sMadUxnERFHUFKof1r_fJNrqHx2TM4Mzd09fbFW9v5uQ_RVcPcV0gq7vAN_6ua1xw8s_oXpRrciFUMIlO3rQnEJO3gI6gW7Q8B9FZDGB1bjxqvrQydD9wDNbu8h7I561W3G633UZrdvceCnJjNrkCpgPK2Bg3pIDB3gDxkdG7wO579x-ov0AwaI7vbf0PP-HejFR8STBpbb0XWcMXeHbfPfuBasjI2h__dadWbO9Xsnvtz7SqF6DF3Yh1jSV0v6aiMrm8m6_bJa72JcaruwO1ZTSJh5aWpWXup6k_rMZ5pTQjcmks0YlxItNt7Pmj6W1-kGeVfHifyJJvBcjupZwiMyNOY7I30EeMvpES3u6G4UGk-ZGcNiUHD63Lzih08trL2sQm17sj9_SkZ4dmPd7iK026nqpZpfEjozBRhU4sQXUFDvzcJMhYTdVwg5majlnUH5-9vcE0uT_Md5voF4sSloBJb8aWVK-kGlCnWdhKaWaGh5nBrMXb6diAPiBlMI38RmR-FcZVEWRSxkHo13ku7Rq5uYBuHpybH_gj0_khOj8_Q3MvQ_Gn8fzDU8mYT5JxmQvhh5hDWGRpA0o1_BP4YEzFWVlHRR6kYVqnSRbUgczgYxOGkR9GkUyaEgu45YH5jCVcxhdxMZJwmZZVnUdZwAmXnHDJCZeccMkJl5xwyQmXnHDJCZeccMkJl5xwyQmXnHDJCZeccMkJl5xwyQmXnHDJCZeccMkJl5xwyQmXnHDJCZeccMkJl5xwyQmXnHD5K0u4zIqiSNM8DgrfniEnUabnDWcmvphm0wpMkEIm0q_7LEubC-Ps8kNzW5SDf2qc8JMRl-tkYDBPHTOhJ10MFxiz0aWLqeODUuZjee-9_uPLaZikOhlKW5nfiPUb0mcpDUH7lbRw75OtxDUcxWsb0FrtRr9fuElUVhx2xvTTHkWHLTh5AzhU0IErZUKY9AF5i-5gWZt3LdSaht3nLFzOwv2wLNxD-beHMm8P5tz-SrNtT17h8Kg02w_F4wfFkKy8Y2CtUVXCCYqGKJF3QaAVAZ2mKXQoFJ0aJ9IbT717JNWxaMIgBdXracaComGJ3EVbuza6ajRURyAYz66xNY8AfCZg9QZ5XT7dINFqVDEY91Beq1wqSpHQR1MfSWCQAuyho5DroQibsqyeZpAHosQB_DFsasyHfhQpOKyzOoqfcC3J3aZdbyMRVDCUNkIFLD6JZ0W-Wl29IDvhyFoGfh5mkvKD-0F-obZiP3gmGkyuUwIh8K5PHJZzmwFaOH50oipKwlzETz5IXFTsfoqkiLKOtmeQICGWJtglKO_L0OniGNhw3dRZEOdPPl70vljngs26s1Eaer-PRWAWD9EKEcYxUvVzGSZ5XD_5gMmdZVK-aFDWdtLeYjBUxBq-Vz6wO5tFUh3jAD5o4HUZh08-3m9QG3kN_b3xgllII9exXRu0xjEaN4ZxioDx0V6fVzXhiLl9QbZXOLFPnPu8Y1dXBkJtl9cd5heo2gsdyFWZL-ap2SFBeaqW4ygHM0kSs0Oi70RdB-WGuK7FN1KuJrpxUhdV2h3llICauh6UUYzKsTN6bIaUY9sGrblFLxSSK-rLJrNjN6EJVL0tBvwPCKlTK6opHo4y2dGwvnpAA06ks6Jmh2TMOSt7QGZMbIBmoiSzIRJl8e3nh48vuiNLTk25OXRWR-nH4f9nzDILp5SAis3VsptfL53c8t7x2skNRlO6iXVjqNmiL3F2iJ0fm5fpY9qtYPkaTHbPdrNgdSxWuXl1_E9vv9mCnR12WPOJuSOv_X3XM1KcuVj0tVEU5cKw2ZRSJigECezsVgeiZ4c47BlLvsM2lXWmsxcxgOw6Yu2AtAdbe6krsRRr4wA_UKSl-jybMQ6Oj-kVrEfYh-1SJ0MfJETF2m8FHLp3tE8wJ2-7wtFStvaRmgncytb6z6zX64PqvIqiyEWFXj-_rNMiqcrSlzIIDtV52fKb03VebGixocWGFhtabGixofU_xdA6v0p6t8w18Ce9hLsIfhqvaf0oRbx1FZZlHgZBGNaxSGs_q8OgETLyZZPLKPbTKinLOKmSvKjSoAjDOK0lTCwI8zhpzpvdXklvdhGkF3E6UtIb10Hg-37KJb1c0sslvR-7pDeHBmuwAQqQGFzS-0uX9J67Lkb47eq01qfUV6naWig6s30Omqr13TFMx4vpet9e9vtuUL-zE81Vq0tuj_3VtOkAY1u0Jr6yU_6lqtbUQtuZ3YKcNmbRZOjF2_ffCVpEw1LURmMDKl2vdikDzgOmNo4k8XG5NZdbc7k1l1tzuTWXW3O5NZdbc7k1l1uP5fDmVVAEMvSjPpnSCVj0HPsBQQeTtR1HIq3Kpgoae9SdOISzZA-NJcyV7rNTy9fnzcMxmeD7QIKUCI7lzQMd3OrpmxukF0rdxOi6SYK2CZquFQC_bEld6DX3-WZH769sFugcSJPEDbSJWZq2XUvofYGj99VnExMOxVxxVbMEk-reyrVbuqS9Cao4TvsRdNovWZVGSZuMeC96NeFYCV8VSyGyJvSl3TsnPOOS-wNDLFqb19-iPkwb1evx2uOtJTrVhk5cEMkwpWr3MMt0JZej_xDXjAP8Hf61dTN2e0x0G8eA1aC4MZZnwjIulUXS6wzdIaXBahinNYYwzeISZEDm-7bsxYkmHdcYzosI_Sz6Q5TNfKo4z2dhfkR9SOJZjuqFl0az6APUhyxT2gapHdlx9SFs0jgQQRTCuln1oQ91uTUCDwxXFTCF_SJd9SQW8X4SgLaTrFY_XNmKcWtlnfKvqHILbQM7KR977hWYAEr0tRwqpXsOTPfIwYTRKiV9SEkIVQVELARYx64fkbE4GIuDsTgYi4OxOH5tWBx5nMZhhnwxsLaikyrRs99H5zjoDhtZi6AAsZqXcW8M2LQHhwc_NF-BRqbwPbDOdE18cyguTQRoClwaFo_89UQ03cWu_m9YgM0NVQaK4-rt6WM2VsH_5dffeMksMh-xGRdkgEaPkyEWPyxOB14tsGdTfE6cWdkpqEmSFrlbiE7pfHhAoNksRLkA_yqBoKTDRIOFwEIMJIM-fPBamOeDcnOUD7vSAXr4ZlcwJCAYsggEQy8J3opOWyZ3wGCOEWIiokYEYRYktXXrOeklVgo8PC8EPh5QuE5IBEcwjOzvHp5AACqp8oEFs4iY7TSc-fFqBX_9dYpCYAXiHzVBH1Q7zbiHRLLfZqj1XWgzINkxDWZpodvMZmFMbQIRBLbNE1AW8CwJAGg6oxY_KWaJbvGTcBYF1GKQz-KEmjwmGTA5ooybuK6r3mdqM2303j0mRUZtsMqoncDjS5oE-d7VSafK2JZYBZih7knEX3B5sZBWm7421dcjBqIl08xzZJfyE2l9SmHdLHUKL4LevJUL23XPy818MPpGs9xxPlOGvpURwOBhIecdzLwEExpTdol3TVUz6hXkn7JTiqF9QXZDj2C17-nGoLoJ1KAPESvTaQP0-i-VYFaVnnYfencGTqrZrqlY0yZWN2217XSo9MhRlnkcYW5GU1W-JYc-kUmTw2MykLS87TQKxhUYxOLKYlQ4-c82RqdWBnh0bSwcnfCsRATSzATMmnq-vdUxlR1O_NXG8aBZ98deYrVheONOsj5JfbbLtx3TTk_qum2vF9KZlhlxp_KmPZ0LzUhbjLTFSFuMtMVIW4y0xUhbjLTFSFuMtMVIW4y0xUhbjLTFSFuMtMX33f4TI3CVFUhUIf292lyH8aFbdKF08vV2ebzWVSVpHXv5SHlrU2RxXpfZ0wzGyV4jqsYQeKjTZdAjYMQ6up8ouxDjQC-_-_y_PLdGdK_ksvQLUaW1eJpBDgIWbjhpJFgxDPjezI8WslY1EHL-RPv6UgXSKFV1_s7rPXa3gop0FIMiRWdCSYcq_kWS9kNrrv8ISjJILgxL__vrb_-kJm_CimsJdLNG81kco_Oza6eforP9otyxIuKfpacwraCndAgAoA1lfKcmpj7IZjx1fE--fWSJkyL3k4y09acYjspiJB8oWh7b5ZI06Ha7GqZi6ghPR7R5dQucVDwh2NN_WCeaSqsaDfzvYTzZYjOn7oI8WiSvZ4d48DngTk63wxM8Ds7jMNUTSDGS_FlEkKQTYdmSA7HU2eRpZ04UaZ5aM3AceMhhmSeGACph35jNv1R4QSYZtdePDexLI_AXQS5hFcRSCtwuVE_PE08Mg_Km0RLcdma5LZfrQxGD9Apy7K9QV9zfgn3gpX0yewV6YykXlswwAIF7SsGhnmP0nGItSH_bgKLgLdUZs0kXp-CZ9rv_dCHWisrf3tw7Q7DJAbp4oQ9KLnf8cXq39pGK9gCS9nv_g_ZD9P3SNhqfFZwnfb37yELMDnHEU2epZy3Loyxq_Fg5vO4cBDMVawynbTMtdpq36ZhKFZ_qVKNNuzoAs_RaIk_bSMsRQHHRac8HWQNFQwbz7DN0BsOxec3uMZ8qK8NlBjpgBKN0s0d1UZdN-dE90hTVGnwYzFKZlTESkB_JIkr9skjKpo5i_xDMkoVE-GVgllibZm2atWnWpv8JtOnz8fB2MW9SF_Im_mkc0eajAPpUcRSDgEnzNM39LGjCsKlBzsRJGsrAl35TpLIMgrQp8yZpKuRUTZiEQVTAx5Ki8Ccnt4fnk18k4UVcjOD5lHUWRGWTMJ4P4_kwns_HxvOJghDOfp7naVwwng_j-TCez8fD86GttMxraB5X4g6Mw18F5M9XS0tvQ21_MpZO7hYPb1CxMla6WQNyrEw0xSjnoMkbJnt76mbtvNBg8RRb7zONbUWSSeVw9uJWot07rzrabdpp75DjThvuijIZbIjBhhhsiMGGGGyIwYYYbIjBhhhsiMGGGGyIwYYYbIjBhhhsiMGGGGyIwYYYbIjBhp4abCjNRSXyomryylaTOCk1lv0-KC1G91HmJSh4SRUWsQWfcDJl3KDfA7NdSF_DdYc3ULPSHNf5mTjrthvKQpxSr_zT0k6UQ6_a5TXdXu0sbuFIzfKwhtq4pnfQhlywIIUOhCTpKqQmJrfv5ZaIP9Q_Gfi0Ur5i-jOTxWd-TtxfsUxFJZPOUQ6pZEdoNtMPURWL8WqbIUwdPRhl7C35xXH8qitq2NoDFphkUP5K6veo-3vuGqaOD9OJipAatTCJbqeMzTwO66hJwyTPrIx3Mp7GQIs-MGtpjK86KUMELdGei2B0BpAR4QEVJDBQhGjJQXgbjiwJfSVdDkEX9U_0rVhpEMVKi_YiUKej3x0EK3rvbtHZH5QBAMQVPg8d0lSUc0zipMA4auGXoqpsBoSTF2YKxB-R2zUeJiRFJ01nafY7F4Fo4jryDSSNGyVA-A4QHnRC-xzmJMc1xec9_Gu6akHTJ5fSizG66RmSGUFf89r7yzAXS4X-jG9mMNsSDCWsbevFg6hrkCVSJ3I7kRY3qbmTC_T6QWvwodWFzNcmv0SVq3pf7I_ZjAvNEDRJlhs4OSXGEF1B6pwqsVFeOnsHLcnli_4MNOKOVFlX3qmoHRK3-XWw_JTPiw4xekfLdRsB1GG8eTfAPkEVYQT8CcMymA4ErZYYqe-TPNZGNBwDWwpSUIrCKghieRTA79yUug-D86sqP4t8EftZJh4D50d5bO22wwSHPWS_HtLPZKE4yH4GuQ8ELtESLiepOD3kE01Ye5uAp9-A_LAAeS403oci4P2xfYt61USltuiUO0ueFHOkyBZI9d10eqVoXt2KN_JyKd9e1m11Rd1f4dOX8h3B3FzT92T8wPlabm9LBKBA89mtGXCsUr2Lk91osO6dVBTnsucT4o0x-X67mHwiqKoiz_1QxtHPj8mnwg7AaMcKOB6Exac8RQTG1KEHdLQ4xQBHOcUpni4sErpcvF0gNI58OzXP6pw5OGX2K8VacCWPuY7TpkzSPJFR6VvrxUkpdqyXh2QFG_OlyIMqSBHMxJovTqKww08fmusrL-fLS70yV9oCGfIhtULtUo4xI1D6d4pnFmoUrcZ6Q_WelBKcpLI98RMBmGm9vLetNR8f8oiJTT6j_JzPvv30v3QsgJob7BomIrYrp3pPAWJ4r797afzzOAf0YCkznDiPmzNC5tnmuUJyeK4qSTyQEdWbzli95HMeN6QWlC5pcm6MiHDyIb7Fs0A4rLt1Qa7keaGh2Q6gstKBCqkVgqw7IpNGct30YTkzOjee2qclypJiMFqTPSU-GAeScSAZB5JxIBkHknEgGQeScSAZB5JxIBkHknEgGQeScSAZB5JxIBkH8reOA3kIAfIQ9uNB1EfGe3wihJooDNOgSJ8IyeSvz5__cOH9i_e_2vLiLgjV8s8rywr_7QjahqyaOEizZmckoWcacbUFUF5uV5vTYDkn3j6CtpFVcemnfvxEwzm0MuTjAYr7t78tv3djzkuSG3R9V-cdW7UgCaJMNj_zMMnG6PQgNQuxY70VcBLeeW-PDDNOQEuo0-hnHqZiWnqYylLU2VC3ZBPs7PveMKOiCqJIlD_zMHvHFi7pF-RvpkpY5wfv6RALe4gzmz61P509xEIHgYy8-uNQfg7_GIc9-8qUfRjAwmOLOQ6t5nCGM6DVzBzhWOksCZwJWivKwQe6bavSpteEK3Hg0J8D4jZ-DsgLS9KXHPtGCxwGc-D3qr3dRSR0TvMZ_WehAkIckretMsN5Tks0Bzc94BreOnjoZI53adDlah0Y2SNUcqgOigD1gHS858ABOzFBx_mrj-LE-u6UobKTqasSBHTEQIEEdAcA81QnYyfCtXhd-pxjxI4cvioVmKAxNQreYGO7iV3_YRGEe5T0Rli8SrV0VMPmuLytvv9hEHl-VuVRGAVVHiRwOoswy0RZFfEhiDyLMvTLQOSxAsIKCCsgvxEF5Hw0zqM4aMFP4zBnHwXkLa7KIEmiukijUsRpnKYiq7O6TJMia-o4qhM_jH0BZC3jpCzrJiuCqsmzKvTTJqnlOZPbBXkLwws_uwjyMZC3vAnLMo4Y5I1B3hjk7WODvAVJlohEZkGWVQzyxiBvDPLGIG__3CBvX8ud6pfqpm07XR-z71RxinhMfoN1wLQtllB5XxnbGdNWDS68snj1gb6Ri9rNJzHLqXf1lDPFohwd8ojojM451c66HIuY1FuE28Bs5L5_2C_57kZsMeLQpyFPqXSc3EfKraKKQrRlb90vfZxOh94cpdoUWmhWXg_qBhllj1H2GGWPUfYYZY9R9hhlj1H2GGWPUfYYZY9R9hhlj1H2GGWPUfYYZY9R9hhlj1H2GGWPUfYYZY9R9hhlj1H2GGXvV4myl4iqCeMmC_3KKkpOpqsm24dkq5oQSBlUIg1SkWQ2HuAksA6E9ofnoBp1L67ALCtlWcb28DlpqSdmcVZmqfC6W-TsRh5ZSnOHCluEaQsYuF-2twr1T8ViQf4Pws0XtrR5OhqwdqJw6ExQFQFAJ_YpxOWD7QZKpNBv64kF1pXeO4e5k-YggKz9sq8rUORlo76mChfGegW0dWlmduV4DPtYn3IkEg0uDaCirdK21Iy1gejKRjsNwxBopGOgj2Sxqmsg-AHlxte_kjZjBkc6BjzzQpkkQy-oyUNDxaaSvZdXw5Nh-8BRzCl0tCgT-15IgZuq1Fp63paTwFK6x_2YrziO6sAXMkuK3nHVZxmfoLqzEoWBt4-I2h2ZOQZNgfs0BKCaaLgyVKNUWcAuntRBJAcLpmdT4gzPVpkKGHBetMtrmz-j2xMIg0acCtSq15SQpX8ipCcscddeophckpooXG2VJqum8zXBVNGkrJWm3_vj999_N3Qd2JKFIxhmFs_KTsu8JLBy2FTTIlABeo9mfdbokBrJQesk9gShNgiU1jBQvrVmPFObpn0gOy-ggaYzQZASrddIVTfplUeOQurDMP_DZTKwJ-2qnxN5y6FX9OfRtMWia_fnDosIp2JjyoVNCQjoAdCh9rXR_DHqciqakqWhKIvEL1JrsTkJ7idOyFk56mMeL08ZWYrbjJlHtvIIFrHHGLIm-wXip8KOwL99eToh2JEBVE_UUQmSiPYN_udCqlRivb4fAJ8MwBXIsQDcftmR1b3j8FLBejQeKHEEBrlA7JWDiUF6MZA0LvBsX5GbbhpdOUlf2pTExehliU5PIdq1RctYdt1u15ubnkdj7p7KqUAWbfIkEXBh413hU5cqxejS0uGVYwiq06XNLCWfYJBBoOndFDPhfr0gtoYv9M_pczHz_qCpXvsh1KQpg0q9YIAMQcrKnQ4nymhDgQkGmhObvqMoyjl2WlOLKM5FXJeptdOcAogTZHxWDUO3vUagBRVwM8viqBYmgu06jHaCb5ghqTy5JANH9PX9-L-rRzqOpj7tbea91IOxPSu7o_aKSVbExhm3x-SCYBL6AX1PHBzVlm2H7se4dz_ir0M12KaqaO-XrpXTb_fPquN49Uk6i_zV6mq__6tPslmemJ9gCC-UX24_hrEL0PqfBwv2qMupP8sSDWk8DWZ5emUWf6U4D_rTuxXaJnAS723Qos-2q2VXreeltPwVD57mZsriQD0SARFwi0rpWWBKFcLeVhXwBFiLnfpFhtJmKG2G0mYobYbSZihthtJmKG2G0mYobYbSZihthtJmKG2G0mYobYbSZihthtJmKG2G0mYobYbSZihthtJmKG2G0v51Q2k_ClxxH9byaVERz2j_UXCGZ7T_KBzCc9ofQ_3sW1Cn95HQnuOAyfuAxX1nFoOWvsC0HLEwjuu1aNAJW91QGtn6DWorFK8FbRKMK4ztUhf6GUoIAhvZClANn-YpaqwPItMS26Kk3qN9K77p5OXjK_1QHKPIHVVnw6y74_owjNk4l1VYh6ksmsavQjA5olhIKh8Zx5g1IIenMWb5ZP5TnMzzQYst2GYPsRlP7Dh2sUQtmuZHwRKVWVoWQeL7fgF7EhQVAhyEZRVHdZoXSQ0KdxEWEnSZKqqbEL7PS7_2AzDU0zysyvOmN4YmWlwExQiaqMhyWL9AMJooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMprorwFN9KOAfcZ-ImQWCBH0cEL7YJ-M5MlInmcjeYIhXMZ5nPtJkx5G8mSgTgbq_B8K1Fnm6IoOwkj0PHUfqJNxOBmH85fE4QyDVCZx45d1IA7jcDLCJiNsMsImI2wywiYjbDLCJiNsMsImI2wywiYjbDLCJiNsMsImI2wywiYjbDLCJiNsMsImI2wywiYjbDLCJiNsMsImI2wywiYjbDKO38fB8RuHvHS2Yv99jXn56UKslZVNkQ6rEu1DtOgcOeS7RvOywl6l7s0ObdS5vSt2MHQoHwZsoaF0EldgoyKxOyNwtvLgCF6vQDT1I6BUIl3rplNGtFlNiUOa7Vz3KYMErnRogw_2-rUopUlzavr8Ckd6OrmHQn1q11g9e-8mYRwAE1Wreq_drWh96Q2bqvQXfT_7ZFDhMFxaGsREp8uZoD15zFUxjBmC2n1Eftl2Oso-NBdgaogBALTUNw6zoTRMGJNNydQopxiYW25XGi21-zB0UunHuZ8lAcINlkGUx5Vs4prQFkfRSS1oIqOT_lq52vn4s2N4mj-NQ2R-FIjQsM7jNGiqPE_Loi6LNCrTGEbrl0EYZVHYZHWVpTIL_SLPk1TGQRnFDSikflOlDaUmHJjSCCxo4F9EY7CgfpXkMgBdk2FBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFB_1lgQdMiAr0ryqu4SX5RWNDJbpoxI4T-9hFCyyLBcs3El0XECKGMEPowhFCb_P8bhgqtc9AowehNkrhgqNBfEVToTpEHA4aiNyZpAl_6UikaBwBDP3eKVRoGD2XwUAYPZfBQBg9l8FAGD2XwUAYPZfBQBg9l8FAGD2XwUAYPZfBQBg9l8FAGD2XwUAYPZfBQBg9l8FAGD2XwUAYPZfBQBg_9ZwQPddCRehi5MdClg8hxvXZroemEL7OylLvQdKA0G1hEAkk0Fb7WzaP7IFQGhIdT6kWfWXeygZGjbQYFlmvVlITW9kSDUi9bOCFKj4EtOAAuolG8NE84AuxXN6B0lFX4dAMdTzg3SUJYrwBWElVioqd2CMpyDEExjtBDkD7dQJ0oHjFKpyzolan_-QadX31kzwbTjxFkkYN-J6ry6Ub6xSAtbCSfwgJtOCkFIKuvPglm50HJOgfzIKjpdwZ2RgmLg_MZGZ-BJNWx9kExjuLMJh9uduhs7yyOHtPLuj49IFO3q7Q37WmbHTqv4x290myd-kLp5BTq6rmZ7DHUsdo-ZQL7hXdVDkA4O3T6TnSrjs0-dK7GD9KOPgkqPwyK4kwKG2UvPHPoUJ0x7bGgpjoy0wUKY0_nxE3MidGBR6zCMjXHs0NH5UT_KyeEjqhz-3kvtlfMSJ-3wxw4FRaCfVhJq60cQNdVXY7UyB6hsJ6-dZeD1I99aKrxUlSTUqgPhIY4EyQa-42d9JuJeHAVSGoQCRtdz6WmuJhjbvEHouuGWS1SAXZp1YiklCkGs2TcHELXtdijp9F1Weyz2Gex_0uL_fPRtC0wsRrTRTJxIIqDn8YRiD8K6rLMkkwifHJZhGmawH-BLIUoRRUGQY41e2kd-FndpL4Mhd_U6JnNm0QEZRIX_lmTG-AvR_73fnCRJBd-NIK_LDJRx1WaMf4y4y8z_vLHxl_2I-A8VejLIk4Yf5nxlxl_mfGXGX_5afGXzX73LhZ7Cq3R-76valXwiOO1rQfqfVW-gca-o6LVTt9qYyOvRtq4xba6pLctNyYfERiZqDFdTBjAM0reNDPSZV-mXHhv-8kppUkRHTyHLiWiZDJdlxilA8ho13A_miKrIGPU0jqQMONOM5Xf0leUqywNICOJGXv9IWfsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-_rViP4NiIUSYxH5d2vQEpxJsqB4_pJLLJgoVTdBI2YTCashOcdeguudhxVm63gG1ASRlVTan-bbhrKW8EXegZlyAxiaXO1aP4mqdhTugnlR9rWZTRoap7ic9h1PFIuqE6nZc3M8j-ZfVdr2muKm165xT7FiI-yqymzGAYcwho99LKjV4zoNiWl1KK5Fj4tqryCyNtc94xVU3ODI9Foy2I6SNwiPoJaYJK9rV_rt2fTZoTBVVVZoEfpD2qWROVZ2mkMdUxVlNaxiY1sXEjgByHHpGpRrDXVXBZqU7xvvi-8VOErRti95LKEyUpGrNSSHotHhF8PKu19fQobCQhB3Tg3DozFjUoTChz-tuBAKSWlV80Yp65n2Oi-O-4ag_9nAN9SDHJeqqQH18K6KBRzvxrT7DfEdDsYuKga2MZHgWHFoseobaz1LEvVUOBhO985TrQFAI6MoQ6CUJ7Euy0OpLly9dvSA9Wp1mV2s41MiVVVpVa57b2hHSFUHU-CIuGzDUrIHW11nuuzk_uE6yF-NakmA4TQdqTGSm_-XlbtDG_vRgN6jizCPax3svKmYFOS6zSZj1ATTyNPr7_x80O-aq9aJ85ptQnqMRYAtZgi0FszjI6HMURTstYgY1jLAUncox692oFF3Lk9EBwmkcDBDJ7siU42iWFgplfRJlhdtklBf0fzPCIM36Jsenm5rx7UwXNYiA0i8K0xhoVbax_ZnG4SyNj880MTMN8-PpmkFal0GVBrG0oSinINdgKT2ioLYg5UynOR5IvgBGcPXXaTrLCoVa78_CCDMwdFGfaVyvhNMv9ZHOksz2Qe0EkWqnmOUxtvMCJOec2IMSkzqsTu2h8q2ryVROlUq6MocTn4uSWQbrDaN0pocji4AOQvphb2gz7wuj937IemWzKHXm8olPVw_gXGLYc7Umuu5q09H6-vS8SnehEN3-KiG7hXWBZc30tQDhLCpUisvuXNNgFoZjc02CWRocmmtviu-X6YxMn5TY3sK24lun7mo3RQ_9Tl4Tx7E8waRLuuMDhd2LQRR43KPcq39i-QbFG3LnvUsv9lM5-U4VvlOF71ThO1X4ThW-U4XvVOE7VfhOFb5The9U4TtV-E4VvlOF71ThO1X4ThW-U4XvVOE7VfhOFb5The9U4TtV-E4VvlPlF79TpV0BR5g_v15tUFWdgsj7H3DBCowJ9rG7xDS57ue4Y-Wx0N774OtPDsp9Dr77Y-G0D01j_P6L_YsY9u-_eFnXA7Np4IedGKE-GVy8MCWEPFO9ceryhdN9DpKjet5_6laF8Ya1MwrbVbGOeYdFwypXQacXdyDhdHhlhaxNX53xQRcnuBPoHKPt0G0Wh-5H0InMw0IUPcKb-1WrkxWxTAvEn0Up3nes25zED7ogIfCbKgKtJhBJgKkmkV8kcexnhy5IsODgpy9I4DN76syef1mFxXfvUd2jn8ZB2z8KZH3moxMs9evCj4Ssk1AGWZKHWQm2bZCkIpVJkeVg2opERqH04zBp0jxo0qrIREqFIgemtAdUn1wExUWUjgDVJ1Ga1nlQMlA9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUP2vCqjeD-JEprIKgrw5DVTvKHRu2d5vHbb-ha1yHH2KfINJxuD2B8Dt1fLhN0GmlK0s-g0B3ssqzeIw8HM_qhjwngHvfyuA99SSw4WPbXI2SxWMcASDjI_tchAV-02PzjwsZmk0vtE0vjHSGRR77-91NvNPrMCg5WOR2joKY-nncVE3DPnPkP8PhPzHub5GO-1D5goMMHT3Laa5KFBtNI5wrqgsH99_MjyuYKHSQWOFJQKflvTRRJACWQWjC5PO_OLQwsCi_L6zq6LUWWytlKjqIYPDJixfN3cbkGpj_RQu3APZ37u5Az0kGME46NwDA2WD2Vf1vc0wx45FCdMkSEolk0046-e4vGEHZZqvb-DrG_j6Br6-ga9v4Osb-PoGvr6Br2_g6xv4-ga-voGvb-DrG_j6Br6-ga9v4Osb-PoGvr6Br2_g6xv4-ga-voGvb-DrG37r1zf88NP_B1uq_ok)
