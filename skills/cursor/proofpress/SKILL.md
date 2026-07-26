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

[//]: # (ob:ffa6ae00)
   artifact, run `python3 proofpress.py policy <file> portable` once; portability
   remains sticky. If Git history exists without a ledger, run `ingest <file>`.

[//]: # (ob:6d23ae8f)
2. Preserve carrier-native anchors during editing: Markdown uses

[//]: # (ob:35ce54f2)
   `[//]: # (ob:xxxxxxxx)`; static HTML uses `data-proofpress-id`. Remove an
   anchor with its deleted block and invent none for new blocks.

[//]: # (ob:f119601b)
3. Run `anchor <file>` and read the inherited/new/gone inventory.
4. Write claims JSON with one honest entry per touched or removed block. Kinds

[//]: # (ob:6b88d004)
   are `added`, `removed`, `modified`, `moved`, and `unchanged`. Do not enumerate
   untouched blocks.

[//]: # (ob:f381d919)
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

[//]: # (ob:6ad53003)
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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzBjOWVkZjdkMzE1YWIwM2UwY2EwNmM4OCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImY2Njk5MDliIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mODYxM2ZmODY5ODYwMjQ2ZmFlNmZlMzAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzhhNGQyODYyMTE2NjE3MGI3NzlhOWY2MSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq1WeuO28YVfpWB8qMJqgvvFzkI4MZp4saOg82mQREZ0nBmKE2WGjIccncFw0D_9QWKPEIfrD8K9C16znAocp1dpattDcOWeJk51-983-jdhNaNzClr1pJPlpOqWjssFTyPue-GNHN84TDqRCxJJtNJVvLDmsut0A08q3fUC6OlK3hIhRsEkZ8GUR57IgipHyVJGAeCByLwEi9mceikPIqDPHUyh8VeEORunid5zmFdLjUrr0V9mCzf4Zdm3dAt7KDEbQO3C5qJAr7-WdQylzQrBKnFtdSyVGQHT5f1gWQH8m1dlnlVC63hnYqyK7oV6NKdy3X5kwBn2xoX3DVNpZeLxVY2uzabs3K_YDuh9lJtG6q2ie8s7rxdi59bCZ_XrRb1mpVKCwWRaOpWvJ9OdoJiCPMoSlMnzSbdlbW4Ng9BaMU6TyLXB7ejNIkcD6JFRZQL30HLyrpB19aFVAIs7_NRrBMacC-JPNeNIjd2sjhOaZpHbueOtW7NaKXbAhz20E5W1lxPlj--m9jt300gx2Wt8VN3W_B1BgH_ccJKLm4nb8GDvhYwuVeyKPSCtbUu61EUFt99_fLVq_ke0_aY0qFNU8usbSBn64xqqTH8tFZoOtyDihJmybbZlTUaeSUVrqoPcGcPdxTdYzY7Y6cTDS_CWpOlaosCTGc7SJjoXM6Kkl3BsyJMnSBOQngcctVgMS0nH__rl7_9-x-_fAIX7RaUc7N3hUUlbuDKbDZbKdxwSQbPV4oLzWpZoQ9LqDYBRXAtSFkTqXQFVUW4YFCVsFRzqEzp0ZpO3k8Hizzfz-Io4ncsulO3D9r00d36tjtghUG13tkk8wSL8jw8Y5MLUxmEMiYqSAh5TesrXt4odFI3tJGMfHX5-hXpM0-gaTENmtycchvQQbgevev2D2V9lRflzUmnPyKjx0747PBUJElMH73DH0Re1oIILhtYk1BFxC1ACn5uaL0VzZTUrVqpTXWAylT-qCDm1QmXAy_ngSfiRxvkzskFOEju3fBAqrKQ7EA-zWUhPtvMycucNDtBEJAIHewpwIc79uQ5jahwnEfbQ8gx2yYU_5VhpEOzE_GJuOdTkeSPtsebD63HaF1LUc8UVCZ8pYoBeGjC2xrzZ3O6HKr4RHz8kIkwyL1z4rP5cbF4uyQfkY_LbHlr_3yyeXanZSBDmmw4bejsGLgT8cldN40cN3u0PT7UD2apC0ZfKBAbDkMT6gqrRaodjFJo8IUSN4ttqfASzIkT8YmyJOGOE5xXPwLswTubKdnUYg-z3nzclxwGev-5u4iGblpl8PxUfPzE5ambPtqecE6-UzArd2VDSlUcCM0b7B2yF1RBueRt0aMakfoIhctTvRV4LHNd_6za2Wz0bqXg0_1tpXtbbWPNZrgaQWpzNAhn4h2D4tRhIef0LINms5vdYYO-W7rD5-TNXjZ4pxbIniBPpFUFWGiqyV48hf8-C6MkDh9tT2SL-RqZ3-GDYkaMIbLRpGybqjWzKIN-28_JN0B66lPFTHnoO85ZCWtK0rS1woKRek8btiPbWgg1P-G_H4ZAj8XjwfeP0MEwkqQCaoqQhv7DqG12sP1mKJTlkUBvyB7ADuo5a0_Yk0RxRhPXO8seXK0oREF6xkpYWUkAt7IbRRp402hkVD1Yn7An5szJEv8Me8CSDJg-2QD9hbSIDdEtcGZjDjb3ZsR1AZChihlVCtrpSn1oz9tpz5Untv_XDBCz46XmTs9zT_J4WNys2QfH0nkCwoJdVaVUjVEntdkJyWv_DbnrW9QBOEdHK4y1wWgRozrOlA26zJt1DgUl6qqWVp3ozF2GYZLzLPQETzPKXSdKRSg4j3jO45QJEHBxmvmRiECRuQEDDeexlMMHl6ZBInBa4cwzKqPL1tJNgZ3jlYnneNHMiWdedOnEy8BfeunvHWdpOImN-Fg-vR9dfff_lCamCjvlsKN6B89DOUYuOJ4lZsCYNUZiwhbo01TCSLsCAx04CmLbmDdcqfKmEHw79JTuEGBg9HPyvQZYAOVKTMUiUiBwmNFlWO14uB2lMyAZYMvzFxdTMEnLrSK8ZFPy7cWLKbn44vmL119MwZIaOmB7IFjW06HlIcqjHh_UwXzX7IsF_jtoBIlgCX2dyy10aIfcWqLn5k1jN7SpkNedrQbkEAeoVN2V-5DOAt0zohDskV6ZOOqyrZmY4Ug0C-n5SkGi7gEfm-skjCMkE1Fq5oHJ9Uim2Vz_tvqyy4mchlEmaOKzoF9uJMjsck_RWZB6yErLEO74SqF0lvtSHUzlmEEpGcXqm5MXJeZt4BDCBA5Ci8uZZ2hhptn84fg4oRtEzM1dQLpjLwx6ro_Pbwk1u5obckoDiIZDw361kXazqz1JlIGD3SwgyFcM-tekAwtg3iIv5HbXDALqErpwpfopBYQPIrlr97Anh1A2JuBAMMi2xRMHsAAZR3dMgdmCftMY6kuo4uXDUeQUKKIv_Jx5rPd7JBGt30_RfvpKmwagZDQ4PiRAfZE6KaUhjcNRTkcC0VrzFOVXwCQuFRPP7HdZyOZgaC7Qf-hrDTUs2dXBOPEljOUeC02i9THqlBjsq60BOLL0kLyH450GMLD8yMl9h_cejiSn9fApWhL13MMRZgKmi--LKHOO-R5JzCHCZ2tHPZN8g_WCwgnMNcG1os-ABNYpF4VAfDEjzgCE0XkNwILq8BIEYHdXn4gmDHffd2FghunRm5FAtd48RXli7gGpgzn5AW8TVlC51-RP3735pvMGn4Taw-zD01AoFRR9U7bAiHjXh0ZAdr7MydfAGE-kJ86zjNGQZSL2juUxKNxxA5wpXQUmx-KvUO1e4Bw1OWpVb_Zvxz2KkohnThAOPGQkfK2Z_0NFa_fNkzANqZ8lQSaO-w4id1S9Z6tXqMHZzMJoB85ktTIrEbgBq_AW-OYsO_R3j2A-vjh6ZXTAPDMHzOTD4-Xx0_b4mKwmn9qP0E6frSZwC5kOXu_SWJTb7rKtyE-7_-c_Aep_Nl4RRDO-BWDZ0sKOhe7NXjSbRfE3g59bcF_CUxzbIquxYcg___r34S2zKgT3Ho3f05bcy0KWe0Hi5X2KRrJ_lKJz9TwHpYcwooncGxBXjTFLqLLd7pA9XglRkbw1s5aVRUGzEqocUTOvyz3yPEtGZWM1OTR7jv825gmzHKMaA4a8ru1yYqgyK1pgcDW9wYraV41eABNVHbM-1TKp4zjMTbJQOO6RrgzHDzYuTzlXgCdmx7qGvhbF4eFOcv0kdlnMgO4c6eDo9GFI02OOFfopDgPF4TRK_NAfZszxpMGu_ZQjBJwTBEAK8vP5q5dTJJtFMXAOo6ZxamrLO-_9aQ5ExK68MW91C_8O-Bao8FJJXNj-Ike-v3jVISgwGdQE8DwCPKqmBlT-2NaNzQRoLZjERUnNBBC3grXQunLgbOK2AmqCZnY_1R0pE3hjoPCaygKN7vmklWgbknUMFHi2pZ07ZAjmFzZjZIOiZdM1xikekjnUoZ6Th358ZFqj05dRjs49Vuk4vVRYqaZ-jSNQl1sxqwrI_OXziy-_uAQcMk35-Ztv_zKfzyGEz6uqQDGwhzaXuF9HEuwPaVOTB9h4pUyuu8GSYVS7DgF80EDlFJIUFHcQ6Abe6gLTUYCNhRNdFjiaLXVfqRsz4jsToX06wtXhquV55t4DlnfF26d2pbrfNRcddtoh3PU1TmCZA-DgtDlKqZcvNJbLhwc0Gmf9CuclIKTE85hnRlTaUNqnNoY0gVv7E0nPQd4w6qW-SI5NPzri6pP-hLMr6KebXWlliOBdnszRGXhqNPWhR6sjVP1aGf_qBOw9_P0PMpC4eQ)
