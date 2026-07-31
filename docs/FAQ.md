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
That is a useful architectural analogy, not a compatibility claim. The
[C2PA Content Credentials specification](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html)
defines a standardized, cryptographically verifiable model for asset
provenance using assertions, content bindings, claims, and signatures.
Proofpress applies the "provenance travels with the artifact" idea to admitted
decision lineage in knowledge artifacts. V1 does not claim C2PA
interoperability, cryptographic signing, authenticated authorship, or complete
capture.

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzllY2YzOTIxNDIwMDQ0MmI2MDVhMWI3NSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjNiODNkNzBlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9iNTdmMzMzMGFjODhmOWVhNjVlZGFlYjciLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzNjZjc2MDA5MTcyMzFmOWE2NDQ0ODNjZCIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXVtz4zaW_issz8NsaiWZ94vzsNXVnWRSSU9nk96ZTcVdbhAAJcYUqeHFjtLp_77nACBIyRKttpXUTgoPk7EoEjg4ONcPH9UfLkjd5hmh7U3OLq4uNpubhNPMS1zHd23b9900tAPipFFwMbtIK7a9YfmSNy3c26yIG4RXYRjyMLKJnSaJT-PYczJi-0EYBw5x4tRPApLYLGZ27CahR2Mvtjl-4UWhn3jUhXFZ3tDqjtfbi6sP-KG9ackSZihIi1PN4I-UF3DhH7zOs5ykBbdqfpc3eVVaK7i_qrdWurW-q6sq29S8aeCZDaG3ZMlxUTuX6-pnDsvtahxw1bab5urycpm3qy5d0Gp9SVe8XOflsiXlMvbsy52na_6vLoe_b7qG1ze0Khtegi7auuMfZxcrTlCJXhp7LLL5hbxyw-_ETaBcfpMGUeZ5nk1AU1nCSRhwRngaoWRV3eLSboq85CB5vyPFjUezKLTtxIlc0G5CQt_3Y48yuRwl3Q0lm6YrYMEuykmrmjUXVz99uFDTf7iAXa7qBv-SX3N2k4LKf7roytuyui8v3sEaenuAqVlFm8svX_z3Yo0zfYqhkLat87RrYX9uUtLkDZoLL7Ib0oDeWi7G69pVVaM0t3mJQzbbpuVr-KYka9y2XqoZPNrgVl9clV1RgIx0BXvD5erSoqK3cDeNSJC4KZoTbEvLf8EVDAZhwTrgKzUVYYxL7YEV8Xu48hfrwb3tdoNi4BaCOVx8nA2TET_J0sBhO5N93VgtGKP1c9e01ld5a6UFLMSqavEhg_9Hhf7XpBR_sU4fZUK-JCTcTzNybvn-Xi3EzTVfk7zE8bjVVF1NYZhMeyIORSvGLVIyuHVTNTlcHyTekJrsiOtGYUzTODy3uG9KvPdvXToTkmZ5IWXK28bqvc1SbmO1NbnjBdxYV91yZU2IG2RO6jD7we6PLOil-90LISOacMHZklv3VX17wuafNsjE3oeB4yZ2nJ1Zurcr0lqwHcSC0Jd1BSiSFNVyO7PKqoWrEDo3pM3TvMjbrUULkq8XciLCJnRJPBb4dhbtSPvPfi7adqQottadjvuPafCRRyf0xiKfpWlkn0WSt2BuvFxCIBeK6SCPWSpqWVldrYU99hFV2CTjLa8h7-TNhLbijIROSJKzyPg9Jw0ksBm4KGZEDjJAaqMYtOEiyiQShpUzyB95m4PopAapMbZPyBh5buLY8WE94rIhWYJHryFAFKfu5oHHJnYyZr6bcI8-W4KRy6zJLW4h2bRdDZrqQx0EwQ2oTAQS1BgUD1B1wKfFhIY8j7GMkeDZ8r0Q-1NXBYiWl7ToRMy1RtnXEtnXajq6skgDJnmX11W5xoLguHw0CZKYhfEB-TII92uOdaDVkvWG1411D6WTkFoG0pN29PFhRKCH3FEQyoVSprc88rM0ZXZ4dpHfDhL9FZUMTgpxT_yxrEWkwx1vhPuiJ1Mq3AVuSasJFUPB5DtZFJxdXojrHZqo1eTLkoi_CrLlmJC7Ajwaii70ZgqVNYxIMHILawObvp0y2YBDDR-5Z5f3BxATNtOCXAKxklWw2ZhPWl5AhlGRDKRXoooMvqoKxtE4JuR1wjij3Nk14ZfgG3hnUUCep9UGI1rKrTWvl7B8FLrqsNR4xIRPHaZ9LOFw4nqBR84u44-8WVjvxSNzcKDyPeitZI1M0msICqQEp8LQgTXAUAjhbFNVmpelHneds8v7Ks8yXoNZYkXXYXCSmQYNAcbGzwsLHHGr6k7rPagSonA-HcY4S31C0gNhbEWgFYPyFWwXrRTuB38VdRCaVYZh-JQwdsIwXUnuSF6cUH5QJ3ODyOVnl_aFdUeKnA37LJyoaXPwMKz6QLdft40OuxQ2FDZQJrapCEa8MHJIenZ5MeKq20QIgfKpgOCqxkGJMV7IDna3w9hak0nX5dQm-9awleVrc4uJ89tvX1ttZfFfwGvAzHB6Brb5eJVy6ihTRYvLvdjzg3PL90I-htu6qau7HEuEvoSvpRzYu7X3ldWUYAOrCr1NVj4T6mTcIU4S7iaEV5XM1Q-bq4KTW5g_v8O8s3lEn6cOA3X0BiwXu01hd_m0hh2f2qFtZ2cXeVQm5o1uh0pIXg0RRZiCW-qF9WLwMxABNnGqkLZjl6QOObu8L8otJlvMo7j7OFpN7ocRdV-yJrrCFT0zTLUv77tZjy9d4HoR8KFgVhLiEd_0eBG_gaY5TgLfT7KQOUnquTZhPEjwTlCaGLMXQUFgsrraVLkI9DIXSBSo_4Qg0DvEzoqcbkcjjPG00SACqXsi1NZUWXsDmRTiGKhZIXpN6lx5YeylLvOjFNozl_hhnETUDUkaZBHUIFESem7MopCHXhAmbmYT6rguyRgNKHUilLVpSSuQOblbV270ERSNsJlru-HcjuZu-NZxr2z7yo3_E_5rY3-lNA53ZaBJRtMMDGi4-uE8YJ6wRwm2rUizEgBn6EdxmMWhg_FfjDHC35SpngapqSHDgPup7XsRd1k_5Ahl64d8Jj6mJiM8CsLYJkGUOf1kI8hMTfYcsCvnOoiquHBd4p2vSX3LqvtS3I2bnlPrb29ffztCYvqtaa4sMbkAcrGx4Bus0hWKMLsu8XGOc6o2XqDR_-qwvCeFauqHXh6kzzH_FiIkNat8g6kErl6X_YyHelalsSRMU9jejES23vERaqc09hy8DVaZgyRbUaPCAyAWPLkBV7cQdId6FTT6pmsbzGAwy0zHLTEN5jdKanhebBOaxKZLISj0G7W4Lkf7oRsN1WLiiBPLB8t0bDvNwMeyfvkjFHDHOp8M4Km5Ihb7XkgCasdBP9cI01NzPQeOYygcohmYVcr2uoSIzaTZNELcNdTWZMd-ezMUJQen8uSlD9LgDXqBgzXBdv3DGRQtRJASiC66gk6RSPFmolnlsjutarTNGdgDyNXXfgp3mdihLIoIBG7GEubr-DFgi8MOfTpAqGaIYx6lPIGal0T9DCPMUO_L04E_bMtRIgkpXJf3Kw5313350Pu-VCVCUi1dyc4Yq0As46GNbqoeklCOdl1qsGJmiYy8EwVUeGCghHaQUE-JiphQO4_tIAqDJILl9EoZgZRKKc9BGtNORD1ZAF2XXVmgPaaE3sLldAtBtK4wJcPS8HHKRasIoQ4NFz9bqlJWHYg2SET0rkv4Zg13MA4tC84O6scymZeWtOHjS3djnsSQzF3bs_ulj7DPhxZ3GojZR4E4hjoC_hcRnQ9HuObD861PBijRXPaUwfEMVqQljl24JYolqQ9Lfqd2aIv-aS07UAnsi0KS5B1gW_yOiKgyLoHvySDclFIpD_0YihHG4n7ZI7hULfs5uOcc7uKId0EGXZG6BN0Nlyw8pJz3h5RikeoUcmG9zptGNEt4rZ9K6FXpGjLySoBsCqXA82n8GraghQ3GMJlyHGHZYfydUkMcsSy2Pde3B7caobL7tvUEOFVkzUdMkDASx5Hj-NzVBj7grKOA91SAFOSVcQcsE8MUVjCgSxmi7uFpkBW0huWDDkgigu0WV-M0o3pczGnbTVsta7JZQRHQKJgRtACGApJLKXvoc-gQJjbFZ54fQgmUQPXe62OE4_a2-QwAlm91JrwuN5glaFeQWu8hOjB6KlbANZvjHVsI-bAY6WQS0VuiG0p1S0d_i0UexEnIS2AUlYRlek9WifleSCdRIRkMLeRWVPdSSBQN_CmtOiwlK8jyFpqZnFMe3E9ojnBKfUb8iIZEe_WAKCvNPQcKFoYtilwLl1XDgnX12WtPuASBITGnCkcf2VtfJVqvhOJQjr76uC7V-Bg-Zhh2Ckw_IjpU61xQE6yeGCILrzpH1agJtblBtlE7jd42w-8x_MwkgnGCBUYBTSgnNpSIum8ZId1DWHguRN2XvQ7PKI24lyY6xY1QazXfc-DmpjdHrNiH2lE3U3Xb6FIWn1GVFH695GWHZZZoT7FAyKDax8jwIgN1Cw_SFgpVqogpTVXcqfjXR-cecp6pJbyXhUPd39d0m02Rc4hPO_1ErqTQ_Zm17oo2n0tUQkapiZ2EdteJWUxskmnNjvD1Hux5BjDevJeFVS3sVwxD1d73m6Xq9_cTcjKXB3YGDQkbOuURrr6XiM4CiPe2bockYwHUP0PLNcLIdbR9OrgtMny-xkfxL5GDVJQZfOQ9yN2MOGCXcjlTOnOSjMeBk6WRr6PdCC0f5c2nwtxYr_6ysL6tREGSY60FCyuqRj0-r0qoY_sSEB9WW1FVtx30VlC4ILagQ2xeCi3KlMT3LH1r8XXKEZbCSprsqnoq6DOb2H4YwJbxoZTTIPzYdJ4Bn_d9CEviOI0CnqS6ORsh6r21PAMLF5UG9M4N1sdpMQ5WQ1GsoLe-M54NyoLAxaosm4l15RS033DUGObt6zLl7T3n5YGOR2Yw2Uky2ZPMHraNfZGFuRHdve8Xx42iFlcF0anoxLHKo9DvhnyI-xrwH7buyUi9MKxHko8busQjhCZMCzGC8B92QJ-MvYNAIz-BDWXrvG2FnUtorIeQ9mHpz0UmlTWCSGKwQSl8pQYc-5DODwUa2FZ1pa1sStFhc7iz7SWb2pQoJV4cJDwEx9Ll-HBEoE386dg-SrCwvuF80-8ctEgqBogAIisVAe-jmmGPS9TAFmIqpHaIu9BQwawPFvHuI67jAA8VUlWrWaiIov5y8U5wWllHH17fY60OQXlOi_z3Ja-qTvGm7xQP8VdFkTHQV18KsU8kr_qOH3ne4cM_CFDW-9dfvH7z_Y-wmPfg_iqc3xEoOWbWiaeTjw2DZZLYQXCANV-PCZsHz6sD10uzzD-7yG-FW2CZs6wqaEmqQmyFRCZFTt8gYIuT5lABtltdArVkir0Qwh47Nvkd5OUiY4gur1GJXMAnnEDYFe0GBh8xlMg96JzSw6bOqynl4NvJQXkhiYBDYxMj4TQ1tkoZ9_mJJvHYMApCmIAKtDV4bujTlJ9d2gHnloUe49ghL6w3iOyJdu8XWcDp8YY2dUK7fuyTiCa71vs36HZFTTRKKqPtfAO17T_z23z2iHZPHQZaTb6Rf2FCf7N5hNMdpNwGIz67yL9Z3wqA4jcYJF_jEczPVQqfcOyDwzZYPP52Xf5mzeeDzPLYdccofC9KA8LOLrHwd_QkCAlrC_Md1GTQBEI5tZIIQSnG5K3EE0T73ebQ0l1NUURcJ44dx7cfEJx2YNYSjzzgIkpqfaMPdk4gjZ0yzJewIrD4FAz4cafLXEJsLzq7vC_avk6ZjccSwRdq1N0zjALyegEBTs0wxStNg8DnhwgNxHr15uX_Wni2R0mti3N9lAeSncIZOWGY3XeGSGM94nS-68bJHhX2HCLj4fLRw-DhMJNY0nCHAk6Ou8_BkJX-sZpiTwpFtnjBJGA25FSR9rdWlaqj48WxjH94wC9GLZvqd2QohpiyOJaMDw_1CtuactnlzepgzpcnVdoG5ZEN4kyLY0n0qA6EacssgtFiJzktjiW5I6PRh8f4c5mMdDs3pLJB6D6rHUtR0_tH2M-gnLKdt1VVjAHIxbH8cXi812RzMDm9-eZLmaF2zoObDYKn4gAXyQ7HAv_hqX5AYFmCy-AyUuwH4XxxLDgfHvNlAavOtiiuCp8Cu4NtXRyLmkeEw_Mvi3a1QN6w-JmLGGc10OtISFnBJbLVR7bC4ligm5Z1J4Q0HII1xIC9wUYh6HFf6cfQp6HSUVQQ2Y9_Cxk7-sD24eJ-tRXxTYKNYocO-NhOKbAfPRDWvs3VmUDTlzYHcpz8iipNKAmxb-8arZJBzk-hmfE0yWyb2FlKaWZTJ4AOmYSZ1tiYPzbmTo05ZR9Mn2b6NNOnmT7N9GmmTzN9munTztOnnc6I32eEO-7Hw4Tvx9jvZ6G4O3aSZnB7EJCQxF7k28RNgoBldhglbhbbYRB7mR_DpTRNaJLB4MQhcUYSTsPAObagHYq757y1nSsvuHLCAxR3304dHjNqKO6G4m4o7obibijuhuJuKO6G4m4o7obibijuhuJuKO6G4m4o7obibijuhuL-B1Hco4RA9Rp7se_qUm50RPiQ4v7JZ3uQLcFPc_qIJbkR81ji28kIWhod_On9ePqJHeglrSui2xQEZ-TpOn4NsQLUK4GQUoEysutZ8WJj4e_4Yj4SeaTpJ-CafbK4Lt8e4Iyg4bA-PlyBZsBU8g16vmAvwyeOkOu43YSOUlk1XoUYBm3qoN4NdqFSiJmqDjDfyvQ0LEOxDyYa8dQJMhIlXqob8dGx5cj6n3re2HLtHoO-O8j30EKvsEL8ZVNUsiKaqZIJNCwxMdmbQBVaV_JcYTvgbbsIEYJJeZ8D1phJa-2NO1R4cXIjrbIf6goyWY_XtdAigdvmqv89CasbNTIg1Gtp62gsUpxScGVESntgLcJKPx_zEXafEy9AKDsBQwLltwodtE6AAUMeJI7vB47LPF3IDWe8D336-YezvVmlmRdymmAZqZ14OK99gIp9-kFrhbFN19wPahF16CKUJZBL1WMhEpmLcbKuFJsoathGNKTa8Ub7IY1op4FRTUszjq5Qr3dUtA8PQCII97KnwtAk8R9e5Cl2ARzivjbPpksb3n6-E-pltQ-LTaVCMFNAXICIAdfUr4Jbk1goCcI0cTIoOj29E6OT6MEGnnyEfOAscdo4QpvEDvQWQRJoyHR00qxEetYR8dza-S9e_Klfwbv_OPBL6VAIL6Fczcs5yS8ruBOZP5_B81_xUuyUCk25eNtGWAt69BzfhBEGIJhCApAbnyqoV57KUvqTPI9oxB5jlOSw9ZOnsVAQ_WZ9L-PYPXTGK6yjhTwM47x852QAKLXdI37TGxZ0Lqut3Kx0C39X64XSSL-Tg0YYXMGVLKAvvcTlf421i3i2f4mNjEub_jgAysR8ScYFumxx8UFxGiA_NPdcvFSDA2ey18IWRN6bN4O_i1OatXKMXe-cWUuZKbGv1E4_eiuI9U0eOH5e7Hiu9isJIWlTHkMhAk9bjGzmwd4cNKCvqmpZ8JdF1bHvoEZAlsClhtnnlLSI919C95NeohVdVrfZ5fdfvHj1-guonj4Tu9y_TwWFPqKlwymE0DoEJFbV85J3sK5i92jqxxevv1UWg7pFNqXOaNomevxfUdXy9Vwy1OZYl6iGncqtgOCic4BOuD0yq-dBDY2Uix9kKzZAl0N001s1yrDCDkbRbql9TbjTrK9juK4cRu86DuoRqJGoe7h4nxHJg8I8ZKUuTk3QunpCoUTtqxoxbRDhEJ2kj1Se50E7RR2WDCenA8NkqI6eTA0h_aIRmOnoChJZo2Otpd4ea3a9anYkZIDPkjL_VVZB1-WgILljM6VWmKfOiC41NrzaKOhFhLRGVWRc5ErRZh05WZImJrKkLnNljpMlQtM7KdfHNwi6Yu21sP5e9RC0NAjcoyG2IWMBCiAuWvX-_dXJxteLGSQ6O7R1Ezei1uxCLefixPRAY0wDzwuThAxA44gm07e-z-C37IslwHrUvSyedCgQ3bQoc0RAgGxUtmsMdfXnu_WLQkyuy9EtKES6Bef7ldeVQuIESI8VPjlwIFzJ4r8PFBLCOxxuFQEZj-9GnaumNkOoWJOZ9GN0YwyA1wO8TOX5BfjIGtrcIb5XGVo0dBpDTPqfRm7mN1_OyT0anpoPjye1acqt3WOB47cHOfjHKyvqkCyN4ixwtc2N6EZ7bxY_hSekNxZkQ9rBtB06xEvBBOM09hNdVg1cohFN4qkkIJVHBKQCnQ4Yo1jUjkGPtlqCM80BIrdIaOqlcb5Tbiv9YLcuzqjUAyiYYiDoLqSPibriphJZgZIeQZU-8IsjCw2iqDMfNMpUvKtAoXXTNUYPnWDbtU8vNz8OYH4cwPw4gPlxgDP-OMCf90cAzkQcX1dM4PsPSvTDrwk-fC1sNIB6wwgrhFcQ3Mu_4mEWdDyI6PV94H73usMixKrkyFtG3ytaGt6tx8L7ZbZ6MN_ONJ_2RpBHQg_pqDwL_CC0s9COUuZ4R98I0lTTx98I-gM27fTXmzTFVg935Xw8zKH9t2MN7y7pEG84vPLsA7xhJ4wd28m44Q0b3rDhDRvesOENG96w4Q0b3rDhDRvesOENG96w4Q0b3rDhDRvesOENG96w4Q0b3rDhDRvesOENG97wn4M37AdBHIR-nPmpZ3jD_794wxVtFgyPORegB4xQc3SbubikWcWGUGwIxYZQbAjFhlBsCMWGUGwIxYZQbAjFhlBsCMWGUGwIxY8QikfUqIGbejIN6ygzdeofHRlNeZRN_H1_5CJRlp7fK0R5qfLFyxHtCq1m6IrG_2iALNfoKse009VEU72OUI6_qiWeBY-J2UYHkir2D9I8Ksj9Cgs9Vcb11g95b77LLxv_Ayif8G8YBFEGbY9NaBxnCSdhwBnhItscZCxrkuvjjOXf2ypO514_SlceqLt_CF3Zd2xCPMdOie1wP-N-5JEsdB3CIBWFcRaHSUwzO2M-JgaSeZSz0E_jLISK080-ka4cX3neAbqyl8Yei2xDVzZ0ZUNX_vemK4Oa3SyJvYA74afQlQ9ltEnysmAx_XRaAh1wU7y8oO6GiB-u2Lmp2f_oLnxxqbnEWW5-GH-7WLXr4rPrkvFMVKXEEgdnBMzgV0TEd-hme7xiyfeUfX_T8N3joK6R50VIOcx7xxCrg_IXlY1XRA0iHUPTyvbOK4mgqUi3v74YTbBzWrVzHHyBbRYRJ1-qTMf17ZG7oWY44OzHuN2SbLxL7j7IxJvtMOH2qd8j7pWhfhvqt6F-G-q3oX4b6rehfhvqt6F-G-q3oX4b6rehfhvqt6F-G-q3oX4b6rehfhvqt6F-G-q3oX4b6rehfhvqt6F-G-q3oX4b6rehfhvqt6F-G-r3n476_e7j_wFH4w5B)
