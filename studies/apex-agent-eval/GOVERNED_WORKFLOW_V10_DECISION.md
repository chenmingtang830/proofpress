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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZhZDMzM2RlNDQzZjM5MGM5MjBhNzNkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImJkNzEzYmY1IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iN2I0MDhlMjAzZTkzNjBiOTViZmQzNDAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY3MjYzNmJlZWNhMTNjMzE1ZWU3Y2ExNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfVl33MaS5l_BYfc9_eCqEvaFfpIt21c93lry-PY51z5kApkgYaGAagBFirb8Oj9gfuL8komIXJCojRTJ6-uZxgtFVgG5REZGfLHqtzPWDVXJiuGi4mfnZ5vNRcx4EARchGFQBplbZL7LkoCHZ4uzvOV3F7y6Ev0Az_bXzI_i88R1vSR1XdcPokgEbsiCSLDQy_zYY0UiBI-DkKeJ77m5lyWln6ReFMV5HAZJ7HEPxuVVX7Q3ors7O_8N_xguBnYFM9RswKkW8EsuavjgR9FVZcXyWjiduKn6qm2ca3i-7e6c_M75vmvbctOJvod3Nqx4x64Ebmrycdf-ImC72w4HvB6GTX_-4sVVNVxv81XRrl8U16JZV83VwJqrNHBfTN7uxH9tK_j9YtuL7qJom140QIuh24rfF2fXgiERc554QV5GZ_KTC3FDDwFxxUWe5KGbCt8NRBbEbp5FecmD0MWVtd2AW7uoq0bAyvWJ1Bdx4sdBnAtRMC8oAi8SIoFfY7kdtbqLgm36bQ0b9nGdRdvx_uz877-dqel_O4NTbrsef5NfC36RA8n_frZt3jXtbXP2M-xB8wMe8LDllehfsI14v4QFNcNS3LD6xVff_fjFm2-_eHXxt-_e_I8vv_7ubxc_eu7Fqy8-f_329Xffrtb8bPFRbMWGoavy7QCneZGzvupxblGXF6wHKg-CxtsO122Ha39XNThkf9cPYg3fNGyNh6z3sIBXe2SMs_NmW9ewo-IaTlJIWuR1W7yDp704zYvAD-BxOMRBvMf9foU82Aju_K3t3pV1e-vceO45cFV1A4zofC2uWO18ccPgJbUIxjmtboPcKG7hk39xHjpKvWW4Y-eVKIiRYZjhboNbQaYBBjz7fTEumIUxL3M_nyxYv-rk7bbhDO7PqZX9i3Po-VNzukUaxCl7_Jw_wOV01mLdOoohHeZsJCEWTg-XXPCFs265qJeM_wLcVsA33EEu245r27COTRZWlHmUBKU7WRhcfr4tBoerBfb3EOPQ8yeIkedR4PqZePycH8yU_7UFsYY0_DAeyQfgiYqLphBLoixQjPX4-U_NB2e5HBdHMmJKjqwIUpHEk6V9XrNqvUQJBcKpoNlASmzr4R6ynHrvBHncNEkSP8yfvoYfroWzYSBkueP5y4H175w1-6XtquHOMUyCQ22ImvDYAG-UbQ1X7QTPxFmQJIzxpy_wg_ONAIFVwJF9_yaInZsEfoM7vvL0YS0d-nlu_sGP30jVceogWZi7pSi85yHitum3G1Qqgi87FD0MuOq6bYD3llds41RroOCNWINch3vZCbiorMFzPXHxeOwmfuI_fYFLZw1PVEu4CqC737z50rkFFQzioWbdleicXsiRejE4VVPgZYCTbtqqF864wBp0_2SBQSGyJBTPxIYlKBA642U_3AHm0PyoZLj_BTBqI2rnlvXIhJ0oWyBj056goOCFG0eBvytGrlCFVzdiiViobvstDHSrFciDLu6DBzlxiyM39QKvLJ55dUTLrv1VNIpgODirGrricOK3d6JTJAbyAjMWXdv3zlXHNtcnaJmHfh4w_tyr_eB8LkfDZfLKCGqxeSvEO6fb5vLyfw3UG_-S75y63X4Ueh5L-DMv9yuk0rJt6jtHDTtKxl9F107kQIFXYeEU1UAy9ARxyzQLAMpn09WCxn7dcPH-gSy5__gJ5guTiMeFGz16xu8aB-SXcAZiIpIniutA3PULgBVKwaJQIYMDBnfY4JTVzSlKeG7BGX_8uuxn18D2iIJ4xa6aFlBAAUqNbQbRrZzXIIeHdrPkgGMd3hZbEM0n1sWLEnTuDr1eiZLBciSocrq2Fv29oPDQGyfOKQ7TKGV5-ZR5R4mwADTEarDqgF05mCp1u0GNBENsB6EJdn6KDJkQIufBU5bzYQTr-Cxc5zc0_QfnM4Vyd1S7_kmK_bRKd4FYInzK6l6CFpKPFqyuewdsT2DZ90AwVODA0x2qHyDY1TVhodEMdvgpwoWuG4MNtiOPBNhcNzA264rragA1vCXQclr1HHnplHGR-B6PuffE2QktKlhtv2OuGm_x32UjtkMHShtuewXXDIwRcZqpuCj9NHri6i4vL_Hdn5q-3XaFwGk32_6n5v_8r_9tpJHTb3MAJgDQ5OfKxUCwTH4yrrMALpiqQMYCkSbZM1BRghqgZVnVuKjNpgbj34GrKYq7Aj5C2-wKcLgAUVrTw6RNTklOXpap600V9LdKs45gTLzfiK7CDd_DZ_e8eso8gU2IyA-fZSVfbonDJm-iwnb663Zbgz2CEHawD7gsq6KC3--cXWr9vND-mTPQR2gJXiDYlU4P-kZ7UMRFVmQJd0OWF6kosjzzk5QHfoxXqGkHGlO5kBzlQnKKa1G827QVbQhmpJnQL6L_QrfIz-h7qqvizhrB9kdZg5Cn65Guqr4th4sSTkZ0m65SHrE-984TJvKwzHLu5UnhpbmXZjwN86J0cy9O_SwP08xnRSQ4990syMrADdM0hneSJAhjBPs94BnybMnTOvfT34HQ6EjyXT9euunSz37wwnPXOw_DT1z33EXngaI4HrIf5cwXCTDN-Olv_wxnGHGsdFZds_5aGl1hWrheWJI8ojEs_5Vi5ud2PKnJye3EvNLLySylyS1flJ78wb4lNazrwtnmaSJg72bY0d2khn2K-4j2uHJQsqm_4RuyKKSx27TNUjoVCQvfkErFe92vnM_BUq44Eo0kHMi7Ap4CqAYEhkkG-KCvavjDgcNi6FQFcPleFFv41QHgsNniI2huj0txetQ5eu5BWT0A_tYVuSt7B95ds2HAD9W67lZgZBSiQdNXqg4J8ZsBUVMrMTzMBEJ7vcEph04IWq0AyTNUrFbLUEQD62tQ2xfvi3oLVwVR2BpQQ4UfSy5dHZDomhVLEeSeSCJBrEfHZjnjRm54oHNNDcuYm0ZeFHtewPWwlr9NDfsk_9kh3CY2NQPxrJ04dNY7Uh1tCOXacV61dHBI7JawofwCzgx0BgCzO5hSml2WxeUgRbdaV_Z0Gsrxop0xyjrJt4Nz5LXRWCkFYkEzo-Rv0EyduKp6-JQYxdrAFZ56D0bFRvvJ0KVxxI-xknT5hr0jTKXtUseyS3EIrtCrFIKwULSDJecutQX68vvXDp2XIhUu0w-XBevxfXhyXTUVWT89K8Vwp_wCG_T4A2ypEer2QhlxZMWSXITvasEwrLPASwLQThpQ6g4t8A5tG3V9foWn19vBEgSwb9y2Ma61M2K9qYUUHOiMKpDGeE5X-5a18vQASbsWgwqDgxEqLVnw_rEB4YMi5dvrakPPb8DUs-172Ge1rmo2HpJNrTcg7dYwDJffs6LYdqy4Wzi8u1t22wY4CDeWVzXIiIUDMqbiCCPX1YBiUUnHWizxrgFX_iKdafD-FkAdCkn7Q2JJLtYbmBwhClJfHYQ8bvu4FKO8xcmI5jBThcdFoAWEGFILGFxysYFAdC7AT22NfF9o-SrvQ4N0H0_RZsPRdLY5D72XHfpg6cUDN3N8DcfHV68ruECIhgsCuVWLE3JyKe66AmC1OOxV3ebw7Gff-NGC9M8NXS94Xn6zxG8cXDOK3GtGX22bCoQTCmt4w4KAamRUE4UQXJEW45tIcTDeBGDHmsvDwLGqRrMlDEZsVoNJMHR3ijqvjpDiq3HV8NfrAS8m4DeOJzCZe0IQ60CqRsoJ6TjBRYCQAntc3hVcHrtpKxxlJLLeBxFbLxREWFVLffrhkIVsVEoachGECdjJRqWMAY1RpXxkYEINn4ZuHgqXZVGU6OGtWIUBGo-POaD0o-stFb-zpuDAQZeFwVRZGLlFGEepAT9WeMKou6eEGaQPRaDDAL72XHflun-xf8Nn_-cxPeV0UiT52SoL6bVg5UXqrb-OIQQzQeKuEho_9Vdpph58e582o8e9FN8Lg1WIM53gFGASHoJFkaWEERUUNRET6ygfG_kA5Sj1MJzuncOlVMErABAMhynhEpH0H_2peisg14HRX1kOLFi-xGegPzmNVBEoK-8IxaKoUokMyHmn2CXLI5GXeQ72j7khYyBG7fspARVGcEkydg4mHd7ukTP0Hj_9qVnCeHg7lrewFylklP6uQTyYjSppOX1TSRRgYy5IrPTStb6pAdbi1qWmbdpuDfrsV6X6lPg2rtuy6kAabqqNQNNTKZ8aJaTlN6HXjmyA5C5GFyoC04CuyfcCG5fRG1QMg2RUo2ClcoEPugq1W6OE953EW2QarA4EpdT5BWUYeX7mpUVR6POz4lQW3z423gSb3xLEqWhbbAcRqiNCGCj3QooWxBZIfIb8h_6iBmnA8GUyVE4YASkLeFQGZelzI1KtsNbECHh0REpbBmkhooAXIk1DPZcVpLJp98j40lIpdtTx8sIuuYALz8nK2qBRBLoepIbUzQ08XVuuMPTag7RsQDZsuzFgpJDrcNsaw1DaaXDJkPJe7LQl_iRic8KcEgwR2EXt34CBhqSDKb4gXDq6gAkhwE0kXAacAfdNVBsAnT-ATDG-YrwUyCmX_-qtsiCMLz-VIGqMPIwanEalNy7_FRWE71-e4ICAJ2lZulme5MYpYAXjjAJ7fBxtcOD2ggSRptwxfWepPa0igZeB2QnxaMwOaixcxaSd_GCVevSLu_CjyBnadyDa5QiELxSOJ0lE6i9I6PFoFcekB9OFGweT9yj-JqXY1QR8wUteQC9Fq1QOEyyyLD329gSRXd8BPbi99skoSWxGOaExvcQvi8zlQeEZc92KQuq0pycEEOWlMP4KR3QdcDopyryFC2CYf-W85JwOWoJV2OKohfS0OJZRllJHa8YAZihRM4DAVoJO3nS1sv6YwarstYmtCsapVPNgLvEWMC_OpwaCzRpupZulV4tbkvZh2QnQQ7AYFCbnjjYMtFOi125gGYGwrMiFUrR6yJ3n2GYJ31xd4WgnLl_o5bknXAGgwMABK1hrid8HRV_VqNxNOQeYzAQJcRrVCsiqUZ8SYRUkjFJ3FcFNQmpODKw4XUW-_Nyy-YDSI70k-awBKNalH15Ko47unjFntH8EvlmCqNz20mhTUB9RHy2KuFzBpcu_uwvH_fkS-LcdMC4DcBG4s4MFrGyBCSxLSYvjJTlp-amj18xCr4AGGK4ruFZIvz2bcuX8jXVrhec2WSTJB3g5RiwHPKp8ez1GCVRksGbkI9mxGI_zkh-5vucXuZunRkBY4e4Dse6PjV8PLzTwxIAu3j7yNJqwFPnNMOUXpMEgnZEgOIZ2vdxuFMCEiw6bxHc0ODe3XwsLLtZkFyJIJ7GCM8toFjkM0Qt7EtLkHnPzJBB-nms6WOF128v9wGC5vqw-6Eg_88MyMtfKip_v4ZdHR8PNgRYh93MeCBabjYwBcqOZnxLutnD2FMl_cP7jFlgRdKzjJ58tQKFdXSs3LB78B8uvbgc5Sdt-it4TKesXzhW5QuA2Ky971aBhTbMbJy8DHgH1Amde7CKLH0PnyxroAeyCzg8Y5Vch8Rm8_x6ed2Q4VjmKcSTluJpOMbRS3SEbwSZZfWgSB83oQ56tccCvlaVgZIKKJoD2__6HJUAL522LY_8oowsOQpgOH5Ro3TjGLD0rMQ-ZJHcjoDYxiMPr_BxR71Ky7ka9Kw11ABKwohvS4OMYBMyClasG-LJqDpyp_a7UM9bOv5WRFR1ZQF3IpZtKoEcRBvfQSkDGQ7Nz4kfRz57AN2GWpFEGCEekfPQImIQLxe1PSZ-wruDL185XcLC37E4pPhgsB3mLqiivOJzsyvlGGVYGmdO8CzPRwry1gGWQG7vtdsS1EbK2EXBCdnllwlOghB9nBoxbqR22OfbwLA0tTvLYL0vuCh6UhsBj4obtPXu-HAztGCyyLEh4nidlOIoyk5ah5n6eDAtLW4MskJ9N_d62Q0B-f8ifraI8elAZdnReODK87vyy5Vf4pxWguN4CpnVkaoF8Da_7QG6L0SCR39AHUmhJ5j0AeOWTEyw5Iii1Ln3D-7sG-L2v9HrfY3AAMPGpYMVPDVD8QEKKOjQwCVMvA-vcS0fLcMxRsRjmsekmgD3ft027BjQN16OEFQ8vVMQe9EctFCraDa-qI1iB-tLwW1nN0uyWMZQpH6jABJwAupTGmOyloo24NBwOEpEvpR67NOQSoDRlVGZ8UBN5YTHBJFoDFMHrg5-aoMwg97RtyGE4tJJHAIURRU7IBjcSWV6GLgPz3-C7MSlnlA0fn1mjb6kIw8zLeAGQw_jXx2QbNcNTMmZw5_btG-2K2-uK_Kfo6iGpC2x147na33WFBCf_jJpFuiZrJoNJdPOWI4PovAV0BK3R8pxEZzGA1dvxqKoxOnQ_cAzWbnMH7HOrgNt62w8K2d05qMi12WQrmB44Y9BuSAaLvQbmI6O3xulH9x_AX2AYNMf3jv7n3_FsDlR8CTBpTb0XWcPneHffn_1MNWRk7R_-dqdWbO9bsnvN10TVc0Bx16zjWEL3ZyoqE81N1bUNUvsC49X9kdoy2sRjS8viPHXj2J1W47yRyIhcGg06Me7JdDv0_Mn0NtdLk0I8fk4UyWsGursRSxRmJGl09gb6iNE3ksPb_TQ8iDx_IKdN6sFjdNlZhUpee8l1bLLbXbmjNr06tuvDI75RrOvImlVaPwoKHVXoWQPQFSTwC50gY5CqlgYruR1N1N_Obq8xTe6zaneIkViUsARCejhEUkVJuaBeibCNRGZahunFdOx2eWhBH5EyGAduyRK38MMi8xIhQs93eZoKQyM7F9DOg7PzA3-b-fwYnz88Q3MvQ_H3w_mH9yVjPkvGZcqY62MOYZbEJYBq-OG5YEyFSc6DLPViP-ZxlHjcEwn8Wfp-4PpBIKIyj9MiF0f2cyjhMjwPswMJl3Fe8DRIvDnhck64nBMu54TLOeFyTricEy7nhMs54XJOuJwTLueEyznhck64nBMu54TLOeFyTricEy7nhMs54XJOuJwTLueEyznhck64nBMu54TLOeFyTricEy7nhMs_WcJlkmVZHKehl7nmDlmJMqNseGDiix42LsAEyUQkXD5mWZpcGOuUH5vbIh38S-2EXxxwuS4mBvPSMhNG1sVwgTYbbb5YWj4oaT7md87bv75c-lGskqGUlfkN694RnqU0BOVXUsp9TLZiV3AVr0xAa7Mb_f7UTqIy6rDXpp_yKFpiwcobwKUCBi6kCaHTB8Qa3cGC63dNqzXVdn_Owp2zcD8uC_dY_u2xzNujObd_0mzbe_8Lhyel2X5sP34AhmTlnWrWGhQ53KBg2iXyxvMUEFBpmkyFQtGpcU96433vnkh1zErfiwF6Pc9aUDU0KF2UtWuiqxqhWgpBe3a1rXmiwWcEVq-X8vz5FolWo4zB2JfySuZSUYqEuprqSoKAZGAPnWy57jO_zPPieRZ5JErswS_ToQ750E92CvZ5woPwGWlJ7jblejsQQQVDaWAyYPFJuMrSzebyU7ITTtDSc1M_EZQfPC7yS3kU-8EzVmJynVQInnN1z2V56DDAC6evTlAEkZ-y8NkXiUTF6ZfIiqjr6HgmCRKs0cEuRnlfmk_rU82GeckTL0yffb3ofTHOBZN1Z6I09P4Yi8AsHuIVYoxTrIr_gVGUhvzZF0zuLJ3yRYsytpPyFoOhwjr4XPrAbkwWSXFKAriAwHke-s--3m8QjbyF-d453sqnlavYrgla4xq1G0M7RcD4aK8eVjVhqbl9RbZXOLHPnPuyYxcrA6O2zVWP-QWy9kIFcmXmi35qdUxR3lfLcVKC6SSJ1THVd09dB-WG2K7Fd0JsFmpwgosy7Y5ySgCmdpMyioN67AEzllPOMWMDam7RC4XsinhZZ3bsJjQB1NtiwP-IkrqPoorj4SqTHQ30VQuaSCKVFbU6pmMeQtkjOmNhAjQLqZk1k0iLbz8__DDRLV1y35bLY3f1IP9Y8v8Bu0z8JSWg4nBc9NVVY-WWj47XXgwYTekXxo0hd4u-xNUxcX5qX3qOZb8B8pWY7J7sZsGqWKx086r4nzp-fQQ7J2yJ5nv2jrL23_pRkOLOWT3WRlGUC8NmS0qZoBAkiLO1CkSvjknYB5B8R2xK60xlL2IA2XbEmgUpD7byUhesYZ12gB8p0pJzPlgwTq6PnhWsRziHbaOSoY8yohTtawaX7j2dE-zJ2W5wtZStfaJmAo-yNf4z4_X6qDqvLMtSVqDXz815nEVFnrtCeN6xOi9TfnN_nddsaM2G1mxozYbWbGjNhtb_L4bWw6ukd8tcPXcxarhz7_fDNa1_SBEvL_w8T33P830espi7Cfe9konAFWUqgtCNiyjPw6iI0qyIvcz3w5gL2Jjnp2FUPmx3eyW9ybkXn4fxgZLekHue67rxXNI7l_TOJb1_dElvCgNysAEy0BhzSe8_u6T3oXTRym8X0xqf0lilamqh6M6OOWiy1nfHMD1cTDf69pJ_6yf1OzvRXEldcnvsU9OkAxw6oo7kyk75l6xak4Q2O1uDntZm0WLqxdv33zEiohYp8qBxAJmux23OgPuAqY0Hkvjmcuu53Hout57Lredy67ncei63nsut53Lrudz6UA5vWniZJ3w3GJMprYDFKLEfEXTQWdthwOIiLwuvNFfdikNYJHtsLKGS2Genlm_Mm4drssD3gQUpERzLmycY3OD04Rr5hVI3Mbquk6BNgqZtBcA3W4ILI3Kvhh3cX5gs0ApYk9QNjIlZmmZcw-hjgaPz-tVCh0MxV1zWLMGm-lvR2aVLypsgi-OUH0Gl_ZJVqUHa4oD3YoQJp0r4ilAwlpS-K8zZWeEZm90fGWJRaF59iniYDmrE8crjrTQ61YYu7CaSfkzV7n6SqEouC_-Q1Aw9_B5-mroZczw6uo1rwGpQPBgjM4GMjbRIRszQHwMNBmHcjxj8OAlz0AGJ65qyFyuadBoxPCwi9A_BD0GycqniPF356Qn4EIWrFOGFEwer4CPgQ5JItEGwIzkNH_wyDj3mBT7QzcCHMdRl1wg8MlyVwRb2i3Tlk1jE-4kHaCfabH6-NBXjxsq6z78iyy2UDWylfOy5V2ADqNE7MQWlew5M-8rBhtEqJTwkNYSsAiIRAqJj14849-KYe3HMvTjmXhxzL44_Wy-ONIxDP0G56Blb0UqVGMXvk3Mc1ISl4MzLQK2meTgaAybtwZLBj81XoJXJ_h5YZ9qR3JyqSx0BWoKUBuKRv56Ypj_fxf9aBJjcUGmgWK7ekT9Whyr4v_r6GydaBfpPHMZuMkCrx82QiJ8Wp4OsZjizLj4nySztFESShCJ3C9EpnQ8vCAyb-KgX4KdUCFI7LFSzECDERDOoywev-Wk6KTdH_bCrHWCGb3YVQwSKIQlAMYya4Jb1yjK5AQFzihEjFpTM8xMv4satZ6WXGC3w-LwQ-PMI4LpHI1iK4cD57vUT8ACSSh-YtwpI2C79lRtuNvDb35eoBDag_hEJugDtlOCeMsn-mL7CuzCmR7pj6a3iTI2ZrPyQxgQm8MyY97SygGdJAcDQCY34SbaK1Iif-KvAoxG9dBVGNOQpzYDJEXlYhpwXo8_UZNqos3tKiow8YJlRu4DHG9oE-d7lTafK2JZEBZih9k3Eb5C8WEirTF-T6uuQAFGaaeVYukv6iRSekr1uGpXCi01vbkVtph5lud4PRt9olzvOZ8rQNzoCBDwQsuph5zmY0JiyS7JrKYeRr6D8FL0EhuYF0U89gsW-pxuD6jpQgz5ErEynA1D0b6RilpWe5hxGdwZuqtx2VKxpEqvLttj2KlR64iqLNAwwN6MsCteww5jIpNjhKRlISt_2qgvGJRjE7NL0qLDyn02MTlIGZDTXFo5KeJYqAnlmAWYNr7ZrFVPZkcSvB8uDZtwfe4nVWuAddpKNSeqrXbltmXZqU1dte1ULa1t6xb3Mm3ZULvTcaWvutDV32po7bc2dtuZOW3OnrbnT1txpa-60NXfamjttzZ225k5bc6etudPW_P_d_jfuwJUXoFGZcPdqcy3Bh27RWmLybtucrnWVSVqnXj5R3lpmSZjyPHmexVjZa8TVGAL3VboMegS0Wkf3E2UXYhzo5fdf_Kdj14julVzmbsaKmLPnWeQkYGGHkw4EK6YB3-vqZCFrwYGR02c615cykEapqtV7Z_TYrRkV6UgBRUBnQUmHMv5FmvZja67_CiAZNBeGpf_97Xffys3rsGIngG86NJ_ZKT5_cO30c0y2X5R7qIj4HzKTHxcwUzxtAKAMZXyHk1CfZDPed33vffsEiaMsdaOE0PpzLEdmMZIPFC2PbdMQgm63m2kqporw9MSbl2uQpOwZmz39h3GiybSqg4H_vR5PptjMqrsgjxbp69UxGfyQ5k7WtNMbfLg5jyVU7-kUI8ifRQxJmAjLlqwWS71Jnrb2RJHmpTEDDzceskTmPUsASDgOZvIvZb8gnYw64mPd9qVk-A0jl7AMYkkAt9uqZ5SJ9yyD8qbREtz2mtxGyo2hiEl6BTn2N4gV949gv_HSPpu9AdyYi9qwGQYg8EwpODRKjFFSdIzw2wBAwWnkHTNJF_e1Z9qf_vOadZLLb6_vrCWY5ABVvDAGJZsdf5w6rf1ORXsNkvZn_0z5IcZ56Ri1zwruk_rv3Q8QYnVMIt53l0bR0pwUUYevlSXrHtLBTMYa_WVbLrOd4U06poTiS5VqNLSbI22W3gqUaYMwEgGAi0p7PioaKBoy2eeYoTNZjslrtq_5UloZtjBQASNYpZ09qoq6TMqPmpG2KGnwcW2W8iQPkYHcQGRB7OZZlJc8CN1jbZZMS4R_TpulGU3PaHpG0zOa_m-Aph_eD2-3501st7wJfz_c0eYPaehThEEICiZO4zh1E6_0_ZKDngmj2BeeK9wyi0XueXGZp2VUFiipSj_yvSCDP3OKwt-7ub1-Pul55J-H2YF-PjlPvCAvo7mfz9zPZ-7n80f38wk8H-5-mqZxmM39fOZ-PnM_nz-unw8dpRFeU_O4YDdgHP4pWv68bgy_TdH-4lA6uV08PCCw0la6pgE5VhaKY6RzUOcNk729tLN2PlXN4im2PmYam4okncphncVaoN1bFT2dNp20c8xxpwx3yZlzs6G52dDcbGhuNjQ3G5qbDc3NhuZmQ3OzobnZ0NxsaG42NDcbmpsNzc2G5mZDc7OhudnQ3Gxobjb03M2G4pQVLM2KMi1MNYmVUmPE76PSYtQceZoDwIsKPwtN8wkrU8YO-j0y24XwGtId3kBkpSSu9TVJ1m0_1YW4pRH8E2kX0qFX7Mqafq92Fo_wQM3ytIZau6Z3ug3ZzYJkdyBkSRuQ6pjcvpdbYP-h8UnPJUq5UuivdBaf_jqyv8UyFZlMWqEeksmOMGyiHqIqFu3V1ktYWjgYdeya_OK4fjkVDWzsAdOYZFL-SvD7oPu7sg1Ty4dpRUUIRtU60e0-YzMNfR6UsR-lidHxVsbToaZFH5m1dEiuWilD1FqifWgHowc0MqJ-QBkpDFQhSnNQvw1Ll_iu1C7HWheNT4yjGG0QhBJFOwHA6eAvR5sVfbCP6MF_SAMAmMt_4VusKTnnlMaJQXBw5uasKEwGhJUXpgvEn5DbdThMSEAnjldx8he7A9HCduTrljR2lADbd4DyoBs65jBHKdIUn3fwt-WmBaRPLqVPD_HNKJD0Csaa19FfhrlYMvSnfTOT3eZgKGFt26geGOegS4RK5LYiLXZScy9q9PrBaPBHqwqZr3R-iSxXdb7cX7NeF5ohaJI0A9ycHGOItiK1bhUbpJfO_B-0pJfPxztQshuCsra-k1E7ZG797YT8lM-LDjF6R-l1EwFUYbyqn_Q-QYhwoPkThmUwHQhGzTFSPyZ5dFo1nGq25MUAivzC80JxsoHfQ1PqPq6dX1G4SeCy0E0S9pR2fpTH1m57THDY6-w3tvTTWShWZz_duQ8ULvESkpMgztjyiTasvE0g069Bf5gGeXZrvI_tgPfX9hZx1UKmtqiUO8OeFHOkyBZo9d10egk0L9fsnbhoxO0Fb4tLmv4Sn74Q76nNzRV9TsYP3K9mu86xAQWaz3bNgGWVqlNc7EaD1ewEUaz_7Pke9Tb35Pt_tycf84oiS1PXF2Hwj-_JJ8MOIGgPFXA8qhef9BRRM6YePaAHi1N04yirOMVRhUVMlYu3NbbGEbdL_azKmYNbZj6SogUpecp1HJd5FKeRCHLXWC9WSrFlvTwmK1ibL1nqFV6MzUyM-WIlClvy9LG5vuKiai4UZS6VBTKVQ5JCbSMOCSMA_TvFM7VcRat6vSG8J1CCm5S2J_5FDcwULh9tayXHpzJiYZLPKD_n1Xef_6eKBdBwk1PDRMR2Y1XvyYYYztvvX2r_PO4BPVjSDCfJY-eMkHk2vJCdHF7IShIHdETxrtdWL_mcDxtSNaVL6pwbrSKsfIjv8C5QH9bduiBb83yqWrMd6cpKF8qnUahl3QmddCDXTV2WB0bnDqf2KY3SUAxGIdn71MfcB3LuAzn3gZz7QM59IOc-kHMfyLkP5NwHcu4DOfeBnPtAzn0g5z6Qcx_IuQ_k3AfyT90H8uff_y-KlG6a)
