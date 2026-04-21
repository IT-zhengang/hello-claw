# AI Agent Architecture (VIII): Gateway Architecture (OpenClaw, Claude Code, and Hermes Agent Compared)

<p class="protocol-subtitle"><strong>A Gateway is never just a message entry point. It determines whether an Agent behaves like a tool you summon or a worker that stays on duty.</strong></p>

<div class="protocol-figure">
  <img src="../../../static/agent/chapter8/images/overview.png" alt="Gateway architecture overview" />
  <p><sub>Overview: this chapter is not mainly about connecting Telegram or Slack. It is about how the Gateway layer, as the interface between an Agent and the world, ends up shaping the whole system.</sub></p>
</div>

<div class="protocol-meta-card">
  <ul>
    <li><strong>Series</strong>: AI Agent Architecture (VIII): Gateway Architecture</li>
    <li><strong>Core question</strong>: is a Gateway merely a message bridge, or is it the real control plane of an Agent system?</li>
    <li><strong>You will see</strong>: OpenClaw's always-on control plane, Claude Code's add-on remote-control layers, and Hermes Agent's lightweight bridge model</li>
    <li><strong>For</strong>: readers who care about Agent entry layers, message routing, multi-Agent orchestration, and long-running execution models</li>
    <li><strong>Reading time</strong>: 15 minutes</li>
  </ul>
</div>

---

## The design philosophy of the Gateway determines what an Agent is

<div class="protocol-figure">
  <img src="../../../static/agent/chapter8/images/gateway-philosophy.png" alt="Gateway philosophy shapes Agent behavior" />
  <p><sub>Figure 1: the Gateway decides where messages come from, how they are routed, who is allowed to trigger the Agent, and therefore whether the Agent behaves like a passive responder or an active system.</sub></p>
</div>

Should an Agent only start moving after you send it a message, or should it stay online, watch for events, and keep acting under rules even when you are not actively talking to it?

That is not a feature difference. It is an architectural fork. And that fork is hidden inside the definition of the Gateway.

A Gateway is the entry layer between an Agent and the outside world. Which platform a message comes from, how authentication works, how a session is resolved, which Agent receives the request, and how results flow back—all of that may happen at the “edge,” but it ultimately determines what kind of thing the Agent becomes.

- If the Gateway only forwards messages inward, the Agent behaves more like a passive tool.
- If the Gateway also owns routing, scheduling, triggering, and stateful orchestration, the Agent starts looking more like a long-running digital worker.
- If the Gateway is treated as optional and the execution loop remains the center of gravity, then the system becomes more “Agent-core first” and the entry layer stays thin.

<div class="protocol-callout">
  <strong>The real issue:</strong> Gateway design is not just about “how to connect a message platform.” It is really about whether the Agent should meet the world through a lightweight entry point or through a persistent control plane.
</div>

That is exactly why OpenClaw, Claude Code, and Hermes Agent land on three fundamentally different answers.

---

## OpenClaw: the Gateway is the operating system of the whole setup

<div class="protocol-figure">
  <img src="../../../static/agent/chapter8/images/openclaw-gateway.png" alt="OpenClaw Gateway control plane" />
  <p><sub>Figure 2: OpenClaw turns the Gateway into a real control plane: channel adapters, session resolution, command queues, and runtime execution all orbit around it.</sub></p>
</div>

### An always-on control plane

In OpenClaw, the Gateway is not a peripheral. It is one of the core product layers of the system.

It usually runs as a long-lived Node.js process, listens on a fixed port, and exposes both WebSocket and HTTP interfaces. Once a message arrives, it does much more than forward it. It drives a deterministic control path:

```text
External message (Telegram / Slack / Discord / WhatsApp ...)
        ↓
Channel Bridge (platform adapter)
        ↓
Session Resolution (resolve the session key using rules)
        ↓
Command Queue (serialize execution to avoid tool contention)
        ↓
Agent Runtime (LLM reasoning + tool execution)
        ↓
Result flows back to the original channel
```

That means the OpenClaw Gateway is not really a message entry point. It is a control plane. Who can enter, which context receives the request, and which behavior can be triggered are all decided there first, not guessed on the fly by the model.

### One process for many channels and many Agents

OpenClaw's most distinctive strength is that it can place many channels and many Agents inside one continuously running control center.

Different channels, accounts, and workspaces can be routed to different Agents through binding rules. Each Agent then owns its own workspace, session history, and permission context. In other words, the Gateway is not just an integration layer. It becomes an orchestration center.

That design yields several strong properties:

- <strong>deterministic routing</strong>: Slack, Telegram, WhatsApp, and other sources can be mapped predictably to different Agents
- <strong>context isolation</strong>: the session key becomes the unified data model, so different channels and conversations stay naturally separated
- <strong>central governance</strong>: integration, authentication, routing, and execution boundaries can all be controlled from one plane

### Heartbeat and Cron turn the Agent into an active system

The OpenClaw Gateway also has another decisive role: it does not only receive messages, it wakes the Agent up.

- <strong>Heartbeat</strong>: wakes the Agent on a cadence so it can check whether there is work to do on its own.
- <strong>Cron</strong>: triggers work at exact times and runs each execution in an isolated session.

This is the turning point. Once the Gateway can both receive messages and actively trigger tasks, the Agent stops being just a conversational tool and starts becoming a continuously operating system component.

<div class="protocol-highlight">
  <p>OpenClaw's most important Gateway insight is not simply “support many channels.” It is that the Gateway becomes the multi-Agent control plane and active scheduling center.</p>
</div>

---

## Claude Code: it did not start with a Gateway at all

<div class="protocol-figure">
  <img src="../../../static/agent/chapter8/images/claude-remote-control.png" alt="Claude Code remote control and channels" />
  <p><sub>Figure 3: Claude Code never began as a Gateway-first system. Its center is the local CLI session; remote control, Dispatch, and Channels are later extensions around that core.</sub></p>
</div>

### At heart it is a CLI tool, not a daemon

Claude Code starts from a completely different premise.

It is first and foremost a command-line tool. You open a terminal, run `claude`, start the conversation, and when you close the terminal, the session is largely over. There is no original assumption of a persistent, always-listening, globally orchestrating Gateway layer.

That means Claude Code assumes the following by default:

- the Agent is a tool you use while you work
- its lifecycle is tightly bound to a local terminal session
- “always online” is not the default capability but a later addition driven by user demand

### Its remote-control features are really post-hoc Gateway layers

As users began wanting remote access, asynchronous dispatch, and message-channel control, Claude Code gradually added three distinct capability layers:

- <strong>Remote Control</strong>: lets you connect from another device into the currently running local session, much like controlling a terminal remotely
- <strong>Dispatch</strong>: lets you send a task into Claude Code asynchronously and wait for the result later
- <strong>Channels</strong>: lets external message platforms act as entry points into Claude Code sessions

But these additions do not fully turn Claude Code into an OpenClaw-style Gateway-first architecture. They feel more like remote-access layers wrapped around a CLI-centered core.

### Its limits come from that same starting point

The core limitation is that Claude Code still depends heavily on the local machine being online.

If the local machine is off, if the desktop app is not running, or if the session does not exist, then remote control, dispatch, and channel-based access all become constrained. So while Claude Code now has some Gateway-like powers, that layer is still not a truly independent, continuously deployable, 24/7 control plane.

Its answer is therefore quite clear:

- by default, the Agent is a tool, not an employee
- remote access can exist, but it is an extension around the CLI core, not the architectural center
- the Gateway is not a foundational assumption but a later layer built in response to real use cases

---

## Hermes Agent: the Gateway is only a lightweight bridge

<div class="protocol-figure">
  <img src="../../../static/agent/chapter8/images/hermes-gateway.png" alt="Hermes Agent lightweight Gateway architecture" />
  <p><sub>Figure 4: Hermes Agent flips OpenClaw's priority order. The AIAgent execution loop is the real center, and the Gateway is only a thin bridge that brings outside messages in.</sub></p>
</div>

### The core is the execution loop, not the Gateway

Hermes Agent nearly inverts OpenClaw's design priorities.

In Hermes, the real center is the AIAgent execution loop itself. Even if you never use the Gateway and only run Hermes in the terminal, it still remains a complete Agent system. The Gateway is simply one more way to connect to it.

That changes where complexity lives:

- without a Gateway, OpenClaw is barely the same system
- without a Gateway, Hermes still fully exists
- therefore Hermes naturally keeps the Gateway thinner, more restrained, and closer to an adapter layer

### It unifies incoming platforms without becoming the orchestration center

Hermes can still connect to many platforms, but it emphasizes normalized message ingestion, session routing, and result push-back rather than turning the Gateway into a heavy control center.

Its flow looks more like this:

```text
Platform message
    ↓
Platform Adapter (normalize message format)
    ↓
Authorization check + session resolution
    ↓
Create or call an AIAgent instance
    ↓
Run the conversation loop
    ↓
Push results back to the original platform
```

The clean part is the separation of responsibilities:

- platform adapters handle translation into one internal shape
- the Gateway core handles authentication, routing, and instance access
- AIAgent handles the actual execution

Because the Gateway does not absorb too much orchestration logic, Hermes can keep the structure relatively clean even as supported platforms increase.

### The cost of that cleanliness: stronger single-Agent boundaries

Of course, this thin Gateway model is not free.

Because it does not act as a true orchestration center, the relationship between one Gateway instance and one Agent instance becomes tighter. If you want a work Agent and a personal Agent fully separated, the natural answer is often to run separate instances rather than to manage both through one shared control plane with flexible routing rules.

But Hermes also extends in an interesting direction: it does not only connect horizontally to message platforms. It can also connect vertically into the development toolchain. Through mechanisms such as ACP, editor context can enter the Agent's input layer as well. That makes the Gateway evolve from a “message bridge” toward a “context aggregation layer.”

<div class="protocol-callout">
  <strong>Hermes' key judgment:</strong> the Gateway is not the system core. Its job is simply to bring the world into the Agent reliably. The true ceiling of the system is still determined by the execution loop.
</div>

---

## The three core tradeoffs behind Gateway design

<div class="protocol-figure">
  <img src="../../../static/agent/chapter8/images/tradeoffs.png" alt="Gateway architecture tradeoffs" />
  <p><sub>Figure 5: OpenClaw, Claude Code, and Hermes Agent diverge across three deep questions: whether the Gateway is core or peripheral, whether the Agent should always stay online, and whether exposure defaults should be open or closed.</sub></p>
</div>

Put together, these routes do not mainly differ in how many platforms they support. Their real disagreements sit inside three architectural tradeoffs.

### Tradeoff 1: is the Gateway the system core or just an entry point?

- <strong>OpenClaw</strong>: the Gateway is the nerve center, carrying orchestration, routing, authentication, and multi-Agent management.
- <strong>Claude Code</strong>: the Gateway is not the starting point of the architecture, but a remote-capability layer added around a CLI tool.
- <strong>Hermes Agent</strong>: the Gateway is intentionally thin, while the execution loop remains the undisputed center.

The heavier the Gateway, the more centralized the system becomes, the more complex configuration grows, and the stronger unified control becomes. The lighter the Gateway, the more independent the Agent core stays, and the easier the system becomes to test, swap, or decompose.

### Tradeoff 2: should the Agent always stay online or only run on demand?

- <strong>OpenClaw</strong> and <strong>Hermes</strong> fit naturally into server-side, always-on deployment.
- <strong>Claude Code</strong> remains far more native to the “works only when the local machine is on” tool model.

Always-on design creates more operational cost and a larger exposure surface, but it buys proactivity. On-demand design is lighter, but it loses much of the agentic behavior that depends on scheduling or continued execution when the user is away.

### Tradeoff 3: should the default be open or closed?

The Gateway is the most direct exposed surface of the system, so the choice between default openness and default refusal has immediate security consequences.

- more open defaults make integration faster but increase deployment risk
- stricter fail-closed defaults raise setup friction but suppress exposure risk at the architecture level

This is not merely a “security option.” It is a projection of system philosophy: do you want the Agent to behave like an experimental utility, or like a continuously operating production system?

<div class="protocol-highlight">
  <p>Gateway design ultimately answers one question: do you want the Agent to be a tool that appears when summoned, or a worker that keeps operating even when you are not looking?</p>
</div>

The three frameworks begin diverging from each other the moment they answer that question differently.

---

## Summary

The most important value of this chapter is not listing which platforms each framework can connect to. It is clarifying the three architectural judgments behind their Gateway designs:

1. <strong>OpenClaw's answer</strong>: the Gateway is an operating-system-like control plane around which multi-channel, multi-Agent, and active scheduling behavior are organized.
2. <strong>Claude Code's answer</strong>: the CLI is the true starting point, and Gateway-like capability is a remote-control extension layered on top later.
3. <strong>Hermes Agent's answer</strong>: the Gateway is only a thin bridge; the AIAgent execution loop is the real center of gravity.
4. <strong>The deepest tradeoff</strong>: this is not about “which platform is supported,” but about whether the Agent is fundamentally a conversation tool, a continuously operating system, or a loop-centered architecture with the thinnest possible entry layer.

If the whole article had to be compressed into one sentence, it would be this: <strong>the design philosophy of the Gateway ultimately determines what an Agent is.</strong>

<style>
.protocol-kicker {
  margin: 0 0 10px;
  text-align: center;
  color: #b56a41;
  font-size: 0.82rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
}

.protocol-subtitle {
  margin: -4px 0 20px;
  text-align: center;
  color: #7c5034;
  font-size: 1.05rem;
  letter-spacing: 0.02em;
}

.protocol-callout,
.protocol-highlight {
  margin: 22px 0 26px;
  padding: 16px 18px;
  border-radius: 18px;
}

.protocol-callout {
  background: linear-gradient(135deg, rgba(255, 245, 238, 0.96), rgba(255, 255, 255, 0.98));
  border: 1px solid rgba(223, 129, 79, 0.22);
  color: #7f4b31;
  box-shadow: 0 10px 24px rgba(179, 93, 55, 0.06);
}

.protocol-callout strong {
  color: #b35e34;
}

.protocol-highlight {
  position: relative;
  background: linear-gradient(135deg, rgba(223, 129, 79, 0.14), rgba(255, 243, 234, 0.92));
  border: 1px solid rgba(223, 129, 79, 0.26);
  box-shadow: 0 14px 28px rgba(164, 86, 49, 0.08);
}

.protocol-highlight::before {
  content: "“";
  position: absolute;
  top: -18px;
  left: 14px;
  font-size: 3rem;
  line-height: 1;
  color: rgba(223, 129, 79, 0.34);
  font-family: Georgia, serif;
}

.protocol-highlight p,
.protocol-callout p {
  margin: 0;
  line-height: 1.85;
}

.protocol-highlight p {
  color: #7b452c;
  font-weight: 600;
}

.protocol-cover,
.protocol-figure {
  margin: 28px auto;
  padding: 14px;
  border-radius: 20px;
  background: linear-gradient(180deg, #fff7f1 0%, #ffffff 100%);
  border: 1px solid rgba(226, 145, 97, 0.26);
  box-shadow: 0 14px 34px rgba(150, 78, 41, 0.08);
  overflow: hidden;
}

.protocol-cover img,
.protocol-figure img {
  display: block;
  width: 100% !important;
  max-height: none !important;
  margin: 0 auto;
  border-radius: 12px;
}

.protocol-cover p,
.protocol-figure p {
  margin: 12px 6px 2px;
  text-align: center;
  color: #8a4c2d;
  font-size: 0.94rem;
  line-height: 1.7;
}

.protocol-meta-card {
  margin: 20px 0 28px;
  padding: 18px 20px;
  background: linear-gradient(135deg, rgba(255, 240, 232, 0.95), rgba(255, 255, 255, 0.98));
  border: 1px solid rgba(223, 129, 79, 0.28);
  border-radius: 18px;
  box-shadow: 0 10px 28px rgba(179, 93, 55, 0.08);
}

.protocol-meta-card ul {
  margin: 0;
  padding-left: 1.1rem;
}

.protocol-meta-card li {
  margin: 0.45rem 0;
  line-height: 1.75;
}

.vp-doc h2 {
  margin-top: 42px;
  padding-left: 14px;
  border-left: 4px solid #df814f;
}

.vp-doc h3 {
  margin-top: 28px;
}

.vp-doc blockquote {
  border-left: 4px solid #df814f;
  background: rgba(255, 241, 234, 0.76);
  border-radius: 0 14px 14px 0;
  padding: 10px 16px;
}

.vp-doc table {
  border-radius: 12px;
  overflow: hidden;
}

.vp-doc tr:nth-child(2n) {
  background-color: rgba(255, 241, 234, 0.42);
}

.dark .protocol-subtitle {
  color: #efc1ab;
}

.dark .protocol-kicker {
  color: #f0b896;
}

.dark .protocol-callout {
  background: linear-gradient(135deg, rgba(88, 42, 24, 0.7), rgba(34, 27, 24, 0.94));
  border-color: rgba(223, 129, 79, 0.22);
  color: #f2d5c7;
}

.dark .protocol-callout strong {
  color: #ffcfb6;
}

.dark .protocol-highlight {
  background: linear-gradient(135deg, rgba(143, 78, 47, 0.36), rgba(46, 33, 29, 0.95));
  border-color: rgba(223, 129, 79, 0.24);
}

.dark .protocol-highlight::before {
  color: rgba(255, 201, 170, 0.28);
}

.dark .protocol-highlight p {
  color: #ffd8c3;
}

.dark .protocol-cover,
.dark .protocol-figure {
  background: linear-gradient(180deg, rgba(82, 37, 24, 0.68), rgba(30, 30, 30, 0.92));
  border-color: rgba(223, 129, 79, 0.26);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.28);
}

.dark .protocol-meta-card {
  background: linear-gradient(135deg, rgba(88, 42, 24, 0.86), rgba(30, 30, 30, 0.95));
  border-color: rgba(223, 129, 79, 0.24);
}

.dark .protocol-cover p,
.dark .protocol-figure p {
  color: #f3cbb8;
}

.dark .vp-doc blockquote {
  background: rgba(110, 53, 30, 0.3);
}

@media (max-width: 768px) {
  .protocol-cover,
  .protocol-figure,
  .protocol-meta-card,
  .protocol-callout,
  .protocol-highlight {
    border-radius: 16px;
  }

  .protocol-cover,
  .protocol-figure {
    padding: 10px;
  }

  .protocol-cover p,
  .protocol-figure p {
    margin-top: 10px;
    font-size: 0.9rem;
    line-height: 1.65;
  }
}
</style>
