# Code Review Agent Harness

Evidence-first local PR quality gate for AI-generated patches.

`code-review-agent` 是一个面向 AI Coding 工作流的本地 review agent harness：先用确定性工具解析 diff、构建上下文、证据和 guardrails，再让规则基线或受约束 agent 输出每条 finding 都可追踪的 review report。默认工作流不依赖 API key；`hybrid-live` 可选接入 OpenAI-compatible backend。

## 核心方向

- `map`：构建 RepoMap，输出 Python 文件、imports、symbols、related tests 和轻量风格基线。
- `hygiene`：识别过程性资产、实验脚本、临时文档和整理建议。
- `review`：解析 unified diff，绑定 RepoMap、changed entities、risk tags 和 evidence，生成 evidence-backed 预审报告。
- `eval`：用 planted-bug cases 和 deterministic oracle 评估 precision、recall、误报和 no-finding accuracy。

`summary` 不再作为独立 MVP 命令维护，后续合并进 `map --format markdown`。

## 为什么不是普通 AI Review Bot

- 裸 `diff -> LLM comments` 容易高误报，也难以复现评估。
- 本项目先生成结构化 evidence 和 verifier，再让受约束 agent 输出 finding；规则层只是 baseline 和 guardrail。
- 没有 evidence id 的问题不会成为正式 issue。

Design Rationale 见 [项目方案第 8 节](docs/CodeReviewAgent_2.0项目方案.md#8-design-rationale)。

## 当前状态

已包含：

- 标准 `src` Python 包结构和 `code-review-agent` CLI 入口。
- `hygiene` 命令的扫描、分类、LLM fake classifier 和整理建议。
- Phase 1 核心 dataclass：RepoMap、StyleBaseline、DiffLine、DiffHunk、DiffFileChange、ChangedEntity、RiskSignal、EvidencePackage、AgentRun。
- Phase 2 unified diff parser：支持 modified / added / deleted / renamed / binary file change。
- Phase 3 RepoMap builder：AST 提取 imports、classes、functions、methods，输出 `repo_map.json` / `repo_map.md`。
- Phase 4 changed entity extraction：把 diff hunk 映射到 module/class/function/method，无法精确映射时退化到 module。
- Phase 5 risk classification：用确定性规则输出 `RiskSignal`，覆盖 test gap、doc-only、config/dependency、error-handling、security、artifact 和 design constraint。
- Phase 6 EvidencePackage builder：生成 diff/entity/risk/test_discovery/hygiene 五类 evidence index。
- Phase 7 deterministic baseline：把高信号风险转成 evidence-backed baseline finding，并把 dependency change 放入 `needs_human_review`；这不是最终产品形态，而是 agent harness 的可复现基线。
- Phase 8 review pipeline CLI：`review` 命令可串起 diff parser、RepoMap、changed entities、risks、evidence、rules，并输出 `review_report.json` / `review_report.md`。
- Phase 9 micro eval benchmark：加入 deterministic oracle metrics 和 3 个 micro eval fixtures。
- Phase 10 report output：稳定 `review_report.json` schema，并输出固定章节顺序的 Markdown report。
- Phase 11 review filter：正式过滤 missing/invalid evidence、纯风格偏好和无关位置，并把弱证据 issue 降级到 `needs_human_review`。
- Phase 12 fake/hybrid agent：支持 `--mode hybrid-fake` 和 `--export-prompts`，用于展示 agent harness、prompt hash 和 evidence validator。
- Phase 13 built-in eval：`eval` 命令可跑 7 个内置 planted-bug cases，输出 `metrics.json` / `case_results.json` / `eval_report.md`，用于回归和演示，不等同于外部权威 benchmark。
- Phase 14 demo polish：`examples/demo_repo` 已打磨为可复现的小型 Python 项目，README 包含 demo 命令、架构、sample report 和 eval 指标。
- Post-MVP Phase 15 iterative review loop：`hybrid-fake` / `hybrid-live` 支持 `ReviewAgent -> GroundingVerifier -> CriticAgent -> PriorFeedback -> ReviewAgent` 的 bounded loop，并在报告中输出 `Loop Summary`。
- Post-MVP Phase 16 reliability：loop 支持 checkpoint/resume，live backend 支持 retry/fallback，并在 report 中聚合 tracing 字段。
- Post-MVP Phase 17 eval/demo 回归：`eval --mode all` 同时比较 `rules`、`hybrid-fake-iter1` 和 `hybrid-fake-iter2`，统计 reviewer burden / checkpoint / tracing 指标，并运行 Phase 16 reliability smoke。
- 基础测试和 hygiene 单元测试。

MVP 内 Phase 0-14 已完成。Post-MVP 可选方向：

- GitHub PR comment 集成。
- 自动修复建议。
- 多语言 AST / MCP server。
- 更完整的真实 reviewer / critic agent 编排。
- 外部 benchmark adapter，例如 AACR-Bench / Martian Code Review Bench 的子集接入。

## 架构

```text
Repository + unified diff
  -> map: AST RepoMap, imports, symbols, related tests, style baseline
  -> hygiene: process artifact classification and cleanup suggestions
  -> review: diff parser -> changed entities -> risk signals -> evidence package
  -> deterministic baseline OR iterative review loop
       ReviewAgent -> GroundingVerifier -> CriticAgent
          -> PriorFeedback -> ReviewAgent
  -> filter: evidence validator, location guard, confidence routing
  -> output: review_report.json, review_report.md, Loop Summary

eval:
  planted-bug patches + ground_truth.json
  -> review pipeline
  -> deterministic oracle
  -> Phase 16 checkpoint/resume/fallback smoke
  -> metrics.json, case_results.json, eval_report.md
```

## 开发文档

- [用户使用指南](docs/user_guide.md)
- [Post-MVP 增强路线图](docs/post_mvp_roadmap.md)
- [2.0 项目方案](docs/CodeReviewAgent_2.0项目方案.md)
- [2.0 实现计划](docs/CodeReviewAgent_2.0实现计划.md)
- [2.0 TODO](docs/CodeReviewAgent_2.0_TODO.md)

## Demo 命令

```powershell
pip install -e ".[dev]"
code-review-agent map     --repo examples/demo_repo --out outputs/demo-map
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent review  --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
code-review-agent review  --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review-loop --mode hybrid-fake --max-iter 2
code-review-agent eval    --cases examples/eval_cases --out outputs/demo-eval --mode all
```

当前可用命令：

```powershell
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent map --repo examples/demo_repo --out outputs/demo-map
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review-fake --mode hybrid-fake --max-iter 2 --export-prompts
code-review-agent eval --cases examples/eval_cases --out outputs/demo-eval --mode all
```

## Sample Review

`case_001_test_gap.patch` 会触发一条高质量 finding：

```text
Category: test_gap
File: src/shop/service.py
Message: Business logic changed while related tests exist but were not updated.
Evidence:
  - diff:src/shop/service.py:18
  - test_discovery:tests/test_service.py
```

`hybrid-fake --max-iter 2` 会额外展示 loop 摘要：

```text
## Loop Summary

| Metric | Value |
|---|---:|
| Iterations | 2 / 2 |
| Converged | true |
| Fallback | false |
```

`case_005_no_finding_doc_only.patch` 和 `case_006_no_finding_test_only.patch` 用于展示 No Finding：文档或测试清理不应该被工具强行评论。

## Eval 指标

当前内置 7-case planted-bug benchmark 的 balanced profile 示例：

| Variant | Recall | Spurious/PR | Precision | No-finding Accuracy | Evidence Coverage | Checkpoints | Trace Runs |
|---|---:|---:|---:|---:|---:|---:|---:|
| `rules` | 0.6000 | 0.1429 | 0.7500 | 1.0000 | 1.0000 | 0 | 0 |
| `hybrid-fake-iter1` | 1.0000 | 0.7143 | 0.5000 | 1.0000 | 1.0000 | 7 | 14 |
| `hybrid-fake-iter2` | 1.0000 | 0.7143 | 0.5000 | 1.0000 | 1.0000 | 7 | 24 |

这个表展示的是 harness 取舍，不是说项目目标是规则扫描：deterministic baseline 更保守、误报更低；hybrid-fake 召回更高，但需要 evidence filter、loop summary 和人工复核控制噪声。`hybrid-fake-iter1` 用于回归单轮行为，`hybrid-fake-iter2` 用于展示 critic-to-reviewer loop 打开后的收敛和审计信息；当前 deterministic fake loop 不声称 iter2 改善 precision/recall。

`eval --mode all` 还会运行 Phase 16 reliability smoke：确认 checkpoint 写出、resume 可用、无 live credentials 时 `hybrid-live` fallback 到 rules。

## 当前限制

- 主要支持 Python 仓库和 unified diff。
- 本地 CLI 优先，不自动发布 GitHub PR comment。
- 默认不自动修改目标仓库，也不做自动修复。
- Eval 使用 deterministic oracle，不使用 LLM judge；内置 benchmark 用于可复现开发验证，外部 benchmark adapter 属于 Post-MVP。
- `hybrid-live` 可调用 OpenAI-compatible backend；checkpoint/resume、retry/fallback 和 tracing 已接入，但真实 provider 的质量仍需要人工和外部 benchmark 验证。

Live reviewer startup script:

```powershell
Copy-Item scripts/review-live.env.example scripts/review-live.env.local
# Edit scripts/review-live.env.local and fill SILICONFLOW_API_KEY / SILICONFLOW_MODEL / SILICONFLOW_BASE_URL.

powershell -ExecutionPolicy Bypass -File scripts/review-live.ps1 `
  -Repo examples/demo_repo `
  -Diff examples/demo_repo/demo.patch `
  -Out outputs/demo-review-live `
  -Mode hybrid-live `
  -ExportPrompts
```

`scripts/review-live.env.local` is ignored by git. You can also skip the file and set the same variables in the current shell.

## 开发验证

```powershell
python -m pytest
python -m pytest tests/test_models.py tests/test_review_diff_parser.py tests/test_context_repo_map.py tests/test_review_changed_entity.py tests/test_review_risk.py tests/test_review_evidence.py tests/test_review_rules.py tests/test_review_filter.py tests/test_review_agents_fake.py tests/test_review_pipeline.py tests/test_eval_metrics.py tests/test_output_review_markdown.py -v
python -m code_review_agent.cli --help
python -m code_review_agent.cli review --help
```
