# Code Review Agent Harness 2.0 项目方案

> 日期：2026-04-24

---

## 1. 定位

`code-review-agent` 是一个面向 AI Coding 工作流的**本地 PR 预审 harness**。

它在 Codex / Cursor / Claude Code 生成的改动进入 PR 之前，先把 diff 解析成结构化证据、上下文和 guardrails，再由 deterministic baseline 或受约束 Agent 输出带证据的 review report。

核心主张：

> 每条 finding 必须有可追踪证据。没有证据的问题不能作为正式 issue 输出。

---

## 2. 为什么不做普通 AI Review Bot

`diff → prompt → LLM comments` 有三个结构性问题：

1. **同源失败**：用同家族模型既生成又 review，correlated failure 导致错误相互回响而不抵消（Zietsman 2026）。
2. **误报难控**：裸 LLM 追求高召回，signal-to-noise ratio 极低；能保持沉默才是稀缺能力（Pereira et al. 2026）。
3. **无法评估**：用 LLM-as-judge 评估 LLM review，对 prompt 微小变化高度敏感，测量的是 prompt artifact 而不是真实能力（Zhao et al. 2026）。

本项目的答案：deterministic 工具收集证据和 guardrails，受约束 agent 做语义判断，schema + verifier 控制噪音，planted-bug oracle 做评估。规则层不是产品主语，而是 baseline、回归锚点和 agent 输出的校验支架。

---

## 3. 架构

```
Input
  repo path  ·  diff/patch  ·  optional hygiene  ·  optional config

Deterministic Tool Layer
  diff parser  ·  AST parser  ·  import extractor  ·  symbol extractor
  test discovery  ·  hygiene classifier  ·  risk classifier

Context Layer
  RepoMap  ·  ChangedEntity[]  ·  EvidencePackage
  HygieneEvidence  ·  RiskSignal[]  ·  StyleBaseline

Agent Layer（MVP 用 Fake / baseline，Post-MVP 强化 live agent）
  ReviewAgent  ·  CriticAgent  ·  ReportAgent

Harness Layer
  prompt builder  ·  schema validator  ·  confidence policy
  evidence validator  ·  deduplicator  ·  filter

Output
  review_report.json  ·  review_report.md
  metrics.json（eval 时）
```

---

## 4. 命令

```powershell
code-review-agent map     --repo .  --out .cra/map
code-review-agent hygiene --repo .  --out .cra/hygiene
code-review-agent review  --repo .  --diff changes.patch  --out .cra/review
code-review-agent eval    --cases examples/eval_cases     --out .cra/eval
```

| Command | 主要输出 |
|---|---|
| `map` | `repo_map.json`, `repo_map.md` |
| `hygiene` | `project_hygiene.json`, `PROJECT_ARTIFACTS.md`, `uncertain_queue.md` |
| `review` | `review_report.json`, `review_report.md` |
| `eval` | `metrics.json`, `eval_report.md`, `case_results.json` |

`summary` 命令合并进 `map`，作为 `--format markdown` 的输出形式，不单独维护。

---

## 5. Review Pipeline

```
1.  parse diff
2.  build / load RepoMap
3.  extract changed entities
4.  discover related tests
5.  load hygiene signals
6.  run risk classification
7.  build EvidencePackage
8.  run deterministic baseline / guardrail findings
9.  run ReviewAgent（可选，MVP 用 Fake 或跳过）
10. run CriticAgent / ReviewFilter
11. deduplicate, downgrade weak findings
12. write JSON + Markdown report
```

---

## 6. LLM 在 harness 里的位置

LLM 不接管整个 review，只做三件有限的语义任务：

**ReviewAgent**：输入是 EvidencePackage，不是裸 diff。输出必须引用 evidence id，不能基于未提供的事实推断。`[]` 是合法输出，代表 No Finding。

**CriticAgent**：二次验证 ReviewAgent 的 finding——evidence id 是否存在、问题是否在 changed lines、是否纯风格意见、是否重复。这步是误报控制的核心。

**ReportAgent**：只做 JSON → Markdown 转换。不修改 file / line / severity / evidence 等事实字段，把"事实生成"和"语言表达"分开，降低幻觉风险。

---

## 7. Agent Harness 体现在哪里

| 层 | 作用 |
|---|---|
| Tool Use | Agent 通过 DiffParser / RepoMap / RiskClassifier 拿结构化结果，不凭空读 diff |
| Context | 只传 changed entity 附近代码 + symbol/import/test 摘要，控制 token budget，默认执行 metadata redaction |
| Schema | 所有 LLM 输出必须符合 ReviewIssue / CriticDecision schema，不通过就重试或降级 |
| Evidence | 验证每条 issue 的 evidence id 是否存在且可追踪到文件/行号 |
| Confidence | 低置信度 → `needs_human_review`；无 evidence → 丢弃；无问题 → `No Finding` |
| Evaluation | deterministic oracle 量化 precision / recall / false positives / no-finding accuracy |

---

## 8. Design Rationale

每个核心设计决策都有 2026 年论文直接支撑：

| 决策 | 依据 | 关键论点 |
|---|---|---|
| Deterministic evidence 先于 LLM | Zietsman 2026 (2603.25773) | 同家族 LLM 既生成又 review → correlated failure，错误相互回响而不抵消 |
| `no_finding_accuracy` 作为核心指标 | Pereira et al. 2026 (2603.11078) | 高召回 agent signal-to-noise ratio 极低；能保持沉默才是稀缺能力 |
| planted-bug + line-range oracle | Zhao et al. 2026 (2604.16790) | LLM judge 测量 prompt artifact；deterministic oracle 才可重复 |
| `design_constraint_violation` 检测 | Yu et al. 2026 (2604.05955) | test pass rate 严重高估 patch 质量；不到一半 pass 级别 patch 满足设计约束 |
| risk tags 作为 review rubric | Li et al. 2026 (2604.14261) | 显式 rubric 约束起草阶段比 single-pass 自由生成更能避免表面化评论 |
| metadata redaction policy | Mitropoulos et al. 2026 (2603.18740) | PR title/commit message 通过 framing effect 系统性偏置 LLM 的安全判断 |
| FakeLLM 区分 `recall_biased` / `precision_biased` | Zietsman 2026 | cross-strategy verifier 打破相关性失败；同策略 reviewer+critic 是 correlated failure 的来源 |

---

## 9. 核心数据模型

全部在 `models.py` 中定义，使用 `@dataclass(slots=True)` + `to_dict()`。

### RepoMap

```python
@dataclass(slots=True)
class RepoMap:
    root: str
    files: list[str]
    python_modules: list[PythonModuleSummary]
    imports: dict[str, list[str]]
    imported_by: dict[str, list[str]]
    related_tests: dict[str, list[str]]
    style_baseline: StyleBaseline | None
```

### PythonModuleSummary

```python
@dataclass(slots=True)
class PythonModuleSummary:
    path: str
    module_docstring: str | None
    imports: list[str]
    classes: list[SymbolSummary]
    functions: list[SymbolSummary]
    methods: list[SymbolSummary]
```

### SymbolSummary

```python
@dataclass(slots=True)
class SymbolSummary:
    path: str
    symbol_type: str          # "class" | "function" | "method"
    name: str
    qualified_name: str
    line_start: int
    line_end: int
```

### StyleBaseline

```python
@dataclass(slots=True)
class StyleBaseline:
    """轻量仓库风格基线，由 RepoMapBuilder 收集。
    所有字段均可为空/零，不阻塞主流程。
    total_public_functions < 5 时，risk 模块跳过所有 design_constraint 检测。
    """
    docstring_coverage_ratio: float      # 0.0–1.0，public 函数 docstring 覆盖率
    dominant_import_style: str           # "absolute" | "relative" | "mixed"
    test_naming_pattern: str | None      # "test_*" | "*_test" | None
    dominant_exception_handling: str     # "raise" | "return_none" | "mixed"
    total_public_functions: int          # 样本总数，评估基线可信度用

    def to_dict(self) -> dict:
        return {
            "docstring_coverage_ratio": self.docstring_coverage_ratio,
            "dominant_import_style": self.dominant_import_style,
            "test_naming_pattern": self.test_naming_pattern,
            "dominant_exception_handling": self.dominant_exception_handling,
            "total_public_functions": self.total_public_functions,
        }
```

### DiffLine / DiffHunk / DiffFileChange

```python
@dataclass(slots=True)
class DiffLine:
    line_type: str              # "context" | "added" | "removed"
    old_lineno: int | None
    new_lineno: int | None
    content: str

@dataclass(slots=True)
class DiffHunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    section_header: str
    lines: list[DiffLine]

@dataclass(slots=True)
class DiffFileChange:
    old_path: str | None
    new_path: str | None
    change_type: str            # "added" | "modified" | "deleted" | "renamed"
    hunks: list[DiffHunk]
```

### ChangedEntity

```python
@dataclass(slots=True)
class ChangedEntity:
    path: str
    entity_type: str            # "module" | "class" | "function" | "method"
    name: str
    qualified_name: str
    line_start: int
    line_end: int
    hunk_ids: list[str]
```

当前实现：RepoMap Builder 已落地到 `context/repo_map.py`，ChangedEntity extraction 已落地到 `review/changed_entity.py`。`methods` 单独存储，避免 method 归属混入 class/function 列表；无法精确映射时退化为 module-level entity。

Phase 5/6 实现补充：Risk classification 已落地到 `review/risk.py`，EvidencePackage builder 已落地到 `review/evidence.py`。

Phase 7/8 实现补充：Deterministic baseline 已落地到 `review/rules.py`，pipeline 已落地到 `review/pipeline.py`，CLI 已支持 `code-review-agent review --repo <repo> --diff <patch> --out <out>`。当前 MVP 能在无 LLM/API key 环境下输出 `review_report.json` / `review_report.md`；这里的 baseline 用于回归、guardrail 和 agent harness 对照，不代表项目最终要做规则扫描器。

Phase 9/10 实现补充：Micro eval metrics 已落地到 `eval/metrics.py`，并加入 test gap / error handling / doc-only 三个 micro fixtures；Report output 已落地到 `output/json_report.py` 和 `output/review_markdown.py`，`review_report.json` 带 `schema_version`，Markdown 章节顺序固定。

Phase 11/12 实现补充：正式 filter 已落地到 `review/filter.py` 并接入 `review/pipeline.py`，`discarded` 分区只写入 JSON，记录 `filter_reason`。Fake/Hybrid agent interface 已落地到 `review/agents.py`，CLI 支持 `--mode hybrid-fake` 与 `--export-prompts`，prompt export 会写入 prompt hash 和 redacted input JSON；真实 LLM backend 仍保持后置。

Phase 13/14 实现补充：内置 planted-bug eval 已落地到 `eval/cases.py` 和 `eval/runner.py`，CLI 支持 `code-review-agent eval --cases examples/eval_cases --out <out> --mode rules|hybrid-fake|all`，输出 `metrics.json`、`case_results.json` 和 `eval_report.md`。`examples/eval_cases` 已扩展为 7 个可复现 cases，用于开发回归和 demo 指标；外部 benchmark adapter 属于 Post-MVP。`examples/demo_repo` 已打磨为可复现 demo shop 项目，README 已加入架构、demo 命令、sample review、eval 指标表和当前限制。

### RiskSignal

```python
@dataclass(slots=True)
class RiskSignal:
    tag: str
    confidence: float
    reason: str
    evidence_ids: list[str]
```

### AgentRun

```python
@dataclass(slots=True)
class AgentRun:
    agent_name: str
    model: str | None
    prompt_hash: str | None
    input_evidence_ids: list[str]
    output_issue_ids: list[str]
    fallback_used: bool
```

---

## 10. Risk Tags

| Tag | 触发条件 |
|---|---|
| `api_change` | public function/class signature 变更；`__init__.py` exports 变更 |
| `behavior_change` | 非测试 Python 文件有逻辑行增删，changed entity 是 function/method |
| `test_gap` | 非测试代码变更，related tests 存在但无测试文件在 patch 中 |
| `config_change` | `pyproject.toml` / `.github/workflows/*` / `setup.cfg` 等配置文件变更 |
| `dependency_change` | dependencies section 或 requirements-like 文件变更 |
| `error_handling_change` | hunk 含 `try/except/raise/finally`，或删除了 `raise`，或新增 bare `except` |
| `security_sensitive` | hunk 含 auth/token/password/secret/path/subprocess/eval/exec |
| `doc_only` | patch 只改了 Markdown/docs |
| `experiment_artifact` | 新增文件路径匹配 experiment/debug/demo/tmp 模式，或 hygiene 判断为过程资产 |
| `design_constraint_violation` | 见下 |

`design_constraint_violation` 只在以下条件全部满足时触发（低误报优先）：
- `StyleBaseline.total_public_functions >= 5`
- 新增/修改 public function 缺少 docstring，且仓库 `docstring_coverage_ratio >= 0.70`
- 或新增测试文件命名不符合 `test_naming_pattern`
- 或新增 import 风格与 `dominant_import_style` 不一致，且该风格占比 `>= 0.80`（"mixed" 不触发）

---

## 11. Metadata Redaction Policy

EvidencePackage 传给 LLM 或导出 prompt 时默认执行：

| 字段 | 处理 |
|---|---|
| diff hunk / changed file path / AST symbols / risk tags / hygiene signals | 保留（核心证据） |
| PR title / PR description | redact |
| commit message | redact |
| author / reviewer metadata | redact |

---

## 12. Eval 设计

### 目录结构（Plan B，扁平结构）

```
examples/eval_cases/
  demo_repo/               # 共用基线 repo（planted bug 已植入）
    src/shop/
    tests/
  patches/
    case_001_test_gap.patch
    case_002_api_change.patch
    case_003_error_handling.patch
    case_004_artifact_pollution.patch
    case_005_no_finding_doc_only.patch
    case_006_no_finding_test_only.patch
    case_007_design_constraint.patch
  ground_truth/
    case_001_test_gap.json
    case_002_api_change.json
    case_003_error_handling.json
    case_004_artifact_pollution.json
    case_005_no_finding_doc_only.json
    case_006_no_finding_test_only.json
    case_007_design_constraint.json
```

每个 case 独立 `before/` `after/` 目录（Plan A）作为 post-MVP 增强预留，不进入 MVP。

### Ground Truth 格式

```json
{
  "case_id": "case_001_test_gap",
  "patch": "patches/case_001_test_gap.patch",
  "expected_findings": [
    {
      "category": "test_gap",
      "file": "src/shop/service.py",
      "line_range": [30, 45],
      "severity": "medium",
      "key_bug": true
    }
  ],
  "expected_no_finding": false
}
```

### Deterministic Oracle

```
finding.file == ground_truth.file
AND finding.category == ground_truth.category
AND line_range_overlap(finding, ground_truth) >= threshold
```

不用 LLM judge，不用自然语言相似度。相同输入重复运行必须得到相同结果。

### 指标

| 指标 | 含义 |
|---|---|
| `precision` | 输出 finding 中真实问题占比 |
| `recall` | ground truth 问题被命中占比 |
| `false_positives_per_pr` | 每个 patch 平均误报数 |
| `key_bug_inclusion` | 关键 bug 是否被命中 |
| `no_finding_accuracy` | 无问题 patch 能否保持沉默 |
| `evidence_coverage` | finding 中带有效 evidence 的比例 |

### Threshold Profiles

| Profile | 用途 |
|---|---|
| `strict` | 高 precision，低误报，适合提交前质量门 |
| `balanced` | 默认，平衡 recall 与 spurious findings |
| `recall` | 更积极发现问题，适合探索性 review |

Eval 报告用表格展示 profile frontier：

| Variant | Profile | Recall | Spurious/PR | Precision | No-finding Accuracy |
|---|---|---|---|---|---|

### Ablation

| Variant | 描述 |
|---|---|
| `rules_only` | deterministic baseline / guardrail，只用于回归和对照 |
| `prompt_only` | 只把 diff 给 LLM |
| `evidence_backed` | RepoMap + risk + evidence + optional LLM |

---

## 13. Demo Repo 结构

```
examples/demo_repo/
  src/shop/
    __init__.py  models.py  service.py  discounts.py  api.py
  tests/
    test_service.py  test_discounts.py
  scripts/
    seed_data.py
  docs/
    design.md
  prompt_experiment.py      ← hygiene: experiment_artifact
  debug_order_flow.py       ← hygiene: debug_artifact
  generated_report.json     ← hygiene: generated_output
```

---

## 14. 报告结构

```markdown
# Review Report

## Summary
## Findings
## Needs Human Review
## Changed Files
## Changed Entities
## Risk Signals
## Evidence Index
```

Findings 在最前。每条 finding 必须包含 file / line / severity / confidence / evidence list。No Finding 要说明检查了什么、为什么没有输出。

当前 Phase 10/11/12 输出链路已包含上述章节，并写入 `review_report.json` / `review_report.md`。`discarded`、`agent_runs` 和 `prompt_exports` 只进入 JSON；Markdown 主报告继续保持 README-friendly。Phase 13/14 补充了 eval 输出：`metrics.json`、`case_results.json` 和 `eval_report.md`。

---

## 15. 产品边界

**MVP 内**：Python · 本地 CLI · 只读 · unified diff · AST · changed entity · RepoMap · hygiene signal · deterministic risk/guardrail · fake/live-compatible agent harness · evidence-backed report · 内置 planted-bug eval。

**MVP 外**：外部 benchmark adapter · GitHub webhook · PR comment 自动发布 · 自动修复 · 多语言 · MCP server · Draft→Ground→Critic 三阶段强化 · `references.py`（call graph，post-MVP）。

---

## 16. 简历叙事

英文：

> Built an evidence-first local code review agent harness for AI-generated patches. The tool parses unified diffs, extracts changed functions and classes with Python AST, builds repository context, and packages traceable evidence for constrained reviewer / critic agents. Deterministic checks serve as baseline and guardrails rather than the product endpoint. Evaluation uses a built-in planted-bug corpus with a deterministic line-range oracle rather than LLM-as-a-judge to track precision, recall, spurious-findings rate, and no-finding accuracy.

中文：

> 实现了一个面向 AI Coding 工作流的本地 code review agent harness。先解析 diff、提取 changed entity、构建 RepoMap 和 evidence package，再让受约束 reviewer / critic agent 在 schema 和 verifier 约束下输出 review report。确定性规则是 baseline 和 guardrail，不是最终产品主语。评估使用内置 planted-bug cases + deterministic oracle，不依赖 LLM judge。

面试时强调：为什么不是 API wrapper、如何控制 LLM 误报、如何设计 evidence schema、如何把 diff hunk 映射到函数/类、如何发现测试缺口、如何评估 review agent。

---

## 17. 参考资料

### 行业信号

- GitHub Octoverse 2025: https://github.blog/news-insights/octoverse/
- Stack Overflow Developer Survey 2025: https://survey.stackoverflow.co/2025/ai
- DORA 2025: https://blog.google/innovation-and-ai/technology/developers-tools/dora-report-2025/
- GitHub Copilot code review: https://docs.github.com/en/copilot/concepts/agents/code-review
- CodeRabbit: https://www.coderabbit.ai/
- Qodo: https://docs.qodo.ai/

### 关键学术论文

| 论文 | arXiv | 对应设计决策 |
|---|---|---|
| CR-Bench: Evaluating the Real-World Utility of AI Code Review Agents (Pereira et al., 2026) | 2603.11078 | `no_finding_accuracy` 作为核心指标；precision-recall trade-off frontier |
| The Specification as Quality Gate (Zietsman, 2026) | 2603.25773 | deterministic evidence 先于 LLM；correlated failure 防御；cross-strategy verifier |
| Does Pass Rate Tell the Whole Story? (Yu et al., 2026) | 2604.05955 | `design_constraint_violation` tag；pass rate 高估 patch 质量 |
| Bias in the Loop: Auditing LLM-as-a-Judge for SE (Zhao et al., 2026) | 2604.16790 | planted-bug oracle；不用 LLM judge |
| ReviewGrounder: Rubric-Guided, Tool-Integrated Agents (Li et al., 2026) | 2604.14261 | risk tags 作为 review rubric；Draft→Ground 两阶段（post-MVP） |
| Measuring and Exploiting Contextual Bias in LLM ACR (Mitropoulos et al., 2026) | 2603.18740 | metadata redaction；framing bias 防御 |
