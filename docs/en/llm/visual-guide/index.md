---
title: "AI Visual Guide: From Models to Agents, MCP, Workflows, and Memory"
---

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

const previewImages = [
  { src: '../../../static/llm/visual-guide/images/01-ai-overview.png', title: '01 Overview: what layers exist in the AI stack?' },
  { src: '../../../static/llm/visual-guide/images/02-what-is-a-model.png', title: '02 What is a model: where capability boundaries come from' },
  { src: '../../../static/llm/visual-guide/images/03-what-is-an-agent.png', title: '03 What is an Agent: from “can say” to “can do”' },
  { src: '../../../static/llm/visual-guide/images/04-what-is-mcp.png', title: '04 What is MCP: a standard plug for external tools' },
  { src: '../../../static/llm/visual-guide/images/05-what-is-a-workflow.png', title: '05 What is a workflow: turning capability into stable execution' },
  { src: '../../../static/llm/visual-guide/images/06-knowledge-base-and-memory.png', title: '06 What is knowledge / memory: why systems should not restart from zero' },
  { src: '../../../static/llm/visual-guide/images/07-gpt-vs-claude-vs-gemini.png', title: '07 GPT vs Claude vs Gemini: how to think about the differences' }
]

const isPreviewOpen = ref(false)
const currentPreviewIndex = ref(0)
const currentPreview = computed(() => previewImages[currentPreviewIndex.value])
const previewScale = ref(1)
const previewScaleText = computed(() => `${Math.round(previewScale.value * 100)}%`)
const previewStageRef = ref(null)
const previewFitWidth = ref(960)
const previewCanvasStyle = computed(() => ({
  width: `${Math.max(320, previewFitWidth.value * previewScale.value)}px`
}))

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

const updatePreviewFitWidth = () => {
  nextTick(() => {
    const stage = previewStageRef.value
    if (!stage) return
    previewFitWidth.value = Math.max(320, stage.clientWidth - 40)
  })
}

const setPreviewScale = (scale) => {
  const nextScale = Math.min(4, Math.max(0.7, Number(scale.toFixed(2))))
  previewScale.value = nextScale
}

const resetPreviewViewport = () => {
  setPreviewScale(1)
  updatePreviewFitWidth()
  resetPreviewScroll()
}

const openPreview = (index) => {
  currentPreviewIndex.value = index
  isPreviewOpen.value = true
  lockBody()
  resetPreviewViewport()
}

const closePreview = () => {
  isPreviewOpen.value = false
  unlockBody()
}

const showPrev = () => {
  currentPreviewIndex.value = (currentPreviewIndex.value - 1 + previewImages.length) % previewImages.length
  resetPreviewViewport()
}

const showNext = () => {
  currentPreviewIndex.value = (currentPreviewIndex.value + 1) % previewImages.length
  resetPreviewViewport()
}

const zoomIn = () => {
  setPreviewScale(previewScale.value + 0.2)
}

const zoomOut = () => {
  setPreviewScale(previewScale.value - 0.2)
}

const onPreviewWheel = (event) => {
  if (!(event.ctrlKey || event.metaKey)) return
  event.preventDefault()
  if (event.deltaY < 0) zoomIn()
  else zoomOut()
}

const onPreviewImageDblclick = () => {
  if (previewScale.value < 1.6) {
    setPreviewScale(1.6)
    return
  }
  resetPreviewViewport()
}

const onWindowResize = () => {
  if (!isPreviewOpen.value) return
  updatePreviewFitWidth()
}

const onKeydown = (event) => {
  if (!isPreviewOpen.value) return
  if (event.key === 'Escape') closePreview()
  if (event.key === 'ArrowLeft') showPrev()
  if (event.key === 'ArrowRight') showNext()
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  window.addEventListener('resize', onWindowResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  window.removeEventListener('resize', onWindowResize)
  unlockBody()
})
</script>

<div class="llm-visual-guide">

<div class="llm-visual-guide__hero">
  <div class="llm-visual-guide__eyebrow">LLM Architecture Analysis · Visual Guide</div>
  <h1>One page to connect models, Agents, MCP, workflows, and memory</h1>
  <p class="llm-visual-guide__subtitle">If terms like models, Agents, MCP, workflows, and knowledge bases all sound familiar on their own but blur together in practice, this page is designed to place them back onto one clear map.</p>
  <div class="llm-visual-guide__tags">
    <span>AI Fundamentals</span>
    <span>Model vs Agent</span>
    <span>MCP</span>
    <span>Workflow</span>
    <span>Memory</span>
  </div>
</div>

<div class="llm-visual-guide__lead">
  <p><strong>Start with the main thread:</strong> the model handles understanding and generation, the Agent handles goal-driven action, MCP handles tool connectivity, workflows turn repeated steps into stable execution, and memory preserves context, materials, and experience. The seven visuals below unfold along that sequence.</p>
</div>

<div class="llm-visual-guide__toc">
  <a href="#overview">01 Overview: what layers exist in the AI stack?</a>
  <a href="#model">02 What is a model: where capability boundaries come from</a>
  <a href="#agent">03 What is an Agent: from “can say” to “can do”</a>
  <a href="#mcp">04 What is MCP: a standard plug for external tools</a>
  <a href="#workflow">05 What is a workflow: turning capability into stable execution</a>
  <a href="#memory">06 What is knowledge / memory: why systems should not restart from zero</a>
  <a href="#compare">07 GPT vs Claude vs Gemini: how to think about the differences</a>
</div>

## Where to start based on who you are

<div class="llm-visual-guide__path-grid">
  <a class="llm-visual-guide__path-card" href="#overview">
    <span class="llm-visual-guide__path-kicker">Beginners</span>
    <strong>Start with 01 Overview</strong>
    <p>Put models, Agents, MCP, workflows, and memory back onto one map before diving into individual definitions.</p>
  </a>
  <a class="llm-visual-guide__path-card" href="#model">
    <span class="llm-visual-guide__path-kicker">Product / Operations</span>
    <strong>Start with 02 Models + 05 Workflows</strong>
    <p>Understand model limits first, then see how reliable execution emerges through process design.</p>
  </a>
  <a class="llm-visual-guide__path-card" href="#agent">
    <span class="llm-visual-guide__path-kicker">Developers</span>
    <strong>Start with 03 Agents + 04 MCP</strong>
    <p>Get quickly into execution loops, tool use, protocol layers, and system boundaries.</p>
  </a>
  <a class="llm-visual-guide__path-card" href="#memory">
    <span class="llm-visual-guide__path-kicker">Knowledge-base builders</span>
    <strong>Start with 06 Memory</strong>
    <p>Separate retrieval from persistent system memory before deciding how workflows and Agents should use them.</p>
  </a>
</div>

## First, lock in the relationship map

Many introduction pieces define these concepts one by one. The faster way to build intuition is to understand how they relate to each other. Keep this text-based relationship map in mind:

<div class="llm-visual-guide__relation-map">
  <div class="llm-visual-guide__relation-card">
    <strong>Model</strong>
    <p>The cognitive engine that understands prompts, reasons over context, and generates outputs.</p>
  </div>
  <div class="llm-visual-guide__relation-arrow">-></div>
  <div class="llm-visual-guide__relation-card">
    <strong>Agent</strong>
    <p>The action layer that uses the model to decide, call tools, read results, and continue execution.</p>
  </div>
  <div class="llm-visual-guide__relation-arrow">-></div>
  <div class="llm-visual-guide__relation-card">
    <strong>Workflow</strong>
    <p>The structure that turns repeated tasks into stable, repeatable, and auditable execution paths.</p>
  </div>
  <div class="llm-visual-guide__relation-rail">
    <span>MCP / APIs / CLIs are the connectivity rails that let Agents reach the outside tool world</span>
  </div>
  <div class="llm-visual-guide__relation-card llm-visual-guide__relation-card--memory">
    <strong>Knowledge Base / Memory</strong>
    <p>The long-term layer that feeds models, Agents, and workflows with documents, history, preferences, and accumulated experience.</p>
  </div>
</div>

Read the stack this way:

- <strong>Models are the starting capability layer</strong>: without them, there is no understanding, reasoning, or generation.
- <strong>Agents are the action orchestration layer</strong>: they turn the model from a responder into an executor.
- <strong>Workflows are the reliability layer</strong>: they convert improvised success into repeatable delivery.
- <strong>Memory is the continuity layer</strong>: it keeps state, background, and experience from resetting every time.
- <strong>MCP / APIs / CLIs are connection channels</strong>: they are not the goal themselves, but the way systems touch real tools and data.

Once this relationship map is clear, it becomes much harder to confuse “model upgrades,” “Agent design,” “workflow orchestration,” and “knowledge architecture” as the same thing.

<section id="overview" class="llm-visual-guide__section">

## 01 Overview: what layers exist in the AI stack?

<div class="llm-visual-guide__figure llm-visual-guide__figure--tall">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(0)">View full image</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(0)" @keydown.enter.prevent="openPreview(0)" @keydown.space.prevent="openPreview(0)">
    <img src="../../../static/llm/visual-guide/images/slices/01-ai-overview/part-1.png" alt="AI overview visual guide part 1" />
    <img src="../../../static/llm/visual-guide/images/slices/01-ai-overview/part-2.png" alt="AI overview visual guide part 2" />
    <img src="../../../static/llm/visual-guide/images/slices/01-ai-overview/part-3.png" alt="AI overview visual guide part 3" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>Key idea</span><p>Start by separating the model as the capability core from the surrounding system layers like Agents, workflows, and memory.</p></div>
</div>

This overview works best as a map. The most common beginner mistake is to treat models, Agents, workflows, knowledge layers, and model vendors as one single category of problem. They are not. They live at different layers.

A useful way to read the stack is through four questions:

- <strong>Where does the capability come from?</strong> Understanding language, generating content, and making in-context judgments belong primarily to the model layer.
- <strong>Who actually acts?</strong> Once the system starts using tools, reading files, or executing commands, you have moved into the Agent layer.
- <strong>How does it connect?</strong> Whether the system reaches external tools through MCP, APIs, or CLIs is a connectivity-layer design choice.
- <strong>What persists over time?</strong> Documents, historical context, user preferences, and experience belong to the long-term knowledge layer.

The point of this overview is not to memorize vocabulary. It is to separate layers. Once the layers are separated, many AI debates become easier to decode: are people discussing model ability, system design, protocol design, or execution design?

A practical takeaway: when you look at any new AI product, do not ask only, “What model does it use?” Ask instead, “How much system capability has it built around the model?” That is often where the real product differentiation lives.

<div class="llm-visual-guide__insight">
  <strong>Takeaway:</strong> The more useful question is not “Which model is inside?” but “How much capability has the product built outside the model?”
</div>

</section>

<section id="model" class="llm-visual-guide__section">

## 02 What is a model: where capability boundaries come from

<div class="llm-visual-guide__figure llm-visual-guide__figure--tall">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(1)">View full image</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(1)" @keydown.enter.prevent="openPreview(1)" @keydown.space.prevent="openPreview(1)">
    <img src="../../../static/llm/visual-guide/images/slices/02-what-is-a-model/part-1.png" alt="What is a model visual guide part 1" />
    <img src="../../../static/llm/visual-guide/images/slices/02-what-is-a-model/part-2.png" alt="What is a model visual guide part 2" />
    <img src="../../../static/llm/visual-guide/images/slices/02-what-is-a-model/part-3.png" alt="What is a model visual guide part 3" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>Key idea</span><p>A model is excellent at understanding and generation, but “can speak” does not automatically mean “can act.”</p></div>
</div>

A model is best thought of as a trained probability engine. It does not store a literal encyclopedia in memory. Instead, it predicts the most plausible next output given the context it currently sees.

That is why the model layer should be understood through boundaries rather than personality:

- <strong>Knowledge boundary</strong>: training data has a cutoff and does not guarantee up-to-date facts.
- <strong>Execution boundary</strong>: a model can describe what should happen, but it will not automatically do it.
- <strong>Context boundary</strong>: it operates within a finite context window rather than infinite memory.
- <strong>Cost boundary</strong>: stronger models are usually more expensive, slower, and require smarter orchestration.

This also explains why “a better model” does not automatically produce “a better product.” Prompting, context management, tool integration, memory, and execution design can dominate the user experience.

Another useful lens is to ask three things:

- What are models naturally good at? Language understanding, summarization, pattern recognition, drafting, and structured outputs.
- What are they not naturally good at? Real-time retrieval, persistent memory, and direct external action.
- What do they fail on most easily? Missing information, messy context, vague goals, and unclear constraints.

In other words, the model is not the whole product. It is the reasoning core that still needs a surrounding system to become reliable and useful.

<div class="llm-visual-guide__insight">
  <strong>Takeaway:</strong> The most important thing is not whether a model sounds human. It is whether you understand where it still needs external system layers to close the gap.</div>

</section>

<section id="agent" class="llm-visual-guide__section">

## 03 What is an Agent: from “can say” to “can do”

<div class="llm-visual-guide__figure llm-visual-guide__figure--portrait">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(2)">View full image</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(2)" @keydown.enter.prevent="openPreview(2)" @keydown.space.prevent="openPreview(2)">
    <img src="../../../static/llm/visual-guide/images/slices/03-what-is-an-agent/part-1.png" alt="What is an Agent visual guide part 1" />
    <img src="../../../static/llm/visual-guide/images/slices/03-what-is-an-agent/part-2.png" alt="What is an Agent visual guide part 2" />
    <img src="../../../static/llm/visual-guide/images/slices/03-what-is-an-agent/part-3.png" alt="What is an Agent visual guide part 3" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>Key idea</span><p>An Agent links goals, tools, execution, and feedback into a loop rather than ending at one generated reply.</p></div>
</div>

If the model is the brain, the Agent is the working system that takes that brain into the task environment. It does not just generate one answer. It interprets goals, breaks work into steps, calls tools, observes results, and keeps going.

A simple way to describe an Agent is: <strong>a model wrapped in an execution loop</strong>. That loop typically includes:

- understanding the user’s actual goal,
- choosing the next action,
- using tools or environments,
- reading real observations,
- adjusting the next step based on what happened.

That is why Agents matter. Their value is not that they are “more advanced chatboxes.” Their value is that they get the system closer to real task completion.

A quick way to test whether something is functioning like an Agent is to ask:

- Does it stop at one answer, or continue with actions?
- Can it use files, browsers, commands, or business tools?
- Does it update its next step based on observations?
- Does it maintain a minimal execution state?

Once you think of the Agent as the action orchestration layer, many system design questions naturally appear: planning, approvals, rollback, memory, safety, and coordination.

<div class="llm-visual-guide__insight">
  <strong>Takeaway:</strong> An Agent is not another model. It is the outer system layer that turns a model from a generator into a goal-driven executor.</div>

</section>

<section id="mcp" class="llm-visual-guide__section">

## 04 What is MCP: a standard plug for external tools

<div class="llm-visual-guide__figure llm-visual-guide__figure--balanced">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(3)">View full image</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(3)" @keydown.enter.prevent="openPreview(3)" @keydown.space.prevent="openPreview(3)">
    <img src="../../../static/llm/visual-guide/images/slices/04-what-is-mcp/part-1.png" alt="What is MCP visual guide part 1" />
    <img src="../../../static/llm/visual-guide/images/slices/04-what-is-mcp/part-2.png" alt="What is MCP visual guide part 2" />
    <img src="../../../static/llm/visual-guide/images/slices/04-what-is-mcp/part-3.png" alt="What is MCP visual guide part 3" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>Key idea</span><p>MCP is not a smarter model. It is a standard way to connect tools and expose them more consistently to AI systems.</p></div>
</div>

As soon as Agents need to connect to more tools, engineering complexity grows quickly. Each tool has different interfaces, parameters, authentication rules, and response formats.

MCP tries to solve that fragmentation. It is best understood as a protocol layer between Agents and external capabilities.

Its value usually shows up in three places:

- <strong>Discovery</strong>: the Agent can first learn what tools exist.
- <strong>Invocation</strong>: tools can be called through a more consistent interface.
- <strong>Governance</strong>: permissions, identity, boundaries, and observability become easier to manage.

A critical mental shift: MCP solves an <strong>integration problem</strong> before it solves anything about reasoning. It does not make the model itself smarter. It makes tool connectivity more standard and more manageable.

That means the layers work together like this:

- the <strong>model</strong> decides whether tool use is needed,
- the <strong>Agent</strong> decides when and how to use tools,
- <strong>MCP</strong> standardizes how those tools are exposed,
- the <strong>workflow</strong> decides whether those calls become stable process steps.

This is why MCP matters much more as systems move from toy demos to multi-tool, multi-user, permission-sensitive production environments.

If you want to go deeper after this page, these are the best follow-ups:

- [Chapter 1: Function Calling, MCP, ReAct, and Skills](../chapter1/)
- [AI Agent Chapter 6: MCP vs CLI](../../agent/chapter6/)

<div class="llm-visual-guide__insight">
  <strong>Takeaway:</strong> MCP does not replace Agents. It makes Agents better connected to an increasingly complex external tool world.</div>

</section>

<section id="workflow" class="llm-visual-guide__section">

## 05 What is a workflow: turning capability into stable execution

<div class="llm-visual-guide__figure llm-visual-guide__figure--tall">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(4)">View full image</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(4)" @keydown.enter.prevent="openPreview(4)" @keydown.space.prevent="openPreview(4)">
    <img src="../../../static/llm/visual-guide/images/slices/05-what-is-a-workflow/part-1.png" alt="What is a workflow visual guide part 1" />
    <img src="../../../static/llm/visual-guide/images/slices/05-what-is-a-workflow/part-2.png" alt="What is a workflow visual guide part 2" />
    <img src="../../../static/llm/visual-guide/images/slices/05-what-is-a-workflow/part-3.png" alt="What is a workflow visual guide part 3" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>Key idea</span><p>The key question is which steps should stay flexible for the Agent and which ones should become stable SOPs.</p></div>
</div>

Many teams can get an AI demo to work once. The harder part is turning “it worked this time” into “it works reliably next time.” That is where workflows matter.

A workflow organizes repeated steps into a structure that is easier to inspect, reuse, and stabilize. Common examples include:

- collecting sources, then cleaning them, then generating a draft, then reviewing and publishing it,
- multi-stage approval flows,
- recurring operational tasks such as reports, summaries, support responses, and knowledge updates,
- hybrid systems where Agents handle high-variance decisions while workflows preserve predictable steps.

This means workflows are not “more advanced than Agents.” They answer a different question: <strong>which parts of the system should improvise, and which parts should become process?</strong>

As tasks become more repetitive, higher-risk, more collaborative, or more auditable, workflows usually matter more than pure Agent improvisation.

That is why the best mental model is division of labor:

- Agents handle variation.
- Workflows handle reliability.
- Strong systems usually combine both instead of forcing a choice between them.

<div class="llm-visual-guide__insight">
  <strong>Takeaway:</strong> The value of a workflow is not that it looks more automated. The value is that it turns occasional success into repeatable production capability.</div>

</section>

<section id="memory" class="llm-visual-guide__section">

## 06 What is knowledge / memory: why systems should not restart from zero

<div class="llm-visual-guide__figure llm-visual-guide__figure--portrait">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(5)">View full image</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(5)" @keydown.enter.prevent="openPreview(5)" @keydown.space.prevent="openPreview(5)">
    <img src="../../../static/llm/visual-guide/images/slices/06-knowledge-base-and-memory/part-1.png" alt="What is knowledge and memory visual guide part 1" />
    <img src="../../../static/llm/visual-guide/images/slices/06-knowledge-base-and-memory/part-2.png" alt="What is knowledge and memory visual guide part 2" />
    <img src="../../../static/llm/visual-guide/images/slices/06-knowledge-base-and-memory/part-3.png" alt="What is knowledge and memory visual guide part 3" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>Key idea</span><p>Separate external knowledge retrieval from internal memory continuity. That distinction changes the architecture you build next.</p></div>
</div>

Knowledge bases and memory are often mentioned together, but they are not the same thing.

A practical distinction is:

- <strong>Knowledge base</strong>: more like an external reference layer—documents, files, manuals, FAQs, business materials, and retrieval systems.
- <strong>Memory</strong>: more like the system’s own persistent state—user preferences, task progress, dialogue history, and accumulated summaries.

They both try to solve the same broad problem: do not force the model to restart from empty context every time.

That matters because real work rarely happens in one prompt:

- users have preferences that should persist,
- tasks have history that should carry over,
- external knowledge is too large to stuff directly into prompts,
- successful patterns should be remembered instead of rediscovered.

A more advanced way to think about the layer is through two types of persistence:

- <strong>knowledge persistence</strong>: documents, product notes, case studies, and FAQ retrieval,
- <strong>state persistence</strong>: history, identity, task status, and experience summaries.

This is why the hardest design question is often not retrieval quality itself, but governance: what should the system remember, what should it forget, and when should that memory be retrieved?

<div class="llm-visual-guide__insight">
  <strong>Takeaway:</strong> Knowledge and memory are not optional extras. They are the layer that turns AI from a one-shot responder into a system that can collaborate over time.</div>

</section>

<section id="compare" class="llm-visual-guide__section">

## 07 GPT vs Claude vs Gemini: how to think about the differences

<div class="llm-visual-guide__figure llm-visual-guide__figure--portrait">
  <div class="llm-visual-guide__figure-top">
    <button class="llm-visual-guide__figure-link" type="button" @click="openPreview(6)">View full image</button>
  </div>
  <div class="llm-visual-guide__figure-stack llm-visual-guide__figure-stack--interactive" role="button" tabindex="0" @click="openPreview(6)" @keydown.enter.prevent="openPreview(6)" @keydown.space.prevent="openPreview(6)">
    <img src="../../../static/llm/visual-guide/images/slices/07-gpt-vs-claude-vs-gemini/part-1.png" alt="GPT Claude Gemini comparison visual guide part 1" />
    <img src="../../../static/llm/visual-guide/images/slices/07-gpt-vs-claude-vs-gemini/part-2.png" alt="GPT Claude Gemini comparison visual guide part 2" />
    <img src="../../../static/llm/visual-guide/images/slices/07-gpt-vs-claude-vs-gemini/part-3.png" alt="GPT Claude Gemini comparison visual guide part 3" />
  </div>
  <div class="llm-visual-guide__figure-caption"><span>Key idea</span><p>Do not compare only benchmark scores. Compare style, cost, context stability, and ecosystem fit for the work you actually need to do.</p></div>
</div>

Once the earlier layers are clear, model comparison becomes much less naive. The real question is not “Which model is universally strongest?” but “Which model best fits the system and tasks I am building?”

More useful dimensions include:

- <strong>conversation and writing style</strong>: fluency, tone, summarization quality, and long-form clarity,
- <strong>code and tool-use fit</strong>: structured outputs, function calling, and engineering tasks,
- <strong>context behavior</strong>: stability over long contexts, drift, and summarization quality,
- <strong>ecosystem integration</strong>: how each vendor connects to IDEs, office workflows, enterprise systems, or multimodal pipelines.

For an individual assistant, you may care most about responsiveness, cost, and writing feel. For enterprise systems, you may care more about permissions, system fit, stability, and integration.

That is why the stronger question is not “Who wins?” but:

- What kind of work dominates my workload?
- What cost and latency constraints do I actually have?
- Am I building a personal assistant or a multi-user product?
- What kind of surrounding system—chat UI, IDE, workflow platform, business app—will the model live inside?

<div class="llm-visual-guide__insight">
  <strong>Takeaway:</strong> The goal of model comparison is not to find a permanent winner. It is to find the best match for your task shape, system structure, and constraints.</div>

</section>

## Finally, reconnect the whole chain

<div class="llm-visual-guide__summary-grid">
  <div>
    <strong>Model</strong>
    <p>Determines whether the system can understand, reason, and generate useful outputs.</p>
  </div>
  <div>
    <strong>Agent</strong>
    <p>Determines whether the system can act around a goal, use tools, and finish work.</p>
  </div>
  <div>
    <strong>MCP</strong>
    <p>Determines how external tools become discoverable, callable, and governable.</p>
  </div>
  <div>
    <strong>Workflow</strong>
    <p>Determines whether repeated work becomes stable, auditable, and reusable.</p>
  </div>
  <div>
    <strong>Knowledge / Memory</strong>
    <p>Determines whether context, materials, and experience survive across tasks and time.</p>
  </div>
  <div>
    <strong>Model choice</strong>
    <p>Determines how you trade off style, speed, cost, stability, and ecosystem fit.</p>
  </div>
</div>

The goal of this page is not to replace deeper chapters. It is to make the map visible first. Once the map is clear, the deeper technical readings become far easier to organize in your head.

Recommended next steps:

1. [Chapter 1: Function Calling, MCP, ReAct, and Skills](../chapter1/)
2. [Chapter 2: Hermes-Agent Self-Learning Skill Mechanism](../chapter2/)
3. [AI Agent Chapter 6: MCP vs CLI](../../agent/chapter6/)

<transition name="llm-preview-fade">
  <div v-if="isPreviewOpen" class="llm-visual-guide__preview" @click="closePreview">
    <div class="llm-visual-guide__preview-dialog" @click.stop>
      <div class="llm-visual-guide__preview-topbar">
        <div>
          <div class="llm-visual-guide__preview-eyebrow">Current image preview</div>
          <div class="llm-visual-guide__preview-title">{{ currentPreview.title }}</div>
        </div>
        <div class="llm-visual-guide__preview-actions">
          <div class="llm-visual-guide__preview-zoom">
            <button class="llm-visual-guide__preview-zoom-btn" type="button" @click="zoomOut">-</button>
            <span class="llm-visual-guide__preview-zoom-label">{{ previewScaleText }}</span>
            <button class="llm-visual-guide__preview-zoom-btn" type="button" @click="zoomIn">+</button>
            <button class="llm-visual-guide__preview-zoom-reset" type="button" @click="resetPreviewViewport">Reset</button>
          </div>
          <button class="llm-visual-guide__preview-close" type="button" @click="closePreview">Close</button>
        </div>
      </div>
      <div ref="previewStageRef" class="llm-visual-guide__preview-stage" @wheel="onPreviewWheel">
        <button class="llm-visual-guide__preview-nav llm-visual-guide__preview-nav--prev" type="button" @click="showPrev">Prev</button>
        <div class="llm-visual-guide__preview-canvas" :style="previewCanvasStyle">
          <img class="llm-visual-guide__preview-image" :src="currentPreview.src" :alt="currentPreview.title" @dblclick="onPreviewImageDblclick" />
        </div>
        <button class="llm-visual-guide__preview-nav llm-visual-guide__preview-nav--next" type="button" @click="showNext">Next</button>
      </div>
      <div class="llm-visual-guide__preview-footer">
        <span>{{ currentPreviewIndex + 1 }} / {{ previewImages.length }}</span>
        <span>Starts at a reader-friendly width; use the zoom buttons, double-click to zoom/reset, or Ctrl / Command + mouse wheel to zoom</span>
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
  color: var(--llm-guide-ink);
  font-size: 16px;
  line-height: 1.9;
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
.llm-visual-guide__toc,
.llm-visual-guide__summary-grid,
.llm-visual-guide__path-grid {
  display: grid;
  gap: 12px;
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
  background: #fffdf5;
  border-radius: 0 14px 14px 0;
}

.llm-visual-guide__lead p {
  margin: 0;
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
  background: #fff;
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
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98) 0%, rgba(247, 251, 255, 0.98) 100%);
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
  background: #fff;
  box-shadow: 0 8px 20px rgba(25, 48, 71, 0.05);
}

.llm-visual-guide__relation-card--memory {
  grid-column: 1 / -1;
  background: linear-gradient(180deg, #ffffff 0%, #f5faf7 100%);
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
  background: linear-gradient(180deg, #fffdf9 0%, #fff8ef 100%);
  border: 1px solid rgba(240, 211, 167, 0.72);
  color: #6b7280;
  line-height: 1.75;
}

.llm-visual-guide__figure-caption span {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 999px;
  background: #ffe7bf;
  color: #9a5c00;
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
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
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
  width: min(1380px, calc(100vw - 32px));
  height: calc(100vh - 32px);
  padding: 18px;
  border-radius: 24px;
  background: rgba(250, 252, 255, 0.96);
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.28);
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  gap: 12px;
}

.llm-visual-guide__preview-topbar,
.llm-visual-guide__preview-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.llm-visual-guide__preview-actions,
.llm-visual-guide__preview-zoom {
  display: flex;
  align-items: center;
  gap: 10px;
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

.llm-visual-guide__preview-close,
.llm-visual-guide__preview-nav,
.llm-visual-guide__preview-zoom-btn,
.llm-visual-guide__preview-zoom-reset {
  border: 0;
  cursor: pointer;
  font-family: inherit;
}

.llm-visual-guide__preview-close {
  padding: 10px 16px;
  border-radius: 999px;
  background: #eaf2ff;
  color: var(--llm-guide-accent);
  font-weight: 700;
}

.llm-visual-guide__preview-zoom {
  padding: 6px;
  border-radius: 999px;
  background: rgba(234, 242, 255, 0.92);
}

.llm-visual-guide__preview-zoom-btn,
.llm-visual-guide__preview-zoom-reset {
  padding: 8px 12px;
  border-radius: 999px;
  background: #fff;
  color: var(--llm-guide-accent);
  font-weight: 700;
  box-shadow: 0 8px 18px rgba(31, 41, 55, 0.08);
}

.llm-visual-guide__preview-zoom-btn {
  min-width: 38px;
}

.llm-visual-guide__preview-zoom-label {
  min-width: 56px;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--llm-guide-ink);
}

.llm-visual-guide__preview-stage {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 0;
  overflow: auto;
  padding: 18px 72px 24px;
  border-radius: 22px;
  background:
    linear-gradient(180deg, rgba(250, 242, 228, 0.92) 0%, rgba(255, 250, 242, 0.92) 100%);
  border: 1px solid rgba(233, 219, 197, 0.88);
  scroll-behavior: smooth;
}

.llm-visual-guide__preview-canvas {
  flex: 0 0 auto;
  max-width: none;
  transition: width 0.18s ease;
}

.llm-visual-guide__preview-image {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 18px;
  padding: 6px;
  background: #fff;
  box-shadow: 0 20px 42px rgba(31, 41, 55, 0.14);
}

.llm-visual-guide__preview-nav {
  position: absolute;
  top: 22px;
  z-index: 2;
  width: 54px;
  height: 54px;
  border-radius: 999px;
  background: #ffffff;
  color: var(--llm-guide-accent);
  font-size: 0.82rem;
  font-weight: 700;
  box-shadow: 0 10px 22px rgba(31, 41, 55, 0.12);
}

.llm-visual-guide__preview-nav--prev {
  left: 12px;
}

.llm-visual-guide__preview-nav--next {
  right: 12px;
}

.llm-visual-guide__preview-footer {
  color: var(--llm-guide-muted);
  font-size: 0.88rem;
}

@media (max-width: 640px) {
  .llm-visual-guide__hero {
    padding: 22px 18px 20px;
    border-radius: 18px;
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

  .llm-visual-guide__preview-topbar,
  .llm-visual-guide__preview-footer {
    flex-direction: column;
    align-items: flex-start;
  }

  .llm-visual-guide__preview-actions {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .llm-visual-guide__preview-zoom {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
  }

  .llm-visual-guide__preview-stage {
    padding: 12px 12px 16px;
  }

  .llm-visual-guide__preview-nav {
    width: 100%;
    height: 44px;
    position: static;
  }

  .llm-visual-guide__preview-image {
    width: 100%;
    padding: 8px;
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
  .llm-visual-guide__path-card,
  .llm-visual-guide__lead,
  .llm-visual-guide__toc a,
  .llm-visual-guide__summary-grid div {
    border-radius: 16px;
  }
}
</style>
