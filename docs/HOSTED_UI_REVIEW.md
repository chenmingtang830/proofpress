# Hosted UI local review

Home is now an attention dashboard at http://127.0.0.1:7335/home. Knowledge retains the approved library and lineage on /ledger.

The dedicated `owner-local.py` preview signs the browser in automatically over its loopback-only listener. Its owner token stays in the local process and is not rendered in the page or printed during startup; do not paste or share the token. Normal hosted and self-hosted servers continue to require Owner sign-in.

If the local server needs restarting, run this from the repository root:

```sh
PYTHONPATH=src python3 web/owner/scripts/owner-local.py --serve-only
```

This mode serves the existing synthetic preview database and uses the stored local Owner token server-side to establish a loopback browser session. It does not issue or rotate credentials, seed data, or make admission decisions. If the database or preview credential file is missing, stop and resolve that prerequisite with the owner; do not switch to a seeding or credential-creation mode as part of this review.

1. Check the Home metrics, attention reasons, and direct full-review links. Queued/running model jobs belong under In progress; approved claims do not appear in the attention list. Empty workspaces do not invent outcomes.
2. Open Knowledge and confirm Map appears by default, with List still available. Select a claim node: its connected evidence should be emphasized and a concise preview should occupy the existing right-hand record area, not a second graph card. Use the quiet Open claim record action to read Proposed by, Approval authority, May support, and Limits & conditions. Try search, applicability filtering, and proposal-date or alphabetical sorting; expand supporting evidence and admission history. A policy admission must be labeled as a system decision rather than human review. Missing fields should say they are not recorded.
3. Use View lineage. Inspect evidence and related current claims, then return to the library. Owner eligibility must not imply access for every agent.
4. In Review, open full review and inspect the complete Relevant when and Validity conditions lists beside the evidence and checks. Inspect the separately controlled automatic-approval policy, its workspace-wide/high-risk scope, preconditions, and non-calibrated model gate. Reading the page does not require approving, rejecting, or requesting changes.
5. On desktop, drag the Knowledge divider, resize it with arrow keys, and collapse/restore each side; the opposite pane should expand without losing the selected claim. At a narrow width, open and close a Knowledge record, including with Escape and keyboard focus. At 820px or narrower, check that Knowledge lineage reads vertically without clipping. Confirm Home stacks into one column.

Validation results are reported per local iteration; visual acceptance, PR, merge, and deployment remain separate.

The preview remains a single-owner workspace with synthetic content. It does not establish team or tenant isolation, universal agent access, customer outcomes, or production readiness. No proposal: this is a local UI review handoff.
