[//]: # (ob:be94d633)
# Privacy Boundaries for Portable Artifacts

[//]: # (ob:9db57e7e)
> Status: V1 product-boundary decision draft
>
> Date: 2026-07-22
>
> Scope: artifact policy, ledger admission, capsule visibility, stopping
> portability, manual drift, correction/redaction, and minimal edge cases.
>
> Out of scope: fine-grained ACLs, online key services, multiple-audience
> publication streams, legal-retention policy, and real-time collaboration.

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

[//]: # (ob:7930d482)
   switch for each share.

[//]: # (ob:569487e1)
2. **Record selectively**: record accepted versions and consequential

[//]: # (ob:0b0c3d09)
   decisions, not the complete conversation.

[//]: # (ob:a0426f1c)
3. **Raw holder can inspect**: anyone holding the raw artifact may be able to

[//]: # (ob:2130f482)
   read its capsule; hidden does not mean confidential.

[//]: # (ob:67fa619e)
4. **Stop prospectively**: disabling portability affects the current and future

[//]: # (ob:1e299506)
   copies only; it cannot recall old copies.

[//]: # (ob:9b23becd)
5. **Never hide gaps**: show uncaptured or unattributable changes as drift or

[//]: # (ob:592b5a4a)
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

[//]: # (ob:663d5dbb)
   agreement.

[//]: # (ob:af2b57ac)
Record a concise rejected rationale, not a transcript of the discussion.

[//]: # (ob:886e450e)
> **Record the decision, not the conversation.**

[//]: # (ob:ee2856b9)
## 3. Core invariants

[//]: # (ob:e2605fb1)
1. **Sticky portable**: later admitted versions of a portable artifact update

[//]: # (ob:68785757)
   the capsule by default.

[//]: # (ob:5f65a982)
2. **No per-share ceremony**: an ordinary file handoff does not trigger a new

[//]: # (ob:aeac0b2a)
   permission workflow.

[//]: # (ob:99d90af1)
3. **One raw artifact, one holder boundary**: anyone who can read the raw file

[//]: # (ob:ba409295)
   is assumed able to read the capsule.

[//]: # (ob:4128f9b6)
4. **Hidden is not confidential**: being invisible when rendered is not

[//]: # (ob:a10cea77)
   encryption or an ACL.

[//]: # (ob:ce32419f)
5. **Selective admission**: raw conversation, scratch material, and private

[//]: # (ob:5e7353ab)
   context stay out of the ledger by default.

[//]: # (ob:45537439)
6. **No silent rewrite**: errors in admitted events are expressed through later

[//]: # (ob:a4fc38af)
   events.

[//]: # (ob:8e179c0a)
7. **No offline recall**: a distributed plaintext copy cannot be remotely

[//]: # (ob:4528e96d)
   withdrawn.

[//]: # (ob:60865161)
8. **Deleted body is not deleted history**: once an old version enters a

[//]: # (ob:2ca9c474)
   capsule, deleting it from the current body does not guarantee its removal
   from history.

[//]: # (ob:ef452471)
9. **Unknown stays unknown**: do not invent an actor, time, or reason that

[//]: # (ob:75f89d69)
   cannot be established.

[//]: # (ob:1d83fa80)
10. **Gaps stay visible**: body/capsule mismatches, missing events, and stripped

[//]: # (ob:dd1b102a)
    metadata must cause an explicit downgrade.

[//]: # (ob:012c1d7c)
11. **Private interval stays private**: re-enabling portability must not

[//]: # (ob:38973198)
    automatically export intermediate events or payloads from a local-only
    interval.

[//]: # (ob:115d0026)
12. **Precise trust labels**: computed, verified, attested, self-asserted,

[//]: # (ob:5d7c23b8)
    unknown, and redacted must remain distinguishable.

[//]: # (ob:863dc7c7)
13. **Portable merge unions only disclosure**: a multiplayer merge may unite

[//]: # (ob:9d7834e0)
    only records already disclosed by its input capsules; it must not read or

[//]: # (ob:58a799c4)
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

[//]: # (ob:28d8f9a5)
  capsule is removed on the next materialization.

[//]: # (ob:8aba5387)
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

[//]: # (ob:aac2dc55)
  interval do not automatically enter the capsule.

[//]: # (ob:021e0444)
- The current body may become a new safe checkpoint.
- Continuing an old portable head may express only the net change allowed for

[//]: # (ob:c2f79407)
  disclosure; it must not leak the intermediate private graph.

[//]: # (ob:9b3548d4)
- If safe continuation is impossible, begin a new portable lineage or derived

[//]: # (ob:44391d33)
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

[//]: # (ob:a7a37a1c)
  low-entropy content such as names, short conclusions, or API keys.

[//]: # (ob:28c50da3)
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
| A recipient changes the capsule | Fail chain/digest verification and mark it tampered |
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

[//]: # (ob:ce1a43f4)
   without another permission prompt.

[//]: # (ob:563c5b97)
2. A casual branch creates no event; a consequential rejection creates one

[//]: # (ob:7dea6ce8)
   concise event.

[//]: # (ob:a7ea7b03)
3. The capsule contains no raw transcript, tool trace, local path, or secret.
4. A raw holder can inspect the capsule; the product does not describe hidden

[//]: # (ob:42520131)
   data as confidential.

[//]: # (ob:882faf6c)
5. Changing the body without updating the capsule makes `verify` report a body

[//]: # (ob:0af074e5)
   mismatch.

[//]: # (ob:899007c7)
6. Changing the capsule makes `verify` report tampering.
7. Manual drift is not automatically attributed to the current user or agent.
8. After `make local`, future versions are no longer embedded.
9. Re-enabling portability does not leak local-only event IDs, payloads, or

[//]: # (ob:069e47f0)
   omitted counts.

[//]: # (ob:2ecc39be)
10. A clean copy carries no capsule and does not modify the source ledger.
11. Stripping metadata downgrades the file to an ordinary artifact rather than

[//]: # (ob:251abad4)
    falsely claiming provenance remains.

[//]: # (ob:c0e2865d)
12. Correction or redaction does not claim to modify or recall old distributed

[//]: # (ob:282e8d73)
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzYxOGFhNGZkODJjZDY5ZDA4NDE3MjE3OCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjlmNDFhMTRkIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV82ODZjYTEyYWIxNTY5Mjg1ZjI1Y2RkN2QiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzMyZjFlYzhkYTRhYTUzMGY2N2E0MWZmYyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrVvXlzXNW1N_xVTvn-cat4JPnMg6jKWw5wE1dBoCBDPRVR9j7n7CP1datbT59uCyWkygY8AJ4AYwKYKQzmknhIIAQsG38XrlrDX_crPGvtuQcdSd1t-n1yfROp1WfvfdZee83rt_94iLTatYJk7WO1_ND8oZWVY6ETE-IXeexmeZjkduw7ketE8aGZQ2kzXzuW1xZp2YbvlkvEDcL5KHGTNA4T6juO47s0SEM7TPy4cP00yGLPCf0wzDw_C2I3SgKbFLETF46XZXHsu7YD4-a1MmuepK21Q_N_xF_ax9pkEWZo0Bfa8Oc6SWkdfv0tbdWKGknr1GrRk7Wy1mxYS_DtZmvNStesZ1rNZrHSomUJz6yQ7ARZpPhKPR-3mv9J4WU7LRxwqd1eKecPH16stZc66VzWXD6cLdHGcq2x2CaNxdizD_c83aL_p1ODn491Sto6ljUbJW0AJdqtDv3TzKElSpCESeE7xPHzQ_yTY_Qk-xKQlh4L4zAjjktSJwgTNw4KN8jyPMLvrjRbbXy1Y_Vag8LK5X7Uj3lu4dAszolPSODZRRgR3ymKjL-OWN2xjKyUnTq8sIvrzJqtvDw0__s_HhLT__EQ7HGzVeJP_M80P5YCwX9_KGvm9IVDz8MbSF6AifNmVh5-5tmjvz3y2P8-duRXjx97_Ohzjz359HO_efaJuWVc70H4hrTbrVraacOGHUtJWSuR9qTVwHXD34CdKBuy015qtnCFJ2oNHLVcg78sw18aZBm3kq905lAJD8JYh-YbnXod1p0twW5R_r5pvZmdgO-mNPHz0PPg67BRbeSk-UPPtGonSbZm_bzZaeSkVaOlVTRb1jOC9tYRSYAZuQSS52xtK8hxdBU--Tdrv6Mgy7TXVnDlyAnAVYf-NKNXmORpENGITnyFP7O2Xvt289Tp_7n33m8da-Puje5bp7d_-H7r7Qvds19v37q19eWDhcbP4J-1-c7nm9c_gu-5thvO2tGs64q_bF94ufv-N_AXuc_WSrNey9b--9TpOptOvNgKaZGet_LizLWjJOx5q631t7Zv3e2eOb_9yYVK2v6b1ffVCvoFgVvEJLFHmkkLC2vrvVd23ruydeP05pefdD98feO7i_DmW-tvWz-eug4yrkV_PPWB1V2_u_XX1__71EtbV7_cPP-vrfUbW-s3d069t_3gnPVcHYQNEGbnpVsb69_CD4_DJlJr8_y17plvN9avdf_1effMv7qX39g5dbqCcpFvR4VrJyO9D2x09_JXO9dPbX9xeuPu1c0PPtm-8Ur3_LuwgxVTUjwkfkJGmtKZsx555HGa1YFElhRfVrOR0UcegWnVJ5t_vm0pLgJiW2W7lp1Yg0f0yuogxntWliV5GGd-MdLKfgYLOwLytpHPNht1UA50sdYoLdK2SL5cY7JjzjratvImHK9Gs20tU9KwQIK2O60KaoUkzNzE66UWUGHz5qdbn9yCN-s-eHnz3bucjfZg84rHqljeDhwSxfHYK9h85wb_EvBv9-4XguFXOimccYJy2tr88BXg-Wr2yUHlF1Gcjb2c48eP49MLDRiY1K3_bHZaDfjfH8--abETaImvsk_QWqg3yw77mKnzmsFJqCN6F-llXpHa4diLhCO2c-4cnH-rTyZWEykKqWPbkTc5IlkD_1kmJ6jFaLfQeObpZ3995OdPPmFZP149tZ9_FbRzCztLQbGPvfbtB-9u3H2fq6Xu-x9u3bwKwrV76Wz38j-617_svvXVzrkLIGb_596F7VMXQAKDzIAvbN85vXXpDnxh8_qrmx-8vPPuFfadKmqHTpEkNBif2i-CzsXNtV60nqT5Im1ZIHQ2vrsLv29eOwdyXv660HhxdnZW_T_8ah2vLTaaLZofhy_jy1x8W6-YycTeQ50EQRDm4y-5e-vV7U_PGHYwTt69e3X73Ffd177cfO21zVdPASWtp0jrRN5cbaCGAmEM5z2zfvnrp57UfL196wd8NxDhFaQm1E_Bes171u3OSXIpUWul3JZZ20Mk7vFohVi0EzdzCuJMZCW_a7bgb4sWOjugU29vrH_evXCme-WvVpm1SDtbAibd-P4j_pedv5wFdbRx95JV53Ph8sBK6H7_7c4HH3J6d8--2z3zOWcatAnO3eVMbZW0irppnAd2mPa9E8ig9T9v3_ps-8H7MKiYtZqwSNndHqsgahH7tCBpPu4CZi1hMn1yCx7bePDB1tvvAhk21te7r33SvXVh8_wVoFP3_l_gB7QOFBOCQ4ib9j_33l9ozFob65csIBI4M1b3_J3Na3fk35lJUWFJRDENoiDK-t7DFe8BR-SAtKx4sopHozDMfZtOYBmzVousou5bXmnjGb-EVHz7G0u4RVa7RRrAq7WVtqAd-Ee1xmyzmAX_qrO41AYTFczd7u2zm5e-rKCcF0VO5mR235I96zH0fP9PB_aiBlq6RbkObsDGfLZ58dbeFNzHCBWUdDKPenmWT3BZYDrjQb1yYfOdbzfXP9n-9uuN717vnn8HzGg4tCiCr3wBvtPmq0yc3rrTvf92tRrynJw4tM9UHG-NoBFQi3731ea177tX3tj-y1-Bbbauf7R96uXtd98AO45tNki97i1w3T7e-O4UfJdLqe1Pvtz-4Qd4ja0rZ7eu_h0e3bz6Q_fey-wJD564cgkcmu1TZ3bOXdy8fAUG2Lj33uY_v9r-5nvwXTbuX4fzuvXxN90PLnf_9Q8YCU5q98zft2-fBUlXwT-kcMHDJdkEicBpD28CBgK8Yffy51v_-GHrpXsoA_g4NIfTgaOROkVJzWyJ7VtfguOwc-pK9-Y74P32LHtg7-I4pH4wcFLHWTY6JM-yqIvVXqJWTjMWvZphzgd-AhOhOGMLn3vkkUqXzY2DMO31EmEPNz_-DuwEVPiX_7xz7vIeunboAxVnjrqhHRSpM8aszF18Trp-3DfsdRTZOQNOvMk0dhu3Usp4LiQ33_8GBX9GKpguiEmUJJk_xkrRogZG7575W_feKViUPPDITN0f3tm-vd69fA01-WcXu-e_7V5-CUQwHJ7N63_rXr8DfFGATL6JHLmCwZw2tWqwjtZJUq_mOwJmTBD4vXznz1mP8cgeI8_l29s3Tm-euoFC_-yZ7q3v99jnfTxeseuEFkXs-PHEViQfxJCAiHPyiACtF7M4Begp2HXFES2KdiwcOHYw-A5U-aMRSQMgYt96HbVgzkamUbeXstrz6aoAH9hPThbZE1rOrDaNjj4OKlwF5MASaDezZl2dlu6bF6ys02LGEi5MmgHwUcXJcfMipjTI-pbrWd3P3tu4e1fvyjJtLdK9Cbf7g1XKPfXi3HXC8RcB2hw0RE_kCaxy8NpA2K4oy_7KK-gdsZOOp_vKBWRHEUsHwX528-ptNOevnIdnwTgAFgQPWztYO19d2L5dFdRL7SS03TCZwPu8__Hmzc9gAVrg_OMTdIwvX9m4-xmKqYuvMt12mgUCeOSLB_0PtygpQXnB31D3f3dm593PDPm00BACquI9_IQQGtv9--L28TKXkPs9Wns8XaWPEtcn8P8TWg63qLXdDIQSNjW3spmn3G7CEYPvZFScJ0G-w4reFYersAuwKkJ3kA_Ofwy7wUUnRqI_vbTz7n_t63Dt8mClS-eFdmZPYBEqHyHzb6gHXr7PKb35zg1wOWh2YqUJjAW0zGm9TRgN4SeKep2tqMSTJbi6ypgmQZQHQwXTQZf9MxaxhiWgg48DWQXsL7fAhLxkbr8KDMP2nwT93bZqZcUCAzuiaewW4y-w-8VLmx9eB7m1eeuf_DERwrn9OZxcxqVKoC016zltWVvXwVO5g3Lhzt_Fl2_9F98IMOTxmEu1IBxMLnKqznrsxbZPex2sAEyod2_tnHrPWiKNvFkUyrgWIVoe3Nu8fncPk-RAA1Uws5_keVz0eaeTWSUPWGy-9poWz4rqm69fAzrynA9L8bC0Dk_9cAXRF387_353_a51nEet93A7bJASD-F9eleE5_Ty7Z0PPt766POd029Vnz0n9nPXj92HsKpZC-O71z_COOdL33fPrW_cPcupKeSrCJn9-TZ436i3Xn0LtLT829Vv4W-gQfmfNx580L35ZxTbzCaHfdm-_zcYTH77oyvoODMDvfvqbfiBPwZW_tb65a0v1mHg7Vs_dD87t4dHm-Zx0h8Tmww1uCDsXry8fesWbtKtH7bu35JsU7Jk_XF4v-NoDePPTJyu0NYs6eQ12sioVbZBzS_z6CSMsHH_AeYqKvY2iYqwcNzevQ3ndLK5XitotpbV9zD2rN2eqTi9oL7DMHRp39yO9USDDSMP3l6acPgjVRPnUWD7qTvOxFt_-xuK6L99YtGGTHHyDzb_fInH7JXAmK3Tk7Ru7Zx6dfP1_8L88dfrW-sfMZH-DXwbTt_m9a82P_hc-7xcpVbtGzgWeeLY47yC-Cr425vvfLxz_RQmWW5fhkOy9ep5PB7nr8Gv8EL8QIJg2zl3Ec4WD-LuET9xisTx-2IFIdpm8Fut0TnI5g5_qGJ7IxoEThDR8Sbv3n_LAt8UY80sQM0VwvYXpzf__hKPYMMWbzy4tXn1ezhvGB3jGoPvPqMRDNF99eLW-lugz5leqJKyWZ5Gfu4U460aI4S3Ptm69Y4MlGO2tMeu4b72MmlgykdUzciw4ealz0GoCo-hQgaGfpD5hI65vY-RskPqLJfbKaXTCicB5DxPsiKBv_sGKMelJwq0e--xuOZd4Mmtqx9hBmVQPXff-LL7_jdgCvGkF6jqKrstzkjm9mWwQrDbnlL51L1ZtO_bVaInw7KoAXm73-mO6yzvcWv7ky-3PtsjPV94AWhuJxhxvlmL8zAPAWsSo1Fz9uLmlbvd777QOyB8Zn4cNtYvbXz3upCRy-AjtWqkXvsDryyo4K04S1zbz-IRV8zi40zxtih8ta50IXy0-dr3YIpjucOl9Wr5FSZRFhV-v3j1rcfqrEykubK2N1f0fbuCK1I_8IM4zkecjkseHs1gObKBIwFnBXNs73ys4hoYP2cWC7eFgBx6rmqWioMktaMwG3Gxs1ikJHwTzls8fHjzU7D1ZKIP2OvTO1s37nAO0374SVC2DeV8o0BgAnjz7hXDOgejiNeQVDnjHgXvxi2ivrcIrGfpLD2o_bHLU5UxLp841HbHnB6TNdfugOXavXIbzdk7bwApwUTUNggLaNTw0MEWY4XYgzM7n6yDAtu-fXoPs99PMydynDGXOGsZsSgZBWdaiJWlWkcfx5gUNzngB6574IfVpTUWxGwKkyirKhUriiTOk3Dc3eye-dcGqP2MazEuqsCubuL2Wahsassrdbosg9FWuUIzDPR3z4JB9xaKmvtneUgoW6sKZoCiT_y4NyAYzVngyoCg3bp3bfuHNzCWfv9NUHZ72N0Vj1WwXxiFTu4kxdgrYGV2Vt7MOkgVkC4NK6dtmmFKi7QxarJKSmFm5KzgDr6CUZUTjWZlyDR0_ayIx14fD6ZwywceUOIPicLEzIXvd85c7PXYuSCF89O99d4eUSmHxiBIgrGXKfUsl4LcuAFXGI0hlnjqXv5z98I1Ifa6b321cfd9ET-z2GDWYVB3yyAe8adl4NeiJn48WWXGhUkW9OfJRqLyrZd5UGFj_Uz33E3utO8ntJClWWg7fRXaoxFw-85pbqhLm5yrCPZL99aHO--e4WRFP-adb3r_fOkjGL7nIx4bAJ8MbcgrFzbuvt69fHHni_Moqridf_1vGHnA4M8XPM_OvYXq4IHtOkmYknx8irNQweanpzb_-TosDsgN7uTW39c37t2rpniSg3NU9NUUjbICVYrIxPi81WmongKa19rHuBig-UJjFSTBPAjV5ZUOCnLmfFQUHMZu6LiePz6NjqAqsVrNOi2t7XNfg3LsXrjbPX92D4vZyQkJQ29yBMKWEdbfcCxdW2iAFZN3MvELUkr8aHRkLDTg2QoKhU6c52E8vnTk7j7395hKNro0LNalgWGNPczBMEuSJMwnR6-ytogZ4BdB9Z6stZoN1CyqRwQ-7m8bgY_KCmo5bh46BR1_Q4U7_-46lp8wIYCWFpN1VnO1QVtoem4_uIL5xaVm8wSnKAsh7IBoZAKSu6RbN19lQuWSdVxxwPFqj8TPQzdNo16bIZ4Djxt8-4zbd6fLzgptyRIwVHctmhP2xz2siAMNVOXIFFnopEnWt0rHGH0va3rg2xXTgeMeBq6fjDgdExD_zUNb73yDfgM3VOBAZM0ORn7Ovrtz9V0e0iesmQDEmBzZ2rxwrnvlDVAe3JKF_RNlkTfOVpk2fkj8gBZ9a3at5wya702kge9XBR1cJ06L2Bl5St50gQFBbp9cuQSaERXn5T9z4vAMh1mR2f3-W3DhwA-xBC_lFHN9m-_c4Kb-xjp65Lz8G7XrrQ-5-SwiC-C_i6hVlZdOsywGQdj3Xh5Y_ftie6Rj75criOi5tltQf8TJNt--vPnKR9YKWas3wfLEGjozE2dkUTlBRUBYVSHwGr4H97uvfazPYlVgP8qyPA5JNtpyZ2EZN3hkgGd1YbuEz37pI-2nb91Y33n3M_1WVy7B0nde_hKUrCjsv_wVPIyxSFYvd5J1b2aikocNUWEs-VGUZEkcjfYK3PLffvChMI9u_pk1Efxt--5flTTefO2vO9f_gfx769XumS95gB54T4RLrt1hwVLSAP_5DzQ_nFNs6spl2RI-9_233NXmFjDGmIBu7NUr9sbOPSfyi163IZmzwD3Hwl_YdTiTe0jsIV-vquJyfZpnNhl5xhetzZfPdM_-E3TtkKYHbHg46SheRsKwWm4UpHSFFfG58CT8F9d_FqlqhnAzEOl50Rt8c2y2Wk5tFBKn39urvWroE1UxGT-PUzv2xpkXDg7LmXCzgGdO0GhAPmKJwN8cFYxvtDDxrB0r47ZUKo91PGNkvsqd8H2fJH3b6jhzcELqFLZU0B9DZhbaSnsx1R6PVkvHuIjzYiIrUYlE1tH4Rve7l4GE3ILn7ZZ7dDRmQRGl2WSoAo8BZ_fFkISkM7kbU2gsPYYJWdlrIiqHutfvbL7_TcU-JtTO4yTvtWMcTMhcP9W9c5nTYPPVB9u396qs2PWhKr4PbIcWuT_m7BgKMqIoGApi2Qr4XxWbzUgLVBzhpUGivBPdnip_LMnSPCjGpY0Q0Ox7ewR1CI3skEZjTjhr8dCNaABisQdgXVYvawRzRD-Wjm2jr4AP3LsLmmpj_T4alLdlOQQLinJb4C9_hY9BLIEs3sL-bfb3pVqeVwW9szQibn9n3IFfDb69tX6eN5WLxrS9vER0XXIvCMacWfmIj4GDVfJOYyAKbS-B94UlXIrTwHWVp3VuofFsH5dxJ_H5GQmNcEiYrccykMQciYD9RSIb0GNOmhck9gPHdcIgioooi0I_LPDQNJpt9s66_IFXNev6NwZGwYxZBlcgf0O0gucR9gGLeI0RTCgIYxAGMjEiSkTZLNrHCjj5tLXSqgkwijJ15tPML8AyoJ4NbnychgnITvioiBKPuAnYKZmLRUk0wTqrzIf_A-0cJ0EcETt1HKQUtg8yUAm-X_OO7fwJKI0IDwpTIPy1Hc373rwb_S_bnrdRtwuSo6Hn2QgckQHH6E__-NCgKHjglCFFLJFyCZPAEXWzyAuyzMYNZWMY4BGCXcdGfRCzOQEYGlEephlVsxlAEGK2h4_g0NMXCR8Zzgav58daqtPXN2_-RR0l-ISHTawcLHms69T-8GHtl4Ahw8-1YV2C8ydWhVbU9S_V2rbWz279483u3S-sI489iVNe_3Lr7oPu7bM7b8J7Xey-9gmr6XpPm0Zmj7qwndCL__pt-K5oLrz6YOvmte6bYNh_CA5V9-LljfvXhwdYxKYQ33OB_hGIfiI3xcCxkCywH3AKMWJqZ8QmhRumbi5HNPAqFNjHdEAouIEKaqOvMJDVt3AbVtayWZiYePUGs_tZNt-gv0qvd0-f2_70DI_5m0V7vLwOtFVfVV7lZkQeTeE4egENqCSdAY0hSHcwvAsxdAgbnHhFHtqpOnwGBIZuvR4T14KDAogiQFFHdf7sxt2_ogFw71T3zNfsQLhzui2sBPMUzs9JWl9js6DzzEwIw43i0pG7CllPL5psKCv5rCJvxDPnZmsZm9Zj05JVWUCMxlqtgenMNpt68_UH3fN3emuNsRoHzj4LB_D-J13w8T4aHhQP_sWtm69iYBOmLGo5Xxub0ue9X80VtHXYTMabnvl6552bhnl9-avu_b9337ooKgTeFPEQ8WpYvPq37vsfqhgFmyDACX4FaruFZhC1FmFx_GXg2Ytvb1_6Fwaw3vkY5QSL9SpTbPPPP2x9dhedWibVrMNWp3Gi0VwV3UZbF65v_vN1w0QbnuMRDFZkGcm9KM1DP5MMZiCZKOk-OjwJxXhja629hFlp0D_42_CGQcnztpv5ThqFWeLJJRlAJlq2HQyRRIxuB7kHL5gRL3OVnNMgJWL08dBG5IsEmU0cj2S2HcipDAASMdXYSCKN_r9wJaNHyFmVy25pGrHYzI6TwgE2oCRWi9VAJFqIHQRRRIzt-rntOXHqB7EihAEy0k-ICaOF7PoP6GM9-fRjR55kU_547R_WHv_58epL_KtXX7LoCyvw3rW2dLYHv2pxTA31xF6DX7snvnp13Bcb9s-yjv7iV08_-8Tje_BBkQPDgh3qgsUs98oAVRF79dDRUaRVktlhSp3IS2iqZIEGTBGrmSzyCYpeJr-5uMVBeLG8Ynn-oKhrfNHi7w12HNbc_KLW5u1Vh1MwbzAH8yJTTEUNmAQnGF6FKMaUH-Owqrya-XalaIYRTYLSazMGl9VnGBvWww4LXQrighlB05x6WeCrY2lAuwjiPgyMFmGdC6sQH-CJR1WmLsLULCXDo1dczFjYVXHh9Mb3Z3hMYpfua7BO12-Af9699bJogj57Eaya7fu3tm__ZeedW5XmXJoHmZ_kgZ-FyhI2kGO0_jk4_Is0GDPigK1IbZcqHWQgwogZfkpYF5k6xSZw3sW1I7O_cBy6P7xjEUP9b9--ufH9q5VEzCOQGBR4qdAi3wCIUUQ8INSLUihZnHqFbfu5Gt1AfxGj_yQ4Lr2FIv1V6vD0_evY-CpbXmXOFmz1Go-h84ZcXnYvnlElGGDbyQIM-JEn31nxFC--EKXvwByvDdZCyKQXQ5vAUkXZ3gH_hWyFi1ldWpOBPdHSwY4hP-A75y5u__MOf8ehMBKySXvXVDwWRMrCGtDhDVY_zz3xCpM0CAPY2SDIA6rsPwMSp4d1DoZsIyYAU8SPc-IWaa6Pnwa7UdwzQcyarStnkRisIRfrvOXuCNe1JNzx5RUucAx33vkGvgzqg0lSWUGc8RaEtAUTYfp1WbQgdP_-NjhpO6de3flEVpJJ53rj3nvbt26hH3v75s5HX6PTLjFFxDdLMDgxSsGzoriFNGtRFiwBtSj2nM2DvWhb6x90b3-__a_b3R9ekRxmdJJsfnwOXDkm5ftbjdfEcWHh1GoGoJEbBV7sBqy3kAc3NLJPDwOMBswjJorz2M5z1yUhUZxmYPVIBTgpqB3pgdCg8BOX2tSI3Wj0He3T_z8CniNDUlGSJ5nrgpWv1abG05GG40OEwxELoQmc4yQKbZIql9ZAyDFc2jEBbqQ298M8D8F_JomjYzQK80bbC_uFsJHmGetkzSM_CpSSM1BtzNjPhEBqmMmoAz2_arJ2Te6FZhRLdhs8AsINYlFMJuNuKINvfNG9_IaoRDAyi6tgyhT15qqO5jzdoD3xmhmrCZ-I-I40othcOn6jLF0e28EjceMsyJqBCI-O4PySB3pqPCphRnn4e3z3j82P3mLbgUFkFQ_qvvYxym2wS1mQV4ZrnpMhL23wsWFwYb1Bq9PCRGMqUILqCNlnID2c-Xz7my_Y-KEgeAnvBxq4RVdboOx5uOlf_-jzBVjs9eq727dv81Aq315eOcIPPxszEmPC5qC7IFqM5JhY9XL5DXYSL2GVFG8yZgGn7QfXt758ffPNz8C1YyPFcxKGAJEQ0B4VFJXoCKIciBNVFk0JjawC9cyOB2uqp3ic4Q2w1hjs8UBbS5UWfXu--9nf2fwJzv8bHuVCjbhWypiXmJGtmiUYmSE3UCmHmUiBhfTJ51sXrrNRsVjikUd-ActjY1oI0C5PD77kYbly2Otl3E0Ykm07WE98H3B3S7C7wDYGA4e2SU7aRDStcIW48-7Frbs3-HTsqD7Th7AkXkfwCJvbbJPRjqJYPrPJu7fvgfVutqpsXv8IXpW1IKLxwHmBNVxLvY4rcPkKUNZRMGA6ZVsUbrB5pSkLr8lLn9iPsm6VWQb1YpaUJW3x38UewE88mQJE4O8Ox4kXL_Np2Yl_pgc3BvaP-Wls8Tp2xZmTAc1wBBtekrV9-ir8uv3DWwY_7a6JfD-O3SyNSUQK5ddqkC0hOH9izCxp27i2nwYkdSOtLAwYLa0sRsPBkpFHN8-yzANdXPjahVXQWGKWSWBbYbqARXJ4lzjWTF44jeGA4cF47FQBc_HaOSQjy-8gj-rYwixZRWXD3RC-BWCeVFLUDUiQZ0HkB5lS9waslmEtjoKMJZOgReGEjuunTqGiowZYlnIZJoB3pSFd2LUVLHfCpY1wQpmfIR4YEvgAZhEhIJWLP8zgbKS9P9xP1Q5pT90jbDrQS7o4qt2tXVuGtZFlEJ34Krs5n2p5XP5e2s2TLPdyJZWIUW4lS33wAGSlWQqeZOEXNIsdT1lRBm5YD3scCP9LHugsjrIwLrIwiJQPoSHBpA_x00F7gamOT35-rXvmPMPe-kpIzzsvw9FDCcY9tctXNn54n5ndwqwqWW8gS4DySlP4o2z0KHn1KK807d7DhgJYLV8q707DN_rsvVnBo7LEnEvLhcZxkJelcTXJYe6mH0fZA-Ynd617hDCrrUbJ1LsXIu3cvXeZa4PqSJ4TpJ7n0tgLlSIw4M3k3jx8mDLmQPOs9sb6W927IufcAxHAdlUEVb9-BciPW82qgjkWDC875_ljGQrGRxYaimhc-aLLJ_ea24dgagHBNAH1OeanXvSvoihWR3KhAa7W5q1_cm4xKy-qZLEdFdROizT3ld4xcNh6DtvBodTkiY49m0ZeGOah9os0ulpP-GZsgLQ13fdr9vfO8k9Z34WK5TBe56ERmM1oB7J4SIUJTgzqlGxy2shaaytMop2ga2oUznt9VOd6mUdqmBvRaKuu8rsbd89i9oW93Y-nPtg-dYGzEYcYQgvfCCtxs7tSZGY2EDMLYj_w1LEx0OD6Reb-Ud2kfebYWeK5uUtcV0dvFdCbLDX5KQDbpAtP0iIOQWhniYo4GRhuRshgVCw2i6RoORlPcOavjCxkAet7TiJaGLlqhdwm5ddPhsCmqwVRtL_2Gnx38-oPCC5m-HjdsxfRxzNgEjiHKHtRVA1dugFmdbU0iWKK90_FDqs15tJEI71pW3lcgDYZF3bd0A7zqHDzSEsvhdkmr3R5aFBr6ADxy7eOq0IlXuHEWz1USRlSX1Tsf4UK9MKrW2duiOITxgCqgKmSvkXiO1kahqldJGagTGC6DZZ87ReKTdVFuWEEuxXmmTpVBjqbEtT_z4CqybBxTDOgGQiHyNO5LYWz1mNWTB4eDUR9p8HZmhXWrC5RXmu3dfNVUS905o2tSxiC2759c_vLU5U8gHhC1I1dn2YqGG2grOkzdgDENGl9uRRZyQO6KFfXAFEz1Mi-IdFkhLegng_ePY3SRNv0CiVNHtSfAPMMvJp77-28d7k_C88E0FUpbnUV2vk7uqUQjG3WmYiHlUlIlXut3rHIBsr6cUZ9VRJh4KuJl38IaGkyLA0COSY5WFuh4n4DQK1nW_cNhiY3Ng39Io_SHE6TSv1pfDR5sn4irDOphpwMmCsDRRTqEjkNf2bkayYEZdZvl6Pv8OAMvJ9Oksjsq0gp3P5e-O_sQ39OZOuVFmdKhf0NVCXiR9y80gWC9AT9K_JxhHqgJghIBSUjDEw1FU36qfDRjCBgJaeCiAiTlAZF6CQ6DqgA1Ho4dW9MNCnVkgzUpZcS4qnjZ8CkyVq2_SKfSUvPs-M0joMg1tV3BhiaUpUPB99s-5__4r2xrF6Go7b0ZYxEDRJGE0SenWNWMTdeRpbEzjWyJV6VwBC-2IGUozJFqzIPxloxCsLTYj3elKxmYdXlH_cX3opgOBOelRzs0CRMPS-PPR0jNJDbjKK20cHYJNPlRWGT2LUd47BofLYeptsbck2eQPBMoiRNwijQHR8aha3HMn3YwGpySYUfRkkeuJlO9xpYa5pjfzL4NJMVuXABp4bv2HCOw4YYlWTanXlC33fCNEj9yFfusIHH1rOj-4dWU9rUjwj287iOo8OHCm1NDP4wgNNUJ0meB34BSj3UC9BYamofJwWLhgETuT1DBLoUFD34Uoyh74OLe5enlgcC3OKp7dc_5_Gx7vq3IL0wSKABC1iU_YLIJ7EkKRpeZ05v3_pOhTu7507JdkdRur_59Sub9y6LihyZ6VlskZUlKae4yc1WJKdlGBN3r-J-3XhdZsP7PGjVni9Z2ayV3bj31fanZzDUyg7D9oMPYVxeZlrJqhGNQScnTpI46lAaYHPSfpogbhwww0kCukRUjaH4fu-RR1b2SHJW128Uvu-FThwGgZKgBgaddkkOBiYnR7dTkrpuVkSurijW-HJmw8OIQHGr1upSU_4Nvjpj0Rdgf-HggKvWmLGaLUyHVAZ-7DRJwXGisefaOnCtQOZ6Aj-TRouTwYEgdZzCT-OgUCrTAJDrs0geAhIczXtkAc8WKp9u-8ZL3dsfYdePTM4zVcYS_tWmQEoJiFvie1RFjw1kOVX0fECIOGkdRj4QP4gyqrW_gRpnhjz-_wv_JjVDnIPh7wYR6D9VJqkR4XrCHAeAdpOKz0280E-cNNHNMQbaW39PyEiwbYajZYCXzcvakYUGv78dPiVt49NmWoLUEp_K8gecwXy0sonCSYIsBA0KFoMK3BpAceLlDob4JkVDGDmJl9HEc5X7bYDA9dNtYmhu0lFJ4PwHRUApSXRDhgJ4k-1TYyC1yWBs7MeF59EopEoEGuBt_e85CgobrRfHZDUL_L6_rQ2imBBaxJkTqK01MNt0iOKnB19TLX1OAb65G9BCh7E1HpvWn-PCqKkMe0qLPCyy1FYa1UBWM-zj_YClSTXt2TnYwRQb-pUg1fhp5gl6KJBo3fd_4FELLI68-Sm6w--9sn3j051zr3EDCJ7iKg6xpphTU7kpGVgzHriFhOhYu4Gt1kOk_YClSX3jRXZh0zCxc-UYGvhpPbfQTwcQTTaiVLRJUjcKoyL2nVxZGgZWWg9p9sQ_012eqUszGto6829Aokkx9VBgzkRX3Pff8pjK1vvfgUbkRZaCdYz6wD10ZJjmUURSrnF5OFQjpSlr4qdCP-NyCQ-FzLaVS3DE3uyeOSMcIJnp6975rHuG5WxuvNW9chENkY9ucjaEn488cxRT3pix2Lh_aeusSFuKWRA_QmLfWCxF3pwtl4C-zD9hchPLU_cR9qFpQP2MEkxxKEmoYdp6zOjpQa8xh1a7eZuvvd29__c9EnfAFr4DxpivJLyB0qYl_P5g15RlEftBFIZ-rOsqDCQ21Ws5WWg1LpRR3PQEpHk_JC_7N_peGmDnsz5NATXAviUIy7sw2BHta2DiLRS4Yt59wDoOhrQb8OFE0xjI_Uufozd89PEnhJ3NRmAxflZ-BvzKLJzDWA13mFXQXP8KnITu-Xc3HnyweeG0NCnMcTFxrKNXV79HCvIA1osWhy8RUoYup5zlYRp1wLmPzcfjT8E55tEhLbQYgUSJcL8njj2T_dET1nkEA6ieUkZUmVkVLgbTHKIqq6dfAKZjHqj0w1BOsi4gw1hnrWvl0IGNYVhh42FR9thThNj97O_b33yuR8bKQ4qN7b0jYqyRJ35ZXT9fMw4sptj47i8wEoo9VpWN8aRhnb1D6tPBpX3nBlcXXFZhVzD4PB-ZgSuRHj8NS_xB5we_u4lNmlhvjyP1sBgTHlamAq44qI7NilJkFhrtCYeyjxngBIZCRYScr1yW9XNu4cEwXsdvyXPCA1Y8MqgC3e9z4c-zgVjoWweZyUIfVQ3EYI45uUvS0NMJfgMO0UBq2C-4oTT-U5tkEQV3KSl0UFLhHWrFN2n0Qq7lTm2s39_6Yn3r7gMx9NkzoqFltgPuwmH8oajReo7tITJKYUL-COGmIRrklwywoO6V13auntKJEb5x3E4Q8QawOA1VJ4OcIunx2ea1m4Ntft3Ln3Y_-0ZVY3GWBT0L7C6eFz0_r76FNsIeLY2iLvPmD6DDu29e2Fp_ZWv9HAd627j_1tbX6_J7t78XXeAtirVpiK8kA4TYmXHjlY3717fWP8LYDdPr1VFM24mCPM4LJ1Z4OgZ2pMFWBwaAlArUsQMP7M00SGPDPJSYkP0VaAcDdpRmLfhDiQvKFMZVZYoa61GnjScE2GiIZJlV7tWbGHS_ewOEjkwHX9ilGtviX8PN-uAToSx1BtmbM-SpMDQHay11ZaWsmwXDsr3EwQF4NaTMVbc0sA-3qCW2jykIGaAY6h5QnwK9Z_Py5e0Hd5gENfq6ZJZ7L7XFLXqmZYBHX_u8X4m9z3qy-nTUwENSEbHvR3M9Tc7MTPnLX8V55Rg-6--KyEAv8AF7PJ4zcE4EC3BbQBaMoGvV_eeF_nQJWHmtgawTs6FZ8sIaVsyKTQnCE8BV9OZn2Kgosw3VpKErjF3hdUkqK2ek4PBoqoYo3iLFsgtgreyie7le27j3Fag79C57YCb5mMjSwwHchJoUS0ExKBGXDHVYLXQcGlHiEcenie7wUECnhtA5AGapwlYLgtimvhPp9LMBY2rkHEZFJLWahYUWlsrXi7AnPJyr4Bt8LNtcZS9iZRbCd2Li27YTuJlyMwx8055QeRVUqUp1UmpjpJ1mSiAa6KU6Nj4dIFKQKIpheRcoVhPePtujoTfu_pXrVtGxwdjMsBu--6rHbuBfuv097-bgnVFop976cPPaffEh656qZE3PS700ppTErgrEG9ioMpixf5hT6R5TcPai2BN1izwmpZFP-0OsI4GYaqC3GdmCq9pkS_jWk7Q9WFMHegOr8VZroDBwBmwfhu-yCh3ESWNcrSVBKTs34TscUW2FmSHA-Wj5KeZn9Xl4rFLZC0vzuaHh3uf_hGQSaKt_PCRumISfVAj20Pzv2XdfOISQqDqs3vO5EVbv-1wH5fEPz9bguLbyQ8__aeahwYgaEfhjLAKPoqovKI5fYxkRfFWJarvIbzVokGVJnxcQRVUEJxlCLCxbyBsGU6ov71EooRpFd7-gpBpXV6YFK_B6DehLPdMTL9Csw7q1JQ9WjTkMatrAvxx12MGbDjQw5MTGNBAhRx1zAHw5Sjw7779Gu2rMQfhjy7JKOMNgeuIOUwI_ML9sruqC0zDx46jvrtaDTbsrSOW8VJaDAJVcoDSqbpG1Uzvz8gNs3FCC9IlDDjSB5RbtPsSJKshv23fDwsnGWEklouY8kGNNwjGwXpclE6yhgkau49nF2EzTwvoFtGaEpfmo1M998JKG1V9FrjAqSOgkdIxF7YoGOo8KBuQWUonrvlq91gYLrSjgSyVSroJcDnWTJLDD8cglKtnQvn8UK1NEJQrXcBZsofhGFY2S1PVSmuVjrGQ4oOk8HPnmqtVpCDDQHMtfOg2pjXgp3lIFjYLETQPik_FoJAOxLSLMFuCfxQ7lWA7aiKxkIw1BamDCz1m_xsNRW1xCrmy0wXMD4UrrB1Y1GoJ0zNEHFm6geE56aAMYctJDGyiPYw49eGWLAXI46WUbMH566D2AAvc_uoGgZ47uWEcbWb2DgfZag0lrERRO1-CAFKRTbx-UHw00vQnONGhlaFw3cxrXeuIFMY1qmBz7lQyIt4nONXhvhcYqMyfqgyqb1fG2DLF-WjVy0DcysMomN9Ggca2xySY3y5DbXb08yNN0jFmGSn6y2KIsk1FpUWmcsodISAMUTM_isSIcqutoy4NygYEJNuqwg7sRRzEezH2POZT2Rp-zcZYqzf8iDEjSZ0AebN4q6DK0bMEAARKC5OXxAIlexmzLCooQ8F_s1CXjUWQIJlqlWZbkiU0KZ4xJD4K2pgx_VsBsXns7QI6U-KDqkmA8cmBffFl2lrEMHi3BdpMb_2aDfNUto44bF0kajrGIPVHi5q2UopEIw_EgE6vihmU2qs4PceyMkmjM82MgRIDVDKx75LEnq-iRUc_1--9JP9isu-PczVv9MHczEohYNJRVWfEUL8gg6Xj0kAB6DK2t2Wlj1Huouq5kmiDwIt9LxljKbmB98xZttbD1DWyj_s451q_9wkqrimn8IvNiUozJNGy-KgrE1ImS_usVDzbPbtCC830h15U6qfE9Y0kk5ppW3aEZuDHtv535wBTAuHEOzFoZRAntOAyccBzRun9UxHkeNUflU-dRp6ogSkaSzI_8Mc8KF58zfDFMgu2JV7LYQSpVGDAFbJAfjUOzKiTHeVgJWwcMhYvDxBdG3mcsLLCaqdLOUVDESR4m49KMRU5SOKmsl7VWLtG8iomcPPYKEttjTLsrCOW8NRSDkpYzlgShrCBInjupY49rruiM2DJiRWakUzIuVpdfIOD_YovklWradsAnzvucvANSaV_YmfMqD27G46o8tTiJPCeJx6QS6bSby3jhAcjANSQOzMwXCZZNDVcslABocZF1L_EsVnGWE-S27Y5j2lShfepOmRlLYn3OqF6XyqMWwE66XjouzcSpn2GhdwUfytgMrHXQGkyPwD524BSylGKVRgPnMYuyccytA4GUoppbBjujBvptjVbp9CSPYs-n9pjUYisQUHwWqaORrFaEymeNxctrDdhSKflLDAZXuVoaEXVUt3FIZkIhmeoxDSRTJtxEhJxnXNo8u3ggh9dAMp3QLIMxUw0gak7RG_4iQ5zbg76LASI6uYkGTQoNeGnO4lpPaSYeBL0cHL_RWU7ReJn__e_hcYyfwiCHnn--Okql0TDHmnzXy1o1ouNDGd8AMDTH9_rihvvepF4iuoyI3l5ENAAOJ7KI3TjFwPkz5_GtZ2vliRIdLmVPVp2rYYzi7_WOBgbgOHPvKvA0ct7DGN5AptPDgzv9tAw3iUgTT_wSUaLMrvewlg8qNgxYuslONqhaNSDcQ57JgIab7EyDjrYGa3vI72SgkumZhsOd7X9QA-1rcoMaMFvmoMMRvPY_rAGUNcawg_FpDT81ydUaQE7msH3gUPsfz4BwGmW8QT0ew6lPyP7GG2ZJSu1QKxXuQpPn8RoYpOkDhqo0uUlKAi-ORlzKrPUkzjUQJqPoNXFzl0X2DGifOXavEW5qBYUMVKeJ7KCBsmSO14fcdABxqiGSRhlvsIREYwWZ4-2CQ3QAYawhgMYZd1D0IvpaFgQHGncYJ6sYgIgZ9fngjI32mUawXaCg7_tjrmmW1Q_0RNaWCd6VC642BS3SoKtWSQpqdN4xlmYiq4JkmVtEiW9HY5NMe7CsToj52kg64LwTjFY9IQsT7KiycghlXD4-8Y4WgjomLBHIqdrySrNkMbEZfu-wIKUGVKoKKPte4uSeNzbtdJFzo2xjigrMRVFlLCvkZPUyrFmV9JFGpXrQ0EwTPbwGWpIeN5oDGci6U3gzptkZMEJtrAFHNJE5Bl9Cgw1NZIIhFQcK9efhvIEB_PNw3sBA43k4b2Bg1jycCQzomIczgQHN8nAmMJBV9AQ9yCozlgmsYgY8awc9dAYCijlZH6rKAexdDRVijjcAQHKAYiENsmGO2IvbcQCvRKNdjDDcoPURES8izr6GG6YF6s1VEMztFstl8hgBbG62ZJHSwgaJcgbLXVushiCrd0Shd7NlHanahDgL7Jx4oy2K4WWYNw4sY7R_ADYDgabA4G9TEeToMe4H1aYGyZjELhooEnq4IdgUByjhNNrMjRJOe856QqamYPBGszG72CT1A5dUGb3mY44-mHLSbcbG0NWNzAcoMdMNxuOPPmiJUof4XuGPMPquiXos4yDAuliWPdDaXN0p4mVBmkQTWYw7Zx3pa5fOWhTMXzxW3Dd9FIOrwxqmq9LSOSVhRuNJEQzFCh5vtqDKgsaIkii1vYlM7PHKaBk7EDfDMcr09n3PGBfqzPRjaQ8KGTdwwTxyJkUclqdGVM599oXEsVuQos8VH3X-ADQ-tsBJZ4C5f5K_OyuwNvkXldAnJ4C7jp-sTB_apLAjnwaTopGsIqikS5LYdn8yddQ5wz66DL59rVg7jogjqDZ5Oz18d45101cRJkyoH_XL_9EJ09sAX0Uel2aZl6R0IjOjTjlittljg3eNSx1JKrQXdecTSmkeG6uKEwYOAb9gYoLaKkDN0foav2Wgt2dGpOsraZbZ1I3DIJ8MzVzTuuaWjUQCUHRiC8V6UkEw9q2ssnctdmmcR97EaLaPriuNL2BMCa_3VK1RW-4sw5L51MKsO3ATh27WH3v8QRWjW_fHHnzQStLt7RNa-fMwErsiY7cW5SFJTDCX4ZNfo36rE5QOeOxWOimYgAr_GpfX4oEh4LYnGotYNaYkfyZlH7qZ_DpQ1ryIIm63DubpLsToeZ7uQoxG6ekuxOiunjJFdEt2n-D5SRlEd2hPcRVGN_YUV2F0Yk9xFUbX9RRXYbRZT3EVRkv1FFdhtFNP86Tq1ulp8oXum56yZtMt1tNdiNGQPd2FGO3b012I0ew9ZR7RneHTXYjRRz7dhRgt59NdiNGRPmUzTPesT5lHdEP7lJ0X3fA-3YUYDfFTpojumZ-yZNVt9dO0k3V__bR9OdWCP-WF6Kb9KTOI7vSfpqmq-_6nyaa6x3-azoNu-p_iKowG_ymuwujwnyZf6G7-Ka7C6O6f5knVnfzT5AvdxD9NvtAN-1NchdHOP9UdUa370ww26K7-aQbkdAf_FFdhdOtPcRVGZ_40w4K6UX-KqzCa8qcZOtft-FNchdF6P02-0G3209SpuqV-mnpEN9FP0_rVDfPT3BHdHD_l8JvuqJ_yQnTT_ZSj57o1f7oLMVr3pxzG1939Uw6_6U7_6S7EgASY7kIM7IApx5s0fsCUw_gaYGDa-QSFNjDtvKTCJZgys2oEg2mfGoVuMN2FGOAHU5asGhth2ulABZ0wbaWnkBWmbAZoNIYp5yU1gsN0F2JgPkw5t6FRIqbMrBpXYspKTwNSTJkiGslimi6vBrGY5io0ZsWUzWYNdjFlvatRMqbt0Sh4jSkvRONxTNkA0AAe04xhasiOaWbkNDLHVItNFQLHNPM_GmljiqswEDWmfEw0BMe0QyEKp2PKFNF4HtMuiVK4H1O2kzU-yJQLCTWOyJT1vsYbmXZBssIlmbLe1_glU47JaJyTKZ8ajYEyZRdGg6dMudhUY65MOQKh0VqmrX0Vzss0y0A0sMs0DTON5TLlTdEoMNOOxijsmGk7dQpmZuoSRILSTDlNpfFrpqxlNNTNVHttFcbNNEu4NIrNNIstNaTNNKWpBq2ZZsRQQ9dMMwijwWmmSQsNVzNNWmg8mmlaHBqbZpqr0Ogz0wzOacyZqdqAClVmmiFCDTQz5fyTRqSZdhhboddM2fTSSDdTWMjzBr7OHw-tLq0hXk6H3XzGpmoWRS1DrDs5GQOjUjjSem6EW2shQlStIZcAr3mIAdXBmHjlXa3ZOMZB9fDV2F-O1fCFV1bosTAOM-K4JHWCMHHjoHCDLM8jTYRGp16fQSwfPqDv2U5MmKvJP-O4Puxt6a4YPxpL6BnxPj_nl58i5FbRbFnq_qcjAu_5YOCnGsRnf3fV7_NueA3JM-qwg8CqGl1nYmMaQDmjjjmIoKgxb_Y35lAsrhJOQ7bEdpgS-IFd6FENLqlAbkadlt2-9iy7sssq5YWq9TV-Sx37lAOKUX4hJLtoTFxXVXU7pAF8MwZB5NdKfsUJQ-aTmOXmFa-VGJMa_GbUlbA7154lq_Iq4ow0EGB9BYhl3EaMf5T4gfoW4yooNw2IMwaN2E3EKDUFEN-j1hK_J1iD8XHYvv3BTRr4OKMuil1W_Fy7uYKwZ4xKiqVAJvdde8iuPysK-FKJlKu6Q0Jj5oxBLg53x67uYNcLiMs0-c2w7N7TfQDiadycUVfCLjD-FWiXFm4XtRZh85BA5VJz1eo0YC_boLhyBATsNCToNxP52VLVrYcaS2cMGolLD4GLGd5tG7SVtdih_DZPDalYyUYaTsdAxuMIra3a4hJyZaMNGhuEK60fWNVojJwxRx-8Uk-j3kx6aAPHZtJDG8g0Yw49iGFtgM1MetkGfIweGjTSk_ymbHWtt7r8_WDQjxoTxhy999LCoRdzHxjBUoO-THCmQStDQ7qY07h9t-tN5JUM1JaJzjWIoalRWcyJPLxwRqNYzwoUa-CFDG8xb9XIgdHSNerK5CYaNK41pMrkZhlyKYjCSxl1lqGSnyy2KF3eC7Vbw6Q8REIaGCijXvw69IZKjWgy6rCDu6HBSca4PdfEndZnqdL813Ako87LzP9fNRHTfpbfH5hRvIGhscYtWzBAxGWDRQ3WJW4c5LZl1Q0WGqJkDIoYQPurzdaJot5crTTLNCLJqJMyS__phmnAZ-0ZS5r3KOWEJjIM_9UlRMFuVJDDQCkZgxw18LzKsrMMspdZgu0mN_73eX-YAVIy6iKYZf9L7l7UBIK14Vew2-Api-I0xAXxQBz4bos2Ku870cAlY5CHNth1IgJsG1j3yGNPVqJ9a6CSUWdlVvxz0mvW9grznoGDTB91xiqzFoLai-sLq6x4DV4yBj3Eo-z2eQtjbM1iuLquZBqNYDLqUkIhYkoQIA30tFZRHSCJaKvVbJXs6ui--xVRENEXVqruHDBQTcZhGjZf5T0DGrdk1HkiQQGQnOD7UuFs8vvZ8fp45tzBy6_USY3vmQDZB9e06mYKjWUyBgUwApsDs1YGUQzAklGnipEIj-OtPngTPN47ISRILj4TF9MhWZqIXo_Kp86jTlVBFA1iMs5Z4eJzRt-tXGtrA7fnskQVVlnsIJUqDBgNbDLqyhKk2W-EN47nuJS-OQum8CslYShcHJALdFWzNWO1a8vwJlV-hAY7GYtmLHKSwkkt0WuslUs0r2IiA91k1GnxIopHHvkF7BYXa0LLMMUDm3NY3dshLhDBq66YTIYdrSCIgXgyBkHAD24Tdr0Lu7MyI52ScTGVtzHlsHGLLZJXX_OpcU9GppKDVHpG3IypriDlDCQuzOQBXn5_oxmPq_LUNBbKOFTquwL1BXalSs-dnkIJgBZfIWv1JslLPItVnKXxUUammctpRtnNRe0W7mCdpLTOwnIYdUYRPWOxq2Bq-BNp4_0a-FOVKteYKePQTJx681Y-kJiMzfi9JkyPwD524BSicVip0TSCysjUYoaySkMt09YihUWy7AC7FVkn37iaWwY7owb6ba3yHiEDVWUcarEV8OwFmBJ1NJLVilD5rLF4ea2xgolHLjFKDAZXuVoaaWVUt3FIZkKBpugxwcR-TAgxJtxEhJxnXPAmv4M6vAYiyoRmGYyZaqwTc4re8BcZ4twe9F0MLJPJTTRoUmigEnMW13pKM7G-15fx_vC0eGc5ReNl_ve_h8cxfgqDHHr--eoolQYnGWvyXW8K15gjD2V8A0rEHN_rixvue5N6iegyInp7EdGAEZnIInbjFAMlxJzHt56tlSdKdLiUPVl1roYxir_XOxrAIOPMvavA03AfD2N4A8RDDw_u9NMy3CQiTTzxS3gqHC0YMA-WDyo2DKCOyU425LI-hcTxkGcyoDYmO9Ogo62xNB7yOxlgGeZF4471xBi3jBvAF5Mb1ACxMAd1MQSO18KPOKwBSTHGsIPxaQ0wMcnVGnAR5rCe9RQ5QdW9mvsfz0B9GGW8IVflKfCGvccbZklK7VAr2a3EJzEfz_N4DQzS8Dgeqdf-sGcRioHgMMpSZq0nca6BMBlFr4mbuyyyh-OI-N7cQmPWeg43tYJCBqTDRHbQQGYwx_Otx9TVkQcTpxpgYZTxBktINE6COV5gPSs84RFPggF7MM64g6JXoxjsf9xhnKxiACJm1OeDMzbaZxrBwDQYZ02z_LJeM7K2TNasFLy2ZQpapEFXrZIUWO9CsxMrTXgDxtJMZFVd_qzBDsYjmfZgWZ0Q87WRdMB5JxitekIWIqpiLbbISmXlkAJBGI94RwtBHS7BmQBCOVVbXmmWLCY2A7RcZO4QklJZ9JVXHWtwhPFoJzNnWCXXxhQVmIvwd7ASVYWciPbimlVJH2lUqgcNmjDRw2tgIOhxozmQgQ28Zxs2uM1LHmUZ1gi1sQa8wUTmGHwJDVswkQmGVBwoOIKH8wYGzMDDeQMDPuDhvIEBC_BwJjDa_R_OBEYb_8OZwGjP1xPE5kXJM1bZWQFnmLJEqhnwrB300Bkt-OZkjjHbwexd3UlvjudazxkrPlixkG6JN0f0QKSJq6IP5pXoxvYRhhu0PnR7-p7DDdMC9eYqCOZ2i-UyeYwANjdbskhpNcgy5mbKJQz-wx-zekcUejdb1pGqTdDd6iMsatb6raMzeOJWZovVDTRnyyVgNKag2DXcy802FUGOHuN-UG3q1vVJ7KLRgK6HS-Zw5WjZg40GrHawEk6jldwo4bTnrCdkagoGbzQbs4tNUj9wSZXRHz7m6IMpJ93xfdDbzvdTYqbbuMcffdAS1b3ZE7mpXbZKEWBdLMs2qqOQkVeqS8V0i_b4i3HnrCPIhqgT0hY8s2Txjik8Vtw3fRSDq2Y5oCXKAavS0rqBeyIEQ7GCx5stqLKgUfdsjz-xxyujZewAByRgBiNlsCSojU1yWau20p6x2s1mHT_IwFiXzvauQkZ3dE-EOCxPTcp994UYvdzjzx-AxpcNf-gMMPdP8ndnBdYm_6IS-uQEcNfxk5XpQ6PTeyI0klUElXTRfd3jzxn20WXw7WvF2nE4Sixn3ibLIAOwQ3KhAUZaFWF02_dECNMUYais2dmjespo9R5_ZtQpIHhU7Afo02I9kY2mIhXr_FSdTyileWysKk6oG8EnQh2rADWHTaZZndSWe3tmRLq-kmZGS_gEaOaa1jW3bIRVounEFor1pIJg7FtZZe-abhifDM320XWlu8ONKeH1nqo1asudZVgyn1qYdQdu4tBN32OPP6hidCP32IMPWkm6OXtCK39-oPPZSfOCxH7guE4YRFEBIi_0Q2bdYKqnxMZsvrPzQTSjB56Poj_NyMZqsyMa5-CN3jiDDtzIH49hqSRZpHIJ9WOeWzg0i3PiExJ4dhFGxHeKAlVS2SzaxwrYUdpaAYnYZk-UqTPvJUVBE9tP_NRJ49QP0ghEUhwkgeMEiUv8IgCHoggc2wEhEEURDXz4ax4mKYlz1v6yj9fDvx8CXy6ctaNZN_y148z73rwf_i_bnrdR6ur3TwrfIWAxHzKpAmPLRu75Q3kzKw8_8-zR3x557H8fO_Krx489fvS5x558-rnfPPvE3DLulPyupMyxECnqF3nsZrDw3I59J3KdCA0pxiK80XyJlEuoeyPqZpEXZJmNm8fGSLElOmSxF8E9_2btt_W8HH6qxGxAVBA3he0mtJCzGZ3uYrafYaai3Snn0VMAJs07WXtWVtqrrkUrb5GivdD4GfyzHgdzc95SNHfFx8-BHIHPVQCSc9iMLHpWFdozSmHo-hdwR9vNlRV4AxzJaFCdAQXMAiA56F-w2zIlTw8rYcojFct44FikRDpqc2JhT_MC7JKvD1iVzi62QBOAFj3y2JPo9zZYbfAJumaVtHWylrHaRV6UQWdJJ69REKZsZQxYgYd8yzYY3sslvuAi67lBL5u5BOLFefwE_oRVobDyep2kzdauCSuxbXHkp0Xm-67LSr_ZthmwAZJJ_s0a2lu6OzsUYIkEqeukxAvkuAZugEI9aDYLUA9lqVVU2qnVeZ-zxHhg7Yaw08gm4G38eOo6yzz_eOoDi2_JnPUboGS50MhkmrMUAWjsZcF2Y3h2ccl6rk6yEzMWKub6jPU4DE9ZGIK7WWikl3OWXtNCQy2qBe5NrYXpit49oStWSgssDcMOXyNDjrvBCkH5AAsNERVH3YsVftguwWYlst-mhJFog6tH1g4Mw66SVj681FaQ2Q7BUrdBRBKits-AUhBkRq-c0lxU7BW4iS0shZuvGNilQVSkoR-E6jgbeAq6ORRLvcGqaOmYPCvqxmJAs_MbW1qAXrXsxNrgmWWJqiFqT6yFpkWaJp7nFKzGmr-kxmEQazkIrIIYGARoDLyf0JQoCWkgLeg21ZGBE5RXvPvbZbDtfpKjKorlIgxQBf1242AkiLnSwklhrWESZamcy4BN0NWOI6MgZG2R3ZOdS7u_uONgzjPDfjpXLsZAStAvPiHgA8nZhJIgtqM0jkI5rYGFoOsmR4Y2UMlO5IKig_39u1MhtBM_cpI8JkUul2MAIGgqjINnIA8S9d3UJ7adFIriBsSBrvgZGbGAod1gtIEpUPjK7i8eeXDyisDPck_xvYFqoF98DJACqYyyjORelOahn8mpMjxvmV-YtskjjxwBC7iRzzI5ybKq8DJtbUzMWUfb_VzHycHlf3uJKR3QB_Db3COP7L4kLwkoWErUpawZgXOhhlLQereq_3539YtddpkfUlAOWv1qLAUxPA6MjMMV7CpsG-hAK2NVArwExtB2FcoiDDKbOB7JbD1b7jsgr2NDrBw_fhx_Wmjw6pX_bHZaDfjfH8--KSrJhJ_IPjEwnWCLZX9x31-4TaRHYEdgbaEBM-nFZvByPUI_CaIEzP_QyaharMaC0CqzUyIrN_rVVQUdXD-3PQedj1jRIQqpY9uRN4QO1sB_llU1zkLjmaef_fWRnz_5hGX9ePXUWP-APNaTTz925Ek25Y_X_mHt8Z8fr77Ev3r1Jd3TIjLvg1-1aosN4Hj1xF6DX7snvnp13Bcb9s-yjv7iV08_-8Tje7ABdSOSEwfkLMuCcu2jcTv0CSlFiSPyQrkKAgjsTzDegP2YIJDlDXXQD_8fmKRcObPvNJlVh8ZBiQJjFf9cwT0OjUNwzWI38RX3GHAfYkUvgmPGQNNelOAZKV0iJ2sgjV-0_gNNSf37QuPF2dlZ9f_wq3Wcb1Z-HL79OC8RkhKMayolxF_UdZ_qBPAhGIPiAL8U7y5CXViT_4ta-zD7--EUbG00eHl96IsWGhTM1DViecpklD4an0B-jHMcGVoJh1q2JODniNjBsPGJKJyRQw_Lm0lmKGLXo3aSucTTukihoQjSH23Au9SZ5jccF1Uv1FtqxY4ydwqeIq0T2BGGGhOpUcusX_76KTiNhmThLzxnHSlY-R8Knxbrbl5EQ0IewjrzkdHa5oaGwM9Dg3tmoQGHFNPTsCnlo1a9t45QWaa1BvAufBP-qTxTeQLfiSzCJlYZj3mQoaHqZ6GyVAj10yzP8x6VtQeuy-5aK09jv4iT1M9Y_Iybwho5xtBaiBKAa1blZCL70td6Deql2WLG6JIoTjL6ovEjcNp_BVtnKG_sWQZHDf004ZrhrqFnxkqsRPK_b7PBCKNw_sFjJIYBUcKxAGs0qzLJotBN3TQJC7BNFFE1nI0iKlJ1fygzu5M3Ams7Ia4DBrCaywC0EXPNWkcMnSf4hs3GeFL5Ok1mirWVD8LhCdrATKJ8jzfSKSoowaK6bTlQIlKaV9quytnYAEc6wJ2t2bKTyhwEe56HsLmHBY_VWqJRT7jkcDKw0R0HeBadL963xyNN-BNWtrCePhYtQe8NQRawnRbcqpV6pzQrXqyUwGniq5FJxhlFm1n4L-QYsEFKuebhqVAYSQhXdpxLNKU7YHdx-x3jUrLkUYabyt7qmJIvOAcy835AI0o1t7uJ7QJXEcdJ0jTV9oiGFuphrv3i_ezOXtSPY8f1SQB2tjq9GlxIsRcKap7Hln6ycGLl2dKZU077x5bwZLPDi2Gc9owqwuSkh3Vw-rA0K55I_twTTPqW5CQ7wz1VnO0m6CaumvgUKseNhYzNFkvm4JAgtUA41JsryPEMc4KP_VvaSoHjlmVMaZmyFhkWTjrZrGEypO8tngN7N6Oq0RU2mGYt2oYf4H-E2yr2mRvIJC2b9Q6WnILjU6qaWCxIV6fRUAzLoGUQWkCQBtbBhmGiqIJHcicMPD_2s4Ion9BAaurhkX0B_-zOIHEYu2mU-iDwVBzHwGoSUx0xTo04JynVZ5VJVoY1wtxeJtFLFgCBk800HAYmKswsOBB2EVB4RVdFtgwsp17Ys7wm82lCxKM8a9WaHZZPL8E9FhHWhYbLnEN0okiKUUAM-GIkigguFdISHIpUWJSofTxMdJYdZiOyZByTBgKXYJW9PQzZ5hqPu9w5loM0eMO57sfffYe9zE5izH2QULuaGlZKO9qVmFAyeuLnORiktutqI9WAiRKDiWgZUZUZfEuBIpxcBKuWeRORPiZSPaOD1-HudkUoIwGpkkShTVLl0mNPlh_YtNelF2thI4sImhlAM-JmVf468WwvdIOY-uxYiHioAq7Sxs_QVuHdz4QLGhkUMrwLUe9hIFeZcdbnePRU2ooYktnNyANKEm1cK2XOCi4qYlF25NgU7IOABMoMNiCvNKfsH8FKShkSebabRQXvtuUGtga1MiOtI2JUsR1t1RaZ2YnGxO6vCeczTl3PDkJNcwPHSr_mPmGpxLCJA3LNL0hR2OqcGUhVZnB1ROApjQLVEs7O7i9ZpH7sYltUocMcBjqVfskRwabkxhZRlOcRnDvtFBj4U2Y0dUQ4KRaK4g_t_rap7QV5nPtpkGgzWoNN6bfdL3aUHDeMaJqFhVOE6kQYcFJmxHREdChS5zpf6O2KQHGcpkkWgmOQ6ZCexo8yA8VjwEFJXoYXDxyXer6t3ttAiFI9GaMDPoG-Yy4Dz8wxQVaRIyE29QoXhBNRloMBC2Vs764oTyr6l2Z2HpPMs5WLaQA_6Ur4kXGc2txcwaLi-lqFEMp82w9SLyqKQlNY4TzpV6qEbZIqHpgiiolHebKdC26N5KTL70cGZsIDw0IvZVWmzklsr8jdwncdpSUN3CaDR0eFYYIlUJYLYn2aGCfFMix8UCy-ynYpihzsgwRTDErXauwmXYA9MhQTs-CUsVdhknmeG0ZZGDp6JQZWk0mnfUIvKT3rg-2QBmFQKCFhoDEZJdujgivxE8ZlFh6ElZUq2zPyczeJ04ASohKOBgaTftHxIJWUziNh4EfE9yOVDTdQlozitVFBkzDTJwN-u781-MBe4adgjnpEF1UoTCXjrUeFSEJIC-3e8VSCfJMq9kjBEMvcwPcyJdYNSCWjoGxUhKSS1otZsCdoC3-tcDszD1R15oa5pySFAaFkkGgiiEjSA7VpkIZgdha-2hgDJEm-_xiYR-LbGJKEJ6r0eYBH1UlgPUSbixoWyaDAqChHOjTNDDozGTuQeygS24_yInNjbZ9rJCRjMUzRERVmUMeHM2VjDaN6wM-1FRDV_16KUEaLFlXGRhFGse-7WZa6uipBQSZp32o_YEYV8SkncYo4soOkMMx-hZmkwg8GGAAzm3iGAd6F8bYINKPylwzSomjOYGq2rZxLstAwvIdyDU7HMrj6e5ROKBtfROctHu3BwqSFBosl6MTDLFklMqJYZcF6sI8OdUH46HSnhnEy4jv7hFeqqPkiNug1mChMlLA3gJx0fFm-7tHHZ1QN0Eqr2W5mzbq0Nvh5l5aAiNXPWo_1mAa1RRA77ItMTM6KiHKGAUMedOttLGdyFEyONuE1jgOeM3-oL2LNJ9Zh5yEBZxEkFnFkNAZKLNoXenKXkLKcnJsMQ4qGdCSs7IsP9zdP9lUn8uoLnrasiP1FTkoohjDiRPGGgYnVwxt74EZVRDhiz4l9J0s4_ATXORr7SlYCAtvW67SuylwKnePrqSyScg9-KArKt1uyKetQYvv1eKfFIrh8fTNmvk5orVIWUC1jNges3ZLZcUxolz0id6ExKHNF_kW64aUZiIWdgZ-5YOZONLxYi23MQkO2TwmlITmWsS-KSXwjllVgBWziZi3G_SweKWoDjsM3y8Mr6qUOc9_uOC-zW262jNIw_hYzFvAfihVh8mNJ1zJf8kKDqw6W8erd2Aq54jo59WIX_ks7_gbkmM7VtVh95IzcC23PD9o-uKtY-YsvYagRoHvOiyh5MmjGMH1E7kZb3hhYJ7CJtT8YwXCppUpd7rnQwOaassYS2GwPMRLL2IwFasHcaTYWS7nTfO2i3o_p1ZQamw48Ik9zz64rBxc_AjpgyTAb6t9LlXXiCa0ZsX5cIa5NJY5qtJ5XebQE_GKPhn6cFCrtYmCz9RzifeKi7X6Yk8zzwUaJ80LneAwMtp4cj5EAmdHsKDI_bCN0WxyXb88My12Is3H0cS4gRUfSLP9U9CXhw08yS4PlSmbAVT1ZazUby6wTWeZZWNKHz2yEgU7QtZ4EjWxgltlx5YHoKjCdXOox1ZlOwnRTjnuMfUGoY348dV2-fAOO6tyPpz6ocqAjShLfCYNA-W8G9lzPZlYjtO2-h34KKpl4fpbpuksDY04KZCkIZIGLmWVn1YZaq84InToj1CsPMLCGBKCVkgEVSRkwSAowxOM8SxRfkSDKgx5N9DMZv2DGE5pGe4QMWHWgkHokRRPNeELENiur9KKI2H4Ki4q0l6Lx8mRdSKGYRlncKZVeNZeroClmlR7jgV40FFVsRVCWtSTAekXiSxe7aFgXbo7OWc902jJw0mOssQQihtMWGkODK3JZZgCI9F7e2KzyIROSBB7odJLEymgwQP60tb5f5DhQdPBO1ZULaURyJw_sIHC1jFNYf2LO37GsIE-Mgh5ZLIcmQditlCxryys7GuBUAX1AAPK-gIXGsK4ErrdhwOPa-TvGZNBxrntEfwBWhsgGDlEsjmWjqLtZzgIIXqLiXZOF_oTNLtiX6UGs36mK9bkhpVmYh7GXmpkvgUY42FmhCoXrNaDEGms_qCpDs9Moz_3QKRw1voFBqET875aaqMI6THtnICJPsORog9vpvxPtDW354pgYba6ACOz9O2ZHQcvXmKBG0TkjCDPT0wJhiQoJ_Rh3LJk3yqrshIlWp0Vb5Pqws6bC-MX639x38ySyqa68UQiIRrGRck3aUpJpvgCliQHi48o0PJauHZ-xjqOs4T-iOseEluQL3ckjekTIyWYtL2XLXqmQM0BxdBr8pLD6JFZ0iE0vaJ8wKSF29gSlK1VBjwwUrBu7Pm_05G5ZVISF4_boFCuc001f9VpBs7WsXn0uU5ci33lANBWXB2MgDEOX9qqr4TiMFQXMSegl4Jj7xE-1a6JQI-WFd8Pic0VTsl0LhDHrhqqVPbFEVcFTx9oO0GRYsME1lXDVlQB-gYX4uUkoa3ikpSc142qtzswYHIt77dw1WGgwzueVSlhGLjN8vR0S3OOXGoSndKUSlVJ7oWGK7aq8eOFFbhCktpGfN4AxZZCDVRmq6Caa1IhaQFfYbbg8N9daVlhj2DwkqhmYWyKVFrK2kOxVCiPM4pjkYCLqHFrsFLC7ZoqbM8lwpMqKkIObBonj0ChJlBdiQHb2KIaGKKaU1ljJhM_JWl99W4lyjO0KKmRup4o_LjQMN48XwvU2fPBgQJWdk3hxDL56kkQq8G9ggep0vyif23f1nGn_8GKUI2x9A14GUX4Gi0w01mB3sfiEsDpe4XXwwpTfMhQCPjx7Gj72YWBW4shtCZkZYsAbC40A28ILoMJST4kAAUePu3kV8jiw4Xgn4MqQTGXmDDxTQRpRqKVrRESVlipLhMMLnINvI6q2RcZmAPpwoSGM9JTybAP8bc1qZoySuW43HLAgKljdJ1GYpDQoQifRYdQMwR3zflbvw97cncftEC2fGGtCM51UU4issqtA9w4cZ50pVd19HklI5NhZSnRxgAHKqnS8idwoS26VIQUSA11k1iAmK677C7rl8dl92-MgiQkmJEBCqLfTeK4q8jw-RKskp0PiEIPdkQ56Gait6t3HAGJFmQ9KpVUySc-zFMLBBXnT7JQ8h6DTyIpqPPgl8hqdBj_03GJ6fGjb2S7RFK4_BpdY4XlG4H35IbauaCmtUWOVOYTQk6gRaswOE91nGJumLcKackTkboWUlSclxzKZ2LWdQhelJVEWFb7df1L6UGB3Pyle6IYxuM9R4Cp3zUCqVRF-Juhxa0AfYAEf7aktEpw2C3KMcgNTxEoGJYF1ZKGhUUoqDhy2r0ZxREIvVILBwLxVTPeYBBFSHCaPX4_-Z_wwgOmBx3CtJ9IiW-N6vm9gpZQ85KGOtAy8mBytn0MBs7I_DsYeSVATpIrjQt93wjRI_cjXhZgUvEi3iPpZYBfsz4pAlUNcONCZT3WyxwAFVnWKw1O8LIwKSgTklzIaWTirxt253zrc01clCfNVFSdJCrLFj20d0jFghNXWPyHDXDMqGzGjtLeKbRohMBH8GkwHV-jYJHOKIozS0FVsaEAPK2E7ARRhGSYmJPUS0OyuURSugYWHapoDYgQ3OrxYm0WlFCOyhg8cRBQb6RPVoG3ZSwCv01zllm2FhgJlVNiuF_mJkioG-LAi2ug4wktzVe44yWPihQUJNK6GBhdWBBwdJ1h0ULHQHUIiVJRzJGkBXmQS24QoUhhYwooUo8MCy_WDiKmqY_Aix6OR7ySushUN1GDDd8dYC6tpFogNKzTTuTuU8H9QmSCDbuCnN3NWzo9ZE-Z_yQCZquuVXW_z1iOPrOxRTFJ1QGiSeEWepQ7VLfkaqFh753ujs1akvu2UpK6bFZGb6p53sCt7yhhZAzQc-ayzzNNqDdFxwt3XGq9ulzYJVrvLAAQHtGjKvzGHkr4ADCBq9ZkZuLq0VhlsxYJ0Py5AHWiX34BTNn05BSWne7FZSaXpdCAZehJ_mVkwX-WjZdgREZKsSD1dS6pQlw2RRdqDsWcFA9hpqJ4FM4_8u6UaLJQHx61VyuIJOYa7hFU7Y0nIIUY09pkMfTV6pmPZEx7kaKaIJCNasIaA2Q0UB-dOHvppYHv6FQ3cZ_GK_yFdTR7GAGMfZEitZ9erfAw_SHPb80geKF1jQD_3xBGXSc6NVU6pvvcVslrGGqWLJr61Zn4JGRQH6wkWsiWDHmGKEoFxQN514FdK85Q170j_fobXBHM4mP7CioEKpsTPgFXAXLETQ7NJ5GllbPIjpLxkGVnSscR6s3kCpPCJKiMicRMv9BMnTXSHfZIHgVOYbYKqs5zNNG-w4DGUGcdk_9hCYxV4V5dyDUQZYATWJ3csXZuXBVgLDcI68uBT0jY-lbzHPpWFYDiD-WhlK7YfR2Huppkb6CJBA2JbUhJNIavVrHPzUlZ8IT4DYp5VRV3sMHISL6OJ5yp2L5yckDAc1pffko2D8Poo-HnvIPtFkWVBkzbdC3EgK3IKpq4TUo26YiB8y1gmRtaYvccC2lgnpLqb-gpIKpF70NQsPNCOIbV1jVuWJD2Fxeply9oiFjO9aKZMj8lthI-XSAvTluZHWAd1TNb4we_72-U0cFM7sP04iJUhY8CQGzqbL2kWPWB2KHkX7mpDHlAWxWt1Gg1lS-AJkvYW41PDWk2xhJHHNYGsx9UOHq_yTtMkiT1s3fB0cbZGNNdKeb-I5nvoZ9tOaZGHRZbaWvUVWQjnva8QZwDVvAKRLSgQ7Kdwg6zQdqtCSu-PjfbVMSupy7wMNNNWgTuw0ZKH_4gBjiYyErJ8RVhUzVYNzE20V1h0kPfT8RoDi-F8MIANbnuxkVBsMAsKTUVuiK0u4d7D-T4p91qNKmoxhF9csZmgzgOPxOCJFImOCoTED2jRT9wBiPeKYINDo4Ik1DXAowzg-N6cpAY-Zw3paCjwQL8QuDM6wWj0QYumXw6vtSqzPoLJcqxYkQgu8gGJxECEfY1ngBe1sPKf0gjaMau2p76uAuCFulEYFbHv5MqbBmmWxRyzqoeEvWjoFTxPAs9J89SzI6XSDJj8XvqVlPneJ1X_LJOREqhmpa9WAaPcEs1CAeuuyeZ8FgKXyKg8B81PKtpamh_LlSb3VlSTh6qhQlGz0GDxEC6f67VlNMllrKBCOmd5GiZ-TijVwVwDzV9ZRU8rPCfmxIK6q9dV-UXPOcBHRL87vIA8JpJM-DAeH4z1LGuviznDrMSKyUheE8eKp1llohENw3VrX3aZlKAbsQwfhWlJM6SxhM4Hm5_5V2zISpfadiI3B7kPXnSsnR51CYHyI0e_WOCZo7ywp8IoiFzwsrKcBnmgA8_qzgG1ExO8R0AFAzPwXD3wbCKtXfTVArqqBAUn200mQf-95MUBLImsG0NU5nlGVEyyMAlrQccK5qasOVRhFFkcpx1-FQMgCq8Fo5otFjAhPWWDiLHIvfUZw1U3MZpE_Bel0t4tOUWS5uDGg93sa8SP3HMiv-ipTraGXItQkRWMvAJDbkWg0xvGZQsKSee5Wls4_C9aPx-GmoNoNIiGofD9XOBrjBmVWuacdBClhksW-Huv8cEFy2BGjI_cB61fK2Vei5lVonEZ3RFkMfGI7kjfC1ICxzPylaoFW41c1Z4tp-MoAyzgwGeur7Fyo4Z19PEnYCiZp2QVx4-yUoReU0LAkmJPlARyM4fmgOdIGhUz4hFo2B1E3xMvSZdTftIeFdJM493pNIml9ksOxQOIxmYxjBuLCJAdPpMK2ihEJNGHw-RoX2TnUYs1JvVHI_Ew4elScET8FXVti0zf7g8EH7eILYGIYKhw6Tn0LGmdMKMLfHcqZ9Tj_gep1Xl9_GFRPd9Tza7Gr0nUeUVWc2gNRahbdNlCWVHei9avUeL0poCxFUTU6qtWLlYaZ-iaXpypgZAwT2qVbO-1QSD1wovWUY5Rac77qIpgsxZnpf9IvWyqIotau4clZVIIrSgDgh54neVXNAS9SKozICuVaxEIHoxJjRSLaL7t59WeJAqbhgO1yqZPcRAYZAlKYpFv09JfZSDyR1nxFTNuwGLJWNCzEvTKzjNSkIDmiYYgNO6PMSAIK2542V0Ih0FRUErB0kl9nfdQF8jobhBRDfibo71QumaLv0yA9gL_iRiorKviLWo8z0pbsxJBC2uvWBE1g1_GiDSCWnL3mnf34kwScojLblOfYdWLRGdWk_FpntZIziBzm5mEAuG2mGEMsBrdoX3DvPK8d3LJ25iJAg4DV0RHrGExvYgz3N4BY_UEbcizwGkA3yKLvCh4d4Adsx1cIhjJb4MbLmFwmq1FsBv-ILTDLG_ch-WJxiZODJBsddI4QQ07qXmS3VshtlSDVuO-iIB6iy526mQPkykCixEb_AtHF51iCokkdh9cZvXNBFUueBQVCSFuGoaGOyIvJeqvipYZwBXYHhWCEt4Am0wys0Dkr3AJCt_LizBMvTBRNpBxYZGuCeqr2uqveTvpzHBHXhsrHPCjRwdUdK1GNKR25OUJjTXWgbraqLcj_cD3EymDLydF6NgRCTWKgb6ySAOBjHzvEEMj4t9tNipe1wUap0UaRqHecONioh48herbhWSMNiiIF-c5cTTOjnHhkMb_GPnWINbdwM8762kQ9VjswUGs5l49yI0ZBrhvVq_iXCkVgMoV1SHEcVw_9vIoUu9mXFRkgFTv87YhVZvqelkOvO_Zji5mVhcQaXyNkW8RMu_R4dZUhWMWBFmWekEU6_Zg46oh_ZZV9wXJsSJKs5zkjpvrehp9hZBG0Bj9HqCnDBQ45aD1uh9tpXL66gR78CVhuFiKF7OObEaa3xrXHH7RISRulbNMTDJn7VZMobiNJcKHNfbMGKhoVWEDJ07sokhJVlBV7WnceKT3Z-9ri6TM89wgdQlJslzJXuMmIwMvYdTriHrsPyAUKqjnGG4C0kmhHiibuNQZt92sYwMIu4pWURjknp05Ovpr3H9kdHSPeImRDGhFnsdwpQsN6mbca2RACox6OZFANzfspwodVoBV4CGOVZ7ooI66wai3j70aLN2JYs_L0hCh03Q3s7qZyDA5Ku_fqSiet4MgtqnvRJkuUQpshxbmDv2MQTH0JLHZCTWBqXnhF-H-qGhJZx4-mJ2sVCDvgdDsrR2gub53RUAHVabpAzDE7NTJnSJTJDZuVJLRq_ZA1KwqZ-XZfgT75PHbJURdkrpISafcm_LNuEEpkhTMNWKA9T25YThmTaxul8Yq5i_xR8OWRubqq5NjaX1iABeJ6IVA7uPfRlQM4-viPgJ1mmt9ClB9UcGUc59VjMm5XNV5yr5mbVfxbnXd8cyVPWv9G3BkKqKurpNFgVO4RimRcaOUkYErWGRZmgsm6jy82nzVBQNh6MO5ET00PNWSRknumfVlKvf42FITe34Z1tCq0TCky4d06AZoI8JWffdgmOBa6Ek9SduDLRr93RlYzAzfZRXYeL-BKD1S8KsqrbTQ4DchyOtbevGfBN50_yYOyYM-_yf4938BA07FZg)
