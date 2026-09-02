[//]: # (ob:ae580676)
# Proofpress Design System — Verified Knowledge Ledger

[//]: # (ob:4565936e)
**Status (2026-09-01):** Current cross-interface guidance for Proofpress CLI, Markdown receipts, review surfaces, lineage views, governed-context projections, and the hosted owner AKMS chrome. Product hosts may supply their own brand shell and workflow vocabulary, but Proofpress trust states and evidence semantics must remain recognizable and consistent.

[//]: # (ob:9787677e)
## Overview

[//]: # (ob:e21f2b5d)
In one phrase: **a paper-and-ink ledger**. A paper-colored surface, ink-colored text, and one cyan-blue accent govern interaction. Semantic colors describe verification and review state; they are never decoration.

[//]: # (ob:6ba0b871)
Proofpress interfaces make one boundary legible: evidence and model recommendations can support a candidate conclusion, but only policy-compliant human admission makes it governed knowledge. Information density serves that decision. Show the conclusion before its machinery, the evidence bundle before raw sources, and pending work before completed work.

[//]: # (ob:ca5dbbae)
The design system is workflow-neutral. A legal product may organize work by organization, matter, and data room; a research product may organize it by project, run, and artifact. Those host structures are not Proofpress primitives. Proofpress owns the visual language for evidence, candidate conclusions, review receipts, admission state, trusted context, and lineage between them.

[//]: # (ob:ab42e61c)
**The Trust Boundary Rule.** A surface must never imply that retrieval, deterministic integrity, a model recommendation, or staging alone authorizes reliance. Governed context begins only after the configured admission gate succeeds.

[//]: # (ob:730432c3)
## Feeling

[//]: # (ob:beafea83)
Proofpress should feel like a bound volume with a cyan seal: paper you can sit with, a stamp you can trust, knowledge worth building on. It is archival, not ornamental; quiet, not empty. A reviewer should feel they are examining a record, not operating a dashboard.

[//]: # (ob:532d94f7)
The hosted owner workspace is a steward's desk over that ledger. Home and Ask Proof Press are how a human orients; they are not how knowledge becomes governed. Cyan is the seal and the interaction, never a substitute for admission.

[//]: # (ob:66d5152d)
Do not optimize for "looks like a 2026 AI product." Optimize for this: a future agent or human can tell, in one glance, what they may rely on, why, and under whose authority.

[//]: # (ob:6af4c951)
## Hosted owner chrome

[//]: # (ob:fa9a96d3)
The hosted owner IA is frozen as of 2026-09-01. Do not subtract these surfaces:

[//]: # (ob:4ffeef89)
- **Home** — orientation and Ask Proof Press entry; not a KPI dashboard
- **Review** — governance inbox
- **Ledger** — current authoritative knowledge
- **Activity** — consumption receipts
- **Admin** — principals, credentials, policy
- **Ask Proof Press** — persistent context-aware clerk

[//]: # (ob:0605066b)
Admit is the lifecycle verb. Approve is the owner-chrome label for that same decision; the control must keep `data-decision="admit"`. The assistant may explain, query, navigate, and draft a bounded clarification request. It must never admit, reject, or appear to.

[//]: # (ob:343a8d41)
A host may keep Home and Ask Proof Press. Those surfaces are chrome around the ledger, not a second authority.

[//]: # (ob:03c75a58)
## AI-tell denylist

[//]: # (ob:7097ec6f)
These patterns make Proofpress look like generic AI software and hide the trust boundary. They are defects, including when a host is exploring:

[//]: # (ob:b42cc176)
- Decorative gradients, glow, glassmorphism, or aurora backgrounds. Paper is flat.
- Inter, Geist, or other default AI-product sans as the narrative voice. Georgia carries knowledge prose; system sans operates controls.
- KPI tiles, sparkline dashboards, or metrics-that-look-important as Home.
- Sparkle, magic-wand, or ✦ as a mark of authority. A host may use a small mark on the Ask Proof Press toggle; it must never sit on Admit/Approve, a status chip, or a candidate conclusion.
- Green, red, or orange used for decoration, generic success, or visual variety.
- **Draft** as a Proofpress lifecycle term. A proposal is a **candidate**. Draft belongs to documents, not admission state.
- Copy that treats Ask Proof Press, a model recommendation, or a passing check as admission.
- Linear or ChatGPT chrome: infinite chat as the product, stacked elevated cards, gradient pills, or confidence percentages as authority.
- Image generation or video generation as product UI. Trust states must remain recognizable without generated atmosphere.

[//]: # (ob:a83b0b86)
## Design critic protocol

[//]: # (ob:007d1f14)
When an agent proposes visual work, run a critic against screenshots only. Do not put the stop criterion in the critic prompt.

[//]: # (ob:bea9a7b3)
**Taste bar.** Would this still look like Proofpress if the logo were covered? Paper, ink, one cyan seal, Georgia for knowledge, system sans for controls, monospace for proof. If it could be a generic AI workspace, it fails.

[//]: # (ob:b93e40e3)
**Trust bar.** Can a stranger point to the candidate, the evidence, the checks, the advisory recommendation, and the human decision — and see that only the last one admits? If Ask Proof Press, a green check, or a cyan glow could be mistaken for admission, it fails.

[//]: # (ob:40d605db)
**References.** Use the brand-film stills and the hosted owner surfaces as the visual references, not a moodboard of other products.

[//]: # (ob:5e18e46f)
**Output.** Numbered findings, each with a screenshot crop description, the rule it violates, and a concrete fix. Separate taste misses from trust-boundary misses. Do not congratulate. Do not invent a new IA.

[//]: # (ob:715fe0fc)
The human, not the critic, decides when to stop. A critic that is also asked "are we done?" will say yes.

[//]: # (ob:7056876e)
## Colors

[//]: # (ob:451376f2)
| Token | Light | Dark | Use |
|---|---|---|---|
| paper | #FAF9F5 | #15171C | Page and graph-canvas background |
| ink / ink-2 / ink-3 | #20222B / #5A5D6B / #8B8E9C | #E9E7E0 / #A6A9B4 / #787B87 | Primary / secondary / indexed metadata |
| line | #E3E1D9 | #2C2F38 | Rules, connectors, and inactive boundaries |
| card / wash | #FFFFFF / #F1EFE8 | #1D2027 / #22252D | Working surfaces / quiet inspector and hover wash |
| accent / accent-soft | #0E5E6F / #E3EEF0 | #5FB3C4 / #173741 | Proofpress, edit, selection, modified, interaction |
| add / add-bg | #2E7D4F / #E7F2EA | #6FBF8E / #1B3226 | Verified checks, admitted knowledge, active governed context |
| del / del-bg | #B4453A / #F7E9E7 | #C87E82 / #3A2320 | Rejected, invalid, blocked, removed |
| move / move-bg | #8A6210 / #F5EEDC | #D7B56D / #332B18 | Needs review, why, moved, attention without alerting |

[//]: # (ob:a8d606fe)
The launch film remains the canonical palette for dark UI: white `#EAE8E0` carries primary content, cyan `#5FB3C4` carries Proofpress and interaction, orange `#D7B56D` carries why or review attention, red `#C87E82` carries rejected or blocked, and green `#6FBF8E` is reserved for verified or admitted. Adjacent diff states use the same meanings: modified is cyan, moved orange, removed red, and added green. Both themes must be proofread.

[//]: # (ob:b5b71caf)
**The State, Not Brand Rule.** Green, red, and orange communicate ledger state. Do not use them for decorative emphasis, generic success, or visual variety. Cyan may identify Proofpress and interactive selection, but it cannot make a candidate appear admitted.

[//]: # (ob:eeee2405)
The fixed fallback mapping for GitHub PR comments is `🔵 mod`, `🟣 mov`, `🔴 del`, and `🟢 new`. Blue is the closest GitHub emoji equivalent to the cyan accent; purple deliberately replaces yellow for moved, so an ordinary move is not misread as a warning. `branding.color: blue` in GitHub Action metadata controls only the action icon background in Marketplace/Actions lists; it does not control PR comments.

[//]: # (ob:f49db722)
## Typography

[//]: # (ob:53b8c3a4)
- **Document headings:** Songti SC / Noto Serif SC with Georgia / Times New Roman fallbacks, 900 weight, up to 2rem. Serif establishes the artifact or proposition being examined; it is not applied to every interface heading.
- **Brand narrative and knowledge prose:** Georgia with Times New Roman and serif fallbacks, 15–18px / 1.65–1.8 for sustained reading. This is the default voice for taglines, manifestos, editorial passages, quotations, source-document prose, and brand-film language. Use regular weight and restrained tracking; the type should feel authored, mature, and archival rather than ornamental.
- **Controls and operating surfaces:** native system sans-serif stack, 12–15px / 1.5–1.7. Keep buttons, navigation, filters, tables, inspectors, and dense review mechanics sans-serif so actions remain fast to scan.
- **Versions, hashes, locators, lane labels, and receipts:** `ui-monospace`, SFMono-Regular, Menlo, monospace with `tabular-nums`; 10px labels may use restrained uppercase tracking.

[//]: # (ob:877970b3)
**The Document, Then Interface Rule.** Georgia gives brand narrative, source material, and important propositions an authored, archival gravity. Display serif establishes titles. Sans-serif operates the product. Monospace indexes the proof. Do not set controls in Georgia, turn metadata into body prose, or render long claims in monospace.

[//]: # (ob:46a56fa1)
## Layout

[//]: # (ob:8aa0ba5a)
- **Focused review:** single reading column with a maximum width of 760px and body lines no wider than 70 characters. Use the order navigation → metadata → conclusion → recommendation and checks → evidence → decision.
- **Review with a human gate:** a flexible reading column may pair with a fixed 320–344px decision or receipt panel. Keep the conclusion and its evidence visually dominant.
- **Local lineage:** a bounded canvas may pair with a 300–320px inspector. Read left to right as Bound Evidence → Candidate Conclusion → Governed Context. Use a subtle 21px dot grid only when it materially improves spatial orientation.
- **Responsive:** below approximately 820px, stack reading and decision surfaces. Replace decorative graph connectors with a vertical evidence → conclusion → context sequence; preserve state and keyboard order.
- **Rendered artifacts:** Markdown tables, lists, bold text, code, and citations must render as content. Exposed raw markup is a defect.

[//]: # (ob:0855c398)
**The Reading Order Rule.** Orientation → proposition → support → decision → receipt. Progressive disclosure may reveal more detail, but it must not reorder the trust argument.

[//]: # (ob:d364c4d7)
## Elevation & Depth

[//]: # (ob:6a736e61)
Proofpress is flat by default. Hairline rules, paper/card contrast, and quiet washes establish hierarchy. Reserve small shadows for sticky decision surfaces, selected-node emphasis, floating contextual assistance supplied by a host, and literal source-document paper. Do not give every evidence block or graph node its own floating card shadow.

[//]: # (ob:bf7362b0)
Node selection may use a two-ring cyan focus halo without changing node dimensions. Hover may translate an interactive lineage node by at most 2px and must be disabled under reduced-motion preferences.

[//]: # (ob:196e567f)
**The Ledger, Not Dashboard Rule.** Structure comes from indexing, rules, reading order, and receipts—not layers of elevated cards, telemetry tiles, or decorative gradients.

[//]: # (ob:8b46fd18)
## Shapes

[//]: # (ob:5eb7133d)
Records, tables, evidence rows, and source material remain rectilinear. Use 7–8px radii for controls and compact graph nodes, 10px for bounded recommendation surfaces, 12px for a decision panel or the outer lineage workspace, and full pills only for status chips or a host-supplied floating assistant.

[//]: # (ob:6bb05de6)
Connectors are two-pixel paths with no arrowheads unless direction would otherwise be ambiguous. Evidence-to-conclusion connectors are quiet solid rules. Candidate-to-context connectors encode the admission boundary: gray dashed while pending, red dashed while blocked or rejected, and solid green only after admission.

[//]: # (ob:54961ec9)
**The Visible Boundary Rule.** The connector, destination node, inspector copy, and available action must agree. Never draw a solid path into governed context while the conclusion is pending, blocked, rejected, expired, superseded, or awaiting revision.

[//]: # (ob:f43f7a30)
## Components

[//]: # (ob:0287d639)
- **Status chip:** compact monospace pill. Admitted/current is green; needs review or revision is orange; blocked/rejected is red; agent or interactive scope is cyan. Never express authority through confidence percentages.
- **Diff tag:** compact inline marker. New is green, modified cyan, removed red, and moved orange.
- **Evidence bundle:** the reviewable support unit for a conclusion. Summarize its bound evidence blocks and source count; do not present the bundle as a raw file.
- **Evidence block row:** filename or artifact identity, verified locator, bounded quotation, integrity state, and a clear route to the immutable source. Use a bottom rule instead of an independent promotional card.
- **Candidate conclusion:** state, proposition, evidence count, recommendation, and material impact. Its review state must remain distinct from deterministic integrity and model evaluation.
- **Review panel:** presents recommendation, deterministic checks, evidence sufficiency, and explicit Approve / Request changes / Reject consequences. Keep the human decision available without obscuring the record.
- **Admission receipt:** replaces decision controls after approval and records reviewer, decision, ledger head or version, timestamp, and append-only history. A success message without projected ledger state is incomplete.
- **Governed-context projection:** contains only admitted and currently applicable knowledge. Blocked, pending, rejected, expired, superseded, and needs-revision conclusions may remain auditable but must not appear available to downstream consumers.
- **Source viewer:** preserves original identity, digest, locator, and citation highlight. Moving from evidence to source must preserve orientation and provide a clear return path.

[//]: # (ob:c8ecfb15)
### Local Lineage Workspace

[//]: # (ob:4495ce20)
A lineage view is an inspectable trust path, not a free-form network graph. Default to the selected conclusion's local provenance. Bound evidence nodes converge into the candidate conclusion; the final edge crosses the human-admission boundary into governed context.

[//]: # (ob:a9b6733b)
Clicking or keyboard-activating a node first updates a persistent inspector with node type, identifier, state, integrity or receipt information, and one explicit next action. Evidence opens the bound excerpt before the raw source. A candidate opens review or history. Governed context opens the exact downstream projection only when admitted; while pending it remains inspectable but visibly unavailable.

[//]: # (ob:f4762698)
**The Local Lineage Rule.** Render the smallest graph that answers “why can this conclusion be trusted?” Expand through selection, filtering, or a separate ledger projection—not by loading the entire knowledge graph into the default canvas.

[//]: # (ob:0bd4799e)
### Review State Machine

[//]: # (ob:7578205b)
The canonical review states are candidate / needs review → admitted, needs revision, rejected, or blocked. A revised conclusion is a new version with preserved lineage; it is not a silent edit of the reviewed proposition. Only an admitted, current conclusion may enter governed context.

[//]: # (ob:aae4f716)
Every mutation must produce immediate, consistent feedback: disable duplicate submission, show loading and error state, record the receipt, advance the visible ledger head or version, and project the result through the queue, conclusion, lineage, history, and context views. Plain-language copy must state what happens next. For example: “The proposer will receive this request; the current conclusion remains excluded until a revision is reviewed.”

[//]: # (ob:bcd36484)
### Review and Diff Patterns

[//]: # (ob:03c0628e)
- **Change block:** use a three-pixel semantic edge and a light wash. Put word-level changes inside a collapsed disclosure so the document remains readable.
- **Comment card:** use a semantic edge, card surface, and quiet status copy such as “Awaiting response,” “Recorded · awaiting revision,” or “Resolved.”
- **Block hover:** reveal a wash surface and an explicit Comment affordance. Clickability must never depend on hover alone.
- **Decision bar:** when a focused single-column review needs persistent actions, use a sticky bottom bar with solid green Approve and solid cyan Request changes. State must change immediately after submission to prevent repeated action without feedback.

[//]: # (ob:e693f5e3)
### Voice and Language

[//]: # (ob:300ee19f)
Use product-facing trust terms: Source, Evidence, Candidate Conclusion, Review, Admit, Request changes, Reject, Receipt, Ledger, Lineage, and Governed Context. Reserve storage or implementation terms such as event, ref, blob, projection algorithm, and lock for developer diagnostics. Host chrome may label Admit as **Approve**; the lifecycle event, API, and `data-decision` value remain `admit`.

[//]: # (ob:cab7f711)
English is the source language for UI strings, CLI output, and documentation surfaces. Interfaces may adapt through `Accept-Language`, with Chinese as the first locale. Stable Proofpress vocabulary—especially Evidence, Conclusion, Review, Admit, Receipt, Ledger, Lineage, and Governed Context—must retain one documented mapping across locales and host products.

[//]: # (ob:b01d87ba)
## Do's and Don'ts

[//]: # (ob:df1fade1)
### Do

[//]: # (ob:3ba94c8c)
- **Do** preserve progressive disclosure from conclusion to evidence bundle to bound excerpt to immutable source.
- **Do** keep deterministic integrity, model recommendation, policy outcome, and human admission visibly separate.
- **Do** make selected graph nodes keyboard-operable and expose the same receipt information without relying on color alone.
- **Do** project a recorded admission consistently across review, ledger, lineage, history, and governed context.
- **Do** let a host product apply its own brand shell while retaining Proofpress trust-state semantics.
- **Do** keep the hosted owner chrome as Home, Review, Ledger, Activity, Admin, and Ask Proof Press; do not subtract those surfaces.
- **Do** fail closed: unavailable data or invalid lineage must render as blocked or not ready, never as a plausible placeholder.

[//]: # (ob:70e00445)
### Don't

[//]: # (ob:755d7400)
- **Don't** treat evidence as synonymous with a raw source file.
- **Don't** use an unbounded force-directed graph as the default ledger view.
- **Don't** show pending, blocked, rejected, expired, superseded, or needs-revision knowledge as available to an agent or API.
- **Don't** make evaluation metrics, model confidence, or recommendation the visual equivalent of admission.
- **Don't** treat Ask Proof Press, a passing check, or a cyan glow as admission.
- **Don't** use Draft as a Proofpress lifecycle term for a candidate conclusion.
- **Don't** use Inter as narrative type, decorative gradients, or KPI tiles as the Home metaphor.
- **Don't** bake legal-specific matter, counsel, or data-room concepts into Proofpress core components.
- **Don't** expose mock counts, synthetic receipts, or hardcoded lineage without an explicit preview label.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2QwZDM3MjMwYTVmODdkNzA3YTMzOTc2NiIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
