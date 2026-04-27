---
title: AI 模型图解：从模型到 Agent、MCP 与 Memory
---

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

const previewImages = [
  { src: '../../../static/llm/visual-guide/images/01-ai-overview.png', title: '01 总览：AI 世界里到底有哪些层' },
  { src: '../../../static/llm/visual-guide/images/02-what-is-a-model.png', title: '02 什么叫模型：AI 的能力边界从哪里来' },
  { src: '../../../static/llm/visual-guide/images/03-what-is-an-agent.png', title: '03 什么是 Agent：从“会说”到“会做”' },
  { src: '../../../static/llm/visual-guide/images/04-what-is-mcp.png', title: '04 什么是 MCP：给工具接入装统一插头' },
  { src: '../../../static/llm/visual-guide/images/05-what-is-a-workflow.png', title: '05 什么是工作流：把能力变成稳定流程' },
  { src: '../../../static/llm/visual-guide/images/06-knowledge-base-and-memory.png', title: '06 什么是知识库 / Memory：让系统不再每次从零开始' },
  { src: '../../../static/llm/visual-guide/images/07-gpt-vs-claude-vs-gemini.png', title: '07 GPT、Claude、Gemini 有什么区别' }
]

const isPreviewOpen = ref(false)
const currentPreviewIndex = ref(0)
const currentPreview = computed(() => previewImages[currentPreviewIndex.value])
const previewCounterText = computed(() => `${currentPreviewIndex.value + 1} / ${previewImages.length}`)
const previewStageRef = ref(null)
const previewImageRatio = ref(1)
const isTallPreview = computed(() => previewImageRatio.value > 1.28)

const lockBody = () => {
  if (typeof document !== 'undefined') document.body.style.overflow = 'hidden'
}

const unlockBody = () => {
  if (typeof document !== 'undefined') document.body.style.overflow = ''
}

const resetPreviewScroll = () => {
  nextTick(() => {
    previewStageRef.value?.scrollTo({ top: 0, left: 0, behavior: 'auto' })
  })
}

const openPreview = (index) => {
  currentPreviewIndex.value = index
  previewImageRatio.value = 1
  isPreviewOpen.value = true
  lockBody()
  resetPreviewScroll()
}

const closePreview = () => {
  isPreviewOpen.value = false
  unlockBody()
}

const showPrev = () => {
  currentPreviewIndex.value = (currentPreviewIndex.value - 1 + previewImages.length) % previewImages.length
  previewImageRatio.value = 1
  resetPreviewScroll()
}

const showNext = () => {
  currentPreviewIndex.value = (currentPreviewIndex.value + 1) % previewImages.length
  previewImageRatio.value = 1
  resetPreviewScroll()
}

const onPreviewImageLoad = (event) => {
  const { naturalWidth, naturalHeight } = event.target
  if (!naturalWidth || !naturalHeight) return
  previewImageRatio.value = naturalHeight / naturalWidth
  resetPreviewScroll()
}

const onKeydown = (event) => {
  if (!isPreviewOpen.value) return
  if (event.key === 'Escape') closePreview()
  if (event.key === 'ArrowLeft') showPrev()
  if (event.key === 'ArrowRight') showNext()
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  unlockBody()
})
</script>

<div class="llm-visual-guide">

<div class="llm-visual-guide__hero">
  <div class="llm-visual-guide__eyebrow">AI 大模型架构解析 · 图解导读</div>
  <h1>一页串起模型、Agent、MCP、工作流与 Memory</h1>
  <p class="llm-visual-guide__subtitle">如果你总觉得模型、Agent、MCP、工作流、知识库这些词看起来都懂，但放在一起就容易混，这一页就是用来把它们重新排回同一张地图里的。</p>
  <div class="llm-visual-guide__tags">
    <span>AI Fundamentals</span>
    <span>Model vs Agent</span>
    <span>MCP</span>
    <span>Workflow</span>
    <span>Memory</span>
  </div>
</div>

<div class="llm-visual-guide__lead">
  <p><strong>先抓主线：</strong>模型负责理解与生成，Agent 负责围绕目标行动，MCP 负责连接工具，Workflow 负责把步骤沉淀成流程，Memory 负责把资料与经验留住。后面的 7 张图，就是沿着这条线一层层展开。</p>
</div>

<div class="llm-visual-guide__quick-grid">
  <div class="llm-visual-guide__quick-card">
    <span>模型</span>
    <strong>先回答：系统“会不会”</strong>
    <p>负责理解、推理、生成与结构化表达，是能力底座。</p>
  </div>
  <div class="llm-visual-guide__quick-card">
    <span>Agent</span>
    <strong>再回答：系统“会不会自己做”</strong>
    <p>让模型围绕目标持续行动，而不是只生成一段话。</p>
  </div>
  <div class="llm-visual-guide__quick-card">
    <span>MCP</span>
    <strong>再回答：工具“怎么规范接入”</strong>
    <p>统一发现、调用和约束工具，降低接入碎片化。</p>
  </div>
  <div class="llm-visual-guide__quick-card">
    <span>Workflow</span>
    <strong>再回答：流程“能不能稳定复用”</strong>
    <p>把高频任务从一次性成功，变成可复用、可审计的 SOP。</p>
  </div>
  <div class="llm-visual-guide__quick-card">
    <span>Memory</span>
    <strong>最后回答：系统“记不记得住”</strong>
    <p>延续知识、偏好、状态与经验，让协作具有连续性。</p>
  </div>
  <div class="llm-visual-guide__quick-card llm-visual-guide__quick-card--accent">
    <span>模型选型</span>
    <strong>别只问谁强，更要问谁匹配</strong>
    <p>成本、风格、上下文稳定性和生态集成，都会改变答案。</p>
  </div>
</div>


<div class="llm-visual-guide__toc">
  <a href="#overview">01 总览：AI 世界里到底有哪些层</a>
  <a href="#model">02 什么叫模型：AI 的能力边界从哪里来</a>
  <a href="#agent">03 什么是 Agent：从“会说”到“会做”</a>
  <a href="#mcp">04 什么是 MCP：给工具接入装统一插头</a>
  <a href="#workflow">05 什么是工作流：把能力变成稳定流程</a>
  <a href="#memory">06 什么是知识库 / Memory：让系统不再每次从零开始</a>
  <a href="#compare">07 GPT、Claude、Gemini 有什么区别</a>
</div>

## 适合谁从哪一节开始读

<div class="llm-visual-guide__path-grid">
  <a class="llm-visual-guide__path-card" href="#overview">
    <span class="llm-visual-guide__path-kicker">零基础读者</span>
    <strong>先从 01 总览 开始</strong>
    <p>先把“模型、Agent、MCP、工作流、Memory”放回同一张地图里，再往下看定义，不容易混层。</p>
  </a>
  <a class="llm-visual-guide__path-card" href="#model">
    <span class="llm-visual-guide__path-kicker">产品 / 运营</span>
    <strong>优先读 02 模型 + 05 工作流</strong>
    <p>先看模型边界，再看如何把能力沉淀成稳定流程，最适合做方案判断和需求拆解。</p>
  </a>
  <a class="llm-visual-guide__path-card" href="#agent">
    <span class="llm-visual-guide__path-kicker">开发者</span>
    <strong>优先读 03 Agent + 04 MCP</strong>
    <p>更快理解工具调用、执行循环、协议接入与系统分层，适合进入工程实现视角。</p>
  </a>
  <a class="llm-visual-guide__path-card" href="#memory">
    <span class="llm-visual-guide__path-kicker">做知识库 / 助手的人</span>
    <strong>优先读 06 Memory</strong>
    <p>先分清知识库与 Memory，再回头看 Workflow 和 Agent，能更快进入真实业务设计。</p>
  </a>
</div>

## 先把关系图装进脑子里

很多入门文章会把这些概念拆开讲，但真正让人建立理解的，往往不是一个个定义，而是它们之间的关系。你可以先把下面这张“文字版关系图”记住：

<div class="llm-visual-guide__relation-map">
  <div class="llm-visual-guide__relation-card">
    <strong>模型 Model</strong>
    <p>负责理解、推理、生成，是整个系统的认知引擎。</p>
  </div>
  <div class="llm-visual-guide__relation-arrow">-></div>
  <div class="llm-visual-guide__relation-card">
    <strong>Agent</strong>
    <p>围绕目标驱动模型做判断、调工具、读结果、继续执行。</p>
  </div>
  <div class="llm-visual-guide__relation-arrow">-></div>
  <div class="llm-visual-guide__relation-card">
    <strong>Workflow</strong>
    <p>把高频任务沉淀成稳定步骤，让执行更可控、更可复用。</p>
  </div>
  <div class="llm-visual-guide__relation-rail">
    <span>MCP / API / CLI 负责把 Agent 连接到外部工具世界</span>
  </div>
  <div class="llm-visual-guide__relation-card llm-visual-guide__relation-card--memory">
    <strong>Knowledge Base / Memory</strong>
    <p>给模型、Agent 和 Workflow 持续提供资料、上下文、偏好与经验沉淀。</p>
  </div>
</div>

这一层关系可以这样理解：

- **模型是能力起点**：没有模型，系统就没有语言理解、推理和生成能力
- **Agent 是行动组织层**：它让模型不只是回答问题，而是开始围绕目标执行任务
- **Workflow 是稳定交付层**：它把本来依赖临场发挥的能力，变成可重复的流程
- **Memory 是长期积累层**：它让系统记住上下文、资料与经验，而不是每次都重新来过
- **MCP / API / CLI 是连接通道**：它们不是目标本身，而是让系统能接上外部工具和真实世界

如果你先有了这张关系图，后面再看单个概念时，就不会把“模型升级”“Agent 设计”“工作流编排”“知识库建设”混成一件事。

## 最容易混淆的 4 组概念

<div class="llm-visual-guide__compare-grid">
  <div class="llm-visual-guide__compare-card">
    <strong>模型 vs Agent</strong>
    <p><span>模型</span>决定系统能不能理解和生成；<span>Agent</span>决定系统能不能围绕目标持续执行。</p>
  </div>
  <div class="llm-visual-guide__compare-card">
    <strong>Agent vs Workflow</strong>
    <p><span>Agent</span>擅长应对变化；<span>Workflow</span>擅长把高频步骤固化成稳定流程。</p>
  </div>
  <div class="llm-visual-guide__compare-card">
    <strong>MCP vs 工具本身</strong>
    <p><span>MCP</span>是统一接入方式；<span>工具</span>才是真正执行查询、写文件、调系统的能力来源。</p>
  </div>
  <div class="llm-visual-guide__compare-card">
    <strong>知识库 vs Memory</strong>
    <p><span>知识库</span>偏外部资料检索；<span>Memory</span>偏系统自己的状态、偏好与经验延续。</p>
  </div>
</div>

<div class="llm-visual-guide__reading-steps">
  <div>
    <strong>第一步：先看层</strong>
    <p>遇到新概念，先判断它属于能力层、行动层、连接层、流程层还是记忆层。</p>
  </div>
  <div>
    <strong>第二步：再看连接</strong>
    <p>判断模型、工具、流程和记忆之间是否形成闭环，而不是只停留在一次回答。</p>
  </div>
  <div>
    <strong>第三步：最后看落地约束</strong>
    <p>权限、成本、可审计性和稳定性，往往决定一个方案能不能真的上线。</p>
  </div>
</div>

<section id="overview" class="llm-visual-guide__section">

## 01 总览：AI 世界里到底有哪些层

<div class="llm-visual-guide__figure llm-visual-guide__figure--tall">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(0)">查看大图</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(0)" @keydown.enter.prevent="openPreview(0)" @keydown.space.prevent="openPreview(0)">
    <img src="../../../static/llm/visual-guide/images/slices/01-ai-overview/part-1.png" alt="AI 入门总览图（上）" />
    <img src="../../../static/llm/visual-guide/images/slices/01-ai-overview/part-2.png" alt="AI 入门总览图（中）" />
    <img src="../../../static/llm/visual-guide/images/slices/01-ai-overview/part-3.png" alt="AI 入门总览图（下）" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>图解重点</span><p>先看清“模型是能力源头，Agent / Workflow / Memory 是模型之外的系统层”。</p></div>
</div>

这张总览图最适合拿来建立全局感。对初学者来说，最容易犯的错，就是把“模型、Agent、工作流、知识库、不同厂商模型”全部当成同一层的问题。实际上它们关注的是不同层面。

读这张图，只需要先抓住 4 个判断：

- **先问能力来源**：内容生成、理解上下文、分析意图，主要是模型层能力
- **再问行动能力**：会不会调工具、查文件、执行命令，这才进入 Agent 层
- **再问接入方式**：工具是直接用 CLI、API，还是用 MCP 统一接入，这是连接层问题
- **最后问长期复用**：是否能把规则、文档、经验和历史上下文保留下来，这是知识层问题

这一张图的意义，不是背定义，而是先把“层”分开。层分开后，你就更容易判断自己讨论的是模型问题、系统问题，还是流程问题。

更实用的阅读顺序是：

- **第一步先识别“能力源头”**：哪些事情是模型天然会的，哪些不是
- **第二步再看“系统外壳”**：Agent、Workflow、Memory 都是在模型外面补能力
- **第三步理解“现实约束”**：成本、权限、工具接入、稳定性，都会把一个 AI 产品拉回工程现实

<div class="llm-visual-guide__insight">
  <strong>这一节最该带走的结论：</strong>遇到一个新 AI 产品时，先别急着问“它用的是什么模型”，而要先问“它把模型外的系统能力做到了哪一层”。很多产品差异，其实就出在这里。
</div>

</section>

<section id="model" class="llm-visual-guide__section">

## 02 什么叫模型：AI 的能力边界从哪里来

<div class="llm-visual-guide__figure llm-visual-guide__figure--tall">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(1)">查看大图</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(1)" @keydown.enter.prevent="openPreview(1)" @keydown.space.prevent="openPreview(1)">
    <img src="../../../static/llm/visual-guide/images/slices/02-what-is-a-model/part-1.png" alt="什么叫模型（上）" />
    <img src="../../../static/llm/visual-guide/images/slices/02-what-is-a-model/part-2.png" alt="什么叫模型（中）" />
    <img src="../../../static/llm/visual-guide/images/slices/02-what-is-a-model/part-3.png" alt="什么叫模型（下）" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>图解重点</span><p>把“会说”与“会做”分开看，模型擅长认知与生成，但默认不直接行动。</p></div>
</div>

模型可以理解成一个经过大量数据训练出来的“概率引擎”。它最重要的，不是“会不会聊天”，而是能力边界：

- **知识边界**：训练数据有截止时间，不一定知道最新世界发生了什么
- **执行边界**：模型能告诉你“应该怎么做”，但默认并不会亲自去做
- **上下文边界**：模型不是无限记忆体，它只能在有限上下文窗口里做判断
- **成本边界**：更强的模型通常更贵、更慢，也更需要精细调度

所以“模型更强”不等于“产品一定更好用”。真正决定体验的，往往还包括提示词、上下文管理、工具接入和任务拆解。

看这一节时，再多问自己 3 个问题：

- **模型擅长什么**：语言理解、模式归纳、文本生成、结构化输出
- **模型不擅长什么**：实时事实获取、长期状态保存、外部世界直接执行
- **模型最怕什么**：信息不足、上下文混乱、目标模糊、约束不清

<div class="llm-visual-guide__insight">
  <strong>这一节最该带走的结论：</strong>模型回答得像不像人，并不是最重要的；真正重要的是，你是否理解了它在哪些地方必须借助外部系统来补足能力边界。
</div>

</section>

<section id="agent" class="llm-visual-guide__section">

## 03 什么是 Agent：从“会说”到“会做”

<div class="llm-visual-guide__figure llm-visual-guide__figure--portrait">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(2)">查看大图</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(2)" @keydown.enter.prevent="openPreview(2)" @keydown.space.prevent="openPreview(2)">
    <img src="../../../static/llm/visual-guide/images/slices/03-what-is-an-agent/part-1.png" alt="什么是 Agent（上）" />
    <img src="../../../static/llm/visual-guide/images/slices/03-what-is-an-agent/part-2.png" alt="什么是 Agent（中）" />
    <img src="../../../static/llm/visual-guide/images/slices/03-what-is-an-agent/part-3.png" alt="什么是 Agent（下）" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>图解重点</span><p>观察 Agent 如何把目标、工具、执行和反馈连接成一个循环，而不只是一次回答。</p></div>
</div>

如果说模型是一颗大脑，那么 Agent 就是一套让这颗大脑真正进入任务现场的工作系统。它不只是生成一句回答，而是围绕目标持续行动。

你可以把 Agent 理解成“带执行循环的大模型系统”，通常至少包含这些环节：

- 接收目标：理解用户到底要完成什么结果
- 制定动作：决定下一步该查、该算、该调用哪个工具
- 执行与观察：拿到真实外部结果，而不是只靠模型臆测
- 继续迭代：根据新信息调整后续动作，直到完成任务

判断一个系统是不是 Agent，通常问 4 个问题就够了：

- 它是不是只回答一句话，还是会继续做后续动作
- 它能不能调用工具、文件、浏览器、命令行或业务系统
- 它会不会根据执行结果调整下一步，而不是一次生成到底
- 它是否具备最基本的任务状态和执行循环

<div class="llm-visual-guide__insight">
  <strong>这一节最该带走的结论：</strong>Agent 不是另一个模型，而是让模型从“只会生成”升级到“能围绕目标执行”的系统外壳。
</div>

</section>

<section id="mcp" class="llm-visual-guide__section">

## 04 什么是 MCP：给工具接入装统一插头

<div class="llm-visual-guide__figure llm-visual-guide__figure--balanced">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(3)">查看大图</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(3)" @keydown.enter.prevent="openPreview(3)" @keydown.space.prevent="openPreview(3)">
    <img src="../../../static/llm/visual-guide/images/slices/04-what-is-mcp/part-1.png" alt="什么是 MCP（上）" />
    <img src="../../../static/llm/visual-guide/images/slices/04-what-is-mcp/part-2.png" alt="什么是 MCP（中）" />
    <img src="../../../static/llm/visual-guide/images/slices/04-what-is-mcp/part-3.png" alt="什么是 MCP（下）" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>图解重点</span><p>不要把 MCP 当成“更聪明的模型”，它更像让工具接入变统一的标准化通道。</p></div>
</div>

当 Agent 要连接越来越多工具时，工程复杂度会迅速膨胀。MCP（Model Context Protocol）想解决的，就是工具接入碎片化的问题。

MCP 的价值通常体现在 3 个方面：

- **统一发现**：Agent 可以先知道“有哪些工具可用”
- **统一调用**：用相似的方式发起工具调用，而不是每接一个系统都重造一套逻辑
- **统一约束**：更容易建立权限、认证、边界和可审计性

一个很重要的认知是：**MCP 解决的首先是工程接入问题，而不是推理问题。** 它不会让模型突然更聪明，但会让工具接入更规范、更可管理。

把它和前后几层连起来看：

- **模型** 决定“该不该调用工具”
- **Agent** 决定“什么时候调用、先调什么、调完后怎么继续”
- **MCP** 决定“工具之间有没有统一的接入语言”
- **工作流** 决定“这些调用步骤能不能沉淀成稳定流程”

如果你后续想深入看这条线，可以继续读本专题已有的这两篇：

- [第一章：Function Call / MCP / ReAct / Skills 技术栈](../chapter1/)
- [AI Agent 第六章：MCP vs CLI](../../agent/chapter6/)

<div class="llm-visual-guide__insight">
  <strong>这一节最该带走的结论：</strong>MCP 不是为了替代 Agent，而是为了让 Agent 更容易、也更规范地连接越来越复杂的工具世界。
</div>

</section>

<section id="workflow" class="llm-visual-guide__section">

## 05 什么是工作流：把能力变成稳定流程

<div class="llm-visual-guide__figure llm-visual-guide__figure--tall">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(4)">查看大图</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(4)" @keydown.enter.prevent="openPreview(4)" @keydown.space.prevent="openPreview(4)">
    <img src="../../../static/llm/visual-guide/images/slices/05-what-is-a-workflow/part-1.png" alt="什么是工作流（上）" />
    <img src="../../../static/llm/visual-guide/images/slices/05-what-is-a-workflow/part-2.png" alt="什么是工作流（中）" />
    <img src="../../../static/llm/visual-guide/images/slices/05-what-is-a-workflow/part-3.png" alt="什么是工作流（下）" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>图解重点</span><p>看清哪些步骤应该交给 Agent 自由判断，哪些步骤更适合固化成 SOP。</p></div>
</div>

很多团队做 AI 系统时，最先得到的是几个“能跑通”的 Demo；但一旦要稳定交付，就必须把“这次刚好成功”变成“下次还能重复成功”。这就是工作流的价值。

工作流最常见的场景包括：

- 固定顺序任务：例如抓取资料 → 清洗内容 → 生成文稿 → 审核发布
- 多阶段审批：例如先生成，再校验，再人工确认
- 稳定运营流程：例如日报、周报、客服回复、知识整理
- 和 Agent 配合：把高自由度决策留给 Agent，把稳定步骤沉淀成流程

Workflow 常常承担 3 个角色：

- **给复杂任务定顺序**：先做什么、后做什么、谁来审核
- **给不稳定步骤加护栏**：哪些地方必须人工确认，哪些地方必须结构化输出
- **给团队经验沉淀模板**：把一次成功做法变成下次还能重复跑的 SOP

<div class="llm-visual-guide__insight">
  <strong>这一节最该带走的结论：</strong>工作流的价值，不是让系统看起来更自动化，而是把原本偶然成功的过程，变成稳定可复用的生产能力。
</div>

</section>

<section id="memory" class="llm-visual-guide__section">

## 06 什么是知识库 / Memory：让系统不再每次从零开始

<div class="llm-visual-guide__figure llm-visual-guide__figure--portrait">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(5)">查看大图</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(5)" @keydown.enter.prevent="openPreview(5)" @keydown.space.prevent="openPreview(5)">
    <img src="../../../static/llm/visual-guide/images/slices/06-knowledge-base-and-memory/part-1.png" alt="什么是知识库和 Memory（上）" />
    <img src="../../../static/llm/visual-guide/images/slices/06-knowledge-base-and-memory/part-2.png" alt="什么是知识库和 Memory（中）" />
    <img src="../../../static/llm/visual-guide/images/slices/06-knowledge-base-and-memory/part-3.png" alt="什么是知识库和 Memory（下）" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>图解重点</span><p>把“外部知识检索”和“系统内部记忆延续”分开，这会直接影响后续架构设计。</p></div>
</div>

知识库和 Memory 经常被混用，但它们并不完全一样。最简单的区分是：

- **知识库** 更像“外部资料库”，重点是文档、文件、说明书、FAQ、业务资料的存储与检索
- **Memory** 更像“系统自己的记忆层”，重点是历史对话、用户偏好、任务状态、经验摘要与上下文延续

它们共同解决的问题都是：**不要让模型每次都从空白上下文重新开始。** 这层能力通常在真实业务里很快变得重要，因为：

- 用户有长期偏好，需要记住
- 任务有历史上下文，需要延续
- 外部知识很多，不可能全部塞进 prompt
- 成功经验需要沉淀，否则每次都重复试错

进一步看，这一层可以拆成两个方向：

- **知识型沉淀**：把公司资料、产品文档、历史案例、FAQ 等放进可检索的知识体系
- **状态型沉淀**：把用户偏好、当前任务进度、历史对话、执行结果和经验摘要保留下来

<div class="llm-visual-guide__insight">
  <strong>这一节最该带走的结论：</strong>知识库 / Memory 不是锦上添花，而是让 AI 从“一次性回答工具”走向“长期协作系统”的关键一层。
</div>

</section>

<section id="compare" class="llm-visual-guide__section">

## 07 GPT、Claude、Gemini 有什么区别

<div class="llm-visual-guide__figure llm-visual-guide__figure--portrait">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(6)">查看大图</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(6)" @keydown.enter.prevent="openPreview(6)" @keydown.space.prevent="openPreview(6)">
    <img src="../../../static/llm/visual-guide/images/slices/07-gpt-vs-claude-vs-gemini/part-1.png" alt="GPT、Claude、Gemini 的区别（上）" />
    <img src="../../../static/llm/visual-guide/images/slices/07-gpt-vs-claude-vs-gemini/part-2.png" alt="GPT、Claude、Gemini 的区别（中）" />
    <img src="../../../static/llm/visual-guide/images/slices/07-gpt-vs-claude-vs-gemini/part-3.png" alt="GPT、Claude、Gemini 的区别（下）" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>图解重点</span><p>别只比较榜单，优先比较不同模型在风格、成本、上下文稳定性和生态集成上的匹配度。</p></div>
</div>

当你已经理解模型、Agent、MCP、工作流和 Memory 这些层次后，再看 GPT、Claude、Gemini 的差异，就不容易陷入“只比参数”或“只看榜单”的误区。

更有价值的比较维度包括：

- **通用对话与写作风格**：谁更稳定、谁更自然、谁更适合长文本整理
- **代码与工具调用能力**：谁更擅长结构化输出、函数调用与工程任务
- **上下文处理体验**：长上下文是否稳定、是否容易漂移、总结能力如何
- **生态整合方式**：各家产品如何把模型放进 IDE、文档、办公流和企业能力里

真正有价值的问法通常不是“谁更强”，而是：

- 你的任务更偏写作、代码、分析，还是多工具执行
- 你更在乎单次效果，还是长期成本与集成方式
- 你需要的是个人助手，还是面向团队或客户的产品能力
- 你准备把模型放进怎样的系统外壳里：聊天框、IDE、工作流平台，还是企业 SaaS

<div class="llm-visual-guide__insight">
  <strong>这一节最该带走的结论：</strong>模型对比的真正目标，不是找到一个永久赢家，而是找到在你的系统结构、成本约束和任务形态下最合适的那一个。
</div>

</section>

## 最后，把整条线重新串起来

<div class="llm-visual-guide__summary-grid">
  <div>
    <strong>模型</strong>
    <p>决定系统会不会理解、生成、推理与结构化表达。</p>
  </div>
  <div>
    <strong>Agent</strong>
    <p>决定系统能不能围绕目标调用工具、分步执行并完成任务。</p>
  </div>
  <div>
    <strong>MCP</strong>
    <p>决定工具如何被统一发现、接入和管理。</p>
  </div>
  <div>
    <strong>工作流</strong>
    <p>决定高频任务能否变成稳定、可审计、可复用的流程。</p>
  </div>
  <div>
    <strong>知识库 / Memory</strong>
    <p>决定系统能否保留资料、历史与经验，而不是每次从零开始。</p>
  </div>
  <div>
    <strong>模型选型</strong>
    <p>决定在不同成本、速度、风格与生态之间如何取舍。</p>
  </div>
</div>

如果你是第一次进入这条线，这一页最重要的作用不是替你学完全部细节，而是先把地图立起来。

## 如果你正准备自己搭一套 AI 系统

<div class="llm-visual-guide__build-grid">
  <div class="llm-visual-guide__build-card">
    <strong>1. 先定义任务形态</strong>
    <p>这是单轮问答、长链路执行，还是高频重复流程？不同任务形态，对 Agent 和 Workflow 的依赖完全不同。</p>
  </div>
  <div class="llm-visual-guide__build-card">
    <strong>2. 再定义模型职责</strong>
    <p>哪些环节交给模型推理，哪些环节必须交给真实系统执行，尽早把边界切清楚。</p>
  </div>
  <div class="llm-visual-guide__build-card">
    <strong>3. 设计工具接入方式</strong>
    <p>工具少时可以直接接 API / CLI；工具多、权限复杂时，再考虑用 MCP 做统一接入与治理。</p>
  </div>
  <div class="llm-visual-guide__build-card">
    <strong>4. 给流程加护栏</strong>
    <p>把容易出错、需要审批或必须留痕的步骤沉淀成 Workflow，不要把一切都交给自由发挥。</p>
  </div>
  <div class="llm-visual-guide__build-card">
    <strong>5. 提前规划 Memory</strong>
    <p>明确什么该记、记多久、谁能读、何时清理。很多系统不是做不出来，而是记忆治理做不下去。</p>
  </div>
  <div class="llm-visual-guide__build-card">
    <strong>6. 用评估闭环验证方案</strong>
    <p>别只看 Demo 漂不漂亮，要持续评估成功率、延迟、成本、可解释性和人工介入点。</p>
  </div>
</div>

下一步推荐阅读：

1. [第一章：Function Call / MCP / ReAct / Skills 技术栈](../chapter1/)
2. [第二章：Hermes-Agent 自学习 Skill 机制](../chapter2/)
3. [AI Agent 第六章：MCP vs CLI](../../agent/chapter6/)

<transition name="llm-preview-fade">
  <div v-if="isPreviewOpen" class="llm-visual-guide__preview" @click="closePreview">
    <div class="llm-visual-guide__preview-dialog" :class="{ 'is-tall': isTallPreview }" @click.stop>
      <div class="llm-visual-guide__preview-topbar" :class="{ 'is-tall': isTallPreview }">
        <div class="llm-visual-guide__preview-meta">
          <div class="llm-visual-guide__preview-eyebrow">当前图片预览</div>
          <div class="llm-visual-guide__preview-title">{{ currentPreview.title }}</div>
        </div>
        <div class="llm-visual-guide__preview-actions" :class="{ 'is-tall': isTallPreview }">
          <span class="llm-visual-guide__preview-counter">{{ previewCounterText }}</span>
          <a class="llm-visual-guide__preview-open" :href="currentPreview.src" target="_blank" rel="noreferrer">{{ isTallPreview ? '原图' : '新开原图' }}</a>
          <button class="llm-visual-guide__preview-close" type="button" @click="closePreview">关闭</button>
        </div>
      </div>
      <div ref="previewStageRef" class="llm-visual-guide__preview-stage" :class="{ 'is-tall': isTallPreview }">
        <button class="llm-visual-guide__preview-nav llm-visual-guide__preview-nav--prev" type="button" @click="showPrev" aria-label="查看上一张">
          <span class="llm-visual-guide__preview-nav-icon" aria-hidden="true">‹</span>
          <span class="llm-visual-guide__preview-nav-label">上一张</span>
        </button>
        <img class="llm-visual-guide__preview-image" :class="{ 'is-tall': isTallPreview }" :src="currentPreview.src" :alt="currentPreview.title" @load="onPreviewImageLoad" />
        <button class="llm-visual-guide__preview-nav llm-visual-guide__preview-nav--next" type="button" @click="showNext" aria-label="查看下一张">
          <span class="llm-visual-guide__preview-nav-label">下一张</span>
          <span class="llm-visual-guide__preview-nav-icon" aria-hidden="true">›</span>
        </button>
      </div>
      <div class="llm-visual-guide__preview-footer">
        <span>{{ isTallPreview ? '长图已按可阅读宽度展开，可上下滚动查看细节' : '直接展示原图，滚动即可看细节' }}</span>
        <span>支持键盘 `←` `→` 切换，点击空白处关闭</span>
      </div>
    </div>
  </div>
</transition>

</div>

<style>
.llm-visual-guide {
  --llm-guide-ink: #20313f;
  --llm-guide-muted: #5c7387;
  --llm-guide-line: rgba(67, 90, 111, 0.16);
  --llm-guide-soft: #f7f8fa;
  --llm-guide-warm: linear-gradient(180deg, #fffaf1 0%, #ffffff 100%);
  --llm-guide-accent: #0f6ab5;
  --llm-guide-accent-2: #eab308;
  --llm-guide-card-bg: #ffffff;
  --llm-guide-card-bg-soft: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(247, 251, 255, 0.98) 100%);
  --llm-guide-lead-bg: #fffdf5;
  --llm-guide-caption-bg: linear-gradient(180deg, #fffdf9 0%, #fff8ef 100%);
  --llm-guide-caption-ink: #6b7280;
  --llm-guide-caption-tag-bg: #ffe7bf;
  --llm-guide-caption-tag-ink: #9a5c00;
  --llm-guide-preview-panel: linear-gradient(180deg, rgba(251, 252, 255, 0.98) 0%, rgba(244, 248, 255, 0.96) 100%);
  --llm-guide-preview-stage: radial-gradient(circle at top left, rgba(255, 245, 218, 0.96) 0%, rgba(255, 250, 241, 0.96) 28%, rgba(244, 248, 255, 0.94) 100%);
  --llm-guide-preview-open-bg: rgba(255, 248, 228, 0.96);
  --llm-guide-preview-open-ink: #8a5a00;
  --llm-guide-preview-close-bg: #eaf2ff;
  --llm-guide-preview-image-bg: #ffffff;
  color: var(--llm-guide-ink);
  font-size: 16px;
  line-height: 1.9;
}

.dark .llm-visual-guide {
  --llm-guide-ink: #e5edf7;
  --llm-guide-muted: #a8b5c7;
  --llm-guide-line: rgba(148, 163, 184, 0.2);
  --llm-guide-soft: #0f172a;
  --llm-guide-warm: linear-gradient(180deg, rgba(41, 51, 67, 0.86) 0%, rgba(15, 23, 42, 0.92) 100%);
  --llm-guide-accent: #7ec8ff;
  --llm-guide-accent-2: #f2c365;
  --llm-guide-card-bg: #141c2b;
  --llm-guide-card-bg-soft: linear-gradient(180deg, rgba(20, 28, 43, 0.98) 0%, rgba(16, 23, 37, 0.98) 100%);
  --llm-guide-lead-bg: rgba(35, 45, 61, 0.85);
  --llm-guide-caption-bg: linear-gradient(180deg, rgba(37, 44, 58, 0.98) 0%, rgba(24, 31, 44, 0.98) 100%);
  --llm-guide-caption-ink: #c1cede;
  --llm-guide-caption-tag-bg: rgba(242, 195, 101, 0.16);
  --llm-guide-caption-tag-ink: #ffd88d;
  --llm-guide-preview-panel: linear-gradient(180deg, rgba(14, 20, 31, 0.98) 0%, rgba(20, 27, 40, 0.96) 100%);
  --llm-guide-preview-stage: radial-gradient(circle at top left, rgba(55, 49, 34, 0.88) 0%, rgba(24, 28, 37, 0.94) 32%, rgba(15, 23, 42, 0.98) 100%);
  --llm-guide-preview-open-bg: rgba(94, 74, 23, 0.36);
  --llm-guide-preview-open-ink: #ffe09b;
  --llm-guide-preview-close-bg: rgba(42, 79, 124, 0.36);
  --llm-guide-preview-image-bg: #0f172a;
}

.llm-visual-guide__hero {
  padding: 28px 24px 22px;
  border: 1px solid var(--llm-guide-line);
  border-radius: 20px;
  background: var(--llm-guide-warm);
  box-shadow: 0 10px 28px rgba(19, 53, 85, 0.05);
}

.llm-visual-guide__eyebrow {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.76);
  color: var(--llm-guide-accent);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.llm-visual-guide__hero h1 {
  margin: 16px 0 12px;
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.08;
  letter-spacing: -0.03em;
}

.llm-visual-guide__subtitle {
  margin: 0;
  font-size: 1.02rem;
  line-height: 1.9;
  color: var(--llm-guide-muted);
}

.llm-visual-guide__tags,
.llm-visual-guide__quick-grid,
.llm-visual-guide__toc,
.llm-visual-guide__summary-grid,
.llm-visual-guide__path-grid,
.llm-visual-guide__compare-grid,
.llm-visual-guide__build-grid {
  display: grid;
  gap: 12px;
}

.llm-visual-guide__quick-grid {
  margin: 18px 0 26px;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.llm-visual-guide__tags {
  margin-top: 18px;
  grid-template-columns: repeat(auto-fit, minmax(140px, max-content));
}

.llm-visual-guide__tags span {
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(15, 106, 181, 0.1);
  font-size: 0.88rem;
  color: var(--llm-guide-ink);
}

.llm-visual-guide__lead {
  margin: 18px 0 22px;
  padding: 14px 16px;
  border-left: 4px solid var(--llm-guide-accent-2);
  background: var(--llm-guide-lead-bg);
  border-radius: 0 14px 14px 0;
}

.llm-visual-guide__lead p {
  margin: 0;
}

.llm-visual-guide__quick-card,
.llm-visual-guide__compare-card,
.llm-visual-guide__build-card {
  padding: 16px;
  border-radius: 16px;
  border: 1px solid var(--llm-guide-line);
  background: var(--llm-guide-card-bg);
  box-shadow: 0 10px 22px rgba(19, 53, 85, 0.04);
}

.llm-visual-guide__quick-card span,
.llm-visual-guide__build-card strong + p,
.llm-visual-guide__compare-card span {
  color: var(--llm-guide-accent);
}

.llm-visual-guide__quick-card span {
  display: inline-flex;
  margin-bottom: 10px;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(15, 106, 181, 0.08);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.llm-visual-guide__quick-card strong,
.llm-visual-guide__compare-card strong,
.llm-visual-guide__build-card strong {
  display: block;
  margin-bottom: 8px;
  font-size: 1rem;
}

.llm-visual-guide__quick-card p,
.llm-visual-guide__compare-card p,
.llm-visual-guide__build-card p,
.llm-visual-guide__reading-steps p {
  margin: 0;
  color: var(--llm-guide-muted);
  line-height: 1.75;
}

.llm-visual-guide__quick-card--accent {
  background: linear-gradient(180deg, rgba(255, 249, 235, 0.92) 0%, var(--llm-guide-card-bg) 100%);
  border-color: rgba(234, 179, 8, 0.22);
}

.llm-visual-guide__toc {
  margin: 26px 0;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.llm-visual-guide__toc a,
.llm-visual-guide__path-card,
.llm-visual-guide__summary-grid div {
  padding: 15px 16px;
  border-radius: 14px;
  border: 1px solid var(--llm-guide-line);
  background: var(--llm-guide-card-bg);
  text-decoration: none;
  color: var(--llm-guide-ink);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.llm-visual-guide__toc a:hover {
  transform: translateY(-2px);
  border-color: rgba(15, 106, 181, 0.28);
  box-shadow: 0 14px 28px rgba(19, 53, 85, 0.08);
}

.llm-visual-guide__path-grid {
  margin: 16px 0 28px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.llm-visual-guide__path-card {
  text-decoration: none;
  color: var(--llm-guide-ink);
  background: var(--llm-guide-card-bg-soft);

}

.llm-visual-guide__path-card:hover {
  transform: translateY(-2px);
  border-color: rgba(47, 127, 95, 0.22);
  box-shadow: 0 14px 28px rgba(19, 53, 85, 0.08);
}

.llm-visual-guide__path-kicker {
  display: inline-flex;
  margin-bottom: 10px;
  padding: 5px 10px;
  border-radius: 999px;
  background: rgba(15, 106, 181, 0.08);
  color: var(--llm-guide-accent);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.llm-visual-guide__path-card strong {
  display: block;
  margin-bottom: 8px;
  font-size: 1rem;
}

.llm-visual-guide__path-card p {
  margin: 0;
  color: var(--llm-guide-muted);
  line-height: 1.7;
}

.llm-visual-guide__relation-map {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr) auto minmax(0, 1fr);
  gap: 14px;
  align-items: center;
  margin: 22px 0 18px;
}

.llm-visual-guide__relation-card {
  padding: 18px;
  border-radius: 16px;
  border: 1px solid var(--llm-guide-line);
  background: var(--llm-guide-card-bg);
  box-shadow: 0 8px 20px rgba(25, 48, 71, 0.05);
}

.llm-visual-guide__relation-card--memory {
  grid-column: 1 / -1;
  background: linear-gradient(180deg, var(--llm-guide-card-bg) 0%, rgba(35, 74, 56, 0.14) 100%);
}

.llm-visual-guide__relation-card strong {
  display: block;
  margin-bottom: 8px;
}

.llm-visual-guide__relation-card p,
.llm-visual-guide__insight {
  margin: 0;
  line-height: 1.8;
}

.llm-visual-guide__relation-arrow {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--llm-guide-accent);
}

.llm-visual-guide__relation-rail {
  grid-column: 1 / -1;
  padding: 12px 16px;
  border-radius: 16px;
  background: linear-gradient(90deg, rgba(15, 106, 181, 0.1) 0%, rgba(47, 127, 95, 0.1) 100%);
  color: var(--llm-guide-ink);
  text-align: center;
  font-size: 0.96rem;
}

.llm-visual-guide__compare-grid {
  margin: 18px 0 20px;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
}

.llm-visual-guide__compare-card span {
  font-weight: 700;
}

.llm-visual-guide__reading-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 12px;
  margin: 18px 0 8px;
}

.llm-visual-guide__reading-steps div {
  padding: 16px;
  border-radius: 16px;
  background: linear-gradient(180deg, var(--llm-guide-card-bg) 0%, rgba(24, 60, 96, 0.08) 100%);
  border: 1px solid rgba(15, 106, 181, 0.12);
}

.llm-visual-guide__reading-steps strong {
  display: block;
  margin-bottom: 8px;
}

.llm-visual-guide__section {
  margin-top: 38px;
}

.llm-visual-guide__figure {
  margin: 20px 0 26px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  width: min(1240px, calc(100vw - 40px));
}

.llm-visual-guide__figure-top {
  display: flex;
  justify-content: flex-end;
  margin: 0 6px 10px;
}

.llm-visual-guide__figure--tall {
  width: min(941px, calc(100vw - 32px));
}

.llm-visual-guide__figure--portrait {
  width: min(1024px, calc(100vw - 32px));
}

.llm-visual-guide__figure--balanced {
  width: min(1122px, calc(100vw - 32px));
}

.llm-visual-guide__figure-stack {
  display: grid;
  gap: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 12px 28px rgba(31, 41, 55, 0.12);
}

.llm-visual-guide__figure-stack--interactive {
  cursor: zoom-in;
}

.llm-visual-guide__figure-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 1px solid rgba(39, 83, 232, 0.16);
  cursor: pointer;
  font-family: inherit;
  padding: 8px 14px 8px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.94);
  color: #2753e8;
  font-size: 0.9rem;
  font-weight: 700;
  text-decoration: none;
  box-shadow: 0 10px 20px rgba(39, 83, 232, 0.12);
}

.llm-visual-guide__figure-link::before {
  content: '⤢';
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border-radius: 999px;
  background: linear-gradient(180deg, #2753e8 0%, #5b6df6 100%);
  color: #fff;
  font-size: 0.82rem;
  line-height: 1;
}

.llm-visual-guide__figure img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 0;
  box-shadow: none;
}

.llm-visual-guide__figure-caption {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin: 12px 0 4px;
  padding: 12px 14px;
  border-radius: 14px;
  background: var(--llm-guide-caption-bg);
  border: 1px solid rgba(240, 211, 167, 0.72);
  color: var(--llm-guide-caption-ink);
  line-height: 1.75;
}

.llm-visual-guide__figure-caption span {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--llm-guide-caption-tag-bg);
  color: var(--llm-guide-caption-tag-ink);
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.llm-visual-guide__figure-caption p {
  margin: 0;
  font-size: 0.92rem;
}

.llm-visual-guide__insight {
  margin-top: 18px;
  padding: 16px 18px;
  border-radius: 14px;
  border: 1px solid rgba(15, 106, 181, 0.12);
  background: linear-gradient(180deg, var(--llm-guide-card-bg) 0%, rgba(24, 60, 96, 0.08) 100%);
}

.llm-visual-guide__summary-grid {
  margin: 22px 0 18px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.llm-visual-guide__summary-grid strong {
  display: block;
  margin-bottom: 8px;
  font-size: 1rem;
}

.llm-visual-guide__summary-grid p {
  margin: 0;
  color: var(--llm-guide-muted);
  line-height: 1.75;
}

.llm-visual-guide__build-grid {
  margin: 18px 0 24px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.llm-preview-fade-enter-active,
.llm-preview-fade-leave-active {
  transition: opacity 0.2s ease;
}

.llm-preview-fade-enter-from,
.llm-preview-fade-leave-to {
  opacity: 0;
}

.llm-visual-guide__preview {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(15, 23, 42, 0.66);
  backdrop-filter: blur(8px);
}

.llm-visual-guide__preview-dialog {
  position: relative;
  width: min(1480px, calc(100vw - 32px));
  height: calc(100vh - 32px);
  padding: 18px 18px 14px;
  border-radius: 28px;
  background: var(--llm-guide-preview-panel);
  border: 1px solid rgba(255, 255, 255, 0.36);
  box-shadow: 0 24px 80px rgba(15, 23, 42, 0.32);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  gap: 14px;
}

.llm-visual-guide__preview-dialog.is-tall {
  width: min(1120px, calc(100vw - 40px));
}

.llm-visual-guide__preview-topbar,
.llm-visual-guide__preview-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.llm-visual-guide__preview-meta {
  min-width: 0;
}

.llm-visual-guide__preview-topbar.is-tall {
  gap: 12px;
  padding: 0 4px;
}

.llm-visual-guide__preview-topbar.is-tall .llm-visual-guide__preview-meta {
  flex: 1;
}

.llm-visual-guide__preview-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.llm-visual-guide__preview-actions.is-tall {
  gap: 8px;
  flex-wrap: nowrap;
}

.llm-visual-guide__preview-eyebrow {
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--llm-guide-accent);
}

.llm-visual-guide__preview-title {
  margin-top: 4px;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--llm-guide-ink);
}

.llm-visual-guide__preview-topbar.is-tall .llm-visual-guide__preview-eyebrow {
  display: none;
}

.llm-visual-guide__preview-topbar.is-tall .llm-visual-guide__preview-title {
  margin-top: 0;
  font-size: 0.96rem;
  line-height: 1.35;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.llm-visual-guide__preview-counter {
  display: inline-flex;
  align-items: center;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(15, 106, 181, 0.08);
  color: var(--llm-guide-accent);
  font-size: 0.84rem;
  font-weight: 700;
}

.llm-visual-guide__preview-actions.is-tall .llm-visual-guide__preview-counter {
  padding: 6px 10px;
  font-size: 0.78rem;
}

.llm-visual-guide__preview-close,
.llm-visual-guide__preview-nav,
.llm-visual-guide__preview-open {
  border: 0;
  font-family: inherit;
}

.llm-visual-guide__preview-open,
.llm-visual-guide__preview-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 16px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.llm-visual-guide__preview-actions.is-tall .llm-visual-guide__preview-open,
.llm-visual-guide__preview-actions.is-tall .llm-visual-guide__preview-close {
  padding: 8px 12px;
  font-size: 0.82rem;
  box-shadow: none;
}

.llm-visual-guide__preview-open {
  background: var(--llm-guide-preview-open-bg);
  color: var(--llm-guide-preview-open-ink);
  box-shadow: 0 10px 24px rgba(212, 164, 53, 0.14);
}

.llm-visual-guide__preview-close {
  background: var(--llm-guide-preview-close-bg);
  color: var(--llm-guide-accent);
  box-shadow: 0 10px 24px rgba(39, 83, 232, 0.12);
}

.llm-visual-guide__preview-open:hover,
.llm-visual-guide__preview-close:hover {
  transform: translateY(-1px);
}

.llm-visual-guide__preview-stage {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 0;
  overflow: auto;
  padding: 28px 88px;
  border-radius: 22px;
  background: var(--llm-guide-preview-stage);
  border: 1px solid rgba(223, 231, 244, 0.9);
}

.llm-visual-guide__preview-stage.is-tall {
  align-items: flex-start;
  padding: 18px 36px 24px;
}

.llm-visual-guide__preview-image {
  display: block;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  border-radius: 20px;
  padding: 8px;
  background: var(--llm-guide-preview-image-bg);
  box-shadow: 0 20px 42px rgba(31, 41, 55, 0.16);
}

.llm-visual-guide__preview-image.is-tall {
  width: min(980px, calc(100% - 8px));
  max-width: min(980px, calc(100% - 8px));
  max-height: none;
}

.llm-visual-guide__preview-nav {
  position: absolute;
  top: 50%;
  z-index: 2;
  width: 56px;
  height: 56px;
  border-radius: 999px;
  transform: translateY(-50%);
  border: 0;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.96);
  color: var(--llm-guide-accent);
  font-size: 1.5rem;
  font-weight: 700;
  box-shadow: 0 10px 22px rgba(31, 41, 55, 0.12);
  transition: width 0.22s ease, background 0.22s ease, box-shadow 0.22s ease, opacity 0.22s ease;
}

.llm-visual-guide__preview-nav-icon {
  line-height: 1;
}

.llm-visual-guide__preview-nav-label {
  max-width: 0;
  overflow: hidden;
  white-space: nowrap;
  opacity: 0;
  font-size: 0.82rem;
  letter-spacing: 0.02em;
  transition: max-width 0.2s ease, opacity 0.2s ease, margin 0.2s ease;
}

.llm-visual-guide__preview-nav--prev {
  left: 12px;
}

.llm-visual-guide__preview-nav--next {
  right: 12px;
}

.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav {
  width: 42px;
  height: 92px;
  padding: 0 10px;
  border: 1px solid rgba(126, 200, 255, 0.18);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(14px);
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.12);
  opacity: 0.92;
  overflow: hidden;
}

.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav--prev {
  left: 8px;
}

.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav--next {
  right: 8px;
}

.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav:hover,
.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav:focus-visible {
  width: 94px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 18px 32px rgba(15, 23, 42, 0.16);
  opacity: 1;
}

.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav:hover .llm-visual-guide__preview-nav-label,
.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav:focus-visible .llm-visual-guide__preview-nav-label {
  max-width: 42px;
  opacity: 1;
}

.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav--prev:hover .llm-visual-guide__preview-nav-label,
.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav--prev:focus-visible .llm-visual-guide__preview-nav-label {
  margin-left: 6px;
}

.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav--next:hover .llm-visual-guide__preview-nav-label,
.llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav--next:focus-visible .llm-visual-guide__preview-nav-label {
  margin-right: 6px;
}

.llm-visual-guide__preview-footer {
  padding: 0 4px;
  color: var(--llm-guide-muted);
  font-size: 0.88rem;
}

.dark .llm-visual-guide__tags span,
.dark .llm-visual-guide__figure-link,
.dark .llm-visual-guide__preview-nav {
  background: rgba(20, 28, 43, 0.92);
  color: var(--llm-guide-ink);
  border-color: rgba(126, 200, 255, 0.18);
}

.dark .llm-visual-guide__figure-link::before {
  background: linear-gradient(180deg, #4d90ff 0%, #7ec8ff 100%);
}

.dark .llm-visual-guide__relation-rail {
  background: linear-gradient(90deg, rgba(126, 200, 255, 0.12) 0%, rgba(93, 211, 158, 0.1) 100%);
}

@media (max-width: 640px) {
  .llm-visual-guide__hero {
    padding: 22px 18px 20px;
    border-radius: 18px;
  }

  .llm-visual-guide__hero h1 {
    max-width: none;
    font-size: clamp(2rem, 11vw, 3rem);
  }

  .llm-visual-guide__figure {
    left: auto;
    transform: none;
    width: 100%;
  }

  .llm-visual-guide__figure-top {
    margin: 0 2px 8px;
  }

  .llm-visual-guide__figure-link {
    padding: 7px 12px;
    font-size: 0.84rem;
  }

  .llm-visual-guide__figure-caption {
    flex-direction: column;
    gap: 8px;
    padding: 12px;
    border-radius: 12px;
  }

  .llm-visual-guide__preview {
    padding: 12px;
  }

  .llm-visual-guide__preview-dialog {
    width: 100%;
    height: calc(100vh - 24px);
    padding: 14px;
    border-radius: 18px;
  }

  .llm-visual-guide__preview-dialog.is-tall {
    width: 100%;
  }

  .llm-visual-guide__preview-topbar,
  .llm-visual-guide__preview-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .llm-visual-guide__preview-actions {
    width: 100%;
    justify-content: space-between;
  }

  .llm-visual-guide__preview-topbar.is-tall,
  .llm-visual-guide__preview-actions.is-tall {
    width: 100%;
  }

  .llm-visual-guide__preview-actions.is-tall {
    flex-wrap: wrap;
  }

  .llm-visual-guide__preview-topbar.is-tall .llm-visual-guide__preview-title {
    white-space: normal;
  }

  .llm-visual-guide__preview-stage {
    padding: 16px 12px 64px;
  }

  .llm-visual-guide__preview-stage.is-tall {
    padding: 12px 10px 64px;
  }

  .llm-visual-guide__preview-image.is-tall {
    width: 100%;
    max-width: 100%;
  }

  .llm-visual-guide__preview-nav {
    top: auto;
    bottom: 12px;
    transform: none;
    width: calc(50% - 18px);
    height: 44px;
    font-size: 1rem;
  }

  .llm-visual-guide__preview-nav--prev {
    left: 12px;
  }

  .llm-visual-guide__preview-nav--next {
    right: 12px;
  }

  .llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav {
    width: calc(50% - 18px);
    height: 44px;
    padding: 0 14px;
    border-radius: 14px;
    opacity: 1;
  }

  .llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav:hover,
  .llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav:focus-visible {
    width: calc(50% - 18px);
  }

  .llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav-label {
    max-width: none;
    opacity: 1;
  }

  .llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav--prev .llm-visual-guide__preview-nav-label {
    margin-left: 6px;
  }

  .llm-visual-guide__preview-stage.is-tall .llm-visual-guide__preview-nav--next .llm-visual-guide__preview-nav-label {
    margin-right: 6px;
  }

  .llm-visual-guide__preview-footer {
    gap: 6px;
  }

  .llm-visual-guide__relation-map {
    grid-template-columns: 1fr;
  }

  .llm-visual-guide__relation-arrow {
    justify-self: center;
    transform: rotate(90deg);
  }

  .llm-visual-guide__figure,
  .llm-visual-guide__relation-card,
  .llm-visual-guide__insight,
  .llm-visual-guide__quick-card,
  .llm-visual-guide__compare-card,
  .llm-visual-guide__build-card,
  .llm-visual-guide__path-card,
  .llm-visual-guide__lead,
  .llm-visual-guide__toc a,
  .llm-visual-guide__reading-steps div,
  .llm-visual-guide__summary-grid div {
    border-radius: 16px;
  }
}
</style>
