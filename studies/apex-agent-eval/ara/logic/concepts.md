[//]: # (ob:449de915)
# Concepts

[//]: # (ob:e71fde2b)
## Governed working set

[//]: # (ob:613d4748)
- **Notation**: \(W_g\)
- **Definition**: The bounded set of staged claims and relations supplied to an executor after integrity, policy, scope, and traversal rules are applied.
- **Boundary conditions**: It is an evaluation context, not an assertion that every included conclusion is legally correct.
- **Related concepts**: Staging, claim coverage, graph traversal

[//]: # (ob:71c15a91)
## Staging

[//]: # (ob:954c5d5e)
- **Notation**: \(S(c)\)
- **Definition**: Policy-permitted, non-authoritative use of a candidate claim for a bounded evaluation before human admission.
- **Boundary conditions**: Staged does not mean lawyer-admitted, trusted, or legally verified.
- **Related concepts**: Admission, policy recommendation, governed working set

[//]: # (ob:6574d766)
## Admission

[//]: # (ob:5e815eb7)
- **Notation**: \(A(c)\)
- **Definition**: An authorized human decision that permits a claim to enter trusted context subject to integrity validity.
- **Boundary conditions**: No admission study was performed in this pilot.
- **Related concepts**: Staging, authority boundary

[//]: # (ob:0cf8a740)
## Claim coverage

[//]: # (ob:01fc921c)
- **Notation**: \(K(R,W_g)\)
- **Definition**: The extent to which a working set contains sufficiently specific claims for the requirements an executor must satisfy.
- **Boundary conditions**: Topic mention is not sufficient coverage; expression quality and task allocation remain executor responsibilities.
- **Related concepts**: Requirement decomposition, information starvation

[//]: # (ob:aec53707)
## Grader replicate

[//]: # (ob:3483c647)
- **Notation**: \(G_i(y)\)
- **Definition**: An independent verifier judgment applied to the same generated artifact.
- **Boundary conditions**: Replicates characterize evaluator variation, not executor-run variance.
- **Related concepts**: Majority score, mean score, Pass@1

[//]: # (ob:2d156a46)
## Executor-only efficiency

[//]: # (ob:5bf0978a)
- **Notation**: \(E_x\)
- **Definition**: Token and wall-clock measurements from artifact generation after task context has been prepared.
- **Boundary conditions**: Excludes ingest, retrieval, proposal, verification, graph construction, and staging.
- **Related concepts**: End-to-end cost, amortization

[//]: # (ob:696e68e0)
## Fail-closed gate

[//]: # (ob:e1e1b928)
- **Notation**: \(B(x,p)\)
- **Definition**: A policy decision that prevents executor invocation when current state violates a material reliance condition.
- **Boundary conditions**: A block has no artifact-quality score and does not by itself measure corruption recall.
- **Related concepts**: Stress condition, policy recommendation

[//]: # (ob:e47094e2)
## Native-verifier hybrid evaluation

[//]: # (ob:ae1774fb)
- **Notation**: —
- **Definition**: Locally generated artifacts scored by the benchmark's native output-verifier configuration.
- **Boundary conditions**: It is not official benchmark Pass@1 because generation did not occur inside the native agent environment.
- **Related concepts**: Archipelago, APEX Agents, grader replicate

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzkzODJkY2RlZTQxZWY1ZTVmMDQ5Nzk2MyIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6Ijk1M2Q5YmRiIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9jZGMwOWNhZDRjOGJiN2Q3Zjk4NDFiNDgiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzZiMThmM2IzMjRhOGM4YWQyZmNkZjc2NiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW-tu48YVfhVC-dHNVlrzfnH_1Em3QZA2XWwWbYF4IQxnDqWJKZIZkrYVY4E-RJ-wT9Jzhld5JdqSArRoDSxgiRye23fOme8MtQ8zpiqZMF4tpZhdzopiGTmhLbgAcC1IPPAS042CyHdm81mci-1SyBWUFa4t18z2_MsoEaEJSeB4LGRmzKwgdrktWBIyAZyxwA68II5MRzhW4jDm8xgsK_DAD2OwhYtyhSx5fgtqO7t8oC_VsmIr1JCyilTN8UMMKV74KyiZSBanYCi4laXMM2ON63O1NeKt8U7leVIoKEt8pmD8hq2AnNq5rPKfAN2tFQlcV1VRXl5crGS1ruM3PN9c8DVkG5mtKpatQse82Hlawc-1xM_LugS15HlWQoaxqFQNn-azNTAKYuQ5IopFPGuuLOFWL8LgwpILbkacCZeHcRyIIIlC14rdkCzLVUWuLVOZAVreIZIu_dgKEyd2bJeFHMNqJ1wkge837rTWLTkryjpFh22yk-dKlLPLHx9mrfqHGaKcq5I-NbdBLGMM-Y-zr1uXjQ_o8-wjetJlBcFc1UJCecEKuF-gWVm1gFuWXrwZVC_iWqbigim2WKT5SvLFAkPDoajKNxsxmx-VZKyqlIzrCrFdxqyUJdkAabJkJca8Ai2vrta5Ik9uZEYiy21ZwQbvZGxDkO96NEcBJSXL7DKr0xT942u8DhSfj_MuQDPMQFq05ApYo0ff6YyGpediLoeWE_l2HHpWYHroAo8S0ptXOtVaDI0WQwOzid8UucwqnZJKayIjum-tDUWeSr4dSRgnxEiITrUTc6XMk2qZYFRAFUq2KVnG1iU4scld147ChFvcciOWxAlmaBT5SRzZ6DUjoFzfjeLIcTlzIy-KrDgIPQqER7IrRq48YGzp78w2bX9hhgvb_2A5l7Z7aXu_Nc1L08S1bZypUiw7dsCB2afR1Yf_ZPbFac5vNCafPs331g4IWfWV85cCsqtvja9zAfezj7ocRc0P3n5Ud5_f_rnGhvc_VJfarlPK8qFBAp9x3UhAZFGSofEV3JPzX7du4MVOkxDahII2BrjDK18Yo1XVtiADqB-j_hlh2ymAwEoE2PGOgm9oP8pAGHe5uiGLS6gmlX1hHHhkQrNvOcINdPM_XfPCeP36-xzLDwP5-vWlcX396m_L1fX1l9cZ3foDYMXL7uaHNRhxXmcohOQaeTJYmOJGumNegL3AY5G1Y94PuDVLDd5ULIZVE-5Hnss94cGx8vd4_MMr_uUBl9_pzrooQG1khWk6n_DY9wJXNM1ysOhKbGSTptM-j9dNeO1BaHkQB8fr2OP31WG_rzKjKUf5C4K9rjcTfpsc2Vrgmrs1ljK5MTQxIx417fxniyciYFoJj2yLn6htTxi-e_V-jkn_5UTWoxZsRUaVT4SBAfecwNyF5huFPFYh3ywwj5AXPNUFPl8-EQrHDR3uu6dr3BOMb5by1XYiK1AU4MYjKBwTwbCF5fnM3a2Ft_fAa9wJF3mWbg1IEsklZEhcpoMy8dhUpcSJGQUhO9uCPUF6u7w_lCz5DWDpZNiAWZoueDqVMX7k4xwDu4XzRyb1cyXW3erpjNmzfGq3ssBCThaerHFPML56dT8vDmaM0XBTA6kuTlwTwQA3MCMX7B3TvkdFt7C41ZMbZvV6GyspDKIqtbbhieg85_mJcDGwgsBN4l_Ppsfx-9c__rkvbH_KOabP1kAChB0N9x2jIVuP44e0j1PrO0h6HhnSDhpX9NWoaDunR4wYcNfMiC5c9-ToeobtTq8pGRlG-8DVu7d_NzQrG7lrXL2_enOIEx2vfx-DOcOWEUs63pb9zOh0Y0ac6HhjWm5zhvoRZTo7Fh1nOgOZgS4db01Pec4wYMSlzg7H1dnhGLGoE4p2h_-cY8XArs6OyZhXnW7RiFad0EwekaEz7BiRrbMjM5Cs0-0ZMazj7TnEg86ppoFvnR2fll-d0VsGZnW8MY_50Dk74cC3zg7KwLPOsGcgWSfY8xTxOavKe6Z1XqCIUB1pxscRu3uY3a23O-p6GXN8UuLcw2HRHYIclNoZ8O694xt01rY1KgVAPj__wHjitL8JyvgkeHweOj4dfng5Fns5Fns5Fns5Fns5Fns5Fns5Fns5Fvs_ORZ7_sv37uVza9alFXza_5b5qRftv8rbdG76wGIzCEw_idwkdMMwEqHv-SbDtuYFXhyaLALhoLUJohAl4Io44MDwCwv8Qw7te68eXnr2vvfq3S9Q_vveqz_M1qxc43orDBIeJ67nCaJSWsaI1LY5-RRbbYXZEQvB9rzEc71O2IjAdsKOYaOt5MgSNqJuJ55ldpJHBLWVfCbbxAEDMRBGcxKsu6yCVEsrjbLGTJQ0y-R4B3fsptMbLKmwSDHzYKVktZ23DWlulDwvYK6lVIoR_iw1VJ0CSlZgsEbcm8a0r8gQprbIMTKhTSzJxm8rQ5Za3TAVtZ1ibuDsQreaF_90p1ozmp8AxciMpzV5RrmS1vonWigphZWue54rBbxqlb8nJ9u1hDFpbpnuvAlGT33mxkqxYj14tKfjtpAFHo-EmcSJrycpDdmItA_JMEnHW2EQ2BZzuMVsm3XCRgz9MP7HcG-MaLZoaWmlu7BRl0CJwQyOOEqBYWoDkhD0ff6M4IkBbwFRWsKmY87TMP_Q5J3IMTcI1Q3gsym724JakIjGukrVpf6Aqjsg211CTCDZs_cuNQ36_ctmgyRLW4yQTlbjY1wtP4i9wLSTCMK-FIfRZMD1iZGjSxMXOy53IuH6SSduNIUcRvaY6QLD2RCErkoa0EsCVsOJRY3NFwu5DXJXZVj2Mf1QkRb0NW4g2hLh206j-n0-4N-eXdyxklRjhmxQhyRjsCoLmebPqsUuN7dN4qHKwzAJ5nm2JVzGwO3iOpqkBpieMxy1MnlkOcBtV4RJv1mM5qXDWB0zAhl3a8nXiMwoGzUcTOo23JLqCrO_LBBU_Np1bCpKOi1qfx-6oaObnWa9QXCNEi0rkyfA-5AXKJcktK2T6nJQ3sfrdyhc79O07OcaEwPR0T2flTcG1igyLS0CzUEHBlPwmQJ1yVjiI8gBJvB_P7hDaZxviryUTenKjHKp0YC7l7p9xDo_b8qWa1nMizjrm_JosBzt0M-aFLt9n0MQhJ7LBI86qaPh8XBeHDMN9oT4p1qsdCzYsCM3B4wb-IzR9pvcAZzfdw6WBl8jyeLYBLBrdB0dgbplSraNknKgA3Ch6qy5h0BNgPdn9lNTssgHFO6fure3n9_h3v176zBa4LkRj8HxLa-vt9HkO6B13AjbSg9NmzMLG60dib7zDlPtYdSOGU_5DXlc1l01Jirf9NB0aFH2NjxKV03Xe9FO3E5RIBYYHcQ-QZbe3mvOUxo0DZRIkBRUShKQuPOpHIuGPjVpxLutT7MZ-gU5Nn7eXCPzy6blTuD6NhOLKl9gcuJl0sY2OL_IX54oQDtwbceJXRxH-gIczekDpM8bvFupjilYaMV-GPIeytEsfhjKY4brfu9UeiYsh14ms9uuzd2tES9eKzo2pygiYbqVuf4vBNjSsVNh-IkHQ6oLZ4BwGtur9m0FpUSW9wm06DquLiiNXE-iYmTBFf00tktAzXrrou3GNABP7rnU1AcrDpCnw0A7YDMnCoUZ837_HZ1BDECfeIbQNXTft03XZz6LkqGh98cKB5A_8liAI9g6woKiqt8dYXdZb5i6-Q0Gu6HKeV0VdTX4gaFL5Kpuyvs5Yw6BluvWhQnSK2ibJF7gjNj4qGUgIW8e4phwmISlFKCtay1qXyhlt1LlGbWfKZas-FoWeGOVz5vXUVf0dKlbxIGdsD0j-YT__g2-CPco)
