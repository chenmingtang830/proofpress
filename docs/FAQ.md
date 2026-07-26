[//]: # (ob:c7a592b2)
# Proofpress FAQ

[//]: # (ob:a49fb51d)
## Is this just Git blame or Git for docs?

[//]: # (ob:96ae4bfa)
No. Git remains the source of history for code and repositories. Proofpress is
for Markdown and static HTML knowledge artifacts: it records accepted changes,
stated reasons, consequential rejections, and their relationship to the
artifact.

[//]: # (ob:2768cb86)
On GitHub, the file and its portable capsule travel through ordinary commits
and pull requests. Outside Git, the raw file can carry the same public history.
Proofpress does not replace Git.

[//]: # (ob:5f1b1d0d)
## Is Proofpress C2PA for knowledge work?

[//]: # (ob:6512908f)
That is a useful analogy, not a compatibility claim. C2PA addresses content
credentials for media. Proofpress records the decision lineage of knowledge
artifacts. V1 does not claim C2PA interoperability, signed authorship, or
complete capture.

[//]: # (ob:a3d540f7)
## What is actually verifiable?

[//]: # (ob:d74dbb70)
The engine computes changes from the artifact and deterministically checks
whether recorded change claims match that diff. It also checks capsule
integrity, event relationships, and drift from the recorded head.

[//]: # (ob:8fa616a9)
Reasons, rejected directions, and actor identities are attributed context
unless backed by stronger evidence. Their presence in the ledger does not make
them independently proven facts.

[//]: # (ob:73291080)
## What is the trust model?

[//]: # (ob:8d429e3c)
Proofpress makes captured history inspectable and checkable. It does not make
every statement true, prove every identity, or guarantee that every relevant
conversation was captured.

[//]: # (ob:33ddfda5)
Actor roles include an attribution basis such as environment-attested,
harness-attested, self-asserted, or unknown. Missing or unattributable history
should remain visible instead of being guessed.

[//]: # (ob:c9598d68)
## What if somebody tampers with the capsule or replaces the file?

[//]: # (ob:74fbbd06)
The capsule's internal integrity checks detect accidental body drift and
inconsistent rewrites of its recorded events. Proofpress V1 does not provide
cryptographic signing or an external trusted checkpoint.

[//]: # (ob:04441f75)
A future signature layer could authenticate that a trusted key signed a
particular capsule and make third-party alteration or forgery detectable. The
strength of the identity claim would still depend on how that key is bound to
a person or system.

[//]: # (ob:35e0d872)
Signing alone does not tell a verifier that a file holder replaced the entire
file and capsule with another self-consistent history. Detecting complete
replacement, rollback, or omission requires comparison with an external
trusted head, witness, or checkpoint.

[//]: # (ob:168fce18)
## Can parallel copies be merged without Git?

[//]: # (ob:dea2353a)
Yes. `merge-plan` finds a common ancestor for portable copies of the same
artifact and reports compatible changes and genuine block conflicts. After a
person or agent resolves the visible document, `merge` preserves the supplied
public histories and records a multi-parent event.

[//]: # (ob:23fb3e21)
Different documents are not parents. They remain `ingredients` and are
referenced with `merge-lineage`.

[//]: # (ob:edb4aab8)
## What happens if the local ledger ref is unavailable?

[//]: # (ob:c1f2572e)
A valid portable file still works. Its capsule can be inspected, imported, and
verified without `refs/proofpress/ledger`.

[//]: # (ob:0a3671ab)
The ref is the complete local working record and repository index. Losing it
can lose local-only history and local lookup, but it does not invalidate the
public history embedded in a portable file.

[//]: # (ob:332ec0a8)
## Why not ask an LLM to explain the diff?

[//]: # (ob:82e38345)
An LLM can provide a useful reading of two snapshots. Proofpress adds stable
artifact identity, version lineage, portable handoff, explicit separation
between attributed context and computed facts, and deterministic checks that
recorded claims match artifact changes.

[//]: # (ob:de1a1962)
## Does the portable capsule leak private prompts or chat history?

[//]: # (ob:14c0600f)
Proofpress is not a conversation recorder. A capsule contains only history
admitted into the public portable lineage; merging copies combines only the
public records already present in those input capsules.

[//]: # (ob:7082ab1a)
Anyone holding the raw portable artifact may inspect its capsule. Keep private
history local, or create a clean copy before sharing.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzllY2YzOTIxNDIwMDQ0MmI2MDVhMWI3NSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImZhZGVkY2JmIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iMWQ4OTU0NDlmNmQxOWIzMjBhZGU1OWQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzNjZjc2MDA5MTcyMzFmOWE2NDQ0ODNjZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNqtWmtv5LYV_SvE5EM_dOzV--F-KIwEbYLuNmm7SFHEi1mKpGYYa6SJSNkZLPa_914-JNneyF7PAHnMgyIv7-Pcc8_404r2WtaU6Y3kq6vV4bApBavjMgqTKAiSJKqyIKVhlaer9arq-HHD5VYoDWvVjkZpdlVkPClFlJZJJKKyDGtR0qKuRcqKgtdVJNKAlkVd8jQr06LIi5znZRFwBs_wIqawL5eKdXeiP66uPuEbvdF0Cye04ncNXze0Eg28_Vn0spa0agTpxZ1UsmvJDlZ3_ZFUR_JT33X1oRdKwTMHym7pVuCVHnzcd78KuOzQ44Y7rQ_q6s2brdS7obpk3f4N24l2L9utpu22iIM3D57uxW-DhNebQYl-w7pWiRY8oftBfF6vdoKiC2vKBWdVvbKfbMSdWQSuFZsq5EWZJklZZzwsqzgKYHFacrSs6zVebdPIVoDlPh7NJmZ1ngVBGeZRHNYlzZIkKWLG7XWcdRtGD2po4MIR2sm6nqvV1S-fVu74TyuIcdcrfGW_FnxTgcN_WQ3tbdvdt6sPcAefDXA075h687frf13u8aSvSROqdS-rQUN8NhVVUmGyiKbeUAV-08LsN-hd16M1t7LFLdVRabGHb1q6x7B5q9bwqMJQr67aoWnARraD2Ah7u6rp2C2sZjlNy6iKYDmERWPeXK2mhCBwD_jKHUU5F9Z7kEXiHj75hjxZq48HNANDCOmw-ryeDqMQvyoN-YPDflBEQzKSXwelyd-lJlUDFyFdb97U8H906F8XrfiGvHyXBfvKjIqkqum57ftnd2kW92JPZYv7CaK6oWewTT1WIm7FOi4IbTksPXRKwueTxQfa0wfmRnlWsKrIzm3ujy2u_X6o1sbSWjbWJqkV8dVGXNkQ3dM70cDCvhu2O7JgblqHUMbBk-jPMujb6KdrYyOmcCP4VpD7rr99QfBftslC7LM0jMqgqM9s3fsd1QTCQQlAXz004EjadNvjmrSdhk8BOg9Uy0o2Uh8Ja6jcX9qDKF_wJY15mgR1_sDa__qzmB5o0xzJ3Yj7z3nwmUcX_MbzhFdVHpzFkveQbqLdApAbxwxaKOJQi9R9tzf56BHV5CQXWvTQd6Ra8FZR0yzMaHkWG_8tqIIGtoYSxY4owAZobQxBGz5Em0zDIJJD_5Bagum0B6sR2xdszOOoDIPiy37Ea0OzhIreA0A0L43mFx5biGTBk6gUMTvZglnJ7OkthpAe9NCDpzzUAQgewGUGSNBjQB6AdcC7ywUPxTHnNafpyfZdm_j0XQOmyZY1g8FcMuu-xHRfoga2I1RBSt7Jvmv3SAj-2D5WpmXBs-IL9tUA93uBLJBouj-IXpF7oE7GagukL4ro89sYoIfe0VAmjFOWQ54ndVXxIDu7ye8ni_6EToYiBdwzL7a9QTqMuDLli5XMmCkXWFJ1Cy4GwpSEdZ6e3V7A9QFTlCi5bal51dCjwIY8NFDRQLqwmhnVkGZ4HrXZBjl9u5SyqQh4kUdnt_c_YCYEk0AvAazkHQQb-4kWDXQYh2RgvTPVdPBd13CBybFgb5gVNRPhwxT-FmoDVzYN9HnWHRDRKkH2ot_C9dHobkCq8UwKv3Qb_VzDETSK05ie3cb_CXVJPppHLqCA2o_gt5Yr26T3AAq0haJC6EAOMBEhPG2JpcV1FYsoPLu930kYFntIS2R0A4KT7TSYCLA3vr8kUIhHxzvJR3AloLBchjHBq4TS6gswtqMwigF9hdzFLIX1UK-GB2Fa1QjDL4GxF2wztPSOyuYF9IOFdZTmkTi7tdfkjjaST3E2RaS0hApD1ge-_UGrEXYZBBQCaBvbEoLROMtDWp3dXkRct8xACNCnBsDV7YMWI17YCfbhhHEki003Eiygj7PhaOmrusXG-fbtO6I7In6HqoE0w-M55ObzLOWluyyRlkjERZyk57bv2j6GYT303Z1EiuApfG_twNlN33dEtZADuw6rzTKfBXdyEdKwzB42hO8626ufDleNoLdwvrzDvnN4xp8v3QZ49AEyF6dNk3dy2cNhwoIsCOqzmzyjiVKN41ALzUtRQ8Kc3NJfkuupzsAECOISkQ6KiFYhPbu91-0Rmy32UYw-7tbT-2nHcS7Z05HhmpkZjnps74e115dWeF8UfBiklZV4zDdeL1rUvsBpZk9vgpPALLs6dNIAve0FVgXy71AE-oDaWSPZcbbDXE-bbWKUuldKbaqr9QY6KeAYuNkpeqoKr-KsiKuIJ3kF41lEk6wocxZltErrHDhIXmZxVPA8E1mcZmVUB5SFUURrzlLGwhxtVZpqo8zZaF1F-WdwNMpmURBlF0F-EWXvw-gqCK6i4s_w3wDnK-fxueT4efbpp_OIeSYfrdi2o2qHWFplSV5kdZGFiP9mj5n-5lL1ZZKa2zJLRVIFSZyLiPstZyqb3_JEfcwdRkWeZkVA07wO_WEzycwddorYJcUIog4Xblpc-Y72t7y7b81qDLpk5Pv3797OlBgfGnVFzOFGyMXBQhyQpTsVYX3T4uMCz3RjvFGjfxuQ3tPGDfXTLA_WS-y_jYEktZMHbCXw6U3rT_zSzOo8VmZVBeGtaR6MEZ-pds5jp-htcEsJlhwNR4UHwCx48gClTlB0B74KHv1x0Ao7GJyyHnHLHIP9jdEenjdhwpQ4DBWAgg_U5U07i8c4aLgRE3dcuD5kZhgEVQ01Vvvrz1TAB9n5agHPnZXzIokzmrKgSP1ZM03PnXWKHMfROFQzsKu0-qYFxOY2bZQxdw_cmj7IX5-GhnIIZn958SAN1TBecMomCNfP4eRoY4K1wEzRHUyK1Jq3NsOqsNNp12NuriEfwC7P_ZzushChOs8pADfnJU9G_Ji0xSlCXy8QuhOKQuSVKIHz0tyfMNMMx7i8XvjDsRwtspLCTXu_E7C69_TB1751JUpSmu3sZIwsEGk8jNGq85KEK7SbdhQr1sR05Aco4OCBgxP0ZOF4JDpiwe2iCNI8S8scruOdMhMpnVNOURqrwaCeJUA37dA2mI8VZbfwcXUEEO07bMlwNXycCTMqAtRh4uJ74piym0DGhERF76aFb_awggsYWfB0cD_SZNESm8N_fPWoEGUBzTwK4sBffaZ9Ps24l4mYHgWKAngE_JvTsR_OdM2nv299tUCJ6fLIGQJ_gTVtSeAUTgxZsv4g9jsXoSPWJ9kO4BKIi1OS7ArILXFHDarMKfA9nYxbcioTWVIAGeG88NeeyaXu2qfonhewSqDeBR10R_sWfDd9RPBHygv_I6W5pPsV8pK8k0qZYQk_80cZvzpfQ0feGZHNqRT4-zR-DSHQEGCEyUrgDtsB8XfJDUXO6yKIoySYymqmyj7OrVfIqaZrPpOClNOiyMMwEdGY4JPOOgO81wqkYK_FHchMhClkMOBLC1H38DTYCl5D-jACkkGwh-Rq3mbcjIs97XjQ3banhx2QAOVkRvACJApYbq300uc0ISwEJeFxkgEFKoG9e3_MdFyfmycIsOI4dsKb9oBdgg0N7ccYYgFjpSID7vkFrjgC5MNlbJFZRW-LZWjdbQv9PZI8wEnoS5AUnZVlfCW7xnxvrLOqkAVDgn9b0d1bI9E0qKeqG5BKdtDlCaaZPdP-cL_gOSoYSzhNcpbRsaonRdl57hQp2CS2IbkEr9XDhUf26b1nSoLClthTTaHP8s2zRPKdcRza4dnHTev2R_hYI-w02H4MOnR7af40gfg_DLHEq5foGnfgmG7QbVyksdrW-D3Cz9oqGC_IwDxlJRM0AIo4zi0zpXuChVMlak97Q1Ezlou4KscWN1Ot3XmnyM3KpyMy9ok7jsNUr9VIZfEZx6Tw661oB6RZZjxFglAD20dkuK7B3aaCxgwFlmowRXXNncM_j85ecl67K3y0xKH369RwODRSAD49mCeks2Kcz8h-aLS8sKqERamFSMK4Gxa8oAGtR8_O9HUv9pwgjKuPllj1Jn_NNszF3gfL8fePC3Zy_OOtGgYSPk3KM139USM6iyDucz3IaM1T4D_TyDXTyEe0fb24bTq83OOj-Mr0IIcyU418BLvV7G_A3tjrLPksLGtRpGFd5cmIdjO1fNY3XytzI1_9_ZK87Qwhkci14GJNp9zjF10LPNZTQHzYhaLrbgeYrYC4oLYwQqxsjRdtSxKPMv1IxL4SKEshk6YPXb0E-jygQZKlEDIxUblRhJ-nzgnyuZ9DeFkUVZ6KshqHs5mi7rPlBC3cMA2YnRXy46qZg9VEip305ifj9eQsAC7e1fXa3Esy8L4S6DHs2zdtJfS9EO0XJh7bwewkye1Msn46NnqShb0Ry93Pi_NBcTTXgegSOglkeQzm3UxMuD8K_lPoXq3Um8R6pvlEWURjSlnJRyNmEv7TCeirtXcwaFYnEFC-l1qbPLfSmJeQHsvSfzGd1HIE08QgQBV85Tac19DYHxpMsKObSrUdSrFgJazU3rKloOQVjYu0FBkU1kjHp58IxhR_vbaPFlySfwhx8JGDEclhgAEQy1SMvI9uhhi36IEjYCq0dsBdGKjg1CeX-PAZ_vk_5V4Cqg)
