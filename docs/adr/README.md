# Architecture Decision Records

This directory contains the Architecture Decision Records (ADRs) of the hello-world project.

An ADR captures an important architectural decision, along with its context and consequences. We follow the format described by Michael Nygard in [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

## Index

| ADR                                                                  | Title                                                | Status   | Date       |
| -------------------------------------------------------------------- | ---------------------------------------------------- | -------- | ---------- |
| [0001](0001-record-architecture-decisions.md)                        | Record architecture decisions                        | Accepted | 2026-09-15 |
| [0002](0002-use-python.md)                                           | Use Python                                           | Accepted | 2026-09-15 |
| [0003](0003-separate-greeting-composition-from-output.md)            | Separate greeting composition from output            | Accepted | 2026-10-06 |
| [0004](0004-single-module-layout.md)                                 | Single-module layout                                 | Accepted | 2026-10-06 |

## Creating a new ADR

Use the `/new-adr` Claude Code command, or copy [`0000-template.md`](0000-template.md) manually. ADRs are immutable once accepted: to change a decision, write a new ADR that supersedes the previous one.
