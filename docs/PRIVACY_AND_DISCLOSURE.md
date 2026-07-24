[//]: # (ob:be94d633)
# Privacy Boundaries for Portable Artifacts

[//]: # (ob:9db57e7e)
> 状态：V0 产品边界决议稿
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
V0 只需要五条规则：

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
V0 采用 artifact policy：

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
重新开启是少见、明确的 transition。V0 必须保证：

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
- V0 不承诺 crypto-shredding 或远程删除。

[//]: # (ob:4779c987)
如果连事件存在本身都不能披露，安全选择是生成新的 sanitized/derived lineage，并明确它不是旧历史的完整连续投影。

[//]: # (ob:0d3174f5)
## 9. V0 edge cases

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
## 10. V0 明确不做

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
Portable V0 发布前至少通过：

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

[//]: # (proofpress:meta:eyJhcnRpZmFjdF9pZCI6InBwXzYxOGFhNGZkODJjZDY5ZDA4NDE3MjE3OCIsInBvbGljeSI6ImxvY2FsIiwicHJvb2ZwcmVzcyI6MX0)
