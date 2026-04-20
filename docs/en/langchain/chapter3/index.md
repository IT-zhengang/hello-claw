---
title: "LangChain in Practice (III)"
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--chain">
  <div class="langchain-hero__eyebrow">LangChain Deep Guide · Article 3</div>
  <div class="langchain-hero__headline">Chain / LCEL / RunnableParallel / Streaming</div>
  <p class="langchain-hero__subtitle">This is where LangChain moves beyond a single Runnable pipeline and into real workflow orchestration: composable chains, parallel branches, and streaming-first execution.</p>
  <div class="langchain-hero__tags">
    <span>LCEL</span>
    <span>RunnableParallel</span>
    <span>Streaming</span>
    <span>Workflow Orchestration</span>
  </div>
</div>


<div class="langchain-series-heading">Series Navigation</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">Article 3 · Orchestration Layer</span>
    <span class="langchain-series-card__desc">Move from interfaces into orchestration and see how Chain, LCEL, parallel branches, and streaming workflows fit together.</span>
    <span class="langchain-series-card__meta">Chain · LCEL · RunnableParallel · Streaming · You are here</span>
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
  <a class="langchain-series-card is-current" href="../chapter3/">
    <span class="langchain-series-card__kicker">Article 3 · Orchestration Layer</span>
    <span class="langchain-series-card__desc">Move from interfaces into orchestration and see how Chain, LCEL, parallel branches, and streaming workflows fit together.</span>
    <span class="langchain-series-card__meta">Chain · LCEL · RunnableParallel · Streaming · You are here</span>
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

> This article moves into LangChain's orchestration layer and focuses on Chain, LCEL, `RunnableParallel`, and streaming workflows so you can see how multi-step LLM flows are composed and executed.

---

## 3. Chain: Orchestrating LLM Workflows with Composable Pipelines

The `prompt | llm | parser` pattern from the previous article is already a Chain. This chapter goes deeper into LangChain's orchestration core — **LCEL (LangChain Expression Language)** — and shows how to compose more complex multi-step workflows in a clean, idiomatic way.

### 3.1 Getting Started with LCEL (LangChain Expression Language)

LCEL is LangChain's core orchestration style. It began in v0.2 and continues through v1.x. The central idea is extremely simple: **every component implements the `Runnable` interface, and you connect them with `|`.**

```ini
# The core idea of LCEL:
# Any object that implements the Runnable interface can be connected with |

chain = component_a | component_b | component_c

# Equivalent to:
# result = component_c.invoke(component_b.invoke(component_a.invoke(input)))
# But LCEL is more concise and automatically supports: streaming, async, batch, and parallel execution
```

**The Runnable interface provides these methods:**

| Method | What it does | Typical scenario |
| --- | --- | --- |
| invoke(input) | Synchronous call that returns the full result | Most common |
| ainvoke(input) | Asynchronous call | Async frameworks such as FastAPI |
| stream(input) | Streaming output, token by token | Chat UIs |
| batch([input1, input2]) | Batch invocation | Batch jobs |

### 3.2 The `|` Pipe Operator: Compose Components Like Building Blocks

The `|` operator wires multiple components into a pipeline: the output of one stage becomes the input of the next stage automatically.

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatDeepSeek(model="deepseek-chat")

# Chain 1: generate code
code_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Python expert. Return code only, without explanation."),
    ("human", "Write a function for {task}."),
])

code_chain = code_prompt | llm | StrOutputParser()

# Chain 2: explain the code
explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a programming teacher. Explain the following code line by line in Chinese."),
    ("human", "{code}"),
])

explain_chain = explain_prompt | llm | StrOutputParser()

# Compose the two chains: generate code -> explain code
from langchain_core.runnables import RunnablePassthrough

full_chain = (
    code_chain                                      # Step 1: generate code
    | (lambda code: {"code": code})               # Wrap the string into a dict
    | explain_chain                                 # Step 2: explain code
)

result = full_chain.invoke({"task": "quicksort"})
print(result)
# A line-by-line explanation of a Python implementation of quicksort...
```

**Use `RunnableLambda` instead of a bare lambda when possible:**

```python
from langchain_core.runnables import RunnableLambda

# A custom intermediate transformation step
def format_as_input(code_text: str) -> dict:
    """Convert the plain-text output of the previous step into the dict format required by the next step."""
    return {"code": code_text}

full_chain = code_chain | RunnableLambda(format_as_input) | explain_chain
```

### 3.3 RunnableParallel: Run Multiple Chains in Parallel

Sometimes you need to **run several tasks at the same time** and merge the results afterward. That is exactly what `RunnableParallel` is for.

```python
from langchain_core.runnables import RunnableParallel

# Define three parallel chains
summary_chain = (
    ChatPromptTemplate.from_template("Summarize the following text in one sentence: {text}")
    | llm | StrOutputParser()
)

keywords_chain = (
    ChatPromptTemplate.from_template("Extract 5 keywords separated by commas: {text}")
    | llm | StrOutputParser()
)

sentiment_chain = (
    ChatPromptTemplate.from_template("Analyze the sentiment of this text (positive / negative / neutral): {text}")
    | llm | StrOutputParser()
)

# Execute them in parallel with RunnableParallel
analysis_chain = RunnableParallel(
    summary=summary_chain,
    keywords=keywords_chain,
    sentiment=sentiment_chain,
)

result = analysis_chain.invoke({
    "text": "LangChain is a powerful framework for building LLM applications, but the learning curve can be steep."
})

print(result)
# {
#   'summary': 'LangChain is a powerful but demanding framework for LLM applications.',
#   'keywords': 'LangChain, LLM, framework, learning curve, application development',
#   'sentiment': 'neutral (it highlights both strengths and weaknesses)'
# }
```

```text
How RunnableParallel works:

                    ┌─ summary_chain ──→ summary
input ──→ copy 3x ──┼─ keywords_chain ──→ keywords  ──→ merge into one dict
                    └─ sentiment_chain ─→ sentiment
```

> 💡 Parallel does **not** automatically mean multithreading. In synchronous mode, `RunnableParallel` often still behaves like sequential invocation around I/O waits. In asynchronous mode with `ainvoke()`, the requests become truly concurrent. For production systems, async is usually the better default.

### 3.4 Streaming Output: Let the Result Appear Token by Token

How does the familiar “typewriter effect” in ChatGPT-style interfaces work? Use the `stream()` method.

```python
chain = (
    ChatPromptTemplate.from_template("Write a five-character quatrain about {topic}")
    | llm
    | StrOutputParser()
)

# Stream the output
for chunk in chain.stream({"topic": "autumn"}):
    print(chunk, end="", flush=True)
# Autumn wind sweeps falling leaves,
# Cold dew dyes the hills red,
# ...
```

**Use streaming in FastAPI like this:**

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/chat")
async def chat(question: str):
    chain = prompt | llm | StrOutputParser()

    async def generate():
        async for chunk in chain.astream({"question": question}):
            yield chunk  # Send one token at a time to the frontend

    return StreamingResponse(generate(), media_type="text/plain")
```

> 💡 The difference is fundamental: `invoke()` waits until all tokens are generated before returning, while `stream()` / `astream()` return data as it is produced. One of LCEL's biggest advantages is that **a chain assembled with `|` automatically becomes stream-capable** — you do not need to re-implement the pipeline for streaming.

### 3.5 Practical Example: A Multi-Step Content Generation Pipeline

Let’s build a “technical blog generator”: input a topic → generate an outline and key points in parallel → write the full article from the merged result.

```python
from langchain_core.runnables import RunnableParallel

# Step 1: generate an outline + key points in parallel
outline_chain = (
    ChatPromptTemplate.from_template(
        "Create a technical blog outline for the topic '{topic}' with 3 to 5 section titles."
    )
    | llm | StrOutputParser()
)

points_chain = (
    ChatPromptTemplate.from_template(
        "List the 5 most important technical points about '{topic}' as a concise bullet list."
    )
    | llm | StrOutputParser()
)

parallel_step = RunnableParallel(outline=outline_chain, key_points=points_chain)

# Step 2: write the full article based on outline + key points
write_chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a technical blogger. Write a complete article based on the provided outline and key points."),
        ("human", "Outline:\n{outline}\n\nKey points:\n{key_points}\n\nWrite the full article."),
    ])
    | llm | StrOutputParser()
)

# Compose the full pipeline
blog_pipeline = parallel_step | write_chain

# Usage
article = blog_pipeline.invoke({"topic": "Introduction to asynchronous programming in Python"})
print(article)
```

**Pipeline execution flow:**

```text
                    ┌─ outline_chain ──→ outline ─┐
{"topic": "..."} ──→                               ├──→ write_chain ──→ full article
                    └─ points_chain ──→ key_points ┘
```

**Chapter 3 recap:**

| Concept | One-line explanation |
| --- | --- |
| LCEL | LangChain's orchestration language; all components are connected via `\|` |
| Runnable | A unified interface supporting `invoke`, `stream`, `batch`, and `ainvoke` |
| RunnableParallel | Runs multiple chains in parallel and merges the result into a dict |
| RunnableLambda | Wraps a normal function so it can participate in a Runnable pipeline |
| stream() | Streaming output for the “typewriter effect” |

</div>
