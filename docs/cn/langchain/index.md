---
title: LangChain深度技术指南：写在开头
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--guide">
  <div class="langchain-hero__eyebrow">LangChain 深度技术指南</div>
  <div class="langchain-hero__headline">从框架抽象到工程落地的一条完整学习线</div>
  <p class="langchain-hero__subtitle">这一部分承接 AI Agent 的能力设计，再往下一层拆解 LangChain 的组件边界、编排方式、记忆管理，以及后续 RAG / Agent / LangGraph 的工程实现路径。</p>
  <div class="langchain-hero__tags">
    <span>Framework Abstractions</span>
    <span>LCEL</span>
    <span>Memory</span>
    <span>RAG → Agent → LangGraph</span>
  </div>
</div>

LangChain 深度技术指南这一部分，延续的是“Agent 能力设计 -> 框架抽象 -> 工程落地”这条主线，专门回答一个更具体的问题：当系统级能力真正落到 LangChain 时，组件、编排与状态究竟怎样组织。

如果说“AI Agent 智能体”更关注记忆、规划、协作与安全这些系统级问题，那么这里就继续往下一层，集中拆解：

- LangChain 的核心抽象是怎样分层的
- `Runnable` / `LCEL` 如何把提示词、模型、检索和工具串成可组合管线
- Tool Calling、Agent、LangGraph 分别适合什么任务形态
- RAG、状态管理、可观测性怎样真正进入生产环境

这一部分会和“AI Agent智能体”“AI大模型架构解析”形成一条连续的学习路径：

- AI Agent智能体：讲系统能力设计
- LangChain深度技术指南：讲主流框架抽象与工程实现
- AI大模型架构解析：讲模型本身的能力边界与推理机制

<div class="langchain-series-heading">系列导航</div>

<div class="langchain-series-grid langchain-series-grid--overview">
  <a class="langchain-series-card" href="./chapter1/">
    <span class="langchain-series-card__kicker">第一篇 · 总览</span>
    <span class="langchain-series-card__desc">先回答为什么需要 LangChain，并建立模块地图、版本演进和整体学习路径。</span>
    <span class="langchain-series-card__meta">Framework Positioning · Module Map</span>
  </a>
  <a class="langchain-series-card" href="./chapter2/">
    <span class="langchain-series-card__kicker">第二篇 · 接口层</span>
    <span class="langchain-series-card__desc">聚焦 Model I/O、PromptTemplate、OutputParser 与结构化输出，先把输入输出接口层打稳。</span>
    <span class="langchain-series-card__meta">ChatModel · PromptTemplate · Structured Output</span>
  </a>
  <a class="langchain-series-card" href="./chapter3/">
    <span class="langchain-series-card__kicker">第三篇 · 编排层</span>
    <span class="langchain-series-card__desc">从接口层进入编排层，理解 Chain、LCEL、并行链与流式工作流是如何组织起来的。</span>
    <span class="langchain-series-card__meta">Chain · LCEL · RunnableParallel · Streaming</span>
  </a>
  <a class="langchain-series-card" href="./chapter4/">
    <span class="langchain-series-card__kicker">第四篇 · 状态层</span>
    <span class="langchain-series-card__desc">聚焦 Memory、会话级历史管理与摘要记忆，补齐多轮对话里的状态与上下文管理。</span>
    <span class="langchain-series-card__meta">Memory · Session History · Summary Memory</span>
  </a>
  <a class="langchain-series-card" href="./chapter5/">
    <span class="langchain-series-card__kicker">第五篇 · 知识层</span>
    <span class="langchain-series-card__desc">围绕 Document Loaders、Text Splitter、Embedding、VectorStore 与 Retriever，搭建完整的 RAG 检索增强链路。</span>
    <span class="langchain-series-card__meta">RAG · Embeddings · Vector Store · Retriever</span>
  </a>
  <a class="langchain-series-card" href="./chapter6/">
    <span class="langchain-series-card__kicker">第六篇 · 自治层</span>
    <span class="langchain-series-card__desc">围绕 Tool、ReAct、Tool Calling 与 `create_agent`，进入目标驱动的工具调用与自主决策。</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent</span>
  </a>
  <a class="langchain-series-card" href="./chapter7/">
    <span class="langchain-series-card__kicker">第七篇 · 项目层</span>
    <span class="langchain-series-card__desc">把 Model I/O、Memory 与 RAG 组合成一个可上传文档、支持检索和流式响应的知识库助手。</span>
    <span class="langchain-series-card__meta">FastAPI · Chroma · Streaming · Integrated Project</span>
  </a>
  <a class="langchain-series-card" href="./chapter8/">
    <span class="langchain-series-card__kicker">第八篇 · 生态层</span>
    <span class="langchain-series-card__desc">介绍 LangSmith、LangGraph 与主流框架对比，建立 LangChain 后续工程深化与选型视角。</span>
    <span class="langchain-series-card__meta">LangSmith · LangGraph · Ecosystem · Comparison</span>
  </a>
</div>

你会在这里看到的主题包括：

- LangChain 核心组件与版本演进
- Prompt / Runnable / Output Parser 的组合方式
- RAG 链路、Retriever 设计与上下文注入
- Tool Calling、Agent、LangGraph 的边界与取舍
- 观测、评估、缓存、持久化与生产化实践

当前已上线：

- [第一篇：LangChain 实战教程（一）](./chapter1/)
- [第二篇：LangChain 实战教程（二）](./chapter2/)
- [第三篇：LangChain 实战教程（三）](./chapter3/)
- [第四篇：LangChain 实战教程（四）](./chapter4/)
- [第五篇：LangChain 实战教程（五）](./chapter5/)
- [第六篇：LangChain 实战教程（六）](./chapter6/)
- [第七篇：LangChain 实战教程（七）](./chapter7/)
- [第八篇：LangChain 实战教程（八）](./chapter8/)

建议阅读顺序：

1. 先读第一篇，建立 LangChain 这条“框架工程线”的整体地图
2. 接着读第二篇，先把 `Model I/O` 这一层的模型调用、Prompt 模板和结构化输出接口吃透
3. 然后读第三篇，建立 `LCEL`、`RunnableParallel` 与流式输出这些编排层概念
4. 再读第四篇，补上 `Memory`、会话历史管理和摘要记忆的工程实现
5. 随后进入第五篇，把 `RAG` 的文档加载、切分、向量化与检索链路串起来
6. 接着阅读第六篇，理解 `Agent`、`Tool` 与 `create_agent` 这条自主决策主线
7. 再看第七篇，把前面模块真正组合成一个可运行的知识库助手项目
8. 最后阅读第八篇，补上 `LangSmith`、`LangGraph` 与框架选型这条生态进阶线

</div>
