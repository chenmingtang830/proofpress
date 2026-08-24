[//]: # (ob:b2d936d4)
# Proofpress v9 S4-boundary 2×2 handoff study

[//]: # (ob:e16a427c)
## Result in one paragraph

[//]: # (ob:0ecc6e72)
Across three frozen public LAB Contracts tasks and three repeated receiver runs per
task, the clean arm scored 758/852 public criteria for ordinary handoff and 789/852
for Proofpress (+31 criteria; +3.64 weighted percentage points). The mean paired
delta was +3.51 points with a repeated-run 95% t interval of +0.55 to +6.46 points,
which clears the preregistered −3 point descriptive non-inferiority margin. In the
separately labelled LAB-derived stress arm, ordinary handoff propagated the frozen
unsafe conclusion in 4/9 pairs and Proofpress in 0/9, an observed 44.4 point
protection effect. Only four pairs were discordant, so the exact two-sided McNemar
test is p=0.125. This is promising panel evidence, not a general or official Harvey
benchmark claim.

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
| Arm | Ordinary | Proofpress | Weighted delta | Mean paired delta (95% interval) |
|---|---:|---:|---:|---:|
| Clean | 758/852 (89.0%) | 789/852 (92.6%) | +31 / +3.64pp | +3.51pp [+0.55, +6.46] |
| Stress | 760/852 (89.2%) | 783/852 (91.9%) | +23 / +2.70pp | +2.59pp [−1.48, +6.66] |

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

[//]: # (ob:a77329f7)
## Claim boundary and receipts

[//]: # (ob:a02c5c15)
- These are public-task rubric scores from a frozen LM evaluator, not Harvey's
  private leaderboard or an official Harvey benchmark result.
- The clean arm supports only a descriptive non-inferiority finding on this frozen
  three-task panel.
- The stress arm is benchmark-derived and supports an observed protection signal,
  not a population-wide legal-workflow claim.
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
- `scripts/bench-aggregate-2x2.mjs`

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzhkNjhkNzJmMWIzOTNiNjdkZjBjNzMxYiIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
