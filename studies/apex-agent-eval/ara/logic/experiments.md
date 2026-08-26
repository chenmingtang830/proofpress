[//]: # (ob:1fd447c4)
# Experiments and analyses

[//]: # (ob:5cdd44a8)
## E01: Task 1 paired three-executor comparison

[//]: # (ob:b6dd7a0d)
- **Verifies**: C01, C02
- **Evidence**: `evidence/tables/table1_task1_three_model.md`, `evidence/results/task1_results.md`
- **Run**: `src/artifacts.md#task-1-execution-and-grading`
- **Setup**:
  - Models: GPT-5.6 Sol, GPT-5.6 Luna, Muse Spark 1.1
  - Dataset: World425 APEX data room
  - System: full-data-room baseline versus Proofpress governed working set
- **Procedure**:
  1. Freeze prompts, working-set receipt, and task metadata.
  2. Generate one normal artifact per executor-condition cell.
  3. Apply repeated native Output LLM verifier judgments to each artifact.
  4. Record majority, mean, executor tokens, latency, and artifact digest.
- **Metrics**: passed rubric cells, majority and mean verifier result, executor tokens, executor seconds
- **Expected outcome**: Treatment preserves task quality; efficiency direction may vary by executor.
- **Baselines**: Ordinary full-data-room execution.
- **Dependencies**: none

[//]: # (ob:f97f44e5)
## E02: Task 2 paired three-executor comparison

[//]: # (ob:39982a57)
- **Verifies**: C01, C02
- **Evidence**: `evidence/tables/table2_task2_three_model.md`, `evidence/results/task2_results.md`
- **Run**: `src/artifacts.md#task-2-execution-and-grading`
- **Setup**:
  - Models: GPT-5.6 Sol, GPT-5.6 Luna, Muse Spark 1.1
  - Dataset: The same World425 APEX data room with a different legal deliverable
  - System: full-data-room baseline versus task-isolated Proofpress governed working set
- **Procedure**:
  1. Reuse eligible prior claims and add task-specific claims.
  2. Freeze task scope, prompts, and working-set digest.
  3. Generate one normal artifact per executor-condition cell.
  4. Apply repeated native Output LLM verifier judgments and record executor telemetry.
- **Metrics**: passed rubric cells, majority and mean verifier result, executor tokens, executor seconds
- **Expected outcome**: Treatment preserves majority quality and tests whether prior claim reuse reduces execution work.
- **Baselines**: Ordinary full-data-room execution.
- **Dependencies**: E01

[//]: # (ob:c45f558a)
## E03: Material-conflict stress gates

[//]: # (ob:e3606694)
- **Verifies**: C03
- **Evidence**: `evidence/results/task1_results.md`, `evidence/results/task2_results.md`
- **Run**: `src/artifacts.md#stress-gating`
- **Setup**:
  - Models: Executor is not invoked when the gate blocks
  - Dataset: Frozen task state plus an unverified material conflict
  - System: Proofpress pre-execution decision gate
- **Procedure**:
  1. Introduce the frozen conflict input.
  2. Evaluate integrity, claim state, and task impact under policy.
  3. Record allow or block and whether an artifact exists.
- **Metrics**: gate decision, executor invocation, artifact production
- **Expected outcome**: Material unresolved conflicts block before client-artifact generation.
- **Baselines**: Ordinary workflow behavior where available; no matched score is assigned to a blocked cell.
- **Dependencies**: none

[//]: # (ob:a42239fb)
## E04: Upfront-cost and reuse audit

[//]: # (ob:a3003e68)
- **Verifies**: C04, C05
- **Evidence**: `evidence/results/upfront_and_reuse.md`
- **Run**: `src/artifacts.md#corpus-to-proposal-and-working-set-construction`
- **Setup**:
  - Models: Task decomposition, claim proposal, critic, and policy roles
  - Dataset: Shared World425 corpus
  - System: cold construction followed by later-task reuse
- **Procedure**:
  1. Inventory recorded upstream model and wall-clock telemetry.
  2. Separate executor measurements from preparation.
  3. Identify reused and task-specific claims in the later working set.
  4. Mark missing telemetry rather than imputing it.
- **Metrics**: upstream tokens, upstream seconds, dollar fields where recorded, reused-claim count, new-claim count
- **Expected outcome**: Reuse is observable, but end-to-end savings remain unresolved until upstream telemetry is complete.
- **Baselines**: No-reuse reconstruction is pending.
- **Dependencies**: E01, E02

[//]: # (ob:8215fdc1)
## E05: Cross-study causal-design comparison

[//]: # (ob:a6927b15)
- **Verifies**: C06
- **Evidence**: `evidence/figures/figure1_pr35_results_poster.md`, `evidence/results/pr35_comparison.md`
- **Run**: `src/artifacts.md#pr35-relaybench-source-study`
- **Setup**:
  - Studies: PR35 parity-controlled handoff study and this APEX working-set pilot
  - System: design-attribute comparison, not pooled outcome analysis
- **Procedure**:
  1. Extract each study's treatment difference, denominator, task stage, and authority boundary.
  2. Separate observed results from inferred explanations.
  3. Identify testable ablations that could distinguish information parity from information starvation.
- **Metrics**: treatment parity, execution replication, task count, quality aggregation, safety design, cost scope
- **Expected outcome**: Design differences yield bounded hypotheses rather than direct causal transfer.
- **Baselines**: The two studies serve as design contrasts, not exchangeable samples.
- **Dependencies**: E01, E02, E03, E04

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2Y0ZDgwYzY1NmVjMGZiZWMyNGNjMmJmNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjA4YWNiZDFhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84OTBkOTVkZTA0YThkZTE4N2RkMmYyNWIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzY1OWE2NDQ2NmYwZDMzZDljYjUzN2Y1YyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW22P2zYS_iuE--GAnLWrd0vup1ybFgWaa5DkXoAmcCmKstWVJVWUdtdd5L_fM6Qka1-873ctDgs09poiOTMPZ54ZkurFjDdtnnHRrvJ0tpzV9Srz08gWYRBKYWeJFK4vhJtk4Ww-S6p0t0rztVQt-qoNd4NwyW0RpCLiUSijIF4EURK5YeaEtpNiBjdxeZA5dhKEkfA9OwiFJ4LIzkQm7dTLUol501yJ6lQ2u9nygn60q5avIaHgLYma449EFmj4p2zyLOdJIVkjT3OVVyXboH_V7FiyY--aqsrqRiqFMTUXJ3wtyahLzU31q4S5XUMTbtq2Vsvj43XebrrkSFTbY7GR5TYv1y0v15FnH18a3cjfuhx_rzolm5WoSiVLYNE2nfwyn20kJxDtiIskdfjMtKzkqe4EcOUqiu00DlJp-zxKpRMt0tTN3CAhzaqmJdNWRV5KaD6sSLEKg5iHvh-GGSDz0lgkgbfIAmHM6bVbCV6rroDBLukpqiZVs-XPF7Ne_MUMq1w1iv4yj2W6SgD5z7NvepPZR9g8-wxLBq-gZW67NJfqmNfy3IJaZWvJU14cH-1FW0mXF-kxb7hlFdU6F5Ylz2us1Ra91dE2nc0f5Ge8bZs86Vos7yrhKlekhiyyFVeAvZV6vq7dVA0Zc5KXNKXaqVZu8aTkW1r1y0bNMYEif5kty64oYKLYoF0SRJ_nA0YzOCF1WolGciNHPxmUlisusGx-5MkgirjjuU4qHBGHEcmtWu1t_TKyfhkZHEqc1FVettorGy2JlBh-9TrUVZGL3WSGqU9MJtHe9kh3UVXWrjKgIpu6yXuvVImzlF5iC9934yiDQY4f8yzJfBHFcZglseu7Cy59R_qhHyex5wvux0EcO8kiCtwkCgKau-VkygWwpe-Za7uhZUeWG350vKXrL93or7a9tG307XFGL-5GTmIn7uzLpPXiD3bApKjEiV6WL1_mN0aQTPN2jJ-falm-_oF9U6XyfPZZB2XaiYOPr0Tf9ce_daC9_6_o1Ko9JjgvzGJgjJOlvr8QPrqDeFt5Tva_2VvCeJniHy92mA2dBslpqlWqKWPIM7R8xW4Z1e5qUpCIG_rNaPkHBQKRQgMeXVbAdpawQp0wh9UcuSFl7aaREhhL0cFdGJIK4vxWhaDRPafJFVC6VcskTNMFt9Nn19Jir16ZBCzVq1dL9o3tzPHhfirpyZvTPJWlkPTkF9n_ONYMpfC117lAvr6kcBYvMt-XwRWF3V5h92mw3m-au2H14jhCKbN4di3_W7AKP8iCIOJXFPaW7C1SW5PzwkJ7hpzTMtUSUbA11Vt3InqfGW4BUnqhHYax_5x6XcfQuw0-TNoVLeGnTpzVLRhy33W9OEuu6Oov2T_qrEELVFWtppBGoiRkHGzc3ong3eNvwY97tu3JMHo-na6j55MHBveBsLsFvch1ggz10RVNA0hoKuQlyl07JninsOapVPm63IfjnSDeb5o7opqHsbtInODZVbyOaXgbnFm-7gBp_30VUxQFouD59mA-vKJGX4m-pp8gJMn0EJbIdV6WlHU_Hcybn2asrfQYxcu8zX_HDK_fvfk30wmcUW3RcUr97PX710eH0uMj9HlA_nuCjpPk-HAdb2Tpx-syyXuPwev-ie0JOk6y3h-O1yShPQavOxPME1Sb5LSnwuQ9QY1JunoMQnekkKcots9ZT8WnT02P12WSlR4D0j3TzlPA2uekp4IVPlSNz5M8eDE72-wuiRvnmLMhc1lJ1ZXpbbMOCrx774XMgIagk2Tz_Y9dbjk2M6BMz1OmpwrTM5aLl23ly7byZVv5sq182Va-bCtftpVfPj_kdmM43e-VWjrOl5uP8e-6yXiW64owjfwUORNjPL7IFpnneFkQesJJF470MikjO3Pt0Jd8kXoL6TpuKBJbxk4SeYHNDxl008VFvHT8Gy4uxlu-P-XFxcVsw9UG_ReuWERJFPo8Iav1HJOSp_fNh9Yu_eRByv3I9d1k4Yth8kk5M0z-HHVIL9EXob9wsixNg9GcSWnSS3xS8sOXszIcrnVcbatUFliLX-YHyb7_RZ2MjPddqadXjTgeFpAef0X9Lae3Gz5jAWxr3WhD-7EfZNvVGP2pZMxib0m6WrLv3320gqOQfaiK-fjjx67kc_aW-PgD4AO8R44Z9i2HJNku2b-qpkh9NzAVeopmBvfbml4f9KXpkmUony16ZtEzlmAoxSkjx-7U5GKdremivsT6nVXNCe05IMSojU5CpuCZXnXniH0H-H6XDP6-rVs1H8ZYGIMsImRet3PtbYQK28qWkw5HNNo9Yt_LUjbI0ayCJmXVbHnBBiwZvJUNzkOZHcmINhxCFoUe7x2x12CXHeTUelPBSmxJTiX7qWvrrmU__viWrCMXadivXbo2ro_NiuRiM8rRc_lH7L2-s2Nb_mvV5O1uDmV5OR81wLgTWcJCemWhFDtj1aiseWfiyOD0VrZNLrRf1nRlhoTaJWjRumOKQYaegsTs9TRudoPYsUFJwkL1jo6YFmR61bWIL-3wH2mLRbYyWk_ZnEpl0P-t4wWkfs1kluUiJyugN1ZJ47rlO3bKzWsWg7Denr_1zqIt-qmBI1O_Kx41-ns_6FusSkmR1EdoiTW-Ief3Ue9wlyNB8MwUeDrqJ_X9lGeeWpj3EkXk2GIh4kBmziBxUqs_E8-4mmfc-_KM-1Cecf-HPPNRHxBs5SHCYWd5i7iCT2WZpC05K-QaEQ2pCMuG4HgQJ2kDsY6FDu7HMtR7Xcti4nVO72ygyiAf0YftJoRTQ06WQihhnUX_cOConuF0BClR1XK-ZzsaP2W8kQU0Oz2J3fzHsZup3jWT7SlEFhLM2-z-tPQ0SuwpymQMQKnY2Ua2G0ierFu_PUHodwKDxwDQS_GclIWa5jBjyUUaoypxklCMdcpk6zxlrEdufHtBkXB8202DgAfhIGiyFz5IVA_YyU5I5zmYyZhmwbS7qOjN4Da5QoS0LC9P4VAprXqpzxQJHnMIqq6w0XdN9Tt10nHZUre66CgAWFf2_krZ3MDOBtgvE9CEU_C5p1JQljDvHpL8g9TyQ9ma94C0qplRaFzgvEScDizyxpyYSrS2cm0KDOPMWvdJjZQje2E0nbnC6_U-ayCUvkThRVGdMYBmDoc1CfVRAutHhpHn8Fh1PeY1pIOBk8gl7IU-1J1PaEobSI2HI3rwbegMKKviFI8HFNR4gp1VjYTJOW2SxunXhiL3IXhz3FJgZ2R0Ijf8lIgABmM6fsrzgvLK1_AeWmyxgWywNJ7Bo0Bu2HdThVAhLWlFSDVDsQ-vUQLfCWKxcF0vG_dCk4OeacQ_6qBmKIWCdOHFjsMTJxvF7M9uDsb7A85ejGoraLXSWt0jpoFp3SmrrSy4RF3RsQbVG5PsR9SGyDfecmvU6_INHogsWqnceJwJhmFu_EaM5MLEhYkC1Bgoq66wwIcNpxJwrEiMmpejXFSFdshROZZVFEIYh1qXqovG0qGnsbgl2ukohV5EHl7vY11NVMe3TBd2JhIRnZbQPj_Nu5oEPkhUVhR9Y8whuyoIMbkbi0IImE4mJHTY_4DVw0rsjH7pSBVXKxZEsCYibdG0NhoKirdU121zRAXaR-0YpBF3tBuwB9inI9Zm-Q2bmdHcIeuPDX3Wn7MUyPKGwSuLVPVROsA17w2wzFqLqitRSpTybNpwmGZMIYewrhIqGyjs5yxBKYQQJr_EF8rTUyivIGjL83JKSJg6LyYWjNZjQnLEQrbyJg76e2UN5cYlF8Iw4g5IO1w8zGm3cphPYh473iKMecLlEOiTo88pnzzpzLIXxzPhyyRNE8cd64jJMeZBXnnA-aOzqhsvGCqFFUIZnnioqtBd97rfg4NoBFaj4LsEM20sVXWNkAaTGwnngzmfW9LVZMBIULsjmkLaLgo4BTw-rbKsv7TUcbXBwuptzbSur_OiulI6GOyt4VVZOVmFuS5l6qoq9g7cn7bl6iC9vDlvG5226XBCK_QXRfeofbE8bKoEnB44VltkRjDIfCyA1n0RYV7MpSJaX9zyG-jHBBDV_WYpDPPkJQQQmcrzuuClpiB1jYOoKtcvv-PDdCHiaCl4wbL0v3YAtC5XG5qP9jw6Wgz0o5yxHXMhkif5f8I2e9vN6Pmk0gdJIiX0xYpGoGeTcQOxXjdy3XdQPJNoM0uG1EIZWW_lDpPNtya09qgrtiNOY8Nt-GZXV6BNhQdT_jTnKX2AwgReKkxwE7HQbro9q1h_hsz0kqBkYWNUw025om0muZM8N1fbGnvswkFY6g7moQ-PPvxr9wJf8N9_ALAEYIo)
