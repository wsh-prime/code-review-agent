# Read Guide: Phase 5 + 6（risk + evidence）

> 目标：帮助你快速看懂当前 Phase 5/6 代码，并能独立扩展规则。
> 
> 当前状态：`review/risk.py`、`review/evidence.py` 已实现，相关测试通过。

---

## 0. 先建立心智模型

Phase 5/6 在 review pipeline 里的位置：

```text
diff_parser -> changed_entity -> risk -> evidence -> (rules reviewer / agent)
```

你要记住两句话：

1. **Phase 5 (`risk.py`)**：从结构化 diff + repo context 里打 deterministic risk tags。
2. **Phase 6 (`evidence.py`)**：把 diff/entity/risk/test/hygiene 整理成统一 `EvidencePackage`，并检查证据引用是否完整。

---

## 1. 先读输入/输出（不要先读细节）

### Phase 5 主函数

```python
classify_risks(
    changes: list[DiffFileChange],
    repo_map: RepoMap,
    changed_entities: list[ChangedEntity],
    hygiene_classifications: list[FileClassification] | None = None,
) -> list[RiskSignal]
```

输入是四块：`diff`、`repo_map`、`changed_entities`、可选 `hygiene`。
输出是 `list[RiskSignal]`（每条必须带 `evidence_ids`）。

### Phase 6 主函数

```python
build_evidence_package(
    repo_path,
    changes,
    changed_entities,
    risk_signals,
    repo_map,
    hygiene_classifications=None,
) -> EvidencePackage
```

输出是一个完整可追踪上下文包：
- `changed_files`
- `changed_entities`
- `risk_signals`
- `evidence_index: dict[id, ReviewEvidence]`
- `metadata`（含 redaction 信息）

---

## 2. 阅读顺序（推荐 45 分钟）

## Step A：读 `risk.py` 顶部常量（5 分钟）

先看所有 tag 常量和 token 常量：
- 风险标签：`API_CHANGE`、`BEHAVIOR_CHANGE`、`TEST_GAP`、`CONFIG_CHANGE`、`DEPENDENCY_CHANGE`、`ERROR_HANDLING_CHANGE`、`SECURITY_SENSITIVE`、`DOC_ONLY`、`EXPERIMENT_ARTIFACT`、`DESIGN_CONSTRAINT_VIOLATION`
- 路径/关键词表：`CONFIG_PATHS`、`DEPENDENCY_FILES`、`SECURITY_TOKENS`、`EXPERIMENT_MARKERS`

这一步的目的：先知道“它会产出哪些风险”，再看“怎么产出”。

## Step B：读 `classify_risks()` 主流程（10 分钟）

主流程是一个聚合器，顺序如下：

1. `doc_only` 快速短路（纯文档 patch 直接返回）
2. config/dependency 风险
3. API 变化
4. 行为变化（函数/方法逻辑变动）
5. test gap（改了源码但没改关联测试）
6. hunk 内容风险（error handling / security token）
7. experiment artifact（路径 + hygiene 联合判定）
8. design constraint（基于 style baseline）
9. 去重 `_deduplicate_signals()`

注意：每个子函数都直接构造 `RiskSignal(evidence_ids=[...])`，不允许“无证据风险”。

## Step C：读最关键的 4 条规则（15 分钟）

按收益优先阅读：

1. `_test_gap_risks()`
   - 取 `repo_map.related_tests[path]`
   - 若 source 改了、相关测试存在但未在 patch 中改动 -> `TEST_GAP`
   - 证据会附带 `test_discovery:*` 和 `diff:*`

2. `_api_change_risks()`
   - 公开签名变更（`def/class` 且非 `_private`）触发 `API_CHANGE`
   - `__init__.py` 的导出变化也触发

3. `_design_constraint_risks()`
   - baseline 不可靠（`total_public_functions < 5`）直接跳过
   - docstring coverage 高时，新增/修改 public function/method 无 docstring 触发
   - 新测试命名风格和 import 风格偏离基线也会触发

4. `_experiment_artifact_risks()`
   - `added` 文件且路径像 experiment，或 hygiene 分类在 `PROCESS_CATEGORIES`
   - 同时附 `hygiene:*` 证据（如果有）

## Step D：读 `evidence.py`（10–15 分钟）

先看 `build_evidence_package()` 的 5 个 `_add_many()`：

- `_diff_evidence()`：把新增/删除行转成 `diff:path:line`
- `_entity_evidence()`：把 changed entity 转成 `entity:path:qualified_name`
- `_test_discovery_evidence()`：从 `repo_map.related_tests` 生成 `test_discovery:*`
- `_hygiene_evidence()`：把 hygiene 分类放入证据索引
- `_risk_evidence()`：每条 risk 生成一个 `risk:tag:path` 证据

最后读 `find_missing_evidence_ids()`：
- 当前只校验 `risk_signals[*].evidence_ids` 是否存在于 `evidence_index`
- 这是后续 filter/verifier 的基础前置检查

---

## 3. 配套测试怎么读（最省时间）

建议严格按下面顺序：

1. `tests/test_review_risk.py`
   - 看每个 test 名就是一条需求说明
   - 重点：
     - `test_test_gap_triggers_when_related_tests_are_not_changed`
     - `test_design_constraint_triggers_only_when_baseline_is_reliable`
     - `test_experiment_artifact_uses_path_or_hygiene_classification`

2. `tests/test_review_evidence.py`
   - 看 `test_build_evidence_package_indexes_diff_entity_risk_and_tests`
   - 再看 `test_find_missing_evidence_ids_reports_invalid_references`

读法：先看断言，再回头看 fixture 构造，再回源码。你会更快理解“为什么这么设计”。

---

## 4. 你可以手动做的 3 个学习练习

### 练习 1：加一个 security token

在 `SECURITY_TOKENS` 增加一个词，比如 `pickle.loads`，写一个最小测试确认会触发 `SECURITY_SENSITIVE`。

### 练习 2：验证 evidence 引用闭环

手工构造一个 `RiskSignal(evidence_ids=["diff:foo.py:999"])`，调用 `find_missing_evidence_ids()`，确认能报出缺失项。

### 练习 3：理解 design constraint 的门槛

把 baseline 的 `total_public_functions` 改成 4，观察 `DESIGN_CONSTRAINT_VIOLATION` 规则被整体跳过。

---

## 5. 当前实现的优点与注意点

### 优点

- 全 deterministic，可重复
- 每条风险都可追到 `evidence_ids`
- 与 hygiene 联动但不强耦合
- test 颗粒度好，回归保护有效

### 注意点（非阻断）

- `find_missing_evidence_ids()` 当前只检查 `risk_signals`，后续引入 `ReviewIssue` 时建议扩展到 issue 级校验
- `SECURITY_TOKENS` 是关键词匹配，属于轻量启发式，后续可逐步升级为 AST 模式
- `risk.py` 体量较大，后续可按规则组拆分为子模块（保持接口不变）

---

## 6. 快速定位索引

- 风险主入口：`src/code_review_agent/review/risk.py` -> `classify_risks()`
- 证据主入口：`src/code_review_agent/review/evidence.py` -> `build_evidence_package()`
- 证据完整性检查：`src/code_review_agent/review/evidence.py` -> `find_missing_evidence_ids()`
- 风险测试：`tests/test_review_risk.py`
- 证据测试：`tests/test_review_evidence.py`

---

*建议：每次 Phase 5/6 规则有新增，都在本文件追加“新增规则 → 对应测试名 → 风险标签 → 证据ID格式”。*