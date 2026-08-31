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

[//]: # (ob:a0af85cb)
Use two frozen, non-substitutable panels. The structure-ground-truth conformance panel contains four development and four held-out image-PDF fixtures with exact text, cell matrices, numeric values, page/bounding-box locators, reading order, and cross-page continuation identities; its digest is `sha256:3af601bb5087cec692c71ccf1953ae5d0e39f76e5a9e74cd91fc810fc312a4a8`. The ecological panel contains four development and eight held-out private data-room documents selected outcome-blind by source digest; its digest is `sha256:1ae42599f67169323e10af17dafa2ef92c5375ca1029fb21444b9e6328fedfba`. Conformance accuracy cannot be inferred from ecological executability, and synthetic conformance cannot establish real-document generalization.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFkYzQxNzlhYmViZmY2ZDM1M2M0YTVmZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjgyY2M4NjVlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85YWZlZjczOTcyNzllOGEzN2MwODAxOGEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EzMTU4NmMyNjBmMGU1NmE4NTQ5M2ZiZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVtvHNeR_isN5iV2Zsi-X6iHhSLZG8GOLciKN0BiUOfK6aine9IXSrQgIG-7z7uL_IT9YXlYYP_FVp1Ldw_J6aFMKYmBAxiGOOw-p845VV99Vadq-O6EtH0pCesvSn5yfrLbXQScxUFWECqolCmPkojFJJHyZHVCG359wctL0fXwbLchYZKeFwWlLOGyyGQQRSTJwyz2aeDzLIGfpQhknvuMySjhVGRZRMOURblMAxKkIWcpjMvLjjVXor0-OX-HP_QXPbmEGSrS41Qr-AcVFXzwvWhLWRJaCa8VV2VXNrW3geeb9tqj197ztmnkrhVdB-_sCHtNLgUuau_jtvmTgOUOLQ646ftdd352dln2m4GesmZ7xjai3pb1ZU_qyzzyz_bebsWfhxL-fTF0or1gTd2JGvaibwfxfnWyEQQ3MQ8Zy9NEnOhPLsSVegg2V1wURAqZRUUWZoXISZQxP_eDnKBkTdvj0i6qshYguT2R6oJEQZKnLEx96YskJXkSF5GkQi_HSHfByK4bKlhwiHKypuXdyfkf3p2Y6d-dwCk3bYf_0r8W_ILClv_hZKhf182b-uQHWIPVBzzgfuCl6M7ITrxdg0B1vxZXpDr74vePn7y8-Oqbb__t6y-e_usXFy9fPP7muy-_eHHx_eOvnz19_PLZt99cfB8mp1t-svog_SJ935Z06OFYLyjpyg6FEJW8IB1sdy_UeEO_aVpcxOuyxiG7664XW_hNTbZ42nYxK3i1Qw05Oa-HqoKlsQ0cqdCbQquGvYankyApQp5ReBxOsxdvceG__N-__vv__c9fP4MPzSSEczX7DtVOvIFP_nB29sO59wvvlw09vwqTdV_2lcA3-uudUjrSkpP3q2kmHhVCSiL3ZvriLWyN9xUIXAl-KbwnoFGgTAy3wINhvb_95b-9ly2puyVZfuHdfxwpWu97UpWcqN-ByUwyo7aC5u-JnTESg7WKTyD2zS3setIP3dIeZmkYZ7nM9oT5Tr22uD-_8MaHFpbKgsiXSZJ-4Og3lyFbIX4Un_2xfrkRnrLoNRNV5ZGae1z0ogV0Acwq2ZqLdmGxeSgSPxL-A8X58wAYCueytK-A4YxIuW8Fz9tySwBY7QBHdviOxxf2Wsoi8qkgP3nGQ8tco5OCzX_aiM7r4QQ6gAXvEt1LLbgnUHPXS1sB-hWnCf1ogm1ExZuhX9r-NEgJYHu0N-dv4L01vOg9fv7F770dqcEDLp_A3W8sHAJnhS9ZkD1k3gPLtceANrAzu1eJS1LpEb1SHc7CnoBbFJRw-ilkq8D8ls4jp1kY5TF7yNxr71VPutcXoQRvnUbosAPAroQKTkIhQx4FaeQX5NUfa_tonqWEiSjks31BUW-4ERkUsfgkZ9YCfejg0L5UCOahUN6zp91K_eusa4aWCW9h3yTzU5-m_GPKBvhJjsEXWE_kA1fbm_flBlaxhp95qdySHeiIES28tmBJcUqIzIqHS3Bo-Ud1NuW5AOrNHyxBcOp9_vm3LSwRbZZVpNyef_75hKDqk055s1bo4UBD3gCB9voFvQ38omAhSz_dDuGwbVOhAj8Gd9vj2N44dgfSsiXAiTLCsiRkH13AuqkV8i2dHgnBISbJvgf4Bo9dYWZvmdt93MDCawsaDM6YJUQWD5bg0PKtR3jSCgjrPNk2P4p65WlUWVOI1kC5lrgfCYuw-AQC6oii7K9BwqHmoPXGb0HEA_EmU_4Ljv9KgNdaEDAMhJ9QP_7oAm4FhEVsmRjHPhEQe-_N_Vv9njJVUpPquiuP0eQDryzoTQRxfp4U0YNmPrDio6BXiILlfk4fNPnaI32zhXM2wf0WAl2vGxiD8FEN0uF4vXaH5vNH6LWRSy4gXpjHEQmi9KPujH0HVPSFwIyBJzBxooXDQRloMmhtA6bVL-wcjcMskw9UmJvCccFUTmbpyBKgPyS7wa8f8ytSA7fQu93sPDvSEXVdem_JW7PM5zInD5fh1vHoQdAFmeEwBNkKTD2U3dYDLLz2Sqk-3SwdD3hzxknw8SUcMW5hduHHKcRA-5r7BP2-Z18_cjC3Hl44jUCIOAiz-CfOdmiBUwQCscaubfqGNYDCEMB1Exbf3IQfVjZddgJmhXt7wZS_wjnVb2weS1zEMiMxJaLg0o9J7nMmE8EFrqNuejWmyeh5JqPnsY1gr3dNWfcqQdmqmTA7ZX_C5NQPmAqsSnY9G2GeHpwNohKPPzFz2DWyv5BwGKIFB2cSlB0NzimJpRRxJrOM8syPSMhISAMesIBS4ie-jGVc-H4QJUlOwgizwD7ENFFSJH6qIBEzOSrRqI_rPIrfw0ZjOi_0w3Tt5-soeOlH52FwHue_8v1zH5mz2XFUQAphEwcx388-ffcPzU0qbdW5ww3pNriU0C8imkKcGCOMqjFm6USjyPfOE5pRSUBolkU8jlhmR52lDs2oD8v4KVO42yiNFHnGYpqnJEpCaaWYZQIPrO1wAs8MK1I_CAUoTcGKcdgpp2cXt5yus9tPaSDB_tKARnasWQbvgIgflJwrr_SWTfgNUKKJK3AGBeJXYeyV212lWIN6-tTDoSXSxR9F20BwTa7QP79VPrrzhg54bt_AbFeiAhAvew9M3_6Iw6yVl1BOGH4h3rJqACvCibdqTptPUfwUDvZHLSWmprYAVacQAXhyaOHRFoFvu-tXwG3AtaOFAOMGANmSlde0nmza7VCRdS9gCcjK-6GGbfa25BrlxNnKFiQQbOjhcfjvsiWwMR7E86zZiu708FnHCYuSLE5FUcT2fGYpzQPns5StNAOzFJCHwMihL-zAswTmpET3y0iaUSOeZIJRPwyK1I46S1IeEfdeWcfXo7HOFGoLJ3Rlci2wpaBJ6jDhv6HumwHOipvEmVYfVAv4ZT3GFXrsssaz1IqgHlTny0uO-qX0SZZaY5VmzrRtUs1_WUCljBe5hM3JeDLu-ZQpPbA7C6lPCwhxEKQyDHxBRkCYZUOns7x3btMMLNMwITkTNA9GgWfpzmWB75e89DokBFogfTbg9rV5lwDBQf63v_wXwsNsr88P7wRP4hicJexoNO7ELAd6ROBDgZIZPKOiABcOTrwY4XyW5DSDPyhlyWgsQ3AYQIoyFlGZ-BQc2exR8JSkyHxZJAL8iB8UQZZKsK5AZpEAEJ8_WtAkF3EeSRQwKQof6AYKkLNCimA-KhMxiYqcF0ymsUgjQpKY0TynaRokrIhmjwqeAqnII4jRgxgcRRHHIQ9ZBM42YBCW7C3LT3iYJ5FPipiFee5LKnkWFL4Ik4zHr-4I-yzsZUwkkheCZnLy32PO9sg53isDq2_g4cOaqKwEvLgDy0CB4MNtw0FFW_hQAOwPFCK6lYVtpb7aGVx7mmSuPLx9r5puAF9DB0An8BYIMiPq6w89KgBh1L27AJ8DTmLKirWiG6q-O_VeDOAYwZtqy1BG8cjjjTKMTlTCRNEdXtaDYcHgHYNBT73HniQlYKNdkmVmMPSWlDXAnn1gDHRLbW8dfFr3gG8gzpW6JEbnijfzTWW3ZsFLpX5WpDxIkmwiOrM09oHjWkpK24Ez0JoiZX6Wjl5qlqeekO3DEs4WLaSfSk6ESCmxo89y0EfEPgYXsZCC-cDUEzlSq1l-2Yz-kESx9ZCyfAtPjhk4rwIF9cgVHLWKm-AkdXpj3J5HcOhz3saaRkkAcZ2aqUZiNRK3GmyhO_1jHaKoOqT8lX7bw7c7lBdlKTnoUMkA4N807WtU7g40flcNnXavnipAWXk7zKzwlQc8akDrat6sQIJq2NbaZkwyswM78ygErDASGsANgdQeoMWDZNEByeCn6TUUc1KQUAtmuJuRvQdD1qKWNYKBnR3k6roBKKDefYjzgOIKXiLZM2a7uk1-wYavMV8OfGRAi9JmNGd7N2GPS8mDMAlkLkb6NEv5H1PI--TuERdGxUEYGJPHROfqLKBZdVJQsjagaX9pYW1lYVNNDRunt2FL3pbbYeuZpRvw05y-x0yAokyGABC-LXvcH6M1a9SaVmA5jo0GVgqkYPUtgTEJ26ByNa35xMim5deTMDJ0pDJSYa4CY4A9ha_HIhnvl6H3t__4Ty_4bDVXsv1HIvVI-JleH6wLVAOt846Hgs8WkDL3gVCF4MXTgtsTnt2ZHDjhpcuPEW3ymBZ5EAPFtAPP7kMmpPywiw0bJgItCAICTIaNWDa76zgi9r0uLbRLA86n1VaSbVmVojsHdKtJzUoYpjc1a7DrDH6pzwnP44q0pUnq6XzrI68BlFEPwEK_ev7MqCLR6KfPUGssrP5aJ6sxSkDmcOp9ASqmJbj2tkOHcKDCR8SqNRgFPI6Aq0ZB3Jo-UyIiGADaCdA8iBogUCm7zmgszCrBhHr8UWHMysYrYq1xEXS3YsOI9DqLbFBpD17AR1TcwI-HQIi2qONbNk9jTDQE4-rDGuSHOWV-wZNg8rWz66JD4PMh9z7eaKwYBCsXhwaPwZsuQzSAe-p9rTR0cmka8oFyEaUhGFB3AlcA-lTrmA1m2JRw6C3bAEL9aWjLjpdMw4faAwn-WIEZx7c0lCFpGjUBfC3G6xi3a-FAXqsds1NRngf3mgo8RkwONIYxqdyNKqRsMGsAeKv8ynwpj3AT4FeEdxsBSGc2BCcFPgrqU3YbRdRAoGkiUBKca8TKMQpeOFASMUmTVMY8Hb3J7HrtwIEu3JOZcYuEFDKGkdN4pE2zq7MJau5_D2bjzTxJCkpjHkwR1uxqbFniY3wMFDmUPo-SOB_Fnl19jeHbA-6x-tGGjU3X9q19y7WkQKvTDsiFh5o8jTPT_AOWAhrPNoYIkt0OdJlQwER4gcF8JSfserQQk_X6zbAFJHm8w0FIpSYb6m7YYeIbn4F5B0xt1cNWqHiHldb9qhMcRdKFpIhPapCb0cYVpknVc4q0quyOUHkHzRRgaxRaq5fNZQUYz2uBeNc3TYXGVo1BmPkBM2u1Iia1Vn900V2_wKZ8oE00LII4z0dAm10nHgK0D7kb3Ag8PlATjqx2bfJPlmPyEiCnBakNW9XEEbYHXMxXQuxMOkQzbuuVQb9ITyZ0MxEjqTHWbDB4AyaKyZRT76mOCcsanThBIOKA-d4lYuRtP6CKw_H-hFTglAxf1SMoTmYVBzyRgnKvoVjjDfrboYZhgo2jNloMWspa5kHoJyJIAjHShdld6YGdX7r4HPP6WU5yXmRZMtKn2V3oBD0feKdpMzwsSFIswk_FSKJm15yHNOZDritvZ-Bs9tJGSXPgge2eA83oEAjaPygh6IsGB5x2NTfntQocJxp_PTdnPEVjrevRWltx2epab60bKC6EnAKW1M_00xIzr9s0b0wmXaCjtexnfhWwz6aRiZ96z6RdsVoiqJYgbad3qamPZFdX6KRBSHl9Y5NBSXEjMD87nrkWThkFCH-FWIKbokSYR4lwKDuIUfqZwJ0xjdXIOWbPa1zbNkrI6Y3Z1UKzazCDacIQ8XYHITk5wr8Ip4FPg8D3eTgazXSDfUD5lm6ibVI-zEQkwxgMctTq2eX0ZDT3uW-2Kefcz2QEEUcaj_cSsyvoI8Le61a5kaDmYx5kPyCcDh4OE84NLwxUiDgyKK2srGnB1_bohkdT-BFODbxHh6C3RQ0vtfGAUcAkFQH73feUOqScXy1pnB9vkJHZ2mYQjGBemZzA2Y0bC7zag__T9VVQrK_CeN3BEnoQiJ_-qWvqV4_A1WAiAoMisAlF-IyZdiaHh3T6Cq-nbt25v8fTuaNLBWyzH3tUvt2J-vEz7wk41rcnP6jGF7COg7--0eFy-9fGt5vfvyjhUFruvSSgLP-MbTCivirbpsYzvIDfK9nv6obZ4Pn_1GaYNCmKLOAfpwFirXI2u94EVVuV-8BPCVeABO-v26G-owJDJw4PSXZDDFNq8cIqsQJhUlZrzGkLfnteLR1QjX2GMro3c7VpkzJaIrsb707ebK5VKc7tmdRDoBwgGXojxV2nqYxv5HbOcb5ZgPv-A6pPkiyjNM2YFPCPNIwkRAMkD6ctmZeVzEsq5qUm7_6Z1eD-5TY3y02C93cXkxyrrPko5TNpLnIR5kQylhEZhGGUh-DH8iSgReiDiYdhEDM_kTRKwLuRgBIZSspo4aciy9mB9dxVPRPDf3dUzwQhYT6H0NBVz7jqGVc987OsngF0jMJIYHQ4mscMlxfP556QO2UP4VwOEj9LatcqXwXnKGGnNOk7BTMyvmu8p1WGDts91H1ZmfyDYqabpsKlI8fUOnBh73xeaRKqnuJ4M0zucKXqxm0M7kbJr7RlYsoSUzvdI_i1IubKeWDWtsb0I1ZutALCxFLlKFBgpQ86DdprH6uyBbU5rxlVcDVOrsbJ1Ti5GidX4-RqnFyNk6txcjVOrsbJ1Ti5GidX4-RqnFyNk6txcjVOrsbJ1Ti5GidX4-RqnFyNk6txcjVOrsbJ1Th9iq_6fVBxU5QUQQps9aN9sadKbyjnvf4zMLNSAsk79k2FGaWcSX7rC2zB7__6VFcd8IYNSo2n8T07_vEvub3nQPf4SsM8ysMsST6FqAs7OQtTf62p1XPANOE9WZmRr5e-wo-mAaO3vzH304qsriG6G1dpDRijTcstfskvDWhGbnzR0ycXWTGb6QqGjHMYzkOXdrmIo4Sy-O-8yzbwnXi_omOKzaAMq6XvDvTDkEpx49vOPrnIHQKwpp4mFmgFHcpK8XT0nG_uV_w4Q667ix8fc1v5CL4SIBN-mBbXCb0Ya1mnhwDp2NjTkEeRxTOAcnoIUe6e66mQpS4lGIcF4mgTkSrqGaOgiWL3Gx0dmQs4uVYh0OkhZLhH_ajJ1K-85_BUNRr1mF3ewSKRSm8gwvWeQqj4nRAQBUCEjKk0xdYVJpweMvXl5QO5MRVCa2BLiqlPXBtFGMOUfbM9PWSmy9PpGHRoMbnABqDm_HoWz2-BSU9Lh_UaQzw9ZGB3T_bdPNnxI2DjZUt2GwvumpwTNWtrrKQ3jyDrM2p1oBj3WY2UQYfYyNDadS0G0KDKO6ifdM-3gIrZR8Ey1ZO9WroNXyzrXZng4oB8lgXa7ACETL3mvOLDinuJlKHIqZ8XSRCRWDIZp5mf0kPFvWPF5_HiXkeDHA1yNMjRoH9yGnT_boebxfLZ-7tr4f8uxf-Ck5ymzE-FjAMSJnkUJYLzLJch4Yylae5HofQDMNCMF77I4zjFive84CKCTw6s51bxf3IeFOdxcUfxP_eTIAyK0BX_u-J_V_zviv9d8b8r_nfF_0eL_32SpFFWBJSpq0pd2zCFSgd250Nin7ESLM2zvGCiUN-UrXF8Cof2cPzhUYyZNOBJWsg4kfpOSavqFNgcX93xeGTizvvZGzCqYadvc1a3A_QxKQVoMr6FEKpD4_3cj71-mZJAoAR4MQgHj-8gtTTv2YtwU6ALwyswMkUOqmgMi5mUvjRtealQYq_0fDXLCFixz1TJw5mhVWdAJkXdiTOsGisvx_d26hYfBldw6MH_EKNMsdiBst434HCEZ-8-Tr1vdTGqTSi8gqVdWGO7GJf_6tFYsdbZi2lPU3I12f5F2QjTatHKT3JV-6aKXPrNAtSxDFxPkGKp0lT5M0WZx_XneHCID6Av0Cm3b5-8WH__tRecpivwpgqnUWgJ2o4pP1gSIPR3JazcCG_vpnG3K--38c18JNaijKm6NQ4fmoq3m1k7Xc1KTNG9J0lVYQ3kIyzzUgVoJWz2KEkrTA2JN-vQx5Gf_O7p4zUFG-Fw8LYOEL3ToG5AlYvRsKVTX7Oc0XhZOaUazQJw98RbJFmwI3uc68yU-dy4iDVFvMbbngLV3W5FqyTH4oVN2XKIgtv--k6A0X9as1PGpVNzI1-bfACsG5FWjNUPKuukBJzucXWqrAMFxBr0Je6TCZHRIkvjVE5edcoOHFe140H9vqErS9G-5awi17gCU-RjkoRgMjuha0JnK1L-bORyeM29V4pKm7ZewwRlb0qIQOXxchkVwnv-9EuFEp0qr18vlqoCyezLtcIUfQWu6ApSY2RUY0GrqhbS65zqUPRvUe8nZzg9hacKpNVUaFou_Oh2drkbVU3XzuybllZtxZxV1cyc8qpNMrwXVBFrxfQd_OjcljSBA_9JgphxOfXjTUmX45pwPFdiaun2d0Adypk-D1vyujIVJtZfYVSgvKyHltpq0D8zUD-W2K3G4ndd0QxeYjAM1OieaUqCA6Qdkl41vcX0WRYeTv31Xip-VmLnPTboOdZZqJJFWBmCyYRaptgGnvktaV-jKk9qq0CjvUJrbobLja2ytFcDZgX6cgAjMCnsV23okO5m8f68PLasr7RKKxrfKd8MCoJcjk0uaJFoZyEr4jT345EyzVJZxxXheAYKiwY1Ug4t5s8NYBkEmEeO9srAtnWcel-WLeygpUHTtKYAEYOt8SUs_uv6-c5hFKwnIxIRFlvLMAdhAyQVyN4KiVSR1DiqrmtTZAgXtedMDFmB7dezjKGwseL96zYL5raKCtFm1smkRcZYeCAjwdu7ofFU0ZCdv7vjDkVLYDnhrSsaU5hqFbIb_3YOaB1twNHrZZhlLUbRrp_X9fO6fl7Xz-v6eV0_r-vndf28rp_X9fO6fl7Xz-v6eV0_r-vndf28rp_X9fO6fl7Xz-v6eV0_r-vndf28rp_359TPS3wCBJbRT1DM_jus33zTjKEzwnE3UCCTvSkOVK7EZD_GS9L1ZdsM92vpmwl_rF9qf_iar-FnIDcY2mIkhg5QQeF-yxioUtVcqvTgrDDLFmwqemRu80xmHnNz-oLNrO3uXiuT5OeqBoX1h6Qj-yLoIbHNai42YWxokTlrhCfV-oaoM46NcEOFDuiJokMf0k9VEClkFhVZmBUiJ1HG_NwPFMu4s59qLKI_3k_181HD-_eYLf89hanD4O_SUsFlxoB_Sj9PCAdRacRIEvkxjYCJZhn-IQWS4994YHmcpBC6RlnCCkJ4EUYiSJP7_j2F5DxJz4PsjpaKPGQsTxPhWipcS4VrqXAtFa6lwrVUuJYK11LhWipcS4VrqXAtFa6lwrVU_DxaKiB85nmchVnuj05rlsAwmvCQvMOd-SmtJWgxCiwl6Mqt7zRSH477pI8WD1WWb3Fwc6Wn72x084ZCfFCxtlS177aXQ3cZmI4M5eXwKpc2b2du40bzhr5nbLpOKwUKWtamwt2UqpXIhRGmjIYjxQfICZP0PCISAklKEx_iVMHSImRZwJgMiiQiIuG-iAqZpSIhhchixotAsjzwJYuCkMQkf2VA6Ea67Mh-ifJy008bZhLVHvgwAq4B8G9SNV3FqkviZinCm1Z7aH0BEXEIoZJMsyAtMIoKQGWCjBOJJdaw3ARTLiTww0LSMIjjmBYijcJcCi4peYUYeUfWb8rqqSvV1gaVs43YSwOacsXrGgwGr_XnGmbGmi4k9tOJ-7Gp6zlyPUeu58j1HLmeI9dz5HqOXM-R6zlyPUeu58j1HLmeI9dz5HqOXM-R6zlyPUeu58j1HLmeI9dz5HqOXM-R6zlyPUeu58j1HP3je45-eP__qOHJ0w)
