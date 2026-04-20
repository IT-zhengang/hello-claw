---
name: hello-claw-article-publisher
description: "将现有 Markdown 草稿、专题文档或已抓取文章整理并发布到 hello-claw 文档站。适用于新增章节、迁移文章、保留原文与图片、本地化远程图片、同步中英文结构、更新 VitePress 导航与 README，并执行 docs build 校验。If the source is still a remote webpage that must be crawled first, prefer `hello-claw-web-article-publisher`."
---

# Hello Claw Article Publisher

你正在 `hello-claw` 项目中执行“文章整理与发布”工作。这个 Skill 的目标不是只改一篇 Markdown，而是把文章稳定地接入 `hello-claw` 的文档体系、目录结构、导航、样式和发布校验流程中。

## 何时使用

当用户提出以下类型的请求时，应优先使用此 Skill：

- 将外部 Markdown / 草稿 / mds 文档接入 `hello-claw`
- 新增或迁移文章到某个知识目录（如“构建龙虾”“龙虾大学”“AI Agent智能体”）
- 保留原文内容与图片，同时做站点适配
- 将外链图片下载到本地，修复文档站无法展示的问题
- 为章节补齐中英文结构、导航、README、首页入口
- 对文章做视觉优化，使其更符合公众号长文的阅读感
- 发布前执行 `npm run docs:build` 做完整校验

更适合本 Skill 的输入是：

- 本地 Markdown / 草稿
- 已经抓取好的网页 Markdown
- 已经下载好的图片和附件

如果用户给的是一个远程网页链接，并且目标是“直接接入 hello-claw”，优先使用整合型 Skill：`hello-claw-web-article-publisher`。

如果上游流程会生成临时 payload JSON，建议在转换为 Markdown 成功后立即删除，不把这类中间文件留在仓库或 `Downloads` 中。

如果只是小范围错字修正或单一段落改写，不需要使用这个 Skill。

## 项目级原则

1. **先确定归属目录，再落文档**
   - `docs/cn/` 与 `docs/en/` 应保持结构镜像
   - 顶层栏目应和已有目录风格一致，如 `adopt/`、`build/`、`university/`、`agent/`、`llm/`
2. **优先保留用户原文**
   - 若用户强调“保留原文”“保留图片”“内容不变”，先保留内容，再做样式与结构适配
3. **远程图片默认本地化**
   - 外链图片在文档站经常受防盗链、权限或热链失效影响
   - 优先下载到 `docs/static/.../images/` 共享静态目录，再改成本地相对路径
   - 中英文镜像文章默认引用同一份图片，不再分别保存到 `docs/cn/.../images/` 与 `docs/en/.../images/`
4. **目录、导航、首页入口要同步**
   - 文章接入不只是一篇 `index.md`，还要同步更新 `docs/.vitepress/config.mts`、首页、README 等入口
5. **发布前必须构建校验**
   - 最低标准是运行 `npm run docs:build`

## 标准工作流

### 第一步：理解来源与目标

先确认以下信息：

- 源文档路径是什么
- 用户希望接入到哪个目录
- 是否要求保留原文、保留图片、保留结构
- 是否需要同步英文页
- 是否涉及新增顶层栏目或章节迁移

如果用户没有明确目标目录，先根据主题判断：

- Runtime、工具、网关、安全 → `build/`
- 真实场景案例 → `university/`
- Agent 能力设计（记忆、协作、自治） → `agent/`
- 模型底层、上下文、推理链路 → `llm/`

### 第二步：创建目标目录结构

对 `hello-claw` 中的新文章，正文与共享图片优先使用如下结构：

```text
hello-claw/docs/cn/<section>/chapterX/index.md
hello-claw/docs/en/<section>/chapterX/index.md
hello-claw/docs/static/<section>/chapterX/images/
```

如果是顶层栏目导言页，则使用：

```text
hello-claw/docs/cn/<section>/index.md
hello-claw/docs/en/<section>/index.md
```

补充规则：

- 如果文章位于目录入口页，例如 `docs/cn/university/email-assistant/index.md`，共享图片目录应为 `docs/static/university/email-assistant/images/`
- 如果文章是扁平文件而不是目录入口页，优先参考同目录现有结构；如无既有约定，再按“栏目/文章名/images”创建共享目录
- 对已有历史目录，不要为了统一而强行搬迁语言专属图片；只有中英文共用同一内容的图片才放进 `docs/static/`

### 第三步：处理正文内容

#### A. 保留原文模式

若用户明确要求保留原文：

- 直接复制原文到目标 `index.md`
- 尽量不改动标题层级与正文结构
- 只做必要的相对路径修正、图片本地化和轻量样式优化

#### B. 适配重写模式

若用户没有要求保留原文：

- 可以按 `hello-claw` 的教学文风进行重写
- 但要保留核心观点、图表逻辑和章节结构

### 第四步：本地化图片

如果文中有远程图片：

1. 根据文章路径，在 `docs/static/.../images/` 下创建共享图片目录
2. 使用 `curl -L` 下载资源到本地
3. 将正文中的远程链接改为指向 `docs/static` 的相对路径
4. 中英文镜像目录引用同一份图片，不要额外复制一份到英文目录

命名建议：

- 使用语义化 kebab-case，如 `memory-overview.png`
- 同一文章图片命名风格统一

示例：

```text
文章：
docs/cn/agent/chapter3/index.md
docs/en/agent/chapter3/index.md

共享图片：
docs/static/agent/chapter3/images/cover.png

正文引用：
../../../static/agent/chapter3/images/cover.png
```

### 第五步：做 hello-claw 风格适配

需要优先检查这些位置：

- `docs/.vitepress/config.mts`
- `docs/cn/index.md`
- `docs/en/index.md`
- `README.md`
- `README_EN.md`
- `README_JA.md`

常见适配动作：

- 新增顶部导航入口
- 新增 sidebar 分组与章节链接
- 在首页“项目包含几大核心模块”处补齐栏目说明
- 在 README 的目录表中补齐新章节/新目录
- 需要时给旧入口页增加“内容已迁移”说明

### 第六步：优化视觉样式

如果文章来自公众号或偏长文，允许做轻量样式增强，但要遵守以下约束：

- 不改变正文事实含义
- 只增强封面图、信息卡、图卡、引用块、表格、标题层级
- 样式优先局部写在当前文章尾部 `<style>` 中，避免污染全站
- 风格上偏“公众号长文”：暖色调、卡片感、留白清晰、图文节奏明显

### 第六步补充：专题系列页的统一模式

如果用户发布的是**连续专题**而不是单篇文章（例如 LangChain、Agent、LLM 等“第 1～N 篇”系列），优先把它当成一个系列来统一处理，而不是逐篇孤立接入。

推荐做法：

1. **导读页与章节页分开设计**
   - 导读页（如 `docs/cn/langchain/index.md` / `docs/en/langchain/index.md`）保留完整系列导航
   - 章节页保留统一 Hero，但系列导航默认折叠，避免首屏过高
2. **导读页的卡片布局更紧凑**
   - 当系列达到 6～8 篇时，导读页卡片优先使用更紧凑的 overview grid
   - 桌面端优先 4 列，平板 2 列，移动端 1 列
3. **章节页系列导航默认收起**
   - 默认只展示“当前章节”卡片
   - 提供“展开全部 / 收起”交互
   - 展开后隐藏重复的当前章节卡片，避免当前项展示两次
4. **系列导航卡片不重复放标题**
   - 对已明确篇次的系列卡片，优先保留：
     - kicker（如“第五篇 · 知识层” / “Article 5 · Knowledge Layer”）
     - desc
     - meta
   - 默认去掉 `LangChain 实战教程（五）` / `LangChain in Practice (V)` 这类重复标题行，减少卡片高度
5. **中英文文案语气保持镜像**
   - Hero 的 headline / subtitle
   - 系列导航卡片的 kicker / desc / meta
   - 导读页的“当前已上线 / Available now”“建议阅读顺序 / Suggested reading order”
   - 尽量保持结构与语义一一对应

当用户要求“统一风格”“统一封面”“章节页导航更紧凑”“中英一起同步”时，应优先检查是否需要套用这套系列模式。

### 第七步：构建校验

完成后必须运行：

```bash
npm run docs:build
```

如果失败：

- 优先修复 frontmatter YAML 错误
- 修复图片相对路径错误
- 修复导航链接错误
- 检查中英文目录是否存在对应文件

## 输出质量门槛

交付前，至少确认以下事项：

- 文章已进入正确目录
- 文章图片已本地化或明确可访问
- 导航与侧边栏已更新
- 首页/README 入口已同步
- 迁移章节已处理旧链接或给出跳转说明
- `docs:build` 通过

## 推荐参考文件

如需完整执行清单，读取：

- `references/workflow-checklist.md`
- `references/hello-claw-touchpoints.md`
- `assets/article-template.md`

## 常用命令模板

```bash
# 查看目标目录结构
find docs/cn -maxdepth 3 -type d | sort

# 搜索导航与章节引用
rg -n "chapter11|记忆系统设计|Memory System Design|AI Agent智能体" docs README*.md

# 下载图片到共享静态目录
curl -L "<image-url>" -o docs/static/<section>/<article>/images/<name>.png

# 构建校验
npm run docs:build
```

## 不要做的事

- 不要只改文章正文而忘记更新导航和首页入口
- 不要保留不稳定的外链图片作为最终发布资源
- 不要把同一张中英文共用图片重复存到 `docs/cn/.../images/` 和 `docs/en/.../images/`
- 不要在用户要求“保留原文”时做大幅重写
- 不要跳过构建校验
- 不要提交 git commit，除非用户明确要求
