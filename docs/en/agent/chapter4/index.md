---
title: "AI Agent Architecture Design (IV): Multi-Agent Collaboration"
---

# AI Agent Architecture Design (IV): Multi-Agent Collaboration (Comparing OpenClaw, Claude Code, and Hermes Agent)

<p class="multi-subtitle"><strong>From “one Agent doing everything serially” to “multiple Agents splitting work, checking each other, and sharing experience”: how three mainstream frameworks design role boundaries, context isolation, and coordination</strong></p>

<div class="multi-cover multi-figure">
  <img src="../../../static/agent/chapter4/images/multi-agent-overview-wechat.png" alt="Multi-Agent system overview" />
  <p><sub>Overview: the original article opens with one summary diagram that puts “why multi-Agent,” the four design questions, and the three framework philosophies into the same frame</sub></p>
</div>

<div class="multi-meta-card">
  <ul>
    <li><strong>Series</strong>: AI Agent Architecture Design (IV): Multi-Agent Collaboration</li>
    <li><strong>Goal</strong>: understand how three frameworks design multi-Agent collaboration, and the engineering tradeoffs behind role separation, context isolation, and coordination</li>
    <li><strong>Best for</strong>: readers who care about Agent internals and want to understand why these systems are designed the way they are</li>
    <li><strong>Estimated reading time</strong>: 15 minutes</li>
  </ul>
</div>

---

## Why do we need multiple Agents?

A single Agent has two fundamental limits.

**First, the context window is finite.** In a complex project, files, history, and tool-call outputs quickly fill a single context window. As the window gets fuller, model attention becomes more diffuse, the “Lost in the Middle” problem gets worse, and output quality drops.

**Second, one Agent can only do one thing at a time.** If a task contains four independent subtasks, a single Agent must execute them serially—research first, then write, then review, then test. If each one takes five minutes, the total is twenty minutes.

The architectural value of multi-Agent systems is that they make subtasks parallel, keep each Agent’s context cleaner, and let each worker focus on its own scope.

But multi-Agent is not free. It introduces coordination overhead, communication cost, and context-consistency problems. A poorly designed multi-Agent system can lose all the benefit of parallelism and end up slower and more fragile overall.

That is exactly the problem these three frameworks try to solve in different ways.

---

## The four core design questions of a multi-Agent system

Before comparing the frameworks, it helps to make the design questions explicit:

- **How are roles separated?** Who does what, and how are responsibilities bounded so they do not overlap or leave gaps?
- **How is context isolated?** How is information partitioned so one Agent’s context does not pollute another Agent’s judgment?
- **How do Agents communicate?** How are results passed along, how is work assigned, and is coordination language-based or structure-based?
- **How are results merged?** How are outputs combined, how are conflicts resolved, and how does the user receive one coherent final answer?

The three frameworks answer these questions in strikingly different ways, revealing three different philosophies of multi-Agent architecture.

---

## OpenClaw: a two-layer model, from subagents to routed Agents

<div class="multi-figure">
  <img src="../../../static/agent/chapter4/images/openclaw-multi-agent-wechat.png" alt="OpenClaw multi-Agent collaboration diagram from the original article" />
  <p><sub>Figure 1: the original article presents OpenClaw as a three-part collaboration picture—subagents at the bottom, routed Agents in the middle, and Agent Teams / community orchestration above</sub></p>
</div>

### Two multi-Agent modes, two different jobs

OpenClaw’s multi-Agent support has two layers that are often mixed together, even though they solve different problems.

**Layer 1: SubAgents**

The main Agent spawns a subagent through the `sessions_spawn` tool or the `/subagents spawn` command. The call is non-blocking: the main Agent issues the task and immediately continues its own work instead of waiting. When the subagent finishes, it reports back to the main Agent or to a designated channel.

This is the most common mode, and it is ideal when the main Agent wants to outsource a focused subtask and keep moving.

Its key limitation is explicit: **a subagent can only report back to the main Agent; it cannot talk directly to sibling subagents.** All coordination flows through the main Agent.

**Layer 2: Routed Agents**

This is a Gateway-level multi-Agent pattern. Each Agent has its own workspace, session storage, and auth profile, while bindings route different channels or users to different Agents.

This layer fits scenarios such as:

- separating work and personal Agents
- assigning different Agents to different users
- enforcing strict security isolation

At this level the Agents are fully independent. They do not share memory or context, and any communication has to be forwarded explicitly through webhooks or queues.

### Context isolation: the filesystem becomes the coordination layer

OpenClaw’s core isolation mechanism is filesystem isolation.

Each Agent owns its own `workspace`, its own `MEMORY.md`, `SOUL.md`, and session history, typically stored under `~/.openclaw/agents/<agentId>/`.

That means the standard way for Agents to collaborate is not by sharing a giant live context window. It is by **handing off files**: one Agent writes a result somewhere, and another Agent reads it later.

This makes OpenClaw especially suitable for strongly isolated, loosely coupled scenarios. Each Agent behaves almost like a small service with a clear boundary, and coordination happens through storage and scheduling.

---

## Claude Code: Agent Teams, P2P communication, and filesystem coordination

<div class="multi-figure">
  <img src="../../../static/agent/chapter4/images/claude-code-agent-teams-wechat.png" alt="Claude Code Agent Teams diagram from the original article" />
  <p><sub>Figure 2: the original article contrasts two Claude Code models directly—the hierarchical Subagent pattern on the left and a P2P Agent team on the right</sub></p>
</div>

### The essential difference between its two modes

Claude Code splits multi-Agent collaboration into two distinct layers, and the official documentation is unusually clear about the boundary:

**Subagents** operate inside a single session. They report only to the main Agent and do not communicate directly with one another. They are best for fast, focused tasks where reporting back is enough.

**Agent Teams** are different. Multiple fully independent Claude Code instances form a team, each with its own context window, and they can **communicate directly with one another (P2P)** without funneling every interaction through a single lead.

That is the biggest architectural difference between Agent Teams and ordinary subagents.

- Subagents behave like separate contractors reporting upward
- Agent Teams behave like a project team sitting in the same room

Members can directly exchange findings, question each other, and converge together.

### The filesystem as the shared coordination surface

Claude Code’s coordination model is also built around the filesystem—not because messaging is impossible, but because shared files are often the more efficient collaboration medium.

A helpful analogy is team writing. Instead of each person verbally retelling their edits to the next person, everyone opens the same shared document and immediately sees what others have done.

Inside Claude Code, each Teammate is an independent Agent instance with its own subtask. If one Teammate finishes a module, another Teammate that depends on it can simply read the file and continue. Nobody has to explicitly relay the information.

The obvious downside is conflict: if multiple Teammates edit the same file at once, they overwrite each other.

Claude Code’s answer is **Worktree mode**. Each Teammate works in a separate Git worktree, like writing on separate draft sheets first and merging later. That avoids simultaneous edits to the same lines.

### When should you use Agent Teams, and when are subagents enough?

The decision rules are quite practical:

- **Use Subagents** when the work is quick, narrow, independent, and only needs a result reported upward
- **Use Agent Teams** when the work spans frontend, backend, testing, or other specialties, and teammates benefit from directly sharing discoveries or challenging each other’s plans
- **Stick to a single session** when the task is sequential, the same file must be edited repeatedly, or dependencies between steps are tight

So Claude Code does not treat multi-Agent as the default answer. It treats it as a collaboration structure with a clear payoff boundary.

---

## Hermes Agent: isolated workers plus shared episodic knowledge through PLUR

<div class="multi-figure">
  <img src="../../../static/agent/chapter4/images/hermes-plur-wechat.png" alt="Hermes Agent multi-Agent collaboration diagram from the original article" />
  <p><sub>Figure 3: the Hermes diagram emphasizes fully isolated execution units plus Skills / PLUR-based experience sharing, where coordination depends less on live conversation and more on experience propagation</sub></p>
</div>

### Core design: total isolation, coordination through files and Skills

Hermes Agent’s multi-Agent philosophy is simple and strict: **each subagent is fully isolated**—its context, terminal, and conversation history are all separate—and coordination mainly happens through the filesystem and the Skills layer.

That isolation shows up in several places:

- an independent conversation thread that does not inherit the parent Agent’s history
- an independent terminal instance
- `execute_code` Python RPC scripts that provide a low-context-cost tool channel

So Hermes strongly prefers clean execution units over heavy parent-context inheritance.

### Skills as a shared knowledge layer across Agents

In any multi-Agent system, one practical problem shows up quickly: one Agent discovers an effective way to do something, while another Agent has no idea that lesson already exists.

Hermes does not solve that mainly through live messaging. It solves it through **Skills as a shared knowledge base**.

A Skill here is essentially a working note automatically written after the Agent completes a complex task:

- how to do the task
- which pitfalls appeared
- what to remember next time

By default, each Agent’s notes are stored locally and are not visible to others. But if a Skill is placed in a shared directory such as `~/.hermes/skills/`, every Agent can load it on startup.

For example, you may ask one Agent to analyze competitors. It discovers an efficient workflow and saves it as a Skill. The next Agent handling a similar task loads that Skill and avoids rediscovering the same process from scratch.

PLUR pushes this idea further. If you correct one Agent’s approach, PLUR can propagate that correction to other Agents in the same project automatically, instead of requiring manual updates everywhere.

That is what makes Hermes distinctive: **Agents do not mainly coordinate by talking in real time; they coordinate by accumulating shared experience.** A pitfall one Agent hits today can be avoided by all of them tomorrow.

---

## The core tradeoffs in multi-Agent system design

### Tradeoff 1: should the AI decide the division of labor, or should you define the rules?

The same job can be approached in two very different ways.

One way is to tell the AI, “Do a competitor analysis,” and let it decide what to search, how to compare, and when to stop. That is convenient, but the workflow may vary every time, and when something breaks it can be hard to tell where things went wrong.

The other way is to define the steps yourself: “First collect sources, then organize comparisons, then write the report, and only proceed after each step is complete.” That is slower, but debugging becomes much easier.

So the rule is straightforward: **the more fixed and error-intolerant the task is, the more the human should define the rules; the more open-ended and adaptive it needs to be, the more freedom the AI can be given.**

### Tradeoff 2: should Agents talk directly, or pass work through files?

Think of two coworkers.

- One style is to sit together and verbally hand off work the moment it is done
- Another is to drop the result into a shared folder and let the other person pick it up later

The first is real-time, but it requires both people to be active simultaneously. The second is looser and often simpler, but you do not know when the handoff will actually be consumed.

Multi-Agent coordination has the same choice:

- tasks that need back-and-forth confirmation benefit from real-time messaging
- tasks that mostly transfer results often work better with file-based handoff

### Tradeoff 3: should a subagent know what the parent Agent was thinking?

Imagine asking a coworker to review your plan.

If they heard your entire thought process beforehand, they may unconsciously follow your logic and miss the fact that your premise was wrong from the start.

If they know nothing and only review your conclusion, they are more likely to surface genuinely independent criticism.

Subagents work the same way:

- if you want them to help execute, more background is often better → let them inherit the parent context
- if you want them to review and judge independently → let them start from zero

---

## Closing Note

Multi-Agent is not just “open more model windows.” The real design challenge lies in role definition, context isolation, coordination strategy, and result integration.

- **OpenClaw** favors strong isolation, file-based coordination, and a two-layer routing model
- **Claude Code** emphasizes explicit teamwork, peer-to-peer communication, and Worktree-based conflict control
- **Hermes Agent** focuses on fully isolated execution units plus shared knowledge propagation through Skills and PLUR

No single architecture wins in every scenario. The key question is whether the task is worth decomposing in the first place, and then whether coordination should be driven by live communication, shared files, or shared experience.

<style>
.multi-subtitle {
  margin: -4px 0 20px;
  text-align: center;
  color: #7b6641;
  font-size: 1.05rem;
  letter-spacing: 0.02em;
}

.multi-cover,
.multi-figure {
  margin: 28px auto;
  padding: 14px;
  border-radius: 20px;
  background: linear-gradient(180deg, #fffaf2 0%, #ffffff 100%);
  border: 1px solid rgba(222, 180, 106, 0.28);
  box-shadow: 0 14px 34px rgba(148, 101, 28, 0.08);
  overflow: hidden;
}

.multi-cover img,
.multi-figure img {
  display: block;
  width: 100% !important;
  max-height: none !important;
  margin: 0 auto;
  border-radius: 12px;
}

.multi-cover p,
.multi-figure p {
  margin: 12px 6px 2px;
  text-align: center;
  color: #7c5a1f;
  font-size: 0.94rem;
  line-height: 1.7;
}

.multi-meta-card {
  margin: 20px 0 28px;
  padding: 18px 20px;
  background: linear-gradient(135deg, rgba(255, 246, 221, 0.92), rgba(255, 255, 255, 0.98));
  border: 1px solid rgba(226, 179, 76, 0.34);
  border-radius: 18px;
  box-shadow: 0 10px 28px rgba(201, 145, 38, 0.08);
}

.multi-meta-card ul {
  margin: 0;
  padding-left: 1.1rem;
}

.multi-meta-card li {
  margin: 0.45rem 0;
  line-height: 1.75;
}

.vp-doc h2 {
  margin-top: 42px;
  padding-left: 14px;
  border-left: 4px solid #e2ad47;
}

.vp-doc h3 {
  margin-top: 28px;
}

.vp-doc blockquote {
  border-left: 4px solid #e2ad47;
  background: rgba(255, 248, 230, 0.72);
  border-radius: 0 14px 14px 0;
  padding: 10px 16px;
}

.vp-doc table {
  border-radius: 12px;
  overflow: hidden;
}

.vp-doc tr:nth-child(2n) {
  background-color: rgba(255, 248, 230, 0.45);
}

.dark .multi-subtitle {
  color: #c8d0da;
}

.dark .multi-cover,
.dark .multi-figure {
  background: linear-gradient(180deg, rgba(56, 43, 20, 0.65), rgba(30, 30, 30, 0.92));
  border-color: rgba(226, 173, 71, 0.28);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.28);
}

.dark .multi-meta-card {
  background: linear-gradient(135deg, rgba(73, 53, 20, 0.86), rgba(30, 30, 30, 0.95));
  border-color: rgba(226, 173, 71, 0.28);
}

.dark .multi-cover p,
.dark .multi-figure p {
  color: #f2d7a0;
}

.dark .vp-doc blockquote {
  background: rgba(82, 61, 22, 0.3);
}

@media (max-width: 768px) {
  .multi-cover,
  .multi-figure,
  .multi-meta-card {
    border-radius: 16px;
  }

  .multi-cover,
  .multi-figure {
    padding: 10px;
  }

  .multi-cover p,
  .multi-figure p {
    margin-top: 10px;
    font-size: 0.9rem;
    line-height: 1.65;
  }
}
</style>
