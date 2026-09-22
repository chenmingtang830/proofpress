---
target: claim network prototype
total_score: 26
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 4
timestamp: 2026-09-21T16-35-37Z
slug: web-owner-src-claim-network-preview-tsx
---
# Claim Network Prototype UI/UX Critique

## Design Health Score

| # | Heuristic | Score | Key issue |
|---|---|---:|---|
| 1 | Visibility of system status | 3/4 | Selection and counts are visible; receipt activation previously had no feedback. |
| 2 | Match with real world | 3/4 | Governance language is strong; Nodes and Edges expose rendering mechanics. |
| 3 | User control and freedom | 3/4 | Reset and filtering are reversible; selection cannot be cleared. |
| 4 | Consistency and standards | 3/4 | Shared primitives are used, but page CSS duplicated their styling. |
| 5 | Error prevention | 2/4 | Enabled receipt buttons previously did nothing; dense mode reduces readability. |
| 6 | Recognition rather than recall | 3/4 | Sidecar helps; inactive relation meanings and unresolved state need explanation. |
| 7 | Flexibility and efficiency | 2/4 | Search and density controls exist; mobile relies on horizontal panning. |
| 8 | Aesthetic and minimalist design | 3/4 | Calm Boardroom Clarity language; the original header and toolbar lacked containment and gutter. |
| 9 | Error recovery | 2/4 | Empty-state recovery was incomplete and sidecar selection could become stale. |
| 10 | Help and documentation | 2/4 | Time direction is explained; arrow direction and relation status are not. |
| **Total** |  | **26/40** | **Promising concept with an incomplete inspection contract.** |

## Design Specificity Verdict

The recorded-time claim graph, persistent inspector, institutional palette, and governance vocabulary are recognizably Proofpress. The surface still behaves partly like a graph sandbox: arbitrary node and edge limits dominate the controls, relation state is under-explained, and the densest/mobile states trade comprehension for fitting more circles.

The detector returned zero findings for the TSX target. That is not evidence of complete quality: browser and source inspection found structural, accessibility, and behavioral defects that the detector cannot infer.

## Overall Impression

The strongest idea is a stable chronological claim map with an inspection sidecar. The biggest weakness was trust at the moment of evidence inspection: Open receipt looked actionable but produced no result. The header, toolbar, graph, and footer also lacked a common page gutter, making the surface feel attached to the sidebar instead of composed within the workspace.

## What's Working

- Selecting a claim does not rearrange the graph, preserving spatial memory.
- Claim details live in a persistent sidecar rather than a transient tooltip.
- Shared Input, NativeSelect, Label, and Button primitives form the interaction layer.

## Priority Issues

### [P1] Receipt inspection was a dead end

Enabled Open receipt buttons had no handler, destination, disabled state, or feedback. This damaged trust at the exact point users sought provenance. Fix: open a receipt detail in the same sidecar and provide a clear return path.

### [P1] Workspace hierarchy lacked a content gutter

The title and toolbar began directly beside the sidebar rule, while local CSS redrew shared controls. Fix: add one page frame with canonical horizontal padding; treat the toolbar as one grouped control surface and let the shared components own their input geometry.

### [P1] Individual SVG claims were absent from Chrome's accessibility tree

The graph appeared as one image even though SVG groups carried button roles. Fix: expose an equivalent accessible claim-selection list, communicate selected state, and keep live announcements concise.

### [P1] Mobile is still a desktop canvas inside a scroller

At 390px the 900px SVG requires horizontal panning while the sidecar is below it. Fix: use a claim-centered chronological relation list on mobile; keep the full map optional.

### [P2] Relation semantics remain under-explained

Dashed violet unresolved edges have no textual legend, and inactive relation labels are hidden. Fix: expose admitted versus unresolved relation state and an accessible relationship list without adding another verbose panel.

### [P2] Controls describe graph mechanics, not owner intent

Nodes and Edges are useful prototype controls but not production information architecture. Fix: in production, prioritize scope, date, relation type/state, and a claim-centered neighborhood; keep density as a secondary projection control.

## Persona Red Flags

- **Workspace steward:** reached Open receipt and received no response; confidence collapsed at the proof boundary.
- **Keyboard or screen-reader user:** received one aggregate graph image instead of discoverable claim choices and relation semantics.
- **Mobile owner:** must pan a wide canvas and then scroll to a detached inspector.

## Minor Observations

- Search should match scope and evidence, not only statement/title.
- Empty-state copy referenced an applicability filter that did not exist.
- Relationship totals can exceed the relations currently drawn without explanation.
- The selected claim can disappear under filtering while its stale sidecar remains.
- Year and meaning of timeline dates should be explicit when real data replaces fixtures.

## Questions to Consider

- Is the production job to browse a graph, or to trace why one current claim can be relied on?
- Should unresolved relations be visible by default or explicitly opted into?
- On mobile, would a chronological relationship list answer the task better than a miniature graph?
