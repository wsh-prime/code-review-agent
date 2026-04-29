# Code Review Agent Harness

Evidence-first local PR quality gate for AI-generated patches.

`code-review-agent` 是一个面向 AI Coding 工作流的本地 review harness：先用确定性工具解析 diff、构建上下文和证据，再输出每条 finding 都可追踪的 review report。真实 LLM backend 后置，MVP 不依赖 API key。

## 核心方向

- `map`：构建 RepoMap，输出 Python 文件、imports、symbols、related tests 和轻量风格基线。
- `hygiene`：识别过程性资产、实验脚本、临时文档和整理建议。
- `review`：解析 unified diff，绑定 RepoMap、changed entities、risk tags 和 evidence，生成 evidence-backed 预审报告。
- `eval`：用 planted-bug cases 和 deterministic oracle 评估 precision、recall、误报和 no-finding accuracy。

`summary` 不再作为独立 MVP 命令维护，后续合并进 `map --format markdown`。

## 为什么不是普通 AI Review Bot

- 裸 `diff -> LLM comments` 容易高误报，也难以复现评估。
- 本项目先生成结构化 evidence，再让规则或受约束 agent 输出 finding。
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
- Phase 7 rules-only review：把高信号风险转成 evidence-backed finding，并把 dependency change 放入 `needs_human_review`。
- Phase 8 review pipeline CLI：`review` 命令可串起 diff parser、RepoMap、changed entities、risks、evidence、rules，并输出 `review_report.json` / `review_report.md`。
- Phase 9 micro eval benchmark：加入 deterministic oracle metrics 和 3 个 micro eval fixtures。
- Phase 10 report output：稳定 `review_report.json` schema，并输出固定章节顺序的 Markdown report。
- Phase 11 review filter：正式过滤 missing/invalid evidence、纯风格偏好和无关位置，并把弱证据 issue 降级到 `needs_human_review`。
- Phase 12 fake/hybrid agent：支持 `--mode hybrid-fake` 和 `--export-prompts`，用于展示 agent harness、prompt hash 和 evidence validator。
- 基础测试和 hygiene 单元测试。

下一步：

- Phase 13：Full Eval Benchmark。
- Phase 14：Demo Polish。

## 开发文档

- [用户使用指南](docs/user_guide.md)
- [2.0 项目方案](docs/CodeReviewAgent_2.0项目方案.md)
- [2.0 实现计划](docs/CodeReviewAgent_2.0实现计划.md)
- [2.0 TODO](docs/CodeReviewAgent_2.0_TODO.md)

## CLI 目标接口

```powershell
code-review-agent map     --repo examples/demo_repo --out outputs/demo-map
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent review  --repo examples/demo_repo --diff examples/demo_repo/demo.patch --out outputs/demo-review
code-review-agent eval    --cases examples/eval_cases --out outputs/demo-eval
```

当前可用命令：

```powershell
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent map --repo . --out outputs/demo-map
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/demo.patch --out outputs/demo-review
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/demo.patch --out outputs/demo-review --mode hybrid-fake --export-prompts
```

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
