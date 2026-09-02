[//]: # (ob:18ff50c1)
# Artifact Provenance Protocol

[//]: # (ob:2a745bc5)
> Status: draft protocol boundary with an implemented Evidence Envelope V1.
>
> Scope: provenance for produced artifacts of any media type. The built-in
> implementation verifies DOCX semantics, recognizes PDF structure while
> verifying exact bytes, and falls back to exact bytes for other formats.
> Markdown and static HTML remain the only native portable-ledger carriers.

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
| Artifact evidence envelope | Any readable file | Exact properties supported by the selected adapter and provider; built-in support includes canonical DOCX semantics and byte identity for PDF and other files |

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
The reference registry ships:

[//]: # (ob:a9292193)
```text
adapter   proofpress.generic-binary   maximum level: byte
adapter   proofpress.pdf              maximum level: byte
adapter   proofpress.ooxml-word       maximum level: semantic
provider  proofpress.digest           supported level: byte
provider  proofpress.ooxml-semantic   supported level: semantic
```

[//]: # (ob:fa2430ec)
Changing an evidence JSON field from `byte` to `semantic` invalidates its
`evidence_id`. The registry also rejects any adapter/provider combination that
did not declare the requested capability, even if the identifier is recomputed.

[//]: # (ob:0b334035)
## 4. Evidence envelope V1

[//]: # (ob:5f062bd3)
A DOCX record created by `provenance create` has this shape:

[//]: # (ob:69d7ad6e)
```json
{
  "protocol": "proofpress.artifact-provenance",
  "protocol_version": 1,
  "evidence_id": "ppe_<content-derived-id>",
  "subject": {
    "name": "proposal.docx",
    "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "byte_length": 12345,
    "format": "docx",
    "digest": {
      "algorithm": "sha256",
      "value": "<lowercase-hex>"
    },
    "semantic": {
      "algorithm": "sha256",
      "normalization": "ooxml-word-c14n-v1",
      "digest": "<lowercase-hex>",
      "parts": [],
      "metrics": {}
    }
  },
  "verification": {
    "status": "verified",
    "level": "semantic",
    "provider": "proofpress.ooxml-semantic",
    "adapter": "proofpress.ooxml-word",
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
digest identifies the original file bytes. For semantic evidence, verification
compares the canonical format digest, so an equivalent ZIP repackaging can pass
even when the original byte digest no longer matches.

[//]: # (ob:50d7dc1d)
### 4.1 Admitted decisions

[//]: # (ob:1fc03f38)
Applications may attach a portable, host-neutral decision register to an
admission with `snapshot --decisions decisions.json`. The register is stored
as public testimony in the event and therefore travels in a portable capsule:

[//]: # (ob:a552fc8f)
```json
{
  "schema_version": "proofpress/admitted-decisions/v1",
  "decisions": [{
    "decision_id": "decision-001",
    "target": "stable application-defined target",
    "before": "optional prior state",
    "after": "optional accepted state",
    "status": "implemented",
    "supersedes": [],
    "evidence_refs": ["evidence-001"],
    "next_action": "verify the accepted state",
    "artifact_binding": {"path": "artifact.md", "sha256": "<lowercase-hex>"}
  }]
}
```

[//]: # (ob:539a23f4)
`target`, `before`, `after`, and evidence identifiers are intentionally opaque:
a host may use a clause, issue, work item, or another stable object without
making the core protocol domain-specific. The engine validates the record
shape and status vocabulary (`accepted`, `implemented`, `pending`, or
`superseded`), but does not assert the truth of the decision or resolve its
target. These records are provenance assertions, not semantic verification.
A decision-only admission is allowed when the visible artifact body
is unchanged; this records a new accepted transition without manufacturing a
text edit.

[//]: # (ob:6e94fedc)
## 5. CLI

[//]: # (ob:5b70b5cc)
Create evidence beside any file. The default `--level auto` selects `semantic`
for a recognized DOCX and `byte` for PDF or the generic fallback:

[//]: # (ob:7afe0f1d)
```sh
proofpress provenance create proposal.docx \
  --output proposal.provenance.json
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
The command exits `0` only when the declared verification level passes. DOCX
semantic verification can survive changes to ZIP compression, entry order, or
timestamps, but fails when any canonical Word part changes. Byte verification
fails when digest or length differs. Unsupported levels, providers, or
adapters are usage errors rather than downgraded successes.

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
    OoxmlWordAdapter,
    OoxmlSemanticEvidenceProvider,
)

registry = EvidenceRegistry()
registry.register_adapter(GenericBinaryAdapter())
registry.register_provider(DigestEvidenceProvider())
registry.register_adapter(OoxmlWordAdapter())
registry.register_provider(OoxmlSemanticEvidenceProvider())
record = registry.create("proposal.docx")
result = registry.verify("proposal.docx", record)
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
The protocol boundary supports these current and future format adapters:

[//]: # (ob:93245741)
| Artifact | Appropriate evidence |
|---|---|
| Source code | Git commit/tree identity, pull request, review, and check-run references |
| DOCX | **Built in:** canonical Word package digest and logical metrics; future: declared visual render |
| PPTX | Slide/shape/notes identities plus per-slide renders |
| XLSX | Sheet/table/named-range/formula identities plus recalculation checks |
| PDF | **Built in:** byte identity and descriptive structure metadata; future: page renders, extraction/OCR reports, and preferably a relation to its editable source |
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
  generic adapter. DOCX and PDF adapters inspect package/file signatures.
- OOXML parsing rejects DTD/entity declarations, duplicate ZIP parts, oversized
  individual parts, and oversized expanded packages.
- DOCX semantic verification canonicalizes the Word package but does not prove
  that Microsoft Word or another application rendered it identically.
- Generic and PDF evidence does not render, recalculate, or semantically diff
  binary artifacts.
- Existing Markdown and static HTML workflows retain their current command,
  capsule, ledger, and verification behavior.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZkYmRkYjQ1ZDIwZmMzNDc5NzRlMmZjNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjU4YjlmYzhjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV80YzM3Y2VjYWQ5OTU1ZDIxMjRjNTFmMDAiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VjMjFhMmZhMGY3N2YzNGFmMzE4MDMzNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXXtz20aS_yoo3T9OjqTwfii3qVIU712uktgV-_a2LnJJg5mBiDUJ8ABQstb2d7_umcEMKJKQRClZZ29cuxWKwLx6evr56-HHI9J0ZUFod1Gyo5Oj1eoiZjljeRgx3y1oECZZEnK_oNHR5Civ2e0FK69428G77Zz4UXwS-X4RBxl3w4i4GaMRibI8hSas4GHMPEJSl7CioDTP_Ch14TmLecb8sKAezzLol5Utra95c3t08hH_6C46cgUjLEiHQ03gQ84X8MVfeFMWJckX3Gn4ddmWdeXM4f26uXXyW-d1U9fFquFtC21WhL4nVxwXtfF1U_-Nw3LXDXY477pVe3J8fFV283U-o_XymM55tSyrq45UV2ngHm-0bvj_rkv4fLFueXNB66rlFdCia9b88-RozgkSMUrzrKApPZLfXPBr8RIQl1-ENEgop4RlWQQk9vyQRl7hujizuulwaReLsuIw835HFhec-h7xC-IWSVIEISkCL3WDIJHLUbO7oGTVrhewYB_nSeuGtUcnv348UsN_PIJdrpsWP8nHnF3kQPJfj2jN-Iejd7CCnhtgYFbT9vj0l7c__Pn07O3F619e_eXlz6c_n73Ej29fnb36cbZkR5NH8Q_puqbM1x1s20VO2rLFHSBNhbOHZ7DXXHS57uZ1g_N8X1bYa3sLT5bwpCJL3FA538lRCw2hr6OTar1YwOzpHPaMy1Xni5q-h3e9tCgil3rwOmxXxz_g2k7VpJFjgDqkohw_djWtF_CiGpYwJuazQl7jN_DNvzj3tOxuVzhB3HZgoaPPEzMRnyRhlAs6PH0i3zpvOtKt2xOHNaTonJVq4-T1umIEjsMNcLRDKqdcrhZ8CRzAmfMXz4EOzDRXpCEbc0ySOCJB5m_M0Zs53_OirErct1Hq_Itz990ResR-lFE3Cg8byxx1p2ydbs5Hd8Yp6sZ5X9U3C85AJOwngJ9zlhS-d9ik3sI09E60HHsHpobZNZw70B_lq649GaN_zNzCZfyw4afO11-bxX_9dU-ZhoMghbbtvFw5ZFlXV8gY_cGdOGXXOmZSC5CnG5NyUx5QnqaH0gRmoWiB4nrBYbTB7gnB77z-_s_txHlVFCXsGkieNXJsO0apKEjiLNjkHn_mvL2pocvlCgZDLWF2Y93AYnl7D_8-rIcRrqaFF0Yui59zXgNqzQlsqepKHms8630nY6wV5qBtqMufc2KfnDfyLeeTc7ZuGpiOA5p8hX__95x0wFnY4TWcgU_n1afpdKr_D3-ayQq1tzHbNOR5TOizkhFPJ_8A3A175vz6WmlbIzdAOuJYDXx-9-L1q1_enn7348sLqQFHCJtHAQ-Yvykzg5kjbRXac_01X9zHfHsbjfAbSz1K4jB94ugvr0vGUWIyThcEWA0oBXRY3Dp1xWX7MeYKvDB1ffrUWVxeXmLb8wosoPegr-BfDu8Cy9coseARbyqycKT54oBMr3M05hycvJkemgebhxJsJTADnjq9H8UbIDhBmJMVyctF2d06lMN_qysQX1XdOUvSvOeCw3ICqqadOafiCIyeTJ8ncRw9cXZvhaQveCP2seFXwOkoG0Dot7CLi9uxDSSZn_leFjzXBhJGVrBZsIHGQJ1d8Qq6o1PYU5RaDhDrQ7lcL7f4a2sDC-KHgcvpE6d3hvZhKdUf7zn-P9-8-tkpSr5gTtHUS-cyv-34JbLcZcuXpOpKeumU1Qjx3DwIQjfY3MBw5uhDxSuYGYrFv3j3iID9rUZkQFS4sZ-z4Knjn_YHizacoL0ILtXlylhT8utLqYSEWp-TFR9jqzhjCQFv76kzA776W1tX59XH88pxzo96uX9-dCL_6lmsN2qmZtrnRxNsNMJdacSKmHv-k2epWl-i4VWvkClBWJGKOfO67aYM7SXOZs4PHcgP4FcQcpoNR4jocZ4WcUGePL1-LHDVLkHQdyA5wXqu0IsFWYHKmzO0BYH10Wzsu8UJj-0xz8KCs82zGc2csx9_uIfZ9UtjvJ0nbh7Rx_Z-JljVHPKct_AJ9uIWjvpilGcTUnC38NgjRwQWbefnleFFZ-vkwPFCH3-2YoVzfo5MOZ3W62617pxmhD0T4jI3vaMf7p_QKZN8J5QjnIqSN62UcETKPKk7x0jBWFrwKAp-O1KAqf9B06IfYz8pQsKiLI28R05IqIlbwdRUmanIBQ65ImUFFJJOEoq-MWqkURQnPntWxriWM9vBGNuCYYsaMfApTcL8kRNCQwFs6CUKJrCH4cBfupfCQnBu5hwcw8XCydflopuWlYPK0KFzTt_DvMmYR8YKF1wyb1NMxWD_KFMAh8OVw7Ia5_T1fcJhvOWIxEgKnqTB88wDSfV33tQgu1e8wv24HdhY0BglfQl66dfLQSBObd2YSC9IRorYf445An-tbrs5akdxurcnwjEIBPzlvEDWcrTi-AVsxBH2Yknk0jT1nmOSp8BWstnYCfMzt4hoQp9jRG9mfBnitNLXu1STEBoQe7sEE_RCGI6X35xXvmhTMj4SDYkTL80y_1nY61S_OWqb88Sjqf8bUqVvbcjSrlfIMZxJ4rSCOiNUSbMwz7I8f65Dp92XPuDu5HU3H7pdchkyrgXqvajRK2tGyBglPI59mj3HFF_37ynJuFyDFsm5MKqaZVlhkIGKoCOqlpYsuQ63OWMaJo09j8XFxhSTmfPnulmSrj9BDgOC0AcEY8dbjojQHHQsSXL6HPPYiInq6LTiL3AhuqaurpD8stNWBK7BKnJge0dIlQV-GCWh9xxT_GRiQPBxBbNdNeWG-TiMXsFH5029btCWAZHpjIWxIrDc8oTEzzHLUwySOsKHFs6ZMuW-f3X2V3DE6jX4rxV2uwA9Dktga5gghgpxEWPSJQ6yIi82rZp05rzhYCrhQcNz0Yfc5NFTu1jeG019RDcj3AhGnx_GQfHsM5waFwrUOCMdmTgVvxaywEHDsFmLXUGHCP9EwwiONP8AA9-Vhe8mfZ7tCDrArNSF8qKP1JM-QcYvgjSiGQM1Evk0TFPqJ3HhBwGye1V3Ypf64KRKBUo5s6rLqhOZzUaMhFmv_i9Mer3DHOKipLeDHoZ5xUEnImN5YMqxrYvuAlxZOLVwTlRms829E8_3aJ6xjOaEcswaRNxLco8Guetl8FeSxgHzkyRMaOSCpi_ymHDQ9wnxWQFOLvbdkU5kKOVunYTxZyA05gl914-nbjL1s7euexIlJ573r_BBZE4VxVEsxHEG3cXAQObbj79xWlMwqsw6zkk7FxGZ1M25l4YkwfmJPgaJSMXDh2QT1QABT2gcu2CK5qQfYJBgVAM8JUu4GVqYnVffwv-cNxjdPxl6MKjklLhhWsm1Tl0IZ3vJWUkcXMfMQU3Q-xXYlwoHmrFlGE-4RGUfgRYOiIxfzpyfSPOe1TeVOPHIKtD6P97-9CP21vAlOHNC3wpXpoKn16B6FIdPReYPFDZpGvSEZztEoqJtyvLCy0K_CH1N20FitN-8ByU7VZcxiSLuhiEvmO5ykP9UXT4lp-nc1M17GVqqqwojO-fVIMmnRNgKHgi5ojeY5KhrbzBZc0NavZMT-Kqk834zmvNKCA_Y4rKbyNeFYSgaqUcTsS04bZyLo2Q1fCE03bLsOtF8hPJ-DCLBz4KABb7mapORVWQ6OMuqRnF5God-nsQsDPX-msSrGuUpyVRJRcHNdYM-Fy5fQBV6qkhaKSsII9L9hsBBw5F7xSTHJWJZDRiX0D-0v0K1NxWHuA_ZckXfHNShNmNVZ9tRcugWjw-XS1I2WCsExIo33a3cNBEEVBMRq6DdWpgX0uqd7fAHFImTxA88zrzcFSgYQeJBGllv5OGpYSDEEhRWOwE2b-gcjjp8Jewx7Z-3ksjFuluLjI08-Nq-ZLylDRgMuIEyzIGTh-5wTjLur9hfUm6Eb8MC9F7BMh4GseYok6A2EuPg9LIaiILlQDHZGPn6gAwyztty5PH5YjVSHlLih5z4Wag12CCFrEZ6WgLY-XlTRjtKRn_aK-jh0XeobFVMs7udGMnSA8IEHyxXa_yOlUWBfy9IuUR2EACoCbxKWvGi8Pnu2lpialrybqlC9BEqdEzBesdmIpL4yXkptJU6QKi-tAuNZ1IcM74A8YtacofH-Y0JuamGePAFW0rAnXh7wasrUNg7U-e9dPPyNOYxWmta1Qyy6QMZemguHMymN69fnoGd9BXM8bxaVxJ3JTIbraNgaH2IsZXmuTx94CPPyXUJiovVIl3awEnkKLrr9dUcqXRe9WaByhIqYo2dPnCbw6TwGI_zfsWDpLw5fY_Jr6u-C-56fp6CmS40kOh7kHJXfR-YPe-PmhsmYHHElAsvTIwxSKirMZ6UG--UEhf8JP6pwIW0sQQLS0PLcNl51WDIsxm8TfoF4oZWdQWExAHxLaDbeaXlZt-gEH7ulNxgznxRX4kGazCYgG2UgYa9C-ZotSycqkca4qlO5nkFRNgRsOz5IA998CwS8C30Xg0y_4qOT0nii5APUkgx5XklAz8YmuIfVuB6lbjp_QHGQ68JJrgAO1rUN9CLtJ5YDcvGEdEGvgXd48zLqzk8Br45ETsyVRYYE96_FkYtuRUN50J9CRtuhbJLbwbqRWEdiC0c6rFdbdsVirN2znkn9my9QJOjwagEgjNHDl-WxkkEvqybG400ADQMxM2jsQn9CBS80MQPPS8P-hEGcIW7x-MQ5IGgtEjRyC0eNlXS1_wzcn2j8ShrgkfMCz8jQeppbTrANKg1PAWecE0WJRMWnThcG7leY5gzXpD1ohuGV_8mssD4cF2ZpZmjcY4REXAQC_GOESaonlDWSE07wiHcLdKEsywPuV77ADFhxPOjsA995yFNvDROU5ZoQ3MAh-hRts8GbOgdFYb2UUGZSzTXD7AOhiefilowjS5UOAMbe-rZYJNVnyt-8W_CxagQb9CAFGXTkn2re2vXQing2x9lMuhcgKplc5OGVA3wsXDhL5AQ8iWyQkEnRMnx5pvImRdKeeAs_SCM9EN5jgYD45dkcVWDLzNfyq5lRYHuEd8Avl6rgf9NSE5KWj6d8w-wJvnWZ_zPZ7W-oaDbWGQrAiGyo16kDqYujrJ8Ko6zedILha1N6xek3-yVwt0XN4XPoEE_jwvSqRX-19szpyuX0C9Zrr4dvCr1Kb7167vhepU7ubFU9L4vyo4romogyhCEMrQKBisAQ3q56h7dDlQICAL-0HZiAefV53uEJvN4koaeXxR-qi1ZA9XpD9kTQDfCdpLRCqSXcNbVWrSbuCTvUSQPfCphy4uKBIxyKckicz0YRYHeCuBU8L1PzUlRKSJU9asF-kstR38efRFyg-oGyA5_rODESnQEOiioxsWc1hjRgaGF79anHsQhB8k_HlIB5zCLooRHMTGRSAMo6on4BGgQ0h3XRdBRKTuyADuwvAITDr1u3Adt5AjpNlAjYHfVUq0IAVw3Mkb45j9OpyAGnF5WVUoFK3NXYzX0ZO7YsCPUCBIWRsQv8sgttNw2-CWji8agSb0OAB_DJ24Yg12jVY9BK_U6_fFApD6GAj4NWLI846kJKhhsktExT4EdqSe6yUwqrNFzGURBRrifUjc38TODUep17uHwo551I6_wCxonMqYtfS-DSHo8AXaBjcR57f8Qq38WGlHCgoJ4LGNGdg3AS2ruT8Ml9XxIfC8IsihkhWvEpIYqPYRM96OQDqNCRmISkswt8nhw3DRoaeAcHIpHaoUEUq28y_NKtFACo276gAnGgTDo7_xXdcd8F0JXavgWha3JQ4PXBpK3Ra-KN00N3zSkQ98MxDwMUd9UVw1hHKO4FIXzuODhPHQTngP_aoNxAJgygufRsKc-iBCRnKUsjz1XM9wACTUg9cF4Jj5b3V6-ezGbHe9-9tUIk7IiTWke8MynOsYxAEEZJn0ClAkdGmWS_Ls0ub4TFpeip3r0veCNvl0P5ICHX51XGPJQjtGftrp-8ZV5PJMfeHOh2OXFrhFffLWzSb-nL3ZPRbUSGu5P2lObSVH24o6RLpn4T73VKlq26OENWsrTvdVSDvEVBrxb3qCcw4az-v09h9rzaA7iLfRyL9OsbKBivfgfBXz1p6IgYZ6BGi2Ylg8DDJgpNTscydWiDBHHtuwM6oSA7BCJTzbIUEKzYNanBYTJUk03AyfSIIEmHUG0wEgCJEsY0CiN_SLV_D5Ajmm_dAz_1dM7TsCvpFnKA21nDCBho0R6ILBrphSltK421tybt0JxD_KJgyiYpBsYZ0qmYAhMJ3GFTaw6Gaq1vqMRGuZhSoI8YglP9cIHOLON0NJhaDFOdI5uI9Pj_Eg6A0nqu1etO_Ie0zZgkEuBJJJUuCTl54HsAo2VE_p-gqqrvlERnYHfLPwOsI-ICOqB0nn16q8__ajHU64HdAS2yR3nAwjJR_RMlPtpwKI4TLiJhxjgm0kQHQxfExa9CmqeV-AIlE1dYWKpRzVNMcuMtDSqVMGTerN9zssGDmADYmeiIpRCAlOyoGuZXQUP4wr8NkzlVEV5tZbEl4EsFQhBRaX6Estw7hzJrXMUpDTOc48AD2l2MoA7o4IfDZvr-TXmaRDFNPZDbbAPkHS7stePxMOVeC8BrvlWJm_OK4V4MDp8E0wxIlZikhduAe6hb7ImA1CdTvA9BRr3yfn3shO2Xdkdd5ieN3m71XqxEOcVVODEkZgsub9iN6fNuhqkcmVSTmDdPqnTggsCC2w1P5bCTnUtEgmL9Uay4rps1zpTIbt6_fotdvVmAc2ORbjvGLFX7VY3K95MW3xLNVdT-euPb0R7DJnLCRxjHI1NG0yFHfdB9Lu9AR8NmFwdPzkhkASfnO_QvB0QycT0wTqFLcGEHAbeXp39okzyPospaAXzwPx_j1EQqA9gKvTdBY1U8EAM-LLPGOmcOoyvJYNKHv3w_USnYY7VwRNf8g_CDJOWtpxCncOBvlYDlyAzxtKUfuISHmVgRxB9WAZoSa0gD8c8KrdF3IMh1dV5JUJCMvVyqQQPu8BOLzXN7uQIVYACp2GSNRXYE2U3yHdtqEwxSWwkprmuFii3DShjmClSDIBKEi03gywZkWMk9EAhJpSRXFv6AxCnkWNPQ1_2YiINiEtY4vpZPHBke0CmBsscjqTskC2LDlOEAq-yGYsS_ohCvGjDS2bp8JoQPCj9TjXCYoNTsQaLTmwldnfqYMCFkkaE_3LhyWIEDsNHV9IyFCA4PCe9kvvGpFPhWSWcO4Xk0aEtmUIkGoDU40wW5FYBb37SliUsQcvnVlmYK5HilD5vxys8WNOctBgqlTLdQOUcnQQfhNv6AKBK_PTLVX6IOQEm-oYKt9e3k4Ek4sLv7XlZnCX0l3HcPgffw_rEEC973MBelEYfA0V51xGjplWMQzn7wiFTaIGJwn5oDW-OUw8Z2LIU331GPt1xuw2Ku7t324ibcgS07e73u-_CkVf9iBtp1INfSjonDfuCr8kBZSHwwQfckvOEy2mWNRNZjLsSC0gocTf7Btpur9DPP8P8pSsyhKWaQDuaZlrevDSZwpkctJ__x6ObOUKhmWTXddkKhAmc-5XSAePwShTjQntuKhNHKmdEGD8Y8Z35uZcQGsJ2g-jOSZAFceKnA8T3GVgqGIPbtS4HNhTFskF-G5zzEP_98Xfc2odD2jWkW_d24n3ejdm-D8D-LCh1Droz8QPmga_EcvCkc5cVQJ8ioV7K05hlPMtoGHGeQZdulERpztwkDHkeJEXs7l_SLpx6euIGO3DqUQQKPCDknx2n7lLiERK5QZQkz41T3ykCLE7d4tQtTt3i1C1O3eLULU7d4tQtTt3i1C1O3eLULU7d4tQtTt3i1C1O3eLULU7d4tQtTt3i1C1O3eLULU7d4tQtTt3i1C1O3eLULU7d4tQtTt3i1C1O3eLULU7d4tQtTt3i1P94OHX8ZdovGKQ-XwNNDUh9XSE0sPrHwdSf9ScStwfZvhP-oJ97e8DsD_oJt-1-n-e31x4w38N-tewBHR_2o2MPoMRhP8T1EFI85EeuHtDPg3666gELfdAPCz1gPof_zM0DJnn4j1Q8YOaH_7zEg0TA8_yiwfZQ-rcIDqy8EWDbDZC9sA1xOmhZCsjkPpG5t9P1im14YkpsmrAHLmqPhNzbKRhbvR0tUmsrmKMAV94F7-yTkXt7RhqaOP5_i4CQWr-JuQ8Yt90nLfeOQFWtzyDuwzGGQgXR9wnJ_aSQiasevKlMfS2L-AeC-7lPRO7nhXl9ozwY3We_hQLn0-4Tjnu7HFZi1U15VaLlmg9dSemU7PRX9knM_aMpfxEN8HpJtvwf6V9JtOvd_geSdD9ft8p1UoawSuLtpLcRqPdPV68euUxQB_NG2r7cJ2HHN1Ly8UDu6lG0AB6GD_dJ2v2zV-FobTwPIO3FhtBs9wnavX0jzHG_UNovRoyU3du1CvXJSE0Lm66E76Zlb2TvzgLDNyKQeLs9xd1-txTulQpCXEunHSdyJSt0Zo8qLQxZSqI0SWjGvSIiIeOIRol8vcbhr8QMK8_-IZWD1tq21ra1tq21_c9lbT-82ntX5XD0eXdl8O9SDe3nJImDhKZJGOcsiorAZ0Eace5hYtjjUU6iIHYpHMTUSyLPd4OM5cSLioQlKRtb01Y5dHziZidRuqMcOmAuzWPBcv_U5dCUFYRkQZhTAxX7o5VD7yuD3rB42klv0fwdHgnfUcTW0Ry8mZcLjj1JwIeoKjUl1KoYkiwWrYPJaQzFDyusceK1CIdLsxJjvd_uD_Hacmtbbm3LrW25tS23fpZya0ZccDFzmrkuseXW_5hy64ou1ggYNKWtm6rXxI1MVK1uZAAT4Q9SecL0WlugbQu0bYG2LdD-Egq0I9QsfhKFNEgOK9AeORk88rI0iWKaJ_y3rc3e2RQrVTb-PbxpXX9YLqY3eBJ3Nu1PyhOrwnc2lmObs7jd2Iw-Xl9Dic85DQgn6e9fVi5dWM0rZNHWup4cnV1F92NNA1A4uMkSCCYgb6xk4nSpQ6gsfoW7GRz_ifMlF6GTlKRpEhY8y5KxInRhTjxzJXoRguqDw0wLmv0TVaKjYVe3ZCFq9h5YjH5dsRnsVgWHS4UwprVwY3ovZobHHXrGai3YwqXoXTx5aBG77FcOfWdmv119ux5CS4XHDiIxsuXfdVn8-ZGRf1PqhdX02ttoYVazY16D94AdO1WWPvh2yTuQ6OL7j59_myp9Q4v7K_U35e0DKvYNcWy1vq3W_x2r9T2X5T71SZyHxR-8Wl-zkNwCDUsZ1OljHmobBDPZMIbPKxG9aVQ3xqtR4Ie-AKGVTtb_rmFLFkiB__nhNUK9CX1PhPGD7IQFw-o-G1EnvDGx4V1rVQ1egCjDgTHgNP9edwrkRcT92A99ZmqUHn2ngNyX_qqfy6kqeEC0zqWKirQDK0-UmYmiEZVXGOBAlFXYhznqjUI3p69zG6vwzMAYydMo8oroaZcYbFgEd2v09UN7k4G9yeC3uMkgyt0oCWJCgiI9_CaDjXjDDswcyieUi3j-9lUXoRxr1801xl8UuAjlPIo7lJSNRPtP8DZ10D9Y2dBItaQtFdBcOXBDQcpFq25YqG4HklVA2tCw6_ufybK0TbE8aP6E6xa0dy4DPva6hee5bgHMsDAmEaPUsOsXdt0CPnyFdjay22Yb8fUbxf1f_k0N-wa6u7r7Bhld9n23QtxxmMcvgrjrXdu7IOxdEPYuCHsXhL0L4rnugvBzTsM4K8LUdw--CwIW1D4E-D-GK8iTJGAE1ppHf7BbHr7--jtM0cPOnnz99bZ5in795t3oKnupgo_fKGKd_BGvgdhc-ybmQB46U0JuAIC9LjJLt_dH2Psj_rH3R_iRX3icUELNBc32_ojf-_6IPmKn75HYqPTSullBVnvpeixCOGbGYlb68h1Moel87_dvvz9W8mloXk0ctpaWDhcRCpEumggzqcVII84NjMUSdgwls3oshEH_iqlBVbOS0xipA9OqQmCkkRQbKgNjH5tBbpyFsE1_KmlTIzPJFhgWrSSsa2iw9QcfvQgplcWlGRvXb_Sk3b6G4__b_Rtne-7fONtz_8bZF3j_RssXxYV0jX-DyzdAbYGHeKfeKZx5zmmPtUT3VZi5pmoGXAYxlZW0qYTERvTCnlY7BLQpb6JuUATpE4ffTJ8RYNquI3SOikuBFycyx1fxNZghC90r8OhYPWAECoSmxRNndxcA0YLmXJIhkmGYAD7uUa7THTTcKuHCJIIfFOFTp9iRBhTK5cS5lE4pfiIFCGb1Aw4mJjfIQ6ASKauH_UbogNHuzEJV7YryCiUzN_Zqix5OH74y2me2b992j6UsRRVm8DSNprpnYY5vYoZlffxsH_l3j_QS7CUMNjj1ioBIcSSdQc-Yq5MG1syk92rlbETwXtcT3BnazaIgcAXQdPfQvyjzUUQ5tmgo0Q7OdU1JDoqgud1KhBvw8Z7fYD0VkYOH7hUmSYUdJYgJoojVRaErR9C-gR5EmQlaNJrqRv08qoLaj5OEAxv4ie9GEWUu9QKWDH6c9U4FtS5Wu7-C2opMKzKfX2Q-_AYAXZop53QSft5ddfm7lJqCbxUHcLTyxI9oBo28yCNxGtOQuiRKQlH35ocs5BjuShnz4iKKCi-O4iL1i3jPegZlpunUzd562UkUngTxjjJTL8t44YbUlpnaMlNbZmrLTG2ZqS0ztWWmtszUlpnaMlNbZmrLTG2ZqS0ztWWmtszUlpnaMlNbZmrLTG2ZqS0ztWWmtszUlpk-vMzUz4Iio0UBVnA2ADz2aVBtWjwuo9lHssMYiBulXk5DUy-kk5y9afGEfKXKQAsnFW3lPnIqUiGXbUVW7Ry4YWrSh2bqokBvww6UJlkL3IEYMoxwr3OYmoM_j1Mua7AKVdJApPT6CHYjsf4yxy0g42bmfbhixAYK8yCNmesxz9f--SDXuscGenTa9FjrSNCP_ZdCyGth3n-tzSANVwCXdyCCZXpUaTKVyzd7qMVw_5oxTgSh7khuEEN4jjDAPNQOhdZsRs5SDNZztvXyUO8Ocl_DN9YrIBRnfFPbDyw_2ET5zHwnV23erWAnLiTQYaDjZbhu79x06hGjKRjFENrzCGuDlA3YV6ksccIDC2in8SINkXf3K7QwobAPLCOB4apBerznqidkulFSi43BOJSAwJyICAOWNOMpxt9bIBhNXePvg8G5XMN_tP6bDGGQiolUREnXpih1KCQnnjAd_mY1pu90FYg8wrKcwzE-nykOBi2hQT_b6JgXl_3u4eoHDIR_Yr0RTOJSKsdLzUjs8qvJJuZT1bjhqF2zBvGj9I2WVjWW-bT1AvSScEcl7TFmswcWJLI5WN4DfKUlPsashugZJ6_Z7XkFr-pA6TfS-dIgc6fiN4ZDQU6B0ux6KSntjmqNfa0b4Wify1wcamF7QYG9oMBeUGAvKLAXFNgLCuwFBfaCAntBgb2gwF5QYC8osBcU2AsK7AUF9oICe0GBvaDAXlBgLyiwFxTYCwrsBQX2goJHXVBwSLXmvp8n3VOavlXEvf2b0mfi5921n0a2BhcCaxBrlQQRT4ahuj11IDvrq8_UT8pv_AT8rh-xFqiF7Sk98jenaZBQOHYsyyLYes8PaeQVothyZ8W0rrt8QMX0M-_hw2u9d_2M6efd1aO_S7lsUDA3TkhCgzzP3JSCtxEHqeuHoPH9LCaRF_t-CH9S6schfAWfvDSPiyDJg9hL9i9pV8VsfOJFOypmozTPCpraillbMWsrZm3FrK2YtRWztmLWVszaillbMWsrZm3FrK2YtRWztmLWVszaillbMWsrZm3FrK2YtRWztmLWVszaillbMWsrZm3F7P_vitk0p0kRgf3ncVsx-0VXzL4VAGGNUdwHz5Cxo93ZBtD_tuzWlt3asltbdmvLbm3ZrS27tWW3tuzWlt3asltbdmvLbm3ZrS27tWW3tuzWlt3asltbdmvLbm3ZrS27_RLKbt99_j-A5EMo)
