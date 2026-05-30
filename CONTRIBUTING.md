# Contributing to AI-First CLI

Thanks for considering a contribution. This project is a living methodology — it gets sharper with counter-examples, new case studies, and careful disagreement.

## Ways to contribute

- **Sharpen a principle** — tighten wording, add a do/don't, or surface an edge case.
- **Propose or challenge a principle** — open an issue with the *Principle proposal* template. Extraordinary claims need evidence; we prefer sourced arguments over opinion.
- **Add a case study** — another tool that embodies (or violates) the philosophy, with sources.
- **Translate** — README and docs into another language.
- **Improve the Claude skill** — see [`skill/ai-first-cli`](./skill/ai-first-cli).

## Principles for changes to the principles

This repo holds itself to its own standard:

1. **Cite your sources.** Claims go in `docs/sources.md` with a confidence note. First-party/marketing sources are labeled as such.
2. **Be honest about uncertainty.** If a claim is under-evidenced or contested, say so in the text — don't launder it into fact.
3. **No silent breaking changes** to the numbered principles. Renumbering or removing a principle is a discussed change, logged in `CHANGELOG.md`.

## Workflow

1. Fork and create a branch: `git checkout -b improve-principle-9`.
2. Make your change. Keep prose tight and bilingual parity in mind — if you change `README.md`, update `README.zh-CN.md` (or note that a follow-up translation is needed).
3. If you touch the skill, run validation:
   ```bash
   python3 ~/.claude/skills/skill-creator/scripts/quick_validate.py skill/ai-first-cli
   ```
4. Open a PR using the template. Link any related issue.

## Style

- English docs: imperative, terse, example-driven.
- Markdown: one sentence per idea; tables for reference; fenced code with language tags.
- Conventional, descriptive commit messages (`docs:`, `skill:`, `fix:`, `feat:`).

## Code of Conduct

Participation is governed by our [Code of Conduct](./CODE_OF_CONDUCT.md). Be kind; argue the idea, not the person.

## License of contributions

By contributing, you agree your contributions are licensed under [CC BY 4.0](./LICENSE), the same license as the project.
