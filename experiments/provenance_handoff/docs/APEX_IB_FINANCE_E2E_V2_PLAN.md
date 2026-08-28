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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZlNGRmNTM1MWM1NGU4NTdhOTMxMWRhNCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImRlZmU5ZjdhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84YjhiYjcxNGU1OGU2YmY1NDQxMTRkZWMiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhjNGY3Y2NiYmYzMWIxMDk0MWEwZjg2ZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXOtu3Eh2fpWCFvkz6ZZ4J1v-kXhn7IWBycTxTgYBdgdysVjVzTGb7GGRkmXDQB4iT5gnyTmnLmS3pLZHUhAEaMCApW6y6tS5fudS-nzG-6FWXAxXdXV2ebbbXSmZVCqN01CkiSzSnK_iMKx4crY4K7vq9qqq11IP8Kze8CjNLos8E3GawEtcljzIeBZVvErCOFNRUaapVEUQKZ7mQRiXVR5X8FlYwFd5XKgkKmHdqtaiu5b97dnlZ_xluBr4GnZo-IBbLeCHUjbwwS-yr1XNy0ayXl7Xuu5atoHnu_6Wlbfsbd91atdLreGdHRcf-FriofY-7rvfJBx37HHBzTDs9OXFxboeNmN5LrrthdjIdlu364G36yIOLvbe7uXvYw0_X41a9leia7VsgRdDP8ovi7ON5MjESiq5Ujk_M59cyWt6CJgrr4qyKMs8TGRayKxUwLcwTCopkLKuH_BoV03dSqDcSaS5KkSiciHKUsVhGQarJOSBKjJljmOpuxJ8p8cGDhwhnaLrK312-bfPZ3b7z2cg5a7X-JP5WlZXJbD8b2dj-6HtbtqzX-EMTh9ga_lxB_zewtsauQDL8FbIqw1vq06pi6oT-uLl21f_cfXmz1ev3_z08qfvX129il5d_RJdvf3x5U_n2-ps8Yf0iw9DX5fjAGK9KrmuNWqZbNQV18DuQdJ647DpejzEh7rFJfWtHuQWvmn5FqXtDrOAVzVqyNllOzYNHE0A5aC7xJSy6cQHeFqtIhUkcQqPgzQH-REPPukRe13Todmr67qS8MPydd3rgcEx2XUEL1kieFURdTtUS3kDn_yJfesq7G3Dkdzhdof0o8qA-p19WUxU5iDyJJN8j8q_DnwYNQNpsHq7HUl3GOwH2gR7Ao-OUfcn9g2vH6EoqiQvw7x6Nop-Bjtm8G_YSAbqUl_jm101CtQGtgMWMdX1EyeJdefs7Tv2p3Qidcd7vkenCHks0lX2bHT-EjFe8d1gKJVOoIoEetP1H1TT3TDei009gJ8Ze3yINyM36vsQnUlcFEKV0R6d76SWuBL7fQQ_iKp8XKT3PX9EhiqM4oTz8PF7vgaJcKbqj7Ji8qMUIzgY4Asf2IZrZniyQ-Ot8LG--yRb9qa9hoXBVI8ILQuSKMmzxxP2M8hG8FHzhuEKPdeGJPkRdKu5ZcNNx5Al6GpBWFt9eYScoioCWSVPkM2SfffdT12_5c3ld9-x3Vg2tWAD1x8WELYGuUQlGmoB1O56CGdIFKpS2XUfFhNhDXy1R9hKpVxUIn8anzT4TSccL0RYT9XrsedkfmCXIwqxblnZDRvi2PkRjoVFJtMs3fdXr_ZtxVmys5mv6PbX3z6i6UUeAzIp0-eiB9k29JIPGByRO4gEAAQIMHJWSnBUcmJl3V53gvh4TMmypExUJoPnIjE8Zz_IQfYAZVCjQLdA7YEUIBjREvo-g-TAPQHyYrobe1gaP98dUbkyWUUiVPsqZ-la6p0UgM8EM_iCabnlqNf6K7L9lvePSTfOilQV6fPR9K8l4I1rkCUiFwgUJM4dGG09OEahT5eagXw1RBNJKAlZ3h_za6oAj5uJ5yP0X2DrvjZeTgF9QGzdimasJP4PSgnyQxVFINdVCybGvgeFul2wsT1CaCniKM-rfY_3byNvkEDjEuDUa8mCy0nPe9kANK-brwj7W5eph9vjYo_LmJdl-vxEfg9GUFfAWf-aUQFMRib75u2tCzEARs4Z-oTfxyNMjcssElLmz04vAM1tR--79ATUYbtrwPyZ8QBA4yAbUNKhB9HrUSDOUWPDbo7Qm6uwClcyfXZ6fwRJel_Wg5rXLUTmpl7XiMMA_6NHbbsBg-F13cg1MR15Ldkx66qyrAjT4Kv0hpdsjelmC-uiKwVylo9Q2vuW0XJgfTcO8rjqBkUcZmUon53UH8CZN92OwhLiC-3Bp9MN-oqybVh_gW6sroxzO8ZaXog0zZ6f3ntUFwIVq-4cY-i8Tr9gYRD8A9NH6OWQ1GWrJP5foFdu63G73HaVbNhvY7Umx0_uoar5uu0w1sJhlEQ_K_WCFHndNdUx1S1WIgeN2MdL3wO5pQVgGJYVAUi0MMm1_IrCfvXlI9pZ8SjJAlk-EzUvFTghgxt_n4tAU2qwYF2L8FPqDTMQ-WKWOB_hGbBYpVkePxOVr82TRtvwVT5AVN9Z2Vp4bF3_BP0M7jtCZbUqV1lZ7Ev2Lz0xnbaRbbXratChrwj0oXeOyBGCY7iCvPJpe78ieGj8hCvmoINew0JgNcOmlwg2KrmD5chg6y2Y8U0N8j7CGFWWBcCh8GnEve3rLQfy_MMkLS02shobWS2FbBrnOJxObPlvXb-HLu7in7BMwjJYHVQNuh3rYVmjHy71_2qZ5aG3jmXmXBarNI6euv-7sbUcIZR4zn4hMZbd2KLsjBdTvG5G8rw9RokBwjHm68eQQRkkRZSHTyXPqBamJhb0akuSbsb1Aus_uEi_gG-57lrUjAYjA3x1jLxCVlm6kvu1qVeEUKiWtAFX8DVzu-fxY_W5JAlTUa4evSNka29QScmpIPsQa3qMdB1BRJzlcramQalJWx1ma78uXMn3DPiLFdArgQ6LtqRvXC1WXsWVCkVYxlWRq1jxcBWmJfyEB4G4Rdy1VWlmq9IMbEt8IGOjIntPO2GF1f2GBdZfsZwN-cjtbIV5iXu2CBXPH1n91p0arhRIQ_aAFW2RXZfhZRxxwYMikLmMRJbGK5WGYRTEuVqlQcqrOBexzFcBX-VlGoQi4kGQccAMaRLKPMHKE6Z1VCw30rqMky_AaCxJR0GULYNiGRU_R8FlHF6G8T8GwWWAyNNynIozZcTTvAJFmT79_H9aXyd1NfVv0MgNPI8BIpQiKmOFYYLWmJXErSY_Sy3b7lgEoowFSBJsxu04K2-7HR9bn_bnCkBngC-R4G6XWcna7vKUmnNClPVjy94bkLHc9Wmy9GnWErUkKEBHgiwM3ts8Z3aU69D7yEsWRhdhNMUthnFLs563C5biN4Ys-IKiLr3vBE8Iqrll0UUGbhFkwW4Ae7Lf0LjgY__CwviVDfp4PTYDu-HaRwIsFhh0fQ4oDAXZ4yGYbZksIEMQzYg6jNv1dglw1_wWQBEjE0GMjsvDweBUHaadkBHeVya0QhIqCYtVFMss8qowq9dbIT2l4I4FS5JWjMShLfnyM_jZP_MWAb_BfOCAIXWTkGPq_cWQa2vZgqXO_K6B9T_KNUBGQLRS3IoGK86DXAO2QIaZ7-CFiW-YzmIm5r7qd6PhpiVxnvVo-Frqc_cVxmg8DnChu2nZBjCzHpZrvkPNsBnUGtcmczHZs2OVKcgj83zOjRkqPmbxuKyOSClRQSmU4nElvZRm3YrJYL-x-2CXLdNYgmPnURwp73mmhoQrjj2hwTCT8KymtJ-DLFjVgcB7CcYuCHlSaQS1BdaDoOYWJd2p-MCBed3WoFs-c4tLl0YuSJ2WIL_dlFMyrAvgc1hVRInXW3L4DEwEvQ6-YggDAm82NeoSWh6-OkOvkNiAGWNXnEp4Q9c1hJ40_vxBoo4RwCUMJSAV_aeHxZoFeRhCAMyirPLGN_VdvId8hj6K3TFfqbwA45Yy8rFm1lqxOz6lVWJSvpnUvMDO_97iwpO8cPHBNT9mu9ASX98Ii1TkdflUP3hI7lRSR_A2oEey5WM4LDmSF2CqRPISaV2SchkdPL-nCm85GQRRXqVqtQoL4Tg56wXNZPfY3g77953GLHdLvoLU0BVFTUhGrQQnhGi1bGw6T0WQmQ-bCiLmnRY7DZCqYTlgmHdQllKBCx2-MWzIlcqU4JVQ6cqdftZwmhzSo1pGdpO4lFlYqbg0fQWjrFMXacbiZ-oD2X3DLOJhGCMQj9y-s9aQ3fcpzZ1DZQbTiHA5kqiWJJm5QQCM6Lw9gR_FyiHBCdhVjI11o6Alu3EwFki1Aj6v6pkiGTpNeA5AUwnBdEFVMYp_QFPXL3mrAbk47f97G59DSBkgmjoH6QPauulKPPLC-OH93MidizDURY_45QIRGpDKGhQAlfORQ50YSW47SDcutDSozz0CBCTnkAaSmVoGLgkueUWC57YkckyZydrHEmeLFgRTMcKYAiukN2xs62HefnENGa6XnUI_JbEuv8MsiPz3wrjYvW4TsgpwGOQ6sJSl03AcsmdZ7wYrdCA9PWffO1WEINP3AJG6_aZWdUeBQMjbqc9Fp3thgokBeggqennTAzSiNSBezZpfjCKzrHtWQpYL7EAWZkBHA_G5Vrc-xXdq4COceQsCoqYjuteBN_s0Q7AGruFve6o3-wXW7GqBUFfrcbsz34PCf2C6Xre8IW0rLSjg8MGtrpHMHNDfVMECVgg4JHDhk7QG5L0fJQRWUAtG3t4IV08ydTIzSd-COe1zG6D8CYujUmNp8hrV6Zy93JbgljsEhWNr90BA4Xp70ljL1vX8HENV1xAE9o5eA0us_SHSgwMWYEuQqszLdPv9AAP-W8Q-SNoMYCK60hofAzTqIMy2BpkCD-sWrJ7ohW-65kA2DDKhTVd1TbeGI4u6xy_6iQ8ElC2bpg6mYQ53zGAGzOMjJZZR4DSr-9yf9TrGgfmgDOnPbgPw6BajMvDahCovIzHqoauAuEZynBY0CRHvrYTkVMKhagbsHQbnzHVdUT8MCkAB0AZGIvjuQaA3fhQySoivy1aO8GkzhwmUdxnkhgCLV8RiLFnSwBsAwyOAoFoprpK0THMquFHUmHXqp5D4yE67i7w8krBmGBVqCopT891u85Tm-aF1g-MBCdmqpDOkxcyS2JsftDdAi7TACM-xAXLgFWxZ33sGQxo6NeVKaW43StVxvrQE4WqJQRoz43eTJzGPH7oSlw_bHnxltQPzsXbpBGkgv39l7hatK_SBbm4ptOF-A-UISEojADCxTBNBcN7A-2n8wIrqKeMDGM8OPR0odau5LZ9QbWvA8q3eIKcFmBa8Q_gPUYi8QA803C5NcKOBzwWxF8lBLENr8vW6h4TZOYDapMzbEcMPoR50XvA11kSsgoAuvZzc5Nw32WMyUwmb7Bts2no0z3vcZHJfJumEMGBLIuBt0YGaiQADfhD_8Wlb8p2oIwdbvUAnUG_dcwtvHHAYHIRuOk2eRNfVaJdBrYLwKKTTKCzaGAxtXb51Tw_rg8rKJMqLIkwzjytnUx6Th3jyeIbL78u84GnJi7LyG84mNny_7vGjFnM6VS_lJ_kH2gc9J91Ep4HFJdn7gXKbVxuOLmwdzP0GVO1YU29R-W_4IDZVZ3baevRl3FDbLRXoZ8nFB2qKUHmJikt3e9tUW0NvQQCMpGqakaAjff3xiFTzKCnjMpRBztOJyX7MZBpnfvR8iAPTCh-qP1nIZbqBdjWv_6puTMMb9NM6u09TxmtwvQ3uAwZccLUpA_SbeXKqPe74Diy5xhbDY0_VrJZ6xuRsCDDbDhZaPTYfEVwiGD383s-a4ALjAJuiWBSuPOE7qiZhQQWz52GswP8P3c7S8En2nROOr78ekU-VqTgFu-NC-jL0bKzGyucp8zA1fYnqj6evakWDB8NkrzYiaRAvZaXkP6xd2ZMY45niHxy99fVqXwXhAgC6Pj7_6ZPYjBcF6mbkM_TZdM5xZ_OIsRq7LQ_jMiqKNIgnFDSbtLHbPmVEBrz0EvMiW4kzmn1hU7ELm3Lb_MXEyBkmQVfigppLn2Y4367p4sLSxyoACOBJFhaTTw9gZHDfkXkurR1aLLugfsKWzyqIi8nM9z4lrDvLGhDtPCzeQKaREoVUMvblp9mE0MNe55tHe47x1T5z13G9MObpw_IBO-zXdDlkj-9OFg6IgdZTQ8hietA9uyVmzAbbgNOygXd7B0G9mLzbCl56WGovjCts2Xva6j2sL8yVJrJRTDTtHaYpZ55hmTnQICjtKThnr63DM65L3D8UMyU3d3zbtxXiIJivVqEIhZxKyLPJK68Hjx-Zwuq_S4TgVIblmxFyFYumpe2Uq_rjQDMM6O7gA15CinRYGcJ-K_nACe1Sc4fvJgbDMx3hQDc5RLUqIoTKU1ZdbWkFyTri_WOZFzJJs7TyLY7ZpNfkBh8zrOUQQBkHPEpBP3ns9pjNb9k9njKCNdce7C_6RFu7ZkkNGmmBwUHl3MMHkEhPXTOb-BrFJi85Ax5rM_6zIFOcWLzwFWeTWpzvMcy1TSpwMcY6Xa1qGFu5X2iGGAlQ0vtHD9joHEuQHyyEztkAtz3asHDUGA_k8YSF9vviOgbCV6syK_NY8jxwwpqNsU09r0dPolmdJIQMaj_UtFC_loMHFtiyMbJ-qBWKVynxKYzy9DONeDkqqJ7F9rrVU2dBUjPK1kGtqagaTXBtMqhWgqHZ3MVjEv9-S7DNHcm0KbEaQoMy3aixMgfnHLc0eIap8qauKix5TUUi5xepWuXe8nVE27un0pvFgFMdAHxKB6_bgpJHYFxbhl1HTtamZXxE0kFZRGGYVjzx2c9sFHAy_T8w1meXBgeSBmWSqygsfSY3Tfr5myOPn9qb5ZW2P0ndTxtOr-kOLqZVZA-m7w-qYgtm81Rm5kUgm4Wg12ssnpnxO6qxIjBqJ0HYMQcTfx3V1Ao_J05RmrYD0LJfv5klp_7Lo_BURmme8JAL7zNn44g-bj1-tNDxzUYP1TvH9Vd0bNXdZW2xf7Q5EvpZLF6CwV4MNSIh_NR7UxIruaobhFQoOpOa6vubwrPOnzbdCapomaorfjLH2ejCtcl7azQrEyOxjGoqOPAdRMwLD0-d8IyX1lzJAXMmkrodE8FGDiVinnsWVS-dkBdWMZeTBM16d8ZYlhSDZgBF-wJdc4uOz4z0IHZsnBh8XEFl6RREP_SLpNRvIf79c3jMkstQRWByknOfws3GQ-fzSn9g0NO3xFdRWakwNJpnNHGa_XQ3-p4wxenbrsbZAjca7MT0Y4stD4UNfQwaGM3qdta4c8MKZuoGlHpNYNs1mmjMpJ2QAI3mQNDvpcEIrnADm9-YT9784FNRpwRU8ga4NSyNezY7S943t0tErrbfZeZniLV35o3cHIVTtCNjLPEqWUmerqqVTw5nc6x7bvNxE6lTScnUgy5Mn92jDLPQLIy6-hDVwPfmOqZZDrDIAUMsscLXCe0dd7Lec2aINtnzlMSYxoxx2tphHfzBZhkHQ12ks32PnU_w22ZQaRpJsE5B4Phdi6gCPQS_8SNN5sR2GRuTjfPTrpIAlGAQYH-pIZ_SHMHJJ0pj2loZyky6in7L_O4qv3gqdB_6EBhOh3KjbX5alYb3gHFr7CjPLOLYXEGcVlGkMqkyj85mo8SzuYJvmg12RQmRxGkuCxUKnyTNxoWnhv6j53-dEJY4jGirmdp09d9JKmOwHwCnyp6GSQ2W9nI8GAZxaRBN05rOFDyLSS2FfSqGYVWEhs1ck35svS_ykQZ3GeczJAcVW9Nef20qT3tgkB42U1R6sjgzPidcmIGPh050jWl1IwUDTSodpCqUSNfqnszHHIDSH9OmdmtYgGdcra3A-nXmG1i4D6Y2mA7yyxFi8l5kWpCBGrVFt6nvZjaAR63547F-6lwhDPhlfajRfYMRb2cDhXfagb9-QbW75699SKDL_62P78ELfTz7lf5yCI2UHn5-8LdBZp_buor94l0tNryv2M8cFP7_5V8OoULCY_9wyCouy1VZZQ-M_Gszvfzf__lfbBoX_-Y7Bw-9few2bLBKeRU9Gz2YQYLfWXdgBdjYIuyA-bNN98FS3wvUjQtle8oyksvr6D2AyUMfC9ojGl5vH-TgARX26sFLivIV7QWkyIPDPHT8-xd7Z9V6Ih8MuRUbMkHICEGXWwNZR22tkSpiM5O_uFsd0-ZwjuGfz242t34zk8bMGiFYBMHa4f5AuXe6AGaaW58pH8ypzuigYsSdIh7myb6Pco63Dr75FsiRP0pkuDe_3jG_2jC_8vH5ZCZPN5Nvv55zeD0l-nL_5ZOv3cR5lus2Cc5FxiKRcR5HUcVVHGAPSGSlEFGSR6swV1G0KhPOM1HwVQFZVRhB1pOLJM9pAPy-89x32ya-DKJ7btv4v7l1um1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum1zum3zcDswSaNipVQUVysfs2Zj7_dp8h8YXHcdppwnSRmHqZS-yDebZZ9NyDx2Gr3_MCBKxTlVe1HAwErThRrms7rv0cW8NxhM9lgg9UjWIn53m0J388lbnxVNGAKDC4IXdCPoCo2i0VUIMs8pTZ-XsvaVa8Ovpcl5ZUUTXsCCue4c3pZAg3FwV34EaWp2K6m_ZlR3D-5Yf4r1mjve7Ncv8O9_AFf3uc4)
