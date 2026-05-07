我建议你把这个问题定义成：

> **不要把完整 EvidencePackage 直接塞进 prompt；而是把 EvidencePackage 变成一个可索引、可裁剪、可按需展开的 Evidence Store。LLM 每一轮只拿“当前判断必须用到的证据切片”。**

你现在的项目其实已经很适合这么改，因为你本来就是 evidence-first 架构：`EvidencePackage` 里已经有稳定 evidence id，`ReviewIssue` 也通过 `evidence_ids` 引用证据，而不是把完整 evidence 嵌进 issue；后面还设计了 `ReviewAgent` / `CriticAgent` 协议、prompt export、fake/hybrid agent，以及真实 LLM backend 作为后续增强。

---

## 1. 核心方案：EvidencePackage 不直接进 prompt

现在可能是：

```text
diff + repo_map + changed_entities + risk_signals + hygiene + tests
全部拼成一个 review_agent_prompt
```

这个很容易爆上下文。

建议改成：

```text
EvidencePackage.json     # 完整证据库，存在本地
EvidenceManifest         # 短索引，给 LLM 看
SelectedEvidence         # 本轮真正塞进 prompt 的证据切片
```

也就是说：

```text
完整 evidence
    ↓
建立 evidence_index
    ↓
按 changed file / risk / entity / test relevance 打分
    ↓
只选择 top-K 证据进入 prompt
    ↓
LLM 需要更多证据时，请求 evidence_id
    ↓
harness 再取证据切片进入下一轮
```

这才像 agent。不是一次性把所有上下文喂进去，而是：

```text
observe → ask/retrieve evidence → reason → produce candidate issue → verify → critique
```

---

## 2. 你的项目里最应该新增一个模块：`context_budget.py`

可以新增：

```text
src/code_review_agent/review/context_budget.py
```

负责三件事：

### 第一，估算 token

不用引入 tokenizer，MVP 可以先用粗估：

```python
def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)
```

然后给每个 evidence 加字段：

```python
@dataclass(slots=True)
class EvidenceSlice:
    evidence_id: str
    kind: str
    file: str | None
    priority: float
    token_estimate: int
    content: str
```

### 第二，给 evidence 分优先级

优先级可以这样排：

```text
最高优先级：
1. changed hunk 本身
2. changed entity 的函数 / 类 / 方法签名和局部代码
3. risk signal 对应的 evidence
4. related test 的路径、测试名、相关片段

中优先级：
5. imported_by / imports / public API 影响范围
6. StyleBaseline 摘要
7. hygiene signal 摘要

低优先级：
8. 全量 repo_map
9. 无关文件 hygiene evidence
10. 长 README / docs / unrelated tests
```

你要记住一句话：

> **LLM 做 code review 时，最需要的是“变更附近的高密度上下文”，不是“整个仓库的低密度上下文”。**

### 第三，按预算裁剪

例如默认：

```text
总输入预算：24k tokens

system + instruction:      2k
diff summary:              2k
changed hunks:             6k
changed entity context:    5k
related tests:             4k
risk/style/hygiene:        3k
reserved for next round:   2k
```

实现上可以简单一点：

```python
def select_evidence_for_prompt(package, max_tokens: int) -> list[ReviewEvidence]:
    candidates = score_evidence(package)
    selected = []
    used = 0

    for ev in sorted(candidates, key=lambda x: x.priority, reverse=True):
        cost = estimate_tokens(ev.content)
        if used + cost > max_tokens:
            continue
        selected.append(ev)
        used += cost

    return selected
```

---

## 3. Evidence 要分层：Manifest / Slice / Full

你现在的问题本质是证据没有分层。

建议每条 evidence 支持三种表示：

### L0：Manifest，只放索引

给 LLM 快速知道“有哪些证据”，但不放完整内容：

```json
{
  "id": "entity:src/shop/service.py:create_order",
  "kind": "changed_entity",
  "file": "src/shop/service.py",
  "symbol": "create_order",
  "summary": "Changed function create_order, lines 31-58",
  "token_estimate": 940
}
```

### L1：Slice，放关键片段

真正进入 prompt 的内容：

```json
{
  "id": "diff:src/shop/service.py:35",
  "kind": "diff_hunk",
  "content": "@@ -31,7 +31,11 @@\n def create_order(...):\n+    ...",
  "line_range": [31, 42]
}
```

### L2：Full，完整证据

不默认发给模型，只保存在本地 evidence store：

```json
{
  "id": "repo_map:src/shop/service.py",
  "kind": "repo_map",
  "content": "完整 module summary / imports / classes / functions / methods ..."
}
```

这样 prompt 里默认只放：

```text
Manifest + selected L1 slices
```

而不是完整 L2。

---

## 4. 引入真正的 Agent Loop：让 LLM 可以“要证据”

你说得对，agent 本质不是“调用一次 LLM”，而是一个 loop。你这个项目可以做成下面这样：

```text
Step 1: Deterministic pipeline
parse diff → repo_map → changed_entities → risks → evidence_store

Step 2: Planner / Reviewer
LLM 看 compact context，输出：
- candidate findings
- 还需要的 evidence_ids
- 不确定点

Step 3: Evidence Retriever
程序根据 evidence_ids 取证据切片

Step 4: Reviewer second pass
LLM 基于新增证据输出 ReviewIssue

Step 5: Grounding Verifier
程序检查：
- evidence_id 是否存在
- file 是否在 changed files 里
- line 是否和 changed hunk/entity 有 overlap
- issue 是否缺证据

Step 6: Critic
另一个 critic agent 只看 candidate issue + used evidence，决定保留、降级、丢弃

Step 7: Final report
findings / needs_human_review / discarded
```

你可以把它做成最多 2～3 轮，不要无限循环：

```python
for round_idx in range(max_rounds):
    response = reviewer.review(context)
    
    if response.evidence_requests:
        extra = retrieve_evidence(response.evidence_requests)
        context.add(extra)
        continue

    break
```

这样就很像真正的 agent harness 了。

---

## 5. LLM 输出不要只允许 finding，还要允许 evidence request

你可以定义一个结构：

```json
{
  "candidate_findings": [
    {
      "category": "test_gap",
      "severity": "medium",
      "file": "src/shop/service.py",
      "line_start": 35,
      "line_end": 42,
      "message": "The changed behavior in create_order is not covered by related tests.",
      "evidence_ids": [
        "diff:src/shop/service.py:35",
        "test_discovery:tests/test_service.py"
      ],
      "confidence": 0.82
    }
  ],
  "evidence_requests": [
    {
      "reason": "Need to inspect related tests for create_order.",
      "evidence_id": "test_discovery:tests/test_service.py",
      "preferred_level": "slice"
    }
  ],
  "uncertainties": [
    "Need to confirm whether this function is public API."
  ]
}
```

这里的关键是：
**LLM 不能自由说“我需要看看整个项目”，只能请求已有 evidence_id 或受控 query。**

比如允许：

```text
request_evidence_by_id
request_related_tests
request_symbol_context
request_importers
```

不允许：

```text
read arbitrary file
scan whole repo
use internet
```

这样你的项目会显得很“工程化”，不是套壳调用 API。

---

## 6. 长 evidence 的处理：优先结构化压缩，不要直接 LLM 摘要

对于代码 review，很多 evidence 不应该用 LLM 摘要，因为摘要可能漏掉 bug。更推荐**确定性压缩**。

例如 RepoMap 不要塞完整内容，而是压成：

```json
{
  "file": "src/shop/service.py",
  "imports": ["decimal.Decimal", "shop.models.Order"],
  "public_symbols": [
    {
      "name": "create_order",
      "kind": "function",
      "line_range": [31, 58],
      "signature": "create_order(user_id: str, items: list[Item]) -> Order",
      "docstring_present": true
    }
  ],
  "imported_by": [
    "tests/test_service.py",
    "src/shop/api.py"
  ]
}
```

测试文件也不要整文件塞进去，而是只塞：

```text
- related test file path
- test function names
- 和 changed entity 名字匹配的测试片段
- 如果没有匹配测试，明确写 none
```

例如：

```json
{
  "id": "test_discovery:src/shop/service.py:create_order",
  "kind": "related_tests",
  "content": {
    "related_test_files": ["tests/test_service.py"],
    "matched_test_functions": [],
    "reason": "tests/test_service.py imports create_order, but no test function name contains create_order"
  }
}
```

这比把整个测试文件发给 LLM 更省上下文，而且更稳定。

---

## 7. 你可以把 prompt 改成“受约束审查器”

不要写：

```text
Here is all evidence, review the code.
```

而是写：

```text
You are a constrained code review agent.

You may only produce findings supported by evidence_ids.
If evidence is insufficient, request more evidence instead of guessing.
Do not report style-only issues.
Every finding must include:
- file
- line range
- category
- severity
- confidence
- evidence_ids
```

然后给它：

```text
1. PR / diff compact summary
2. changed files
3. changed entities
4. risk signals
5. evidence manifest
6. selected evidence slices
7. output schema
```

这和你现有的“每条 finding 都必须有 evidence、filter 阻止无证据 issue、低置信度降级”的方向是一致的。你的设计文档里 Phase 11 已经有 missing evidence、invalid evidence id、低置信度、line 与 hunk/entity 无关、纯风格偏好、duplicate issue 等过滤规则，这部分可以直接作为 LLM 输出后的 verifier。

---

## 8. 推荐你按这个顺序改

### 第一阶段：先解决上下文爆炸

新增：

```text
review/context_budget.py
review/evidence_store.py
```

实现：

```text
EvidenceManifest
EvidenceSlice
select_evidence_for_prompt()
estimate_tokens()
score_evidence()
```

先不接真实 LLM，只让 `--export-prompts` 导出的 prompt 变短。

验收标准：

```text
同一个大 patch：
旧 prompt 可能 80k tokens
新 prompt 控制在 16k / 24k / 32k 以内
同时 findings 不明显下降
```

---

### 第二阶段：加 evidence request loop

新增：

```text
AgentRequest
AgentResponse
EvidenceRequest
```

把 `ReviewAgent.review(package)` 改成更真实的：

```python
class ReviewAgent(Protocol):
    def review(self, context: AgentContext) -> AgentResponse: ...
```

其中 `AgentContext` 不是完整 package，而是：

```python
@dataclass(slots=True)
class AgentContext:
    manifest: EvidenceManifest
    selected_evidence: list[ReviewEvidence]
    previous_requests: list[EvidenceRequest]
    round_index: int
```

---

### 第三阶段：接真实 LLM backend

你可以新增：

```text
review/llm_backend.py
```

支持 OpenAI-compatible API：

```python
class LLMBackend(Protocol):
    def complete_json(self, messages: list[dict], schema_name: str) -> dict: ...
```

然后：

```text
FakeLLMReviewer
OpenAICompatibleReviewer
```

都实现同一个接口。

这样面试时可以讲：

> 我的系统不是依赖某一个模型，而是把 LLM 放在受约束的 reviewer / critic 位置。证据构建、证据裁剪、grounding verification、eval oracle 都是模型外部的 deterministic harness。

这比“我调用了大模型做 code review”高级很多。

---

## 9. 最推荐的最终架构

你可以把项目升级成这句话：

> **Evidence-first interactive code review agent: it builds a local evidence store, lets the LLM request bounded evidence slices, and verifies every finding against deterministic grounding rules before reporting.**

对应架构：

```text
Diff Parser
   ↓
RepoMap / Test Discovery / Hygiene
   ↓
Evidence Store
   ↓
Context Budgeter + Evidence Selector
   ↓
Reviewer Agent
   ↕ evidence request loop
Evidence Retriever
   ↓
Candidate Findings
   ↓
Grounding Verifier
   ↓
Critic Agent
   ↓
Review Filter
   ↓
Final Report + Eval
```

这能同时解决两个问题：

1. **上下文太长**：不再全量塞 evidence，而是 evidence manifest + selected slices + on-demand retrieval。
2. **不像 agent**：加入 bounded evidence request loop，让 LLM 多轮交互地审查，但每轮都被 evidence id 和 verifier 约束。

我认为这是你这个项目下一步最自然、也最适合写进简历的升级点。
