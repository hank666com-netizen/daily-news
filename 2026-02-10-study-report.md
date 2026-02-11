# Explorer 学习报告 | 2026-02-10

**生成时间**: 2026-02-10 15:25
**来源**: GitHub AI Agents 探索数据
**学习目标**: 理解 Self-Evolving Agents、OpenClaw 生态、RAG/Multi-agent

---

## 📚 一、Self-Evolving Agents 核心概念

### 1.1 EvoAgentX - Self-Evolving Ecosystem

**Repo**: https://github.com/EvoAgentX/EvoAgentX

**核心特点**：
- 自动生成和执行 multi-agent workflows
- 基于 LLM 的 workflow 生成器
- 支持工具集成（ArxivToolkit 等）
- 可配置的 LLM（支持 OpenAI GPT-4o-mini）

**架构**：
```
User Prompt → LLM → WorkflowGenerator → Workflow Graph
                                        ↓
                    AgentManager → 多 Agent 协作执行
```

**学习点**：
- ✅ Workflow 自动生成
- ✅ Agent 动态协作
- ✅ 工具集成框架

---

### 1.2 AgentEvolver - Efficient Self-Evolving

**Repo**: https://github.com/modelscope/AgentEvolver

**核心机制**：
1. **Self-Questioning** - 自动任务生成
2. **Self-Navigating** - 环境探索
3. **Self-Attributing** - 归因学习

**游戏 Arena**：
- Multi-agent 社会推理
- Avalon / Diplomacy 等游戏

**学习点**：
- ✅ 自动化数据构造
- ✅ 多 Agent 协作训练
- ✅ 强化学习框架

---

### 1.3 Agent0 - Zero Data Self-Evolving

**Repo**: https://github.com/aiming-lab/Agent0

**核心创新**：
- 零数据自我进化
- Tool-Integrated Reasoning
- Vision-Language 支持

**论文**：
- arXiv:2511.16043
- arXiv:2511.19900

**学习点**：
- ✅ 少样本/零样本学习
- ✅ 工具集成推理
- ✅ 多模态 Agent

---

### 1.4 Neo - Self-Improving Code Reasoning

**Repo**: https://github.com/Parslee-ai/neo

**核心特点**：
- **Semantic Memory** - 向量记忆
- **Pattern Retrieval** - 模式检索
- **Confidence Scoring** - 置信度评估

**架构**：
```
Prompt → Local Embedding → FAISS Search → Pattern Matching
                                    ↓
                 LLM API → Solution + Memory Update
```

**技术栈**：
- Jina Code Embeddings (768-dim)
- FAISS (向量搜索)
- Local JSON 存储

**学习点**：
- ✅ 语义记忆系统
- ✅ 检索增强生成
- ✅ 本地化知识库

---

## 🔗 二、OpenClaw 生态

### 2.1 VoltAgent/awesome-openclaw-skills

**Stars**: 12.3k

**内容**：
- OpenClaw Skills 大全
- Agent-to-Agent 协议
- 各种实用 Skills

**发现的有趣 Skills**：
| Skill | 功能 |
|-------|------|
| clawtoclaw | Agent 间协调 |
| agent-shield | 安全协议 |
| lobsterpot | 技术方案共享 |

**学习点**：
- ✅ Skills 生态系统
- ✅ Agent 通信协议
- ✅ 分布式 Agent 协作

---

### 2.2 e2b-dev/awesome-ai-agents

**Stars**: 25.7k

**内容**：
- AI Autonomous Agents 大全
- 包含 AutoGPT, BabyAGI, GPT-Engineer 等

**分类**：
- Agent Frameworks
- Autonomous Agents
- AI Tools

**学习点**：
- ✅ 行业全景
- ✅ 技术选型参考
- ✅ 最佳实践

---

## 🧩 三、RAG + Multi-agent 框架

### 3.1 Langflow

**Repo**: langflow-ai/langflow

**特点**：
- Low-code 可视化
- RAG + Multi-agent
- 拖拽式工作流

**适用场景**：
- RAG 应用快速构建
- Multi-agent 编排
- LLM 应用原型

**学习点**：
- ✅ 低代码设计
- ✅ 可视化调试
- ✅ 模块化架构

---

### 3.2 Griptape

**Repo**: griptape-ai/griptape

**特点**：
- 模块化 Python 框架
- Chain-of-Thought Reasoning
- 工具和记忆系统

**架构**：
```
Agent → Tasks → Tools + Memory → Reasoning → Output
```

**学习点**：
- ✅ 结构化推理
- ✅ Memory 管理
- ✅ Tool 集成

---

### 3.3 SuperAGI

**特点**：
- Dev-first 开源
- Autonomous Agent 框架
- 完整工具链

**适用场景**：
- 复杂任务自动化
- 多步骤工作流
- Agent 团队协作

---

## 💡 四、技术趋势总结

### 4.1 Self-Evolving Agents 的 4 个方向

| 方向 | 代表项目 | 关键技术 |
|------|---------|---------|
| Workflow 自动生成 | EvoAgentX | LLM + Planner |
| 零数据学习 | Agent0 | Few-shot + Tool |
| 记忆增强 | Neo | Vector DB + Retrieval |
| 强化训练 | AgentEvolver | RL + Game Arena |

### 4.2 OpenClaw Skills 生态系统

- Skills 是独立的能力包
- Skills.sh 管理安装
- Agent-to-Agent 协议
- 分布式协作

### 4.3 RAG + Multi-agent 融合

- Langflow: Low-code 可视化
- Griptape: 结构化推理
- SuperAGI: 完整框架

---

## 🎯 五、下一步学习计划

### 本周任务

| 优先级 | 任务 | 目标 |
|--------|------|------|
| 🔴 | 深入 EvoAgentX | 理解 workflow 自动生成 |
| 🔴 | 研究 Neo | 实现语义记忆 |
| 🟠 | 学习 Langflow | RAG + Multi-agent |
| 🟠 | 探索 VoltAgent | OpenClaw 生态 |

### 学习资源

- EvoAgentX GitHub
- Neo 文档
- Langflow 官网
- OpenClaw Skills

---

## 📖 六、关键术语表

| 术语 | 解释 |
|------|------|
| Self-Evolving | Agent 能够自动改进和进化 |
| Semantic Memory | 基于向量的语义记忆系统 |
| RAG | Retrieval-Augmented Generation |
| Multi-agent | 多 Agent 协作系统 |
| Workflow | 工作流程/任务编排 |
| Tool Integration | 工具集成框架 |

---

**报告生成**: Explorer v2.0
**下次更新**: 明天 8:00
**存储位置**: ~/clawd/hank-second-brain/tech/exploration/
