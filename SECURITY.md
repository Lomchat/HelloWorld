# Security Policy

## Supported Versions

Security fixes are provided for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.3.x   | :white_check_mark: |
| 2.2.x   | :white_check_mark: |
| 2.1.x   | :x:                |
| 2.0.x   | :x:                |
| < 2.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues, discussions or pull requests.**

Instead, report them privately through [GitHub Security Advisories](https://github.com/Lomchat/HelloWorld/security/advisories/new).

Please include as much of the following information as possible:

- The type of issue (e.g. terminal injection, output tampering, supply chain)
- The affected version(s)
- Step-by-step instructions to reproduce the issue
- The exact bytes written to stdout (`python -m hello_world | od -c`)
- The potential impact of the issue

## Response Timeline

| Step                      | Target           |
| ------------------------- | ---------------- |
| Acknowledgment            | 48 hours         |
| Initial assessment        | 5 business days  |
| Fix for critical issues   | 14 days          |
| Public disclosure         | After the fix is released, coordinated with the reporter |

## Security Model

The output of hello-world is written directly to the user's terminal. Our threat model therefore focuses on **output integrity**:

- The output must never contain terminal escape sequences, control characters or bidirectional overrides. This is verified against 22 known injection vectors and every C0 control character by the security test suite (`tests/security/`).
- The output must never be influenced by the environment (locale, terminal, color settings, arbitrary variables). This is verified by the environment isolation tests.
- The output is pinned by MD5, SHA-1, SHA-256 and CRC32 fingerprints in the conformance test suite (`tests/conformance/`).

### Supply chain

- hello-world has **zero runtime dependencies**.
- Development dependencies are monitored by Dependabot.
- Releases are built in CI from tagged commits only.

## Acknowledgments

We are grateful to the security researchers who help keep hello-world and its users safe.
