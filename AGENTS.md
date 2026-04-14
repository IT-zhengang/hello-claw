# Repository Guidelines

## 项目结构与模块组织

本仓库是一个基于 VitePress 的文档站点。主要内容位于 `docs/`，并按语言拆分为 `docs/cn/` 与 `docs/en/` 两套镜像目录。每个语言目录下按 `adopt/`、`build/`、`university/`、`appendix/` 分组，大多数页面使用 `index.md` 作为入口。站点配置集中在 `docs/.vitepress/`：`config.mts` 负责多语言、导航和构建配置，`docs/.vitepress/theme/` 存放自定义 Vue 布局与样式。共享静态资源放在 `docs/public/`；页面专属图片应优先放在相邻的 `images/` 目录或对应语言资源目录中。仓库根目录下的 `README*.md`、`asset/` 与 `scripts/` 主要用于仓库首页展示与阅读增强。

## 构建、测试与开发命令

- `npm ci`：按 `package-lock.json` 精确安装依赖；建议使用 Node 24，与 GitHub Pages CI 保持一致。
- `npm run dev` 或 `npm run docs:dev`：启动本地 VitePress 开发服务器，实时预览 `docs/` 内容。
- `npm run build` 或 `npm run docs:build`：生成生产版本站点，输出到 `docs/.vitepress/dist`。
- `npm run preview` 或 `npm run docs:preview`：本地预览已构建的静态站点。
- 若涉及示例脚本，可按需安装额外依赖，例如：`pip install -r docs/en/university/email-assistant/examples/requirements.txt`。

## 编码风格与命名约定

优先以 Markdown 内容为主进行修改；若同时调整中英文内容，尽量保持章节结构一致。标题、段落和说明应简洁直接，链接尽量使用相对路径。修改 `docs/.vitepress/` 下的配置、Vue 或 CSS 文件时，遵循现有的 2 空格缩进和当前代码风格。新增目录、资源文件建议使用小写 kebab-case 命名；若所在目录已约定入口文件为 `index.md`，请继续沿用。

## 测试指南

当前仓库没有独立的自动化测试套件，因此 `npm run docs:build` 是所有文档和主题改动的基础校验步骤。提交前请至少在本地开发环境中检查修改页面，确认侧边栏、导航、多语言跳转和图片显示正常，并兼顾桌面端与移动端效果。若你修改了示例代码，只运行受影响的示例即可，并将前置条件写入页面或示例目录下的 README。

## 提交与 Pull Request 规范

从现有 Git 历史看，提交信息以简短、祈使句风格为主，例如 `docs: update ...` 或 `Add ...`。每次提交应聚焦一个清晰的主题，必要时在标题中标明影响的语言或章节。Pull Request 需包含变更摘要；若有关联议题、讨论或任务，请一并附上链接。涉及首页、布局或视觉样式调整时，应提供截图说明。若中英文内容暂未完全同步，请在 PR 描述中明确指出，便于评审理解这是有意差异还是待补事项。
