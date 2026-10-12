# ADR-0005: Defer internationalization

- **Status:** Accepted
- **Date:** 2026-10-12
- **Deciders:** @maintainers

## Context

Several users have requested localized greetings (e.g. `Bonjour, le monde !`, `¡Hola, mundo!`, `Hallo, Welt!`). Supporting multiple languages raises non-trivial questions:

- **Locale detection:** `LANG`, `LC_ALL`, `LC_MESSAGES`, or an explicit option?
- **Typography:** French requires a narrow no-break space before `!`. Spanish requires an inverted exclamation mark at the beginning. Some scripts are written right-to-left.
- **Security:** non-ASCII output would invalidate several security and conformance guarantees (ASCII-only output, absence of bidirectional control characters).
- **Contract:** the output is a public, byte-exact contract. Making it locale-dependent is a breaking change for every downstream consumer.

## Decision

We will **not** implement internationalization at this time. The output remains `Hello, World!` regardless of the locale. This is enforced by the environment isolation tests in `tests/security/` and `tests/e2e/`.

## Alternatives Considered

### gettext catalogs

- **Pros:** Standard, mature tooling.
- **Cons:** Adds `.po`/`.mo` files and a build step. Translations must be maintained.

### Hard-coded dictionary of translations

- **Pros:** No tooling required.
- **Cons:** Does not scale, mixes content and code, breaks ADR-0006 (single source of truth).

## Consequences

### Positive

- The output contract remains stable and byte-exact on every platform.

### Negative

- Non-English users cannot get a localized greeting.

### Neutral

- Internationalization remains on the roadmap and will be reconsidered in a future major version.
