---
title: "LangChain in Practice (I)"
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--overview">
  <div class="langchain-hero__eyebrow">LangChain Deep Guide · Article 1</div>
  <div class="langchain-hero__headline">Framework Positioning / Module Map / Learning Path</div>
  <p class="langchain-hero__subtitle">Start with the entry question: why does LangChain exist, and how does it organize memory, retrieval, tools, and orchestration into a real LLM application framework?</p>
  <div class="langchain-hero__tags">
    <span>Framework Overview</span>
    <span>Module Map</span>
    <span>RAG</span>
    <span>Agent</span>
  </div>
</div>


<div class="langchain-series-heading">Series Navigation</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">Article 1 · Overview</span>
    <span class="langchain-series-card__desc">Start with why LangChain matters, then build the module map, version context, and overall learning path.</span>
    <span class="langchain-series-card__meta">Framework Positioning · Module Map · You are here</span>
    </span>
    <span class="langchain-series-disclosure__toggle">
      <span class="langchain-series-disclosure__toggle-closed">Expand full series</span>
      <span class="langchain-series-disclosure__toggle-opened">Collapse series</span>
    </span>
  </summary>

  <div class="langchain-series-grid langchain-series-grid--compact">
  <a class="langchain-series-card is-current" href="../chapter1/">
    <span class="langchain-series-card__kicker">Article 1 · Overview</span>
    <span class="langchain-series-card__desc">Start with why LangChain matters, then build the module map, version context, and overall learning path.</span>
    <span class="langchain-series-card__meta">Framework Positioning · Module Map · You are here</span>
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
  <a class="langchain-series-card" href="../chapter6/">
    <span class="langchain-series-card__kicker">Article 6 · Autonomy Layer</span>
    <span class="langchain-series-card__desc">Move from fixed pipelines to goal-driven execution with tools, ReAct loops, tool calling, and `create_agent`.</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent</span>
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

> This article starts with framework positioning and the module map, answering why LangChain matters before building the shared mental model for RAG, Agents, and Memory.

---

## 1. What Is LangChain, and Why Do You Need It?

You may already know how to use `requests` or `httpx` to call an LLM API: send in a prompt, get back an answer. But when you want to build a **real AI application** — one with conversational memory, question answering over private documents, or an Agent that can use tools on its own — direct API calls are no longer enough. LangChain exists to solve exactly that problem.

### 1.1 What Is Wrong with Calling the API Directly?

Let’s start with the simplest possible model call:

```python
import httpx
import os

API_KEY = os.getenv("DEEPSEEK_API_KEY")

response = httpx.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Explain what LangChain is in one sentence"}],
    },
)
print(response.json()["choices"][0]["message"]["content"])
```

This code runs, but once requirements become more complex, you run into **four core pain points**:

| Pain point | Scenario | Cost of raw API calls |
| ---- | ---- | ---- |
| **No memory** | Multi-turn dialogue, and the LLM does not remember the previous turn | You must manually maintain the `messages` list, and it keeps growing |
| **No knowledge** | Asking about your own private documents, which the LLM knows nothing about | You must implement the full RAG pipeline yourself: load -> split -> embed -> retrieve -> assemble |
| **No tools** | Asking the LLM to query a database, search the web, or use a calculator | You must build JSON parsing, tool dispatch, and error handling yourself |
| **Hard to compose** | Multi-step workflows such as summarize -> translate -> format | You manually chain multiple API calls, and the code turns into spaghetti |

```text
Raw API calls fit: simple one-question/one-answer scenarios
LangChain fits: applications that need memory / knowledge bases / tools / multi-step orchestration
```

> 💡 **Analogy**: raw API calls are like operating a database by hand — `cursor.execute("SELECT ...")`. LangChain is more like an ORM (Django Model / SQLAlchemy): it abstracts away repetitive low-level details so you can focus on business logic.

### 1.2 LangChain’s Core Positioning: an LLM Application Framework

LangChain is not a model, and it is not an API service. It is a **framework that connects large models with the outside world**.

```text
LangChain in one sentence:

“Using standardized components, it turns an LLM from a ‘chat interface’
into a complete application that can remember, retrieve, use tools,
and orchestrate complex flows.”
```

**The core idea behind LangChain is “modular + composable”**:

```text
┌──────────────────────────────────────────────────┐
│                Your AI Application               │
├──────────────────────────────────────────────────┤
│  Model I/O  │  Chain  │  Memory  │   Agent      │
│  (model I/O)│ (orchestration) │ (memory) │ (autonomy) │
├──────────────────────────────────────────────────┤
│  Document Loaders  │  Embeddings  │  Vector      │
│  (document loading)│  (embeddings) │  Stores     │
├──────────────────────────────────────────────────┤
│  Middleware        │  LangGraph (Agent runtime) │
├──────────────────────────────────────────────────┤
│  LLMs (DeepSeek / OpenAI / Claude / local models)│
└──────────────────────────────────────────────────┘
```

**Several of LangChain’s design principles are worth remembering**:

| Principle | Meaning | Benefit |
| ---- | ---- | ---- |
| **Model-agnostic** | The same code can switch from DeepSeek -> OpenAI -> Claude with one line of configuration | You are not locked into a single vendor |
| **Composable components** | Each module is independent and can be assembled like Lego | Use only what you need |
| **LCEL pipelines** | Components are chained with the `|` operator, so the code reads like a sentence | Extremely readable |
| **Observable** | Built-in integration with LangSmith to trace the input and output of each step | Debugging is no longer blind |

> 💡 **LangChain officially released v1.0 in October 2025**, and by the time of the original article, the latest version was v1.2. LangChain v1.0 introduced major upgrades such as the new `create_agent` abstraction, middleware, `with_structured_output`, and an Agent runtime built on LangGraph. Older functionality was moved into the `langchain-classic` package. The tutorial is written against the latest v1.x architecture.

### 1.3 Architecture Overview: the Core Modules

This tutorial follows the sequence below to explain LangChain’s major modules one by one:

```text
Chapter 2            Chapter 3           Chapter 4        Chapter 5        Chapter 6
Model I/O     ->     Chain (LCEL)  ->    Memory    ->     RAG      ->      Agent
model I/O            orchestration        dialogue memory retrieval         autonomy
prompt -> LLM        A | B | C            remember context doc-based QA     use tools

                         ↓ combined together ↓

                   Chapter 7: integrated practical project
                FastAPI + LangChain knowledge-base assistant
```

**What problem does each module solve?**

| Module | One-line description | What pain point it solves |
| ---- | ---- | ---- |
| **Model I/O** | Unified model invocation + prompt templates + output parsing | Different models expose different API formats |
| **Chain (LCEL)** | Use `|` to turn multiple steps into a pipeline | Multi-step orchestration becomes messy |
| **Memory** | Automatically manage dialogue history | LLMs do not have memory |
| **RAG** | Document loading -> embedding -> retrieval -> answer | LLMs do not know your private data |
| **Agent** | Let the LLM decide which tools to use and how | Needed when the LLM must perform real actions |

### 1.4 Installation and Environment Setup

**Environment requirements:**

- **Python >= 3.9** (Python 3.8 is no longer supported from v1.0 onward)
- **Pydantic v2** (Pydantic v1 is no longer supported from v1.0 onward)

**Install the core packages:**

```bash
# Core framework (required, includes langchain-core automatically)
pip install langchain

# Model providers (choose one as needed)
pip install langchain-deepseek       # DeepSeek (official integration, recommended)
pip install langchain-openai         # OpenAI (also works for OpenAI-compatible services)
# pip install langchain-anthropic    # Claude
# pip install langchain-google-genai # Gemini

# Agent runtime (used in Chapter 6; LangChain v1.0 Agents are built on LangGraph)
pip install langgraph

# RAG-related packages (used in Chapter 5)
pip install langchain-chroma         # Chroma vector database
pip install langchain-community      # Community integrations (document loaders, etc.)
```

**Configure your API key (preferably via a `.env` file):**

```ini
# .env file
DEEPSEEK_API_KEY=sk-your-api-key-here
# or
OPENAI_API_KEY=sk-your-api-key-here
```

```python
# Load it in code
from dotenv import load_dotenv
load_dotenv()  # automatically reads environment variables from .env

# ── Approach 1: use the official provider package (recommended) ──
from langchain_deepseek import ChatDeepSeek

# DeepSeek has its own dedicated langchain-deepseek package, so base_url does not need manual setup
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    # api_key is automatically read from the DEEPSEEK_API_KEY environment variable
)

response = llm.invoke("Hello, LangChain!")
print(response.content)
# Hello! I am an AI assistant, and I am glad to talk with you through LangChain!

# ── Approach 2: the unified init_chat_model interface (new in v1.0, recommended) ──
from langchain.chat_models import init_chat_model

# Use the unified "provider:model" format so one function works for all providers
llm = init_chat_model("deepseek:deepseek-chat")  # DeepSeek
# Switch to OpenAI: init_chat_model("openai:gpt-4o")
# Switch to Claude: init_chat_model("anthropic:claude-sonnet-4-20250514")

# You can also specify the provider separately
# llm = init_chat_model("deepseek-chat", model_provider="deepseek")
```

> 💡 **This tutorial uses DeepSeek as its main model** because it is cost-effective, strong in Chinese, and compatible with the OpenAI-style interface. But all examples can be switched to OpenAI / Claude / Gemini by changing only one line of configuration.

---

## Summary

The main value of this article is that it makes the entry questions for the LangChain learning path clear from the beginning:

1. **Why you would need LangChain**: once an application starts needing memory, a knowledge base, tool calls, and multi-step orchestration, raw API calls quickly become unmanageable.
2. **What LangChain actually is**: it is not the model itself, but the framework layer that organizes models, retrieval, tools, and workflows into a complete application.
3. **How to continue learning**: you can go deeper step by step along `Model I/O -> Chain (LCEL) -> Memory -> RAG -> Agent`.

If the original article were compressed into one sentence, it would be this: **LangChain does not exist to replace the model — it exists to help a model grow into an application that is deployable, extensible, and maintainable.**

</div>
