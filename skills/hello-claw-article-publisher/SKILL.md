---
name: hello-claw-article-publisher
description: 将外部文章、Markdown 草稿或专题文档整理并发布到 hello-claw 文档站中。适用于新增章节、迁移文章到新目录、保留原文与图片、本地化远程图片、统一中英文结构、更新 VitePress 导航/侧边栏/首页 README、并执行 docs build 校验的场景。
homepage: https://github.com/IT-zhengang/hello-claw
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["node","npm","python3","curl"]},"install":{"npm":["vitepress"]}}}
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

如果只是小范围错字修正或单一段落改写，不需要使用这个 Skill。

## 项目级原则

1. **先确定归属目录，再落文档**
   - `docs/cn/` 与 `docs/en/` 应保持结构镜像
   - 顶层栏目应和已有目录风格一致，如 `adopt/`、`build/`、`university/`、`agent/`、`llm/`
2. **优先保留用户原文**
   - 若用户强调“保留原文”“保留图片”“内容不变”，先保留内容，再做样式与结构适配
3. **远程图片默认本地化**
   - 外链图片在文档站经常受防盗链、权限或热链失效影响
   - 优先下载到当前文章目录下的 `images/` 子目录，再改成本地相对路径
4. **目录、导航、首页入口要同步**
   - 文章接入不只是一篇 `index.md`，还要同步更新 `docs/.vitepress/config.mts`、首页、README 等入口
5. **发布前必须构建校验**
   - 最低标准是运行 `npm run docs:build --prefix hello-claw`

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

对 `hello-claw` 中的新文章，优先使用如下结构：

```text
hello-claw/docs/cn/<section>/chapterX/index.md
hello-claw/docs/cn/<section>/chapterX/images/
hello-claw/docs/en/<section>/chapterX/index.md
hello-claw/docs/en/<section>/chapterX/images/
```

如果是顶层栏目导言页，则使用：

```text
hello-claw/docs/cn/<section>/index.md
hello-claw/docs/en/<section>/index.md
```

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

1. 在当前文章目录创建 `images/`
2. 使用 `curl -L` 下载资源到本地
3. 将正文中的远程链接改为 `./images/<name>.png` 之类的相对路径
4. 中英文镜像目录如需相同图片，可复制一份到英文目录对应 `images/`

命名建议：

- 使用语义化 kebab-case，如 `memory-overview.png`
- 同一文章图片命名风格统一

### 第五步：做 hello-claw 风格适配

需要优先检查这些位置：

- `hello-claw/docs/.vitepress/config.mts`
- `hello-claw/docs/cn/index.md`
- `hello-claw/docs/en/index.md`
- `hello-claw/README.md`
- `hello-claw/README_EN.md`
- `hello-claw/README_JA.md`

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

### 第七步：构建校验

完成后必须运行：

```bash
npm run docs:build --prefix hello-claw
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

- `{baseDir}/references/workflow-checklist.md`
- `{baseDir}/references/hello-claw-touchpoints.md`
- `{baseDir}/assets/article-template.md`

## 常用命令模板

```bash
# 查看目标目录结构
find hello-claw/docs/cn -maxdepth 3 -type d | sort

# 搜索导航与章节引用
rg -n "chapter11|记忆系统设计|Memory System Design|AI Agent智能体" hello-claw/docs hello-claw/README*.md

# 下载图片到本地
curl -L "<image-url>" -o hello-claw/docs/cn/<section>/chapterX/images/<name>.png

# 构建校验
npm run docs:build --prefix hello-claw
```

## 不要做的事

- 不要只改文章正文而忘记更新导航和首页入口
- 不要保留不稳定的外链图片作为最终发布资源
- 不要在用户要求“保留原文”时做大幅重写
- 不要跳过构建校验
- 不要提交 git commit，除非用户明确要求
