---
title: AI Agent 架构设计（五）：安全与可控性设计
---

# AI Agent 架构设计（五）：安全与可控性设计（OpenClaw、Claude Code、Hermes Agent 对比）

<p class="guard-subtitle"><strong>从“Agent 越来越能干”到“Agent 依然可控”：拆解三个主流框架如何处理提示注入、权限审批、沙箱隔离与安全边界</strong></p>

<div class="guard-cover guard-figure">
  <img src="../../../static/agent/chapter5/images/cover.png" alt="安全与可控性设计封面图" />
  <p><sub>导图：先用一张总览图把“自主性”和“控制权”的矛盾摆在台面上，再进入三种框架的安全设计对比</sub></p>
</div>

<div class="guard-meta-card">
  <ul>
    <li><strong>系列</strong>：AI Agent 架构设计（五）：安全与可控性设计</li>
    <li><strong>目标</strong>：从架构层面理解三个框架如何平衡 Agent 自主性和人的控制权，以及 Prompt Injection 防御、审批机制、沙箱设计背后的工程取舍</li>
    <li><strong>适合</strong>：对 Agent 底层设计感兴趣，想真正理解“为什么这样设计”的读者</li>
    <li><strong>预计阅读</strong>：15 分钟</li>
  </ul>
</div>


---

## 为什么安全是 Agent 架构的核心问题？

<div class="guard-figure">
  <img src="../../../static/agent/chapter5/images/why-security.png" alt="为什么安全是 Agent 架构的核心问题" />
  <p><sub>图 1：前四篇讨论的是 Agent 如何变强，这一篇转向另一个更关键的问题——变强之后，如何确保它依然可控</sub></p>
</div>

前四篇讲的——记忆、工具、执行循环、多 Agent 协作——都在回答一个问题：**Agent 怎么变得更能干？**

这篇要回答的问题是：**Agent 变强之后，怎么防止它做它不该做的事？**

这个问题比普通软件的安全问题更难，因为 Agent 有一个普通软件没有的特性：**它的行为由语言模型决定，而语言模型会处理大量来自外部的文本——文件、网页、API 响应、用户消息。**

任何进入模型上下文的文本，都可能包含恶意指令。攻击者不需要破解系统，只需要让模型读到一段精心设计的文字。

OWASP 在 2026 年发布的《Agent 应用十大安全风险》里，把这类攻击（Agent Goal Hijacking，Prompt Injection）列为第一位。

2026 年已经有不少真实案例：代码注释里藏着的恶意指令让 Agent 泄露 SSH 密钥；恶意 Markdown 文件让 Agent 发送未经授权的邮件；GitHub 仓库里的 README 劫持了 Agent 的操作权限。

**安全不是可选项，而是 Agent 架构的基础设施。** 三个框架对这个问题，给出了截然不同的防御纵深设计。

---

## Agent 安全的四个核心战场

<div class="guard-figure">
  <img src="../../../static/agent/chapter5/images/threat-surface.png" alt="Agent 安全的四个核心战场" />
  <p><sub>图 2：真正需要防御的，不只是单一漏洞，而是从输入、凭证、权限到供应链的完整攻击面</sub></p>
</div>

在拆解三个框架之前，先明确 Agent 安全要防的四类攻击：

- **Prompt Injection（提示注入）**：攻击者把恶意指令嵌入 Agent 会处理的内容里，例如文件、网页、工具返回值，让 Agent 把这些文字当成合法命令执行。
- **凭证泄漏**：Agent 执行代码或访问外部服务时，意外把 API Key、SSH 密钥等凭证暴露给攻击者控制的服务器。
- **权限提升**：利用 Agent 已经拥有的工具访问能力，执行用户本没有明确授权的操作，比如读取工作目录之外的系统文件，或者执行删除命令。
- **供应链攻击**：通过恶意 Skills 插件、MCP 服务器、外部工具包，把恶意代码带入 Agent 的执行环境。

三个框架的安全架构，本质上都在这四个战场上构筑防线，只是深度和策略各不相同。

---

## OpenClaw：最大开放，安全靠配置

<div class="guard-figure">
  <img src="../../../static/agent/chapter5/images/openclaw-security.png" alt="OpenClaw 安全架构示意图" />
  <p><sub>图 3：OpenClaw 把“能力开放”放在前面，安全能力并不缺席，但大量依赖用户显式配置与约束</sub></p>
</div>

### 设计哲学：信任用户，安全边界由用户定义

OpenClaw 的安全哲学很像 Unix：**给 Agent 最大的能力，让用户自己决定边界在哪里。**

这个哲学的代价，在 2026 年初暴露得很清楚：大量实例直接暴露在公网，部分部署甚至没有身份认证；开放技能市场里，也出现了同时夹带 Prompt Injection 载荷和传统恶意代码的恶意 Skill。

这些并不一定是传统意义上的“实现缺陷”，而更像是“默认开放”这一路线在真实用户环境里的自然后果。

### 权限模型：六层级联，但默认宽松

OpenClaw 其实有一套相当完整的六层级联权限策略：全局、模型提供商、Agent、群组、沙箱、子 Agent。

问题不在于有没有能力，而在于**默认值偏宽松**：默认没有 Shell 命令白名单，没有审批清单，也没有严格的凭证访问限制。用户从零开始安装后，往往拿到的是一个对本机拥有近乎完整权限的 AI Agent。

**把安全配置的责任交给用户，意味着最终安全质量会严重依赖用户本人的安全意识。** 当多数用户并不了解 Agent 风险时，这种设计会自然放大隐患。

### 供应链风险：ClawHub 是开放的

ClawHub 是 OpenClaw 的技能市场，任何人都可以上传 Skill。对于生态繁荣来说，这是优势；但从安全角度看，用户安装 Skill 的动作，本质上接近于执行未知第三方代码。

原文特别提到，恶意 Skill 不只会窃取 API Key，还可能把恶意内容写入 `MEMORY.md` 或 `SOUL.md`，从一次执行扩展成跨 Session 的持久化控制。这也是 Agent 时代供应链攻击最值得警惕的地方：**污染的不只是当前运行过程，还包括未来的“记忆”和“人格”。**

---

## Claude Code：纵深防御，沙箱是核心

<div class="guard-figure">
  <img src="../../../static/agent/chapter5/images/claude-code-sandbox.png" alt="Claude Code 沙箱与纵深防御示意图" />
  <p><sub>图 4：Claude Code 的关键判断是——不要把安全希望寄托在用户配置上，而要把安全边界编码进系统与操作系统原语</sub></p>
</div>

### 设计哲学：把安全编码进架构，不依赖用户配置

Claude Code 的出发点和 OpenClaw 明显不同：**用户不应该先成为安全专家，才能相对安全地使用 Agent。**

这意味着安全控制不能只是“提供给你一些可选配置”，而必须内建在系统架构里，让默认路径就尽可能安全。

### 沙箱：OS 级隔离

Claude Code 的沙箱是安全体系里最关键的一层。它基于 OS 级原语实现两类核心隔离：

- **文件系统隔离**：Agent 只能读写当前工作目录，无法访问系统文件、家目录的其他部分以及 SSH 密钥等敏感内容。更重要的是，这种限制会自动传递给 Claude Code 派生出来的子进程。
- **网络隔离**：所有网络请求必须经过沙箱外的代理，由代理决定哪些域名可以访问。Agent 不能直接连接未知主机。

这两层隔离的价值在于：**即使 Prompt Injection 成功，攻击者能造成的破坏也会被限制在沙箱边界内。**

它不能读取宿主机上的高价值文件，也不能随意把数据发往任意服务器。原文提到，Anthropic 的内部测试甚至发现：把安全边界做得更硬之后，需要用户频繁确认的操作反而变少了。换句话说，**更强的默认隔离不一定更烦人，反而可能减少“处处问你要不要继续”的打扰。**

---

## Hermes Agent：保守默认值 + 多层扫描 + 容器隔离

<div class="guard-figure">
  <img src="../../../static/agent/chapter5/images/hermes-defense.png" alt="Hermes Agent 多层安全防御示意图" />
  <p><sub>图 5：Hermes Agent 更强调“默认保守”，并把防御前移到上下文注入之前，同时把最终隔离边界下推到容器层</sub></p>
</div>

### 设计哲学：从保守出发，主动发现风险

Hermes Agent 和 OpenClaw 的路线几乎相反：**默认保守，逐步开放，每个高风险能力都要显式声明。**

这个路线会让初始配置更复杂，但它把系统的起点设在“默认不信任”，而不是“默认放行”。

### 上下文文件扫描：在注入发生前拦截

Hermes Agent 有一个很有辨识度的机制：**在上下文文件真正进入系统提示之前，先做 Prompt Injection 扫描。**

像 `AGENTS.md`、`SOUL.md` 这类会被注入上下文的文件，不是读到就直接交给模型，而是先经过扫描器检查；写入 `MEMORY.md` 和 `USER.md` 的内容也会走类似流程。

这是一种明显前移的防御思路：不是等恶意提示混进模型上下文之后再让模型“自己抵抗”，而是在它进入上下文之前就尽可能拦下来。

### 容器后端：把安全边界下推到基础设施

Hermes Agent 的另一层关键设计，是把隔离进一步下推到容器层。原文提到的 Docker 后端会结合只读根文件系统、Capabilities 丢弃、PID 限制和命名空间隔离等手段，把破坏面锁在容器内部。

一个很有意思的架构决策是：**当运行在 Docker、Modal、Daytona 这类隔离后端时，某些危险命令的审批检查可以减少甚至跳过。**

原因并不是“这些命令突然不危险了”，而是**真正的安全边界已经由基础设施承担**。如果容器本身已经把宿主机隔离开，应用层就不需要重复做同样强度的拦截。

这也说明了一个重要观点：应用层安全常常依赖模式匹配和规则判断，可能被绕过；而基础设施层的隔离更接近操作系统和运行时约束，通常更难被语言层面的攻击突破。

---

## Agent 安全设计的核心取舍

<div class="guard-figure">
  <img src="../../../static/agent/chapter5/images/tradeoffs.png" alt="Agent 安全设计核心取舍" />
  <p><sub>图 6：真正的架构难点，不是“懂不懂安全”，而是在开放性、能力、体验和约束之间如何做取舍</sub></p>
</div>

### 取舍一：默认开放，还是默认保守？

OpenClaw 选择默认开放，优势是上手快、能力释放充分，代价是风险更多暴露给最终用户承担。

Hermes Agent 选择默认保守，优势是起点更稳，代价是配置复杂度更高。

这不是单纯的设计偏好，而是在回答一个更根本的问题：**你的产品是不是假设用户天然懂安全？** 如果目标用户并不是安全专家，那么“默认保守”往往是更负责任的起点。

### 取舍二：应用层安全，还是基础设施层安全？

OpenClaw 的安全更多停留在应用层配置与提示层约束；Claude Code 把隔离下推到操作系统原语；Hermes Agent 进一步强调容器层边界。

一个清晰的判断是：**越靠近基础设施层的安全边界，通常越难被 Prompt Injection 这类语言层攻击绕过。** 模型可以被文字欺骗，但操作系统不会因为一段提示词就撤销文件系统隔离。

### 取舍三：安全和能力之间的张力

沙箱会让 Agent 更安全，但也会限制它访问系统级工具、管理系统服务或操作更大的宿主机环境。

这没有完美解法。更稳妥的实践通常是：**先在最严格的沙箱里运行，只有在确定能力受限且确有必要时，再逐步放开；而不是从宽松开始，等出问题后再补规则。**

原文在这里也给出了整个系列的五层结构总结：

```text
记忆系统     -> 状态怎么存、取、管
工具系统     -> 能力怎么扩展、权限怎么约束
执行循环     -> 任务怎么规划、执行、从错误里恢复
多 Agent     -> 多个 Agent 怎么分工、通信、避免互相添乱
安全可控性   -> 自主性和控制权怎么共存
```

---

## 小结

五篇看下来，这个系列已经把 Agent 架构里最关键的几层能力串起来了：记忆、工具、执行、多 Agent，以及最终的安全与可控性。

- **OpenClaw** 代表的是“最大开放，安全靠用户配置”的路线。
- **Claude Code** 更强调“把安全编码进架构”，靠操作系统级沙箱形成纵深防御。
- **Hermes Agent** 则走“默认保守 + 前置扫描 + 容器隔离”的组合路线。

没有哪一种方案可以在所有场景里绝对最优。真正决定设计取舍的，始终是你的任务类型、用户画像、可接受风险和工程投入。

但有一件事是共同的：**Agent 变强的速度，远快于我们理解如何安全使用它的速度。**

建立安全意识，从理解架构开始。

<style>
.guard-subtitle {
  margin: -4px 0 20px;
  text-align: center;
  color: #7c5034;
  font-size: 1.05rem;
  letter-spacing: 0.02em;
}

.guard-cover,
.guard-figure {
  margin: 28px auto;
  padding: 14px;
  border-radius: 20px;
  background: linear-gradient(180deg, #fff7f1 0%, #ffffff 100%);
  border: 1px solid rgba(226, 145, 97, 0.26);
  box-shadow: 0 14px 34px rgba(150, 78, 41, 0.08);
  overflow: hidden;
}

.guard-cover img,
.guard-figure img {
  display: block;
  width: 100% !important;
  max-height: none !important;
  margin: 0 auto;
  border-radius: 12px;
}

.guard-cover p,
.guard-figure p {
  margin: 12px 6px 2px;
  text-align: center;
  color: #8a4c2d;
  font-size: 0.94rem;
  line-height: 1.7;
}

.guard-meta-card {
  margin: 20px 0 28px;
  padding: 18px 20px;
  background: linear-gradient(135deg, rgba(255, 240, 232, 0.95), rgba(255, 255, 255, 0.98));
  border: 1px solid rgba(223, 129, 79, 0.28);
  border-radius: 18px;
  box-shadow: 0 10px 28px rgba(179, 93, 55, 0.08);
}

.guard-meta-card ul {
  margin: 0;
  padding-left: 1.1rem;
}

.guard-meta-card li {
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

.dark .guard-subtitle {
  color: #efc1ab;
}

.dark .guard-cover,
.dark .guard-figure {
  background: linear-gradient(180deg, rgba(82, 37, 24, 0.68), rgba(30, 30, 30, 0.92));
  border-color: rgba(223, 129, 79, 0.26);
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.28);
}

.dark .guard-meta-card {
  background: linear-gradient(135deg, rgba(88, 42, 24, 0.86), rgba(30, 30, 30, 0.95));
  border-color: rgba(223, 129, 79, 0.24);
}

.dark .guard-cover p,
.dark .guard-figure p {
  color: #f3cbb8;
}

.dark .vp-doc blockquote {
  background: rgba(110, 53, 30, 0.3);
}

@media (max-width: 768px) {
  .guard-cover,
  .guard-figure,
  .guard-meta-card {
    border-radius: 16px;
  }

  .guard-cover,
  .guard-figure {
    padding: 10px;
  }

  .guard-cover p,
  .guard-figure p {
    margin-top: 10px;
    font-size: 0.9rem;
    line-height: 1.65;
  }
}
</style>
