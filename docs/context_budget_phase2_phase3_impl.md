# Context Budget Phase 2/3 实现说明

> 目的：说明第二批和第三批功能如何落地，方便代码审查。

## 一句话总结

我们没有重写 review 主流程，而是把上下文预算、分片、多次调用、模型补充请求和恢复机制都收进 `OpenAICompatibleReviewAgent` 内部。外层仍然调用：

```python
reviewer.review(package, prior_feedback=...)
```

所以原来的 loop、verifier、critic、filter 仍然可以继续工作。

## Phase 2：大 diff 能力

### 1. ReviewerContext

新增正式数据结构：

- `ReviewerContext`：真正发送给 LLM 的上下文视图。
- `ReviewShard`：记录一个分片的审计信息。
- `ShardReviewResult`：记录一个分片的审查结果。

完整 `EvidencePackage` 仍然保留在本地，用于 verifier、filter、report 和 checkpoint hash。

### 2. 分片 Review

入口在：

```text
src/code_review_agent/review/context_budget.py
```

核心函数：

```python
build_reviewer_contexts(...)
```

逻辑：

- 小 diff：构建一个 `ReviewerContext`。
- 大 diff：按 changed file 切成多个 shard。
- 每个 shard 内继续使用 risk-first evidence selection。
- 每个 shard 都有自己的 selected / omitted evidence 审计。

### 3. 合并 Shard 结果

入口在：

```text
src/code_review_agent/review/agents.py
```

`OpenAICompatibleReviewAgent.review()` 会：

1. 构建多个 `ReviewerContext`。
2. 对每个 context 调用一次 LLM。
3. 收集所有 shard 的 issue。
4. 按 `(category, file, line)` 合并重复 issue。
5. 把合并后的候选继续交给原有 verifier、critic、filter。

这样最终仍然只生成一个 report。

### 4. Large Patch 回归

测试覆盖在：

```text
tests/test_review_context_budget.py
tests/test_review_pipeline.py
```

验证点：

- 大 diff 会产生多个 reviewer context。
- live mode 会多次调用 LLM。
- report 中会记录 shard 数量和每个 shard 的预算摘要。

## Phase 3：模型反馈和恢复

### 1. 有限 Context Request

LLM 现在可以返回对象格式：

```json
{
  "issues": [],
  "context_requests": []
}
```

允许的请求类型只有：

- `same_file_more_evidence`
- `related_tests`
- `related_symbol`
- `risk_evidence`

不允许模型自由请求任意文件、全仓库、命令执行或无限检索。

### 2. One-shot Context Refill

入口在：

```python
build_context_refill(...)
```

逻辑：

- 只补发一轮。
- 只从完整 `EvidencePackage` 中选择还没发过的 evidence。
- refill context 仍然受 token budget 限制。
- refill 后不会继续递归请求上下文。

### 3. Shard Checkpoint / Resume

新增 checkpoint 文件：

```text
<out>/live_context_checkpoint.json
```

记录内容：

- shard id
- selected evidence ids
- context requests
- LLM issues
- agent run audit

恢复逻辑：

- 开启 `--resume` 后，如果 package hash 和 diff hash 匹配，已完成 shard 不再重复调用 LLM。
- 如果 diff、package 或 shard evidence 变化，对应 shard 会重新执行。
- 原有 `loop_checkpoint.json` 不被重写。

## 主要影响文件

```text
src/code_review_agent/models.py
src/code_review_agent/review/context_budget.py
src/code_review_agent/review/agents.py
src/code_review_agent/review/pipeline.py
src/code_review_agent/output/json_report.py
src/code_review_agent/output/review_markdown.py
src/code_review_agent/cli.py
```

## 没有做的事

- 没有引入 RAG 或向量库。
- 没有引入 multi-agent。
- 没有做 prompt caching。
- 没有并发调用 shard。
- 没有无限 context feedback loop。

## 审查建议

建议按这个顺序看：

1. `models.py`：先看新增数据结构。
2. `context_budget.py`：看 evidence selection、sharding、refill。
3. `agents.py`：看 live reviewer 如何多 shard 调用和恢复。
4. `pipeline.py`：看 report 审计如何接入。
5. `tests/test_review_context_budget.py` 和 `tests/test_review_pipeline.py`：看行为是否符合预期。

