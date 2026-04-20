---
name: webpage-to-markdown
description: "爬取网页内容并生成结构化 Markdown 草稿，支持可选的深度分析。Use when the user asks to crawl, scrape, fetch, convert, save, or analyze a webpage as Markdown. If the end goal is to publish a crawled webpage directly into hello-claw, prefer the integrated skill `hello-claw-web-article-publisher`."
---

# Webpage to Markdown

爬取网页并转换为格式规范的 Markdown 草稿，默认保存到当前工作目录下的 `./mds/`。

这个 Skill 只负责“抓取 + 转 Markdown”。

- 如果用户已经有 Markdown / 草稿，后续要接入 `hello-claw`，改用 `hello-claw-article-publisher`
- 如果用户要把远程网页 / 微信公众号 **直接发布到** `hello-claw`，优先用整合型 Skill：`hello-claw-web-article-publisher`

附带两个常用脚本：

- `scripts/export_page_payload.js`：在浏览器页内导出原始 payload JSON
- `scripts/find_latest_payload.py`：自动定位最近生成的 payload JSON

## 依赖

```bash
pip3 install html2text beautifulsoup4
```

## 工作流程

### 1. 默认流程优先级

为避免“直接抓取 HTML 时内容截断 / 异常 / 富文本结构失真”，优先按下面的稳定性顺序选择：

1. **长文章 / 微信公众号 / 富文本复杂页面**：优先用浏览器导出 payload JSON
2. **普通文章页 / 静态页 / 内容较短**：可直接用 `chrome_get_web_content(htmlContent=true)`
3. **只要正文文本、不关心结构细节**：再考虑直接抓取 textContent

结论：**不要把“直接抓完整 HTML”当默认方案**。对公众号和长文，默认应切到“浏览器导出 payload -> 脚本转换”的路径。

### 2. 打开网页并加载完整内容

```
chrome_navigate(url=目标URL)
```

等待页面加载后，通过 JS 滚动到底部触发懒加载（尤其是微信公众号）：

```
chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight); return document.title;", tabId=tabId)
```

如需多次滚动（长文章），可循环滚动：

```
chrome_javascript(code="window.scrollTo(0, document.body.scrollHeight); return document.body.scrollHeight;", tabId=tabId)
```

> **注意**：不要用 `chrome_computer(action="scroll")`，微信页面上容易超时。用 `chrome_javascript` 直接操作 DOM 更稳定。

### 3. 获取网页 HTML 或导出 payload

#### 方案 A：稳定优先，直接导出 payload JSON（推荐）

如果页面过长、正文结构复杂、是微信公众号，或你已经知道 `chrome_get_web_content` 容易异常：

- 读取 `references/browser-payload-export.md`
- 用 `scripts/export_page_payload.js` 在浏览器页内直接导出 payload JSON
- 然后直接运行：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py --latest
```

这条命令会：

- 自动从当前目录、`/tmp`、`~/Downloads` 找最近下载的 `*_payload.json`
- 自动转成 Markdown
- 默认在成功后删除这个临时 JSON

如果你确实要保留 payload，再加：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py --latest --keep-input
```

#### 方案 B：短页面时直接抓 HTML

```
chrome_get_web_content(htmlContent=true, tabId=tabId)
```

内容超过 70KB 时会保存到临时 JSON 文件，无需手动读取——直接传给脚本。

如果页面过长、正文结构复杂，或你希望直接拿到一个可复用的原始 payload JSON，读取 `references/browser-payload-export.md`，并使用 `scripts/export_page_payload.js` 在浏览器页内直接导出。

### 4. 执行转换脚本

脚本位于 `scripts/convert_webpage.py`，接受以下任一输入：

- `chrome_get_web_content` / Chrome MCP 导出的包装 JSON
- 浏览器中直接保存的原始 payload JSON（包含 `title` / `url` / `author` / `htmlContent`）

命令：

```bash
python3 scripts/convert_webpage.py <input_json> [output_path] [--delete-input]
```

- 也支持直接取最近下载的 payload：

```bash
python3 scripts/convert_webpage.py --latest [output_path]
```

- 省略 `output_path` 时自动保存到当前工作目录下的 `./mds/<标题>.md`
- 在 `--latest` 模式下，如果只传一个位置参数，会自动把它当成 `output_path`
- 加上 `--delete-input` 时，Markdown 成功生成后会自动删除输入的 payload JSON
- 使用 `--latest` 时，默认也会在成功后删除该 payload JSON；如果要保留，显式加 `--keep-input`
- 脚本自动完成的处理：
  - 提取主内容区域
  - **微信公众号专用预处理**：data-src 图片修复、多行 code 合并、空标签清理
  - **图片 URL 清理**：移除 `#imgIndex` fragment、HTML 实体修复、添加默认 alt 文本
  - **代码块修复**：识别被转为缩进列表的代码/流程图内容，恢复为围栏代码块
  - **格式优化**：空标题移除、加粗标记修复、H2 章节分隔线
  - **文件头生成**：自动添加作者、原文链接元信息
  - 表格/链接修复、空行规范化

如果页面太长、`chrome_get_web_content` 容易截断，或你已经在浏览器里拿到了完整 payload，直接把原始 payload JSON 传给脚本即可，不需要再手工包一层 wrapper。对浏览器下载出来的临时 payload，优先直接用 `--latest`，这样路径定位和删除都自动完成。

如果你还没有这个 payload JSON，优先用 `scripts/export_page_payload.js` 通过浏览器直接下载，再进入转换步骤。

如果 payload 文件刚下载完、不想手动找路径，可以先运行：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/find_latest_payload.py
```

它会优先从当前目录、`/tmp`、`~/Downloads` 中找最近生成的 JSON 文件。

#### 当前项目中的常用写法

如果你在 `hello-claw` 项目根目录执行脚本：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py --latest
```

生成的 Markdown 会默认保存到：

```text
./mds/<标题>.md
```

如果你已经有一个明确的输入文件，或想显式指定输出文件，也可以这样写：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py <input_json> ./mds/custom-name.md --delete-input
```

建议优先在项目根目录执行，这样输出位置、后续整理和版本管理都会更清晰。

### 5. 内容区域识别（脚本自动处理）

按优先级尝试：
- `div.rich_media_content` / `div#js_content` — 微信公众号
- `<article>` / `<main>` — 通用网页
- `div.article-content` / `div.post-content` / `div.entry-content` — 博客
- `<body>` — 兜底

### 6. 转换后审校

脚本输出后，**必须 Read 生成的 .md 文件**，检查以下常见问题：

- **图片 URL**：是否还有 `#imgIndex`、`&amp;` 等残留
- **代码块**：流程图/树状图/YAML 是否正确包在 ``` 围栏中
- **空标题**：是否有孤立的 `#` 或 `##`
- **引用块**：`>` 后内容是否正确，加粗标记是否完整
- **章节分隔**：H2 标题前是否有 `---` 分隔线

如有问题，直接用 Edit 工具修复 .md 文件。

### 7. 需要落到 hello-claw 时

如果用户的真正目标不是“拿到 Markdown”，而是“发布到 hello-claw 站点”：

- 已经有 Markdown 草稿：切换到 `hello-claw-article-publisher`
- 还在网页阶段：优先直接使用 `hello-claw-web-article-publisher`

## 深度分析（仅在用户明确要求时）

在原文 Markdown 末尾追加分析章节，结构如下：

```markdown
---

## 深度分析

### 核心概念

[提取文章的核心概念和关键术语，构建层次关系]

### 概念对比

| 维度 | A | B | C |
|------|---|---|---|
| 本质 | … | … | … |
| 价值 | … | … | … |
| 场景 | … | … | … |

### 关键洞察

[反直觉的结论、技术选型建议、常见误区]

### 实践启示

[可操作的实施路径和优先级]

### 风险与挑战

| 风险 | 说明 | 应对策略 |
|------|------|----------|
| …    | …    | …        |

## 核心结论

[一段话总结]
```

## 注意事项

- 图片保留原始 URL，不下载到本地
- 某些防盗链图片可能无法在本地渲染，属正常现象
- 如果脚本输出的 JSON 路径在 `.claude/` 下的临时目录，直接传路径给脚本即可
- 微信公众号图片需要 Referer 头才能加载，Markdown 编辑器中可能显示为裂图，这是预期行为
- 对公众号、超长页、复杂富文本页，默认不要执着于“直接抓 HTML”；优先改走“浏览器下载 payload -> `convert_webpage.py --latest`”
