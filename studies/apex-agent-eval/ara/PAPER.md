[//]: # (ob:f92973e3)
---
title: "Governed Working Sets for Legal Agents: A Two-Task APEX Pilot"
authors: ["Chenming Tang"]
year: 2026
venue: "Independent pilot study"
doi: "not assigned"
ara_version: "1.0"
domain: "Legal AI evaluation and governed agent context"
keywords: ["Proofpress", "APEX Agents", "legal AI", "knowledge ledger", "claim staging", "agent evaluation", "safety gate"]
claims_summary:

  [//]: # (ob:9846ed96)
  - "A governed working set can preserve majority-scored deliverable quality when its staged claims cover task requirements."
  - "Context bounding changes executor efficiency conditionally rather than uniformly across models."
  - "Pre-execution state validation can prevent artifact generation under tested material conflicts."
  - "Executor-only savings cannot establish end-to-end savings when upstream knowledge construction is incomplete or unmetered."

[//]: # (ob:56043bb3)
abstract: "This pilot compares ordinary full-data-room execution with a composite Proofpress treatment on two legal tasks drawn from one APEX world. Three executors produced one artifact per normal-condition cell, and each artifact received three native Archipelago Output LLM verifier judgments using Gemini 3.1 Pro Preview. Because no preregistration established primacy, majority passed rubric cells and mean passed rubric cells are co-primary descriptive summaries: majority quality was preserved or improved in every observed cell, while every Task 2 treatment mean declined. Muse reduced executor tokens and latency on both tasks; Sol and Luna showed mixed or adverse efficiency. Proofpress failed closed in both tested corrupted-state treatment cells. The evidence is bounded: claims were staged rather than lawyer-admitted, upstream treatment cost is incompletely measured, execution was local rather than native Archipelago, and the results are not official APEX Pass@1."
---

[//]: # (ob:ce26da1f)
# Governed Working Sets for Legal Agents

[//]: # (ob:a24fb021)
## Overview

[//]: # (ob:f468bae9)
The study asks whether a claim-centric governed working set can preserve legal-task output quality, reduce executor work, and stop execution when a material state conflict appears. It evaluates a composite intervention—corpus selection, evidence binding, claim proposal, policy recommendation, staging, graph selection, and execution gating—rather than an isolated retrieval method.

[//]: # (ob:49dac34a)
The strongest observed pattern is conditional: the treatment preserved the majority rubric score in all normal cells, while every Task 2 treatment mean declined; only Muse achieved lower executor tokens and latency across both tasks. Majority and mean are co-primary descriptive summaries because the pilot was not preregistered. The tested safety gates blocked both corrupted-state treatment runs before a DOCX was produced. Upstream construction cost and cross-task amortization remain unresolved.

[//]: # (ob:a151d404)
## Layer Index

[//]: # (ob:b979b1e6)
### Cognitive Layer (`logic/`)

[//]: # (ob:f8861e63)
| File | Description |
| --- | --- |
| [problem.md](logic/problem.md) | Empirical observations, gaps, insight, assumptions |
| [claims.md](logic/claims.md) | Six falsifiable mechanism claims |
| [concepts.md](logic/concepts.md) | Eight study-specific concepts |
| [experiments.md](logic/experiments.md) | Five declarative analyses |
| [related_work.md](logic/related_work.md) | APEX, Archipelago, PR35 RelayBench, and ARA relationships |
| [study_design.md](logic/solution/study_design.md) | Paired design and metric interpretation |
| [architecture.md](logic/solution/architecture.md) | Treatment component and authority graph |
| [constraints.md](logic/solution/constraints.md) | Validity and authority boundaries |

[//]: # (ob:e60a7d41)
### Physical Layer (`src/`)

[//]: # (ob:c665e5a8)
| File | Description |
| --- | --- |
| [environment.md](src/environment.md) | Reproduction environment and frozen revisions |
| [artifacts.md](src/artifacts.md) | PR36 product mechanism and frozen experiment pointer index |

[//]: # (ob:ca8eab5a)
### Exploration Graph (`trace/`)

[//]: # (ob:dbb4f7c9)
| File | Description |
| --- | --- |
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Source-bounded research DAG with explicit and inferred nodes |

[//]: # (ob:04ddd7bf)
### Evidence (`evidence/`)

[//]: # (ob:2fbf79bb)
| File | Description |
| --- | --- |
| [README.md](evidence/README.md) | Evidence ledger and claim bindings |
| [table1_task1_three_model.md](evidence/tables/table1_task1_three_model.md) | Task 1 exact paired results |
| [table2_task2_three_model.md](evidence/tables/table2_task2_three_model.md) | Task 2 exact paired results |
| [table3_cross_task_summary.md](evidence/tables/table3_cross_task_summary.md) | Cross-task directional summary |
| [figure1_pr35_results_poster.md](evidence/figures/figure1_pr35_results_poster.md) | PR35 source visual used as design contrast |
| [task1_results.md](evidence/results/task1_results.md) | Task 1 frozen run record |
| [task2_results.md](evidence/results/task2_results.md) | Task 2 frozen run record |
| [upfront_and_reuse.md](evidence/results/upfront_and_reuse.md) | Upstream cost and claim-reuse evidence |
| [log_pointers.md](evidence/logs/log_pointers.md) | Direct pointers to manifests, runs, and source records |
| [raw/](evidence/raw/) | Audited Task 1 and Task 2 frozen manifests |

[//]: # (ob:1a7e264e)
## Research boundary

[//]: # (ob:1f3021e7)
The Proofpress product mechanism is the PR36 claim-centric CLI implementation in this repository through `9f6e3f1`. The local harness snapshots `1ff29dd` and `0b7ddf4` are non-public experiment provenance labels, not Proofpress product source or required public dependencies. Claims are staged rather than lawyer-admitted. Native Archipelago grading over locally produced artifacts is not official APEX Pass@1.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZhYTM0MmI3ZjNiNTA3MTA5MWI3ZmEwNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQwZTA1MzBiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kZjE0NjE3YWVhODFmY2E1MjRhNGQwMTQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzAyYzkzMTM2YWQzNzgzNGRkMTMyNGNkZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXOtu40aWfpWC8mMTrGTzftH8WU93T9BAZ2N0emcGiBvqYlVRYkyRDIu0W3E3sP_2BRbzCPtg-2OAeYs5p4qXkluSLSuzG-waSByJLJ5bnct3TlG5m9C6yVLKmkXGJ_NJVS1SSl3PScLUTXwrtK3Yhs_U8ifTSVLyzYJnSyEbWCtX1PGDeUDT1OHcTjw7jcI4dH0RJcyNuc8Dzqwg4FEc0jjhiWP7MRDlfuiwhFt-Yok4doEuzyQrb0S9mczv8EuzaOgSOOS0QVZT-JCIHC78UdRZmtEkF6QWN5nMyoKsYH1Zb0iyIZd1WaZVLaSEZyrKrulSoFJbl-vyJwHqtjUSXDVNJefn58usWbXJGSvX52wlinVWLBtaLCPXOt96uhY_txl8XrRS1AtWFlIUYIumbsXn6WQlKBrRs4Tlu1Yy0VcW4kYtAuOKBU9tL7BDKmhkp4z6jkc9btkeSlbWDaq2yLNCgOT9juQLy2Gxa7sB5W4YuR4Y23U8xlOtTifdgtFKtjko7KCcrKy5nMx_vJt07O8msMtlLfGTvi34IgGT_zh50alM3oHOk_egSe8VuM1NyzMhz2klPs5ArKKZiRuan5-NrGdJm-X8nNZ0Nru8uHz1diaBQcHP1nwyPcrDaNPUWdI2sLGLhMpMogAiTxdUgsEboei1zaqsUY3rrECSciMbsYY7BV3jfm-rMwUCEj1lMi_aPAfl2AquCzTO-2lvnQm4Hy5asFpQzUfd6YUWC9cOPI-5HmXCF5QGURCIwPMj5Fs2ys-6DSTdBhJwJXZdlVnRKH-sFScUov_WyVCVecY2BgXTGwwiys-e6CiyTJtFClYRdVVnnT_KxJ4LN7GY5zlxlDKb2V5M0yT1WBTHQZrEjueAs3q28AIvTmLXY9SL_Ri3LPKdJPJx12RDUZU7sC3-d-JYTjCzopkTvLPduePPveCfLWtuWbC2szOsckPfo2kYTT4bV-_-11wvyUt2rTbk8-fpzqgRPGuGmPm-EsXFa_Ki5OLj5L0KRN6yvbfvRdyXt39uIdX9X4lIJdRTAvJObwM8k8YO1BKB5QEEb8RH1Pzrv_7lP_72X3_5Bi72nDhXIlRYD8QtXJnNZldFkzW5mJOrybdYVwrByZ_K-hpF-EE0kqRlTd6IJc3JBUoq5-SCvLstZ-8okGo2lYpmMN4EPaGXKI68QPA4OFoiQmYgyQVZ9rLcdrJI0RBGC4JbJuobQdb0p7LOms0M6mENCzlUvUGgHArdlkB-YHlukhxvIprIpob9RwO9g_pJqiwvQZRyjWlJEvDUrKBQU1PYnxmnDZ2BZ62J-ChYe8BCTDgBp3a6JdDjduCQuF-RR9PoJMOyC8u2hKOOlyaWY28J9z3QVVwOsf-KGMsOcEi9IEqoiI_m8G4lCAb1hlB5LcntSjQrURNKWE6z9YyBcnXGdvvPge3wYk6xYD1RnrrEoGxImSjn5KSCXAACEHAYzCUZ5gSazwkISxosm2sd9fvkobZvc8_ytuR5Qzeg6usCE-HhTdheeWAfkjiME1tsB-qLclmAxBBkms7XH_JymbHzD98cZvsVOfjkIXeIogCkcH8FMT6RP2SAKz6Rl0KyOqvQ8uTTVfGJQLYj3V_8-iOUAEAGa8jz77_WlKt6FFODC1NIEVg05N52VFyuNjJjEFe9jLJ-jKH2P3bASiwIfOHT6FQBHm8iUdxk4NvorMpMSPuQiRiNBE387TB69bHKy5oqLt_WtFqBkJhTxSPs9MCzB4zFk8RLQxb_KqIcYbGRwwICXZxt6PqQxSxAnjxMtuvAq5uMi4IJkE50Hx9jq31PHbCSAwAWMkByIvvH2-ftq4uX371SzjTQPmQfm4ZQKT2xJeBbwAC0ZiuSlG3Bofo-kA53rT9gFDt1ofiJ8Ok8sSqMHTbRgLcha4HwLZNrrAtYCi7fusG9yvXiflUAyKtW7MV896ToOqwL_KqYqEdIIpZZUWApvJrQgq0UaPqO1te8vC30mqsJaUr1iKSYeX-BFQCI_0wURiUInFsdOxdvL872Ab6HxEkhoTRrVR-16nIh2_UaMRTCtieLYEC8J1hkgHn_dDTKU-LcZs0KUQg8UUrofczt7wr-CeY10OLxuj0OEZ4gnQEXj5euB1kn8DfA5PH8TwGUWw1JjsacNUCFlG1TtQ35uaU5dChTcoJuBjB9qm5PA6eDYpp4326Ruk3QHqrrIllxim4GyD1eNwPiniCCgX-PF2E_QD3FmUcofLxEe-rw06UxMO_x0uyBpqfkwREB_waMY6Dd46U5BEVPkMmAvb8BCxno9gkW2glDT5DGALu_AdsYyPZ4ab5Ao6cIMsLdp5WYpyLdN69Jtq6gBYcLWjaoJw3Cr1ooFIVnVc2qPla39wZuv5vcrjZbOgw0pqR3q5my4iGqvQBKDQ0XVHeHA_lHH4scONDSljbPO8ypv3kGcvc8An4eAT-PgJ9HwM8j4OcR8PMI-HkE_DwC_v8wAn78Gzb9GyadTHM7-rz7VZKH3qb5VV6Z4XacWn4oQu5TO4ljn7KUR9QRYeA54HZOykVsWVYE95jrepHPhZcGIg4txlLX26fQrpdngrnl7nh5ZnjH7Df28szdZEXlChMA2Ch1qce8yIEFioYB6DvvOw2py2vd3Fwidr2aXBX6RRRY8ePV9ksnV5P3V8UGHH1O0L5XBXheq3gimKgE_MHpoMLACoYhNV5muALaGABlMluCZIpJTRedyfG2fWbpxWuaqQudrK_NbosWfMRuuhfrQhCfvRabW3xdT8k9xtfVBKesSsN-nI0X8o6-_nZdlLe54Euc1cLfWl9VsQeaUGhql_rS_Q5QX5U0Fc2GLKG5UzbaPryY74By3f5GTuqkri2iNA77_TXao25_T-p7ACLV6n26buaMqBigJ7gEKgZrtLBEvTtK1JC6ez8TC7s8Q9NqAV5oW-sch-y7drM76wAHE2masQzS9sYEtvmGQM1DIN7AA6QtMnDGNVylrC4hAa5LENNkdFmL2Xh-gkEuCFg849oNOo0x7ZE-vAjsi-hqNzbswEu9CQYWAaidwVaDQCmktC2NXnWCz8oCxJH0BrSSSB-9FZ4Hu2VyRcCxZ005g_8Ma5QR20oiXF-T0X3wZdamhnSuZhaSZAU2g7kADcA-LYAlEEdwkGFHP9o5RcyocMNUxFy9_aqcwmhRO6c4qfd87MEUWBgWNrelPsNQ7iEJr-ltgad1a7grdPYAl8z5GXm3AlgzOERf3GAfcOGwWRXsTwE-QPPZ4CeEiTyfqhgXFCrpsLgWTGT6sAFpF1Sh_guotlklcrosyff6UOXNm-_IjXq3Gcj_1PKlcmDSSvTVbwWksYy4ZzaqCf-qanxGfi8YbSWQLdGnarHM0KxKoMEBsGWrszVlm-l42lHhq3u8P_RA4aUSfi3QPXfdrNE9ZooSbAvvwRAooxMF1Jn5SH8IVyqNAxdwomwNRsXPGYiI73uPjaU24e0K4Za-pdK7Y2ynEo8LhiUc9us71B0cUu3REMdNeS0KrQ6-PY7xDPZISvAX5QG_Iz-Uubr9pi0okavyFkMt-6glpBwzuzDSwZnpWykF-TDvlFJroQnreIW8VbcVfJrpuB8lV1ZEDxPDdA4jrBvQzfs8dgub2Kc2M-3k9BZaoBnl6wy6bz4do9dgUUKbvhW1kBbAYrKt1VBwDB3YFCjWEBEmiy9dU_szgjnQvM0b7QWYXUplGyxBqvaCv_yLrTITFPP99UJwO_Wo8JIgsPvUYAyLutRw2pynY-V7jmt7gAgt1SYpVsbop2f10Eyno2YHgAtdZvFUjS00kBnHPB21_4kTV-3so68jDb1Nsikrc48xxdOxgGh_7MsIoQC2aQ0O-XrAA5B1zXQKYBeFKZDaf__7f4JnVy1UXZELVR7GITNJMlVQp1pPTJpAgkIoaxSOKbBcg4fqAjjtIcmULFWbapBU6XNQAQAJLAPeppdSLEwlxjUEiACDovTg5QD6-Nl-1wsjboPXeT5zByhqDMa2dvAfe64MiKKrHjonHJPxfkdUqVdpD6oM6A7cckhf9cHs1yGVMQNC5uzFG5L-YxI8Sbp6gxrqio25BDPCUH4UQFB5rsuJBryU-qAFLipZ9mfLui2QWYo2o-Tl9y_-3FUSXY_PyL_16W8LsqgMiBophXUE0TX0fdkvuigCLASEDkgG9qrMwXoHXCYFFMsDK7LCYAAyxuxyTCEPTiQ7gonHmGtTK47cqCdoDCkHgsfPGjsGAfSRMWM09NMh6Rnjx47BaVPE_so3sPLVuspqNaDToaJsDA69pBX8zQrol1bNFBundq3YyI6wLnYG3eECkv0h-whVNpf9z7zG0UJXJDsiJSSfqtkiM15S8iF_nZJnshIMCDLSrxmHWpAgdbMwEtq-irT-gLuBcUhrXScppICNFD2dWqictMCEbBC6dxkpYcmcbpfZy7euT97Cl83vIWBXOhHi6Zx6HA0Ha3tOSp8FxCd0owYn8GeVNs_v3UeWlzTT_RRe60Je1SKV5CF0u2NKzQBHQVABWAO4YReDe_eRwTsDhEABKVRzA2x0M455Ruf6YecQpmbbNh_ob99G8n_E9qnPViPNblyFienTrkFbHxZu5KYMUn-QDHFnDLyNuDtqdN1HtZ34oRNRmqihhgY14zT76KDbNZfevoYWeSu6wZuC-uNtZSHobX4RxfDzSDnsq-5J5EDXvKL8BGd2X070DJpjYBD1ezSwUoaJ7-AGWJabhJFIBYuGvGSM040NOH4m3rFwOI-TIKQu51bPwhiTH78LO2bd-fuvtSw7b6rMVba1cepe93PVlxff6n4VnwTgrLcpK1JRY1wWJX_Ahb3USx0_4SGPea-eMV43LXjEpLzHRrGTpjFLgoSmPXFjeH607XbNwYdrKi_3Mupxla7YCjt2ULL3WGUHe4F1HP5iA71Q45Zt2mqVPD-wWKUoBAM27IBq4XVC7Nsag5ujCDiP47Z78cDNeZCbu1BIRZHpB2772e1ZjfxejICHAzOmISrpX0DWLNNsCSnbXlS16y86aRaA1SGKt5nqhfL88ANdxvCJVG5PINtAm0Ja7IsBrHXVBmecNQVc1quN29PR2ubaXTy_v8TYvT6ztQXRv6Y0qDoPU3V2UXX2Um0r9U73AvwTHgS9dlPetQypGxi1h6WqEVRrxvZJ84IauOgy6j0F4I48v3cbyb9U-9ynYYlv8qwhX6eAugF9IYLuGkO9O93PwXu4Qm_PTVXgq8Imrfp9a29ufHzbRgOHg-nKBogb8oClIhyysXHaNULnR55e9YU8TOww8pgdsWHebBxoGU3cP_rNrbJdrsiHOA2Em9ofdLujJyorCr09sJUFgOBVCYb6YKepE3P-QZnzg5WEnKfeh26WUsyqNoGasFVZcUJWUJUh8f96ABuJLdYOpbq9hbavm3pDs6rJ9ScaDNDRGXmhgTN91HDpjPzrl1NKwG9qaq7m7EpVaESH-egAJNC4ewdEXxz_fYZ__g6XFIM1)
