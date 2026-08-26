[//]: # (ob:8c65fe99)
# Environment

[//]: # (ob:40559188)
## Runtime

[//]: # (ob:ddbca772)
- Node.js 22 or later.
- Python 3 for Proofpress proposal/admission helpers and receipt verification.
- RelayBench dependencies pinned by [`../../relaybench/package-lock.json`](../../relaybench/package-lock.json).
- Network access required only for real provider execution; verification of frozen receipts is local.

[//]: # (ob:b6e47420)
## Reproduction

[//]: # (ob:a13ea393)
From `studies/long-horizon-eval/relaybench`:

[//]: # (ob:78d42e5e)
```bash
npm ci
npm run check
```

[//]: # (ob:0cc4cb75)
From `studies/long-horizon-eval/ara`:

[//]: # (ob:b92fac5c)
```bash
python3 src/execution/verify_receipts.py
```

[//]: # (ob:8b2d8673)
The first command checks harness lint, fixtures, tests, and readiness. The second verifies that every admitted and secondary result file matches the content-addressed final manifest.

[//]: # (ob:246916a5)
## Secret boundary

[//]: # (ob:cc9dac7c)
Provider credentials are supplied only through local environment variables or an ignored `.env` file. Credentials, raw prompts, private transcripts, hidden chain-of-thought, and undisclosed source documents are not part of this ARA and must not be committed.

[//]: # (ob:a2b34564)
## Platform qualification

[//]: # (ob:e21fd314)
The final study was orchestrated on macOS with Gateway-hosted model calls. Result eligibility depends on recorded model/provider identity and frozen protocol checks, not the orchestrator operating system. Exact provider telemetry remains in the retained run records.

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzA5Mjc5N2UxOTIyNDU0ZDJmNWQ1ODk3ZiIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjhhZTNmZDllIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV81NjEzYmE0Y2RhNTUwZTY4YTRlZGY1ZWIiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzAwZTdiZWQ4OWE4ZDFkMTk1YWZlNDc5NiIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtWllv4zgS_iuE-2UX64OiRB3ep97B7L7NNnoG-9IdODxKNiey5JaoJJ4g_32KOmw5HTtpe2bRuwgQIA5FFev46qsqOg8jUVqTCmUXRo_mo81mQRMWJRF4CWMBDzRLueZxEqWj8UgWervQZgmVxb3VSjAeziPgWnqpCqOQsyjVNErSFDyP8sT3WJIKHsQiSVlMmRdQFVENSQJJSGOmmac5ytWmUsUtlNvR_MH9YRdWLPGETFh31Bg_SMhw4T9QmtQImQEp4dZUpsjJCvcX5ZbILflQFkW6KaGq8J2NUDdiCc6og-Wy-BXQ3Lp0AlfWbqr5bLY0dlXLqSrWM7WCfG3ypRX5Mvbp7ODtEr7UBj8v6grKhSryCnL0hS1reByPViCcE2MBfqoTGLUrC7htNqFzYcFDz5ciUFpwTiGMRQA65SCdZkVpnWmLzOSAmvcRyRaUQiRBx4mItae9hIsUgigJW3M67RZKbKo6Q4OZ01MVpa5G808Po-74hxFGuSgr96l9DHoh0eWfRnV-kxd3-egKbejx4AJsa22gmmVFvpysitL8VuQTuBXZTJRiVpVqBvmtKYt8jQdM13o0_iY0CWtLI2uLQVxIUZnKHQlZuhAVOtdCI6-2eLBT-cbkTmS1rSys8Uku1i62vepjfLVyeBjN8zrL0BC1wgBC6wKZFerGRUaFPEX44XaMnYV7Z-aPeyNwvTtHaN0osHE4gztceUcON9rtxingIoxoGT1ejXtPjxDKTpWFKkG0djRPeqfAIg48RYEhEqjCxEkjGoOIqENBXtgGsx0YSAcGgrBUN5vCNGdvRNmc5Ezt_3KWXjkUZUZtBxKGyBoIaTB7JuiqIrWLFK2GclOaDtuV9OYJ7sCdnvBk4NEQeCDBY7FgnucxSVniBej-WKkokUwlTAYJQEwVD8IgiCPlZFthG4y2EZh7GEq3MGKUhRMaT1j4i8fmPJnT8G-UzinFlzqH4y4qQAbc90aPg9WH_yKqG6i1qFuJaoX7Ax1yGQU8lirGDY2MARA7FL4Ir8fH8bO5DNrYXSZjBHM7V4WG-9FVww66VseePmGBr55-qZF9d49X9Vrk89JgXpXakeP_Al00Sp_LFgHlPPHi-IAtPta5NWs4yRTvyH7X0ziO9_K1lkpEEftW-RPyEwZp-mtFGCNFSVyZLKef8wn5sEX7c-KTFJf31ZAgDjZF5SKh9yplWDgP9JEhpm_A6KE-0ILI-f0low-3nrBceD4IP_HPOumfZbEm18fRVkImthJytbqe79VAkhQHOkSxDhhwOEuH6-trxODqc55v1kSZ9ndZ5y1Nf87x-f5ol1IHRyPpB0pG_E8xH-08abdMGKYcV5fZvWmQ5pMmre9BNXk5u3X92XaBxAJmY6vpZvuSK2LJdBxG5yHhlxWQ1JSVJdi4YaLr1v0VQYrKHe6xqNkxbrm3NebBmLh2En-5nSc8xIIw8UJxGJ6fAau5JbKocy2wUz2dCl_vPpENSiVaqEidex4m-q3RUBJ8QyO3GpFVBHsCUtVYyA1oUuTZlthVWdTLFcFTRUY6Lj7hBsGkH_AwOFDrA5INksuafKlFhr24Eq8ghqMvnXAKMC_Vvnfp6S1EcjTYZcyW3IkKKRNhUtnS9WboGrIW6t8_kzscAci_cO1ObDGjsPI99Q0WRZUJsz5aJZ5o0bVy77VGBq5l1qk7WZZCA3n_8T1pLMOiSwYl40iFOF_28-XiGPNfZsMwcY8Q_vkHfBPxH6H680_vqO8Ykf95ZrWEfoTC_1h7Bmx8vuBLWLlsmAA3TRsxFXaouNqUFXQOUpiwBNxNARF6baxLYPdauw9pEgXgDGxROI5Oa2GP8fpFKH9KzUe4_PwzLiF011yTW1E2tySO69BBxCzzAkWR6ynuum68MyU_7IWPSSnuXJe43rhI4FB3iyRBkCLzYyXhIg8e4fEj_H8pFM9jf03WSJsZQd9mCMePLbAgM0sjTWbslmjYQI5KoJB-lGrfcXdGbQBN42Hc6xx5NShlD6O7lZvSf0CXO6xap2lZ_AY5-fCRvPN5pzGmSkHEETvZNCT9CNVYUNSYdG6SwWrapUIDAZO7udEttrdlxgEGn4NAZ7gwK6hcRXj9DcaJe6w2PsOrieFcPryueHgbu97Grrex623sehu73sauU2PX66_Pv7o-Zo_PXw-_dFX-h9yHR1wmkR8GSZzKRPoA4IvE86RMhBdLnsQ6THVAZeKrNIlYwCWKZFyGlAtPUH7MoK8uxP055XNOn7kQ330Z9f92IT7eyeM8BMqkB0rqXt6giejlvdAe9MIgoZEnmPsqsxc26Bg6YRf1AmtTtd9cQrbBiHSDT8Pd3ajTJlgj76Mrq_9wZbXrN_GjG4U2Js8xj-SWfLqeTmf4sy_As-67z4lzPSpZ5NdXf3l501-bA38Ce1eUN0Qo5fTuvvHsyMwZhS1hRnYd7q4K_f1Ad1KkfT_blyViqpYEp880Q533pVYRJrUf0DjpvT_ojwahfLHp6cGWJDxQTEZ-HPUSB31QJ_HC5qY7CzjjCiIa-OlO-0G_0511XhPTOyj0Q-y1PSFT0R8x6Gteac6xZqU7JBSMxlTpRNFdDgz6l6d2XNqUdKeKiFEcK5jHm8i0tLDvU7pTv6fbBVfPmsmtGzgnyNEu2fG9tvihfibF86fHfZ2ihchfkod0h89BJ7RH_Kt6m16o4BFnNOIeVb3QQbvTl_Xv6JqhUqVpFlcG65zLBWHySZFO3FC7XNk2gGi6qVRWOA9XRV0qILpQtVOm1RxnT4Ieto5-LM66zZjs3lzXiBj3VEIDnCa6J8IS8wi95TOMyi7PBp3ZPizf0mT1QE9DmSRJFCFZ9LIHfdcB0L-Puwvdczk-tIUqsi7pxo1LXQbsNUMoFFjWRHPd0P67xpT8eO-uKHaiLWSwBttk1BoDjbUhb8QgwvFP1MXxYfdPLF9F6eoRf34HUO09og)
