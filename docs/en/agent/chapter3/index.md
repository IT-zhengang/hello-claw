# AI Agent Architecture Design (III): Task Planning and Execution Loops (Comparing OpenClaw, Claude Code, and Hermes Agent)

<p class="loop-subtitle"><strong>From “a model that can call tools” to “a system that can finish complex work reliably”: how three mainstream Agent frameworks design planning, scheduling, recovery, and stopping behavior</strong></p>

<div class="loop-cover loop-figure">
  <img src="../../../static/agent/chapter3/images/cover.png" alt="Task planning and execution-loop cover" />
</div>

<div class="loop-meta-card">
  <ul>
    <li><strong>Series</strong>: AI Agent Architecture Design (III): Task Planning and Execution Loops</li>
    <li><strong>Goal</strong>: understand how OpenClaw, Claude Code, and Hermes Agent turn a user goal into a multi-step task that can execute, recover, and stop safely</li>
    <li><strong>Best for</strong>: readers who want to understand Agent execution from an architectural perspective rather than treating tool use as a black box</li>
    <li><strong>Estimated reading time</strong>: 15 minutes</li>
  </ul>
</div>

---

## What problem does an execution loop really solve?

The memory system answers “what the Agent knows.” The tool system answers “what the Agent can do.”

But what determines whether an Agent behaves like a real system instead of a talkative model is a third question:

> **When the user gives a complex goal, how does the Agent break it into a sequence of actions, keep correcting itself, and still carry the task to completion?**

That is the job of the execution loop.

When the execution loop is poorly designed, four failure modes show up quickly:

- **No planning**: the system starts acting immediately and realizes halfway through that the direction was wrong
- **No recovery**: when a tool fails, it either retries forever or stops too early
- **No observability**: the user cannot tell what the system is doing or intervene in time
- **No persistence**: once the task gets long and context fills up, state is lost

So the execution loop is not a minor implementation detail. It is the Agent’s task operating system. It determines whether the Agent can only take a couple of steps or can reliably finish real work.

---

## ReAct is the common starting point, but not the full answer

<div class="loop-figure">
  <img src="../../../static/agent/chapter3/images/react.png" alt="ReAct execution loop" />
  <p><sub>Figure 1: Reason → Act → Observe is the shared foundation of modern Agent execution</sub></p>
</div>

All three frameworks differ sharply, but they still share the same underlying pattern: ReAct (Reason → Act → Observe).

```text
Receive input
  ↓
Reason: inspect the current state and decide what to do next
  ↓
Act: call a tool and perform the operation
  ↓
Observe: read the result returned by the tool
  ↓
Inject the result back into context and continue the loop
```

The loop itself is simple. The difficulty appears when you try to make it production-grade:

- When a tool fails, should the system retry, route around the problem, or escalate?
- When the context window approaches its limit, how should history be compacted without losing the task?
- When a long task has to wait, how does execution continue across sessions?
- How can the user see intermediate state and intervene when needed?

In other words, **ReAct provides the skeleton. What really differentiates frameworks is how they handle triggers, planning depth, scheduling, recovery, and stopping conditions.**

---

## OpenClaw: making proactive wakeups part of execution

<div class="loop-figure">
  <img src="../../../static/agent/chapter3/images/openclaw-loop.png" alt="OpenClaw execution architecture" />
  <p><sub>Figure 2: OpenClaw combines message-driven execution with heartbeat-driven execution</sub></p>
</div>

### Two entry points: user-triggered and system-triggered

OpenClaw’s execution loop is distinctive because it does not rely on a single entry path.

The first path is the standard message-driven flow:

- the user sends a message
- the Gateway receives it
- an Agent session starts
- the ReAct loop runs
- the system produces a result and exits

The second path is more unusual and more characteristic: the heartbeat flow.

- the system triggers a heartbeat on a fixed interval
- the Agent reads `HEARTBEAT.md`
- it checks whether any scheduled or pending tasks should run
- it either acts or exits quietly

This solves a foundational constraint: **language models do not naturally remember to act on their own.** OpenClaw inserts an external clock into the architecture so the Agent can be woken up proactively.

### Using scheduling instead of blocking waits

Heartbeat solves “wake up periodically and inspect the world.” It does not solve “resume exactly at a later point in time.”

So OpenClaw uses Cron jobs for wait-heavy tasks. If an external operation needs three minutes before the result is available, the session does not block and wait. It simply schedules a future continuation.

```text
Trigger external operation
    ↓
Discover that waiting is required
    ↓
Create a Cron job for 3 minutes later
    ↓
End the current session
    ↓
Resume in a fresh session later
```

This is a classic engineering move: **take waiting out of the session and hand it to the scheduler.** Each individual session stays lightweight, while long tasks are broken into multiple short sessions stitched together over time.

### Strengths and tradeoffs

OpenClaw’s main strength is that it naturally fits long-running and proactive tasks. You can think of it as an Agent designed to be awakened repeatedly.

But its recovery behavior depends more heavily on the model’s own judgment. When a tool fails, the error is injected back into context and the model decides what to do next.

That gives flexibility, but it also means:

- recovery quality depends heavily on model behavior
- system-level hard constraints are relatively light
- predictability under complex failure conditions is weaker than in more heavily engineered frameworks

**So OpenClaw is best understood as an execution style that prioritizes proactivity and session slicing.**

---

## Claude Code: bringing planning, recovery, and user observation into the core loop

<div class="loop-figure">
  <img src="../../../static/agent/chapter3/images/claude-code-loop.png" alt="Claude Code execution architecture" />
  <p><sub>Figure 3: Claude Code emphasizes explicit planning, engineered recovery, and visible execution</sub></p>
</div>

### Plan first, then execute

The first major difference in Claude Code is that it elevates “think first, act second” into a first-class architectural stage.

For complex work, the system often enters a Plan mode first:

1. build a full execution plan
2. show the plan to the user
3. execute only after confirmation

The design logic is clear: **for tasks with meaningful side effects, a wrong direction is usually more expensive than a slower start.**

If the work involves editing code, changing configuration, running commands, or touching external systems, discovering the mistake only after execution can be costly. The value of Plan mode is not that it makes the system magically smarter. It makes errors surface earlier.

### Recovery is implemented as system logic, not prompt tricks

The second defining trait of Claude Code is that many recovery behaviors are encoded into program logic instead of being delegated entirely to the model.

Typical recovery branches include:

- **tool-call failures**: identify the error type, then choose retry or fallback
- **malformed model output**: ask the model to repair the structure and regenerate
- **context pressure**: compact history and continue execution

This reflects a very strong engineering principle: **failure is not an exception to the loop; it is a native branch of the loop.**

One especially reusable pattern is the circuit breaker. If automatic compaction keeps failing, the system should not retry forever. It should stop once a threshold is reached and expose the failure to the user.

### User observation is treated as loop input

Claude Code also makes a very important choice: **execution is visible by default.**

Tool calls, file edits, command output, and intermediate progress are streamed to the user in real time. That is not only about better UX. It changes the execution architecture because the user becomes an active participant in the loop:

- the user can catch direction drift early
- the user can add constraints mid-flight
- the user can decide whether risky actions should continue

That makes Claude Code feel less like a background daemon and more like an **interactive engineering operator**.

### Subagent isolation becomes an explicit design axis

Claude Code is also notable for how it handles subagents. It does not force a single collaboration mode. Instead, it exposes multiple levels of context sharing and isolation:

- **Fork**: copy the parent context for parallel exploration
- **Teammate**: keep separate contexts and coordinate through external artifacts
- **Worktree**: isolate filesystem changes in a separate worktree

This shows that in Claude Code’s architecture, **“how much context should a subtask share?” is itself treated as a first-class design question.**

---

## Hermes Agent: embedding scheduling into the system and constraining loops with budgets

<div class="loop-figure">
  <img src="../../../static/agent/chapter3/images/hermes-loop.png" alt="Hermes Agent execution architecture" />
  <p><sub>Figure 4: Hermes Agent deeply embeds scheduling and adds explicit iteration budgets</sub></p>
</div>

### The scheduler is not an add-on; it is part of the core

Hermes Agent’s most distinctive trait is that scheduling is not a side feature. It is part of the main system loop.

In OpenClaw, heartbeat and Cron sit beside the execution loop as highly practical proactive mechanisms. In Claude Code, the center of gravity is interactive execution and recovery. In Hermes, `scheduler.tick()` is directly part of the system’s recurring maintenance cycle.

The flow is roughly:

```text
scheduler.tick()
    ↓
Acquire scheduler lock
    ↓
Find due tasks
    ↓
Start a fresh Agent session for each task
    ↓
Load attached Skills
    ↓
Execute the prompt and route the result
    ↓
Compute the next run time
```

That makes Hermes especially suitable for long-running background automation, periodic tasks, and multi-task autonomous operation.

### Cron + Skills pushes execution toward learning

A particularly interesting Hermes choice is that scheduled tasks can be paired with Skills.

That means a scheduled task is not just “run this prompt at a given time.” It becomes “run this prompt using a specific accumulated method.”

As the Skill library grows, the very same recurring task becomes more capable over time. In other words, **the execution loop starts to blend into the learning loop.** That is a strong fit for recurring reports, research assistants, content pipelines, and operational automation.

### Iteration budgets: hard constraints against runaway loops

Hermes also introduces a very reusable mechanism: the **iteration budget**.

<div class="loop-figure">
  <img src="../../../static/agent/chapter3/images/tradeoffs.png" alt="Execution-loop tradeoffs" />
  <p><sub>Figure 5: planning depth, scheduling model, stopping strategy, and isolation level shape the personality of an execution loop</sub></p>
</div>

The system assigns a clear budget to tool calls, warns as the limit approaches, and stops when the ceiling is reached.

The architectural value is immediate:

- it sharply reduces the risk of infinite loops
- it turns resource boundaries into system-level constraints
- it stops relying entirely on the model’s subjective sense of “I should probably stop now” 

If you want an Agent that can run for long periods without supervision, this kind of hard boundary is often essential.

### What timeout strategy reveals about design philosophy

Hermes today is closer to a fixed wall-clock timeout: once the task has been running for a certain duration, it is terminated. That is easy to reason about, but it can kill legitimate long tasks.

Architecturally, a better direction is often activity-based timeout: only treat the task as stalled if the system has stopped making progress for too long.

That detail matters because it reveals a broader principle: a timeout strategy should not merely limit duration. It should **detect real stagnation and loss of control**.

---

## What are these frameworks really optimizing for?

Viewed side by side, the three approaches are making different bets on what matters most.

### Tradeoff 1: plan first, or think while acting?

- **Claude Code** leans toward planning before execution
- **OpenClaw / Hermes** lean toward entering the loop earlier and adjusting along the way

The first works better for high-side-effect tasks. The second works better for automation and long-running operation.

### Tradeoff 2: soft stopping or hard stopping?

- **Hermes** uses budgets and limits for hard stopping
- **Claude Code** uses conditional circuit breakers for specific failure classes
- **OpenClaw** relies more heavily on the model’s own sense of completion

The harder the stopping rule, the more predictable the system becomes. The softer the stopping rule, the more autonomy it preserves.

### Tradeoff 3: is the user a spectator or part of the loop?

- **Claude Code** explicitly pulls user observation and intervention into the loop
- **OpenClaw / Hermes** lean more toward background execution and asynchronous autonomy

For development workflows and high-risk actions, keeping the user in the loop is often critical. For recurring jobs and autonomous background tasks, automation usually matters more.

### Tradeoff 4: is scheduling external or foundational?

- **OpenClaw** gives heartbeat and Cron strong practical value
- **Hermes** makes scheduling part of the core loop itself
- **Claude Code** invests more in interactive execution quality

None of these answers is universally correct. They simply reflect different task shapes and different product goals.

---

## One table to compare the three execution styles

| Dimension | OpenClaw | Claude Code | Hermes Agent |
| ---- | ---- | ---- | ---- |
| Entry points | user messages + heartbeat | mostly interactive user-driven execution | user messages + built-in scheduler |
| Planning strength | lighter, more adjustment during execution | strong, explicit Plan mode | medium, more scheduling-oriented |
| Error recovery | more model-driven | system-level recovery and circuit breakers | budgets, timeout, and scheduling together |
| User visibility | medium | very high, visible by default | medium, more background-oriented |
| Long-task support | session slicing + Cron continuation | compaction, recovery, and user control | native support for recurring scheduled work |
| Stopping model | softer stopping | conditional hard stops | explicit hard stops via budgets |
| Core personality | proactive wakeup engine | interactive engineering operator | scheduler-centered autonomous operator |

---

## Closing summary: mature execution loops usually combine all three directions

The essence of an execution loop is not “how many tools the model can call.” It is **how the system carries a task from start to progress to recovery to completion.**

Each framework contributes a very clear strength:

- **OpenClaw** is strong at proactive wakeups and splitting long tasks across sessions
- **Claude Code** is strong at planning, recovery, and human collaboration
- **Hermes Agent** is strong at built-in scheduling and budget-based control

If you are designing your own Agent framework, the most reusable lessons are usually not one framework’s full implementation, but a combination of all three:

1. plan important tasks first, as Claude Code does
2. hand waiting to the scheduler instead of blocking sessions, as OpenClaw does
3. constrain runaway behavior with budgets, timeouts, and hard stopping rules, as Hermes does

Only when those three capabilities mature together does an Agent evolve from “a model that can use tools” into **a system that can work reliably over time**.

<style>
.loop-subtitle {
  margin: -4px 0 20px;
  text-align: center;
  color: #6b7280;
  font-size: 1.05rem;
  letter-spacing: 0.02em;
}

.loop-cover,
.loop-figure {
  margin: 28px auto;
  padding: 14px;
  border-radius: 20px;
  background: linear-gradient(180deg, #fffaf2 0%, #ffffff 100%);
  border: 1px solid rgba(222, 180, 106, 0.28);
  box-shadow: 0 14px 34px rgba(148, 101, 28, 0.08);
}

.loop-cover img,
.loop-figure img {
  width: 100% !important;
  max-height: none !important;
  border-radius: 12px;
}

.loop-meta-card {
  margin: 20px 0 28px;
  padding: 18px 20px;
  background: linear-gradient(135deg, rgba(255, 246, 221, 0.92), rgba(255, 255, 255, 0.98));
  border: 1px solid rgba(226, 179, 76, 0.34);
  border-radius: 18px;
  box-shadow: 0 10px 28px rgba(201, 145, 38, 0.08);
}

.loop-meta-card ul {
  margin: 0;
  padding-left: 1.1rem;
}

.loop-meta-card li {
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

.dark .loop-subtitle {
  color: #c8d0da;
}

.dark .loop-cover,
.dark .loop-figure {
  background: linear-gradient(180deg, rgba(56, 43, 20, 0.65), rgba(30, 30, 30, 0.92));
  border-color: rgba(226, 173, 71, 0.28);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.28);
}

.dark .loop-meta-card {
  background: linear-gradient(135deg, rgba(73, 53, 20, 0.86), rgba(30, 30, 30, 0.95));
  border-color: rgba(226, 173, 71, 0.28);
}

.dark .vp-doc blockquote {
  background: rgba(82, 61, 22, 0.3);
}
</style>
