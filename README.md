<div align="center">

# AI-First CLI

### A design philosophy for command-line tools whose primary user is an AI agent — not a human.

**English** · [简体中文](./README.zh-CN.md)

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](./LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-d97757.svg)](./skill/ai-first-cli)
[![Validate](https://github.com/yzfly/ai-first-cli/actions/workflows/validate.yml/badge.svg)](https://github.com/yzfly/ai-first-cli/actions/workflows/validate.yml)
[![Stars](https://img.shields.io/github/stars/yzfly/ai-first-cli?style=social)](https://github.com/yzfly/ai-first-cli/stargazers)

*12 principles · a Vercel case study · a copy-paste audit checklist · a ready-to-install Claude skill.*

</div>

---

> **The CLI's primary reader is shifting from humans to agents.**
> For thirty years we designed command-line tools for people who read error messages, run `--help`, and debug by hand. Agents do none of that well. **AI-First CLI** is the discipline of treating *machine-callable, predictable, parseable* as the main path — without losing the human one.

The one-line test:

> **After reading a command's output, an agent should know exactly what to do next — without guessing, hallucinating a command, or stalling.**

This is **not** "bolt a `--json` flag onto an old CLI." It is inverting the human assumptions baked into every interface — that the caller reads prose errors, debugs interactively, and reads external docs — and rebuilding for a caller that does none of those things.

## Table of Contents

- [Why this exists](#why-this-exists)
- [The 12 Principles](#the-12-principles)
- [One example: prose error vs. actionable error](#one-example-prose-error-vs-actionable-error)
- [CLI vs. MCP — which to build](#cli-vs-mcp--which-to-build)
- [Case study: how Vercel pushes this to the limit](#case-study-how-vercel-pushes-this-to-the-limit)
- [Use it as a Claude skill](#use-it-as-a-claude-skill)
- [The self-audit checklist](#the-self-audit-checklist)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)
- [Author](#author)

## Why this exists

Agentic tools — Claude Code, OpenClaw, coding agents of every shape — invoke CLIs millions of times a day. Vercel CEO Guillermo Rauch calls the CLI the key embedding surface of the *"cloud for agents."* When the caller is a model, the old design defaults actively hurt: interactive prompts hang headless runs, colorized tables poison pipes, prose errors waste tokens and invite hallucinated fixes.

This project distills — from Vercel's first-party methodology **plus** independent practitioner sources, cross-checked with adversarial verification — what "agent-first" actually means in practice. Every principle is sourced; see [`docs/sources.md`](./docs/sources.md), including an honest bias statement.

## The 12 Principles

| # | Principle | In one line |
|---|-----------|-------------|
| 1 | **Machine output is the default, not a flag** | Structured envelope on non-TTY; pretty output only for humans at a terminal |
| 2 | **Separate stdout from stderr** | Data → stdout, diagnostics/logs/errors → stderr, so pipes stay clean |
| 3 | **Accept raw payloads** | Take JSON isomorphic to the API schema — zero translation loss for an LLM |
| 4 | **Errors must be actionable** | Exit code + stable error code + message + fix command + retryable flag |
| 5 | **Be self-describing & discoverable** | `--help`, schema introspection, `explain CODE`; the CLI is the source of truth for what the API accepts *now* |
| 6 | **Non-interactive by default** | Every prompt has a flag bypass; auth via env vars, never a browser flow |
| 7 | **Zero dependencies, self-contained** | A single signed binary: fast start, trustworthy, no dependency-chain surprises in a sandbox |
| 8 | **Composable (Unix)** | Pipeable, reads stdin, streams NDJSON for pagination |
| 9 | **Guardrails for autonomy** | `--dry-run`, idempotency keys, input hardening, response sanitization against prompt injection |
| 10 | **Token-frugal** | Field selection, pagination, terse output — don't blow the context window |
| 11 | **Determinism over cleverness** | Stable output contracts + versioned schemas; agents prize predictability |
| 12 | **One core, many surfaces** | CLI / MCP / SDK / env var share a single capability core |

Full rationale, do/don't, and edge cases: **[`docs/principles.md`](./docs/principles.md)**.

## One example: prose error vs. actionable error

```diff
- Error: something went wrong
- (exit 1)
```

```json
{
  "ok": false,
  "error": {
    "code": "AUTH_004",
    "message": "Token expired",
    "fix": "run `tool auth login`",
    "retryable": false
  }
}
```

The error **code is stable** so an agent matches on `AUTH_004` instead of parsing English, and `tool explain AUTH_004` returns a structured explanation — so the agent never has to scrape external docs.

## CLI vs. MCP — which to build

| Dimension | A well-built CLI | A custom MCP server |
|-----------|------------------|---------------------|
| Integration cost | Zero — the agent just shells out | Build a server per integration |
| Composability | Native Unix pipes | Weaker in-protocol composition |
| Discovery | `--help` built in | Needs schema definitions |
| Permissions / audit | Reuses system perms + shell history | Build your own |
| When to pick MCP | Persistent connections, structured bidirectional streams, rich typed negotiation |

**Rule of thumb:** make the CLI agent-first first — it covers most cases. Reserve MCP for genuinely stateful protocols. *One core, many surfaces* (Principle 12) lets both share the same foundation.

## Case study: how Vercel pushes this to the limit

Vercel rebuilds its entire surface around agents, and it's the most complete real-world embodiment of this philosophy — read the full, source-verified write-up in **[`docs/vercel-case-study.md`](./docs/vercel-case-study.md)**. Highlights:

- **CLI → zero-dependency, self-updating, code-signed native binary.** No Node runtime, fast start, OS-verifiable provenance — exactly Principle 7.
- **Docker inside Vercel Sandbox**, on **trust-domain microVMs**, not shared-kernel containers. The under-appreciated thesis: *agent-generated code is untrusted by default*, so isolation belongs at the VM level (Principle 9 taken to its conclusion).
- **One core, many surfaces:** CLI, API, MCP server, and git are all positioned as agent interfaces. Vercel MCP is an OAuth-compliant server; AI SDK 6 redefines `Agent` from a class into an *interface*; `mcp-to-ai-sdk` compiles dynamic MCP servers into static, versioned tools (Principles 5 + 11 as engineering).
- **Zero**, a Vercel Labs systems language whose compiler emits JSON diagnostics with stable codes and typed repair metadata — the philosophy taken all the way down to the language itself.

> ⚠️ The case study draws almost entirely on first-party Vercel sources and carries an explicit bias statement; one marketing claim ("clone millions of agents in a single API call") was **refuted** by adversarial verification and is flagged as such.

## Use it as a Claude skill

This methodology ships as an installable [Claude Code](https://claude.com/claude-code) skill, so an agent applies the principles automatically when you design or review a CLI.

```bash
# Install for Claude Code
git clone git@github.com:yzfly/ai-first-cli.git
cp -r ai-first-cli/skill/ai-first-cli ~/.claude/skills/
```

The skill auto-triggers when you're deciding output formats, error handling, flags, packaging, or autonomous-operation safety for a command-line tool. Source: [`skill/ai-first-cli`](./skill/ai-first-cli).

## The self-audit checklist

Drop this into any CLI review. Full version with rationale in **[`docs/checklist.md`](./docs/checklist.md)**.

- [ ] Structured output by default on non-TTY? Does `--json` exist?
- [ ] Data → stdout, logs/errors → stderr?
- [ ] Non-zero exit on failure, with `code` + `message` + `fix` + `retryable`?
- [ ] Error codes stable and backed by an `explain`?
- [ ] Every interactive prompt has a flag bypass? Env-var auth?
- [ ] Mutating operations offer `--dry-run` / idempotency?
- [ ] Inputs hardened against path traversal, control chars, injection?
- [ ] Output contract stable, versioned, token-frugal?
- [ ] `--help` / schema fully self-describing?
- [ ] Packaging as close to zero-dependency and trustworthy as possible?

## Documentation

| Doc | What's inside |
|-----|---------------|
| [`docs/principles.md`](./docs/principles.md) | The 12 principles in depth, with do/don't |
| [`docs/vercel-case-study.md`](./docs/vercel-case-study.md) | Source-verified Vercel methodology + bias statement |
| [`docs/checklist.md`](./docs/checklist.md) | The full self-audit checklist |
| [`docs/sources.md`](./docs/sources.md) | All sources, with confidence & bias notes |
| [`skill/ai-first-cli`](./skill/ai-first-cli) | The installable Claude skill (Chinese, agent-optimized) |

## Contributing

Contributions are warmly welcome — a sharper principle, a counter-example, a new case study, a translation. Read **[CONTRIBUTING.md](./CONTRIBUTING.md)** and our **[Code of Conduct](./CODE_OF_CONDUCT.md)** first. Proposing or challenging a principle? Use the *Principle proposal* issue template.

## License

[**Creative Commons Attribution 4.0 International (CC BY 4.0)**](./LICENSE) — use it anywhere, including commercially; just give attribution.

## Citation

If this work informs your tools or writing, please cite it (see [`CITATION.cff`](./CITATION.cff)):

```
云中江树 (yzfly). AI-First CLI: A design philosophy for command-line tools whose
primary user is an AI agent. 2026. https://github.com/yzfly/ai-first-cli
```

## Author

**云中江树** · WeChat Official Account: **云中江树** · GitHub: [@yzfly](https://github.com/yzfly)

<div align="center">

If this clarified how you think about agent-facing tools, consider leaving a ⭐.

</div>
