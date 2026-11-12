# =============================================================================
# hello_world.py - Core implementation of the Hello World application
# =============================================================================
#
# Overview
# --------
# This module contains the complete business logic of the application. When
# executed, it writes the canonical greeting, "Hello, World!", followed by a
# single line feed, to standard output.
#
# The implementation consists of exactly one statement. This is a deliberate
# architectural decision, documented in ADR-0009 ("Reduce the implementation
# to a single statement"), which supersedes ADR-0003 and ADR-0006.
#
# Execution
# ---------
# The module can be executed in two ways:
#
#   1. Through the package entry point: `python -m hello_world`
#      (see src/hello_world/__main__.py).
#   2. As a standalone script, by running this file directly.
#
# Design principles
# -----------------
#   * Simplicity: the shortest correct implementation is the easiest one to
#     read, review, test and maintain (KISS, YAGNI).
#   * Single source of truth: the greeting is defined exactly once, inline,
#     where it is used.
#   * Zero dependencies: only built-in functions are used. No import is
#     required.
#   * Statelessness: the module defines no variable, no function and no class.
#     It has no state that could be corrupted or shared between threads.
#
# Output contract
# ---------------
# The output is part of the public API and MUST remain byte-exact:
#
#   48 65 6c 6c 6f 2c 20 57 6f 72 6c 64 21 0a
#   H  e  l  l  o  ,     W  o  r  l  d  !  LF
#
# This contract is enforced by the conformance test suite (tests/conformance/),
# including SHA-256, SHA-1, MD5 and CRC32 fingerprints of the greeting.
#
# Security considerations
# -----------------------
# The greeting is a string literal. It cannot be influenced by environment
# variables, command-line arguments, the locale or any other external input,
# which makes terminal injection impossible by construction (see SECURITY.md).
#
# Error handling
# --------------
# No explicit error handling is performed. If standard output is closed or
# unavailable, the exception propagates to the interpreter, which reports it
# and exits with a non-zero status. This is the expected behavior for a
# command-line application.
#
# Performance
# -----------
# The statement executes in constant time, O(1), and allocates no memory
# beyond the string literal, which is interned at compile time.
#
# Maintenance notes
# -----------------
#   * IMPORTANT: Do not add any other statement to this module. The test suite
#     verifies that it contains exactly one statement (tests/unit/).
#   * Do not add a module docstring: it would count as a second statement.
#   * Do not split the greeting into several arguments: print() would insert
#     a space between them (see #57).
#   * Do not append a line feed to the greeting: print() already terminates
#     the line (see #73).
#
# =============================================================================

# Print the greeting to standard output.
# The built-in print() function appends a single line feed and honors any
# redirection of sys.stdout, which keeps this statement testable in-process
# (see ADR-0008).
print("Hello, World!")  # noqa: T201 - Printing the greeting is the purpose of this application.
