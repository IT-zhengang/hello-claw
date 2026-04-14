# Workflow Checklist

## 1. Intake

- Confirm source document path
- Confirm destination section (`build` / `university` / `agent` / `llm`)
- Confirm whether original content must be preserved
- Confirm whether original images must be preserved
- Confirm whether English mirror pages are required

## 2. File Layout

- Create target directories
- Add `index.md`
- Add `images/` for local assets
- Mirror the structure in `docs/en/` when appropriate

## 3. Content Processing

- Preserve title hierarchy if keeping original content
- Normalize image paths
- Add migration notes if moving content from an old path
- Keep article-specific styles local to the page

## 4. Integration

- Update `docs/.vitepress/config.mts`
- Update `docs/cn/index.md`
- Update `docs/en/index.md`
- Update `README.md`
- Update `README_EN.md`
- Update `README_JA.md` when top-level project structure changes

## 5. Verification

- Search for old chapter references with `rg`
- Build docs with `npm run docs:build --prefix hello-claw`
- Review build errors before finishing
