[//]: # (ob:cb2efec0)
# Proofpress Long-Horizon Contract Negotiation Evaluation

[//]: # (ob:b7f8b55a)
## Status

[//]: # (ob:f5ea102c)
Superseded historical research plan. No benchmark runs were completed from this proposal and it reports no independent experimental result. The completed successor is the [Harvey LAB-derived governed long-horizon study](../long-horizon-eval/relaybench/README.md); use the [archive map](ARCHIVE_MAP.md) for the retained receipt-bound planning sources.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFiODVlYjE1OTU4NzJmYTMwYTYxNTI2YSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImQyYTNjNjE5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84ZDU0N2E1ZjE2NWM5ODU3ODFlNjYyNjUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q3ZDAzNjUzN2RhZmMxZThiODYzMTI2ZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfetu40iW5qsQnh_T3Ss5eb-4MT-ys2uRuVvV3aiq6flRk_AEgxEWOyVSTVJ2ugoF7EMssA-0b7JPMuecuDAky5QteWawAFFAllIig8ET5_Kda_5yxbqhlowPt3V1dXO13d4GZZ6IMkiKJM9CySKfpUESpuxqcVW21eNtVd-JfoBr-xULk_Sm5CkL_bAMeJjnme-zIoiCqAz8Ki9L-FiGMmd-lLMqK1nsxzKPU84TxmBtmcQS1q3qnrf3onu8uvkF_zLcDuwOnrBmAz5qAR9KsYYv_iq6WtasXAuvE_d1X7eNt4Lr2-7RKx-9v3RtK7ed6Hu4Z8v4F3Yn8KX2vu7avwl43V2HC66GYdvfvHt3Vw-rXXnN2807vhLNpm7uBtbc5ZH_bu_uTvx9V8Pn210vulveNr1ogBZDtxO_Lq5WgiERq5BFPA2KK_XNrbini4C44javkjhjiQzShBd5kuWBSNMwTXBnbTfgq92u60bAzs2JrG-rrPKjNImyikkeiLzM0ygIU6FeR-_ulrNtv1vDC4e4T952VX9189MvV_rxv1zBKbddj5_Uz6K6LYHkP139eSua95-8D20lvl59hhcxTIGnPOyqWvTvVqy7F49LOIklvPbQwa_LRty1Q80GOIblum3ulqu2q39um3fff_PDN--___Dx9i_fvv_T9aa6WryKz9gwdHW5w3VvS9bXPe5DrOUt64Hsg6D1dgM8DV_mS93gkv1jP4gN_NKwDZ763kst4P4e2eXqptmt1_CKfAXnKxSFynXLv8AtvAyFFNyHy_EdxVckwMhU3rf4jh_VO8LCigrenxQV4Ca9E1ZVtMUt8qh4gG_-wXvpKvjO3jf3bL2jj7DK8LjF10FOAq68-nUx7rfMZF4mCdvb7w8DG3b95G7-wbMXTawuE8ECP-SvXB3edNv2ogIJ7QXr-Mrbrllz7f2p9UrR8NWGdV-8btf03ordC_hONB7I3XYtBjFuaMs6trebLErStBT7u_nePKItUajre3HivY_eMEGDJE_j2E-iC56qD1N4DysxrETnskK9Afm9F70HPwC91qDa6nU9PHqsqTwh5QQ9ikJGCRPhBTv7cSWcI6lhO7BOA1d5Q-ttBOt3nfDgi-XQLuF_HuxVKili64mdySQvZVZlezv7l9WjZ_SG5-iNE-c1cdvEqQVVVMZJlV68gw9HrkdCMTgstgbaDKLbdnUPh9t2X-S6ffAewJIgpbZTFMqjWIayunh_S2Kcdis6hoftGSXrae0G29wK4L1q_QhXdu3ubuVVHZMDvMK4vzVY0L39xX4VllEYX7y_j2Q0_hF0nrgDer2_A4p5f7As95tv3__ht0is-7oSSNUtLl5zuJTM_nP0A3wRFr4o9_b3Yc3qjVe2u6ZigCSm-erJxRPcxIQIZCnDM5_minvvNe3gia9bEE4lZloDeGsi0JemfViL6k4sPL5mroJ-QgNexQC38uTMXaHsb42mRrnvECVo9m5Y17UPorvxyhoVEUONYpmMT-yqEgJ2lcQX7EpY4-dtdv2AHN4J2YIqQmQIh7Or-9XNxB58sBQ8zviZewiuPVmDhvMG1n_x_r5jqJB__69NeO2B0WJS0Y3dqS22EliVAR5tO_h5SqjyMK-yqJJ72xplYdfUwwmmfXLxBNPmQRLkRcTOfNqfG9c0iG3dA4xSmq9_bOBIQEo9QGh7NgGUDKrFKaYtQJKEzM_cFRyN-kxqr4arazgndtcJsUHNAodSN4plCFKw5hHBx2PZtl8mTibLhQhjce6uvkHxACa4E4phCdYwrwI804EjgUzL0biDQQXeAa9EDAujAyZoVWYAj4sDJWxgI3oe4HTwF5jQZ26Z4B1fxiwPs_SiJ5vr1wJcqRWyTiVArkDblI90QM1uUwIaAgEiN-rvO9Q_cJxgWqaEu2LgQVWXUWXp_e53H-Ob3_3Ok-2uU2fXL7wWmF67CVZTLEBje2XHgBkAEnV3YoqPSgm2oryMbqSY6zWYiX7V7taVB56m9zEmRPgxvybvAcimPa3eXFUCy1UTdBNlLirmi729fQNM2NUoOkB3-LqqcXenfIfn75rSR6zkeVrtu1YfghvQm3AtENoz7i9BqR7k5ASWByN-8vYp7yYORVLF_K029CMheC7qe3gSaCLUR3di6K0yQv9mXHwDPi4co1p6Cur4ZVoycUC38MbxIpbEq68g26m7p_whKdMyLJM32s4k0Xrw471-V4J4NgQ8ZL1GMZW1WFf9YoJoKUtEnkn2Rrt0ENyGPaLqbvvRnWOoPwYyjvcUnhLVQmGCBZioiV2GaQhARR5woH9DKLtudu2uX-ofvN0WZE4ppZPH-5IVpuBulPEqFMEbbus9QDd217RkCa3GgJMf0F7vS8j4FKWLp0ICUvqhz-Qb7lTB4nqDIgq3yroDQW3pLwAnwNNTAPlDiGfdwx4_BNdTRxwHUZHH4UEIhVgJHakvp-M0-9dOnJvAwGDM0vOehS8u2zV4sCiJ6noFZ9CyALh7_BlMdy_wFQexVhEK-r1pp9QXjyPGy-oAiwsGwAAMmTFjJ3n62B1TgbE48WVeZhc89s8NvKRV167_T_HUnghg0EKrNDlwGDnek25byCNRFft2-L5dkwZ0H0Na5RRhJu-cIFAUV0UQiOwNtvEtQ0OmMBRgkApdWZDvDepEHYa4ASXZAGrnIH4YMWHdgOZ1UrirNCiT-MDr_gQf7joMkEm2Ww-nqPP08inUW-RFmh7g7Vc88L2KjoAMoaCA2RIDOtZdW-04BTeUn9iJCuP7C29Tf0XXu-93op8EAHnkR8E-w6hACnLginUNSjjZye4kx3jTd06QJxOBFGWQvcU-fnS8txr1PoFJxW4azu5q-BP-jrZhuyvXYDhUMGnS8Q9EkB6Y_Qu2aC80u9KRqqngQxkLP0_KNyHTkowMJle2dYOe07fv_6CiEihcHVBPaaFuV3Y173__r80S2EwSX20m_JQqkHEUZclb7BFM-66zKJkioB0IObgHhJVKMcoAaAZSFRK05QaEaUr6ZRrlSRbtC-OP-Oo9ONLkRNFeOVvXZfeSSPLJmyd4P84qPyyr5I12oxgZT_MfgcoDnB0Qfr1ebhlSnYNtAh1swvGDCa1UtZT1VOwtqXge8vCtdvmDvYmDAkR2m-L7nJdpFlT8jR6-BFjRAHjDo9CxUcNfis0HD-MpGOrphLDysCbUNsH6ZRZLnrC3otGH8TKV0mIUprRY1wFJBKS2bYvWgXIEkyChSIuk2A9I_Xk3AAgVJjFzCjkeuXyKw2MWRkF0mPlUQLhVS_WnzO2R66dcSZYVPIujsx-JUZz_TpFaKzyorTCsY3wzgUUFnk7aV4aR4bCmojh-zCP_IFLyA4X3SNkKVarwYqpM3zqVxeIM01j5W2xkCXLRwR2gaDgX22FhMR4gkU5gsnChko49sD6avKruEaEBa0_QKiz9TGbiIAHNpNApTA5i8HJCPX_fFGyLwzQSjF-8haUJ72vvUUk1kwP5-Bi_vWdgIZWzr4AtqSIJZngqKlhGBUt4kF-8wT-1Xg9vv1bOMp6NBSYrQCUElVSKROmxUgwPmFxHxDChbFhRxEVy4EV_fNy2sF5_Us3sXTjlnSZVEYHLcVTaV3qR-sUqZu-OKe4QoeBhlFzw2Pe9cRdNLBtPbSqCrVgEoNNk9IdLlvjlfg7zB4HREXdvLxCb4_dMEYWlYZGkwUWPXmIQ5KFer9GjAXQ36iMEfwubefaqlu8oO9OprSwmU8-VZH7GD7yw78Bxhzvlbu1h9Q5WlrzA-3v2rim_WEYZE5xf-PhPEqljqztajCVUArCCUO6EyRiiUt5tkUqcAb0pozblXJRJVgixb5r-QskCQEBd_fWEsB5cOkGHgheFn8fxWU_ayy2rXAYugrG-ybxtUJZRkBRnPXPppRa0ITlNoYKKsyvfKLRZk5sxo0K_TDBkAr53VkbyTEoAjH-keLX3b6n3f_8P7MH8EXn_5GXhv9lwI-LHa--9128AzogOU4ST4ZGKSXA2zz8guvag6OceKFiR8kJIbMwMGJOF9UsmM5ZxKMODspu_4pIYQNEoDFXBKaPy3D0TDFslfl6VvLjs2UsQERVzGH20sdLUoK6u8jCzDE82VQJIqQkeCgJW5lEgD2q11gQx-lW9RdoDH7R7xWECYw0NP1nR9rJlToR3ghLwv3-Qn3uLLeqI-v59gJ6qVmLpxK4CgyF6lNkxoWJSQlP8H_kyK2X8H7RfWxjDFdegoDiVcMgJGEiusTgWPJCbkwGNIEiZDOJ9c_9HMAlgMjF8ckokDi6dOMkw9GMmDjzxlz7pD6rSBv7YYH3bV8F3SvwHRRZ0FGw0DMNy_QrtmAQn_OcpsFPkWVpk8qw9BdfAEgeRsN22HwBPbEw4rKklMJGq0sGtmooVPiGVVKcYFf7BprgS9jusPT95KAcXTymoPMrDkMkznwZMzAW8uOzajRudQDbHF87CJRgQrdUJb9RyytiKLAnK_MDLffl2nAgMlVAABqaUbf0VNtdUyoho26sKYnY9RQnB2kyhv1JkMuThWxBJkQLIw7w16-5U4HFD8ByVjqaRYmy4dErXVLJMgoPS42--wrth8KETUnSoYE_XTRy7Y6pmAgx8mlXVJc9dGkv2_tPC--mTjsWiIZ-uzfz8m9XUQUVFBpQ-OKgPu67DReAbvt71p2OyR2-YilKlcSRFFV3wVMeu82eKe5WqQ-pizEjWHTA5xcIPWeTzwvRWXGn1dAvmgqn-BPrFNDuI26rKUx4WGey-ZGHG4zKNi4KhPWjagdY05Sa6_cPjK8G_bFslMfBEehI6IOZv2LzwGftG1jV_dFZwe0mcRahL5cw2k76Vw62ssfQIjKruZunL4CYEuWAZ84sg51UQRUXqZ7BAnHGWs6IoM1mIIAwDFnCRpEUo4MoozYSf5gA3KJ2E7jJ1pajTusnTX4HQ2PMR-mG69PNlGP7ohzdxeBMl_833b3xU2ZriyIuCcZH7HFhl_PaX_-oeFuJZ1V6yYv2KAi2siASwgSC1S2s4HSeand-4VUQ_W6R-EIqchQVBZHq20z1inj3dGKLXCtKIJywOfT_PzVpOr8jYNnN2G0i10DEWrBocwwfIuVhBTcWTtgJNeePHqjD0fqMyz4sI_Pow881-nW6S8d1f2hyi1y2zKgsSIUouA7Ou0y9ik-rnt3_UvAZSPaJ1ZY0uj9I0onophTqXqvb0qDpjvGv7_kidgq5vBKmYolyQp6nwZRAWoXlDp-_EpE8uaCNR-A1Ok2wzGLMFpUo2YNnAPFuPwLw81tTyYUymY0UYIhGs3NQ-xbWH--ECibH2_r4DWKj1ulnNQEkiAXBatakHClQZnGE6CtFqUKkHcAXsRoX1wCq0gGkUxDCF4JivazQSU8XjNrzuxCJYfxA2PKizwAKKu659mDqSNK2EzFPBgzAbhc823IzM_LrOGb16Iqs4LaQEf9Wu7jTTGIt7QVeMABVKDM8wUPFFeK7ONcF1N5p68zwtRJEGMufYZmrZ02mt0bu9pEeGHH6q11ARpBLwBeXGyQEk3KTqellNJUG6SYGaF-HktfSZY-gXthodPooNq9f4FTmpw65reqX2qBsDeWgjNm0H3zB6NiAa8ImrHdZMUNGIt8HGEbNl47MudIYHP6nEDn7ia_VbJ4AQjVGwJtlTKcKrd8Q8syBEtWYPjyArCyV88H-nfqcWercjSbakzEA2iNcHZyHF2ypx2-CFBF9QpDDWZQQStZPq6kQVSHKGzoSVMqFkjLnZXnDQdV5LiZ3tBbg-Al4t2yQyzsqCJak0bON0PJkMyAWtS0gfUAm2gOLa-wTcoctYDDdQnR1oPzzHSqxJdmpTIanki9iQQuYKvy40N9JXxAQexjOAn-HByk93jpX0v-6IIIs5LBV5hS0Z0cpSI-gjG3RMtUCbRerwiNoC1YZN3J3QsUNaGVQC2nzDmr0JKMK6VE451Ah39Qp0tk4FlTJtKBbGmUcNjvqe9tFRoRpKNihxAeoZ_6qLqo9Vx9gihilzF2YikmGciMACG6fVbNStL-ke02vKHIxlKqqqDC34cBrKnvYYv7pHTFg28fovNXgHWFcLhv2ezB91Ly1QtJBWxGnA0wZnwOLAdljUyuBtCFyA6eWYxAIWqATY0x6ZF1gZHARU3IC-AKbXqiplrzqbNf2D6KZMl8wCHvhxWRQWLzldbA6aOLcxzRpao-K1SX5i4kF34Ru1Sk4tv6DuxBZ5JUZaLWlj9bcdyKZ8NNlhvI8wQD1g0P6wiB2uBcWmcY0y--r0FLnhwglC-ayUMuUAqXPrKDiNdQ6hzu6V00_iWGSZlEEM_5knOe1z-kkXdcQphf6zsTFwW3Q95gqVhdVpB6o1aimMF18rFNDdq6OlJDus0G57t6CsfNQ190r9TSj9QoqsyHPBZWHl0OnIG2X7JU12es08EKEowZaEhTUkTt-dqdu5oJXuwB5o_Ub8yKp7xMu9BQCwHIEmLo5ASzDuik21EldU_Y71uN4PqE1xqfe2k85sE2v4aoyrHK961ISIAyGjNGBhXkZWssdWv5GNzu7eU9y2VedORY4YldHYbB81aXCEtLPMJkhB7dcf65sVsxGOAH2AKEPVKltcQ_gMlSUqR-AJToAJOI8AHNyeXNuskLfabRTCAYUNe4GDQNcEQ1PaA1MM_zddakaOHSbbO1gnvaaagV4Kraz1aSPkkXBsK61bQK60Pwc3Zfjwfts2lD9pNPH2XnOvCJkiYe2ux0o5woQedinCQvn1WPuDX_VYk9JjXQmYDHFHL23RGVxfHN8tHSL8HPjjcY1ekS1-1ofUibsaWfAJbjHQd7eZkOkqL2IZJLlgkQ1qOL2cxgG_oD2zoqy9SVKoXTKNKK69vcp3WrsCV6KhumV0GWv41Vocr2-V4O65kYhvGcBkPjhUQq9JE28qrlFEBRdJnIR5mI4xHds0Oqq0l3eAmpUTIZPKT5morGPlNIUedDae0-FpdRPxkGogVK4_3tt-oWDQDpUC-IdiCrOB_8dkLGKRjBZs7BG1PuD5DZ_ktsDtOd4u6rvVYO8fHtrD-2uz7ujJ7LYVldkx4gxhfTAlBGb5IETB_hik-BgXYg3gJa_adeUyE3iNQAfAyWujUtWOiUfVtjWzmiwNveoOAAmIvALg2qbAQ42SNYhnyneKA1aVTAbliOGctlcXw53Zw4pxI8rNqMo7N9WlG7I0IDvA_sqVQg-8ETXFeQAE3xO7oV8JDuK6bafgqeBlkMeJn2W5teZO1-woTq_qfzWBlSgUPADqOTFIpyXWLn5mU6t-Slb5vhQFE1FU2YDI2OfqnM65naqwg5uRdwxCXtgoiRPW0Ey1cA0ysqexjZj2MCoVLD3D3jM4-0ZBEydiSbYAG3A4Oi0YsSSvtQR9TdbfLbAGBQynjiwkwaZTUFGpGYJM9HZiIF9XqVeCRzQ4Cl4QebChHCHBLyxYmuCXLM6qIiyY7xNWVt7i2K3rHukZDbf6ISErI8ljwFU8sTHmsQf3JSd6oo3Wq0ejgCqtbdf6VJQaLnfgalLs8gMAuE-N1U2LZ-Jqyuse7R4Hn80dzbaH2NXxg3umTpts40IjTuPgm_CE9eKQTir2hDGx5q43fp4t0jU1L3t-3MRZhsKvAu6nRZBYAOs0ET_10l_dB4wWEKFOM5Azjuxq3occbFxQfYkIw4YWdUZzsWczEW2Cn95UOuazqkFrNibQ4bA9Pco9-n63oVoz8MvuQUxJtQDtjjexGjBQRJGf-aEIqB2HaOO0Lrt8fmbnsdGRflSkSRBwFlu312lGNn1KF_QSjwkRp0aEyI9ZAgwDYK3vA2gUjCuo2oC2RC8Um5fwPmwBFjr6P5b5agBzDRQgx65R76wl3SbqlZ-i4juD02isdZHTYzxxHAD4wOdMssynNKOywGMj9F4U5eI-ZpO5TAuWp6CEGLNW32ltdrOHJ9uVTeSBg0MuWZ6k0oJXp4PZeY1zu5LdhhsdONbl85RZY_xRtYtMkLrMAQmDNx8XliGdhmaX81_Yn2wclzSPU5mXshAWajgtyzZwcH4HMhYdc1CclG-lLBnBc1OBTH1SuvRYR2qJuLZbCJxDfCOTbCRVApyC76KMg9F6pvvPKmclFSux3vYKnmmTaizFJHMLPyyLlCdZkTkhQtsx7VD8tY3PVsdkZRpJkfoj5Z1eaP2AS1qaFbEU5neyI46VXRxECcasDDneWmmPUN3Cc8o2EEBXR2ZrVfbViDrJUnAKDtfDeKjm0CgmquKUquvtnjgCDDWGeMF8PLCuUjHMJcXmHHOuYvCqJlZlocl9JdQupm0sUF1W8GdsIbDT5O2c7Yvatk0MLg1L9P-E4FZGnU5uazTO780m4Ipf9ZS5GMGKCvosDuv4kYjdeELM61rggqGxilHZ-x3FrwAsN1Z_KbNCpklz99LamP0TrXsVvelshHuN3RWPywqwcqOSTpVFZEuNk4ARkHvrfjNl7kUZRYXPy3A0904P-qjrX91JbmQ8z4MsjaqgjOyJOc3ljuY_t0WcqrsI5RKyX6pgodklbFDJAIhg3VBygWopUJrhlURHQUmqOFGNzFPE8rMcsFARirQc4-e2C915l9f0kpt8SQQ23U_Lyk_90UrY9nIb2rigSZwSj6xiWwrdIRSnFwdPeasvRBiDhaU9_Fq2X1UiH3ltSU66dg5NkY561APIrvVajVpSuWW3FwjQMZXbLOgGHbAAlTcoJ4RuIHTFuxo7FvHbJQjAQnkmC2onb_jjQjscNlAHQrgdQOGZhLMtBjY6QIfQddCvV3mkJ1lNWhaUIbcFOipYKY5ZXQcGqo2jFH9VSRg6Ep2qaTuVelIMrQPJY20MyfvSOguAUY7kLQ-DMkkUgIsYyjxJrJPo9PiPwPnsTv3lCsNmthwc3_sg0v3A6kGlCqkASHZM2Ts4hoUFvHt1W1i_PWzIIbKorSTkUKlIJTpyGq5_COiaD-FUJDAuJM84YiobDXbGCIyK65xJAMaGJTKSZZHEYgywOMMB9koHzuvvx1I2772TMCKBa0BQlj-LrgXe4VzhCfCosBcR42EqdEFZBlRezZ67Lcg-g2_ypC5ba6IxaVgKt4eq3O8FsKnGKX3IZJawpKiixBoPZyyBbTV8yWQBm1uKgxTcwFyRWEXOxmEDVgteMC_gmdC0Mv90OwkByOyowFTnrkkIUYgJ9q-uBjYHY1QPY-ZkOUaDQXScPEe3W-ubnlZEkI7CBAGeAAWvVqqcRuszpVH30xj7tQ742qoFnpZUzzE98Ms1_LQew2hOEZ63qu9WoJYor4ie030LGJACqJqdVKsi6pDxKiDwPWjJFjAMKg6ryihdTmCuXiMMnQovl4lkmS8F2NAxpWFHNpj6swumLuw5w6p0FOOJT9rdbEUaX4lqhzEcLKDZdSXTgTLQe5stBjR19U67QxOmomU6gGZEnQ7ZKjgAeT9jXE1J1_5-dpNRqkrGReiHGfiffPSO7KiIUcO9bPaDqVApwtJnSRhFYxWdMw7CweUvm-9gihg4uviF9IPCximckQ9OYubcGQ66U0_lzGxMWv-zDx6upUXLPGK8de9Bg6k46UxO1j6M1l6iJlnaII2RrR44occon37GP6tSCIXYnYKI449Qux7dKhL2MX3IrAe4X8fnFlSQ5wHOCDAPMqkuJDRVFpRU0kxcgTvFqr3dKDcWaeiUdrgqgHyRjzEK9sdc1TsSJjBJm4UuyN6Pv5SPY0xuQs7zSCZpkUYlS0cfYJy74fDcq6dnGK6WMmdxwnklLfs5AzUs-50_FkMDPeO7L1U9nqpQVrn5pU6xL1FFm7I1Zn88Zh0o4FLjAWijoHa3X-VnQ5NHKp-wvvognacBKXXl6zJTAtBaS-1hcizuQ57T2TcCxlNgV03AoGpBtS-T9ybovwOHBNEK62rKqKg6W7UdbMkaxEH1jw5GSt1lj4WUE1wE7IItKkUZjmUnzkQSl4teNVrEJHiymPFQAEvmVt0600YsC10wNoQqmlShlKHU4z5FqKhD3ayiBb1q0qY1nkuqmFCdrhumG1QSQgXGSXNQToLyC2i1d0qiMYhuTKWFMapmbd9z7sG9phJeONU1A5dh4pxYHPsZK_28GOvZnKkompCXjDcZCx17OumF1RYLe-gThjUXsYirKEqC0DKSMxbFqaQ4MWHDdMiAMeWliKM4s5jVGYByxKSemmdi6_VYzliRCVHahZ0RJ8bTu2BiiVZtqvOZobN9MObDmDK33M-aqic1f0-is4d9ElZzddS7fX86HxWLAM1EwdKxjcoZpuJK_Ysnoxg-yHw_9mHhkI3hnHFYipX48yefqIYCrBShrx1BVxrj2XD-NYqyea42JUJF6QE2wRHbOQQqXk8ijCW9Y7m8PVOy-mNBJS2NMSpYnqoK0eQusDdWFwsu1FOxNUVphn1Weso8rqJgW6AGwWDVcdvo6j8d4l1SiFcHRp9XIXFapglo47IcUzHOqBjn0F8z9cVIFYsAQ-d5KkIrVc4gGDMK9IKZLlUrVNrPlHIfBHjdPIvlprEBjPT16imYW-i4FL6hU0RjgRnr3eAzampjIdwTsslyOMuya1m135NjsmWTBctVDj5IVpTStg05s2pG_Xl6AI0JtEgZJlkl0jy3kujMpDlWK3560IzZbZnmQVSxrKxs6tGZPWOl_JKBMqGbfdUFQjdjGIuuibClhxC_bm8ErdEjBve4WK-nvGRQdUEhq5Iltk_BGVNjiXPR7Bll-ykuZR3rDz5Wk2AcREcMVbmWUTXoZ1Noaxi1_EiGF-S2WRmXsV-B18j5mCKyg26eVJe9fnqN02S5GEMfNvSm4YLK-VOsVActyMu38U0q1NgNLVZZcIoiqfyD6iJG8RRWqqZS-UmFxePgaOe-E-0wM3RGsXnFPByDQIK4SjironxMsjgjciyPnz_uRpPWdf5s-spO57BhTGW-VKxD-brkWnwI3oFO3bK6M1XaWKmxwWoVRVfl-OCDdaaBikqagdb7n0Jsx7aWhUmpdKhDe9CvNsOhVsHT1eVNNnhj4zUq4g8G3NppG7DXyRIdisbNKn2gxfpaIXHKyaNZXZeYrMN4EOWVRiKKrxSf0Jv0gGRwkANWtrV2NgW-tVrxB5MUVHSvRLm7u6PNkaVFDW8jagbkqgiiau3pN-Dj0WgdXa5i47iaL_Eh3xPgx9jL6CZQdx9mpRnWDdW2WRDBTbVEOaeYGwEBWKkFiiGVVOpHfNUVS8ZpoMf8M0ANkI9GI0SdhlQnDKSggj03vGajbpSyxhg0LIahUVrt_Y5yRGP7iyIfxh8p8kNvu18TZYM2Vi-ZZmoqUdK0IJoexkcpK2ZjUypgCGx0pzPprSkDo2i8ph0e8l1n-kR1BmC08fS4P7akRkCrwBNL4_QAIWy3G1jvliAALOjIJ6oy0f9eW3l8mQ1eylxvcN-AfwWJoTPZUQb7SL7QpgonrE7Goxx7hTiLx4jKONjKbaO_aCKVQXxFmeRVAT54YjWYM6Rqv87prOlSplLSZk_Qfdfss2sU7jb1LMQFFAV_kbdvG9BMeM5th7RgkDJguhXaZObVUWIu-uRcAwkWP45CX_jMJlucsVjH--leNc8KLb3rwY3hSsbBtdmtKU7mFMe4UQ5dgWT9dH0qprj0iQf4__7X_zZ5QqXy9kIaTtwNLhwrXxpebw9aJuCJ1AyJclJNOZJJLgFcBHEq45Gh7ZiukaFPz94y6a9UZrLyc1YKKyLOOC77L4udP2Nrql4gFyWwRB7yILK1Tc7grbEL6_xpWq7dBxW9YVrBgSAtTQuN0d2q-QpvV1beqUtdIhREG7UFhjJHrBqxiAauKSDLRm6uqoJRWfjuUTVeUYGzTbOQrlfNYGTM1EgsGo-j-quo_8nJ4ysYSYWEvRZP1VOFTT6NpYTxKhSCdKFFP6KOPTQhRGVq240qwFOihEROy2tLQp28uh7BuPW9znkg4tkoT3LaIWAizZKYV3Gcx3tDIdR0M5eTTw8sM-q-DLKCFbFf-NZLcmaYjSXRbzKWzLh9aZYnYGZikY5VoeOkMgtbzx8-JjpAMbWK5BvQT96YxnWGV7c79MUYmfBjrMsQhIyVHhaIOAVYvU4q6H-uHN077XrQfRpxOmET0y_nuB9j0sMkVMfCBdR5dgfWlzHuyUBmxJQNyIMEGE0lmLD1LMplIPIwiq1D78xmO3b4rxy3RhruoaduJUxS0tuaiRGcQlQHMZK2e5oCUqUlIJBChZaOV7iaoryp3CrwXZpHvAxEaQMOztw3t_vnhVPczJSgoozTgidhEtiyFGewm2Xp88e0qX_B_uHh4VrNt7pm9bty3d69q8dlluqnfkm1EUsCPkvrnf124X0HDn268HDiFsFTdzv4yqqA8PnN4Ml_apYfW6xQ_DBOkJjc4NHNLOsGy416sXQGUcAO_8cOuDsIn9nj8SkdpoJQa9uzNkMrLPUKmlLhc6QaJ4xRvA2NZds9js8FpLTaldfAvHoYGTzduee3UyFQEZY8kFHlRxZcOGP4nOkUL5yqZ8JhMgRTEeI4LJv8cAbtPalpev3cPFXbil14TpXOgj7b4WDPOi9j2RHFqDcttdlK9GhKGgai0_I0ksP0cFGhBdnUvZ6dL6iTaZYNolLE7HrEDQV2Hkz8FG9c6OJ1k1x3u2j2Omxcv4OK3u2wKhulJ4wETgNly-5xLtJ-9vZpkkTHGhjF3KnK_ZnEzV77rAou02QK20ds6xbc8WKkSrV-UQ0zmBPFugfGVyqC90RVfv4VeUbPO_zlSg3KwE9YsSmq2_Lx6uanqw8Air5e4VBCXUl4-L2KhRz7nkZ12R--r8GL6CrvR_zn1D7_uvivHucHaIKmOuGQR7C1NY4nFM193bUN-lO3iDZ6NflRpb-QNHoKJZVK4qBHtkF67hoc4YJf6GyPmuoI76gdJxoaOE6ptZP19v4VEDWlTz8BsCg1nB2ZUEmC8eyST-_X0yi_A-VnRXqpbDh5r06yj6oH6o7KwTDFhXBL4z47yc8ULLa6vhhkvb6ncN72Wu3PvNQvVw-rR_3kgwdr5XPskJ9sSveejxs4GDAG613jpMgXT-7MqyTOWCKDNOFFnmR5AOA0TBNLK3ckpzuO0h3T-ct_yNm-fMaonbFpV7sJfj0-RPPURNE3GRsax1meRVnEwFuufB4kUQywX_hhxPPQB_TJ4qyKUp_5VZKKME7KKA4iBj9HMk2pC-2ZV3IGhxZLP_zRz2_i6CbwjwwOrUIW8RRg2Tw49D9lcGgORy3jIPWTKHp-cOgPoyyrQYwU_j85RfRBdK7U61xE3evgF1OR3Hpvjqibfzs2U1RNRzuiyjTa-WlERUsTx75DD6U5qnc-_-b6-p379RLRzTusfHiktwHWef_H774Bnvnt72lmAj1E6Uz0aLeff4OM9emv39x-9_4veBnBKpUE1qU7FN3cDrr3FKlFYYseHGU-PexzHpM6j0mdx6TOY1LnManzmNR5TOo8JnUekzqPSZ3HpM5jUucxqfOY1HlM6jwmdR6TOo9JncekzmNS5zGp85jUeUzqPCZ1HpM6j0mdx6TOY1LnManzmNR5TOo8JnUekzqPSZ3HpM5jUucxqfOY1HlM6jwmdR6TOo9JncekzmNS5zGp85jUeUzqPCZ1HpM6j0mdx6TOY1LnManzmNR5TOo8JnUekzqPSZ3HpM5jUucxqfOY1HlM6jwmdR6TOo9JncekzmNS5zGp85jUeUzqPCZ1HpM6j0mdx6TOY1L_fxuT-vnXfwd1CUyv)
