# AGENTS.md — Code Review Agent 项目 Agent 配置

本文件供 Codex、Claude Code 等 Agent 工具读取，定义本项目的 Agent 行为规范。

---

## 项目简介

**code-review-agent** 是一个面向 AI Coding 工作流的本地 Code Review Agent Toolkit。
- CLI 入口：`code-review-agent`（通过 `pip install -e ".[dev]"` 安装）
- Python 3.10+，无第三方运行时依赖
- 核心命令：`summary`（项目上下文）、`hygiene`（过程资产识别）、`review`（diff 预审）

---

## 核心原则

1. **只读优先**：除非明确被要求，不自动修改仓库文件，不自动重构或删除代码
2. **证据驱动**：每条 Review Issue 必须有可追踪的代码证据，不凭空猜测
3. **模块隔离**：各模块（hygiene/context/review/output）通过 `models.py` 数据模型通信
4. **测试先行**：新增功能必须在 `tests/` 目录创建对应测试文件

---

## 禁止行为

- ❌ 不得直接修改 `outputs/` 目录下的示例输出文件
- ❌ 不得修改 `docs/` 目录下的方案文档（除非明确被要求）
- ❌ 不得添加任何运行时第三方依赖到 `pyproject.toml` 的 `dependencies`（dev 依赖可以添加 pytest 相关）
- ❌ 不得删除 `tests/` 中已有的测试用例

---

## 开发工作流

### 运行测试
```bash
pytest                              # 全部测试
pytest tests/test_hygiene_classifier.py -v   # 特定模块
pytest tests/ -v -s                 # 带输出详细模式
```

### 安装和运行
```bash
pip install -e ".[dev]"             # 开发模式安装
code-review-agent --help            # 查看所有命令
code-review-agent hygiene --repo . --out outputs/run1          # 规则模式
code-review-agent hygiene --repo . --out outputs/run1 --llm    # LLM 增强模式
```

### 新增模块流程
1. 在 `models.py` 定义数据模型（`@dataclass(slots=True)`）
2. 在对应模块目录创建实现文件
3. 在 `cli.py` 注册命令
4. 在 `tests/` 创建测试文件

---

## 代码风格

- 使用 `from __future__ import annotations`（所有模块顶部）
- 类型注解完整，使用 Python 3.10+ 风格（`list[str]` 而非 `List[str]`）
- 数据类使用 `@dataclass(slots=True)` + `to_dict()` 方法
- 分类常量使用模块级字符串常量（如 `MAIN_CODE = "main_code"`）
- 不使用 `print`，使用 `sys.stderr.write` 或 logging 输出调试信息

---

## 当前已实现模块

| 模块 | 文件 | 状态 |
|------|------|------|
| 文件扫描 | `hygiene/scanner.py` | ✅ 完整 |
| 证据收集 | `hygiene/evidence.py` | ✅ 完整 |
| 规则分类 | `hygiene/classifier.py` | ✅ 完整 |
| 分类体系 | `hygiene/taxonomy.py` | ✅ 完整 |
| LLM 分类 | `hygiene/llm_classifier.py` | ✅ 完整 |
| 移动规划 | `hygiene/planner.py` | ✅ 完整 |
| 数据模型 | `models.py` | ✅ 完整 |
| CLI | `cli.py` | ✅ 基础完整 |
| Context/Summary | `context/` | 🔲 待实现 |
| Review/Diff | `review/` | 🔲 待实现 |
| Output 格式化 | `output/` | 🔲 待完善 |

---

## Skills 配置

本项目已在 `.agents/skills/` 下配置以下自定义 Skills：

- `code-review-agent` — 项目结构、模块职责、开发规范（自动触发）
- `agent-research` — AI Agent 领域论文调研与方法跟踪（使用 `$agent-research` 触发）

官方精选 Skills 安装方式见 `scripts/install-skills.ps1`。
