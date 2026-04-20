---
title: "LangChain in Practice (V)"
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--rag">
  <div class="langchain-hero__eyebrow">LangChain Deep Guide · Article 5</div>
  <div class="langchain-hero__headline">RAG / Document Loaders / Embeddings / Retriever</div>
  <p class="langchain-hero__subtitle">This article moves into LangChain's knowledge layer and shows how external documents are loaded, split, embedded, indexed, and retrieved to power grounded answers.</p>
  <div class="langchain-hero__tags">
    <span>RAG</span>
    <span>Text Splitter</span>
    <span>Embeddings</span>
    <span>Vector Store</span>
  </div>
</div>

<div class="langchain-series-heading">Series Navigation</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">Article 5 · Knowledge Layer</span>
    <span class="langchain-series-card__desc">Build the full RAG path around Document Loaders, Text Splitter, Embeddings, VectorStore, and Retriever.</span>
    <span class="langchain-series-card__meta">RAG · Embeddings · Vector Store · Retriever · You are here</span>
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
  <a class="langchain-series-card is-current" href="../chapter5/">
    <span class="langchain-series-card__kicker">Article 5 · Knowledge Layer</span>
    <span class="langchain-series-card__desc">Build the full RAG path around Document Loaders, Text Splitter, Embeddings, VectorStore, and Retriever.</span>
    <span class="langchain-series-card__meta">RAG · Embeddings · Vector Store · Retriever · You are here</span>
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

> This article moves into LangChain's knowledge layer and focuses on Document Loaders, Text Splitter, Embeddings, VectorStore, and Retriever so you can see how RAG connects external knowledge to an LLM application.

---

## 5. RAG: Let an LLM Answer from Your Data

RAG is one of the most practical LLM application patterns today. Imagine your company has hundreds of internal documents and you want an AI assistant to answer based on those documents, but you do not want the cost and maintenance burden of fine-tuning. **RAG is the answer**: retrieve relevant document chunks first, then pass them into the prompt so the model answers from evidence instead of pure recall.

### 5.1 What Is RAG, and Why Is It More Practical than Fine-Tuning?

```text
RAG (Retrieval-Augmented Generation) = retrieval + generation

Traditional path:
  user asks -> LLM answers from its own prior knowledge -> may hallucinate

RAG path:
  user asks -> system retrieves relevant documents ->
  documents + question go into the prompt -> answer is grounded in facts
```

**RAG vs. fine-tuning vs. long context:**

| Approach | Cost | Freshness | Best fit |
| --- | --- | --- | --- |
| **RAG** | Low (mainly embeddings + indexing) | High (document updates can take effect immediately) | Knowledge-base Q&A, document assistants |
| **Fine-tuning** | High (GPU training and iteration cost) | Low (you retrain when data changes) | Style control, domain-specific model behavior |
| **Long context only** | Medium to high (token cost grows fast) | High | Small document sets used occasionally |

**The full RAG lifecycle:**

```text
Offline stage (usually done once per corpus):
  documents -> split into chunks -> embed chunks -> store in a vector database

Online stage (for every question):
  user question -> embed question -> search similar chunks in vector database ->
  combine retrieved chunks + question into a prompt -> LLM answers
```

### 5.2 Document Loading: PDF, Markdown, and Web Pages

LangChain ships with many document loaders, covering most common source types:

```python
# Load a Markdown or text file
from langchain_community.document_loaders import TextLoader

loader = TextLoader("./docs/guide.md", encoding="utf-8")
docs = loader.load()
print(f"Loaded {len(docs)} document(s)")
print(docs[0].page_content[:200])
print(docs[0].metadata)  # {'source': './docs/guide.md'}

# Load a PDF
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./docs/report.pdf")
docs = loader.load()  # one Document per page
print(f"Total pages: {len(docs)}")

# Load a web page
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://docs.python.org/3/tutorial/index.html")
docs = loader.load()

# Load many files from a directory
from langchain_community.document_loaders import DirectoryLoader

loader = DirectoryLoader("./docs/", glob="**/*.md", show_progress=True)
docs = loader.load()
print(f"Loaded {len(docs)} document(s)")
```

> 💡 Every `Document` object has two key fields: `page_content` for the text itself and `metadata` for source details such as file path, page number, or URL. That metadata becomes useful when you want to show citations in the final answer.

### 5.3 Text Splitting: `RecursiveCharacterTextSplitter`

A single document may be thousands of words long, while an LLM has a finite context window and generally performs better when evidence is chunked cleanly. That is why we split documents into smaller semantic pieces:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
)

chunks = splitter.split_documents(docs)
print(f"Original documents: {len(docs)} -> chunks: {len(chunks)}")
print(f"Approximate chunk length: {len(chunks[0].page_content)} characters")
```

**Why overlap matters:**

```text
chunk_size=500, chunk_overlap=50

Original text: [████████████████████████████████████████████]
Chunk 1:       [██████████████]
Chunk 2:              [██████████████]
Chunk 3:                      [██████████████]
```

| Parameter | Typical range | Why it matters |
| --- | --- | --- |
| `chunk_size` | 300-1000 | Too small loses context; too large hurts retrieval precision |
| `chunk_overlap` | 50-100 | Preserves continuity across boundaries |
| `separators` | semantic first | Prefer paragraphs, then sentences, then characters |

> 💡 Split quality directly affects RAG quality. Code docs often benefit from smaller chunks, while narrative content can use larger chunks.

### 5.4 Vector Storage: Embeddings + Chroma / FAISS

After splitting, each chunk must be converted into a vector so the system can do semantic search. That embedding process maps text into a high-dimensional numeric space.

```python
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Step 1: create the embedding model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)

# Step 2: store chunks in a vector database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)
print(f"Stored vectors: {vectorstore._collection.count()}")

# Step 3: semantic search
results = vectorstore.similarity_search("How do Python decorators work?", k=3)
for doc in results:
    print(f"Source: {doc.metadata.get('source', 'unknown')}")
    print(f"Snippet: {doc.page_content[:100]}...")
    print()
```

**What embeddings are doing conceptually:**

```text
"Python decorator"    -> [0.12, -0.34, 0.56, ..., 0.78]
"Python decorators"   -> [0.11, -0.33, 0.55, ..., 0.77]  # semantically close
"The weather is nice" -> [0.89,  0.23, -0.67, ..., 0.01] # semantically different

At query time, the user question is embedded too, and the system finds nearby vectors.
```

**Chroma vs. FAISS:**

| Feature | Chroma | FAISS |
| --- | --- | --- |
| Install | `pip install langchain-chroma` | `pip install faiss-cpu` |
| Persistence | Built in | Manual save / load |
| Metadata filtering | Supported | Not built in |
| Typical fit | Small to medium corpora | Large-scale similarity search |

> 💡 For small projects, Chroma is an excellent default. At larger production scale, teams often move toward FAISS, Milvus, or another dedicated vector database.

### 5.5 Retrieval Chain: From “Found” to “Answered”

Once the vector store exists, you can build a complete RAG chain: **retrieve first, answer second**.

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatDeepSeek(model="deepseek-chat")

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a knowledge-base assistant. Answer the user's question based on the reference documents below.
If the answer is not present in the documents, explicitly say "I could not find relevant information" and do not invent facts.

Reference documents:
{context}"""),
    ("human", "{question}"),
])

def format_docs(docs):
    return "\n\n---\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in docs
    )

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("How does the @ syntax for Python decorators work?")
print(answer)
```

**The data flow looks like this:**

```text
"How do decorators work?"
       |
       +--> retriever.invoke()
       |      -> semantic search
       |      -> top 3 relevant chunks
       |      -> format_docs()
       |      -> {"context": "document text ..."}
       |
       +--> RunnablePassthrough()
       |      -> {"question": "How do decorators work?"}
       |
       v
combined into {"context": "...", "question": "..."}
       |
       v
rag_prompt -> LLM -> StrOutputParser -> final grounded answer
```

### 5.6 Practical Example: A Local-Document Q&A System

Let’s combine the full workflow into a simple local knowledge-base assistant:

```python
from langchain_deepseek import ChatDeepSeek
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ============================================
# Offline stage: documents -> vector database
# ============================================

def build_knowledge_base(docs_dir: str, db_dir: str = "./chroma_db"):
    """Build the local knowledge base."""
    loader = DirectoryLoader(docs_dir, glob="**/*.md")
    docs = loader.load()
    print(f"Loaded {len(docs)} document(s)")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunk(s)")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=db_dir)
    print(f"Persisted vector store to: {db_dir}")
    return vectorstore

# ============================================
# Online stage: question answering
# ============================================

def create_qa_chain(vectorstore):
    """Create a retrieval-based QA chain."""
    llm = ChatDeepSeek(model="deepseek-chat")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Answer the question using the reference documents below.
When citing evidence, include the source filename.
If the answer is not in the documents, respond with "I could not find relevant information." 

Reference documents:
{context}"""),
        ("human", "{question}"),
    ])

    def format_docs(docs):
        return "\n\n---\n\n".join(
            f"[{doc.metadata.get('source', '?')}]\n{doc.page_content}"
            for doc in docs
        )

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

# First run: build the knowledge base
# vectorstore = build_knowledge_base("./my_docs/")

# Later runs: reopen the existing store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

qa = create_qa_chain(vectorstore)
print(qa.invoke("What is a Python decorator?"))
```

**Article 5 recap:**

| Step | Component | One-line role |
| --- | --- | --- |
| Load | `DocumentLoader` | Turn files or pages into `Document` objects |
| Split | `TextSplitter` | Break long content into retrieval-friendly chunks |
| Embed | `Embeddings` | Convert text into semantic vectors |
| Store | `VectorStore` | Persist vectors and support similarity search |
| Retrieve | `Retriever` | Fetch the most relevant chunks for a question |
| Answer | `LLM + Prompt` | Combine question + evidence into a grounded response |

</div>
