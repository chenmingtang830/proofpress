# Hosted UI local review

The owner workspace changes are ready for human visual review. Start with [Home](http://127.0.0.1:7334/home), then [Knowledge](http://127.0.0.1:7334/ledger). The Knowledge label keeps the existing `/ledger` route.

If the local server needs restarting, run this from the repository root:

```sh
PYTHONPATH=src python3 web/owner/scripts/owner-local.py --serve-only
```

This mode serves the existing synthetic preview database. It does not read, issue, or rotate credentials, seed data, or make admission decisions. Use the existing signed-in browser session. If the database is missing or the session requires sign-in, stop and resolve that prerequisite with the owner; do not switch to a seeding or credential-creation mode as part of this review.

1. On Home, inspect the next candidate statement and proposed use, open its review, and return. Check that Available knowledge shows useful statements rather than a metrics dashboard.
2. Open Knowledge. Try search, applicability filtering, and proposal-date or alphabetical sorting. Open a claim and read Proposed by, Admitted by, May support, and Limits & conditions. Expand supporting evidence and admission history. Missing fields should say they are not recorded.
3. Use View lineage. Inspect evidence and related current claims, then return to the library. Owner eligibility must not imply access for every agent.
4. In Review, open full review and inspect the complete Relevant when and Validity conditions lists beside the evidence and checks. Reading the page does not require approving, rejecting, or requesting changes.
5. At a narrow width, open and close a Knowledge record, including with Escape and keyboard focus. At 820px or narrower, check that Knowledge lineage reads vertically without clipping. Confirm Home stacks into one column.

Validation reported for this implementation: 31 unit tests and the full owner browser smoke suite passed before the final corrections. The latest build, bounded Knowledge tests, and correction browser pass then passed. An independent finish review marked the mobile lineage, nonwrapping Review button, and Home empty-state spacing corrections resolved. These checks support implementation behavior; Richard's visual acceptance is still pending. This guide does not claim the changes are merged or deployed.

The preview remains a single-owner workspace with synthetic content. It does not establish team or tenant isolation, universal agent access, customer outcomes, or production readiness. No proposal: this is a local UI review handoff.
