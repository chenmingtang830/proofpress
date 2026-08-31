[//]: # (ob:ffb9914f)
[//]: # (ob:v18-title)

[//]: # (ob:1b9c9fe5)
# Exact Knowledge Construction v18

[//]: # (ob:c7bae7d0)
[//]: # (ob:v18-status)

[//]: # (ob:0f9993df)
**Status:** Stage A completed on the five frozen zero-heavy tasks with no answer executor. Stage B entry-gate work added complete token telemetry and a controlled official-authority candidate lane, but did not qualify the paid executor comparison. On the fixed 49-slot plan, two repeated closure runs varied from 35 candidate-covered / 14 gaps to 26 / 23, no task was executor-ready, period and calculation gaps remained, and source-bound authority candidates still lacked a controlling-applicability decision. Stage B remains blocked. All constructed objects remain candidates until Human Approval.

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
- `retrieval_adapter/exact_knowledge_contract.py` defines fail-closed schemas and validators for requirement plans, numeric atoms, authority nodes, derivations, readiness, and proposed-claim number binding.
- `retrieval_adapter/run_exact_knowledge_readiness_private.py` accepts a private task bundle and emits a sanitized report containing digests, object counts, slot states, and gap IDs without reproducing prompts, source excerpts, numeric values, or authority text.
- `retrieval_adapter/run_exact_knowledge_stage_a_private.py` runs the frozen five-task construction audit through the fixed GPT-5.6 Sol compiler, extractor, and derivation roles without an answer executor.
- `retrieval_adapter/reaggregate_exact_knowledge_stage_a_private.py` recomputes readiness from saved private artifacts after deterministic contract corrections without making new model calls.
- `retrieval_adapter/build_official_authority_catalog_private.py` creates a private, digest-bound authority catalog from allowlisted House U.S. Code, GovInfo CFR, and IRS sources. Official custody can support a candidate but cannot establish controlling applicability or admission.
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkwZGEyYjk0M2QyZjQ4NzYwOTUxODU0YyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQxN2Y4ODQ4IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85ZTI3NzA3Y2FmYjQ0NTI2YWRkZmVmMjgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q4N2RkZGU3MDU1ZjQzYjc0ZmYxZjY4MCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVuP5MZ1_ivEKAFspXuG98sISLBeyfLCjlbZXTsGLKFVJIvT1LDJNsme2ZEgwG_5A4Gfktf8MD8EyL_IOaeqyGJfuLMzY13sAgx5p7tZdarO_ZzvdH97xtq-LFjWr8r87PJsu10lds7cNPG93C38OArtJHDiwM_OFmdpk9-t8vKKdz18tlszNwgvPW6nnhvYbhBFkVfYcWJzJ3KKNPYdJ3d8z_PyIHFzOw7yJI1Z7qShk_hJmhdOkgUM1s3LLmtueHt3dvkt_tGvenYFO1Ssx60W8I-UV_DC73hbFiVLK261_Kbsyqa21vD5pr2z0jvr87Zpim3Luw6e2bLsml1xPNTk5bb5msNxdy0uuO77bXd5cXFV9utdep41m4tszetNWV_1rL6KPfti8nTL_7gr4d-rXcfbVdbUHa_hLvp2x79bnK05w0v0naiIYz8-E6-s-A19CC6XrxLuRpEdZaxIfT9wQ5bnBS9c_Oy2aXs82qoqaw6UK45UqzyO8jznkR0Ehe-lkV8UThHGtjiOpG6VsW23q-DALtKZNW3enV3-4dszuf23Z8Dlpu3wX-Jtnq9SuPI_nO3q67q5rc--hDMoeUAG97u85N0F2_K3SyCo7pf8hlUXn_z-2fM3q19_9vLff_PJx59-snr-8rPXb1799vmbFy8_W_3Oic83-dnivQSL9X1bprse-LlKWVd2uDuvihXr4J57Tuvt-nXTIvXXZY1LdnddzzfwTs02yGZ1igU82qFonF3Wu6qCM2Vr4CUXt5FWTXYNny6KNEkcv4CPAxt7_hZP_LP__fN__N___Pnn8KLcBPhDu29R3vgtvPKHi4svL60PrJ816eWNEy_7sq84PtHfbUnaWMvOvluMOzlpkiUFDyY7ffIWrsb6NRBc8fyKW89BlECKMrwCC5ado-AD6x5PS2pQAEGYJwRlUcp4lNtPRtD-lXQ963fd3J3YRZIkXl48GQkffviaNr388EMr05_brlnHrWbLa55brOh5a33-KgjOrc8aa8vK3OJvZ-iMo8gBy5X-1a4q5xmZsbnLCm0eukEST4gAW5fDlpZawCrrNVhH0BWraJsNHXJWiD6w7rnEjCQVSR6HTvq0lP2a863VrzlwBkw7bGk9r1i5sT5t2XZtsY7ey1jd1GXGKusKPQcyt9ul3cwteombRY7Pn5TWN-B9pIgBVS0vmhbortsSvEg3PcQVkX8LjsZCEnNrhlYwkGDiPe9Jad0XvT_uwLm-S_RckLzCjvYIKTcMPC54Hc7abG2pld4pb6efmxEyn4OUxRl7PA3PWW1JD75Bb8ZuGbIL1Xl5PajzxHy0rATe1qyf41aYJDZjT0DgGxCYDUd3VXYba323bUCEwB1a8L-atW1zC-arh7etv_zpvzYoa3JDq9xs2xkSI49FjDP38STuS1FZ37C2ZHU_a-8DH0IeHk3t6MRujuu8Q4pOPzUjQyGYT69w8sfu75xbyCNNiKxtBewA_kDsuC1Bgqymru6ERqL-96y7tiBK22xHCiswCVOPnEZO4jr-Y8nbZ8623HKMJudYw93CcfO98ARszbbp4DBqhXe7koPPz7DDTlPfdez04Xt-9dVX-NgXNahmeaNfM7xmWct_tljfbMrsgFXi3ZG8rMn5nqgE3A8D9nDaUEJAHyvalEn2gTCAkHz-yoJsZdsBdejC8jKHFAdoxCuCoNViM4zyQ-4F4WMubV88VIg-q7pRmoRZmk590S_Ltuv3D9lVZfYuQZl9cM4JpHEaMP8pqFhaX7Uc8g3MZVYsZ1uICS_ICawGJ4CpXd_CS-fbu6_A4xbIHqtgMzqcerzgYeE8AYWHnppVkPdm7F3uOkmL2LGLqR35N_1pqwN94PU7-XTyoRkepVHsunGQTHaHsBx86jNwWP9JERrcKkg8g8yynyfhA2v-0RlCnDgNnTBynoKQV7taBZxCW5ejtqa7ssrBIzfiIwUaIjD833BMAyLrm7nEIsltjwfxU5C4nBi5rNnBf4FaCjM_-qJearRTmYXniyFqXs5INM_sJPEL9hQ0qse2mNF3wkeWhcWx6iOMNwTRIhSDd5oaUrZdv931kEvOxTUeTyPPddwjJP6CSCzKt2Acc9inarZ0P_wtz3Z9095P-u6xypyfC5I8T-Loicl7Rmns3pUix8EDXJVYHWtSLHKBxWqqqrkl6aybdgPp0lyhguVZxN38iamdBrUsv2FgSUYRKEXwCvIIMRSmMy1aHBJUdjXnl-wiAM8UHqH2uaBWaGK_bjlfKkIxYC5KuIn7sf8-K707g0mdIEvzmP0VSH1RDIKqbnYBy3H-DWWk-sWDfLTSmHVsw63tzOWylMW2nR-j-GNB8a6qLBl7bVnNq_vd5-mH57SIhTFz4yciBg06g887rnrk2eef_J5skBRKUSXCe_qGt80SSLq5E1nhfIZThF7kPw2RBxW1XQacnY3THAY-hRfTktpr8RwxHwNPkICKvyvDOvnQXE2RY5mT80fujrZClFPoxDzvsODDNDHGjgB5DirC6bn6zN1kPE54nCaPpO41fgo_npfsqoaw20pFxYfVmKi3oqCISna7BnVmEDCW1Q7eh8h_jnOuV6R5ED6Sun2ZybBqNisyBfdd206mG4tiWwpRRM7au3cl4_sfnhERVhS2z4Psgbt9Dm4O62iolzkHDd2UNZbWMkvF6p0l3Qhpcb9mvZKS_Tv4cqG6ImfgZrCYtsogrBONBnpHdS34KmZZmCfc9yNuF7ntpsyO44ThJ4HrtKZs3FiycWNla55db5uy7qkP1dJO2ItQf2Er4kvs-EAmcKetoHeBtEWov_TABlHXFP0K0pcr3m7bUvahutS59J2QRy4L4swBxgR5HqSB6zKwYgVnfhjFSZbloZeGCSvcKAmZF_MssEM7T1wn8TByxTo_9ZMEty599zu4aGzeuLYbLu146dlvXPfSjy59_59s-9JGiuSNY4CZs8B3fAfEZHz12x-mBUVSKlpEYH_WqJZ-6tsxKyDrRA2hNbSukRTge7eD5KpeEDhumGFbgatVtQ6RXPWhLR61SeT4gQfJoBfkahOt63OC9NNtG7msHYaRlzDXTvxELat1cuSyj2nFyMiH_CNlBCkHQ4oWFeysKKHQKqIMV5zMroeUHd36UtSF9CwJgiRhGurdBgLODBKRMscMl8pG8K7oNpb93Zg8watTuwOpX3lDm8JbR6o5CzLebNiDDLJ1BZ85t55BMDBcDhYNZcAO5LGy1ja1IJsrK-tXuw2rrWdbtHCsOj_No9QuPDuPUycuBh5pXawTrJ9rQ8mFkzRPQpfHYBMitbDWmVKC-5i2ktwpy-Mg9ewijgp3ULyx0yR3ekybSCatwJ1rXKWDxKhadhyTm7LLqqZDp62W2LVoslGi2K4aUx44FggDmBcpjDdOSCti5t_yDj7awWo55F299fUOKCyw0r6tWKa8mOgI0Urofci7DZUpK0U56te0OCRKIJ2wRImaM9WqDURFrM_Wl1KiRSCLGTWqjKyCggimYGAX1hbTq1wT8JKT8FbZrlKijKcQ2TcusemEKwXxY3Rz6FDppjfsjk6H_heEdkYoi9R1eBwXYZY6iqNaP05y9DHNtP0mjtSnc-sFcK6Bx4lQ8vFwgR0HmnOxygL_r-7VzcNa1FBhOVwsiu8COdTv2lq_JWR-MxqJ8z39lGosiKZoZMuQVLpH8dA3QFPe3CIjOdvAA1WJ2dvMJSaOAw7aD1OeDwqoNQpPaPZcl08uHCU8KiIWRQXlWEKzx8afrtnv1cCTy_ssCGyIBwIvG_yo1tNTgeAjenOTJM6SudJQlRO5tZbKCQ1B4QEpt245u-Y1CtXgA2R8pXsBGaGStqBaKekAUQLGgzfo_uX0BWcOBA1R4IaxN9hkrWk4iP9jmn8U-FKhGMTxL3_6b-sXKjUZLRb4UXR8VHOThoFuTC8fdnApVQ6-9wYVBWx4BXzIqbtVceHGQZSVsZm4zYWIxJsK7u9qecSDnnag4lKR1C2477IHL7k9t14NxlBSVZTgNtmU3goUG1StB8GzmsJiWbbbkJYCR6sGkrQKBbaCZahelUEcDHbhNLOYmyU8z-MsoWSemKW1T0-o2XwbVC4deIEN8SQkD76tltY6o6OivVePU5mHwk0KiKZ9Fg6La21PufhjGpiiqiz1TToIpAcYtUvBSndYVgYusbq7JWdDuWtZgbwBJzKG6DMLtRoEMy0hZcCzwSLd-Re1e259QnIpPNWyKq-51TW7FmSr2woC4SKAXpApoFEm3kr74B8Vz4QkgTetdng71h1YKZlBizeVH4QNPYjBwINhuRHkS7yObTqGZxUtNenlwHdbaYn19AZ9L_zZ5HdLkEp07jK0E-KPkom3uBPp4DHxRqXRNKNUQSscEYjyIRbWVsSEFkxtC9cNcQnw6U76JmQDlXPBjQgtLbG2CzTtuHW7LgkfiRA_vAXMqBcQRoJWYVGRwpnsDuwAXFx_p0ICwS3YTwRtQEygWDKewyJJxLPhhXRUpxd40CP3Id2zKjcScUL6QMtbLp1ri4aVIp9dxRdCIIhYNLRCxvCvQ3Ip_NrwvESXTqDBhYy7FrJGg3QJ9im2cDhWCIw_EtwLFg880kRvMbBpIWWjFH98vWvLLi-l2PGiQCFDXpGpo9h_2KjCormM5WBTjEYQ4LiUNV7BTngarfcXdXRuPR_yCVkKF_HqEMaOr5IaoKnp0X_0qIjTxzVbIrfegMubegawJ3cUMA4bDBHJF3VMKdqY4YjgCqXpijYFuUSHCHa4x0PNRkNdA9Izus8xhDrSiJKWzQ3SNE6SKMrHlEZDTJywyHPYBxWZFJDMcnDCYTKYTA0OMUlp7gNvkMtyz3U9D6Jb4d5FmjwiHuSyj0QwTIIlUCJMr6TQDnBq-clppisMy8XRDBde1pJa-fgxnALIalu-lR9YE7eF4KDEoBve70TJj2qZFp33tmmvUfk7rg4tb2OQTBT6tCpFtI43_UUNN3cEv6HyX-54eeB63Iu80Q0OkA4t1nooRKOWnoGlJQVblGLAecGBwCfBdQ75BlzLDutPlE0eKkXGyy1pEdY32LQEMhOgcN_1bS_JwiQd0mMNG3JCHWaxHio-sROHxZDT22wMfUb4x6gP74viUHGw74dFlsRJnA3ra8AOuf5j8BlltcT0HXUBksYNE-wi3yTCj4KM3VShwHFMlEOP-2sQLyr8aKWevQKPihdEwV2FEuhO4Pjn2H8_ch5g-Wr_TMO6qy3txulwENByiFgpMKFXheak4DYr4RM4mF58v4PMoYeIAG031opVYo4KJrwh-lRhuwklAH9S-IyFPy5PA4G39eLjMT2Cpaieg4sI64RPCUOjounx_sjJyxRpuEPkq7gHbN50F_jf1SxDQQtaiEO4RAQMuiIvdTFEPCoKku5Zi1SGSEy807MNBA7w6tcqTDye22n1wqVI3EFAatpzMAYXYy1J-F1a76DKRw9R8LnHFxSL096O517qp06chWGqlETDFp1M898BEVLZjeO5uR-5thsPLk9DDY0q_j4AIFUezrPICxM3c6KR8hETNKz9AGSP2iFI0oT7mcP9sXg-gn3kDo-B7JyqEmjBEualpF4oUKSLZAXgD1Smy5kqGIQV3A_CKIjjoTQ74oAG8_cINM_4CtsK4cPsEazfUqqOVHxaCC-A6lI7NJhoGTnL1pZcg05Dn5OSramMjLBHbZtYFUGlHnbKPmiHQ1pDOnv4sQyCA9TB5pqjncXxL8pUqFCLsz3w8a6f0Z08y-yC-zmk6kPkpaGY9iBMD8Ei7YQ3x7sBlW_U9Y6WCV5TdprKM3UvIgt-YAbEucSuQyI6JJ_SjUgaCcAjDYzipGgkfMq2IqlmiPTB8jAsKpMeaiWokspMRBHavhs5fuJF8VCh05BVB4r7MFCU0oICYrMkDFLPGTbTcFJys8dAnPYCLRTxBVU38Jq0kiBW7LWAlIJokbRqr26rnfJCWrA6sR8HRmNHpXwUnNN3dG79UqJ0xrh_8KzdQla4ZVcURIVOMzaKFlruhnTTAzmXrbMhdV7DlVWDI8IwBDwadZ3nKmBoXoOMcScYqvUaNuxoufL9YF18sKta62NXd7stKoYKpfTEWzM9IkNYihNSqKGlHrxtIcwbTLSskKJNaSplXzYQ01X3NDZWjQWXvhlKqzNa5Pg8jCLw3vaQeWggtQMtehy2TPEqL8Ajhqxw4iE31uBmctPHoMRYic5AdGSBg59-_mYZnIfW6wak7GPOt685vxa39ulv_hUrHJBDdbQZRXt7_TJGlv4jEg-RJCnszEDDst9RyEqVodHZCjpIW4B9vQztaVHQ8s6CEGKtCuTYU6ECsGQ1B1ZjPw8sJ9_yOqfCMcP0Za4S7MRuUXA38bkdqLvVgHEHDH0vcJuq2npZ6KY5GMRs0DUN76ZFNA_FrCnnSqUaYUjPrc9VXZHiJPhYg8W3mt8uP375_PfSM-XYs6UX4MbrZlPWlEPJ3jseU0gF9oA2VD64XXNiwiE4y1rzaovt_DtsvAkMj54ylwXEmthexXCQi4hHrXZFxaNu197gyeUFqHxWNPWolDRmeljAnEmgeWpDhpuwNHe1MryC751CR5yG4KlykhPZeZ6GduSM0emIyhtj6_cB2Cnj4qdp5GZ5FMXZUAMbMXeaTX4ofE6ZYvSzh4WnSRFSr1hJu7jXbRPetuxgfVmPlpVsClxGcy1ugN3hy-gSsAA_hizUuREeQRhjXpMjRfyEtS6vUDjY1VXLSba7DDsCQ_EFklOIa6kmfyWrzRiJaV5GpGrd6GYmmb_mOpWokXSRDzreApyRuSBhRVCk4BuScOTfgEocItOHAwzVDD2V58FhTbmHrR3pSkVk0e1Q40rh84bwfRQHFXKwauA9lb-H_FnYddXcQG0WfUWIz2rc9Nz6uJHwAEi96w5ZRIiEfbO0xaygAxmpkeHAe6YyFdHdpIrNgIrY5Vd8tn_neOARCy8oEmeMXkaE5QntPg2WVJAqN-Je4foBd4bkTcNPar27e0AiVboSe1HmQELLvKEepqEk1YjXI4CPY2WX2gQyfwFXIqseMizUmlbwIpdIqzVrMWeeYihoJ4lkUHUg-GwFOoirah3ghfrUWEWlLmPboqwJUQCDU2HyA6caPi58tmgi0tLs9o63SxUBCzwGfnQauQzRJpEyxGvgrFCPBH-VUojwBp12rrWwUzwZw2aZqBLCKkcQGov9_ELdGEeNAbtF19i0V0CWqEthDnI85v7yO5SGI1_QIXyv_HqOl6A-z15Yz-Fe3p59Sd_5ke-yk2_vfbnH4duE2hjef1XCDba59YaBcP6ovgEErH3ZNmRMVigi3YkvAqH-w0O_B-SR30QBwkqorCMIYyFypzY7fF6iiV9J9snyjND9osmoSKM0XnQX869Zxgm6NHg4UYGRaMk5hOS5oFEd-duz2_XdsDs9e0NftkOVIbH5H6clwV5Z9HGjWbiO2vY9sNchS-3EtR3sp0W5y3mS5HEU-MNt6aBqHVCsA62__Z75fn_8-ICfHla7dL47DpB-F1r8SSDhcRH4bhblgRdATlK4KU_jMAOHFKVZyv3ATdLM9kM3jlF_cyeIXG7bURLzKCsSynpPHOkYKDy-DJIjoPC4iD0_LTIDCv-JgMKj2I9YXHDGCwMKfxQo_AVYbsc5NPaikILPOd5o9bEcWWDpUyQMsuevOYOO3IfBmhusucGaG6y5wZobrLnBmhusucGaG6y5wZobrLnBmhusucGaG6y5wZobrLnBmhusucGaG6y5wZobrLnBmhusucGaG6y5wZobrLnBmhusucGaG6y5wZobrLnBmv89YM1PgcxPocsNrPx7hZU_xS_iHK598MsfCOkMvSx48l_-yIU2jcZB1NNLEVRlbQORip9QyaO7tNy5X_6w8yyN-ROROJCDVOIagw0aIFSkdSqzGZOnpwT-I2Bv2kRdIjDWEhjcscctyvRwmeq8kJ-CWRUhjiKRth6AkeenZOcdcwgi0BK1DrUbxAQ1F90ypYtLLeQCCybjJGwtnRCrPV5M9xzjLLXlGBaI8GGhohGRPlDAJoGQ56fEZHZLQvxJ67wU7oqW4K2EJApoBhp3KpnJWEle9ruHKSSmSeNZ3YwpOEnoAlva4GQYIkLzaRSMBxRHPULoAH6FSExwXcmAwPOOcSalWgRz0_GFV6qsJ872fiMagRuFgZOlnsMd3_GixAszj_H01IjGAO__wUY0jA39CdjQ-w8C7f8IgbvQZk_c746Plnwv4zROFLrMD50wiHjoZwWPIt-OoiAOWZR5kZsnYZF5ReDZQRxECVDHEVHP4Ig2vJve53AHgzXepZNc-s6RwRqb2UEKm5rBmp_GYI3LwPaFLEmZ495vsGb0lsrZHGk9Hm07YitJZkFj0-DNWk_j9sb_rijTEwZpAamySJFGgyErriPYS6r9pUgcnQSRO74vnsCSxg0_wNoCbbzlx5qQbiBbTgTHH3G8HTXFjkODEV6hLOhYu1tIhKPECLGxiEydXEjqlL2CE4mQID_wqxNfrdLhwcFeCBjhwBZqDssU0kznmOkcM51jpnPMdI6ZzjHTOWY6x0znmOkcM51jpnPMdI6ZzjHTOWY65290OsdJ85QlAQt9JzPTOX-H0zn3uweCTazY5BYwddHTOaxtLukiJv6NGhYIdW12V2tZBEV8tIYpVXFuiwAjkqGmPZg2gCSGT0Yz9sukp44zdEH5_Y6lApNOszAUencMSxGK5YP2ShjmcZSOgr7QtwAp4sHXI-9qfqvDks20lJmWMtNSZlrKTEv9GKelwLjYsRt5SToYBQ1YcOza3hMe4J_ssY3VE9JFWZDMJPRSSOLR6-8-wv4cLTvpzX2kACzwBr17yKUO44WBHUsZvVScXUMm-1Jwa69pSDvqX7U3zv2ArDjJBXz-Z7537sT_-HNRdJh-_6DEOeKdXPGa44Xtf--fE-6HhY4tszTg1wY9sHhtEhyixVIBJ88PI0m8DC-xFKByVL9BKeX0g0BfYWpA5sAJdPc94p_-wT4PotCN4H2qt6h2oyUCBAJXd4PH7iiT3wtmrBaLHNhBJVeJF6jEfuiTSoOC71Gq3yNiaEaAsyJ1Ez-K2OB5NNjJIMAPB48M6H_JXNmko1mHsfHYYc2OEgIx_qQ5twHnRd8ceUmoY-C_6K5REVvjnpgHk1EvMG6767Smrxa5SHn-aJS2gSGLaXFQVD6FlZd9u7eiZlTXO1ZNWnIfSRC1QBZzWZSTlXnZZqbSZccxalLF0WFGiawdBvqsUzosrg3CSEYl31H2a5GZL6lgRU3Ia2xTkUnThNb6ah8e8vrNM_jvs9WrT17_9jdvXp9v8q_MQKgZCDUDoWYg1AyEmoFQMxBqBkLNQKgZCDUDoWYg1AyEmoFQMxD64x9mYn6BGZn3FJNC4490DMUcUNu7JflRvH_El8kcRFUzEf-IYddT_8zStKZ0QAa1eLcQ4skO__7UITjeesflqOCjRiwbcoismoAle1Y1V0NjRGypanqYOUJAhWwFqs9PcWt26PF2fSdMx2RAUERRSwIDylAA4wswR2SD7yBAFj2tuwlwSCvEvXMa8siNT0V0_95HOlRt_vgEJBII4QdY13baGXqvmcaEu1FkRxkrUt8P3BBur-CFG5-aaRwmq_7WZxp_xGbg_mOp-zN1zumBwXFk7nsZGMQfCAtymwWF5zI_LzIv9WM_Zhk4NHiN-4Wf8SBmhc1S5uUJS2zuRGEU5kkUuQ67z-GmA4POG5wTdC-d-MjAIKSURQz7m4HBn8bAoJcVWRbaHvNY_IMMDB5RZCxbWySLJ32X_EEsrdly1BmqMB7cEhcDh2qmSnkj0TXXfzJMbw69rDUUkJ8sqQ2CTg5i_9tG-hvKy8XQF-GMsCOnptW84LBLal1Yji8G6MHtuCH87XqLmXFChVoW3nx_CF_NNEp0CiU40sUdBWmCQ6wquBEaSmTToQuZDkj_qcDcA48UEleONJo5RDOHaOYQzRyimUM0c4hmDtHMIZo5RDOHaOYQzRyimUM0c4hmDtHMIf6NziFyj9lJHuap7QVmDtHMIZo5xB94DvHwANT-XKmS8Gpg4kr2RyfUi3qKJpoLFQ0eVlFFd5WORhM66OThgL9qELn12_PXELIAdQvr0-bmRV001vNfvhJcefHqtYJKn1svJWEqDEcLbUmU1wR-ghVrGewAPRCylt1aT0-tacVWT-npatBBYM5SWZ_CcrdM1M21KvrwpbtYOMKSLUWuGGdnDExPfkH_R2Vo-c9brIEuSBtQTrqGFFPlUfvY5MkYyUKN1i2Lkld7322HJg0fE_m9GTA1A6ZmwNQMmJoBUzNgagZMzYCpGTA1A6bf54ApT3gOYUnge-EwvaIB2bT6y0PhaHqXbGC2PhJGWPNO_EKDGnAbYwr8LYh6KUOREekomUiXFtjyC7G1vpKfYDiyG-D5coHBVmMdQWJrhmrsEWTNkHLiIpq5Ogp3EUTgogr2AvxBNwmnEqAccqmuAB64niVmasqNKosLmA2YBl7S9eBtDFtqkZZAy5B8CPnRCtes5pYaSFXZl1IYmYSRJwSJA-KZ7qD7YSyA0B-kiZ2YDR00UYnwR1hvA8_Q9XTCyfyCfh-y00M4iJZXZIsxRYTF4VA0IDMyrZetLgKZW29a-rWPO-DjldRAcVoa_BSlbOHPu6a64RNE0KiPeUPF7L1eppqIULZhAhUggzAN5OB55Ut0QLCelMqkj2HNcQ-gC-lkdq2swV5dUXSa9j0B9ffqDoxBO2_gzXy4mQ838-FmPtzMh5v5cDMfbubDzXy4mQ838-FmPtzMh__V58O__O7_ATGrBCM)
