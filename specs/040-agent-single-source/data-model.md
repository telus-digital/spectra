# Data Model: One Source of Truth for Every Agent

## Entities

### Phase (`agents/_phases.md`)

One header block per phase, in order. The block's position in the file is the phase's order.

| Field | Type | Rules |
| --- | --- | --- |
| `id` | slug `[a-z0-9-]+` | unique |
| `title` | text | non-empty |
| `aidlc` | text | non-empty (`Inception`, `Construction`, `Operations` today) |

The file is a sequence of `---` … `---` blocks with nothing between them except blank lines.

### Agent (`agents/<id>.md`)

| Field | Required | Rules | Roster key |
| --- | --- | --- | --- |
| `id` | always | slug; equals the file name without `.md`; unique | `id` |
| `title` | always | non-empty | `title` |
| `command` | when the agent has one | `speckit.<name>` or `speckit.spectra.<name>`; may repeat across agents (Implementation/Testing) | `command` (omitted when absent) |
| `provider` | always | `speckit` or `spectra` | `provider` |
| `type` | always | `core` or `add-on` | `type` |
| `phase` | always | an `id` from `_phases.md` | `phase` |
| `order` | always | positive integer; unique within its phase | — (determines position) |
| `status` | always | `available` or `planned` | `status` |
| `summary` | always | one line, non-empty | `description` |
| `manifest` | iff shipped | one line; only on shipped agents | — (extension.yml + command file) |

**Derived**
- *shipped* = `provider == spectra` and `status == available`.
- *position* = (phase order, `order`).
- *number* = 1-based index among shipped agents in position order (card `01`–`14`).

**Body rules**
- Shipped: the body is required and follows [contracts/agent-source-format.md](contracts/agent-source-format.md).
- Every other agent: the body must be empty. Whitespace only is allowed.
- A shipped agent's `command` must be `speckit.spectra.<id>`, registered in the manifest, with a command file at `spectra/commands/<id>.md`.

### Body (shipped agents only)

| Part | Cardinality | Content |
| --- | --- | --- |
| Lead | 1 | one paragraph, inline formatting only |
| Further prose | 0..n blocks | paragraph, list, table, code |
| Item `Arguments` | 1, first | one paragraph, optionally followed by one list |
| Item `Use it when` | 1, second | paragraph(s) or list |
| Other items | 0..n | any blocks; label is the heading text |
| Item `Examples` | 1, last item | exactly one fenced code block; ≥ 1 non-empty line |
| Guides | 0..n, after Examples | any blocks; title is the heading text |

### Generated output

| Field | Meaning |
| --- | --- |
| path | repository-relative file |
| kind | `whole` / `region <id>` / `line <selector>` |
| render | function of the loaded source → text |

The full list is in [contracts/generated-outputs.md](contracts/generated-outputs.md).

### Seeding report entry (`seeding-report.md`, one-time)

| Field | Meaning |
| --- | --- |
| agent | id |
| copy | `AGENTS_LIST.md` / `spectra/README.md` / card / command-file description |
| sentence | the old sentence, normalized |
| outcome | `dropped` / `reworded` / `merged`, with a pointer to the new location where one exists |

## Validation (each failure names file, and line or field)

1. A file under `agents/` that is not `_phases.md` and not `<slug>.md`.
2. A missing or unterminated header, or a header line without `": "`.
3. An unknown key, a duplicate key, or a missing required key.
4. A value violating its rule (enum, slug, integer, phase reference).
5. A duplicate `id`, or a duplicate `(phase, order)` pair.
6. A body on a non-shipped agent, or a missing body on a shipped agent.
7. A body structure violation: no lead, missing or out-of-order Arguments, Use it when or Examples,
   Arguments longer than one paragraph, or Examples not exactly one code block.
8. Markdown outside the subset (see research D5), reported at its source line.
9. A shipped command not registered in `spectra/extension.yml`, or a registered command with no shipped
   source.
10. A narrative page under `docs/` naming a Spectra command the source does not ship.
11. The built roster failing `spectra_cli.roster.parse(…, strict=True)`.

## State transitions

An agent goes from `planned` (header only) to `available` (header plus body, plus `manifest`, plus a
manifest registration and command file) in one change. Going back the other way removes the body and
`manifest` in the same change. The generator enforces both directions through rules 6 and 9.
