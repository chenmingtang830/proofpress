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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzZkYmRkYjQ1ZDIwZmMzNDc5NzRlMmZjNSIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjNkMGNiNmRlIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV80ZDhhNTg3N2M5ZTFmNWE0ZGVlNzg0NTIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2VjMjFhMmZhMGY3N2YzNGFmMzE4MDMzNyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtXXtz27i1_yoc959sriTz_fC2O-NN0nbvZDeZTbrt3FXGBgHQYiORKknZcZN893sOHgRpS7QtOfsaZtpZWSSAg4OD8_wB-nhEqibPCG3OcnZ0crRen4UsZSz1A-baGfX8KIl87mY0OJocpSW7PmP5Ba8beLdeEDcITwLbCxLHI34U-1HIHBLRmGRBxpLUC7kbxo6dBiEN4jj0SBJmiZ0xm2SeG_hOSkLsl-U1LS95dX108hH_aM4acgEjLEmDQ03gQ8qX8MVPvMqznKRLblX8Mq_zsrAW8H5ZXVvptfW6KstsXfG6hjZrQt-TC46T6n1dlf_mMN1NhR0ummZdnxwfX-TNYpPOaLk6pgterPLioiHFRezZx73WFf_PJofPZ5uaV2e0LGpeAC-aasM_T44WnCATPWbTNGT8SH5zxi_FS8BcfuazmARxFNGEO1lAfMY58C1wkbKyanBqZ8u84EC5XpHlGaeuQ9yM2FkUZZ4PzHNi2_MiOR1F3Rkl63qzhAm7SCctK1Yfnfz88UgN__EIVrmsavwkH3N2lgLLfz6iJeMfjt7BDLQ0wMCspPXx6Y9vv_vr6bO3Z69_fPXTix9Of3j2Aj--ffXs1cvZih1NHiQ_pGmqPN00sGxnKanzGleAVAVSD89grbnoctMsygrpfJ8X2Gt9DU9W8KQgK1xQSe_kqIaG0NfRSbFZLoF6uoA143LW6bKk7-FdJ86ywKYOvA7L1fAPOLdTRTRKDHCHFJTjx6ak5RJeVMMSxgQ9a5Q1fgXf_Mm6o2VzvUYCcdlBhI4-TwwhLon8IBV8OJyQb6w3DWk29YnFKpI11lq1sdJyUzAC2-EKJNoihZWv1ku-AgngzPrJsaADQ-aaVKRHYxSFAfESt0ejM7Oe8ywvcly3Qe78ybr57gA_QjdIqB34-41ltrqV11az4IMrY2VlZb0vyqslZxd8gAFuylmUuc5-RL0FMtqVqDn2DkIN1FWcW9Af5eumPhnif8jszBaaY4_hp9bTp2byT59qzlQcFCm0rRf52iKrsrhAwdAbd2LlTW0ZopagT3tE2TH3KI_jfXkCVCheoLpechits3pC8Vuvn_-1nlivsiyHVQPNs0GJrYc4FXhRmHh96XFn1turErpcrWEwtBJmNTYVTJbXd8jv_XoYkGqaOX5gs_Ax6epwa0FgSVVXclvjXtedDImWnzLXoTZ_TMI-WW_kW9Yn69mmqoAcCyz5Gv_-54I0IFnY4SXsgU_z4tN0Om3_D38aYoXZ61Eb-zwNCX1UNuLu5B9AumHNrJ9fK2tr9AZoRxyrgs_vnrx-9ePb029fvjiTFnCAsWngcY-5fZ3pzSzpq1At9Zd8eZfw7Ww0IG8sdigJ_fjA0V9c5oyjxmScLgmIGnAK-LC8tsqCy_ZDwuU5fmy79FAqzs_Pse28AA_oPdgr-JfCuyDyJWoseMSrgiwt6b5YoNPLFJ05C4k35KF70N-U4CuBG3AoeS_FG6A4QZmTNUnzZd5cW5TDf4sLUF9F2VgrUr3nQsJSAqamnlmnYgsM7kyXR2EYHEjdW6HpM16Jdaz4BUg66gZQ-jWs4vJ6aAFJ4iauk3iPtYCEkTUsFiygcVBnF7yA7ugU1hS1lgXM-pCvNqtb8nVrATPi-p7N6YHkPUP_MJfmj2uJ_983r36wspwvmZVV5co6T68bfo4id17zFSmanJ5beTHAPDv1PB-ioB51_sxqNxUvgDJUiz85d6iA3a0GdECQ2aGbMu_Q8U_1xqIVJ-gvQkh1vjbelPz6XBohYdYXZM2HxCpMWERYyA-lDOTq33VZzIuP88Ky5kda78-PTuRfWsS0UzM1ZM-PJthoQLrigGUhd9yDqVStz9HxKtcolKCsSMGsRVk3U4b-Emcz67sG9AfIKyi5VgwHmOhwHmdhRg4mT48Fodo5KPoGNCd4zwVGsaAr0Hhzhr4giD66jbpbJHhojXniZ5z192Yws569_O4OYW9fGpLtNLLTgD6092dCVM0mT3kNn2AtrmGrLwdlNiIZtzOHPXBEENF6MS-MLFq3dg5sL4zxZ2uWWfM5CuV0Wm6a9aaxqgHxjIjN7PiGfbiboFMm5U4YR9gVOa9qqeGI1HnSdg6xgrE440HgfTlWgKv_oeWFHmM3K3zCgiQOnAcSJMzEtRBqqtxUlAKLXJC8AA7JIAlV3xA34iAII5c9qmBcSsq2CMZtxXCLGyHIKY389IEEoaMAPvQKFRP4w7Dhz-1z4SFYVwsOgeFyaaWbfNlM88JCY2jRBafvgW4yFJGxzIaQzOmrqRD8H-UK4HA4c5hWZZ2-vks5DLcc0BhRxqPYexw6kFX_5VUJunvNC1yP646PBY1R0-dgl34-7yTi1NINqfSMJCQL3cegEeRrfd0s0DqK3X2bEI5JIJAv6wmKltUajh_BRxwQLxYFNo1j5zGIPAWxks2Gdpib2FlAI_oYIzozE8sQq5ax3rkiQlhA7O0cXNAz4Tiefz0vXNEmZ3wgGxJGTpwk7qOI12n75qBvziOHxu4X5IpubdhSb9YoMZxJ5tSCOwNciRM_TZI0faxN14YvOuFupWWz6IZdchoyrwXmPSsxKqsG2BhEPAxdmjwGia_1e0ozrjZgRVIunKpqlReYZKAi6YimpSYr3qbbrCELE4eOw8KsR2I0s_5aVivS6B1kMWAIvUcydrjlgApNwcaSKKWPQUcvJ9pmp5V8QQjRVGVxgeyXndYicQ1ekQXLO8CqxHP9IPKdxyDxk8kBwcc1ULuu8p772M1ewUfrTbmp0JcBlWkNpbEC8NzSiISPQeUpJkktEUOL4Ey5cs9fPfsXBGLlBuLXArtdgh2HKbANEIipQpzEkHYJvSRLs75XE8-sNxxcJdxouC90yk1uPbWK-Z3Z1Ad0MyCN4PS5fuhlj07h1IRQYMYZacjEKvil0AUWOobVRqwKBkT4JzpGsKX5Bxj4pi58N9F1tiPoAKtSZyqKPlJPdIGMn3lxQBMGZiRwqR_H1I3CzPU8FPeibMQq6eSkKgVKPbMu86IRlc1KjIRVL_0XFr3eYQ1xmdPrTg_dumKnE1Gx3LPkWJdZcwahLOxa2CeqslmnzonjOjRNWEJTQjlWDQLuRKlDvdR2EvgrikOPuVHkRzSwwdJnaUg42PuIuCyDIBf7bkgjKpRytU788DMwGuuEru2GUzuauslb2z4JohPH-R_4YNvQSnEc1UIYJtBdCAJkvv34hcuaQlBl1XFB6oXIyMR2yp3YJxHSJ_roFCKVDO9TTVQDeDyiYWiDK5oSPUCnwKgGOKRK2E8tzObFN_A_6w1m90-6EQwaOaVuWGvkaqvMRLC94iwnFs5jZqEl0HEF9qXSgWZsmcYTIVGuM9AiAJH5y5n1Panes_KqEDseRQVa__3t9y-xt4qvIJgT9laEMgU8vQTToyR8Kip_YLBJVWEkPNuiEhVvY5ZmTuK7me-2vO0URvXi3avYqboMSRBw2_d5xtouO_VP1eUhNU3rqqzey9RSWRSY2ZkXnSKfUmFreCD0SrvAJEVbe4XFmitStys5ga9yutCLUc0LoTxgifNmIl8XjqFopB5NxLIg2UiLpXQ1fCEs3SpvGtF8gPNuCCrBTTyPeW4r1aYiq9i0d5VVjWLzOPTdNAqZ77frawqvapRDiqmSi0KaywpjLpy-gCporkheKS8IM9J6QWCj4cjaMMlxiZhWBc4l9A_tL9DsTcUm1ilbrvibgjls3VjV2e0sOXSL24fLKSkfrBYKYs2r5loumkgCKkLELGizEe6F9HpnW-IBxeIocj2HMye1Y6pZ3Ckjtwu5f2kYGLECg1VPQMwruoCtDl8Jf6yNz2vJ5GzTbETFRm781r9kvKYVOAy4gDLNgcRDd0iTzPsr8ZecG5BbPwO7l7GE-17YSpQpUBuNsXd5WQ1EwXOgWGwM3HaDdCrOt_XIw-vFaqTUp8T1OXETv7VgnRKyGumwArD1Q19HW0pHf9qp6OHRt2hsVU6zuZ4YzaIBYUIOVusNfsfyLMO_lyRfoTgIANQEXiW1eFHEfDd9LUFaq3lvmUKMEQoMTMF7x2Yik_jJeiGsldpAaL7aEBr3pNhmfAnqF63klojza5NyUw1x4wuxlIA78faSFxdgsLeWzrV2c9I45CF6a62p6VTTOzp031o4uE1vXr94Bn7SV0DjvNgUEnclKhu1pWBoOsVYS_dc7j6IkRfkMgfDxUpRLq1gJ3JU3eXmYoFcmhfaLVBVQsWsod0HYbMfZQ7jYapn3CnKm933kPq66jvjtuOmMbjpwgKJvjsld9X3ntVzvdVsPwKPI6RcRGFijE5BXY1xUG28UUZcyJP4pxIX0scSIiwdLSNl86LClGfVeZvoCeKCFmUBjMQB8S3g27xo9aZukIk4d0qusGa-LC9Egw04TCA2ykHD3oVw1K0unKpHLcRT7cx5AUzYkrDUcpD6LkQWEcQW7Vp1Kv-Kj4cU8UXKBzmkhHJeyMQPpqb4hzWEXjkuut7AuOlbhgkpwI6W5RX0Ir0nVsK0cUT0ga_B9liL_GIBj0FuTsSKTJUHxkT03yqjmlyLhgthvoQPt0bd1S4G2kXhHYgl7NqxbW3rNaqzesF5I9Zss0SXo8KsBIIzBzZfEodRALGsnRqL1AE0dNTNg7EJegQKUWjk-o6TenqEDlzh5vbYB3kgOC1KNHKJu02V9jX_jF7vNR4UTYiIeeYmxIud1pp2MA1qDofAEy7JMmfCoxObq1frNY454xnZLJtuevXfogqMDzeFmZrZGnPMiECAmIl3jDJB84S6RlraAQnhdhZHnCWpz9u5dxATRj0_CPugO_dp5MRhHLOodTQ7cAiNsn00YIMOVBj6RxllNmmlvoN1MDJ5KGrBNDpT6Qxs7KhnnUVWfa752Z9FiFEg3qACLcqmOfum7a3eCKOAb3-UxaC5AFXL5qYMqRrgYxHCnyEj5EtkjYpOqJLj_psomWfKeCCVrucH7UO5jzoD45dkeVFCLLNYya7liYK2R3wD5HqjBv6z0JyU1Hy64B9gTvKtz_ifz2p-XUXXm2QtEiGyI61SO6SLrSyfiu1snmilcGvR9ITaN7VRuPliX_l0Gmg6zkijZviPt8-sJl9Bv2S1_qbzqrSn-NbP77rzVeFkb6oYfZ_lDVdMbYEoXRBK1yvozAAc6dW6eXA7MCGgCPh924kJzIvPdyhN5uDRCMfNMjduPVkD1dGb7ADQjfCdZLYC-SWCdTWXNkxckfeokjsxlfDlxYkEzHIpzSJrPZhFgd4ykFSIvU_NTlElIjT16yXGSzXHeB5jEXKF5gbYDn-sYcdKdAQGKGjGBU0bzOjA0CJ206UHsclB8w-nVCA4TIIg4kFITCbSAIo0Ew-ABiHfcV4EA5W8IUvwA_MLcOEw6sZ1aJ0cod06ZgT8rlKaFaGAy0rmCN_8_XQKasDSuqpQJli5uy1WoyXmhg87wA0vYn5A3CwN7KzV2wa_ZGzREDRJ2wCIMVxi-yH4Na3pMWglbdMfDkTSORSIacCT5QmPTVLBYJOMjTkEdqSetE1m0mAN7ksv8BLC3ZjaqcmfGYyStrn7w4-06AZO5mY0jGROW8ZeBpH0cAZsAxuJ_ar_ELN_FB5RwryMOCxhRnd1wEuK9sNwSVoOiet4XhL4LLONmmyhSvdh090opP24kJCQ-CSxszTsbLcWtNQJDvbFI9VCA6lWzvm8EC2UwigrnTDBPBAm_a1_FDfcd6F0pYWvUdmaOjREbaB5a4yqeFWV8E1FGozNQM3DEOVVcVERxjGLS1E5Dysezn074inIb-swdgBTRvE8GPakkwgBSVnM0tCxW4HrIKE6rN4bz8Rn6-vzd09ms-Ptz74aEFKWxTFNPZ64tM1xdEBQRkgPgDJhQKNckr9Jl-tb4XEpfqpHz4Vs6HYayAEPv5oXmPJQgdFfbnX95CvzeCY_8OpMicuTbSM--WprE72mT7aToloJC_eXNlKbSVX25IaTLoX4L9prFS1rjPA6LeXuvtVSDvEVJrxrXqGew4az8v0dm9pxaArqzXdSJ2lF2UDFtPofBHzpXZERP03AjGas1Q8dDJg5arY_kqtGHSK2bd4Y1AkB3SEKn6xToYRm3kyXBYTLUkz7iRPpkECThiBaYKAAkkQMeBSHbha38t5BjrVx6RD-S_M7jCCupEnMvdbP6EDCBpl0T2DXTBlK6V315qzdW2G4O_XEThZM8g2cM6VTMAXWFnGFT6w66Zo13dEAD1M_Jl4asIjH7cQ7OLNeamk_tBgnbY2uV-mxXpLGQJJ096p1Q95j2QYccqmQRJEKp6TiPNBdYLFSQt9P0HSVVyqj04mbRdwB_hERST0wOq9e_ev7l-14KvSAjsA3uRF8ACP5gJ0JUjf2WBD6ETf5EAN8MwWiveFrwqNXSc15AYFAXpUFFpY0qmmKVWbkpTGlCp6k3fYFzyvYgBWonYnKUAoNTMmSbmR1FSKMC4jbsJRTZPnFRjJfJrJUIgQNlepLTMO6sSVv7SMvpmGaOgRkqBUnA7gzJvjBsDktryGPvSCkoeu3DnsHSbetev1APFyO9xLgnK9l8WZeKMSDseF9MMWAWglJmtkZhIeuqZp0QHVtge8QaNwn6295I3y7vDlusDxv6nbrzXIp9iuYwIklMVlyfcVqTqtN0SnlyqKcwLp9UrsFJwQe2HpxLJWd6loUEpabXrHiMq83baVCdvX69Vvs6s0Smh2LdN8xYq_qW92seTWt8S3VXJHyr5dvRHtMmUsCjjGPxqYVlsKOdRL9Zm8gRx0hV9tPEgSa4JP1Lbq3HSaZnD54p7AkWJDDxNurZz8ql1xXMQWvgA6s_2uMgkB9gFBh7C54pJIHYsAXumLU1tRh_FYzqOLRd88nbRnmWG088SX_INww6WlLEsoUNvSlGjgHnTFUpnQjm_AgAT-CtJulg5ZsDeT-mEcVtoh7MKS5mhciJSRLL-dK8bAz7PS85dmNGqFKUCAZplhTgD-RN516V89kCiKxkSBzUyxRbxtQRrdSpAQAjSR6bgZZMqDHiO-AQYwoI2nr6XdAnEaPHYa-1Goi9ohNWGS7SdgJZDUgswXL7I-kbFAsswZLhAKv0s9FiXhEIV5ax0tW6fCaENwoeqUq4bHBrtiARyeWErs7tTDhQkkl0n-piGQxA4fpowvpGQoQHO4TbeS-NuVUeFaI4E4hedrUliwhkhaApHEmS3KtgDfft54lTKHVz7XyMNeixClj3oYXuLGmKakxVSp1uoHKWW0RvJNu0wlAVfjR01VxiNkBJvuGBlfb20lHE3ER92pZFnsJ42UcV9fgNaxPDPFC4wZ2ojR0DhT1XUOMmVY5DhXsi4BMoQUmCvvRWniznTRk4Jan-O4zyumW221Q3d2820bclCOgbTe_334XjrzqR9xIox78mNMFqdhv-JocMBYCH7zHLTkHXE6zKpmoYtzUWMBCibvZNdDt9gr9_APQL0ORLizVJNrRNWv1zQtTKZzJQTX9H4-uFgiFZlJcN3ktECaw79fKBgzDK1GNC-vZNyaWNM6IML434jtxUyci1IflBtWdEi_xwsiNO4jvZ-CpYA5u27wsWFBUywb5bXDOXfz3x19wae8PaW8h3W1vJ87n7ZjtuwDsj4JS52A7I9djDsRKLIVIOrVZBvzJIurEPA5ZwpOE-gHnCXRpB1EQp8yOfJ-nXpSF9u4pbcOpxye2twWnHgRgwD1C_ug4dZsShxC8Ii6KHhunvlUFjDj1Eac-4tRHnPqIUx9x6iNOfcSpjzj1Eac-4tRHnPqIUx9x6iNOfcSpjzj1Eac-4tRHnPqIUx9x6iNOfcSpjzj1Eac-4tRHnPqIUx9x6iNOfcSpjzj1Eac-4tRHnPqIUx9x6iNOfcSp__5w6vjLtL9hkPpiAzw1IPVNgdDA4teDqT_qTyTeHuT2nfB7_dzbPajf6yfcbvf7OL-9dg969_vVsnt0vN-Pjt2DE_v9ENd9WHGfH7m6Rz_3-umqe0z0Xj8sdA969v-Zm3sQuf-PVNyD8v1_XuJeKuBxftHg9lDtbxHsefJGgG17IHvhGyI56FkKyOQulbmz082a9SIxpTZN2gMntUND7uwUnC3tR4vS2hpoFODKm-CdXTpyZ8_IQ5PH_6dICKn5m5x7R3DrXdpy5whUnfXp5H045lCoYPouJbmbFbJwpcGbytVvdRH_QHA9d6nI3bKwKK9UBNP2qZdQ4HzqXcpxZ5fdk1hllV_k6Lmm3VBSBiVb45VdGnP3aCpeRAe8XJFb8Y-MryTa9Wb_HU26W65rFTopR1gV8bby2yjUu8ltZ49SJriDdaPWv9ylYYcXUspxR--2o7QKuJs-3KVpd1Ov0tGt89yBtGc9pVnvUrQ7-0aY426ltFuNGC27s2uV6pOZmhoWXSnfvmdvdO_WA4ZvRCLx-jaJ2-NuqdwLlYS4lEE7EnIhT-jMHnS00GcxCeIoogl3soD4jCMaJXDbOXZ_JaZ78uxXOTk4etujtz1626O3_cfytu9_2nvbyeHg8_aTwb_IaWg3JVHoRTSO_DBlQZB5LvPigHMHC8MOD1ISeKFNYSPGThQ4ru0lLCVOkEUsitnQnG4dhw5P7OQkiLcch_aYTdNQiNwf-jg0ZRkhieen1EDFfm_HoXcdg-55PPVEezT_hUcidhS5dXQHrxb5kmNPEvAhTpWaI9TqMCRZLmsLi9OYiu-esEbCS5EOl24l5nq_2Z3iHY9bj8etx-PW43Hr8bj1oxy3ZsSGEDOliW2T8bj1r3PcuqDLDQIGzdHWvuk1eSOTVSsrmcBE-IM0nkBePR7QHg9ojwe0xwPav4UD2gFaFjcKfOpF-x3QHtgZPHCSOApCmkb8y57N3toUT6r0_t2_aVl-WC2nV7gTtzbVO-XAU-FbG8uxzV683diMPny-hhKXc-oRTuJf_li5DGFbWSHLumzPk2Owq_h-3PIADA4usgSCCcgby5nYXWoTKo9f4W46239i_ZYPoZOYxHHkZzxJoqFD6MKdeOST6JkPpg82M81o8gc6iY6OXVmTpTizd8_D6JcFm8FqFbC5VApjWoowRkcxM9zu0DOe1oIlXInexZP7HmKX_cqhb1D25c63t0O0WuGhg0iMbP7f9lj8_Mjovyl1_GJ66fRamNlsoavzHohjo46ld75d8QY0uvj-4-cvc0rf8OLuk_p9fXuPE_uGOeNp_fG0_i94Wt-xWepSl4Spn_3OT-u3IiSXoIWldM7pYx3qNghm0nOG54XI3lSqGxPVKPCDPoBQyyDrPxtYkiVy4P--e41Qb0LfE-H8oDjhgWF1n404J9wjrHvXWlFCFCCO4cAYsJt_qTsF0izgbuj6LjNnlB58p4BcF33Vz_lUHXhAtM65yorUHS9PHDMTh0ZUXaGDA1FeoU5zlL2DbpY-5zZ0wjMBZySNg8DJgsMuMeh5BDfP6LcPx5sMxpsMvsRNBkFqB5EXEuJl8f43GfTyDVswc6ifUC_i_tt1ugj1WL2pLjH_osBFqOdR3aGmrCTaf4K3qYP9wZMNlTRLracClisFachIvqzVDQvFdUezCkgbOna6_5k8ltZXy53mB1y30EbnMuEzXrfwONctgBvmhyRglBpx_Y1dt4APX6GfjeLWbyO-fqOk_7d_U8OugW7O7q5BBqd9160QNwLm4YsgbkbX410Q410Q410Q410Q410Qj3UXhJty6odJ5seuvfddEDCh-j7A_yFcQRpFHiMw1zT4nd3y8PTpt1iih5U9efr0tnuKcX3_bnRVvVTJx68Vs05-j9dA9OfexxzITWeOkBsAoLZFZurj_RHj_RG_7v0RbuBmDieUUHNB83h_xC99f4TO2LX3SPROerW2WUFWtXY9FikcQ7Ggqr18B0tobb33-dvnx0o_dd2ricU20tPhIkMhykUT4SbVmGlE2sBZzGHFUDOrx0IZ6FfMGVRFlSRj4BxYayoERhpZ0TMZmPvoJ7mRCuGbfp_TqkRhki0wLVpIWFfXYdMbH6MIqZXFpRm96zc0a29fw_GHun_j3ef_BzWh9fw)
