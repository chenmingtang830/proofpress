[//]: # (ob:36c14089)
# PageIndex retrieval adapter — implementation contract

[//]: # (ob:19668a0b)
## Status and scope

[//]: # (ob:a856a7d9)
This is a design and implementation plan for the adapter that follows the
retrieval-evidence receipt contract. It is deliberately not an assertion that
PageIndex is already installed, evaluated, or preferred in production.

[//]: # (ob:237cdc42)
The adapter's only responsibility is candidate discovery and locator
production. Proofpress remains responsible for immutable evidence receipts,
deterministic eligibility checks, policy recommendation, and human admission.

[//]: # (ob:42b1cca2)
## Inputs

[//]: # (ob:5f28e5e2)
The adapter accepts a content-addressed document source, a task query, and an
adapter configuration. The source digest is the identity boundary: a tree,
page map, or preview derived from one digest must never be reused for another.

[//]: # (ob:0c9453f4)
The configuration must record the PageIndex package/model version, tree build
settings, query mode, maximum selected sections, and maximum selected pages.
Its canonical digest becomes `retrieval.config_digest` in the receipt.

[//]: # (ob:60425159)
## Runtime sequence

[//]: # (ob:1571ad28)
1. Verify the source bytes against `source.content_digest`.
2. Build or load a section tree keyed by that digest; cache entries are invalid
   on a digest mismatch.
3. Search the tree with the task query and return ranked section candidates.
4. Resolve each chosen section to one or more source pages and extract the
   exact evidence quote from the selected page text.
5. Emit one `proofpress/retrieval-evidence/v1` receipt per selected quote:
   - `section_span` when the section identity and section digest are available;
   - `page_span` when only page-level provenance is available;
   - `text_span` for an exact offset in canonical extracted text.
6. Send the receipt through `proofpress evidence import`; no candidate becomes
   reusable knowledge until the existing evaluation and human-admission path
   succeeds.

[//]: # (ob:905225dc)
## Receipt mapping

[//]: # (ob:ee5211eb)
| PageIndex output | Proofpress receipt field | Deterministic check |
| --- | --- | --- |
| source bytes | `source.content_digest` | SHA-256 equals imported source identity |
| section node ID | `locator.section_id` | non-empty typed locator |
| canonical section serialization | `locator.section_digest` | SHA-256 receipt value |
| resolved page range | `locator.page_start` / `page_end` | positive, ordered page span |
| page text or rendered-page representation | `locator.page_digest` or `text_digest` | SHA-256 receipt value |
| PageIndex query and settings | `retrieval.query` / `config_digest` | typed immutable provenance |
| adapter release | `retrieval.adapter` / `version` | typed immutable provenance |

[//]: # (ob:8634da1d)
## Explicit non-goals

[//]: # (ob:db8423cc)
- Do not make PageIndex a new admission authority.
- Do not treat a tree match, embedding score, or model confidence as evidence
  integrity or as counsel approval.
- Do not silently fall back from a section locator to an unlabelled quote.
- Do not introduce a vector database as part of this adapter PR.

[//]: # (ob:4ed61524)
## Acceptance tests for the implementation PR

[//]: # (ob:ad7f8157)
- Given the same source digest and configuration, repeated indexing emits the
  same section identifiers and receipt digests.
- A changed source byte digest invalidates the cached tree and cannot reuse its
  old locators.
- A selected section produces a receipt that the #39 contract imports and that
  passes the `retrieval_receipts` deterministic check.
- A missing page mapping, malformed locator, or quote that cannot be bound to
  the adapter's extracted representation fails closed.
- Existing lexical and OTLP evidence paths continue to work unchanged.

[//]: # (ob:d1c0a627)
## Follow-on evaluation boundary

[//]: # (ob:b0dd596c)
The adapter will be compared with the current lexical-chunk baseline only in
the separate retrieval-adapter evaluation PR. This document intentionally
makes no quality or cost claim for PageIndex.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzk2ZmI4ODgyNDBkYWQ5NjNiYzAzZGIwMiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImRhZDgxZTZjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xZmZkZWIyZWUxY2U0NTU2MGEzZWYyMzAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzE3ZDE3MjA1Yzk3ZjY3Njc3ZWQxYTE2NiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNq9Wdtu3MgR_ZXG7EMeMjPiZXgZ7ZMCKxsBi0SwjUWAlTFqdjc1jHiZZZOSJ7aBfES-MF-SU928jaSMZGkRwDAkslldfarq1KnWlxmvmyzlotlkcnY62-026zBN4jj2Vo7kch36iXB8mTjebD5LKrnfyOxG6QZr9ZZ7QXjKZeAKn_txEMeuTEWogjSQsZK-kE648tfe2vNdj_ueiKLEdXkceInn8yR2Iy6jCHZlpkV1p-r97PQL_dJsGn6DHXLe0FZz_JCoHA9-UXWWZjzJFavVXaazqmRbrK_qPUv27LKuqnRXK63xzY6LW36j6FAHj-vqHwrHbWsyuG2anT49ObnJmm2bLEVVnIitKousvGl4eRP7zsnB17X6rc3w86bVqt6IqtSqBBZN3apv89lWcQIRuMWuCsXMPtmoO7MI4KqNm6ZSJZ5SrlCrIAgd7qvU8x3yrKobOtomz0oFz_uI5Bs3km7kOYFYR2kYhVGkpMvdMLTH6bzbCL7TbY4De-SnqGqpZ6e_fpl123-ZIcpVrekn-1rJTQLIf52JSqrPs084QZ8NdIpK6JNaNXWm7ni-2OW81CeXZz-dX_z13fnfN-_PP76_OP_l7OfN2buzy4_n75eFnM2_K514A-NJ2yCKm4TrTFNSqTzdcA10G2Xstc22qsnn26wkk3qvG1XgTckLCq71fY4PNaXD7LRs8xwnEVvET1kEkrwSt1jrh8JdOfEayxG6Rn2mc14C6osSRthwWMYl3zWqZv_5179ZVuxyVQBCjs86J7iUxrsdZaG6x5Mf2Mvt0IEZOVAT0vNZs9_RSShXkHezb_PRY3cdhjF3kgOPP8BEqxkvJUPd4Ntjfv3Anlh-ZEeUZ8gjuX71jh9RkAz_OJNKZzel-erB4SmZWFrVrNmqAaRmy0fXdrzmB355fiSkWHlv8GvY6g-aVWW-R6D0DiWcJVmeNXtyWsBUJkE7bOAksn7Er5WXuELwQ78uyl3b6GfiMiw6Eo0g9WIVqO-1Pjkr40KoXUPxMBbKZoH1RBhKMtR4S1FhumproeZY1Bw5qyPWq8BPV6_wBuvT7KatbfyLVjfMkpBJgbF2OtY-KVDWObtTR7wJnZUXuMFhpr5vyyYrFNMgalWK52rjieXHqjGIXC69-NU7uktmWtjenNqCjsaFLsf4Dc9KoHJtny67YHXt9np5VY6-5Wh5B46tncDzAikOHVNCZbuGFXy3o5M8g8Sj1UeAUCrwXFclr93v6yTiVdsggdjXSfem1DCm0kzlEq_eKWQymjLOnY2emW554Fcc-ivJXXng1_nnXZ6JrGFlVS5uKp4_V5hPfnAEDZnEK88X4g27Lti7CisJvNtpOXBWqnuUcpGZ7sZsOwRZIR-Gb44kxkrJ0A28w4o9M4zAkauM9JUemPgBSz8D00vNXL5_puPIKI1RWr-7jwv2UwbtY2uNF0PB2ZIyXeOAlubIu50C-aNfHcFUusLhoXfo75-rPK_uF_CIGn9rnUuqtpQcsvY4kM99ewS7xJEyWIfi9_Fl2jbuszxnCRF3AeYFJPeQyAZK0dY19Yxcfc4ElKHYtuUte0jUn-a98Jyhi1LybkRtwJ11b3qJeFQUI7-NzU4bs04bM6h0cbursrIxUr82O5H0638j5feJRDWqcD-xMBXaEyNGwr9Sg-sqbTYpQqPqXZ11Ul8n7mkSJCqSqe-GkXL80PdFKjx_7borDEAhenuYrEI8iGLl-67rRKmfRjwJE-VL7pvRSCPPjWS30Tp1I2hbejLzHC9cOPHCCz96zqnvn7r-Hx3n1CHUOsSns8i3ydMv_1-db5LVKvEt11tKPR4F0g3XSeKkWGBsTMR5l8e_s6bu9k6lv0rXaRL6ker3nsjsfu-X6ubOqpIQR56fSrEerE6kdGf1LdoY3dDUtaYXV-UYMVSvJOExdM0ehiW7aGg3KKksUeA4Bc1LDQMb2BGL9iPTV-WINLmXo1IlBDEECc9zJec9k9CPcA2UkaqaWCGDw3UlW0G2lk-otQ6fcOVEjvRTxzfyyeAzkfQDPq_X6AxZxjHgXpUThw5FRUESa7QIOiGcs6JoLbk8RFLPrwDJKD0EA5I3vSuGPfScWYoxcrZAGGXXS8ilbVsQ1n37PoIPOGXtr2PheGLV4zMZLcasPDY1dLbiyPXdIODSlby3NRkkHmP93TMC17cMarfe22Py8qrsTR101CX7uH3YdjNt-ziQbgjGvjGdkuFaKWC-I4aHjOxzjdoTsrhGN5csrasCqTHYM7NEiY5SU7uqVUtOU1w5Un2r6iOgx1GSBGuVhGnk90BNZpwJUK8dXwzhzs25WNJmubwqtWoaBAyJYxBktHSO037OirbAFJErQQpEK5PB2iL86DVBpCECLxpTEFVJrbiHJKFUxExxPZDE0h6gnyaobMnxLs-PQCSQg-hOa87DdQ_RZPAa8_Jlk1QPvOtKFfroqX4ycPA4XHVW3zQteUv2JwKcUiivOJK0h9RG41btAWOyt9Rqv_sRUKKqGSwBNuxSI09LwJchbowxEuBD2mW64I3YYit_yT4oXgsrj4z1QSyNpWLiiIC0dclqXt6OMR4ZjSK6WmIW01V-Bz_gDWim0hCxg_OVSX6cqqjqARWTDmYHQEfcb5sEfFaf6beB2X5rIahsDRlQp_nECHd4ECzZeYHJhfa5Hi8YTx63nJM793poOztU4GDP7HNqPFggStb5jd7x8prdb3tR3p1p4ALTa7uHvUrHIfkdz3Ji6B97g-Tu1JppFfRwkYMJcupJkJhmfKB-9uh7Omn3vaWKDqcqTVGfVB5jUXWI4lAdPiHFu5TTCsLPddXebKd4jaCjw0NXXv-I5jvpXl2VGpeItkwLui2rezRcBIPqKTd7QGdrooypnB-6y2IcDne82RprugWfK6mXT0wxXQW68XrterHnJKHbV-DkFmFS1y-5F-iMrgLlJxDJvh8PfDq5KuiMvmX4F7brsq9X5Ve2WCzYwf_08IAmvv4vgsCbD385W3hByMBXGM67GFFRWgNDTlqrXVKWIGt28Y4Md3Jj2ed2JskqTfuq2OE7gmkQJdbKmFO9PYiwDPTyTxvUJ6w-9reHh3JBWbu15Yuuimu6-J7assXSQLJfs5OudpC_ZHRX6axBW6VOiwbbm6DKsKYHXiDGwVxlFi3sPoriNejWhxv2nuM7W24vOsqYGiNp9h2Tthg7mnlvDvSgt33toB913YQNzCa9VqnBVlyrQ7vdS2O5a-DP2XzqSqorCWfliCiWvhT-MBdMbqnGOnvppVNndx0I31Uy9MOV6O1O7qE6u2-6VmpoXO9EGTO9DmNAkShJvtBIVJu0YVbrmCBYuuMj9REdYSJWN2ScFuOdgOBDn2AgFGAIxCd76ixHQoHLU07XD1BTtleNzbsvKPRB5Ghbmj8N5n3HmdrCvmYQgENQYvS3Lwbe5QlFHG5A6RDfg2GpQ3QZcfn-CGdKiYE-VEKsHTlo9PGCbYzlW2_G-v1WXrrigYp9Nc6U42XZEOPX33JRMpjGgnave8lgjRy0ZlBxrTsBY0vWWtcG7zNm_9gmp-Q7yH2rn0jc2NsjUljSJpXxjZcULKPbGbwgD6p8IM5-h4e6uJs6SfRMejA3uof94K-HIbgjduu9nXUZYo_RxvozVv6mn_qumXzccjo_TMUAsX5EoZ5I6j1HiIuR701hWK1lvOpOiQHFjDvIXnKjORh3R53xgFlTqBeUTQ4dKI0b570g6K7gzNn-9vHny1FykBbQBoSsBLeiWu6r-hb10oXqSJp7ApQlvMhPkmFUn9x5jmn-invLnr28QDnrdOV4q2HanVxlPjGhfu91JFU53eFZZZhhQLWCk-abRo3XSYt-g8kRQALM3NQMo29mxAPegZX2VyWxqSYxR9KhIzZRIdlFzrPCVPvAtY9mq0_f8O-_GzBkWA)
