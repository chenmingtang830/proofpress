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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFkYzQxNzlhYmViZmY2ZDM1M2M0YTVmZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjE2ZTlmM2VlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kYWVkNmM3MTA3NzA0NGI5MWNhZTI5YWIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2EzMTU4NmMyNjBmMGU1NmE4NTQ5M2ZiZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVmPG0eS_iuFnhfbS3bXfbQeFhrJ3jF8QvZ4B_AIrTybZZFVnDpaahsC5m33eXcxP2F_2DwssP9iI_KoKrLJYssteW1MAoahJouZkZFxR3zkT2ek6UpJWHdV8rPLs-32KuAsDrKCUEGlTHmURCwmiZRnizNa89srXl6LtoNn2xUJk_SSxQUPfRnxjGUxzSURCaGZSEPh85QlLImLuChIkso84XGU0yDL4iT0kyRPZJT7sC4vW1bfiOb27PIn_KO76sg17LAmHW61gH9QsYYXvhNNKUtC18JrxE3ZlnXlreD5urn16K33dVPXctuItoXPbAl7Sa4FHmrn5ab-QcBx-wYXXHXdtr28uLguu1VPz1m9uWArUW3K6roj1XUe-Rc7n27EX_oS_n3Vt6K5YnXVigp40TW9eLM4WwmCTAxSUchIiDP9ypW4UQ8Bc8UVJwK4kgV-lvlxTIuAERECs5GyuunwaFfrshJAub2R9RWJgiRPWZj60hdJSnLgaSSp0Mcx1F0xsm37NRw4RDpZ3fD27PL7n87M9j-dwS3XTYv_0m8LfkWB5d-f9dXLqn5VnT2HM1h5wAvuel6K9oJsxeslEFR1S3FD1hcf_-nxk2-vPvvyq3_9_OOn__Lx1bfPHn_5zScfP7v67vHnnz59_O2nX3159V2YnG_42eKt5It0XVPSvoNrvaKkLVskQqzlFWmB3Z1Q6_Xdqm7wEC_LCpdsb9tObOCdimzwtu1hFvDRFiXk7LLq12s4GlvBlQrNFLqu2Ut4OgmSIuQZ8h9usxOv8eAf_M_f_u1___tvH8KLZhPCudp9i2InXsEr319cPL_0fud9UNPLmzBZdmW3FviJ7narhI405OzNYtyJR4WQksidnT5-DazxPgOC14JfC-8JSBQIE0MWeLCs9_e__pf3bUOqdo6W33n3X0eKxvuOrEtO1HugMiPNKK0g-TtkZ4zEuUzFeyB7n4VtR7q-neNhloZxlstsh5hv1Mdm-fM7b3ho5qgsiHyZJOlbrr5_DNkI8aP48M_VtyvhKY1eMrFee6TiHhedaMC6gM0q2ZKLZuaweSgSPxL-A8n5Sw82FO5ljq9FQRmRclcLvm7KDQHDahc4weEDj8_wWsoi8qkgP3vHY8dcopMC5j-tRet1cAMtmAXvGt1LJbgnUHKXc6wA-YrThL4zwlZizeu-m2N_GqQEbHu0s-cf4HNL-KD3-OuP_-RtSQUecP4GDn9i5hI4K3zJguwh-x45rr0G1IGt4d5aXJO1XtEr1eXM8MTPfUEJp--DtjWo39x95DQLozxmD9l76b3oSPvyKoSwJ04jdNgB2K6ECk5CIUMeBWnkF-TFnyv7aJ6lhIko5BO-IKl7bkQGRSzey501ED60cGmfKAvmIVHep0_bhfrXRVv3DRPeDN8k81Ofpvxd0gb2k5wyX6A9kQ-x2s6-367gFEv4m5fKLdmFTijRzMdmNClOCZFZ8XAKjh3_pMymPBd5mPEHUxCcex999FUDR0SdZWtSbi4_-mi0oOqVVnmzRujlQEJeQQDtdTNyG_hFwUKWvj8O4bJNvUYBfgzutsO1vWHtFqhlcwYnygjLkpC9cwKrulKWb-72SAgOMUl2PcCXeO3KZnY2cruPG5j52IwEgzNmCZHFgyk4dnzrEZ40AtI6Tzb1j6JaeNqqLClkayBcc7EfCYuweA8E6oyi7G6Bwr7iIPXGb0HGA_kmU_4Lrv9GgNeaITAMhJ9QP37nBG4EpEVsPjCOfSJIku_s_YX-nFJVUpH1bVueCpOPfGRGbiDvh0S-iB6085ETnzR6hShY7uf0QZsvPdLVG7hnk9xvINH12p4xSB_VIi2u12l3aF5_hF4bY8kZixfmcUSCKH2nnLGfARF9JrBi4AksnGjicFEGkgxSW4NqdTOco3GYZfKBArNPHBdM1WTmriyB8Idke_H1Y35DKogtNLfrrWdXOiGuc5-b89Ys87nMycNpuHM9ehF0QWY5TEE2AksPZbvxwBbeeqVUr67mrge8OeMkePcUDjZuZnfhxynkQLuS-wT9vmc_fuJi7jw8cxuBEHEQZvHP3O3YAccMBHKNbVN3NavBCkMC1462eJ8Jzxe2XHYGaoW8vWLKX-Ge6h1bxxJXscxITIkouPRjkvucyURwgeeo6k6taSp6nqnoeWwl2MttXVadKlA2aiesTtm_sDj1HEuB65LdTlaYlgcni6jC48-sHLa17K4kXIZowMGZAmVLg0tKYilFnMksozzzIxIyEtKAByyglPiJL2MZF74fREmSkzDCKrAPOU2UFImfKpOIlRxVaNTXdRnFb4DRWM4L_TBd-vkyCr71o8swuIzzf_L9Sx8jZ8NxFEAKaRMHMt9MXv3p_7U2qaRV1w5XpF3hUUK_iGgKeWKMZlStMSknGkG-d53QrEoCQrMs4nHEMrvqpHRoVn1YxU-pwmGlNFTkGYtpnpIoCaWlYlIJPHK24wU8s6xI_SAUIDQFK4Zlx5qePdx8uc6yn9JAgv6lAY3sWpMK3hES36o4V95olo32G0yJDlwhZlBG_CaMvXKzXauoQT197uHSEsPFH0VTQ3JNbtA_v1Y-uvX6FuLcrobdbsQajHjZeaD69k9cZqm8hHLC8IZ4zdY9aBFuvFF72nqKik_hYn_UVGJpagOm6hwyAE_2DTzaoOHbbLsFxDbg2lFDIOIGA7IhC69uPFk3m35Nlp2AI2BU3vUVsNnbkFukE3crG6BAsL6Dx-G_64YAYzzI51m9Ee358buOExYlWZyKoojt_UxKmkfuZ65aaRZmKVgeAiuHvrALTwqYoxDdryJpVo14kglG_TAoUrvqpEh5gtx7VR1fDso6EagN3NCNqbUAS0GS1GXCf33V1T3cFTeFMy0-KBbwZjXkFXrtssK71IKgHlT3y0uO8qXkSZZaYpVkTqRtFM1_nrFKGS9yCczJeDLwfKyUHuHOTOnTGoQ4CFIZBr4gg0GYVEPHu7x3bdMsLNMwITkTNA8GgiflznmC71e89FoMCDRB-m7A7Wv1LsEEB_nf__qfaB4mvL48zgmexDE4S-BoNHBiUgM9QfCxRMksnlFRgAsHJ14M5nxS5DSLP6hkyWgsQ3AYEBRlLKIy8Sk4ssmj4ClJkfmySAT4ET8ogiyVoF2BzCIBRnz6aEGTXMR5JJHApCh8CDeQgJwVUgTTVZmISVTkvGAyjUUaEZLEjOY5TdMgYUU0eVTwFIKKPIIcPYjBURRxHPKQReBsAwZpyc6x_ISHeRL5pIhZmOe-pJJnQeGLMMl4_OJA2mfNXsZEInkhaCZH_z3UbE_c470qsLoDDy9WRFUl4INb0AwkCF7c1BxEtIEXBZj9nkJGt7BmW4mvdga3ng4yFx5239d124OvoT1YJ_AWaGQGq69f9KgAC6P67gJ8DjiJsSrWiLZfd-2596wHxwjeVGuGUopHHq-VYrRiLUwW3WKzHhQLFm8ZLHruPfYkKcE22iPZyAyW3pCyArNnHxgS3VLrWwuvVh3YNyDnRjWJ0bliZ75eW9bMeKnUz4qUB0mSjYHOpIx95LrmitJ24QykpkiZn6WDl5rUqUfL9nYFZ2stpJ9KToRIKbGrT2rQJ8g-ZS5iIQXzIVJP5BBaTerLZvWHFIqth5Tla3hyqMB5axBQj9zAVau8CW5SlzcG9jyCS5_GbayuFQWQ16mdKgyshsCtAl1oz_9chUiqTin_SX_aw0-3SC_SUnKQoZKBgX9VNy9RuFuQ-O26b7V79dQAysLbYmWFLzyIo3rUrvrVAihY95tK64wpZragZx6FhBVWQgXYI0jxADUeKIuOUAZ_jR9DMkcBCTVhJnYztHegyJrUskJjYHcHutq2hxBQcx_yPAhxBS8x2DNqu7gb_IIO32K9HOKRHjVKq9E02ts3e1xKHoRJIHMxhE-Tkv8pgbxP7R7twiA4aAaG4jHRtTpr0Kw4KVOyNEbTvmnN2sKaTbU1ME6zYUNel5t-45mjG-OnY_oOKwEqZDIBAOGbskP-GKlZotQ0AsdxbDawUEYKTt8QWJOwFQpX3ZhXDG2afr0JI31L1oYqrFVgDrAj8NUwJON9EHp___f_8IIPF1Mh230kUo-EH-rzwblANFA7DzwUfDhjKXMfAqoQvHhacHvDk57JkRuea34M1iaPaZEHMYSYduFJP2S0lG_X2LBpIoQFQUAgkmGDLZv0Ok6Qfa-mhXZpEPNpsZVkU65L0V6CdatIxUpYpjMza8B1Bm_qe8L7uCFNaYp6ut76yKvByqgH4KCfff2pEUWirZ--Qy2xcPpbXazGLAEjh3PvYxAxTcGtt-lbNAcqfURbtQSlgMfR4KpV0G6NrykS0RiAtRMgeZA1QKJStq2RWNhVggp1-KeyMQubr4iltosgu2vWD5ZeV5GNVdoxL-Aj1tyYHw8NIeqizm_ZtIwxhiGYVx-XID_MKfMLngSjr520i44Zn7fp-3iDsmISrFwcKjwmb3oM0Rjcc-9zJaGjS9MmH0IuoiQEE-pW4AlAniqds8EOqxIuvWErsFA_9E3Z8pJp86F4IMEfK2PG8VPalGHQNEgC-FrM1zFv18QBvVY6JreiPA_ymgq8RiwO1CZiUrUbNUhZY9UA7K3yK9OjPEImwFuEtysBls4wBDeFeBTEp2xXKlADgsaNQEhwr8FWDlnwzIWSiEmapDLm6eBNJu21Ixc60ycz6xYJKWQMK6fxEDZNWmejqbl_H8zmm3mSFJTGPBgzrElrbJ7iU_EYCHIofR4lcT6QPWl9DenbA_pY3aDDRqcr-6ldzbVBgRanLQQXHkryuM5E8o9oCkg8W5lAkGy3IMuEgk2EDzDYr-SE3Q4aYqpef-g3YEkeb3ERslab9VXbb7Hwjc_Avj2Wtqp-I1S-w0rrftUNDiTpQVK0T2qR_WzjBsuk6jkVtKrqjlB1Bx0pAGuUtVYfNs0KUJ6XAu1dV9drVLb1kISZP7CyVqnApNLijy667WaiKR_CJhoWQZzng0GbtBOPGbS36Q2uBF4fiAnHqHZp6k82xuQlmJwGqDbRqg4cgT3gYj4TYmvKITritl4Z5It0ZLRuJmMkFeaaNSZvEIliMeXce6pzwrJCJ07QEHGw-d412si7fkANh2P_hKzBKZl4Va-gYjIrOOCJlCn3aooz3iC_LUoYFtg4SqO1QXNVyzwI_UQESSCGcGHSKz3C-bnG51DXz3KS8yLLkiF8mvRCR9Pzlj1NW-FhQZJyWUC2OQRRkzbnMYl5m3bl3QqcrV7aLGlqeIDdU0MzOASC-g9CCPKijQNuu5iq81IljmMYfztVZ7xFo63LQVsbcd3oWW8tG0gupJwCjtRN5NMGZl67ql-ZSrpAR2ujn2krYDeaxkj83PtU2hOrI4JoCdK0mkt1daK6ukAnDUTK2z0mg5AiI7A-O9y5Jk4pBRB_g7YEmaJImGaJcClbyFG6CcGtUY3FEHNMntd2bVMrIsdPTFoL9bbGCqZJQ8TrLaTk5ET8RTgNfBoEvs_DQWnGDvYR4ZvrRNuifJiJSIYxKOQg1ZPm9Kg09-k325Jz7mcygowjjYe-xKQFfYLYe3WVawliPtRBdhPC8eLhMuHesGGgUsQhgtLCyuoGfG2HbnhQhR_h1sB7tGj0NijhpVYeUArYZE1Af3c9pU4pp60lbeeHDjJGthYMghnMC1MTuNjrWGBrD_5PlzdBsbwJ42ULR-iAIH7-Q1tXLx6Bq8FCBCZFoBMq4DNq2poaHobTN9ieutNzf4O3cwClArrZDRiVr7aievyp9wQc6-uz5wr4Atpx9O09hMvdt41vN-8_K-FSGu59S0BYfo0wGFHdlE1d4R1ewfuK9kNomBXe_88Fw6RJUWQBfzcAiKWq2Ww7k1RtVO0DXyVcGST4_LLpqwMTGLpweIyyPTLMqMUzK8TKCJNyvcSatuB399XUQaixG6EM7s20Nm1RRlNkufHT2avVrRrFubuTegiEAyhDb6Ri13Er4xu53XPYb5LgvnmL6ZMkyyhNMyYF_CMNIwnZAMnDkSXTsZLpSMV01OSnX7MY3H_cZn_cJHhzeJjk1GTNOxmfSXORizAnkrGMyCAMozwEP5YnAS1CH1Q8DIOY-YmkUQLejQSUyFBSRgs_FVnOjpzn0PRMDP8dmJ4JQsJ8Dqmhm55x0zNueuY3OT0D1jEKI4HZ4aAeE7s8ez_3NLlj9RDu5WjgZ4PapapXwT1K4JQO-s5BjYzvGvq0StGB3X3VlWtTf1CR6ape49ExxtQycGV7Pi90EKqe4tgZJgdcqeq4DcndQPmN1kwsWWJpp30Eb6vAXDkPrNpWWH7EyY1GQJpYqhoFEqzkQZdBO-1jVbWgMvc1CRXcjJObcXIzTm7Gyc04uRknN-PkZpzcjJObcXIzTm7Gyc04uRknN-PkZpzcjJObcXIzTm7Gyc04uRknN-PkZpzcjJObcXIzTu_jq34fNNwUJUWQQrT6zr7YU5U3lPNe_gUis1JCkHfqmwozSjmT_M4X2ILf__25njrgNeuVGI_re3b9019ye8-F7vGVhnmUh1mSvA9SZzg5SVN_r0Orr8GmCe_Jwqx8O_cVfjQNGL37jbnvl2TVhmj3Wmk1KKMty81-yS8NaEb2vujpvZOsIpuxBUOGPUzMQ-e4XMRRQln8C3PZJr5j3K_CMRXNIA2Lue8O9MOQSrH3bWfvneQWDbAOPU0u0Ajal2sVp6PnfHW_4ceJ5To8_PiY28lH8JVgMuGP8XCt0IexmnV-zCCdWntc8qRl8YxBOT9mUQ7v9VTIUo8SDMtC4GgLkSrrGbKgMcTuVjo7Mg04uVQp0Pkxy3CP-VFTqV94X8NT60Gph-ryFg6JofQKMlzvKaSK3wgBWQBkyFhKU9G6sgnnx1R9_vgQ3JgJoSVESypSH2NtJGFIU3bV9vyYms5vp3PQvsHiAushNOe3k3x-A5H0eHQ4r1HE82MKdnizb6bFjh_BNl43ZLuyxl0H50Tt2hgt6cwjGPUZsToyjPtphSGDTrExQmuWlehBgtbeUfmkO74FRMw-CpqpnuzU0W36YqPehUkujtBno0BbHYCUqdMxr3i74V4iZShy6udFEkQklkzGaean9Nhw7zDxeXq414VBLgxyYZALg37lYdD90Q77w_LZm8Oz8L_I8L_gJKcp81Mh44CESR5FieA8y2VIOGNpmvtRKP0AFDTjhS_yOE5x4j0vuIjglSPnuTP8n1wGxWVcHBj-534ShEERuuF_N_zvhv_d8L8b_nfD_274_-Twv0-SNMqKgDLVqtSzDWOqdIQ7b5P7DJNgaZ7lBROF-qZsbcfHdGjHjj88izGbBjxJCxknUveUtKiOic3p053OR8bYebd6A0rVb3U3Z3E3QR-KUmBNhk-hCdWp8W7tx7ZfxiIQCAE2BuHi8TMYWprP2Ua4GdCF5ZUxMkMOamgMh5mUvNRNea2sxM7o-WJSEbBkX6iRhwsTVl1AMCmqVlzg1Fh5PXxuq7r4sLgyhx78D22UGRY7Mtb7ChyO8Gzv49z7Sg-j2oLCCzjalVW2q-H4Lx4NE2utbUx7OiRXm-02ygYzrQ6t_CRXs29qyKVbzZg6loHrCVIcVRonf8Ys87T8nE4O8QH0Bbrk9tWTZ8vvPveC83QB3lTZaSRagrRjyQ-OBBb6mxJOboi3vWnk9tr7It6vR-IsylCqW-LyoZl426_a6WlWYobuPUnWa5yBfIRjXmoArQRmD5Q0wsyQeBOEPq785I9PHy8p6AiHi7dzgOidetUBVS5Gmy1d-prUjIZm5VhqNAdA7onXGGQBR3Zirgsz5rPXiDVDvMbbnkOou9mIRlGOwwursuGQBTfd7UEDo39as1XKpUtzQ7w2-gA4N1paMUw_qKqTInDs4-pSWQsCiDPoc7FPJkRGiyyNUzl61bE6cFrUTif1u4quNEX7los1ucUTmCEfUyQEldkKPRM6OZHyZ0Msh23unVFUWjfVEjYoOzNCBCKPzWUUCO_rp58oK9Gq8frl7KgqBJlduVQ2RbfAVbiCoTFGVMNAq5oW0ucc51D0uyj3ozMcn8JbhaDVTGjaWPjR3epyO4ianp3ZVS0t2ipyVlMz05BXMcnEvSCKOCume_CDc5uTBA7xTxLEjMsRjzcWXU5LwulaiZml2-WAupQLfR925HVhJkysv8KsQHlZDzW10Ub_wpj6YcRuMQy_64lm8BK9iUCN7BlQElwgbTHoVdtbmz6pwsOtv9wpxU9G7LzHxnoOcxZqZBFOhsZktFpm2Aae-YI0L1GUR7FVRqO5QW2u--uVnbK0rQFzAt0cwAxMCvtVGzql2x_en47HltWNFmkVxrfKN4OAYCzHRhc0G2hnISviNPfjIWSalLJOC8LpChQODWpL2TdYPzcGy1iAaeZoWwYW1nHufVI2wEEbBo3bmgFETLaGD-HwX9tNOYdZsN6MSLSwCC3DGoRNkFQieyclUkNSw6p6rk0FQ3ioHWdighVgv95lSIWNFu-226wxt1NUaG0mSCZNMubCPRkCvJ0OjaeGhuz-7YEeiqbAxoR3WjRmMNUKZDv8dg5IHa3B0etjmGPNZtEOz-vwvA7P6_C8Ds_r8LwOz-vwvA7P6_C8Ds_r8LwOz-vwvA7P6_C8Ds_r8LwOz-vwvA7P6_C8Ds_r8LwOz_tbwvMSn0AAy-h7GGb_I85vvqqH1BnNcdtTCCY7MxyoXImpfgxN0uV1U_f3g_RNiD-Fl9pdvuJL-BuCG0xtMRNDB6hM4S5kDERpXV-r8uBkMMsObKrwyHTzTGUea3O6wWbOdhhrZYr8XM2gsO4YdWSXBL0kwqymZBPG-gYjZ23hyXq5R-okxkZzQ4VO6IkKh94GT1UQKWQWFVmYFSInUcb83A9UlHEQTzUM0Z_GU_12xPD-GLP531MYEQa_CKSCy4xB_Cn9PCEcSKURI0nkxzSCSDTL8IcUSI6_8cDyOEkhdY2yhBWE8CKMRJAm9_09heQySS-D7ACkIg8Zy9NEOEiFg1Q4SIWDVDhIhYNUOEiFg1Q4SIWDVDhIhYNUOEiFg1T8NiAVkD7zPM7CLPcHpzUpYBhJeEjd4WB9SksJaowylhJk5c53GqkXBz7pq8VLleVrXNy09HTPRoM3lMUHEWtKNftusRwaZWAQGcrLYSuX1q8nbmMPvKH7jHXbaqFAQsvKTLibUbUSY2E0U0bCMcQHkxMm6WVEJCSSlCY-5KmCpUXIsoAxGRRJRETCfREVMktFQgqRxYwXgWR54EsWBSGJSf7CGKG9ctkJfonyetWNDDOFag98GAHXAPZvFDU9xapH4iYlwn2tPXa-gIg4hFRJplmQFphFBSAyQcaJxBFrOG6CJRcS-GEhaRjEcUwLkUZhLgWXlLxAG3mg6jdW9VRLtbFJ5YQRO2VAM654W4HCYFt_KmFmrbEhsVtO3M1NHebIYY4c5shhjhzmyGGOHObIYY4c5shhjhzmyGGOHObIYY4c5shhjhzmyGGOHObIYY4c5shhjhzmyGGOHObIYY4c5shhjn6tmKM93BBDwBDEEQLSkOtV96uEBq1Igzd2Be-p0OEQOkiPyozwoP1z_cIwIQhVVOsKCeo3VCDvv__-DL1fkBeoaM-fHwFd3AeiwhPhB3EYp0AtESETMiwSLtMREkSBU0tIcTBgsSNUYH-22CsFueJoF0dWeyOaaoC1DECGXxDW8gC23Qu_M2A7ho324CojeuMXgaukJJUZiWVOo1gkNCM-C3xsuMhQUBb6FDIfPw05jyIIckjAozwSKTzNk4iQODp-pDuIlfQyCS7j6ABiJYszjg0jh1hxiBWHWHGIFYdYcYgVh1hxiBWHWHGIFYdYcYgVh1hxiJXfBmKFyKBgPPWzZBx8fShihd52GAvrurFSrH94DIsuxTAeZawoCpKHqfQZCzORQS4fy5RGhFEJmTolRZCRiBV55IsiDHhEOPVTh2FxGBaHYXEYFodhcRgWh2FxGBaHYXEYFodhcRgWh2FxGBaHYXEYFodhcRgWh2FxGBaHYXEYFodhcRgWh2FxGBaHYXEYFodhcRgW97s5v-jv5qTg7XGqeB_ZoefFj_4YyR0lSZZafg6ptN0L4pos8JV3fZu9UJDHyUfbldHNWtBsPenLVavf_ojNIPb3-_2dCRMO__7OY_xTmcmREJPE4mCJYNpMHjns4TWfWeVTBgZHgNSYm63t28KY9mvDmBoOfS2vJzW8I7_Mo1dXJNv1R9IPTesYB2Fz1aEteq0U921-XocTwVMGh88yHwcnAkZECOJ-7Od1BnjKaRzSP5603h8Xtv-zNuGbwxigXwT3VEQiJdQPk9APi5wlYRr48E_I8FjOUiaEzDjjcRGQICVZnnAGsTejlGfcT0WYHDnPIdBTdBmEB0BPQSoKGQn3Mz0O9ORATw705EBP7w30JEWYg4-XNJz0jEdHfSytmvPBthgWBXks_ZASNmaXo1s2Kz_E43YqvjEAI7jncjMpd-yESZd3YAjY9FFjfjs4hC8-_5OnZq4aO4mxLatK6ysGCaoQ-oIlaeQTSkTAi9gXRAo_LbIkCIkfheBfY_CdhMbhi4Wek-Cef174at5yqTEknwQLIML3pxZoeM1OZOIL6oN2phKrc_hS7tvRy6UavTRvqA-Pc8PLnblhXAwZpR6aslAPuNlSLnZEatPp3x_xHVhrRyKxNqPHob12u8YrMrAXUx1eC5Ur29I0VzMmQXjoBy3HQhPOi-CKH6h5T9D7NfeeffONFyyCIDz3vS_K33-opgkmU3MmCH6F4m9rhcoKm0Lx108_Waqar1FYIET9fuV96NJVmnVJhZkmFKYhYgcaJiUae9u2qjRhFD40KXSbK13sXuRi6BMO92ZaDfo4e3gXMIbbTk_iDy4I4SkaQjUFtSh1MmU-Pa54F5GCABcFS3k0Ad4MX9EAH_lBT22b8jCCfdTEhe4m4SC-bYUbvnpDscHst2OlD-BTbLUiUZZ6r1RxPiQ1hw11tyLdLvhnzIyGYZR9kzwOmSpXqy2Mg4g6iKiDiDqIqIOIOoiog4g6iKiDiDqIqIOIOoiog4g6iKiDiDqIqIOIOoiog4g6iKiDiDqIqIOIOoiog4g6iKiDiDqIqIOIOoiog4g6iKiDiDqIqIOIOoiog4g6iKiDiDqI6D80RPT5m_8DmizFTg)
