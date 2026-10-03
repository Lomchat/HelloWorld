---
description: Add a regression test for a fixed issue
argument-hint: "<issue-number> <short description of the bug>"
---

Add a regression test for issue $ARGUMENTS.

1. Open `tests/regression/test_known_issues.py` and read the existing tests to match their style.
2. Add a new test function named `test_issue_<number>_<snake_case_description>`.
3. Its docstring MUST start with `#<number>:` followed by a one-sentence description of the original bug, in the past tense.
4. The test MUST fail on the buggy behavior and pass on the current code. Explain in your report how you verified this.
5. Keep the tests sorted by issue number.
6. Run `.venv/bin/pytest -m regression`, then `make check`.

Never modify or delete an existing regression test.
