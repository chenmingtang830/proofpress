[//]: # (ob:b4481af4)
# RelayBench H4 Phase Zero readiness report

[//]: # (ob:ab4ec62c)
## Outcome

[//]: # (ob:259a6317)
The isolated H4 C1/C2 Phase Zero harness is technically ready for Richard Tang and Tommy to review and freeze. Scientific freeze and every real model/API call remain machine-blocked. This repository contains no benchmark result, Harvey LAB evaluation, model comparison, or Proofpress efficacy claim.

[//]: # (ob:77de4c9a)
This repository-native report supersedes the standalone RelayBench readiness report only for the isolated Phase Zero freeze-review candidate described here.

[//]: # (ob:e3e3838b)
## Integration basis

[//]: # (ob:657f1545)
- Local branch: `relaybench/h4-phase-zero`.
- Stacked base: Proofpress PR #22 commit `10ee8c4c9a6d56dfedf563a0679e6a5bb167fa0a`, because that commit is not an ancestor of fetched `origin/main` at `a5e5ea5e3174c2c51982ea36537cef362a973ce5`.
- Richard's `studies/LONG_HORIZON_EVAL_RESEARCH_PLAN.md` and `studies/LONG_HORIZON_EVAL_FLOW.md` are unchanged.
- `proofpress.py`, `proofpress_evidence.py`, the portable artifact specification, and root package architecture are unchanged.

[//]: # (ob:c5a4ddb0)
The original target root was an unborn Git working tree containing untracked human review-build work. Integration occurred in a separate Git worktree so none of that work was moved, overwritten, staged, or committed.

[//]: # (ob:3ee8b27e)
## Included review surface

[//]: # (ob:4d06e951)
The packet includes the runner, deterministic worker, adapter boundary, C1/C2 definitions, H4 controller, parity audit, cold-boundary evidence, deterministic scorer, schemas, tests, scripts, synthetic releases, exact Harvey acquisition manifest, proposed intermediate rubrics, frozen-manifest candidate, protocol, claim boundary, alignment analysis, readiness report, and the single `PHASE_ZERO_FREEZE_PACKET.md` entry point.

[//]: # (ob:0240776a)
It excludes dependencies, caches, temporary workspaces, generated result records, Harvey binaries, the protected Cold Handoff ZIP, dashboards, videos, and unrelated local projects.

[//]: # (ob:3b122ff0)
## Harvey source integrity

[//]: # (ob:8986e7c1)
The candidate pins Harvey LAB commit `7be41d57fd5a6e97b5f246a029e810f83d09cd96` and the MSA playbook-escalation `scenario-01`. `HARVEY_SOURCE_MANIFEST.json` records the exact repository, MIT license identity, 11 upstream paths, Git blob IDs, byte counts, and SHA-256 hashes.

[//]: # (ob:d7f75cc8)
The source identity was derived from Git objects at that commit. The executable local test-double releases were not constructed from preserved Harvey files; they are explicitly synthetic and cannot be described as Harvey material.

[//]: # (ob:73fb0082)
## Scientific-control disposition

[//]: # (ob:b6a76f6e)
- Active scope is H4 evolving negotiation state, C1 versus C2, one cold boundary before S3, no merge, and one paired TEST-ONLY replicate.
- Clean continuity and integrity faults remain separate and unexecuted.
- Both arms receive byte-identical substantive files; only the C2 bindings carrier and verification affordance may differ.
- The parity auditor rejects changed common bytes, unallowlisted paths, and carrier content beyond the strict representation/binding schema.
- The controller rejects missing, early, reused, or third-worker boundaries.
- The scorer separates legal quality, unsafe state propagation, state consistency, recovery/false stops, and operational cost.
- The Harvey legal evaluator is `NOT_RUN_TEST_ONLY`, and test-only episodes are excluded from every denominator.

[//]: # (ob:6c7dcf54)
## Approval-blocked material

[//]: # (ob:f9adbd6a)
The MSA matter, complete S1–S4 release chain, and 16 proposed intermediate criteria remain `REQUIRES_RICHARD_TOMMY_APPROVAL`. The upstream Harvey task is single-stage; the local composition is not an official Harvey LAB task or score.

[//]: # (ob:0551d679)
Provider, route, resolved model, reasoning effort, sampling controls, tools, transport, telemetry, runtime checkouts, timeout, retry rule, budgets, repeats, exclusions, and analysis remain unset. Provider fallback and cross-provider retries remain disabled.

[//]: # (ob:dbefabdb)
## Validation

[//]: # (ob:4c59e0e7)
Validation on 2026-08-22 completed without real calls:

[//]: # (ob:2b452c3b)
- Existing Proofpress Python suite: PASS — 65 tests.
- Existing Proofpress Node suite: PASS — 5 tests.
- RelayBench lint: PASS — all JavaScript and JSON artifacts parsed successfully; no forbidden artifact.
- Fixture/source/rubric verification: PASS — four synthetic releases, one exact Harvey commit, 11 source hashes, MIT license identity, and four approval-blocked stage rubrics.
- RelayBench tests: PASS — 16 tests, including changed-substance/extra-information parity failures and missing/reused/third-worker boundary failures.
- RelayBench readiness: PASS for TEST-ONLY mechanics; scientific freeze and real execution remain BLOCKED.
- Frozen-manifest verification: PASS; every listed local file matches SHA-256.
- Portable Markdown verification: PASS for every added Markdown artifact; exact command output is recorded in `PROOFPRESS_VERIFICATION.json`.

[//]: # (ob:a982a623)
The lint count includes the Harvey-source verifier and claims generator added for freeze review. Generated mock episodes existed only in operating-system temporary directories and were removed by the harness.

[//]: # (ob:44387f71)
## Remaining human decisions

[//]: # (ob:becc231c)
1. Approve or replace the exact Proofpress, engine, and Harvey revisions.
2. Approve or replace the candidate MSA matter.
3. Approve the S1–S4 release composition and intermediate criteria.
4. Approve C1 native continuity facilities and human semantic parity.
5. Freeze all provider/model/tool/sampling/telemetry fields.
6. Preregister formal runtime, timeout, retry, budget, repeat, invalidation, exclusion, and analysis rules.

[//]: # (ob:ba2218db)
C0, clean-track execution, integrity-fault execution, H8/H12/H16, merge topology, and the 72-run pilot are deferred beyond Phase Zero.

[//]: # (ob:430ce8f1)
## Stop condition

[//]: # (ob:86cff10d)
Stopped at a validated local draft-PR candidate. No real or paid model/API call, benchmark-result claim, deployment, dashboard, video, archive, push, pull request, merge, force-push, Proofpress engine change, Richard-plan change, or protected-ZIP change occurred.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzhlMGUyNWIyMzg3YWQ5NTc5OTcxYWZhNiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjBmOWMzZTA1IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8wMDhiYmE0YjA4N2Y5MmQ0NzMxZGY0M2QiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzUzMmRjMjEyMmI2ZWQ0NDEzZjUzNzJiNCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXOlyG8d2fpUu-EeSCkDOvlC_KJqyeK9EMiTtlOWogF6JuRrMwLNQglWuuu-QPOF9kpzTPRsgEpRI35RTNS6bAgc93afP-p3F-jyhRZUoyqt5IiZHk_V6HklLOj5z3CikIvbDOA5tqmgwmU5YLjZzkdzKsoK15ZI6fnBEHYsFwvNjP44tGQmhIip8FXk0sDwvVqFikrpUKKlYbFuMUh7DB8Yiz4mELWBfkZQ8v5PFZnL0GX-p5hW9hRNSWuFRU_jAZAoPfpJFohLKUkkKeZeUSZ6RJazPiw1hG3JZ5LlaF7Is4Z015R_orcRLbT0u8r9JuG5d4IbLqlqXR4eHt0m1rNkBz1eHfCmzVZLdVjS7jVzrcOvtQv5aJ_B5XpeymPM8K2UGvKiKWv4-nSwlRSZaKuautPyJeTKXd3oRMFfOLStijHrMikIVO8ILXVsoz0UurPOiwqvN0ySTQHkrkXTuu47gju04LJDC82xX-W7oMM9cp6Fuzum6rFO4sIN08rwQ5eTol8-T5vjPE5ByXpT4yXwtxZwBy3-ZXKxldnxGTnIhP03ew0VapYDzX56en7x-e3z11_nV6fH3Z-en19fw6fLi6uZghVR_i_7QqioSVlcgtjmjZVKiFslUzWkJ7Kyk3q-ulnmBRH5IMtyy3JSVXME3GV2hNLeIncL7JarB5Cir0xRI50uQmzQ3Z2nOP8ArzPMioAH5BSKr5Ce82JVM6ealzPiSvPbI5ZKWkryTRQ6aRQVIoCzhE8gEXmoooUJoEteoe_IjPPmOfO0uqMXVZo0XWOpvbie_T3sKKfMkDxy-ReFFXYFCyr0EfEf6VXv2d_yYBq4dfuv-N0tJkjJHQxR4wRP78MQZXnNJC33JpCSV5Mss4TRNN_r2PUVrWtAtcqQr3ciN2BY5Z_DhtqCoHcRox_6L37d-DwsCP1S27_lPP3NG3uRwPcIKCvI-IosChc9Q-IdLb7ZGrsx-A64sDv4rm5HrCjwQsA32lUekJy4Fh7VFGfepJwSznk4ZiikvktskA_IqWtzKioBjqMhHWhKakTpjeZGRHxJ4khewzS2pCikJHrdHTK6UEXNCuUMYT2sggJjTSVkXYP_yUWE99NYekXnCCmTs2889H9mD4QC4kpi3QVvhWVFnmSymRMhKFuDzQTAJ1xzCp1TQdSX3sMdyPCsMA_pc8s4qIj81ZAkJ7k2ASiWynBJOIRrBn-AAwYdQiHJIXAl3wae3MttHnssgYii1rVavaXEnN6TM64KDaWslS6rNI9J7-K090oviKJAht597PkqP00wkArwQWSdZ2dLz5vglqPBqBWq9CJn0bAE2LnwKShMyXzlesIc9IlShz3n0R5DXrgfBVbBcm50ArHIHeqCKfKUtL2cIPMAeK1A--AGU7yEvdBUDsOBskXcNagEnqITP8GGRpwTg0jovE_QTjwjx0Zf3yJIFNAxUIP8gambkmFfAHQK4b40RBmOLvMvTO3RNmbzNq8S4vrICoU8h7hDAh2VdkpM9jjTgoeDK347zx2vASHc0nelVIJAV7FgkNH2EXfve28MpFVPBxI5TeBINqFhvr49xbYX-CPRlnYKnItf2P_7-39ceeJhUYiAGyJNk4K8yQeyAwEkggr1-y_dtEYTx80kEwH0HSg_EFXmNcgIgCkLEtwGepfg7LfMMhSqVAhQ0JSWFW-CDfabJpKJMbMODn2iKHuBxPd9auC-6cD8GrBo-4ZR-FYF_HcsJZlY0c5xORoJ8hIwCeIIcSAmCovJoz40BzPsOd59y4xk5_YSBC1ja5z_kcgPHg_nUSQXg4_L4-pr84-__Q3yfYEpVaoCi39tjTjSOHBo47hOIQt0FKaOTq7OdqGt87KzxmXc6pZOFVl-e0mSfU_Q8yCpUaO8A-RXoP95_Wa8A7AjJdWb4GH7c994-Vyg5d1ybP58G-6BxMgjeME1IIa5rFslPkFENxDklMgNwJ42RIwP3iI1Rx7GjHet5EoEnFngd8DHZrCoAPgFZkuvsbdqHxpmidVoNv3odHb62nX1SdC0uI7UtxesqXyMeFV8VynYX74MhAVfKtsQTT8OVa7BnCNiU3Bnlh19TnQmIgqpqdnnV45MDcp4bmweR7vLg_bRNxicYzTAN5rDWJL76mzaLlnM3VqEIqc8sZSs7jLjrQc5P0RizvNJ7NvUC0tQLIA5I_mGdJxrTw4n6JEyL298wK36PhYY04ZvBDsPiw2ATXdZ4Yl2izFU1VyALWayLpCl_lMw-kiLyfY-Hkgnuh44LQM1ngbAFp5CfKm55YWD7sQ_OUDGfeTz2hQ2eKBAKcmQL74-YQJcxjLSOnADyfnwy6T3xje0dWdaRG_w7_LQQAzcc1xYcxlGsFKhJ__TzP6voofXQ1CMgQVwiMPcks2CZ8ny8jt5jUKJoVPTZtYXmNEZZEAd-wGPanTYoN7SnPVJIaDYDGbgh9wLXtuN2s0FtodnsOVWDDQGcQK4SADWFIDcUPBb6vBuA-RtS5W1ahc8UpLC_gcX1OLR5pL-VWFA0pqjByOHx5ZkOxPAMfSEAHL4ELraA54DcLBPDUQCwWFFEd0Ex3chyorP8FS0-IMQBhzcd5iAS_EJNjffTZ2kcQAvgATyB6wwCM-AguC3fmFh3cI-bbFnNpU1pFNmOF7WsHtRNerl9ZR2k2dZGXygdh6qgk-CgNNJs-6xSxxCGXJHvDCzSSZptSRlxsGkaCB8sWgrlBy61AIzKAHwds4NQUYsupsBwTutSdqkSvp-gKCosaABVEsu-JFdEyQqcliALUwE5ROEu0F8vqC99CT9AOT3ucN8GQCOpG4CX4lK5gUPj0OXSN5dodO5fSrIoq1pAAn745uL8h_nri6uzdxfn89Ofjt-AF7g-Pb46eT2_fHN8Ds5goXVtzwuv3lz8p1lXSFJnpjwp9IGLvnh7sN7AnQcP5hKBNdzSfIOgoPP3rfch5RqiOKqTUT2kRFd9mtI3LAQNBwOr6kLunH8PfmgURLBIKc_zVeioVkEGFaqBiT-14tQAEQCGhVEbA0mMZc9YnaRCv3Swpdo553VRwGowXUpKifYCyVB7gt69zEFBMolaofUGv9AUrQBkCTBF8AkfAbVUEtgFYeRWPywa_aq2-LJrj47jWi4NWMApa_kyKJAN7fEbSl2tVdqW4yum3Jg57eaD6teA6U-tYxWEARQXtNhMG38sJMRnjX8AX4KXbnL4FN9B51VtCAWtrjDzTMWsfZ20mrl7HuTyBb5bgjWuqK5aQaaBvxfJWn_YZEAtLm0yV8S1Guk2vpTyX-vEVA_AO2eJgg2mbUIrNOYsVlIkKPeiZkXCYQdV5L_JbNau76GYfrPKgfipcbYDDgCOu81WEDVAV2m6Aac5_SKqGoNC_pYgLbC7xeXr4-vT-bvTq4v5q6vT03en88vjk7-e3mj7hs2AORo57dGiOFSeFJz5VAdMLehBHbEtIj6jIljoqGuiFGn6QF20YmCvhd5IexTgD3gHWH4CEoY1mciVIu_OLkG2QC_LqX4ZBZ6Xhh91hqGgh8BNP63cF8kCbtuh69h-YHWW0xcne8v5pjJjs7nvOIKFduwy3XHQmw8qjwPLeWoNkVpOLCPbUpErrJiLOFh0moH1mTVGxjz_MJMlMMQ4q0XJJXI6n1n24oAsXh9f_XT68_z64serk9P52-Pzs1en1zcHfwOAsGiFNMj8ehAyJW_PbgDhw3ZlX2CcEtsm9boEp0dXYKzVEqSDnhCwDCNn38NvbFNJk303grt-fTxz_IAg3-Q-cTGA6Lb0A4ibnS8aFEsHHH1q2ROYjWhLNlmjSWK0NqHLmIm8Nh1e4yTIRwmhCwM_9lshJ9Eaq_fHUCkLPK6RpkpSWb5ATm50wJOf1sC7pAJw2XsfXWmgGe7IJBCMDophitcpRVv72sMlEXoBZBFByLWeaS4Nara9Uj-l7NqcwaVHRRC6lpKdsxhUYjus9vRiqgPhL5PawXfeEZgCEFySa3eKyHclIbgbFcKla5pgEL4B9Z1dnL_5WdctEIJIjWlOsFygQ0mS1TqEZKK3ZKKLBWWLwLsgbhyL0YYGHL3MqyWIcIWLucTroUbPjK6hqpQ1g_tk-uaN2PMM5IxWBNENPB2yswRJF0VbXzLFJoOXCMWKpEAkCfLegFCUkoU-28TZPgLq6ozR4gY_aS1GvA00gX3VEETS_CNCKfiusUejZuZwXXnIUN82eRtUKohf2tRRiQEVIVGHDdlNEO2o6WNzR8kqKTEuQQilRbrB8AVw2cCZapkUYmbifytWcPrdbiZSd-wvSSpvgaO_1hAW0bnUWUmVNOqiwy-9bSCmeYR2iFfNuD7XzG4cKpqW-FK-bi4P2miwG1ZA87Lqzm-szJzaJE9ANmju4vziZn714_kc9WuO-rVowjA6Bi1fuYa0CgOjse8Ga2l3YFI-0JAcQAluuQfmBnEM-bkV-b6UXR7U9w96-_3GPkAb8ywRR5blBEHot9sPWgMDJ_r0Ev8OIgIvpglrrWtxdfofP55BwjK_OjuBAPT9_Obi7duf58eXl1cXkJosjA_uwkgjlYqWH1AUBvTMNErWHrVx0Uhj47wGCVmOaS0wZRhW9U4gV61u-zARo46Qlut5XhfCBz2KhlfP6TU05oOwJzd_QF5bGpBXAYtXssJQCzi6SlZNIQ0OwYXwO3zC3RHeFXUKJ7NaQL6jIeNa0krDWNDD0kBpFFKLKltZgEVJiHntHcAPpinDkqp2EkVelrN1-x2eBNbavgrBAgPk3tQk4J4fYj5r9RG776H0uvxYa6TdT0RcCKVE7HTKO-iWfNEJeGYTpDnV4q6vIhrbUUS72lLfF-mi3bPaHTvvnYPqfPnW4KVBDQ77GYNVWEn6C72j1zq90YL8y_XFeZedlxhC0EjLmgM4L1WdppsXGFFBOVkiwE11a_VRr5JPmKgfGlR1aBKcrZA1OF3BonsTKozRW0mVwVsaMTZ4zSDAh5Clrqzh7nTX8WlX0CZeu9zRLBsQCG6qyf9MqqrN0ATPWRO64ZIg04LOkgxYsjKq1MRdRZMUmFFqcppQd2hC3OF94a1_Y5ewLq1riMPyYo9eVhKJgvu8ADd1XxlRq27X3WiN8uWbC0j8vjdy20lAv5TYiyYyNfjA-FHELOj4MZ9rwbne77Kt87ylxQeRf8zu0wG8hdlUF8H7ta1KvWi0AMWvg3FdrWtdQmuH_7CQsoBQcPHq8goL3D-dXp29Ojs5vjm7ODeZyZ7w6doqEEEgQuYEXVW57xcO4ttT24Blm83CTc0d8c6NZExp5YD80CW8qxwbVC02kJ8MqzVigHs2UCS7nZlxwkH-LADP4mBk0iibzjZAzFgxwqFSpLWpV-9xwTKAvFBK4TG7L-D03creBX9j17GvD3mh5_tcuF6XCfSNyGb75zQU5aYbqUUTch7cqk-je-QCL7j9C7jqCwAzQA1tSvAFcoFtvH4bSFMAxCG8H6QToNoJgNRWWIaHJfAUs4LGecA2_gGYpbHhVNcodGg9NI0AxACHLTY47OI_WKRMBV4-wEgNanCLSlQQ7ZzSFh3sYoIWDrRoAB3eXRcaB9BgFxkAlCj3WJhth1RyN46F13eJ-tZuI_LntGjhv2Bq8jvARes8zW83fdErdGZwY7JOUkR4BSbKkB9h7tckMX0_Z49deEJwO7a5T1V3i0H_d5Amf0VLt_U98DKzbeGCMnQln77LO2jxPrVxC0mu2OkaTfsW0Kwprmk3hVXQdZpvsJg4qJo1RbOpqcHfYTGyLpf4Uzegfq11abPJrUHBuJyZBcNWkTbRJmpO2_7EDEwx6x4isW0Vb_bu7LL5oquWfyGa978jJ--ZCQdbrB6YCNdj5qLmD369d57cTM3Lst-9rfebpwX5166ChNlEY63i3_50o-gAf3Rv_ZFJ9EnfLJttNctmSd_PmDwwqx6GQmKD7Nsntbeal7PGdZpSNmBQCICAnZrYi-hL0BSxIiKle-YUTAh-iLIdKpqBhGMdpXVD4gs6TG1K92U0ndul9i5RWFHdKqJfGttWF3W220XVJLfs-jz5uNzomRfUyscJkjvtdYMxZk37ZpfWA5TcV49xUMGV61sejYQN_zgupVYUeVbHteF8xnA2YTiz8fnPrClfP7eyO7dh_37_VMZjIyp_yBwKdQI7FJbvM1tQKwQpeZxDWAkcaceRpaRrS1fEsZIOEzyGrT3406NuwISMreiB-9w3hmIfuc49Yyg05rHvhOE4hjKOofx5x1DAdAMZcfwf_LqqzMDzdKx-uk_ZzdPbt3TupnQ5eyDHB_10n5f0HZ2l3Ft4HEdsxhGbccRmHLEZR2zGEZtxxGYcsRlHbMYRm3HEZhyxGUdsxhGbccRmHLEZR2zGEZtxxGYcsRlHbMYRm3HEZhyxGUdsxhGbccTm__2IzVf_ZTugnhgx9YhLvWISpfjLLxMfEXvgT96_3_Es98_NDI67Z18zOnOSF4UpE6Nf-BJ1V7rsriN8les1SreFctYU5wJ_ptdooN0gkQfGYpqzmrmYnabr_bs_kAYYir5tIGbPX4B670BMNyXx-EDMP1OuXz_W002FdKfsDLr0cx__J4MuviMhPjAaqsCVHhMytGXsSur5rrClYl5EVRhHMoxpoCwviljke5a0fDDkMPLZw1e6b9bFO3Lse2Zdur8Sd5x1GWddxlmXcdZlnHUZZ13GWZdx1mWcdRlnXcZZl3HWZZx1GWddxlmXcdZlnHUZZ13GWZdx1uX5sy4spIA5AF4xK_6DZl2CcdZlnHUZZ13GWZdx1mWcdRlnXcZZl3HW5f3v8O__AqQzCNY)
