# Code Review Agent 使用指南

本地 Code Review Agent，读取仓库 + diff，输出带证据的 JSON / Markdown 报告，**不会修改被审查仓库**。

## 安装

```powershell
pip install -e ".[dev]"
code-review-agent --help
```

---

## 快速上手（三步）

```powershell
# 1. 生成仓库地图（可选，但能让 review 更准确）
code-review-agent map --repo . --out outputs/my-map

# 2. 导出当前改动
git diff | Out-File -Encoding utf8 changes.patch

# 3. 审查
code-review-agent review `
  --repo . --diff changes.patch --out outputs/my-review `
  --repo-map outputs/my-map/repo_map.json
```

报告输出到 `outputs/my-review/`：`review_report.md`（人读）和 `review_report.json`（机器读）。

---

## 命令速查

| 命令 | 用途 | 需要 API |
|---|---|---|
| `map` | 扫描仓库，生成结构 / imports / symbols / tests 索引 | 否 |
| `hygiene` | 识别实验脚本、临时文档等过程性文件，给出整理建议 | 否（`--classifier hybrid` 使用内置 fake）|
| `review` | 读取 unified diff，生成 evidence-backed review 报告 | `rules` / `hybrid-fake` 不需要；`hybrid-live` 需要 |

### hygiene

```powershell
code-review-agent hygiene --repo . --out outputs/my-hygiene
# 加 --classifier hybrid 启用语义分类（内置 fake，无需 API）
```

### review 模式

```powershell
# 默认 rules 模式（无 API）
code-review-agent review --repo . --diff changes.patch --out outputs/my-review

# fake agent 走完整 harness（演示 / 调试 prompt，无 API）
code-review-agent review --repo . --diff changes.patch --out outputs/my-review --mode hybrid-fake --export-prompts

# 调用真实模型
code-review-agent review --repo . --diff changes.patch --out outputs/my-review --mode hybrid-live
```

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
