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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZlNGRmNTM1MWM1NGU4NTdhOTMxMWRhNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImNjYTc2ZTVhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81ODNjODhhZWQyNGU4YWQ4Y2E4OWY1ZGYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhjNGY3Y2NiYmYzMWIxMDk0MWEwZjg2ZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXetu3MhyfhVCJ_mzmZF4v8g_Ep9d-8DAZo_js1kEOGchNZvNGa455CwvkmXDQB4iT5gnSVX1hT0jiZIlJUEQAgusNEN2V1dVV311s76csG6oSsaHi6o4OT_Z7y9KERZlFEQej0KRRgnLAs8rWHiyOsnb4uaiqDaiH-DZfsv8KD6PeJBFrs9dL-ex64dZ4keZm4XcLVmZpp4fsSgMBRcszWJeJmUQhVHCwzzy_DzmOaxbVD1vr0R3c3L-BX8ZLga2gR1qNuBWK_ghFzV88IvoqrJieS2cTlxVfdU2zhaeb7sbJ79x3ndtW-470ffwzp7xj2wj8FAHH3ftbwKOO3a44HYY9v352dmmGrZjfsrb3RnfimZXNZuBNZs0cM8O3u7E72MFP1-MvegueNv0ogFeDN0ovq5OtoIhEzlnSSwidiI_uRBX9BAwV1xEacDTlInCB-ayIuXAlTIqSqSs7QY82kVdNQIo1xKpL1IelgnneV4GXu4Bbz3mlmlcyuMo6i442_djDQf2kU7edkV_cv7XLydq-y8nIOW26_En-bUoLnJg-V9PxuZj0143J7_CGbQ-wNbi0x74vYO3e-QCLMMaLi62rCnasjwrWt6fvX7_5t8u3v3x4u27n17_9P2bizf-m4tf_Iv3P77-6XRXnKy-Sb_YMHRVPg4g1ouc9VWPWibq8oL1wO5B0HrjsG07PMTHqsEl-5t-EDv4pmE7lLY-zApe7VFDTs6bsa7haBwoB90lpuR1yz_C02Xml24YRPA4SHMQn_Dgkx45bys6tPPmqioE_LB-W3X94MAxnSsfXlJEsKIg6vaoluIaPvmD89hVnPc1Q3KHmz3SjyoD6nfydTVRmYDIw1iwAyr_MrBh7B2QhlPtdiPpjgP7FXDX-h54NEfdH5xHvD5DkV8IlntJ8WIU_Qz32IH_hq1wQF2qK3yzLUaO2uDsgUVO2XYTJ4l1p877D84foonUPevYAZ3cYwGPsvjF6PzFd1jB9oOkVGiBliTQ67b7WNbttcM6vq0GsDNjhw-xemRSfe-jMwzSlJe5f0DnB9ELXMn5fQQ7iKo8L9K7np-RYen5QciY9_Q934JEmFNWn0ThiE-Cj2BggC9scLasdyRP9nh5C3ysaz-LxnnXXMHCcFVnhBa7oR8m8dMJ-xlkw9nYs9rBFTrWS5LEJ9Ct-sYZrlsHWYKmFoS1689nyEmL1BVF-AzZrJ3vvvup7XasPv_uO2c_5nXFnYH1H1fgtgaxRiUaKg7U7jtwZ0gUqlLeth9XE2E1fHVAGHgOxguePI9PPdhNLRwjRFivrDZjx-j6wb0cUYhV4-TtsCWOnc5wzEvB_8XRob16c3hX9E3Wd-YB3X747RlNT5OAuXEevRQ9yLahE2xA54jcQSQAIIDDJXdyAYZKTKysmquWEx_nlCwO87CMhftSJHqnzg9iEB1AGdQo0C1QeyAFCEa0hLZPIjkwT4C8nL4dO1gaP9_PqFweZj73ykOVU3St-73ggM-4I_GF04sdQ73uH5DtY96fk24Qp1GZRi9H059zwBtXIEtELuAoSJx7uLTVoBmFNl30Dsi3B28iCCUhy7s5u1amYHFj_nKE_jNs3VXSypVAHxBbNbweC4H_B6UE-aGKIpBri5XDx64DhbpZOWMzQ2jOAz9JikOL9y8jq5FAaRLg1BvhuOeTnneiBmhe1Q8I-7HLVMPNvNiDPGB5Hr08kd_DJagK4Kx5TaoABiPT_WbNjXYxAEZOHbQJv48zTA3y2OdCJC9OLwDNXUvv6_AE1GG3r-H6O9ICAI2DqEFJhw5E348ccU451s71DL1J6RVeJqIXp_dHkKSxZR2oedWAZ66rTYU4DPA_WtSmHdAZXlW12BDTkdfCmbtdRRynXuQ-SK937mww3GxgXTSlQM76CUp71zK9GJyuHQcxr7puGnhx7okXJ_UHMOZ1uye3hPiiN-BT6wZ9RdE2rL9CM1YV0rjNsZalPIril6f3DtUFR-UUt44xtEanXzme6_6908_QyyCoi7Mw-G-gV-yqcbfetYWond_GYkOGn8xDUbFN06KvhcOUAu2s6FekyJu2LuZUN814AhpxiJe-B3JzBcDQLZcEIPGGCdaLBxT2wZdntLNgfhi7In8hal6XYIQkbvzdFkFPocHKaRuEn6LfOhIin1mB8wzPgMVlFCfBC1H5Vj4ptQ1fZQN49b2SrYLHyvRP0E_ivhkqiyzP4jw9lOyfOmI6bSOaYt9WoEMPCPS-d2bkCM7RyyCufN7ebwgeSjuhkzlooDewENyaYdsJBBuF2MNydGGrHVzj6wrkPcOYMs9TgEPe84h731U7BuSZh0laPd-KYqxFseairrXh0DqxY7-13QG6uI1_vDz0cjc7yhq0e6eDZaV-6ND_wTTLfW_NReZMpFkU-M_d_8PYKI4QSjx1fiEx5u3YoOykFStZVY9keTv0EgO4Y4zX55BB7oapn3jPJU-qFoYmCvT2iqS-HjcrzP_gIt0KvmV926Bm1OgZ4Ks58lJRxFEmDnNTbwihUC5pC6bgoet2x-Nz-bkw9CKeZ0_eEaK1d6ikZFSQfYg1DUa68sEjWrGcymlQaNIUx9Haryud8j0B_mIG9IKjwaIt6RudixUXQVF63MuDIk3KoGRe5kU5_IQHAb9F3FVZaUdlpR24W_wjXTZKsne0E2ZY9W-YYP0V09kQj9xYK9gpbmsRSp4_Mfvdt-VwUYI0RAdYUSXZ-9w7D3zGmZu6IhE-j6MgKyPP890gKbPIjVgRJDwQSeayLMkj1-M-c92YAWaIQk8kIWaeMKyjZLmU1nkQfgVGY0rad_147aZrP_3Zd88D79wL_sF1z11EnorjlJzJfRYlBSjK9OmX_9X8OqmrzH-DRm7heXQQnuB-HpToJmgNKyWuNPlFctlqx9TlecBBknBn9I5Welvv-NT8tDmXCzoDfPE507tYKWu1y3NyziFR1o2NcylBxnrfReHahFlr1BI3BR1xY8-9VHGOdZQrz9jIc8fzzzx_8lsO-q3e6VizciL8RpIFX5DXpfe14AlB1TeOfxaDWQRZONeAPZ3f8HLBx-aFlbQrW7Tx_VgPzjXrjSfAZIFE16eAwlCQHR7CUSWTFUQIvB5Rh3G7Ti0B5prdAChy6IogRsfl4WBwqhbDTogI70oTKiHxMvTSzA9E7BtVsPL1SkjPSbhjwpKkFSBxeJdM-hns7B9Zg4BfYj4wwBC6CYgx-8PFkGsb0cBNteyuhPU_ig1ARkC0gt_wGjPOg9gAtkCGye_ghYlvGM5iJKa_6vaj5KYi0Y56evha9Kf6K_TReBzgQnvdOFvAzP2w3rA9aoaKoDa4Nl0XGT1rVsmEPDLPxNwYoeJjCo-LYkZKYenmvCxZUAgjJataMV3YR1Yf1LJ5FAgw7MwP_NJYnqkgoZNjzygwWBK2ckqHMcjKKVoQeCfgsnNCnpQaQW2B9cCp6UVJdwo2MGBeu5Polllmca3DyBWp0xrkt59iSgfzAvgcZhVR4tWODL4DVwStDr4iCQMCr7cV6hLePHzVQq8Q2MA1xqo4pfCGtq0JPfX480eBOkYAlzAUh1D0H-8Xa-wmngcOMPbjwly-qe5iLOQL1FHUjklWJilcbiF842us0ora8TmlEhnyWVIzAjv9W4MLT_LCxQdd_LB2oSUe3giTVGR12ZQ_uE_ulFJH8DagRVLpYzgsGZJXcFWJ5DXSuiblkjp4ekcWXnHSdf2kiMos81KuOWnVgizZPbW24_zrvscod0e2gtRQJ0WlS0atBCOEaDWvVThPSRDLhk0JEflOg5UGCNUwHTDYFZS1KMGEDo90GyIr45KzgpdRpk9vFZwmg_SkkpHaJMhF7BVlkMu6glTWqYpksfiF6kBqXy_2mecFCMR9va9VGlL7Pqe4c6zMcDV8XI4k2guSjH0hAEa05j6BHcXMIcEJ2JWPtTKjoCX7cZA3kHIFzM7qySQZGk14DkBTDs50RVkx8n9AU9utWdMDctHa_7cmOAWXMoA31QbSOLRN3eZ45JW0w4exkT4XYaizDvHLGSI0INWpUQCUzkcOtXwkue0h3DjrhUR9-hEgIDyFMJCuqWLgmuCSUSR4bkcix5CZbvuYY2_RimAqehiZYIXwxhmbarDLL7ogw_p1W6KdEpiX32MURPZ7JU3sQbUJWQU4DGIdWErRKTkO0bOo9oMSOpAenTrfa1UEJ9N1AJHaw6JWcUuBQMi7qc5Fp3slnYkEeggqOnHdATSiNcBfWcUvhzyzqDonhygX2IEsjIGOGvxzVd6YEF-rgfFw8i1wiD0dUb8OvDmkGZw1cA1_O1A96xdYs604Qt2-H3d7-T0o_EenrzYNq0nbcgUKGHxw01dIZgLob8pgASs4HBK48FmoC2SsHwUESlArh6y9FG4_yVTLTAZ9K0drn94A5U9YHJUaU5NXqE6nzutdDma5RVA4NmoPBBS6tifkbdnpmp9maNnWBIGNoe-BJer-IdKDA6ZwlyBUsdN0h_UACf4bxD5ImgUwEV31PT4GaFRDmF0FMgUeVg3ceqIXvmnrI9k4EAlt26Kt2w0cmVcdftFNfCCgrNg0VTAlc5hmhiPBPD6SYxoFTpPdZf6U1ZEGzDhlCH_2W4BHN-iVgdfSVRkZ8bEf2gKIqwXDbkEZELFOSUhMKRzKZsDennvq6Kor6odEASgA2kBKBN89cvTSjkJECf513YgRPq1tmEBxl0RuCLBYQSzGlCU1vAEwnAEERVayMozyKKGEG3kNq1I_ucQnVtq152W-gDU9Py0npzgV39U2zymeH99uMDwgIZWV1BdpZd0k590PvbmACmnBJTzFAsiRVVBpfWMZJGlo1EqdStO7UaiO_aU5CLcX6KQxMv4wWRL5-LEp0fGwqsEXSjswHmvWWpAS8ptXbLOoTKFxdPZNoQ0PCygzICnyAcAEIgo5wXkJ76f2AyWq57QPoD87tnSg1E3PVPqEclsDpm_7LXKaw9WCdwj_IQoRZ2iBhpu1dG7U8Lki9iI5iGVoTbbZdBAwawNQyZB5N6L7IdSDxgu-xpyIUhDQpdeTmbRtkzqmIzNh0_2GO60smuE9bjKZLxl0ghtQKRGwtmhAZUeABD-I_9i0LdlO1JGjrV6hEah2-rmVuRxwGGyErtueLElfFaNaBrUK3CMXWqMwaSMxtDL5yjzdrw9lnId-kqZeFBtcaXV5TBbi2e0ZOr7Pk5RFOUvzwmxodWyYet3TWy1sOstOiM_iG8oHHSPdRKOBySXRmYZyFVdLjq5UHkz_BlTtnbraofJfs4Fvi1butDPoS5qhpl2XoJ854x-pKELpJUou3a5tU24NrQUBMJKqLEaCjnTVpxmpJn6YB7kn3IRFE5NNm8nUzvzk_hANpkt8qPqsIJesBqrVjP6XVS0L3qCfyth9niJeieuVcx_Q4YKpjRxAv7EhpzjgjqnAkmls0D12lM1qqGZMxoYAs6pg4a3H4iOCSwSjx9-bXhNcYBxgUxRLiStP-I6ySZhQweh5GAuw_0O7VzR8Fl2rhWPyrzPyKWKcdvATxoVJQ1ttNUo-z-mHqehLVH88fVGV1HgwTPdVeaQexEtRKdkPda_USeTlmfwfHL0x-WqTBWEcAHo_3_9pgtiYpSnqpm8idKs7Z97YPKGtRm3LvCD30zRygwkFWZ02atvntMiAlV5jXKQycVKzz1QodqZCbhW_SB9pYRI0Jdqp6fDJwvlqTe0X1sZXAUAAS7JSmHx6AD2D_o6u51rdQ4VlV1RP2DErg7iarvnBp4R1ragB0c794nVF5Jc8FaUITPrJ6hC63-o8urVnjq_qmduG65W8nsYtH7FDfU3DIQd817LQQAy0ngpCCtOD7qktMWKW2AaMlnK8u1sI6tVk3TJ46X6pvZKmsHEuaatLWJ_LkSa6oxhoqhmmKWa2sIwNNAhKGwpOnbfK4EnTxe9uipmCm1u27XGJOHDmWeZxj4sphWx1Xhk9eHrLFGb_dSAEp5Is344Qqyg0LVSlvKw-DdTDgOYOPmA5hEjHmSGst5INnNAuFXfYfmIwPNMSDtSdQ5SrIkIoPaXUVaVWkKwZ6x-IJBVhFMv5LhkuTZ1ekxl8SrOWRgB54DI_Av1kgd7D6t9SezynBcvWHqwvmkC718WSCjRSAYOjzLmBDyCRjqpmKvCVik1W0gIeG9n-s6KrOLF4ZTLOMrQ4PWCYLpsUYGLk7dS5qmFsxGGiGXwkQEljHw1go3OsQX6wEBpnCdwOaMPEUS0tkMETCtofimsOhGdZHudJIFjiamFZbWxTzevJnWhKJwkhg9oPFS3UbcRggAWWbKSs7yuF4iglPoVenn6mFi9NBeWznINq9VRZEFSMUnlQdVXKCq_gRkZQjYCLpmIXg0nM-w3BNn0kWabEbAg1yrRjj5k5OOe4o8YzDJW3VVFgymtKEmm7SNkq_ZbJI6raPaXeFAac8gBgU1p4XSWUDAJjvWLYla9lLUvGM5J289T3vKhgoYl-rFbA6ep_Q1ufWhoMSOTmYVL6Xm4iuanTz0yOPL1rz4orVX2Sqp_KnV7RDC6GVXQfZN0fVEUlzOxQxrIiEM2C0-t6TJ7J9jvKsSIwaiZBqDYH6X811VQKPyVOUZi2B9BymL-xglPz5Sw8FX6UhMxj3NhMqx3R-K2ntxZqvinvUXbacP0FDVtxe1mV7B9VjIR2FpOXcGHPhgqREH5qrCmJlUzVNUIqFJ0MTfu7i8JW5a-X1QnKaMmsK35i42w04b2Meyu8VtJHYhpVZnDgO_CYZwaeauFJK92zUgwYM5HUVZsIFnIoEDPcU6h6rYW8Uoq5niQo17vVxrImH2QBlN4k6OobNHyypQexY63FYPwKKktbgvdDu0hK_R783z95czc590ofrpxgzIRwVnuo3a_0DY2epiSe-XlRep7UPKmJU--nnuh7RhenKbtKYwvcqLES040NljxKLOij00BvVjVW4U43K8iuG1DqDYFtXWiiNpNmQgLUmgNOvxMSI-jEDWx-LT9594MJRbUSUMob4NawluZZ7ixYV9-sEbmqepfsnyHW3uo30n0UWtFm2liCLMwEi7IiM8Gh1cd6YDaf1pE6pZRkPuhM1tkNypALWW5U54coB37Q1zH1csCNHNDFEitMnlDNuNPtPXUk0TJ6noIYWZiRRrvXWAd_UFHGUVMX6WzXYeUT7LZsVJpaEpRR4Nh-1yCqQAvBrk1LkzyxWkb5ZGn8ep1JAErQCTh_qiCe6hmCk88UxjRVKSmT4SraLfm7zvziqdB89MfAcDqUbm0z3arUvAeM22BF2boRc30FQVT4fhmLMjbozGoltvoKHtUbrJMSPAyiRKSlx02QZLULTwX9J_f_aiGssRlRZTN7WdX_ICiN4fwAOFV01EwqsbSR41EziA6DqJtWVqbgWQxqye1TMgyzItRspov0Y2NskfE0uMto95AcZWxlef2tzDwdgEF6WHZR9dONk-1zXLsZ-HhoeVvLUjdSMFCn0lGoQoF0Vd4R-cgDUPgjy9R6DQXwpKlVGVizjr2Bgvtw1QZZQX49gk8-8EwruqBSbdFs9rcjG8Cj6vrjsX5qdSIM-KVsqNR9iRFvrIbCW-XAX7-i2t3xr30IoMv8Wx_fgxX6dPIr_csh1FJ6_PnRvw1ifa7yKuqLDxXfsq5wfmag8P8n_-UQSiQ89R8OyYI8z_Iivqflv5fdy__57__hTO3ij545uO_tuWlYN4tY4b8YPRhBgt3ZtHALsLBF2AHjZxXuw0295KgbZ6WqKQtfrK_8SwCTxzYWtIfXrNrdy8EjKtTowWvy8gXtBaSIo8Pcd_y7F_ug1HoiHy5yw7d0BSEiBF1uJGQde3UbKSNmXfmz29mxXh5OM_zLyfX2xmwmwxirEIJJEMwdHjaUG6MLYKa-MZHyUZ-qRQclI24l8TBONnWUU5w6ePQUSJqneZ54oYhSEedlBO7JCwEnGO7Z4x32aIM98vFluSbPvyaPH885Hk_xv949fPLQJM6LjNuE2BcZ8FAESeD7BSsDF2tAPM4598PEz7yk9P0sDxmLecqyFKIqz4eoJ-FhklAD-F3nuWvaJjh3_TumbQpRiqxM2DJts0zbLNM2y7TNMm2zTNss0zbLtM0ybbNM2yzTNsu0zTJts0zbLNM2y7TNMm2zTNss0zbLtM0ybbNM2yzTNsu0zTJts0zbLNM2y7TNMm2zTNss0zbLtM0ybbNM2yzTNsu0zTJts0zbLNM2y7TNMm2zTNss0zbLtM1MOTCM_DQrSz8oMuOzrLb3uzT5GxrXdYUpYWGYB14khEnyWb3sVofMU7vRu48DolTsU1WDAhJWyirUYPfqXqKJuZQYTHSYIDVIViF-PU3Rt3bnrYmKJgyBzgXBC5oRNIVS0WgUgq7nFKbbqaxD5dqyKyFjXlFQhxewwNad42kJvDAa7opPIM3euRFUX5OqewB3lD3FfM0ta_a4ias_A-h__c65b_Dq-Ouj-avbXy9jWNZ8SVqWcZlEfOYvfY17KjUcXLbsm_7e230rzP1FmCTx03D2L5B9M114u2VzXV99khGRUejDGwEoguLPqf997k9U-V4RBLH74qRSFC-bfcUd15aIvNQnWJsvHzc9Zgn-3ukxrBDL8bHfj0sfaH5194lupVdDCUfTWYhtTu-T7dysmcTpCrcrwd3mwIrazDEBtMe6PhViVWKHIFYnVC63wkp-N-6naA1t0toyVlbm7T4BP0zvbalJKo_gBWcN9e1Qaofekd1M6JVXBreo5oTDNh_AVHW9Ph6us1OxtgE-fXDC7mEO33OuEfhoevKnA5pK5sqiaX10UKM7t_rrbh1scj9H5_qGCb0oDXiaMlH4YHJZkXIGkEMmuu-c0DPjUA9P6C0W9P-DBX38xOetv3v19e45u_-RwcLAS0TkJUVcuFkRRCIoE18URernXLiuHyZFyOAMSVGWgEAiEUYRy_IsymHtsOD-Pec5HCzMfnaz88g_j-I7Bgs5Z0ksomWwcBksXAYLl8HCZbBwGSxcBguXwcJlsHAZLFwGC5fBwmWwcBksXAYLl8HCZbBwGSxcBguXwcJlsHAZLFwGC5fBwmWwcBksXAYLl8HCZbBwGSxcBguXwcJlsHAZLFwGC5fBwmWwcBksXAYLl8HCZbBwGSxcBguXwcJlsHAZLGznSgPCZakvgtAVxt9ZExv35WC_Yd5Cd_F6KQ8KN0zcyGQ5rBEMSw-eOkCh53TavZD8Q74pAWJdxTSCHsxBOXoecip2eOGaXPuUBMXkOnOCdBVl7qkfAQBGfO5sEZT0Yw_BkexNwEDfVPRQnpIgcq6SBPWmHRVoLWTqcYPfZcvOYfGEUYom8iV2p0eCVeD6KzcNrNZXggZU6NhWndoOL4gZ8sIaytihuYDtarCU7V6Xwa1qmsQisOBGRlVTb5oihPrEURJbBiiyhutXIPKiHjBes04Y_CeTDfQsRvZyD3JQONAJ9pESi7dnTRTM1ElilTq4Pd01tbmbP612XIF5pcogVCOB-Me-_scDaTNXJs3SKEuZlyWJsWjWhI6tyU-cr8Evwbjp2QCcH4mCS93BjN3dqHmqk3twfA_00lvFob_yPJ_qNBKJ6TZv8Piy8Qx8lPJYcnJA6l0j1aKhHtaWclyyg-2Ss7IUaFDEJaKEfKzqgu4aZwDCVAq20w3ddk1cQgm4nYzmAjCNXldCDxYone73DK8mssqAAGriXksoYEpzZ7pEQVOBthVWPInOIuBmrVMTMk4m7T3T0MDyrlI7TPoOufR37qnrujHw0Jkws60w1Lark4iTWXl9PJwIWoes8wJqql3L23VHCs1qlJU1u9upK8qpmRwLlf8OgJPJolDyklI1U9qLMnSmlVLo3sO7myp11hqglp1VVC5kbBQJENZX9T3g7YA_h2pOvokglPOL_5iZzIeG4n_9-l9UOrrU)
