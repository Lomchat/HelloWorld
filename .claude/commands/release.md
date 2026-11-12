---
description: Prepare a new release (version bump, changelog, tag)
argument-hint: "major | minor | patch"
allowed-tools: Bash(make check), Bash(git status), Bash(git diff:*), Bash(git log:*), Bash(git commit:*), Bash(git tag:*)
---

Prepare a **$ARGUMENTS** release of hello-world.

1. Make sure the working tree is clean (`git status`). If it is not, stop and report.
2. Run `make check`. If anything fails, stop and report.
3. Read the current version from `__version__` in `src/hello_world/__init__.py` and compute the next version according to Semantic Versioning and the requested bump ($ARGUMENTS).
   - `major`: breaking change to the output or to the entry points.
   - `minor`: backwards-compatible addition.
   - `patch`: backwards-compatible bug fix.
4. Update `__version__` in `src/hello_world/__init__.py`.
5. In `CHANGELOG.md`, move the `[Unreleased]` entries to a new `## [X.Y.Z] - YYYY-MM-DD` section (today's date) and update the comparison links at the bottom of the file.
6. Run `make check` again: `tests/unit/test_package.py` verifies that the version matches the changelog.
7. Show the full diff and ask for confirmation.
8. Once confirmed, commit with `chore(release): vX.Y.Z` and create an annotated tag `vX.Y.Z`.

NEVER push. The release workflow is triggered by the maintainers when they push the tag.
