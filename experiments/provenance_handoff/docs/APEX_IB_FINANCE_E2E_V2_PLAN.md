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

[//]: # (ob:43415aa8)
## Luna executor qualification outcome — 2026-08-29

[//]: # (ob:65a4b4f7)
The immutable root `executor-qualification-luna-20260829T122809Z` completed 6/6 scheduled serial cells. All six produced valid required outputs and finalized workbooks with complete terminal telemetry, exact `openai/gpt-5.6-luna` through `openai`, zero fallback, zero infrastructure invalidations, and zero unauthorized source access. The cells recorded 133 model calls, 3,333,208 tokens, 3,167.114 aggregate elapsed seconds, $0.29007778 settled executor cost, and 14,067,266,570 bytes reclaimed by receipt-bound post-cell compaction.

[//]: # (ob:9a78e8dc)
The frozen 5-of-6 promotion rule therefore returned `allow`. The independent audit recomputed the same decision with audit digest `sha256:32ab5ce5d5d50bf5dcfc5ee1cd72f7af0f1d69ad792c55f365f51932ef18b97e` over source report digest `sha256:c545f4c367ea398aacba23cf9d9da057228886114121c95e1c214dae72da0088`. Luna is the fixed v2 executor candidate for subsequent qualification and, if released, both causal arms; this executor result alone does not release calibration or formal execution.

[//]: # (ob:e21ed400)
## Governed-route qualification outcome — 2026-08-29

[//]: # (ob:126a6042)
Four immutable development roots were retained as failed iterations rather than pooled or erased: the initial schema contradiction produced 0 atoms and 46 extraction failures at $0.02852608; the schema-fixed route produced 21 atoms, 21 failures, 3 conflicts, and 9 gaps at $0.10655537; deterministic atom construction produced 36 atoms, 0 failures, 0 conflicts, and 4 gaps at $0.15101274; and task-contract separation produced 56 atoms, 0 failures, 0 conflicts, and 2 gaps at $0.22213063. These are development diagnostics with zero calibration and formal denominators.

[//]: # (ob:de706476)
The replacement root `upstream-task-quality-directives-20260829T133858Z` passed its frozen development gate. For one development task it retained 7 requirements, 22,648 source receipts, 35 deterministically constructed atoms, 0 extraction failures, 54 governed records, 45 supported records, 0 material gaps, and 0 conflicts. Every route receipt was exact and fallback-free; known preparation cost was $0.14447019. The execution gate digest is `sha256:ba6ae2560b338d5a5f4364d7558ad83d827eb8be317fbf17a52ae00c97629291`, the private artifact digest is `sha256:f24a961e01a0d027490a794b8a122e0a20d7103bf16fb67dbb7928209c16048b`, the governed overlay digest is `sha256:3b34dd43d2ff42e49196d2c8f16da0897360d52524263a9b2a369eb36f4cc0c6`, and the working-set digest is `sha256:fb904c7dd34e3282de81a1bb874013fbc500a5e1a5d2c83c07cc511eb3c860e8`. This promotes the governed route to calibration eligibility but does not count as treatment evidence.

[//]: # (ob:5839d45a)
## Fresh-task freeze state — 2026-08-29

[//]: # (ob:6f2c2aa5)
The selected-executor freshness audit found 15 same-world Investment Banking candidates and excluded the one development task consumed by Luna. It retained no hidden rubric, gold, or prior answer; formal tasks are not yet frozen and the formal denominator remains zero. Only two remaining candidates require an edited workbook artifact and therefore support an arm-comparable Finance E2E: `task_9909f2ec2bbb4899ba7a956a475dfc01` and `task_b2d58a02b48b4b5abd886aafac8b1c7e`. The freeze step must record the public-only selection rule and the caveat that the former appeared in PR #54 under Ling while remaining unconsumed by Luna; no formal cell may start until that freeze and the independent calibration release are complete.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZlNGRmNTM1MWM1NGU4NTdhOTMxMWRhNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImUwZWZlYWY5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83NGQ2MWQ0MzRkOWUwOWE0ZjM4ZmUzZDAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhjNGY3Y2NiYmYzMWIxMDk0MWEwZjg2ZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfetu5Eiy3qsQvfafdZVEJu_qH3afuSwGWM-O54wXxp4zkJLMpMTtUrGGZKlbMxjAD-En9JM4IvLCZF0otVq99sKJswejVhWZt8iIL26ffnvD-7FteD1et-LN1Zvd7rqRiWjSOI3qNJFFmvMyjiLBkzerN1UnHq9FeyuHEb473HGWZlciiXhaRpJXRRXGeZKGPKtCwXkVxXUYhTxvyrTIozSrK8nKWlSJEDEri7RJwjqs4L2iHeruQfaPb65-w3-M1yO_hRE2fMShVvBDJTfwi7_Kvm1aXm1k0MuHdmi7bXAH3-_6x6B6DH7ou67Z9XIY4Jkdr9_zW4mLmv267_4uYbn7Hl94N4674ery8rYd7_bVRd3dX9Z3cnvfbm9Hvr0t4vBy9nQvf9m38PP1fpD9dd1tB7mFvRj7vfx99eZOctxEGcpG8qZ8o35zLR_oS7C58jpPRBaJJE5EKcOSJ01cNDIWIc6s60dc2vWm3UqYuTmRzXVRJ01e11XVxFEVhSXseNgUWaOWo2d3XfPdsN_AghnOs-56Mby5-rff3ujhf3sDp9z1A_6kPpbiuoIt_7c3--37bfdh--ZnWIORB1zHxx3s9z08PeAuwGv4tpbXd3wruqa5FF09XL774Zv_cf3dv1x_-933777_6pvrb9g3139l1z_8-d33F_fizeqT5IuPY99W-xGO9briQzuglMlNc80H2O5R0vv2413X4yLet1t85fA4jPIePtnyezxts5gVPDqghLy52u43G1haDTMH2aVNqTZd_R6-3ZSsCZM4ha_DaY7yIy58kqPg25YWHXzz0AoJP6y_bfthDGCZwQODh_QkuBA0ux2KpfwAv_lD8Ny3BD9sOE53fNzh_FFkQPze_L6aZpnDkSeZ5LNZ_uvIx_0QwGkE7f39nmQngPGErGFM2KOl2f0heMbjCzNiAi58lItXm9FPcI8D-N94JwMQl_YBn-zEvkZpCHawRUHT9dNO0tZdBD_8GPwhnaa64z2fzbOOeFynZfZq8_wrC7jgu1HNVJoDbehAP3T9-2bTfQh4X9-1I-iZfY9f4ps9V-J7bp5JXBR1U7HZPH-Ug8Q3Bb_sQQ-iKC8f6anvL5xhE7E44Tx6-ZjfwonwoGk_ShHIj7Leg4KBfeFjcMeHQO3JDi-vwK_13a9yG3y3fYAXw1VdOLQsTFiSZy-f2E9wNjXfD3wT4Bt6PqgpyY8gW5vHYPzQBbglqGrhsO6Hq4XpFKIIpUg-42zWwR__-H3X3_PN1R__GOz21aatg5EP71dgtka5RiEa2xpmu-vBnOGkUJSqrnu_mia2gY9mEyublNeizj9vnwbQm-Zw7CHC-5r2dt9zun5wL_d4iO02qLrxjnbsYmHHoiKTaZbO9dU387tibrK5M0_I9tNPL0h6kcc8zKr0teaD2zb2ko9oHHF3EAkACKjhkgeVBEUlp61stw9dTfu4JGRZUiVNJsPXmmJ0EXwtR9kDlEGJAtkCsYepwIQRLaHuU0gO1BMgr2Do9j28Gn-_WxC5KilZHTVzkdPzWg87WQM-qwOFL4JB3nOU6-GJs33O80unG2cAJov09eb0lwrwxgOcJSIXMBR0nDu4tO1oNgp1uhwCON8BrIkklIRb3i_ptaYAjZvVrzfR_wpD963Scg3MDybbbuvNXkj8LwglnB-KKAK5TqyCet_3IFCPq2C_XZhoVccsz8Vc4_23Pd_gBJVKgFXfyiC8muS8lxuA5u3micN-7mva8XH52OMq5lWVvv4kv4JL0ArYWfuYEgF0Rqb7zbePxsQAGLkIUCf8sl_Y1LjKWC1l_urzBaB539Hzxj0BcbjfbeD6B0oDwBxHuQEhHXs4-mFfI85p9pvgw8J88yYSUSnTV5_vn-EkrS7rQczbLVjmTXvbIg4D_I8adduNaAwf2o28pU3HvZbB0u0SWVZEafjkfKOr4BbdzS28F1UpTGf9AqE99ZpBjkHf7Ue5LLphEUdZFclXn-rXoMw33Y7MEuKLwYJPIxv0EXnb8P4VqrFWKOW2tLW8qNM0e_35nhBdMFSBOFrG2FmZfhtEYfgfg2FhvhycuqxM4i8wX3nf7u_X952Qm-Dve3FLip_Ug2j57bZDWwuLaSTqWTmsSJBvu41YEt2irHOQiDle-gqmW2kAhma5IQCJN0zyQT4hsE8-vCCdgrMkC2X1SrN514ASUrjxF_cIBnINVkG3Rfgph7tAQeRLx3Fe2DPY4ibN8viVZvmt-qaSNnyUj2DVd_psNTzWqn-Cfgr3LcxSlFWZVcX8ZP_U06bTMHIrdl0LMvTEgZ57ZuEcwThGJfiVnzf2NwQPlZ4wwRxU0LfwIrg1410vEWwIuYPX0YVt7-Eaf2jhvBc2pqmqAuBQ9HmT-6Fv7zlMz36ZTmuo76TYb6RY13KzMYrDyMQ9_3vXz9DFMf6JqiSqwvIgatDtgh5eq-TDuP5PhlnOPbXkmXNZlGnMPnf8H_dbvSOEEi-Cv9IxVt1-i2entFjD282eNG-PVmIEc4z--hIyqMKkYHn0udNTooWuiQa9g57SsNnfrjD-gy_pV_ApH7otSsYGLQN8tDS9QoosLeU8NvUNIRSKJd2BKnjqup34-lJ8LkmitK7KF48I3tp3KKSkVHD7EGtajPTAwCI6vpyOaZBrshWH3trPKxPyfQP7ixHQ6xoVFg1Jn5hYrLyORRPVURWLIm_ihkdllFbwEy4E7Bbtro5KBzoqHcDdqt_TZaMge08jYYTV_AsDrD9jOBv8kUfnDW6I23kJBc9fGP0euma8buA0ZA9YUQfZhyq6ihmveViEMpesztK4bNIoYmGMuYgw5SLO61jmZcjLvErDqGY8DDMOmCFNIpknGHlCt46C5eq0ruLkd9hoDEmzkGXrsFiz4icWXsXRVRT_pzC8ChF56h2n4EzFeJoLEJTpt7_9X42vk7iq-DdI5B18Hw1EJGtWxQ2aCXqHExLXkvwqsWw9YhHWVVzDScKdMSM64W0z4kvj03ZdIcgM7AuruRnFCVnrUT4n5pzQzPr9NrhRIGO969Nkbd2sNUpJWICMhFkU3mg_x1nKQ2R15FUQscuITXYrQLs1BD3froIUP1HTgg_I6tLz5uAJQW0eA3aZgVqEswg-APYM_o6XC35tH1gpvXKHOn7Yb8bgAx-sJcBggULXF4DC8CB7XESgUyYr8BDqzR5lGIfr9StAXfNHAEUBXRHE6Ph6WBisqkO3EzzCU2FCfUh1k0RFyWKZMSsKTrxeH9LnBNwxYEmnFePk8C7Z8DPo2X_hWwT8CvOBAgbXTYKPOcxfhrt2K7dwUx29q2D9n-UtQEZAtLJ-rDcYcR7lLWAL3DD1GTww7Ru6s-iJmY_63V7tpp6i6_UM8LEcLsxHaKNxObAL3YdtcAeYeRjXt3yHkqE9qFt8N10X5T2brVIBedw863Ojh4pf03hcioVTSpqwqpuGx0LaU3KyFdOFfWb2Qb-2SmMJip2zmDVW80wJCRMc-4wEg3PCTkxp7oOsAtHBgfcSLntNyJNCIygt8D4waualJDuCjxw2r7tX6JY7anFt3MgVidMazm83-ZQBxgXwexhVxBNv70nhB3BFUOvgI2piMMEPdy3KEt48fNRBr-DYwDXGrDiF8Mau2xB6GvDn9xJljAAuYagaXNH_fP5YszCPIjCAGcuEvXxT3sVqyFfIo-gR87LJC7jcUjJra5zUih7xc1IlyuVzTs0e2MW_b_HF03nhy0eT_HBGoVc8PRAGqUjr8il-cO7cKaSO4G1EjaTDx7BYUiRv4arSlNc41zUJl5LBixNReL2TYchykTZlGRW12UknF-Sc3UtzO8F_3w3o5d6TriAxNEFRZZJRKkEJIVqtNtqdpyCIo8OmgIh6ZouZBnDVMBwwuhmUtWxAhY7PNBuybLKm5qJu0tKs3kk4TQrpRSkjPUhcySwSTVypvIIS1imL5GzxK-WB9LhRxngUxQjEmRnXSQ3pcT8nuXMozHA1GL6OTnSQdDLuhQAY0dn7BHoUI4cEJ2DUer_RahSkZLcf1Q2kWAF3o3oqSIZKE74HoKkCY7qiqBjZP5hT16_5dgDkYqT_37fxBZiUEaypUZDWoN1uugqXvFJ6eO4bmXURhrrsEb9cIkKDqQYbPAAK5-MOdfWezm0H7sblIBXqM1-BCSQX4AbSNdUbuCa4ZAUJvndPR44uM932fYW1RSuCqWhhVIAV3Jtgv21HN_1iEjJ8WHcN6imJcfkdekGkv1dKxc6yTbhVgMPA14FX6XmqHQfvWba7UR86TD29CL4yoghGpu8BInXzpJY4EiA45Pspz0Wre6uMiQJ6CCp6-aEHaETvAHvlJL8Cssyy7YMKvFzYDtzCDOaxAfvcNo_WxTdiYC2cegoM4kBLNI_D3sznDMYadg3_NRM95x_wzq6tEeoOw_5-pz4HgX8fDO3tlm9I2ioNCjj84nFocZo5oL8pggVbUcMiYRd-lfoCWe1HDoE-qFVA2l4d7jCdqTkz5fStAiN9ZgA8f8LiKNQYmnxAcboI3t1XoJY7BIX7rR4DAYXJ7Ul1W-5Nzs9saNNtCAJbRT_Aluj7h0gPFljAXQJXxQ3TzfMBCvxvEfvg1ByAiehqGPBrgEYNhLlv4UxhD9st3HqaL3zSbQ7OJgBP6K4T3aa7hSXXbY8f9NM-EFDW2zRlMNXmcLMZgQLz-JUKwyiwmvKU-tNaRykwa5TB_dndATx6RKsMe61MlT2jej-MnYDJbSTHakHlEPFen5CcQjgUzYCxo_AiMFlXlA-FAvAAaAB1IvjsgaFXehQ8SrCv663cw283Lkwgv0shNwRYXNAWY8iSCt4AGC4AAlE2vEnSKs0p4EZWw8nUTybxhZl2Y3k5k_DOiBXNZBSn5Lse5nOS54e3GxQPnJCOSpqLtHJuUvDd14O9gBppwSW8wATIgVbQYX2rGdTUUKk1JpRmRiNXHetLKzjcQaKRRs_4x0mTqK8fqhLjD-scvNDSgf7Ydm0OUkF--4irFrUqtIbOvSk04DyBsgCSUgYAJpZpUhOcV_B-Kj_QR_U55QNozw41HQj1duA6fEKxrRHDt8Md7nQNVwueIfyHKEReogYaH9fKuFHB54q2F6eDWIbeyW9ve3CYjQJolct8v0fzQ6gHlRd8jDERLSAgS-8mNenqJr3MQEXCpvsNd1prNLv3OMikvpTTCWZAh0RA26ICVRUBCvwg_uPTsKQ7UUYOhnqLSqC9N99b2csBi8FC6E03kCYZWrHXr0GpAvNYSyNRGLRRGFqrfK2ezstDk1UJy4siSjOLK50qj0lDfHZ5hvHvq7zgacWLStgBnYoNm697eamFO8-ml_JX-Qnpg56TbKLSwOCS7G1Bufar1Y6udBzM_AtmtQs27T0K_wc-1neiUyPdW_Sl1NC2WzcgnxWv31NShMJLFFw6zm1TbA21BQEwOlWVjAQZ6duPC6eas6SKq0iGOU-nTbZlJlM584vrQwyYbvBL7a8acqlsoH6blf-m3aiEN8inVna_Th6vwvXauI9ocEHVpgGg38xOR8x2x2ZgSTVu0Tz2FM3aUs6YlA0BZp3BwluPyUcElwhGDz-3tSb4gv0Ig-KxNPjmCd9RNAkDKug9j3sB-n_sdnoOv8q-M4dj468L5yOyJk7h3vFa2jC0U1ajz-dz6mFa-hDFH1cv2oYKD8bpvmqLNMDxkldK-kPfK70SdXkm-wdL39p4tY2C8BoA-rBc_2md2IwXBcomsx66U52zrGxeUFajh-VRXLGiSMN4QkFOpY0e9nNKZEBLr9Ev0pE4JdmX2hW71C639l-UjXQwCaoSY9SM--TgfP1OYxfW1lYBQABNstKYfPoCWgbzGV3Ptb6HGsuuKJ9wz50I4mq65rPfEtZ1vAZEO-ePN5Qpa-pCNjK24SenQui81nl2ac_SvurvHCuut-p6WrN8sB36Y2oOme27OQsDxEDqKSGkMT3Inh4SPWaFbUBpacN7f4Sg3k7arYSHzp_aW6UKt8ENDXUD769VSxPdUXQ0dQ_T5DM7WMYFGgSl7Qwugm-1wlOqqz5dFDM5N0e67XmBODDmZRnVUS2nELJTeWXl4OUlUxj9N44QrEpt-d0efBWNpqXOlDftx5FqGFDdwS94BS7SYWQI862kAye0S8kdvps2GL7TEQ40lUMUq6KJUHhKi6sOreC0FrR_LPNCJmmWCpvicCq9JjX4kmItgwCqOOQsBfnksRnDqd_SY3xOCZYrPZhftI72YJIlLUikBgYHkXMLH-BEesqaacdXCTZpSQd43KrynxVdxWmLVzbirFyLi9mGmbSJABWjbqeJVY37rZwHmsFGApS0-tECNlrHGs4PXoTKWQG32dwwcLRRGsjiCQ3t58e1BMLLssqqPJY8D81hOWVsU87rxZVoWiYJIYPYjy29qL-VowUWmLJRZ30uFYqtlPgttPL0M5V4mVlQPCuYZaunzIKkZJSOg-qr0rR4BW-VB7WVcNG072IxiX1-S7DNLEmlKTEaQoUy3X7AyBysc39PhWfoKt-1QmDIawoSGb1I0SrzlI0j6tw9hd40BpziAKBTOnhcB5QsAuOD3rAHZs5apYwXTjqsChZFqeCJ9X6cUsDp6n9CWZ9-NSiQNKySvGFRZT25qdLPdo68vGrP8St1fpKyn9qcPlAPLrpVdB9U3h9ERQfMXFfG0SLgzYLR6wcMnqnyO4qxIjDaTgehyxyU_TWzplT4Be0UuWk7AC3z-I3jnNoPF-GpZGme8IjXVmc65YjWbr28tNDsm7YeTW8U17-iYhPHr9XB_r32kVDPYvASLuzl2CISwt9abUrHSqrqA0IqPDrlmg6nk8JO5m9Q2QmKaKmoK_7Gxdmowgfl97Z4rZSNxDCqiuDAZ2AxLy08NYentPTAGzmiz0SnrstEMJFDjpjdPY2q1-aQV1ow19MJqvcdlbGsyQY5AGWwAbrNIyo-VdKD2HFjjsHaFRSWrgHrh3qRhPoHsH__JVq6yVXUMLhyknPrwjnloW690icUetqUeMkq0USRkjwliVPtp-no-4wqTpt2VcoWdmODmZh-v8WUR4MJfTQaaM3arZO4M8UKquoGhPqWwLZJNFGZyXZCAlSaA0a_lwojmMANDP5B_ea7r60raoSAQt4At8a1Us9qZMn7zeMakavOd6n6Gdrao3ojU0dhBG2hjCUuk1LytBSldQ6dOtaZ2nxZReoUUlLxoEuVZ7coQ73IMaMmPkQx8Fldx1TLATdyRBNLW2HjhLrHnW7vRaAmrbznyYlRiRmltAeDdfAH7WUcFHWRzPY9Zj5Bb6tCpakkQSuFGsvvtogqUEPwD7akSa1Yv0bbZKX8BhNJgJmgEQj-1II_NXAEJ7-SG7NtGzUz5a6i3lL_NpFfXBWqj-EQGE6LMqVttlqVivdg424xo-zciKW6gjgVjDWZbDKLzpxSYqeu4Fm1wSYoUSdxmsuiiWrrJDnlwlNC_8X1v-YQ1liMqKOZg8rq_ygpjBF8DThV9lRMqrC0PceDYhDjBlE1rcpMwXfRqSWzT8EwjIpQsZlJ0u-3VhdZS4Oj7N0akoOIrUqvf6siTzMwSF9WVVTDdONU-VxtzAz8euzqbqNS3TiDkSqVDlwVcqTb5oTnoxZA7o9KU5t3aICnVK2OwNr3uANouA9XbVQZ5Hd7sMkzy7SiC6rEFtXmcOzZAB7V1x-X9X1nAmGwX1qHKtlXGPHRKSg8Sgf-_DuK3Qm2DwnzslwfX4EW-vjmZ2IOoZLSw98fcIM4v9dxFf3Bj219x3sR_MRB4P8pmUMokPBS4pAyrqqyEtmZkv9BVS__7__5v4KpXPzZPQfnnl7qhg3LlAv2avNBDxL0zm0HtwATW4Qd0H_W7j7c1JsaZeOy0TllyeT6gd0AmDzUsSA99Ya392d38GAWuvXgHVl5QWPBVOTBYs4t__TLftRiPU0fLvK2vqMrCB4hyPJWQdb9oG8jRcScK395HB0b1OLMhv_25sPdox1MuTFOIgSDIBg7nBeUW6ULYGbzaD3lgzpVZx4UjDgK4qGfbPMoF9h18OwukKIqqiqPEpkWMquaFMxTlABOsLvntne4rQ1uy8dv_pp8_jV5fnvOYXsK-_1088lTnTiv0m6TYF1kXCcyzmPGBG_iEHNAdVbVNUtyVkZ5w1hZJZxndcHLAryqiIHXk9dJnlMB-Kn1nOq2ia9CdqLbRshGlk3OfbeN77bx3Ta-28Z32_huG99t47ttfLeN77bx3Ta-28Z32_huG99t47ttfLeN77bx3Ta-28Z32_huG99t47ttfLeN77bx3Ta-28Z32_huG99t47ttfLeN77bx3Ta-28Z32_huG99t47ttfLeN77bx3Ta-22YhHZikrCibhsWitDbLKXs_JcmfULhuMkw5T5IqjlIpbZDPqWV3KmReWo3evx8RpWKdqm4UULBSZaFGt1b3BlXMjcJgsscAqUWyGvGbboqhcytvrVc0YQg0LgheUI2gKlSCRq0QdD0nN90NZc2F644_SOXzSkEVXrAFruwcdkvghTFwV36E0xyCR0n5NSW6M7ij9SnGa4602fM6rv4CoP_dd8G5xqvDjw_6r44_9m1YTn9J0TRZk6f1wl_62u8o1TC7bOUn_b23c29Y-oswec6KZPEvkH3yvPB2q-K6of2oPCIr0PMbASiC_M-p_n3pT1SxSMRxFr76VMmLV8W-8sS1pUnemBWs7YfP6x5zDv5s9xhmiFX72C-HqQ9Uv6b6xJTS66aEg-4sxDYX5852qddM4XSN2_XBHe_AisrMMQC0w7w-JWJ1YIcgVi91LLfFTH6_303eGuqktaOsnMjbuQN-er7Hp6ZmeQAvar6luh0K7dAzqpoJrfLK4hZdnDAv8wFMtdmsD5vr3FCsq4Avnuywe3qHz6xrD_toa_KnBdpM5sqZ0_pgoVZ2jurrjhY2mZ-DdX1Ch15axHVRcCkYqFwuipoD5FCB7pMderYd6ukOPa9B_3_QoM_v-Dz6u1e_n-6z-4c0FsZRLtMoF5kISxGnMm5yJoUoWFXLMGRJLhIOa8hF0wACSWWSprysyrSCdyeiZmfWM28sLH8Ky6uUXaXZicbCuuZ5JlPfWOgbC31joW8s9I2FvrHQNxb6xkLfWOgbC31joW8s9I2FvrHQNxb6xkLfWOgbC31joW8s9I2FvrHQNxb6xkLfWOgbC31joW8s9I2FvrHQNxb6xkLfWOgbC31joW8s9I2FvrHQNxb6xkLfWOgbC31joW8s9I2FvrGwW0oNyJAXTMZJKK29czo2zsVgP6HfwlTxRkUdizDJw9RGOZwWDEcOXtpAYfp0up1U-4f7pg8Q8yq2EHTWBxWYfsgp2RElazLtUxAUg-s8iItVWoYXLAUAjPg8uENQMuwHcI5UbQI6-jajh-epJkTGVU1BP-l6BUYKuf66xe-qZGeePOEUokmZwu70lXgVh2wVFrFT-krQgBIdd22vh8MLYpu8MIey71FdwHAb0JTdzqTBnWyawiLwwlvlVU21aXoiVCeOJ3HHAUVu4PoJRF5UA1ZveC8t_lPBBvouevZqDDJQ2NAJ-pECi8e9JhpmmiCxDh0cd3dNZe72T6sdZmDe6jQI5UjA_3Gv_2FD2sKVKcoiLQselXluNZrToeNK8gv7a_BDUG6mNwD7R9L4xlQwY3U3Sp6u5B4DFoFcRqssYasoYpSnUUjMlHmDxVeFZ2CjtMVSnQNK7rZKLLZUw9pRjEtVsN3UvGkkKhR5gyih2rcbQXet5gDCdAi2NwXdbk5cQQm4nZz6AjCMvmmlaSzQMj3sOF5N3CoLAqiIe62ggE3NXZoUBXUFulpY70l6mcJubkxoQvnJJL2XBho41lVJhw3f4S79h_AiDMMM9jCYMLMrMFS2a4KIk1p5d9icCFKHWxfFVFS7VrfrRAjNKZRVObvj0BXF1GyMhdJ_M-BkoygUvKRQzRT2ogidLaWUpvbwdFGliVoD1HKjitqE7Ld6CuDWt5sz4G22P3MxJ9tEECr4K3tOT-YrNMX7P0P6Ov3vTVTxLOfz1sNvDyrF58etIz0EDp5o4nz-i57b1Vnwqqiain-B-f50tnvZseSIG7LLzIl6k8JdaO6M0iRmqcy-2IxV5c-UZsUAiVXBhyUWtqhjYcYyjIqYR8UXmvFgImRK9X6w3sD33aK6eV5fvyPQS38V1lG8TyxJV4RfnBPDJ_5crA7pHqFdJ6d07CseproA8I18M1ycE6wn5jCekhOTvVIxvCkDoKycDqlcnBOMM3uLJ0ke2jg7aOWrS518IfMsQEfps_60dv3pLuolmfDI6XNU_AhHC5xiRaA8Bad-CWdKOPU1Td1UCH1Su31dVSFrGsAbQjQiZiKKGY8o23ey3d42CT_dbu8VtlfY_7wK-_m0FIdt98nvp7vq_zF_n1gWMmZxU9dxKmRahA2rI5lkmZRlWeTgGjJsmhQZTySLEiGiNCuLWnJw7ERFCdlT6zmkEYjYVZRfhfkJGgGWFGHWwBF7GgFPI-BpBDyNgKcR8DQCnkbA0wh4GgFPI-BpBDyNgKcR8DQCnkbA0wh4GgFPI-BpBDyNgKcR8DQCnkbA0wh4GgFPI-BpBDyNgKcR8DQCnkbA0wh4GgFPI-BpBDyNgKcR8DQCnkbA0wh4GgFPI-BpBDyNgKcR8DQCnkbA0wh4GgFPI-BpBDyNwD87jcB0EVlTsTQVogCZnHoDbBelU870as2PJrgGOiDPIlFJZpGT0w-5qAKe18Y4eYDHVRw3rQF3vL3cYEAmvgjXzQbmtm4Q38zBOkhGt7_FmP1DO3KbJZ_k_4lM_EIRAMV4demjxASjvUr6Fs1CSihd-35amO1WOlknoLSXLiiQk1kENU5RZ_MWSR4FH6Zoxg1d_GtyU2-mqKG5DOaPgh-9WGkiVJK6r8ogA5ZGpltCRcyibBWl4YrF6cwLB3xQRBd5mTo-qdzw3UCnioYfvWYEDdb-6yqoXlLHO3wvSlZhlq9YAi9LMq3HVa_HdItRDCVlFLRCve8edF2h8RpU71d9Bzh6Kd7BJatykOMqb2wBmNMnO5Pkl7W3ujhnSlEofPRkpQYObIPy7l-0B62cXD4xyoqa3dRxz6NfqyCET9pZYGtt8KOGGDhF_FajRP5wblpa5tV6B-ZdRTMnuGOiLjcmuHKlckM3U2TiuGHfPjR7-fX0CjAf1-AGXNsurRtt151-_-BmuOMsza5knlYNb0LGZJ01SVw2YPXSKm5YmuRRGJZVzsIyrOO0YIyFdR5VANxZVDQlFylL4D5RmFCpCL3CgzE4E2UKT4YVPFyxpqhYWYRJ2lSJKBnPikJEBU8L-P8wzUSYCZFWPBdlDqOmdXazIK-g3aOmKQFrTdEXp0va7Wl5YXOzbfki1b2mFJAqfVkdRQ7Igqpc6BqrG_fD2klmHPpudOlNdFN5faaWqx1srEK59U5rjTvH2RRWz7Gfb0msAI5YnLJWguEAkAM7f0Hhbl1yT4HWFn0OgFjnABl1x1HUHHahx_AdQRKcuNtTNxVggW_R7FUTpt0dW1vlFK9vTG-pONeXNFWNqCAyXGTQvOjfoVY6ciPUFlO6lL6PwTC0yLRNg9L-1mIcNeOq5I1KG9tqKSdYToBKeRZjhzHLPVWN9HJSmy-kRarP0CLVZ2iR6nO0SL2iRRr_X2VFktuHtu-2OItrVOTDlyBHejUmCDArpHIXOByqvGZ5JqPZWCrBd0r4rYziQCDNT_B6PP9F7rUgmLtM78FYBhYi-xLTRu28hRceNuxObwN1eNOBGQR8e7sb1-lFtt4ARL0J-oWNTuoozKIk-wIzfqd0GXnWphBYqz4qhVSBJV3EoLSm9UAXZpxleZHkefGF9njSW3quB_EG9Vva2SnUEDH2PD6mY5Yi5zJo2qCvur5X4frxCCuRP6sb5uY4glTnWN-dBkQX527XU6xQB3dgeHKfL85diNMjaf3xZ9hOBTdniUD0nTH_7oLYwSbYtSk3BciYHr44J9ynR_9aNuT8WMNLwqoPXvUxWhKkCcObPqaLc3L5DAIqJeo7DRlo-XrYyU-0MbnJxhxgljP8UD84hwYm20R-tOqgwc4o7ClAOd0Dkjm6BZopwe6EbZA0bFTTHroRKb0wHSLd8P0WPCydc0E4MZ8CAr5P45cqAZpnPOFlwposijJeFQDQS3GOX8qyxzzNL-Vtnrd53uZ9gs17PvXbEQXUarokV9Hvp-me_iH8VnUUR-AsZDBmkcYMnHJwx8O0SVMeijSM4lwkMhdFkWeiZmFeVHnOWVbEeVGHimrpycWdILti-VWcniC7SqKwzgqRe7IrT3blya482ZUnu_JkV57sypNdebIrT3blya482ZUnu_JkV57sypNdebIrT3blya482ZUnu_JkV57sypNdebIrT3blya482ZUnu_JkV57sypNdebIrT3blya482ZUnu_JkV57sypNdebIrT3blya482ZUnu_JkV57sypNdebIrT3blya482ZUnu_JkV57sypNd2R4B2SRcxiwOE0925cmuXpvsylNdeaorT3V1nurKLQKTlaxqJhtmZdshjXAyCC_nenga2TTg-GdpU8sisXFIhwPCuWEvpW5AZK_rywwysRBdP3KzOkIpxmJYR2KKrBupm2onp469douA4B3awR1Y4tvuRB2n66qs3GjNmiY5FyLVYpiFayrxrPluFcT4L3UmZGVg1-GWbLFHSlUZgh1aJaH9korAT2WhGu8ZALiyGVSdvlPZonlNlorrKhWQrrtmnTmGGV2B4Q4LY7jaC90WTB6EDYlasKPoaQzikVR1TrdjknxzT3Q8y-oaujePKsFK6SPXrabh6L0UiDDg0cYUlG61JUj80dZUOSOsNPbBaAQ5vVO4ZeW0o58sUD3w_-7bgTiU3MqNJdwLU-yoCKFdSIDp2g4TB1myXUXIwCSyNA5t2MDhKjElOJ9BMXKcfkJUNcsnrebIf9o1RLG6fgZLO6dNVMpSKfy1AepKvqkqVgXUaYJ4lqqw95jzR5f22EdseI-kz_IPDS79kEPPtGSpJxtNydtzJnKqY9OKHRArOZg4pVb3hw-m2O40Drvf7UdXvxyW5K30iRjCDrqp7RabWDTrgRO6ME71STSCvsPbSbFOl5tv8FCtybXi-_zyopwXTCRCplFuI7EOBY2j4l_KHJPF6d9suMoJJ54TC8zxEq2Crlk8bTlmJmOyFNSVfCTodI74W3v9zQdOFaO9B-BZ7fvtjLxLS7wKhOnuTOsQFrHKnNIorDAa-1RGFqRMxZbCNGQqBnw64PdMcIe6FmMGJ2MjnjhzRpwJCK25RinsvwRjZhInUcr5nLZpiX5tHmh6gtHr-S9axnWWZCrl2B-ef4HZzlXFYlD7SZIpZ8YlzwtZiPoLzVir3yP0RE6j67Nr1aB1_cXCjCWLpEiI4Gma8Z90l8L6RHp7PuUnJOL5L3qmSEQs40jl8QWmS4G-SSbcFCjKhyYfmuqPhom6ZokpTcg8zBTzyGvP-KcTSaDgxhjntWuc17qG-EEOSpYXZpwWcSkSYpxwKQYPYgs6lX90eEvi8OyXLCmFhtWMU1PYa87uJ6dQY20v65lESTpPlDyPadXRvWc5ThVOE1QQ8By1oakdLs6pzSXeT-1nEZamsSy-nY8182wclK3qK6eAsC1fWSQldTTk05NzES1NUccHTTeJyijZ2jHqXsTIMx_P0oka7HlAzOqowWcdzu1zLvDJ03E02OmRfrD1iYiZGtRKWtEcDHpCQ02JROOkIsIcrJd0sGpHNz19GIYa9mgWjngomZjVrjkIUQUnnMDSGa3zrBNozlz501diUhrPWChRxKjJOqNMgaLZkt1Kw5o_SK5DHMPYbjbrs61HJ2ly1SyctMCCDlgtyuBqMlRaeI6kxSkt7OVa76HTBDCv1XKO8dO4cPNEZJEA5SdKGZY8aeKikbEIz3HhWnLJp7lwPZr1aNajWY9mPZr9wmj2-fTmhzTDxe-niYP_IbTJIksFzDKKRcrjOozDJI1jXmZNGmUlSzgr8kiwpIa1hElUV2WDKWDB6jTK46RIzqzniCk5vkrSq7A8wZQsQ9lI3pSeKdkzJXumZM-U7JmSPVOyZ0r2TMmeKdkzJXumZM-U7JmSPVOyZ0r2TMmeKdkzJXumZM-U7JmSPVOyZ0r2TMmeKdkzJXumZM-U7JmSPVOyZ0r2TMmeKdkzJXumZM-U7JmSPVOyZ0r2TMmeKdkzJXumZM-U7JmSPVOyZ0r2TMmeKdkzJXumZM-U7JmSPVOyZ0r2TMmeKdkzJXumZM-U7JmSPVOyZ0r2TMmeKdkzJXumZM-U7JmS_4mZkp3ilQIwuMxSOIx8omOwZGgTmngtDjNbBxGHWVzIKhN2XIfW7KRwfRobWRGWf7txvL2TwRNjdlDCwMS9MNKgZGXRxihhOS2wx7J6IHb0zwXr4gazz1sqZckPQhZRHM9DFvEqjuMVCwsrpfEqyvKLKErORytWKLusDMMcdIMV6YM6IZyiiVpk2SrNQx21mIIa1aOJvuoLtTsRBFkqIZahyAAbF_EUb3Oo546jFJ_MGKdLIc8qfTEpfVt_fd7LhmlWaS1TAf8XVk0q6gYJLaJa5KzJwf1uIpGBQ52XrE7TJgbEjZV5gP2joipz-Rwvu07Bp07qOMslj8uC87riLK6bUpSCh2kON6UoMjjeiEU16IIIvPhEcJkz-DgsClgz3f3WsLwikn9gp8C8amauBiyZP0piwLdWmPTWhgf-QfFe3YiFxaFvlYvrlN8RsdCBJdPPLyZAl6WER1mSxaxIyqnI2aH7c6opX4ulz1jULIprEEVehLa_yiHuswW7L-fb63UdNvxXlcXyrcHaGIHtceOvdABJlfPapg50FURbGxdY6cFQsxLg3U0y031MLXK2QEwZLlakqHtVIEEbRSUravPsK1mk3rnCn6ZAW3zYsV2qSnr1eoC_aZrG-duDyhXqnpnV8Nhx4syME7rxvMNhktkwaRRGLE_e2ob6tfGhDCKbjZE-bwzmjsEYi9D2kSoZ5CLNyYRBnpENWdKLoBhBv5Rxw6ay_ol_0dGLL6VNJKMbx0Va_G2WgLRMH9MCbylwhVRMdK8PGniCdpxkO58xfoDEsFWWFJO-M4m6OD3BP-GSp9hTOiHBqyBNph4xHUZdBUkaOM1U5rfhvFFGh3_dZhlVPqeE3tQ3fjAcR-rstGEn7-2tzoAcVtHSMyiSSZLkYVQqyzM5J2SGtarHIIrW9hXPuIQfwgoOQ6QcVH-cJSJP04KLIhYFy2VVVDIGUF81Uc5TxkE26jLPWMnK6GaleXxVIZ4tIzkeqWEJL7NIhhEPRQiXpgx5XiZVwQF8yZCzUORRGMMgWVNluagqsGIFC8s6An1XVHoku_H43w1_PDFSXMWJEEksWNMkTCZlVGaC1QW8GUxUUeZxFoqUpSwBj4KXFeNxVsoqzsDs1WGdOWFztzL5xJKqMkzqXIg4kWAfmJBFxKOqKvIkjOKmqtMw5GAheYrDx3WY13UaRTBUXWShLG50wbCCE9oBnCRL5arnd1l1BajAJ1aPWDNHxdEUmLENDDabvADnmyypmyos88SW6Ti0pW6q8-WMo8aMlkUOR5CDkFmw5ZCQukH2F_KHLiXDjxLbJ5WJmyNHFKP9R61ett28uPRMuvvtrE3Dtgk8ggxp9WbE61gr24owFUL4y1aznKlfH6xJKzuMK6g_WePU-JiLqIfS-NRw_GgiEALJxKfkskxeBTc48-uyDMuGIT1nVSVFWVY852Wa8SRPRVOHkSp4U9-tmACNETL4YpVUKa8EgETOYQpFFdW51EjYyo7cGbILIgA5JD_XMXADsM1-KZbziVEQ9w9d8N1O6pogU2-nktsUKjRJTrOB--3hKSsWNHUWNp1CEQRdmkADOn3Khxm1E4WZgeKc0KyWJ_700M-__x9XYJN5)
