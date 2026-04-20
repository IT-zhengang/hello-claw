# Browser Payload Export

当网页较长、富文本复杂、或者 `chrome_get_web_content` 返回不稳定时，优先在浏览器页内直接导出原始 payload JSON。

## 目标

导出一个可直接喂给 `scripts/convert_webpage.py` 的 JSON 文件，至少包含：

```json
{
  "title": "文章标题",
  "url": "原文链接",
  "author": "作者",
  "publish_time": "发布时间",
  "description": "摘要",
  "cover": "封面图链接",
  "htmlContent": "<html>...</html>"
}
```

## 推荐步骤

1. 读取 `../scripts/export_page_payload.js`
2. 把脚本全文传给 `chrome_javascript`
3. 等浏览器下载出 `*_payload.json`
4. 优先直接运行：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py --latest
```

这会自动：

- 找到最近下载的 payload JSON
- 转换为 Markdown
- 成功后删除该临时 JSON

如果确实要保留 JSON，再改用：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py --latest ./mds/custom-name.md --keep-input
```

或者显式传入某个 payload 路径：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/convert_webpage.py <payload_json> <output_md> --delete-input
```

如果刚下载完不想手工查路径，可以先运行：

```bash
python3 .codex/skills/webpage-to-markdown/scripts/find_latest_payload.py
```

## 说明

- 这个导出脚本不会把 payload 内容直接回传给模型，而是让浏览器下载成文件，避免大段 HTML 被工具输出截断
- 默认适合微信公众号，也兼容普通文章页
- 文件名会自动按标题生成，如 `LangChain_实战教程_二_payload.json`
- 推荐把它当成**默认稳定路径**，而不是 `chrome_get_web_content(htmlContent=true)` 的备选路径
