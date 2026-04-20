---
title: LangChain 实战教程（三）
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--chain">
  <div class="langchain-hero__eyebrow">LangChain 深度技术指南 · 第三篇</div>
  <div class="langchain-hero__headline">Chain / LCEL / RunnableParallel / 流式输出</div>
  <p class="langchain-hero__subtitle">从单条 Runnable 管线进入真正的工作流编排层，把提示词、模型与中间处理步骤组织成可组合、可并行、可流式的 LLM 工作流。</p>
  <div class="langchain-hero__tags">
    <span>LCEL</span>
    <span>RunnableParallel</span>
    <span>Streaming</span>
    <span>Workflow Orchestration</span>
  </div>
</div>


<div class="langchain-series-heading">系列导航</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">第三篇 · 编排层</span>
    <span class="langchain-series-card__desc">从接口层进入编排层，理解 Chain、LCEL、并行链与流式工作流是如何组织起来的。</span>
    <span class="langchain-series-card__meta">Chain · LCEL · RunnableParallel · Streaming · 当前阅读</span>
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
  <a class="langchain-series-card is-current" href="../chapter3/">
    <span class="langchain-series-card__kicker">第三篇 · 编排层</span>
    <span class="langchain-series-card__desc">从接口层进入编排层，理解 Chain、LCEL、并行链与流式工作流是如何组织起来的。</span>
    <span class="langchain-series-card__meta">Chain · LCEL · RunnableParallel · Streaming · 当前阅读</span>
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

> 这一篇进入 LangChain 的编排层，围绕 Chain、LCEL、`RunnableParallel` 与流式工作流，理解多步骤 LLM 流程如何被组合与执行。

---

## 3. Chain：用链式调用编排 LLM 工作流

上一章的 `prompt | llm | parser` 其实已经是一条 Chain 了。这一章深入 LangChain 的**编排核心—— LCEL（LangChain Expression Language）**，学习如何用最优雅的方式组合复杂的多步骤工作流。

### 3.1 LCEL（LangChain Expression Language）入门

LCEL 是 LangChain 的核心编排方式（始于 v0.2，v1.x 延续）。它的核心思想极其简单：**所有组件都实现 `Runnable` 接口，用 `|` 串联。**

```ini
# LCEL 的核心理念：
# 任何实现了 Runnable 接口的对象，都可以用 | 串联

chain = component_a | component_b | component_c

# 等价于：
# result = component_c.invoke(component_b.invoke(component_a.invoke(input)))
# 但 LCEL 写法更简洁，而且自动支持：流式、异步、批量、并行
```

**Runnable 接口提供的方法：**

| 方法 | 作用 | 适用场景 |
| --- | --- | --- |
| invoke(input) | 同步调用，返回完整结果 | 最常用 |
| ainvoke(input) | 异步调用 | FastAPI 等异步框架 |
| stream(input) | 流式输出（逐 token 返回） | 聊天界面 |
| batch([input1, input2]) | 批量调用 | 批处理任务 |

### 3.2 管道操作符 `|`：像搭积木一样组合

`|` 操作符把多个组件**串联成一条流水线**——前一个组件的输出，自动变成后一个组件的输入：

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatDeepSeek(model="deepseek-chat")

# ── 链 1：生成代码 ──
code_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个 Python 专家。只返回代码，不要解释。"),
    ("human", "写一个{task}的函数"),
])

code_chain = code_prompt | llm | StrOutputParser()

# ── 链 2：解释代码 ──
explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个编程老师。用中文逐行解释下面的代码。"),
    ("human", "{code}"),
])

explain_chain = explain_prompt | llm | StrOutputParser()

# ── 串联两条链：生成代码 → 解释代码 ──
from langchain_core.runnables import RunnablePassthrough

full_chain = (
    code_chain                                     # Step 1: 生成代码
    | (lambda code: {"code": code})                # 把字符串包装成字典
    | explain_chain                                # Step 2: 解释代码
)

result = full_chain.invoke({"task": "快速排序"})
print(result)
# 逐行解释快速排序的 Python 实现...
```

**用 `RunnableLambda` 替代裸 lambda（推荐）：**

```python
from langchain_core.runnables import RunnableLambda

# 自定义中间处理步骤
def format_as_input(code_text: str) -> dict:
    """把上一步的纯文本输出，转成下一步需要的字典格式"""
    return {"code": code_text}

full_chain = code_chain | RunnableLambda(format_as_input) | explain_chain
```

### 3.3 RunnableParallel：并行执行多条链

有时候你需要**同时执行多个任务**，然后把结果合并。`RunnableParallel` 正是干这个的：

```python
from langchain_core.runnables import RunnableParallel

# 定义三条并行链
summary_chain = (
    ChatPromptTemplate.from_template("用一句话总结：{text}")
    | llm | StrOutputParser()
)

keywords_chain = (
    ChatPromptTemplate.from_template("提取 5 个关键词（用逗号分隔）：{text}")
    | llm | StrOutputParser()
)

sentiment_chain = (
    ChatPromptTemplate.from_template("分析情感倾向（正面/负面/中性）：{text}")
    | llm | StrOutputParser()
)

# 用 RunnableParallel 并行执行
analysis_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    sentiment=sentiment_chain,
)

result = analysis_chain.invoke({
    "text": "LangChain 是一个强大的 LLM 应用开发框架，但学习曲线比较陡峭。"
})

print(result)
# {
#   'summary': 'LangChain 是强大但学习成本高的 LLM 框架。',
#   'keywords': 'LangChain, LLM, 框架, 学习曲线, 应用开发',
#   'sentiment': '中性（既肯定了优势，也指出了不足）'
# }
```

```text
RunnableParallel 的执行方式：

                    ┌─ summary_chain ──→ summary
input ──→ 复制 3 份 ├─ keywords_chain ──→ keywords    ──→ 合并为字典
                    └─ sentiment_chain ─→ sentiment
```

> 💡 并行 ≠ 多线程。`RunnableParallel` 在同步模式下通常表现为顺序调用（但每次 API 请求本身是 I/O 等待），在 `ainvoke()` 异步模式下才是真正的并发请求。生产环境建议优先使用异步。

### 3.4 流式输出：一个字一个字吐出来

ChatGPT 那种“打字机效果”是怎么实现的？用 `stream()` 方法：

```python
chain = (
    ChatPromptTemplate.from_template("写一首关于{topic}的五言绝句")
    | llm
    | StrOutputParser()
)

# ── 流式输出 ──
for chunk in chain.stream({"topic": "秋天"}):
    print(chunk, end="", flush=True)
# 秋｜风｜吹｜落｜叶，
# 寒｜露｜染｜山｜红。
# ...
```

**在 FastAPI 中做流式响应：**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/chat")
async def chat(question: str):
    chain = prompt | llm | StrOutputParser()

    async def generate():
        async for chunk in chain.astream({"question": question}):
            yield chunk  # 一个 token 一个 token 发给前端

    return StreamingResponse(generate(), media_type="text/plain")
```

> 💡 关键区别：`invoke()` 要等所有 token 全部生成后才返回，`stream()` / `astream()` 会边生成边返回，用户体感会好很多。LCEL 的一大优势正是：**你用 `|` 组装出来的链，天然就支持流式输出**，不需要再单独改一套代码。

### 3.5 实战：多步骤内容生成管线

构建一个“技术博客自动生成器”：输入一个主题 → 并行生成大纲和关键要点 → 根据大纲撰写全文：

```python
from langchain_core.runnables import RunnableParallel

# ── Step 1：并行生成大纲 + 关键要点 ──
outline_chain = (
    ChatPromptTemplate.from_template(
        "为主题「{topic}」生成一篇技术博客的大纲（3-5 个章节标题）"
    )
    | llm | StrOutputParser()
)

points_chain = (
    ChatPromptTemplate.from_template(
        "列出关于「{topic}」最重要的 5 个技术要点（简短的要点列表）"
    )
    | llm | StrOutputParser()
)

parallel_step = RunnableParallel(outline=outline_chain, key_points=points_chain)

# ── Step 2：根据大纲和要点撰写全文 ──
write_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "你是一个技术博客作者。根据给定的大纲和关键要点，撰写一篇完整的博客文章。"),
        ("human", "大纲：\n{outline}\n\n关键要点：\n{key_points}\n\n请撰写完整文章。"),
    ])
    | llm | StrOutputParser()
)

# ── 组合完整管线 ──
blog_pipeline = parallel_step | write_chain

# 使用
article = blog_pipeline.invoke({"topic": "Python 异步编程入门"})
print(article)
```

**管线执行流程：**

```text
                    ┌─ outline_chain ──→ outline ─┐
{"topic": "..."} ──→                               ├──→ write_chain ──→ 完整文章
                    └─ points_chain ──→ key_points ┘
```

**第 3 章核心知识回顾：**

| 概念 | 一句话解释 |
| --- | --- |
| LCEL | LangChain 的编排语言，所有组件通过 `\|` 串联 |
| Runnable | 统一接口，支持 invoke / stream / batch / ainvoke |
| RunnableParallel | 并行执行多条链，结果合并为字典 |
| RunnableLambda | 把普通函数包装成 Runnable，插入管道中 |
| stream() | 流式输出，打字机效果 |

</div>
