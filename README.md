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
Proofpress 0.2.0 is the current stable npm release. It adds multiplayer
portable documents: the CLI can analyze parallel copies of one Markdown or
static HTML artifact, preserve both histories, and record their accepted
resolution as a multi-parent event. Pin the package version when you need a
fixed integration surface.

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
`proofpress@0.2.0` is the current stable release channel. The deprecated
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzU1NmIxMTVkZTcxMWIwY2QzM2VlZDI2MCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjI4MzZjYzNkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8zZDY5YmI5N2E1NmE0OTczNmM0MzRmMjkiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2UyOWYxODUxZTBiNDhhYTFkNDIxM2ZjMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVuP20h2_itE78POYCU175f2ZLBez2zGyEzWsD2zCCyjVawqtrhNkRqS6navMcA-Je9BsE_Ja37YPATIv8g5dWOpL2y15J0giF7sboksHp46l-_cqj-ekLYvC0L785KdnJ2s1-dRFOeeFzGeeF7uUhYEnDM_dk8mJ3nDbs5ZecG7Hq7tlsSP4rM8Dbw89Au_iGjBswhuialL45znfgpXpBx-JbEf0diNkiLNPTdIE-amGYuo6_uwLis72lzx9ubk7CP-0p_35AKeUPMPPXxdkZxX8OsPvC2LkuQVd1p-VXZlUztLuLppb5z8xnnVNk2xbnnXwT1rQi_JBcdX2vq4bf7E4WU3LS647Pt1d3Z6elH2y00-o83qlC55vSrri57UF2ngnm7d3fIfNyX8fL7peHtOm7rjNXCibzf8p8nJkhNkoZ8GMaUBO5GfnPMrcRGwlp8HLM7yPEtIFJMwS-DCMAgLP0PKmrbHVzuvypoD5Xo_qnPuZ4WXRh538zAlxGOh7wUF9eXrKOrOKVl3mwpe2Ec6adOy7uTs3ccT9fiPJ7DHTdvhT_Jrzs5zYPi7E9ow_uHkPbyBlgV48Ouvn3_13dezFb7GU0SE9H1b5pse9uY8J13ZIZtJWyOJ8B1IDhdLbvpl0yIxl2WNq3Y38M0KvqnJCndNEjU56eBGWOvkrN5UFZBIl7AxXL5aXjX0Eq6NOU0SkEG4HPakR6E5O_nsv_76L__9n3_9HD5UjyCMiWevUXj4NXzyxdohVXlR_938hAKXeDs_-XJeO84X5erC6VoKn5Ou4313WjUXzay7upifwB09fK6EDZbrb9ZCzEhLTn6aDFQBd7Is4_kWVVsy-iBdv9qWZfUElCaQzK2H8DhOWJbGezxkuMopO6dfcgfkuOuditzw1ima1lltqr5cy9-fvzxzSO00a15PHDLy2i53ecYysgdF32xWpO7gMcwBBaj7zqHwSJBxtqHcIQ5r6GYFnzughfSyupk4IGiCcsZHKAJlTGLu77MRb5dlfem88F89l89CrlzWzXXF2QV3rpv2ErjiaNWdOGXdrcG8CBM1QlHMiyAmcboHRV86f1_2zoow7qCKwD8VmMemJX15xWeW3MA1lxy2FpavQMZ5Tcd45MUZSyM_2KLoTU_6zbig_soxF41IKYuLrPDd9ImrWy_jzryZq-WUbtoWxaCTjK7XK_AHFScdMAB8hPALY--a-Z5bRNvv-rKG1arqkZcdrhp52yyFl404fer61utecr6GvQMN-DNvmynjoHYMthCc3A0Yztrh9QW4CakqjHVjr5vkHjgc6j2VnMVi0S3nNXK3lFc702lHrjiQc-UMngcv-QBf1c1UXwdfDgShmG4RFBEeptzLn0wQWOLNeqGp6VDzpJefkmvSAjcYWYMRF1y5bktwNvN6MZOUjhlq4noZK568X4uBB78V8rl4QECVcDrou2pezZy3yxFyQj8JoiBhW-QI6HNj2RoH1mJNUQA3nAJU3wHQsun5I_K76zKP6LPnxS4H5PLJSXwLzHt3537GV837z_gHslpXvDvV30_V96efO0jFCEv9PI4iFnifnt4G1Q_WQDQqPEDfggsDAnD7EclqMATmuL10ergexGHddOUYvSzMvBi81ien1-j0XYXVpkcoGXwrPLDwMXhtTtjFmEonWUx4lv5NBAKfzZ2O3KBykX7A_kA1gFsCns0BQN5Zzu8Z2M4xm8iTPCwAnm07JBBzkKqiBErLndzB_XeMOcKUkiJnwSHP3cZtxOnE7doxiFWuIZ5x6gbYVbZsCm_f3zjtpu7LMdyWRzmK3SGkKfGCcMqhVQP-6SkB1oh4eXFcsCgLD6ENVBWEBOUCpI_UDdjpVqsiBJATB0SJAbyzrPpsfbNwQODGVDULAeLHJNoi7Y8opj__5d-14P_8l_9wVhwMwyPyNHbfiFT5HngM16eH0_B209ZKXcuqBKkBiWpAv87G4HUYFnFyC8zu9XQlPmshyYGztRFAVVUC_oEPYctIBZGpsSvg5ReLEfFJshDMaRh-Av6AOQID2cMOoPJ1PcQhNzPnWyJgB6Uc8AczBqqDnwqgfwlaSpsRFpICAumgIH9jFqroxObh9qVjFp5nmUcTf4vEt9eNcnhAo9OSsnpEwn_l3H_LiHAHWRrFaZ4f8mAAcyXEShA5fbPJJwKifQfumDXX9ek3b7_7VlpNhI2lCDpFJgUfcMWrsW3L3LSAMP8Q0v6w6e_Q1rQloHtSwd3XkjQToKt1Z87LfhT05wXNAo-SQ0hDYde8AAIYpxWRcabDSE8m4GF6GagL-9tuKAKdDmkbIy0NsoKmxDuEtFcaUVDStiWEfEABrTYMswR1U09bDJda1FKTWhQADLT0ejRT4GZRzsI7cWpJHSEn6nE7hMR37xjN4oRxUET8kOdasIBUXeN0mzXyEo2UWGcxW_araiGkXPwMP6q8XjcmSCnJKURHh5C2i12vyKamy-m6IrUg1Bj3EZvkuuB2Ut89hLa3y1LjKHHj1L7R-e6HV0rMnaIlK44ZH1BP58V3b0DixiIOPyZ-VrC7Fv2C9-gXZAZ2Fzxw-4YROaIF9WhAyAFPtcRIZZEHv6blBaCSSLJ0wlyVLTi31VoC-Yf4EXE3D0J-CD_AqrAGUL7Yjk3frHC7APTdOFgB4MJYgmit1n2nwjDalvKXMd_L0iBNcvd2drC8IiCVKxC5x0Db7WtH9idihRcQWuz3rK8JXQ57sCSdgxBb6s8YQAvyyOdBHuz31CkgYqWKizOn2PQbzLRokdCSYJAOuim-yjmuY3mBCkLhbUjvx1mSEn8_ohx43grMOpuNRTRp5nLPC_d-7_KiBsFiw2uDNxT_I_S7LNfrreffeUUax6Hvecl-z38DQRxdogsrQKiHGLpvHFgfwAElNaoCqA5G8LRZlxxNf4tVqJHkZ5plEYn2FIbfg-0jKHZTDONV7W0KO4-J6DUEURBijYli4adu5PE9FWDUj9CKy2KBCQ-m02bTg12SH474kRwUKvXJdgTzAm0K2vuiaq4fMQG3rx0xAYkbM8pJsN-zRjlAwIHC_jyI7osRFgQBdyOyLwu-h8B6MQXUhbVVUBiQEDDLWCwRNdIfN4ARSxBZBgxx8hYJ5SqZU4w5jSyJM-ptI8XveHsBpkVVSQWcwSwbKqNSgkc2a6cFRnYwTArfY8GtAhfQXlXc6GFTCEvYAWYwZavHQqMd1xjzL1FOWZbyT0qawdoYiUAY0DjS7IhSuKhGgUlaIVNnzj9wvna4gNsiiBkLA4owS6nrfVJaR_VD0CgQptGRKQHnydFYzOdzu2h0R0EYgBeXJdknJVdEWM1qhTJYI9uArbJwIauaaomZ87xWgRYWROGOfBR8JmEKoMYNfznW3jI9hq3m-rHkXpRE3P_EgvAcXGJZg_HvnBUWtXM-eNB7llxYLQ6LsWyfR1LG809L6x-XvBZQztS3haRiKh5EAszmgMmnICoErVfXbFrKu8mYp3ddCiY9-aUVTBtW2xUL7QKHPCYGYUgDFrufnrVEYBNATSAHmN9Z8Z5gAkOYfp3g-GxNOhHjdA5YiLIeTfr6IAQ0jIpfjrUlQxdaQLgsyJziGwn9Gs985gl4dRqkn5ZQTQwmE7prkX0Rn_Q3zs9_-TdnftKroFp4eK1a8xPxbVOPto_4JIuwU2w7pt-0sMKjnt26bMRJwt5xFt0Kh3Z5wvR2beDsTnXeKsu_-PblbF5PRXfCmtCxUIjkaezfigp3IcgR4AxDBI2pnllWTgo2hATgpXF_15scrLKz5i3WTMaMnO8mXpEn-zAIwqKq6k6BNS8qgvm4FyCSE_HvB_hv03ZNOxH8eVU6sgkM6bez43f5UyQs8Px9-JPzrp_yosCkYgFCnxN66Syb5rIbCxxjUJo4SdkeDPhah7639-EMhKBfTuFOJS29qYY2IgU8woDUd4sgI_mT6XnTg_LJaiBKwDut3URUpJGWD-8_gw-7U9Pu9zl2J0AI_-E2f95PdCvhiQr6zynEmrKdT3yj2wP5eZolLol5FDEWpCzP8pBkfiyiC8COYk3NHu0tQHrp5bophemR9XPZ86d_w5a_99gmiekOawW7ddJaRDRl7tlV2TVFf16AXPJ23ZaqebPLvTPKkoKGScwSLypinvhxFoU0pZ4b-5wkAeMuTTl8GRV4aZ4TViQZCUOPEZeKAh1mGUUTptytszj7CRiNXZK-68dTN5n68Vs3OQuDMz_-jeueuWgKFccxqZExFno8BAEZPv34KTo3hbTJxsol6ZYY6RReTOIwjaiI2MUaVq-lEsTDmygx2YjfwefXJeuX8E2awi9LXl4se_UbrPnF6frLe9RWUZtGSVwEqRdnbqCptXowFbWPt1aq5VgWI-ZP0lz0uYjlrG7LO017T2-iREA_rWVBRTQUtvNaeExZeOoGxdXbOHv47b0ErKRLCrfIuSbXasVU5B7SYUlVTVOQ2C0JxMvzGvFUIWpV8K4r4Ws23UZmZSn2-7aIqWjbAIOouFH283YT500FxngCaIxjObUTXmFed82KY5v5rxGnrZr2ZiZCTGAu_0A5wBYg7hpRHRIl0vEy5QX4DviIdSC8_pmzArQ3r4deTVPrUAHsVqukbLcj-FZA70QaI9W6hYlpgEjz2uQ8VQvyRFQMRLmXdOKNtpMdMhsi3xUZLlPlLa-E9YWtbrb2FqEprwqASF0jeaxb23GLpEgMEoFvPiINIPaMxGCVUtF0KaTBaoPVRbcDulsNY5Ccea1pJWxV9siUEt8PCDei65hKC7ZfEND3G11aoQC4V7gUkjKvsZoAPJIdCMBlsC0oRAIsdMtyPXEaWXKoeG9ysiPMiIqM5kkRxyEngxkzHbiKGYc01jqgNZtKXjmyKbHr-TwlfkYzTYfVd6sN1HhLrVqLkBRAmp94pDDvZHXZ3rVOT26gdWf-zIVAfr0kMw_CEgkqui17Zry4thvdmVgfsK-QWtznmz8D9LwTccxrDHh1ER43tLPqdlpoJg4Sz1swkHkDki-lrORKo5QMCsWy9BNuaSrZdEdQqwXFU9WTJ5AKbGcpLYhqINV1DGlabprNvK45Ch0Ytw9SmvlFK2FTJ4HXyEanBWMpTcHPZonZ6KHpeNjo0XZitZgbR14KMIr7zDhhq8P47k4_uXeYYJ9YLaRAVmHREa2rTWe1R6m2QJWsmumlArEKKg5afpUTZGcPs4aysMjcPEgINW7KalBWb3NY67FmxHSqdvXJDY8PhdXaoMR-kLGcgJU11tVqatYvcUi7MlJ2CqwuC4hgZn8C_7IQfRWliLVXa0DRQKzIXes6_0KQvpjADyL0WkxgOSoiroUwmQugAlYx-Vxts1u-IkAkwJIe-IMB4i6AI6WF62eBAJDGAg2d1JoJB_RII-hYY3mrR6SxcGewwAKzM5Qvm4oBmSVWgwE6IlJXKKUgoO2a52NOgRVZjv0DANQ1-Vbn9aCjB7ZMa3jmpUHAIp_HCTUmYeiiNg55__ZnuYWg1zXfAFqohB9dbQCh3Yicdy26YTS-E0ACW5FJNRnqtVee8_M__6tz5Ss8CiIn0mdYWpvXqOZ2w6TWJWuPFxOZaxP1n0UHdIDdxETVQrQK1NiFClupgATKarnC91lIg764EsxeyN2HrS_BXQC1aIthq3kpmjZFskrkP-e1ZaHqpt3unlJQc0QI8ggwQUoKL6RGhq1ecb0rBzR5I2EyIBszihEJSRGSJE-NUbRawG8bxX16t7ljwsJHjFvGweGEPmNubHhitXdbkrpvX3apejhAEqy-MYE-VVACHERYUDWEoeHiHzgFDXMwLkfLOdOOEz20NKIdPgne7DZ3QLA6iUNN-QS7gOE__gE2DnVCVtPV9dLFw26C-sj6eldizIHlTN7TpQ0aRgSLgPcPfBYl1DdMtHrOLai3awe5Wrgo_DjLWcrTyLgeq6n83qj0aS3iK2F2JWQApDUitn5c0JQmIdh8Y0KtLvJtsd2vJ7ybwVWwFWzL6d-fIp9Ol7xaPyLdQeanOXVZRGNvwOCmu3zQ-L17xaUm6Et_DeTCNdJVa41FGVoR1d2hUYDo8nhnEqjvP1M_fT4iZixOA54FHgEsYrDh0JA-iNkTG8s1swDjgCEokpwZp2X1mmtmPaFnXCeWAprlFC2KZ-i22si3JeeTtYNra-tC8MeCIg1Sk9ixOsQtA7dvpzeErxi7LEtwqjUaEtVDK7uQBfhR_YWoijPnDZfpgcF1CRUVfmQIQ5tWZkhkHmGwZ7qrW0iY8KYC_Kt0vwZ5qO8NxPhIeicsLEQ57eDUJ1vpGYEX7eycgAP4kto1FwY29rKILaLxeS2s6alcFaOzZ1h3E0y02vfK-opUJQNe2rgKX1omIsQiUwQRVmZBBHxar6YVx3xI1TSX4PFUiQNse02uSFnhciNqk7DAjaIgpPng4qwW_F3E79FWeutSuSc7XFk1F9uXjcoxoFeIDAsvTrwhChm69I3yP6HnXkOAIKFJ4AVRMei91YY_TEju3VQPV7fN5mIJYgYPJ-2NRKsldmvqWpaEhOtNVYnAEuKgbuYsQPI6yz-cSslcGGkk87rjuOH9IJVafLdFSNY_nkEgAgK2mqJICxd_2t3UFHUeXECxARyNEmm1vDBUHiO_Ag_YEjwidzEJvILzgrqZSdpYMwSKr4dMBGgum4BAJOeUKTC9mgin4TUQcCk5Fipv5S7xfohqiPxCmB2Zrr7YlHgrVvpRqWUYoRykRP5WMVnVXMZSYpwlAWNpxvxIc8QaXbBs8b6DCMgnCJx4OwVTjWW3eS2AJqXiN2xKg5BD-2fM4IK9wZV0J460SD94g_WS6UqZlgS-mLykIztgeq7wLDr0a4hUOagzOnzYg7KRWRWMYUVnz4iRojGHeDEKk9CUM6zRCY30DhiEgL0DE7PzoSoLncV21CEqzvevv5XuQG0Ogh3wSE2NfdnWA5tcXI4ne3Q2ZvotwG1Q64XV37QiN4DMRQcGejrYPSuYwOdDwMvbLbQuN0h0-TQ5Sj0qruo8rLHzB_YblEAHFMgLE1MIAFbfYP7rYkxMgyLyU5aBYA54ZZgV2c7c7jT5oeE82NQgLYKUBN5QZDLDIHfh_JNHO8BkyuashcoxCQspZWaB2jMd9mNaitbN3jwBUwIy5nVkddD5TL0EqAUy6aIl62U3AbdfiuYavkJ9wUudHzeN0B5YGUtDRFQF5Cpg06TMcgC40swX5YVusEbV_Xw2r1GwTKuOkllT41l8gYR8uXhmAwjLRkjpN5sMck7Wa1BAITGnVzWz8my_Eek1YUoU7VJm4CGnWIr6cjGWR6I8xW478JlGNKyZmSdA2QcnYB5purt930OXdzWwZ9n0dx80nWIHgdLA6VRaNJU-0J1b18sbZ34iyiOiamUjYH7tgKqvudBcMHL9_OQhImSC5x6ax3MSFALniHiMegayW8M_Qzlr71Eek963Kz1oNJTNv-ECwa1KCAsBudRsii3DujwhswYa07zmoHinP2xAaTZlxUDCkRDQOlKXfflnMNIThzPEIN1EU7Au1xzdJWZIhAe9kU3JFm6Trg6ZjwAAaEOSGRdYHovKCkltV1BEy5XVsIUBA8QyAlPR5qIGchyMsAXi1vVeET4MZndwfM0Ksz50rPLopTGjhBDPDYeYcRiGuhWS7jDbpN0hZkpTBoF7mBsTPIw73bWUT55eUtbJlHfntRZnRxydBftecXmTKvkKBCXCH3GLtGT3FYERJzCAjhKXDPXroQFK6h6a3aqU3b8r6VqBfBA3gWNEVVpAjgvEdr1SxH4DzzEvx8qiGNkeN6FuwiNGvIgPQYOZzdLQ_oBRq6bCT7A3FYQNWwEAQLeCXvAC8KpC5GWLOFZ0wPdvd2bJ1-xEUQmklQmYLVsWVMkAbAvpl50p_Juas6qoS7Q_UUgIuQtrTdUwj-0ZX4oniNqmLDKiGiGUvUY1B13vhgknpRlSkXCLZLleZroJVm6sU9UWz7bC3YsNCiRAQXDBjYoZRCMX7CswA0zrzPlGnpHmyKyPwFHS2euZI7BqgNTh2XRIXYpIQDkrk-NE04LkTUQlUDg_CIvVsWzwQkvsAVGo14RKAqwKecI1ft0ZLDgmS34aJSSEuNmjQy7STNMNqr7DhJxOKWY5xrORH3quEc9haE4t-dRBOO2qvQCwVRElqWuCDWs2Ti1-yLybAiCi73MhTCosYW4Br4RBp5RRkyaR0vpsqyY2AJl7ugJ1ijlPiOvGJAoLk8SwhurU24wOyumwNMxi5hOCNWXjXYfZuYEve87DaYJZmBPfpy6lxolbI3K6rfGAsTesUmNx_zWfguuCmBdl36zQYTNkp8tZw_xPv8V6BHyiZrBGoe35FLEBePhKOgF0C6bfRxt30dqJTh17C5yXXylM20izNJUfCzNuxmeAhDEvSrjn0ygtssgfyoXD5J7i1b7TeHrfPXCoEaXYC6MfYg3o7QJdHxu6w1kQcc3j6ayABkEYBFGe0mBIBZjBvMGa7DBspw1U5IWRG8GyAxax5u92ecFHZ-ruwuttbjyOrFX3HZtCtK1LdtqXDJ_pq63zNafifE3n9uma5lJstQXMjlmNdo0ZZAPX5yfwtUhjdM5pv1qfyp9Fn8EtxC-STJyswC03nXRd3QpLbzrwkND_UcS_e16TJWnsu1lIkqGoYY0nql07ZORQGS8rsw4OF_ZuUzGV6FtzAnbkjSgyy3YwNN5Dd-F2gQ2falqZZBejlQe4pwdxRPMLL899N3EDd2irsOYgBzXYd4xR42nQgxCdn8tMLtKabLSyx_uPJWo7kwdeFuZ5EvkGuluTirczWXuMGdYiZbmWRQLSXc5ra4PgtqI0_ZeYZgYh1x4WA5xOlVZEbhgCLREGyAIDpqXrAnBFP1YITbPCC5M8Sgkze2aNN-5iZx6fTQSNlB5Rf503uTQxqLWP6FSR8DxP3dwvhhZIa6LRzrPuOY7IHWu0Adgmgyi9IeJ-kZaTeDnHUhSssMEbOw5PRHUxvIYnFL3s9EB32zXVFYZn4JpFA5SEUODOIXxUVSMD4RH7SqPd3eoRxJU2NdjNkZ0EpSsSN4oQSBmPMUxT7uEx7o5C3rfz92z6A9utZeFhv6Itt-GbbFlQSqzyNVKXd7ba1luMy1kWuG4EMXnuxwa3DPOdin-HDGfKopDJjOkSA8bKoN1ofTpYT2QqFmpwZKFXk6xWHaB3pi4hTMJmFQyguezs0U2t2EaqBy5FY8Bia9JRtvjBkxHEN9iGAq_JW9GCJO9S1SlA0PUFAOhSUCWzUYrGEY8AIZHH3IAXVqeaNYdqzlLZf4h0S0k2a3Aj6PAhwkE-IPmYRNIjfhPB5CEsxv2QR8JPlNEQW8hM5XZE3Qo_CII4YVFqdUQPY6u7G86xmVOhRmgeSEuXU2Lplvkwf1yykyBNPU5iTqNBsoeRVXsX9pw3hRVwJ0yyfDJkDNnnEyuz8UASD6s1BPAOiN6qrDFDQHWWYV5b00xjEYHvQRwYpGHqm3KENeu6U2H8aYOqOmsYubyIwhzQiIEI1uyqfvDBg6fOimBwyR1sIBXh4cBWkQ8yOZuWy1SXLoVJk36lkzfwptekUwJPKjHnAhsm3J36Gkuj1yIre6FziiLRXCN2F8k08zDRDDQbHW3KeUzjwmVG-KxBWav-NDoBO5T3uZulMXMLw2xrKNbKg-w97YrtcWeyrVzM_iCy6cWEkO4wlwXXoZX5dqu5zKE8UO0_s0r7OpEyxQwiAmKV_dtKbT2cleBJTKPAdwEcDQ1hw0CuSaPsP2lr6qXj2bSQxpnr0czNhnYOaxJ32JW9R2xrzMtiar_ajOSV8iD28oL5zAuHvNIwgWsY8rTRWtNcGrh-RrwsjYZRnGHa1rzk_mO0IlQYyUJ5aebmReIXuTdg9WG-djhEbu_BWSw5CpJzviRXJTZZYCWJgwlGEHsjVzThznOdx_zBM3uk1n71h9dvn__u26_Pn79--_L3z1-8PX_z6usX-CwwNYI4dC9YZwdfgyFtVa5E7hfCgXc66fo7rFYRHJoRceqd53b6Ya9f_vD8xT-dP__Hr86_evnmxbd_ePP9a_lid0aBf0KG3vOHRTD1fPvPiog_UiISHLc_v__PkMi_siIyGeqL1yWYz5b9b_-FEgG29_sDJTv9_YNVw7CywA4-qd5aqN6AIuHevHt3IsYv4DMx2HXy_v3d-W6ZBXqI8ntWl7Pc36-ZyC3Jwpgc4-jEy1llBZwjc9QQmS7UqDYEQdDWXJkeRnvo5XciRessAt1hzu32wFffOFsjKkDKTDJDM_jjCcRTyCa06irjf-8QnAwvNAcQHcDzruxxOhza3nmIfuRvBcm3tafj7clwe2L-4_9ledz9VAEzVW-edeb_dP_Y_GNnCHyagwICAFepl2WEpAW4TuaTgnghJRyT7oUfZUXhM98NSRySNKJ5kuccvG5UcD_OBfh-4JVuHxXgeWdhcuam9xwVYP4Q1fGogONRAcejAo5HBRyPCvh_eVRAEudFyPw8T4Idjwrwdzsq4GUvB8gtu2XV2598JoBz60iA7TLaHmcCmLYNVUQ48EwARx4JgMm045kAxzMBjmcC3DMRGoZBFCd5kbi7ngngH88EOJ4JcDwT4HgmwPFMgOOZAMczAY5nAhzPBDieCXA8E-B4JsDxTIDjmQDHMwGOZwIczwQ4nglwPBPgeCbA8UyA45kAxzMBjmcCHM8EOJ4JcDwT4HgmwPFMgOOZAMczAY5nAhzPBDieCXA8E-B4JsDxTIDjmQDHMwGOZwIczwQ4nglwPBPgeCbA8UyA45kAxzMBfsEzAd7_9D_ELHpe)
