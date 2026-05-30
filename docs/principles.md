# The 12 Principles of AI-First CLI Design

> The core thesis: **the CLI's primary reader is shifting from humans to agents.** An agent-first CLI makes *machine-callable, predictable, parseable* the main path and degrades gracefully to human ergonomics — never the reverse.
>
> The one-line test: **after reading a command's output, an agent should know exactly what to do next — without guessing, hallucinating a command, or stalling.**

Each principle below pairs a rule with a concrete *do / don't*. Sources are mapped in [`sources.md`](./sources.md).

## 1. Machine output is the default, not a flag

Detect the TTY. An interactive terminal gets human-friendly output; a non-TTY (piped, or called by an agent) defaults to structured. Or expose it explicitly via `--json`. The structured envelope must be **stable**:

```json
{ "ok": true, "data": { }, "error": null }
```

**Do:** ship a consistent envelope every command shares.
**Don't:** make agents screen-scrape a table that reflows on terminal width.

## 2. Separate stdout from stderr

Data goes to **stdout**; diagnostics, progress, and errors go to **stderr**. Then `cmd --json | jq` is never polluted by a log line.

**Do:** keep stdout pure machine-parseable payload.
**Don't:** interleave `[INFO] connecting…` into the JSON an agent is parsing.

## 3. Accept raw payloads

Let callers pass JSON that maps 1:1 to the underlying API schema (`--json` / `--params`). An LLM generates that with zero translation loss; bespoke flag grammars force lossy guesswork.

**Do:** `tool create --json '{"name":"x","region":"sfo1"}'`.
**Don't:** invent `--set-name`, `--set-region`, `--set-...` for every field.

## 4. Errors must be actionable

A failure must carry: non-zero **exit code** + **stable error code** + human **message** + a **fix** suggestion + a **retryable** flag.

```json
{"ok": false, "error": {
  "code": "AUTH_004",
  "message": "Token expired",
  "fix": "run `tool auth login`",
  "retryable": false
}}
```

Codes must be **stable** so agents match `AUTH_004` rather than parsing prose, and pair them with `tool explain AUTH_004` for a structured explanation — never send an agent to scrape external docs.

**Do:** make failure a structured, navigable object.
**Don't:** `Error: something went wrong` (exit 1).

## 5. Be self-describing & discoverable

`--help` is an agent's discovery entry point — this is the core of the "CLI is the new MCP" argument: an existing CLI already ships `--help`, auth, pagination, and retries, for zero integration cost. Go further: build schema-introspection commands, and ship usage guidance **version-matched to the binary** (e.g. Vercel Zero's `zero skills`) so docs never drift from reality.

**Do:** make the CLI the source of truth for what the API accepts *now*.
**Don't:** keep the only accurate reference on a website that lags the binary.

## 6. Non-interactive by default

Agents run headless. Any `Are you sure? [y/N]` deadlocks them. The rule: **every interactive prompt must have a flag bypass** (`--yes`, `--force`), and credentials come from environment variables.

**Do:** `tool deploy --yes`; auth via `TOOL_TOKEN`.
**Don't:** block on a TTY prompt or a browser OAuth dance in CI.

## 7. Zero dependencies, self-contained

Agents spin tools up repeatedly in ephemeral sandboxes. A dependency chain is unpredictability, latency, and attack surface. A single **code-signed** binary is verifiable, fast to start, and cross-platform. This is exactly the direction of Vercel's native-binary CLI.

**Do:** ship one signed static binary per OS/arch.
**Don't:** require a specific runtime + a lockfile resolve on every cold start.

## 8. Composable (Unix)

Be pipeable, read from stdin, and stream **NDJSON** for pagination so output is processable without buffering. Composability is what lets agents chain primitives instead of demanding a bespoke endpoint per task.

**Do:** `tool list --json --page-all | jq '.[].id'`.
**Don't:** force a custom protocol for what a pipe already solves.

## 9. Guardrails for autonomy

Agents hallucinate inputs — "build like it." Validate and reject path traversal, control characters, and injection; offer `--dry-run` on mutations; use idempotency keys on side-effecting operations (same key retried ⇒ no double execution); sanitize returned data so prompt injection embedded in a response isn't fed straight back into the agent.

**When the tool executes agent-produced code/commands**, input validation is only the first layer — isolation belongs at the **VM level (trust-domain microVM)**, not a shared-kernel container. Assume agent-generated code is untrusted by default. This is the core thesis of Vercel Sandbox (see the [case study](./vercel-case-study.md)).

**Do:** `--dry-run`, idempotency keys, VM isolation for untrusted execution.
**Don't:** trust agent input, or run generated code with host privileges.

## 10. Token-frugal

Support field selection (`--fields id,name`), pagination, and terse output. Verbose responses exhaust the context window and degrade the agent.

**Do:** return only what was asked for.
**Don't:** dump a 2,000-line object when the agent needed one id.

## 11. Determinism over cleverness

Agents prize predictability. Keep output contracts **stable**, **versioned**, and free of nondeterminism (random ordering, timestamps, or color codes polluting JSON). `mcp-to-ai-sdk` — compiling a dynamic MCP server into static, versioned tools — is this principle as engineering: a fixed contract beats runtime negotiation.

**Do:** version the schema; sort deterministically.
**Don't:** let output shape drift release to release.

## 12. One core, many surfaces

Expose the same capability core through CLI, MCP, SDK, and environment variables. Vercel positions CLI, API, MCP server, and git all as agent interfaces over one orchestration/compute/storage layer.

**Do:** one core; thin adapters per surface.
**Don't:** reimplement logic — and bugs — per surface.

## Anti-patterns

- **`200-with-error-body`** — always exiting 0 and burying the error in the payload, so the agent thinks it succeeded.
- Human and machine output mixed on the same stdout stream.
- Prose-only errors with no stable code and no suggested fix.
- Interactive by default with no `--yes` bypass — deadlocks headless agents.
- Unstable output: random ordering, or timestamps/color codes contaminating JSON.
- Trusting agent input without validation.
- Documentation on an external site that drifts from the binary's version.
