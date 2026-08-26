[//]: # (ob:c2c7ab67)
# Claims

[//]: # (ob:3d71e849)
## C01: Coverage mediates quality preservation under bounded context

[//]: # (ob:24fe646f)
- **Statement**: A governed working set can preserve task-deliverable quality when its staged claims cover the requirements that the executor must express.
- **Conditions**: Supported only in the observed same-world legal-task pilot under majority rubric scoring; independent tasks, executor repetitions, and incomplete-coverage regimes remain untested.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A preregistered same-task replication with adequate audited claim coverage consistently yields lower treatment majority quality than full-corpus execution.
- **Proof**: [E01, E02]
- **Evidence basis**: Tables 1 and 2 show no treatment majority regression, while Task 2 mean declines identify a remaining expression or coverage boundary.
- **Tags**: quality, coverage, bounded-context

[//]: # (ob:8ddb3a45)
## C02: Context bounding produces executor-dependent efficiency

[//]: # (ob:f891712d)
- **Statement**: Bounding an executor's working context reduces generation effort only when avoided corpus search exceeds the overhead imposed by the governed representation.
- **Conditions**: Supported descriptively for the evaluated executor-task pairs; the design does not isolate search effort from prompt-format or reasoning-policy effects.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Across a preregistered heterogeneous task panel, efficiency effects remain invariant across executors despite measured differences in corpus-search behavior.
- **Proof**: [E01, E02]
- **Evidence basis**: Table 3 shows consistent Muse savings, inconsistent Luna effects, and consistent Sol overhead.
- **Tags**: efficiency, executor, context-bounding

[//]: # (ob:ac36174d)
## C03: Pre-execution state validation can enforce a fail-closed boundary

[//]: # (ob:4efd8336)
- **Statement**: Separating state validation from artifact generation can prevent downstream work when an unverified conflict would materially alter the permitted reliance context.
- **Conditions**: Supported only for the tested tax-status conflict patterns and configured policies; corruption recall, false-stop rate, and adversarial robustness remain unmeasured.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Replaying a frozen stress input under the same policy reaches executor invocation or produces a client artifact despite the material unresolved conflict.
- **Proof**: [E03]
- **Evidence basis**: Both final manifests record a block decision with no artifact produced.
- **Tags**: safety, fail-closed, policy-gate

[//]: # (ob:14a86352)
## C04: Reusable claims separate knowledge carryover from task-specific drafting

[//]: # (ob:e808a1c3)
- **Statement**: Evidence-bound claims can carry factual state across related tasks while leaving task-specific analysis to newly scoped claims.
- **Conditions**: Supported as an implementation behavior in the observed shared-data-room sequence; causal quality value and economic savings from reuse are untested.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Ledger replay shows that the purported reused claims were regenerated, changed in substance, or were not selected into the later task working set.
- **Proof**: [E04]
- **Evidence basis**: The Task 2 manifest separates reused claims from new task-specific claims in its frozen working-set record.
- **Tags**: reuse, task-scope, ledger

[//]: # (ob:def2f9c8)
## C05: Preparation shifts rather than eliminates system cost

[//]: # (ob:c804c12c)
- **Statement**: A governed knowledge layer moves work from downstream execution into upstream construction, so executor savings alone cannot establish lower end-to-end cost.
- **Conditions**: Supported as a measurement-boundary conclusion; the reuse horizon required for amortization is not yet observed.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Complete cold-start telemetry shows that upstream construction is negligible relative to executor work or that treatment total cost is lower without reuse.
- **Proof**: [E04]
- **Evidence basis**: Upstream Task 1 work is material, Task 2 telemetry is incomplete, and the final efficiency tables cover only executor generation.
- **Tags**: cost, amortization, measurement-boundary

[//]: # (ob:21cf656e)
## C06: Information parity changes the visibility of governance effects

[//]: # (ob:863a8f96)
- **Statement**: Governance effects are easier to identify when substantive task information is held constant and the treatment changes only reliance metadata; a treatment that also narrows information can confound protection with information starvation.
- **Conditions**: This is an inferred cross-study hypothesis from PR35 RelayBench and the APEX pilot, not a causal result from a shared protocol.
- **Sources**: []
- **Status**: hypothesis
- **Falsification criteria**: A preregistered ablation with byte-identical substantive context shows the same task-specific regressions as bounded working sets, or a coverage-complete bounded set eliminates no starvation indicators.
- **Proof**: [E05]
- **Evidence basis**: Figure 1 documents the PR35 parity-controlled handoff result, while Tables 1–2 show mixed mean effects under a working-set intervention.
- **Dependencies**: C01, C02, C05
- **Tags**: parity, causal-design, information-starvation

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwX2JjMzI2ZDI3YTYxZGEyZWVjYTJkYzc5ZCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6ImY2MTE0MmE3IiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV9mMGI5MDY1YTc5NTRkN2RlNTIwYzdkMjUiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsX2NiN2E2ZGE2YmFlYjNhNTQ4YmJkMzg0ZSIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrtW9uO28gR_RVCeQjgiDZvokj5yet4gwU2iGE7QYBdQ2h2N6VeU2yZTc5YHhjIP-QP8yWp6gvJ0Yw0M9IYuWCAxe6IoqrrdqpOFblXE9K0oiS0XQo2WUy222VB4yhl0ZykISMR55REjM5zNplOCsl2SyZWXLVwr1qTaJYusoRywvKU0iIg4TyPoiTk2TyBn0TJLM2SLOc0ovOsKDOeJmVWkDSJiiwKeEZZlIFcJhSVF7zZTRZX-KFdtmQFJ1SkxaOm8EfBK7jwN96IUpCi4l7DL4QSsvbWcL9sdl6x8942UpbbhisFv9kS-omsOBp17XIjf-NgbtegwHXbbtXixYuVaNdd8ZzKzQu65vVG1KuW1KssDl5c-3XDP3cC_l52ijdLKmvFa_BF23T823SyBkeA0DINwyQi84m5suQX-iZwLl-WQZEH6YzM81nC5ozPooDOWTRDzWTTomnLStQcNHcRqZa0gGgwkhaEFzGZJVlRsDhLuDHHarekZKu6CgyOUE8qG6Ymi1-uJvb4qwlEWTYK_zJfc7YswOW_TF5bk70PYPPkI1jisgLD3HZMcPWCbPkXH9SqW59fkOrF8-Fov-hExV6Qhvh-JVeC-j6tiNio5xtMm4ekGGnbRhRdC5FdFkQJhRrwqlwSBR5vub6na9eyQTs-iRpFqp1q-Qa-qckGA37dnikIUJgqk0XdVRVYR9dwnaN3Pk6deyaQf3jTkjacmHP0N05pvmRxxGZlEJdlDKGI8oJESZQFEZ4rW51oNoKejaAHuUQ_baWoW52QjT4JlXCfrA5bWQm6G0kYp8NIiE60EzNFybJdluAV3mwbYRNSFeGCx0VAkyTKs5KGNExyUhZlQrM8T8siBxvnhAOkkzTJizxOKEnyWZ6HxTybAYxnmLqqJWjKFfgW_zuJgij1g8yP0g9hvIiSRRT9IQgWQQD3Wj_DXTM4pYjm8eTb6OrVfy73ikrSTzoi375Nb8UNZ6LtUfOXLa9f_eS9lox_mXzUUGQdPfj1HuZufv25g2L3f4NJrdUpkLwycYDfYNcgRYp1FCpty7-g6a-1EXDJncOYVmCLDYFfwpXfef097W6Lh2MVhrMnGFUnPGZzaFNJfl14EC4gJJCMiN4NhBs7kPe5I5Vodx46ljcXpD16PJx_TzHYvrqa8cYrJP6XHVc5SkpooGn56Cr73rNn7wHCfAMxe_Zs4b3yViix5sy7lM0njJvirUdJ7QRyryXqk8_4oHIFjfiavhljUISS2Z6-EeqrPxqzUbrFjvL4F047gJt_p4vvJ4ZxwBkDszxeloIKftzFZZaH8zBij67yDRf_4OSAT52E36ve3fZ0oDmsO-JiQuM0nCf7-sYL4ELcN3Ixy7BAcw9KhGAm7TCUd7r4fmJ4XcqGco94JREVVJnjLk54ybI4Th9d5Rsufs-hycJvMXv3hZWN3HiuCHqrIy4OE5Kl8Sza0zdZeO94p3S7N4UVIKLP496nWl5WnAEe73Tx_cRQ0jQ7RKTRuyXHXcyzICMhjR9d5RsufnMhAFyU-xoWTipGSqvsoXehEqH_j7iY8TIqc5rt6TvTKWFiiAmxFmWrPPi0Bke0a0y9SmzudPH9xIha101DJQF-d7QPmgUJDSP66Cofq8VDkCqyA4Eb-MKUDJMXR1wchbRMZynf0zddeD8hfDdGX1Acm4ZtxqAwYAamrDtdfD8xhdAtSZbWojuyGFBHsjJPH13lGy7-k1EH8hi7BEyHCkoD_A1cB8MmPUxyKBU773LfxcDcTNIfYi57WthJ4RV-1Mrqn3gFX4m6xkr1q2U4v07wYLxDkVq04ivc_-rtm797mlh5SPc644FX7149P0RtTjj9VO7iWtYZio8IzsMVP5XAVAJtxZrobLwEruoJSAKoWis-VDV5cYZtIzJ0SlBOZDs13Z2h84gNnRmPB7AdNAg047aEgiEw7XqyrmxgyIUUJt2a7Rm2jZjTKfE4kRpJBTJ1AElzTmRGJOrMyDyAJA1BsTjCAdlj8rJWbcPJxnQiE6QzbBsRrlMicyKjglqgtpwKgI3HGlKiR84wYkTBzgzQAygWWEhoIxUwDo67U6btApitBS6lOLlA-cbWM2wb0bVTAnQiHzunsYzY2uM1lrvY2AgYQ5kQNdjQbe11XCC3TUfPapoDszslGidStxFXOqcpDhTvzLg8gMJhfVJdAXiBC5YHQFwGHwjlrXmlCc1Dbfs44qpXk8v17poNvYwp_HKM6mNSnQJv38Wph4u_nQfJw9GR999dH3nsYDw9XkqPV7PjRfXV05buaUv3tKV72tI9bemetnRPW7qnLd3_0pbu_g_z3cNsq9MijL_d_tT6rgf3j_J0ns5YxGNShnmZEz4jWU5TUvIopbOAZyAIJBazIgtnRRrGaR7MaTgvQXFGczKPk0MG3facPlsktz2n799n-W97Tn81WRO1RpoYJfNZmAckjJHHaBkjXmqz8jjltKIYvrsUlUlIaOJEjVioE3UGfXSs4bgacxqwPIauFvRqjJilVeMcSviQvacui_jOlX77CQ9DDJNWX3W8yNt0CgjcFx3u57_WqBzwMSbQBUq3-m6L4ADRep0nav17WWi9GIxHG-6D2jB6VXxFKl9PZltRydZ6cEN-k7qQNF3RCOopCh_r1UsQNVBIvfOYDmpBpeetUWIKPI7BzVRuthVvuU9d_BoYLDccFycbIjBgrX4Zw5rxXnbAnbQNv3y0l8Dtnb6inFXmix9JpXCLZOkQqMsbQUxwwDV4EEhunL3aRlCxcr-4FO3aIwxcrfc5nX7lxMTC69XFxQGKqVvw407AtKq8Sl5inHAExAgNznLx1Z2thEHPx91pp4a1hDVTvz-njXwThFPvTRBZYx2B8PTrH3jHB8wc5YXaoRG0UHnp1fK208HgxrzsMbWLqA9ocgSQAXUYp1gm1VC8iY0B5q5NJnQLBLK33i1QrdofyErrZO2c9jdOHeT8G5DrW6_FGyAwjnMORXOA_WgyGsP-9FX8UcQTksKUHoaUzYnTYDToHEL8d9qsd8g6SUPXIJRyzkzPRr-i6p7YbM0qe6ev90UHEhnLTN2SUVodKgKMK4DHFpcwoAIoY8qJ2X7A970vTR0golEv9S3wQ7GC3JFgUA3FQSiJ685eY2OYJlsQmM229Q0T8XQ1IEpicvmmdzsu8bhIN1tYsgf4NZScRmIIJPjXWlXzajrKkZ7b2Eok6gvgTgTyyK52nVcUumELZyKQVIfymYDfNghUhcXVxNG3Xin4mlwI2ZyIdS_WIFej0uP9uVO41MKtMpRWLKv9Vz93NXGmmKo7-vK9rPpU2sPw4Iihgk9dFvsOb4dxPA-SAFCUzOMydCgajd9jHD_GI5yjiOYFL5IkzebZnDtdRnP1IUR_pycy2NQu9PvThoKUkP0t3NBBuwVsYOpWAENStbbbb3mzEW2rUV0JzbttHO7T3B2cTR-FZP_iKw2k4ewtAelNrVx6lGKl01gDE-jkS8zgpttqAxtggBUgpQTQcRAltziwcZNbhCEvRZxUXiML4CHQUkbN3CHkUUH-Dpo22enSi3H5imvlFtsVIGHbOcpi9r4b7tlyA2Gh61GjQIBLKx0-9Y2EQMsXGM0-2g7uKNEFDA6BE2V1MYrpLQCPD2L7BwlsA-YOELUhtSghWug3fFUVVDBLd-jR5lV7TU2gy_cquVde90CsYEDBPjxCzNTa769A88PwhVEmCcJZlJOidJAZrXbG8H3E53xHURwyGrEkJ0EQMKfSaHVzCMXf6bGdU51AxHYQQ5x7a34JgAMuvO1J-x0IJYg5bOKV1tdkn2sQN3n5GuZs5kMJIj4k1Qb8_LlD2wCgBCJQ9QwTWzfXiIQMquUGKbppD8b9DceOgVP7dyHYP2PINeEHYNp21Y8p266x1mst-pAAadb039RSzFSzpcA5wT0nolBnwDH6ViQcilfQ2PQt9ukMxq0xLX00eN0CxeRwm10P1NhCsc9otae09ibEfS8r7LfCjHG2KFl9fBwEDbL34KpFT60ozKKpp8HTHMZplLEgCTMY0gvqQDHaD45xeurj3qOgLOdREJBZlCakB-Vo2XeP8fgxn97q2UbJoaa7pCeVrLEG1Zg0EE8oVkKt7aQG44HfSp_r5qfae0DWMT00x3cUBNWgVYcF-qWd0hFka5i-vuq-qWd2phsy2YAw8bV_zIlq7SAtHNQfFY2v7ZANClYMmz9w8pZjxWmba-i81aFaPb6qxEqY_90LEKaf1o7crKOleQZivB89W9lCTUKfohDjbGxdsmuNcx4Ey7867TQ2Q3MoyHUteOpAO9gm1GjHYBgKBsa02RHVb80QbRYsmjX1pg3Ubg-saNb0WiCnt6bFYewGIclYWmbzMI371dKweB5j9_yXA46iOEjLIk2ysoz0_tgM3cM--RCKv9Ozfn1TH6whnZy5OkA9FYZIE-yILwGWo9TDTAREQFOGLo8ZPj5Md39gaZoRAHdqOR1WPuMbESwXh0foD2vMMNPDa5j4EN6aQPjm_YD1bgu0jiM90LXs7bt4BmQJCt0PkHfr3kb9zoHer011KSCunwOn7Co7QRPb_7XCErB8nyIxaPDQpRhAYrQHK3Yt9004KZKlUSjdZsMVEkuzrzfEYfmksIK6DeyoRSvd2Um_M_IdbvubsW-OWhTw3yE8uHhEq2Acv6WozA4WlR_1qAPVhEnauX0qN4EyKNMrq0ZWFe4NIGCyLG1YhjWaWcH96x__tAu4jfgCd-u9mgOGGULINRIAXQyrfT3Krz_abRWOXbp2407gdRDhv2bXC5BRb2pTxTe7mOk4ff3BPzcexHyDf_4NEQaZ6g)
