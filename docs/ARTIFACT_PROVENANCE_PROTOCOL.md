[//]: # (ob:18ff50c1)
# Artifact Provenance Protocol

[//]: # (ob:2a745bc5)
> Status: draft protocol boundary with an implemented Evidence Envelope V1.
>
> Scope: provenance for produced artifacts of any media type. The built-in
> generic implementation verifies exact bytes only. Markdown and static HTML
> remain the only native portable-ledger carriers.

[//]: # (ob:7765a392)
## 1. Definition

[//]: # (ob:6259c054)
Proofpress is the Artifact Provenance Protocol for knowledge work. It connects
an artifact to inspectable evidence about what was produced, which verifier
checked it, what level was checked, and the work context that admitted it.

[//]: # (ob:2bed7f21)
The protocol separates three concepts:

[//]: # (ob:76d0f0de)
- **Provenance** is the relationship among an artifact, its production or
  admission context, and supporting evidence.
- **Evidence** is a concrete, integrity-bound record emitted by a provider.
- **Verification level** states the strongest property that the evidence
  actually checks.

[//]: # (ob:08e3ce88)
This separation lets Proofpress cover PDFs, Office documents, images,
archives, code references, and future carriers without describing a byte hash
as semantic verification.

[//]: # (ob:75376934)
## 2. Two compatible protocol surfaces

[//]: # (ob:cf1450d6)
Proofpress has two complementary surfaces:

[//]: # (ob:4bd21c0e)
| Surface | Current scope | What it proves |
|---|---|---|
| Native portable ledger | Markdown and static HTML | Block identity, admitted revisions, computed diffs, claims, actors, reasons, and portable lineage |
| Artifact evidence envelope | Any readable file | Exact properties supported by the selected adapter and provider; built-in support is byte digest and length |

[//]: # (ob:84eb6ac6)
The existing [Portable Artifact V1 contract](PORTABLE_ARTIFACT_SPEC.md) is
unchanged. Its capsule commands and carrier behavior do not route through the
generic binary adapter.

[//]: # (ob:b53e3d22)
## 3. Verification levels

[//]: # (ob:d81ca648)
Evidence declares exactly one level:

[//]: # (ob:314802c8)
```text
linked    binds to an external record or object identifier
byte      checks exact file bytes and length
render    checks a declared canonical rendering
semantic  checks format-aware logical units
native    carries protocol-native revision lineage
```

[//]: # (ob:c3378ff8)
Levels are capability ceilings, not marketing badges. A provider and adapter
must both explicitly support the declared level. A lower level does not imply
a higher one: byte-verified PDF evidence says nothing about page rendering,
and render verification says nothing about spreadsheet formula correctness.

[//]: # (ob:4b2e7665)
The reference registry ships only:

[//]: # (ob:a9292193)
```text
adapter   proofpress.generic-binary   maximum level: byte
provider  proofpress.digest           supported level: byte
```

[//]: # (ob:fa2430ec)
Changing an evidence JSON field from `byte` to `semantic` invalidates its
`evidence_id`, and the default registry rejects the unsupported capability
even if the identifier is recomputed.

[//]: # (ob:0b334035)
## 4. Evidence envelope V1

[//]: # (ob:5f062bd3)
A record created by `provenance create` has this shape:

[//]: # (ob:69d7ad6e)
```json
{
  "protocol": "proofpress.artifact-provenance",
  "protocol_version": 1,
  "evidence_id": "ppe_<content-derived-id>",
  "subject": {
    "name": "report.pdf",
    "media_type": "application/pdf",
    "byte_length": 12345,
    "digest": {
      "algorithm": "sha256",
      "value": "<lowercase-hex>"
    }
  },
  "verification": {
    "status": "verified",
    "level": "byte",
    "provider": "proofpress.digest",
    "adapter": "proofpress.generic-binary",
    "verified_at": "<UTC timestamp>",
    "checks": []
  },
  "context": {
    "work_item": "optional host-defined identifier",
    "attempt": "optional host-defined identifier",
    "outcome": "optional host-defined identifier"
  }
}
```

[//]: # (ob:85df6e12)
`context` is optional and host-defined. It can link evidence to a work item or
outcome without making Proofpress the system of record for that workflow.
Applications must not place secrets, raw prompts, private reasoning, or
unnecessary source content in it.

[//]: # (ob:1ee8f6fa)
`evidence_id` detects inconsistent edits to the envelope. It is not a digital
signature and does not prove the identity of the creator. The SHA-256 subject
digest binds the record to the exact file bytes.

[//]: # (ob:6e94fedc)
## 5. CLI

[//]: # (ob:5b70b5cc)
Create evidence beside any file:

[//]: # (ob:7afe0f1d)
```sh
proofpress provenance create report.pdf \
  --output report.provenance.json
```

[//]: # (ob:7a0d0865)
Add host identifiers from a JSON object:

[//]: # (ob:dd8fe553)
```sh
proofpress provenance create report.docx \
  --context work-context.json \
  --output report.provenance.json
```

[//]: # (ob:4ad59851)
Verify the current file against the record:

[//]: # (ob:855672dd)
```sh
proofpress provenance verify report.pdf \
  --evidence report.provenance.json
```

[//]: # (ob:6e0fc74b)
The command exits `0` only when all built-in byte checks pass. It exits `1`
when digest or length differs. Unsupported levels, providers, or adapters are
usage errors rather than downgraded successes.

[//]: # (ob:df03761a)
## 6. Adapter and provider API

[//]: # (ob:7fe7831a)
The zero-dependency reference API is in
[`proofpress_evidence.py`](../proofpress_evidence.py):

[//]: # (ob:1fa9af62)
```python
from proofpress_evidence import (
    EvidenceRegistry,
    GenericBinaryAdapter,
    DigestEvidenceProvider,
)

registry = EvidenceRegistry()
registry.register_adapter(GenericBinaryAdapter())
registry.register_provider(DigestEvidenceProvider())
record = registry.create("report.pdf", level="byte")
result = registry.verify("report.pdf", record)
assert result.ok
```

[//]: # (ob:d750c881)
An adapter:

[//]: # (ob:290f5c7c)
1. declares a stable `adapter_id` and `max_level`;
2. decides whether it supports a path and media type;
3. describes non-verification subject metadata.

[//]: # (ob:6718992a)
A provider:

[//]: # (ob:ae71c82c)
1. declares a stable `provider_id` and `supported_levels`;
2. creates the verification record from an artifact and adapter;
3. independently verifies that record against the artifact.

[//]: # (ob:894b99bb)
The registry requires both capability declarations before creation or
verification. Later adapter registrations take precedence over the generic
fallback, allowing an application to add a PDF or OOXML adapter without
forking Proofpress core.

[//]: # (ob:57e662c9)
Provider checks must be deterministic for the same artifact and declared
environment. Format-specific adapters should record their parser, renderer,
calculation engine, configuration, and versions in their check data.

[//]: # (ob:88611d6f)
## 7. Format adapter direction

[//]: # (ob:b985a7bc)
The protocol boundary supports stronger adapters without claiming they exist
in the reference implementation:

[//]: # (ob:93245741)
| Artifact | Appropriate evidence |
|---|---|
| Source code | Git commit/tree identity, pull request, review, and check-run references |
| DOCX | OOXML paragraph/table identities plus a declared visual render |
| PPTX | Slide/shape/notes identities plus per-slide renders |
| XLSX | Sheet/table/named-range/formula identities plus recalculation checks |
| PDF | Byte identity, page renders, extraction/OCR reports, and preferably a relation to its editable source |
| External documents | Provider object ID, revision/version ID, export digest, and observation time |

[//]: # (ob:50d0b7a6)
A PDF generated from a DOCX should normally produce two evidence records and a
host-level `rendered_from` relation. Verification of the PDF does not inherit
semantic verification from the DOCX unless a provider explicitly checks that
relationship.

[//]: # (ob:a639fbfd)
## 8. Security and compatibility boundaries

[//]: # (ob:4ad2463f)
- Evidence is data, never an instruction to install or execute software.
- `evidence_id` is integrity metadata, not authentication or non-repudiation.
- A sidecar can be replaced together with its artifact; external witnesses or
  signatures are a separate future layer.
- Media type inference is descriptive and extension-based in the built-in
  adapter. It is not content validation.
- Generic evidence does not parse, render, recalculate, or semantically diff
  binary artifacts.
- Existing Markdown and static HTML workflows retain their current command,
  capsule, ledger, and verification behavior.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZkYmRkYjQ1ZDIwZmMzNDc5NzRlMmZjNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjU1N2NkM2FhIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV85MmIxN2FjNDQ1ZDhlN2JhMzkzNjcyOGEiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VjMjFhMmZhMGY3N2YzNGFmMzE4MDMzNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXHtv28aW_yoD3X-SriTz_XBvC7huem8XaRMkud0CVSAPZ4YSa4nk5cOONsl333PmQVK2Q8eWu1gsFLSIJM7jzJnzPr_w44RWTZZS1iwzPjmdlOUy4Anniedzx0qZ64Vx6AknZf5kOkkKvlvybCXqBsbWa-r4wamTeC61Ypq4aRQHAbVZyEIrToOIuSz1rcAVcRoFLAhi6gVBagsvSbjjWJwJy3ZwXZ7VrLgS1W5y-hG_NMuGrmCHDW1wqyl8SMQGfvhNVFma0WQjSCWusjorcrKG8UW1I8mOvK6KIi0rUdcwp6Tskq4EHmrv56r4U8Bx2woXXDdNWZ-enKyyZt0mc1ZsT9ha5NssXzU0X0WudbI3uxL_bjP4vGxrUS1ZkdciB140VSs-TydrQZGJvh8y7lI6Ub8sxZUcBMwVy9hJ7JAyD_gbiTChbuwGoRPh2LKoGjzacpPlAig3N7JZCubY1EmplYZh6no0de3Ict1QHUdTt2S0rNsNHNhBOllR8Xpy-sfHid7-4wRuuahq_KQeC75MgOV_TFjBxYfJeziBkQbYmBesPjl78-7nn87O3y1fv3n124tfz349f4Ef3706f_VyvuWT6YPkhzZNlSVtA9e2TGid1XgDtMqRengGdy3kkm2zLiqk8zLLcdV6B0-28CSnW7xQRe90UsNEWGtymrebDVDP1nBnQp062RTsEsbaUQpCyGwYDtfViA94tjNNNEoMcIfmTODHpmDFBgbqbSnnkp4SZU1cwy9_I_fMbHYlEojXDiI0-TztCXFo6PmJ5MPhhHxP3ja0aetTwiuaNqTUc0hStDmnoA7XINGE5iTblhuxBQkQnPxmE1igJ7OkFd2jMQwDH0TS2aPRnpMfRZrlGd7bKHf-Rm6OHeFH4Pgxs3zvcXv1qk6ymjRrMXozJC0qcpkX1xvBwSR8mQFOIniYOvbjiHoHZHQ3UQtcHYQaqKuEILAeE2VTn47xP-BWanHxuO1n5Jtv-sN_843hTCXAkMLcep2VhG6LfIWCYRR3SrKmJj1RG7Cne0RZkXCZiKLH8gSo0LxAc70RsNvg9qThJ69__KmekldpmsGtgeVpUWLrMU75bhjE7r70OHPy7rqAJbclbIZeor-NtoLDivoe-f26FUakmqW251s8eEq6BtxaU7hSvZRSa9R1s8iYaHngc21miack7BN5q0aRT-S8rSogh4AnL_H7f61pA5KFC16BDnxa5J9ms1n3P3ztiZVub4_ayBNJQNmTshG1U3wA6YY7I3-81t62txtgHXGvCj6_f_b61Zt3Zz-8fLFUHnCEsYnvChfimT1S3TlRsQozUn8lNvcJ3xcnjcgbj2xGAy86cPcXVxkXaDG5YBsKogacAj5sdqTIhZo_Jlyu7UWWww6l4uLiAucucoiALsFfwZ8ExoLIF2ix4JGocrohKnwhYNOLBIM5gsT35GF4sK-UECtBGHAoeS_lCDCcYMxpSZNskzU7wgT8na_AfOVFQ7a0uhRSwhIKrqaekzOpAqOa6YgwCPwDqXsnLX0qKnmPlViBpKNtAKNfwy1udmMXSGMnduzYfaoLpJyWcFlwgX2AOl-JHJZjM7hTtFoEmPUh27bbW_J16wJT6niuJdiB5J1jfJgp9yeMxP_n21e_kjQTG07SqtiSi2TXiAsUuYtabGneZOyCZPkI86zEdT3L3b9Ab046pRI5UIZm8Tf7HhPw5VkjNsBPrcBJuHvo_mdGsVglKMaLkFJdlH00pX6-UE5IuvU1LcWYWAUxDykPxKGUgVz9WRf5Iv-4yAlZTIzdX0xO1TcjYiaomfVkLyZTnDQiXZHP00DYzsFU6tkXGHgVJQolGCuac7Iu6mbGMV4SfE5-bsB-gLyCkevEcISJthBRGqT0YPLMXpCqXYChb8ByQvScYxYLtgKdt-AYC4LoY9holkWCx-5YxF4q-L5u-nNy_vLne4S9GzQm20loJT576OrnUlR7JU9EDZ_gLnag6ptRmQ1pKqzU5g_cEUS0Xi_yXhbJLc0B9cIcf17ylCwWKJSzWdE2ZduQakQ8Q2pxK7rhH-4n6IwruZPOEbQiE1WtLBxVNk_5zjFWcB6lwvfdv44VEOp_6Hhh9vgyKzzK_Tjy7QcSJN3ETgo102EqSgGhK5rlwCGVJKHpG-NG5PtB6PAnFYwrRdkdgnHbMNziRgByykIveSBBGChADL1FwwTxMCj8hXUhIwRyvRaQGG42JGmzTTPLcoLOkLC1YJdANx3LyHhqQUpm75upAOIfHQrgdnhyOFZFzl7fZxzGZ45YjDAVYeQ-DR3Iqv8WVQG2uxQ53sduEGPBZLT0GfilPy4GhTh9dWMmPaUxTQPnKWgE-Sp3zRq9o9Tu24QILAKBfJFnKFqkcxxvIEYcES8e-haLIvspiDwDsVLTxjTMia3UZyF7ih3teZ_LUFKrXO9CEyE9IK52ASHoUgaOF98uckfOybgYqYYEoR3FsfMk4nXWjRyNzUVos8j5C7liZvdsqdsSJUZwxZxacmeEK1HsJXGcJE-ldF36YgruJCma9TDtUsdQdS1w72mBWVk1wkY_FEHgsPgpSHxtxmnLuG3BiyRCBlXVNsuxyMBk0RFdS023oiu3kTEPEwW2zYN0j8RwTn4qqi1tjAYRDgxhX1GMHZ85YkIT8LE0TNhT0LFXE-2q01q-IIVoqiJfIfvVorUsXENUROB6R1gVu47nh579FCR-6mtA8LEEassq2wsfh9Ur-EjeFm2FsQyYTDJWxvIhcktCGjwFlWdYJCUyh5bJmQ7lfnx1_jskYkUL-WuOy27Aj8MReAsEYqkQDzFmXQI3TpN0P6qJ5uStgFAJFQ31wpTclOrpW8zuraY-YJkRaYSgz_ECN31yCmd9CgVunNOGTkkurqQtIBgYVq28FUyI8CsGRqDS4gNsfNMWvp-aPtsEFsCu1FJn0RP9xDTIxNKNfBZzcCO-w7woYk4YpI7rorjnRSNvyRQndStQ2ZmyyPJGdjYruRN2vcw3bHq9xx7iJmO7wQrDvuJgEdmxfGTLsS7SZgmpLGgt6InubNaJfWo7NktiHrOEMoFdA1_YYWIzN7HsGL6FUeByJwy9kPkWePo0CagAfx9Sh6eQ5OLaDW1kh1Ld1qkXfAZGY5_QsZxgZoUzJ35nWad-eGrb_wEfLAtmaY6jWQiCGJYLQID6Xz_-xW1NKaiq67im9VpWZCIrEXbk0RDpk2sMGpFahh_TTdQbuCJkQWBBKJpQs8Ggwag3OKRLuF9amC_y7-E_8har-6fDDAadnDY3vHNyNSlSmWxvBc8owXPMCXoCk1fgWroc2O-tyngyJcpMBVomIKp-OSe_0OqSF9e51HgUFZj9z3e_vMTVKrGFZE76W5nK5PD0ClyPlvCZ7PyBw6ZVhZnw_A6TqHkb8SS1Y89JPafj7aAxai7vq5qdesmA-r6wPE-kvFty0P_USx7S0yTXRXWpSktFnmNlZ5EPmnzahJXwQNqV7oJpgr72Gps117TubnIKP2VsbS6jWuTSeMAVZ81UDZeBoZykH03ltSDZSAvRthp-kJ5umzWNnD7CeScAk-DErstdp5PqviOr2fToLqvexRJR4DlJGHDP6-63b7zqXQ5ppiouSmkuKsy58PgSqmC4oniloyCsSJsLAUXDnY1jUvtSeawKgktYH-av0O3NpBKbkq3Q_E3AHXZhrF7sdpUclkX1EepIOgarpYEoRdXs1KXJIqAmRJ6CNa0ML1TUO78jH9AsDkPHtQW3EytihsWDNnJ3kY9vDQMjtuCw6imIecXWoOrwk4zHuvy8VkxO26aVHRul-F18yUXNKggY8AJVmQOJh-WQJlX31-KvODcit14Kfi_lsfDcoJOovkHdW4xHt5f1RgwiB4bNRt_pFGTQcb5tRx7eL9Y7JR6jjieoE3udBxu0kPVOhzWAya_7NppoG_3pi4YeHv2AzlbXNJvdtLcsBhAm5WBbtvgbz9IUv29otkVxkACoKQyltRwoc76bsZYkrbO8t1wh5gg5JqYQveM0WUn8RF5Ib6UVCN1Xl0KjTko1Exswv-gl78g4v-1LbnoiKr4USwW4k6M3Il-Bw76zdW6sm51EgQgwWutczaCbPrChj-2FQ9j09vWLc4iTngONi7zNFe5KdjZqomFopsRYq_BcaR_kyGt6lYHj4oVsl1agiQJNd9Gu1silRW7CAt0l1Mwa0z5Im70wtbkIEnPiQVO-176H9Nf12ilCFJMIwnTpgeTag5a7XvuR3XOjapYXQsQRMCGzMLnHoKGu9zioN95oJy7lSf7RhQsVY0kRVoFWL2WLvMKSZzUYTc0B8ULzIgdG4oY4Cvi2yDu7aSakMs-d0WvsmW-KlZzQQsAEYqMDNFxdCkfd2cKZftRBPLVmLnJgwh0FSyMHiedAZhFCbtHd1aDzr_l4SBNflnyQQ1ooF7kq_GBpSnwoIfXK8NKNAqPSdwyTUoALbYprWEVFT7yAY-OOGAPvwPeQdbZaw2OQm1N5IzMdgXGZ_XfGqKY7OXEt3ZeM4Uq0Xd1loF-U0YG8wqEfu2tuXaI5q9dCNPLO2g2GHBVWJRCcOaJ8cRSEPuSyVtJ7pAGgYWBuHoxNMDswyEJDx7PtxDU7DOAKN9XjMcgDyWnZolFXPJyqrW__p7fre5NHRRMyYpE6MXUju_OmA0yDPsMh8IQrusm4jOikcu31evvAnIuUtptmWF79U3aB8WGb90frVWOBFRFIEFM5pjcm6J7Q1ihPOyIhwkqjUPA48UR39gFiojfPD8I-mMU9FtpREEU87ALNARzCoGyfDNhgEhWO8VHKuEU7qR9gHXqZPBS10E9a6nIGTrb1s8El6zVLsfy7TDFyxBtUYEX5LOPfd6vVrXQKOPqjagYtJKhaTe_bkHoCPpYp_BIZoQbREg2dNCUn-yNRMpfaeSCVjuv53UOlR4ON8Ue6WRWQy6y3amn1Lwq6FXEEyHWrN_67tJyM1mK2Fh_gTGrUZ_zrsz7f0NDtHbKWhRC1kDGpA9KlKqunUp37J8Yo3Lo0c6BupHEKNwfuG5_BBEPHkjb6hP96d06abAvr0m35_WCo8qc46o_3w_PqdHLvqJh9L7NGaKZ2QJQhCGUYFQxOAIH0tmwePA9cCBgC8bXz5AEW-ed7jCa3RRh5tpOmTtRFsj1UxyjZAaAbGTupagXySybr-ixdmrill2iSBzmVjOXlv0jAKpe2LKrXg1UUWC0FSYXc-6zXFN0iQldfbjBfqgXm85iL0Gt0N8B2-FKCxip0BCYo6MYlTS1WdGBrmbuZ1oNUcrD84yUVSA5j3w-FH9C-EtkDigwTD4AGId_xXBQTlayhG4gDsxWEcJh14z10QY60bgM3AnFXodyKNMBFpWqEb_95NgMzQIytyrUL1uFuh9XoiLkRw45www2551MnTXwr7ex2j1_qfdEYNMn4AMgxHGp5AcQ1nevp0UrGpz8ciGRqKJDTQCQrYhH1RYUem9T7mENgR_pJN2WuHNaoXrq-G1PhRMxK-vpZj1EyPvfx8CMjur6dOikLQlXTVrlXj0h6OAPuAhtJfTVf5OmfhEeMcjelNo95b7sG4CVN-2G4JCOH1LFdN_Y9nlq9meygSl_DpvtRSI_jQkwD6tHYSpNgoG4daGmQHDwWj1RLC6Rn2ReLXM7QBqOoTMEE60BY9Cf_ym-E79LoKg9fo7Ht-9CQtYHlrTGrElVVwC8VbTA3AzMPWxTX-aqiXGAVl6FxHjc8QnhWKBKQ3y5gHACmesPzYNiTKSL4NOERTwLb6gRugIQasPrReCYxL3cX75_N5yd3P3s-IqQ8jSKWuCJ2WFfjGICgeiE9AMqECY0OSf6hQq4fZMSl-akf_Shlw8wzQA54-HyRY8lDJ0bf3Vr62fP-8Vx9ENVSi8uzu3Z89vzOKeZOn91Nip4lPdx3XaY2V6bs2Y0gXQnxdyZqlTNrzPAGM5V235qptniOBe9aVGjncOK8uLxHqW2bJWDePDux406Ue6iYMf-jgC-jFSn1khjcaMo7-zDAgPX_1OzxSK4abYhU26zpUScUbIdsfPJBhxKmuXPTFpAhSz7bL5yogASmNBTRAiMNkDjkwKMocNKok_cBcqzLS8fwX4bfQQh5JYsj4XZxxgASNsqkrwR2zbWjVNHV3plNeCsd96CfOKiCKb5BcKZtCpbAuiaujIn1IkO3ZhYa4WHiRdRNfB6KqDv4AGe2V1p6HFpM0K5Ht9fpIS9p00OSzPJ6dkMvsW0DAbkySLJJhUfSeR7YLvBYCWWXU3RdxbWu6AzyZpl3QHxEZVEPnM6rV7__8rLbT6cesBDEJjeSD2CkGPEzfuJELvcDLxR9PaQHvvUNokfD12REr4uaixwSgawqcmwsGVTTDLvMyMvelWp4kgnb1yKrQAErMDtTXaGUFpjRDWtVdxUyjBXkbdjKydNs1Srmq0KWLoSgo9JryWOQGyp5S4_ciAVJYlOQoU6cesBd74IfDJsz8hqIyPUDFjheF7APkHR3da8fiIfL8L0EeOadat4sco146H34PphixKwENEmtFNJDp--aDEB1XYPvEGjcJ_KPrJGxXdacNNie7_t2ZbvZSH0FFzglCpOl7lfe5qxq80ErVzXlJNbtk9YWPBBEYOX6RBk7vbRsJGzavWbFVVa3XadCLfX69Ttc6u0Gpp3Ict8JYq_qW8uUoprVOEpP16T8_vKtnI8lc0XACdbR-KzCVtiJKaLfXA3kaCDkWv0UQWAJPpEfMLwdMKmv6UN0CleCDTksvL06f6NDctPFlLwCOrD_bzAKEvUBQoW5u-SRLh7IDV-YjlHXU4f9O8ugm0c__zjt2jAnWvHkj-KDDMNUpK1IKBJQ6Cu9cQY2Y6xN6YQWFX4McQTtlGWAluwc5OMxjzptke_BUO5qkcuSkGq9XGjDw5e46EXHsxs9Ql2gQDL6Zk0O8UTWDPpdey5TEomTJJltvkG73YMyhp0iLQDoJDFy65ElI3aMejY4xJBxmnSR_gDE2duxw9CXxkxELrUoDy0nDgaJrAFkdmCZxyMpGxTLtMEWocSr7NeiZD6iES9d4KW6dPiaEFQUc1OVjNhAK1qI6ORV4nJnBAsujFay_JfITBYrcFg-WqnIUILgUE-Mk_u2b6fCs1wmdxrJ05W2VAuRdgAkgzPZ0J0G3vzSRZZwhM4-1zrCLGWLU-W8jchRsWYJrbFUqmx6D5UjXRN8UG4zBUDd-DHH1XlIrwF99Q0drvG304ElEjLvNbIsdQnzZdzX9OANrE9u8cLgBr6I0jA1ULR3De3dtK5x6GRfJmQaLTDV2I_Ow_fqZCADtyLF959RTu94uw2au5vvtpFvypHQtpu_3_0uHPWqH_lGGv3gTcbWtOL_h1-TA85C4oMf8ZacA15Osy247GLctFjAQoW7-dJGt-dr9POvQL9KRYaw1L7QjqFZZ29e9J3CudrU0P9xcr1GKDRX4tpmtUSYgN6X2geMwyvRjEvvue9MiHLOiDD-asT3yFuf9JnPIVLBGtxd5yJwoWiWe-R3j3Me4r8__i9e7ddD2jtId7faqf35bsz2fQD2J0GpC_CdoeNyG3IlnkAmnVg8Bf6kIbMjEQU8FnHMPF-IGJa0_NCPEm6FnicSN0wD68tHugunHp1a7h049e4VYf_PceoWozalvuX6YfjUOPU7TcARp37EqR9x6kec-hGnfsSpH3HqR5z6Ead-xKkfcepHnPoRp37EqR9x6kec-hGnfsSpH3HqR5z6Ead-xKkfcepHnPoRp37EqR9x6kec-hGnfsSpH3HqR5z6Ead-xKkfcepHnPoRp37EqR9x6kec-tPg1N9__h8wZC_p)
