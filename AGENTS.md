[//]: # (ob:e43408a0)
# Project instructions

[//]: # (ob:bbe579fd)
## Public contribution workflow

[//]: # (ob:34d3dbf3)
This is a public open-source repository. Contributors may propose changes
through ordinary Git branches and pull requests without installing Proofpress
or possessing any repository-level Proofpress ledger.

[//]: # (ob:1be95c90)
1. Treat Git commits, pull-request review, and the repository test suite as the
   canonical public collaboration record.

[//]: # (ob:950c5740)
2. Do not require, fetch, push, or commit `refs/proofpress/ledger`. A
   contributor's local ref is private local state and is never a prerequisite
   for participation.

[//]: # (ob:406bcda8)
3. For source-code changes, use the normal implementation and test workflow.
   Proofpress artifact snapshots are not used for source code.

[//]: # (ob:3ce94304)
4. When editing Markdown or static HTML, preserve existing `ob` markers,
   `data-proofpress-id` attributes, metadata, and portable capsules. Do not
   manually rewrite encoded transport.

[//]: # (ob:f5265244)
5. If an incoming file carries a portable capsule, `inspect` it before relying
   on its provenance. Updating a portable artifact must keep its visible body
   and capsule consistent, but contributors without Proofpress may submit an
   ordinary PR for maintainers to reconcile.

[//]: # (ob:2d919674)
6. Run tests appropriate to the change and describe user-visible behavior,
   compatibility impact, and validation in the pull request.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzc5NWU0MTc0YjU2ZDdkNWNmODkxOTNlYSIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
