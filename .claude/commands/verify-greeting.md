---
description: Run the full verification pipeline and confirm the greeting is byte-exact
allowed-tools: Bash(make check), Bash(python -m hello_world), Bash(od -c), Bash(./scripts/verify_output.sh)
---

Verify the integrity of the Hello World output. Follow these steps in order and do not skip any of them.

1. Run `make check` and confirm that lint, type checking and the full test suite pass with 100% coverage.
2. Run `./scripts/verify_output.sh` and confirm that it reports success.
3. Run `python -m hello_world | od -c` and confirm that the output is exactly:

   ```
   0000000   H   e   l   l   o   ,       W   o   r   l   d   !  \n
   0000016
   ```

4. Confirm that nothing is written to stderr.

Report the results as a table with one row per step (✅ / ❌), followed by a one-line verdict.

If any step fails, do NOT attempt to fix anything. Report the failure with the exact output and wait for instructions.
