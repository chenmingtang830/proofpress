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

[//]: # (ob:10278dcf)
See the companion [H4 flow illustration](LONG_HORIZON_EVAL_FLOW.md) for a compact view of the cold boundary, the C1/C2 information-parity conditions, and the episode-level outcomes.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzFiODVlYjE1OTU4NzJmYTMwYTYxNTI2YSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImYyMWNlOWFhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9hN2IwMGJjZTc1ZTg1YmRlZDVhMTY3MTgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Q3ZDAzNjUzN2RhZmMxZThiODYzMTI2ZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfety40aW5qsgND-mu5eUcb-oY39U13i2vOu2HbanJ2I9Dk0mMlNEF0mwAVAq2eGIeYiJ2AfaN9kn2XNOXpCkKFCiamfnB6I7yhIJJBInz_3y6dcr1g2NYvVw24irm6vd7jbiZSZ5lFVZWcSKJSHLoyzO2dXiirfi8VY0d7If4Np-xeIsv6mrokyqsCqTuC5lXhRxWsk4rESeF0nGVZ4xmSRpUUYJDwXjrKwUC-MwVyqJuZSwrmj6ur2X3ePVza_4y3A7sDt4wpoN-KgF_MDlGj74i-wa1TC-lkEn75u-abfBCq5vu8eAPwbfdW2rdp3se7hnx-qP7E7iSx183LV_lfC6-w4XXA3Drr_54ou7Zljt-XXdbr6oV3K7abZ3A9velUn4xcHdnfzbvoGfb_e97G7rdtvLLdBi6Pbyt8XVSjIkooqjWlYMKYaf3Mp7ugiIK29ZwcOQ17LIZJlxIUXGoryIStxZ2w34arfrZith5_ZE1reiEGGSZ0khmKojWfIyT6I4l_p1zO5ua7br92t44Rj3Wbed6K9ufvr1yjz-1ys45bbr8Sf9tRS3HEj-09W3O7l991XwvhXy09XP8CKWKfCUh71oZP_FinX38nEJJ7GE1x46-Ha5lXft0LABjmG5brd3y1XbNb-02y--__KHL999__7D7Xdfv_vmeiOuFq_iMzYMXcP3uO4tZ33T4z7kWt2yHsg-SFpvP8DT8GU-Nltcsn_sB7mBb7Zsg6d-8FILuL9Hdrm62e7Xa3jFegXnKzWF-LqtP8ItNY-lknUIl-M7yk9IgJGpgq_xHT_od4SFNRWCbzQV4CazEyYEbXGHPCof4JO_C166Cr5z8OU9W-_pR1hleNzh6yAnAVde_bYY98sLVfIsYwf7_WFgw76f3M3fBe6iidVVJlkUxvUrV4c33bW9FCChvWRdvQp2a7a9Dr5pAy639WrDuo9Bt9_2wYrdS_hMbgOQu91aDnLc0I517GA3oEvynMvD3XxvH9FyFOrmXp5575M3TNAgK_M0DbPkDU81hymDh5UcVrLzWaHZgPzeyz6AL4Bea1BtzboZHgO2FYFUaoIeVaUS0KzxG3b240p6R9LAdmCdLVwVDG2wkazfdzKAD5ZDu4T_BLBXpaWIrSd2prKSq0IUBzv759VjYPVG4OmNM-c1cdvEqUUi4Wkm8jfv4P2J65FQDA6LrYE2g-x2XdPD4bbdR7VuH4IHsCRIqd0UhcokVbESb97fkhin3cmO4WEHVskGRrvBNncSeE-sH-HKrt3frQLRMTXAK4z7W4MFPdhfGoqYJ3H65v19IKPx96Dz5B3Q690dUCz4k2O533397k-_R2LdN0IiVXe4eFPDpWT2n6NfEiVxFUp-sL_3a9ZsAt7ut4KBJzHNV08unuAmJmWkuIovfJov7n2wbYdAftqBcGoxMxogWBOBPm7bh7UUd3IR1GvmK-gnNKhFWpZFmV24K5T9ndXUKPcdegmGvbes69oH2d0EvEFFxFCjOCarJ3YlpIRdZekbdiWd8Qs2-35ADu-kakEVoWcIh7Nv-tXNxB5CsBR1WtQX7iG6DlQDGi4YWP8x-NueoUL-479s4-sAjBZTmm7sTm-xVcCqDPzRtoOvp4SqjEtRJEIdbGuUhf22Gc4w7ZOLJ5i2jLKorBJ24dO-3fqmQe6aHtworfn6xy0cCUhpAB7agU0AJYNqcYppK5AkqcoLdwVHo38mtdfA1Q2cE7vrpNygZoFDabaaZcilYNtHdD4eedt-nDiZopQyTuWlu_oSxQOY4E5qhiW3hgUC_JkOAglk2hqNOxhU4B2ISuSwsDpgglYcQgReHSlh6zZi5AFBR_0CE_rMLRO8E6qUlXGRv-nJ9vq1hFBqhawjJMgVaBv-SAe03W84eEMgQBRG_W2P-geOE0zLlHALJrJUvI0qy-APf_iQ3vzhD4Fq950-u34RtMD0JkxwmmIBGjvgHQNmAJeou5NTfMQV2Ar-NrqRYm7WYCb6VbtfiwAizeBDSh7hh_Kaogcgm4m0ensVB5YTE3STvJSChfJgb18CE3YNig7QHT4WDe7uXOzw_F1T-ojxuszFYWj1ProBvQnXAqEDG_6SK9WDnJzx5cGIn719KrpJY5mJtP5cG_qRPPhaNvfwJNBEqI_u5NA7ZYTxzbj4BmJcOEa99JSrE_KcM3lEt_jGiyKWxKuvINu5u6fiIaVyHvPsM21nkmg9xPFBv-cgnltyPFSzRjFVjVyLfjFBtJxlsiwU-0y79Dy4DXtE1d32YzjHUH8MZBzvKT0lxUL7BAswURO7jPMYHBV1xIHhDXnZzXbf7vul-SLY70DmtFI6e7wvWWHK3U2KWsQy-ozbegeuG7vbtmQJncaAkx_QXh9KyPgUrYunUgJKhXHI1GfcqXaLmw2KKNyqmg4EtaVfwJ2ASE87yO9jPOse9vg-up464jRKqjKNj1IoxEoYSH08n6c5vHbi3CQmBlOWX_YsfHHVriGCRUnU12t3Bi0LOHePv4Dp7iW-4iDXOkNB32_bKfVVpwmruTjyxSUDxwAMmTVjZ3n61B1TibE0C1XJizc89tstvKRT1378T_nUnghgvYVWa3LgMAq8J8O2uE6kqA7t8H27Jg3oP4a0yjnCTN45QaAkFVUUyeIzbONrhoZM-1DggwgMZUG-N6gTTRriBpTkFrz2GsQPMyasG9C8Tgq3yCOepUdR91fww12HCTLF9uvhHHWeXj7l9VZlledH_vYrHvhOZ0dAhlBQwGzJAQPrrhX7mpIbOk7spMD8_iLYNJ8w9O77vewnHYAyCZPokGF0IgU5cMW6LUo42cnuLMcE03dOkKeQkZI8Kj7HPn70orcG9T45k5rdjDu7b-Bf-B1tw27P12A4dDJpMvCPZJQfmf03bNFdaHdlMlVTyQeeyrDM-Gch05KMDBZXds0WI6ev3_1JZyVQuDqgntZC3Z53Td3_8V-2S2AzRXy1mYhTRKTSJCmyz7FHMO37znnJlAHtQMghPCBfictRBkAzkKpQoC03IExT0q_ypMyK5FAYf8RX7yGQpiCK9lqzdcO7l2SSz948wftpIcKYi-wz7UYzMp7m3wOVBzg7IPx6vdwxpHoNtgl0sE3HDza1IhqlmqncWybqMq7jz7XLH9xNNShAZLcpvi9rnheRqD_Tw5fgVmzBecOjMLlRy1-azYcA8ymY6umkdPKwJq9tgvV5kao6Y5-LRu_Hy3RJi1Ga0vm6npNEjtSubdE6UI1g0kmo8iqrDhNS3-4HcEKlLcyc8xxPXD7F4SmLkyg5rnxqR7jVS_XnzO2J66dCSVZUdZEmFz8Sszj_SJlaJzyorTCtY2MziU0FgSnaC8vIcFhTWZwwrZPwKFPyA6X3SNlK3arwYqpM3zpVxaoZlrHKz7GRJchFB3eAoqlruRsWzscDT6STWCxc6KJjD6yPJk80PXpowNoTtIp5WKhCHhWgmZKmhFmDGLycUM_fN-W2pXGeSFa_eQtLm9430aOWaqYGivExf3vPwELqYF87tqSKFJjhqawgTyqW1VH55g1-0wY9vP1aB8t4Ns4xWYFXQq6SLpFoPcbl8IDFdfQYJpQNq6q0yo6i6A-PuxbW68-qmYMLp6LTTFQJhBwnpX1lFmlerGIO7pjiDhnLOk6yNzz2XW_DRZvLxlObymBrFgHXaTL7UyuWhfywhvmDxOyIv7cXiM3pe6aIwvK4yvLoTY9eYhLkoVmvMaIB727UR-j8LVzlORBtvafqTKe3spgsPQvFwqI-isL-DIE73Kn26wC7d7Cz5AXR37N3TcXFKimYrOs3Pv4rhdRx3R0t5hKEBF9B6nDCVgxRKe93SKWaAb2pojYVXPCsqKQ8NE3fUbEAPKCu-XRGWI8unaBDVVdVWKbpRU86qC3rWgYugrm-ybptxHkSZdVFz1wGuXPakJy2UUHn2XVsFLuqyc1YUaFvJhgyg9i74Im6kBLgxj9Svjr41zz43_8L9mD_SYL_GhTxv7p0I_qP18G7oN-AOyM7LBFOpkcEUxBsXn5AdO1R0889UFCQ8kKX2JoZMCYLF5dMVizTWMVHbTd_wSUxgWK8MFQF54zKc_dMMKzIwlLwunrbs5cgIjrnMMZoY6ep9bo6EWBlGZ5suwSQUhM8FEWMl0mkjnq11uRi9Ktmh7QHPmgPmsMk5hq29dmOtpctcya9E3Hw_8Oj-tzn2KLJqB_eB96TaBW2TuwFGAzZo8yOBRVbEpri_yRUBVfp_6P9usaYWnMNCorXCYecgInkBptjIQK5OZvQiKKcqSg9NPf_ACYBTCamT86JxNGlEycZx2HK5FEk_tIn_Ul32sA_G-xv-yTrvRb_QZMFAwWXDcO0XL9CO6YgCP9lytmpyiKvCnXRnqJrYImjTNh-1w_gT2xsOmzbKGAi3aWDW7UdK_WEVFKfYlKFR5uqtbDfYe_52UM5unhKQZVJGcdMXfg0YOJawourrt342Qlkc3zhIl6CATFanfyNRk0ZW1lkES-PotyXb8fLwFALBfjAVLJtPsHmtkIbEWN7dUPMvqcsIVibKe-Py0LFdfw5iKRJAeRhwZp1dzrxuCH3HJWOoZFmbLh0StcIxbPoqPX4y0_wbph86KSSHSrY830Tp-6Y6pkAA58XQrzluUtryd59tQh--srkYtGQT_dm_vy71dRBJVUBlD46qPf7rsNF4JN6ve_P52RP3jCVpcrTREmRvOGpnl2vn2nu1aoOqYs5I9V0wOSUCz9mkZ8XdrbiyqinWzAXTM8n0Dd22EHeClHmdVwVsHvO4qJOeZ5WFUN7sG0HWtO2m5jxj6BeyfrjrtUSA0-kJ2EAYn_D4YWfcW5k3dSP3gr-LIm3CE2pXDhm0rdquFUNth6BUTXTLD2PbmKQC1awsIrKWkRJUuVhAQukRc1KVlW8UJWM4jhiUS2zvIolXJnkhQzzEtwNKidhuExTKfq0bsr8NyA0znzEYZwvw3IZxz-G8U0a3yTZfwnDmxBVtqE48qJktSzDGlhl_PTX_98zLMSzerxkxfoVJVpYlUhgA0lql9bwJk4MO3_mURHzbJmHUSxLFlfkItOzvekR--zpwRCzVpQndcbSOAzL0q7lzYqMYzMXj4GIhcmxYNfgmD5AzsUOamqedB1oOho_1YVh9pvwsqwSiOvjIrT79aZJxnd_6XCIWZcXoogyKXmtIruuNy_iiuqXj380dQOkekTryramPcrQiPqltNe51L2nJ9UZq7u270_0KZj-RpCKKcpFZZ7LUEVxFds39OZObPnkDWMk2n-D0yTbDMZsQaWSDVg2MM8uIrAvjz219TAW07EjDD0R7Nw0McV1gPupJRJjHfxtD26h0et2NetKEgmA08SmGShRZf0MO1GIVoNaPYArYDc6rQdWoQWfRrsYthEc63Vb44np5nGXXvdyEaw_Shse9VlgA8Vd1z5MHUmeC6nKXNZRXIzC5wZuRmZ-3eSMWT1TIs0rpSBedat7wzTW4r5hKkaCCiWGZ5io-CgDX-fa5LqfTb15nhayyiNV1iXnkWNPb7TG7PYtMzIU8FO_hs4gcfAvqDZOASD5TbqvlzXUEmSGFGh4EU7eSJ89hn7hutHhR7lhzRo_oiB12HfbXqs9msZAHtrITdvBJ4yeDR4NxMRijz0T1DQSbHBwxG7ZxqwLU-HBn3RhB3-q1_q7TgIhtlbB2mKP0ITX74h1Zkke1Zo9PIKsLLTwwX-9_p1Gmt2OJNmRMgPZIF4fvIU0b-vC7RYvJPcFRQpzXVYgUTvpqU5UgSRnGEw4KZNaxphf7YUA3dS1tNi5WYDrE86rY5tMpQWvWJYryzbexJOtgLxhdAnpAyrBNVBcB18Bd5g2FssN1GcH2g_PUcg1yU5jOyS1fBEbUspc-68Lw430ETFBgPkM4Gd4sI7TvWMl_W8mIshiDktNXulaRoyyNB70iQ16plqizSJ1eEJtgWrDIe5OmtwhrQwqAW2-Zc3eJhRhXWqnHBp0d80KdLZeB5U2bSgWNphHDY76nvbRUaMaSjYocQnqGX81TdWnumNcE8OUuYsLmag4zWTkHBtv1GzUrS-ZHjNrqhKMZS6F4LFzPryBsqczxq-eEZOOTYL-YwPRAfbVgmG_J_NH00sLFC2kFXEa8LT1M2BxYDtsamXwNuRcgOmtsYgFLCAk2NMemRdYGQIEVNzgfYGb3uiulIPubLbtH2Q3ZbpUEdVRmPKqcv6SN8XmeROXDqY5Q2tVvDHJT0w86C58o1bLqeMX1J04Iq_FyKglY6z-ugfZVI-2Ooz3kQ_QDJi0P25ih2tBsRm_Rpt9fXqa3HDhBKFCxpXKa3CpSxcoeIN1HqEunpUzT6qxyTLjUQr_s0_yxufMk940EacV-i_WxsBtyfVYK9QW1pQdqNeopTReeq29gO5eHy0V2WGFdtf7DWX80fTca_U3ofQrJYuqLGWtKieH3kTeKNsvGbIza5aRjCUHWxJXzpB4c3e2b-cNo3RH9sDoN-JHJu7RX-6dAwDLkdNUyxOuJRh3zaZGiWuq_pn1uN4PqE1xqXduks5uE3v4GsyrnO56NIRII6mSPGJxyRMn2eOo38hGF0_vaW7b6XOnJkfMyhjf7NBrMs4R0s4xmyQFddh_bG7WzEZ-BOgD9DJ0r7Lza8g_Q2WJyhF4oiaHCTiPHDi4Pbt2VaFgtd9oDwcUNuwFDgJDE0xNmQhMM_xfTasZBXZYbO9gnfyaegZ6JY2yNqeNLo-CY1sZ3QJyZeI5uKnAh_e7dkv1k60h3sFrHjQhUyas3ffYKUc-YYBTirBQeT32_uBHPfak9NhXAiZD3tFLO-8Mrq9O75YOEb6OwvG4xqjINT-bQ-rkXYMs-MRvsa7vfjMh06KsUhVlpWSJS2p4s5w2AH_DeKagqr0tUuhdMuNRXAcHne-0toBQYkt9yxgyNvCtszhB32rBPQgj0b9l4CbXg0cljJoM8abyGlVS1TJLs7iM8zGn44ZGR5X28glQu3ImVSbCnEnhAitvKPRosvGSCU-nm4iH9AChDv3x3vYjJYP2qBQgPpRTPhvEf0ylMpXZaMHGGVEXA14-8ElhC9xe4u2yuVsN7v7hoT2-v7HrjpHMfieozY4RZ0gXg2khsMtHMQr2hyjHx_gu1gBR8qpdC5-ZIGoEOoCfvLYqVe-YeFRv2zCrrdLQq-7BIQGR1w64sSnwUKtkrcczFTulEROcqYiPPpw39ur7cBfOsGLeiGozuvPOL3WZgSzjkB35_jqUwgh8KxvK84ATfE_shnElBIjrtp1yT2XNozLNwqIonTX3pmZHcXrV_KtNrCSxrCOgnpeD9EZi3eIXDrWapxQiDJWsEG9LuITIOOfqnc6lk6qwg5uRd6yHvHBZEi-tYZhq4RtkZE9rG7HsYVUqWHqGs2dw9lvtmngZS7IFOIBTY9CCGUuKWjnoa7L-foM1KGA4dWQhBTadkopazZDLRG8nB4p1tXol94iAo-AFkQe3VCMk9wsblib4pUgLUcUVC0PylXW0OE7r-kd6wcCteUjMeKLqFPyqOnM55nEG9yUnemaMNmhGo4AqrW3X5lS0GuZ7CDUpd_keHLivtk43LZ7Jq-moe7R7NcRsPjTbgceujx_CM33aZBsXxuO0Ab5NT7goDumkc0-YE9ve9TbOc026tuflII6bOMtYhiKqw7yKMufAekPET6P0V88BowVEV2c7UDCO7GrfhwJsXFB_iB6GSy2aiubiwGaitwlx-laYnM-qAa25tYkOj-3pUf7R9_sN9ZpBXHYPYkqqBWh3eojVOgNVkoRFGMuIxnGINt7oss_nF04eWx0ZJlWeRVHNUhf2esPIdk7pDbPEY0HE6xEh8mOVANMA2Ov7ABoF8wq6N6DlGIXi8BLehyPA0mT_xzZf48BcAwUosNvqdzaS7gr1Ok7R-Z3BGzQ2usibMZ44DnD4IObMiiKkMqO2wOMg9EEW5c1zzLZymVeszEEJMeasvjfa7FcPz44r28xDDQG5YmWWK-e8ehPM3mtcOpXsD9yYxLFpn6fKGqsf9bjIBKl5CZ4wRPNp5RjSG2j2Of-F88k2cMnLNFclV5V0roY3suwSB5dPIGPTcQ2Kk-qtVCUj99x2INOclGk9NplaIq6bFoLgEN_IFhtJlQCn4Lto42C1np3-c8pZS8VKrne9ds-MSbWWYpK5ZRjzKq-zoiq8FKGbmPYo_trBZ6djCp4nSubhSHlvFto84C0jzZpY2uf3qiOelV0cZQnGqgwF3kZpj666c8-p2kAOuj4y16tyqEb0SXJZU3K4GcZDtYdGOVGdp9RTb_fEEWCoMcUL5uOBdULnMJeUm_PMuc7B655YXYWm8JW8djltY4HqSsC_qXOBvSFv72xfNLZtc3B5zDH-k7J2MupNcjujcflsNjmu-FFPlYvRWdFJn8VxHz8SsRtPiAVdC1wwbJ1i1PZ-T_krcJa3Tn9ps0KmyXD30tmYwxNtep296VyGe43TFY9LAb7yVhedhPPIlsZPAkZA7m36zZS5lzxJqrDm8WjuvRn0Ude_epLcynhZRkWeiIgn7sS84XJP8186Ik7dXeTlkme_1MlCu0vYoJYBEMFmS8UF6qVAaYZXkh0lJanjRA8yTxErLErwhapY5nzMn7spdO9dXjNLbuslCdj0MOcizMPRSrjxcpfaeMOQOBUemWA7St2hK04vDpHyzlyIbgw2lvbwLW8_6UI-8tqSgnQTHNomHf2oB5BdF7VataRry_4sEHjH1G6zoBtMwgJU3qCDELqBvKu6a3BiET9dggAsdGSyoHHybf24MAGHS9SBEO4GUHi24Oyaga0OMCl0k_TrdR3pSVWTlgVlWLsGHZ2slKesrucG6o2jFH_SRRg6ElOqaTtdetIMbRLJY28MyfvSBQvgo5yoWx4nZbIkghAxVmWWuSDRm_EfHeeLJ_WXK0ybuXZwfO-jTPcDawZdKqQGINUxbe_gGBbO4T3o28L-7WFDAZHz2jh5DkJnKjGQM-76-4iueR9PZQLTStVFjT6VywZ7MAKj4roECcDasEwlildZKscEiwcOcNA6cNl8P7ayBe-8ghEJ3BYEZfmL7FrgnbrW_gREVDiLiPkwnbqgKgMqr-1BuC3JPkNs8qQv22iisWjIpT9DxQ9nAVypcUofMlVkLKtEkjnj4cESuFHDlyALuNpSGuUQBpaaxDpzNoINOC34BryAZ1LT2vzT7SQEILOjAtOTu7YgRCkm2L--GtgcjFEzjJWT5ZgNBtHx6hzdfm1uetoRQToKCwR4ApS8Wul2GqPPtEY9LGMc9jrga-sReFpSP8fOwC_X8NV6TKN5TXjBqrlbgVqiuiJGTvct-ICUQDXspEcVUYeMVwGB70FLtuDDoOJwqozK5eTMNWt0Q6fSyzxTrAiVBBs6ljQcZIPtP3sD6sJBMKxbRzGf-GTczXWk1Ssp9pjDwQaafceZSZSB3tvsMKFpunfaPZownS0zCTQr6nTITsGBk_cL5tW0dB3uZz-ZpRIqreIwLiD-rMfoyEFFjBruZdgPtkOlinnIsjhJxi46Dw7C88tfhu9gmxhqDPErFUaVy1N4kA9eYeZSDAczqadrZi4nbf7sQ4BrGdGyjxhvPXjQYDtOOluTdQ-jtZeoSZYuSWNlqwdO6DHLZ57xT7oVQnvsXkPE6UfoXY9hFQn7WD5kLgI87OPzGyoo8oBgBJgHmdQ0EtouCyoqGSYWEE4xcbAbHcYiDb3WDl8FUCzyIUXB_lDqfkfyCWzRZmEasg_zL_xxzMlNyHmZqCyv8oSzfIwBRtwNj-dejZ5huVqpkqVZXQvl2M8D1HDsdzkshnH0bOy-1P14ukNZ1-aXpsS-RBVt29aY-_KUdaCES4MHYIyC3t1hl59LTZ7ofML-6qNynnFIaSrftJmSA2201IFPjs19yHOm-kaO8ZSzqxEwqFtQ78vWvcn130NAgt4K6xqqqOg-W70dHMka5FH3j0lGKjNlj42UE1wE7IIjKhWPx7YTD5HE56JXQYvYAk-RsjqWwJKlU7ce2ohjoTfAhlBHk26UspR6PKQINXXom3W2oNdD2rTGc0UVm6ozfcN0gy5C6MQ4aQ6qSVB9Aa32Xks0JtGtqXRujO5ZO4ycewivqYUXTnXNIGSYOCeWpmHBeFhWYz-bh4piCPkWeJOx0bGnk144bbFwhz5hWEuZylQkSRbFjpE8WBSvk-IMwoadkAFjWnOZJmnhfFYPAOWEST2HZ-L69VjJWFVIyd3CHsSJjfTegFhiVJuefGYYbB_BfFhT5rf7OVP1pOfvSXb2eE7Caa6OZrfvz9ejUhmhmahYPo5ReWAqvtS_GBnF8kERhmkIC8dsTOeMYClO4i9HPtEDBdgpQh97gq41xrPp_GsUZftcY0qkztKD2wRH7HAIdL6eRBhbesd2eXemZPXHhkpaGnNUsDx1FaLJXeBsrGkWXOin4miK1gyHrPSUeXxFwXZADXKD9cTt1nT_mRTvklK8JjH6vApJc55noI05H0sxHlSMd-ivQX2xUsUS8KHLMpexkyoPCMZCgb4B00W0Upf9bCv3UYLXr7M4bhoHwEhfr546cwuTl8I39JponGPGej_5jJraWgj_hFyxHM6Sdy0ThzM5tlo22bAsSohBioorNzbkYdWM-vM8AI1NtCgVZ4WQeVk6SfQwaU71ip8HmrG75XkZJYIVXLjSo4c946T8LYAysV99NQ1CN2Mai65JcKSHPH4z3ghao0cfPKjlej0VJYOqiyolOMvcnIIHU-OI8ybsGW37KS_lAuv3IXaTYB7EZAx1u5ZVNRhnU2prGLX8SIYX1LYZT3kaCoga63osETmgmyfdZa9Hr_GGLBdj6sOl3oy7oGv-lCs1SQuK8l1-kxo19kOLXRY1ZZF0_UFPEaN4SidVU6X8TGDzOATaZehlOyyGzig2r8DDsR5IlIqsZiIpxyKLB5HjePxyuBtDWj_4c-Urh87h0pjafOlch451KbR4H30BOnXHms52aWOnxga7VTRddeCDDzaVBmoq2Q603v-QcjeOtSxsSaVDHdqDfnUVDr0Knq5pb3LJG5ev0Rl_MODOTruEvSmWmFQ0blbrAyPW19oTp5o8mtU1x2Id5oOorjQSUX6i_ITZZAAkg4McsLOtddgU-NZ6xR9sUVDTXUi-v7ujzZGlRQ3vMmrWydUZRD3a028gxiNoHdOu4vK4hi_xId-Tw4-5lzFMoOk-rEoz7Btq3LAgOjdiiXJOOTdyBGClFiiGVNKlH_nJdCzZoIEe80_gaoB8bI2HaMqQ-oSBFNSw56fXXNaNStaYg4bFMDVKq73bU41oHH_R5MP8I2V-6G0Pe6Jc0sbpJTtMTS1KhhZE0-P8KFXFXG5KJwyBje5MJb21bWCUjTe0w0O-6-ycqKkAjDaeHvcPLakR0CrwRG6DHiCEm3YD692SCwALevKJqkz2fzRWHl9mg5cyPxo8NOCfQGLoTPZUwT5RL3SlwgmrU9RJibNCNUvHjMoIbOWP0b8Jkcp6fBXPSlFBDJ45DeaBVB32OV2ELmU7JV31BMN3wz77rfa7bT8LcQFlwV8U7bsBNJue88chnTNIFTAzCm0r8_oosRZ9FtdAgcVPkziUIXPFFg8W6_Q83avwrNDS-xHcmK5kNYQ2-zXlybzmGD_LYTqQXJxuTsU2lz6JAP_Pv_27rRNqlXeQ0vDybnDh2PmyrZvd0cgEPJGGIVFOxFQgmZUKnIsozVU6MrSD6RoZ-jz2li1_5apQIiwZl05EPDgu95fFLsfYmuoXKCUHlijjOkpcb5MHvDVOYV2OpuXbfVDRG2YUHAjS0o7QWN2th6_wdm3lvb7UJbqCaKN2wFD2iPUgFtHANwVk2SjM1V0wugrfPerBK2pwdmUW0vV6GIyMmYbEIngcPV9F809eHV-7kdRI2Bvx1DNVOOSzdZSwUYX2IH3Xoh-9jgNvQkphe9utKsBTooJEScsbS0KTvKYfwYb1val5oMez0ZHkdEDAZF5kaS3StEwPQCE0upnPyecBy6y651FRsSoNq9BFSR6G2dgS_VlgyWzYlxdlBmYmlfnYFToilTm39XLwMdmBF9PoTL51-ikaM36d5dXdHmMxRib8FOsydELGTg_niHgNWL0pKpg_V47hnQk96D7jcXppEzsv54UfY9HDFlTHxgXUeW4HLpax4clAZsS2DaijAhihEkzYepaUKpJlnKQuoPew2U4d_ivh1kjDPfQ0rYRFSnpbixhRU4rqKEfSdk9LQLq1BARS6tTS6Q5X25Q3VVsFvsvLpOaR5C7h4OG--dM_L0RxsyhBFU_zqs7iLHJtKR6wm2Ppy2Ha9F-wf3h4uNb4Vtes-YKv27svmnGZpf6qX1JvxJIcn6WLzn6_CP4MAX2-CBBxi9xTfzv4yrqB8PnN4Ml_tV1-aLFD8f2IIDG5wZObWTZbbDfq5dIDooAd_vc9cHcUP7PH0ygdtoPQaNuLNkMrLM0KhlLxc6QaEcYo34bGsu0ex-eCp7Ta82tgXgNGBk_37vn9VApUxryOVCLCxDkXHgyfh07xQlQ9mw5TMZiKGOGwXPHDA9p70tP0etw83duKU3hel86CfnbgYM8GL2PbEeWoNy2N2SqMaDiBgZiyPEFy2BkuarQgm3ows_MRdTJh2aBXij67gbihxM6DzZ_ijQvTvG6L6_4UzcGEjR93UNO7A6tyWXrykSBooGrZPeIiHVZvnxZJTK6BUc6dutyfKdwcjM_q5DIhU7g5Yte34MOLkSo1-kUPzGBNFPseWL3SGbwnqvLn35BnDN7hr1caKAN_wo5NKW7549XNT1ff7uT23VegAIT8dIXYhKah8JmvdWZk4mvC73Lff99AaNGJ4Ef8G2s__7Y4hfH39bff_LfbD99-_9X__Pab2y__8u7r2zcC-YEfQXhOCO8IVrZBYEKwteoWG0w6DfaoK15IDQM8Sd2RiO3INkjC_RZRW_ADU-DRQI7wBiZWIpxA9-dfRlDAEeYSZ2bdJDeCyo1wdd-tmYd5CX4pDZ-dEHogKcnJs497uoQBp_xe4ptoGXdlraEZ9PzYmb1d6yfbV_n16mGFcJV_1vBVfgqfwuMGWx7Wj0YAzbmaRBruIqAO4XMPDcyIsOEhZG-fff5oSyf6DiH75o60GKExPKCQuhzANSJLvhjpM6qyRMR1GYVVWjOlcpaBG16OSJ8-hKcPX-nDev76H84YL8crdXidbsGb6LfTgJzn0Ek_CwQpz4tQIBAcJtNrkXORhAmEKbmIKxlnOeiXQlQQlotUJWkaKfi_rFmZhCpUdZY__0qnQEiLm6Q8AUIquMp4KfPzIKSfXUE9RRqNpRBAjVIVo895Cmn0POvMiKIzouiMKDojis6IojOi6IwoOiOKzoiiM6LojCg6I4rOiKIzouiMKDojis6IojOi6IwoOiOKzoiiM6LojCg6I4rOiKIzouiMKDojis6IojOi6IwoOiOKzoiiM6LojCg6I4rOiKIzouiMKDojis6IojOi6IwoOiOKzoiiM6LojCg6I4rOiKIzouiMKDojis6IojOi6IwoOiOKzoiiM6LojCg6I4rOiKIzouiMKDojis6IojOi6IwoOiOKzoiiM6LojCg6I4rOiKIzouiMKDojis6IojOi6Iwo-mJE0SiMi1LU6gA48iQ4nXkapWERqVEPA1OLnfRwFJCxfvqQBtT02axBKQzaTfv5d0_J9Y9PTv4kDqm3yaNdGBDSr5vtx_4Qt5PCX-MZjjs7tbFnQEjHNcHRaymF9HT1ZtBIQ6iiTq1Nqui7783k9OvgQlnBw5DX4JPKMuPwvhmL8oLK2CfhQh3Q5Hm40P98p_5yqFSHyKn3dIQwOqJt_ocgjBYhj8KkgEcWEavjsBKVhJg4D-s0LhDTgEMcI1iqijQUIo5YxtOkUGEqylCk1Hh46n2ewIsWN0l1E6cn4EVVHNWyYmyGF53hRWd40efrX3kdIiRYKcbpGU8Lum7xy5Xa19_-M4jQ743zaY0CAWaYpEHdos_nsD8m01VjzWfMYZrUmCkW2Lh0xlSdMVVnTNUZU3XGVJ0xVWdM1RlTdcZUnTFVZ0zVGVN1xlSdMVVnTNUZU3XGVJ0xVWdM1RlTdcZUnTFVZ0zVGVN1xlSdMVVnTNUZU3XGVJ0xVWdM1RlTdcZUnTFVZ0zVGVN1xlSdMVVnTNUZU3XGVJ0xVWdM1RlTdcZUnTFVZ0zVGVN1xlSdMVVnTNUZU3XGVJ0xVWdM1RlTdcZUnTFVZ0zVGVN1xlSdMVVnTNUZU3XGVJ0xVWdM1RlTdcZUnTFVZ0zVGVN1xlSdMVVnTNX_jJiqP__2fwE9gkAZ)
