---
name: agent-research
description: 辅助调研 AI Agent 领域的论文和最新方法。当需要阅读论文、整理调研笔记、跟踪最新 Agent 框架（如 OpenAI Agents SDK、LangGraph、AutoGen、MCP协议）、对比不同方法优劣、或将论文思路落地到项目代码时触发。
---

# Agent Research Skill

## 适用场景

- 阅读和理解 Agent 相关论文（ReAct、RAG、Tool Use、Multi-Agent、Code Agent）
- 跟踪最新 Agent 框架动态（OpenAI Agents SDK、LangGraph、AutoGen、CrewAI）
- 将论文方法转化为 code-review-agent 项目的具体实现思路
- 对比不同 Agent 架构方案的优劣
- 整理调研结论为结构化笔记

---

## 论文阅读流程

### 第一步：快速定位核心贡献
阅读摘要、引言最后一段、结论第一段，回答以下问题：
1. 解决什么问题？
2. 核心方法/创新点是什么？
3. 主要实验结论是什么（量化指标）？
4. 与当前项目的关联点在哪里？

### 第二步：深入方法细节
- 重点读 Method/Approach 章节
- 记录关键算法步骤、数据流、模块设计
- 标注可直接复用的设计模式

### 第三步：评估实现可行性
- 是否有开源代码？（优先找 GitHub 链接）
- 依赖哪些模型或外部服务？
- 与 code-review-agent 项目的集成点在哪里？

---

## 关键领域与追踪方向

### Code Agent（核心方向）
- **SWE-bench** 系列：评估 Agent 解决 GitHub Issue 的能力
- **Agentic Coding**：Codex、Cursor、Devin 的实现思路
- **Code Review Agent**：LLM-based 预审、evidence-backed review
- **Tree-sitter / AST 分析**：静态分析辅助 Agent

### Agent 框架与协议
- **OpenAI Agents SDK**：Handoffs、Guardrails、Tool Calls
- **MCP (Model Context Protocol)**：工具注册与调用标准
- **ReAct Pattern**：Reasoning + Acting 交替循环
- **Multi-Agent Orchestration**：主从 Agent、并行 Agent

### RAG 与上下文管理
- **RepoMap**：代码仓库的结构化表示（参考 Aider 实现）
- **Semantic Chunking**：代码文件的语义切片
- **Evidence-backed Review**：从代码中提取证据支撑 Review 结论

---

## 调研笔记模板

当整理调研结论时，使用以下结构：

```markdown
## 论文/方法：{标题}

**来源**：{arXiv链接 / 博客 / 代码库}
**日期**：{发布时间}

### 核心贡献
- 

### 方法概述
- 

### 关键指标
| Benchmark | 本方法 | Baseline |
|-----------|--------|----------|

### 与项目的关联
- 可用于：
- 实现难度：低/中/高
- 优先级：

### 参考资源
- 代码：
- 论文：
```

---

## 常用资源

| 类型 | 链接 |
|------|------|
| OpenAI Agents SDK 文档 | https://developers.openai.com/api/docs/guides/agents |
| OpenAI Skills 文档 | https://developers.openai.com/codex/skills |
| MCP 协议文档 | https://developers.openai.com/codex/mcp |
| Agent Skills 开放标准 | https://agentskills.io |
| SWE-bench | https://www.swebench.com |
| arXiv CS.AI | https://arxiv.org/list/cs.AI/recent |
| Papers With Code (Agent) | https://paperswithcode.com/task/autonomous-agents |

---

## 输出规范

调研结论输出到项目 `docs/` 目录：
- `docs/research/` — 论文阅读笔记
- `docs/methods/` — 方法对比分析
- `docs/roadmap.md` — 基于调研的功能路线图更新
