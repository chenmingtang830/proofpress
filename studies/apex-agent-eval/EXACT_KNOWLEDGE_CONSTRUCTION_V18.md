[//]: # (ob:ffb9914f)
[//]: # (ob:v18-title)

[//]: # (ob:1b9c9fe5)
# Exact Knowledge Construction v18

[//]: # (ob:c7bae7d0)
[//]: # (ob:v18-status)

[//]: # (ob:0f9993df)
**Status:** Stage A completed on the five frozen zero-heavy tasks with no answer executor. The latest Stage B closure slice deterministically projects official-authority candidates, screens authority responsiveness separately, requires source-bound period domains, supports explicit cross-slot calculation dependencies, and selects numeric atoms from deterministic receipt-local inventories. Exact repeated runs on the fixed 49-slot plan covered 27 and 25 slots, agreed on 41/49 slot states, left 19 stable gaps and eight unstable slots, and produced zero executor-ready tasks or Human Approval receipts. The paid executor remains blocked. All constructed objects remain candidates until Human Approval.

[//]: # (ob:8771d08b)
[//]: # (ob:v18-decision)

[//]: # (ob:60e62598)
## Product decision inherited from PR55

[//]: # (ob:f9d861b8)
Keep the existing Claim Graph as the canonical governed substrate and keep small-seed disclosure as the current default executor interface. The v16 and v17 results did not justify replacing the graph or increasing retrieval breadth. They identified a construction mismatch: exact tasks ask for atomic numbers, periods, authorities, calculations, and output forms that an abstract claim may not contain.

[//]: # (ob:392c714e)
This phase therefore enriches the existing graph with typed exact-knowledge objects. It does not create a second graph, grant retrieved text admission, or turn calculation into authority. Human Approval remains the only path that authorizes downstream reliance.

[//]: # (ob:2f4ff133)
[//]: # (ob:v18-question)

[//]: # (ob:62625f07)
## Primary research question

[//]: # (ob:4e9d88ca)
Can requirement-aware exact-knowledge construction raise native APEX task success on the frozen zero-heavy tasks without weakening evidence lineage, authority boundaries, or admission semantics?

[//]: # (ob:26990aaa)
The mechanism hypothesis is narrower than “more context improves quality.” Before an executor runs, every atomic task requirement should have a declared completion path: exact evidence atom, controlling-authority candidate, deterministic derivation, or an explicit gap. Retrieval should fill a requirement slot instead of accumulating loosely relevant excerpts.

[//]: # (ob:73a7aea2)
[//]: # (ob:v18-invariants)

[//]: # (ob:547cae7b)
## Construction invariants

[//]: # (ob:65983f1d)
1. The requirement plan is compiled only from the task prompt and native output type. Rubrics, gold answers, and silver locators are forbidden inputs.
2. Every number-like source span is inventoried before semantic selection, including years and section numbers.
3. A material number in a proposed claim must bind to a custody-valid numeric atom, a recomputable derivation, or an exact authority citation span.
4. Numeric atoms preserve display text and normalize a decimal value while recording kind, unit or currency, entity, period, and precision.
5. Every derivation variable binds one digest-valid numeric atom with the same value. The expression, rounding rule, input units, output unit, entity, period, intermediate basis, result, and digest must recompute.
6. Authority candidates bind an exact source span, citation, proposition, jurisdiction, effective date, and authority level. They cannot self-confirm normativity.
7. Candidate coverage and governed coverage are separate metrics. Candidate construction cannot make an executor ready for governed reliance.
8. No candidate object or gate may admit itself. Human Approval remains the sole admission authority.

[//]: # (ob:cb719214)
[//]: # (ob:v18-pipeline)

[//]: # (ob:e2f12de5)
## Proposed pipeline

[//]: # (ob:0bb4210b)
```text
native task prompt
  -> atomic requirement plan
  -> requirement-routed source discovery
  -> exact numeric atoms / authority candidates / derivations
  -> candidate readiness matrix
  -> human governance of eligible objects
  -> small-seed task working set
  -> native executor and blind grading
```

[//]: # (ob:655e465a)
The implementation in this PR stops at candidate readiness and claimability. It deliberately does not manufacture a Human Approval receipt or run a paid executor.

[//]: # (ob:46e3560b)
[//]: # (ob:v18-artifacts)

[//]: # (ob:7b96cbb3)
## First implementation slice

[//]: # (ob:4b8b5a43)
- `retrieval_adapter/exact_knowledge_contract.py` defines fail-closed schemas and validators for requirement plans, numeric atoms, source-bound period domains, authority nodes and applicability screens, cross-slot derivations, readiness, and proposed-claim number binding.
- `retrieval_adapter/run_exact_knowledge_readiness_private.py` accepts a private task bundle and emits a sanitized report containing digests, object counts, slot states, and gap IDs without reproducing prompts, source excerpts, numeric values, or authority text.
- `retrieval_adapter/run_exact_knowledge_stage_a_private.py` runs the frozen five-task construction audit through the fixed GPT-5.6 Sol compiler, extractor, and derivation roles without an answer executor.
- `retrieval_adapter/reaggregate_exact_knowledge_stage_a_private.py` recomputes readiness from saved private artifacts after deterministic contract corrections without making new model calls.
- `retrieval_adapter/build_official_authority_catalog_private.py` creates a private, digest-bound authority catalog from allowlisted House U.S. Code, GovInfo CFR, and IRS sources. Official custody can support a candidate but cannot establish controlling applicability or admission.
- `retrieval_adapter/build_exact_knowledge_review_queue_private.py` compares repeated frozen readiness runs and emits a private evidence-bearing review queue plus a sanitized stability manifest. It cannot create approval or admission.
- The local Gateway and telemetry aggregator retain input, uncached/cache-read/cache-write, text/reasoning output tokens, latency, terminal cost, and per-field completeness for later runs.
- `tests/test_exact_knowledge_contract.py` exercises exact receipt binding, decimal normalization, derivation recomputation, tamper rejection, authority boundaries, task-prompt-only planning, candidate/governed separation, numeric claim gating, and sanitized reporting.

[//]: # (ob:b3efe6f1)
[//]: # (ob:v18-qualification)

[//]: # (ob:9bf810f4)
## Qualification sequence

[//]: # (ob:b7822859)
### Stage A — substrate audit

[//]: # (ob:18b61671)
Run the candidate-readiness builder on the five frozen v17 zero-heavy tasks without an executor. Report per task and per slot:

[//]: # (ob:89d03e58)
- requirement count and type;
- candidate-covered, governed-covered, gap, and invalid-binding counts;
- the path used for each covered slot;
- numeric, authority, and derivation object counts;
- construction failures by invariant;
- construction calls, tokens, latency, and known cost.

[//]: # (ob:ec0994fa)
Stage A passes only if every task has exactly one output-structure slot, no invalid binding, no private content in the sanitized report, and every material proposed number passes the numeric binding gate. Gaps are allowed and must remain explicit.

[//]: # (ob:784763c5)
Stage A passed that structural definition across 49 slots: 24 were candidate-covered, including five mechanically covered output-structure slots; 25 were explicit gaps; and there were no invalid bindings or sanitized-report leaks. On the 44 substantive slots, candidate coverage was 19/44 (43.18%). The construction produced 49 general evidence atoms, 16 numeric atoms, 10 task parameters, 10 derivations, zero validated authority nodes, and 39 recorded invariant failures. The formal run used 15 model calls and cost $0.5762715 with complete terminal cost receipts. No answer executor ran, no claim was proposed, and no object was admitted.

[//]: # (ob:30dcb8e5)
Structural passage does not authorize the Stage B executor comparison. The current stop decision is to close three substrate blockers first: provide a controlled authoritative-source corpus and exact authority bindings; construct complete, recomputable inputs for exact tax and annual calculations; and require every declared period in a series before treating the slot as covered. The detailed evidence and task-level breakdown are recorded in `EXACT_KNOWLEDGE_STAGE_A_RESULTS.md`.

[//]: # (ob:a4fae153)
The first Stage B entry-gate attempt confirmed that these are mechanism blockers rather than a reason to run the executor. A non-frozen diagnostic recompiled 50 slots instead of 49. Reusing the frozen Stage A plans and a separate official-authority extractor then produced 35 candidate-covered slots and 14 gaps in one run, but only 26 and 23 in an immediate repeat. Neither run produced an executor-ready task. The authority lane proved official source custody and metadata binding, not that a cited provision controlled the slot; at least one structurally covered slot selected a related IRS procedure instead of the requested Treasury Regulation. The next gate must resolve source-bounded period domains, deterministically construct calculation inputs and derivations, validate authority applicability, and pass a repeatability check before Human Approval or an answer executor is considered.

[//]: # (ob:cad50356)
The next closure iteration removed model rewriting from the official-authority constructor: frozen retrieval plus controlled metadata now deterministically produces the authority candidates, while a separate model call only screens requirement responsiveness and cannot confirm legal applicability. Authority validation failures fell from roughly 30–40 per run to zero, and the candidate count repeated exactly at 68. Numeric construction now inventories receipt spans deterministically and asks the model to select content-addressed candidate IDs; derivations may bind explicit supporting inputs from other requirement slots while remaining fully recomputable. Value-by-period coverage requires one receipt-bound domain that explicitly enumerates every year.

[//]: # (ob:54f1d1e2)
The optimized repeated runs still did not pass readiness. Run v10 covered 27/49 slots with 22 gaps, one period domain, three derivations, 468,162 input tokens, 37,482 output tokens, and $1.0730833 known cost. The exact v11 repeat covered 25/49 with 24 gaps, three period domains, two derivations, 468,647 input tokens, 37,398 output tokens, and $0.5872335 known cost; the lower cost reflects cache reads. Both made 23 construction calls with complete token and cost receipts. They agreed on 41/49 slot states: 22 were covered in both, 19 were gaps in both, and eight flipped. A private review queue identified only two slots with shared concrete candidate objects eligible for Human Approval review, 15 requiring semantic candidate reconciliation, 19 source or construction gaps, and eight construction-stability adjudications. Human Approval receipts remain zero, so no answer executor ran.

[//]: # (ob:3eb73212)
### Stage B — fixed development executor

[//]: # (ob:059dd987)
After Stage A passes and eligible objects follow the normal Human Approval path, compare the frozen v16 small-seed route with small-seed plus exact working set on the five zero-heavy tasks using one fixed development executor. Freeze task prompts, sources, graph version, approved objects, executor route, grader panel, output handling, and retry policy.

[//]: # (ob:1adc7e2d)
The mechanism advances only if it improves criterion coverage without increasing unsupported-claim, citation, authority, native-output, or governance errors. Report context, tool calls, model calls, tokens, latency, and known cost next to quality.

[//]: # (ob:70f596c6)
### Stage C — frozen three-executor confirmation

[//]: # (ob:b15cbd8a)
If Stage B advances, freeze the mechanism and run the same paired panel on GPT-5.6 Sol, DeepSeek, and GLM. This stage tests executor interaction; it is not another mechanism-tuning round. Report paired task deltas and intervals rather than treating model cells as independent samples.

[//]: # (ob:aba800da)
### Stage D — full native panel

[//]: # (ob:0a68a28a)
Run all 12 native APEX tasks only after the zero-heavy construction gate passes. Preserve the console, new-DOCX, and edited-DOCX denominators. The full panel estimates whether exact construction helps beyond the deliberately difficult subset and whether gains survive native artifact creation and validation.

[//]: # (ob:547f6374)
[//]: # (ob:v18-success)

[//]: # (ob:1a89deff)
## Success and stop rules

[//]: # (ob:ce1b9cee)
The phase succeeds as a mechanism test if exact construction increases atomic requirement coverage and native task quality on the frozen comparisons while preserving governance and staying within an explicitly reported cost envelope. A higher aggregate score does not excuse a regression in unsupported claims, citations, authority handling, artifact validity, or admission semantics.

[//]: # (ob:ce89e8b9)
Stop and diagnose before another paid run when a failure is attributable to requirement compilation, graph sufficiency, object construction, approval coverage, projection, execution, or delivery alignment. Do not compensate for a construction gap by silently expanding context or retrieval budgets.

[//]: # (ob:123fbd56)
[//]: # (ob:v18-claims)

[//]: # (ob:fe420096)
## Claim boundary

[//]: # (ob:aff04e5c)
Passing the deterministic contracts proves only that exact candidates are structurally bound and recomputable under this harness. It does not prove that a source is legally controlling, that a candidate is correct for a real matter, that a model answer is lawyer-approved, or that the mechanism improves legal quality. Those claims require the staged evidence above and, for real downstream reliance, Human Approval under the applicable organizational policy.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkwZGEyYjk0M2QyZjQ4NzYwOTUxODU0YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImVkZTNjNDM3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8zNWQxNDA5YmQ4ZjgyZjYwNzllMjcxNTEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q4N2RkZGU3MDU1ZjQzYjc0ZmYxZjY4MCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfVuP3MiV5l8hyrOA7cks8X6pBnYhq-W2YI-7V5K9BtyN6iAjWMkWk0yTzCpVNxrw2_yAWczTzOv8MD8MsP9izzkRQQazMqmSqtw3B2C0VZnJiBMR536-E_zmjHVDVbJiuKz42cXZbneZuZz5eRYG3C_DNIndLPLSKCzOVmd5y28veXUl-gF-22-YH8UXZRbFEfc933ODwONRwYq8LDwfng94LryMRX4ep74fJoGXBlnpZiKM_CL1iyhM3ADG5VVftNeiuz27-Ab_GC4HdgUz1GzAqVbwj1zU8MEfRVeVFctr4XTiuuqrtnE28Pu2u3XyW-ezrm3LXSf6Hp7ZseINuxK4qNnHXfuVgOXuOxxwMwy7_uLJk6tq2Ozz86LdPik2otlWzdXAmqs0cJ_Mnu7EX_YV_Pty34vusmibXjSwF0O3F9-uzjaC4SYKLoIiDJIz-cmluKYfweaKyyDiXuhmOU_L1C9jN8mEn3iRh5S13YBLu6yrRgDl-kTqS54mnHORuFFUhkGehGXplXHqyuUo6i4Ltuv3NSzYRzqLtuP92cWfvzlT039zBqfcdj3-S34t-GUOW_7ns33zpmlvmrMvYA2aH_CAhz2vRP-E7cTbNRDUDGtxzeonz__09Nnry9_-_tP_87vnH3_y_PLZp79_9frlH569fvHp7y__6KXnW362ei_GYsPQVfl-gPO8zFlf9Ti7qMtL1sM-D4LG2w-btkPq31QNDtnf9oPYwjcN2-Ix61Ws4NEeWePsotnXNayp2MBZCrkbed0Wb-DXZZlnmReW8HM4xkG8xRX__L___V__33_9-y_gQzUJg33ntM_Ab-IGPvnzkydfXDg_c37e5hfXXroeqqEW-MRwuyNuYx07-3Y1zeTlWZGVIprN9PwtbI3zWyC4FvxKOM-AlYCLCtwCB4ZdouBnzj2eVtQgAwIzzwgqkpyJhLuPRtDhlvQDG_b90p64ZZZlAS8fjYRf_vIVTXrxy186hfncbsN64bQ70QjusHIQnfPZyyg6d37fOjtWcUe8XaAzTRKPu2n-d9sqLgpSY0ubFbsi9qMsnREBuo7DlI4ewKmaDWhHkBWn7NotLXKRiX7m3HOIBU4qM57GXv64lP1WiJ0zbAScDKh2mNJ5VrNq63zSsd3GYT19V7CmbaqC1c4VWg483H6f9wu7GGR-kXiheFRaX4P1USwGVHWibDugu-kqsCL9fBFXRP4NGBoHSeTOAq2gIEHFB8Gj0nrIen_Zg3F9F-v5wHmlmxwQUm0ZWFywOoJ1xcbRI72T304_t8BkoQAuSwv2cBqescZRFnyL1ozdMDwuFOf1m1GcZ-qjYxWcbcOGpdOKs8xl7BEIfA0MsxVorqp-62xudy2wEJhDB_7XsK5rb0B9DfC187e__scWeU1N6FTbXbdAYhKwhAnmP5zEQy6qmmvWVawZFvU9eHoF2Jy5Hp3pzWmcd3DR6acWeCgG9RmUHn_o_N65g2dkMJGzq-E44HzAd9xVwEFO29S3UiJR_gfWv3HAS9vuJgprUAlzi5wnXuZ74UPJOzycXbUT6E0uHY3wS8_nB-4J6Jpd28Ni9AjvNiV3fr9wHG6ehxAv5B8-55dffomPfd6AaFbX5jbDZ46z_p8OG9ptVdw5KvntRF7RcnHAKpEI44h9OG3IISCPNU3K1PEBMwCTfPbSgWhl1wN1aMJ4xSHEARpxi8BpddjCQYWxCKL4IZt2yB7aRV8U3STP4iLP57bo11XXD4eL7OuqeBejLD64ZATyNI9Y-BhUrJ0vOwHxBsYyl4yzHfiET8gIXI5GAEO7oYOPzne3X4LFLfF4nJItyHAeiFLEpfcIFN611KyGuLdg7zLXWV6mnlvO9cj_Np92epAH0bzznE4-tHBGeQJRfhpls9nBLQeb-hQM1v8lDw12FTieQWQ5LJPwM2f50QVCvDSPvTjxHoOQl_tGO5xSWteTtOb7quZgkVv5kxIVESj-rwWGAYnz9VJgkXE3EFH6GCSuZ0quaPfwX6CW3MyPPm_WBu2UZhF8NXrN6wWOFoWbZWHJHoNG_dgOI_pe2siqdARmfaTyBidaumLwTdtAyLYfdvsBYsklvyYQeRL4nn-ExF8RiWX1FpQjh3nqdkf7I96KYj-03f247x6jLNm5KOM8S5NHJu8phbEHW4onDhbgqsLsWJtjkgs0VlvX7Q1xZ9N2WwiXlhIVjBeJ8PkjUzt3ahm_ZqBJJhaopPMK_Ag-FIYzHWocYlR2tWSX3DICyxQfofaZpFZK4rDphFhrQtFhLivYifsd_31GencEk3tRkfOU_R1IfVGOjKp3dgXDCfE1RaTmxgN_dEqZ9WwrnN3C5rKcpa7Lj1H8saR4X9eO8r12rBH1_fbz9MNLUsTilPnpIxGDCp3B7z1fP_L0s-d_Ih2kmFJmiXCfvhZduwaSrm9lVLgc4ZRxkISPQ-SdjNq-gJNd9NM8BjZFlPOU2iv5HB0-Op7AAbV4V4R18qGlnKLANKcQD5wddYVMp9CKBe8x4cMMNsaKAFkOSsKZsfrC3hQizUSaZw-k7hX-Cn_OK3bVgNvt5DLjwxoM1DuZUEQhu9mAODNwGKt6D9-D5790cn5Q5jyKH0jdIc8UmDVbZJlShL7rZvOJZbItBy-Cs-72XcH44Y8XWISVpRuKqPjA2T4DM4d5NJRLLkBCt1WDqbXC0b567ygzQlI8bNigueRwD75Y6arIGZgZTKZdFuDWyUIDfaOrFuIyZUXMMxGGiXBL7vo5c9M0Y_hLOHUaUxVuHFW4cYqNKN7s2qoZqA7V0UxYi9B_YSniC6z4QCRwa4xgVoGMQai-9IEFor4th0sIX65Et-sqVYfqc-8i9GKR-CxKCw8OJuI8yiPfZ6DFSsHCOEmzouBxkMcZK_0ki1mQiiJyY5dnvpcF6Llinp_qSfK0LkL_W9hoLN74rh-v3XQduK99_yJMLsLwn133wkWK1I5ToYxFoRd6wCbTp998PyUo4lJZIgL9s0GxDPPQTVkJUSdKCI1hVI0UA9-7HKRGDaLI8-MCywpCj2pUiNSoH1ri0ZMkXhgFEAwGEdeTGFWfE6SfLtuoYd04ToKM-W4WZnpYo5Kjhn1IKUZ5PmQfKSLIBShS1KigZ2UKhUaRabjyZHQ9huxo1tcyL2RGSeAkSdXQ7LfgcBYQiFQcI1xKG8G3stpYDbdT8ASfzvUOhH7VNU0KXx3J5qxIebNxDlLIzhX85tx5Cs7AuDmYNFQOO5DHqsaY1IForqqd3-y3rHGe7lDDsfr89Bnlbhm4PM29tBzPyKhinTj6pTKUGjjLeRb7IgWdkOiBjcqUZtyHlJXUTAVPozxwyzQp_VHwpkqTmukhZSIVtMLpvMFRegiM6nUvMLip-qJuezTaeoh9hyobOYrt6ynkgWUBM4B6Ucx47cU0Ikb-nejhpz2MxiHuGpyv9kBhiZn2Xc0KbcVkRYhGQutD1m3MTDk58tGwocEhUALuhCEqlJy5VG3BK2JDsblQHC0dWYyoUWRUFhRYMAcFu3J2GF5xg8ErQcxbF_taszKuQkbfOMS2l6YU2I_RzqFBpZ3esltaHdpfYNoFpixz3xNpWsZF7ukTNepx6kQfUkw7LOIoeTp3XsDJtfA4EUo2HjawF0Azl6Os8P-aQe88jEUFFcZhY5F9V3hCw75rzF3Cw28nJXF-IJ9KjCXR5I3sGJJK-ygf-hpo4u0NHqRgW3igrjB6W9jEzPPAQIdxLvgogEah8IRkL1X51MBJJpIyYUlSUowlJXsq_JmS_V4FPDV8yKLIBX8gCorRjho1Pe0IPqA2NwviHBUrjVk5GVsboZyUEGQe4HLnRrA3okGmGm2A8q9MK6A8VJIWFCvNHcBKcPBgDfr_dXqDCw-chiTy4zQYdbJRNBzZ_yHFP3J8KVEM7Pi3v_6n8ysdmkwaC-woGj7KuSnFQDtmpg972JSag-29RkEBHV7DOXCqbtVCmnFgZa1sZmZzJT3xtob9u1ofsaCnDajcVCR1B-a7GsBK7s6dl6MyVFSVFZhNNqe3BsEGURuA8Zy2dFhR7LckpXCidQtBWo0MW8MwlK8qwA8GvXD6sJhfZILztMgomKfDMsqnJ8RsuQyqho6CyAV_EoKH0NVDG5XRSdDeq8ap1UPpZyV40yGLx8GNsqca_CEFTJlVVvKmDATSAwe1z0FL95hWhlNiTX9DxoZi16oGfoOTKBiizxyUamDMvIKQAdcGg_Tnnzf-ufOc-FJaqnVdvRFO3-474K1-JwmEjQB6gaeARhV4a-mDf9SikJwE1rTe4-44t6ClVAQtv9R2ECYMwAcDC4bpRuAv-TmW6RiuVZbUlJUD2-3kFebTW7S98GfLb9fAlWjclWsn2R85E3dxL8PBY-yNQmNIRqWdVlgiEBWCL2yMiAEtqNoOthv8EjinW2Wb8BgonQtmREpphbldoGkvnJtNRfhIhPjhLmBEvQI3EqQKk4rkzhS3oAdg44Zb7RLI04L5pNMGxET6SKZ1OMSJuDbckJ7y9BIPemQ_lHnW6UYiTnIfSHknlHHtULGS57OvxUoyBBGLilbyGP51l1xyv7aCV2jSCTS4Un7XSuVokC55fPpYBCwrhoM_4tzLIx7PyGC91XhMK8Ublfzjq31X9bxSbCfKEpkMz4pUHfn-40Q1Js2VLweTojeCAMe1yvHK44SnUXt_3iTnzrMxnlCpcOmvjm7s9CmJAaqaAe3HgII4f9zQJWrqLZi8uWUAfXJLDuM4weiRfN6kFKJNEY50rpCbrmhS4Es0iKCHB1zUojfUt8A9k_mcXKgjhSil2fwoz9MsSxI-hTQGYuKERl7CPmjPpIRgVoARjrNRZRpwiFlIcx94gxpWBL4fBODdSvMuw-QJ8aCGfSCCYeYsgRBheKWYdoRTq1_OI12pWJ4cjXDhYyOoVY8fwykAr3bVW_WDDZ22ZBzkGDTDh5Uo9VMj0qL13rTdGxT-XuhFq90YOROZPq8r6a3jTn_ewM4dwW_o-Fd4AY_8QARJMJnBEdJh-FofCtFolGVgeUXOFoUYsF4wIPBLMJ1jvAHbssf8E0WTd4WiENWOpAjzG2yeAllwUEToh26QFXGWj-GxgQ05IQ6LWA_tn7iZx1KI6V02uT4T_GOSh_dFcWg_OAzjssjSLC3G8Q1ghxr_IfiMql5j-I6yAEHjlsnjItsk3Y-SlN1coMBwzITD9PsbYC9K_BipnoMEj_YXZMJduxJoTmD551h_P7IeOPLLwzWN417uaDZBiwOHVoDHSo4JfSolJwezWUubIED14vc9RA4DeASouzFXrANzFDBpDdGmSt1NKAH4k9xnTPwJtRpwvJ0XH0_hEQxF-RwcRGonfEoqGu1NT_tHRl6FSOMe4rnKfcDiTf8E_3u5eKAgBR34IUIhAkZZUZu6Gj0e7QUp82x4KqMnJr8Z2BYcB_j0K-0mHo_tjHzhWgbuwCANzTkqgydTLknaXRrvTpaPHiLn8-BckC1OWzvBgzzMvbSI41wLiYEtOhnmvwMipKMbL_B5mPiun44mz0ANTSL-PgAgnR7mRRLEmV94yUT5hAkax_4AZI-eIcryTISFJ8IpeT6BfdQMD4HsnMoSGM4SxqUkXshQJIukBeAPFKaLhSwYuBUijOIkStMxNTvhgEb19wA0z_QJ20nmw-gRtN9aiY4SfBoIN4DyUntUmKgZBSs2jhqDVkO_U5xtiIzysCdpm2kVSaXpdqo6aI9NWmM4e_dnBTgHKIPtG4F6Ftu_KFKhRC329sDP-2FBdnhRuKUIOYTqo-dloJgOIEwfgkXaS2uOewMi3-rtnTQTfKb1NKVnmkF6FuKOGpDrkrOOgegYfCozomgkAI9SMPokZSHhE7aTQTVDpA-mh2FQFfRQKUGnVBY8itgN_cQLsyBJxwydgay6I7gfBorSUlCCb5bFUR5442QGTkpN9hCI04GjhSy-ouwGbpOREsSMveGQkhMtg1bj012911bIcFZn-uOO0thTKh8Z5_QenTu_Viidye8fLWu_UhluVRUFVqHVTIWilRG7Id30ABeqdDaGzhvYsno0ROiGgEWjqvNSBgzVa1QwIfsSpZadsGFH05XvB-sSo141Sh_7pt_vUDC0K2UG3obqkRHCWq6QXA0j9BBdB27eqKJVhhR1Sltr_bIFn66-p7JxGky4DO2YWl2QIi8UcZKA9XbHyMMAqd2Roodhy_RZ8RIsYsxKLx1jYwNupiZ9CEqMVWgMZEUWTvCTz16vo_PYedUCl30sxO6VEG_krn3yu3_BDAfEUD1NRt7eQb2Mkab_iNhDBkkaOzPSsB725LJSZmgytpIOkhY4vkG59jQoSHnvgAux0QlyrKlQAlgdtYCjxnoeaE6xEw2nxDHD8GUpE-ylflkKPwuFG-m9NYBxdw70vcBtOmsbFLGfc1CIxShrBt7N8Gg-FLOmjSulaqQiPXc-03lF8pPgZy0m3xpxs_7402d_UpaJY82WPoAdb9pt1VAMpWrvuEzJFVgD2lL64GYj6BDugrOcjah3WM6_xcKbxPCYIXNVgq-J5VV0B4X0ePRoV5Q86vfdNa5cbYCOZ2VRj1JJU6SHCcyFAFrkLkS4Gcu5b6ThNXzvFDriNARPp5O8xOU8j93Em7zTCZU3-dbvA7DTyiXM88QveJKkxZgDmzB3hk7-UPicVsVoZ-8mnmZJSDNjpfTiQbVNWtuqh_FVPlplsslxmdS13AF2ix-jScAE_OSyUOVGWgSpjEVDhhTxE86mukLmYFdXnSDe7gusCIzJFwhOwa-lnPyVyjajJ2ZYGRmq9ZOZmUX-hunUrEbcRTboeAlwgeeijJVRmYNtyOLp_EZU4uiZfjjAUPfQU3oeDNb89LC0o0yp9Cz6PUpcJW3e6L5P7KBdDlaPZ0_p7zF-lnpdFzdQmmVdEfyzBic9dz5uFTwAQu-mxyMiRMKhWtphVNADjzR44HD2TEcqsrpJGZsRFbHnV2KxfucFYBHLICozb_JeJoTlCek-DZbUkCo_EUHph5HwxuDNwE8atbt7QCJ1uJIGSeFBQMuCMR9moCR1i9cDgI9TZpfKBCp-AVOish7KLTSKVvChUEirDeswZp5jKGgmhWTQeSD4bQ0yiKMaFeCV_tWURaUqY9chr0lWAIVTY_ADqxp_Lm22LCLS0OzmVnRr7QFLPAb-dO65jN4mkTL6a2CsUI7k-WqhkO4NGm1ulLBzXBnDYpnMEsIoRxAaq8P4Qu-YQIkBvUXb2HZXQJbMS2EMctzn_uJb5IYjF3RI26uu5_gUxOfpC-cZ7Mvbsy_ozg--L05-fXC5x92vCbUxfv-ygh3suPOaAXP-oG4AAW1fdS0pk0tkkf7ERSBUf_jQe0AeeBMFMCuhso4gjCXLnZrs7vMKTfxSHZ9Kz0jZL9uCkjRa4mV1kX_FCkHQpdHCyQyMQksuISTPJY16yd-c3Wxux9np2Wu6bIcyQ3Lyv8xTgoPW6NNEi3AdPe17YK9jlruZ73pYT0u4L0SW8TSJwnG3TFC1CSg2gdbffMfnfn_8-IifHke78L49DpB-F1r8USDhaRmFfpHwKIggJin9XORpXIBBSvIix0ubsrxww9hPU5Rf7kWJL1w3yVKRFGVGUe-JJR0DhacXUXYEFJ6WaRDmZWFB4T8SUHiShglLS8FEaUHhDwKFvwDN7Xl3lb1MpOBzXjBpfUxHlpj6lAGDqvkbxqAn82Gx5hZrbrHmFmtuseYWa26x5hZrbrHmFmtuseYWa26x5hZrbrHmFmtuseYWa26x5hZrbrHmFmtuseYWa26x5hZrbrHmFmtuseYWa26x5hZrbrHmFmtuseYWa26x5v8IWPNTIPNT6HILK_9OYeWP8Uacu2PfefMHQjrjoIge_c0fXErTpBxkPr2STlXRteCphBmlPPoLx19684fLizwVj0TiSA5SiWOMOmiEUJHU6chmCp4eE_iPgL15EXWNwFhHYnCnGrdM08Nm6vVCfApqVbo4mkSaegRGnp_inXf0IUhHS-Y69GzgEzRCVsu0LK4Nlws0mPKTsLR0gq0OzmI-5-Rn6Sknt0C6DyvtjcjwgRw2BYQ8P8Umi1MS4k9p57U0VzSE6BQkUUIzULlTykz5Smqz391MoTBNxpk17RSCE4eusKQNRoYhIpTPvWBcoFzqEUJH8Ct4YvLUNQ9IPO_kZ1KoRTA3E194pdN6cm3v16IR-UkceUUeeMILvSDJgrgImMhPtWiM8P7vrUXD6tAfgQ69fyPQ4UsI_JXRe-J_e7y15Dtpp_GS2Gdh7MVRIuKwKEWShG6SRGnMkiJIfJ7FZRGUUeBGaZRkQJ1ARD2DJbrwbX6fxd1prAkuvOwi9I401rjMjXKY1DbW_Dgaa3wGui9mWc48_36NNZO11MbmSOnxaNkRS0kqCpqKBq83Zhh30P53RZGeVEgrCJVliDQpDJVxncBeSuwvZODoZYjcCUP5BKY0rsUdrC3QJjpxrAjpR6rkRHD8CcfbU1HsODQY4RVag065u5VCOCqMEJuSyFTJhaBO6ytYkXQJ-B27OrPVOhweDewTCSMcj4WKwyqEtN05tjvHdufY7hzbnWO7c2x3ju3Osd05tjvHdufY7hzbnWO7c2x3ju3O-Yl253g5z1kWsTj0Ctud8w_YnXO_fSDYxCWb7QKGLmY4h7nNNW3EzL5RwQKhru3-aqOSoIiPNjCl2s_tEGBEPNR2d7oNIIgRs9aMwzTpqeWMVVBxv2Vpx6Q3NAy53j3DVIQ-8lF6FQzzOEpHQ1_oFiBNPNh6PLtG3JiwZNstZbulbLeU7Zay3VI_xG4pUC5u6idBlo9KwQAWHNu294QHhCdrbFP2hGRRJSQLBb2UnHh0-_uPsD5Hw85qcx9pAAt8Qd_ePaUe_YXxONbKe6kFewOR7KfytA6KhjSjedXe1PcDvOJlT-D3Pw-Dcy_9H7-QSYf5_YMK54h7ciUagRt2eO-fFx-6hZ6rojQ4ry1aYPnZzDlEjaUdTsHvepK4GUHmaEDlJH6jUKruB4m-wtCA1IEXmeZ7wj_9k3seJbGfwPeUb9HlRkc6CASu7keL3VMkf-DMOB0mObCCSqYSN1Cz_VgnVQoFv6NQf0DE0AIDF2XuZ2GSsNHyGLCTkYE_HDwyov_V4aoiHfU6TIXHHnN2FBDI9ifDuI04L7o58oJQx3D-srpGSWzj9GQ_mPJ64eB2-94o-hqei-LnjyZuGw9kNU8Oysyn1PKqbvdW5oyaZs_qWUnuIwWilshioZJyKjOvysyUuuwFek06OTr2KJG2Q0ef9VqG5baBG8ko5TvxfiMj8zUlrKgI-QbLVKTSDKZ1vjyEh7x6_RT--_Ty5fNXf_jd61fnW_6lbQi1DaG2IdQ2hNqGUNsQahtCbUOobQi1DaG2IdQ2hNqGUNsQahtCf_jNTCwsMSILHqNTaHpJx5jMAbG9XZMdxf1HfJmKQXQ2E_GP6HY99muW5jmlO2RQiXcHLp6q8B92HYLhbfZCtQo-qMWyJYPI6hlYcmB1ezUWRuSUOqeHkSM4VHisQPX5qdNabHq82dxK1TFrEJRe1JrAgMoVQP8C1BHp4FtwkGVN63YGHDISce_shjyy43MWPdz3iQ6dmz_eAYkEgvsB2rWbV4beq6cxE36SuEnByjwMIz-G3StF6aenehrHzqqfek_jD1gN3L8t9bCnzjvdMDi1zH0nDYP4grCIuywqA5-FvCyCPEzDlBVg0OAzEZZhIaKUlS7LWcAzlrnCS-Ik5lmS-B67z-LmDYPea-wT9C-89EjDIISUZQrz24bBH0fDYFCURRG7AQtY-r00DB4RZExbO8SLJ22XeiGWUWw5agy1Gw9mSciGQ91Tpa2RrJqbrwwzi0OfNgYKKMzWVAZBIwe-_02r7A3F5bLpi3BGWJHT3WpBdLdK6jxxvFA20IPZ8WP42w9WC-2EGrUsrflhE77uaVToFApwlIk7CtIEg1jXsCPUlMjmTRcqHFD2U4O5xzPSSFzV0mj7EG0fou1DtH2Itg_R9iHaPkTbh2j7EG0fou1DtH2Itg_R9iHaPkTbh_gT7UMUAXMzHvPcDSLbh2j7EG0f4vfch3h3AVT-vNQp4cvxEC9VfXRGvcynGKy50t7g3SyqrK7S0qhDB408LPA3LSK3_nD-ClwWoG7lfNJev2jK1nn265fyVF68fKWh0ufOp4ow7YajhnYUymsGP8GMtXJ2gB5wWat-Y4anzjxja4b0tDVoIDBmqZ1PYLgbJvPmRhZ9vHQXE0eYsiXPFf3sgoHq4U_o_ygNrf55gznQFUkD8knfkmDqOOoQmzxrI1np1rp1WYn64G47VGn4mIzvbYOpbTC1Daa2wdQ2mNoGU9tgahtMbYOpbTD9LhtMRSY4uCVRGMRj94oBZDPyLx8KRzOrZONhmy1hhDXv5RsadIPb5FPguyCatXJFJqSjOkTatMhVF2IbdaUwQ3dkP8Lz1QCjrsY8gsLWjNnYI8iaMeTEQQx1dRTuIonAQTXsBc4HzSSsSoJyyKT6EnjgB47sqam2Oi0uYTagGkRF24O7MU5peFoSLUP8IfnHSFyzRji6IVVHX1pgVBBGlhA4DohnpoEexrYAQn-QJPayN3SURM3CH2G-DSxDP9AKZ_0L5n6oSg_hIDpRky7GEBEGh0VRg8x0aIMqdRHI3Hnd0ds-buEcr5QEytVS46dMZUt73rf1tZghgiZ55C0lsw9qmbojQuuGGVSAFMLckYPntS0xAcFmUKqCPoY5xwOALoSTxRutDQ7yirLSdGgJqL7X9KAMumUFb_vDbX-47Q-3_eG2P9z2h9v-cNsfbvvDbX-47Q-3_eG2P_yH0B9enOgPL070hxen-sM72R8-_ODawxFAdomuSWf7wg8bQgvGIzcg3fUoDaEU0Oh2F4zLdEV3S_GllL5OYOGa6gYaEryw_CgsPe4J_7FIbHfgUOpajmwZIyiI7MXS_TWUJBlrj4hHfrzW9T_sSF8pNTG-GXgkZ2rx0qXPyUj2w5TLUTpCOdQ68XYl03RH3qV7n5b2j9tiT1adKoyUn1rL_JThvqwPskpUM5INeSZCWap_uag1-hXyHLCBZH8Iljs_xZbHG-CfgxPHVHFubrbMl_qZMJ6GT1lUM1KbLWXdg5cKvo82sOenOPHd7yKmNhO5-tEKrFRhD1kfc4qztNx0G4H5ZmHj_c8LPfmntoD86RHcIKVyNGrj5QhHWW6iWb-1-DiBVMp8r-78IOIeeKo5T0uIgSGgwXZ9mQ062p0_tjH_1LvzrTJ-iDK-_x0Q7_HG4amF_ju5QIDHURG4YRTlnlfkLPYiVqQZ-PB5VKZZii8V5m5Qhl4W-qXgZREWrueLKI_z3OPMe_83DnuvXe_CSy_C8MgFAoKLoAiDxF4g8OO4QKAI3SjkCc9c3_3e3jiMuW6jCqv1D6nDIxUuFfX3i5cGYO2CLHNvGDfwcXZYgLqWoEVt3evblY7E-nkL_mG5TeVq-gmEYjgyZr1NewtFpWEZsmTYH7RAkAad22IFplhL5OfUbwZa7LnCR5p6rz11ycFYsfQTWZqNNK6FXXVCnlvoPVG4nRF_XYtywHc19zL-pooveYvV1QbboNTneiiJPZfFXEKnHCnnEgLneOeByt7O73CwFxXYiwrsRQX2ogJ7UYG9qMBeVGAvKrAXFdiLCuxFBfaiAntRgb2owF5UYC8q-Ae5qCCJCh4GfpJk-Q_6ooLFjNlBi5JU9LO2Z5WmO1ETtFcd2KsO7FUHP_mrDk5uzV2hxVrgJQEC5psjGyr6KT2uWHc6aGJqU4L1cU93y0MMJBOLOIsjYQfUcmGK-1iGR5tVlbBgMmtq_TpvZvbC2Gsd7LUO9loHe62DvdbBXutgr3Ww1zrYax3stQ72Wgd7rYO91sFe6_APc61DAm6dzwKIXdwJwjgBmA3x_VAY8jFAoN63truYMgK6Uk6hvcExI6eBo3oceYj83R-8Qs8EHcp6oiGokwGWEqVRiWaAcIBLlC8KahRaiCpesolsdoZmZW7qM57c9FLAlLQ1lJ2DqQP3b3_9t9ClMIeUV0ueh4HXNzyjfWMgDbUfDXIUp1PZdeYe4ZYZaMUx3seqYH9kM0mhYXhGfXO0S_gePxJB7XavGedY_BTcoO3Fx2DcDHankhoVJEcfUqWoZNeEtJm4EbJp9RAQ0Y9FYN1pgc3ktzPTe-78EVOt6_x2rWR19B1H5ChpTwXeVC8pJHnWHZBjE7EgF5FSedIuY-l9yTPKIlamcZ6Bgz8hIUZYvSE4HwqOx8DZNQCjGhWqgLu-TyZiRUuc6aqV8pFm2ieM05UX-6o8rSPBIFmFqX-YlEIu-Cfv3E0CNw0CM0JUxW9qdPY8taCJxghplNSFijpJyqEuxVd93SEvDpO75AVZepQ88JbTxA_Ajk7kfURsWxPMSDnLpQT4UkaOthe29lfAcsCf4COCCb0bJx-63_SatNFNn2Fkb5dguxd4RDI6U_tTYUsSXjTjZfILbePlpxOit6yr3Y5AtmPMO8t-GlhK2c4L22mwRr9RiCdEZQ7iTt27n4qb5TEUMM60wkBFipEsbyqYillQxAlA7ak8HeKTpZ8gLyeZ9W_35vLML9dT4pbxryBglYmx_vwUOFmH31JL9u0RBDvGQfYqI3uVkb3KyF5lZK8yslcZ2auM7FVG9ioje5WRvcrIXmVkrzL6Xq8y-uLb_w-apGBG)
