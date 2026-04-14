# Hello Claw Publishing Touchpoints

When publishing a new article into `hello-claw`, the most common touchpoints are:

## Primary content paths

- `docs/cn/<section>/...`
- `docs/en/<section>/...`

## Navigation and sidebar

- `docs/.vitepress/config.mts`

## Home / overview pages

- `docs/cn/index.md`
- `docs/en/index.md`
- `docs/cn/<section>/index.md`
- `docs/en/<section>/index.md`

## Repository-level entry pages

- `README.md`
- `README_EN.md`
- `README_JA.md`

## Asset placement rule

Prefer article-local assets:

```text
docs/cn/<section>/chapterX/images/
docs/en/<section>/chapterX/images/
```

This keeps chapter assets self-contained and easier to migrate.
