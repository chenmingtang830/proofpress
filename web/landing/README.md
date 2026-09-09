# Proofpress landing page

The public, hero-first landing page for Proofpress, positioned as the Intelligence Ledger for agent-native organizations.

```bash
npm install
npm run dev
npm test
npm run build
```

For Vercel, set the project root directory to `web/landing`. The included
`vercel.json` publishes Vite's `dist` output and provides the SPA fallback.

The primary hero action moves to the final design-partner invitation, whose contact
button opens the public, privacy-bounded Notion intake form. The secondary hero
action opens the repository. The evaluation disclosure keeps product use and
repository contribution as separate paths.

Public copy tells the long-term continuous-learning story while preserving the
governance boundary: outcomes become candidate learnings, evaluation stays
advisory, and only human admission authorizes reuse for a declared purpose.
Product efficacy, partner validation, multi-owner, and multi-tenant claims
require separate evidence.

`scripts/og-card.html` is the deterministic 1200 × 630 source composition for
`public/og-proofpress.png`; update the PNG and its JSON sidecar together when
the positioning changes.
