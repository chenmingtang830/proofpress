[//]: # (ob:51592d7b)
[//]: # (ob:v25-title)

[//]: # (ob:d39effaf)
# Exact Knowledge Construction v25 — Transfer Validation Protocol

[//]: # (ob:7ca48f6e)
[//]: # (ob:v25-status)

[//]: # (ob:762478f7)
## Status

[//]: # (ob:c130f556)
[//]: # (ob:v25-freeze)
The table-cell and deterministic-derivation mechanism is frozen at the v24 implementation. The five zero-heavy tax tasks used to develop it are development-only and are excluded from the primary generalization estimate. No further prompt, retrieval, schema, or formula-template tuning may use their executor or grader outcomes.

[//]: # (ob:659971d6)
[//]: # (ob:v25-freeze-receipt)
The machine-readable pre-run contract is `results/exact-knowledge-transfer-v25-manifest.json`. Execution remains blocked until every placeholder in `frozen_controls` is replaced by a content-addressed value and the contract validator passes; this prevents a nominal preregistration from being treated as an executable freeze.

[//]: # (ob:82e503e0)
[//]: # (ob:v25-question)

[//]: # (ob:99bcaffb)
## Primary question

[//]: # (ob:ff930bea)
[//]: # (ob:v25-question-body)
Does the same governed exact-knowledge mechanism improve task completion on untouched legal tasks and on non-legal exact-information tasks, or did it only fit the five development tax tasks?

[//]: # (ob:35916d75)
[//]: # (ob:v25-extraction-qualification)

[//]: # (ob:7bbdcfd7)
## Stage B.5 — document-extraction qualification

[//]: # (ob:83827557)
[//]: # (ob:v25-extraction-boundary)
Before Phase C, qualify document extraction as an upstream, provider-neutral boundary. Extraction may create source-bound evidence candidates, but it may not create or admit claims. Every output must bind the original source digest, extractor provider/model/version/license/config digest, page and block locators, and table-cell coordinates where asserted. Outputs remain `not_governed_candidate`; conflicts require review and Human Approval remains the only admission path.

[//]: # (ob:3b61cbe0)
[//]: # (ob:v25-extraction-routes)
The primary open-source route is PaddleOCR-VL 1.6, using the official Apple Silicon path on the local M4 qualification host. DeepSeek-OCR-2 is a sensitivity route, not a silent fallback; because its official reference environment is CUDA-based, a result is publishable only from a separately recorded compatible host. The existing deterministic/native representation is the control. Commercial or third-party document-extraction systems may later implement the same envelope without changing downstream graph semantics.

[//]: # (ob:8b1b7aa1)
[//]: # (ob:v25-extraction-panel)
Freeze a document panel by source digest and format/layout strata before inspecting downstream task outcomes. It must include born-digital and image-based PDF pages, row- and column-oriented tables, multi-page or repeated-header tables, and documents without tables. Development documents may tune normalization; held-out documents determine the qualification result. No APEX executor or task grader is called in Stage B.5.

[//]: # (ob:9435bc40)
[//]: # (ob:v25-extraction-metrics)
Report exact cell text, numeric normalization, row/column binding, table boundary, reading order, page/locator validity, source and configuration digest closure, abstention, conflict, latency, peak memory, and known cost. A route does not pass merely because it produces Markdown. It must preserve enough atomic structure and custody to feed the frozen table-cell contract without invented values or automatic admission.

[//]: # (ob:022bfe58)
[//]: # (ob:v25-extraction-sequence)
Do not rebuild or overwrite the current graph before the primary Phase C ablation. First qualify extraction, then run Phase C against the frozen v24 graph after all v25 controls are content-addressed. If Phase C advances, build a separately versioned graph from the qualified extraction envelopes and repeat the same frozen evaluation as a replication. This separates mechanism transfer from upstream extraction quality and preserves lineage to both graph versions.

[//]: # (ob:978f465b)
[//]: # (ob:v25-heldout)

[//]: # (ob:616a60f3)
## Held-out APEX panel

[//]: # (ob:dc90fc17)
[//]: # (ob:v25-heldout-body)
The primary legal panel is the seven APEX tasks not used in v18–v24 development:

[//]: # (ob:080ebadb)
[//]: # (ob:v25-heldout-list)

[//]: # (ob:8b72384c)
- `task_2f85463493f14785beda2ef2d316309a`
- `task_876ace32decb4f26a3f7a7c3bf50bab7`
- `task_b68a970f95ea48019176f0be1f73e61b`
- `task_b9b58e483f384c5990900ef2d8c9fe17`
- `task_ce4a398d9cf64e63aa54cb88b6615c93`
- `task_ed6f8d835b0141309442d2c373d1c5da`
- `task_8705d28530a94c2880fbfd7190e257d4`

[//]: # (ob:d3f194e7)
[//]: # (ob:v25-heldout-rules)
Freeze task IDs, task/source digests, native output types, model route, rubric, grader panel, retry policy, disclosure budget, and executor budget before revealing condition results. Run all seven tasks; do not select tasks by prior score. A failed native artifact remains a failed task and is not silently converted to console output.

[//]: # (ob:fc060b6d)
[//]: # (ob:v25-ablation)

[//]: # (ob:6a630830)
## Three-condition ablation

[//]: # (ob:46aaf790)
[//]: # (ob:v25-ablation-list)

[//]: # (ob:6d8e827d)
1. **Ordinary claim:** governed claims and relations, with the same fixed authority lane available to every condition; no table-cell coordinates and no derivation nodes.
2. **Claim + table cells:** the identical working set plus exact label, period, value, row, column, and source-span bindings; derivation nodes withheld.
3. **Claim + table cells + derivation:** condition 2 plus formula identity, exact input bindings, assumptions, intermediate results, and deterministically recomputed outputs.

[//]: # (ob:1099c2c6)
[//]: # (ob:v25-ablation-controls)
All three conditions receive the same task, source-access policy, authoritative-source policy, executor, output contract, and maximum compute budget. The treatment is the admitted working-set representation, not extra coaching or extra source access. The causal contrasts are table-cell contribution (2 − 1), derivation contribution (3 − 2), and combined contribution (3 − 1).

[//]: # (ob:37ac752c)
[//]: # (ob:v25-nonlegal)

[//]: # (ob:a2ff9553)
## Non-legal transfer panel

[//]: # (ob:0bec5af9)
[//]: # (ob:v25-nonlegal-body)
Create frozen, source-backed tasks in three families: financial-table reconciliation and variance analysis; operational KPI computation; and contract payment schedules. Each family must include row-oriented and column-oriented tables, at least one missing or conflicting input, complete-period calculations, and an exact deterministic gold result held out from construction and execution.

[//]: # (ob:7a2929f9)
[//]: # (ob:v25-authority-boundary)
The generic primitive is a source or governing-provision binding. Legal authority nodes retain their separate normative hierarchy, jurisdiction, and effective-date policy. A contract clause may govern a payment calculation without being promoted to statutory or precedential authority; a spreadsheet source may establish a fact without becoming admitted knowledge.

[//]: # (ob:21e05b04)
[//]: # (ob:v25-metrics)

[//]: # (ob:740aea58)
## Metrics and analysis

[//]: # (ob:3d758593)
[//]: # (ob:v25-metrics-list)

[//]: # (ob:9e9c808b)
- atomic requirement success and strict task success;
- exact-period completeness and deterministic recomputation pass rate;
- exact authority or governing-provision match, with applicability candidacy separated from Human Approval;
- unsupported factual, numeric, citation, and authority assertions;
- native artifact validity and requested-output compliance;
- context tokens, tool calls, model calls, latency, and known cost.

[//]: # (ob:2843a136)
[//]: # (ob:v25-analysis)
Report every task and criterion, then paired per-task condition differences with intervals. Keep legal and non-legal strata separate before any pooled summary. Do not infer a product gain from construction coverage alone, and do not treat candidate-bound objects as approved or admitted.

[//]: # (ob:b4277f58)
[//]: # (ob:v25-decision)

[//]: # (ob:5da2a75b)
## Advance and stop decision

[//]: # (ob:4c70df8a)
[//]: # (ob:v25-advance)
Advance the mechanism only if the held-out APEX panel improves exact requirement or task success without a material governance, unsupported-claim, authority, citation, or artifact-validity regression, and the relevant non-legal families show the predicted table-cell and derivation contrasts. If improvement appears only on the five development tax tasks, classify the mechanism as overfit and stop the product-level claim. If table cells help but derivations do not, retain table cells and remove derivations from the proposed causal explanation.

[//]: # (ob:bd8ecda1)
[//]: # (ob:v25-boundary)

[//]: # (ob:e0464656)
## Claim boundary

[//]: # (ob:1ee41274)
[//]: # (ob:v25-boundary-body)
This protocol tests transfer of a governed representation mechanism. It does not establish legal correctness, authorize downstream reliance, or replace Human Approval. The development-task checkpoint is recorded in `results/exact-knowledge-stage-b-v19-v24-sanitized.json`; evidence-bearing artifacts remain private.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFkYzQxNzlhYmViZmY2ZDM1M2M0YTVmZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImQwNTEyMTkyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hZmYyZThiMDg5NTEzYTRmY2Y0NjcwNmIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EzMTU4NmMyNjBmMGU1NmE4NTQ5M2ZiZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVmP3EaS_iuJ9ovtqarmfbQeFj2SvCP4EmStdwDbKCXz6OKIRZZ5tNQWBMzb7PPuYn7C_jA_LLD_YiPyIFndXaxutzTrBQgYhlRFZkZmRnzxxZGldye0bnNJWbvO-cnZyW63djkL3DilmcikjLgf-iygoZQni5Os4ldrnl-IpoVnmw31wujMS92QZTJkIXVY5nE3cWI_YJ7MvFSGGQ2SxBEySDIee07khl6SxJQJ6fuRy0QUw7g8b1h1Keqrk7N3-Jd23dILmKGgLU61gD9kooAPvhd1LnOaFYLU4jJv8qokG3i-qq9IdkWe11Uld7VoGnhnR9lreiFwUXsf19VfBCy3q3HATdvumrPT04u83XTZilXbU7YR5TYvL1paXiS-c7r3di1-7nL487prRL1mVdmIEvairTvxfnGyERQ3kTuh67mpd6I_WYtL9RBsrlhTKT2RZE6Shq5PA8lkEMVOlKFkVd3i0tZFXgqQ3J5Isaa-GyYR8yJHOiKMaBIGqS8zoZdjpFszumu6AhbsoZysqnlzcvbDuxMz_bsTOOWqbvBP-mvB1xls-Q8nXfm6rN6UJz_BGqw-4AG3Hc9Fc0p34u0SBCrbpbikxenTP58_frn-8ptv__Wrp0_--en65Yvzb7774umL9ffnXz17cv7y2bffrL_3wtWWnyzupV-0bes861o41nVGm7xBIUQh17SB7W6FGq9rN1WNi3idlzhkc9W0YgvflHSLp20Xs4BXG9SQk7OyKwpYGtvAkQq9KVlRsdfwdOiGqcdj3H84zVa8xYV_-t9__9v__NffP4MPzSSUczX7DtVOvIFPfjg9_emMfEI-rbKzSy9ctnlbCHyjvdoppaM1PXm_GGbifiqkpHJvpqdvYWvIlyBwIfiFII9Bo0CZGG4BgWHJr3_9T_KypmUzJcsn5O7jSFGT72mRc6q-A5MZZEZtBc3fEztmYMEyEh9B7Otb2LS07ZqpPYwjL4gTGe8J8516bXJ_PiH9QxNLZa7vyDCM7jn69WXIWohfxGc_li83giiLXjJRFISWnHDRihrQBTArZ0su6onFJp4IHV84DxTn5w4wFM5lal_TNGOATPtW8LzOtxSA1Q5wZIdveXxir6VMfScT9DfPeGiZS3RSsPlPKtGQFk6gAVggF-heSsGJQM1dTm0F6FcQhdkHE2wjCl517dT2R25EAdv9vTn_BO8t4UVy_vzpn8mOluABp0_g9jcmDoGz1JHMjR8y74Hl2mNAG9iZ3SvEBS30iCRXhzOxJw6whozy7GPIVoD5TZ1HksWenwTsIXMvyauWNq_XngRvHfnosF3ArjATnHpCetx3I99J6asfS_toEkdAjHyPj_YFRb3mRqSbBuKjnFkN9KGBQ_tCIRhBocizJ81C_em0qbqaCTKxb5I5kZNF_EPKBvhJj8EXWI_vAFfbm_flBlaxhL_zXLklO9ARI5p4bcKSgohSGacPl-DQ8o_qbMQTkXgxf7AE7op8_vm3NSwRbZYVNN-eff75gKDqk0Z5s1ro4UBD3gCBJu2E3rpOmjKPRR9vh3DYuipQgc_B3bY4NunHbkBaNgU4PkQlceixDy5gWZUK-aZOj3rgEMNw3wN8g8euMLO1zO0ubmDitQkNBmcMEZxMHyzBoeVbj_C4FhDWEVlXv4hyQTSqLDOI1kC5prgf9VKIKD-8gDqiyNsrkLArOWi98VsQ8UC8yZT_guO_FOC1JgT0XOGEmRN8cAG3AsIiNk2MA4cKGiZ7c3-t31OmSktaXDX5MZp84JUJvfF5HCZh6j9o5gMrPgp6qUhZ4iTZgyZfEtpWWzhnE9xvIdAlTccYhI9qkAbHa7U7NJ8_Qq-NXHIC8bwk8KnrRx90Z-w7oKIvBGYMiMDEiRYOB2WgyaC1FZhWO7FzWeDFsXygwlwXjgumcjJTRxYC_aHxNX59zi9pCdxC73a1I3akI-o69d6Ut2axw2VCHy7DjePRg6ALMsNhCLIVmHrImy0BLLwiuVSfbqaOB7w549T98BL2GDcxu3CCCGKgfc19jH6f2NePHMyNhydOwxUicL04-I2zHVrgEIFArLGrq7ZiFaAwBHDNgMXXN-GnhU2XnYBZ4d6umfJXOKf6xuaxxDqQMQ0yKlIunYAmDmcyFFzgOsqqVWOajB4xGT3CNoK93lV52aoEZa1mwuyU_Rsmp37CVGCRs6vRCOP04GgQlXj8jZnDppLtWsJhiBocnElQNpl7ltFAShHEMo4zHjs-9Rj1Mpe7zM0y6oSODGSQOo7rh2FCPR-zwA7ENH6Yhk6kIBEzOSrRqI_rzA_ew0ZjOs9zvGjpJEvffen4Z557FiR_cJwzB5mz2XFUwAzCJg5ivh99-u7_NDeptFXnDje02eBSPCf1swjixABhVI0xSicaRb5zntCMSl2axbHPA5_FdtRR6tCM-rCMnzKF243SSJHELMiSiPqhJ60Uo0zggbUdTuCZYUXkuJ4ApUlZ2g875PTs4qbTdXb7s8yVYH-Rm_l2rFEG74CI90rO5Zd6ywb8BijRxBU4gwLxSy8g-XZXKNagnl4RHFoiXfxF1BUE1_QS_fNb5aMb0jXAc9sKZrsUBYB43hIwfftXHGapvIRywvCFeMuKDqwIJ96qOW0-RfFTONhftJSYmtoCVK0gAiCyq-HRGoFvu2sXwG3AtaOFAOMGANnSBalqIqt62xV02QpYArLytithm8mWXqGcOFtegwSCdS08Dv9d1BQ2hkA8z6qtaFaHzzoImR_GQSTSNLDnM0ppHjifqWylGZhFgDwURvYcYQceJTAHJbpbRtKM6vMwFixzPDeN7KijJOURce-UdXzdG-tIobZwQpcm1wJbCpqkDhP-68q26uCsuEmcafVBtYAvyz6u0GPnJZ6lVgT1oDpfnnPUL6VPMtcaqzRzpG2Dav7TBCrFPE0kbE7Mw37Ph0zpgd2ZSH1aQAhcN5Ke6wjaA8IoGzqc5Z1zm2ZgGXkhTZjIErcXeJTunBb4bslL0iAh0ALpswG3r807Bwh2k1__-h8ID6O9Pju8EzwMAnCWsKN-vxOjHOgRgQ8FSmbwOBMpuHBw4mkP56Mkpxn8QSlLlgXSA4cBpChmfiZDJwNHNnoUPCVNY0emoQA_4ripG0cSrMuVsS8AxMePplmYiCDxJQoYpqkDdAMFSFgqhTselYmA-mnCUyajQEQ-pWHAsiTJosgNWeqPHhU8AlKR-BCjuwE4ijQIPO4xH5ytyyAs2VuWE3IvCX2HpgHzksSRmeSxmzrCC2MevLol7LOwFzMRSp6KLJaD_-5ztkfO8U4ZWF2Bhw9LqrIS8OIOLAMFgg-3FQcVreFDAbDfZRDRLSxsK_XVzuCKaJK5IFh9L6qmA1-TdYBO4C0QZHrU1x-STADCqLq7AJ8DTmLIitWi6Yq2WZEXHThG8KbaMpRRPCK8UobRiEKYKLrBYj0YFgzeMBh0Rc6JpDlgo12SZWYw9JbmJcCefaAPdHNtbw18WraAbyDOpSoSo3PFynxV2K2Z8FKRE6cRd8MwHojOKI194LimktJ24Bi0Jo2YE0e9lxrlqQdku1_C2aKFdCLJqRBRRu3ooxz0EbGPwUUgpGAOMPVQ9tRqlF82oz8kUWw9pMzfwpN9Bo4UoKCEXsJRq7gJTlKnN_rteQSHPuZtrKqUBBDXqZlKJFY9cSvBFprVj6WHouqQ8g_6bYJvNygvypJz0KGcAcC_qerXqNwNaPyu6BrtXolqQFmQHWZW-IIAj-rQuqo3C5Cg6LalthmTzGzAzkgGASuMhAZwTSC1B2jxIJl_QDL42_AaijkoiKcFM9zNyN6CIWtR8xLBwM4OcjVNBxRQ7z7EeUBxBc-R7BmzXdwkv2DDV5gvBz7SoUVpMxqzveuwx6Xkrhe6MhE9fRql_I8p5F1y94gLveIgDPTJY6pzdRbQrDopKFka0LRfWlhbWNhUU8PG6W3Y0rf5ttsSs3QDfprTt5gJUJTJEADKt3mL-2O0ZolaUwtsx7HRwEKBFKy-pjAmZRtUrqo2nxjZtPx6Eka7hhZGKsxVYAywp_Bl3yRDPvXIr__278T9bDFWsv1HfPWI95leH6wLVAOt85aH3M8mkDJxgFB54MWjlNsTHtVMDpzwVPGjR5skyNLEDYBi2oFH9ZABKe9X2LBhItAC16XAZFiPZaNaxxGx71S00C4NOJ9WW0m3eZGL5gzQraQly2GY1vSswa4z-FKfE57HJa1zk9TT-dZHpAKUUQ_AQr98_syoItXop89Qayys_konqzFKQOawIk9BxbQEV2TbNQgHKnxErFqCUcDjCLhqFMSt4TMlIoIBoJ0AzYOoAQKVvGmMxsKsEkyoxb8qjFnYeEUsNS6C7has65FeZ5ENKu3BC_iIghv4IQiEaIs6vmXjNMZAQzCuPqxBjpdkzEl56A6-dlQuOgQ-96n7kN5YMQhWLg4NHoM33YZoAHdFvlIaOrg0DflAuajSEAyoG4ErAH0qdcwGM2xyOPSabQCh_tLVecNzpuFD7YEEf6zAjONbGsqQNPWaAL4W43WM27VwIK_VjtGpKM-De50JPEZMDlSGMancjWqkrDBrAHir_Mp4KY9wE-ArypuNAKQzG4KTAh8F9cmbjSJqINAwESgJztVjZR8FTxwo9ZnMwkgGPOq9yai8duBAJ-pkZtw0pKkMYOQo6GnTqHQ2QM3d62A23kzCMM2ygLtDhDUqjU1LfIyPgSJ70uF-GCS92KPSVx--PaCO1fY2bGy6tG_tW64lBVqddkAuCGryMM5I8w9YCmg82xgiSHc70GWaASbCCwzmyzllV72FmKzXn7otIMn5DgehhZqsK5tuh4lvfAbm7TC1VXZboeIdllv3q06wF0k3kiI-qUGuRxuXmCZVzynSqrI7QuUdNFOArVForV42xQowntcC8a6tqgKNreiDMPMXzKyVipiUWv3RRTftBJtygDZlXuoGSdID2qiceAjQ7lMb3Ag8PlATjqx2afJPlmPyHCCnBqkNW9XEEbYHXMyXQuxMOkQzbuuVQb9oSwd0MxEjLTHWrDB4AyaKyZQVeaJjwrxEJ04RiDhgPrlAjLzpB1RzONZPaAFOyfBVPYLiZFZxwBMpKCdVhj3eoL8Nahgm2Dhqo8Wgqaxl4npOKNzQFT1dGNVKD-z8VOGzz-vHCU14GsdhT59GtdABeu5Z07QZHuaGEZcpRJs9iRqVOQ9pzH3KlTczcDZ7aaOkMfDAdo-BpncIFO0flBD0RYMDTrsYm_NSBY4Djb8amzOeorHWZW-ttbioda-31g0UF0JOAUtqR_ppiRlpNtUbk0kX6Ggt-xmXAvbZNDLxFXkm7YrVEkG1BK0bvUtVeSS7ukAnDULKq2ubDEqKG4H52f7MtXDKKED4S8QS3BQlwjhKhEPZQYzSjgRujGkses4xel7j2rZSQg5vjEoL1a7CDKYJQ8TbHYTk9Aj_ojxzncx1HYd7vdEMFewDyjdVibZJeS8WvvQCMMheq0fF6cFo7lJvtinnxImlDxFHFPR1iVEJ-oiwd6oqVxLUvM-D7AeEw8HDYcK5YcFAhYg9g9LKyqoafG2Lbrg3hV_g1MB7NAh6W9TwXBsPGAVMUlCw331PqUPKcWlJ43xfQUZmay-DYATzyuQETq9VLLC0B__Plpduurz0gmUDS2hBIL76S1OVrx6Bq8FEBAZFYBOK8BkzbUwOD-n0JZanbtTc3-Pp3HJLBWyz7e-ofLsT5fkz8hgc69uTn9TFF7COg19fu-Fy82vj2833L3I4lJqTlxSU5fd4DUaUl3ldlXiGa_heyX7bbZgNnv9vvQwThWkau_zDXIBYqpzNrjVB1VblPvBTyhUgwfvLuitv6cDQicNDkl0Tw7RavLBKrECY5sUSc9qC35xXSwdUY5-h9O7NlDZtUkZLZHfj3cmbzZVqxbk5k3oIlAMkQ2-kuOswlfGN3M7ZzzcKcN_fo_skjOMsi2ImBfwh8nwJ0QBNvGFLxm0l45aKcavJu9-zGty93eZ6u4n7_vZmkmOdNR-kfSZKRCK8hErGYipdz_MTD_xYErpZ6jlg4p7nBswJZeaH4N2om1HpyYxlqROJOGEH1nNb90wA_93SPeN6lDkcQsO5e2bunpm7Z_5fds8AOvqeLzA67M1jhMuT53NHyB2yh3AuB4mfJbVLla-Cc5SwU5r0rcCMjO_q67TK0GG7u7LNC5N_UMx0UxW4dOSYWgfWtubzSpNQ9RTHyjC9xZWqilsf3PWSX2rLxJQlpnaaR_C1IubKeWDWtsT0I3Zu1ALCxFzlKFBgpQ86DdpqH6uyBaU5rxFVmHuc5h6nucdp7nGae5zmHqe5x2nucZp7nOYep7nHae5xmnuc5h6nucdp7nGae5zmHqe5x2nucZp7nOYep7nHae5xmnuc5h6nucfpY_zU74Oam_wwdSNgqx_shz1VekM57-XPwMxyCSTv2C8VxlnGmeQ3fsAW_P4fV7rrgFesU2o8jE_s-Md_5PaOA93hJw0TP_HiMPwYok7s5ChM_aOmVs8B0wR5vDAjX039hF8WuSy7-Yu5H1dkVYZorpXSKjBGm5ab_JHfzM1ieu2Hnj66yIrZDCUY2s9hOE82tctp4IcZC_7Bu2wD34H3Kzqm2AzKsJj67UDH8zIprv3a2UcXuUEA1tTTxAK1yLq8UDwdPeebuzU_jpDr9ubHc247H8FXAmTCX4bFNUIvxlrW6hAgHRt7GPIoshADKKtDiHL7XE-EzHUrQT8sEEebiFRRTx8FDRS73ejoyBTg5FKFQKtDyHCH_lGTqV-Q5_BU0Rt1n13ewSKRSm8gwiVPIFT8TgiIAiBCxlSaYusKE1aHTH16-UBuTIfQEtiSYuoD10YR-jBl32xXh8x0ejodg3Y1JhdYB9ScX43i-S0w6WHpsF5jiKtDBnb7ZN-Nkx2_ADZe1HS3seCuyTlVs9bGSlrzCLI-o1YHmnGflUgZdIiNDK1elqIDDSrIQf3M9nwLqJh9FCxTPdmqpdvwxbLehQkuDshnWaDNDkDI1GrOK-7X3Dvxr0Tc2tzbd3web-6dadBMg2YaNNOg3zkNuvtth-vN8vH723vh_yHN_4LTJIuYEwkZuNQLE98PBedxIj3KGYuixPE96bhgoDFPHZEEQYQd70nKhQ-fHFjPjeb_8MxNz4L0lub__h8fmpv_5-b_ufl_bv6fm__n5v-5-f9Y879Dw8iPUzdjqlSpexuGUOnA7twn9uk7waIkTlImUvVL2RrHh3BoD8cfHsWYSV0eRqkMQqlrSlpVh8Dm-OqOxyMDd97P3oBRdTtdzVncDND7pBSgSf8WQqgOjfdzP7b8MiSBQAmwMAgHj-8gtTTv2UK4adCF4RUYmSYH1TSGzUxKX6o6v1Aosdd6vhhlBKzYp6rl4dTQqlMgk6JsxCl2jeUX_Xs7VcWHwRUcEvgfYpRpFjvQ1vsGHI4gtvaxIt_qZlSbUHgFS1tbY1v3y3_1qO9Ya2xhmmhKribbL5T1MK0WrfwkV71vqsml3UxAHYvB9bgRtioNnT9DlHlcf44Hh_gA-gKdcvv28Yvl918RdxUtwJsqnEahJWg7pvxgSYDQ3-WwciO8rU3jbhfk6-B6PhJ7UfpU3RKH90zH2_Wsne5mpabpnkhaFNgD-QjbvFQDWg6b3UtSC9NDQkY39HHkx__y5HyZgY1wOHjbB4jeqVMVUOViNGzp1NcoZ9QXK4dUo1kA7p54iyQLdmSPc52aNp9rhVjTxGu87Qqo7nYraiU5Ni9s8ppDFFy3V7cCjP6nNRtlXDo11_O1wQfAuhFpRd_9oLJOSsChjqtTZQ0oIPagT3GfWIg4S-MoiOTgVYfswHFVOx7U7xu6shTtW04LeoUrME0-JkkIJrMTuid0tCLlz3ouh2XuvVbUrKrLJUyQt6aFCFQei8uoEOT5ky8USjSqvX452aoKJLPNlwpTdAlc0RWkxsio-oZW1S2k1zn0oehvUe8HZzg8hacKpNV0aFou_OhmdrnpVU33zuybllZtxZxV18yY8qpNMrwXVBF7xXQNvnduU5rAgf-EbsC4HO7jDUmX45pwPFdieun2d0Adyqk-D9vyujAdJtZfYVSgvCxBS6016J8aqO9b7BZ987vuaAYv0RkGanTPXEqCA8waJL1qeovpoyw8nPrrvVT8qMWOnBv07PssVMsirAzBZEAt02wDz3xN69eoyoPaKtCoL9Gaq-5iY7ssbWnArEAXBzACk8L-1IYO6a4374_bY_PyUqu0ovGN8s2gIMjl2OCCJol27LE0iBIn6CnTKJV1XBGOZ6CwaVAjZVdj_twAlkGAceRoSwb2WseKfJHXsIOWBg3TmgZEDLb6l7D5r2nHO4dRsJ6MSkRYvFqGOQgbIKlA9kZIpJqk-lF1X5siQ7ioPWdiyApsv56lD4WNFe-X2yyY2y4qRJvRTSYtMsbCHe0J3l6FhqimITt_c0sNRUtgOeGNEo1pTLUK2fT_dg5oXVaBo9fLMMuajKLn-7zzfd75Pu98n3e-zzvf553v8873eef7vPN93vk-73yfd77PO9_nne_zzvd55_u8833e-T7vfJ93vs873-ed7_PO93nvd5_3p_f_CygN7pk)
