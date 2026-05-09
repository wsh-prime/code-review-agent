# Live Review 改造复盘

本文记录最近这一轮 live review 改造：我们遇到了什么问题，怎么修，为什么这么修。它不是完整架构说明；完整数据流看 `docs/architecture_overview.md`。

## 背景

目标是让 `hybrid-live` 能稳定审查大 diff，同时减少模型噪音。之前的问题不是“模型完全不可用”，而是上下文组织方式让模型很难稳定做出高质量判断：有时信息太碎，有时信息太多，有时一个 shard 失败会拖垮整次运行。

## 问题 1：单行 diff 作为主证据太弱

之前 live 输入里大量使用 `diff` 单行 evidence。单行能定位，但缺少局部上下文，模型经常只能看到“这一行变了”，看不到它前后的控制流、函数语义和相邻修改。

这会带来两个结果：

- 模型更容易猜测，输出“可能有问题”的弱评论。
- 模型更频繁请求上下文，但它并不总能准确知道该请求哪些 evidence。

解决方式：

- 在 `review/evidence.py` 增加 `diff_hunk` evidence。
- `diff_hunk` message 保留 hunk header 和一段 window，上限由 `MAX_HUNK_EVIDENCE_LINES`、`MAX_HUNK_LINE_CHARS` 控制。
- `context_budget.py` 里把 `diff_hunk` 作为默认展开 evidence，`diff` 单行保留为定位和兼容用途。
- prompt 明确告诉模型：主要基于 `diff_hunk` 推理，单行 diff 主要用于定位。

为什么这样做：

`diff_hunk` 是 review 的自然单位。它比单行多了足够上下文，又比整文件便宜很多，适合作为 live reviewer 的默认输入。

## 问题 2：Evidence 信息高度重合，prompt 被撑大

`EvidencePackage` 里同时有 `changed_files`、`changed_entities`、`risk_signals`、`evidence_index`。它们本来服务不同阶段，但如果原样展开给模型，会重复表达同一件事：

- 文件变更摘要里有路径。
- entity 里有符号和路径。
- risk 里有 reason 和 evidence_ids。
- evidence_index 里又有 risk/entity/diff 的完整 message。

解决方式：

- live 输入使用 `risk_compact_manifest_v1`。
- `risk`、`entity` 更多作为卡片和 manifest 展示，不默认完整展开。
- 默认展开 evidence kind 收敛为 `diff_hunk`、`test_discovery`、`hygiene`。
- 限制 manifest、risk card、entity card 数量，避免大 diff 下清单本身变成新的大 prompt。

为什么这样做：

模型需要知道“有什么可看”和“当前重点是什么”，但不需要每一层都完整展开。压缩后的 manifest 给模型导航能力，primary evidence 给模型判断能力。

## 问题 3：按文件数切 shard 仍然会超预算

旧 shard 逻辑主要按文件数切分。大文件、长 hunk 或证据密集文件会让某个 shard 远大于其他 shard，导致超时或 API 压力集中。

解决方式：

- `build_reviewer_contexts()` 改为 token-aware shard split。
- 每个候选文件加入 shard 前先估算输入 token。
- live 单次调用被限制在 `DEFAULT_MAX_SHARD_INPUT_TOKENS = 9000` 附近。
- 如果单个文件本身就很大，允许单文件 shard 截断，而不是继续塞更多文件。

为什么这样做：

大 diff 的问题主要不是文件数量，而是上下文体积不均衡。按估算 token 切分比按文件数更接近真实 API 风险。

## 问题 4：refill 可能再次变成大 prompt

模型请求补充上下文是必要的，但如果一次 refill 放太多 evidence，就会把 primary shard 的问题搬到 refill。

解决方式：

- `build_context_refill()` 同样使用 9000 token 上限。
- 每个 context request 最多补有限数量 evidence。
- `available_context` 鼓励模型请求明确 evidence ids，而不是宽泛请求整个文件。

为什么这样做：

refill 应该是“精准补证据”，不是第二次完整 review。限制 refill 大小可以降低超时和重复推理。

## 问题 5：模型不知道“还能请求什么”时，请求质量会差

只告诉模型当前 shard 里的 evidence 不够。它还需要知道有哪些路径、风险、证据可以请求，否则 context request 会偏模糊。

解决方式：

- `ReviewerContext.available_context` 保留 evidence manifest、路径索引、风险索引。
- manifest 只展示有限数量和样本，避免清单本身过大。
- context request schema 保持有限类型：`same_file_more_evidence`、`related_tests`、`related_symbol`、`risk_evidence`。

为什么这样做：

模型不应该盲猜 evidence id；它应该基于一个受控目录请求上下文。这个目录越清晰，请求越接近 reviewer 真实需要。

## 问题 6：一个 shard 超时会导致整次 live fallback

早期实现里，某个 shard 抛 `_AgentTransientError` 后，整个 `hybrid-live` 会进入 fallback-rules。大 diff 下这很不划算：其他 shard 可能已经成功，结果却被一次网络/API 抖动掩盖。

解决方式：

- primary shard transient error 只记录失败并继续其他 shard。
- refill shard transient error 直接跳过，不中断主流程。
- 只有所有 primary shard 都失败且没有任何 issue 时，才整体 fallback。
- fallback 时保留已有 `agent_runs`，并尝试从 checkpoint 恢复已完成 loop。

为什么这样做：

review shard 是天然可降级单元。部分 shard 失败应该变成报告里的审计信息，而不是直接清空整次 live 结果。

## 问题 7：checkpoint 和 report 容易误导

复用同一个 `--out` 目录时，旧 checkpoint 可能影响新运行。live 失败时，如果前面其实已经完成了一些调用，最终 report 也可能显示得像完全没跑。

解决方式：

- 非 `--resume` 运行会清理旧的 `loop_checkpoint.json` 和 `live_context_checkpoint.json` 文件。
- checkpoint 校验 mode、package hash、diff hash。
- fallback 时尽量 salvage 已完成 loop records 和 live agent runs。

为什么这样做：

报告必须准确反映“真实跑了什么”。否则我们很难判断问题是模型质量、上下文预算、API 稳定性，还是恢复逻辑污染。

## 问题 8：低信号建议过多

live 模型有时会输出 comment/docstring/test-quality 之类建议，或者用“may/could/might”描述不确定行为。这些内容对 code review 噪音很大。

解决方式：

- 新增 `review/issue_quality.py`，集中判断 style-only 和 low-signal suggestion。
- `filter.py` 和 `verifier.py` 共用这些启发式。
- 如果文本包含具体 failure 关键词，例如 crash、wrong、security、timeout 等，则不会因为措辞弱就直接丢弃。

为什么这样做：

我们要过滤的是“没有失败场景的评论”，不是过滤所有低置信问题。具体 correctness/security 风险仍应该保留或进入人工复核。

## 当前验证结果

最新 live run：`outputs/runs/20260509-185258-live-codex-final`。

关键结果：

- `mode = hybrid-live`
- `fallback_used = false`
- 17 个 changed files，97 个 changed entities，82 个 risk signals
- 6 个 primary shard，6 个 refill shard
- 13 次 agent run，全部 `ok`
- 总输入/输出 token：87825 / 8519
- context warnings 为空
- findings 5，needs human review 5，discarded 2

这说明当前 live 流程已经能完整跑通大 diff，token-aware shard 和 hunk evidence 生效了。

## 仍然没完全解决的问题

现在可以投入“辅助审查/实验验证”，但还不建议直接作为生产阻断 gate。剩余问题主要是质量和产品化：

- shard 仍是串行调用，耗时较长。
- live finding 仍有部分误报，需要继续用真实 case 调 prompt 和 filter。
- `diff_hunk` 当前主要定位到 hunk 起始行，细粒度 line range 还可以继续改。
- per-shard 失败已经不会全局 fallback，但 report 里还可以更明显展示失败 shard 数和覆盖缺口。
- 目前 critic 仍是 fake/deterministic，真实 critic 的产品化还没完成。

## 结论

这轮改造的方向是：**hunk 作为主要判断证据，manifest 作为导航，refill 作为精准补证据，filter 作为噪音收口**。

它解决了大 diff 下最要命的稳定性问题，也让模型看到的上下文更像一个真实 reviewer 会看的上下文。下一步重点不应继续堆更多 prompt 信息，而应围绕真实运行结果做 precision/recall 调优和失败 shard 可观测性。
