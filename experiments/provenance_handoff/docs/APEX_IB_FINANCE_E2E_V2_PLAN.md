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
The frozen promotion rule required at least 5 of 6 successful completed attempts and no more than one transport failure. The observed denominator is 4/6 successful completed attempts, 2/6 valid model failures, 0/6 infrastructure-invalid cells, and 0/6 final transport failures. The authoritative qualification report therefore records `decision: block`, and the independent audit records `qualification_decision: not_yet_qualified` with audit digest `sha256:e75bfaf022ec6f439f0065b3f25471009b72090c3582220c71b18c218f9ad524` over source report digest `sha256:a2d95c710b1b2f8b298045fb4d92a688d18a588a5056d06dd5ba7d973585c6`.

[//]: # (ob:e0183a18)
The stop rule is now active. No upstream task-quality qualification, fresh-task freeze, calibration pair, or Normal-versus-Proofpress formal executor cell may be started from this protocol state. Upstream task-quality, calibration, and formal denominators remain zero; the 13 freshness-audit candidates remain unfrozen. Passing the earlier 5/5 transport/schema canary does not override the task-reliability failure. Any future executor candidate or materially changed executor configuration requires a new pre-registered qualification protocol and a new run root; these six outcomes remain immutable and may not be selectively rerun or pooled to manufacture promotion.

[//]: # (ob:b7c276e1)
## Second executor candidate protocol — pre-registered 2026-08-29

[//]: # (ob:226ec661)
The next fixed executor candidate is `openai/gpt-5.6-luna` routed only through provider `openai`, with no fallback and no supplied reasoning override. It uses the same pinned Archipelago adapter revision, Docker image, development-only qualification task, 60-step cap, 360-second model-response timeout, 2,400-second stage watchdog, serial schedule, output validity rules, telemetry contract, and 5-of-6 promotion threshold as the failed Ling protocol. The six Luna cells receive a new immutable run root and denominator; they are never pooled with Ling cells. A terminal model or task failure stays in the denominator, while any host suspension, incomplete terminal telemetry, model/provider mismatch, fallback, unauthorized source access, or other infrastructure invalidation blocks the root.

[//]: # (ob:4c106146)
A task-free adapter canary must first confirm the exact model slug, provider, one model attempt, no fallback, terminal token and cost telemetry, and a schema-valid response. If the canary fails, no qualification cell starts. If the six-cell Luna root fails promotion, downstream task-quality qualification, task freezing, calibration, and formal execution remain at zero. If it passes and an independent audit recomputes the same `allow` decision, the experiment continues to the separately frozen upstream task-quality gate; executor promotion alone does not authorize formal release.

[//]: # (ob:66784778)
The immutable canary root `executor-canary-luna-20260829T122635Z` passed before any qualification cell started. It resolved `openai/gpt-5.6-luna` only through `openai`, used one model attempt and one provider attempt with zero fallback, returned the exact schema-bound value, recorded 83 input and 28 output tokens, and settled at $0.0000502. Its executor-qualification, calibration, and formal denominators are all zero.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZlNGRmNTM1MWM1NGU4NTdhOTMxMWRhNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQxMGM2OGQ3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85YWYwNmE0YTk0MmY2MTE2YWI4ZjAwOWQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhjNGY3Y2NiYmYzMWIxMDk0MWEwZjg2ZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXelu5FZ2fhVCk_yZVJW4L-ofScfLwMDEcRzHCJIY0iV5WcVpFlnmIrVsNJCHyBPmSXLOuQtvrVJL8iSDXMCDUVeRdz3Ld9b69Yr1Y12xYryty6ubq93utuJhWUVB5BVRyNMoYVngeSULrxZXeVc-3pb1mg8jPDtsmB_FN75b5kUWFiyKeVymWRKnrODcSzw3jGI_z_0yKiMviKI4LyI353kYscrjUVBWQVr5MG5ZD0V3z_vHq5tf8R_j7cjWMEPDRpxqAX_kvIEPfuR9XdUsb7jT8_t6qLvW2cDzXf_o5I_Od33XVbueDwO8s2PFB7bmuKm9j_vuTxy2O_U44GYcd8PN9fW6HjdTviq67XWx4e22btcja9dp4F7vvd3zn6ca_r6dBt7fFl078BbOYuwn_mlxteEMDzH03CJOy-RKfHLL7-khOFx-m7HKjVnIstCvYs-LWZ5WrpuVuLKuH3Frt03dcli5upHmNi3CKimKPK8CL_fcLPSYW6VxJbYjV3dbsN0wNbBhH9dZdH05XN38-69Xcvpfr-CWu37Av8TXvLzN4cj__WpqP7TdQ3v1E-xB0QNMzT_u4Ly38PaApwDDsLbgtxvWll1VXZddMVy__-6rf7395u9vv_7m2_fffvHV7Vf-V7c_-rff_fH9t6st7upz6IuNY1_n0wjXepuzoR6QynhT3bIBjnvkNN40broeN_GhbnHI4XEY-Ra-adkWb1ttZgGvDkghVzft1DSwtQJWDrRLh5I3XfEBnq4yv3LDIILH4TZH_hE3PtOR83VNm3a-uq9LDn8sv677YXRgm849kq5cBCtLWt0OyZI_wCe_c547ivNdw3C54-MO148kA-R39WkxrzKBKw9jzvZW-c8jG6fBgdtw6u12ItpxYL6SFzAnnNGl1f3OecbrF1bkl5zlXlK-2Yp-AD524L9xwx0gl_oe3-zKqUBqcHZwRE7V9fNJ0tGtnO--d34XzUvdsZ7trbPwWFBEWfxm6_zRd1jJdqNYKVcXWtGFPnT9h6rpHhzWF5t6BDkz9fgQayYmyPfcOsMgTYsq9_fW-T0fOI7k_DyBHERSvnylp56_cIeV5wchY97L5_waboQ5Vf2Rlw7_yIsJBAycCxudDRsccSY7ZN4SH-u7X3jrfNPew8DAqhcuLXZDP0zily_sB7ibgk0DaxwcoWeDWBL_CLTVPDrjQ-fgkaCohcvaDjcXlpOWqcvL8BV3s3R-__tvu37Lmpvf_97ZTXlTF87Ihg8LUFsjXyIRjXUBq931oM5wUUhKedd9WMwLa-CrvYVlVcSKskhed04DyE11OfoSYbyqXk89I_YDvpzwEuvWybtxQye2unBiXhrzKI725dVX-7yiOFnxzBO0_fTbFyg9TQLmxnn0VuvBYxt7zkZUjng6iAQABBTA5E7OQVDx-Sjr9r4r6BwvEVkc5mEVc_etluitnC_5yHuAMkhRQFtA9rAUWDCiJZR9AsmBeALk5Qzd1MPQ-PnuAsnlYeYXXrVPcnJdy2HHC8BnhSPwhTPwLUO6Hp642-e8f-l2gziNqjR6uzX9Yw544x7uEpELKAq6zh0wbT2qg0KZzgcH7ncAbcIJJeGR95fkWpWCxI2Lt1voP8DUfS2kXAXrg8XWbdFMJcf_B6KE-0MSRSDXlQunmPoeCOpx4UzthYXmReAnSbkv8f5pYg0uUIgE2PWaO-7NTOc9bwCa180Tl_3cYerx8fK1B3nA8jx6-0V-AUxQl3Cy-jVBAmiMzPzN2kelYgCMrByUCT9PFw41yGMfDKPkzdcLQHPb0fvKPAFy2O4aYH9HSABY48gbINKxh6sfpgJxTjU1zsOF9SaVV3oZj958vX-Em9SyrAcyr1vQzE29rhGHAf5Hidp2IyrD-7rhazp0PGvuXOKuMo5TL3KfXK9346zR3GxhXBSlsJzlC4j21DADH52-m0Z-mXTdNPDi3ONvvtQvQZg33Y7UEuKLQYNPRRv0FVnbMP4CxVhdCuF26WhZWoD9_vbrPUG6oKic8mgbY6dp-p3jue5fO8OF9TIw6uIsDH6D9fJtPW2X267kjfOnqVyT4CfxUNZs3Xaoa2EzFUc5y4cFEfK6a8pLpJtmRQIUsY-XvoDl5hKAoVquCEAih3E28CcI9smXL1Bnyfwwdnn-Rqt5X4EQErjxZ_MKBjINFk7XIvzkw8YREPnaMJwvnBkccRXFSfBGq_xaPCmoDV9lI2j1nbxbCY-l6J-hn8B9F1ZZZnkW5-n-zf6hp0OnaXhb7roaaOiJCz33zoV7BOXoZWBXvm7urwgeCjmhnDkooNcwEHDNuOk5go2S72A4Yth6C2z8UMN9XziYKs9TgEPe6xb3XV9vGSxPP0y3NRQbXk4NL5cFbxolOBRNbNmfun4PXRzjHy8PvdzNDrwG3c7pYVhBH8r0f9LNcu6tS5Y542kWBf5r5_9-auWJEEpcOT_SNebd1OLdCSlWsbqZSPL2qCVGUMdor19CBrkbpn7ivXZ5grTQNJGgd5BLGpppvUD_Dw7SL-BbNnQtUkaDmgG-urS8lJdxlPF939RXhFDIl7QBUfAUu514_JJ_Lgy9qMizF88I1to3SKQkVPD4EGtqjHTvg0Y0bDnp0yDTpC0PrbWfFsrlewXnix7Q2wIFFk1J3yhfLL8NysorvDwo06QKKuZlXpTDX7gR0Ft0utIr7UivtAO8VXwgZiMne08zoYdV_QsdrD-hOxvskUdjBNPFbQxCzvMXer-HrhpvK7gN3gNWlE72IfduAp8VzE1dnnC_iKMgqyLP890gqbLIjVgZJEXAk8xlWZJHrlf4zHVjBpghCj2ehOh5QrOOnOXitm6C8BMcNLqkfdePl2669NMffPcm8G684G9c98ZF5ClPnJwzuc-ipARCmT_99X_Vv07kKvzfQJEbeB4VhMcLPw8qVBM0huESl5T8Jr5sOWPqFnlQwE0Cz6gZDfe2mvGl_mm9LxdoBs7FL5iaxXBZy1le43MOaWX91Dp3AmQsd30ULrWZtUQqcVOgETf23Dtp5xhbufe0jLxxPP_a82e95aDeGpyetQsnwm_EsuAL0rr0vrp4QlDNo-NfxyAW4S6cB8Cezp-QueBj_cJCyJUNyvhhakbngQ1aE6CzQKDrFaAwvMgeN-HIkMkCLISimZCGcbpeDgHimj0CKHKIRRCj4_CwMdhVh2YnWISn3ITykooq9NLMD3jsa1Iw_PXykl7jcEeHJd1WgItDXtLuZ5Czf89aBPwC84EABtONg4057A-Gp7bmLXCqIXcFrP8jXwNkBETLi8eiQY_zyNeALfDAxHfwwnxuaM6iJaa-6neTOE25RNPqGeBrPqzUV6ijcTtwCt1D62wAMw_jcs12SBnSglrj2MQuwnpWRyUc8nh42uZGCxUfk3iclxduKazcvKgqFpRc35IRrZgZ9pnRBzlsHgUcBDvzA7_SkmcOSCjn2CsCDMYNGz6lfRtk4ZQdXHjPgdkLQp7kGkFqgfFAqalBiXZKNjI4vG4r0C0zxOJSmZELIqcl3N9utikd9Avgc-hVxBuvtyTwHWARlDr4ilgYLPBhUyMtIefhqwZ6BcMG2Bij4uTCG7uuIfQ04N8fONIYAVzCUAWYon97_lpjN_E8UICxH5ea-ea4i5aQbxBHkTMmWZWkwNyc-1rXGKEVOeNrQiXC5DNuTV_Y6j9aHHi-Lxx8VMEPYxYa4umJ0ElFUpfN_oNz904udQRvI0ok6T6GzZIgeQesSkte4lqXRFyCBlcnvPDyJF3XT8qoyjIvLdRJGrEg4-5eGttx_mU3oJW7JVlBZKicokIlI1WCEEK0mjfSnCcniCHDZoeIeKfFSAOYaugOGM0IypJXIELHZ6oNnlVxVbCyqKJM7d4IOM0C6UUhIzlJkPPYK6sgF3EFQaxzFMk44jeKA8l5vdhnnhcgEPfVvEZoSM77muDOITEDa_g4HN3owOlmTIYAGNFpfgI5ip5DghMwazE1UowCleymUXAg-QqY6dUTTjIUmvAcgKYclOmCvGKk_2BNXb9k7QDIRVH_f7TBClTKCNpUCUit0NZNl-OWF0IO79tGal-Eoa57xC_XiNBgqU6DF0DufDyhrpjo3nZgblwPXKA-9QgsIFyBGUhsKg9wSXBJExI8t6UrR5OZuH3KMbdoQTAVNYxwsIJ540xtPZrhFxWQYcOyq1BOcfTL79AKIvm9ECJ2L9qERwU4DGwdGEquU5w4WM-83o3y0mHp0cr5QpEiKJm-B4jU7Qe1yiMCgkveznEu2t07oUwE0ENQ0fOHHqARjQH6ygh-OaSZed07OVi5cBx4hDGsowH9XFeP2sRXZKA1nHgLFOJAW1Svw9nsrxmUNZwa_muP9Ix_wJhdXSDUHYZpuxPfA8F_cIZ63bKGqC2XoIDBB49DjctMAP3NHiw4igI2CafwC5cMpKUfGQTyohYOSXtxucN8p-rOhNG3cBT1qQnw_gmLI1Gja_IeyWnlvN_mIJY7BIVTK-dAQKFie1xwy1bF_NSBVl1DEFgL-gGORPIfIj3YYAq8BKaK6abbjwcI8N8i9sGlGQAT0dUw4GOARhWE2dZwp3CGdQtcT-uFb7rm4G4csIQ2Xdk13Rq2XNQ9ftHP50BAWR7THMEUh8PUYTgCzOMjObpRYDfZKfEnpY4QYFopg_mz2wA8ekStDGctVJW-o2Iaxq6ExTWcYbagMIhYL2-Izy4c8mbA3J67clTUFelDoAC8AJpA3Ai-e6DohRwFixL067LlE3zamDCB7C6B3BBgsZKOGF2WlPAGwPACICizilVhlEcJOdxIaxiR-lklvjDSrjQv8zmM6flpNSvFOfgup3lN8PyQu0HwwA1Jr6RipIXBSc43Xw6aASXSAiZcYQDkQCpIt76WDGJpKNQq5UpTs5GpjvmlOVzuwFFJo2X8_SxJxOOHokTZwzIGX0rqQHusXaqLFJBfv2KKRSkKtaIzOYUm3A-gXABJkQ8AJuBRWBCcF_B-Tj-QV_Wa9AHUZ4eSDoi6HZh0n5Bva0T37bDBky6AteAdwn-IQvg1SqDxcSmUGyV8Luh4cTmIZWhMtl73YDArAVALk3k7ofoh1IPCC75Gn4gkEKCl97OYNGWT3KYjPGEzfwNPS4mmzx4nmcWXMDpBDUiXCEhbFKAiI0CAH8R_bJ6WZCfSyMFU71AI1Fv13EIzB2wGE6GbbiBJMtTlJIdBqgL1WHBFUei0ERhainwpns7TQxXnoZ-kqRfFGlcaWR6zhHh1eoay7_MkZVHO0rzUExoZGzpe9_JUC3OdVc_5L_wzwgc9I9pEoYHOJd7rhHJpV4sTXUg_mPoXrGrnNPUWif-BjcWm7MRMW42-hBhqu2UF9Jmz4gMFRci9RM6l49g2-dZQWhAAo1sVwUigkb7-eOFWEz_Mg9zjbsKi-ZB1msmczvzi_BAFpit8qP5FQi4RDZSjafqv6kYEvIE-pbD7ZbZ4Ba6Xyn1EhQuiNnIA_cZ6OeXe6egILInGFtVjT96slmLGJGwIMMsIFnI9Bh8RXCIYPfxe55rgANMIk-K1VDjyjO_Im4QOFbSex6kE-T92O7mGX3jfqcvR_tcL91PGVRAB37GCaze0kVYj7-c1-TA1fYnkj7sv64oSD8aZX6VGGuB6ySol-SH5Su5EMM-s_2DrrfZXay8IKwCgD5fzP7URG7M0Rdr0tYVuZOdcFjYvSKuR0zIvyP00jdxgRkFGpo2c9jUpMiCll2gXSU-coOxraYpdS5Nb2i9CRxqYBEWJUmrKfDJwvhxT6YWl1lUAEECSLCQmnx9AzaC-I_ZcSj6UWHZB8YQtMzyIi5nN9z4lrGtYDYh2zl-vyyO_KlJe8UC7n4wMofNS59mpPZfOVT5zLLjeCfbUavngOOTXVByyd-7qLhQQA6qngJDE9EB7ckq0mAW2AaElFe_2CEG9m6VbBi-dv7V3QhS2zh1NdQfjF6KkiXgUDU1ZwzTbzAaWMYEGQWm9gpXztRR4QnQVp5NiZuPmSLY9zxEHyjzLvMIr-OxCNjKvNB28PGUKvf_KEIJdiSPfTGCrSDTNZaS8qj-OlMOA4g4-YDmYSIeeIYy3kgyc0S4Fd9huPmB4piMcqDKHyFdFCyH3lCRX6VrBZV2Q_gFPUh5GcVTqEIeR6TWLwZckaykEkAcu8yOgTxaoOYz8LTnHa1KwTOrB-KI2tAcVLKmBIiUwOPCca_gAN9JT1EwavoKwSUoawGMt0n8WxIrzES-0x1mYFqu9A1NhkxJEjOBO5asap5bvO5pBRwKU1PJRAzbaxxLuDwZC4SyA297a0HHUCAmk8YSE9vvXdQmEZ1ke50nAWeKqyzLS2OaY14sz0SRNEkIGsh9rGqhf81EDCwzZiLs-FwrFUkp8CrU8_U0pXmoV5M9y9qLVc2SBUzBK-kElq1Q1suBaWFAtB0aTtovGJPr9lmCb2pIIU6I3hBJlumlAzxzsc9pS4hmaypu6LNHlNTuJlFwkb5V6S_sRZeyeXG8SA85-AJApHbwuHUoagbFBHti9r-5ahIwv3LSbp77nRSULtfVjpALOrP8ZaX1yaBAgkZuHSeV7ubbk5kw_XTny8qw9w66U8UmKfkp1ek81uGhWET-IuD-QinSYmaaMIUXAmgWl1w_oPBPpd-RjRWDUzhch0xyE_lWrplD4ik6KzLQdgJZ9_41hnOovL8JT7kdJyDxWaJlppCNqvfXy1EJ1blJ7VL0SXP-Mgq08HlY6-ydpI6GcReclMOz1WCMSwk-1NKVrJVH1gJAKr06YpsPpoLAR-RtEdII8WsLrip-YOBtF-CDs3hrZSuhIdKMKDw58BxrzWsNTdXlCSg-s4iPaTHTrMk0EAzlkiOnTk6h6qS55IQlzOd-gGO8ojWVJOsgAKIN20DWPKPhESg9ix0Zdg9YrSCxdBdoP5SIR9Xeg__7Ou8TJuVf5wHKcMW3CGemhZr7SZyR66pB45udl5XmC8gQlzrmfqqLvFVmcOuwqhC2cRoORmH5qMeRRYUAflQZqs7o1AncqWUFk3QBRrwlsq0ATpZm0MxKg1BxQ-j0XGEE5bmDyB_HJN19qU1QRAbm8AW6NSyGexcyc9c3jEpGrjHeJ_Bk62qN8I5VHoQjtQhpLkIUZZ1FWZto4NPJY98TmyzJSZ5eS8Addizi7RhliIEONKv8Q-cD38jrmXA7gyBFVLB2F9hPKGnfi3pUjFi2s59mIEYEZIbQHhXXwD2llHCR1Ec32PUY-QW6LRKU5JUEKhQLT71pEFSgh2INOaRI7lsNInSyE36A8CbASVALOH2qwpwaG4OQXMmPauhIrE-Yqyi3xb-X5xV2h-BgOgeG8KZXaprNVKXkPDm6NEWWDIy7lFQRR6ftVzKtYozMjldjIK3hWbrByShRhECU8rbxCG0lGuvAc0H9x_q-6hCUmI0pv5iCi-t9zcmM4XwJO5T0lkwosre_xIBlEmUGUTSsiU_AsGrWk9skZhl4RSjZTQfqp1bJIaxqcZTJzSA48tiK8_rXwPO2BQXpYZFENM8eJ9LlCqRn4eOyKrhGhblzBSJlKB6YKGdJ1dcLyERsg80eEqdUYEuAJUSs9sHoccwIJ94HVRhFBfj-BTt7TTAtiUEG2KDaHY8sG8Khkf9zWt51yhMF5SRkqaF9gxEcjofAoHPjTJyS7E90-OKxL9_r4AqTQx6ufqHMIpZQefn7QG8T4XPpV5Bff18WG9aXzAwOC_4vsHEKOhJc2DsmCPM_yMj6T8j-I7OX__s__cuZ08WfXHJx7-1I1rJtFrPTfbD1oQYLcWXfABRjYIuyA9rM094FT7wqkjetKxpS5z5f3_h2AyUMZC9RTNKzenj3Bg1XI0oP3pOVLmguWwg82c277pwf7XpL1vHxg5LbYEAuCRQi03ArIOg2SG8kjZrD89bF3bBCbUwf-69XD5lFPJswYIxCCThD0He4nlGuhC2CmedSW8kGeqrEOckYcOfHQTtZxlBVWHTy7CiTN0zxPvJBHKY_zKgL15IWAE_TpmeUdZmmDWfLxq2WT17PJ88tzDstT_E-ni0-eqsR5k3KbEPMigyLkQRL4fsmqwMUYUBHnReGHiZ95SeX7WR4yFhcpy1KwqjwfrJ6kCJOEEsBP7edUtU1w4_onqm1KXvGsSpittrHVNrbaxlbb2GobW21jq21stY2ttrHVNrbaxlbb2GobW21jq21stY2ttrHVNrbaxlbb2GobW21jq21stY2ttrHVNrbaxlbb2GobW21jq21stY2ttrHVNrbaxlbb2GobW21jq21stY2ttrHVNrbaxlbbXAgHhpGfZlXlB2WmdZaR9n6Kkj8jcV1FmBIWhnngRZxrJ5-Ry25kyLw0G73_MCJKxTxVWSggYKWIQo1mru4dipg7gcF4jw5SjWQl4lfVFENnZt5qq2jGEKhcELygGEFRKAiNSiGIPWcz3XRl7RPXht1zYfPykjK84AhM2jmslkCGUXCXf4TbHJxHTvE1Qbp7cEfKU_TXHEmz51Vc_SOA_vffOOcKrw6_Pqi_Ov7almEZ9SVpVcVVEhUXfulr2lGoYY_Zss_6vbdzI1z6RZgk8dPw4i-Qffa6kLtFct1QfxQWkSbofY4AFEH255z_fuknqnyvDILYffOlkhUvkn35CbalRd6pHSz1l8-rHjMu_mz1GEaIRfnYz4ehDxS_KvtEpdLLooSD6izENqtzd3up1kzgdInb5cUdn8CC0szRAbTDuD4FYqVjhyBWz6Uvt8ZIfj_tZmsNZdLSEFaG5-3cBT-93uNbE6s8gBcFaylvh1w79I7IZkKtvNC4RSYn7Kf5AKZqmuVhcZ3pijUF8OrJCrunT_jMviY4R52TP29QRzIXxpqWBxvVtHOUX3e0sVn9HOzrMyr0ojQo0pTx0geRy8q0YAA5hKP7ZIWeLod6ukLPStD_DxL0-RWfR7979el0nd2fpbAw8BIeeUkZl25WBhEPqsTnZZn6ecFd1w-TMmSwh6SsKkAgEQ-jiGV5FuUwdlgW_pn97BcWZj-42U3k30TxicLComBJzCNbWGgLC21hoS0stIWFtrDQFhbawkJbWGgLC21hoS0stIWFtrDQFhbawkJbWGgLC21hoS0stIWFtrDQFhbawkJbWGgLC21hoS0stIWFtrDQFhbawkJbWGgLC21hoS0stIWFtrDQFhbawkJbWGgLC21hoS0stIWFtrCwuxQa4C5LfR6ELtf6zqjYOOeD_Yx6C5XF66VFULph4kbay2GUYBh08NICClWn0-24OD88N3mBGFfRiaB7dVCOqoecgx1euCTVPjtB0bnOnCBdRJm78iMAwIjPnQ2CkmEawDgSuQlo6OuIHt6nWBApV7EE-aZpFSgqZPJxjd9Fys5-8ISRiybyBXanR4JF4PoLNw2M1FeCBhTo2NS9nA4ZRBd5YQxl6lFcwHQNSMpup8LgRjRNYBEYcC2sqjk3TS6E8sTxJjYMUGQD7Fci8qIcsKJhPdf4Tzgb6Fm07MUcpKCwoBPkIzkWj2tNJMxUTmLpOjiu7prT3PVPqx1GYN7JMAjFSMD-Mdn_sCDtAsukWRplKfOyJNESzajQMSn5hfU1-CUIN1UbgPUjUXCnMpgxuxspT2Zyj47vAV16izj0F57nU5xGIDGV5g0aXySegY6SGktUDgi6awVZtJTD2pGPS2Sw3RWsqjgKFH6HKCGf6qYkXisYgDDpgu1VQrcZExdQAriTUV0AutGbmqvCAknTw44ha-JRaRBASdxLAQV0aO5ahSioKtCUwvJMousITrNRrglhJxP1XitoYGhXQR3afYen9FfuynXdGM7QmTGzSTCUtquciLNYeX9YnAhUh0fnBZRUuxTcdcKFZiTKipjdseuKfGrax0Lhvz3gpL0o5LwkV83s9iIPnU6l5Cr38HRSpfJaA9QyvYpShUytXAKY9XVzBrztnc8-mZNuIgjl_Og_pybzDYri7c-Qvk39e-XlLE7Yfunh1weZ4vvXLT09BA6eKOJ8_kDPrepMWZ7mVc5-g_X-cLZ62dDkiBvi69jwepPAvVDc6UVh4Ec8_s1WLDJ_5jArOki0CD5MsdBJHRdWzF0vDZiX_kYrHpSHTIjeB20NfNtdFDfPq-s3CPrSr8IagveJLcmM8NU5Mnzi52KlS_cI7RoxpWNb8TDUBYBvZM2wOkdYT6xhPEUnKnolfHhzBEBoOelSWZ0jjDNnizdJFtq4d9HCVucy-ELquQQZJe_688r1Z16UW1LukdP3KPojHG1w9hWB8CwZ1UsYS8KlL2npKkPos8rtizx3_aoCvFGWVRn4pRf4zKNo38lye10k_HS5vRXYVmD_5Qrs57elOCy7Dz-drqr_8_w-MU954AdVUQRRyaPUrfzC42Ecc55laQKmoY9Fk2XMQu57YVl6UZylBWdg2JU5BWRP7eewjYDn33jJjZucaCPgh6kbV3DFto2AbSNg2wjYNgK2jYBtI2DbCNg2AraNgG0jYNsI2DYCto2AbSNg2wjYNgK2jYBtI2DbCNg2AraNgG0jYNsI2DYCto2AbSNg2wjYNgK2jYBtI2DbCNg2AraNgG0jYNsI2DYCto2AbSNg2wjYNgK2jYBtI2DbCNg2AraNgG0jYNsI2DYCto2AbSNg2wjYNgJ_6W0EZkb0q9yPorJMgSbn2gBdRWmkM71Z8aNyroEMSGKvzLmvkZNRD3lRBDyvjHG2AI-zOO5qBe5Yfd2gQyZYucuqgbUtK8Q3-2AdKKOb1uizv69HpqPkM_0_EYm_kARAPl6Z-sgxwKhZSXLRnksJqWvq543paqWTeQJCesmEAj6rRRDj5HVWo3CyKNgwezPuiPFvyUy9m72GihnUj4IfDSwkEQpJWVelkIEfeapaQnjMvHjhRe7CD6I9KxzwQeqtkiwybFLesN1At4qKH61mBA1a_8ssqJ5TxTs854ULN04WfgiDhbGU46LWY-ZiJENOEQUpULfdvcwrVFaDqP0qNoCjL_k7GPfzBOg4TyqdAGbUye5R8svKW02cM4coBD56MlMDJ9ZOefMX7UEqh9dPzLKgYjdx3fver4Xjwjf1nmNrqfCjhBi4RHyqEiR_uDZJLfvZegfqXXgzZ7ijvC53yrlyI2JDd7Nn4rhgX7-0N_jtPASoj1swA251ldad1OtGvb9zN2yYH8U3PInyilWu7_MirsIgq0DrRXlQ-VGYeK6b5YnvZm4RRKnv-26ReDkAd99Lq4yVkR8CP5GbUIgIucODOZhfZhG86ebwcu5Xae5nqRtGVR6Wmc_iNC29lEUp_M-N4tKNyzLKWVJmCcwaFfHdBXoF6e5VVQZYa_a-GFXSZk3LC4ubdckXie4lhYBE6sviyHNAGlTEQpeY3TgNSyOYcWi7EdMr76aw-lQuVz1oX4Uw643SGnONe0tYPEd_viOyAjiiccpSEIYBQA70_Irc3TLlnhytNdocALHOATKqjiOvOZxCj-47giS4cLOmbk7AAtuimkQRpj4dnVtlJK83qra0PFeXNGeNCCcyMDJIXrTvUCodmRHiiClcSs-jMww1Mh3TIKS_1hhHxbgieCPCxjpbynCWE6ASlsXYoc9yoqyRns9i84VtkYozbZGKM22RinNtkXrRFmn8v9oVibf3dd-1uIpbFOTDb9Ec6c06QYBaIZF7oYdDnhR-EnNvby4R4DtF_JpGcSKg5if6ejx_IJMtCOZebu_h-zFoiPi3WDZK5xYGPCzYnUcDcXjXgRoEfLvejctoFS8bgKh3Tn_hoMPCc2MvjH-DFb8Xsowsa5UILEUfpUIKx5JMYhBSU1ugF1Ycx0kaJkn6G53xLLfkWg_8DeJTOtnZ1eD5_vP6MR13KTKYQbYN-qLre-GuH4-wEtmzsmBuH0eQ6ByLzWlAtDrHXU91hTrggeHJc16dY4jTM0n58Uc4TgE39wKBaDtj_N0EsYMOsEtVrhKQMTy8Okfcp2f_kldk_GjFS8QqL17UMeomSDOGV3VMq3N0-YwGVILUdxIy0PbltLOdqH1ys445wCxn-kN9Z1waqGzl-ZGigyY7I7BnB-XMB0RzxAWyU4I-CV0gqbpRzWdoeqTkxqSLtGFTCxaWjLkgnNhfAgK-z-svlQE0j1nIstCvYs-LWZ4CQM_Kc_2ldPeYp_tLWZ1ndZ7VeZ-h857f-u2oBdRiZpIb79Ppdk9_lv5WhRd4YCzEMGcaBT4Y5WCOu1EVRcwtI9cLkjLkSZmmSVwWvpukeZIwP06DJC1c0Wrpyc2daHblJzdBdKLZVei5RZyWiW12ZZtd2WZXttmVbXZlm13ZZle22ZVtdmWbXdlmV7bZlW12ZZtd2WZXttmVbXZlm13ZZle22ZVtdmWbXdlmV7bZlW12ZZtd2WZXttmVbXZlm13ZZle22ZVtdmWbXdlmV7bZlW12ZZtd2WZXttmVbXZlm13ZZle22ZVtdmWbXdlmV7bZlW12ZZtd2WZXttmVbXZlm13ZZle22ZWuEeBVyHjgB25om13ZZldv3ezKtrqyra5sq6vzra7MJDCe87zweeVr2jaaRhgRhJf3enga2VRg-MdRVfA01H5IoweEwWEvbd2AyF7mlylkoiG6fOVucYRSlMbQhsTsWVdUN-dOzhV7dYuA4D3qwR1o4nV3Io_TNFUWprdmSYvcJyJRYhi7S0rxLNhu4QT4L3EnpGXg1IFLWqyRElmGoIcWoasfEh74OS1U4j0FABc6girDdyJatJ-TJfy6QgREy65axoZiRlNg2GBiDBNnIcuCyYLQLlENdkR7GoV4OGWdE3fMlK_4RPqztKwhvnkUAVYKH5lmNU1H45IjQoFH7VMQslWnILFHnVNlzLCQ2Ae9EWT0zu6WhVGOfjJB9cD-29YD9VAyMzcu4V5YYkdJCPWFAJjM7VB-kEu6K3V9UIl-FLjabWD0KlEpOK9oMXIcfkJUtRdPWuwj__nUEMXK_BlM7ZwPUQhLIfCXCqgL-qasWOFQpwXiXYrE3uOePzK1R7-i3XtEfbr_0GC2HzLaM13S1LOOpuDtORU557FJwQ6IlQxMXFIt68MHlWx3Godtd9NoypfDlLyFvBHVsIM4tW6xiEV2PTBcF8qoPolG0HZ4NwvWmblZg5eqVa4m3-enFyUs9cuw5JGXaE-s0YLGEPEv7RwTB9G_aXeV4U48RxYY46W2CjJn8bTm2FMZs6agquQjQqd7xE81-6svjCxGzQdgWU19u9e8S1K8cITJ6kxtEKaBiJzSLH6qJPapiCxQmfAtuZHrCx_waYffM8Edylr0GZz0jfz0Cf77H-uTWUY)
