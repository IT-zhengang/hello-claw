---
title: AI Agent智能体：写在开头
---

AI Agent智能体这一部分，聚焦的是“龙虾真正变成智能体”之后的核心能力。

如果说“构建龙虾”更强调 Runtime、工具、网关、安全沙箱这些底座，那么这一部分更关心的是：

- Agent 如何记忆
- Agent 如何持续协作
- Agent 如何在长周期任务里保持稳定
- Agent 如何从一次次执行中形成经验

这里讨论的，不再只是“系统怎么搭起来”，而是“智能体如何真正长期工作”。

## 你会在这里看到什么

这一目录会逐步收录 Agent 级能力设计相关内容，例如：

- 记忆系统设计
- 多智能体协作
- 自治与反思机制
- 长期任务调度与经验沉淀

当前已上线：

- [第一章 记忆系统设计](./chapter1/index.md)
- [第二章 工具系统设计](./chapter2/index.md)
- [第三章 任务规划与执行循环](./chapter3/index.md)
- [第四章 多 Agent 协作](./chapter4/index.md)
- [第五章 安全与可控性设计](./chapter5/index.md)
- [第六章 MCP vs CLI](./chapter6/index.md)
- [第七章 Skills 系统设计](./chapter7/index.md)
- [第八章 Gateway 架构设计](./chapter8/index.md)

建议阅读顺序：

1. 如果你还没看过 Runtime 与工具底座，先阅读[构建龙虾](/cn/build/)
2. 如果你最关心智能体“为什么会忘、怎么记住、怎么越用越熟”，直接从第一章开始
3. 如果你想理解 Agent 如何把复杂任务拆成可执行步骤，可以继续阅读[第三章 任务规划与执行循环](./chapter3/index.md)
4. 如果你开始关心“一个 Agent 不够用时，团队应该怎么协作”，接着阅读[第四章 多 Agent 协作](./chapter4/index.md)
5. 如果你已经开始把 Agent 放进真实环境，想进一步理解 Prompt Injection、审批机制与沙箱边界，再读[第五章 安全与可控性设计](./chapter5/index.md)
6. 如果你想进一步理解为什么现代 Agent 框架会同时拥抱 CLI 与 MCP，以及它们在产品里的真实分工，继续阅读[第六章 MCP vs CLI](./chapter6/index.md)
7. 如果你想理解 Agent 的专业经验到底该沉淀为社区 Skill、个人 Skill，还是执行中自动生长出来，继续阅读[第七章 Skills 系统设计](./chapter7/index.md)
8. 如果你想进一步理解 Agent 和外部世界之间的入口层，为什么会反过来决定整个系统的工作模式，继续阅读[第八章 Gateway 架构设计](./chapter8/index.md)
9. 如果你想继续把这些系统能力落到主流框架实现，可以接着阅读[LangChain深度技术指南](/cn/langchain/)
