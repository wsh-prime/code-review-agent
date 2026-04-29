# 如何阅读 code-review-agent 代码

> 本文档随项目进展持续更新。当前对应 Phase 4 完成状态（62 个测试通过）。

---

## 读代码之前：建立整体感

不要直接跳进源文件。先在脑子里固定三件事：

**这个工具做什么？**
给 AI 生成的 patch（Codex / Cursor / Claude Code 的输出）在进入 PR 之前做本地预审。核心主张：每条 finding 必须有可追踪证据，不允许凭空输出问题。

**命令 → 输出 的映射**（当前实现了 `hygiene`，其余 Phase 3 以后陆续完成）：

| 命令 | 主要输出文件 |
|---|---|
| `hygiene` | `project_hygiene.json` · `PROJECT_ARTIFACTS.md` · `uncertain_queue.md` |
| `map` | `repo_map.json` · `repo_map.md` |
| `review` | `review_report.json` · `review_report.md`（Phase 8，未完成）|
| `eval` | `metrics.json` · `eval_report.md`（Phase 9，未完成）|

**一句话定位各层职责**：

```
CLI         →  解析参数，把请求分发给各模块，写输出文件
models.py   →  所有模块共享的数据合同，不含任何业务逻辑
hygiene/    →  只读扫描仓库，识别"过程资产"并建议整理
review/     →  解析 diff，提取结构化变更 + 映射变更实体（Phase 4 完成）
context/    →  AST 扫描仓库，建 RepoMap + 测试发现（Phase 3 完成）
output/     →  把结构化数据渲染成 Markdown 报告（Phase 10，待实现）
```

---

## 推荐阅读顺序

### 第一步：读数据模型（30 分钟）

**文件**：`src/code_review_agent/models.py`

这是整个项目的"词汇表"。所有模块之间只通过这里的 dataclass 通信。读这个文件不需要了解任何业务逻辑，只需要知道：

- 每个 dataclass 代表什么数据
- 哪些字段是必填的，哪些有默认值
- `to_dict()` 方法统一序列化为 JSON

**阅读重点**（按文件内顺序）：

1. `HygieneEvidence` / `SemanticClassification` / `FileClassification` / `MoveSuggestion`
   → hygiene 流水线的数据
2. `SymbolSummary` / `PythonModuleSummary` / `StyleBaseline` / `RepoMap`
   → context 层（Phase 3）的数据
3. `DiffLine` / `DiffHunk` / `DiffFileChange`
   → diff parser（Phase 2）的数据
4. `ChangedEntity` / `RiskSignal` / `ReviewEvidence` / `ReviewIssue`
   → review 核心数据，每条 issue 必须引用 `evidence_ids`
5. `EvidencePackage` / `AgentRun` / `ReviewReport`
   → 整个 pipeline 的最终聚合容器

**配套测试**：`tests/test_models.py` — 验证序列化和字段默认值，可以作为"使用示例"对照阅读。

---

### 第二步：读 hygiene 模块（1 小时）

**目录**：`src/code_review_agent/hygiene/`

这是目前唯一完整实现的功能模块，按以下顺序读：

#### 1. `scanner.py` — 入口，最简单

```
scan_repository(repo_path) → list[ScannedFile]
```

做什么：遍历目录，跳过 `.git` / `__pycache__` / `node_modules` 等，读每个文件前 4096 字节作为 `content_sample`，不做任何分类。

读完之后你知道：数据从磁盘进入系统的第一步是什么样子的。

**配套测试**：`tests/test_hygiene_scanner.py`

#### 2. `taxonomy.py` — 常量定义，很短

```
ALL_TYPES / MOVE_TYPES / REVIEW_TYPES / TARGET_DIRS / DESCRIPTIONS / SUGGESTED_ACTIONS
```

做什么：定义 7 种 artifact 类型（`experiment_script` / `adhoc_script` / `process_doc` / `generated_artifact` / `demo_sample` / `obsolete_candidate` / `uncertain`），以及每种类型对应的建议动作和目标目录。

读完之后你知道：LLM 分类器的输出空间被严格限定在这 7 个标签里。

**配套测试**：`tests/test_hygiene_taxonomy.py`

#### 3. `evidence.py` — 证据收集

```
collect_evidence(repo_path, scanned_files) → list[HygieneEvidence]
```

做什么：对每个文件，收集 4 类信号——
- `imports`：这个文件 import 了哪些本地模块
- `imported_by`：哪些文件 import 了它（反向图）
- `referenced_by_tests`：哪些测试文件引用了它
- `declared_in_config`：它是否出现在 `pyproject.toml` / `setup.py` 等配置文件中

另外实现了 `is_safety_guard_triggered()`：如果一个文件被其他模块 import 或被测试引用，就触发安全守卫，分类器不会建议移动它。

**配套测试**：`tests/test_hygiene_evidence.py`

#### 4. `classifier.py` — 规则分类器，最核心

```
classify_files(repo_path, scanned_files) → list[FileClassification]
classify_file(file, imported_paths) → FileClassification
```

做什么：对每个 `ScannedFile` 用确定性规则打标签（`main_code` / `test_code` / `experiment` / `design_doc` 等）。规则依次检查：
- 是否被其他本地模块 import（→ `main_code`）
- 路径/文件名特征（`test_` 前缀 → `test_code`，`scripts/` 路径 → `dev_script` 等）
- 内容 sample 关键词（`wandb` / `matplotlib` → `experiment`，`# TODO` → `todo` 等）

每条分类都会记录触发了哪条规则（`signals` 字段），confidence 是该规则的确定性程度。

**配套测试**：`tests/test_hygiene_classifier.py`

#### 5. `llm_classifier.py` — LLM 分类层（MVP 用 Fake）

```
FakeLLMClassifier.classify(evidence) → SemanticClassification
classify_with_llm(evidences, llm) → list[SemanticClassification]
```

做什么：定义了 `LLMClassifier` 协议（接口），`FakeLLMClassifier` 是测试用的假实现。真实 LLM 接入后只需实现同一协议即可替换。

`validate_semantic_classification()` 是输出验证器：LLM 的输出必须通过这里，否则抛异常——这是 harness 的噪音控制机制之一。

**配套测试**：`tests/test_hygiene_llm_classifier.py`

#### 6. `planner.py` — 移动建议生成

```
build_move_suggestions(repo_path, classifications) → list[MoveSuggestion]
build_project_artifacts_draft(classifications, suggestions) → str
```

做什么：把 `FileClassification` 映射到目标目录（如 `experiment` → `scripts/experiments/`），生成安全的移动建议（不实际移动文件），并渲染出 `PROJECT_ARTIFACTS.md` 的文本内容。

**配套测试**：`tests/test_hygiene_planner.py`

---

### 第三步：读 CLI 把数据流串起来（20 分钟）

**文件**：`src/code_review_agent/cli.py`

读 `run_hygiene_command()` 函数，这是目前唯一完整的命令处理器。它把上面所有模块串联起来：

```
scan_repository()
    → classify_files() / classify_files_semantic()
    → build_move_suggestions()
    → build_project_artifacts_draft()
    → ReviewReport(...)
    → 写 project_hygiene.json / PROJECT_ARTIFACTS.md / uncertain_queue.md
```

看完之后你能理解：数据如何从磁盘文件变成 JSON 输出，每一步的输入输出是什么。

**配套测试**：`tests/test_cli.py`

---

### 第四步：读 diff parser（20 分钟）

**文件**：`src/code_review_agent/review/diff_parser.py`

```
parse_unified_diff(diff_text) → list[DiffFileChange]
```

做什么：把 `git diff` / patch 文件的文本解析成结构化的 `DiffFileChange → DiffHunk → DiffLine` 层级。处理新增/删除/重命名/二进制文件/畸形 hunk（畸形 hunk 被 skip 并输出 warning，不中断整体解析）。

阅读建议：先看 `parse_unified_diff()` 的主循环（约 60 行），理解状态机结构，再看 `_parse_hunk()` 了解行号计算逻辑。

**配套测试**：`tests/test_review_diff_parser.py` — 重点看 `test_parse_demo_patch_preserves_hunk_line_numbers`，用的是真实的 `examples/demo_repo/demo.patch`。

---

### 第五步：读 RepoMap Builder（30 分钟）

**目录**：`src/code_review_agent/context/`

#### 1. `test_discovery.py` — 关联测试发现，先读这个（更简单）

```
discover_related_tests(repo_path, python_paths, module_summaries) → dict[str, list[str]]
```

做什么：对每个非测试 Python 文件，找到"可能在测试它"的测试文件。策略分三层，优先级依次降低：
1. **路径名命名约定**：`service.py` → 找 `test_service.py`
2. **import 引用**：测试文件中 import 了这个模块
3. **符号名引用**：测试文件中出现了该模块的 class/function 名称

这是保守策略——宁可漏报，不要误报，符合项目"证据驱动"的核心主张。

**配套测试**：`tests/test_context_test_discovery.py`

#### 2. `repo_map.py` — RepoMap 构建器，主要逻辑在这里

```
build_repo_map(repo_path) → RepoMap
render_repo_map_markdown(repo_map) → str
```

`build_repo_map()` 的执行流程：

```
scan_repository()                  ← 复用 hygiene/scanner.py，得到文件列表
    ↓
_summarize_python_module()         ← 对每个 .py 文件：ast.parse() 提取
    classes / functions / methods（含行号）
    imports（ast.Import + ast.ImportFrom）
    module_docstring
    ↓
discover_related_tests()           ← 调用 test_discovery.py
    ↓
_build_imported_by()               ← 把 import_map 反转，建反向依赖图
_build_style_baseline()            ← 统计 docstring 覆盖率、import 风格等
```

**两个关键细节**：
- `_summarize_python_module()` 只扫描 `tree.body`（顶层），类里的方法会被扫，但函数内的局部类不会——有意为之（成本/收益权衡）
- `_build_imported_by()` 做了 `src.` 前缀去除（`src.shop.service` → `shop.service`），处理本地包的常见导入方式

**配套测试**：`tests/test_context_repo_map.py`

---

### 第六步：读 ChangedEntity 提取器（20 分钟）

**文件**：`src/code_review_agent/review/changed_entity.py`

```
extract_changed_entities(changes, repo_map) → list[ChangedEntity]
```

做什么：把 diff hunks 映射到具体的 Python 实体（class / function / method / module）。

核心算法 `_innermost_symbol()`：
- 对 hunk 里每一行改动，找 `repo_map` 中行号范围包含该行的所有符号
- 取"最小包含范围"的那个（method 优先于 class，因为方法的行范围更小）
- 有 tie 时按优先级：method > function > class
- 如果没有任何符号覆盖该行（如模块级常量），fallback 到 `entity_type="module"`

`_merge_entity()`：同一个 `(path, entity_type, qualified_name)` 的多个 hunk 合并为一条 `ChangedEntity`，`hunk_ids` 累积。

**阅读建议**：结合 `test_maps_hunk_to_function_method_class_and_module` 测试一起看，用例里有一个完整的 diff 覆盖了 class / method / function 和模块级代码，是最清楚的"示例文档"。

**配套测试**：`tests/test_review_changed_entity.py`

---

## 运行代码的方法

```powershell
# 安装开发模式
pip install -e ".[dev]"

# 运行全部测试
python -m pytest tests/ -v

# 对本仓库跑 hygiene（rules 模式）
code-review-agent hygiene --repo . --out .cra/hygiene

# 对本仓库跑 hygiene（hybrid 模式，使用 FakeLLM）
code-review-agent hygiene --repo . --out .cra/hygiene --classifier hybrid

# 对本仓库跑 map（生成 RepoMap）
code-review-agent map --repo . --out .cra/map
```

---

## 设计约定备忘

读代码时会反复遇到这些约定，记住可以省很多困惑：

| 约定 | 说明 |
|---|---|
| `@dataclass(slots=True)` | 所有数据类都用 slots，避免意外属性赋值 |
| `to_dict()` | 序列化统一用 `asdict(self)` 或手写，不用 `json.dumps` 直接处理 dataclass |
| `from __future__ import annotations` | 所有模块顶部都有，允许用 `list[str]` 而不是 `List[str]` |
| `evidence_ids: list[str]` | `ReviewIssue` 引用证据用 ID 字符串，不嵌套对象 |
| `sys.stderr.write` / logging | 不用 `print` 输出调试信息 |
| Safety guard | `imported_by` 或 `referenced_by_tests` 非空 → 绝不建议移动该文件 |
| FakeLLMClassifier | MVP 阶段代替真实 LLM，实现同一 `LLMClassifier` Protocol |
| `_innermost_symbol()` | method > function > class，取行范围最小的符号作为 entity |

---

## 当前未实现的模块

| 文件 | 计划功能 | 对应 Phase |
|---|---|---|
| `review/risk_classifier.py` | 确定性 risk tag 打标 | Phase 5 |
| `review/evidence_builder.py` | 构建 EvidencePackage | Phase 6 |
| `review/rules_reviewer.py` | 纯规则 findings，无需 LLM | Phase 7 |
| `cli.py` → `review` 子命令 | 串联完整 review pipeline | Phase 8 |
| `output/` | Markdown / JSON 报告渲染 | Phase 10 |
| `review/filter.py` | 误报控制层 | Phase 11 |
| `review/fake_agent.py` | FakeLLM + Agent Protocol | Phase 12 |

---

*最后更新：Phase 4 完成 — 62 个测试通过*
