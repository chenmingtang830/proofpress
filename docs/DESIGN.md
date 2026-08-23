[//]: # (ob:ae580676)
# Proofpress Design System — Review Surface (Archived: Act II / Cloud UI Blueprint)

[//]: # (ob:4565936e)
**Status (2026-07-25):** The serve review surface was removed during the strategic overhaul (decisions now use GitHub-native review), but its color system remains Proofpress's cross-interface brand language. The launch film, CLI terminal, and future UI share the same dark tokens; when GitHub Markdown cannot specify custom text colors, the nearest emoji colors provide the fallback expression.

[//]: # (ob:9787677e)
In one phrase: **a paper-and-ink ledger**. A paper-colored surface, ink-colored text, and one cyan-blue accent govern all interaction; semantic colors are reserved for diffs. Information density serves one action—review: summary before full text, changes before unchanged content, and pending work before completed work.

[//]: # (ob:7056876e)
## Color Tokens

[//]: # (ob:451376f2)
| Token | Light | Dark | Use |
|---|---|---|---|
| paper | #FAF9F5 | #15171C | Page background |
| ink / ink-2 / ink-3 | #20222B / #5A5D6B / #8B8E9C | #E9E7E0 / #A6A9B4 / #787B87 | Primary / secondary / muted text |
| line | #E3E1D9 | #2C2F38 | Borders |
| card / wash | #FFFFFF / #F1EFE8 | #1D2027 / #22252D | Cards / wash surface |
| accent / accent-soft | #0E5E6F / #E3EEF0 | #5FB3C4 / #173741 | Brand color, edit, modified, interaction |
| add / add-bg | #2E7D4F / #E7F2EA | #6FBF8E / #1B3226 | verified, added, approve |
| del / del-bg | #B4453A / #F7E9E7 | #C87E82 / #3A2320 | rejected, removed |
| move / move-bg | #8A6210 / #F5EEDC | #D7B56D / #332B18 | why, moved, attention without alerting |

[//]: # (ob:a8d606fe)
Rule: the launch film is the canonical palette for dark UI: white `#EAE8E0` carries primary content, cyan `#5FB3C4` carries Proofpress and edit, orange `#D7B56D` carries why, red `#C87E82` carries rejected, and green `#6FBF8E` is reserved for verified. Adjacent diff states use the same meanings: modified is cyan, moved orange, removed red, and added green. Semantic colors are not decorative; both themes must be proofread.

[//]: # (ob:eeee2405)
The fixed fallback mapping for GitHub PR comments is `🔵 mod`, `🟣 mov`, `🔴 del`, and `🟢 new`. Blue is the closest GitHub emoji equivalent to the cyan accent; purple deliberately replaces yellow for moved, so an ordinary move is not misread as a warning. `branding.color: blue` in GitHub Action metadata controls only the action icon background in Marketplace/Actions lists; it does not control PR comments.

[//]: # (ob:f49db722)
## Typography

[//]: # (ob:53b8c3a4)
- Page titles / document headings: Songti SC / Noto Serif SC, 900 weight—the ledger's sense of ceremony.
- Body and UI: system Chinese sans-serif stack (PingFang SC…), 15px / 1.75.
- Versions, hashes, and numbers: monospace (`ui-monospace`), with `tabular-nums`.

[//]: # (ob:46a56fa1)
## Layout

[//]: # (ob:8aa0ba5a)
- Single column, with a maximum content width of 760px; document body lines should be no wider than 70 characters.
- Fixed top-to-bottom hierarchy: navigation row → metadata row → change-summary card → body → sticky bottom decision bar.
- The body must render Markdown (tables/lists/bold/code); raw markup symbols are a defect.

[//]: # (ob:f43f7a30)
## Components

[//]: # (ob:0287d639)
- **Chip:** rounded pill, 11.5px; status colors—published green, pending review/response yellow, agent cyan.
- **Tag** (diff marker): 10.5px bold small pill, new green / modified cyan / removed red / moved orange, placed inline with the block title.
- **Change block:** 3px accent rule on the left plus a very light accent wash; word-level changes go inside `<details>` (“View changes in this block”), collapsed by default so the body remains readable.
- **Comment card:** 3px accent edge on the left, card surface, and a light shadow; status text (“Awaiting response / Recorded · awaiting revision / Resolved”) uses ink-3.
- **Block hover:** reveal a wash surface and a “＋ Comment” affordance in the upper right; clickability must be explicit.
- **Decision bar:** sticky at the bottom, with solid green Approve / solid cyan Request changes; **the state changes immediately on click** (disable the button and change the copy to “✓ Recorded · awaiting revision”), preventing repeated clicks without feedback.

[//]: # (ob:7578205b)
## Feedback State Machine (Page Copy Follows Ledger State)

[//]: # (ob:aae4f716)
Awaiting response (feedback is newer than the latest version) → Revising (agent session active, subsequent SSE) → Responded (new version recorded, page refreshes automatically, comment marked resolved). Each step must use plain language: “The agent will receive this the next time it reads its inbox.”

[//]: # (ob:300ee19f)
## Voice and Language

[//]: # (ob:cab7f711)
UI vocabulary uses only the product terms: Draft / Review / Approve / Comment. Internal terms (event, ref, blob) must not appear in the interface. **Language principle (set by Richard on 2026-07-18): English is the primary experience**—all UI strings, CLI output, and documentation surfaces use English as the source language; the interface adapts through `Accept-Language` (with an explicit setting to follow), with Chinese as the first locale. In brand contexts, the product vocabulary (Draft → Review → Approve, for agents) **is never translated**; locale copy is a translation, and must be updated whenever the English source changes.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2QwZDM3MjMwYTVmODdkNzA3YTMzOTc2NiIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
