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

[//]: # (ob:ca34ef9a)
## Evidence and reproducibility boundary

[//]: # (ob:ca44f652)
The sanitized reports record aggregates, denominators, context upper bounds, tool counts, terminal receipts, and known costs. Raw APEX files, prompts, generated DOCX artifacts, grader payloads, provider credentials, and private source text remain excluded from the repository. The canonical runner and contract live in `retrieval_adapter/run_workflow_utility_private.py` and `retrieval_adapter/native_e2e_contract.py`; the concise operating decision remains in `GOVERNED_WORKFLOW_V10_DECISION.md`.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzAxNGMwMDBjODBlZThhY2JlMzM0NTVlNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjJhNDRkOTNkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mMzJjYzdlMTVkYWQ3MDc1MDQwMTI5MjYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Y1NmE1ZGIyNzA4NGMxOWQwZjBmNjE1OCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtPWtz3EZyfwXFOyU5eXeF94Ou1EWxdY4T23IknZ2UT0UOgAEJCwus8SDFs1x1PyIfkz93vyTdPQ_MLpcgRTLrSoIqlbiLxcz09PT0u2d-PmJtXxYs60_K_Oj4aLM5sR0_s207i23OY5al3PP8IODB0eIobfKrk7w8410P73bnzA3C4zBxwpjFjhtnMU8TL-e5w307zpwkjJy8KNI4Sp0w8rhrZ0WSw3OWOInrxgn3g9iGfvOyy5oL3l4dHf-MX_qTnp3BCBXrcagFfEh5BQ--421ZlCytuNXyi7Irm9o6h_eb9spKr6xv26YpNi3vOmizYdk7dsZxUluP2-ZHDtMdWuzwvO833fGzZ2dlfz6kq6xZP8vOeb0u67Oe1WexZz_bat3yn4YSPp8MHW9PsqbueA246NuB_7I4OucMkegy388BEUfiyQm_oJcAufyk8Nwsi7gT5CyP7CiwfdtxEzdEyJq2x6mdVGXNAXK1ItVJEYQsyFM3smMf0JfbhV2EThCL6UjoTjK26YYKJuwinFnT5t3R8Q8_H8nhfz6CVW7aDj-Jn3l-kgLKfzga6nd1c1kfvYU5KHrABe6HvOTdM7bh75cAUN0v-QWrnn3x8rsXr7558fnJ9y9f_csfvnr5_cl3TnjyzfM3X3734uTVi9d__OrN69Uap_8xxMX6vi3ToYc1PUlZV3YIAa-KE9YBrntO_Q39edPiDN6VNXbZXXU9X8MvNVvjUquZLKBph-RxdFwPVQXzys5hPbnASFo12Tt4OwqdyAtcHB2WsufvcdZfICXWPLe-b9p3RdVcWhdOaH3D-vKCW8-_ffFv1lf8jFUWNJJAsDwn6DZIk_wSnvzGumsvrzisWY-k1V9tcAZIMUB9R78sRjjTImWFW7hbcL7uWT90Fqtzq4RnLYwOT3BHpM1Q5wx20xSEv7Hu1MEEVF4eOV7qFo8I1RvYzBb868-5lUPDsgIMCmK1iqal54jHWuDxs4qVa-uLlm3Orc0I7Ia1bAvS2Pa90LH9R4WUWz8NrCr7K6se1ilvoReAD4BvOe5knMbTp2vOaqsd0rbMLGAum4rDCBOQZlnMPGZvUyRwPeJ0gIwz3t6yqtdenljByLV5HHnsnqN90IN9sF4AYxgE-oa67OHJ9-est8Suy-GrIHTAEDxdM4O0iOdtL5eb8cjz83uC9YaIxFteOIG14W0GfAuYF6x0y6266a0cGHjWV1e0ILAAKE0ugf8jZU0sTQDcwkmKbSL6JxI-ZQY7uWgq2ObLYWNtWM0rqxvW61s34W-sO_UwsYZFwsKEu_EjgjWu6zPAUZ2XvVjjzznfvOb8nfWdb_2hYt05PPviq6-tYOXp71PrmgSxH6bFNsPA7bzmSCdlt-5uIe5rL08gJgwyP41D-56jIcXSPibdA2b2POthv1uyL8Bmj_P9x6_dAP58CxT2ZZ3z9_T7FBK8IE4yL8vvCdZf__KfWrS8ev7FX__yXxaxHOCV-IgJ3lm0zZ95bfH3QP_lGjdAJeaxmCDwIg5cngThPSHDbQcqYQtQYCOFp3Qoqxy4Yw1qSAuwVSCXATCeDSDSFd4moHIjz3VcZxuq52dnLYjPXkiDlljLLaRzQ5MJAnJjO2eFEz9oZOCMNFcQXh9GpeCMRBaqvVXTDcCXPliv16yqlh2HX5sNrF3VNFNkFPhZ5DiZ-yDg9IbuxsH5-wz-IIwKWANM0LFPP4lXbrDZTAoxZrOCOQ-C7Ytv3yyDVWiCdgnUffpJsordzebUYikAuBfK0wnY0ty3WWxvL-q3vF32rHt3TVLXtxDVZMMp0vK563hR-AhQfBDaJDX8YL0c-s2A0vfz1yNq6Bvh0SI80vcMdKcpAosy5rDMSbdAFN0vsZFF498i3Pa8P4GVgDte4vvJvYfc2myfGZLrdUmMuWtA1COmOnj2B9Qga35pff7yM8DfFC5AjgRpmgX3Bgx5IwdoJN2DbrsGaPoW7VuhEiHXllotvUji5RJsh25qo7lhnmQs2oLrM_FpYfVNU3ULUnCzpruNP040mxKyhZuFue08GALZxirKM9jCQlkj87q9EFhhWTasB_QI5MuuRz7SN--ATw6TrAg03DApEvfB8N1IWm-a3tAKABqQdWRAwG9fo_YPgE3pulkW5Fny8CVEEgMTCXa5VPSGDvWBzaZt3pdrwBcovM7Cd_xFHHjb8C6n-CWQfpbY-aMhELHWoUKO-GlyXlHLHRWKHshfgW1NITAtksLJuf8oCOyGLAP9pBgqocOcg1YlwNlG5OlvHXdlB75_aqUcsD6FwChneRFEe3wMrM5gzQAe2FW3ab77W0xZ54HHnTCMHzLujUT_x7oDymnQK0OCZN2BqSBF0GclmdGTOnCSpXbKnYfABsvVcWITaQXvLEGlQjVTNUVrnAlCA51GG6crC9pdTSxXnnoeZwHfAu1L0LCb4ewcVt61n4ARSdsMHRIoe39_y9Ld3nrK9cNDlmdB8ljwkLIAFkNeFkWZgSxagIbea8cK-Svg564vQVtAt1VT04-oW02gjUW2a7tF-lhgvm4GMNy7Y-sHfHX5HJ2PHTA24FZv_045bVn7vrxYNe3ZM5Z2z9zQdlaO7_pTxkQYZTbPvccC841E26kbrNzkCXID4BUZB9wxre8COr_e4waawqbvxHaRbWPz-_Mra83qK6nAIOXz94wcGX_mbXMLEd7eeoqX2DEPwjR-LHgQbfiOaNUNKezTmqS8xFHBygrVANquUp5JvE2gzS6ixIt2hP0DwFxap983bZX7bnDy_Lt_ObGdU-scbJCmBsYDRknTLuumPwdsWVlb9mBqN_Ux7Rb-fgSzKkHubGHTsQPm-e5jYjNrWiS0biByQy9XVwK6rqy__uU_QQZaBei5glGv0GXwHBTRoSPPV8WnfF6xncJ4jwaqs7KePgVBklUD-ZcESE-f0m4zQELPODzB0IH0uWTVBEYTO2Mpdx9tv7zA91DzyFDhBECBIZ43Q5WjUgViJeew2OuyBjjkhh6k67ifcu7mYNswL9j2SH2DalhesrO6od5In4BBkLJAnlWsPcMdUN6yv-_aTS520_R-554bhX4aPDqgRKpD2wI3t6TAlpEq2FSwMMAlR76peEELi7FlUV9DrJOmYZT46aPDC5by2IHSWv91ACZPetCf6g_Wcrm05P_49Q0Q2xLmBcwsn1KBeOiGgeMXjw7yq0GGIYqyBVkkxXeBzBXJfgnrfaH3BLpQiMfWRMVTpiZwLF4k26GCFxdlzlFhQ_265aAh50NWpiVFRe4YhbprHxPkmjHfL8LAfVzYyB5gNai8f6YgFKq7nQpGaSoF4wKGaYAZMAyuLoRltYvItwsVhT26EK71k6zlTAQ16RcVIeUnLC5s1898Hno5aAGxA0KN-ylSCtAB9SkDxZYMFIOdwrN3m6YkzzOMSCNh3FN9w7DnW4wwV2V2ZfRgRp2NTiiefc-AdNcU_Qlo4WcYUStl3LtLneOcpylYQhmPWZzauVvYSZY4wBLzMMgKxrKc2VFYOCFz8yhIHCdltud6XsiT0M9s9JWh3U_xa7Fax370CyAaA8WgfIZLO1569hsnhufHQfiJbR_byGslxoWWmnGf-UA949Off72QNxGwCEmDXnGObMEt3Cwo_IBFiEzqw4hSS9p-pPCyHDP24yAIQS32bU-NaUSc1Zj3DxjLcbwizllgs9B1fDWOEUOW4zwkBCxSOxCgLZURXeq1NZLIyvqy1xs6cq2mwP871KFyUt7B7nDgcVuewbauTHwS31wAEC3n2okyxkeEp6G_bGSEAzjCynrBsnMLSImjuw9YhyQQnBRHMSF7IzNWSEXA8Rkr607YZRoOwzm8sp6jN3d0ay4Ei6_55RL9mQIQVFTRm7gULk5sbjKrET8LEQBFAQFLm0kFDfojbKz2yAW5pgULI2ACGfdI-tKaGtF2vab3D5bXT58utCo2RrjoXaUa4Apur5bqRajlDBh5X3ZFie0zsDs6iXOBbaIHqTZT629Z1_0D6KrPrVMbjDqy53BAMbRQXEDAkpePcDZ2vzPwp1YJEr3honMCGrtoh7pGZwVRtzBypKuCIkMdkRb5nmAZyxy1IaEqL6ifil1e8XbJ8nXZI07WDP60Fqa-UHhcrH6Nyw-Y6clTIjzPQFmUQgMyDXGPYUGi65ZXJbpeJpaauVmeMSdnSRyopTbSFUY2cZcMBNlnHvhu6IfMZlGu2d2YlCD7fEieAehQNDnBA3Y1tl3t7cJx4Ku59-WG_-fXL79ZkoracphH27GKXGKYQIBhzFdeaF1EhHbsg1aR3hfuFVhDWjgh9NG0ISe_5GF5kw1rcnB8sP7YcfQ-ZhQeGAR1GxohdvkpdVUbvP6F-0LB767kDMa4P6l6UiXFyPCaGJRQDHQ0hDwsZQZsBNSGJcEvqAhlLu1H6f3Dl18q7LAUeM8AMyLmKVzOSN-XbQNGsRhiK6ZFsgOsqWEDK0phxvQKkzUU-B4Ga9ia0wxEEHtnIrjCtANzaWmjEQaDianDHr3EvUnsDK0J0Ma7Dc_KAgYX20aBgsvXYiYIRs-BJ2xQdFyoqQhR05CLUfDrTuCdUcxIsXfcyXKz9QgzsHC-4fBf3Y9xuU7Nzjdntzutr1C7R8YIaGYyUid6Btb-HqfbNNUS3eHAFTZmOgZY-m1zIfgAMp0KaQQTM7D566aCxa8ADgswA2tUAydoKnxdQhVMQfUcNS2rZZfLTopWynh49fwL0bugjg2ICwpbL6um2RD3apsK2-PwBbsg0QqNEIe4cVH7YtUoOa1LtTtRtn-4Ln4FHmlZJeU3ItSJzKWbiq0vzBCyCq1vZEwAmeoSoV925HE0dQgMEaIJpaSkGthxBUkLHUMJMtSRkdtizM76sM_0kzwvCbI4Dgs_iwvNR42MJ0Nk3jeJSTi5yVcBeKxZ24J-uLOyxAeIoV1jBoiY3a2jtA5cHei328cjYTuW7fhUNFEqEf0ms2fzfUs4IXmCIszBzIgK17EVxoxsLC157p9MJQdyiqjgbmC7UaQ1VCO_6po4-vj0KJXVgNtiWxgd7_5RDLGp8pE7t4r3fbDCeBXYT-BDFK58Bz_E9irxnowtkZVbkpWbDaOVG1FDf-WJhsEqiYyGgufvNopiahSvfBo2Tlb2OJpvbH8JLb7jr2waKnZWXkIfXAGsYj17OQtNzvdoOBiXPiSuAFY13OU8tKuxgbPyYzm7UHSRrOLwyeSeBNPMid3Aj3mm9RAjW23Ube6SgKb0JcdhLAdLPmKZ6tPISdPEdP80M9yyGIcj7aYfbY5b1Rwzgww7R0V2O4UGGJnWLgVDVfonKFPCJbpQ7gexw7nyt6QqAvfB-qaR_-GgexKcNirvacxVod9pUUFVyoXKJQDoWyalBpk2GwQCvpwCNzxRzU-tMxCNHShoGWLtJba-RO-WUBUkelCGdttvKiCFOUnjS4FgYMvAD70BvKVvhN11VjUpq5a0TETSojGZeBtS7P6dK4xM0GHEvdSOi7SwC0ebyGPCoKSZh-YAkkr69OnZTRLz6VNlgK9RFQIzPys7bghrTLY3jSYgRvRhiQXB6SuNVusJphWEcgkRNWVrhI7r2U7GWcA0Ix7TEw0Zed-MQ9hCDeqWQ4t20pIiA8JC_mkAfAGol-dgnBmKOOiYiJKhJi33vARzHmiHZE3agu10_qnFy7PzXkQZdDfp1QYLGBAFK1x-6WaQAEvhgaMAwnKpco4wSqsNJTrgGhPgYL41TggXD7mOsAh7NCwI45IxHG-7DmRmCGqrYN-jBz63Tn9rr2zbc5zIi_1T3PLbKRhacmsVeImFJry9IH3bxR0q3aA4B92vcleL_oPEC4PQPUVruhh63DzS-pUhlYr9uYRtSqtmSRPrJ3Sxk9-nByReaBRPqgl-XrguqKtRmGnpbWSPjkz87qmgSmXjOegatuuxhOuex-xQzcrvn-qJnHAf7zFeVeT9zEzso8Cyod-ijSD52y3qxXVlY5_-4virxEUh6norJyQ5vEpIkLuuVAjslRNJsWIqN5YTrHyS_SI2jh_sVUAfQLqTvmF5QCCTDDGw48iLEp55o4PASH2VmH9IHuup9H0x2v3LDSMFNQmeWGnT9JijtxHeTqRC2COnP3xigyaysD5xIpjF21Mp_tRw2bVVpMEcwF-MaavQ3lnFAbR3I9Ck3sLGuL7wuNGBU4PafhP0S1gYT_S3TFaRu7CWzsr2obubN0iS-onnu1kehMXowdG5uioP5wGJtz8s3ZWNuHEdWOq3p4Sa00_8VeSMLa9jCNqBmpcgTsNV4Lw9_RSQD2ui8N5ZwmmHvjaUO90ew41sXOKKe0ETUwhWjiORBnpohAOClhjjIqAw0ZbxKOq68gz5Z9lp9UEbRYLzamN2AvGpH4dR5id5wrU4MxKRR870sfnESn0tItsPkwSUS92_kWKs-dP9M4XXn4wsqanMBvh1qwU-2G6yRxs9vjNXGlMwfswKSsH4IJxn5NMGXuKuklBZCsSQgmAV0JMwXIXK-hA2gXpyreOl7WHHOh0YmBWYV9Q4iFaO_0TwQsHHUKzhX98VhoX-sN0tIPrEdne6VW0dBZt6oP568So2R9nTp78LaiDbRsFOZ_qXYPfJnm6DnW4dVxqY-oMG_tov6sOebqMbMLD7F9AbkzXqOLBLb8SASsT5oBO6b-7yhr_bHb56KVfp4_vzvJXnXeuQrd89LoTUof-IHf7YFh8NoZrrBF3u9BhcI2n9RO9M3at6MqELFDboYEkYeKGjDWqjSsFwA92t7EDZGoWPuQ2eI-IYQsUYKxH2KXcfWVogn76U0bjx6d1Y45ZupgxmyWxDydg8d-VuccHr-thWO73HPGf00FBXEwvA09ANiiJleaz1B6M0wrDK7lvrIExTjFsRejJWo4gFWwBAKTsVRa1kM96SWYNhK1wSYwnQS0oBZIp1glUkEwrBoM2nYlyh6_q5nzMnd0YNaSyyGAX1x1VLKPeinfl-FDlpmEXaIzQWUGznrt-rEkLVHsg4IYYFSjCFl2lZYRi9rMndim_L1MrdBJfRSlcRSKwPoACo6kz08kz5bmnoDAYFrQw2x0ZpMHlTVazFPMkmIwNxAdre7s-dtR66nsZLOXRccLIgRZCKwpYSCxNrloepkxYRy-yUGzFEVfZx2_69Q_1Gq3SmNzdZV3fbuVM2oRtHiyhOyNJaJLGLjHb_1r9uOIbBAixs5K8LP8QYk3ut5T7bEocM0XajIcN4HHKbcdwP7D3M5zrkThIv_CghfWgR-DYypHBf-7vDP8G_4iSPgyjK8jDScQSj_sbgX_ctpBGEg4HpTiUaINONXJlIQbaLF9jEhxQpoZLfljgIvKedlDJhRHhaXSfcyg8RDAfW3DDScvTSkTOJUQaL68toqP6lEwj0YuEm0I8nNlfkx26U5jZPuWaIRknQzua6T20PBRkzYiDoVsIUt7u4LsQ7rxoMPoOYYO0VPBcOrTCKkA7_-pf_QLFG4vg9sMqW3qU0FDDe2JjBKbOmtn-5wDD6b8G2cH3fdmxX9R4A7cRE5wm-8cWY1qMWJ7eceKczWnwx2L9uj7LrRMNRxqE813NDQdbWKy7ocIxGS9encneKko0WwKkNfNOgfxDkLOYUg70Uhw7tF9MDiHsvsG-aU-SqTWFMRvU7OQvh_9uZBRZIyFA9G7OetoMTeXOJegNna0oN5zgOder4ceIlkV5jXypXJWgABPdY7yMCCB1HV6t1jjznliE8Bbzo2qa4npnt3WLnmJJDE53SlrLMi10epazIx7Q6Xaxm-rDvWXW23zFrOo-lU1W7iptWdhKG9il6bKsBlRTyTZOHuSdpyN_jD7AgnLVVCbSlItFjMEGsm0hgkkcwkSscM5HWm37ST-s7dl4kLCpSnTNmVMmNStada96UJuDHvh-wwouYN0ZPdBncbZrAHYraagsUFMyc0z88F-lU_dXuL4-sH9irkMTkiraoDVbTXbUDe0Xs0FYtMcXpDtoBNIv1-_DHdT9WNxCOYYQ1kWbjR2gGurFtTzTeD7gnIA5C0TKeVgry3E6jNCn8UG9Toz5x3Kb3rjbUORv_NICxYj3HPX0hw5h5I5KKVFLeNY40FSRLOYtDMH7z0etnlC-O--heBYjKAR-EGct8DwR-ojfrWJOoDnd4QFUhVsyxC2AklMOyGQDBmcxqAYYucDgGsv6Z1QMKe8zmta7VBkorBiWMKMVD8kRhIzI60X_v-ivAgVTO_NgWFqMYpUI9oOK4tGnD2pyqvboSGZDOsRIpWZcgU3A90KYlK-G1yBpDw0Vnj3Y0nk47XoiQHGIIE7w-a1qAFc23r0Remjmwyk42yf1r9h7YqxV6K_-JOShC5MFLT9Qs5eSc0JbZncYUFUJM1N1x4CBcRebAUyw-jb0YzwJkrubERomoOoHrAUWe7u8W282MSYyNLy8vV2veArR0tB9m9Rup_d3SaPTsd0Kp_mFqXe7Xc6Z6XKrEXXzn2e9lKPfvL4_7v8Eg8d_jf0vndxOIdQMv9WMeuJzp7WgUtW4lj92vLFUa6mWv4rMpl7tRxCAzvsEEFUyswLDZSA7C5UAP1Q4QGQJjVqKMafVGFZigZkVtglwNErNUOYBIvdyhVKrp6anqUsTTMRKDqWm9mePG0bdUgfZDiWvQSYOKipHoJ9dhIbNTSYlUGeJmfcH1fH-xpzCTRCRMtFItsyRoRuruQk5BRL_ID6ZmDdYirwqRGdCpcClltUtWgXQ-5QGxwyQo3DQJYlfvtrGEeBQE9yoC1lvaBRXNy8H4C7WcHOuCDcq7b2UvZv9oTRhTWJFPCTeTzF1VlEQOK0pTFAluqKrSC6Sar6zXnLjcToYieiJFqBbzM8DkXpcImeGUVEQp1gj4Ta8KDFQCt9SzKYVbKjv8-OaVyYqw4FGYJ06hPQ5GlbJE2kPqjEXaCvDnNVrQqN3HCz8OZUBTaGVYSQILqoHPqYS14HVXpiLFRdXjakyIjmWnGDsdDOU45RkbyDdXIUwdlQWBxMdDO7EcjhKGpM_vjGwZ2GHQH2_FFnu9VBxROgywqmgnORnhZ8Q-zgENwL3OtDEgdAtkUGLDUAWGWTCT8jo7X7P23d92ZLFkpNGP1byrP9XLPeEVdbarmnxdD0Q675GsBt6RxgQizF3g_56YC3zyTVyrclaEowTiBgIEHC_JVj9vyFCnej-RW9-sOdXbwB8y6sXUJKNQacdIW1vwSwtRVUMJRqUnSiZct2-OjjFHLB2C1XuHxKBNGGHSZb3WaxeGjTiSxRtQT0HHv8JMfAVSO2AN0vd4kC-QFZWTrtEPdgWmKej1LfSu6ASGF6mCC9jQMC6rlpIGBnjYote5vxLK0rrsoLOzpTxoV_jBfxpEY2IAhPD1mlMCI_xclKDcSrriG3NlpEO7G4MIleD_z1TvxvB6HWhH6KXQqFoSmmgddjCtYmsa04w2WIvNERWwhShPDvE97rwF5Z-8h4nmGLJq1EKbL8hkrLqpJQb7JXTDaxMreyeMJyqro3WtnPVM1MSWYKZWrD4b0GGH861Y9q4zt7-erfBrdlc1OuVlbqBk6ILudulNRX4NLNSwHZbAIDHe02Fx2bKsgftS1tpSbgLhaBFzZ4CkKxrsSnMZqrdtNdXBF8P1wEGMkzGGswNUF2WvS_WusGYH1fEzVI2XMi_TIhbUKVICJMEyL2veo6LRYVzljKNUN7EK8wUDpewpT03tdRXU4ii90Dz5UszndXbOc9oZ1KEcSO830iaI8SGpyWQ3itMIcWQWAaWsz85Xew5BUO4mJ3e47YdpwnRwyThpwpDPDzkrAtUzUyWqwW7vRJooYKHWMtMUKnWTS-Zp8LDlNirMsnTSG0XHoKwxUJhFeAqlVy3cMBMi13NY7LusSJxE48E4xkLi4SEHUQzCaf6n2sVO3hB31tnPrG90P6YQRcEoysWNao4FFl70JX6gmIGsuBKeDIqbYQHpn2oPBxo9TYRQOYbcFhaBrbmxiE3-OMAez8tMSGJeFLLCCQGRIUvl1kLfLgzk40CfY6mYeGyOhK9A_yQTUCWDHoCG1hu5ESlXa81B4e25FJhijBZ5B-5gFBE4m4DQRhU0WgfHQWgbYa7sGnEv2H9droc1qIWkCWvVDHtGPC80AZVqtFwD32kBOeaTUnGO1M0n9pLD_TRxQ9dPUh31MM4YUScMPOCUELCqt1PVhJAXmF1ZL7b5r_WTPHJCj6B4Bc0ZM-4Vw8C6K9LKdOOFZC6wwYmrjntUlsQInK6sr4WwNTVjPdoaFQ5Wa-5HNg8Rq3gDoDnD6rWt3HeduyusIq5iRJ8av-mNQ4FgOdBOTj-GhirtcMFjQmRpwoRNZPu-W9i2Gwa-jgob56-MNtGjHJyinGVenuVuwvLY1h454ywVkwff8xAUES3RqvCSnM4y_K7sdpk1kYvCyAHzJijPXeVAkJuyO0Y6QBBUsF1VCkk-qzUgZeaAAa0_6h8Heg4gDOppy38Uemh6ZVRLCwlaI663Q2OSfliOAphyDZSFg9ZeW74X6blgBiLtNZ3SRM9LYOjaedE3WxUeE-IhdXjIisiGnaw9U8bxMTpG8JBzX5TWQ_n42BWpI8ApMeQKf2EWImMedbiyEHgy-MjC3LxS9ADyW1bggsrSfpF-YYzU_V56yEkwa5aZYWD084ZUMM1taMcvJNNBVro1JNq2owygClshz_AgA2NEOeC3Zsnk97L6RJf6NSn-aJAOSSqp6cgexuixwJZZc0DMFKlaFOtWwkohN9PWOKJKBfoY0UBSBwvES4B7py5xtKQtWZ_RqHr830-Xb3JuO1EYJPaYRGAc5iMJ6CGn8ICleKwZxBjg36pjpZCHXD61cM9ME9HIS2LEldHkppqlMU9Bigtpao-xPcBuBYYvWt2X56QAE_Q7R22Qfwvs2g2pkR31iAwAa8l0kjTPDU0Ipe_CQh8d2vuyZ8MPJ_1g0r6oSArBCmp321Tilp16Sey43Pd17YdxZNHI7h9w3JDmIIxzN_TyPBhzxMYTiMy47j1PD9rOQ-oWsqpDMnlpI1W6uEysMt17QlFj0B9esUuR7F0AQaOaSewHPozHkFASos4mWChJtGFXVcNy0Ubke4HtSoyKKYLaEG_gSlElgKXklpHjMYWLpg78rmmvhAwA6dTUZK_JMiCmKBFJhCIwqAFoDeGE5WwDc34Gr59cytNuToBb4IqdSFBWmytZa3C9ncg0POEuP1HD4OufKo2JatvQRcGI2nQajZgRhfZO9x3_Y598_uKzL19_-fKb1Tq_Xnbx9hekmT1372Duor555zNQsN8fvaV7fIAQrz_fuanHeC51WvnDqxKdbDnIIaDW_333-BBU4zU-GU3zbpf42K5XFLFd7D9LvbteQEWOFNxRIFluO8D8I_qZOiWbZz53YvvRQRQ5G2SrykJgwTuplKkC4qvQ7FN6ADYanRVTp2ZHUZaF_wMo3S5B0RkIqhvjEckvVU1CP1-TybALhDV4051OO2DI09NeGR5almE4S5ZjqpTkUQ7KDOaJA69WN93TdPCxjZO0Dj62ceLTwcc2jiA6-NjGUUWHx_l4ZMjBxzYO3zj42MZ5HAcf2zgS4uBjG0dHHJ63jEcQHH69x7L_g49tVI8ffuyxvvzw-3ussP4V-LkuSD68_B5rcg-_3mO97uHl2FhFd3haG0vtDj62Ubx2eDofy8oOL0vGorNfQ2dSpVmH15nGYp-Dj22YqYdf79H-PPx6j7bk4fn5WKn0K9iCutTj8GOP1RS_gq6oCy4OP_aYt3_wsY3M-8Ov95iQf_CxjbTuw-tMY-bz4ec9Jtgens7HvNvDy7ExffXw8x7zmQ6vp445RIf3O4y5J4fna2PSxMHHNnInDj62kRRw-HmP8eTD2yVj1PRXGFuHUQ8z9lsjwPHz0eX5lR5DRgdl3q8xhHEZxDiaiGobnZcy028pj5QU-b5UfaDjMYsxDWpJR6D07dBjAo4ogdNZ7EYxnIi_UgaBOKZcJi7R8Z8qyS29ssxoIKL47rfPFJ6bZRF3AtAgIzsKbN923MQN9RqY18qYV6qYV838PAfq5kDdVqDu7ncc7d7x4_2y_waf264zepQ7iwI3TsIsskNeZFmROW7OI98u8ojzoMjiNHJCv4hCxwO7I2YxC-F5GINyZodxwum08n3z2XdlUXLsxXuuLHKBJeaJl89XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFs1XFv3fv7LID3mcunHG_FDnIxmph4bMfVjOoJLFSRylIE48butzsY00QjNF6J75f5qLIUukgxQF3xOihpya3Xlz2e3hsiZ_Hack1lBlJpH_yohqkjtPoeGCCcciuhv0Ot9lFezIdoOYRy7LtIpiZCvute8-Ls2wl9_kL3dyHd1kncGuDCmGS3bBIvGCkSXtM7q8RRDZ8nog11mE4vakm60pHzafI993gkXkJmKwmywl2Kl2EEiAgFW4nr0PoNEG8hdRFKsBIng_vvH9SL6vuA-xogQnkNxsuAQLL_Lk-8bnG8ySYOHY_th7mLj70DMaHd7C8QP5frxI7L2THU0KYGOOZwLviIu-brIYPOD3_oic0InFpVE32QOA_ESBY3yeCoLM16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16TN16T9f70m7e0v_w1lKWP0)
