[//]: # (ob:ae580676)
# Proofpress Design System — Verified Knowledge Ledger

[//]: # (ob:4565936e)
**Status (2026-09-01):** Current cross-interface guidance for Proofpress CLI, Markdown receipts, review surfaces, lineage views, governed-context projections, and the hosted owner AKMS chrome. Product hosts may supply their own brand shell and workflow vocabulary, but Proofpress trust states and evidence semantics must remain recognizable and consistent.

[//]: # (ob:678e1b70)
[//]: # (ob:hosted-workspace-v2)

[//]: # (ob:9368ad00)
## Hosted Workspace V2 direction

[//]: # (ob:efc880ec)
The owner workspace uses a compact, three-part operating frame: a 224px navigation rail, a flexible primary work surface, and a 384–416px contextual inspector. At desktop widths the selected row and its inspector remain visible together; on smaller screens the inspector becomes a sheet. This spatial contract is the benchmark for Home, Review, Ledger, Activity, Admin, and Ask Proofpress.

[//]: # (ob:cfee6f69)
Hosted Workspace V2 adopts the reference dashboard's **information architecture only**: density, three-part composition, persistent selection, and contextual inspection. The reference screenshot is not a palette, typography, logo, or component-skin specification. Its visual world remains canonical Proofpress: warm paper, near-black ink, quiet warm-gray rules, and one cyan seal. Georgia carries the proposition and source prose; the native system sans operates navigation, filters, tables, and controls. It does not inherit another product's cool-blue palette, typography, logo treatment, or legal-matter vocabulary.

[//]: # (ob:06711fc4)
Use shadcn primitives as accessible construction material, not as a visual preset. Reduce their default radius and shadow, keep one consistent control height, and build hierarchy primarily with type, alignment, and rules. A component that looks recognizable as an unmodified starter-kit component is unfinished.

[//]: # (ob:bd3d4bba)
The desktop reference viewport is 1536×1024. The primary table begins on the same vertical axis as its title and filter row; the contextual inspector begins at the application header and owns its own scroll. Selection is expressed through the canonical accent-soft wash and a one-pixel cyan marker, never a glow. The mobile reference viewport is 390×844, where tables become structured records and the decision controls form a safe-area-aware bottom bar.

[//]: # (ob:c3130a45)
Hosted Workspace V2 does not define a second palette. It uses the canonical tokens below: paper `#FAF9F5`, card `#FFFFFF`, ink `#20222B`, secondary ink `#5A5D6B`, line `#E3E1D9`, accent `#0E5E6F`, and accent-soft `#E3EEF0`. Green and red remain reserved for admitted and rejected terminal state. Pending review and model recommendation remain neutral ink on wash.

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
The hosted owner workspace is a steward's desk over that ledger. Home and Ask Proofpress are how a human orients; they are not how knowledge becomes governed. Cyan is the seal and the interaction, never a substitute for admission.

[//]: # (ob:66d5152d)
Do not optimize for "looks like a 2026 AI product." Optimize for this: a future agent or human can tell, in one glance, what they may rely on, why, and under whose authority.

[//]: # (ob:6af4c951)
## Hosted owner chrome

[//]: # (ob:fa9a96d3)
The hosted owner IA is frozen as of 2026-09-01. Do not subtract these surfaces:

[//]: # (ob:4ffeef89)
- **Home** — orientation and Ask Proofpress entry; not a KPI dashboard
- **Review** — governance inbox
- **Ledger** — current authoritative knowledge
- **Activity** — consumption receipts
- **Admin** — principals, credentials, policy
- **Ask Proofpress** — persistent context-aware clerk

[//]: # (ob:0605066b)
Admit is the lifecycle verb. Approve is the owner-chrome label for that same decision; the control must keep `data-decision="admit"`. The assistant may explain, query, navigate, and draft a bounded clarification request. It must never admit, reject, or appear to.

[//]: # (ob:343a8d41)
A host may keep Home and Ask Proofpress. Those surfaces are chrome around the ledger, not a second authority.

[//]: # (ob:03c75a58)
## AI-tell denylist

[//]: # (ob:7097ec6f)
These patterns make Proofpress look like generic AI software and hide the trust boundary. They are defects, including when a host is exploring:

[//]: # (ob:b42cc176)
- Decorative gradients, glow, glassmorphism, or aurora backgrounds. Paper is flat.
- Inter, Geist, or other default AI-product sans as the narrative voice. Georgia carries knowledge prose; system sans operates controls.
- KPI tiles, sparkline dashboards, or metrics-that-look-important as Home.
- Sparkle, magic-wand, or ✦ as a mark of authority. A host may use a small mark on the Ask Proofpress toggle; it must never sit on Admit/Approve, a status chip, or a candidate conclusion.
- Green, red, or orange used for decoration, generic success, or visual variety.
- **Draft** as a Proofpress lifecycle term. A proposal is a **candidate**. Draft belongs to documents, not admission state.
- Copy that treats Ask Proofpress, a model recommendation, or a passing check as admission.
- Linear or ChatGPT chrome: infinite chat as the product, stacked elevated cards, gradient pills, or confidence percentages as authority.
- Image generation or video generation as product UI. Trust states must remain recognizable without generated atmosphere.

[//]: # (ob:a83b0b86)
## Design critic protocol

[//]: # (ob:007d1f14)
When an agent proposes visual work, run a critic against screenshots only. Do not put the stop criterion in the critic prompt.

[//]: # (ob:bea9a7b3)
**Taste bar.** Would this still look like Proofpress if the logo were covered? Paper, ink, one cyan seal, Georgia for knowledge, system sans for controls, monospace for proof. If it could be a generic AI workspace, it fails.

[//]: # (ob:b93e40e3)
**Trust bar.** Can a stranger point to the candidate, the evidence, the checks, the advisory recommendation, and the human decision — and see that only the last one admits? If Ask Proofpress, a green check, or a cyan glow could be mistaken for admission, it fails.

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
| review / review-bg | #5A5D6B / #F1EFE8 | #A6A9B4 / #22252D | Candidate, needs review, advisory recommendation, and quiet attention |
| move / move-bg | #665A8A / #EFEDF5 | #AAA0D2 / #29263A | Moved content only; never review state or generic attention |

[//]: # (ob:a8d606fe)
The launch film remains a narrative reference, but the operating UI uses a quieter subset: white `#EAE8E0` carries primary content, cyan `#5FB3C4` carries Proofpress and interaction, neutral ink carries pending review and advisory recommendation, red `#C87E82` carries rejected or blocked, and green `#6FBF8E` is reserved for verified or admitted. Moved content may use muted violet. Yellow/orange is not an interactive control, status, recommendation, or attention color in the hosted owner workspace. Both themes must be proofread.

[//]: # (ob:b5b71caf)
**The State, Not Brand Rule.** Green and red communicate terminal ledger state. Pending review and advisory recommendation are neutral because neither has authority; moved content is muted violet. Do not use semantic colors for decorative emphasis, generic success, or visual variety. Cyan may identify Proofpress and interactive selection, but it cannot make a candidate appear admitted.

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
- **Status chip:** compact monospace label. Admitted/current is green; needs review or revision is neutral ink on wash; blocked/rejected is red; agent or interactive scope is cyan. Pending and recommendation surfaces must not use yellow/orange. Never express authority through confidence percentages.
- **Diff tag:** compact inline marker. New is green, modified cyan, removed red, and moved violet.
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
- **Decision bar:** when a focused single-column review needs persistent actions, use a sticky bottom bar with solid green Approve, an ink-on-paper Reject control, and a cyan-outline Request changes control. Never use yellow/orange for a decision. State must change immediately after submission to prevent repeated action without feedback.

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
- **Do** keep the hosted owner chrome as Home, Review, Ledger, Activity, Admin, and Ask Proofpress; do not subtract those surfaces.
- **Do** fail closed: unavailable data or invalid lineage must render as blocked or not ready, never as a plausible placeholder.

[//]: # (ob:70e00445)
### Don't

[//]: # (ob:755d7400)
- **Don't** treat evidence as synonymous with a raw source file.
- **Don't** use an unbounded force-directed graph as the default ledger view.
- **Don't** show pending, blocked, rejected, expired, superseded, or needs-revision knowledge as available to an agent or API.
- **Don't** make evaluation metrics, model confidence, or recommendation the visual equivalent of admission.
- **Don't** treat Ask Proofpress, a passing check, or a cyan glow as admission.
- **Don't** use Draft as a Proofpress lifecycle term for a candidate conclusion.
- **Don't** use Inter as narrative type, decorative gradients, or KPI tiles as the Home metaphor.
- **Don't** bake legal-specific matter, counsel, or data-room concepts into Proofpress core components.
- **Don't** expose mock counts, synthetic receipts, or hardcoded lineage without an explicit preview label.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2QwZDM3MjMwYTVmODdkNzA3YTMzOTc2NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImRkNzFjY2MyIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83NDk3MWE1YmYzODM3MGQ1ZTA2ZTc2ZGIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzVhYzNmNWQ2NmJlY2FlYzBlM2Y4YjQ3YyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtfetu5EiW3qsQasCzLmeqeL-oYAxUVaqewvT0NKp6ZmFMN0pBMpjJFZPMJZlSaXsamF9-AO8A-2eNBWzAT2DD_71v0k_gR_A5Jy6MTKVYJan3YjsaM91SihmMy4lzP-f74YT1Y12xYvxQlydnJ9vth9Itg8QPXBZVaVImbsKCIEvi-GRxknfl7YeyXvFhhGeHNfOj-IylMQvzqPCKKk8rXqV5mFYei3PuV1UexXnsuX7ISpYFXlr4iZ9WVRWFVciTxCvjHMYt66Hornl_e3L2A_4yfhjZCt7QsBFftYAfct7AB7_nfV3VLG-40_Preqi71lnD811_6-S3zjd911Xbng8DfGfLiiu24riovY_77q84LHfX44DrcdwOZ8-fr-pxvctPi27zvFjzdlO3q5G1qzRwn-99u-d_vavh5w-7gfcfiq4deAt7MfY7_uPiZM0ZbmJZJl5RFP6J-OQDv6aHYHP5hyTMEo9FeRWkQeKWEXdjnsQl7sK260dc2oembjnMXJ1I8yFiRVBFZQx7WjBeuDzAXU4KsRw5uw8F2w67Bhbs4zyLri-Hk7M__HAiX__DCZxy1w_4k_gzLz_ksOV_ONm1V2130558D2tQ9IDr6Irh-euL92-__Pp0U54sHkQrbBz7Ot-NcEQfcjbUA1IMb6oPbICtGzmNtxvXXY8TuqpbHHK4HUa-gb-0bIMnpya2gK8OeNonZ-2uaWCaxRqOh4sF5k1XXMHTjEepGyf4djiZkX_ERUw04bzmQ71qnff0EuenP_3ZEfTES-fX8Br4mpwGK0ua3xaJjN_AJ184nz9Ow8sVd77Cf_cwyHi7xaUgJQBVnfy4mCYcRnGUBTH_J5jws2fvRzbuBucvfNePl262dL1_e_bsmfNq1_dAD07Rd8OwrOGtPRwpd1a7umQt_FB106S3rGd7M86SNImTZH_Gv4WrS6-d28AvHOOxmT3hvlf5eVQ--A1vW6drubNd92zgZ86zZ8zZsi3vl6wtYZ1XDp1L_-zZqXMu_1J0TdfDZg4zK45z5uZp4j14PsY56l0enA274jTPvNu1JQO-1fBVDbf-zIEvlhxPgLUz8ylYVOY5e_gJfLvmTikISlwzpx6cm66_qpruZtny3dizBvcGJsQaBxhLuStGmPCtM0cRLA99HnvFg-fz7BnO6Nt-N4zOS7UZ74CBnQKVnjvDTtDlBv_eAg_rnXqzbW6dcc3GmfkkgRsGfhHszecN5w0S2jyBTk_N0GfOWcVZ-uDxDXIY1t2uKZ0KvuQ0NdADE9TgXHfNbsOdGxBG8Flxy-CoOGvOZpYbBX6ZhVXy0Ong3q87IIPSAQYLm4uUMGxxx4EsmAN_uWF9-YsBaebKQelMO4-3aO62xGXkRX750Om87py2G51uO9ab-m-QCfXOdydN110NaouQjznnbxVhnn534vxWPj43IVaFRRbtX99fmQsv1n234Z8gjePfmCGTimUsi8vgKe-9c0Zvz_Fwqr77G946bHC6ypm4-6kjN3HY5WM_syVhBZRXpdlTprYE_voreAauKoqlrq9BpjAU9sC9SuccSMYgePhbf_uCJsecX3_zdppcA8rb3uTc2I3cmLTCR0_uvNzUI-7UCBvY1BUvbgvQGIGEc-BvWyCga67-TGMuxZgOqJkz-xaEAUvL8EmkdE4HSkz1ivOtg3t4ZMdOnW_hOa6YIFzInjszU3ODIolYlO5N7fztcuRNAxe4vaV9nifxI4_P0HfiZgkv4urRbwTihgVuQU3kfSvlokEyePXFzV9x2Nq6wKs_dNUIXGnuvoM0KgrvQAd8yLyWoHWBcgy0DESy6mHlQL3DwlmBlMR_g_q66fotWB2bBdC9w3Y9PO3kYG2sZugaJEYOesT-vKR-V_T1CAsEuhw7UEk-cU73fmnmtFw3Kb3KC5_49r9cI9-B_61Qg4RvbIFIBwcMsR1oDChBFk6_a1F2iUHZitUt0PtQzDEkEKkZS_LgibMDhYLBZYSj6FGF-EsSsiMcFAizGk5_IilTNauIDczNLgt4CCbX02dHqo6c3SvcRphYj2ZM72w70BGdsaPJFMAQQBkf-YJ-5ddzzNwtgWOW-ZNn945XvEf1c8Dp_Q7uJr4771F7rupmIzZxIGY17gmmOe2EeykPD7jEY2b329243Y04s693m5yj0l7B00DncDU5K9ZKaQJK47wFDYssnK0zp6wkXlRxtyqeODsS07sNaxck4egE6dsLYDgF6PSgZuPFgdMdxm6LKrYcfVzPzc6NYjC29hX9V2ixDJ_gEPqhWdPTC5K48h84-h-db7srWMsfna_q1XqE_75m_RX8Bwnmj9-1f1wul3v_h4-EsQXPfDFNiRwdBwwSCDmuHrpc3PyG7VqgAKLSnm-Q5QAltKyXXLxXpL1w8p04oA5mxOYufZQnXsGqB85G2DRoecO7vgZieIn3R1s1XyJt0g1CAi66zWbX1gU87Ix8jkFy-McP3egRe1PVH_GusKZBCQVidrsFUiD9-st6_NUud755RzNBKYdK0eX__oc__w9n05WXMxOqwqzME3-fer693XYgMLfr20_Q596DMzQaBXlaBCx8xFtQP33dFTtcliPHHtD98b5rV2PtvH_lPMcD6pz36FHB34mBfMm7fkaKp0mSJe6BpPq8GQnSUHNagIIHpPBWu180icAEVjVzVkC4g2C_zhyHDWMWxRXbV0q_Yrfd7lP6nn5o5gRSxtycReyBo-Puv4GVDrx0xIe49QOMTo5beg8QHRi7reLbG_ax3uw2zs2cbZBGURFk6QNnI3b-nXztb_sSmJHa7t8ahstP__E_SZ2m1r8Pu-12ZvfLIA6LsNy3vi8afi1G_DegrG2Jyc8dxLHnZ84kZkkQ89h7_DtN9QfMyQas-vwWZFXFds146vyK1T26oEGVaziIV2LfzwvWI8ua45kVTMzP3cdP7OuuBJuHN7ygb6CVBDQE1DHedMueiAZ9IhWSlrNmTUfUA8cPltfMxLws5lGcVI-fmCAh4dIVjP01G9Z5h3uiSOn92O-KcQeGGrBTTmb6xsEB759YmoNuVHr7BP1-Dfv9KRGvH5pjnxxkWBCUDxz9nQgdgO6JMhrVK-WX7Lsb-BU50tDtevTNgejqa1D9hdR1-lk_ag56Ko8fOJtXXdtyiluQDYyEsAWR1qDluB4E92g7-BtMDjdhcHZtg5Rd1nOzicIs9niRPXA2gg5-Xw_osb3rtcQ_FmrCqP2BztwKImu7WXEaVAkL3AP5vtl2LYrlT6p7xoNzRqCfJmUcZI94CzJ0GU8o1vUWuTkQ-Zahf7hrO-E3pCAdaLfofQHT4HkhIg0zDL1IeVHl3r5e81VXAEV9JWJgYMVJt-T8JoA4u_drc1pwmEUF992nTuDckTE7Bz8gD2oLd3_YAiVQtHIk2w9pdiHdYBXogktQwzZzvvUsj5MgyJ86vVdNXVwh-wSt74rfEt9awuHVyAHhY1CWkfNWdQ-T3G3R9EQNGtj-UM-SbRL78aE8fvj0JHfd-6K6Uu94W5LrGQTDBrRYuFIOKVvCGz2nw7t5GSZZtm9RvKOXChXd-Q0YjvC-T5HWPd-Z845FSeq7Uf6kV38rXAEdmgiN1KPAghSH0xtuAlBlW86B9clnUHGZ2xjGeFglXvyk2V1gvN7Z7KTyRGEa4ZrnTg3mRFmTEYQhcrj2qIZXMEc0Qs5mvS0F6lRpeGxuKHle11XlfCO9hp95cMe-N8cng8KN_ZQ_eQrINV9RnNqhsZFtSn1mjbdfCLIBZGeL3gAKG-MLGHCTGa7J4yyoogOH1O-7uhDf_gpeuMPEh09sztFvzGxL4Lqce1n1hNeik0CGb5Zg9SDrEYwRtnIznIFxhmrFwrmQGscC3WSSxmdDonkC9Ow9YWYXYJrUw1pFBaR-08hvkrn8u7forhMep1dfvXU6ckktZm9a7nplmuT79tPr7hfCjfa6a3_xSel-9-mZMyorr2Il9w7e9ylSeN194uhzloVFWjxgWGGAA8GjncH7azr4Fdoc6JHBhJ-mG1BZJjUZRi2aHaXzgEk-Q_uJy103DKODmcDOfHqN4qFZrh2VSei6DxtcrBQegsWOYNyORiB_cIZbYOC3m243KEu3ZzeKvqrDlX6_UNk6J9cofLv2Q4FD0ivpLyr1hn-I0iTjbukHHouqKC-KyOURy3D2oGEQOcqEIq2cFGteXJGrmfKjSDujhBr1G-bTfI-ZSKAw3BojmNlJxiCU9_TIxCWM5XyoavR-b_ta5kcNuXeWJsyLUla6YRnAd2B9JYtCUIQ8NyuKPE9SVmB6WeomLM-Yn4XwjSxOw4R78DyyRRSSlOckTussDn-EjcYMJB0u9b_13bMwOYvcf-e6Z3TmcseRoQRpGZVRBNQxffrDz5YaRfQmUpfWYEYin0gy2Ki04imp5zSGkc0kSfHnTUKSr_ZSzoIqy2K44OrVRl6SfPVT0ol6c9rAORegXvRXZXcDBiMveL3F8JpSb2TAc7GnUGP4DTMQWl4u5c10ZB4fHI20ScfDaPn5r3_zXoZkT3EKlM6CTwzkWUDXDqWT8LrHb0hn27DGSCH-pHJjnGvQTPNdA5aecCAbyxHiSyll8CV995VYH4RqpCxkMK5Xbf03dC3x-Uk_Oj0iR-QZRSHcgjAKmVto8jAysRR5fCrFSo7Gwtz3QMniJQVmaDQj60qO9pR0KnGIC7CArvSHOKw4KBwW_TjLvNnBJhQF0o84X5EpxehYT533SjOiMSgTpejrnCL5QOnFlG9gKscv8EhvSUMWaUOljOfCkPdvcRb7vh-DfczJzU6bYqR-3c3Ne3BOV4lOdd4QCaC7vaQpDajGEy0CE8XAqVZ4JpkoqK5rgVoFZ16i8d3UDH3bGHhyGNjclB9Jc4HJjfrCOFeKG5w6b1s0OMW2wbSGeoRrgMJ5ENYUhqsGsfVroPtxbc7CyTl8G5R7uj9kH-CFEBFKucoc1g-ELZ-cJJ28oltOITu6WeohWgrHW4ufzpyQD4LD47zIAx6qEzKS4ZQz_glZbv2KtZh8JKanP6D9WqCza0TvHy4EDggEeddtXqBABwWH9cX6-GA1OVclt6LwuBhCCQyV6kF5IYPyIQoLDz0FBsmBnNzUGNEaTs2PgXcJrVXG4fe0Vq5V6WOUNTHeiRNPtDSIOBbxOIpXtdMlVuw55-MNBrXg_ZuZwwMdOIhYUCZBkWsBN2UOainz-JRAWAFo5_yaNeh4Q4OiboGxAvfAm7rqgdYXGGc4cgcpjwMWuyJfSIM3WWQmw_mhUY03rYDr86W6UkoG5XDNYe_pZrJqlH4K-GtVr3bI9Ka9XOHGDztgdmCoz2xUWRTAnhkq3FxtlJHSOLH62WRFOVjsZlFc-WnIud51I3_xLlN7cGaijO3edjvBx4Da8ZkF5TawzVb_hYhoMTEjvGQwVr6rG2IJyHTeUtIWXqWajpEyAntMBW9H1rxw_npX81F8zDfb8RavsSBfmII5dS0A-EeGZEAuLpHzLkfF8K90fZXKkz9zKjzNk4JlCUviQG2kkXlp8J7H5lSCKD29LxuMloIMmUl2L9LtBlPSdSM9Me1vzkUYQsmBU-cVnpoycOHwtNZkCN2FvFcMswjh9oy7UfARTckzu8Tghgc8TcKUgg5Chk4JodqgekqqJz2OST1n6EPdUbxFpCPB52J3iNxAiUP9g8TyqmHEAW9wr2nLkEPDvQY23eLHt4Kn7cjVeEPsWDIAILL711vkHg_iICkjf9IZpnzT6a5-dvaoHDjMvbIE86eKikQNbCSU3kduD0gPRc_9SBl4SuM-m1E_46rIvCD0goBpE2FKIpXTeVpK6HQNv2txJOFvk2MJGiZzom7z7qN45CupgNIjMtigz01kfujrIL5xji5vOFP1HRCAO2AkOEUl_-SDQO2tfAqt06LesgZkIxjjIE3Hmn4Rupj8wt7q1DfRdBS-TykxluyGPLcN76-OeDmUppN5HGukkiDTmo6RF6uSGp-Q5Qo8UtwjuBAD8Fet-b1QEmzsu0YIWspTvUSNZ6me-vffnSA_GL87uTyloBcbcKGoj-LN4h-3DRg7C2DYpCK27LpekSpBulMPolIJFhSmYFhN2jwWWPFhJGFgyHl6HSorQotChrTdgtbljN2s1pFlHvNzIHB9j4wsXrWRT8jJlVvKepKSdBIySCwoewAujMreZ3CTiAdl7rIiq5g2y4y83ombfF6irqIl3yvjgGcZEJXWJ6bc3YmVPDoZl7ZqDVomLV8YxMoQIuoQEqrkQKGoX9aofAozgNJJxe4DoSLZdOhgnWFFgcc4mGqYt6fVIyPlV7Oix-fw0kmigk2KjcyPOMVbTsk6C-dLXg-CBDtYcK_yJvBYlAEwMMxAE1dvSkO7Ro_0qc7wKeAPNZDRJLLh6wOYr9JuoUGEogJPySs50EyQX441BedBveivKFtDM9CBJrdBdbgYlnjHl3iAS9CV0VGHTHIgIqex3tMAHO2bVV0sb-A06fs__f1_w-cwMwesIRAlEw07xo0R8QwKzcknyRY4ZPdjt1o1sLZ671ajugjPEyd7LlmWVB1VqFmcz1HjhaZPKXXIGMSsO8qndSjzCDncZPsvNO2SFj6IXZIm0zWwIA4rE8z8NXIo4OG0fPMaaCaL5gX5PShdCAYg_e7ZMz1NdIvQMKCHgUGxwh1wSpn8NUjusG9o0ctfdVtpzpAreTjYx1kLBh00w0BZMuiipelrrQ0Hp9gq7pHzCt7w5TffSvZ1BneyAjUZd5eCqoJyJTUvcHrFFWwop5QZZNmCytTNcraYGUxzINtH-AKActGzA8oZ3YWJfOgubdB4pBMRfJ_OouSd-RkbtEn9u7en0i6UvrZ7nWoqI0iOg0bYuOmGLVxVfnq_zC2TwmNZ6YK1pN2gRs7-xH0fkn6vrIcyckGURyx0tfVgZOTLsZ-SXC9TnoUpqjW9rUx2xaxj-hKQf4c-NiNHGV8EKtCMXHKTImY8D_yQF4YRqTL2J9P90cn3TbfqHLDh8HJfY273LwX3JQfiQvsLyWhZaP6J11vzzsUe16wEJRLDXBgZKvg5FUyDelEhLypomjmyMEOyabNtgc9UrG7mLHYv95PAd9M8q6b9mWoGpv15dPq_8uDQH_FqD-JnVgJxYOn7ITPQ7nCyh5TWRjopubg5FzyGHBd0AnB2tM-kZw2_xO25y3lWlL5MM1BsGY8Fpeq0kxtUBDFFfM9q_KydrEBdKyswIPNQ21NGfYPeyceXKqDM0erbntNM54gr5gxk05Uiww-EnxD1khvNrSHMXJ-xLE_BCNSegqkKQq_h8QUN5ATfioPGBWCWJu7udd1RvwTpXiRB2fORUsDRl44zxUxzuqZ4LCpHkVS2pfZdiz9pJgLDAJ8fdzi2_rBur8nYAjl-A2bnnOekYGGQJ64bJno_jLoL05R9ZAkFE16jZujgSFFMgXECrOQGNCKg6F9-dwI7CQxoAGXlls8dne-FbhzkFa8oh1WqyroIYxIBc_UVyvJgCfbBcHkaelNUTZdcyLGeVk3x5vxN9ibCn7zIS7xX8NM3TKaQUIrUEjjJNZD5pNfSoMhVnecUnPHlfwMcxXd9338Jn3wRnUevY_opfZleZDjyFxfZRXLh4mfn8Xn2MsSfkjR5mSb43r7eIO08lwaP-BnomWP1AaiijDzm9HZSVnHA4MJ7ndGLX_lvghR-eicSjnUKpaTluqVcNR1fQa2ZhqKc5OfODew5bQj9gxN74128uUhpa17DshL8DBYX-a_hM8xJQy1Jc4LnwrOoEvaQb6FJQ_45MTa-TAaqnssflmj_4Bvci-giprfCii7euPhZ9OZl8Iq2yEuCJPRoiyZWyks0ZnWiM4qokkK3C9MXJ19b4hLh38t8RZt1kbwOxeuSN_7FOX4Wv3n5Jr2g170MfD-Gz3QwWAkMJtMyTZkpt3V16NemF6OW-Rz_LV_8Mgyj4Jx2N0FiwM9epclFikT0RXDugxDEMyQTXSzlmjU1_EDxbvwE9DV4laRCGXh4Ln-Qb5lIbzrDieD0Gb6aZKSZ-raYl4nimNHKbacNxinB2PgfOYc4js5TWinM4LW4Yufn5-5rWqmf-XGA2_4bWgvtWStk6Qtp15jhSBSUSrcw3nysFEqJkCBy_TzKwKiNJlVUV0cZLPOxhU_k-f7dWzST8Au0LSQa84GPZ8Bq0RS4_OLi_CK9cC-1pbqVt1wueSHE_6Wk9uk503NN13fPvUwROOJBelwZFuynHLt7jxEF5aWku-mNvSQ63GxNbYIPospyKW_IJUoKmY8k7MNrdU2ksoI35PTgZJWZu9nhG1DM8vHU-Q-8Ab3nuTQ4YVzSGowI9rX2oy2kQbs4arVpmqAot9LOj8cRTp2XoIlQsE3ZQDkXKi2W1czpJVFYwRNlEbJJS52K3PYCcI-rX9sAm26k-0tatM43n32yMl4viAOzhXDHW16T3rU27ccXzmbveOrh4GSkjoIDDAcZBKZLAM6Hb7ZrbE30Wb4BET9BYqjJB1zd3kvo19xk7nj10NZgLU6LfGumQ0M6MjX1zXgI0yKswiqNg8mONEoDDcbwhKq_Bf78D_8VN1n8_Of_jkLgUtwn_Nt_Qa3vEkgR0zekgxmz-TA1W44OfP6vagd7ZYEI4IZpg1so5OcLME_7bYOOwabOyVRvkCi2DcnkW7peNGM6brhDnUOhLyAoUlOle5v2tB6Q_IXD5ob1GPE7dS7JIsAf6fTPHMw3ucQLJmd5LsuMlHqiTMbJLpKCuC4w_WHSomAITGHiI032uRgH_UMDBuXgrMuOD0p7Jk-6sd1z_mq_irwyLd3E1Xk-RqnlpIF-qoJSEQzGLEGpDfMpQGUUVRqBm8fWSqIh_tz5tkZ29DXc8HcdWpyK8OAeZa4Lqjhqtwtnt0U68EFSncqhgGRA-tXDmgsyUkkRjjDUdSlezpF8RTSXl7TFiuNutw3ybxiYU0b6lIImlyKdeoKTTbIRfztwvZ4Z9Ze0wsN1CeMZJ26s0It--tPfeun2I2yEdxrTb6cpUe4ADJrhjFXRI_rD60FdGuU5JsewCMiwFarH6LRgbV3B9nRSXeyozgodfOhQw9BKJ4Jr6AOmHJulci-KxYj7ahjFKi3klKyLnq8wo02ejeTp6I-g6WKAEHVkEQ5CAtuLrwtejJdywzACqzJaRODegR1ei9B2a8Tv5Tm8UpeMUsG0NqLDkHAGrTghw6OzFLtOjkjYcR_3OJI7LjY8OXV-jcEbYLYjbYoMOhEHhvUDURglbVrTlxYGJkNxJaU2HJvLYeae-epOMoNBeR0r9JmgQQqsXK7t9yJXFAbFC0hZjB2IR3oNbL8Mvcl3qogjrvhyVy-1mwpY7fs3v4Hflu_EIS2c3_C26UxPFpHn5SjSEpftbjNcvnA8F7ZEvEIrLcah7rbokmXoLpHHO-cPTb2iBDU0izId8zWqn_f0hccVNaubuDisJpRGn45WGIyA6qom6tMUB7zwmiITr-sBePKtvKV77KUeG3RrvJ_OVAdXDG83Kn9qk4X9qv-MbkMVQ-fjJC1QoIgFAoHtekOgAC_qHGyaqa5kh7YBZRlgUABDn_WGBtAnO-eIzeIgB-bNw1D7J4zy70k6zFV2K0lTpjxIyyp3w-l4p2JvQzI8to67LuH3rnKSGKmSeBFuBLE3rNiEBxSPSFyMO6DmBPfnVDv0OqrUnu4x1TXpvcVfjORE_PVQo2yV9Ut_1UmK-IvOdDSzDdQahNsUI9a4XOZUDf9Y53eXjHdsy-pefU9oXWAGA0cKwhCWrV2vdPB03-EbLZZJErc6yLAkugeFTE9VqKCgjJQdqtftKOcrauVkDp6YpA6nC5_P4dwCl2bl42Fo7ndKVfGgs1fEyXohCgaRe6ercGjDpkKcV_ubrpPiXgnngTg_yh-CC-f4Hm5Dh0V7dSkUK_LkYSBQ3nf4CC47xv4GDGdidoWZPaKPaNhirvQ1rRejajco_PsO6E3ojikuTkar9FEJ7i5PQQkZXDepbqYxIKoKJ9-T2jlY3kgVeHsEdEB6ynMyYPoCPPNiqnsRXgBSN2TppaBsvS7kB3xKCCWBoDPklcQi3RJsia5RqdRFV0rBW9RSFVBRMeIwbFAm0qlz8RGDSSVl5GKUFjQxiliKoPyMGCiSJEqZW1ZJMqWiTG0Y9sTA4zssYOqzeSvVbcb7QqmuxwqHRA7XNSaybTpKMABdq9Hmlggzd7gdgpFM2QmsX5G8muG1cZhVOTry01T7b41mDxOv_czmDdq14wWZG7lR4XpTxpju53Aky_yh_RlAJrFhNN1dN6SKTLLQWdcg9kBy3uI1kDRK8fthzYDmhJWMmbNXt3evjnJb8nJJNcOTCV01nVDl5F1A21nlBWE9xE5q6rAUkfOhEonRaG7uKrG4Ki1wV2Suk4I_JZujo4fca3RzaTrIPfHaTJPBbRELmznuPGScl3HkurmO_hrtLOS5PKU9BSjf-ABNsgSzoiVFEVM-0WGIQ2EscGgEr9hzJahUa_ou7h4W3QMZ-1KuKjcQ3A1kFiqPEXjKroBj2nQ02-0U4ZoLwUVVCSpeAv_XBGq0z9i7749rhwGitF0tFO0qNk1XdF8v_ulPf8aTB20OtALUJA7TD4Dpc8xyuVW5MPvOHZ33M5fB6fGkihgrokhnrBpNOaZrPtdvQ0W6PM-PYj_zijibIn-6BYeuI358dw2kOyKGXgjZBCQ62p240Hov6C1Li0SHhul6oLWKCgA-qvSFA6VpuueeL59kExcg3cXpBDMFwkZFVlKnETTHl1c7YCiUFyKEvuApOq1nEPFjZANLzRn0pdXphHMOTR4mceJWLveSqWBH9xjR7S0e3z5EXvMbsnspAHxTD5yyBTZ5vdp1O7i_Sklajt3S0AmK_fcKTjx0DehARPmnk0Ilv0nqg_E1GLSTOXVTopAK0p7hod5SyhcWzqyB_pUXXbjI9_4iPeJCCVXRGUFoOCHhIzeKGD4n19vzWJKnHoZ29fYbTVX2GMXj-qWU3LDT4bGtzNJm1yDmRf1cMbUeYLiKU-drUfGFeg6Ty8OTFpbYnTiX2J4DJbwepq00Ildq3_jHbU3GJ5AtMCZeyswzdsPqUfm6P7F5YZbylEdZWPpTfvfUA8aMNM-3dlHWHPDnNPeiOE416zG6vRjW3GObuOCuEJ282G810fUTEAN65IzoDl4dmN4LtYnPdZCGgjDliylvf89xDidNjl2UpVMEQUqGY6xqUvVQGt-acRlFEHBowkuvggjYgaHbrdb3JKypREDs9AAfmFtVt6R7oRaN-snXot3LSqQhqjguTX6Kd_bqwolfZaBCvONiv3YOX0VZHbS_ROZKQ961mEMj8m6mJEjn_W4DkxGlZoMs19nXkQZTqhTwwPgCTDKRIoZWSitCg7J4j5zoeIEquBx3Jkk6FzBLnCc-gN49In_luRXBESy20rE16QRbaJmjnZeLqThLVZvJ5JUGYyI9ihgVO6g32GyENoRWogzNvBtHUC1EGkw7jGjRYrpqS9oGXmXpExWKEFAn6g_KG3kkr5R8HGIyhrFiSGrawsXRCLOW2TVRC6axD_vhYDNxEaFO6hY2jZSje6rWjNJRrG7b7RvFNDKJ5TPVbKGlV-7PbX9slRMwFSvvqqouQFsqJJPFXGz4YNSFBM_BVqDMfEcib9AneKGpjEKavYPh1zhIPpvYtlKKu3wA7kJNQIjgUTE6neovhMST2iAuTseG9JiTuiPkFs1VFjZJBBRdILbQX1uoIOWaSIWCwOLzEf39WLYmyXCL1LMkyShRZk6pDJFihA48O5DmI9cjazyR4I0gKHIHOGNZ5SrX9-X91eyC17QjmyoLVeYGKXWCH-PHqDUVtKNGie9LJbEMdWBWdJEvFln6UjNyoz5UWtlErWxX1uICoomtma6KX-rzpUznG7iJoNxvZJENOvbE0kWPF0ccypnRIARVwnpFQeSJhwiwocXEQkx_BxzKat2g04pC9hThxIukyRq981KXFu2JpLl7WJuEZIMFDJrvcPLjouYw4xvJsc4r5gFW0-uC5KmjmZbiD-xNpmR6GKR5FoZ5WU0ZZFO7Ml278vjGY3DsI5U6k4EAprYMR0l-q-x8gxx-MdBBUNn0NW9FVezLfYlDdgZ-Byh8xYXitZfVaownwksVnTmF4aiLhPS4E_9Y3tV9j-tyM9pWGkUZ98sk82Jt5Bmd1ZSl8IQeaaLGa1JWpVlRitDZQiUM1MiFpGSZ2LvhGq6n-vypVYJmxS0yCtUbQUtk0JZk-bcU_R8L3m9HVV5PrFXX4VPipD4I8dVJk9M87k6h8_QS_hGFvHG_J85leHcVy3qxb5ugX07lKZlEivzkmoyEW9ByNCeZy9UsiyDNqoCz1J00aN2Obt9P8ajGcu1wg36Hn_709zfrW1FTiqHbvX4IqjT-lz_96T-jj1UkHAvF0kgAEeFHYsakvQ0qF1fKiWkLpc8jv4V7JhwjtOdAPL3B5eU89dVScWTh-p9zcwUR86MoiLxg8uZOXfIMjvX5Le-UPRhwzwv8LMnCWCfPTl3wjNyUx7e0k0RlpvwNMilMibgp_0sVhw97HEy4vTFrWQp9cVe3OilMstO9FANnqCmJBePwqFpO-jkvTRXx1PktyevWmKqyn4wpUIkkWjwPYWKhFxYcO_WwZKpPmfr4qaa2T2jKJ92HTrkjvYLaFeQ6fX_A6nJFlKQh9r106fCFVLaUHoe8jDIxyfErk-zJA3Cf4iWFMKmTYpCBJJG8S_gRKJg7MXXdFUWe1UIxroXqqEM8ixoHgQGJpahL3RMD_QhiX4R2RjXha9L0BuKwp84bbJvxkaHCdob3_1sR_sUISi9yyWmN11xwBFmxKitn7x63YnjAmJtdSe7ZsW6oIcFkOCtyOgVOMuN0icqCxWWZhokuETUaJt69v5_Z-VDTmB9lYeInXpUZFaiqGaLhRnhsV0OML6JTAI4FWD4oH-WyAQO90UYFbJRUxLqmYVu8vEbIZ5D8TsUI1NaiF5kEhkoxoUwrsvOm2e3NaCEDA6pT0RQuUU5KpBPQ9NdoDwMRnE_uHYpD8gXyfPjDOwml6Pyv_3nXB0QPYTElPjd0zbU4YZmRRLY0pZkL84ZiWUyknKteJ7Rz7aQEqLWxCsR7KTQwUl1YXjeoThjllcL6RUeMyGWn1ibKtaFsqJzR22UtbiWj_SLGv5SBbsmEBds1NB6m-m_JHRYxI2mQ50wqQqaXcSrybKnwoGuXop5hsiVFxqx0A2CbKLCtyOVyaIDKZ5WP547z58B5fSqlGW2QGGPiidr3OfE81IOxy58gtC0XtYTSJyxNPsU9Z6yE1A1z4Np5zhOtqRgdPI07-7kNOZUKlEYlD1hVxFOJidGjUw78lJabrwxe-07m15-LQvyDs1jI88P_SvavokNfKSaNC7ubLKAjkMDAkT93oqcP32gDjSaqryKdBwqciryz-cJUQFmzQu_eeiNDi3i_RMov8BjM9gFmwlZth4RKsTdaAVXwo1AWjRFEXwV41bNnklqfPXtx0GRBzuL8m7cyLXavPcKlg34aruzmS9IGLueKpMDU42BGemXKptZWuqmpEu5P6FGKWRCSa-47T0-ndC1h7AMn3U6S9_K8KPh2XCqKvFyIO_0KFcKBqyI6YRWRbcjpnqGwN8LYUwc90HA5Kv4i78OgujlaewhJwQukiw1dKGRBqZVjKZLMhGZkacoZD7LeRytLszFDDzF7PdgwNqVOGX1ejUrhz-ncqkWv5xdJmlZpoCW70czV4BL39WpVEc04TivPDSu31Mau0b51L-X3cd1ZD5u9UYqbaXnCB3d8tVLo4Cupx8a9HbqOV7eLVitIzhhMFgd_2PlOGZDKujLfSUn32qFhBEQnU5-SAVVXRk75MuKaoYP7iIGuZQD2ERIdrGQFx56YFZssNFvVg2qvMdiki6MMEmSpiplUL5Hjiu4d68F4ZYN1TnskTf7CW50gYTa7FDa6uDC4ksP-lkuhKuuOlndO807BimqLIvpMTDda3WDViEfccWkA7Bcc6xCF0a_IbL9iTgILi0UJQnlmOhBEnz4KMFEpmnaWHeRJGQFSkTHEylvdCYu8PA3bCQuGXNDrrsEErpm0qdxjceImQZBN1vDUunjvOt_bllilZPDcTTy3KhhLJ8tadyreu9GP60I8xXnUCKTPtbCVKmIDZI_JORQU1zeI7aexS-MOT_pgODIeHxNUPXBMTx4QPBXT4az7JsCXQCofvJ-u_xQ8Ub1RFLeZYoAyQ3cvzGgUiRsFLRhh2muucbj9d8vn97pz3Cmgv9OtY_80RDOR-Y4kKjh4X6-U_RFJ7uOIU02E8FaWR3vnwNC67Yw6eeqUhBm523XXH7wixz2nJptLkvcV8HnVQhMDaMCNRcYOak7YSpNmC7rGIBxbxioL1SdUhMIPXiR59QaVPYrMYY7abQvzQ9Ey9bVEBycwesyqmBiBYuKmiSVbe8tQ-J0W3T_i3ZRdun84YZStgT-hd4iXH_Lbk7M_nBAxnuG7Pp5gQ23hg1F_JbI7u6o39fIqwL8ruXD829LDoP9Mku8MKBjXc_L9j4ufrTM1nE9f5zuk-w85pvUhS2IgZIbhA57dIDqRizA6Llp2RacZYeNxEJbw667Fm4ofDHwQ3bOxyzhMVNoL1PtaIwMlKffyZL_t-ud3up7rzf6H58-_P3O-cP6iy8-EgFrqPKXltf9v55DugxibkLvH0H51BMf5vT9lCn0ehPS9351pTM-rIk1dXvw8c_lWNYQz-lPKSmCZ5LBQrhygHaNGp5qFTCzAGI6rOPv5JgnPwgwbShh59gz-Jl0WUz0U6GOY7iozDZ89O4MVmM147mLCxGBSVUX480wSjWvMLS1aozcvMWmKEJPCgPodTVC4flWJyxymX14GZZgfoEY8aSex3yg2AdI5oCSlKasE9taLgvgf_85z_VB081N13uMsHHYReMBDDqAYnnreW5CuwGdk5swgG4urYlDqVrLmKvQtqqbXd3C-gGWKypr72MzBLCRcwjn-KuXazCpO72MTx0d9zStRUmccg6y2k_UM9162DT-9jw18-l2fvi5Ga6mmPL3vLs-_SVL_Z5D8XlUgE4bneHrf5Tz-1vdCkUCnsLGTmy4X9sshbcu8J52wnfM1u65BU7nvtn3qraMgUpXlpoiVwn6qAF7YSqLe_PS-C3P8RdqVbNhTE4uWXc1Fin9h9FgUBK-u4A8nN-tbGkxUuNzfTECdv6yzlIaBoBtFlNIB_I7jG4XFSAd-p3BTBXqFP-HAipzS7iYbErE1PhvrJGZZkAZl7gdRFGP4g5dJmlI3VLF3JoiJCeBhApv8YLUPq31Y7cNqH__k2sfnIzUdIhUlPx7HIfoUKNPPgrxUhakXe0nihkmSMbdMc5hTxj1gAB7wW56UPAmqKs_C3K8Y8IQ888rSTzJMvKni6J713AFe8s7c5Mz3jwAv5UWVV0GSW-AlC7z0rwJ4KY_hrnI3DnzdNclQGOQZPULOq5L-oCqLkMeMTfVnhui_gyDwEPGt3MeFVyVhEPpVoMnMkOhGYtZjpTI2EGaO72PBu1Gt31M1rlE9rxg75ZzuZV4wJ0jDn_70t6EXwxhG_ahRqX4-ajlCvQWG_STVvrvR5fNTIqY8fJV-NHYrjkbICwzWiKy_XjXYlEgY6psKPoMhXfJRNm5R5elaCZex2Bwob03tr_HWPTrmMZe6x_Mkj-HU3OkYDZ3HOMbH6i2y7dvECDZ12VLGDnXhXauqY-yitKTys161axSVMcKOWFIH3qn77tQzR9cBjjqhSpSBTzntonJV9PkRdQ6IA5B3WJ4ndrqvV9jmu8I8GeAXS9wu7MbR8xXe5l5zJDhILgpBZJMaIwtg7DBt5K3RpwnVJ5GRiQ5r4adGPA2zeR9Yd7fEV6ZO63MHFvHM972sCgN_AnHQ-p-RnvFYHa6T8QBpxkmLGuiO0v0Ee1WxGfTj7wZtwWEbfIrcUW_lKRtQtatay45N1LYDIXqmonF5jWtM9UWLUcQMWAMyUfSAIeeGqHE8n7z2EuiGUF72efEgIk26dAp4eg9rXF5Rf2b19RorM7FJOdY1zuVJpkWRVUnkx7lOcTU02n2UsMdppQRwJoGfphCxbhPBPtZ0gsiJqOmMqIelHGBkUxPExiGTU8MKlJo9PRMZuyRugvtSYVxgXl3TYDst5eQQQArITfiUjCx7PNI9l3cX-CUlmgn-OxXGYumeKG6bsIAwQCW24V5fC743yNx__Ls0DBFSB7t5ixJnyUonbLOpNkfd1bsFPVSfALyXVXwJBjyTwClTatlc7waPVQzkdh5MhdiGubDPKh-l8pNi80o0WsHmeV-8Sd5kb15dLvbBQS5lR9rLhSYf3F36hud5qZ_gN3TDXP23OEzC9OWlLJKXQ134F-kb93JSuUhrei4T0mTvSKyNglsNUvgW35H4bhBcnh70bdQakdEHc6_GSBdq7ju1jrZzPJavod6g_GTU1cDCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JYW3tLCW1p4SwtvaeEtLbylhbe08JZPgre8A1_5_zG45VNwiVS4_Z8IrOczhn8Kyo4xfEs9IHBj_nAiGl_Dh6IeH0jgDyei4TV8FtGvom81_OqefP_9Z2H73UXGM98u0NVeiUZs1BVddljXPaWMhuZC7Rj2dCEqxBi5yPeTYYB63wQQ6sXUmF2yVBXq-xTk3N3pnmNHfV5O-ajYsZ14LzlIRO_9PX-zUX0o_AtGIT95pT6BRnd3Du9kgodq-woMhPw_Rt90VVlFTbCnuZhtfY1eN8iXpBsTJztie4jhHgA7cV6302nBX7FNYnP02MRxDZhP2alu0sbcjk_tyCF9PiZdmqdFnrHAzaLQC9MqCPyQ5YV3Hyadxjb6NCadZRo_O9P4fEBBDWGl53IW_HgcpOqfBZUrS73K41FURZUbBnkZZznDJOaqdF23iJIwjlnAyggoMEnDIorytOQMBi2DLANj_v4lHQHm8tMzLz0CzJX6FQcaZxaYywJzWWAuC8xlgbkmYK7YddMsdd0yuR-Y6xiZsLJDc1AEhJUeo3WbX6CHflYJReAuCXOxRwNkSqqsTiOcZaRsGIFk4zQl3tawBwyto5DHNKgzbEexUSoelm4s8wbrE0nbUwVa_WYPL8wESaGmh3ebxh4ihBkJvrKLrOg9e1hIP9U8z9bHq-VTx9l9HLAWqBDjI-1eS7xfDAI6iSBdpOq7QH-CbFOxEE0etXpO5vgeltjEMS1m2L82zLAoAtWmKLmfZoXFDDOzUqY7f2hMSvEAGy0zIgrRPuj_ZuCwJI0Cz2VZzAP3fuCwoxJf8Q-4OxjL153RJa8gJrNTqZ_TrgoDWJR7K7CRS9n58FImcRgoYlh3cikbGd6BDruUzeUuhaaIDc6oBSG2NhJOgUvZzE82OzKP9FJ29_uXBwszamssZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcMsZJiFDLOQYRYyzEKGWcgwCxlmIcP-FUOGHYfNMt50LwbUhSSCBjPVN_Uo4aA0GJPRjQHVnPsAC8wKmHsb6MuGOap_-wCTugcc6jd4l7SLH2Mg0gup5yWBoKaG45qahVmru1wQd34Q8lMSZonHorwK0iBxS9R-eRJTR46jyE8aPOdfBvnp-4dAVx2BCvJ-PI4E9M-CflSi_811M55nRZUFsesVHoP9zxM3SqsicFMvKYO09Lwiz6MyZ6wM0zDigZ-5iIh0_5KOox9FwRH0o7JMvKIofIt-ZNGPLPqRRT-y6EeaEgOWJkVZuFWU_b-AfvTt3nQM3UZHPj9TeVmi8uIoPZ9ZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVWsthKFlvJYitZbCWLrWSxlSy2ksVW-hfHVvr-x_8DxzsjKg)
