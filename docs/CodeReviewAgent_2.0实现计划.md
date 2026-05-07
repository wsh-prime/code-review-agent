# Code Review Agent Harness 2.0 实现计划

> 日期：2026-04-24

---

## 1. 原则

**只做 review agent harness，不做大而全 agent。** 面试时有价值的是"能把 context、evidence、误报控制、agent 约束和 eval 做出来"，而不是"接了一个 API"。规则层只作为 deterministic baseline / guardrail，不是项目主语。

**零第三方运行时依赖。** 标准库：`ast` `pathlib` `json` `dataclasses` `re` `difflib` `subprocess`。真实 LLM backend 后置。

**每个模块跟着测试走。** 新模块上线前测试先通。

**默认只读。** 所有命令只写 `--out` 目录，不修改被分析仓库。

---

## 2. 当前状态

已完成（不需要重做）：

- Python package skeleton、CLI 入口
- `models.py` 基础 dataclass
- `hygiene/`：scanner、evidence、classifier、taxonomy、llm_classifier、planner
- 输出 Markdown/JSON
- 基础测试

真正缺的：

- `context/repo_map.py`：RepoMap 和 StyleBaseline
- `review/diff_parser.py`：unified diff → 结构化 hunks
- `review/changed_entity.py`：hunk → function/class/method
- `review/risk.py`：deterministic risk tags
- `review/evidence.py`：EvidencePackage builder
- `review/rules.py`：deterministic baseline / guardrail findings
- `review/pipeline.py`：串起来的 review 命令
- `eval/`：benchmark + deterministic oracle

---

## 3. 目录结构

```
src/code_review_agent/
  cli.py
  models.py

  context/
    __init__.py
    repo_map.py
    test_discovery.py
    # references.py — post-MVP，call graph 轻量版；MVP 阶段由 repo_map.imported_by 覆盖

  hygiene/
    scanner.py  evidence.py  classifier.py
    llm_classifier.py  planner.py  taxonomy.py

  review/
    __init__.py
    diff_parser.py
    changed_entity.py
    risk.py
    evidence.py
    rules.py
    pipeline.py
    filter.py
    agents.py           # Protocol + FakeLLM
    prompts/
      review_agent.md
      critic_agent.md

  output/
    __init__.py
    json_report.py
    review_markdown.py
    hygiene_markdown.py

  eval/
    __init__.py
    cases.py
    metrics.py
    runner.py
```

---

## 4. 执行顺序

```
Phase 0   文档冻结 + README 定位
Phase 1   models.py 升级
Phase 2   Diff Parser
Phase 3   Minimal RepoMap Builder
Phase 4   Changed Entity Extraction
Phase 5   Risk Classification
Phase 6   Evidence Package Builder
Phase 7   Rules-only Review
Phase 8   Review Pipeline CLI
Phase 9   Micro Eval Benchmark
Phase 10  Markdown/JSON 输出完善
Phase 11  Review Filter / Critic
Phase 12  Fake/Hybrid Agent Interface（Protocol + FakeLLM）
Phase 13  Full Eval Benchmark
Phase 14  Demo Polish
```

不要先做：真实 LLM SDK、GitHub PR comment、自动修复、多语言 AST、Draft→Ground→Critic 重构。

---

## 5. Phase 0：文档冻结

**目标**：方向固定，不再变动，开始写代码。

- [x] 在 README 写一句话定位：evidence-first local PR quality gate for AI-generated patches。
- [x] 在 README 加一行 Design Rationale 链接到项目方案第 8 节。
- [x] 确认命令名：`map` / `hygiene` / `review` / `eval`，`summary` 合并进 `map`。
- [x] 更新 `CodeReviewAgent_TODO.md`，标记旧方向已调整。

完成标准：README 可读，开发顺序明确，旧方案与新方案关系说清楚。

---

## 6. Phase 1：核心数据模型升级

**目标**：先定数据结构，后写逻辑。

**新增到 `models.py`**：

```
SymbolSummary
PythonModuleSummary
RepoMap
StyleBaseline      # 见方案第 9 节完整 dataclass
DiffLine
DiffHunk
DiffFileChange
ChangedEntity
RiskSignal
EvidencePackage（或用 dict，具体结构见方案第 12 节示例）
AgentRun
```

**扩展已有模型**：

- `ReviewEvidence`：加 `id` / `kind` / `source`
- `ReviewIssue`：加 `confidence` 和 `evidence_ids`
- `ReviewIssue` 不嵌套完整 `ReviewEvidence`，完整证据统一放在 `EvidencePackage.evidence_index`

**测试**：`pytest tests/test_models.py -v`

测试点：
- 每个 dataclass 使用 `slots=True`
- 每个模型有 `to_dict()`，输出稳定 JSON-friendly dict
- nested model 正确序列化
- `ReviewIssue` 能携带 `confidence` 和 `evidence_ids`
- `ReviewIssue.evidence_ids` 可被后续 filter 校验
- `StyleBaseline` 为空/零时不阻塞主流程

**完成标准**：
- [x] 所有新增模型可导入
- [x] `to_dict()` 测试通过
- [x] `python -m pytest tests/test_models.py -v` 通过

---

## 7. Phase 2：Diff Parser

**目标**：解析 unified diff，产出结构化 changed files 和 hunks。

**新增文件**：

```
src/code_review_agent/review/diff_parser.py
tests/test_review_diff_parser.py
```

支持格式：`diff --git a/path b/path` / `--- a/path` / `+++ b/path` / `@@ -old,count +new,count @@ section`，以及 added / deleted / modified / renamed 四种文件变更类型。

`DiffLine` 记录：`line_type`（context/added/removed）、`old_lineno`、`new_lineno`、`content`。

错误处理：空 diff 给出清晰错误；malformed hunk 跳过并记录 warning；binary diff 记录 file change，不进入 hunk parsing。

**完成标准**：
- [x] 能读取 `examples/demo_repo/demo.patch`
- [x] 输出 changed files 和 hunks，行号正确

---

## 8. Phase 3：Minimal RepoMap Builder

**目标**：为 Python 仓库构建 changed entity mapping 所需的最小机器可读上下文。StyleBaseline 第一版允许为空或只包含轻量字段，避免 RepoMap 阶段过重。

**新增文件**：

```
src/code_review_agent/context/repo_map.py
src/code_review_agent/context/test_discovery.py
tests/test_context_repo_map.py
tests/test_context_test_discovery.py
```

**`repo_map.py` 第一版负责**：

- 复用 hygiene scanner 的 ignore 规则。
- 扫描 Python 文件。
- 用 `ast.parse()` 提取 module docstring。
- 用 `ast.parse()` 提取 imports。
- 用 `ast.parse()` 提取 classes / functions / methods。
- 记录 symbol `line_start` / `line_end`。
- 建立最小 `imports` map。
- `StyleBaseline` 允许为空，不阻塞主流程；当前实现已收集 docstring 覆盖率、import 风格、测试命名风格，异常处理模式暂为 `mixed`。

**暂缓到后续增强**：

- 更精细的 `imported_by` 反向图（当前已有基础本地模块反查）。
- 更精细的 public 函数 docstring 覆盖率策略（当前已有轻量统计，跳过测试文件）。
- import 风格占比阈值统计。
- 异常处理模式统计。

**`test_discovery.py` 第一版负责**：

- 路径匹配：`tests/test_<module>.py` / `test_<name>.py` / `<name>_test.py`
- 轻量 import + symbol name 关联
- 输出 `related_tests: dict[str, list[str]]`

**CLI**：

```powershell
code-review-agent map --repo examples/demo_repo --out outputs/map
```

输出：`outputs/map/repo_map.json` + `outputs/map/repo_map.md`

**完成标准**：
- [x] 能对 demo repo 输出 `repo_map.json`
- [x] Python symbol 行号可用于 changed entity mapping
- [x] style_baseline 为空时不影响主流程

实现记录：`src/code_review_agent/context/repo_map.py`、`context/test_discovery.py` 和 `map` CLI 已落地；`PythonModuleSummary` 新增 `methods` 字段，避免方法归属混入 classes/functions。

---

## 9. Phase 4：Changed Entity Extraction

**目标**：把 diff hunk 映射到函数/类/方法或 module-level change。

**新增文件**：

```
src/code_review_agent/review/changed_entity.py
tests/test_review_changed_entity.py
```

映射规则：

- hunk added/modified lines 落在 function/method 范围内 → 映射到最内层 symbol
- 落在 class body 但不在 method → 映射到 class
- 落在 import / constant / module docstring → 映射到 module
- 文件删除或无法解析 AST → file-level entity（当前 `ChangedEntity` schema 暂无 reason 字段）

第一版不处理：复杂 nested function、decorator 精细归属、语法错误文件的 AST（退化到 module-level）。

**完成标准**：
- [x] 每个 hunk 至少映射到一个 entity
- [x] 无法精确映射时不崩溃
- [x] 输出包含 hunk id 和 line range

实现记录：`src/code_review_agent/review/changed_entity.py` 已落地；同一 hunk 中 module-level 和 symbol-level 变更会分别保留，多个 hunk 命中同一实体时合并 `hunk_ids`。

---

## 10. Phase 5：Risk Classification

**目标**：用确定性规则给 changed entities 和 files 打 risk tags。

**新增文件**：

```
src/code_review_agent/review/risk.py
tests/test_review_risk.py
```

支持的 tags 和触发规则见项目方案第 10 节。

`design_constraint_violation` 触发条件（三条之一满足即触发，但 `total_public_functions < 5` 时全部跳过）：
- [x] 新增/修改 public function 缺少 docstring，且仓库 `docstring_coverage_ratio >= 0.70`
- [x] 新增测试文件命名不符合 `test_naming_pattern`（pattern 存在时）
- [x] 新增 import 风格与 `dominant_import_style` 不一致，且该风格占比 `>= 0.80`（当前 RepoMap 只有全量单一风格时才给出非 `mixed`，因此保守触发）

每个 `RiskSignal` 输出：`tag` / `confidence` / `reason` / `evidence_ids`

**完成标准**：
- [x] `test_gap` 能在 demo patch 中触发
- [x] `doc_only` patch 不输出 code risk
- [x] `design_constraint_violation` 只在低误报规则满足时触发

实现记录：`src/code_review_agent/review/risk.py` 已落地，所有 Phase5 tag 均有第一版确定性规则；输出仅为 `RiskSignal`，正式 finding 留给 Phase7 rules。

---

## 11. Phase 6：Evidence Package Builder

**目标**：把 diff、RepoMap、changed entities、risk tags、hygiene signals 汇总成 ReviewAgent 可消费的结构化上下文。

**新增文件**：

```
src/code_review_agent/review/evidence.py
tests/test_review_evidence.py
```

每条 evidence 有稳定 id，格式：

```
diff:src/shop/service.py:35
entity:src/shop/service.py:create_order
risk:test_gap:src/shop/service.py
test_discovery:tests/test_service.py
hygiene:src/shop/debug_flow.py
```

Metadata redaction 规则（见项目方案第 11 节）：PR title/commit message/author 不进入 EvidencePackage，本地 diff MVP 通常没有这些字段，但 schema 预留 redacted 标记位。

**完成标准**：
- [x] 每个 changed file 能生成 EvidencePackage
- [x] risk signals 和 evidence id 互相引用
- [x] JSON 可序列化

实现记录：`src/code_review_agent/review/evidence.py` 已落地，生成 diff/entity/risk/test_discovery/hygiene 五类 `ReviewEvidence`；`find_missing_evidence_ids()` 预留给 Phase8 inline filter 和 Phase11 正式 filter 复用。

---

## 12. Phase 7：Rules-only Review

**目标**：在没有真实 LLM 的情况下跑通 review pipeline，并提供 deterministic baseline / guardrail。它用于回归、对照和证据链验证，不代表最终要做规则扫描器。

**新增文件**：

```
src/code_review_agent/review/rules.py
tests/test_review_rules.py
```

第一版只做四条高信号规则：

**Rule 1 — Test Gap**：非测试代码变更 + related tests 存在 + patch 没有改任何 related test → `test_gap` / medium / confidence 0.75–0.9

**Rule 2 — Process Artifact Added To Mainline**：patch 新增文件 + 文件在 `src/` 或根目录 + hygiene 判断为 experiment/debug/demo/tmp/generated → `experiment_artifact` / low-medium / confidence 0.7–0.9

**Rule 3 — Broad Exception Handling**：added lines 含 `except Exception` 或 bare `except` + 非测试 Python 文件 → `error_handling` / medium / confidence 0.7–0.85

**Rule 4 — Dependency Change**：dependency file 变更 + 无 lock/test/config 说明 → `dependency_change` / low / confidence 0.6–0.75，默认放入 `needs_human_review`

**完成标准**：
- [x] 不依赖 LLM 也能输出 review report
- [x] demo case 能触发 `test_gap` 和 `experiment_artifact`
- [x] no-finding patch 能保持无正式 finding

实现记录：`src/code_review_agent/review/rules.py` 已落地，输出 `RulesReviewResult(findings, needs_human_review)`。当前正式 findings 覆盖 `test_gap`、`experiment_artifact` 和新增 broad exception；`dependency_change` 默认进入 `needs_human_review`。

---

## 13. Phase 8：Review Pipeline CLI

**目标**：把前面模块串成可用的 `review` 命令。

**新增文件**：

```
src/code_review_agent/review/pipeline.py
tests/test_review_pipeline.py
```

更新：`src/code_review_agent/cli.py`

**命令**：

```powershell
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/patches/case_001.patch --out outputs/review
# 可选参数：
--hygiene outputs/hygiene/project_hygiene.json
--repo-map outputs/map/repo_map.json
--mode rules|hybrid-fake
```

Phase 8 第一版只需支持 `--mode rules` 作为 baseline；Phase 12 已补上 `--mode hybrid-fake` 来展示 agent harness 路径。

**Pipeline 步骤**：

```
parse diff
build / load repo map
load optional hygiene
extract changed entities
classify risks
build evidence packages
run rules
inline filter（仅两条：丢弃 evidence_ids 为空的 finding，丢弃 file 不在 changed_files 中的 finding）
write report
```

> Phase 8 只做两条内联过滤。完整 filter 逻辑（confidence threshold、duplicate 合并、downgrade）在 Phase 11 正式实现，Phase 8 不依赖 Phase 11。

**完成标准**：
- [x] 一条命令可以跑完 demo patch
- [x] 输出 changed files / changed entities / risk tags / findings
- [x] 无 LLM 环境可运行
- [x] 默认不修改 repo

实现记录：`src/code_review_agent/review/pipeline.py` 和 `code-review-agent review` CLI 已落地。Phase 10 后，报告写入已委托给 `output/json_report.py` 和 `output/review_markdown.py`。

---

## 14. Phase 9：Micro Eval Benchmark

**目标**：在 deterministic baseline review pipeline 跑通后，立刻加入最小回归集，避免 risk/baseline/filter 后续调整时行为漂移。

**新增或复用文件**：

```
examples/eval_cases/patches/case_001_test_gap.patch
examples/eval_cases/patches/case_002_error_handling.patch
examples/eval_cases/patches/case_003_no_finding_doc_only.patch
examples/eval_cases/ground_truth/case_001_test_gap.json
examples/eval_cases/ground_truth/case_002_error_handling.json
examples/eval_cases/ground_truth/case_003_no_finding_doc_only.json
src/code_review_agent/eval/metrics.py
tests/test_eval_metrics.py
```

**第一版只做 3 个 case**：

- `test_gap`
- `error_handling`
- `no_finding_doc_only`

**完成标准**：
- [x] micro eval 可以在本地快速运行
- [x] oracle 使用 file equality、category equality、line range overlap
- [x] no-finding case 单独计算准确性
- [x] 不依赖 LLM judge

实现记录：`src/code_review_agent/eval/metrics.py` 已落地，新增 3 个 micro eval patch / ground truth fixtures。当前 Phase 9 只实现 metrics 和 fixtures，完整 `eval` CLI 留给 Phase 13。

---

## 15. Phase 10：Markdown/JSON 输出完善

**目标**：让报告适合 README 截图和面试展示。

**新增文件**：

```
src/code_review_agent/output/json_report.py
src/code_review_agent/output/review_markdown.py
tests/test_output_review_markdown.py
```

Markdown 结构：

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

- Findings 在最前
- 每条 finding 必须有 file / line / severity / confidence / evidence list
- No Finding 要说明检查了什么、为什么没有输出
- Evidence Index 不要过长

**完成标准**：
- [x] report 适合放进 README
- [x] JSON 字段稳定
- [x] Markdown snapshot 测试通过

实现记录：`src/code_review_agent/output/json_report.py` 和 `output/review_markdown.py` 已落地；`review/pipeline.py` 已改为调用 output 模块写 `review_report.json` / `review_report.md`。Phase 11/12 后，当前 JSON schema 版本为 `1.1`。

---

## 16. Phase 11：Review Filter / Critic

**目标**：正式实现误报控制层。

**新增文件**：

```
src/code_review_agent/review/filter.py
tests/test_review_filter.py
```

过滤/降级规则：

- missing evidence
- evidence id 不存在
- confidence 低于阈值
- file 不在 changed files，也无 related evidence
- line 与 changed hunk/entity 完全无关
- message 是纯风格偏好
- duplicate issues

输出分区：`findings` / `needs_human_review` / `discarded`（`discarded` 只写 JSON，不在 Markdown 主报告展示）

**完成标准**：
- [x] filter 能阻止无证据 issue
- [x] low confidence issue 进入 needs_human_review
- [x] duplicate finding 被合并

实现记录：`src/code_review_agent/review/filter.py` 已正式接入 pipeline。过滤层会丢弃 missing/invalid evidence、纯风格偏好、无 changed-file 关联的 issue；会把低置信度、行号与 changed hunk/entity 无关、file 不在 changed files 但仍有相关 evidence 的 issue 降级到 `needs_human_review`；duplicate finding 会合并 evidence ids 并保留较高置信度。`discarded` 只进入 JSON 报告。

---

## 17. Phase 12：Fake/Hybrid Agent Interface

**目标**：在 pipeline 和正式 filter 稳定后加入可选 fake/hybrid agent，展示 agent harness 接口和防幻觉机制，但不让核心功能依赖真实 API。

**新增文件**：

```
src/code_review_agent/review/agents.py
src/code_review_agent/review/prompts/review_agent.md
src/code_review_agent/review/prompts/critic_agent.md
tests/test_review_agents_fake.py
```

**Protocol**：

```python
class ReviewAgent(Protocol):
    def review(self, package: EvidencePackage) -> list[ReviewIssue]: ...

class CriticAgent(Protocol):
    def filter(self, issues: list[ReviewIssue], package: EvidencePackage) -> list[ReviewIssue]: ...
```

**FakeLLM 策略**（必须区分，用于 eval 展示 correlated failure）：

| 策略 | 行为 |
|---|---|
| `recall_biased_reviewer` | 倾向提出候选 finding，模拟高召回 reviewer |
| `precision_biased_critic` | 倾向质疑、降级或过滤，模拟高精度 critic |
| `same_strategy` | reviewer 和 critic 用同一策略，展示 correlated failure 风险 |
| `cross_strategy` | reviewer 和 critic 用不同策略，展示 harness 的过滤价值 |

**Prompt Export**（无 API 时也能展示上下文准备）：

```powershell
code-review-agent review --repo . --diff changes.patch --out outputs/review --export-prompts
```

输出 `outputs/review/prompts/review_agent_input.json` + `review_agent_prompt.md`。

真实 LLM backend 作为后续 Phase，不进入 MVP。

**完成标准**：
- [x] 支持 `--mode rules` 和 `--mode hybrid-fake`
- [x] Fake LLM finding 经过 evidence validator
- [x] invalid evidence id 被过滤或降级
- [x] prompt 文件有 hash

实现记录：`src/code_review_agent/review/agents.py` 已落地，包含 `ReviewAgent` / `CriticAgent` Protocol、recall-biased fake reviewer、precision-biased fake critic、`same_strategy` / `cross_strategy` harness，以及 prompt hash/export 工具。`code-review-agent review` 已支持 `--mode hybrid-fake` 和 `--export-prompts`，导出 `review_agent_input.json`、`review_agent_prompt.md`、`critic_agent_input.json`、`critic_agent_prompt.md`。

---

## 18. Phase 13：Full Eval Benchmark

**目标**：用内置 planted-bug benchmark 做可复现回归和 demo 指标。必须使用 deterministic oracle，不使用 LLM judge。它不是外部权威 benchmark，外部 benchmark adapter 留到 Post-MVP。

**新增文件**：

```
examples/eval_cases/demo_repo/src/shop/...
examples/eval_cases/patches/case_001_test_gap.patch ... case_007_design_constraint.patch
examples/eval_cases/ground_truth/case_001_test_gap.json ... case_007_design_constraint.json
src/code_review_agent/eval/__init__.py
src/code_review_agent/eval/cases.py
src/code_review_agent/eval/metrics.py
src/code_review_agent/eval/runner.py
tests/test_eval_metrics.py
```

**Deterministic Oracle**：

```
finding.file == ground_truth.file
AND finding.category == ground_truth.category
AND line_range_overlap(finding, ground_truth) >= threshold
```

**命令**：

```powershell
code-review-agent eval --cases examples/eval_cases --out outputs/eval --mode rules
```

**Threshold Profiles**：`strict` / `balanced` / `recall`（见项目方案第 12 节）

**完成标准**：
- [x] 至少 5 个 eval cases
- [x] 至少 2 个 no-finding cases（doc-only 和 test-only）
- [x] eval 命令可跑通
- [x] oracle 使用 planted bug + line range overlap
- [x] eval 不依赖 LLM judge
- [x] 报告展示 strict/balanced/recall frontier 表
- [x] README 可以展示一张指标表
- [x] 能对比 deterministic baseline 与 fake/evidence-backed agent variant

实现记录：`src/code_review_agent/eval/cases.py` / `runner.py` 已落地，`code-review-agent eval` 支持 `--mode rules`、`--mode hybrid-fake`、`--mode all`。这里的 `rules` 是 deterministic baseline，不是项目主线终点。`examples/eval_cases` 已包含 7 个 planted-bug fixtures，其中 `case_005_no_finding_doc_only` 和 `case_006_no_finding_test_only` 用于衡量 no-finding accuracy。输出为 `metrics.json`、`case_results.json` 和 `eval_report.md`。

---

## 19. Phase 14：Demo Polish

**目标**：让项目适合投简历、录屏、面试讲解。

**README 必须包含**：

- 一句话定位
- 为什么不是普通 AI Review Bot（三行内讲清楚）
- 架构图
- demo 命令
- sample report 截图或文本片段
- eval 指标表
- 当前限制（Python/local CLI 优先，真实 LLM 为可选 backend，GitHub comment / auto-fix 属于 Post-MVP）

**Demo 命令（必须可复现）**：

```powershell
pip install -e ".[dev]"
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent map     --repo examples/demo_repo --out outputs/demo-map
code-review-agent review  --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
code-review-agent eval    --cases examples/eval_cases --out outputs/demo-eval --mode all
```

**面试讲解顺序**：

1. AI coding 生成 PR 越来越多，问题是信任和误报
2. 裸 LLM review 是 `diff → comments`，不可控，且同源失败
3. 我的系统：`diff + repo → evidence → constrained agent → verified report`
4. 展示 test gap case 的 finding + evidence index
5. 展示 eval metrics 和 frontier 表
6. 解释 hygiene 模块如何识别过程资产污染

**完成标准**：
- [x] README 能在 3 分钟内讲清楚项目
- [x] demo 命令可复现
- [x] 报告里有至少一个高质量 finding 和一个 No Finding case
- [x] eval 输出能支撑"不是 toy"的叙事

实现记录：`examples/demo_repo` 已打磨为小型 demo shop 项目，包含 `src/shop` 主代码、`tests`、`docs`、`scripts` 和 hygiene 可识别的过程资产。`examples/demo_repo/patches` 覆盖 test gap、artifact pollution、error handling、doc-only no finding 和 test-only no finding。README 已加入架构图、demo 命令、sample review、eval 指标表和当前限制。

---

## 20. 测试文件对照表

| 模块 | 测试文件 |
|---|---|
| `context/repo_map.py` | `tests/test_context_repo_map.py` |
| `context/test_discovery.py` | `tests/test_context_test_discovery.py` |
| `review/diff_parser.py` | `tests/test_review_diff_parser.py` |
| `review/changed_entity.py` | `tests/test_review_changed_entity.py` |
| `review/risk.py` | `tests/test_review_risk.py` |
| `review/evidence.py` | `tests/test_review_evidence.py` |
| `review/rules.py` | `tests/test_review_rules.py` |
| `review/pipeline.py` | `tests/test_review_pipeline.py` |
| `output/review_markdown.py` | `tests/test_output_review_markdown.py` |
| `review/agents.py` | `tests/test_review_agents_fake.py` |
| `review/filter.py` | `tests/test_review_filter.py` |
| `eval/metrics.py` | `tests/test_eval_metrics.py` |

---

## 21. 验收标准

达到以下全部标准，项目可作为简历主版本：

- [x] `hygiene` 能识别过程资产并输出报告
- [x] `map` 能输出 Python RepoMap
- [x] `review` 能解析 diff 并定位 changed entities
- [x] `review` 能输出 risk tags
- [x] `review` 能输出 evidence-backed findings 或 No Finding
- [x] 每条 finding 都有 evidence
- [x] 无 LLM/API key 环境可运行
- [x] 至少 5 个 eval cases，至少 2 个 no-finding cases
- [x] eval 使用 deterministic oracle，不依赖 LLM judge
- [x] eval 能输出 precision / recall / false positives / key bug inclusion
- [x] eval 能展示 strict/balanced/recall 的 trade-off frontier
- [x] README 有可复现 demo 命令和 sample report

---

## 22. 后续增强（MVP 后再考虑）

**真实 Agent Harness**：OpenAI-compatible API，API key 只读环境变量，prompt hash，model 记录，timeout/fallback，schema validation。reviewer 和 critic 可选使用不同模型族作为 correlated failure 防御增强。

**Draft → Ground → Critic Pipeline**：DraftAgent 输出 CandidateFinding，GroundingVerifier 绑定 evidence id，CriticFilter 做最终过滤。不进入 MVP，避免过早增加 pipeline 状态和测试复杂度。

**外部 Benchmark Adapter**：优先考虑 AACR-Bench 的 Python 子集，把外部 PR / comment 标注转成当前 `ground_truth.json` 风格，再用 deterministic file/category/line overlap oracle 评估。Martian Code Review Bench 可作为工具横评参考，但不能把 LLM judge 作为唯一标准。

**GitHub Integration**：输入 PR URL，拉取 diff，dry-run report，可选发布 PR comment。

**MCP / Tool Protocol**：暴露 repo_map / review report / hygiene scan，供 Codex/Cursor 调用。

**多语言**：JavaScript/TypeScript、Go、Java。建立在 evidence-first review harness 稳定后。

---

## 23. 风险与控制

| 风险 | 控制 |
|---|---|
| 范围过大 | 先完成 Python + local CLI + deterministic baseline + fake/live-compatible agent harness |
| 误报太多 | 只输出高证据 finding，低置信度降级 |
| LLM 成为项目瓶颈 | MVP 不依赖真实 API |
| Demo 不可信 | 做 eval cases 和 no-finding case |
| Eval 被质疑 | planted bug + deterministic oracle，不用 LLM judge |
| LLM 被 metadata 诱导 | prompt/export 默认 metadata redaction |
| 文档多于代码 | 每个 Phase 都有可运行命令和测试 |
| AST 映射复杂 | 先处理常见 function/class/method，失败时 module-level fallback |

---

## 24. 最小可演示版本

如果时间极紧，只需要：

```
review/diff_parser.py
context/repo_map.py
review/changed_entity.py
review/risk.py
review/evidence.py
review/rules.py
review_report.md + json
3 个 demo patches
deterministic eval oracle
2 个 no-finding cases
```

最小 demo 命令：

```powershell
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
```

最小 demo 报告必须展示：changed files / changed entity / `test_gap` risk / evidence / no-finding case。
