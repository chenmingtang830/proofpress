[//]: # (ob:cb2efec0)
# Proofpress Long-Horizon Contract Negotiation Evaluation

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFiODVlYjE1OTU4NzJmYTMwYTYxNTI2YSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjNlYWNlODBjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9kZDg2YzI5N2VkM2JhMjdjNGI2NDk5YWIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q3ZDAzNjUzN2RhZmMxZThiODYzMTI2ZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrFfetuLDly5qsk5B-eGVfp5P2iwf44c9yL07s9F0y3xz_GDZlkkqqcU5VZkxfpqBsN-CEM-IH2TfZJHBG8JKskZUlVWixs9KilTJJJxuWLLyLYP1-xfmwUE-NtU1_dXO33txEvM8mjrMrKIlYsCVkeZXHOrlZXvKsfb-vmTg4jPDtsWJzlN0ksmWJVKBTjosxFkqoyipKklDyXZVanSoYhr4pCFFXMy1SFucpZWkieZvB8BePWzSC6e9k_Xt38jP8y3o7sDmbYshGnWsEPXG7hF3-RfaMaxrcy6OV9MzRdG2zg-a5_DPhj8Ke-69S-l8MA7-yZ-MLuJH7Uwa_77m8SPnfqccDNOO6Hmw8f7ppxM_Fr0e0-iI1sd017N7L2rkzCDwdv9_LvUwM_306D7G9F1w6yhb0Y-0n-srraSIabmEgmZBmKK_2bW3lPD8Hmytu6hi2Kq0LWCWdxIVKep1XFOK6s60f8tNtt00pYuT2R7W1d1GGSZ0lRMyUiWfIyT6I4l_pzzOpuBdsP0xY-OMZ1iq6vh6ubv_58Zab_-QpOuesH_En_Wda3HLb8r1d_3Mv247fBp66WX69-hA-xQoGnPE51I4cPG9bfy8c1nMQaPnvs4a_rVt51Y8NGOIb1tmvv1puub37q2g9__ub7bz7--dPn2z999_EP17v6avUmOWPj2Dd8wnFvORuaAdcht-qWDbDto6TxphFmw4_50rQ45PA4jHIHf2nZDk_94KNW8P6A4nJ1007bLXyi2MD5Sr1DfNuJL_CK4LFUUoTwOH6j_IobMAtV8B1-42f9jTCw3oXgD3oX4CWzElbXtMQ9yqh8gN_8Q_DaUfCbg2_u2XaiH2GU8XGPn4OSBFJ59ctqXi8vVMmzjB2s9_uRjdOwuJp_CNxDC6OrTLIojMUbR4cv3XeDrEFDB8l6sQn2W9ZeB3_oAi5bsdmx_kvQT-0QbNi9hN_JNgC922_lKOcF7VnPDlZTJFmec3m4mj_bKTqOSt3cyxPf_ewLC3uQlXmahllywazmMGXwsJHjRva-KDQ70N97OQTwB9ivLZi2ZtuMjwFr60AqtbAfVaWSjMn4gpX9sJHekTSwHBinhaeCsQt2kg1TLwP4xXrs1vA_AaxVaS1i24WVqazkqqiLg5X96-YxsHYj8OzGifNaeG3h1CIwrmlW5xev4NMzz-NGMTgstoW9GWW_75sBDrfrv6ht9xA8gCfBndov7VAJTjJW9cXrW5PgdHvZMzzswBrZwFg3WOZeguzV20d4su-mu01Q90yN8Anz-rbgQQ_Wl4Z1zJM4vXh9n8lp_CPYPHkH-_XxDnYs-J0TuV999_F3v8bNum9qibu6x8EbAY-S239p_5IoiatQ8oP1fdqyZhfwbmprBkhiWa6ePLwgTUzKSHEVnzmbr-5D0HZjIL_uQTm1mhkLEGxpg7603cNW1ndyFYgt8w30kz0QdVqWRZmduSrU_b211Kj3PaIEI94t6_vuQfY3AW_QEDG0KE7IxMKqailhVVl6waqkc37BbhpGlPBeqg5MESJDOJypGTY3C2sIwVOItBBnriG6DlQDFi4Y2fAl-PvE0CD_9t_a-DoAp8WU3jd2p5fYKRBVBni06-HPS0pVxmVdJLU6WNasC1PbjCeE9snDC0JbRllUVgk7c7Y_tr5rkPtmABilLd_w2MKRgJYGgNAOfAIYGTSLS0JbgSZJVZ65Kjga_TOZvQaebuCc2F0v5Q4tCxxK02qRIUjB2kcEH4-8674snExRShmn8txVfYPqAUJwJ7XAEqxhQQ14podAAoVWoHMHhwqyA1GJHFfWBizsFS8AHldHRtjCRow8IOgQr3ChL7yyIDuhSlkZF_lFM9vntxJCqQ2KTi1Br8Da8Ec6oHbacUBDoEAURv19QvsDxwmuZUm5a1ZnaX3ZrqyD3_zmc3rzm98Eqpt6fXbDKuhA6E2Y4CzFCix2wHsGwgCQqL-TS3LEFfgKftm-kWFutuAmhk03besAIs3gc0qI8HN5TdEDbJuJtAb7FAeRqxf2TfJS1iyUB2v7BoSwb1B1YN_h13WDqzsVO7z81pI9InKgPgytPkU3YDfhWdjowIa_BKUG0JMTWB6c-MnXl6KbNJZZnYr3WtAPhOCFbO5hJrBEaI_u5Dg4Y4TxzTz4DmJcOEY99BLUCXnOmTzat_jGiyLWJKtv2LZTby_FQ0rlPObZOy1ncdMGiOODYeKgni0BD9VsUU1VI7f1sFrYtJxlsiwUe6dVeghuxx7RdHfDHM4xtB8jOcd7oqdkvdKYYAUuamGVcR4DUFFHEhjeEMpu2qmbhrX5QzDtQee0UTp5vK8ZYQnuJoWoYxm947I-AnRjd21HntBZDDj5Ef31oYbMs2hbvEQJKBXGIVPvuFINi5sdqii8qpoeFLWjfwE4AZGeBsifYjzrAdb4KbpeOuI0SqoyjY8oFBIlDKS-nOZpDp9dODeJxGDK8vPmwg9X3RYiWNRE_byGM-hZANw9_gSue5D4iaPcaoaC_t52S-ZLpAkTvD7C4pIBMABHZt3YSZl-7o0lYizNQlXy4oJp_9jCRzpz7cf_xKcOtAEWLXTakoOEUeC9GLbFIpF1deiH77stWUB_GrIqpzZm8c2FDUrSuooiWbzDMr5j6Mg0hgIMUmMoC_q9Q5toaIgbMJItoHYB6oeMCetHdK-Lyl3nEc_So6j7W_jhrkeCTLFpO57anaePL6Heqqzy_Ahvv2HCj5odAR1CRQG3JUcMrPuungSRGzpO7GWN_P4q2DVfMfQehkkOiwCgTMIkOhQYTaSgBG5Y36KGk5_sT0pMsPzmwvYUMlKSR8V7rOMHL3pr0O4TmNTiZuDs1MA_4d_RN-wnvgXHocmkxcA_klF-5PYvWKJ70K7KMFVL5ANPZVhm_F22aU1OBpMr-6bFyOm7j7_TrAQqVw-7p61QP_G-EcNv_61dg5gpkqvdQpxSRypNkiJ7jzWCa596h5KJAe1BySE8IKzE5awDYBnIVCiwljtQpiXtV3lSZkVyqIw_4KcPEEhTEEVrFWzb8P41TPLJlxdkPy3qMOZ19k6r0YKMp_mPsMsjnB1s_Ha73jPcdQG-CWywpeNHS63UjVLNEveW1aKMRfxeq_zevSTAAKK4Lcl9KXheRLV4p8nXACtaAG94FIYbtfKlxXwMkE9BqqeX0unDllDbgujzIlUiY--1R5_mx3RKixFN6bCuB5IISO27Dr0D5QgWQUKVV1l1SEj9cRoBhEqbmDmFHJ95fEnCUxYnUXKc-dRAuNNDDafc7TPPL4WSrKhEkSZnT4kszv8kptYpD1orpHVsbCaxqCAwSfvaCjIc1hKLE6YiCY-Yku-J3iNjK3Wpwqt3ZfnVpSyWYJjGKt9jIWvQix7eAEMjhNyPK4fxAIn0EpOFK510HED00eXVzYAIDUR7Ya9iHhaqkEcJaKakSWEKUIPXb9TL7y3BtjTOseDi4iWsLb1voket1UyNFOMjf3vPwEPqYF8DWzJFCtzwEivIk4plIiovXuAfumCAr9_qYBnPxgGTDaASgko6RaLtGJfjAybXETEsGBtWVWmVHUXRnx_3HYw3nDQzBw8uRadZXSUQcjyr7RszSPNqE3PwxpJ0yFiKOMkumPbjYMNFy2XjqS0x2FpEADotsj9CsSzkhznM7yWyI_7aXqE2z7-ztCksj6ssjy6aeo0kyEOz3WJEA-hutkcI_lYu8xzUnZgoO9PrpawWU8-1YmEhjqKw30PgDm-qaRtg9Q5Wlrwi-nvxraW4WCUFk0JcOP23CnfHVXd0yCXUErCC1OGEzRiiUZ72uEuCwX5TRm0puOBZUUl56Jr-RMkCQEB98_WEsh49urAPlaiqsEzTs2Y6yC3rXAYOglzfYt424jyJsuqsOddB7kAbbqctVNA8u46NYpc1uZkzKvSXBYHMIPYueKLO3AmA8Y_EVwf_ngf_579gDfYfSfA_giL-d0c3In68Dj4Gww7gjOwxRbhIj9RMQbB5_gHRs0dFP_ewgzUZL4TE1s2AM1m5uGQxY5nGKj4qu_kLDokEikFhaApOOZWX3lkQ2DoLy5qL6rK516AimnOYY7S50tSirr4OMLMMM9sqAdypBRmKIsbLJFJHtVpbghjDptnj3oMcdAfFYRK5hlacrGh73TAn6J2IA_4Pj_Jz77FEw6gfvgfoqe4Ulk5MNTgMOaDOzgkVmxJakv8kVAVX6f-j9brCGKGlBhXFq4RDSUAiucHiWIhAbk4SGlGUMxWlh-7-n8ElgMtE-uSUShw9unCScRymTB5F4q-d6Xe60gb-scP6tq9STFr9R70tGCg4NgxpuWGDfkxBEP7TEtipyiKvCnXWmqJrEIkjJmzaDyPgiZ2lw9pGgRDpKh1cqq1YEQtaSXWKSRUeLUpoZb_D2vOTh3L08JKBKpMyjpk6czYQYiHhw1Xf7Xx2AsUcP7iI1-BAjFUnvNGoJWcriyzi5VGU-_rleAwMlVAABqaUbfMVFtfW2okY36sLYqaBWELwNkvoj8tCxSJ-j03SWwHbw4It6-808bgjeI5Gx-yRFmx4dMnW1Ipn0VHp8Tdf4duQfOilkj0a2NN1E8-9sVQzAQ4-L-r6knnX1pN9_HYV_PVbw8WiI1-uzfzxV5ulg0qqAnb66KA-TX2Pg8BvxHYaTnOyz76wxFLlaaJknVwwq-fXxQvFvdrU4e4iZ6SaHoScuPBjEflxZXsrrox5ugV3wXR_Av3FNjss9n203Uhj2nIT0_4RiI0UX_ad1hiYkWbCAMT-GzYv_Ih9I9tGPHoj-L0k3iDUpXJmm8nQqfFWNVh6BE7VdLMMPLqJQS9YwcIqKkUdJUmVhwUMkBaClayqeKEqGcVxxCIhs7yKJTyZ5IUM8xLgBqWTMFymrhR9Wjdl_gtsNPZ8xGGcr8NyHcc_hPFNGt8k2T-F4U2IJtvsuN9u84v325__f_ewkMzq9pINGzZEtLAqkSAGkswujeF1nBhxfudWETO3zMMoliWLK4LINLfXPWLnXm4MMWNFeSIylsZhWJZ2LK9XZG6bObsNpF4ZjgWrBmf6ACUXK6ipeNJVoOlo_LkqDLPehJdllUBcHxehXa_XTTJ_-2ubQ8y4vKiLKJOSCxXZcb1-EZdUP7_9oxENbNUjelfWmvIos0dUL6VR51rXnj5rzpjou2F4pk7B1DeCViztXFTmuQxVFFex_UKv78SmTy5oI9H4DU6TfDM4sxWlSnbg2cA9u4jAfjzW1IpxTqZjRRgiEazcNDHFdYDrERI3Yxv8fQJYaOy6Hc1CSdoCkLR614xEVFmcYTsK0WtQqQdIBaxG03rgFTrANBpi2EJwzNe1Bonp4nFHr3tcBBuOaMOjOgssoLjru4elI8nzWqoylyKKi1n5XMPNLMxv65wxo2eqTvNKKYhX3eheM431uBd0xUgwoSTwDImKLzLwba4l13029eblvZBVHqlSlJxHTjy91hqz2kt6ZCjgp3oNzSBxwBeUG6cAkHCTrutlDZUEmSYFal6EkzfaZ49hWLlqdPhR7lizxV9RkDpOfTtos0fdGChDO7nrevgNo7kB0UBMXE9YM0FFI8EOG0fskm3MujIZHvxJJ3bwJ7HVf-slbERrDaxN9tR64_U3Yp5ZEqLasodH0JWVVj74X69-p5FmtfOW7MmYgW6QrI_eQFq2deK2xQcJvqBKIddlFRKtk-7qRBNIeobBhNMyqXWM-dleCNBNXkurnesFuH4GvDqxyVRa8IplubJi43U82QzIBa1LuD9gElwBxXXwLUiHKWOx0kB1dmD98BxruSXdaWyFpNYvEkOizDV-XRlppF-REATIZ4A8w8Q6TveOley_6Yggjzmu9fZKVzJijKVB0M8s0HPVEn0WmcNnzBaYNmzi7qXhDmlkMAno861oDpZQhHGpnHJsEO6aEehsvQoq7dpQLWwwjxYc7T2to6dCNdRsMOISzDP-qymqfq46xhUxLLm7uJCJitNMRg7YeK1ms219TfeYGVOV4CxzWdc8duDDayh72mP85h4x6cQkGL40EB1gXS049ntyf9S9tELVwr0iSQOZtjgDBgexw6JWBl9D4AJcr8AkFohALcGfDii8IMoQIKDhBvQFML3RVSkH1dmsHR5kv-S6VBGJKEx5VTm85HWxeWji3MY052itiTcu-YmLB9uFX9RpPXXygrYTW-S1GhmzZJzV3ybQTfVos8P4HmGAZkTS_riIHZ4Fw2ZwjXb7-vT0dsODCxsVMq5ULgBSly5Q8BrrvI06u1fOzCSwyDLjUQr_Z2fy2ufMTBd1xGmD_pP1MfBacj3nCrWHNWkHqjXqiMZLrzUK6O_10VKSHUbo9oNfUMYfTc29Nn8LRr9SsqjKUgpVOT30OvJm3X5Nk50Zs4xkLDn4krhyjsTru7N1Oxe00h35A2PfSB5ZfY94eXAAAIYj0CTkM9ASnLsWU2PE9a7-ng043vdoTXGoj66Tzi4Ta_ga5FWer3o0G5FGUiV5xOKSJ06z51a_WYzO7t7T0rbX505FjsjKGGx2iJoMOMK9c8ImyUAd1h-bl7WwEY4Ae4AoQ9cqO1xD-AyNJRpHkAlBgAkkjwAcvJ5du6xQsJl2GuGAwYa1wEFgaILUlInAtMD_zZSaUWCHyfYexsmvqWZgUNIYa3PaCHkUHNvG2BbQKxPPwUsFTj7su5byJ63ZvIPPPChCJiasmwaslCNMGGCXIgxUXs-1P_irAWtSBqwrAZch7-ijHTqD56vnV0uHCH-Owvm45qjIFT-bQ-rlXYMi-AS3WOg77RZ0ui6rVEVZKVniSA2vl9MG4Be0Z9aUtbdJCr1KZhDFdXBQ-U5j1xBKtFS3jCFjA391HicYOq24B2Ek4lsGMFmM3i5h1GQ2b4nXqJJKyCzN4jLOZ07HNY3OJu31HaB25EyqrA5zJmsXWHlNoUedjed0eDrbRDKkGwh16I_vdl-IDJrQKEB8KJcwG8R_TKUyldnsweYeURcDnt_wSWELvF7i67K524zu_fGhO36_sePOkcy0r6nMjpFkSBeDaSWww0cxKvbnKMdpfIg1QpS86ba1L0wQNcI-AE7eWpOqV0wyqpdthNVmaehTJwAkoPIagBufApNaI2sRz1LslEas5kxFfMZwXturj-HO7GFF3ohyM7ryzk91mYYsA8iOsL8OpTACb2VDPA-A4HsSN4wrIUDcdt0SPJWCR2WahUVROm_udc3O6vSm_ldLrCSxFBHsnsdBei2xbvAzm1rNLEUdhkpWTCZJ7QiRuc_VO51zO1VhBTez7FiEvHIsiUdrGKFa-Q4ZxdP6Rkx7WJMKnp5h7xmcfauhicdYki_ABhyBQQsylhS1crDX5P39AmswwHDqKEIKfDqRitrMEGSir5MjxbravBI8oouj4ANRBlvKERL8woKlBXkp0qKu4oqFIWFlHS3O3br-kZ7RcGsmiRlPlEgBV4nMccxzD-5rTvREG23QzE4BTVrXbc2paDPMJwg1ibv8BADu29bZptULvJqOume_JyBm869mO0Ds-vghPNOnTb5xZRCnDfAtPeGiONwnzT0hJ9beDTbOc0W6tublII5bOMtYhnUkwryKMgdgvSbip1H6m_uA0QMi1GlHCsZRXO33UICNA-pfIsJw1KLJaK4OfCaiTYjT29pwPpsGrGZriQ5P7Gkq_-iHaUe1ZhCX3YOakmmBvXu-idWCgSpJwiKMZUTtOLQ3XuuyL-dndh5bGxkmVZ5FkWCpC3u9ZmTbp3RBL_GcEPFqRGj7MUuANADW-j6ARUFeQdcGdByjUGxewvewBVga9n8u8zUA5hp2gAK7Vn-z0XSXqNdxiuZ3Rq_R2Ngir8d44TgA8EHMmRVFSGlG7YHnRugDFuXiPmabucwrVuZghBhzXt9rbfazhyfblS3zICAgV6zMcuXAq9fB7H3GuV3JfsONIY5N-Txl1ph41O0iC1vNS0DCEM2nlRNIr6HZl_xX9ifbwCUv01yVXFXSQQ2vZdkRB-d3IGPRsQDDSflWypIRPLcVyNQnZUqPDVNLm-u6hSA4xC-yyUYyJSAp-C3aOVirZ7v_nHHWWrGR2_2g4ZlxqdZTLAq3DGNe5SIrqsKjCF3HtLfjb218djam4HmiZB7OO-_1QpsJLmlp1pulMb-XHfG87OqIJZizMhR4G6M9Q3UHzynbQABdH5mrVTk0I_okuRREDjfjfKj20IgT1Tyl7nq7J4kAR40UL7iPB9bXmsNcEzfnuXPNweuaWJ2FpvCVULtc9rGw66qGf6YOAntN3t7Zvqpt23Jwecwx_pNSOB31Ormd0zi_N5uAK_5qoMzFDFY06bM6ruPHTeznE2JB34EUjK0zjNrfT8RfAVhunf3SboVck5HutfMxhyfaDJq96R3DvcXuisd1DVi51Umn2iGytcFJIAgovc2wW3L3kidJFQoez-7e60Gfbf2bO8mtjpdlVORJHfHEnZjXXO5Z_nNbxKm6i1AuIfu1JgvtKmGBWgdABZuWkgtUS4HaDJ8keyIlqeJENzIvbVZYlICFqljmfObPXRe69y1v6SW3-ZIEfHqY8zrMw9lLuPZyR21c0CROiUdWsz1RdwjF6cMhUt6bBxHGYGHpAH_l3VedyEdZW1OQboJDW6Sjp3oA3XVRqzVLOrfs9wIBOqZymxW9YAgLMHmjDkLoBUJXom-wYxF_uwYFWOnIZEXt5K14XJmAwxF1oIT7EQyeTTi7YmBrAwyFbki_QeeRnmQ1aVgwhsIV6GiyUj7ndT0YqBeOWvxVJ2HoSEyqput16kkLtCGS59oY0ve1CxYAozyTtzwmZbIkghAxVmWWuSDR6_GfgfPZnfrrDdJmrhwcv_uI6X5gzahThVQApHqm_R0cw8oB3oO6LazfHncUEDnUxgk51JqpxEDOwPVPET3zKV5iAtNKiUIgpnJssHeNwGy4zrkJwPqwTCWKV1kqZ4LFuxzgoHTgvP5-LGULPnoJI1K4FhRl_ZPsO5AdITSegIgKexGRD9PUBWUZ0Hi1B-G2JP8MscmTumxjieakIZd-DxU_7AVwqcYle8hUkbGsqpPMOQ_vWgLXaviamwVcbimNcggDS73FmjmbLxtwVvCC-wJeoKa1-6fXSQlAZ2cDpjt3bUKIKCZYv34axBycUTPOmZP1zAaD6nh5jn7ampeeVkSQjcIEAZ4AkVcbXU5j7Jm2qIdpjMNaB_xs3QJPQ-p5bA_8egt_2s40mleEF2yauw2YJcorYuR03wEGJALViJNuVUQbMj8FG3wPVrIDDIOGw5kySpcTmGu2CEOX6GWeKVaESoIPnVMa7soGW392wa0LB8GwLh1FPvFJu5urSBMbWU_I4WABzdRzZogysHu7PRKapnqnm9CFabbMEGhW1emQnYEDkPcT8mpauw7XMy2yVLVKqziMC4g_xRwduasiZgv3ursfbIVKFfOQZXGSzFV03nUQHi5_3f0OtohBYIhfqTCqHE_hXfngJWbOvcPBdOrpnJnjpM1_9iHAsYxq2SnmVw8mGm3FSW9zsm4yGnuNlmTtSBqrWwNIwoAsn5njX3QphEbsXkHE81PoVc9hFSn7nD5kLgI8rOPzCyoo8oBgBIQHhdQUEtoqC0oqGSGuIZxi9cFqdBiLe-iVdvgmgGKRzykq9udS1zsSJrBJm5UpyD7kX_jjzMkt6HmZqCyv8oSzfI4B5ns3PJl78-0ZVqqVKlmaCVErJ37ehRpO_M6_FsMAPRu7r3U9nq5Q1rn5tUmxr9FE27I15v74nHcgwqXBAzBOQa_usMrPUZPPVD5hffVROs8AUurKN2WmBKCNlTrA5FjchzJnsm8EjJfArr4Bg6oF9bps3pug_wQBCaIV1jeUUdF1tno52JI1yqPqH0NGKtNlj4WUC1IE4oItKhWP57IT70YSX4redLWITfAUKROxBJEsnbn1bhtxInTBtSFU0aQLpexOPR7uCBV16Jc1WzDoJm0a46WkiqXqTN0wvaCTEJoYJ8tBOQnKL6DXnrRGI4luXaWDMbpm7TByHiC8phJeONUtg5Bh4ZxYmoYF42FZzfVs3q0oZiMvud5kLnQc6KRXzlqs3KEvONZSpjKtkySLYidI3rUoXiXFiRs2bIcMOFPBZZqkhcOs3gUoz7jUU_eZuHo9VjJWFVJyN7B3xYmN9C64scSYNt35zDDYPrrmw7oyv9zPuaonNX9P2NnjPglnuXrq3b4_nY9KZYRuomL53EblXabia_2rb0axclCEYRrCwDGb6Zz5shSn8efffKIbCrBShH7tKbq2GC_S-deoynZe40qkZukBNsERu3sINF9PKowlvXO5vDtT8vpzQSUNjRwVDE9VhehyV9gba4oFV3pWbE3RluFQlJ4Kj28o2B52g2Cw7rhtTfWfoXjXRPEaYvRlE5LmPM_AGnM-p2K8q2K8Q3_LrS9Wq1gCGLoscxk7rfIugrFXgV5wp0vdSZ32s6XcRwSvn2dx0jQ3gJG93jwFcyvDS-EXekU0DpixwSef0VJbD-GfkEuWw1nyvmP1YU-OzZYtFizXJcQgRcWVaxvy7qqZ7efpC2gs0aJUnBW1zMvSaaJ3J81zteKnL5qxq-V5GSU1K3jtUo_e3TNOyy-5UCb2s6-mQOhmprHomQRbegjxm_ZGsBoDYvBAyO12KUoGUxdVquYsc30K3jU1bnMuuntG-37ipVxg_SnEahLkQQxjqMu1rKnBOJuorXG28vM2vCK3zXjK07CGqFGIOUXkLrp5Ul329ttrvCbL1Ux9OOrNwAWd8yeu1JAWFOU7fpMKNaaxwyoLQSySzj_oLmJUT-m0aimVn9VYPA6Bdhl6bIe9Q2dWmzfch2MRSJTWmWB1Us5JFu-KHCfj5193Y7bWD_5c-srdzuFoTO2-NNehY10KLT5FH8Cm7lnT2yptrNTYYbWK3lcd-ODEJtNARSXtSOP9byn3c1vLyqZUerShA9hXl-HQo-DpmvImR944vkYz_uDAnZ92hL1JlhgqGher7YFR62uNxCknj251yzFZh3wQ5ZXmTZRfiZ8wiwxgy-AgR6xs69zdFPjVesTvbVJQ73st-XR3R4sjT4sW3jFqFuRqBlG39gw7iPHoah1TruJ4XCOXOMmfCfAj9zKHCdTdh1lphnVDjWsWRHBTr1HPiXMjIAAjdbBjuEs69SO_moolGzTQNP8CUAP0ozUI0aQh9QnDVlDBnk-vOdaNUtbIQcNgSI3SaB8nyhHN7S96-5B_JOaHvvawJsqRNs4u2WZqKlEye0F7esyPUlbMcVOaMAQxujOZ9M6WgREbb_YOD_mut32iJgMw-3ia7p87MiNgVWBGboMe2AjX7QbeuyMIAAN6-ommTA6_NV4eP2aHjzI_Gjx04F9BY-hMJspgP5MvdKnCBa9TiKTEXiHB0plRmS-28tvoL7qRyiK-imdlXUEMnjkL5l1SdVjndNbtUrZS0mVPMHw34jO1GnfbehaSAmLBXxXtuwY0S8_57ZAODFIGzLRC28y8PkrMRZ-810CBx0-TOJQhc8kW71qs5_vp3nSfFXp6P4Kb6UomILSZtsSTecUxPsthKpBcnG5OxRaXPokA_-9__KfNE2qTd0BpeLwbPDhXvrSi2R-1TMCM1AyJelIvBZJZqQBcRGmu0lmg3TVds0CfvnvLpr9yVag6LBmXTkW867jcf1ns_Du2luoFSslBJMpYRImrbfIu3pq7sM6_Tcv3-2Cid8wYOFCktW2hsbZbN1_h69rLe3Wpa4SC6KP2IFD2iHUjFu2B7wrIs1GYq6tgdBa-f9SNV1Tg7NIsZOt1Mxg5M30lFl2Po_urqP_Jy-NrGEmFhINRT91ThU0-rdsJG1VoBOlDi2FGHQdoQsra1rZbU4CnRAmJkoY3noQ6eU09gg3rB5PzQMSz05HkckDAZF5kqajTtEwPLoXQt5v5knz6wjJr7nlUVKxKwyp0UZJ3h9lcEv0u15LZsC8vygzcTCrzuSp0vqnMwdbzLx-TPaCYRjP5FvRTNGZwnZXV_YSxGCMX_pzoMgQhc6WHAyJeAdZgkgrmP1eO4Z0JPeg9gzg92sT2y3nhx5z0sAnVuXABbZ5bgYtlbHgykhuxZQPqKAFGtxIs-HqWlCqSZZykLqD37mZ77vDfeN0aWbiHgbqVMElJX2tvjBBEUR1xJF3_NAWkS0tAIaWmlp6vcLVFeUu5VZC7vEwEjyR3hIN375vf_fPKW9zsLUEVT_NKZHEWubIU72I3J9LnX9Om_wv2Dw8P1_p-q2vWfODb7u5DMw-z1n8a1lQbsSbgs3bR2a9Xwe8hoM9XAd64RfDUXw5-si4gfHkxePLftuvPHVYofppvkFhc4LOLWTctlhsNcu1dRAEr_F8TSHcUv7DG52_psBWExtqetRgaYW1GMDsVv7RV8w1jxLehs-z6x3leQEqbiV-D8JrLyGB2751fL1GgMuYiUkkdJg5ceNfwebdTvPJWPUuHqRhcRYzXYbnkh3fR3pOaprffm6drW7ELz6vSWdHP7nKwF4OXueyIOOpdR222CiMaTpeBmLQ8Xclhe7io0IJ86kHPzhe0yXSXDaJSxOzmihsidh4sf4ovrkzxuk2u-100Bx02ftxBRe_usirH0hNGgqCBsmX3eC_SYfb2aZLEcA2MOHeqcn8hcXPQPqvJZbqZwvURu7oF_3oxMqXGvuiGGcyJYt0DExvN4D0xlT_-Av__3zVaBxQ)
