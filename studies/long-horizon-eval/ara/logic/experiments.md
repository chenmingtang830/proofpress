[//]: # (ob:8219c192)
# Experiments

[//]: # (ob:080c3518)
## E01: Phase Zero mechanics validation

[//]: # (ob:58f6e3f8)
- **Verifies**: C01.
- **Status**: completed; engineering evidence only.
- **Provenance**: ai-executed.
- **Setup**: Deterministic H4 test-double releases, declared cold boundary, C1 ordinary and C2 Proofpress condition manifests, file-level parity checks, state scoring, and TEST-ONLY exclusion markers.
- **Procedure**: Run fixture verification, parity, stage-controller, scoring, reporting, and readiness tests; verify that TEST-ONLY output cannot enter benchmark aggregation.
- **Metrics**: Boundary enforcement, parity result, deterministic state score, schema validity, and exclusion eligibility.
- **Expected outcome**: The harness enforces the declared boundary, verifies parity, produces deterministic records, and excludes TEST-ONLY data.
- **Baselines**: No-treatment deterministic condition and intentionally invalid fixture cases.
- **Result**: Mechanics readiness passed; this result does not measure language-model behavior.
- **Evidence**: [`../../relaybench/BENCHMARK_READINESS_REPORT.md`](../../relaybench/BENCHMARK_READINESS_REPORT.md) and the adjacent test suite.

[//]: # (ob:3607dd4f)
## E02: Frozen seven-model paired quality panel

[//]: # (ob:692ad304)
- **Verifies**: C02 and C04.
- **Status**: completed and frozen.
- **Provenance**: ai-executed.
- **Setup**: Credit, MSA, and License task families; seven complete model panels; clean/stress 2×2 cells; three receiver repeats per cell; one frozen S1-S3 sender state per model/task; identical worker caps and S4 rubrics between conditions.
- **Procedure**: Generate and freeze sender state, branch fresh S4 receivers into ordinary and Proofpress conditions, evaluate matched deliverables against the same task rubric, reject invalid pairs, and aggregate only content-addressed admitted panel files.
- **Metrics**: Passed rubric criteria and matched criterion denominator, reported by model, task, arm, and condition; tokens and latency where telemetry is complete.
- **Expected outcome**: Proofpress should preserve clean continuation within a practically acceptable bound; any descriptive improvement must remain scoped to the frozen panel.
- **Baselines**: Strong ordinary portable handoff using the same source state, task, model, tools, caps, and evaluator.
- **Result**: Ordinary 10,654/11,928 (89.3%); Proofpress 11,141/11,928 (93.4%); descriptive delta +4.1 percentage points across 126 admitted pairs.
- **Evidence**: [`../evidence/tables/final-panel.md`](../evidence/tables/final-panel.md), [`../evidence/FINAL_RESULTS_RECEIPTS.json`](../evidence/FINAL_RESULTS_RECEIPTS.json), and the seven panel receipts it names.

[//]: # (ob:35734341)
## E03: Controlled handoff trust-stress panel

[//]: # (ob:34fc74b2)
- **Verifies**: C03 and C04.
- **Status**: completed and frozen.
- **Provenance**: ai-executed.
- **Setup**: The same E02 tasks and paired receiver design, with preregistered stale-authority, unsupported-approval, or revoked-approval fixtures injected at the S3-to-S4 cold boundary. Artifact content is byte-matched; only Proofpress has external current-state metadata and deterministic blocking.
- **Procedure**: Apply each fixture to both conditions, run three S4 repeats, score the final deliverable with fixture-specific deterministic unsafe-propagation checks, and keep quality scoring separate.
- **Metrics**: Unsafe propagation events per admitted stress pair, plus matched work-product rubric quality.
- **Expected outcome**: Proofpress should block injected non-current or unsupported state without requiring a claim of substantive legal correctness.
- **Baselines**: Ordinary portable handoff with the identical perturbed artifact and no ledger current-state gate.
- **Result**: Across 63 admitted stress pairs, ordinary handoff propagated eight injected unsafe states and Proofpress propagated none.
- **Evidence**: [`../evidence/tables/final-panel.md`](../evidence/tables/final-panel.md), the final receipt manifest, and fixture files under [`../../relaybench/bench/experiments/stress-fixtures/`](../../relaybench/bench/experiments/stress-fixtures/).

[//]: # (ob:40941016)
## E04: DeepSeek fourteen-scenario breadth check

[//]: # (ob:ce6846cc)
- **Verifies**: C04 only; secondary sensitivity evidence.
- **Status**: completed and excluded from the seven-model aggregate.
- **Provenance**: ai-executed.
- **Setup**: Fourteen LAB-derived scenarios under the frozen DeepSeek route.
- **Procedure**: Apply the task-expansion protocol and retain task-level outcomes without pooling them into the primary cross-model estimate.
- **Metrics**: Task-level paired quality and floor/ceiling sensitivity.
- **Expected outcome**: Detect whether the three primary task families conceal scenario heterogeneity.
- **Baselines**: Matched ordinary handoff per scenario.
- **Result**: Retained as secondary breadth evidence; it does not support a seven-model breadth claim.
- **Evidence**: [`../../relaybench/results/deepseek-v9-14-task-expansion-2026-08-25.json`](../../relaybench/results/deepseek-v9-14-task-expansion-2026-08-25.json).

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2UwZjU2MTM0MzVkOGE2YzIxMjc4ZWVkMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImM2OTZiODNlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xYTYyYWIxZTc0MmYyOTNlZTk4M2JjYTMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzVlMTMzMDIxODRmNTY0NjQ5NWFjYmIxMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWmtv20YW_SsDLRZoUsniW5T8yUnTbbF5wXYX2O0G6nA4lBhTJEsOnahBfsf-oP1je-5wSNGy5di1u8AuUgSNzced-zj33DPDfBrxSqUJF2qZxqPFqCyX0kr8wHY9149DHgjHdmahlLEzGo-iIt4u43Qla4Vn6zV3_GBhzWzHTuwQL8z5XFhze2bF-C-Ucx67ydwVMzuIfFu6SeiLmRtGTuCHIvZ9zkXME9iN01oUl7Lajhaf6Be1VHyFFTKuaKkxfohkhgt_k1WapDzKJKvkZVqnRc7WeL6otizasrdVUSRlJesa75RcXPCVpKCuXK6K9xLhNhUZXCtV1ovpdJWqdRMdiWIzFWuZb9J8pXi-Cl1reuXtSv7apPh52dSyWooir2WOXKiqkZ_Ho7XklEQRzIModOWovbKUl_ohJFcubR44PLLlzHMSZ-5KOQ_dSHCXPCsqRaEtszSX8LyrSLb0pe26loMcozRe4M19LqLIdtpwjHdLwcu6yRCwQ36Koorr0eLnTyOz_KcRqlxUNf3U3pbxMkLKfx41-UVefMhH7xBDhwcqsGriVNbTrMhXk3VRpb8V-URe8mzKK46rq1RM5ccSNdlghfpoE4_G98ITV6pKo0ahjMuI12lNi8osWfIa6VVS22sUlianL9KcTNbbWskN7uR8Q9XtnB_j1ZoQMVrkTZYhFLFGCWWbhCgrxAWeDh17Luw5rY7qKfmRAn2xCwLXzTo8jrUDJSFNfsCVP7GrD6ptSQ5QjYGX0ed34y7XI4CZXFmKSvI2Dn2nS4pc-rbt-zPPduPZPIo8KQJXJiLxKK5CadQaODADBwZgiouySHOl0V3plSjU7jeK9B3hKEvFdmBhiK2BEY3a3wm7ukjUMkHUsiqr1KC7juyF7nVHeI6c-87Mt1zpBvMklly6vs2FI2yRzGSQ4PfE86zEm0vbC13Orbn0Qz8i24orjdK2AgsbpaQLI8dygokVTpzg3HYW_mzhzr61rIVl4SWTcKqwsGPbm81HnwdXP_1Xca3B1uJuzes1nvfBetwWiNmmcmgbAygaHH4RYJ8_j2_sZxmnqu9m1DBXC1HE8uPonWaIuBGH7u4xwbW7vzZg4P72utnwfFGl6KwqJoL836AM7fbvZQwrtASwG15lDMtesLcormT_kFXBNpJeTUXNEGsac_LvVipBqe9mYh8D451nfpgENFUf1bMJe_q0HbOyfvp0wZ5b9tE_c7p6hr5s9DWMyTKTSPYxk_kKtIHn8xWTlzt_M0zlK866gTWLYy_Zc9ZZsO-r4jeZs5pwPdkAehkrOYZszH5t4LLasvKLqbybGZ5DRdya0mDuQLRY3qN7eT2tDuN5jL-9w-nVTyRVcVta_Rn6xLP3HHaxAn6tiiyDGQAgLpKEgfBrNakVyQXKxhfTejczX0qq6yVi5kXOo_t4PanuoyTVs-aebdnBnsPegn0nZXkm5QVLigZsAyjUQua8SgsWYdTHas2-mNS7mdGD-va8ChmEXiDEo7t5Pa8eK_Jsewz4Y6WYQ25D-NapSi8J-XgvlrmQOun7ecUYERlPNwdZdc8NI39O4hj1byJoGc1Zk1XFY8lOTk-YDhZjit2VRQ-Q5u9f-CaSPMR2DwzvHsx2gMgeM8wdaR1ioQeGe2fGOUAwjxmse3OwA3Z4YLD3YYIDjf-Y8d6xyduW7gjn0-jDmjYbz8GvKXYrai2JXQmwb0_Zn1yfkSbcMmwSCsYPOOUcBaxTgewD9uJFo5gWY6QrUPUmUzUrKlgh8UsX220_TGV0X_JKrAETLmRN1br7RuyWDXmbzOEOa7i9GO66Pn1Vjl-V41fl-FU5flWOj6sc735qtn9qFH6--VDoSwdkj3IKFswDD14kQWQFiQxm7twSge84ViK5G8fCCSzbt_x5GFp2nLgzf55Ycej4Yegkgg6Rb47n2imYu0DNfPuGU7D-DPr_7xRs3NtLpBPCVOxx4Xb2BkO3s_eQiWlWcuyZZ0Ea2H4061YaDFGz0oMmYNsIulvMS2-rAvDnuEov8nQiP0rR4NXOqFRNSbe-g71qk-bomlSwHzxGn00mcdG0H0oyicDrMYslNmI0d0SRxSwqGt2PY_bchrRCxNScmgSdwZcUEoxxSgliG6QsgWWYSiD1Jhm6k2ZZRZ2sWQd3CLeS1aKgsMba3vmLs_PJm9cv_87kR5E1dWurugAsd5EKGTeVDvS0yWH_o8Kv7FJns9WLY7OUXmMlJ6IbAdV4t14lqZP7pStdSgqDUlIftwa3UKlcDfyC3CxJcfIcmg91QTpZhHKsyU3GV6tKrrQPxt9XUkF66no-M2nEW0lRCUmo7Tw1ypUyPyzQLkWSPF_LDW9xqIMjt3d5klm6SqOUZIJZm5pD0DSC0wCTTtk5RPeaVzpQ40etlXhf8l21Lw1A-2yaA-J6z0vzCWngUIxndjlD13Dj0jPgi3hTJ-R1MVEktikReyZ3UCKbqd6I4DeeZbQ_0CnoKy8Is8b-qU4jGX_VN-6usiUd_aKdFLYEJuMsLuAr1XID7JO5DPK8IdS0AiySa36ZFlWXU9N9tMTPvxwdTfEHfcO3GgTTZy9eP__h1cnpX5enL06--_H1i7Mz_PT2zek5WPGXd9_c74UnOnqqDo_fY8OCNBE4Wd2kCrur6-LCcJCdOH6QhHEUW3HHQQNtPGS7h4pas2IAcvcCy_J84XcrDnTuQda7h0CFj_dlu-cVfe4Ys1dnJy04X6ZIIqhd8Rq6hW_QLbI-bkPvV2RdDhA0bgqQYj41YtH5978cJmRGN9S6kkSaQqboFOITYBkgw8_0xDEIut_gntmTM5f0TIy7bVfTc3qlKXlzzAhXSu9SPxTEeIy-0mqvzzxWNRHRCNCoPkjtq-mPG3nxLzKXFa3Rpk7K3-SVtcdQaEjfmu7Va23fRFG3u-8rJH8Tw6PZSQA0tMiGKzBTjA7OyARpI_i94mkOqBJ4a74xKW_DIO6lL-t9JxPcDH10DNqOt-4MYgJpQw4QGuJNqggWuj56vNTXufat7nSzHhOgL8CO6xU6d81FUAwSX4B5uCqqbiwQD27b8oy16_Cu2rQu9kkABIoL4ElfpX-BkIst-7CWIBGFUbqBO2CrugfWLbQ8yHG9LhoMXfpFVpeyxZ9ORJo3erToc480pzOSCgqLMINUcSFk2X4H1hR-DLe2iK1GoCVEtGTppqTO0XS7wQ4IsW5QJZovJdxB3QdHMjq9N7H2GUYpZEgPkf7rc7e7wjjC_b7wNbYHUCsGeG0uu8QWRYa6E9DN8Ggx1bPtjs7fdMvZ1jjwvaltj-dOyL4J50fun58cDxOIW7Zn90_M3SOPnhhmAqsrzr71jmxqQyJW-myuP3ajmqIqyIwTDMGW9hLk2gjoFNlU56GeQufzbNImsGP92595Mt6z9P2Pr09eYhCc_fTynAbC8xc_vj0_O3pfF_mevVuefDLu50fLcG3L6F4vEWiqGH3nrG-ZJK4fWG6U-LHnWP0k2R0HDCfJw_bxZj1uJU5ox2HId7p_sLU_OEfcP3SOnHdYxrzUCG5b3kzJfgIAYekK4pPak_oXRIZ0SnoG6IcMbj83aynV5HVTtkwz4SX1JUdDFDRGLkEqu4udzCFmft_yBm9p9cydqGIC8r4i0o_YSXc8asiTKCjaKgialvmOW2oddAySD90GT4FJJpqKDisn7ZQCiXHSbzrgqxpN79pQv5sm0An2wxC6nGaMkWmgl6igQ4fBDKkg4NsxqmeQHqCtRDfHw9Qlw8HS5taYnNQgUhL9e44htzyRE-Sv5K0Y7_ccFMWFlGUvbcx2AA0Ckct7jh6Mkp-0NTa0ps8a2knfM0QP8RRDpIQm7wcNjfNJK51VN5HM8veaCDrfOxTk2ISbWhFuBoAyAqM7HW__JRoFyZn-vsaKBBIywlO5ZsMMAxd1L2BLKBLKN9H-m4N8r0tC1dopGGQGBYoIqx0YKfN5gbXiFWmbKyBb7RK_Y_yTloYD98Yc1-PdBOoc6UqEJ2W6WqtdrlpEtHmp90XN4DXkVP6hLL8DtWHhfqvcYrNrFi1r4DZJthu2Ge3_B2cuRp9OOrKY3rTX-PJbT24ZBXTw5CVhFEgZdNQ8OMQcjoIHnz5202DueP488bht9WcpgwPJg9PgHieJh0eF2cjqmbHZDVGzQ-p16n1nyfcmH-zlybMJyosGBLBNbrqSD3RYn8gKvSwPcy29QqMJCwNv-kQAwFYFhoM531Ck9fQj7XGMIZu6J4oScsxIt027DyCjJcBCKdTtaKIHXnHxJrY839nf20RqeGdFUU0B_Kzl3L4otxAhHVnRt761hDdtatqR0Tl2ZTNH40VI9FcPtzXNhmKFLdFunSvM9srw9HU-of2SMXONnk51Pgkr9QBnHbY7jB2TyOqPGAxDg4eHUOr7gbj5bscM5jvnNAY4aoBjcjmf2N7kav0n_fmvPxCOj2DoOku8-4w__wHBPW4M)
