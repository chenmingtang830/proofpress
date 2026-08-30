[//]: # (ob:ad756759)
[//]: # (ob:v17-title)

[//]: # (ob:b02d00a8)
# Governed Workflow v17: Zero-Heavy Native Quality Ceiling

[//]: # (ob:56b5ce63)
[//]: # (ob:v17-status)

[//]: # (ob:35e5f496)
## Status and decision boundary

[//]: # (ob:25d88efa)
The frozen five-task zero-heavy diagnostic completed 45/45 scored cells across three executor models and three context mechanisms. This is a diagnostic subset, not the complete 12-task APEX Legal panel and not a claim about general legal quality. The formal panel used original APEX tasks and rubrics, three blind Gemini 3.1 Pro grades per artifact, no lawyer follow-up asks, and no PageIndex context or cost.

[//]: # (ob:05c4a89f)
[//]: # (ob:v17-design)

[//]: # (ob:d6585853)
## Frozen design

[//]: # (ob:cba112f3)
| Axis | Frozen value |
| --- | --- |
| Tasks | `World425_AVK_01`, `World425_amk_01`, `World425_amk_04`, `World425_jrf_01`, `World425_tas_07` |
| Executors | DeepSeek V4 Flash via Alibaba; GLM-5.3 Flash via Baseten; GPT-5.6 Sol via OpenAI |
| Conditions | v16 small-seed open loop; v17 governed open discovery; v17 raw-corpus upper-bound control |
| Denominator | 5 tasks × 3 models × 3 conditions = 45 cells |
| Grading | Three blind structured grades per artifact; original task rubric and gold visible only after execution |
| Implementation | `e4eee81` for the clean execution; v2 supplied one missing grader result without regenerating an executor artifact |

[//]: # (ob:717159aa)
[//]: # (ob:v17-mechanisms)
The v17 governed arm begins with a small admitted Claim Graph seed and exposes read-only graph traversal, paged BM25 gap/authority search, typed-object inspection and creation, and deterministic decimal calculation. It has no fixed graph-call, BM25-query, result-page, or lifetime-evidence cap. The only stopping guards are model context, wall time, repeated identical decisions, and fixed-route decision-provider exhaustion. Retrieved and derived objects remain `not_governed`; none can admit itself or authorize downstream reliance. The raw control exposes the same search and calculation surface without governed claims.

[//]: # (ob:4f845a75)
[//]: # (ob:v17-overall)

[//]: # (ob:29eba841)
## Overall result

[//]: # (ob:2aa78008)
| Condition | Mean rubric success | Mean context upper-bound units | Mean tool calls | Result |
| --- | ---: | ---: | ---: | --- |
| v16 small-seed open loop | **8.89%** | 9,261 | 1.20 | Highest overall on this subset |
| v17 governed open discovery | 1.48% | 173,063 | 1.67 | Lower quality despite broader discovery |
| v17 raw-corpus upper bound | 5.43% | 325,187 | 4.00 | Below small-seed; more context was not an upper quality bound |

[//]: # (ob:6d22c7cd)
The open arm did not validate the hypothesis that removing discovery caps would improve these zero-heavy tasks. Relative to small-seed, governed open discovery fell 7.41 percentage points while using about 18.7× the context upper-bound units. Raw corpus fell 3.46 points while using about 35.1× the context units. With only five tasks, these are directional mechanism findings, not population estimates.

[//]: # (ob:9b7d5530)
[//]: # (ob:v17-models)

[//]: # (ob:90fe8060)
## Result by model

[//]: # (ob:4f340c82)
| Model | Small-seed | Governed open | Raw corpus |
| --- | ---: | ---: | ---: |
| DeepSeek V4 Flash | 0.74% | 2.22% | 0.00% |
| GLM-5.3 Flash | **22.22%** | 0.74% | 6.67% |
| GPT-5.6 Sol | 3.70% | 1.48% | **9.63%** |

[//]: # (ob:90977904)
The direction is model-dependent. Governed open discovery slightly exceeded small-seed only for DeepSeek, while GLM strongly preferred small-seed and Sol performed best with raw corpus. No model shows a stable general advantage from the v17 mechanism on this subset.

[//]: # (ob:084aeada)
[//]: # (ob:v17-tasks)

[//]: # (ob:c058b969)
## Result by task, averaged across models

[//]: # (ob:cb28ec1b)
| Task | Small-seed | Governed open | Raw corpus |
| --- | ---: | ---: | ---: |
| `World425_AVK_01` — exact tax amount | 0.00% | 0.00% | 0.00% |
| `World425_amk_01` — exact authority chain | 0.00% | 0.00% | 0.00% |
| `World425_amk_04` — annual calculations | 0.00% | 0.00% | 0.00% |
| `World425_jrf_01` — authority synthesis | **33.33%** | 0.00% | 22.22% |
| `World425_tas_07` — multi-part authority document | **11.11%** | 7.41% | 4.94% |

[//]: # (ob:78bf95b3)
Three tasks remained zero under every model and mechanism. More search did not supply the requirement decomposition, exact authority chain, or executable calculation structure needed by their rubrics.

[//]: # (ob:d821ec13)
[//]: # (ob:v17-failures)

[//]: # (ob:a32bde2e)
## Criterion-level failure attribution

[//]: # (ob:dbf3c35d)
The two v17 conditions produced 66 criterion diagnoses each. Governed open discovery attributed 26 criteria to requirement coverage, 16 to graph sufficiency, 15 to derivation/authority/calculation capability, 6 to execution, 2 to delivery alignment, and 1 satisfied. Raw corpus attributed 32 to requirement coverage, 19 to graph sufficiency, 8 to derivation/authority/calculation capability, 2 to execution, 3 to delivery alignment, and 2 satisfied. Projection was not selected as the primary failure for any criterion.

[//]: # (ob:041201a1)
This changes the optimization target. The dominant problem is not a BM25 ceiling or graph traversal budget. The executor often fails before projection: it does not compile the rubric-like task requirements into explicit information needs, or the substrate lacks a responsive atomic fact/authority/derivation object. Increasing disclosure volume then adds text without resolving the missing unit of work.

[//]: # (ob:02d0ce7f)
[//]: # (ob:v17-tools)

[//]: # (ob:f8365019)
## Agent behavior and typed objects

[//]: # (ob:f1ba998f)
Across the 15 governed-open cells, executors made 25 successful tool calls; across raw corpus they made 60. Search was the only materially exercised capability: governed open used gap search in 9 cells and authority search in 2; raw used gap search in 13 and authority search in 5. No cell called the deterministic calculator, and no formal cell produced a scored advantage attributable to evidence-atom, authority-node, or derivation-node creation. The typed schemas and non-admission controls are implemented and tested, but this panel did not demonstrate that models will autonomously use them well.

[//]: # (ob:62c87232)
Stop states across the 45 cells were bounded and explicit: 31 model-ready, 9 context guard, 3 repeated-decision guard, and 2 fixed-route decision-provider guard. The latter finalizes with the already collected state only after three failed attempts on the same frozen route; it does not switch providers or fabricate evidence.

[//]: # (ob:7be19a3e)
[//]: # (ob:v17-cost)

[//]: # (ob:d73a6b04)
## Token, latency, and cost audit

[//]: # (ob:469cadbc)
The clean v1 execution made 358 fixed-route attempts. Gateway receipts record 10,634,339 input tokens and 791,805 output tokens. Known cost was $19.3962. One failed DeepSeek terminal attempt had no numeric provider cost, so this figure is a known-cost lower bound even though every call has a terminal receipt. The v2 completion added two grader attempts, 35,544 input tokens, 14,201 output tokens, and $0.1961 known cost; one attempt succeeded. Total known formal cost was therefore $19.5923, with the same one unpriced failed attempt.

[//]: # (ob:9e5eabbb)
| Route | Attempts | Input tokens | Output tokens | Mean latency | p95 latency | Known cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| DeepSeek / Alibaba | 53 | 1,641,761 | 46,207 | 9.01s | 19.94s | $0.2507 lower bound |
| GLM / Baseten | 69 | 1,933,248 | 121,314 | 15.00s | 29.86s | $0.2257 |
| GPT-5.6 Sol / OpenAI | 85 | 3,402,468 | 46,432 | 8.87s | 32.62s | $8.9649 |
| Gemini grader / Google, v1 | 151 | 3,656,862 | 577,852 | 29.92s | 60.88s | $9.9550 |
| Gemini grader supplement | 2 | 35,544 | 14,201 | 50.57s | 45.62s | $0.1961 |

[//]: # (ob:1a82dcb3)
Latency is client wall time per fixed-route attempt. Because calls ran concurrently, route latency totals must not be interpreted as experiment wall-clock duration. Qualification/debug runs are engineering overhead and are excluded from the formal cost above.

[//]: # (ob:036d290a)
[//]: # (ob:v17-governance)

[//]: # (ob:2d9c4f5e)
## Governance audit

[//]: # (ob:32031b71)
All 45 formal cells were scored; every model call had one terminal receipt; PageIndex made no scored-context contribution and cost $0. Retrieved receipts, evidence atoms, authority candidates, and derivation results were labeled non-governed and had `admission_authority: false`. Authority candidates defaulted to `normative_authority_confirmed: false`. The deterministic calculator accepted only decimal arithmetic over declared variables and could not execute code. Human approval remains the only admission path.

[//]: # (ob:3e9ae96c)
[//]: # (ob:v17-decision)

[//]: # (ob:674c877e)
## Product decision

[//]: # (ob:3c95c466)
Keep Claim Graph as the governed canonical substrate and keep small-seed disclosure as the current default. Do not promote unconstrained open discovery as a general quality improvement. The next experiment should add a requirement compiler before retrieval, then route each atomic requirement to one of three typed completion paths: exact evidence atom, authoritative provision, or deterministic derivation. Search should fill a declared requirement slot rather than accumulate loosely relevant text. The zero-heavy tasks should be rerun only after the graph contains or can construct those typed units; otherwise another retrieval-budget experiment is unlikely to change the result.

[//]: # (ob:49a0b5d1)
[//]: # (ob:v17-artifacts)

[//]: # (ob:db1c8d8c)
## Private evidence and reproducibility

[//]: # (ob:17ddeae8)
The passing qualification report is `/private/tmp/proofpress-private-eval-20260830/v17-zero-heavy-qualification-v4/sanitized-report.json`. The clean formal execution is `v17-zero-heavy-formal-v1`; the complete 45-cell result is `/private/tmp/proofpress-private-eval-20260830/v17-zero-heavy-formal-v2/sanitized-report.json`. Private task prompts, source text, model artifacts, grader payloads, and credentials remain outside Git. The canonical runner is `retrieval_adapter/run_workflow_utility_private.py`; open discovery is implemented in `retrieval_adapter/open_discovery_private.py` and `retrieval_adapter/agentic_disclosure_private.py`.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzRkZTk5NTUxNWE0N2RhNTVjN2M1ZGFjYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImVmNzY4ZTdkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mMzIyMDJmMjA3YmU5ZTZiYjJkMTU1MGMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzRhZDZlODE5NGJhYWUxOTA4Nzc5NTZjZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrFXOmO5EZyfpVE7wrYlauqeSWPHvjHSBod0DHambFkr1aoSSaTVVSzSIpkdU9LLcD__ALG-g38In4T_zDgt3BEZCbJ6unitGoaMNRQV_GIjIyM44uj59cz0fZFLmS_LrKzi7OmWQeZShLOXS6CKBOcy0jyTEhxtjhL6-xmnRUb1fXwbLcVHg8vctcN4iT1ZZCnmYqcOM3iQCZSJnHihvAjYj_O_URkjguXcofz0E-DIPdTIbPAAbpZ0cn6SrU3Zxe_4pd-3YsNrFCKHpdawIdUlXDhO9UWeSHSUrFWXRVdUVdsC8_X7Q1Lb9i3bV3nTau6Dt5phLwUG4WbOrjc1j8p2O6-RYLbvm-6i_PzTdFv9-lK1rtzuVXVrqg2vag2se-cH7zdqp_3BXxe7zvVrmVddaoCWfTtXv22ONsqgUJUeRTGKsrO9JW1uqKHQLhqnfue53i550SpSlSYpl7mcu5I5Kxue9zauiwqBZzbEynXgchCFbtJkAqh3MSJoyjhoVR6O4a7tRRNty9hwx7yKes2684ufvj1zCz_6xmcct12-EnfVtk6BZH_cCbrTL05-xF2YLUBj7ffZ4XqzkWj3iyBnapfqitRnn_2_LtnL7559sn6--cvvvz0q-ffr79zo_Vfn714vv782dPv_mX94tnLf_rq1cvVDgXwe9RL9H1bpPseTnWdiq7oUJbVVdHW1Q6WX8N9UAdFZPf9tm5xK5dFhZS7G7izgzuV2OGZ6y0tzjqQDNA7u6j2ZQkblFs4VqUFk5a1vIRnRRbxMOIJPA4n2qs3uP0__c_f_-1___Pvf4aLZgmRZbR2g6qnruHKD-fnP16wP7A_1enFlRst-6IvFb7R3zSkeKIVZ78txpVSx8scR8QHK32Gql-pjH1ft5d5WV8zoHXB_qraevm5Elc37BvRF1dqjpM_sIdSYX_Zi7Lob9jHqgBF24zcoq7ihSnDPEy5VKH_6AzfFV3Xi37fzcnO54rnQRIesPKSXmOiylimpHYIab2vMgHOZE5ef2DveHVGKB7P4ljl4lE4ebVVLG_rX1TFcpDZshfdJfsFRbklUWaF2FR11xeSgXdqSgUGwAJ-HnDWzUjL4TIQ4G0fhce7h5WprthUc4eVhTyG_w715lO9Tf32O07n7rMzxyFT4bpefuJat-zpm6Jjt3ZFcHF7xW7_Vt2y5XLJzP_x6ys4GXzwNah9mQUeXz_9buSMXPcBX5EbuTwR4jS-7sp8p9B1Fd2u-_PfKlQauMg21hJFu2Op2hRVx64hlM2cTJDHARcRfxyucH1RlnOq4CUqFXHgHiz4XL8HURxCVv8OXXjr4TnbFCKKHSc-cbVb9nFdZQWGIDjpr5WoWLtPWzC-bi8lxBJ71RBnewjq7ZKMaE4XwszzINJlJ7KF5103cEJ4zlmRsaruUVOLDBAS6-Hu9qap4TcETfgqeqC5q69AOCybOZokjTLOfedErt5SUYi55awPT5xcxU54uOALWgjxGxF4hzK8_fSMNgDIDBwZe6euB4eNj8Chv9yBTJadAlu7HWMtnckteyGuQSHaBnzrxHHM6UPiJIDhnOBUxlAhMgCikjQVDp3eAMcMDGWAlVZ3eBwQNuvKuagRBwLEKE5l6y1AhC5zTiGkw-M0CZMjC-L7CyZQIzfo5WRbd2av3YP15B1EZiOLFyvppo_MnQ4lpynVcjbixGme8NR_ZH5fbVul6O0O_YookEuEKAy8nmqZIsUiOoQthlC1Yl_PYYTYc0G6j83tXR3MRVHuwZnNqaHwPchdPXXAysdt0UO-WVfLEnZYMkOITdKUd-jgwyjMKGCW5r70efaYfKHr6K9rwg_SBruOQSKZ7SUIOgyZtCtY9Kk6poTcruZcR-B6jivcx2UVPJvJ2CjK1U1f7IpfBHm9XrQbBZ6OfGENKbuoetwGWMWOFXOsQhImVZQ_Jqtveb66ng-FeeyH3HEPPd9TTLMByG3FVVG3ZEz4PviEFIsW7_J5D3h9RtlyNxVJEuePxtFTbbJ4cC4fsOqS_JtUZdktmHqj5B6rEmwnMsU8bnHWjORCT8aR53uPxufLvm4YJqCgZWLkGTIs4pJdK9ADgnjoh4CyetOUhSz6C-bP8Bmlyk2Erx6Nz7s6JiEtnE3CIl-E6R2Q8aq-VNWCYWmtkjcL4gAJMbEHV_AOBXvny3NYLEykyFL5SNyg1csSofiVa9QInQKpkc9jSKbfgK619b4nG1a7pu8AFcFC12IOoSquRJqmj8QlhHHiALJMwwN8_KJq9j3rkSh-fb7vD75TfgFrzUV6V8ReJu9E-tPZ_Eq_gkBSlgVq6DWmAOBsFYP85j5hrthHSop9p-YcrQ95T-KIR-Lyrv5rjyIqOVtz87JEBjlX95Sw8NUH6f09j89ouu85vptG7skrPgXZg_fJ6xYA4tQJAYhvVfbkAHFJPKmtAA9SQWCfOw5fJUIloTyZr7frQLqINCf-MArAXUeH4v-WwEY_VKHeIf57Hp8Tv0y4DMLw5BW_VKphH5ei2LHPWtFsmdABYai2SFHVVQGCh2iVdn2LSTiq8aWaE3-QCCflmXsyX3fFb2vrszgjS10ZZ7G8s2pxhUwDZcgWpea-VRoDFmmBBeJ3nsmDSMyckxsBXaHiR-UMw0Ijug5LHz9jpTuHc6LIAETqtkcX9_q80auc97vmsL9zIMUfF7Z3cgYHj6ezlq0SugNBd2xXY7avU9U90TTtHWbaOwBslbxs6qLqqVvV0krYprDfsEvxI_aFAGzcTChMe0UTItSFOrGN1NV5v85BaKoF2ZhuVZe6F56vXF9yL3SjPOM8ypTjx6n0chGCJ_H8MJeJkwQQjmSeRZEnw1Q5aZpzF_BtIlBSiKyo66RP6yLwfwNBY3MHJBYunXjpO68878LlFzz6B8e5cLA-ZCQ-baf9Nrn66_9vq4p0WHeRtqLbYmsH2xOe4zixgwItssPGklHvB3eMDNXIj2D9mEcJWTBRnTSRDNXH7v6Yxf0kzqQXpInvBXbxSUPoyJaOd3IMWccNAsdJE4cHg6QmzR27p1M6NGaFOM8d4bpx4KeRXWHStLFA5D06LxSHTWQeUgasktiExhQqNMCnO7ZiPBbyMXUFdwQ_YroYxhTVL6jGi2HHLs5cT_P49Ntn_8y-UhuIP42oTNEFnxaA3jBqCZBSz8AOsJLLSnryZ33wOl02yEK_DRgOwENbbCCDLjVxXesh10vVb8jU9CZSUJqMfaYg2y6Yv3IxNLNNC6C7I6BobQi5B4h3fYPgsS5BIZf7hiHVheGWfQuG-gWkVG8GyYDUEAiujquOz7lKuJu7gRpUZ9LpOqKRx9tVhmyY5iG4xNiFcGTJTjpYo0Y-oCtlSAZR4oB38yCf9izJSaPKkHy_5tOXa8d9vZhcErvLey8FB5d-avO7T8F5r53otV7q2ZCT37JPAAq9VOqSfRewT0vYGrsqBHtaFqlIxRP22VdfL_nKn9z6SIDuqgpuffsKboXsZV3SjeeQ9T_9Qq_w8Vh2ugVHFbJuLIRSdaCs6-bJYYfrsIytb7biemlKpJM-DOlTC8vSWp-oimpDaJO3jBvV_q__YL41Ufo8qYT945j5EwXAgHi68PariQ0A7APctkc3cI_-PxkNikzWNJFQ9Td1mTGcXUEsUFflDRN5j1XUIYelVb9Ao8exB2GaUa8VKD3o6Gu0Xu0YKP0d3gOZeOA8INIXSmcDu0IDIWKwNR0dahCif2iV9hA9PjIQqsdNsNv7UlDrxf0AAr3nu5nvWwWfdDyPmOLv6mKCPyPFYCLbFT163ykoJ20x1RiqUAI0y5Yk0A09ALgc4YIoF-DosIT80dceZxvRnOvpEQyDnRKt3C50DWapazAM1m9MZ4WSU8R88GVhIhEcFro_8tUYlyhHE6Xcl_TYin3RQz7WoY-jvFmzs8Q8bUE8LH_egwovzHkskbkFOj8AqwpT7uUAfqVotMOmbXV93TR0nnvRZuCfISM0OaD2oIsxbUfqDWFVhrR6ylZsFDVOeJrV21tLgMO4OurjFtJ7vaMXqm8LQLyZEQHA57FkZXoC7DWEoLU9y9dPYP8V7qDSx8eKvlNljvs04v8Fy7bXFRiSEjsgUhaYher9ttT80GZszxdVvhM7ZQ5Nn80od1D9FrRWDfo9pmuoNd1MWMmyGCGs4I4zAJ1Jn_yILs_0vg1dGeWAcyAXEMFAd9IOH-PKQzrchqbrRF6UerHvKHegOTa9h8Byeh-b7auiHx7AQjbVGPCK6c4cBqiL-37pZ475dnjmww_jVZx88OGH8DlZQH4Bv92V58Cvz4vNVnWAB4xUsNaPQEkDI0v5aGwgQkH8Af6O_IUT-nQljODXV_U1qLbBQhjHmwKUP21rcpATEnaNuyFGA1CMJKvAxyV8jy_cGGkHKwe5_0gh_B53_QRstB3h3zV5hh4driZomTGEZ1xuEkaRA3A8DAj809FPBgsmsPbUWYFh_zhLyK7rPYSqYocugd7s1BQfUyRF31Dq1KKvJ7teHD2dHCIri1aBiwFTYoCDXJgyWFhxW0BQ3FPQ0iDWjVcRBGiNg4-o6mraKyXy_ioIj9P0-cq9S1PT-R6jDvnanHakAaveOXrboeUOznQIZfBshVbaacje1I31SKDEEB16Ned7EsjJwzR0nZg79lAncxnH4ujRUQubOAaSu6lKZBQNrmcyfTG6ngfNU9gc1xHSS70wjLyJnxxGLAbf8x5DE_f5Ew3j7gLRW-asogBN0Ft53gf03XE-MJjtAJiit_HoKXI39r0QfIJ9foJWwaZXkfPBxI18-GGyCn16ecY8uXLBz_tOovyJyIc5j4l5njq5AX6xB91UbySIFB6YulZSWgiuVlALo_ggCcSqdbWBB5pW5aptD1_FOIr7BqvCvBCupOh9CYG1wyGt2De1QRvdtr7GnLXT9SybZ4rsSmhrhqx6R-aFHnS0k0M_PmMTEHcFQMk8crMhf5-MphyrpRwbNjFUc5EqnkYiDh0-pGTj_Ml9JvH7R0dslOax63Ke8MBTY_o3TJMMlvIegyBHDOWtBJH997_-O6gM4vlevGFiB46zH63l7u9DGiajnNAYsTMca1H9LkKBJiSqan-ImbuHkjG5qyYzovibysQztFXfX_m-tXRNyzMu4pCYzXqR2A5OvAAo3k53mNVyjykYkXXdletqshi9PqCIn6AjmfMJIpGhzHwHYN-QJY1TOoNPOH3ABrGFAcQ22FMOeEMGaP5egTYBEL_eAZQudDJz73FSHqITQbLtA3xtM15WafeT0hpFa4tEMxadhyKJY5mkXCZDhWWc_zli0XOjO4aw50cyT1LhOVSV12XXcZpnNOqTZ3HMQir30limgZ_lA_iajOdMvPupwzVHHb9lEe54w_sC8db0eOlhSiUBdPe1SYK7fZ4XstCtVpfjDUrf6EjHRPh8etAA_oTutCwYkRpKDAvmaQploTmDkER_m6ETShfys77o8kJlB5hssgHfm-E7OcJ3_LvZ9u6w7c-x7U3Z_lb_fRAStFAd8la4gv5fJ6FNC6gOkaxRoZwGOW7Gk50xhBg0SGahm3juGNrG0alBjU4ffDLpha52SF3mR6u-UxRh6T4bqAylnzrvsRwOG-sABeToXJpBIBeQw8OCSq-AzgQBBrkZcgDLsrhUpt41HnDHAIbXw8wMfKPqM-0EHUlHPoeS-6GZWgqJ9WfMhxuwH8TiooedSoZ1qcn5j0phqhEr9kWFBZvO5jNl3eEZXdUluHJcBusRGUiVkrGhFNbVJaVAyIctm2FSABKBPKi9nKseOImnslz5sTNUwiYjZsfQyrEBsaEm7eMcQeQGobBUJzNjo2M7bejL4hQVK57lQeBFQ3yazIHZoaX3GOTK9-WkhvDEYqgRWCLZG_1W6KzYSx3Lro2tEa7FHAo8XknYF5LGoqMmvDX3izu5JjU0NqKxcRFQSmJ7NSCdu9U_vO89IY7uedP1j77ECRMjYdqcyojjwwKhdVB1OzQ-JmMdY2AQtqc0omjrNSkQowWZquASTWExcrSsABiQEY3WQNeGyqU2cq0VndwCwugMM9USi3P0J3K23qbrioUtP5sEQf_l3QK8Rq9BvO4dWciRqV1dGeOlmoKprV8XWL4FxahqwJ0dHCCIGMW0Y9ew_xmrcoTv5k4Qx7EaEMNk8m_4i6bTR_dck3ph3RhCRjIUA6i8ijHDllCHQRd7S0eN-fopPaolX-LMFE5RVRB5flGmuo2MipJWh6VLE2NoM9O-gG68oUvGLdgpMsqlTD3UNDGJkScHPrqDhUBXLU8dKgmkQS3ORIwzFnOZmMdzT_lZGNM8jcav41zjEd92bDDR1iZEJr0ogcMciU5mFUfXdsq4oS2rSJGEURhk_tjSm0wgTuDaqUOEN6AeEF4bKoDjn9My11mEfrDw_QS8w2SkD9mOEncRO5zV02G_Ffuyqq8rvSf0eH90k5WfhN6KPa-GMx9KH9qvYKatWaGpL3AoFUQ2LO0Oqof0FqyrtaXmxQYjILWZL3E9Oh9WUilUl9FwmIVhKNxsTbJhpsrwnWFZs1-t01eebUxTnwRHOwj5ml6TlRaYEV_wIDiQCEC9YAGQ51Aa-nz_6KzcJHQ1p7STJ9TLsnumsILpB7BR98CVftA6VStJMI5W4xeUKU88fzFaHVkNEt1XgOXQ_R6a14xBSCeDqBx6CVdjkWecGR0S-9PHPmkQ85Y1CZ98m-jJA4rv8xW0c9u_xSo21cYXYeAuIirBByEcDFazk5XjIlsgvSTAD3AwHodbU72xtTagaRq_WFZLiGbi-wsviPGz5y58N8BPHBJyJOYlqzi0VD0evV2FOx86xizmWJNbBI63CMJYMxlAIgF3VnHUURF-FXpELl4lYZAYcnpMwWjkOeRX9aaESHlFvQbuEtWQh4s4RGI8ihYx9zR3CZEDQBLHRBeucO7cR5eybWXKBPi2Ufhbq-RA2Vlx4jPglk-j5XO1g0hEPMyTJEvdAQFO5n6Nqr3P6K7p67S6DyT3LU6dldiZpMet-vVoZwDs9qB9GFVShZAeJ8WUyYogqoIH2tnVlxLHo1i2bw38-Mt0Eg9Ae7rfQM5Qaaihqk0BiUBLeQo4H_TmGnPhzTey3KNvGWqKU0sXKbwwF778NI_dxBV5OIxPTYaSj4Sv-bliSzrIuPCTCHD-gE8mo8ZjEHvY7LAdG3ECyHAcwSVPh9mocZzY4vH3mA8-9OVPJmM4FPUgnGgiS4uGCBaaCskYgUGBJ11hGwkXk7lNAKndYlpfgnepB9Utxi6yHc3EgqvZA_1bH0qD03EyAF7APbwe4Op6oHwB3rvs1OsVe3rPYrBOLoA6hqcae9SUe16p8X38ZzzyAgvfI6VXM0AegKZUTW-L7nYEQACt7U7hs8g1Xi8FIvoruIO23RnpYVMNzUjjDexBZWrFPt_vsFXeYBCn88Ey4CQHGnF6I_rtXDoqAFgFcRQn_jheN05-H52ROj7KbUttWeSpJI4jlQzGNJnuHjX-YePaVuOl52QAJ3kUDtnzZILbUH2fkexm2uyYlAQMCeP2rJ6s2Ce17uOBw6l7xAhSpzbFfaU5BEi2AWI7uaZjuqNuDmpShXY08ZHdlpQAQBPVOKa1MKqptLb20moLwxEWqlxov4zVQlsPmb4N-o02XucmZ9AJ3wSloeZ0F6bye2Cpo6HqXi5ByY5KZ5RXHs68WMMdsnWzoZyyvVHzp8x1JcgUjmVLKQ2qupT7HVqUwpGATpUIqEuF2S8VZ7To7vab7VIpCgdCyGGmpEyVC30WmQ-OFOropqvXCHI7Kxlq-gK6RJ6uC2zxVvR5FPtSF8mmZwdxdl9hoQsr7LUp0plaO3qxuZQ2CXMZOVLlTj7kJOMfBRyxzNkpf2vzgSvdNBeum-RjcXoY_J-a5qlT-7YFHHIOGWQkIfwNoGQc5J_kVadO4S_NZRrhXuKIuIP_DBOKYlSG5QHV5VVw3gk4TUiuAevQEqufuroynlyneCZcjmkeMnGHrH5meeW-fnI4exvwJRVszAzde_NvF_KOMm6Piuqp6Iwovnb1vpWK6Wkv0xGyCrKwkLQRN2UtMhNoJZgiToAhhjOjWuBGOlAA9llhzGx0n2BT4M1og4MZrEUmIOC153BzfW0mzNcgRFSXtdnvqrkBod3xjzjePKkk4ZTY21TxnfXwzpQe8X_PGzTjX8j16M2nb71lgj_-Bj__By_-hw4)
