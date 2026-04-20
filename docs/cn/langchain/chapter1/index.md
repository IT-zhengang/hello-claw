---
title: LangChain 实战教程（一）
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--overview">
  <div class="langchain-hero__eyebrow">LangChain 深度技术指南 · 第一篇</div>
  <div class="langchain-hero__headline">框架定位 / 模块地图 / 学习路径</div>
  <p class="langchain-hero__subtitle">先回答“为什么需要 LangChain”这个入口问题：它如何把记忆、检索、工具和多步编排组织成一个真正可落地的 LLM 应用框架。</p>
  <div class="langchain-hero__tags">
    <span>Framework Overview</span>
    <span>Module Map</span>
    <span>RAG</span>
    <span>Agent</span>
  </div>
</div>



<div class="langchain-series-heading">系列导航</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">第一篇 · 总览</span>
    <span class="langchain-series-card__desc">先回答为什么需要 LangChain，并建立模块地图、版本演进和整体学习路径。</span>
    <span class="langchain-series-card__meta">Framework Positioning · Module Map · 当前阅读</span>
    </span>
    <span class="langchain-series-disclosure__toggle">
      <span class="langchain-series-disclosure__toggle-closed">展开全部系列导航</span>
      <span class="langchain-series-disclosure__toggle-opened">收起系列导航</span>
    </span>
  </summary>

  <div class="langchain-series-grid langchain-series-grid--compact">
  <a class="langchain-series-card is-current" href="../chapter1/">
    <span class="langchain-series-card__kicker">第一篇 · 总览</span>
    <span class="langchain-series-card__desc">先回答为什么需要 LangChain，并建立模块地图、版本演进和整体学习路径。</span>
    <span class="langchain-series-card__meta">Framework Positioning · Module Map · 当前阅读</span>
  </a>
  <a class="langchain-series-card" href="../chapter2/">
    <span class="langchain-series-card__kicker">第二篇 · 接口层</span>
    <span class="langchain-series-card__desc">聚焦 Model I/O、PromptTemplate、OutputParser 与结构化输出，先把输入输出接口层打稳。</span>
    <span class="langchain-series-card__meta">ChatModel · PromptTemplate · Structured Output</span>
  </a>
  <a class="langchain-series-card" href="../chapter3/">
    <span class="langchain-series-card__kicker">第三篇 · 编排层</span>
    <span class="langchain-series-card__desc">从接口层进入编排层，理解 Chain、LCEL、并行链与流式工作流是如何组织起来的。</span>
    <span class="langchain-series-card__meta">Chain · LCEL · RunnableParallel · Streaming</span>
  </a>
  <a class="langchain-series-card" href="../chapter4/">
    <span class="langchain-series-card__kicker">第四篇 · 状态层</span>
    <span class="langchain-series-card__desc">聚焦 Memory、会话级历史管理与摘要记忆，补齐多轮对话里的状态与上下文管理。</span>
    <span class="langchain-series-card__meta">Memory · Session History · Summary Memory</span>
  </a>
  <a class="langchain-series-card" href="../chapter5/">
    <span class="langchain-series-card__kicker">第五篇 · 知识层</span>
    <span class="langchain-series-card__desc">围绕 Document Loaders、Text Splitter、Embedding、VectorStore 与 Retriever，搭建完整的 RAG 检索增强链路。</span>
    <span class="langchain-series-card__meta">RAG · Embeddings · Vector Store · Retriever</span>
  </a>
  <a class="langchain-series-card" href="../chapter6/">
    <span class="langchain-series-card__kicker">第六篇 · 自治层</span>
    <span class="langchain-series-card__desc">围绕 Tool、ReAct、Tool Calling 与 `create_agent`，进入目标驱动的工具调用与自主决策。</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent</span>
  </a>
  <a class="langchain-series-card" href="../chapter7/">
    <span class="langchain-series-card__kicker">第七篇 · 项目层</span>
    <span class="langchain-series-card__desc">把 Model I/O、Memory 与 RAG 组合成一个可上传文档、支持检索和流式响应的知识库助手。</span>
    <span class="langchain-series-card__meta">FastAPI · Chroma · Streaming · Integrated Project</span>
  </a>
  <a class="langchain-series-card" href="../chapter8/">
    <span class="langchain-series-card__kicker">第八篇 · 生态层</span>
    <span class="langchain-series-card__desc">介绍 LangSmith、LangGraph 与主流框架对比，建立 LangChain 后续工程深化与选型视角。</span>
    <span class="langchain-series-card__meta">LangSmith · LangGraph · Ecosystem · Comparison</span>
  </a>
  </div>
</details>

> 这一篇从框架定位与模块地图切入，先回答为什么需要 LangChain，再建立后续 RAG、Agent 与 Memory 的整体坐标。

---

## 1. LangChain 是什么？为什么需要它？

你已经会用 `requests` 或 `httpx` 调用大模型的 API 了——传一段 prompt，拿到一段回答。但当你想构建一个**真正的 AI 应用**（带记忆的对话、基于私有文档的问答、能自主使用工具的 Agent），直接调 API 就远远不够了。LangChain 正是为了解决这个问题而生的。

### 1.1 直接调 API 有什么问题？

先来看一个最简单的大模型调用：

```python
import httpx
import os

API_KEY = os.getenv("DEEPSEEK_API_KEY")

response = httpx.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "用一句话解释什么是 LangChain"}],
    },
)
print(response.json()["choices"][0]["message"]["content"])
```

这段代码能跑，但当需求变复杂时，你会遇到**四个核心痛点**：

| 痛点 | 场景 | 裸调 API 的代价 |
| ---- | ---- | ---- |
| **没有记忆** | 多轮对话，LLM 不记得上一句话 | 手动维护 `messages` 列表，越来越长 |
| **没有知识** | 问你的私有文档内容，LLM 一无所知 | 自己实现 RAG 全套流程（加载 → 分割 → 向量化 → 检索 → 拼接） |
| **没有工具** | 让 LLM 查数据库、搜网页、调计算器 | 自己写 JSON 解析 + 工具分发 + 错误处理 |
| **难以组合** | 多步骤工作流（总结 → 翻译 → 格式化） | 手动串联多次 API 调用，代码变成意大利面 |

```text
裸调 API 适合：一问一答的简单场景
LangChain 适合：需要记忆 / 需要知识库 / 需要工具 / 需要多步编排的复杂应用
```

> 💡 **类比**：裸调 API 就像你手动操作数据库——`cursor.execute("SELECT ...")`。LangChain 就像 ORM（Django Model / SQLAlchemy）——帮你抽象掉重复的底层细节，让你专注于业务逻辑。

### 1.2 LangChain 的核心定位：LLM 应用开发框架

LangChain 不是一个模型，也不是一个 API 服务——它是一个**连接大模型与外部世界的框架**。

```text
LangChain 的一句话定位：

「用标准化的组件，把 LLM 从一个“聊天接口”变成一个能记忆、能检索、
  能使用工具、能编排复杂流程的完整应用。」
```

**LangChain 的核心思想是“模块化 + 可组合”**：

```text
┌──────────────────────────────────────────────────┐
│                  你的 AI 应用                    │
├──────────────────────────────────────────────────┤
│  Model I/O  │  Chain  │  Memory  │  Agent       │
│  (模型交互)  │  (编排)  │  (记忆)  │  (自主决策)   │
├──────────────────────────────────────────────────┤
│  Document Loaders  │  Embeddings  │  Vector      │
│  (文档加载)         │  (向量嵌入)   │  Stores      │
├──────────────────────────────────────────────────┤
│  Middleware（中间件）│  LangGraph（Agent 运行时） │
├──────────────────────────────────────────────────┤
│  LLM（DeepSeek / OpenAI / Claude / 本地模型）      │
└──────────────────────────────────────────────────┘
```

**LangChain 的几个设计原则**：

| 原则 | 含义 | 好处 |
| ---- | ---- | ---- |
| **模型无关** | 同一套代码，换一行配置就能切换 DeepSeek → OpenAI → Claude | 不被厂商锁定 |
| **组件可组合** | 每个模块独立，像乐高一样自由拼装 | 按需使用，不用全买 |
| **LCEL 管道** | 用 `|` 操作符串联组件，代码像读句子一样自然 | 可读性极高 |
| **可观测** | 内置与 LangSmith 集成，追踪每一步的输入输出 | 调试不再抓瞎 |

> 💡 **LangChain 于 2025 年 10 月正式发布 v1.0 稳定版**，当前最新为 v1.2。v1.0 带来了重大升级：全新的 `create_agent` 抽象、中间件系统、`with_structured_output` 结构化输出、以及基于 LangGraph 的 Agent 运行时。旧版功能已迁移至 `langchain-classic` 包。本教程基于 v1.x 最新架构编写。

### 1.3 架构全景图：核心模块一览

本教程会按照以下顺序，逐一讲解 LangChain 的核心模块：

```text
第 2 章              第 3 章           第 4 章         第 5 章         第 6 章
Model I/O     →     Chain (LCEL)  →    Memory    →    RAG       →    Agent
模型交互              链式编排            对话记忆          检索增强          自主决策
prompt → LLM         A | B | C         记住上下文         基于文档问答       使用工具

                         ↓ 组合到一起 ↓

                   第 7 章：综合实战项目
                FastAPI + LangChain 知识库助手
```

**每个模块解决什么问题？**

| 模块 | 一句话说明 | 解决什么痛点 |
| ---- | ---- | ---- |
| **Model I/O** | 统一的模型调用 + Prompt 模板 + 输出解析 | 不同模型 API 格式不一样 |
| **Chain (LCEL)** | 用 `|` 把多个步骤串成流水线 | 多步编排代码混乱 |
| **Memory** | 自动管理对话历史 | LLM 没有记忆 |
| **RAG** | 文档加载 → 向量化 → 检索 → 回答 | LLM 不懂你的私有数据 |
| **Agent** | LLM 自己决定用什么工具、怎么用 | 需要 LLM 执行真实操作 |

### 1.4 安装与环境配置

**环境要求：**

- **Python ≥ 3.9**（v1.0 起不再支持 Python 3.8）
- **Pydantic v2**（v1.0 起不再支持 Pydantic v1）

**安装核心包：**

```bash
# 核心框架（必装，自动包含 langchain-core）
pip install langchain

# 模型提供商（按需选择一个）
pip install langchain-deepseek       # DeepSeek（官方集成包，推荐）
pip install langchain-openai         # OpenAI（也可用于兼容 OpenAI 接口的服务）
# pip install langchain-anthropic    # Claude
# pip install langchain-google-genai # Gemini

# Agent 运行时（第 6 章用到，v1.0 的 Agent 基于 LangGraph）
pip install langgraph

# RAG 相关（第 5 章用到）
pip install langchain-chroma         # Chroma 向量数据库
pip install langchain-community      # 社区集成（文档加载器等）
```

**配置 API Key（推荐用 `.env` 文件）：**

```ini
# .env 文件
DEEPSEEK_API_KEY=sk-your-api-key-here
# 或
OPENAI_API_KEY=sk-your-api-key-here
```

```python
# 在代码中加载
from dotenv import load_dotenv
load_dotenv()  # 自动读取 .env 文件中的环境变量

# ── 方式 1：使用官方提供商包（推荐） ──
from langchain_deepseek import ChatDeepSeek

# DeepSeek 有专用的 langchain-deepseek 包，无需手动配置 base_url
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    # api_key 自动从 DEEPSEEK_API_KEY 环境变量读取
)

response = llm.invoke("你好，LangChain！")
print(response.content)
# 你好！我是一个 AI 助手，很高兴通过 LangChain 与你交流！

# ── 方式 2：init_chat_model 统一接口（v1.0 新增，推荐） ──
from langchain.chat_models import init_chat_model

# 使用 "provider:model" 统一格式，一个函数搞定所有提供商
llm = init_chat_model("deepseek:deepseek-chat")  # DeepSeek
# 切换 OpenAI：init_chat_model("openai:gpt-4o")
# 切换 Claude：init_chat_model("anthropic:claude-sonnet-4-20250514")

# 也可以用 model_provider 参数分开指定
# llm = init_chat_model("deepseek-chat", model_provider="deepseek")
```

> 💡 **本教程使用 DeepSeek 作为主要模型**（性价比高、中文能力强、兼容 OpenAI 接口），但所有代码只需改一行配置即可切换为 OpenAI / Claude / Gemini。

---

## 总结

这篇文章最核心的价值，是先把 LangChain 这条学习线的入口问题讲清楚了：

1. **为什么会需要 LangChain**：因为一旦应用开始需要记忆、知识库、工具调用和多步编排，裸调 API 很快就会失控。
2. **LangChain 的定位是什么**：它不是模型，而是把模型、检索、工具和工作流组织成完整应用的框架层。
3. **后续应该怎么学**：可以沿着 `Model I/O → Chain (LCEL) → Memory → RAG → Agent` 的顺序逐步深入。

如果把原文压缩成一句话，那就是：**LangChain 不是为了替代模型，而是为了让大模型真正长成可落地、可扩展、可维护的应用。**

</div>
