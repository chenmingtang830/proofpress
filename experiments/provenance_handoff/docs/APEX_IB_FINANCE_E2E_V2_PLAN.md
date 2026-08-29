[//]: # (ob:f92f0435)
# Proofpress Finance Evidence-First E2E v2 Plan

[//]: # (ob:794146ea)
## Status and immutable predecessor

[//]: # (ob:2deab17d)
This is the active production plan for Finance E2E v2. PR #54 and run `formal-pr54-telemetry-20260828T0610` remain immutable v1 evidence: 12/12 scheduled cells ran, 5/12 produced gradeable artifacts, only 2/6 pairs were jointly gradeable, and the result was bounded incomplete. No v2 retry changes, exclusions, or results may be added to the v1 denominator.

[//]: # (ob:c1a3c596)
V2 adapts the evidence-first workflow architecture evaluated in PR #53 to APEX Investment Banking tasks. It reuses architecture and generic contracts, not Legal lifecycle categories, Legal conclusions, private Legal corpus, or PR #53 development scores. PR #53 failed its own honest-gap promotion gate and is not evidence that the Finance route is qualified.

[//]: # (ob:4388cfb2)
## Research question

[//]: # (ob:f1234aa1)
For a fixed executor that has first passed a frozen Investment Banking reliability qualification, does replacing access to a full frozen APEX data room with a Proofpress-governed, task-scoped working set preserve or improve native task quality while changing completion rate, latency, tool calls, tokens, and model cost?

[//]: # (ob:c6042476)
The causal contrast has exactly two headline arms:

[//]: # (ob:8d80ed42)
- **Normal:** public task, byte-identical pristine workbook, and full frozen data room.
- **Proofpress:** the same public task and byte-identical pristine workbook, but only a governed task-scoped working set and permitted source extracts; no full-data-room access.

[//]: # (ob:9f5acdc7)
The same frozen executor configuration is used in both arms. Upstream routing candidates and component ablations are development diagnostics and never enter the treatment-effect denominator.

[//]: # (ob:186e565a)
## Evidence-first Finance workflow

[//]: # (ob:873a06b5)
The treatment is constructed before executor invocation:

[//]: # (ob:64b4f6e0)
1. Deterministically inventory and digest every source and pristine workbook.
2. Decompose the public task into frozen deliverable, calculation, output, and validation requirements without rubric, gold, or prior-answer access.
3. Retrieve task evidence globally, with deterministic workbook cell/range/formula locators and document page/section locators.
4. Extract source-bound Finance atoms containing subject, predicate, value, unit, currency, period, as-of date, support mode, exact source value or excerpt, locator, and receipt digest.
5. Construct narrow observed facts deterministically from explicit atoms; models may not rewrite factual statements or their bindings.
6. Classify records without changing their prose or bindings as observed fact, derived calculation, calculation choice, assumption, risk signal, or banking analysis.
7. Independently criticize every candidate for support, scope, units, period, source version, formula dependency, and task relevance. Ambiguous, unsupported, conflicted, or material records follow a frozen escalation route.
8. Run independent requirement completeness and honest-gap assessment. Preserve missing inputs, unresolved calculation methodology, circular dependencies, version conflicts, and ambiguous valuation bases.
9. Deterministically validate the governed graph, typed relations, source custody, leakage boundary, and execution policy.
10. Materialize only allowed records and source extracts into an arm-neutral working set. No model has admission authority.

[//]: # (ob:b492c1f7)
## Finance-specific record semantics

[//]: # (ob:83685f85)
Observed facts are explicit source values or statements. Derived calculations must retain formula, dependency IDs, units, and period. Calculation choices and assumptions are not facts and must remain visibly separate. Risk signals and banking analysis may be included only as non-authoritative analysis records with their evidence dependencies and qualifications.

[//]: # (ob:cf82346c)
Material conflicts include inconsistent period, currency, unit, source version, transaction perimeter, share count, enterprise/equity-value basis, sign convention, aggregation basis, or mutually incompatible formulas. A material unresolved conflict blocks execution. Missing evidence or methodology that can change a requested output is a material gap and blocks execution; an immaterial, explicitly disclosed residual gap may proceed only under the frozen policy.

[//]: # (ob:bc3277d2)
## Qualification stage 0: executor reliability

[//]: # (ob:3b3abb52)
Candidate executors are tested before any causal E2E. The qualification freezes model slug, provider, reasoning level, parameters, adapter revision, tool policy, retry policy, step limit, watchdog, prompt digest, and no-fallback rule. It uses development tasks excluded from the formal matrix.

[//]: # (ob:3b62cee7)
Promotion requires complete terminal telemetry, successful workbook finalization, valid required output files, no unauthorized source access, and at least 5 of 6 completed development attempts with no more than one transport failure. A timeout or transport failure remains an outcome. If no candidate passes, the study stops with zero formal artifacts.

[//]: # (ob:7f1d19e5)
Ling Finance remains eligible but is not privileged because it is free. A different executor may be selected only before formal freeze and must then remain identical across both arms.

[//]: # (ob:cd668150)
## Qualification stage 1: governed working-set route

[//]: # (ob:08316b1e)
Development tasks evaluate requirement coverage, valid explicit-atom rate, source/locator/digest binding, unit and period retention, factual unsupported rate, material-conflict recall, honest material-gap recall, final-output leakage, schema completion, telemetry completion, and escalation rate.

[//]: # (ob:ca8c556e)
Promotion requires all development tasks to complete; 100% source/locator/digest binding; 100% terminal telemetry; zero requested-output leakage; zero known unsupported factual records in the allowed set; 100% detection of frozen material conflicts; at least 90% honest material-gap recall; and an `allow` decision only for packages without unresolved material gaps or conflicts. Failure stops calibration and formal execution with zero formal denominator.

[//]: # (ob:a2f06943)
Premium-model judgments are diagnostic references, not gold or admission. Frozen human-authored test fixtures may establish deterministic expected conflicts and gaps without exposing formal rubric or answers to construction.

[//]: # (ob:89c7316a)
## Calibration and formal release

[//]: # (ob:da2460eb)
After both qualifications pass, one fresh Normal/Proofpress calibration pair validates access isolation, byte-identical workbook starts, neutral packaging, telemetry, grading, reconstruction, and compaction. Calibration quality direction may not tune the treatment. Any leakage, digest, access-parity, fallback, telemetry, or blinding failure blocks formal release.

[//]: # (ob:efef5673)
Formal tasks and attempts are frozen before treatment construction. The initial target remains two fresh Investment Banking tasks by two arms by three attempts, for 12 scheduled executor cells, subject to confirming that neither the selected executor nor treatment route has previously consumed their hidden evaluation material. Previously observed PR #54 task outcomes are not automatically eligible as fresh v2 formal tasks.

[//]: # (ob:d9b96b8a)
## Grading and endpoints

[//]: # (ob:bb519388)
Every valid artifact is graded three independent times with the frozen native APEX output verifier, blinded to arm and excluded from Proofpress sidecars. Majority criterion outcomes produce the artifact score. Grader repetitions are not executor repetitions.

[//]: # (ob:fbb8f821)
Primary endpoints are scheduled-cell completion and majority native rubric fraction. Secondary endpoints are exact success, paired gain/tie/loss, workbook validity, wall time, steps, tool calls, tokens, executor cost, preparation cost, working-set bytes, retrieval and graph counts, gap/conflict outcomes, and safety stress results. Report scheduled, valid-artifact, graded-repetition, and jointly gradeable-pair denominators separately. This is local native grading, not official APEX Pass@1.

[//]: # (ob:b1b41b09)
## Stop rules and evidence

[//]: # (ob:fae89532)
Runs are serial. Valid bounded model failures are retained and never selectively rerun. Infrastructure invalidation preserves the original receipt and invalidates the entire pair before a new pair ID may be scheduled. No post-observation early-stop or exclusion rule may be added to improve results.

[//]: # (ob:7b048271)
Every call records model slug, provider, reasoning level, parameters, prompt/config digest, model attempts, fallback state, latency, tokens, and settled or explicitly unknown cost. Every stage records inputs, outputs, digests, decisions, exclusions, and errors. Private data-room bytes, credentials, raw private prompts, and hidden rubrics remain outside Git; sanitized manifests, schemas, tests, aggregate reports, reconstruction digests, and the portable plan ledger are retained.

[//]: # (ob:8ed659ed)
## Execution phases

[//]: # (ob:74415cb9)
1. Implement and test Finance v2 deterministic contracts and private-run adapters.
2. Recover Docker/APEX and credential configuration without printing secrets; verify storage gates.
3. Run bounded executor and upstream route qualification.
4. Freeze the selected route, tasks, providers, prices, and protocol.
5. Run the calibration pair only if both qualification gates pass.
6. Run the formal serial matrix only if calibration releases it.
7. Audit denominators, costs, receipts, reconstruction, PR state, and Notion state before reporting any conclusion.

[//]: # (ob:93bb9bd6)
## Execution status — 2026-08-28

[//]: # (ob:3095ad26)
The v2 goal is active. An isolated `codex/finance-e2e-v2` worktree was created from current production `main` and merged with the PR #54 harness so v1 evidence remains separately addressable. Protocol implementation and development qualification have started; no v2 calibration or formal executor artifact exists yet, so both denominators remain zero.

[//]: # (ob:8ff6f75c)
## Qualification update — 2026-08-29

[//]: # (ob:77728443)
The first six-cell executor qualification root is immutable invalid operational evidence. Its first persisted cell recorded complete 14-call telemetry but a 38,590.25-second host-suspension clock gap and no valid output. Its second cell completed with a valid workbook and required output after 52 calls and 3,302,083 executor tokens. A third cell was interrupted during world population before any model or grader invocation after the root had already been declared invalid. The root therefore contributes zero executor-qualification promotion cells, zero calibration artifacts, and zero formal artifacts; it is not pooled with the replacement root.

[//]: # (ob:d21d3360)
The fresh replacement qualification root `executor-qualification-v2-20260829T0953` passed its host gate at 21,591,642,112 free bytes and is running six serial cells with an internal process-bound `caffeinate`. Rebuildable caches, not research evidence or Docker images, supplied the required space. The upstream fixed-route transport/schema canary separately passed 5/5 roles with exact model/provider receipts, zero fallback, and $0.0006642 known cost; it is not task-quality evidence. A freshness audit found 13 same-world Investment Banking candidates not previously consumed by the frozen Ling executor and excluded the three consumed tasks without retaining rubric, gold, or prior answers. Formal tasks remain unfrozen until executor and upstream task-quality qualification both pass. V2 calibration and formal denominators remain zero.

[//]: # (ob:f1ba67a0)
## Frozen executor qualification outcome — 2026-08-29

[//]: # (ob:8ab8bfba)
The fresh replacement root completed all 6/6 scheduled serial attempts under the frozen `inclusionai/ling-3.0-flash-fin` configuration through Novita with no fallback, no unauthorized source access, complete terminal telemetry for every cell, and $0.00 known executor cost. Four attempts produced valid required outputs and finalized workbooks; two attempts ended as retained `model_error` outcomes without valid finalized workbooks. The six cells recorded 251 model calls, 16,150,235 tokens, and 8,581.795 aggregate elapsed seconds. Post-cell compaction reclaimed 14,067,248,546 bytes while retaining hashes for the removed reconstructible archives.

[//]: # (ob:154325e6)
The frozen promotion rule required at least 5 of 6 successful completed attempts and no more than one transport failure. The observed denominator is 4/6 successful completed attempts, 2/6 valid model failures, 0/6 infrastructure-invalid cells, and 0/6 final transport failures. The authoritative qualification report therefore records `decision: block`, and the independent audit records `qualification_decision: not_yet_qualified` with audit digest `sha256:e75bfaf022ec6f439f0065b3f25471009b72090c3582220c71b18c218f9ad524` over source report digest `sha256:a2d95c710b1b1b2f8b298045fb4d92a688d18a588a5056d06dd5ba7d973585c6`.

[//]: # (ob:e0183a18)
The stop rule is now active. No upstream task-quality qualification, fresh-task freeze, calibration pair, or Normal-versus-Proofpress formal executor cell may be started from this protocol state. Upstream task-quality, calibration, and formal denominators remain zero; the 13 freshness-audit candidates remain unfrozen. Passing the earlier 5/5 transport/schema canary does not override the task-reliability failure. Any future executor candidate or materially changed executor configuration requires a new pre-registered qualification protocol and a new run root; these six outcomes remain immutable and may not be selectively rerun or pooled to manufacture promotion.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZlNGRmNTM1MWM1NGU4NTdhOTMxMWRhNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjI0ODA2ZjE4IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9jYmIwMmZmMDY2ZGRmZDMyZDEzMmExNzAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhjNGY3Y2NiYmYzMWIxMDk0MWEwZjg2ZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfetuK0eS5qsU1LN_ekmp7hedH7tnfBkY6PF4PV5jgRlDyqrKJKtPsYqui3Rkw8A-xDzhPslGRF4qSUqUjqSeRWMTaKN1yKrMyIzIiC9uyd8v2DA1glXTTVNfXF_s9zeCx7VIoiSokpjnScaKKAhqFl-sLsq-fripmw0fJ3h23LIwSa-DII6KoCyzIgxEXeYhC_OCZ3XpZ7UI0iITfp0EPBVlGkci9cOE8ygUEedpzqq6hHHrZqz6Oz48XFz_jv-Ybia2gRlaNuFUK_ij5C188DMfGtGwsuXewO-asek7bwvP98ODVz54Pwx9L_YDH0d4Z8-qT2zDcVEHHw_9Xzksdx5wwO007cfrq6tNM23n8rLqd1fVlne7pttMrNvkkX918PbAf50b-PtmHvlwU_XdyDvYi2mY-R-riy1nuIlhnPupCPIL-ckNv6OHYHP5TVWWfiiEn6Z1LeoorIMoZEHmI2X9MOHSbtqm40C55kh7k1exyCp4VURBGfhFHDBf5KmQy1HU3VRsP84tLDhEOqt-qMeL63_7_UJN__sFcLkfRvxLfs3rmxK2_N8u5u5T1993F7_AGrQ8wNT88x72ewdvj7gLMAzrKn6zZV3dC3FV99V49fGHb_7XzXf_ePPtd99__P6rb26-Cb-5-Tm8-eEvH7-_3NUXqy-SLzZNQ1POE7D1pmRjM6KU8VbcsBG2e-I03jxt-wEX8anpcMjxYZz4Dr7p2A65rRezgldHlJCL625uW1haBZSD7NKmlG1ffYKnRREKP44SeBy4OfHPuPBFjrxvG1q0981dU3P4Y_1tM4yTB8v07kJ4SRHB6pqo26NY8nv45E_eS0fxfmgZkjs97JF-FBkQv4s_VguVGbA8Tjk7oPJfJzbNowfc8JrdbibZ8WC-mlcwJ-zROer-5L3g9TMUhTVnZZDV70bRT3COPfjftOUeiEtzh2_29VyhNHh72CJP9MOyk7R1l94PP3p_ShZS92xgB3RWAYuqpEjfjc6fQ4_VbD9JSrlmqCCG3vfDJ9H29x4bqm0zgZ6ZB3yItTOT4vsUnXGU55UowwM6f-Qjx5G8X2fQgyjK51n62PNneCiCMIoZC14_57fAEeaJ5jOvPf6ZVzMoGNgXNnlbNnpyT_Z4eGt8bOh_4533XXcHA8NRPcO01I_DOEtfT9hPwJuKzSNrPRxhYKMkiX8G2WofvOm-93BLUNUCs3bj9Rly8jr3eR2_gTdr789__r4fdqy9_vOfvf1ctk3lTWz8tAKzNfE1CtHUVEDtfgBzhkShKJV9_2m1ENbCVweEFSIBC1plb9unEfSmZo5hIownms08MDp-cC5nZGLTeWU_bWnHLs_sWJCnPEmTQ331zeFZ0SdZn5lnZPv5t89Iep5FzE_L5L3owW2bBs4mNI64O4gEAARUcMi9koOi4stWNt1dX9E-nhOyNC5jkXL_vUgMLr2v-cQHgDIoUSBbIPZAChCMaAl1n0RyoJ4AeXljPw8wNH6-PyNyZVyEVSAORU7RtR73vAJ8VnkSX3gj3zGU6_EZ3r7k_XPcjdI8EXnyfjT9Swl44w54icgFDAWxcw-Htpn0RqFO56MH_B3BmnBCSbjlwzm9JnLQuGn1foT-M0w9NFLLCaAPiG26qp1rjv8PQgn8QxFFINfXK6-ahwEE6mHlzd0ZQssqCrOsPtR4_2NmLRIoVQKsesM9_3qR84G3AM2b9hlmv3SYZno4z_aojFhZJu9P5FdwCJoadta8JkUAnZHlfLPuQZsYACOXHuqEX-czmxqVaVhxnr07vQA0dz29r90TEIfdvoXj70kNADROvAUhnQZg_ThXiHPE3Hr3Z-jNRFAHBU_end6_ACeNLhtAzJsOLHPbbBrEYYD_UaN2_YTG8K5p-YY2Hfeae-dOV52meZD4z9IbXHsbdDc7GBdVKZCzfoXQPjbMyCdv6OeJnxddP4-CtAz4u5P6NSjztt-TWUJ8MRrwqWWDviJvG8ZfoRpraqnczm0ty6skSd-f3kdEFwyVV58sY-qNTH_wAt__L954hl4GTl1axNHfgF6-a-bdetfXvPX-OtcbUvykHuqGbboebS0sRnDUs3xckSBv-rY-J7p5UWUgEYd46Ssgt1QADM2yIACJJ4yzkT8jsM--fEY6axbGqc_Ld6LmowAlJHHjrzYLRnINVl7fIfzk49aTEPnKcpzP7BlssUjSLHonKr-VT0ppw1fZBFZ9r3ir4LFS_Qv0k7jvDJV1URZpmR9y9p8G2nSahnf1vm9Ahp5h6FPvnOEjGMegAL_ybXN_Q_BQ6gkdzEEFvYGB4NRM24Ej2Kj5HoajA9vs4BjfN8DvMxsjyjIHOBS8jbgfhmbHgDzzMHFrrLa8nlteryvetlpxaJnYsb_2wwG6OMU_QRkHpV8cRQ36vTfAsFI-tOv_bJjlqbfOeeaM50UShW-d_8e5UztCKPHS-5nYWPZzh7yTWkywpp1J8w5oJSYwx-ivn0MGpR_nYRa8lTwpWuiaKNA7KpLGdt6sMP6Dgwwr-JaNfYeS0aJlgK_OkZfzOk0Kfhib-oYQCsWStqAKnjtujzx-Lj4Xx0FSlcWrZwRv7TsUUlIquH2INQ1GugvBIlq-nIppkGvS1cfe2i8rHfK9gP3FCOhNhQqLpqRvdCyW30S1CKqgjOo8E5FgQREkJfyFCwG7RburotKeikp7cLaqT3TYKMg-0EwYYdX_wgDrLxjOBn_kwRrBDnFbg1Dw_JXR77EX040AbvABsKIKso9lcB2FrGJ-7vOMh1WaRIVIgiD0o0wUiZ-wOsqqiGeFz4qsTPygCpnvpwwwQxIHPIsx8oRuHQXLJbeuo_gP2GgMSYd-mK79fB3mP4X-dRRcB9F_9f1rH5Gn2nEKzpQhS7IaBGX59Pf_p_F1ElcZ_waJ3MLzaCACXoVlJNBM0BhWSFxJ8rvEstWMuV-VUQWchDOjZ7TC23rG18anzbp8kBnYl7BiehYrZK1meUvMOSbKhrnzbiXIWO-HJF4bN2uNUuLnICN-Gvi3ys-xlnIXGB157QXhVRAudstDuzV6A-tWXoLfSLLgC7K69L5mPCGo9sELr1JQi8AL7x6wp_dXPFzwsXlhJfXKFnX8OLeTd89GYwkwWCDR9SWgMGTkgIvwVMpkBR5C1c4owzjdoIYAdc0eABR5dEQQo-PwsDBYVY9uJ3iEj4UJFZMqEQd5EUY8DY0oWPF6xaS3BNwxYEncipA4PEsm_Ax69h9Zh4BfYj5QwOC6cfAxx8PBcNc2vIOTauldCev_wjcAGQHR8uqhajHiPPENYAvcMPkdvLDsG7qz6Inpr4b9LHdTkWh7PSN8zcdL_RXaaFwO7EJ_33lbwMzjtN6wPUqG8qA2ODYdF-k9662SAXncPONzo4eKjyk8zuszXIqFX1ZCsKjmhktWtmI5sC_MPqhhyyTioNhZGIXCaJ4lIaGDY29IMFgctmJKhz7Iyqt7YPjA4bBXhDwpNILSAuOBUdODkuzUbGKwef1OoltmqcW1diNXJE5r4N9-8Sk9jAvgcxhVRI43O1L4HhwR1Dr4iiQMCLzfNihLePLwVQu9gmMDxxiz4hTCm_q-JfQ04t-fOMoYAVzCUBW4ov_tabamfhYEYADTMK3N4VvyLkZDvkMeRc2YFSLL4XBzHhpbY6VW1IxvSZVIl8_immHY5b93OPDCLxx80skPaxYa4vmJMEhFWpct8YOn-E4hdQRvE2okFT6GxZIi-QBHlUheI61rEi4pg5ePROHVTvp-mNWJKIogr_ROWrkgi3evze14_3M_ope7I11BYqiDotIko1SCEkK0WrbKnacgiKXDloCIfKfDTAO4ahgOmOwMypoLUKHTC80GL0QqKlZXIin06q2E06KQXpUyUpNEJU-DWkSlzCtIYV2ySNYWv1MeSM0bpCELggiBeKjntVJDat63JHeOhRmORojDEUdHTpyxDwTAiN6cJ9CjGDkkOAGzVnOr1ChIyX6e5AmkWAGzo3oySIZKE54D0FSCMV1RVIzsH9DUD2vWjYBctPT_exddgkmZwJpqBWkM2qbtS1zySurhQ99Ir4sw1NWA-OUKERqQ6rXIAArn4w711Ux824O7cTVyifr0I0BAfAluIB1TtYFrgktGkOC5HbEcXWY67XOJtUUrgqloYWSAFdwbb-6ayU6_6IQMG9e9QD3FMS6_Ry-I9PdKqtiDbBNuFeAw8HVgKEWn3HHwnnmznxTTgfTk0vtKiyIYmWEAiNQfJrXqEwECJu-WPBet7oM0JhLoIagY-P0A0IjGAHtlJb88ssy8GbwSvFzYDtzCFOhowT434sG4-FoMjIWTb4FBHGmJ-nXYm0OawVjDruG_DkTP-geM2TcVQt1xnHd7-T0I_CdvbDYda0naSgUKGHzwMDZIZgbob4lgwVZUsEjYhd-4OkBG-5FDoBi18kjbS-aOC081z6TTt_K09OkJkP-ExVGoMTR5h-J06X3claCWewSFc6fmQEChc3tcnpadzvnpDRV9SxDYKPoRtkSdP0R6sMAczhK4KnaY7jAfIMF_h9gHSbMAJqKrccTHAI1qCLNrgKewh00Hp57ohW_69og3HnhC277u234DS66aAb8Yln0goKy2aclgys1hejM8CebxkRLDKLCa4jH1p7SOVGDGKIP7s98CPHpAqwx7LU2V4VE1j1NfA3EtZ1gtKB0iNigO8SWEQ9EMmDvwLz2ddUX5kCgAGUATSI7gu0eGXupR8CjBvq47PsOnrQ0TyO-SyA0BFqtpizFkSQVvAAzPAIK6EEzESZlkFHAjq2Fl6heT-MpMu7a8LOQwZhDmYjGKS_JdTfOW5Pnx6QbFAxxSUUl9kFbWSfK--3o0B1AhLTiEl5gAOdIKKqxvNIMkDZWa0KE0PRu56lhfWgJzR45GGj3jHxdNIh8_ViXaH1Y5-FpJB_pj3VozUkJ-84qtFpUqNIbOPik04WEC5QxISkIAMBFP4orgvIT3S_mBYtVbygfQnh1rOhDqbmQqfEKxrQnDt-MWd7qCowXvEP5DFMKvUANND2tp3Kjgc0Xbi-QglqEx2WYzgMOsFUAjXebdjOaHUA8qL_gaYyJKQECWPi5q0tZNapmejIQt5xvOtNJoZu9xkkV9SacTzIAKiYC2RQUqKwIk-EH8x5ZpSXeijBxN9QGVQLPTz63M4YDFYCF024-kScamntUwKFVgHiuuJQqDNhJDK5Wv1NPT8iDSMg6zPA-S1OBKq8pj0RBvLs_Q_n2Z5SwpWV7WZkKrYsPk615famHTKQbOf-NfkD4YGMkmKg0MLvHBFJQrv1ru6ErFwfS_gKq91zY7FP57NlXbupcz7Qz6kmqo69cC5LNk1SdKilB4iYJLp7ltiq2htiAARlyVyUiQkaH5fIarWRiXURlwP2PJssmmzGQpZ351fYgG0wIfan5TkEtmA9VoRv5F08qEN8inUna_LR6vxPXKuE9ocEHVJh6g39SQUx_sjsnAkmrs0DwOFM3qKGdMyoYAs8pg4anH5COCSwSjx9-bWhMcYJ5gUmSLwJEXfEfRJAyooPc8zTXo_6nfKxp-40OvmWPir2f4U6ciSuDcsYqbMLRVVqP485Z6mIa-RPHH1deNoMKDaTmvyiKNwF7ySkl_qHOlViIPz2L_YOmdiVebKAirAKCP5-s_jRObsjxH2QyNh25V55xXNq8oq1HTsiAqwzxP_GhBQValjZr2LSUyoKXX6BepSJyU7Cvlil0pl1v5L9JGWpgEVYk2atp9snC-GlPbhbWxVQAQQJOsFCZfHkDLoL-j47lW51Bh2RXlE3bMiiCulmN-8ClhXctrQLTzNHt9noSiyrngkQk_WRVCT2udF5f2nNtX9cyp4vogj6cxy0fbob6m5pCDfde80EAMpJ4SQgrTg-ypKdFjltgGlJYyvLsTBPVh0W4FvPQ01z5IVdh5tzTVLYxfyZYmOqPoaKoepsVntrCMDTQIShsKLr1vlcKTqqt6vChmcW5OdNvLAnFgzIsiqIKKLyFkq_LKyMHrS6Yw-q8dIViV3PLtDL6KQtNcZcpF83miGgZUd_ABK8FFOo4MYb6VdOCCdim5w_bLBsMzPeFAXTlEsSoihMJTSlxVaAXJOqP9I57lPE7SpDYpDqvSa1GDrynW0gigjHwWJiCfLNJzWPVbao63lGDZ0oP5ReNojzpZ0oBEKmBwFDk38AE4MlDWTDm-UrBJS1rAYyPLf1Z0FJctXpmIs3QtLg82TKdNalAx8nTqWNU0d_ww0Aw2EqCk0Y8GsNE61sA_GAiVswRuB7Rh4KiVGsjgCQXtD9l1DoQXRZmWWcQZNfwRs6wytiXn9epKNCWThJBB7KeGBho2fDLAAlM2ktdPpUKxlRKfQitPf1OJl6aC4lneQbZ6ySxwSkapOKg6KqLBI7iRHlTH4aAp38VgEvN-R7BNL0mmKTEaQoUy_TxiZA7WOe-o8Axd5W1T1xjyWoJEWi9StEq_ZeKIKndPoTeFAZc4AOiUHl5XASWDwNioNuwu1LyWKeMznPbLPAyCpGax8X6sUsDl6H9BWZ8aGhRI4pdxJsKgNJ7cUulnOkdeX7Vn-ZUqP0nZT2VO76gHF90qOg8y7w-iogJmtitjaRHwZsHoDSMGz2T5HcVYERh1CyNUmYO0v5pqSoVf0k6Rm7YH0HIYv7GcU_PlWXjKwySLWcAqozOtckRjt15fWqj3TVkPMWjF9a-o2OrTYVWwf1Y-EupZDF7Cgb2aGkRC-KnRpsRWUlX3CKmQddI1HR9PCluZv1FmJyiiJaOu-ImNs1GFj9LvbfBYSRuJYVQZwYHvwGJeGXiqmSe19MgEn9BnIq6rMhFM5JAjZnZPoeq1ZvJKCeZ64aAc76SMZU02yAIoownQtQ-o-GRJD2LHVrPB2BUUll6A9UO9SEL9A9i__x6cO8llIEI4cpwx48JZ5aF2vdIXFHqalHgRlrUIAil5UhKX2k_d0feGKk6TdpXKFnajxUzMMHeY8hCY0Eejgdas6azEnS5WkFU3INQbAts60URlJt2CBKg0B4z-wCVG0IEbmPxefvLd18YV1UJAIW-AW9Naqmc5M2dD-7BG5KryXbJ-hrb2pN5I11FoQTtTxhIVccFZUtSFcQ6tOtYDtfm6itQlpCTjQVcyz25QhhzIMqM6PkQx8IO6jqWWA07khCaWtsLECVWPO53eS08SLb3nxYmRiRmptEeNdfAP5WUcFXWRzA4DZj5Bb8tCpaUkQSmFCsvvOkQVqCHYvSlpkitWwyibLJXfqCMJQAkaAe-fGvCnRobg5DdyY7pGSMqku4p6S_5bR35xVag-xmNguCxKl7aZalUq3oON22BG2ToR5-oKoqQOQ5FykRp0ZpUSW3UFL6oN1kGJKo6SjOciqIyTZJULLwn9V9f_aiassRhRRTNHmdX_kVMYw_sacCofqJhUYmnDx6NiEO0GUTWtzEzBs-jUktmnYBhGRajYTCfp587oImNpcJbZriE5itjK9Pq3MvJ0AAbpYVlFNS4nTpbPVdrMwMdTX_WtTHUjBRNVKh25KuRIN-IRz0cugNwfmabWYyiAJ1WtisCacewJFNyHozbJDPLHGWzygWVa0QGVYotqczz1bACPquOPy_q-14Ew2C-lQ6XsS4z4YBUUnqQDf_kDxe6R2z440GXu-vgKtNDni1_o5hAqKT3-_OhuEOtzFVdRX_zYVFs21N5PDAT-7_LmEAokvPbikCIqy6Ks0ydK_kdZvfx__vd_eEu5-It7Dp56-1w3rF8krA7fjR70IEHvbHo4BZjYIuyA_rNy9-Gk3lYoG1dC5ZR5yNd34S2AyWMdC9JTtazZPbmDR1So1oOPZOVrmgtI4UeLeWr5jw_2oxLrhXw4yF21pSMIHiHIcich6zyq00gRMevIX51Gx0a5OL3hv1_cbx_MZNKNsRIhGATB2OFhQblRugBm2gfjKR_VqVp0UDDiJIiHfrLJo1xi18GLu0DyMi_LLIh5kvO0FAmYpyAGnGB2z27vsFsb7JaP390xefsxeXl7znF7SvjH480nz3XivEu7TYx1kVEV8yiLwrBmIvIxB1SlZVWFcRYWQSbCsChjxtIqZ0UOXlUQgteTVXGWUQH4Y-t5rNsmuvbDR7ptai54ITLmum1ct43rtnHdNq7bxnXbuG4b123jum1ct43rtnHdNq7bxnXbuG4b123jum1ct43rtnHdNq7bxnXbuG4b123jum1ct43rtnHdNq7bxnXbuG4b123jum1ct43rtnHdNq7bxnXbuG4b123jum1ct43rtnHdNmfSgXES5oUQYVQXxmZZZe-PSfIXFK7rDFPG4riMgoRzE-SzatmtCpnXVqMPnyZEqVinqhoFJKyUWajJrtW9RRVzKzEYHzBAapCsQvy6m2Ls7cpb4xUtGAKNC4IXVCOoCqWgUSsEHc_FTbdDWYfCtWV3XPq8vKYKL9gCW3aOuyXwwGi4yz8DN0fvgVN-TYruAdxR-hTjNSfa7GUdV_8CoP_jd95TjVfHXx_1X51-7dqwrP6SXIhUZEl15pe-5j2lGg4OW_FFv_f21AjnfhEmy8I8PvsLZF9MF55uWVw3Np-lR2QE-vBEAIog_3Opfz_3E1VhUEdR6r87qeTFy2Jf_sixJSJv9QrW5suXdY9ZjH-yewwzxLJ97Nfj1AeqX119okvpVVPCUXcWYpvLp3h7rtdM4nSF2xXjTndgRWXmGADaY16fErEqsEMQa-AqlttgJn-Y94u3hjppbSkrK_L2FIOfp_eUa5LKI3hRsY7qdii0Q-_Iaia0yiuDW1RxwmGZD2Cqtl0fN9fZoVhbAV8-22H3_A4_sa4Z9tHU5C8LNJnMlUXT-mihRnZO6utOFraYn6N1fUGHXpJHVZ4zXoegclmdVwwghwx0P9qhZ9qhnu_Qcxr0_wcN-vKOz5Pfvfrj8T67_5TGwijIeBJkdVr7RR0lPBJZyOs6D8uK-34YZ3XMYA1ZLQQgkITHScKKskhKGDuuq_CJ9Rw2FhY_-cV1El4n6SONhVXFspQnrrHQNRa6xkLXWOgaC11joWssdI2FrrHQNRa6xkLXWOgaC11joWssdI2FrrHQNRa6xkLXWOgaC11joWssdI2FrrHQNRa6xkLXWOgaC11joWssdI2FrrHQNRa6xkLXWOgaC11joWssdI2FrrHQNRa6xkLXWOgaC11jYX8uNcB9loc8in1u7J3VsfFUDPYL-i10FW-QV1Htx5mfmCiH1YJhycFrGyh0n06_53L_cN8UAzGvYgpBD_qgPN0PuSQ7gnhNpn0JgmJwnXlRvkoK_zJMAAAjPve2CErGeQTnSNYmoKNvMnrIT0kQGVdJgnrT9gq0FDL1uMHvsmTnMHnCKESThBK70yPRKvLDlZ9HVukrQQNKdGybQU2HB8Q0eWEOZR5QXcB0LWjKfq_T4FY2TWIRGHAjvaqlNk0RQnXiyIktAxTZwvGrEXlRDVjVsoEb_CeDDfQsevZyDjJQ2NAJ-pECi6e9Jgpm6iCxCh2cdnctZe7mp9WOMzAfVBqEciTg_9jH_7gh7cyRyYs8KXIWFFlmNJrVoWNL8iv7a_BLUG66NwD7R5LoVlcwY3U3Sp6q5J68MAC5DFZpHK6CIKQ8jURiuswbLL4sPAMbpSyW7ByQctdJseiohrWnGJesYLutmBAcFQq_RZRQzk1b01mrGIAwFYIddEG3nROXUAJOJ6O-AAyjtw3XjQVKpsc9w6OJW2VAABVxryUUMKm5K52ioK5AWwurPUmuEtjNVocmpJ9M0nuloYFlXaV0mPAd7tI_-Je-76ewh96CmW2BobJdHURc1MrH4-ZEkDrcuiCiotq1PF2PhNCsQlmZszsNXVFMzcRYKP13AJxMFIWClxSqWcJeFKEzpZRc1x4-XlSpo9YAteyoojIhc6dIALe-aZ8Abwf7cyjmZJsIQnk_hy_pyXyHpnj3M6Tv0_8ugpKlGTtsPfz2qFL8kN0q0kPg4JkmzpcP9NKuzpyVeSlK9jeg96cnu5ctS464Ib1Krag3KdwzzZ1BEkdhwtO_GcWy8mdJs2KAxKjg4xILU9RxhmLuB3nEgvxvRPGoI2RS9d4bb-D7_qy6eVlfvyXQ534V1lK8zyxJVYRfPiWGz_xcrArpnqBdK6d06isep7oA8E2sHS-fEqxnaJgekxOdvZIxvCUDIK2cCqlcPiUYT-wtcpI8tOmA0dJX5yr5Qua5Bh2leP1l7frLWVRL0uGRx_ko70c4WeASKwLlWTPql7BIQtLXRLquEPqidvuqLP1QCMAbdS3qKKyDKGQBZfsebbc3TcLPt9s7he0U9t-vwn75tRTHbffxH4931f_n_D4xz3kURqKqoqTmSe6LsAp4nKacF0WegWsYYtNknbKYh0Fc10GSFnnFGTh2dUkJ2cfWc3yNQBBeB9m1nz1yjUAY534qgMXuGgF3jYC7RsBdI-CuEXDXCLhrBNw1Au4aAXeNgLtGwF0j4K4RcNcIuGsE3DUC7hoBd42Au0bAXSPgrhFw1wi4awTcNQLuGgF3jYC7RsBdI-CuEXDXCLhrBNw1Au4aAXeNgLtGwF0j4K4RcNcIuGsE3DUC7hoBd42Au0bAXSPgrhFw1wi4awTcNQLuGgF3jYC7RsBdI_D3fo3AchBDUYZJUtc5yOTSG2C6KK1ypndrftTBNdABWRrUJQ8NcrL6Ic-qgJe1MS4e4GkVx22jwR1rrloMyESX_lq0QNtaIL45BOsgGf28wZj9XTMxkyVf5P-ZTPyZIgCK8arSR44JRnOU1Ck6CCmhdM3DsjDTrfRonYDUXqqggC9mEdQ4RZ31KJw8CjYu0YxbOvg35KbeLlFDfRj0j4KfDCw1ESpJ1VelkUGYBLpbQkbMgnQVJP4qjJIDLxzwQR5cZkVi-aS8ZfuRuIqGH71mBA3G_qsqqIFTxzs8F8QrP81WYQyDxanS47LXYznFKIacMgpKoe76O1VXqL0G2ftVbQFHn4t3MB6WGchxmQlTAGb1yR5I8uvaW22cs6QoJD56tlIDJzZBefsX7UErx1fPzLKiZjfJ7sPo18rz4ZvmILC11vhRQQwkEZ8SUuSPaVPSclitd2TeZTRzgTs66nKrgyvXMjd0u0QmThv2zUsHg98sQ4D5uAE34MZ0ad0qu271-3u345aFSXrNs6QUTPhhyKtUxFEhwOolZSTCJM4C3y_KLPQLv4qSPAxDv8qCEoB7GOSiYHUSxnCeKEwoVYRa4dEcLKyLBN70S3i5DEVehkXux4ko47oIWZrndZCzJIf__CSt_bSuk5JldZHBrEmV3p6RV9DugRAFYK0l-mJ1Sds9La9sbjYtX6S615QCkqUvq5PIAVlQmQtdY3XjPK6tZMax70aHXkc3pdena7ma0cQqpFtvtdbYNB6QsHqJ_fxAYgVwxOCUtRQMC4Ac2flLCnerknsKtDbocwDEegqQUXccRc1hFwYM3xEkQcLtnrqlAAt8CzHLJkyzO6a2yipeb3Vvaf1UX9JSNSKDyHCQQfOif4da6cSNkFtM6VJ6HoNhaJFpm0ap_Y3FOGnGlckbmTY21VJWsJwAlfQsph5jljNVjQx8UZuPXYv0yx__F16kRiQ)
