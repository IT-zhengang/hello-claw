---
title: LangChain 实战教程（八）
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--ecosystem">
  <div class="langchain-hero__eyebrow">LangChain 深度技术指南 · 第八篇</div>
  <div class="langchain-hero__headline">LangSmith / LangGraph / Ecosystem / Framework Comparison</div>
  <p class="langchain-hero__subtitle">从单一框架走向完整生态，理解 LangSmith 可观测、LangGraph 工作流，以及 LangChain 与其他框架的边界。</p>
  <div class="langchain-hero__tags">
    <span>LangSmith</span>
    <span>LangGraph</span>
    <span>LlamaIndex</span>
    <span>Semantic Kernel</span>
  </div>
</div>

<div class="langchain-series-heading">系列导航</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">第八篇 · 生态层</span>
    <span class="langchain-series-card__desc">介绍 LangSmith、LangGraph 与主流框架对比，建立 LangChain 后续工程深化与选型视角。</span>
    <span class="langchain-series-card__meta">LangSmith · LangGraph · Ecosystem · Comparison · 当前阅读</span>
    </span>
    <span class="langchain-series-disclosure__toggle">
      <span class="langchain-series-disclosure__toggle-closed">展开全部系列导航</span>
      <span class="langchain-series-disclosure__toggle-opened">收起系列导航</span>
    </span>
  </summary>

  <div class="langchain-series-grid langchain-series-grid--compact">
  <a class="langchain-series-card" href="../chapter1/">
    <span class="langchain-series-card__kicker">第一篇 · 总览</span>
    <span class="langchain-series-card__desc">先回答为什么需要 LangChain，并建立模块地图、版本演进和整体学习路径。</span>
    <span class="langchain-series-card__meta">Framework Positioning · Module Map</span>
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
  <a class="langchain-series-card is-current" href="../chapter8/">
    <span class="langchain-series-card__kicker">第八篇 · 生态层</span>
    <span class="langchain-series-card__desc">介绍 LangSmith、LangGraph 与主流框架对比，建立 LangChain 后续工程深化与选型视角。</span>
    <span class="langchain-series-card__meta">LangSmith · LangGraph · Ecosystem · Comparison · 当前阅读</span>
  </a>
  </div>
</details>

> 这一篇进入 LangChain 的生态与进阶层，围绕 LangSmith、LangGraph 与框架对比，建立后续工程深化与选型视角。

---

## 8. LangChain 生态与进阶

LangChain 不只是一个框架——它背后有一整套生态工具。这一章介绍最重要的几个，以及和其他框架的对比，帮你规划后续的学习方向。

### 8.1 LangSmith：追踪与调试你的 LLM 应用

LLM 应用最头疼的是**调试**——链条长了之后，不知道是哪一步出了问题。LangSmith 是 LangChain 官方的可观测平台：
```

    # 开启 LangSmith 追踪（只需设置环境变量）
    import os
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"
    os.environ["LANGCHAIN_PROJECT"] = "my-project"

    # 之后所有 LangChain 调用都会自动记录到 LangSmith
    chain = prompt | llm | parser

    result = chain.invoke({"question": "什么是 RAG？"})
    # 在 smith.langchain.com 可以看到完整的调用链路

```

**LangSmith 能看到什么：**

| 功能            | 说明                       |
|---------------|--------------------------|
| **链路追踪**      |  每一步的输入、输出、耗时、token 用量   |
| **错误定位**      |  哪一步报错了、错误信息是什么          |
| **Prompt 调试** |  查看实际发送给 LLM 的完整 prompt  |
| **性能分析**      |  每步耗时占比、token 成本统计       |
| **评估测试**      |  批量跑测试用例，对比不同 prompt 的效果 |

> 💡 **强烈推荐在开发阶段就接入 LangSmith**——当你的 RAG 回答不准确时，可以看到检索到了哪些文档块、prompt 拼装成什么样子、LLM 是基于什么信息回答的。

### 8.2 LangGraph：Agent 的底层运行时

LangGraph 在 v1.0 中的定位发生了重大变化——它不再只是“可选扩展”，而是 **`create_agent` 的底层运行时**。当你需要更细粒度的控制（多分支、条件循环、人机协作），LangGraph 让你用图（Graph）来定义 Agent 的状态流转：
```

    # pip install langgraph
    from langgraph.graph import StateGraph, END
    from typing import TypedDict

    # ── 定义状态 ──
    class AgentState(TypedDict):
        question: str
        search_results: str
        answer: str
        needs_more_info: bool

    # ── 定义节点（每个节点是一个处理函数） ──
    def search_node(state):
        """搜索知识库"""
        results = retriever.invoke(state["question"])
        return {"search_results": format_docs(results)}

    def answer_node(state):
        """基于搜索结果回答"""
        answer = llm.invoke(f"根据以下内容回答：{state['search_results']}\n\n问题：{state['question']}")
        return {"answer": answer.content, "needs_more_info": "不确定" in answer.content}

    def refine_node(state):
        """如果答案不确定，进一步搜索"""
        results = retriever.invoke(state["question"] + " 更多细节")
        refined = llm.invoke(f"补充信息：{format_docs(results)}\n原始回答：{state['answer']}")
        return {"answer": refined.content}

    # ── 构建图 ──
    graph = StateGraph(AgentState)
    graph.add_node("search", search_node)
    graph.add_node("answer", answer_node)
    graph.add_node("refine", refine_node)

    graph.set_entry_point("search")
    graph.add_edge("search", "answer")

    # 条件分支：如果需要更多信息 → refine，否则 → 结束
    graph.add_conditional_edges(
        "answer",
        lambda state: "refine" if state["needs_more_info"] else END,
    )
    graph.add_edge("refine", END)

    app = graph.compile()
    result = app.invoke({"question": "LangGraph 和 LangChain 有什么区别？"})

```
```

    LangGraph 的执行路径：

      search → answer → (需要更多信息?) → refine → END
                       ↘ (已经够了)   → END

```

### 8.3 与其他框架对比：LlamaIndex、Semantic Kernel

| 维度           | LangChain    | LlamaIndex   | Semantic Kernel  |
|--------------|--------------|--------------|------------------|
| **定位**       |  通用 LLM 应用框架 | RAG 专精框架     | 微软的 AI 编排 SDK    |
| **核心优势**     |  组件丰富、生态大    | RAG 效果更优     | 与 Azure 深度整合     |
| **编排方式**     |  LCEL 管道     | Query Engine | Plugin + Planner |
| **Agent 支持** |  ✅ 完善        | ✅ 基础         | ✅ 完善             |
| **语言**       |  Python, JS  | Python, JS   | Python, C#, Java |
| **学习曲线**     |  中等          | 较低           | 中等               |
| **适用场景**     |  全类型 LLM 应用  | RAG 为主的应用    | 微软技术栈项目          |

**怎么选？**

```

**大部分场景** → LangChain（生态最大、社区最活跃、教程最多）
**纯 RAG 应用** → LlamaIndex（检索策略更丰富、开箱即用效果好）
**微软/Azure 技术栈** → Semantic Kernel

```

> 💡 **它们不是互斥的**——很多项目同时使用 LangChain 做 Agent 编排 + LlamaIndex 做 RAG 引擎。

### 8.4 持续学习路线图
```

    你现在的位置（读完本教程）：

    ✅ 已掌握                              📚 下一步
    ──────────────────────────────────────────────────
    Model I/O（prompt + 输出解析）    →  Prompt Engineering 进阶
    with_structured_output       →  自定义 Tool Calling Schema
    Chain（LCEL 编排）                →  LangGraph 状态机
    Memory（对话记忆）                →  持久化存储（PostgreSQL/Redis）
    RAG（检索增强生成）               →  高级 RAG（重排序/混合检索/知识图谱）
    Agent（create_agent）             →  多 Agent 协作（CrewAI/AutoGen）
    Middleware（中间件）              →  自定义中间件开发

```

**推荐的学习资源：**

| 资源                 | 链接                                | 说明                |
|--------------------|-----------------------------------|-------------------|
| LangChain 官方文档     | python.langchain.com              | 最权威的参考            |
| LangChain Cookbook | github.com/langchain-ai/langchain | 官方示例集             |
| LangSmith          | smith.langchain.com               | 调试和评估平台           |
| LangGraph 文档       | langchain-ai.github.io/langgraph  | 状态机 Agent         |
| DeepLearning.AI 课程 | deeplearning.ai                   | 吴恩达的 LangChain 短课 |

**最后的建议：**
> 💡 **学框架最好的方式是做项目**。从你自己的需求出发——给你的笔记做一个智能搜索、给你的代码仓库做一个文档问答、给你的团队做一个内部知识助手。遇到问题再回来查文档，这比从头到尾读文档有效 10 倍。

> ⚠️ **从旧版迁移？** 如果你的项目还在使用 v0.2/v0.3 的 API（如 `create_tool_calling_agent`、`AgentExecutor`、`ConversationBufferMemory` 等），可以先安装 `pip install langchain-classic` 维持运行，然后逐步迁移到 v1.x 的 `create_agent` \+ LangGraph 架构。官方提供了详细的迁移指南。

</div>
