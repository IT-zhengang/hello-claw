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

Prefer shared assets under `docs/static` when CN/EN pages use the same image:

```text
docs/static/<section>/<article>/images/
```

Examples:

- `docs/cn/agent/chapter3/index.md` + `docs/en/agent/chapter3/index.md`
  -> `docs/static/agent/chapter3/images/`
- `docs/cn/university/email-assistant/index.md` + `docs/en/university/email-assistant/index.md`
  -> `docs/static/university/email-assistant/images/`

For existing language-specific illustrations, keep the current article-local `images/` directories if the content is not identical across languages.
