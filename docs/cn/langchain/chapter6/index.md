---
title: LangChain 实战教程（六）
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--agent">
  <div class="langchain-hero__eyebrow">LangChain 深度技术指南 · 第六篇</div>
  <div class="langchain-hero__headline">Agent / Tool / ReAct / create_agent</div>
  <p class="langchain-hero__subtitle">从固定流程转向目标驱动，把工具、推理循环与自主决策接入 LangChain 的 Agent 运行时。</p>
  <div class="langchain-hero__tags">
    <span>Agent</span>
    <span>Tool</span>
    <span>ReAct</span>
    <span>create_agent</span>
  </div>
</div>

<div class="langchain-series-heading">系列导航</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">第六篇 · 自治层</span>
    <span class="langchain-series-card__desc">围绕 Tool、ReAct、Tool Calling 与 `create_agent`，进入目标驱动的工具调用与自主决策。</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent · 当前阅读</span>
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
  <a class="langchain-series-card is-current" href="../chapter6/">
    <span class="langchain-series-card__kicker">第六篇 · 自治层</span>
    <span class="langchain-series-card__desc">围绕 Tool、ReAct、Tool Calling 与 `create_agent`，进入目标驱动的工具调用与自主决策。</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent · 当前阅读</span>
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

> 这一篇进入 LangChain 的自治层，围绕 Tool、ReAct 与 `create_agent`，理解模型如何在目标驱动下选择工具、规划步骤并完成任务。

---

## 6. Agent：让 LLM 自主决策和使用工具

Chain 是"你定好流程，LLM 按步骤执行"。Agent 则完全不同——**你只给 LLM 一个目标和一堆工具，让它自己决定用什么工具、按什么顺序完成任务**。

### 6.1 从 Chain 到 Agent：从"按剧本演"到"自主决策"
```

    Chain（链式调用）：
      你定义：Step1 → Step2 → Step3 → 输出
      LLM 只负责：执行每一步
      类比：流水线工人

    Agent（智能体）：
      你定义：目标 + 可用工具
      LLM 自己决定：用什么工具、按什么顺序、何时结束
      类比：独立做事的员工

```

**什么时候用 Agent？**

| 场景                | Chain 还是 Agent？ |
|-------------------|-----------------|
| 固定流程（翻译→润色→格式化）   | ✅ Chain         |
| 需要根据情况选择不同工具      | ✅ Agent         |
| 需要多次迭代（搜索→分析→再搜索） | ✅ Agent         |
| 用户意图不确定，需要 AI 判断  | ✅ Agent         |

### 6.2 Tool：教 LLM 使用工具

在 LangChain 中，Tool 就是**LLM 可以调用的函数**。用 `@tool` 装饰器定义最简单：
```

    from langchain_core.tools import tool

    @tool
    def multiply(a: int, b: int) -> int:
        """将两个数字相乘。当需要计算乘法时使用此工具。"""
        return a * b

    @tool
    def get_word_count(text: str) -> int:
        """统计文本中的字符数。"""
        return len(text)

    # Tool 对象有这些属性
    print(multiply.name)         # multiply
    print(multiply.description)  # 将两个数字相乘。当需要计算乘法时使用此工具。
    print(multiply.args_schema)  # 参数类型定义（自动从类型注解推断）

    # 直接调用
    print(multiply.invoke({"a": 6, "b": 7}))  # 42

```

**Tool 的 docstring 极其重要**——LLM 通过它来判断"什么时候该用这个工具"。写得越清晰，Agent 的决策越准确：
```

    # ❌ 差的描述
    @tool
    def search(query: str) -> str:
        """搜索"""  # LLM 不知道该在什么场景用
        ...

    # ✅ 好的描述
    @tool
    def search_web(query: str) -> str:
        """在互联网上搜索最新信息。当用户问到近期事件、实时数据、
        或你不确定的事实性问题时，使用此工具。"""
        ...

```

### 6.3 ReAct 模式：思考-行动-观察循环

LangChain 的 Agent 默认使用 **ReAct（Reasoning + Acting）** 模式——LLM 在每一步都会经历"思考→行动→观察"的循环：
```

    用户问题："北京今天的气温是多少摄氏度？换算成华氏度是多少？"

    🧠 思考：我需要先查北京的天气，获取气温，然后做单位换算。
    🔧 行动：调用 get_weather("北京") 工具
    👁️ 观察：返回结果 → "北京今天 22°C，晴"

    🧠 思考：气温是 22°C，我需要换算成华氏度。公式是 F = C × 9/5 + 32
    🔧 行动：调用 multiply(22, 9) 工具
    👁️ 观察：返回结果 → 198

    🧠 思考：198 / 5 + 32 = 71.6°F。我有了最终答案。
    💬 回答：北京今天 22°C（约 71.6°F），天气晴朗。

```

**用 LangChain 创建 Agent（v1.0 新 API）：**
```

    from langchain.agents import create_agent
    from langchain_deepseek import ChatDeepSeek

    # 创建模型实例
    llm = ChatDeepSeek(model="deepseek-chat")

    # 创建 Agent（基于 LangGraph 运行时）
    agent = create_agent(
        model=llm,  # 传入 ChatModel 实例（推荐），也可用 "deepseek:deepseek-chat" 字符串
        tools=[multiply, get_word_count],
        system_prompt="你是一个有帮助的助手。请使用提供的工具来回答问题。",
    )

    # 使用（输入格式为 messages 列表）
    result = agent.invoke({
        "messages": [{"role": "user", "content": "请计算 123 乘以 456"}]
    })
    print(result["messages"][-1].content)  # 56088

```

> 💡 **v1.0 重大变化：
>
>   * **旧 API（已迁移至` langchain-classic`）**：`create_tool_calling_agent()` \+ `AgentExecutor`，需要手动定义包含 `agent_scratchpad` 的 Prompt 模板
>   * **新 API：` create_agent()`**，只需传 `model`、`tools`、`system_prompt`，底层基于 LangGraph 运行，自动处理工具调用循环
>   * **`model` 参数**：推荐传入 ChatModel 实例（方便自定义 temperature 等），也可传 `"deepseek:deepseek-chat"` 字符串
>

### 6.4 自定义 Tool：让 Agent 调用你的 API

实际项目中，你需要让 Agent 调用自己的业务 API。下面展示如何把任何 Python 函数变成 Agent 可用的工具：
```

    from langchain_core.tools import tool
    import httpx

    @tool
    def search_knowledge_base(query: str) -> str:
        """搜索内部知识库。当用户问到公司产品、内部文档、业务流程相关的问题时使用。"""
        # 调用你自己的 API
        response = httpx.get(
            "http://localhost:8000/api/search",
            params={"q": query, "limit": 3},
        )
        results = response.json()
        return "\n".join(r["content"] for r in results)

    @tool
    def create_ticket(title: str, description: str, priority: str = "medium") -> str:
        """创建一个工单/任务。当用户要求创建任务、报告问题、提交需求时使用。
        priority 可选值：low, medium, high, urgent
        """
        response = httpx.post(
            "http://localhost:8000/api/tickets",
            json={"title": title, "description": description, "priority": priority},
        )
        ticket = response.json()
        return f"✅ 已创建工单 #{ticket['id']}: {title}"

    @tool
    def get_current_time() -> str:
        """获取当前时间。当用户问到现在几点、今天日期时使用。"""
        from datetime import datetime
        return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

```

> 💡 **安全提示**：Agent 能调用你给它的任何工具。在生产环境中，务必对工具的输入做校验、限制权限范围、记录调用日志。不要给 Agent 直接执行 SQL 或 shell 命令的权限。

### 6.5 实战：能搜索 + 计算 + 查天气的智能助手

构建一个综合能力的智能助手——同时拥有搜索、计算、时间查询等多种工具：
```

    from langchain.agents import create_agent
    from langchain_core.tools import tool

    # ── 定义工具集 ──
    @tool
    def calculator(expression: str) -> str:
        """计算数学表达式。支持加减乘除、幂运算等。
        例如：'2 + 3 * 4'、'2 ** 10'、'100 / 7'"""
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            return str(result)
        except Exception as e:
            return f"计算错误: {e}"

    @tool
    def get_current_time() -> str:
        """获取当前日期和时间。"""
        from datetime import datetime
        return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

    @tool
    def string_length(text: str) -> int:
        """统计字符串的长度（字符数）。"""
        return len(text)

    @tool
    def text_to_uppercase(text: str) -> str:
        """将英文文本转换为大写。"""
        return text.upper()

    # ── 组装 Agent（v1.0 新 API） ──
    tools = [calculator, get_current_time, string_length, text_to_uppercase]

    llm = ChatDeepSeek(model="deepseek-chat")

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="""你是一个多功能 AI 助手，拥有以下工具：
    - 计算器：数学计算
    - 时间查询：获取当前时间
    - 字符串工具：统计长度、转大写

    请根据用户需求选择合适的工具。如果不需要工具，直接回答即可。""",
    )

    # ── 测试 ──
    # 需要工具的问题
    result = agent.invoke({
        "messages": [{"role": "user", "content": "2 的 20 次方是多少？"}]
    })
    print(result["messages"][-1].content)
    # Agent 会调用 calculator("2 ** 20") → 1048576

    # 多步骤推理
    result = agent.invoke({
        "messages": [{"role": "user", "content": "现在几点了？距离晚上 10 点还有多久？"}]
    })
    print(result["messages"][-1].content)
    # Agent 会先调用 get_current_time()，然后自己计算时差

    # 不需要工具的问题
    result = agent.invoke({
        "messages": [{"role": "user", "content": "你好，介绍一下你自己"}]
    })
    print(result["messages"][-1].content)
    # Agent 直接回答，不调用任何工具

```

### 6.6 中间件（Middleware）：控制 Agent 的执行流程（v1.0 新增）

v1.0 引入了**中间件系统**，可以在 Agent 执行循环的关键节点插入自定义逻辑。最常用的是 **Human-in-the-Loop（人工审批）**——让 Agent 在调用敏感工具前暂停，等待人工确认：
```

    from langchain.agents import create_agent
    from langchain.agents.middleware import HumanInTheLoopMiddleware
    from langgraph.checkpoint.memory import InMemorySaver

    # 配置人工审批中间件
    hitl = HumanInTheLoopMiddleware(
        interrupt_on={
            "create_ticket": True,      # 创建工单前需要人工确认
            "delete_database": {"allowed_decisions": ["approve", "reject"]},
        }
    )

    # 创建带中间件的 Agent
    agent = create_agent(
        model=ChatDeepSeek(model="deepseek-chat"),
        tools=tools,
        middleware=[hitl],
        checkpointer=InMemorySaver(),  # 中间件需要状态持久化
    )

```

**中间件的工作流程：**
```

    用户请求 → Agent 决定调用 create_ticket
           → HumanInTheLoopMiddleware 拦截
           → Agent 暂停，等待人工决策
           → 人工选择：approve / edit / reject
           → Agent 继续执行（或放弃该工具调用）

```

> 💡 **中间件不只有 HITL**——你可以用中间件实现：摘要压缩（防止上下文过长）、PII 脱敏（自动移除敏感信息）、成本追踪（统计 token 用量）等。

**第 6 章核心知识回顾：**

| 概念               | 一句话解释                                 |
|------------------|---------------------------------------|
| **Agent**        |  LLM 自主决策用什么工具、按什么顺序完成任务              |
| **Tool**         |  LLM 可调用的函数，用 `@tool` 定义              |
| **ReAct**        |  思考→行动→观察的循环决策模式                      |
| **create_agent** |  v1.0 统一的 Agent 创建接口，基于 LangGraph 运行时 |
| **docstring**    |  Tool 的描述决定了 LLM 何时选用该工具              |
| **Middleware**   |  v1.0 新增的中间件系统，支持人工审批等控制              |

</div>
