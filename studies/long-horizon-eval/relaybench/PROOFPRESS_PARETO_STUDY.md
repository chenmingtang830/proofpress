[//]: # (ob:03db813b)
# Proofpress × Harvey LAB: governed handoff Pareto study

[//]: # (ob:f69daa06)
## Decision

[//]: # (ob:e439b2a3)
This study estimates product effects when the underlying model, task
materials, evaluator, tools, and execution limits are held constant: the clean tax
of governed handoff on an unmodified task, and the protection effect under a frozen
trust failure. It then tests model-family replication and task-family breadth under
predeclared gates. Current v9 results are reported in `RESULTS_V9_2X2.md`.

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
distillation, verification, judging, or policy-gate work used by Proofpress is part of the
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
This study integrates those surfaces. The Proofpress team owns the integration and
will implement it directly on RelayBench without requiring a separate harness-owner
review. The frozen Phase Zero mechanics remain unchanged; new real-run adapters,
experiment manifests, and analysis live beside them. The local UI is a product and
communication surface, not experimental evidence.

[//]: # (ob:27d99607)
## Research questions

[//]: # (ob:b63dff18)
### Primary

[//]: # (ob:6a191609)
On unmodified public LAB tasks, is Proofpress non-inferior to ordinary handoff while
adding verification and auditability, and what token, cost, and latency proof-price
does it impose?

[//]: # (ob:1baca415)
### Mechanism

[//]: # (ob:21cc85e2)
In a separately labelled LAB-derived controlled handoff stress test, does
Proofpress reduce stale or unsafe state propagation without increasing false stops,
unnecessary revalidation, or clean-continuation failures?

[//]: # (ob:8c2f2a73)
### Deployment

[//]: # (ob:fe993a43)
Does Proofpress move the quality-cost frontier after all treatment overhead is
included?

[//]: # (ob:c12d3992)
## Experimental unit

[//]: # (ob:27d61266)
One unit is a matched pair on one version-pinned public LAB matter. The frozen v9
study uses a 2×2 design: ordinary versus Proofpress handoff crossed with clean versus
pre-frozen perturbed boundary state:

[//]: # (ob:cc9a861e)
1. identical initial matter files and staged releases;
2. identical resolved model, reasoning setting, tools, task instruction, evaluator,
   and provider route;
3. one registered cold worker/workspace boundary;
4. S1–S3 sender state is reused exactly, while raw and Proofpress S4 receivers use
   independent model calls;
5. the clean arm leaves the task unchanged and the stress arm gives both conditions
   byte-identical perturbation content while only Proofpress receives ledger state;
   and
6. final deliverables are scored with one frozen evaluator against every public
   task criterion, plus a blinded trust endpoint for the stress arm.

[//]: # (ob:dd7734b6)
This produces a score on our public-task composition. It is not an official Harvey
private-leaderboard score because the private evaluation service is not part of the
public repository. Perturbed results must be called a **LAB-derived controlled
handoff stress test**, never a Harvey benchmark result.

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
sender may import evidence and propose conclusions. Deterministic checks run first;
a frozen LM judge returns `accept`, `reject`, or `escalate`; and a deterministic,
research-only policy executor admits only `eligible AND accept`. `reject` and
`escalate` fail closed. After the boundary, the receiver gets only the output of:

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
### Track A — complete frozen panels

[//]: # (ob:92d5764d)
DeepSeek Flash, Claude Opus 4.8, GLM 5.2, Muse Spark 1.1, Qwen 3.8 27B, Inkling,
and GPT-5.6 Sol completed the same frozen three-task 2×2 panel. Every route pins one
provider and disables fallback and hidden retry. DeepSeek remains the low-cost
task-expansion anchor; Opus and GPT are frontier-quality replications. None is an
official Harvey hold-out score.

[//]: # (ob:066c5e34)
### Track B — gated replication and breadth

[//]: # (ob:478bda41)
Kimi K3 was offered the same protocol but explicitly terminated after repeated
costly route failures. Its valid calibration cells and invalid attempts remain
deployment evidence and are excluded from panel treatment estimates. Later adapter
portability corrections allowed GLM, Muse, Qwen, Inkling, and GPT to finish without
changing tasks, stress fixtures, rubric, selection logic, or claim boundary.

[//]: # (ob:8c71b340)
Only DeepSeek entered the pre-frozen 14-task expansion; 12 scenarios yielded valid
pairs. Cross-model panels remain three-task replications. Optional Luna and Grok
tracks were not run. GPT completed 18/18 quality and safety pairs, but one successful
Raw response omitted usage fields, making its full token/cost proof-price partial.

[//]: # (ob:7c94c14e)
### Credits and normalized cost

[//]: # (ob:885fe02c)
Credits do not make a run economically free. Record both actual incremental cash
charged to the user and normalized reference cost computed from provider-reported
usage and the frozen public price schedule. Pareto plots use normalized reference
cost; the run ledger preserves both.

[//]: # (ob:42296223)
## Outcomes

[//]: # (ob:e49abdbb)
### Quality

[//]: # (ob:223580ee)
- public-task all-pass rate;
- public-criterion pass rate;
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
1. Freeze upstream Harvey revision, three public task IDs, Proofpress revision,
   model routes, judge, tool surface, evaluator, caps, and invalidation rules.
2. Complete the DeepSeek anchor and provider-pinned cross-model replications on 18
   pairs each where the route is operational.
3. Preserve every invalid attempt; terminate Kimi by explicit user decision rather
   than treating route failure as a zero effect.
4. Freeze all 14 LAB Contracts scenarios before DeepSeek breadth outcomes.
5. Attempt every frozen scenario once and report missing tasks as invalid, not zero.
6. Complete GPT-5.6 Sol frontier confirmation and mark any missing provider usage
   telemetry as partial proof-price rather than inventing zero cost.
7. Aggregate complete panels, incomplete diagnostics, breadth, proof-price, and
   claim boundaries as separate evidence tiers.

[//]: # (ob:c70ab3d2)
## Execution readiness

[//]: # (ob:1d9da899)
[Interactive experiment structure: Raw handoff versus Proofpress governed
handoff](visuals/harvey-proofpress-experiment-map.html)

[//]: # (ob:d209203f)
All work is pinned to Harvey LAB commit
`7be41d57fd5a6e97b5f246a029e810f83d09cd96`. The repeated panel freezes Credit
scenario 02, MSA scenario 04, and License scenario 03. The breadth manifest freezes
all 14 scenarios across those three task families and records every upstream file
digest before outcomes.

[//]: # (ob:239ce906)
No-call preparation:

[//]: # (ob:c7b93919)
```bash
node scripts/bench-preflight-real.mjs --harvey-checkout <harvey-labs-checkout>
node scripts/bench-prepare-real.mjs \
  --harvey-checkout <harvey-labs-checkout> \
  --output <new-run-packet-directory>
```

[//]: # (ob:daa79044)
The real runner is two-phase. `prepare` runs one frozen S1–S3 sender state, builds
the C2 evidence-bound ledger, executes per-item deterministic checks, sends one
transaction-level policy batch to Gemini 3.7 Flash, and records fail-closed research
decisions. `resume` forks byte-identical raw and governed S4 receiver workspaces,
compiles task-relevant graph context, expands selected evidence, checks completeness,
and converts the final Markdown memo to DOCX. Human review is reserved for blind
post-run error analysis and cannot alter continuation.

[//]: # (ob:96c723ca)
```bash
node scripts/bench-run-real.mjs --phase prepare \
  --packet <run-packet> --output <new-run-directory> \
  --track A_HARVEY_COMPARABLE --authorize-real-calls

node scripts/bench-run-real.mjs --phase resume \
  --output <run-directory> --authorize-real-calls
```

[//]: # (ob:8a9e8051)
Both phases require the explicit payable-call flag. Track A currently passes the
non-payable local preflight with Claude Code 2.1.234. Track B and the policy judge use
`AI_GATEWAY_API_KEY`; the worker adapter hard-pins `moonshotai/kimi-k3`, the policy
judge hard-pins `google/gemini-3-flash`, and neither permits provider fallback.

[//]: # (ob:4fa7f2a1)
The automated admission path is an experimental treatment, not a change to the
production Proofpress authority model. The LM recommendation is not legal truth.
Production deployments retain authorized human admission for ambiguous exceptions,
business risk appetite, and accountable approval; a later C3 ablation can measure
that operational workflow separately.

[//]: # (ob:5b8f65cd)
## Implementation plan

[//]: # (ob:8a77ef0b)
### Phase 1 — generalize RelayBench without rewriting it

[//]: # (ob:4ab38fb2)
- preserve the existing H4 stage controller, cold workspace boundary, parity audit,
  invalidation rules, record schemas, and deterministic scorer;
- add a Claude CLI adapter and a Vercel AI Gateway adapter behind the existing adapter
  contract;
- add a Proofpress C2 treatment adapter that executes the PR 34 lifecycle and exports
  only trusted-context output to the fresh receiver;
- add a Raw C1 adapter with the same model, task files, tool surface, and execution
  limits but no Proofpress context;
- add normalized-cost, cached-token, reasoning-token, retry, and treatment-overhead
  telemetry; and
- retain provider responses and failures in a non-publishable local run ledger.

[//]: # (ob:63139849)
### Phase 2 — Harvey LAB Contracts calibration

[//]: # (ob:22c33d19)
Select 1–3 public contract matters with version changes, reopened issues, and authority
boundaries. Run one excluded smoke pair, then paired C1/C2 calibration on Opus 4.8 and
Kimi K3. Inspect task-level regressions and receipts before setting the publishable
repeat count.

[//]: # (ob:17bd325a)
### Phase 3 — publishable Harvey pilot

[//]: # (ob:3d52df54)
Freeze task IDs, repeats, model routes, judge, evaluator, analysis, and exclusion
rules. Expand only after both tracks pass information parity and complete telemetry.
Report paired effects and the quality-cost-token-latency frontier, not a cherry-picked
aggregate.

[//]: # (ob:10fb9dd1)
## Extension tracks

[//]: # (ob:5962ad71)
### Track C — cross-family frontier robustness

[//]: # (ob:7b3602cb)
Add GPT-5.6 Sol through Vercel AI Gateway after the Harvey calibration. This track
tests whether the Proofpress effect transfers across model families. It is especially
useful because Harvey reports that changing the APEX harness improved some models and
regressed GPT-5.6 Sol, demonstrating the need to separate harness effects from the
Proofpress treatment.

[//]: # (ob:f3144a90)
### Track D — distillation and RLM ablation

[//]: # (ob:ff682143)
Use GLM-5.2 only after the basic handoff effect is established. Compare plain RLM,
RLM plus Proofpress governed context, and Proofpress with deeper distillation. This
track asks whether structured cumulative knowledge reduces repeated search and
delegation cost; it must not be pooled with the simpler handoff treatment.

[//]: # (ob:e671391a)
### Benchmark 2 — Redline Bench

[//]: # (ob:733aa604)
Redline Bench is the most natural second substrate because it already evaluates
multi-turn contract negotiation. Test operative-version selection, supersession,
rejected-path revival, authority boundaries, and document-native redlines while
retaining its standard Harbor harness and judge configuration.

[//]: # (ob:00ec02db)
### Benchmark 3 — APEX Agents Corporate Lawyer

[//]: # (ob:9b60dc96)
Use the canonical Archipelago environment and corporate-lawyer subset. Preserve the
official Gemini 3 Flash judge at low thinking and report Pass@1 over eight trajectories
when reproducing the published setup. Treat any direct-filesystem variant as a
separate harness ablation, because Harvey reports material model-dependent score
movement from that change.

[//]: # (ob:13a5bdcb)
### Benchmark 4 — PRBench and knowledge-scale work

[//]: # (ob:45b35915)
PRBench can test high-stakes professional reasoning after the agentic mechanism is
established. LAB Firm Knowledge or a bounded APEX knowledge workflow can later test
whether Proofpress distillation improves repeated work over large corpora. These are
new interventions and require separate preregistration; they are not automatic
extensions of the Harvey handoff result.

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
