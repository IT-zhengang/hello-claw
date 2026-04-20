

# AI Agent Architecture (VI): MCP vs CLI (OpenClaw, Claude Code, and Hermes Agent Compared)

<p class="protocol-subtitle"><strong>If an Agent can already execute commands directly, do we still need an extra MCP layer? This chapter breaks down one of the hottest Agent debates of 2026.</strong></p>

<div class="protocol-figure">
  <img src="../../../static/agent/chapter6/images/overview.png" alt="MCP vs CLI overview" />
  <p><sub>Overview: the real question is not “which side is more advanced,” but when an Agent should prefer a protocol layer versus direct command execution.</sub></p>
</div>

<div class="protocol-meta-card">
  <ul>
    <li><strong>Series</strong>: AI Agent Architecture (VI): MCP vs CLI</li>
    <li><strong>Core question</strong>: if an Agent already knows how to execute Shell commands, why does MCP still remain central in mainstream frameworks?</li>
    <li><strong>You will see</strong>: token cost, authentication boundaries, tool discovery, and how OpenClaw, Claude Code, and Hermes Agent answer the problem differently</li>
    <li><strong>For</strong>: readers interested in Agent internals who want to understand the architectural reasoning behind each design</li>
    <li><strong>Reading time</strong>: 15 minutes</li>
  </ul>
</div>



---

## First, what is this debate really about?

<div class="protocol-figure">
  <img src="../../../static/agent/chapter6/images/why-debate.png" alt="Why the MCP vs CLI debate is heating up" />
  <p><sub>Figure 1: this is not just a taste argument. It is about token cost, integration shape, and the right execution interface for different Agent tasks.</sub></p>
</div>

<div class="protocol-callout">
  <strong>Start with the core idea:</strong> this chapter is not about “CLI replacing MCP” or “MCP replacing CLI,” but about which interface should lead in which Agent scenario.
</div>

In 2026, one argument in the Agent world has grown steadily louder:

**Should we use MCP or CLI?**

Perplexity's CTO said publicly that the company had started lowering MCP's priority internally. YC CEO Garry Tan also argued that MCP consumes too much context budget and comes with extra authentication complexity, and even mentioned building a CLI substitute in about 30 minutes. Anti-MCP sentiment has also been growing on Hacker News.

At the same time, OpenClaw founder Peter Steinberger posted a line on X that spread widely: **“If the Agent can already run commands directly, why add one more protocol layer?”** He then built MCPorter, a tool that converts MCP servers into CLI tools.

So this debate is not really about fashion or status. It touches a very real architectural problem.

---

## What is MCP, and what is CLI?

**CLI (command-line interface tools)** means commands like `git status`, `gh pr list`, or `docker ps`. The Agent runs those commands in the terminal, reads the output, and continues its work.

Because language models have already seen huge amounts of command-line usage during training, they often know how to use these tools naturally. The biggest advantage is simple: **no extra integration layer is required.**

**MCP (Model Context Protocol)** is an open standard introduced by Anthropic to define a unified way for Agents to communicate with external tools. Tool providers package their capabilities as MCP servers, and the Agent discovers them through `tools/list` and invokes them through `tools/call`.

In other words, MCP provides a standardized plug shape for tools. In theory, any tool that follows the MCP standard can be connected to any Agent that supports MCP.

<div class="protocol-highlight">
  <p>CLI is closer to a toolbox the model already knows how to use, while MCP is closer to an external capability bus built for discovery, authentication, and management.</p>
</div>

---

## Why this debate appeared: a real token-cost problem

<div class="protocol-figure">
  <img src="../../../static/agent/chapter6/images/token-cost.png" alt="Token cost comparison between MCP and CLI" />
  <p><sub>Figure 2: one of the clearest triggers for the debate is the context overhead difference between MCP and CLI on the same practical task.</sub></p>
</div>

Scalekit published benchmark results that made the issue very concrete: for the same GitHub task, MCP and CLI can have dramatically different token costs.

Why is the gap so large?

A GitHub MCP server may expose 43 tools. Once the Agent connects, the full schema for all 43 tools—names, parameters, descriptions, usage patterns—gets injected into context. Whether the task actually needs those tools or not, they already occupy context space.

For a simple task like checking the state of one PR, the Agent may only use one or two tools, but it still carries the schema for the other 41 the whole time.

If the Agent uses CLI instead, it can run something like `gh pr view 123 --json title,state` and finish with only a few hundred tokens. It does not even need a tool-discovery step, because the model has likely already seen the command pattern during training.

**That is the MCP token tax.**

The more MCP servers you attach, the heavier the tax becomes. Some people measured setups with four MCP servers connected at once—GitHub, a database, Microsoft Graph, and Jira—and found that tool schema alone could consume 150,000+ tokens before the real task had even started.

<div class="protocol-callout">
  <strong>Quick takeaway:</strong> when tasks are short, frequent, and already familiar to the model, CLI often wins on cost first. MCP is not unusable; it simply carries heavier default context overhead.
</div>

---

## So is MCP useless? No.

That conclusion is too fast. CLI clearly wins in personal developer workflows, but it loses in another class of scenarios.

**The core limitation of CLI is that it assumes your credentials and your permissions.**

When an Agent uses CLI, it uses the identity already configured on the local machine: your GitHub token, your AWS credentials, your database password. For your own workflow, that may be perfectly fine.

But if you are building a product and your users need the Agent to access *their* GitHub, *their* Salesforce, or *their* workspace, then “run CLI with my credentials” no longer works.

In that case, what you actually need is:

- per-user OAuth authentication
- user-level permission isolation
- structured audit logs
- multi-tenant access control

Those are all areas where MCP is naturally stronger. CLI does not give you that abstraction by default.

There is also another important scenario: **some systems simply do not have a CLI at all.**

Salesforce has no CLI for this purpose. Workday does not. Greenhouse does not. Many SaaS systems only expose APIs, and often complex OAuth-based APIs. In such cases, MCP is not just a nicer option; it is the only realistic path.

---

## The real conclusion: do not pick a camp, split by scenario

The most useful industry consensus is not “who won,” but *where each interface belongs*.

**CLI is better for:**

- tools the model has already seen heavily in training, such as `git`, `gh`, `aws`, and `docker`
- local execution with no multi-user identity requirement
- high-frequency, lightweight operations where per-call overhead must stay low
- loop-heavy batch workflows, where CLI can directly script repeated operations while MCP would require many separate tool calls

**MCP is better for:**

- SaaS integrations such as Salesforce or Workday, where no CLI path exists
- product scenarios that require OAuth and per-user identity
- compliance-sensitive environments that need audit logs and permission isolation
- tool-discovery scenarios, where the Agent does not already know what capabilities are available

**The most mature answer is not either-or. It is using both and selecting by task.**

Claude Code is a good example: local file operations and code execution go through CLI, SaaS integrations go through MCP, and Skills provide the layer that unifies both paths so the Agent does not need to care about the transport shape underneath.

<div class="protocol-highlight">
  <p>The mature Agent answer is not choosing a side, but letting CLI and MCP each handle the work they are structurally best at, then hiding the split behind one abstraction layer.</p>
</div>

---

## How the three frameworks position themselves

<div class="protocol-callout">
  <strong>Read the three frameworks through this lens:</strong> OpenClaw leans toward inheriting the MCP ecosystem, Claude Code layers CLI and MCP in parallel, and Hermes Agent pushes MCP into a bidirectional capability interface.
</div>

### OpenClaw: MCP as the main ecosystem inheritance layer

<div class="protocol-figure">
  <img src="../../../static/agent/chapter6/images/openclaw-mcp.png" alt="OpenClaw MCP path" />
  <p><sub>Figure 3: OpenClaw primarily inherits the external MCP ecosystem. Protocol-level extension is the main path, while CLI remains more of a supplement.</sub></p>
</div>

OpenClaw's reasoning for adopting MCP is straightforward: **there are already 5,800+ MCP servers available externally, so there is no reason to rebuild the wheel.**

Configuration is simple too: add an `mcpServers` block to `openclaw.json`, connect to a server, and the Agent can use that server's tools. GitHub, Postgres, Slack, Notion—everything can be plugged in.

The weakness is that OpenClaw does not do demand-driven schema loading. The more MCP servers you attach, the more tool schema ends up in context, and token consumption rises linearly. Community practice suggests that once you go beyond five or six MCP servers, context pressure starts becoming noticeable.

CLI support exists mainly through the Skills system: wrap command-line behavior inside a Skill, let the Agent call the Skill, and let the Skill run the actual commands. That path works, but it has not yet become as unified a discovery and integration surface as MCP.

**Summary: MCP is OpenClaw's primary expansion path, CLI is supplementary, ecosystem scale is the strength, and token efficiency is the obvious weakness.**

### Claude Code: use both, with Skills as the unifying layer

<div class="protocol-figure">
  <img src="../../../static/agent/chapter6/images/claude-code-layer.png" alt="Claude Code CLI and MCP layering" />
  <p><sub>Figure 4: Claude Code does not choose between CLI and MCP. It layers them: CLI does the work, MCP extends capabilities, and Skills unify the interface.</sub></p>
</div>

Claude Code offers the most systematic architectural answer among the three.

**CLI is the default execution path.** Claude Code is fundamentally an Agent that can run terminal commands directly. File operations, code execution, and Git interactions all prefer Shell first. That is the lightest and most efficient route.

**MCP is the structured extension layer.** Claude Code also adds a key optimization when connecting MCP servers: **lazy loading (`defer_loading: true`)**. At session start, only tool names are loaded. The full schema is only loaded when actually needed. That turns MCP's token tax from “pay everything upfront” into “pay on demand.”

It also includes tool search, so the Agent can locate relevant tools semantically rather than walking the entire tool list every time.

**Skills are the unified interface layer.** Whether the underlying path is CLI or MCP, the Agent sees it as a Skill invocation. That abstraction hides transport details and makes it easier to switch between both paths for the same task.

Source analysis also suggests that Claude Code's built-in tools (file I/O, Shell execution) and MCP tools live inside one common registry with unified permission checks and schema validation. Even Computer Use is implemented as `@ant/computer-use-mcp`, which shows that Anthropic did not build a separate bespoke path for it.

**Summary: CLI does the work, MCP expands the system, Skills unify the surface, and Claude Code makes the three-layer split the clearest.**

### Hermes Agent: both an MCP client and an MCP server

<div class="protocol-figure">
  <img src="../../../static/agent/chapter6/images/hermes-mcp.png" alt="Hermes Agent bidirectional MCP architecture" />
  <p><sub>Figure 5: Hermes Agent stands out by not only consuming MCP tools, but also exposing itself as an MCP server so other AI tools can access its memory and history.</sub></p>
</div>

Hermes Agent approaches MCP from a more unusual angle: **it is not only an MCP client; it can also act as an MCP server itself.**

With `hermes mcp serve`, Hermes can expose its session history and memory to other MCP clients. Claude Desktop, VS Code, and Cursor can all query Hermes through the MCP protocol. That means Hermes's memory is not just for itself; it can become part of a broader multi-tool AI environment.

Hermes also includes ACP (Agent Communication Protocol) for two-way editor integration. The editor can send the current file and cursor location into Hermes, and Hermes can use that context to reason more accurately about the task.

On the safety side, Hermes isolates environment variables for MCP subprocesses. Sensitive host credentials are not passed into MCP server processes by default. If a given server needs a specific environment variable, that requirement must be declared explicitly in a Skill.

CLI also exists in Hermes, supported through six execution backends for local and remote command-line execution, but it does not become the main discovery interface the way MCP does.

**Summary: bidirectional MCP participation is Hermes Agent's signature trait, its security posture is the most conservative of the three, and CLI is present but not the central extension route.**

---

## The real answer behind the debate

MCP vs CLI is not an either-or ideological choice. It is fundamentally a **division-of-labor question across different scenarios**.

A one-sentence summary of the emerging consensus would be:

> **CLI handles tools the model already knows; MCP handles tools that must be discovered and authenticated.**
>
> For personal developer workflows, CLI is faster and cheaper. For user-facing products, MCP solves multi-user authentication problems that CLI does not solve naturally. And for SaaS systems with no CLI at all, MCP becomes the only realistic option.

The most mature Agent architectures—Claude Code is the clearest example—have already resolved this internally: CLI and MCP run in parallel, and Skills provide the unified wrapper so the Agent does not need to care which path is used underneath.

This debate will probably continue in the community for a long time. But in product architecture, the answer has already started to appear.

<div class="protocol-highlight">
  <p>CLI handles tools the model already knows; MCP handles tools that must be discovered and authenticated. That is less a slogan than the engineering split mainstream Agent frameworks are converging toward.</p>
</div>

---

## Summary

The real value of this article is not in choosing a side for CLI or MCP, but in reframing the discussion as a practical architecture question:

1. **Why CLI wins many developers over**: it is light, fast, cheap, and naturally aligned with what the model already knows.
2. **Why MCP still matters deeply**: it solves multi-user authentication, SaaS integration, permission isolation, and tool discovery in ways CLI does not naturally cover.
3. **Where the three frameworks differ**: OpenClaw leans harder on inheriting the MCP ecosystem, Claude Code offers the most mature CLI/MCP/Skills layering, and Hermes Agent turns MCP into a bidirectional capability layer.
4. **What the most mature answer looks like**: not choosing one side, but letting CLI and MCP coexist behind a unified abstraction.

If the whole chapter had to be compressed into one sentence, it would be this: **MCP vs CLI is not a route war, but a division-of-labor problem about choosing the right tool interface for the right Agent task.**

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
