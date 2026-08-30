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

[//]: # (ob:c8c9c5ac)
### v14 open-loop agentic-disclosure rerun

[//]: # (ob:b455ff40)
The v14 rerun corrects a separate executor-side limitation in v12.1. Agentic disclosure now starts with up to five claims at traversal depth one instead of one claim at depth zero. The host no longer imposes a fixed tool-call count. Each tool response remains bounded to five results, traversal remains restricted to visible governed claims, and gap-search evidence remains `not_governed`. The host retains independent safety guards for an exact repeated decision, a 24,000-token accumulated state upper bound, and 600 seconds of agent-loop wall time; none fired in the formal panel. This is a new executor run, not another retrospective regrade of the v12.1 answers.

[//]: # (ob:8146dc4d)
DeepSeek, GLM, and GPT-5.6 Sol each passed a fresh four-ask qualification on the exact provider route. The formal rerun then produced 36 of 36 scored Agentic cells: 12 asks per executor, three ask-specific blind grades per answer, 108 of 108 valid grades, and zero inconclusive cells. All 36 agents stopped by returning `executor_ready`. DeepSeek chose zero, one, and two tool calls on 4, 7, and 1 asks; GLM on 5, 6, and 1; Sol on 2, 8, and 2. Thus the observed zero-to-two-call range was chosen by the executors rather than imposed as a host cap.

[//]: # (ob:1e936575)
| Executor | v14 open-loop Agentic | Frozen v12.1 Agentic | Frozen full graph | Frozen static | v14 minus old Agentic | v14 minus full graph | v14 minus static |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash | 84.07% | 68.50% | 67.27% | 67.78% | +15.58pp `[+4.72, +27.13]` | +16.81pp `[+4.44, +31.11]` | +16.30pp `[+3.80, +30.09]` |
| GLM 5.3 Flash | 81.39% | 76.41% | 74.31% | 78.40% | +4.98pp `[-9.54, +18.26]` | +7.08pp `[-8.75, +23.70]` | +2.99pp `[-13.15, +20.12]` |
| GPT-5.6 Sol | 82.41% | 80.93% | 85.97% | 89.03% | +1.48pp `[-7.50, +11.25]` | -3.56pp `[-17.13, +10.28]` | -6.62pp `[-19.07, +5.83]` |

[//]: # (ob:57fc003a)
Bracketed values are deterministic ask-paired 95% bootstrap intervals over the same 12 asks. DeepSeek shows a resolved positive v14 signal against all three frozen baselines. GLM's mean improved against all three, but every interval crosses zero. Sol's mean improved slightly against old Agentic and remained below full graph and static, with all intervals crossing zero. The rerun therefore confirms that the old seed and fixed call budget materially suppressed DeepSeek on this panel; it does not establish the same causal conclusion for GLM or Sol, and it does not establish a universal Agentic advantage.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZhZDMzM2RlNDQzZjM5MGM5MjBhNzNkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImIwNWUyYzA5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hYjhmNGVhN2M4Njc5N2VhMDE2OThlNTUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY3MjYzNmJlZWNhMTNjMzE1ZWU3Y2ExNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfemSG9eV5qtksKejZ0IAmPtS_EVrsTUjWWpKbU-Erai6mXmzCiYKQCMBkmVTf-cB5hHnSeacc9cEEguLJVpun-gOi4XMvPs9-_nO356JzXbeiWZ7PW-fXT1br69z0SZJ0so0TbqkCpsqDkWRtOmzybN61T5ct_Nb2W_h3f5OxFl-VVZFmHV1E4kkCmPR5l3eNnXeCpHnZZmIuM7DpK7arKjaFn5rWimrNhR1VcRJmlXQbjvvm9UbuXl4dvU3_GN7vRW30MNCbLGrCfyjlgv44Q9yM-_mol7IYCPfzPv5ahncwfurzUNQPwTfb1arbr2RfQ_frEXzWtxKnNTg583qLxKmu9tgg3fb7bq_ev78dr6929WzZnX_vLmTy_v58nYrlrdlEj4ffL2R_7mbw7-vd73cXDerZS-XsBbbzU7-PHl2JwUuYh1mMm5CnBn-ci3f0EuwuPJa1GWXSlE0ZV5UhRRhlFelzDIc2WqzxaldL-ZLCSM3O7K4zos4T_JaykZESZNEmZQF_DNX09Gju27Eut8tYMIxjrNZbdr-2dWf_vZMd_-3Z7DLq02P_1KPZXtdw5L_6dlu-Xq5ert89hPMwZwH3ODtrp3L_rlYy3dTGNByO5VvxOL5b7_7w5evfv_lF9d__O7V__rqm-_-eP2HKLz-4svPv_7h6-9-P7tvn00-6FiJ7XYzr3db2M3rWvTzHvuWi-5a9LDKW0nt7bZ3qw2O_fV8iU32D_1W3sOTpbjHTTZzmMCnPR6MZ1fL3WIBM2ruYCelWot6sWpew9tRXtZNEifwOmziVr7D-f4Wz-BStsEfV5vX3WL1NngThVdwquZv4CAG38hbsQi-fCPgIz0I0bY0ujWeRvkWfvmX4NJWFjuBMw6-kA0dZGhm-7DGqeChgQP47OeJG7BI87ar43owYPNpUK92y1bA_Tk1sn8Jxt4_1WfYlEleisf3-SNczuBe3q8CfSADEazVQkyCHi65bCfB_aqVi6lo_wKnrYEnbYCnbOfGthYbMRhY09VZkXThYGBw-dtdsw1aPcD-zGKMvX9iMeo6S8K4ko_v873t8j93QNZwDd-7LXkPZ2LeymUjp7SysGKix9__vHwfTKducEQjhstRNUkpi3wwtM8XYn4_RQoFxKmh3oBK7BbbM8ty6rsTyxOWRVHEaf3xY_jxTgZrAUS2DaJ4uhX96-Be_GW1mW8fAntIsKk1rSa8toUvutUCrtqJM5NXSVEI0X78AN8H30ogWA1s2fevkjx4U8C_4I7PIrNZ04D-98r-B39-pVjHqY0UaR12someZhF3y363RqYi2-kGSY-AU3W3WsLZm96KdTC_hxV8I--BrsO93Ei4qGKJ-3ri4rV5WMRF_PEDnAb38MZ8ClcBePerV18Fb4EFA3lYiM2t3AS9VC31chvMlw1eBtjp5Wrey8ANcAG8fzDApJFVkconOoYdMBDa42m_fQCZw5xHTcPjL-GgLuUieCt6PIQb2a1gGZerEyso2ybMsyTeJyO3yMLnb-QUZaHFqt9BQ28NA7no4l7cyIlbnIVllERd88Sjo7XcrP4ql3rBsHExX9IVhx1_-yA3eolheeEwNptV3we3G7G-O7GWdRrXiWiferTvg89VazjMdm4JtVz_IOXrYLOr1eX_BlbP_aW-OXW74yyNIlG0Tzzc3-IqTVfLxUOgm3WU8a9ysxrQgQavwiRo5luioScWtyurJBVJNRwtcOyvl618d-GRPHz9xOFLi6zNmzB7dI_fLQOgXzLY0iEieqJPHZC7fgJihWawSFRI4YDGA7ENuvmbUysRhU0r2sePy3_3Ho49SkHtXNwuVyAFNMDUxHorN7Pga6DD29V62oIcG7SrZgek-cS42qYDnru3Xl_ITsBwlFAVbFYL2Z8VCse-OLFPeVpmpai7j-nXUYQJSENiAVodHNcWVJXFao0cCZrYbaVZsKtTy1BJKes2-ZjhvHfCOr4L1_kVdf8--I2WcvdYu_lfYuynWXoIiyXTjxndS-BC6tVGLBZ9ALonHNl3sGDIwOFMb5D9wILd3pEs5NTgoD21cGkY5qCD7dEjCTrXG2hbbJq7-RbY8I6EltOs58hHp5SLIo7avI0-sneSFrVY7X9jr1q7wv9Ol3K33QDThts-h2sGyog8faha2cVl9pGju7m5wW__vOxXu00jsdv1rv_z8v_9n_9rqVHQ72oQTEBAU79rEwOJZeoXN84GTsGQBQqRyLKonmAVlVADa9nNFzio9XoByn8AV1M2Dw38hLrZLcjhEkjpgl4mbnKKcrZdV4bRkEH_XnNWJ4zJd2u5meOEz5yzM5-eUk9gEjKL0ycZyVc7OmGDL5FhB_3darcAfQRF2K2_wV03b-bw74dgf7V-mhj7zDPgR6gJXqOwq4we9MRYUOR11VRFG6aibkrZVHUVF2WbxDleoeVqS21qE1KgTUhBcyeb1-vVnCYEPVJPaBcxf6FZ5Ce0PS3mzYPXgm-P8hohS9cjTVX9qtted7AzcrPezLVFrK-jq0LIOu2quo3qoonKOiqrtkzrpgvrKC_jqk7LKhZNJts2Dquk6pIwLcscvimKJM1R2O9BniHLltqtq7j8GRYaDUlxGOfTsJzG1Y9RehVGV2n6WRhehWg80CuOmxxntYhlAYfG_fq3v4cxjE6sMlbdif5OKV1p2YRR2hE9ojY8-5U-zE9teNKdk9lJRF1Uk1pKnXu2KNP5xbYl3WwYwt7WZSFh7rZZZ27SzX6M-YjmOAuQsum_4QlpFErZXa6WU2VUJFn4DbFUvNf9LPgcNOV5i4tGFA7oXQNvgagGCwydbOGHfr6APwLYLIFGVRAu38lmB_8MQHBY7_AVVLfdUIIeeY7pe6u1HhD-7udkruwD-PZebLf4ox7XwwyUjEYuUfVVrEOJ-MstSk0rJcNDT0C079fY5XYjJY1WAuXZzsVCD0MvGmhfWz19-a5Z7OCqoBR2D1LDHH9Wp3Q2QtHNUexkUkeyyCQdPdo2zxjnTsOFxjXdrBBhmUVZHkVJa5r17G262Y-yn43JbXK9EECejRGH9nqPqqMOoU07wRcr2jhc7BXJhuoB7BnwDBDMHqBLpXZ5GleAK7ozvLKn3dCGF2OM0dpJvdsGRz5zykonURa0ParzDZxpI2_nPfxKB8WbwC3ueg9KxdrYydCkccSOMVPr8q14TTKV0UsDTy_FJlotvSoiCANFPVid3KnRQF9-_3VA-6WXCocZp9NG9Pg9vHk_X85J--lFJ7cP2i6wRos_iC0LFHV7qZU40mKJLsKzhRTo1pngJQHRTilQ-g5N8A7tlvr6_BXevt9tPUIA88ZpW-XaGCPu1wupCAcaoxpcY9yn20PNWlt6YEk3K3QqbAP0UBnKgvdPbFF80Ev5w918Te-vQdXz9XuY5_x-vhBuk_zVegXU7h6aadVz0TS7jWgeJkG7eZhudks4QTixer4AGjEJgMbMWxQj7-dbJIuaOi7kFO8anMq_KGMafL8DoQ6JpP8jHclW3q-hcxRRcPX1Rqjt9rdLH5QfsDNac-hpjttFQgsQMVwtOODqFFsRiPYFztNqgee-MfRV3YclrrvbRf8YOtXZP3lovdygDZY-HLmZ7jNsHz-9m8MFQmm4ISF3vsIOWzIp7psCYLTY7O1iVcO7v_k2zibEf97Q9YL31ZMpPglwzEhy7wQ92i3nQJyQWMMXngioW0Y20UjZ6qVF_yauOChvEmTHRas2A9uaL82xhMbomC1AJdhuHvTqfHFkKX7rRg1_fb3FiwnyW4s7MOh7sCDehsyXik4owwkOAogU6OPqruDwxJvVHFtxi2zmQYttBgokbL5Q_PT9mIZsWUqZtjJJC9CTLUtxDg3HUj7QMaGbL9OwTmUoqiwrTPOer8IKGo_3OSD1o-utGH9wT86BUZOFlamqNAubNM9KK_x47gnL7j7GzaBsKBINBvA4CsNZGP6r_y989z-O8algo0hSXM2qlD5LZlGmv_qdcyHYDopwVlD7ZTwrK_3iD-e4Gb0elfhdmsxS7OnESYFD0qagUVQlyYhaFLUeE28rH-v5AOao-DDs7kPQKqqCVwBEMGymg0tE1N_ZU81UgK7DQf_CM2DB8JV8BvyzpZbmJJR1DyTFIqnSgQx48k4dl6rOZN3VNeg_9oY4R4ye98c4VASJS-pg16DS4e12J8PM8cWfl1NoD2_H9C3MRREZzb8XQB7sRDW1HH6pKQoc41YSWemVaX29ALEWp6447XK1uQd-9lfN-jT5tqbbbr4BarieryWqnpr5LJBCenYT-uzIBIjuondhTsI0SNdke4GJK-8NMoatOqiWwSrmAj9s5sjdlpp4Pyh5i1SD2YhTSu9f0qVZFFdR2TSN2T_PT-Wd28f6m2DyOxJx5jQtsScR6i1CMVDNhRgtkC2g-ALPH9qLlrgGAj8mReWEElCKpM26pOvi1pJUz601UAIe7ZEymkHZyCxpG1mWqenLc1L5a_dI_9JUM3bk8erCTlsJF74lLWuNShHweqAaijcv4e2FZwpDqz1QyyXQht3GOYy05Lp9u7KKodLT4JLhykd5sOrwf2mxW5I5lTBEwi5y_yUoaLh00MWXJJc6EzBJCHATSS6DkwH3Tc7XIHT-CDTF2orxUuBJuflv0axK0vzmhRKinOfBcXBqlb64-W_IIOL45sQJSNqi7LqwqovaGgU8Z5xlYI_3o20DuL1AQZQqd4zfeWzPsEg4y3DYSeIxMjuwsXSWE3eKk1kZ0T_CSZxlwXb1Gki7aoHkCy3HEyUi9pcU9Ho2y3Pig-UkzJPBd-R_U1TsdiB8wUdRQh9ls1I1k0yqqjz29UAiu3uA9Wj9sQ9aKXLbygmOGRVx11RhmzSRVdc9L6QJe_oIB6K6FNZeEcjNBk46Mcp6BRfAHv5Z8LJtaaOVsApTdFzIdIttWWapeLQ5GHAYOuQMQLA1oVM3XY-sP6awan1toKuCcqrYPKhL7QpkXuxPNwSTtaeVbpYZLU5J6YfdRgIfgsEgMbkKjGJgjBK9MQMrD4SnRU40ozVN7r0n1lN4cnuLrZ24fGlU15EMJQgFVhzwnLUe-b3I-6pbbcOybUFMFpKIOLXqOWR1qx_jYZVEjMpwlsFNwtUcKFh5Octi9bun88FKu_VSy-c1QL4u8_JUKXV096w6Y-wj8GQKpHLXK6VNi_oo9dGg6JRrcenmT-EkCH-6gfO72qJfBsRFOJ0bGMDMJ5hwZClo0V2Sk5qf3npzWOgT4ADbuzlcK1y_A51yFvxRbO61PLeuMrV8IC_nKMvBGdW2vR69BNozuBBkI9nTGI-fpTgL4yhu6rAuLYHw3N0jvu4P9V9vnxvBEx26ePvI0mjdUmQ3w5BfoAZbZYwEwrFd3U93ay1gwkWHSeI3Rji3t98Qi1bek16IQjqRFexZebPIYIhW2JMiTR2JsC4SGde1WQfPve5buS90lpvLGgOPjKs47TJ7rTz_-YH88mhvuN3QJm3juk2kyO1EnIPccuaPcXd7cvZQkn8f_PtbOIrAY4O4-M0EGNrtnTbD4sa_9-zqvpOTuO0LtJ4oWj8JbskUArdZW9nnS1SsqXdr5BVwRoC9wJ43-5LFH9LgqwWsBxwXNH5AK3-VSj6D79_B-4Fyx2pDMbakDVfDLrYrxe7wGMEkxWKskwDV6DHLlmvwG60pWJqgvQnA_b__cQqiRfDDCtv-g_IuBCjCbPBFJa1bw5jHZ5XMQyrJgxOorQ9ifJyfo9Q7VUd3rb9VijoIEjCiN8TBXRskmCWzUDfw1Xw5sqf-t4rPeDP_vfKsGM8C8sJWmakkWhSh8Qi1BDx4qHYO7Cjm3RPyTVoVZVaBhCPL1lkEbMCFPu0fEz7hXcGXXwe_hY19Kx4044PGaqC3yIrqeQs7Owu-1YqVlcyp34ntaGK_msAwyIy92uyRa0tkfSXgBO2KuqItYSXivLLCuBfa4atjl0dpGHJS53HXtaFsk84usAvc8K1nTxeDYQyDTVUlRVvXRZc6UmbDMnTfTxNh4XFroAXqt6Hd2zcIqOdj9mzt5TGNKrdj8DxQ7vXgL7v2Fv_0HBR3O5BpAxVaoD7D674ls4VTSNQT-kERLXV4RwRe9eZAlnQSlB6XueH9wxLOez83432HzgGQiU85K_68hBUfCUjRmwYqYRlVoJ1HpdMMXYyKd2AeG24Csue71XJ1D9I0XI8ORrx9rj32wD8WUktF--5VvQUzYF9G_NZas1K7lQ9leA60YwJ2AE1Kzid7o9dG3tgTDhSxnSo-dmOXSwLTVF4Z96JZ5Il3CAbeGlgRvD74q3XKbNWcdksyGG5X6oyAFEYrcoI2hJms6i4NBaj_Vr5zQTmONnx4ZI25pTJNq6hqGxA5rH3dBdvoHj4mYgZn7t8-p1e8vZuT_RRNPUR14Vi9iUJj77rFBSf7jO5FmSYXQjmT6OZN3QExcQtoCLpHzXPgnUUHVu_7o-ZLy0MPHceg7S4f4Pi81YLb_a7fasnuIUBGbtQmn8H0cDK2xgwpYLB3cPhI6V1g9878B-IvHBhUxw-2_qefcW9GMr4kqLQ234u04Su8u--e_UQ5ZKTtjz_dyxU7eEp6r31Mq3oFUtyd2LSYQvdrSiqTyzfzzWqJq32N_ur-SG4ZTeKxqWV5XYZ5Hg6zcV4pyYhMGks0YpyJdBt7_2R4WxiVRSMf3yeS5HsBvHspp0jMiNKY6A20EaNtpIav-6F7EM_8SEyb4oPH1mVvFDp47WVrfJOb_ZEHetKzY7Meb_GVPrqBylml8SOhMF6FXixBdAUK_NwEyFhJ1VCDmZqOWdS_PXt7h2Fyv5nvN-EWiwKWgEhvx5ZUr6QaUK9J2FpJZoaGmcFsxNvp2IA-IGQwT8JOFGETp00VFVKmURy2ZSntGvmxgH4cnB8f-Dc-58fO-eURmgcRij-Pxx-eC8Z8kojLUogwxhjCqsg7EKrhf6IQlKm0qNukKqM8zts8K6I2kgX82cVxEsZJIrOuzsumlkfmMxZwmV6l1UjAZV43bZkUEQdccsAlB1xywCUHXHLAJQdccsAlB1xywCUHXHLAJQdccsAlB1xywCUHXHLAJQdccsAlB1xywCUHXHLAJQdccsAlB1xywCUHXHLAJQdccsDlryzgsqiqKs_LNKpCe4e8QBlHGy4MfDHN5g2oIJXMZNi6KEsbC-Pt8mNjW5SBf2qM8JMRk-tkoDBPPTXBHV10Fxi10T8XU88GpdTH-iH44Xcvp3GW62AorWV-KzavSZ6lMARtV9LM3QVbiVu4irfWobXe936_8IOoLDvsjeqnLYoeWfDiBnCoIAM3SoUw4QPyHs3BsjXfWqg1DbvPUbgchfthUbjH4m-PRd4ejbn9lUbbni3h8FFhth-Kxw-CIWl5p8Bak6aGG5QMUSLfRJEWBHSYptCuUDRqnAlvPPftiVDHqoujHESvpxkLsoYlUhet7VrvqpFQPYZgLLtG1zwB8JmB1huVbf10g0StUflg_Et5q2KpKERCX019JYFACtCHTkKuxyLu6rp5mkEe8RJH8I9hU2M29JNIwXFbtEn6hGtJ5jZtehvxoIKitBXKYfFZOqvK9frmBekJJ9YyCsu4kBQf7Ab5ldqKQ-eZ6DC4TjGEKLg9c1kubQbOwumrkzRJFpciffJB4qJi91M8isjraHsGARJiaZxdguK-zDldnAIbbru2iNLyyceL1hdrXLBRd9ZLQ987XwRG8dBZoYNx6qiGpYyzMm2ffMBkzjIhXzQoqztpazEoKmIDvysb2BsbRdKcogAhSOBtncZPPt5vURr5Afp7HUSzmEaufbvWaY1jNGYMYxQB5WN1e1nWhMfmDhnZQeLE4eE8pB37sjIc1NXytsf4ApV7oR25KvLFvDU7xijP5XKcpGAmSGJ2jPWdyeug2BDftPhayvVEN07iogq7o5gSEFM3gzSKUT52QY_d8OTYtkFqXqEVCo8ryssmsmM_oAlEvR06_I8wqXMrqk88XGXSo2F99YAGlEhHRc2O8ZhLVvYIz5hYB81EcWZzSJTGdxgfPr7oHi85N-Xu2F0dPT8e_b9glkU8pQBUbK6V_fx26cWWO8NrL7foTekn1oyhZou2xNkxcn5qXqaPab-G5esw2L3Yj4LVvlhl5tX-P739Zgv2dtgjzWfmjrT233pHSHHmYuFyo8jLhW6zKYVMkAsSyNm9dkTPjlHYC5Z8j2wq7UxHL6ID2TfE2gFpC7a2UjdiKTbGAH4kSUv1eTFhHFwf0ytoj7APu6UOhj56EBVpvxdw6d7RPsGcgt0aR0vR2idyJnArV9Z-Zq1eH5TnVVVVKRq0-oV1m1dZU9ehlFF0LM_Lpt-cz_NiRYsVLVa0WNFiRYsVrf8qitblWdL7aa5ROHEc7ir6eTyn9ZMk8bZNXNdlHEVx3KYib8OijaNOyCSUXSmTNMybrK7TrMnKqsmjKo7TvJUwsSgu06y7bHYHKb3FVZRfpflISm_aRlEYhjmn9HJKL6f0fuqU3hIabEEHqIBjcErv3zul99J1McxvX6a1NiWXpWpzoejOuhg0leu7p5iOJ9M5217xb_0gf2fPm6tWl8weh6tpwwHGtmhDdGUv_UtlramFtjO7Bz5t1KLJ0Ip3aL8TtIiGpKiNxgZUuF7rnwy4DxjaOBLEx-nWnG7N6dacbs3p1pxuzenWnG7N6dacbj0Ww1s2URXJOExcMKXnsHAU-xFOBxO1nSYib-quiTp71T0_hLdkj_UlzJXss5fL5-Lm4ZpM8Hs4ghQIjunNAxncyunbOzwvFLqJ3nUTBG0DNH0tAJ7sSFxwkvt8uyf3NzYKdA5Hk9gNtIlRmrZde9BdgmPw9RcT4w7FWHGVswST6t_KjZ-6pK0JKjlO2xF02C9plUZIm4xYL5yYcCqFr0mlEEUXh9Luneee8Y_7I10sWprXv6I8TBvl5Hht8dYcnXJDJz6IZJxTtntcFDqTy5N_iGqmET6H_7V5M3Z7jHcbx4DZoLgxlmbCMi6VRuJkhv6Y0GAljPMSQ5wXaQ08oAhDm_bieZNOSwyXeYR-EfkhKWYhZZyXs7g8IT5k6axE8SLIk1nyAeJDUShpg8SO4rT4EHd5GokoiWHdrPjgXF1-jsAj3VUVTOEwSVe9iUm8n0Ug7WTr9U83NmPcalnn7Csq3ULrwF7Ix4F5BSaAHH0jh0LpgQHTv3IwYdRKSR5SHEJlAREJAdKxb0dkLA7G4mAsDsbiYCyOXxsWR5nmaVwgXYysruiFSjjy-9ExDrrDTrYiqoCtlnXqlAEb9uDR4MfGK9DIFL4H5pluiG4O2aXxAE2BSsPikb2eDk1_tS__GxJgY0OVguKZet35mI1l8P_2m2-DbJaYP7EZH2SARo-TIRI_TE4HWi2wZ5N8TpRZ6SkoSZIUuZ-ITuF8eEGg2SJGvgD_qxiC4g4TDRYCCzHgDPrywWdxWQ7SzZE_7HMH6OHbfcaQAWMoEmAMjhO8Fb3WTN4AgTl1EDORdCKKiyhrrVnPCy-xXODxcSHw5xGB6wxH8BjDyP4e4AlEIJIqG1g0S4jYTuNZmK7X8K8_TZEJrIH9oyQYgminCffwkBy2GWt5F9qMiHdMo1le6TaLWZxSm3AIItvmGSgLeJcYADRdUIufVbNMt_hZPEsiajEqZ2lGTZ7iDBgcUadd2raNs5naSBu9dx8TIqM2WEXUTuD1JU2CbO_qplNm7IpIBaih_k3EJ7i8mEirVV8b6hsQAdGcaRZ4vEvZibQ8pbBuljqEF0Fv3sqF7drRcjMf9L7RLPeMzxShb3kEEHhYyHkPM69BhcaQXaJdU9WM-gTpp-yVYGg_kP3QItgcWrrRqW4cNWhDxMx02gC9_kvFmFWmp90HZ87ASXW7DSVr2sDqbtXseu0qPXGVZZkmGJvRNU1oj4MLZNLH4WMikDS_7TUKxg0oxOLGYlR48c_WR6dWBmh0azQcHfCsWASemQmoNe18d699KnuU-OutZ0Gz5o-DwGpD8MaNZC5IfbZPtz3VTk_qdrW6XUhvWmbEvYqbDnQsNCNtMdIWI20x0hYjbTHSFiNtMdIWI20x0hYjbTHSFiNtMdIWI20x0hbXu_0nRuCqG-CoQoYHubke4UOz6ELJ5Jvd8nSuqwrSOvXxifTWrirSsq2LpxmMF71Gpxpd4LEOl0GLgGHraH6i6EL0A738_sv_Hfg5ogcpl3VYiSZvxdMMcuCw8N1JI86KocP3bn4ykbVp4SCXT7SvL5UjjUJV5-8CZ7G7F5SkowgUCToTCjpU_i_itB-ac_07EJKBc6Fb-n_-8N3v1eSNW3Ej4dxsUH0Wp875xbnTT9HZYVLuWBLxL9JTnDfQUz4EANCKMn7TElEfRDOeu75nvz6xxFlVhllB0vpTDEdFMZINFDWP3XJJEvRqtx6GYmoPT09n8-YeKKl4QrCnf7dGNBVWNer4P8B4sslmXt4FWbSIX8-O0eBLwJ28boc3eBycxyOqZ5BiJNmz6ECSTIRpSx7EUm-Dp705kad5atXAceAhj2SeGQKIhK4xG3-p8IJMMKqTjw3sSyfwiSCTsHJiKQFuH6rH0cQzw6C4adQEd71ZbkvlnCtiEF5Bhv01yoqHW3AIvHR4zF6B3FjLhT1m6IDAPSXnkKMYjlJsBMlvWxAUgqW6Yzbo4hw802H3ny_ERp3yt3cP3hBscIBOXnBOyeWePU7v1iFS0QFA0mHvv9F2CNcvbaOxWcF90uXdRxZidowinrtLjrQsT5Ko8Wvl0bpLEMyUrzGerrpptde8DcdUovhUhxptV-sjMEs_SKRpW2kpAgguOuz5KGkgb8hgni5CZzAcG9fsX_Op0jJ8YqAdRjBKP3pUJ3XZkB_dI01RrcGHwSzVRZ3iAQoTWSV5WFdZ3bVJGh6DWbKQCH8fmCWWplmaZmmapel_Amn6cjy8fcyb3Ie8SX8eR7T5JIA-TZqkwGDyMs_LsIi6OO5a4DNplscyCmXYVbmsoyjv6rLLugYpVRdncZRU8GdNXvizkzvA8ymvsvgqrUbwfOq2iJK6yxjPh_F8GM_nU-P5JFEMd78syzytGM-H8XwYz-fT4fnQVlriNVSPG_EGlMNfBeTP10t73obS_mQsnNxPHt6iYGW0dLMGZFiZ6BOjjIMmbpj07akftfNCg8WTb91FGtuMJBPK4e3FvUS9d970tNu008Exw51W3NXJZLAhBhtisCEGG2KwIQYbYrAhBhtisCEGG2KwIQYbYrAhBhtisCEGG2KwIQYbYrAhBht6arChvBSNKKumKxubTeKF1Fjy-6iwGN1HXdYg4GVNXKUWfMKLlPGdfo-MdiF5DdcdvkDJSlNc7zFR1l0_5IU4JSf809JOlEGv2ac1_UHuLG7hSM7yMIfamKb30IZ8sCCFDoRH0hdIjU_u0MotEX_IvRmFtFKhIvozE8VnHmf-U0xTUcGkc-RDKtgRmi30S5TFYqzaZghTTw5GHntPdnEcv-qKGrb6gAUmGaS_kvg9av6e-4qpZ8P0vCIkRi1MoNs5ZbNM4zbp8jgrC8vjvYinMdCiD4xaGqOrXsgQQUusLkUwugDIiPCAKmIYyEI05yC8DY-XxKHiLsegi9wbrhXLDZJUSdFBAuJ08q9HwYre-1t08R9KAYDDFT-PvaOpTs4pjpMD4WhFWIumsREQXlyYSRD_iNiucTchCTp5PsuLf_URiCa-Id9A0vheAoTvAOZBN9TFMGclrim-H-C_pusVSPpkUnoxdm4cQTIjcDmvzl6GsVjK9WdsM4PZ1qAoYW6bYw-ibYGXSB3I7Xla_KDmXi7Q6getwR8rnch8a-JLVLpq8NXhmM24UA1BlWS5hZtTow_RZ6TerRJbZaWzNWiJL1-5O9CJNyTK-vxOee3wcJung-WneF40iNE3mq9bD6B24837AfYJiggj4E_olsFwIGi1Rk-9C_LYGNZwCmwpykEoipsoSuVJAL9LQ-o-DM6vacIiCUUaFoX4GDg_imNb7XoMcDhA9nOQfiYKxUP2M8h9wHDpLOFykojjIJ9owtraBDT9DviHBcjzofE-FAHvd6u3KFdNVGiLDrmzx5N8juTZAq6-H06vBM2be_FaXi_l2-t21dxQ9zf49rV8RzA3t_Q7KT9wv5a7-xoBKFB99nMGPK1U7-Jk3xuseycRxSv2fIa9MSbfPy4mn4iapirLMJZp8stj8im3AxDasQSOR2HxKUsRgTH1aAEdTU4xwFFeckqgE4uEThdfLRAaR76dmnd1zBzcMvuTIi24kqdMx3lXZ3mZyaQOrfbihRR72stjooKN-lKVURPlCGZi1RcvUNijp4-N9ZXX8-W1XpkbrYEM6ZBaodVSjhEjEPr3kmcWahQrjfWG4j0JJThJpXviXwRgpuVyp1trOj6kERMbfEbxOV989_n_1r4Aam6waxiIuFp72XsKECP44fuXxj6Pc0ALllLDifL4MSOknm2fKySH5yqTJAAe0bzujdZLNudxRWpB4ZIm5sawCC8e4ju8C4TDup8X5HOeFxqa7QgqK12omFohyLoTPGkk1k1flgu9c-OhfZqjLMkHoyXZc-yDcSAZB5JxIBkHknEgGQeScSAZB5JxIBkHknEgGQeScSAZB5JxIBkHknEg_9FxII8hQB7DfjyK-sh4j0-EUJPEcR5V-RMhmfzp-fOfroJ_Cf77qr56E8Vq-eeNJYX_4wTahmy6NMqLbm8kcWAa8aUFEF7u19vzYDlnvj6BtlE0aR3mYfpEwzm2MmTjgRP3P_68_NH3OS-Jb1D5rj44tWpRFiWF7H7hYZKO0etBahJix3ov4Ca8C96eGGaagZTQ5skvPExFtPQwlaaoo6HuSSfY2_eDYSZVEyWJqH_hYTrDFi7pV2RvpkxY70HwdIiFDuLMhk8dTucAsdBDICOr_jiUn0c_xmHPvjZpHwaw8NRijkOreZThAmg1M0e4VjpKAmeC2ooy8IFsu1Jh0xvClThy6S8BcRu_B2SFJe5Lhn0jBQ6dOfC8Wd3vIxJ6t_mC_otYASEOj7fNMsN5TmtUB7cOcA2rDh67meNdGnS5VjtGDg4qGVQHSYB6QNrfc-SCnZmgZ_zVV3FibXdKUdmL1FUBAtpjoEAC-iOAeaqTsRvha7z--Zyjx44MvioUmKAxNQreYGP7iV3_YRKEf5X0Rli8SrV0lMPmmbytvP9hEHlh0ZRJnERNGWVwO6u4KETdVOkxiDyLMvT3gchjAYQFEBZA_kEEkMvROE_ioEU_j8OcfRKQt7SpoyxL2ipPapHmaZ6Loi3aOs-qomvTpM3COA0FHGuZZnXddkUVNV1ZNHGYd1krL5ncPshbHF-FxVVUjoG8lV1c12nCIG8M8sYgb58a5C3KikxksoiKomGQNwZ5Y5A3Bnn75wZ5-0buZb80d6tVr_NjDo0qXhKPiW-wBpjVClOogq-N7oxhqwYXXmm8-kLfyUXrx5OY5dS7es6YYlGOjllEdETnnHJnfYpFROotwm1gNLLrH_ZLvrsTO_Q4uDDkKaWOk_lImVVUUojW7K35xfnptOvNE6pNooUm5e0gb5BR9hhlj1H2GGWPUfYYZY9R9hhlj1H2GGWPUfYYZY9R9hhlj1H2GGWPUfYYZY9R9hhlj1H2GGWPUfYYZY9R9hhlj1H2fpUoe5loujjtijhsrKDkRbrqY_uYaFXjAqmjRuRRLrLC-gO8ANYB0_7wGFQj7qUNqGW1rOvUXj4vLPXMLC6KLBVBf4-U3fAje9L8ocIWYdgCOu6Xq3uF-qd8scD_B-7mK5vaPB11WHteODQmqIwAOCf2LcTlg-2Gk0iu31UgFphX-uBd5l6aiwC89rcur0AdL-v1NVm4MNYbOFvXZmY3nsXQ-fqUIZHO4NIAKtosbXuaMTcQTdmop6EbApV0dPQRL1Z5DQQ_oMz4-ilJM2ZwJGPAOy-USjK0gpo4NBRsGumsvBqeDNsHimJuoSdFGd_3QgrcVCXW0vs2nQSW0r_up2zFadJGoZBFVjnDlYsyPnPqLgoUBto-wmr3eOYYNAXu0xCAaqLhylCMUmkB-3hSR5EcLJieDYkzNFtFKqDDebFa3tr4Gd2eQBg0olQgVv1AAVn6ESE9YYq7thKlZJLUh8KXVmmyajrfEEwVTcpqafq73_344_dD04FNWTiBYWbxrOy0zEcCM4dNNi0CFaD1aOaiRoenkQy0XmBPFGuFQEkNA-FbS8YztWnaBrL3ASpoOhIET6K1GqnsJr3ySFFIfBjGf_hEBvZktXZzIms59Ir2PJq2WPSrw7nDIsKt2Jp0YZMCAnIAdKhtbTR_9Lqc86YUeSzqKgur3GpsXoD7mRtyUYz6mMUrUEqWojZj6pHNPIJFdBhDVmW_QvxU2BH4X5eeTgh2pAC1E3VVoiyhfYP_-JAqjdhsHgbAJwNwBTIsALVf9qR17xm8lLMelQcKHIFBLhB75WhgkF4MPBpXeLdvyEw3TW68oC-tSuJiOF6iw1Po7NqkZUy7Xu022ztHozF2T8VUIIk2cZIIuLANbvCtaxVidG3P4Y2nCKrbpdUsxZ9gkFGkz7tJZsL9ekFkDT9w7-l7MQt-o0-9tkOoSVMElfrAABkCl5V7HU6U0oYMExQ0zzf9hrwol-hpXSuStBRpW-dWT_MSIM4c44tyGPrdLQItKIebWRZPtDAebN9gtOd8wwhJZcklHjgirx_6_3050jM0ubC3WfBSD8b2rPSONqgmRZUaY9wBkYuiSRxG9DtRcBRbdj2aH1NnfsSnQzHYhqpo65fOldNfu3fVdbz5LJ8l4Xp9c9j_zWfFrMzMIxjCC2WXO_Rh7AO0_sfRhD3qchrOikxDGk-jWZnfmMVfK8qD9vR-jboJ3MQH67Rw0Xat7JvNvJaWvuLF09RMaRwoRyIgAm5RLQMLTKlc2LumAZoAa7GXv8hQ2gylzVDaDKXNUNoMpc1Q2gylzVDaDKXNUNoMpc1Q2gylzVDaDKXNUNoMpc1Q2gylzVDaDKXNUNoMpc1Q2gylzVDav24o7Y8CVzyEtXxaVMQL2v8oOMML2v8oHMJL2h9D_XQtqNv7kdCe44DJh4DFrjOLQUs_YFiOWBjD9UZ0aIRt7iiMbPMapRXy14I0CcoV-napC_0OBQSBjmwZqIZPC9RpbI8i0xLZoqDek30ruunF5eMnbiieUuSPqrdu1v1xfRjGbFrKJm7jXFZdFzYxqBxJKiSlj4xjzBqQw_MYs3wz_ylu5uWgxRZs00FsphM7jn0sUYum-UmwRGWR11WUhWFYwZ5EVYMAB3HdpEmbl1XWgsBdxZUEWaZJ2i6G38s6bMMIFPW8jJv6sumNoYlWV1E1giYqihLWLxKMJspooowmymiijCbKaKKMJspooowmymiijCbKaKKMJspooowmymiijCbKaKKMJspooowmymiijCbKaKKMJspooowmymiijCbKaKKMJspooowmymiijCbKaKKMJvprQBP9JGCfaZgJWURCRA5O6BDsk5E8GcnzYiRPUITrtEzLMOvy40ieDNTJQJ3_RYE66xJN0VGcCEdTD4E6GYeTcTj_njiccZTLLO3Cuo3EcRxORthkhE1G2GSETUbYZIRNRthkhE1G2GSETUbYZIRNRthkhE1G2GSETUbYZIRNRthkhE1G2GSETUbYZIRNRthkhE1G2GSETUbYZIRNxvH7NDh-45CX3lYcfq8xLz9fiI3SssnTYUWiQ4gWHSOHdNdIXpbZq9C92bGNurR3RQ6GBuXjgC00lF7iCmyVJ3ZvBN5WHh3BD2tgTW4EFEqkc910yIhWqylwSJOdWxcySOBKxzb4aK_fiFqaMKfOxVd43NOLPRTqr9UGs2cf_CCMI2CialUftLkVtS-9YVMV_qLrs08GGQ7DpaVBTHS4nHHak8VcJcOYIajdR-SXXa-97EN1AaaGGABwllzjMBsKw4Qx2ZBMjXKKjrnlbq3RUvsPQyeVYVqGRRYh3GAdJWXayC5tCW1xFJ3UgiYyOumvlapdjj87hqf58zhE5ieBCI3bMs2jrinLvK7ausqTOk9htGEdxUmRxF3RNkUuizisyjLLZRrVSdqBQBp2Td5RaMKRKY3AgkbhVTIGCxo2WSkjkDUZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFpRhQRkWlGFBGRaUYUEZFvSfBRY0rxKQu5KySbvs7woLOtkPM2aE0H98hNC6yjBdMwtllTBCKCOEPg4h1Ab__wNDhbYlSJSg9GZZWjFU6K8IKnQvyYMBQ9Eak3VRKEOpBI0jgKFfeskqHYOHMngog4cyeCiDhzJ4KIOHMngog4cyeCiDhzJ4KIOHMngog4cyeCiDhzJ4KIOHMngog4cyeCiDhzJ4KIOHMngog4cyeCiDh_4zgod66EgORm4MdOkocpyTbi00nQhlUddyH5oOhGYDi0ggiSbD15p5dB-EyoDwcEq8cJF1ZxsYudpmUKC5Nl1NaG1PNCj1sYUTovAY2IIj4CIaxUvThBPAfm0HQkfdxE830PGAcxMkhPkKoCVRJiZaaoegLKcQFNMELQT50w3U8-IRofTSgl6Z_J9v0fjlPHvWmX7qQFYlyHeiqZ9upF8NwsJG4iks0IYXUgC8-uazaHYZlKx3MY-Cmn5vYGcUszg6n5HxGUhS7WsfJOMoymzi4WbH7vbe4ugxvWzb8wMyebtKetOWttmx-zre0StN1qkv5E5eoq6em4keQxlr5UImsF_4VsUAxLNjt-9Mt-raHELnavwgbeiTIPLDoMjPpLBRDtwzxy7VBdMec2qqKzNdIDMOdEzcxNwY7XjELCyTczw7dlXO9L_2XOiIOncY92J7xYj0-WoYA6fcQrAPa2mllSPouqrLkRzZEyfMnW_d5SD04xCaajwV1YQU6guhIc4EsUa3sRO3mYgH1wCnBpaw1flcaoqLOcYWfyC6bly0IheglzadyGqZozNLpt0xdF2LPXoeXZfZPrN9Zvt_b7Z_OZq2BSZWY7rKJh5EcfTzOALxJ0FdlkVWSIRPrqs4zzP4v0jWQtSiiaOoxJy9vI3Cou3yUMYi7Fq0zJZdJqI6S6vwoskN8JeT8McwusqyqzAZwV8WhWjTJi8Yf5nxlxl_-VPjL4cJUJ4mDmWVZoy_zPjLjL_M-MuMv_y0-Mtmv52Jxd5Cq_S-d1mtCh5xPLf1SL6vijfQ2HeUtNrrqjbW82q4jZ9sq1N6V_XWxCMCIRMthosJA3hGwZtmRjrty6QLH2w_GaX0UUQDz7GiRBRMpvMSk3wAGe0r7idDZBVkjFpaDxJm3Gim4ltcRrmK0oBjJDFiz11yxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7GfGfmbsZ8Z-Zuxnxn5m7OdfK_YzCBZCxFkatrUNT_AywYbi8WMyuWygUNVFnZRdLKyE7CV3DbJ7HpecpfMdUBrAo6zS5jTdNpS1lnfiDYgZVyCxyeWe1qOoWm_hDqgnlV-ryZThYar7iaNwKllE3VDdjo_7eSL-stltNuQ3tXqdd4s9DfFQRPYjBtCNOST0B0GlBs95kEyrU2klUkxce-WZpbG6iFdcdYMj47BgtB4hrRceQS8xTFidXW2_W20uBo1pkqbJsyiMchdK5mXV6RPyMVlxVtIaOqZ1MrHHgDyDnhGpxnBXlbNZyY7pIft-sRcEbdui7zJyE2W5WnMSCHrNXhG8vHfyGhoUFpKwYxwIh46MRRkKA_qC_k4gIKkVxRcr0c6CL3Fx_C888cderqEc5JlEfRHI-bcSGniy599yEeZ7EopdVHRsFcTDi-jYYtE71H6RI-6tMjAY712gTAeCXEA35oBeE8O-Jg2tvfbp0s0LkqPVbfalhmON3FihVbUW-K2dOLoiSrpQpHUHippV0Fye5aGZ84PzJB0b15wE3WnaUWM8M-7Jy32njX30aDOooswj0sf7IKlmFRkui0lcOAcaWRrDw_8Omh0z1QZJOQuNK8-TCLCFIsOWolkaFfR3kiR7LWIENYywFr2KMXNmVPKuldnoAOE2DgaIx-7ElNNkllcKZX2SFJXfZFJW9F8zwigvXJPj083N-PamixJEROEXlWkMpCrb2OFM03iWp6dnmpmZxuXpcM0ob-uoyaNUWleUl5BrsJQ-IqG2IuFMhzkeCb4AQnDzp2k-KyqFWh_O4gQjMHRSn2lcr4TXL_WRz7LC9kHtRIlqp5qVKbbzAjjnnMiDYpParU7tofCts8lUTJUKujKXE99LslkB6w2j9KaHI0vgHMT04GBos-ArI_d-yHoVsyT35vJZSKUHcC4p7LlaE513te1pfUN6X4W7kIvucJWQ3MK6wLIWuixAPEsqFeKyP9c8msXx2FyzaJZHx-bqVPHDNJ2R6ZMQ6zRsy7516K42Uzjod7KaeIblCQZdUo0PZHYvBl7gcYuyE__E8jWyN6TOB0UvDkM5uaYK11ThmipcU4VrqnBNFa6pwjVVuKYK11ThmipcU4VrqnBNFa6pwjVVuKYK11ThmipcU4VrqnBNFa6pwjVVuKYK11T5u9dUWa2BIsyf3663KKpOgeX9FyiwAmOCfeyvMUyu_yVqrHwstPch-PqTg3Jfgu_-sXDax6YxXv_isBDDYf2Ll207UJsGdtiJYeqTQeGFKSHkmeyNc8UXzvc5CI5ytP9cVYXxhrUxCttVvo55j0nDKlZBhxf3wOG0e2WNpE2Xzvigwgn-BHpPaTtWzeJYfQQdyDxMRNEjvHtYr3SwIqZpAfuzKMWHhnUbk_hBBRKisGsSkGoikUUYapKEVZamYXGsQIIFBz9fIIHv7Lk7e3mxCovv7lDdk5_HQds_CWR9EaIRLA_bKkyEbLNYRkVWxkUNum2U5SKXWVWUoNqKTCaxDNM46_Iy6vKmKkROiSJHpnQAVJ9dRdVVko8A1WdJnrdlVDNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1A9A9UzUD0D1TNQPQPVM1D9rwqoPozSTOayiaKyOw9U7wl0ftrePzps_Qub5Tj6FtkGs4LB7Y-A26vlw1-iQglbRfIPBHgvm7xI4ygsw6RhwHsGvP9HAbynljwqfGqTi1muYIQTGGR6apejpDpsenTmcTXLk_GNpvGNHZ1BsvfhXhez8MwKDFo-5altkziVYZlWbceQ_wz5_0jIf5zrD6infchcgQDG_r6lNBcFqo3KEc4VheXT-0-Kxw0sVD5orLKHIKQl_ehDkMOxikYXJp-F1bGFgUX5t96uihJnsbVaoqiHBA6bsHTd1DYg0cbaKXy4B9K_92MHHCQYwTjo2AMDZYPRV-2DjTDHjkUN0yRISsWTjTvrlyjesIcyzeUbuHwDl2_g8g1cvoHLN3D5Bi7fwOUbuHwDl2_g8g1cvoHLN3D5Bi7fwOUbuHwDl2_g8g1cvoHLN3D5Bi7fwOUbuHzDP0H5BvKtXR0r4rD3dK96w8HTYQ0HWtWrX2klh14uums01Gx-iTIORVtFdZ2LPSz1BOOEphhniDbEg6hDkn0doDqB-SGiuZITbMTpha2MXFQzvDor6yxs4yce3o8WvXMv4h8lMTwclHSnG3K5EHvp2Qfg92UW562Mnnq0JyLGXg4aNuFjXrzYKRz9VJRtXITyF1hc5zCwjnQN3A1k7a1y31D4rtiAWLUhlzsO_8TiVhKR8KvuFxitS4x3QIvjXkzF3t7qSM3Lin54V2xvFK5IRj_I8UEkNoHeg8umZ-DlZseuzni3X8gORB_Vs9svLYC4JfFY_W6JgqHmAh7eFTlGtF8CeOEKdUuFq6KtiijH-ga_I5dmfJyvNGi9PffTBTKg4cIYWHh0t2GwIyJ5LbdHs8g8w8bs2J04PRrCMlZLAMyYgD4Dow8j-gYCeNlcC215mGjL7lT5o2HMa-mgJ9y-qsADjRs9O3YLxsf3gz5DvVExRnfSBrCDlrhTvrvpXljI3sm36MaU5-tt8pEyLZ9rQ7NC6zs-EnWmNq6oy_nzPhmCDs-1XdafxHDwH1aApS6irCxlniddEaZVk6dRmcYU8TJagMUWvThfgIW5LXNb5rZPx20vL51ka9uoMV1lP4_XrfkktXqyKgzzNg7Tsi7TSIRdEXVJWhRZ3qRFm8LS53keZ6AlZG3boTu1jaoqTbu8SARQpyPzOSjUU1xF4VWYjBTqKeKiqNMm4UI9XKiHC_VwoR4u1MOFerhQDxfq4UI9XKiHC_VwoR4u1MOFerhQDxfq4UI9XKiHC_VwoR4u1MOFerhQDxfq4UI9XKiHC_VwoR4u1MOFerhQDxfq4UI9XKiHC_VwoR4u1MOFerhQDxfq4UI9XKiHC_VwoR4u1MOFerhQDxfq4UI9XKiHC_VwoR4u1MOFerhQDxfq4UI9XKiHC_VwoR4u1MOFerhQzy9WqCcVoouathBFYYOPPeyRgbb5eNgQE8oU1bLImqqQsVVtPSQRz1j4WBCQpXLOPXhI9kPYiz08GVTWsESENtMfwM_QXuGu0NkizBYXNaHaxnXRJ8q56rXNtfe_o52hEEA0OYA8rnwqyv2mI42XrcmGpyveznHYS9lTGv1aTcEoptO98M23ZB-j8OoGWZ4LsvPCMg5fQosiaObtYvyxCT5C9bKRNoTfRSE5LX-IV0rBlvp9o8OoVbYgytrbZjQVG_prgj6sTk4ajkI63sNbJq-DucEK48r6EEBsV5Eb5UDLmQTA_nWSn-poMh4MaGJGvsYfKJ7K1Gkgsjlfqja0NUgbG-ikqlh0XbpJaePtZKhEgVJNg4P_HKhRyhEURal6I1XjQ7koipQSFSUvtBHVYGah0Xr-IYj5edzmbS66soitFOQB5ZxXbc5i3HxCxeZSjQaLM6gAv1laxPRfkrxBasyNBH5ahcmLWayqIc0qaiEG2SFWKkxRnlVZ4POCErRirfFkwKkjao4E-AtUlCIHFUSNQPUcKVUE52AF9GMqSZHOEv2x0mNAFUFNCxWIMjmlghTlLNVLR28GKSxl6HS3D1A5ynBWkXYQzkqtVFWp2gVajItUjDKDDVCNpPSx0x2jKLpEpSgrHU0PcyfVIbJKVJydViHyOkoTuEEi66xdwINtGi2I9GGISyoME9OpYAk1A6TUMzI5e3xsSnzMIMtdgSgAF-itz8PILahK89RUoUMxTkEIsluN6qcFCcWrph5TIuI65oNY2s01zkLPEWGugCcIHorrKuYfzg9KsUT04HX6cQq3q6IfNeWzD8pZFFKGgCJ_2gFhtaqhd8DYnlSC7u0dWYF9srW_J_OlQkY4sJyZkj565I4OKnF6s1oaqGXHiChQw5ORrlDO0-ehN_VxSLjWfFFvFPZlxUGd9USV0Dbz26EleO6lNWxXhvP5gqHCGycwYo3lfCrUPGlSkVXA5x3muQfvNUg1ehwyF0nfVBfMWMF7VKTG0P4QJQN9i2jVa-WG5AQlELxdaVlKYxYtx-AAtUBVrzC-UldvwPFQu_g6GnLNgvpxsvBsvnGPVEPO5QzPVAU1net1RVF1unJZoIuZ9TpOFiUaKhRmJVlXxUxBFg8f25EaMG90lgrPiExVIveBFSdwDij3bbkalWB7m-PmHW6dyELl5dSg0LkV6AAiCiZ58OMU1ftTKp-GchEMdaW8HGJu935gpKbjryUBFCu5XCiXC-VyoVwulMuFcrlQLhfK5UK5XCiXC-VyoVwulMuFcrlQLhfK5UK5XCiXC-VyoVwulMuFcrlQLhfK5UK5XCiXC_0U5UI_P1Io9PMjJUI_P1Yc9JUqCxr8-E9VF7Qpm6rJRLNX_ykNVmu5nFKC8giGg4FFOlOp7MJWTlUqS7Os6whZ6SmHpyL_UvWic-p7vlqbvtojtu8COKOOfZqfqlQWpXnbkHPjKUf7MTlaJ0YLrDDJsyJ74tEO0YcGzZn81vfBVxr-mKKM3M-n6qplRdeEYSKeeLi_2RCwjWyNowdZ1VCIxtAEbXsbegovqwvqXbEzdUGHs1GH09ih9O2YHbse56tYOm8NAoxo1qBSGZypF5M0VWJogziODq9nJC9UF0vwIMkMt9oBIe1nx-7G6aEOPBQTwzSG5UY9XxuG9OxMYEZtBmtvr3ENefOigqGzY1fh2OCUvHUQqYJb5tUktZ5J9P7Ne4S4M4Fa3ciRnxDekEJh0sFSKkJJo6nMjt2AIzVBt8KU6zDqFhmB1yhXKM9kp2OaaZjuJBv0lovKqI6VAX3lCnu6c3Z489WZ9gAPKNTDQMErwUeH1IHEYnPC19u7KdmeCRqHwl3UaXV5zDqFGQVuVC-92H-TpPzCnmZfcHcb4K-_iTPstQGchH6PDuzgJmxQVoPTrmSrxcOHVR8VddmlUhRNmRdVIUUY5VUps-xY9VFbye989VHm6czTmac_HU-_vG7w6eqjrhjnJ6k-mrdlLEC_KGCBMUkoK9usitOwEyKvijzr6rSN06Yr4ziSdZ1KWYm8k3nVtWmZNxdXHy2v0uQqLkeqj9ags8dNWHH1Ua4-ytVHufooVx_l6qNcfZSrj3L1Ua4-ytVHufooVx_l6qNcfZSrj3L1Ua4-ytVHufooVx_l6qNcfZSrj3L1Ua4-ytVHufooVx_l6qNcfZSrj3L1Ua4-ytVHufooVx_l6qNcfZSrj3L1Ua4-ytVHufooVx_l6qNcfZSrj3L1Ua4-ytVHufooVx_l6qNcfZSrj3L1Ua4-ytVHufooVx_l6qNcfZSrj3L1Ua4-ytVHufooVx_l6qNcfZSrj3L10aevPtpmaQSnuImbxCYbeEB0A2Hw8RhyRhjM6iisRJK1eeni2i2s3EAYfBwinMYxc14xb3xUEBVBi7XRE-4JeuGI62vUka0XmUPwhSQpeiAM-KeJntNv2KJzyguB5UDxZGwohb-nuKIDjE7EstQCEjk4rHRoTPzO4z8IlJl443Ng8H5g0Jt5P0fnwDBETYs7noPYBbvpZobRQN6ElCOoPw4YSkqQjUPZwEs6O0bF2EDXQZxOwjCckgGHsBjudwt6iaAW_FwENdAcuIwuO0TQFxRdrgIf6K7OMeR2SVK8pgV-3I9N4_E9M15g3dKUJFPG5FGlxkBuapamrumJeyRydKq1TVSFNmXDwyB8AsfJ0N2xMo6zw9ifYWqftMl9VkjedwRYDzLKvle2_u-afG5q1UxgxoCSHkRrm1RJTwr_AJkbK6fAoGizexuvUKO8C_I3qTL7Jn7fQXSHkDDY-CSgUmykaGHVYheABosGgnWhnkVe7AI8wKpg-oFyYGB07iQo1W_kldvpYpcGrhY7w7I9qOIrBx1VAET2QKNZ4uB992Y_CC1V9EE7jemqNWJ9Sm9v8zwqkzwXpU0a8IAjR-O4PwzzUf_sGX7sb5oJqiapuFmAaq371v0--Nz9bFr4EK_FBSHhKNSls5DEQivqW4ndyt6fRRnIsOs1GhtTkD4mwWdxMYuSn27oYT4rI_MwTbH2KkjYkX2IZjp8mMxKTEJMwllY4cOD0HIcTaQjx63QbgVwK0_rpEdlwMtSZQuMc9VfMQv1sxLEbBxoMitC9SwmGYmsnAgngQ9B9o3tWAYVnspYD8AK31aAtnLwZyBC694KWDwcCegYGfU2TWZZrnvDtdIm61I9zMkSSQ-hMbhUn2WgV-CzE0J0klZZV4ooEbklkx6aqD7DHwME6qJGVEqM5yxVWS9OUwNhvCdnvMbUsYVqCR1aVac1ErMTEbXkZqGGZ1qIpZRXi2Z38J228ZIEuye69k50PWinX4AMi8Yv06B_65SpQeeZKFPrntFWXTod-6aCmwdBNUhUnQBjmYU2aVGx3c1976E7L9p9MGcfxtmD__MQncfNvsdMoHbHMG6MUhAUo1gtTaRQYK3wy_YCO6pdrfaNINXqVOZl0qQiq0QjXUWhSiJya7Uf5WuVLQfrM14rWxjZ04ivuuquCQrp0a9gGvONlXgyDDMG7k5mM2UfQ7ZGpkUN4alDI8WIeUbUK0w30rXRcDzULr6OcQ1Gv_DTxuDZfOMeqYZcBCY8U_WJNfTBFSWZ6LrAgS4V3Ou0MRS9qAyvNey6GsGqIMjwsR2pKZWDsYOe6K9qsKs0BYctP4FzTVAQKH2PGHR7C_ngXWSd103Fm9WgMNYr0PH0FFv94KftqPenVJwYRRYY6koF_Yi53ftBzAZpg9owhpfqVNRBlEeRiJsoSq1RHuSnuJCyGCR9_26OiS6U3uEqZhsngK2crUOmDEoghi-djgxrwiIJRRoWhXCAJEkWl2IvdwKbmqKMiqSD4En8RHsCc1ZZERQNoxKRdCC1UkxpoBqkVdfOxfOsfVC44WTQxwtMSaCu7i5NWAuZ-iAoqbGIByWRVc4s_B6X5SDK90jh49-t3iJdnijipG-nTeAhVDbC_oLjarbZuSmQJg2LYKvQw8P61y-0p2i5u69R50e6ILxN9PL29S5O9sESxwnMOYdPJpJORHERZa1Vu9u2a4soLY8Ijhbu1EavHCQBfq-4rzLxvD_m8n6ELXcv2c8v_whCT6LAtEDIIklqGpPnGMvcTzGbnHyhKXnjfzqe-jdoM9bAGREaVanNaJZXuk0QJJVjGsStyLZ5pvIovKvsxfGsoBY_AylPtwgiXBIZ92-aUZMnBCYRNU1VlmEs08SBr8k4K3290iZ1qAoMC6-wpo5IaBZobXxwMo4teaE2WIs7pEgDr3en0h7G2Ri26LLTZoRjwboquFaLcSaXyLJpfZ5tXXavQMhqo8txSMNaJkhsp-ZdHTMBt2w6KOuu6PkpJ0hXZ3mZyaQObX53nDewovmexUtzIsXs8KINVPDTCd5VGTVRjhUlra6WVWWYFWV0zFisCc8tKPHrIfKSKoCNVkdgtDeaw17Pl9d6ZW40sx3SIcdoR4jRLPj3gT3BVlxZ6YLbqMCTPYL4HWXnU8qRMovse7sVHR_SiIkVBwm-lti85rnY3GDXqDjMem6RXHRVwuCH71-a0FCcA8Yzqih4ojy-QkCMd_tcldN7rgKPQQ2Xzet-4ocBj6eaLwhN_AS26Xd4FygOtBoNPFWc54Wuj02me9_GYfYCG6FWqG74CZ40AgWtL8uF-GXjyNfG8kUoVVoyOcc-ZJkmCHnfgZBgSVBdhm2del7DYYIajU_n6Vm0Nxy9KWpr2PJWLFa31tSu69bDmoub_Yw2HYivNCgnFBh4HlPang7ikixAcEjmu3uTluzTaMI-cMtndaiBWcpklCmT_BjCW-vFHOw5qT1cIj2p29XqFq6qm5YZca9Sgox34JQFKKrrSIayzqQNpujKKklFUg2Rgbwa6mezAtqwbNtQVEImFtUpLbI2b_xy5N8tg-Vc0wZtQNfUSSG2W3hBREc8gIOlavLhLANuSFP1gWFzlbmPv3tYtXhH96DlvAaocrJ5eaqyFil_1oboGzR4eDIlA5TKr9Vsj5RsHBRZIzWPJIQpNLQcyjEzH8sH9TYs9-fwW04i1mrqY3BM6BMio3O4frh-B1i4s-CPYnOvcSjXVaaWL54hnpGyik90agISG0VHFoJwrS6OBYizMI7ipoabbAWLLgqbVrTervsHSfkJxCBbvBVrWCAVRQbkZUrFSw1lf24AM_ECo2REdRVsxWYyE7TEk5qtUmzr1Xa7ukelTQFjrikDH78xqVEWmMbI5628J0qHFI4Qb7BnVeuXyiOQ6HEKHaOORFgXiYzr2grHTVcUhX_6qaaHggtWlAsr2Z-u45DGdVFj1HiX2WuVp2VWino0YXjixZf5yGKK-unlPwVwlzVpG9dtIkXuKlhLKeEnX8q3ia84BQxXp_bfB7_RpUpOFolwwHZDBNKzIrGrIuLXww5UEWPQ2pWRQUEu-liLClyQerclLRC4AigvGU_2QK-c7lCjaxxa-asCScSSGOQrGSBQqsLLroK87WK70qFWcIxgkqjIjJqe_2MUkds1-I1GOLU0QddO2TfV_kHVUgkQdGUjqX6wqohwUPtAw3HpmEerM0qnu42N83MUyqfq6Jp4SYUQ6MVcem2MpaEf7Kn_rY6ldDP__VBRVpIWwWsPGSUcPJLEfKg98-4JvSitijKrmiqUZeuQjEO4XdIzWKBxwDcAoIyi2LHhwr2tEUAsZbNadWS2HFzBl19bueVoXv23GnTEynLU78R2NLFfTWAYVPWBVByfXFsiO4AKOpk32JawEnFeWWtlm4ZhLopkDynQIKh49Pe0RSiu87jr2lC2iY0VE0UctXm7p8EYSus3bWfSrvC_06XcwXXFBHCS81B4OkHKQOWtUHWqiy51pKyVXVx6NPnm5gb_9eelutK6KJCuLu_KONeKOajffeKz9ybRAvXbULPwgYzV8zEcfu1oN42qIkvBc10JnoAH8E-vnocCiFTVz9RnFlqjcVh56onCADZRAeNYbOrNAcyZk6D0uGwAtUmCNL8rVJCTRRb-vIQVd5vWwPkeAA7XoNtWSdRFznReC5HIsqiGB0ZZrmASHQb4o6NggQmjwPtk89BQVXED_zjRRkO1IFvxDlFXHiZkeYARb5_r-mTAPxb70aiWdqot8FGDBsn9ykU9PAe6oALsAEJhu7ozNwZw5caLv9BYLy-CG7tcEpimqibhXjSLPPEOwaDKhFV7J66YhLZzuJTPSzM5i6qq8rxMoyq0dygHrS3Pw2FRgFeKcpO_aYnJ5SfJQpE3oIJUMpNh64qth1FZNHtRcPcCyMFSUio_Dd6Crui6nPV8qUvc2koJTmWdGmjfyQh-7GQAczT11AQPjg-PiE6X98_F1DOz6rD_h-CH372cxlkeKOuBVqO_BV2W5FkquqbzLzVz7wWCBP2VHH02b1wVF9ur9fXC1hvbiLee3Vjj8Wjd2CMLngcIhwoysEbiMcXS5D3C2LuoF1N-EMMHYCtPMYwwk1XdpaFIUisjdm3XlWE0sH0Fv9foG86EgLHoIDhgVdOTjgSZplVUtU3rkM2xvIDMYo8vf7Xb6lowXhktDFjTkI1bjHrc-lS86-Dq2AoZPkneL3ml4pVMlvibKLTRSrh9pPnrXpRivxCqMgqR46mjGqZ0n0UhHxQow2osvV9cZb60gtVhjbBZ8HL5QL4iJc0TeIAS9x8UxqC-Ar7U0QO52BrrlwlW0jYh6N5h2c97Fdc2Amv508_w__8frMnYow)
