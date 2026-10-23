# Proofpress landing page

**Build on every discovery.**

**The typed knowledge system for RSI.**

This is the customer-facing site for teams producing findings with agents.
It explains the cost of reconstructing scattered work, the typed finding and
its lifecycle, bounded research evidence, and the mission of compounding knowledge.

```bash
npm ci
npm run dev
npm test
npm run build
```

## Story and interaction

A knowledge thread connects the hero, scattered records, product, workflow
comparison, evidence, and mission. Native scrolling advances the sticky product
sequence: **Capture → Verify → Reuse → Learn (successful run → failed run) → Review**.
Learn has one navigation item and two consecutive scroll states. Reduced motion
preserves the same states. There is no wheel interception or timed outcome switch.

Outcome-calibrated claim weighting is explicitly a **product direction preview**.
Path strength and node size illustrate contextual reuse utility, not evidence
confidence or approval. The animation is not a live control-plane screenshot.

The hero links directly to GitHub and the existing Notion contact form. The
mission network finishes above “Knowledge worth building on.”; native blog
articles follow, then “For those who move knowledge forward.” and the contact CTA.
Company attribution is **Continuara Labs**. Keep fundraising details off this site.

## Deployment and sharing

The Vercel project root is `web/landing`; a normal Git build runs `npm run build`
and serves `dist`. `vercel.json` enables clean URLs for generated blog pages.
The reviewed film under `public/films/` must be included so a clean checkout
reproduces the published site. Other video sources and renders remain ignored.

`scripts/og-card.html` is the deterministic 1200 × 630 share-card composition.
Update `public/og-proofpress.png`, the versioned OG PNG, their JSON sidecars,
and homepage Open Graph/Twitter metadata together. The dated image URL avoids
reusing the old share-card URL.

The article sources and original dates live in `src/content/`; importing or
changing an article does not authorize posting to its original social channel.

## Evidence boundaries

Rubric completion, numeric errors, the separate Muse executor-token pilot, and
the IEEE paper are separate results with separate scopes. They are not customer
ROI, an official Harvey leaderboard, universal prevention, or proof of the
complete autonomous-learning loop. See the linked study records on the page
and [the product thesis](../../docs/THESIS.md).
