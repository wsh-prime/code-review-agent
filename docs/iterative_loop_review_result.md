# Iterative Review Loop 审核结果

> 日期：2026-04-29
> 对象：`docs/iterative_loop_impl.md`
> 结论：方案可继续推进，不需要整体重设计。

## 总结论

`IterativeHarnessRunner` 的方向是正确的。

优先落地范围建议收敛为：

1. `GroundingVerifier`
2. `CritiqueResult -> PriorFeedback -> ReviewAgent.review()` 反馈链路
3. `IterativeHarnessRunner`
4. checkpoint / resume
5. API retry / fallback
6. loop summary 输出
7. 基础 tracing 字段

暂缓项：

1. Prompt caching
2. 完整 HITL 交互
3. patch draft
4. apply-and-verify loop
5. 外部 benchmark adapter

## 架构结论

### 状态机

状态机成立。

保留三类退出条件：

1. `uncertain == []`
2. `i >= max_iter - 1`
3. `issue_set(i) == issue_set(i-1)`

需要调整：

1. `max_iter` 默认值保留为 `2`
2. `max_iter=1` 必须严格退化为当前单轮行为
3. `issue_set` 必须使用稳定 issue id
4. 稳定判断应比较规范化后的 `keep + uncertain + reject`
5. 不能只比较 `keep`

### Feedback 链路

保留：

```text
CritiqueResult
  -> PriorFeedback
  -> ReviewAgent.review(prior_feedback=...)
```

调整：

1. `CritiqueResult.uncertain` 不使用 `list[tuple[ReviewIssue, str]]`
2. 新增结构化 dataclass 表示 critic 反馈项
3. feedback 中保留：
   - issue id
   - category
   - critic reason
   - original confidence
   - evidence ids
4. `prior_feedback=None` 时行为必须和当前 reviewer 完全一致

### GroundingVerifier

保留 pre-filter 位置。

执行顺序：

```text
ReviewAgent.review()
  -> GroundingVerifier
  -> CriticAgent.critique()
  -> PriorFeedback
```

`GroundingVerifier` 输出：

1. `verified`
2. `ungrounded`
3. `discarded`

校验项：

1. `evidence_ids` 非空
2. `evidence_ids` 均存在于 `package.evidence_index`
3. issue file 属于 changed paths，或 evidence 指向 changed paths
4. line 与 changed hunk / changed entity / diff evidence 相关
5. style nit 直接 discarded

## 实现范围

### 第一阶段必须完成

文件：

1. `src/code_review_agent/models.py`
2. `src/code_review_agent/review/agents.py`
3. `src/code_review_agent/review/verifier.py`
4. `src/code_review_agent/review/loop.py`
5. `src/code_review_agent/review/pipeline.py`
6. `src/code_review_agent/cli.py`
7. `src/code_review_agent/output/review_markdown.py`
8. `tests/test_review_verifier.py`
9. `tests/test_review_loop.py`
10. `tests/test_review_agents_fake.py`
11. `tests/test_review_pipeline.py`
12. `tests/test_cli.py`

### 暂不实现

文件：

1. `src/code_review_agent/review/hitl.py`
2. `tests/test_review_hitl.py`

功能：

1. `--hitl`
2. `--no-interactive`
3. `--enable-cache`
4. prompt cache token 统计
5. human decision report

## 数据模型结果

### 新增模型

```python
@dataclass(slots=True)
class UncertainFeedbackItem:
    issue_id: str
    category: str
    critic_reason: str
    original_confidence: float
    evidence_ids: list[str] = field(default_factory=list)
```

```python
@dataclass(slots=True)
class PriorFeedback:
    iteration: int
    uncertain_items: list[UncertainFeedbackItem] = field(default_factory=list)
```

```python
@dataclass(slots=True)
class CritiqueResult:
    keep: list[ReviewIssue] = field(default_factory=list)
    uncertain: list[UncertainFeedbackItem] = field(default_factory=list)
    reject: list[ReviewIssue] = field(default_factory=list)
    agent_runs: list[AgentRun] = field(default_factory=list)
```

### AgentRun 新增字段

```python
iteration: int = 0
feedback_hash: str = ""
retry_count: int = 0
retry_log: list[str] = field(default_factory=list)
latency_ms: int = 0
token_count_in: int = 0
token_count_out: int = 0
trace_id: str = ""
span_id: str = ""
parent_span_id: str = ""
status: str = "ok"
error_type: str = ""
```

暂不加入：

```python
cache_hit: bool
cache_saved_tokens: int
```

## Agent 接口结果

### ReviewAgent

```python
class ReviewAgent(Protocol):
    def review(
        self,
        package: EvidencePackage,
        *,
        prior_feedback: PriorFeedback | None = None,
    ) -> list[ReviewIssue]: ...
```

### CriticAgent

```python
class CriticAgent(Protocol):
    def critique(
        self,
        issues: list[ReviewIssue],
        package: EvidencePackage,
    ) -> CritiqueResult: ...
```

保留兼容函数：

```python
run_fake_hybrid_agents(...)
run_openai_compatible_review_agent(...)
```

但内部改为调用 loop。

## Loop 结果模型

### IterationRecord

字段：

1. `i`
2. `candidate_issue_count`
3. `verified_count`
4. `ungrounded_count`
5. `keep_count`
6. `uncertain_count`
7. `reject_count`
8. `feedback_sent`
9. `agent_runs`

### LoopResult

字段：

1. `final_issues`
2. `needs_human_review`
3. `discarded`
4. `agent_runs`
5. `iterations`
6. `iterations_completed`
7. `converged`
8. `fallback_used`
9. `fallback_reason`

## Checkpoint 结果

文件名：

```text
loop_checkpoint.json
```

写入位置：

```text
--out/loop_checkpoint.json
```

必须包含：

1. `schema_version`
2. `run_id`
3. `mode`
4. `max_iter`
5. `iteration`
6. `converged`
7. `package_hash`
8. `diff_hash`
9. `iterations`
10. `last_feedback`

resume 校验：

1. `schema_version` 匹配
2. `mode` 匹配
3. `package_hash` 匹配
4. `diff_hash` 匹配
5. `iteration < max_iter`

校验失败：

1. 不 resume
2. 从头运行
3. 在 summary 中记录 `resume_ignored_reason`

## Retry / Fallback 结果

### Retry

重试对象：

1. `urllib.error.URLError`
2. HTTP `429`
3. HTTP `500`
4. HTTP `502`
5. HTTP `503`
6. HTTP `504`

不重试对象：

1. HTTP `400`
2. HTTP `401`
3. HTTP `403`
4. JSON parse error
5. schema validation error

默认参数：

```python
max_attempts = 3
base_delay_seconds = 2.0
backoff_factor = 2.0
```

### Fallback

fallback 后：

1. deterministic rules findings 保留
2. live agent findings 置空
3. `summary.mode = "hybrid-live/fallback-rules"`
4. `summary.fallback_used = true`
5. `summary.fallback_reason` 填写异常摘要
6. `AgentRun.status = "fallback"`

## CLI 结果

第一阶段新增参数：

```text
--max-iter N
--resume
```

默认：

```text
--max-iter 2
```

规则：

1. `rules` 模式忽略 `--max-iter`
2. `rules` 模式忽略 `--resume`
3. `hybrid-fake` 默认不写 checkpoint
4. `hybrid-live` 默认写 checkpoint
5. `hybrid-fake` 可后续加 `--checkpoint`

暂不新增：

```text
--hitl
--no-interactive
--enable-cache
```

## Report 结果

### summary 新增字段

```json
{
  "loop_enabled": true,
  "loop_iterations_completed": 2,
  "loop_converged": true,
  "fallback_used": false,
  "fallback_reason": null,
  "resume_used": false,
  "resume_ignored_reason": null,
  "total_latency_ms": 0,
  "total_token_count_in": 0,
  "total_token_count_out": 0
}
```

### 顶层新增字段

```json
{
  "loop": {},
  "tracing": {}
}
```

### Markdown 新增章节

```markdown
## Loop Summary
```

内容只展示：

1. mode
2. iterations
3. converged
4. fallback
5. retry count
6. total latency
7. total tokens
8. 每轮 candidate / verified / uncertain / kept / rejected 数量

## 测试结果清单

必须新增测试：

1. `test_ground_verify_empty_evidence_ids`
2. `test_ground_verify_unknown_evidence_id`
3. `test_ground_verify_file_not_changed`
4. `test_ground_verify_line_not_related`
5. `test_loop_max_iter_one_matches_current_fake_hybrid`
6. `test_loop_converges_when_no_uncertain`
7. `test_loop_runs_second_iter_for_uncertain`
8. `test_loop_stops_on_stable_issue_set`
9. `test_checkpoint_written_after_iteration`
10. `test_resume_uses_checkpoint_feedback`
11. `test_resume_ignored_when_package_hash_mismatch`
12. `test_retry_on_503_then_success`
13. `test_no_retry_on_401`
14. `test_fallback_rules_preserved_on_live_failure`
15. `test_cli_review_accepts_max_iter_and_resume`
16. `test_report_contains_loop_summary`

必须保留通过：

1. `tests/test_review_agents_fake.py`
2. `tests/test_review_pipeline.py`
3. `tests/test_output_review_markdown.py`
4. `tests/test_cli.py`

## 推荐实施顺序

1. models
2. fake agents protocol
3. verifier
4. loop without checkpoint
5. loop tests
6. pipeline integration
7. CLI flags
8. checkpoint write/read
9. retry helper
10. live agent retry integration
11. fallback integration
12. report loop summary
13. tracing fields

## 第一阶段验收标准

1. `pytest tests/test_review_verifier.py -v` 通过
2. `pytest tests/test_review_loop.py -v` 通过
3. `pytest tests/test_review_agents_fake.py -v` 通过
4. `pytest tests/test_review_pipeline.py -v` 通过
5. `pytest tests/test_cli.py -v` 通过
6. `pytest` 全量通过
7. `code-review-agent review --mode hybrid-fake --max-iter 1` 与当前行为一致
8. `code-review-agent review --mode hybrid-fake --max-iter 2` 输出 loop summary
9. `code-review-agent review --mode hybrid-live --resume` 能读取合法 checkpoint
10. live API 失败时 rules findings 不丢失

## 最终判断

继续推进。

第一阶段目标：

```text
可靠的 iterative review harness
```

不是：

```text
完整工业级 agent platform
```

完成第一阶段后，再进入：

1. HITL
2. Prompt caching
3. FixPlan
4. PatchDraft
5. External benchmark adapter
