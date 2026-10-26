# Research: One Source of Truth for Every Agent

The Technical Context had no open unknowns. This file records the design decisions it left open and
the facts about today's files that drove each one.

## Findings about today's files

| Fact | Consequence |
| --- | --- |
| `json.dumps(data, indent=2, ensure_ascii=False) + "\n"` reproduces `agents-list.json` byte for byte | SC-003 can be asserted as byte equality, not just "equal in meaning" |
| Key order in every entry is `id, title, description, status, phase, type, provider, command`; planned entries without a command omit the key | The generator emits keys in that fixed order and omits `command` when absent |
| Roster order is grouped by phase, in phase order (all 55 entries) | Order = (phase position, within-phase position); no global sequence needed |
| `AGENTS_LIST.md` lists shipped agents in a *different* order from the roster (ADR first) | Generated order becomes roster order (FR-010 says roster order); a one-time reorder, visible in the diff |
| Flow tests slice `AGENTS_LIST.md` between `<!-- SPECTRA:AGENT id=… -->` markers | The generated region keeps emitting one such marker before each agent |
| Flow tests slice `spectra/README.md` from ``## `speckit.spectra.<x>` `` to the next `\n## ` | Per-agent heading stays `` ## `<command>` — <title> ``; guides use `###` |
| Flow tests slice a card from `<span class="name">…</span>`, read `class="cdesc"` up to the next `</span>`, and expect the first `<pre><code>` to hold the bare command | Card markup is frozen as a contract (contracts/agents-page-markup.md); one `<pre><code>` per example line; the lead renders inline only |
| `AGENTS_LIST.md` items are `- **Label** — text`, but some are `- **Label.** text` (no dash) | The joiner is " — " unless the label ends in `.`, `?` or `!`, which reproduces both forms |
| `spectra/README.md` per-agent prose uses numbered lists (97 lines), one table, fenced code with `bash`/`text` info strings, `###` subsections and `---` separators; `AGENTS_LIST.md` uses none of those except fences | The Markdown subset must include ordered lists and tables (see Spec refinements) |
| Manifest and command-file descriptions are one-line double-quoted YAML strings | Both are rendered as `description: "<value>"` with `\` and `"` escaped |
| Test files in `tests/test_generator.py` assert today's *mechanism* (prose anchors, title containment, "descriptions deliberately not compared") | Those tests are replaced, not kept; see Spec refinements on SC-004 |

## Decisions

### D1 — Header format

- **Decision**: The file opens with a `---` line, then one `key: value` per line, then a closing
  `---`. The value is everything after the first `": "`, trimmed, taken literally: no quoting, no
  escaping, no multi-line values. Keys: `id, title, command, provider, type, phase, order, status,
  summary, manifest`.
- **Rationale**: Editors and GitHub render `---` blocks as front matter, so it is readable everywhere.
  Splitting on the first `": "` carries summaries containing colons, quotes and em dashes unchanged
  (spec edge case). Parsing it takes about 20 lines with no third-party parser (FR-003).
- **Alternatives**: TOML (`tomllib` is 3.11+, and the floor is 3.9); YAML (needs PyYAML); JSON blocks
  (hostile to prose editing).

### D2 — How order is expressed (spec Assumption "Order")

- **Decision**: An `order:` integer header field gives the position within the agent's phase. Agents
  sort by (phase position in `_phases.md`, `order`, then `id` as a tie-break that is rejected as a
  duplicate). Seeding assigns 10, 20, 30, … in today's order. Phase order is the order of entries in
  `_phases.md`.
- **Rationale**: Adding an agent stays a one-file change (SC-002); gaps of 10 let an agent be inserted
  without renumbering. Global order is already grouped by phase, so a per-phase number reproduces it
  exactly.
- **Alternatives**: An order list in `_phases.md` (adding an agent then touches two files); a
  file-name prefix (`10-adr.md`) (breaks "named by id", FR-001); a global sequence number (any insert
  renumbers everything).

### D3 — Body structure

- **Decision**: For a shipped Spectra agent, the body has this structure, using only `##` headings:

  1. **Lead**: the first paragraph, required, inline formatting only.
  2. **Further prose**: optional; paragraphs, lists, tables, code.
  3. **Items**: `##` sections, from `## Arguments` through `## Examples` inclusive.
     - `Arguments` is required, first, and a single paragraph.
     - `Use it when` is required and second.
     - Any further labelled items follow.
     - `Examples` is required, last, and exactly one fenced code block with one invocation per line.
  4. **Guides**: `##` sections after `Examples`, optional, any blocks.

  Position decides kind: a `##` section before or at Examples is an item; one after Examples is a
  guide.
- **Rationale**: Items reproduce the labelled-bullet facts of `AGENTS_LIST.md`. Guides carry the
  README-only walkthroughs (template overrides, upgrade notes, "Somewhere other than `docs/`?") that
  FR-015 moves into the source, which do not fit inside a bullet. A single heading level keeps the
  source flat and readable.
- **Alternatives**: `###` for guides (renders as nested under Examples on GitHub); a per-section kind
  marker (more syntax for the maintainer to learn).

### D4 — How each output renders the body (identical text, different framing)

| Part | `AGENTS_LIST.md` | `spectra/README.md` | Card | Full reference (on the card) |
| --- | --- | --- | --- | --- |
| Heading | `### <title> ✅` after `<!-- SPECTRA:AGENT id=… -->` | ``## `<command>` — <title>`` | `<h3>` | — |
| Lead | `**`<command>`** — <lead>` | `<lead>` | `.cdesc` span | `<p>` |
| Further prose | as written | as written | — | HTML |
| Items | `- **Label** — text` list | same list | Arguments → `.args`; Examples → one `<pre><code>` per line | `<ul>` of labelled items |
| Guides | `#### <title>` + blocks | `### <title>` + blocks | — | `<h4>` + blocks |
| Separator | blank line | `---` | — | — |

The Examples label is "Example (Claude)" for one line and "Examples (Claude)" for more, as today.
Source line breaks are kept as written. The generator re-indents (continuation lines of an item get
two spaces) but never rewraps, so diffs stay small and the maintainer's wrapping is respected.

### D5 — Markdown subset and HTML rendering

- **Decision**: `tools/markdown_subset.py` parses blocks and inline spans. It renders blocks back to
  Markdown (for re-indentation) and to HTML.
  - **Blocks**: paragraph, bulleted list, ordered list, nesting by two- or three-space indent, fenced
    code with an optional info string, pipe table, and `##` headings (in source only).
  - **Inline**: code spans, `**bold**` → `<b>`, `*italic*` → `<i>`, `[text](url)` with http(s) or
    relative URLs, and a backslash escape.
  - **Escaping**: all text is escaped with `html.escape` before inline markup is applied. Code spans
    are extracted first so their contents are never interpreted.
  - **Rejected with `file:line`**: any other heading level; blockquotes; images; reference-style links;
    raw HTML, meaning a `<` followed by a letter or `/` outside a code span (GitHub would swallow it
    as a tag); HTML entities (write the character); an unterminated `**`, `*` or code span; and
    `javascript:` or other non-http link schemes.
- **Rationale**: This is the subset the prose actually uses. Rejecting raw `<tag>` keeps GitHub's
  rendering and the site's rendering identical. `<b>`/`<i>` match today's card markup and CSS.
- **Alternatives**: A third-party Markdown library (breaks the zero-dependency rule); a regex-only
  converter (cannot nest lists or reject reliably).

### D6 — Regions and line-level outputs

| Output | Mechanism | Region / target |
| --- | --- | --- |
| `agents-list.json` | whole file | — |
| `README.md` | region | `readme-agents-table` (unchanged) |
| `AGENTS_LIST.md` | regions | `agents-list-shipped` (new), `agents-list-speckit-core`, `agents-list-roadmap` |
| `spectra/README.md` | regions | `spectra-readme-commands`, `spectra-readme-agents` (new) |
| `docs/getting-started/agents.html` | regions | `agents-page-nav`, `agents-page-cards` (new; same comment markers) |
| `spectra/extension.yml` | line | the `description:` line of each `- name: "speckit.spectra.<x>"` entry |
| `spectra/commands/<x>.md` | line | the `description:` line inside the opening `---` block |

Line-level targets must be found exactly once. A missing or duplicated target fails with the file
named, just as a missing marker does today. The notice comment changes to "Generated from agents/ —
do not edit by hand".

### D7 — Check scope

- **Decision**: `--check` renders everything in memory and reports, without writing:
  - each output that differs (FR-018);
  - every source validation error (FR-021);
  - any mismatch between manifest commands and shipped sources (FR-019);
  - every `speckit.spectra.<name>` or `/speckit-spectra-<name>` in `docs/**/*.html` or `docs/**/*.md`,
    and in the text outside generated regions of `README.md` and `spectra/README.md`, whose `<name>`
    the source does not ship (FR-024). Generated pages under `docs/` are scanned too: a deliberate
    superset of FR-024, which costs nothing and would catch a renderer bug.
  The roster dict built from the source is passed through `spectra_cli.roster.parse(…, strict=True)`
  before anything is written.
- **Rationale**: It stays one check, so `tools/checks.py generated-listings`, its CI step, and the
  `Catalog and package stay in sync` job are unchanged (FR-020). A hand edit and a stale output are the
  same failure: the output differs from the render.
- **Removed checks**: `check_prose_anchors` and `check_title_containment` existed only because prose was
  hand-written. Generation now guarantees both.

### D8 — Seeding (FR-016)

- **Decision**: Seeding is done once, during implement:
  1. A one-off script (`specs/040-agent-single-source/seed/seed_headers.py`) writes every header from
     `agents-list.json` and `extension.yml`, with `order` = 10, 20, … per phase. It writes
     `_phases.md` and the header-only files for core and planned agents.
  2. For each of the 14 shipped agents, the implementer writes the body: the `AGENTS_LIST.md` block is
     the base (lead and items). README-only material becomes guides, and README sentences that only
     restate the base are dropped.
  3. A second one-off script (`seed/seed_report.py`) splits every old copy (the `AGENTS_LIST.md` block,
     the README section, the card, the old command-file description) into sentences. It normalizes
     whitespace and Markdown/HTML markup, and lists every sentence not found verbatim in the new
     source, per agent and per copy, in `seeding-report.md`.
  The scripts stay in the feature directory as provenance and are never run again.
- **Rationale**: The merge needs judgement (which README paragraph is a restatement), so a person or
  agent does it. The report needs to be exhaustive, so a script does it (FR-016's "nothing is
  discarded without appearing in that report").
- **Alternatives**: A `--seed` flag on the generator (one-time code in permanent tooling); a fully
  automatic merge (it would duplicate README restatements in both outputs).

### D9 — Collapsed Full reference

- **Decision**: Each card ends with `<details class="fullref"><summary>Full reference</summary>…</details>`
  holding the full body rendered to HTML: lead, further prose, items and guides. It is placed after
  the examples, so the first `<pre><code>` in a card is still the first example.
- **Rationale**: `<details>` opens without scripts (FR-011, SC-006). Placing it after the examples
  keeps the flow tests' slicing valid.

### D10 — Versioning

- **Decision**: The extension goes from 1.28.0 to 1.29.0 (minor), with a `spectra/CHANGELOG.md` entry, a
  `catalog.json` update, and a zip rebuild. The CLI `VERSION` is untouched.
- **Rationale**: Shipped text changes (README sections, the command descriptions Spec Kit shows) but
  behaviour does not. The descriptions users see change, so this plan takes a minor bump rather than a
  patch. Principle VI forbids moving the CLI for it.

## Spec refinements this plan implies

These follow from the clarified decisions and have been folded into the spec (2026-10-25).

1. **FR-004**: guides, the further titled sections, come *after* Examples (D3). FR-004 currently
   places them between Use it when and Examples. Short labelled items still sit there.
2. **FR-013**: the subset adds ordered lists and pipe tables (D5). The README material that FR-015
   moves into the source uses both.
3. **SC-004**: "existing tests pass unchanged in what they assert" covers the tests that read the
   roster, the full reference, the extension README, and the Agent reference page, which are the
   content tests. `tests/test_generator.py`'s mechanism tests for prose anchors, title containment,
   and "descriptions are deliberately not compared" test behaviour this feature removes on purpose,
   and are replaced.
