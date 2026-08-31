[//]: # (ob:ffb9914f)
[//]: # (ob:v18-title)

[//]: # (ob:1b9c9fe5)
# Exact Knowledge Construction v18

[//]: # (ob:c7bae7d0)
[//]: # (ob:v18-status)

[//]: # (ob:0f9993df)
**Status:** Stage A completed on the five frozen zero-heavy tasks with no answer executor. The latest Stage B closure slice deterministically projects official-authority candidates, screens authority responsiveness separately, requires source-bound period domains, supports explicit cross-slot calculation dependencies, and selects numeric atoms from deterministic receipt-local inventories. A zero-model-call correction aligned runner binding with the readiness contract: independently screened responsive authority nodes now remain eligible `not_governed` candidates instead of being discarded before binding. Reaggregated exact runs on the fixed 49-slot plan covered 29 and 27 slots, agreed on 41/49 slot states, left 17 stable gaps and eight unstable slots, and produced zero executor-ready tasks or Human Approval receipts. The paid executor remains blocked. All constructed objects remain candidates until Human Approval.

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

[//]: # (ob:d972d512)
A deterministic audit then found a runner/contract mismatch: the readiness contract accepted `independent_review_supports_candidate`, but the runner bound only exact-reference matches. Rebinding the saved artifacts under one shared contract required zero new model calls and changed v10 to 29/49 covered with 20 gaps and v11 to 27/49 with 22 gaps. The state-agreement count remained 41/49, while stable gaps fell from 19 to 17, shared candidate objects rose from five to ten, and shared-object Human Approval candidate slots rose from two to five. The remaining failure layers are five authority-responsiveness rejections, six missing or invalid period domains, six slots with no eligible candidate, 14 candidate-identity reconciliations, and eight construction-state instabilities. This correction restores candidate eligibility only; it creates no approval, admission, or executor readiness.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkwZGEyYjk0M2QyZjQ4NzYwOTUxODU0YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjU1NTMxMWU0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8yZWJhNDBkZTMwOGRmYWY2NTQ5YjU1MzYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q4N2RkZGU3MDU1ZjQzYjc0ZmYxZjY4MCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfVmP3NiV5l8h0j2A2xOR4r5kATOQVXK1YI-rRpI9BlyF1CV5mcESkwyTDKWyCgX4rX9AD_pp5nV-mB8GmH8x55y78DIWZkqZXesFjHIqgrzr2c93Tnx7xvqxrlgxXtbl2cXZdnuZuSXz8ywMSr8K0yR2s8hLo7A4W53lXXl7WdZXfBjh2WHD_Ci-8NLAS5nneknB_KrwEpZFLCjdrAzLiiVpkZZxWaUsKeMg51GVFiyvqiQs3DSOw6qEcct6KLp3vL89u_gW_zFejuwKZmjYiFOt4I-cN_DBn3lfVzXLG-70_F091F3rbOD5rr918lvni77rqm3PhwHe2bLiLbviuKnZx333NYft7noccDOO2-HiyZOretzs8vOiu35SbHh7XbdXI2uv0sB9Mnu753_b1fD35W7g_WXRtQNv4SzGfse_W51tOMNDjKIo8DwenolPLvk7eggOl1_6PGehW_LATeF0qjgKsxwej3FlXT_i1i6buuWwcnUjzWWZJmVZ8sSNoioM8iSsKq-KU1dsR67usmDbYdfAhn1cZ9H15XB28ddvz-T0357BLXf9gH-Jr3l5mcOR__Vs175tu5v27CvYg6IHvOBxV9Z8eMK2_P0aFtSOa_6ONU-e_-Xps9eXv__j5__jD88__ez55bPP__jq9cs_PXv94vM_Xv7ZS8-v8VI_hLDYOPZ1vhvhPi9zNtQDzs6b6pINcM4jp_F246brcfVv6xaHHG6HkV_DNy27xmtWu1jBqwOSxtlFu2sa2FOxgbvk4jTypivewtNVlWeZF1bwOFzjyN_jjn_9f__9X__f__n3f4YP5SQMzr2kcwZ64zfwyV-fPPnqwvmV8-suv3jnpeuxHhuOb4y3W6I21rOz71bTTF6eFVnFo9lMz9_D0Ti_hwU3vLzizjMgJaCiAo_AgWGXVvAr5x5vy9UgAQIxzxZUJDnjSek-2oL2j2QY2bgbls7ErbIsC8rq0Zbwm9-8okkvfvMbpzDf227YwJ1uy1teOqwaee988TKKzp0_ds6W1aXD3y-sM00Sr3TT_D_sqEpekBhbOqzY5bEfZelsESDrSpjSUQM4dbsB6Qi84lR9d02bXCSiXzn3HGKBkqqsTGMvf9yV_Z7zrTNuONwMiHaY0nnWsPra-axn243DBvquYG3X1gVrnCvUHHi5wy4fFk4xyPwi8UL-qGt9DdpHkhisqudV18O6274GLTLMN3FFy78BRePgEktnYa0gIEHEB8GjrnWf9P62A-V6F-n5QHmVm-wtpL5moHFB63DWFxtHjXQnvZ1-b4HIQg5UBlbDw9fwjLWO1ODXqM3YDcPrQnZev9XsPBMfPavhbls2Lt1WnGUuY4-wwNdAMNcc1VU9XDub220HJATq0IH_tazvuxsQXyN87fzj7__rGmlNTujU19t-YYlJwBLGmf_wJe5TUd2-Y33N2nFR3kchWIc8mcvRmdycxrmDik6_tUBDMYjPoPLKh87vnTt4RwYROdsGrgPuB2zHbQ0U5HRtcys4Evl_ZMNbB6y06-20wgZEwlwj54mX-V740OXtX8623nK0JpeuhvuV55d75gnImm03wGbUCHerkoPnF67DzfPQ99z84-d88-YNvvZlC6xZvzOPGT5znPV_cdjYXdfFwVWJb6flFV3J90gl4mEcsY9fG1II8GNDkzJ5fUAMQCRfvHTAW9kOsDpUYWVdgosDa8QjAqPVYQsXFcY8iOKHHNo-eSgTfZF1kzyLizyf66Lf1f0w7m9yaOriLkJZfHFJCeRpHrHwMVaxdt70HPwN9GUuWcm2YBM-ISVwqZUAunZjDx-db2_fgMat8Hqcii3wcB7wiseV9wgrPNTUrAG_t2B3qessr1LPreZy5L-bbzsD8ANv77ynky8t3FGepL6fRtlsdjDLQac-BYX1P8lCg1MFimfgWY7LS_iVs_zqwkK8NI-9OPEeYyEvd60yOAW3riduzXd1U4JG7sQjFQoiEPzfcHQDEuebJcciK92AR-ljLHE9E3JFt4P_wmrJzPzky3ZtrJ3CLLxcaat5vUDRvHCzLKzYY6xRvbZFj34QOrKuHI5RHyG8wYgWphh807Xgsu3G7W4EX3LJrgl4ngS-5x9Z4m9piVX9HoRjCfM03ZbOh7_nxW7s-vtR3z1GWdJzUVaWWZo88vKekhu7d6R446ABrmqMjnU5BrlAYnVN090QdbZdfw3u0lKggpVFwv3ykVc7N2pZ-Y6BJJlIoBbGK9Aj2FDozvQocYhQ2dWSXnKrCDRTfGS1z8RqBSeOm57ztVooGsxVDSdxv-u_z0h3ezC5FxV5mbL_gKW-qDShqpNdwXCcf0MeqXnwQB-9FGYDu-bOduFwWc5S1y2PrfhTseJd0zjS9tqyljf3O8_TLy9xEYtT5qePtBgU6Aye93z1ytMvnv-FZJAkShElwnP6hvfdGpb07lZ4hcseThUHSfg4izyIqO0KuNlFO81joFN4NQ-pvRLv0eWj4QkU0PC7PKyTLy3FFDmGOTl_4OwoK0Q4hXbMywEDPswgY8wIkOagIJzpqy-cTcHTjKd59sDVvcKn8PGyZlctmN1OLiI-rEVHvRcBRWSymw2wMwODsW528D1Y_ks35wdVXkbxA1e3TzMFRs0WSabioe-62XxiEWzLwYooWX97lzO-__ACibCqckMeFR852xeg5jCOhnxZcuDQ67rF0FrhKFt9cKQaIS4eN2xUVLJ_Bl-tVFbkDNQMBtMuCzDrRKKBvlFZC36ZsiIuMx6GCXer0vVz5qZpxvBJuHUaUyZuHJm4cYoNL95uu7odKQ_V00yYi1D_wlTEV5jxAU_g1hjBzAIZg1B-6SMTRENXjZfgvlzxftvXMg815N5F6MU88VmUFh5cTFSWUR75PgMpVnEWxkmaFQWm7OKMVX6SxSxIeRG5sVtmvpcFaLlinJ_ySeK2LkL_OzhoTN74rh-v3XQduK99_yJMLsLwP7vuhYsrkieOBmbJotALPSCT6dNvf5gUFFGpSBGB_NkgW4Z56KasAq8TOYTGMLJGkoDvnQ6SowZR5PlxgWkFrkY1MkRy1I9N8ahJEi-MAnAGg6hUkxhZnxNLP522kcO6cZwEGfPdLMzUsEYmRw77kFSMtHxIP5JHkHMQpChRQc6KEAqNIsJw1UnvWrvsqNbXIi5keklgJAnR0O6uweAswBGpS_RwKWwE34psYz3eTs4TfDqXO-D61e9oUvjqSDRnRcKb6TlIIDtX8My58xSMAX04GDSUBjssj9WtMakD3lzdOP-yu2at83SLEo4156fvKHerwC3T3EsrfUdGFuvE1S-loeTAWV5msc9TkAmJGtjITCnCfUhaSc5UlGmUB26VJpWvGW_KNMmZHpImkk4r3M5bHGUAx6hZDxydm3oomm5Apa2G2PUospGi2K6ZXB7YFhADiBdJjO-8mEZEz7_nAzw6wGgl-F2j8_UOVlhhpH3bsEJpMZERopFQ-5B205EpJ0c6Gjc0ODhKQJ0wRI2cM-eqa7CK2FhsLiRFC0MWPWpkGRkFBRLMQcCunC26V6VB4DUn4m2KXaNIGXchvG8c4noQqhTIj9HJoUKlk75mt7Q71L9AtAtEWeW-x9O0iovcUzdq5OPkjT4kmbafxJH8dO68gJvr4HVaKOl4OMCBw5pLMcoK_68d1cnDWJRQYSUcLJLvCm9o3PWteUp4-d0kJM73-FOysVg0WSNbhkulcxQvfQNrKrsbvEjOruGFpkbvbeEQM88DBR3GOS81AxqJwhOcvZTlkwMnGU-qhCVJRT6W4Owp8Wdy9gcl8OTwIYsiF-yBKCi0HjVyesoQfEBububEOdJX0lE54VsbrpzgECQeoHLnhrO3vEWi0jpA2lemFpAWKnELspWiDiAluHjQBsN_PX3AhQdGQxL5cRpomWwkDTX5PyT5R4YvBYqBHP_x9__t_Fa5JpPEAj2Kio9iblIw0ImZ4cMBDqUpQfe-Q0YBGd7APZSU3Wq4UONAykrYzNTmSljiXQPnd7U-okFPK1BxqLjULajvegQtuT13XmphKFdV1aA22Xy9DTA2sNoIhOd0lcOKYndNXAo32nTgpDVIsA0MQ_GqAuxgkAunL4v5RcbLMi0ycubpsoz06Qk2W06DyqGjIHLBngTnIXTV0EZmdGK0D8pxKvFQ-VkF1nTIYj24kfaUgz8kgSmiypLfpILA9cBF7XKQ0gOGleGWWDvckLIh37VugN7gJgqG6DMHuRoIM6_BZcC9wSDD-Zetf-48J7oUmmrd1G-5M3S7Hmhr2IoFwkHAeoGmYI3S8VbcB380vBCUBNq02eHpOLcgpaQHLb5UehAmDMAGAw2G4UagL_E5pukY7lWk1KSWA93t5DXG0zvUvfDPrrxdA1WicpemnSB_pEw8xZ1wB4-RNzKNwRm1Mlphi7CoEGxhY0R0aEHU9nDcYJfAPd1K3YTXQOFcUCOCS2uM7cKadty52dSEj0SIH54CetQrMCOBqzCoSOZMcQtyAA5uvFUmgbgtmE8YbbCYSF3JtA-HKBH3hgcyUJxe4EGPnIdUzyrcSIsT1Adc3nOpXHsUrGT57Bq-EgRBi0VBK2gM_3W4XDK_rnlZo0on0OBK2l0rGaPBdYnrU9fCYVsxXPwR415csb4jg_RW-ppWkjZq8Y-vd309lLUkO15VSGR4VyTqyPbXEzUYNJe2HEyK1ggCHNcyxiuuE95G6f1lm5w7z7Q_IUPhwl7VZuz0KbEBipoR9ceIjDh_3ZAlcuprUHlzzQDy5JYMRj2Btki-bFNy0SYPRxhXSE1XNCnQJSpEkMMjbmrRGho6oJ5JfU4m1JFElJRsfpTnaZYlSTm5NAZi4oREXsI-KMukAmeWgxKOMy0yDTjEzKW5D7xBDssD3w8CsG6Fehdu8oR4kMM-EMEwM5aAidC9kkSr4dTyybmnKwTLk6MeLnxsOLXy9WM4BaDVvn4vH9jQbQvCQYpBNbyfiZKPGp4W7fem698i8w9cbVqehqZMJPq8qYW1jif9ZQsndwS_ofxf7gVl5Ac8SIJJDWpIh2FrfSxEo5WageU1GVvkYsB-QYHAk6A6tb8Bx7LD-BN5k4dMUfB6S1yE8Q02D4EsGCg89EM3yIo4y7V7bGBDTrDDItZD2Sdu5rEUfHqXTabPBP-Y-OFDURzKDg7DuCqyNEsLPb4B7JDjPwSfUTdrdN-RF8BpvGbiukg3CfOjImE3ZyhQHDPmMO3-FsiLAj9GqGcvwKPsBRFwV6YEqhPY_jnm34_sB678cn9PetzLLc3GaXNg0HKwWMkwoU8F5-SgNhuhEziIXvx-AM9hBIsAZTfGipVjjgwmtCHqVCG7CSUA_yTzGQN_XO4GDG_nxaeTewRDUTwHBxHSCd8SgkZZ09P5kZKXLpI-Q7xXcQ6YvBme4H8vFy8UuKAHO4RLRIDmFXmoK23xKCtIqmfDUtGWmPhmZNdgOMCnXysz8bhvZ8QL18JxBwJpaU4tDJ5MsSShd2m8gygfvUTG5969IFmc1na8DPIw99IijnPFJAa26KSbfwdESHk3XuCXYeK7fqpVnoEamlj8QwBAKjxcFkkQZ37hJdPKJ0yQHvsjkD1qhijLMx4WHg-n4PkE9pEzPASycypKYBhL6JcSeyFBES-SFIB_IDNdLETBwKzgYRQnUZrq0OyEA9Li7wFonukTthXEh94jSL-1ZB3J-DQQHgDFpXYoMFEyclZsHDkG7Yaek5RtsIy0sCdum0kVsUrT7JR50AGLtLQ7e_hYAcYB8mD3lqOcxfIv8lQoUIu1PfD4MC7wTlkUbsXDElx1bXkZKKY9CNPHYJF2Qpvj2QDLd-p4J8kEnyk5TeGZdhSWBT8QA2JfYlbtiGrnU6oRuUYC8EgBo25SJBI-Y1vhVDNE-mB4GAaVTg-lElRIZcGiiN3QT7wwC5JUR-gMZNUB434cKEpxQQW2WRZHeeDpyQyclJzsIRCnPUMLSXxF0Q08JiMkiBF7wyAlI1o4rcan22antJBhrM7kx4HQ2FEoHwnn9BmdO7-TKJ3J7teadVjJCLfMigKp0G6mRNHK8N1w3fRCyWXqTLvOGziyRisiNENAo1HWeSkChuI1Khj3Ih2tN7BhR8OVHwbr4lquGqmPXTvstsgYypQyHW9D9AgPYS12SKaG4XrwvgczT4toGSFFmdI1Sr5cg03X3FPYOC0GXMZOh1YXuMgLeZwkoL1d7XkYILUDLnoYtkzdVVmBRoxZ5aXaNzbgZnLSh6DEWI3KQGRk4QY_--L1OjqPnVcdUNmnnG9fcf5WnNpnf_hvGOEAH2qgycja28uXMZL0nxB5CCdJYWf0GtbjjkxWigxNylasg7gFrm-Upj0NClw-OGBCbFSAHHMqFACWV83hqjGfB5KTb3lbUuCYofuyFAn2Ur-quJ-F3I3U2RrAuIML_SBwm4raBkXs5yUIxELzmoF3Myyaj8WsKeVKoRohSM-dL1RckewkeKzD4FvLb9affv7sL1IzlZizpQ_gxNvuum7Jh5K5d9ymoArMAV1T-OBmw-kSDsFZzoY3W0zn32LiTWB4TJe5rsDWxPQqmoNcWDxqtCsKHg27_h3uXB6A8mdFUo9CSZOnhwHMBQea5y54uBnLS98Iwyv43il0xGkIngoneYlblnnsJt5knU6ovMm2_hCAnRIuYZ4nflEmSVroGNiEuTNk8sfC55QoRj17GHiaBSHNiJWUi3vZNqFt6wHGl_FoGckmw2US1-IE2C1-jCoBA_CTyUKZG6ERhDDmLSlSxE84m_oKiYNdXfWcaHsoMCOggy_gnIJdSzH5KxltRkvM0DLCVRsmNTPz_A3VqUiNqIt00PEU4ALNRRmroioH3ZDF0_1pVKK2TD8eYKhq6Ck8DwprfnuY2pGqVFgWww45rhY6T5vvEzkok4M1-u4p_K39ZyHXVXIDuVnkFcE-a3HSc-fTTsIDwPVuB7wiQiTsi6UtegUD0EiLFw53z5SnIrKbFLHRqIhdecUX83deABqxCqIq8ybrZUJYnuDu02BJBanyEx5UfhhxTztvBn7SyN3dAxKp3JU0SAoPHFoW6HiYgZJUJV4PAD5OkV1KE0j_BVSJjHpIs9BIWsGHXCKtNqxHn3mOoaCZJJJBxYHg2QZ4EEc1MsAr9dQURaUsY98jrQlSAIHToPMDu9KPC50tkog0NLu55f1aWcACj4GPzi0XbW3SUrS9BsoK-Ujcr2IKYd6g0i6NFHaOO2OYLBNRQhjlCEJjte9fqBPjyDEgt-gYu_4KliXiUuiDHLe5v_oOqeFIgw6he2V7js-BfZ6-cJ7Bubw_-4p6fpS74uTXe809Dr8m1Ib-_mUNJ9iXzmsGxPmj6gAC0r7uOxIml0giw4lGIJR_-Ng-IA_sRAHESqisIwhjQXKnJjt8X6KJX8rrk-EZwftVV1CQRnG8yC6WX7OCE3RJazgRgZFoySWE5LlYo9ryt2c3m1s9O737jprtUGRITP63eUhwVBJ9mmgRrqOm_QDsdcxyN_NdD_NpSelznmVlmkShPi0TVG0Cik2g9bff873fHz-u8dN6tAvvu-MA6bvQ4o8CCU-rKPSLpIyCCHySys95nsYFKKQkL3IeRn6WF24Y-2mK_Ft6UeJz102ylCdFlZHXe2JLx0Dh6UWUHQGFp1UahHlVWFD4TwQUnqRhwtKKM15ZUPiDQOEvQHJ73qGwF4EUfM8LJqmP4cgKQ5_CYZA5f0MZDKQ-LNbcYs0t1txizS3W3GLNLdbcYs0t1txizS3W3GLNLdbcYs0t1txizS3W3GLNLdbcYs0t1txizS3W3GLNLdbcYs0t1txizS3W3GLNLdbcYs0t1txizS3W3GLNLdb8l4A1PwUyP4Uut7Dy7xVW_hi_iHM49sEvfyCkMw6K6NF_-aMU3DQJBxFPr4VRVfQdWCphRiGP4cLxl375wy2LPOWPtES9HFwljqFlkIZQEdcpz2Zynh4T-I-AvXkSdY3AWEdgcKcctwjTw2Gq_YJ_CmJVmDhqiTS1Bkaen6KdO-oQhKElYh1qNrAJWi6yZYoX14bJBRJM2kmYWjpBVnt3MZ9zsrPUlJNZIMyHlbJGhPtABpsEQp6fIpPFKQnxJ6XzWqgrGoL3EpIooBko3ClkJm0ledh3F1NITJNxZ203ueBEoStMaYOSYYgILedWMG5QbPXIQjX4FSwxceuKBgSed7IzydUimJuJL7xSYT2xtw8r0Yj8JI68Ig887oVekGRBXASM56dKNDS8_wcr0bAy9CcgQ-9fCLT_IwT-yqg98b87XlryvZTTeEnsszD24ijhcVhUPElCN0miNGZJESR-mcVVEVRR4EZplGSwOo6IegZbdOHb_D6bOyisCS687CL0jhTWuMyNcpjUFtb8NAprfAayL2ZZzjz_foU1k7ZUyuZI6vFo2hFTSdILmpIGrzemG7dX_ndFnp4QSCtwlYWLNAkMGXGdwF6S7S-E4-hliNwJQ_EGhjTe8QOsLayN9_xYEtKPZMqJ4PgTjnegpNhxaDDCK5QEnWJ3K4lwlBghNgWRKZMLTp2SV7AjYRKUB3p1pquVO6wV7BMBI9TXQslh6ULa6hxbnWOrc2x1jq3OsdU5tjrHVufY6hxbnWOrc2x1jq3OsdU5tjrHVuf8TKtzvLzMWRaxOPQKW53zC6zOud85EGziks1OAV0X053D2OaaDmKm3yhhgVDXbne1kUFQxEcbmFJl5_YIMCIa6vqDagNwYvisNGM_THpqOzoLyu-3LWWYDIaEIdN7YBiKUFeuuVfCMI-jdBT0hboAqcWDrse7a_mNCUu21VK2WspWS9lqKVst9WOslgLh4qZ-EmS5FgoGsODYsX0gPCA8mWOboifEizIgWUjopaDEo8c_fIL5ORp2lpv7RAFY4Av69vCWBrQX9HWspfXScPYWPNnPxW3tJQ1pRrPV3lT3A7TiZU_g-V-HwbmX_qd_FkGHef9BiXPEM7niLccD2-_758X7ZqHnSi8N7usaNbD4bGYcosRSBicvDy1JPIwgcxSgcmI_zZSy-kGgr9A1IHHgRab6nvBP_-SeR0nsJ_A9xVtUutERBgKBqwetsQfy5PeMGafHIAdmUElV4gEqstd5UilQ8Dty9UdEDC0QcFHlfhYmCdOax4CdaAL-ePCIRv_Ly5VJOqp1mBKPA8bsyCEQ5U-GctM4L-oceUGoY7h_kV2jILZxe6IeTFq9cHHb3WAkfQ3LRdLzJxO16QtZzYODIvIppLzM270XMaO23bFmlpL7RIKoBbKYy6CcjMzLNDOFLgeOVpMKjuoaJZJ2aOizQfGwODYwIxmFfCfab4VnvqaAFSUh32KaikSaQbTOm314yKvXT-G_Ty9fPn_1pz-8fnV-Xb6xBaG2INQWhNqCUFsQagtCbUGoLQi1BaG2INQWhNqCUFsQagtCbUHoj7-YiYUVemTBY1QKTT_SoYM5wLa3a9KjeP6IL5M-iIpmIv4Rza7H_pmleUzpYBmU4t2CiScz_PtVh6B42x2XpYIPKrHsSCGyZgaWHFnTXenEiJhSxfTQcwSDCq8VVn1-6rYWix5vNrdCdMwKBIUVtSYwoDQF0L4AcUQy-BYMZJHTup0Bh4xA3J3VkEdOfE6i--c-rUPF5o9XQOICwfwA6drPM0MfVNOYcT9J3KRgVR6GkR_D6VW88tNTNY26surnXtP4IxYD9y9L3a-p804XDE4lc99LwSD-QFhUuiyqAp-FZVUEeZiGKStAocFnPKzCgkcpq1yWs6DMWOZyL4mTuMySxPfYfTY3Lxj0XmOdoH_hpUcKBsGlrFKY3xYM_jQKBoOiKorYDVjA0h-kYPAII2PY2iFaPKm75A9iGcmWo8pQmfGglrgoOFQ1VUobiay5-ZNhZnLo89ZAAYXZmtIgqOTA9r_ppL4hv1wUfRHOCDNyqlotiA6zpM4TxwtFAT2oHT-Gf_vBaqGcUKGWhTbfL8JXNY0SnUIOjlRxR0GaoBCbBk6EihLZvOhCugNSfyowt74jhcSVJY22DtHWIdo6RFuHaOsQbR2irUO0dYi2DtHWIdo6RFuHaOsQbR2irUO0dYg_0zpEHjA3K-Myd4PI1iHaOkRbh_gD1yEeboDSn5cqJHypL_FS5kdnqxfxFIM0V8oaPIyiiuwqbY0qdFDJwwb_pUPk1p_OX4HJAqtbOZ917160Vec8-91LcSsvXr5SUOlz53O5MGWGo4R2JMprBj_BiLU0dmA9YLLWw8Z0T515xNZ06eloUEGgz9I4n8FwN0zEzY0oum66i4EjDNmS5Yp2dsFA9JRP6P8oDC3_vMEY6Iq4Aelk6IgxlR-1j02elZGsVGnduqp5s9fbDkUavib8e1tgagtMbYGpLTC1Baa2wNQWmNoCU1tgagtMv88CU57xEsySKAxiXb1iANmM-MvHwtHMLJm-bLMkjLDmg_iFBlXgNtkU-FsQ7VqaIhPSUV4iHVrkyobYRl4pzNAc2Wl4vhxAy2qMI0hsjY7GHkHWaJcTBzHE1VG4i1gEDqpgL3A_qCZhVwKUQyrVF8ADP3BETU19rcLiAmYDooHXdDx4GnpKw9ISaBmiD0E_RuCatdxRBanK-1IMI50w0oRAcbB4ZiroUZcFEPqDOHEQtaGaExUJf4LxNtAMw0g7nNUvmOchMz2Eg-h5Q7IYXUQYHDZFBTLTpY0y1UUgc-d1T7_2cQv3eCU5UOyWCj9FKFvo86Fr3vEZImjix7KjYPZeLlNVRCjZMIMKkECYG3LwvtIlJiDYdEql08cw5rgH0AV3snirpMFeXFFkmvY1AeX32gGEQb8s4G19uK0Pt_Xhtj7c1ofb-nBbH27rw219uK0Pt_Xhtj7c1of_GOrDixP14cWJ-vDiVH14L-rDxx9deTgCyC7RNOltXfh-QWjBysgNSHY9SkEoOTSq3AX9MpXRvSb_UnBfzzFxTXkDBQle2H4UVl7pcf-xlthtwaBUuRxRMkZQEFGLpeprKEiic4-IR3680vU_bUleSTGhfxlYL2cq8VKpz0lJDuMUy5EyQhrUKvB2JcJ0R35L9z4l7Z92xY60OmUYKT61FvEpw3xZ70WVKGckCvJMhLIQ_2JTa7QrxD1gAcluHyx3foosjxfAPwcjjsnk3FxtmT_qZ8J42nKKopqe2mwr6wGsVLB9lII9P0WJd_8WMZWZiN1rLbCSiT0kfYwpzsJyUzcC85eFjd9_XqjJP3UEZE9rcIPgSq3UdHOEoyQ3rVn9avHxBVIq84Oq84Oo9MBSzcu0Ah8YHBos1xfRoKPV-bqM-edenW-F8UOE8f17QHzALw5PJfTfSwOBMo6KwA2jKPe8ImexF7EizcCGz6MqzVL8UeHSDarQy0K_4mVVhIXr-TzK4zz3SuZ9-C8Oe69d78JLL8LwSAMBXvKgCIPENhD4aTQQKEI3CsukzFzf_cF-cRhj3UYWVskfEodHMlzS6x8WmwZg7oI082AoN7BxtpiAeidAi0q7N7cr5YkN8xL8_XSbjNUMEwjFMGTMfJuyFopawTJEynDYK4EgCTrXxRJMsRbIz6neDKTYc4mPNOVed6rJgc5Y-olIzUYK18Kuei7uLfSeSNyOxl83vBrxt5oH4X9Txpesxfpqg2VQ8nM1lMCei2QuoVOOpHMJgXO88kBGb-c9HGyjAtuowDYqsI0KbKMC26jANiqwjQpsowLbqMA2KrCNCmyjAtuowDYqsI0KfiGNCpKoKMPAT5Is_1E3KliMmO2VKAlBPyt7lmG6EzlB2-rAtjqwrQ5-9q0OTh7NIdNiLvCSAAHzwxEFFcMUHpekO100EbXJweq6p97y4AOJwCLO4gjYAZVcmOyu0_Cos-oKNkxqTe5fxc3MWhjb1sG2dbBtHWxbB9vWwbZ1sG0dbFsH29bBtnWwbR1sWwfb1sG2dfjFtHVIwKzzWQC-iztBGCcAs8G-HwtDPgYIVOfW9RdTREBlysm1NyhGUxoYqseRh0jfw95P6JmgQ5FPNBh1UsCCoxQq0XQQ9nCJ4oeCWokWooyXKCKb3aGZmZvqjCczveIwJR0NRedg6sD9x9__LXTJzSHh1ZHlYeD1Dcto1xpIQ2VHAx_F6ZR2nZlHeGQGWlH7-5gVHI4cJgk0dM-obo5OCX_Hj1hQmd1rVpaY_OSlsbYXn4JyM8idUmqUkNQ2pAxRiaoJoTPxIETR6j4gYtBJYFVpgcXktzPVe-78GUOt6_x2LXlV244aOUrSU4I35Y8UEj-rCkhdRMzJRKRQntDLmHpfsoyyiFVpnGdg4E9ICA2rNxjnY8Hx6Di7BmBUoUIlcNf3SUWsaIszWbWSNtJM-oRxuvJiX6anlScYJKsw9feDUkgF_-Sdu0ngpkFgeogy-U2Fzp4nNzStMcI1itWFcnViKfuyFH_q62B5cZgcLi_I0qPLA2s5TfwA9Oi0vE-IbBuCGUljuRIAX4rI0fHC0f4WSA7oE2xEUKGHfvK--U0_k6bN9BlG9nYJtnuBVyS8M3k-NZYkYaMZLxNfKB0vPp0QvVVTb7cEstU-7yz6aWApRTkvHKdBGsNGIp4QlTnyg7z3MCU3q2MoYJxphY6KYCOR3pQwFTOhiBOA2JNxOsQnCztBNCeZ1W8P5vbML9dT4JaVX4PDKgJjw_kpcLJyv4WUHLojCHb0g2wrI9vKyLYysq2MbCsj28rItjKyrYxsKyPbysi2MrKtjGwrI9vKyLYyul_3DFlrAqP_9cxHb9XP4Jzhb7QP4QP820N57sHfX51uN1FmiV9G3qO0m3h60CVFoB0RDylYHBVGy_snGhGo60sfr_fPM8nWZnntYfMV2RboGFxxasJjBlQUYPbU6d3Zr0ZsfX2wdZHOXlPEe8JnkjbbbUWCW-nWht3q0qddKwisNI0Yo6vOsV426miOhOKnXJGBETWiovrglLu8B9hcafkttzut7wGNbHyes9AteeCmZcWqOAqzPIqoGcXRRja6ncb32cjmF8CK9-8vtN8cxTObo3jfHe998r10fklc1-dwwEBEjPuhm0ZZXPqcVTmrSj8rvDjN_QJ2FkU55tiCiLm8SDw3yHw3JZq7c3NHOr_46UWUHOn8EgEdex4PbeeXn0bnFz-JoyBNU6Azbju__Ng7vzwVB0sKSqjWqfZAOIYi1ddOpTBTRanZFVAIxwszXqeT0qQX1TkdVO5gflfBEVWm4A1orUsFXH1jOkUGUiLnoiJmKBgBgaTjrQwQ5-WkoBU66r6dbTKBTkk-oLNNYjvb2M42trON7WxjO9vYzja2s43tbGM729jONrazje1sYzvb2M42trON7WxjO9vYzja2s43tbGM729jONrazje1sYzvb2M42trON7WxjO9vYzja2s43tbGM729jONrazje1sYzvb2M42trON7WxjO9vYzja2s43tbPML62xTVq5XBCxIggnEZFT8qGYzD6jbOYFdl3ksuJo3Bohdhc8VTv9SH_EbYfRNJWuyPpfuXP3oesV7MvhpZk5dTlQgQwRHUDtPuRNRmEoml6YSsTgpMyVkfC9XIhhAlpGhXAK14GdI8Yq4Bdu7EzgdBQQ-lUxCQYgsIUWISdbEP0ZATlwu-vPITkp1m7j3SYUCwcH4XrLSWzmg8x49RnqYgiDwOGgwGTymd9bSH94jtmkkwVbTOMhqMAwOp4BoWkPNagMFTmxWjrDesyl00BzTifV7hxISmCPodWDloJgDHjM4HWhfs7IBUgT3YfIuhLAYb_cYdpEjR2FWC86sRShjqtMWdh_4Aqhhp6MSK5HJJCBRauii8mPIpfJ0V3vQ5BmGR6g_25bKtqWybalsWyrblsq2pbJtqWxbKtuWyralsm2pbFsq25bqh2xL9dV3_x__oGcH)
