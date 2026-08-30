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
The clean v1 execution made 358 fixed-route attempts. Gateway receipts record 10,634,339 input tokens and 791,805 output tokens. Known cost was $19.3962. One failed DeepSeek terminal attempt had no numeric provider cost, so this figure is a known-cost lower bound even though every call has a terminal receipt. The v2 completion added two grader attempts, 35,544 input tokens, 14,201 output tokens, and $0.1961 known cost; one attempt succeeded. Across the clean run and completion supplement, the formal result therefore records 10,669,883 input tokens, 806,006 output tokens, and $19.5923 known cost, with the same one unpriced failed attempt.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzRkZTk5NTUxNWE0N2RhNTVjN2M1ZGFjYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjcwMmZkYTIwIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84ZThiZGU1Yjc2ZDFmYzViODU1MzUyMDAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzRhZDZlODE5NGJhYWUxOTA4Nzc5NTZjZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXeuO40Z2fpVCew3szlJq3i89yI-xPb7Al_HOTOxkvYamWCxKdFOkTFLd0542kH95gWDzBnmRvEl-BMhb5JxTVSSlaXHamkYSZAUbbomXU6eqzuU7l5LfnPGmK3IuukWRnV2cbTYLP5NJEgROwP0o40EgIhFkXPAz6yyts5tFVixl28Gz7Yq7QXjhc9eRnuNF8KSdxa4b2CKwQ-m5cIFzHiaZE_l-Inyey0jGkRA8Tt3QtlM7jzwBdLOiFfWVbG7OLt7gl27R8SWMUPIOh7LgQypLuPCdbIq84GkpWSOviraoK7aC5-vmhqU37NumrvNNI9sW3tlwccmXEie1c7mpf5Iw3W2DBFddt2kvzs-XRbfapnNRr8_FSlbrolp2vFrGnn2-83Yjf94W8HmxbWWzEHXVygrWomu28lfrbCU5LmJku3nGXftMXVnIK3oIFlcuYhmnmQzSKMycXARpHARe4Nr47KZuOpzaoiwqCZybHSkXPs9CGTuJn3IuncSOoygJQiHVdDR3C8E37baECbvIp6ibrD27-OHNmR7-zRnsct20-EndltkihSX_4UzUmXx99iPMwEgDbm-3zQrZnvONfD0DdqpuJq94ef7Zs--ePv_m6SeL7589__LTr559v_jOiRZ_fvr82eLzp0---8fF86cv_v6rly_m6-zM-k3ixbuuKdJtB7u6SHlbAKtnsroqmrpaw_ALuA_iIInstlvVDU7lsqiQcnsDd9Zwp-Jr3HM1JeushZUBemcX1bYsYYJiBdsq1cKkZS0u4VmeRUEYBQk8Djvaydc4_d__51__-b_-7a9_gIt6CJ5lNPYGRU9ew5Ufzs9_vGAfsN_X6cWVE826oislvtHdbEjweMPPfrWGkVLbzWybxzsjfYaiX8mMfV83l3lZXzOgdcH-LJt69rnkVzfsG94VV3KKkw_YfamwP215WXQ37GNZgKAtB25RVvHCmOEgTAMhQ-_BGd5furbj3badWjsvkEHuJ-EOKy_oNcarjGVSKIOQ1tsq42BMptbrA_aOVycWxQ2yOJY5fxBOXq4ky5v6F1mxHNZs1vH2kv2CS7mipcwKvqzqtisEA-u0KSUoAPODcz9g7cRq2QHY2zjJH4TH_c3KZFssq6nNysIghn925eZTNU319jt2Z__Zie0QKXccNz9yrFv25HXRslszIpi4rWS3f6lu2Ww2Y_q_-PUl7Aw--ArEvsx8N1g8-W7gjEz3Dl-REzlBwvlxfO2v-Vqi6SradfuHv1QoNHCRLY0m8mbNUrksqpZdgyub2Bk_j_2AR8HDcIXj87KcEgU3kSmPfWdnwGfqPfDi4LK6d8jCWw9P6SbnUWzb8ZGj3bKP6yor0AXBTn8tecWabdqA8rVbIcCXmKuaONuCU29mpERTshBmrgueLjuSLdzvegM7hPucFRmr6g4ltcgAIbEO7q5uNjX8BacJX3kHNNf1FSwOyya2JkmjDPCHfSRXb4ko-Nxy0oYndi5jO9wd8DkNhPiNCLxDGN5-ekIa_NzzbRG7x44Hm42PwKa_WMOazFoJunY7-Frak1v2nF-DQDQbsK0jwzElD4mdAIaz_WMZQ4HIAIgKklTYdHoDDDMwlAFWmu_x2CNs1pZTXiP2OSwjP5attwARmswpgRB2EKdJmBwYEN-3GEeJXKKVE03d6rm295aTdxCZ9CxuLIWTPjB3ypUcJ1SzSY8Tp3kSpN4D8_ty1UhJb7doV3iBXCJEYWD1ZMMkCRbRIWzRu6o5-3oKI8QQOArnobndl8GcF-UWjNmUGHLPhajMlTusfNwUHcSbdTUrYYYl04TYKEx5hwzej8KEAGZp7gkvyB6SLzQd3XVN-EEYZ9cyCCSzrYCFDkMmzAgGfcqWSS5W8ynT4Tuu7XDnYVkFy6YjNvJy9aYr1sUvnKxex5ulBEtHtrCGkJ1XHU4DtGLNiilWIQgTMsofktW3LF9dT7vCPPbCwHZ2Ld8TDLMByK34VVE3pEz4PtiEFJMW77J593h9QthyJ-VJEucPxtETpbK4cU7QY9UZ2Tchy7K1mHwtxRazEmzNM8ncwOCsiZULXRFHruc-GJ8vunrDMAAFKeMDzxBhEZfsWoIcEMRDOwSU5etNWYiiu2DeBJ9RKp2Ee_LB-NyXMQFh4WQQFnk8TPdAxsv6UlYWw9RaJW4s4gAJMb4FU_AOAXvny1NYLEwEz1LxQNyg1osSofiVo8UIjQKJkRfEEEy_Bllr6m1HOizXm64FVAQDXfMphCoDydM0fSAuwY0TBxBlah7g4xfVZtuxDoni12fbbuc7xRcw1pSnd3jsZmLP0x_P5lfqFQSSoixQQq8xBABjKxnEN3ct5px9JAXftnLK0HoQ9yQ2fyAu9-VfWRReicmcm5slws8DeUcKC1-9l9zf8fiEpHuu7Tlp5Bw94hNYe7A-ed0AQBwbIQDxjcwe7yAugTu14mBBKnDsU9vhyYTLJBRH8_V2HkglkaaWP4x8MNfR7vJ_S2Cj67NQ71j-Ox6fWn6RBMIPw6NH_FLKDfu45MWafdbwzYpx5RD6bIvgVV0VsPDgrdK2azAIRzG-lFPL7yfcToPMOZqv_eU3ufVJnJGljoizWOyNWlwh00AZokWhuG-kwoBFWmCC-J17ci8SE_vkRECXy_hBOUO3sOFti6mPnzHTncM-kWcAInXToYl7db5Ro5x3681ufWdnFX-0TO3kDDYed2chGslVBYLumKqGXOSe69pu7trg9RMZpqmbOUFg47JXdUc0dXmH6fIOAFspLjd1UXVUrWpoJCxTmG9YpfgR60IANm5GFMa1ohERqkIdWUZq67xb5LBosoG10dWqNnUuXE86ngjc0InyLAiiTNpenAo35yFYEtcLc5HYiQ_uSORZFLkiTKWdpnngAL5NOK4UIiuqOqnduvC9X2GhsbgDKxbO7Hjm2S9d98IJLoLoj7Z9QdUwveJYAsqjMJZRBsIzXH3zv1uqIhlWVaQVb1dY2sHyhGvbdmzjghbZbmFJi_e9K0aaauRFMH4cRAlpMFEdFZE01Yeu_ujBvSTOhOunief6ZvBRQejAlA5XcjRZ2_F9204TO_D7lRoVd8ycjqnQ6BHiPLe548S-l0ZmhFHRxgCR96i8kB_WnrkPGTBLYgIanahQAJ_umIzxkMjH0BXMEfzLx4OhT5GdRTledDtmcOa4iscn3z79B_aVXIL_2fBKJ13waQ7oDb0Wh1XqGOgBZnJZSU_-rDZehcsaWai3AcMBeGiKJUTQpSKucj1kein7DZGamkQKQpOxzyRE2wXz5g66ZrZsAHS3BBSNDiH3APGubxA81iUI5Gy7YUjV0tyyb0FRv4CQ6nW_MrBqCATnh0XHCwKZBE7u-LIXnVGl64BEHi5XabJhmodgEmMH3JEhO6pgDRJ5j6qUJulHiQ3WzYV42jUkR4UqTfL9ik9fLmznlTW6xNeXd17ydy791OT7T8F-L-zolRrqaR-T37JPAAq9kPKSfeezT0uYGrsqOHtSFilP-WP22Vdfz4K5N7r1EQfZlRXc-vYl3ArZi7qkG88g6n_yhRrh4yHtdAuGKmTtkAil7EBZ15vHuxWu3TS2utnw65lOkY7qMCRPDQxLY30iK8oNoU7eskCL9r__K_OMitLnUSbs74bInygABsTdhbdfjnQAYB_gti2agTvk__GgUKSyuoiEor-sy4xh7wpigboqbxjPO8yi9jEsjfoFKj22PXBdjHolQehBRl-h9irDQOFv_x6siQvGAzx9IVU0sC4UECIGG13RoQIh2odGKgvR4SM9oXqYBLu9KwQ1VtzzwdG7npN5nhHwUcXzgCr-piom2DMSDMazddGh9R2DcpIWnY2hDCVAs2xGC7qkBwCXI1zgpQWGDlPIH33tBmzJN-eqewTdYCt5I1aWysHMVA6GwfgbXVmh4BQxH3yxtCeCzULzR7Ya_RLFaLwU25Iem7MvOojHWrRxFDcrdmYYp1nEw-znLYiwpfdjhsxZaPwArEoMuWc9-BV8oww2Tavt6s2G9nPLmwzsM0SEOgZUFtQawnakviGsypBWR9GK8aLaCI-jenNrBnAYR0d5XEF4r2b0XHZNAYg300sA8HlIWemaAHsFLmhh9vLVY5h_hTOo1PaxomtlmeM89fL_gmnb6woUSfI1ECkLjELVfBsqfig1NvuLIt_ytdSbpvZmWHcQ_QakVvbyPYRrKDXthFvJshghLA9suwc6ozr5AVmeqH1ruiLKAedALMD9nu6oHD74lftUuDVNx47cKHVjz5ZOT3MoeveO5fg6NttWRdc_gIlsyjHgFV2d2XVQF3f9Uc8csu3wzKNH8TxOPnz0CD4nFsQX8NeZuzb8-bxYrmQLeECvCub6ESgpYGQoH_QNRMiPP8S_kWfZoUdXwgj-fFVfg2hrLIR-fFOA8KdNTQZyRMKMse9iFABFTzL3PRzCcwPLiZG2P7eR-48kwu9h1o9BR5sB_l2TZejQ4CqChhlNeMLkJmEU2QDHQ5_AP239qLFgBGuP7RXo54-9hOy63oKrKtZoEujNVo7xMXlStA2lCi26ejRr6-Du5OBZWTT3HXSYAh0cxMIUwcKIqwKc4paclgKxTjyPwEErHHxAVOfjWimR9-Z-eJimF8ydfZqKzvfodcjW5jQjBVjVzNHa9iV3MKa9K4NnK9TSVkH2Tb0xFgmEGLxDJ6dsTwIxeZiGjh0HttnUUV_GIT96sNXCBI6-CJxUJiKKetMz6r4YTM-9-ilMjGtz4aZuGEbuyE72LRa97XmPpom77ImCcftA9JbZ88hHFXTnrvshfbftDzVm2wGmaG1ceorMjXkvBJtgnh-hVdDpeWR_ODIjjx4l89CjlyfUM5AO2HnPTqQ3WvK-z2Oknsd2boBd7EA25WsBSwoPjE0rCS04V7NQlhZ8WAnEqnW1hAc2jcxl0-y-in4U5w1ahXEhXEnR-hICa_pNmrNvao022lV9jTFrq_JZJs7k2RVX2gxR9ZrUCy3ooCe7dnxCJ8DvcoCSeeRkffw-ak05lEs51GyiqeY8xcZrHod20IdkQ__JXSrx21tHjJcOYscJgiTwXTmEf303Sa8p79EIckBR3goQ2X_807-AyCCe7_hrxtdgOLtBW_b_7tLQEeWIxoCdYVuL6jcR8hUhXlXbXczc3peMjl0VmQHF31Tan6Guet7c84ymK1quNhG7xEzUi8TWsOMFQPFmPMOsFlsMwYis48wdR5FF7_UhefwEDcmUTeCJCEXm2QD7-ihp6NLpbcLxDTaILTQgNs6eYsAbUkB9XoEmARC_XgOULlQwc-d2UhyiAkHS7R18bSJeVinzk9IYRWOSRBManYc8iWORpIFI-gzL0P9zQKOnWnc0YdeLRJ6k3LUpK6_SrkM3z6DUR_fi6IFk7qaxSH0vy3vwNWrPGVn3Y5trDhp-wyLccfv3OeKt8fbSwxRKAujuah0Et9s8L0ShSq1OgDcofKMtHQLh8_FGA_jjqtJiMSLVpxgs5ioKZaE4A5dEZzNUQOlAfNYVbV7IbAeTjSbguRN8Jwf4jn8z2-4e294U2-6Y7W_V-SAkaKA6xK1wBe2_CkI3DaA6RLJahHJq5LgZdnZCEWKQIJGFTuI6g2sbWqd6MTq-8UmHFyrbIVSaH7V6LynC0m3WU-lTP3XeYTocJtYCCsjRuGz6BbmAGB4GlGoENCYIMMjMkAGYlcWl1PmuYYNbBjC87ntm4Btln2kmaEhasjkU3PfF1JILzD9jPLwB_UEszjuYqWCYlxrt_yAUOhsxZ19UmLBpTTxT1i3u0VVdginHYTAfkcGqUjDWp8LauqQQCPkwaTMMCmBFIA5qLqeyB3biyiyXXmz3mbBRi9khtHKoQazPSXvYRxA5fsgN1VHP2GDYjmv6MjhFxjLIct93o94_jfrATNPSezRy5dtylEN4bDDUACyR7I16K7Tn7IXyZdda1wjXYgwFFq8k7AtBY9FSEd6o-8VerEkFjSXfGL8IKCUxtRpYnf3sH953HxNHd7zpeAdfCggTI2GanMyI490EoTFQddMXPkZtHYNj4KamNKBoYzXJEaMG6azgDFXBGjiaVQAMSIkGbaBrfeZSKbmSilasAGG0mplqhsk5OiJn8m0qr1iY9LMOENTJOwusRqdAvKodGciRyXVdaeWlnILOrV8XmL4FwahqwJ0tbCAsMS7Tml3D_Ce0yuaek9t-HMeyRwyjzr_-RNPxrXuODr0wbwwuI-mTAZReRZ9hUqh9o4u5pbzGdP6UHlUrX2LPFHZRVeB5fpE6u42M8pJGh6FL7WNoMuO6gCq8oUnGKZguMoqldD5UFzGJkcc7NrqFgUBWDU8tCgmEQQ32RAw9FlORmBvkrvSyMKZ-GoVfh77GA7btUGOiyU3wTLhRAps5EB31Kg6m7Zh2Q5NWETwJo9DPvKGkN-pAHMG1Y5sIb0A8wL1uKAGOx2mZY1uh51uel4B1GLX0IdtR4lixHbB63Ow3Z19W9XWl5oQW73dOMveS0J2zZ1W_533qQ9kVjLQVK9T1BQalAs-Gqd1e9JCexdpaaWpeLNEDUpn5Esej_WElpUJVGg2bWRi6wuVKBxu6qwzf6YfV81UyfeWawjTVSbC1g5CvrjWZ1QI1CqzA93dWBKCebwHk2V0Ntb-_s-dOEjqKU5rJY6plmTmTW8HwA9ioO-BKPWiMqllJUI5G4Rdc0yBxPWvQOtIaJLqtAMuh-d1VrwmFEHYGXjl0k0AOSZ6hZ7QP7I9v-6RGzFu2SYLRt5Gc3CP5Pp1BOzf1W8xiU27cCn3HiigF74ewMZjNTua2g2zB6iU-foCNcQO4NZYbk2sDmrrwi2m1hGgmnme5foyfXcfyHB8_BRCQIzE3mcehoeoG0dtZuPO-YsziAHNylm-7lh_GikkfAgm4M4-jlpLw89AlcvE8Cf1Ek1NtCloizyG-qpcleMorqjUEDlENg9CKQyQWRJEVB67iLiFyAEjimOjClSCw76JL0bbUaQJ8Wwv8rRFyoGzPA-LTDwyfWsqncgcRj4IwT5IsdXoEOOr71aL2Pq27uq7TqDqQ2DbYdVZiZZIeN-LXoZ4BsNuC9KFXSSVCeuwUkzoqAq8KFmhtRp8JbI9i2bbR8ONP4048AO3pdgkxQ6WghqyWBQQCDcUpYHzQmivMhTdfi3KLtqXPKY41nafwwpT78tI8dhKH52HfPjVqSj7gvqb7ig1pPwu4l0SA83t8Mmo1HpzY_XqHTduI7UOEY_NABGnfGzW0Exs8_h79wbu2_PGoDYe8HrgTRWRm0BDBQp0hGTwwCPCoKmw8oTXq2wSQ2lrj_BK8SzWo1hqqyKY1ExOueg70Wx9SgdOhMwBewDm86uHqoqd8Ada7bOWrOXtyx2AwTs6BOrqnGmvUFHteyeF9_BmPvMDE90Dp5QSQB6Ap5KYzSXfTAsCB1mot8VnkGq-XHBH9FdxB3W716mFRDdVI4Q2sQWVyzj7frrFUvkEnTvuDacBRDDTg9A3vVlPhKAdg5cdRnHhDe93Q-X2wR-pwK7dJtWWRK5M4jmTSK9Oou3uQ-Pu1axuJF66dAZwMorCPnkcd3Jrq-7Rkb8bFjlFKQJPQZs_IyZx9Uqs6HhicukOMIFRoU9yVmkOAZAogppKrK6ZrquagJFWoRyMb2a5ICAA0UY5jnAujnEpjci-N0jBsYaHMhbLLmC00-ZDx2yDfqON1rmMGFfCNUBpKTnuhM787mjooqqrlEpRsKXVGceVuz4tR3D5a1xPKKdobJH_MXFvCmsK2rCikQVEXYrtGjZLYEtDKEgF1KTH6peSMWrr9erMZKsXFAReyGylJneVCm0Xqgy2Fyrup7DWC3NasDBV9AV0iT9cFlngr-jws-0wlycZ7B352W2GiCzPstU7S6Vw7WrGpkDYJcxHZQuZ23sckw6GAA5o52eVvdN53hJPm3HGSfEhO943_Y9U8tmvflIDDIIAIMhLg_npQMjTyj-KqY7vwZ_oytXDPsEXcxp9hwqUYhGG2Q3V25Z-3HHYTgmvAOjTE_Ke2rrQlVyGedpdDmIdM7JFVz8yunFePd3tv_WBGCRvdQ_fe_JuB3IOMm62ifCoaI_Kvbb1thGSq20tXhIyAWAaSbvhNWfNMO1oBqogdYIjhdKsWmJEWBIB9Vmg1G8wn6BRYM5pgrwYLnnFweM053Fxc6w7zBSwiistCz3e-uYFF27OP2N48yiRhl9jbVPGdRf_OmB7xf8cb1ONfiMVgzcdvvaWCP_6KEnzH72BJwGP9r2B9rH4Fi35Ti5Jy-9f3fjVrdP3nLaXH9I3nBViFJmMvwTT83_xVLezEW4B-yubAz2mtEI0Mv6a1rSjKvufvab3XSU-Q6QIrMXccxlF9fIeGevt9ffDmCaX7qcqhSxCg1Sl5c20SKDcx6xSHKidhvhGGGJImOhQyaTuU7aKvhGo7g15Jza53vEOMOFczMcvy5ux6hUd7vuaXctfgaNaIjQNcqDYS8pugGJglLlRWEAMv_EoNbMqo4OGZex9mmviROrWm41NK4xM645NLb_5HZeP-x7H640g9tQvn17vPG73r8NWDnLAKcxdjxkyGIcD0IPPDLIy8NHVsiVnSNAkj15Z-ZOd26OUhKDjEnODspeOmPE38w1O644yVG1x43h1nrPqfLDydsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsTqdsfobO2Ml3cRxI6wV2qczVv8_z1iN3NI9upus8QkNXQobTmLp_ykl7WGYWHHs7XEc26Fl2-GdLOtTXCOeTwe6Tge6Tge6Tge6Tge6Tge6Tge6Tge6Tge6Tge6Tge6Tge6Tge6_hYOdP34638DnD93_Q)
