---
title: "LangChain in Practice (VI)"
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--agent">
  <div class="langchain-hero__eyebrow">LangChain Deep Guide · Article 6</div>
  <div class="langchain-hero__headline">Agent / Tool / ReAct / create_agent</div>
  <p class="langchain-hero__subtitle">This article moves from fixed pipelines to goal-driven execution and shows how LangChain agents choose tools, plan steps, and complete work autonomously.</p>
  <div class="langchain-hero__tags">
    <span>Agent</span>
    <span>Tool</span>
    <span>ReAct</span>
    <span>create_agent</span>
  </div>
</div>

<div class="langchain-series-heading">Series Navigation</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">Article 6 · Autonomy Layer</span>
    <span class="langchain-series-card__desc">Move from fixed pipelines to goal-driven execution with tools, ReAct loops, tool calling, and `create_agent`.</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent · You are here</span>
    </span>
    <span class="langchain-series-disclosure__toggle">
      <span class="langchain-series-disclosure__toggle-closed">Expand full series</span>
      <span class="langchain-series-disclosure__toggle-opened">Collapse series</span>
    </span>
  </summary>

  <div class="langchain-series-grid langchain-series-grid--compact">
  <a class="langchain-series-card" href="../chapter1/">
    <span class="langchain-series-card__kicker">Article 1 · Overview</span>
    <span class="langchain-series-card__desc">Start with why LangChain matters, then build the module map, version context, and overall learning path.</span>
    <span class="langchain-series-card__meta">Framework Positioning · Module Map</span>
  </a>
  <a class="langchain-series-card" href="../chapter2/">
    <span class="langchain-series-card__kicker">Article 2 · Interface Layer</span>
    <span class="langchain-series-card__desc">Focus on Model I/O, PromptTemplate, OutputParser, and structured output so the input-output contract becomes stable first.</span>
    <span class="langchain-series-card__meta">ChatModel · PromptTemplate · Structured Output</span>
  </a>
  <a class="langchain-series-card" href="../chapter3/">
    <span class="langchain-series-card__kicker">Article 3 · Orchestration Layer</span>
    <span class="langchain-series-card__desc">Move from interfaces into orchestration and see how Chain, LCEL, parallel branches, and streaming workflows fit together.</span>
    <span class="langchain-series-card__meta">Chain · LCEL · RunnableParallel · Streaming</span>
  </a>
  <a class="langchain-series-card" href="../chapter4/">
    <span class="langchain-series-card__kicker">Article 4 · State Layer</span>
    <span class="langchain-series-card__desc">Focus on Memory, session-scoped history, and summary-based memory to complete the story of multi-turn state handling.</span>
    <span class="langchain-series-card__meta">Memory · Session History · Summary Memory</span>
  </a>
  <a class="langchain-series-card" href="../chapter5/">
    <span class="langchain-series-card__kicker">Article 5 · Knowledge Layer</span>
    <span class="langchain-series-card__desc">Build the full RAG path around Document Loaders, Text Splitter, Embeddings, VectorStore, and Retriever.</span>
    <span class="langchain-series-card__meta">RAG · Embeddings · Vector Store · Retriever</span>
  </a>
  <a class="langchain-series-card is-current" href="../chapter6/">
    <span class="langchain-series-card__kicker">Article 6 · Autonomy Layer</span>
    <span class="langchain-series-card__desc">Move from fixed pipelines to goal-driven execution with tools, ReAct loops, tool calling, and `create_agent`.</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent · You are here</span>
  </a>
  <a class="langchain-series-card" href="../chapter7/">
    <span class="langchain-series-card__kicker">Article 7 · Project Layer</span>
    <span class="langchain-series-card__desc">Combine Model I/O, Memory, and RAG into a document-upload, retrieval-enabled knowledge assistant with streaming responses.</span>
    <span class="langchain-series-card__meta">FastAPI · Chroma · Streaming · Integrated Project</span>
  </a>
  <a class="langchain-series-card" href="../chapter8/">
    <span class="langchain-series-card__kicker">Article 8 · Ecosystem Layer</span>
    <span class="langchain-series-card__desc">Finish with LangSmith, LangGraph, and a comparison of major frameworks so the ecosystem picture becomes clear.</span>
    <span class="langchain-series-card__meta">LangSmith · LangGraph · Ecosystem · Comparison</span>
  </a>
  </div>
</details>

> This article moves into LangChain's autonomy layer and focuses on Tools, ReAct, and `create_agent` so you can see how a model selects tools, plans steps, and completes tasks toward a goal.

---

## 6. Agents: Let an LLM Decide and Use Tools

A Chain means **you define the workflow** and the LLM follows it. An Agent is different: **you give the model a goal plus a set of tools, and it decides which tool to use, in what order, and when it has enough information to stop**.

### 6.1 From Chain to Agent: From Scripted Flow to Autonomous Decisions

```text
Chain:
  you define Step 1 -> Step 2 -> Step 3 -> output
  the LLM executes each step inside that fixed pipeline
  analogy: assembly-line worker

Agent:
  you define a goal + available tools
  the LLM decides which tool to use, in what order, and when to finish
  analogy: an employee solving a problem independently
```

**When should you use an Agent?**

| Scenario | Better fit |
| --- | --- |
| Fixed workflow such as translate -> polish -> format | ✅ Chain |
| Tool choice depends on the situation | ✅ Agent |
| The model may need multiple rounds like search -> analyze -> search again | ✅ Agent |
| User intent is ambiguous and the model must decide | ✅ Agent |

### 6.2 Tools: Teach an LLM How to Act

In LangChain, a Tool is simply **a function the model is allowed to call**. The easiest way to define one is with the `@tool` decorator:

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers. Use this tool when multiplication is needed."""
    return a * b

@tool
def get_word_count(text: str) -> int:
    """Count the number of characters in a text."""
    return len(text)

print(multiply.name)         # multiply
print(multiply.description)  # Multiply two numbers. Use this tool when multiplication is needed.
print(multiply.args_schema)  # inferred automatically from type annotations

print(multiply.invoke({"a": 6, "b": 7}))  # 42
```

**The docstring is extremely important.** The model relies on it to infer when a tool should be used.

```python
# Bad: too vague
@tool
def search(query: str) -> str:
    """Search"""
    ...

# Better: tells the model when this tool is appropriate
@tool
def search_web(query: str) -> str:
    """Search the web for recent information. Use this when the user asks about recent events,
    real-time data, or factual topics you are uncertain about."""
    ...
```

### 6.3 The ReAct Pattern: Think -> Act -> Observe

Most LangChain agent loops follow the **ReAct (Reasoning + Acting)** pattern. At each step, the model goes through a cycle of thinking, acting, and observing the result.

```text
User: "What is today's temperature in Beijing, and what is that in Fahrenheit?"

Think: I need the weather first, then I need a unit conversion.
Act:   call get_weather("Beijing")
Observe: "22 C, sunny"

Think: I now have 22 C. Convert it with F = C * 9 / 5 + 32.
Act:   call multiply(22, 9)
Observe: 198

Think: 198 / 5 + 32 = 71.6 F. I have the final answer.
Answer: "Beijing is 22 C today, about 71.6 F, and the weather is sunny."
```

**Create an agent in LangChain v1.0:**

```python
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(model="deepseek-chat")

agent = create_agent(
    model=llm,
    tools=[multiply, get_word_count],
    system_prompt="You are a helpful assistant. Use the provided tools when they are relevant.",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Please calculate 123 multiplied by 456"}]
})
print(result["messages"][-1].content)
```

> 💡 **Important v1.0 shift:** older APIs such as `create_tool_calling_agent()` plus `AgentExecutor` were moved toward the `langchain-classic` compatibility path. The modern default is `create_agent()`, which runs on top of the LangGraph runtime and manages the tool loop for you.

### 6.4 Custom Tools: Let the Agent Call Your APIs

In real systems, an Agent usually needs to call internal APIs, business actions, or support workflows. Any Python function can become a Tool:

```python
from langchain_core.tools import tool
import httpx

@tool
def search_knowledge_base(query: str) -> str:
    """Search the internal knowledge base. Use this when the user asks about company products,
    internal documents, or business processes."""
    response = httpx.get(
        "http://localhost:8000/api/search",
        params={"q": query, "limit": 3},
    )
    results = response.json()
    return "\n".join(r["content"] for r in results)

@tool
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    """Create a ticket. Use this when the user asks to report an issue, file a task,
    or submit a request. priority can be low, medium, high, or urgent."""
    response = httpx.post(
        "http://localhost:8000/api/tickets",
        json={"title": title, "description": description, "priority": priority},
    )
    ticket = response.json()
    return f"Created ticket #{ticket['id']}: {title}"

@tool
def get_current_time() -> str:
    """Return the current date and time. Use this when the user asks what time it is today."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

> 💡 **Security note:** an Agent can call any tool you give it. In production, validate tool inputs, restrict permissions, and log every sensitive action. Do not hand raw SQL execution or unrestricted shell access to an Agent.

### 6.5 Practical Example: A Multi-Tool Assistant

Let’s build a small assistant with calculation, time lookup, and text utilities:

```python
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek

@tool
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression such as '2 + 3 * 4' or '2 ** 10'."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def get_current_time() -> str:
    """Return the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def string_length(text: str) -> int:
    """Count the number of characters in a string."""
    return len(text)

@tool
def text_to_uppercase(text: str) -> str:
    """Convert English text to uppercase."""
    return text.upper()

tools = [calculator, get_current_time, string_length, text_to_uppercase]
llm = ChatDeepSeek(model="deepseek-chat")

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""You are a multi-purpose AI assistant with these tools:
- calculator: math
- time lookup: get the current time
- string tools: count length and convert to uppercase

Choose tools only when they help answer the user's request.""",
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is 2 to the power of 20?"}]
})
print(result["messages"][-1].content)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What time is it now, and how long until 10 PM?"}]
})
print(result["messages"][-1].content)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Hello, introduce yourself"}]
})
print(result["messages"][-1].content)
```

### 6.6 Middleware: Control the Agent Loop

LangChain v1.0 also introduced a middleware system, which lets you intercept important moments in the Agent loop. One of the most useful patterns is **Human in the Loop (HITL)**: pause before a sensitive action and wait for approval.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_deepseek import ChatDeepSeek

hitl = HumanInTheLoopMiddleware(
    interrupt_on={
        "create_ticket": True,
        "delete_database": {"allowed_decisions": ["approve", "reject"]},
    }
)

agent = create_agent(
    model=ChatDeepSeek(model="deepseek-chat"),
    tools=tools,
    middleware=[hitl],
    checkpointer=InMemorySaver(),
)
```

**How that middleware flow works:**

```text
user request -> agent decides to call create_ticket
             -> HumanInTheLoopMiddleware intercepts
             -> agent pauses and waits for a human decision
             -> human chooses approve / edit / reject
             -> agent continues or drops the tool call
```

> 💡 Middleware is not only for HITL. The same hook system can support summarization, context compression, PII masking, cost tracking, or custom policy checks.

**Article 6 recap:**

| Concept | One-line role |
| --- | --- |
| **Agent** | Lets the LLM decide which tools to use and in what order |
| **Tool** | A callable function exposed to the LLM, usually defined with `@tool` |
| **ReAct** | The think -> act -> observe loop behind many agent behaviors |
| **create_agent** | The unified v1.x agent constructor built on LangGraph |
| **Docstring** | The tool description that strongly shapes tool selection |
| **Middleware** | The v1.x interception layer for approvals, guards, and control |

</div>
