# Sources & Methodology

This project synthesizes Vercel's first-party methodology with independent practitioner sources, cross-checked by an adversarial deep-research pass (6 angles · 26 sources fetched · 109 claims extracted · 25 verified by 3-vote adversarial verification → 24 confirmed, 1 refuted).

## Vercel — primary / case study

- Rauch tweet (originating prompt): https://x.com/rauchg/status/2060443982342357032
- Docker in Vercel Sandbox (changelog): https://vercel.com/changelog/run-docker-containers-inside-vercel-sandbox
- Experimental native binaries for Vercel CLI: https://vercel.com/changelog/experimental-native-binaries-for-vercel-cli
- Vercel CLI for marketplace integrations, optimized for agents: https://vercel.com/changelog/vercel-cli-for-marketplace-integrations-optimized-for-agents
- Vercel CLI docs: https://vercel.com/docs/cli
- Vercel Agent docs: https://vercel.com/docs/agent
- Agentic infrastructure (blog): https://vercel.com/blog/agentic-infrastructure
- Security boundaries in agentic architectures: https://vercel.com/blog/security-boundaries-in-agentic-architectures
- Vercel Sandbox is now generally available: https://vercel.com/blog/vercel-sandbox-is-now-generally-available
- Vercel Sandbox concepts: https://vercel.com/docs/vercel-sandbox/concepts
- Zero-config backends on Vercel AI Cloud: https://vercel.com/blog/zero-config-backends-on-vercel-ai-cloud

## Standards layer — MCP & SDKs

- The AI Cloud — a unified platform: https://vercel.com/blog/the-ai-cloud-a-unified-platform-for-ai-workloads
- Introducing Vercel MCP: https://vercel.com/blog/introducing-vercel-mcp-connect-vercel-to-your-ai-tools
- AI SDK 6: https://vercel.com/blog/ai-sdk-6
- mcp-to-ai-sdk: https://vercel.com/blog/generate-static-ai-sdk-tools-from-mcp-servers-with-mcp-to-ai-sdk
- Vercel MCP docs: https://vercel.com/docs/agent-resources/vercel-mcp
- AI SDK MCP tools: https://ai-sdk.dev/docs/ai-sdk-core/mcp-tools

## Practitioner / integration

- vercel-labs/vercel-openclaw: https://github.com/vercel-labs/vercel-openclaw
- Claude Agent SDK on Vercel Sandbox: https://vercel.com/kb/guide/using-vercel-sandbox-claude-agent-sdk
- AI Gateway coding agents: https://vercel.com/docs/ai-gateway/coding-agents
- Enderfga/openclaw-claude-code: https://github.com/Enderfga/openclaw-claude-code

## Vercel Zero language

- Repo: https://github.com/vercel-labs/zero
- MarkTechPost coverage: https://www.marktechpost.com/2026/05/17/vercel-labs-introduces-zero-a-systems-programming-language-designed-so-ai-agents-can-read-repair-and-ship-native-programs/
- Firethering analysis: https://firethering.com/vercel-zero-programming-language-ai-agents/

## AI-first CLI design principles (independent)

- You Need to Rewrite Your CLI for AI Agents (Justin Poehnelt): https://justin.poehnelt.com/posts/rewrite-your-cli-for-ai-agents/
- Why CLI is the New MCP for AI Agents (OneUptime): https://oneuptime.com/blog/post/2026-02-03-cli-is-the-new-mcp/view
- better-cli — a SKILL.md for AI-friendly CLIs (yogin16): https://github.com/yogin16/better-cli
- Writing CLI Tools That AI Agents Actually Want to Use (dev.to): https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no
- Designing CLI Tools for AI Agents — Lessons from Memori: https://archit15singh.github.io/posts/2026-02-28-designing-cli-tools-for-ai-agents/
- MCP vs CLI vs CLI+Skills (Medium): https://medium.com/@akshaychame2/mcp-vs-cli-vs-cli-skills-trade-offs-use-cases-and-best-practices-49b9cfd7a556

## Principle → source mapping

| Principle | Primary source(s) |
|-----------|-------------------|
| Dual-mode output / stdout-stderr split / actionable errors / non-interactive default | better-cli's five foundations |
| Raw payloads / schema introspection / input hardening / dry-run / response sanitization / env auth / multi-surface | Poehnelt, "Rewrite your CLI" |
| Composability / existing tooling / self-describing / zero integration cost / permission reuse | "CLI is the new MCP" |
| Stable error codes / typed repair / version-matched guidance / zero-dependency binary | Vercel Zero + Vercel CLI native binary |
| Idempotency keys | General API idempotency practice (Stripe / Shopify / AWS) |
| Trust-domain microVM isolation / one core many surfaces | Vercel security-boundaries + agentic-infrastructure + AI SDK 6 |

## Confidence & bias (read before citing)

- **Sample bias:** the confirmed sources are almost entirely first-party Vercel. Adversarial verification proves "claimed & internally consistent," not "effective in production."
- **Refuted (do not cite):** "Sandbox clones/launches millions of agents in a single API call" — 1-2 vote, marketing hyperbole.
- **Under-evidenced:** OpenClaw / Claude Code "large-scale embedding into Vercel's agentic infrastructure" — repos and integration paths are real; the scale narrative lacks independent corroboration. Treat as *direction credible, scale unproven.*
- Third-party critique sources (truefoundry / qovery / northflank) are blog-quality and were not used as factual grounding.
