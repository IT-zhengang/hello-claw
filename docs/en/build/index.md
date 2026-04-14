# Build: Opening the Hood

> **Goal of this section:** Level up from "driver" to "engineer" — understand OpenClaw's internal mechanisms and gain the ability to customize Skills, connect new channels, and optimize architecture.

---

In early 2026, as OpenClaw rapidly climbed the GitHub trending charts, most people saw it as a useful tool. But behind that, there's a more significant trend worth noting: **AI Agents are evolving from "black-box products" into "understandable, modifiable, and rebuildable infrastructure"**.

In Part One, you learned to "drive" — install, configure, use Skills, connect mobile clients. That practical skill is enough to boost your daily productivity by an order of magnitude.

But imagine this scenario:

```text
You: Help me organize the important emails from the past week into a weekly report
OpenClaw: Sure, reading emails... Strange, some emails aren't showing up in the results
You: (confused) Why? Did I use the wrong search terms, or did it miss something?
```

As a driver, you can only try again or rephrase the request. But if you understand how the engine works, you can pinpoint the problem:

- Are the file-matching arguments in the `exec` command incorrect?
- Is the `read` tool's file scope not comprehensive enough?
- Or did the LLM compress away important content during summarization?

**This is the starting point of Part Two: from "try again" to "I know why".**

---

## 1 Why: Understanding the Underlying System

### 1.1 Solving Those "Hard to Explain" Problems

When using AI tools, what's most frustrating isn't "it did something wrong" — it's "I don't know why it went wrong."

Let's look at a few real scenarios:

<details>
<summary>Scenario 1: Memory Loss</summary>

A week ago you told OpenClaw: "I prefer Tab indentation over spaces." Today it generated code using 4 spaces again.

As a user, you can only correct it again. But if you understand its memory system, you'll know:

- User preferences are stored in `MEMORY.md`
- That file has a size limit and old content gets compressed
- More likely, your preference was only treated as "conversation history"
- The solution is to explicitly write coding standards into `AGENTS.md`

</details>

<details>
<summary>Scenario 2: Wrong Tool Selection</summary>

You asked OpenClaw to analyze the project's code structure, but it used the `exec` tool to call `find` with unreasonable arguments, causing it to miss key files.

After understanding the tool system, you'll discover:

- The quality of a tool's description directly affects the LLM's selection
- OpenClaw's prompt may lack specific guidance on best practices for file searching
- You can optimize tool descriptions by modifying `TOOLS.md` to help the LLM make better choices

</details>

<details>
<summary>Scenario 3: Slow Response</summary>

A simple file query takes over ten seconds.

After understanding the architecture, you can identify:

- Is it network latency between the Gateway and the model service?
- Is the LLM's inference time too long?
- Or is the message waiting in a queue?
- You can use `openclaw logs` to see exactly which step is taking time

</details>

**What these problems have in common is: on the surface it looks like "the AI isn't behaving," but in reality it's "some component's configuration or design doesn't meet expectations."** When you understand the underlying mechanisms, diagnosis time drops from hours to minutes.

### 1.2 Mastering the "Meta-Skill" of the AI Era

Let's be honest: OpenClaw won't always be the best AI Agent tool.

Looking back at AI's development: 2023 was the breakout year for AutoGPT, and 2024–2025 saw a flood of Agent frameworks emerging. The pace of technology iteration far outstrips anyone's learning speed.

But some concepts are cross-framework and timeless:

| Concept | In OpenClaw | In Other Frameworks |
|---------|-------------|---------------------|
| **Agent Runtime** | Gateway → Agent Runtime → Clients/Nodes architecture | LangChain's Chains, AutoGPT's Executor |
| **Agent Loop** | Receive → context assembly → model inference → tool execution → reply | The core paradigm of almost every Agent |
| **Layered Memory** | SOUL.md (identity) + MEMORY.md (facts) + conversation history | Vector DB + cache + context window management |
| **Tool Abstraction** | read/exec/edit/write core tools | Function Calling, Tool Use, Plugin systems |
| **Multi-Channel Access** | Telegram/Discord/Slack adapters | Unified Channel Interface |

**What Part Two gives you are concrete implementation examples of these foundational concepts.**

When you understand OpenClaw's ReAct loop implementation, you'll have an "aha moment" looking at LangGraph's node design: "Oh, this is just making each phase of the loop an explicit graph node." When you understand OpenClaw's prompt system, you'll instinctively ask "where is the system prompt defined?" when you look at any new Agent framework.

This ability doesn't expire. Whatever framework is popular next year, you'll get up to speed quickly, because you've seen through to the essence, not just the surface.

### 1.3 The Possibility of Creation

Here's a fact worth paying attention to: **OpenClaw's official Skills are limited in number, but the community has already produced a large number of third-party Skills**.

Who wrote these Skills? Developers who understood the underlying mechanisms — just like you will.

- **Coding Assistant Skill**: Lets OpenClaw understand the team's coding standards and automatically generate compliant code
- **Stock Analysis Skill**: Connects to trading APIs, pushes customized market analysis reports every morning
- **Smart Customer Service Skill**: Integrates with the company's knowledge base to automatically answer common customer questions
- **Personal Knowledge Management Skill**: Automatically organizes notes, extracts to-dos, and builds knowledge connections

These aren't features provided by OpenClaw officially — they were created by community developers building on the OpenClaw architecture.

**When you understand how to build Skills, how to modify prompts, and how to connect new channels, you shift from "consumer" to "creator".**

Going further, if you have unique needs for a specific scenario that the existing OpenClaw can't perfectly satisfy, you have options:

- **NanoClaw route**: Implement a minimal but entirely your own Agent with very little code
- **Fork route**: Modify the OpenClaw source code to adapt it to your work environment
- **IronClaw route**: Add security hardening, audit logging, and access control to meet compliance requirements

Part Two will show real examples of each of these routes, giving you a concrete path **from understanding to creation**.

### 1.4 Extending Your Professional Value

Let's be practical: what real benefits will learning this bring you?

Based on observations of trends in the AI development market:

- Developers who can skillfully use AI Agent tools are more competitive in the job market
- Developers who can build custom Skills and integrate enterprise systems are in high demand in the freelance market
- Technical consultants who can perform deep customization based on Agent architecture typically command higher project value

The demand in this market is real, and the supply is currently relatively limited.

More importantly, this kind of skill has a **compounding effect**. The ReAct loop you understand today, the Skill development you master tomorrow, the multi-channel integration you learn the day after — these capabilities stack together and grow your competitiveness in AI application development exponentially.

---

## 2 What: What You Will See

Part Two is not a source-code reading guide — it's an **architectural expedition**. We'll observe the OpenClaw system from different angles and at different depths.

### 2.1 Block One: Dissecting OpenClaw (Chapters 1–7)

This block will dig into OpenClaw's core mechanisms layer by layer, like dissecting a precision instrument.

#### Chapter 1: Core Positioning and Design Philosophy

Exploring a fundamental question: **What is the essential difference between an Agent Runtime and a Chatbot?**

This isn't as simple as "one can execute things and the other can't." You'll discover:

- Why OpenClaw chose self-hosting over cloud hosting
- The design philosophy behind the core tools (read/exec/edit/write)
- How the WebSocket Gateway architecture keeps the system loosely coupled
- The advantages and tradeoffs of these design choices

#### Chapter 2: The ReAct Loop — The Agent's "Think-Act" Engine

A deep dive into the Agent's core working mechanism:

- The complete lifecycle of the ReAct loop
- Serial execution and causal consistency
- The relationship between loop depth and task complexity
- The divide between three architectural philosophies: Planner, Reactor, and ReAct
- State management and layered memory structure

#### Chapter 3: The Prompt System — The Agent's "Soul Engineering"

This is one of OpenClaw's most distinctive designs: **using multiple Markdown files to define the Agent's "personality" and "knowledge"**.

- `SOUL.md`: The Agent's identity, character, and behavioral guidelines
- `USER.md`: User profile, preferences, and interaction habits
- `AGENTS.md`: Workflow and decision rules
- `TOOLS.md`: Environment information memo
- `IDENTITY.md`: Agent's basic identity information
- `MEMORY.md`: Storage format for long-term memory
- `HEARTBEAT.md`: Trigger conditions for scheduled tasks
- `BOOTSTRAP.md`: New workspace initialization guide

You'll understand:

- How these files are combined into the final system prompt
- How the hot-update mechanism makes changes take effect immediately
- How to fine-tune Agent behavior by adjusting prompts
- Token budget allocation strategy (how much goes to the system prompt vs. conversation history)

#### Chapter 4: The Tool System — The Agent's "Hands and Feet"

OpenClaw's core capabilities come from its tools. We'll go deep into:

- The design philosophy of the four foundational tools (read/write/edit/exec)
- Tool descriptions as interfaces: how to help the LLM accurately understand a tool's purpose
- The lazy-loading mechanism for Skills
- The minimal complete set: why four tools are enough

#### Chapter 5: The Message Loop and Event-Driven Architecture — The Agent's "Heartbeat"

This is the Agent's "heartbeat." You'll see:

- The command queue and swim-lane model
- Four task types: Main, Cron, Subagent, Nested
- Time awareness and the heartbeat mechanism
- Layered fault-tolerance design

#### Chapter 6: The Unified Gateway — One Entry Point, Countless Channels

OpenClaw can run on multiple platforms simultaneously. We'll explore:

- The Gateway's architectural position and responsibilities
- The adapter pattern and the open/closed principle
- Three-layer abstraction of the message model: Session/Conversation/Message
- Bidirectional communication and identity recognition

#### Chapter 7: The Security Sandbox — Balancing Freedom and Constraint

A deep look at OpenClaw's security mechanisms:

- Three-layer defense-in-depth architecture
- Filesystem sandbox and isolation
- The three-layer model of the command execution sandbox
- Defense against prompt injection attacks

### 2.2 Block Two: Exploring Alternatives (Chapters 8–10)

The best way to understand a system is to see how others solved the same problems.

#### Chapter 8: Lightweight Solutions — What to Do When OpenClaw Is Too Heavy

- **NanoClaw**: Minimal TypeScript implementation, single process + container isolation
- **Nanobot**: Python textbook-level implementation, research-friendly + MCP support
- **ZeroClaw**: Rust implementation, <5MB memory, runnable on $10 hardware

You'll see: how far can complex features be simplified? Which features are indispensable and which can be sacrificed?

#### Chapter 9: Security Hardening — Putting Armor on Your Agent

- **IronClaw**: Enterprise-grade security architecture
  - WASM sandbox: no external tool is trusted by default
  - Key protection: zero-exposure model
  - Prompt injection defense: multi-layer filtering
  - Docker sandbox: the last line of defense

#### Chapter 10: Hardware Solutions — Running an Agent on "Shrimp" Hardware

- **PicoClaw**: Low-power version running on embedded devices
  - Hardware selection: why did ARM win?
  - Power optimization: how to run an Agent on battery power
  - Offline capability: fully local inference in an environment with no network

### 2.3 Block Three: AI Agent Systems

This block focuses on core Agent capabilities such as memory, collaboration, autonomy, and long-running behavior.

#### Chapter 11: Memory System Design — How an Agent Actually Remembers

- **OpenClaw / Droid / Hermes comparison**: three different memory philosophies
  - Files as memory: why transparency and control matter
  - Context engineering: why token budget management is an architecture capability
  - Episodic memory: how to turn experience into reusable Skills

### 2.4 Block Four: LLM Architecture Analysis

This block is reserved for model internals, reasoning paths, context mechanics, and multimodal architecture topics.

### 2.5 Block Five: Create Your Own (Chapters 11–15)

This block focuses on hands-on OpenClaw customization. At the moment, only Chapter 13 has been published, so this overview only lists content that already exists to keep navigation aligned with the actual docs.

#### Chapter 13: Skill Development in Practice

Building on Chapter 4's tool system, from description to code:

- **Frontmatter advanced configuration**: Not just name and description — also auto-install and dependency declarations
- **`impl/` in action**: Moderate-complexity TypeScript — RSS fetching, email parsing, error handling
- **Subagent calls**: Chapter 4 mentioned the subagent tool; here we see how to use it inside a Skill to decompose tasks
- **Case study**: Xiao Li's news aggregation Skill — automatic fetching, summary generation, and tag classification all in one

---

## 3 How: Exploring This Section

### 3.1 Three Entry Paths

We've designed three different entry points — choose based on your current state:

**Path A: Principles First**

If you're curious about "how it works," start at Chapter 1 and read through to Chapter 7 in order. This is the most systematic path to understanding.

**Path B: Comparison First**

If you already have some hands-on experience and want to know "what else is possible," start with Chapters 8–10 for alternative designs, then move into the new AI Agent Systems category with Chapter 11. That sequence makes it easier to separate runtime tradeoffs from Agent-capability design.

**Path C: Need First**

If you already have a specific customization goal ("I want to integrate it with our company's XX system"), jump straight to Chapters 11–15. Read and build simultaneously, going back to look up the underlying principles as needed.

### 3.2 Levels of Understanding

For each concept, you don't need to "have it all." Choose your depth based on your goal:

| Depth | Target Audience | How to Learn |
|-------|----------------|--------------|
| **Conceptual** | Most readers | Knowing "this module exists" and "what it's responsible for" is enough |
| **Principled** | Readers who want deeper understanding | Understand how it works and why it was designed this way |
| **Code-level** | Readers who want to do custom development | Read source code, understand implementation details, be able to modify |

For example, for the Command Queue:

- **Conceptual**: Know that "the Command Queue serializes command execution" and understand its position in the architecture diagram
- **Principled**: Understand queue scheduling, concurrency control, and the swim-lane model (queue mode configured per channel: steer/followup/collect/steer-backlog/steer+backlog/queue/interrupt)
- **Code-level**: Be able to read and modify the Command Queue implementation, add new queue modes or handlers

You can choose different depths for different concepts. For example, go deep on the prompt system (because you want to customize the Agent's personality) but stay at the conceptual level for channel integration (because you only use Telegram).

### 3.3 Practical Suggestions

Although we don't have mandatory "homework," we recommend:

#### Read a Chapter, Change Something

- After reading the chapter on the prompt system, try modifying your `SOUL.md` and see how the Agent's response style changes
- After reading the chapter on the tool system, try writing the simplest possible Skill (for example, a tool that returns the current time)
- After reading the architecture analysis chapter, try using `openclaw logs` to observe a complete message flow

#### Read With a Question in Mind

If you encounter strange behavior while using OpenClaw, treat it as an opportunity to explore:

- "Why didn't it call the tool I expected this time?" → Go to Chapter 4 to see the tool selection mechanism
- "Why did it forget our previous agreement?" → Go to Chapter 3 to see the memory system design
- "Why is the response so slow?" → Go to Chapter 5 to see the message loop's execution flow

#### Take Notes, Draw Diagrams

The best way to learn a complex system is to reorganize it in your own way:

- Draw your own architecture diagram (even if it's imperfect, it externalizes your understanding)
- List the concepts you care about and how they connect
- Record the problems you encounter and the solutions you find

---

## 4 The Tradeoff: Costs and Benefits

Before diving in, we need to honestly discuss the costs.

### 4.1 What You Need to Invest

> **Note:** Learning this section requires more effort, but the returns are long-term.

<details>
<summary>Click to expand: Learning cost details</summary>

#### Time

Part Two covers significantly more ground than Part One. Reading all the chapters completely requires a meaningful time investment. If you want to practice hands-on, it will take even longer.

But remember — this isn't an exam, there's no deadline. You can take a month or half a year.

#### Cognitive Load

This section involves:

- TypeScript/JavaScript code (OpenClaw is built with Node.js)
- System design concepts (event-driven architecture, message queues, state management)
- AI principles (LLM behavioral characteristics, prompt engineering, the ReAct paradigm)

If you're unfamiliar with some of these areas, you may need to look things up. That's completely normal.

#### Frustration

Understanding complex systems is not linear. You might spend an hour reading a chapter and feel like you didn't absorb anything. Or you think you understood it, but when you try to apply it, things are completely different in practice.

This frustration is a normal part of the learning curve. Everyone who has truly come to understand OpenClaw has been through it.

</details>

### 4.2 What You Will Gain

#### The Ability to Solve Complex Problems

When you encounter strange behavior in OpenClaw, diagnosis time drops from hours to minutes. When you need to customize a feature, you know where to start.

#### Cross-Framework Transferability

When a new Agent framework emerges next year, you'll be up to speed within days, because you've seen through to the essence.

#### The Possibility of Creation

From tweaking configurations to developing Skills, from forking and modifying to building from scratch, you have a full toolkit to express your ideas.

#### Potential Economic Returns

Whether it's improved competitiveness when job hunting, or a skill set to offer as a freelancer, this is a capability with real market demand.

### 4.3 An Honest Recommendation

Not everyone needs to go deep into this section.

If your experience using OpenClaw is that:

- The existing Skills already meet most of your needs
- You haven't encountered any behavior that you can't explain
- You don't have a strong curiosity about "underlying principles"
- Your time and energy are limited

Then staying in Part One is a completely reasonable choice. You can always come back when a specific problem motivates you to go deeper.

**The best motivation for learning is "I need to solve this problem," not "I should finish this tutorial."**

---

## 5 From Driver to Engineer

Let's return to the car analogy.

Part One taught you to drive — press the accelerator, steer the wheel, watch the dashboard. That gets you to many destinations quickly.

Part Two takes you under the hood — see how the engine combusts, how the gearbox shifts, how the electrical system controls everything. This won't make you drive faster, but when you hear a strange noise, you'll know where the problem is. When you want to modify something, you'll know where to start. When you're faced with an unfamiliar car, you'll be able to understand it more quickly.

More importantly, **you begin to develop the ability to design and build**.

Maybe you won't actually build a car. But when you understand how an engine works, your understanding of "movement" changes forever. You're no longer a passive consumer of transportation, but someone who has the capacity to participate in creation.

AI Agents are becoming a foundational infrastructure tool — just like databases, web servers, and operating systems. Understanding their underlying mechanisms today is like understanding the HTTP protocol in 1995, the Linux kernel in 2005, or Docker containers in 2015.

This understanding won't pay off immediately, but it's a long-term investment. At some point in the future, it will let you see an opportunity others can't see, or solve a problem others can't solve.

---

**Now, choose where you want to start:**

- [Chapter 1: Core Positioning and Design Philosophy](./chapter1/index.md) — Understand the essence of an Agent Runtime and see why OpenClaw was designed the way it is
- [Chapter 11: Memory System Design](./chapter11/index.md) — Compare three memory architectures and understand what it really means for an Agent to “remember”
