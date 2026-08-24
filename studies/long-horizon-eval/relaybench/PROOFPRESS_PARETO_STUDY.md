[//]: # (ob:03db813b)
# Proofpress × Harvey LAB: governed handoff Pareto study

[//]: # (ob:f69daa06)
## Decision

[//]: # (ob:e439b2a3)
This study asks whether Proofpress improves long-horizon legal-agent work when the
underlying model, task materials, evaluator, tools, and execution limits are held
constant.

[//]: # (ob:46841646)
The primary comparison is deliberately product-shaped:

[//]: # (ob:76cadfc5)
- **Raw handoff** transfers the ordinary readable workspace available to the next
  agent.
- **Proofpress handoff** transfers the same source material and exposes only
  conclusions admitted through the Proofpress ledger and returned by the trusted
  context gate.

[//]: # (ob:57eeadf3)
This is not a comparison against a separate memory or ontology product. Any
distillation, verification, judging, or review used by Proofpress is part of the
treatment and its complete token, latency, and dollar cost must be counted.

[//]: # (ob:8c648201)
## Relationship to PRs 22, 23, and 34

[//]: # (ob:7d05415d)
- PR 22 defines the original long-horizon research question and claim boundary.
- PR 23 supplies RelayBench execution, cold-boundary, parity, scoring, and reporting
  mechanics.
- PR 34 supplies the product treatment: evidence import, append-only ledger,
  evaluation, policy recommendation, human admission, trusted context, and local UI.

[//]: # (ob:3c438977)
This study integrates those surfaces. It does not fork Tom's RelayBench harness and
does not treat the local UI as experimental evidence.

[//]: # (ob:27d99607)
## Research questions

[//]: # (ob:b63dff18)
### Primary

[//]: # (ob:6a191609)
At matched model and execution limits, does Proofpress increase Harvey LAB final
all-pass or criterion-pass performance after a cold agent handoff?

[//]: # (ob:1baca415)
### Mechanism

[//]: # (ob:21cc85e2)
Does Proofpress reduce stale or unsafe state propagation without increasing false
stops, unnecessary revalidation, or clean-continuation failures?

[//]: # (ob:8c2f2a73)
### Deployment

[//]: # (ob:fe993a43)
Does Proofpress move the quality-cost frontier after all treatment overhead is
included?

[//]: # (ob:c12d3992)
## Experimental unit

[//]: # (ob:27d61266)
One unit is a matched pair on one version-pinned Harvey LAB matter:

[//]: # (ob:cc9a861e)
1. identical initial matter files and staged releases;
2. identical resolved model, reasoning setting, tools, task instruction, evaluator,
   and provider route;
3. one registered cold worker/workspace boundary;
4. raw and Proofpress conditions run with independent model calls; and
5. final deliverables scored with the same official LAB evaluator configuration.

[//]: # (ob:41a8ded2)
The first calibration should use 1–3 public contract matters with consequential
state changes across stages. It is a calibration, not a public benchmark result.
Expansion to a publishable sample is conditional on parity, telemetry, evaluator,
and treatment-integrity checks passing.

[//]: # (ob:6852bd0c)
## Conditions

[//]: # (ob:2d044e9c)
### C1 — Raw handoff

[//]: # (ob:0641ea0f)
The receiving agent gets the ordinary portable matter workspace and readable handoff
state. There is no Proofpress verifier result, ledger, hidden orchestrator state,
transcript, or cross-session memory.

[//]: # (ob:00263ff2)
### C2 — Proofpress governed handoff

[//]: # (ob:5947a59d)
The receiving agent gets byte-identical source material. Before the boundary, the
sender may import evidence and propose conclusions. Deterministic checks and the
frozen policy may evaluate them; an authorized non-proposer review identity makes
the admission decision. After the boundary, the receiver gets only the output of:

[//]: # (ob:39182e1a)
```text
proofpress context --scope <scope> --actor <receiver> --format json
```

[//]: # (ob:e368caab)
Rejected, expired, superseded, scope-incompatible, and unadmitted conclusions must
not appear as trusted context. Their IDs and blocked actions may remain auditable.

[//]: # (ob:f31c71e0)
### What may differ

[//]: # (ob:8df0559f)
The conditions differ only in the treatment mechanics required to create and consume
governed context. Source material and task substance remain identical. Proofpress may
distill source-bound candidate conclusions because distillation is part of the
product treatment, but every generated token and every model call is charged to C2.

[//]: # (ob:3358036e)
## Model tracks

[//]: # (ob:704d982d)
### Track A — Harvey-comparable

[//]: # (ob:92d5764d)
Use a model and configuration already reported by Harvey whenever the exact public
route remains accessible. The first candidates are GPT-5.5 or Claude Opus 4.7 because
Harvey has published LAB all-pass and cost/latency context for them. A result from our
public task subset remains our composed long-horizon extension, not an official
Harvey hold-out score.

[//]: # (ob:066c5e34)
### Track B — open-weight cost replication

[//]: # (ob:478bda41)
Use one version-pinned open-weight checkpoint served through one no-fallback route.
Prefer a base family already present in Harvey's published research, such as Kimi K3,
if the exact checkpoint, license, quantization, serving stack, and resolved identity
can be recorded. Do not substitute an unrelated cheap model and describe it as a
Harvey-matched result.

[//]: # (ob:8c71b340)
Track B is a cost and reproducibility replication. It does not replace Track A.

[//]: # (ob:42296223)
## Outcomes

[//]: # (ob:e49abdbb)
### Quality

[//]: # (ob:223580ee)
- official LAB all-pass rate;
- official LAB criterion-pass rate;
- operative-version and stage-disposition correctness;
- unsafe state propagation;
- stale or superseded conclusion reuse;
- clean continuation;
- false stop and unnecessary revalidation rates; and
- invalid, incomplete, abstained, and inconclusive runs with reasons.

[//]: # (ob:5bf8f2a8)
### Resource use

[//]: # (ob:f2f377e9)
- total input, cached-input, reasoning, and output tokens;
- total provider and local inference cost;
- wall-clock latency;
- model calls and retries;
- Proofpress distillation, judge, verification, and review overhead; and
- tool calls, file reads, and turns when available.

[//]: # (ob:a77c9da2)
No hard cost ceiling is needed for the calibration. Complete resource accounting is
mandatory.

[//]: # (ob:3b954f6e)
## Pareto analysis

[//]: # (ob:c4c15e9f)
For each matched model/task configuration, compare quality against total cost,
tokens, and latency.

[//]: # (ob:0bbdff6d)
Proofpress strictly dominates raw handoff when quality is no worse on every frozen
quality metric, better on at least one, and resource use is no worse. A result may
also advance the empirical frontier when it produces higher quality at higher cost
and no observed configuration achieves that quality for less. That trade-off must be
shown, not collapsed into a single marketing score.

[//]: # (ob:62856701)
Report at minimum:

[//]: # (ob:8ec0fe29)
- the matched same-budget quality delta;
- the incremental cost per additional all-pass task and passed criterion when
  denominators permit;
- the full non-dominated frontier; and
- task-level paired outcomes, including regressions.

[//]: # (ob:b4a4682f)
## Run sequence

[//]: # (ob:f15c27f0)
1. Freeze upstream Harvey revision, public task IDs, Proofpress revision, model route,
   judge, tool surface, and evaluator.
2. Run deterministic RelayBench mechanics and information-parity checks.
3. Run one smoke pair with outputs excluded from reported metrics.
4. Run 1–3 calibration task pairs with full telemetry.
5. Inspect treatment receipts and task-level differences before expanding.
6. Freeze repeat count and analysis plan for the publishable pilot.
7. Run the pilot without changing task selection, prompts, model, or scoring.

[//]: # (ob:8c9683e6)
## Publication boundary

[//]: # (ob:4239307a)
Until the publishable pilot is frozen and complete, the only defensible claim is:

[//]: # (ob:bdad788e)
> We are testing whether governed, verified handoffs improve long-horizon legal-agent
> performance at a measurable quality-cost trade-off.

[//]: # (ob:2c099878)
Do not report test doubles, smoke runs, hand-picked successful tasks, or local graph
screenshots as benchmark improvement. Preserve nulls, exclusions, failures, and
invalid runs.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2ZmZGRiMWQyY2M5OGEwMTM3MWE1OThlMiIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
