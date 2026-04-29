# Evidence 设计文档

> 本文档解释 code-review-agent 中 Evidence（证据）体系的设计理念、数据结构，以及 Phase 11 之前已落地的五类 Evidence 各自的含义。

---

## 一、为什么要 Evidence？

传统的 Code Review 工具要么输出"我觉得这里有问题"，要么把整个文件扔给 LLM 让它猜。两者的共同缺陷是：

- **不可追溯**：谁也不知道这条 Review Issue 是从哪里来的
- **无法过滤**：没有证据，就无法判断一条 finding 是有效发现还是幻觉
- **不可审计**：报告之外没有任何中间产物可供检查

Evidence 体系的核心思路是 **先收集可追溯的代码事实，再从事实中推导 finding**。每条 `ReviewIssue` 必须携带 `evidence_ids`，指向 `EvidencePackage.evidence_index` 里有据可查的 `ReviewEvidence` 对象。Phase 11 的 filter 层正是依赖这套体系来过滤无证据、假证据、幻觉 finding。

---

## 二、核心数据结构

### `ReviewEvidence`（单条证据）

定义在 `src/code_review_agent/models.py`：

```python
@dataclass(slots=True)
class ReviewEvidence:
    id: str       # 全局唯一标识，格式如 "diff:src/shop/service.py:35"
    kind: str     # 类型枚举，见下文五类
    source: str   # 文件路径或系统标识符
    message: str  # 人类可读的描述
```

### `EvidencePackage`（一次 review 的完整证据包）

```python
@dataclass(slots=True)
class EvidencePackage:
    repo_root: str
    changed_files: list[DiffFileChange]       # 解析出的 diff 变更文件列表
    changed_entities: list[ChangedEntity]     # AST 提取的变更函数/类/方法
    risk_signals: list[RiskSignal]            # 确定性风险分类结果
    evidence_index: dict[str, ReviewEvidence] # id → evidence 全量索引
    metadata: dict[str, Any]
```

`evidence_index` 是核心查询表。所有 `ReviewIssue.evidence_ids` 都必须在这里找得到对应条目，否则 Phase 11 filter 会将该 issue 标记为 `invalid_evidence_ids` 并丢弃。

### `ReviewIssue`（一条 Review 发现）

```python
@dataclass(slots=True)
class ReviewIssue:
    file: str
    line: int | None
    severity: str         # "low" | "medium" | "high"
    category: str         # 如 "test_gap", "api_change", ...
    message: str
    suggestion: str
    confidence: float
    evidence_ids: list[str]  # 必须非空，且全部在 evidence_index 中存在
```

---

## 三、五类 Evidence（Phase 11 前已落地）

以下五类 Evidence 在 `src/code_review_agent/review/evidence.py` 的 `build_evidence_package()` 中统一收集。

---

### 1. `diff` — Diff 行级证据

**ID 格式**：`diff:<文件路径>:<行号>`

**示例**：`diff:src/shop/service.py:35`

**收集来源**：`review/evidence.py` → `_diff_evidence()`

每一行 `added` 或 `removed` 的 diff line 都会生成一条 `diff` 类型的 Evidence。对于没有 hunk 内容（如新增空文件、整文件删除）的变更，退化为 `diff:<path>:1`。

**含义**：这行代码在本次 diff 中被修改了。这是最底层、最直接的代码变更证据。

**典型用途**：`ReviewIssue` 需要指向变更行时必须有对应 `diff` 证据，否则说明 finding 的位置与本次变更无关。

---

### 2. `entity` — 变更实体证据

**ID 格式**：`entity:<文件路径>:<qualified_name>`

**示例**：`entity:src/shop/service.py:ShopService.create_order`

**收集来源**：`review/evidence.py` → `_entity_evidence()`

基于 `review/changed_entity.py` 提取的 `ChangedEntity` 生成。每个被 diff hunk 触及的 Python 函数、方法、类都产生一条 entity 证据，包含精确的行范围（`line_start`–`line_end`）。

**含义**：某个具名代码实体（函数/类/方法）的实现在本次 diff 中被修改。Entity 证据比 diff 证据更语义化，支持"这个函数被改了"这类更高层次的推断。

**典型用途**：`api_change`、`behavior_change` 类 finding 通常引用 entity 证据。

---

### 3. `test_discovery` — 相关测试发现证据

**ID 格式**：`test_discovery:<测试文件路径>`

**示例**：`test_discovery:tests/test_service.py`

**收集来源**：`review/evidence.py` → `_test_discovery_evidence()`

基于 `RepoMap.related_tests`（由 `context/repo_map.py` 构建）生成。RepoMap 通过文件名匹配（`test_<module>` 或 `<module>_test`）以及 import 分析，发现与源文件相关联的测试文件。

**含义**：这个测试文件与被变更的源文件存在关联（命名约定 + import 追踪）。如果测试文件本身没有出现在 diff 中，就可以推断"业务逻辑改了但测试没跟上"，支持 `test_gap` 类 finding。

**典型用途**：`test_gap` 风险信号与 finding 的核心证据。

---

### 4. `hygiene` — 文件卫生分类证据

**ID 格式**：`hygiene:<文件路径>`

**示例**：`hygiene:experiments/quick_test.py`

**收集来源**：`review/evidence.py` → `_hygiene_evidence()`

基于 `hygiene` 命令输出的 `FileClassification` 生成（可选输入，通过 `--hygiene` 参数传入）。每个被分类为过程产物（`experiment_script`、`process_doc` 等）的文件都产生一条 hygiene 证据。

**含义**：某个被变更的文件在 Hygiene 分析中被标记为"不属于主线代码"的过程产物。如果这类文件被混入功能 diff，可能说明 AI Coding 产物管理不规范。

**典型用途**：`experiment_artifact`、`design_constraint_violation` 类 finding 的支撑证据。

---

### 5. `risk` — 风险信号证据

**ID 格式**：`risk:<tag>:<文件路径>`

**示例**：`risk:test_gap:src/shop/service.py`

**收集来源**：`review/evidence.py` → `_risk_evidence()`

基于 `review/risk.py` 中 `classify_risks()` 产生的 `RiskSignal` 生成。每条风险信号本身也被记录为 Evidence，使其可以被 `ReviewIssue` 引用。

**含义**：确定性风险分类器（无需 LLM）判断此变更带有某种风险标签。`risk` 证据是对底层 `diff`/`entity`/`test_discovery` 证据的聚合性描述，代表"综合判断"而非"原始事实"。

**已定义的风险标签（`risk.py` 中的常量）**：

| 标签 | 含义 |
|------|------|
| `api_change` | 公共函数/类的签名被修改 |
| `behavior_change` | 函数逻辑实现被修改 |
| `test_gap` | 业务逻辑改了但相关测试文件未变 |
| `config_change` | 配置文件（pyproject.toml 等）被修改 |
| `dependency_change` | 依赖声明（requirements.txt 等）被修改 |
| `error_handling_change` | 异常处理逻辑被修改 |
| `security_sensitive` | 涉及 auth/token/subprocess 等安全敏感词 |
| `doc_only` | 整个 patch 仅改动文档/Markdown |
| `experiment_artifact` | 变更文件被 Hygiene 识别为实验产物 |
| `design_constraint_violation` | 违反仓库架构约束（如测试文件引入了生产依赖）|

---

## 四、Evidence ID 命名规则速查

| 类型 | ID 格式 | 例子 |
|------|---------|------|
| diff | `diff:<path>:<lineno>` | `diff:src/svc.py:12` |
| entity | `entity:<path>:<qualified_name>` | `entity:src/svc.py:Svc.run` |
| test_discovery | `test_discovery:<test_path>` | `test_discovery:tests/test_svc.py` |
| hygiene | `hygiene:<path>` | `hygiene:experiments/poc.py` |
| risk | `risk:<tag>:<path>` | `risk:test_gap:src/svc.py` |

---

## 五、Evidence 在 Pipeline 中的流动

```
parse_unified_diff()         → DiffFileChange 列表
extract_changed_entities()   → ChangedEntity 列表 (AST)
classify_risks()             → RiskSignal 列表 (确定性规则)
                                      ↓
                        build_evidence_package()
                                      ↓
              EvidencePackage（包含 5 类 evidence_index）
                                      ↓
           run_rules() / run_fake_hybrid_agents()
            生成候选 ReviewIssue（携带 evidence_ids）
                                      ↓
                         filter_issues()  ← Phase 11
          验证 evidence_ids → 分流到 findings / needs_human_review / discarded
                                      ↓
              write_review_json() + render_review_markdown()  ← Phase 10
```

---

## 六、关键约束（Phase 11 filter 强制执行）

1. **`evidence_ids` 不能为空**，否则直接 `discard`（reason: `missing_evidence`）
2. **所有 `evidence_ids` 必须在 `evidence_index` 中存在**，幽灵 ID 会被清理，全无效则 `discard`（reason: `invalid_evidence_ids`）
3. **纯风格偏好的 issue**（含 PEP8/命名规范等关键词）直接 `discard`（reason: `style_preference`）
4. **文件不在变更范围 && 无相关 evidence** → `discard`（reason: `file_not_changed`）
5. **置信度低于阈值（默认 0.6）或行号与变更 hunk/entity 无关** → 降级到 `needs_human_review`

这套约束保证了最终 `findings` 中的每一条 Review Issue 都有可追溯的代码事实支撑。
