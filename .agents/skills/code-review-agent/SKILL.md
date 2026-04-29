---
name: code-review-agent
description: 当用户在 code-review-agent 项目中工作时触发。涵盖项目结构、模块职责、开发规范、测试方式、CLI 命令设计，以及 hygiene/review/context/output 四大模块的实现细节。当需要新增功能、修复 bug、理解模块间关系或运行测试时使用本 skill。
---

# Code Review Agent Harness — 项目 Skill

## 项目定位

面向 AI Coding 工作流的本地 Code Review Agent Toolkit。
核心命令：`summary`（建立项目上下文）、`hygiene`（识别过程性资产）、`review`（对 diff/patch 做 evidence-backed 预审）。
**默认只读**，不自动修改仓库，不替代人类 reviewer。

---

## 目录结构

```
code-review-agent/
├── src/code_review_agent/
│   ├── __init__.py          # 导出核心数据模型
│   ├── __main__.py          # python -m 入口
│   ├── cli.py               # Click CLI 定义，注册 summary/hygiene/review 命令
│   ├── models.py            # 所有共享 dataclass 数据模型
│   ├── hygiene/             # Hygiene 命令实现
│   │   ├── __init__.py
│   │   ├── scanner.py       # 扫描文件，产出 ScannedFile 列表
│   │   ├── taxonomy.py      # 7 种 artifact_type 定义与分类规则
│   │   ├── evidence.py      # 收集文件的引用证据（imports、被谁引用等）
│   │   ├── classifier.py    # 规则分类器，产出 FileClassification
│   │   ├── llm_classifier.py# LLM 语义分类器，产出 SemanticClassification
│   │   └── planner.py       # 整合规则+LLM 结果，生成 MoveSuggestion 列表
│   ├── context/             # Summary 命令实现（待完善）
│   │   └── __init__.py
│   ├── review/              # Review 命令实现（待完善）
│   │   └── __init__.py
│   └── output/              # 输出格式化（Markdown/JSON）
│       └── __init__.py
├── tests/                   # pytest 测试，文件名对应模块
│   ├── test_hygiene_scanner.py
│   ├── test_hygiene_classifier.py
│   ├── test_hygiene_evidence.py
│   ├── test_hygiene_llm_classifier.py
│   ├── test_hygiene_planner.py
│   ├── test_hygiene_taxonomy.py
│   ├── test_models.py
│   └── test_cli.py
├── outputs/                 # 各命令的示例输出（不提交到主线）
│   ├── demo-hygiene/
│   ├── demo-read/
│   └── phase1-hybrid/
├── docs/                    # 项目方案文档
├── pyproject.toml           # 构建配置，CLI 入口: code-review-agent = "code_review_agent.cli:main"
└── AGENTS.md                # Codex Agent 配置
```

---

## 核心数据模型（models.py）

| 模型 | 用途 |
|------|------|
| `HygieneEvidence` | 单个文件的全量证据（路径、内容样本、imports、被引用关系、配置声明） |
| `SemanticClassification` | LLM 语义分类结果（artifact_type、confidence、suggested_action、reason） |
| `FileClassification` | 规则分类结果（category、mainline_relevance、confidence） |
| `MoveSuggestion` | 移动建议（source_path → suggested_path，含理由和置信度） |
| `RepoMap` | 仓库地图（文件列表、imports 图、symbols、related_files） |
| `ReviewIssue` | 单条 Review 问题（含 evidence 字段，必须有可追踪证据） |
| `ReviewReport` | 完整 Review 报告 |

---

## Hygiene 模块分类体系（taxonomy.py）

**7 种 artifact_type：**
- `experiment_script` — 实验性脚本，只用于一次性验证
- `adhoc_script` — 临时辅助脚本（数据下载、迁移等）
- `process_doc` — 过程性文档（方案草稿、调研记录、todo）
- `generated_artifact` — AI 生成的中间产物
- `demo_sample` — 演示示例，不属于主线逻辑
- `obsolete_candidate` — 疑似废弃代码
- `uncertain` — 无法确定，需人工确认

**规则分类（classifier.py）的核心分类：**
`MAIN_CODE` | `TEST_CODE` | `DATA_SCRIPT` | `DEV_SCRIPT` | `EXPERIMENT` | `DESIGN_DOC` | `RESEARCH_DOC` | `PLANNING_DOC` | `TODO` | `ARTIFACT` | `UNKNOWN`

**过程性类别集合（PROCESS_CATEGORIES）：**
`DATA_SCRIPT`, `DEV_SCRIPT`, `EXPERIMENT`, `RESEARCH_DOC`, `PLANNING_DOC`, `TODO`, `ARTIFACT`

---

## 开发规范

### 语言和依赖
- Python 3.10+，无第三方依赖（仅 dev: pytest>=8.0）
- 数据模型使用 `@dataclass(slots=True)`，必须实现 `to_dict()` 方法
- 模块间通过 `models.py` 中的 dataclass 传递数据，不跨模块直接导入实现细节

### 新增功能流程
1. 在 `models.py` 中定义或扩展数据模型
2. 在对应模块（hygiene/context/review/output）中实现逻辑
3. 在 `cli.py` 中注册新命令或选项
4. 在 `tests/` 中创建对应测试文件 `test_<模块名>.py`

### 测试规范
```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/test_hygiene_classifier.py -v

# 带输出运行
pytest tests/ -v -s
```

### CLI 使用
```bash
# 安装到本地（开发模式）
pip install -e ".[dev]"

# Hygiene 检查
code-review-agent hygiene --repo . --out outputs/my-run

# Hygiene + LLM 语义分类
code-review-agent hygiene --repo . --out outputs/my-run --llm

# 查看帮助
code-review-agent --help
code-review-agent hygiene --help
```

---

## 输出格式

所有命令输出到 `--out` 指定目录：
- `project_hygiene.json` — 机器可读的分类结果
- `PROJECT_ARTIFACTS.md` — 人类可读的 Markdown 报告
- `uncertain_queue.md` — 需人工确认的文件列表（有 LLM 模式时生成）

---

## 当前进展（Phase 1）

- ✅ Hygiene 模块完整实现（scanner → evidence → classifier → llm_classifier → planner）
- ✅ 基础 CLI（hygiene 命令可运行）
- ✅ 完整测试覆盖（8 个测试文件）
- 🔲 context/summary 模块（待实现）
- 🔲 review 模块（待实现）
- 🔲 output 格式化模块（待完善）

---

## 重要设计原则

1. **证据优先**：每条 ReviewIssue 必须有 `evidence` 字段，不允许凭空判断
2. **置信度分级**：所有分类结果都带 `confidence` (0.0-1.0)，低置信度进入 uncertain_queue
3. **只读默认**：工具不自动修改任何文件，移动操作仅生成建议
4. **可组合命令**：各命令独立可运行，也可以串联（先 summary → hygiene → review）
