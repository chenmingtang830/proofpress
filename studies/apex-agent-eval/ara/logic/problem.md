[//]: # (ob:daadea32)
# Problem Specification

[//]: # (ob:367ebadf)
## Observations

[//]: # (ob:37a848c8)
### O1: Majority quality did not decline in the observed normal cells

[//]: # (ob:89bc4c4b)
- **Statement**: Across six model-task cells, treatment majority rubric score tied baseline in five cells and improved in one.
- **Evidence**: Tables 1 and 2.
- **Implication**: A bounded working set did not create an obvious majority-score regression in this pilot.

[//]: # (ob:d7e540ed)
### O2: Mean grader outcomes expose task-specific weakness

[//]: # (ob:4392a1c8)
- **Statement**: Mean score improved for every Task 1 treatment artifact and declined for every Task 2 treatment artifact.
- **Evidence**: Tables 1 and 2.
- **Implication**: A majority-only headline hides meaningful rubric-level instability and claim-coverage sensitivity.

[//]: # (ob:a58ff02c)
### O3: Executor efficiency is heterogeneous

[//]: # (ob:ebfa361b)
- **Statement**: Muse used fewer executor tokens and less executor time on both tasks; Sol did so on neither; Luna did so only on Task 2.
- **Evidence**: Table 3.
- **Implication**: Context governance is not a model-independent efficiency optimization.

[//]: # (ob:b1cca5d1)
### O4: Tested corrupted states failed closed

[//]: # (ob:1300d4f3)
- **Statement**: Both Proofpress stress treatment cells returned a blocking decision and produced no DOCX.
- **Evidence**: `evidence/results/task1_results.md`, `evidence/results/task2_results.md`.
- **Implication**: The gate provided a safety behavior that artifact-quality scoring alone does not measure.

[//]: # (ob:880693c4)
### O5: Preparation cost is material and incompletely observed

[//]: # (ob:6086ed3b)
- **Statement**: The recorded Task 1 decomposition, proposal, and critic loop consumed 316,456 tokens over approximately 440 seconds; complete Task 2 upstream telemetry is absent.
- **Evidence**: `evidence/results/upfront_and_reuse.md`.
- **Implication**: Executor-only savings cannot determine total system cost.

[//]: # (ob:eb4ac89d)
### O6: The comparison study used a different causal design

[//]: # (ob:7ec0e728)
- **Statement**: PR35 RelayBench reports 10,654/11,928 ordinary criteria and 11,141/11,928 Proofpress criteria across 126 valid paired runs, with byte-identical substantive handoff content and a ledger-status treatment.
- **Evidence**: Figure 1 and PR35 `PUBLIC_RESULTS.md` / `CLAIM_BOUNDARIES.md`.
- **Implication**: Its clearer aggregate lift cannot be transferred directly to a working-set treatment that changes information volume and task-stage placement.

[//]: # (ob:e2763084)
## Gaps

[//]: # (ob:ef488147)
### G1: No executor-run replication

[//]: # (ob:94572f6a)
- **Statement**: Each normal cell contains one generated artifact.
- **Caused by**: O1, O2.
- **Existing attempts**: Three grader calls per artifact.
- **Why they fail**: Re-grading measures evaluator variation, not executor outcome variance or Pass@1.

[//]: # (ob:b02a44f2)
### G2: No complete end-to-end accounting

[//]: # (ob:c2d27c4a)
- **Statement**: The study lacks complete upstream tokens, time, and dollar cost for both tasks.
- **Caused by**: O5.
- **Existing attempts**: Task 1 records a partial upstream loop; Task 2 records reuse counts.
- **Why they fail**: Partial telemetry cannot identify an amortization break-even point.

[//]: # (ob:5e1f9206)
### G3: Composite treatment obscures the active mechanism

[//]: # (ob:f2a13c9d)
- **Statement**: Retrieval, proposal, verification, staging, graph selection, and executor prompting change together.
- **Caused by**: O2, O3, O6.
- **Existing attempts**: Cross-model and cross-task comparisons.
- **Why they fail**: Heterogeneity is observable but cannot be attributed to one component without ablations.

[//]: # (ob:42b77ef1)
### G4: Safety breadth is unknown

[//]: # (ob:44d703d1)
- **Statement**: Successful blocking on the tested conflicts does not estimate false negatives or false positives over a corruption distribution.
- **Caused by**: O4.
- **Existing attempts**: One stress condition per task and a separate deterministic mechanism suite.
- **Why they fail**: The sampled conditions are too narrow for robustness claims.

[//]: # (ob:2bf18a16)
## Key Insight

[//]: # (ob:8de3a2fa)
- **Insight**: A governed working set should be evaluated as a cost-shifting and authority-control mechanism whose value depends jointly on claim coverage, executor search behavior, reuse horizon, and fail-closed policy—not as a universal quality enhancer.
- **Derived from**: O1–O6.
- **Enables**: Separate claims for majority quality, mean instability, conditional efficiency, safety gating, and amortization rather than one aggregate “better” claim.

[//]: # (ob:5e4e0803)
## Assumptions

[//]: # (ob:7e219520)
- A1: The frozen manifests faithfully report artifact hashes, grader replicates, tokens, latency, and stress decisions.
- A2: Majority rubric cells are the primary descriptive quality summary; mean grader score remains a required secondary statistic.
- A3: Local executor generation and native output grading are meaningfully comparable for a pilot but not interchangeable with official APEX execution.
- A4: Staged candidates are evaluation inputs only and carry no lawyer-admission authority.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzJlNGI2OTZiMmM0ZjRiNDBmZGQwZDg4OSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijk3NmE0OGE2IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iNjkwOGUwMTRjNzZkODE2ZDc3NTMwZjgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzU2YTY1YjQ3MDQyZDVlYWIyYmNiMjM4OCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXNtyG0eS_ZUKzJsXEPtSfaNflqY1HsVoRgpJ3p2IsQKuWxNtNbrhvpCCGYrwP-w-zvycv2Qzq28FkWgCaMo7McEIKUiiu6uyMrNOnjwo4HbGiiqJmaiWiZydzzabpaMo9yOfO4LGlFMrltKSYRjN5jOey-1SJleqrODecsUczz9nzFeWjIQXcxFxm0kurMhmvgyY5_hx6ESBcK2Yho4lJXXt0KUxi8OA2zF3Pd-FcWVSivxaFdvZ-S3-US0rdgUzpKzCqebwC1cpvPBfqkjihPFUkUJdJ2WSZ2QF9-fFlvAteV3kebwpVFnCMxsmPrArhYvaebnIf1Kw3LrAAVdVtSnPz86ukmpV82ciX5-JlcrWSXZVsewqdK2znacL9XOdwO_LulTFUuRZqTLwRVXU6tN8tlIMnRgFPqMh82fNK0t1rW8C56oluNYKlWVTEfgytMFLgQfeCdGyvKhwacs0yRRY3kUkXXo-8z1OA4s60lOMO1xwxw3DZjmtdUvBNmWdwoIdtFPkhSxn53-_nbXT384gynlR4m_NZSWXHFz-99llu2TyDtY8ew8r6bICw1zVMlHlGduojwswK6sW6pqlZ8-GqRe8TlJ5xgq2WKT5VSIWC7gIS1k_W8vZ_KgcY1VVJLyuILRLzsqkRBNUGi9ZCS6vlB6vrlZ5gQv5kGQ4ZLktK7WGKxlbY8R3FzSHAUrMldl5VqcpLE-s4HWF7nk_7_wzgwTEm5aiUKyZR1_pjFbLILYsGoceC7mSAQ84iyLu2BznzSudaW0ISRtCAskkPmzyJKt0RhZ6JjSi-6u1YZOnidgaI5j5YAyiM-3EVCnzuFrG4BVVbIqkzciS2-fK5Zag1InCWNjCphGLeUxFGEV-zCOHOgFT1FbUpxGPXCoYjbwosnkQeg4PPQ_Hrhgu5RZ8iz9njuX4CytcOP472z136Llr_YdlnVsW3Nv6Ge6KRRg4InRmn4xXb_8fk4-nufigQ_Lp0_zenaNkUvX75tVGZRcvyGUu1cfZe70ZZS32Xv5s1929_HMNcPfvsyu1WadsytsmEPCMZEwq5jpwO4BtpT7i2l83qyBvN0pAORAMzYI7umml1PZssESoG3jlD2TfI9V2g6YhTINlMwx6N7XrB4ozGe9M_YrDcq_10-XojH8gn906NlPAQhqKcHcm-5z8hf2UF0m1JT_XLMWfMpEEoIZIJXDnkyQj41aAGQeOU60UybXJCq8V4yaHERdUUP7oJi_IV1-9BTBRa8idr746JxeiyMuSlMlHsoadki4qVn4gQqVpOScVQjXeSdYw72ByCpxgx14ZKI9aei7DXgfsVSwjVwVkWUHyugICoEqiPm7yUhGcaVFu1IMuPnAcnXnkRrEPWcMmRhxM3chh9uc58QgG33GwHhD4VwGxWQNAYPzjvCAKCRnsVfC23Tp6xMHMC-PYcsSuve45ef5RibrC8WJYfaIysSVJSVaqUkUOAKHyunzQwYePM-JSxWPm-jZ_dBPvuhTYIYH_4Eh1A3FS3QRV_kFlJWGZJCmkAFwYcSm3hWCetHftpefkna4SBEJW1Bv8DasvZEHMkhRfTyEXHnTpgePIcZ_armVJGruPbuMdn36TVyuD4MN4-seAABoSoC2o6hGfhqHlR66gu_Z65zCyAkKm0RqMLitMgDVMXyQs1fFKMvGgTw8cJ19vUsitdNsC7riLfSv0lXT5o5t8x8XvVthWNRyl2_gA22BuXiY4zZwAPsAfLB1xseKUAXf8DGr9ZngcjBVJCSYjg9k2u4RBlYhjBXz4QRcfOA6kA6vBTrC_TK4eqPSBEpYKnPDRLb7j4ddvXI-8USnbfgMoswJvI5MviW3NfY-e2fY8ckICAUiyMQ87ge9a4W4Sfwfd3wOMpL1lDCKhTQ9tGuyODGX9r3kPYouiztDw9BDihbM--PiIQRH1Aif22WMZdCcizxmEAejOGnIFEYTgNCwBkM6BrCD4F9gMEiDLY1BtOYzSeJemfudoM7vtTlQmF1W-gB-ECZHXWZVoHjzuvQMHGfGhcKQTCMoe17h70aPZISmDJmoYut4gVrN1W_2AtY140lN2HDmWv2ssFOnLFoaUAfkAn6KGMqDJK_ZFDznzwHGSa0XWCvuRpFyPOzcGluaKz9DuMey94983Clow7PEGFJ6Tay2INXk_xxp7BQbOR_xLHR4EKt4lFd9BwX7LYgV0nYOxEiot1JI6-5DlNw_v7wceHiO5VAaWKx_JmDsee1sLARwhrlOiZ8TeM286naqjJ1kMsFGVIx5zeGyHzN7NyD-rLXmRQWlZPZB0ZPfOsZZKKpc5MTtlHlx6e5vumcgVyqkZrPAmL_S6S1WRcpXXqSQcdjukUd3gWjm6GamyQmuX3V2UZb3eHNIB7945WoAdO_Ic65R5FuTCbsAnLvJfVAYUKEtiCK_mmtUKog9Eqym0pJM8yIqVK3Vn6e9h_pQl670axGdWtKrfBf6p00o_Ag6GXZih13-4X6v4YQZYqB8owdgq-QUev3j9_G9EKyZddJDXXby5eLZPlTjeGFOSmGLDoFecYMOJekRXoKcYbqgWxxt-qiqhF1rUvIDev2mzqwQm4axU3VpjLDj48IS1GQrHCUE5ScGYYK0hb0yMxBHyBRrVIwA2SG263XnAIdWEtRlSyAmROFCPmGCfoYNM9f3hOkd3IVkrrMEcu3nMqvJr8jZPNQCUOV7JVDJhbYZmcoLvD9VEJhhoCCYTnX-EIKKZABtIEOR9894pBqh70wJAlnz76nIKvA7iygnOP1E8mRQNQ1uZGI0jtJO5XoqAugBYmub5BmkocB140LX9OfX8bv_k15O2ea_DnBCN03SWCeYaIszEUBwhsjBAfAwEZpiOCly0qd3dY-wuUUwJxSDYHL82VG2mzD1IOifMPa60TDDLEHYmhvsIBUdX_mdTysug85zgzEMklwnGGTrPI4DZgVIO1PMGz2SepqxoYBvp1FDhpzjckINOcPgpcs8EYw0taGIAjtB6kLJvVtDfp0o0VzAaPeGCx7GJhilgfVMI-6AbnRCIMUlnilGDfjTR4UdIRZDpkDrYrcKFBOkJkMMUiHCmrhjmEgBP0b40YW2G7HT82gzZaAqfGxSp4004VY4CcoEYsihXSazzFtO5OVoCjfQCwb2AhkHv10nA0ktbx6_NkKYmMZ5e9TrBhJNFr3nX5HeFHF_q8BxPXEK72YDIsWt7b8h3t7Ob1XZnDf0Yc3gykTCNWnCoenJs1M4A4HR-W5IAxxU68vBzeyNnLhtPmwfyzGNp5iG926fzSU_nk57OJz2dT3o6n_R0PunpfNLT-aSn80lP55Oezic9nU96Op_0dD7p6XzS0_mk3-d80uEfSew-ktfadO4En-7_7N1DHz98lM8YxkHMKbc85XqODXTGtf3IUSKIbBaE3PfjkFHlK0YZU8rlKrCZ8iJpuwG3Ip9Z-xZ036cNo3OH3vNpw_5juf9ynza8nWG8kd_40vZ95loRxaTWYxgSU5t5R8lF7cjUgf7Xtmxo2e1uZENB6kY-RBZqR3Q8HrsRVQFjvB9xUIr6EU-XePojX6N2hJ7v24GnlGSys8OQf1o7pug2x5zgaprnXqiAS8DTnv2Q4fzPW9lTsxHcWkCs9e1Oe8OLdU8SG5js9FETJTvHNXInPA8-u07yuuxtXTRGFuqqaD5i2TgXqtQmSfPq2T2I2vrSszzOhRtFjif6_BukKTOmj6gptZPbNoVNz4DeO30gDZlpXyC_0AGwOw-cHMQ-LHkGSI8L11mzgnEgZmA9-AE5QJNhixTsSCFiAHc80VtFHxfBc6kL_S0J-LnyEogqtLzXcHkknDxknmCWZ4W6bGuPGkKYGc5JClaHMZELGzEMIiem3XSGqLU3gF_mFBmgSfE1eVlnbHgdJY2sDfG-eBL3_kBeNpW_pS4MHkHv4E5kLYIABVAb6FD02xiDD3MgCevkFz3QSLAc6rrUU5LaVp_-hsRmBmuaNtbhpm37UoShsmS_1w25bF-0vtCxs7_dE44fu_eJzmCKOq3KM4y1vWz_goL743zPTY550_3xREp2hQiKmJFIbWrZ8nq1YgCpkGgrNgDAoitdCDb6nckUe_D-7WDYyiV0T2Pw6sXcjVjEPb93uaH4mSE--TTcaMxdV8nIBfpGWdwZYOh3-2L-hQ63wV5nG3jwo34XHdZAqQXIBg9I2NB9f94i8tCmK6A-0GxqdGIcv4HloOSpN8DAgTyDgZAdADj7c6ODwgayS0iG7KokgmUNY4EYrBHCq7yCUDRfPqJDNBL7KJDcsewgcFU4gGMvRZqxf0wNsZ3dChn3eOhJ6vaBN2TFfYH_QkfpursaCmY7PgGWDRi9YUkBSyxqVGFuAMEJ31ZqgXGEdEJX1xxwLtMCyAomyeNYC2K6TqM0BIVCQu-xQDSsDVS6J0H-mFzBbm2Lt17oj6-__-bli8vlm-dvv3_57i2mBzkjP16-vHjxl-U3r77_67cXb148f7s_bV6Aa0SqWIGZfQXsS-NLmsRVlzsc5RaWlRBAXKmE9YoKUqzKwfaW5S2Q5Q14qjGofe8ZtnyMvFhjwnWewr7S5jdsq0JmsEmZ0PEbyUWpgsiKPRaJuC81hmg7NAP7FdkO0dzQjuI4tGNrKPmDSGtk9Ukyaz-LCHzqUCsUPW4ayuu-7D3-ZKAO6iXTG41vcYxX9hy4bpc-H8GRGvkrmGVTlQ04Fkp1NBiSFIrfBuO_O-h_r7bY32x1gW7ksgU-g6O1haPsZA8oPNew8VvRTJ806phPS7Ob60hB4LXXrCz_0x4JdyBtG1pv6I_CngYairAZpNPV3HYu5kDrEFKLO07fZxoC71iFecwTh_cE0hsNYlPU2q_Ngr24wfhB3vTzYy37uqtF3X26jBDtmHJfoF-3Iw1lq8WCBtZi5PeErQFXW46oZcUPC1R6iP7Wp5HQisDzgxD4g3T8zt2GRG2G9vG05Xbu2PEd5oecuTLq5jbk5n2h_kJnGwEeIUeuFNL-e-PvwEZ24b8_lgeXWJEWms63RAb_bqSBvhzvDfWf-lYJaSKwk4aU6a6C12YR6L5PCc9G5RqONJvKMCJY-GCfA7VJGxlmJP6KWTwOYzf2B_w1JHQz_sfL4F21iFRElecJaffcwVDG98X5Cx2pbCinfkkTyK4Fwo2DXx3YfU3VvTlAx2L_KlNdN4MUVBNbDeU6_A29KBtKrnoSiOOIYcMAQ4HttS8_NMoxRDY5TAFog4pSnhPgUEV-o7GsyHldVpm2RX8idSQHKDQQIfUdwFini4_xpsBQzR-U-rvO0GdOCKzMtmiP4Yb6bwT89zjkqd16s0JRCUdA12OTXZKfEBubjl77iHTqyHyAiBLIGJCArqGbt4iN8_zS4QlGZ9E0zKQRwn_79X91X4921lmCYjEAeNf-qWyFpbdDmW8BurTmBGjUMIbffv2fAWUyrRHpDdHlThNRHef1Z7LoXAtCpvozHzIFbBhkhXnXrOIOQazULjTLCMy1UrqH1SKkwUh_-_UfXEHmF7_9-s_GmpH0Yh4NmZBxRKkYSkz_xsuQXg--ndJhlhMr7gfSswNv6EX6d1j69Po9jri2-71TJhpkv3AMvbrVfVttF3fqCiUDQCmo5NB5QTez0UWzVwfqNV77uolka0inyK41_WSk_R5R2ba7OBa2LBpNGhugXL_Msefpc7klrJ2AkmlkREa4gWLRcUm0cNAUwUNN2dIlCBOONRqwLkeahEDzVDTlU9-ju65cZxnMrc_lNgZ0kHqBdQQ7DYnlTCZSy044rXFyN8nAprIR3HQZBWTbotKTspsttGdMrpNGme43_Z0MfP8J_v0fYW7TeQ)
