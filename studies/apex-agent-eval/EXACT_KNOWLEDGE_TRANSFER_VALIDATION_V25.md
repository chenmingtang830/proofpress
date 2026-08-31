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

[//]: # (ob:b933210a)
[//]: # (ob:v25-ablation-projection-contract)

[//]: # (ob:e1ce66fa)
The condition projector is frozen as `phase_c_ablation_contract.py` before any Phase C executor run. It produces content-addressed projections over the same graph and source manifest: all conditions retain the identical claims and authority nodes; only condition 2 adds source-bound table cells, and only condition 3 adds derivations that bind existing table-cell IDs. The projection itself retains `automatic_admission=false` and `human_approval_required=true`; it cannot convert research candidates into governed reuse.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFkYzQxNzlhYmViZmY2ZDM1M2M0YTVmZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImMzYzdjMTNmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kNTQxOGJkNzVhYTY2ODcwNDgzYjUxZjkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EzMTU4NmMyNjBmMGU1NmE4NTQ5M2ZiZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfVuP3EaW5l8hql_aPZkl3i8lDBZqy94x2m4bssfbgNsoxbWKVmYym2SWVDYEzNvu885gfsL-sH5YYP7FnBMXkpmVN7ksjY05gLuhyiSDJyJOnOv3MX-6YG1fayb661peXF2s19eRFGlUVIwrrnUukywRKcu0vphd8EbeX8v6RnU9XNvdsjjLr2SieB7qKJI8qpTKiiRhcViqkHNRxRlTRREXVcFVqYusKnme8YSxCj5N4oQpBuPKuhPNnWrvL65-wj_6657dwBMWrMdHzeAfXC3gg29VW-ua8YUKWnVXd3WzCm7h-qa9D_h98FXbNHrdqq6De9ZMvGI3Cie19XHb_KBgupsWB7zt-3V39eTJTd3fbvilaJZPxK1aLevVTc9WN2USPtm6u1V_29Tw7-tNp9pr0aw6tYK16NuNeju7uFUMF1EkohBRgiuGn1yrO3MRLK66llkalVwWGWN5XhZhWiY8i3SFkjVtj1O7XtQrBZL7HVlcsyTKylzEsMyhynJWZmmVaK7sdJx014Ktu80CJhyjnKJpZXdx9d1PF-7xP13ALjdth_-yXyt5zWHJv7vYrF6tmteri-9hDl4fcIP7jaxV94St1Zs5CLTq5-qOLZ588pdnH39z_ac_f_m_Pv_k-f_85PqbF8_-_PWnn7y4_vbZ5589f_bNZ1_--frbOLtcyovZO-kX6_u25psetvWas67uUAi10Nesg-XulRlv0982LU7iVb3CIbv7rldL-GbFlrjbfjIzuLVDDbm4Wm0WC5iauIUtVXZR-KIRr-DqLMqqWBYcLofd7NUbnPjv__-__-__-H___hF86B7CpDRPX6PaqdfwyXdPnnx_Ffwu-H3Dr-7ibN7X_ULhHf392igda9nF29n4JJlUSmumt570yRtYmuBPIPBCyRsVfAwaBcokcAkCGDb4-7_8W_BNy1bdMVl-F5w_jlZt8C1b1JKZ7-DIjDKjtoLmb4ldCJaWOlfvQezdJex61m-6Y2tY5HFagB3ZEuZrc9vR9fldMFx0ZKpwZkOdZfk7jr47Dd0q9aP66K-rb25VYE70XKjFImArGUjVqxasC9isWsylao9MtoxVFiYqfKQ4f9uADYV9ObauVcUF03r7FHzV1ksGhtUPcGKF91x-ZK21rpKQG-v_8554aJpzdFKw-M8b1QU97EAHZiG4QfeyUjJQqLnzY0sB-pWCj_rFBLtVC9ls-mPLn0c5A9uebD3zn-C-OdwYPPvqk78Ea7YCD3h8B_bfcWQTpKhCLaLiMc89MF2_DXgG1m71FuqGLeyIQW0258iahGWoOJP8fci2gON3bD9KDsFJmYrHPHsevOxZ9-o61uCt8wQddgS2K-NKsljpWCZRnoQVe_nXlb-0LHImVBLLybqgqDtuREdVqt7LnrUQPnSwaZ8aCxagUMFnz7uZ-deTrtm0QgVH1k2LMA95Ln9J2cB-slPmC05PEkKstvXcb25hFnP4W9bGLfmBThyiI7cdOUlpzpguqsdLcGj6J3U2l6Uq40I-WoLoMvjDH75sYYp4ZsWC1curP_xhtKDmk854s1bZ4UBDXkMAHfRH9DYKq0rEIn9_K4TDts0CFfgZuNsexw6GsTuQVhwzOEnBRJHF4hcXcNWsjOU7tnssBoeYZdse4M-47cZm9j5yO8cNHLntiAaDMxYZM4nI4yQ4NH3vET5uFaR1gW6bH9VqFlirMueQrYFyHYv9WFzF1XsQ0GYUdX8PEm5WErTe-S3IeCDfFMZ_wfbfKfBaRwSMIxVmPEx_cQGXCtIicTwwTkNIpbNy69lf2PvMUWUrtrjv6lNh8oFbjuhNArlsmVXJo558YMYnjV6lKlGGJX_Uw-cB65sl7LNL7peQ6AbdRghIH80gHY7XW3foPn-KXhtjySMWLy7ThEVJ_ouujL8HVPSFwopBoLBwYoXDQQVoMmhtA0erP7JyPI2LQj9SYXaFk0qYmsyxLcsg_GHFTnz9TN6xFcQWdrWbdeBHOqGux-475q1FEUpdssfL8GB77CDogtxwmIIsFZYe6m4ZgC28D2ptPr09tj3gzYVk0S8v4WDjjjxdhWkOOdC25n6Mfj_wt5_YmAcXH9mNSKk0iov0Zz7t0ATHDARyjXXb9I1owApDAteNtnh3Eb6f-XLZBRwrXNtrYfwVPtN84-tY6jrVBUs5U5XUYcrKUAqdKalwHqumN2O6il7gKnqBuFXi1bqpV70pULbmSVid8n9hcep7LAUuanE_GWFaHpwMYgqPP7Ny2DW6v9awGaoFB-cKlB2PrjhLtVZpoYuCyyJMWCxYzCMZiYhzFmahTnVahWGUZFnJ4gSrwCHkNElWZWFuTCJWckyh0W7XVZK-hYXGcl4cxvk8LOdJ9E2YXMXRVVr-QxhehRg5uxVHBeSQNkkQ8-3k05_-S2uTRltt7fCWdbc4lTisEp5DnpiiGTVjTMqJTpHPrhO6UVnEeFEkMk1E4UedlA7dqI-r-JmjsP9QOinKQqS8zFmSxdpLMakEHpjb4QKeG1blYRQrUJpKVMOwY03PT-54uc4vP-eRhvOXRzzxY00qeAdEfKfiXH1nl2y032BKbOAKMYMx4ndxGtTL9cJEDebqywCH1hgu_qjaBpJrdof--Y3x0V2w6SDO7Rt42p1agBGv-wCOvv8Th5kbL2GcMHyh3ojFBk4RPnhpnunrKSY-hY390UqJpaklmKpLyAACvWnh0hYN33LdzyC2AdeOJwQibjAgSzYLmjbQTbvcLNi8VzAFjMr7zQqWOViye5QTn1a3IIESmx4uh_9uWgYLE0A-L5ql6i4P73WaiSQr0lxVVer3Z1LSPLA_x6qVbmCRg-VhMHIcKj_wpIA5KtF5FUk3aiKzQgkexlGV-1EnRcoT4p5VdXw1HNaJQi1hh-5crQWWFDTJbCb8t1n1zQb2SrrCmVUfVAv4cjXkFXbseoV7aRXBXGj2V9YS9cvok66txhrNnGjbqJr_44hVKmRValicQmbDmo-V0gOrc6T06Q1CGkW5jqNQscEgTKqh416eXdt0A-s8zlgpFC-jQeBJufO4wOcVL4MOAwIrkN0bcPv2eNdggqPy7__yr2geJmt9dXglZJam4CxhRZNhJSY10BMCH0qU3OAFVxW4cHDi1WDOJ0VON_ijSpaCpzoGhwFBUSESrrOQgyObXAqeklVFqKtMgR8Joyoqcg2nK9JFosCITy-teFaqtEw0CphVVQjhBgpQikqraDqqUClLqlJWQuepyhPGslTwsuR5HmWiSiaXKplDUFEmkKNHKTiKKk1jGYsEnG0kIC3ZmlaYybjMkpBVqYjLMtRcyyKqQhVnhUxf7kn7vNkrhMq0rBQv9Oi_h5rtiX08qwJrO_Dw4YqZqgTcuIaTgQLBh8tGgoq28KECs7_hkNHNvNk26mudwX1gg8xZgN33RdNtwNfwDVgn8BZoZAarbz8MuAILY_ruCnwOOImxKtaqbrPou8vgxQYcI3hTezLMoXgayMYcjE4tlMuiO2zWw8GCwTsBg14GzwLNarCNfko-MoOhl6xegdnzFwyJbm3PWwefrnqwbyDOnWkSo3PFznyz8EtzxEvlYVHlMsqyYgx0JmXsA9t1rCjtBy5Aa6pchEU-eKlJnXq0bO9WcPbWQoe5lkypnDM_-qQGfULsU-YiVVqJECL1TA-h1aS-7EZ_TKHYe0hdv4ErhwpcsAAFDdgdbLXJm2AnbXljWJ6nsOnTuE00jZEA8jrzpBUGVkPgtoKz0F3-dRWjqDal_Ad7d4B3dygvylJL0KFagIF_3bSvULk70Pj1YtNZ9xoYAMosWGNlRc4CiKM2eLqa1zOQYLFZruyZccXMDs5ZwCFhhZHwAOwIZNYATzxIlhyQDP4ab0MxRwWJrWAudnOy93CQraj1Co2BfzrI1XUbCAHt6kOeByGukjUGe-7Yzh4Gv3CG77FeDvHIBk-UPUbTaG_X7EmtZRRnkS7VED5NSv6nFPKc2j3ahUFx0AwMxWNma3XeoHl1MqZk7oym_9KbtZk3m-bRsHB2GZbsTb3cLAM3dWf8bEzfYyXAhEwuAGByWfe4Pk5r5qg1rUI4js8GZsZIwexbBmMycYvK1bTuEyebld8-RLBNxxZOKqxVYA6wpfCrASQT_D4O_v5__m8QfTSbKtn2JYm5JP7Izg_mBaqBp3PPRdFHRyxlGUJAFYMXzyvpd3jSMzmww8eaH4O1KVNelVEKIaYfeNIPGS3luzU2fJoIYUEUMYhkxGDLJr2OE2Kf1bSwLg1iPqu2mi3rRa26K7BuK7YSNQzTO8warLqAL-0-4X7csbZ2RT1bb30aNGBlzAUw0T999ZlTRWatn91Dq7Ew-3tbrMYsASOHy-ATUDErwX2w3HRoDkz6iLZqDocCLkeDa0ZBuzV-ZkREYwDWToHmQdYAiUrddU5j4akajlCPfxobM_P5ippbuwi6uxCbwdLbKrKzSlvmBXzEQjrzE6AhxLNo81sxLWOMYQjm1Yc1KIxLLsJKZtHoayftokPG5136PsFwWDEJNi4ODzwmbxaG6AzuZfC50dDRpVmTDyEXMxqCCXWncAagTyubs8ETbmvY9FbcgoX6YdPWnayFNR9mDTT4Y2PMJN5lTRkGTYMmgK_FfB3zdiscyOu1Y7IrxvPgWnOF24jFgcZFTKZ2Y4CUDVYNwN4avzKdylNcBPiKye5WgaVzC4IPhXgU1Kfubk2gBgKNDwIlwWcNtnLIgo9sKEuE5lmuU5kP3mTSXjuwoUf6ZG7cKmOVTmHkPB3CpknrbDQ15_fBfL5ZZlnFeSqjMcOatMaOS3wqHgNFjnUokywtB7Enra8hfXtEH6sfzrA70yt_1_bJ9UGBVac1BBcBavI4zkTzD5wU0Hhx6wJBtl6DLjMONhFuEPC8WjJxP5wQV_X6p80SLMmzNQ7CFuZhm1W3WWPhG6-B526wtLXaLJXJd0Tt3a_ZwUEkCyRF-2QG2c027rBMaq4zQaup7ihTd7CRAiyNsdbmZtesgMPzSqG965tmgYdtMSRh7g-srK1MYLKy6o8uuuuPRFMhhE08rqK0LAeDNmknHjJo79IbvFW4faAmEqPauas_-RhT1mByWpDaRas2cITlARfzJ6XWrhxiI27vlUG_WM9G6-YyRrbCXLPB5A0iUSymXAbPbU5Yr9CJMzREEmx-cIM28qEfMOBw7J-wBTglF6_aEUxM5hUHPJEx5UHDEeMN-tuhhmGBTaI2eht0rGpZRnGYqSiL1BAuTHqlB1b-WONzqOsXJStlVRTZED5NeqGj6XnHnqav8Igoy6WuINscgqhJm_OQxrxLu_JhBc5XL32WNDU8sNxTQzM4BIbnH5QQ9MUaB3zsbHqc5yZxHMP4--lxxl10p3U-nNZW3bQW6211A8WFlFPBlPqJfvrALOhum9eukq7Q0froZ9oK2I6mMRK_DD7TfsZmiqBairWdXaVmdaK6OkMnDULq-51FBiXFhcD67LDnVjhzKED4O7QluChGhGmWCJuyhhylnwjcuaMxG2KOyfXWri0bI-R4x6S10KwbrGC6NES9WUNKzk7EX0zyKORRFIYyHg7N2ME-oHzHOtG-KB8XKtFxCgdy0OpJc3o8NOf0m33JuQwLnUDGkadDX2LSgj4h7Fld5UaDmg91kO2EcNx42EzYN2wYmBRxiKCssoqmBV_boxsejsKPsGvgPTo0ekvU8NoeHjgU8JAFg_O77SltSjltLVk7P3SQMbL1ZBDMYF66msCTnY4Ftvbg__n8Lqrmd3E672AKPQgkL3_omtXLp-BqsBCBSRGcCRPwuWPauRoehtN32J560HN_i7uzh6UCZ7MfOCpfrtXq2WfBx-BY31x8b4gvcDoOfr3DcHn4tfPt7vsXNWxKK4NvGCjLr5EGo1Z3dduscA-v4Xsj-z42zC3u_88lw-RZVRWR_GUIEHNTs1n3LqlamtoHfsqkMUhw_7zdrPYgMGzh8JBkO2I4qMULr8TGCLN6MceatpIPn2ulg1BjO0IZ3JtrbfqijJXIr8ZPF69v7w0U5-GTzEWgHCAZeiMTu46Pcr5R-mcOz5skuG_fAX2SFQXneSG0gn_kcaIhG2BlPC7JFFYyhVRMoSY__ZrV4Hy4zS7cJHq7H0xyClnzi8Bn8lKVKi6ZFqJgOorjpIzBj5VZxKs4hCMex1EqwkzzJAPvxiLOdKy54FWYq6IUB-azDz2Twn970DNRzEQoITUk9AyhZwg985tEz4B1TOJEYXY4HI-JXT66P2ea3LF6CPtyMPDzQe3c1KtgHzWslA36LuEYOd819GnNQYfl3qz6euHqDyYyvW0WOHWMMa0OXPuez0sbhJqrJHaG2R5XajpuQ3I3SH5nTyaWLLG00z2Fr01gbpwHVm1XWH5E5EarIE2sTY0CBTb6YMugvfWxplqwcvs1CRUI40QYJ8I4EcaJME6EcSKME2GcCONEGCfCOBHGiTBOhHEijBNhnAjjRBgnwjgRxokwToRxIowTYZwI40QYJ8I4vY9X_T4K3JRkVZRDtPqLvdjTlDeM857_DSKzWkOQd-pNhQXnUmj54AW24Pf_eGlRB7IRG6PG4_iBH__0S27PHOiMVxqWSRkXWfY-RD2ykpM09Y82tPoKbJoKPp65ke-PvcKP55HgD9-Y-35FNm2IbqeV1sBh9GW5oy_55REv2M6Lnt67yCayGVswbHiGi3n4sVWu0iTjIv3Aq-wT3zHuN-GYiWZQhtmxdweGccy12nnb2XsXuUMDbENPlwu0im_qhYnT0XO-Pg_8OLFc-8GPz6RHPoKvBJMJf4yT65SdjD9Zl4cM0qmxxyFPWpbAGZTLQxZl_7OeK11bKMEwLASOvhBpsp4hCxpD7P7WZkeuAafnJgW6PGQZzsCPukr9LPgKrloMh3qoLq9hkhhK30KGGzyHVPFrpSALgAwZS2kmWjc24fLQUT8-fQhuHEJoDtGSidTHWBtFGNKU7WN7eeiYHn-czUE3LRYXxAZCc3k_yeeXEEmPU4f5uoN4eeiA7X_Y19Nix49gG29atr71xt0G58w8tXWnpHeXYNTn1OoAGPezFYYMNsXGCK2dr9QGNGgRHNRPvuVbQMX8pXAyzZW9mbpPX3zUO3PJxQH5fBToqwOQMvU25lXvBu5lWseq5GFZZVHCUi10mhdhzg-BewfE52lwL4VBFAZRGERh0K88DDqf7bALli_e7sfCfxDwv5Ks5LkIc6XTiMVZmSSZkrIodcykEHlehkmswwgOaCGrUJVpmiPivaykSuCTA_N5AP7PrqLqKq32gP9lmEVxVMUE_ifwP4H_CfxP4H8C_xP4_yT4P2RZnhRVxIVpVVpsw5gqHVidd8l9BiRYXhZlJVRl3pRt7fiYDm3Z8cdnMe6hkczySqeZtj0lq6pjYnN6dqfzkTF23q7ewKHarG03Z_YwQR-KUmBNhrvQhNrUeLv249svYxEIlAAbg7DxeA-Glu4-3wh3AF0Y3hgjB3IwoDEEMxl9adr6xliJLej5bFIR8GI_MZCHJy6segLBpFp16gmixuqb4b616eLD4MYcBvB_aKMcWOwArPc1OBwV-N7HZfClBaP6gsJLmNq1P2zXw_RfPh0Qa51vTAc2JDcP226UDWbaTNr4SWmwbwbk0t8eMXWiANcT5QhVGpE_Y5Z5Wn9OJ4d4AfoCW3L78uMX828_D6LLfAbe1NhpFFqDtmPJD6YEFvrrGmbuhPe9aVztRfBFuluPRCzKUKqb4_CxQ7ztVu0smpU50H2g2WKBGMinCPMyALQaFnuQpFUOQxJMGPo48sf__PzZnMMZkbDxHgeI3mljOqDGxVizZUtfk5rR0KwcS41uArh66g0GWbAiWzHXEwfz2WnEOhCv87aXEOoul6o1kiN44bZuJWTBbX-_18DYn9bszOGypbkhXht9AMwbLa0a0A-m6mQEHPu4tlTWgQIiBv1Y7FMoVfCqyNNcj151rA6cVrXTSf32QTcnxfqWJwt2jzNwIB9XJIQjs1YWEzqZkfFnQyyHbe4tKCpv2tUcHlD3DkIEKo_NZVSI4Kvnnxor0Rl4_fwoVBWCzL6eG5tiW-AmXMHQGCOqAdBq0EJ2niMOxX6Lej86w_Eq3FUIWh1C08fCTx9Wl7tB1Sx2ZvtoWdU2kbNBzUxDXrNILu4FVUSsmO3BD87tmCZIiH-yKBVSj3y8sehyWhNO10oclm57BcymPLH74SGvM4cw8f4KswLjZQM8qa01-k-cqR8gdrMB_G4RzeAlNi4CdbrnSEmwgbzDoNc83tv0SRUedv3VVil-ArELnjnrOeAsDGQRZobGZLRaDmwD13zB2leoyqPaGqPR3uFpbjY3tx5l6VsDbga2OYAZmFb-VRs2pdsF70_hsfXqzqq0CeM745tBQTCWE6MLOhpoF7Go0rwM0yFkmpSyTivC6QoUggatpdy0WD93BstZgGnm6FsGntZxGXxat7CCPgwaH-sAiJhsDTch-K_rpyuHWbB9GNNoYZFahjUInyCZRPZBSmRAUsOoFtdmgiGc1JYzccEKLL99ypAKu1O83W7zxtyjqNDaTJhMVmTMhTdsCPC2OjSBAQ3553d7eihWAh8TPmjROGCqV8hu-O0c0DregKO303DTOppFE5-X-LzE5yU-L_F5ic9LfF7i8xKfl_i8xOclPi_xeYnPS3xe4vMSn5f4vMTnJT4v8XmJz0t8XuLzEp_3t8TnZSGDAFbw9wBm_2fEb75uhtQZzXG34RBM9g4caFyJq34MTdL5TdtszqP0TYQ_xZfaHn4l5_A3BDeY2mImhg7QmMJtyhio0qK5MeXBCTDLAzZNeOS6ea4yj7U522Bzc9vPtXJFfmkwKKI_JB3bFsEOiTSrqdhMiE2LkbO18Gwx3xF1EmOjueHKJvTMhEPvwqeqmFa6SKoiLipVsqQQYRlGJsrYy6caQPSn-VS_HTU8n2N2_PcURobBB6FUSF0IiD91WGZMgqg8ESxLwpQnEIkWBf6QAivxNx5EmWY5pK5JkYmKMVnFiYry7NzfU8iusvwqKvZQKspYiDLPFFEqiFJBlAqiVBClgigVRKkgSgVRKohSQZQKolQQpYIoFb8NSgWkz7JMi7gow8FpTQoYThMeU3fYW5-yWoInxhhLDbry4J1G5sNhnezW4qbq-g0O7lp6tmdjyRvG4oOKtbXBvnsuh2UZOEaG8XLYyuXNm4nb2CFv2D5j03VWKVDQeuUQ7g6qVmMsjGbKaTiG-GBy4iy_SpiGRJLzLIQ8VYm8ikURCaGjKkuYymSokkoXucpYpYpUyCrSooxCLZIoZikrXzojtFMuO7Feqr657ccFc4XqAHwYA9cA9m9UNYtitZC4SYlw99Qeml_EVBpDqqTzIsorzKIiUJmokEwjxBqmm2HJhUVhXGkeR2ma8krlSVxqJTVnL9FG7qn6jVU901JtfVI5WYitMqCDK96v4MBgW3-qYW6ssSGxXU7czk2Jc0ScI-IcEeeIOEfEOSLOEXGOiHNEnCPiHBHniDhHxDkizhFxjohzRJwj4hwR54g4R8Q5Is4RcY6Ic0ScI-IcEefo18o52uENCSQMQRyhIA25ue1_ldSgW9bijl3DdyZ02McOslCZkR60O68PTBOCUMW0rlCgzZIrXPvvvrtA7xeVFR60778_QLo4h6IiMxVGaZzmIC1TsVA6rjKp85ESxGGl5pDiYMDiIVRgf9bYKwW9kmgXx6UORjbVQGsZiAwfkNbyiGU7i78zcDuGB-3QVUb2xgehq-Qs1wVLdcmTVGW8YKGIQmy46FhxEYccMp8wj6VMEghyWCSTMlE5XC2zhLE0OTylB4yV_CqLrtJkD2OlSAuJDSNirBBjhRgrxFghxgoxVoixQowVYqwQY4UYK8RYIcYKMVZ-G4wVpqNKyDwsshH4-ljGCr_vMRa2dWNzsP7bc1hsKUbIpBBVVbEyznUoRFyoAnL5VOc8YYJryNQ5q6KCJaIqk1BVcSQTJnmYE4eFOCzEYSEOC3FYiMNCHBbisBCHhTgsxGEhDgtxWIjDQhwW4rAQh4U4LMRhIQ4LcViIw0IcFuKwEIeFOCzEYSEOC3FYiMNCv5vzQX83Jwdvj6jiXWaHxYsf_DGSB4ckm1v92Xek_bMgrimi0HjXd3kWKvKIfPRdGdushZNtkb7StPr9j9gMan_e7-9MFmH_7-88wz-NmRwFcUksAkuUsGbywGT3j_nCHz5jYBACZGBuvrbvC2PWrw0wNQR9zW8mNbwDv8xjRzci-_FH0fehdZyD8Lnq0Ba9MQf3XX5eRzIlcwGTL4oQgRORYCoGdT_08zoDPeU0D-m_n7aezwvb_Vmb-O1-DtAH4T1VicoZD-MsDuOqFFmcRyH8EzI8UYpcKKULKWRaRSzKWVFmUkDsLTiXhQxzFWcH5rOP9JRcRfEe0lOUq0onin6mh0hPRHoi0hORnt4b6UmruAQfr3k86RmPjvpQWnXMB_tiWBKVqQ5jzsSYXY5u2Y38GI_bm_jGEYxgn-vlpNyxFSZdPaAhYNPHwPy2eAhffP6XwGCuWo_EWNerlT2vGCSYQuhLkeVJyDhTkazSUDGtwrwqsihmYRKDf03BdzKexi9nFichg_CyCg3ecm45JJ9GMxAiDKcWaPjMIzLxA3Ojx1RidQ4_KkMPvZwb6KX7wtw84obnW7hhHAwXylw0XUILcPOlXOyINK7TvwvxHZbWQyKxNmPh0EG3XuAWOdqLqw4vlMmVfWlaGoxJFO_7Qcux0IR4ERzx9wbvCed-IYMXX38dRLMoii_D4Iv6jx8ZNMEENeeC4Neo_r5WaKywKxR_9fzTuan5ugMLgpjfrzxHLlulWdRcOTShcg0RD2iYlGj8bvuq0mSh8KJJodtt6Wx7I2dDn3DYN9dqsNPZ4buAMVz3Fok_uCCkp1gK1ZTUYo6TK_NZuOJDRgoSXAwt5emEeDO8ogFu-cGitl15GMk-BnFhu0kIxPetcLeuwVBscM_bstJ7-Cm-WpEZS71Tqrgckpr9hrq_Zf02-WfMjAYwyq5JHkGmxtVaC0MUUaKIEkWUKKJEESWKKFFEiSJKFFGiiBJFlCiiRBEliihRRIkiShRRoogSRZQookQRJYooUUSJIkoUUaKIEkWUKKJEESWKKFFEiSJKFFGiiBJFlCiiRBEliihRRIkiShRRooj-l1FEwzjkZWXy-JEIdyTdPpuGN-TRjlFzhIwncpXIPKseLcM3Y0NwtP1D4wZWZQwuMPixWrm4vwogTj2PTDpZrmNkUnZIDMuAOsgrnazECV6pa6biBCy8yXoQfzYHHssIp9xPJfXtBgTDH1jxaTQ3tAYcxOfduKMxpOZa5SVEuJAexUmqC-yZHOKODiy_09xRUuPDanw-g_c4y3QkXX4QlqnOVC5BSbiWZREmoCdhVFUhL2LOOZhLJcuwyuKqkAzcehpXaVTFMfhzJnjODDnyLJZpcRUmV1m2h2WaqpgnaUY_rUcsU2KZEsuUWKbEMiWWKbFMiWVKLFNimRLLlFimxDIllimxTIllSixTYpkSy5RYpsQyJZYpsUyJZUosU2KZEsuUWKbEMiWWKbFMiWVKLFNimRLLlFimxDIllulvkWUKsaSUheTxBGM3QZye2uPD0FHvy3OIcXWWZqoakuYJmnQCUvm5sFDlW5dmtQxpxW6Z2RXvZPxfxlDZnYH9m092Zm6tvwmSQCHVqA3Wupgmg5j03Accsu0tWLtmhXZlFV8u0yqtch6mWaKKiIelTPMyiVPNoyjiLItToVWWpRDNJ0meRiIVUvKihP_FOmV59nJmJ7obxA4UMuNju9kW-KlebVDfVs18bEmNdaPXt7WBeSF4rRsKRL5QukflnB8bn-HLi2bBJmthmmtwdQfe1ZGW1k1XIwvXpeW2n4iB6bYxwmqjj03vVT8irSagbKJLE12a6NJElya6NNGliS5NdGmiSxNdmujSRJcmuvRj6dK8SpI4CtkWx_NIhf1snulQqYTt-sFSg-c-aTlGOlWRUHmuHy-Qxcz7O5wUTTvlmnXByzW2sa_FtR_Rko_O405P1u4s7rRvme9ZkYME6slynEGgrle2PLZbVN2K6tATjA74HfjUXv4Hqzo6SzG0vYYcHvvriAl9R2p1lkYlhzSKsTwvizAtE55FJqnfS60eqK2nqdWk8meq_Pls9-M865F2_EF41mkqMhaxTCY6jJA4Hcmc5TpMqqhiOudxwSVII3jFYsFEWmhesCzUstBFLvPqfJ51FF5lyR6etUgEROWJJp418ayJZ008a-JZE8-aeNbEsyaeNfGsiWdNPGviWRPPmnjWxLMmnjXxrIlnTTxr4lkTz5p41sSzJp418ayJZ008a-JZE8-aeNbEsyaeNfGsiWdNPGviWR_jWWcQTUEWCX47GRohE4zfqR0-E6w3sL1kyMMsAys8mOUJfm8CC_i5QDx4_uX6_uWUQ-NzgJEXubFp3ZDsPWwOjtOyJINJC8wmIoNVGGicV8ZFbim3py5ODNHEeu5QHZ_a8vDUIIA83XZLZGJKZq5ztnVPYu-ZchRMb9Q0P4ZK8kTvIApxVN0RjFr3iJp28sNKD6no9ZCK_qNmi069NCK8NBDqa-baDteuMSH_ETJjbFnUva93OF-OFkohaXPS2EET1kyx_xBw09sB6O0A9HYAejsAvR2A3g5AbwegtwPQ2wHo7QD0dgB6OwC9HYDeDkBvB6C3A9DbAY6_HeD7t_8J-cVrRA)
