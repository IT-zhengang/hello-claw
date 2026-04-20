---
name: hello-claw-web-article-publisher
description: "抓取网页或微信公众号文章，并直接发布到 hello-claw 文档站。Use when the user wants one end-to-end workflow: fetch webpage content, convert it to Markdown, localize images, publish into hello-claw, sync navigation/readmes, and run docs build validation."
---

# Hello Claw Web Article Publisher

这个 Skill 负责把两段流程串成一次性工作流：

1. 抓网页 / 公众号正文
2. 转 Markdown
3. 发布到 `hello-claw`

适合这种请求：

- “爬这个网页，生成 MD，并发布到 hello-claw”
- “把这篇公众号文章接到 LangChain / Agent / LLM 模块”
- “抓远程文章，保留原文，处理图片，并同步站点导航”

不适合这种请求：

- 只想拿 Markdown，不需要发布：用 `webpage-to-markdown`
- 已经有 Markdown 或本地草稿：用 `hello-claw-article-publisher`

## 推荐工作流

### 1. 明确接入目标

先确认或推断这些信息：

- 目标栏目：`build` / `university` / `agent` / `llm` / 其他已有模块
- 是否必须保留原文结构
- 是否需要中英文镜像
- 是否要本地化图片

如果用户没说，默认：

- 优先保留原文结构
- 中英文同步
- 远程图片本地化

### 2. 用 Chrome 抓完整网页

对于微信公众号、长文章、复杂富文本页，**不要默认直接抓完整 HTML**。这类页面直接走 `chrome_get_web_content(htmlContent=true)` 更容易出现截断、异常或结构失真。

优先级建议：

1. 微信 / 长文 / 富文本复杂页：优先浏览器导出 payload JSON
2. 普通静态文章页：再考虑直接抓 HTML
3. 只关心正文文本：最后才考虑直接拿 textContent

优先沿用 `webpage-to-markdown` 的稳定做法：

1. `chrome_navigate` 打开目标页面
2. 用 `chrome_javascript` 滚动到底，触发懒加载
3. 用 `chrome_get_web_content(htmlContent=true)` 拿完整 HTML

如果页面较长、富文本很多，或浏览器工具返回内容不稳定，也可以在浏览器中直接导出一个原始 payload JSON，只要包含这些字段即可：

```json
{
  "title": "文章标题",
  "url": "原文链接",
  "author": "作者",
  "publish_time": "发布时间",
  "htmlContent": "<html>...</html>"
}
```

`webpage-to-markdown/scripts/convert_webpage.py` 现在已兼容：

- Chrome MCP 的包装 JSON
- 上面这种原始 payload JSON

如果需要稳定导出这个 payload，优先读取 `../webpage-to-markdown/references/browser-payload-export.md`，并执行 `../webpage-to-markdown/scripts/export_page_payload.js`。

推荐的快速路径是：

1. 用 `export_page_payload.js` 在浏览器里下载 payload JSON
2. 直接运行 `convert_webpage.py --latest`
3. 让脚本自动定位、转换并删除这个临时 JSON

### 3. 转成 Markdown 草稿

直接调用已有转换脚本：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py <input_json> <output_md> --delete-input
```

建议输出到临时文件，例如：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py /tmp/article.json /tmp/article.md --delete-input
```

如果 payload 刚下载到 `~/Downloads`，最省事的方式是直接：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py --latest
```

如果你只是想先确认路径，再定位：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/find_latest_payload.py
```

然后审校以下问题：

- 代码块是否恢复正常
- 表格是否被打断
- 空标题是否被清理
- 图片链接是否可用
- 微信文章中的强调 / 引用是否失真

默认把 payload JSON 当成中间产物处理：Markdown 成功生成后就删除，避免遗留临时抓取文件。

### 4. 发布到 hello-claw

进入发布阶段时，直接复用 `hello-claw-article-publisher` 的目录和接入规则：

- 正文放到 `docs/cn/...` 与 `docs/en/...`
- 共享图片放到 `docs/static/.../images/`
- 更新 `docs/.vitepress/config.mts`
- 更新 `docs/cn/index.md`、`docs/en/index.md`
- 更新 `README.md`、`README_EN.md`
- 最后执行 `npm run docs:build`

如果目标是**专题系列模块**（例如 LangChain / Agent / LLM 的第 N 篇）而不是单篇独立文章，发布阶段还要额外套用系列规范：

- 导读页保留完整系列卡片
- 章节页的系列导航默认折叠，只显示当前篇，点击再展开全部
- 系列卡片默认不重复展示“教程名 + 篇次”标题行，优先保留篇次标签、简介和 meta
- 中英文系列页要同步更新，不只新增当前文章
- 当系列总数从 4 篇扩展到 6～8 篇时，优先同步调整导读页卡片布局，使首屏更紧凑

完整检查清单按需读取：

- `../hello-claw-article-publisher/references/workflow-checklist.md`
- `../hello-claw-article-publisher/references/hello-claw-touchpoints.md`
- `../hello-claw-article-publisher/assets/article-template.md`

### 5. 图片与封面处理

如果文章要正式发布到 `hello-claw`，远程图片默认本地化：

1. 下载到 `docs/static/<section>/<article>/images/`
2. 中英文共用同一份静态资源
3. 将页面中的图片路径改为相对路径

公众号封面图也按同样方式处理，不要依赖外链热链。

## 输出边界

这个 Skill 的目标不是只做中间产物，而是交付一个**可被 hello-claw 站点直接构建通过的最终结果**。

结束前至少确认：

- 文章正文已放到正确目录
- 图片路径稳定
- 目录入口与侧边栏已接入
- 首页 / README 已同步
- `npm run docs:build` 已通过
