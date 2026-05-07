# Iterative Review Loop：Harness 层实现方案

> 日期：2026-04-29
> 对应：post_mvp_roadmap.md Phase 15（Issue Refinement Loop）
> 定位：在现有 harness 上加入 **Critic→Refine 迭代循环**，重点覆盖
> 断点重传、API 容错与重试、Fallback 降级链、幂等性追踪、
> AgentRun Tracing、Prompt Caching、Human-in-the-Loop Gate 等 harness 可靠性技术。

---

## 1. 背景：当前 harness 的单次 pass 问题

现有 `hybrid-fake` / `hybrid-live` pipeline 是一次性的：

```
EvidencePackage
  → ReviewAgent.review()       # 一次调用
  → CriticAgent.filter()       # 只做剪枝，不给任何反馈
  → filter_issues()
  → report
```

两个已知缺陷：

1. **ReviewAgent 无纠错机会**：错误的 evidence 引用、置信度偏高的幻觉 finding 一路进入报告，CriticAgent 无法把"不确定"反馈回去。
2. **Harness 无容错状态**：一次 API 失败（超时、限流、服务中断）导致整个 review 命令重新从零开始。对长 diff 或慢推理模型来说代价极高。

本文档描述如何以最小改动量解决这两个问题：加入一个**有状态、可恢复、最多 N 轮**的迭代循环。

---

## 2. Loop 设计概览

### 2.1 状态机

```
                   ┌─────────────────────────────────────────────┐
                   │           LoopState（磁盘持久化）              │
                   │  iteration / iteration_records / feedback    │
                   └────────────────┬────────────────────────────┘
                                    │  load（--resume）/ save（每轮结束）
  EvidencePackage                   ▼
  ──────────────► IterativeHarnessRunner.run()
                          │
            ┌─────────────▼──────────────────────┐
            │  iteration i（i = 0, 1, … max_iter-1）│
            │                                      │
            │  ReviewAgent.review(                  │
            │    package,                           │
            │    prior_feedback = feedback_i        │  ← 上一轮 Critic 的结构化反馈
            │  ) → candidate_issues                 │
            │                                       │
            │  GroundingVerifier.verify(            │  ← 确定性校验层（不调 API）
            │    candidate_issues, package          │
            │  ) → verified / ungrounded            │
            │                                       │
            │  CriticAgent.critique(                │
            │    verified_issues, package           │
            │  ) → CritiqueResult                   │
            │       .keep[]                         │
            │       .uncertain[ (issue, reason) ]   │
            │       .reject[]                       │
            │                                       │
            │  收敛？                                │
            │  = uncertain 为空                      │
            │  OR i >= max_iter - 1                 │
            │  OR issue_set(i) == issue_set(i-1)    │
            └───────────────────────────────────────┘
                          │
                  final = keep[]
                          │
                   filter_issues()
                          │
                        Report
```

### 2.2 收敛条件（任意满足即停止）

| 条件 | 含义 |
|---|---|
| `uncertain == []` | Critic 对所有候选 issue 有明确判断，不需要下一轮 |
| `i >= max_iter - 1` | 到达最大轮数上限（默认 2），强制退出 |
| `issue_set(i) == issue_set(i-1)` | ReviewAgent 对 feedback 无响应，集合不变，幂等收敛 |

**为什么默认 max_iter = 2**：第 0 轮 = 当前行为；第 1 轮 = 有一次反馈后的改进；两轮 loop 已经足够展示 agent harness 能力，且 API 成本和延迟可控。

---

## 3. Harness 技术要点

### 3.1 断点重传（Loop Checkpoint）

**动机**：`hybrid-live` 调用真实 LLM，一次 review 可能花费 30–120 秒。若第 1 轮 API 调用因网络抖动失败，不应重跑第 0 轮（已完成且结果已知）。

每轮 loop 结束时，`IterativeHarnessRunner` 把状态写入 `--out/loop_checkpoint.json`：

```json
{
  "schema_version": "1.0",
  "mode": "hybrid-live",
  "iteration": 1,
  "converged": false,
  "iterations": [
    {
      "i": 0,
      "candidate_issue_count": 4,
      "keep": [...],
      "uncertain": [
        {
          "issue_id": "I-002",
          "category": "test_gap",
          "critic_reason": "evidence E-003 引用的行号超出 changed entity 范围"
        }
      ],
      "reject": [],
      "agent_runs": [...],
      "feedback_hash": "sha256:b2c1..."
    }
  ]
}
```

**恢复流程**：

```powershell
# 正常运行（从头开始）
code-review-agent review --repo . --diff changes.patch --out outputs/review --mode hybrid-live

# API 超时中断后，从断点继续
code-review-agent review --repo . --diff changes.patch --out outputs/review --mode hybrid-live --resume
```

`--resume` 逻辑（在 `IterativeHarnessRunner._load_checkpoint` 中实现）：

```
1. 读取 loop_checkpoint.json
2. 反序列化已完成的 IterationRecord[]
3. 还原最后一轮的 PriorFeedback
4. 返回 (start_i = checkpoint.iteration, prior_feedback, completed_records)
5. run() 的 for 循环从 start_i 开始，跳过已完成的轮次
```

**安全保证**：
- `--resume` 只在 `--out` 目录下存在 `loop_checkpoint.json` 时生效，否则从头开始（幂等启动）。
- `hybrid-fake` 模式默认不写 checkpoint（完全确定性，重跑等价于恢复）；可通过 `--checkpoint` flag 强制开启。
- `loop_checkpoint.json` 只写入 `--out` 目录，不修改被审查仓库。

---

### 3.2 API 容错与重试

**现状**：`OpenAICompatibleReviewAgent` 当前只用 `urllib.request.urlopen`，超时时抛裸 `URLError`，没有重试。

**新增 `_retry_with_backoff()`**（纯 stdlib，零第三方依赖）：

```python
from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar
from urllib import error as urllib_error

T = TypeVar("T")

_RETRYABLE_HTTP_CODES: frozenset[int] = frozenset({429, 500, 502, 503, 504})


def _retry_with_backoff(
    fn: Callable[[], T],
    *,
    max_attempts: int = 3,
    base_delay_seconds: float = 2.0,
    backoff_factor: float = 2.0,
    retry_log: list[str] | None = None,
) -> T:
    """
    Retry fn with exponential backoff on transient errors.
    On fatal errors (401, 400, non-retryable), raises immediately.
    """
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except urllib_error.HTTPError as exc:
            if exc.code not in _RETRYABLE_HTTP_CODES:
                # 401 Unauthorized / 403 Forbidden / 400 Bad Request → 不重试
                raise _AgentFatalError(f"HTTP {exc.code}: {exc.reason}") from exc
            last_exc = exc
            wait = _retry_after(exc) or (base_delay_seconds * (backoff_factor ** attempt))
            if retry_log is not None:
                retry_log.append(
                    f"attempt {attempt + 1} failed: HTTP {exc.code}, retrying in {wait:.1f}s"
                )
            time.sleep(wait)
        except urllib_error.URLError as exc:
            last_exc = exc
            wait = base_delay_seconds * (backoff_factor ** attempt)
            if retry_log is not None:
                retry_log.append(
                    f"attempt {attempt + 1} failed: URLError {exc.reason}, retrying in {wait:.1f}s"
                )
            time.sleep(wait)
    raise _AgentTransientError(
        f"API call failed after {max_attempts} attempts"
    ) from last_exc


def _retry_after(exc: urllib_error.HTTPError) -> float | None:
    """Parse Retry-After header (seconds or HTTP-date) if present."""
    header = exc.headers.get("Retry-After") if exc.headers else None
    if header is None:
        return None
    try:
        return float(header)
    except ValueError:
        return None  # HTTP-date 格式暂不解析，退回 backoff
```

**错误分类与处理策略**：

| 错误类型 | HTTP 码 / 异常 | 处理 |
|---|---|---|
| 连接超时 / DNS 失败 | `urllib.error.URLError` | 重试，指数退避 |
| 限流 | 429 | 重试，尊重 `Retry-After` header |
| 服务暂时不可用 | 500 / 502 / 503 / 504 | 重试 |
| 请求格式错误 | 400 | 不重试，记录 prompt hash，走 Fallback |
| 认证失败 | 401 / 403 | 不重试，立即抛 `_AgentFatalError`（重试无意义） |
| JSON 解码失败 | — | 不重试，记录原始响应，走 Fallback |
| Schema 验证失败（evidence_ids 为空等） | — | 不重试，issue 降级为 `needs_human_review` |

所有重试事件记录在 `AgentRun.retry_log` 字段（见 3.4 节），可在报告和 eval 中追溯。

---

### 3.3 Fallback 降级链

**设计原则**：deterministic rules baseline 是 guardrail，永远不依赖 API。API 失败只影响 agent 层，不应让 guardrail 失效。

```
hybrid-live API 全部重试失败
        │
        ▼
fallback_used = True
fallback_reason = "API error after 3 attempts: 503 ..."
        │
        ▼
agent_findings = []         ← agent 层输出置空
agent_runs 标记 fallback     ← AgentRun.fallback_used = True
        │
        ▼
candidate_findings = rules_result.findings   ← 只用 deterministic 结果
        │
        ▼
report.summary.mode = "hybrid-live/fallback-rules"
report.summary.fallback_reason = "..."
```

Fallback 触发条件：

```python
class _AgentFatalError(Exception):
    """Non-retryable API error (401/403/400). Triggers immediate fallback."""

class _AgentTransientError(Exception):
    """Retryable error exhausted max_attempts. Triggers fallback."""
```

`pipeline.py` 中的 fallback 捕获点：

```python
try:
    loop_result = runner.run(package, resume=resume)
    agent_findings = loop_result.final_issues
    agent_runs = loop_result.agent_runs
    if loop_result.fallback_used:
        mode = f"{mode}/fallback-rules"
        fallback_reason = loop_result.fallback_reason
except (_AgentFatalError, _AgentTransientError) as exc:
    agent_findings = []
    agent_runs = []
    mode = f"{mode}/fallback-rules"
    fallback_reason = str(exc)
```

---

### 3.4 幂等性与 AgentRun 追踪

**目标**：让每次 agent 调用在 `AgentRun` 中留下可追踪的输入指纹，支持 eval 回归和 debug。

`AgentRun` 新增字段（`models.py`）：

```python
@dataclass(slots=True)
class AgentRun:
    # --- 现有字段 ---
    agent_name: str
    model: str
    prompt_hash: str
    input_evidence_ids: list[str]
    output_issue_ids: list[str]
    fallback_used: bool
    # --- 新增字段 ---
    iteration: int = 0                    # 所属 loop 轮次（单次 pass 时 = 0）
    feedback_hash: str = ""               # PriorFeedback JSON 的 sha256（无 feedback 时 = ""）
    retry_count: int = 0                  # 实际发生的重试次数
    retry_log: list[str] = field(default_factory=list)  # 每次重试原因
```

**输入指纹三元组**：

```
prompt_hash + feedback_hash + sorted(input_evidence_ids)
```

若两次运行的三元组相同：
- **fake agent**：输出完全确定，eval 幂等，CI 不 flaky。
- **live agent**（`temperature=0`）：输出大概率相同，可用于 diff 调试。

`feedback_hash` 的计算：

```python
def _feedback_hash(feedback: PriorFeedback | None) -> str:
    if feedback is None:
        return ""
    raw = json.dumps(
        {
            "iteration": feedback.iteration,
            "uncertain_items": [
                {"issue_id": item.issue_id, "critic_reason": item.critic_reason}
                for item in feedback.uncertain_items
            ],
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return "sha256:" + hashlib.sha256(raw.encode()).hexdigest()[:16]
```

---

### 3.5 Critic Feedback 传递协议

`CriticAgent` 的新接口返回 `CritiqueResult`，不再只是 `list[ReviewIssue]`：

```python
# models.py 新增
@dataclass(slots=True)
class UncertainFeedbackItem:
    issue_id: str
    category: str
    critic_reason: str   # e.g. "evidence E-003 引用的行号 42 超出 changed entity 范围 10-35"
    original_confidence: float

@dataclass(slots=True)
class PriorFeedback:
    iteration: int
    uncertain_items: list[UncertainFeedbackItem]

@dataclass(slots=True)
class CritiqueResult:
    keep: list[ReviewIssue]
    uncertain: list[tuple[ReviewIssue, str]]   # (issue, critic_reason)
    reject: list[ReviewIssue]
    agent_runs: list[AgentRun]                 # Critic 本轮的 AgentRun 记录
```

更新后的 Protocol：

```python
# review/agents.py
class ReviewAgent(Protocol):
    def review(
        self,
        package: EvidencePackage,
        *,
        prior_feedback: PriorFeedback | None = None,
    ) -> list[ReviewIssue]: ...

class CriticAgent(Protocol):
    def critique(
        self,
        issues: list[ReviewIssue],
        package: EvidencePackage,
    ) -> CritiqueResult: ...
```

**向后兼容**：`prior_feedback=None` 时 `ReviewAgent` 行为与现有 `review()` 完全一致；`critique()` 是 `filter()` 的超集（`keep = filter(issues)` 等价）。现有测试不需要修改，只需补充新的 loop 测试。

---

### 3.6 GroundingVerifier（确定性 pre-filter）

在 `CriticAgent` 之前加一个纯确定性的校验层，复用 `filter.py` 已有逻辑，不调 API：

```python
# review/verifier.py
@dataclass(slots=True)
class VerifierResult:
    verified: list[ReviewIssue]     # 通过校验，送去 CriticAgent
    ungrounded: list[ReviewIssue]   # 未通过，直接降级 needs_human_review

def ground_verify(
    issues: list[ReviewIssue],
    package: EvidencePackage,
    changed_paths: set[str],
) -> VerifierResult:
    """
    Deterministic grounding check. Does NOT call any API.
    Checks:
    1. evidence_ids not empty
    2. all evidence_ids exist in package.evidence_index
    3. file path in changed_paths
    4. line_start <= line_end (basic sanity)
    """
```

在 loop 中的位置：

```
ReviewAgent.review() → candidate_issues
    → GroundingVerifier.ground_verify()   ← 确定性，快速，零 API 成本
        .verified    → CriticAgent.critique()
        .ungrounded  → needs_human_review（直接降级，不浪费 Critic token）
```

**价值**：把"无 evidence"或"file 不在 changed set"这类 trivial 幻觉在进入 CriticAgent 之前过滤掉，减少 Critic 的无效 API 调用，且让 Critic 的 `uncertain` 反馈更有意义（都是真正有争议的 issue）。

---

### 3.7 AgentRun Tracing（可观测性）

**背景**：OpenAI Agents SDK（25k+ stars）和 LangGraph 都把 tracing 列为核心能力，面试官普遍期待看到 agent 调用的可观测性设计。我们的 `AgentRun` 已经是 tracing 的雏形，只差延迟和 token 计数两个字段。

`AgentRun` 在已有字段之外追加：

```python
@dataclass(slots=True)
class AgentRun:
    # ... 已有字段（iteration / retry_count / retry_log / feedback_hash）...
    # --- Tracing 新增字段 ---
    latency_ms: int = 0                    # 本次调用墙钟时间（ms）
    token_count_in: int = 0                # prompt token 数（从响应 usage 读取）
    token_count_out: int = 0               # completion token 数
    cache_hit: bool = False                # 是否命中 prompt cache（见 3.8 节）
    cache_saved_tokens: int = 0            # 因 cache 节省的 token 数
```

`latency_ms` 在 `_retry_with_backoff` 的调用侧采集：

```python
import time

start = time.monotonic()
try:
    response = _retry_with_backoff(fn, retry_log=run.retry_log)
finally:
    run.latency_ms = int((time.monotonic() - start) * 1000)
```

`token_count_in / token_count_out` 从 OpenAI-compatible 响应的 `usage` 字段读取（已在响应 JSON 中，无需额外调用）：

```python
usage = response.get("usage", {})
run.token_count_in = usage.get("prompt_tokens", 0)
run.token_count_out = usage.get("completion_tokens", 0)
# prompt_cache_hit_tokens 是 Anthropic 扩展字段（见 3.8 节）
run.cache_saved_tokens = usage.get("prompt_cache_hit_tokens", 0)
run.cache_hit = run.cache_saved_tokens > 0
```

**Tracing 在报告中的呈现**：`review_report.json` 的 `agent_runs` 数组已有每次调用记录，loop 结束后追加聚合摘要到 `tracing` 字段：

```json
"tracing": {
  "total_latency_ms": 4821,
  "total_token_in": 3200,
  "total_token_out": 480,
  "total_cache_saved_tokens": 1800,
  "per_run": [
    {"agent_name": "openai_compatible_reviewer", "iteration": 0,
     "latency_ms": 2341, "token_in": 1800, "token_out": 280,
     "cache_hit": false, "cache_saved_tokens": 0},
    {"agent_name": "openai_compatible_reviewer", "iteration": 1,
     "latency_ms": 2480, "token_in": 1400, "token_out": 200,
     "cache_hit": true, "cache_saved_tokens": 1800}
  ]
}
```

**为什么对面试有价值**：面试官看到 tracing 会直接问"你怎么知道哪一轮慢、哪一轮 token 多？"。有 `latency_ms` 和 `token_count` 就能回答，没有就是黑盒。且这些字段在 eval 中可以直接对比"loop=1 vs loop=2 的总 token 开销"，给 tradeoff 分析提供数字依据。

---

### 3.8 Prompt Caching（成本与延迟优化）

**背景**：Anthropic 在 claude-cookbooks 中专门有 prompt caching cookbook，LiteLLM（45k stars）也内置了 cache 支持。对 code review 的 loop 场景，prompt caching 极其自然：**第二轮的 `EvidencePackage` 与第一轮完全相同**，只有 `PriorFeedback` 不同——前者适合缓存，后者每轮变化。

**适用场景图示**：

```
轮次 0:
  messages[0]: system_prompt          ← 静态，适合缓存
  messages[1]: evidence_package_json  ← 静态，适合缓存（本次 review 中不变）
  messages[2]: "Return ReviewIssue[]" ← 轻量 user prompt

轮次 1:
  messages[0]: system_prompt          ← ✅ 命中 cache（与轮次 0 完全相同）
  messages[1]: evidence_package_json  ← ✅ 命中 cache
  messages[2]: prior_feedback_json    ← 新增，不命中（每轮变化）
  messages[3]: "Return ReviewIssue[]"
```

第二轮的 `system_prompt + evidence_package_json` 部分（通常占 80%+ token）可命中缓存，**Anthropic API 对命中部分仅计 10% 费用**。

**实现方式（不引入第三方依赖）**：

Anthropic API 通过在 `content` 块里加 `"cache_control": {"type": "ephemeral"}` 标记可缓存块：

```python
def _build_review_messages(
    package: EvidencePackage,
    prior_feedback: PriorFeedback | None,
    *,
    enable_cache: bool = False,
) -> list[dict]:
    system_block: dict = {"type": "text", "text": _load_prompt(_REVIEW_PROMPT)}
    evidence_block: dict = {
        "type": "text",
        "text": json.dumps(package.to_dict(), ensure_ascii=False),
    }
    if enable_cache:
        # Anthropic 扩展字段；其他 OpenAI-compatible provider 会静默忽略此字段
        system_block["cache_control"] = {"type": "ephemeral"}
        evidence_block["cache_control"] = {"type": "ephemeral"}

    messages: list[dict] = [{"role": "user", "content": [evidence_block]}]
    if prior_feedback is not None:
        messages.append({
            "role": "user",
            "content": json.dumps(prior_feedback.to_dict(), ensure_ascii=False),
        })
    return messages
```

`enable_cache` 默认 `False`，通过 `--enable-cache` CLI flag opt-in，避免对不支持该字段的 provider 产生意外副作用。

**与 Tracing 的联动**：`AgentRun.cache_hit` 和 `cache_saved_tokens` 由 3.7 节的 tracing 层自动记录，`review_report.json` 的 `tracing.total_cache_saved_tokens` 直接展示节省效果，**无需额外代码**。

**面试讲解**：

> "loop 第二轮的 EvidencePackage 不变，我们把它标记为 cacheable。Anthropic API 在第二轮会命中 prompt cache，命中部分只收 10% 费用。tracing 里能看到 `cache_hit=true` 和 `cache_saved_tokens`，这是 loop 带来的额外收益——不只是质量更好，还更便宜、更快。"

---

### 3.9 Human-in-the-Loop Gate（HITL）

**背景**：Anthropic Managed Agents（`CMA_gate_human_in_the_loop.ipynb`）、OpenAI Agents SDK（显式 `human_in_the_loop` 文档章节）、LangGraph（`interrupts` 机制）三大框架都把 HITL 列为显式能力。我们已经有 `needs_human_review` bucket，只需在 loop 结束后加一个可选的交互暂停门。

**在 pipeline 中的位置**：

```
IterativeHarnessRunner.run() → LoopResult
        │
        ▼
[--hitl 开启时] HITLGate.check(loop_result.ungrounded + needs_human_review)
  → 打印每条 issue 摘要
  → 等待用户输入 y / n / s（confirm / reject / skip）
  → 返回 HumanDecision[]
        │
        ▼
_apply_human_decisions(loop_result, decisions)
  confirm → 移入 findings，confidence 升为 1.0
  reject  → 移入 discarded，reason = "human_rejected"
  skip    → 保留在 needs_human_review（不变）
        │
        ▼
Report（包含 human_decisions 审计字段）
```

**CLI 交互示例**：

```
[HITL Gate] 2 issues need human review.

[1/2] Category: security_sensitive  Confidence: 0.52
  File: src/payment/processor.py  Lines: 45-67
  Summary: SQL query constructed via string concat, potential injection
  Evidence: E-007 (risk_signal: behavior_change)

  Action? [y=confirm / n=reject / s=skip] > y

[2/2] Category: api_change  Confidence: 0.48
  File: src/api/endpoints.py  Lines: 12-15
  Summary: Response field removed without deprecation notice
  Evidence: E-002 (diff_hunk)

  Action? [y=confirm / n=reject / s=skip] > s

[HITL Gate] 1 confirmed, 0 rejected, 1 skipped.
```

**实现草稿**：

```python
# review/hitl.py
from __future__ import annotations
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from code_review_agent.models import ReviewIssue

@dataclass(slots=True)
class HumanDecision:
    issue_id: str
    action: str          # "confirm" | "reject" | "skip"
    timestamp_utc: str

@dataclass(slots=True)
class HITLGate:
    interactive: bool = True   # False 时跳过交互（CI 用）

    def check(
        self,
        issues: list[ReviewIssue],
        *,
        auto_skip: bool = False,
    ) -> list[HumanDecision]:
        if not self.interactive or auto_skip:
            # CI 模式：全部 skip，不触发 input()
            return [
                HumanDecision(
                    issue_id=_issue_id(i),
                    action="skip",
                    timestamp_utc=_now_utc(),
                )
                for i in issues
            ]
        decisions: list[HumanDecision] = []
        total = len(issues)
        print(f"\n[HITL Gate] {total} issue(s) need human review.\n")
        for idx, issue in enumerate(issues, 1):
            _print_issue_summary(idx, total, issue)
            while True:
                raw = input("  Action? [y=confirm / n=reject / s=skip] > ").strip().lower()
                if raw in {"y", "n", "s"}:
                    break
                print("  Please enter y, n, or s.")
            action_map = {"y": "confirm", "n": "reject", "s": "skip"}
            decisions.append(HumanDecision(
                issue_id=_issue_id(issue),
                action=action_map[raw],
                timestamp_utc=_now_utc(),
            ))
        confirmed = sum(1 for d in decisions if d.action == "confirm")
        rejected = sum(1 for d in decisions if d.action == "reject")
        print(f"\n[HITL Gate] {confirmed} confirmed, {rejected} rejected, "
              f"{total - confirmed - rejected} skipped.\n")
        return decisions
```

**CLI 参数**：

```powershell
# 开启 HITL（loop 结束后对 needs_human_review issues 暂停等待确认）
code-review-agent review --repo . --diff changes.patch --out outputs/review \
  --mode hybrid-live --hitl

# CI 环境：auto-skip（不阻塞流水线，仍记录 decisions）
code-review-agent review ... --mode hybrid-live --hitl --no-interactive
```

**HITL 决策写入报告**：

```json
"human_decisions": [
  {"issue_id": "I-003", "action": "confirm",
   "original_bucket": "needs_human_review", "timestamp_utc": "2026-04-29T14:32:01Z"},
  {"issue_id": "I-004", "action": "skip",
   "original_bucket": "needs_human_review", "timestamp_utc": "2026-04-29T14:32:08Z"}
]
```

**为什么对实习面试有价值**：它把"人在回路中"从概念变成了可 demo 的交互行为。面试时可以展示：agent 系统知道自己不确定的地方，不是静默地通过或拒绝，而是主动请求人类裁决，且每条决策都有时间戳审计日志。这正是 Anthropic、OpenAI 当前 responsible agentic behavior 的核心论点。

---

### 3.10 Fake Agent 对 Loop 的确定性支持

`FakeLLMReviewAgent` 和 `FakeLLMCriticAgent` 需要支持 loop 接口，且保持**完全确定性**（供 eval 和 CI 使用）：

**`FakeLLMReviewAgent.review(package, prior_feedback=...)`**：
- `prior_feedback=None`：行为与现有 `_issues_from_risk_signals(package)` 完全一致（第 0 轮退化）。
- `prior_feedback` 不为 None：对 `uncertain_items` 中出现的 issue，把 confidence 乘以 `0.8`（模拟"被批评后保守处理"），其余 issue 不变。

**`FakeLLMCriticAgent.critique(issues, package)`**：
- `confidence < 0.5` → `uncertain`（带固定 reason `"low confidence"`）
- `evidence_ids` 全不在 `package.evidence_index` → `uncertain`（带 reason `"ungrounded evidence"`）
- 其余 → `keep`
- 无 `reject`（fake critic 保守，不主动拒绝）

确定性保证：fake agent 的判断完全基于 `confidence` 数值和 `evidence_index` 查找，没有任何随机性。`max_iter=1` 时 fake loop 输出与当前 `run_fake_hybrid_agents` 完全一致（回归安全）。

---

## 4. 新增 / 修改文件清单

| 文件 | 操作 | 关键变更 |
|---|---|---|
| `src/code_review_agent/models.py` | 修改 | 新增 `UncertainFeedbackItem / PriorFeedback / CritiqueResult`；`AgentRun` 加 `iteration / feedback_hash / retry_count / retry_log` |
| `src/code_review_agent/review/agents.py` | 修改 | `CriticAgent` Protocol 改为 `critique()`；`FakeLLM` 实现 loop 接口；新增 `_retry_with_backoff / _AgentFatalError / _AgentTransientError / _retry_after`；`OpenAICompatibleReviewAgent.review()` 包装重试 |
| `src/code_review_agent/review/verifier.py` | **新增** | `GroundingVerifier / VerifierResult / ground_verify()` |
| `src/code_review_agent/review/loop.py` | **新增** | `IterativeHarnessRunner / LoopResult / IterationRecord`；checkpoint 读写；收敛检测 |
| `src/code_review_agent/review/pipeline.py` | 修改 | `hybrid-fake/live` 分支改为调用 `IterativeHarnessRunner`；fallback 捕获；`max_iter / resume` 透传 |
| `src/code_review_agent/cli.py` | 修改 | `review` 命令加 `--max-iter`（默认 2）和 `--resume` flag |
| `tests/test_review_loop.py` | **新增** | 全部 loop 场景（见第 6 节） |
| `tests/test_review_verifier.py` | **新增** | `ground_verify` 单元测试 |
| `tests/test_review_agents_fake.py` | 修改 | 补充 `critique()` 接口和重试场景测试 |
| `src/code_review_agent/review/hitl.py` | **新增** | `HITLGate`、`HumanDecision` 数据类；`check()` 交互方法；CI auto-skip 模式 |
| `tests/test_review_hitl.py` | **新增** | HITL 场景测试（confirm/reject/skip/auto-skip） |

---

## 5. loop.py 接口草稿

```python
"""Iterative review harness with checkpoint and retry support."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from code_review_agent.models import (
    AgentRun,
    CritiqueResult,
    EvidencePackage,
    PriorFeedback,
    ReviewIssue,
    UncertainFeedbackItem,
)
from code_review_agent.review.agents import CriticAgent, ReviewAgent
from code_review_agent.review.verifier import ground_verify

LOOP_CHECKPOINT_FILENAME = "loop_checkpoint.json"
LOOP_SCHEMA_VERSION = "1.0"


@dataclass(slots=True)
class IterationRecord:
    i: int
    candidate_issues: list[ReviewIssue]
    verified_count: int
    ungrounded_count: int
    critique: CritiqueResult
    feedback_sent: list[UncertainFeedbackItem]

    def to_dict(self) -> dict[str, Any]:
        return {
            "i": self.i,
            "candidate_issue_count": len(self.candidate_issues),
            "verified_count": self.verified_count,
            "ungrounded_count": self.ungrounded_count,
            "keep_count": len(self.critique.keep),
            "uncertain_count": len(self.critique.uncertain),
            "reject_count": len(self.critique.reject),
            "feedback_sent_count": len(self.feedback_sent),
            "agent_runs": [r.to_dict() for r in self.critique.agent_runs],
        }


@dataclass(slots=True)
class LoopResult:
    final_issues: list[ReviewIssue]
    ungrounded_issues: list[ReviewIssue]   # 所有轮次的 ungrounded，汇入 needs_human_review
    agent_runs: list[AgentRun]
    iterations_completed: int
    converged: bool
    fallback_used: bool = False
    fallback_reason: str | None = None


@dataclass(slots=True)
class IterativeHarnessRunner:
    reviewer: ReviewAgent
    critic: CriticAgent
    max_iter: int = 2
    out_dir: Path | None = None         # 若非 None，每轮写 checkpoint

    def run(
        self,
        package: EvidencePackage,
        changed_paths: set[str],
        *,
        resume: bool = False,
    ) -> LoopResult:
        start_i, prior_feedback, records = self._load_checkpoint(resume)
        all_ungrounded: list[ReviewIssue] = []

        for i in range(start_i, self.max_iter):
            # 1. Reviewer
            candidates = self.reviewer.review(package, prior_feedback=prior_feedback)

            # 2. Grounding Verifier（确定性，不调 API）
            vr = ground_verify(candidates, package, changed_paths)
            all_ungrounded.extend(vr.ungrounded)

            # 3. Critic
            critique = self.critic.critique(vr.verified, package)

            # 4. 收敛检测
            feedback_items = [
                UncertainFeedbackItem(
                    issue_id=_issue_id(issue),
                    category=issue.category,
                    critic_reason=reason,
                    original_confidence=issue.confidence,
                )
                for issue, reason in critique.uncertain
            ]
            record = IterationRecord(
                i=i,
                candidate_issues=candidates,
                verified_count=len(vr.verified),
                ungrounded_count=len(vr.ungrounded),
                critique=critique,
                feedback_sent=feedback_items,
            )
            records.append(record)
            converged = _converged(critique, prior_feedback, records)
            self._save_checkpoint(records, converged=converged)

            if converged:
                return LoopResult(
                    final_issues=critique.keep,
                    ungrounded_issues=all_ungrounded,
                    agent_runs=_all_runs(records),
                    iterations_completed=i + 1,
                    converged=True,
                )

            prior_feedback = PriorFeedback(
                iteration=i,
                uncertain_items=feedback_items,
            )

        # max_iter 到达，取最后一轮的 keep
        return LoopResult(
            final_issues=records[-1].critique.keep,
            ungrounded_issues=all_ungrounded,
            agent_runs=_all_runs(records),
            iterations_completed=len(records),
            converged=False,
        )

    def _load_checkpoint(
        self, resume: bool
    ) -> tuple[int, PriorFeedback | None, list[IterationRecord]]:
        if not resume or self.out_dir is None:
            return 0, None, []
        cp_path = self.out_dir / LOOP_CHECKPOINT_FILENAME
        if not cp_path.exists():
            return 0, None, []
        # 反序列化 checkpoint，返回 (start_i, last_feedback, records)
        # 实现略：从 cp["iteration"] 读取轮次，从最后一个 record 还原 PriorFeedback
        ...

    def _save_checkpoint(
        self, records: list[IterationRecord], *, converged: bool
    ) -> None:
        if self.out_dir is None:
            return
        cp = {
            "schema_version": LOOP_SCHEMA_VERSION,
            "iteration": len(records),
            "converged": converged,
            "iterations": [r.to_dict() for r in records],
        }
        (self.out_dir / LOOP_CHECKPOINT_FILENAME).write_text(
            json.dumps(cp, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def _converged(
    critique: CritiqueResult,
    prior_feedback: PriorFeedback | None,
    records: list[IterationRecord],
) -> bool:
    if not critique.uncertain:
        return True
    # issue set 不变：本轮 keep+uncertain 与上轮相同
    if len(records) >= 2:
        prev_ids = _issue_ids_from_record(records[-2])
        curr_ids = _issue_ids_from_record(records[-1])
        if prev_ids == curr_ids:
            return True
    return False
```

---

## 6. 测试策略

| 测试用例 | 文件 | 关键断言 |
|---|---|---|
| `test_single_iter_equals_current_behavior` | `test_review_loop.py` | `max_iter=1` 时 `LoopResult.final_issues` 与现有 `run_fake_hybrid_agents` 输出一致 |
| `test_converges_at_iter_0_when_no_uncertain` | `test_review_loop.py` | fake critic 无 uncertain → `converged=True`，`iterations_completed=1` |
| `test_uncertain_triggers_second_iter` | `test_review_loop.py` | 构造 fake critic 在第 0 轮返回 uncertain → 进入第 1 轮 |
| `test_issue_set_stable_converges_early` | `test_review_loop.py` | 两轮 keep 集合相同 → `converged=True`，loop 提前退出 |
| `test_ungrounded_issues_go_to_ungrounded_list` | `test_review_loop.py` | reviewer 返回无 evidence 的 issue → 出现在 `LoopResult.ungrounded_issues` |
| `test_checkpoint_written_after_each_iter` | `test_review_loop.py` | 两轮结束后 `loop_checkpoint.json` 的 `"iteration"` 字段 = 2 |
| `test_resume_skips_completed_iters` | `test_review_loop.py` | 写入 checkpoint（`iteration=1`），`resume=True` 启动 → `reviewer.review` mock 只被调用 1 次 |
| `test_retry_on_503` | `test_review_agents_fake.py` | mock HTTP 层前两次返回 503 → 第三次成功，`AgentRun.retry_count == 2` |
| `test_no_retry_on_401` | `test_review_agents_fake.py` | mock HTTP 返回 401 → 立即抛 `_AgentFatalError`，不重试 |
| `test_retry_after_header_respected` | `test_review_agents_fake.py` | 429 + `Retry-After: 1` → sleep 调用参数 ≈ 1.0 |
| `test_fallback_to_rules_on_exhausted_retry` | `test_review_pipeline.py` | 3 次重试全失败 → `summary.mode == "hybrid-live/fallback-rules"`，rules findings 不丢失 |
| `test_ground_verify_empty_evidence_ids` | `test_review_verifier.py` | `evidence_ids=[]` 的 issue → `ungrounded` |
| `test_ground_verify_unknown_evidence_id` | `test_review_verifier.py` | `evidence_ids=["E-999"]`（不在 evidence_index）→ `ungrounded` |
| `test_ground_verify_file_not_in_changed` | `test_review_verifier.py` | `file` 不在 `changed_paths` → `ungrounded` |
| `test_agent_run_tracing_fields_populated` | `test_review_loop.py` | loop 完成后 `AgentRun.latency_ms > 0` 且 `token_count_in > 0` |
| `test_tracing_total_latency_aggregated` | `test_review_loop.py` | `LoopResult.tracing.total_latency_ms == sum(per_run latency_ms)` |
| `test_cache_hit_recorded_on_second_iter` | `test_review_loop.py` | fake agent 模拟 `cache_saved_tokens>0`，`AgentRun.cache_hit==True` |
| `test_hitl_confirm_moves_to_findings` | `test_review_hitl.py` | action=confirm → issue confidence=1.0，进入 findings bucket |
| `test_hitl_reject_moves_to_discarded` | `test_review_hitl.py` | action=reject → issue 移入 discarded，reason="human_rejected" |
| `test_hitl_auto_skip_no_input` | `test_review_hitl.py` | `interactive=False` → 全部 skip，不调用 `input()` |

---

## 7. 报告输出变化

`review_report.json` 新增 `loop` 字段：

```json
{
  "summary": {
    "mode": "hybrid-live",
    "finding_count": 3,
    "loop_iterations_completed": 2,
    "loop_converged": true,
    "fallback_used": false,
    "fallback_reason": null
  },
  "loop": {
    "enabled": true,
    "max_iter": 2,
    "iterations_completed": 2,
    "converged": true,
    "checkpoint_path": "outputs/review/loop_checkpoint.json",
    "iterations": [
      {
        "i": 0,
        "candidate_issue_count": 5,
        "verified_count": 4,
        "ungrounded_count": 1,
        "keep_count": 3,
        "uncertain_count": 1,
        "reject_count": 0
      },
      {
        "i": 1,
        "candidate_issue_count": 4,
        "verified_count": 4,
        "ungrounded_count": 0,
        "keep_count": 3,
        "uncertain_count": 0,
        "reject_count": 1
      }
    ]
  }
}
```

Markdown 报告新增简洁摘要（不展开每轮细节）：

```markdown
## Loop Summary

| Metric | Value |
|---|---|
| Mode | hybrid-live |
| Iterations | 2 / 2 |
| Converged | ✓ |
| Fallback | — |
| Total Latency | 4821 ms |
| Total Token In | 3200 |
| Total Token Out | 480 |
| Cache Saved Tokens | 1800 (iter 1 命中) |
| Human Decisions | 1 confirmed / 0 rejected / 1 skipped |

Iteration 0 → 5 candidates, 1 ungrounded, 1 uncertain feedback sent
Iteration 1 → 4 candidates, 0 ungrounded, converged (0 uncertain)
```

`review_report.json` 同步新增 `tracing` 和 `human_decisions` 字段（见 3.7 / 3.9 节）。

---

## 8. CLI 参数变化

```
review_parser.add_argument(
    "--max-iter",
    type=int,
    default=2,
    metavar="N",
    help=(
        "Maximum loop iterations for hybrid modes. "
        "1 = single pass (current behavior). Default: 2."
    ),
)
review_parser.add_argument(
    "--resume",
    action="store_true",
    help=(
        "Resume a hybrid-live loop from the last checkpoint in --out. "
        "No-op if loop_checkpoint.json does not exist."
    ),
)
review_parser.add_argument(
    "--hitl",
    action="store_true",
    help=(
        "Enable Human-in-the-Loop Gate after loop completes. "
        "Prompts for confirm/reject/skip on needs_human_review issues."
    ),
)
review_parser.add_argument(
    "--no-interactive",
    action="store_true",
    help=(
        "Run HITL in auto-skip mode (CI-safe). "
        "Issues are recorded as 'skip' without blocking on input(). "
        "Only meaningful when --hitl is also set."
    ),
)
review_parser.add_argument(
    "--enable-cache",
    action="store_true",
    help=(
        "Add cache_control markers to system_prompt + evidence_package blocks. "
        "Effective with Anthropic API; silently ignored by other providers."
    ),
)
```

对 `rules` 模式，`--max-iter`、`--resume`、`--hitl` 和 `--enable-cache` 均被静默忽略（无 loop）。

---

## 9. 实现顺序（建议）

```
步骤 1  models.py：新增三个 dataclass；AgentRun 加字段
步骤 2  agents.py：_retry_with_backoff / _AgentFatalError / _AgentTransientError；
                  CriticAgent Protocol 加 critique()；FakeLLM 实现
步骤 3  verifier.py：ground_verify()
步骤 4  loop.py：IterativeHarnessRunner（先不做 checkpoint，让 loop 跑通）
步骤 5  tests/test_review_loop.py：单轮退化 + 双轮收敛两个核心测试
步骤 6  pipeline.py：替换 hybrid 分支，接入 IterativeHarnessRunner
步骤 7  cli.py：--max-iter / --resume
─── MVP loop 已可 demo，以下为 harness 可靠性加分项 ───
步骤 8  loop.py：补充 checkpoint 读写（_load_checkpoint / _save_checkpoint）
步骤 9  agents.py：retry 逻辑集成到 OpenAICompatibleReviewAgent.review()
步骤 10 tests：checkpoint 恢复 + retry + fallback 测试
步骤 11 output/review_markdown.py：Loop Summary section
─── 可观测性与体验加分项 ───
步骤 12 models.py / agents.py：AgentRun 加 latency_ms / token_count_in/out 字段；
                                OpenAICompatibleReviewAgent 采集 latency + usage
步骤 13 loop.py / output：聚合 tracing 摘要到 LoopResult.tracing；Markdown Loop Summary 加 Tracing 行
步骤 14 agents.py：_build_review_messages() 加 enable_cache 参数；
                   读取 prompt_cache_hit_tokens 写入 AgentRun.cache_saved_tokens
        cli.py：--enable-cache flag 透传
步骤 15 review/hitl.py：HITLGate / HumanDecision；_apply_human_decisions()；
        pipeline.py / cli.py：--hitl / --no-interactive 接入；
        report 加 human_decisions 字段
```

**做到第 6 步**：loop 可在 demo 中运行，可在面试中展示 2-agent 迭代和收敛。
**做到第 11 步**：断点重传、API 容错、fallback 降级、Loop Summary 报告全部覆盖，harness 可靠性论据完整。
**做到第 15 步**：Tracing、Prompt Caching、HITL 全部落地，覆盖工业级 agent harness 全景，面试论据无懈可击。

---

## 10. 面试讲解要点

用一句话定位：

> "我们的 harness 不只是调一次 API，而是一个有状态的迭代 loop：每轮 Critic 把不确定的 finding 连同原因反馈给 Reviewer，GroundingVerifier 在每轮之前做确定性校验保证 evidence 不幻觉，所有轮次的输入输出持久化到磁盘，API 失败后可以断点继续，每次调用的延迟和 token 消耗都记录在 tracing 里，系统提示和 evidence 用 prompt cache 优化第二轮成本，不确定 issue 可以通过 HITL Gate 交由人类裁决。"

可展示的技术点：

| 技术点 | 对应面试问题 |
|---|---|
| Critic→Refine loop + 收敛检测 | "你的系统有 loop / 自我校验吗？" |
| `GroundingVerifier` 确定性 pre-filter | "怎么防止 agent 幻觉？" |
| `PriorFeedback` 结构化传递（不传裸文本） | "agent 之间怎么通信？" |
| `prompt_hash + feedback_hash` 幂等指纹 | "eval 结果可复现吗？CI 会 flaky 吗？" |
| `_retry_with_backoff` + `Retry-After` | "API 不稳定时怎么处理？" |
| Fallback 不降级 guardrail | "模型挂了你的系统还能用吗？" |
| `loop_checkpoint.json` 断点重传 | "长任务中途失败怎么办？" |
| `max_iter=1` 退化到现有行为 | "向后兼容怎么保证？" |
| `AgentRun.latency_ms / token_count` tracing | "你怎么知道哪一轮慢、哪一轮 token 多？" |
| `cache_control` + `cache_saved_tokens` | "怎么降低 loop 的 API 成本？" |
| `HITLGate` confirm/reject/skip | "agent 不确定时谁来拍板？怎么审计？" |
