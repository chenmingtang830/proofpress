[//]: # (ob:3eba833f)
# Proofpress Product

[//]: # (ob:f598c9f1)
<!-- impeccable:product-schema 1 -->

[//]: # (ob:599097ed)
## Platform

[//]: # (ob:90cca906)
web

[//]: # (ob:cb0968a8)
## Users

[//]: # (ob:54dc4824)
The primary user is the owner of a knowledge workspace who works through multiple coding agents and devices. Agents submit bounded evidence and candidate conclusions; the owner reviews what may become reusable knowledge; successor agents read only governed context.

[//]: # (ob:f1f48c9c)
## Product Purpose

[//]: # (ob:40636aeb)
Proofpress is the governance layer for agent-produced knowledge. It records evidence, proposals, checks, human decisions, receipts, and the current context that downstream agents are allowed to rely on.

[//]: # (ob:feb10e3b)
## Positioning

[//]: # (ob:3bc86ca8)
Proofpress is not a generic knowledge graph, RAG system, or chat memory. Its distinct mechanism is an explicit admission boundary: agents may propose and automated systems may verify or recommend, but only configured human authority admits knowledge for reuse.

[//]: # (ob:c7b3273d)
## Operating Context

[//]: # (ob:5784f531)
The current product is a Python-first local and single-owner hosted control plane. Agents connect through the Python SDK, HTTP, or MCP. Hosted Workspace V2 is the owner's control surface for reviewing candidates, inspecting evidence and lineage, administering credentials, and asking bounded questions about the governed state.

[//]: # (ob:47fc435f)
## Capabilities and Constraints

[//]: # (ob:966cc484)
- One owner authorizes admission in the current hosted workspace.
- Agent credentials can submit evidence, propose conclusions, and read governed context but cannot approve, reject, supersede, or change policy.
- The hosted assistant is advisory and may not perform admission decisions.
- Verification and model recommendations are inputs to review, never authority.
- Current scope excludes multi-owner governance, general OCR/RAG, Notion ingestion, multi-repository ingestion, and customer VPC deployment.

[//]: # (ob:ee682932)
## Brand Commitments

[//]: # (ob:6006a6d0)
The product name is always one word: **Proofpress**. The operating experience is precise, calm, evidence-forward, and deliberately free of generic AI-product decoration. Product vocabulary includes Evidence, Candidate Conclusion, Review, Approve/Admit, Receipt, Ledger, Lineage, and Governed Context.

[//]: # (ob:3aad66a1)
## Evidence on Hand

[//]: # (ob:d5d61527)
The repository contains the canonical governance kernel, Python SDK, HTTP and MCP transports, single-owner hosted service, owner review workflow, persisted audit data, experiment evidence profile, credential lifecycle, and integration tests. The internal Render deployment is the dogfood environment; design-partner outcomes remain separate evidence.

[//]: # (ob:ee31884d)
## Product Principles

[//]: # (ob:7fdb0a67)
1. Make authority visible: a user can always distinguish evidence, checks, recommendations, and human decisions.
2. Preserve bounded provenance: every reusable conclusion remains connected to evidence and receipts.
3. Project only admitted, current, in-scope knowledge to successor agents.
4. Integrate with customer-owned agents rather than replacing their runtime.
5. Prefer one coherent product surface and contract over parallel interfaces with different semantics.

[//]: # (ob:184e98cb)
## Accessibility & Inclusion

[//]: # (ob:88f6f2cd)
The web workspace must support keyboard operation, visible focus, reduced motion, semantic status text independent of color, responsive layouts, and WCAG AA contrast.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzcyNzM3YmQ0ODQ0N2ZlYTE1YzcxZWU3NiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjE0NWEwY2NlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85NGE3MDE1MzRjOWE1MDgzNGQ5Njk4NDYiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzM1MzRjZTk5MjQ2ZTJlZjZjZjlkZTQ3ZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWmmPG8cR_SsdBkgAhVzNfdBBgM06sI3EluDI9gdHIHr6WE52ODOeY9fMQv89r3pOrmjuIRvwB34QRM50V1fX8epVce8XvGpSzUWzSeVivSjLTeiEbphIL_K8UCtu-yK0lQqDxXKRFHK_kem1qhusrbfc8YO1xy0L6yPb8XgUchkr7kSx53iJ1qEbcTyy_ch3XdfWrmVpyw94rPwwsjxfOcqCXJnWorhV1X6xvqcvzabh1zgh4w0dtcSHRGV48L2qUp3yJFOsUrdpnRY522J9Ue1Zsmdvq6LQZaXqGntKLm74taJLHTyuiv8qXLetSOC2acp6_fr1ddps2-RCFLvXYqvyXZpfNzy_jlzr9cHuSv3Upvi8aWtVbUSR1yqHLZqqVR-Wi63iZETb87klhFp0Tzbq1iyCcdUm9nho2b7riZj7VuR6Mg7iyCPrlkXV0NU2WZoraD54JNu4tF7FseMFsJgOhI6l8kLVXafXbiN4WbcZLuyQnqKoZL1Y_3i_6I-_X8DLRVXTp-61kpsEJv9x0eY3eXGXL97jDkM84Oi33775_Lurdxc7uVg-K05401Rp0jZwzybhdVpTtKhMb3gNszXKyGubbVGRMjdpTiLrfd2oHd7kfEdeG5RaYmtNnl6s8zbLoKLYwjWqu1ySFeIGq12V8Mh1NZbDK4362VxgNA6FhmwFxVJ_HJfS6FFSIKk7PPkjO7q-2ZekDnkSUbH4sJwO1X4ciVjbn3DoX_-wWrF0VyohyPfrstuyqhGGO85stlr9bVKi5BU_0MCPYysOjcyZBsgbXVS7k5fFbadlJ-4YI5J5bAXPPuFOJScUF4kVBxGPDsR-h-ioH9F6WHNCZd-Twosc73my320VK6t0x4EllN0srVmDZ4hBfCk044wCMlPyWrG7orqpgTD4tC3Y3YmLalt7CBLxMEbIy-xtW5VFrR5z1EerT1zeswI34Mb2LzpvFr69Aa4JmnOe47IZ38MW8DwDPuXNqotWJXvLnDKDSmxLuQ_UKuqUQILu8IgJDlaeuL6biCgQD-LqieccXj0vGrgc10TNETPXX1e83C7Zt5dfsA6ylgz2OBXqYeICKw9z9E2pKt5AIXbVPzttgGPrT6VAGHnad-2Xn0npINqqgptZD0pkFc7e7gHc-UqnVd0wHMczxnPJasjN1MpkywljoFYIz_UPcfqKlzxJM_hI1UYY9Kubiqd58xgcPLL1FLAFgQBMeL-KJiv2Jh-goqts6f9IgtylpnaxNDe5NFh0WyByZAcjk5oZqMyBjkoFkRO7zoGOf686xXa7tNmpx010bP0JuwSWFfBAWi8_s0PSLmSomJu4ye74vmZFbrBTrtmrV1O6vXp1wWhTUZ6CEJdzGQT8MKb_cZtKRdAEG38JHR-xxZHlJ0whfRnYvhO--ES6VKVKgh-iqCQEodTBquA5EInSZwawN_igsiUl2QlLKOXaUeTJ4xhfpblIy0zVTy0r8w0nrBFqmVg8CD_hVPuCfc1v1JAizZ4RiSfeA2AxRRdWGWKFGgHo0Kb1lkHAiTSxI0-BiR0Wl0swcOSeyeY9-xP7KhdZa3jkabOc2nfCOlGkA-0I-ek6UNCAPM04xq4F1NZtSR0CQmSfFLySlC0E50W-HKzI9MOgeb8c6P8CMUYnb0SleEfBzZuBz6tNpG3L4UGUCNtOhPClFwYyEAQEqIVGZt-hsL5DYSCp4qYsgI6m4arMScTSh29E0t9Ta5OlYj-TMG93ZkJMI_XCTqgudLPRcIuqQOP6hqtO7LWDTJGW8KnwCHiIWzZ6F0_jn5co4bhJYHMNdHEcV0nfV34Qx4nvKsdCDyso3uuGN6Zx6ry1dhy0IfRk4VhOsLLileW8c-y1ba99_y-WtbbIar3Fif3wyIl4Qlk8Pb3_VXotE39dL7Tl9ZbQIZEWeqEk0BFlhJExa4_60Hx6t9OL1Zb0kiTSWig1iJ01QL3YF_Yz_Rm-8F00NIFOHD2cMWtxBtUf6116adzyPGmDCik5ajxrZ3ppx_uUQYQtpevFPHClM4iYtS6TQifakl6Ui2QKvBB-cYPxblOn0ov6lC6EvmFxVbTXW2BG1hAeo-iQJh1h7ziNBNIAly7YZfesbhOUdZYUbY7oJqztChytBR7LVAIwqHj14FV_NlOpg60aGvCG7fieIaWKHZW9tjZYMar7GQ4yeDi0DzUWceBYnu37GojTe_C8-GWfSO17oeSxzZPRJ7MuaxYkT-mbeqGB5brCjwAByRh5s1bq497-2c0RLHDBvmpYP5oZzbwkrgT9eFYvO0DF_9t2h0IolTAzLjzALpWWDT6RV-ZUsjcYnsEBEk4BX1V8Nzq8giOzrLiDIk0BOTB2kZ8yb6gj6cWhlSTWaN6pe5uZ97GerBeImhLGQRw6iTUKnLVpR037vOZLmNhTO3AsMvFAHQQ9pGFRWu8MB82Z-rlEJUKwT8zchD3SbT1YjIK4c0mXAiArxY5KZn9kt-KWRpF7Op0cugMplkuWtE0XznCKTq_bCps6V06Mh07GKdOdtJGBZD_hlDhWvm0ByezAH3Fo6isnpzyxTxwwXSZAD6Cu0vGISVPrOMOkl7aCQ6dDUVoVGSsznqsRefA0V6IZQYviuhPK_v35P5fsy3fv3hoPf331tm8RjFAYi84_ZEkmugmMJtBCuoBul3TEAar1vGJpnIHwaIh5wllQKjV5aPxe34yY-FOraop1nIpHzSz1KSzADk45T9tBGAS2DtFvjtgy9cGT857fzA7h4UeRjC1fCS7HSjf1t_0Jn9KkkoUv_pOvOs_NjWUoe19CHmLaQdXorGog_yHam8SBHJP2JfbeKoI8GtQvifiituK8IddB8VjHKI1GFBa9qhz3gDfyLj4laDG1XXQspSxJhyjiDbNLjyBrhHW_MAjDq7uNhVTZlOO8jwKgapqXLWJ4DLsly8GoqynVjcCr3pi1AF8H_sAaEkY35blPkamGLDvIQx69ufr2NVBuyb4pms41110ELvuts7Zy9s6UbHQLqMAV-_7tFW5XZsWeWvaLIw3UwHLAQrxY2txKRqI0Gz1MAfrEUUIvNors2BGAFkvzQexsunDAeF42LeihDqgOt5nsxmYsgkdhS-AR6sMQkyv4_Q5907LnQFma0H6qh7pSirjVUG8uv1oNGkmq1sbpFyOfuAXSJW3Gjel7f_5jjPyrkTFdjbGPitWHyGUX3a8vqQrQY1PWl-xfVAoq_D8iE5T8YkiTq0dJkeeRZWOduHIqstPAZHLh0yYgvVQhAk-HtkjAuQaps6HIzIMvnXIcQL25NKCeAfMA2-gCARrHqgmIMVHY5QEHNUClwXSWlOUEBIQIrQQuwR182YcJxe1UDeANnWYULCOioTpoJfYi670A9FXXXQww-j2y7sKPHuM-GXyIElHNMm3ghrK41kUBQp3fplWR06vPsKxOr_MV_NcYRt82RJeJCu9gNNyMPIvgGTQ84XNHhcondwQJn9J2HA0dIcKPTHoGLhzbGoxAOdwd4WA2_Onlfsosp0-Vge0-QNfO7A8oMMDUoRRU5Hs1FmaTTSaq1ozQdz81HlPp6Y078o2OCh8wgoFf4xjXZDrVno7LGcKGPcuhMBKpWHV4PrE4CHzY3kCWBz7ahw-gLG22IzqbgJZjI8QRMBVxeFIWJEkQruFZiuhuEZY7qr6-MYCmsMnpftgy52R1W2k-9G3EtzhdgUoSRU6WoY6ZoKVFdaeNTLXuhNQwEc4R9Yk6kdiRxz3f1lKPIDObvU0B98wZ2lAvhBMGdhTGXI-N3WysNkObl47HClifwq3ry3ZF93q4uiFyLXKXGEmK8Cops2EblAZRZEVFWwFLeZ3emnYPydsH6w9X6EguL3uz1x8j9fsPdNEjP8Ur4NP4Q7yJhjU6dvXz4r35cd9oevztgx_xP3prOOv42qTTGtVtC-P8pr_044Cc_h4B74wCx37sN9q89Lf-5_64BQoHTqfkkeGoyHi6-0XpH-_vB6HfQG3JvuyK0Q9jIH7vgIFOs5E_12PbM6QmJd0Dlj1k79CHXnSKDRe7X9xtaXJ6Bb5BDSdthUTDV44pMEgf6-4R-c8YCp_4e5XOFvNp73zSOZ8A3__Wbnz6JHuc5I7S1vaH46Pax-bWv8pwWkuuY8_xuVSx7WktIiRX6MdQ2wotx3V06LtcOJy7sesGTigCehtZXuR7XsR_-UrHxtPO2neOjKfHP1g6j6fP4-nzePo8nj6Pp8_j6d_BeDpRKnBiGiBx8fsfTx9lY6fpYGdbQigyyZGxtZluPTK5NluPDK_p-Xl-fZ5fn-fX5_n1eX59nl-f59fn-fV5fn2eX790fv3-w_8BM2Pc1w)
