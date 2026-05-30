# The AI-First CLI Self-Audit Checklist

Drop this into any CLI design review or PR. Each item maps to one of the [12 principles](./principles.md).

## Output (Principles 1, 2, 10, 11)

- [ ] **Structured output by default on non-TTY.** Does `--json` exist, and is it the implicit default when stdout is not a terminal?
- [ ] **stdout/stderr separation.** Data on stdout, logs/progress/errors on stderr. Verify `cmd --json | jq` is never polluted.
- [ ] **Stable envelope.** Every command shares a consistent shape (e.g. `{ok, data, error}`).
- [ ] **Token-frugal.** Field selection (`--fields`), pagination, and terse output available.
- [ ] **Deterministic.** No random ordering, no timestamps or color codes inside JSON. Output is versioned.

## Errors (Principle 4)

- [ ] **Non-zero exit on failure.** No `200-with-error-body`.
- [ ] **Actionable error object:** `code` + `message` + `fix` + `retryable`.
- [ ] **Stable error codes** an agent can match on (not prose).
- [ ] **`explain <CODE>`** returns a structured explanation without scraping external docs.

## Input & discovery (Principles 3, 5)

- [ ] **Raw payloads accepted** — JSON isomorphic to the API schema (`--json` / `--params`).
- [ ] **Self-describing** via `--help` and schema introspection.
- [ ] **Version-matched guidance** ships with the binary (docs don't drift).

## Interaction & auth (Principle 6)

- [ ] **Non-interactive by default.** Every prompt has a flag bypass (`--yes` / `--force`).
- [ ] **Env-var auth** — no mandatory browser flow for headless runs.

## Safety for autonomy (Principle 9)

- [ ] **`--dry-run`** on mutating operations.
- [ ] **Idempotency keys** on side-effecting operations.
- [ ] **Input hardening** against path traversal, control characters, injection.
- [ ] **Response sanitization** against embedded prompt injection.
- [ ] **VM-level isolation** if the tool executes agent-generated code (trust-domain microVM, not shared-kernel container).

## Composability & packaging (Principles 7, 8, 12)

- [ ] **Pipeable**, reads stdin, streams NDJSON for pagination.
- [ ] **Packaging** as close to zero-dependency and trustworthy (signed binary) as possible.
- [ ] **One core, many surfaces** — CLI / MCP / SDK share a single capability core.
