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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzYxODgxNjFiZTUwYmFiZWJmNjA2MjM0NSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImYyNzBhNzMxIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81MjVjNTAxM2VmYWFmZTZiZjNkYjBlYzciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2YzNTJiM2NhZjgwMzJlYjZkOTU1OGRhNCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1fetuHMmV5qskND8M9BapvF_UgAe01LYF9G0k2cZgaFCREZFkDqsyazKzyKZbDRjzYx9gYcyv2ZfY3_s0_SR7zolrFqkkVcU1ZFuqysw4eeLEuZ-vfn7BhqltGJ8uWvHi1Yvt9iKPyjLKo1pmYc1qWTd5mMdJmr1Yvah7cXch2ks5TnDteMXiLH_FmryQQkaiFE2aFmEUNyxNWV6KMGriOMo5PIZXMo2ijGeMNVlepZEs65QlmYgLeK5oR97fyOHuxauf8R_TxcQuYYU1m3CpFfyllmv44M9yaJuW1WsZDPKmHdu-C67g-n64C-q74Meh75vtIMcR7tkyfs0uJb7U7OOh_3cJr7sb8IFX07QdX718edlOV7v6lPebl_xKdpu2u5xYd1km4cvZ3YP8j10Lf7_YjXK44H03yg54MQ07-cvqxZVkyMQmLkJWJNEL9cmFvKGLgLnyIouBCWGUyAY4IfO6SUQdSo5c2PbDhK92sW47CZSbHVlfNEkW1wlnTRkmsaxzUWVZKViqXkdTd8HZdtyt4YVjpJP3gxhfvPq3n1_o5X9-AbvcDyP-TX0txUUNLP-3F3zNdkK--Cu8ghEHWFn0fHz547u3fz57_a8XZ9-_uXjz9v3rb394_6d335xuxIvVF4kOm6ahrXcT7NhFzcZ2ROazoUPC4TvYZkmP3E1X_YAkXrcdPnW8g2828E3HNriXmtTVixHuhIe9eNXt1msgnF_Bfkn1xvW659dwcS2rVORJApfDVk3yJ3ytH4f2hvG74Hf9rhNsaOUYNP0Q_Ki5H5wZDqwMDUwIIm6LMidv4ZN_Cp76FBSa6W6LpKMsgFy9-GXlKKxEnRWykM9O4W-D9xObduOr4M9RAEIidnw6qdUD7wJca4AnnHe_hT_BGzhnr4I4jPOTsDiJ4_POUb1lA5uRnFVVHedFPSP5HbxbMMFRDJp2GJd590_B_asXWASnRCZRyA9d71PwLzsQL1QVn5AZrBtv5RB8Ou8-nZyc0H_hr8Fr1gUMtApvty2cl6Dtxq3kHm3E-xllnEWNrLLkUMr-NEq4ElXZOAV9o-6CU7fbIAG3oIcCftX3I3AESNv265bfrQKQc7FuFzYoKXkcFlU-I-ubnySH03cjAwGvSCdneY8evGFhm7IsbkpWhUes6tQ3cAGEvuunoN61axG00whCrE7FphdyHbABZRnY8uvf_xsM0SB__fv_XuBJkYZFE4fVEdSB6HRSijHou_UdbC7cNoC6HV8tLCtRAaUVO2LZ6DT46qs3EvTeIANjIoAGLr_66pX-oF23010AwsMCEHR-fRco1ewoW4ORnMtuJfKSp80RlP0WCDsDm9aJE2JJLS_h0ARsCpjYtKSdT4O3k9vLjYQzBlZq2g0LPMtZzuMqmfMMuPABT0p7eYXP6Sa2VoLwiBQv3bckzGEWsaIsj6cB7-hBgpXU3rIxmPo-4HC3HKSAfQy2uxoONkMFtSRKAvynpij58SR9_PgRbz_v4Mlw_b_3u6GD___1f_6vgE5SoC-lT9A1W_fjjj4mz6ntHZUc1ppTmfCkqcP8eCrhuIGPBeLUBcbP0CpwiUtFLqMwLJJn5FJw7z8bdi0DYt559-MP7z6c_e7bb4Lg13_8_Sl_FpgXNyGvwYd6FqkD2zJO6D8bgweKEkwK7COdR-M1r-G0_zPozhWdULqmBxMzLh3QqKkqmT0Djz-BT4M7Cob5WykugchaXrGbFpydT8HvW9Bz7t-eudYme8k0Z-AhZ7l4BhrfdsDG9RptsGefNjsw2cgxcFj7DRxeEAZQgSQZEiOZ4Ds2XC8wkcm05kKIGYHxqeGD1aCB8dkeUXSP3Lqg68Iq5lHDomehBPl72w_XyC6MFoEjyttkbReMfGATv4LPQPm1wPweNzxgSBX4P0vcqkuRhXm9R2MUvO34GuIB8BA6cqXWWozuwII1bLd-xBNFvj3tIUsOapnCZbV4XuJOgjNP84FI0R7gYzD0DBjncjuhBRngQ7C5ELpu1xI_ma4W7H5RyqzICr5HbAz-nia2GfrNobx86mOWxLHIc5GG8rkJPAnesVu0YZvthDpRWI4FOpQMICTqQEZbuOD0vDsJXl-h1KJjvsDQpCgiHvFwj94keI3Jgf_YgZoBUT8ZpLKd4AANLYn_49x80jMWWBnxRCaCi2cl7Sxw149X_Q58mxpDGJVQUM4xhS6gEFVQg6YI1hfttBS0RIJFcs_rO5ZWrfBFO-ib4P8lGDwBWz60_W5EusZWyIHcL9j0mDxWdNOWnGfWxBC2M_6sxL4jFoILD48E51tqPgOxijq2lspIM09QNYcXGFuWuUyze-fpOFrR9df04kE00YKiDz-BpVBlKbZ-9dViiBSXWV7PI7PkFMgDV6XtbhiQ0lEaZcn8PXjDwtGQcR5mTR0dsSoFZu9VuGXiMgzJMGmpzOaEm6c194g7xcyFS7IF9jjL0vl-pUCZyu4FmPXUAZ9SYnBN91jC5Sn3L3CLyaYpo7R8PprOAp2txKiVdLnKef5mhKO5bk60ywD8syHvINH1mtF6P0gqWJ0B__YInZtiZtd-uml74jOWMn1wUcSL8FlJO7G5wODtm5VNEYGVm3rer43wrdS27IYBE0tIHdq3BSGMRVNKmfE9YuPgOyCo3a7ZHYi43ZmNHC7l4xx85O4lQ1YnpYij_JnI-RHEZr2GcJz3W0yuKh0ajGwjnceFjqsOftGCNI0k5i0IXx1WeRjn1TNR-QGDtQb0EeyeutplUuZRh_xpS0QOrEHXJtiyBSrTijFZhvu8TPb8q8MOyROfsqSYqzhl8N9nJk95f56Dt3Lun_YJV-RK93BqMDUulQtIqfiFg9KEDZjXPN4jNw3eteM1SRaEl3LCcOhJmhqZuHzzYiCS5CEPn4kYW24wqQI_lMOUFr-S_Hrbtx3yDp48McXDWXbtfiiXFSK7r1oOJPK3lBzV1-PDXHRg1B2FofbkwGbfgNGZwO4s1TjCQtZl3DwPkW8bc5XLG9TaagJ_px4LD-z2xOqeK2CvHNCbWtI3aZmUYSrn7n12GvwwgGRglQcrBX3TGK9RJfcoKRRsHnEYnvoYxq_ASi-LZVoJUTZ7EdJz0PkXCjNUPAzK73J0DpanyEE---D9mvFrFE5wIMQYLIYi6DGHcK6fnV4vf8RZhzcPco3V7Lvguutvl_KaUZmKOC3jZ6fpJPjLFcgfn3ZkSjg4ENcUH3XkI8C3Eg7TQCeqwYwcxkb9VoJrduqXCe_7sbUoq_2syHNQjBGddXAmYyTdCQdrACIZfDTGG4vcH1fBx0dcx6po8iaK5xzOT13Vdd02kt_x9SOeTvC5exZOCJi8PM9jubd2FHzT0WOMUD9mOx6-ZWlhUWRhWsfHLEyXoib0a1FNb0RmAIU3tRty9FmHvgqIGOhfOp9L-wEOs6ii8BjSzhoMxaQhsJ1IpUIgIRmGZvBcoG9DQSqSh-U9dDCAdrnkQpVRU0XpXvCYg6MHITXYhN2XbNjDNy1sWSGzLMoKedziSnXCn0u0SsYVGqkCrvtqXKpxRI0wIePQ9q8WOMNFXaQiao4jLsI4fLPdUWpuA3F4ywPd3uHMO6yNpANZM2O_oJHyNOMpk0du22s2gqqk0GCn0oYYW-06m5Cd5AaegxpO119ET3ppWf1kJWc83qsH5OD3fmeLTY8L097VSwefVyIs72m7py730ZXAPlJZd7EK3iQZmK4oO3CxE0rimR021QVr3-FEr_sOE8GcDdQs43kBC-JQ8ioOU14eSNUHbNYgpdGSgRwkBmNADSiPgVHBVMeVWzZOp0v1tKrgRZPua7o0eL2mgnm_vXt86_euXtj6Os3SrCzFgcudKaWAwQDoDsycSlQkvTHrOi47aQYp6WEmYIM9WdKpWVWHRc4PpOqEDjHD_gPKQPs6wfjZGAiQT_PGuAp8zdrNcnZfgoMdN8UeWVnwTp7ILzXOn7lrMfGRskiG8ZHLm6v3rTR1jICqkitnlylGbilvi91SmyWnNK15VETRkdSdBN9gh2Lw9g3EjyZdugpUt-IKDhYb1QegZ3udVeX9DsLOoFkKzZuqFFV-7Nah7mnRPFLBWJU9tpK3je7ZCFDQ_yZHk_ZGS6K-kEtddAzsZJWW82RRcQrKp0PzIkWrq1Re4-Qjjufjdy9IWl7kkYiq5rnooeYg18wG8Q445pPkk6pWtqrIoqy6oKKLDokgElrMseVxypvyucgkPwh3bp4l2FCdmnZUp5mQZ6tgFsEt7W4kS1Ad2XORiSaQTffTGtwovV1nK3DaU9LRW8uXqsF5XvGs4ulz0fl7451RqMjALoNqaf29XYxyec3zMNrr1z2KbRjcbphQfZaKMyas7bzPXADcc2LwI8FtGEdVXjPxXISe6cNBaoOUoS6tuvh23ffXEE9eyyUGVgKCg2avT-IIumwTFBH1yhOzC3zWhaJaivPuFuTzFQUSu4nyB-C3L7Q6lXEexUn6fAxEYxEM_Rr9bdgtUG-7drzCZkTwH8Zp0T2NBIP4O3l2puGwADW2X9R3551qwtb_wIfqv3q9-Ocd3LvAtTwqhcjLZ9N-3zDQcmRnseULPCfpKvbeI4Kajct9rmXOq6rKxbOzcGwvsQj4CYzpTTv0HRoTOy8AH--PEMBH4wIDszpPwprzZ6NT0fcRPSksTg43On_AgmY3YQzAh7vt1F8ObAuqOMDLKRMBDsWSYxWLPGrks0kk-jCK0pO2I_99pTR0f9vh35FgSgQMu47oQ814hQpns1tKQIs8ruti7sOUVETXDRerYNxtwaNTDTbKhQPlCiLXPuLMPPUxj_k1dcPzqK74Ho2R9_THHPd7Vy8sByF8nsVpdeByNi2DZ3JFeTPaHWulyO9FabuFw3AJnKD-a2oaWfKa0pylmWz2qIqD9x5bH2fDveuXEgxxVNZNGR28pE7uYzPMekd5FuwWRKdHNVhoN2cFJ0xSDAqR-K0OH5aCbcl5CTp0j64EogInT4_wYX7xAhOSOIwbmR64mObAKCkeu8FEwt26Z4J0tWkg3-5V6VZK9Sy1SHMuypzxw4g6CX7A0p8qnGMSAGztem3rgqg4-qG9bLGjHJ9N3tY7uelvkDmf96jSoqh4VRaHUfW2IbeJlidX5TfAoZ9gDdlxabzPWtqCPrjyquLfyKUKWyiSqEibuRtfUVyMrYfwYBDkRxTZA5cvddrEqRQ8ZAev-Cl43046AP0U_O6h9mmcdsLeUpOwvInBZK3X_e0YLLVUxxz0mmjmaaooPA2-MakDnJDpu5PLnq0f48rSfUv5kFSUdVgmx9NwEpzpktOf3oJkkIutGrfJMOrilEoXuRGIcQJlsxmXIoM0TVm1t4FRdApyjI6o1GxnKJfosjzKqOVbl5VP2ZSieRZKbEULU0JYw96ycbTetXYZ6SmGmYNaZXE6imdNUfPn4RXctlfu2a9H3UQrZVud3O-2AlP0C_tZyVCUlZgb9CgGX6zt2s1uY96Tukja8bHi4PKdS5KfhZFsRPocdGBuZl6LVoML_qgN5tLv0P5ik4fuv8M4ZSmOqngtsuZZWOWPjenLlySJMVmEuSyeY-mT4EOvX1ZrBO19UeIKP_GTBCfB-wldsaAV2Em7lErmdcHi_bGZw2j8QCkWtLF6tHc2zgL-4RKz0GUXSZY9ByE2UHuNg6pqLhHbv23PgGvDGK2vAmx7tydMKlL768oMq7_QeeAL5d3hlfSNGTVfHKQHoaEXd1V46i31GpYIHmCglXB83PwLp8f_ioP42EbpPcEfzvceQmP_B87tj30zXcAWXsphO7QaHmCso1cFj0OZiwhOUpqXdcVEGcWFqLM0ZE2V16WMYlZLEYo4q5M6DxvwUQr4b5MwVkpM_WDdkcb81X69isL0F-A0jtzbGe_8Q5S8SstXUfQ_wvBViFZds9wHMPjF-_Tn_2_YACSYanIfXNsrjNMLGfMiyTgPkVn0DG-YX8vs0VP4erU4SgQrZJqkjV3NG8zXqx05UU8fvwfHGT7fG2hcmUkWO2u1snln11oNQfDUb7dAOz7JM24r0N6UFxBD20zY2GhCzZc2SFYx8wYPOCUQjCt5qgn7YUejBKOiDxtoTi4H1YB99vpb7OvrULqDa3mHsxM3LcfQa6MaW-UJ24kWXW2izM2zGn8JX_CShgywCQ6_MC-uInn4ilpEOLihrO71NMYDKkxvWJHkURhnDfg3odkwD5bAiMcTgQb0Q1kchmUZlzzlkXmohz2gH3ocmoBfUvhneMC_wg4EH1DFaVMz4IySkV6VRB9d1HIaKOd9kLNBJpqMn6SulFF-SfeU4xrf96tg163R0uteOVPrw0kdHPag2tVGNcrZuQVbutGBpV6bXkz3f2JxV83-YDu1XuwUjokS05kDxpoG3n-05Quk26TIdBd2tzaL_AUtLdl_2_msWYBr_IAFXiVl2k7DdWt4eXEX6BEBM3E37kANt1gUUTwHbj84NqpFAHOrcVWHSeREwAN50CJwDGwDfKRPaT9g6hfNKF3XuUO5IPhlkdYNT9M4TipDoAf34AT_qegN-rlNmFdZHUc1SzJ7oBygg8UlOQ6fIVC66DQADg7jecdN3w12GyIXUOBRGOHeyyvVs7kK5Ia161XwBh6vkmG9ci76fg3b6Wg67yxRGqUHuT9TRnI7D_VsCyJKY-tcTkzWo6qiricsWlmXhpnwEOMc2SnZpSFMeOwtwzz-wvaFeZPzMAnBZbHb5yFTaDZ_CdCEtWA8yquaCV5ZC-ZhT7j554OhJDxjRf2aNBc_3rZYJ1UNc_AX2mg1RWfnw0ZwJjlK4voOV9GOtQvCzHiUHhxyI2m0gpHe0R8t0337sxmz8y6hRUF_qu5pCmu02sWFWXeH9Q380mS4UdnO5j1wGFl1ZNPiqFJItLX2-Bp0IXhU3T6iBbYRCkU00JGqubB-izqalrcvD1rsgdjUqEa_uuvUI1HiqcivvXqq7jnqbUYOls9w-e8pTAFqZXAJtOPa4xWI8a5T8BtKZHedqR_QW5sWO7Q4qKNIRcHiuw6PQIdjiMqrh3e-3GEGF18E--k7DNFPH4h9jHrhnImkqEWecqtXHQCJdbAOxxPRJxpUMaoROOHwr4fnDjVJSZXJSjYyljEzJHnII06TfiGCiH48l6zgaS7huDuF6kBF9OOPBgfRq-UZD1mUMB661Ty8EL3a0bgf3f43yr1zT1A-weeqmMbIVllRFYXMIy4tsQ42xCnBL4D_MGowFWC7yzrNSssHDxFknw_PjOzx2T_AnuDbH16ffUtL_vpf_yd45D-__uM_1aX_-E_XmKV7lu5fGrSXXa8VBf7zsYf_1__Vl_7j2Bd76E8QvP3D9z-8--bNI2Ig44IJFlVwDhOzVx4AijshRwKZkKkZUWHc4tcL0hPJMof4EjzA1EqPh3ViA4BjMEuCj2qzxEe4-o1qDDYazLjDWg1_cqMS9gSoR-i-20_BH_W7D-gjgaoEr_cP7fSSvn9Zg_eELowaqfhEA3DkvJg22a53ToAJN9UC5mNc48wEBJR_0YUnNy9pcisPPJ-p-op99ILjLZsyTmRY8ZglLqCzEC6a9cdAsQi0YDj_gz18PPjjh-_gNHqaRWemdA5ZB0q2Lu5FTEL5T8pcK41ELtTqvINDirVN2JTx68-OgbcdyG6rOuDa6aqHwJuNqqP5EjZxwXusRcbTSmQpp0YLYpIHI-NM1pdjwRjVXJdpU1Z1yimVSit48DCe1ToU48XH7dBzyN_3k2-8MSKdsJTXG2ebprZkp-ajDVbHfLM1rgPEAMxzIMzwwLiUSsjjOq6rvAHfxDLVoc1Yph6FFGPWEpxXLI6YZHYtDzxGr3UM8Au4riBMCrxk1or1hBEKVz7v6AFnBMV5Mu5q03Or0uDUNK38dbitHfAm1w0LJwPYoKu-uv1pFZjep1WgGp9M4ke3LJpW3-16N-43HrWqk_HMwGKsLG9O4H9QYlTaw13lQggPqkQrVzrOo-muUz40ptgmzTOTORvnLSe6-9i0u80Sbgt-bwxSxaKoquva-SMOgGcmXEdA5xglmpZlFKcsAz_bnl6HpmPF6wgcnCsMzKfV_YyT4g9NT-OJVPd9Q9p3ZDd0hls0HBvYf7xx6sE2KdOkllBTNTXmHNGmbVRSBAdrBCiHdb9Fid_S1tANf5ZDDRK3MVmCjaRxXEoQ3PQtVgz33uI9-LvcNlHgBksOUb7qINHhm95n5SCzeuzXOIS0hcBHc0LVS9xp9AzDBqyMdMk4oIMeQ6poQUZElGdJWqa8YbFN6ThMoZmMHAoIZLJHeRnXRZ2CwrPpLQ8jSC91DMAPWTgMsRfcrLAKWSNK3kSN9f899J85Vtth0D015nU624qnpFRrSwgoau1RCpU1OIOjTj4idpAqbaCmBcHK4dvDIydl8VTQDGtuMBeOObsR3YZ2vMIWWPCp2eUgaVBgYcPDVAhwKcM4dm6mByhkYWQPRwPyhtMWLJ-sQC9URR6y2gblHliQF5QfifRj8utJmORxVsqUhy5HZcF_nPvyVCwf_dyKi4jHMsmTzCbVPHgfP_d1IFqPV8VUDQO01_50gNPQJvv1fY--4IkKrDlEK5u-u1N5KDcr5beauLQGmL9Lct7QJNNSW5Q4pZtRDJt1f2sSXj908zzWKjBZLjQc2unz8l8YFeEZGFRlRN2MdNBCmPcbx90GbbKGJrAX6nc1Ga4_qlRYqyepvBwYrlZLVYYws1ekMMDbEJTYaHWWFVaUHXXI6v4-IOzs9bcmi_XepA6dH0spRKDYl7rVPadz5ZdFdAJNKW44r-Cu76Y9V3S2f7nevxG4gj2xkookuLIcBvBTyBHdi4pwl8EWYEBCjpjKYJNwqdeky-DhhX447DgV1FQKjzaIGtfJ9UEzAl6WIpnKLK6FDSVpkus7eixGEAL4gfqvPDVYGHA7-eWtGYhXn-lIGdeiMr0u4xgPkwK7UWd29WavHM5F-yi0xuUOTjw8RFLOFOm80VlcutHUkc67Cin9k84q4o6MJsdISVIVFYPsqETovWZYT51rWg1vPHUMy2Bf2Fdf_QHeRG27lkUSTyD8pTm8IFo070MVzValNdV-KTnCTYGoQml4cDQmBjqAqbiTs90oZ3PtGGheDkzgQYlI6_yoPQJygIAl-pW1eKqk-MPzeSa0VSvfB_0ZprlXpYUReGS8HDN86VwR9SxDCxIZKyIlmZlpwDXp9xYobWwmOlbazSffXTfbrxRWF2gMOeA_1aP1Vvpd2ugx42NVnsIf0NDtIBHpsh9n2EjwIKWJ0eFwSUd1VDYepJK6GoNQuEOfd3XXfnXQFlLxwKOQth28nC0OUmrdphNI8ekUuDqEzDp3disVe7s7jKVgZ9oto95T5UAOslnwA6omL8o0jTmvrePngb85e3ggeJsx81EVNWURZlXDXdbA4rlZp-9wPDathHVZyLNV6rcbwMF6pPRi7ZHOiSggHyrwnXfkwbl0zwm7ZSaOW8qVJFkJHmVcJJFLMjtwOM-rPhzZzRQ3WJgkuFBe1bZ7xIG9uaj-cKS24PVM4dIPsNCFdOBPdBzPMUxToQ7l3Rw8k0Zlmphqj7nn7aib9vIEamEX7D8Q5uvQXEfvqKBBtW22Wm9-JpA3i-u53vuFPxd_jHtR-f4cyF57i6paqWTxwsEroppJdDvLysqGB3g3k40vx6wzoX-ZRGUa8UohDKhYy8HYmYr6EUh0VkzB6KLxAl692Q2q6YDom42rau1txpQ3GwKugKiHbCspznGmNM-7-1pTZ72Myzj64a9ttaj19D2-2EAbc96pLr7RKG4jsWrUEdQkvhHlcqiMrHs7SPopCtQVmY9w5ej9Hs9L5b19VOXqTT94xWH1FqsA5E-hfSn91NHoFZJ83inlT3nG-caeLhXahUzKGP7H5WA93D-XIT0Yus-aEeC7UMZfpeBWnhHXGTPnDWE6g8Emtn_zUhDGSo2ubQJ7TmDFlsoGtIcY_5KYUXgMZr_vLkez04p2XbMny1hLb9NBRsxpnu26dYBpFLgfsOeMHvWb0eb6VBrRjPebfhibrmvlWizlbSFiDhOZp2XV2GSXB204O8SHoxLaEDNJRVGWonGZNQ-ocJZZOxBjcD9jpM_G2zejj3twoj5V6Ad087fkaVCGauUPSbrsFqXa1MpesHUt72ZpMQNQZ2oSDqfJ1t5dSm_mdJJNwiSfwD2Wa9Vs_-vf_9u8PA5ons5-nmVfI0dVIVmVRnmW2ZSIh6w428wvRkfUa6Q1mGSWpJwXsUu-W8BEo5CPAD1UgRf1sgKvrA5YSIWBQ9KUORgFXlm58vARvRTMoRiHmMTEC9wdOopf7I0oChamNRBVuPZKh4hoqnFHoBqamFNzlnpaWzv07kqM-y3cp8GPu8mEozNnjdK2Ktx-MGT1QWCsNbA9a9S9268X9E3FqiwBm86q0joNHgCj89afAznRiEddMGwED7MsdjrOginqNY9BQUQFqPrrzruHuvvsbOVHF4Cpn7P7qGyP7rPDepzpANYNX9is88EgQQDDRzS8d6ZhjtHqWnzJDmLVdIH_SZxLyXORl0ntZys1UOP9DsWnIiwaFRTWhRBpHjWRfb4HumhV_DFoie57vzWYVOdKM2Y1ayUMdF3K3aYCS4pGqbdBu2hr2Uw6P4ut2UtRJ3BQpLGoilC6eqeFavRKvIdiLKq_ojnHBKiRC9cKrnst2U3fitHMmIyYg79CsQDDsevUSaGqMLV6YPOoyvd4YCJSbpdaZTkY2LiMU8ltg5eH8egO7BfgNZrgMpYodwkwzdZRPAhHz1w9GZDRtI1VeVJBYJ6ytHahicVoND_TdQTiItZN11hRwx5lFBWyVDpUtwr4J0o_KpfQVE6Np2cs4y3O_YIbg89SUbsKDc471bdO9WFs3jPZ6HmHpYr4jQVRaXhjRI3WPu9m2F0LtYwmKeIsq0OvpuIBSJokxxFwkCCcxmihaJv50AWDkfOyZAJcxNy2tHjAkTMheTIIpEk5xHVWRZEsqspGIR4u5MwwHIbxGGhpwi_POy_MU-0H82ZVlQxY8nOqpCwhVq-qwjY-eFCRrkRzMOyjgnaLIZgh-u5FGczGGZSZ6O5gd7Hkx6h7SkcdqqZCvzGroxm6W1U8VGeq8iVMxhwNoSpWvJMNcGEOGcUg0FNh3oI-zkI43hWEMozblhsPqFKz5hjQSW2ONFXnnXbSa6ly1_CdQz1ybfv3PIgFUU9ZkVe1zJo8shU4D89yJuqPQ1TaXnn0fErsxLF5Sw-10vRyPgmI0ujtRsY8yRvWCGv7PGxKa-MPh5u0ZRN1fDB37OVVqSSi-npVw81Pky1ZtX8zdWyI6eY1yVnjnUU3VJ6AyoDoOVS1Xx0o9kFhM6h8uw4y4cz3u1Hl0l2ZyVKuElA6Q7_rDDKbHoB_wOB8JqOhdPh9EheivwIioDTHpl2nKR04p3VJjsXbNNIqmiZkZRxGjev8dhCcM2l9HFXTuKd5nJcQwhZZbEMmD2jTZtkPx87cO43B2XnHLW1LQl8lSVEWLE9yezg9sE0r9EfgZ_Z6WtzPdpihgNn1m14Y1TqqtIM9Vib54Uu0uw8P-fZpEowzFqCq2ZLE5Wka5XVWpwXNH6gWFIf0OROBp4N2GsMfsTgpC55KV3DxcDxtf8fhkJwYbdti66ulmAl8jSjiueT2NT3MTrv1h8NvPlRctLUxbYL2Ep77Bol2-sN-LkP5iiBQBthnnJc0bDcWOE16fg6zMw4NB51LfIguyjup7uRk4ZQQ9ER5eEi4C3HnhUA4Zdd06yztZZKsBO1F5LxtNJU-CCgqLTDNIx2hlZpp0a90bz6d0kg45kalZi90B99cdc_qsTQL0aVd8XZ0Z8_UBYECOCxLjWdJESWySKMqtp6Hh5nqRYKHwp_yXlBLHubgyRqadIvt7DGd66-Cr77aPlImX8rKy6pKGsHrSNqwyQNYdbHeQRCpJsbAufU45k0R20U81FR_iOlA3NNb1Z2jvqPwRP4EAqD77cipuL26W0zdiUzUadmAYnMBpIeZ6kcGB6Keek1vSx4_x67GnPGmtjbdA0X1XK2DYU11qjW4lRSdCkyeaA9rpSyNyafQZ3uwn3o5ysWrkLmvNX4fFT50T8jSUJuIRJ7WWZi4V_TwVPUrHoiIajR4mtUiTBImXG-bB5I6y0odCnOKV935F6GAblQDi0s9EcmgjUnl45w-aCwIVxuIkWtqwDXRokIT7NSQ7n6Z_p4OqlIOogKGN7Tv52GrWrfpOHRUY5jjKsnTKqorNyXnAabuT4cdBHnqxaweyOcr0xRz3jHqqodP2eR9amSPPjXtNbiCf-viOFVaFrmIax5nzOVHHciq4eQBMKk2HiuiKuGySmIr7h5y6j73ng371GTGIGYDpy0CX8ZpXweHajJjxwKamnNXghJNwDrm0rrzHsbp_sseglIq182F6ZyCfz9tl0FyZQ2BSlG6aRUP09TQdQQqqbPz6Guakixl6xmlE1XV3J8F7tFpxHvQD_OYbHpC-VJBvc7iOszCtMxK56M6-FPPCzkUwNS00M390Bpb3VTeD97ro5XJj0uRY11VZSKqkCWWVg8D1bkZx4KXmiMX1rIRecPr0Blzh2fqhSlPgSg10XbWgLDIJs5cUOChlu7nDg8AIjVk6Iy9ae_QPqJFh1TZM9Xlr2rwAU0f09iv8ibpSagIySdE51e5lrdXuPegsW7MXtun6l4FHbMubCY4KFnCypixpnIRu8VJnTH3KcCnRnNEsmhYJePazXh5WKjzmt1B4KadHkVSMA63piqihUwQooyeKzc3mPlQpiMGPAOq6YPaY0YvqUV--qz_bGHsXMZFXjRlGgkb6Xr4qjMWPoqZamSeZUlUizoJC2ukPRjVOf8OgkYl_Wdaf9mdGRmkFLGmUNdo1UlF79HJ47jtVfxlG7RtjxGqmvOOchXK4qzbDQYZJo5fsDe8KqQsZZmK0OakPJxW6-cdgb2qU2OKTXgzHh_Mw2xcHElBMrUgkY5UPWO6RZfGEntX2QavwUbIGzaCtcemZ1Smo-TIY1WGR40nKWKkR-pQG-LuE4kl9-2dLQGZAmAHbia2M11he7M7IarN4uzHt6515c_RPZBAbdlOxivYTNonKlNjy7wlaMEfBcUK8XAC8VLhNLxDpnWdDwejzaqqG3XZ9qYvzqY4TAOXSwTY3ACzk9yY9RsomcFmrW2Ip6NyACsvAeCjN-j8KGoG04z_eZFsqloUaQTeeOpmgR0erjN2TwO4NXFhit1yEYQ1uRt-cpi3dsb-GBBbe-5vIpxfV6cbvp87AOpw36_aqCfjq-iBxA7Esh1N7YWcNT0QhUEOipi-xc2qPTZsis_zamp2tMs-eWnsyyyn5g8pjaFWXt9RS0wXvH3zDTzK1NKoK_ZrKpfPzbnGXsNZCgPx4j8aFdk4x3BUGdpPhPBlXlJuanXSvtYaxaHRuDJCYPfLPEol97zNoun3gOnxe7WSTQVZrAQ99UC6bC9f9HVAoxj7mUI8THi6LFCBekXXf2FKjDYfYlrgaNbLaE4rHrBFRALTiUqdKFD4emy49nMWanfureg4a4tD-A4dyWXb0WDjSDrxU_B71q5VZ_dL3fc968NWe6h4wjbgAXjyqMvu8PUaew0DFfmtxwADdlr-Fi4xjSpYwWe22d8QQEUI4L5KYSlYHpXoZ4PBLftJ0a5GR7BBgJJG8ECMebTXaHfjPvsdtJEbECPWUqvbJw2PNyus4oCF7oC34zbUcOZZqDlmxr0EsypTjSStzo0wtuhT8PY-YN_XNqNNI3LWarL12NvWhXaaHSJT5kHfy5Vr8HRSxaTrXclQFVMQlMNWT_Q0Mh0rr2iih9b2T9esLELLKBgxMySmjy6NX6Pt0BU0Z69sTUF8TS1N5BKR8FAucwnAIxScNSyTonJwSh5guAen9GXA3xbgqGmklEzKOnWVDIsF7mYsDsf0Vrlg062kBqBU5VQOJwYNBDuaqDWZUDExM48QWyrNoOb5cCUDn6CsjW-BMQg3oJl2MbXMDw5gE6xEz105-N3cfaHO1wcnBVU_93xxI9tYWwIJgwDGZe6BmPn0vDqt4OJey86cBcUDuIpdqlbbz4MFzMcoFRqDuVqnGKiINFyCp_M3bc9O1NgokKfHhRQzQBevWXctPc8O8wx6No-6NgyWKO6LLiwM8nK3Zo84eUUYFZkoRRO5Vk4Ptt2T1S_GXreBe1E0FWNxnedeEGPg2Pd7jZ8DU912vUVNGZZxkoauU93BrLtOm4Ox0ufNJHoGlVBsdM7XGwBTXe-6MWfPpTIjIaDwyIf-Wjk9D4J3mGvhoJlpXnKOTANOokJeYx9s-QC7u2Yt-Suv-V7PU1DvvJJ76pjX3T50430kwbk9UG6IAuD2eiNxrVpqsEAFY4gDo2zchwrMThFbo7s0Tsbj7odyHT6SD3D30Zh-5YvQSrZwQXPM37Hr_Sd8ztV4-MnWqfhawzFSHp5mjPZdBXImTkjT-lZD9wiPvqug5uef4C6ogenvPLQVG-7MnfnJqsO9zrAZjpOaklai73cOrYwz69Ao4R8uKaJ8XKqWVKfB50r3VgKoYPzQKMfKQx_Rk6XzirqeWj7zfQUPrstvdhefb6qwLRSowN7T9DLSaieXrc80usrU57wnL9GrJmEbsNWSep_BXZkjQJo8kx4qdglJFYSb5Iq41z6iX6EffERLz8bZGdx2cbAvKsok4XVeltwVeNzvN3iK_Ut_hcGkB8IsK0OZRgV3rR3uhxm8EvChP6-Axp0K02IGujSvVEthcTgMsMFiUTgDcxfWkYgablOd3o81mKzG035yweQ5kzAtYjQ0lXX4vF9hcAXew39LAYecdyB9WFRzHguKx15_ERWRmQfKoKNajfWirkZ9412ukVztmWjvKWd9oQW2VJGBfqbBvNbOpJnJdLZPTdq6aU1lSmhs6Z67uIAVE0e8yKImZplrVHK_I-FVR7741yBMV4PM8xTOje7_V2lw9wMR-5Wug37mYR_F1wfvQGXxrZzut5fvd5ZjIyZcS92jiGmrG10sYJdN-Z93Cv3WQDjPcTU0QuH-Jj5QdfvrL_Dn_wGHPvae)
