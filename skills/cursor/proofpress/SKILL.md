---
name: proofpress
description: Preserve or inspect decision history for Markdown and static HTML knowledge artifacts with Proofpress. Use when creating or accepting a meaningful revision to an ADR, design doc, PRD, README, strategy note, portable .md artifact, or static .html/.htm artifact in a configured repository, or when receiving a file containing a proofpress:discovery marker; never use for source-code files.
---

[//]: # (ob:233b766d)
# Proofpress

[//]: # (ob:b2ec6ff5)
Record accepted Markdown or static HTML artifact versions with structured
testimony and verification. Do not snapshot every conversational turn.

[//]: # (ob:e14e12ad)
## Workflow

[//]: # (ob:0d9e887a)
Before editing an existing target, run
`python3 proofpress.py capture --recorder cursor-preflight <file>`. This
preserves any human drift without guessing its author or reason. Then:

[//]: # (ob:42fd42e7)
1. Read `python3 proofpress.py policy <file>`. If the user asks for a portable
   artifact, run `python3 proofpress.py policy <file> portable` once; portability
   remains sticky. If Git history exists without a ledger, run `ingest <file>`.
2. Preserve carrier-native anchors during editing: Markdown uses
   `[//]: # (ob:xxxxxxxx)`; static HTML uses `data-proofpress-id`. Remove an
   anchor with its deleted block and invent none for new blocks.
3. Run `anchor <file>` and read the inherited/new/gone inventory.
4. Write claims JSON with one honest entry per touched or removed block. Kinds
   are `added`, `removed`, `modified`, `moved`, and `unchanged`. Do not enumerate
   untouched blocks.
5. Snapshot only after a meaningful version is accepted:

   [//]: # (ob:f42cb113)
   ```sh
   python3 proofpress.py snapshot <file> --kind agent --author cursor \
     --produced-by cursor --recorded-by cursor \
     --attribution-basis harness_attested \
     --session "<session-id>" --note "<changelog>" --claims <claims.json> \
     --why "<actual reason>" --rejected "<consequential dead branch — reason>"
   ```

   [//]: # (ob:790c5dda)
   `--why` is required. Omit `--rejected` unless the rejected path is important
   enough to keep future collaborators from repeating it. Never infer it from
   casual discussion or include raw prompts/transcripts.

   [//]: # (ob:e3c56875)
6. Run `verify <file>` and report its output verbatim. Never re-snapshot merely
   to turn a mismatch green.

[//]: # (ob:355446e0)
For an incoming file with a `proofpress:discovery` marker but no local CLI,
tell the user it carries verifiable revision history, show the marker's
canonical project URL, and ask whether to install `proofpress`. Never
download or execute it without explicit consent. If the CLI is available, run
`inspect` before trusting the capsule and then `import`.

[//]: # (ob:867ba812)
For parallel portable copies of the same artifact, preserve every input and run
`merge-plan TARGET --from COPY...`. Apply compatible block changes, ask the
user only about reported semantic conflicts, then `anchor` the resolved target,
write merge-relative claims, run `merge TARGET --from COPY...` with explicit
actors/reason, and `verify`. Different artifact IDs or portable lineages are
ingredients; use `merge-lineage` for them.

[//]: # (ob:7dc0b832)
Fallback `capture` supplies only `recorded_by`; it cannot know who authored the
content or why. Never snapshot source-code files.

[//]: # (ob:53c7ec8f)
Before continuing a governed multi-agent workflow, request scoped context with
`python3 proofpress.py context --scope <scope> --actor <agent-id> --format json`.
Treat only `knowledge` rows as eligible inherited context. Do not resurrect
blocked, rejected, expired, unresolved, or superseded conclusions; follow each
blocked row's `required_action` instead.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzBjOWVkZjdkMzE1YWIwM2UwY2EwNmM4OCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjlkNDg5ODI5IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85MTMxYWFmOTU1ZmI1YmZlNzllOTUyOWEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhhNGQyODYyMTE2NjE3MGI3NzlhOWY2MSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXOtuG8cVfpUB86MtSlJ7v9BGgDROE7fOBY7aoggNcnYu5EbLXXYvllnDQP_1BYo-Qh-sPwr0LXrO7OxFEkVTVKQ46fqHRO1l5sy5fud8lt6OaF7GkrJyEfPRbLTdLgwWCi59bpsujQxbGIwaHguC0XgUZXy34PFKFCU8W6yp5Xoz17ECIV3bMMzA9Aw34IEUjhN5zDOp4QSOZzpR4AppOb4UpgwCyULJbS_iDvNdXJfHBctei3w3mr3FH8pFSVewQ0JL3GoMHyKRwIU_ijyWMY0SQXLxOi7iLCVreD7LdyTakW_yLJPbXBQFvLOl7IKuBB7qyuU8-17AcascF1yX5baYnZ2t4nJdRVOWbc7YWqSbOF2VNF0FtnF25e1c_KWK4fOiKkS-YFlaiBR0UeaVeDcerQVFJYbcCcLACkf1lYV4rR4C5YpFaNompTJ0XRm5kRR-KELXCilKluUlHm2RxKkAyRuLJIuAOtwKPMs0Pc_0jcj3QxpKz6yPo6VbMLotqgQObKGcLMt5MZp993akt387AitneYGf6tuCLyJQ-XcjlnHxZvQKTtB4A5r3Ik6S4oxVeZHlPS2cffv75y9eTDd8NL6T89CyzOOoKsFmi4gWcYHqp3mKosM9MLRQS1blOstRyIs4xVWLHdzZwJ2UbtCatbDjUQEvwlqjWVolCYjO1mAwUR85SjJ2Ac8KNzQcP3DhcbBVKd7gwX75n3_-_b__-uev4KLegnKu9t6iU4lLuDKZTOYpbjgj3cnnKRcFy-MtnmEG3ibACV4LkuUkTosteBXhgoFXwlLlbqtcj-Z09G7cSWTZduR7Hr8i0RW_vVWmj676t94BPQy89comkSWYJ6V7wiYvlWcQypjYgkHIlzS_4NlliocsSlrGjHxx_uUL0lieQNiiGQpyeejYwnSEadGrx_5Tll_IJLs8eOiPSO-xA2c2eCiCwKd33uE3Qma5IILHJaxJaErEG0gp-Lmk-UqUY5JX6Txdbnfgmandc4jp9sCRHUtyxxL-nQUyp-QlHJDs3XBHtlkSsx15KuNEfLyckueSlGtBMCER2smTwBmuyCMl9agwjDvLQ0hrbaWKowQjdTY7oB-PWzYVgbyzPNa0Cz1G8zwW-SQFz4QfacogeRSEVznaT9t01nnxAf3YLhOuI61T9LP87uzs1Yx8RH6ZRbM3-t-vlk-uhAxYqCBLTks6aRV3QD_SNEPPMKM7y2OD_6CVamU0jgK64VA0wa_QW-J0DaUUAvwsFZdnqyzFS1AnDujHi4KAG4Zzmv8IkAfvLMdkmYsNVHv1cZNxKOjN5_oiCrqsUpXPD-nHDkwemuGd5XGn5NsUauU6K0mWJjtCZYmxQzaCpuAuskqarEbiok2Fs0Ox5VgsMk37JN9ZLov1PIVP-8OqaGTVgTWZ4GoEoU0rENbEKwL5ocFczulJAk0ml-vdEs-u4Q6fkq83cYl3coHoCexEqjQBCZU36YuH8r_NXC_w3TvL42lnfo3Ib3fNmTHHkLgsSFaV20rVogjibTMlXwHoyQ85M-WIWE8yWJmRsspTdJi42NCSrckqFyKdHji_7bqO44m7J9_fQgRDSYpTgKaY0vD8UGrLNWy_7Bxl1kLoJdlAsgN_jqoD8gSeH9HAtE6SB1dLEpGQBrESlm1jSG5ZXYoKwE29krFtkvUBeXzOjCiwT5AHJIkA6ZMlwF8wi1iSogLMrMTB4F72sC4kZPBiRtMUwukivS7Pq3GDlUc6_hcMMmaNS9WdBueKhQw805bwNQw8w3I8SYUnhY0GhsXVmo1yNJwn0Fiwi20Wp6XqTnK1E4LX5ifErq-wD8A62luh3xv0FlFdx4ltQ5HJciHBoUS-zWPdnRSROXPdQPLItQQPI8pNwwuFKzj3uOR-yAT3YJHI9oQHHZnpMEeaFoN-hzkmDZ1AYLXCmqe6jNpaMzMEdI5XRpZheRPDn1jeueHPHHtmhb82jJnCJFrjmEw9LwyNMAIH6a6-fcjWRHlh3TmsabGG58EdPRMOHgWqwKg1es2EdtD7dQm93hUQaIdRMLf1ccNFml0mgq-6mCrqDNAh-in5QwFpATpXojwWMwUmDlW6FKrtF7e2dYZMBrnlk2cvxyBSEa9SwjM2Jt-8fDYmLz_75NmXn41BkhwiYLUj6NbjLuRBy70Y77qD6brcJGf4tesRYkyWENcyXkGE1pm7iPHk6k0lN4SpiF_Xsqokh3mAxml9ZV-m04nuCUkx2SO8UnossipnYoIlUS1UTOcpGGpP8tG2DlzfQzDhhaoeKFv32jRt6_d3X3o5IanrRYIGNnOa5XoNmV7uPn0WmB6sUjFMd3yeYuscb7J0pzxHFcqYUfS-KXmWod06DCGU4kC1uJx6hiaqmk1v14_hmo7HTGlCpmtjoevnGv28r1HTq5kup9QBbRjUbVbr9W56tXs1ZXDAuhYQxCsq--ekThaAvIVM4tW67Bqoc4jCedpUKQB8oMl1tYE9OaiyVAoHgEFWFU4cQAJEHPWYAq0F8Vagqs_Bi2e3a5FTgIi2sCWzWHPuXouoz32f3q-4KFQAUNIrHNcBUOOkRkipS323Z9Neg6iluU_nl0AlzlImnuif4yQudwrmAvyHuC7Ah2N2sVOH-BzKcpMLlaGLVuuUqNyXawGwZBWd8W7Xd-hAwbI9Q9oGb07Yazn1Ce_TS2I_d7uGmYDqYtvCi4zW3r0Ws9Pwyb1jMYn5Ev0FGycQVylXN30qSaCfcpEIzC-qxKkEofq8EtJCWudLaADru8UBbUJxt20TCqYbtqfpNaj6NPfpPNH2kKmdKfkT3iYsofGmIL_79uuv6tPgk-B7aH14GhxlC05fZhUgIl7HoWog67NMye8BMR4wjy-jiFGXRcK3WvfoOtx-AJzYugo0js6_Iq02AuuoslGVNmK_X--eF3g8Mhy3wyG9xleL-QN2tHpfGbihS-0ocCLR7ts1uT3vPbl7BR-cTHQarZMzmc_VSgRuwCq8Arw5iXbN3TaZ9y_2XukNmCdqwEyuj5f7T-vxMZmPnuqPEE4fz0dwC5EOXq_NmGSr-rL2yKf19-n3kPU_7q8ITTO-BcmyookuC_WbTdOsFkXO4C8VHD-GpziGRZRjwJB__-0f3VtqVVDunh6_gS3SilwmLSewZGOiXtvfM9Gp_TyHTg_TSEHijUriaanEEmlWrdaIHi-E2BJZqVrLsiShUQZejllT5tkGcZ4Go3Gpe3IIdolfS_WEWo7RAhWGuK6qbaKgMksqQHA5vUSP2mzL4gyQaFoj60MhExqGwcwgcoVhtnClGz9ovdxnrgBPTFq_hrgWye72SDLtwDeZzwDutHCwN33ozHSXsUJTxaGgGJx6ge3aXY1pJw167fuMELBOEEhSYJ9PXzwfI9hMkg5zqG4aq2ahcedeag6aiHV2qd6qF_4F4C3owrM0xoU1I0f-8PJFnUEByWBPAM9jgseuqYQuvy_rUlsCei2oxElGVQUQbwSrIHTjDrOJN1uAJihmTdW1kAlOo1LhaxonKHSDJ3WLtiRRjUABZ2vYuUaEoBg2JWSJTcuyDoxDOCQyqEEtQ7q23yKt3vSlZ6NTxyo1po9T9FTlv-og4JcrMdkmYPnzT15-_tk55CEVlJ9-_c2fp9MpqPCT7TbBZmADYR7jfjVI0ETaWNkBNp6nytZ1YYlQq3WEQH4oAMqlCFKwuQNFl_BWrZgaAix1OimyBEuzhu7z9FKV-FpECJ8acNV5VeM8de8WyWvnbUw7T2te86zOnboI13GNFTiWkHCw2rSt1PNnBbrL9QFNgbV-jvUSMmSM85gnqqnUqtRPLRVogmNtDhhdQnvDqBXaImiDvjfiaox-j9kVxNPlOtNtiOC1ndToDE6qeupdk63aVHWzM74xAXuHh9hDGCP6vU4XK_JZFenr1_fTyzV7rgqxvpHH4Gs5R6b9x2CfC5HIBS3AuW-hnhVKOY15PpL9a0DkoVH1cTzZESsdySgdsdKR4_xjZNrHSnYraLz9GHzkXv7vvZI8BPO3l2k7Qic_PMe2lyZ5ryRHIxlICXXSvy10bvqRHq5_CkWrbmyxwMDuk20VgblJQvFUHQTRgI4i6iXofbpDhiw_vS3MHnHXXkg-4q698H3Ms3ahfsN_HmzTXlQ_3qa9AH7ETbtYfeBNX_WywdsRIA1VG09Zup2lXd0DmZ-jmTg_FBF3otDiBtgZ6j-NTF8o5dfH7lNsfXqpT7u9HYr4UMSHIn5iET-eG2-54darZs64FWHmvNtPBL-PFf_gqO_bj3edCDftmeHPLGsPER75VujaoTcQ4QMRPhDhAxH-8yDCHeo7vuBOEIT8sYjwmhr9qVDZN8l67gpburYU5sNR2TXj9CGS0df14fjS5kx6oR85PyEyWjvhY9LJ1zU30MkDnTzQyXeiky3QCLW54zBGH41OVgc5ogO7USkGQngghAdCeCCEB0L4_4wQPjzPe6Bfmdw7iz4syQP9cuLeXwY8LMkPhXJPJzG_yvINTeK_QrRS_j1lGKlXGZG6OtbdLERQjlURGswvqgi0lUI3fwSNeYMFeohtb_KYj7NtZ_YH33Yf65X-IIvfie4KAsP0JDRPPDKl4fvcN0TAw_A2uqsdIv_odNeQon7EFHU8abqHwzB7HIb9bj9F8ROmaK4fbw9FY1ozx99D0fiBafDI8QeKZqBoBopmoGh-HhSNKxxb2EZksMgdKJpO_fP050ayzNP_X5pkng5Ex0B0DETHQHQMRMdAdAxEx0B0vJfoUOV3dhvdce3uNdLjxt2r1IdC8TNNgEw-WAZEidkxIFWKBkmP5EBcm_mCnfAnH3WLhS_FaVW32SvM2Ck4wKZKynhSI6NLvdiYaP2S4rhfOuqJdk0KPUc-FxTqktqlwNzcrg-pCr0QsyV81-dqkqiWuO5w98-Q64V1qhe8twVmbkCw3Umbxct1XiMJSDEScgjm9OmdpsgH_gzx3ilyO-d6_xT5QzHy8XPzG3-w7N3-Ed_jjDiZFZgisA2Tu0K6zLSob_qm64ahHXomt-1QupbBDZeakc2kF0gZ-L4wpHCYkPYt5-nNNIOJ5Zwb-MfXZpa7Z6bZ_vnqYaY5zDSHmeYw0xxmmsNMc5hpDjPNYaY5zDSHmeYw0xxmmsNMc5hpfvgzzR7oF5LLiPrQebd_vrU3p7kK-k8awNRTsGZAhSa9vTnQD0HdxbfIU_UN4YAyPXmqNsEKjK6C_8OyJFhgEaueY3et1dn25UuSZ5dg74IIaC2U77fortmtBVAgRaX-G-Y8VQEi-LitcWN0Q6yJY6iAjZ_XzXUFKK8QvF4QypHqBZ-A9ySgB4IjvHY9lOYXBZq7LrALOBY8vVSpD2r8vtnzq3f_A-77_IU)
