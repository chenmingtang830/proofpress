[//]: # (ob:b2d936d4)
# Proofpress v9 long-horizon handoff study results

[//]: # (ob:e16a427c)
## Result in one paragraph

[//]: # (ob:0ecc6e72)
Seven models completed the frozen three-task, three-repeat 2×2 panel. Six had
positive weighted deltas on both clean and stress arms; Inkling was +1.53pp clean
and −0.47pp stress. Effects remain model- and task-dependent: GPT-5.6 Sol was
+12.67pp clean on MSA but −2.35pp on License. Unsafe propagation fell from 4/9 to
0/9 for DeepSeek, 3/9 to 0/9 for GLM, and 1/9 to 0/9 for Qwen; other models were
0/9 in both conditions. A frozen DeepSeek breadth expansion produced 12 valid of
14 attempted pairs: +10.59pp overall, but +3.89pp after excluding three raw-floor
tasks. These are descriptive public-task results with substantial proof-price and
route attrition, not general causal estimates or official Harvey benchmark claims.

[//]: # (ob:4764a52f)
## Frozen design

[//]: # (ob:3f495765)
The unit is a paired S4 receiver run. S1–S3 sender state is frozen and reused across
conditions and repetitions. The model, provider, output limits, tools, evaluator,
task documents, final deliverable, and public rubric are held constant.

[//]: # (ob:e93c7056)
| | Clean handoff | Perturbed handoff |
|---|---|---|
| Ordinary summary | baseline quality | failure susceptibility |
| Proofpress | clean tax / non-inferiority | protection benefit |

[//]: # (ob:b652264c)
The clean arm does not modify the public LAB task. The stress arm adds one
pre-frozen boundary artifact to both conditions. Only Proofpress receives the
external ledger state that marks that artifact expired. The stress arm is a
**LAB-derived controlled handoff stress test**, not an official Harvey result.

[//]: # (ob:5e4d1b9e)
## Quality

[//]: # (ob:1a802c43)
| Arm | Task | Ordinary | Proofpress | Weighted delta |
|---|---|---:|---:|---:|
| Clean | Credit | 255/297 (85.9%) | 258/297 (86.9%) | +3 / +1.01pp |
| Clean | MSA | 257/300 (85.7%) | 282/300 (94.0%) | +25 / +8.33pp |
| Clean | License | 246/255 (96.5%) | 249/255 (97.6%) | +3 / +1.18pp |
| **Clean total** | **Three-task panel** | **758/852 (89.0%)** | **789/852 (92.6%)** | **+31 / +3.64pp** |
| Stress | Credit | 261/297 (87.9%) | 256/297 (86.2%) | −5 / −1.68pp |
| Stress | MSA | 253/300 (84.3%) | 279/300 (93.0%) | +26 / +8.67pp |
| Stress | License | 246/255 (96.5%) | 248/255 (97.3%) | +2 / +0.78pp |
| **Stress total** | **Three-task panel** | **760/852 (89.2%)** | **783/852 (91.9%)** | **+23 / +2.70pp** |

[//]: # (ob:fdab9520)
Across the nine task-repeat pairs, clean mean paired delta is +3.51pp (95%
repeated-run interval [+0.55, +6.46]); stress mean paired delta is +2.59pp
([−1.48, +6.66]). The confirmatory v9 panel uses one worker model only:
`deepseek/deepseek-v4-flash-0731` through a DeepInfra-only gateway route.

[//]: # (ob:a8644192)
The interval is a descriptive paired t interval over nine task-repeat pairs. The
three tasks are a fixed panel and repetitions reuse the same sender state, so this
is not a population-level treatment estimate.

[//]: # (ob:9da02a73)
Task-level deltas are heterogeneous. Across the three repetitions, clean Credit
was +3/−1/+1 criteria, MSA was +7/+9/+9, and License was +1/0/+2. Stress Credit was
+3/−3/−5, MSA was +9/+6/+11, and License was +1/0/+1. The aggregate must not be
reported without this distribution.

[//]: # (ob:15d54412)
## Protection effect

[//]: # (ob:cd2e5291)
| Stress fixture | Ordinary unsafe | Proofpress unsafe |
|---|---:|---:|
| Stale credit authority | 0/3 | 0/3 |
| Unsupported MSA approval | 1/3 | 0/3 |
| Revoked security approval | 3/3 | 0/3 |
| **Total** | **4/9** | **0/9** |

[//]: # (ob:5d631fe2)
All nine Proofpress stress runs independently failed the injected conclusion's
`not_expired` deterministic check and excluded it from trusted context. The batch
judge recommended `reject`; the separate high-risk re-review recommended `accept`
in every run, but deterministic ineligibility remained authoritative and admission
stayed false. This is direct evidence for keeping deterministic validity separate
from LM policy recommendation.

[//]: # (ob:eee518e8)
The endpoint was scored blind from memo digests. Four pairs favored Proofpress and
zero favored ordinary handoff; exact two-sided McNemar p=0.125. The observed effect
is therefore not conventionally statistically conclusive, and the fixture response
varies materially by task.

[//]: # (ob:17fc99ae)
## Proof-price

[//]: # (ob:d64e6f34)
Proof-price is C2 receiver-side model usage minus C1 receiver-side usage. Shared
S1–S3 sender cost and evaluator cost are excluded from this treatment overhead.

[//]: # (ob:d06f4537)
| Arm | Mean extra tokens | Mean extra provider cost | Mean extra sequential model latency |
|---|---:|---:|---:|
| Clean | 128,452 | $0.0897 | 109.2 s |
| Stress | 128,556 | $0.0943 | 116.2 s |

[//]: # (ob:a908931d)
The current implementation is not cost-Pareto efficient. Transaction-level batch
review reduces judge call count, but graph compilation, policy review, selective
evidence expansion, and receiver assembly still add roughly 128K tokens and about
two minutes per handoff. This overhead is a product constraint, not an evaluator
artifact.

[//]: # (ob:e2c20f93)
## Mechanism diagnosis

[//]: # (ob:48c417c3)
The positive quality effect is concentrated rather than universal. MSA repeatedly
gains exact quantitative risk values, likelihoods, deadlines, and approval context
that are dispersed across source files. License repeatedly gains the required
72-hour breach-notification counter-position, and the stress fixture shows why
version-governed context matters.

[//]: # (ob:08fc7f43)
Credit exposes the remaining coverage problem. Proofpress repeatedly loses criteria
for structural conditions of approval, especially the guarantor fund wind-down
protection, and sometimes loses exact policy-version citations. Verified context
was correct but not always sufficient. The next product optimization should preserve
the deterministic trust gate while reducing graph compilation cost and adding a
task-completeness check for uncovered approval conditions.

[//]: # (ob:4f4144dd)
## Cross-model replication

[//]: # (ob:4ca70d46)
DeepSeek, Opus, GLM, Muse, Qwen, Inkling, and GPT-5.6 Sol each completed all 18
frozen pairs and support separate panel-level estimates. Kimi was explicitly
terminated after repeated costly route failures; its retained calibration cells
and invalid attempts do not support a treatment estimate.

[//]: # (ob:658b678e)
| Worker model | Valid / planned pairs | Evidence tier | Clean weighted delta | Stress weighted delta | Unsafe propagation |
|---|---:|---|---:|---:|---:|
| DeepSeek Flash | 18/18 | Complete frozen panel | +3.64pp | +2.70pp | 4/9 → 0/9 |
| Claude Opus 4.8 | 18/18 | Complete frozen panel | +8.57pp | +7.75pp | 0/9 → 0/9 |
| GLM 5.2 | 18/18 | Complete frozen panel | +3.99pp | +4.23pp | 3/9 → 0/9 |
| Muse Spark 1.1 | 18/18 | Complete frozen panel | +2.82pp | +4.81pp | 0/9 → 0/9 |
| Qwen 3.8 27B | 18/18 | Complete frozen panel | +5.05pp | +4.58pp | 1/9 → 0/9 |
| Inkling | 18/18 | Complete frozen panel | +1.53pp | −0.47pp | 0/9 → 0/9 |
| GPT-5.6 Sol | 18/18 | Complete frozen panel | +4.46pp | +3.52pp | 0/9 → 0/9 |
| Kimi K3 | 0/18 pooled | User-terminated; unavailable | — | — | — |

[//]: # (ob:113b815d)
Across complete panels, weighted clean deltas range from +1.53pp to +8.57pp and
stress deltas from −0.47pp to +7.75pp. Repeated-run intervals exclude zero for both
arms on DeepSeek, Opus, GLM, Muse, and Qwen; GPT excludes zero only on stress, and
Inkling on neither arm. This is replication with visible heterogeneity, not evidence
of a universal effect. All prior invalid attempts remain preserved. Kimi's earlier
cells must not be pooled into a complete panel.

[//]: # (ob:84e36947)
## DeepSeek 14-task breadth expansion

[//]: # (ob:708dffef)
The expansion froze every scenario in the three public LAB Contracts families before
outcomes. Twelve of 14 task pairs were valid (85.7%); MSA scenario 05 and License
scenario 03 failed on provider transport/policy-review calls and are excluded, not
scored as zero.

[//]: # (ob:b84e75c6)
| Scope | Tasks | Ordinary | Proofpress | Weighted delta | Direction |
|---|---:|---:|---:|---:|---:|
| Credit | 3 | 217/253 | 227/253 | +10 / +3.95pp | 3 positive |
| MSA | 5 | 228/320 | 273/320 | +45 / +14.06pp | 4 positive, 1 negative |
| License | 4 | 160/211 | 188/211 | +28 / +13.27pp | 3 positive, 1 tie |
| **All valid tasks** | **12** | **605/784 (77.2%)** | **688/784 (87.8%)** | **+83 / +10.59pp** | **10 positive, 1 tie, 1 negative** |
| **Non-floor sensitivity** | **9** | **582/669 (87.0%)** | **608/669 (91.0%)** | **+26 / +3.89pp** | **7 positive, 1 tie, 1 negative** |

[//]: # (ob:bc410870)
Three large gains came from tasks where ordinary handoff scored below 25%:
MSA scenarios 02 and 06 and License scenario 05. The all-valid macro paired mean is
+15.47pp with a descriptive task-level interval of [+1.95, +28.99]; the predeclared
non-floor sensitivity is +4.04pp [+0.18, +7.90]. The latter is the more conservative
breadth summary. Each task has one receiver pair, so these intervals measure frozen
task heterogeneity, not repeat-run or population uncertainty.

[//]: # (ob:d812ed43)
Mean breadth proof-price was +132,837 receiver-side tokens, +$0.1127 provider cost,
and +145.7 seconds per valid handoff. Maximum observed cap utilization was 72.2%,
so valid breadth outputs were not cap-bound.

[//]: # (ob:6b452c0f)
## Frontier and optional tracks

[//]: # (ob:e5a8d0fd)
GPT-5.6 Sol completed 18/18 pairs. Clean weighted delta was +4.46pp (paired mean
+4.11pp, 95% repeated-run interval [−1.42, +9.64]); stress was +3.52pp (+3.40pp,
[+0.79, +6.00]). MSA drove the largest gain; clean License regressed −2.35pp.
All nine stress pairs were safe in both conditions. One successful Raw response
omitted input/output/cost usage, so GPT quality and safety estimates are complete
but its full-panel token/cost proof-price is explicitly partial and unavailable as
a complete estimate. Optional Luna and Grok tracks remain unrun.

[//]: # (ob:a77329f7)
## Claim boundary and receipts

[//]: # (ob:a02c5c15)
- These are public-task rubric scores from a frozen LM evaluator, not Harvey's
  private leaderboard or an official Harvey benchmark result.
- Seven complete panels support separate model-level estimates. They must not be
  silently pooled into a universal treatment effect; Kimi remains unavailable,
  not a zero-effect model.
- The DeepSeek breadth expansion attempted 14 tasks but yielded 12 valid pairs; its
  large overall delta is floor-sensitive and must be accompanied by the nine-task
  non-floor sensitivity.
- The stress arm is benchmark-derived. Protection signals appeared for DeepSeek,
  GLM, and Qwen; the other four complete panels were 0/9 unsafe in both conditions.
- GPT quality and safety receipts are complete, but one provider response omitted
  usage telemetry; its all-in token/cost proof-price is a partial lower bound only.
- Six invalid v9 attempts remain listed in the run index. A separate pre-v9 attempt
  ledger preserves eight valid negative/zero/positive observations and nine invalid
  attempts from v3–v8; none is silently converted into a valid v9 observation.
- The machine-readable result contains all 18 run summaries, score and trust receipt
  digests, request-level proof-price values, exclusions, and exact denominators.

[//]: # (ob:3ce5adc8)
Authoritative artifacts:

[//]: # (ob:68a38c2a)
- `bench/experiments/treatment-effect-protocol-v9.json`
- `results/deepseek-v9-s4-2x2-run-index-2026-08-24.json`
- `results/deepseek-v9-s4-2x2-results-2026-08-24.json`
- `results/pre-v9-attempt-ledger-2026-08-24.json`
- `results/opus48-gateway-v9-replication-2026-08-25.json`
- `results/cross-model-ladder-summary-2026-08-25.json`
- `results/cross-model-ladder-summary-2026-08-26.json`
- `results/qwen38-27b-gateway-v10-replication-2026-08-26.json`
- `results/gpt56-sol-gateway-v10-replication-2026-08-26.json`
- `results/deepseek-v9-14-task-expansion-2026-08-25.json`
- `scripts/bench-aggregate-2x2.mjs`
- `scripts/bench-aggregate-model-ladder.mjs`
- `scripts/bench-aggregate-task-expansion.mjs`

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzhkNjhkNzJmMWIzOTNiNjdkZjBjNzMxYiIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
