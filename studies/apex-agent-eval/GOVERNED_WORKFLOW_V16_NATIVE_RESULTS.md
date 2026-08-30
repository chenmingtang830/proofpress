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

[//]: # (ob:969474b4)
That diagnostic is now complete. The [v17 zero-heavy results](GOVERNED_WORKFLOW_V17_ZERO_HEAVY_RESULTS.md) show that uncapped governed discovery did not improve this frozen subset: small-seed scored 8.89%, governed open discovery 1.48%, and raw-corpus access 5.43%. Criterion attribution places the dominant failures in requirement coverage and graph sufficiency, so the next construction step is a requirement compiler that binds each atomic task requirement to an evidence atom, controlling authority, or deterministic derivation before retrieval and execution.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzAxNGMwMDBjODBlZThhY2JlMzM0NTVlNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImYwNmRjYjE0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9jMjRjOTU1NGVlMzQwZjM3ZjAwOGVkZmUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2Y1NmE1ZGIyNzA4NGMxOWQwZjBmNjE1OCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfXtz20aW71dBaSZ3dxySxvuh1NZc38STyW4SZ21PcvdmXFIDaEiISYABQMlKnKp8iPvn7JebT7LnnH6gSVGQLGmZmq2uSsUUCfTjdPd5n1__fMS6oa5YMZzU5dHx0Xp94nph4bpukbqcp6zIeRCEUcSjo9lR3pZXJ2V9xvsBnu3PmR_Fx15c5UnoZ5Fb-lWW5VEURJ6bRSW8xrLSc6uwKllR5Hma-jyueJK7LI144pZxkIcetFvWfdFe8O7q6Phn_GM4GdgZ9LBkA3Y1gw85X8IX3_KurmqWL7nT8Yu6r9vGOYfn2-7Kya-cb7q2rdYd73t4Z82Kt-yM46S2vu7aHzhMd9Nhg-fDsO6Pnz49q4fzTb4o2tXT4pw3q7o5G1hzlgbu0623O_7jpobPJ5uedydF2_S8AVoM3Yb_Mjs65wyJWLlxWeReeCS-OeEX9BAQl58UflhkURRyHoRuFSSV66a8rDiOrO0GnNrJsm44jFytyPKkimIWlbmfuGlYeFnpVm4Ve1EqpiNHd1Kwdb9ZwoR9HGfRdmV_dPz9z0ey-5-PYJXbrsdP4mdenuRA8u-PNs3bpr1sjt7AHNR-wAUeNmXN-6dszd_NYUDNMOcXbPn08xffPn_59fPPTr578fLf_vTli-9OvvXik6-fvf7i2-cnL5-_-suXr18tVuXR7IM2FxuGrs43A6zpSc76uscR8GV1wnqg9cCpvc1w3nY4g7d1g032V_3AV_BLw1a41GomM3i1x-1xdNxslkuYV3EO68kFRfJlW7yFp5PYS4LIx95hKQf-Dmf9Oe7EhpfOd233tlq2l86FFztfs6G-4M6zb57_X-dLfsaWDrwkB8HKkka3xj3JL-Gb3zl3beUlhzUbcGsNV2ucAe4Y2H1Hv8zGceZVziq_8rfG-Wpgw6Z3WFM6NXzXQe_wDZ6IvN00JYPTNDXC3zl3amBiVEGZeEHuV484qtdwmB34bzjnTgkv1kugoNisTtV29D3SsRF0_HTJ6pXzecfW5856HOyadWxrpKkbBrHnho86Uu78uGHLerhyms0q5x20AuODwXccTzJO48mTFWeN023yri4cYC7rJYceJkZaFCkLmLu9I4HrEacDYpzx7pZVvfbwxAomvsvTJGD37O297uy98xwYw0aQb9PUA3zz3TkbHHHqSvhTbHSgEHy7YsbWIp63vVx-wZMgLO85rNe0SYL5hRc5a94VwLeAecFKd9xp2sEpgYEXw_KKFgQWAKXJJfB_3FkTSxMBt_CyansT_ZmET13ASa7aJRzz-WbtrFnDl06_Wa1uPYS_c-7UwsQaVhmLM-6njziscV2fAo2ash7EGn_G-foV52-db0PnT0vWn8N3n3_5lRMtAv331LpmURrGebXNMPA4rzjuk7pf9bds7msPTxAmjoowT2P3nr3hjqVzTLoHzOxZMcB5d2RbQM0B5_t_vvIj-Ocb2GFfNCV_R79PESGI0qwIivKew_r7r3_TouXls8___ut_OsRygFfiV0zwzqprf-KNw9_B_q9XeACWYh6ziQ1epZHPsyi-58jw2IFK2MEo8CVFp3xTL0vgjg2oIR2MbQlyGQbGiw2IdEW3iVH5SeB7vrc9qmdnZx2Iz0FIg45Yyy1b54ZXJjaQn7olq7z0QT0DZ6S5gvB6PyoFZySyUO1dtv0G-NJ759WKLZfznsOv7RrWbtm2U9soCovE8wr_QYPTB7ofO-fvCvgHx6gGawwTdOzTj9OFH63Xk0KMuaxi3oPG9vk3r-fRIjaHdgm7-_TjbJH66_Wpw3IY4N5Rnk6MLS9DsD7c7UX9hnfzgfVvr0nq5pZNNfni1NYKue8FSfwIo3gvtEl68b3zYjOsNyh9P3s1kob-Ijo6REf6uwDdaWqDJQXzWOHlW0MUzc_xJYf6v0W47Xl-gioR94IsDLN7d7l12D41JNermhhz34KoR0r18N2fUINs-KXz2YtPgX5TtAA5EuV5Ed17YMgbOYxG7nvQbVcwmqFD-1aoRMi1pVZLD5J4uQTboZ86aH5cZgVLtsb1qfg0c4a2XfYzUnCLtr-NP068NiVkK7-IS9d78AjkO05Vn8ERFsoamdfdhaAKK4rNaoMegXLeD8hHhvYt8MnNJCsCDTfOqsx_8Phu3Fqv28HQCmA0IOvIgIDfvkLtf80ndd2iiMoie_gS4hYDEwlOuVT0Nj3qA-t1176rV0AvUHi9WeiFszQKtsc7n-KXsPWLzC0fjYBItR4VcqRPW_IlvbmjQtEX8ldgW1MEzKus8koePgoB-01RgH5SbZZChzkHrUoMZ5uQp7_3_IUbheGpk3Og-hQBk5KVVZTs8TGwpoA1g_HAqbpN893_xpR1HgXci-P0If3euOn_0vSwc1r0ypAgWfVgKkgR9GlNZvSkDpwVuZtz7yFjg-XqObGJfAnPzEGlQjVTvYrWOBMbDXQabZwuHHjvamK5yjwIOIv41tC-AA273Zydw8r77kdgRNIxQ4cEyt4_3rJ0t7895frhMSuLKHus8ZCyABZDWVdVXYAsmoGGPmjHCvkr4Od-qEFbQLdV29CPqFtNkI0lru_6Vf5Yw3zVbsBw74-d7_HR-TN0PvbA2IBbvfln5bRl3bv6YtF2Z09Z3j_1Y9dbeKEfThkTcVK4vAwea5ivJdlO_WjhZx8hNwBeUXCgHdP6LpDzqz1uoClqhl7qVsU2Nb87v3JWrLmSCgzufP6OkSPjJ961t2zC29-e4iVuyqM4Tx9rPEg2fEa81W9yOKcNSXlJo4rVS1QD6LhKeSbpNkE2t0qyINkR9g8Y5tw5_a7tlmXoRyfPvv23E9c7dc7BBmkbYDxglLTdvGmHc6CWU3T1AKZ22xzTaeHvxmEua5A7W9T03IgFof-Y1CzaDjdav6Hthl6uvgZyXTl___VvIAOdCvRcwagX6DJ4BoropifP15JP-bxSN4f-Hm2o3sJ58gQESbHckH9JDOnJEzptxpDQMw7fYOhA-lyK5QRFM7dgOfcf7bw8x-dQ8yhQ4YSBAkM8bzfLEpUqECslh8Ve1Q2MQx7ojXQdD1PO3RJsGxZE2x6pr1ENK2t21rTUGukT0AnuLJBnS9ad4Qmobznfd22mFKdp-rzzwE_iMI8efaC0VTddB9zckQJbRqrgUMHCAJcc-abiBR0sxpZFfY2wXp7HSRbmjz5esJTHBpTW-u8bYPKkB_21ee_M53NH_h__fA2bbQ7zAmZWTqlAPPbjyAurRx_yy40MQ1R1B7JIiu8KmStu-zms94U-E-hCIR7b0C6eMjWBY_Eq2w4VPL-oS44KG-rXHQcNudwUdV5TVOSOUai7tjGxXQsWhlUc-Y87NrIHWAMq708UhEJ1t1fBKL1LwbiAblpgBgyDqzNhWe0S8s1MRWGPLoRr_aToOBNBTfpFRUj5CUsr1w-LkMdBCVpA6oFQ42GOOwX2AbUpA8WODBSDncKLt-u2Js8z9Eg9YdxT_YVhzzcYYV7WxZXRghl1NhqhePY9A9J9Ww0noIWfYUStlnHvPveOS57nYAkVPGVpjrkCblZkHrDEMo6KirGiZG4SV17M_DKJMs_LmRv4QRDzLA4LF31laPdT_Fqs1nGY_AKExkAxKJ_x3E3ngfvaS-H74yj-2HWPXeS1kuJCSy14yELYPeO3P_92IW_awCIkDXrFObIFv_KLqAojliAxqQ0jSi339iOFl2WfaZhGUQxqcegGqk8j4qz6vH_AWPYTVGnJIpfFPqVGUD9GDFn285AQsEjtwAFtqYzoUm-ccYssnC8GfaAT32kr_H-POlRJyjvYHR583dVncKyXJj2Jb85gEB3n2okyxkeEp2G4bGWEAzjCwnnOinMHthJHdx-wDrlBcFIcxYRsjcxYIRWBxmesbnphl-lxGM7hhfMMvbmjW3MmWHzDL-fozxQDQUUVvYlz4eLE101mNdJnJgKgKCBgaQupoEF7RI3FHrkg17RicQJMoOABSV9aUyPartf0_sHy5smTmVbFxggXPatUA1zB7dVSrQi1nAEjH-q-qvH9AuyOXtJcUJv2g1Sb6e1vWN__b9BVnzmnLhh1ZM9hh6JrobiAgCUvH9FsbH6n40-cGiR6y0XjNGhsots0DToraHcLI0e6Kigy1NPWIt8TLGNdojYkVOUZtbNkl1e8m7NyVQ9IkxWDfzoHU18oPC5Wv8HlB8oM5CkRnmfYWZRCAzINaY9hQdrXHV_W6HqZWGrmF2XBvJJlaaSW2khXGNnEXTIQZJtlFPpxGDOXJaVmd2NSgmzzIXkGoEPR5AQP2NXYdrW3C8-DP82zLw_8v7568fWcVNSOwzy6ni3JJYYJBBjGfBnEzkVCZMc2aBXpeeFegTWkhRNCH00bcvJLHla2xWZFDo73zl96jt7HgsIDG7G7DY0Qm_yEmmoMXv_cf67G7y_kDMa4P6l6UiXFyPCKGJRQDHQ0hDwsdQFsBNSGOY1f7CKUuXQepfcPH36hqMNy4D0bmBExT-Fyxv192bVgFIsutmJaJDvAmtqsYUUpzJhfYbKGGn6AwRq24jQDEcTemQiuMJ3AUlraaIRBZ2LqcEYv8WwSO0NrArTxfs2LuoLOxbFRQ8Hl6zATBKPnwBPWKDou1FSEqGnJxSj4dS_ozihmpNg7nmR52AYcM7Bwvubwv2YY43K9ml1ozm53Wl-ido-MEcjMZKROtAys_R1Ot22Xc3SHA1dYm-kYYOl37YXgA8h0lrhHMDEDX3_VLmHxlzAOBygDa9QAJ2iX-LgcVTQ1qmeoaTkdu5z3UrRSxsPLZ5-L1sXuWIO4oLD1fNm2a-JeXbvE97H7il2QaIWXkIZ4cFH7YstRcjqX6nSibH9_XfwKOtKyyp3filAnMpd-KrY-M0PIKrS-ljEBZKpzHP28J4-jqUNgiBBNKCUlVceeL7a00DGUIEMdGbktxuyc9_tMP8nzsqhI07gKi7TSfNTIeDJE5n2TmISTm3wVQMeGdR3ohzsrS3yAGNo1ZoCE2T06SuvA1YF2-308Eo5j3Y3fileUSkS_yezZct8STkieqIpLMDOSyvdcRTEjG0tLnvsnU8mOvCqpuB-5fpJoDdXIr7omjj48PUplNeCx2BZGx7v_KIbYLsuRO3eK97134nQRuR_BhyRehB5-SN1FFnw0voms3JGs3HwxWfgJvRguAvFitMgS40XB83dfSlJ6KV2E1G2aLdyxt9A4_nK0-Ey4cKmr1FsEGX3wxWAV69nLWWhyYUDdQb_0IfPFYNWLu5yHTjW-4C3CVM4uFk1kizT-aPJMgmnmpX4UprzQeoiRrTbqNndJQFP6kucxVoIln7BCtWnkpOnNdP80MzyyGIcj7WYYbY5b1RwzgwwbR0V2O4UGGJnWLgVDVfonKFPCJTpT7gdxwrnyt-QqAvfe-bqV_8NO9yQ4rVXe05irQr_TooKqVAqVSwxg6JiUGmTarHEQ8McpcMMT9fqpcwaisQcFrUCqvcC3L9G7JVQFSR6Uof32k2qQwpyk_qVAMKhl0IeeAN4ytMLuOlu2OVvOaZloS4uXycRbk2L3H1xRZGIfJjzI3bTKK7fytIk8JgzKPfPQHEBSSZ88ObtJYj55ogzwFapCYOYXdc8NYY3J9qbRBJsRfVhiQXD6SqPVeoJpBaFcQkJN2Rqx5weuV3AWMc2Ix_REQ0beN-MQjlCLuuWmQztpTpEBYSH_uAF6wVAvz8E4MxRx0DGRJJuGtNzzGsx52Dska_IObKfzTxxen50PIsqgm8mv1ljAgCRY4PJLN4McsBQe2AsQrJQq5zhGabWhRAdaYwIczLfBCeHiIdcRFuGAhgVRXDKG423XgcwMQW0V7Hv0wJfO6e_dhesGnpcEaXiKR347BUNLbq0Cz7HQhHcXpG_7eEKlGxTnoNtV7mrRfpQFcRT7p2hNV5sBD4-0fmVIZcl-quGY0qo50sT6EV3s5PcZgIgXmsSTakJYVr4P6moSF1p6G9mjIxO_eyqoUtl4CbqG6wcs47rlMTtUs_L7p3oiJ9zHe4xH1fZ-aib2UWDZ0G_RRpD87Rb14rqysU9_8cJF5qMQ9YOFF5McXmQkyH1fKgTuwkukWDGVG8eLFiHJfhEbxw_uIqIPIN1J33AC2CCTDDFy0yRIMl4Eo4PASH2VlH9IHuup9H0xOv3zNSMFNYs-cvK2HTBHby28nbgL4Yycfv-xC5rIzPnYS2AWb06l-FPdFddWkTrzgH4ppq3C-94ijeB9PwFN6g0cjOsLjwcdODWo7TeNfg4LE4j25tki8WfO3Fu4ITR38wHJ8jALQr8oo7gaPTg6V1fl4Twg8fb7ub9wkTa-B0v95pRIc_pxuEi88c3rFIL3QM3LkKbxIvLenH4CxIc1UXTvHeG0Q18byp1-j-FGNi5xxb1DE1OIFp4niQZ6aIIdgpaY4iKgMNGW8Sjq-voM-Wfda_VBG0WC82pjdoLweZjGSRFmZca1ODMSkUfO9KH5xEp9rRI3jLMMlEvdvpFirPnT_TOFVx-PLKldmi_gn1tv4Bfbr-zRRo_vzJXGFIwfiopSMN4L5xn5tIGX-IssVpYCMaQoWkT0TRwvYmV9CJtAfXOt4bkbYMM6HRiYFZhX9HKULLzwI8ELBR9DsYb_hr4wLPSH7WaB0Ceuv9OsetdTY1NfqH-DdJGavexpM9wdaiTfTaKdxvQv0e43e5qNdpr1fGlg6g968Nd-UR_2NJvcQIHdf4G8KVmjngen9EYKqESc9zqh--Ymb_h3u8GXL-QqfXh7QbAIgmsNstXbxx0hNRg-YoM_dNUHj1DNdWJf7rQYXdvS-ht9MnWr6psJXaByQQfL4iiIPW1QG1UKhhvobmUHytaoQsxtCDwRxxAqxliJsE-5-8DSAvntCxmNG7-9G2vc0s2UwSyZbSwZW-Av_C0ueF0f23pPn7HAGz001NTEAvA89qOqylmZav3BKI0wrLL71joI0xTjVkSegjUoYsEWgKHUvYqiLuVrvCOzBsNWuCTGEqCXlALIFOsEq0gmFIJBW07FuGLfD8uwZF7pjRrSWGQxCuoPq5ZQ7kW3CMMk8fK4SLRHaCyg2M5dv1clhKo9kHFCDAvUYArP83qJYfS6IXcrPi1TK3cTXEYrXUUgsT6AAqCqMdHKU-W7pa4L6BS0Mjgca6XBlO1yyTrMk2wLMhBnoO3t_tw7q00_UH85h4YrThakCFJR2FJSYWLNyjj38iphhZtzI4aoyj5uO793qN_olM70-ibr6m4nd8om9NNklqQZWVqzLPWR0e4_-tcNxziagYWN_HUWxhhj8q-9uc-2xC5jtN2oyzgdu9xmHPcb9h7mc33kXpbOwiQjfWgWhS4ypHjf-3cf_wT_SrMyjZKkKONExxGM-huDf923kEZsHAxM9yrRAJlu4stECrJdgsglPqS2Eir5XY2dwHPaSSkTRoSn1ffirfwQwXBgzQ0jrUQvHTmTGGWw-KGMhupfekHAIBVuAv31xOFKwtRP8tLlOdcM0SgJ2jlc96ntoSBjQQwE3UqY4nYX14V45mWLwWcQE6y7gu-FQytOEtyHf__1_6NYI3H8DlhlR89SGgoYb2zM4JRZU9u_XGAY_fdgW_hh6Hqur1qPYO-ktM8zfOLzMa1HLU7peOlOY7T4orN_3-5l14mGvYxdBX7gx2JbOy-52IdjNFq6PpW7U5RsdDCcxqA3dfonsZ3FnFKwl9LYo_NiegDx7EXuTXNKfHUojMmodidnIfx_O7PAAgkZqmdj1tN2cKJsL1Fv4GxFqeEc-6FGvTDNgizRaxxK5aoGDYDGPdb7iABCz9HV6pwjz7mli0ANXjTtUlzPzPbusHFMyaGJTmlLRRGkPk9yVpVjWp0uVjN92PesOtvvmDWdx9Kpql3FbScbiWP3FD22yw0qKeSbJg_zQNKQv8MfYEE465Y17C0ViR6DCWLdRAKThGAiVzhmIq3Ww6SfNvTcsspYUuU6Z8yokhuVrDvXvClNIEzDMGJVkLBgjJ7oMrjbNIE7FLU1DigomDmnf3gm0qmGq91fHlk_cBcxickFHVEXrKa7agfugtihq97EFKc7aAfwWqqfh398_0N1A-EYxrFm0mz8AM1Av-y6Ey_vH3ggRhzF4s10WikoSzdP8qwKY31MjfrE8Zjeu9pQ52z8eQPGivMMz_SFDGOWrUgqUkl51zjSVJAs5yyNwfgtR6-fUb44nqN7FSAqB3wUF6wIAxD4mT6sY02iAnd4QFUhVsyxC2AklMOy3gCBC5nVAgxd0HAMZP0razYo7DGb17lWGyitGJQwohQPtycKG5HRif57P1wADaRyFqausBhFL0vUA5YclzZvWVdStVdfIwPSOVYiJesSZAquB9q0ZCW8ElljaLjo7NGe-tNpxzMRkkMKYYLXp20HY0Xz7UuRl2Z2rLKTze3-FXsH7NWJg0X4kdkpjiiAhz5Ss5ST82JXZncaU1QEMUl3x46jeJGYHU-x-DwN0jwLSuZrTmyUiCoErgcUefp_mG2_ZkxifPny8nKx4h2MlqD9MKvfSO3v58ZLT_8glOrvp9blfi0XqsW5StzFZ57-UYZy_-XyePhfGCT-F_zf3PvDBGH9KMjDlEc-Z_o4GkWtW8lj9ytLlYZ6Paj4bM7laRQxyIKvMUEFEyswbDZuB-FyoC_VCRAZAmNWooxpDUYVmNjNareJ7WpsMUeVA4jUy52dSjU9A1Vding6RmIwNW0wc9w4-paWoP1Q4ho00qKiYiT6yXWYyexUUiJVhrhZX3A931-cKcwkEQkTnVTLHDk0I3V3Jqcgol_kB1OzBmuRLyuRGdCrcClltUtWgft8ygPixllU-XkWpb4-bWMJ8SgI7lUErI-0DypaUILxF2s5OdYFGzvvvpW9mP2jNWFMYUU-JdxMMndV7SRyWFGaokhwQ1WVHiDVfOG84sTldjIU0RMpQrWYnwEm96rGkRlOSbUpxRoBvxlUgYFK4JZ6NqVwS2WHH9-8MkWFeKdxmXmV9jgYVcqSaA-pMxZpK8CfV2hBo3afzsI0lgFNoZVhJQksqB58SSWsFW_6OhcpLqoeV1NCNCwbxdjpxlCOc16wDfnmljimnsqCQOIjaCeWw1HCkPT5nZEtAycM2uOdOGKv5oojSocBVhXtJCfj-Bmxj3MgA3CvM20MCN0CGZQ4MFSBYRbM5Lwpzlese_tPPVksBWn0YzXv4q_NfE94RWG7qsk3zYa2zjvcVhvek8YEIsyf4f8DMRf4FJq0VuWsOI4aNjdsQKDxnGz185YMdar3E7n17YpTvQ38Q0a9mJpkFCrtGPfW1vilhaiqoQSj0hMlE67fN0fPmCOWDsHqvcXNoE0YYdIVg9ZrZ4aNOG6L16Cego5_hZn4akjdBmuQvkMgX9hWVE66Qj_YFZimoNd30LraJ9C9SBWcwYGGftlyLvfABr7s0Os8XAllaVX30NjZXALtCj_4jxvxMjEAIvhqxSmBEX6ualBu5b7ia3NlpEO7H4MIS8H_n6rWje71OtCJ0EuhSTUnMtE67FBaxdY0pRkdsA5fR1LAEaI8OaT3ePJmlH_yDiZaYsiqVQttPiCTsZq2kRQc5tAMb0yq7J0wIioraF2nZAMTNbE1mKlL1pxt0GGH812y4m1vHn89W-HX7K8adMrL3EDJ0MW-291vKvJrUKGB4zAHBonxnh6Ly-Z1A9yXstbm8hAIR4uYOwMiXVFnV5rLUL1tp3cd_GG4HjiIcTLGcHZA6qoedKneFdbsoDp-hqrxXOZlOsSCerWVgEiwzPOGD6ho9BhXOeMo1U2qwnzBQKkHylNTZ10FtThKLzRPvhDzeVWc85JOBjUoO9LnjbQJYny41WSyG8VphDgyi4ByNhTniz0gCMrd5JUed8M4z5gOLhlIE4Z8fghWBKpnpkrUgN3eizRRoEKjZaYpVJq2lMzT4GHzbVKYZemkN4qGQVljoDCL8BRKr0a4YSZEbuCxNPRZlXmZpoMBYyHp8BAgio1wmv-18bGR18SddfYzG1rdjilEUTCKcnGjmmOGhRdDjR8oZiArroQng-JmWED61ybAjkZPExFU9iGPhUPD1txYxCZ_2MAZL-tCSGJeVbLCCQciQ5bKrYW-XegoxI4-w1Ix8bXZEz4C7ZNMQJUMWoA9tFrLg0i5WisOCu_ApcAUfXTIO_AEo4jA2URENqqg0To4dkLHCHNlV0h7wf6berVZgVpImrBWzbBlpPNMb6Ba9VbqwfdaQI75pFScI3XzibPk8TDP_NgPs1xHPQyMEYUw8ACUELCqt1PVhJAXlF04z7f5r_OjhJzQPSheQXPGjHvFMLDuirQy_fJMMhc44MRVxzMqS2IETRfOV0LYmpqx7m2FCgdrNPcjm4c2q3gCRnOG1Wtbue86d1dYRVzFiD4xftMHhwLBsqOdnH4MDS21wwVhQmRpwoRN5IahX7muH0ehjgob-CujTfQowCnKWRaURelnrExd7ZEzsFRMHnxPEBQRLdGq8JyczjL8rux2mTVRisLIDeZNUJ67yoEgN2V_jPsAh6CC7apSSPJZrQEpMwcMaP1R_7ih72EIG_Vtx38Qemh-ZVRLCwnaIK23Q2Ny_7ASBTDlGigLB629rn4n0nPBDMS91_ZKEz2vgaFr58XQblV4TIiH3OMxqxIXTrL2TBnwMTpG8BDcF6X1UD4-NkXqCHBKDLnCvzALkTGPOlxdCToZfGRmHl4peoD4HatwQWVpv0i_MHrq_yg95CSYNcssMDD6WUsqmOY2dOJnkukgK93qEm3bUQZQha2QZwhkYPQoO_zGLJn8Tlaf6FK_Nscfja1DkkpqOrKFMXosqGXWHBAzxV0tinWXwkohN9NWP6JKBdoYyUBSBwvEaxj3Tl3iaEk7sj6jVfX4f5wu3-Tc9ZI4ytwxicAA85Eb6CEoPGApHmsGMQb4t-pYKeQhl08t3FPTRDTykhhxZTS5qWZpzFOQ4kKa2mNsD6i7BMMXre7Lc1KAafQ7UBvk3wK7dk1qZE8tIgPAWjKdJM1LQxNC6Ttz0EeH9r5s2fDDST-YtC-WJIVgBbW7bSpxy82DLPV8Hoa69sOALBrZ_QPghjQHYZz7cVCW0ZgjNiIQmXHde6IHbech9TNZ1SGZvLSRlrq4TKwy3XtCUWPQH16yS5HsXcGGRjWT2A98GGFIKAlRZxPMlCRas6tly0rxjsj3AtuVGBVTG2pNvIErRZUGLCW3jByPKVw0deB3bXclZABIp7Yhe02WATG1E3GLUAQGNQCtIZywkq1hzk_h8ZNLiXZzAtwCV-xEDmWxvpK1BtffE5mGJ9znJ6obfPwTpTFRbRu6KBjtNp1GI2ZEob3TffA_7slnzz_94tUXL75erMrrZRdvfsE9s-fuHcxd1DfvfAoK9rujN3SPD2zE69_v3NRjfC91WvnDyxqdbCXIIdit_3j3-NCoxmt8Cprm3S7xcf2gqlK32o-l3l8voCJHCp4okCy3AZh_QDtTKNm8CLmXuo8-RJGzQbaqLAQWvJNKmZaw-ZZo9ik9AF8anRVTqNlJUhTxfwNJt0tQdAaCasb4iuSXqiahn6_JZDgFwhq86U6nnWFI9LSXhoeWFRjOkuWYKiV5lIMyg3kC8Gpx0z1NB-_bQNI6eN8G4tPB-zYgiA7etwFVdHiaj5AhB-_bAN84eN8GHsfB-zYgIQ7etwEdcXjeMkIQHH69x7L_g_dtVI8fvu-xvvzw53ussP4N-LkuSD68_B5rcg-_3mO97uHl2FhFd_i9NpbaHbxvo3jt8Pt8LCs7vCwZi85-C51JlWYdXmcai30O3rdhph5-vUf78_DrPdqSh-fnY6XSb2AL6lKPw_c9VlP8BrqiLrg4fN9j3v7B-zYy7w-_3mNC_sH7NtK6D68zjZnPh5_3mGB7-H0-5t0eXo6N6auHn_eYz3R4PXXMITq832HMPTk8XxuTJg7et5E7cfC-jaSAw897jCcf3i4Zo6a_Qd86jHqYvt8YAY6fjy7Pr3QfMjoo836NLozLIMbeRFTbaLyWmX5zCSkp8n2p-kDHY2ZjGtScIFCGbjNgAo4ogdNZ7EYxnIi_UgaBgCmXiUsE_6mS3PIrx4wGIonvfvtMFfhFkXAvAg0ycZPIDV3Pz_xYr4F5rYx5pYp51czPNlBnA3Vbgbq733G0e8dP8Mv-G3xuu87oUe4sivw0i4vEjXlVFFXh-SVPQrcqE86jqkjzxIvDKom9AOyOlKUshu_jFJQzN04zTmjl--az78qi7DhI91xZ5ANLLLOgtFcW2SuL7JVF9soie2WRvbLIXllkryyyVxbZK4vslUX2yiJ7ZZG9ssheWWSvLLJXFtkri-yVRfbKIntlkb2yyF5ZZK8sslcW2SuL7JVF9soie2WRvbLIXllkryyyVxbZK4vslUX2yqL_-VcWhTFPcz8tWBjrfCQj9dCQuQ_LGVSyOEuTHMRJwF2Ni22kEZopQvfM_9NcDFkiASkKvidEDTk1-_P2st_DZU3-Ok5JrKHKTCL_lRHVJHeeIsMFE45FdDfodb7LKriJ60cpT3xWaBXFyFbca999WJrhIP-Sv9zJdXSTdQanMqYYLtkFsyyIRpa0z-gKZlHiyuuBfG8Wi9uTbramQjh8nnzei2aJn4nObrKU4KS6USQHBKzCD9x9AxptoHCWJKnqIIHn0xufT-TzivsQK8pwAtnNhks0C5JAPm98vsEsiWaeG46tx5m_jzyj0RHMvDCSz6ezzN072dGkADbmBebgPXHR100WQwD8PhyJE3upuDTqJnsAiJ-p4Rifp4Ig9po0e02avSbNXpNmr0mz16TZa9LsNWn2mjR7TZq9Js1ek2avSbPXpNlr0uw1afaaNHtNmr0mzV6TZq9Js9ek2WvS7DVp9po0e02avSbNXpNmr0mz16TZa9LsNWn2mjR7TZq9Js1ek_bfd01aGXpZ6JKRO0IFvgCzZFX_JD0J3epYRVoRrkXBX4FMug198a7tUOjhahqDkWWxF5d--egD1apVifmW7VrAhG60ctWKPmQiv_SxS0V3AoOx5DGP0zB-9PH-_de_fa2AdEZLABpAd4NOeofzhxWK8mRSOXvPKg7NXztqe-9LM_bFfszVZ-Uu4GprTG4u1D69to4AZVzctKQ34briJHo5WalhEzIB1qRfCX4K6jCHjvloDAEt-pGFSrLOgd0L0w5s9ZtWav8wvpGe_36LnNu2hFPUXbEBTSvvOHtLwE1Udb9ib0nppr1TCBCCenUrzKzJkP6pH2kswHKEirKzM9X2IeVuhDBBPU2k6AkPHA6bSDiujTTahMMMuDYOeEw7_jCg2MQv8pBVWe77ZRz7Weh5oFnw5CagWA1keTtQrGVVllV9AC7xNGLsCKB6EMRYHpegAbA0Dcs0zrzQw7y6zGNRBK3woMwDUAaiyvdiFrAgLeEvl-deWnh5kXtldHfE2Mg_Dr09iLFB4XKXF5VFjLWIsRYx1iLGWsRYixhrEWMtYqxFjLWIsRYx1iLGWsRYixhrEWMtYqxFjLWIsRYx1iLGWsRYixhrEWMtYqxFjLWIsRYx1iLGWsRYixhrEWMtYqxFjLWIsRYx1iLGWsRYixhrEWMtYqxFjLWIsRYx1iLGWsRYixhrEWMtYqxFjLWIsRYx1iLGWsRYixhrEWMtYqxFjLWIsRYx1iLGWsRYixhrEWMtYqxFjLWIsRYx1iLGWsRYixhrEWMtYqxFjP1HRIwNk7J0iziuPOaP7F7js5n5yI8ArKarikG7Rp2ApzoJ2sBaM9j9fUHS1I8iOUrLzBELDzEhUGCMBd8jjB5MToI0tCZi4Xws3iW5YSIYqm9QcWrXc9qve_EMBT_XiVMI7qKB_cgyktoiZVxQ8eVMqWHCWpAJyWuhBmt15gYNBkQh7hVzg2sllJB_h03XKCkg7DShNNTEc0GIy7Q0UwGkquarqVKh3MvSMEvCMNcVwAY23VgB_CBQOYnXVaNP9CXVDctyX5E_I1zOl6DitZfoJSDvRYsHCJkBLYzIfyM_CuKd7EI_zozybambMdpkM8PHhBrpNgSxsPFJE2emcaqcsBpSd6-2ZpjJWltT5fUC1UUKCgk_uXU6hMyArfSJQhujTKGZTJcGaxrGANt_zPXG1kAkotHdo1UveBYcjI3SGFa0PeDcFbgpQddoBwGDTLgdAnxGpKTAoaoQwolpdqCgOrHyTOW_I0OGTwQHRWlMCvkYl4tK0SUNubZdQNOCHqEDi3xtka8t8vX_ROTrc0zxGJGvNw1t5ztiX2dxFiZhHm7hnt7VPp3GaWVbbZDb71Jzf7Ghv7_wElM57XbhKqfgmY2h3wSdPMZFxngfdmmMSyoFWvqMpsYc3wEegPpiTUrBNF7x9W6MmRk9CsDm5q3g1JKnznNWYGCEtLYtJ6zR-QdgEBd-WGRRFHIehG4VJJXrprys-E0YxBoa9XYM4n-ULXN3VOZdWFnvl_2osYeByS3dyK8QUzOK4oQnWZZXpRvnVeZnSV4mHmZfhV5QFT5L3QJWmLkBeg_z0I14fNN8dmFyff_Yd4-9eA9MbuXGZZF7oYXJtTC5FibXwuRamFwLk2thci1MroXJtTC5FibXwuRamFwLk2thci1MroXJtTC5FibXwuRamFwLk2thci1MroXJtTC5FibXwuRamFwLk2thci1MroXJtTC5FibXwuRamFwLk2thci1MroXJtTC5FibXwuRamFwLk2thci1MroXJtTC5FibXwuRamFwLk2thci1MroXJtTC5FibXwuRamFwLk2thci1MroXJtTC5FibXwuRamFwLk2thci1MroXJ_UeEya3iNGJuiTJb50YZEGKa894f--vNP-_DnUpO_t_zly9O_vz82bf_YWBP_YESl4RGg8Cc6_Vu8ZNAslVuJRldkFtGFIui84wPx-aqy3pFSuGeje1R3GxslJKHpe41LrxARnUirOVeOJ_q3W-gAcKuYoXM39rN1qUQl8nXqDNkjDJ-v81zSBYNiuVvGTJolyPl2U5zEgaPaIYaTS_4DXIn5PBUiWO8ACwf9RFT757dpAARQzOVMYO9SXk_aiTCRSgZkkVmtsjMFpnZIjNbZGaLzGyRmQ-HzPzml_8CBgxpDw)
