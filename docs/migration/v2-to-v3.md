# Migrating from 2.x to 3.0

Version 3.0.0 reduces the implementation to a single statement ([ADR-0009](../adr/0009-reduce-the-implementation-to-a-single-statement.md)). This is a breaking change for programmatic users and for users of the `hello-world` console script.

## Summary of breaking changes

| Area             | 2.x                                   | 3.0                                     |
| ---------------- | ------------------------------------- | --------------------------------------- |
| `GREETING`       | Module-level constant                 | Removed                                 |
| `greet()`        | Returns the greeting                  | Removed                                 |
| `main()`         | Prints the greeting, returns `0`      | Removed                                 |
| Console script   | `hello-world`                         | Removed: use `python -m hello_world`    |
| `python -m`      | `python -m hello_world`               | Unchanged                               |
| Output           | `Hello, World!\n`                     | Unchanged                               |

## Step-by-step migration

### 1. You used the `hello-world` command

**Before (2.x):**

```console
$ hello-world
Hello, World!
```

**After (3.0):**

```console
$ python -m hello_world
Hello, World!
```

### 2. You called `main()` to print the greeting

**Before (2.x):**

```python
from hello_world import main

main()
```

**After (3.0):**

```python
import runpy

runpy.run_module("hello_world", run_name="__main__")
```

### 3. You used `greet()` or `GREETING` to obtain the greeting as a string

**Before (2.x):**

```python
from hello_world import greet

greeting = greet()
```

**After (3.0):**

```python
greeting = "Hello, World!"
```

The greeting is part of the public, byte-exact output contract and is guaranteed not to change within a major version. It is therefore safe to use the string literal directly.

## Need help?

Open a [discussion](https://github.com/Lomchat/HelloWorld/discussions) or check the [FAQ](../../README.md#-faq).
