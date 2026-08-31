[//]: # (ob:ffb9914f)
[//]: # (ob:v18-title)

[//]: # (ob:1b9c9fe5)
# Exact Knowledge Construction v18

[//]: # (ob:c7bae7d0)
[//]: # (ob:v18-status)

[//]: # (ob:0f9993df)
**Status:** Stage A construction continues on the five frozen zero-heavy tasks with no answer executor. Official authority is projected from a controlled source lane and independently screened only for responsiveness. Exact-span period inventory, unbounded BM25 period gap recovery, deterministic numeric inventory, and per-requirement schedule-column validation now have complete terminal telemetry. Repeated runs found five stable period-domain IDs, but period domains proved only year sets; the requested numeric columns and recomputable calculations remained incomplete or unstable. The latest run covered 27/49 slots with 22 explicit gaps, zero invalid bindings, zero Human Approval receipts, and zero executor-ready tasks. The paid executor remains blocked. All constructed objects remain `not_governed` candidates until Human Approval.

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

[//]: # (ob:046661c1)
[//]: # (ob:v18-period-numeric-mechanism)

[//]: # (ob:8d60ca25)
### Period and exact-calculation closure mechanism

[//]: # (ob:64bf4db0)
The current closure mechanism inventories exact multi-year source spans deterministically and permits the model to select only content-addressed candidate IDs. For explicit gap recovery, BM25 scans every matching section; only candidate-bearing sections survive, and lossless chunking keeps every candidate while respecting provider context. Repeated unbounded runs produced five identical period-domain IDs, demonstrating that top-k retrieval had hidden valid year sets. A selected period domain remains `not_governed` and proves only an explicit year set.

[//]: # (ob:6080d1c1)
Numeric construction now routes a selected schedule span to a per-requirement column validator. Every number in the exact span is inventoried, required periods are explicit, and exact excerpts are rebuilt deterministically from verified substrings. This eliminated mechanical binding failures and closed one value-by-period slot in a single run, but the repeat was unstable. The stricter column validator found the complete ordinary-income series and no complete federal-tax, state-tax, total-tax, or second schedule series. The resulting stop signal is substantive: the next mechanism needs requirement-aware table cells and authoritative-source construction, not broader context or looser completeness rules.

[//]: # (ob:885d9df3)
The v12–v18 checkpoint is committed at `results/exact-knowledge-stage-b-v12-v18-sanitized.json`. Across all runs, invalid bindings remained zero, terminal token and cost receipts were complete, Human Approval receipts remained zero, no task became executor-ready, and no answer executor ran.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkwZGEyYjk0M2QyZjQ4NzYwOTUxODU0YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjE1MDlmMGNjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81NjM1NTdlMTNmYThhZjk1ODA0ZjFhMTQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q4N2RkZGU3MDU1ZjQzYjc0ZmYxZjY4MCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfVuP3Na15l8hlDNAkqlq8X5pAzNQZMfHSE7skZRMgNhobXJvdtFikxWSJaltGMjb_IAzOE8zr_PD8jDA_ItZa-0LN-umlrrt2PEGAqdVRe7ruq9vrfr2ERumpmbVdNXwR5ePtturwucsLIs44mEd51nqF0mQJ3H1aPWo7PntFW-uxTjBs-OGhUl6ySO_5nXOc-bzMqryOk4rP8nCLMl56ddZnPE0jUtW1BEvWVQWVZrHVZJlcRoFZc1gXN6MVf9aDLePLr_Ff0xXE7uGGVo24VQr-KMULXzwJzE0dcPKVniDeN2MTd95G3i-H2698tb7Yuj7ejuIcYR3tqx6xa4Fbmrx8dB_LWC7uwEH3EzTdrx8_Pi6mTa78qLqbx5XG9HdNN31xLrrPPIfL94exF93Dfx9tRvFcFX13Sg6OItp2InvVo82guEhBolf1H6FJ4afXInX9BAcrrhK0ihJMhFENctZXSS5H9cBC2JcWT9MuLWrtukErFzfSHvF84xzLjI_Seo4KrO4roM6zX25HbW6q4ptx10LGw5xnVU_8PHR5V--faSm__YR3HI_jPiX_FrwqxKO_C-Pdt2rrn_TPfoK9qDpAS942vFGjI_ZVrxdw4K6aS1es_bxJ39-8vTF1e_-8Pl___0nH3_6ydXTz__w_MWzPz598dnnf7j6U5Bf3PBHq_ciLDZNQ1PuJrjPq5KNzYizi7a-YiOc8yRovN206Qdc_aumwyHH23ESN_BNx27wmvUuVvDqiKTx6LLbtS3sqdrAXQp5GmXbV6_g6bouiyKIa3gcrnESb3HHv_y___E__t__-Y9fwYdqEgbnzumcgd7EG_jkL48ff3Xp_cL7ZV9evg7y9dRMrcA3ptstURsb2KPvVvNMAZB8UYtkMdMnb-FovN_BglvBr4X3FEgJqKjCI_Bg2HMr-IV3h7fVapAAgZgXC6qykomM-w-2oP0jGSc27cZzZ-LXRVFEvH6wJfz6189p0stf_9qr7Pe2GzYKr9-KTnCP1ZMYvC-eJcmF94fe27KGe-LtmXXmWRZwPy-_t6PioiIxdu6wUl-kYVLki0WArOMwpacH8JpuA9IReMWrh_6GNnmWiH7h3XGIM5RUFzxPg_JhV_Y7IbbetBFwMyDaYUrvacuaG-_TgW03Hhvpu4p1fddUrPWuUXPg5Y67cjxzilERVlkQiwdd6wvQPorEYFWDqPsB1t0NDWiRcbmJa1r-G1A0Hi6Re2fWCgISRHwUPeha90nvrztQru8ivRAor_azvYU0Nww0LmgdwYZq4-mR3klvp987Q2SxACrLK3b_NTxlnac0-A1qM_aG4XUhO69fGXZeiI-BNXC3HZvO3VZaFD5jD7DAF0AwNwLVVTPeeJvbbQ8kBOrQg_91bBj6NyC-Jvja-_vf_tcN0pqa0GtutsOZJWYRy5hg4f2XuE9FTfeaDQ3rprPyPomzCnTOUo4u5OY8zjuo6PRbZ2goBfEZ1QG_7_zBhYd3ZBGRt23hOuB-wHbcNkBBXt-1t5Ijkf8nNr7ywEq72c4rbEEkLDVymQVFSFbgvZa3fznbZivQmjx3NSKsg5DvmScga7b9CJvRI7xblRw8f-Y6_LKMw8AvP3zOly9f4mtfdsCazWv7mOEzz1v_F49N_U1THVyV_HZeXtVzsUcqiYjThH342pBCgB9bmpSp6wNiACL54pkH3sp2hNWhCuMNBxcH1ohHBEarx85cVJyKKEnvc2j75KFN9LOsm5VFWpXlUhf9thnGaX-TY9tU7yKUsy-eUwJlXiYsfohVrL2XgwB_A32ZK8bZFmzCx6QErowSQNduGuCji-3tS9C4NV6PV7MzPFxGohZpHTzACg81NWvB763Yu9R1UdZ54NdLOfLf7Le9EfhBdO-8p5MvnbmjMsvDME-KxexgloNOfQIK63-ShQanChTPwLOczi_hF975V88sJMjLNEiz4CEW8mzXaYNTcut65tZy17QcNHIvH6lREIHg_0agG5B535xzLAruRyLJH2KJ64WQq_od_BdWS2bmR192a2vtFGYRfGWs5vUZihaVXxRxzR5ijfq1LXr0o9SRTe0JjPpI4Q1GtDTF4Ju-A5dtN213E_iS5-yaSJRZFAbhkSX-hpZYN29BOHKYp-23dD7irah2Uz_cjfruMMo5PZcUnBd59sDLe0Ju7N6R4o2DBrhuMDrWlxjkAonVt23_hqiz64cbcJfOBSoYrzIR8gde7dKoZfw1A0kyk0AjjVegR7Ch0J0ZUOIQobLrc3rJrxPQTOmR1T6Vq5WcOG0GIdZ6oWgw1w2cxN2u_y4jvduDKYOkKnnOvoelflYbQtUnu4LhhPiGPFL74IE-BiXMRnYjvO2Zw2Uly32fH1vxx3LFu7b1lO21ZZ1o73aep18-x0UszVmYP9BiUKAzeD4I9StPvvjkzySDFFHKKBGe0zdi6NewpNe30is87-HUaZTFD7PIg4jaroKbPWunBQx0iqiXIbXn8j26fDQ8gQJa8S4P6-RL52KKAsOcQtxzdpQVMpxCOxZ8xIAPs8gYMwKkOSgIZ_vqZ86mEnkh8rK45-qe41P4OG_YdQdmt1fKiA_r0FEfZEARmezNBtiZgcHYtDv4Hiz_czcXRnXJk_Seq9unmQqjZmdJphZx6PvFcmIZbCvBiuBsuH2XM77_8BkSYXXtxyKpPnC2L0DNYRwN-ZIL4NCbpsPQWuVpW330lBohLp42bNJUsn8GX610VuQRqBkMpl1VYNbJRAN9o7MW4ipnVcoLEceZ8GvuhyXz87xg-CTcOo2pEjeeStx41UZUr7Z9002UhxpoJsxF6H9hKuIrzPiAJ3BrjWBngaxBKL_0gQmisa-nK3BfrsWwHRqVhxrL4DIOUpGFLMmrAC4m4TwpkzBkIMVqweI0y4uq4mlUpgWrw6xIWZSLKvFTnxdhUERouWKcn_JJ8rYu4_A7OGhM3oR-mK79fB35L8LwMs4u4_g_-_6ljytSJ44GJmdJHMQBkMn86bf_mBQUUalMEYH82SBbxmXs56wGrxM5hMawskaKgO-cDlKjRkkShGmFaQWhR7UyRGrUD03x6EmyIE4icAajhOtJrKzPiaWfTtuoYf00zaKChX4RF3pYK5Ojhr1PKkZZPqQfySMoBQhSlKggZ2UIhUaRYbj6pHdtXHZU62sZF7K9JDCSpGjodjdgcFbgiDQcPVwKG8G3MtvYTLez8wSfLuUOuH7Na5oUvjoSzVmR8GZmDhLI3jU8c-E9AWPAHA4GDZXBDstjTWdN6oE317Tev-5uWOc92aKEY-3F6Tsq_TryeV4GeW3uyMpinbj6c2koNXBR8iINRQ4yIdMDW5kpTbj3SSupmSqeJ2Xk13lWh4bx5kyTmuk-aSLltMLtvMJRRnCM2vUo0LlpxqrtR1TaeojdgCIbKYrt2tnlgW0BMYB4UcT4OkhpRPT8BzHCoyOMxsHvmryvd7DCGiPt25ZVWovJjBCNhNqHtJuJTHkl0tG0ocHBUQLqhCEa5JwlV92AVcSmanOpKFoasuhRI8uoKCiQYAkCduVt0b3iFoE3goi3rXatJmXchfS-cYibUapSID9GJ4cKlU76ht3S7lD_AtGeIcq6DAOR53ValYG-USsfp270Psm0_SSO4qcL7zO4uR5ep4WSjocDHAWsmctRVvh_3aRPHsaihArjcLBIviu8oWk3dPYp4eX3s5C42ONPxcZy0WSNbBkulc5RvvQNrIn3b_AiBbuBF9oGvbczh1gEASjoOC0FNwxoJQpPcPa5LJ8aOCtEVmcsy2rysSRnz4k_m7PfK4Gnho9ZkvhgDyRRZfSoldPThuA9cnMLJ85TvpKJyknf2nLlJIcg8QCVe28EeyU6JCqjA5R9ZWsBZaEStyBbaeoAUoKLB20w_tfTB1wFYDRkSZjmkZHJVtLQkP99kn9k-FKgGMjx73_7395vtGsySyzQo6j4KOamBAOdmB0-HOFQWg669zUyCsjwFu6BU3arFVKNAylrYbNQmytpifctnN_1-ogGPa1A5aHiUregvpsJtOT2wntmhKFaVd2A2mTL9bbA2MBqExCe19ceq6rdDXEp3Gjbg5PWIsG2MAzFqyqwg0EunL4sFlaF4DyvCnLm6bKs9OkJNjufBlVDJ1Higz0JzkPs66GtzOjMaO-V49TioQ6LGqzpmKVmcCvtqQa_TwJTRpUVvykFgeuBi9qVIKVHDCvDLbFufEPKhnzXpgV6g5uoGKLPPORqIMyyAZcB9waDjBdfduGF9wnRpdRU67Z5Jbyx3w1AW-NWLhAOAtYLNAVrVI635j74oxWVpCTQpu0OT8e7BSmlPGj5pdaDMGEENhhoMAw3An3JzzFNx3CvMqWmtBzobq9sMJ7eo-6Ff_b8dg1UicpdmXaS_JEy8RR30h08Rt7INBZnNNpohS3ComKwha0R0aEFUTvAcYNdAvd0q3QTXgOFc0GNSC5tMLYLa9oJ782mIXwkQvzwFNCjXoEZCVyFQUUyZ6pbkANwcNOtNgnkbcF80miDxST6SuZ9eESJuDc8kJHi9BIPeuQ8lHrW4UZanKQ-4PJBKOU6oGAly2fXipUkCFosClpJY_ivw-WS-XUjeIMqnUCDK2V3rVSMBtclr09fi4BtpXDxR4x7ecXmjizSW5lrWinaaOQ_vt4NzcgbRXairpHI8K5I1JHtbyZqMWiubDmYFK0RBDiuVYxXXie8jdL7yy678J4af0KFwqW9aszY-VNiAxQ1E-qPCRlx-bolS9TUN6DylpoB5MktGYxmAmORfNnl5KLNHo40rpCarmlSoEtUiCCHJ9zUWWto7IF6ZvU5m1BHElFKsoVJWeZFkWV8dmksxMQJiXwO-6AtkxqcWQFKOC2MyLTgEAuX5i7wBjWsiMIwisC6lepduskz4kENe08Ew8JYAiZC90oRrYFTqyeXnq4ULI-PerjwseXUqteP4RSAVofmrXpgQ7ctCQcpBtXwfiZKPWp5WrTfN_3wCpl_FHrT6jQMZSLRl20jrXU86S87OLkj-A3t_4og4kkYiSiLZjVoIB2WrfWhEI1OaQZWNmRskYsB-wUFAk-C6jT-BhzLDuNP5E0eMkUlmi1xEcY32DIEcsZAEXEY-1FRpUVp3GMLG3KCHc5iPbR94hcBy8Gn99ls-szwj5kf3hfFoe3gOE7rqsiLvDLjW8AONf598BlNu0b3HXkBnMYbJq-LdJM0P2oSdkuGAsWxYA7b7u-AvCjwY4V69gI82l6QAXdtSqA6ge1fYP79yH7gyq_292TGvdrSbII2BwatAIuVDBP6VHJOCWqzlTpBgOjF70fwHCawCFB2Y6xYO-bIYFIbok6VsptQAvBPMp8x8CfUbsDw9j77eHaPYCiK5-AgUjrhW1LQaGt6Pj9S8spFMmeI9yrPAZM342P879XZCwUuGMAOEQoRYHhFHerKWDzaClLq2bJUjCUmv5nYDRgO8OnX2kw87ttZ8cK1dNyBQDqa0wiDx3MsSepdGu8gykcvkfG5dy9IFqe1neBRGZdBXqVpqZnEwhaddPPfARHS3k0QhTzOQj_MjcqzUEMzi78PAEiHh3mVRWkRVkE2r3zGBJmxPwDZo2dIirIQcRWIeA6ez2AfNcN9IDunogSWsYR-KbEXEhTxIkkB-Acy0-WZKBiYFSJO0izJcxOanXFARvzdA80zf8K2kvjQewTpt1asoxifBsIDoLjUDgUmSkbBqo2nxqDd0HOKsi2WURb2zG0LqSJXaZudKg86YpGWcWcPH6vAOEAe7F8JlLNY_kWeCgVqsbYHHh-nM7zDq8qvRczBVTeWl4Vi2oMwfQgWaSe1OZ4NsHyvj3eWTPCZltMUnukmaVmIAzEg9yVnNY6ocT6VGlFrJACPEjD6JmUi4VO2lU41Q6QPhodhUOX0UCpBh1TOWBSpH4dZEBdRlpsInYWsOmDcDwNFaS6owTYr0qSMAjOZhZNSk90H4rRnaCGJryi6gcdkhQQxYm8ZpGRES6fV-nTb7rQWsozVhfw4EBo7CuUj4Zw-owvvtwqlM9v9RrOOKxXhVllRIBXazZwoWlm-G66bXuBCpc6M67yBI2uNIkIzBDQaZZ3PRcBQvCYVE0FiovUWNuxouPL9YF3CyFUr9bHrxt0WGUObUrbjbYke6SGs5Q7J1LBcDzEMYOYZEa0ipChT-lbLlxuw6do7Chuvw4DL1JvQ6hkuCmKRZhlob994HhZI7YCL7oct03fFa9CIKauD3PjGFtxMTXoflBhrUBnIjCzc4KdfvFgnF6n3vAcq-1iI7XMhXslT-_T3_4YRDvChRpqMrL29fBkjSf8RkYd0kjR2xqxhPe3IZKXI0Kxs5TqIW-D6JmXa06DA5aMHJsRGB8gxp0IBYHXVAq4a83kgOcVWdJwCxwzdl3OR4CAP61qERSz8RJ-tBYw7uND3ArfpqG1UpWHJQSBWhtcsvJtl0XwoZk0rVwrVSEF64X2h44pkJ8FjPQbfOvFm_fHnT_-sNBPHnC19ACfe9TdNRz6Uyr3jNiVVYA7ohsIHbzaCLuEQnOVtRLvFdP4tJt4khsd2mZsabE1Mr6I5KKTFo0e7puDRuBte487VAWh_Vib1KJQ0e3oYwDzjQIvSBw-3YCUPrTC8hu-dQkechuDpcFKQ-ZyXqZ8Fs3U6o_Jm2_p9AHZauMRlmYUVz7K8MjGwGXNnyeQPhc9pUYx69jDwtAhC2hErJRf3sm1S2zYjjK_i0SqSTYbLLK7lCbBb_BhVAgbgZ5OFMjdSI0hhLDpSpIif8DbNNRIHu74eBNH2WGFGwARfwDkFu5Zi8tcq2oyWmKVlpKs2zmpm4flbqlOTGlEX6aDjKcAzNJcUrE7qEnRDkc73Z1CJxjL9cIChrqGn8DworOXtYWpHqVJpWYw75LhG6jxjvs_koE0O1pq7p_C38Z-lXNfJDeRmmVcE-6zDSS-8j3sFDwDXuxvxigiRsC-WtugVjEAjHV443D3TnorMblLExqAidvxanM3fBRFoxDpK6iKYrZcZYXmCu0-DJTWkKsxEVIdxIgLjvFn4SSt3dwdIpHZX8iirAnBoWWTiYRZKUpd43QP4OEd2KU2g_BdQJSrqocxCK2kFHwqFtNqwAX3mJYaCZlJIBh0Hgmdb4EEc1coAr_RTcxSVsozDgLQmSQEETovOD-zKPC51tkwi0tDsza0Y1toClngMfHRpuRhrk5Zi7DVQVshH8n41U0jzBpU2t1LYJe6MYbJMRglhlCMIjdW-f6FPTCDHgNyiY-yHa1iWjEuhD3Lc5v7qO6SGIw06pO5V7Tk-B_Z58pn3FM7l7aOvqOcH31Unv95r7nH4NaE2zPfPGjjBgXsvGBDnj6oDCEj7ZuhJmFwhiYwnGoFQ_uFD-4DcsxMFECuhso4gjCXJnZrs8H2FJn6mrk-FZyTv131FQRrN8TK7yL9mlSDoktFwMgKj0JLnEJIXco16y98-erO5NbPTu6-p2Q5FhuTkf12GBCct0eeJzsJ19LTvgb1OWekXoR9gPi3joRBFwfMsic1p2aBqG1BsA62__YHv_e74cYOfNqNdBt8dB0i_Cy3-IJDwvE7isMp4EiXgk9RhKco8rUAhZWVVijgJi7Ly4zTMc-RfHiRZKHw_K3KRVXVBXu-JLR0DheeXSXEEFJ7XeRSXdeVA4T8RUHiWxxnLa8FE7UDh9wKFfwaSOwgOhb0MpOB7QTRLfQxH1hj6lA6DyvlbymAk9eGw5g5r7rDmDmvusOYOa-6w5g5r7rDmDmvusOYOa-6w5g5r7rDmDmvusOYOa-6w5g5r7rDmDmvusOYOa-6w5g5r7rDmDmvusOYOa-6w5g5r7rDmDmvusOYOa-6w5j8HrPkpkPkpdLmDlf-gsPKH-EWcw7EPfvkDIZ1pVCUP_ssfXHLTLBxkPL2RRlU19GCpxAWFPMZLLzz3yx8-r8pcPNASzXJwlTiGkUEGQkVcpz2b2Xl6SOA_AvaWSdQ1AmM9icGdc9wyTA-HqfcL_imIVWni6CXS1AYYeXGKdt5RhyANLRnr0LOBTdAJmS3TvLi2TC6QYMpOwtTSCbLau4vlnLOdpaeczQJpPqy0NSLdBzLYFBDy4hSZnJ2SEH9KOq-luqIhxKAgiRKagcKdQmbKVlKH_e5iCoVpsu6s62cXnCh0hSltUDIMEaF8aQXjBuVWjyzUgF_BEpO3rmlA4nlnO5NcLYK52fjCax3Wk3t7vxKNJMzSJKjKKBBBHERZEaVVxER5qkTDwPv_YSUaTob-BGTo3QuB9n-EIFxZtSfhd8dLS36QcpogS0MWp0GaZCKNq1pkWexnWZKnLKuiLORFWldRnUR-kidZAasTiKhnsEUfvi3vsrmDwproMigu4-BIYY3P_KSESV1hzU-jsCZkIPtSVpQsCO9WWDNrS61sjqQej6YdMZWkvKA5afBiY7txe-V_1-TpSYG0AldZukizwFAR1xnspdj-UjqOQYHInTiWb2BI47U4wNrC2sQgjiUhw0SlnAiOP-N4R0qKHYcGI7xCS9A5drdSCEeFEWJzEJkyueDUaXkFO5ImAT_Qqwtdrd1ho2AfSxihuRZKDisX0lXnuOocV53jqnNcdY6rznHVOa46x1XnuOocV53jqnNcdY6rznHVOa4655-0OicoecmKhKVxULnqnJ9hdc7dzoFgE1dscQroutjuHMY213QQC_1GCQuEuva7640KgiI-2sKUajt3QIAR0VA_HFQbgBMjFqUZ-2HSU9sxWVBxt21pw2S0JAyZ3iPDUIS-csO9CoZ5HKWjoS_UBUgvHnQ93l0n3tiwZFct5aqlXLWUq5Zy1VI_xmopEC5-HmZRURqhYAELjh3be8ID4pM5tjl6QryoApKVgl5KSjx6_ONHmJ-jYRe5uY80gAW-oG8Pb2lEe8Fcx1pZL61gr8CT_Vze1l7SkGa0W-3NdT9AK0HxGJ7_ZRxdBPl_-pUMOiz7DyqcI57JtegEHth-378g3TcLA195aXBfN6iB5WcL4xAlljY4BT-0JPEwosLTgMqZ_QxTquoHib5C14DEQZDY6nvGP_2Lf5FkaZjB9xRv0elGTxoIBK4ejcYeyZPfM2a8AYMcmEElVYkHqMne5EmVQMHvyNWfEDF0hoCrugyLOMuY0TwW7MQQ8IeDRwz6X12uStJRrcOceBwxZkcOgSx_spSbwXlR58hLQh3D_cvsGgWxrduT9WDK6oWL2-5GK-lrWS6Knj-aqc1cyGoZHJSRTynlVd7urYwZdd2OtYuU3EcKRC2RxUIF5VRkXqWZKXQ5CrSadHDU1CiRtENDn42ah-WxgRnJKOQ7034nPfM1BawoCfkK01Qk0iyi9V7uw0Oev3gC_31y9eyT53_8_YvnFzf8pSsIdQWhriDUFYS6glBXEOoKQl1BqCsIdQWhriDUFYS6glBXEOoKQn_8xUwsrtEjix6iUmj-kQ4TzAG2vV2THsXzR3yZ8kF0NBPxj2h2PfTPLC1jSgfLoBTvFkw8leHfrzoExdvthCoVvFeJZU8KkbULsOTE2v7aJEbklDqmh54jGFR4rbDqi1O3dbbo8c3mVoqORYGgtKLWBAZUpgDaFyCOSAbfgoEsc1q3C-CQFYh7ZzXkkRNfkuj-uc_r0LH54xWQuEAwP0C6DsvM0HvVNBYizDI_q1hdxnESpnB6tajD_FRNo6ms-mevafwRi4G7l6Xu19QFpwsG55K5H6RgEH8gLOE-S-ooZDGvq6iM8zhnFSg0-EzEdVyJJGe1z0oW8YIVvgiyNEt5kWVhwO6yuWXBYPAC6wTDyyA_UjAILmWdw_yuYPCnUTAYVXVVpX7EIpb_QwoGjzAyhq09osWTukv9IJaVbDmqDLUZD2pJyIJDXVOltZHMmts_GWYnhz7vLBRQXKwpDYJKDmz_N73SN-SXy6IvwhlhRk5Xq0XJYZbUe-wFsSygB7UTpvDvMFqdKSfUqGWpzfeL8HVNo0KnkIOjVNxRkCYoxLaFE6GiRLYsulDugNKfGsxt7kgjcVVJo6tDdHWIrg7R1SG6OkRXh-jqEF0doqtDdHWIrg7R1SG6OkRXh-jqEF0d4j9pHaKImF_wlJd-lLg6RFeH6OoQ_8F1iIcboPTnlQ4JX5lLvFL50cXqZTzFIs2VtgYPo6gyu0pbowodVPKwwX_tEbn1x4vnYLLA6lbep_3rz7q6957-9pm8lc-ePddQ6Qvvc7UwbYajhPYUymsBP8GItTJ2YD1gsjbjxnZPvWXE1nbp6WhQQaDP0nqfwnBvmIybW1F003QXA0cYsiXLFe3sioHo4Y_p_ygMrf58gzHQFXED0snYE2NqP2ofm7woI1np0rp13Yh2r7cdijR8Tfr3rsDUFZi6AlNXYOoKTF2BqSswdQWmrsDUFZj-kAWmohAczJIkjlJTvWIB2az4y4fC0ewsmblsuySMsOaj_IUGXeA22xT4WxDdWpkiM9JRXSIdWuKrhthWXiku0BzZGXi-GsDIaowjKGyNicYeQdYYlxMHscTVUbiLXAQOqmEvcD-oJmFXEpRDKjWUwIMw8mRNTXOjw-ISZgOiQTR0PHgaZkrL0pJoGaIPST9W4Jp1wtMFqdr70gyjnDDShEBxsHhmK-jJlAUQ-oM4cZS1oYYTNQl_hPE20AzjRDtc1C_Y56EyPYSDGERLshhdRBgcNkUFMvOlTSrVRSBz78VAv_ZxC_d4rThQ7pYKP2UoW-rzsW9fiwUiaOZH3lMwey-XqSsitGxYQAVIICwNOXhf6xIbEGw7pcrpYxhz3APogjtZvdLSYC-uKDNN-5qA8nvdCMJgOC_gXX24qw939eGuPtzVh7v6cFcf7urDXX24qw939eGuPtzVh_8Y6sOrE_Xh1Yn68OpUffgg68OnH115OALIrtA0GVxd-H5BaMV44kckux6kIJQcGl3ugn6ZzujekH8puW8QmLimvIGGBJ_ZfhLXAQ9E-FBL7LdgUOpcjiwZIyiIrMXS9TUUJDG5R8QjP1zp-h-3JK-UmDC_DGyWM5d46dTnrCTHaY7lKBmhDGodeLuWYbojv6V7l5L2j_tqR1qdMowUn1rL-JRlvqz3okqUM5IFeTZCWYp_uak12hXyHrCAZLcPlrs4RZbHC-A_ASOOqeTcUm3ZP-pnw3g6PkdRbU9tsZX1CFYq2D5awV6cosR3_xYxlZnI3RstsFKJPSR9jCkuwnJzNwL7l4Wt338-U5N_6gjInjbgBsmVRqmZ5ghHSW5es_7V4uMLpFTme1XnRwkPwFIteV6DDwwODZbry2jQ0ep8U8b8z16d74TxfYTx3XtAvMcvDs8l9D9IAwGeJlXkx0lSBkFVsjRIWJUXYMOXSZ0XOf6oMPejOg6KOKwFr6u48oNQJGValgFnwfv_4nDwwg8ug_wyjo80EBBcRFUcZa6BwE-jgUAV-0nMM174of8P-8VhjHVbWVgtf0gcHslwKa9_PNs0AHMXpJlHS7mBjbPFBNRrCVrU2r29XWlPbFyW4O-n21SsZpxBKJYhY-fbtLVQNRqWIVOG414JBEnQpS5WYIq1RH7O9WYgxT5R-Ehb7vWnmhyYjGWYydRsonEt7HoQ8t7i4LHC7Rj8dSvqCX-reZT-N2V8yVpsrjdYBqU-10NJ7LlM5hI65Ug6lxA4xysPVPR22cPBNSpwjQpcowLXqMA1KnCNClyjAteowDUqcI0KXKMC16jANSpwjQpcowLXqOBn0qggSyoeR2GWFeWPulHB2YjZXomSFPSLsmcVpjuRE3StDlyrA9fq4J--1cHJozlkWswFXhEgYHk4sqBinMPjinTniyaitjlYX_fcWx58IBlYxFk8CTugkgub3U0aHnVWU8OGSa2p_eu4mV0L49o6uLYOrq2Da-vg2jq4tg6urYNr6-DaOri2Dq6tg2vr4No6uLYOP5u2DhmYdSGLwHfxZwjjDGC22PdDYcjHAIH63Prhco4I6Ew5ufYWxRhKA0P1OPIQ6Xvc-wk9G3Qo84kWo84KWHKURiXaDsIeLlH-UFCn0EKU8ZJFZIs7tDNzc53xbKbXAqako6HoHEwd-X__27_HPrk5JLx6sjwsvL5lGe06C2mo7WjgozSf064L8wiPzEIrGn8fs4LjkcMkgYbuGdXN0Snh7_gRC2qze804x-Sn4NbaPvsYlJtF7pRSo4SksSFViEpWTUidiQchi1b3ARGjSQLrSgssJr9dqN4L708Yal2Xt2vFq8Z2NMhRkp4KvKl-pJD4WVdAmiJiQSYihfKkXsbU-znLqEhYnadlAQb-jIQwsHqLcT4UHI-Os28BRjUqVAF3w5BUxIq2uJBVK2UjLaRPnOarIA1Velp7glG2ivNwPyiFVPAvwYWfRX4eRbaHqJLfVOgcBGpD8xoTXKNcXaxWJ5eyL0vxp74OlpfG2eHyoiI_ujywlvMsjECPzsv7iMi2JZiRMpZrCfCliBwdLxztb4DkgD7BRgQVeugn75vf9DNpxkxfYGRvz8F2L_GKpHemzqfBkiRsNBMU8gut4-WnM6K3bpvtlkC2xuddRD8tLKUs54XjtEhj3CjEE6IyJ3GQ9x7n5GZ9DAWMM63QUZFsJNObCqZiJxRxAhB7Kk6H-GRpJ8jmJIv67dHenv3leg7cMv41OKwyMDZenAIna_dbSsmxP4JgRz_ItTJyrYxcKyPXysi1MnKtjFwrI9fKyLUycq2MXCsj18rItTJyrYxcK6O7dc9QtSYw-l8eheithgWcM_yN9iF8gH8HKM8D-Pur0-0meJGFPAkepN3Ek4MuKRLtiHhIyeKoMDoxPDaIQFNf-nC9f54qtrbLaw-br6i2QMfginMTHjugogGzp07vnf1q5NbXB1uX6ew1RbxnfCZps91WJri1bm3ZrSl92nWSwLhtxFhddY71stFHcyQUP-eKLIyoFRU1B6fd5T3A5srIb7XdeX33aGQTipLFPheRn_Oa1WkSF2WSUDOKo41sTDuNH7KRzc-AFe_eX2i_OUpgN0cJvjve--QH6fyS-X4o4ICBiJgIYz9PipSHgtUlq3lYVEGal2EFO0uSEnNsUcJ8UWWBHxWhnxPNvXNzRzq_hPllkh3p_JIAHQeBiF3nl59G55cwS5Moz3OgM-E6v_zYO788kQdLCkqq1rn2QDqGMtXXzaUwc0Wp3RVQCsdLO15nktKkF_U5HVTuYH5XwxF1puAlaK0rDVx9aTtFFlKiFLIiZqwYAYGU460NEO_ZrKA1OuqunW0KiU7J3qOzTeY627jONq6zjets4zrbuM42rrON62zjOtu4zjaus43rbOM627jONq6zjets4zrbuM42rrON62zjOtu4zjaus43rbOM627jONq6zjets4zrbuM42rrON62zjOtu4zjaus43rbOM627jONq6zjets4zrbuM42rrON62zzM-tsw2s_qCIWZdEMYrIqfnSzmXvU7ZzArqs8FlzNSwvErsPnGqd_ZY74pTT65pI1VZ9Ld65_dL0WAxn8NLOgLic6kCGDI6id59yJLEwlk8tQiVyckpkKMr6XK5EMoMrIUC6BWggLpHhN3JLt_RmcjgICn8pmoSBFlpQixCRr4h8rICcvF_15ZCetum3c-6xCgeBg_CBbma0c0PmAHiM9TEEQeBw0mAoe0ztr5Q_vEds8kmSreRxkNRgGh9NANKOhFrWBEie2KEdY79kUJmiO6cTmrUcJCcwRDCawclDMAY9ZnA60b1jZAimC-zB7F1JYTLd7DHuWIydpVkvObGQoY67TlnYf-AKoYeejkitRySQgUWroovNjyKXqdFd70OQFhkeqP9eWyrWlcm2pXFsq15bKtaVybalcWyrXlsq1pXJtqVxbKteWyrWlcm2p7tQL51RvGz9O0zQgC-7evW0OKlYoWrFWaIu1IfhfnVlPzlO_YtShZ17PFzLsYVLzazvBppNQMPy5xaGxe9dx5DKPC0C9UDBr6pgTkOdhF2rjHg7WtEjfSEl5A7Zns8b8hDeeOdjUz32-f9EPsd6TmSby7gmWq3O2WMPAd62qgARNf44Q8oQXvI6-l_N9HYR__9u_A43KXOq2b7pJlYxKEAym0V6qrgeP7aLth2uH9kyAGztudMMzU1yo734773XGvModLmAdC2zMxSnmPt4F7QmXHs32vRhDV59enOLc45N93Fe7G9l5wjYFdt1eih11gjTI0EsGE-F4H7XjvPiOqRFEbZuXVpWGzs7qTOsCloZnPIJ5iK1KTnDV8Zl_33SvlKuqSWsGKFrEp9yJye7Phr7BeHGKK47PZ9xjXSEMrEaVKhR1gP9VoJ4oOD6ADBkkhOZEVzqrR56OwbwfoawMMWuKXRmSXUv_YA4c2SR890Z0SRolSSbAdGY5q4sk9-M6YFRHebQRnenu9UM2onPK1ylfp3y_F-V7976U-z0Ck9MNEOcWgD9MA8QgiZJAhJHw48DPihpeZ2Eq_KSsRV4kFRdBCP-Ji5AHRZEHBY9j5ieCsyIIRXaXzR00QAwv4_QySI80QAwSv6j9qnINEH8aDRDLmkVh5Cd5MLc7umsDRBvtAozedDsx3q8boqlHnOORzajDb7pl2gKNrUIxBDWViZGjHf1kFxcKb9hp8wt5J2uSagY0LeX07cqyLn_zb2GiH8DQnTYz95v4aJPQGkSX3y1gaUqcrqu-3d10tgWJ8pf6DR2C9k0JIWWHLPiXBJHU0tikOIxS4Aqg9tnHo4R_LCEABpuLhyPVkMCSjSX01fgPtNTxMHRmo9Jn0EXTmQ3Aseu-gouGlxjQPYdJW5SMqCqK_SoR9fEJgI88_ZN9Cx-iOeHp5o-uV6HrVeh6Fbpeha5XoetV6HoVul6Frleh61XoehW6XoWuV6HrVeh6Fbpeha5XoetV6HoVul6Frleh61XoehW6XoWuV6HrVeh6Fbpeha5XoetV6HoVul6Frleh61XoehW6XoWuV6HrVeh6Fbpeha5XoetV6HoVul6Frleh61XoehX-zHoV1iGvEr_K0jKboSlzBegpKM171HGaoHucxnHOizg1MAyrtNMKuj9ETaY2x6usiLPcrznVYUnsx1ymaVkVH1pfOaPCTtl_W_xsOm4CkuR5hx144f2WLnUOHVpVQlQ_NFY4uwnQVhupYVRrODmHIV-d_ht1Ulc1ApPkC7sfW5Kxm11HSV6sh9CDz-vS1uS4xWFkHh9DJYOGIFulRHO1E9lpxoEmZpbchInCI6VFHJyhjuJSUvxiFKPfrl9Z3s0GPNWNhI5KDjf1RqjtjbO74HsDP9ursVHIC9P5x4Yf62HP-X5VxasoT2t_RnlZNbaK2O5THMsOCr6WdV4Yn7FBszqirxCMh6jZ1aylVB2Ix6w49coK5mlghgp4YX5qOkLxJNRhCdKakmFFjPwpiQcyjfrekR-qI-gmU2D8OgmpovwCqtbXe36JgnjjWcFrrRXQkYYCWdEYkl2Wh-FSqolodHlqygJRHRF0cRksiQ23ayo4EzqEqMK-5rFacAySryf2dqV0MP059ZP-FGP4srxkvlAaTCs8hKgSS84NHfCerLC-tIAoZDALpo4a0h2WSKjqOaHNjBPBWrs3GXpM5dAzi4Fx2YSWH5bpcuqtd9aRy2NR1WFQlnPycK7ctkTuh5dc82uxJujLulzDKGuqSNVpkouvx757CdwvkzsYlJBlDgfJFWMcSdt3roc87qJo50OHrc8b1GZYoBaJrhIVop6XMUOTR3g_k9t1GHYdhl2HYddh2HUYdh2GXYdh12HYdRh2HYZdh2HXYdh1GP7-Owx_9d3_BxomQOc)
