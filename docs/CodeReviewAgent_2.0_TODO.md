# Code Review Agent Harness 2.0 TODO

> 日期：2026-04-25  
> 主线：evidence-first review agent harness → deterministic guardrails → 受约束真实 Agent  
> 依据：`CodeReviewAgent_2.0项目方案.md` · `CodeReviewAgent_2.0实现计划.md`

**规则**：新模块必须同步加测试。MVP 只写 `--out` 目录，不修改被分析仓库，不依赖真实 LLM。

---

## 执行顺序

```
1  核心数据模型      models.py 升级
2  Diff Parser       unified diff → 结构化 hunks
3  RepoMap Builder   Python AST → symbols + imports + tests
4  Changed Entity    hunk → function/class/method
5  Risk              deterministic risk tags
6  Evidence          EvidencePackage builder
7  Baseline Review   deterministic baseline / guardrail，无 LLM 也能跑
8  Pipeline CLI      review 命令串起全链路
9  Micro Eval        3 个 case，pipeline 跑通后立刻加，防回归
10 Report Output     Markdown/JSON 报告
11 Filter            误报控制层
12 Fake Agent        Protocol + FakeLLM
13 Full Eval         7 个 case + frontier profiles
14 Demo Polish       README + demo 命令
```

做到第 8 步：最小可演示 review harness。  
做到第 9 步：有防回归保护。  
做到第 13 步：有可复现内置 eval；外部 benchmark adapter 留到 Post-MVP。

---

## Phase 0 — 方向冻结

- [x] 确认主线命令：`map` / `hygiene` / `review` / `eval`
- [x] `summary` 不进 MVP，后续作为 `map --format markdown` 的输出
- [x] 项目方案第 8 节加入 Design Rationale 表
- [x] 真实 LLM 和 Draft→Ground→Critic 不进 MVP
- [x] `README.md` 更新一句话定位：evidence-first local PR quality gate for AI-generated patches

---

## Phase 1 — 核心数据模型

文件：`src/code_review_agent/models.py` · `tests/test_models.py`

**新增**：

- [x] `SymbolSummary` — path / symbol_type / name / qualified_name / line_start / line_end
- [x] `PythonModuleSummary` — path / module_docstring / imports / classes / functions
- [x] `RepoMap` — root / files / python_modules / imports / imported_by / related_tests / style_baseline
- [x] `StyleBaseline` — 允许为空/零，`total_public_functions < 5` 时跳过 design_constraint 检测
- [x] `DiffLine` — line_type / old_lineno / new_lineno / content
- [x] `DiffHunk` — old_start / old_count / new_start / new_count / section_header / lines
- [x] `DiffFileChange` — old_path / new_path / change_type / hunks
- [x] `ChangedEntity` — path / entity_type / name / qualified_name / line_start / line_end / hunk_ids
- [x] `RiskSignal` — tag / confidence / reason / evidence_ids
- [x] `EvidencePackage` — changed files / changed entities / risk signals / evidence index
- [x] `AgentRun` — agent_name / model / prompt_hash / input_evidence_ids / output_issue_ids / fallback_used

**扩展已有**：

- [x] `ReviewEvidence`：已有 id / kind / source / message（本次已完成）
- [x] `ReviewIssue`：已加 confidence / evidence_ids（本次已完成）

**完成标准**：
- [x] `python -m pytest tests/test_models.py -v` 全通
- [x] 所有模型可从 `code_review_agent.models` 导入
- [x] `StyleBaseline` 为空时不阻塞主流程

---

## Phase 2 — Diff Parser

文件：`src/code_review_agent/review/diff_parser.py` · `tests/test_review_diff_parser.py`

- [x] 解析 `diff --git` / `--- a/` / `+++ b/` / `@@ -old,count +new,count @@`
- [x] 支持 modified / added / deleted / renamed（轻量）
- [x] 每行记录 old_lineno 和 new_lineno
- [x] 空 diff 给出清晰错误；binary diff 只记录 file change，不进 hunk parsing
- [x] malformed hunk 跳过并记录 warning

**完成标准**：
- [x] 单文件 / 多文件 / added / deleted diff 测试通过
- [x] hunk 行号可用于 report 定位

---

## Phase 3 — Minimal RepoMap Builder

文件：`src/code_review_agent/context/repo_map.py` · `context/test_discovery.py` · 对应测试

第一版目标：能支撑 changed entity mapping，StyleBaseline 可以为空。

- [x] 复用 hygiene scanner 的 ignore 规则
- [x] `ast.parse()` 提取：module docstring / imports / classes / functions / methods / line_start / line_end
- [x] 建立 `imports` map 和基础 `imported_by` map
- [x] `test_discovery.py`：路径匹配 `tests/test_<module>.py` / `test_<name>.py` / `<name>_test.py`
- [x] `StyleBaseline` 轻量收集（可为空，不阻塞主流程）：docstring 覆盖率 / import 风格 / 测试命名风格 / 异常处理模式

**暂缓**：完整 imported_by 反向图 / import 风格偏好统计 / 异常处理模式统计（StyleBaseline 允许零值）

CLI：`code-review-agent map --repo <repo> --out <out>` → `repo_map.json` + `repo_map.md`

**完成标准**：
- [x] demo repo 能生成 `repo_map.json`
- [x] symbol line range 可用于 diff hunk 映射
- [x] 解析失败文件不导致整个 map 崩溃

实现记录：`map` CLI 已输出 `repo_map.json` / `repo_map.md`；`PythonModuleSummary` 增加 `methods` 字段，避免把方法混入 class/function 列表；解析失败或非 UTF-8 Python 文件会跳过该模块摘要但保留文件级扫描结果。

---

## Phase 4 — Changed Entity Extraction

文件：`src/code_review_agent/review/changed_entity.py` · `tests/test_review_changed_entity.py`

- [x] hunk added/modified lines 落在 function/method 范围 → 映射到最内层 symbol
- [x] 落在 class body 但不在 method → class
- [x] 落在 import / constant / module docstring → module
- [x] 新增函数 → 映射到新 symbol；删除函数 → 至少保留 file-level entity
- [x] AST 解析失败 → fallback module-level（当前 `ChangedEntity` schema 暂无 reason 字段）

**完成标准**：
- [x] 每个 hunk 至少有一个 changed entity
- [x] 测试覆盖 function / method / class / module 四类映射

实现记录：`extract_changed_entities()` 会合并同一实体的多个 hunk id；同一 hunk 内如果同时改到 module-level 常量和函数/方法，会保留多个 changed entity。

---

## Phase 5 — Risk Classification

文件：`src/code_review_agent/review/risk.py` · `tests/test_review_risk.py`

支持的 tags（触发规则见项目方案第 10 节）：

`api_change` · `behavior_change` · `test_gap` · `config_change` · `dependency_change` · `error_handling_change` · `security_sensitive` · `doc_only` · `experiment_artifact` · `design_constraint_violation`

`design_constraint_violation` 触发条件（`total_public_functions < 5` 时全部跳过）：
- [x] 新增/修改 public function 缺 docstring，且仓库 `docstring_coverage_ratio >= 0.70`
- [x] 新增测试文件命名不符合 `test_naming_pattern`
- [x] 新增 import 风格与 `dominant_import_style` 不一致，且占比 `>= 0.80`（当前 RepoMap 只有全量单一风格时才给出非 `mixed`，等价于保守触发）

**完成标准**：
- [x] `test_gap` 能在 demo patch 中触发
- [x] `doc_only` patch 不输出 code risk
- [x] `design_constraint_violation` 只在低误报规则满足时触发

实现记录：`review/risk.py` 已支持 `api_change` / `behavior_change` / `test_gap` / `config_change` / `dependency_change` / `error_handling_change` / `security_sensitive` / `doc_only` / `experiment_artifact` / `design_constraint_violation`。每个 `RiskSignal` 引用稳定 evidence id，不直接生成 issue。

---

## Phase 6 — Evidence Package Builder

文件：`src/code_review_agent/review/evidence.py` · `tests/test_review_evidence.py`

- [x] 为每类信号生成 stable evidence id：
  - `diff:src/shop/service.py:35`
  - `entity:src/shop/service.py:create_order`
  - `risk:test_gap:src/shop/service.py`
  - `test_discovery:tests/test_service.py`
  - `hygiene:src/shop/debug_flow.py`
- [x] issue 只能引用 evidence_index 中存在的 id
- [x] evidence source 可追踪到文件/行号或系统检查
- [x] prompt/export 默认 redact PR title / description / commit message / author（本地 diff MVP 通常无此类字段，schema 预留标记位即可）

**完成标准**：
- [x] EvidencePackage 可 JSON 序列化
- [x] invalid evidence id 能被 filter 捕捉

实现记录：`review/evidence.py` 已生成 diff/entity/risk/test_discovery/hygiene 五类 `ReviewEvidence`，并提供 `find_missing_evidence_ids()` 供 Phase11 filter 或 Phase8 inline filter 复用。

---

## Phase 7 — Rules-only Review

文件：`src/code_review_agent/review/rules.py` · `tests/test_review_rules.py`

四条 baseline guardrails（只做高信号，宁少勿滥）：

| Rule | 条件 | tag | severity | confidence |
|---|---|---|---|---|
| Test Gap | 非测试代码改动 + related tests 存在 + patch 未改任何相关测试 | `test_gap` | medium | 0.75–0.9 |
| Process Artifact Added | patch 新增文件 + 在 `src/` 或根目录 + hygiene 判断为过程资产 | `experiment_artifact` | low-medium | 0.7–0.9 |
| Broad Exception | added lines 含 `except Exception` 或 bare `except` + 非测试文件 | `error_handling_change` | medium | 0.7–0.85 |
| Dependency Change | 依赖文件变更 + 无 lock/test/config 说明 | `dependency_change` | low | 0.6–0.75 → `needs_human_review` |

**完成标准**：
- [x] 不依赖 LLM 也能输出 review report
- [x] `test_gap` 和 `experiment_artifact` 能在 demo case 中触发
- [x] no-finding patch（doc-only / test-only）不输出正式 finding

实现记录：`review/rules.py` 已落地。它是 deterministic baseline / guardrail，用于回归、对照和 agent 输出校验，不是项目最终产品主语。`test_gap` / `experiment_artifact` / broad `error_handling_change` 会生成 baseline finding；`dependency_change` 进入 `needs_human_review`；doc-only patch 保持无正式 finding。

---

## Phase 8 — Review Pipeline CLI

文件：`src/code_review_agent/review/pipeline.py` · `tests/test_review_pipeline.py` · 更新 `cli.py`

命令：

```powershell
code-review-agent review --repo <repo> --diff <patch> --out <out>
# 可选：--repo-map <repo_map.json>  --hygiene <project_hygiene.json>  --mode rules|hybrid-fake
```

第一版只支持 `--mode rules`。

Pipeline 步骤：

```
parse diff → build/load repo map → load optional hygiene →
extract changed entities → classify risks → build evidence packages →
run rules → inline filter（两条：丢弃 evidence_ids 为空 / file 不在 changed_files）→
write report
```

**完成标准**：
- [x] 一条命令跑完 demo patch
- [x] 输出 changed files / changed entities / risk tags / findings / evidence index
- [x] 无 LLM 环境可运行，默认不修改 repo

实现记录：`review/pipeline.py` 和 `review` CLI 已落地。命令输出 `review_report.json` / `review_report.md`，Phase 8 仅做两条 inline filter：丢弃 `evidence_ids` 为空的 issue，以及丢弃 `file` 不在 changed files 中的 issue。

---

## Phase 9 — Micro Eval Benchmark

文件：eval case fixtures + `src/code_review_agent/eval/metrics.py` · `tests/test_eval_metrics.py`

先做 3 个 case，pipeline 跑通后立刻加，用于防回归：

| Case | 类型 |
|---|---|
| `case_001_test_gap` | 应有 finding |
| `case_002_error_handling` | 应有 finding |
| `case_003_no_finding_doc_only` | 应保持沉默 |

Oracle：`file == ground_truth.file AND category == ground_truth.category AND line_range_overlap >= threshold`，不用 LLM judge。

**完成标准**：
- [x] micro eval 本地快速运行（< 5s）
- [x] no-finding case 单独计算准确性
- [x] risk / rules / filter 任意调整后 micro eval 能发现回归

实现记录：`eval/metrics.py` 已落地，提供 deterministic oracle：file equality、category equality、line range overlap，并支持 no-finding accuracy。已加入 3 个 micro eval fixtures：`case_001_test_gap`、`case_002_error_handling`、`case_003_no_finding_doc_only`。

---

## Phase 10 — Report Output

文件：`src/code_review_agent/output/json_report.py` · `output/review_markdown.py` · `tests/test_output_review_markdown.py`

Markdown 结构（顺序固定）：

```
# Review Report
## Summary
## Findings
## Needs Human Review
## Changed Files
## Changed Entities
## Risk Signals
## Evidence Index
```

- Findings 在最前，每条必须有 file / line / severity / confidence / evidence list
- No Finding 要说明检查了什么、为什么没有输出
- Evidence Index 保持简短

**完成标准**：
- [x] sample report 可直接放进 README
- [x] JSON 字段稳定，Markdown 关键字符串测试通过

实现记录：`output/json_report.py` 与 `output/review_markdown.py` 已落地，`review_report.json` 增加 `schema_version`，Markdown 固定输出 Summary / Findings / Needs Human Review / Changed Files / Changed Entities / Risk Signals / Evidence Index。`review/pipeline.py` 已改为使用 output 模块。

---

## Phase 11 — Review Filter

文件：`src/code_review_agent/review/filter.py` · `tests/test_review_filter.py`

过滤/降级规则：

- [x] missing evidence → 丢弃
- [x] evidence id 不存在 → 丢弃
- [x] confidence 低于阈值 → `needs_human_review`
- [x] file 不在 changed files 且无 related evidence → 过滤
- [x] line 与 changed hunk/entity 完全无关 → 降级
- [x] duplicate issues → 合并

输出分区：`findings` / `needs_human_review` / `discarded`（`discarded` 只写 JSON）

**完成标准**：
- [x] filter 能阻止无证据 issue
- [x] low confidence issue 进入 needs_human_review
- [x] duplicate finding 被合并

实现记录：`review/filter.py` 已升级为正式误报控制层，输出 `FilterResult(findings, needs_human_review, discarded)`；`discarded` 记录 `filter_reason` 并只写入 JSON。`review/pipeline.py` 已接入正式 filter，报告 summary 增加 `discarded_count`。

---

## Phase 12 — Fake/Hybrid Agent Interface

文件：`src/code_review_agent/review/agents.py` · `prompts/review_agent.md` · `prompts/critic_agent.md` · `tests/test_review_agents_fake.py`

Protocol：

```python
class ReviewAgent(Protocol):
    def review(self, package: EvidencePackage) -> list[ReviewIssue]: ...

class CriticAgent(Protocol):
    def filter(self, issues: list[ReviewIssue], package: EvidencePackage) -> list[ReviewIssue]: ...
```

FakeLLM 策略（必须区分，用于 eval 展示 correlated failure）：

| 策略 | 行为 |
|---|---|
| `recall_biased_reviewer` | 倾向提出候选 finding，模拟高召回 reviewer |
| `precision_biased_critic` | 倾向质疑、降级、过滤，模拟高精度 critic |
| `same_strategy` | reviewer + critic 同策略，展示 correlated failure 风险 |
| `cross_strategy` | reviewer + critic 异策略，展示 harness 的过滤价值 |

- [x] `--mode hybrid-fake` 可运行
- [x] `--export-prompts` 输出 prompt hash + input JSON
- [x] invalid evidence id 被 filter 降级或丢弃

实现记录：`review/agents.py` 已加入 `ReviewAgent` / `CriticAgent` Protocol、`FakeLLMReviewAgent`、`FakeLLMCriticAgent` 和 `run_fake_hybrid_agents()`；`review` CLI 支持 `--mode hybrid-fake` 与 `--export-prompts`，prompt 导出包含 prompt hash 和 redacted input JSON。

---

## Phase 13 — Full Eval Benchmark

文件：`examples/eval_cases/` + `src/code_review_agent/eval/` + `tests/test_eval_metrics.py`

7 个 case（至少 2 个 no-finding）：

| Case | 类型 |
|---|---|
| `case_001_test_gap` | finding |
| `case_002_api_change` | finding |
| `case_003_error_handling` | finding |
| `case_004_artifact_pollution` | finding |
| `case_005_no_finding_doc_only` | no finding |
| `case_006_no_finding_test_only` | no finding |
| `case_007_design_constraint` | finding |

Threshold profiles：`strict` / `balanced` / `recall`

命令：`code-review-agent eval --cases examples/eval_cases --out outputs/eval --mode rules`

**完成标准**：
- [x] eval 命令可跑通，输出 `metrics.json` + `eval_report.md` + `case_results.json`
- [x] oracle 使用 planted bug + line range overlap，不用 LLM judge
- [x] eval report 展示 profile frontier 表
- [x] 能对比 deterministic baseline 与 fake/evidence-backed agent variant

实现记录：Phase 13 已完成。`eval` CLI 支持 `rules` / `hybrid-fake` / `all`，benchmark 已扩展到 7 个内置 planted-bug cases。这里的 `rules` 是 deterministic baseline；外部 benchmark adapter 属于 Post-MVP。

---

## Phase 14 — Demo Polish

- [x] `examples/demo_repo/` 像真实 Python 项目（不是碎片文件）
- [x] demo patch 覆盖：test gap / artifact pollution / error handling / no-finding doc-only / no-finding test-only
- [x] README 包含：一句话定位 / 为什么不是普通 Review Bot / 架构图 / demo 命令 / sample report / eval 指标表 / 当前限制

Demo 命令（必须可复现）：

```powershell
pip install -e ".[dev]"
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent map     --repo examples/demo_repo --out outputs/demo-map
code-review-agent review  --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
code-review-agent eval    --cases examples/eval_cases --out outputs/demo-eval --mode all
```

**完成标准**：
- [x] README 3 分钟内讲清楚项目价值
- [x] demo 命令可复现
- [x] report 里有至少一个高质量 finding 和一个 No Finding case

实现记录：Phase 14 已完成。README、用户指南和 demo repo 已同步更新。

---

## Post-MVP

不阻塞 MVP 的方向，按价值排序：

- [ ] 真实 OpenAI-compatible LLM backend（reviewer / critic 可选不同模型族）
- [ ] 外部 benchmark adapter（优先 AACR-Bench Python 子集；Martian Code Review Bench 作为对照）
- [ ] Draft → Ground → Critic 三阶段 pipeline
- [ ] GitHub PR URL 输入 + dry-run comment
- [ ] MCP tools（暴露 repo_map / review report / hygiene scan）
- [ ] `apply` 命令（确认后移动过程资产）
- [ ] 多语言（JS/TS → Go → Java）
- [ ] `references.py`（call graph 轻量版）
