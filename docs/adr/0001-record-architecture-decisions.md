# ADR-0001: Record architecture decisions

- **Status:** Accepted
- **Date:** 2026-09-15
- **Deciders:** @maintainers

## Context

We need to record the architectural decisions made on this project, so that current and future contributors (human or AI) can understand not only *what* was decided, but *why*. Without a written record, decisions are re-discussed, and their original rationale is lost.

## Decision

We will use Architecture Decision Records, as described by Michael Nygard, stored as Markdown files in `docs/adr/` and numbered sequentially. Each ADR is immutable once accepted. To change a decision, a new ADR supersedes the previous one.

## Alternatives Considered

### Wiki pages

- **Pros:** Easy to edit.
- **Cons:** Not versioned with the code, easily outdated, not reviewable in pull requests.

### No formal record

- **Pros:** No overhead.
- **Cons:** Decisions are forgotten and relitigated. AI assistants lack the context needed to respect past decisions.

## Consequences

### Positive

- Decisions are discoverable, versioned and reviewed like code.
- AI coding agents can be instructed to read ADRs before making changes (see `CLAUDE.md`).

### Negative

- Writing an ADR takes time.

### Neutral

- A template is provided in [`0000-template.md`](0000-template.md).
