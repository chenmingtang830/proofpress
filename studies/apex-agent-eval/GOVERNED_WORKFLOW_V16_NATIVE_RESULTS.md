[//]: # (ob:76173525)
# Governed Workflow v16 Native APEX Legal Results

[//]: # (ob:bfbaf2f2)
## Status and interpretation boundary

[//]: # (ob:3d713b2f)
This is the detailed record for the v16 native Claim Graph projection panel completed on 2026-08-30. It reports 72 of 72 scored cells: 12 original APEX Legal tasks, three context mechanisms, and two executors. Each generated artifact received three blind grades against the original task rubric. All six console, five new-DOCX, and one edit-DOCX task denominators completed, with zero inconclusive cells.

[//]: # (ob:80436104)
The quality number in this report is **mean rubric completion**, calculated as the mean fraction of original APEX rubric criteria satisfied across three grades. It is not APEX Pass@1. A `0%` cell means the graders found zero satisfied rubric criteria; it does not mean the runner failed. The staged graphs contain candidate claims, not lawyer-admitted matter knowledge, and none of these results authorizes real legal reliance.

[//]: # (ob:cc8a3a05)
## Version ledger

[//]: # (ob:720e873a)
| Version | Evaluation unit | What changed | Result that may be relied on |
| --- | --- | --- | --- |
| v11 | 12 original tasks, JSON-only rehearsal | Compared PR36 v7 and v11 graph-only, but did not create or edit native documents | Useful construction diagnostic only; not native APEX E2E |
| v12.1 | 12 follow-up asks derived from two parent tasks | Agentic, full-graph, and static conditions | Original absolute score used the wrong parent-task rubric and is superseded by v13 |
| v13 | Same 12 frozen follow-up asks | Regraded the existing v12.1 answers with an ask-specific lawyer rubric | Correct retrospective score for those artifacts; not a new executor run and not 12 independent APEX tasks |
| v14 | Same 12 follow-up asks | Larger initial seed and no fixed tool-call cap | DeepSeek improved materially; GLM and Sol deltas were unresolved |
| v15 | Same 12 follow-up asks | Added raw-section BM25 RAG and Static plus open-loop controls | Sol favored RAG; no universal mechanism won |
| v16 | 12 original APEX tasks with native output types | Governed graph disclosure, small-seed open loop, and claim-plus-source projection | First complete native 12-task panel in this line of work |

[//]: # (ob:82ce734d)
The v13-v15 percentages are not directly comparable with v16. They use 12 narrow follow-up asks from only two parent tasks and an ask-specific rubric. v16 uses 12 original tasks, their original rubrics, and their required native output types.

[//]: # (ob:576119f4)
### Historical follow-up panel summary

[//]: # (ob:f9a69e28)
| Version / condition | DeepSeek V4 Flash | GLM 5.3 Flash | GPT-5.6 Sol |
| --- | ---: | ---: | ---: |
| v13 old Agentic, regraded | 68.50% | 76.41% | 80.93% |
| v13 full graph, regraded | 67.27% | 74.31% | 85.97% |
| v13 static, regraded | 67.78% | 78.40% | 89.03% |
| v14 open-loop Agentic | 84.07% | 81.39% | 82.41% |
| v15 raw-section BM25 RAG | 68.43% | 77.73% | 92.31% |
| v15 Static plus open loop | 71.48% | 74.63% | 79.86% |

[//]: # (ob:95846bff)
## v16 mechanisms

[//]: # (ob:65c4b860)
| Report label | Actual context path | BM25 | PageIndex content supplied to executor |
| --- | --- | --- | --- |
| Governed RAG | Bounded disclosure of admitted graph claims, relations, lineage, and evidence bindings | No | No |
| Small-seed open loop | Small governed seed plus read-only graph traversal and optional `not_governed` gap search | Only when the executor calls gap search | No |
| Claim plus source | Governed disclosure plus up to five global-BM25 raw-source receipts | Yes | No |

[//]: # (ob:3589c3cd)
“Governed RAG” is retained as the frozen experimental label, but **governed graph disclosure** is the more precise mechanism name. It is not conventional raw-document RAG and it does not use BM25.

[//]: # (ob:f852e956)
The shared v16 context builder nevertheless executed PageIndex on four non-exact task queries while constructing the unused hierarchical branch; eight exact queries bypassed it. No scored v16 condition consumed those PageIndex results. This was harness overhead, not treatment content: the original formal run incurred `$0.003117384` of PageIndex cost, and the artifact-preserving v2 reaggregation incurred another `$0.005936562`. A future runner should lazily build only requested retrieval branches.

[//]: # (ob:27321216)
## Aggregate v16 result

[//]: # (ob:280daf18)
| Executor | Governed graph disclosure | Small-seed open loop | Claim plus source | Small-seed context / governed | Mean small-seed tool calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| DeepSeek V4 Flash | 14.92% | 23.16% | 9.99% | 22.78% | 0.17 |
| GPT-5.6 Sol | 15.47% | 25.29% | 20.59% | 68.97% | 3.00 |

[//]: # (ob:54c711c2)
DeepSeek small-seed exceeded governed disclosure by `+8.25pp`, with a task-paired 95% bootstrap interval of `[+0.31, +17.97]`, and exceeded claim plus source by `+13.18pp` `[+1.85, +27.40]`. Claim plus source was below governed disclosure by `-4.93pp` `[-9.72, -1.04]`.

[//]: # (ob:cca0afa1)
GPT-5.6 small-seed was `+9.82pp` above governed disclosure `[-2.01, +21.59]` and `+4.71pp` above claim plus source `[-7.79, +16.51]`; both intervals cross zero. Its claim-plus-source delta over governed disclosure was `+5.11pp` `[-2.47, +14.68]`. The resolved mechanism signal is executor-specific, not universal.

[//]: # (ob:bd40a808)
## Per-task rubric completion

[//]: # (ob:24e21376)
| APEX task | Output | DS governed | DS small seed | DS claim+source | Sol governed | Sol small seed | Sol claim+source |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `World425_jcf_01` | edit DOCX | 62.96% | 77.78% | 55.56% | 66.67% | 81.48% | 66.67% |
| `World425_jcf-03` | new DOCX | 28.57% | 57.14% | 14.29% | 0.00% | 42.86% | 42.86% |
| `World425_tas_02` | new DOCX | 0.00% | 16.67% | 0.00% | 0.00% | 38.89% | 0.00% |
| `World425_tas_04` | new DOCX | 25.00% | 75.00% | 0.00% | 25.00% | 50.00% | 25.00% |
| `World425_tas_05` | new DOCX | 12.50% | 12.50% | 0.00% | 12.50% | 12.50% | 12.50% |
| `World425_tas_07` | new DOCX | 0.00% | 0.00% | 0.00% | 14.81% | 11.11% | 0.00% |
| `World425_AVK_01` | console | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `World425_RO_02` | console | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 33.33% |
| `World425_amk_01` | console | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `World425_amk_04` | console | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| `World425_jrf_01` | console | 0.00% | 0.00% | 0.00% | 0.00% | 33.33% | 0.00% |
| `World425_tas_01` | console | 50.00% | 38.89% | 50.00% | 66.67% | 33.33% | 66.67% |

[//]: # (ob:7ca1ac1b)
### Output-type view

[//]: # (ob:5e139449)
| Executor | Condition | Six console tasks | Five new DOCX tasks | One edit DOCX task |
| --- | --- | ---: | ---: | ---: |
| DeepSeek | Small seed | 6.48% | 32.26% | 77.78% |
| GPT-5.6 Sol | Small seed | 11.11% | 31.07% | 81.48% |

[//]: # (ob:4b85bbc5)
The edit result demonstrates that the native edit path works, but one task cannot establish general edit performance. Console tasks are the dominant failure mode.

[//]: # (ob:c26d9ca7)
## Context, tools, and cost

[//]: # (ob:6f2c6d01)
Context figures are conservative accumulated-state token upper bounds, not provider-billed input tokens. The sanitized report does not contain per-cell provider input/output token counts or per-task dollar allocation, so per-task dollars must not be inferred from these figures.

[//]: # (ob:72069f92)
| Executor | Condition | Total context upper bound | Mean per task | Tool calls |
| --- | --- | ---: | ---: | ---: |
| DeepSeek | Governed graph disclosure | 287,789 | 23,982 | 0 |
| DeepSeek | Small-seed open loop | 65,562 | 5,464 | 2 |
| DeepSeek | Claim plus source | 287,617 | 23,968 | 0 |
| GPT-5.6 Sol | Governed graph disclosure | 287,789 | 23,982 | 0 |
| GPT-5.6 Sol | Small-seed open loop | 198,479 | 16,540 | 36 |
| GPT-5.6 Sol | Claim plus source | 287,617 | 23,968 | 0 |

[//]: # (ob:8cc5dc97)
The formal panel used approximately 1,414,853 context upper-bound units across all 72 cells. Its 350 model calls comprised 72 executor generations, 216 blind grades, and 62 small-seed decision calls: 24 answer decisions plus 38 tool decisions.

[//]: # (ob:023ff80f)
### Per-task small-seed context and tool use

[//]: # (ob:6ec4e180)
This table supplies the task-level efficiency view that the provider billing report cannot. It shows accumulated-state upper bounds and tool calls for the only mechanism whose context varies with executor decisions.

[//]: # (ob:777cc60f)
| APEX task | DeepSeek context | DeepSeek tools | Sol context | Sol tools |
| --- | ---: | ---: | ---: | ---: |
| `World425_jcf_01` | 7,666 | 1 | 12,935 | 2 |
| `World425_jcf-03` | 3,570 | 0 | 21,684 | 3 |
| `World425_tas_02` | 4,411 | 0 | 15,729 | 1 |
| `World425_tas_04` | 14,055 | 1 | 23,230 | 2 |
| `World425_tas_05` | 4,778 | 0 | 17,238 | 2 |
| `World425_tas_07` | 4,768 | 0 | 23,994 | 9 |
| `World425_AVK_01` | 5,373 | 0 | 5,373 | 0 |
| `World425_RO_02` | 5,104 | 0 | 23,692 | 3 |
| `World425_amk_01` | 3,145 | 0 | 8,900 | 2 |
| `World425_amk_04` | 4,813 | 0 | 23,991 | 8 |
| `World425_jrf_01` | 3,784 | 0 | 17,618 | 4 |
| `World425_tas_01` | 4,095 | 0 | 4,095 | 0 |

[//]: # (ob:bb85c90d)
| Execution stage | Model cost | PageIndex cost | Model calls | Accounting note |
| --- | ---: | ---: | ---: | --- |
| Route canary | $0.0036772 | — | 8 | Fixed-route qualification |
| Native qualification v1 | $2.92440102 | $0.005670882 | 91 | Generated and graded 18 qualification cells |
| Qualification v2 reaggregation | $0 | $0.005632326 | 0 | Reused artifacts; shared builder still reran PageIndex |
| Formal v1 | $8.9686168 | $0.003117384 | 350 | Generated and graded 72 formal cells |
| Formal v2 reaggregation | $0 | $0.005936562 | 0 | Reused all answers and grades |
| Governed downstream reuse v2 | $0.1489397 | — | 4 | One isolated evaluation-only second hop |
| Governed downstream reuse v3 | $0 | — | 0 | Deterministic revalidation |

[//]: # (ob:bf9f1de4)
The successful v16 chain cost approximately `$12.0544` before artifact-preserving PageIndex rebuild overhead, or `$12.0660` including it. This total excludes earlier v13-v15 experiments and failed historical attempts.

[//]: # (ob:b7dadf57)
## Governance findings

[//]: # (ob:353e1668)
| Executor | Condition | Unsupported claims / task | Citation errors / task | Authority errors / task |
| --- | --- | ---: | ---: | ---: |
| DeepSeek | Governed graph disclosure | 0.69 | 1.50 | 0.33 |
| DeepSeek | Small-seed open loop | 0.72 | 0.50 | 0.11 |
| DeepSeek | Claim plus source | 0.78 | 0.11 | 0.22 |
| GPT-5.6 Sol | Governed graph disclosure | 0.17 | 0.39 | 0.00 |
| GPT-5.6 Sol | Small-seed open loop | 0.17 | 0.00 | 0.00 |
| GPT-5.6 Sol | Claim plus source | 0.31 | 0.56 | 0.08 |

[//]: # (ob:39cb0be1)
These are blind-grader findings in a staged evaluation. They are not Human Approval and do not authorize downstream reuse.

[//]: # (ob:db33ea5e)
## Is roughly 20% normal for APEX?

[//]: # (ob:be6adc59)
APEX is difficult, but the v16 mean is still low on the closest available public comparison. The original January 2026 APEX-Agents paper reported a best overall Pass@1 of 24.0% across 480 tasks. The live leaderboard has since improved and now separates Mean Score from Pass@1. As of 2026-08-30, the official Corporate Lawyer leaderboard reports GPT-5.6 Sol Max at 63.4% Mean Score and 35.6% Pass@1 across 160 legal tasks. The overall APEX-Agents leaderboard reports GPT-5.6 Sol Max at 56.7% Mean Score.

[//]: # (ob:a70202fb)
Sources: [APEX-Agents paper](https://arxiv.org/abs/2601.14242), [APEX-Agents leaderboard](https://www.mercor.com/apex/apex-agents-leaderboard/), and [Corporate Lawyer leaderboard](https://www.mercor.com/apex/apex-agents-leaderboard/corporate-lawyer-agent/?harness=w:t&pass=pass-1).

[//]: # (ob:267c0ed3)
The v16 `25.29%` best cell aggregate is Mean rubric completion, so it should be compared conceptually with Mean Score, not with Pass@1. It is materially below the current 63.4% GPT-5.6 legal Mean Score. This is not a leaderboard reproduction: v16 covers 12 tasks from one world, uses a local projection harness, and isolates three Claim Graph context mechanisms. The gap is therefore a product diagnostic, not a claim that GPT-5.6 itself scores 25.29% on official APEX.

[//]: # (ob:a4180fcb)
## Why many tasks are exactly zero

[//]: # (ob:308e56b8)
The zeros are substantive rubric failures. The panel completed successfully; all outputs were materialized and all grades were valid. Several original tasks demand exact primitives that the current claim abstraction did not preserve or disclose:

[//]: # (ob:0f793792)
- `World425_AVK_01` has one all-or-nothing criterion: the exact tax amount `$18,486`. The graph instead preserved a defensible conclusion that the exact amount was unsupported because filing status, basis, depreciation, gain character, and S-corporation status were unresolved. That is honest governance, but it scores zero against the benchmark's expected calculation.
- `World425_amk_04` requires exact annual tax values for 2022, 2023, and 2024. The graph records the ineligible-shareholder event and some income facts, but not a complete typed calculation chain for the three expected totals.
- `World425_amk_01` requires six linked authority and fact findings, including the exact Treasury Regulation rule, Wisconsin community-property status, residence, marital-status uncertainty, the missing-consent consequence, and a recommended confirmation step. The graph contains general election/consent uncertainty but not that complete authority-fact chain.
- `World425_jrf_01` requires a concrete proportionality conclusion, a tax-code violation conclusion, and the nonresident-alien consequence. The graph contains distribution data and risk language but lacks the exact authority-bound synthesis the rubric expects.
- `World425_tas_07` requires a nine-part passive-investment-income termination analysis tying statutes, regulations, historical earnings and profits, three years of gross-receipt ratios, and a triple-net lease together. The graph explicitly records that the necessary Income Schedule, lease, and authority text were not retrieved in the construction batch.

[//]: # (ob:3105a342)
The core issue is not simply “too few claims.” A reusable legal Claim Graph needs more than abstract conclusion nodes for calculation- and authority-heavy tasks. It needs a layered representation:

[//]: # (ob:580bdde2)
1. **Conclusion claims** for reusable legal or factual conclusions.
2. **Typed evidence atoms** for exact amounts, dates, percentages, parties, units, and source locators.
3. **Authority nodes** for statute or regulation text, jurisdiction, effective date, and citation form.
4. **Derivation nodes** for formulas, inputs, assumptions, intermediate values, and rounding rules.
5. **Task projections** that assemble the minimum sufficient claims, atoms, authorities, and derivations for the requested work product.

[//]: # (ob:90cabe2b)
Exact calculations should use a deterministic computation tool over governed typed inputs. Exact authority questions should retrieve and bind the controlling authority, not rely on an abstract summary claim. Missing primitives should remain an explicit gap and should trigger raw-source retrieval before execution; retrieval evidence must remain `not_governed` until separately admitted.

[//]: # (ob:d449a350)
## Next diagnostic before another large paid panel

[//]: # (ob:e32764b5)
The current grader records only an aggregate rubric fraction and governance-error counts, so it cannot distinguish four failure stages: absent from the graph, present but not disclosed, disclosed but not used, or used but rejected by the grader. The next qualification should add a per-criterion matrix, without exposing the hidden rubric to the executor:

[//]: # (ob:1bb6794b)
| Diagnostic stage | Question |
| --- | --- |
| Task-derived requirement | Did prompt decomposition identify the calculation, authority, factual, drafting, and output requirements? |
| Graph sufficiency | Does a governed claim, typed atom, authority, or derivation exist for each requirement? |
| Projection | Was the required object disclosed or retrieved? |
| Execution | Did the artifact use it correctly and with the required precision? |
| Grading | Which original rubric criterion passed or failed? |

[//]: # (ob:e626514f)
Run this first on the five zero-heavy tasks above. Then compare: current small-seed, small-seed plus typed authority/calculation tools, and a raw-corpus upper-bound control. That experiment will test whether the Claim Graph product shape is sound but under-specified for exact work, versus whether projection itself is the limiting mechanism.

[//]: # (ob:d4194042)
### Optimization arm: do not cap quality discovery

[//]: # (ob:a9616d2d)
The next development run should optimize task success before optimizing retrieval efficiency. Add an open-loop discovery arm with no fixed graph-traversal count, BM25 query count, or top-five lifetime evidence cap. The executor may iteratively reformulate queries, request more result pages, retrieve controlling authority, gather calculation inputs, and return to the graph until it declares the work product ready.

[//]: # (ob:de6e6846)
“No fixed retrieval cap” does not remove operational safety boundaries. Retain the model context window, a generous wall-time and total-spend circuit breaker, read-only source access, complete tool receipts, and the rule that retrieved material remains `not_governed` until explicitly admitted. Report score as the primary development objective; record calls, tokens, latency, and cost as outcomes rather than using them to truncate a potentially correct answer. After a quality ceiling is established, ablate calls and context to find the efficient frontier.

[//]: # (ob:ca34ef9a)
## Evidence and reproducibility boundary

[//]: # (ob:ca44f652)
The sanitized reports record aggregates, denominators, context upper bounds, tool counts, terminal receipts, and known costs. Raw APEX files, prompts, generated DOCX artifacts, grader payloads, provider credentials, and private source text remain excluded from the repository. The canonical runner and contract live in `retrieval_adapter/run_workflow_utility_private.py` and `retrieval_adapter/native_e2e_contract.py`; the concise operating decision remains in `GOVERNED_WORKFLOW_V10_DECISION.md`.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzAxNGMwMDBjODBlZThhY2JlMzM0NTVlNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjNjMGUwZWNmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83MmNiNGFmOWIyMmQ2NjI5NDExOTgxZTciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Y1NmE1ZGIyNzA4NGMxOWQwZjBmNjE1OCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfWtz3EaS4F9BcMa7N3J3C-8HHRuzOlvj9a5teSWNfRseBVkACiQsNNDGgxRtOcI_4j7O_Tn_ksvMeqC62QQpktuO2UCEw2p2A1VZWVn5zqyfj1jblwXL-pMyPzo-2mxObMfPbNvOYpvzmGUp9zw_CHhwtDhKm_zqJC_PeNfDs905c4Pw2CmiJEh5HqWOF-RhGLHE9bhvxyzNmJvFfhZ5MF4R-0Xh8sRlTpakUVRkds4DJ89g3LzssuaCt1dHxz_jH_1Jz85ghor1ONUCPqS8gi--5W1ZlCytuNXyi7Irm9o6h-eb9spKr6xv2qYpNi3vOnhnw7K37Izjora-bpsfOCx3aHHA877fdMdPn56V_fmQrrJm_TQ75_W6rM96Vp_Fnv106-2W_ziU8Plk6Hh7kjV1x2vARd8O_JfF0TlniEQvs7nNs-JIfHPCL-ghQC4_idws9VmRpK4LuHIT33GS2OERQta0PS7tpCprDpCrHalOiiBkQZ66kQ3YdJLcLuwidIJYLEdCd5KxTTdUsGAX4cyaNu-Ojr__-UhO__MR7HLTdvhJ_MzzkxRQ_v3RUL-tm8v66A2sQdEDbnA_5CXvnrINf7cEgOp-yS9Y9fTzF98-f_n1889Ovnvx8j_-8uWL706-dcKTr5-9_uLb5ycvn7_665evX63W-dHig4iL9X1bpkMPe3qSsq7sEAJeFSesA1z3nMYb-vOmxRW8LWscsrvqer6GX2q2xq1WK1nAqx2Sx9FxPVQVrCs7h_3kAiNp1WRv4ekodCIvcHF22Mqev8NVf46UWPPc-q5p3xZVc2ldOKH1NevLC249--b5_7G-5GessuAlCQTLc4JugzTJL-GbP1h3HeUlhz3rkbT6qw2uACkGqO_ol8UIZ1qkrHALdwvOVz3rh85idW6V8F0Ls8M3eCLSZqhzBqdpCsI_WHcaYAIqL48cL3WLR4TqNRxmC_7rz7mVw4tlBRgUxGoVTUvfIx5rgcdPK1aurc9btjm3NiOwG9ayLUhj2_dCx_YfFVJu_TiwquyvrHpYp7yFUQA-AL7leJJxGU-erDmrrXZI2zKzgLlsKg4zTECaZTHzmL1NkcD1iNMBMs54e8uuXnt4Ygcj1-Zx5LF7zvZeT_beeg6MYRDoG-qyh2--O2e9JU5dDn8KQgcMwbdrZpAW8bzt7XIzHnl-fk-wXhOReMsLJ7A2vM2AbwHzgp1uuVU3vZUDA8_66oo2BDYApckl8H-krImtCYBbOEmxTUT_RsKnzOAkF00Fx3w5bKwNq3lldcN6fesh_IN1pxEm9rBIWJhwN35EsMZ9fQo4qvOyF3v8GeebV5y_tb71rb9UrDuH7z7_8isrWHn676l9TYLYD9Nim2HgcV5zpJOyW3e3EPe1hycQEwaZn8ahfc_ZkGLpHJPuASt7lvVw3i05FmCzx_X-76_cAP75Bijsizrn7-j3KSR4QZxkXpbfE6zffv27Fi0vn33-26__zyKWA7wSv2KCdxZt8xOvLf4O6L9c4wGoxDoWEwRexAHoZ0F4T8jw2IFK2AIU-JLCUzqUVQ7csQY1pAXYKpDLABjPBhDpCm8TULmR5zqusw3Vs7OzFsRnL6RBS6zlFtK54ZUJAnJjO2eFEz9oZuCMtFYQXu9HpeCMRBaqvVXTDcCX3luv1qyqlh2HX5sN7F3VNFNkFIBa7TiZ-yDg9IHuxsn5uwz-QRgVsAaYoGOffhyv3GCzmRRizGYFcx4E2-ffvF4Gq9AE7RKo-_TjZBW7m82pxVIAcC-UpxOwpblvs9je3tRveLvsWff2mqSubyGqyRenSMvnruNF4SNA8V5ok_Tie-vF0G8GlL6fvRpRQ38RHi3CI_2dge40RWBRxhyWOekWiGL4Jb5k0fy3CLc9z09gJeCOl_h-cu8ptw7bp4bkelUSY-4aEPWIqQ6--wtqkDW_tD578SngbwoXIEeCNM2CewOGvJEDNJLuQbddAzR9i_atUImQa0utlh4k8XIJtkM3ddDcME8yFm3B9an4tLD6pqm6BSm4WdPdxh8nXpsSsoWbhbntPBgC-Y5VlGdwhIWyRuZ1eyGwwrJsWA_oEciXXY98pG_eAp8cJlkRaLhhUiTug-G7kbReN72hFQA0IOvIgIDfvkLtHwCb0nWzLMiz5OFbiCQGJhKccqnoDR3qA5tN27wr14AvUHidhe_4izjwtuFdTvFLIP0ssfNHQyBirUOFHPHT5LyiN3dUKPpC_gpsawqBaZEUTs79R0FgN2QZ6CfFUAkd5hy0KgHONiJP_-i4Kzvw_VMr5YD1KQRGOcuLINrjY2B1BnsG8MCpuk3z3f_GlHUeeNwJw_gh895I9H-tO6CcBr0yJEjWHZgKUgR9WpIZPakDJ1lqp9x5CGywXR0nNpFW8MwSVCpUM9WraI0zQWig02jjdGXBe1cT25WnnsdZwLdA-wI07GY4O4edd-2PwIikY4YOCZS9f75l625_e8r1w0OWZ0HyWPCQsgAWQ14WRZmBLFqAht5rxwr5K-Dnri9BW0C3VVPTj6hbTaCNRbZru0X6WGC-agYw3Ltj63t8dPkMnY8dMDbgVm_-l3LasvZdebFq2rOnLO2euqHtrBzf9aeMiTDKbJ57jwXma4m2UzdYuclHyA2AV2QccMe0vgvo_GqPG2gKm74T20W2jc3vzq-sNauvpAKDlM_fMXJk_MTb5hYivP3tKV5ixzwI0_ix4EG04TPirW5I4ZzWJOUljgpWVqgG0HGV8kzibQJtdhElXrQj7B8A5tI6_a5pq9x3g5Nn3_7Hie2cWudggzQ1MB4wSpp2WTf9OWDLytqyB1O7qY_ptPB3I5hVCXJnC5uOHTDPdx8Tm1nTIqF1A5Eberm6EtB1Zf32699BBloF6LmCUa_QZfAMFNGhI89Xxad8XrGdwnyPBqqzsp48AUGSVQP5lwRIT57QaTNAQs84fIOhA-lzyaoJjCZ2xlLuPtp5eY7PoeaRocIJgAJDPG-GKkelCsRKzmGz12UNcMgDPUjXcT_l3M3BtmFesO2R-hrVsLxkZ3VDo5E-AZMgZYE8q1h7hiegvOV833WYXJym6fPOPTcK_TR4dECJVIe2BW5uSYEtI1VwqGBjgEuOfFPxghY2Y8uivoZYJ03DKPHTR4cXLOVxAKW1_ucATJ70oL_V763lcmnJ_-Ofr4HYlrAuYGb5lArEQzcMHL94dJBfDjIMUZQtyCIpvgtkrkj2S9jvC30m0IVCPLYmKp4yNYFj8SLZDhU8vyhzjgob6tctBw05H7IyLSkqcsco1F3HmCDXjPl-EQbu48JG9gCrQeX9iYJQqO52KhilqRSMC5imAWbAMLi6EJbVLiLfLFQU9uhCuNZPspYzEdSkX1SElJ-wuLBdP_N56OWgBcQOCDXup0gpQAc0pgwUWzJQDHYKz95umpI8zzAjzYRxT_UXhj3fYIS5KrMrYwQz6mwMQvHsewaku6boT0ALP8OIWinj3l3qHOc8TcESynjM4tTO3cJOssQBlpiHQVYwluXMjsLCCZmbR0HiOCmzPdfzQp6Efmajrwztfopfi9069qNfANEYKAblM1za8dKzXzsxfH8chB_b9rGNvFZiXGipGfeZD9Qzfvvz7xfyJgIWIWnQK86RLbiFmwWFH7AIkUljGFFqSduPFF6Wc8Z-HAQhqMW-7ak5jYizmvP-AWM5j1fEOQtsFrqOr-YxYshynoeEgEVqBwK0pTKiS722RhJZWV_0-kBHrtUU-P8OdaiclHewOxz4ui3P4FhXJj6Jby4AiJZz7UQZ4yPC09BfNjLCARxhZT1n2bkFpMTR3QesQxIILoqjmJCjkRkrpCLg-IyVdSfsMg2H4RxeWc_Qmzu6NReCxdf8con-TAEIKqroTVwKFye-bjKrET8LEQBFAQFbm0kFDcYjbKz2yAW5pwULI2ACGfdI-tKeGtF2vaf3D5bXT54stCo2RrjoWaUa4A5u75YaRajlDBh5X3ZFie9nYHd0EucC20QPUm2mt79hXfevoKs-s05tMOrInsMJxdRCcQEBS14-wtk4_M7En1glSPSGi8EJaByiHeoanRVE3cLIka4Kigx1RFrke4JtLHPUhoSqvKBxKnZ5xdsly9dljzhZM_intTD1hcLjYvdr3H7ATE-eEuF5BsqiFBqQaYh7DAsSXbe8KtH1MrHVzM3yjDk5S-JAbbWRrjCyibtkIMgx88B3Qz9kNotyze7GpAQ55kPyDECHosUJHrCrse1qbxeOA3-aZ18e-H9_9eLrJamoLYd1tB2ryCWGCQQYxnzphdZFRGjHMWgX6XnhXoE9pI0TQh9NG3LySx6WN9mwJgfHe-uvHUfvY0bhgUFQt6ER4pCf0FC1weufu88V_O5KrmCM-5OqJ1VSjAyviUEJxUBHQ8jDUmbARkBtWBL8gopQ5tJ5lN4_fPiFwg5LgfcMsCJinsLljPR92TZgFIsptmJaJDvAmho2sKMUZkyvMFlDge9hsIatOa1ABLF3FoI7TCcwl5Y2GmEwmVg6nNFLPJvEztCaAG282_CsLGBycWwUKLh9LWaCYPQceMIGRceFWooQNQ25GAW_7gTeGcWMFHvHkywPW48wAwvnGw7_q_sxLtep1fnm6naX9SVq98gYAc1MRurEyMDa3-Fym6ZaojscuMLGTMcAS79tLgQfQKZTIY1gYga-_qqpYPMrgMMCzMAe1cAJmgofl1AFU1A9Q03LatnlspOilTIeXj77XIwuqGMD4oLC1suqaTbEvdqmwvdx-oJdkGiFlxCHeHBR-2LVKDmtS3U6Uba_vy5-BR5pWyXlNyLUicylm4qtL8wQsgqtb2RMAJnqEqFfduRxNHUIDBGiCaWkpJrYcQVJCx1DCTLUkZHbYszOer_P9JM8LwmyOA4LP4sLzUeNjCdDZN43iUk4uclXAXisWduCfrizs8QHiKFdYwaImN2jo7QO3B0Yt9vHI-E4lu34rXhFqUT0m8yezfdt4YTkCYowBzMjKlzHVhgzsrG05Ll_MpWcyCmigruB7UaR1lCN_Kpr4ujD06NUVgMei21hdLz7j2KITZWP3LlVvO-9FcarwP4IPkThynfwQ2yvEu-j8U1k5ZZk5eaL0cqN6EV_5YkXg1USGS8Knr_7UhTTS_HKp2njZGWPs_nG8ZfQ4jP-yqapYmflJfTBFcAq1rOXs9DifI-mg3npQ-IKYNWLu5yHTjW-4Kz8WK4uFEMkqzj8aPJMgmnmxG7gxzzTeoiRrTbqNndJQFP6kuMwloMlH7FMjWnkpGliun-aGR5ZjMORdtOPNsetao6ZQYaDoyK7nUIDjExrl4KhKv0TlCnhEl0o94M44Vz5W1IVgXtvfd3I_-GkexKcNirvacxVod9pU0FVyoXKJQDoWyalBpk2GwQC_jgFbniiXj-1zkA0dqCgZYi1F_j2JXq3hKog0YMytNt-UgEpzEmaXwoEA1sGfugJ4C19I-yus6pJWbWkbSKSFi-Tibchxe6_uMLIBB1G3EvtuEgLu3C0iTwmDEqaeWgOIKmkT56c3SQxnzxRBvgaVSEw87Oy44awxmR702gCYkQfltgQXL7SaLWeYFpBKJcQUVO2Rui4nu1knAVMM-IxPdGQkffNOIQj1KBuObRoJy0pMiAs5B8HwBeAenkOxpmhiIOOiSgZatJyz0sw54F2SNakLdhO559YvDw770WUQQ-TXm2wgAFRsMLtl24GCbAUHjgLICyXKucIo7TaUKIDrjEBDtZb44Jw85DrCIuwR8OCMC4Zw_G260BmhqC2CvY9euBz6_SP9sq2PceJvNg_xSO_nYKhJbdWgZdYaMLbC9K3XTyh0g2Ka9DjKne1GD9IvDAI3VO0pouhx8MjrV8ZUqnYTyUcU9o1S5pYP6KLnfw-PSDxQqN4Uk3w88J1QV2NwkxLbyN7dGTid08FVSobz0HXsF2PJVyPPGaHalZ-_1RP5IT7eI_xqCLvp2ZiHwWWDf0WbQTJ325RL64rG_v0F8dfJS4KUddbOSHJ4VVCgtx1pUJgr5xIihVTubGcYOWT7BexcfxgrwL6ANKd9A3LAwKZZIiBHUdelPDMGx0ERuqrxPxD8lhPpe-L0elfbhgpqEnwkZU2TY85ehvh7UQqhDNy-v3HNmgiC-tjJ4JVvDmV4k9Nl13bRZrMAfzFmLYK7zurOID33Qg0qTdwMK5vPB504NSgtt8E_RI2xhPjLZNV5C6spbOyfRju5gOSpH7i-W6WB2ExenB0rq7Kw3lA4u33S3dlI25cB7b6zSmh5vRjfxU545vXMQTvgZqXIE7DVeC8Of0EkA97ovDeWcJph742lDvdHsONbFziintBE0sIVo4jkQZ6aIQTgpYY4yagMNGW8SjquvIM-WfZafVBG0WC82pjdgLxqR-HUeYnecK1ODMSkUfO9KH5xEp9LSLbD5MElEs9vpFirPnT_TOF1x-PLKmpzBfwz6038IvtV_Zoo8d35kpjCsYPWUEpGO-F84x82sBL3FUSKkuBGFIQrAL6JgxXobI-hE2gvrk28NL2cGCdDgzMCswrejmIVo7_keCFgo-hWMN_fVcYFvrD9rCA6BPb3RlWveso2NQX6l8vXsXmLHvG9HdBDeS7UbAzmP4l2P1mz7DBzrCOKw1M_UEDf-0X9WHPsNENGNj9F9AbkzXqOHBKb8SASsR5rxO6bx7yhn-3B3z5Qu7Sh4_neSvPuzYgW799XAhpQP8RB_yhLT4YQrXWCbrcGTG4RtL6G30y9ajqmwldoLBBB0vCwAsdbVAbVQqGG-huZQfK1ih8zG3wHBHHECrGWImwT7n7wNIC-e0LGY0bv70ba9zSzZTBLJltKBmb567cLS54XR_bek-fMc8ZPTQ01MQG8DR0g6JIWR5r_cEojTCssvvWOgjTFONWhJ6M1ShiwRYAUMpORVEr-RpvyazBsBVuibEF6CWlADLFOsEqkgmFYNDmUzGu0HX93M-ZkzujhjQWWYyC-sOqJZR70c58P4qcNMwi7REaCyi2c9fvVQmhag9knBDDAiWYwsu0rDCMXtbkbsWnZWrlboLLaKWrCCTWB1AAVA0mRnmqfLc0dQaTglYGh2OjNJi8qSrWYp5kk5GBuABtb_fnzloPXU_zpRwGLjhZkCJIRWFLiYWJPcvD1EmLiGV2yo0Yoir7uO383qF-o1U60-ubrKu7ndwpm9CNo0UUJ2RpLZLYRUa7_-hfNxzDYAEWNvLXhR9ijMm99uY-2xKnDNF2oynDeJxym3HcD-w9zOc65E4SL_woIX1oEfg2MqRw3_t3h3-Cf8VJHgdRlOVhpOMIRv2Nwb_uW0gjCAcD051KNECmG7kykYJsFy-wiQ8pUkIlvy1xEnhOOyllwojwtLpOuJUfIhgO7LlhpOXopSNnEqMMFteX0VD9SycQ6MXCTaC_njhckR-7UZrbPOWaIRolQTuH6z61PRRkzIiBoFsJU9zu4roQz7xsMPgMYoK1V_C9cGiFUYR0-Nuv_xfFGonjd8AqW3qW0lDAeGNjBqfMmtr-5QLD6H8E28L1fduxXTV6ALQTE50n-MTnY1qP2pzccuKdwWjzxWT_uT3LrhMNZxmn8lzPDQVZWy-5oMMxGi1dn8rdKUo2WgCnNvBNk_5FkLNYUwz2Uhw6dF5MDyCevcC-aU2Rqw6FsRg17uQqhP9vZxVYICFD9WzMetoOTuTNJeoNnK0pNZzjPDSo48eJl0R6j32pXJWgARDcY72PCCB0HF2t1jnynFum8BTwYmib4npmtneLg2NKDi10SlvKMi92eZSyIh_T6nSxmunDvmfV2X7HrOk8lk5V7SpuWjlIGNqn6LGtBlRSyDdNHuaepCF_hz_AhnDWViXQlopEj8EEsW8igUm2YCJXOGYirTf9pJ_Wd-y8SFhUpDpnzKiSG5WsO9e8KU3Aj30_YIUXMW-MnugyuNs0gTsUtdUWKCiYOad_eCbSqfqr3V8eWT-wVyGJyRUdURusprtqB_aK2KGt3sQUpztoB_BarJ-Hf1z3Q3UD4RhGWBNpNn6AZqBftu2Jl_cD7gmIg1C8GU8rBXlup1GaFH6oj6lRnzge03tXG-qcjX8bwFixnuGZvpBhzLwRSUUqKe8aR5oKkqWcxSEYv_no9TPKF8dzdK8CROWAD8KMZb4HAj_Rh3WsSVTNHR5QVYgVc-wCGAnlsGwGQHAms1qAoQscjoGsf2f1gMIes3mta7WB0opBCSNK8ZA8UdiIjE7037v-CnAglTM_toXFKGapUA-oOG5t2rA2p2qvrkQGpHOsRErWJcgU3A-0aclKeCWyxtBw0dmjHc2n044XIiSHGMIEr0-bFmBF8-1LkZdmTqyyk01y_4q9A_Zqhd7K_8icFCHy4KGP1Crl4pzQltmdxhIVQkzU3XHiIFxF5sRTLD6NvThNvJy5mhMbJaKqA9cDijzdPy22XzMWMb58eXm5WvMWoKXWfpjVb6T2d0vjpad_Ekr191P7cr-RMzXiUiXu4jNP_yxDuf9yedz_EwaJ_wX_t3T-NIFYN_BSP-aBy5k-jkZR61by2P3KUqWhXvYqPptyeRpFDDLjG0xQwcQKDJuN5CBcDvSlOgEiQ2DMSpQxrd6oAhPUrKhNkKtBYpYqBxCplzuUSjU9PVVding6RmIwNa03c9w4-pYq0H4ocQ0GaVBRMRL95D4sZHYqKZEqQ9ysL7ie7y_OFGaSiISJVqpllgTNSN1dyCWI6Bf5wdSqwVrkVSEyAzoVLqWsdskqkM6nPCB2mASFmyZB7OrTNpYQj4LgXkXA-ki7oKJ5ORh_oZaTY12wQXn3rezF7B-tCWMKK_Ip4WaSuauKkshhRWmKIsENVVV6gFTzlfWKE5fbyVBET6QI1WJ-Bpjc6xIhM5ySiijFHgG_6VWBgUrglno2pXBLZYcf37wzWREWPArzxCm0x8GoUpZIe0idsUhbAf68Rgsatft44cehDGgKrQwrSWBDNfA5lbAWvO7KVKS4qHpcjQkxsBwUY6eDoRynPGMD-eYqhKmjsiCQ-Ni0E8vhKGFI-vzOyJaBEwbj8VYcsVdLxRGlwwCrinaSkxF-RuzjHNAA3OtMGwNCt0AGJQ4MVWCYBTMpr7PzNWvf_nNHFktGGv1Yzbv6W73cE15RvV3V4ut6INJ5h2Q18I40JhBh7gL_74m1wCffxLUqZ0U4SiBuIEDA8ZJs9fOGDHWq9xO59c2aU70N_ENGvViaZBQq7Rhpawt-aSGqaijBqPRCyYTr9q3RMdaIpUOwe2-RGLQJI0y6rNd67cKwEUeyeA3qKej4V5iJr0BqB6xB-g4b-QJZUTnpGv1gV2Cagl7fwuiKTmB6kSq4gAMN87JqKWlggC9b9Dr3V0JZWpcdDHa2lI12hR_8x0G8TAyAEL5ec0pghJ-LEpRbSVd8Y-6MdGh3YxChEvz_qRrdmF7vA50IvRUaVUtCE-3DDqZVbE1jmtEBa_F1RAUcIcqTQ3yPJ29B-SfvYKE5hqwatdHmAzIZq25qicF-CcPw2sTK3gVjR2XVWtfKWc9ETWwJZmrF6rMBHXa43oplbzvz-OvVCr9md1WjU17mBkqGLuhul95U5NfAQg3HYQkMEuM9HRaXLcsauC9lrS3lIRCOFrF2Bki6osmuNJehettWUx38YbgeOIhxMsZwdYDqoux1qd4V1uygOn6GqvFS5mVaxII6RUqAJNjmZc17VDQ6jKuccZTqJlZhvWCglD3lqamzroJaHKUXmidfiPW8ys55TieDBpQT6fNG2gQxPiQ1mexGcRohjswioJT12flqTxME5W5ycofbfpgmTAeXjE4Thnx-SK8IVM9MlagGu70TaaKAhVrLTFOo1E0umafBw5bbqDDL0klvFAODssZAYRbhKZRetXDDTIhcz2Gx77IicRKNB6ONhcTDQxpRDMJp_rfaxUFeE3fW2c-sb_Q4phBFwSjKxY1qjgUWXvQlfqCYgay4Ep4MipthAenfag8nGj1NhFA5hzwWFoGtubGITf4wwBnPy0xIYl4UssIJAZEhS-XWQt8uTOTjRJ9hqZj42pwJH4HxSSagSgYjAA2tN_IgUq7WmoPC23MpMMUcLfIOPMEoInA1AaGNKmi0Do6T0DHCXNk14l6w_7pcD2tQC0kT1qoZjox4XmgCKtVsuQa-0wJyzCel4hypm0-cJYf7aeKGrp-kOuph9BhRHQYe0CUErOrtVDUh5AVmV9bzbf5r_ShbTugZFK-gNWPGvWIYWHdFWpl-eSGZCxxw4qrjGZUlMQKnK-srIWxNzVjPtkaFg9Wa-5HNQ8QqngBozrB6bSv3XefuCquIqxjRJ8Zv-uBQIFhOtJPTj6GhSjtcsE2ILE2YsIls33cL23bDwNdRYaP_ymgTPUrjFOUs8_IsdxOWx7b2yBm9VEwefM8mKCJaolXhJTmdZfhd2e0yayIXhZED5k1QnrvKgSA3ZXeMdIAgqGC7qhSSfFZrQMrMAQNaf9Q_DvQ9gDCob1v-g9BD0yujWlpI0BpxvR0ak_TDchTAlGugLBy09trynUjPBTMQaa_plCZ6XgJD186Lvtmq8JgQD6nDQ1ZENpxk7Zky2sfoGMFD-r4orYfy8XEoUkeAU2LIFf6FVYiMedThykLgyeAjC_PwStEDyG9ZgRsqS_tF-oUxU_dn6SEnwaxZZoaB0c8aUsE0t6ETv5BMB1np1pRo244ygCpshTzDRgbGjHLCb8ySye9k9Yku9WtS_NEgHZJUUtORI4zRY4Ets-aAmClStSjWrYSVQm6mrXlElQqMMaKBpA4WiJcA905d4mhJW7I-o1H1-H-eLt_k3HaiMEjsMYnAaOYjCeghXXjAUjzWDGIM8G_VsVLIQ26f2rinpolo5CUx4spoclPN0pinIMWFNLXH2B5gtwLDF63uy3NSgAn6nVYb5N8Cu3ZDamRHIyIDwFoynSTNc0MTQum7sNBHh_a-HNnww0k_mLQvKpJCsIPa3TaVuGWnXhI7Lvd9XfthtCwa2f0D2g1pDsI4d0Mvz4MxR2zsQGTGde_ZPWg7D6lbyKoOyeSljVTp4jKxy3TvCUWNQX94yS5FsncBBI1qJrEf-DC2IaEkRJ1NsFCSaMOuqobl4h2R7wW2KzEqpghqQ7yBK0WVAJaSW0aOxxQuWjrwu6a9EjIApFNTk70my4CYokQkEYrAoAagNYQTlrMNrPkpPH5yKbvdnAC3wB07kaCsNley1uD6eyLT8IS7_ERNg49_ojQmqm1DFwUjatNpNGJFFNo73df-xz757PmnX7z64sXXq3V-vezizS9IM3vu3sHcRX3zzqegYL87ekP3-AAhXv9-56Ye43up08ofXpboZMtBDgG1_uPd40NQjdf4ZLTMu13iY7teUcR2sb-Xene9gIocKXiiQLLc1sD8A8aZ6pLNM587sf3oIIqcDbJVZSGw4J1UylQB8VVo9ik9AF8anRVTXbOjKMvC_waUbpeg6AwENYzxFckvVU1CP1-TyXAKhDV4051OO2DI7mkvDQ8tyzCcJcsxVUryKAdlBvNEw6vVTfc0HXxuo5PWwec2Oj4dfG6jBdHB5zZaFR0e52PLkIPPbTTfOPjcRj-Og89ttIQ4-NxG64jD85axBcHh93ss-z_43Eb1-OHnHuvLD3--xwrr34Gf64Lkw8vvsSb38Ps91useXo6NVXSHp7Wx1O7gcxvFa4en87Gs7PCyZCw6-z10JlWadXidaSz2Ofjchpl6-P0e7c_D7_doSx6en4-VSr-DLahLPQ4_91hN8Tvoirrg4vBzj3n7B5_byLw__H6PCfkHn9tI6z68zjRmPh9-3WOC7eHpfMy7PbwcG9NXD7_uMZ_p8HrqmEN0eL_DmHtyeL42Jk0cfG4jd-LgcxtJAYdf9xhPPrxdMkZNf4e5dRj1MHO_MQIcPx9dnl_pOWR0UOb9GlMYl0GMs4motjF4KTP9lrKlpMj3peoDHY9ZjGlQS2qB0rdDjwk4ogROZ7EbxXAi_koZBKJNuUxcovafKsktvbLMaCCi-O63zxSem2URdwLQICM7CmzfdtzEDfUemNfKmFeqmFfN_DwH6uZA3Vag7u53HO3e8eP9sv8Gn9uuM3qUO4sCN07CLLJDXmRZkTluziPfLvKI86DI4jRyQr-IQscDuyNmMQvh-zAG5cwO44RTt_J969l3ZVFy7MV7rixygSXmiZfPVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxbNVxb9z7-yyA95nLpxxvxQ5yMZqYeGzH1YzqCSxUkcpSBOPG7rvthGGqGZInTP_D_NxZAlUiNFwfeEqCGnZnfeXHZ7uKzJX8cliT1UmUnkvzKimuTOU2i4YMKxiO4Gvc932QU7st0g5pHLMq2iGNmKe-27D0sz7OVf8pc7uY5uss7gVIYUwyW7YJF4wciS9hld3iKIbHk9kOssQnF70s3WlA-Hz5HPO8EichMx2U2WEpxUOwgkQMAqXM_eB9BoA_mLKIrVBBE8H9_4fCSfV9yHWFGCC0huNlyChRd58nnj8w1mSbBwbH8cPUzcfegZjQ5v4fiBfD5eJPbexY4mBbAxxzOBd8RFXzdZDB7we39ETujE4tKom-wBQH6iwDE-TwVB5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS5mvS_vuuSct9J_FtMnLHVoEvwCxZlz9JT0K7PlaRVmzXotpfgUy6rfviXceh0MPVdA9GloROmLv5owOqVasc8y2bjWgTOmjlqhFzyER-6WOXiu5ED8achzyM_fDR4f3t179_rRrpjJYADIDuBp30DucPKxTlyaRy9o4VHIa_dtT23pdm0MX-nqvP8t2Gq42xuKVQ-_TeWqIp4-qmLb2prysuopOLlRo2dSbAmvQrwU9BHeYwMR-NIcBFN7JQidYlsHth2oGtftNO7QfjG-n577bQuW1LWFnZZgNoWmnL2Vtq3ERV92v2lpRuop1MNCEo17e2mTUZ0j93I45FsxyhouxQpiIfUu7GFiaop4kUPeGBQ7AJhePeSKNNOMyAayPAY9rxhzWKjdws9VmRpK6bh6Gb-I4DmgWPbmoUqxtZ3t4odmZVM6v6gL7E0x1jxwaqB-kYy8McNAAWx34eh4njO5hXlzgsCGAU7uWpB8pAULhOyDzmxTn8ZfPUiTMnzVInD-7eMTZwj31nT8dYL7O5zbNi7hg7d4ydO8bOHWPnjrFzx9i5Y-zcMXbuGDt3jJ07xs4dY-eOsXPH2Llj7Nwxdu4YO3eMnTvGzh1j546xc8fYuWPs3DF27hg7d4ydO8bOHWPnjrFzx9i5Y-zcMXbuGDt3jJ07xs4dY-eOsXPH2Llj7Nwxdu4YO3eMnTvGzh1j546xc8fYuWPs3DF27hg7d4ydO8bOHWPnjrFzx9i5Y-zcMXbuGDt3jJ07xs4dY-eOsXPH2Llj7Nwxdu4YO3eMnTvGzh1j546xc8fYuWPs3DF27hj7j9gx1o_y3M7CsHCYO7J73Z_NzEd-hMZquqoYtGvUCXisk6CNXmsGu79vkzT1o0iO0jJz7IWHPSFQYIwF32MbPVicbNLQmB0Ll2PxLskNs4Oh-gYVp2azJHrd289Q8HOdOIXNXXRjP7KMpLZIGRdUfLlQapiwFmRC8kaowVqduUGDAVGItGISuFZCqfNvP7S1kgLCThNKQ0k8F4S4TEszFUCqar6aKhVKnST2k8j3U10BbPSmGyuAH9RUTvbrKtEn-pLqhmW5r8ifES7nS1Dxmkv0EpD3osEDhMyANkbkv5EfBfud7LZ-XBjl21I3Y0RkC8PHhBrpdgtiYeOTJs5M41Q5YXVL3b3ammEma21NldeLri5SUMj2k1unQ8gMIKVPVLcxyhRayHRpsKYBBiD_MdcbRwORiEZ3h1a94FlwMAalMayJPODcZUiUoGs0vWiDTH07RPMZkZICh6rAFk5MswPVqhMrz1T-OzJk-ETtoCiNSXU-xu2iUnSJQ65tF9C0YEaYYO58PXe-_gfqfP3ml_8PdSihCg)
