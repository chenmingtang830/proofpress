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
All 45 formal cells were scored; every model call had one terminal receipt; PageIndex made no scored-context contribution and cost $0. Retrieved receipts, evidence atoms, authority candidates, and derivation results were labeled non-governed and had `admission_authority: false`. Authority candidates defaulted to `normative_authority_confirmed: false`. The deterministic calculator accepted only decimal arithmetic over declared variables and could not execute code. **Human Approval** remains the only admission path.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzRkZTk5NTUxNWE0N2RhNTVjN2M1ZGFjYSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjA3MTljZDM0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84MjRkYTZjMzVkMTg1MWU2NTJkM2NlYWMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzRhZDZlODE5NGJhYWUxOTA4Nzc5NTZjZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXeuO3Mh1fpXC2As4SncPi2TxMkJ-aHfl3cVeJEvybmJ70SoWi930sMlekj2jWc0C-ZcXCJw3yIvkTfIjQN4i59SFZLemqVFr4AQxYcOa6SZPnao6l-_cxm_PeN3mGRftMk_PLs6226WfyjhmjDLuhylnTISCpVzws9lZUqU3yzRfyaaFZ5s1d1lwwb0gElHgOkxSR8S-T2MpAxqEQSpDGoVU-kHkuW6WCZ4FnCVeFHmZTJjvusIJYqCb5o2ormR9c3bxFn9ply1fwQoFb3GpGfyQyAI--F7WeZbzpJCklld5k1clWcPzVX1DkhvyvK6qbFvLpoF3tlxc8pXETe19XFd_lrDdXY0E1227bS7Oz1d5u94lC1FtzsValpu8XLW8XEWec773di1_2uXw83LXyHopqrKRJZxFW-_kL7OzteR4iE5IY5F6_pn-ZCmv1ENwuHIZuX7KA-GxlEaMyoC5qSckF8hZVbe4tWWRlxI4tzdSLH2eBjKisZ9wLmnsRGEYs0BIvR3D3VLwbbMrYMMu8imqOm3OLv749sws__YMbrmqG_xJfy3TZQJH_sczUaXyzdmPsAMrDXi97S7NZXPOt_LNHNgp27m84sX5F8--f_riu6efL3949uLr337z7Ifl9zRc_uHpi2fLL58--f6fli-evvz9N69eLjbp2eyDxIu3bZ0nuxZudZnwJgdWz2R5lddVuYHll_A9iINUZHftuqpxK5d5iZSbG_hmA9-UfIN3rrc0O2vgZIDe2UW5KwrYoFjDtUp9MElRiUt4lqchC0KGkgg32so3uP3f_Ndf_uW___0vfwcfmiV4mqq1tyh68ho--eP5-Y8X5FfkN1VycUXDeZu3hcQ32putEjxe87NfZv1KieOmjsOjvZW-QNEvZUp-qOrLrKiuCdC6IH-QdTX_UvKrG_Idb_MrOcbJr8h9qZDf7XiRtzfkM5mDoK16blFW8YMhwyxImJCB9-AMHx5d0_J214ydnccky_w42GPlpXqN8DIlqRTaICTVrkw5GJOx8_oVec-rI4fisjSKZMYfhJNXa0myuvpZliSDM5u3vLkkP-NRrtVRpjlflVXT5oKAddoWEhSA-OzcZ6QZOS2HCZ9HcfYgPB5eViqbfFWOXVYasAj-sy83v9Xb1G-_53YOnx25DpFwSt3sxLVuyZM3eUNu7Ypg4naS3P6pvCXz-ZyY_8VfX8HN4IOvQeyL1HfZ8sn3PWfKdO_xFdKQspjz0_g6PPONRNOVN5vm7_5UotDAh2RlNZHXG5LIVV425Bpc2cjN-FnkMx6yh-EK1-dFMSYKbiwTHvl0b8Fn-j3w4uCy2vfIwjsPj-km52HkONGJq92Sz6oyzdEFwU1_K3lJ6l1Sg_I1OyHAl9hPDXGyA6dez5USjclCkALYCUV6Ilt439UWbgjvOc1TUlYtSmqeAkIiLXy7vtlW8C84TfiVt0BzU13B4ZB05GriJEwZ85wTuXpHRMHnFqM2PHYyGTnB_oIv1EKI3xSB9wjDu0-PSIOfeb4jIvfU9eCy8RG49JcbOJN5I0HXbntfq-7klrzg1yAQ9RZs68BwjMlD7MSA4Rz_VMZQIFIAokJJKly6egMMMzCUAlZaHPDYIWzSFGNeI_I5HCM_la13ABGazDGBEA6LkjiIjyyI788IR4lcoZUTddWYvTb3lpP3EBn1LG4kBU0emDvtSk4Tqvmox4mSLIYA64H5fbWupVRvN2hXeI5cIkQhYPVkTaQSLEVHYYvOVS3It2MYIXIpnO5Dc3sogxnPix0YszEx5J6bpNKVe6x8VuctxJtVOS9ghwUxhMggTHmPDN6PwogApknmYaz4kHyh6WivK4UfhHV2DYFAMt0JOOggIMKuYNGnbAjEqOvFmOnwqetQTh-WVbBsJmJTXq7atvkm_5krq9fyeiXB0ilbWEHIzssWtwFasSH5GKsQhAkZZg_J6juWr6rGXWEWeQFz6L7le4JhNgC5Nb_Kq1opE74PNiHBpMX7bN49Xh8RtowmPI6j7ME4eqJVFi-Osg6rzpV9E7IomhmRb6TYYVaCbHgqicsszho5ucAVUeh67oPx-bKttgQDUJAy3vMMEZbiklxLkAMF8dAOAWX5ZlvkIm8viDfCZ5hIGnNPPhifhzImICwcDcJCjwfJAch4VV3KckYwtVaKm5niAAkRvgNT8B4Be-_LY1gsiAVPE_FA3KDWiwKh-BU1YoRGQYmRxyIIpt-ArNXVrlU6LDfbtgFUBAtd8zGEKpnkSZI8EJfgxhUHEGUaHuDHr8rtriUtEsVfn-3avd9VfAFrjXl6yiM3FQee_nQ2v9GvIJAURY4Seo0hABhbSSC-ueswF-RTKfiukWOG1oO4J3b4A3F5KP_aovBSjObc3DQWfsbkHSksfPVecn_H4yOS7rmOR5OQnrziEzh7sD5ZVQNAHBohAPG1TB_vIS6BN7XmYEFKcOxj1-HJmMs4ECfz9W4eSCeRxo4_CH0w1-H-8T9XYKPtslDvOf47Hh87fhEz4QfBySt-LeWWfFbwfEO-qPl2Tbh2CF22RfCyKnM4ePBWSdPWGISjGF_KseP3Y-4kLKUn83V4_Da3Pooz0oSKKI3Ewar5FTINlCFaFJr7WmoMmCc5Jojfeyf3IjFyTzQEulxGD8oZuoUtbxpMffyEme4M7kl5BiBS1S2auNfnW73KebvZ7td39k7xx5mtnZzBxePtLEUtua5AqG9sVUMuM891HTdzHfD6sQySxE0pYw4ee1m1iqYp7xBT3gFgK8XltsrLVlWrarUSlinsb1il-BHrQgA2bgYUhrWiARFVhTqxjNRUWbvM4NBkDWdjqlVNQi9cT1JPMDegYZYyFqbS8aJEuBkPwJK4XpCJ2Il9cEciS8PQFUEinSTJGAV8G3M8KURWquqkb-vC936Bg8biDpxYMHeiuee8ct0Lyi5Y-PeOc-FgfsicOJaAsjCIZJiC8PSfvv3fLVUpGdZVpDVv1ljawfKE6zhO5OCB5ul-YcmI970rRoZq6IWwfsTCWGmwojooIhmqD139MYt7cZQK109iz_Xt4oOC0JEtHa_kGLIO9X3HSWKH-d1JDYo7dk-nVGjMClGWOZzSyPeS0K4wKNpYIPIRlRflh41n7kIGzJLYgMYkKjTAV9_YjHGfyMfQFcwR_JcPF0OfItuZyvGi27GLE-pqHp88f_qP5Bu5Av-z5aVJuuDTHNAbei0Op9QS0APM5JJCPfmTvngdLhtkod8GDAfgoc5XEEEXmrjO9SjTq7LfEKnpTSQgNCn5QkK0nRNvQdE1k1UNoLtRQNHqEHIPEO_6BsFjVYBAzndbglRnhlvyHBT1Kwip3nQnA6eGQHBxXHQ8xmTMaEZ92YnOoNJ1RCKPl6sM2SDJAjCJEQV3ZMkOKli9RN6jKmVI-mHsgHVzIZ52LclBocqQ_Lji09dLh76eDT7im8s7P_L3PvpznR0-Bfe9dMLXeqmnXUx-Sz4HKPRSykvyvU9-W8DWyFXOyZMiT3jCH5Mvvvl2zhbe4KtPOciuLOGr56_gq4C8rAr1xTOI-p98pVf4rE873YKhCkjTJ0JVdqCoqu3j_QrXfhpbf1nz67lJkQ7qMEqealhWrfW5LFVuCHXyljAj2v_xb8SzKqp-HmTC_qGP_BUFwIB4u_D2q4EOAOwD3LZDM3CH_D_uFUqprCkioeivqiIl2LuCWKAqixvCsxazqF0Mq1b9CpUe2x64KUa9liD0IKOvUXu1YVDhb_cenIkLxgM8fS51NLDJNRBSDNamoqMKhGgfaqktRIuPdISqfhPk9q4Q1FpxzwdH73o09Twr4IOK5xFV_KAqJtgzJRiEp5u8Res7BOVKWkw2RmUoAZqlc3WgK_UA4HKEC7yYgaHDFPKn37qMrPj2XHePoBtsJK_FeqZzMHOdgyGw_tZUVlRwipgPfpkZTwSXheZP2Wr0SypG44XYFeqxBfmqhXisQRun4mbNzhzjtJniYf7TDkR4Zu5jjszN0PgBWJUYcs878Cv4Vhtsta2mrbZbdZ87XqdgnyEiNDGgtqCzPmxH6luFVQnSalW0Yr2oMcLDqN5-NQc4jKujPK4hvNc7eiHbOgfEm5ojAPjcp6xMTYC8Bhe0tHf5-jHsv8QdlPr6SN42sshwn-b4f8a07XUJiiT5BogUOUaher-1Kn5oNbb3iyLf8I00l6bvpj93EP0apFZ28t2Hayg1zYhbSdMIISxnjtMBnUGd_Igsj9S-DV0RZoBzIBbgfkd3UA7v_cp9KtyGJnVCN0zcyHMk7Wj2Re_OsZxexya7Mm-7BzCRrXIM-Impzuw7qIu7_tHPHLPt8MyjR9Eiij959Ah-jmcQX8C_dOE68M-X-WotG8AD5lQw149ASQMjS_mob1CE_OgT_Df0Zk7gqU-CEP75proG0TZYCP34NgfhT-pKGcgBCbvGoYvRABQ9ycL3cAnPZTMaIW1_4SD3n0qE3_2uH4OO1j38u1aWoUWDqwlaZgzhEZMbB2HoABwPfAX-1dUPGgsGsPbUXoFu_9hLSK6rHbiqfIMmQb3ZyCE-Vp4UbUOhQ4u2Gux6dvR2MvCsJFz4FB2mQAcHsbCKYGHFdQ5OcaeclgaxNFqE4KA1Dj4iqothrVSR9xZ-cJymxxb0kKam8wN6HWVrM7UjDVj1ztHadiV3MKadK4NnS9TSRkP2bbW1FgmEGLxDK8dsTwwxeZAE1ImYYy910JdxzI8ebbWwgaMvGE1kLMKwMz2D7ove9Nyrn8LGuA4XbuIGQegO7GTXYtHZno9omrjLnmgYdwhEb4mzCH1UQXfhup-o3x3nE4PZ9oApWhtXPaXMjX0vAJtgnx-gVdDpReh8MjAjjx7Fi8BTL4-oJ5MU7LznxNIbHHnX5zFQz1M7N8AutiCb8o2AI4UHhqZVCS04V3tQMyP4cBKIVatyBQ9sa5nJut5_Ff0o7hu0CuNC-CRB66sQWN1d0oJ8Vxm00ayra4xZG53PsnEmT6-41maIqjdKvdCC9nqyb8dHdAL8LgcomYU07eL3QWvKsVzKsWYTQzXjiWRJyKPAYV1I1vef3KUSH946Yr00iyhlLGa-K_vwr-sm6TTlIxpBjijKOwEi-c9__lcQGcTzLX9D-AYMZ9try-G_-zRMRDmg0WNnuNa8_CBCvibEy3K3j5mb-5Ixsasm06P4m9L4M9RVz1t4ntV0Tcs1JmKfmI16kdgGbjwHKF4Pd5hWYochmCJL6YJSTRa91yfK48doSMZsAo9FIFLPAdjXRUl9l05nE05vsEFsYQCxdfYqBrxRCmjmFdQmAOJXG4DSuQ5m7rxOFYfoQFDp9h6-thEvKbX5SdQaeW2TRCManQU8jiIRJ0zEXYal7_85otFjrTuGsOuFIosT7joqK6_Trn03T6_UJ_fimIVk5iaRSHwvzTrwNWjPGVj3U5trjhp-yyJ843bvc8Rbw-tVD6tQEkB3W5kguNllWS5yXWqlDL9Q4Zu60j4QPh9eNIA_ristM6JIdSmGGXE1hSLXnIFLUrMZOqCkEJ-1eZPlMt3DZIMNeO4I3_ERvqMPZts9YNsbY9sdsv1czwchQQvVIW6FT9D-6yB0WwOqQyRrRChTjRw3_c2OKEIEEiTSgMYu7V1b3zrVidHpjU8mvNDZDqHT_KjVB0kRkuzSjkqX-qmyFtPhsLEGUECGxmXbHcgFxPCwoNQroDFBgKHMjDIA8yK_lCbf1V9wQwCGV13PDPymss9qJ2hIGmVzVHDfFVMLLjD_jPHwFvQHsThvYaeCYF5qcP-9UJhsxIJ8VWLCprHxTFE1eEdXVQGmHJfBfEQKp6qCsS4V1lSFCoGQD5s2w6AATgTioPpyLHvgxK5MM-lFTpcJG7SYHUMrxxrEupy0h30EIfUDbqkOesZ6w3Za05fFKTKSLM183w07_zToA7NNSx_RyJXtikEO4bHFUD2wRLI3-q3AWZCX2pddG11TuBZjKLB4hcK-EDTmjSrCW3W_OIg1VUFjxbfWLwJKiW2tBk7nMPuH37uPFUd3vEm9oy8xhYmRsNqcTBXH-wlCa6Cquit8DNo6esfAbU2pR9HWaipHjBpksoJzVIVZz9G8BGCglKjXBvVZl7nUSq6lohFrQBiNYaacY3JOjcjZfJvOK-Y2_WwCBD15NwOr0WoQr2tHFnKkclOVRnlVTsHk1q9zTN-CYJQV4M4GLhCOGI9pQ65h_yNa5XCPZo4fRZHsEMOg86-baDq9dY-a0AvzxuAy4i4ZoNKr6DNsCrVrdLFfaa8xnj9Vj-qTL7BnCruoSvA8P0uT3UZGeaFWh6UL42PUZoZ1AV14Q5OMW7BdZCqWMvlQU8RUjDzes9ENLASyanlqUEggDKqxJ6LvsRiLxFyWudJLg0j102j82vc1HrFtxxoTbW6Cp8INY7jMnuigV7E3bae0G9q0iuBxEAZ-6vUlvUEH4gCundpEeAPiAe51qxLgOE5LqDMLPH_meTFYh0FLH7IdxnQWOYxUw2a_Bfm6rK5LvSe0eL-m8cKLA3dBnpXdnXepD21XMNLWrKiuLzAoJXg2TO12oof0ZqSptKZm-Qo9oCozX-J66n5IoVKhOo2GzSwEXeFqbYIN01WG73TLmv1qmb5ybWFa1UmwtUMhX1NrsqcFasRmzPf3TgSgnj8DyLN_Gvp-f-0saBxQzanayWNVy7J7Vm4Fww9go2qBK_2gNar2JEE5ao1f8ExZ7HqzXuuU1iDRXQlYDs3vvnqNKIRwUvDKgRsz2Sd5-p7RLrA_ve1TNWLekm3MBr8N5OQeyffxDNq5rd9iFlvlxmeBT2ehSsH7AVwMZrPjhUORLTi92Mcf4GJcBl8N5cbm2oCmKfxiWi1WNGPPm7l-hD-7dOZRH39iEJAjMTdeRIGl6rLw3SzceVcxJhHDnNzMd9yZH0SaSR8CCfhmEYWNSsIvAleRixZx4MeGnG5TMBJ5DvFVtSrAU16pWgOjimrAglkUIDEWhrOIuZq7WJEDQBJFii58wphzF10VbUuTJsC3jcDfWiEHys6CKT59Zvk0Uj6WOwh5yIIsjtOEdghw0PdrRO1jWndNXafWdSCxq7HrrMDKpHrcil-LegbAbgfSh14lkQjpsVNMmqgIvCpYoI1dfS6wPYqku9rAj98NO_EAtCe7FcQMpYYaslzlEAjUKk4B44PWXGMu_PKNKHZoW7qc4lDTeQIvjLkvL8kiGlOeBV371KAp-Yj7Gu8rtqT9lHEvDgHnd_hk0GrcO7H79Q7bthHHhwjH4UywpOuN6tuJLR7_iP7gfVv-eNCGo7weuBNNZG7RkIKFJkPSe2AQ4EFV2HrC2aBvE0BqMxvml-BdVYNqZn0V2bZmYsLV7EH9rQ-pwWnfGQAv4B5ed3B12VG-AOtdNPL1gjy5YzFYJ-NAHd1ThTVqFXteyf59_DMeWY6J757SqxEgD0BTyG1rk-62BYADrfVG4rPINX5ecET0V_AN6nZjTg-LaqhGGm9gDSqVC_LlboOl8i06cXU_mAYcxEA9Tt_ydj0WjnIAVn4URrHXt9f1nd9He6SOt3LbVFsaujKOolDGnTINurt7ib9fu7aVeOE6KcBJFgZd9Dzo4DZUP6YlezssdgxSAoaEMXtWThbk80rX8cDgVC1iBKFDm_yu1BwCJFsAsZVcUzHdqGoOSlKJejSwkc1aCQGAJpXjGObCVE6ltrmXWmsYtrCozIW2y5gttPmQ4dsg36jjVWZiBh3wDVAaSk5zYTK_e5raK6qu5Soo2ajUmYor93terOJ20brZUKaivV7yh8w1BZwpXMtahTQo6kLsNqhRElsCGlkgoC4kRr8qOaOP7rDebJdK8HDAhexHStJkudBmKfXBlkLt3XT2GkFuY09GFX0BXSJP1zmWeEv1c3_sc50kG94d-NldiYkuzLBXJklncu1oxcZC2jjIROgImTlZF5P0QwFHNHO0y9_qvE8FTTJOaZz1yemu8X-omqd27dsScMAYRJChAPfXgZK-kX8QV53ahT83H6sW7jm2iDv4Z5jwKHphmO9RnV_55w2H24TgGrCOWmLx56YqjSXXIZ5xl32Yh0wckNXPzK_o68f7vbc-m6uEjemh-2j-7ULuUcbtVal8Khoj5V-balcLSXS3l6kIWQGZWUi65TdFxVPjaAWoInaAIYYzrVpgRhoQAPJFbtSsN5-gU2DN1AY7NVjylIPDq8_hy-W16TBfwiGiuCzNfhfbGzi0A_uI7c2DTBJ2ib1LFd9Zdu8M6Sn-73hD9fjnYtlb8-Fb76jgj7-gBN_xd7Ak4LHur2B9pv8KlvqbWiopd_j5wV_NGnz-006lx8wXL3KwCnVKXoFp-L_5V7WwE28J-inrI39Oa41opP9rWrtSRdn3_HtaHzXpCTKdYyXmjmEc3cd3bKl33zeDN09Uul9VOUwJArQ6Ud7cmASVm5i3mkOdk7C_KQzRJ01MKGTTdijbeVcJNXYGvZLeXed4-xhxoXdij-Xt2fUaR3u-5Zdy3-AY1hQbR7jQbSTKb4JiYJY411lBDLzwV9XApo0KDs_ce5gpklGSYq9EkNIMIpGIMY-5aixHn-lwSmk4oTOcXHr7V5WN-49jdeNIHbUL-svd80bvG756kAmrIHMxZkxlEABMZ6kfpEHoJQl1JGZJkzgIXUf6oZM5gZcFoOAQc4Kzl9RNeBL7x7d0x4yVyy48744ZqxAOCwIHZ5qxmmasphmracZqmrGaZqymGatpxmqasZpmrKYZq2nGapqxmmasphmracZqmrGaZqymGatpxmqasZpmrKYZq2nGapqxmmasphmracZqmrGaZqymGau_tRkr6cbUDbFW6EwzVv8_Z6wGbuke3U2z4YSGKYX1k1jm_5RS3WEQz6LIO-A4coKZ4wR3smymuAY8TwNd00DXNNA1DXRNA13TQNc00DUNdE0DXdNA1zTQNQ10TQNd00DXNND1kANdH_h_aPZhI1wD4kdHuH5vexN7sdbw6omFVyvUrFJl6kyl406Qdefw1XdcVy0OX1E00dOAm1RxlE44PO8sg0ktY_UKmGlVefaD5qxcP-UBVjdpxKgMmJt6AsDAsTmrbkrn_XNWD3dl958Ne-9kVT9l9FeZrMqkgPPMAuryxEkgkhMuvB2ngZNlEIgjrJaSBdR34yxKKPhGGVOa0iT1WUJ978Mmq6ILh94xWeWENAY2_GmyapqsmiarpsmqabJqmqyaJqumyappsmqarJomq6bJqmmyapqsmiarpsmqabJqmqyaJqumyappsmqarJomq6bJqmmyapqsmiarpsmqabJqmqyaJqumyappsmqarJomq6bJqmmyapqsmiarkLkkpZJGQEOk02TV39Jk1aNH-82_jx5N01XTdNU0XTVNV03TVdN01TRd9QDTVT_-8j_8ND4C)
