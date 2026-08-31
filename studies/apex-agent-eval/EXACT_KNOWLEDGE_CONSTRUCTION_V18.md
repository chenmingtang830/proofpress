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

[//]: # (ob:d4dffb5f)
[//]: # (ob:v24-freeze-decision)

[//]: # (ob:4c1f3364)
## v24 freeze and transfer decision

[//]: # (ob:58858d00)
[//]: # (ob:v24-freeze-evidence)
The v19–v24 construction sequence added deterministic row- and column-oriented table-series extraction, exact label/period/value cell coordinates, formula-template selection without model-proposed values, and deterministic same-period recomputation. In the v23/v24 repeat, 48/49 slot states were stable and 92 candidate objects were shared. The ordinary-income, federal-tax, state-tax, and total-tax schedules each remained complete across five periods; total tax retained five recomputable derivations. Invalid bindings and new invariant failures were zero. All objects remained `not_governed_candidate`; Human Approval receipts and executor runs remained zero.

[//]: # (ob:71aa454d)
[//]: # (ob:v24-freeze-interpretation)
This is the mechanism freeze point, not a task-quality result. The five tax tasks are now development-only, and neither the v23 single-run 30/49 nor the v24 29/49 candidate coverage may be used as a generalization claim. Further optimization against those tasks would make the product question less identifiable. The next phase is the preregistered held-out and cross-domain ablation in `EXACT_KNOWLEDGE_TRANSFER_VALIDATION_V25.md`.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkwZGEyYjk0M2QyZjQ4NzYwOTUxODU0YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjFiYjhmMDNhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mMTYzNTkzMTQwZjQ2Yzc0ZGNkZjhhMjQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q4N2RkZGU3MDU1ZjQzYjc0ZmYxZjY4MCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfVmPHMe15l9J0HcA21PVzH1pATOgqeUS9rU0JO0xYAnNyMzI7hSrM8uZVWy2BQF-mx9wB_dp5nV-mB8GmH8x55xYMrI2NtktWrIOIFBkLZGxnDjrd7767pEYNm0jqs1FWz86f7ReXxR-LcKyiKM6bOI8S_0iCfIkrh4tHpV9fXtRt5dy3MBnxysRJul5UOZ-mIsqK0QWVUkVJH4e10kl6yQKqrTJgrCOwzRI87xKZR4naZE0QQ0fFlEUByGMW7dj1b-Rw-2j8-_wH5uLjbiEJ6zEBh-1gL-UcgUv_FEObdOKciW9Qb5px7bvvCv4fD_ceuWt99XQ9816kOMI31mL6rW4lLio2ctD_62E5W4HHPBqs1mP548fX7abq215VvXXj6sr2V233eVGdJd55D-efXuQf9m28PeL7SiHi6rvRtnBXmyGrfx-8ehKCtzEoCzzxo_EI_XKhXxDH4LNlRdNkEZJEQWx38RplcV1VTe5CGOcWT9scGkXq7aTMHNzIquLOs_qupaZnyRNHJVZ3DRBk-a-Wo6e3UUl1uN2BQsOcZ5VP9Tjo_M_f_dIP_67R3DK_TDi39Tbsr4oYcv__Gjbve76m-7RN7AGIw94wJtt3crxsVjLt0uYULdZyjdi9fizPz15-vLit7__8r__7rNPv_js4umXv3_x8vkfnr589uXvL_4Y5GfX9aPFewmW2GyGttxu4DwvSjG2Iz5drpoLMcI-bySNt91c9QPO_nXb4ZDj7biR1_BOJ67xmM0qFvDVEUXj0Xm3Xa1gTdUVnKVUu1Gu-uo1fLppyqII4gY-Dse4kW9xxb_8v__xP_7f__mPX8GL-iEC9r2mfQZ5kzfwyp8fP_7m3PuF98u-PH8T5MtNu1lJ_Mbmdk3SJgbx6PvF9KSgLKqikcnsSZ-9ha3xfgsTXsn6UnpPQZRAiircAg-GPTWDX3h3-LaeDQogCPNsQlVWCpnV_oNNaHdLxo3YbMdTe-I3RVFEdfNgU_j1r1_QQ89__Wuvcr-3vhKj9Pq17GTtiWYjB--r50ly5v2-99airT359sQ88ywLaj8vf7CtqmVFauzUZqW-TMOkyGeTAF1XwyM9M4DXdlegHeGueM3QX9MiTwrRL7w7DnFCkpqizlMwAA86s99KufY2VxJOBlQ7PNJ7uhLttffFINZXnhjpvUp0fddWYuVdouXAwx235XhiF6MirLIglg8615dgfbSIwawG2fQDzLsbWrAi43wRlzT9GzA0Hk6x9k7MFRQkqPgoetC57oreX7ZgXN8leiFIXuNnOxNprwVYXLA6UgzVlWdGeqe8Hf_eCSGLJUhZXon7z-Gp6Dxtwa_RmokbgceF13n52l7nmfoYRAtn24nNqdNKi8IX4gEm-BIE5lqiuWrHa-_qdt2DCIE59OC_TgxDfwPqawNve3__2_-6RlnTD_Ta6_VwYorgbGVCivD-U9yVorZ7I4ZWdJuT-j6JswpszlyPzvTmNM47pOj4t07IUArqMwKv877PD848PCNHiLz1Co4Dzgd8x3ULEuT13epW3Ui8_xsxvvbAS7teTzNcgUqYW-QyC4owiO87vd3DWbdrid7kqaORYQMe-o57Arpm3Y-wGDPCu03J3udPHIdflnEY-OWHP_PVq1f4ta87uJrtG3eb4TXPW_4XT2z667baOyr17jS9qq_ljqgkMk4T8eFzQwmB-7iihwp9fCAMICRfPfcgWlmPMDs0YXVbQ4gDc8QtAqfVEycOKk5llKT32bRd8TAu-smrm5VFWpXl3BZ93g7jZneR46qt3iUoJ794ygiUeZmI-CFmsfReDRLiDYxlLkQt1uATPiYjcGGNAIZ2mwFeOlvfvgKL2-DxeI04cYfLSDYybYIHmOG-pRYriHsr8S5zXZRNHkBkOZvDf3O_7Y1wH2T3znM6-qUTZ1RmeRjmSTF7OrjlYFOfgMH6n-Shwa6CxAuILDenp_AL7_RXT0wkyMs0SLPgISbyfNsZh1Pd1uV0W8ttu6rBIvfqIw0qIlD8f5UYBmTeX08FFkXtRzLJH2KKy5mSq_ot_AmzJTfzk6-7pTN3SrPIemG95uUJiZaVXxRxIx5ijuZra4zoR2Uj28aTmPVRyhucaOWKwTt9ByHbdrPebiCWPOXXRLLMojAID0zxNzTFpn0LyrGG56z6Ne2PfCur7aYf7iZ9dxjllJ1Lirou8uyBp_eEwtidLcUTBwtw2WJ2rC8xyQUaq1-t-huSzq4friFcOpWoEHWVybB-4NnOnVpRvxGgSSYRaJXzCvIIPhSGMwNqHBJUcXnKLvlNApYpPTDbp2q26iZurgYpl2ai6DA3LezE3Y7_LiO9O4Ipg6Qq61z8AFN91lhBNTu7gOGk_CtFpO7Gg3wMWpmN4lp66xObK0qR-359aMafqhlvVytP-15r0cnV3fbz-JdP3SKR5iLMH2gyqNAFfD4IzVeefPXZn0gHaaFUWSLcp7_KoV_ClN7cqqjwdITTpFEWP8wk9zJq2wpO9qSfFgiwKbKZp9ReqO_R4aPjCRKwku-KsI5-6VROUWKaU8p7Ph11hUqn0IplPWLCRzhijBUBshyUhHNj9RN7U8m8kHlZ3HN2L_BT-PG6FZcduN1eqTI-osNAfVAJRbxkN1dwnQU4jO1qC--D53_q5MKoKeskvefsdmWmwqzZSZFpZBz6fjF_sEq2leBF1GK4fVcwvvvhEyIimsaPZVJ94NO-AjOHeTS8l7WEG3rddphaqzzjq4-eNiN0izdXYmOkZHcPvlmYqsgjMDOYTLuowK1ThQZ6x1Qt5EUuqrQuZBxn0m9qPyyFn-eFwE_CqdOYunDj6cKNV13J6vW6b7sN1aEGehLWIsy_sBTxDVZ8IBK4dUZwq0DOIFRf-sAC0dg3mwsIXy7lsB5aXYcay-A8DlKZhSLJqwAOJqnrpEzCUIAWa6SI0ywvqqpOozItRBNmRSqiXFaJn_p1EQZFhJ4r5vmpnqRO6zwOv4eNxuJN6Ifp0s-Xkf8yDM_j7DyO_7Pvn_s4I73j6GDWIomDOAAxmV797h9TgiIpVSUi0D9XeC3jMvZz0UDUiTeExnCqRlqA71wO0qNGSRKEaYVlBWlGdSpEetQPLfGYh2RBnEQQDEZJbR7iVH2OTP142UYP66dpFhUi9Iu4MMM6lRw97H1KMdrzIftIEUEpQZGiRgU9q1IoNIpKwzVHo2sbsqNZX6q8kBslgZOkVEO3vQaHs4JApK0xwqW0Ebyrqo3t5nYKnuDVud6B0K99Qw-Ftw5kcxakvIV9Bilk7xI-c-Y9AWfAbg4mDbXDDtMTbec81INorl15_7q9Fp33ZI0aTqzOjp9R6TeRX-dlkDf2jJwq1pGjP1WG0gMXZV2kocxBJ2RmYKcyZQT3PmUl_aSqzpMy8ps8a0J78aZKk37SfcpEOmiF03mNo4wQGK2Wo8Tgph2rVT-i0TZDbAdU2ShRYruaQh5YFggDqBctjG-ClEbEyH-QI3x0hNFqiLs23rdbmGGDmfb1SlTGiqmKEI2E1oesm81MeSXK0eaKBodACaQThmjx5sxv1TV4RWJTXZ1riVaOLEbUeGV0FhREsAQFu_DWGF7VjoC3koR3VW1XRpRxFSr6xiGuR2VKQfwE7RwaVNrpa3FLq0P7C0J7QiibMgxknjdpVQbmRJ16nD7R-xTTdos4-j6dec_g5Hr4Ok2UbDxs4ChhzrUaZYH_6zZm52EsKqiIGjYWxXeBJ7TZDp27S3j4_aQkznbup77GatLkjawFTpX2UX3przCnur_Bg5TiGr6wajF6O7GJRRCAgY7TUtb2AjqFwiM3-1SVTw-cFTJrMpFlDcVY6mZPhT_3Zr9XAU8PH4sk8cEfSKLK2lGnpmccwXvU5mZBnKdjJZuVU7G1E8qpG4LCA1Lu3UjxWnYoVNYGaP_KtQLaQ6XbgtfKSAeIEhw8WIPxvx7f4CoApyFLwjSPrE52ioZW_O9T_CPHlxLFII5__9v_9n5jQpNJY4EdRcNHOTetGGjH3PThCJuyqsH2vsGLAjp8BedQU3VrJZUZB1E2ymZmNhfKE-9XsH-XywMW9LgBVZuKU12D-W43YCXXZ95zqwz1rJoWzKaYz3cFFxuu2gYEz-sbT1TV9ppuKZzoqocgbYUCu4JhKF9VgR8MeuH4YYmwKmRd51VBwTwdllM-PXLNTpdB9dBJlPjgT0LwEPtmaKcyOl2096pxGvXQhEUD3nQsUju4U_bUg9-ngKmyyvq-aQOB84GD2pagpUdMK8MpiW68IWNDsWu7AnmDk6gEos88vNUgmGULIQOuDQYZz77uwjPvM5JLZamWq_a19MZ-O4BsjWs1QdgImC_IFMxRB97m9sFfVrJSkgTWdLXF3fFuQUvpCFq9aewgPDACHwwsGKYbQb7U61imE7hWVVLTVg5st1e2mE_v0fbCP_v6dglSicZdu3ZK_FEycRe3Khw8JN54aZyb0RqnFZYIk4rBF3ZGxIAWVO0A2w1-CZzTrbZNeAyUzgUzom5pi7ldmNNWejdXLeEjEeKHu4AR9QLcSLhVmFQkd6a6BT0AG7e5NS6BOi14nnLaYDKJOZJpHR5JIq4NN2SkPL3Cgx7YD22eTbqRJqekD275ILVxHVCxkuezXcmFEgiaLCpaJWP4r_3pkvt1LesWTTqBBhfa71roHA3OSx2fORYJy0rh4A849-qI7Rk5orewx7TQstGqf3y7HdqxbrXYyaZBIcOzIlVHvr990AqT5tqXg4eiN4IAx6XO8arjhG-j9v66y868pzae0Klw5a9aN3Z6la4BqpoN2o8NXsT51x1doh99DSZvbhlAn9ySw2gfYD2Sr7ucQrQpwlHOFUrTJT0U5BINIujhDS7qpDc09iA9k_mcXKgDhSit2cKkLPOiyLJ6CmkcxMQRjXwK-2A8kwaCWQlGOC2synTgELOQ5i7wBj2sjMIwisC7VeZdhckT4kEPe08Ew8xZgkuE4ZUWWgun1p-cR7pKsTw-GOHCy05Qq79-CKcAsjq0b_UHrui0leCgxKAZ3q1E6Y86kRat96YfXuPlH6VZtN4NK5ko9OWqVd467vTXHezcAfyGiX9lENVJGMkoiyYzaCEdjq_1oRCNTlsGUbbkbFGIAesFAwKfBNNp4w3Yli3mnyia3L8UlWzXdIswvyHmKZATDoqMw9iPiiotShseO9iQI9fhJNbD-Cd-EYgcYnpfTK7PBP-Y7sP7ojiMHxzHaVMVeZFXdnwH2KHHvw8-o10tMXzHuwBB47VQx0W2SbkfDSm7-YUCwzG7HK7f34F4UeLHSfXsJHiMv6AS7saVQHMCyz_D-vuB9cCRX-yuyY57saanSVocOLQSPFZyTOhVdXNKMJsrZRMkqF58f4TIYQMeAepuzBWbwBwvmLKGaFOV7iaUAPyT3GdM_Em9GnC8vWefTuERDEX5HBxEaSf8llI0xpue9o-MvA6R7B7iuap9wOLN-Bj_vDh5oHALBvBDpEYE2LuiN3VhPR7jBWnz7Hgq1hNT72zENTgO8Oq3xk08HNs5-cKlCtxBQDp6plUGj6dckrK7NN5elo--RM7nzrmgWBy3drKOyrgM8ipNS3NJHGzR0TD_HRAhE90EUVjHWeiHuTV5DmpouuLvAwAy6eG6yqK0CKsgm2Y-YYLs2B-A7DFPSIqykHEVyHhKnk9gH_2E-0B2jmUJHGcJ41K6XihQdBdJC8A_8DKdn8iCgVsh4yTNkjy3qdkJB2TV3z3QPNMrYq2ED6NH0H5LfXX0xaeBcAMoL7VFhYmaUYrqytNj0Groc1qynSujPezpts20ipql63bqOuiITVo2nN3_WAXOAd7B_rVEPYvtXxSpUKIWe3vg4-PmxN2pq8pvZFxDqG49LwfFtANh-hAs0lZZc9wbuPK92d5JM8FrRk9TeqbbKM9C7qkBtS71VBuI2uBTmxE9RwLwaAVjTlIVEr4QaxVUC0T6YHoYBtVBD5USTErlhEeR-nGYBXERZbnN0DnIqr2L-2GgKHMLGvDNijQpo8A-zMFJ6YfdB-K042ihiC8ou4Hb5KQEMWPvOKTkRKug1Xl1vdoaK-Q4qzP9sac0tpTKR8E5vkdn3ucapTP5_dayjgud4dZVURAVWs1UKFo4sRvOm75QS106s6HzFWzZyhoidEPAolHV-VQGDNVrUgkZJDZb72DDDqYr3w_WJa1edUof227crvFiGFfKDbwd1aMihKVaIbkaTughhwHcPKuidYYUdUq_MvrlGny61R2VjddhwmXT29TqiVsUxDLNMrDevo08HJDa3i26H7bMnFXdgEVMRRPkNjZ24Gb6ofdBiYkWjYGqyMIJfvHVy2VylnovepCyT6Vcv5Dytdq1L373b5jhgBhqpIeRt7dTLxOk6T8h8VBBksHO2DksN1tyWSkzNBlbNQ-6LXB8G-3a06Bwy0cPXIgrkyDHmgolgPVRSzhqrOeB5pRr2dWUOBYYvpzKBAd52DQyLGLpJ2ZvHWDc3oG-F7jNZG2jKg3LGhRiZe-ag3dzPJoPxawZ40qpGqVIz7yvTF6R_CT4WI_Jt07eLD_98umftGWqsWZLL8COd_1121EMpWvvuEwlFVgDuqb0wc2VpEPYB2d5V3K1xnL-LRbeFIbHDZnbBnxNLK-iOyiVx2NGu6Tk0bgd3uDK9QaYeFYV9SiVNEV6mMA8EUDL0ocItxBlHTppeAPfO4aOOA7BM-mkIPPrukz9LJi80wmVN_nW7wOwM8olLsssrOosyyubA5swd45O_lD4nFHFaGf3E0-zJKSbsdJ6cafapqxtO8L4Oh-tM9nkuEzqWu2AuMWX0SRgAn5yWahyoyyCUsayI0OK-Anvqr1E4RCXl4Mk2R4rrAjY5AsEp-DXUk7-Umeb0RNzrIwK1cbJzMwif8d0GlEj6SIbdLgEeELmkkI0SVOCbSjS6fwsKtF6ph8OMDQ99JSeB4M1Pz0s7WhTqjyLcYs3rlU2z7rvkzgYl0Os7NlT-tvGz0qvm-IG3mZVVwT_rMOHnnmf9hoeAKF3N-IRESJhVy2tMSoYQUY6PHA4e2EiFVXdpIyNRUVs60t5sn4XRGARmyhpimDyXiaE5ZHbfRwsaSBVYSajJowTGdjgzcFPOrW7O0AiTbiSR1kVQEArIpsPc1CSpsXrHsDHKbNLZQIdv4Ap0VkP7RY6RSt4UWqk1ZUYMGaeYyjoSRrJYPJA8NkV3EEc1akAL8ynpiwqVRmHAWVNiQIonBUGP7Aq-3Fls1URkYYWN7dyWBoPWOEx8KNzz8V6mzQV66-BscJ7pM7XXArl3qDRrp0SdokrE1gsU1lCGOUAQmOxG1-YHZN4Y0Bv0Tb2wyVMS-WlMAY57HN_8z1KwwGCDmV7NT3Hl3B9njzznsK-vH30DXF-1Nvq6Ns75B77bxNqw77_vIUdHGrvpQDh_FExgIC2b4eelMkFish4hAiE6g8fygNyTyYKEFZCZR1AGCuRO_aw_e9rNPFzfXw6PaPuftNXlKQxN15VF-tvRSUJumQtnMrAaLTkKYTkmZqjWfJ3j26ubu3T6btviGyHMkPq4X-ZpwQ3RqNPDzoJ1zGPfQ_sdSpKvwj9AOtpWR1KWRR1niWx3S0XVO0Cil2g9Xcf-dzvjh-3-Gk72nnw_WGA9LvQ4g8CCc-bJA6rrE6iBGKSJixlmacVGKSsrEoZJ2FRVn6chnmO97cOkiyUvp8VucyqpqCo98iSDoHC8_OkOAAKz5s8isumYlD4TwQUnuVxJvJGCtkwKPxeoPBnoLmDYF_Zq0QKfi-IJq2P6cgGU58qYNA1f8cYjGQ-GGvOWHPGmjPWnLHmjDVnrDljzRlrzlhzxpoz1pyx5ow1Z6w5Y80Za85Yc8aaM9acseaMNWesOWPNGWvOWHPGmjPWnLHmjDVnrDljzRlrzlhzxpoz1pyx5j8HrPkxkPkxdDnDyj8qrPwhfhFnf-y9X_5ASGcaVcmD__JHrW7TpBxUPr1VTlU19OCpxAWlPMZzLzz1yx9-XZW5fKAp2ungLHEMq4MshIpunYlspuDpIYH_CNibF1GXCIz1FAZ3qnGrND1splkvxKegVpWLY6ZIj7bAyLNjsvOOPgTlaKlch3ka-ASdVNUycxeXjssFGkz7SVhaOiJWO2cxf-bkZ5lHTm6Bch8WxhtR4QM5bBoIeXZMTE4-khB_WjsvlbmiIeSgIYkKmoHKnVJm2lfSm_3uZgqNaXLOrOunEJwkdIElbTAyAhGh9dwLxgWqpR6YqAW_giemTt3IgMLzTn4mhVoEc3PxhZcmrafW9n4tGkmYpUlQlVEggziIsiJKq0jI8liLhoX3_8NaNFiH_gR06N0bgXZ_hCBcOL0n4feHW0s-SjtNkKWhiNMgTTKZxlUjsyz2syzJU5FVURbWRdpUUZNEfpInWQGzk4ioF7BEH94t77K4vcaa6DwozuPgQGONL_ykhIdyY81Po7EmFKD7UlGUIgjv1lgzWUtjbA6UHg-WHbGUpKOgqWjw8soN43ba_y4p0lMKaQGhsgqRJoWhM64T2Etf-3MVOAYFInfiWH0DUxpv5B7WFuYmB3moCBkmuuREcPwJxztSUewwNBjhFUaDTrm7hUY4aoyQmJLIVMmFoM7oK1iRcgnqPbs6s9UmHLYG9rGCEdpjoeKwDiG5O4e7c7g7h7tzuDuHu3O4O4e7c7g7h7tzuDuHu3O4O4e7c7g7h7tz_km7c4KyLkWRiDQOKu7O-Rl259xtHwg2cSFmu4ChixvOYW5zSRsxs29UsECoa7-9vNJJUMRHO5hS4-cOCDAiGeqHvW4DCGLkrDVjN016bDm2CirvtizjmIyOhiHXexSYijBHbm-vhmEeRukY6AuxAJnJg63Hs-vkjQtL5m4p7pbibinuluJuqR9jtxQoFz8Ps6gorVJwgAWHtu094QHx0RrblD2hu6gTkpWGXipJPLj94ydYn6NhZ7W5TwyABd6gd_dPaUR_wR7HUnsvKyleQyT7pTqtnaIhPdGl2pv6fkBWguIxfP6XcXQW5P_pVyrpMOcf1DhH3JNL2UncsF3evyDddQsDX0dpcF7XaIHVazPnEDWWcThlve9J4mZEhWcAldP1s5dSdz8o9BWGBqQOgsQ13xP-6V_8syRLwwzep3yLKTd6ykEgcPVoLfZIkfyOM-MNmOTACiqZStxAI_a2TqoVCr5Hof4GEUMnBLhqyrCIs0xYy-PATqwAfzh4xKL_9eHqIh31OkyFxxFzdhQQqPYnx7hZnBcxR54T6hjOX1XXKIntnJ7qB9NeLxzcejs6RV_Hc9Hy_MkkbfZAFvPkoMp8Ki2v63ZvVc6o67ZiNSvJfaJB1ApZLHVSTmfmdZmZUpejRK_JJEdtjxJpO3T0xWjusNo2cCMFpXwn2e9UZL6khBUVIV9jmYpUmiO03qtdeMiLl0_gzycXzz978YffvXxxdl2_4oZQbgjlhlBuCOWGUG4I5YZQbgjlhlBuCOWGUG4I5YZQbgjlhtAffzOTiBuMyKKH6BSafqTDJnPg2t4uyY7i_iO-TMcgJpuJ-Ed0ux76Z5bmOaW9aVCJdw0unq7w73YdguHttlK3Ct6rxbIngyhWM7DkRqz6S1sYUY80OT2MHMGhwmOFWZ8dO62TTY83V7dKdcwaBJUXtSQwoHYF0L8AdUQ6-BYcZFXTup0Bh5xE3Du7IQ_s-FxEd_d9mofJzR_ugMQJgvsB2nWYV4beq6exkGGW-VklmjKOkzCF3WtkE-bHehptZ9U_e0_jj1gN3L0tdbenLjjeMDi1zH2UhkH8gbCk9kXSRKGI66aKyjiPc1GBQYPXZNzElUxy0fiiFFFdiMKXQZZmaV1kWRiIuyxu3jAYvMQ-wfA8yA80DEJI2eTwfG4Y_Gk0DEZVU1WpH4lI5P-QhsEDFxnT1h7J4lHbpX8Qyym2HDSGxo0HsyRVw6HpqTLWSFXN3Z8Mc4tDX3YOCigullQGQSMHvv9Nr-0NxeWq6YtwRliRM91qUbJfJfUee0GsGujB7IQp_DuMFifaCQ1qWVnz3SZ809Oo0SkU4GgTdxCkCQZxtYIdoaZEMW-60OGAtp8GzG3PyCBxdUsj9yFyHyL3IXIfIvchch8i9yFyHyL3IXIfIvchch8i9yFyHyL3IXIf4j9pH6KMhF_UaV36UcJ9iNyHyH2I_-A-xP0FUPnzwqSEL-whXuj66Gz2Kp_iiObCeIP7WVRVXaWlUYcOGnlY4L_2iNz6w9kLcFlgdgvvi_7Ns67pvaefP1en8uz5CwOVPvO-1BMzbjhqaE-jvGbwE8xYa2cH5gMuazteueGpN8_YuiE9bQ0aCIxZVt4XMNyNUHlzJ4tuSXcxcYQpW_Jc0c-uBKie-jH9j9LQ-q83mANd0G1AORl7upgmjtrFJs_aSBamtW7ZtHK1w22HKg2_puJ7bjDlBlNuMOUGU24w5QZTbjDlBlNuMOUG04_ZYCoLWYNbksRRartXHCCbk3_5UDiaWyWzh-22hBHWfFS_0GAa3CafAn8LoltqV2RCOupDpE1LfE2I7dSV4gLdka2F5-sBrK7GPILG1ths7AFkjQ05cRBHXR2Eu6hJ4KAG9gLng2YSVqVAOWRSQwU8CCNP9dS01yYtrmA2oBpkS9uDu2Ef6XhaCi1D8qHkx0lci056piHVRF_mwuggjCwhSBxMXrgGemPbAgj9QTdxVL2h9iYaEf4E821gGcYNrXDWv-Duh670EA5ikCvSxRgiwuCwKGqQmQ5to0tdBDL3Xg70ax-3cI6X-gaq1VLjp0plK3s-9qs3coYImu5j3VMye6eWaToijG6YQQVIIcwdOfi-sSUuINgNSnXQJzDnuAPQhXCyem20wU5eUVWadi0B1fe6EZTBcFrBc38494dzfzj3h3N_OPeHc38494dzfzj3h3N_OPeHc3_4j6E_vDrSH14d6Q-vjvWHD6o_fPOjaw9HANkFuiYD94XvNoRWok78iHTXgzSEUkBj2l0wLjMV3WuKL9XtGyQWrqluYCDBJ5afxE1QBzJ8qCn2a3AoTS1HtYwRFET1Ypn-GkqS2Noj4pEfrnX9D2vSV1pN2F8GttOZWrxM6XMykuNmyuVoHaEdapN4u1RpugO_pXuXlvZP-2pLVp0qjJSfWqr8lOO-LHeySlQzUg15LkJZqX-1qCX6FeocsIFkuwuWOzsmlocb4D8DJ07o4tzcbLk_6ufCeLp6yqK6kdpsKcsRvFTwfYyBPTsmie_-LWJqM1Grt1ZgoQt7KPqYU5yl5SY2AveXhZ3ffz7Rk39sC8iftuAGdSutUbPkCAdFbpqz-dXiwxOkUuZ7dedHSR2Ap1rWeQMxMAQ02K6vskEHu_NtG_M_e3c-K-P7KOO7c0C8xy8OTy30H4VAoE6TKvLjJCmDoCpFGiSiygvw4cukyYscf1S49qMmDoo4bGTdVHHlB6FMyrQsg1oE7_-Lw8FLPzgP8vM4PkAgIGsZVXGUMYHAT4NAoIr9JK6zuvBD_x_2i8OY63aqsEb_kDo8UOHSUf94kjQAaxdkmUfHuIGPs8YC1BsFWjTWfXW7MJHYOG_B3y236VzNOIFQHEfGrbcZb6FqDSxDlQzHnRYI0qBzW6zBFEuF_Jz6zUCLfabxka7e64-RHNiKZZip0mxicC3icpDq3OLgscbtWPz1SjYb_K3mUcXfVPElb7G9vMI2KP26GUphz1Uxl9ApB8q5hMA53Hmgs7dzDgcmKmCiAiYqYKICJipgogImKmCiAiYqYKICJipgogImKmCiAiYqYKKCnwlRQZZUdRyFWVaUP2qigpMZs50WJaXoZ23POk13pCbIVAdMdcBUB__0VAdHt2b_0mIt8IIAAfPNUQ0V45Qe16I7HTQJtXuDzXFP3PIQA6nEIj7FU7ADarlwr7stw6PNahtYMJk1vX6TN3N7YZjWgWkdmNaBaR2Y1oFpHZjWgWkdmNaBaR2Y1oFpHZjWgWkdfja0Dhm4daGIIHbxJwjjBGB2ru-HwpAPAQLNvvXD-ZQRMJVyCu0dibGSBo7qYeQhyve48xN6LuhQ1ROdizoZYHWjDCrRDRB2cInqh4I6jRaiipdqIpudoVuZm_qMJze9kfBI2hrKzsGjI__vf_v32Kcwh5RXT56Hg9d3PKNt5yANjR8N9yjNp7LrzD3CLXPQijbex6rgeGAzSaFheEZ9c7RL-Dt-dAWN270UdY3FT1k7c3v2KRg3R9yppEYFSetD6hSV6ppQNhM3QjWt7gIiRlsENp0W2Ex-OzO9Z94fMdW6LG-X-q5a39EiR0l7avCm_pFCus-mA9I2EUtyESmVp-wylt5PeUZFIpo8LQtw8CckhIXVOxfnQ8HxGDj7DmDUoEI1cDcMyUQsaIkzXbXQPtJM-8RpvgjSUJenTSQYZYs4D3eTUigF_xKc-Vnk51HkRoi6-E2NzkGgFzTNMcE5qtnFenZqKru6FH_qa296aZztTy8q8oPTA285z8II7Og0vU9IbFcEM9LOcqMAvpSRo-2Frf0NiBzIJ_iIYEL34-Rd95t-Js266TOM7O0p2O45HpGKzvT-tNiShEQzQaHeMDZevToheptVu14TyNbGvLPsp4OlVO28sJ2OaIxXGvGEqMyN3Kt7j1NxszmEAsYnLTBQUddIlTc1TMUtKOIDQO3pPB3ik5WfoMhJZv3bo7s8983llLgV9bcQsKrE2Hh2DJxswm-lJcf-AIId4yCmMmIqI6YyYiojpjJiKiOmMmIqI6YyYiojpjJiKiOmMmIqI6Yyuht7hu41gdH__CjEaDUsYJ_h7-gfwgv49wD1eQB__-Y43URdZGGdBA9CN_FkjyVFoR0RD6muOBqMTg6PLSLQ9pc-HPfPU32t3fbaffIVTQt0CK44kfC4CRUDmD22e-_kq1FLX-4tXZWzl5TxnvCZZM22a1XgNrZ1JW5t69O2UwJWu06Mw6pziMvGbM2BVPxUK3Iwok5W1G6cCZd3AJsLq7_1cqf53YPIJpSliP1aRn5eN6JJk7gok4TIKA4S2Vg6jY9JZPMzuIp35xfaJUcJXHKU4PvD3Ccfhfkl8_1QwgaDEAkZxn6eFGkdStGUoqnDogrSvAwrWFmSlFhjixLhyyoL_KgI_Zxk7p2LO8D8EubnSXaA-SUBOQ4CGTPzy0-D-SXM0iTK8xzkTDLzy4-d-eWJ2lgyUMq0Tr0HKjBUpb5uaoWZOkpdVkClHM_dfJ0tSpNdNPu017mD9V0DRzSVgldgtS4McPWVGxQ5SIlSqo6YsRIEBNKBt3FAvOeTgTboqLsy2xQKnZK9B7NNxsw2zGzDzDbMbMPMNsxsw8w2zGzDzDbMbMPMNsxsw8w2zGzDzDbMbMPMNsxsw8w2zGzDzDbMbMPMNsxsw8w2zGzDzDbMbMPMNsxsw8w2zGzDzDbMbMPMNsxsw8w2zGzDzDbMbMPMNsxsw8w2zGzzM2O2qRs_qCIRZdEEYnI6fgzZzD36do5g13UdC47mlQNiN-lzg9O_sFv8Sjl9U8ua7s-lMzc_ut7IgRx-erIklhOTyFDJEbTOU-1ENaaSy2WlRE1O60wNGd-plagLoNvIUC-BWQgLlHgj3Ora-xM4HRUEfiqblIJSWUqL0CVZ0v1xEnLqcDGex-tkTLeLe59MKAgcjB9kC7uUPTkfMGKkD1MSBD4OFkwnj-k7Sx0P7wjbNJK6VtM4eNVgGBzOANGshZr1Biqc2KwdYbnjU9ikOZYT27ceFSSwRjDYxMpeMwd8zLnpIPv2KjsgRQgfpuhCKYvN7c6FPXkjN8qtVjezVamMqU9b-X0QC6CFnbZKzUQXk0BEidDF1MfwlurdXexAk2cYHmX-mJaKaamYloppqZiWimmpmJaKaamYloppqZiWimmpmJaKaamYlupOXDjHuG38OE3TgDy4e3Pb7HWsULZiqdEWSyvwvzoxn7xO_UoQQ880n69U2sOW5pdugc0UoWD4U5NDZ_eu46hpHlaAZqLg1jRxTUCeh52oi3vYm9OsfKM05TX4nu0S6xPeeGJjUz_3692Dfoj5Hq00UXRPsFxTs8Uehnq70h2QYOlPCUKe1EXdRD_I_r4Jwr__7d9BRlUtdd233Ua3jCoQDJbRXmnWg8du0_bD0aE9lxDGjleG8Mw2F5qzX09rnTCvaoUzWMcMG3N27HIfZkF7UquIZv1eF8N0n54du7mHH_ZpX22vFfOE6wpsu50SO9oE5ZBhlAwuwmEetcN38R2PRhC16146XRqmOmsqrTNYGu7xCO4hUpUcuVWHn_y7tnutQ1UjWhNA0RE-HU5sXH42jA3Gs2O34vDzbHhsOoThqlGnCmUd4L8KzBMlxwfQIYOC0BxhpXM48kwO5v0EZWGF2UjsworsUsUHU-LIFeG7E9ElaZQkmQTXWeSiKZLcj5tAUB_lQSI6y-71MYno2Piy8WXj-4MY37vzUu5yBCbHCRAnCsCPQ4AYJFESyDCSfhz4WdHA10WYSj8pG5kXSVXLIIQ_4iKsg6LIg6KOY-EnshZFEMrsLovbI0AMz-P0PEgPECAGiV80flUxAeJPgwCxbEQURn6SBxPd0V0JEF20C1z0ttvK8X5siLYfccpHtqNJvxnKtBkaW6diCGqqCiMHGf0UiwulN9yy-Zk6kyVpNQuaVnr6duF4l7_5tzAxH8DUnXEzd0l8jEvoDGLa72awNK1Ol1W_2l53rgeJ-pf4hvZB-7aFkKpDDvxLgUga5WxSHkYbcA1Qe_bpqOAfcwiAxebi5igzJLFlYw59tfEDTXXcT525qPQJdNF2dgGw7YZXcEZ4iQndU5i0WcuI7qLY7RLRLx8B-KjdP8pb-BDkhMfJH5mrkLkKmauQuQqZq5C5CpmrkLkKmauQuQqZq5C5CpmrkLkKmauQuQqZq5C5CpmrkLkKmauQuQqZq5C5CpmrkLkKmauQuQqZq5C5CpmrkLkKmauQuQqZq5C5CpmrkLkKmauQuQqZq5C5CpmrkLkKmauQuQqZq_BnxlXYhHWV-FWWltkETZk6QI9Bad6jj9Mm3eM0jvO6iFMLw3BaO52k-0P0ZBp3vMqKOMv9pqY-LIX9mNo0Ha_iQ_srJ1TYMf9vja9tDruApHne4QeeeZ_ToU6pQ6dLiPqHxgqfbhO01ZWyMJoaTj3Diq8p_42mqKuJwJT4wurHFenYq21HRV7shzCDT_My3uS4xmFUHR9TJYOBIDutRFO3E_lpNoCmy6xuExYKD7QW1RAMdZSXUuoXsxj9evnaiW6uIFK9UtBRdcNtvxFaexvszu69hZ_t9Nho5IVl_nHhx2bYU7FfVdVVlKeNP6G8nB5bLWz3aY4Vew1f8z4vzM-4oFmT0dcIxn3U7GKyUroPxBNOnnrhJPMMMEMnvLA-tTkg8aTUYQrKm1JpRcz8aY0HOo147ygONRl0WymwcZ2CVFF9AU3rm524REO8ca_gaysnoaMcBfKiMSU7bw_DqVQbktH5rmkPRDMimOYymJIYbpfUcCZNClGnfe3HGlljkny5EW8X2gbTXzf9xryKOXzVXjIdKA1mDB5CVOlKToQOeE5OWl95QJQymBRTR4R0-y0SuntOGjfjSLLW5SbDiKkceuFcYJw2oeWHebmcuPVOBnJ5LKsmDMpyKh5OnduOyv3wluv6Ui4J-rIslzDKkjpSTZnk7Nux717B7VfFHUxKqDaHveKKdY6U7zv1Qx4OUUzwYdLWpx1qOyxIi0JXyQpRz_Ocoa0jvJ_LzQzDzDDMDMPMMMwMw8wwzAzDzDDMDMPMMMwMw8wwzAzDPwqG4S_h-jx5Rt0Hh4iGd9_e4Rvef3tOO_xc0Q57L390vMOg7duhJ2VygSIy_hD0w3VcN02ZzBkQ9-7w3SgJw3ipnOqTfDfmyXEVNFGUxrMnwxjGMSeIAQTuYyMn5sjTDITeHb5-gnIwyfMkr33_wWZ0ZHfMlfvV153K3BSYuYHnzCzDKE9sXhYIESdx_UNPleKLNTaVUIcBTlgxZsyUz90Ycx1RO0pVi_W7aRWGVkBRmp4dE587jjbbE33-Z8cE4PCYzw000YIlyGosMcLaBcfPDnOGfHwn2a1zuu-Yh5NaWWpeib21Lh2sj8PAeogO9vMpJt5bmGN5l84yndiZYjC7M8fXD4FsS0YQlelWDQMeG4RI9VJ1XdS6tdPAYfRK3o83tgnSKCmiIPabOK2yuK7qBgLLo7yxlhTx3byxrDVZa_4QWvPuzMe7bKDx94f5PT8Ku2lZRLGsRV5CNBenMFeBzWZhUVdJFhdJnAZNVZRxHICsVJGQSVnAQYR1I9K6qOv8yHr2CE2j8zA8Dw8SmpZl3viRYEJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZUJTJjRlQlMmNGVCUyY0ZULTnxWhqaMfyjiSoZ82xcR-4rDGHZLauxHBGZuXR2WdBUGZVDZ16XDDTeL7YeRu5u5VQR0FlSzDYrKsE9_b6VXclbBNQbI9Iv7auRBDf7PUkTamZJaYleom2kWddNGoH63F8J6sRClXj1U66LHqciYmw6pXeRvCKSBUcLsSS4RDrcjgmJ7wqZMFRXdpwaym12iPEJFca5N-mkH24bIpQ_omjB7j4lX6aeHF-U4BU-UPdO0Fn1CEB0os6kNUTFF-204ianE05USnb9JONtc0KrC0TUrYzJUGv1JArJN_n6jvE-ROtWWYNO2RNnZUNbtZFfI35M0BAKdaG7q7iv1ozniEZTw3H-vU7T45mmtR-UmHzWKefTlxf6u6EpVIRQ4RoA3-JvrA05J_N_4_cy0ps6WSbEKBCI0PppJb2j9XHtpbw9dDiOCbPQJQnTHSiDQteDoPukRHI_JR7rrevBmbwuI-JJhAJVLhaMnt1JBfrQaVDj7zPt8O9DCNvNDOOzn5qNMJRaqaEIiTg3rJCbOveZ8MKYxHlQVTbJ_yshSxKy9YbyFsLTiB2M6FIeRx3lAYw_bq7gEvXz5_8vsXn3_2_OKPT3737NMniu8vTA4CML_5Hv77_9iG28E)
