# Code Review Agent 使用指南

本地 Code Review Agent，读取仓库 + diff，输出带证据的 JSON / Markdown 报告，**不会修改被审查仓库**。

## 安装

```powershell
pip install -e ".[dev]"
code-review-agent --help
```

---

## 快速上手（推荐脚本）

最省事的方式是直接改 `scripts/run-*.ps1` 顶部的参数，然后运行脚本。

```powershell
# 生成 RepoMap
powershell -ExecutionPolicy Bypass -File scripts/run-map.ps1

# 运行 hygiene，默认 hybrid，不走 rules
powershell -ExecutionPolicy Bypass -File scripts/run-hygiene-llm.ps1

# 生成 diff 并运行真实 LLM review，默认 hybrid-live
powershell -ExecutionPolicy Bypass -File scripts/run-review-llm.ps1
```

也可以一键按顺序运行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-all-llm.ps1
```

脚本默认输出：

- `outputs/my-map/repo_map.json`
- `outputs/my-hygiene/project_hygiene.json`
- `outputs/my-review-live/review_report.md`
- `outputs/my-review-live/review_report.json`
- `outputs/logs/*.log`：每次脚本运行的终端日志

---

## 手动命令（三步）

```powershell
# 1. 生成仓库地图（可选，但能让 review 更准确）
code-review-agent map --repo . --out outputs/my-map

# 2. 导出当前改动
git diff | Out-File -Encoding utf8 changes.patch

# 3. 审查
code-review-agent review `
  --repo . --diff changes.patch --out outputs/my-review-live `
  --mode hybrid-live `
  --repo-map outputs/my-map/repo_map.json `
  --hygiene outputs/my-hygiene/project_hygiene.json
```

报告输出到 `outputs/my-review-live/`：`review_report.md`（人读）和 `review_report.json`（机器读）。

---

## 命令速查

| 命令 | 用途 | 需要 API |
|---|---|---|
| `map` | 扫描仓库，生成结构 / imports / symbols / tests 索引 | 否 |
| `hygiene` | 识别实验脚本、临时文档等过程性文件，给出整理建议 | 否（`--classifier hybrid` 使用内置 fake）|
| `review` | 读取 unified diff，生成 evidence-backed review 报告；`rules` 是 deterministic baseline，`hybrid-*` 是 agent harness 路径 | `rules` / `hybrid-fake` 不需要；`hybrid-live` 需要 |
| `eval` | 运行内置 planted-bug benchmark，输出 precision / recall / no-finding accuracy | 否 |

### 脚本速查

| 脚本 | 用途 | 默认模式 |
|---|---|---|
| `scripts/run-map.ps1` | 生成 RepoMap | map |
| `scripts/run-hygiene-llm.ps1` | 运行 hygiene | `--classifier hybrid` |
| `scripts/run-review-llm.ps1` | 生成 diff 并运行真实 LLM review | `--mode hybrid-live` |
| `scripts/run-eval-hybrid.ps1` | 跑 eval harness | `--mode hybrid-fake` |
| `scripts/run-all-llm.ps1` | 串行运行 map / hygiene / review | hybrid/live |

`eval` 当前 CLI 没有真实 live LLM 模式，因此 eval 脚本默认使用 `hybrid-fake`，不使用 `rules`。

### hygiene

```powershell
code-review-agent hygiene --repo . --out outputs/my-hygiene --classifier hybrid
```

### review 模式

```powershell
# 调用真实模型
code-review-agent review --repo . --diff changes.patch --out outputs/my-review --mode hybrid-live
```

### eval benchmark

当前 `eval` 是项目内置的 planted-bug benchmark，用于可复现回归测试和 demo 指标展示。它不是外部权威 benchmark；外部 benchmark adapter 属于 Post-MVP 增强。

```powershell
# 只跑 deterministic baseline
code-review-agent eval --cases examples/eval_cases --out outputs/demo-eval --mode rules

# 对比 baseline 与 hybrid-fake agent harness
code-review-agent eval --cases examples/eval_cases --out outputs/demo-eval --mode all
```

`eval` 会输出：

- `metrics.json`：聚合指标和 profile frontier。
- `case_results.json`：每个 case 的 TP / FP / FN。
- `eval_report.md`：人类可读的指标表。

---

## 配置 API（仅 hybrid-live 需要）

复制示例并填写 key：

```powershell
Copy-Item scripts/review-live.env.example scripts/review-live.env.local
# 编辑 scripts/review-live.env.local：
#   SILICONFLOW_API_KEY=sk-your-key
#   SILICONFLOW_MODEL=deepseek-ai/DeepSeek-V4-Flash
#   SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
```

然后用启动脚本（自动加载 env 文件）：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/review-live.ps1 `
  -Repo . -Diff changes.patch -Out outputs/my-review-live -Mode hybrid-live
```

也可以直接设置环境变量后运行 `code-review-agent review --mode hybrid-live`。支持通用变量名 `OPENAI_COMPATIBLE_API_KEY` / `OPENAI_COMPATIBLE_MODEL` / `OPENAI_COMPATIBLE_BASE_URL`（优先级低于 `SILICONFLOW_*`）。

> ⚠️ **不要把 `review-live.env.local` 或真实 API Key 提交到仓库。**

---

## 注意事项

- `review` 报告是预审结果，不替代人工 reviewer；`needs_human_review` 中的项目需要人工判断。
- 所有命令只读 `--repo`，不会修改目标仓库文件。
- demo 可复现命令：`map` / `hygiene` / `review` 使用 `examples/demo_repo`，`eval` 使用 `examples/eval_cases`。
