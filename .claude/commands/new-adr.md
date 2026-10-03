---
description: Create a new Architecture Decision Record
argument-hint: "<title of the decision>"
---

Create a new Architecture Decision Record titled: $ARGUMENTS

1. List `docs/adr/` and find the highest ADR number. The new ADR gets the next number, zero-padded to 4 digits.
2. Copy `docs/adr/0000-template.md` to `docs/adr/NNNN-<kebab-case-title>.md`.
3. Fill in every section: Context, Decision, Alternatives Considered (at least two, each with pros and cons), Consequences (positive, negative and neutral).
4. Set the status to `Proposed` and the date to today.
5. Add the ADR to the index table in `docs/adr/README.md`.
6. If the decision supersedes an existing ADR, update the status of the old ADR to `Superseded by ADR-NNNN` and link both ways.

Do not implement the decision. ADRs are reviewed before implementation.
