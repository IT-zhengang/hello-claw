---
title: LangChain 实战教程（二）
---

<div class="langchain-page">

<div class="langchain-hero langchain-hero--modelio">
  <div class="langchain-hero__eyebrow">LangChain 深度技术指南 · 第二篇</div>
  <div class="langchain-hero__headline">Model I/O / PromptTemplate / Structured Output</div>
  <p class="langchain-hero__subtitle">从模型调用、提示词模板到结构化输出，把 LangChain 最基础也最常用的接口层串起来，建立稳定的输入输出规范。</p>
  <div class="langchain-hero__tags">
    <span>ChatModel</span>
    <span>PromptTemplate</span>
    <span>OutputParser</span>
    <span>Structured Output</span>
  </div>
</div>


<div class="langchain-series-heading">系列导航</div>

<details class="langchain-series-disclosure">
  <summary class="langchain-series-disclosure__summary">
    <span class="langchain-series-card langchain-series-card--summary is-current">
    <span class="langchain-series-card__kicker">第二篇 · 接口层</span>
    <span class="langchain-series-card__desc">聚焦 Model I/O、PromptTemplate、OutputParser 与结构化输出，先把输入输出接口层打稳。</span>
    <span class="langchain-series-card__meta">ChatModel · PromptTemplate · Structured Output · 当前阅读</span>
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
  <a class="langchain-series-card is-current" href="../chapter2/">
    <span class="langchain-series-card__kicker">第二篇 · 接口层</span>
    <span class="langchain-series-card__desc">聚焦 Model I/O、PromptTemplate、OutputParser 与结构化输出，先把输入输出接口层打稳。</span>
    <span class="langchain-series-card__meta">ChatModel · PromptTemplate · Structured Output · 当前阅读</span>
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

> 这一篇进入 LangChain 的接口层，围绕 Model I/O、PromptTemplate 与结构化输出，先把输入、提示词与结果格式的约定打稳。

---

## 2. Model I/O：与大模型交互的标准化接口

Model I/O 是 LangChain 最基础的模块——它解决的是“怎么和大模型说话、怎么让大模型按你想要的格式回答”。三个核心组件：**ChatModel**（调用模型）→ **PromptTemplate**（构造输入）→ **OutputParser**（解析输出）。

### 2.1 ChatModel：统一的模型调用接口

LangChain 用 `ChatModel` 把所有大模型的 API 差异抹平了。无论你用 DeepSeek、OpenAI 还是 Claude，代码结构完全一样：

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage

# ── 创建模型实例 ──
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,  # 创造性：0=确定性，1=更随机
    max_tokens=1000,  # 最大输出 token 数
)

# ── 方式 1：直接传字符串（最简单） ──
response = llm.invoke("Python 有几种基本数据类型？")
print(response.content)

# ── 方式 2：传 Message 列表（更精确地控制角色） ──
messages = [
    SystemMessage(content="你是一个资深 Python 教师，回答要简洁。"),
    HumanMessage(content="解释什么是列表推导式"),
]
response = llm.invoke(messages)
print(response.content)
```

**Message 的三种角色：**

| 角色 | 类 | 作用 |
| ---- | ---- | ---- |
| **System** | `SystemMessage` | 设定 AI 的身份和行为规范 |
| **Human** | `HumanMessage` | 用户的输入 |
| **AI** | `AIMessage` | AI 之前的回复（用于多轮对话） |

**切换模型只需改一行：**

```python
# ── 方式 A：每个提供商用各自的类 ──
from langchain_deepseek import ChatDeepSeek
llm = ChatDeepSeek(model="deepseek-chat")  # DeepSeek

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")  # OpenAI

from langchain_anthropic import ChatAnthropic  # pip install langchain-anthropic
llm = ChatAnthropic(model="claude-sonnet-4-20250514")  # Claude

# ── 方式 B：init_chat_model（v1.0 新增，推荐） ──
from langchain.chat_models import init_chat_model

# 同一个函数，用 "provider:model" 格式切换提供商
llm = init_chat_model("deepseek:deepseek-chat")
llm = init_chat_model("openai:gpt-4o")
llm = init_chat_model("anthropic:claude-sonnet-4-20250514")
```

> 💡 **v1.0 新增的 `init_chat_model`** 是更优雅的选择：不需要记住每个提供商的类名，统一用一个函数，通过 `"provider:model"` 格式切换。特别适合“用户可选模型”的场景——配置文件里存一个字符串就行。

> 💡 `invoke()` 是同步调用。LangChain 还提供了 `ainvoke()`（异步）、`stream()`（流式输出，一个 token 一个 token 返回）、`batch()`（批量调用）。

### 2.2 PromptTemplate：告别手拼字符串

手动拼接 prompt 字符串很容易出错，也不利于复用。`PromptTemplate` 让你像写 f-string 模板一样构造 prompt：

```python
from langchain_core.prompts import ChatPromptTemplate

# ── 定义模板 ──
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，擅长用通俗易懂的方式解释技术概念。"),
    ("human", "请解释什么是{concept}，给一个{language}的代码示例。"),
])

# ── 填充变量 ──
messages = prompt.invoke({
    "role": "Python 教师",
    "concept": "装饰器",
    "language": "Python",
})

print(messages)
# [SystemMessage(content='你是一个 Python 教师，擅长用通俗易懂的方式解释技术概念。'),
#  HumanMessage(content='请解释什么是装饰器，给一个 Python 的代码示例。')]

# ── 直接送给模型 ──
response = llm.invoke(messages)
print(response.content)
```

**PromptTemplate 支持多种构造方式：**

```python
# 方式 1：from_messages（最常用，精确控制每条消息的角色）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{role}"),
    ("human", "{question}"),
])

# 方式 2：from_template（简单场景，只有一条 human 消息）
from langchain_core.prompts import PromptTemplate
prompt = PromptTemplate.from_template("请把以下内容翻译成{language}：\n\n{text}")

# 方式 3：包含聊天历史占位符（第 4 章 Memory 会用到）
from langchain_core.prompts import MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手。"),
    MessagesPlaceholder(variable_name="chat_history"),  # 动态插入历史消息
    ("human", "{question}"),
])
```

> 💡 **PromptTemplate 的价值不只是“好看”**——它让 prompt 变成了可复用、可测试、可版本管理的代码组件。你可以把一套精心调试好的 prompt 保存为模板，团队共享。

### 2.3 OutputParser：让 LLM 返回结构化数据

LLM 默认返回自由文本。但在实际应用中，你通常需要结构化数据（JSON、列表、Pydantic 对象）。`OutputParser` 负责把 LLM 的文本输出**解析成你想要的格式**。

```python
# ── 最简单的 Parser：直接提取文本 ──
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
# 把 AIMessage 对象 → 纯字符串
text = parser.invoke(response)  # "Python 有 6 种基本数据类型..."
```

```python
# ── JSON Parser：让 LLM 返回 JSON ──
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数据分析助手。请以 JSON 格式返回结果。"),
    ("human", "分析这个城市的基本信息：{city}\n\n{format_instructions}"),
])

# parser 自动生成格式说明，教 LLM 怎么输出 JSON
prompt_with_instructions = prompt.partial(
    format_instructions=parser.get_format_instructions()
)

chain = prompt_with_instructions | llm | parser

result = chain.invoke({"city": "杭州"})
print(result)
# {'name': '杭州', 'province': '浙江', 'population': '约1237万', 'famous_for': '西湖'}
print(type(result))  # <class 'dict'>  ← 已经是 Python 字典了！
```

```python
# ── Pydantic Parser：类型安全的结构化输出 ──
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class CityInfo(BaseModel):
    """城市信息"""

    name: str = Field(description="城市名称")
    province: str = Field(description="所属省份")
    population: str = Field(description="人口数量")
    highlights: list[str] = Field(description="城市亮点，3-5 个")

parser = PydanticOutputParser(pydantic_object=CityInfo)

# parser.get_format_instructions() 会自动生成详细的格式说明
# 告诉 LLM 需要返回什么字段、什么类型
chain = prompt_with_instructions | llm | parser

result = chain.invoke({"city": "成都"})
print(result.name)        # 成都
print(result.highlights)  # ['大熊猫繁育基地', '宽窄巷子', '火锅文化', ...]
print(type(result))       # <class 'CityInfo'>  ← Pydantic 对象，有类型校验！
```

```python
# ── with_structured_output：模型原生结构化输出（v1.0 新增，强烈推荐） ──
# 这是 v1.0 引入的最优雅方式：直接让模型返回 Pydantic 对象，
# 不需要手动拼 format_instructions，不需要单独的 Parser！

from pydantic import BaseModel, Field

class CityInfo(BaseModel):
    """城市信息"""

    name: str = Field(description="城市名称")
    province: str = Field(description="所属省份")
    population: str = Field(description="人口数量")
    highlights: list[str] = Field(description="城市亮点，3-5 个")

# 一行代码：把模型“绑定”为返回 CityInfo 的版本
structured_llm = llm.with_structured_output(CityInfo)

result = structured_llm.invoke("介绍一下成都这个城市")
print(result.name)        # 成都
print(result.highlights)  # ['大熊猫繁育基地', '宽窄巷子', '火锅文化', ...]
print(type(result))       # <class 'CityInfo'>  ← 直接拿到 Pydantic 对象！
```

> 💡 **四种结构化输出方式的选择（v1.x）：**
>
> - 纯文本：`StrOutputParser`
> - 需要字典：`JsonOutputParser`
> - 需要类型安全（经典方式）：`PydanticOutputParser`
> - **生产环境首选：`model.with_structured_output(Schema)`**——代码最简洁、延迟最低、可靠性最高

### 2.4 实战：构建一个智能翻译器

现在把 ChatModel + PromptTemplate + `with_structured_output` 组合起来，做一个有**语言自动检测 + 翻译 + 置信度评分**的翻译器：

```python
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

# ── Step 1：定义输出结构 ──
class TranslationResult(BaseModel):
    source_language: str = Field(description="原文语言")
    target_language: str = Field(description="目标语言")
    translation: str = Field(description="翻译结果")
    confidence: float = Field(description="翻译置信度，0-1")
    alternatives: list[str] = Field(description="其他可能的翻译，最多 2 个")

# ── Step 2：构建 Prompt ──
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业翻译。请自动检测原文语言，翻译成{target_lang}。
如果原文已经是目标语言，请翻译成英文。"""),
    ("human", "{text}"),
])

# ── Step 3：用 with_structured_output 组装成链（v1.0 推荐方式） ──
llm = ChatDeepSeek(model="deepseek-chat")
structured_llm = llm.with_structured_output(TranslationResult)

translate_chain = prompt | structured_llm

# ── Step 4：使用 ──
result = translate_chain.invoke({
    "target_lang": "中文",
    "text": "The quick brown fox jumps over the lazy dog",
})

print(f"原文语言: {result.source_language}")      # 英文
print(f"翻译结果: {result.translation}")          # 敏捷的棕色狐狸跳过了那只懒狗
print(f"置信度: {result.confidence}")            # 0.95
print(f"其他翻译: {result.alternatives}")        # ['快速的棕色狐狸...', ...]
```

**这个例子展示了 Model I/O 三大组件的完美配合：**

```text
PromptTemplate          ChatModel            OutputParser
  (构造输入)       →      (调用模型)       →      (解析输出)

{text, target_lang}  →  DeepSeek API   →  TranslationResult
                                           .translation
                                           .confidence
                                           .alternatives
```

**第 2 章核心知识回顾：**

| 组件 | 一句话解释 |
| ---- | ---- |
| **ChatModel** | 统一的模型调用接口，一行代码切换模型 |
| **init_chat_model** | v1.0 新增的统一初始化接口，一个函数搞定所有提供商 |
| **PromptTemplate** | 可复用的 prompt 模板，支持变量注入 |
| **OutputParser** | 把 LLM 文本输出解析为结构化数据（dict / Pydantic） |
| **with_structured_output** | v1.0 推荐的结构化输出，模型原生支持，最简洁可靠 |
| **管道组合** | `prompt | llm | parser` → 一条完整的处理链 |

---

## 总结

这一篇把 LangChain 最基础、也是最常用的一层能力拆清楚了：

1. **ChatModel** 负责把不同模型提供商的调用方式统一起来，让你能用同一套代码切换 DeepSeek、OpenAI、Claude。
2. **PromptTemplate** 负责把 prompt 从“手拼字符串”升级成可复用、可维护、可测试的模板组件。
3. **OutputParser / with_structured_output** 负责把模型的自由文本回答收敛成程序真正可消费的结构化结果。
4. 当这三者用 `prompt | llm | parser` 这样的方式组合起来时，LangChain 的“标准化接口层”就建立起来了。

如果说第一篇解决的是“为什么需要 LangChain”，那么这一篇解决的就是：**真正开始写 LangChain 时，最先上手、最先串起来的核心接口是什么。**

</div>
