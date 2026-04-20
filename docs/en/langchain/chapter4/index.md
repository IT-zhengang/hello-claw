---
title: "LangChain in Practice (IV)"
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--memory">
  <div class="langchain-hero__eyebrow">LangChain Deep Guide · Article 4</div>
  <div class="langchain-hero__headline">Memory / Conversation History / Summary Memory</div>
  <p class="langchain-hero__subtitle">LLM memory is not magic inside the model. It is an application-layer strategy for carrying forward conversation state. This article explains how that works in LangChain.</p>
  <div class="langchain-hero__tags">
    <span>ChatMessageHistory</span>
    <span>RunnableWithMessageHistory</span>
    <span>Summary Memory</span>
    <span>Session State</span>
  </div>
</div>


<div class="langchain-series-heading">Series Navigation</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">Article 4 · State Layer</span>
    <span class="langchain-series-card__desc">Focus on Memory, session-scoped history, and summary-based memory to complete the story of multi-turn state handling.</span>
    <span class="langchain-series-card__meta">Memory · Session History · Summary Memory · You are here</span>
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
  <a class="langchain-series-card is-current" href="../chapter4/">
    <span class="langchain-series-card__kicker">Article 4 · State Layer</span>
    <span class="langchain-series-card__desc">Focus on Memory, session-scoped history, and summary-based memory to complete the story of multi-turn state handling.</span>
    <span class="langchain-series-card__meta">Memory · Session History · Summary Memory · You are here</span>
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

> This article moves into LangChain's state layer and focuses on Memory, session history, and summary-based memory so you can see how multi-turn context is stored, compressed, and reused.

---

## 4. Memory: Giving an LLM Memory

Have you noticed that every LLM call feels like “meeting for the first time”? The model does not remember what you said in the previous turn. This chapter addresses that problem by giving your AI application **multi-turn conversational memory**.

### 4.1 Why Do LLMs “Have No Memory”?

An LLM is **stateless** by nature. Every invocation is independent — the model does not automatically store the previous conversation.

```python
llm = ChatDeepSeek(model="deepseek-chat")

# Turn 1
response1 = llm.invoke("My name is Xiaoming")
print(response1.content)  # Hello Xiaoming! Nice to meet you!

# Turn 2
response2 = llm.invoke("What is my name?")
print(response2.content)  # Sorry, I do not know your name. ← It forgot completely!
```

**Why?** Because on the second call, the API only receives the message `"What is my name?"`. The first-turn conversation was never sent again.

**The essence of “memory” is simply this: append prior dialogue to the next request.**

```python
from langchain_core.messages import HumanMessage, AIMessage

# Manually append history -> now the LLM can "remember"
messages = [
    HumanMessage(content="My name is Xiaoming"),
    AIMessage(content="Hello Xiaoming! Nice to meet you!"),  # Previous reply
    HumanMessage(content="What is my name?"),                # New question
]

response = llm.invoke(messages)
print(response.content)  # Your name is Xiaoming! ← It remembers now.
```

> 💡 The key idea is this: LLM “memory” is not a built-in internal feature of the model. It is an application-level concern. You must send previous dialogue history along with each new request. LangChain's memory abstractions exist to automate that process.

### 4.2 ConversationBufferMemory: Full Dialogue History

In LangChain's current LCEL-oriented architecture, the recommended way to manage memory is `ChatMessageHistory` + `RunnableWithMessageHistory`:

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatDeepSeek(model="deepseek-chat")

# Step 1: define a prompt with a history placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),  # history goes here
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# Step 2: create session storage (isolated by session_id)
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Step 3: wrap the chain with message-history support
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Usage: the same session_id shares the same memory
config = {"configurable": {"session_id": "user_001"}}

print(chain_with_memory.invoke({"input": "My name is Xiaoming, and I am a Python developer."}, config=config))
# Hello Xiaoming! Great to meet you. Python is a wonderful language!

print(chain_with_memory.invoke({"input": "What is my name? What is my job?"}, config=config))
# Your name is Xiaoming, and you are a Python developer! ← Perfect recall.

# A different session_id means a different memory state
config2 = {"configurable": {"session_id": "user_002"}}
print(chain_with_memory.invoke({"input": "What is my name?"}, config=config2))
# Sorry, you have not told me your name yet. ← New session, no memory.
```

**How the memory flow works:**

```text
User sends: "What is my name?"
       │
       ▼
RunnableWithMessageHistory:
  1. Load the prior history using session_id
  2. Combine history + new message into a full messages list
  3. Send the result to the LLM
  4. Save the new question-answer pair back into history
       │
       ▼
What the LLM actually receives:
  [system] You are a helpful assistant.
  [human]  My name is Xiaoming, and I am a Python developer.   ← history
  [ai]     Hello Xiaoming!...                                  ← history
  [human]  What is my name?                                    ← new message
```

> 💡 The problem with buffer memory is obvious: as the conversation grows, the history grows too, and eventually the model's context window will overflow. That is where summary memory comes in.

### 4.3 ConversationSummaryMemory: Summary-Based Memory

When a conversation becomes long — dozens or even hundreds of turns — sending the entire history in every prompt will **blow up the context window**. Summary memory solves that by **compressing older dialogue into a short summary** instead of keeping everything verbatim.

```python
from langchain_core.messages import HumanMessage, AIMessage

def summarize_history(llm, messages, max_messages=6):
    """
    When the history exceeds max_messages,
    summarize the older turns with the LLM.
    """
    if len(messages) <= max_messages:
        return messages  # still within the limit

    # Split old messages from recent messages
    old_messages = messages[:-max_messages]
    recent_messages = messages[-max_messages:]

    # Generate a summary of the older turns
    old_text = "\n".join(
        f"{'User' if isinstance(m, HumanMessage) else 'AI'}: {m.content}"
        for m in old_messages
    )

    summary = llm.invoke(
        f"Summarize the key information in the following dialogue in 2 to 3 sentences:\n\n{old_text}"
    ).content

    # Return: summary + recent messages
    from langchain_core.messages import SystemMessage
    return [SystemMessage(content=f"Summary of the earlier conversation: {summary}")] + recent_messages
```

**Comparing the three memory strategies:**

| Strategy | Principle | Strength | Weakness |
| --- | --- | --- | --- |
| Buffer | Keep the full history | No information loss | Long conversations exceed token limits |
| Summary | Compress old messages into a summary | Works for very long conversations | The summary may lose details |
| Window | Keep only the most recent N turns | Simple and efficient | Early information is dropped entirely |

> 💡 A common production choice is a hybrid strategy: keep the latest 5 to 10 turns in full buffer form for detail, and compress older turns into a summary so important context survives without exploding token usage.

### 4.4 Practical Example: Build a Context-Aware Multi-Turn Chatbot

Now let’s combine these ideas into a complete chatbot that supports **role definition, memory management, and streaming output**:

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Configuration
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    streaming=True,  # enable streaming
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an AI coding assistant named Xiaozhi.
Your characteristics:
- Strong at Python, JavaScript, and Rust
- Concise answers with clear code examples
- Remembers what the user said earlier and actively connects the context"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# Memory management
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

# Interaction loop
def chat(session_id="default"):
    config = {"configurable": {"session_id": session_id}}
    print("🤖 Xiaozhi: Hi! I am Xiaozhi, your AI coding assistant. How can I help?")
    print("(Type 'quit' to exit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        print("🤖 Xiaozhi: ", end="")
        # Stream the reply
        for chunk in chatbot.stream({"input": user_input}, config=config):
            print(chunk, end="", flush=True)
        print("\n")

# chat()  # Uncomment to run
```

**Chapter 4 recap:**

| Concept | One-line explanation |
| --- | --- |
| LLMs are stateless | Each call is independent, so memory must be managed at the application layer |
| Buffer memory | Keeps the full history; simple but limited by token size |
| Summary memory | Compresses old dialogue into a summary for long conversations |
| RunnableWithMessageHistory | A straightforward way to add memory to a simple chain |
| LangGraph Checkpointer | The recommended state-persistence mechanism for Agent-style workflows in v1.0 |
| session_id | Isolates memory across different users or conversations |

> 💡 For v1.0-style memory management, a good rule of thumb is: use `RunnableWithMessageHistory` for simple chat chains because it stays light and direct; use `LangGraph + Checkpointer` (for example `MemorySaver` or `PostgresSaver`) for Agents and more complex workflows because it can persist the full graph state. Older interfaces such as `ConversationBufferMemory` are effectively legacy now and should not be the default choice for new projects.

</div>
