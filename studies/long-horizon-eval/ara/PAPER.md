---
title: "Verified Handoffs Through a Governed Knowledge Ledger"
authors: ["Proofpress contributors"]
year: 2026
status: frozen-complete
date_created: "2026-08-22"
last_updated: "2026-08-26"
compiled_retrospectively: true
source_commit: "c96fd86b59e6844ad45201d7db4e0caaa91f5b4c"
abstract: >
  This artifact documents a frozen, LAB Contracts-derived evaluation of
  ordinary versus Proofpress-governed handoffs across three legal task
  families and seven model panels. Across 126 admitted paired runs, ordinary
  handoff passed 89.3% of matched rubric criteria and Proofpress passed 93.4%,
  a descriptive difference of 4.1 percentage points. In 63 controlled stress
  pairs, ordinary handoff propagated eight injected unsafe states and
  Proofpress propagated none. These are bounded product-mechanism results, not
  official Harvey scores, statistical-significance claims, population causal
  estimates, or evidence of improved legal intelligence. The ARA was compiled
  retrospectively from frozen protocols, immutable results, invalid-attempt
  records, Git history, and content-addressed receipts; it does not fabricate
  contemporaneous research sessions.
layers:
  logic: logic/
  src: src/
  trace: trace/
  evidence: evidence/
  staging: staging/
---

[//]: # (ob:348414db)
# Layer semantics

[//]: # (ob:207e52ff)
| Layer | Role | Mutability in this frozen artifact |
| --- | --- | --- |
| `logic/` | Current claims, problem, concepts, experiments, and solution specification | Frozen; revisions require a new study version |
| `src/` | Reproduction environment, configuration, executable receipt verifier, and pointers to the harness | Frozen |
| `trace/` | Reconstructed decision and experiment DAG plus the compilation session | Append-only; reconstructed nodes are explicitly marked |
| `evidence/` | Content-addressed receipts, result tables, exclusions, and figure pointers | Append-only |
| `staging/` | Unpromoted observations from this compilation | Empty by design; no historical observations were invented |

[//]: # (ob:5dd94796)
# Layer index

[//]: # (ob:9ee0d58e)
- **Logic**
  - [`problem.md`](logic/problem.md) — observed handoff failures, gaps, assumptions, and key insight
  - [`claims.md`](logic/claims.md) — four bounded, falsifiable claims
  - [`experiments.md`](logic/experiments.md) — mechanics, quality, and trust-stress experiments
  - [`concepts.md`](logic/concepts.md) — controlled vocabulary
  - [`solution/`](logic/solution/) — architecture, algorithm, constraints, and heuristics
  - [`related_work.md`](logic/related_work.md) — typed dependencies and deltas
- **Physical**
  - [`environment.md`](src/environment.md) — reproducibility environment and secret boundary
  - [`configs/`](src/configs/) — frozen task/model configuration
  - [`execution/verify_receipts.py`](src/execution/verify_receipts.py) — content-addressed evidence verifier
  - [`artifacts.md`](src/artifacts.md) — pointers to the complete adjacent RelayBench harness
- **Exploration**
  - [`exploration_tree.yaml`](trace/exploration_tree.yaml) — reconstructed DAG grounded in committed records
  - [`sessions/session_index.yaml`](trace/sessions/session_index.yaml) — compilation session only
  - [`pm_reasoning_log.yaml`](trace/pm_reasoning_log.yaml) — disclosure of retrospective reconstruction decisions
- **Evidence**
  - [`FINAL_RESULTS_RECEIPTS.json`](evidence/FINAL_RESULTS_RECEIPTS.json) — admitted content-addressed result set
  - [`tables/final-panel.md`](evidence/tables/final-panel.md) — bounded aggregate table
  - [`figures/public-result.md`](evidence/figures/public-result.md) — publication visual pointer and caveat

[//]: # (ob:db7eb561)
# Provenance boundary

[//]: # (ob:3ad5ae15)
This ARA was not maintained by the ARA Live PM during the original experiment. Its logic and exploration layers were compiled after study closure from committed records. Every reconstructed node names its source; only the 2026-08-26 compilation session is contemporaneous. Raw prompts, private transcripts, hidden chain-of-thought, credentials, and unlicensed source documents are intentionally excluded.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZmNjMyOGFjMzI3MjczODFhNDRmZTRlZSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImU3ZDljNzZhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83ZjQ5MzRlNWNjM2EwMDk4NjM5ZTVkMWYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzZiYzBhOGUyMTU0NmM4NmUxNGUzZTVhMSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWm2P28YR_isLBQESVy8UxTfJQIGL6zhGL4VxdgoUPkNe7i4l5ihS4ZJ3UWwD_dY_UOQn9If1Q4H-iz6zS1LUne5yPadoPhiw76Td5ezM7DMzzyzv3YCXVZpwUS1TOVgMtttlkgQzN-Ji5oZuOIum3PMS5Sk1GA7iQu6WMl0pXWGtXnPXDxaOmCV-5M6VE8TTmZwF3PND_J87oS9jwcN5HDhTNRVTP5i7YehMg0h4TpjwkGPchVyZalFcqnI3WLyjL9Wy4ivskPGKthriQ6wyDPxZlWmS8jhTrFSXqU6LnK2xvih3LN6xF2VRJNtSaY1ntlxc8JUiow6Gy-J7BXPrkgSuq2qrF5PJKq3WdTwWxWYi1irfpPmq4vkqmjmTg6dL9UOd4vOy1qpciiLXKocvqrJWH4aDteLkRBXKuQgDPrAjS3VpFsG5ahkm3nzmKV-IGXeceRTM5sqX04Q0K8qKTFtmaa6geXsi2TKIhcMj5U59LxBRoKaemimfT605jXZLwbe6zmCwS3qKopR6sHj9btBs_26AUy5KTZ_stJLLGC5_Pajzi7y4ygdvYEOLBzrgqpap0pOsyFejdVGmPxX5SF3ybMJLPnlx8uLp2XgjB8P_CkO8qso0risc3TLmOtW0kcqSJddwaaWMvLrCdqToRZqTSL3TldpgJucbOtFW4SEe1YSCwSKvswzqizWOTVnD46wQF1jN56ESUUiScWKV-pGM22OFPSPs5Uqyb3guiyRhL2H4Dqub3bmURq0tYU5dYeQzdp_Hq92WlCUMAE-DD2-G7VkM8ASpvRSl4tZmM9M6UC0BD9d3ZBwCIjKcetyN_MR1KVryojKobuDCGrgwAFdcbIs0rwz6S7MTuaX9Rl55QzjLUrHrSehjryfEoPqBsNRFUi0TWK3KbZk26NfxdDGbRqGr_Cji8ZwrHkfJ3OFz1_GBE-nMEs_1XCl8YGYa-U4cuQ7sdnyHq0ghpwiSXfHKoNiey2KKY6eBgeu4wciJRm7wauou_HDhzH7nOAvHwUONw7EqUrOZnKtk8KE3-u5_jnsDRovLNddrrA-8JJgqWO9JShVGRg-qDU4fCLUPH4ZHI1_JtOriHqeZVwtRSPXj4I3JJbIWt81eyxk3Zn-okau76XW94fmiTBGPpaRU-ttNLkbVh-YWJYF87s8PcssX__r5b__-x89f3pVCRqPReV6lVaYW7LwpbPuD1ezVuizq1Zrx_aH_EXplSiLUT_dHjtDmAzrsVqOZF3lTT8YHGp3ynSqZVrC0SoW-O7fdXHwdXr3tXCdUvpskD93ufbPde3ZWIJm9Z9_WSDdpllY7luasQnlnSVn8pHLWIoG9P8_fMziQ7VWziayvmC_l3AvnwRHFoAtQew8ftAvvsH-ulCP9SD1kmxF79Oi0WKXi0aPznLERe_0WMQhDNoD-2zdfZDQ32Q99yf7517-zIgaWL4GHvWIZONCBVigcKvaD6fWSh4TAc6FYXNS55OUvF7kjD9zhjBmXPldT_2O2fUUnfnJ2wq64Zqh1bMNRQPAfFoPjVWtlZk_TS8VefMtkjfqyMsOI6tvD4igJ2OtRqg20_JWqvMh4ujnME72ovGZ5U85PpNRsW8eozZzy12hVcmlNNfoi2bKboXlLJD58iweF421x9_GW2hC6Jd4eLr4XeLeFzcfofgzxt4TJw7f5mDhJV2nOM6Z-3KLubCBuzJ5Xmpl8w4BvmsmK0uzNMjoJza5UCY5ZbLYpahDjSUVApBhgIrst0m4EV2PfmRnQRhsQe1BMuIjpC5WpCjuassh0De20knt7_nLy7SnMzNMEVMPome1RMrah18b2u8HVmkjuE6uxeb4B7osz9tnMb5SHzwoU2ePOdsfBHuZX6BGLumKGBpAvkRfqDG4rSAOiWjRo21GIymhe8VKsWVVyofSYGOe9G4A7GkXrxD6z79PaPtt_94mzfOIsnzjLJ85yz5uJe90_XO-_w2GnienFj7Xav3Tt8KvcLXjuTHAlncDlc6g25ypw0CY6sZfMnDBMYBNXXhw6XuJyN4zETCoVJWHMYykCT9zDthv3DLOF4-HfkXuG7hbw_33P4PC57yTS9XkYtPcMvRLQwOrjcjv9LM8H57ntrvWCvT7vX7ERfE1njrnzwZvzfIfKuGDkyfOcnF7jEZsyR8QxwAPUOcKuUm2FJK06x7u0VcZ1tay38sZsQLMtU1mWqioLvVWiQvRluwWjay1sWtSlgPRis0krelzMg0RGQezPVRB5Hpee7zpTGcrYU47gnM-niR97wlgZa6rpeO73lARN-HeZXhaiJk6FocakITs9-Yo9IR9ggR5JeJeSIZ11bUlWkZCgokQ8EhUiwNS6F8ujVev1dXsiXMAu4lClUixTKzCOiusLkpPwDaoRCBZxJE2hzTaFVBnb8lxlesxO7LNTF_xGwgFwIebSEr_KOtfDThOS1uyIBRp0jEXz8exzKIwkV4m1eSIG4WGiTMEJU2427Z1989h8NvY-H5I8zqTSWL2lE2EyTRJQS0q1kOmNpwy0T8B_dKdpbiKh7_OcBTOLoiIj_gn_QzZJI7V7Cu-1LYstXxE4mEpX6wqljS7-8RUG8gT8sqLXC6QtiekrvH8yL3I1xvmCyeGAm2JAvjJXZdVoo4hgpXrTksEhpX9zlEmSihRn8g1H4QO5FQWWDM2uqHxEEEc6XYHL4iMZb5vGIUze1pkFheC15hlJA99NN6QuGQrcpLJ1WLrZUq2SDQLgLpVl6YqmjeJdWWoDgsRdiwmC6aZlLBBXFaLIsFW62dRV87alsQ5El2epHPGKeHtlhZl3DUP2LK3atzFDA4KmVxkhmZJjCSpKKJy7fsxSChRlq2XCCUCcQp7Zh0xLkKsCMdCx6OY6To8p9KklWdBywzcW9teEBnSJr_hhvhjmvbC_zEDrukX3yT4EtKGiLNoPGERCPFKam5zqqQCFEXQtdLq72x6J7e5u70VLG5lunHA-9cH7p24rs8dUG5kfxT0PftLgW-u3txh7UpfUNuxxaCnckA5EqC0d_r5f1PaAdZGZy1ZGWDJINt_es6-NBo-7t3R0jObNGYI_V1dN79WUxUYVOjNS5Ew10UVTKr9MyyKnPY0mSbqqbV9K6ijR4dPgiiRS3SqteiZ7UO-KFo_I1pojgyLAW_2ajS067Nb0Sg8FwuQJCZuMfk1H3NjO_nDyjG2z2ravNqys3Q1CIegEHCqXoyLPdo9NgOyl5kjE2iQTarKRIyoE4IaXF5iz-nTINMdyawwNm6hkxgXmeAS0Im9b842v1N4LB2q1Tm_wTlt9l8Pxm4KUtHzdWKVtdjDA6hv7nj1FAjDvXWEQMtljmNZvfw9kmNsD2yWTnceaoCYMpvPQDaJExr6YtWHQ64uuhdYd3U4jD9E0dWQyn4dx0srrNUAt_fm4tqYtOglPs9rk-RXf0jFoXcNL-zO5UBSmmgpSu48NuP423YjdJQFVaSvPEFtkun0Jbhe2gnrh2Zd2OGxFNnVLQKsfak7Jw6oHkOpqZItrP9w7XZtccKDtfswK75Xpy0LwGOXMEgmS0KaMSfd8N2KfplwPIiEq-BFKZSvAqVrbPESsK-2yz1qhj6JS2qlXKvqTAbm8KsqLvorXxu1GBBkKcgoJhFtLl0CTQKOQ_4GIF-udJizvQdHLR3YDylqHg1Z62WSxtMnNvTUNKwOxrbrusudghK2eNJLbrw0QbNYiljexfO4gI-5xQHmRPGrS4W7ZZozxdtdqfMeS_SEe5p2OdbRJtt2vrTN675H-kJV3PRe3LB_883tOdA_JF2X9K-ywbhO1PYSn-7vI3jnsB5dAqxrv-CbD5jaXH51tz6WfjCmVr8qG1KF82nagslmWWE0H24Z8TJoPS3vneLDrHWtan96sFZSLu4yzwTlwXeRIYUsg91D80VkrmP6AJis0ZXtQwgN21zeY9muLWuvc5lD3nv36-Z9OTpdnT19-d_rqJX4_efr8xauX4--xMVTpatMdy5o4bvuKYyzQ1C2tuhxoS9gkoWvpkWlSLJa67Y4usBu1nJyvVqUi2m4LYivaVkE9sTe8I7v3Nem3rWmgu78bZqAzyJctmi3L5ZfoUI9cbDUFKImVH4u5cBOv44q9u67-e_773Vw1cqMpqqRwotiNZMdB95dZjdzf0msCi1BDJ24E2pg9pb8AO0KWGL2Y12gYNLNN-2MTNEbHfc9_NLhSfb2dGLMzfkXcdmMY1BaNuEEMpm1LisF1KgELuudP81GRjOjaH_UaFQj9MV3z86ypQHUOYKicMG1V6zf_hvAQ8qEJz6Cw4WdA6vh6X_HmA_79B4cIjEc)
