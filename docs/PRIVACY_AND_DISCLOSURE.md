[//]: # (ob:be94d633)
# Privacy Boundaries for Portable Artifacts

[//]: # (ob:9db57e7e)
> 状态：V1 产品边界决议稿
>
> 日期：2026-07-22
>
> 范围：artifact policy、ledger admission、capsule 可见性、停止 portable、人工 drift、correction/redaction 与最小 edge cases。
>
> 不在范围：细粒度 ACL、在线密钥服务、多 audience publication streams、法务保留政策和实时协作。

[//]: # (ob:38c20796)
## 结论先行

[//]: # (ob:552f8a90)
Proofpress 的隐私模型不围绕 “share” 建立。用户继续通过 Slack、邮件、Drive 或其他工具发送文件；Proofpress 不要求每次 handoff 前执行一次 publication，也不假装知道文件是否已经被复制或转发。

[//]: # (ob:7407f209)
V1 只需要五条规则：

[//]: # (ob:ee94d49a)
1. **Declare portable once**：portable 是 artifact 的 sticky policy，不是每次分享的开关。
2. **Record selectively**：只记录 accepted versions 与 consequential decisions，不记录完整 conversation。
3. **Raw holder can inspect**：拿到 raw artifact 的人可能读取 capsule；hidden 不等于 confidential。
4. **Stop prospectively**：关闭 portable 只影响当前和未来，不能召回旧副本。
5. **Never hide gaps**：未捕获或无法归因的变化显示为 drift / unknown，不猜测 provenance。

[//]: # (ob:c9d68c4f)
> **Append-only begins at admission. It does not mean capture everything forever.**

[//]: # (ob:6a6c293a)
## 1. 正确的心智模型

[//]: # (ob:5051a788)
旧模型过度围绕 publication 构建：

[//]: # (ob:d411f78c)
```text
local journal → share preview → disclosure projection → disclosure stream → shared copy
```

[//]: # (ob:d3c3fb06)
V1 采用 artifact policy：

[//]: # (ob:76e10073)
```text
                  make local
PORTABLE  ─────────────────────→  LOCAL
   ▲                                │
   │ explicit enable                │ ignore
   │                                ▼
   └────────────────────────────  IGNORED
```

[//]: # (ob:2f0cb618)
这些状态回答“历史在哪里”，而不是“谁现在有权限”：

[//]: # (ob:61f99e53)
| Policy | Ledger 行为 | 文件行为 |
|---|---|---|
| `ignored` | 不捕获未来变化 | 普通 artifact |
| `local` | 历史留在 Git/local/backend | raw file 不携带 portable capsule |
| `portable` | admitted events 进入同一 lineage | raw file 携带安全 capsule |

[//]: # (ob:595556d3)
安装 Proofpress 不应自动把所有 Markdown 或 static HTML artifact 设为 portable。用户或 agent 第一次明确声明后，policy 被持久化；后续 admitted versions 继承它，不再每轮询问。

[//]: # (ob:ae4bcddd)
## 2. Ledger admission boundary

[//]: # (ob:092c1fa1)
Working body 可以包含 scratch，也可以领先于 ledger head。并非所有写入文件或出现在 session 中的内容都自动获得 append-only 语义。

[//]: # (ob:ab8d506b)
### 2.1 默认进入 ledger

[//]: # (ob:f84efabd)
- 用户确认保留或任务完成所形成的 artifact version；
- 从 parent 到新 version 的 computed semantic changes；
- 作者提交的 change claims 与验证结果；
- requested / produced / edited / recorded actors 及 attribution basis；
- 精炼、artifact-facing 的 why；
- 未来 agent 不应重走的 consequential rejection；
- correction、supersession 和 detected manual drift。

[//]: # (ob:78e5757c)
### 2.2 默认不进入 ledger

[//]: # (ob:0766d40e)
- raw prompts 与完整 session transcript；
- chain-of-thought、私密推理和 tool calls；
- 每次 save 或每个中间 token state；
- casual brainstorm 和未展开选项；
- Slack、会议或语音的逐字稿；
- source payload、secret、credential 和本地绝对路径；
- 用户明确标记为 private/local-only 的 context。

[//]: # (ob:3771c1c0)
### 2.3 Consequential rejection 判据

[//]: # (ob:1c3e3dcd)
只有同时满足下列条件的否决才应记录：

[//]: # (ob:31da1e3a)
1. 这个方向被认真考虑过；
2. 它因一个可以表达的理由被放弃；
3. 后继者重提它会浪费工作或破坏已达成共识。

[//]: # (ob:af2b57ac)
记录的是一句精炼的 rejected rationale，不是讨论逐字稿。

[//]: # (ob:886e450e)
> **Record the decision, not the conversation.**

[//]: # (ob:ee2856b9)
## 3. 核心不变量

[//]: # (ob:e2605fb1)
1. **Sticky portable**：portable 的后续 admitted version 默认更新 capsule。
2. **No per-share ceremony**：普通文件 handoff 不触发新的 permission workflow。
3. **One raw artifact, one holder boundary**：能读取 raw file 的人被视为能读取 capsule。
4. **Hidden is not confidential**：渲染不可见不等于加密或 ACL。
5. **Selective admission**：raw conversation、scratch 和 private context 默认不入账。
6. **No silent rewrite**：已 admitted event 的错误通过后续事件表达。
7. **No offline recall**：已分发的明文副本无法远程撤回。
8. **Deleted body is not deleted history**：旧版本进入 capsule 后，从当前正文删除不保证从 history 消失。
9. **Unknown stays unknown**：无法证明的 actor、时间或 why 不得补猜。
10. **Gaps stay visible**：body/capsule mismatch、missing event 和 stripped metadata 必须明确降级。
11. **Private interval stays private**：重新开启 portable 不得自动导出 local-only 期间的中间事件或 payload。
12. **Precise trust labels**：computed、verified、attested、self-asserted、unknown、redacted 必须可区分。
13. **Portable merge unions only disclosure**：多人合并只能联合输入 capsule

[//]: # (ob:58a799c4)
    已公开的记录，不得读取或复制参与者本地 ref 中的 private interval。

[//]: # (ob:a092554e)
## 4. Capsule 的可见性与内容

[//]: # (ob:aeff8148)
Capsule 是 lineage 的 self-contained portable representation，不是权限系统。持有 raw artifact 的人可以用文本工具或 Proofpress-aware agent 读取它。

[//]: # (ob:d7ab5925)
### 4.1 Capsule 默认可以包含

[//]: # (ob:9efa1c70)
- artifact ID、policy、protocol version 和 current head；
- current body digest 与 event parent chain；
- admitted versions 的安全 checkpoint/delta；
- semantic changes；
- claims 与 verification result；
- actors、timestamps 和 attribution basis；
- admitted why 与 consequential rejections；
- correction、supersession、redaction 和 drift 状态。

[//]: # (ob:2df8ee5c)
### 4.3 多人 portable merge

[//]: # (ob:1b38d216)
同一 artifact 的并行 copy 可以各自公开不同的 capsule 分支。合并时，
Proofpress 验证共同祖先，只联合调用者明确提供的 raw files 中已经披露的
records，并生成引用各公开 head 的多-parent event。本地
`refs/proofpress/ledger` 是更完整的记录，但不是 portable merge 的隐式输入。

[//]: # (ob:b0960269)
因此，参与者没有提交的草稿、local-only actors/reasons、被清除的 private
interval 和其他仓库文件不会因为合并自动泄露。如果某个事实需要进入合并
记录，必须由调用者通过正式 merge 的 actors、claims、why 或 rejection
字段明确 admission。

[//]: # (ob:49aae806)
### 4.2 Capsule 默认不得包含

[//]: # (ob:e924a924)
- raw transcript、完整 prompt 或 tool trace；
- private/local-only event IDs 和 omitted-event counts；
- 本地路径、environment secrets、tokens 或 encryption keys；
- 没有明确 admission 的 source content；
- 为了“完整”而自动保存的每个中间正文。

[//]: # (ob:f0f6e462)
### 4.3 删除内容的风险

[//]: # (ob:f8360c02)
Portable history 可能包含旧 checkpoint、delta 或 deleted blocks。因此：

[//]: # (ob:a57d5e5c)
> **Deleting text from the current body does not prove it is absent from the capsule.**

[//]: # (ob:507eb82f)
如果一段内容不应该被 raw artifact holder 看到，就不应让包含它的 version 进入 portable lineage。把它放进 capsule 后再从可见正文删除，不是隐私控制。

[//]: # (ob:483804ed)
## 5. 普通 handoff，不是 share 状态机

[//]: # (ob:49dd8fc0)
用户把 portable artifact 拖进 Slack 或发送邮件时，Proofpress 不创建 `disclosure_event`，也不要求选择 audience。文件只是按照当前内容被复制。

[//]: # (ob:886e00f6)
Proofpress 不能可靠知道：

[//]: # (ob:184d2482)
- 谁真正点击了发送；
- 文件是否被打开；
- 收件人是否保存、复制或转发；
- 某个本地副本是否已经离开设备。

[//]: # (ob:abd89abd)
因此协议不设置 `disclosed_by`、`sent_by` 或 per-audience stream，也不使用 “unshare everywhere” 等无法兑现的语言。

[//]: # (ob:97f6f122)
## 6. Portable lifecycle

[//]: # (ob:24a6662e)
### 6.1 Enable portable

[//]: # (ob:2d7504b2)
第一次 enable 是一次明确的 artifact-level 选择。系统应说明：未来 admitted history 会随 raw file 携带，且 holder 可能读到旧版本中后来被删除的内容。

[//]: # (ob:99efd910)
Enable 后无需在每个版本或每次发送时重复确认。

[//]: # (ob:81f914b1)
### 6.2 Continue portable

[//]: # (ob:7e55157e)
当 agent 完成用户要求保留的修改，或用户明确确认当前结果时：

[//]: # (ob:cdb74d1f)
1. 计算 parent → current body 的 semantic changes；
2. 接收 actors、claims、why 和必要的 rejection；
3. 核对 claims；
4. append version event；
5. 原子刷新 capsule。

[//]: # (ob:645c4ae1)
Casual discussion 和未被采用的临时状态不会因为发生在 portable artifact 周围就自动进入 capsule。

[//]: # (ob:58cac2dd)
### 6.3 Make local

[//]: # (ob:2c9d0822)
`make local` 表示：

[//]: # (ob:f3548215)
- 当前工作 artifact 不再携带 portable capsule，或从下一次 materialization 起移除它；
- 后续 admitted events 只进入 local ledger；
- stable anchors 可以保留；
- 已经分发的 portable copy 不变；
- 本地 ledger 不因关闭 portable 自动删除。

[//]: # (ob:8c9204c8)
这不是 recall，也不是抹除过去。

[//]: # (ob:697c7f40)
### 6.4 Clean copy

[//]: # (ob:b454588d)
用户可以从 portable artifact 生成无 capsule 的普通副本。Clean copy：

[//]: # (ob:859b076c)
- 只包含当前可见正文；
- 不声称携带完整 provenance；
- 不修改源 artifact 或 local ledger；
- 不会让过去分发的 portable copies 消失。

[//]: # (ob:3e4ed2f7)
### 6.5 Re-enable portable

[//]: # (ob:1b4a1e02)
重新开启是少见、明确的 transition。V1 必须保证：

[//]: # (ob:14bc1711)
- local-only interval 的 event IDs、版本、actors、why 和 omitted counts 不会自动进入 capsule；
- 当前正文可以作为新的安全 checkpoint；
- 若需要延续旧 portable head，只能表达被允许披露的净变化，不能泄漏中间 private graph；
- 无法安全延续时，应开始新的 portable lineage/derived artifact，而不是伪装成完整连续历史。

[//]: # (ob:ff98d967)
具体 continuation encoding 在 implementation spec 中冻结，但 privacy invariant 不变：**private interval stays private**。

[//]: # (ob:a74d9489)
## 7. 人工编辑与归因

[//]: # (ob:6761d19f)
> **A document can detect that it was changed. It cannot know who changed it, exactly when, or why.**

[//]: # (ob:b0624cf8)
如果 body 与 capsule head 不匹配，Proofpress 可以确定：

[//]: # (ob:a1e83e45)
- 当前正文发生了未记录变化；
- 哪些 blocks added / removed / modified / moved；
- 当前工具第一次观察到 mismatch 的时间。

[//]: # (ob:669c59c4)
它不能仅凭文件知道：

[//]: # (ob:cbc60133)
- 谁完成修改；
- 修改实际发生时间；
- 修改原因；
- 修改是否来自同事反馈、用户本人或另一个 agent。

[//]: # (ob:02196bad)
因此检测事件应类似：

[//]: # (ob:9d551f6b)
```text
event: unrecorded_edit_detected
what: computed semantic changes
edited_by: unknown
authored_at: unknown
observed_at: attested
why: unknown
```

[//]: # (ob:8261234d)
Actor roles 至少区分：

[//]: # (ob:f1daa663)
```text
requested_by
produced_by
edited_by
recorded_by
```

[//]: # (ob:618dd688)
每个 actor 的 attribution basis 是：

[//]: # (ob:86c9996d)
```text
signed | environment_attested | harness_attested | self_asserted | unknown
```

[//]: # (ob:12d61fe3)
当前登录用户、文件 owner 或运行 hook 的 agent 都不能自动等同于 `edited_by`。

[//]: # (ob:4d62bb79)
## 8. Correction、supersession 与 redaction

[//]: # (ob:bfc61b9c)
### 8.1 Correction

[//]: # (ob:c2d65249)
Actor、时间或 change account 写错时，append correction 指向原 event。默认视图采用更正后的解释，但原记录仍可见。

[//]: # (ob:b46a45ef)
### 8.2 Supersession

[//]: # (ob:2218bf81)
结论或正文后来改变时，创建新 version 并声明 supersedes。旧版本仍是历史事实，但不再是 current head。

[//]: # (ob:6ecc8d68)
### 8.3 Redaction

[//]: # (ob:3202fe48)
敏感 payload 已进入 portable history 时，未来 capsule 可以追加 redaction 状态并移除相应明文，但必须明确：

[//]: # (ob:7ccd86ac)
- 旧副本可能仍包含原文；
- 移除 payload 后，部分历史只能 partial verification；
- 不能用普通 hash 冒充安全删除，尤其是姓名、短结论、API key 等低熵内容；
- V1 不承诺 crypto-shredding 或远程删除。

[//]: # (ob:4779c987)
如果连事件存在本身都不能披露，安全选择是生成新的 sanitized/derived lineage，并明确它不是旧历史的完整连续投影。

[//]: # (ob:0d3174f5)
## 9. V1 edge cases

[//]: # (ob:a24edc0a)
| 情况 | 行为 |
|---|---|
| v1 portable，形成 accepted v2 | v2 自动 append 并刷新 capsule |
| 讨论 casual branch | 不记录 |
| 明确否决未来不应重走的方向 | 记录精炼 rejected rationale |
| 用户直接在 IDE 修改 | 计算 drift；actor/time/why 未知则保持 unknown |
| 用户把 artifact 改为 local | 停止未来 embedding；旧副本不变 |
| local 后重新 portable | 不导出 private interval；安全 checkpoint 或新 lineage |
| 收件人修改正文但不更新 capsule | body mismatch，标记 unrecorded edits |
| 收件人修改 capsule | chain/digest verification 失败，标记 tampered |
| 收件人只复制渲染正文 | capsule 丢失，降级为普通 artifact |
| 当前正文删除了旧敏感内容 | 检查 capsule；不能假设 history 中也已删除 |
| 用户生成 clean copy | 无 capsule，不声称 provenance，不影响源 ledger |
| 已分发副本需要撤回 | 明确无法保证 recall；只能发送 replacement |

[//]: # (ob:2c249df0)
## 10. V1 明确不做

[//]: # (ob:14d8b083)
- 每次文件发送前的 share UI；
- disclosure streams 与 audience labels；
- 一份离线文件内的 per-user/per-field ACL；
- 多 audience 自动 projection；
- 在线密钥吊销；
- 已分发明文文件的远程删除；
- 自动判断 Slack、会议或口头内容的敏感等级；
- 默认打包完整 session transcript；
- 完整签名和组织身份体系；
- 对所有 retention/privacy 法规作统一承诺。

[//]: # (ob:0444a90a)
## 11. Release acceptance tests

[//]: # (ob:3208f8df)
Portable V1 发布前至少通过：

[//]: # (ob:ec5f7bca)
1. v1 enable portable 后，accepted v2 无重复 permission prompt 地更新 capsule；
2. casual branch 不产生 event，consequential rejection 产生一条精炼 event；
3. capsule 不包含 raw transcript、tool trace、local path 或 secrets；
4. raw holder 可以 inspect capsule，产品不把 hidden 描述成 confidential；
5. 修改正文但不更新 capsule时，verify 报 body mismatch；
6. 修改 capsule 时，verify 报 tampered；
7. manual drift 不被自动归因给当前用户或 agent；
8. make local 后，未来版本不再嵌入 capsule；
9. re-enable portable 不泄漏 local-only event IDs、payload 或 omitted counts；
10. clean copy 不携带 capsule，也不修改源 ledger；
11. metadata stripping 后降级为普通 artifact，不伪称仍有 provenance；
12. correction/redaction 不声称修改或召回旧分发副本。

[//]: # (ob:9e0d89d9)
## 12. 最小发布承诺

[//]: # (ob:1501efd4)
> **Proofpress can make an artifact carry a checkable record of its admitted changes and attributed decision context.**

[//]: # (ob:f9cbd5f9)
它不承诺：

[//]: # (ob:aae706e7)
- 记录所有发生过的变化；
- 所有 provenance 都有强身份认证；
- why 可以被证明为真；
- hidden metadata 等于保密；
- 已分享内容可以召回；
- 一个离线文件可以对不同持有人实施不同权限。

[//]: # (ob:3cb7a253)
最终产品心智是：

[//]: # (ob:bb79d355)
```text
Choose once whether the artifact is portable.
Record decisions, not conversations.
Let admitted history travel with the work.
Make gaps and corrections visible.
Never pretend a distributed file can be recalled.
```

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzYxOGFhNGZkODJjZDY5ZDA4NDE3MjE3OCIsInBvbGljeSI6InBvcnRhYmxlIiwicG9ydGFibGVfaGVhZCI6IjQzMDE4YWFjIiwicG9ydGFibGVfaGVhZF9ldmVudCI6InBwZV8xYmRmYTg0NTEyMTY1NzdmN2M3NjQ2ZjQiLCJwb3J0YWJsZV9saW5lYWdlX2lkIjoicHBsXzMyZjFlYzhkYTRhYTUzMGY2N2E0MWZmYyIsInByb29mcHJlc3MiOjF9)
[//]: # (proofpress:discovery:Verifiable revision history by Proofpress | https://github.com/chenmingtang830/proofpress)
[//]: # (proofpress:capsule:eNrVfWlzFFeW9l_JYL75RZD7woeO8NgdPY7wdDvs7n7jjaEDcrmJapCqNFUlaE27IySDFkAbRoABsZlFNLYWG4xBJaH_4q6s5VP_hTnnbplViCxt0O-4sbsqK_Pem-eee_bz8JdDfrlaiP2weqIQHTp2aGjohK25vm_GkauHke1Fqmtqjq457qHDh4JSNHIiKpwilSrcW-n3dcs-ZmmqEYRerMNjRI80J4o8L3YD0_JtKzZC3dRMVVcj1Y9IHGiW6dtBoBuxHRuWExMTxo0KlbB0hpRHDh37C36pnqj6p2CGIvlzFX4e8AMyAF__SMqFuOAHA0QpkzOFSqFUVPrh7lJ5RAlGlM_KpVI8VCaVCjwz5Ien_VMEX6njcrn0nwRedriMA_ZXq0OVY0ePnipU-4eDI2Fp8GjYT4qDheKpql885Rrq0Y6ny-S_hgvw-cRwhZRPhKVihRSBEtXyMPnr4UP9xEcSmoaKFAwPsSsnyBl6E5CWnNCCKPZd09J0zbYcJ3ZCxzbtGGkwVCpX8dVODBSKBFYu9mPghKHHGgndyDd93zLU2HZ8U4vjkL0OX92J0B-qDA_AC-u4zrBUjiqHjv3HXw7x6f9yCPa4VK7gJ_YziU4EQPD_OBSWIvLnQ3-CNxC8ABNHpbBy9LPPP_njhx_9vxMf_vbjEx9_8sVHn_7uiz98_usjg9Ghw7viG79aLReC4Sps2InArxQqSHu_XMR1w2_AToQOOVztL5VxhacLRRy1MgK_DMIvRX8Qt5Kt9PChCjwIYx06VhweGIB1h_2wW4S9bzBQCk_DvQHxzMg2DLgdNqqKnHTs0Gflwhk_HFH-tTRcjPxygVSUuFRWPuO0Vz4UBDgsluBHEV3bEHIcOQtX_kXZ6SjIMtWRIVw5cgJw1aG_Hk5X6EWB5RCHHPgKf6U0L75ojI79Y-PmHzWlvr6UXBlrvX7VvDqdTDxrraw0n2wdL_4K_iiN648ai3fhPl3V7T7V6dN1_ktr-lxy6zn8IvZZGSoNFMKRv4-ODdDp-IsN-WW_460MN9RVx7M73qpZu9JaWU_Gp1r3p3Np-y9K16059LMsPXZ9T93TTKmwUJo3z7dvzjeXxhpP7id3LtVfzsCbN2tXlV9GF0HGlckvo7eVpLbe_O7S30e_ai48aUz93KwtNWvL7dGbra1J5YsBEDZAmPZXK_XaC_jwMWwiURpT15LxF_XateTnR8n4z8nc5fboWA7lHFN1Yl319vQ-sNHJ3NP24mjr8Vh9faFx-35r6XwydQN2MGdKgofE9Pw9TakdUT744GMSDgCJFCG-lFIxJB98ANPKK41vVhXJRUBspVIthKdH4JF0ZQMgxjtWFnqR7YZmvKeV_QoW9iHI22LUVyoOgHIgpwrFiuJXFT8aLFDZcUT5pKpEJThexVJVGSR-UQEJWh0u51DL9u1Q94xOagEVGssPmvdX4M2SrXONG-uMjXqwec5jeSyvWprvuO6-V9C4vsRuAv5N1h9zhh8aDuCM-yinlcad88Dz-ewTmZoWO2647-WcPHkSnz5ehIH9AeU_S8PlIvz_LxNfK_QEKvxWegWthYFSZZhepuq8kOEk1BGdizRCIw5Ue9-LhCPWnpyE8690ycR8Ijk20VTVMQ6OSMob_wz6p4lCaXe8-NnvPv_9h__66a8V5ZeF0Z38yaGdHqthAIp932tvbd2or99iaim5dae5vADCNZmdSOZ-TBafJFeetienQcz-Y2O6NToNEhhkBtzQWhtrzq7BDY3FC43b59o35uk9edS2tdjziLV_an8JOhc3V_lS-ZREp0hZAaFTf7kO3xvXJkHOi6_Hi1_29fXJf-GrcrJwqlgqk-gk3IwvM3M1XTGViZ2H2rMsy472v-Rk5ULrwXjGDsbJk_WF1uTT5OKTxsWLjQujQEnl3_3y6ah0togaCoQxnPdQ-bff__unKV-3Vl7ju4EIzyG1T8wgjKKoY936EUEuKWqVgNkyIz1EYo9Hc8Si6umhFvvagazk_5bK8NspBZ0d0Kmr9dqjZHo8mf9OqYRlvxr2A5PWX91lv7S_nQB1VF-fVQbYXLg8sBKSVy_at-8weicTN5LxR4xp0CaYXGdMrVRIHnUDN7JUO-h6J5BBtW9aKw9bW7dgUD5rPmGRsm97LIeosWuS2A-i_S6gT-Em0_0VeKy-dbt59QaQoV6rJRfvJyvTjal5oFOy-S18QOtAMiE4hLhp_9i4dbzYp9RrswoQCZwZJZlaa1xbE79TkyLHknBcYjmWE3a9h87fA47ILmmZ82Qejzq2HZkqOYBl9Cll_yzqvsGhKp7xWaTi1ecKd4uUatkvAq8WhqqcduAfFYp9pbgP_KvhU_1VMFHB3E1WJxqzT3IoZziOFmqh2rVkQ_kIPd__Goa9KICWLhOmg4uwMQ8bMyu9KbiDEXIoqYUGMaIwOsBlgemMB3V-unH9RaN2v_XiWf3lpWTqOpjRcGhRBM8_Bt-pcYGK05W1ZPNqvhoytMjXSJepuL81gkZALfryaePaq2T-cuvb74Btmot3W6PnWjcugx1HNxukXrICrtu9-stRuJdJqdb9J63Xr-E1mvMTzYUf4NHGwutk4xx9woAn5mfBoWmNjrcnZxpz8zBAfeNm46enreevwHepby7CeW3ee57cnkt-_hFGgpOajP_QWp0ASZfDP36sg4frhwdIBEZ7eBMwEOANk7lHzR9fN7_aQBnAxiERnA4czR8gKKmpLdFaeQKOQ3t0Plm-Dt5vx7Lf2DvXtYlpvXFS97NsdEg-p1EXpdpPlIiENHp1mDofeAUmQnFGF37kgw9yXTbdteyg00uEPWzcewl2Air8uW_ak3M9dO22D-ScOaLbqhUH2j5mpe7iF8L1Y75hp6NIzxlw4jLV2FXcSiHjmZBs3HqOgj_0c5jOcn3H80JzHytFixoYPRn_PtkYhUWJA4_MlLy-3lqtJXPXUJM_nEmmXiRzX4EIhsPTWPw-WVwDvohBJi8jRw5hMKdKlAKso3zGH8jnOx_MGMsyO_nOPKJ8xCJ7lDxzq62lscboEgr9ifFk5VWPfd7B4zm77pM4djXTPbAViQcxJMDjnCwiQAbiPpwC9BTsuuSIMkE7Fg4cPRhsB_L8UccPLCBi13o1uWDGRlmjrpey6vl0XoAP7CctdNQDWk5fahp98jGocBmQA0ugWgpLA_K0JF9PK-FwmRpLuDBhBsClnJOjR7FLiBV2LddQkoc36-vr6a4MkvIp0ptwb38wT7kHhhvpmr3_RYA2Bw3REXkCqxy8NhC2Q9Kynz-P3hE96Xi656eRHXksHQT7RGNhFc35-Sl4FowDYEHwsFMHq_10urWaF9QLVM9Wdds7gPe5da-x_BAWkAqcH--jYzw3X19_iGJq5gLVbWM0EMAiXyzof7RM_AooL_gNdf_L8faNhxn5dLzIBVTOe5ie7xNX7d4XvYuXmYTc6dHq8XSePvJ004d_D2g5zKJO7WYgFLepmZVNPeVqCY4Y3BMSfp44-Y5KeuccrliNwaqw9Tf5YOoe7AYTnRiJfjDbvvG3HR2utzyY69IZthqqB7AImY8Q-TfUA-c2GaUb15fA5SDh6aESMBbQMiIDVZ_SED4R1Ot0RRU8WZyr84xp33Iia1vBtNtl_4pGrGEJ6ODjQEoM-8ssMC4vqdsvA8Ow_WdAf1eVQiVngZbqkMDV4_0vMHn8VePOIsitxspP7DEewll9BCeXcqkUaP2lgYiUleYieCprKBfWfuA3r_yNbQQY8njMhVrgDiYTOXln3TVc1SSdDpYFJtSNlfboTaXfL0alOJbGNQ_RsuBeY3G9h0myq4FymNn0osiNu7zTg1klC1g0Ll5MxbOkeuPSNaAjy_nQFA9N67DUD1MQXfG3qVtJbV05yaLWPdwOFaTEO3ifzhXhOZ1bbd--17z7qD12Jf_saa4Z6aarv4NV9SkY3128i3HOr14lk7X6-gSjJpevPGT2zSp436i3LlwBLS1-W3gBv4EGZT_Xt24ny9-g2KY2OexLa_N7GEzcfXceHWdqoCcXVuEDewys_GZtrvm4BgO3Vl4nDyd7eLRB5HrdMbGDoQYThMnMXGtlBTdp5XVzc0WwTYUm60_C-51Eaxg_U3E6RMp9_nBUIMWQKJUqqPlBFp2EEeqbW5iryNlbz4ntWNM799Y-kiabBwoxCUfCgR7GnvK2Z3JOL6hv27Z10jW3pvy6SIcRB6-XJtz-kbyJI8dSzUDfz8TN779HEf39fYUURYqTXWh8M8ti9lJg9A2QM2RAaY9eaFz6G-aPn9WatbtUpD-Hu-H0NRafNm4_Sn1eplLz9g0ci8jT1P28Ar8V_O3G9XvtxVFMsqzOwSFpXpjC4zF1Db7CC7EDCYKtPTkDZ4sFcXvET7TY08yuWIGNthl8KxSHd7O52z-Us70OsSzNcsj-Jk82ryjgm2KsmQaomUJoPR5r_PAVi2DDFte3VhoLr-C8YXSMaQy2-5RGMERyYaZZuwL6nOqFPCkbRoFjRlq8v1VjhHDlfnPlugiUY7a0w65hvvagX8SUD6-aEWHDxuwjEKrcY8iRgbZphaZP9rm9H_mVYX-A5nKHK8JphZMAcp4lWZHAL58D5Zj0RIG2cZPGNdeBJ5sLdzGD8qZ6Ti4_SW49B1OIJb1AVefZbW7oh3pXBssGu-3fZT61N4t23Z0nekIsi3pD3u50upNplvek0rr_pPmwR3o-NizQ3Jq1x_n6FMbDLASckhiNmomZxvx68vJxugPcZ2bHoV6brb-8xGXkIPhI5YI_UPhvVlmQw1tu6OmqGbp7XDGNj1PFWyZw64DUhXCpcfEVmOJY7jBby5dftueETmx2i1dT-WiAlomUhkZ6c0XX3TlcEZiWablutMfpmORh0QyaI3vjSMBZwRzb9XsyroHxc2qxMFsIyJHOlc9SruUFqmOHe1xsHxYpcd-E8RYLHy4_AFtPJPqAvR6sNZfWGIelfvgZULZF6XyjQKACuLE-n7HOwShiNSR5zrhBwLvRY6frLSzlc9JHdmt_vOWp3BiX6WtE1fc5PSZrrq2B5ZrMr6I5u3YZSAkmYmqD0IBGAQ8dbDFWiG2Nt-_XQIG1Vsd6mP1mEGqOpu1ziX1KJhYlouBUC9GyVOWTjzEmxUwO-MB0D3w42z9Cg5glbhKFeaVicey5kWfvdzeT8Z_roPZDpsWYqAK7uoTbp6CyKQwODZBBEYxWKkMkxEB_MgEG3RUUNZsTLCQUjuQFM0DRe6bbGRB0jijgyoCgbW5ca72-jLH0za9B2fWwu3Mey2E_27G1SPPifa-AltkpUSkcRqqAdCkqEamSEFNafhWjJmf9CjczIlpwB7dgVOV0sZQbMrV1M4zdfa-PBVOY5QMPSPGHRKFiZvpVe3ym02NnghTOT7Jys0dUSiMuCBJr38sUepZJQWbcgCuMxhBNPCVz3yTT17jYS648ra_f4vEzhQ6mHAV1NwjiET8NAr_GBf7xTJ4ZZ3uh1Z0n2xOVV86xoEK9Np5MLjOnfSehhTAIbVXrqtDeGwFba2PMUBc2OVMR9Euycqd9Y5yRFf2Y6887f569C8N3XGKxAfDJ0Iacn66vX0rmZtqPp1BUMTt_8XuMPGDw5zHLszNvIT94oOqaZwd-tH-K01BB48Fo46dLsDggN7iTzR9q9Y2NfIp7EThHcVdN0V5WIEsRqRg_pgwXZU8BiQrVE0wMkOh48SxIgmMgVAeHhlGQU-cjp-DQ1W1NN8z90-hDVCVKuTRAKkpr8hkox2R6PZma6GExa5Hv27ZxcATClhHa33AiGDleBCsmGg75F6QU_5jpyDhehGdzKGRrbhTZ7v6lI3P3mb9HVXKmS0OhXRoY1uhhDtqh53l2dHD0qhROYQb4S1C9ZwrlUhE1i-wRgcvdbSNwqZJDLU2PbC0m-99Q7s7fqGH5CRUCaGlRWaeUzhZJGU3P1tY85hf7S6XTjKI0hNAG0UgFJHNJm8sXqFCZVU5KDjiZ75GYka0HgdNpM7hHwOMG3z5k9t1YZXiIlEUJGKq7Mol8-mMPK2JXA-U5MnFoa4EXdq1Sy4zey5p-4-6c6cBxty3d9PY4HRUQf2ehrevP0W9ghgociLA0jJGfiRvthRsspO_TZgIQY2JkpTE9mcxfBuXBLFnYP14WuTSRZ9qYtm9aJO5as658kaF5byK9cX9e0EHX3CB2tT1PyZouMCDI7JP5WdCMqDjnvmHEYRmObEVm8uoFuHDghyiclyKCub7G9SVm6tdr6JGz8m_Urit3mPnMIwvgv_OoVZ6XTsLQBUHY9V4GWP07YnukY-fNOUQ0dFWPibnHyRpX5xrn7ypD_shACSxPrKHLZuIyWVRGUB4QllUIrIZvazO5eC89i3mBfScMI9f2w70ttw-WscQiAyyrC9vFffbZu6mf3lyqtW88TN9qfhaW3j73BJQsL-yfewoPYyyS1sudod2bIa_koUPkGEum43ih5zp7ewVm-be27nDzaPkb2kTwfWv9OymNGxe_ay_-iPy7ciEZf8IC9MB7PFxybY0GS_0i-M__TaKjEcGmrkiULeFzr14wV5tZwBhjArrRV8_ZGzUyNMeMO90G74gC7jkW_sKuw5nsIbG3uT2viks3SRSq_p5n_FJpnBtPJn4CXbtN0wM2PJzRJC8jYWgtNwpSMkSL-HR4Ev7D9J_i5zVD6CGI9CjuDL5pKl0tozYKibGbvdqrtn0iLyZjRm6gusZ-5oWDQ3MmzCxgmRM0GpCPaCLwD59wxs-0MLGsHS3jVmQqj3Y8Y2Q-z50wTdP3urZV047ACRkgsKWc_hgyU9BW6sVUPR7Nl45u7EbxgaxEJhJpR-Pl5OU5ICGz4Fm7ZY-OxtCKnSA8GKrAY8DZXTEkLumy3I0pNJoew4Ss6DXhlUPJ4lrj1vOcffSIGrle1GnHaJiQWRxN1uYYDRoXtlqrvSor3vpQHt9bqkbiyNzn7BgKykRRMBREsxXw_zI2G_plUHE-Kw3i5Z3o9uT5Y14YRFa8X9pwAU3v6xHU8Ymj2sTZ54R9Cgvd8AYgGnsA1qX1splgDu_HSmPb6CvgAxvroKnqtU00KFdFOQQNijJb4Nvv4DKIJZDFTezfpr_3F6IoL-gdBo6vd3fG7frV4O5mbYo1lfPGtF5eIroukWFZ-5xZ-ogfgYNVYZ3GQBRS7QfvC0u4JKeB6ypO65Hjxc-7uIw5iX86LKARDnGz9UQIkpghEdBfBLJBLmxDsVSl75yWP7Cq5rT-jYJRUGOWwhWIb4hW8CeEfcAi3swIWSiIzCAUZGKPKBGVUlw9EcPJJ-WhcoGDUVQC7VgQmjFYBsRQwY13A9sD2QmXYsczfN0DOyXUsSiJeFhnFZrwP9DOrme5jq8GmoaUwvZBCirB9uuYpmp_BUojwoPEFLB_rzrHTOOY7vwfVT2mom7nJM_CZfw1c_Uv7wyKggVOKVJEv1_pxySwQ_TQMawwVHFD6RgZ8AjOrvtGfeCzaRYYGk5kByGRs2WAIPhs7x7BoaMvEi5lnA1Wz4-1VGOLjeVv5VGCKyxsokRgyWNdZ-oPH039EjBk2LnOWJfg_PFVoRW1-ESurVmbaP74dbL-WPnwo09xysUnzfWtZHWi_TW810xy8T6t6bqZmkbZHnVuO6EX_-wq3MubCxe2msvXkq_BsL8DDlUyM1ffXNw-wMI3xTcNHejvgOj3xaZkcCwEC-wEnIKPGKihr_qxbgd6JEbM4FVIsI9_DggFM1BBbXQVBtL6FmbDilo2BRMTF5ao3U-z-Rn6y_R6MjbZejDOYv7Zoj1WXgfaqqsqL3czHIMEcBwNi1hEkC4DjcFJtzu8Cz60DRvsGXFkq4E8fBkIjLT1ep-4FgwUgBcB8jqqqYn6-ndoAGyMJuPP6IHQj6RtYRUwT-H8nCEDI3QWdJ6pCZFxo5h0ZK5C2NGLJhrKKmxWnjdimfNsaxmd1qDT-mdFATEaa4UipjOrdOrGpa1kaq2z1hirceDs03AA639KCz5uoeFB8ODPNJcvYGATpowLEVsbndJkvV-lIbR16EyZNx1_1r6-nDGv554mmz8kV2Z4hcDXPB7CXw2LV79Pbt2RMQo6gYUT_BbUdhnNIKKcgsWxl4FnZ662Zn_GANb1eygnaKxXmmKNb143H66jU0ulmnJUGS6eLpbO8m6j5vRi46dLGRNt-xwPZ7A4DP3IcILINkPBYBkkEynd9w5PQjDeWB6p9mNWGvQPftu-YVDwvKqHphY4dugZYkkZIJNUtu0OkYSPrlqRAS8Y-kaoSzmXgpTw0feHNiJexApVXzP8UFUtMVUGgIRPtW8kkWL3L0zJpCNEtMrlbWkavthQdb1YAzYgvisXmwKRpEJsN4gifGzdjFRDQ4A1VxIiAzLSTYgDRgt56x-gj_Lp7z768FM65S_XflR6_PPLwlfs1oWvFPLnIXjvQlU422_eqjBMDflEr8GvbfBbF_b7Ytv9UZRPfvPb333-64978EEcAcOCHaqDxSz2KgOqwvfqnaOjCKskVO2AaI7hkUDKghQwha_mYJFPUPRS-c3ELQ7CiuUly7MHeV3jlwp7b7DjsObmN4Uqa686GoB5gzmYL6liigvAJDjB9lWIfExxGYeV5dXUt6vwZhjeJCi8tszgovoMY8PpsNuFLjlxwYwgQUSM0DLlscxAu3DivguMFm6dc6sQH2CJR1mmzsPUNCXDoldMzCjYVTE9Vn81zmISb-m-Buu0tgT-ebJyjjdBT8yAVdPaXGmtftu-vpJrzgWRFZpeZJmhLS3hDHJMqn92D_8iDMbQ18BWJKpOpA7KIMLwGd4nrItInWITOOviaovsLxyH5PV1xc-o_9bqcv3VhVwiRg5IDAK8FKciPwMQI4m4S6gXqVBCNzBiVTUjOXoG_YWP_l5wXDoLRbqr1OHpzUVsfBUtryJnC7Z6gcXQWUMuK7vnz8gSDLDtRAEGfGTJd1o8xYoveOk7MMfFN2shRNKLok1gqaJo74D_IFvhYs72j4jAHm_poMeQHfD25EzrpzX2jtvCSIgm7bem4rEgUhTWgA4v0vp55onnmKSWbcHOWlZkEWn_ZSBxOlhnd8g2fAIwRUw38vU4iNLjl4LdSO45QMya5vwEEoM25GKdt9gd7rpWfOb4sgoXOIbt68_hZlAfVJKKCuKQtSAEZZgI06-DvAUh-eEqOGnt0Qvt-6KSTDjX9Y2brZUV9GNXl9t3n6HTLjBF-J0VMDgxSsGyoriFJCwTGiwBtcj3nM6DvWjN2u1k9VXr59Xk9XnBYZlOksa9SXDlqJTvbjUe4ceFhlPzGYA4umMZrm7R3kIW3EiRfToYYG_APHwiN3LVKNJ13_Ylp2WweoQCPCioHeGBECs2PZ2oJBO7SdF3Up_-fwl4jghJOV7khboOVn6qNlM8HWE4vkM4HL4Q4sE59hxb9QPp0mYQcjIu7T4BboQ2N-0ossF_9j0tjdFIzJvUXtgphI0wz2gna-SYjiWVXAbVJhv7OSCQGmoypoGe35ZouybzQkOCJbtFFgFhBjEvJhNxN5TBS4-Tucu8EiGTWTwLpkw8UDqbRnN-VyQd8ZrDSgmu8PiOMKLoXGn8Rlq6LLaDR2JpAmTNGxGeNILzbyzQU2BRiWyUh73Hyx8bd6_Q7cAgsowHJRfvodwGu5QGeUW45gsR8koNPjoMLqwzaDXGTTSqAgWoDpd9GaSH8Uet54_p-DYneAXeDzRwmZwtg7Jn4aaff-zyBWjsdeFGa3WVhVLZ9rLKEXb46ZgOHxM2B90F3mIkxsSql7nL9CTOYpUUazKmAafW1mLzyaXG1w_BtaMjuUcEDAEiIaA9yikq0BF4ORAjqiia4hpZBuqpHQ_WVEfxOMUboK0x2OOBtpYsLXoxlTz8gc7v4fx_YFEu1IgjFRHz4jPSVdMEIzXk3qiUw0wkx0K6_6g5vUhHxWKJDz74DSyPjqkgQLs4PfiSR8XKYa8HcTdhSLrtYD2xfcDdrYDdBbYxGDik6kd-1edNK0whtm_MNNeX2HT0qH7WhbDEX4fzCJ072yaTOop8-dQmT1Y3wHrPtqo0Fu_Cq9IWRDQeGC_Qhmuh13EFOlsByjoCBsxwpcoLN-i8wpSF12SlT_SjqFullsFA3OdXKqTMvvM9gE8smQJEYO8Ox4kVL7Np6Yn_rAM3BvaP-ml08WnsijEnBZphCDasJKs1tgBfW6-vZPjp7ZrINF1XDwPXd_xY-rUpyBYXnO8ZM0vYNrpqBpYf6E6qLDIwWqmy2BsOlog86lEYhgbo4thMXVgJjcVnOQhsK0wX0EgO6xLHmsnpMQwHbB-Mx04VMBevTSIZaX4HeTSNLfT5Z1HZMDeEbQGYJ7kU1S3fikLLMa1QqvsMrFbGWtwLMpZIgsaxZmu6GWixjI5mwLKky3AAeFcppAv9ayto7oRJG-6EUj-DP7BN4AOYhYeAZC7-KIWzEfb-9n5q6pB21D3CpgO9hIsj292qhUFYmz8IohNf5W3Op1wek7-zb_MkK71cSSlipFtJUx8sAJlrloInGZsxCV3NkFZUBjesgz12hf8lDnToOqHtxqFtOdKHSCHBhA_x_qC9wFTHJx9dS8anKPbWUy49187B0UMJxjy1ufn661vU7OZmVYX2BtIEKKs0hR9Fo0eFVY-yStNkAxsKYLVsqaw7Dd_o4c0-zqOixJxJy-PFkyAvK5m_muQoc9NPouwB85O51h1CmNZWo2Tq3Auedk425pg2yI_kaVZgGDpxDVsqggy8mdibdw9TRh1oltWu164k6zzn3AERQHeVB1WfnQfy41bTqmCGBcPKzln-WISC8ZHjRUk0pnzR5RN7zexDMLWAYCkB03PMTj3vX0VRLI_k8SK4Wo2Vnxi3ZCsv8mSx6sREDeIgMqXeyeCwdRy23UOpiRPtGipxDNuO7NQvStHVOsI3-wZIG0n7frP9vX3sKu27kLEcyussNAKzZdqBFBZSoYITgzoVOjkphuWRISrRTpMROQrjvS6qM73MIjXUjShWZVf5en19ArMv9O1-Gb3dGp1mbMQghtDCz4SVmNmdKzJDFYgZWq5pGfLYZNDgukXmzlHdhH2mqaFn6JHu63oavZVAb6LU5H0AtgkX3g9i1wahHXoy4pTBcMuEDPaKxab4AVpOmScY8-dGFkKL9j17DokzuWqJ3Cbk13tDYEurBVG0X7wI9zYWXiO4WMbHSyZm0MfLwCQwDpH2Iq8aml0CszpfmjgusV0bVDetNWbSJEV6S23l_QK0ibiwrtuqHTmxHjmp9JKYbeKvdHlnUGvoALG_fOukLFRiFU6s1UOWlCH1ecX-U1Sg0xea40u8-IQygCxgyqVv7JlaGNh2oMZeNlDGMd3eLPnaKRSbrIvSbQd2y45Ceaoy6GxSUP-vAVUTYWOXhEAzEA6Okea2JM5ah1lx8PBoIOqHi4ytaWHN2X7Cau2ayxd4vdD45eYshuBaq8utJ6O5PIB4QkR3dZOEMhidQVlLz9guENOE9aUTZCUD6CJd3QyIWkaN7BgSTUR4Y2KY4N0TJ_BSm16ipImD-h4wz8Cr2bjZvjnXnYWnAmhBiNu0Cm1qLW0pBGObdibiYaUSUuZe83fMUYGyphsSU5ZEZPDV-Mu_A7Q0EZYGgez6EVhbtuT-DIBax7buGAxNbGxgm3HkBBGcJpn6S_HRxMl6T1hnQg1pITBXCIrITkvkUvizTL7mgKDMuu1y9B22xuH90iSJyL7ylMLqK-6_04vmEZ6tl1qcKhX6G6hKxI9Ynk-AIB1B_5x8nE8MUBM-SAUpIzKYajKa9L7w0TJBwFxOBRFhewGxYlvz0jigBFDr4NTemGhCqnkhqEsj8H1DHr8MTJqoZdsp8pmw9AzVDVzXsty0-i4DhiZV5bvBN2v99DPrjaX1Mgy1pStjxGuQMJrA8-wMs4q68SKyxHeuGPazqgSK8EUPpBiVKlqZecisFaMgLC3W4U2JahZaXX6vu_CWB8Op8MzlYI14dmAYkWukMcIMclumqG3vYGyC6aI4Vn1XV7XMYUnx2TqYrjfkmjiB4Jk4XuDZjpV2fKQobB2W6bsGVhNLik3b8SJLD9N0bwZrLeXY9waflmVFJlzAqWE7tj3HYUOMTDK9nXls09TswApMx5TucAaPrWNHdw6tJrWp6fjYz6NrWho-lGhrfPB3AZwmO0miyDJjUOp2uoAUS03u40HBomHARGzPNgJdCIoOfCnK0Jvg4q6z1PIbAW7-VOvSIxYfS2ovQHphkCAFLKBR9mmeT6JJUjS8xsdaKy9luDOZHBXtjrx0v_HsfGNjjlfkiEzPqbI_1C_kFDO56YrEtBRjYn0B92vpksiGd3nQsj1fsHK2Vra-8bT1YBxDrfQwtLbuwLiszDSXVR3igk72NM_T5KHMgM0J--kAceOAGc74oEt41RiK75sffDDUI8mZX78Rm6Zha65tWVKCZjDoUpdkd2ByYnQ18ANdD2NHTyuKU3y5bMPDHoHizipn-0viN7j1sEL-DPsLBwdcteJhpVTGdEhu4EcNvAAcJ-IaupoGriXIXEfg56DR4kRwwAo0LTYD14qlyswAyHVZJO8ACY5EHbKAZQulT9da-ipZvYtdPyI5T1UZTfjnmwIB8UHc-qZBZPQ4gywni553CREnrEPHBOJbTkhS7Z9BjcuGPP7_hX8TmsGNwPDXLQf0nyyTTBHhOsIcu4B2E4pP9wzb9LTAS5tjMmhv3T0he4JtyzhaGfCyY6J25HiR_f3tcNWvZq6WggpILX5VlD_gDNlHc5soNM8KbdCgYDHIwG0GKI6_3O4Q34RosB3NM0LiGbp0vzMgcN10OzA0N-GoeHD-rdgixPfShgwJ8Cbap_aB1CaCsa7pxoZBHJtIEZgBb-t-z72gsJGB-ISoZoHvO9tay3F9n8RuqFlyazOYbWmI4v2Dr8mWPi0G31y3SJyGsVM8tlR_7hdGTWbYAxJHdhwGqtSoGWS1jH28E7A0oaYNNQI7mGBDvxSkKX5a9gS9E0i05NZrFrXA4sjlB-gO3zzfWnrQnrzIDCB4iqk4xJqiTk3upoRgzRjgFvp-GmvPYKt1EGknYGlC3xiOGqvE9tRIOoYZ_LSOv4X-nwOIJhpRctokie7YTuyaWiQtjQxWWgdpeuKfpV2egU5CYqtp5j8DiSbE1DuBOeNdca9esJhK89ZL0IisyJKzTqY-sIeOtIPIcfyAaVwWDk2R0qQ18b7Qz5hcwkMhsm2VfjhiXyfj49wBEpm-ZO1hMk5zNktXkvkZNETuLjM2hM8ffvYJprwxY1HfnG1O8LQlnwXxIwT2jUJT5KW-Sj_Ql_onVG5ieeoOwj4ksIgZEh9THFISpjBtHWb0Pw96jTq0qZvXuHg12fyhR-IO2MLUwBgzpYTPoLSlEn5nsGvSsnBNy7Ft003rKjJIbLLX8mCh1ZhQRnHTEZBm_ZCs7D_T91IEO5_2aXKoAXoXJyzrwqBHtKuBibVQ4IpZ9wHtONim3YANx5vGQO7PPkJv-JOPf83tbDoCjfHT8jPgV2rhHMVquKO0gmbxKTgJydSN-tbtxvSYMCmy42LiOI1eLbxCCrIA1pcKgy_hUoYMBozlYRp5wJmPzcZjT8E5ZtGhVGhRAvES4W5PHHsmu6MntPMIBpA9pZSoIrPKXQyqOXhVVke_AExHPVDhh6GcpF1AGWOdtq5Vth04MwwtbDzKyx47ihCThz-0nj9KR8bKQ4KN7Z0jYqyRJX5pXT9bMw7Mp6i__BZGQrFHq7IxnrRdZ-829eng0l5fYuqCySrsCgaf5242cMXT42OwxNdpfvDlMjZpYr09jtTBYlR4KKEMuOKgaWyWlyLT0GhHOJRepoATGArlEXK2clHWz7iFBcNYHb8izgkLWLHIoAx032LCn2UDsdB3AGQmDX3kNRCDOaZFuh_YRprgz8AhZpAadgpuKIz_QPVDh4C75MVpUFLiHaaK76DRC5mWG63XNpuPa831LT70xDhvaOkbBnfhKH6IC2QgwvYQEaXIQv5w4ZZCNIibMmBByfzF9sJomhhhG8fsBB5vAIszo-pEkJMnPR42ri2_2eaXzD1IHj6X1ViMZUHPArvz53nPz4UraCP0aGnkdZnLr0GHJ19PN2vnm7VJBvRW37zSfFYT962-4l3gZYK1aYivJAKE2JmxdL6-udis3cXYDdXr-VFMVXOsyI1izZV4OhnsyAxb7RoAUihQTbUMsDcDK3Az5qHAhOyuQNsdsKMwa8Ef8nRQpjCuLFNMsR7TtPEBATZmRLLIKnfqTQy6ry-B0BHp4Om3VGMr7DbcrNv3ubJMM8jGkYw85Ybmm7WWaWWlqJsFw7Laz8ABWDWkyFWXU2AfZlELbJ-sIKSAYqh7QH1y9J7G3Fxra41K0Exfl8hy91JbzKKnWgZ49OKjbiV2i_ZkdemoNx4Sioje7xzpaHKmZsq33_HzyjB8ajd4ZKAT-IA-7h7J4JxwFmC2gCgYQdcq-Wm6O10CVl75jawTtaFp8kLZrpgVmxK4J4Cr6MzP0FFRZmdUUwpdkdkVVpcks3KZFBweTdkQxVqkaHYBrJW36F6m1-obT0HdoXfZATPJxkSW3h7AjatJvhQUgwJxKaMO84WORhziG75mEi_t8JBApxmhswvMUomtZlmuSkzNSdPPGRjTTM5hr4ikSilW0MKS-Xoe9oSHIxl8g8uizVX0IuZmIUzN9U1V1Sw9lG5GBt-0I1SeB1UqU52EqBhpJ6EUiBn00jQ2_s8BIgWJIhmWdYFiNeHqRIeGrq9_x3Qr79igbJaxG14-7bAb2E2rr1g3B-uMQjt15U7j2ia_SLunclnTMAIjcAnxXV0G4jPYqCKYsXOYU-EeE3D2HNfgdYssJpUin3aHWPcEYpoCvR0WLbiyTbYCd31Kqm_W1IHewGq8swVQGDgDtg_DvbRCB3HSKFenkqAiOjfhHoaoNkTNEOB8tPwk89P6PDxWgeiFJdGRbcO9f_or_PkfDYJj7Q)
