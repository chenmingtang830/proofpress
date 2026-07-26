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
[//]: # (proofpress:capsule:eNqtWtluJLcV_RWi_ZCHtDS1L8pDINhIbGQmdpKBg8Aa9LBIVndZ1VXtWiQ3BvPvOZdkLZLGJY26AS-9sMjLu5x77ml9WvGmK3Iuuk0hV1erw2GTKpH7qecGnuMEgZdFTsjdLA5X61VWy-NGFlvVdljb7rgXRldJJINUeWEaeMpLUzdXKU_yXIUiSWSeeSp0eJrkqQyjNEySOIllnCaOFHhGJj7HvrJoRX2nmuPq6hO96TYd3-KEknd01BovMlXig59VU-QFz0rFGnVXtEVdsR3W182RZUf2U1PX-aFRbYtnDlzc8q2iSz34uKl_Vbhu39CGu647tFdv3myLbtdnl6LevxE7Ve2Latvxapv4zpsHTzfqt77A603fqmYj6qpVFXzRNb36vF7tFCcn5lwqKbJ8ZT7ZqDu9CM5Vm8yVSRoGQZpH0k0z33OwOEwlWVY3HV1tUxaVguVDRMqNL_I4cpzUjT3fzVMeBUGQ-EKa61jrNoIf2r7EhT2yU9SNbFdXv3xa2eM_rRDlumnplflayU0Gl_-y6qvbqr6vVh9whyEfcLSsRfvmb9f_utzTSV-TKLzrmiLrO8Rnk_G2aCldVJlveAu_dUrv13e7uiFrbouKtmyPbaf2-KbiewrbYNUaj7YU6tVV1ZclbBQ7xEaZ22VlLW6xWsQ8TL3Mw3KEpVO_0w2mhGC4B76yR3EplfEeskjd45Nv2JO13fFAZlAIkQ6rz-vpMI74ZaErHxz2Q8s6JCP7tW879veiY1mJi7C60W9y_J8c-tdFK75hL99lwb404irIcn5u-_5ZX-rFjdrzoqL9FGvrvhHYJh8rkbYStVSMVxJLD3Vb4PPJ4gNv-ANzvThKRJZE5zb3x4rWft9na21pXpTGpqJr2VBtzJYN6xp-p0osbOp-u2ML5oa5izJ2nkR_lkHfej9daxsphUslt4rd183tC4L_sk0WYh-Frpc6SX5m697veMcQDs4AfXlfwpG8rLfHNavqDp8COg-8K7KiLLojEyUv9pfmIC4XfMl9GQZOHj-w9r_DWaLreVke2d2I-8958JlHF_wm40BmWeycxZL3SDdVbQHk2jE9-hizqMXypt7rfBwQVeekVJ1q0HeKdsFbSc4jN-LpWWz8t-ItGtgaJUodUcEGtDZBoI0PySbdMFgh0T-KroDpvIHVhO0LNsa-l7pO8mU_0rXRLFHRewBE-dJofuGxhUgmMvBS5YuTLZiVzJ7fUgj5oesbeGqAOoDgAS7TQEIeA3kA68C7ywUP-b6UueThyfZd6_g0dQnTikqUvcZcNuu-THdf1vZix3iLlLwrmrraEyH4Y_tEGqaJjJIv2JcD7veKeCDr-P6gmpbdgzppqw2Qviiiz2-jgR69o-RCaacshzwO8iyTTnR2k99PFv2JnIwiBe7pF9tGIx1FvNXlS5UshC4XLMnqBReDMAVuHodntxe43lOKsrbYVly_KvlRUUPuS1Q0SBdVswCzxo6ckFtnG3L6dillQ-XIJPbObu9_YCaCydBLgJWyRrCpn3SqRIexSAbrram6g-_qUipKjgV73SjJhXIfpvC3qA1aWZbo86I-EKJliu1Vs8X1yei6J6rxTAq_dJvuuYajuOeHPj-7jf9T7SX7qB-5QAFVH-G3SramSe8BCrxCURF0EAeYiBCdtsTS_Dzzleee3d7vCoyLDdKSGF1P4GQ6DSUC9qb3lwyFeLS8k32EK4HCxTKMKZkFnGdfgLEdxygG-orcpSzFetSr5kGUVjnB8Etg7AXb9BW_40X5Avoh3NwLY0-d3dprdsfLQk5x1kXUdgUqjFgffPtD146wKxBQBNA0tiUE434Uuzw7u72EuHaZhhDQpxLgavchiwkvzAT7cMI4ssWm6ynh8MfZcDT0tb2lxvn27TvW1Uz9jqpBmtHxErn5PEt56S5LpMVTfuIH4bntuzaPUVgPTX1XEEUYKHxj7KDZrbuvWVshB3Y1VZthPgvulMrlbho9bAjf1aZXPx2uSsVvcX5xR33n8Iw_X7oNePQBmUvTps67YtnDbiCcyHHys5s8o4lFO45DFZpXyzUJs3JLc8mupzqDCQjiEpF2Eo9nLj-7vdfVkZot9VGKPu3W8Ptpx3Eu2fOR4eqZGUc9tvfDetCXVnRfEnwE0spIPPqbQS9a1L7gNL3nYIKVwAy7OtSFBnrTC4wKNLwjEegDaWdlIY6zHeZ62mwTrdS9Umpr67zboJMCx-Bmq-i1mXvlR4mfeTKIM4xnHg-iJI2FF_EszGNwkDiNfC-RcaQiP4xSL3e4cD2P51KEQrgx2dp2vNPKnInWlRd_hqNJNvMcL7pw4gsveu96V45z5SV_xn8dmq-sx-eS4-fZp5_OI-bpfDRi2463O8LSLAriJMqTyCX813vM9Debqi-T1OyWUaiCzAn8WHly2HKmsg1bnqiP2cO4isMocXgY5-5w2Ewys4edInYVagRRiws3Fa18x5tbWd9XejUFvRDs-_fv3s6UmCE07RXTh2shlwYLdSCWblWE9U1Fjys6047xWo3-rSd6z0s71E-zPKwvqP-WGpLaXXGgVoJPb6rhxC_NrNZjaZRlCG_OY2eM-Ey1sx47RW_DLQtYctQcFQ_ALDx5QKkzEt3BV-HRH_uupQ6GU9YjbuljqL8J3uB5HSZKiUOfARSGQF3eVLN4jIOGHTFpx4XrIzNdx8ly1Fg-XH-mAj7IzlcLePasWCaBH_FQOEk4nDXT9OxZp8hxkowjNYO6StXdVEBsadKm1ebuwa35g_wd0lBTDiXMLy8DSKMaxgtO2YRw_exOjtYmGAv0FF1jUuTGvLUeVpWZTuuGcnONfIBdA_ezustChPI45gBuKVMZjPgxaYtThL5eILQnJImKM5WC8_J4OGGmGY5xeb3wR2M5WWQkhZvqfqewuhnow1D7xpUkSXViZyZjYoFE4zFGt_UgSdhCu6lGsWLNdEd-gAIWHiSc0E0WjkeSIxbcrhInjKMwjXGdwSkzkdI65RSlMes16hkCdFP1VUn5mHFxi4-zI0C0qakl42r0uFB6VATUUeLSe2aZsp1AxoQkRe-mwjd7rJAKIwudDvcTTVYVMzn8x1f3EpUmaOae4zvD1Wfa59OMe5mIOaBAkoBH4N-Yj_1wpms-_X3rqwVKSpdHzlD0G6xuS4qmcKbJkvEHM9_ZCB2pPtm2h0sQF6skmRXILXXHNarMKfA9n4xbcqpQUZCAjEiZDNeeyaX22qfonhdYpUjvQgfd8aaC76aPGP1IeTH8SKkvaX-FvGTvirbVwxJ9Nhyl_Wp9jY680yKbVSno92n6GiHoEGCCyUzRDtue8HfJDUks88TxvcCZymqmyj7OrVfIqbprPpOCXPIkiV03UN6Y4JPOOgO81wqksNfgDjKTYIoYDHxpIOoeT8NWeI3owwhIGsEekqt5m7EzLvW046Grtw0_7EACWiszwgtIFFhurBykz2lCWAhKIP0gAgVKwd4Hf8x03CE3TxBg1XHshDfVgbqE6EvejDGkAqZKJQbcyAtacQTk4zKmyIyit6UyNO42hf6eSB5wEn0JSVEbWWaoZNuY77V1RhUyYMjobyvqe2MkmYZ6yuqeqGSNLs8ozcyZ5of7Bc9xJUQgeRCLiI9VPSnK1nOnSME6sTXJZXStBhce2efgPV0SHFtST9WFPsu3gSWy77TjyI6BfdxUdn-CjzXBTkntR6NDvS_0nyaw4Q9DDPFqCnKNPXBMN3QbG2mqtjV9T_CzNgrGCzIwDkUqFHdAEce5ZaZ0T7BwqkQ90F5X5ULEys_SscXNVGt73ilyczukIzH2iTuOw1TTtSOVpWcsk6Kvt6rqiWbp8ZQIQg62T8hwncPduoLGDAVL1ZjS1uWdxb8BnQfJeW2v8NEQh2ZY1_aHQ1ko4NODeaKwVozzGdv3ZVdcGFXCoNRCJDHuuolMuMPz0bMzfX0Qe04QxtuPhlg1On_1NsLGfgiW5e8fF-yU9OdbOQYSOU3KM139USM6iyA-5LoT8VyG4D_TyDXTyEe0fb24rTt8sadH6ZXuQRZlphr5CLvb2d-AvTHXWfKZm-YqCd08i4MR7WZq-axvvlbmJr76-yV7W2tCUhDXwsXKurWPX9QVeOxAAelhG4q6vu0xW4G4kLYwQmxRaS-alqQeZfqRqX2mSJYiJs0funoJ9KXDnSAKETI1UblRhJ-nzgny-TCHyDRJsjhUaTYOZzNFfciWE7RwzTQwO7fEj7NyDlYTKbbS2zAZrydnAbhknedrfa9CwPutIo9R376pMtXdK1V9YeIxHcxMktLMJOunY-NAsqg3UrkP8-J8UBzNtSC6hE6KWJ7AvBupCfdHwX8K3auVep1YzzQfL_K4z7lI5WjETMJ_OgF9tfYOg2Z1goDKfdF1Os-NNDZISI9l6b_oTmo4gm5iCFCGr-yG8xoa-0NJCXa0U2lnhlIq2AIru8GypaDEGfeTMFURCmuk49NPBGOKv17bJwsu2T-UOgyRw4hkMUADiGEqWt4nNyPGFXngCExFawfuYqDCqU8u8eEz_vk_hCkDeA)
