# Contract: how SPECTRA is described (FR-017, FR-018, FR-021)

## Canonical description

- **Long form** (ledes, README intro, meta descriptions): *SPECTRA is an extension by TELUS Digital that
  enhances [GitHub Spec Kit](https://github.com/github/spec-kit): agents that take spec-driven development
  across the entire software development lifecycle. You install and manage it with Spec Kit's own
  `specify` CLI.*
- **Footer tagline** (every docs page that has one): `SPECTRA · a Spec Kit extension by TELUS Digital`
- **Landing page `<title>`**: `SPECTRA — a Spec Kit extension by TELUS Digital`
- **Capability brief footer line**: `A TELUS Digital extension for GitHub Spec Kit · Human-gated by design`

Pages may word the long form to fit their context, but each must make the same three points: it is an
**extension**, it is **by TELUS Digital**, and it **enhances GitHub Spec Kit**.

Naming: uppercase `SPECTRA` for the product in new copy. Lowercase `spectra` appears only as the extension
id (`specify extension add spectra`, `speckit.spectra.*`).

## Trust claims (capability brief, README Supply chain)

| Card / bullet | Must say |
|---|---|
| Markdown only | The published extension is **14 command files and 13 templates**, plus its licence, notice, trademark policy and changelog. No scripts, no binaries, no post-install hooks. TELUS Digital ships no executable code: Spec Kit installs the files, and the agent you already approved runs them |
| No telemetry | SPECTRA makes no network calls of its own. Spec Kit fetches the public catalog and package when you install or update; nothing reports on you, your code or your project |
| Nothing to grant | Unchanged: public catalog, no login, token or elevated permissions |
| Auditable & pinnable | Unchanged in substance: commit `.specify/extension-catalogs.yml` |

The counts must equal `ls spectra/commands | wc -l` and `ls spectra/templates | wc -l` at implementation
time (SC-008).

## Banned in current docs

- "A curated catalog of Spec Kit extensions" (and "curated set" or "curated catalog" in any form)
- "A TELUS Digital platform"
- "installed as a uv tool", "One command installs it", "Install with uv"
- Any description of SPECTRA as a tool, command, or installer of its own

## Out of scope

Other tools' CLIs (`gh`, Claude Code, Kiro CLI, Gemini CLI, Codex CLI, the `specify` CLI), and agents that
classify a project as "a CLI". Historical records: `specs/`, `spectra/CHANGELOG.md`,
`docs/ip-audit-findings.md`.
