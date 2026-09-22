---
target: Owner Review journey and dead ends
total_score: 24
max_score: 40
na_heuristics:
p0_count: 0
p1_count: 3
timestamp: 2026-09-22T21-54-52Z
slug: web-owner-src-main-tsx
---
# Proofpress Owner Review critique

Target: `web/owner/src/main.tsx` in `codex/review-judge-retry-flow`. Mode: Operate. Method: independent design assessment and detector/browser assessment.

## Design health

| # | Heuristic | Score | Key issue |
|---|---|---:|---|
| 1 | System status | 3 | Model status can remain visible after a different claim is selected. |
| 2 | Real-world match | 3 | Blocked candidates appear under Decision history despite no human decision. |
| 3 | User control | 2 | Blocked candidates have no direct correction handoff. |
| 4 | Consistency | 3 | Authority layers are consistent on the happy path. |
| 5 | Error prevention | 3 | Approval confirmation and policy guard are clear. |
| 6 | Recognition | 2 | Recovery from failed checks and stale advice requires interpretation. |
| 7 | Efficiency | 1 | Item-by-item review has no visible triage accelerator. |
| 8 | Minimalism | 3 | Progressive disclosure works, though actions accumulate. |
| 9 | Error recovery | 2 | Model retry exists; blocked correction is poorly routed. |
| 10 | Help | 2 | Inline advice is useful; remediation guidance is uneven. |
| **Total** | | **24/40** | **Acceptable** |

## Design specificity and evidence

The interface is specific to Proofpress: deterministic checks, advisory model review, and owner authorization are visibly distinct. The claim, applicability, evidence, and receipt language support governance rather than a generic approval dashboard. The detector returned `[]` (zero findings, exit 0) for the target; this did not catch the workflow problems. An isolated offline browser fixture confirmed that the manual model review path can complete. At desktop width, the owner decision card is visible in the right column before the Evidence/Checks/History tabs lower on the left. Mobile browser inspection and live detector overlays were unavailable because the in-app browser did not support viewport control or DOM mutation. No user-visible overlay was created.

## What works

- The three authority layers and approval confirmation make the consequential human act explicit.
- Bound evidence, applicability, model rationale, and history remain inspectable in full review.
- The model processing dialog discloses the provider, possible charges, and advisory role; the offline happy path completed.

## Priority issues

1. **P1: Blocked checks are filed as a human decision.** `queueFor` maps `blocked` to `decided` (`main.tsx:1195`); the inspector says View decision although no human decision occurred (`main.tsx:1429`). Failed checks hide review actions (`main.tsx:1396`, `1451`). Give blocked candidates a named correction queue, exact failed requirements, and a copyable agent handoff to create a corrected candidate. Suggested command: `$impeccable harden`.
2. **P1: Model status can follow the wrong claim.** `judgeMessage` is global and remains when `choose` changes selection (`main.tsx:303`, `709-717`, `1089`). Bind the status to claim ID and name, or clear it on selection. Suggested command: `$impeccable clarify`.
3. **P1: Approval immediately advances without a receipt.** The admit path calls `load(nextPending)` immediately (`main.tsx:797-800`). Show the recorded approval, its current eligibility, and View receipt / Review next actions before advancing. Suggested command: `$impeccable harden`.
4. **P2: Decision appears before evidence detail.** Desktop browser inspection found the decision card in the right column while evidence tabs sit lower in the left column (`main.tsx:1487-1570`). Put an evidence summary and review checklist adjacent to the decision, or make the decision a deliberate final section after the evidence. This is an observed design risk, not a confirmed functional dead end. Suggested command: `$impeccable layout`.
5. **P2: A failed replacement model run may be masked by older advice.** `judgeFailed` requires no recommendation (`main.tsx:1404`), hiding job failure detail and Retry when a previous recommendation remains (`1450-1464`). Confirm the API's replacement-job behavior; if it retains prior advice, show Previous advice and Latest attempt failed separately. Suggested command: `$impeccable harden`.

## Personas and cognitive load

- **Power user:** One claim at a time with no visible triage accelerator; approval immediately advances without a receipt to inspect.
- **First-timer:** A blocked candidate under Decision history falsely implies a decision was made; View decision gives no correction path.
- **Accessibility-dependent user:** A claim-free global status announcement can describe a different selected claim; the native button in each queue row does preserve keyboard selection.

The primary journey is chunked well into checks, advice, and owner authority. Cognitive load rises around blocked checks and stale advice because the user must infer the next actor and next action. The emotional low point is a blocked candidate mislabeled as decided; the approval ending is abrupt.

## Questions to consider

- Should a failed deterministic check create an explicit handoff to the proposing agent, with the exact failed requirements?
- What minimum approval receipt should appear before the owner chooses Review next?
- Should previous model advice remain visible when a new attempt fails, and how should its age be labeled?
