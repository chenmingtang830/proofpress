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

[//]: # (ob:c4147335)
## Why not use `MEMORY.md`, a local vault, or a shared memory service?

[//]: # (ob:c523bff4)
Those are good solutions for workspace continuity. They retain broad context,
support retrieval and injection, and help later sessions continue the work.
The handoff boundary is different: a recipient may receive the artifact
without the original vault, permissions, identifiers, or retrieval stack.

[//]: # (ob:26b6010a)
The two layers complement each other. A vault can hold private working context,
unfinished exploration, and material relevant across many artifacts.
Proofpress carries the smaller record admitted into one shared artifact:
accepted transitions, reasons, consequential rejections, and attribution.
Memory helps the next agent continue the workspace; provenance helps the next
recipient understand the artifact.

[//]: # (ob:3cce2ab9)
## Why not export selected vault context with the file?

[//]: # (ob:c3264cbe)
That is a valid design. Once the exported context is bound to a particular
artifact and revision and travels with it, it is functioning as an artifact
provenance record. Proofpress provides a portable structure and deterministic
checks for that deliberately admitted subset; it does not claim to be the only
way to package it.

[//]: # (ob:484a7c94)
## How does Proofpress complement OpenWiki, DeepWiki, and Open Knowledge Format?

[//]: # (ob:95be06b6)
| Layer | Primary job | How Proofpress complements it |
| --- | --- | --- |
| [OpenWiki](https://github.com/langchain-ai/openwiki) | Generate and maintain an agent-readable wiki from repositories and connected sources; it can emit Open Knowledge Format bundles. | Record which generated or edited artifact revision was admitted, why, and by whom. |
| [DeepWiki](https://docs.devin.ai/work-with-devin/deepwiki) | Index and explain a repository through navigable documentation and question answering. | If an explanation is exported or committed as an artifact, give that artifact a portable admission trail. Proofpress does not attest DeepWiki's internal state. |
| [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/README.md) | Represent linked knowledge in a vendor-neutral Markdown and YAML bundle. | Add accepted revision lineage and claim-versus-diff verification to selected artifacts in the bundle. |
| Proofpress | Preserve and check admitted artifact transitions. | It does not generate a wiki, retrieve context, provide a knowledge graph, or establish that the content is semantically correct. |

[//]: # (ob:c437b5ad)
They can form one stack rather than competing alternatives: a generator such
as OpenWiki produces documentation, Open Knowledge Format organizes the
knowledge bundle, a wiki surface helps people and agents explore it, and
Proofpress records the acceptance boundary for the files that are actually
shared. Not every transient generated view needs a snapshot.

[//]: # (ob:21881140)
## Can Proofpress manage an Open Knowledge Format bundle?

[//]: # (ob:cf2aa037)
At present, Proofpress works at the artifact level. An Open Knowledge Format
concept is a Markdown file with YAML frontmatter; Proofpress preserves
frontmatter at byte zero and can attach a portable capsule to each selected
file. Proofpress does not currently validate the bundle schema, graph or link
consistency, or atomic admission of a whole bundle. Use an OKF-aware validator
for the format and Proofpress for artifact provenance.

[//]: # (ob:cb554e1a)
## Does a DOCX sidecar provide the same revision history as Markdown or HTML?

[//]: # (ob:94228968)
No. Markdown and static HTML can carry a native portable revision ledger.
For DOCX, Proofpress currently verifies semantic evidence in a separate
provenance sidecar. That evidence can travel with the document and detect
canonical-content drift, but it should not be described as an embedded
revision history.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzllY2YzOTIxNDIwMDQ0MmI2MDVhMWI3NSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjE2ODEwMWZlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8zYTYzMmExYWVmNTQ1NjBmNjA3YmQxM2YiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzNjZjc2MDA5MTcyMzFmOWE2NDQ0ODNjZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVtz48aV_iso5SGbWpLC_SI_bKk8tuPyTMZxZpN1WVOaRneDhAUCDC7SMOP573tO3wCKJMSRmNRuCg-2JRJonD7X73x9IH-6IHWbZ4S2tzm7uLrYbG4TTjMvcR3ftW3fd9PQDoiTRsHF7CKt2PaW5UvetHBtsyJuEF4xl8VeGIWcuhHJfJpkEWWZx5yEhJkdx4yQNA1SnzkZ8RyXhixMeBIQL7DT0I0cWJflDa3ueb29uPqEv7S3LVnCEwrS4qNm8EPKC_jgr7zOs5ykBbdqfp83eVVaK7i-qrdWurV-rKsq29S8aeCeDaF3ZMlxUzsf19WvHLbb1bjgqm03zdXl5TJvV126oNX6kq54uc7LZUvKZezZlzt31_zvXQ4_33YNr29pVTa8BF20dcc_zy5WnKASnTB2bCfjF_KTW34vLgLl8luPhJ5LHMKzwA9COwvtKGWOl6FkVd3i1m6LvOQgubZIcevRLAptO3Ei13My0Kvv-7FHmdyOku6Wkk3TFbBhF-WkVc2ai6tfPl2ox3-6ACtXdYM_ya85u01B5b9cdOVdWT2UF-9hD9of4NGsos3lt9d_XqzxSV_iKKRt6zztWrDPbUqavEF34UV2SxrQW8vFel27qmqU5i4vcclm27R8Dd-UZI1m01LN4NYGTX1xVXZFATLSFdiGy92lRUXv4GoakSBxUxcuB7O0_CPuoHcIC_YBX6lHEca41B54EX-AT35n7V3bbjcoBpoQ3OHi86x_GPGTLA0ctvOw7xurBWe0fu2a1voub620gI1YVS1-yeC_qND_GpXid9bpq4zIl4SE-2lGzi3fn6qFuLjma5KXuB63mqqrKSyTmUjEpWjFuEVKBpduqiaHz3uJN6QmO-K6URjTNA7PLe7bEq_9Y5fOhKRZXkiZ8raxdLRZKmystib3vIAL66pbrqwRcYPMSR1m71l_4EFfuz9eCxnRhQvOltx6qOq7E4x_2iIjtg8Dx03sODuzdO9WpLXAHMSC1Jd1BSiSFNVyO7PKqoVPIXVuSJuneZG3W4sWJF8v5IMIG9El8Vjg21m0I-3f9LNo25Gi2Fr3Ju8_pcEnbh3RG4t8lqaRfRZJ3oG78XIJiVwopoM6ZqmsZWV1tRb-qDOq8EnGW15D3cmbEW3FGQmdkCRnkfEnThooYDMIUayIHGSA0kYxacOHKJMoGFbOoH7kbQ6ikxqkxtw-ImPkuYljx4f1iNuGYgkRvYYEUZxqzQO3jVgyZr6bcI--WIJByKzJHZqQbNquBk3pVAdJcAMqE4kENQbgAVAH_LYY0ZDnMZYxErxYvmthn7oqQLS8pEUncq41qL6WqL5W09GVRRpwyfu8rso1AoLj8tEkSGIWxgfkyyDdrzniQKsl6w2vG-sBoJOQWibSkyz69DIi0UPtKAjlQinjJo_8LE2ZHZ5d5He9RL9HJUOQQt4TPyxrkenQ4o0IX4xkSkW4wCVpNaJiAEy-k0XB2eWFvN6hi1pNviyJ-KkgW44FuSsgogF0YTRTQNawIsHMLbwNfPpuzGUDbrM4cs8u719ATDCmBbUEciWrwNhYT1peQIVRmQykV6KKCr6qCsbROUbkBQieUe7suvDXEBt4ZVFAnafVBjNayq01r5ewfRS66hBqPOHCpy7TPlVwOHG9wCNnl_Fn3iysD-KWOQRQ-QH0VrJGFuk1JAVSQlBh6kAM0AMhfNoYSvOy1OOuc3Z5X-VZxmtwS0R0HSYnWWnQEWBt_H1hQSBuFe60PoAqIQvn42mMs9SH3vNAGlsRaMUAvoLvopfC9RCvAgehW2WYhk9JYycs05XknuTFCfCDOpkbRC4_u7TX1j0pctbbWQRR0-YQYYj6QLfft41JuxQMCgaUhW0sgxFo-h2Snl1ezLjqMpFCAD4VkFzVOigx5gvZwe52GFtrtOi6nNrksTdsJXxt7rBwvn79xmori3-EqAE3w8cz8M2nUcqpq4yBFpd7secH55bvWt6GZt3U1X2OEEFD-FrKgb1b-1BZTQk-sKow2iTyGVEn4w5xknC3ILyqZK3eb64KTu7g-fk91p3NE_o8dRnA0RvwXOw2hd_l4xp2fGqHtp2dXeQBTMwb0w6VULwaIkCYolvqhXXdxxmIAEYcA9J27JLUIWeX97rcYrHFOorWx9Vq8tCvaPqSNTEIV_TM8KjH8r6faX7pAveLhA8Ft5IUj_hG80X8FprmOAl8P8lC5iSp59qE8SDBK0FpYk0tgqLAJLraVLlI9LIWSBZI_4Yk0HvkzoqcbgcrDPm0wSKCqXsm1dZUWXsLlRTyGKhZMXpN6lx5YeylLvOjFNozl_hhnETUDUkaZBFgkCgJPTdmUchDLwgTN7MJdVyXZIwGlDoRytq0pBXMnLTWlRt9BkUjbebabji3o7kbvnPcK9u-cuP_hH_b2F8pjcNVGWiS0TQDB-o__XQeMk_4oyTbVqRZYS5NQz-KwywOHcz_Yo0B_6Zc9TRKTS0ZBtxPbd-LuMv0kgOWTS_5Qn5MPYzwKAhjmwRR5uiHDSgz9bCXkF05N0lU5YWbEq98Q-o7Vj2U4mo0ek6tP75783rAxGjTNFeWeLggcrGx4BtE6YpFmN2UeDvHZ6o2XrDRf-8Q3pNCNfV9Lw_S51h_C5GSmlW-wVICn96U-omHelalsSRMUzBvRiLbWHzA2imNvYRvg13mIMlWYFS4AcSCOzcQ6haS7oBXQaNvu7bBCgZPmZm8JR6D9Y2SGu4XZkKX2HQpJAVtqMVNObCHaTRUi4krjmwfPNOx7TSDGMv09gcs4I53PpvAU8-KWOx7IQmoHQf6WQNOTz3rJXQcQ-GQzcCqUrY3JWRsJt2mEeKuAVuTHf_VbiggB6fy5EUnaYgGs8Hem8Bcf3V6RQsRpASii66gUyRSvJloVrnsTqsafXMG_gByaeyneJcRC2VRRCBxM5Yw3-SPnlvsLfTlBKF6QhzzKOUJYF4S6ScMOENjl-cTf9iWo0SSUrgpH1Ycrq41fNCxL1WJlFRLV7IzRhSIMB7a6KbSlIQKtJvSkBUzS1TknSyg0gMDJbS9hOaRqIgRtfPYDqIwSCLYjlbKgKRUSnkJ05h2IutJAHRTdmWB_pgSegcfp1tIonWFJRm2hrdTLlpFSHXouPi7pZCy6kCMQyKjd1PCN2u4gnFoWfDpoH6Eyby0pA8f37ob8ySGYu7anq23PuA-9z3uNBJTZ4E4BhwB_0TE1MMBr7l_vvXFBCW6yyNlcDyDFWWJYxduCbAk9WHJ75SFthif1rIDlYBdFJMkrwDf4vdEZJUhBH4gvXBjSqU89GMAI4zFetsDulRt-yW85xyu4sh3QQVdkboE3fUfWXhIOdeHlGKT6hRyYb3Jm0Y0S_iZfpTQq9I1VOSVINkUS4Hn0_g1mKAFA2OaTDmusOww_46pIY5YFtue69t9WA1Y2ce-9Qw6VVTNJ1yQMBLHkeP43DUO3vOsg4T3XIIU5JV5BzwT0xQiGNClTFEPcDfIClpD-GASkshgu-BqWGZUj4s1bbtpq2VNNisAAY2iGUEL4CgguZRSU599hzBiFJ95fggQKAH0rvUx4HG1b76AgOVbUwlvyg1WCdoVpDY2xADGSEUEXLM5XrGFlA-bkUEmGb0lhqFUtwz0dwjyIE9CXQKnqCQtoyNZFeYHIZ1khWQytHC2onqQQqJoEE9p1SGUrKDKW-hm8pny4H5Ec4RT6jPiRzQkJqp7Rllp7iVUsHBsAXIt3FYNGzboU2tPhASBJbGmikAf-JtGidYroTiUQ6OPm1Ktj-ljhmmnwPIjskO1zsVogqUHQyTwqnNUjXqgcTeoNsrSGG0z_B7Tz0wyGCd4YBTQhHJiA0Q0fcuA6e7Twkspag17HZ5RGnEvTUyJG7DW6nkvoZsb7Y6I2HvsaJqpum0MlMV7FJLCr5e87BBmifYUAUIGaB8zw3UG6hYRZDwUUKrIKU1V3Kv8p7OzppxnagsfJHCo9XVNt9kUOYf8tNNP5EoK059Z665o87lkJWSWGrEktLtOzGJik8xodsCva7LnBcR480ECq1r4r1iGKttrYyn8_mFETubywM6gIWF9pzzg1R8VorMQ4trX7ZBkLAD807dcA47cZNvnk9uiwudrvBV_EjVIZZk-Rj6A3M1gBuxSbmdMZ06S8ThwsjTyTbYbsOWDuvlcmhvx6seF9boSgCRHrAUbK6pG3T6vSsCxGgLizcoUVXXXQW8FwAW5BZNi81JoUZYk_sjTtxZfpxxpKUTSZFfVY0mf2cT2wwBMxnsoZ0j4oeu8gD7XfQhL4jiNAp6kpjkbMOraW17AhQukAb1zg_g4LYbJqgfFinrTnfGsVxYkLlZl2UzsK6eg_YajxrBu35Qpbx84Lw90PLKCyU6SyZ5ktt82apCFtRHDXfeLw0bRiKuS6Fh24ojyKPS7Ie_zviH8e9M9m6kXjvVE8XFDl3iE0IQZIQYU_n4H9MXcOwg0iBMwKFvnbSv8XFJjmkJ6TEt_JSqpxAiiiIGBUvhKLTiMIVMfCnSwrepKW9mUYsDmcGWrJRszSpQSLw4SHkJgGTjeHxEYF38-t48SLKwfON9oy0GLpHKASCASqQh6H9UMNi5RA1vIqVDaIe9CQwVP3dvE-8-4jwNzqFCqWjOFiizqx4v3YqaVdXT_80dTq31SntMi_-cOr6pO8VZ3iofmVwXI6MdXvxZinzi86jt-5HmHD_8gQVkf3nzz5u1PP8NmPkD4q3R-TwByzKwTTyefWgZhkrAgBMCar4cDmwfPqwPXS7PMP7vI70RYIMxZVhW0JFUhTCGZSVHTN0jY4kNzQIDt1kCgloxNL4RgY8cm_wR5uagYostrVCEX9AknkHZFu4HJRywlag8Gp4ywsfNqSjnEdnJQXigiENDYxEg6Ta2tSsZDfqJLPLWMohBGqALjDZ4b-jTlZ5e257kl0GMcO-SF9RaZPdHufZQAzqzXt6kj2vVjn0Q02fXeP0K3KzDRoKgMzPkWsO3f8rt89oR2T10GWk2-kT9hQX-7eWKmO0i5DU58dpF_s14LguI3WCRf4xHMr1UKv-HaB5dtEDz-dlP-Zs3nvczy2HXHKXwvSgPCzi6xiHeMJEgJawvrHWAyaAIBTq0kQ1CKNXkr-QTRfrc5tHRXYyMirhPHjuPbewNOOzRriUce8CFKav1gDnZOGBo7ZZlvYUfg8Sk48NNBl7mE2F50dnmvW41TZsO1RPIFjLp7hlFAXS8gwaknjM2VpkHg80MDDcR69fbr_7HwbI-S2oBzc5QHkp0yM3LCMrvvDJHGeiLofNeNk0ejsOcQGQ-Xjx4G94eZxJKO2wM4ue7jGQyJ9I9hikdSqGGLayYJs76mirK_tapUHR0vjlX8wwt-M2jZVL8jUzHklMWxYnx4qVfY1pTLLm9WB2u-PKkyPiiPbJBnWhwrokd1IFxbVhHMFjvFaXGsyB1Zje4f489lMTLtXF_KeqF1VTtWosbtR9ivoJyynbdVVQwJyMWx-nF4vTdkc7A4vf3hW1mhds6Dmw2Sp-IAF4cdjiX-w4_6CxLLklyGkJFi76XzxbHkfHjNrwvYdbZFcVX6FNwdmHVxLGseEQ7Pvyza1YJ5Q_AzFznOaqDXkZSyoktkq4_TCotjiW5c1p0U0nBI1pADHi02SEFPx4pew5yGykBRSeRx_lvI3KET26eLh9VW5DdJNgoLHYixHSjwOHsgrX2XqzOBRkObAzVOfkWVJpSE2Ld3jVFJL-eXjJnxNMlsm9hZSmlmUyeADpmEmdHYcH5sODs1nCn7NPVpU5829WlTnzb1aVOfNvVpU592nj7t9In4xxPhjvv58MD3U9PvZxlxd-wkzeDyICAhib3It4mbBAHL7DBK3Cy2wyD2Mj-Gj9I0oUkGixOHxBlJOA0D59iGdkbcPeed7Vx5wZUTHhhx9-3U4TGj04j7NOI-jbhPI-7TiPs04j6NuE8j7tOI-zTiPo24TyPu04j7NOI-jbhPI-7TiPs04v4vGnGPEgLoNfZi3zVQbnBEuD_i_sVne1AtIU5z-oQnuRHzWOLbyYBaGhz8GXs8_8QO9JLWFTFtCpIz8nQdv4ZcAeqVREipSBnZ9ax4sbHw7_hiPRJ1pNEP4Gb6ZHFTvjswM4KOw3R-uALNgKvkG4x8Mb0Mv3GkXIftJnSUyqvxU8hh0Kb26t1gFyqFmCl0gPVWlqd-G2r6YKQRT50gI1HipaYRHxxbDrz_ueeNLTfh0eu7g3oPLfQKEeLHTVFJRDRTkAk0LDkx2ZsACq0rea6w7fm2XYYIyaRc14A1VtLaROPOKLw4uZFeqZe6gkqm-boWWiQI21z1vydxdYNGBoR6I30dnUWKU4pZGVHS9rxFeOlXw3mE3fvECxDKT8CRQPmtYgetE2jAkAeJ4_uB4zLPALn-jHc_pl9-OKvdKs28kNMEYaQJ4v68do8V-_KD1gpzm8Hce1hEHboIZQnmUvVYyETmYp2sK4URBYZtRENqAm9gD-lEOw2MalqaYXYFvN5R0T7skUSQ7mVPhalJ8j-8yFPsAjjkfeOeTZc2vP1qJ9VLtA-bTaVCsFJAXoCMAZ-pvwpujXKhJAjTxMkAdHrGEoOT6N4Hnn2EfOAscdw5QpvEDvQWQRIYynRw0qxEetER8dza-Td--Ivewfv_OPCX0gEILwGu5uWc5JcVXImTP3-A-7_jpbCUSk25eNtGeAtG9BzfhBEOICaFBCE3PFVQrzyVpYwneR7RCBtjluRg-tHTWABEv1k_yTz2AJ3xCnG0kIdhnpfvnPQEpfF75G-0Y0HnstpKY6Vb-LlaL5RGtCV7jTD4BHeygL70Erf_PWIXca9-iY0MoY0-DgCYmC_JEKDLFhdvFKcB8pfmgYuXanDhTPZa2ILIa_Omj3dxSrNWgbEbnTNrKSsl9pUm6AdvBTHd5EHg58VO5Jq4khSSceUhFSL4tMXAZ_Zsc9CBvquqZcG_LqqO_QgYAacELg3NPqekRb7_Erqf9BK96LK6yy5_-ub61ZtvAD39QVhZv08FQB_Z0v4UQmgdEhKr6nnJO9hXsXs09fP1m9fKY1C3OE1pKprxCc3_q1G1fD2XE2pzxCWqYafSFJBcTA0wBVczs-Y5qKGBcvEX2Yr11GWf3YypBhVW-MEg2y1NrIlwmmkcww1yGLzr2KtHsEYC93DxPiMODwr3kEhdnJqgd-mBQsnaVzVy2iDCoXESnak8z4N2ijos6U9O-wmTHh09ezSE6E0jMdPRFRSyxuRaS7091uxG1exIyoCYJWX-D4mCbspeQdJiM6VWeE6dEQM1NrzaKOpFpLRGITIuaqVos46cLEkXE1XSwFxZ4yREaHSQcnN8g6QrYq-F9adKU9DSIdBGfW7DiQUAQFy06vr91dHG14sZFDo7tE0TNxit2aVazjUTo4nGmAaeFyYJ6YnGwZiMbn1fMN_yWCxB1qPuJXgyqUB00wLmiIQA1ahs15jq6q928YtiTG7KwSUoRLqF4PsHryvFxAmSHhE-OXAgXEnwrxOFpPAOp1s1gIzHd4PO1Yw2Q6pYk5mMYwxjTIA3Pb1M5fkFxMga2tw-v1cZejR0Gn1O-u9GGvOHb-fkAR1PPQ-PJ41rStM-mgLHbw_O4B9HVtQhWRrFWeAanxuMGz16s_g5c0LGsCAbjh2M-6FDvBRcME5jPzGwqp8lGoxJPHcISNURQalApwPOKDa149ADU0typjkwyC0KmnppnO_AbaUf7NbFGZW6AQVTEwimC9E50SBuKpkVgPRIqujEL44sDImiznzQKVPxrgKF1s1gDE2dYNv1eLx8-uMA0x8HmP44wPTHAc74xwH-ff8IwJkGx9cVE_z-HkQ__Jrg_mthgwXUG0aIEF5Bci9_j4dZ0PEgo6f7wMfd684UIaKSI28Z_aTG0vBqsxZeL6vV3vN2HvNlbwSN_E_XDr4RZEZNn34j6F9gtNNfbzIjtma5K-fz4Rna_3dTw7tbOjQ3HF559oG5YfN_45vmhqe54WlueJobnuaGp7nhaW54mhue5oanueFpbniaG57mhqe54WlueJobnuaGp7nhaW54mhue5oanueFpbniaG_63mBv2gyAOQj_O_NSb5ob_b80NV7RZMDzmXIAeMEPNMWzm4iMzVTwNFE8DxdNA8TRQPA0UTwPF00DxNFA8DRRPA8XTQPE0UDwNFI8MFL___L8abyo9)
