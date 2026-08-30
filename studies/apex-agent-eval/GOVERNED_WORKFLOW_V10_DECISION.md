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

[//]: # (ob:7d91bb6a)
### v13 ask-specific retrospective regrade

[//]: # (ob:b58b50d2)
The v12.1 artifacts were subsequently regraded without rerunning any executor. The corrected evaluation unit is one frozen lawyer follow-up ask, not the parent APEX task. The v13 rubric therefore excludes the parent task gold response and task rubric and scores only directness, expected governed-claim coverage where applicable, relation reasoning where applicable, gap handling where applicable, citation traceability, authority boundaries, and lawyer actionability. Each frozen artifact received three new blind grades from the same fixed Gemini 3.1 Pro route. The regrade produced 108 of 108 scored cells, 324 valid grades, and zero inconclusive cells. Including structurally invalid attempts that were rejected and retried, DeepSeek had 118 of 118 terminal receipts, GLM 114 of 114, and Sol 113 of 113; every receipt carried cost telemetry.

[//]: # (ob:8526de12)
| Executor and condition | Ask-specific rubric | Unsupported claims per ask | Citation errors per ask | Authority errors per ask |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek v12.1 agentic disclosure | 68.50% | 1.472 | 1.194 | 0.694 |
| DeepSeek full-graph control | 67.27% | 1.972 | 2.222 | 0.778 |
| DeepSeek static baseline | 67.78% | 2.750 | 5.361 | 1.556 |
| GLM v12.1 agentic disclosure | 76.41% | 1.222 | 1.167 | 0.639 |
| GLM full-graph control | 74.31% | 1.417 | 1.833 | 0.583 |
| GLM static baseline | 78.40% | 1.583 | 4.500 | 0.750 |
| GPT-5.6 Sol v12.1 agentic disclosure | 80.93% | 0.889 | 0.944 | 0.361 |
| GPT-5.6 Sol full-graph control | 85.97% | 0.444 | 1.417 | 0.111 |
| GPT-5.6 Sol static baseline | 89.03% | 0.528 | 1.556 | 0.250 |

[//]: # (ob:4a8d270e)
The corrected absolute scores show that the earlier low rubric percentages were largely an evaluation-unit mismatch: narrow follow-up answers had been graded against the complete parent-task rubric. They do not establish an agentic quality promotion. DeepSeek's agentic delta over static was `+0.72pp`, GLM's was `-1.99pp`, and Sol's was `-8.10pp`; every paired interval crossed zero. Sol had the highest ask-specific absolute scores in all three conditions, but its static condition was strongest. The regrade is retrospective: it corrects grading of frozen answers but does not remove the original executor instruction to produce a complete legal work product.

[//]: # (ob:9ec3159f)
The follow-up panel and native APEX Legal E2E are now separate runner contracts. Follow-up evaluation uses 12 asks derived from two task graphs and the ask-specific rubric above. Native E2E uses the 12 original APEX tasks, their original rubrics, and their typed outputs: six console messages, five new DOCX artifacts, and one edited DOCX artifact. Native reports use a separate schema and denominator, inject no lawyer follow-up asks, require all three output types, and fail closed on any incomplete output-type cell. No new paid native formal panel is reported here.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZhZDMzM2RlNDQzZjM5MGM5MjBhNzNkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjcyNzdiNGMzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iNzE1ODhlNjYzZjcwNDljNjQxODQyNGUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY3MjYzNmJlZWNhMTNjMzE1ZWU3Y2ExNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfemSG0eS5qukcWZsdkwAmPdR_MXW1ZqVWhpS0z1m3bKqyMzIKjRRSAwSYLFa1N99gH3EfZJ19zgyEkgcrCpR0sitzdQsABkZh4ff_vmPz8R6M29Etbmc188unq1Wl6mooyiqZRxHTVT4VRH6Iovq-NnkWdnW95f1_Fp2G_htdyPCJL1IkywrZJjESZPWaZnnqQgbEQVRLYoqDKMiC2UkS1FGkchlIZskq-MyrJKqqYLUL2Dcet5V7Vu5vn928SP-sbnciGt4w0Js8FUT-EcpF_DBn-V63sxFuZDeWr6dd_N26d3A79v1vVfee9-t27ZZrWXXwTMrUb0R1xIXNfh43f5dwnK3axzwZrNZdRfPn1_PNzfbcla1t8-rG7m8nS-vN2J5nUf-88HTa_nf2zn8-3LbyfVl1S47uYS92Ky38qfJsxspcBOzMMvKuIqeqU8u5Vv6EWyuvCyzIMlzmaZRk_lxUaVxkMdhLHFm7XqDS7tczJcSZm5OZHGZZmEapaWUlQiiKgoSKTP4Z6qWo2d3WYlVt13AgkOcZ9Wu6-7ZxV9_fKZf_-MzOOV23eG_1Neyvixhy__6bLt8s2zvls9-gDUYesAD3mzrueyei5V8N4UJLTdT-VYsnn_57Z8_f_Wnzz-7_Mu3r_73F19_-5fLPwf-5Weff_rV66--_dPstn42-SCyEpvNel5uN3Cal6Xo5h2-Wy6aS9HBLm8kjbfd3LRrnPub-RKH7O67jbyFb5biFg_ZrGECj3ZIGM8ultvFAlZU3cBJSrUX5aKt3sCvgzQvqyjEI4JD3Mh3uN4vkQaXsvb-0q7fNIv2znsb-BdAVfO3QIje1_JaLLzP3wp4SE9C1DXNboXUKO_gk3_yzh1lsRW4Yu8zWREhwzCb-xUuBYkGCPDZT5N-wiJO66YMy8GEzaNe2W6XtYD7c2xm_-SN_f7YO_0qj9JcPPyd38Pl9G7lbetpgvSEt1IbMfE6uOSynni3bS0XU1H_Haitgm9qD6ls289tJdZiMLGqKZMsavzBxODy19tq49V6gt2JzRj7_ZHNKMsk8sNCPvyd7-0r_3sLbA338H1_JO-BJua1XFZySjsLOyY6_Pxvy_fedNpPjnjEcDuKKspllg6m9ulCzG-nyKGAOVX0NuAS28XmxLYce-7I9vh5lmVhXD5-Dt_fSG8lgMnWXhBON6J7492Kv7fr-ebes0SCQ61oN-FnG3iiaRdw1Y7QTFpEWSZE_fgJvve-kcCwKjiy715Fqfc2g3_BHZ8F5rCmHv33wv4ffvxKiY5jByni0m9kFTzNJm6X3XaFQkXW0zWyHgFUddMugfam12LlzW9hB9_KW-DrcC_XEi6qWOK5Hrl4deqDdAsfP8Gpdwu_mE_hKoDsfvXqC-8ORDCwh4VYX8u110k1Uic33nxZ4WWAk1628056_QQXIPsHE4wqWWSxfCIybECA0BlPu8096ByGHjUPDz8HQl3KhXcnOiTCtWxa2MZle2QHZV35aRKFu2zkGkX4_K2coi60aLstDHRnBMhZF_fsQY7c4sTPgyhoqieeHe3luv2HXOoNw8HFfElXHE787l6u9RbD9gIxVuu267zrtVjdHNnLMg7LSNRPPdv33qdqNJxmPbeMWq5eS_nGW29Ldfm_ht3r_1LPHLvdoCIHgcjqJ57ul7hL03a5uPf0sD1n_IdctwM-UOFVmHjVfEM89MjmNnkRxSIqhrMFif3VspbvziTJ_Z8fIb44S-q08pMHv_HbpQf8S3obIiLiJ5rqgN11E1ArtIBFpkIGBwzuiY3XzN8e24nAr2pRP3xe7m9vgexRC6rn4nrZghZQgVATq41cz7yvgA9v2tW0Bj3Wq9tqC6z5yLzqqgGZu7Nfn8lGwHSUUuWt24XsTiqFY08cOac0zpNclM1j3ttzhAloQ2IBVh2Qaw2myqJdoUSCIbYbaTbs4tg2FFLKso4eM533vbKOv4Xr_Ipe_977g9Zyd0S7-S8J9uMi3YfNkvFjZvcSpJD6aSUWi84D2xNI9h1sGApwoOk1ih_YsOsb0oV6M9irj21c7Psp2GA7_EiCzfUWxhbr6ma-ATG8JaXluOg58NAx4yILgzqtg0e-nbRFrVa7z9irVrf4_9Ol3G7WILThts_hmoExIo8TVS2bME8eOburqyt89m_Lrt2uK4mvXW27vy3_3__5v5Ybed22BMUEFDT1uXYxkFqmPunnWQEVDEWgEJHMs-IJdlEpNbCXzXyBk1qtFmD8e3A1ZXVfwUdom12DHi6BlS7oxyRNjnHOumlyPxgK6D9pydorY_LdSq7nuOATdHbi0WPmCSxCJmH8JDP5YksUNngSBbbX3bTbBdgjqMJu3ANumnk1h3_fe7u79cPE-GeegTxCS_ASlV3l9KBvjAdFXhZVkdV-LMoql1VRFmGW11GY4hVathsaU7uQPO1C8qobWb1ZtXNaELyR3oR-EfMXukV-QN_TYl7dOyO4_ihnEPJ0PdBV1bXN5rKBk5Hr1XquPWJdGVxkQpZxU5R1UGZVkJdBXtR5XFaNXwZpHhZlnBehqBJZ16FfREUT-XGep_BMlkVxisp-B_oMebbUaV2E-U-w0ehICv0wnfr5NCy-D-ILP7iI4098_8JH54HecTzkMClFKDMgmv7TH38JZxhRrHJW3YjuRhldcV75QdwQP6IxHP-VJuandjzpl5PbSQRNUJJZSi93fFHm5Wf7lvSwvg9nW-aZhLXbYXt3kx72Me4jWuPMQ86m_4ZvyKJQxu6yXU6VU5F04bckUvFedzPvU7CU5zVuGnE44HcV_ApUNdhgeMkGPujmC_jDg8MS6FQF5fKdrLbwTw8Uh9UWf4Lmdj8Vr0OZY9690VYPKH-3c3JXdh48eys2G_xQz-t-BkZGJZdo-irRoVT85Qa1plbp8PAmYNq3K3zlZi0lzVYC59nMxUJPQ28aWF8bvXz5rlps4aqgFnYLWsMcP1ZUOhvh6IYUGxmVgcwSSaRHx-Y443pqONO5pocVws-TIEmDIKrNsI6_TQ_7KP_ZmN4mVwsB7Nk4ceisd7g62hDateN91tLB4Wa3pBuqL-DMQGaAYnYPr1Rml2NxebijWyMrOzoN7XgxzhhtnZTbjXfgsd5YaSTqgvaNir5BMq3l9byDT4lQnAVc46l3YFSsjJ8MXRoH_BgztS_fiDekUxm71HPsUhyi1tqrYoIwUbSDFeVOjQX68ruvPDovvVU4zTCeVqLD5-GXt_PlnKyfTjRyc6_9Aiv0-IPaskBVt5PaiCMrlvgifLeQAsM6E7wkoNopA0rfoQneoe1SX59_wK9vtxuHEcC6cdnWuDbOiNvVQirGgc6oCvcYz-l637LWnh7Y0nWLQYWNhxEqw1nw_okNqg96K1_fzFf0-xWYeq59D-uc384Xoj8kd7deAbe7hWFq9b2oqu1aVPcTr17fT9fbJVAQLqycL4BHTDzgMfMa1cjb-QbZouaOCznFuwZU-XflTIPnt6DUIZN0PySSrOXtCl6OKgruvj4IddzucWlCeY0voz2HN83xuEhpASaGuwUErqjYqkB0LkBP7QLpvjL8Vd2HJe57f4ouGfams0t56L1cow-WHhy5mf1jOD4-ejOHC4TacEVK7rzFF9bkUtx1BcBscdjrRVvCb__wTZhMSP68pesFv1ffTPEbD-eMLPdG0Ffb5RyYEzJreMJRAfXIKCYqKWu9tRjfxB0H402C7rio1WHgWPOlIUsYjMhsASbBZn2vd-ezA1vxZT9r-OurDV5M0N9qPIHBuwcb4hzIfKn4hHKc4CSASYE9ru4KTk-8bec4Sr_JZh202WaiwMLmCyVP349ZyFak5HEtozgDO9mKlD6g0YuUDwxM6OHz2C9j6YsiSTIzvBOrsIrGw2MOyP3oeivB791ScGDUZWF1qiJO_CpOk9wqP054woq7x4QZlA9FosMAvg58f-b7_-L-C3_7n4fklLdWLCksZkVMj0WzINFP_bEPIdgXZP4so_HzcJYX-oevT0kz-nmQ43NxNIvxTUcoBYikjsGiKHLSEbUqaiMmzlE-NPIBwlHJYTjde69WXAWvAKhgOEwDl4i4f-9PNUsBvg6E_pnjwILpK_0M5GdNI81JKWvuSYtFVqUTGZDyjpFLUSaybMoS7B97Q_pAjF73YwIqgtQlRdglmHR4u3vKMGt88bflFMbD2zG9g7UoJqPl9wLYg12o5pbDJzVHATKuJbGVTrnWVwtQa3HpStIu2_UtyLN_aNGn2bd13TbzNXDD1Xwl0fTUwmeBHNLxm9BjBxZAfBejC3NSpkG7Jt8LLFxFb1AwbBShWgGrhAt8sJ6jdFtq5n2v9C0yDWYjQSl9flETJ0FYBHlVVeb8nDiVQ7cPjTfB4rek4sxpWWJHI9RHhGqgWgsJWmBbwPEF0h_6i5a4BwIfJkPliBGQi6hOmqhpwtqyVCesNTACHhyRMpZBXskkqiuZ57F5lxOkcvfugfGlqRbsKOPVhZ3WEi58TVbWCo0ikPXANZRsXsKvF44rDL32wC2XwBu26z5gpDXXzV1rDUNlp8Elw50PUq9t8L-02TXpnEoZImUXpf8SDDTcOnjF56SX9i5g0hDgJpJeBpQB903OV6B0fg88xfqK8VIgpVz9czAroji9eqGUqD7y0EtwGpWeuPpnFBBheHWEAqI6y5vGL8qstE4BJxhnBdjD42gbD24vcBBlyh2Sd47YMyISaBmInTQeo7ODGItnKUmnMJrlAf3Dn4RJ4m3aN8Da1QikX2g9njgRib8oo58nszQlOZhP_DQaPEfxN8XFrgfKFzwURPRQMsvVMNGkKPJDTw80spt72I_anftglCy1oxyRmEEWNlXh11EVWHPdiUKatKdHBBDVpbD-Ck-u10DpJCjLFi6AJf6Z97Ku6aCVsgpL7KWQeS2OZYWlktGGMIAYGpQMwLA1o1M3Xc-sO2SwanttYKuCcarEPJhLdQs6L75PDwSLtdRKN8vMFpek7MNmLUEOwWSQmVx4xjAwTonOuIFVBMKxIida0Johd34nVlP45voaRzty-eKgLAPpS1AKrDrgBGsd9ntW9FWPWvt5XYOaLCQxcRrVCcjqUR8TYZXEjHJ_lsBNwt0cGFhpPktC9blj88FO9_ults8ZgGJd5sdTZdTR3bPmjPGPwDdTYJXbThltWtVHrY8mRVSu1aWrv_oTz__hCui33WBcBtRFoM41TGDmMkwgWUpa7C_JUctPH70hFnoEJMDmZg7XCvdvz6aceX8R61utz62KRG0f6Msp6nJAo9q312GUQEcGF4J8JDsW42FaChM_DMKq9MvcMggn3D0S6_7Q-PXmuVE8MaCLt488jTYsRX4zTPkFbrBRzkhgHJv2drpdaQUTLjosEp8xyrm9_YZZ1PKW7EJU0omt4JtVNIschuiFParSlIHwyyySYVmafXDC666X-8xgubmsIcjIsAjjJrHXyomf7-kvD46G2wOt4jos60iK1C6kD5BbyfyYcLejZw81-ffef9wBKYKM9cLsDxMQaNc32g2LB__e8au7QU6Sti_Qe6J4_cS7JlcI3GbtZZ8v0bCmt1snrwAaAfECZ17tahZ_jr0vFrAfQC7o_IBR_iGVfgbPv4Pfeyocqx3FOJJ2XA1fsWmVuEMygkWKxdhLPDSjxzxb_YBfa0vB8gQdTQDp_933U1AtvNctjv1nFV3wUIVZ4w-Vtm4dY46cVToPmST3vUJtYxDj8_wUtd6pIt2VflYZ6qBIwIzekgTvxyDFLJr5eoAv5suRM3WfVXLGWfmfVGTFRBZQFtbKTSXRowiDB2glIOGh2Tnwo5jfHtFv4iLLkwI0HJnXvUfAJlxoan9M-oRzBV9-5X0JB3sn7rXgg8FK4Lcoisp5DSc7877RhpXVzOm9E_uiiX1qAtMgN3a73mHXlsm6RsAR3hU0WZ3DToRpYZVxJ7XDNcfOz9Iw7KRMw6apfVlHjd3gPnHD9Z49XQ6GcQxWRRFldVlmTdyzMpuWod_9NBkWjrQGXqA-G_q9XYeA-n7Mn62jPGZQFXb0nnsqvO79fVtf459OgOJmCzqtp1IL1GN43TfktugNEvUNfaCYliLeEYVX_XKgS_YalJ6XueHd_RLovZub-b7D4ADoxMeCFX9bwo6PJKToQwOTMA8KsM6DvLcM-xwVh2Aemm4Cuue7dtnegjYN16OBGW-e64g9yI-F1FrRbnhVH8EMxJdRv7XVrMxuFUMZ0oEOTMAJoEupj8le6b2RV5bCgSPWUyXHrux2SRCaKirT_9Bs8sQhgkG0BnYErw9-aoMyG7Wm7ZIchptW0QhoYbQjR3iDn8iibGJfgPlv9bs-KafnDR-eWWNuqYzjIijqClQO61_vk230Gx6TMYMrd29fb1fc3czJf4quHuK6QFZvA9_4u65xw8k_o9-iXJMLoYJJdPOmPYGYvAV0BN2i5TmIzmIAq3PjUfOllaH7gWOwdpf3QD53WnG73XYbrdndeyjIjdnkCpgOKGNj3JACJnsDxEdG7wJf37v_QP0FgkFzfO_of_gJz2ak4kuCSWvrvcgavsC7--7ZD1RDRtb--Lc7tWJ735Lda7-mXb0ALe5GrGssofs1FZXJ5dv5ul3ibl9ivLo7UFtGi3hoaVla5n6a-sNqnFdKMyKXxhKdGCcy3cZ-fzS9zQ_yrJIPfyey5FsBsnspp8jMiNOY7A30EaNvpISnu2F4EGl-JKdNycFD-7IzC5289rI2scn17sw9vejZoVWPj_hKk66nalZp_sgoTFShE0tQXYEDPzcJMlZTNdxgppZjNvXHZ3c3mCb3h_nuEP1mUcISMOnN2JbqnVQT6jQLWynNzPAwM5m1uJuOTegDUgbTyG9E5ldhXBVBJmUchH6d59LukZsL6ObBufmBPzKdH6Lz8zM09zIUfxrPPzyVjPkkGZe5EH6IOYRFljagVMN_Ah-MqTgr66jIgzRM6zTJgjqQGfzZhGHkh1Ekk6ZM86qUB9YzlnAZX8TFSMJlWlZ1HmUBJ1xywiUnXHLCJSdccsIlJ1xywiUnXHLCJSdccsIlJ1xywiUnXHLCJSdccsIlJ1xywiUnXHLCJSdccsIlJ1xywiUnXHLCJSdccsIlJ1xywuWvLOEyK4oiTfM4KHx7h5xEmZ43nJn4YoZNKzBBCplIv-6zLG0ujHPKD81tUQ7-qXHCT0ZcrpOBwTx1zISedDFcYMxGly6mjg9KmY_lvff6jy-nYZLqZChtZX4j1m9In6U0BO1X0sK9T7YS13AVr21Aa7Ub_X7hJlFZcdgZ0097FB224OQN4FRBB66UCWHSB-QtuoNlbZ61UGsadp-zcDkL98OycA_l3x7KvD2Yc_srzbY92cLhUWm2H4rHD4ohWXnHwFqjqoQbFA1RIt8GgVYEdJqm0KFQdGqcSG889eyRVMeiCYMUVK-nmQuKhiVyF23t2uiq0VAdgWA8u8bWPALwmYDVG-R1-XSTRKtRxWDcS3mtcqkoRUJfTX0lgUEKsIeOQq6HImzKsnqaSR6IEgfwj-FQYz70o0jBYZ3VUfyEe0nuNu16G4mggqG0ESpg8Uk8K_LV6uoF2QlH9jLw8zCTlB_cT_ILdRT7wTPRYHKdEgiBd33ispw7DNDC8asTVVES5iJ-8knipuLrp0iKKOvoeAYJEmJpgl2C8r4MnS6OgQ3XTZ0Fcf7k80Xvi3Uu2Kw7G6Wh5_tYBGbxEK0QYRwjVT-XYZLH9ZNPmNxZJuWLJmVtJ-0tBkNFrOFz5QN7a7NIqmMcwAcNvC7j8Mnn-w1qI6_hfW-8YBbSzHVs1watcY7GjWGcImB8tNfnVU04Ym5fkO0VTuwT5z7v2NWVgVDb5XWH-QWq9kIHclXmi_nV7JCgPFXLcZSDmSSJ2SHRd6Kug3JDXNfiGylXEz04qYsq7Y5ySkBNXQ_KKEbl2BlvbIaUY8cGrblFLxSSK-rLJrNjN6EJVL0tBvwPCKlTO6opHq4y2dGwv3pCA06ks6Jmh2TMOTt7QGZMbIBmoiSzIRJl8e3nh49vuiNLTi25OXRXR-nH4f9nrDILp5SAisPVsptfL53c8t7x2skNRlO6iXVjqNWiL3F2iJ0fW5d5x7RbwfY1mOye7WbB6liscvPq-J8-fnMEOyfssOYTa0de-69dz0hx5WLR10ZRlAvDZlNKmaAQJLCzWx2Inh3isGds-Q7bVNaZzl7EALLriLUT0h5s7aWuxFKsjQP8QJGWeufZjHFwfcxbwXqEc9gudTL0QUJUrP1WwKV7R-cEa_K2K5wtZWsfqZnAo2yt_8x6vT6ozqsoilxU6PXzyzotkqosfSmD4FCdly2_OV3nxYYWG1psaLGhxYYWG1r_Uwyt86ukd8tcA3_SS7iL4KfxmtaPUsRbV2FZ5mEQhGEdi7T2szoMGiEjXza5jGI_rZKyjJMqyYsqDYowjNNawsKCMI-T5rzV7ZX0ZhdBehGnIyW9cR0Evu-nXNLLJb1c0vuxS3pzGLAGGwBbsXNJ7y9d0nvuvhjht6vTWp9SX6Vqa6HozvY5aKrWd8cwHS-m63172b92g_qdnWiu2l1ye-zvpk0HGDuiNfGVnfIvVbWmNtqu7BbktDGLJkMv3r7_TtAmGpaiDhoHUOl6tUsZcB8wtXEkiY_Lrbncmsutudyay6253JrLrbncmsutudx6LIc3r4IikKEf9cmUTsCi59gPCDqYrO04EmlVNlXQ2KvuxCGcLXtoLGGudJ-dWr4-bx6uyQSfBxKkRHAsbx7o4FZP39wgvVDqJkbXTRK0TdB0rQD4ZkvqQq-5zzc7en9ls0DnQJokbmBMzNK041pC7wscva8-m5hwKOaKq5olWFR3J9du6ZL2JqjiOO1H0Gm_ZFUaJW0y4r3o1YRjJXxVLIXImtCX9uyc8IxL7g8MsWhtXn-K-jAdVK_Ha4-3luhUGzpxQSTDlKrdwyzTlVyO_kNcMw7we_ivrZuxx2Oi2zgHrAbFg7E8E7ZxqSySXmfoDikNVsM4rTGEaRaXIAMy37dlL0406bjGcF5E6GfRH6Js5lPFeT4L8yPqQxLPclQvvDSaRR-gPmSZ0jZI7ciOqw9hk8aBCKIQ9s2qD32oy60ReGC4qoAl7Bfpql9iEe8nAWg7yWr1w5WtGLdW1in_iiq30Dawk_Kx516BBaBEX8uhUrrnwHSvHCwYrVLSh5SEUFVAxEKAdez6ERmLg7E4GIuDsTgYi-PXhsWRx2kcZsgXA2srOqkSPft9dI6DfmEjaxEUIFbzMu6NAZv24PDgh-Yr0MwUvgfWma6Jbw7FpYkATYFLw-aRv56IprvY1f8NC7C5ocpAcVy9PX3Mxir4v_z6Gy-ZReZPHMYFGaDZ42KIxQ-L04FXC3yzKT4nzqzsFNQkSYvcLUSndD68IDBsFqJcgP8qgaCkw0SDhcBGDCSDvnzwWJjng3JzlA-70gHe8M2uYEhAMGQRCIZeEtyJTlsmb4HBHCPERESNCMIsSGrr1nPSS6wUeHheCPx5QOE6IREcwTByvnt4AgGopMoHFswiYrbTcObHqxX8669TFAIrEP-oCfqg2mnGPSSS_TFDre_CmAHJjmkwSws9ZjYLYxoTiCCwY56AsoDfkgCAoTMa8ZNilugRPwlnUUAjBvksTmjIY5IBkyPKuInruup9pjbTRp_dY1Jk1AGrjNoJ_HxJiyDfu7rpVBnbEqsAM9S9ifgNbi8W0mrT16b6esRAtGSaeY7sUn4irU8prJulTuFF0Js7ubCv7nm5WQ9G32iVO85nytC3MgIYPGzkvIOVl2BCY8ou8a6pGkY9gvxTdkoxtA_IbugRrPY93RhUN4Ea9CFiZTodgN7_pRLMqtLTnkPvzsBFNds1FWvaxOqmrbadDpUeucoyjyPMzWiqyrfk0CcyaXJ4TAaSlredRsG4AoNYXFmMCif_2cbo1M4Aj66NhaMTnpWIQJqZgFlTz7e3Oqayw4m_2jgeNOv-2EusNgxv3EnWJ6nPdvm2Y9rpRV237fVCOssyM-5U3rSnc6EZaYuRthhpi5G2GGmLkbYYaYuRthhpi5G2GGmLkbYYaYuRthhpi5G2uN_t7xiBq6xAogrp79XmOowP3aILpZOvt8vjta4qSevYw0fKW5sii_O6zJ5mMk72GlE1hsBDnS6DHgEj1tH9RNmFGAd6-d3n_-W5NaJ7JZelX4gqrcXTTHIQsHDDSSPBimHA92Z-tJC1qoGQ8yc615cqkEapqvN3Xu-xuxVUpKMYFCk6E0o6VPEvkrQfWnP9R1CSQXJhWPrfX3_7J7V4E1ZcS6CbNZrP4hidn107_RQv2y_KHSsi_lneFKYVvCkdAgBoQxmfqYmpD7IZT13fk08f2eKkyP0kI239KaajshjJB4qWx3a5JA263a6GqZg6wtMRbV7dAicVTwj29B_WiabSqkYD_3sYT7bYzKm7II8WyevZIR58DriT89rhDR4H53GY6gmkGEn-LCJI0omwbMmBWOps8rSzJoo0T60ZOA485LDME1MAlbAfzOZfKrwgk4za68cG9qUR-I0gl7AKYikFbheqp-eJJ6ZBedNoCW47s92Wy_WhiEF6BTn2V6gr7h_BPvDSPpm9Ar2xlAtLZhiAwDOl4FDPMXpOsRakv21AUfCW6o7ZpItT8Ez7r_90IdaKyu9u7p0p2OQAXbzQByWXO_44fVr7SEV7AEn7b_-D9kP076VjND4ruE-6vfvIRswOccRTd6lnLcujLGr8Wjm87hwEMxVrDKdtMy12hrfpmEoVn-pUo027OgCz9FoiT9tIyxFAcdFpzwdZA0VDBuvsM3QG07F5ze41nyorw2UGOmAEs3SzR3VRl0350W-kJao9-DCYpTIrYyQgP5JFlPplkZRNHcX-IZglC4nwy8AssTbN2jRr06xN_w606fPx8HYxb1IX8ib-aRzR5qMA-lRxFIOASfM0zf0saMKwqUHOxEkaysCXflOksgyCtCnzJmkq5FRNmIRBVMCfJUXhTy5uD88nv0jCi7gYwfMp6yyIyiZhPB_G82E8n4-N5xMFIdz9PM_TuGA8H8bzYTyfj4fnQ0dpmdfQPK7EWzAOfxWQP18tLb0Ntf3JWDq5Wzy8QcXKWOlmD8ixMtEUo5yDJm-Y7O2pm7XzQoPFU2y9zzS2FUkmlcM5i1uJdu-86ui06aS9Q447bbgrymSwIQYbYrAhBhtisCEGG2KwIQYbYrAhBhtisCEGG2KwIQYbYrAhBhtisCEGG2KwIQYbemqwoTQXlciLqskrW03ipNRY9vugtBj9jjIvQcFLqrCILfiEkynjBv0emO1C-hruOzyBmpXmuM7XxFm33VAW4pJ65Z-2dqIcetUur-n2amfxCEdqloc11MY1vYM25IIFKXQgJElXITUxuX0vt0T8of6XgU875SumPzNZfObrxP0Wy1RUMukc5ZBKdoRhM_0jqmIxXm0zhamjB6OMvSW_OM5fvYoGtvaABSYZlL-S-j3q_p67hqnjw3SiIqRGLUyi2yljM4_DOmrSMMkzK-OdjKcx0KIPzFoa46tOyhBBS7TnIhidAWREeEAFCQwUIVpyEN6GI0tCX0mXQ9BF_S_6Uaw0iGKlRXsRqNPRvxwEK3rvHtHZfygDAIgrfB46pKko55jESYFx1MIvRVXZDAgnL8wUiD8it2s8TEiKTprO0uxfXASiievIN5A0bpQA4TtAeNAN7XOYkxz3FH_v4b-mqxY0fXIpvRijm54hmRn0Na-9vwxzsVToz_hmBqstwVDC2rZePIi6BlkidSK3E2lxk5o7uUCvH4wGf7S6kPna5JeoclXvi_05m3mhGYImyXIDN6fEGKIrSJ1bJTbKS2d70JJcvujvQCPekirryjsVtUPiNt8Otp_yedEhRs9ouW4jgDqMN-8G2CeoIoyAP2FYBtOBYNQSI_V9ksfaiIZjYEtBCkpRWAVBLI8C-J2bUvdhcH5V5WeRL2I_y8Rj4Pwoj63ddpjgsIfs10P6mSwUB9nPIPeBwCVawu0kFaeHfKIFa28T8PQbkB8WIM-FxvtQBLw_tneoV01UaotOubPkSTFHimyBVN9Np1eK5tWteCMvl_Lusm6rK3r9Ff76Ur4jmJtr-pyMH7hfy-1tiQAUaD67NQOOVapPcbIbDdZvJxXFafZ8QrwxJt9vF5NPBFVV5Lkfyjj6-TH5VNgBGO1YAceDsPiUp4jAmDr0gI4WpxjgKKc4xdOFRUKXi7cLhMaRd1PzW50zB7fMfqRYC-7kMddx2pRJmicyKn1rvTgpxY718pCsYGO-FHlQBSmCmVjzxUkUdvjpQ3N95eV8eal35kpbIEM-pHaoXcoxZgRK_07xzELNotVYb6jek1KCi1S2J_5FAGZaL-9ta83HhzxiYpPPKD_ns28__S8dC6DhBqeGiYjtyqneU4AY3uvvXhr_PK4BPVjKDCfO4-aMkHm2ea6QHJ6rShIPZET1pjNWL_mcxw2pBaVLmpwbIyKcfIhv8S4QDutuXZAreV5oaLYDqKx0oUIahSDrjsikkVw3fVnOjM6Np_ZpibKkGIzWZE-JD8aBZBxIxoFkHEjGgWQcSMaBZBxIxoFkHEjGgWQcSMaBZBxIxoFkHEjGgfyt40AeQoA8hP14EPWR8R6fCKEmCsM0KNInQjL56_PnP1x4_-T9r7a8eBuEavvnlWWF_3YEbUNWTRykWbMzk9Azg7jaAigvt6vNabCcE08fQdvIqrj0Uz9-oukc2hny8QDF_dvflt-7MeclyQ1q39V5x3YtSIIok83PPE2yMTo9Sc1C7FxvBdyEd97dkWnGCWgJdRr9zNNUTEtPU1mKOhvqlmyCnXPfm2ZUVEEUifJnnmbv2MIt_YL8zVQJ63zhPR1iYQ9xZtOn9pezh1joIJCRV38cys_hH-OwZ1-Zsg8DWHhsM8eh1RzOcAa0mlkjXCudJYErQWtFOfhAt21V2vSacCUOXPpzQNzG7wF5YUn6kmPfaIHDYA58X7W3u4iEzm0-4_1ZqIAQh-Rtq8xwndMSzcFND7iGXQcP3czxVxp0uVoHRvYIlRyqgyJAPSEd7zlwwU4s0HH-6qs4sb47ZajsZOqqBAEdMVAgAd0BwDz1krEb4Vq8Ln3OMWJHDl-VCkzQmBoFb3Cw3cTu_7AIwr1K-iAsXqXaOqphc1zeVt__MIg8P6vyKIyCKg8SuJ1FmGWirIr4EESeRRn6ZSDyWAFhBYQVkN-IAnI-GudRHLTgp3GYs48C8hZXZZAkUV2kUSniNE5TkdVZXaZJkTV1HNWJH8a-ALKWcVKWdZMVQdXkWRX6aZPU8pzF7YK8heGFn10E-RjIW96EZRlHDPLGIG8M8vaxQd6CJEtEIrMgyyoGeWOQNwZ5Y5C33zfI29dyp_qlumnbTtfH7DtVnCIek99gHTBtiyVU3lfGdsa0VYMLryxefaFv5KJ280nMdupTPeVMsShHhzwiOqNzTrWzLsciJnWHcBuYjdy_H85LvrsRW4w49GnIUyodJ_eRcquoohBt2Vv3Sx-n06E3R6k2hRaaldeDukFG2WOUPUbZY5Q9RtljlD1G2WOUPUbZY5Q9RtljlD1G2WOUPUbZY5Q9RtljlD1G2WOUPUbZY5Q9RtljlD1G2WOUPUbZ-1Wi7CWiasK4yUK_soqSk-mqyfYh2aomBFIGlUiDVCSZjQc4CawDof3hOahG3YsrMMtKWZaxvXxOWuqJVZyVWSq87hY5u5FHltLcqcIRYdoCBu6X7a1C_VOxWJD_g3DzhS1tno4GrJ0oHDoTVEUA0In9FeLywXEDJVLot_XEAutK753L3ElzEUDWftnXFSjyslFfU4ULc70C2ro0K7tyPIZ9rE85EokGlwZQ0VZpW2rG2kB0ZaOdhmEINNIx0EeyWNU1EPyAcuPrb0mbMZMjHQN-80KZJEMvqMlDQ8Wmkr2XV8OT4fjAUcwtdLQoE_teSIGHqtRa-r0tJ4GtdK_7MV9xHNWBL2SWFL3jqs8yPkF1ZyUKA28fEbU7MnMMmgLPaQhANdFwZahGqbKAXTypg0gOFkzPpsQZnq0yFTDgvGiX1zZ_Ro8nEAaNOBWoVa8pIUt_RUhPWOKuvUQxuSQ1UbjaKi1WLedrgqmiRVkrTT_3x--__27oOrAlC0cwzCyelV2WeUhg5bCppkWgAvQezfqs0SE1koPWSewJQm0QKK1hoHxrzXimDk37QHYeQANNZ4IgJVqvkapu0juPHIXUh2H-h8tk4EzaVb8m8pbDW9GfR8sWi67dXztsItyKjSkXNiUgoAfAC7WvjdaPUZdT0ZQsDUVZJH6RWovNSXA_cUPOylEf83h5yshS3GbMPLKVR7CJPcaQNdkvED8VTgT-25enE4IdGUD1RF2VIIno3OD_XEiVSqzX9wPgkwG4AjkWgNsvO7K6dxxeKliPxgMljsAkF4i9cjAxSG8GksYF3u0rctNNoysn6UubkrgZvSzR6SlEu7ZoGcuu2-16c9PzaMzdUzkVyKJNniQCLmy8K_zVpUoxurR0eOUYgup2aTNLySeYZBBoejfFTHheL4it4QP97_S9mHl_0FSv_RBq0ZRBpR4wQIYgZeXOCyfKaEOBCQaaE5t-S1GUc-y0phZRnIu4LlNrpzkFECfI-Kwahm57jUALKuBmtsVRLUwE23UY7QTfMENSeXJJBo7o6_vxf1ePdBxNfdrbzHupJ2PfrOyO2ismWREbZ9wekwuCSegH9DlxcFRbth26H-Pe_YjfDtVgm6qivV-6Vk4_3f9WXcerT9JZ5K9WV_vvv_okm-WJ-Qqm8EL55fZjGLsArf95sGCPXjn1Z1miIY2nwSxPr8zmrxTnQX96t0LbBG7ivQ1a9Nl2teyq9byUlr_ixdPcTFkcqEciIAIeUSk9C0ypQtjbqgKeAHuxU7_IUNoMpc1Q2gylzVDaDKXNUNoMpc1Q2gylzVDaDKXNUNoMpc1Q2gylzVDaDKXNUNoMpc1Q2gylzVDaDKXNUNoMpc1Q2r9uKO1HgSvuw1o-LSriGeM_Cs7wjPEfhUN4zvhjqJ_9COr2PhLacxwweR-wuH-ZxaClDzAtRyyM43otGnTCVjeURrZ-g9oKxWtBmwTjCmO79Ar9G0oIAhvZClANn-YpaqwPItMS26Kk3qPvVnzTycvHR_qpOEaRO6vOhll35_VhGLNxLquwDlNZNI1fhWByRLGQVD4yjjFrQA5PY8zyzfxd3MzzQYst2GYPsRlP7Dx2sUQtmuZHwRKVWVoWQeL7fgFnEhQVAhyEZRVHdZoXSQ0KdxEWEnSZKqqbED7PS7_2AzDU0zysyvOWN4YmWlwExQiaqMhy2L9AMJooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMpooo4kymiijiTKaKKOJMprorwFN9KOAfcZ-ImQWCBH0cEL7YJ-M5MlInmcjeYIhXMZ5nPtJkx5G8mSgTgbq_B8K1Fnm6IoOwkj0PHUfqJNxOBmH85fE4QyDVCZx45d1IA7jcDLCJiNsMsImI2wywiYjbDLCJiNsMsImI2wywiYjbDLCJiNsMsImI2wywiYjbDLCJiNsMsImI2wywiYjbDLCJiNsMsImI2wywiYjbDKO38fB8RuHvHSOYv95jXn56UKslZVNkQ6rEu1DtOgcOeS7RvOywl6l7s0OHdS5b1fsYOhQPgzYQlPpJO7ARkVid2bgHOXBGbxegWjqZ0CpRLrWTaeMaLOaEoc027nuUwYJXOnQAR9869eilCbNqenzKxzp6eQeCvVXu8bq2Xs3CeMAmKja1XvtbkXrSx_YVKW_6P7sk0GFw3BraRITnS5ngvbkMVfFMGYK6vQR-WXb6Sj70FyApSEGANBSPzishtIwYU42JVOjnGJgbrldabTU7sPQSaUf536WBAg3WAZRHleyiWtCWxxFJ7WgiYxO-mvlaufjz47haf40DpH5USBCwzqP06Cp8jwti7os0qhMY5itXwZhlEVhk9VVlsos9Is8T1IZB2UUN6CQ-k2VNpSacGBJI7CggX8RjcGC-lWSywB0TYYFZVhQhgVlWFCGBWVYUIYFZVhQhgVlWFCGBWVYUIYFZVhQhgVlWFCGBWVYUIYFZVhQhgVlWFCGBWVYUIYFZVhQhgVlWFCGBWVYUIYFZVhQhgVlWFCGBWVYUIYF_b3AgqZFBHpXlFdxk_yisKCT3TRjRgj97SOElkWC5ZqJL4uIEUIZIfRhCKE2-f83DBVa56BRgtGbJHHBUKG_IqjQnSIPBgxFb0zSBL70pVI0DgCGfu4UqzQMHsrgoQweyuChDB7K4KEMHsrgoQweyuChDB7K4KEMHsrgoQweyuChDB7K4KEMHsrgoQweyuChDB7K4KEMHsrgoQweyuChDB76ewQPddCRehi5MdClg8hxvXZroemEL7OylLvQdKA0G1hEAkk0Fb7WzaPfQagMCA-n1Is-s-7kACNX20wKLNeqKQmt7YkmpR62cEKUHgNHcABcRKN4aZ5wBNivbkDpKKvw6SY6nnBukoSwXgGsJKrERE_tEJTlGIJiHKGHIH26iTpRPGKUTlnQK1P_8w06v_rIng2mHyPIIgf9TlTl0830i0Fa2Eg-hQXacFIKQFZffRLMzoOSdS7mQVDT7wzsjBIWB9czMj8DSapj7YNiHMWZTT7c7NDd3tkcPaeXdX16QqZuV2lv2tM2O3Rfx1_0SrN1ehdKJ6dQV6_NZI-hjtX2KRP4XnhW5QCEs0O378Rr1bXZh87V-EHa0SdB5YdJUZxJYaPshWcOXaozlj0W1FRXZrpAYezpnLiJuTE68IhVWKbmeHboqpx4_8oJoSPq3H7ei30rZqTP22EOnAoLwTmspNVWDqDrqleO1MgeobCevvUrB6kf-9BU46WoJqVQXwgNcSZINPYHO-kPE_HgKpDUIBI2up5LLXExx9ziD0TXDbNapALs0qoRSSlTDGbJuDmErmuxR0-j67LYZ7HPYv-XFvvno2lbYGI1p4tk4kAUBz-NIxB_FNRlmSWZRPjksgjTNIH_BbIUohRVGAQ51uyldeBndZP6MhR-U6NnNm8SEZRJXPhnLW6Avxz53_vBRZJc-NEI_rLIRB1Xacb4y4y_zPjLHxt_2Y-A81ShL4s4Yfxlxl9m_GXGX2b85afFXzbn3btY7C20Ru_7vqpVwSOO17YeqPdV-QYa-46KVjvd1cZGXo20cYttdUlvW25MPiIwMlFjupgwgGeUvGlWpMu-TLnw3vGTU0qTIjp4DjUlomQyXZcYpQPIaNdwP5oiqyBj1NY6kDDjTjOV39JXlKssDSAjiRl7_SVn7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfv61Yj-DYiFEmMR-Xdr0BKcSbKgeP6SSyyYKFU3QSNmEwmrITnHXoLrnYcVZut4BtQEkZVU2p_m24aylvBFvQc24AI1NLnesHsXVOgt3QG9S9bWaTRkZpl4_6TmcKhZRN1SP4-J-Hsm_rLbrNcVNrV3n3GLHQtxXkd2MAQxjDhn9XlKpwXMeFNPqUlqJHBP3XkVmaa59xivuusGR6bFgtB0hbRQeQS8xTVjRrvbfteuzQWOqqKrSJPCDtE8lc6rqNIU8pirOalrDwLQuJnYEkOPQMyrVGO6qCjYr3THeF98vdpKg7Vj0XEJhoiRVe04KQafFK4KXd72-hg6FhSTsmB6EQ2fGog6FCX1edyMQkNSq4otW1DPvc9wc9wlH_bGXa6gHOS5RVwXq41sRTTzaiW_1GeY7GordVAxsZSTDs-DQZtFvaPwsRdxb5WAw0TtPuQ4EhYCuDIFeksC-JAutvnT50tUL0qPVbXa1hkODXFmlVY3muaMdIV0RRI0v4rIBQ80aaH2d5b6b84PrJHsxriUJhtN0oMZEZvpvXu4GbexXD3aDKs48on2896JiVpDjMpuEWR9AI0-jv___g2HHXLVelM98E8pzNAIcIUtwpGAWBxn9HUXRzoiYQQ0zLEWncsx6NypF1_JkdIJwGwcTRLI7suQ4mqWFQlmfRFnhDhnlBf2_mWGQZv2Q48tNzfx2losaREDpF4UZDLQqO9j-SuNwlsbHV5qYlYb58XTNIK3LoEqDWNpQlFOQa7CUHlFQW5ByptMcDyRfACO4-us0nWWFQq33Z2GEGRi6qM8MrnfCeS-9I50lmX0HjRNEapxilsc4zguQnHNiD0pM6rA6jYfKt64mUzlVKunKXE78XZTMMthvmKWzPJxZBHQQ0hd7U5t5Xxi990P2K5tFqbOWT3xqPYBrieHM1Z7ouqtNR_vr0-9VuguF6PZ3Cdkt7Atsa6bbAoSzqFApLrtrTYNZGI6tNQlmaXBorb0pvl-mM7J8UmJ7C9uKb526q90UPfQ7eU0cx_IEky6pxwcKuxeDKPC4R7lX_8TyDYo35M57TS_2Uzm5pwr3VOGeKtxThXuqcE8V7qnCPVW4pwr3VOGeKtxThXuqcE8V7qnCPVW4pwr3VOGeKtxThXuqcE8V7qnCPVW4pwr3VPnFe6q0K-AI8-fXqw2qqlMQef8DGqzAnOAcu0tMk-t-jh4rj4X23gdff3JQ7nPw3R8Lp31oGeP9L_YbMez3v3hZ1wOzaeCHnRihPhk0XpgSQp6p3jjVfOH0OwfJUT3vP9VVYXxg7YzCcVWsY95h0bDKVdDpxR1IOB1eWSFr060zPqhxgruAzjHaDnWzONQfQScyDwtR9Axv7letTlbEMi0QfxaleN-xbnMSP6hBQuA3VQRaTSCSAFNNIr9I4tjPDjVIsODgpxsk8J09dWfPb1Zh8d17VPfop3HQ9o8CWZ_56ARL_brwIyHrJJRBluRhVoJtGySpSGVSZDmYtiKRUSj9OEyaNA-atCoykVKhyIEl7QHVJxdBcRGlI0D1SZSmdR6UDFTPQPUMVM9A9QxUz0D1DFTPQPUMVM9A9QxUz0D1DFTPQPUMVM9A9QxUz0D1DFTPQPUMVM9A9QxUz0D1DFTPQPUMVM9A9QxUz0D1DFTPQPUMVM9A9QxUz0D1DFTPQPUMVM9A9QxUz0D1DFTPQPUMVM9A9QxUz0D1DFTPQPUMVP-rAqr3gziRqayCIG9OA9U7Cp1btvdbh61_YascR39FvsEkY3D7A-D2avvwkyBTylYW_YYA72WVZnEY-LkfVQx4z4D3vxXAexrJ4cLHDjmbpQpGOIJJxsdOOYiK_aFHVx4WszQaP2ia3xjpDIq99886m_kndmAw8rFIbR2FsfTzuKgbhvxnyP8HQv7jWl-jnfYhawUGGLrnFtNaFKg2Gke4VlSWj58_GR5XsFHpYLDCEoFPW_poIkiBrILRjUlnfnFoY2BT_rWzu6LUWRytlKjqIYPDISxfN70NSLWxfgoX7oHs793cgR4SjGAcdO6BgbLB7Kv63maY44tFCcskSEolk0046-do3rCDMs3tG7h9A7dv4PYN3L6B2zdw-wZu38DtG7h9A7dv4PYN3L6B2zdw-wZu38DtG7h9A7dv4PYN3L6B2zdw-wZu38DtG7h9w--gfQPF1i4ONXHY-Xane8Pet8MeDrSrF7_STg6dXDSX6KhZ_xxtHLK6CMoyFTtY6hHmCU0xzxB9iHtZh6T79oDqBOaHiOZKT7AZp2eOMnJRzfTKJC8Tvw6feHrfW_TOnYx_1MSQOKjoTg_U10LslGfvgd_nSZjWMnjq2R7JGHs5GNikjzn5Ysdw9GOR12Hmy59hc_uAgQ2ka-BuYGt3KnxD6btiDWrVmkLuOP0jm1tIRMIvmp9htn1hfA-0OB7FVOLtTmdqntf0w7liO7Pom2R0gxofRGITGD04b3kGXm526OqMv_Yz2YDqo97cn5dWQPotcUT9domKoZYCDt4VBUZ0XAJkYYu2pcJV0V5F1GNdh9-BSzM-z1catN7S_XSBAmi4MQYWHsNtmOyISF7LzcEqMsexMTt0J47PhrCM1RaAMCagT8_Yw4i-gQBettZCex4m2rM7VfFomPNK9tAT_bmqxAONGz07dAvG5_da01BnTIzRk7QJ7GAlblXsbrqTFrJD-RbdmOp8nUM-0KblU-1oVmh9h2eiaGrdN3U5Te-TIejwXPtl3UUMJ_9hDVjKLEjyXKZp1GR-XFRpHORxSBkvow1YbNOL0w1YWNqytGVp-3TS9vzWSba3jZrTRfLTeN-aj9KrJyl8P61DP87LPA6E32RBE8VZlqRVnNUxbH2apmECVkJS1w2GU-ugKOK4SbNIAHc6sJ69Rj3ZReBf-NFIo54szLIyriJu1MONerhRDzfq4UY93KiHG_Vwox5u1MONerhRDzfq4UY93KiHG_Vwox5u1MONerhRDzfq4UY93KiHG_Vwox5u1MONerhRDzfq4UY93KiHG_Vwox5u1MONerhRDzfq4UY93KiHG_Vwox5u1MONerhRDzfq4UY93KiHG_Vwox5u1MONerhRDzfq4UY93KiHG_Vwox5u1MONerhRDzfq4UY93KiHG_X8bI16YiGaoKozkWU2-djBHhlYmw-HDTGpTEEps6QqMhla09ZBEnGchQ8FAVmq4Ny9g2Q_hL3YwZNBYw1bRGg3_R78DJ0VngrRFmG29FkTamzcF01Rfahe-1w79zk6GUoBRJcD6OMqpqLCbzrTeFmbani64vUcp72UHZXRr9QSjGE63UnfvCP_GKVXVyjy-iQ7Jy1j_0foUQTLvF6Mf22Sj9C8rKRN4e-zkHorf4hXSsmW-vfGhlG7bEGUdbTNWCo29dckfVibnCwchXS8g7dMUQdzgxXGlY0hgNquMjfygZUz8UD86yI_9aLJeDKgyRn5Cj-gfCrTp4HY5nypxtDeIO1sIEpVuei6dZOyxuvJ0IgCo5omB_-3Z0apQFAQxOoXsZof6kVBoIyoIHqhnagGMwud1vMPQcxPwzqtU9HkWWi1IAco57RpcxLj5iMaNudaNNicQSX4zeIspP8nzRu0xtRo4MdNmDSbhaob0qygEULQHUJlwmT5SZMFHs-oQCvUFk8Ckjqg4UiBP8NEyVIwQdQM1JsDZYrgGqyCfsgkyeJZpB9WdgyYImhpoQGRR8dMkCyfxXrr6JdeDFvp97bbB5gcuT8ryDrwZ7k2qopYnQJtxlkmRp7AAahBYnq4tx2DIDjHpMgLnU0PayfTIbBGVJgcNyHSMogjuEEiaaxfwIFtGm2I9GGISyoNE8upYAu1AKTSM3I5O3JsSnLMIMtdgCoAF-jOlWEUFlSteUrq0KEEpyAE2Y1G9dOKhJJVU0coEXMdi0Es7eGaYKETiDBXwFEE99V1lfMP9INaLDE9-Dl9OIXbVdCHmvPZL_JZ4FOFgGJ_OgBhraphdMD4nlSB7vUNeYFdtrV7JvOlQkbY85yZlj565j0fVOr0ul0aqOVeEFGihqMjXaCep-mhM_1xSLnWclEfFL7LqoO66ok6oa3n10NP8Nwpa9i0RvK5iqHCGycwYo3lfCzVPKpikRQg53vMcwfea1Bq9DBkLtK-qS-Y8YJ3aEiNof0hSgbGFtGrV8s16QlKIbhrtS6lMYuWY3CAWqEqW8yv1N0bcD40Lv4cHblmQ908Wfhuvu6_UgP1IWf4TnVQ07VeF5RVpzuXebqZWafzZFGjoUZhVpPtu5gpyOLh13amBswbg6XCcSJTl8hdYMUJ0AHVvi3bUQ22szVuDnHrQhZqL6cmhcEtTycQUTLJvZunqH4_pfZpqBfBVFsV5RBze_YDJzWRv9YEUK3kdqHcLpTbhXK7UG4Xyu1CuV0otwvldqHcLpTbhXK7UG4Xyu1CuV0otwvldqHcLpTbhXK7UG4Xyu1CuV0otwvldqHcLvTR7UJ_-On_A9dukug)
