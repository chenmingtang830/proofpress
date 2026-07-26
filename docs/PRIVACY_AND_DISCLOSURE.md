[//]: # (ob:be94d633)
# Privacy Boundaries for Portable Artifacts

[//]: # (ob:9db57e7e)
> Status: V1 product-boundary contract
>
> Date: 2026-07-22
>
> Scope: artifact policy, ledger admission, capsule visibility, stopping
> portability, manual drift, correction/redaction, and minimal edge cases.
>
> Out of scope: fine-grained ACLs, online key services, multiple-audience
> publication streams, legal-retention policy, and real-time collaboration.

[//]: # (ob:599b267b)
## Read this first

[//]: # (ob:fe6e310c)
| Question | V1 answer |
|---|---|
| Can a recipient inspect the capsule? | Yes. Treat every raw portable file as disclosed. |
| Are prompts and private reasoning included? | No, unless a user explicitly writes them into admitted document history. |
| Can an old copy be recalled? | No. Stopping portability affects current and future copies only. |
| What does a merge disclose? | Only public records already present in the supplied capsules. |

[//]: # (ob:ca1fe953)
Use the rest of this document when choosing a policy, handling drift, or
reviewing an edge case.

[//]: # (ob:38c20796)
## Executive decision

[//]: # (ob:552f8a90)
Proofpress does not build its privacy model around a “share” action. Users
continue sending files through Slack, email, Drive, or other tools. Proofpress
does not require a publication step before every handoff, and it does not
pretend to know whether a file has been copied or forwarded.

[//]: # (ob:7407f209)
V1 needs only five rules:

[//]: # (ob:ee94d49a)
1. **Declare portable once**: portability is a sticky artifact policy, not a
   switch for each share.
2. **Record selectively**: record accepted versions and consequential
   decisions, not the complete conversation.
3. **Raw holder can inspect**: anyone holding the raw artifact may be able to
   read its capsule; hidden does not mean confidential.
4. **Stop prospectively**: disabling portability affects the current and future
   copies only; it cannot recall old copies.
5. **Never hide gaps**: show uncaptured or unattributable changes as drift or
   unknown rather than guessing provenance.

[//]: # (ob:c9d68c4f)
> **Append-only begins at admission. It does not mean capture everything forever.**

[//]: # (ob:6a6c293a)
## 1. The right mental model

[//]: # (ob:5051a788)
The old model was too centered on publication:

[//]: # (ob:d411f78c)
```text
local journal → share preview → disclosure projection → disclosure stream → shared copy
```

[//]: # (ob:d3c3fb06)
V1 uses an artifact policy:

[//]: # (ob:76e10073)
```text
                  make local
PORTABLE  ─────────────────────→  LOCAL
   ▲                                │
   │ explicit enable                │ ignore
   │                                ▼
   └────────────────────────────  IGNORED
```

[//]: # (ob:2f0cb618)
These states answer “where does history live?”, not “who has access now?”:

[//]: # (ob:61f99e53)
| Policy | Ledger behavior | File behavior |
|---|---|---|
| `ignored` | Do not capture future changes | Ordinary artifact |
| `local` | History remains in Git/local/backend state | Raw file carries no portable capsule |
| `portable` | Admitted events enter the same lineage | Raw file carries a safe capsule |

[//]: # (ob:595556d3)
Installing Proofpress must not automatically make every Markdown or static HTML
artifact portable. After a user or agent explicitly declares the policy once,
it persists; later admitted versions inherit it without asking again.

[//]: # (ob:ae4bcddd)
## 2. Ledger admission boundary

[//]: # (ob:092c1fa1)
The working body may contain scratch material or be ahead of the ledger head.
Not everything written to a file or seen in a session automatically receives
append-only semantics.

[//]: # (ob:ab8d506b)
### 2.1 Included in the ledger by default

[//]: # (ob:f84efabd)
- An artifact version the user accepted or that completed the task.
- Computed semantic changes from the parent to the new version.
- Author-submitted change claims and their verification result.
- Requested, produced, edited, and recorded actors, plus attribution basis.
- A concise, artifact-facing reason.
- A consequential rejection future agents should not revisit.
- Corrections, supersessions, and detected manual drift.

[//]: # (ob:78e5757c)
### 2.2 Excluded from the ledger by default

[//]: # (ob:0766d40e)
- Raw prompts and complete session transcripts.
- Chain of thought, private reasoning, and tool calls.
- Every save or intermediate token state.
- Casual brainstorming and undeveloped options.
- Verbatim Slack, meeting, or voice transcripts.
- Source payloads, secrets, credentials, and local absolute paths.
- Context the user explicitly marked private or local-only.

[//]: # (ob:3771c1c0)
### 2.3 Consequential-rejection criteria

[//]: # (ob:1c3e3dcd)
A rejection should be recorded only when all of these conditions hold:

[//]: # (ob:31da1e3a)
1. The direction received serious consideration.
2. It was abandoned for a reason that can be stated.
3. A successor revisiting it would waste work or undermine an established
   agreement.

[//]: # (ob:af2b57ac)
Record a concise rejected rationale, not a transcript of the discussion.

[//]: # (ob:886e450e)
> **Record the decision, not the conversation.**

[//]: # (ob:ee2856b9)
## 3. Core invariants

[//]: # (ob:e2605fb1)
1. **Sticky portable**: later admitted versions of a portable artifact update
   the capsule by default.
2. **No per-share ceremony**: an ordinary file handoff does not trigger a new
   permission workflow.
3. **One raw artifact, one holder boundary**: anyone who can read the raw file
   is assumed able to read the capsule.
4. **Hidden is not confidential**: being invisible when rendered is not
   encryption or an ACL.
5. **Selective admission**: raw conversation, scratch material, and private
   context stay out of the ledger by default.
6. **No silent rewrite**: errors in admitted events are expressed through later
   events.
7. **No offline recall**: a distributed plaintext copy cannot be remotely
   withdrawn.
8. **Deleted body is not deleted history**: once an old version enters a
   capsule, deleting it from the current body does not guarantee its removal
   from history.
9. **Unknown stays unknown**: do not invent an actor, time, or reason that
   cannot be established.
10. **Gaps stay visible**: body/capsule mismatches, missing events, and stripped
    metadata must cause an explicit downgrade.
11. **Private interval stays private**: re-enabling portability must not
    automatically export intermediate events or payloads from a local-only
    interval.
12. **Precise trust labels**: computed, verified, attested, self-asserted,
    unknown, and redacted must remain distinguishable.
13. **Portable merge unions only disclosure**: a multiplayer merge may unite
    only records already disclosed by its input capsules; it must not read or
    copy a private interval from any participant's local ref.

[//]: # (ob:a092554e)
## 4. Capsule visibility and content

[//]: # (ob:aeff8148)
A capsule is the lineage's self-contained portable representation, not a
permission system. Anyone holding the raw artifact can read it with text tools
or a Proofpress-aware agent.

[//]: # (ob:d7ab5925)
### 4.1 Included in a capsule by default

[//]: # (ob:9efa1c70)
- Artifact ID, policy, protocol version, and current head.
- Current body digest and event-parent chain.
- Safe checkpoints or deltas for admitted versions.
- Semantic changes.
- Claims and verification results.
- Actors, timestamps, and attribution basis.
- Admitted reasons and consequential rejections.
- Correction, supersession, redaction, and drift states.

[//]: # (ob:2df8ee5c)
### 4.2 Multiplayer portable merge

[//]: # (ob:1b38d216)
Parallel copies of the same artifact may disclose different capsule branches.
During a merge, Proofpress verifies the common ancestor, unites only records
already disclosed in the raw files explicitly supplied by the caller, and
creates a multi-parent event referencing each public head. The local
`refs/proofpress/ledger` is a more complete record, but it is not an implicit
input to a portable merge.

[//]: # (ob:b0960269)
Therefore, a merge does not automatically expose drafts a participant did not
submit, local-only actors or reasons, sanitized private intervals, or other
repository files. A fact that belongs in the merge record must be explicitly
admitted by the caller through the formal merge's actors, claims, reason, or
rejection fields.

[//]: # (ob:49aae806)
### 4.3 Excluded from a capsule by default

[//]: # (ob:e924a924)
- Raw transcripts, complete prompts, or tool traces.
- Private or local-only event IDs and omitted-event counts.
- Local paths, environment secrets, tokens, or encryption keys.
- Source content without explicit admission.
- Every intermediate body saved merely for “completeness.”

[//]: # (ob:f0f6e462)
### 4.4 Risks of deleting content

[//]: # (ob:f8360c02)
Portable history may contain old checkpoints, deltas, or deleted blocks.
Therefore:

[//]: # (ob:a57d5e5c)
> **Deleting text from the current body does not prove it is absent from the capsule.**

[//]: # (ob:507eb82f)
If content must not be visible to a raw-artifact holder, no version containing
it should enter the portable lineage. Putting it in a capsule and later
deleting it from the visible body is not a privacy control.

[//]: # (ob:483804ed)
## 5. Ordinary handoff, not a share state machine

[//]: # (ob:49dd8fc0)
When a user drags a portable artifact into Slack or sends it by email,
Proofpress does not create a `disclosure_event` or require an audience
selection. The file is simply copied as it currently exists.

[//]: # (ob:886e00f6)
Proofpress cannot reliably know:

[//]: # (ob:184d2482)
- Who actually clicked send.
- Whether the file was opened.
- Whether a recipient saved, copied, or forwarded it.
- Whether a local copy has already left the device.

[//]: # (ob:abd89abd)
The protocol therefore does not define `disclosed_by`, `sent_by`, or
per-audience streams, and it avoids promises such as “unshare everywhere” that
it cannot keep.

[//]: # (ob:97f6f122)
## 6. Portable lifecycle

[//]: # (ob:24a6662e)
### 6.1 Enable portable

[//]: # (ob:2d7504b2)
Enabling portability for the first time is an explicit artifact-level choice.
The system should explain that future admitted history will travel with the raw
file and that a holder may be able to read content later deleted from the
visible body.

[//]: # (ob:99efd910)
After enabling it, no repeated confirmation is needed for each version or
handoff.

[//]: # (ob:81f914b1)
### 6.2 Continue portable

[//]: # (ob:7e55157e)
When an agent completes a revision the user asked to retain, or the user
explicitly accepts the current result:

[//]: # (ob:cdb74d1f)
1. Compute semantic changes from the parent to the current body.
2. Accept actors, claims, a reason, and any necessary rejection.
3. Verify the claims.
4. Append the version event.
5. Refresh the capsule atomically.

[//]: # (ob:645c4ae1)
Casual discussion and unaccepted temporary states do not enter the capsule
merely because they occurred around a portable artifact.

[//]: # (ob:58cac2dd)
### 6.3 Make local

[//]: # (ob:2c9d0822)
`make local` means:

[//]: # (ob:f3548215)
- The current working artifact no longer carries a portable capsule, or the
  capsule is removed on the next materialization.
- Later admitted events enter only the local ledger.
- Stable anchors may remain.
- Previously distributed portable copies remain unchanged.
- Disabling portability does not automatically delete the local ledger.

[//]: # (ob:8c9204c8)
This is neither recall nor erasure of the past.

[//]: # (ob:697c7f40)
### 6.4 Clean copy

[//]: # (ob:b454588d)
A user may generate an ordinary capsule-free copy from a portable artifact. A
clean copy:

[//]: # (ob:859b076c)
- Contains only the current visible body.
- Does not claim to carry complete provenance.
- Does not modify the source artifact or local ledger.
- Does not make previously distributed portable copies disappear.

[//]: # (ob:3e4ed2f7)
### 6.5 Re-enable portable

[//]: # (ob:1b4a1e02)
Re-enabling portability is a rare, explicit transition. V1 must guarantee:

[//]: # (ob:14bc1711)
- Event IDs, versions, actors, reasons, and omitted counts from a local-only
  interval do not automatically enter the capsule.
- The current body may become a new safe checkpoint.
- Continuing an old portable head may express only the net change allowed for
  disclosure; it must not leak the intermediate private graph.
- If safe continuation is impossible, begin a new portable lineage or derived
  artifact instead of pretending the history is complete and continuous.

[//]: # (ob:ff98d967)
The implementation specification freezes the continuation encoding, but the
privacy invariant remains: **private interval stays private**.

[//]: # (ob:a74d9489)
## 7. Manual edits and attribution

[//]: # (ob:6761d19f)
> **A document can detect that it was changed. It cannot know who changed it, exactly when, or why.**

[//]: # (ob:b0624cf8)
When the body does not match the capsule head, Proofpress can establish:

[//]: # (ob:a1e83e45)
- That the current body contains unrecorded changes.
- Which blocks were added, removed, modified, or moved.
- When the current tool first observed the mismatch.

[//]: # (ob:669c59c4)
From the file alone, it cannot know:

[//]: # (ob:cbc60133)
- Who made the change.
- When the change actually occurred.
- Why the change was made.
- Whether it came from colleague feedback, the user, or another agent.

[//]: # (ob:02196bad)
A detection event should therefore look like:

[//]: # (ob:9d551f6b)
```text
event: unrecorded_edit_detected
what: computed semantic changes
edited_by: unknown
authored_at: unknown
observed_at: attested
why: unknown
```

[//]: # (ob:8261234d)
Actor roles distinguish at least:

[//]: # (ob:f1daa663)
```text
requested_by
produced_by
edited_by
recorded_by
```

[//]: # (ob:618dd688)
Each actor has one of these attribution bases:

[//]: # (ob:86c9996d)
```text
signed | environment_attested | harness_attested | self_asserted | unknown
```

[//]: # (ob:5b630bcc)
`signed` is reserved for a future cryptographic signing implementation. V1
rejects it as an input rather than overstating attribution confidence.

[//]: # (ob:12d61fe3)
The signed-in user, file owner, or agent running the hook must not
automatically be treated as `edited_by`.

[//]: # (ob:4d62bb79)
## 8. Correction, supersession, and redaction

[//]: # (ob:bfc61b9c)
### 8.1 Correction

[//]: # (ob:c2d65249)
When an actor, time, or change account is wrong, append a correction that
references the original event. The default view uses the corrected
interpretation while leaving the original record visible.

[//]: # (ob:b46a45ef)
### 8.2 Supersession

[//]: # (ob:2218bf81)
When a conclusion or body later changes, create a new version and declare what
it supersedes. The old version remains a historical fact but is no longer the
current head.

[//]: # (ob:6ecc8d68)
### 8.3 Redaction

[//]: # (ob:3202fe48)
When a sensitive payload has entered portable history, a future capsule may
append a redaction state and remove the corresponding plaintext, but it must
make these limits explicit:

[//]: # (ob:7ccd86ac)
- Old copies may still contain the original text.
- Removing the payload may leave some history only partially verifiable.
- An ordinary hash must not masquerade as secure deletion, especially for
  low-entropy content such as names, short conclusions, or API keys.
- V1 does not promise crypto-shredding or remote deletion.

[//]: # (ob:4779c987)
If even the event's existence cannot be disclosed, the safe choice is to
create a new sanitized or derived lineage and state clearly that it is not a
complete, continuous projection of the old history.

[//]: # (ob:0d3174f5)
## 9. V1 edge cases

[//]: # (ob:a24edc0a)
| Situation | Behavior |
|---|---|
| An accepted v2 follows portable v1 | Append v2 automatically and refresh the capsule |
| A casual branch is discussed | Record nothing |
| A direction future agents should not revisit is explicitly rejected | Record a concise rejected rationale |
| A user edits directly in an IDE | Compute drift; keep actor, time, and reason unknown |
| A user makes the artifact local | Stop future embedding; leave old copies unchanged |
| An artifact becomes portable again after a local interval | Do not export the private interval; use a safe checkpoint or new lineage |
| A recipient changes the body without updating the capsule | Report a body mismatch and mark unrecorded edits |
| A recipient makes the capsule internally inconsistent | Fail chain/digest verification and report tampering |
| A holder replaces or rolls back the whole file with a self-consistent copy | Detect only by comparing an external trusted head, witness, or checkpoint |
| A recipient copies only rendered body text | Treat the capsule as lost and downgrade to an ordinary artifact |
| The current body deletes old sensitive content | Inspect the capsule; do not assume history also deleted it |
| A user generates a clean copy | Carry no capsule, claim no provenance, and leave the source ledger unchanged |
| A distributed copy needs withdrawal | State that recall cannot be guaranteed; send a replacement |

[//]: # (ob:2c249df0)
## 10. Explicit V1 non-goals

[//]: # (ob:14d8b083)
- A share UI before every file handoff.
- Disclosure streams and audience labels.
- Per-user or per-field ACLs inside one offline file.
- Automatic projection for multiple audiences.
- Online key revocation.
- Remote deletion of distributed plaintext files.
- Automatic sensitivity classification for Slack, meetings, or spoken content.
- Packaging complete session transcripts by default.
- A complete signing and organizational-identity system.
- One blanket promise covering every retention or privacy regulation.

[//]: # (ob:0444a90a)
## 11. Release acceptance tests

[//]: # (ob:3208f8df)
Portable V1 must pass at least these tests before release:

[//]: # (ob:ec5f7bca)
1. After enabling portability for v1, an accepted v2 updates the capsule
   without another permission prompt.
2. A casual branch creates no event; a consequential rejection creates one
   concise event.
3. The capsule contains no raw transcript, tool trace, local path, or secret.
4. A raw holder can inspect the capsule; the product does not describe hidden
   data as confidential.
5. Changing the body without updating the capsule makes `verify` report a body
   mismatch.
6. Making the capsule internally inconsistent makes `verify` report tampering;
   detecting a self-consistent whole-file replacement requires an external
   trusted head, witness, or checkpoint.
7. Manual drift is not automatically attributed to the current user or agent.
8. After `make local`, future versions are no longer embedded.
9. Re-enabling portability does not leak local-only event IDs, payloads, or
   omitted counts.
10. A clean copy carries no capsule and does not modify the source ledger.
11. Stripping metadata downgrades the file to an ordinary artifact rather than
    falsely claiming provenance remains.
12. Correction or redaction does not claim to modify or recall old distributed
    copies.

[//]: # (ob:9e0d89d9)
## 12. Minimum release promise

[//]: # (ob:1501efd4)
> **Proofpress can make an artifact carry a checkable record of its admitted changes and attributed decision context.**

[//]: # (ob:f9cbd5f9)
It does not promise:

[//]: # (ob:aae706e7)
- To record every change that ever occurred.
- Strong identity authentication for all provenance.
- That an admitted reason can be proven true.
- That hidden metadata is confidential.
- That shared content can be recalled.
- Different permissions for different holders of one offline file.

[//]: # (ob:3cb7a253)
The final product mental model is:

[//]: # (ob:bb79d355)
```text
Choose once whether the artifact is portable.
Record decisions, not conversations.
Let admitted history travel with the work.
Make gaps and corrections visible.
Never pretend a distributed file can be recalled.
```

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzYxOGFhNGZkODJjZDY5ZDA4NDE3MjE3OCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImNjOTBkMzBmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8zOTY3NjE1NmRmZmNiOGI4MGFiNTE2MmUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzMyZjFlYzhkYTRhYTUzMGY2N2E0MWZmYyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrsvXlzHFWWN_xVMjx_TASPJOe-iIh-wgNMjyOg4YVeYqJF2Dczb0o1LlVpKqss1E1H2IDNZmwDBhowW7OYodtLNzQNXvB3YVSS_Nd8hfecu9eilFRVpp6JKJrulkqV9948996zn9_5_SHSatcKkrWP1fJDi4fW1o6FTkyIX-Sxm-Vhktux70SuE8WH5g6lzXzjWF5bpmUbvluuEDcIF0kRRjSnTh7nhe9HtuMWxPdJGOe2U7iuE2YpSbOE-o4TZAEhRRAmvkPj1CdekLsRjJvXyqx5krY2Di3-Hn9pH2uTZZihTto41Rz8kNI6fPBr2qoVNZLWqdWiJ2tlrdmwVuD7zdaGlW5YT7SazWKtRcsSnlkj2QmyTPGlej5uNf-Dwut2WjjgSru9Vi4ePrxca6900oWsuXo4W6GN1VpjuU0ay7FnH-55ukX_s1ODn491Sto6ljUbJW0ALdqtDv3D3KEVSpCIWZbYuWcXh_gnx-hJ9iUgLj3mJWEUOkGYF0WWxmlskzRwQpfiypqtNr7asXqtQWHlckfqxzy3cGgW58QnJICBw4j4DgzAX0es7lhG1spOHV7YxXVmzVZeHlr87e8Piel_fwh2udkq8Sf-Z5ofS4Hkvz2UNXP6zKGn4Q3kaYCJ82ZWHn7iyaO_PvLQvx878ouHjz189KmHHn38qV89-cjCan5o7kAnh7TbrVraacOGHUtJWSuR9qTVwHXD32CXKRuy015ptnCFJ2oNHLXcgL-swl8aZBW3kq907lAJD8JYhxYbnXod1p2twG5R_r5pvZmdgO-mNPHz0PPg67BRbfoMvtUTrdpJkm1Y_9LsNHLSqtHSKpot6wlBe-uIJMCcXALJc7a2NTxxdB0--Sdrv6PgkWlvrOHK8STAqTr0hzm9wiRPg4hGdOIr_Jm1_cq3W6dO_8_t937tWJs3r3TfPL3zw_fbb53rnv1659q17S_vLjV-Bv9aW-98vnX5I_iea7vhvB3Nu674y86557vvfwN_kftsrTXrtWzjv0-drrPpxIutkRbpeSsvzlw7SsKet9q-9ebOtZvdMy_tfHKukrb_ZPV9tYJ-QeAWMUnskWbSzMLafu-Fe-9d3L5yeuvLT7ofvrr53Wvw5tu33rJ-PHUZuFyL_njqA6t76-b2n1_971PPbV_6cuulf2zfurJ96-q9U-_t3H3ReqoOzAYIc--5a5u3voUfHoZNpNbWS293z3y7eevt7j8-7575R_fC6_dOna6gXOTbUeHayUjvAxvdvfDVvcundr44vXnz0tYHn-xceaH70ruwgxVTUrwkfkJGmtJZsB544GGa1YFElmRfVrOR0QcegGnVJ1t_vG6pUwTEtsp2LTuxAY_oldWBjfesLEvyMM78YqSV_QwWdgT4bSOfbzbqIBzocq1RWqRtkXy1xnjHgnW0beVNuF6NZttapaRhAQdtd1oV1ApJmLmJ10stoMLW1U-3P7kGb9a9-_zWuzf5MdrjmFc8VnXk7cAhURyPvYKtd67wL8H57d78Qhz4tU4Kd5wgn7a2PnwBznz18clBqhdRnI29nOPHj-PTSw0YmNSt_2h2Wg34_x_PvmGxG2iJr7JPUF-oN8sO-5iJ85pxklBG9C7Sy7witcOxFwlX7N6LL8L9t_p4YjWRopA6th15kyOSNfDPKjlBLUa7pcYTjz_5yyP_8ugjlvXjpVP7-beCdm5hZykI9rHXvnP33c2b73Ox1H3_w-2rl4C5ds-f7V74W_fyl903v7r34jlgs_9z-9zOqXPAgYFnwBd2bpzePn8DvrB1-eWtD56_9-5F9p0qaodOkSQ0GJ_az4LMxc21nrUepfkybVnAdDa_uwm_b739IvB5-etS49n5-Xn1X_jVOl5bbjRbND8OX8aXee0tvWLGE3svdRIEoBKOv-TutZd3Pj1j6ME4effmpZ0Xv-q-8uXWK69svXwKKGk9Rlon8uZ6AyUUMGO475n1b7987FF9rneu_YDvBiy8gtSE-mmW53nPut0FSS7Faq2U6zIbe7DEPR6tYIt24mZOQZyJrOQ3zRb8bdlCcwdk6vXNW593z53pXvyzVWYt0s5W4JBufv8R_8u9P50FcbR587xV53Ph8kBL6H7_7b0PPuT07p59t3vmc35oUCd48SY_1FZJq6ibxnlgh2nfOwEPuvXHnWuf7dx9HwYVs1YTFim722MVRC1inxYkzcddwLwlVKZPrsFjm3c_2H7rXSDD5q1b3Vc-6V47t_XSRaBT986f4AfUDtQhBJMQN-1_br-_1Ji3Nm-dt4BIYMxY3ZdubL19Q_6dqRQVmkQU0yAKoqzvPVzxHnBFDkjLiierzmgUhrlv0wksY95qkXWUfatrbbzj55GKb31jCbPIardIA85qba0taAf2Ua0x3yzmwb7qLK-0QUUFdbd7_ezW-S8rKOdFkZM5md23ZM96CC3f_-zAXtRASrcol8EN2JjPtl67tjcF9zFCBSWdzKNenuUTXBaoznhRL57beufbrVuf7Hz79eZ3r3ZfegfUaLi0yIIvfgG209bLjJ1eu9G981a1GPKcnDi0T1Ucb40gEVCKfvfV1tvfdy--vvOnP8Ox2b780c6p53fefR30OLbZwPW618B0-3jzu1PwXc6ldj75cueHH-A1ti-e3b70V3h069IP3dvPsyc8eOLieTBodk6duffia1sXLsIAm7ff2_r7VzvffA-2y-ady3Bftz_-pvvBhe4__gYjwU3tnvnrzvWzwOkqzg8pXLBwSTZBInDaw5uAggBv2L3w-fbffth-7jbyAD4OzeF24GikTpFTM11i59qXYDjcO3Wxe_UdsH57lj2wd3EcUj8YuKnjLBsNkieZ18Vqr1ArpxnzXs0x4wM_gYmQnbGFLzzwQKXJ5sZBmPZaibCHWx9_B3oCCvwLf7z34oU9ZO3QByruHHVDOyhSZ4xZmbn4lDT9uG3YayiyewYn8SqT2G3cSsnjOZPcev8bZPwZqTh0QUyiJMn8MVaKGjUc9O6Zv3Rvn4JFyQuPh6n7wzs71291L7yNkvyz17ovfdu98BywYLg8W5f_0r18A85FATz5Kp7INXTmtKlVg3W0TpJ69bkjoMYEgd977vwF6yHu2WPkuXB958rprVNXkOmfPdO99v0e-7yPxyt2ndCiiB0_ntiK5IPoEhB-Tu4RoPViHqcAOQW7rk5Ei6IeCxeOXQy-A1X2aETSAIjYt15HLZgfI1Op20tY7fl0lYMP9Ccni-wJLWdeq0ZHHwYRrhxyoAm0m1mzrm5L941zVtZpMWUJFybVAPio4ua4eRFTGmR9y_Ws7mfvbd68qXdllbaW6d6E2_3BKuGeenHuOuH4iwBpDhKix_MEWjlYbcBs15Rmf_EFtI7YTcfbffEcHkfhSwfGfnbr0nVU5y--BM-CcgBHECxsbWDd--rczvUqp15qJ6HthskE3uf9j7eufgYL0Aznb5-gYXzh4ubNz5BNvfYyk22nmSOAe7640_9wi5IShBf8DWX_d2fuvfuZwZ-WGoJBVbyHnxBCY7t_X9y-s8w55H6v1h5PV8mjxPUJ_HdCy-EatdabgVBCp-ZaNrOU2024YvCdjIr7JMh3WNG74nIVdgFaRegOnoOXPobd4KwTPdGfnr_37n_t63Lt8mClSeeFdmZPYBEqHiHjbygHnr_DKb31zhUwOWh2Yq0JBwtomdN6mzAawk8U5TpbUYk3S5zqKmWaBFEeDGVMB132z5jHGpaABj4OZBWwv1wDE_ySmf3KMQzbfxLkd9uqlRULDOyIprFbjL_A7hfPbX14GfjW1rW_88eEC-f653Bz2SlVDG2lWc9py9q-DJbKDeQLN_4qvnztv_hGgCKP11yKBWFgcpZTdddjL7Z92mtgBaBCvXvt3qn3rBXSyJtFoZRr4aLlzr2tyzf3UEkONFDFYfaTPI-LPut0MqvkDoutV17R7FlRfevVt4GOPObDQjwsrMNDP1xA9PnfXnq_e-umdZx7rfcwO2zgEvfhfXpXhPf0wvV7H3y8_dHn906_WX33nNjPXT9278Oq5i30717-CP2cz33fffHW5s2znJqCvwqX2R-vg_WNcuvlN0FKy79d-hb-BhKU_3nz7gfdq39Ets10ctiXnTt_gcHktz-6iIYzU9C7L1-HH_hjoOVv37qw_cUtGHjn2g_dz17cw6JN8zjp94lNhhqcEXZfu7Bz7Rpu0rUftu9ck8emZMH64_B-x1Ebxp8ZO12jrXnSyWu0kVGrbIOYX-XeSRhh885djFVU7G0SFWHhuL17Gy7oYHO9VtBsI6vvoexZuz1TcXtBfIchz3ww53asRxpsGHnx9pKEwx-pmjiPAttP3XEm3v7LX5BF_-UTizZkiJN_sPXH89xnrxjGfJ2epHXr3qmXt179L4wff31r-9ZHjKV_A9-G27d1-autDz7XNi8XqVX7BoZFnjj2OK8gvgr29tY7H9-7fAqDLNcvwCXZfvklvB4vvQ2_wgvxCwmM7d6Lr8Hd4k7cPfwnTpE4fp-vIETdDH6rNToH2dzhD1Vsb0SDwAkiOt7k3TtvWmCboq-ZOai5QNj54vTWX5_jHmzY4s2717YufQ_3Db1jXGLw3Wc0giG6L7-2fetNkOdMLlRx2SxPIz93ivFWjR7Ca59sX3tHOsoxWtqj13Bbe5U0MOQjsmak23Dr_OfAVIXFUMEDQz_IfELH3N6HSNkhdRbL7ZTSaIWbAHyeB1mRwN99A5Tj3BMZ2u33mF_zJpzJ7UsfYQRlUDx3X_-y-_43oArxoBeI6iq9Lc5I5vZFsELQ2x5T8dS9j2jft6tYT4ZpUQP8dr_THddR3uPWzidfbn-2R3i-8AKQ3E4w4nzzFj_D3AWsSYxKzdnXti7e7H73hd4BYTPz67B56_zmd68KHrkKNlKrRuq13_HMgoqzFWeJa_tZPOKKmX-cCd4Wha_WlSyEj7Ze-R5UcUx3OH-rmn-FSZRFhd_PXn3roTpLE2mubex9Kvq-XXEqUj_wgzjOR5yOcx7uzWAxsoErAXcFY2zvfKz8Gug_ZxoL14WAHHqu6iMVB0lqR2E24mLnMUlJ2Cb8bHH34dVPQdeTgT44Xp_e2L5yg58wbYefBGHbUMY3MgTGgLduXjS0c1CKeA5JlTHuUbBu3CLqe4vAepLO04PqH7s8Venj8olDbXfM6TFY8_YN0Fy7F6-jOnvjdSAlqIhaB2EOjRpeOthizBC7e-beJ7dAgO1cP72H2u-nmRM5zphLnLcMX5T0gjMpxNJSraMPo0-KqxzwA5c98MP6ygZzYjaFSpRVpYoVRRLnSTjubnbP_GMTxH7GpRhnVaBXN3H7LBQ2tdW1Ol2VzmirXKMZOvq7Z0GhexNZzZ2z3CWUbVQ5M0DQJ37c6xCMFiwwZYDRbt9-e-eH19GXfucNEHZ76N0Vj1UcP0xBzp2kGHsFLM3OyptZB6kC3KVh5bRNMwxpkTZ6TdZJKdSMnCXcwVfQq3Ki0ax0mYaunxXx2OvjzhSu-cADiv0hURibOff9vTOv9VrsnJHC_elee28Pr5RDY2AkwdjLlHKWc0Gu3IApjMoQCzx1L_yxe-5twfa6b361efN94T-z2GDWYRB3q8Ae8adVOK9FTfx4skqNC5Ms6I-TjUTla89zp8LmrTPdF69yo30_roUszULb6cvQHo2AOzdOc0Vd6uRcRLBfutc-vPfuGU5WtGPe-ab3z-c_guF7PuK-AbDJUIe8eG7z5qvdC6_d--IlZFVcz7_8F_Q8oPPnCx5n59ZCtfPAdp0kTEk-PsWZq2Dr01Nbf38VFgfkBnNy-6-3Nm_frqZ4koNxVPTlFI2yApWKyNj4otVpqJoCmtfaxzgboPlSYx04wSIw1dW1DjJyZnxUJBzGbui4nj8-jY6gKLFazTotrZ0Xvwbh2D13s_vS2T00ZicnJAy9yREIS0ZYfcOxdGOpAVpM3snEL0gp8aNRkbHUgGcrKBQ6cZ6H8fjckZv73N5jItmo0rBYlQa6NfZQB8MsSZIwnxy9ytoyRoCfBdF7stZqNlCyqBoR-Li_bAQ-Kiuo5bh56BR0_A0V5vy7tzD9hDEB1LQYr7Oa6w3aQtVz5-5FjC-uNJsnOEWZC-EesEbGILlJun31ZcZUzlvH1Qk4Xm2R-HnopmnUqzPEC2Bxg22fcf3udNlZoy2ZAobirkVzwv64hxZxoIGqDJkiC500yfpW6Rij76VND3y7Yjow3MPA9ZMRp2MM4r-5a-udb9Bu4IoKXIis2UHPz9l37116l7v0CSsmADYmR7a2zr3Yvfg6CA-uycL-ibTIK2erVBs_JH5Ai741u9ZTBs33JtLA96ucDq4Tp0XsjDwlL7pAhyDXTy6eB8mIgvPCHzlxeITDzMjsfv8tmHBgh1jiLOUUY31b71zhqv7mLbTIefo3StdrH3L1WXgWwH4XXqsqK51mWQyMsO-9PND693XskY69X64goufabkH9ESfbeuvC1gsfWWtko94EzRNz6MxInBFF5QQVDmGVhcBz-O7e6b7ysb6LVY79KMvyOCTZaMudh2Vc4Z4BHtWF7RI2-_mPtJ2-feXWvXc_02918Tws_d7zX4KQFYn9F76Ch9EXyfLlTrLqzUxk8rAhKpQlP4qSLImj0V6Ba_47dz8U6tHVP7Iigr_s3Pyz4sZbr_z53uW_4fm99nL3zJfcQQ9nT7hL3r7BnKWkAfbz72h-OKdY1JXLtCV87vtvuanNNWD0MQHd2KtX7I2de07kF71mQ7JggXmOib-w63An9-DYQ75elcXl-jTPbDLyjM9aW8-f6Z79O8jaIUUPWPBw0lFnGQnDcrmRkdI1lsTnwpPwP1z-WaSqGMLNgKXnRa_zzbHZajm1kUmcfm-v8qqhT1T5ZPw8Tu3YG2deuDgsZsLVAh45QaUBzxELBP7qqDj4RgkTj9qxNG5LhfJYxTN65qvMCd_3SdK3rY6zADekTmFLBf3RZWahrrTXodrj0WruGBdxXkxkJSqQyCoaX-9-9zyQkGvwvNxyj4rGLCiiNJsMVeAxONl9PiTB6czTjSE0Fh7DgKysNRGZQ93LN7be_6ZiHxNq53GS9-oxDgZkLp_q3rjAabD18t2d63tlVuz6UNW5D2yHFrk_5uzoCjK8KOgKYtEK-H_lm81IC0Qc4alBIr0TzZ4qeyzJ0jwoxqWNYNDse3s4dQiN7JBGY044b3HXjSgAYr4HOLosX9Zw5oh6LO3bRlsBH7h9EyTV5q07qFBel-kQzCnKdYE__Rk-BrYEvHgb67fZ31dqeV7l9M7SiLj9lXEHfjX49vatl3hRuShM28tKRNMl94JgzJmVjfgQGFglrzQGotD2ClhfmMKlThqYrvK2Liw1nuw7ZdxIfHpOQiMcEmrrsQw4MUciYH-RyAb0mJPmBYn9wHGdMIiiIsqi0A8LvDSNZpu9s05_4FnNOv-NgVEwZZbBFcjfEK3gaYR9wCReYwQTCsIYhIFMjIgSUTaL9rECbj5trbVqAoyiTJ3FNPML0AyoZ4MZH6dhArwTPiqixCNuAnpK5mJSEk0wzyrz4T8gneMkiCNip46DlMLyQQYqwfdr0bGdPwClEeFBYQqEv7SjRd9bdKP_Y9uLNsp2QXJU9DwbgSMyODH609_fNygK7jhlSBErpFzBIHBE3SzygiyzcUPZGAZ4hDiuY6M-iNmcABSNKA_TjKrZDCAIMdv9R3DoqYuEjwxjg-fzYy7V6ctbV_-krhJ8wt0mVg6aPOZ1anv4sLZLQJHh99rQLsH4E6tCLeryl2pt27fObv_tje7NL6wjDz2KU17-cvvm3e71s_fegPd6rfvKJyyn6z2tGpk16kJ3Qiv-67fgu6K48NLd7atvd98Axf5DMKi6r13YvHN5uINFbArxPRfoHwHrJ3JTDBwLeQT2A04hRkztjNikcMPUzeWIBl6FAvuYDggFV1BBbPQlBrL8Fq7Dylw2CwMTL19hej-L5hv0V-H17ukXdz49w33-ZtIeT68DadWXlVe5GZFHU7iOXkADKklnQGMI0h0M70IMHcIGJ16Rh3aqLp8BgaFLr8fEteCgACIJUORRvXR28-afUQG4fap75mt2IdwFXRZWgnoK9-ckrW-wWdB4ZiqEYUZx7shNhaynFk0WlJV8VhE34pFzs7SMTeuxacm6TCBGZa3WwHBmm0299erd7ks3enONMRsH7j5zB_D6J53w8T4qHhQv_mvbV19GxyZMWdRyvjY2pc9rv5prqOuwmYw3PfP1vXeuGur1ha-6d_7affM1kSHwhvCHiFfD5NW_dN__UPko2AQBTvALENstVIOotQyL4y8Dz7721s75f6AD652PkU8wX69Sxbb--MP2ZzfRqGVczTpsdRonGs11UW20fe7y1t9fNVS04TEeccCKLCO5F6V56GfygBlIJoq7jw5PQtHf2Npor2BUGuQP_ja8YFCeedvNfCeNwizx5JIMIBPN2w6GSCJGt4PcgxfMiJe5is9pkBIx-nhoI_JFgswmjkcy2w7kVAYAiZhqbCSRRv9fuJDRI-Qsy2W3MI1YbGbHSeHAMaAkVovVQCSaiR0EUUSM7fq57Tlx6gexIoQBMtJPiAmjhez6L9DHevTxh448yqb88e2_WXv88-Ol5_hXLz1n0WfW4L1rbWlsD37V4pga6om9Bn_7tvjqpXFfbNi_lnX05794_MlHHt7jHBQ5HFjQQ13QmOVeGaAqYq_uOzqK1EoyO0ypE3kJTRUv0IApYjWTRT5B1sv4N2e3OAhPlldHnj8o8hqftfh7gx6HOTc_r7V5edXhFNQbjME8ywRTUYNDghMMz0IUY8qPcViVXs1su1IUw4giQWm1GYPL7DP0Dethh7kuBXFBjaBpTr0s8NW1NKBdBHHvB0aL0M6FVogP8MCjSlMXbmoWkuHeK85mLKyqOHd68_sz3CexS_U1aKe3roB93r32vCiCPvsaaDU7d67tXP_TvXeuVapzaR5kfpIHfhYqTdhAjtHy5-DwL1JhzIgDuiK1XapkkIEII2b4KWFdZOgUi8B5Fdc9Gf2F69D94R2LGOJ_5_rVze9friRiHgHHoHCWCs3yDYAYRcQDQr0ogZLFqVfYtp-r0Q30FzH6T4Lj0pso0p-lDk_fuYyFr7LkVcZsQVevcR86L8jlaffiGZWCAbqdTMCAH3nwnSVP8eQLkfoOh-OVwVwIGfRiaBOYqijLO-B_8FjhYtZXNqRjT5R0sGvIL_i9F1_b-fsN_o5DYSRkkfauoXhMiJSJNSDDGyx_nlviFSppEAaws0GQB1TpfwYkTs_RORiyjZgAVBE_zolbpLm-fhrsRp2eCWLWbF88i8RgBbmY5y13R5iuJeGGL89wgWt4751v4MsgPhgnlRnEGS9BSFswEYZfV0UJQvevb4GRdu_Uy_c-kZlk0rjevP3ezrVraMdev3rvo6_RaJeYIuKbJSic6KXgUVHcQpq1KHOWgFgUe87mwVq07VsfdK9_v_OP690fXpAnzKgk2fr4RTDlGJfvLzXeENeFuVOrDwCN3CjwYjdgtYXcuaGRfXoOwGjAPGKiOI_tPHddEhJ10gysHikAJwW1Iy0QGhR-4lKbGr4bjb6jbfr_JeA50iUVJXmSuS5o-VpsajwdqTjeRzgcsRCawD1OotAmqTJpDYQcw6QdE-BGSnM_zPMQ7GeSONpHozBvtL6wXwgbqZ6xStY88qNACTkD1cb0_UwIpIapjNrR84smK9fkVmhGMWW3wT0gXCEWyWTS74Y8-MoX3Quvi0wEI7K4DqpMUW-ua2_O4w3a46-Zs5rwifDvSCWKzaX9N0rT5b4dvBJXzgKvGfDwaA_Ov3FHT417JUwvD3-P7_629dGbbDvQiaz8Qd1XPka-DXopc_JKd81T0uWlFT42DC6s12l1WqhoTARKUB3B-wykhzOf73zzBRs_FAQv4f1AArfoeguEPXc3_eNvfbYA871eenfn-nXuSuXbyzNH-OVnY0ZiTNgcNBdEiZEcE7NeLrzObuJ5zJLiRcbM4bRz9_L2l69uvfEZmHZspHhBwhAgEgLqo4KiEh1BpANxosqkKSGRlaOe6fGgTfUkjzO8AVYagzUeqGup1KJvX-p-9lc2f4Lz_4p7uVAibpTS5yVmZKtmAUamyA1kymEkUmAhffL59rnLbFRMlnjggZ_D8tiYFgK0y9uDL3lYrhz2ehV3E4Zk2w7aE98H3N0S9C7QjUHBoW2SkzYRRStcIN5797Xtm1f4dOyqPtGHsCReR5wRNrdZJqMNRbF8ppN3r98G7d0sVdm6_BG8KitBROWBnwVWcC3lOq7A5StAXkdBgemUbZG4weaVqiy8Jk99Yj_KvFWmGdSLeVKWtMV_F3sAP_FgChCBvztcJ568zKdlN_6JHtwY2D9mp7HFa98VP5wMaIYj2PCUrJ3Tl-DXnR_eNM7T7pLI9-PYzdKYRKRQdq0G2RKM8yfGzJK6jWv7aUBSN9LCwoDR0sJiNBws6Xl08yzLPJDFha9NWAWNJWaZBLYVhguYJ4dXiWPO5LnT6A4Y7ozHShVQF99-EcnI4jt4RrVvYZ6so7DhZgjfAlBPKinqBiTIsyDyg0yJewNWy9AWR0HGkkHQonBCx_VTp1DeUQMsS5kME8C70pAurHEFi51wbiOMUGZniAeGOD7gsAgXkIrFH2ZwNlLfH26naoO0J-8RNh3oJU0cVe7Wrq3C2sgqsE58ld2MT7U8zn_P72ZJlnuZkorFKLOShT64A7JSLQVLsvALmsWOp7QoAzes53gcCP9LXugsjrIwLrIwiJQNoSHBpA3x00F7gaqOT37-dvfMSwx76yvBPW88D1cPORi31C5c3PzhfaZ2C7WqZLWBLADKM03hj7LQo-TZozzTtHsbCwpgtXypvDoN3-iz9-bFGZUp5pxbLjWOA78sjdYkh7mZfhx5D6if3LTuYcIstxo5U-9eiLBz9_YFLg2qPXlOkHqeS2MvVILAgDeTe3P_YcqYAc2j2pu33uzeFDHnHogAtqvCqfr1C0B-3GqWFcyxYHjaOY8fS1cwPrLUUETjwhdNPrnXXD8EVQsIpgmo7zG_9aJ-FVmxupJLDTC1tq79nZ8WM_OiihfbUUHttEhzX8kdA4et57IdHEpN3ujYs2nkhWEeartIo6v1uG_GBkjb0HW_Zn3vPP-U1V0oXw4769w1ArMZ5UAWd6kwxolOnZJNThtZa2ONcbQTdEONws9eH9W5XOaeGmZGNNqqqvzm5s2zGH1hb_fjqQ92Tp3jx4hDDKGGb7iVuNpdyTIzG4iZBbEfeOraGGhw_Sxz_6huUj9z7Czx3Nwlrqu9twroTaaa_BSAbdKEJ2kRh8C0s0R5nAwMN8NlMCoWm0VS1JyMJ_jhr_QsZAGre04iWhixaoXcJvnXT4bAprMFkbW_8gp8d-vSDwguZth43bOvoY1nwCTwE6L0RZE1dP4KqNXV3CSKaRiHILpZrjHnJhrpTevK4wK0Sb-w64Z2mEeFm0eaeynMNtnS5b5BraEBxJtvHVeJSjzDiZd6qJQypL7I2P8KBei5l7fPXBHJJ-wAqASmSvoWie9kaRimdpGYjjKB6TaY8rVfKDaVF-WGEexWmGfqVhnobIpR_68BVZNu45hmQDNgDpGnY1sKZ61HrZg8PBqw-k6DH2uWWLO-Qnmu3fbVl0W-0JnXt8-jC27n-tWdL09VngHEE6Ju7Po0U85oA2VN37EDIKZJ7culeJQ8oIsydQ0QNUOM7BsSTXp4C-r5YN3TKE20Tq9Q0uRF_Qkwz8Cquf3evfcu9EfhGQO6JNmtzkJ76YYuKQRlm1Um4mVlHFLFXqt3LLKBsn6cUV-lRBj4auLl7wNamnRLA0OOSQ7aVqhOvwGg1rOt-wZDkxubhn6RR2kOt0mF_jQ-mrxZPxHWmRRDTgaHKwNBFOoUOQ1_ZsRrJgRl1q-Xo-1w9wy8nw6SyOirCClc_17Y7-xDf0FE65UUZ0KF_Q1EJeJHXL3YBYL0OP0r4nGEeiAmCHAFxSMMTDXlTfqp8NEMJ2DlSQUWESYpDYrQSbQfUAGo9ZzUvTHRJFdLMhCXXkqIp66fAZMmc9n2i3wmNT3PjtM4DoJYZ98ZYGhKVN4ffLOdv_-D18ayfBmO2tIXMRI5SOhNEHF2jlnFzHjpWRI718hWeFYCQ_hiF1KOygStijwYa0UvCA-L9VhTMpuFZZd_3J94K5zhjHlWnmCHJmHqeXnsaR-hgdxmJLWNDsYmD11eFDaJXdsxLovGZ-s5dHtDrskbCJZJlKRJGAW64kOjsPVopvcbWE0uqfDDKMkDN9PhXgNrTZ_Ynww-zTyKnLmAUcN3bPiJw4IYFWTa_fCEvu-EaZD6ka_MYQOPrWdH9w-tpqSpHxGs53EdR7sPFdqaGPx-AKepSpI8D_wChHqoF6Cx1NQ-TgoWDR0mcnuGMHTJKHrwpdiBvgMm7k0eWh5wcIundl79nPvHure-Be6FTgINWMC87OdEPIkFSVHxOnN659p3yt3ZffGULHcUqftbX7-wdfuCyMiRkZ7lFllbkXyKq9xsRXJahjFx8xLu15VXZTS8z4JW5fnyKJu5spu3v9r59Ay6Wtll2Ln7IYzL00wrj2pEY5DJiZMkjrqUBtic1J8miBsHh-EkAVkissaQfb_3wANrewQ5q_M3Ct_3QicOg0BxUAODTpskBwOTk6PbKUldNysiV2cUa3w5s-BhRKC4dWt9pSn_Bl-ds-gzsL9wccBUa8xZzRaGQyodP3aapGA40dhzbe24ViBzPY6fSaPFSedAkDpO4adxUCiRaQDI9Wkk9wEJjuY9vIBHC5VNt3Plue71j7DqRwbnmShjAf9qVSClBNgt8T2qvMcGspxKej4gRJzUDiMfiB9EGdXS30CNM10e_-_Cv0nJEOeg-LtBBPJPpUlqRLgeN8cBoN2k4HMTL_QTJ010cYyB9tZfEzISbJthaBngZYsyd2Spwfu3w6ekbXzaTEvgWuJTmf6AM5iPVhZROEmQhSBBQWNQjlsDKE683MEQ3yRrCCMn8TKaeK4yvw0QuH66TQzNTRoqCdz_oAgoJYkuyFAAb7J8agykNumMjf248DwahVSxQAO8rf89R0Fho_XimMxmgd_3t7VBFBNCizhzArW1BmabdlH89OBrqqTPKcA2dwNaaDe2xmPT8nNcGDUVYU9pkYdFltpKohrIaoZ-vB-wNCmmPTsHPZhiQb9ipBo_zbxB9wUSrfv-D9xrgcmRVz9Fc_i9F3aufHrvxVe4AgRPcRGHWFPMqKnclAy0GQ_MQkK0r93AVush0n7A0qS88SK7sGmY2LkyDA38tJ4u9NMBRJOFKBVlktSNwqiIfSdXmoaBldZDmj3xz3SVZ-rSjIa2jvwbkGiSTd0XmDNRFff9t9ynsv3-dyAReZKlODpGfuAeMjJM8ygiKZe43B2qkdKUNvFToZ9xvoSXQkbbyhW4Ym90z5wRBpCM9HVvfNY9w2I2V97sXnwNFZGPrvJjCD8feeIohrwxYrF55_z2WRG2FLMgfoTEvrFYiLw5X64AfZl9wvgmpqfuw-1D04D6GSUY4lCcUMO09ajR04NeYwatNvO2Xnmre-evewTu4Fj4DihjvuLwBkqb5vD7g11TmkXsB1EY-rHOqzCQ2FSt5WSh1ThTRnbT45Dm9ZA87d-oe2mAns_qNAXUAPuWICyvwmBXtK-AiZdQ4Ip59QGrOBhSbsCHE0VjwPfPf47W8NGHHxF6NhuB-fhZ-hmcV6bhHMZsuMMsg-byV2AkdF96d_PuB1vnTkuVwhwXA8fae3Xpe6Qgd2A9a3H4EsFl6GrKjzxMoy44t7H5ePwpuMfcO6SZFiOQSBHut8SxZrLfe8Iqj2AAVVPKiCojq8LEYJJDZGX11AvAdMwClXYY8klWBWQo66x0rRw6sDEMS2w8LNIee5IQu5_9deebz_XImHlIsbC9d0T0NfLAL8vr52vGgcUUm9_9CUZCtseystGfNKyyd0h-Opi071zh4oLzKqwKBpvnI9NxJcLjp2GJP-j44HdXsUgT8-1xpJ4jxpiHlSmHKw6qfbMiFZm5RnvcoexjBjiBrlDhIecrl2n9_LRwZxjP47fkPeEOK-4ZVI7u9znz59FATPStA89kro-qAmJQx5zcJWno6QC_AYdoIDXsF9xQKv-pTbKIgrmUFNopqfAOteCbNHohl3KnNm_d2f7i1vbNu2Los2dEQct8B8yFw_hDUaP1HMtDpJfChPwRzE1DNMgvGWBB3Yuv3Lt0SgdG-MZxPUH4G0DjNESddHKKoMdnW29fHSzz6174tPvZNyobix9ZkLNw3MXzoubn5TdRR9ijpFHkZV79AWR4941z27de2L71Igd627zz5vbXt-T3rn8vqsBbFHPTEF9JOgixMuPKC5t3Lm_f-gh9N0yuV3sxbScK8jgvnFjh6RjYkcaxOjAApBSgjh14oG-mQRob6qHEhOzPQDsYsKNUa8EeSlwQpjCuSlPUWI86bDwhwEaDJcuocq_cRKf7zSvAdGQ4-Nwu2dgW_xpu1gefCGGpI8jegsFPhaI5mGupMytl3iwolu0VDg7AsyFlrLqlgX24Ri2xfUxGyADFUPaA-BToPVsXLuzcvcE4qFHXJaPce4ktrtEzKQNn9JXP-4XY-6wmq09GDTwkBRH7frTQU-TM1JQ__VncV47hc-td4RnoBT5gj8cLBs6JOAJcF5AJI2hadf9-rj9cAlpeayDqxHRoFrywhiWzYlGCsARwFb3xGTYq8mxDNGnoCmNXeF6SisoZITi8mqogipdIsegCaCu7yF4u1zZvfwXiDq3LHphJPiYe6eEAbkJMiqUgG5SIS4Y4rGY6Do0o8Yjj00RXeCigU4PpHACzVGGrBUFsU9-JdPjZgDE1Yg6jIpJazcJCDUvF64XbEx7OlfMNPpZlrrIWsTIK4Tsx8W3bCdxMmRkGvmmPq7wKqlSFOim10dNOM8UQDfRS7RufDhApcBR1YHkVKGYTXj_bI6E3b_6Zy1ZRscGOmaE3fPdVj97Av3T9e17NwSujUE-99uHW23fEh6x6qvJoel7qpTGlJHaVI97ARpXOjP3DnErzmIKxF8WeyFvkPimNfNrvYh0JxFQDvc3JElxVJlvCtx6l7cGcOpAbmI23XgOBgTNg-TB8l2XoIE4aO9WaE5SychO-wxHV1pgaAicfNT91-Fl-Hl6rVNbC0nxhqLv36T8gmQTa6u8PiQ6T8JNywR5a_C377jOHEBJVu9V7Pjfc6n2fa6c8_uHJGlzXVn7o6T_M3TcYUcMDf4x54JFV9TnF8WssIoKvKlFtl3lXgwZZlfR5BlFUhXOSIcTCsgW_YTClunmPQgnVKLr7BSXVuLoyLFiB12tAX-qZHnmGZh1WrS3PYNWYw6CmDfzLUYcd7HSggSEnNqaBCDnqmAPgy1Hi2Xl_G-2qMQfhjy3LKuEOg-qJO0wJ_MDssoWqBqdh4sdRX6_Wg027K0jlohSWgwCVnKE0qrrI2qmdefkBNm4oQfrYIQeawHSLdh_iRBXkt-27YeFkY6ykElFzEcixIeEYWK3LignWUEEj1_HsYuxD08L8BdRmhKb5oJTPffCShtZfRa4wKkjoJHSMRe2KBrqIAgb4FlKJy75avdYGDa0o4EslUq6CXA51kySww_HIJTLZUL9_EDNTRCYKl3AWbKH4RhWNktT1UprlY6xkOKDpIlz55rrVaQgw0BzTXzoNKY14Kt5KBY2CxE0D4pPxaCQdsS0i1BY4P8sdyrEctBJZeYw0BKmBCb9g_RIvR215BU9low2WGzBXWj-wqNEQpGOOPrBwA8Vz0kMbwJCTHtpAeRxz6MGWLQbI4aSXbcD46aH3AArc_-gGgp45umMdbWT1Djraaw3GrYVTON2AC1KQTr190PNooOlNcKZBLUPjupnTuNYjz4hpVMHk2K9kQLxNdK7BvhUaq8ycqA-qbF772zLE-mnVyEHfyMAqm9xEg8q1xiab3CxDurt6eZCn6RizDOX8ZLlFWSSjUqPSOGX3kZAGKJiexWNJOFTn0ZYHPQUGJtioww7uRhzFeDH3PeZQ2ht1zsZdqlT_izAgSZ8CebB5q6DLULMFBQRICJyX-wMkehnTLSsoQsB-sVOXjEeRIZholWpZkic2KZwxJj0I2ppS_FkCs9n2doAcKfFB1CXBeOTAuviy7KxiGjxqgu0mV_7NAvmqLqOOGxdJGo6xiD1R4hatlKKSCMNxJxPL4oZlNqruD3HsjJJozPtjIESA1gxH98hDj1bRI6Oe6_f3ST_YrLvj3C1a_TB3cxKIWBSUVWnxFBtkkHQ8ekgAPYbW1uy00es9VFxXHpog8CLfS8ZYym5gfYsWbbWw9A10o_7KOVav_cxaq-rQ-EXmxaQY89Cw-aooEFMnSvrbKx5snt2gBRf7XK5rdVLje8aCSMw0reqhGbgx7e_OfGAKoN84h8Na6UQJ7TgMnHAc1rp_VMRF7jVH4VPnXqcqJ0pGksyP_DHvCmefc3wxjIPtiVey3EEqVSgwBWyQH41Dsyokx0VYCVsHDIWLw8AXet7nLEywmquSzlFQxEkeJuPSjHlOUriprJa1Vq7QvOoQOXnsFSS2x5h2VxDKRWsoBiUt5ywJQllBkDx3UsceV13REbFVxIrMSKdkp1g1v0DA_-UWySvFtO2ATZz3GXkHpNK-sDMXVRzc9MdVWWpxEnlOEo9JJdJpN1ex4QHwwA0kDszMFwmaTQ1XLIQASHERdS_xLladLCfIbdsdR7WpQvvUlTJzlsT6nFO1LpVXLYCddL10XJqJWz_HXO8KPpQdM9DWQWowOQL72IFbyEKKVRINjMcsysZRtw4EUopibhX0jBrItw1aJdOTPIo9n9pjUoutQEDxWaSOSrJaEQqfDeYvrzVgSyXnL9EZXGVqaUTUUc3GIZEJhWSqxzSQTBlzEx5yHnFp8-jigQxeA8l0QrMM-kw1gKg5Ra_7iwwxbg_6LgaI6OQmGlQpNOClOYtrPaYP8SDo5eD4jc5qisrL4m9_C4-j_xQGOfT009VeKo2GOdbkuzZr1YiO92V8A8DQHN_r8xvue5N6iegyInp7EdEAOJzIInY7KQbOnzmPbz1ZK0-UaHApfbLqXg07KP5e72hgAI4z964MTyPn3Y_hDWQ6PTyY049Ld5PwNPHALxEpyqy9h7V6ULZhwNJNdrJB0aoB4e7zTAY03GRnGjS0NVjbfX4nA5VMzzQc7mz_gxpoX5Mb1IDZMgcdjuC1_2ENoKwxhh30T2v4qUmu1gByMoftA4fa_3gGhNMo4w3K8RhufUL2N94wTVJKh1qpcBeaPI7XQCdNHzBUpcpNUhJ4cTTiUuatR3GuATcZRauJq7vMs2dA-yywvka4qRUUMlCdJrKDBsqSOV4fctMB2KmGSBplvMEUEo0VZI63Cw7RAZixhgAaZ9xB1ovoa1kQHGjcYSdZ-QCEz6jPBmfHaJ9hBNsFCvq-P-aa5ln-QI9nbZVgr1wwtSlIkQZdt0pSUKPyjh1pxrIqSJa5RZT4djQ2ybQFy_KEmK2NpIOTd4LRqsdlYYIdVWYOIY_Lxyfe0UJQx4QlAj5VW11rlswnNsf7DgtSakClKoey7yVO7nlj004nOTfKNoaoQF0UWcYyQ05mL8OaVUofaVSKBw3NNNHLa6Al6XGjBeCBrDqFF2OalQEj5MYacEQTmWPwJTTY0EQmGJJxoFB_7s8bGMA_9-cNDDSe-_MGBmbN_ZnAgI65PxMY0Cz3ZwIDWUVP0IOsMmeZwCqmw7N20EtnIKCYk_WhqhxA39VQIeZ4AwAkB0gW0iAb5oi9uB0HsEo02sUIww1qHxHxIuLsa7hhUqDeXAfG3G6xWCb3EcDmZisWKS0skCjnMN21xXIIsnpHJHo3W9aRqk2Is8DOiTfaohhehtlxYBW9_QOwGQg0BQp_mwonR49yPyg2NUjGJHbRQJHQww3BpjhACqdRZm6kcNoL1iMyNAWDN5qN-eUmqR84pcqoNR9z9MGQky4zNoauLmQ-QIqZLjAef_RBTZQ6xPcKf4TRdw3UYxoHgaOLadkDpc3VlSJeFqRJNJHFuAvWkb5y6axFQf3Fa8Vt0wfRuTqsYLoqLJ1TEmY0nhTBkK3g9WYLqkxojCiJUtubyMQez4yWvgPRGY5Rprfue85oqDPXj6U9yGTcwAX1yJkUcVicGlE591kXEsduQYo-U3zU-QOQ-FgCJ40BZv7J891Zg7XJv6iAPjkBp-v4ycrwoU0KO_JpMCkaySyCSrokiW33B1NHnTPso8vg29eKjeOIOIJik5fTw3cXWDV9FWHChPpRP_8fnTC9BfBV5HFplnlJSicyM8qUI2aZPRZ41zjXkaRCfVFXPiGX5r6xKj9h4BCwCybGqK0CxBytb_AuA701MyJcX0mzzKZuHAb5ZGjmmto112wkEoCiE1so5pMKgrFvZZW1a7FL4zzyJkazfVRdaXwBY0p4vcdqjdpqZxWWzKcWat2Bizh0sf7Y4w-KGF26P_bgg1qSLm-f0MqfhpFYi4zdSpSHBDFBXYZPfonyrU6QO-C1W-ukoAIq_GtcXos7huC0PdJYxqwxxfkzyfvQzOTtQFnxIrK43SqYp7sQo-Z5ugsxCqWnuxCjunrKFNEl2X2M5yc9ILpCe4qrMKqxp7gKoxJ7iqswqq6nuAqjzHqKqzBKqqe4CqOcepo3VZdOT_Nc6LrpKUs2XWI93YUYBdnTXYhRvj3dhRjF3lM-I7oyfLoLMerIp7sQo-R8ugsxKtKnrIbpmvUpnxFd0D5l40UXvE93IUZB_JQpomvmp8xZdVn9NPVkXV8_bVtOleBPeSG6aH_KB0RX-k9TVdV1_9M8prrGf5rGgy76n-IqjAL_Ka7CqPCf5rnQ1fxTXIVR3T_Nm6or-ad5LnQR_zTPhS7Yn-IqjHL-qe6IKt2fprNBV_VP0yGnK_inuAqjWn-KqzAq86fpFtSF-lNchVGUP03XuS7Hn-IqjNL7aZ4LXWY_TZmqS-qnKUd0Ef00tV9dMD_NHdHF8VN2v-mK-ikvRBfdT9l7rkvzp7sQo3R_ym58Xd0_ZfebrvSf7kIMSIDpLsTADpiyv0njB0zZja8BBqYdT1BoA9OOSypcgikfVo1gMO1bo9ANprsQA_xgypxVYyNMOxyooBOmLfQUssKU1QCNxjDluKRGcJjuQgzMhynHNjRKxJQPq8aVmLLQ04AUU6aIRrKYpsmrQSymuQqNWTFltVmDXUxZ7mqUjGlbNApeY8oL0XgcU1YANIDHNH2YGrJjmhE5jcwx1WRThcAxzfiPRtqY4ioMRI0pXxMNwTFtV4jC6ZgyRTSex7RTohTux5T1ZI0PMuVEQo0jMmW5r_FGpp2QrHBJpiz3NX7JlH0yGudkyrdGY6BM2YTR4ClTTjbVmCtT9kBotJZpS1-F8zLNNBAN7DJNxUxjuUx5UzQKzLS9MQo7ZtpGnYKZmToHkaA0Uw5TafyaKUsZDXUz1VpbhXEzzRQujWIzzWRLDWkzTW6qQWum6THU0DXTdMJocJpp0kLD1UyTFhqPZpoah8ammeYqNPrMNJ1zGnNmqjqgQpWZpotQA81MOf6kEWmm7cZW6DVTVr000s0UFvK0ga_z-0PrKxuIl9Nhnc_YVM2iqGWIdScnY2BUCkdaz41way1EiKo15BLgNQ8xoDoYE1ve1ZqNYxxUD1-N_eVYDV94bY0eC-MwI45LUicIEzcOCjfI8jzSRGh06vU5xPLhA_qe7cSEmZr8M47rw96W7orxo7GEnhDv8y-8-SlCbhXNlqX6Px0ReM8HAz_VID7761W_z97wGpJn1GEHgVU1us7ExjSAckYdcxBBUWPe7G_MoVhcJdyGbIXtMCXwA2voUQ0uqUBuRp2WdV97krXsskrZULW-wbvUsU85oBjlDSFZozHRrqqqO6QBfDMGQeTXSt7ihCHzScxys8VrJcakBr8ZdSWs59qTZF22Is5IAwHW14BYRjdi_KPED9RdjKug3DQgzhg0Yp2IkWsKIL4HrRXeJ1iD8XHYvv3BTRr4OKMuijUrfqrdXEPYM0YldaSAJ_e1PWTtz4oCvlQi5ap6SGjMnDHIxeHuWOsO1l5ANNPknWFZ39N9AOJp3JxRV8IaGP8CpEsLt4tay7B5SKBypbludRqwl20QXDkCAnYaEvSbsfxsparrocbSGYNGoukhnGKGd9sGaWUtdyjv5qkhFSuPkYbTMZDxOEJrq7a8gqey0QaJDcyV1g8sajRGzpijD7bU06g3kx7awLGZ9NAGMs2YQw9iWBtgM5NetgEfo4cGifQo75St2nqr5u8Hg37UmDDm6L1NC4c25j4wgqUGfZngTINahoZ0Madx-7rrTeSVDNSWic41iKGpUVnMiTxsOKNRrOcFijWchQy7mLdq5MBo6Rp1ZXITDSrXGlJlcrMMaQqi8FJGnWUo5yfLLUpX90Lt1jAp95GQBgbKqI1fh3ao1Igmow47uBsanGSM7rkm7rS-S5Xqv4YjGXVepv7_oomY9vO8f2BGsQNDY4NrtqCAiGaDRQ3WJToOct2yqoOFhigZgyIG0P56s3WiqDfXK9UyjUgy6qRM03-8YSrwWXvOkuo9cjkhiQzFf30FUbAbFeQwUErGIEcNLK-y7KwC72WaYLvJlf999g8zQEpGXQTT7P-Nmxc1gWBt2BWsGzxlXpyGaBAPxIHvtmijst-JBi4Zgzy0wdqJCLBtOLpHHnq0Eu1bA5WMOivT4p-SVrPWV5j1DCfItFHnrDJrIai9aF9YpcVr8JIx6CEeZd3nLfSxNYvh4rry0GgEk1GXEgoWUwIDaaCltY7iAElEW61mq2Sto_v6KyIjos-sVfUcMFBNxjk0bL7KPgMat2TUeSJBAeCcYPtSYWzy_uzYPp4Zd_Dya3VS43smQPbBNK3qTKGxTMagAHpgczislU4UA7Bk1KliJMLD2NUHO8Fj3wnBQXLxmWhMh2RpIno9Cp869zpVOVE0iMk4d4WzzzndW7nW1gpuT7NE5VZZ7iCVKhQYDWwy6soSpNmvhDWO97iUtjlzpvCWkjAULg7IBbKq2Zqz2rVVeJMqO0KDnYxFM-Y5SeGmlmg11soVmlcdIgPdZNRpsRHFAw_8HHaLszUhZZjggc05rPp2iAYi2OqK8WTY0QqCGIgnYxAE7OA2Ye1dWM_KjHRKdoqp7MaUw8Ytt0he3eZT456MTCUHqfSE6IypWpDyAyQaZnIHL-_faPrjqiw1jYUyDpX6WqA-w1qq9PT0FEIApPga2ag3SV7iXaw6WRofZWSauZxmlHUuardwB-skpXXmlkOvM7LoOYu1gqnhT6SN_TXwpypRrjFTxqGZuPVmVz7gmOyY8b4mTI7APnbgFqJyWCnRNILKyNRiirIKQ63S1jKFRbLoAOuKrINvXMytgp5RA_m2UdlHyEBVGYdabAU8egGqRB2VZLUiFD4bzF9ea6xh4JFzjBKdwVWmlkZaGdVsHBKZUKApekxQsR8STIwxN-Eh5xEX7OR3UIPXQESZ0CyDPlONdWJO0ev-IkOM24O-i4FlMrmJBlUKDVRizuJaj-lDrPv6srM_PCzeWU1ReVn87W_hcfSfwiCHnn662kulwUnGmnzXTuEac-S-jG9AiZjje31-w31vUi8RXUZEby8iGjAiE1nEbifFQAkx5_GtJ2vliRINLqVPVt2rYQfF3-sdDWCQcebeleFpuI_7MbwB4qGHB3P6celuEp4mHvglPBSOGgyoB6sHZRsGUMdkJxvSrE8hcdznmQyojcnONGhoayyN-_xOBliG2WjcsR4Zo8u4AXwxuUENEAtzUBdd4NgWfsRhDUiKMYYd9E9rgIlJrtaAizCH9azHyAmq-mrufzwD9WGU8Ya0ylPgDXuPN0yTlNKhVrKuxCcxHs_jeA100nA_HqnXfrdnEoqB4DDKUuatR3GuATcZRauJq7vMs4fjCP_ewlJj3noKN7WCQgakw0R20EBmMMfzrYdU68iDsVMNsDDKeIMpJBonwRwvsJ4UlvCIN8GAPRhn3EHWq1EM9j_usJOsfADCZ9Rng7NjtM8wgoFpMM6a5nmzXtOztko2rBSstlUKUqRB162SFJjvQrMTa014A3akGcuqav6swQ7GI5m2YFmeELO1kXRw8k4wWvW4LIRXxVpukbXKzCEFgjAe8Y4WgjqcgzMGhHyqtrrWLJlPbA5ouczMISSl0ugrWx1rcITxaCcjZ5gl18YQFaiL8HfQElWGnPD24ppVSh9pVIoHDZow0ctrYCDocaMF4IEN7LMNG9zmKY8yDWuE3FgD3mAicwy-hIYtmMgEQzIOFBzB_XkDA2bg_ryBAR9wf97AgAW4PxMY5f73ZwKjjP_-TGCU5-sJYrNR8pxVdtbAGKYskGo6PGsHvXRGCb45mWPMdjB9V1fSm-O51lPGig-WLKRL4s0RPWBpolX0wawSXdg-wnCD2ocuT99zuGFSoN5cB8bcbrFYJvcRwOZmKxYprQZZxdhMuYLOf_hjVu-IRO9myzpStQm6Wn2ERc1bv3Z0BE90ZbZY3kBzvlyBg8YEFGvDvdpsU-Hk6FHuB8WmLl2fxC4aBeh6uGQBV46aPehocNQOlsJplJIbKZz2gvWIDE3B4I1mY365SeoHTqky6sPHHH0w5KQrvg_a7Xw_KWa6jHv80Qc1UV2bPZFO7bJUisDRxbRsIzsKD_JadaqYLtEefzHugnUEjyHKhLQFz6xYvGIKrxW3TR9E56qZDmiJdMCqsLQu4J4IwZCt4PVmC6pMaNQ12-NP7PHMaOk7wAEJqMFIGUwJamORXNaqrbXnrHazWccPMlDWpbG9K5PRFd0TIQ6LU5Ny33UhRi33-PMHIPFlwR8aA8z8k-e7swZrk39RAX1yAk7X8ZOV4UOj0nsiNJJZBJV00XXd488Z9tFl8O1rxcZxuEosZt4mq8ADsEJyqQFKWhVhdNn3RAjTFG6orNnZI3vKKPUef2aUKcB4lO8H6NNiNZGNpiIVq_xUlU_IpblvrMpPqAvBJ0IdqwAxh0WmWZ3UVntrZkS4vpJmRkn4BGjmmto112yEVqLpxBaK-aSCYOxbWWXtmi4YnwzN9lF1pavDjSnh9R6rNWqrnVVYMp9aqHUHLuLQRd9jjz8oYnQh99iDD2pJujh7Qit_eqDy2UnzgsR-4LhOGERRASwv9EOm3WCop8TCbL6zi0E0pwdejKI_zMnCarMiGufghd44g3bcyB-PYaokWaZyCfVjnls4NItz4hMSeHYRRsR3igJFUtks2scK2FHaWgOO2GZPlKmz6CVFQRPbT_zUSePUD9IIWFIcJIHjBIlL_CIAg6IIHNsBJhBFEQ18-GseJimJc1b-so_Xw78fAlsunLejeTf8peMs-t6iH_4f2160kevq908K3yGgMR8yqQJjy0LuxUN5MysPP_Hk0V8feejfjx35xcPHHj761EOPPv7Ur558ZGEVd0p-V1LmWIgU9Ys8djNYeG7HvhO5ToSKFDsivNB8hZQrKHsj6maRF2SZjZvHxkixJDpkvhdxev7J2m_peTn8VonZgKjAbgrbTWghZzMq3cVsP8NIRbtTLqKlAIc072TteZlpr6oWrbxFivZS42fwr_UwqJuLlqK5Kz5-CvgIfK4ckPyEzcmkZ5WhPacEhs5_AXO03VxbgzfAkYwC1TkQwMwBkoP8Bb0tU_z0sGKm3FOxiheOeUqkobYgFvY4T8Au-frgqNL55RZIApCiRx56FO3eBssNPkE3rJK2TtYylrvIkzLoPOnkNQrMlK2MAStwl2_ZBsV7tcQXXGY1N2hlM5NAvDj3n8CfMCsUVl6vk7TZ2jVgJbYtjvy0yHzfdVnqN9s2AzZAHpJ_sobWlu5-HArQRILUdVLiBXJcAzdAoR40mwWIh7LUIirt1Oq8zlliPLByQ9hpPCZgbfx46jKLPP946gOLb8mC9SugZLnUyGSYsxQOaKxlwXJjeHZ5xXqqTrITcxYK5vqc9TAMT5kbgptZqKSXC5Ze01JDLaoF5k2theGK3j2ha1ZKC0wNwwpfI0KOu8ESQfkASw3hFUfZixl-WC7BZiWy3qaEkWiDi0dWDgzDrpNWPjzVVpDZDkFTt4FFEqK2z4BSEGRGq5zSXGTsFbiJLUyFW6wY2KVBVKShH4TqOht4Cro4FFO9QatoaZ88S-rGZECz8htLWoBetezExuCdZYGqIWJPrIWmRZomnucULMeav6TGYRBrOQisghgYGGgMZz-hKVEc0kBa0GWqIwMnKKt497fLYNv9JEdRFMtFGKAK-u3GwUgQc6WFk8JawyTKUjmXAZugsx1HRkHI2iK6JyuXdn9xx8GYZ4b1dK5cjIGUoF98QsAH8mQTSoLYjtI4CuW0BhaCzpscGdpABTvxFBQdrO_fnQqhnfiRk-QxKXK5HAMAQVNhHDwDeZGo76Y-se2kUBQ3IA50xs_IiAUM7Qa9DUyAwld2f_HIg5tXBH6We-rcG6gG-sXHACmQwijLSO5FaR76mZwqw_uW-YWpmzzwwBHQgBv5POOTLKoKL9PWysSCdbTdf-o4OTj_b68woQPyAH5beOCB3ZfkJQEFTYm6lBUj8FOooRS03K2qv99d_GKVXeaHFISDFr8aS0EMjwPjweECdh22DWSglbEsAZ4CY0i7CmERBplNHI9ktp4t9x3g17HBVo4fP44_LTV49sp_NDutBvz_j2ffEJlkwk5knxiYTrDFsr647y9cJ9IjsCuwsdSAmfRiM3i5HqafBFEC6n_oZFQtVmNBaJHZKfEoN_rFVQUdXD-3PQeNj1jRIQqpY9uRN4QO1sA_qyobZ6nxxONP_vLIvzz6iGX9eOnUWP8CeaxHH3_oyKNsyh_f_pu1xz8_XnqOf_XSc7qmRUTeB79q1ZYbcOLVE3sN_vZt8dVL477YsH8t6-jPf_H4k488vMcxoG5EcuIAn2VRUC59NG6HviGlSHHEs1CuAwMC_ROUNzh-jBHI9IY6yIf_CyopF87sO02m1aFyUCLDWMc_V5weh8YhmGaxm_jq9BhwH2JFz4JhxkDTnpXgGSldISdrwI2ftf4VVUn9-1Lj2fn5efVf-NU6zjcrPw7ffpinCEkOxiWVYuLP6rxPdQP4EOyA4gD_Jt5duLowJ__ntfZh9vfDKejaqPDy_NBnLVQomKpr-PKUyihtND6B_BjnODI0Ew6lbEnAzhG-g2HjE5E4I4ceFjeTh6GIXY_aSeYST8sihYYiSH-0Ae9SZ5LfMFxUvlBvqhW7ytwoeIy0TmBFGEpMpEYts_7tl4_BbTQ4C3_hBetIwdL_kPm0WHXzMioS8hLWmY2M2jZXNAR-Hircc0sNuKQYnoZNKR-06r15hEozrTXg7MI34V8VZypP4DuRZdjEKuUxDzJUVP0sVJoKoX6a5XneI7L2wHXZXWrlaewXcZL6GfOfcVVYI8cYUgtRAnDNKp1MRF_6Sq9BvDRbTBldEclJRl00fgRG-y9g6wzhjTXLYKihnSZMM9w1tMxYipUI_vdtNihhFO4_WIzEUCBKuBagjWZVKlkUuqmbJmEBuokiqoazUURFqu4PZWZ38kagbSfEdUABVnMZgDZirnnriCHzxLlhs7EzqWydJlPF2soG4fAEbThMIn2PF9IpKijGoqptOVAiUppn2q7L2dgARzpwOlvzZSeVMQj2PHdhcwsLHqu1RKGeMMnhZmChOw7wJBpfvG6Pe5rwJ8xsYTV9zFuC1huCLGA5LZhVa_VOaWa8WCmB28RXI4OMc4o28_A_eGJABynlmoeHQmEkwVzZdS5Rle6A3sX1d_RLyZRH6W4qe7NjSr7gHMjM6wENL9XC7iq2C6eKOE6SpqnWRzS0UM_h2i_ez-7Hi_px7Lg-CUDPVrdXgwup44WMmsexpZ0sjFh5t3TklNP-oRW82ezyohunPaeSMDnpYR2cPizMijeSP_cI474lOcnucE8WZ7sJsomLJj6FinFjImOzxYI5OCRwLWAO9eYanniGOcHH_jVtpXDiVqVPaZWyEhnmTjrZrGEwpO8tngJ9N6Oq0BU2mGYt2oYf4P-E2Sr2mSvIJC2b9Q6mnILhU6qcWExIV7fREAyrIGUQWkCQBtbBhmGsqOKM5E4YeH7sZwVRNqGB1NRzRvYF_LP7AYnD2E2j1AeGp_w4BlaTmOqIcWvEPUmpvquMszKsEWb2Mo5eMgcI3Gwm4dAxUaFmwYWwi4DCK7rKs2VgOfXCnuU1GU8TLB75WavW7LB4egnmsfCwLjVcZhyiEUVS9AKiwxc9UUScUsEtwaBIhUaJ0sfDQGfZYToiC8YxbiBwCdbZ28OQbS7xuMmdYzpIgxec63r83XfYy-wkxtgHCbWpqWGltKFdiQklvSd-noNCaruuVlINmCgxmPCWEZWZwbcUKMLJRTBrmRcR6WsixTMaeB1uble4MhLgKkkU2iRVJj3WZPmBTXtNerEWNrLwoJkONMNvVmWvE8_2QjeIqc-uhfCHKuAqrfwMLRXe_U64IJFBIMO7EPUeBnKV6Wd9intPpa6ILpndlDygJNHKtRLmLOGiwhdlR45NQT8ISKDUYAPySp-U_SNYSS5DIs92s6jg1bZcwdagVqandUSMKrajrdoyUztRmdj9NeF-xqnr2UGoaW7gWOnX3CcslRg2cYCv-QUpClvdMwOpynSujgg8pVGgWsLY2f0li9SPXSyLKrSbw0Cn0i85ItiU3NgiivI8gnunjQIDf8r0po4IJ8VcUfyh3d82tb0gj3M_DRKtRmuwKf22-8WOkuOGEU2zsHCKUN0IA07K9JiOiA5F6lzmC7ld4SiO0zTJQjAMMu3S0_hRpqN4DDgoeZbhxQPHpZ5vq_c2EKJUTcbogE8g75jJwCNzjJFVxEiITb3CBeZElOZgwEIZ27srypPy_qWZncck82xlYhrATzoTfmQcpzZXVzCpuL5RwYQy3_aD1IuKotAUVjhP-pUqYZukiIdDEcXEozzYzhm3RnLS6fcjAzPhhWGul7IqUucktlfkbuG7jpKSBm6TcUZHhWGCJVAWC2J1mugnxTQsfFAsvkp3KYoc9IMEQwxK1mrsJp2APTIUE9PglLJXoZJ5nhtGWRg6eiUGVpNJp31CLyk564PukAZhUCgmYaAxGSnbo4Ir8RvGeRZehLW1Kt0z8nM3idOAEqICjgYGk37R8SCVlMwjYeBHxPcjFQ03UJaM5LVRQZMw0icdfru_NdjAXuGnoI56RCdVKEwl461HhUhCSAtt3vFQgnyTquORgiKWuYHvZYqtG5BKRkLZqAhJJa0X86BP0Bb-WmF2Zh6I6swNc09xCgNCySDRRBCRpAVq0yANQe0sfLUxBkiSfP8xMI_Et9ElCU9UyfMAr6qTwHqIVhc1LJJBgVFRjrRrmil0ZjB2IPZQJLYf5UXmxlo_10hIxmKYoCPKzaCuDz-UjQ306sF5rq0Bq_7nUrgyWrSoUjaKMIp9382y1NVZCQoySdtW-wEzqvBPOYlTxJEdJIWh9ivMJOV-MMAAmNrEIwzwLuxsC0czCn95QFoU1RkMzbaVcUmWGob1UG7A7VgFU3-P1Aml4wvvvMW9PZiYtNRgvgQdeJgn60R6FKs0WA_20aEuMB8d7tQwToZ_Z5_wShU5X8QGuQYThYli9gaQk_Yvy9c9-vCcygFaazXbzaxZl9oGv-9SExC--nnroR7VoLYMbId9kbHJeeFRztBhyJ1uvYXljI-CytEmPMdxwHLmD_V5rPnE2u08xOEsnMTCj4zKQIlJ-0JO7uJSlpNzlWFI0pD2hJV9_uH-4sm-7ESefcHDlhW-v8hJCUUXRpyos2FgYvWcjT1woyo8HLHnxL6TJRx-gsscjX0lMwHh2NbrtK7SXAod4-vJLJJ8D34oCsq3Wx5TVqHE9uvhTot5cPn65sx4nZBapUygWsVoDmi7JdPjGNMue1juUmOQ54r4izTDS9MRCzsDP3PGzI1oeLEW25ilhiyfEkJDnlh2fJFN4huxqAJLYBOdtdjpZ_5IkRtwHL5ZHl5TL3WY23bHeZrdarNlpIbxt5iz4PwhWxEqP6Z0rfIlLzW46GARr96NreArrpNTL3bhf7Thb0CO6Vhdi-VHzsm90Pr8oO6Du4qZv_gShhgBuuc8iZIHg-YM1UfEbrTmjY51AptY-53hDJdSqtTpnksNLK4payyAzfYQPbHsmDFHLag7zcZyKXear13k-zG5mlJj0-GMyNvcs-vKwMWPgA6YMsyG-udSRZ14QGtOrB9XiGtTgaMaredVFi0Bu9ijoR8nhQq7GNhsPZd4n7hou1_mJPN80FHivNAxHgODrSfGYwRA5vRxFJEfthG6LI7ztyeGxS7E3Tj6MGeQoiJpnn8q6pLw4UeZpsFiJXNgqp6stZqNVVaJLOMsLOjDZzbcQCfoRk-ARhYwy-i4skB0FpgOLvWo6kwmYbgpxz3GuiCUMT-euixfvgFXdeHHUx9UGdARJYnvhEGg7DcDe65nM6sR2nbfQz8FkUw8P8t03qWBMScZsmQEMsHFjLKzbEMtVeeETJ0T4pU7GFhBAtBK8YCKoAwoJAUo4nGeJepckSDKgx5J9DPpv2DKE6pGe7gMWHag4HokRRXNeEL4Niuz9KKI2H4Ki4q0laLx8mReSKEOjdK4Uyqtas5XQVLMKznGHb2oKCrfiqAsK0mA9YrAl0520bAuXB1dsJ7otKXjpEdZYwFEdKctNYY6V-SyTAcQ6W3e2KyyIROSBB7IdJLESmkwQP60tr5f5DgQdPBO1ZkLaURyJw_sIHA1j1NYf2LO37CoIA-MghxZLocGQVhXSha15ZkdDTCqgD7AAHldwFJjWFUCl9sw4HFt_B1jPOg4lz2iPgAzQ2QBh0gWx7RRlN0sZgEEL1HwbshEf8JmF8eXyUHM36ny9bkhpVmYh7GXmpEvgUY4WFmhEoXrNaDEBis_qEpDs9Moz_3QKRw1voFBqFj8b1aaKMI6THpnwCJPsOBog-vpvxHlDW354hgYba4BC-z9O0ZHQcrXGKNG1jknCDPXUwJhiQwJ_Rg3LJk1yrLshIpWp0VbxPqwsqZC-cX839x38ySyqc68UQiIRrKRMk3akpPpcwFCEx3Ex5VqeCzdOD5nHUdew39EcY4BLXkudCWPqBEhJ5u1vJQle6VCzgDB0Wnwm8Lyk1jSIRa9oH7CuITY2ROUrlU5PTIQsG7s-rzQk5tlUREWjtsjU6xwQRd91WsFzTayevW9TF2K584Doim_PCgDYRi6tFdcDcdhrEhgTkIvAcPcJ36qTROFGikb3g3zzxVNeexawIxZNVSt7PElqgyeOuZ2gCTDhA0uqYSprhjwM8zFz1VCmcMjNT0pGddrdabG4FjcauemwVKDnXyeqYRp5DLC11shwS1-KUF4SFcKUcm1lxom266Kixde5AZBahvxeQMYUzo5WJah8m6iSo2oBXSNdcPlsbnWqsIaw-Ihkc3AzBIptPBoC85eJTDCLI5JDiqijqHFTgG7a4a4-SEZjlRZ4XJw0yBxHBolibJCDMjOHsHQEMmUUhsrGfM5WevLbyuRj7FdQYHM9VTxx6WGYebxRLjegg_uDKjScxIvjsFWT5JIOf4NLFAd7hfpc_vOnjP1H56McoStb8DKIMrOYJ6JxgbsLiafEJbHK6wOnpjya4ZCwIdnT8PHPgzMUhy5LiEjQwx4Y6kRYFl4AVRY6UkRIGDocTOvgh8HNlzvBEwZkqnInIFnKkgjErV0jojI0lJpiXB54eTg24isbRGxGYA-XGoIJT2lPNoAf9uwmhmjZK7LDQc0iIqj7pMoTFIaFKGTaDdqhuCOef9R78Pe3P2M2yFqPjHmhGY6qKYQWWVVga4dOM4qU6qq-zySkMixs5To5AADlFXJeBO5UabcKkUKOAaayKxATGZc9yd0y-uz-7bHQRITDEgAh1Bvp_Fcled5fIhWSU6HxCE6uyPt9DJQW9W7jwHEijwfhEqrZJyeRymEgQv8ptkpeQxBh5EV1bjzS8Q1Og1-6bnG9PDQsrNdvClcfgwuscLyjMD68kMsXdFcWqPGKnUIoSdRItSYHiaqz9A3TVuEFeUIz90aKStvSo5pMrFrO4VOSkuiLCp8u_-m9KHA7n5TvNANYzCfo8BV5pqBVKs8_IzR49aAPMAEPtqTWyRO2jzwMcoVTOErGeQE1pGlhkYpqbhwWL4axREJvVAxBgPzVh26hySIkDph8vr1yH92HgYwPfAabvR4WmRpXM_3DayUkrs81JWWjhfzROvnkMGs7e8EY40kiAlSdeJC33fCNEj9yNeJmBSsSLeI-o_ALtifFY4qh7hwoTOf6mCPAQqs8hSHh3iZGxWECPAvpTQyd1aNm3O_drilr1ISFqsyTpIUeIsf29qlY8AIq61_RLq55lQ0Yk5Jb-XbNFxgwvk1GA6ukLFJ5hRFGKWhq46hAT2smO0EUISlm5iQ1EtAsrtGUrgGFh4qaQ6IEdzo8GRt5pVSB5EVfOAgItlI36gGbctaAnid5jrXbCskFAijwna9yE8UVzHAhxXRRscRXlmoMsdJHhMvLEigcTU0uLAi4Og4waKCirnuEBKhIp0jSQuwIpPYJkSRwsASVqQYHRZYrh9YTFUegxc5Ho18J3GVrmigBhu2O_paWE6zQGxYo5mO3SGH_52KBBl0Azu9mbN0foyaMPtLOshUXq-selu0HnhgbY9kkqoLQpPEK_IsdaguyddAxdo63xudtSL0backdd2siNxU17yDXtmTxsgKoOHKZ51VHlZriIoTbr7WeHa71Ekw2106IDigRVP-jRmU9Bk4ACJXn6mB6ysblc5WTEj34wLEgTb5DThl05ZTUHK6FpulVJpGB5KhJ_CXmQnzVTZahhURIcmK1NO5pAp12WBZpD3oe1YwgJ2Gqlkw48i_WanBQrlz3FqnzJ-Qo7tLaLVzloQcYkRjn0nXV6NnOhY94U6OZopIMqIEawiY3UBycO7koZ8Gtqdf0cB9Fq_4r9LU5G4MUPaBh9R6dr3KxvCDNLc9j-SBkjUG9HOPH3GV5FxZ5ZTqe1_Bq6WvUZpo4lsb5pfwgOJgPc5CtmSQI0xQIjAO8LsO_EppnrLiHWnfz_GcYA4H059YMZDBlPgZHBVQV-zEkGwSeVopm_wKKStZepa0L7HebJ4ALnyiSolI3MQL_cRJE11hn-RB4BRmmaCqLGczLRpH8BjyjGOyfmypsQ5nV6dyDXgZYARWJ3cs3ViUCVhLDcIq8uBT0jY-lWePfSoTwXAG89HKUmw_jsLcTTM30EmCBsS2pCSqQlarWefqpcz4QnwGxDyr8rrYYeQkXkYTz1XHvXByQsJwWF1-SxYOwusj4-e1g-wXRZYlTdp0L8SBrMgpqLpOSDXqioHwLX2Z6Flj-h5zaGOekKpu6ksgqUTuQVWz8EA6htTWOW5ZkvQkFquXLWvLmMz0rBkyPSa3ET5eIS0MW5ofYR7UMZnjB7_vb5fTwE3twPbjIFaKjAFDbshsvqR5tIDZpeRVuOsNeUGZF6_VaTSULoE3SOpb7Jwa2mqKKYzcrwlkPa528HiVdZomSexh6Yank7M1orkWyvtFNN9DPtt2Sos8LLLU1qKvyEK4732JOAOo5hWIbEGBYD-FG2SF1lsVUnq_b7Qvj1lxXWZloJq2DqcDCy25-48Y4GgiIiHTV4RG1WzVQN1EfYV5B3k9Hc8xsBjOBwPY4LoXGwnZBtOgUFXkitj6Cu493O-Tcq_VqCIXQ9jFFZsJ4jzwSAyWSJFor0BI_IAW_cQdgHivcDY4NCpIQl0DPMoAju-NSWrgc1aQjooCd_QLhjunA4xGHbQo-uXwWusy6iMOWY4ZKxLBRT4gkRiI0K_xDvCkFpb-UxpOO6bV9uTXVQC8UDcKoyL2nVxZ08DNsphjVvWQsBcNveLMk8Bz0jz17EiJNAMmv5d-JWW290lVP8t4pASqWevLVUAvt0SzUMC6G7I4n7nAJTIqj0Hzm4q6lj6P5VqTWyuqyEPlUCGrWWowfwjnz_XaKqrk0ldQwZ2zPA0TPyeUameugeavtKLHFZ4TM2JB3NXrKv2i5x7gI6LeHV5AXhNJJnwYrw_6ela11cWMYZZixXgkz4ljydMsM9HwhuG6tS27SkqQjZiGj8y0pBnSWELng87P7Cs2ZKVJbTuRmwPfBys61kaPakKg7MjRGws8cZQn9lQoBZELVlaW0yAPtONZ9RxQOzHBPgLKGZiB5eqBZRNp6aJbC-isEmScbDcZB_3nkicHsCCyLgxRkec5kTHJ3CSsBB0zmJsy51C5UWRynDb4lQ-AKLwW9Gq2mMOE9KQNIsYit9bnDFPdxGgS_l_kSnuX5BRJmoMZD3qzrxE_cs-J_KInO9ka0hahIioYeQW63IpAhzeMZgsKSeepWlsY_M9a_zIMNQfRaBANQ-H7uXCu0WdUap5z0kGUGs5Z4O-9ygdnLIMRMT5yH7R-rZRxLaZWicJlNEfwiIlHdEX6XpASOJ4Rr1Ql2GrkqvJsOR1HGWAOBz5zfYOlGzWsow8_AkPJOCXLOH6QpSL0qhIClhRroiSQmzk0BzxH0iifEfdAw-4g-p54Sbqa8pv2oOBmGu9Oh0kstV9yKO5ANDaLYdxYRIDs8JmU00YhIok6HMZH-zw7D1qsMKnfG4mXCW-XgiPir6hzW2T4dn8g-LhFbAlEOEOFSc-hZ0nrhOld4LtTOaMe919Jrc7z4w-L7PmebHY1fk2iziuymkNrKEJdossWypLynrV-iRynNwSMpSAiV1-VcrHUOEPW9OJMDbiEeVCrZHuvFQIpF561jnKMSnPeB5UHm5U4K_lH6mVTJVnU2j1HUgaFUIsyIOjhrLP4ioagF0F1BmSlYi0CwYMdUiPEIopv-89qTxCFTcOBWmXRp7gIDLIEObGIt2nuryIQ-YMs-YopN6CxZMzpWQl6ZecZKUhA80RDEBr9YwwIwooOL7sz4TAoCkopaDqpr-MeqoGMrgYR2YC_OtoLpWuW-MsAaC_wn_CByrwqXqLG46y0NS8RtDD3iiVRM_hl9EgjqCU3r3l1L84kIYc47zblGWa9SHRmNRmf5nGN5Aw8t5lJKBCuixnKAMvRHVo3zDPPeyeXZxsjUXDCwBTRHmtYTC_iDNd3QFk9QRvyLnAawLfIMk8K3h1gxywHlwhG8ttghksYnGZrGfSG3wnpMM8L92F5orCJEwM4W500TlBDT2qeZH0rxJZq0GrcF-FQb9HlTp3soTJFoDFigX_h6KRTDCGRxO6Dy6zuTFBlgkdRkRDipmFomCOyKVF_VrSMAK7B9igXlLAG2GTyMAtE_gqToPC9vAjD1AsTpQMZDYt0TlBf1lZ_zttJZ44b8lpZ4YAfPTKgomo1oiG1Iy9PaKyxDlRro96K9AP3J1IKX06K0LEjEmoUA92ySAOBjNx3iKER8e82GxWv6wKN0yINo1BvuNGYqAdPobq7kPTRBgXx4jwnjsbZMRoOafyPkbsGseoGft9ZTYPIx2IPDmI198pBrswwwH0zexXnSqkAVK7IDiGO4_qxl0eRejejUZEBUr3PbkMqN9X1shzOvmc7OplZNSDS-BojdxEy--hwbarCMAuCLEu9IIp1ebDRaki_ZVW_IDlWRGmWk9xxc51Po1sIaQSN0fsAPWagwCkDrdf8aCuR05cn2IMvCcPFkr2YeWRzUv3WuObwi3Yhca2cRWKSBWu3ZAp12lggfFhhz5yBilblNnDixC6KlGQFVdmeRscjvT97ty2SPM9zg9QlJMlyxXuNTkYGXsKo7Yh69D8gFAqopxhuAtJJoR4onbjUEbfdtGMDCLuKVlEY5J6dOdr7a_Q_Miq6R2xiJB1akecxXOlCg7oZfY0MSIFRmxMJdHNDf6qQYQVoBR7iWOWJduqoDka9dezVYOlOFHteloYInaarmVVnIkPlqOy_U5E8bwdBbFPfiTKdohTYDi3MHfoZg2LoCWKzG2oCU_PEL8LtUVGSzix8UDtZqkDeA6HZmztAc913RUAHVYbpA1DE7NTJnSJTJDY6KknvVXvAa1YVs_JsP4J98nh3CZGXpBop6ZB7U74ZVyhFkIKZRgywvic2DNesidntUlnF-CX-aOjSeLj68uRYWJ8YwEXCeyGQ-_i3ERXD-LroR6Buc61PAKovKphybrOKMfkpV3mesq5Z61W8Wl1XPHNhz0r_BgyZCq-r62RR4BSukUpkdJQyInAF8yxLdcFEnYdXW6xqMBCGPtwbUUPDQy1plOSemV-mYo8PrTSx5pdhDa0bBUM6fUi7boA2wm3V1wfDBNdCS-pR2h4s0eivzsBkZvguy8DG_gYi9UjBr6qw0lKDd0KQ7Vt68Z8E3nT_Jg6Jgz79ByQTk3isCxTL68OfVDzy0OJv2XefOYT9snTQuedzI-jc97kOWeMfnqzB1Wjlh57-w9x96zhlBKWPMVQDZHN90WL8GssawFeVbeGWeYUqOvAFfZ7B7lsi5rbY6NTrsGzBq1hHK9XcNElSN4zSnv5nT3K0OjgrLBmmqv8ccOvBb1d1igOLyHPsbNT5nrX-P9wW7mEGk1EgyPe7mB9CdmP414QCX9XoNyNOQZO-TnAHWNmveMEDVqwIgDj0PsvULwa-l-Ht5CgKEqQD3TH12pAecrw-ZLe96lsF3Fp8-EjOsJeBtXVa8_8p6WS2d-isrpKW1vQzqSkr1wEi3SzstmM_4azGbtzvWZ82Nvz3h9ZXsKmejESiIKhh_E3tpPDqMqY2z3PFGFoKXFfW8coqgXthhzrBmWSnumPchMY36GsPGFEw1VyPgmJUuBTM-SCmReY76l3x-s4d4tVJZhs8-Rk_JbPb_b_odvcdgTAOYYEuSZ0gTNw4wAyTPI_yIS0UvT8Mb4n4k7SEhC_SwMVeVw5JcieMoyRJXOqmdky9EP6QJ8zNFjlO7IYFjQqviAvPKUDnJ_Bmu7zPkB6QQbToDOsBGcM_MJo36wE56wH5_24PyMgLHdsN4OzHGuVC82Jt6e6Lu0pYGte249iNMz9TfgGD4aoY_Dgs1HSZ_V8Y4N9ZShSLPYqAAzEKHXgWc6kTJhZEEK5Fe_oRDDQXgOk4aA7O8YsmgkTV0RYnAxj8DP-WeXBWOc6EMkQU85U5EZZ-sYaMZm-YdgSfbIGFwdd26zY32GnODM6KSX6DliezxhUGkyABzvE4SwXiQFP9IIMC106CIClkK4kyuFAZYMT8VjdJbc_RR8CQbOIIjCOr4CNxSzloEoo_UQykLuWs-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-ems-en_39637chxHGm_SkN7YYDbM6rzgQRk0CJtE6BMrSRbWPxjkJlVWcNe9nQPuno4GpsGBF_sAywEX3lfYq_3afQkfxwyM7Kqe4pzoPpmR5Blcqa7siorMzLii4jvexA_fRA_fRA_vYn46YbFTyH4OT24AOogPfyJ1U8DKTVRBbypcpvIBboSmz0r2Y0UiN3ISHtFkK69pt9_Xt1RtGU-2TUD-ZZPds1ADuWTXTPQGflk1wxoW-WaN6SpvfkoAR2njLKX5vMWK0G4Lz_ZNQOuyU92zYDK8ZNdM-BP_HT3KdyEn-yaAS3gJ7tmQMr3ya4ZUNh9smsGnHGf7JoBE9unu08hL_t0710IwT7ZNYPmKrnmTg_YLZ5bGgjC613TJnGLdySl-Z_0ukHF-ie9bq6LNNLNcE19vFL6WtXgN1x79obbzGxRLbN4u4ISSv1T1T5C9RYjxzLzCWciqPCQ2xyXytzizJdctlxuT4b82ivuyi0HgLNc8iNg-m0cH4_w_gJXD0DWX-DqARz5S1xdIMFf4OoBlPULXD2AeX6BqwcKj3J1uYItlx_s3ttIQHqLJ1KLtxjmPlqM_uWI1uEtRv5EYoj-IBGpwVvcxH20CEXq3mv93WLke4gBeh9MtA9uMfCkOIK_tJDl3-LSN2fT9xZP2OpvMc4N6ezdIAFb_C0GuSOdvH8yIW2_xaA3ZXX3a09402-16u9BrO4fUGjLb_OA1_KaSwTkucNvcd1JcnFvqITB-zazdVeK7yk_Sjiyb3UnNyTRdsMEDNW3GOZ-FNYe0xCe6NuMfVci6alNInTMt7mTT8LXLHifJ0S-zT3clTF5ajaEDfk2d3JXuuSp7SjsGDe_k_vTZ3gDJv3iNx_-EzSUe69TWq9vPv7de7OnTK50Pt_8Tu7eGj31TqR2_uZ3cvfi-qm3IwVDtzyGbl1R5A8FKdq53WE-XdXj37KUudwmQLhhHYwPQ6TM5BajTNWh-CtLgcQtrvzxCgpvjqSo4DaG8Y5VB2IEfVL_luZ4X1jyZ7gKMVxdl2zaDVthpeL3vxyoX8JgR5azeamw1lcIxvg0PFeLDfVbUCk0cgRhNc91iacDjhqkpg44apC8OuCoQXrrgKMGCbADjhqkyA65hiVldsg1LEm1Q75XSbsdcNQgMXfAUYPU3SGfVZJ7Bxw1SP8d0jZJgvCQ-1VSiAccNUgyHnDUIA15yGeVROUh17CkMg84apDsPOQMS0r0kKtJEqYH9SV8OvWQ56skW0cJ1F9syCBxeki3VPKrhzTCkoI9qOPvU7OHnGFJ2R7SHEoq95CjSor3gKMGqd9DOoiSEj7gqEGqeCf-_-UsvySODzdokDM-3KBBjvhwgwbp4cMNGqSGDzioJI0PN2iQQT7coEFG-YBPKhnlA65eSTAf8EkltXy4QYO88wHNoGSkDzdokHw-3KBBKvpwgwY56ANuGUk3H27QIL98wCeVVPIBt4xkjQ9okSRXfLhBgwTxAc2g5IIPOL2S9j3g9EqG94C2V3K8B3ynkvk9YFghieADDio54gNaJEkcH9IM-rzxLzzon4PM9F8_u3x7Ra2Od7n0V2rzDmvHRmPAc7mG0s8sQcNrZj7Bh6HfuBZO81oXVVJ3ZRNFcVe2KgKnIk5KQvz5sbHpcv4Zi0oRVFJVXUFMTfwzTo0_9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GQ-9GTevSdzlMMqTRrFSWp0UXWJ6eo2r0zXZLgKULSK6FQZPnoczyWcfZymcz_44zT529yly8I8F453vganAPN0Ae7l_vjaSvu421m-TpMuNk3VQrykcggbi1JlcUdy8_26277uFkiSDnaLEmrn572OH8PpHZmijdu8y4pK16qt4qRsdZ7BYqsLXZk4Udq0UZvkOtVF1KVxCb5H2aVKVaQQfctHxc9-lkRJcRSVR0nxXZw-jsrHcf2vUfQ4wgUoc1HHRifwz2fhDP31F-OOZQ1kSiV6ammTNBAFNE3kJWM05vyKUDL4X2Y3TS5OK35ArN-q0mRp1mWiqetzmZ5_G-V3LvrHiORZRuQjzQOzjd7ASCerL-Df2TM4oR7P_Gwn9sffwhKHn_tjhtfZ3AUpyFZsJUOdS0D0w0SfDwZ_uyayeLxSwKs_BwdB-P_nAXvx555bnR2-MyQnJ-TV4ZDH9sZeccDU8_3BgjVHcL4uUBAWxXLm6LQ5hRsEXhcNnkBODefIqeHQnVEi26qsszwPPuAp5fqc7It7cCsKtjxCjTCSZFZ6vbnWzXEiMGkBEQCEG13llW3zutZJUeoBI_s3HNzCWU3y2JOrQCVRVFVJ1WSN56_vTGHSOGpCrbh_Q35lloqDhaBW_aXZ1Yr7EnnDA6GsPUocv4YL_DtJd5JGlhXGUZeiUcZq2734xsdWLGpj7MnL8LnziJifnII59AnAKOAYf1jPwe1fIme8sipuogV3iTlXUho4Qy9rLYTZXv3daffN5MFWDkW6CvmuebBjkms7H2s_qK6D5-99aIn37UB7wavsIN8jQzrFnRCumc2paBviGK9IspLLJcZhBHLj83yz5sIF2OcFnpQ2jjieFMJCHeak1lEayxJoVNyZOuRF_2PPgl4bFE0jlAH1-tx0oco9yi6uCfRSfqWjgBUpYthdut6gTi6efiytJJtySiWlzDQcdFmSpJ5yP63gKCnrYrDw9-buJ3QSwQ_JdRJrlYoYT550laoDPY1AfcCDAvpisWTI08k4MTu82qBlhOf_-cd_Esz784__PWNbdDyDGdz0KCBJspGG9MpwFkgDC-YTvnv61slbobuxnM-eoUAlebjshaImDrxOuaeTlb8pJEFfoCLiyBiZ86GymBUVYzO0EKEC1PpmlnfYERgwe1J65dTIUNaJdLbOF6ygCZe9VMjIPqU0WnRFE4GHoJR_fSVESx0rx9tpRmE10n6jQLnDl7jBtTtBt69Rb14Z1TXaE_oHNTKiHPXo0TOrIuytDJLuP3r0eLBbESdEqdnm3dXuYWXlP2-A5-9IkeisixqT6DIWuy1lN6L59OiRpfgHLxSPsvfgjOI9Ws0HUbbycjTE2h_UldD93SERsCOVUEB0kSs4FmRnBFU9koCGW94rvoS3rVZXqM6Av3RhJBp6P7OozQuG1EKydOv3yyTsqKaVcZrqLtdF4dVtgjoi-xQZPgWJbcLpQjfvJx7s7x5BH2fUQ8xQDDs9xx2SETtSLlnU5lGTVHGXePdMCpZEGurRI5ZoeIu6fijmgHcOUfIlqi2qc7wn2qoXK5dwphn3Wii9VVBC03ynbMb4zrumUW1a6rbIvLBLU8Mp02TdUNiFZWNZDUmbU1Lu3oo_eDwLZVT4zfMDsSVjYVi0bPC3SdGWtM5NbTqTGNF6LCBCT-p0pJ_H8mSbxenbofDH5EGC6YEmKwyYOTlIIpIFqobKIvjq-ai4VKhOvJ41TsUb_UOx2xNmr8ibSMWpaiIZrc3iuCurZo_KCON3_7G-2KCoyc__-V9WcNJGofQTwaJC6cfRb9itlSuwL7RX7iNwLuq8rMvSFLFoEbdpk3Y6KgbGH3y0fqDqw4Z3Yh6SrAWfpdJZXvl5KAsTR1EoduTnYbbzj0h9nay-fvXNd09_8_L5bPbzTz_e61-YntnLV18-fUlD_vyP_5l95J-ff_o7f_SnvwswbytQdj86W5yu1tbM4F8_dvF__K_96E_3fbB9_85mL373h1ffPH_2kWVgklK1Kq5hH3o5uARORQ0B8mCH9IYVuHsXY4AnBW4IyqyjIXA45BJs9K_BueIjjj6zJv8ED8keDcYl_npi9cSmKiCuBs8386uniLu6NqHX-wGialyG4IC_tCk1L5Q9-y06RXqfcLYLiN7wy2rfiLiys2AuDLBmGBz8_TLAb1iLDj7we_vsFopCb_93i-3n9PvPNXiNxsuXf5jhsWzlebxWm3d-BjLcb9yPcYynLhCyqRmBwXsFoarXd969vtOEdpeeCDhMVyWpieomUakEsnmeF20w9S9W8CxLOn0DF9zD5EO4nrYyu7e-XBx1IrekKPv7776C3RhYFqupZDX_1FAOMIwUW_Yb-bBni0Su4_xktSCFqh5eSv9ktlRbi2RsBx7aYgVrd0ES8h5Q7t9R7INS3FMCim3eZHWbZ03htaSUyXTTtu3gyALH8eUISJk5gGby1Gp1lXVVrbPGiPh8nTRxp-LhqYWpebxnFuNWV062c9Y3G9LldrkanEN06d7aLEKQisYfoZzUehse3hiJb1FPbO2CDFL3NCtSWfeKvcOXDW6Ugf0PsY8KHIgetgWqm02J2pVFohNdFx34Jn5SdQWOVjGAUHBW49kLiye4uHonqT45vWXbNLVKYghQ_FhdlcE3dTsQgA7OPLtuaDRak97nX29Y5m3YQrGFxUSqaVaHvvWz4A2LT29zH4MTwkS1djuak19-u94c9Rd6oJXHWDhHGvC1xWaolw47wyknf-MkuOYzp941n7G6lwO8rGA7i3_Bx5YXfVgEOSMFLS_DTLmQuZ-bI_gPrhiGe-RTexVwrXGl7dyjM3wBfhd74Agtbu2ceb2zOWImMBu83Hq-4RammRPFAdA44fcmsKpUHNdaa_FHKoPFN814cSWz5z_YxeVf0O2Wl8mqKk4ylYOf7XdvWRRtFplweaGhDmGzKTVsnpa3uLNp8yIgsZ3vIm08P6TPizuSv_ecrG-Pwu-wWAfJyy2pc9PRxEN4aWPMOK43Z05nG6wWGIfl-hxX_LmTtDua_clsNKy4s5H4NwEj79cLLOYbPcW3rDsqwqosGQx_gP-zoaN9z-wgK92vlxeYaYXAx86ELa7xuzE4GM7glDECQsJ9iLLrxBpp4yJPsyprOuWjuhTi1CZuovEauVHPyPULpCqqRJc6A4PnYb24SU3ahgHk02DX2H2ijexVsqwE7lHg2lmJb9h3sLPphMPwfsLNirD_o62aLu68_x_0yAhGg-dMu3AKqdbEoz3bLNYXlLRE4fqN05hPKDjEIEppxLNWvija6lWytWRtQlp5ePqkKGTbX5CPSPKqZA1sIdAlPT1ccssnHgfNLeZ9V1w1I6U65FPvq7_bQVKytgWXMkoScTNVl-i8VIFRsLiP8ilgfimovmk1541FoIKF7g5YDNEuOGCekKaswS7UZREp3YjSdGGyPDLDoNzeC13ZIkkhkBTgR1MRt0qjtEjyymRNJNhcUuWFHsrH7u1imFrVsamjLKu60p-qQTdUiPl9y0ie8_YQFrnOTYOZVOIe--OY9ePpXX-0IHL84tO2aDWEvaqK_cIPWqxC1O8Pa_QkjzgsbwwmMFdXjKCJ_LFFYAm6FVAEDs9Tcv3wQKcbna6o3DmzsjRLylwXORWfMsokTVsh0PdqNcTv5jOH7uGhZR3OAPfDiAz3ny-13NiQgW7zdjWZu0rluoJQrShbWQVBX1iI7P2eAUSrDx4ih3iv2nDiyOqdsqkDP6klSGZhcfGPl3OOb7CJGthteVKo0s9r0GQWonffOrBX_HcCfWG2wt0233G252EazMKOt68G3QFNkzpJWoPz6w1F0Momwu20bnt4nyt0qyilhvdtNhvw7sh9H8WSuLrhBMUwjtxXznfQluQpHheU7mypCnPVdZSq2r_1oCNOWm3o1pwqMIOutDAH4rXn4NnydFlNc1eRiftva5ZXdFP7qlF3XrYuVV7Hra61P9SDrjrfW0N5CHbeKZKya7K1P7PYBt4pSQLbhKOLCSgU720O4s6VrHARQwg7lUnYjAF90WU8r3_OSmWwqE3elQJJB51-0vTz6NEfLYqMK7F3mDJB6oyCwI5j2JyjgfkMM-Fzljz3x7d90ulK2Z1sCxwwdZV3eWp8tiloHQwk7R89-h1KH9NmsfufTAJM2ufO1LtqJsr7LxgE53XKu68nKXvrD9yp2nZnkcdgfSNVtoUc1EGbYtDSgsLooxJOnm5rEjh1xL1s4xyGg1H4vu9aqXsGW0rcXr6Wu5eJR8zj2GjwRXSSeTQ-6Jp0j5jwIxpyiLYbvOOl0mZJCY7GBrxzG5BSlLnd2ggUNZiPnAbznG_sPkXAu4d7mRvw4mKV-icIejTdE9C56ctyOKd_sWKPAx1rAdfZPNnKEnUFxpo_jWALfMPa9zsXEQtsRoesTfXcuRJ4YmbqriirLEuaRmyhiuokzzMz8PvgcP5yp9rHZTS3rJA9Ef3GddxVZZTXXSPoWNdVcVaFwU1QY0wHIeOX8Cy0QiyMhYeBe0kbY4sp7KFr076BV9VfwRo7g0DiI-lN7_tY7G_GsSQm8E9WFKkIrHmkLpXDK6YwwTSvIHJKylR8yrZUOof5HUaP2Qi-Unuc1-naCBWlKQ5U1OIYwvfipowG6JV73BfP5j5Xfr5Zb9fNeunOLt5z7lSySCDE14NjanFqek6kkrE5snhVg3AEh_SEL781zbvz9cJaIzj-torL33a8ev7SCA_jgQXU2gNnWQjKolR4MIFZPTu3Fv8awMoNzsfXntS8xNn9CH0agk_z2ah8jbOznBSZ8ttirQyGV1Xt10bSdpUxeTNeG8nsq8DSnA8M1HTNYJXGVRY3ddZU3nLrtGqTOLDcX8OyXS7N0qfBO8kgDLL_znLBH7rO8Ot2y3SDRC_0vp5dbLioiO5vHmYDrO3vXZHDGXHHQHRPPgUZzn5gNE9Wu1bTorsuPOlDmMeXUsG24dAEHmxDL-ZkxWwzvTPcbsXS8kUziU9EmCWVidjaLVr9hHbYzOMb-GT_-bl_qM_ZW3_D5Shn601QvsFPMZ_B-kOzYh1ILLs441s-WbHxJzx9-GIn7EoStyatwOtPJdego7qA87geZAI2VEc0lwI151vuehD4VjeqQ78_PEZg3lt2PBhqngcOhEWGxQtE2E7BS1z8JYDa3CnVS1kU1pTBiAtKj9E7RJyHlhnBQOA0rFenvXvTfO-2qoZORm2Clw5rxO3mwVv3IQv-COYBa0rpUr_qPabNcPnc3r-rd_Ow9MIs26n8hOqSKDVFVsEx6oOvWsHGjorxJk5HEPKtTXzdpFlbVlXbCYJsavDJ4H9jBDmAV-eyHC2uTC-C0GAsBrY29ut9yKjdGy-esYG0Ff1H_FNb149ffkmeBiGxcwh83i826xXVGXoUlyBlHjkIzd-ZqwH863pIXO7Ne-JSYyLQ9cDhpTMJwewW3zF2BeAZ8_OP_3QPv4Ktevzzj_89EYlArASRalzkuYf-uqgrTFYk45eZzb5Z9O_IVPqI7iZ-UKbhSFZp1jRlIkmmtIiaKBjDu6AufR7m8KgaSU7VuT1T5_Z45XCVatVhrrwNmIB8wSHpwBmu2qb260rlZZsPTqIvXDRMzhO6Rh8JX6n2yFo9paneVb5hEaPJGqCyVFGm4aZKKcOLSqOrJIBkXnR-0XifWRsXH7JdhZPiyJ9jDICho-gjdTuzVLMO92thdUmle7ts3dHj2dcXWxfED5w1Sk8wQLI30He3FcIJytekUnX-ejlhb2pV5ymc6aquvNOQVWkVZWaYZM6PpT7B14_yaAxbct3BGRx08EzTeVFdKuwAifI8ERvXtlUXpkC-p5wDp13gHDnt9wK0VLxNOSHOG68gLIL5AQPI9bMnq33Vu3xuwwXfSAD2mmzQGz57bB0t5p1dhb8tycSiNDy7CY2FCe_x4L1yBbGKRrfLl85BrA6YmP80KYxpiraoUh2i8lHUFXsrkH0h4XIBM3FFZbpTRS6RLts2K-Iu9tcHB65NshCEPpp9_3aNR9gFnd4NmMh3lHpZsZ_-vS0D3roHx7TL-hxM4PD3Yek_mc65nZj5oFR4ZvOv8jUOLCkapRoe66ItTbe1eQhsvZiKOmEG2yxp6zIyktdvq3qQa_-OSAdtaLJ1lkzWBRyaCBi-8a7ha331Zj57g7aG_4jHOUL1bl1Iq4etpVbv14u2p4NxgQVtrnkRDo6LFe8Uqn6gkiYsDmecS0pE3xlzPlUK38ABm1RJZhoPPNRlV3RxMjhTZsWx9AMtF51prprl9L7UicF1l8Kk-XwhOANFUSRmeFwVEFw-32FImiiPrIu0hsA8U5mW0KTMwRoHN_18H07Vrd2y24AxpnaZRT_A1Hx9wBIzx9iDgEuFTiobqnsD_ANBvuwSugoB5-m5k_FysSQ3Bq_FUTuHBicr7kuhOggsUnWZj2EVM0f87gThdJM7RJ3VPlmFZnsqZ9elZZLnOgpyhzUE4W0dB5aSa5g8yocu9Qrv45yoMDnjsTnjABePCGNamyulsMQdWri0rWWfOjCKpqpUCy5i4Uu3qriDtxum33iRJJRAp1aHGy0TzIrWcWzKuvZRSGnyPM7DhjQ-GFa2VMt5Yz0ZH8seKtUzPdoxeit4ILOfan95sgrCPC6zGZZ0Mxgw5efUaVVBrF7XkoRqWl1mbdwNUpG2OOfGtTmh_8Op7qd0fztRhvJxBiETqyt4u5jaVlQlaKMOTnv_CSNlG83Qt-HHGVyYCqjYl3B5Buo-PlnlSJrUwSy8HSQ_FQR6HOZNIbwRbO8aQhnVSOV9ljeZClsebBmI5K9tDYgveoLNCysHn8bWhNrswU5z_snKOunaMOoOv7uarRuayVbacnY8iImlnqmyqLXJuyL2iYQc7W8yLMDDpT4izbt-jUcFej4VVpx53DJpsDE0tN9vpDL5DdW9T3XB5FkdJ2mTdY1k2gNuP3_GfxesLFfQ5x0psBgYIlMTh6vnHJeLuu2D2PGduRt26iNiVRVRVralwFaV0grc0jK8-5fDzP2gPJUiy61DVGy2k8NA-7aJM7gnW81Yvw1RwWKsL3pG4iUx6J-b4SubHUCGYty27PM829sacg0ewifA7i1OxI4lxE9ZgaXtYmebOokYePMODcw_2fQFeVK2vwTRZbNRVLRvsbdz1U-u9bbrIlUlUdxJf0RdNmWXReO1ns2-XHITzvl0fWlaJEUFAXCZJ35h6iyHZ6oGBUhkqvHVgEXHAh8zqHuwK-0ILJFhF9GiHbt7efb0ZNX4e5tqHKvTtKxKVaSF39pVXuuoLJpw0X3JgVwvK8xtoMEJTuvBBxdoXdGS40a6GmAlrnVm8HlqXueL9wxa-E3poJNwRcv30ESc32wFYx8TGHo1teKKLIsLneuszHwzXWogDky6crwEruHInICaYpXAhm4yI-maWGcqNiFM8c01yUoCQuEYAAvk3T4CpBYckP0p5ljdJ7in6tES2FRZg50IfmMFzKX-1T93QNXc5xPm_vz16GQAYln4an9a9O5cMzsnaxPldVqnWac8Ah8wpO619r5sG07HNWLwVP3bD9MpvuIRHDbbm4vIkF9KVNKNF7ElHLInVmbrqoXhcdaX7F3iY9-d4ubtZEld0UEIC0GPtPUFZK5-Cl509hn5obwHDCH7uqftO-euMzshY1iGATBswKX0_t1ZctwdwEadKg1Nyzg1ZRbXiX-srqurti7KYQyLmAPVHdoO33OIun0OC-3kX3xGJHhyiFfXLRXNYvaAznEHFPnaO9db8nj26NH5R4oLpvIJpq7Trm10bHzAp8AvrrNqWPz3cVrciRRwpJVOkqYrEy3dneBfDUqsqM1Q-tQxKct13RzGLbiG1J3sWFPqAnFugF6731FgZX6ABWArYskdunx7NQk6IqtjVnVgVCX01VGRZE1XjWIafGFDxJMqTwbON07DIAHWhGWpU7FKg3XHhWo67c0eWN8KLPzISVTbXQy2cefgxcpXBof51O_fLuBGGSSeXRqKq1uEfaxvOJ85ihaaNPqZg4BWg-Eoi8DB_lpbrmNK2eyyCu20nbZxW2Q6j1J5xKKom5wZ0uwj_taFXBzOg9MLVmAxeOsT05hmuW6jNFVt7h2HRjdFFIcMLYynnamWXT6eqdHzWnvpMDcXqthPXYUfwgWKFxuAZnTLYMvpuEEGEbBYEGh3EN1rKpF3ce6c6xWZPmBcYLBjg-qsgaUCh35UB6dLXWg1cNl4C_lo0SEsgqkt1-t3YEffTR3FdVKnBQQvupY-1rqFeL8Lm3F8_yaN9DhYgq_RZrx2XRonq0tYu1IYtBNtwxWoG-W1vnrsioFOVor6XuCnahv81K09-qkrK8IRwq9ONjxmVVm0iW6SXAmymxQQqWXhTKJDMdusl-ykueoj7IJGuuIp9CEqyrhOG1OniV_uXdwqVRT7ul83rj0HHh8NP3fo0F_8tJzI1OqP9fU2XWvAYYwL04j1jasWyUQCTA8RJvKaCNjFehnfQzAqpJhkekgrMKIpnI6FiaTeqqlrZhcdPywzps8-hKnD1-41wo_fqg2m78IfYT3Qa1cxBn-_2VuGlWs0BEllJf1kAf-7u697MLjLOY9-rksmU55BERDK-f6wW3-NDit-B724YJJd7XMzVQqg80RHeZRVeeXDgDhpi7gz6dAL4Yc6wsiYzAx3712unMkhfG5zsVp57whtghQeDn1gjSV-jFjCc73xa_LNVNSKlZ4pFqun_l6ztki0LoduRnU8UW4j5YAf8ziiSJuuLbpGR3KYd00BFmxUYlMdx8GIkxeN8w4Wi-mSvPEP0cCE50lW70E9R9Wy_hyh6AMX2CWsd2zQYmBPBbxYNtfgClOsj7jeLMAFRg-McD_uw-HqgRnxA1BjPnuTdCU0hOQTovPLruXlW3z3YLHeu3ftr2qrLGy8PPEywUHJU1UlSnW1oAWFynLTjSc3mX0bvMJpECI2Zadqk2jpwkySuNJdFe9kG4VVkhpZ0fVhCN8eIXNJHQb9k7ZZkAlmLl0-xy6ylriuLPOD-4Lr4FY2YsA9wOUqVNjTB3Ac-emDyrkJYgiTlEXZVVnc-igb7HNTgVEeT-FQ52Fizas8jXWr06j0h3SaRElnsmpn_npDMfl733dHVt8RXJyPqhDmgf1z5dbqyjX1Erht79Bml3mnovco67E_X3P85cv5fXUUmpqTFeEkfOIsF2cYZDgMYYpio4haFccFOD6-hCEQzPB-3ivP5EKhMRzgy6UvrBjsA_yK7ZOFB3DbxE0Tfhm3D2JAZxJHUohNxVNkI7najUqTqeYwQMnwviW-PlM9nPZYaI7GtDcNzjEXEKDFMxQx0iVtoH533tWvX3DRzUS4XiYQ-TWtyVu_gpKqyWGGBz7zn-JBrQfmT-25eNS_haVAb5nS89ie4R9nqksIPH_wkSDaKuV8KMu6qUNs-UVHpo_eB9nAX_WcuKcEr7Qf-Kzw3FYzEnxCzadYXbx29YAeXnGFawIjeGRBeaYGxCs3BKSoQUkf8oQxgjAP4IOQncUiu2hXdls3xgu6q3VbZjH48pn0-rdpXGbdoHJ4tkeyZaKUI8MqwTjD_jEfVYoQjOfQ-HaxtSDEh9lv9vFlEL_fKmC4SmBlIpbUi9V4HyM_BdsG-P3QfWDTsJut4ivjo9iGY5QZXPQu50Sunm14xBAJl5j9ivSifqyZHK8X5BJ966a_8lRbpxuO-4sJBOGRl1dUCrSavXj2HC7lcohUDfyEygSGzoDllMTeGUfhFF4azSAf4x7HYmz5AzEXuoc0Z5p32hNrj4SrShIgM_--3KUYWAxeFrFbzJSl1-CRPJDkuVBspwmLQQ7Rpiczap4Zo5S4mXB3eSISfkSpO3GpVY-muNI_6uV0dtcvD3hFdAvKgqQWZmDeULV5FyIe_HZ2RpSZ9UkxfIYVrcvFihqXe7KoH2a_VYslV7R_buvdB_XnVvaS5kSdgf8QrEdbbgC_XmKN5YzjxmU_w3Cfhr-Ej7gCHaxcUL7Jwd0ApU9g9hkAY9otTlGojeNj_IHvnRtusDCCICe4IEZM1uf0b2N3-oX4TNooaWqpxO-Dpf0cJJSxscRW_vsGKSq0C863ISfODrjNCbaeVqs4Ie4k-zB7sUtE-sRj8dSG6s9ctezXvmRjsR1sIpegQs9NEk24OynXs1pLqpTTQEi64_M-lm2AtlWQ7rHNmePdNUjo0DBMj-gaEu3WJXoFPDts7k_OK58NaZ9QKRc5VLR4CAmdIuiJ2kZ1KjdtLXRpSQMBSdtFQ7q06Hj23KVkkMFxvTo6XcMUTh4bRd51xhhljM4kB9NWOqoGHsFTW1v4xxdDAsuwFdolY4ckZRZJdlVa3DbGOV-zOXJsP1jJRSXZxPaLuD5S6DFIwb2jOJKjR-HTJjyBMYR3ZMB-MB7mlRAHwymxbhxtAft_gftCFb97u1K5jn04uFvbmBWDFQbhj-D-cDNDdgzereAgvzMrtxd4DuBT6pRLjK8nAwnbhR3bivu0BSgo_bU5BU_nL_Y8O-Lmarg92ybFkwG2eKlW70zg2SFKYbspqVrFcSTje7FpiY05vVh-rICgjOIyb6u2i6WEFZNhqo5G1H7TKmBTYX9ZdrVSiS6KIASqOhh0T421y0aeq773QJ6NQGgwt5g3fDNTGF9WF9iJX1adL8kLVPGkwmhUAzauoHsfzxk8EPeKqQ36YRHNLWUPdl6FQdmyuOyakOjUy-wJ5cHYIXONNGAuyQN_wi7TXmof91nYpq7nfa9owk4wkKomS5I8aeNKclJepU-YDr4Lziaf-MCKukEbxDxoeLA9LNSvwHuOuhRshRV9cZchdXgWsQtE7OphPSqOpY0lQWVy12kRh53W9CqtuzrP4DErKTD26oHCQ_AlHj7OPfq448ROzxvyXq7eOKeFvSi6zxskbJIYqTziXCmhdQ60B4Vp4Cv1bjz-dS7W_vvyztQTS5BL2QvqKRu7SOREHdEJE56Wtia8D10k5gW5gZsEC0ESndzOt9hXJuTAWq5ZDNNiA346uFzltnxYKTZ3TrzwA8NfBEpi355yTPXx7LpiC7_6KEm_r3VnHrAq2U7ia6U5dt65zmsVVaaspH45UIQMuvOfhh5WQGIYtka01xfR-JIZNPvfUpc-Pqnv0PeeZi_ZwOt8zgBc577p2wmF7La_l1EG51XStVI3KrqVQfu7QMgMfDg4rN0pNrITsN6EHMOBX-H7vadJh-GkSdNGF1XVSErORG1Vt0NEHe_uK9RVuDhz55g72qeLzKM8ryKTxWUjhUB5FJsurN34ghr_B0luWuchPSyXVyneZrZ1m6JtcKiolKAdENkNawtM67mNHGnKZBo_Bxcj0nEbd403VV3d6DbvgnkJ2YrtZEzltNIoK5MqSZmtnA8kZcqoMIPKx-_W7snYVbKQPzn9RPw8yB3DUl9j6si5YZjfxD8GXiIuj1E1GqX9VUDZYpEEy5_Fn0ZbF3zcMnP7HbUYHUr-g54smKMxe02nn2AdeNf_K_4Gd3VLZzAfodQit-OiT6CPSdyUedwlKpeyNiRsSfJRPqsjnNYdwiH3MzzaxHs0pigy2De214QTF7qs2zTP9-Qmv0SRBOaf9_z6A1hmITAKzI2FkEac7iExEMYIL812t5Vh3MWARb_wWapURp5wW5rkSRB9kuZkxYziTg5gyJtjWV_HL3FPnvTPf8NponODhHSoeg7_5LN7nz3-f_TZHz5D-SFJSg9-HiSlRz-XlDb-YrOArbFpwa0__ezPf5v_YsI9QU71NTEAwDcG6WP8DJUV4LM6Xe9TbuVENN1O0A-oZmRTWI9XF8sl3LM1VqQK5HWwRdJAdKX2Sl3cXMk4oEz7Pyco_4mVz39pmXIvFHFTUbH7KElMSZqL_sNN7-Q-AhETdxJoONz0Tu4j8jBxJ4Egw03v5D6KDVPrRKgFb7VO7sg9ODUnQh94q3VyR37BiTsJGAFvtU7uSBk4JUsv1H-3Wid35AacmhOh8rvpndyH62_iTgLmvpveyX2o_absiXD13fRO7kPmN3WWCJveTe_kPnR7U4evUObd9E7uw6k3cScB-d2N7-Qe7HhTcyIcdTe-k3uQ2E3tHeGau_Gd3IOMbupOpFfvpndyr2a-qYUibTA3v5V79MlM-gW-HeXmt3L3fpWJOwkqbW5-J5-wFEf8WJ8HuIV_cudEwZQfK6D_LfyTO2cFpvaOAPG38ArujNRP3YnA7rfwCu6My0-tVwGDb3Pu3BUtnvLZBJK9jbW_K2Y7vpM_w7DUqH8dFrAbQ8LV8ft_IGoyKj1T7X8oFBgTURy8OIsXbBhgswAQSgn9_kLbog14rcfX4QUHHTfAFA46boA9HHTcAJs47PsVEOOg4wbwxs6--gWHDbCMQw4bABeHHDZAKQ45bABJHPRpBX845LAB2HDIYQNk4aBPKzDCIYcNMIOD7lsBCA45bIAGHHLYIPQ_5LBBnH_Qp5Wg_qArWSL4gw4r4fpB362E5oc9-HwYfshhg5j7oOethNgH9aUknj7oSpbg-aDDSqR80CUlYfFBvQuJgX_xYf8cxNl__ezy7RVcfPVJLg6P5KoQPrMZz9eMJOFz0G9c3t-8TmskEcmLtusaXekqUhqOfqLA5CfGTP38M2bsI2ojo5OE2Nv4ZxywPyTyHxL5D4n8h0T-QyL_IZH_kMh_SOQ_JPIfEvkPifyHRP5DIv8hkf-QyP8_lsgfQQy6qJK6K5soiruyVZGO4WgsyVlAUhhqkfAR5eNi7m_xcVL8be4gjBB7wEFYfBGHkFja_fG15ctw97B8nSZdbJqqVZkCsx91RamyuCN25n7dbV93C-wZhCOWQI7z817Hj8smiUyB2j1dVlS6Vm0F993qPIMwoS40OIIJHIlt1Ca5TnURdWlclvC_LlWqIirYmzwffuCzBI7no6g8Sorv4vRxnDzO8n-NoscR-jEyAU1TRy3c_WfhtPz1F-v8YIZTwnR8Y5hJmjLNmybyvXwaYZ4iJAT9F1ZDa65mv-HwBxc1Ilb-FHcymtOd6EmctmD1MpTBFsZMDTcRKmR8QbQQF_1jNP-2n-nIxV0sCgUjnay-gH9nz8AMP5752U7sj7-F_Qc_901JTtnTklX4IGbuN6aIuEIQA_H5OclffRHG4uAlBj2w86D36POR5uUZthYSK7DjITq2N_aKVc17vj_U6zk63bCGK5I4YKzpmReQaXHRkHdqWRqORNDpCyvIaDmUnY7P0pyq5ZHQEbgHt_Q6yyPSoEHCVaXXmzE5wQ7tblrEUZJ3VVdJR3xd66Qo9aCf8hsklN4inT-R306uApVEEZw4VZM1nhWgM4VJ46gJWZf-DbujmHQJFgKcbJdml3XpSwwlAgKXPd3pv4YL_DvR2BF3iyVsUIHfwly6vVBkHVsSk43XCAy16m13IUffLGGIY_xhjZKdS-z4tMJfAasShaqE4pyx6pd3Oj23s2PBmsmDrRx_0VXYrcaDHRPx0fl1eJHzJfG-HUudkNvYQb7H_kY6ELwipp0CHOMV0bex7OdYtNmqDDtJSq8z6lSbjycJWpBlNanB94llCTQq7kwddjX-kYVQkHN0y3RhyHzlpovgjga7EbkT3q10hIcokLK7lCUs8WB0FEFuU07pVJWZ7posSxLp7U8rOD_KeiBkOdsLf09oBEVFnesk1ir1Dcp5nnSVqqO9gmn-tNYXi2VLncGOXoR7O702zM8__pPAM1TlUlbqDWZw0yMVm9Ux6i3ZO-vEOj1QS7vCknOzZ0j1JtqkrPh8HJB2n6z8TXmpuZExMudDxhsvuWdlxtwFkMmXezRhR1jGcieqZrE-pBsh_hdSqAt12I6nyIXBm43gYFXKv74yi8qOeaHtNCPhD3ESUajX4Uvc4Np9PKU026CitGqb2p9gQVpEGE0QlGFGTW9lEH7BiHZHGgKsXPPuavewskR6s9msB88aog4vekUvmqWV7oyw-1DFckoMGnStHjHT5YQIH6sx3RlMt8LJIjhGg1uZ8V74RGxztnjK7FMP2rPvA6XvMY-WjcWbyCcBrXpASmA5CEhf6s74ue3o7y2bhmWhcLx3IRny6YVhYCroeJ_gkG8a1aalbovM0xM0KC7YZGNNASIiZGYMiuWJ60dkZWchGQDPPj8Q72imGsQdDn-bli2tc1ObziRGuLgKVTRJnY74jTi23SxO3w7b16e1-SCGbrLCwHYXgxrlsSqratgfjy-PTSYS0oNVmzWO2RX9JLFfU7yqeROpOFUQ-vjR2iyGMKhq9vTKM3L0H-sLYqT7-T__yxKC2UCNfiJoV0jNNfoNu3dyBfYJPkLu3dZ5WZelKeLGM0u1aZN2OhRjBiNIDMkhNwUboCkzmLVwdlca9Z28fS1MDLH7PvL22c4_Qvtysvr61TffPf3Ny-ez2c8__Xivf2F6Zi9fffn0JQ358z_-Z_aRf37-6e_80Z_-LtI8NqW7-9HZ4nS1toYC__qxi__jf-1Hf7rvg-37dzZ78bs_vPrm-bOPLAOTlKpVKBhkPNF-0kWNLuLhDumNk6mzvjZ4FKTzyYbA0TIswcr-GpwMPijoM2uWPW1Quw9-eom_nlJ1NVUB8SV4gKILWcRdXZvQ-_sA0SUuQ3BEX3LUpj316uy36BzofVSsLjB4wy-rfSN0nc6COXfYmuEPIg08pGl8YxXsPsx-b5_dEV-D1_u7xfZz-v3nSGBpPCHuB9IbtyQTHv4Za9HZAdyPcYyne1Fopuo9E1GfPdd3LKPu0hOOt-mqJDVR3SQqlYAuz_OiDab-xQqeZUnnZ-CKenrmIesTbWV283xpC3KIbYnx7_fffQW7MbAslhnE8j-pITVUGDFZRvLeSk7TUkAXak705EhOjuLETyzDuQ-nvJ-zWMHaXbBEjiOF61k1EMldpzQE2rzJ6jbPmsIzoiiT6aYdKifOwP16OQIUfIJ48tRqdZV1Va2zxgidcZ00cafi4anllA59SsCxcw8TrXC8IOM7uFVvrbQTZS745oh2_WT1h_U2PLwxIt0iK87aOdvE_Ib5ZuZCt5KWg5cNjpCB_d87lnN2IJxUyZRUdFkkOtF10bUiNaE0CkkWekjunhzHsxc2rnbxpX0SoXSc5nVum6ZWSayMkOZ3VQbfDOWUjwYUwI7bXsRXnedMqpFKtFpZ0WcLi8mmYK4RbLlOHjWg3nf0mG_Xm6P-Qg8Yn6zOqZXsNYvNkGuX5V0tJaclkpnPHAfNfMYcNQ74sRTATgDufHnRjwVMFr2nySRGwrlIE8N_cMUw7CGf2stv-DG2aTtnnrVnKGdhNemcKM4AcJuiZYNVpeK41lqLP1KZvMzLZry4EojZ7eLyL-h2y8tkVRUnmcrBz_a7tyyKNotMuLzQUIfw0RRbKU8LMivz5sXAfDvfRZx4fii5gzuSv_ecrG9PfNeboSjdlthT6WjiIXwaC2Xg1pszx4MKVgsFqNfnuOLPHTHTEQrvalhxZyNyVgII3hN7_PgpvmUGOyHZYzpJVp-w4Zt9z-wgK92vl0gOjgSUvc9rYtmE343BwUAlkwLGOZVJMkVT2lAxSohVWdOpxEM6ZQkBfRON10iKNyDL-yik71yQvZ1cIFVRJbrUGRg8D2_FTWrSthnIUMll7T7RRvYqWVYCuSj0dLJDDepFMN8VhthT7KtY_dRWTRd33v9PY3AFTTrEKkgyxdPFWxOP9myD2py00yHA3bj4P6HgEIMopRHXWXk1IMu6xtaSGbZo5bWMGjxFTQb0ESnTRNaAFb_hlMOnh0tu-cTjoLlFLrUVlax4jThLBahON4aYLSd1FtsWXMooCeTHFYp0l6EIxg047i0SEyx0d8CK9POUDHoNdqEui0jpRjhMC5PlkRkG5fZe6MoWjwnhmACFmYq4VRqlRZJXJhNBZWOSKi_0kARxb5nthAhq08ZNYtIiFfG4oHw3xL6-ZUTLeXsIi1znpsFM7tHCtfy-TFEapHUHnM73qRukWd0sTsl5wyOZhgrYgnEZdsv1pQO87lgVyNiWA8HwPmggxP2It711QJh80ImoWoTrjkWABGwsLMoKI5oVFU7YdDDc2NMvXzoU647VfWo5D9Mijs6YDDcVXq0vtiNXdPD-7lPPZ0j8wiHYtLj4MeljzFh75xK9LRtirClh_VvPWr9i8to7l9yxkOkWK_4Z2fWE-1y7wubQ-yVDkQC3bj0zPmGmlHy2KC590eWRiCb3ziV5ZKO9Obf36uYmMMdIUXuPejt-X3OrKIM0t47s1RNzUtzZKNLTWAlM4xlwLUnuXevsEBkWVTcceaRuzCIfA6_KLkbkerdezn7dZFFOxpu8Rwke0Tw7fsY5X9q-ylABDj1mvKyVfA8kGS0d532K7-ynMQiFb9j97qQyhtlBn0jFDY-LlFX-XHJwqKZMhs9C4LwJ1Y6cip3elZWTahbnioSO2IHcmG7CD6i7oqyyLGka7R0_BdF2nmdmcB6Cuf1ypxrACyAz_-VEVBDXcVeVUV6LRrgyXVfFodLYU6lQYmTD4jq_6j2V95bLAfyZuDE22WqNsE0LBWeV1SqAeHY69eLPI4uJsKgJJfhOVuTBCdxzpC6Vi-OmsJI0r8CjTMo0FpC5VDqH-R161dkorFd7DvXp3KmK0hQHKmot5M6dipsyGkT17nFfPJv7XBrEYdt1A1GTtcK8awbCdBR3DAwuS9zgB2nDH9k4ngRwONQZlmT2rJW13Couj9nxdvhLI5yAB5Zgf0-Yb0NzG72jge6RE97azWsC-SEX8p7En8Qf_SgqH2tMjspbOGvFYPGUnkKslUG3s6r92kjarjImb8ZrI5l9FVia84GBmq4pqtK4yuKmzhqvEBDrtGqTOMhyfA3Ldrk0S5_g6wRZHWQmneUKiJv9MqXST3pfzy5Yb4jvb6Boba23k5w8OyNdJIh66Gwlw9kPjObJatdqWtTLuYwDfS5faqGtyjI-2IZejJNw653hdiuWue-dciadu5hGtrUdtPopCrQZmTfwyf7zc_9Qn7P39obT1WfrTZAc5qfwooVOGGBF6q94y6i2icafcMbhi52SYI9bk1YJ_EcwWBRri5KiHiCkLNg8lwIW5yXtnuL4VjeqQy8yPEZg3ls-_BmCm4eqAYyYiTeEcIZXxhufUr2UTWDNCYy4oLQBS-FA_EvLjMJjOPbXq9PevWm-d5uzp5NRm-Clwxpxu3nw1r0DTBoA1GzKl_pV77E-hhHn9v5dPYyH61A_aAq3hYg5Sk2RVXCMehHCWsHGjorxJk5H0NqtTXzdpFlbVlXbCbJm6iRT8L8xshbATnNZjhZvoxchJdBWO2kfYiS6ECwHxNN8xD-1ehD45ZdeIgUuHugyC7pFUBuPHARbpC4ZwGKORt7lJLw_K7l3gfQGTiedSQjytfiODatfYgLOPTxKdxz__ON_T-gj1KVRdRYXee4hkS7qCpMVyfhlZrNvFv07MpU-NrmJH5RpOJJVmjVNmQj4nhZREyV75IZcWjHMbVCdhZyqc3umzu3xyoEX1bLCXHkbMAGFgUPSVQUcCk3t15XKyzYfnERfuLiOnCfSsJoOxKgmw1o9pakeTr5ho_jJ2oiyVFGm4aZKKa-MSqOrpBsIfLpF431mbVyUxXYVToojf44xKIGOoo857cxSTevC691LilFaONgdPZ59fbF14ejAWSPYlsPtvSGru60wMFa-Zo2qd9fLCXtTqzpP4UxXtehhZVVaRZkZJt_yY8nb-voyHo3BIM7HnsFBB880nS_SpcKy8CjPE7FxbVt1ITRsRYIJjoZz5LTfC1xRcSdh5ZxPW7Ukdg4GkOvrTlb7qvu89OobCcBekw16w2ePrbNbzaQC2BZ8YbHOd04CBia8x4P3yhXMKRrdLl86BzFrOjH_aVIY0xRtUaU6RCujqCv2Vij6EqklSvteURnfVPI_0mXbZkXcxf764MC1SVYloYn__u0aj7ALOr0bMJHvCJJesZ_-faA8wYqR8KDrczCBw9-HpcFkOud2YuaDUsKZzUvJ1ziwpGiUahusi7Y03dbis1iaPRV1wgy2WdLWZWQk39lW9SAH-R3rZnFosnWWLJTQwhJxvypYUn4-e4O2hv-IxzkCoF4s0JeC21pL9X69aHvXPtV7XWQ4OC5WvFMoK0ylHlg8unUS4PbNolbrVKlsAwdsUiWZEUmkuuyKLk4GZ8qsOJZ-geWiM81Vs_yI2k5icN2lMGk-jwLOQFEwn0VwXBUQXD7foWKYKBuri7SGwDxTmZbQpMzBGgc3_fw6QTpedhvUxcNy-kU_QKZ83nSJGTUrsswnlQ3VvQH-geBHdgld5nSsg3KJotxjMRQw-Ccrrlun_DAW7zk0elhhyRG_O0EYhneHqLPaJ6vQbE_lMrq0TPJcR0FOpYYgvK3jwFKO5PzQpcYONXNOnCWMYW_OfF8hFuHaHBKFJe7QwqXtZDInDoyiqSrVgotY-JKWKu7g7YZpCV4kCTdMYin0jZYJZovqODZlXfsopDR5HudhwwofDCtbwuK8sZ6Mz_vFqKqgf8fyaOAzwptnP9X-8mQVhHlcfjAsVmUwYMrPqdOqgli9rkuR5mp1mbVxN0jRODnmm9YshP4PZ16e0v3tRBnKxxmETKxQ9hVTfmpzJXAD51T-RD14fHn6thUcZIls8iUcYv6eZeNy5DLZFclWEOhxmDelWhbB9q4hlFGNL7kpsrzJlAmWiU2PS17P5sZ9MQhsXlg5-DS2Vs6i6OJKeTVK66Rrw9g1_O7Ka11J2f6OBzGx1DNVFrU2eVfEPgOXo_1NhoVJuNRHbDcT8qAFej4VVuI0IpaLjWOh_Q6F-qgeeKpKXncmadKiU13rz76AlEekwYKV5QqdvCMlwn9S5zYuo3PbB7HjAFe1_Xgzu_FW6Mq7lJWVeuWY7u7t32h3wbBverK2jLfbIBP2_PqiZyxd0kz-zhmAsgi9V012OsBTioZDRINt-O4tTqnjQQSUFVi0K5ayqZOIoTPvkmCrN1rlBflCtvYd8WGzUVSObNGzc9VPrta26yJVJVHcSeV3XTZll0Xj1ZrNvvRts5OrNS2SooIQtswTHzLpLIdnqgalFVY0_sprXg_ywXatHIEtMezkWbxidzfOnp6spKV3atHXaVpWpSrSQuRA81pHZShVyqUtVETqV5jbAoMzmNbDTqsuqwaGaEcog_fsej1Jv60c-BGuaPkebvLzm61g7LEAU62mVlyRZXGhc52VmajXGYjkkq4cL4Fr6LQmwKJYJWlVNpmRhEusMxWbEGi4TieUoEww5GBDvONGkNKCQyong-yTrVNSiAn4GnHcFKbpRBDck4b5V_9cJEhdRmDuT1CPLwYwlAWg9icXfW7MCcEPAc_xgWQFDe_MMrG6sP1ziM74xUDlpngRm5SXVb0yW1fJCDe0vmQPD29cQtxhIpAUW_GrA9jLgaynG3X-lm7n7vwUtoaaYCRsc6NUcxC6g2_O1bO2Lc1l0ZwrThqRdu-5vCDcAWyWqcKztIxTU2ZxnXjPo-vqqq2LchgJYuROVU22j-4cYlcRSAdb9RefVwieHKK-dUsleYjB02no4BZf2eMq1x_PHj06_0iafAqVN3Wddm2jY6NFhDpr66walhaJXjDWofbjNNV0IjXSSidJ05WJHwQ5DVvmrQqbmKQbFFObXDXKwdCCK9Tc6YoVay6c5TbDtfsdhSfmB1gAtt6OnIrLt1eT0F2btzqrOjBsEkDqqEiypqtGkYGnx5B-KiqiCV1Yll8eacb6Kospj7_BqsZCNZ32ZzpYwAqs7MjVUttdJNMTiFysfN1hmJX8_u0CbpSh1tmloei0RfDEeljzmeNBoEmjnzkgZTUYjrB4DpnXGhvbbRn1DXS2uzZui0znUSqPWBR1k9dNkBT4rQtcOCgG1xGswGLw1qcseJbrNkpT1UptW6ObIopDHgRGpc5Uy24Xz9Toea3Fc8jVQNz2-7dX4YdwgZ5xAYtAT3TLYI3J5GOfPlgsCFc7iJE1FeC6aHHOdVzcpDtO0-_YoDprYKnAwRv554uSuC60GrhNVlrcxVwOpxBkarlevwM7-m7qOKyTOi2yOta1dMnVLUTNXVjq77vDaKTHwRJ8jTbjtasBP1ldwtqVApmdmBWu4PRYH7uimJMVK5jCT9U2-Klbe_RTV16DI4RfnWynyqqyaBPdJLkSfDQp4iTNwpnEQ322WS_ZUXJVONhjiVycUzF8VJRxnTamThO_3Lu4Vaoo9vXWhSqyaPi9Bm0wLSerQIP2I8_XQMwGTlsMvoxY37hqsWU_QMYQpyHPheBRFjS2FcqjcoTJfuq0AiOawulYGO_OV0VT13XR7nnYfnGKpTEfwgTca_ca4cdv1QaTYOGPBsq28PebvWVYuUZDoFJW0q2S6yKNdBM2evL9vOGY01o1LoV2PWZEVkWuCyxY_DgBYoNzHn1Nl5IltF4RnMhZ87AXeI1O45aZlcJJdjWhzVRCXeeJjvIoq_JKfNSkLeLOjISk-aGOMDolM8O9QZcrZ3II5dpcrFbeO0KbICV0Qz9UY6kb437wXG_8mnwzFTnquq5SZO9M_b1mbZGgLPXAzaiOJ4pWpCzuYx5HFGnTtUXX6EgO864pwIKNClWq4zgYcfKicd7BYjFdkktQ0MCE50lW78EOR7WX_hyhCAAX2CUKo8NTMTymAvYZi9i78g7rI643i1OSBGf0jKv8OQc_o-5javtlb5KuhIaQfEJ0ftm1vHyL7x4s1nv3rv1Vba2C09y-_mWCg5KnqkqU6mqJ2AuV5aYbT24y-zZ4hdNAQGzKTtUm0dLjlSRxpbsq3snZYW3_8sKCyuz6MBBuj5C5JOCC7izbisQ0DpcuK2IXWUuMMrav3H3B9YcqGzHgHuCiDyqP6QNQi_z0Qf3ZRNu5Scqi7Kosbn2kC_a5qcAoj6dwyB49seZVnsa61WlU-kM6TaKkM1m1M3-9obj4ve_qIavv2ufPR7n8eWD_PPnblWsZJIjYkZFxjpZ3KnqPsh778zXHX75A29cYoak5WRFWwSfOcnGGQYaL4yfOm6YujalMlbWRx6QCGm7v573yTA8U3MIBvlz68oTBPsCv2C48eAC3Tdw04Zdx-yAOcyZxJAXJVIJENpJrxmyJLrUlriWzDV6Dj5DPVA-nPRY9ozHtTYNz7FgPIYqhiJEuaUNtiLuPDKbcz698CsglAFHKHcuZ3mJ5s-wQLrN4-vULKV35hDSMHixrIB5OIV4qxcKXZd3UVTmofEDjRTNKVuxXPSewKdEp5eg-Ozq3VX0EYVBzGlbZrl1dnIc4XAGXAAEeG1C-kxtRvw2BGWpQ2oZ8OowBzAMAIGRvsPgoWgZXjH_9kuxq3ZZZDN54Jr3AbRqXWTeooJ3VBEoJpdh0SUOG1XIxhDWFND8lmWmZ6Nj32H-72FoY4cPsN_v66YkHaxXwyCSwthDP6WXfv4-xf513N_x-6ADw5t7N2vCVR7yai97lXshZsw1RGOTgErNfkV61jzWb4vWCnJpv7fJXnmr7csNx_yHBGDwycUriof3i2XO4lMulUVXsE0qXD49zy72GvRSO4iW8NFNS4tR4JIoR2g_E8OUe0pxp3mlPrEURNhpJI8z8-3KXYnAveFnU_T5Ttv2eR_JQkOdKsF0PZMtGeNGTGbVijJFC3Ey4uzxRAT-i1F-4FOPN6ELxFdEtKAtUWqCA-fXU5l2IWfDb2RlRZvZjtKAfZr9ViyVXdn9u674Hddj8DnlO1Nk56XK4AW3aHX69xFrDGUd-y36GATsNfwkfcYUqmMFXvtjf3QAlIWD2GcJiWh4G-tXG8Zb9wPfOrSNYIECgEVwQYx7rNfq3sTv9Qm0kDWI0tVTq9sHS4w0Sq9hgYSvgfbsNFZwFJ9SQM2MHYOY0VU-rVdwIdxZ9mL3YJex74hFtapHzp6Za9mtfurDYDjaRS_Og7xUwsCKPHmZMhIHVpqqJlMNnT2w3Mm2rIGlim9bGu2uQFqFhmEbMNYnZrUvt13h22AyanFc-p9A-oZImcolo8RCWOUXgEbWN6lRu2lrolJIGQoq2i4Z0StHx7LlLbCDT2Xp1dLqGKZw8Noq864wxyhidSSajrXRUDXCwp7bG7o8vhkRvYaOlS2kOSYwsFuyqlbgBijOnZnPk2ECwoolKk4kVE5F5pNhimIH7-XAkR5_Ap014AmMQ7kgz_WA8zCsh2IRTYt1IOviboftCla97OwW5nns4uFvbmFuCFQYBjCD3cDPD7nnereDivjMrtxd4DuBT6pRLba8nCxi2UTIbg_u0hRgoibQ5BU_nL_Y8O-K2Ubg92y7EkwG2eKlW70zg2SHOYHvzqGrDcYnie7GJhY05vViqjzh5ZRSXeVu1XSylnMiLrupoRP01LVIzFbiXZVcrleiiCIKYqoNB99Qau5zeuep7D8XZGIIGc4t5wzfzeKrqLe6qqErSLJJKdRHgkUqbUS3UuJLsfTzn8F_cK2597ofFJLYHlVhsLOYbNIBx1bstzLkrVTmxG_BnYaO5bl5yjlwBzn34x6l2ntc9Vczbah_64i6T4PA8YDeEmIDD2kgcSxtLFsg0htgwqvoxVeB92MqRJ9wd_eyL0Eg-cUF9zHdmIN9xKp5YOkbC4anHaOwqkDNxRJY2PDVsjXAfugrcP38Dd4Ebpr8K2FZ8uDN05rfeHI4qwwY8TtwlzUs_rByaO2dW2CjhLwKKsI9L2ZL6eHZd6t6vAEoY72vlmAfsI7azdJhRt13Ld2VrH_gHtv_4W-pexnv1ncveZ-olM3Wd9xQAvdwJ28FZbaj2GdyVIQOkw5lsU_Fdmd4to2Vwxvke3MVkY19cVmna6KKqGknwmKit6naIz-LdfYVc2Bdnzqa6Y2a68DfK8yoyWVw2UtqRR7Hp2myYAh6lTGmthVSGXDCjeKnbdlqK_OBwp8R0OyBdGmaqTet5OByxwWRSOIfjLtJxG3eNhzq7utFt3gXzEjJr2smYypCkUVYmeNDU3uFTypRRYcpBgnftnoyPbQsgkwNKJKWDTCQs1jUmIpxLgNky_GPgseDyGNUXURJZBaQMNqq1XC_8abQ3wcctk6vfE4sd42w_6IktOTKw13Sc19aZdD2ZcvZxp610a_JRQm1LO-7iBFdMEjdlHneJyqVQqdGlSvJRdqQj1M8dRiFPKTzaxHs0pigy2De2_p9hcF3WbZrnezJdXyKxNXMGe07kAUSwkJAe5sbCGSMW35C8A43FS7PdLS8fV5ZjISZ8lqpHkdPWFrp4wi4P-Z-smP3WUTgPeTUsQ-H4Je7Juv35b_Dv_wesS96c)
