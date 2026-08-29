[//]: # (ob:6ecae0a6)
# Agents Are Creating a New Knowledge Layer—and We Need to Govern It

[//]: # (ob:c584c789)
Most enterprise AI infrastructure is built around a familiar problem: how do
we give agents better access to what the organization already knows?

[//]: # (ob:e42ad814)
We add retrieval. Memory. Ontologies. Knowledge graphs. Better context.

[//]: # (ob:ab788dd1)
All of that matters. But it addresses only one side of the system.

[//]: # (ob:afde7313)
Agents do not just consume enterprise knowledge. They create a new knowledge
layer.

[//]: # (ob:789cd254)
They research, compare sources, synthesize findings, make decisions, and pass
conclusions to the next agent or human. Once that work is reused, the agent's
output has become part of the organization's operating knowledge.

[//]: # (ob:ab5d3fb8)
That creates a different question:

[//]: # (ob:09cb2dcb)
**What may the next agent or human rely on, why, and under whose authority?**

[//]: # (ob:758aecf7)
## Two kinds of knowledge

[//]: # (ob:503d943e)
Enterprise knowledge is what agents reason from: documents, databases,
policies, domain ontology, and memory.

[//]: # (ob:3004cedf)
Agent-produced knowledge is what their work produces: conclusions, claims,
findings, analyses, and decisions.

[//]: # (ob:1fa0680f)
Existing knowledge infrastructure organizes the first. Proofpress governs the
second.

[//]: # (ob:6eb4e760)
This distinction matters because a conclusion is not safe to reuse merely
because it is retrievable. A future agent also needs to know:

[//]: # (ob:308f1937)
- What evidence supports it?
- Which version of the source was used?
- What scope and assumptions apply?
- Was it verified?
- Who was authorized to admit it?
- Does it depend on another conclusion that has since changed?
- Has it been contradicted, expired, or superseded?

[//]: # (ob:cd2caa9f)
A memory system can retrieve a conclusion. An observability system can show how
an agent arrived there. A knowledge graph can represent relationships. None of
those facts alone decides whether this conclusion is currently eligible for a
specific actor to rely on.

[//]: # (ob:606edc32)
## Why this becomes urgent

[//]: # (ob:d2e23f0d)
Enterprise knowledge often grows relatively steadily. Agent-produced work can
grow much faster as adoption, autonomy, branching research, and agent-to-agent
handoffs increase.

[//]: # (ob:611cd9f4)
That is not a claim that every organization follows a mathematically
exponential curve. It is a practical systems observation: once agents generate
more conclusions than people can review informally, verification and authority
stop being optional workflow polish. They become infrastructure.

[//]: # (ob:b485602c)
The risk is not only a wrong answer. It is a conclusion that was once reasonable
but has lost its evidence, scope, review state, or authority as it travels.

[//]: # (ob:dbcaa053)
Output becomes input. Then input becomes output again. Small ambiguities become
organizational memory.

[//]: # (ob:cd41345b)
## The product object: a Governed Claim Graph

[//]: # (ob:bad998bd)
Proofpress turns selected agent work into a governed claim graph.

[//]: # (ob:f610d9e0)
The core objects are conclusions, claims, evidence, provenance, verification,
authority, scope, dependencies, and supersession. A conclusion may depend on
several claims. A claim is supported by evidence. Authority scopes who may rely
on the result. A later conclusion can supersede an earlier one without erasing
its history.

[//]: # (ob:39827abc)
Agent work crosses three separate gates:

[//]: # (ob:290dd04f)
1. Integrity checks establish that the evidence and artifacts are present and
   bound correctly.
2. Policy evaluation recommends, blocks, or escalates.
3. Configured authority admits or rejects the conclusion for a defined scope.

[//]: # (ob:07045b01)
Evaluation can recommend. It cannot authorize reuse.

[//]: # (ob:edc6df16)
Admission does not declare universal truth. It creates an inspectable,
scope-bound answer to whether a future agent or human may rely on a conclusion
now.

[//]: # (ob:f17d1d48)
## Proof, not product definition

[//]: # (ob:5dcf7272)
We tested this mechanism in a frozen panel of 7 models, 3 Harvey LAB-derived
legal task families, and 126 valid paired runs.

[//]: # (ob:5f1dd627)
Within that bounded panel, Proofpress-governed handoffs raised rubric completion
from 89.3% to 93.4% and reduced observed unsafe propagation from 8 to 0 across
63 controlled stress pairs.

[//]: # (ob:ca99c380)
Those results are deliberately narrow. They are not an official Harvey
leaderboard score, a population-level causal claim, or evidence that the models
became more legally intelligent. They are evidence that governing what crosses
the handoff boundary can change downstream behavior under controlled
conditions.

[//]: # (ob:659b328c)
The study supports the thesis. It does not define the category.

[//]: # (ob:923c89fb)
## What Proofpress is building

[//]: # (ob:06f40f8d)
Today, Proofpress has a local ledger and CLI, a local review and context UI,
agent adapters, artifact provenance, and portable Markdown and static-HTML
carriers. Public API/SDK and MCP surfaces are planned, not shipped.

[//]: # (ob:8db2910a)
The longer-term idea is simple:

[//]: # (ob:689b9f66)
**Existing knowledge infrastructure organizes what agents reason from.
Proofpress governs what their reasoning produces.**

[//]: # (ob:d046170c)
If your agents are already producing research, decisions, or analyses that
other agents and humans reuse, I would like to hear where the handoff breaks.

[//]: # (ob:1baf66d2)
Read the full thesis and technical repository:
https://github.com/chenmingtang830/proofpress

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2UxNjY3ZGZmMjdhNDI3NDc2YTg2ZjU1NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjNkNzQ4ZTAwIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85MDczMTMxNjhjZWZlODRmNmFkNWI2MDYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2M4NTQ2NGEzYzM4NzEwZjI5OTc5YjJiNSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW22P28iR_isNBUEAn2bM9xd9WUycvawROzEuvtsPkTFo9ovEDEUqJGWtYhjIj7hfeL_knuomKWozQ9sjHfbuoA_r1VDs7urqqqeeqmp9mvG6zTUX7X0uZ4vZdnuv3CiKpdZezAMvDuKIJ5EOw2g2n2WVPNzLfKWaFu82a-6F0UKmiSMdjBFRwn2uVCC4zmKRxNpXfhSkgqvQ99PUC1NXizQItE7TzPEiV6VJxjGvzBtRfVT1Ybb4RH-09y1fYYWCt7TUHB8yVeDBf6g61znPCsVq9TFv8qpka7xf1QeWHdi7uqr0tlZNgzFbLh74StGmTh7X1V8VtruracJ1226bxcuXq7xd77JbUW1eirUqN3m5anm5Snzn5cnoWv1tl-Pz_a5R9b2oykaV0EVb79Tn-WytOCnRl3GQKMeZ2Sf36qN5CcpV96kT-67vRolQWiWBjrgMs8gh7W6ruqWt3Rd5qSB5fyLFvUjCIAq4L_wkdh3tpWmcZl4W2u100t0Lvm12BTbskZyiqmUzW_zl06xb_tMMp1zVDX2yXyt5n0Hlf5ntyoey2pezD9hDbw9Ymj6KQjUvIUzZNje8VjeiVryFdm74Tan2NzSuUHKlbgp-UPUNRH9QMi9vN3I2_ybb4m1b59muxZHeZ7zJG7IwVeh73kDVrTLz7dp1VdMGHvKSpmwOTas2-KbkGzrpfiNzDG3IOmaLclcU2JZY4ziVVUhWVOIBb0cKpulwWh0n2aqfaNN3Zq_srlbsVbdXxtkf1Z79od8re4O9YlAnBJfSSLclk1R7PPkV-9pZ6lv2o8JzJVlbsd_DCTBRe9jSZsh2MG72eX4UWYRJIOIkvbjIb6umZZhG1ds6bxS7e83yUte8gWmLdoep84Zlu7xoGa-rXSmxguabvMh5fRR5y2t-Iq8KPC4TN7i4vNAaHgIFYDXqIy9u2Vu1AQzcsj-VbVVUq1w1t6P5VjXfrvHkt6ptJ-TlWZwkUroXl_euKFilWbvmLdvA1lVNwuxalre0EXJg1bCqLA74R7Eml8q-j89T8mqpCFAuL6-dQ1asrFr21x2sg9But1FjKxnc_5a9X6sDM-igJuSF6QrphZe3B7M8tKh4LdZzyLrB2tBdtauFauasOZTQZZP_XTGNObAEHm74g2JSTdpDKH2dJf8D8sIQrLoaDJa51qrGtOxvO4Q8INdiQionFZknRXZxqV68-NEa6MFYXomZmQF_VtVsvdvwEjo2Jjpn-_VhzjiAAGCgarafOvUw4Uro-ETe9_uKkSAN2flgSJOw-iv25KAJzAwdX6aBr85c_ftHzJ5AcU8asxESyuENKImuq80CviPgLng8ZxO68R0nEErqM6Uzp38DNiB3mO0RCXGeOU6pqh9Y91azIJcWxW5COldzJ0qcc6X7_ieQNDLIkVyn0aWqV7yEdzbG8HReN-2t5XMT0kUqC1QcOWdK9x4UkkkjoSDX6wGaZSAIIHpwI6sowzfxLkFiw7VCzJ482US7qX-u1d8w45P4U6pSANJ2W2KKDSLHd8uSvs3FmoE9G-n6mGFwb-yUBfZ3SiWkJzhPzzY8tjGBl1kuxoTBCBOVTxV3y-4gXgYy95Fn4A3tYcotQImVFL53It2Pa8Kl3BxMtYGt7Goy-y9gxtOjJkBDesrztSPPXf9R1Kh0q0pQkmpPkIEsJ_9IqAr9QZACHMZ685R6XFfIVAfnimfCUGfROKyC5xvLURSlY71XcuMVuioKkpiTf6wN7X5KvCxIwsjxxPniIdHLm4deRMOPONvXFQW3stkTgX5tdnDio7SFCfFkBst3Qv9c8f60a7egcP2AvMRfhgmV9vPwTWVf5CuO1Ij9ecOLYkI8IQPXD8LT8E6qsMANNWSUwi6wZ8oY6hKA_8oc3e9r_qUA-pXTbNfT_pFxmSJ7lxeX8ZjDMwSGsmFIAjERhlsiYiJYDo6PmVf9zNZwVxM61ZHryFQ5F5eX5kAyrboJYIi1Gpkigr8RDv_vEXxOayIn5-VU8EgTJMmZuLi8d0ctiroyWUe7rhVChiIhWqRKxEmn6KeXOlI6gb64bC6cGfOtagoOYq3EQ8PAhnmG4LW2uETBbQiFxD6HesXTkc6JHXiT415c3u-ReO4sONqwB28H45MGk_DEoKqpWVDeUStwidupZFmKSGo3uvyZy01uyiHgpMoiqVQwS1jqrsyJOvCCgYq1ayt5n5YQjE35lBtLVwanyZHx37lZoxdbKqRcOanpC-D0pbFTJF8iv_Bi7zKy_AhqB8OjqgxFhI2i8lHebKAPqnvU1d8B8VteKpPUx2xTSVXAxX32A59QWKhdKSMvvpCQOYSzsY5lVJKBuEam-agQejNgJHYgK63BOHg-VVIQPE2FnziXEfL9umrI9Jtd0WEjNJVnipAGsbzkNVhQVz2gb43LEI3VuZjiP2Ga-V4iLiUk4K_dycORXBPOmIJBY1xi5DeY0HwFBwdUTSUAqeeLJNXZz2gGjmsU5LqymjHoL_HYqZETvuFEOnB0Ii8hx_tK8sPYwGBXRL6wFDDE0Nva4PKrN6_nw_Nu-NOqSmTmpa7DLyIizqYAQVT1Dbg3fFYqTmObfLMt1FRgi5I0S3UUXUKKFy--Jek9LSJMUVcniNzYEZcQ8bVmB-SJ_brkfrwA9sMPrP-Q8MeaGkJG3lGaaqrm62YcOpTeJUT8N0hjKwK7ougc0phXC0guc2tb26rJqQW0WJYn_Zyfy_hh3vdCZl26fG9DHa1pvukbFeo-yhyVhRGP08hRnuZB4Ce-I4jzAAbMnF27hnXtGktYtlVucgaqPtJK1H7o_6Luwwfq8xS5OIxmGPd-RpOYrtIz20INUsx7INXKJJ9d96nJ3IXLwzCQ0g-SREVKOQmPlYutJbEMYt-VsXAdN0uCTCah0iHiQKBiESlHJQFeINcAIWtNF8ke18JPPkPR1K_xHC-6cZIbL33vxgvPWzjhvzjOwnTCOo2bqo3PteJkNMenn36xxpMxW9sYApStKbfxdKQ5lzoyjQAzx6hX1Fn0OU2eukRQuX0ctTsh_DjxuILUcah6IUbdn06Ic9o25OSwq82Cras9Ityy3IP851S2sRvLFJXBGBfCZGPVUEg8rQv0mEFH0nz3CDD0alUpVzxSgWOavmZHo_5QDxRnNHYgbIc4t0-LEfiun_pCRpHJsI0Yo7ZPX00_o19jCmETEqiEu4CUCOQgHiQ4NnJO6_nP6sDglOEkxy-XpfGSCZnApoR2A086WvcyjZo1x2Tk2V2WIXgQfG950yzLUZpM5vVEy4FOXih7FDb7b2wuJedmiHn7N5iuq7IQIbGFFyxTt_2xjG32Nzi6LXHQk_A8oZ4o0YFOQzcKjPd1RjP0hgb1PKOp05tl6AW-dj3PU4NZjvo83QrnNGgME-_S0fbw3YsXTwujM2wuiFLhCH-whmMTp0fAb-vHdHO7bqi5G7gpNyzGzD1q0XRzn9NtkRwBk8M_58vSBNucbFNWG450qbIo0qnG1q4nDj5JXK1DL43SYPCLUctm7KvP7L6cVomW5dFxeMmLA23DiDp40IS0fuCHPHSpPhP10o5aOL1uz-jGWPZmk0rz7bJs4GulnMKW0BdaeA530uAYT4fWzeA8z-_CWDzAaZLxL8t-RN5arLChBLHult2BSZotWq_hRQN8RWQ2AET6mHBRgGOMOKGUaxhjZwtDk6fbx1n9GkAXAVv3IqZpBIDKFroaYP-2NWDJQf8O9iVOE9N0uc6HgZWZaSg9Gd7B5Yb0YYX4HeWzOaWzW4W5KYpDnWsbQMdVdIOmTU4bsVdo7BI_2GUzpUoTcmu4ORVp50z9tM1r-gBAwtaxTQWW-N0j5blOq6lwtQNeEMbZAK2j3lTvYWe0mUZDGqI6-G9Z4o_OBOoanMdkGbUxkIdTbtEtRYZPr9t-DQ5hnW9BCf5I0b_SS8Q9glcinVB8QU_JYaXJ7ZTRrCklnZqw2NUUHwDYqshXOWUTGnrjcKotRutcMHNpy5q4wfUJP_O8OExVGHMRHv3s2Ec7ovY3dcT6CKhTmUVJHKV6OKZRk2wKtr-y3TXApy1O83JZ0hi22cFfNNCJuCiUKyvjBXOy76qsNoDyrOalWJ-mq8ZnzMRtdWM-ID3sa2AwaIoeUyE_DJFXBTyJhRpY2qjtNg75z2yg4SkSWAIsOA0spmxz5LOwiY_q2NXa1rAAk-haM2564zZ8AgYhBr6Of01dbVluqtMmBIlUsq2qtoXq7JkSbIL9qqZuFHRoIUR0nJ6U11MFWGNbbWEspGCrfIhDp6SxH0Yhtll3_LMjXqfxZMpmE61SL3JEnA651qh7OCqCP7cPaKDQqMnyBYoDCBEdUSwogcqhvGN3xkDuvFcRZbvKoNmgD2bBD6AHO54KxwkPeRIo4Yfh0WeOvcduc-d0ERnfZPlql7egON174MEjo8NBfZHjhFEgid-A1URHBB56kCO2d2bzsM9_vJT04rpcD5416ieOq7nPbASSCFNG5_ipCyiLHT4E8lGDcGR0z-3s0eexQ4HXDeYzWJgNvhiY9xyvC5hNF8jGpkyUf4jWRLowPaGFEcG8a7ZOdU5LOKCN7DCIhjcG8zXLU1yqzKyWMxlv6Sv1NB9dvj6hAyZ-9hGdivQA2iLHOxTs9jlmh3FCKLCF1bIkn-quZk-chI4TN3Vj4UThkAyMWp9jev28nmW3jqNcmFfCPSmHasqojdmtc07_0ZpHzxLwzbJkzPZlyIpqWBBC3bL0QKRNAZCpY_dw6BzCDmw9yiCOaoD7tDOM82_ZqwrJwQp4KsdYRLSuobdrZc3U9CaOx2YIRde3kPbsb59mY44bRVIGTggAGNLQY_-0D_OXaXz2-UGUZlkYKhf_DIWhYy-0N4IzmpjEpkwRFX5oNHBjD8aGDlvasiSNn-YHQ1bdO4qhyiP1LrHX_WQIkDzw3CCJ_CGtH_VNj9j6jN5nt4RI3CyIXC9V7pCsj9qhx7ras1uaICQH9ubutzdSGa68LAu1Im1zhGRbTuwRzPUiBuPIqcRDeQCrd5MZa-YGKXe1K7mbDMIf26S98Ge0Oo0MWQ0qTeWqQrXm1KhowJL01v81nX7q3wa_NvJDZMNBLclSVDwxOSbOZIvAa3mcGUvjHNBzAqRlGfk2DwLFIy9rTdwiFUxtPuWJpxyheZR6Q-A9tl-HOPT8FioRSnt-dGYc55dVvDYwUCvqz22r7c4mNDcFQgoCCjLnPq5YEOrRbsA_axo2zd7Qn1jUGASkQUBWBXIZOM9IpNM57DkRmdzbgpmBdEqhVH909pQ5GDThi8084ff7kjTLN6A6a_4xh3S2tnVUvSkqSuM0U5rXbhh7vhdEMh40P-opjxjAc_vCk2HPjZQnhI4AeQMDGnWLx5naN_Z8e4YTJZknwLMcZ4h3ozZwv78zmrnmeVdtZ__-mgiOTacl31LZZj5ExhNSZIq_fefsLa8f6FAt92kpH7r54f3bNzhEyspNzf3dDtFXsLt3r1_--Xd_MG--ffUOB1JjbtVF3QIhh2oOpiSExHyr5GRNDyP9MOOCD4A5akCPDv_b2si9V3tJLOOMe6E82taxszxUcp_fHx7KnuAFj1TlRhVH-y4t0pcdb6fqvo503TDTOoj5kI2NOs6d6Of0jYeipoGCZVd06mfC4Zpw2xX45-w1WN-ukKzIH0ydD6ZOlWxVW1cb0AKrP0z5e5ip0MURB0E6lHFHfepuY2d1m7_i14On3ejPJN8jP85TgK_hp3kCWPvT7IP5oZ-JTD9__rOf8o2em6bD8Td-iGf_937gZ6zhF_59H8Kdqa0-ArjQs03Anlr3n6fobg-8M0UTW3Zkb4xSX5esOxDW5m0Bxmzm7yX_NNuv6dbAv-bwIKLVJyMLvivF-p8m-IYbDxO_TLUyj68yjNv44-sNn365g_j6CxzDBYZhwoX7-fEbCl-6rnGROxlScOFARCGdOPVTN0wwSRq4IsykyhIn8qWbpY4QSkRO7IokCiXnMgNvhG-53tNbeuxWRrjw3UduZQw_Wv7feivD1YkIwjDVvhtc5FbGf_3jPwnbH7uacb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Zcb2Z8f_oZsaHz_8NHxyuEA)
