---
title: LangChain 实战教程（四）
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--memory">
  <div class="langchain-hero__eyebrow">LangChain 深度技术指南 · 第四篇</div>
  <div class="langchain-hero__headline">Memory / 会话历史 / 摘要记忆</div>
  <p class="langchain-hero__subtitle">让模型“记住上下文”并不是魔法，而是应用层对历史消息和状态的持续管理。这一篇把多轮对话中的记忆机制和工程实现路线讲清楚。</p>
  <div class="langchain-hero__tags">
    <span>ChatMessageHistory</span>
    <span>RunnableWithMessageHistory</span>
    <span>Summary Memory</span>
    <span>Session State</span>
  </div>
</div>


<div class="langchain-series-heading">系列导航</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">第四篇 · 状态层</span>
    <span class="langchain-series-card__desc">聚焦 Memory、会话级历史管理与摘要记忆，补齐多轮对话里的状态与上下文管理。</span>
    <span class="langchain-series-card__meta">Memory · Session History · Summary Memory · 当前阅读</span>
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
  <a class="langchain-series-card is-current" href="../chapter4/">
    <span class="langchain-series-card__kicker">第四篇 · 状态层</span>
    <span class="langchain-series-card__desc">聚焦 Memory、会话级历史管理与摘要记忆，补齐多轮对话里的状态与上下文管理。</span>
    <span class="langchain-series-card__meta">Memory · Session History · Summary Memory · 当前阅读</span>
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

> 这一篇进入 LangChain 的状态层，围绕 Memory、会话历史与摘要记忆，理解多轮对话中的上下文如何被保存、压缩与调用。

---

## 4. Memory：让 LLM 拥有记忆

你有没有发现，每次调用 LLM 都像是“第一次见面”？它完全不记得上一轮你说了什么。这一章解决这个问题——让你的 AI 应用拥有**多轮对话记忆**。

### 4.1 LLM 为什么“没有记忆”？

LLM 本身是**无状态的**。每次调用都是独立的——模型不会自动保存上一次的对话内容。

```python
llm = ChatDeepSeek(model="deepseek-chat")

# 第 1 轮
response1 = llm.invoke("我叫小明")
print(response1.content)  # 你好小明！很高兴认识你！

# 第 2 轮
response2 = llm.invoke("我叫什么名字？")
print(response2.content)  # 抱歉，我不知道你叫什么名字。 ← 完全忘了！
```

**为什么？** 因为第 2 轮调用时，API 收到的只有 `"我叫什么名字？"` 这一条消息。第 1 轮的对话内容根本没有传过去。

**“记忆”的本质就是：把历史对话拼接到新请求里。**

```python
from langchain_core.messages import HumanMessage, AIMessage

# 手动拼接历史 → LLM 就“记住”了
messages = [
    HumanMessage(content="我叫小明"),
    AIMessage(content="你好小明！很高兴认识你！"),  # 上一轮的回复
    HumanMessage(content="我叫什么名字？"),          # 新问题
]

response = llm.invoke(messages)
print(response.content)  # 你叫小明！ ← 记住了！
```

> 💡 核心认知：LLM 的“记忆”不是模型内部的功能，而是应用层的工作——你需要在每次请求时，把之前的对话历史拼到 `messages` 里发过去。LangChain 的 Memory 模块就是帮你自动化这个过程。

### 4.2 ConversationBufferMemory：完整对话记忆

在 LangChain 的最新 LCEL 架构里，推荐的方式是用 `ChatMessageHistory` + `RunnableWithMessageHistory` 来管理记忆：

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatDeepSeek(model="deepseek-chat")

# ── Step 1：定义带历史占位符的 Prompt ──
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。"),
    MessagesPlaceholder(variable_name="chat_history"),  # 历史消息插入这里
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# ── Step 2：创建会话存储（按 session_id 隔离） ──
store = {}  # 简单的内存存储

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# ── Step 3：包装成带记忆的链 ──
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# ── 使用：同一个 session_id 的对话共享记忆 ──
config = {"configurable": {"session_id": "user_001"}}

print(chain_with_memory.invoke({"input": "我叫小明，我是一个 Python 程序员"}, config=config))
# 你好小明！很高兴认识你，Python 是一门很棒的语言！

print(chain_with_memory.invoke({"input": "我叫什么？我的职业是什么？"}, config=config))
# 你叫小明，你是一个 Python 程序员！ ← 完美记住了！

# 不同 session_id = 不同的对话记忆
config2 = {"configurable": {"session_id": "user_002"}}
print(chain_with_memory.invoke({"input": "我叫什么？"}, config=config2))
# 抱歉，你还没有告诉我你的名字。 ← 新会话，没有记忆
```

**记忆的工作流程：**

```text
用户发送 “我叫什么名字？”
       │
       ▼
RunnableWithMessageHistory：
  1. 根据 session_id 取出历史消息
  2. 把历史 + 新消息组装成完整 messages
  3. 发送给 LLM
  4. 把新的问答对存回历史
       │
       ▼
LLM 收到的实际消息：
  [system] 你是一个友好的助手。
  [human]  我叫小明，我是 Python 程序员   ← 历史
  [ai]     你好小明！...                  ← 历史
  [human]  我叫什么名字？                  ← 新消息
```

> 💡 Buffer 记忆的问题：随着对话轮数增加，历史消息会越来越长，最终超出模型的 context window。解决方案：摘要记忆。

### 4.3 ConversationSummaryMemory：摘要式记忆

当对话很长时（几十轮甚至上百轮），把所有历史消息都塞进 prompt 会**撑爆 context window**。摘要记忆的思路是：**用 LLM 把之前的对话压缩成一段摘要**，而不是保留完整历史。

```python
from langchain_core.messages import HumanMessage, AIMessage

def summarize_history(llm, messages, max_messages=6):
    """
    当历史消息超过 max_messages 条时，
    用 LLM 生成摘要来替代旧消息
    """
    if len(messages) <= max_messages:
        return messages  # 没超限，直接返回

    # 取出需要被压缩的旧消息
    old_messages = messages[:-max_messages]
    recent_messages = messages[-max_messages:]

    # 用 LLM 生成摘要
    old_text = "\n".join(
        f"{'用户' if isinstance(m, HumanMessage) else 'AI'}: {m.content}"
        for m in old_messages
    )

    summary = llm.invoke(
        f"请用 2-3 句话总结以下对话的关键信息：\n\n{old_text}"
    ).content

    # 返回：摘要 + 最近的消息
    from langchain_core.messages import SystemMessage
    return [SystemMessage(content=f"之前对话的摘要：{summary}")] + recent_messages
```

**三种记忆策略对比：**

| 策略 | 原理 | 优点 | 缺点 |
| --- | --- | --- | --- |
| Buffer | 保留全部历史 | 信息无损 | 长对话会超出 token 限制 |
| Summary | 旧消息压缩为摘要 | 支持超长对话 | 摘要可能丢失细节 |
| Window | 只保留最近 N 轮 | 简单高效 | 完全丢失早期信息 |

> 💡 生产环境推荐：混合策略——最近 5-10 轮用 Buffer（保留细节），更早的部分用 Summary（压缩但不丢失关键信息）。

### 4.4 实战：构建一个有上下文的多轮对话机器人

把前面学的组合起来，构建一个完整的多轮对话机器人，支持**角色设定、记忆管理、流式输出**：

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# ── 配置 ──
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    streaming=True,  # 启用流式
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个名叫“小智”的 AI 编程助手。
你的特点：
- 擅长 Python、JavaScript、Rust
- 回答简洁，代码示例清晰
- 会记住用户之前说过的话，主动关联上下文"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# ── 记忆管理 ──
store = {}

def get_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chatbot = RunnableWithMessageHistory(
    chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# ── 交互循环 ──
def chat(session_id="default"):
    config = {"configurable": {"session_id": session_id}}
    print("🤖 小智：你好！我是 AI 编程助手小智，有什么可以帮你的？")
    print("（输入 'quit' 退出）\n")

    while True:
        user_input = input("你：")
        if user_input.lower() == "quit":
            break

        print("🤖 小智：", end="")
        # 流式输出
        for chunk in chatbot.stream({"input": user_input}, config=config):
            print(chunk, end="", flush=True)
        print("\n")

# chat()  # 取消注释即可运行
```

**第 4 章核心知识回顾：**

| 概念 | 一句话解释 |
| --- | --- |
| LLM 无状态 | 每次调用独立，需要应用层管理记忆 |
| Buffer 记忆 | 保留完整历史，简单但有 token 限制 |
| Summary 记忆 | 压缩旧对话为摘要，支持长对话 |
| RunnableWithMessageHistory | 简单链的记忆管理方式 |
| LangGraph Checkpointer | Agent 场景推荐，持久化完整图状态（v1.0） |
| session_id | 用于隔离不同用户 / 会话的记忆 |

> 💡 v1.0 记忆管理策略选择：简单聊天链继续用 `RunnableWithMessageHistory`，够轻、够直接；Agent 或复杂工作流则更推荐 `LangGraph + Checkpointer`（如 `MemorySaver`、`PostgresSaver`），因为它可以持久化完整图状态。旧版 `ConversationBufferMemory` 等接口已经弃用，新项目不建议继续使用。

</div>
