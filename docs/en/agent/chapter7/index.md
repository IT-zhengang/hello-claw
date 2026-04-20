# AI Agent Architecture (VII): Skills System Design (OpenClaw, Claude Code, and Hermes Agent Compared)

<p class="protocol-subtitle"><strong>Skills are not just instruction files. They are the mechanism through which an Agent acquires, preserves, and reuses professional experience across tasks.</strong></p>

<div class="protocol-figure">
  <img src="../../../static/agent/chapter7/images/overview.png" alt="Overview of Skills system design" />
  <p><sub>Overview: the real question is not “how to write a Skill file,” but whether Agent experience should come from the community, from the user, or from execution itself.</sub></p>
</div>

<div class="protocol-meta-card">
  <ul>
    <li><strong>Series</strong>: AI Agent Architecture (VII): Skills System Design</li>
    <li><strong>Core question</strong>: where should an Agent's professional experience come from, and how should that experience stay reusable across future work?</li>
    <li><strong>You will see</strong>: OpenClaw's community marketplace, Claude Code's personal knowledge accumulation, and Hermes Agent's automatic skill generation</li>
    <li><strong>For</strong>: readers building Agent workflows who want to understand the deeper logic behind Skills, `SKILL.md`, and reusable execution knowledge</li>
    <li><strong>Reading time</strong>: 15 minutes</li>
  </ul>
</div>

---

## What problem do Skills actually solve?

<div class="protocol-figure">
  <img src="../../../static/agent/chapter7/images/skills-essence.png" alt="The essence of Skills as professional Agent experience" />
  <p><sub>Figure 1: models are generalists, but they do not know your company context, team conventions, or personal operating methods. Skills are how that experience gets loaded into the Agent.</sub></p>
</div>

Language models are natural generalists. They know how to write code, answer questions, and call tools, but they do not automatically know how your team names branches, how your release process works, how you structure status updates, or how you personally solve a recurring class of tasks.

That is exactly where Skills matter.

On the surface, a Skill can look very simple: a Markdown file, or a directory that includes instructions, scripts, templates, and references. The Agent loads it when needed and follows the guidance inside.

But the important question is not what the file looks like. It is this:

<div class="protocol-callout">
  <strong>The real issue:</strong> a Skill is not just “another document.” It is a decision about where Agent expertise comes from, and how that expertise stays reusable over time.
</div>

Mainstream frameworks currently make three very different bets:

- OpenClaw bets on the community: let the people who understand each scenario best publish reusable Skills for everyone else.
- Claude Code bets on the user: the best Skill is the one written by the person who actually understands the project and workflow.
- Hermes Agent bets on the Agent itself: real execution is the best source of experience, so Skills should emerge from completed tasks.

Those three bets shape everything else: ecosystem design, startup speed, safety boundaries, context cost, and long-term evolution.

---

## OpenClaw: outsource experience to the community

<div class="protocol-figure">
  <img src="../../../static/agent/chapter7/images/openclaw-clawhub.png" alt="OpenClaw and the ClawHub Skills marketplace" />
  <p><sub>Figure 2: OpenClaw inherits a large Skills ecosystem through ClawHub. Startup is fast, but the trust boundary expands with the marketplace.</sub></p>
</div>

### ClawHub: the npm model for Agent skills

OpenClaw takes a very direct position: professional knowledge is too distributed to expect every user to write everything from scratch, so the system should provide an open marketplace where scenario-specific experience can be packaged and installed.

That is the role ClawHub plays. Email processing, CRM workflows, code review, data analysis, knowledge operations—users can install prebuilt Skills and get broad capability coverage almost immediately.

This gives OpenClaw its biggest advantage: startup speed.

- You do not need to learn how to write a Skill before you get value.
- You do not need to formalize your own experience first.
- You can search for the scenario and install a reusable answer.

The logic is similar to npm, Homebrew, or a plugin marketplace: modularize experience, standardize it, and let more people reuse it at low cost.

### The price of openness: supply-chain risk

But the community path also comes with a very obvious cost.

When OpenClaw outsources the source of experience to a marketplace, it also expands the trust boundary outward. Installing a Skill means executing logic that originated outside your local environment. If review, signing, isolation, and auditability are weak, a large ecosystem becomes harder to trust safely.

<div class="protocol-highlight">
  <p>Community-driven growth makes Skills scale fastest, but the hidden assumption is not just “the crowd is smart.” It is also “you accept the risk of external experience entering your local environment.”</p>
</div>

That makes OpenClaw compelling for teams that need fast coverage across many task types, but it also means every installed Skill should be treated like a supply-chain decision, not just a convenience feature.

---

## Claude Code: turn your workflow into reusable knowledge

<div class="protocol-figure">
  <img src="../../../static/agent/chapter7/images/claude-write-skills.png" alt="User-authored Skills in Claude Code" />
  <p><sub>Figure 3: Claude Code emphasizes writing down your own methods. A Skill is treated as externalized personal or team experience rather than a marketplace package.</sub></p>
</div>

### The Agent learns your way of working only when you write it down

Claude Code starts from the opposite assumption.

Its view is that the most valuable experience is often not generic knowledge but the highly specific part tied to your repo, your tools, your team conventions, and your preferred operating style. That is why the most accurate Skills often should not come from a public market at all. They should come from the people doing the work.

That logic shows up in the way Claude Code structures `SKILL.md`, references, scripts, templates, and supporting assets: you document the method, attach the tools, add the references, and the Agent can execute using your workflow rather than a generalized one.

This path has clear strengths:

- experience stays close to the real workflow instead of a generic “good enough for many people” abstraction
- the safety boundary is clearer because the source of the Skill is controlled by you or your team
- over time, Skills become an operational playbook and knowledge base for the project

The tradeoff is also clear: the barrier is higher. You have to write, maintain, and curate those Skills yourself.

### Progressive Disclosure: more experience does not have to mean higher context cost

<div class="protocol-figure">
  <img src="../../../static/agent/chapter7/images/progressive-disclosure.png" alt="Claude Code Progressive Disclosure" />
  <p><sub>Figure 4: Claude Code uses Progressive Disclosure to layer Skill loading, so a richer experience library does not automatically mean a more expensive context window.</sub></p>
</div>

One of Claude Code's most important design choices is that it does not inject all experience into context at once. Instead, it uses Progressive Disclosure:

```text
Layer 1 (startup, roughly 100 tokens)
Only the Skill name and description are loaded
The Agent knows what experience is available

Layer 2 (on demand, often under 5,000 tokens)
The full SKILL.md is loaded only when relevant
The Agent follows the detailed instructions

Layer 3 (read from the filesystem directly)
scripts/, templates/, references/, and related assets
These are not injected by default; they are read or executed only when needed
```

This solves a very practical problem: as personal or team Skills grow over time, the system does not have to pay a linear context penalty just to keep the experience library large.

Layer 3 is especially important. Scripts, templates, and reference files can be very large, but they do not need to be pushed into the model context on every run. They can remain available without being permanently “expensive.”

### Skills still matter after compaction

Claude Code also handles the long-session problem more carefully. When context compaction happens, the currently loaded Skills do not simply disappear. Key parts remain attached under a controlled budget.

That means:

- the constraints you spent time encoding do not vanish just because the task gets longer
- the method loaded for the task can keep influencing the execution cycle
- a Skill becomes more than a startup prompt patch; it acts as a durable rules layer during the work itself

---

## Hermes Agent: let Skills grow out of execution itself

<div class="protocol-figure">
  <img src="../../../static/agent/chapter7/images/hermes-self-evolving.png" alt="Hermes Agent automatic Skill generation" />
  <p><sub>Figure 5: Hermes Agent stands out by turning completed execution traces into Skills, then refining those Skills through later runs.</sub></p>
</div>

### The biggest challenge to the usual assumption

Hermes Agent questions something the other two frameworks largely accept: why should Skills be written by humans in the first place?

If an Agent already goes through trial, correction, and completion during a complex task, then maybe the most valuable experience is not the instruction written before the task starts. Maybe it is the reusable method extracted after the task succeeds.

Hermes pushes that idea much further:

- when the Agent finishes a sufficiently complex task, the system extracts the execution pattern
- that pattern is saved as a Skill in the local skills directory
- similar future tasks can load that experience automatically
- if later execution finds a better way, the Skill can be revised again

This is a true self-evolution route. A Skill is no longer a static document maintained by a human. It becomes compressed operational history.

### The hard part is not generation, but quality judgment

The real difficulty of Hermes is not whether the system can produce a document. It is whether the produced artifact is actually worth reusing.

The main challenges cluster around three questions:

1. <strong>Which tasks deserve a Skill?</strong> If the threshold is too low, the system stores noise. If it is too high, valuable repeatable experience gets lost.
2. <strong>At what abstraction level should the method be written?</strong> Too specific, and it only reproduces one run. Too abstract, and it stops being operationally useful.
3. <strong>How is quality controlled?</strong> If the underlying execution was flawed, the resulting Skill may simply preserve a bad pattern as “experience.”

<div class="protocol-callout">
  <strong>Hermes' biggest risk:</strong> self-evolution only works when execution quality is already strong enough. Otherwise, the system may just become better at reinforcing its own mistakes.
</div>

### Shared skills make experience spread across Agents

Another interesting direction in Hermes is that Skills can move beyond the current Agent. Shared directories and community extensions allow knowledge to spread across multiple Agents working in the same environment.

From an engineering perspective, that turns execution history into an organizational experience layer rather than a private memory artifact.

---

## Three bets, three tradeoffs

<div class="protocol-figure">
  <img src="../../../static/agent/chapter7/images/tradeoff-matrix.png" alt="Tradeoff matrix across three Skills approaches" />
  <p><sub>Figure 6: OpenClaw, Claude Code, and Hermes Agent emphasize different priorities across ecosystem speed, experience precision, safety boundaries, and self-evolution.</sub></p>
</div>

Seen together, this is not really a question of which framework is “more advanced.” It is a set of different engineering bets:

| Route | Main source of experience | Biggest strength | Biggest risk | Best fit |
| ---- | ---- | ---- | ---- | ---- |
| OpenClaw | Community marketplace | Fast startup and broad coverage | Higher supply-chain and permission risk | Many task types, rapid capability assembly |
| Claude Code | Personal / team accumulation | Precise experience, strong boundaries, deep customization | Requires deliberate curation effort | Teams that care about quality, safety, and workflow fit |
| Hermes Agent | Automatic generation from execution | Can keep improving over time | Quality control is hardest | Repetitive tasks where long-term training pays off |

That is why the most mature real-world answer is usually not a single choice:

- use community Skills to cover general capability quickly
- use self-authored Skills to lock in core workflows and high-value knowledge
- then let real execution continue producing new reusable patterns over time

<div class="protocol-highlight">
  <p>The future of Skills is probably not choosing between community, personal knowledge, and self-evolution. It is letting all three exist together, then connecting them through stable formats and better experience governance.</p>
</div>

As Skill formats converge toward more open standards, cross-framework reuse becomes increasingly realistic. At that point, a Skill stops being just a feature inside one product and becomes a portable unit of operational knowledge across the broader Agent ecosystem.

---

## Summary

The most important value of this chapter is not teaching one `SKILL.md` syntax. It is clarifying the three design philosophies behind Skills systems:

1. <strong>OpenClaw's answer</strong>: make the community the experience pool, and gain the fastest capability coverage.
2. <strong>Claude Code's answer</strong>: let the user write down their own method, and gain the most precise and controllable workflow memory.
3. <strong>Hermes Agent's answer</strong>: let execution generate the Skill, and gain the possibility of ongoing self-evolution.
4. <strong>The mature direction</strong>: do not blindly choose one side. Let general capability, private experience, and automatic accumulation cooperate inside one engineering system.

If the whole article had to be compressed into one sentence, it would be this: <strong>the essence of Skills design is not “how to write instructions,” but how an Agent should acquire, preserve, and reuse professional experience.</strong>

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
