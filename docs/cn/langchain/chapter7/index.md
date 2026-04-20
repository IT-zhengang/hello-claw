---
title: LangChain 实战教程（七）
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--project">
  <div class="langchain-hero__eyebrow">LangChain 深度技术指南 · 第七篇</div>
  <div class="langchain-hero__headline">FastAPI / RAG Assistant / Streaming / Session Memory</div>
  <p class="langchain-hero__subtitle">把前面几层真正组合起来，完成一个可上传文档、支持检索、多轮会话与流式响应的知识库助手。</p>
  <div class="langchain-hero__tags">
    <span>FastAPI</span>
    <span>Chroma</span>
    <span>Streaming</span>
    <span>End-to-End Project</span>
  </div>
</div>

<div class="langchain-series-heading">系列导航</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">第七篇 · 项目层</span>
    <span class="langchain-series-card__desc">把 Model I/O、Memory 与 RAG 组合成一个可上传文档、支持检索和流式响应的知识库助手。</span>
    <span class="langchain-series-card__meta">FastAPI · Chroma · Streaming · Integrated Project · 当前阅读</span>
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
  <a class="langchain-series-card" href="../chapter6/">
    <span class="langchain-series-card__kicker">第六篇 · 自治层</span>
    <span class="langchain-series-card__desc">围绕 Tool、ReAct、Tool Calling 与 `create_agent`，进入目标驱动的工具调用与自主决策。</span>
    <span class="langchain-series-card__meta">Agent · Tool · ReAct · create_agent</span>
  </a>
  <a class="langchain-series-card is-current" href="../chapter7/">
    <span class="langchain-series-card__kicker">第七篇 · 项目层</span>
    <span class="langchain-series-card__desc">把 Model I/O、Memory 与 RAG 组合成一个可上传文档、支持检索和流式响应的知识库助手。</span>
    <span class="langchain-series-card__meta">FastAPI · Chroma · Streaming · Integrated Project · 当前阅读</span>
  </a>
  <a class="langchain-series-card" href="../chapter8/">
    <span class="langchain-series-card__kicker">第八篇 · 生态层</span>
    <span class="langchain-series-card__desc">介绍 LangSmith、LangGraph 与主流框架对比，建立 LangChain 后续工程深化与选型视角。</span>
    <span class="langchain-series-card__meta">LangSmith · LangGraph · Ecosystem · Comparison</span>
  </a>
  </div>
</details>

> 这一篇进入 LangChain 的工程落地层，把 Model I/O、Memory 与 RAG 组合进一个完整的 AI 知识库助手。

---

## 7. 实战项目：构建一个完整的 AI 知识库助手

前面 6 章学了 LangChain 的所有核心模块，这一章把它们**全部组合起来**，构建一个端到端的 AI 知识库助手——用 FastAPI 做后端，支持文档上传、语义检索、多轮对话、流式响应。

### 7.1 项目架构设计
```

    项目结构：

    knowledge-assistant/
    ├── main.py              # FastAPI 入口
    ├── chains.py            # LangChain 链定义
    ├── knowledge_base.py    # 知识库管理（加载、分割、向量化）
    ├── memory_store.py      # 对话记忆管理
    ├── config.py            # 配置（API Key、模型参数）
    ├── requirements.txt     # 依赖
    └── docs/                # 用户上传的文档目录

```

**系统架构图：**
```

    用户（前端/curl/Postman）
          │
          ▼
    ┌─────────────────────────────────────────────┐
    │              FastAPI 后端                     │
    ├─────────────────────────────────────────────┤
    │                                             │
    │  POST /upload    → knowledge_base.py        │
    │    上传文档 → 分割 → 向量化 → Chroma        │
    │                                             │
    │  POST /chat      → chains.py               │
    │    问题 → 检索文档 → 拼接prompt → LLM       │
    │    ↕ memory_store.py（多轮记忆）             │
    │    ↕ 流式SSE响应                             │
    │                                             │
    ├─────────────────────────────────────────────┤
    │  Chroma（向量数据库）  │  InMemory（记忆存储）│
    └─────────────────────────────────────────────┘

```

### 7.2 后端：FastAPI + LangChain 集成

**`config.py` — 配置管理：**
```

    # config.py
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # 模型配置
    LLM_MODEL = "deepseek-chat"
    LLM_API_KEY = os.getenv("DEEPSEEK_API_KEY")

    # Embedding 配置
    EMBEDDING_MODEL = "text-embedding-3-small"

    # 知识库配置
    CHROMA_DB_DIR = "./chroma_db"
    DOCS_DIR = "./docs"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

```

**`main.py` — FastAPI 入口：**
```

    # main.py
    from fastapi import FastAPI, UploadFile, File
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel

    from knowledge_base import KnowledgeBase
    from chains import create_rag_chain
    from memory_store import MemoryStore

    app = FastAPI(title="AI 知识库助手")

    # 初始化核心组件
    kb = KnowledgeBase()
    memory = MemoryStore()

    class ChatRequest(BaseModel):
        question: str
        session_id: str = "default"

    @app.post("/upload")
    async def upload_document(file: UploadFile = File(...)):
        """上传文档到知识库"""
        content = await file.read()
        file_path = f"./docs/{file.filename}"

        with open(file_path, "wb") as f:
            f.write(content)

        # 向量化并存入数据库
        num_chunks = kb.add_document(file_path)
        return {"message": f"✅ 已添加 {file.filename}，生成 {num_chunks} 个向量块"}

    @app.post("/chat")
    async def chat(req: ChatRequest):
        """对话接口（流式响应）"""
        chain = create_rag_chain(kb.vectorstore, memory.get_history(req.session_id))

        async def generate():
            full_response = ""
            async for chunk in chain.astream({"input": req.question}):
                full_response += chunk
                yield chunk
            # 对话结束后保存记忆
            memory.save_message(req.session_id, req.question, full_response)

        return StreamingResponse(generate(), media_type="text/plain")

    @app.get("/health")
    async def health():
        return {"status": "ok", "documents": kb.doc_count}

```

### 7.3 知识库管理：文档上传与向量化

**`knowledge_base.py` — 文档加载 + 分割 + 向量化：**
```

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

            # 加载已有的向量数据库（如果存在的话）
            self.vectorstore = Chroma(
                persist_directory=config.CHROMA_DB_DIR,
                embedding_function=self.embeddings,
            )

        def add_document(self, file_path: str) -> int:
            """添加文档到知识库"""
            # 根据文件类型选择加载器
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            else:
                loader = TextLoader(file_path, encoding="utf-8")

            docs = loader.load()
            chunks = self.splitter.split_documents(docs)

            # 添加到向量数据库
            self.vectorstore.add_documents(chunks)
            return len(chunks)

        @property
        def doc_count(self) -> int:
            return self.vectorstore._collection.count()

```

### 7.4 对话接口：流式响应 + 多轮记忆

**`memory_store.py` — 会话记忆管理：**
```

    # memory_store.py
    from langchain_core.messages import HumanMessage, AIMessage

    class MemoryStore:
        """简单的内存会话存储"""

        def __init__(self, max_history=10):
            self.store = {}           # session_id → messages list
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

            # 保留最近 N 轮（防止记忆过长）
            if len(self.store[session_id]) > self.max_history * 2:
                self.store[session_id] = self.store[session_id][-self.max_history * 2:]

```

**`chains.py` — RAG + 记忆链：**
```

    # chains.py
    from langchain_deepseek import ChatDeepSeek
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    import config

    def create_rag_chain(vectorstore, chat_history: list):
        """创建带记忆的 RAG 链"""
        llm = ChatDeepSeek(
            model=config.LLM_MODEL,
            streaming=True,
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        def format_docs(docs):
            return "\n\n---\n\n".join(
                f"【{doc.metadata.get('source', '?')}】\n{doc.page_content}"
                for doc in docs
            )

        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个智能知识库助手。请基于参考文档回答问题。
    如果文档中找不到答案，请坦诚告知。回答时引用文档来源。

    参考文档：
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

**测试 API：**
```

    # 启动服务
    uvicorn main:app --reload

    # 上传文档
    curl -X POST http://localhost:8000/upload \
      -F "file=@./my_notes/python_guide.md"
    # {"message": "✅ 已添加 python_guide.md，生成 42 个向量块"}

    # 对话（流式）
    curl -X POST http://localhost:8000/chat \
      -H "Content-Type: application/json" \
      -d '{"question": "什么是装饰器？", "session_id": "user_001"}'
    # 根据文档，装饰器是一种...（流式逐字返回）

```

### 7.5 部署与优化：生产环境注意事项
```

    生产环境 Checklist：

    ✅ 基础
      □ API Key 用环境变量管理，不硬编码
      □ 添加 CORS 中间件（前端跨域）
      □ 添加 API 认证（Bearer Token / API Key）

    ✅ 性能
      □ 向量数据库用持久化存储（不要每次重启都重建）
      □ Embedding 调用做缓存（同一文本不重复计算）
      □ 用异步（ainvoke/astream）处理并发请求
      □ 大文件上传用后台任务（BackgroundTask）

    ✅ 可靠性
      □ LLM 调用加 retry 和 timeout
      □ 添加结构化日志（记录每次问答的输入输出）
      □ 集成 LangSmith 做链路追踪（下一章介绍）

    ✅ 成本
      □ 监控 token 使用量
      □ 设置每用户/每日的调用限额
      □ 长对话用摘要记忆而非 Buffer 记忆

```
```

    # 示例：添加超时和重试
    from langchain_deepseek import ChatDeepSeek

    llm = ChatDeepSeek(
        model="deepseek-chat",
        request_timeout=30,       # 30 秒超时
        max_retries=3,            # 最多重试 3 次
    )

```

**第 7 章核心知识回顾：**

| 模块       | 技术                          | 对应章节         |
|----------|-----------------------------|--------------|
| 文档上传+向量化 | DocumentLoader + Chroma     | 第 5 章 RAG    |
| RAG 问答链  | Retriever + Prompt + LLM    | 第 5 章 RAG    |
| 多轮记忆     | MessageHistory              | 第 4 章 Memory |
| 流式响应     | astream + StreamingResponse | 第 3 章 Chain  |
| API 服务   | FastAPI                     | —            |

</div>
