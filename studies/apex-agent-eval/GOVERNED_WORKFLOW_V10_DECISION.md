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
DeepSeek and GLM each passed a fresh four-ask workflow qualification before formal scoring. DeepSeek completed 12 of 12 qualification cells with 44 of 44 terminal receipts; GLM completed 12 of 12 with 56 of 56. The models then ran as separate single-worker formal panels to avoid shared-provider load. Each formal panel contained the same 12 lawyer asks and three conditions, producing 36 of 36 scored cells with zero inconclusives. DeepSeek had 71 of 71 terminal receipts; GLM had 76 of 76. One GLM relation ask reached `executor_ready_forced_finalization`; all other agentic asks reached `executor_ready` without forced finalization.

[//]: # (ob:e4329246)
| Executor and condition | Rubric | Mean context | Unsupported claims per ask | Citation errors per ask | Authority errors per ask |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek v12.1 agentic disclosure | 39.90% | 7,273 tokens | 0.000 | 0.000 | 0.000 |
| DeepSeek full-graph control | 38.01% | 20,455 tokens | 0.750 | 1.417 | 0.333 |
| DeepSeek static baseline | 33.33% | 23,985 tokens | 0.000 | 0.056 | 0.000 |
| GLM v12.1 agentic disclosure | 43.69% | 12,379 tokens | 0.389 | 0.417 | 0.167 |
| GLM full-graph control | 36.33% | 20,455 tokens | 1.861 | 8.917 | 0.194 |
| GLM static baseline | 42.64% | 23,985 tokens | 0.000 | 0.556 | 0.028 |

[//]: # (ob:989b7acb)
For DeepSeek, agentic disclosure exceeded full graph by `+1.90pp` with a 95% bootstrap interval of `[-6.79pp, +10.23pp]`, and exceeded static disclosure by `+6.57pp` with `[-6.13pp, +19.84pp]`; neither contrast was statistically resolved. Its context was 35.74% of full graph and 30.32% of static disclosure. For GLM, agentic disclosure exceeded full graph by `+7.36pp` with `[+0.04pp, +14.64pp]`, while its `+1.06pp` delta over static disclosure had `[-10.71pp, +12.39pp]`. Its context was 61.22% of full graph and 51.61% of static disclosure. The result supports bounded agentic disclosure as a qualified workflow for these two executors on this two-task, 12-ask panel; it does not establish a universal executor ranking or a complete native 12-task Legal E2E score.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZhZDMzM2RlNDQzZjM5MGM5MjBhNzNkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImE3YWQ0YzY3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9lMjdkYTZhMTkzY2ZhNWJlNmU4NDNlNGYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY3MjYzNmJlZWNhMTNjMzE1ZWU3Y2ExNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfemS40aS5qvAqqdtdkwkC_eR9Ut3a1Zqaao03WMmyTIDQCCTXSTBIcisylbp7z7APuI-ybp7HAiQIJOVmSqpp93aTF1JAnF4ePjtH39-JjbbeSOq7eW8fnbxbL2-TEUdRVEt4zhqosKvitAXWVTHzybPyra-u6zn17LbwrPdjQiT9KIJ81JWpd_4cZQWTS7DuJFVmPpB0zQyigqRR5lI8iouEvhHXYq4qEQu4hLmCPMMxq3nXdXeys3ds4uf8Y_t5VZcwwwLscWpJvCPUi7gg7_IzbyZi3IhvY28nXfzduXdwPPt5s4r77zvNm3brDey6-Cdtahei2uJmxp8vGn_JmG7uw0OeLPdrruL58-v59ubXTmr2uXz6kaulvPV9VasrvPIfz54eyP_ezeHf1_uOrm5rNpVJ1dAi-1mJ3-ZPLuRAokoYJdxleLO8JNLeUsPAXHlpQyzWqQiKKKqEUkpU5nHkYwbXFm72eLWLhfzlYSVmxNZXKZZmEZpKWUlgqiKgkTKDP6Zqu3o1V1WYt3tFrDhENdZtZu6e3bxw8_P9PQ_P4NTbjcd_kt9LevLEkj-w7Pd6vWqfbN69hPswfADHvB2V89l91ys5dspLGi1ncpbsXj-5bd_-fzlnz__7PKv37783198_e1fL_8S-Jefff7pV6---vbPs2X9bPJebCW228283G3hNC9L0c07nFsumkvRAZW3ksbbbW_aDa799XyFQ3Z33VYu4ZuVWOIhmz1M4NUOGePZxWq3WMCOqhs4SaloUS7a6jU8HaR5WUVhBI_DIW7lW9zvl8iDK1l7f203r5tF-8a7DfwL4Kr5LTCi97W8Fgvv81sBL-lFiLqm1a2RG-Ub-OQP3rmjLHYCd-x9JitiZBhme7fGrSDTAAM--2XSL1jEad2UYTlYsHnVK9vdqhZwf06t7A_e2POn5vSrPEpz8fA5v4fL6S3lsvU0Q3rCWytCTLwOLrmsJ96yreViKuq_AbdV8E3tIZft-rWtxUYMFlY1ZZJFjT9YGFz-eldtvVovsLuHGGPPnyBGWSaRHxby4XO-s1P-9w7EGtLwXX8k74An5rVcVXJKlAWKiQ4__3H1zptO-8WRjBiSo6iiXGbpYGmfLsR8OUUJBcKpotlASuwW23vIcuq9E-Tx8yzLwrh8_Bq-v5HeWoCQrb0gnG5F99pbir-1m_n2zrNMgkOtiZrw2BbeaNoFXLUTPJMWUZYJUT9-ge-8byQIrAqO7LuXUerdZvAvuOOzwBzW1KP_Xtj_w49fKtVx6iBBJ_qgO4OnIeJu1e3WqFRkPd2g6BHAVTftCnhvei3W3nwJFLyVS5DrcC83Ei6qWOG5nrh4depnYRY-foFTbwlPzKdwFUB3v3z5hfcGVDCIh4XYXMuN10k1Uie33nxV4WWAk1618056_QIXoPsHC4wqWWSxfCI2bECB0BlPu-0d2ByGH7UMDz8HRl3JhfdGdMiEG9m0QMZVe4KCsq78NInCfTFyjSp8fiunaAst2m4HA70xCuSsi3v2ICduceLnQRQ01ROvjmi5af8uV5pgOLiYr-iKw4m_uZMbTWIgLzBjtWm7zrveiPXNCVqWcVhGon7q1b7zPlWj4TLruRXUcv1KytfeZleqy_81UK__S71z6naHSRwEIqufeLlfIpWm7Wpx5-lhe8n4d7lpB3Kgwqsw8ar5lmToCeI2eRHFIiqGqwWN_dWqlm_PZMnDx08wX5wldVr5yYNn_HblgfyS3paYiOSJ5joQd90EzAqtYFGokMMBg3ti6zXz21OUCPyqFvXD1-U-uwS2RyuonovrVQtWQAVKTay3cjPzvgI5vG3X0xrsWK9uqx2I5hPrqqsGdO4evT6TjYDlKKPK27QL2d1rFI69ceKc0jhPclE2j5m3lwgTsIbEArw6YNcaXJVFu0aNBEPsttIQ7OIUGQopZVlHj1nOu95Yx2fhOr-k6d95n2grd0-1m_-SYj-t0n0glowfs7qPQQupRyuxWHQe-J7Asm-BYKjAgac3qH6AYNc3ZAv1brBXnyJc7Psp-GB78kiCz3ULY4tNdTPfghrekdFyWvUceemUc5GFQZ3WwSNnJ2tRm9XuO_aq1S3-_3Qld9sNKG247XO4ZuCMyNNMVcsmzJNHru7q6grf_XHVtbtNJXHa9a77cfX__s__tdLI63YlGCZgoKnPdYiBzDL1Sb_OCrhgqAKFiGSeFU9ARWXUAC2b-QIXtV4vwPn34GrK6q6Cj9A3uwY7XIIoXdDDpE1OSc66aXI_GCroP2vN2htj8u1abua44Xv47J5XT7knsAmZhPGTrOSLHXHY4E1U2F530-4W4I-gCbt1D7hp5tUc_n3n7VPrp4mJzzwDfYSe4CUauyroQd-YCIq8LKoiq_1YlFUuq6IswiyvozDFK7RqtzSmDiF5OoTkVTeyer1u57QhmJFmwriI-QvDIj9h7Gkxr-6cEdx4lDMIRboeGKrq2mZ72cDJyM16M9cRsa4MLjIhy7gpyjoosyrIyyAv6jwuq8YvgzQPizLOi1BUiazr0C-ioon8OM9TeCfLojhFY78De4YiW-q0LsL8FyA0BpJCP0ynfj4Ni--D-MIPLuL4I9-_8DF4oCmOhxwmpQhlBkzTf_rzbxEMI45Vwaob0d0opyvOKz-IG5JHNIYTv9LM_NSBJz05hZ1E0AQluaU0uROLMpOfHVvSw_o-nG2ZZxL2boftw0162MeEj2iPMw8lm_4bviGPQjm7q3Y1VUFFsoVvSaXive5m3qfgKc9rJBpJOJB3FTwFphoQGCbZwgfdfAF_eHBYAoOqYFy-ldUO_umB4bDe4SPobvdL8TrUOWburfZ6wPhbzilc2Xnw7lJst_ihXtfdDJyMSq7Q9VWqQ5n4qy1aTa2y4WEmENrLNU653UhJq5UgebZzsdDL0EQD72urty_fVosdXBW0wpZgNczxY8WlsxGJblixkVEZyCyRxHp0bE4wrueGM4Nrelgh_DwJkjQIotoM68Tb9LCPip-N2W1yvRAgnk0Qh856T6qjD6FDO95nLR0cErsl21B9AWcGOgMMszuYUrldjsflIUV3Rld2dBo68GKCMdo7KXdb78hrvbPSSLQF7YyKv0EzbeT1vINPiVGcDVzjqXfgVKxNnAxDGkfiGDNFl2_Ea7KpjF_qOX4pDlFr61UJQVgo-sGKc6fGA_34u688Oi9NKlxmGE8r0eH78ORyvpqT99OJRm7vdFxgjRF_MFsWaOp2Ujtx5MWSXITvFlJgWmeClwRMO-VA6Ts0wTu0W-nr83d4ernbOoIA9o3bts61CUYs1wupBAcGoyqkMZ7T9aFnrSM9QNJNi0mFrYcZKiNZ8P6JLZoPmpSvbuZren4Nrp7r38M-58v5QvSH5FLrJUi7JQxTq-9FVe02orqbePXmbrrZrYCDcGPlfAEyYuKBjJnXaEYu51sUi1o6LuQU7xpw5d9UMA3e34FRh0LS_ZBYspbLNUyOJgpSXx-EOm73uDSjvMLJiOYw0xyPi4wWEGJILWBwxcXWBKJzAX5qF8j3lZGv6j6skO79Kbps2LvOLudh9HKDMVh6ceRm9q_h-PjqzRwuEFrDFRm58xYnrCmkuB8KgNXisNeLtoRnP_kmTCakf27pesHz6pspfuPhmlHk3gj6areag3BCYQ1vOCagHhnVRCVlrUmL-U2kODhvEmzHRa0OA8earwxbwmDEZgtwCbabO02dz46Q4st-1fDXV1u8mGC_1XgCg7kHBHEOZL5SckIFTnARIKTAH1d3BZcnbts5jtIT2eyDiG0WCiJsvlD69N2Yh2xVSh7XMooz8JOtSukTGr1Kec_EhB4-j_0ylr4okiQzwzu5CmtoPDzngNKPrrdS_N6SkgOjIQtrUxVx4ldxmuTW-HHSE1bdPSbNoGIoEgMG8HXg-zPf_6P7L3z2P4_pKW-jRFJYzIqYXotmQaLf-lOfQrATZP4so_HzcJYX-sFX92kzejzI8b04msU40wlOASapY_AoipxsRG2K2oyJc5QPzXyAclR6GE73zquVVMErACYYDtPAJSLp38dTzVZArgOjf-YEsGD5yj4D_VnTSHMyypo7smJRVOlCBuS8U-xSlIksm7IE_8fekD4Ro_f9mISKIHNJMXYJLh3e7p4zzB5f_Liawnh4O6ZvYC9KyGj9vQDxYDeqpeXwTS1RgI1rSWKlU6H19QLMWty60rSrdrMEffZ3rfq0-Lah22a-AWm4nq8lup5a-SxQQjpxE3rtyAZI7mJ2YU7GNFjXFHuBjavsDSqGrWJUq2CVcoEPNnPUbistvO-UvUWuwWwkKaXPL2riJAiLIK-qypyfk6dy-Pah-SbY_I5MnDltS-xZhPqI0AxUeyFFC2ILJL5A_sN40QppIPBlclROOAG5iOqkiZomrK1IddJaAyfgwRkp4xnklUyiupJ5Hpu5nCSVS7sH5pemWrGjjlcXdlpLuPA1eVlrdIpA14PUULp5BU8vnFAYRu1BWq5ANuw2fcJIW67bN611DJWfBpcMKR-kXtvgf4nYNdmcyhgiYxe1_wocNCQdTPE52aV9CJgsBLiJZJcBZ8B9k_M1GJ3fg0yxsWK8FMgpV_8SzIooTq9eKCOqzzz0GpxGpTeu_gUVRBheneCAqM7ypvGLMittUMBJxlkF9vA82taD2wsSRLlyx_Sdo_aMigReBmYni8fY7KDG4llK2imMZnlA__AnYZJ42_Y1iHY1AtkX2o4nSUTqL8ro8WSWpqQH84mfRoP3KP-mpNj1wPiCl4KIXkpmuRommhRFfuztgUV2cwf0qN21D0bJUjvKCY0ZZGFTFX4dVYF1150spCl7ekQCUV0KG6_w5GYDnE6KsmzhAljmn3kf1zUdtDJWYYu9FjLT4lhWWSodbRgDmKFBzQACWws6ddP1yrpjDqv21wa-KjinSs2Du1S3YPPifHog2KzlVrpZZrW4JeUfNhsJeggWg8LkwjOOgQlKdCYMrDIQjhc50YrWDLn3nFhP4ZvraxztxOWLg7IMpC_BKLDmgJOsdcTvWdlXPWrt53UNZrKQJMRpVCchq0d9TIZVkjDK_VkCNwmpOXCw0nyWhOpzx-cDSvf0UuRzBqBcl3l4qpw6unvWnTHxEfhmCqJy1ymnTZv6aPXRoojLtbl09YM_8fyfroB_2y3mZcBcBO7cwAJmrsAElqWixf6SnPT89NEbZqFXQANsb-ZwrZB-Bz7lzPur2Cy1PbcuEkU-sJdTtOWAR3Vsr8Msgc4MLgTFSPY8xuO8FCZ-GIRV6Ze5FRBOunsk1_2--evtc2N4YkIXbx9FGm1aiuJmWPIL0mCrgpEgOLbtcrpbawMTLjpsEt8xxrm9_UZY1HJJfiEa6SRWcGaVzaKAIUZhT5o0ZSD8MotkWJaGDk563Y1yn5ksN5c1BB0ZFmHcJPZaOfnzA_vlwdlwe6BVXIdlHUmR2o30CXKrmR-T7nbs7KEl_877jzfAiqBjvTD7ZAIK7fpGh2Hx4N85cXU3yUna9gVGT5Ssn3jXFAqB26yj7PMVOtY0uw3yCuARUC9w5tW-ZfGX2PtiAfQAdsHgB4zyd6nsM3j_LTzvqXSsDhTjSDpwNZxi2yp1h2wEmxSLsUk8dKPHIlv9gF9rT8HKBJ1NAO3_3fdTMC28Vy2O_ReVXfDQhNngg8pat4ExR88qm4dckrveoLY5iPF1fopW71Sx7lq_qxx1MCRgRbekwfsxyDCLZr4e4Iv5auRM3XeVnnF2_meVWTGZBdSFtQpTSYwowuABegnIeOh2DuIo5tkT9k1cZHlSgIUj87qPCNiCC83tjymfcK7gx195X8LBvhF3WvHBYCXIW1RF5byGk51532jHylrmNO_ETjSxb01gGRTGbjd74toKWdcJOCG7giarc6BEmBbWGHdKO1x37PwqDSNOyjRsmtqXddRYAveFG2707OlqMExgsCqKKKvLMmviXpTZsgw999NUWDjaGmSB-mwY93YDAur7sXi2zvKYQVXa0XvuqfS697ddfY1_OgmKmx3YtJ4qLVCv4XXfUtiid0jUN_SBElqKeUcMXvXkwJbsLSi9LnPDu7sV8Hs3N-t9i8kBsIlPJSt-XAHFRwpS9KGBS5gHBXjnQd57hn2NisMwDy03Advzbbtql2BNw_VoYMXb5zpjD_pjIbVVtJ9e1UcwA_VlzG_tNSu3W-VQhnygExNwAhhS6nOyV5o28spyOEjEeqr02JUllwSlqbIy_YOGyBOHCQbZGqAIXh_81CZltmpPuxUFDLet4hGwwogiJ2SDn8iibGJfgPtv7bu-KKeXDe9fWWNuqYzjIijqCkwOG1_vi230DI-pmMGdu7ev9yve3MwpfoqhHpK6wFa3gW_iXddIcIrP6FlUaHIhVDKJbt60ZxBTt4CBoCV6noPsLCawOjcfNV9ZHXqYOAZvd3UH7PNGG27LXbfVlt2dh4rcuE2ugumAM7YmDClgsTfAfOT0LnD6PvwH5i8wDLrjB0f_0y94NiMdXxJcWtvvRd7wBd7dt89-oh4y8vbHv93rFTv4lvxe-zVR9QKsuBuxqbGF7vfUVCZXt_NNu0JqX2K-ujvSW0abeGhrWVrmfpr6w26cl8oyopDGCoMY91S6jT1_srzND_Kskg-fE0XyUoDuXskpCjOSNKZ6A2PEGBsp4e1umB5Enh-paVN68Bhd9lahi9c-rk1ucrO_ck9venZs1-MjvtSs66meVVo_CgqTVejECkxXkMDPTYGMtVSNNJip7Rii_vzszQ2WyX0y3x-iJxYVLIGQ3o6RVFNSLajTImytLDMjw8xiNuLNdGxB71EymEZ-IzK_CuOqCDIp4yD06zyXlkZuLaBbB-fWB_7MfH6Mz8-v0DyoUPxlvP7wvmLMJ6m4zIXwQ6whLLK0AaMa_hP44EzFWVlHRR6kYVqnSRbUgczgzyYMIz-MIpk0ZZpXpTyyn7GCy_giLkYKLtOyqvMoC7jgkgsuueCSCy654JILLrngkgsuueCSCy654JILLrngkgsuueCSCy654JILLrngkgsuueCSCy654JILLrngkgsuueCSCy654JILLrngkgsuf2cFl1lRFGmax0Hh2zvkFMr0suHMwhczbFqBC1LIRPp1X2Vpa2GcU35obYsK8E9NEH4yEnKdDBzmqeMm9KyL6QLjNrp8MXViUMp9LO-8V3_6eBomqS6G0l7mN2LzmuxZKkPQcSWt3PtiK3ENV_HaJrTW-9nvF24RlVWHnXH9dETREQtO3QAuFWzgSrkQpnxALjEcLGvzroVa07D7XIXLVbjvV4V7rP72WOXt0Zrb32m17b0_4fCoMtv3xeMHw5C8vFNgrVFVwg2KhiiRt0GgDQFdpil0KhSDGveUN9737olSx6IJgxRMr6dZC6qGFUoX7e3a7KqxUB2FYCK7xtc8AfCZgNcb5HX5dItEr1HlYNxLea1qqahEQl9NfSVBQArwh05CrocibMqyeppFHskSB_CP4VBjMfSTSMFhndVR_IS0pHCbDr2NZFDBUdoKlbD4KJ4V-Xp99YL8hBO0DPw8zCTVB_eL_EIdxWHyTDRYXKcUQuBd33NZzh0GeOH01YmqKAlzET_5IpGoOP0UWRF1HR3PoEBCrEyyS1Ddl-HTxSmw4bqpsyDOn3y9GH2xwQVbdWezNPR-n4vAKh7iFWKMU6zq5zJM8rh-8gVTOMuUfNGirO-ko8XgqIgNfK5iYLe2iqQ6JQF8sMDrMg6ffL3foDXyCuZ77QWzkFauc7s2aY1rNGEMExQB56O9Pq9rwlFzh4rsoHHikDkPZce-rQyM2q6uO6wvUL0XOpGrKl_MU7NjivK-Xo6TEswUScyOqb57-jqoNsQNLb6Wcj3Rg5O5qMruqKYEzNTNoI1iVI-dMWMz5Bw7NljNLUahkF3RXjaVHfsFTWDq7TDhf0RJ3UdRzfFwlcmPBvrqBQ0kka6Kmh3TMedQ9ojOmNgEzURpZsMkyuM7rA8fJ7qjS-7bcnPsro7yjyP_z9hlFk6pABWHq2U3v145teV94LWTW8ymdBMbxlC7xVji7Jg4P7UvM8e0WwP5Gix2z_arYHUuVoV5df5PH785gr0TdkTzPXtHWfuvXS9Icedi0fdGUZYL02ZTKpmgFCSIs6VORM-OSdgzSL4nNpV3pqsXMYHsBmLtgnQEW0epK7ESGxMAP9KkpeY8WzAOro-ZFbxHOIfdShdDH2VEJdqXAi7dWzon2JO3W-NqqVr7RM8EHmVr42c26vVefV5FUeSiwqifX9ZpkVRl6UsZBMf6vGz7zf19XuxosaPFjhY7WuxosaP1P8XROr9Ler_NNfAnvYa7CH4Z72n9IE28dRWWZR4GQRjWsUhrP6vDoBEy8mWTyyj20yopyzipkryo0qAIwzitJWwsCPM4ac7b3UFLb3YRpBdxOtLSG9dB4Pt-yi293NLLLb0fuqU3hwFr8AEK0Bjc0vtbt_SeSxej_PZtWhtT6rtUbS8U3dm-Bk31-u45puPNdH1sL_vXbtC_s5fNVdSlsMchNW05wNgRbUiu7LV_qa41RWi7syXoaeMWTYZRvMP4nSAiGpGiDhoHUOV6tcsZcB-wtHGkiI_brbndmtutud2a26253Zrbrbndmtutud16rIY3r4IikKEf9cWUTsKil9gPSDqYqu04EmlVNlXQ2Kvu5CEckj00lzBXts9eL19fNw_XZILvAwtSITi2Nw9scGunb2-QX6h0E7PrpgjaFmi6XgB8syNzobfc59s9u7-yVaBzYE1SNzAmVmnacS2j9w2O3lefTUw6FGvFVc8SbKp7Izdu65KOJqjmOB1H0GW_5FUaI20yEr3ozYRTLXxVLIXImtCX9uyc9IzL7g9MsWhrXn-K9jAdVG_H64i31ujUGzpxQSTDlLrdwyzTnVyO_UNSMw7we_iv7Zuxx2Oy27gG7AbFg7EyE8i4Uh5JbzN0x4wGa2HcbzGEaRaXoAMy37dtL0426bTFcF5G6FexH6Js5lPHeT4L8xPmQxLPcjQvvDSaRe9hPmSZsjbI7MhOmw9hk8aBCKIQ6GbNhz7V5fYIPDBdVcAWDpt01ZPYxPtRANZOsl7_dGU7xq2XdV98RbVbaB_YKfk4CK_ABlCjb-TQKD0IYLpXDjaMXinZQ0pDqC4gEiEgOvbjiIzFwVgcjMXBWByMxfF7w-LI4zQOM5SLgfUVnVKJXvw-usZBT9jIWgQFqNW8jHtnwJY9ODL4ofUKtDKF74F9phuSm0N1aTJAU5DSQDyK1xPTdBf79r8RAbY2VDkoTqi354_ZWAf_l19_4yWzyPyJw7ggA7R63AyJ-GFzOshqgTOb5nOSzMpPQUuSrMj9RnQq58MLAsNmIeoF-K9SCEo7TDRYCBBioBn05YPXwjwftJujftjXDjDDN_uKIQHFkEWgGHpN8EZ02jO5BQFzihETETUiCLMgqW1YzykvsVrg4XUh8OcRg-sejeAohpHzPcATCMAkVTGwYBaRsJ2GMz9er-FfP0xRCaxB_aMl6INppwX3kEkOxwy1vQtjBqQ7psEsLfSY2SyMaUxggsCOeQ-UBTxLCgCGzmjEj4pZokf8KJxFAY0Y5LM4oSFPaQYsjijjJq7rqo-Z2kobfXaPKZFRB6wqaifw-Io2QbF3ddOpM7YlUQFuqHsT8RskLzbSatfXlvp6JEC0Zpp5ju5ScSJtTymsm5Uu4UXQmzdyYafuZbnZD2bfaJd7wWeq0Lc6AgQ8EHLewc5LcKGxZJdk11QNo15B-Sk7ZRjaF2Q3jAhWh5FuTKqbRA3GELEznQ5A03-lFLPq9LTn0IczcFPNbkPNmrawummrXadTpSeusszjCGszmqryLTv0hUyaHR5TgaT1badRMK7AIRZXFqPCqX-2OTpFGZDRtfFwdMGzUhHIMxNwa-r5bqlzKnuS-KutE0Gz4Y-Dwmoj8MaDZH2R-mxfbjuund7UddteL6SzLbPiTtVNe7oWmpG2GGmLkbYYaYuRthhpi5G2GGmLkbYYaYuRthhpi5G2GGmLkbYYaYt_7_afGIGrrECjCukf9OY6gg_Dogtlk292q9O9rqpI69TLJ9pbmyKL87rMnmYxTvUacTWmwENdLoMRAaPWMfxE1YWYB_r4u8__y3N7RA9aLku_EFVai6dZ5CBh4aaTRpIVw4TvzfxkI2tVAyPnT3SuH6tEGpWqzt96fcRuKahJRwkoMnQmVHSo8l-kad-35_pPYCSD5sK09L-_-vbPavMmrbiRwDcbdJ_FKT4_u3f6KSY7bModayL-VWYK0wpmSocAANpRxndqEuqDasb7ru-9b58gcVLkfpKRtf4Uy1FVjBQDRc9jt1qRBd3u1sNSTJ3h6Yg3r5YgScUTgj39hw2iqbKq0cT_AcaTbTZz-i4ookX6enZMBp8D7uRMO7zB4-A8jlC9BylGUjyLGJJsImxbciCWOls87eyJMs1T6waOAw85IvOeJYBJ2A9m6y8VXpApRu3tYwP70gj8RlBIWCWxlAG3D9XTy8R7lkF10-gJ7jpDbivl-lTEoLyCAvtrtBUPj-AQeOmQzV6C3VjKhWUzTEDgmVJyqJcYvaTYCLLftmAoeCt1x2zRxX3wTIfTf7oQG8Xlb27unCXY4gDdvNAnJVd78Th9WodIRQcASYezf6LjEP28dIwmZgX3Sf-8-wghZsck4n13qRctq5MiavxaObLuHAQzlWsMp20zLfaGt-WYyhSf6lKjbbs-ArP0SqJM20orEcBw0WXPR0UDZUMG--wrdAbLsXXN7jWfKi_DFQY6YQSrdKtHdVOXLfnRM9IWFQ3eD2apzMoYGciPZBGlflkkZVNHsX8MZslCIvw2MEtsTbM1zdY0W9P_BNb0-Xh4-5g3qQt5E_8yjmjzQQB9qjiKQcGkeZrmfhY0YdjUoGfiJA1l4Eu_KVJZBkHalHmTNBVKqiZMwiAq4M-SsvD3bu4Azye_SMKLuBjB8ynrLIjKJmE8H8bzYTyfD43nEwUh3P08z9O4YDwfxvNhPJ8Ph-dDR2mF19A9rsQtOIe_C8ifr1aW34bW_mSsnNxtHt6iYWW8dEMDCqxMNMeo4KCpGyZ_e-pW7bzQYPGUW-8rjW1HkinlcM5iKdHvnVcdnTadtHcscKcdd8WZDDbEYEMMNsRgQww2xGBDDDbEYEMMNsRgQww2xGBDDDbEYEMMNsRgQww2xGBDDDbEYENPDTaU5qISeVE1eWW7SZySGit-H1QWo-co8xIMvKQKi9iCTziVMm7S74HVLmSvId3hDbSstMR1vibJuuuGuhC31Bv_RNqJCuhV-7KmO-idxSMc6Vke9lCb0PQe2pALFqTQgZAlXYPU5OQOo9wS8Yf6JwOfKOUroT8zVXzm68T9FttUVDHpHPWQKnaEYTP9EHWxmKi2WcLUsYNRxy4pLo7rV1PRwNYfsMAkg_ZXMr9Hw99z1zF1YphOVoTMqIUpdLvP2czjsI6aNEzyzOp4p-JpDLToPauWxuSqUzJE0BLtuQhGZwAZER5QQQoDVYjWHIS34eiS0Ffa5Rh0Uf9EP4rVBlGsrGgvAnM6-uNRsKJ37hGd_YdyAIC5wuehw5qKc05pnBQERy38UlSVrYBw6sJMg_gjarvG04Rk6KTpLM3-6CIQTdxAvoGkcbMECN8ByoNuaF_DnORIU3zew39N1y1Y-hRSejHGN71AMivoe177eBnWYqnUn4nNDHZbgqOEvW29ehB1DbpE6kJuJ9PiFjV3coFRPxgN_mh1I_O1qS9R7areF4drNutCNwRdktUWbk6JOURXkTq3SmxVlM7-Bi3p5Yv-DjTilkxZV9-prB0yt_l2QH6q58WAGL2j9brNAOo03rwbYJ-giTAC_oRpGSwHglFLzNT3RR4boxpOgS0FKRhFYRUEsTwJ4HduSd37wflVlZ9Fvoj9LBOPgfOjOrZ212GBwwGyXw_pZ6pQHGQ_g9wHCpd4CclJJk4P-UQb1tEmkOk3oD8sQJ4Ljfe-CHh_at-gXTVRpS265M6yJ-UcKbMFWn2_nF4ZmldL8VperuSby7qtrmj6K3z6Ur4lmJtr-pycH7hfq92yRAAKdJ_dngHHK9WnONnPBuvZyURxfuz5HvXGmHz_uJh8IqiqIs_9UMbRr4_Jp9IOIGjHGjgehMWnIkUExtRhBHS0OcUARznNKZ5uLBK6XbxdIDSOfDM1z-qaObhl9iMlWpCSp0LHaVMmaZ7IqPSt9-KUFDvey0Oqgo37UuRBFaQIZmLdF6dQ2JGnD631lZfz1aWmzJX2QIZySFGoXckxYQRG_17zzEKtotVYb2jek1GCm1S-J_5FAGbaLu99ay3HhzJiYovPqD7ns28__S-dC6DhBqeGhYjt2uneU4AY3qvvPjbxedwDRrCUG06Sx60ZIfds-1whOTxXnSQe6IjqdWe8Xoo5jztSCyqXNDU3RkU49RDf4l0gHNb9viBX87zQ0GxHUFnpQoU0CkHWndBJI7Vu-rKcmZ0bL-3TGmVFORhtyd6nPhgHknEgGQeScSAZB5JxIBkHknEgGQeScSAZB5JxIBkHknEgGQeScSAZB_IfHQfyGALkMezHo6iPjPf4RAg1URimQZE-EZLJD8-f_3Th_cH7X215cRuEivzzyorCfzuBtiGrJg7SrNlbSeiZQVxrAYyX5Xp7P1jOPW-fQNvIqrj0Uz9-ouUcowzFeIDj_u3H1fduznlFeoN-vqvzTlEtSIIok82vvEzyMTq9SC1C7FqXAm7CW-_NiWXGCVgJdRr9ystUQksvU3mKuhpqST7B3rkfLDMqqiCKRPkrL7MPbCFJv6B4M3XCOl94T4dY2EOc2fKpw-0cIBY6CGQU1R-H8nPkxzjs2Vem7cMAFp4i5ji0miMZzoBWM3uEa6WrJHAn6K2oAB_Ytq0qm94QrsSRS38OiNv4PaAoLGlfCuwbK3CYzIHvq3a5j0jo3OYz5s9CBYQ4ZG_bZYb7nJboDm57wDX81cFjN3N8SoMuV-vEyAGjUkB10ASoF6TzPUcu2D0bdIK_-ipObOxOOSp7lbqqQEBnDBRIQHcEME9NMnYjXI_X5c85Zuwo4KtKgQkaU6PgDQ62m1j6D5sg3KukD8LiVSrSUQ-bE_K29v77QeT5WZVHYRRUeZDA7SzCLBNlVcTHIPIsytBvA5HHBggbIGyA_IMYIOejcZ7EQQt-GYc5-yAgb3FVBkkS1UUalSJO4zQVWZ3VZZoUWVPHUZ34YewLYGsZJ2VZN1kRVE2eVaGfNkktz9ncPshbGF742UWQj4G85U1YlnHEIG8M8sYgbx8a5C1IskQkMguyrGKQNwZ5Y5A3Bnn75wZ5-1rudb9UN23b6f6Yw6CK08Rj6htsAKZtsYXK-8r4zli2anDhlcerL_SNXNRuPYkhpz7V-4IpFuXoWEREV3TOqXfWlVgkpN4g3AZWI_fzw3nJtzdihxmHvgx5Sq3jFD5SYRXVFKI9ext-6fN0OvXmGNWm0UKL8nrQN8goe4yyxyh7jLLHKHuMsscoe4yyxyh7jLLHKHuMsscoe4yyxyh7jLLHKHuMsscoe4yyxyh7jLLHKHuMsscoe4yyxyh7v0uUvURUTRg3WehX1lByKl012z6kWtWkQMqgEmmQiiSz-QCngHWgtN-_BtWYe3EFblkpyzK2l88pS71nF2dVlgqvW6JkN_rIcpq7VDgiLFvAxP2qXSrUP5WLBf0_SDdf2Nbm6WjC2snCYTBBdQQAn9inEJcPjhs4kVK_rScW2Fd651zmTpqLALr2y76vQLGXzfqaLlxY6xXw1qXZ2ZUTMexzfSqQSDy4MoCKtkvbcjP2BmIoG_00TEOgk46JPtLFqq-B4AdUGF9_S9aMWRzZGPDMC-WSDKOgpg4NDZtK9lFeDU-G44NEMbfQsaJM7nshBR6qMmvpedtOAqR0r_upWHEc1YEvZJYUfeCqrzK-h-vOKhQG2T6iavd05hg0BZ7TEIBqouHK0IxSbQH7eFJHkRwsmJ4tiTMyW1UqYMJ50a6ubf2MHk8gDBpJKjCrXlFBlv6KkJ6wxV1HiWIKSWqmcK1V2qzaztcEU0Wbsl6afu9P33__3TB0YFsWTmCYWTwruy3zksDOYdNNi0AFGD2a9VWjQ26kAK1T2BOE2iFQVsPA-NaW8Uwdmo6B7L2ADpquBEFOtFEj1d2kKY8ShcyHYf2HK2TgTNp1vyeKlsOsGM-jbYtF1x7uHYgIt2Jr2oVNCwjYATChjrXR_jHrcl82JUtDURaJX6TWY3MK3O-5IWfVqI9FvDzlZClpM-Ye2c4jIGKPMWRd9gvET4UTgf_27emEYEcOUD1RVyVIIjo3-D8XUqUSm83dAPhkAK5AgQWQ9quOvO69gJdK1qPzQIUjsMgFYq8cLQzSxEDWuMC7fUVhuml05RR9aVcSidHrEl2eQrxrm5ax7brdbbY3vYzG2j1VU4Ei2tRJIuDC1rvCpy5VidGl5cMrxxFUt0u7WUo_wSKDQPO7aWbC83pBYg1f6J_T92LmfaK5Xsch1Kapgkq9YIAMQcvKvQknymlDhQkOmpObvqUsyjl-WlOLKM5FXJep9dOcBoh72PisHoZud41ACyrhZsjimBYmg-0GjPaSb1ghqSK5pANH7PXD_L9rRzqBpr7sbeZ9rBdjZ1Z-R-0Vk6yITTDuQMgFwST0A_qcJDiaLbsOw49xH37Eb4dmsC1V0dEv3Sun3-6fVdfx6qN0Fvnr9dXh_FcfZbM8MV_BEl6ouNxhDmMfoPU_jzbs0ZRTf5YlGtJ4Gszy9MoQf60kD8bTuzX6JnAT72zSoq-2q2VXbealtPIVL56WZsrjQDsSARHwiErpWWBKlcLeVRXIBKDFXv8iQ2kzlDZDaTOUNkNpM5Q2Q2kzlDZDaTOUNkNpM5Q2Q2kzlDZDaTOUNkNpM5Q2Q2kzlDZDaTOUNkNpM5Q2Q2kzlDZDaf--obQfBa54CGv5tKiIZ4z_KDjDM8Z_FA7hOeOPoX72I6jb-0hoz3HA5EPA4n4yi0FLH2BZjliYwPVGNBiErW6ojGzzGq0VyteCNQnOFeZ2aQr9DBUEgY9sFaiGT_MUN9ZHkWlJbFFR78m5ldx06vLxlX4pjlPkrqqzadb9db0fxmycyyqsw1QWTeNXIbgcUSwktY-MY8wakMP7MWb5Zv5T3MzzQYst2GYPsRlP7Dr2sUQtmuYHwRKVWVoWQeL7fgFnEhQVAhyEZRVHdZoXSQ0GdxEWEmyZKqqbED7PS7_2A3DU0zysyvO2N4YmWlwExQiaqMhyoF8gGE2U0UQZTZTRRBlNlNFEGU2U0UQZTZTRRBlNlNFEGU2U0UQZTZTRRBlNlNFEGU2U0UQZTZTRRBlNlNFEGU2U0UQZTZTRRBlNlNFEGU2U0UQZTZTRRBlNlNFEGU3094Am-kHAPmM_ETILhAh6OKFDsE9G8mQkz7ORPMERLuM8zv2kSY8jeTJQJwN1_g8F6ixzDEUHYSR6mXoI1Mk4nIzD-VvicIZBKpO48cs6EMdxOBlhkxE2GWGTETYZYZMRNhlhkxE2GWGTETYZYZMRNhlhkxE2GWGTETYZYZMRNhlhkxE2GWGTETYZYZMRNhlhkxE2GWGTETYZYZMRNhnH78Pg-I1DXjpHcfi-xrz8dCE2ysumTIc1iQ4hWnSNHMpdY3lZZa9K92bHDurc2ZU4GAaUjwO20FI6iRTYqkzs3gqcozy6gldrUE39CqiUSPe66ZIR7VZT4ZAWO9d9ySCBKx074KOzfi1Kacqcmr6-wtGeTu2hUH-1G-yevXOLMI6AiSqq3ulwK3pf-sCmqvxF_z77ZNDhMCQtLWKiy-VM0p4i5qoZxixBnT4iv-w6nWUfuguwNcQAAF7qB4fdUBkmrMmWZGqUU0zMrXZrjZbavR86qfTj3M-SAOEGyyDK40o2cU1oi6PopBY0kdFJf69S7Xz82TE8zV_GITI_CERoWOdxGjRVnqdlUZdFGpVpDKv1yyCMsihssrrKUpmFfpHnSSrjoIziBgxSv6nShkoTjmxpBBY08C-iMVhQv0pyGYCtybCgDAvKsKAMC8qwoAwLyrCgDAvKsKAMC8qwoAwLyrCgDAvKsKAMC8qwoAwLyrCgDAvKsKAMC8qwoAwLyrCgDAvKsKAMC8qwoAwLyrCgDAvKsKAMC8qwoAwLyrCg_yywoGkRgd0V5VXcJL8pLOhkv8yYEUL_8RFCyyLBds3El0XECKGMEPowhFBb_P8PDBVa52BRgtObJHHBUKG_I6jQvSYPBgzFaEzSBL70pTI0jgCGfu40qzQMHsrgoQweyuChDB7K4KEMHsrgoQweyuChDB7K4KEMHsrgoQweyuChDB7K4KEMHsrgoQweyuChDB7K4KEMHsrgoQweyuChDB76zwge6qAj9TByY6BLR5HjeuvWQtMJX2ZlKfeh6cBoNrCIBJJoOnxtmEfPQagMCA-nzIu-su7eAUautlkUeK5VUxJa2xMtSr1s4YSoPAaO4Ai4iEbx0jLhBLBf3YDRUVbh0y10vODcFAlhvwJ4SdSJiZHaISjLKQTFOMIIQfp0C3WyeCQonbagl6b_5xsMfvWZPZtMP8WQRQ72najKp1vpF4OysJF6Cgu04ZQUgK6--iiYnQcl61zMo6Cm3xnYGaUsju5nZH0GklTn2gfNOEoym3q42bG7vUccvaaP6_r-BZm-XWW96Ujb7Nh9HZ_opRbrNBdqJ6dRV-_NVI-hjdX2JRM4L7yragDC2bHbd8-06tocQudq_CAd6JNg8sOiKM-ksFEO0jPHLtUZ2x5LaqorM12gMvZ0TdzE3BideMQuLNNzPDt2Ve6Zf-2k0BF17rDuxc6KFenzdlgDp9JCcA5raa2VI-i6asqRHtkTHNbzt55yUPpxCE013opqSgr1hdAQZ4JUY3-wk_4wEQ-uAk0NKmGr-7nUFhdzrC1-T3TdMKtFKsAvrRqRlDLFZJaMm2PouhZ79H50XVb7rPZZ7f_Wav98NG0LTKzWdJFMHIji4JdxBOIPgrossySTCJ9cFmGaJvC_QJZClKIKgyDHnr20DvysblJfhsJvaozM5k0igjKJC_-szQ3wlyP_ez-4SJILPxrBXxaZqOMqzRh_mfGXGX_5Q-Mv-xFInir0ZREnjL_M-MuMv8z4y4y__LT4y-a8-xCLvYXW6X3Xd7UqeMTx3tYj_b6q3kBj31HTaqd_1cZmXo22cZttdUtvW25NPSIIMlFjuZgwgGdUvGl2pNu-TLvwwfFTUEqzIgZ4jv0oERWT6b7EKB1ARruO-8kSWQUZo0jrQMKMB81UfUvfUa6qNICNJFbs9ZecsZ8Z-5mxnxn7mbGfGfuZsZ8Z-5mxnxn7mbGfGfuZsZ8Z-5mxnxn7mbGfGfuZsZ8Z-5mxnxn7mbGfGfuZsZ8Z-5mxnxn7mbGfGfuZsZ8Z-5mxnxn7mbGfGfuZsZ8Z-_n3iv0MhoUQYRL7dWnLE5xOsKF5_JBOLlsoVDRBI2UTCmshO81dg-6ehzVn6X4HtAaQlVXbnJbbRrKW8kbcgplxARabXO15PUqqdRbugGZS_bVaTBkdpqaf9BJONYuoG6rHcXE_T9RfVrvNhvKm1q9zbrHjIR6ayG7FAKYxh4L-oKjU4DkPmml1K61EiYm0V5lZWmtf8YpUNzgyPRaM9iOkzcIj6CWWCSve1fG7dnM2aEwVVVWaBH6Q9qVkTled5pDHdMVZS2uYmNbNxI4CcgJ6xqQaw11VyWZlO8aH6vvFXhG0HYveSyhNlKSK5mQQdFq9Inh519trGFBYSMKO6UE4dGUs2lBY0Od1NwIBSa0pvmhFPfM-R-K4bzjmj71cQzvICYm6JlCf34po4dFefquvMN-zUCxRMbGVkQ7PgmPEomdo_CxF3FsVYDDZO0-FDgSlgK4Mg16Swr4kD62-dOXS1Quyo9Vtdq2GY4NcWaNVjea5o51gXRFEjS_isgFHzTpofZ_lYZjzvfskezWuNQmm03SixmRm-m8-3k_a2K8eHAZVknnE-njnRcWsoMBlNgmzPoFGkUb_8P8Hw46Far0on_kmledYBDhCluBIwSwOMvo7iqK9EbGCGlZYik7VmPVhVMqu5cnoAuE2DhaIbHdiy3E0SwuFsj6JssIdMsoL-n-zwiDN-iHHt5ua9e1tFy2IgMovCjMYWFV2sMOdxuEsjU_vNDE7DfPT5ZpBWpdBlQaxtKkopyHXYCk9oqG2IONMlzkeKb4AQXD1wzSdZYVCrfdnYYQVGLqpzwyuKeHMS3OksySzc9A4QaTGKWZ5jOO8AM05J_Gg1KROq9N4aHzrbjJVU6WKrszlxOeiZJYBvWGVzvZwZRHwQUhfHCxt5n1h7N73oVc2i1JnLx_59NMDuJcYzlzRRPddbTuir0_Pq3IXStEdUgnFLdAFyJrpnwUIZ1GhSlz295oGszAc22sSzNLg2F57V_ywTWdk-2TE9h62Vd-6dFeHKXrod4qaOIHlCRZd0m98oLJ7McgCj0eUe_NPrF6jekPpfPCjF4elnPybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKvybKk_zmyo__fL_Acqmru8)
