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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzYxOGFhNGZkODJjZDY5ZDA4NDE3MjE3OCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijg4ODhmNjgzIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV83ZTMwMTIzZWI2OGYyZWY5ZDU4ZWZjNDEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzMyZjFlYzhkYTRhYTUzMGY2N2E0MWZmYyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrsvXlzHFWWN_xVMjx_TASPJOe-iIh-wgNMjyOg4YVeYqJF2Dczb0o1LlVpKqss1E1H2IDNZmwDBhowW7OYodtLNzQNXvB3YVSS_Nd8hfecu9eilFRVpp6JKJrulkqV9948996zn9_5_SHSatcKkrWP1fJDi4fW1o6FTkyIX-Sxm-Vhktux70SuE8WH5g6lzXzjWF5bpmUbvluuEDcIF-3Ec107DBJ4xvbjlBLXjT0nyUlKnMIL0sjL_CDJsqzIksTLAhjOLxzPDuKCuhGBcfNamTVP0tbGocXf4y_tY22yDDM06DNt-HOdpLQOv_6atmpFjaR1arXoyVpZazasFfh2s7VhpRvWE61ms1hr0bKEZ9ZIdoIsU3ylno9bzf-g8LKdFg640m6vlYuHDy_X2iuddCFrrh7OVmhjtdZYbpPGcuzZh3uebtH_7NTg52OdkraOZc1GSRtAiXarQ_8wd2iFEiRhDP8UYewd4p8coyfZl4C09FhEPdtxPZqGceHSIsmDmBaZ7-DKmq02vtqxeq1BYeVyP-rHPLdwaBbnxCck8OwijIjvFEXGX0es7lhG1spOHV7YxXVmzVZeHlr87e8Piel_fwj2uNkq8Sf-Z5ofS4Hgvz2UNXP6zKGn4Q3kWYCJ82ZWHn7iyaO_PvLQvx878ouHjz189KmHHn38qV89-cjCan5o7kDnhrTbrVraacOGHUtJWSuR9qTVwHXD3-A4UTZkp73SbOEKT9QaOGq5AX9Zhb80yCpuJV_p3KESHoSxDi02OvU6rDtbgd2i_H3TejM7Ad9NaeLnoYfbABvVxpO0eOiJVu0kyTasf2l2Gjlp1WhpFc2W9YSgvXVEEmBOLoHkOVvbGp44ug6f_JO131HwyLQ31nDleBLgVB36w5xeYZKnQUQjOvEV_szafuXbrVOn_-f2e792rM2bV7pvnt754fvtt851z369c-3a9pd3lxo_g3-trXc-37r8EXzPtd1w3o7mXVf8Zefc8933v4G_yH221pr1Wrbx36dO19l04sXWSIv0vJUXZ64dJWHPW23fenPn2s3umZd2PjlXSdt_svq-WkG_IHCLmCT2SDNpZmFtv_fCvfcubl85vfXlJ90PX9387jV48-1bb1k_nroMPK5Ffzz1gdW9dXP7z6_-96nnti99ufXSP7ZvXdm-dfXeqfd27r5oPVUHZgOEuffctc1b38IPD8MmUmvrpbe7Z77dvPV29x-fd8_8o3vh9XunTldQLvLtqHDtZKT3gY3uXvjq3uVTO1-c3rx5aeuDT3auvNB96V3YwYopKV4SPyEjTeksWA888DDN6kAiS7Ivq9nI6AMPwLTqk60_XrfUKQJiW2W7lp3YgEf0yurAxntWliV5GGd-MdLKfgYLOwL8tpHPNxt1EA50udYoLdK2SL5aY7xjwTratvImXK9Gs22tUtKwgIO2O60KaoUkzNzE66UWUGHr6qfbn1yDN-vefX7r3Zv8GO1xzCseqzryduCQKI7HXsHWO1f4l-D8dm9-IQ78WieFO06QT1tbH74AZ776-OS-4xRRnI29nOPHj-PTSw0YmNSt_2h2Wg34_x_PvmGxG2iJr7JPUFuoN8sO-5iJ85pxklBG9C7Sy7witcOxFwlX7N6LL8L9t_p4YjWRopA6th15kyOSNfDPKjlBLUa7pcYTjz_5yyP_8ugjlvXjpVP7-beCdm5hZykI9rHXvnP33c2b73Ox1H3_w-2rl4C5ds-f7V74W_fyl903v7r34jlgs_9z-9zOqXPAgYFnwBd2bpzePn8DvrB1-eWtD56_9-5F9p0qaodOkSQ0GJ_az4LMxc21nrUepfkybVnAdDa_uwm_b739IvB5-etS49n5-Xn1X_jVOl5bbjRbND8OX8aXee0tvWLGE3svdRIEQZiPv-TutZd3Pj1j6ME4effmpZ0Xv-q-8uXWK69svXwKKGk9Rlon8uZ6AyUUMGO475n1b7987FF9rneu_YDvBiy8gtSE-mmW53nPut0FSS7Faq2U6zIbe7DEPR6tYIt24mZOQZyJrOQ3zRb8bdlCYwdk6vXNW593z53pXvyzVWYt0s5W4JBufv8R_8u9P50FcbR587xV53Ph8kBL6H7_7b0PPuT07p59t3vmc35oUCd48SY_1FZJq6ibxnlgh2nfOwEPuvXHnWuf7dx9HwYVs1YTFim722MVRC1inxYkzcddwLwlVKZPrsFjm3c_2H7rXSDD5q1b3Vc-6V47t_XSRaBT986f4AfUDtQhBIMQN-1_br-_1Ji3Nm-dt4BIYMxY3ZdubL19Q_6dqRQVmkQU0yAKoqzvPVzxHnBFDkjLiierzmgUhrlv0wksY95qkXWUfatrbbzj55GKb31jCbPIardIA85qba0taAf2Ua0x3yzmwb7qLK-0QUUFdbd7_ezW-S8rKOdFkZM5md23ZM96CC3f_-zAXtRASrcol8EN2JjPtl67tjcF9zFCBSWdzKNenuUTXBaoznhRL57beufbrVuf7Hz79eZ3r3ZfegfUaLi0yIIvfgG209bLjJ1eu9G981a1GPKcnDi0T1Ucb40gEVCKfvfV1tvfdy--vvOnP8Ox2b780c6p53fefR30OLbZwPW618B0-3jzu1PwXc6ldj75cueHH-A1ti-e3b70V3h069IP3dvPsyc8eOLieTBodk6duffia1sXLsIAm7ff2_r7VzvffA-2y-ady3Bftz_-pvvBhe4__gYjwU3tnvnrzvWzwOkqzg8pXLBwSTZBInDaw5uAggBv2L3w-fbffth-7jbyAD4OzeF24GikTpFTM11i59qXYDjcO3Wxe_UdsH57lj2wd3EcUj8YuKnjLBsNkieZ18Vqr1ArpxnzXs0x4wM_gYmQnbGFLzzwQKXJ5sZBmPZaibCHWx9_B3oCCvwLf7z34oU9ZO3QByruHHVDOyhSZ4xZmbn4lDT9uG3YayiyewYn8SqT2G3cSsnjOZPcev8bZPwZqTh0QUyiJMn8MVaKGjUc9O6Zv3Rvn4JFyQuPh6n7wzs71291L7yNkvyz17ovfdu98BywYLg8W5f_0r18A85FATz5Kp7INXTmtKlVg3W0TpJ69bkjoMYEgd977vwF6yHu2WPkuXB958rprVNXkOmfPdO99v0e-7yPxyt2ndCiiB0_ntiK5IPoEhB-Tu4RoPViHqcAOQW7rk5Ei6IeCxeOXQy-A1X2aETSAIjYt15HLZgfI1Op20tY7fl0lYMP9Ccni-wJLWdeq0ZHHwYRrhxyoAm0m1mzrm5L941zVtZpMWUJFybVAPio4ua4eRFTGmR9y_Ws7mfvbd68qXdllbaW6d6E2_3BKuGeenHuOuH4iwBpDhKix_MEWjlYbcBs15Rmf_EFtI7YTcfbffEcHkfhSwfGfnbr0nVU5y--BM-CcgBHECxsbWDd--rczvUqp15qJ6HthskE3uf9j7eufgYL0Aznb5-gYXzh4ubNz5BNvfYyk22nmSOAe7640_9wi5IShBf8DWX_d2fuvfuZwZ-WGoJBVbyHnxBCY7t_X9y-s8w55H6v1h5PV8mjxPUJ_HdCy-EatdabgVBCp-ZaNrOU2024YvCdjIr7JMh3WNG74nIVdgFaRegOnoOXPobd4KwTPdGfnr_37n_t63Lt8mClSeeFdmZPYBEqHiHjbygHnr_DKb31zhUwOWh2Yq0JBwtomdN6mzAawk8U5TpbUYk3S5zqKmWaBFEeDGVMB132z5jHGpaABj4OZBWwv1wDE_ySmf3KMQzbfxLkd9uqlRULDOyIprFbjL_A7hfPbX14GfjW1rW_88eEC-f653Bz2SlVDG2lWc9py9q-DJbKDeQLN_4qvnztv_hGgCKP11yKBWFgcpZTdddjL7Z92mtgBaBCvXvt3qn3rBXSyJtFoZRr4aLlzr2tyzf3UEkONFDFYfaTPI-LPut0MqvkDoutV17R7FlRfevVt4GOPObDQjwsrMNDP1xA9PnfXnq_e-umdZx7rfcwO2zgEvfhfXpXhPf0wvV7H3y8_dHn906_WX33nNjPXT9278Oq5i30717-CP2cz33fffHW5s2znJqCvwqX2R-vg_WNcuvlN0FKy79d-hb-BhKU_3nz7gfdq39Ets10ctiXnTt_gcHktz-6iIYzU9C7L1-HH_hjoOVv37qw_cUtGHjn2g_dz17cw6JN8zjp94lNhhqcEXZfu7Bz7Rpu0rUftu9ck8emZMH64_B-x1Ebxp8ZO12jrXnSyWu0kVGrbIOYX-XeSRhh885djFVU7G0SFWHhuL17Gy7oYHO9VtBsI6vvoexZuz1TcXtBfIdh6NK-uR3rkQYbRl68vSTh8EeqJs6jwPZTd5yJt__yF2TRf_nEog0Z4uQfbP3xPPfZK4YxX6cnad26d-rlrVf_C-PHX9_avvURY-nfwLfh9m1d_mrrg8-1zctFatW-gWGRJ449ziuIr4K9vfXOx_cun8Igy_ULcEm2X34Jr8dLb8Ov8EL8QgJju_fia3C3uBN3D_-JUySO3-crCFE3g99qjc5BNnf4QxXbG9EgcIKIjjd5986bFtim6GtmDmouEHa-OL311-e4Bxu2ePPuta1L38N9Q-8Ylxh89xmNYIjuy69t33oT5DmTC1VcNsvTyM-dYrxVo4fw2ifb196RjnKMlvboNdzWXiUNDPmIrBnpNtw6_zkwVWExVPDA0A8yn9Axt_chUnZIncVyO6U0WuEmAJ_nQVYk8HffAOU490SGdvs95te8CWdy-9JHGEEZFM_d17_svv8NqEI86AWiukpvizOSuX0RrBD0tsdUPHXvI9r37SrWk2Fa1AC_3e90x3WU97i188mX25_tEZ4vvAAktxOMON-8xc8wdwFrEqNSc_a1rYs3u999oXdA2Mz8OmzeOr_53auCR66CjdSqkXrtdzyzoOJsxVni2n4Wj7hi5h9ngrdF4at1JQvho61XvgdVHNMdzt-q5l9hEmVR4fezV996qM7SRJprG3ufir5vV5yK1A_8II7zEafjnId7M1iMbOBKwF3BGNs7Hyu_BvrPmcbCdSEgh56r-kjFQZLaUZiNuNh5TFIStgk_W9x9ePVT0PVkoA-O16c3tq_c4CdM2-EnQdg2lPGNDIEx4K2bFw3tHJQinkNSZYx7FKwbt4j63iKwnqTz9KD6xy5PVfq4fOJQ2x1zegzWvH0DNNfuxeuozt54HUgJKqLWQZhDo4aXDrYYM8Tunrn3yS0QYDvXT--h9vtp5kSOM-YS5y3DFyW94EwKsbRU6-jD6JPiKgf8wGUP_LC-ssGcmE2hEmVVqWJFkcR5Eo67m90z_9gEsZ9xKcZZFejVTdw-C4VNbXWtTlelM9oq12iGjv7uWVDo3kRWc-csdwllG1XODBD0iR_3OgSjBQtMGWC027ff3vnhdfSl33kDhN0eenfFYxXHL4xCJ3eSYuwVsDQ7K29mHaQKcJeGldM2zTCkRdroNVknpVAzcpZwB19Br8qJRrPSZRq6flbEY6-PO1O45gMPKPaHRGFs5tz398681muxc0YK96d77b09vFIOjYGRBGMvU8pZzgW5cgOmMCpDLPDUvfDH7rm3BdvrvvnV5s33hf_MYoNZh0HcrQJ7xJ9W4bwWNfHjySo1LkyyoD9ONhKVrz3PnQqbt850X7zKjfb9uBayNAttpy9DezQC7tw4zRV1qZNzEcF-6V778N67ZzhZ0Y5555veP5__CIbv-Yj7BsAmQx3y4rnNm692L7x274uXkFVxPf_yX9DzgM6fL3icnVsL1c4D23WSMCX5-BRnroKtT09t_f1VWByQG8zJ7b_e2rx9u5riSQ7GUdGXUzTKClQqImPji1anoWoKaF5rH-NsgOZLjXXgBIvAVFfXOsjImfFRkXAYu6Hjev74NDqCosRqNeu0tHZe_BqEY_fcze5LZ_fQmJ2ckDD0JkcgLBlh9Q3H0o2lBmgxeScTvyClxI9GRcZSA56toFDoxHkexuNzR27uc3uPiWSjSsNiVRro1thDHQyzJEnCfHL0KmvLGAF-FkTvyVqr2UDJompE4OP-shH4qKygluPmoVPQ8TdUmPPv3sL0E8YEUNNivM5qrjdoC1XPnbsXMb640mye4BRlLoR7wBoZg-Qm6fbVlxlTOW8dVyfgeLVF4uehm6ZRr84QL4DFDbZ9xvW702VnjbZkChiKuxbNCfvjHlrEgQaqMmSKLHTSJOtbpWOMvpc2PfDtiunAcA8D109GnI4xiP_mrq13vkG7gSsqcCGyZgc9P2ffvXfpXe7SJ6yYANiYHNnaOvdi9-LrIDy4Jgv7J9Iir5ytUm38kPgBLfrW7FpPGTTfm0gD369yOrhOnBaxM_KUvOgCHYJcP7l4HiQjCs4Lf-TE4REOMyOz-_23YMKBHWKJs5RTjPVtvXOFq_qbt9Ai5-nfKF2vfcjVZ-FZAPtdeK2qrHSaZTEwwr738kDr39exRzr2frmCiJ5ruwX1R5xs660LWy98ZK2RjXoTNE_MoTMjcUYUlRNUOIRVFgLP4bt7p_vKx_ouVjn2oyzL45Bkoy13HpZxhXsGeFQXtkvY7Oc_0nb69pVb9979TL_VxfOw9HvPfwlCViT2X_gKHkZfJMuXO8mqNzORycOGqFCW_ChKsiSORnsFrvnv3P1QqEdX_8iKCP6yc_PPihtvvfLne5f_huf32svdM19yBz2cPeEuefsGc5aSBtjPv6P54ZxiUVcu05bwue-_5aY214DRxwR0Y69esTd27jmRX_SaDcmCBeY5Jv7CrsOd3INjD_l6VRaX69M8s8nIMz5rbT1_pnv27yBrhxQ9YMHDSUedZSQMy-VGRkrXWBKfC0_C_3D5Z5GqYgg3A5aeF73ON8dmq-XURiZx-r29yquGPlHlk_HzOLVjb5x54eKwmAlXC3jkBJUGPEcsEPiro-LgGyVMPGrH0rgtFcpjFc_oma8yJ3zfJ0nftjrOAtyQOoUtFfRHl5mFutJeh2qPR6u5Y1zEeTGRlahAIqtofL373fNAQq7B83LLPSoas6CI0mwyVIHH4GT3-ZAEpzNPN4bQWHgMA7Ky1kRkDnUv39h6_5uKfUyoncdJ3qvHOBiQuXyqe-MCp8HWy3d3ru-VWbHrQ1XnPrAdWuT-mLOjK8jwoqAriEUr4P-VbzYjLRBxhKcGifRONHuq7LEkS_OgGJc2gkGz7-3h1CE0skMajTnhvMVdN6IAiPke4OiyfFnDmSPqsbRvG20FfOD2TZBUm7fuoEJ5XaZDMKco1wX-9Gf4GNgS8OJtrN9mf1-p5XmV0ztLI-L2V8Yd-NXg29u3XuJF5aIwbS8rEU2X3AuCMWdWNuJDYGCVvNIYiELbK2B9YQqXOmlgusrburDUeLLvlHEj8ek5CY1wSKitxzLgxByJgP1FIhvQY06aFyT2A8d1wiCKiiiLQj8s8NI0mm32zjr9gWc16_w3BkbBlFkGVyB_Q7SCpxH2AZN4jRFMKAhjEAYyMSJKRNks2scKuPm0tdaqCTCKMnUW08wvQDOgng1mfJyGCfBO-KiIEo-4CegpmYtJSTTBPKvMh_-AdI6TII6InToOUgrLBxmoBN-vRcd2_gCURoQHhSkQ_tKOFn1v0Y3-j20v2ijbBclR0fNsBI7I4MToT39_36AouOOUIUWskHIFg8ARdbPIC7LMxg1lYxjgEeK4jo36IGZzAlA0ojxMM6pmM4AgxGz3H8Ghpy4SPjKMDZ7Pj7lUpy9vXf2TukrwCXebWDlo8pjXqe3hw9ouAUWG32tDuwTjT6wKtajLX6q1bd86u_23N7o3v7COPPQoTnn5y-2bd7vXz957A97rte4rn7Ccrve0amTWqAvdCa34r9-C74riwkt3t6--3X0DFPsPwaDqvnZh887l4Q4WsSnE91ygfwSsn8hNMXAs5BHYDziFGDG1M2KTwg1TN5cjGngVCuxjOiAUXEEFsdGXGMjyW7gOK3PZLAxMvHyF6f0smm_QX4XXu6df3Pn0DPf5m0l7PL0OpFVfVl7lZkQeTeE6egENqCSdAY0hSHcwvAsxdAgbnHhFHtqpunwGBIYuvR4T14KDAogkQJFH9dLZzZt_RgXg9qnuma_ZhXAXdFlYCeop3J-TtL7BZkHjmakQhhnFuSM3FbKeWjRZUFbyWUXciEfOzdIyNq3HpiXrMoEYlbVaA8OZbTb11qt3uy_d6M01xmwcuPvMHcDrn3TCx_uoeFC8-K9tX30ZHZswZVHL-drYlD6v_Wquoa7DZjLe9MzX9965aqjXF77q3vlr983XRIbAG8IfIl4Nk1f_0n3_Q-WjYBMEOMEvQGy3UA2i1jIsjr8MPPvaWzvn_4EOrHc-Rj7BfL1KFdv64w_bn91Eo5ZxNeuw1WmcaDTXRbXR9rnLW39_1VDRhsd4xAErsozkXpTmoZ_JA2YgmSjuPjo8CUV_Y2ujvYJRaZA_-NvwgkF55m038500CrPEk0sygEw0bzsYIokY3Q5yD14wI17mKj6nQUrE6OOhjcgXCTKbOB7JbDuQUxkAJGKqsZFEGv1_4UJGj5CzLJfdwjRisZkdJ4UDx4CSWC1WA5FoJnYQRBExtuvntufEqR_EihAGyEg_ISaMFrLrv0Af69HHHzryKJvyx7f_Zu3xz4-XnuNfvfScRZ9Zg_eutaWxPfhVi2NqqCf2Gvzt2-Krl8Z9sWH_WtbRn__i8ScfeXiPc1DkcGBBD3VBY5Z7ZYCqiL267-goUivJ7DClTuQlNFW8QAOmiNVMFvkEWS_j35zd4iA8WV4def6gyGt81uLvDXoc5tz8vNbm5VWHU1BvMAbzLBNMRQ0OCU4wPAtRjCk_xmFVejWz7UpRDCOKBKXVZgwus8_QN6yHHea6FMQFNYKmOfWywFfX0oB2EcS9HxgtQjsXWiE-wAOPKk1duKlZSIZ7rzibsbCq4tzpze_PcJ_ELtXXoJ3eugL2effa86II-uxroNXs3Lm2c_1P9965VqnOpXmQ-Uke-FmoNGEDOUbLn4PDv0iFMSMO6IrUdqmSQQYijJjhp4R1kaFTLALnVVz3ZPQXrkP3h3csYoj_netXN79_uZKIeQQcg8JZKjTLNwBiFBEPCPWiBEoWp15h236uRjfQX8ToPwmOS2-iSH-WOjx95zIWvsqSVxmzBV29xn3ovCCXp92LZ1QKBuh2MgEDfuTBd5Y8xZMvROo7HI5XBnMhZNCLoU1gqqIs74D_wWOFi1lf2ZCOPVHSwa4hv-D3Xnxt5-83-DsOhZGQRdq7huIxIVIm1oAMb7D8eW6JV6ikQRjAzgZBHlCl_xmQOD1H52DINmICUEX8OCdukeb6-mmwG3V6JohZs33xLBKDFeRinrfcHWG6loQbvjzDBa7hvXe-gS-D-GCcVGYQZ7wEIW3BRBh-XRUlCN2_vgVG2r1TL9_7RGaSSeN68_Z7O9euoR17_eq9j75Go11iiohvlqBwopeCR0VxC2nWosxZAmJR7DmbB2vRtm990L3-_c4_rnd_eEGeMKOSZOvjF8GUY1y-v9R4Q1wX5k6tPgA0cqPAi92A1RZy54ZG9uk5AKMB84iJ4jy289x1SUjUSTOweqQAnBTUjrRAaFD4iUttavhuNPqOtun_l4DnSJdUlORJ5rqg5WuxqfF0pOJ4H-FwxEJoAvc4iUKbpMqkNRByDJN2TIAbKc39MM9DsJ9J4mgfjcK80frCfiFspHrGKlnzyI8CJeQMVBvT9zMhkBqmMmpHzy-arFyTW6EZxZTdBveAcIVYJJNJvxvy4CtfdC-8LjIRjMjiOqgyRb25rr05jzdoj79mzmrCJ8K_I5UoNpf23yhNl_t28EpcOQu8ZsDDoz04_8YdPTXulTC9PPw9vvvb1kdvsu1AJ7LyB3Vf-Rj5NuilzMkr3TVPSZeXVvjYMLiwXqfVaaGiMREoQXUE7zOQHs58vvPNF2z8UBC8hPcDCdyi6y0Q9tzd9I-_9dkCzPd66d2d69e5K5VvL88c4ZefjRmJMWFz0FwQJUZyTMx6ufA6u4nnMUuKFxkzh9PO3cvbX7669cZnYNqxkeIFCUOASAiojwqKSnQEkQ7EiSqTpoREVo56pseDNtWTPM7wBlhpDNZ4oK6lUou-fan72V_Z_AnO_yvu5UKJuFFKn5eYka2aBRiZIjeQKYeRSIGF9Mnn2-cus1ExWeKBB34Oy2NjWgjQLm8PvuRhuXLY61XcTRiSbTtoT3wfcHdL0LtANwYFh7ZJTtpEFK1wgXjv3de2b17h07Gr-kQfwpJ4HXFG2NxmmYw2FMXymU7evX4btHezVGXr8kfwqqwEEZUHfhZYwbWU67gCl68AeR0FBaZTtkXiBptXqrLwmjz1if0o81aZZlAv5klZ0hb_XewB_MSDKUAE_u5wnXjyMp-W3fgnenBjYP-YncYWr31X_HAyoBmOYMNTsnZOX4Jfd3540zhPu0si349jN0tjEpFC2bUaZEswzp8YM0vqNq7tpwFJ3UgLCwNGSwuL0XCwpOfRzbMs80AWF742YRU0lphlEthWGC5gnhxeJY45k-dOoztguDMeK1VAXXz7RSQji-_gGdW-hXmyjsKGmyF8C0A9qaSoG5Agz4LIDzIl7g1YLUNbHAUZSwZBi8IJHddPnUJ5Rw2wLGUyTADvSkO6sLYVLHbCuY0wQpmdIR4Y4viAwyJcQCoWf5jB2Uh9f7idqg3SnrxH2HSglzRxVLlbu7YKayOrwDrxVXYzPtXyOP89v5slWe5lSioWo8xKFvrgDshKtRQsycIvaBY7ntKiDNywnuNxIPwveaGzOMrCuMjCIFI2hIYEkzbETwftBao6Pvn5290zLzHsra8E97zxPFw95GDcUrtwcfOH95naLdSqktUGsgAozzSFP8pCj5Jnj_JM0-5tLCiA1fKl8uo0fKPP3psXZ1SmmHNuudQ4DvyyNFqTHOZm-nHkPaB-ctO6hwmz3GrkTL17IcLO3dsXuDSo9uQ5Qep5Lo29UAkCA95M7s39hyljBjSPam_eerN7U8SceyAC2K4Kp-rXLwD5catZVjDHguFp5zx-LF3B-MhSQxGNC180-eRec_0QVC0gmCagvsf81ov6VWTF6kouNcDU2rr2d35azMyLKl5sRwW10yLNfSV3DBy2nst2cCg1eaNjz6aRF4Z5qO0ija7W474ZGyBtQ9f9mvW98_xTVnehfDnsrHPXCMxmlANZ3KXCGCc6dUo2OW1krY01xtFO0A01Cj97fVTncpl7apgZ0WirqvKbmzfPYvSFvd2Ppz7YOXWOHyMOMYQavuFW4mp3JcvMbCBmFsR-4KlrY6DB9bPM_aO6Sf3MsbPEc3OXuK723iqgN5lq8lMAtkkTnqRFHALTzhLlcTIw3AyXwahYbBZJUXMynuCHv9KzkAWs7jmJaGHEqhVym-RfPxkCm84WRNb-yivw3a1LPyC4mGHjdc--hjaeAZPAT4jSF0XW0PkroFZXc5MopmEcguhmucacm2ikN60rjwvQJv3CrhvaYR4Vbh5p7qUw22RLl_sGtYYGEG--dVwlKvEMJ17qoVLKkPoiY_8rFKDnXt4-c0Ukn7ADoBKYKulbJL6TpWGY2kViOsoEpttgytd-odhUXpQbRrBbYZ6pW2WgsylG_b8GVE26jWOaAc2AOUSejm0pnLUetWLy8GjA6jsNfqxZYs36CuW5dttXXxb5Qmde3z6PLrid61d3vjxVeQYQT4i6sevTTDmjDZQ1fccOgJgmtS-X4lHygC7K1DVA1Awxsm9INOnhLajng3VPozTROr1CSZMX9SfAPAOr5vZ799670B-FZwzokmS3OgvtpRu6pBCUbVaZiJeVcUgVe63escgGyvpxRn2VEmHgq4mXvw9oadItDQw5JjloW6E6_QaAWs-27hsMTW5sGvpFHqU53CYV-tP4aPJm_URYZ1IMORkcrgwEUahT5DT8mRGvmRCUWb9ejrbD3TPwfjpIIqOvIqRw_Xthv7MP_QURrVdSnAkV9jcQlYgfcfViFwjS4_SviMcR6oGYIMAVFI8wMNWUN-mnwkcznICVJxVYRJikNChCJ9F-QAWg1nNS98ZEk1wtyUBceikhnrp-BkyazGXbL_KZ1PQ8O07jOAhinX1ngKEpUXl_8M12_v4PXhvL8mU4aktfxEjkIKE3QcTZOWYVM-OlZ0nsXCNb4VkJDOGLXUg5KhO0KvJgrBW9IDws1mNNyWwWll3-cX_irXCGM-ZZeYIdmoSp5-Wxp32EBnKbkdQ2OhibPHR5Udgkdm3HuCwan63n0O0NuSZvIFgmUZImYRToig-Nwtajmd5vYDW5pMIPoyQP3EyHew2sNX1ifzL4NPMocuYCRg3fseEnDgtiVJBp98MT-r4TpkHqR74yhw08tp4d3T-0mpKmfkSwnsd1HO0-VGhrYvD7AZymKknyPPALEOqhXoDGUlP7OClYNHSYyO0ZwtAlo-jBl2IH-g6YuDd5aHnAwS2e2nn1c-4f6976FrgXOgk0YAHzsp8T8SQWJEXF68zpnWvfKXdn98VTstxRpO5vff3C1u0LIiNHRnqWW2RtRfIprnKzFclpGcbEzUu4X1deldHwPgtalefLo2zmym7e_mrn0zPoamWXYefuhzAuTzOtPKoRjUEmJ06SOOpSGmBzUn-aIG4cHIaTBGSJyBpD9v3eAw-s7RHkrM7fKHzfC504DALFQQ0MOm2SHAxMTo5upyR13ayIXJ1RrPHlzIKHEYHi1q31lab8G3x1zqLPwP7CxQFTrTFnNVsYDql0_NhpkoLhRGPPtbXjWoHM9Th-Jo0WJ50DQeo4hZ_GQaFEpgEg16eR3AckOJr38AIeLVQ23c6V57rXP8KqHxmcZ6KMBfyrVYGUEmC3xPeo8h4byHIq6fmAEHFSO4x8IH4QZVRLfwM1znR5_L8L_yYlQ5yD4u8Gke8ryWAgwvW4OQ4A7SYFn5t4oZ84aaKLYwy0t_6akJFg2wxDywAvW5S5I0sN3r8dPiVt49NmWgLXEp_K9AecwXy0sojCSYIsBAkKGoNy3BpAceLlDob4JllDGDmJl9HEc5X5bYDA9dNtYmhu0lBJ4P4HRUApSXRBhgJ4k-VTYyC1SWds7MeF59EopIoFGuBt_e85CgobrRfHZDYL_L6_rQ2imBBaxJkTqK01MNu0i-KnB19TJX1OAba5G9BCu7E1HpuWn-PCqKkIe0qLPCyy1FYS1UBWM_Tj_YClSTHt2TnowRQL-hUj1fhp5g26L5Bo3fd_4F4LTI68-imaw--9sHPl03svvsIVIHiKizjEmmJGTeWmZKDNeGAWEqJ97Qa2Wg-R9gOWJuWNF9mFTcPEzpVhaOCn9XShnw4gmixEqSiTpG4URkXsO7nSNAystB7S7Il_pqs8U5dmNLR15N-ARJNs6r7AnImquO-_5T6V7fe_A4nIkyzF0THyA_eQkWGaRxFJucTl7lCNlKa0iZ8K_YzzJbwUMtpWrsAVe6N75owwgGSkr3vjs-4ZFrO58mb34muoiHx0lR9D-PnIE0cx5I0Ri80757fPirClmAXxIyT2jcVC5M35cgXoy-wTxjcxPXUfbh-aBtTPKMEQh-KEGqatR42eHvQaM2i1mbf1ylvdO3_dI3AHx8J3QBnzFYc3UNo0h98f7JrSLGI_iMLQj3VehYHEpmotJwutxpkyspsehzSvh-Rp_0bdSwP0fFanKaAG2LcEYXkVBruifQVMvIQCV8yrD1jFwZByAz6cKBoDvn_-c7SGjz78iNCz2QjMx8_Sz-C8Mg3nMGbDHWYZNJe_AiOh-9K7m3c_2Dp3WqoU5rgYONbeq0vfIwW5A-tZi8OXCC5DV1N-5GEadcG5jc3H40_BPebeIc20GIFEinC_JY41k_3eE1Z5BAOomlJGVBlZFSYGkxwiK6unXgCmYxaotMOQT7IqIENZZ6Vr5dCBjWFYYuNhkfbYk4TY_eyvO998rkfGzEOKhe29I6KvkQd-WV4_XzMOLKbY_O5PMBKyPZaVjf6kYZW9Q_LTwaR95woXF5xXYVUw2DwfmY4rER4_DUv8QccHv7uKRZqYb48j9RwxxjysTDlccVDtmxWpyMw12uMOZR8zwAl0hQoPOV-5TOvnp4U7w3gevyXvCXdYcc-gcnS_z5k_jwZiom8deCZzfVQVEIM65uQuSUNPB_gNOEQDqWG_4IZS-U9tkkUUzKWk0E5JhXeoBd-k0Qu5lDu1eevO9he3tm_eFUOfPSMKWuY7YC4cxh-KGq3nWB4ivRQm5I9gbhqiQX7JAAvqXnzl3qVTOjDCN47rCcLfABqnIeqkk1MEPT7bevvqYJlf98Kn3c--UdlY_MiCnIXjLp4XNT8vv4k6wh4ljSIv8-oPIMO7b5zbvvXC9q0XOdDb5p03t7--Jb93_XtRBd6imJuG-ErSQYiVGVde2LxzefvWR-i7YXK92otpO1GQx3nhxApPx8CONI7VgQEgpQB17MADfTMN0thQDyUmZH8G2sGAHaVaC_ZQ4oIwhXFVmqLGetRh4wkBNhosWUaVe-UmOt1vXgGmI8PB53bJxrb413CzPvhECEsdQfYWDH4qFM3BXEudWSnzZkGxbK9wcACeDSlj1S0N7MM1aontYzJCBiiGsgfEp0Dv2bpwYefuDcZBjbouGeXeS2xxjZ5JGTijr3zeL8TeZzVZfTJq4CEpiNj3o4WeImempvzpz-K-cgyfW-8Kz0Av8AF7PF4wcE7EEeC6gEwYQdOq-_dz_eES0PJaA1EnpkOz4IU1LJkVixKEJYCr6I3PsFGRZxuiSUNXGLvC85JUVM4IweHVVAVRvESKRRdAW9lF9nK5tnn7KxB3aF32wEzyMfFIDwdwE2JSLAXZoERcMsRhNdNxaESJRxyfJrrCQwGdGkznAJilClstCGKb-k6kw88GjKkRcxgVkdRqFhZqWCpeL9ye8HCunG_wsSxzlbWIlVEI34mJb9tO4GbKzDDwTXtc5VVQpSrUSamNnnaaKYZooJdq3_h0gEiBo6gDy6tAMZvw-tkeCb15889ctoqKDXbMDL3hu6969Ab-pevf82oOXhmFeuq1D7feviM-ZNVTlUfT81IvjSklsasc8QY2qnRm7B_mVJrHFIy9KPZE3iL3SWnk034X60ggphrobU6W4Koy2RK-9ShtD-bUgdzAbLz1GggMnAHLh-G7LEMHcdLYqdacoJSVm_Adjqi2xtQQOPmo-anDz_Lz8FqlshaW5gtD3b1P_wHJJNBWf39IdJiEn5QL9tDib9l3nzmEkKjard7zueFW7_tcO-XxD0_W4Lq28kNP_2HuvsGIGh74Y8wDj6yqzymOX2MREXxViWq7zLsaNMiqpM8ziKIqnJMMIRaWLfgNgynVzXsUSqhG0d0vKKnG1ZVhwQq8XgP6Us_0yDM067BqbXkGq8YcBjVt4F-OOuxgpwMNDDmxMQ1EyFHHHABfjhLPzvvbaFeNOQh_bFlWCXcYVE_cYUrgB2aXLVQ1OA0TP476erUebNpdQSoXpbAcBKjkDKVR1UXWTu3Myw-wcUMJ0scOOdAEplu0-xAnqiC_bd8NCycbYyWViJqLQI4NCcfAal1WTLCGChq5jmcXYx-aFuYvoDYjNM0HpXzug5c0tP4qcoVRQUInoWMsalc00EUUMMC3kEpc9tXqtTZoaEUBXyqRchXkcqibJIEdjkcukcmG-v2DmJkiMlG4hLNgC8U3qmiUpK6X0iwfYyXDAU0X4co3161OQ4CB5pj-0mlIacRT8VYqaBQkbhoQn4xHI-mIbRGhtsD5We5QjuWglcjKY6QhSA1M-AXrl3g5assreCobbbDcgLnS-oFFjYYgHXP0gYUbKJ6THtoAhpz00AbK45hDD7ZsMUAOJ71sA8ZPD70HUOD-RzcQ9MzRHetoI6t30NFeazBuLZzC6QZckIJ06u2DnkcDTW-CMw1qGRrXzZzGtR55RkyjCibHfiUD4m2icw32rdBYZeZEfVBl89rfliHWT6tGDvpGBlbZ5CYaVK41NtnkZhnS3dXLgzxNx5hlKOcnyy3KIhmVGpXGKbuPhDRAwfQsHkvCoTqPtjzoKTAwwUYddnA34ijGi7nvMYfS3qhzNu5SpfpfhAFJ-hTIg81bBV2Gmi0oIEBC4LzcHyDRy5huWUERAvaLnbpkPIoMwUSrVMuSPLFJ4Ywx6UHQ1pTizxKYzba3A-RIiQ-iLgnGIwfWxZdlZxXT4FETbDe58m8WyFd1GXXcuEjScIxF7IkSt2ilFJVEGI47mVgWNyyzUXV_iGNnlERj3h8DIQK0Zji6Rx56tIoeGfVcv79P-sFm3R3nbtHqh7mbk0DEoqCsSoun2CCDpOPRQwLoMbS2ZqeNXu-h4rry0ASBF_leMsZSdgPrW7Roq4Wlb6Ab9VfOsXrtZ9ZaVYfGLzIvJsWYh4bNV0WBmDpR0t9e8WDz7AYtuNjncl2rkxrfMxZEYqZpVQ_NwI1pf3fmA1MA_cY5HNZKJ0pox2HghOOw1v2jIi5yrzkKnzr3OlU5UTKSZH7kj3lXOPuc44thHGxPvJLlDlKpQoEpYIP8aByaVSE5LsJK2DpgKFwcBr7Q8z5nYYLVXJV0joIiTvIwGZdmzHOSwk1ltay1coXmVYfIyWOvILE9xrS7glAuWkMxKGk5Z0kQygqC5LmTOva46oqOiK0iVmRGOiU7xar5BQL-L7dIXimmbQds4rzPyDsglfaFnbmo4uCmP67KUouTyHOSeEwqkU67uYoND4AHbiBxYGa-SNBsarhiIQRAiouoe4l3sepkOUFu2-44qk0V2qeulJmzJNbnnKp1qbxqAeyk66Xj0kzc-jnmelfwoeyYgbYOUoPJEdjHDtxCFlKskmhgPGZRNo66dSCQUhRzq6Bn1EC-bdAqmZ7kUez51B6TWmwFAorPInVUktWKUPhsMH95rQFbKjl_ic7gKlNLI6KOajYOiUwoJFM9poFkypib8JDziEubRxcPZPAaSKYTmmXQZ6oBRM0pet1fZIhxe9B3MUBEJzfRoEqhAS_NWVzrMX2IB0EvB8dvdFZTVF4Wf_tbeBz9pzDIoaefrvZSaTTMsSbftVmrRnS8L-MbAIbm-F6f33Dfm9RLRJcR0duLiAbA4UQWsdtJMXD-zHl868laeaJEg0vpk1X3athB8fd6RwMDcJy5d2V4GjnvfgxvINPp4cGcfly6m4SniQd-iUhRZu09rNWDsg0Dlm6ykw2KVg0Id59nMqDhJjvToKGtwdru8zsZqGR6puFwZ_sf1ED7mtygBsyWOehwBK_9D2sAZY0x7KB_WsNPTXK1BpCTOWwfONT-xzMgnEYZb1COx3DrE7K_8YZpklI61EqFu9DkcbwGOmn6gKEqVW6SksCLoxGXMm89inMNuMkoWk1c3WWePQPaZ4H1NcJNraCQgeo0kR00UJbM8fqQmw7ATjVE0ijjDaaQaKwgc7xdcIgOwIw1BNA44w6yXkRfy4LgQOMOO8nKByB8Rn02ODtG-wwj2C5Q0Pf9Mdc0z_IHejxrqwR75YKpTUGKNOi6VZKCGpV37EgzllVBsswtosS3o7FJpi1YlifEbG0kHZy8E4xWPS4LE-yoMnMIeVw-PvGOFoI6JiwR8Kna6lqzZD6xOd53WJBSAypVOZR9L3FyzxubdjrJuVG2MUQF6qLIMpYZcjJ7GdasUvpIo1I8aGimiV5eAy1JjxstAA9k1Sm8GNOsDBghN9aAI5rIHIMvocGGJjLBkIwDhfpzf97AAP65P29goPHcnzcwMGvuzwQGdMz9mcCAZrk_ExjIKnqCHmSVOcsEVjEdnrWDXjoDAcWcrA9V5QD6roYKMccbACA5QLKQBtkwR-zF7TiAVaLRLkYYblD7iIgXEWdfww2TAvXmOjDmdovFMrmPADY3W7FIaWGBRDmH6a4tlkOQ1Tsi0bvZso5UbUKcBXZOvNEWxfAyzI4Dq-jtH4DNQKApUPjbVDg5epT7QbGpQTImsYsGioQebgg2xQFSOI0ycyOF016wHpGhKRi80WzMLzdJ_cApVUat-ZijD4acdJmxMXR1IfMBUsx0gfH4ow9qotQhvlf4I4y-a6Ae0zgIHF1Myx4oba6uFPGyIE2iiSzGXbCO9JVLZy0K6i9eK26bPojO1WEF01Vh6ZySMKPxpAiGbAWvN1tQZUJjREmU2t5EJvZ4ZrT0HYjOcIwyvXXfc0ZDnbl-LO1BJuMGLqhHzqSIw-LUiMq5z7qQOHYLUvSZ4qPOH4DExxI4aQww80-e784arE3-RQX0yQk4XcdPVoYPbVLYkU-DSdFIZhFU0iVJbLs_mDrqnGEfXQbfvlZsHEfEERSbvJwevrvAqumrCBMm1I_6-f_ohOktgK8ij0uzzEtSOpGZUaYcMcvsscC7xrmOJBXqi7ryCbk0941V-QkDh4BdMDFGbRUg5mh9g3cZ6K2ZEeH6SpplNnXjMMgnQzPX1K65ZiORABSd2EIxn1QQjH0rq6xdi10a55E3MZrto-pK4wsYU8LrPVZr1FY7q7BkPrVQ6w5cxKGL9ccef1DE6NL9sQcf1JJ0efuEVv40jMRaZOxWojwkiAnqMnzyS5RvdYLcAa_dWicFFVDhX-PyWtwxBKftkcYyZo0pzp9J3odmJm8HyooXkcXtVsE83YUYNc_TXYhRKD3dhRjV1VOmiC7J7mM8P-kB0RXaU1yFUY09xVUYldhTXIVRdT3FVRhl1lNchVFSPcVVGOXU07ypunR6mudC101PWbLpEuvpLsQoyJ7uQozy7ekuxCj2nvIZ0ZXh012IUUc-3YUYJefTXYhRkT5lNUzXrE_5jOiC9ikbL7rgfboLMQrip0wRXTM_Zc6qy-qnqSfr-vpp23KqBH_KC9FF-1M-ILrSf5qqqq77n-Yx1TX-0zQedNH_FFdhFPhPcRVGhf80z4Wu5p_iKozq_mneVF3JP81zoYv4p3kudMH-FFdhlPNPdUdU6f40nQ26qn-aDjldwT_FVRjV-lNchVGZP023oC7Un-IqjKL8abrOdTn-FFdhlN5P81zoMvtpylRdUj9NOaKL6Kep_eqC-WnuiC6On7L7TVfUT3khuuh-yt5zXZo_3YUYpftTduPr6v4pu990pf90F2JAAkx3IQZ2wJT9TRo_YMpufA0wMO14gkIbmHZcUuESTPmwagSDad8ahW4w3YUY4AdT5qwaG2Ha4UAFnTBtoaeQFaasBmg0hinHJTWCw3QXYmA-TDm2oVEipnxYNa7ElIWeBqSYMkU0ksU0TV4NYjHNVWjMiimrzRrsYspyV6NkTNuiUfAaU16IxuOYsgKgATym6cPUkB3TjMhpZI6pJpsqBI5pxn800sYUV2Egakz5mmgIjmm7QhROx5QpovE8pp0SpXA_pqwna3yQKScSahyRKct9jTcy7YRkhUsyZbmv8Uum7JPROCdTvjUaA2XKJowGT5lysqnGXJmyB0KjtUxb-iqcl2mmgWhgl2kqZhrLZcqbolFgpu2NUdgx0zbqFMzM1DmIBKWZcphK49dMWcpoqJup1toqjJtppnBpFJtpJltqSJtpclMNWjNNj6GGrpmmE0aD00yTFhquZpq00Hg009Q4NDbNNFeh0Wem6ZzTmDNT1QEVqsw0XYQaaGbK8SeNSDNtN7ZCr5my6qWRbqawkKcNfJ3fH1pf2UC8nA7rfMamahZFLUOsOzkZA6NSONJ6boRbayFCVK0hlwCveYgB1cGY2PKu1mwc46B6-GrsL8dq-MJra_RYGIcZcVySOkGYuHFQuEGW55EmQqNTr88hlg8f0PdsJybM1OSfcVwf9rZ0V4wfjSX0hHiff-HNTxFyq2i2LNX_6YjAez4Y-KkG8dlfr_p99obXkDyjDjsIrKrRdSY2pgGUM-qYgwiKGvNmf2MOxeIq4TZkK2yHKYEfWEOPanBJBXIz6rSs-9qTrGWXVcqGqvUN3qWOfcoBxShvCMkajYl2VVXdIQ3gmzEIIr9W8hYnDJlPYpabLV4rMSY1-M2oK2E9154k67IVcUYaCLC-BsQyuhHjHyV-oO5iXAXlpgFxxqAR60SMXFMA8T1orfA-wRqMj8P27Q9u0sDHGXVRrFnxU-3mGsKeMSqpIwU8ua_tIWt_VhTwpRIpV9VDQmPmjEEuDnfHWnew9gKimSbvDMv6nu4DEE_j5oy6EtbA-BcgXVq4XdRahs1DApUrzXWr04C9bIPgyhEQsNOQoN-M5WcrVV0PNZbOGDQSTQ_hFDO82zZIK2u5Q3k3Tw2pWHmMNJyOgYzHEVpbteUVPJWNNkhsYK60fmBRozFyxhx9sKWeRr2Z9NAGjs2khzaQacYcehDD2gCbmfSyDfgYPTRIpEd5p2zV1ls1fz8Y9KPGhDFH721aOLQx94ERLDXoywRnGtQyNKSLOY3b111vIq9koLZMdK5BDE2NymJO5GHDGY1iPS9QrOEsZNjFvFUjB0ZL16grk5toULnWkCqTm2VIUxCFlzLqLEM5P1luUbq6F2q3hkm5j4Q0MFBGbfw6tEOlRjQZddjB3dDgJGN0zzVxp_VdqlT_NRzJqPMy9f8XTcS0n-f9AzOKHRgaG1yzBQVENBssarAu0XGQ65ZVHSw0RMkYFDGA9tebrRNFvbleqZZpRJJRJ2Wa_uMNU4HP2nOWVO-RywlJZCj-6yuIgt2oIIeBUjIGOWpgeZVlZxV4L9ME202u_O-zf5gBUjLqIphm_2_cvKgJBGvDrmDd4Cnz4jREg3ggDny3RRuV_U40cMkY5KEN1k5EgG3D0T3y0KOVaN8aqGTUWZkW_5S0mrW-wqxnOEGmjTpnlVkLQe1F-8IqLV6Dl4xBD_Eo6z5voY-tWQwX15WHRiOYjLqUULCYEhhIAy2tdRQHSCLaajVbJWsd3ddfERkRfWatqueAgWoyzqFh81X2GdC4JaPOEwkKAOcE25cKY5P3Z8f28cy4g5dfq5Ma3zMBsg-maVVnCo1lMgYF0AObw2GtdKIYgCWjThUjER7Grj7YCR77TggOkovPRGM6JEsT0etR-NS516nKiaJBTMa5K5x9zuneyrW2VnB7miUqt8pyB6lUocBoYJNRV5YgzX4lrHG8x6W0zZkzhbeUhKFwcUAukFXN1pzVrq3Cm1TZERrsZCyaMc9JCje1RKuxVq7QvOoQGegmo06LjSgeeODnsFucrQkpwwQPbM5h1bdDNBDBVleMJ8OOVhDEQDwZgyBgB7cJa-_CelZmpFOyU0xlN6YcNm65RfLqNp8a92RkKjlIpSdEZ0zVgpQfINEwkzt4ef9G0x9XZalpLJRxqNTXAvUZ1lKlp6enEAIgxdfIRr1J8hLvYtXJ0vgoI9PM5TSjrHNRu4U7WCcprTO3HHqdkUXPWawVTA1_Im3sr4E_VYlyjZkyDs3ErTe78gHHZMeM9zVhcgT2sQO3EJXDSommEVRGphZTlFUYapW2likskkUHWFdkHXzjYm4V9IwayLeNyj5CBqrKONRiK-DRC1Al6qgkqxWh8Nlg_vJaYw0Dj5xjlOgMrjK1NNLKqGbjkMiEAk3RY4KK_ZBgYoy5CQ85j7hgJ7-DGrwGIsqEZhn0mWqsE3OKXvcXGWLcHvRdDCyTyU00qFJooBJzFtd6TB9i3deXnf3hYfHOaorKy-JvfwuPo_8UBjn09NPVXioNTjLW5Lt2CteYI_dlfANKxBzf6_Mb7nuTeonoMiJ6exHRgBGZyCJ2OykGSog5j289WStPlGhwKX2y6l4NOyj-Xu9oAIOMM_euDE_DfdyP4Q0QDz08mNOPS3eT8DTxwC_hoXDUYEA9WD0o2zCAOiY72ZBmfQqJ4z7PZEBtTHamQUNbY2nc53cywDLMRuOO9cgYXcYN4IvJDWqAWJiDuugCx7bwIw5rQFKMMeygf1oDTExytQZchDmsZz1GTlDVV3P_4xmoD6OMN6RVngJv2Hu8YZqklA61knUlPonxeB7Ha6CThvvxSL32uz2TUAwEh1GWMm89inMNuMkoWk1c3WWePRxH-PcWlhrz1lO4qRUUMiAdJrKDBjKDOZ5vPaRaRx6MnWqAhVHGG0wh0TgJ5niB9aSwhEe8CQbswTjjDrJejWKw_3GHnWTlAxA-oz4bnB2jfYYRDEyDcdY0z5v1mp61VbJhpWC1rVKQIg26bpWkwHwXmp1Ya8IbsCPNWFZV82cNdjAeybQFy_KEmK2NpIOTd4LRqsdlIbwq1nKLrFVmDikQhPGId7QQ1OEcnDEg5FO11bVmyXxic0DLZWYOISmVRl_Z6liDI4xHOxk5wyy5NoaoQF2Ev4OWqDLkhLcX16xS-kijUjxo0ISJXl4DA0GPGy0AD2xgn23Y4DZPeZRpWCPkxhrwBhOZY_AlNGzBRCYYknGg4AjuzxsYMAP35w0M-ID78wYGLMD9mcAo978_Exhl_PdnAqM8X08Qm42S56yyswbGMGWBVNPhWTvopTNK8M3JHGO2g-m7upLeHM-1njJWfLBkIV0Sb47oAUsTraIPZpXowvYRhhvUPnR5-p7DDZMC9eY6MOZ2i8UyuY8ANjdbsUhpNcgqxmbKFXT-wx-zekckejdb1pGqTdDV6iMsat76taMjeKIrs8XyBprz5QocNCagWBvu1WabCidHj3I_KDZ16fokdtEoQNfDJQu4ctTsQUeDo3awFE6jlNxI4bQXrEdkaAoGbzQb88tNUj9wSpVRHz7m6IMhJ13xfdBu5_tJMdNl3OOPPqiJ6trsiXRql6VSBI4upmUb2VF4kNeqU8V0ifb4i3EXrCN4DFEmpC14ZsXiFVN4rbht-iA6V810QEukA1aFpXUB90QIhmwFrzdbUGVCo67ZHn9ij2dGS98BDkhADUbKYEpQG4vkslZtrT1ntZvNOn6QgbIuje1dmYyu6J4IcVicmpT7rgsxarnHnz8AiS8L_tAYYOafPN-dNVib_IsK6JMTcLqOn6wMHxqV3hOhkcwiqKSLrusef86wjy6Db18rNo7DVWIx8zZZBR6AFZJLDVDSqgijy74nQpimcENlzc4e2VNGqff4M6NMAcajfD9AnxariWw0FalY5aeqfEIuzX1jVX5CXQg-EepYBYg5LDLN6qS22lszI8L1lTQzSsInQDPX1K65ZiO0Ek0ntlDMJxUEY9_KKmvXdMH4ZGi2j6orXR1uTAmv91itUVvtrMKS-dRCrTtwEYcu-h57_EERowu5xx58UEvSxdkTWvnTA5XPTpoXJPYDx3XCIIoKYHmhHzLtBkM9JRZm851dDKI5PfBiFP1hThZWmxXROAcv9MYZtONG_ngMUyXJMpVLqB_z3MKhWZwTn5DAs4swIr5TFCiSymbRPlbAjtLWGnDENnuiTJ1FLykKmth-4qdOGqd-kEbAkuIgCRwnSFziFwEYFEXg2A4wgSiKaODDX_MwSUmcs_KXfbwe_v0Q2HLhvB3Nu-EvHWfR9xb98P_Y9qKNXFe_f1L4DgGN-ZBJFRhbFnIvHsqbWXn4iSeP_vrIQ_9-7MgvHj728NGnHnr08ad-9eQjC6u4U_K7kjLHQqSoX-Sxm8HCczv2nch1IlSk2BHhheYrpFxB2RtRN4u8IMts3Dw2Rool0SHzvYjT80_WfkvPy-G3SswGRAV2U9huQgs5m1HpLmb7GUYq2p1yES0FOKR5J2vPy0x7VbVo5S1StJcaP4N_rYdB3Vy0FM1d8fFTwEfgc-WA5CdsTiY9qwztOSUwdP4LmKPt5toavAGOZBSozoEAZg6QHOQv6G2Z4qeHFTPlnopVvHDMUyINtQWxsMd5AnbJ1wdHlc4vt0ASgBQ98tCjaPc2WG7wCbphlbR1spax3EWelEHnSSevUWCmbGUMWIG7fMs2KN6rJb7gMqu5QSubmQTixbn_BP6EWaGw8nqdpM3WrgErsW1x5KdF5vuuy1K_2bYZsAHykPyTNbS2dPfjUIAmEqSukxIvkOMauAEK9aDZLEA8lKUWUWmnVud1zhLjgZUbwk7jMQFr48dTl1nk-cdTH1h8SxasXwEly6VGJsOcpXBAYy0LlhvDs8sr1lN1kp2Ys1Aw1-esh2F4ytwQ3MxCJb1csPSalhpqUS0wb2otDFf07glds1JaYGoYVvgaEXLcDZYIygdYagivOMpezPDDcgk2K5H1NiWMRBtcPLJyYBh2nbTy4am2gsx2CJq6DSySELV9BpSCIDNa5ZTmImOvwE1sYSrcYsXALg2iIg39IFTX2cBT0MWhmOoNWkVL--RZUjcmA5qV31jSAvSqZSc2Bu8sC1QNEXtiLTQt0jTxPKdgOdb8JTUOg1jLQWAVxMDAQGM4-wlNieKQBtKCLlMdGThBWcW7v10G2-4nOYqiWC7CAFXQbzcORoKYKy2cFNYaJlGWyrkM2ASd7TgyCkLWFtE9Wbm0-4s7DsY8M6ync-ViDKQE_eITAj6QJ5tQEsR2lMZRKKc1sBB03uTI0AYq2ImnoOhgff_uVAjtxI-cJI9JkcvlGAAImgrj4BnIi0R9N_WJbSeForgBcaAzfkZGLGBoN-htYAIUvrL7i0ce3Lwi8LPcU-feQDXQLz4GSIEURllGci9K89DP5FQZ3rfML0zd5IEHjoAG3MjnGZ9kUVV4mbZWJhaso-3-U8fJwfl_e4UJHZAH8NvCAw_sviQvCShoStSlrBiBn0INpaDlblX9_e7iF6vsMj-kIBy0-NVYCmJ4HBgPDhew67BtIAOtjGUJ8BQYQ9pVCIswyGzieCSz9Wy57wC_jg22cvz4cfxpqcGzV_6j2Wk14P9_PPuGyCQTdiL7xMB0gi2W9cV9f-E6kR6BXYGNpQbMpBebwcv1MP0kiBJQ_0Mno2qxGgtCi8xOiUe50S-uKujg-rntOWh8xIoOUUgd2468IXSwBv5ZVdk4S40nHn_yl0f-5dFHLOvHS6fG-hfIYz36-ENHHmVT_vj236w9_vnx0nP8q5ee0zUtIvI--FWrttyAE6-e2Gvwt2-Lr14a98WG_WtZR3_-i8effOThPY4BdSOSEwf4LIuCcumjcTv0DSlFiiOehXIdGBDon6C8wfFjjECmN9RBPvxfUEm5cGbfaTKtDpWDEhnGOv654vQ4NA7BNIvdxFenx4D7ECt6FgwzBpr2rATPSOkKOVkDbvys9a-oSurflxrPzs_Pq__Cr9Zxvln5cfj2wzxFSHIwLqkUE39W532qG8CHYAcUB_g38e7C1YU5-T-vtQ-zvx9OQddGhZfnhz5roULBVF3Dl6dURmmj8QnkxzjHkaGZcChlSwJ2jvAdDBufiMQZOfSwuJk8DEXsetROMpd4WhYpNBRB-qMNeJc6k_yG4aLyhXpTrdhV5kbBY6R1AivCUGIiNWqZ9W-_fAxuo8FZ-AsvWEcKlv6HzKfFqpuXUZGQl7DObGTUtrmiIfDzUOGeW2rAJcXwNGxK-aBV780jVJpprQFnF74J_6o4U3kC34kswyZWKY95kKGi6meh0lQI9dMsz_MekbUHrsvuUitPY7-Ik9TPmP-Mq8IaOcaQWogSgGtW6WQi-tJXeg3ipdliyuiKSE4y6qLxIzDafwFbZwhvrFkGQw3tNGGa4a6hZcZSrETwv2-zQQmjcP_BYiSGAlHCtQBtNKtSyaLQTd00CQvQTRRRNZyNIipSdX8oM7uTNwJtOyGuAwqwmssAtBFzzVtHDJknzg2bjZ1JZes0mSrWVjYIhydow2ES6Xu8kE5RQTEWVW3LgRKR0jzTdl3OxgY40oHT2ZovO6mMQbDnuQubW1jwWK0lCvWESQ43AwvdcYAn0fjidXvc04Q_YWYLq-lj3hK03hBkActpwaxaq3dKM-PFSgncJr4aGWScU7SZh__BEwM6SCnXPDwUCiMJ5squc4mqdAf0Lq6_o19KpjxKd1PZmx1T8gXnQGZeD2h4qRZ2V7FdOFXEcZI0TbU-oqGFeg7XfvF-dj9e1I9jx_VJAHq2ur0aXEgdL2TUPI4t7WRhxMq7pSOnnPYPreDNZpcX3TjtOZWEyUkP6-D0YWFWvJH8uUcY9y3JSXaHe7I4202QTVw08SlUjBsTGZstFszBIYFrAXOoN9fwxDPMCT72r2krhRO3Kn1Kq5SVyDB30slmDYMhfW_xFOi7GVWFrrDBNGvRNvwA_yfMVrHPXEEmadmsdzDlFAyfUuXEYkK6uo2GYFgFKYPQAoI0sA42DGNFFWckd8LA82M_K4iyCQ2kpp4zsi_gn90PSBzGbhqlPjA85ccxsJrEVEeMWyPuSUr1XWWclWGNMLOXcfSSOUDgZjMJh46JCjULLoRdBBRe0VWeLQPLqRf2LK_JeJpg8cjPWrVmh8XTSzCPhYd1qeEy4xCNKJKiFxAdvuiJIuKUCm4JBkUqNEqUPh4GOssO0xFZMI5xA4FLsM7eHoZsc4nHTe4c00EavOBc1-PvvsNeZicxxj5IqE1NDSulDe1KTCjpPfHzHBRS23W1kmrARInBhLeMqMwMvqVAEU4uglnLvIhIXxMpntHA63Bzu8KVkQBXSaLQJqky6bEmyw9s2mvSi7WwkYUHzXSgGX6zKnudeLYXukFMfXYthD9UAVdp5WdoqfDud8IFiQwCGd6FqPcwkKtMP-tT3HsqdUV0yeym5AEliVaulTBnCRcVvig7cmwK-kFAAqUGG5BX-qTsH8FKchkSebabRQWvtuUKtga1Mj2tI2JUsR1t1ZaZ2onKxO6vCfczTl3PDkJNcwPHSr_mPmGpxLCJA3zNL0hR2OqeGUhVpnN1ROApjQLVEsbO7i9ZpH7sYllUod0cBjqVfskRwabkxhZRlOcR3DttFBj4U6Y3dUQ4KeaK4g_t_rap7QV5nPtpkGg1WoNN6bfdL3aUHDeMaJqFhVOE6kYYcFKmx3REdChS5zJfyO0KR3GcpkkWgmGQaZeexo8yHcVjwEHJswwvHjgu9XxbvbeBEKVqMkYHfAJ5x0wGHpljjKwiRkJs6hUuMCeiNAcDFsrY3l1RnpT3L83sPCaZZysT0wB-0pnwI-M4tbm6gknF9Y0KJpT5th-kXlQUhaawwnnSr1QJ2yRFPByKKCYe5cF2zrg1kpNOvx8ZmAkvDHO9lFWROiexvSJ3C991lJQ0cJuMMzoqDBMsgbJYEKvTRD8ppmHhg2LxVbpLUeSgHyQYYlCyVmM36QTskaGYmAanlL0Klczz3DDKwtDRKzGwmkw67RN6SclZH3SHNAiDQjEJA43JSNkeFVyJ3zDOs_AirK1V6Z6Rn7tJnAaUEBVwNDCY9IuOB6mkZB4JAz8ivh-paLiBsmQkr40KmoSRPunw2_2twQb2Cj8FddQjOqlCYSoZbz0qRBJCWmjzjocS5JtUHY8UFLHMDXwvU2zdgFQyEspGRUgqab2YB32CtvDXCrMz80BUZ26Ye4pTGBBKBokmgogkLVCbBmkIamfhq40xQJLk-4-BeSS-jS5JeKJKngd4VZ0E1kO0uqhhkQwKjIpypF3TTKEzg7EDsYcisf0oLzI31vq5RkIyFsMEHVFuBnV9-KFsbKBXD85zbQ1Y9T-XwpXRokWVslGEUez7bpalrs5KUJBJ2rbaD5hRhX_KSZwijuwgKQy1X2EmKfeDAQbA1CYeYYB3YWdbOJpR-MsD0qKozmBotq2MS7LUMKyHcgNuxyqY-nukTigdX3jnLe7twcSkpQbzJejAwzxZJ9KjWKXBerCPDnWB-ehwp4ZxMvw7-4RXqsj5IjbINZgoTBSzN4CctH9Zvu7Rh-dUDtBaq9luZs261Db4fZeagPDVz1sP9agGtWVgO-yLjE3OC49yhg5D7nTrLSxnfBRUjjbhOY4DljN_qM9jzSfWbuchDmfhJBZ-ZFQGSkzaF3JyF5eynJyrDEOShrQnrOzzD_cXT_ZlJ_LsCx62rPD9RU5KKLow4kSdDQMTq-ds7IEbVeHhiD0n9p0s4fATXOZo7CuZCQjHtl6ndZXmUugYX09mkeR78ENRUL7d8piyCiW2Xw93WsyDy9c3Z8brhNQqZQLVKkZzQNstmR7HmHbZw3KXGoM8V8RfpBlemo5Y2Bn4mTNmbkTDi7XYxiw1ZPmUEBryxLLji2wS34hFFVgCm-isxU4_80eK3IDj8M3y8Jp6qcPctjvO0-xWmy0jNYy_xZwF5w_ZilD5MaVrlS95qcFFB4t49W5sBV9xnZx6sQv_ow1_A3JMx-paLD9yTu6F1ucHdR_cVcz8xZcwxAjQPedJlDwYNGeoPiJ2ozVvdKwT2MTa7wxnuJRSpU73XGpgcU1ZYwFstofoiWXHjDlqQd1pNpZLudN87SLfj8nVlBqbDmdE3uaeXVcGLn4EdMCUYTbUP5cq6sQDWnNi_bhCXJsKHNVoPa-yaAnYxR4N_TgpVNjFwGbrucT7xEXb_TInmeeDjhLnhY7xGBhsPTEeIwAyp4-jiPywjdBlcZy_PTEsdiHuxtGHOYMUFUnz_FNRl4QPP8o0DRYrmQNT9WSt1WysskpkGWdhQR8-s-EGOkE3egI0soBZRseVBaKzwHRwqUdVZzIJw0057jHWBaGM-fHUZfnyDbiqCz-e-qDKgI4oSXwnDAJlvxnYcz2bWY3Qtvse-imIZOL5WabzLg2MOcmQJSOQCS5mlJ1lG2qpOidk6pwQr9zBwAoSgFaKB1QEZUAhKUARj_MsUeeKBFEe9Eiin0n_BVOeUDXaw2XAsgMF1yMpqmjGE8K3WZmlF0XE9lNYVKStFI2XJ_NCCnVolMadUmlVc74KkmJeyTHu6EVFUflWBGVZSQKsVwS-dLKLhnXh6uiC9USnLR0nPcoaCyCiO22pMdS5IpdlOoBIb_PGZpUNmZAk8ECmkyRWSoMB8qe19f0ix4Ggg3eqzlxII5I7eWAHgat5nML6E3P-hkUFeWAU5MhyOTQIwrpSsqgtz-xogFEF9AEGyOsClhrDqhK43IYBj2vj7xjjQce57BH1AZgZIgs4RLI4po2i7GYxCyB4iYJ3Qyb6Eza7OL5MDmL-TpWvzw0pzcI8jL3UjHwJNMLBygqVKFyvASU2WPlBVRqanUZ57odO4ajxDQxCxeJ_s9JEEdZh0jsDFnmCBUcbXE__jShvaMsXx8Bocw1YYO_fMToKUr7GGDWyzjlBmLmeEghLZEjox7hhyaxRlmUnVLQ6Ldoi1oeVNRXKL-b_5r6bJ5FNdeaNQkA0ko2UadKWnEyfCxCa6CA-rlTDY-nG8TnrOPIa_iOKcwxoyXOhK3lEjQg52azlpSzZKxVyBgiOToPfFJafxJIOsegF9RPGJcTOnqB0rcrpkYGAdWPX54We3CyLirBw3B6ZYoULuuirXitotpHVq-9l6lI8dx4QTfnlQRkIw9ClveJqOA5jRQJzEnoJGOY-8VNtmijUSNnwbph_rmjKY9cCZsyqoWpljy9RZfDUMbcDJBkmbHBJJUx1xYCfYS5-rhLKHB6p6UnJuF6rMzUGx-JWOzcNlhrs5PNMJUwjlxG-3goJbvFLCcJDulKISq691DDZdlVcvPAiNwhS24jPG8CY0snBsgyVdxNVakQtoGusGy6PzbVWFdYYFg-JbAZmlkihhUdbcPYqgRFmcUxyUBF1DC12CthdM8TND8lwpMoKl4ObBonj0ChJlBViQHb2CIaGSKaU2ljJmM_JWl9-W4l8jO0KCmSup4o_LjUMM48nwvUWfHBnQJWek3hxDLZ6kkTK8W9ggepwv0if23f2nKn_8GSUI2x9A1YGUXYG80w0NmB3MfmEsDxeYXXwxJRfMxQCPjx7Gj72YWCW4sh1CRkZYsAbS40Ay8ILoMJKT4oAAUOPm3kV_Diw4XonYMqQTEXmDDxTQRqRqKVzRESWlkpLhMsLJwffRmRti4jNAPThUkMo6Snl0Qb424bVzBglc11uOKBBVBx1n0RhktKgCJ1Eu1EzBHfM-496H_bm7mfcDlHziTEnNNNBNYXIKqsKdO3AcVaZUlXd55GERI6dpUQnBxigrErGm8iNMuVWKVLAMdBEZgViMuO6P6FbXp_dtz0OkphgQAI4hHo7jeeqPM_jQ7RKcjokDtHZHWmnl4Haqt59DCBW5PkgVFol4_Q8SiEMXOA3zU7JYwg6jKyoxp1fIq7RafBLzzWmh4eWne3iTeHyY3CJFZZnBNaXH2LpiubSGjVWqUMIPYkSocb0MFF9hr5p2iKsKEd47tZIWXlTckyTiV3bKXRSWhJlUeHb_TelDwV295vihW4Yg_kcBa4y1wykWuXhZ4wetwbkASbw0Z7cInHS5oGPUa5gCl_JICewjiw1NEpJxYXD8tUojkjohYoxGJi36tA9JEGE1AmT169H_rPzMIDpgddwo8fTIkvjer5vYKWU3OWhrrR0vJgnWj-HDGZtfycYayRBTJCqExf6vhOmQepHvk7EpGBFukXUfwR2wf6scFQ5xIULnflUB3sMUGCVpzg8xMvcqCBEgH8ppZG5s2rcnPu1wy19lZKwWJVxkqTAW_zY1i4dA0ZYbf0j0s01p6IRc0p6K9-m4QITzq_BcHCFjE0ypyjCKA1ddQwN6GHFbCeAIizdxISkXgKS3TWSwjWw8FBJc0CM4EaHJ2szr5Q6iKzgAwcRyUb6RjVoW9YSwOs017lmWyGhQBgVtutFfqK4igE-rIg2Oo7wykKVOU7ymHhhQQKNq6HBhRUBR8cJFhVUzHWHkAgV6RxJWoAVmcQ2IYoUBpawIsXosMBy_cBiqvIYvMjxaOQ7iat0RQM12LDd0dfCcpoFYsMazXTsDjn871QkyKAb2OnNnKXzY9SE2V_SQabyemXV26L1wANreySTVF0QmiRekWepQ3VJvgYq1tb53uisFaFvOyWp62ZF5Ka65h30yp40RlYADVc-66zysFpDVJxw87XGs9ulToLZ7tIBwQEtmvJvzKCkz8ABELn6TA1cX9modLZiQrofFyAOtMlvwCmbtpyCktO12Cyl0jQ6kAw9gb_MTJivstEyrIgISVakns4lVajLBssi7UHfs4IB7DRUzYIZR_7NSg0Wyp3j1jpl_oQc3V1Cq52zJOQQIxr7TLq-Gj3TsegJd3I0U0SSESVYQ8DsBpKDcycP_TSwPf2KBu6zeMV_laYmd2OAsg88pNaz61U2hh-kue15JA-UrDGgn3v8iKsk58oqp1Tf-wpeLX2N0kQT39owv4QHFAfrcRayJYMcYYISgXGA33XgV0rzlBXvSPt-jucEcziY_sSKgQymxM_gqIC6YieGZJPI00rZ5FdIWcnSs6R9ifVm8wRw4RNVSkTiJl7oJ06a6Ar7JA8CpzDLBFVlOZtp0TiCx5BnHJP1Y0uNdTi7OpVrwMsAI7A6uWPpxqJMwFpqEFaRB5-StvGpPHvsU5kIhjOYj1aWYvtxFOZumrmBThI0ILYlJVEVslrNOlcvZcYX4jMg5lmV18UOIyfxMpp4rjruhZMTEobD6vJbsnAQXh8ZP68dZL8osixp0qZ7IQ5kRU5B1XVCqlFXDIRv6ctEzxrT95hDG_OEVHVTXwJJJXIPqpqFB9IxpLbOccuSpCexWL1sWVvGZKZnzZDpMbmN8PEKaWHY0vwI86COyRw_-H1_u5wGbmoHth8HsVJkDBhyQ2bzJc2jBcwuJa_CXW_IC8q8eK1Oo6F0CbxBUt9i59TQVlNMYeR-TSDrcbWDx6us0zRJYg9LNzydnK0RzbVQ3i-i-R7y2bZTWuRhkaW2Fn1FFsJ970vEGUA1r0BkCwoE-yncICu03qqQ0vt9o315zIrrMisD1bR1OB1YaMndf8QARxMRCZm-IjSqZqsG6ibqK8w7yOvpeI6BxXA-GMAG173YSMg2mAaFqiJXxNZXcO_hfp-Ue61GFbkYwi6u2EwQ54FHYrBEikR7BULiB7ToJ-4AxHuFs8GhUUES6hrgUQZwfG9MUgOfs4J0VBS4o18w3DkdYDTqoEXRL4fXWpdRH3HIcsxYkQgu8gGJxECEfo13gCe1sPSf0nDaMa22J7-uAuCFulEYFbHv5MqaBm6WxRyzqoeEvWjoFWeeBJ6T5qlnR0qkGTD5vfQrKbO9T6r6WcYjJVDNWl-uAnq5JZqFAtbdkMX5zAUukVF5DJrfVNS19Hks15rcWlFFHiqHClnNUoP5Qzh_rtdWUSWXvoIK7pzlaZj4OaFUO3MNNH-lFT2u8JyYEQvirl5X6Rc99wAfEfXu8ALymkgy4cN4fdDXs6qtLmYMsxQrxiN5ThxLnmaZiYY3DNetbdlVUoJsxDR8ZKYlzZDGEjofdH5mX7EhK01q24ncHPg-WNGxNnpUEwJlR47eWOCJozyxp0IpiFywsrKcBnmgHc-q54DaiQn2EVDOwAwsVw8sm0hLF91aQGeVIONku8k46D-XPDmABZF1YYiKPM-JjEnmJmEl6JjB3JQ5h8qNIpPjtMGvfABE4bWgV7PFHCakJ20QMRa5tT5nmOomRpPw_yJX2rskp0jSHMx40Jt9jfiRe07kFz3ZydaQtggVUcHIK9DlVgQ6vGE0W1BIOk_V2sLgf9b6l2GoOYhGg2gYCt_PhXONPqNS85yTDqLUcM4Cf-9VPjhjGYyI8ZH7oPVrpYxrMbVKFC6jOYJHTDyiK9L3gpTA8Yx4pSrBViNXlWfL6TjKAHM48JnrGyzdqGEdffgRGErGKVnG8YMsFaFXlRCwpFgTJYHczKE54DmSRvmMuAcadgfR98RL0tWU37QHBTfTeHc6TGKp_ZJDcQeisVkM48YiAmSHz6ScNgoRSdThMD7a59l50GKFSf3eSLxMeLsUHBF_RZ3bIsO3-wPBxy1iSyDCGSpMeg49S1onTO8C353KGfW4_0pqdZ4ff1hkz_dks6vxaxJ1XpHVHFpDEeoSXbZQlpT3rPVL5Di9IWAsBRG5-qqUi6XGGbKmF2dqwCXMg1ol23utEEi58Kx1lGNUmvM-qDzYrMRZyT9SL5sqyaLW7jmSMiiEWpQBQQ9nncVXNAS9CKozICsVaxEIHuyQGiEWUXzbf1Z7gihsGg7UKos-xUVgkCXIiUW8TXN_FYHIH2TJV0y5AY0lY07PStArO89IQQKaJxqC0OgfY0AQVnR42Z0Jh0FRUEpB00l9HfdQDWR0NYjIBvzV0V4oXbPEXwZAe4H_hA9U5lXxEjUeZ6WteYmghblXLImawS-jRxpBLbl5zat7cSYJOcR5tynPMOtFojOryfg0j2skZ-C5zUxCgXBdzFAGWI7u0LphnnneO7k82xiJghMGpoj2WMNiehFnuL4DyuoJ2pB3gdMAvkWWeVLw7gA7Zjm4RDCS3wYzXMLgNFvLoDf8TkiHeV64D8sThU2cGMDZ6qRxghp6UvMk61shtlSDVuO-CId6iy536mQPlSkCjREL_AtHJ51iCIkkdh9cZnVngioTPIqKhBA3DUPDHJFNifqzomUEcA22R7mghDXAJpOHWSDyV5gEhe_lRRimXpgoHchoWKRzgvqytvpz3k46c9yQ18oKB_zokQEVVasRDakdeXlCY411oFob9VakH7g_kVL4clKEjh2RUKMY6JZFGghk5L5DDI2If7fZqHhdF2icFmkYhXrDjcZEPXgK1d2FpI82KIgX5zlxNM6O0XBI43-M3DWIVTfw-85qGkQ-FntwEKu5Vw5yZYYB7pvZqzhXSgWgckV2CHEc14-9PIrUuxmNigyQ6n12G1K5qa6X5XD2PdvRycyqAZHG1xi5i5DZR4drUxWGWRBkWeoFUazLg41WQ_otq_oFybEiSrOc5I6b63wa3UJII2iM3gfoMQMFThloveZHW4mcvjzBHnxJGC6W7MXMI5uT6rfGNYdftAuJa-UsEpMsWLslU6jTxgLhwwp75gxUtCq3gRMndlGkJCuoyvY0Oh7p_dm7bZHkeZ4bpC4hSZYr3mt0MjLwEkZtR9Sj_wGhUEA9xXATkE4K9UDpxKWOuO2mHRtA2FW0isIg9-zM0d5fo_-RUdE9YhMj6dCKPI_hShca1M3oa2RACozanEigmxv6U4UMK0Ar8BDHKk-0U0d1MOqtY68GS3ei2POyNEToNF3NrDoTGSpHZf-diuR5Owhim_pOlOkUpcB2aGHu0M8YFENPEJvdUBOYmid-EW6PipJ0ZuGD2slSBfIeCM3e3AGa674rAjqoMkwfgCJmp07uFJkisdFRSXqv2gNes6qYlWf7EeyTx7tLiLwk1UhJh9yb8s24QimCFMw0YoD1PbFhuGZNzG6XyirGL_FHQ5fGw9WXJ8fC-sQALhLeC4Hcx7-NqBjG10U_AnWba30CUH1RwZRzm1WMyU-5yvOUdc1ar-LV6rrimQt7Vvo3YMhUeF1dJ4sCp3CNVCKjo5QRgSuYZ1mqCybqPLzaYlWDgTD04d6IGhoeakmjJPfM_DIVe3xopYk1vwxraN0oGNLpQ9p1A7QRbqu-PhgmuBZaUo_S9mCJRn91BiYzw3dZBjb2NxCpRwp-VYWVlhq8E4Js39KL_yTwpvs3cUgc9Ok_IJmYxGNdoFheH_6k4pGHFn_LvvvMIeyXpYPOPZ8bQee-z3XIGv_wZA2uRis_9PQf5u5bxykjKH2MoRogm-uLFuPXWNYAvqpsC7fMK1TRgS_o8wx23xIxt8VGp16HZQtexTpaqeamSZK6YZT29D97kqPVwVlhyTBV_eeAWw9-u6pTHFhEnmNno873rPX_4bZwDzOYjAJBvt_F_BCyG8O_JhT4qka_GXEKmvR1gjvAyn7FCx6wYkUAxKH3WaZ-MfC9DG8nR1GQIB3ojqnXhvSQ4_Uhu-1V3yrg1uLDR3KGvQysrdOa_09JJ7O9Q2d1lbS0pp9JTVm5DhDpZmG3HfsJZzV2437P-rSx4b8_tL6CTfVkJBIFQQ3jb2onhVeXMbV5nivG0FLgurKOV1YJ3As71AnOJDvVHeMmNL5BX3vAiIKp5noUFKPCpWDOBzEtMt9R74rXd-4Qr04y2-DJz_gpmd3u_0W3u-8IhHEIC3RJ6gRh4sYBZpjkeZQPaaHo_WF4S8SfpCUkfJEGLva6ckiSO2EcJUniUje1Y-qF8Ic8YW62yHFiNyxoVHhFXHhOATo_gTfb5X2G9IAMokVnWA_IGP6B0bxZD8hZD8j_d3tARl7o2G4AZz_WKBeaF2tLd1_cVcLSuLYdx26c-ZnyCxgMV8Xgx2Ghpsvs_8IA_85SoljsUQQciFHowLOYS50wsSCCcC3a049goLkATMdBc3COXzQRJKqOtjgZwOBn-LfMg7PKcSaUIaKYr8yJsPSLNWQ0e8O0I_hkCywMvrZbt7nBTnNmcFZM8hu0PJk1rjCYBAlwjsdZKhAHmuoHGRS4dhIESSFbSZTBhcoAI-a3uklqe44-AoZkE0dgHFkFH4lbykGTUPyJYiB1KWfNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT2fNT___jV5-Onr56ejlp6OXn45efjp6-eno5aejl5-OXn46evnp0L38NLYWAARaqh8)
