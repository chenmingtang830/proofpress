[//]: # (ob:6ec771b4)
<p align="center">
  <img src="assets/logo.svg" alt="Proofpress logo" width="88" height="88">
</p>

[//]: # (ob:de7999eb)
# Proofpress

[//]: # (ob:e667d986)
Proofpress is the trust layer for multiplayer AI: an open, agent-native ledger
that travels with the artifact.

[//]: # (ob:0e0e9d9a)
Humans and agents can produce a document quickly, but the decisions that shaped
its final form are usually scattered across chat sessions, Slack, meetings, and
somebody's memory. Git is excellent when the work already lives in Git; most
knowledge artifacts do not. Proofpress keeps a shared, checkable record of
accepted changes, stated reasons, consequential rejections, and their relation
to the artifact itself—so that history can travel with the work.

[//]: # (ob:cc376e2b)
Think C2PA, but for knowledge work: a portable, inspectable record of the
history admitted into an artifact. This is an analogy, not a claim of C2PA
compatibility, signed authorship, or complete capture.

[//]: # (ob:6ef36a68)
> Git made code collaborative. Proofpress makes intelligence cumulative.

[//]: # (ob:169d8523)
## Status

[//]: # (ob:d6f9f208)
Proofpress 0.1.0 is the current stable npm release. Version 0.2.0-alpha.1
previews multiplayer portable documents: the CLI can analyze parallel copies of
one Markdown or static HTML artifact, preserve both histories, and record their
accepted resolution as a multi-parent event. Pin the package version when you
need a fixed integration surface.

[//]: # (ob:19210f53)
## Install

[//]: # (ob:989f25ec)
Proofpress keeps its zero-dependency Python engine and adds a thin npm launcher
plus repository setup command. Python 3 and Git are required:

[//]: # (ob:7b197ac1)
```sh
npm install --save-dev proofpress
npx --no-install proofpress --version
npx --no-install proofpress setup --agent codex
```

[//]: # (ob:5ae48e1b)
`setup` installs a package-aware adapter and writes
`.proofpress/manifest.json`. It is idempotent and supports `codex`, `claude`,
`cursor`, or `all`. Portable history remains opt-in per artifact.

[//]: # (ob:da019dfc)
`proofpress@0.1.0` is the current stable release channel. The deprecated
`0.0.1` placeholder is no longer the default install.

[//]: # (ob:4273537d)
## Verify a portable handoff in five minutes

[//]: # (ob:1160e434)
The [portable handoff demo](examples/portable-handoff/) contains one neutral
community-planning document with a real, embedded v1 → v2 ledger. In a clean
Git repository, install `proofpress`, copy only `strategy.md`, then run
`inspect`, `import`, and `verify`. The recipient needs neither the source
repository nor the original session.

[//]: # (ob:2b655d31)
To add a visible, transparent distribution mark to a repository README:

[//]: # (ob:d4916c37)
```sh
npx --no-install proofpress setup --agent codex --badge README.md
```

[//]: # (ob:5796ae98)
The badge says that revision provenance uses Proofpress; it is not an
instruction for agents to download or execute software. Installed adapters use
`npx --no-install`, so an agent can use an existing local installation but
cannot silently fetch the package.

[//]: # (ob:e7b4f799)
## Single-file install

[//]: # (ob:d8cafbd3)
Proofpress is a single Python file with no third-party runtime dependencies:

[//]: # (ob:0b5b4916)
```sh
git clone https://github.com/chenmingtang830/proofpress.git
cd proofpress
python3 proofpress.py --help
```

[//]: # (ob:166fd594)
To use it in another repository, vendor `proofpress.py` at that repository's
root and install the matching adapter from [`skills/`](skills/).

[//]: # (ob:949eb6a5)
## What “portable” means

[//]: # (ob:2173502c)
Turn portability on once:

[//]: # (ob:c44f6768)
```sh
python3 proofpress.py policy proposal.md portable
```

[//]: # (ob:79416c44)
The setting is sticky. Later accepted revisions refresh a compact, hidden
capsule inside the carrier file. Send the original file to a collaborator and
their agent can inspect and import its public history without access to your
Git repo, chat session, or Proofpress ledger ref. The ref remains the complete
local/Git record; losing it does not invalidate a portable file, but local-only
history and repository-level lookup are then unavailable.

[//]: # (ob:af7113fa)
```sh
python3 proofpress.py inspect proposal.md
python3 proofpress.py import proposal.md
python3 proofpress.py log proposal.md
```

[//]: # (ob:5e991c72)
### Two transport rails

[//]: # (ob:398568bb)
Inside GitHub, the Markdown/HTML file and its capsule travel through ordinary
commits, branches, and pull requests. `refs/proofpress/ledger` remains a
separate complete ledger and repository index; custom-ref fetch/sync is useful
but not required to validate the portable file.

[//]: # (ob:a908fde7)
Outside GitHub, the original raw file is the transport. Its capsule contains the
public versions needed for inspection, sequential continuation, and
agent-guided merging with another copy of the same lineage.

[//]: # (ob:bfc931ca)
The capsule is declarative data, not agent instructions. It is tamper-evident
for accidental drift and inconsistent rewrites, but V1 does not claim signed
authorship or protection from wholesale malicious replacement.

[//]: # (ob:839fc8a1)
Portable carriers include a non-rendering discovery marker with
`Verifiable revision history by Proofpress` and the project URL. The capsule's
canonical discovery object names `proofpress@latest`. An agent may explain
this provenance and offer installation, but must obtain user consent before
downloading or executing anything.

[//]: # (ob:cc095bd4)
## Static HTML carrier

[//]: # (ob:e6463f5e)
Proofpress also supports static `.html` and `.htm` artifacts. `anchor` writes a
stable `data-proofpress-id` onto supported visible blocks (headings, paragraphs,
list items, block quotes, preformatted blocks, table cells, and figure captions).
The metadata marker lives in `<head>`; a portable capsule is a non-executing
`application/vnd.proofpress+json` data block before `</body>`.

[//]: # (ob:b8abc9df)
```sh
python3 proofpress.py policy launch-plan.html portable
python3 proofpress.py anchor launch-plan.html
python3 proofpress.py snapshot launch-plan.html --kind agent --author codex \
  --why "made the accepted review scope explicit"
python3 proofpress.py verify launch-plan.html
```

[//]: # (ob:00768820)
This is a static-HTML carrier MVP, not a framework or CMS integration. Proofpress
does not yet promise round-trip preservation through React/Vue builds, HTML
sanitizers, editors, or CMS pipelines; if they strip transport data, the file
degrades to an ordinary HTML artifact — `identify` can still recognize it
locally, but its provenance does not come back.

[//]: # (ob:226a29fd)
## What gets recorded

[//]: # (ob:cfc1c3aa)
Proofpress records accepted artifact versions, their computed block changes,
explicit actor roles, the reason for the change, and consequential rejected
directions when the authoring agent supplies them. The account is checked
against the actual artifact diff.

[//]: # (ob:5e0b34ed)
It does not automatically store raw prompts, transcripts, tool traces, casual
brainstorming, or every save. A fallback hook checks Git candidates and current
paths already admitted to the ledger, including Git-ignored artifacts. It can
preserve an otherwise missed version, but identifies itself only as
`recorded_by`; it does not guess who wrote the content or why. Harness skills
can also capture a specific existing file before an agent edits it, keeping
unattributed human drift separate from the agent's revision.

[//]: # (ob:d8387b0b)
## Privacy modes

[//]: # (ob:5df13acf)
Each artifact has one policy:

[//]: # (ob:3b52e3b3)
- `portable`: future accepted versions refresh the embedded capsule.
- `local`: versions stay in the local/Git ledger; the current capsule is

[//]: # (ob:126978a2)
  removed.

[//]: # (ob:0890e114)
- `ignored`: future capture is skipped.

[//]: # (ob:c6642117)
Switching from portable to local cannot recall copies already sent. Re-enabling
portable starts a clean lineage at the current body, so private-interval actors,
reasons, rejected paths, event IDs, and omitted-event counts do not leak.

[//]: # (ob:18995a53)
For a one-off history-free copy, use:

[//]: # (ob:f28051ef)
```sh
python3 proofpress.py clean proposal.md --output proposal-clean.md
```

[//]: # (ob:bfac82a8)
## Core workflow

[//]: # (ob:706dcea3)
```sh
python3 proofpress.py anchor proposal.md
python3 proofpress.py snapshot proposal.md --kind agent --author codex \
  --produced-by codex --recorded-by codex \
  --attribution-basis harness_attested \
  --note "incorporated review" --claims /tmp/claims.json \
  --why "the team chose the smaller launch scope"
python3 proofpress.py verify proposal.md
```

[//]: # (ob:33e05aa8)
Use `--rejected` only for consequential dead branches that future collaborators
should not repeat. Source code stays in Git; Proofpress is for Markdown and
static HTML knowledge artifacts.

[//]: # (ob:59769c11)
## Merged lineage and stripped copies

[//]: # (ob:47f21d3a)
### Parallel copies of the same document

[//]: # (ob:55bcd98e)
Portable files do not require Git to merge. Keep every original copy and ask
Proofpress to find their common capsule ancestor and report block-level
conflicts:

[//]: # (ob:8f498c01)
```sh
python3 proofpress.py merge-plan proposal-alice.md \
  --from proposal-bob.md --json
```

[//]: # (ob:d4ed0d79)
The command never rewrites the document. An agent can combine independent
changes and ask the user only about genuine semantic conflicts. After the
resolved body is in the target file, preserve its anchors and record the
reunion:

[//]: # (ob:74883804)
```sh
python3 proofpress.py anchor proposal-alice.md
python3 proofpress.py merge proposal-alice.md --from proposal-bob.md \
  --kind agent --author codex --why "resolved the parallel review copies"
python3 proofpress.py verify proposal-alice.md
```

[//]: # (ob:1575e201)
All inputs must be portable copies of the same `artifact_id` and portable
lineage. Their heads become `parents` of the merge event. When one document
uses different documents as sources, use `merge-lineage` instead; those
external sources remain `ingredients`, not parents.

[//]: # (ob:91a8deb1)
When one document merges several Proofpress-managed sources, record the
upstream references — identity, head version, and digest, never copied
history:

[//]: # (ob:100c5aa7)
```sh
python3 proofpress.py merge-lineage proposal.md \
  --from research-a.md --from research-b.md
```

[//]: # (ob:144c3d60)
When a copy lost its metadata and capsule (pasted as plain text, reformatted,
sanitized), the ledger can still recognize it by a deterministic content
fingerprint:

[//]: # (ob:28dec45f)
```sh
python3 proofpress.py identify pasted-copy.md
```

[//]: # (ob:b705ac38)
`identify` answers identity — "this is that artifact" — on a machine holding
the ledger. It does not restore history or prove the copy was never altered,
and a copy with wording changes intentionally does not match.

[//]: # (ob:2a955c60)
## Surfaces

[//]: # (ob:8deed5b3)
- `proofpress.py`: zero-dependency engine and CLI.
- npm package: thin cross-platform launcher and idempotent repository setup.
- `refs/proofpress/ledger`: complete local/Git-backed ledger, separate from

[//]: # (ob:1ab862cf)
  working branches; portable capsules are the public per-file projection.

[//]: # (ob:92071fb7)
- `skills/`: Claude Code, Codex, Cursor, and Pi authoring contracts plus

[//]: # (ob:1f7d312f)
  best-effort fallback hooks.

[//]: # (ob:605a678d)
- Embedded portable capsule: path-independent handoff outside Git.

[//]: # (ob:820f39ab)
Start with the [documentation index](docs/README.md). The executable behavior is
defined by the [Portable Artifact V1 contract](docs/PORTABLE_ARTIFACT_SPEC.md),
with its disclosure limits in
[Privacy Boundaries for Portable Artifacts](docs/PRIVACY_AND_DISCLOSURE.md).

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjA5ZGQ0MWU0IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV84OTcwYTZlNTVkZDM4ZGI5YjRhOTI2YTgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2UyOWYxODUxZTBiNDhhYTFkNDIxM2ZjMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq9XF1v5MaV_SuE8hAb6W7x-0PjNTIZO_Fg7Y0xM3GwcBvqYlVRzYhNdki2NB3DQJ523xeLPO2-7g_zwwL7L_bcKhbJlkaU1D0JYHikbrJ4eet-nHvvKf14xuo2zxhvL3NxdnG23V4GQZg6TiBk5DipzYXnSSnc0D6bnaWV2F-K_Eo2La5t1swNwovQF1GQRi6PuedGaRJw5mRSOEGYMTf2szSSnvQDGbvCDhwpg8T2mBeL2Je2lHGAdUXe8OpG1vuzix_pl_ayZVd4Qinft_i6YKks8Ot3ss6znKWFtGp5kzd5VVprXF3VeyvdW9_WVZVta9k0uGfL-DW7kvRKBx_X1Z8kXnZX04Lrtt02F-fnV3m73qULXm3O-VqWm7y8all5FXv2-cHdtfzzLsfPl7tG1pe8KhtZQhNtvZM_zc7WkpEK7UQI35H-mf7kUt6oi6BaeRknkc1CGQRCQANpkvoscUMWk2RV3dKrXRZ5KSG52Y_iUrpJ5sRQnZ36MWOO8F3Hy7irX6eT7pKzbbMr8MIuycmrWjRnF9__eNY9_scz7HFVN_ST_lqKyxQK__6MV0K-P_sBb2BsAQ9-8-XLL775crERZ7NnmQhr2zpPdy325jJlTd6Qmlldkoj4DpYj1ZK7dl3VJMx1XtKqzR7fbPBNyTa0a1qo2VmDG7HW2UW5KwqIyNfYGKlfLS0qfo1rQ8mjyElJ49iTlozm4uyT__3bv__f__ztU3zYPYIJoZ69JeORt_jks63Fivyq_KflGYeWZL08-3xZWtZn-ebKamqOz1nTyLY5L6qratHcXC3PcEeLzztjw3LtfqvMjNXs7KfZIBW0kySJTA-kOrDRB-X6xaEtd08ga4JlHjxEhmEkkjg84iHDVVbeWO1aWrDjprUKtpe1lVW1tdkVbb7Vv798fWGx0qq2spxZbOK1bXh1IhJ2hERf7TasbPAYYcEByraxOB4JGxc7Li1miYrvNvjcghfy62I_s2BoSnIhJyTi3ItC6R6zEe_WeXltvXK_famfRVq5LqvbQoorad1W9TW0YhnXnVl52WwRXlSImpAolJkXsjA-QqLPrd_lrbVhQlrkIvhfgfBY1azNb-RiZDe45lpia7F8ARuXJZ_SkRMmIg5c70City1rd9OG-gurv2jCSkWYJZlrx89cffQy9sJZ2MZO-a6uyQwarehyu0E-KCRroADkCJUXpt41cR07Cw7f9XWJ1YrikZcdrpp42yTGywaSP3f90eteS7nF3sED_iLrai4k3E5gC5Hk9gicpSXLK6QJ7SpCNFOvG6VOEjHuPFec1WrVrJclaTfXV1vzecNuJMS5sYbMQ5e8x1dlNTfX4ctBIDLTA4ECJv1YOumzBUIk3m1XRpqGPE9n-Tm7ZTW0IdgWQVxp5bbOkWyW5WqhJZ0K1Mx2EpE9e79Wgw5-rexz9YCBdsZpUe4qZbGw3q0nxPHdyAu8SByIo6DPfhRrLKwlqiyDNqwMrm8BtOxa-Yj9PnWZR_zZcUJb-p7_0UV8B-V9f-9-ITfVD5_I92yzLWRzbr6fd9-ff2qRFBMqddMQkMtzPr68Fbkf1iA0qjJAWyOFQQDafkKyBgwhHNfXVovrYQ7bqsmn5BV-4oTIWh9d3t6n7zusCT3KyfCtysAqx9C1KRNXUy4dJSGTSfx3MQh6trQatifnYu2A_SE1wC1DZrMAyJtR8nuB2DkVE2WU-hng2WFCgpnDqrIckuZPSgcfvmMqEcacZanwTnnuIW5jVqNuN4lBrXKLesYqK6grr8Ucb9_urXpXtvkUbkuDlMzuFNE680I5ZfGiQn56ToE1YV5OGGYiSPxTZIOrwkjILmB9rKwQp2vjiiggZxZMSQDejaL6YrtfWTC4KVdNfED8kAUHov2RzPTnv_6XMfyf__rf1kYiMDxiT1P3TViV6yBj2C4_XYZ3u7rs3DUvclgNLKqCf11MwWvfz8LoDpg96umd-WyVJXvWwUZAqiIH_sGH2DJWoDLt4wqy_Go1YT5R4iOc-v5H0A_CEQJkix0g52ta1CH7hfU1U7CDcwn8IfoA1eCnDPKv4aW8mlAhy1BIexn7O6uwq07GOjy8dCrCyyRxeOQeiPjutuoSHmS0apYXj1j4L6wP3zJh3F4SB2Gcpqc8GGAuR62EyumrXTpTEO0bpGNR3ZbnX7375msdNQk25qroVJ0UesCNLKa2LbHjDGX-KaL9ftfek62qc6B7VuDuWy1aX6B36y6s1-0k6E8znngOZ6eIRsZudAEBhOQF03WmJVjLZsgwrS7UVfytd5yATkOyTYkWe0nGY-acItq3BlFwVtc5Sj5IwIudoC5BWZXzmsqlmry0by0qAAYvvZ3sFNhJkAr_Xp2ac0vZSfe4J5TE9--Y7OL4oZcF8pTnjmABK5rKanZb0iUFKbXOarFuN8VKWbn6GT92fb1mypBilnJUR6eI9pS4XrBdydfzbcFKJWgf3Cdikm0j7cSufYps79a5wVHqxvn4Ruub777tzNzKaraR1PGBe1qvvnkLi5uqONyQuUkm7kf0K9lSXtAd2Kfggbs3TNgRz7jDPcZOeOrIjLou8pDXjL0AKqkmS6PCVV4juW22Gsg_pI9A2qnny1P0gagiKqB8tR27ttrQdgH07S2aAEgVLGFam23bdGUYr3P9y1TuFbEXR6l9tzuY3zBY5QYm9xhou3vtxP4EInM8xrPjnvUl4-thD9assQhia_-ZAmheGrjSS73jnjoHIu5ccXVhZbt2R50WYxLGEnqkQ2lKblJJ64yyQIFS-BDSu2ESxcw9TigLz9sgrIvFVEUTJ7Z0HP_o986vShiWGF4b2VD9S9DvOt9uD55_7xV5GPqu40THPf8tiji-phSWwaiHGrqtLKwPcMBZSa4A16EKnlfbXFLor2kKNdH8jJMkYMGRxvBbxD5GZjenMr6bvc2x89SI3qKIQok1ZYqZG9MM8EgHmMwjvJB6WNCXB_N5tWsRl_SHE3kkhUPFLjusYF5RTKF4nxXV7SMh4O61EyEgskPBJfOOe9akBhgSKPbnQXSfTajA86QdsGNV8AcU1qs5UBfNVuEwsBCEZRqWqBnpn3fAiDlMVkAhVlqToLJr5mRTSSOJwoQ7h0jxG1lfIbR0U1IFZ6jLRs7YOcEjm_WkBSZ20I8y1xHenQEXZC8K2fthlalI2AAz9GOrx0qjJ64xlV-ClIsklh9VtB5rUyWCMqCydNhRo3A1jUJI2pBSF9Y_S7m1pILbqoiZKgMyP4m57XxUWSf9Q8moEGbvI3OG5CkpWCyXy_HQ6J6DCIAXW0TJRxVXVVjVZkM2WJLaoFY9uNBTzW6JhfWy7AotGojijnQSfEZ-DFBj-_841d4JPb1a--unmntBFEj3IxvCS6TEvETwb6wNDbVTOWTQDyy5GlEcVlPdPofFQqYfV9Y_rmWpoFw_31aWSq14mATC5oDJ5zAVRtGrqXY1l81sKtPbNkdIj_7RDmYC6zgVK-9CQp4yA9_nngjtj69aprAJUBPsgPo7G9kyamCo0G8aHJ9sWaNqnMZChMjLyaavCyPgfpD941SbC0qhGcplJeac3kj513TnM42Q1bkXf1xBjTDUTGhuVfdFfdLurZ__-p_W8qztimqV4Y1rLc_Ut1U5SR9xWRIE_I4ZvN3VWOHRzD66bCJJYu-kCO6UQ095wvzubODi3nR-NJZ_9fXrxbKcK3bClvGpUoilcejeqQqfIpClwBmVCAZTvRhFOW3YKAmQpWl_t7sUUdnayppmJlNBzrUjJ0ujYxSEsqgomnOo5lXBqB_3CiY5U_9_j392dVPVM6Wfb3NLk8BI_nF3_L5-skh4jnuMflLZtHOZZdRUzGD0KePX1rqqrpupwjGE04RRLI5QwJem9L27DxcwgnY9x52dtbT9NLRSLeAJBcSunXkJS58tz9sWzqengWQB3xvvZmoiTbK8_-ETfNic93S_T4mdgBL-_V39_DAzVMKzrui_5Kg1NZ1PfWPogZM0R2BHtaZRj8kWsF5-va1yFXr0_Fxz_sxvRPn7gWiS1O4YrTCmTo4WUaTMI1mVTZW1lxnsUtbbOu_Im03qXHARZdyPQhE5QRbKyA2TwOcxd-zQlSzyhLR5LPFlkNGlacpEFiXM9x3BbK4GdNRlVCRMvVsXYfITFE0sSdd2w7kdzd3wnR1d-N6FG_7Kti9sCoWdxsfs0p9Gn_74MZibyto0sXLNmjVVOpkTstCPA64qdrXGiGvZGeLpJEpqNtJ3-Pw2F-0a38QxflnL_Grddr9hzc_Ot59_wG07aeMgCjMvdsLE9oy0Iw5mJ-3j1MpuOZGEhPmjOFU8F7XciG15j7T3fBIlAfp5qQcqilBYL0uVMfXgqRkc12zj4uG3dyJESZtldpZKI-6IitmJewrDknczTSVis2aol5cl4alMzarwrhuVa3bNTndlOfF9a8JUvK6gIK5u1HzeZma9LRCMZ0BjksapjcoKy7KpNpJo5r8knLap6v1ClZhQrnzPJWALhLslVEdCqXa8bnkB30GPNAei619YG6C9ZTlwNftZR1fAHlAlNd2O0VtB3pkORh11ixrTgEjLsu95dhTkmZoYqHEva9QbHTY7dDdEvyspXLfKa1mo6Iutrg72lqCpLDJApKbSOjbUdtoibRKDRdCbT1gDzF6wEFEpVqRLZQ0jGqwZup3Abu0VQ-IsSyMrE5u8JaXk9H4QvDddq5-0EP2Cwd_3ZrTCAbg3tBSJsixpmgAdaQYCtIzYQkakwEKzzrczq9Ijh0K2fU92QhlBlvA0ysLQl2wIYz0Dt1PGKcRaC16zK_SVE5sS2o4rY-YmPDFyjHi3JkBNU2q7tRiLAdLcyGFZ_04jlu396PRsAq29cBc2Cvntmi0clCUaVDQH8azP4iZuNBdqfWBfZbW0z_u_AHreqziWJRW8ZghPG9qM5nbGaGYWCS9rBMi0guVrK8tl51GdDSrHGvknbqkKTbpj5NVK4nnHyVNIBduZ6wjSEUjNHEOHln21W5alJKNDcHuvrVle1Ro2NRp4TWx0nAkR8xh5Non6jR5Ix8NGT9KJu8XsMHBiwCjpij4JjxjG93f62dxhRjyxUlmBnsJSItoWu2ZEj-pogV2zamGW8tQq5DgU-bueoLh4WDVc-Flip17EeJ-mRgTl7m1Oox4bRczn3a4-m_D4UFltAkroeolIGaJsH11HpGbzEqfQlUmyc6g6z1DBLP6E_LJSvIpc1dqbLVA0hFW9azPnXynRVzP8oEqv1QzLcVVxrVTIXEEKrNL3c03MruWGQUjAkhb6oQLxKYAj5pntJp4CkH0EGpjURgkncKQJdGxpvNUS0ljZCyywou4Ml-uqEBAzp2kwoCMh9Q6lZAzebnQ-lRRElqTEHwBQN-KPmNeDj55ImTbwzIk9TwSuDCPeh4SBRd0n5OPpz3oL4del3AEtFCqPbnZAaHvV8y4VG8bgOwUkiIrMitkwr71xrJ__7T-sG7fDozA51T6j0dqyJDcfEyaNL432eDXTvTY1_1k1kANxkxpVK0UVKImFiq3sgATZar6h91npgL66Ucpe6d3H1udIF5CWYjG2WuaKtKmaVar_uSxHEaqs6kP2VAc1J4wgDYAJYpY5Pu9teMQVN7tyAsmbBNMF2VRQDJjPMp9FadwHxREF_G5QPIa7La2-LHwkuCUSCcd3hbDDXicjevfIUo_lZecdhwOWMOKNKfTZFSXQIMGComKCApd8Lzk8zKK6nCLnwiROytA6iDb0JLzZXe3AsBqNQ_vxCbGA8Y98j40jn9DT9O56neKxm3AfPV9vcqo5aJwpW74eg4YJw2LI_p4rgoi7vRJHnPMR1Hsqg7xbOMvcMElFLOOgTz0jUvkHq9LnUcQ3KuxqyACkNWG2bpjxmEc-Yn4fQkcs8kOzPY4T3ixwFbZCHCT9D7fI5_O1LLaPWLeXuHHKbRHw0BkweM8uHzz-aK649gRz6S8hLq7Rqdp4LNnQhnXsDoMCFMvj-76B-sMn3U-fTpiZCGNPJp7DgEV6bDgQ0gczeyax3CgLGAeBIItS0SetEdfcKOsZnHHTWPJ4knKKKE4v94hGfmg5H40ObqKtjeJPeFnsxX1jZ8QQHwW4Y5neKF-pdlnnSKolBZKOQ6tZyAr8dPxCcsWF9Vbq9sCQupSLqjwylKFVrTskuo8wxDPD6lYWprKpAv9du9-APPL3CjU-id6oCIsqpx6S-uygPaPw4rg7p-AAvaRJzVkPG1s9xFbV-LJU0fRcr0rV2Quauykljuh7eXnDilxAl2NcRS-tGxFqkTmBiFFnQRV8xq_mhaR-SFFV18h43YgDsb1kNywvaLkJt4mEZweB5_N0SHEjCv5TzO9RKv3oUr0nT7iyqK4OL5u0Y6BXVIaZE0bOUIUMLP3e-Z_BuTcQwIt45DlekA1-P6LhDyckjybV4-q62l2tYWZ4OKv3Gq3mxNY0sywNCbe7olCFJeqgZmGtYHnNKD-ca8tc9dbIlmUjacPbwSqN-R6akJ5_vEAhAgPbzMmkVYo_b_YlJ59HCsh2wNFkkSPKiyDn6e1X4YGxBU_YXcg8J5My43bSN21GZwg6vZ5yIsBouS8IVHOuCwU9V5PgNF6DAFdnx8rlR71Luh9VDdNfqLCj29VXu5xupUk_ObUuI7oEqZH_aJjczVymWmJSRJ4QcSLcwGhkdHRhFIuPPYhAekLhJOs5QjWN3ZalApqcq9-IlIaSw-Rn6uAi3tBKhomjI9J3zhC9dLtStyWhl74vaWkGTCs7PEsJ_RaVqoQ7U8LHHuSV7qpQDauYPRNBiocS9WLgR34_zhgdnTBI74SDENg7hJgn_1GVleliW90fUbH-8OZrnQ66zSGwg4xUlcTLHj2wStXl9Jc9mjFm-jXgNtx6NeI3bdgeyFwxMCjTYfdGxQQ9HwWvrA_Qut4gxfKpUrJ6ctyOeVgS8wf7DScwBQXpoq8pFAAr99T_upoyUy8L3FgkMMwBrwxnRQ47t086-WHgPGKqF2dezDxnGDL1h0Huw_lnH-1AyNTkrFXXY1IRUtvMirxnPuzHPFfUzbZ_ArUEdM1r6emg9Un3EnALUtJVzbbrZoa0nytyjdyQv9Cl1p93lfIerEyjIaamAnoVxDRtsxIAV4f5LL8yBGty3U8Xy5IMq6fqdDbbz3hWn5Egn69ejAHEKEZo6-83GXbOtls4oLKY85tSjPpsv1LtNRVKOtm1zeAh5zSK-nw11UfiMia2HXJmbxqjMzPPgLIPnoB5hHR3976HLm9KqGddtfcfNJ8Tg6DzwPlcR7SufWCYW7frvbU8U-MRNbUaI2B5a8HVt1J5LoJcuzx7SAjd4PmAzNM9CY7COWCO4E4P2UeHf4Zx1tFHefr2_njSQ0Gji_l7qRDcJkdZCORSijlRhs14QncNDKZ5I-F459_t4DS7vBCwcBIEXsfKvM3_giA9s6QgDNLMjATbfCspXVKHRGXQvSYlj3CbTnWkfAIAkI1EFlJheRoqd0jqcIKiKFcjwhYVDKhlFKbi1VUJcSyqsBXiNvNeVT4MYXdIfNWGuj58avLoxKHgjDHH9oeacTgMdackfcLZJpMOqVMaCxTuftqH4OG40_1I-ezTS1106se7y9KYs6X-dBb2vZD6pm7kqxCUKn_ULTqSfWgITDhBADpqXDLMrwcClPY9CrtFrtm_G51aIT7MTeEYNZVWkOOKsF3bOWK7w3P6lxN5lk1sjx1xO5KBYE4gh6KhP5tloP0JR62qgj4hbiqMjagAANC1khdZAK-qTF5TxGmig9x_yMzSr9mooRKsVSiYrSkL3cgAsYW166Yf_Pcz526irtH-rENCpF2sNe8O84wz42v1BDXb1ENGciOCsrfk5vD1Zjjh1HmGdiTaIj2u151uRpOb0V9VW704KHevdmSQgIJIwVVXMygiF_YVykBoXVhf6b-RZumuj8JROtmbM0eIakDqeDYfWpeqEuiSVd_jpNBC4s3UJFAlP5TF3Z9lwwutiQPSod6-VFJgVdkTrfHLpseCU7bkxkHEfNTNDh96kf1pusHVn3BCzrQUk5Tq2cD1Hbs3z-HQXLfkcw_CmVTteMBWWRDFdl9sjM7GdYufct6tAyCK97lSIRVL9LcgK1HRqW20b5Noa31xMBMbgMwHWIGmxZxGzLZDFvhZ38QYHarr3mbyoJwpS_0kFC5jNFPus-twdm7Qy5Hn4YzAwk-Z63Kb8z6Jj47IGVrjCcfeaEpNw_03co7UhZqXbL9foSEyZGPGWcP5n_ZA9QT41MxgS0bbyjlhA2T4QicBSgs938cEd0XtpKRO3ALr9Rcdpq10WJrrj1UY74_PQISpLMqk4_IgzpLAHcaFw8m9TlfHnsYz--4goQacExfGPGR0QO8p0PWxQ3d0FkRd83g7y-Oe53tekMbcG1oB_cG8IZo84bCdCVCB4wd2gGUHLDI6f_eUF3z0TN19eH2ojceRdce-E3NU22ZkZ3LJ8Jm5evT3Nefq72tad_-6Zn8pUW2B2amrUW-pg9zD9eUZvlZtjMY6bzfbc_2z4hncQfyqySTZBmm5anTqajY0ejOFh4b-jyL-p_c1RRSHrp34LBqGGqPjid2unXLksAteo846Ei72bleIrtG3lQxx5K0aMms6GAXvgV14OGCjp_ZUJs1iHPUBPsBBnPD8zElT145szx5oFaNzkIMbHHuM0eBp-IFPyc8WfS9ydLJx1D0-_liiiTOp5yR-mkaB20P30UnFu52sI44ZlqpludVDAtZcL8vRBuG2LO_5l9RmhpGbDEsFTtONVlRvGIWWKgP0gIHa0mUGXNFODULjJHP8KA1iJvo9Gx1vfEqcefxsIjxSZ0TzdVqlOsSQ1z7iU1kk0zS2UzcbKJCjE43jPuuRxxGlNTraALXpIspsiLpfteU0Xk5pFIUVdnRjI_FEcpde13hC1mqmB6XbpipuqDxDalYEKA2hkM5RPnZTox7CE_bVQbu5wxGklXYl4ubETsLpssgOAgJSfcYYTlMekTHuH4X80M5_YNMf2G5jCw_nFRO5e71pykLnxF2_Rvvyk6P26C2m7SzxbDtATZ66YY9bhvOdnf5OOZyph0J9Z8yMGKhWhndT9GmwnupUrLqDIyuzmlZ1xwC9d-oSZRKRVaiAlprZY0itRCM1By4VMWB1cNJRU_zwZALxFdFQ8JqyVhQkfVc3nQKCLq8AoHMlle5GdTJOZASURI6wPZmNmGqjc6j931I5_hDpgZPstkgjlPBR4ZAeSHxqIpkjfjOl5KEspv3QfxJ-1gUNtYWin9xOuFvmep4XRiKIR4zo4djq0wPn1JlT5UYUHljN13M28q3-w_Rxy468OHYkCyUPBssejqyOd-HI86ZYgXaib5bPho6h-HQ26mw80MSjaQ0D3oHpbfKSOgTcdBmW5eg001RF4DqoA73Yj91-HDE66_qkwfjzDqqarmFgyyzwU6CRHiKMzq6aB5988NTaMCoupUUEUlUeDmpV_aC-Z1NL3eoyozAd0m9M8wZvesuazuBZoc65YMNUuuu-ptHorerKXpmeomo0l4TdVTOtf5giAy0mjzalMuRhZove-EYHZUfzp8kTsMN4X9pJHAo765U9OhQ76oMcfdqV6HEXmlauzv4QsmnVCSHDMNcD14HKfJdqrnsoD0z7L0ajfdNImVMHkQBx1_07aG093JWQUcgDz7UBjgZC2HAgt2-jHH_Stp-XTnfTfB4mtsMTOxnoHKOTuMOuHH3EtqS-LLX2i91EXyn1QifNhCscf-grDSdwe4U872htTy71bDdhThIHw1Gc4bRt_5LHH6NVpcJEF8qJEzvNIjdLnQGrD-drhz8id_TBWRo5KpFTuWY3OZEsaJIkEYIJxO71in2589L0Mb9z-j3q1v7292_evfzN119evnzz7vVvX756d_n22y9f0bMQapRwlF5ozo5cQyVtkW9U7xflwPem6fobmlYxOjSj6tR7z23Mw968_u7lq3-9fPkvX1x-8frtq69___YPb_SL3TsK_BP--3_yI6o-)
