---
title: "LangChain in Practice (VII)"
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--project">
  <div class="langchain-hero__eyebrow">LangChain Deep Guide · Article 7</div>
  <div class="langchain-hero__headline">FastAPI / RAG Assistant / Streaming / Session Memory</div>
  <p class="langchain-hero__subtitle">This article combines the earlier layers into one end-to-end project: a knowledge-base assistant that supports uploads, retrieval, multi-turn chat, and streaming responses.</p>
  <div class="langchain-hero__tags">
    <span>FastAPI</span>
    <span>Chroma</span>
    <span>Streaming</span>
    <span>End-to-End Project</span>
  </div>
</div>

<div class="langchain-series-heading">Series Navigation</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">Article 7 · Project Layer</span>
    <span class="langchain-series-card__desc">Combine Model I/O, Memory, and RAG into a document-upload, retrieval-enabled knowledge assistant with streaming responses.</span>
    <span class="langchain-series-card__meta">FastAPI · Chroma · Streaming · Integrated Project · You are here</span>
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
  <a class="langchain-series-card" href="../chapter6/">
    <span class="langchain-series-card__kicker">Article 6 · Autonomy Layer</span>
    <span class="langchain-series-card__desc">Move from fixed pipelines to goal-driven execution with tools, ReAct loops, tool calling, and `create_agent`.</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent</span>
  </a>
  <a class="langchain-series-card is-current" href="../chapter7/">
    <span class="langchain-series-card__kicker">Article 7 · Project Layer</span>
    <span class="langchain-series-card__desc">Combine Model I/O, Memory, and RAG into a document-upload, retrieval-enabled knowledge assistant with streaming responses.</span>
    <span class="langchain-series-card__meta">FastAPI · Chroma · Streaming · Integrated Project · You are here</span>
  </a>
  <a class="langchain-series-card" href="../chapter8/">
    <span class="langchain-series-card__kicker">Article 8 · Ecosystem Layer</span>
    <span class="langchain-series-card__desc">Finish with LangSmith, LangGraph, and a comparison of major frameworks so the ecosystem picture becomes clear.</span>
    <span class="langchain-series-card__meta">LangSmith · LangGraph · Ecosystem · Comparison</span>
  </a>
  </div>
</details>

> This article moves into the implementation layer and combines Model I/O, Memory, and RAG into a complete AI knowledge-base assistant.

---

## 7. Practical Project: Build a Complete AI Knowledge-Base Assistant

The first six articles covered the key LangChain modules one by one. This article puts them together into a full project: a FastAPI backend that supports document upload, semantic retrieval, multi-turn chat, and streaming responses.

### 7.1 Project Architecture

```text
knowledge-assistant/
├── main.py              # FastAPI entrypoint
├── chains.py            # LangChain chain definitions
├── knowledge_base.py    # loading, splitting, and vector storage
├── memory_store.py      # conversation memory management
├── config.py            # API keys and runtime settings
├── requirements.txt     # dependencies
└── docs/                # uploaded documents
```

**High-level system diagram:**

```text
User (frontend / curl / Postman)
        |
        v
+-----------------------------------------------+
|                 FastAPI backend               |
|-----------------------------------------------|
| POST /upload -> knowledge_base.py             |
|   upload file -> split -> embed -> Chroma     |
|                                               |
| POST /chat -> chains.py                       |
|   question -> retrieve docs -> build prompt   |
|   <-> memory_store.py (multi-turn memory)     |
|   <-> streaming SSE/plain-text response       |
|-----------------------------------------------|
| Chroma vector DB        | In-memory history   |
+-----------------------------------------------+
```

### 7.2 Backend Integration: FastAPI + LangChain

**`config.py` - central configuration:**

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# LLM settings
LLM_MODEL = "deepseek-chat"
LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Embedding settings
EMBEDDING_MODEL = "text-embedding-3-small"

# Knowledge-base settings
CHROMA_DB_DIR = "./chroma_db"
DOCS_DIR = "./docs"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
```

**`main.py` - FastAPI entrypoint:**

```python
# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from knowledge_base import KnowledgeBase
from chains import create_rag_chain
from memory_store import MemoryStore

app = FastAPI(title="AI Knowledge Base Assistant")

kb = KnowledgeBase()
memory = MemoryStore()

class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document into the knowledge base."""
    content = await file.read()
    file_path = f"./docs/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(content)

    num_chunks = kb.add_document(file_path)
    return {"message": f"Added {file.filename}; generated {num_chunks} vector chunks"}

@app.post("/chat")
async def chat(req: ChatRequest):
    """Streaming chat endpoint."""
    chain = create_rag_chain(kb.vectorstore, memory.get_history(req.session_id))

    async def generate():
        full_response = ""
        async for chunk in chain.astream({"input": req.question}):
            full_response += chunk
            yield chunk
        memory.save_message(req.session_id, req.question, full_response)

    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/health")
async def health():
    return {"status": "ok", "documents": kb.doc_count}
```

### 7.3 Knowledge-Base Management: Upload, Split, Embed

**`knowledge_base.py` - document ingestion + vectorization:**

```python
# knowledge_base.py
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import config

class KnowledgeBase:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
        )

        self.vectorstore = Chroma(
            persist_directory=config.CHROMA_DB_DIR,
            embedding_function=self.embeddings,
        )

    def add_document(self, file_path: str) -> int:
        """Add a file into the knowledge base."""
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding="utf-8")

        docs = loader.load()
        chunks = self.splitter.split_documents(docs)

        self.vectorstore.add_documents(chunks)
        return len(chunks)

    @property
    def doc_count(self) -> int:
        return self.vectorstore._collection.count()
```

### 7.4 Chat Endpoint: Streaming + Multi-Turn Memory

**`memory_store.py` - session history management:**

```python
# memory_store.py
from langchain_core.messages import HumanMessage, AIMessage

class MemoryStore:
    """A simple in-memory session store."""

    def __init__(self, max_history=10):
        self.store = {}
        self.max_history = max_history

    def get_history(self, session_id: str) -> list:
        return self.store.get(session_id, [])

    def save_message(self, session_id: str, human_msg: str, ai_msg: str):
        if session_id not in self.store:
            self.store[session_id] = []

        self.store[session_id].extend([
            HumanMessage(content=human_msg),
            AIMessage(content=ai_msg),
        ])

        if len(self.store[session_id]) > self.max_history * 2:
            self.store[session_id] = self.store[session_id][-self.max_history * 2:]
```

**`chains.py` - RAG + memory chain:**

```python
# chains.py
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import config

def create_rag_chain(vectorstore, chat_history: list):
    """Create a RAG chain with conversation history."""
    llm = ChatDeepSeek(
        model=config.LLM_MODEL,
        streaming=True,
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def format_docs(docs):
        return "\n\n---\n\n".join(
            f"[{doc.metadata.get('source', '?')}]\n{doc.page_content}"
            for doc in docs
        )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an intelligent knowledge-base assistant. Answer based on the reference documents.
If the answer is not in the documents, say so honestly. Cite the source in your answer.

Reference documents:
{context}"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ])

    chain = (
        {
            "context": (lambda x: x["input"]) | retriever | format_docs,
            "chat_history": lambda x: chat_history,
            "input": lambda x: x["input"],
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
```

**API test examples:**

```bash
# Start the service
uvicorn main:app --reload

# Upload a document
curl -X POST http://localhost:8000/upload \
  -F "file=@./my_notes/python_guide.md"
# {"message": "Added python_guide.md; generated 42 vector chunks"}

# Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is a decorator?", "session_id": "user_001"}'
# Based on the document, a decorator is ...
```

### 7.5 Deployment and Optimization: Production Checklist

```text
Production checklist

Basics
  - manage API keys through environment variables
  - add CORS middleware for browser clients
  - add API authentication (Bearer token or API key)

Performance
  - persist the vector database; do not rebuild it on every restart
  - cache embeddings so the same text is not embedded repeatedly
  - use async patterns such as ainvoke / astream for concurrency
  - move large uploads to background tasks when needed

Reliability
  - add retries and timeouts around LLM calls
  - write structured logs for each request / response pair
  - integrate LangSmith for tracing and debugging

Cost control
  - monitor token usage
  - apply user-level or daily quotas
  - switch long conversations to summary memory instead of full buffer memory
```

```python
from langchain_deepseek import ChatDeepSeek

llm = ChatDeepSeek(
    model="deepseek-chat",
    request_timeout=30,
    max_retries=3,
)
```

**Article 7 recap:**

| Module | Technique | Connected article |
| --- | --- | --- |
| Document upload + vectorization | `DocumentLoader` + Chroma | Article 5: RAG |
| RAG answer chain | Retriever + Prompt + LLM | Article 5: RAG |
| Multi-turn memory | Message history | Article 4: Memory |
| Streaming responses | `astream` + `StreamingResponse` | Article 3: Chain |
| API service | FastAPI | This article |

</div>
