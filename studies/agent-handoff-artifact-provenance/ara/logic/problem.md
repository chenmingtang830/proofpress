[//]: # (ob:5b4d530f)
# Problem

[//]: # (ob:75d8ff5d)
## Observations

[//]: # (ob:98d591eb)
### O1: Agent handoffs preserve work imperfectly

[//]: # (ob:cf5b74f2)
In multi-stage work, a successor may receive an evidence map, issue register, draft, or summary without knowing which statements are source-backed, which routes were rejected, who accepted a decision, or when it should be reversed. Handoff Debt measures the resulting rediscovery cost in coding-agent takeover, while AgentAsk identifies data gaps, signal corruption, and referential drift at inter-agent message boundaries.

[//]: # (ob:fcdbd7ed)
- **Evidence**: Handoff Debt; AgentAsk; the continuity comparison indexed in `evidence/tables/derived_main_results.md`.
- **Implication**: Readable context is necessary for continuity, but continuity alone does not establish whether inherited work still applies.

[//]: # (ob:f73aa5b4)
Passing complete raw history can restore context but may impose search and context costs. Passing only a final artifact leaves decisions easy to regress or upgrade without authority. The study does not assume that more agents or more versions are automatically beneficial.

[//]: # (ob:36339a7c)
### O2: Artifacts can change independently after handoff state is recorded

[//]: # (ob:f1498f86)
A receiver must decide not only whether prior information can be retrieved, but whether that information is still bound to the artifact currently being used. A semantically plausible handoff can preserve memory while silently referring to a superseded or modified artifact. The evaluated failure is therefore stale admission: reusing accepted state after its recorded artifact identity no longer matches the current artifact.

[//]: # (ob:689aafcb)
- **Evidence**: W3C PROV models document revisions as distinct entities; GitHub can require an out-of-date branch to be updated and retested against the latest base before merge.
- **Implication**: Work validated against one artifact state cannot automatically be admitted against a later state.

[//]: # (ob:eb6d1b42)
### O3: Design-aligned tests establish mechanisms, not prevalence

[//]: # (ob:d925bd21)
Proofpress was designed to verify artifact binding, and the primary stale-binding fixture directly injects a binding mismatch. Complete treatment separation is a strong test that the specified decision rule operates, but it is not an estimate of failure prevalence or benefit on independently authored task distributions. External validity requires fixtures and environments not designed around the treatment's native detection boundary.

[//]: # (ob:c99188ca)
- **Evidence**: The controlled admission and cross-model results indexed in `evidence/tables/derived_main_results.md`; the interpretation boundary in C13.
- **Implication**: Reliability within the controlled task must be reported separately from generalization.

[//]: # (ob:2152be5a)
## Gaps

[//]: # (ob:d7d0911f)
### G1: Handoff studies usually do not manipulate independent artifact revision

[//]: # (ob:fba9cc86)
- **Statement**: Existing handoff work studies context transfer, takeover, communication error, or frozen repository state, but does not directly test whether inherited decisions remain applicable after an external artifact changes.
- **Caused by**: O1 and O2.
- **Existing attempts**: Agent memory updating, clarification at handoff, portable memory, and provenance-aware retrieval.
- **Why they fail**: These mechanisms do not isolate an information-matched receiver decision conditioned on the version of an independently mutable work artifact.

[//]: # (ob:b5da0db8)
### G2: Controlled mechanism evidence can be mistaken for product efficacy

[//]: # (ob:6853ed72)
- **Statement**: Repetition across receiver models on one purpose-built mismatch does not estimate real-world frequency, task diversity, unnecessary stops, or organizational benefit.
- **Caused by**: O3.
- **Existing attempts**: Repeated trials, model robustness checks, and benchmark-derived tasks.
- **Why they fail**: They improve within-task reliability evidence without creating independent task or deployment samples.

[//]: # (ob:8baeebfc)
## Key Insight

[//]: # (ob:5f4a1f20)
- **Insight**: Agent handoff has two separable requirements: semantic continuity and artifact applicability. A readable handoff carries what the predecessor concluded; a provenance check establishes which artifact revision those conclusions were accepted for.
- **Derived from**: O1, O2, and O3.
- **Enables**: An information-matched comparison in which only one receiver can verify the accepted artifact version before deciding to proceed, revalidate affected work, or refuse reuse.

[//]: # (ob:67dbdd77)
## Assumptions

[//]: # (ob:dc3b03a3)
- **A1**: Artifact content can be assigned stable identity under the declared canonicalization rule.
- **A2**: The accepted-version control is protected by the stated trust policy.
- **A3**: Ordinary and Proofpress conditions receive equivalent readable handoff semantics.
- **A4**: Verification establishes identity, integrity, and declared history—not source truth or external authorization.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2JhNDcwNzdhOWU0NDQ2NWIzODRmM2IzMyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjU5MTZkMmMwIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iYjM5NWQ3ODljM2ViNWZjMzg3NTM1NmEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzk5YWNiMDU3NDg3MGZiYmMxNmZmYTQwMiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXFlz21aW_iso9kNXZUga-8I8aexU2jUPTrldyUO3i31XESMQYGORzLhc1T-if-H8kjnn3ouFGyjJSjLJwA-yRIIH5571Owv4eUbKOpWE1euUz1az3W5NiR_ZUUQS4ft-GFAv9qVHPW82n9GC79c8vRVVDddWG-IG4YoKn4SRJ2KPuWEQCC-MooR4oXQ4pcyOhevYMUncKOHET4hvh5HDwoj6QcSTwAuBLk8rVtyLcj9bfcY_6nVNbuEOufhUw9sZoSKDP38UZSpTQjNhleI-rdIitzZwdVHuLbq3fiiLQu5KUVXwmR1hd-RW4JEOXi6L_xZw2KZEgpu63lWrV69u03rT0CUrtq_YRuTbNL-tSX4be_arg0-X4p9NCr-vm0qUa1bklchBEnXZiC_z2UYQFGGQOCF3mT3Tr6zFvboIRCvWlHpJwKM4YZ6ggWReHAVeEBLkrChrPNo6S3MBnLf6yNZJQhi1g8iPI1uCSJ1QShCjq49juFszsquaDA7sIp-sKHk1W_3t88zc_vMMdFyUFf6m3xZ8TUHgf5s1-V1ePOSzj3CG1hrg1qQkr7LiNmUoA2Bsu9zy2fxJ9kLqukxpU4Oi4LIqrdBqRCbXpAIB1kLRa-pNUSJbd2mOJKt9VYstvJOTLeqvZW8OH61Q57NV3mQZMMs2oCShj0mzgt2h9KnPA8-WcDnop0YDWs1-0AeA18w9COfq5ju0I_EAr_zJ6i-q9zu8MWoPLGH2Zd6TjwIeSxnwQ_K2s7Lewl_lVvCU1MLKxC3JFg9FeWe18qqsbPT-wMAjyRSVsLhg2v6Ri3GWmQxo5Ev3xVl-m1vE2jZZnS4q8FdgqmDNFqzNQioyKx7mcEHVMAZ6K0prS_ZWJYRFckv0LO_Azg74lZFHCKjxxfn9sBFWVTd8b5HqrrIeNqLeiBJYbF1vbt33Eca4IfAPPpge8_tx3jrWDD6DmlizUhBt0uqd1j_EWoZuEIWSiiixKXGC2La9IIpRIXlRK5qGge6mEIXY3a5IlW7hjupOaPXtX2j0HzFoZCnbDygMA8mAiApRz4wxVSHrtQSrEuWuTE0oq6izoj6F4B5EUsIvkAJcV0SOFDENnDiCEGBzN4i5m9DYo0HCkpB6bhwJm3ixI-IkRto1qVVI0tpa-eDV-MLMtd1wYccLO_xgRysvWAXRf9j2ysaoagQOV4WEcMmJBPvpX_38wkFM2aUOMhtSbeB6SFuQzWTIiEQrVTQGcceY7JWIYmgR6keQAWJXek5LaxBkWlpfER2AgkVqC2IlL6QcZSaRTsSEEwnixC0zg_BhmPkav79PuciZgNd2cyutqgZT-S3kcFHOLbiWl0QCHcjHRVNbVACDlvKMurBqkWXgtSnbWGg3Am9ZwdHBR4umZGJBIecLPjfXlEBBgJuLEu-BWV-_V1gEONvBX8BlKyl1c4gI-eA1qwImMg5cINwA8xJ8af0AqQuZgtAB0t3uMgGaKMlDB0QYHBMSMvwuOvFDClRSSLc7VE8lSAkMgkK6K1hR1VVPvcgziFIWeB3JOuWCwsk9nKjlr7IEqfYoGRAhYgA8Q7O7LQkXnQh1ek3r_fJMyDVqd2zCQmJ7oS_DVu2DKGzU_jXhE7gmIMca1NwaokWLJuek3C-ttzWYEFwC0RBoV2BLIF4w2S3KEIigmtGO8E_j5lrvcLhiS-qUkQzkRUUuZMpSkp2c9eMXPO4ZKASuVHdA6N1O5DdvrdcFF59mHxW64g27-PYRjDp9-58N2EH3_nswSlJy6wOAlmOsJT7tQHTKoDFQAZ8EvGRtRPXqt4Jim2ZL8uciMS_0vIRE7CiPuyvrR61DcPYUnL1uSlBnaxWQYMBB86tQ6XFkOt9ZEL6FcJOOQyXp-Eks4_DFWb4BF2UiBeOFwFnVyoXBSdHglau3zgQJFgw9zWVRol1jBCcjUEnQkDvUP4Z23sq6gVtU6W2-IBn8hFAn00_AtVDhCUutqr4q4seRwUwENxYlhiohpRgXMU_cgHLXeXGW--rPeiCVoQVUQDcqLO37OEqBBvA1VxEYA_kZdMcykm4vGvQRFwbG3XBeKXrHVgd6NI5rGZksL9ndecpvILDlECFB3BBbe6oQQcFq7ofGubxkIVd4HgpfJfN7-BWi436c9YE-z9_gu087EGWOCWOvbgQ2voWwP1Qv-gGESnj92JhAW1X6s1hqnbQG83kGxDqxHJ4fMkiv6V5SqGodsM1Jrf6k-Im8u-_i-OB44Mej_cAOwtAXgvlR5CeMUV-4UezHnUSGMH6IYYfQ_vMUUaeI-geLqI-vis9VheeKvmsF8ItUua5MKPNkEiaun0S-D_VR6HjCDkni8oQHxAltO_CEE8eSuJGM7TiJEuAbSmCoB53HVLmO-8FOVn6wssMzVa7LIkqpIJer3F8ePk5F8FQET0Xw77sI7s_qEVcyO-YR80l71gG4GPrbM1FBj3hHfY0z6voO9xyasE7oPWQwjHxNrs-15ULxC9YLpo9W2F6v5Du8PEWEnYKDKbUodxugeYs1JQI0JWU00EY5ww2YMpTJrQIA7TZVitpvZYRMYBoV5T34vNiig4B3whUV_FD0SiFFWSqXKlTY2ClPA-9UKudgUOiphpGlhWYoAKc2iEEtSdIM03qqkDzQQhs5KhVWcI9GuVXn-BppQKgBUaR1dZLNQcAQSTEjWpsi49WIQcmQxJQEru_aUavHAZQaGtQzMZApBEatCbIwhfzMpRN3Zj1AR_0w6Nmwpq1dlHAXrZxa9nkKdorqTHOMtMrdzSWgBbAxtllar9t4WWMFoTJGJVCerQWC-uuyQFOAAKptFG9d7cDqlRlsBRYHQNAqwExAUpU267TGj6v4kfflVCE7-0BoB3xj6gGz0pECXQj45WIn4IcyRh0tUSIQ4ywcx7adIwjO37VK6aqkdijaiqFS0hL5fQqn0OkJeerkTErtXJuBCP4M14AA7jFr1yA6FEUXGqdm3os081QO6Zt5TB3tca28s1PPdxQjmjLbqi8j2mA1XrMkMQ8SR9BDgoDtbpDJNnJWfdhUAA-QgyhVOTRSZv3JeiwddNVnjE6fzuapTE6HnoxTHgn-4gJZWN98850BnN98s7L-YpLSG0HrbzX1m-ruWwPlIIvlDTo1orpBnZxBELg-pP1FJHO26fEOYMlNB_cxbWizPY5kT7XLME4IkYx-5c2uq-En77X1w_t3P2JyF1nVVw_tYkuFXSmMvWk-ooaz7Yp3kGLfHCZYTCUV5gSApWm10SnkqcJhSQJFrmqffM3Nrgvng7HFssgyTBgHTTxWFlW1UGLDEmNEOK4TuFQEh_x-T3bVlT6NuWSs5RJxO3GcwyWT753eu7BEQLzfVI0ChbxQORBgYrq7Fr4eS6fJML33NnilEUdJwthRI-4lWEbl_bWtRFF7331SVnvb4V_l-i35ttarS5KPKY8GnNicxof8gie-7g2jB0JdSa0B_1URP5IOwraa3EFBDJAaYtm14AEAlEfui7N8IuL3oPI6VSiJKH8YFEg6nsA7RQ6IrxkRMSB2Iag8jKz_JfbW2xz8eXOtnXl45YhcAukTR7r2c-6DRzeX4cEPsgv8DwXPQ2Hws14LVFhUYa_VyNHDCNItj6IDlm6w6t4d4ZmzRz-8cixQMI_aHvGecx88-o2jTt0VoEgDBGCsE_skKuJWensIDarG7H2i9fMDrQGsO00EZnzzrrwFe_1Z6CERZnPVtmlnQqCBYoADl5dQ3pXhk0yh5htSOj9sGuCxiwwrR6l694L6R7fpyIHt4MwHjgOFTNuvs3YEWzP58hIwGzlDdzfMUIByspTpY2DcOHvA5SU4dfFgrzOCjaVWE-Rh0XbbsnSb1meong4sT6mezCxNm-eqLk5nlqfEj8aWJ1O55SXw9VxRHx7i2ih0RBqmuYJ0u0L3qkhOZ6EXzXN84lpvsDBeXkJfX2OIo_cYIKYrDnsLGAniLjs1ugE2ukKjyXWbrXVJoLm8hFnGx-K9h3UB6oTYAFBc4auT4QmNQYa_zhBIp1BD50scDfLvFY7uBPaUVBY8L_RBij1PamB2pnm80MLvwbW5wfJSohzhkfQZbXkp_53_-H8iEyYA9UQguW1S0yNS3fYL8__3UGSUDVPNt7PpqbX6XQOlCLNu3t9YFduILXnSSD8JkzgG02GEECYgQhHfiZjPLo30u4Hd9ZH-1FmZOitTZ2XqrEydlamzMnVWps7K1Fn5_XVWHr8AerwI5njzPkOsgi_nt75-nTU3jwvXjbw4kVTEgQsxInST2HEFkOFxTDzUauLwwAYUnIS2F0jm2jIIIi_kysuun-5w6c374Ngr210F7pmlt1jYdhBH8o-79Oa7gPwd23FYPL70dlQOXKboeJ7DokR4Mek21wb1QEfxJYC8uWUIxVDAmCcFZ6PLcsNVObzD6XacCbTXN-TUepzaVQNvV-sY7Z4XPp6C-fEX349L67N7ccMSABISqdQ6hKlMUQDAWym6p93VwhvgDPgf5Wo6lJgW8e25WRJqKwkThFQHkJOaqB7M3MJARTIgUZaNCn1zs-suBZaeKbxn9uLxViBAc5stSB6VYdYsgOrIfk8Q2T6AYZtzJrs9rb6wMmr-moqoTCuziPIJZA4y-UdrBK9UlKtecfD2e8HXW5Lmay3PCnz6H8u_5yqX9c0uncgJV6G7hUW4GiPQ3NSzB6DIngO9PjPgiGSY4rt1vB5wt5tjaQ4_cdmkhWC4NEb0kt_yTHbs9u4c4ToiknE8smPY7j_-vjYrrX418lfbY3QSV4TwL4nH9xgh4D2y0pTD5Uy9hpZWVrscNO0y_j_YZUxC5sRQjie2K1o9DroXF2LdU9oOwJaCkxAsvrW-T-u_NNT4tcLYmAHBtxaFXHA8FYWCDvwZpAnqb3ZcyUnH-FrtpIFb4RNWek8Qa1f4lRKIBFSLbyvKW3E-TP6E4UvNBMiQEIa_ToRatuYxrWMvVVqph58lioVSf2wkGLqO5CF1fBHRcGxnFJz3kZ0QrP4gIyKb_arjtDE6bYwOMnBgc9x9D2JKO7zad98uOPdT2mYIS56FYzQuUhANxK7nud2RkNJrx7uEdbKU0DRD2WJihmvrQ46VXlS-URkES0cMmtqKBGhQlsXWguQM1pGlP5tZ8kXX5fjQlgxIwiRvpTjoCfaly-WGn6EUSZFAYUn8UHT6GPQAB0Hguc27unfONhSPcmQ7gNA8Th036aFu3-IbWMhze3MSsX2P8gHmbZu8ndNC6iz0U0Cgkp9FrrRVpQr7qYiqPbeDWF0EUb5_ik97NFcKtDiNUpmCxjpdDh59HcADPasy9vaaIDyw6B5P-s5RZv_ONW92J8f1ie2urvp2kgEIKmepqMj0DoM5a_9A1rx7fsZ8RgfQvqxfkAdSduAHQKG-90_6meK9CljGUysxyAataUB1oeyC5EOQtFARVvAekw0fGuOqD4i4JR8OTjE-kuMIuG009wcPoo14kKSR59vM9rwwaa1s0Jgd2v0zO6q47V7joxMgbTZexPuCBTJmoePJqEc8Xcv1ksk_oVdaYmGyoE2a1V1iO6ivdObBfRx8lg_qaqk27nO2n7dJRYkfi7Um7ws5KISwCIYTF3pRSekVLNnkqrMG7I1ZLp5KYSGwNJIBbRPZCwrhM0cMoL5XqdIWCrdhG0jwdwsT1hW31Yh5qjIN7dqE6oU6XjkI4Z1i2yJLDaaRz2FUUx_DhwXFLiv2GhUQBApjBahvY60Uum7E3FbTg2Z1H7ivtqBbOwb0FCYJ8yTrMsGgKz0wnef2mruK5KBAz_lgnchENCU9rGHKtvbvq5YSGxwQHg00ggTLhek9AVmWNVCffIuP8XURR6u5h5jq49gyOkknQBHLbk1Hx1rVT-qKE3BIYxBvjJFgutWxdA6BVJtSb5a5AgpKUufD1UHHxLClqkf0ts4JMS4YfKpKv66h1R6gDWimTFClqKnbQA5MYI2pAKCqDiBdSNUfM_07EB2UZ-BXqhobQ_ok8GPCuEx8v6uMB3OC3uqudv9b_AEAxA2Yy7jTWd1gIDCwuue2-dX3auglLcxZKHOSF5ilW3hklU3WFlU3bosSWyEvWtkaEIY4G2RaawHSvVltMYEGgZlu8bcEPWUdJRwcoxyax6AI6XJTF3Et9BiF1OtT628dqI1KNz4S11-m2aKOgZW3QpgrLHpbql-Rg04Uphf1P__6N0Zv3VfFU9QbNIoeTOje0AU0OT3F9Ws_xXX2uzheYt_jZLPk7FdSvMTyxNjX8zxjIbWv47CI7oAJFfWDUNBbW5Mu83TDrI-erZ88fQf0jYYdjfY3E18NsjQxRycWDDG6NBs-C6sA3YWNOL0kvD89oKmfe_jYVeNtifmklbiRL7I9uxLXjfOur8T9kcz08YuE3fC0n5i6X84PRH-VeTCxwcr8QHok5j4jdiIg_QOrkHUl8WIWUZs5Dre5IyLhRKFDA0LDGFJ9AAW0Kt4vHOncEDhe2cmZIXD3VcrTEHgaAk9D4GkIPA2BpyHw_-khsE0dlhDXIVzKaQj8Gw-Be_x-jNkH42DdU9EB-hjjT1PiaUqM0cS2CZUAbv3E_QNPiQ_LzmlSPE2Kp0nxNCmeJsXTpHiaFE-T4mlSPE2Kp0nxNCn-TSbFH7_8L30_5GU)
