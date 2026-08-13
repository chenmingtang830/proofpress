[//]: # (ob:c26ac4be)
# Related Work

[//]: # (ob:d9502ea1)
## RW01: Handoff Debt

[//]: # (ob:05c49886)
- **Type**: baseline and boundary.
- **Source**: https://arxiv.org/abs/2606.02875
- **Contribution**: Measures rediscovery and takeover efficiency under several predecessor-context views.
- **Delta**: Freezes repository state at takeover, so it establishes handoff debt while excluding independent post-handoff artifact change.

[//]: # (ob:f38a0111)
## RW02: AgentAsk

[//]: # (ob:52e9607e)
- **Type**: failure taxonomy.
- **Source**: https://aclanthology.org/2026.acl-long.1294/
- **Contribution**: Identifies data gaps, signal corruption, referential drift, and capability gaps at inter-agent message boundaries.
- **Delta**: Repairs message ambiguity through clarification rather than binding inherited decisions to an external artifact revision.

[//]: # (ob:897cf011)
## RW03: W3C PROV

[//]: # (ob:019a1aaf)
- **Type**: imported provenance model.
- **Source**: https://www.w3.org/TR/prov-overview/ and https://www.w3.org/TR/prov-constraints/
- **Contribution**: Represents entities, activities, agents, derivation, revision, usage, generation, and invalidation.
- **Delta**: Supplies revision identity and lineage semantics but not an agent-handoff admission policy or behavioral evaluation.

[//]: # (ob:47987ae5)
## RW04: Software consume-time verification

[//]: # (ob:a030095a)
- **Type**: mechanism precedent.
- **Source**: in-toto, TUF, SLSA, Sigstore, OCI descriptors, and GitHub required-status checks, as indexed below.
- **Contribution**: Conditions artifact consumption or merge on identity, provenance, policy, freshness, or validation against current state.
- **Delta**: Applies mature admission ideas to software artifacts; this study tests their behavioral use at an agent knowledge-handoff boundary.

[//]: # (ob:0ef2f001)
## RW05: Portable and provenance-aware agent memory

[//]: # (ob:1db27cf6)
- **Type**: closest agent-system precedent.
- **Source**: Portable Agent Memory, MemLineage, StateAuditor, and ProvenanceGuard, as indexed below.
- **Contribution**: Adds content-addressed transfer, ancestry, chronology, attribution, repair, or action gates to agent memory.
- **Delta**: Does not isolate the same readable handoff under independent external-document replacement and measure receive-time unsafe continuation.

[//]: # (ob:877c488a)
## Review status and method

[//]: # (ob:f3c33000)
This is a structured primary-source scoping review current through 12 August 2026, not a PRISMA-style systematic review. Searches covered arXiv, ACL Anthology, OpenReview, official standards and project repositories, with index searches of ACM Digital Library and IEEE Xplore. Query families combined `agent memory`, `obsolete/stale state`, `knowledge update`, `handoff/takeover`, `cross-agent transfer`, `artifact version drift`, `provenance`, `admission gate`, `shared-state consistency`, and `benchmark construct validity`. Included works had to evaluate inherited or evolving state, define artifact/provenance verification, or supply benchmark-validity guidance relevant to the claim. Secondary commentary was excluded from the evidence table. Remaining limitations are incomplete backward/forward citation chaining, weaker paywalled software-systems coverage, no patent or non-English search, no dual-reviewer screening, and rapidly changing 2026 preprints. The review therefore supports a scoped novelty boundary, not an exhaustive `no prior work` claim.

[//]: # (ob:ac488866)
## Review synthesis: the broad ideas are established

[//]: # (ob:c84994f8)
Prior work already evaluates obsolete memories and evolving state, agent handoff and takeover, cryptographically verifiable cross-agent memory, provenance-aware action gates, and consume-time software-artifact admission. Proofpress should not claim to invent stale-state evaluation, agent handoff benchmarks, content addressing, cryptographic provenance, artifact admission, or the term `artifact drift`. Its defensible research object is narrower: an information-matched predecessor-to-successor handoff in which an independently mutable external artifact diverges after admission, followed by a receive-time deterministic binding check and measurement of unsafe continuation.

[//]: # (ob:5e4d5266)
## Closest agent-memory and handoff work

[//]: # (ob:0e061db7)
| Work | What it evaluates | Relationship and remaining distinction |
|---|---|---|
| [Keep Me Updated!](https://aclanthology.org/2022.findings-emnlp.276/) (2022) | Updating or removing outdated conversational memory | Establishes obsolete-memory management; no external artifact revision admission. |
| [LoCoMo](https://arxiv.org/abs/2402.17753) (ACL 2024) | Very-long conversational QA, temporal and causal memory | Tests retained information, not whether inherited state is bound to the currently open artifact. |
| [LongMemEval](https://arxiv.org/abs/2410.10813) (ICLR 2025) | Extraction, multi-session and temporal reasoning, knowledge updates, abstention | Includes updating and stale-fact pressure; does not manipulate external artifact identity. |
| [STALE](https://arxiv.org/abs/2605.06527) (2026 preprint) | Downstream action when new events implicitly invalidate old memory | Strongest stale-state benchmark threat; relies on semantic conflict resolution rather than explicit revision identity. |
| [Memora](https://arxiv.org/abs/2604.20006) (2026 preprint) | Longitudinal personalized memory with penalties for obsolete or invalidated reuse | Evaluates stale reuse, but not an agent-to-agent artifact-admission contract. |
| [HorizonBench](https://arxiv.org/abs/2604.17283) (2026 preprint) | Evolving preferences with ground-truth provenance | Uses provenance diagnostically; the receiver does not verify an external work artifact. |
| [MemoryArena](https://arxiv.org/abs/2602.16313) (2026 preprint) | Experience from earlier sessions driving later agentic subtasks | Couples memory to action without a matched clean/stale artifact handoff. |
| [StateAuditor](https://arxiv.org/abs/2608.01619) (2026 preprint) | Deterministic quotation-provenance and chronology checks followed by repair | Very close mechanism pattern; concerns personalized-response dependencies, not post-handoff external-artifact substitution. |
| [Portable Agent Memory](https://arxiv.org/abs/2605.11032) (2026 preprint) | Content-addressed, Merkle-DAG, capability-controlled memory transfer across model families | Direct prior art for cryptographically verified cross-agent transfer; does not isolate stale external-artifact continuation. |
| [Handoff Debt](https://arxiv.org/abs/2606.02875) (2026 preprint) | Coding-agent takeover using repository state, traces, summaries, or structured notes | Direct handoff benchmark prior art; repository state is frozen at takeover and outcomes emphasize rediscovery, cost, and completion. |
| [MemLineage](https://arxiv.org/abs/2605.14421) (2026 preprint) | Signed memory entries, derivation DAGs, verifier-aware retrieval, and sensitive-action gates | Direct provenance-enforcement threat; gates poisoned or untrusted ancestry rather than a legitimately modified or superseded artifact. |
| [AgentAsk](https://aclanthology.org/2026.acl-long.1294/) (ACL 2026) | Error propagation at inter-agent handoffs, including referential drift | Establishes handoff-edge failure analysis; does not enforce revision-bound artifact admission. |
| [MultiAgentBench](https://aclanthology.org/2025.acl-long.421/) (ACL 2025) | Collaboration, competition, coordination topologies, and milestones | Covers multi-agent communication quality, not persistent artifact currentness. |
| [Anchor](https://arxiv.org/abs/2605.26321) (2026 preprint) | Preventing disagreement among benchmark instructions, environments, oracles, and verifiers | Already uses `artifact drift`; its object is benchmark-generation consistency, not handoff-version drift. |

[//]: # (ob:a7a3a721)
## Provenance, versioning, and consume-time admission

[//]: # (ob:a1be6cea)
| Work or standard | Established mechanism | Boundary relative to this study |
|---|---|---|
| [W3C PROV](https://www.w3.org/TR/prov-overview/) and [PROV-AQ](https://www.w3.org/TR/prov-aq/) | Entities, activities, agents, derivation, invalidation, and provenance retrieval | General representation and interchange; provenance records are not inherently authoritative and no admission policy is supplied. |
| [PAV](https://pmc.ncbi.nlm.nih.gov/articles/PMC4177195/) | Lightweight provenance, authoring, curation, and versioning for web resources | Direct prior vocabulary for versioned knowledge artifacts. |
| [in-toto](https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias) | End-user verification of materials, products, actors, and supply-chain steps against a layout | Mature precedent for artifact consumption conditioned on provenance. |
| [TUF](https://theupdateframework.io/papers/survivable-key-compromise-ccs2010.pdf) and [Mercury](https://theupdateframework.io/papers/prevention-rollback-attacks-atc2017.pdf) | Signed metadata, version and expiry checks, rollback and freeze protection | Mature stale-version admission precedent in software update systems. |
| [SLSA artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts) | Consumer checks artifact digest, provenance, and policy expectations before use | Very close consume-time admission model; applies to software supply chains rather than agent handoffs. |
| [Sigstore policy-controller](https://github.com/sigstore/policy-controller) | Kubernetes admission from signatures and attestations, with image-tag resolution | Demonstrates that mutable names must resolve to the same admitted immutable artifact. |
| [OCI descriptors](https://specs.opencontainers.org/image-spec/descriptor/) | Digest-bound content identity | Proves bytes, not whether that revision remains authorized or current. |
| [Software Heritage persistent identifiers](https://arxiv.org/abs/2001.08647) | Intrinsic identifiers for archived software artifacts | Supports independent identity and integrity checks without a currentness policy. |
| [RO-Crate workflow-run provenance](https://www.researchobject.org/workflow-run-crate/profiles/) and [ReproZip](https://www.usenix.org/conference/tapp13/technical-sessions/presentation/chirigati) | Portable workflow inputs, outputs, code, environment, and replay provenance | Establishes reproducible artifact packaging; not a receiver admission experiment. |
| [PROV-AGENT](https://arxiv.org/abs/2508.02866) (IEEE e-Science 2025) | W3C-PROV extension and MCP capture of prompts, responses, decisions, and workflow context | Agent-specific execution traceability without a receive-time artifact gate. |
| [ProvenanceGuard](https://arxiv.org/abs/2606.18037) (2026 preprint) | Claim-to-source attribution verification with block, repair, or reverify | Enforces source attribution, not whether an admitted source artifact has been superseded. |

[//]: # (ob:218ed699)
## Benchmark validity and interpretation

[//]: # (ob:96041c8c)
| Work | Guidance applied here |
|---|---|
| [Measuring What Matters](https://papers.neurips.cc/paper_files/paper/2025/hash/1967e0fc3aa6cbbace562f5cb8e3954e-Abstract-Datasets_and_Benchmarks_Track.html) (NeurIPS 2025) | Make the phenomenon-to-task-to-metric-to-claim chain explicit; sample representative tasks before external claims. |
| [Evidence-Centered Benchmark Design](https://aclanthology.org/2024.acl-long.861/) (ACL 2024) | State the capability claim, evidence model, task model, and excluded phenomena. |
| [The Benchmark Lottery](https://arxiv.org/abs/2107.07002) (2021) | Task selection can reverse perceived superiority; designer-authored fixtures require independent sampling. |
| [CheckList](https://aclanthology.org/2020.acl-main.442/) (ACL 2020) | A targeted minimum-functionality test can validate a specific invariant without estimating distributional performance. |
| [Contrast Sets](https://aclanthology.org/2020.findings-emnlp.117/) (2020) | Use local label-changing contrasts to test the decision boundary and reveal artifacts. |
| [Dynabench](https://arxiv.org/abs/2104.14337) (NAACL 2021) | Human-and-model-in-the-loop adversarial collection can find valid cases that the current system misses. |
| [SWE-bench Goes Live](https://arxiv.org/abs/2505.23419) (2025) | Fresh chronological tasks reduce contamination and benchmark overfitting. |
| [tau-bench](https://arxiv.org/abs/2406.12045) (2024) | Grade final environment state and repeated-run reliability, not persuasive prose alone. |

[//]: # (ob:d0da681a)
## Scoped novelty and non-novelty conclusion

[//]: # (ob:d96b6d09)
Content identity does not imply currentness: a digest can establish that an object is revision A without establishing that A remains the authorized revision. Existing provenance and supply-chain systems already separate immutable identity from a policy-controlled decision to consume. Existing agent work also covers obsolete memory, handoff quality, portable cryptographic memory, and provenance-aware action gates. The contribution here is therefore not a new provenance primitive. It is the controlled joint evaluation of post-handoff external-artifact divergence, semantically information-matched handoffs, deterministic revision admission, and unsafe-continuation behavior.

[//]: # (ob:c7970100)
Within the primary-source literature covered by this search, no evaluated work was identified that combines all four elements. This is a scoped search finding, not proof that no such system exists. A submission-grade systematic review still requires frozen database queries, deduplication and screening counts, explicit inclusion and exclusion records, backward and forward citation chaining, venue/version refresh, and ideally a second reviewer.

[//]: # (ob:a7681fe0)
## R01: Harvey LAB

[//]: # (ob:5152bcf5)
Harvey LAB provides legal-work tasks, an open-source execution harness, model adapters, task result packaging, and evaluation rubrics. It is used here as a task/harness substrate, not as a claim that this wrapper reproduces Harvey's published leaderboard.

[//]: # (ob:f6b950f4)
- Source: https://github.com/harveyai/harvey-labs
- Architecture: https://github.com/harveyai/harvey-labs/blob/v1.0/docs/architecture.md

[//]: # (ob:502e7400)
## R02: Scaling agent systems

[//]: # (ob:9b6cacb9)
Google's study distinguishes a single-agent system from independent, centralized, decentralized, and hybrid multi-agent architectures. The accepted baseline here is therefore described precisely as a **Google-taxonomy centralized hub-and-spoke** architecture: an orchestrator delegates to three parallel specialists and synthesizes their artifacts while workers do not communicate peer-to-peer. Its mutable `coordination.md` is our conventional communication protocol, not a claim that Google shipped that file format. The study reports multi-agent degradation on strictly sequential tasks but gains on parallelizable information-gathering tasks; that motivates an M&A fan-out pilot and retaining a budget-neutral single-agent arm rather than assuming decomposition helps.

[//]: # (ob:b0795eb4)
- Source: https://arxiv.org/abs/2512.08296
- Discussion: https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/

[//]: # (ob:f45a798f)
## R03: Agent-Native Research Artifact

[//]: # (ob:a30649b6)
ARA supplies the research-management structure for this study: logic, source artifacts, trace, and evidence. Its current-state and append-only separation informs how the paper process is recorded.

[//]: # (ob:213a8475)
- Paper: https://arxiv.org/abs/2604.24658
- Implementation: https://github.com/ARA-Labs/Agent-Native-Research-Artifact

[//]: # (ob:4fd097c8)
## R04: Model transport and sampling source

[//]: # (ob:2686316a)
OpenRouter is a transport/routing layer for the fixed Harvey harness, not a second evaluation harness. The study freezes concrete model slugs and provider routing to avoid silent model/provider substitution. The Chatbot Arena Agent Leaderboard may inform a broad candidate roster but is not evidence about legal-work performance or provenance.

[//]: # (ob:d4a8d92c)
- Routing: https://openrouter.ai/docs/guides/routing/provider-selection
- Latest-version semantics: https://openrouter.ai/docs/guides/routing/routers/latest-resolution
- Model metadata: https://openrouter.ai/api/v1/models
- Candidate sampling source: https://arena.ai/leaderboard/agent

[//]: # (ob:0db501c8)
## R05: Provenance interoperability

[//]: # (ob:4e561fc3)
W3C PROV defines provenance as information about the entities, activities, and agents involved in producing an artifact, and provides a model for describing and linking provenance records. It is prior interoperability infrastructure, not evidence that Proofpress or this experiment invented provenance. The restricted-access Lease track instead tests whether a portable, artifact-native declared lineage is useful to a fresh receiver after a workflow boundary.

[//]: # (ob:8cebbd8e)
- Overview: https://www.w3.org/TR/prov-overview/
- Provenance bundle links: https://www.w3.org/TR/prov-links/

[//]: # (ob:5f138b72)
## R07: Matched artifact evaluation precedent

[//]: # (ob:0dbf1a9c)
ARA evaluates a structured research artifact against PDF-plus-GitHub access under matched model, task, tool, and budget conditions; its reproduction evaluation masks expected numeric results and uses blind requirement-level judging. This is methodological precedent for treating a representation as an evaluation object and for condition-blind task rubrics. It is not direct evidence for this study's access-discontinuity claim: ARA exposes its full `logic/`, `src/`, `trace/`, and `evidence/` package to the receiver, while the restricted Lease receiver cannot recover Agent A's source bundle or private process. The Proofpress contribution is therefore a portable provenance-bearing artifact handoff protocol and a conditional evaluation design, not a claim to invent provenance or artifact evaluation.

[//]: # (ob:2cb415a6)
- Paper: https://arxiv.org/pdf/2604.24658

[//]: # (ob:2c3fe1b7)
## R06: Dynamic access and handoff boundaries

[//]: # (ob:8a2ef79d)
Agent-memory benchmarks often evaluate retrieval or state recovery inside a continuing stateful environment. The Lease track instead conditions on a receiver losing a particular source-access path while retaining a delivered artifact and conventional handoff. Dynamic authorization and revocation are established operational patterns; this supports an access-discontinuity scenario, not a claim that organizations normally discard source records. The study therefore distinguishes artifact identity/integrity and declared lineage from verification of inaccessible source truth.

[//]: # (ob:91e5a727)
- Dynamic access architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- Organizational information retention after termination: https://csrc.nist.gov/CSRC/media/Projects/risk-management/documents/overlayRepo/Electronic%20Physical%20Access%20Control%20Systems/ePACS%20Overlay_v1_SP800-53rev5-April2021.pdf

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2FlZWY3NDRhYjQ2MTE0ODkyMjI5ZWJhYiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQ4NjMxZDQ3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82YzdmYTdmNGI4NTliMWRhNWZjYmM2ZmUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2I2ODJjZmZlMmNmYjEzNzRlY2I1NTJlYyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfXl33Ma151fBaM7Me_H0gn2h_mIoxfF5UqxIyss7k-cjFwqFJqLuRgdAk2Jsf_e591YVUOgFpETa4ySVc2KRTXShlrv87lo_PGNNV5WMdx-q4tnFs93uAxOiTMKQ5WHseWGa-b6fiZzlz2bP8rq4-1BUK9F28Gx7zfwovgjCvOBlwllcBBHzYlYWfpb6bpYz4fmRVxShlySpL4Ii4gH34rJkIXPL3PfLLCpDGLeoWl7fiObu2cUP-Ev3oWMreMNWfOrgz2uWizX8-p-iqcqK5WvhNOKmaqt661zD03Vz5-R3zpumrstdI9oWvrNj_CNbCVzS6OOm_quAxe4bHPC663btxXK5qrrrfb7g9WbJr8V2U21XHduu0sBdjr7diL_tK_j5w74VzQdeb1uxhZ3omr34afbsWjDcwjCNA68Ik2fykw_ihh6CrRUfYp6ULCnDPI2y3CtYVPKcx6XAmdVNh0v7sK62Amauz2P9IY9Tn5elgP_kXpCEgudR5Asul6Nm94GzXbtfw4J9nCevm6J9dvGXH56p1__wDM64blr8Sf5ZFB9y2PC_PNtvP27r2-2z72ANmhrg1axhy3W9qviyEWvWweO3dfNxsSmezT6LaFjXNVW-7-C0PuSsrVokHbEuP7AWdhHGxWf23XXd4Nw-Vlscsr1rO7GBv2zZBg9Rz3EGX23x4J9dbPfrNcyYX8NJCbnWfF3zj_A092PGwxy3FQ6pQyq6ePZWrsL5M6wC_qBexIqCZrBDihK38Mn_dA6e7O52OAU8TCCMZz_NhhexJE69UrjjF7nehfN71tyIO-fV5W8n3wUvO3p64n2RF_k5L6Mvfd_wlAOkc1MVonXWYsXWczxbp2Ptx3bmsK1T78R23tb7hgtHfBIcjm-Y2Q5IYzStMs6zyCVW_qJpzZ139KoL5wRHXtMQrFI_zEEatP-9nTuXDb-uOmIDNa81yILxdrm-SEL38Hj8C-cdZ8BnKwcYbds5ktrae09q4osTh5blMWc8z55gFl_X9Wot_q112m5f3Dl1Kb86l191mNqSbg8iwdnUXXUDhNw6ZfWp2k6cX-4mWSTy8AlmeHyUrPlU3SzqZrWEg1uCQvAXbupnMZ7hCxD8e-Jnen7iKMswYkmWlgdTDC6cS9qBPzBYrADWbQXuAlCHEmT3nelDRpiSAIEbh3DCTzmvy7eXTrsH0V_B2XXXqO3kt-cbtoWT2NBZgNahg3bKuoGnKkkUE6fsewFLwyR6yqnOnTdsJ5qzpx274cIP4yjF0_5ms1vT5FlHJ3543N_NtLZ6BmAAqeIDbwSTKoL-ovWN-OBnrseiMI-8OOKxG_hJmWc8wSe3dUfrVwrVUQrVAdXOP-7qatsRPmjoTahF9G-oRL5DTbyu-J0xgqmdjUFI73-h4m7rsvtQAjGJZtdUCh-0uXdRekIEjAdx4QmPAZLw0zKOGOepcMO0FNwFamOxCyiCuTnsQerDmbjwQ-jmacZwbNhf0vPyuC48F9QkfvLMd_147qZzN37vJhdBdBEG_8d1L0hAqh1H7RklRZLwAIhn-PSHnwMaEGVK1X3N2mt4PkhEFCdhmUduAA_QGIY2V0T7EBWtBkyTJHILD3ApURENaGhtPeAD9bAa1A89UMMgkAqX60EN1awGfYyyRWTLmi1gnRnI8UKsHVawXQenMaMvokjYrztHwlyYHg5UOOKGrffEXU6zz5uKtwvnm84B2QCItXCuBYgL1jqMxliqN4CsyUGawH7OHOAd-QBfs2oDYoV1UrbcNgzYroH3wlqKPYe1yPWBMtrtc2Dga3jBGvZKNHnNmmJxQhKp7SvANihD1y_8sN8-A0Ko7XsUKEDB-OAvLoEO8-WNt3CXRc3bpalGJVEfaiW1kBjYMSmTgEVR1NPBgDlM4vo86KDGz1zXZ0kUxGka6vENNKHGfwwoWDn1FiQjPN7A5P4OR2g-7uQClAuQjIbw-Py-g31ExVQDmQD4LuqyJLIQrRbtRHRFDQ8hPYG1yIhANDkJRz3sICOU6_rWua3Wa_oNXtkBmU9Qj8jSzAuzTLhprDfFADBnqeczcAg9r5XuYkX7i0SyWnb1LdB2O2fzlldiy8W8LuFHOti5ue3t_BYsyTlsD_xwd_gnWOjyPFnxLA6FcFkWlHnPHwP-McnqC9GLehEI-jzKCy8qStYLxwHQqBc9Bo7cXTikKGaOkm9aPaAcaxgXWm6BdITdRMJpHb5vGtouoCZBf0fZAztZb9d3TiuQIkjGVVt42aZ1roGCiKwQi6Cw5SjWYAra0p0kJxbkvs8F45neAwMp9eT0CJxzQgzBns5f4TfN05vr05sfn55CSD_hzE-Y9KKout6gvwKF8enZd-QeQFF99PmBA8D4_G974Nb-D28rsK6bwnkPJvYv6R4Q25uqqbe4hR_g7zSlU14C4qrBSSDXYbgIcANgrxjyqZJU892abecDEHp2xoUQlqClEp4egOXwwnlN6hiId9si9CP6bBkcOUpHSeX3Gh0PHmbC8vBjdDTF7Mln-C3w2lsQ88BKFWEFPdCyqaUOWLM7-KNkdIGKBPSGRAMT5kcRsrTIfP7k8507b-W8Bk5DRNXQEhag6kmpr_YIwPQSlgqRnTBBCPmcJYaDWShb40-taOYgpJDcQJp9AlFRIfXO4ZXVauvsdwWwyOLc-T3doMYmP3LQ74xj-uEZ6DD48oua70na47HvRyMdc5oxuCMHv0AtUcOZbsQGfbY4flOvZ0BmtYTzG4G8WLUbp6jYalu3HaqO63pTA6eLet86BnFKXNwJtmmlFgF9saJFaQi9QqCDG_Rwu7L0wdQIReBHge-lXlIUEQ9L8ubKHTQNRtNYMo3IH6xIsSLl0KvxIN_Foe0e_HTaMr_PTfEkvoggTKNIxAXLyzws_Ngv4zhyeZL5oUjcULAod-HXuPABPKXcdTPulVHq56GXJaEXn1nPkSsihTddhO4JV0QuXI-HHrOuCOuKsK4I64qwrgjrirCuiF-FK2KYduCHhfCy0vcGGjGwrkkjjwGp6m2MCbcMEj8APNJv0oBb1dseAzgHdUcqCE4ZwOVIoakHFs57-KoUdWUjxN-BKOFRsC2AVqSqbNf7VUtrVHoX1JaaAAqtm7qC1VdrJFv6wrJ_jDRh1e2lEMMXXYHIymFGl0CRTPKa82rQcs6G3SkyhEnnTc0Kh8ObKzTo4K0tbgZITtwQkoWK0B2Ww4xMOADUhaOgMefUjWHaTdBulBaAEwEqeYSA6VgMeN7T7pfj6mbeijUoA9gPpOxXqDm6uUKFcEgwX7AW288ZWf61Xa7lWCBM6vVev0AS6kZ0AHc6dm5YtqtAXS_p8EjtX_VbfkDVJsPCduKXDYyy1L6sX6u_b7Dm2-VAER-U1l3-GtyB13uggS_NGfriLA04-qqsxFHk_bQryXjN8feVj-bdTnD6yJF4at6xT_W23tyN0BHsjkAzT0pQmCA8KKcoVRJbn3PjvFXkQJKPcS52aL8Uyrkz30r9_UKI3TshPoKMXAMumu939Cb8DgiMLX4fjEW0GYXULgj3QKGAwunICwN_g0nMW2A5zhotXKW18JleGZ5GPBcZUIwbFzGPmRdFqcj8c16Z3m683yvzc5z7w31KvX3cj3bh_XTaAv5FTP7ULRHhx54fe0masTJIYd9ZygH7536csDjlYLpzLwGedXnopwWgw6iICp-7WVacX9LY6k_Q6o-SC_9UAoLHAD6UUwkIv5Awsk4B6xSwToEJoy30E8a9lOV-8WCnAOZ3wzh7PBE8yZHqUo6Csqk3oF0KgbYWfD4zNd_MAYVi_oqUdX0H5AQYGIiuUmONvA0SQvfKrleeRHIVGZON9DAAG3CAIBTTAD0Mz91Jkvvqqyl1DAdIJjZYGR_FV1-N3n5BXAQfCKJjwNTAMYKiE1J7323h_W2FBsTtNZgD5H8AZgKlTCQPlLHZbyuOsHInAAp39Rz_lUbqZi8T3b7nNej1aisdH5vie1wY0CgaJaiRCBQYYyEbArd0NccgjDR2DL6Sq3Xa6wo4q5CflTg5Mg460_ph67ZG1gNd1MoHzYMwp4UmCax-1QAjAmgH_AnzglkpaQOr59c4bUAqBDWwBAAsGwCFnxwEGtUWjyLfFyvRgdHfcWTrEQkxsH9gk-E8cSZbOLt2jxn9SDWATuq2kuJLrHet9e1Y34717VjfjvXtWN-O9e1Y387P79t5VW0_9o6dcYSrZ1qQHvia9Rpo9PX_vnR21bqWwvTd5TtQNiVAVeLY-7074ySdK3d55S2v_F49al_PUDp5nLVDL65AXyrQtRV7BL39FOevYVIqlecz3TrM9yPgEu4G8E-c5HEC_4RJes6t0zsGfhVunQmn1L1uncHF8Yu4dbgo44LHRcg9lnDmibAoPR5m6Mzgngji3PeKOOURi4UXijSMwtDNBMtY6rqRxz_DrZNdRP6Fl55w68QszfMgtm4d69axbp1fs1vHBe73E5EK4eXWrfNlbh3Q4d012A2DJm8xqsPwLI-dPvBD1QxG6z-mE0j7f8zDkp4eFR7aovle8Y6s67Hnh4yXFXl3cD5qz6q_05Kk4UODzFfk2SEbC7_3XHmb-lQiOBGETCXbztHyGaCTdB4RIxwiGes-su4j6z6y7iPrPrLuo38y9xE_4z7iZ9xH_Jz7qJHuo-4f03t0UCjIDwsFJ3xHLigf1zuq2oku0Gmi1ioTYeD0G5ZX66q7u7da596vT1TphGCretIL8jQz-nNw5bx5--1_AsQpATy3BlsjRDbglxIIKBYRvXWVmKjOSbnI8yIVTzbPufMt8DT-MjDM7e3t4jYgFff-LZHfvFYPLZHn-ldN9JbxeVCCqZMcTDS-cF7cAcVUnAyMVgprnWZOOVCsqe496ocNI-5pIpQyHziDEmyedo5StauKvByk_vWGNQDI67ITW63ZEE0B9-FvKPYl5GmmDj_zBEBB_-n3dH40wEnbm7cNX2zhpAEY3yx3oDGX7e5h1Z4Gx5-uobzEX00mOSRiR0k6suAW55j39ODvJHCkF1Sw18SYwIINM8Ar2tHEhL3oJZtu20vIxTlOPP3S3meMosBYmFRP7eIcu0ztT3H2nOfqnKf2yaD30y_5rcpB1DmMbTunNoIglrZ7PIOD5ER8_w01EFRGL5384hzR3rNPf_jm3Xu9wrmxQsR3ZGMbW3fKSQ9bNElAONbB8IOkQHx4uHMPd7rHHkuSzPXKMvZEFhd-zgueMH7O6d67be93ultdaXWl1ZX_tLry4dG7w7Lf-KfTgaBfJPjlZVmWuInw4iDyUzcKI9dN_IIHHoNhPDdxPTf24igOQphUlHl-LFjowfiuSEo_O7OeceQre--5mNAcnop8we4HoVfkNvJlI1828mUjXzbyZSNfNvJlI1828mUjXzbyZSNfNvL1OZEvQxC7rp_mYcLKQTYYPiiTyb7EiaTeUjI_COI8YpnfKzTDr6Te8hjHEFolcIY3-meUqLhy_NpNvb6hUmtH2gGkx7e9nJ6ZfIRMLVmsJEhGuE9-ocA26B_xZ2Ne6p4QbbJIh_ORL3LsfJ6N-YRAiJE-rJWLkUZcEfoaecwl7zZCoiJRaB8ncG4rSPF8hK8BcwK7IhUiLhSETJijnQOzoyxmwClrIKOi7_guzbByv5YdgkActde4aAFPw1BlRwP2nX-0W3qCo2NgaNeNRR4MFGf47nqOfoTzTYA82hayb_3HdnIAemICqJSiyF3u5REovl4tDA48kz8e53nT_JiH3E9FzIBl-t0ZnHEarzzCiyavCULaAPpDvK78_ShQ8BE8ayMoLOnsFFWh9iI8S7CbDVSxrlsJlXdIXnwPFKVklSbSHWBkZaeY0BrYDgegvlWSLmkLR8aH2s_FsNcUqQa038coGnFTK-OEYVGA7lgF4xJTqpF2GO5utmQGIJYD_EcmCIqGU9GQFkw7OMD6hKEDFMW2agqoBUFMrddk1nLUoAoY9rJiUO-GiTk2gfX6UUaAgLtbokxZNX1g45BPyToeBWfqEk5KLqRCQ0hNAoRQdz3BnkGSZD5ArKAMev-A4V3t2fPL3aLL1HWXvpssQcizNTLut8b2wcGYgn6IBklZA__fKPv03Guu3r29Wm5EUbHlG3lXFWjmqv1oYPml7tTRLpEbALO9Bftz-RJxANB9xf-X7765vmthL9fw4yWtEX64kjUa8NM7aecsxZvLq3fw-7dymA833od3b2CB8ygAMozml6AR1r7re4tdUf5_rl9CKd3uwCKhmpZfUQ7KvXdZPap06ZGBoeNqluNLkkovSPPEP3hDAlaJKq_u-dlA--hKEsX9bWkfNsz2nlt2ANSVHsv4k88RbWetcch3p2FO0VvRhjgnNw3AnRe_m-_W-6mrdkATehGLn3y-E3YusOiBnXsIKR6W_mDQw1R4n-kQtDSP0HF4R7Bz85DjXpw73tOvfPlpBxPdajccnNq_tQ7o-rXyx-sUAFBEZYmOwz5DQur-AWkOir5HAItzR3dPDgAOj_QjvRpKQ2nbGUyk67qoSehIryMQSdXS20621qaJk2Owk8Pi8uZ6ecYe0tIMxH1qbXI3Pi8vwGcpy9wk5WWJki_PQXEmceGdywvog1r35wVYIWaF2M8oxB6e4HLUjnp2tkJziNn-IkHqOBLMTVgReEXmpSyKyjj3M5ZFYDrh9IPC833BEjDegJVCdAqDGRpnIY-DTJwMUh8t7ihi7V14wYV7qgVXFDMYPec2Ym0j1jZibSPWNmJtI9Y2Ym0j1jZibSPWNmJtI9Y2Ym0j1jZi_Y8QsS6SJM-CIshc13u6iPV5CveDEGVIIpJBghjeOZPCH-dW02oryzMR-UGZDQaW4WkzEMeXusja-ddV9_t9rn3MWHc2uLmJeqXFDf-tEZgj7UrYaoSZn1MPNW0b0wKNtW4IWCMJkiN3u98ALXLdLJ9GBLoA6A2EglP-275qCBDM1-IGuOev8DrYGKTSinDKgf-530upKtEHLOH1-LYksrJGE6tzjEHSBPCb_XrmcibS0TD2IyC3FTA9bjDdGMKBIXoySE22zAV5v2Eralwwbho5-r-X3qTvZ873bSP_JbiHP-HsvtfvWn7fBwXIsBM9_8yUrdaNOLkPEei4ANviClSugVLQGG9QeFNlZ5BGJUNGw0MpIgzJYhZkjg3cQSaYF2fmQId0KpoQdfqFtvmknB0OAQ7WOCrZru_ALqyVMDOFaN2c4rcJGRImnoh5KVKXnBYqj6T3Dt-PaO9369p0F5vuYtNdbLqLTXex6S4_a6T4iaKa5950OqfiuAHDcWfgt3D8daPyCuB9c_FJihlppJHy04gGdmToA-zgm-9LYjjViXiDhKtuWbhFPH4wpn7bYZLD2cbDtIAzc3eACMBIv652Spl8FGJHDhT1fnzL8H4Q5uTDrnFen5fIkIRgCoR4GXEc8Kh0U56FGdjY5xIZ-ljnryGR4ecnz4enfZxo-ev_dDpK_IvEyP2kcF3QeHlU-p7whJvFpRuHeBuVm5ZxHmRpyKMojt00DVIWhm4YJGVWRGWZxgF5us8s6VRkPLkIwhORcT8OY9ctChsZt5FxGxm3kXEbGbeRcRsZt5FxGxm3kXEbGbeRcRsZt5FxGxm3tdxPHdyycXUbV7dx9X-uuHrglaDf0iAO8_IJ4uo2Mm4j4zYybiPjv8rIOBqsl9845wLkh38-iJMf__kf4nbbnzlYniQ8TFM2jhVSlS0JwT0gThVHlcoK5Gxv899X9PzAYYiAgJA58HCHUmm6BroMeBDILLKnnTLhs1KKYpJPugG_DN6AvtbeVS2M0dsNlhjIrofd7mvs9unGAK9YDiYyoSDlVRu3SJATkwYkOmHXIBQW53bnzCvI7079BaqW1JPcANQQrHfDXIOh2CHqvWb7lqypLVD9GoTuLTnVV2d7ELQctJ7QkathHUrq9kei4egpAkC_pJ4VAnZEDP0E1kDFexBfnxfRD4Db4jx3wyLO3CAI85RzTyThuYh-H6N9QETf8tDPxUMPT8s4rFwfZxkMEfdfJsuAhbkbe0HulTELsINAwJI4Zi4r_MhnKcc28q4XCB6lHMA3oIwsRMdgmHLmh96Z9YxSDDwfL0oOows_OVV8X4YFKJXoXyLFQHAM-PLUD3qHnMGThmXypcw0yKPptAThhX6eeix2-_iMwWlqIo9hkUGaImjWVv2gCyQkroUUrQrIk9vgWJDLy2uc30rUrZKz9jlphRpsVWmK045t4KvGthCklyY4O21_zUaxz3GM1bAFB5_dUvuoB1KcDZ442odrwT_u6moI3WOQquxuQTrPKd51NwfpDPskb3FTJghtCOuYtg-UC0jPVG3vHgwMsA4rQJuwq38CnL3G9atdUHtzXe_XGIe5k8ptsMwKtWfK_aSXUoANInM_8OO5NkYLSWc0xrZWXlbZAKn3glXdhGFiU2psSo1NqbEpNTalxqbU2JQam1JjU2psSo1NqbEpNTalxqbU2JQam1JjU2psSo1NqbEpNTalxqbU2JQam1LzRCk1zi0Y74PLcQAShKNtws1TJdwQD0pAM1WM_2Vh_QcOftTIn-Gk0zg-ObJyNgOSRqwhXQAgWxBdkYh8YI7DfcP0knZ6E3gaZllYpk8-1TdDpI6tAVOCiB1Adp2DEU8OGFSclWiVVw9sS9Q_E1sbibCI_IOtvcIkmrYbx1dNlX8ro-JT-_rQMabumxBu7BWERp5wbj9STN-Bf1C_VZ2xjT_KsD-qOmzzITXuRilxVGPDfGXqxohIExaAKvFGs31jBJSV16aPLWLwF0T1vANJc89mPnSYIRo8vbPMy0XMBXvyuarNlaAMUWEBm_rSgCkbgXKpajfw-W-VPS6zzKqpzfW9VBRxlo0m_Ns-jq6j5zRXcnDsEH11ciOmdvahY0xsZgZg2-Mpf9q59WT69b4qpJeJQgAq6Pzjf29_nM_n9H_40fnLaxAjezJpkK6n9rJwCxan3vjw38l0FJ2ewSjlbTvv0zXqLQfrvKrv2c6HDnPPlhZZnMeFmz35FBHmkM9Kgc8hXaXa7DCvRIY-0NF9gbC9WqGs4WintxNSlCdZ4noHqu8p5vtnQD0q-QbgFtDTnc5rMJKDyO7BGPGdwvsEjWZfmhV6qrMTZzpvUyXlqFMDxUXpkVKpy7gGqfr78kJPvsTMR5o5gNfwRi7A4mtym1aadnRIq6AMC2UX4aTW2BFKyu_FOQBx9kqwdlDKc_KUzgHLDTpbr3hxTt1PXbbVjkw1irZuyf-Lk6f-Uaxp6lvnr5Rh1INb6RBanFPY9yyF36cpx0e5OKd7T7_mii4EA-Yp4bw6AcY5f4hmPjyYQWlOrMZ0tZ_VeJPLMRTePcsx3qVVGOZ6jVK8ij5NrXflj74nLajFOQ02sdLe4zHv1cbUsgzVM01-faLZfKSOhtdJh5azUspmcU5jTMy9Hcu7Qdafnrsh408P-mLabyAdAzKd1pTbvRBS0XLJU6Z_cHFOdk_vIQ6m1qj4E8z8QodfBqA4pCrO1dkZPuT2bO85yq2ndwz-8gOZj28fcuZnPcfJwA7s0EzPTMrjmSkRJbEeHNIQEvmcdHavTLwg8N0y84syKr04zNwsys_etNfnAz9FOru1UK2Fai1Ua6FaC9VaqNZC_WezUB9eOHdYo-R5s_N9XvuCpF-kAouLgAV-6adZLsoiBrgUJEWRelmY-Lko8oCXQQz_S6IEpl4AIQVuBGgqyFkZF1T2d__qTtRjRemFl52ox0qTALRo4P4r1GOJMkqDvHBzN_IfXo81xn0TuWKpSAtflHmRuPcUWVUHuS-TWL4vrequm3q_unY837ncr7DyCY9YB2bfvP3m3evLedvdrYVZKSYHWTjviK8oI1NHm_-rupk5l1evnEuAdpijcjdzKFFU2RBwvBVm7w_Wrs44o2QUTH1vq44g20wG4bDM4ZNiYUR2JQz_2nlRrcDSWDuvqrxhCvB88_LlS-e_duu6EQvnjyN3DjpBcroQ_XtpP0uchKkmGiouYUZrIU05_BwDXWtRrISz3xXqM02gHfsocMn4GW_qtlU575QCW8rPewtyVCKFfxkonp7rPQor9Zb2GiPSKh8agQYALdCedzodZqqg6_uF8w2KUbxwnRwgAAOpzq7PZai2mPePxA2gpEfE9LKZyjYcKtUMN4MZE58RoCEnxSkfgjbrEcfAe7d9Z3RVhveOsn3x2LB8AjOU4MdbhllSaur9ffRDZiDKywWwkYafhq1J1oJRGJgz_hET95dl3eC_DldPOuRRIRB3K-AMG2fH7m4xxlsY9XXSnyKJmqrosHKNkZqEZaPKerldIXzTigUfKPZsrQxwzCwGY1YMaLFhu6pAbYomKE4euQwzt0iQtzp_kVhzyGQYEinO2dGKUUclj9-P6uy-V3t-Pk8BJD7zw8RNQX30VQGDfXkswR5pGGpJHAKcKTlPRDJI4sFW7CH4lxt5iqQlZ2pjiDygintnDm_udl29guO5VpWeksopfctkbCkuZmZKF0NioURbxbrtCfOjJ6rjAsqFmU-m6i2pOukgu4vEkhIGQ0rX4brMclSuMB2cLA5OVDha6ajw9HhmM0dl7GOOiCHIpACTRRsgKMRW5sMc-I8pT5D8y5gwxrajqiOdWgmrxiK1tq2p-qrdc_lLvx7AeLcw02s5QF_oBiek67OAQESDWS7D_DDnaYVkIFNxh_WU9XoN8yFE2OdXyRMqhMyEQe8fd3LlYqMCXKWl0YyQVS-ge_bblpVC53rdm12XR1gI7wH06nnLcDAMvPUI54C-cyryXC-LGAvKPpHP8BeoVz3G1gcBS7RuWlq9tfUfQuyc18L5E-nK4n989-99qiAQtMYClDEIss9fKF9mOxeb7Xq38JN4-Rvn3_FPv4GZ0Cj43horVjc18XO972hsmcbWtDrLSe2WaVYPskHv5ZCy9Byl9THxoPQlLWwwqFzaq_qqfl0bCxrXAoWuv_CSJApg_gh8YA0hruE_AX_M1zUS03i-f7ycAWdtQLQzmfbJQXSb63hPKeoyn49y9Xv-kfJeJ68PmlxKB2A82T1Ea1sJ8oBnsJ6iX-qwru3qtdi8BAo4vzjPXXhu6uHivrl69RZXF-HqXn7CHEY5J1mnqBKCpITVy8M2K8prcoinUFzmrU5K-1HDllb-Wfu5pfSjEyJJCaz4fLBR4VSr3X5NovHoRLVJq9f77v3lq5dnVxq70cKNIz-RZDhoZ1zti_oWgZZgGy3wsdyPrmEhC7IlaxmALW42yG0EQjipel0Mx_oOM-LIfDZF-gDmsMyVAXkCaEJdZhTcIAWVMDzF6lT5zKi2EuwpevtAxYeLf42zYBOrDxc-GBXxqdUjoVTdHmth11i41CIZU1GvWptMlgOFssaKE8oI73UzlYDoDUGRsm8F0k8vdyTsps9nVDulII0UhaAcdDmpqs4Y8DIFWQyC_j1mr9Zb8jRNrtRL_DQ4tdKXGjvs-pt1Wrm6FQWe55T0aQbfQFa14zBeUbHVtm5V64jnozT1gXIJZ9xJ6KYIV6KcAyalc7ujcrSJJYEEigPv9JLI1JaZ-giqQVUDeQFClezaola_kcV6ne5xARTX7nNZT_yjc1XvAVa3-rCx9kXxAGwMlh6xvmKCrwXbKkPqMNW9Z0Mk-0ugJrDyJpaULlwv9rKT3DhS2X_b1xLczw_jtmDbbkntSHXejmAAjMeqRslpGdoyfLEqpfk5OaUwt3lE91jFtoO9Q_QggQknexUPFuzXbq61tj7bAf6NSw7ljrzRBQOyIEEe-aSg8jw38E9tjXLnzRX0w-r_16L5CNLmxeXXgALZTpVhzbnMwF0PXKyNVzheRL669Etb0LDvsvKjD__JspEzEBqp4YRlbAjvCiQE1fARuRxv1QhjaRZXG_tC5N3EDsUL10-T6PQOFX3xdm8JOHvVHEx5H-608UB1KBSQ32yYdEqQK793s2AA0tibIzg-7Nbzo-FRYQNP_h11szEXpF1gK7BmYWRQpADwgOjg25RFjzUHCPHbTpsbZPQaewT080q6FadpKAx979QOvatW24EqsIUDrbsQVBODjA-01M70OTfKEuprJFTkF80DKnM2TSSTinpLSiDA4RJiayUon97VQCRb6arYw0T2mFHt4JfgCO7G7QWwuhZeCKIIO1Jo56VyVADzisIoh9B7RRx32X6chqvxAj4lLLfw_CxcDkgvJhELxg6V8O7YSlVLdDKwMR8ZaTqpqJC0RgqGOjfI5jljAKu-MyfEVLJqjY5tALHrOzC9DS5Sm9dr_rmEgKfsTUUeiNZo3YeK8sTKo2HlQC3GwiPJS-s1y-tGYVMkRdFV-pehewbojB3Vq2kbGUQKXn63FVK_IDqeaKL0tz1DkaXkK3rT2s6EBGaQoj9YWNqkfokWfhycZoA3DYE6ZfewVSMkbbINovmBtSvlfJPpDkapD0kJ2Di9XM0puNpL5cagmr9D21pWEg529OBbg21RBTemR1BuiSaVkaMRNuJUzKvvTMOzSHh-yDM-tFXq47WDYfpUgdahI45LXh6WDu8dYq9jK_WLgqY3qjZQFySeNld1efVAIFMFtb-h5f4FvzC__OPkd9jfliQSTldiryRxDKJ0NoDjPsFrVFGt685-dL4mClgflXXqIKpMb3l-oiCb_HKkcdFglBahKvbq5I7JUJyR3KbynFQ1F0ZZe7ByaWzabsMXW55Xi-16s9hW11Q2RLVqQPvLN6-vQrCMvSyiPXlVra67W4H_HTug5FTIS7VvjI0Y6I2Qxq3Iyf6R_eMO4AgWquVYIHdHz6qvAqkMZmffi0QvpdqCedHV4_MEvtxWn-hM0eqSRsBSftoKmCBIIi9bmmewBJUOvwJyqVgrT7-Y4zW0R3VkqJzgoXU7U-X3naSQutH5UmbiH_D4ru1Llhm200C4_SOWVu_lxaFG5a-Jm4Atd1pWyNJC1ITbUcm83IP3f_rdsH7QptI2Lxu2ERRzq-oltVlpl2B63wDVgiCZfxSIHzcwGtCLmHPe-q7nYmGW4hTAnLBTdw8ceafkLSgvRKTovZ8D_oZ_YE87DmMncmwDm8iOEb1Mkp7fT7uq0WB_5uixZIUz9Q6hcluh3Fh6G6U13g808EC_vXgWypGrnBd90qU2al69u3TMiE9_7MMetOuWLQpxs8QGVtiuzF9KK5DwqCZOheJRsDbabjE8nOg_mI3ZB0WGZFdZZK5iIrkMIkhz2zByzqSzEtp_rnIqqO1Wv2QV6CGibMegawRv-s2oVupmW5rWYGoY-thojtOqx5dHj-Ne_Mc-B7tAUG1_P1myZDGDlE5Q-v3NTog6dLiBCc47tjL9Jmg_bmSfSZmziW2vlE8Zq9xa2QGSvnHTF5q3TO1Whwi02uhvHALKb6--UZ0ydsjVxunD0bQLdMTh-tCz17QkZeQkiSaGL5LAfEGnrQAdP0zU-FHqZjjou04bn9ozSIvqfUHSjdv2Bb4SFSvQ1B-aPu3fo08RK2ENpCVfShDmLKRyXW_hpnGY_IaceaC4AKZw86tKTPHr6saItxnd2oC_dcjL8PkPS9a6TpbvKuYYvBBmVq6kJb24t9_Or_C4--Yc82ZvSsOxCtABDZUPjys0vzfnOBSqe-zf1mp08Bb7P_zfavcQddIBm3nBEkTRNaLctXaetmO9AjvVVGhSECrVXoK-wUi13e0Ja-47-QMHHh4BUV2usAPVMfZamaaG7lxRmQQ9tKZ8rrIBhk4nPR8OeRw9PCCM9PXLP7w_SygR-nb8NEZfI4Xsxfyd7K7WGxYAz-bU_Qa9AttewL--eoMuDJLaNfVOADWHkl65YwhacSJ6pU_7vVJZSAjAZW82bCIIMtpo2Em2vu5SM1DVKFrU7w7ap_2a-439eg9YddIv4aVucNLFfIVhP4qFqc5pQ7XuGEaQZKPMlplyYs1kmES5FBF-kEnYt7UwhhqLCbYdRNpBwzYQ6qhCxNawnqdNiiTmJfO93I-8YOis1mcpDibFIzIMdcg6zIqkDHKRB32sy0g6PIx1fVHCIKKDbiTvJFpZbAU8tGsXnMtPPkgpQD-TybzEWS69LE6EW_KAsZjngENEFPtlxPNUBFkUivklNW3l3fwFAJlWdO0H2IUP_ea0H95jk4jFdbdZA738Ad76zZt3PYe8Zh9lt5PdtdjWwIE1gtk5-mzx3w0aDhx_kuFkCSh1mOC57JslRrYE6jrZQVICh94vLau4NLG_VAkZ8yvswoQusOE8X1BVx7RHIRw8CmlsehQoaEbOYRm86l2VcgKzIRXE6Mujf5bwTyWP6C1hPciF8YZZvqrxYM87WD03WbiJ6yoHq4fzeo_v6nujUf4jMVxLapIERCE5pUKr6u65atmCLiDSupjTUn2SaEXVZ4x0nG5kpqd8hcoNry-Y3k2XdhPV-yIMfWM3XZz1JexRsxLI3ugu3-w383Ivo7jkUaFmWLSYPmLFnF4yomUKxgpMTgtDeBr9azogrIWKjArpdnb9Cig6A-O_A9q-bxUH4WDPS1Q4mNbxJ9hmEHjwnjXeGTHv02i4eodsE4uLQdLROqBPk9FFe8IID_YEjf038smQkYchozAguf2HS7XBRBa_x-4I1PWT6HCOFuW1AOqudyBZKeiL5h7Mc22SDq5Wbjn82moQOmp5Lvv8op4VA67-88s5zdT5Gr1_r4DoJpRstPCDUAdQSGb8jhqW9WER6h4lWR7Ic89lVgPTXUEOeoejM6QEVWHQaMf28-mdC1Hj-W6oPPHE4l83rMBmkNTiaIAqztD-E6QSVQIRSMNoqBIEgwNwz1qUVwAAgDIYCBNxj7srY56XBz4LWd9zz8j6HnTTI9O1dS4GizJ4XRbxIulfN2Rw68KNR6ReK_CmmrNvDZdhj_ovTbaVj1NLTPzGZW8TINEZdoH-9sJ5-UnWwx1WQ449FCpVTudmqWatwjCQxvVz7MgmLAZ2BR5WxqnxemliqgywtpZZeYe5X0AaOvLSO4v7Nlzj1Cf9_NjTdiKbSybljRp9HTfDlsgY8wCMbcLUWwp96LZpnR5ILliWCJqd2Mr7woYqtYkMfp0VQMG2U8lVQ7hhnNx0nOIit0HmNM3NeBsw_jW7AV02kdzku0kcFDwpy6ENvJH3rxtZPiJhnzJ19E0CkgYwS7Q3KVUbbZXbi2S4pvpgR6xV9aNj5EafqqVUIgUT8fpLCto9_F0JYIFkCMNcGrdFzFckwY7yoUGCVeu11u59aA_9VNhOnQrMVSSt2CMQG8Rsny4Ka9mTi7jP6BjK0HuMo4x68u3O-mRX3cjvXMIrUOde9FdPAP2iNpAEgNmbSEx9H16dx2ovZrAXM9iLGezFDPZiBnsxg72YwV7MYC9msBcz2IsZ7MUM9mIGezGDvZjBXsxgL2awFzPYixnsxQz2YgZ7MYO9mMFezPDzX8zwL3T1gjaK1NULnNb3sIsXigy95Wzceu_tn2UkZqigu68T5KkvTLUnjHiYpWn8iLfOna--eg9v-Oqri8HVTdhOY3bkpq--kk5FfMpQfCd03NCKM2Wu5x1tiK_8dpftx_s3Y_zwxEZEvshiNxFf-DZzE3Tll3bdn1-_yquZ2IQUhF7pHm9CcOFoq_b-TRg_PEUNXsY8xsovfJu5CRV2ExhbltIGOLcbE5sQJlmaMBEdTiu8cPoU6FGKvKly7t-ehw4z1YvSDVw3i9iTz9DcUqPUWZspR5up6mNmzvs__W42saWuKP3SdY_oCn0xGnKfTrcAZrh_Sx80jG7RM721XpH7wAPxk8_U3NpxY3IVGDy_y2-OWPZ053xDpk90xT4ws0lpSccmhvxkcdSoamNxToRPd6dGG3Fka-G2GXYYMGfHFudk8CMXoJO5BWYBCgqWLc4J4CdfhiFFH7kMWfjeF6gtzonPJ1-CIQMfuQTTPX5Ghj357A1x88jZH7mhDproG-LiaVZxuhW78gbpWapkt9ZBoVCQZ8ZsM_FZrdNjnpQsKcM8jbLcK1hU8pzHpTjXOr1v3Xl_63SLMS3GtBjTYkyLMf9BMebDb9k46g7t_nS63_Mv0u668Iuo8FPfj0o_8_LcZ1laCnRYg7YTAo6El8INwizjwi2ESOOMZSL3Qjfy4oTSNE4uaNzhOnjvuRfAD250osN1iCkXRZj8S3S4jjMexSz1Pb8cihl63W_EBx6oytW4Xi5EnBRBxLJ-ooZ2792wj1DWJ5tCyeevDLSG35LFf1Sc1bdZGjWLdQR1rsauKyoa2WIBmIzz9b1MtWWCLNuqqb1A8Ifv-J1KkznqA2V0f8IELerLedwKCFBg3qmYgqx1w5iCWUQ2KiIY-kEQeFtMhI9LN3JZ4MWFCIcu4z2YGZ3wvfhEjZnlkR8nIud5MHQ-HSDLidP9bBQy1aHp9CF_owsHWsrKd1Zsh729sI8AJow2zX4ni2SPmjOphjdDTSJ-9bDN0wZoACMVQyDskALeUr1u2z_JNnm1otCLbsSOQY8hwmGmaerWtEPXz77WmdIethNNTScO3_XissyTJMqGlHsDxI0O_15cpllbRCCGcmBmUh-StQeoduLwPxt9TeZZyLDk-Qdl23SGrbfPUEpvlLXncndOtPLRuz1z9i31DR-aNqk6C6PXzyFpvNOZnUctPHVWD0XB-lSv41aZPeMfdvEBS1eX84yi1xNU4YVBLPLMT8qszygxUO2IKh4BR_tYd1ZGeR5HkdeHhA2EeoJePhtaOtihZebo1iQz56BRhzwglXSicj1kC_5923eUYbIvBWZL5mJd3y5OE8_VEDY-2ZQHzmOD1VyOccjjni7y4GYyk0mmY2JTo554-nSZvl4U9cghSV0qitrIIquBLmS3drPFS-8AeW62zpIpWTJ136AgbCnDBsIbPFjzg1SAuwkKC1JAaiLxEhA1Q7_qHuSPKOwJ0LmukMndmANVuW7cqzoDsJ-gtM9G2id6eWITTt2TceaYDVBn2lNkNpB4MKGRo4sftvzse23O-k6JM6MZ6mzcD8JoITFq1IgqxdjVQ9p6cdjFs2-Sg5WgtAOaGCRaMnFKX9-og9SyRYlqAWl0XR8335juvX5IYPZmFnszi72Zxd7MYm9msTez2JtZ7M0s9mYWezOLvZnF3sxib2axN7PYm1nszSz2ZhZ7M4u9mcXezGJvZrE3s9ibWezNLPZmFnszi72Zxd7MYm9msTez2JtZ7M0s9mYWezOLvZnF3sxib2axN7PYm1nszSz2ZhZ7M4u9mcXezGJvZrE3s9ibWezNLPZmFnszi72Zxd7MYm9msTez2JtZ7M0s9mYWezOLvZnF3sxib2axN7PYm1nszSz2ZhZ7M4u9mcXezGJvZrE3s_w6b2b57qf_B9SA-Ts)
