# Security Policy

## Reporting a vulnerability

Report privately using **GitHub private vulnerability reporting**: go to the repository's
[Security tab](https://github.com/telus-digital/spectra/security) and use the **Report a
vulnerability** button. This is available to any GitHub user, and the report is visible only to the
maintainer.

This is the only inbound channel for this repository. Issues and Discussions are disabled, so there
is no public tracker a report could be filed in — and filing one elsewhere in public would disclose
the vulnerability before it can be fixed.

Please include the affected component (the `spectra` extension or the `spectra` CLI), the version,
reproduction steps, and the impact you observed.

Reports are acknowledged within five business days where possible. Spectra is maintained by one
person; there is no on-call rotation behind that number.

## Scope

In scope:

- The `spectra` CLI (`spectra_cli/`), including the install flow and anything it executes
- Shipped agent commands under `spectra/commands/`, including prompt injection, unintended
  destructive file operations, and exfiltration of project contents
- The catalog and package distribution path (`catalog.json`, `docs/packages/spectra.zip`)

Out of scope:

- Vulnerabilities in [Spec Kit](https://github.com/github/spec-kit) itself — report those upstream
- Vulnerabilities in the AI coding agents Spectra runs against (Claude Code, Copilot, Cursor, and
  others) — report those to their vendors
- Output quality issues: an agent producing a wrong or incomplete answer is a bug, not a
  vulnerability. Spectra agents produce drafts for human review

Non-security bug reports and feature requests have no channel: this repository is published for use,
not for contribution. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for what that means in practice.

## Supported versions

The extension and the CLI version independently. Security fixes land on the latest version of each.
There are no long-term support branches.
