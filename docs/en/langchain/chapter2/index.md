---
title: "LangChain in Practice (II)"
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--modelio">
  <div class="langchain-hero__eyebrow">LangChain Deep Guide · Article 2</div>
  <div class="langchain-hero__headline">Model I/O / PromptTemplate / Structured Output</div>
  <p class="langchain-hero__subtitle">This article assembles LangChain's first core interface layer: model invocation, prompt templating, and structured output, all wired into a stable input-output contract.</p>
  <div class="langchain-hero__tags">
    <span>ChatModel</span>
    <span>PromptTemplate</span>
    <span>OutputParser</span>
    <span>Structured Output</span>
  </div>
</div>


<div class="langchain-series-heading">Series Navigation</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">Article 2 · Interface Layer</span>
    <span class="langchain-series-card__desc">Focus on Model I/O, PromptTemplate, OutputParser, and structured output so the input-output contract becomes stable first.</span>
    <span class="langchain-series-card__meta">ChatModel · PromptTemplate · Structured Output · You are here</span>
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
  <a class="langchain-series-card is-current" href="../chapter2/">
    <span class="langchain-series-card__kicker">Article 2 · Interface Layer</span>
    <span class="langchain-series-card__desc">Focus on Model I/O, PromptTemplate, OutputParser, and structured output so the input-output contract becomes stable first.</span>
    <span class="langchain-series-card__meta">ChatModel · PromptTemplate · Structured Output · You are here</span>
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

> This article moves into LangChain's interface layer and focuses on Model I/O, PromptTemplate, and structured output so the contracts around input, prompting, and output become stable first.

---

## 2. Model I/O: A Standardized Interface for Interacting with LLMs

Model I/O is the most fundamental module in LangChain. It answers two practical questions: how do you talk to an LLM, and how do you make it answer in the format you want? Its three core components are **ChatModel** (model invocation) → **PromptTemplate** (input construction) → **OutputParser** (output parsing).

### 2.1 ChatModel: A Unified Model Invocation Interface

LangChain uses `ChatModel` to smooth out the API differences between LLM providers. Whether you use DeepSeek, OpenAI, or Claude, the code structure stays the same:

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage

# Create a model instance
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,  # creativity: 0 = deterministic, 1 = more random
    max_tokens=1000,  # maximum output token count
)

# Approach 1: pass a plain string directly
response = llm.invoke("How many basic data types does Python have?")
print(response.content)

# Approach 2: pass a list of Messages for finer role control
messages = [
    SystemMessage(content="You are an experienced Python teacher. Keep the answer concise."),
    HumanMessage(content="Explain what a list comprehension is."),
]
response = llm.invoke(messages)
print(response.content)
```

**The three Message roles are:**

| Role | Class | Purpose |
| ---- | ---- | ---- |
| **System** | `SystemMessage` | Defines the AI's identity and behavioral rules |
| **Human** | `HumanMessage` | The user's input |
| **AI** | `AIMessage` | The AI's previous reply, used in multi-turn dialogue |

**Switching models only requires changing one line:**

```python
# Approach A: use each provider's own class
from langchain_deepseek import ChatDeepSeek
llm = ChatDeepSeek(model="deepseek-chat")  # DeepSeek

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")  # OpenAI

from langchain_anthropic import ChatAnthropic  # pip install langchain-anthropic
llm = ChatAnthropic(model="claude-sonnet-4-20250514")  # Claude

# Approach B: init_chat_model (new in v1.0, recommended)
from langchain.chat_models import init_chat_model

# One function, switch providers via the "provider:model" format
llm = init_chat_model("deepseek:deepseek-chat")
llm = init_chat_model("openai:gpt-4o")
llm = init_chat_model("anthropic:claude-sonnet-4-20250514")
```

> 💡 **The new `init_chat_model` introduced in v1.0** is a more elegant choice: you do not need to remember every provider-specific class. Use one function and switch by `"provider:model"`. It is especially suitable when end users can choose the model, because your config only needs to store one string.

> 💡 `invoke()` is the synchronous call. LangChain also provides `ainvoke()` (async), `stream()` (streaming output, token by token), and `batch()` (batched calls).

### 2.2 PromptTemplate: Stop Hand-Building Strings

Manually concatenating prompt strings is error-prone and hard to reuse. `PromptTemplate` lets you build prompts the way you would write an f-string template:

```python
from langchain_core.prompts import ChatPromptTemplate

# Define the template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role} who explains technical concepts in plain language."),
    ("human", "Explain what {concept} is and include a {language} code example."),
])

# Fill in the variables
messages = prompt.invoke({
    "role": "Python teacher",
    "concept": "decorator",
    "language": "Python",
})

print(messages)
# [SystemMessage(content='You are a Python teacher who explains technical concepts in plain language.'),
#  HumanMessage(content='Explain what a decorator is and include a Python code example.')]

# Send directly to the model
response = llm.invoke(messages)
print(response.content)
```

**PromptTemplate supports several construction styles:**

```python
# Style 1: from_messages (most common, precise role control)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are {role}"),
    ("human", "{question}"),
])

# Style 2: from_template (simple scenario, only one human message)
from langchain_core.prompts import PromptTemplate
prompt = PromptTemplate.from_template("Translate the following content into {language}:\n\n{text}")

# Style 3: with a chat-history placeholder (used in Chapter 4: Memory)
from langchain_core.prompts import MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),  # insert prior messages dynamically
    ("human", "{question}"),
])
```

> 💡 **The value of PromptTemplate is not just readability**. It turns prompts into reusable, testable, versionable code components. A carefully tuned prompt can be saved as a template and shared across a team.

### 2.3 OutputParser: Make the LLM Return Structured Data

LLMs return free-form text by default. But in real applications, you often need structured data such as JSON, lists, or Pydantic objects. `OutputParser` is responsible for **parsing LLM text into the format you actually want to consume**.

```python
# The simplest parser: extract plain text directly
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
# Convert an AIMessage object -> a plain string
text = parser.invoke(response)  # "Python has 6 basic data types..."
```

```python
# JSON parser: make the LLM return JSON
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a data analysis assistant. Return the result in JSON format."),
    ("human", "Analyze the basic information of this city: {city}\n\n{format_instructions}"),
])

# The parser generates formatting instructions automatically
prompt_with_instructions = prompt.partial(
    format_instructions=parser.get_format_instructions()
)

chain = prompt_with_instructions | llm | parser

result = chain.invoke({"city": "Hangzhou"})
print(result)
# {'name': 'Hangzhou', 'province': 'Zhejiang', 'population': 'about 12.37 million', 'famous_for': 'West Lake'}
print(type(result))  # <class 'dict'>
```

```python
# Pydantic parser: type-safe structured output
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class CityInfo(BaseModel):
    """City information"""

    name: str = Field(description="City name")
    province: str = Field(description="Province")
    population: str = Field(description="Population")
    highlights: list[str] = Field(description="3 to 5 highlights of the city")

parser = PydanticOutputParser(pydantic_object=CityInfo)

# parser.get_format_instructions() automatically generates a detailed format spec
chain = prompt_with_instructions | llm | parser

result = chain.invoke({"city": "Chengdu"})
print(result.name)        # Chengdu
print(result.highlights)  # ['Giant Panda Breeding Base', 'Kuanzhai Alley', 'hotpot culture', ...]
print(type(result))       # <class 'CityInfo'>
```

```python
# with_structured_output: model-native structured output (new in v1.0, highly recommended)
# This is the cleanest v1.0-era approach: let the model return a Pydantic object directly,
# without manually stitching format instructions or using a separate parser.

from pydantic import BaseModel, Field

class CityInfo(BaseModel):
    """City information"""

    name: str = Field(description="City name")
    province: str = Field(description="Province")
    population: str = Field(description="Population")
    highlights: list[str] = Field(description="3 to 5 highlights of the city")

# One line binds the model to return CityInfo
structured_llm = llm.with_structured_output(CityInfo)

result = structured_llm.invoke("Introduce the city of Chengdu.")
print(result.name)        # Chengdu
print(result.highlights)  # ['Giant Panda Breeding Base', 'Kuanzhai Alley', 'hotpot culture', ...]
print(type(result))       # <class 'CityInfo'>
```

> 💡 **How to choose among the four structured-output options in v1.x:**
>
> - Plain text: `StrOutputParser`
> - Need a dict: `JsonOutputParser`
> - Need type safety in the classic way: `PydanticOutputParser`
> - **Best choice for production: `model.with_structured_output(Schema)`** — the cleanest code, the lowest latency, and the highest reliability

### 2.4 Practical Example: Build an Intelligent Translator

Now combine ChatModel + PromptTemplate + `with_structured_output` to build a translator with **automatic language detection, translation, and confidence scoring**:

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# Step 1: define the output schema
class TranslationResult(BaseModel):
    source_language: str = Field(description="Source language")
    target_language: str = Field(description="Target language")
    translation: str = Field(description="Translation result")
    confidence: float = Field(description="Translation confidence, 0-1")
    alternatives: list[str] = Field(description="Up to two alternative translations")

# Step 2: build the prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional translator. Automatically detect the source language and translate it into {target_lang}.
If the source text is already in the target language, translate it into English instead."""),
    ("human", "{text}"),
])

# Step 3: assemble the chain with with_structured_output (recommended in v1.0)
llm = ChatDeepSeek(model="deepseek-chat")
structured_llm = llm.with_structured_output(TranslationResult)

translate_chain = prompt | structured_llm

# Step 4: use it
result = translate_chain.invoke({
    "target_lang": "Chinese",
    "text": "The quick brown fox jumps over the lazy dog",
})

print(f"Source language: {result.source_language}")
print(f"Translation: {result.translation}")
print(f"Confidence: {result.confidence}")
print(f"Alternatives: {result.alternatives}")
```

**This example shows the complete cooperation of the three core Model I/O components:**

```text
PromptTemplate          ChatModel            OutputParser
  (build input)    →      (call model)   →     (parse output)

{text, target_lang}  →  DeepSeek API   →  TranslationResult
                                           .translation
                                           .confidence
                                           .alternatives
```

**Chapter 2 key review:**

| Component | One-sentence explanation |
| ---- | ---- |
| **ChatModel** | A unified interface for model invocation, with one-line model switching |
| **init_chat_model** | The unified initialization interface added in v1.0, one function for all providers |
| **PromptTemplate** | A reusable prompt template with variable injection |
| **OutputParser** | Parses LLM text output into structured data such as dicts or Pydantic objects |
| **with_structured_output** | The recommended v1.0 structured-output approach: model-native, concise, and reliable |
| **Pipeline composition** | `prompt | llm | parser` → one complete processing chain |

---

## Summary

This article clarifies the most basic and most frequently used layer in LangChain:

1. **ChatModel** unifies how different model providers are called, so the same code can switch across DeepSeek, OpenAI, and Claude.
2. **PromptTemplate** upgrades prompts from fragile hand-built strings into reusable, maintainable, and testable template components.
3. **OutputParser / with_structured_output** turns free-form model responses into structured results that programs can directly consume.
4. Once these pieces are composed with a pattern like `prompt | llm | parser`, LangChain's standardized interaction layer is in place.

If Article 1 answered **why LangChain is needed**, then this article answers **what the first core interface layer looks like when you actually start writing LangChain code**.

</div>
