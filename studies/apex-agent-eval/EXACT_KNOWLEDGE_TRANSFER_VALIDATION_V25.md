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

[//]: # (ob:6ffeea75)
[//]: # (ob:v25-b5-result)

[//]: # (ob:b29710e3)
The Stage B.5 primary route has passed its frozen development gate and one-time held-out qualification: PaddleOCR-VL 1.6 through the official MLX server route, pinned to revision `c5630abae1d940eafe0697512a0325494b02ab42`, scored 0.90 text-block F1, 1.00 table-cell F1, 1.00 numeric F1, 0.90 locator rate, 0.80 reading-order rate, 1.00 cross-page-continuation F1, and 1.00 development repeatability on both the development and held-out structural fixture splits where applicable. It completed all 12 ecological documents without failure (peak child RSS 1,112.0 MiB); no extraction result was admitted. The native PDF-text control also completed all 12 ecological documents but deliberately emitted no table cells and scored 0 on the structural cell, numeric, locator, reading-order, and continuation metrics. The DeepSeek-OCR-2 adapter is implemented, but its official route requires a recorded compatible CUDA host; the local preflight rejected before opening source bytes. The complete sanitized record is `results/document-extraction-stage-b5-v25-sanitized.json`. Phase C remains blocked until that sensitivity result and every content-addressed v25 control are frozen.

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
Use two frozen, non-substitutable panels. The byte-reproducible structure-ground-truth conformance panel contains four development and four held-out image-PDF fixtures with exact text, cell matrices, numeric values, page/bounding-box locators, reading order, and cross-page continuation identities; its digest is `sha256:189656cd37c999a826f0cc27e7abe4f6b3acbf4c4ba917a3c9830e921d3adb06`. The ecological panel contains four development and eight held-out private data-room documents selected outcome-blind by source digest; its digest is `sha256:1ae42599f67169323e10af17dafa2ef92c5375ca1029fb21444b9e6328fedfba`. Conformance accuracy cannot be inferred from ecological executability, and synthetic conformance cannot establish real-document generalization.

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

[//]: # (ob:020b892c)
[//]: # (ob:v25-nonlegal-freeze)

[//]: # (ob:c6e3d659)
The frozen non-legal panel is now constructed privately: nine tasks, exactly one row-table, column-table, and missing-or-conflicting-input task in each family. The public sanitized manifest records the panel digest `sha256:fe496b0453e71b08d468324fb111ba524cfe554f7333641c4cddb78db72f4a65`, nine source digests, coverage labels, and the continuing no-admission boundary, while prompts, source values, deterministic gold outputs, and the private task manifest remain outside the repository. This creates a transfer panel; it is not yet an executor result.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFkYzQxNzlhYmViZmY2ZDM1M2M0YTVmZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjRlMmIzNDU3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kMjdhMmZlNjhjYjI1ODUyMzRmNzdjZTUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EzMTU4NmMyNjBmMGU1NmE4NTQ5M2ZiZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfVuPG0eW5l9JVL-0e8hSZuS99LBQW_aO0XbbkDXeBtxGKa7FbJGZ7MxkSWVDwLzNPu8u5ifsD-uHBfZf7DlxyUyyyGTJJXnsnQDcDRWZjDgRceJcv4_86YK2faUo768rcXF1sd1eR4InUV5SJplSmYjTmCc0VepiccEacXctqhvZ9fBst6Ikza7iNCvjPBVxlhSKyySLkihJGSvyJEviqChpJBnlYVjkaaxUVOQKBs9kSmjIQipgXFF1vLmV7d3F1U_4R3_d0xuYYU17nGoB_2ByDS98J9tKVZStZdDK26qrmjpYwfNNexewu-CbtmnUtpVdB5_ZUv6a3khc1N7LbfM3CcvdtTjgqu-33dWTJzdVv9qxS95snvCVrDdVfdPT-qaIwyd7n27l33cV_Pt618n2mjd1J2vYi77dyXeLi5WkuImJJCxO0vzCvHItb_VDsLnyWpCcEiWzgjOSFimJE5XnXKYoWdP2uLTrdVVLkNydyPqaxlFaZJxkoQplmtEiTcpYMWmWY6W75nTb7dawYIJy8qYV3cXV9z9d2Ol_uoBTbtoO_2XeluKawZZ_f7GrX9fNm_riB1iD0wc84H4nKtk9oVv5dgkC1f1S3tL1k8_-8uzTl9d_-vPX_-3Lz57_18-uX7549udvP__sxfV3z7784vmzl198_efr70h6ucGzfR_9on3fVmzXw7FeM9pVHQoh1-qadrDdvdTj7fpV0-IiXlc1Dtnddb3cwDs13eBpu8Us4KMdasjFVb1br2FpfAVHKs2msHXDX8PTaZSWROQMHofT7OVbXPjv_8-__9v__d___gm8aCehQujZt6h28g288v2TJz9cBb8Lft-wq1uSLvuqX0v8RH-31UpHW3rxbjHOJOJSKkXV3kyfvYWtCf4EAq-luJHBp6BRoEwctyCAYYN__Ov_Cl62tO7mZPld8PBxlGyD7-i6ElS_B1dmlBm1FTR_T-ycU7jXmfwIYh9uYdfTftfN7WGekSQvVL4nzLf6Y7P787tgeGhmqTyKQ5Wm2XuOfrgM1Ur5o_zkr_XLlQz0jV5yuV4HtBaBkL1swbqAzar4Ush2ZrEFkWkYy_CR4vx9BzYUzmVuX8uScarU_i34pq02FAyrG-DMDh95fGavlSrjkEn6s2c8tcwlOinY_OeN7IIeTqADsxDcoHuppQgkau5ybitAv5IsZR9MsJVci2bXz21_FmUUbHu8N-c_w-eW8MHg2Tef_SXY0ho84PwJHP_EzCEIXoaKR_lj5j2xXHcMeAe2dvfW8oauzYhBpQ9nZk_CIoSwQbCPIdsart_ceRQsJ3GR8MfMvQxe9bR7fU0UeOssRocdge1KmRSUSEVEHGVxWNJXf63do0WeUS5jIib7gqIeuBEVlYn8KGfWQvjQwaF9ri1YgEIFXzzvFvpfT7pm13IZzOyb4mEWskx8SNnAftJz5gtuTxxCrLY378sVrGIJf4tKuyU30JlLNPOxmZuUZJSqvHy8BKeWf1ZnM1HIguTi0RJEl8Ef_vB1C0vEO8vXtNpc_eEPowXVr3Tam7XSDAca8gYC6KCf0dsoLEtOePbxdgiHbZs1KvAzcLc9jh0MY3cgLZ8zOHFOeZ4S_sEFrJtaW76504OcQJVpuu8B_ozHrm1m7yK3h7iBmY_NaDA4Y55SVT5aglPLdx7h01ZCWheotvlR1ovAWJUlZIivQbnmYj9KSlJ-BAFNRlH1dyDhrhag9dZvQcYD-SbX_guO_1aC15oRkEQyTFmYfHABNxLSIj4fGCchlTQt9ub-ynxOX1Va0_VdV50Lk098ZEZvYpFDHlvGj5r5xIrPGr1SlrwIC_aoyZcB7ZsNnLNN7jeQ6AbdjnNIH_UgHY7XG3doX3-KXhtjyRmLR4okplGcfdCdcZ8BFX0hsWIQSCycGOFwUA6aDFrbwNXqZ3aOJSTP1SMV5lA4IbmuycwdWQrhD80P4utn4pbWEFuY3W62gRvpjLrOfW7OW_M8FKqgj5fh3vGYQdAF2eEwBdlILD1U3SYAW3gXVEq_upo7HvDmXNDow0s42LiZ2WWYZJAD7Wvup-j3A_fxMwdz7-GZ04ikTCKSJz9ztlMLHDMQyDW2bdM3vAErDAlcN9riw034YeHKZRdwrXBvr7n2VzinfsfVseR1onKaMCpLocKEFqHgKpVC4jrqptdj2opeYCt6AV9J_nrbVHWvC5StngmrU-4vLE79gKXAdcXvJiNMy4OTQXTh8WdWDrtG9dcKDkO24OBsgbJj0RWjiVIyyVWeM5GHMSWcEhaJiEeM0TANVaKSMgyjOE0LSmKsAoeQ08RpmYaZNolYydGFRnNcV3HyDjYay3kkJNkyLJZx9DKMr0h0lRT_FIZXIUbOdsdRARmkTQLEfDd59af_0Nqk1lZTO1zRboVLIWEZswzyxATNqB5jUk60ivzgOqEdlUaU5XkskpjnbtRJ6dCO-riKn74Kxy-llaLIecKKjMYpUU6KSSXwxNpOF_DssDILIyJBaUpeDsOONT23uPlyndt-xiIF9y-LWOzGmlTwToj4XsW56tZs2Wi_wZSYwBViBm3Eb0kSVJvtWkcN-unLAIdWGC7-KNsGkmt6i_75rfbRXbDrIM7tG5jtVq7BiFd9AFff_YnDLLWX0E4Y3pBv-XoHtwgn3ug5XT1Fx6dwsD8aKbE0tQFTdQkZQKB2LTzaouHbbPsFxDbg2vGGQMQNBmRDF0HTBqppN7s1XfYSloBReb-rYZuDDb1DOXG2qgUJJN_18Dj8d9NS2JgA8nnebGR3efqsk5THaZ5ksiwTdz6TkuaJ85mrVtqBeQaWh8LIJJRu4EkBc1Sih1Uk7aixSHPJWUiiMnOjToqUZ8R9UNXx9XBZJwq1gRO6tbUW2FLQJH2Y8N-u7psdnJWwhTOjPqgW8GY95BVm7KrGszSKoB_U5ysqgfql9UlVRmO1Zk60bVTN_zJjlXJRFgo2JxfpsOdjpfTE7syUPp1BSKIoUyQKJR0MwqQaOp7lg2ubdmCVkZQWXLIiGgSelDvnBX5Y8TLoMCAwApmzAbdvrncFJjgq_vGv_xPNw2Svr07vhEiTBJwl7Gg87MSkBnpG4FOJkh08Z7IEFw5OvBzM-aTIaQd_VMmSs0QRcBgQFOU8ZioNGTiyyaPgKWmZh6pMJfiRMCqjPFNwuyKVxxKM-PTRkqWFTIpYoYBpWYYQbqAABS-VjKajcpnQuCxEyVWWyCymNE04KwqWZVHKy3jyqBQZBBVFDDl6lICjKJOECMJjcLYRh7Rkb1lhKkiRxiEtE06KIlRMiTwqQ0nSXCSvjqR9zuxhN1eJUrJcjf57qNmeOccHVWBNBx5erKmuSsAHt3AzUCB4cdMIUNEWXpRg9ncMMrqFM9tafY0zuAtMkLkIsPu-brod-Bq2A-sE3gKNzGD1zYsBk2BhdN9dgs8BJzFWxVrZ7dZ9dxm82IFjBG9qboa-FE8D0eiL0cm1tFl0h816uFgweMdh0MvgWaBoBbbRLclFZjD0hlY1mD33wJDoVua-dfBq3YN9A3FudZMYnSt25pu125oZL5WFeZmJKE3zMdCZlLFPHNdcUdoNnIPWlBkP82zwUpM69WjZ3q_g7KyFCjMlqJQZo270SQ36jNjnzEUileQhROqpGkKrSX3Zjv6YQrHzkKp6C08OFbhgDQoa0Fs4ap03wUma8sawPU_h0KdxG28aLQHkdXqmGgOrIXCr4S50l3-tCYpqUsp_Mp8O8NMdyouyVAJ0qOJg4N807WtU7g40frvedca9BhqAsgi2WFkRiwDiqB3erubNAiRY7za1uTO2mNnBPQsYJKwwEl6AA4H0HuCNB8niE5LBX-PHUMxRQYgRzMZuVvYeLrIRtarRGLjZQa6u20EIaHYf8jwIcaWoMNiz13ZxP_iFO3yH9XKIR3Z4o8w1mkZ7h2ZPKCUikkaqkEP4NCn5n1PIh9Tu0S4MioNmYCgeU1OrcwbNqZM2JUtrNN2bzqwtnNnUU8PGmW3Y0LfVZrcJ7NKt8TMxfY-VAB0y2QCAik3V4_5YrVmi1rQS4TguG1hoIwWrbymMSfkKlatp7StWNiO_mYTTXUfXViqsVWAOsKfw9QCSCX5Pgn_89_8RRJ8spkq2_0isHyGfmPXBukA18HYeeSj6ZMZSFiEEVAS8eFYKd8KTnsmJE55rfgzWpkhYWUQJhJhu4Ek_ZLSU79fYcGkihAVRRCGS4YMtm_Q6zoj9oKaFcWkQ8xm1VXRTrSvZXYF1q2nNKximt5g12HUOb5pzwvO4pW1li3qm3vo0aMDK6AdgoX_65guritRYP3OGRmNh9XemWI1ZAkYOl8FnoGJGgrtgs-vQHOj0EW3VEi4FPI4GV4-Cdmt8TYuIxgCsnQTNg6wBEpWq66zGwqwKrlCPf2obs3D5ilwauwi6u-a7wdKbKrK1SnvmBXzEWljzE6AhxLto8ls-LWOMYQjm1ac1KCQF42Ep0mj0tZN20Snj8z59n2C4rJgEaxeHFx6TNwNDtAb3MvhSa-jo0ozJh5CLag3BhLqTuALQp9rkbDDDqoJDb_kKLNTfdm3ViYob86H3QIE_1sZM4KeMKcOgadAE8LWYr2PeboQDeZ12TE5Fex7caybxGLE40NiISdduNJCywaoB2FvtV6ZLeYqbAG9R0a0kWDq7ITgpxKOgPlW30oEaCDROBEqCcw22csiCZw6UxlyxNFOJyAZvMmmvnTjQmT6ZHbdMaakSGDlLhrBp0jobTc3D-2Au3yzStGQsEdGYYU1aY_MSn4vHQJGJCkWcJsUg9qT1NaRvj-hj9cMdtne6dp_av7kuKDDqtIXgIkBNHseZaP6JmwIaz1c2EKTbLegyZWAT4QMc5qsE5XfDDbFVr3_ebcCSPNviIHStJ9vV3W6LhW98BubdYWmr3m2kznd45dyvPsFBJAMkRfukBznMNm6xTKqf00Grru5IXXcwkQJsjbbW-sO2WQGX57VEe9c3zRov23pIwuwfWFmrdWBSG_VHF931M9FUCGETI2WUFMVg0CbtxFMG7X16gyuJxwdqIjCqXdr6k4sxRQUmpwWpbbRqAkfYHnAxf5Jya8shJuJ2Xhn0i_Z0tG42Y6Q15poNJm8QiWIx5TJ4bnLCqkYnTtEQCbD5wQ3ayPt-QIPDsX9C1-CUbLxqRtAxmVMc8ETalAcNQ4w36G-HGoYFNoHa6GzQXNWyiEiYyiiN5BAuTHqlJ3Z-rvE51PXzghaizPN0CJ8mvdDR9LxnT9NVeHiUZkKVkG0OQdSkzXlKY96nXXm_Aueqly5Lmhoe2O6poRkcAsX7D0oI-mKMA067mF7npU4cxzD-bnqd8RTtbV0Ot7WVN63BehvdQHEh5ZSwpH6iny4wC7pV88ZW0iU6Whf9TFsB-9E0RuKXwRfKrVgvEVRL0rYzu9TUZ6qrC3TSIKS6O9hkUFLcCKzPDmduhNOXAoS_RVuCm6JFmGaJcChbyFH6icCdvRqLIeaYPG_s2qbRQo6fmLQWmm2DFUybhsi3W0jJ6Zn4iwoWhSyKwlCQ4dKMHewTyjfXiXZFeZLLWJEELuSg1ZPm9HhpHtJvdiXnIsxVDBlHlgx9iUkL-oywD-oqNwrUfKiD7CeE48HDYcK5YcNAp4hDBGWUlTct-Noe3fBwFX6EUwPv0aHR26CGV-bywKWASdYU7u--pzQp5bS1ZOz80EHGyNaRQTCDeWVrAk8OOhbY2oP_Z8vbqFzekmTZwRJ6EEhc_q1r6ldPwdVgIQKTIrgTOuCz17SzNTwMp2-xPXWv5_4OT-cISwXuZj9wVL7eyvrZF8Gn4FjfXvygiS9wO06-fcBwuf-29e32_RcVHEorgpcUlOXXSIOR9W3VNjWe4TW8r2U_xoZZ4fn_XDJMlpZlHokPQ4BY6prNtrdJ1UbXPvBVKrRBgs8v2119BIFhCoenJDsQw0ItXjgl1kaYVusl1rSluD-vkQ5Cjf0IZXBvtrXpijJGIrcbP128Wd1pKM79mfRDoBwgGXojHbuOU1nfKNycw3yTBPfde6BP0jxnLMu5kvCPjMQKsgFakHFLprCSKaRiCjX56desBg-H2xzCTaJ3x8Ek55A1HwQ-kxWykKSgivOcqoiQuCDgx4o0YiUJ4YoTEiU8TBWLU_BuNGJUEcU4K8NM5gU_sZ5j6JkE_juCnokI5aGA1NCjZzx6xqNnfpPoGbCOMYklZofD9ZjY5dnzeaDJHauHcC4nAz8X1C51vQrOUcFOmaDvEq6R9V1Dn1ZfdNjuXd1Xa1t_0JHpqlnj0jHGNDpw7Xo-r0wQqp8S2BmmR1yp7rgNyd0g-a25mViyxNJO9xTe1oG5dh5Yta2x_IjIjVZCmljpGgUKrPXBlEF742N1taC25zUJFTzGyWOcPMbJY5w8xsljnDzGyWOcPMbJY5w8xsljnDzGyWOcPMbJY5w8xsljnDzGyWOcPMbJY5w8xsljnDzGyWOcPMbpY3zV76PATXFaRhlEqx_siz11eUM77-XfITKrFAR5576pMGdMcCXufYEt-P0_XhrUgWj4TqvxOH7gxj__JbcPHOgBX2lYxAXJ0_RjiDqzk5M09Y8mtPoGbJoMPl3Yke_mvsKPZRFn978x9-OKrNsQ3UErrYHL6Mpys1_yyyKW04MvevroIuvIZmzB0GEOG_OwuV0ukzhlPPmFd9klvmPcr8MxHc2gDIu57w4MCWFKHnzb2UcXuUMDbEJPmwu0ku2qtY7T0XO-eRj4cWK5joMfnwmHfARfCSYT_hgX10mzGHezLk8ZpHNjj0OetSyBNSiXpyzK8bmeS1UZKMEwLASOrhCps54hCxpD7H5lsiPbgFNLnQJdnrIMD8CP2kr9IvgGnloPl3qoLm9hkRhKryDDDZ5DqvitlJAFQIaMpTQdrWubcHnqqs8vH4IbixBaQrSkI_Ux1kYRhjRl_9penrqm89OZHHTXYnGB7yA0F3eTfH4DkfS4dFivvYiXpy7Y8cm-nRY7fgTbeNPS7coZdxOcUz1ra29Jbx_BqM-q1Qkw7hc1hgwmxcYIrV3WcgcatA5O6ifb8y2gYu5RuJn6yV4v3aUvLupd2OTihHwuCnTVAUiZehPzyvcD91KliCxYWJRpFNNEcZVkeZixU-DeAfF5HtzrwyAfBvkwyIdBv_Iw6OFsh0OwfP7uOBb-FwH_S0ELlvEwkyqJKEmLOE6lEHmhCBWcZ1kRxkSFEVzQXJShLJIkQ8R7UQoZwysn1nMP_J9eReVVUh4B_4swjUhUEg_-9-B_D_734H8P_vfgfw_-Pwv-D2maxXkZMa5blQbbMKZKJ3bnfXKfAQmWFXlRclnqb8o2dnxMh_bs-OOzGDtpJNKsVEmqTE_JqOqY2Jxf3fl8ZIyd96s3cKl2W9PNWdxP0IeiFFiT4VNoQk1qvF_7ce2XsQgESoCNQTh4_AyGlvZzrhFuAbowvDZGFuSgQWMIZtL60rTVjbYSe9DzxaQi4MR-oiEPT2xY9QSCSVl38gmixqqb4XNb3cWHwbU5DOD_0EZZsNgJWO8bcDgycL2Py-BrA0Z1BYVXsLRrd9muh-W_ejog1jrXmA5MSK4n22-UDWZaL1r7SaGxbxrk0q9mTB3PwfVEGUKVRuTPmGWe15_zySE-gL7AlNy-_vTF8rsvg-gyW4A31XYahVag7VjygyWBhf62gpVb4V1vGnd7HXyVHNYjEYsylOqWODyxiLfDqp1Bs1ILug8UXa8RA_kUYV4agFbBZg-StNJiSIIJQx9H_vRfnj9bMrgjAg7e4QDRO-10B1S7GGO2TOlrUjMampVjqdEuAHdPvsUgC3ZkL-Z6YmE-B41YC-K13vYSQt3NRrZacgQvrKpWQBbc9ndHDYz5ac1OXy5TmhvitdEHwLrR0soB_aCrTlrAsY9rSmUdKCBi0Odin1zKnJV5lmRq9KpjdeC8qp1P6vcvur4pxrc8WdM7XIEF-dgiIVyZrTSY0MmKtD8bYjlsc-9BUVnT1kuYoOothAhUHpvLqBDBN88_11ai0_D65SxUFYLMvlpqm2Ja4DpcwdAYI6oB0KrRQmadIw7FvIt6PzrD8Sk8VQhaLULTxcJP71eXu0HVDHZm_2oZ1daRs0bNTENevUk27gVVRKyY6cEPzm1OEwTEP2mUcKFGPt5YdDmvCedrJRZLt78D-lCemPNwkNeFRZg4f4VZgfayAd7U1hj9J9bUDxC7xQB-N4hm8BI7G4Fa3bOkJDhA1mHQq6d3Nn1ShYdTf71Xip9A7IJn1noOOAsNWYSVoTEZrZYF28AzX9H2NaryqLbaaLS3eJub3c3KoSxda8CuwDQHMANT0n3VhknpDsH7U3hsVd8aldZhfKd9MygIxnJ8dEGzgXZOeJlkRZgMIdOklHVeEc5XoBA0aCzlrsX6uTVY1gJMM0fXMnC0jsvg86qFHXRh0DitBSBisjV8CMF_XT_dOcyCzWRUoYVFahnWIFyCpBPZeymRBkkNoxpcmw6GcFF7zsQGK7D9ZpYhFba3eL_d5oy5Q1GhtZkwmYzImAvv6BDg7XVoAg0acvN3R3ooRgIXE95r0VhgqlPIbvjtHNA61oCjN8uwy5rNoj2f1_N5PZ_X83k9n9fzeT2f1_N5PZ_X83k9n9fzeT2f1_N5PZ_X83k9n9fzeT2f1_N5PZ_X83k9n9fzeT2f97fE56UhhQCWs48AZv8XxG--aYbUGc1xt2MQTPYWHKhdia1-DE3S5U3b7B5G6ZsIf44vtT98LZbwNwQ3mNpiJoYOUJvCfcoYqNK6udHlwQkwywE2dXhku3m2Mo-1OdNgs2s7zrWyRX6hMSi8PyUd3RfBDIk0q6nYlPNdi5GzsfB0vTwQdRJjo7lh0iT0VIdD78OnKqmSKo_LnOSlLGic87AIIx1lHOVTDSD683yq344aPpxjNv97CiPD4BehVAiVc4g_VVikVICoLOY0jcOExRCJ5jn-kAIt8DceeJGkGaSucZ7yklJRklhGWfrQ31NIr9LsKsqPUCoKwnmRpdJTKjylwlMqPKXCUyo8pcJTKjylwlMqPKXCUyo8pcJTKjyl4rdBqYD0WRRJTvIiHJzWpIBhNeExdYej9SmjJXhjtLFUoCv3vtNIvzjskzlaPFRVvcXBbUvP9GwMeUNbfFCxttLYd8flMCwDy8jQXg5buax5O3EbB-QN02dsus4oBQpa1RbhbqFqFcbCaKashmOIDyaHpNlVTBUkkoylIeSpkmcl4XnEuYrKNKYyFaGMS5VnMqWlzBMuykjxIgoVjyNCE1q8skbooFx2Zr9kdbPqxw2zheoAfBgF1wD2b1Q1g2I1kLhJifDw1p5aX0RlQiBVUlkeZSVmURGoTJQLqhBiDctNseRCo5CUipEoSRJWyiwmhZJCMfoKbeSRqt9Y1dMt1dYllZON2CsDWrjiXQ0XBtv6Uw2zY40Nif1y4n5u6jlHnnPkOUeec-Q5R55z5DlHnnPkOUeec-Q5R55z5DlHnnPkOUeec-Q5R55z5DlHnnPkOUeec-Q5R55z5DlHnnPkOUeec_Rr5Rwd8IY4EoYgjpCQhtys-l8lNWhFWzyxa3hPhw7H2EEGKjPSgw7X9QvThCBU0a0rFGi3YRL3_vvvL9D7RUWJF-2HH06QLh5CURGpDKOEJBlISyXhUpEyFSobKUEMdmoJKQ4GLA5CBfZni71S0CuBdnHc6mBkUw20loHI8AvSWh6xbQ_i7wzcjmGiA7rKyN74RegqGc1UThNVsDiRKctpyKMQGy6KSMZJyCDzCTMiRBxDkEMjERexzOBpkcaUJvHpJd1jrGRXaXSVxEcYK3mSC2wYecaKZ6x4xopnrHjGimeseMaKZ6x4xopnrHjGimeseMaKZ6z8NhgrVEUlF1mYpyPw9bGMFXbXYyxs6sb6Yv2n57CYUgwXcc7LsqQFyVTIOcllDrl8ojIWU84UZOqMllFOY14WcShLEomYChZmnsPiOSyew-I5LJ7D4jksnsPiOSyew-I5LJ7D4jksnsPiOSyew-I5LJ7D4jksnsPiOSyew-I5LJ7D4jksnsPiOSyew-I5LJ7D4jks_ndzftHfzcnA2yOq-JDZYfDiJ3-M5N4lSZdGf45daTcXxDV5FGrv-j5zoSKPyEfXlTHNWrjZBukrdKvf_YjNoPYP-_2dySYc__2dZ_inNpOjIDaJRWCJ5MZMnljs8TFfuMunDQxCgDTMzdX2XWHM-LUBpoagr-XNpIZ34pd5zOhaZDf-KPoxtI51EC5XHdqiN_rivs_P6wgqRcZh8XkeInAi4lQSUPdTP68z0FPO85D-82nrw3lhhz9rQ94d5wD9IrynMpYZZSFJSUjKgqcki0L4J2R4vOAZl1LlgoukjGiU0bxIBYfYmzMmchFmkqQn1nOM9BRfReQI6SnKZKli6X-mx5OePOnJk5486emjkZ6UJAX4eMXIpGc8OupTadWcD3bFsDgqEhUSRvmYXY5u2Y78GI_b6_jGEozgnKvNpNyxFyZd3aMhYNNHw_z2eAhfffmXQGOuWofE2FZ1be4rBgm6EPqKp1kcUkZlJMoklFTJMCvzNCI0jAn41wR8J2UJebUwOAkRhJdlqPGWS8Mh-TxagBBhOLVAw2sOkYkv6A86TCVW5_ClInTQy6WGXto39IdH3PByDzeMg-FG6YemW2gAbq6Uix2Rxnb6DyG-w9Y6SCTWZgwcOui2azwiS3ux1eG11LmyK00LjTGJyLEftBwLTYgXwRF_r_GecO_XInjx7bdBtIgichkGX1V__ESjCSaoORsEv0H1d7VCbYVtofib558vdc3XXlgQRP9-5UPkMlWadcWkRRNK2xBxgIZJicadtqsqTTYKH5oUuu2RLvYPcjH0CYdzs60Gs5wDvgsYw21vkPiDC0J6iqFQTUkt-jrZMp-BK95npCDBRdNSnk6IN8NXNMBH_mZQ27Y8jGQfjbgw3SQE4rtWuN3XYCg22Pn2rPQRfoqrVqTaUh-UKi6HpOa4oe5XtN8n_4yZ0QBGOTTJI8hUu1pjYTxF1FNEPUXUU0Q9RdRTRD1F1FNEPUXUU0Q9RdRTRD1F1FNEPUXUU0Q9RdRTRD1F1FNEPUXUU0Q9RdRTRD1F1FNEPUXUU0Q9RdRTRD1F1FNEPUXUU0Q9RdRTRD1F1FNEPUXUU0Q9RdRTRP_DKKIhCVlR6jx-JMLNpNsPpuENebRl1MyQ8XgmY5Gl5aNleDk2BEfbPzRuYFfG4AKDH6OV67urAOLUh5FJJ9s1Ryalp8QwDKiTvNLJTpzhldpmKi7AwJuMB3F3c-CxjHDK41RS125AMPyJHZ9Gc0NrwEJ83o87SiA1VzIrIMKF9IjEicqxZ3KKOzqw_M5zR70an1bjhzN451mmI-nyF2GZqlRmApSEKVHkYQx6EkZlGbKcMMbAXEpRhGVKylxQcOsJKZOoJAT8OeUso5oc-SCWaX4VxldpeoRlmkjC4iT1P63nWaaeZepZpp5l6lmmnmXqWaaeZepZpp5l6lmmnmXqWaaeZepZpp5l6lmmnmXqWaaeZepZpp5l6lmmnmXqWaaeZepZpp5l6lmmnmXqWaaeZepZpp5l6lmmnmXqWaaeZfpbZJlCLClELhiZYOwmiNNzZ3waOup8eQYxrkqTVJZD0jxBk05AKj8XFipd61LvliatmCPTp-KcjPtLGypzMnB-y8nJLI3110ESKKQctcFYF91k4JOe-4BDNr0FY9eM0Las4splSiZlxsIkjWUesbAQSVbEJFEsiiJGU5JwJdM0gWg-jrMk4gkXguUF_I-ohGbpq4VZ6GEQO1DItI_tFnvgp6reob7VzXJsSY11ozerSsO8ELzWDQUiVyg9onLWj41zuPKi3rDJXujmGjzdgXe1pKVt01XIwrVpueknYmC6b4yw2uhi0zvZj0irCSjb06U9XdrTpT1d2tOlPV3a06U9XdrTpT1d2tOl_3-gS__w7v8B03iP6g)
