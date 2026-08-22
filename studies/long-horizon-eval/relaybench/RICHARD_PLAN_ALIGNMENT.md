[//]: # (ob:3ebe8def)
# RelayBench alignment with Richard Tang's long-horizon plan

[//]: # (ob:244d7d52)
## Source of truth

[//]: # (ob:ca11fdb2)
Richard Tang's proposed plan is canonical for study design:

[//]: # (ob:0845e41a)
- Proofpress PR [#22](https://github.com/chenmingtang830/proofpress/pull/22), inspected head `10ee8c4c9a6d56dfedf563a0679e6a5bb167fa0a`.
- `studies/LONG_HORIZON_EVAL_RESEARCH_PLAN.md`, SHA-256 `8189dfd932cd98b28aa1bc6728b3e4543520ebba2821a36acf3ad1c709a7dec2` at that commit.
- `studies/LONG_HORIZON_EVAL_FLOW.md`, SHA-256 `41acdf04bb8bc33a7e5fbd87dfa713c0b733c793b40264f0d43c64a8a51b4dab` at that commit.
- Relevant prior mechanism study at Proofpress base commit `a5e5ea5e3174c2c51982ea36537cef362a973ce5`: E15–E18 and E09 in `studies/agent-handoff-artifact-provenance/ara/logic/experiments.md`.
- Relevant engine boundaries: `docs/PORTABLE_ARTIFACT_SPEC.md` and `docs/ARTIFACT_PROVENANCE_PROTOCOL.md` at the same base commit.

[//]: # (ob:0403a5cd)
PR #22 is a proposed research plan and flow illustration and reports no benchmark result. RelayBench implements only a test-double H4 Phase Zero calibration layer beneath it.

[//]: # (ob:e6cbf462)
Integration decision: the Proofpress branch is stacked on the exact PR head above, and all RelayBench additions remain isolated under `studies/long-horizon-eval/relaybench/`.

[//]: # (ob:83b35dd0)
## What already aligned

[//]: # (ob:978dbcb5)
- C1 and C2 were intended to receive matched substantive information.
- C2 added provenance binding and mandatory verification, not a substantive answer.
- Provider fallback and cross-provider retries were disabled.
- The harness recorded hashes, transfer inventories, verifier evidence, telemetry, invalid attempts, and TEST-ONLY exclusions.
- Missing or malformed verification evidence failed closed.
- Claim boundaries already denied truth, quality, authorship, identity, and external authorization claims.
- The adapter surface kept provider attachment separate from the protocol and scorer.

[//]: # (ob:8d4714d5)
## What conflicted and is now superseded

[//]: # (ob:63fe1365)
| Previous RelayBench v0.1 | Richard's canonical plan | Alignment decision |
|---|---|---|
| Three repeated cold receivers over one unchanged package | H4 is four consequential negotiation stages with one session boundary and no branch merge | Replace the active three-hop chain with a deterministic four-stage controller and one enforced worker boundary between stages 2 and 3. |
| CURRENT, MATERIAL_DRIFT, and UNVERIFIABLE were the benchmark cells | Clean continuity, evolving negotiation state, and integrity faults are distinct tracks; evolving state is primary | Use only the evolving-negotiation-state track for this H4 calibration. Keep clean and integrity-fault tracks separate and deferred. |
| Primary endpoint was a local `CONTINUE`/`RECHECK`/`REFUSE` action | Principal work product is the final contract package; local verification disposition is not the benchmark result | Score final-work-product rubric inputs and end-to-end state consistency separately. Admission status remains verifier telemetry only. |
| Artifact mutation drove the task | Legitimate negotiation releases drive the primary product track | Remove deliberate artifact/capsule corruption from the active calibration. |
| Generic artifact-plus-memo fixture | Public Harvey LAB contracting matter and filesystem-first harness | Use a pinned Harvey candidate slot and preserve a future LAB adapter boundary. The local executable fixture is explicitly synthetic and TEST-ONLY. |
| One fixed visible Markdown hash was the parity test | C1 receives the complete ordinary workspace; C2 receives equivalent substance plus Proofpress representation/verification | Audit the complete paired substantive file projection and allow only an enumerated C2 carrier/verifier difference. |

[//]: # (ob:d9bc7bd7)
## What RelayBench had invented beyond Richard's plan

[//]: # (ob:04b587c9)
- The three-hop A→B→C→D receiver topology.
- The three action labels as the principal model output and endpoint.
- A deliberately corrupted carrier as a coequal study condition.
- The rule that receiver output never enters later work.
- A capacity-change toy fixture unrelated to contract negotiation.
- An ordinary-arm `UNVERIFIABLE` cell with no observable carrier.
- A single pooled unsafe-continuation rate across materially different failure types.

[//]: # (ob:c9cac741)
Those inventions are no longer active study design. Reusable mechanics—hashing, fail-closed verification, output isolation, adapter metadata, and TEST-ONLY exclusion—remain implementation utilities only.

[//]: # (ob:52baa5c0)
## Recommended H4 matter candidate

[//]: # (ob:0276ba8f)
Candidate, not frozen: Harvey LAB `tasks/contracts/commercial-vendor-customer/master-services-agreement-playbook-escalation/scenario-01` at commit `7be41d57fd5a6e97b5f246a029e810f83d09cd96`; task JSON SHA-256 `ef7e3e968910508fd43b3f90708bdc6cd013f2cbc837ae921175ebe5b2d4394c`.

[//]: # (ob:2ebc0d61)
It is recommended because it has seven out-of-policy issues, explicit delegated-authority rules, a v3 counterparty redline, negotiation history, business and legal emails, deal-economics and authority spreadsheets, a competitor schedule, timeline pressure, and a 72-criterion final escalation memorandum. This is closer to Richard's representative longitudinal matter than the generic fixture and meets every stated selection criterion except calibrated difficulty, which cannot be established without real diagnostic calls.

[//]: # (ob:6c8acd27)
Recommended release schedule, also not frozen:

[//]: # (ob:3658d4e8)
1. Standard MSA, deal economics, and exclusivity window → baseline issue register.
2. Counterparty v3 redline, negotiation history, and competitor schedule → updated negotiation state.
3. After the cold boundary, business-case email, outside-counsel assessment, and authority matrix → targeted revalidation and escalation plan.
4. Escalation-request email → final escalation/approval memorandum.

[//]: # (ob:533a07f6)
The existing Harvey task is single-stage. This four-stage composition and its intermediate rubrics are a local Proofpress long-horizon extension, never an official Harvey LAB score, and require Richard/Tommy approval.

[//]: # (ob:15da622b)
## Unresolved decisions

[//]: # (ob:07daf0be)
The prior readiness report said “eight unresolved freeze fields” but described twelve ambiguities. The reconciled manifest contains exactly twelve classified freeze decisions. Four scientific choices remain approval-blocked: upstream revision pins, matter selection, the H4 release/rubric composition, and C1 native-memory policy. Provider/model/sampling choices remain provider-dependent. Real-run counts, timeouts, retry rules, formal analysis, other horizons, C0, clean-track expansion, and integrity-fault execution are deferred beyond this calibration.

[//]: # (ob:d67f9c0c)
No provider or model setting is selected merely to remove a blocker. The synthetic mechanics fixture supplies no evidence about Harvey difficulty, legal quality, model intelligence, or Proofpress efficacy.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzNjNTA4OGQwNjg2ZTAwY2Y4ZmQ0MzkxZCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImYwMzdiNTE5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81NzQ5MDVjZmQ3MTFmODJmYTZkNThkMDEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Y2YjM0MjA2NWM0YmU0ZjgyYWU1MWUxYyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW9ty20iS_ZUK9cPMxBIiLsRN_aRWy23P2JJDlntip8dBFaoKItYgwMZFNtt2RD_tB-zuy0bs_lx_yZ6sAkBQbdNaSREbE8sHd1AkUJmVlXnyZFb2hwNeNVnKRTPP5MHRwWo194RvR5G0gyhQti3SKJUzL3bkweQgKeV6LrNrVTd4tl5w1w-OPDeQCs-m3A2Fw4NZKDmPXNeTQvhByrmMw8j1pYiiVMVxHCo7ToIw9XjEI8dPsK7MalHeqGp9cPSB_mjmDb-GhJw3JGqCD4nK8cWPqsrSjCe5YpW6yeqsLNgCz5fVmiVr9rIqy3RVqbrGOysu3vJrRZva-roq_0Vhu21FCy6aZlUfTafXWbNok0NRLqdioYplVlw3vLiOPHu69Xalfm4zfJ63tarmoixqVcAWTdWqT5ODheJkxNT2wsR34gPzzVzd6IdgXDX3w1ls-yKVoeOkkZvyQPowtkOalVVDW5vnWaGgeX8i-TwNEm_m2oEvZoma4TWufEc5wmyn024u-Kpuc2zYJT1FWcn64OinDwed-A8HOOWyqumT-VnJeQKT_3RwvlLF8TN2Ukr1_uANNtI7BZ1y08pM1dO8LK6tRVllv5SFpW54Pq1UzteJKsRievHs5Onxxffzl8-Pz-bHz5_9cPbi9OzycElO879xMN40VZa0Dc51nvA6q0kBladzXsPejdLPtA3UoF28zQpasl7XjVril4Iv6bi3djPB-zX5ycFR0eY59iYWOFhlTJPkpXiLVzyVqEiqFI_jTBv1nnZ-Qfv7jvbHeJ5dF0uYkb2Do7CLDItUkl1ipT-QW3SacCm1iityTvUO33zD7roKGxuYrXJeYKFmvaIdkRfBIw8-TTYqu7OZDKXvbqn8qmwroViZMnhks9ip2Tfs90_vkCc4HFYm95Z3a7fw21VZK6l3yrKaCV6URSZ4ztKyYuR1ayZVDYsdbRRb8YpvaWVHM1_NHH5frawRZrCXF-ynb1z3zR_vhgobtXJA0LZaM9vjvpD3VQuaQBEyC99YCjoqXsGPtMl4IVmal-9Yludt3VScgoa-3WGtyEs8X0p7S62_LngD16xw5mvjolqZXY7zhVd2eA9SgExE4j9IssVOHL3vE5e9U5ViGVYq8BRrSlhHqOxGsSVvcFaS1W1S47Aa-i4r0h2HFclZ6MzkZ3TDn2meCeCOFovjKGDwul2pCgdyNzPdYY0ddgu8VDle8Mi6fYTX43PZ1mN4urEPHfaxh6U_jENSe9xHdowz2uirk9WWtjJORJjI8PfajsQsOLQtKCdB9UStS2hPMu9izDssY1T_On7as8SPQhE_uq4Wu1wo1iwqpQDnK3b827_-23f4d4J_3_duWsFlV2VeXq8P_16M3mBIlNkuZBGx4CKcOY-u9uUCINO9BSQB8iDAilKnJahLeiGSxrh8CJFtrZ3gy5DjuwkHEtq3MisgdWlC9-mMQraBCLibzCQo31c84etv7zp2NwwSHqWPpc9J_9AExmpYWpW_qOKIPeXVjVqz58ffsauG12_rKUmrYEX6BFmVyPgOs7kqEbYMnMdS81lDCFGNFkiU4C2deAN3qVlNLJGVbWOVqQXPzMQab9Stqic71AxExIV0w8dSc_wq6KXiULAmOAevnSBF1OXYyjsUA2QC1lX0WIo5h-wVsokkBvPi1fEEIQBYxHpFucxEPdEYrN4LpOLsJmvWYHiFBB4j5lnCd8Sz73ncDtPgsRQlJFHvIQWO33shOSAdf43vcmUhLV6rQ2AOvkrBScwXSCg77On4kgeum2yp-boAJSnzG2gpldDVWP2V2P3CK7sCFuVkaifqQZLJKqsqA7GstAhie5WigovVPJPst1__S2XXi4a1m4VTwPEviqXZLniTKGRjYYsHaXdWEsm7ySQOGSouUbjkCMhGnyGdGyJBJ3rAhsrXhu0sUTCDHd7W7c2kr_cOkGVI9Fxgz6Z00r_0dZiaR7bwlC3CVIgYtbtrJ3YykxG5K6JMr9mVpKwrSRliUbxdlSBeusKutCQqrPq_qK56Q7UsIchohXF9O1pEV873LH3rMm3maUbpCWfbVdh14hxFgXBlNJOxzwPhOzxMpVCAu9hNnXAGaEh4Ir3E4VLgLEKRCs8Po9RPUicQISeyhZBodKVsTuvIdVA50jcHru0Glh1ZrnvpeEe-feS5_2TbRzZluM7i1AIIEt_24BefRt9--D-rq7W7mpIXYL8ggHQ8J1T-zObuDA_oNUZVcOfJj1--duIdJVG4Qdcg5r34UUXbi79jjdovassUhVccOUL1i47K1h5cH7UQ7USL1I5CFTkOjqAXPapNO9EPqTa716YrBNvUdf80AVerVwYXyBbsyrGVisRMxNRTCmSqZOoHyC5BGKuA-0niAKy4za805bzqHfD5-dkP86fnF8_-dn42P_3x-Pn84vTV6fHFyVPtdnC2qwl79fTYcv2AXUVOFMtUxp4rZBwlbsS5k4ggdKPEUzN_5vmurZKEu5HrcC_gIvW4dERoxzwEGLpXDFS1MQXMcpk1X9PlyfPzv95SASYVMgV_T6JEIH3CjdNERqFMeeh4wk5CzxNh7CUzhOostREFIpjxiPsO4I0nn1UBfo7gg2-bNLFU1CbK6mXnAHh4dHQJ8RLzMrvivvIV_oN4mgkXeBNHrsLWfS8UKvUCl8ehJ5R_dcROHf-3X__91Ik0XTi1Y5zhZvPAvaKxIFaWaWr14W1RalAFL4SawumAF9eZmKr3qPMyCsaarLO9BVVcA0ZZUrZEWLD0EbuSpainL88vLo-_e346P764fPbk-ORy_url6QktoBUyDw2_vbw4__H07Pjs5JQ-Xp6fnD83j5L1wMv4Uo0tcfgZltNFhx274Di-I5LQHaJj0yLpouMhTY8um1MRzDR0Lnn1ll5u8-ZwDGLZcpUrbTdWFsilnFGL2ZJlS2kOZOvlgrb0N1WVQII8SzoZWADZGUsjl2KV8W5vY0Hgx74XS-GoKOl3O-q8bLDt7m2UbuVZ4Ho8TTmPEtmvPOqsDChz_zZJWS31frVD4X2d_tjGBVkCEkO0hNZfEiHWvfcb3ZcX-lVTCPGtlXlRQxO96Mue6aQ8zxMu3uqlRFXWtTWwoEo15LdGfZnpIlMOlTLgu2NwpotNBcwChQpSBASleN-UsSWtMemUw7eKFscm8KAiJ2iqNaEoci4oIHHs5arpqPzl6atL6_zs-T_3pB4UTst_gaKI9k8YwXOyF-SPtz9IwQYzaM1ETo5sDJrzbDmKy-Hw8UJG50MpbsJ-bqFRA91Mq7teZCvoKakw19_qUgMVQYEcZR7JfjGyBQmoB0NxyVdUOdRtBShR7K1aNRuqiR1zBAol9FqREzeKKquljm481ZSizLW0GnbG8X05wNM0Se0wDqQTblx-01a75fL3a4n1orjrR0g2IaC9FzXqknWiHtLhMhynZ-7s49-Lj5ZlDf_wJ4xLvRpgjmbW2FAuh84OgIX6OyUQuC3MZQMiyFxGQQIgpqu7mL4--rmlc4UGhbou8UGfo67IasOzaKHuDqN3nbW2G0EdHB77Ql2g175Q2IZQ-gC7hs2mDwVVkG30khy7g1-AYVChKLarwKKpyjwn_4AMEq4IFgQ28a6s3hII9kokqnmn1KCtq9_wDrXF2Mnriwtw1Ql7cXx5evEMqfz7i2dPLo37vj77Ed89eUbJyAQ5qbwBbqHyvMaGTnKFYyGdsqLVzq9uUFhRAN4yFzVgtDMB664rqsBTDuw3bSyp62HREECAB3-7WUW_SQeCtL-kPX1krwH_OjWQSv2D1kicZV7Sa2mO2FAljXMd5YtD9helYHOt_5Zeltar02QTePQMqLeqKmCFseDLTiVgty6W2DtOqRFUHt5ydXJ-dvns7PXp1fTq4vTk6enJX_SnJ69fnV6ZLiL5M9YoRLbCC3R4FNWyFboXRLtD8YRf-s5U76TfdiK2UA0mRELO9GcdsM2tIzO5FiJfEViYpS0SavVCqzap4GxZsWrpXAjFCmk1paUIYrRNKSJwVlh0PZgmXx-yY7nMTATQcy1B_xLeXG-wfUB0fXadBY87DsWWbdNtgzKZ1lw3RT6y5wq0G3aG8LFHdc2nGi9k3Qu9h_TbMedPQadLcdTsWaLMWXZip92NLLZVVe1KLzwAbBefWz6jlf4BHIPstCGAyD_WElJg1PdNW1GkvwRdwTOjNmN_iuTVXcNIsyXkIHNBaqVZVTdD8jSODqaVFQW1mcxKQ4-J1Tll8YKSPyhYpZsNaavFk7g-tfRgcKgTjnEc9V6J1vQNeo3hMqCsUDlrEFn1uoAJCHm2cm1ngPNCv0d5FQhMq7yAg8nyXaETvQ4DfSBcxznxN4IKp0dg8ytIKZgeNgKKAF_EwZEz1vBxODiYzfAw3eiDAug0aCgLEJRsPmb8gHoyQ2HcaLoVGvAzEPhmW-qKZ9UtekVHwbrxg562ggMh9RkmCupQtEvtQpq7CV6BJFTTwcdllgIgiFvAUp-7h-lpopukERVmnnD6FDm6mrmVjR_hTqWXCxbg8zRBXag2NH-4Zhno6YPvR4iOJwoZoveEAeVM76xsG2BMDzEaPPUyx6MohcW7sKQEbkzNNMCKUhED6yo_xJXMBkpMilQU0rp-HJTtBBaK_iDzgQXQ8Eqlna6TDTTggjKAIQXY4XqID-o75vrgwdEHQB4hklmjGLwZ9eGSXY3z6JXOmibBgxqUCUWtDsJud50apgvMVmVJ7LQtap4qq0uxHfhpENOUnKAE7gc3XQ_u12hmS1qTK9Q7aCEYoY8KWKUiGhxxdIHVOcRDbp76Ql3Uv_36HyQVm5to_SzDu2-VJt1BZXWZd9_0QIbkgY8N_yL_hwCTdTY1pDFX22Sg60Tnder5cmEYpy6XMYJkFse9OUb3Y5u4vNcNVyck8dI48GbOLIkHKj669OqEPOTaKrdwUrKsLIESvMR30yVHggGDhMNlQtUWv0aokoGQu_g6Kcu3lqqRGQx41gK1ZJWVlu3oZkLfSAkTNXOkH6bS54GKw8RP3VnAbTdWkWOnkSftWMg4uPrWJO8_vzo_23SFVBoqT8VBFDu2b-veJ5nCDm0UyyIQ0na81BWJiLyQq9h1nNBXifITl7qkM3G14-DcAMW7sBPlht7Qrdzc0HU2fcgd25AdCaHUNSGB1ZV2SHGEOFSYshsP1moJX6Ai_aAkdcwnW9ylG4ibsAR-q3M9eTStitQMB85rc31lDddXJhUN4uoVVaUoqZUuh3VSQ7ZuqB06XMaBNCmSrfkBCsyOf3MWupbAMgg7ojuaYW4OnxGPQdEi22V3A0UdV4pUQvxRshkn3BulsSCjPhkt18UDILjQ8H_dMaYeTHVvgpRnhMdrwy1ld42iy-RBP0Q31cQ9C6MbG6BcJkBlYcB3C-hDcUcxkqAaqCnXZjU1TghncZR0oZTjJX5dlLqWwlJ5vcOXqEnJY3emAi6G-nVzjfqZG8B7XYT2nhvOXCVFFPqOP7T5N3ejnbSH3W7Wxg-0J0PZayLwlGzcQ3YydlY4725_1Y2g3_uaFtOupD6e35V9EISS8zg1HqFMLd6z0k0MWIJMqN1fZ4E6k5T1kP7AF2i6sK4JsCa3QgGuVmXvtQYNR5Hd6PPQHaNN73Hk3sSRoNHskJ0OX1o0NEokVUvXa90OiylfUVuGfHsTHzvaLSp1FA_TdCbCIZFsLpKHvHr_q-DlUOzp4hWhRAUsNbsyIgemlDOZuq9IR2x56y6IWlVFbRqDmh8hakuKMWp6jBKObjJNumaunrLt4WB6iVgAQe5stCO4HKVcZIrQVf7QaB5dXW8y7N3voXsqE7luKCXIrD9QmdHV9Mjk979nziVYzH_DZSkL1ACphPjgO5VT8bVMsutW0wxTalGeAeklDrcEAUrJwShZ67JYvUfKphaGeVnk8HCqIQZpw6YP2RNqRdUiI_aVEoAtSkriXYk9WN3Sd4hKHiEU6wbbW25GsFFDAiQ6WB5gdqLjEfylA7Bp1wAYeZc5bpRuhYZ5XeVSia1z4-HQK55qWj-tOYgXOfMtFfuOpiXViiCz0C1_qFy1hcmXtclXFPcT3VwecqrueFOXk-frOsMXJZSuWOe8-PvEnpg2jmUKfiRq3rnz5_o6pvbVgUONp66j0xdTulM0Lvl35YlZ4sCZhRsPeWI0bdA53ENGB8yBVsadNiX5wKiHfFq3K9hd6cuVobvNE8p-XfyOk6YhGkMP26hEZsrz7Nq036HpCC0UvcvF75nzm09kj8-MrwOFmi8Mr-uJeNmKL_68c_TdDPgjlIbfFy2ii_XfVuyPfR9e59_O9vJP_3hT8_q28etD8wcbfa3FzFrR7Zj1i6pKy3i-duODL4zVq0Cg2AnuPTP-bCNiQKwjjSrjy1jTAydnbzghFMowNp4UGAZjzO3IlzS8pUU3AXPR3zGR1OFOAGGkhZGoDWfVqEv3-vo-3lxtUJ2pxj2W_gqxWajtPNkVuMh75OeIBq1yb7YPB-8W60Ef037oJP_263_Wg9StAQZSYXz3SUS_10n3pkw3AQrq681DOsc7Tw_t-D9ZjO3GY0HjkZjxqNCHfwS_ufvY1O2xIefT54eCvjYh9ThjUDJOYun63JWRH6PgiMAQQY5CWyU88ESC7OQiowT47yz2HIUDjRIVO0IoEflf2s_npqD8o5n9uSmo_n-E2k9B7aeg9lNQ-ymo_RTU_5spKGyTJyGXKoyHgnmU1_ue6QMytbpNuBK4yKS_VtvCbGmucIaKceBA8A1s6OpOaehqP_O1n_naz3ztZ772M1_7ma_9zNd-5ms_87Wf-drPfO1nvvYzX_uZr_3M137maz_ztZ_52s987We-9jNf-5mv_czXfuZrP_N1r5mvN5_-B3EA0zA)
