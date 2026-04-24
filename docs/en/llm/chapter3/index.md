---
title: "Chapter 3: Harness Engineering from Prompt / Context to Runtime Control"
---

# A Clear Guide to the Fast-Rising AI Concept: Harness Engineering

In this chapter, I will explain the new concept of Harness from three angles:

![Image](../../../static/llm/chapter3/images/img01.jpeg)

- **The evolution of Harness**: how the center of gravity in AI engineering moved from Prompt Engineering, to Context Engineering, and then to Harness Engineering.
- **The structure of Harness**: what a mature Harness is made of, and what problem each layer solves.
- **Harness in practice**: how leading companies such as OpenAI and Anthropic apply Harness in real products, and why those practices work.

## I. The Evolution of Harness

Over the last two years, AI engineering has gone through three clear shifts in focus.

On the surface, this just looks like a change in terminology: `Prompt Engineering`, `Context Engineering`, and `Harness Engineering`.

But if you step back and look at the timeline, you will notice that these names correspond to three increasingly fundamental questions:

- Can the model understand what you are asking?
- Has the model received enough of the right information?
- Can the model keep doing the right thing throughout real execution?

So understanding these three shifts is not just about learning new terms. It is about understanding how AI systems move step by step from "being able to chat" to "being able to deliver work."

### 1.1 Prompt Engineering

When large models first exploded into public awareness, many people had an experience that felt almost magical:

The same model could produce dramatically different results depending on how you phrased the request. If you said:

> "Help me summarize this article."

the model might give you a generic overview. But if you changed the prompt to:

> "Please act as a senior technical editor. Summarize this article in three sections: first the core idea, then the argument structure, then the limitations. Keep each section under 150 Chinese characters."

the result was often obviously better. That was the original appeal of Prompt Engineering.

Its core idea was simple: **the model is not necessarily incapable; the real issue may be that you have not described the problem clearly enough. Since the model is sensitive to the form of the input, the first step in engineering optimization is naturally to optimize the instruction itself.**

As a result, a whole toolkit quickly became popular:

![Image](../../../static/llm/chapter3/images/img02.png)

- **Role assignment**: first tell the model who it is. The point is not cosplay; the point is to constrain the professional angle from which it should respond.
- **Style constraints**: tell the model how to speak. This does not primarily solve correctness; it solves whether the answer sounds like what you want.
- **Few-shot examples**: give examples instead of only abstract rules. In many cases the model is not bad at following rules; it is simply better at imitating patterns.
- **Step-by-step guidance**: do not let it jump straight to the answer. Ask it to break down the problem, think, and then answer. This reduces snap judgments.
- **Format constraints**: define what the output should look like in advance. This improves usability rather than intelligence.
- **Refusal boundaries**: draw red lines before the model answers. The goal is to reduce the risk of confident nonsense.

At that stage, prompts felt like a universal key.

Many teams sincerely believed that as long as prompts were polished enough, models would become more stable and more useful.

That belief was not irrational.

Because at that stage, Prompt Engineering really did solve the most direct problem: **how to map human intent more accurately into model behavior.**

#### 1.1.1 Why Prompt Engineering worked

Because a large model is, at its core, a probabilistic generation system that is extremely sensitive to context. It is not really a command line. It behaves more like a temporary cognitive field that gets assembled on the fly:

![Image](../../../static/llm/chapter3/images/img03.png)

- If you assign it a role, it samples along the probability distribution associated with that role.
- If you give it examples, it continues along the pattern those examples establish.
- If you emphasize certain constraints, it is more likely to treat them as high-weight signals.

So the essence of Prompt Engineering is not "issuing commands." It is **shaping a local probability space**.

At this stage, the most important engineering skill was not system design but language design.

The better you understood the temperament of the model, the easier it was to produce results that looked more intelligent.

#### 1.1.2 The ceiling of Prompt Engineering

The problem with prompts is that many tasks are not solved by "explaining clearly." They are solved by "actually knowing the facts." For example, suppose you ask the model to:

- analyze an internal company document
- answer questions about a product's latest configuration
- generate code against a long specification
- complete a complex task across multiple tools

At that point, you discover that no matter how elegant the prompt is, it cannot replace the facts themselves.

Prompting is good at: **clarifying the task, constraining the output, and activating abilities the model already has.**

But it is not good at: **fabricating missing knowledge, managing large amounts of dynamic information, or handling shifting state across long task chains.**

Put more directly:

Prompt solves an **expression problem**, not an **information problem**.

Once work moves from open-ended Q&A into real business scenarios, the engineering focus naturally starts to shift.

People gradually realize that when the model performs badly, the issue is not always that you asked badly. It may be that you never gave it the material it needed in the first place.

The core question changes from "how should I say it?" to "what should I provide?"

That is when the second shift begins.

### 1.2 Context Engineering

If the default assumption of Prompt Engineering is that the model already knows and only needs the right question, then the default assumption of Context Engineering is different:

The model may not know, so the system must supply the correct information at runtime.

In the prompt era, most people focused on "how to phrase a sentence well." In the context era, the questions become:

- What can the model see right now, and what can it not see?
- Which information should be given early, and which should be delayed?
- Which information should be preserved in full, and which should be summarized or compressed?
- Which information should be visible to the current module, and which should be isolated?

#### 1.2.1 Why Context Engineering emerged

The most important reason is that model usage scenarios changed.

When large models first became popular, the dominant interaction pattern was still chat: the user asks a question, and the model returns an answer.

In that mode, prompts matter a lot because tasks are short, chains are short, state is light, and many issues really can be solved by "stating the request more clearly."

But once Agents started to take off, the situation changed immediately. The model was no longer just answering questions. It was being placed into real execution environments:

- it had to sustain multi-turn conversations, and call tools such as search, browsers, code, and databases
- it had to pass intermediate results between steps, revise plans based on external feedback, and sometimes coordinate with other Agents

At that point, the system is no longer facing the question "Was this single answer correct?" It is facing the question "Can the entire task chain run end to end?"

Take a simple example. If you just ask:

> "Summarize this article for me."

then the model only needs to read the article and generate a summary according to the request.

But if you ask it to do something more realistic, such as:

> "Analyze this requirements document, identify potential risks, combine that with historical review comments, and produce a feedback draft for the product manager."

that is no longer something a single prompt can solve. At minimum, the model needs:

- the current requirements document and historical review records
- relevant standards or best practices, plus the goal of the current task
- intermediate conclusions already formed, the target audience of the output, and the right tone to use

Now a new problem becomes visible: the context window is limited. So the real question becomes:

**Did you give the model the right information, in the right form, at the right time?**

That is the real background behind the rise of Context Engineering.

#### 1.2.2 What Context actually is

When many people hear "context," they think "a few pieces of background text." That is not wrong, but it is far too narrow.

In engineering terms, context is not just supplemental text. It is the full set of information that can affect the model's current decision. That usually includes:

![Image](../../../static/llm/chapter3/images/img04.png)

- the current user input and the full dialogue history
- results from external retrieval and tool calls
- the current task state, working memory, and intermediate artifacts
- system rules, safety constraints, and structured outputs passed from other Agents

So the prompt is only one part of context, not the whole thing.

That is why many people have a strong intuition that **the same model with the same prompt can behave completely differently in different systems.**

The reason is often not the model, and not the prompt, but the fact that the context supply mechanism behind those systems is fundamentally different.

#### 1.2.3 Typical practices in Context Engineering

The most representative early example of Context Engineering was RAG.

RAG matters because it answered a very practical question:

**If the knowledge is not in the model parameters, how do you inject it at runtime?**

The basic answer is: retrieve relevant material from an external knowledge base, then place that material into the current context so the model can continue generating on top of it.

So RAG is important because it was the first mechanism that turned "what if the model doesn't know?" into an engineering pattern that can actually be deployed.

![Image](../../../static/llm/chapter3/images/img05.png)

But mature Context Engineering obviously cares about more than just "run a retrieval step." It cares about the whole chain:

- how documents should be chunked so they preserve semantics while remaining easy to recall
- how results should be ranked so the truly important items enter context first
- how long documents should be compressed without blowing up the window
- when dialogue history should stay verbatim and when it should be summarized
- whether raw tool output should be exposed to the model at all
- whether multiple Agents should exchange original text, summaries, or structured fields

So RAG is only the starting point of Context Engineering. There is still a long road ahead in optimizing context itself.

I would argue that the recent explosion of Agent Skills is another very typical practice of Context Engineering.

Once a system starts calling tools, the model no longer faces only the question **"What do I know?"** It also faces **"What am I currently able to do?"**

For example, imagine that you connect more than ten tools to a model and dump all the tool descriptions, parameter schemas, and caveats into the context at once. In theory the model now "knows more" about what it can do.

But in practice, things often become worse: token costs explode, attention gets diluted, and even simple tasks require the model to carry around a pile of irrelevant capabilities.

Skills help here through progressive disclosure:

**Do not show the model every capability and every piece of information upfront. Instead, reveal only the part most relevant to the current task when it is needed.**

That is why a Skill system usually splits capability information into three layers:

![Image](../../../static/llm/chapter3/images/img06.jpeg)

- the metadata layer (`~50` tokens): only the skill name, trigger conditions, and a short overview; loaded globally at startup
- the instruction layer (`~500` tokens): the SOP plus input/output conventions; loaded only when the skill is triggered
- the resource layer (loaded on demand): scripts, templates, API docs, and similar assets; loaded only when a concrete execution step needs them

This mechanism can improve context efficiency by multiples in complex Agent scenarios.

#### 1.2.4 The limits of Context Engineering

By this point, many systems are already much stronger than they were in the pure prompt era.

The model gets better information, and it can handle more complex tasks.

But a new problem appears: even if the information is correct, the model still may not execute correctly in a stable way. It may:

- make a good plan but drift in execution
- call a tool but misunderstand the result
- make one mistake in the middle and then continue down the wrong path
- look confident on the surface while the real task state has already drifted
- slowly go off course over a long chain without anyone noticing

At that point, you realize that both Prompt and Context mainly operate on the **input side**:

- Prompt optimizes intent expression
- Context optimizes information supply

But real-world complex tasks raise a harder question:

**Once the model starts acting continuously, who keeps supervising it, constraining it, and correcting it?**

That is where the third shift begins.

### 1.3 Harness Engineering

The word *harness* originally means a bridle, tack, or restraining system.

![Image](../../../static/llm/chapter3/images/img07.png)

Inside AI systems, it is not just a flashy new label. It is a very direct reminder:

**Once the model moves from "answering questions" to "executing tasks," the system cannot be responsible only for feeding information. It also has to manage and control the process.**

![Image](../../../static/llm/chapter3/images/img08.png)

That is the starting point of Harness Engineering.

If the previous two generations of engineering thought were mostly concerned with making the model "think better," then Harness Engineering is more concerned with **how to keep the model from drifting, keep it stable, and pull it back when it goes wrong.**

#### 1.3.1 A comparison among the three

Take a familiar analogy. Suppose you want a new hire to conduct an important client visit.

**Prompt Engineering**

First, you explain the task clearly:

> "Start with small talk, then introduce the proposal, then ask about their needs, and finally confirm the next step."

That is prompt-level work. The emphasis is on explaining the task clearly.

* * *

**Context Engineering**

Then you prepare all the necessary materials:

> - client background and past communication records  
> - pricing information, competitive context, and the objective of this meeting

That is context-level work. The emphasis is on supplying the right information.

* * *

**Harness Engineering**

But if the meeting is very important, you do not stop there. You also:

> - ask the person to bring a checklist and report key milestones in real time  
> - verify the meeting notes against the recording afterward and correct deviations immediately  
> - accept the result against explicit standards

That is Harness.

At that point the emphasis is no longer just "say it clearly" and "provide the information." The emphasis is on building a continuous mechanism for observation, correction, and acceptance.

#### 1.3.2 The relationship among the three

When new terms appear, people often assume the old ones are obsolete. In fact, the relationship is layered and progressive.

![Image](../../../static/llm/chapter3/images/img09.png)

- **Prompt Engineering** focuses on "How should I speak to the model?" At its core, it optimizes instruction expression inside a single call.
- **Context Engineering** expands the boundary outward. It no longer focuses on the prompt itself, but on what information the model can see at the current moment. So the prompt becomes only one component of context, alongside conversation history, retrieval results, tool outputs, task state, and working memory.
- **Harness Engineering** expands the boundary one layer further. It no longer focuses on whether the inputs are right, but on whether the model is continuously constrained, observed, corrected, and made to converge by a complete system during real execution. In that sense, context becomes only one part of the Harness.

Put differently:

- **Prompt** is the engineering of the instruction.
- **Context** is the engineering of the input environment.
- **Harness** is the engineering of the full runtime control system.

Since each boundary is larger than the last, the later layers naturally contain the earlier ones.

![Image](../../../static/llm/chapter3/images/img10.png)

Many technology trends look like battles of opinion, but in reality they are forced by task complexity:

- when tasks are simple, prompts are enough
- when tasks become complex enough that context becomes the bottleneck, context becomes the center
- when tasks require long-running execution with low tolerance for failure, Harness becomes almost unavoidable

---

## II. What a Harness Is Made Of

### 2.1 What exactly is a Harness?

LangChain engineers use a very typical definition:

> - Agent = Model + Harness  
> - Harness = Agent - Model

In simple terms, the Harness is everything in an Agent environment except the model itself. It determines what the model sees, what it can do, what rules it follows, how it gets corrected when it fails, and how its capabilities are finally delivered in a stable way.

Once you understand this, your view of Agents becomes much clearer:

- Why can the same model perform so differently in different products?
- Why do some Agents feel like interns, while others feel like mature employees?

The upper bound of the model is determined by companies like OpenAI and Anthropic. The Harness is determined by engineers like us.

If you break it apart, a mature Harness usually contains at least the following six core components. This is only my own decomposition, but I think it is a useful one:

![Image](../../../static/llm/chapter3/images/img11.png)

### 2.2 The first layer of Harness: context management

We already discussed context management in the Context Engineering section. Here let us look at it again from the perspective of Harness.

In many tasks, the difference in model performance does not primarily come from the model's own "IQ." It comes from what information the model is allowed to see.

No matter how strong a model is, if the context is messy, incomplete, or overloaded, it will struggle to perform consistently.

So the first responsibility of a Harness is to keep the model thinking within the right information boundary.

That includes several things.

#### 2.2.1 Role and objective definition

The model first needs to know who it is, what the task is, and what success looks like.

Take something as simple as "write an article." Different context can produce completely different outcomes:

- Is it technical education or product marketing?
- Is it written for beginners or for engineers?
- Is the goal virality or rigor?
- Are analogies allowed? Is conversational phrasing allowed?

These are not just details of writing style. They define the task boundary.

The Harness must inject those boundaries explicitly into the model.

#### 2.2.2 Information selection and pruning

Context is not better just because it is larger.

A common problem with large models is not "knowing too little," but "seeing too much irrelevant information."

A good Harness does two things:

- it selects the relevant information
- it blocks the irrelevant information

This is very similar to how a mature engineer handles a requirement:

you do not throw every document at a teammate; you first organize the key background and only then let them enter the problem.

#### 2.2.3 Structured organization of context

The same information can perform very differently depending on whether it is dumped into a pile or arranged in layers. A mature Harness often structures context hierarchically, for example:

![Image](../../../static/llm/chapter3/images/img12.png)

This can greatly reduce the probability that the model misses critical points or forgets constraints.

### 2.3 The second layer of Harness: the tool system

Without tools, a large model is basically still doing text prediction. It can explain, summarize, reason, and rewrite, but it cannot truly touch the world.

Once tools are attached, the situation changes. The model can:

> - search the web for up-to-date information and read long documents  
> - write and execute code, and call databases or business APIs  
> - operate a browser, click pages, generate images, edit files, and send messages

At that point, the model is no longer just "someone who answers questions." It starts becoming "someone who does things."

The role of Harness here is not simply to hang tools onto the model. It is to solve three deeper questions.

![Image](../../../static/llm/chapter3/images/img13.png)

#### 2.3.1 Which tools the model should have

Too few tools means insufficient capability. Too many tools means the model will misuse them.

So tool design is not about "the more complete the better." It should be configured around the task scenario.

A writing Agent and a security analysis Agent should have completely different tool sets.

#### 2.3.2 When the model should call tools

This is even more important than "which tools exist." A poor Agent typically falls into two extremes:

> - it looks things up even when it does not need to  
> - it answers from memory when it should have verified

A good Harness guides the model to judge:

> - Does this question require external information?  
> - Is the current context already enough?  
> - At this step, is it better to search, read, compute, or answer directly?

#### 2.3.3 How tool results are fed back into the model

A tool call does not end when the tool returns. The critical point is:

**How are the returned results understood, filtered, absorbed, and then fed into the next decision?**

If a search returns ten results, you should not dump all ten back into the model verbatim.

The Harness has to help the model extract useful evidence and preserve the relevance of the results to the task.

### 2.4 The third layer of Harness: execution orchestration

Even with context and tools, an Agent is still not mature enough.

Because it still needs one more ability: knowing what to do next. That is execution orchestration.

![Image](../../../static/llm/chapter3/images/img14.png)

Many failing Agents do not fail because they cannot do any individual step. They fail because they cannot chain steps together.

They may be able to search, summarize, and write code, but the whole process looks like they are improvising at every step, and the final output is just a pile of half-finished fragments.

Execution orchestration solves exactly this problem. A full task usually gets decomposed into a process like this:

> 1. Understand the objective  
> 2. Decide whether the information is sufficient  
> 3. Retrieve external information when necessary  
> 4. Continue analysis based on the result  
> 5. Generate an output  
> 6. Check whether the output satisfies the requirement  
> 7. If not, revise or retry

You can see that this is already very close to how humans work.

The difference is that people rely on experience and habit to complete this process, while Agents need the Harness to lay down the rails explicitly.

That is why a mature Harness usually includes much more than "the ability to call tools." It has clearly defined:

> - step boundaries  
> - decision points  
> - intermediate artifacts  
> - termination conditions  
> - exception-handling logic

* * *

### 2.5 The fourth layer of Harness: state and memory

Many people expect an Agent to "work continuously like a person."

If that is the goal, then the system must have state.

A stateless system behaves as if it has amnesia every round.

It does not know what it just did, which conclusions have already been established, or which issues are still unresolved.

That is why state management is such an important part of Harness.

At minimum, it has to answer three questions:

![Image](../../../static/llm/chapter3/images/img15.png)

**Question 1: Which step is the current task at?** For example:

> - information gathering is complete and the outline is being written  
> - a first draft has been generated and is awaiting validation, or a tool call failed and needs a retry

This prevents the system from bouncing around repeatedly.

**Question 2: Which intermediate results should be preserved?**

Not all information should be stored as long-term memory.

But in a complex task, intermediate state must be preserved. Otherwise the system cannot progress continuously. For example:

> - confirmed requirement constraints and important conclusions  
> - filtered source materials and completed subtasks

**Question 3: Which information should become long-term memory?**

This is usually things like user preferences, stable rules, and long-lived project background.

For example, preferred writing style, fixed terminology for a project, or frequently used output templates. So memory is not a case of "the more the better." You have to distinguish among:

> - temporary state  
> - session memory  
> - long-term preference

If those are all mixed together, the system gets messier over time. If they are separated clearly, the Agent becomes more like a reliable collaborator.

### 2.6 The fifth layer of Harness: evaluation and observability

Many systems do not fail because they cannot produce an output. They fail because after producing it, they have no idea whether it is actually good.

Without independent evaluation and observability, an Agent easily remains trapped in a state of "feeling good about itself."

![Image](../../../static/llm/chapter3/images/img16.png)

This layer typically includes:

> - output acceptance: does the result satisfy the task requirement?  
> - environment verification: does it really run, click, or interact correctly?  
> - automated testing: code, interfaces, pages, document format, and so on  
> - process observability: logs, metrics, traces, and retry records  
> - quality attribution: is the problem caused by the model, the context, the tools, or the workflow design?

### 2.7 The sixth layer of Harness: constraints, validation, and failure recovery

What really turns a system from "able to run" into "able to launch" is often not the main path, but the exception path. In the real world, failure is the norm:

- search results are inaccurate, APIs time out
- document formats are messy, the model misunderstands instructions
- outputs violate constraints, tool permissions are missing

Without a recovery mechanism, every time the Agent fails it can only "start over from scratch."

So the final layer of Harness is the part that controls system stability:

![Image](../../../static/llm/chapter3/images/img17.png)

1. **Constraints**: limit what the model can and cannot do. For example, which tools are allowed, which scenarios require verification, and which content touches safety boundaries.
2. **Validation**: check before final output. For example, did it answer the user's question, did it miss key requirements, and does it satisfy the format spec?
3. **Recovery**: when one step fails, analyze the cause, retry the same step, switch to a fallback path, or roll back to the previous stable state.

This layer most closely resembles robustness design in traditional software engineering.

* * *

Of course, everything above is still mostly my own decomposition of Harness at the principle level.

The companies that have really taken this concept seriously, grounded it, and turned it into methodology are leading organizations such as OpenAI and Anthropic.

They are not stopping at the question "How do we make the model sound smarter?" They are trying to answer a more important question:

How do we place the model into a system that can run continuously, deliver repeatedly, and evolve over the long term?

That brings us to the most cutting-edge industry practices around Harness today.

* * *

---

## III. Harness in Practice

Recently, major leading companies have been publishing their engineering practices around Harness in their own products. Let us look at a few typical examples.

![OpenAI: Harness engineering: leveraging Codex in an agent-first world](../../../static/llm/chapter3/images/img18.png)

OpenAI used a team with only a few human engineers and Codex-based agents to build a production application with more than one million lines of code from scratch. Business logic, CI/CD configuration, the observability stack, and internal documentation were all written by agents, and the total time cost was only about one tenth of manual development.

![Anthropic: Harness design for long-running application development](../../../static/llm/chapter3/images/img19.png)

Anthropic built a long-running autonomous coding system. Starting from only a natural-language request, Claude can run continuously for hours without human intervention and deliver end-to-end artifacts such as a 2D game-making tool with a level editor and physics engine, or a digital audio workstation that runs in the browser.

![LangChain: Improving Deep Agents with harness engineering](../../../static/llm/chapter3/images/img20.png)

LangChain improved its own coding agent's Terminal Bench 2.0 score from `52.8` to `66.5` without changing the underlying model at all. The gain came purely from refactoring and iterating on the Harness, which moved the system from outside the top 30 directly into the top 5.

So why can carefully designed Harness systems produce such dramatic quality jumps even when they are built on top of the same model APIs?

Let us look more closely at what these companies are actually doing.

### 3.1 Anthropic's practice

#### 3.1.1 Two typical failure modes

Anthropic highlights two typical failure patterns that appeared repeatedly in practice:

![Image](../../../static/llm/chapter3/images/img21.png)

- The first is **context anxiety**. As the task gets longer and the context window fills up, the model starts dropping details and missing important points. An interesting effect appears near the edge of the window: the model seems to become "anxious" and wants to wrap up prematurely, as if it knows it is about to run out of room.
- The second is **distorted self-evaluation**. After the model finishes work, if you ask it to judge the quality of its own output, it tends to be too optimistic. This bias is especially obvious in areas like design, user experience, and product completeness, where there is no hard binary answer.

#### 3.1.2 Practice one: context reset

To address the first problem, many systems use Context Compaction after the context grows too long: summarize the previous history, compress it, and continue.

Anthropic's approach is different. They advocate Context Reset, and the distinction between the two is quite clear:

![Image](../../../static/llm/chapter3/images/img22.png)

- **Compaction**: the same Agent continues. The history becomes shorter, but its internal "mental state" and sense of what it is doing are still being carried forward.
- **Reset**: you replace it with a fresh Agent in a clean context, but you have to hand the work off clearly between the two model instances.

Anthropic found that for some models, such as Claude Sonnet 4.5, compression alone does not solve the problem of context anxiety. A real reset creates the effect of "clearing the baggage and starting fresh."

This insight is very similar to process restart and state recovery in traditional engineering: not every memory leak can be solved by "cleaning the cache." Sometimes you really do need to restart the process.

#### 3.1.3 Practice two: introduce an evaluator

Anthropic is very direct about this: when a model evaluates the quality of its own output, it often "confidently praises itself," even if a human observer would judge the result as mediocre.

So they use a very typical and very effective Harness technique: separate the worker from the scorer.

That becomes the core pattern: `generator + evaluator`, later extended into `planner + generator + evaluator`.

This design matters because behind it is a simple but very hard-edged engineering principle:

**Production and acceptance must be separated.**

In Anthropic's implementation:

![Image](../../../static/llm/chapter3/images/img23.png)

> - **Planner**: expands a short request into a full product specification  
> - **Generator**: implements step by step  
> - **Evaluator**: behaves like QA, using browsers and tools to operate the application for real and inspect functionality, design, and code quality

One especially important detail is that the Evaluator is not merely "reading code and scoring it." It actually interacts with the page, exercises the flow, and inspects the result.

That means it is not abstract review. It is environment-backed verification.

Once the Evaluator can test independently, inspect quality independently, and maintain fairness, the whole system can enter a real engineering loop of "generate -> inspect -> repair."

### 3.2 OpenAI's practice

#### 3.2.1 Redefining what an "engineer" is

From day one, this team adopted a hard rule: humans do not write the code; humans design the environment.

As a result, the engineer's core work becomes three things:

![Image](../../../static/llm/chapter3/images/img24.png)

- decompose intent: break product goals into smaller tasks the Agent can understand
- fill capability gaps: when the Agent fails, do not ask it to "try harder"; ask what is missing in the environment that caused the failure, then add that missing capability
- build feedback loops: let the Agent see the result of its own work instead of operating blindly

In their own words:

**When something goes wrong, the fix is almost never "work harder." It is "what structural capability is missing?"**

#### 3.2.2 Progressive disclosure

Early on, they made a classic mistake: they wrote a giant `AGENTS.md` file and dumped every rule, architecture note, and convention into it at once.

The result was that the Agent got more confused, not less. Context windows are scarce resources. If you stuff them too full, it is almost equivalent to saying nothing.

Their eventual solution was much cleaner:

`AGENTS.md` contains only around one hundred lines and serves as a directory page pointing to more detailed documents elsewhere in the repository.

```text
AGENTS.md          <- entry point, only pointers
ARCHITECTURE.md    <- architectural overview
docs/
├── design-docs/   <- design documents (with validation status)
├── exec-plans/    <- execution plans (active / done / tech debt)
├── product-specs/ <- product specifications
├── references/    <- third-party references
├── QUALITY_SCORE.md
└── SECURITY.md
```

Does that pattern feel familiar? It is exactly the core mechanism of Skills: progressive disclosure.

The Agent first sees the directory. When it needs more detail, it follows the pointer into the corresponding document.

Even more importantly, OpenAI uses CI to automatically validate document freshness and cross-references.

They also have a dedicated "document gardener" Agent that regularly scans for stale documents and opens PRs to repair them. Knowledge management itself becomes automated.

#### 3.2.3 Letting the Agent "see" the whole application

Once code generation became fast, the bottleneck shifted from "writing" to "verifying." Humans simply could not keep up with the volume.

OpenAI's solution was: let the Agent verify its own work.

![Image](../../../static/llm/chapter3/images/img25.png)

What did that lead to?

Single Codex runs could often keep working for more than six hours straight, usually while the humans were asleep.

The Agent ran the app, found bugs, fixed them, verified the fixes, and opened the PR itself.

#### 3.2.4 Writing architectural constraints into the system

If human code review bandwidth cannot keep up with Agent output speed, how do you guarantee code quality?

OpenAI's answer is to turn the judgment of senior programmers into executable machine-checkable rules.

Their practice is very typical: instead of expecting engineers to keep reminding the Agent that "this layer should not depend on that layer" or "this module should not be implemented this way," they write those rules directly into the engineering system.

For example, they organize business code into fixed layers such as:

> - Types  
> - Config  
> - Repo  
> - Service  
> - Runtime  
> - UI

More importantly, those checks do not only report errors. They also tell the Agent how to fix them.

That means the check result itself contains repair guidance, so it can flow directly back into the context and drive the next round of edits.

As a result, code quality is no longer protected mainly by human attention. It is protected by a rule system that can be executed repeatedly.

To humans, some of these rules may feel overly detailed.

But to an Agent, they are extremely important.

Once the Agent is submitting at high frequency, small problems spread quickly if they are not blocked early.

And OpenAI goes beyond gatekeeping at submit time. They also run background Agents that continuously scan the codebase to see where it is starting to drift away from the intended principles:

> - inspect which modules are becoming messy  
> - assign quality scores to different areas  
> - identify parts worth refactoring  
> - directly open repair or refactor PRs

That turns architecture governance from a manual review activity into a continuously running system.

Its value is not only to discover problems, but to repair them while they are still small.

### 3.3 Looking back, everyone is really doing the same thing

If you place the examples above back into the Harness framework, you notice something interesting: OpenAI and Anthropic appear to take different paths and use different methods, but at the level of system substance they are filling in the same set of capabilities:

> - What exactly should the model see?  
> - What exactly should the model be able to do?  
> - What should the model do next?  
> - How does the system keep working continuously?  
> - How does the system know whether it is doing the right thing?  
> - How does the system pull itself back when it makes a mistake?

- What Anthropic is solving are two core problems in long-running tasks: once context gets too long, the model becomes chaotic; and if the model only evaluates itself, quality gets distorted. So by combining Context Reset with an independent Evaluator, they are effectively strengthening context management, execution orchestration, and evaluation plus observability.
- OpenAI goes one step further. They are no longer primarily concerned with "Can the Agent write code?" They are concerned with: how do we let the Agent work stably and continuously inside a real engineering environment? That is why they use progressive disclosure so the Agent is not drowned in information, give it browsers, logs, metrics, and isolated environments so it can validate results itself, and write architectural rules directly into the system so quality control shifts from "humans watching" to "rules guarding." In Harness terms, that maps directly onto context management, the tool system, evaluation and observability, and constraints plus recovery.

At that point, the meaning of Harness should be very clear:

**It is the process of turning the model from a probability machine that answers questions into an engineering system that can complete tasks reliably.**

That is also why the same model can perform so differently in different products.

The difference is often not just the model parameters themselves. The difference is whether the engineering team has actually built the Harness.

---

## Final Thoughts

Looking back at these three stages, you can see that none of them replaced the previous one. Instead, AI engineering keeps pushing its center of gravity outward as tasks become more complex.

When the task is still just single-turn generation, Prompt Engineering matters because the first problem is still "Was the task expressed clearly enough?"

When the task begins depending on external knowledge, historical state, and runtime information, Context Engineering becomes the key.

And when the model truly enters a real environment with long chains, execution, and low tolerance for error, Harness Engineering becomes almost inevitable, because the system has to answer the hardest question of all: the model must not only be able to think, it must also be organized, constrained, validated, and corrected in a stable way.

So Prompt has not become outdated, and Context is not the final destination. Both still matter, and both remain essential.

But the further you go, the more you realize that the upper bound of an AI product may be determined by the model itself.

Yet whether that product can actually land, operate stably, and deliver repeatedly is often determined by the Harness.

Put differently, the future competition in AI engineering may not only be about "who connected the stronger model." It may be even more about who built a mature operating system around the model earlier:

**a system that knows what the model should see, what it is allowed to do, how its results should be accepted, and how to pull it back onto the right track when it fails.**

In that sense, Harness Engineering is not old wine in a new bottle.

It is more like a signal:

**The core challenge of shipping AI is moving from "making the model look smart" to "making the model work reliably in the real world."**
