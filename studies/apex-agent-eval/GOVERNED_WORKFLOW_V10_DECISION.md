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
| Make progressive disclosure the default agent-facing matter-context API | Promote | The 24-case deterministic safety panel passed all cases with zero blocked leakage, automatic admission, or unauthorized mutation. The 12-ask workflow panel completed every cell and graph-only context was the strongest tested graph treatment. |
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

[//]: # (ob:10827ee7)
## Formal 12-task Legal E2E after the v11 gate

[//]: # (ob:3c3528a4)
The gate-passing v11 construction ran across all 12 formal legal tasks under two preregistered decision-relevant contexts: frozen PR36 v7 prefetch and v11 claim-graph-only disclosure. DeepSeek V4 Flash, GLM 5.3 Flash, and Qwen 3.8 27B all ran with high reasoning. Each artifact received three blind Gemini 3.1 Pro grades. All 72 of 72 cells scored, zero were inconclusive, and all 288 model calls had terminal receipts. Model cost was `$5.9373`; PageIndex was not invoked.

[//]: # (ob:ddfd7148)
| Executor | PR36 v7 context | v11 graph-only | Paired delta | 95% bootstrap interval |
| --- | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash, high reasoning | 13.34% | 11.30% | -2.04pp | [-9.37pp, +4.90pp] |
| GLM 5.3 Flash, high reasoning | 12.85% | 11.16% | -1.69pp | [-7.24pp, +3.11pp] |
| Qwen 3.8 27B, high reasoning | 3.17% | 12.76% | +9.59pp | [+2.31pp, +18.45pp] |

[//]: # (ob:08e2584d)
Qwen was the only executor with a clearly positive paired context signal, winning five tasks and losing none. DeepSeek and GLM confidence intervals crossed zero. Graph-only still scored zero on seven of twelve tasks for every executor, so the construction repair does not establish absolute legal-execution readiness. It establishes a promotable claim-construction path and identifies Qwen as the next primary executor candidate for further executor-focused work.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZhZDMzM2RlNDQzZjM5MGM5MjBhNzNkNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjRkMTEwMDA2IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85OTk4YWMzZTg3MGJkNjk1Y2JiMGVlMTEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY3MjYzNmJlZWNhMTNjMzE1ZWU3Y2ExNiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVtz20aW_isozWzNQ0ga94vylMRJxrVxkrWzyUPikhrdDQoxCGAAUDJj-3V_wP7E_SV7Tt_QpEhIlrQzqS28yBKJPt19-ly-c2n4_RnphrIgdLgo2dn5WdtexIQFQcB4GAZFkLk0812SBCw8W5zlDdtdsHLN-wGe7a-IH8Xn1CtYTP2IEpp6xE9jL45D6gbwt-vFLC5oFlDqJzFjLgvdkHuZl-ZpEec582M3B7qs7Glzzbvd2fl7_GO4GMgaZqjIgFMt4JecV_DBz7wri5LkFXc6fl32ZVM7V_B80-2cfOf82DVN0Xa872FMS-hbsua4qb2Pu-Z3Dtvddkjwahja_vzZs3U5XG3zFW02z-gVrzdlvR5IvU4D99ne6I7_Y1vC7xfbnncXtKl7XgMvhm7LPy7OrjhBJobM81zXjc_kJxf8WjwEzOUXWZalhAY8TdycxVlE89zl3PNwZU034NYuqrLmsHJ9ItVFnPhxEOecU-IFNPAizhP4NZbbUau7oKTttxVs2Md10qZj_dn5r-_P1PTvz-CUm67H3-TXnF3kwPJfz7b127q5qc_ewB60POABD1tW8v4Zafm7JSyoHpb8mlTPvv3h569fff_184tffnj1799898MvFz977sXzr7968frFD9-vNuxs8UliRYahK_PtAKd5kZO-7HFuXhUXpAcuD1zQ2w5XTYdrf1vWSLLf9QPfwDc12eAh6z0sYGiPgnF2Xm-rCnZEr-AkueRFXjX0LTztxWlOAz-Ax-EQB_4O9_stymDNmfNL070tqubGufbcc5Cq8hoE0fmOr0nlfH1NYJBaBGFMrK5FaeQ38MlfnPtSqbYEd-w851QIMpAZdi1uBYUGBPDs42JcMAljVuR-vrdgPdTJm23NCOjP1Mr-4hx7fmpOl6ZBnJKHz_kTKKez4ZvGUQLpEKeVjFg4PSg5Zwtn0zBeLQn7HaSNwjfMQSnbjmtrSUf2FkaLPEqCwt1bGCg_29LBYWqB_R3MOPb8BDPyPApcP-MPn_ODmfIfWzBryMMP45F8AJkoGa8pXwrOAsdIj5__Vn9wlstxccJG7LMjo0HKk3hvaV9VpNws0UKBcaJiNrAS22q4gy1T4ybY46ZJkvhh_vg1_HTFnZaAkWWO5y8H0r91NuT3piuHnWOEBEm1gpvw2AAjiqYCVZuQmTgLkoQQ9vgFfnBecjBYFI7sx1dB7Fwn8Bvo-MrTh7V0xM9z8w9-_Eq6jqmDJGHuFpx6T8PEbd1vW3QqnC07ND0EpOqqqUH2lmvSOuUGOHjNN2DXQS87DopKajzXCcVjsZv4if_4BS6dDTxRLkEVwHe_evWNcwMuGMxDRbo175yeS0o9H5yypqgMcNJ1U_bcGRdYge_fW2BAeZaE_InEsAAHIs542Q87wBxaHpUN978GQa155dyQHoWw40UDbKybCQ5yRt04CvxDM7JGF15e8yVioarpt0DoRjuQeynuvYlMaHHkpl7gFfSJVyd42TV_8FoxDImTshYqDid-s-OdYjGwF4SRdk3fO-uOtFcTvMxDPw8Ie-rVfnC-ktRwmaw0hpq3rzl_63TbXCr_d8C98S85Zkq7_Sj0PJKwJ17ut8ilZVNXO0eRHS3jH7xr9uwARVVYOLQchA2dYG6RZkFIgmx_teCxX9SMv7unSN5-fEL4wiSCQMKNHjzjD7UD9os7gxAiYU-U1IG56xcAK5SDRaMiAg4g7pDBKcrrKU54LmWEPXxd9rMbEHtEQawk67oBFEDBqZF24N3KeQF2eGjaJQMc67CGbsE0T6yL0QJ87gG_nvOCwHIkqHK6puL9naDw2IiJc4rDNEpJXjxm3tEiLAANkQqiOhBXBqFK1bTokYDEduCaYedTbMg45zkLHrOcDyNYx2dBnV-J6T84XyqUe-Da9U_h2KddugvM4uFjVvcFeCH5KCVV1TsQe4LIvgOGoQMHme7Q_QDD1lcCC41hsMOmGBdCjAox2IE94hBzXQNt0tGrcgA3vBWgZdr1nBg0FVwkvsdi5j1ydoEWFay2xxhVYw3-u6z5dujAaYO2l6BmEIzwaaFivPDT6JGru7y8xLG_1X2z7SjHadtt_1v9P__138YaOf02B2ACAE1-rlIMApbJT8Z1UpCCfRdICOYSsifgogQ1wMuirHBRbVtB8O-AanK6o_ARxmZrwOEcTGklHhbeZMpysqJIXW_fQX-vPOsIxvi7lnclbvgOObtj6FR4ApvgkR8-yUq-2QoJ2xuJDtvpr5ptBfEIQtjBPuCiKGkJv--cQ269Wej8zBn4I4wELxDsyqSH-EZnUPhFRrOEuSHJacpplmd-krLAj1GF6mYQNFUKyVEpJIdecfq2bUqxIZhRzIR5Ef0XpkXeYO6pKunOomDnoywiItP1wFRV3xTDRQEnw7u2K1VGrM-984TwPCyynHl5Qr0099KMpWFOCzf34tTP8jDNfEIjzpjvZkFWBG6YpjGMSZIgjBHs94BnRGZLnta5n34ERmMiyXf9eOmmSz_7yQvPXe88DD9z3XMXkweK43jIfpQTnycgNOOn7_8VyTAhsTJZdUX6Kxl0hSl1vbAQ9kjQsPJXSpifOvGkJhdpJ-IVXi7CUjG5lYvSk987t6TIui6cbZ4mHPZuyI7pJkX2MekjsceVg5ZN_Q3fiIhCBrt1Uy9lUlFg4WvhUlGv-5XzFUTKJUOmCQsH9o7CUwDVgMEwyQAf9GUFfzhwWASTqgAu33G6hV8dAA7tFh_BcHtcitOjz9FzDyrqAfC3KUW6sndg7IYMA36o1rVbQZBBeY2hr3QdEuLXA6KmRmJ4mAmM9qbFKYeOc7FaDpZnKEmllqGYBtHXoLbP39FqC6qCKGwDqKHEj6WUro5YdC2KBQ9yjycRF6Injs1Kxo3ScM_kmiJLiJtGXhR7XsA0WSvfpsg-Kn92DLfxtiJgnnUSR5z1gVXHGEKldpznjTg4ZHYjsKH8As4MfAYAsx1MKcMuK-JykKNb7St7cRoq8aKTMSo6ybeDc2LYGKwUHLGgmVHKN3imjq_LHj4VgmJtYI2n3kNQ0eo8GaY0TuQxVpIvL8lbgal0XOpYcSmSYAq9SiMIC8U4WEruUkegX_z4whHnpViFy_TDJSU9jocnN2VdiuinJwUfdiov0GLGH2BLhVC35yqIE1GssIvwXcUJlnUWqCQA7WQApXRogTq0rZX6_AFPb7aDZQhg37htE1zrZMSmrbg0HJiMoshjPKf17chaZXqApV2DRYXBwQqVtiyof2RA-KBY-fqqbMXzLYR6dnwP-yw3ZUXGQ7K59Qqs3QbIMPk9oXTbEbpbOKzbLbttDRKEG8vLCmzEwgEbUzKEkZtyQLOorGPFl6hrIJW_y2QajN8CqEMjaX8oRJLxTQuTI0RB7quDkMdtH5cSlNc4meA5zFTicQnQAkYMuQUCLqXYQCBxLiBPTYVyT7V9lfpQI9_HU7TFcAydbcnD7GWHOVgx8IhmjsOQPg69KkGBEA1TAXLLBidkIqV4mAqA1SLZddXk8OyXL_1oIfzPtVAveF5-s8RvHFwzmtwrIr7a1iUYJzTWMMKCgIoyugnKOVOsxfomchyCNw7YsWLyMJBWWWuxBGJCzCoICYZup7jz_AQrvh1XDX-9GFAxAb8xPIG9ufcYYh1IWUs7IRMnuAgwUhCPS13B5ZHrpkQqI5P1PgSz9ULBhJWV9KcfjkXIxqWkIeNBmECcbFzKWNAYXconFiYU-TR085C7JIuiRJO3ahUGaDy85oDWT6i3dPzORhQHjqYsDKbKwsilYRylBvxY5Qnj7h5TZpA5FI4JA_jac92V6_6b_Rs--5-n_JTTSZPkZ6ssFMOClRepUX8fSwhmgsRdJYJ-6q_STD34-i5vJh73UhwXBqsQZ5qQFBASFkJEkaUCIyooaiom1lE-tPIBzlH6YTjdncOkVUEVAAiGZApQImH9x3yq3grYdRD051YCC5Yv8Rn4TyYolQKUFTuBYtFUqUYGlLwpccnyiOdFnkP8YzRkLMSofT-moEIEXJKCnUNIh9o9Sobe4-e_1Uugh9qxvIG9SCOj_HcF5sFsVFnL_ZHKooAYMy7MSi9T620FsBa3Lj1t3XQb8Gd_KNenzLdJ3RZlB9awLVuOoadyPhVaSCtvIoad2ICwu1hdKAWYBnQtci-wcVm9QccwSEE1DlY6F_igK9G71cp47yTeEqHB6khRSp1fUISR52deSinV52fVqSy5fWi9CTa_FRCnFNsiB4hQHRHCQLkX4WjBbIHFJyh_mC-qkQcEB4tAZSIISEnAoiIoCp8Zk2qVtfaCgAdXpHRkkFIeBYzyNA31XFaRyubdA-tLS-XY0cdLhV0yDgrPRJTVYlAEvh6shvTNNTxdWakwzNqDtazBNmy7sWCkkOtw05jAUMZpoGTIeS92mgJ_CmYzgTklGBJgF71_DQEasg6m-Frg0jEFLBACaKLAZSAZoG-8bAF0_gQ2xeSKUSlQUi7_6q2yIIwvP5cgaqw8jB5cUBUjLv-KDsL3LyckIGBJWhRulie5SQpYxTjjwB5eRxsc0F6wIDKUO-XvLLenXSTIMgi7QDwas4MbC1ex8E5-sEo98Yu78KPIGZq3YNolBYEvFI4Xlki4vyARj0erOBZ-MF24cbA3TtTfpBVb74EvGOQFYlC0SiWZYJFl6anRe4jsagf8YPba96gksaEy4TG9xC9o5rKAeiZct6qQuu3pEQVEqRQmX-HwrgNJF44yb0ABjPCvnC8YEwctwSpscfRCelqkZZyl9NFaMEAYCvQMYLCVoZOarlbWnwpYVby2F6tCcCrdPIRLrAHMi_MpQrBZI61Cs_RqcUsyPiw6Dn4IFoPG5NzRgYFOSvQ6DSwrEFYUuVCOVpM8eI60S_hmvUZqE8oXennucZcDKDBwwCrWWub3XtVXRZW5KWMAkwkXRlxQtQqyiupjKqxcGKPUXUWgScjNvQArTleRLz-3Yj7g9MgvyT6LgKh16YeXMqgTumfCGZ0fgW-WYCq3vQzaFNRH1CcWJaRcwaXLX92F4765BPltBqzLAFwE6exgASvbYILIiqbFUUkmIz919FpYxBDwAMNVCWqF_LsVU66cX0i3UXiuzSLJPsDLMWI5kFGV2-uxSqAqgxUROZKDiPG0LPmR63s-zd08NQbCKncfqXV_av16eKaBJxZ0UftEptGUpUTeDFt-wRoMMhkJhmNoNsttqwAmKDpsEsdocG60XxsLxjciLkSQLswKziyrWSJhiFnYSUiTe8TNk4D7ea75YJXX7Sz3PYvlWll98JF-5odFZNTKqp_fwi8ProabA6Uh83MWcBKbjYwFcuOZH1PutnD2PpL_4PzHDYgi-FjHT75cgENbX6k0LB78Byuvbhc5hbf9HLMn0tYvnLVIhYA2qyx7WWNgLWY3SV4CMgLuBc6cHiKLn0Pnmwr4AeKCyQ-g8geX-AzGv4PnHVmOVYlipKQSV_tTDI10dyhGsElSHZvEwTD6WGZrJPidihSMTVDVBPD-P_60BGjhvG6Q9s-yuuAghOnwQYnWTWLM8rMS84iQZDcCalODOL7OrxD1LqXotmqsDNQBSMCKroUHH2kIYBasXEXgm7I-cqb2WOlnrJ1_LysrurKAvpDJNBXHjCIQ9zBKQMHDsHMvj6KfncA3YZakUQYIh6dszAiYhgsl7Y9pn7BU8IsXzrdwsDdkpxwfEMvB3qIryksGJ7tyXqrAyiBzMe_CTLQwoxawDJHGbroDc22MrB0ETNgur0hYCpzw48yAcau1ww7H7t-loc1JHvtFwVzOgsIweGzcsLNnT9eDoRODNMuChOV5UoSjKTNtGWrup-mwsLw12AL52X7e204IyO-P5bNVlUcTlWVH55kjy-vO71u2xj-tAsXVFjCtI1sL5DBU90GkLcaARH4jPpBGSwrvEcArn9zDkiOCUuvSGt7vapD3vtTrfYfFAcDEU8WK32rg-JGGFHVoEBKmXgbRuZeOkeHYo2IJzEPbTQB7vmvqZgNoGtSjgBUPz1TFHvxHxRUqOiyvqiNYgfvS8FtFzTLsljWUfTlQhQk4AUwpjTXZS8UbfmkkHCwiW0o_dmnYxcFpyqrM-KBm8sISgr1qDXAE1Qc_NUWZQe5pW4uE4dBIGQEUJjgyYRvciGd5EboEwn-D78amnNE2fHpnjdZSHoaZlzEKkMPk18dmGzXDYzpmcOe29o1xxc1VKfKnmOoRVhfE6tpzdb5rjQwX-Rk1i0xNVkQWk4TmLUcB0X0LmAjaYOS5V53FAlZv16PK2vjQ24VjiHbrHYjPjQJum20_KGS3c9CR67DJdjA9SMag05AEFnsFwieC3gqnH9N_AH9BYDAcv3X0bz7i2Ry58cUhpDX3vUQ0fI66--7sjbhDJqL9498e3BW79a2Ie83XgqvngOKuSMfwCt2f6VIZr6_LrqmR2xdYr-5P3C0Tm3jo1bI4T904dvdv47ySyEikNGpMYtzR6Xbs-cn2NtdLE8ofPiea5A0B313zJRozYWl09wbmiDE3ksPofr88iDJ_pKdN-sFTfDlYhWpe-4Lp2mR3uHJHbXp1atfHKb5SouvIO6ti_WgodFWhJzVAV7DAz3SDjEGq2hqs5HY0U9-f3Vxhm9yX5SGJkVmiYQmM9HCMpYqTckG9MmGtRGbahunFdORmeWxBn9AyGAduQRKX-iHNvITz0PNdlqbc8MjuBbT74Oz-wPeznJ-S8_t3aN7qUPx4vP_wrmbMJ-m4TAlxfewhzJK4AFANPzwXgqkwyVmQpV7sxyyOEo95PIE_C98PXD8IeFTkcUpzfmI_xxouw_MwO9JwGeeUpUHizQ2Xc8Pl3HA5N1zODZdzw-XccDk3XM4Nl3PD5dxwOTdczg2Xc8Pl3HA5N1zODZdzw-XccDk3XM4Nl3PD5dxwOTdczg2Xc8Pl3HA5N1zODZdzw-XccDk3XP7JGi6TLMviOA29zDU6ZDXKjLbhno0vmmxMIQTJeMRdNnZZml4Y65Qf2tsiE_xLnYRfHEm5LvYC5qUVJoyii-UCHTbacrG0clAyfMx3zuu_f7H0o1g1Q6ko8yXp3go8K9oQVF5JOfex2YqsQRXXpqDVHla_P7ebqIw77HXopzKKllmw-gZwqYCBqQwhdPsA32A6mDM91rxqTb12f-7CnbtwP60L91T_7anO25M9t3_Sbts7_wuHR7XZfur7-AEYiihv6mWtAc1Bg4L9t0Ree54CAqpNk6hSKCY17mhvvGvsRKtjVvheDNDradaCrqFG66KiXVNd1QjVcgg6s6tjzYkXfEYQ9Xopy59ukRg1yhqMrZRr2UslWiSUaiqVBANJIB6afOW6T_wiz-nTLPJEldiDX_ZJHcuhT74p2GcJC8In5KVIt6nU25EKKgRKA5EFi8_CVZa27eXnIk6Y4KXnpn7CRX_wuMhv5FHcLp6RApvrpEPwnPUdynJfMiAL06oT0CDyUxI--SKRqTj9EkURfZ04nr0GCVLrYhcRfV9aTquplw2zgiVemD75ejH7YpILpuvOVGnE-LEWgV08QlaEYEyJqptyP0pD9uQLFuks3fIlFmViJ5UthkCFdPC5zIFdmy4SOmUBXEDgLA_9J1_vS0Qjr2G-t4638sXKVW3XFK1xjTqNoZMiEHw06_vdmrDc3G1HduvixG3hvG07DrEyCGpTr3vsL5B3L1QhV3a-6KdWpxzlXXc5Ji2YbpJYnXJ9d9zrEL0hdmrxLeftQhEXcFG23YmeEoCp3d41iqN-7B4zFvuSY2gDam4wC4XiinhZd3YcNjQB1Ntiwf-Ek7qLo0riQZVFHA38VQvas0SqK2p1ysfch7MnfMbCFGgW0jNrIZER3-3-8ONMt3zJXVsuTunqUfmx7P89dpn4S9GAiuQY78t1bfWWj4nXng9YTekXJo0hd4u5xNUpcz61Lz3Hsm-BfQU2uyeHXbCqFivTvKr-p45fH8HBCVum-Y69o639Wz8aUtw5qca7UaLKhWWzpWiZECVIMGcbVYhenbKw92D5gdmU0ZnqXsQCsp2INQtSGWyVpaakJp1OgJ-4pCXnvLdh3FMfPStEj3AO21o1Q58URGnaNwSU7p04J9iTs21xtaJbe-LOBB5lY_JnJuv1Sfe8Jv5bwaP3vMz1m7vvec2B1hxozYHWHGjNgdYcaP1_CbTuf0v68Jqr5y5GD3fufTx-p_WfcomXUT_PU9_zfJ-FJGZuwnyvIDxweZHyIHRjGuV5GNEozWjsZb4fxozDxjw_DaPifru7daU3Offi8zA-cqXX_LfH85Xe-UrvfKX3n3ylNwWCDGKADDzGfKX3X32l97580c7vENOanNJ4S9XchRI6O_agybu-B4Hp8ct0Y24v-Vu_d3_noJoruSvSHre5adoBjh1RJ-zKwfUveWtNMtrsbAN-WodFi_0s3u38HRFM1CZFHjQSkO16zJYM0AdsbTzSxDdft56vW8_Xrefr1vN16_m69Xzder5uPV-3nq9bH-vhTamXedx3g7GZ0ipYjBb7AUUH3bUdBiSmeUG9wqi6VYewWPbQWkIpsc_BXb6xbx7UZIHjQQRFIzheb97D4AanD1coL6J1E6vrugnaNGjaUQB8sxVwYUTu5XCA-6npAi1BNIW7AZrYpWnoGkEfLzg6L54vdDkUe8XlnSXYVH_DO_vqksomyMtxKo-g2n5FVKlB2uJI9mKECVNX-GjICUkK3-Xm7KzyjC3uDyyxKDSvPkU8LA5qxPEq4608urgburBfIunH4ra7nyTqJpeFf4TVDD38Hn6aezPmeHR1G9eAt0HxYIzNBDbWMiIZMUN_CjQYhHE3YvDjJMzBBySua669WNWkacRwv4rQ_wl-CJKVK26cpys_nYAPUbhKEV44cbAKPgE-JIlEGwJ2JNPwwS_i0CNe4APfDHwYS132HYEHlqsy2MLtS7rySbzE-5kHaCdq2zeX5sa4ibLuyq_I6xYqBrZaPm6lV2AD6NE7vg9KbyUwbZWDDWNUKvCQ9BDyFpAwIWA6DvOI87s45ndxzO_imN_FMb-L48_2Lo40jEM_QbvomVjRapUYze-jexzUhAVnxMvAraZ5OAYDpu3BssEP7VcQK5Pv98B7pp2wm_vuUleAlmClgXkiXy-Epj8_xP_aBJjeUBmgWKneUT5Wx27wf_vdSydaBfpPJGO_ZECsHjcjTPz-5XSw1QRn1pfPhWWWcQoiSYEiDy-ii3Y-VBAgm_joF-CndAjSOyzUy0KAEXueQSkfDPPTdO-6OfqHQ-8AM7w8dAwROIYkAMcweoIb0qvI5BoMzJQgRiQoiOcnXsRMWs9qLzFe4OF9IfDnCcB1h0ewHMOR8731PgEPIKnMgXmrQBjbpb9yw7aF335dohNowf0jEnQB2inDvS8kt2n6Cu8CTU_4jqW3ijNFM1n5oaAJQuAZmne8ygKeFQ4ASCeC4mfZKlIUP_NXgScoeukqjATJKc-AzRF5WISM0TFnajpt1Nk9pkVGHrDsqF3A47XYhMi9S00XN2MbYSogDLU1Eb9B9uJFWhX6mlZfRxgQ5ZlWjuW7ZJ5I4Sn5rptatfDiS29ueGWmHm253g9W38QuD5LPokPf-Agw8MDIsoed5xBCY8uusF1LSUYOQfvJewkMzQDe72cE6e1MNxbVdaEGc4h4M10cgOJ_LR2zvOlpzmFMZ-Cmim0nLmuaxuqiodtelUonVJmnYYC9GQWlrhGHsZFJicNjOpCUv-3VWzAuISAml-YdFVb_s6nRSc6AjWY6wlENz9JFoMwsIKxh5XajaioHlvjFYGXQTPrjVmO1NnjHk2Rjk_rq0G5boZ3a1Lpp1hW3tqVX3Mu-aUf1Qs9v2prftDW_aWt-09b8pq35TVvzm7bmN23Nb9qa37Q1v2lrftPW_Kat-U1b85u25jdtfeqbtt58_F8Jp4uL)
