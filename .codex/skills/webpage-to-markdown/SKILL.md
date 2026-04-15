---
name: webpage-to-markdown
description: 爬取网页内容并生成结构化 Markdown 文档，支持可选的深度分析。Use when the user asks to crawl, scrape, fetch, convert, save, or analyze a webpage as Markdown.
---

# Webpage to Markdown

爬取网页并转换为格式规范的 Markdown 文档，默认保存到当前工作目录下的 `./mds/`。

## 依赖

```bash
pip3 install html2text beautifulsoup4
```

## 工作流程

### 1. 打开网页并加载完整内容

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

### 2. 获取网页 HTML

```
chrome_get_web_content(htmlContent=true, tabId=tabId)
```

内容超过 70KB 时会保存到临时 JSON 文件，无需手动读取——直接传给脚本。

### 3. 执行转换脚本

脚本位于 `scripts/convert_webpage.py`，接受 `chrome_get_web_content` 输出的 JSON 文件：

```bash
python3 scripts/convert_webpage.py <input_json> [output_path]
```

- 省略 `output_path` 时自动保存到当前工作目录下的 `./mds/<标题>.md`
- 脚本自动完成的处理：
  - 提取主内容区域
  - **微信公众号专用预处理**：data-src 图片修复、多行 code 合并、空标签清理
  - **图片 URL 清理**：移除 `#imgIndex` fragment、HTML 实体修复、添加默认 alt 文本
  - **代码块修复**：识别被转为缩进列表的代码/流程图内容，恢复为围栏代码块
  - **格式优化**：空标题移除、加粗标记修复、H2 章节分隔线
  - **文件头生成**：自动添加作者、原文链接元信息
  - 表格/链接修复、空行规范化

#### 当前项目中的常用写法

如果你在 `hello-claw` 项目根目录执行脚本：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py <input_json>
```

生成的 Markdown 会默认保存到：

```text
./mds/<标题>.md
```

如果你想显式指定输出文件，也可以这样写：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py <input_json> ./mds/custom-name.md
```

建议优先在项目根目录执行，这样输出位置、后续整理和版本管理都会更清晰。

### 4. 内容区域识别（脚本自动处理）

按优先级尝试：
- `div.rich_media_content` / `div#js_content` — 微信公众号
- `<article>` / `<main>` — 通用网页
- `div.article-content` / `div.post-content` / `div.entry-content` — 博客
- `<body>` — 兜底

### 5. 转换后审校

脚本输出后，**必须 Read 生成的 .md 文件**，检查以下常见问题：

- **图片 URL**：是否还有 `#imgIndex`、`&amp;` 等残留
- **代码块**：流程图/树状图/YAML 是否正确包在 ``` 围栏中
- **空标题**：是否有孤立的 `#` 或 `##`
- **引用块**：`>` 后内容是否正确，加粗标记是否完整
- **章节分隔**：H2 标题前是否有 `---` 分隔线

如有问题，直接用 Edit 工具修复 .md 文件。

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
