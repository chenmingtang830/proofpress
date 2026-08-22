[//]: # (ob:cb2efec0)
# Long Horizon Eval Research Plan

[//]: # (ob:b7f8b55a)
## Status

[//]: # (ob:f5ea102c)
Proposed research plan. No benchmark runs have been completed, and this document reports no experimental result.

[//]: # (ob:73566bec)
## Research objective

[//]: # (ob:58644053)
Evaluate whether Proofpress improves the reliability and efficiency of an agent completing a multi-stage contract negotiation across session or worker boundaries.

[//]: # (ob:99f35ae2)
The benchmark is intended to measure end-to-end professional task performance, not merely whether an agent detects a stale file at one handoff. The central question is whether version-bound, admitted decision history prevents early state errors from propagating into the final negotiated contract as the number of negotiation stages grows.

[//]: # (ob:f58bf7d7)
## Why contract negotiation

[//]: # (ob:1d3b45d6)
Contract negotiation is a real enterprise workflow with properties that make long-horizon state consequential:

[//]: # (ob:f834f2fd)
- the operative artifact changes repeatedly through drafts and redlines;
- business and legal constraints are distributed across contracts, playbooks, emails, prior turns, and internal memoranda;
- individual issues move through proposed, accepted, rejected, closed, reopened, and escalated states;
- different lawyers, agents, counterparties, and business approvers act at different stages;
- an apparently small version or authority error can propagate into a materially incorrect final agreement.

[//]: # (ob:40d2b324)
Harvey's Legal Agent Benchmark (LAB) provides a practical starting substrate. Its public contracting tasks model realistic contract drafting, review, redlining, issue identification, and escalation against expert-authored rubrics. The current public contracting benchmark represents negotiation stages as discrete tasks. This plan proposes composing compatible stages into controlled multi-turn episodes while preserving the underlying matter materials and rubric criteria.

[//]: # (ob:313290eb)
## Claim boundary

[//]: # (ob:aee1fbf2)
Proofpress is not expected to improve legal knowledge, clause drafting skill, retrieval quality, or the model's ability to reason about commercial tradeoffs. It supplies no additional substantive answer.

[//]: # (ob:cd488785)
The proposed intervention is narrower: bind each operative contract artifact to the admitted decisions, supporting materials, actors, and versions that justify continuing from it. A receiving agent still performs the legal reasoning.

[//]: # (ob:dee88754)
The evaluation must therefore distinguish:

[//]: # (ob:0356c47c)
1. final task quality;
2. unsafe propagation of stale or unauthorized state;
3. recovery and revalidation cost;
4. conservative false stops introduced by verification.

[//]: # (ob:828d73df)
## Benchmark unit

[//]: # (ob:8151893a)
One benchmark episode is a synthetic but professionally realistic contract matter that advances through a sequence of negotiation states. A representative Master Services Agreement episode may include:

[//]: # (ob:c91fbef8)
1. review the initial agreement against the company playbook;
2. produce a first redline and internal issues list;
3. receive a counterparty redline;
4. incorporate a new business priority communicated by email;
5. record a human approval of one concession and rejection of another;
6. transfer the matter to a fresh agent or session;
7. respond when the counterparty reintroduces a previously closed term;
8. escalate terms outside delegated authority;
9. transfer the matter again;
10. produce the final redline, issues register, and escalation memorandum.

[//]: # (ob:78ee24e8)
Each stage must have a deterministic release packet, expected deliverables, and a rubric. Later stages must depend on earlier decisions so that state errors can affect the final work product.

[//]: # (ob:b75eb924)
## Horizon construction

[//]: # (ob:0f4a8276)
Horizon length is defined by the number of consequential negotiation transitions, not by token count alone.

[//]: # (ob:0dad54d4)
- **H4:** four stages, one session boundary, no branch merge;
- **H8:** eight stages, two session boundaries, one authority update, and one reopened issue;
- **H12 or H16:** additional stakeholder decisions, parallel review branches, a merge, and at least one superseding contract or playbook version.

[//]: # (ob:7bfaeeb6)
The pilot should use H4 and H8. Longer horizons should be added only after calibration confirms that the underlying tasks are neither trivial nor at floor.

[//]: # (ob:eb8eda0e)
## Experimental conditions

[//]: # (ob:8abc86d0)
### C1: ordinary portable workspace

[//]: # (ob:f42e5d4c)
The receiving agent gets the complete ordinary matter workspace: contract versions, redlines, emails, playbook, issues lists, approval notes, and any allowed native session or memory facilities. The baseline must not be deprived of information that a competent production system would normally retain.

[//]: # (ob:30b6bae0)
### C2: Proofpress-bound workspace

[//]: # (ob:5ff6b2b5)
The receiving agent gets the same substantive files, fields, instructions, tools, and token budget as C1. In addition, the operative artifacts and decisions carry Proofpress verification and admission state, including the current admitted head and bindings to the relevant evidence and versions.

[//]: # (ob:6a5e87fa)
Proofpress may expose whether a state is verified, stale, inconsistent, or not admitted. It may not add a legal conclusion, negotiation recommendation, hidden rubric information, or substantive summary unavailable to C1.

[//]: # (ob:26256cfc)
### C0: continuous-context upper bound

[//]: # (ob:a37cd2e1)
A diagnostic condition retains the complete continuous session across the episode. It estimates how much of the observed loss arises from state transitions. C0 is an upper-bound reference and is not the primary product comparison.

[//]: # (ob:7ff020af)
The primary confirmatory comparison is C2 versus C1.

[//]: # (ob:24139842)
## Stress tracks

[//]: # (ob:e1e8b4a6)
The following tracks must be analyzed separately and must not be pooled into a single efficacy rate:

[//]: # (ob:3c43acbd)
### Clean long horizon

[//]: # (ob:b450f8b7)
Only ordinary negotiation events and session or worker changes occur. No file is deliberately corrupted. This track measures clean completion, overhead, and whether durable admitted state helps under normal operation.

[//]: # (ob:cd2c3ed9)
### Evolving negotiation state

[//]: # (ob:34d911e7)
Later stages add legitimate changes: a new counterparty position, updated business instruction, human approval, reopened term, or superseding playbook provision. This is the primary product track because it measures whether the agent selectively carries forward still-valid decisions while revisiting affected ones.

[//]: # (ob:d61b54f2)
### Integrity fault

[//]: # (ob:09896624)
A controlled subset introduces a stale redline, mixed issues list, missing admission record, or corrupted carrier. This is a robustness track. It must remain separate from the evolving-state track because it is closer to the already-demonstrated artifact-binding mechanism.

[//]: # (ob:30830319)
## Agent and harness substrate

[//]: # (ob:7e1feb17)
The initial implementation should build on the public Harvey LAB filesystem-first harness rather than inventing a new general agent runtime.

[//]: # (ob:031e16fa)
The substrate should provide:

[//]: # (ob:b4e085b7)
- version-pinned LAB task materials and rubrics;
- a fixed model adapter and agent loop;
- a per-run sandbox with read-only matter documents and writable work product;
- document read, search, write, and edit tools;
- transcript, tool-use, token, latency, and deliverable capture;
- an episode controller that releases each negotiation stage and forces the registered session or worker transitions;
- the existing LAB evaluator, supplemented by end-to-end state-consistency criteria.

[//]: # (ob:d1f43375)
A durable workflow runtime may be introduced later for multi-hour execution or human approval waits. It is infrastructure, not the experimental treatment, and must be held constant across C1 and C2.

[//]: # (ob:f6385734)
## Task selection and calibration

[//]: # (ob:47d02bd5)
Harvey LAB's strict all-pass scoring is intentionally difficult. A benchmark with near-zero success in both arms would conceal any Proofpress effect. Candidate matters should therefore be calibrated before formal evaluation.

[//]: # (ob:5dc82c25)
Selection criteria:

[//]: # (ob:8cb671dc)
- non-coding legal workflow;
- at least three materially consequential negotiation issues;
- multiple document and communication types;
- explicit delegated-authority or escalation rules;
- compatible stages that can form a coherent episode;
- deterministic rubric criteria at every stage;
- criterion-level baseline performance high enough to avoid floor effects but low enough to leave room for state-continuity failures.

[//]: # (ob:b74fc5a5)
Calibration runs are diagnostic and must not be pooled with confirmatory results. Task composition, horizon schedule, perturbations, prompts, model route, budgets, and scoring rules must be frozen before confirmatory runs.

[//]: # (ob:cd969598)
## Outcome measures

[//]: # (ob:44a23130)
### Primary outcomes

[//]: # (ob:5a79c743)
- **Final all-pass rate:** whether every required criterion in the final contract package passes;
- **Final criterion pass rate:** the proportion of required final-work-product criteria satisfied;
- **Unsafe state propagation:** the proportion of final decisions that depend on a superseded, rejected, unauthorized, or mismatched prior state;
- **Horizon degradation:** the change in final task performance from H4 to H8 and later horizons, reported separately by condition.

[//]: # (ob:704c300e)
### Stage and recovery outcomes

[//]: # (ob:1ca3b458)
- correct accept, negotiate, reject, and escalate dispositions;
- reopened-issue detection;
- closed-term preservation;
- delegated-authority compliance;
- correct identification of the operative contract and playbook versions;
- time, turns, tokens, and document reads needed after each session or worker transition;
- fraction of earlier work unnecessarily repeated;
- targeted revalidation versus full restart.

[//]: # (ob:2b07f7ea)
### Safety and cost outcomes

[//]: # (ob:04263eac)
- unsafe continuation after a relevant state change;
- false stop or unnecessary revalidation when state remains valid;
- Proofpress verification overhead;
- invalid, incomplete, or inconclusive runs, retained with explicit reasons rather than silently replaced.

[//]: # (ob:b39a5c18)
No single composite should hide the distinction between task quality, safety, recovery, and cost.

[//]: # (ob:a99495af)
## Hypotheses

[//]: # (ob:e5d93911)
### Primary hypothesis

[//]: # (ob:0e2ec235)
As horizon length and the number of consequential state transitions increase, C2 will reduce the propagation of superseded or unauthorized negotiation state into the final contract relative to C1.

[//]: # (ob:2cfa50bb)
### Secondary hypotheses

[//]: # (ob:0a629561)
- C2 will reduce recovery time, repeated document reading, and redundant revalidation after session or worker changes.
- C2 will preserve clean-path task completion without a material increase in false stops.
- The C2 advantage, if present, will grow with the number of state transitions rather than appearing only in the integrity-fault track.

[//]: # (ob:dfa07c24)
### Meaningful null result

[//]: # (ob:3f37aecc)
If C2 improves only deliberate stale or corrupted cases but does not improve evolving-state completion, recovery efficiency, or horizon degradation, the result should be reported as robustness replication rather than evidence of broad long-horizon efficacy.

[//]: # (ob:bb579eee)
## Pilot matrix

[//]: # (ob:9c990844)
The proposed pilot contains:

[//]: # (ob:01bb3159)
- 6 calibrated contract matters;
- 2 horizons: H4 and H8;
- 2 primary conditions: C1 and C2;
- 3 independent repeats per cell.

[//]: # (ob:53197b3f)
This yields `6 × 2 × 2 × 3 = 72` primary runs. A smaller, explicitly diagnostic C0 sample may be added without pooling it into the primary comparison.

[//]: # (ob:d6dafb4e)
The pilot is intended to validate task composition, scoring reliability, baseline difficulty, and observable failure modes. It is not automatically publication-grade evidence.

[//]: # (ob:b742f2d6)
## Validity requirements

[//]: # (ob:d508dbc9)
- Pin the Harvey LAB revision and record any local task composition separately from the upstream benchmark.
- Confirm that each C1/C2 pair receives semantically identical matter content.
- Keep the model, provider, resolved model identity, tools, prompts, budgets, stage timing, and evaluator fixed across paired conditions.
- Prevent fallback routing and record exact provider telemetry for formal calls.
- Separate local debugging, transport failures, and compatibility smoke tests from formal evidence.
- Retain all invalid, partial, abstained, and timed-out runs with denominators and exclusion reasons.
- Use blinded or mechanically derived perturbation schedules where feasible.
- Audit the evaluator for leakage from hidden rubric criteria into the agent context.
- Report criterion-level and all-pass results together to expose both partial progress and strict completion.
- Do not describe composed episodes as official Harvey LAB scores; report them as a Proofpress long-horizon extension using version-pinned LAB materials.

[//]: # (ob:11ab831f)
## Relationship to prior Proofpress evidence

[//]: # (ob:1b2310d0)
The prior Proofpress handoff study tested whether a receiving agent would continue from unchanged state and avoid unsafe continuation after a relevant artifact mismatch. This plan does not treat that mechanism as a new result.

[//]: # (ob:d30f7bf4)
The proposed increment is end-to-end and longitudinal: multiple negotiation decisions accumulate, legitimate state changes occur between handoffs, and the final contract—not the local verification disposition—is the principal work product being scored.

[//]: # (ob:116af14b)
## Deliverables

[//]: # (ob:2204aedc)
Before formal execution, the project should publish or freeze:

[//]: # (ob:2987697f)
1. a version-pinned upstream task manifest;
2. the episode composition schema and stage-release schedule;
3. the C1/C2 information-parity specification;
4. the perturbation and clean-track registry;
5. the scoring rubric and invalid-run policy;
6. a preregistered pilot analysis plan;
7. a run manifest containing resolved models, providers, budgets, seeds, and artifact hashes;
8. a results ledger that preserves every attempted cell.

[//]: # (ob:f58bf390)
## Decision gates

[//]: # (ob:d83822af)
Proceed from calibration to the 72-run pilot only if:

[//]: # (ob:e751b80e)
- at least four of the six candidate matters have usable intermediate difficulty;
- paired C1/C2 inputs pass an information-parity audit;
- the evaluator demonstrates acceptable repeatability;
- stage transitions produce observable recovery or state-selection work;
- the baseline is not at a near-zero final criterion rate.

[//]: # (ob:dbe7f2c2)
Proceed from pilot to a larger formal study only if the pilot shows a measurable difference in evolving-state or recovery outcomes, not solely in deliberately corrupted carriers.

[//]: # (ob:ddfb51ec)
## External references

[//]: # (ob:8fb467dd)
- Harvey AI, [Introducing Harvey's Legal Agent Benchmark](https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark), May 6, 2026.
- Harvey AI, [Extending Harvey's Legal Agent Bench to In-House Contracting](https://www.harvey.ai/blog/legal-agent-benchmark-in-house-contracting), June 12, 2026.
- Harvey AI, [Legal Agent Benchmark initial results](https://www.harvey.ai/blog/legal-agent-benchmark-initial-results), May 26, 2026.
- Harvey AI, [harvey-labs repository](https://github.com/harveyai/harvey-labs).

[//]: # (ob:397ceec2)
## Current conclusion

[//]: # (ob:4643fed3)
Harvey LAB contract negotiation is the preferred first substrate for a non-coding, non-research Proofpress long-horizon evaluation. The most defensible product claim would not be that Proofpress makes agents better lawyers. It would be that, under matched substantive information, Proofpress helps an agent preserve and safely revise the operative negotiation state across a growing number of consequential transitions, improving final work-product reliability or reducing the cost of reaching it.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFiODVlYjE1OTU4NzJmYTMwYTYxNTI2YSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImRiZjViOGU2IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xOTUzZDJjODEwOTRjYWZmNmE1MzkwOGIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q3ZDAzNjUzN2RhZmMxZThiODYzMTI2ZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfeuO5EaW3qsQtT92Z5xZ4v1SA__o6ZXdsjXSQNKOAc8KtUFGRCWnM8kcXqq6JAjwQxjwA_lN_CQ-58SFkVlZzOrMtg0YxAxaVZlkMHjiXL9zqV9vWDfUklXDfc1v7m72-_ugzBNRBkmR5FkoWeSzNEjClN2sbsqWP9_z-kH0A1zbb1iYpHdBEfl-GmRxyIOqYDJiLKkqLuIq9MuU-2HpZznLozALYU0_zAIRFknFkyJloUglrMvrvmofRfd8c_cr_jLcD-wBnrBlAz5qBT-UYgsf_EV0taxZuRVeJx7rvm4bbwPXt92zVz57f-7aVu470fdwz55VH9mDwJc6-Lhr_ybgdccOF9wMw76_--qrh3rYjOVt1e6-qjai2dXNw8Cahzzyvzq4uxN_H2v4-X7sRXdftU0vGqDF0I3it9XNRjAkIi9lUuYivVGf3ItHugiIK-6DIol4WOWBX8QVkzJlSVT4eYk7a7sBX-1-WzcCdm5OZHvPM-5HaRJlnMkqEHmZp1EQpkK9jt7dfcX2_biFFw5xn1Xb8f7m7q-_3ujH_3oDp9x2Pf6kvhb8vgSS__Xm-71o3n3jvW-5-HTzM7yIYQo85WHktei_2rDuUTyv4STW8NpDB9-uG_HQDjUb4BjW27Z5WG_arv6lbb764esfv373w_sP93_-9t13tzt-s_osPmPD0NXliOvel6yve9yH2Mp71gPZB0HrjQM8DV_mY93gkv1zP4gdfNOwHZ76wUut4P4e2eXmrhm3W3jFagPnKxSFym1bfYRbqjIUUlQ-XI7vKD4hASam8r7Fd_yg3hEWVlTwvlNUgJv0ThjntMU98qh4gk_-wXvrKvjO3tePbDvSj7DK8LzH10FOAq68-W017bfMZF4mCTvY748DG8Z-djf_4NmLZlaXiWCBH1afuTq86b7tBQcJ7QXrqo2337Lm1vuu9UrRVJsd6z563dj03oY9CvhMNB7I3X4rBjFtaM86drCbLErStBSHu_nBPKItUajrR3HmvU_eMEODJE_j2E-iK56qD1N4TxsxbETnskK9A_l9FL0HXwC9tqDa6m09PHus4Z6QcoYeRSGjhInwip39tBHOkdSwHVingau8ofV2gvVjJzz4YD20a_iPB3uVSorYdmZnMslLmfHsYGf_ZfPsGb3hOXrjzHnN3DZzagGPyjjh6dU7eH_ieiQUg8NiW6DNILp9V_dwuG33UW7bJ-8JLAlSaj9HoTyKZSj51ftbE-O0e9ExPGzPKFlPazfY5l4A7_HtM1zZtePDxuMdkwO8wrS_LVjQg_3FPg_LKIyv3t8HMhr_CDpPPAC93j0Axbw_Wpb7p2_f_fF3SKzHmguk6h4Xryu4lMz-a_SLgigsfFEe7O_9ltU7r2zHhjPwJOb56sXFM9zEhAhkKcMLn-aKe-817eCJT3sQTiVmWgN4WyLQx6Z92gr-IFZetWWugn5Bg4rHeZ7lyYW7QtnfG02Nct-hl6DZu2Fd1z6J7s4ra1REDDWKZbJqZldcCNhVEl-xK2GNn7cb-wE5vBOyBVWEniEczlj3m7uZPfhgKao4qy7cQ3DryRo0nDew_qP395GhQv7DvzbhrQdGi0lFN_agtthKYFUG_mjbwddzQpWHOc8iLg-2NcnC2NTDGaZ9cfEM0-ZBEuRFxC582veNaxrEvu7BjVKar39u4EhASj3w0A5sAigZVItzTFuAJAmZX7grOBr1M6m9Gq6u4ZzYQyfEDjULHErdKJYhl4I1z-h8PJdt-3HmZLJciDAWl-7qaxQPYIIHoRiW3BrmcfBnOggkkGkrNO5gUIF3ICoRw8rogBlalRm4x8WREjZuI0YeEHRUbzChr9wywzu-jFkeZulVTzbXbwWEUhtkHS5ArkDblM90QM24K8EbAgGiMOrvI-ofOE4wLXPCzRlPYn4dVdbe73__Ib77_e892Y6dOrt-5bXA9DpMsJpiBRrbKzsGzAAuUfcg5violGAryuvoRoq53oKZ6DftuOUeRJreh5g8wg_5LUUPQDYdafXmqhJYjs_QTUBAypkvDvb2NTBhV6PoAN3hY17j7s7FDq_fNaePWFnlKT8Mrd4Hd6A34VogtGfCX3KlepCTM748GPGzt89FN3EoEh5XX2pDP5EHX4n6EZ4Emgj10YMYequMML6ZFt9BjAvHqJaec3X8Mi2ZOKJbeOdEEWvi1c8g27m75-IhKdMyLJMvtJ1ZovUQx3v9WIJ4NuR4yHqLYiprseX9aoZoKUtEnkn2hXbpeHA79oyqu-2ncI6h_hjIOD4SPCX4SvkEKzBRM7sM0xAcFXnEgf4dedl1M7Zjv9ZfeOMeZE4ppbPH-5YV5tzdKKt4KIIvuK134Lqxh6YlS2g1Bpz8gPb6UEKmpyhdPAcJSOmHPpNfcKfKLa53KKJwq6w7ENSWfgF3AiI95SC_D_Gse9jj--B27ojjICryODyCUIiVMJD6eB6nObx25twEAoMxSy97Fr64bLcQwaIkquuVO4OWBZy751_AdPcCX3EQW4VQ0PdNO6e-qjhiVcmPfHHBwDEAQ2bM2FmePnXHHDAWJ77My-yKx37fwEtade3G_4Sn9kQA4y20SpMDh1HgPRu2hVUkeHFohx_bLWlA9zGkVc4RZvbOGQJFMS-CQGRfYBvfMjRkyocCH4RjKAvyvUOdqGGIO1CSDXjtFYgfIiasG9C8zgo3T4MyiY-i7m_gh4cOATLJxu1wjjovL5_zeou8SNMjf_szHvhOoSMgQygoYLbEgIF11_KxInBDxYmd4Ijvr7xd_QlD774fRT_rAOSRHwWHDKOAFOTADesalHCyk91ZjvHm75whTyYCKcog-xL7-MmJ3mrU--RMKnbT7uxYw7_wO9qG_VhuwXAoMGk28A9EkB6Z_Su2aC80u9JI1Rz4UMbCz5Pyi5BpTUYGkyv7usHI6dt3f1SoBApXB9RTWqgby66u-j_8a7MGNpPEV7uZOIUHMo6iLPkSewTTPnbWSyYEtAMhh_CAfKVSTDIAmoFUhQRtuQNhmpN-mUZ5kkWHwvgTvnoPgTQFUbTXim3rsnsLknz25hnejzNMY_LkC-1GMTKe5j8ClQc4OyD8drveM6R6BbYJdLCB4wcDrfBaynoOe0t4lYdV-KV2-aO9qQIFiOw2x_d5VaZZwKsv9PA1uBUNOG94FBobNfyl2HzwEE9BqKcTwsrDlry2GdYvs1hWCftSNHo_XaZSWoxgSuvrOk4SOVL7tkXrQDmCWSehSIukOASkvh8HcEKFScyc8xxPXD7H4TELoyA6znwqR7hVS_XnzO2J6-dCSZYVVRZHFz8SUZz_QEitFR7UVgjrmNhMYFGBp5P23DAyHNYciuPHVeQfISU_ErxHylaoUoU3U2X-1rksVsUwjZV_iY2sQS46uAMUTVWJ_bCyPh54Ip3AZOFKJR17YH00ebzu0UMD1p6hFdZ2yEwcJaCZFDqFWYEYvJ1Qr98357bFYRoJVl29hbWB93X0qKSayYFifMRvHxlYSBXsK8eWVJEEMzyHCpZRwZIqyK_e4Het18Pbb1WwjGdjHZMNeCXkKqkUidJjpRieMLmOHsOMsmFFERfJURT94Xnfwnr9WTVzcOFcdJrwIoKQ46S0b_Qi9ZtVzMEdc9whQlGFUXLFY9_1Jlw0WDae2hyCrVgEXKdZ9KeSLPHLwxzmjwLREXdvbxCb0_fMEYWlYZGkwVWPXiMI8lRvtxjRgHc36SN0_lY28-zxthopO9OpraxmU89cMj-rjqKwP0HgDnfKceth9Q5Wlrwh-nv1rrm4WEYZE1V15eO_kUgdW93RIpbABfgKQoUTJmOISnncI5UqBvSmjNpccFEmWSHEoWn6MyULwAPq6k9nhPXo0hk6FFVR-HkcX_Skg9yyymXgIoj1zeZtg7KMgqS46JlrL7VOG5LTFCoonF3FRqHNmtxNGRX6ZoYhE4i9szKSF1IC3Phnwqu9f0u9__k_YA_mn8j7914W_puFG9F_vPXeef0O3BnRYYpwFh7hTEKwefkB0bVHRT-PQEFOygtdYmNmwJisbFwym7GMQxkeld38BZdEAEV7YagKzhmV1-6ZYVie-Dkvq-K6Z69BRBTmMMVoU6Wp8bo67mFmGZ5sqgSQUjM8FASszKNAHtVqbcnF6Df1HmkPfNAeFIcJxBqa6mxF29uWOQPvBCX4__5Rfu5LbFEj6of3gffEW4mlEyMHgyF6lNkpoWJSQnP8H_kyK2X8f2i_tjCmUlyDguJUwiEnIJBcY3EsRCB3ZwGNIEiZDOJDc__PYBLAZCJ8ck4kji6dOckw9GMmjiLxtz7pj6rSBv7ZYX3bJ1GNSvwHRRYMFCwahrBcv0E7JiEI_2XO2SnyLC0yedGegltgiSMkbNz3A_gTOwOHNbUEJlJVOrhVU7FSzUgl1SlGhX-0qUoJ-wPWnp89lKOL5xRUHuVhyOSFTwMmrgS8uOzanYtOIJvjC2fhGgyI1urkb9RyztiKLAnK_CjKfft2HASGSijAB6aUbf0JNtdwZUS07VUFMWNPKCFYmznvrxSZDKvwSxBJkQLIw7wt6x4U8Lgj9xyVjqaRYmy4dE7XcFkmwVHp8def4N0QfOiEFB0q2PN1E6fumKuZAAOfZpxf89y1sWTvvll5f_1GY7FoyOdrM3_-p83cQUVFBpQ-Oqj3Y9fhIvBJtR3785jsyRvmUKo0jqTg0RVPdex69Upxr1J1SF3EjGTdAZMTFn7MIj-vTG_FjVZP92AumOpPoG9Ms4O45zxPq7DIYPclC7MqLtO4KBjag6YdaE1TbqLbP7xqI6qP-1ZJDDyRnoQBiPkNmxd-xr6RbV09Oyu4vSTOItSlcmGbSd_K4V7WWHoERlV3s_RlcBeCXLCM-UWQVzyIoiL1M1ggziqWs6IoM1mIIAwDFlQiSYtQwJVRmgk_zcHdoHQShsvUlaJO6y5PfwNCY89H6Ifp2s_XYfiTH97F4V2U_Dvfv_NRZWuKIy8KVoncr4BVpk9__X_dw0I8q9pLNqzfENDCikgAGwhSu7SG03Gi2fkLt4roZ4vUD0KRs7AgF5me7XSPmGfPN4botYI0qhIWh76f52Ytp1dkapu5uA2ErzTGglWDE3yAnIsV1FQ8aSvQVDR-qgpD7zcq87yIIK4PM9_s1-kmmd79rc0het0y41mQCFFWMjDrOv0iNql-eftHXdVAqme0rqzR5VGaRlQvpbzOtao9PanOWNW1fX-iTkHXN4JUzFEuyNNU-DIIi9C8odN3YtInV7SRKP8NTpNsMxizFaVKdmDZwDzbiMC8PNbUVsOUTMeKMPREsHJTxxS3Hu6nEkiMrff3EdxCrdfNasaVJBIAp_FdPRBQZfwM01GIVoNKPYArYDcK1gOr0IJPo1wMUwiO-bpGe2KqeNzC6w4Wwfoj2PCozgILKB669mnuSNKUC5mnogrCbBI-23AzMfPndc7o1RPJ47SQEuJVu7rTTGMs7hVdMQJUKDE8Q6Dio_BcnWvAdRdNvXudFqJIA5lXeVkGlj2d1hq922t6ZCjgp3oNhSCV4F9QbpwCQPKbVF0vq6kkSDcpUPMinLyWPnMM_cpWo8OPYsfqLX5EQeowdk2v1B51YyAP7cSu7eATRs8GjwZiYj5izQQVjXg7bBwxWzYx60pnePAnldjBn6qt-q4TQIjGKFiT7OGK8OodMc8syKPasqdnkJWVEj74r1O_Uwu924kke1JmIBvE64OzkOJtlbht8EJyX1CkEOsyAonaSXV1ogokOcNgwkqZUDLG3GwvBOg6r6XEzvYC3J5wXi3bJDLOyoIl1HxMbON0PJkMyBWtS0gfUAm2gOLW-wa4Q5exGG6gOjvQfniOXGxJdmpTIanki9iQIHPlv640N9JHxAQe4hnAz_BgFac7x0r6X3dEkMUc1oq8wpaMaGWpPegTG3RMtUCbRerwhNoC1YZN3J3Q2CGtDCoBbb5hzd4AirAulVMONbq7egU6W6eCSpk2FAsTzKMGR31P--ioUA0lG5S4APWMv-qi6lPVMbaIYc7chZmIZBgnIrCOjdNqNunWt3SP6TVlDsYyFZyXoXU-nIaylz3Gn90jJiybeP3HGqIDrKsFw_5I5o-6l1YoWkgr4jTgaeNnwOLAdljUyuBtyLkA01thEgtYgAuwpz0yL7AyBAiouMH7Aje9VlUpB9XZrOmfRDdnumQWVIEfl0Vh_SWni83xJi5tTLOG1qh4bZJfmHjQXfhGrZJTyy-oO7FFXomRVkvaWP1tBNmUzyY7jPeRD1APCNofF7HDtaDYtF-jzL46PUVuuHCGUD4rpUwrcKlzGyg4jXUOoS7uldNPqrDIMimDGP5nnuS0z-knXdURpxT6L8bGwG3R7ZQrVBZWpx2o1qglGC--VV5A96iOlpLssEK7792CsvJZ19wr9Tej9AspsiLPRSULK4dOR94k229pstNr5oEIRQm2JCysIXH67kzdzhWtdEf2QOs34kfGH9Ff7q0DAMuR01SJE64lGHfFplqJK6r-ifW43o-oTXGpd7aTzmwTa_hqxFVOVz1qQsSBkFEasDAvIyvZU6vfxEYXd-8pbturc6ciR0RltG926DVp5whpZ5lNkII6rD_WNytmIz8C9AF6GapW2fo15J-hskTlCDxRkcMEnEcOHNye3NqskLcZd8rDAYUNe4GDwNAEoSkdgSmG_5suNaPADpPtHayT3lLNQC-FVtb6tNHlkXBsG61bQK50PAc3Zfjwft82lD9pNPEOXvOgCJmQsHbssVKOfEIPuxRhofx2qv3Bj3qsSemxrgRMhnigl7beGVxfnN4tHSJ8HfjTcU1RkS1-1ofUiYcaWfCF32Jc33E3I9M8L2IZJLlgkQU1nF5OE4Bf0Z7JKWtvkhRql0x7FLfeQeU7rc0hlGiobhlDxhq-tRbH61sluAdhJPq3DNzkanCohFGTJt4crlFERSWSOAnzMJ0wHds0Oqm0t3eAmpUTIRPup0xwG1g5TaFHnY2XdHha3UQ8pBoIVeiP97YfCQwaUSlAfCjmfDaI_5iMRSySyYJNPaI2Bry84ZPCFrg9x9tF_bAZ7P3DU3t8f23WnSKZcc-pzI4RZwgbgykhMMsHIQr2hyDFx7gu1gBR8qbdcpeZIGoEOoCfvDUqVe2YeFRtWzOrydLQq47gkIDIKwdc2xR4qFGyxuOZi53igPGSyaCcfDin7dX14S7sYUXciHIzqvLOTXXphiztkB35_iqUwgi8ETXhPOAEPxK7YVwJAeK2befcU1GVQR4nfpbl1po7XbOTOH1W_6sBVqJQVAFQz8EgnZZYu_iFTa36KRn3fSkKJqKIW0Bk6nN1TufSTlXYwd3EO8ZDXlmUxIE1NFOtXIOM7GlsI6Y9jEoFS8-w9wzOvlGuiYNYki3ABpwKgxZELClqLUFfk_V3C6xBAcOpIwtJsOkEKio1Qy4TvZ0YKNZV6pXcIxocBS-IPNhQjpDcLyxYmuGXLM54ERbM98lXVtHi1K3rHukFDbf6ISErI1nF4FdVicWYpx7ct5zomTZar56MAqq0tt3qU1FquBwh1CTs8j04cN80VjetXsHVVNQ92b0KYjZ3NNuBx66OH8IzddpkG1fa4zQBvoEnbBSHdFLYE2JizUNv4jxbpGtqXg7iuJmzDIXPg8pPiyCxDqzTRPwySv_sPmC0gOjqNAMF48iu5n0owMYF1YfoYVhoUWc0Vwc2E71NiNMbrjGfTQ1aszFAh8P29Cj36PtxR7VmEJc9gpiSagHanW5iNc5AEUV-5ocioHYcoo3Tuuzy-YWdx0ZH-lGRJkFQsdiGvU4zsulTuqKXeEqIODUiRH7MEiAMgLW-T6BREFdQtQFtiVEoNi_hfdgCLDT6P5X5agfmFihAgV2j3llLuk3UqzhF4TuD02isdZHTYzxzHODwQcyZZJlPaUZlgadG6AMU5eo-ZpO5TAuWp6CEGLNW32ltdrOHZ9uVDfJQQUAuWZ6k0jqvTgez8xqXdiW7DTcaONbl85RZY9WzaheZIXWZgycM0XxcWIZ0Gppdzn9jf7IJXNI8TmVeykJYV8NpWbbAweUdyFh0XIHipHwrZcnIPTcVyNQnpUuPNVJLxLXdQhAc4huZZCOpEuAUfBdlHIzWM91_VjkrqdiI7b5X7pk2qcZSzDK38MOySKskKzIHIrQd0w7FP7fx2eqYrEwjKVJ_orzTC60fcE1LsyKW8vmd7IhjZVdHKMGUlaHAWyvtyVW37jllG8hBV0dma1UO1Yg6yVJUBA7Xw3So5tAIE1U4pep6eySOAEONEC-YjyfWcYVhrgmbc8y5wuBVTazKQlP4Sl67mLexQHXJ4d_YusBOk7dztm9q2zYYXBqWGP8JUVkZdTq5rdG4vDebHFf8qKfMxeSsKNBndVzHj0TsphNiXtcCFwyNVYzK3o-EX4Gz3Fj9pcwKmSbN3WtrYw5PtO4VetNZhHuL3RXPaw6-cqOSTtx6ZGvtJwEjIPfW_W7O3Isyigq_KsPJ3Ds96JOu_-xOciPjeR5kacSDMrIn5jSXO5r_0hZxqu4iL5c8-7UCC80uYYNKBkAE64aSC1RLgdIMryQ6AiWp4kQ1Ms8Ry89y8IWKUKTlhJ_bLnTnXT6nl9zkSyKw6X5acj_1Jyth28sttHFFkzglHhlne4Lu0BWnF4dIea8vRDcGC0t7-LZsP6lEPvLamoJ0HRyaIh31qCeQXRu1GrWkcstuLxB4x1Rus6IbNGABKm9QQQjdQN5V1dXYsYifrkEAVioyWVE7eVM9r3TAYYE6EML9AArPJJxtMbDRARpC16Bfr_JIL7KatCwow8oW6CiwUpyyuo4bqDaOUvxJJWHoSHSqpu1U6kkxtAaSp9oYkve1DRbARzmRtzwGZZIogBAxlHmS2CDR6fGfHOeLO_XXG4TNbDk4vvcR0v3E6kGlCqkASHZM2Ts4hpV1eA_qtrB-e9hRQGS9tpI8B66QSgzktLv-PqBr3odzSGBcyCqr0KeyaLAzRmBSXJdMAjA2LJGRLIskFhPA4gwHOCgduKy_H0vZvHdOwogErgFBWf8iuhZ4p6qUPwERFfYiIh6moAvKMqDyag7CbUH2GWKTF3XZWhNNScNSuD1U5WEvgE01zulDJrOEJQWPEms8nLEEttXwLZMFbG4pDlIIA3NFYoWcTcMGrBa8Yl7AK9C0Mv90OwkByOykwFTnrkkIEcQE-1dXA5uDMaqHKXOyntBgEB0nz9GNW33Ty4oI0lGYIMATIPBqo8pptD5TGvUwjXFY64CvrVrgaUn1HNMDv97CV9sJRnOK8LxN_bABtUR5RYycHlvwAQlA1eykWhVRh0xXAYEfQUu24MOg4rCqjNLl5MzVW3RD5-DlMpEs86UAGzqlNOzIBlN_dsXUhYNgWJWOIp74ot3NVqRVG8FHxHCwgGbsSqaBMtB7uz0Cmrp6px3RhCm0TANoRtTpkK2CAyfvF8TVlHQd7mecRam4jIvQDzOIP6spOrKjIiYN97bZD6ZCpQhLnyVhFE1VdM44CMcvf9t8B1PEUGGIX0g_KCxO4Yx8cBIzl85w0J16KmdmMWn9Zx88XEuLlnnEdOvBgwZTcdKZnKx9GK29Rk2ytiCNka0eOKFHlE8_419UKYTy2J2CiNOPULuewioS9il9yGwEeFjH5xZUUOQBwQgwDzKpLiQ0VRaUVNJMzCGcYvxgNyqMRRo6pR2uCqBY5EOMgv0hV_WO5BOYpM1KF2Qf4i_l84TJzch5HskkLdKoZOkUA0xzNxye--zpGYarpcxZjH-IRFr2cwZqWPa7fCyGdvRM7L5W9XiqQlnl5tc6xb5GFW3K1pj98pR1IMClxgPQRkHt7rDKz0KTJyqfsL76KJ2nHVLqytdlpuRAay114JNjcR_ynM6-kWM85-yqCRhULaj2ZfLe5PqPEJCgt8K6mjIqqs5WbQdbsgZxVP2jwUipu-yxkHKGi4BdsEWlKMOp7MSZSOJy0WeNFjEJnixmVSiAJXOrbp1pI5aFrhgbQhVNqlDKUOr5kCJU1KFuVmhBr5q0aY3XkioGqtN1w3SDSkIoYJw0B-UkKL-AVntUEo0gujGV1o1RNWuHkXMP4TWV8MKpbhmEDDPnxOLYz1jp58VUz-ZMRdGEvGa8yVTo2NNJr6y2WNlDnzGsuYhFzKMoCULLSM5YFKeS4syEDdMhA8a0KkUcxZn1WZ0BKCdM6rl5JrZej-WMFZkQpV3YGXFiIr0rJpZo1aY6nxkG20djPowpc8v9rKl6UfP3Ap097pOwmquj3u3H8_moWARoJgqWTm1UzjAVV-rfPBnF8EHm-7EPC4dsgnOmYSlW4i-ffKIaCrBShD52BF1pjFfh_FsUZfNcbUqEQunBbYIjtnMIFF5PIowlvVO5vD1TsvpTQSUtjRgVLE9VhWhyV9gbq4sFV-qp2JqiNMMhK71kHldRsD1Qg9xg1XHb6Oo_DfGuCeLVwOjrKiROyzQBbVyWUyrGGRXjHPrnTH0xUsUi8KHzPBWhlSpnEIwZBXrFTBfeCpX2M6XcRwCvm2ex3DQ1gJG-3rx05lYal8I3dIporGPGehd8Rk1tLIR7QjZZDmdZdi3jhz05Jls2W7DMc4hBsqKUtm3ImVUz6c_zA2gM0CJlmGRcpHluJdGZSXOqVvz8oBmz2zLNg4izrOQ29ejMnrFSfs1AmdDNvuoCobsJxqJrImzpIY9ftzeC1ujRB_cqsd3ORcmg6oJC8pIltk_BGVNjiXPV7Bll-wmXsoH1ex-rSRAH0YihKtcyqgbjbIK2hknLT2R4Q26blXEZ-xyixqqaUkR20M2L6rLPn17jNFmuJujDQm_aXVA5f8JKNWhBUb7FN6lQYxxarLKoCEVS-QfVRYziKaxUzaXyE47F4xBo576DdpgZOpPYfMY8HOOBBDFPKsajfEqyOCNyLI9fPu5Gk9YN_mz6yk7nsDCmMl8K61CxLoUW74OvQKfuWd2ZKm2s1NhhtYqiqwp88ME600BFJc1A6_1nIfZTW8vKpFQ61KE96Feb4VCr4Onq8iYL3li8RiH-YMCtnbaAvU6WaCgaN6v0gRbrW-WJU04ezeq2xGQd4kGUV5qIKD4RPqE36QHJ4CAHrGxr7WwKfGu14o8mKajozkU5PjzQ5sjSooa3iJpxchWCqFp7-h3EeDRaR5erWBxX8yU-5Ady-BF7mcIE6u7DrDTDuqHaNguic8PXKOeEuZEjACu1QDGkkkr9iE-6YskEDfSYfwFXA-Sj0R6iTkOqEwZSUMGeC69Z1I1S1ohBw2IIjdJq70bKEU3tL4p8iD8S8kNve1gTZUEbq5dMMzWVKGlaEE2P8VHKillsSgGGwEYPOpPemjIwQuM17fCQHzrTJ6ozAJONp8f9c0tqBLQKPLE0QQ8Qwna7gfVuyQWABR35RFUm-j9oK48vs8NLmRsNHhrwTyAxdCYjZbBP5AttqnDG6mRVlGOvUMXiCVGZBlu5bfRXTaQyHl9RJjkvIAZPrAZzhlQd1jldNF3KVEra7AmG75p9xkb53aaehbiAUPA3Rfu2Ac3Ac247pHUGKQOmW6FNZl4dJeaiz841kGDx4yj0hc9sssUZi3W6n-6z5lmhpXcjuAmuZBWENuOWcDKnOMZFOXQFko3T9amY4tIXEeD_-m__3eQJlco7gDQc3A0unCpfmqreH7VMwBOpGRLlhM8FkkkuwbkI4lTGE0PbMV0TQ5-fvWXSX6nMJPdzVgorIs44LvuXxS6fsTVXL5CLElgiD6sgsrVNzuCtqQvr8mlart0HFb1jWsGBIK1NC43R3ar5Cm9XVt6pS12jK4g2ag8MZY5YNWIRDVxTQJaNwlxVBaOy8N2zaryiAmebZiFdr5rByJipkVg0Hkf1V1H_k5PHV24kFRL2WjxVTxU2-TSWEiaqUB6k61r0k9dx4E0IwU1tu1EFeEqUkMhpeW1JqJNX1yOYsL7XOQ_0eHYqkpwPCJhIsySueBzn8cFQCDXdzOXk8wPLjLovg6xgRewXvo2SnBlmU0n0FxlLZsK-NMsTMDOxSKeq0GlSmXVbLx8-JjrwYmqF5Bunn6Ix7dcZXt2PGIsxMuGnWJehEzJVelhHxCnA6nVSQf-5cgzvdOhB92mP04FNTL-cE35MSQ-TUJ0KF1Dn2R3YWMaEJwOZEVM2II8SYDSVYMbWsyiXgcjDKLYBvTOb7dThf-a4NdJwTz11K2GSkt7WTIyoCKI6wkja7mUKSJWWgEAKBS2drnA1RXlzuVXguzSPqjIQpQUcnLlvbvfPG6e4mSlBRRmnRZWESWDLUpzBbpalLx_Tpv6C_dPT062ab3XL6q_KbfvwVT0ts1Zf9WuqjViT47O20dnvVt6fIKBPVx5O3CL31N0OvrIqIHx9M3jy3zTrDy1WKL6fJkjMbvDkZtZ1g-VGvVg7gyhgh_9pBO4Owlf2eHpKh6kg1Nr2os3QCmu9gqZU-BqppgljhLehsWy75-m54CltxvIWmFcPI4OnO_f8bg4CFWFZBTLifmSdC2cMnzOd4o1T9QwcJkMwFSGOw7LJD2fQ3ouaps-fm6dqW7ELz6nSWdHPdjjYq8HLVHZEGPWupTZbiRFNScNAdFqeRnKYHi4qtCCbetCz8xF1Ms2yQa8UfXY94oaAnSeDn-KNK128bpLrbhfNQYeNG3dQ0bsdVmVRevKRIGigbNkjzkU6zN6-TJJorIER5k5V7q8kbg7aZxW4TJMpbB-xrVtwx4uRKtX6RTXMYE4U6x5YtVEI3gtV-fNvyDN63uGvN2pQBv6EFZuC35fPN3d_vfl-L5p334AC4OLTDc4m1AWFr3ytkJGZr2l-l_3-hxpCi457P-HfWPv5t9WpGX_ffv_df7z_8P0P3_zX77-7__ov7769v3KQH_gRNM8JxzuCla1xMCHYWnmPBSadGvaoMl5IDT14kqojcbYj2yEJxwantuAHOsGjBjnCG-hYieYE2j__Mg0FnMZcYs-s7eTGoXLTuLo_b5kz8xL8Umo-OyH0QFKSk1cf93IJPZzyB4FvomTcprWGelD9Y2f2dquebF7l15unDY6r_JMaX-VC-BQe11jysH3WAqjPVQNpuAuPKoTPPdTTLcKah5C9Xfb5g0mdqDu46OsH0mI0jeEJhdRiALc4WfLNkz6DIol4WOWBX8QVkzJlCbjh-TTp0x3h6Y6vdMd6_vp_nTHePq_Uzuu0C94Fv50eyHluOukXGUFappnPcRAcgukVT0se-RGEKSkPCxEmKeiXjBcQlvNYRnEcSPi_qFge-dKXVZK-_kqnhpBmd1F-YggpL2VS5iI9P4T0iyuol5NGQ8E5UCOX2eRznpo0ep51lomiy0TRZaLoMlF0mSi6TBRdJoouE0WXiaLLRNFlougyUXSZKLpMFF0mii4TRZeJostE0WWi6DJRdJkoukwUXSaKLhNFl4miy0TRZaLoMlF0mSi6TBRdJoouE0WXiaLLRNFlougyUXSZKLpMFF0mii4TRZeJostE0WWi6DJRdJkoukwUXSaKLhNFl4miy0TRZaLoMlF0mSi6TBRdJoouE0WXiaLLRNFlougyUXSZKLpMFF0mii4TRZeJostE0WWi6DJRdJkoukwUXSaKLhNFl4miy0TRZaLoMlF0mSj6_8VE0Z9_-99ff_oF)
