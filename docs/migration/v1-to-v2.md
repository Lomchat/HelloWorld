# Migrating from 1.x to 2.0

Version 2.0.0 separates the composition of the greeting from its output ([ADR-0003](../adr/0003-separate-greeting-composition-from-output.md)). This is a breaking change for programmatic users. Command-line users are not affected.

## Summary of breaking changes

| Area            | 1.x                                  | 2.0                                         |
| --------------- | ------------------------------------ | ------------------------------------------- |
| `greet()`       | Prints the greeting, returns `None`  | Returns the greeting, prints nothing        |
| Printing        | `greet()`                            | `main()`                                    |
| Console script  | `hello_world.hello_world:greet`      | `hello_world.hello_world:main`              |

## Step-by-step migration

### 1. You called `greet()` to print the greeting

**Before (1.x):**

```python
from hello_world import greet

greet()
```

**After (2.0):**

```python
from hello_world import main

main()
```

### 2. You captured stdout to obtain the greeting as a string

**Before (1.x):**

```python
import contextlib
import io

from hello_world import greet

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    greet()
greeting = buffer.getvalue().strip()
```

**After (2.0):**

```python
from hello_world import greet

greeting = greet()
```

### 3. You relied on the return value of `greet()` being `None`

This was never part of the documented API. If your code checks `greet() is None`, remove that check.

## Need help?

Open a [discussion](https://github.com/Lomchat/HelloWorld/discussions) or check the [FAQ](../../README.md#-faq).
