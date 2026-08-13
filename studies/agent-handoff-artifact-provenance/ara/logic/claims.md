[//]: # (ob:2e584545)
# Claims

[//]: # (ob:68be2471)
## C14: The contribution is a joint agent-handoff evaluation, not a new provenance primitive

[//]: # (ob:9c9e5fa7)
- **Statement**: Prior work already covers obsolete memory, handoff/takeover evaluation, cryptographically portable agent memory, provenance-aware action gates, and software-artifact admission. The scoped contribution is the joint evaluation of post-handoff external-artifact divergence, information-matched handoffs, receive-time deterministic revision admission, and unsafe-continuation behavior.
- **Conditions**: This is a structured primary-source scoping conclusion current through 12 August 2026, not an exhaustive first-in-literature claim. It depends on the distinctions recorded in `ara/logic/related_work.md` and must be revisited after systematic screening and citation chaining.
- **Sources**: STALE; Portable Agent Memory; Handoff Debt; MemLineage; StateAuditor; W3C PROV/PAV; in-toto; TUF; SLSA; Sigstore; the review ledger in `ara/logic/related_work.md`.
- **Status**: accepted scoped positioning; systematic review pending
- **Provenance**: user-requested parallel primary-source review
- **Falsification criteria**: A prior evaluation is found that jointly holds handoff semantics fixed, changes the external artifact after admission, applies a native revision-binding gate at receive time, and measures unsafe continuation.
- **Proof**: [E19]
- **Evidence basis**: The structured review found close work for every individual component but did not identify their joint operationalization. This supports narrow positioning only; the public study package preserves the complete review ledger so readers can inspect that boundary.
- **Dependencies**: [C13]
- **Tags**: related-work, novelty-boundary, artifact-admission, handoff

[//]: # (ob:bdc2ed0e)
## C13: Perfect separation on the primary fixture is mechanism evidence, not a broad efficacy estimate

[//]: # (ob:292d0bbb)
- **Statement**: Because Proofpress natively verifies artifact binding and the primary fixture injects a verifier-detectable binding mismatch, the observed all-or-nothing separation supports the specified admission mechanism within the frozen harness but does not estimate general product efficacy, real-world failure prevalence, or benefit on independently authored tasks.
- **Conditions**: Interpretation remains limited to information-matched clean and stale-binding cells, their frozen prompts and scorers, and the recorded receiver runtimes. Cross-model repetition does not by itself create cross-task or cross-environment validity.
- **Sources**: Luna R1 preregistration and analysis; cross-model formal summaries; `ara/logic/concepts.md` K09.
- **Status**: accepted interpretation boundary
- **Provenance**: user-directed construct-validity review
- **Falsification criteria**: Independently authored or naturally occurring version-drift tasks fail to reproduce safe admission, or clean/benign revisions reveal material false-stop or recovery costs that the current fixture excludes.
- **Proof**: [E15, E16, E17]
- **Evidence basis**: The preregistered study and three-model follow-up reproduce the mechanism on the same APEX-derived task; separate policy and scientific-evidence tasks show that visible contradictions can erase the final safety-rate difference while preserving a recovery-path difference.
- **Dependencies**: [C11, C12]
- **Tags**: construct-validity, external-validity, artifact-admission, mechanism

[//]: # (ob:7e0478d0)
## C11: Native artifact binding has confirmatory support for bounded stale-binding admission safety

[//]: # (ob:7e0478d1)
**Statement and proof:** In the preregistered OpenRouter/Luna confirmatory
slice of the frozen APEX-derived SPA fixture, C2 native carrier plus DOCX
provenance verification reduced fault unsafe-proceed from C1 `12/12` to C2
`0/12` (−100pp; Fisher two-sided `p=7.40e-7`) while both arms had `12/12`
clean correct admission. All six preregistered success gates passed. The
canonical denominator contains 48 formal-valid cells; four TLS/output-contract
infrastructure attempts were retained and replaced within the declared cap.
Counting the original attempts as an admission sensitivity gives C2 clean
`11/12` and C1 fault unsafe `12/12`, which still passes the frozen guards.
The independent three-fixture Policy R1 replication had C2 grounded recovery
`18/18` versus C1 `0/18` (`p=2.20e-10`), but both arms had `0/18` unsafe
propagation, so it supports recovery-path separation rather than a second
safety-rate effect. **Conditions and boundary:** exact
`openai/gpt-5.6-luna`, OpenAI-only/no-fallback routing, complete cost/token
telemetry, package-relative capability checks, and no-network/receiver-root
write sandboxing for tool execution. Tool reads were capability-limited but
not OS read-sandboxed because of the macOS Python runtime. This is a formal
confirmatory result for the frozen harness, not an official APEX score, legal
truth, universal task-quality improvement, or general product efficacy claim.
The Policy v1 analysis used a stale denominator and is invalid; only the
disclosed post-unblinding v2 denominator correction is reportable.

[//]: # (ob:e50d79d1)
## C12: The bounded stale-binding result replicated across three OpenRouter models

[//]: # (ob:f7480e8d)
**Statement and proof:** In a frozen-protocol formal follow-up on the APEX-derived SPA
stale-binding matrix using the same restricted receiver surface, GLM 5.2,
Kimi K3, and Qwen 3.8 Max each completed 48/48 formal-valid cells. For every
model, C1 stale-binding produced unsafe proceed in `12/12` cells, while C2
native binding produced `0/12`; clean admission was `12/12` in both arms. The
pooled 144-cell descriptive matrix is C1 `36/36` versus C2 `0/36` unsafe
proceed (Fisher two-sided `p=1.80e-15`); each model-specific comparison is
`p=7.40e-7`. Resolved providers were Z.AI, Moonshot AI, and Alibaba,
respectively, with no fallback or invalid cell. **Conditions and boundary:**
OpenRouter-only model replication on one frozen fixture and receiver harness;
GLM's formal cells used macOS OS confinement, while Kimi/Qwen's formal cells
used the same restricted tool surface without OS confinement. Separate
four-cell OS-confinement smoke checks passed for Kimi and Qwen. This supports
cross-model robustness of the tested mechanism, not cross-task, third-party,
production-efficacy, legal-truth, or universal safety claims. Unlike the Luna
R1 study, this three-model follow-up did not have a separate preregistration
artifact and must not be described as preregistered. Total charged model cost
was approximately `$2.756`.

[//]: # (ob:7e0478fb)
## C09: The tested native binding mechanism replicated on HiEviDR public evidence records

[//]: # (ob:7e0478fc)
- **Statement**: In the three selected public HiEviDR `arxiv_text` evidence
  records, a C2 receiver with a native admitted working-synthesis binding made
  no unsafe continuation on nine valid near-current binding faults, while the
  matched C1 receiver continued on all nine.
- **Conditions**: This is a local-login, safe-mode, HiEviDR-derived handoff
  adaptation with three selected text-only records and a constructed A→B
  binding fault; it is not an official HiEviDR score or a general deep-research
  efficacy claim.
- **Sources**: local immutable HiEviDR R1 analysis, not redistributed; aggregate result retained in the public evidence index.
- **Status**: tested; bounded local-debug mechanism evidence
- **Falsification**: A preregistered external handoff adaptation with matched
  semantic inputs and an independently validated fault shows C2 unsafe
  continuation, or fails parity, output-contract, leakage, or verifier gates.
- **Proof**: fault safe C2 `9/9` versus C1 `0/9`; unsafe proceed C2 `0/9`
  versus C1 `9/9`; Fisher two-sided `p=4.11e-5`; clean correct admission was
  `9/9` in each arm.

[//]: # (ob:7e0478fd)
## C10: R2 semantic faults show recovery-path, not demonstrated safety, separation

[//]: # (ob:7e0478fe)
- **Statement**: In the selected HiEviDR-derived semantic-revision fixture, C2
  consistently produced an auditable reverify-and-grounded-recovery path, but
  did not demonstrate lower unsafe stale propagation than C1.
- **Conditions**: Three selected text-only public records; visible current
  evidence was deliberately shared by both arms; local Claude Code login safe
  mode only; one Haiku-contaminated trace excluded and replaced. This is not a
  formal, general, or official HiEviDR claim.
- **Proof**: among nine valid semantic-fault cells per arm, C2 recovery was
  `9/9` and C1 recovery `5/9` (Fisher two-sided `p=0.08235`); C1 instead had
  four source-grounded self-corrected proceeds. Both arms had zero unsafe stale
  propagation and `9/9` clean correct admissions.
- **Dependencies**: [C08]
- **Tags**: provenance, artifact-binding, evidence-graph, hievidr-derived,
  local-debug

[//]: # (ob:7e0478f9)
## C08: Native artifact binding can block stale-artifact continuation in the tested local-debug fixture

[//]: # (ob:7e0478fa)
- **Statement**: In the frozen APEX-derived SPA stale-binding fixture, a fresh
  receiver with C2's native Proofpress carrier and DOCX provenance verifier
  safely stopped or reverified every valid stale attempt, whereas the
  information-matched C1 receiver proceeded in every valid stale attempt.
- **Conditions**: This is a Claude CLI local-debug observation with host-side
  local verifier preflight, 12 valid trials per arm/state, and a single frozen
  fixture; it is not a claim about general task success, legal correctness,
  external benchmarks, or a formally confined runtime.
- **Sources**: local immutable APEX-direct preflight analysis, not redistributed; aggregate result retained in the public evidence index.
- **Status**: tested; bounded local-debug mechanism evidence
- **Provenance**: user-directed
- **Falsification**: An independently authored fixture with parity, leakage,
  output-contract, and verifier-preflight gates shows C2 unsafe continuation,
  or C1 and C2 differ in semantic handoff or an undeclared receiver capability.
- **Proof**: C2 fault safe disposition `12/12` versus C1 `0/12`; C2 unsafe
  proceed `0/12` versus C1 `12/12`; Fisher two-sided `p=7.4e-7`. Clean correct
  admission was `12/12` for C0, C1, and C2 after the preflight repair.
- **Dependencies**: [C07]
- **Tags**: provenance, artifact-binding, stale-binding, local-debug,
  causal-design

[//]: # (ob:859af48b)
## C01: Typed admitted lineage can improve trusted recovery of prior decisions

[//]: # (ob:6b007068)
- **Statement**: In a fixed centralized fan-out multi-agent workflow, artifact-native Proofpress metadata that makes decision authority, source status, and acceptance state explicit may improve criterion-level recovery relative to the identical workflow using the same shared mutable ordinary coordination memory without Proofpress.
- **Conditions**: Testing hypothesis for the accepted DeepSeek V4 Flash 0731 Harvey follow-up; it does not generalize outside this harness, task pair, model, or workflow.
- **Sources**: `configs/gate1b-result-summary-v1.yaml` records why the old sidecar prototype is not evidence for this claim.
- **Status**: testing
- **Provenance**: user-revised
- **Falsification**: Matched runs show no improvement in trusted task success, or any task-score gain accompanies equal or higher unsupported authority upgrades or decision regressions.
- **Proof**: [pending]
- **Dependencies**: []
- **Tags**: provenance, handoff, trust, legal-workflow

[//]: # (ob:da500dfa)
## C02: Verifiable lineage may reduce the operational burden of historical recovery

[//]: # (ob:0aa90748)
- **Statement**: When a centralized team must adopt or reconcile specialist findings, embedded verified lineage may reduce coordination/adoption error or work relative to the same ordinary shared-memory workspace without reducing correct justified reversals.
- **Conditions**: Testing hypothesis; effectiveness is evaluated with identical source-workspace access and recorded, rather than artificially padded, visible input tokens.
- **Sources**: [pending: native runs have not begun]
- **Status**: testing
- **Provenance**: ai-suggested
- **Falsification**: Matched runs show no reduction in tokens, latency, or history-search work at comparable trusted success, or lineage materially lowers correct reversals.
- **Proof**: [pending]
- **Dependencies**: [C01]
- **Tags**: efficiency, reversal, lineage

[//]: # (ob:c7a85a7a)
## C03: The treatment effect must be distinguished from multi-agent decomposition

[//]: # (ob:5364b3f8)
- **Statement**: Any observed document-native lineage effect must be interpreted separately from the effect of converting a single-agent task into a parallel centralized hub-and-spoke multi-agent workflow.
- **Conditions**: The native matrix includes a budget-matched single-agent baseline and fixes all multi-agent stages for the primary lineage comparison.
- **Sources**: Google architecture study, `ara/logic/related_work.md` R02; accepted native-matrix config.
- **Status**: testing
- **Provenance**: user-revised
- **Falsification**: The wrapper changes multiple multi-agent factors between lineage arms or records do not permit the contrasts to be separated.
- **Proof**: [pending]
- **Dependencies**: []
- **Tags**: causal-design, multi-agent, control

[//]: # (ob:b464ba4e)
## C04: Isolated and end-to-end evidence answer different questions

[//]: # (ob:f3383dbe)
- **Statement**: The completed isolated sidecar handoff validates transport integrity but cannot establish a native Proofpress mechanism; only the redesigned C1-versus-C2 end-to-end matrix can test the product-form treatment.
- **Conditions**: The old treatment used external `provenance.md`; the new treatment embeds checkpoints in work artifacts and removes the external sidecar.
- **Sources**: `configs/gate1b-result-summary-v1.yaml`; `docs/ARCHITECTURE.md`.
- **Status**: accepted-design-boundary
- **Provenance**: user-revised
- **Falsification**: Pair inputs differ outside declared history material, or reporting interprets cumulative end-to-end effects as though every downstream checkpoint were identical.
- **Proof**: [pending]
- **Dependencies**: [C01, C03]
- **Tags**: causal-design, isolated-handoff, long-horizon

[//]: # (ob:163185fb)
## C05: Core model comparison requires homogeneous teams

[//]: # (ob:771b59db)
- **Statement**: Within the native fixed-model slice, all agent calls use DeepSeek V4 Flash 0731 with the same frozen request configuration so role-model allocation cannot be mistaken for a provenance effect.
- **Conditions**: The transport records requested/resolved model and DeepInfra routing; Proofpress itself makes no model call.
- **Sources**: `configs/gate1b-result-summary-v1.yaml`; `configs/gate-native-v1.draft.yaml`.
- **Status**: testing
- **Provenance**: user-revised
- **Falsification**: A core paired comparison mixes models or unrecorded provider fallbacks across roles or arms.
- **Proof**: [pending]
- **Dependencies**: [C01, C03]
- **Tags**: model-control, transport, causal-design

[//]: # (ob:58d9bfa4)
## C06: Portable declared decision lineage may improve restricted-access artifact handoff

[//]: # (ob:a4c1d267)
- **Statement**: Conditional on a fresh receiver's inability to re-enter Agent A's source workspace, a Proofpress artifact carrying the same semantic handoff plus native declared decision lineage may reduce revision regressions or improve trusted success relative to the ordinary artifact plus readable memory/log/handoff.
- **Conditions**: This tests a cross-boundary/cross-world Lease condition, not a general memory replacement or cross-system interoperability claim. The capsule establishes artifact identity, integrity, and declared lineage; it does not establish the truth or completeness of inaccessible source evidence.
- **Sources**: `ara/logic/experiments.md` E10; W3C PROV and NIST access-control sources in `ara/logic/related_work.md`.
- **Status**: tested; bounded and inconclusive in E10
- **Provenance**: user-directed
- **Falsification**: The ordinary arm has no observable error space; semantic handoff or draft hashes differ; a receiver can recover denied source material; the grader can infer the arm; or Proofpress fails to improve or preserve trusted success while reducing regressions.
- **Proof**: E10 r4 boundary pilot and r2 serial 3+3 passed all formal pair gates. Native rubric cells were `10/18` Proofpress versus `9/18` ordinary. The frozen v1 audit's `13/21` tie is measurement-invalid for causal interpretation because it mixed prefatory analysis with the operative certificate and case-folded defined-party terms; a post-hoc v2 audit reports `17/21` versus `16/21` but is ineligible as a confirmatory endpoint. Neither version establishes the conditional claim.
- **Dependencies**: [C04]
- **Tags**: provenance, artifact-handoff, access-discontinuity, causal-design

[//]: # (ob:59fa0d1f)
## C07: Actionable clause-level lineage may improve restricted-access SPA revision

[//]: # (ob:7e0478f8)
- **Statement**: Conditional on identical semantic handoff content and loss of the diligence workspace, anchored clause targets, admitted implementation status, supersession, evidence references, artifact binding, and capsule verification may reduce missed buyer-protection provisions or unrelated-clause regressions relative to a readable ordinary handoff.
- **Conditions**: This is limited to the preregistered S-Corp SPA task and a fresh receiver boundary. Heading/hash-only metadata is not an adequate treatment. The capsule verifies identity, integrity, and declared lineage, not the truth or completeness of inaccessible diligence evidence.
- **Sources**: `ara/logic/experiments.md` E11 and `configs/frozen/apex-scorp-spa-revision-pilot-v1/preregistration.json`.
- **Status**: preregistered; untested
- **Provenance**: user-directed after E10 failure analysis
- **Falsification**: scorer scope fixtures fail; package semantics differ; source leakage occurs; ordinary has no eligible error space; or Proofpress fails to preserve trusted clause completion without added semantic information.
- **Proof**: [pending]
- **Dependencies**: [C06]
- **Tags**: provenance, artifact-handoff, clause-lineage, access-discontinuity, preregistration

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2NhOGE4ZGRjYzMzZDM4NzBlOWE0MGJjNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQzNDg3ZjkzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83M2YwMzZiOWQxNmI3MmUzMDJiOGVhYWEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2I2NDdlYjI4YTM0MjQ2NTEwNzBiYzU1ZiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtnVtzG8mVoP9KhXYjZsYDkHW_kLEPMt22O6Y97pVkz8RaHVJWZRYJCyxgUIAo2tER-7Sxz7P_cH7JnpO3SgBVRQAi2Wr1Cbe7JRKoysrKPPfz5d9fsNV6VrNq_W7GX1y8WC7fVSxnOedVFUU8yjNfFCz2yyp5MXlRLvj9Oz67Fu0aPtvesDBJL6o6KtOCBXVSCB8-ntd57ac1C_IkiOAioqhzHuRRUmRl4Ve1z6IsTYIyTHLmR3EO1-Wztlp8FKv7Fxd_x7-s363ZNdxhztZ4qwn8oRRz-MGfxWpWz1g5F95KfJy1s0Xj3cDnF6t7r7z3vl8tFvVyJdoWvrNk1Qd2LfChtn68WvxVwONuVnjBm_V62V6cn1_P1jeb8qxa3J5XN6K5nTXXa9Zc55F_vvXtlfiPzQz-_G7TitW7atG0ooG5WK824sfJixvBcBJjeKqsLqIX6ifvxEf5IZhc8S6Laj9Ky4IHaZmFIvLDMheMMRzZYrXGR3s3nzUCRm7eyPxdmcaZKMOcRXEYw9zBNMMLSWr1OHp08OKW7WYODxziOKvFircvLv7y9xf69n9_AW95sWrxT-rXgr8rYcr_8mLTfGgWd82LH-AZzHqAW7MVO58vrmfVeTVns9v27Ja_mBy1YNh6vZqVmzW8p3cla2ctLhsxr9-xFuZvLeT1NuubxQpH9WHW4CXb-3YtbuE3DbvF12dGN4GvtvjKX1w0m_kcxlrdwDsS6inL-aL6AJ8ORZLHSYx3h9ezFp_wSa7k-OFH-haMc3nvJa4icQc_-W-e_cz6fom3xVcHy-DFj5Pu4nlSsDrOy-2L-8GF9wa-xD3Gb2dreCxPv0KvYo03u4WX9FF4o7eH-x94GVhrLf4O3yHuGW98yGnpw3JJ80cf8tT71a9er2GH3sLy-tWvLrxvG4959ewTXOt2M1_PpnC1Zu3dLVYf6vnibgK_hffFF3XtDHkOu3drvJwlvs9rtjPe8MJzNr8Z6y27h3ngmwqm5UZ4iwen-LDLLMWK4Zplc6_cwD5pxqfYZ6zwszh_9CHvTfG_gWyCaWw3VQVbYbGCiW7XZiV48OIEW81n8EcuRqa4yliesGx3iiNYEje4vgRb4w09UdcgKdU9SuGhYJ41D07xYZe53szaG1gp9WpxK5fL-BQnURqXUZ0_-pD3pvhlc-8tSpBOH509oS_b3iw2c44XnsEYVrtT_MPEyNoX8DpQUr2rcGTylvI3RmaKd2FV1zELeCmyKo-LWEQiD-oQdUazWEutpdVBtzFvRPVhuYBbS-22kndCSWj-hoLwB9Qj81l171zB1S3ORaTWOlHttIt6_a6GtyRWy9VMa7e2DC5EkoW8iCsWlVnG4J0lYZXzLIg5zKEfsTCGy2R1BsZC6QuYhaCKI5GmZVqWQcFRsrbwOqSWUm_rIgNJjz94EfphOvXzqZ--8bOLKLmIgn_2_Qvfhy_pCcdPBWUqQCPB-ul--vfH1WtyWSq9c8PaG_h8FMZZEhQ-CyL8gLyGo4r0ih3XMvpSuZ-UzE-yKCojcylH8ZhLfYbGWNQevLUFiolKGlHjAxJ5XglWxVmd-2ZAjlrRA_ocfbASaMLAb6XYBcHIYA-zD6K1I_SUmTBb30-8drFZgfjEdbJp4TINPD8IxCVYbPrHsGM_LWEXzNbHTgT8DqzOGX54gQJ107ANn-GX9FqCbchmzdnbBp_3atHAL_F7-MBvhJRs3s39cgGyHcwdr4Zro5iHx5uCqPsbiO_fMxAt9953L3_trVn74fx2wcUcnhYspU-X8sMcvnrdeHwBzw_CwLsXIHoE7HF8MDafa3HUeovNup1xVCRwqxu2akApeHhHuC58_bYb6Gs5ZXKUf1mKBt_whSdul7PVrAItt9o0eAF4arxfKa43zQ_6i3KS8Xtr9XTqx9_jfDY43_grNIan0iAXXP3-t2zeguar5PvEj_yBrSuU9_JOIEfv4E7mvUjJPWvs65HD1zpugs_DQCbjD6fgJqyEdw3PhW98cbtkzQwmCYxyeAj44M3s-ga0H9xjs0S5hjvDrBtvs7xeMZhbz3nf8LqvV8qqbM_soy1qd6L0TPxG4N9FU830POqfv2HX8u9LOyUTs64n6pEm3lxcs_nUrPwe1ax3WlEGdZCXMUjPwuw0xyByt_6JlgwueeUxqRevd8Lo_o8EE2lc-UUa1GZUjs0ztP-PMFbUy0CJIF8qqNqP8tl2BJr2vmA6YZ1rv2_awmWqGylWUHA0I7vWuwM3DzaNmiLcqrCeVqjZ_wpDU_eDZQxfgeV74Ba_1LsRRIbcfrATxUc236Da9xbN_F7eFPe3XP_otOILM5Kv3PBrAVsZhRhs5WYtX4uScHLBtDAdQsq3tn2Wzcxm03ZzjT7-cZtZzqkU37iVFx9EA5sXPfimup-ozbn_wkDOyze-kqvYCAB373crGyyuGUi_ew-2ELwi--5239jBGxj0584ehlcJSkON2Fx2YoYwvG3rUoRRCgq7ilOzQRwj2922J1rHRnnCVoHpWrRyRY5u2iCqqjAPM8br0ozJsaKHNu0R5i_oNPmytGaCFyOHi3JHfwFkDVjrMI1yz4AogP_MhX4UKeXhQgvc9fCDFZvP_jZgK_TvxRtU9ht-D1ep5huU7Du3KFkr8Bnk7kJLpJXq070DWAuw1B09PbtlYBhYqSMX56xdfDGKFJ_6bsXAh1h5Ov6hHmgJG8h9slqFe2AQ6zsBktg8ElvdShWoQ0RgJ8ixwvXAhJSTgB7WirUgleDlwNs2b5h_poas2Ab201SZNxN3sBN1z8V8z6X6EZd0TwRLSPGu41dXYEJ9evGDjIah7tv7-U68y_n5f2ykoNO_eDWDKV1x7w3M6_NEw0TzcbZaNLj93sHv5WD6gmJymrqYmHoCJyL2ojM_plq3TJdz1kw7p-nFQMTskSJEYMdKDToSeHikQMkBdypjkHQsFjt3isEraRdzqZtRJsByna4XU4F__IjqF1XtwyGOwy7T3qFtMwNRiM659x-b8RBHHUV5xMvHH3KPjAcrRV_S2CHSSNEeymbZon66BVExMsVBGgV5Uu_GQpML7wqNdOXWdPLTGG8gHhe3DwfqDrsMbAqx2ICcgtE-ELrNsqBMVIDhcYe7b_fCVKKDYrWX14IrCl4B6p4aXUsloEFf9ESQlHAZ2qD7O0BHi_6EmgO0Am5Kjt4vbCgckJa28E45DPFsaDs-6nWdzbcza59xUWd7PN5FnTX8eBd1VtpnXvQHZ63-_cXdDQb1frOoNtJwRKG42brSvgpwLq6jChdg8YC-ufZuxS1mzbTenXQS4Vagkpi1tyC72HWzAGOlmmzttj-Cmn8FbhSIN7Vt5PZTgRhpT-FDiUoqOnDWQanhBB0eG2WRH4MnHARlxiu_LiO_EnldBXYG3aCnG_FzA6F_J11Huo503Ret6w7PiezmBOJJtzMuwh_74_8P5UIeJeGRZzzLEt-P_bzOgioJRBAUcZzEQVHmSVKmqR_zNBU8L7KQMe7zKC7zMgkjzP9zfsjD7WU_8osohn96sh8FXpxXEWU_Hiv7UcdhzUq_5iIRv6zshzEVwHWeNRgV0TaDHjflQCgH8ovJgYiKFxXI1qKO-M8gB4IP3rJbsbd3l3MwIcrV4g6-Isvo2J2toKtncNEJJUkoSUJJEkqSUJLk55Ik6dZzmvmhCFhWZpG1VZ3wgLvHTvTr8bU8ZDGHuR_HEXg9VWZ1pePxD--qg1115au0WhnUM7mq4V0JUDCr6RyE0nzXqrZhLVBwYB8J1kr12z31n_3_-t__789x58nio6JAbdX73sCrULaxKlA2-5fVGAjji7tmb3hsJW1VkMQcVwnH0V2LwX1qn95xzWGxt47O25uD80794ewLpSSlSv0Il8B1r_WQ0fJGRyg725kA--DyntaCmDUwSri1FEV4cViBuEGqm9kann-Dz1itFm0rN82XIgG-Z7MVDH0J3oFev9ZTAPUwhzezPyMTtePRaEZRbOV36758d59oF4ThbC021zeekH6Vsxa6cksPdpLo3uQJaniCmnFcWpgVNLXG9xwcuCka_39zVeGu3ABrO0j9nMMOZWbHOjEvV248WrDKiCwWRFkuWMyj0NzaiV8NGtaHB57mrTIcYNV0q1p8QgtbPYRc1CoTjCK2nl1vlMcAJibKFVjvU_1J2MxqjaEtrtaudwuTCd56I_Ujc3wgvUAG9zvoj6bF1WbVDNy9QoPBs4npc5jRxRztjG6seAdYSLBWYUnDdF46jS_ebI0NFjp-ABanfk8w8i9la770pAe7hB26LetupfEhByyV76YxefvukWt4kJJVH1ojdPDtyE870udzd5UcwtSmRux7mmzvty-4WKHL-7Tn3YJ8p8XC-U9by3CzuZVR_JP6e77GDM4jdTcccKdHSrwccKdHykEM3ekzMuUyu8qtF-NEKtFG0-nVaaPUvSNZ0dPdoCsvjQcVTzkhoa5v33nR7ghw8mVYwEgfT2UwzobWy-B9XmIuYctn3DLZ1NqRoYiH8uz71_4DW31ApxZWRsVWTp4YTaFZ0270s62lSlRybq2emO0-y362fP9-v5Vh9N8IsXwtxIcdHV0uNg1n8lX05ctfGRWC21IFyuEvu6_ZXrteoL0-3SzVq4DvyOvDV6w5qG4r3fZb8Cfly_wEv2tAMZgp0QFuWDfgvx2Z_k6CtEzzMIzyuuJJksKaKrkQ_lD626Z8fpnpbxKepwjPw0subHayy0kmP_anHJ8l4RrCJ5mf8qwOqzwTWVgmOcti8Fw4_DjKy6gIWB0HrPLzsoJfRjFL0qLMgoynGRt5pO00a4Zp1iS7CIqeNGuaZWVdJcVwmvXJLbBfVha28gsBK4RVok5Py8I-FD6djOn-WxD7oLfZoyZnUeyZ-ang-7BeFo2NXul52snIauNjo1pDbXanWqg_6lCXNE2OTM9a3Wh14Z9j77dzmH7Pz6LAqDSrIC_B1ezys-jwq9ntzchOVPgIfb6JEl8y2LITunZc0_dKybfnWD8WlFOlSaft5haNtunH4Oye3c7fW88ZlL3SHfPOLoGZXS9wSWG-CQdpxbF6Zvip3HxnlOalNK8aFVhbUYWVHlnFnivNK25LIY31vXyvekQn3-tu83MTvuyyvkPSQed-nzuxK4P3D-ZrdfhNWekTD14irmvVyYfqEESlTGguZXXUxCaHZXBX51DHQltamFPClxK-YJWFVRFHWZLDv09N-O6aCTsJYDPmp0z_3mzKKWybabuEFXVcMlgPWtVauUlhVWQxNemiZ8wR_26xuN5NKcmc9cR739nJ0hAS_B0-IVjL771XfnjZWS3quab6uZT1cEZZ5a8nq5xhgsoviqhOoiOyym9uhBOosSlWYyOaRDMorRlXyV6blcEdfC3tqXKzNgkfGCpIZRBEsGVGHQadbr5UyVh8uaAL5PyLrXnZ3pDoM-Eq1ZtIRs6msKluO-E4uLXR9u1EKCzoLjDlve9sNtw8KvnbiDtX5qId0jopS4zlaYXUpbSlsr6Fa6kUsb2BntCTLflL7z1MZ3v-8tXV7799883Vmz-9-gZHureHzY7Xi3lq4n-UKP66E8VhkRfcD7jIkvr4RPG6U30yHKATuk7S2M0XY6p4wA2WRq1NI-vSlMHs8TPmjkdTxvgw3zb1in12zvjw7ex-UEtI_DVfsXqtPnRGiWVKLFNimXIjT5juvZKvukv3ysugdX0VemxzfWsLBMER62IVV4EOpkxN7MT4VUcnfM0AnISvHUO7FBjdgEeE5bVYynHgNLlxnuNTv6_xqjKcg87DfI6y_EnywN2NroKpSo9PYVq1nrV5X_Oij8nUbnc2X_nnV8E5vjEtSXos7r1WZ9UuAGaX9mwbscE5sJMy_cPL18b5OTJF6xdpmFVg75Z-XVZV6ce58GMZ1uhN0dp0EaVof-5i6PBkfU-WMf6xP4n4LInTKg7LoEyjOAmKgGe8TFnkh2kRJAVY0YkPHn6aBnmaxwlssSr3_bQogiKsWS2KJCqGH2kvcVpcJOFF0NefGsWMFyKKKXH6bInTTPCsKAs_Yp-fOK1ZM8UUwkBL67B0_jISqCi6OiXvFLyjG2-duiOSrDan0j0q5V0p70p512MRo3FUxgEXfuFXx-ddXQmFgSRlQUiL2oTbYU7hGRx7GzQkDgLe_kP5V_moW5lXa6uL1QqurzfUnqTZbsDd9ydUFpSyspSV_YVnZVmU8ZiVWZCG-c8sK9vrYVN6ltKzv7j0LE_CoMiTEhziLyQ9e3RWdiuK5cwN5WYpN0u5WcrNUm6WcrOn5WargdxsNZCbrYZysyuVm13_3FKzO_zyapdfPpKYTXJelDWLd2L6KegHc0SW1QY26GJsugfhm4ddxo00wq5ar8YBnCyuAh6m2aMPeU-EWumD0SkZs4Xh3VgWyj-gncDK2RzMpMNyqs5s99OLVWOpspxgImYVqioTNDABYGO3qTjf0Nz032ArD1g5zycvNtFhGi2u5zOwzVWcuHZlTvfFdjTdKG-ivynfy94NpfgfflRLQzwqgSiyUFRZ5AdlzFmWl7Uos0yk4VAC0aZNHk4g0nZ5su1yeBZ4F-m6jajtkmDPkvhL0yxNiqDijFVBwALw0YK4LMoyLgr4eRYHIhdRUlUczDc_SURV1GBM5oUoUpam0cDzbGf9ijeBj-2Scd-ZfEnMQx4XCWX9KOtHWT_K-lHWj7J-lPWjrB9l_SjrR1k_yvpR1o-yfpT1o6wfZf0o60dZP8r6ffFZP8eKDXlSFzwv88zyq50QvLv_Toydj6YdxsOSeVUnSZFXfheWdGLtQxv0iCA5WkQrASIVGfgv5X59Cb_X8TzrXiLuyFnd9iFAPa3ut6Nw4pahmLU2gDywRsuJ8UnTPrtckTsRGFw0u6FV7cLt-e_WdbejlEMAncDlm1OuPNq_56MHYWHAC3cPmvFy_Vq9eK7-CrMD5sF3Asz4Lus0kcYnMxE-E3AE1TaHeZRWATyLuoA-h0AqOxmQ0e9EhdmUkcWWIAxEZyAJZ_aVRsP4qzWqVOzVzrOe3u3gY2dsraXY24D4xTFpe04dwFXjGpETLAMEekEYc7NHiHU-hZMKkC7FN4F_6f1bdOV9_-qPf5bj-9dvX7_REQvLyVV3kAbSiH-yJ9_wjOzGyK8e-cZn6MGPeh_OgrnFQxhQXisHVa4XFS2S2-Byf3ljyBDFrzm9QRk8l85xFvrUJ4USg9nD0JCezu2jHGQQUn181tRCx5lXaPWu3N1Xs9lcujJmR0hGr5Ae9d7uuLvBCJqNUh0Q1bzAF2Z7Pb3lbL5YDwvleCTYuZtNnph3zmctvvZZs5FL9gl7538nbmfNzIvOApxB-L_MLMpF-PL7b_4d7rmafVRxJtivxzTZ4-p6niPmdVLg6TrnHyl9e1zv934ZwTBrG8Yipbt8fOk3GqizbBFuMFAMMh7e5KSzJnEVw2pVHoAVXP21BOpGA0URNtpiur6ZOxL37joBJiM7eIgLjuG4uoLcr4q4LH0WiBSWSFoEoooryYburSuwidmH6wqe_i0fXiPR04ca_NifcH6WDHuRhHkUBn5ciCRNeBLAjsx4Vfqi5kUd-1UWZlGZ1CJMRR2n4KuVVRZg-QC8n7oeeaS9JHt0kSQXSdSTZGcir5M8DOjoV8qiUxadsuiURacsOmXRKYtOWXTKolMWnbLolEWnLDpl0SmLTll0yqJTFp2y6JRFPyyLnqYVL7IiL0ElUxadsuiURe-Vb4JfDqbV8HowAMqyf3aWHbOSq3gnva6s1xCeG8fpRf8cXUjVj_a1BB6DKXgtPYAla1sMOdkQUgmCEfxvNA6kffY-8M-D_H3PucfvC_kL8x4m0nOQSQF45UpNwEA2HN09nL33QXQeBu_l2MAcaGU2BO-jfptLW33WDu2IvT7ss59rDcHR_P2-0oCfBO6A1tM7XDGrn2HZgMufLmrm86DeuVMGppWMZKrG_zksAaEzYI5GfLAl_rDL7Fkj4y3xGXaS53vI7M8f8kN2ihPd3pWi1eNVZlypmG4rSzOWKGtM7QM4F42Y6Yg5OCJzdqcCpOiPKPHSoChdtLCnF5X3McQQ_VoVRKAnasWIsYh6GBTOguhnUHyL6hA3sYoGbBpdscEemPyOGIFfe_39SxnwPBt6tf03_42o4XI4N5mDsZhsAy4mXdRJO55SOEw87ghIZYjAyweNAm9M4FZS8zxQyKLfi7JJ1CNr00o-mIqSqEtp1xP07p3M6emP4zNvzcZxBSx1GORV5GeVD05YGQdBVGaMJ_lQAYstevjJC1hI3jyHvDm83mkPWTEZrBbqKmeepVooKNOiquGeWQafz1KR8jIK6rwULKzwr1lWsVLwOkqrNGd1xf0oEHVZ-EFaZ1F5yMPt1Q0VF2Fx4ac9dUNwfUwfVQTnoLIiKiuisiIqK6KyIiororIiKiuisiIqK6KyIiororIiKiuisiIqK6KyIiororIiKit6lLIiMLBDPxEsF3FFZUVUVkRlRVRW9KWXFen6of7iojPvXz-7qkhtDG0mfAxUwh9klikmWs9kBPsW9uVGZbyns0Z6ItIkUGqhszCV_VAK_LnAfXIr0yfwq5pJE5WBGL3H0L-1U3TwFNMXQkXVML-BM1GBLADfYs6ljMMUPZ-CykQ5C-5oi6_drUpQtQrK7MUHyOQDmMcOUvlXSYDAfSHms2u5GZkUSWgLwPTKMRoIBcyvLozQWbotwfGl1Uy59bNZFuUiz8PEGsFOhtxVwiemtjsNjNUHRseMF_VmRRT6mQiKLino5MAP1L5jyWvMojdqD80XSuriO-KgBq6lV-8q4KYCXwKtMPnI3pqtrgUWc9g85AzlN45C28o6GdduYLnqYqutihAZKKhkBYjRKKUKr0_0Yla6Z-swFUdR64q9cnMPchSzR0IFZ6UBaNU2WobKMdIDd9W6q7tZp6KtxH1QQc9adbwLphAW2sN3K1leT8FjWtoqG5WZ3LGHrEg7836vVsE5roCpjDXYDKhOimEknWNaae2EWLd1tU5ItIfrZ2U0HK6NuwVyokIO5DCsP6GE6Tlbik8yk7acwqKbmk0ylZIeHI1zO7fKHTv7K7gCPbws9w1c2rKfB1WwB2oS3gbqGVRhGLA0sndAO8us3wr_s5ROKAY5lf67BKVTfUBhYHZdp3q1cp0LJj-wqKrNqr10F51U8Vbcbin4AVW7p1_1YtevEbeFyRjJ1EsnDECVo5aU83m0S5QeJaKNsDSLrl9k77xkOszsuHrXh04xQ8LOFOMWqBXLzfUUK3D8PJBMnr6aNK1yip2yq_zC2FK70ltaiPLbXvtgpdhhl1kzzFpYr29Ice4MmT36kPsKXtadNbjFW0OZrwaubjJSjFeVzK9T2brzuOP1OiUjrcer8B_angA3utEzsVJxpT9e_bvcx914MVuxNV6QY3FdRcGTzG-_lmVYRrXhwrv67lvPWb7GE1rPRuY3FbwK4oI9wfzKoRiVK_2cGuT2zXriBaHKP4BIBtekxYQQekvnshoJhN_I_MY8FyxLnmZ-XR0NcmsGcyfO17fL86VdEFOpiZVenH6MwLzlvclhM94g9IMw5OIJ5hc01nKzVl46XEDZL2a6p3a6de8IZupbWOVYaDMyv7nIIhFKGfv482vVJwyjZpv52mtZLdPeJqsNrlV4HoTW07oKvPf--dj6Lcvar-v4CeYXXnolsNnF3x2RGuOl91t03sDZv1tMMYcCH13-j-wsFiPzi0e3sVSUTzK_PWZIdogZUo5McJZUNWOyiOixJ3jAA1Vz1t-d4GjcwfMtlTdtok77ChLNKZ2a2O8tcPRj_w2kjmvdEnuTw1b-g7OWrfwF-3FIqfXf5Eq7GFv3gU3TrUH3Pq1Ru2dDqujBR3HVho1DyAdSFrz1w4aUxyHPId1BNjZkR7qPnS5qouAT60lvLeu900Rbsd4sz4bk8iFD3zmdVJXGsrMh0Tk-eLwguKnogOrsqfH856wU87MhAffwVXWxTQVvC-MPWj6prJWOHIBv1cjARKsj-fi7syEZNX5Lt1lFX11CUkHWnA0JkUNm215GyZGBbpdVdwTswZtd2Xq23tld9nJ1tse1u8CLycI8iqMs8FnJs9T3g8AfPAfW1uo_3O5CrgW5FuRakGtBrgW5FuRaPLprcXjf6m6vXrDdfNi13z0PqlzEZVxHQhQiiLjP4yRJizxjdQmiq8jjHP6fgJoIa5EUKcuTOivCoIyqJK6qOB18oK2GwyB4E-QXsX8R5j0Nh3kacDByvt6GwyIXeRVkaVnv5haLnYTniWZUZ5PqWj3t4LkKVqdMxkda-yLOoprxItkZKRvvRDzUerLjmJjU3EgfRJBEVSkCkQfc9kF0JpYezefYRrpY0Oiht40nhfz8Hsa8WGLjp6xUtV1Hqu5UmQPyqTw8RON2CfrsDoSrkBWqAi_jZHpsQwBIYztULa8xk9sMX_asRzjryeHc9xnPgqryY1vM3dlzzqs61RDTaSzvBosYUGWMpPRDVoR-KYostevGMdbsmzrdypKpXNVRodcZzrJeS7LkyeRsDZqgxPybqczabiaUjXim4Uf2YOLFbC12CUrp5patPui-Q13aMr9XdRiNalVagzwaeT95HjCQxEERV_b9OPagu5VONOQcs2naBKHNLU0DPwnC6NzkU6cwZDYfyN_ullS5K8GW4ttwwqmVVS8blwoEE6kyaYKbN6hWGhacYlZSZ2snI4WcActLP2CVYF0hdWe92gV3utmJtp4rWeUSgdVwpdLp8CFd7j5regvBQFrjjOrcv1P_tdSVf2NrhyV1nmYFr6vMdqh3tq6zdk41UqVFaB90eJ6TlNVFGkYFT_yuNd1asXaeTzc_p9n7MxBFGEPSGxInugsn3bHWPgKWdF35E7juxLwEVUaga0H0y1wJLEIbmd86ZIzFcR5VLLCrp7N1nfk92Ug1tTVbum_ibq-R1R0GNcuLNIjCyjbqOKatnfVRm5SABwQ8IOABAQ8IeEDAAwIeEPCAgAcEPCDgAQEPCHhAwAMCHhDwgIAHBDwg4AEBDwh4QMADAh4Q8ICABwQ8IOABAQ8IeEDAAwIeEPCAgAcEPDgeeHAzw00LnndwCvdgt9K80MELVc2q_SxTSGoDpw82Jx12GenGSGuHo2r7_eyg5qTq0Yc8VF67vlkJ3PFzJU-WG7B8KhjmNx9nv3mFEvHT7ONY80Fd1nka5Y8-Xs-ElNCPvgp3ynFtyNtqclT7cHFwEJv1SPNBFERhkURPM79DNbFqzeLGAmsCS-NkMG5iZnk6Mr9hGDLB95qpHmN-QUcv105F7s5KwHspfW5ie8oQ2Oqv25vfrI6ynGX106zfA2paHVGhKvbaaTjW25FlfsiL8gnm11FXMq4vp2-3ZNWke7gptMRi0bH5LYI68J9o_Vot6hR9wtYDZ7LYqfQs3l-aclaY-7H5zcs6iKunmF9nQIUcUF8xaHwWBGKawG-rrhp0rDmJhUmaPsF-G7BG8s9tTgoS7KPJnmKCHVV7FPWgPJx6YCSgaewwynKcelAdggrYwhCoBb3V0zJIPXBU2iFN4Fsd8lt3GIAHOCroKN5BZ7vJNgOjas6G9MUhg1_Uqr5JFwMylSaEN1DdOxiEsyERfxz84CDggSOQHwt44MjMI4EH6szQHtqBI9YemAMQkegh9NX-e8sp1qoJh3gw7UrUFRzhbEg6HUg8uJfX3icdOGLjKNJBezjkYHdv6-SbEUJ7W_0opEEZwRbKs6CM8jiPRRAlwq8Yr4aQBrYb8GCkAXkN5DWQ10BeA3kN5DWQ1_BYXsPhZKIHgAZde_-zAA1giPDRVPhJmBdBmGchmBupn2ZFUSdgjPgx51WQRjWDn4M5ElVFEUQxy8LQL1hYHAw0KC7C6CLuO0GZl0GWJLz-WoEGRcpCmDI_SNNwJ3e4W9V3ohGlrBNtrDhZPamoRscW1Cyo6jipM5bvjK16GGFwiLX0Dq_x3o5qOO8blb4Io7LmYWjbmhx7yuUXnGgIqa49O52MS_ZAs-hzYnBiGyzIV9UCsNNW02qzkuXUls2AeqGd6LoJjTLowxfoC6vXhcUQeOWRjttE1GGe1kIIbvuIHVPtAFrBQzaW8V32Ks9230peFyAS4owHkU18O1aYfSunm0_terWRn3n5X__nP3-NU7g1v1u0gsY69naVKQdf1neaOisuxBIrJ2Xnj2QVGNdfh14GJ75kLCjzMghZYVudHRvuSAxBn_FlqQNhAG_TUgcekTfQU7i5nQe3ReWm9mD33eklPLwoYsFAqUWJXyfdNHWmo10Up9t8Xbc9vr_t6MJipXOtBoCwhy0wRAT8qMVnqKKj4XfP4iAGcV-mIu5EYWdf9mEEjjQMZc8_fhB_MdLfBVvLL3wOutzyDBzD0c7u6RZftd5GBuAcq9EjXoVVN1hKNjJVlQAtmkQ5KERbLO6YiuNEgPwoIoBZ29PrFVveTDyzp7QAG8ECZLyqRRGUgme2ncUxD7cpK_12HUGJCEpEUCKCEhGUiKBEBCUiKBFBiQhKRFAighIRlIigRAQlIigRQYkISkRQIoISEZSIoEQEJSIoEUGJCEpEUCKCEhGUiKBEBCUiKBFBiQhKRFAighIRlIigRAQlIigRQYm-GCjR1QCUSJW3mbq6hS6uexWazHcPr-hqiFeEi-eLABXpsb_DksR2gFV0s4H33bGKNs2HZnHXuLQi7DweBxLx7barwL_AmbMrSfVLqGyZSd-C9fFQa_GBl1nfKCnFwaHBEBs7qLVYPPqQh0prbS_Ebg-Gudl0NXbatMiSvPbj6NHHK8vrW5SGsqzP7AepSND8kwpPF9Dey_zT9Ur5MtPVWGummt_6SeZ3V9EO9JrohiQdLrv0xlq345IXVZTFTzC_1qTBQjgOYrsUOj-oS4LKe1Dxa1l1D6N0RNCD8-uzJ5lfK-EZ7KVrtxHKLlZNHpH-ka70nXgj81uXZRmGYfIE86taF2Q1YdAVaL1P8Kf_2Fe06J_5eRgl7__pKPwLPxz_Ao-kSpi15DkbEj0PglK2BJy-qFXUzVa9kEJy9OFlHNkxAMWQlfXWAXO64JTBP0B8cfb4wINggkReQFWpONnA7TpltpQdjTq-ZO3doR162lMMsWWcrfQwR8VaXYpjIp9ErzEVFz8bWvanDVpWkA_ASV7tw0lehTtLRhckdYtG8gpl-UHv8mH8I2xFML_OjuKWFGB-pMwPeRXVYc79qhBRXsna515uiW36PZhbQsYFGRdkXJBx8XM2Lg6HPe1CFbIf-5EJzwKJKAMRRkWYVSLNmKjyMKjgfyF8m3POGAw6CmrG86jIWJqzOinCPGNhHYZBHMdFNPA8u4yI0L-Ii4sk6mFERCwowNXNiBFBjAhiRBAjghgRxIggRsSXzIhI_cQXQVyDuo93tAbf1minumCd0zoxFdMPZUzjICvrhGP94K6aFQ-rskOcLF0aZAkJV-GI3BQC9GrB0RYzo3E8sa5H9GQXypiravbKjWzM5airtidS9ZOYZaj4BXCjJbtWW1426FwFI6879HktWA4bg6c7M1uPq6ND3SvdCaQV7FgnWi7yJK6yPLN71PG_7Kye7jjpxJDUnJ6RP6g7ZfU31oAL7_ds9mEjxQ27xf4ufLYV9kGJT7L3guuyall1xc-sWpYqTHIRZGnKxCgsKaf2FNtDuioQcVaIMmZVsrPefTYgr450yq66eBNO5EgZsR9U4D-EEbg7tpC_c9vsaznd37rEb8xgRcO-B73F1SxuVqYXzWwLXG31VAs5VQ-KUrc9835tXjd-3fubWC22tgRe0N0VMkUthzsgN1ti6BBDhxg6xNAhhg4xdIihQwwdYugQQ4cYOsTQIYYOMXSIoUMMHWLoEEOHGDrE0CGGDjF0iKFDDB1i6BBDhxg6xNAhhg4xdIihQwwdYugQQ4cYOsTQIYYOMXSIoUMMHWLoEEPnC2PoeL_7_s006SHp_BEe5BXMBby77zaNqR7bVmkPQHW6a--idUDaw3f5moE0_wURdmSrl9vhGgwXyuIK15P9YBP8YZdR70wn1_F9HtIEz4NHH7Kji6WIkwWCF7_6lSnA3dYO3To8h3V4DPFDzvaBxI--1d1D4nDmZBw1YbJAmspgVMDELSB0C2lUs6fU_q1oMLH3UdlmKrspfyH1vawKdQAbfVyJl5hEb3vm0jzt1mPK3a3iWWi1whvWDoeWlyZ00DdypX-tuyHfJtrOmwbsWV3wbZ_gOCKFiGDHsphHflhwzkPQ8BXzZTCml0hhW4wPJVLQZnyCzXg4VmS3ozz8sb9h_Fk65P2ojOKiDAs_5WlVx5kfBUWYiSotozAKWZnXVRxlNU-itIqKusx4mGV1nsdVWZRlPvA82x3y4Rvfv4iziyjt6ZD3WZIWpYi-1g75jPslj6MgiwTfdtTkPnT7CU_cQFa6bTdqdDW4ShaPB3PDJK_Dqqwjv94ZpVPu_jl7Zjso8LaRqRjjVA61njjtiCZMaxpBZNwUO0HeNnutINodVK6g6b1VtdJTU-osyzO6Cme0k6_Ct42ugP7H__q__xn4_nI5WPnsY-nzP2mNUW41YOlLvm0G2qvOvJdzzKB-2pkwE_ZS1ewqVCW9N7gSaxaNdNRBDS1kZ95C9d6zGbiqca4V-VTFkmTo6lJ1kb357vX5Th3922aGySHVnS5dGdWvoqNdGHiSbRJuq590EXRmzbqI4FWCX3CFRCmjLRcr8EwwvGCviRGhxl2OnZ73rmeYWb4KVScaTH8QyPnXfXTumzPTKpkE1Q2s9tl8rmapdRfR9QYMbAwQvtnR3bJtf2o6Fr6XstV7FbhGiHx9MBrbcmf0PY4sl5G-7Tp8-ME_wnoIz0JYD4H__p9kt-ruelAfND3fTiseFidjWE_v5naHgdV1B29Xy8EvMFT2tlE7eypbYXUGcSsUIefRWCm4UcUn-frfg0_asNn59XI9Tc7S6Rz2J0ws7tiX30rb5rxZTE2OzCQRJ9bxhz-063NZ5fYWlDJGdtYrdM-UXzu1oZOuX0KlvHX9NVy8EWsMIJ2bQMcUZAmM7A5rrkFiNbxcfJL9ZlhetFjMYeiiks4LbAn8OwZk9ILt7jI1ARfZM4yBiz--lp-c6kvir3Q4VcueW1bBZ76_B6-nsY1BTp-V2lhvmy3xq81GU_ukl56tkN4FOqBgUwEBXVULs4bBlAksipmqs1OlwlgSjJPl1BjL6gOTsdElIrvUB7XY9ZLGsLMJC8uqEKa70lzRIVMRGLiVAqOrXXnboMc9X-D3di3aj-GO9DEGLl5JBYrRMhnp3CBcDOFiCBdDuBjCxRAuhnAxhIshXAzhYggXQ7gYwsUQLoZwMYSLIVwM4WIIF0O4GMLFEC6GcDGEiyFcDOFiCBdDuBjCxRAuhnAxhIshXAzhYggXQ7gYwsUQLoZwMYSLIVwM4WIIF0O4GMLFEC6GcDGEiyFcDOFiCBdDuBjCxRAu5nFxMT2gGGX4Km_YgcZoQ0FF7IYIMX1sGFxAPxsojIyHdFAY9VCHIWFE4vOs2EM6hMpC7W9m1_2WsqB1nEJx2GVs06B259fjFIo6i3Nf5PzRhzzWUc-2pc9kt-L2MCSMM9sjSBjzCKpHWkd4nPXt9kj34GGc-RnHw6gQx92sFZqZspgPTFw7sdGXdiL7jSdb3cwDCJjtaP7vvvvDxPsXUKrev0Tq6__zDmYwOsu9P7BPJqp-x5Q-vBdyaaD4a9aqVvflq5eXKOVUp3A3eBV_m5gHAJuwWs2WKrKrf6WGbCNI0j7WxoiqK5Uv3XmcIxgxJYtikWC_ah36Iex1VvG68sXuhD_4XrWw2nu9LxzAjCV0PAyYoa39ZFv7cErQOGCm4608C2AmKCJWl6yIuAiL2k_CKMkL-G7OkrwMqyzlUYB17FFRcV7Wfh5HIhNhyrOYB6xMDwXMFBehfxHmPYCZOCrruGYEmCHADAFmCDBDgBkCzBBg5msFzNRRENV5FXM_sMFXxyh1leGJ1qRs5HbcfZU3Hi8uLMuoyNF4iq3uc8zOA3TfQ_ai0WewYbceQzs4O90FXRy5ixu2m1UtY7PgMnnJWTh52wz7TZKL0HlZcX7eqx_OvN_CWxRKvOnSfxBr20O0jf47cIhZ18skL2bYMqhDd2hA9hKm1Umpxf6uIriuFZ5a92knLojjKd5qy5szZZBKIEfpeZR2IlryK_AHjuSVg-_t4A7OcpThsoVbzqDyJ2VFeI0JpK4kAaOEjhVw5r0yRRvWJ1aC6X-dvfx24v1hAaL4BkQC_gXf1sv5rGQlg5cI73qp6rDnID5l2qdZ2HIGmYtuulc2LtzfNt261xHlveCA_MfKK6MLdSm3WmpaiF2-bWCt_UNrEbRC19ZwLTHhH8dTNu8fV-U5rsadb75t5Ff7FrmU7nqB29Dl9tXPvNe6kPJtg0aNWgh_fD11ffX2FotplZoxqUEU0HKjmE2iJbtRuCDW3TDKoty0axMHd1q3bVmgEu3qOyiwJ9itstKZt4lcYbpwfGpEtOm80AJf5imMzNcYXu24gF5b43zdYL6F6z0pVa3cImwJV_80u1UFye__e3iWJel7wnkRzotwXoTzIpwX4bwI50U4L8J5Ec6LcF6E8yKcF-G8COdFOC_CeRHOi3BehPMinBfhvAjnRTgvwnkRzotwXoTzIpwX4bwI50U4L8J5Ec6LcF6E8yKcF-G8COdFOC_CeRHOi3BehPMinBfhvAjnRTgvwnkRzotwXoTzIpwX4bx-UpyX7oGyEkeqwJ8lwEs0H2erRYN3fSqI1yNhc8BHlhnJw1hW-5gp5_safHSlEmNt18ZnUUe63kHlZraFMewTJWmktlhUCxVJkeUh6lKypAkewkTodxejXTcDYKp_XXRfXW2aaSlgc4mpNeGGLueJTzP09EyipfeRLt3UGUZ4jBEK2wqUM0Y8TD5q-7klN-VVoNIvxzGoUt8XcVHiUuRVVhZVHKVZVdZ7r2ILOLX7mMoUcHFTltfzMG7q6Rfh4dwtSymyV7sIfuznED0LeKmOhJ-ItMCYaZomCY-rNK-C2i8zJngmClHkUV0V-E9WBRUTfpByLFtLeJLybPiRethLUXyRJD3sJZCuQZ7XPrGXiL1E7CViLxF7idhLxF4i9tLzsZd8sHuKuEyDLItOZS_tegY6dtw5FAslOYnGRDQmojERjelQGtOfmvnsgyp6Rxv6bWMc8YnqaeiPXhgQgixyZoPxiLdNF8jCijMsV9V1KGpHlShY220rdYcQ5XWAKFDeRIgiQhQRoogQRYQoIkQRIYoIUUSIIkIUEaKIEEWEKCJEESGKCFFEiCJCFBGiiBBFhCgiRBEhighRRIgiQhQRoogQRYQoIkQRIYoIUUSIIkIUEaKIEEWEKCJEESGKCFFEiCJCFBGiiBBFhCgiRBEhighRRIgiQhQRoogQRYQoIkT9pIQo1SnvDYGidn-9g4fa__U2JerVDLvruPeGgcT-EmhR6Oy_Q7tnNYCJutnA6-4wUZvmQ7O4aw4ERZW8CgWXiByX0ROBOypWMvHhgBAWzVaqoO4YPXLhISQHN7a4My0Wh11GF6HNbDS2X3WaIYdFyP2yLB99yHvq9tfacnN2pfI2sTfISGL1fveWci8hy5ntnVFoJtNLzq0tpbrPVI-45BJsm5W6CH9gZvov_2vURrK8c3eeQM7sFxxqhYK2ZtvFjmtXVJrepV6oFjwNKjVbndPzUKpcVJYAmdRJ2zcSmY4rVwvGbcvccTysPCz8gosoycKSsTL0sWK2KkI7ObhJHM6VZSM9zLmiPfRke-hwqJmlYakxXYQ_9pOunoXuFaVhFTI_z8qaZ3WcxkmGTVc89NO8jEXMgyBPkwweg9VFkYswysAjyatEiDj362TgeXrQXnFyEeU9aC-ewtwkVfa1or2KIipTAevBj21-wdmHbp_fiRvIkT4m8LYtf9D_lb324wMNCyaiuKoCYd1PZ_cNeXpHbBunSwXlde9TNX9VKa2u-poL9KmkS2TbzuGZsZhgoiIRpo6CzefTxWoKU3DjEBalG2jQSTJEq9AcunpVlQ93U-kQrLaBPTIG4cYP5ZQOQnewskVVtc25NeVR_LC5elPIZIPv1qBuFoN17-iv9ZdOfbutZFdgSiPky3EE-3pLNEOl2WXlaBgLPPVsZZ4bnkihufDT0snQVa0q9awzHdaB1L0O7Zl35bIx4KnWqsLczl15b1JDSgk6YIwuLuywRz2jhPcdPMOd3KNeyi5p5TddboEjdThOJZZgbV66TiKGTMVSe4j_4heDWeK90NlD2WLr3_WYFkonDbh33_YvDJgn2GablazUkt7bStKXlASdctg8qtpH-WcqxaEdEFX8bxe_XIpyYZzDgpxdNzYy1MrqLAzg6xisNKnEFLueTLWJzDgj2aNVxpG0CTXkwexq3dO5F001b88sqn5QSTduSeKyO1ULRplx2Woms-0-UsIo3hX2dXww-ekOoQZb8IZ9xJJ065lqbprnYtNMRUkloV-itWAQJ4-g6wbgpcqCDGecpsxUFm4MhhoDTO0F4W6CfW-5TKyB6_zI-rnOW7UjGOtfJO4kcSeJO0ncSeJOEneSuJPEnSTuJHEniTtJ3EniThJ3kriTxJ0k7iRxJ4k7SdxJ4k4Sd5K4k8SdJO4kcSeJO0ncSeJOEneSuJPEnSTuJHEniTtJ3EniThJ3kriTxJ0k7iRxJ4k7SdxJ4k4Sd5K4k8SdJO4kcSeJO0ncSeJOEneSuJPEnSTuJHEniTtJ3EniThJ3kriTxJ0k7iRxJ4k7-ZNxJ21hk4rIm8YbFT1oiUr5EJUyzUsRxlmwg6eLTZS2sQNSRY1_lSExObvTmweJeoddRis0na4cVKxmyEVViKRm2aMPeU8Zfy9rblTEdY76BetB0DZCC34hUQ3KQ5t4h1Epndl-gEoppRL3jPaTYzB5NZkw3mdSOvPSf_FXu8gfaanOZEhlDVoE3PHFnZ4udxqV2tmGUVpLcARI6TzH1lvRBaQYiDVVPQMX9ywRyeTqJDwBbGA5bqzR1vCp4xCVQZ76QcVZwDMWs7hM86xivoyn9CIqLePvYUQlbagn21CHc0bHEZUdsfFZEJWwruCOlch5HLEsLpOozoIoKZPKD7OwSgQW69W8SBivorIswiQQSRqFKcPK_KI-HFGZ5BdR0YOo9P0kKlhZfK2IyhpscfAAA5ZFNgrr7EO3JfDEDWQCc5ihc5ICmFJH2NIDYMqYJUkF8yJSW-rg7LkhV_CIzWLeE-YuZCTIHXm1ul-uF7JFBz1JLOAxcWiVYzFX6R5syu4YGtBVBx5WSgAXOf6q645xuFtvBuT9TKk0NcPdyGRVq4xnmOk2WDh7cY4e1rXCTfZ1fOhvthPjjk2xa8BD4ubqdtZgrUrVhYQdtBw-i0aWbbX3GJreqM-IxB_N9uKmqmJqiljh-VVBl4ohojbTnfvrm5XMNQah93JzjbUpuHstzkh8umFY_SUzYqsW405gbK8xWITOjA7rfos1NmjJtwZ6oypyqrV2iXUeZTwQ2hEpShMy71woFVhmOHUtaFDRGN4pKGqtn2_YDH-67ze-fvPyu28uu0SHSgr8QS6wS-_3-kX_RpTrS_zpdybCLBf-SwxoLVZduPf8-5d_voRHma4X68Wl9-ZPv4VPfvf6JfwbHE_4qEYkKoXjqa6NY2PAtlxFL13Hyrp050LfRHtVIykx7U90TsnOEhmlZb7UFpmzTWTd8EYSJtla7SLYwzeLOW9tMKjzU2U2dWKLYbZqArpNK1-0ux9AuUnOrS3SM-67aSu7llHKtdloHm40tY90rLTt6-rYdUrfbJNX5Yyqh5OGnZJ2tcEkYVPL7OOMb5hKWC8aWfmEGFvdaqyCJPW9Br8qEeOUp87-xjTUzKXQGFPXNajH0Za7iUPXLscd_FHM1_c2xdOPs3wQd0GkZSItE2mZSMtEWibSMpGWibRMpGUiLRNpmUjLRFom0jKRlom0TKRlIi0TaZlIy0RaJtIykZaJtEykZSItE2mZSMtEWibSMpGWibRMpGUiLRNpmUjLRFom0jKRlom0TKRlIi0TaZlIy0RaJtIykZaJtEykZSItE2mZSMtEWibSMpGWibRMpGUiLRNpmUjLRFom0jKRlom0TKRlIi0TaZlIy0RaJtIykZaJtEykZSIt78KSv3KWsgyFdCzlSj7ZYSTlR6KogqMs05I9StjcyUFtuXc6jAn28J360cX7dGHn-y69GPQZSmmuK1pcrq_tNwchIBBfh7CSID4berpHvlE0wCp-3V1Il1zuX83qY2m_gaI-ijdclXEYVkEal1kQxBXW0YeRqijt5Q1bYOvDvOGvadkdTmm2QFx7tR3Gb4e8fRbGLwwyLpMiCzAgFSbCDzjjUch4mRYiD1ORZQFjCY9TvyziOhNJlZR-lIIlnQacs-FH2sb8Rm8C_8KPLsI-zG9a5zwrg5Qwvz8J5jfx4zKHV8-ivCTML2F-CfNLmN8-VKMppmW_AN7vX74JCu37fGMsKGmMm6Cts8UIB_wzxQHHBY9EneUBGAWEAyYcMOGAf3Ic8JaO-Zq5wKBgkon3TZDiv7JRVbMDKcUaS70oHwUljDN16TCqFMRQbYGZVEuzamrDCGpeZcW0fGbLRpA1kHymDT1MIoKQaNUoZPvjAG1YZwh1gFPV1W5TOB0yMYGFCSxMYGECCxNYmMDCBBYmsDCBhQksTGBhAgsTWJjAwgQWJrAwgYUJLExgYQILE1iYwMIEFiawMIGFCSxMYGECCxNYmMDCBBYmsDCBhQksTGBhAgsTWJjAwgQWJrAwgYUJLExgYQILE1iYwMIEFiawMIGFCSxMYGECCxNYmMDCBBYmsDCBhQksTGBhAgsTWJjAwgQWJrAwgYUJLExgYQILnwoWvroRzS2aK78IsrDTQeSAVw9s9jsK8epU37l3Oqzk9lSysPN4g8DfV8p9sq1pXdMiYiBU717TVZg0ILRA9uAaNnRK3bUPAuJs6JEPv7vEFZx26z4Asb6-Ln2SaqfjDcNdtOlp76H6H6ZGwnXXP45KnNQ1K1mUxlGQV0WZJLXgfig7IXqpxJYv-zCV-GtasoeznB-kEneE3mehEhdRVPEo4CEvgyAPU5bFdRlGYZwHIs1Y5Jd-XdVpKoJYgFUblIUofRbHZRJnRRnyI6jE4YXvXyRZD5U4DJioMk5UYqISE5WYqMREJSYqMVGJiUpMVGKiEhOVmKjERCUmKjFRiYlKTFRiohITlZioxEQlJioxUYmJSkxUYqISE5WYqMREJSYqMVGJP4tKXMcZC5NIsJBXB1OJVaHL7NbgVMzIXnVmqpKhTrELVvux62uQOii2rLWn3VLthe5uaPT1PhG5mMjFRC4mcjGRi4lcTORiIhcTuZjIxUQuJnLxF0ouZlUVMob-bFEdTC7e9ajUVpJ1FA6Z9Ut1rohoTERjIhoT0ZiIxkQ0JqIxEY2JaExEYyIaE9GYiMZENCaiMRGNiWhMRGMiGhPRmIjGRDQmojERjYloTERjIhoT0ZiIxkQ0JqIxEY2JaExEYyIaE9GYiMZfC9H4ZgPvuyMab5oPzeKuOZBp7CAoHWzrgYTMowCxTuPfE6NonZ4L95kOawQ55U7siaC3zp2cXsXuTt0VVJQXL7BU1KfPbGbsqWcyI3FaBQ8dyef0Eo7MidMpePicnN5KODInvZjlh-fk1Da_sRXZNcEdPiend8mNzUnXuXbMnJza2jY2J13r2uFzcnpv28icOP1Xh4_k9AatsbfTdU99zi4-tL1qDBzedU8dPient1c9OCc-O3XFHtncNDInTuvS4XNyem_TyJw4TUPHzMnJXUUjk-K0Bh0-KeO9Q-bSTsPLUdr1xI6YkZE43SWPoV0faj8Zszi61pIjp_uk3pOROek9WuCztOtoy8fYEuy6HA6fk9PbIEbmxOlIOElWHdmyMLZOuo6Ew-fk9JaFMVnVdRF8pqzKPldWOQ0DRyj6sY6C_jNbHOLz4KkpIAN01MjyU7V-NoEME2Jodf1Lh6veoarXkp-kCEuLZuAUFXW_-wPvpln50-0bqcoVFUyTlzDJURMJQwtnZYYr82TbMcqzo05gYSF2NNV1WFVJHcVRWos0jnM2dAKLPUvj4RNYyMEmB5scbHKwycEmB5scbHKwycEmB5scbHKwycH-8hzsw8_l7DmOMZ7Yu16E0Y_9Ry8-y3GTeclhwcS1EGEGS9jPRZnzIoiC2q-yNC6qjEVBkJRxkmdJGOCZlGURVH7A61Sfs3HI8_WcPRkWF37f2ZNlVKV1kRd09uRPcvYkz-H1JkkVRhmdPUlnT9LZk3T2JJ09-XM-e_LSjaurs8qGYvnuwsQeN8HkaQqq1F9G8tXbtJWqdKwlHWtJx1rSsZZ0rCUda0nHWtKxlnSsJR1rScda0rGWdKwlHWtJx1rSsZZ0rCUda0nHWtKxlr_cYy05aKYwFVkdFeGzHGuJUP6v5mDK8cTWkUdLquMKfj6HQ-5F5H7JxzvKk4C-vAMad4Jtn3PEIo7s-Q5J3EPffImHJPIqLEQWZCzJiuc6JFEvkC_kmMN-AXjaQYVSxHw1Rw3u7LzPOyyw2y1fy3F_g6yWxz2wD0fWW9W7d8Loz-bIvSD1WVYkiSh58VxH7mmj7Ws9NG_cjDv62Du76L6mg-setPbo6Lneo-fkaW9f8OFxO3rqs45_03rgizvAbVDZPNoRbNIqOwziSIeo0SFqdIgaHaJGh6jRIWp0iBodokaHqNEhanSIGh2iRoeo0SFqdIgaHaJGh6jRIWp0iBodokaHqNEhanSIGh2iRoeo0SFqdIgaHaJGh6jRIWp0iBodokaHqNEhaj_fQ9T60f_OTR8N_W87eT_3DIDfzhpVPuFyinpJ_9IuwnI-KVxuZ9e4rLXHukf91zrEIP_BdIPBH4f6z6Laj9Ky4EFaZqGI_LDMBWODqH-LLvzJUf8_HHNsQQ_AMfixH8n4LEzKkNdx5teJX0ZRnAeFHxZZFFc8gZ-xJI2KlIug5EVQR0UUxzxOoiKMkiqAd5XEEk078Eg9GMrIvwiKHgxlDLfO6iIiDOVPgqGswtwPioIVPMkJQ0kYSsJQEoaSMJS_BAylY1cSj5J4lMSjJB4l8SiJR0k8SuJREo-SeJTEoyQeJfEoiUdJPEriURKPkniUxKMkHiXxKIlHSTxK4lESj5J4lMSjJB4l8SiJR0k8SuJREo-SeJTEoyQeJfEoiUdJPEriURKPkniUxKMkHiXxKIlHSTxK4lESj5J4lMSjJB4l8SiJR0k8SuJREo-SeJTEoyQeJfEoiUdJPEriURKPkniUxKMkHiXxKJ-NR_nDj_8fF68Z4A)
