---
target: web/owner/src/main.tsx
total_score: 36
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 0
timestamp: 2026-09-15T09-40-52Z
slug: web-owner-src-main-tsx
---
Method: dual-agent (A: /root/ui_design_assessment · B: /root/ui_detector_assessment)

## Design Health Score

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | 4 | Review and policy states are explicit. |
| 2 | Match System / Real World | 4 | Governance language maps cleanly to owner decisions. |
| 3 | User Control and Freedom | 3 | Long Admin work still lacks a local section index. |
| 4 | Consistency and Standards | 4 | Auth and signed-in typography now share one visual language. |
| 5 | Error Prevention | 4 | Consequential decisions and credential actions are bounded. |
| 6 | Recognition Rather Than Recall | 4 | Labels expose evidence, applicability, advice, and authority. |
| 7 | Flexibility and Efficiency | 3 | Activity history remains costly to scan on mobile. |
| 8 | Aesthetic and Minimalist Design | 4 | Calm institutional hierarchy without dashboard theater. |
| 9 | Error Recovery | 3 | Auth recovery is documented, but still requires an administrative shell. |
| 10 | Help and Documentation | 3 | Inline boundary copy is strong; long forms need more orientation. |
| **Total** | | **36/40** | **Excellent** |

## Design Specificity Verdict

The signed-in workspace feels authored for Proofpress: thin indexed rules, restrained teal, mono proof metadata, and the Evidence to Claim to Reuse Boundary sequence form a coherent institutional ledger. The login surface now uses the same sans-serif voice and explains owner recovery. The deterministic detector reported zero findings in `web/owner/src/main.tsx`; no false positives were observed. Browser overlays were unavailable, so authenticated synthetic screenshots and a fresh local browser login were used as the visual fallback.

## Overall Impression

The release-blocking mobile navigation defect is fixed. Six destinations now remain in one fixed row at 390px, content clears the safe-area-aware footer, and Review filters form an intentional 2 plus 1 layout. The interface is production-ready; the largest remaining opportunity is reducing scan cost in long operational records.

## What's Working

- Home keeps the pending human decision dominant and avoids decorative metrics.
- Review separates deterministic checks, advisory LM output, and Human Approval into distinct surfaces.
- Knowledge lineage makes Evidence to admitted Claim to Reuse Boundary immediately understandable.

## Priority Issues

1. **[P2] Mobile Activity is a long audit wall.** Exact facts are preserved, but repeated rows make local scanning expensive. Group by day or action and add an optional compact density. Suggested command: `$impeccable optimize`.
2. **[P2] Mobile Admin lacks local orientation.** The form is long and consequence-heavy. Add a section index or staged headings with persistent save/status context. Suggested command: `$impeccable layout`.
3. **[P3] Knowledge constraints are quieter than availability.** Validity conditions should be at least as perceptually salient as the green Available badge. Strengthen hierarchy without turning constraints into an alarm. Suggested command: `$impeccable clarify`.

## Persona Red Flags

- **Busy owner on mobile:** Primary navigation is now stable, but Activity history still requires excessive scrolling to find a prior action.
- **Security-conscious operator:** Login now states how access is created and recovered; Admin still asks the operator to retain context across a long policy form.
- **First-time reviewer:** Trust boundaries are clear, but a green Available badge can be internalized before the quieter validity conditions are read.

## Minor Observations

- The Review empty state intentionally leaves space on desktop; this is calm rather than broken, but could become more useful with recent-decision context later.
- Decision-note copy correctly states that a note is required only for reject or request changes, and the accessibility metadata no longer falsely marks it required for approval.

## Questions to Consider

- Should Activity optimize for forensic completeness by default, or offer a compact operator view first?
- Which Admin section is most frequently revisited after initial setup?
- Should validity conditions precede the Available badge on narrow screens?
