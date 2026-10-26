# Contract: Generated outputs

Every row is written by `python3 tools/generate_agent_docs.py` and verified by `--check`. Text outside
a region or line target is hand-written and left byte-identical. Every write uses `\n` line endings.

| # | File | Target | Content | FR |
| --- | --- | --- | --- | --- |
| 1 | `agents-list.json` | whole file | `{"schema_version","phases","agents"}`, keys in today's order, `json.dumps(indent=2, ensure_ascii=False) + "\n"` | FR-007, FR-008 |
| 2 | `README.md` | `readme-agents-table` | Agents table and the Spec Kit sentence (unchanged renderer) | FR-009 |
| 3 | `AGENTS_LIST.md` | `agents-list-shipped` (new) | Per shipped agent, in roster order: `<!-- SPECTRA:AGENT id=<id> -->`, `### <title> ✅`, ``**`<command>`** — <lead>``, further prose, item list, `#### <guide>` sections | FR-010 |
| 4 | `AGENTS_LIST.md` | `agents-list-speckit-core` | Unchanged renderer | FR-009 |
| 5 | `AGENTS_LIST.md` | `agents-list-roadmap` | Unchanged renderer | FR-009 |
| 6 | `spectra/README.md` | `spectra-readme-commands` | Unchanged renderer | FR-009 |
| 7 | `spectra/README.md` | `spectra-readme-agents` (new) | Per shipped agent: ``## `<command>` — <title>``, lead, further prose, item list, `### <guide>` sections, then `---` | FR-015 |
| 8 | `spectra/extension.yml` | line: `description:` under `- name: "speckit.spectra.<id>"` | `      description: "<manifest>"` with `\` → `\\` and `"` → `\"` | FR-012 |
| 9 | `spectra/commands/<id>.md` | line: `description:` in the opening `---` block | `description: "<manifest>"`, same escaping | FR-017 |
| 10 | `docs/getting-started/agents.html` | `agents-page-nav` (new) | Sidebar links, see [agents-page-markup.md](agents-page-markup.md) | FR-011 |
| 11 | `docs/getting-started/agents.html` | `agents-page-cards` (new) | Cards, see [agents-page-markup.md](agents-page-markup.md) | FR-011, FR-014 |

Rows 3 and 7 carry the same text for every agent; only the framing differs (research D4).

## Region markers

The existing marker syntax, in both Markdown and HTML:

```text
<!-- SPECTRA:GENERATED START id=<region> -->
<!-- Generated from agents/ — do not edit by hand. Run: python3 tools/generate_agent_docs.py -->
…
<!-- SPECTRA:GENERATED END id=<region> -->
```

## Command-line interface (unchanged surface)

| Invocation | Behaviour | Exit |
| --- | --- | --- |
| `generate_agent_docs.py` | Validate the source; on success, write every stale output and print `rewrote <path>` per file, or `every generated output was already current` | 0, or 1 on any error (nothing is written when the source is invalid) |
| `generate_agent_docs.py --check` | Validate and compare; write nothing; print one line per problem: stale output, source error, manifest mismatch, unknown command on a narrative page | 0 / 1 |

Every error line starts with the repository-relative path, followed by `:<line>` where a line applies.
`tools/checks.py generated-listings` keeps calling `run(check=True)`, so CI and `ship.py` need no
change.
