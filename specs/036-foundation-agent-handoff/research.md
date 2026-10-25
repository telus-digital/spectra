# Research: Safe Handoffs Between the Foundation Agents

Every decision below is made against the current command text. Line references are to `spectra/commands/`
as of extension 1.24.0.

## R1 — The `-source` folders and their template

**Decision**: An imported policy source goes to exactly one of four series folders:
`<root>/domain-analysis-source/`, `<root>/engineering-methodology-source/`, `<root>/test-strategy-source/`,
or `<root>/deployment-strategy-source/`. Its filename is `NNN-<kebab-title>.md`.

Its template resolves `<kind>-source-template` through the five layers, then falls back to
`kb-document-template`. This is kb-vault's existing rule for any non-reserved category (`kb-vault.md:211-214`),
applied with the folder name as the category. No new template ships.

In kb-vault's reserved map, the four singleton rows are replaced by one row:

> a domain analysis, engineering methodology, test strategy, or deployment strategy →
> `<root>/<kind>-source/`, `NNN-<kebab-title>.md`, `<kind>-source-template`, else `kb-document-template`

That row also names the owning command per kind. It is still "reserved" because the category slug is
fixed: kb-vault must not invent `test-strategies/` or `qa-policy/` for these four kinds.

**Rationale**:
- Principle VII requires one artifact type per subfolder and a numbered series for anything that is not
  a named singleton.
- The `-source` suffix keeps the folder visibly distinct from the standing document it feeds. It also
  avoids `test-strategy/`, the pre-1.19.0 legacy location of `TEST_STRATEGY.md` that test-strategy still
  reads (`test-strategy.md:235-246`).
- Not shipping a template keeps the change small. A project that wants a specific shape for a kind adds
  one override file.

**Alternatives considered**:
- *Use the feeder's template for the source document.* Rejected: those templates carry Constitution input
  and decision sections whose format the feeder owns. A source document shaped like a decision record is
  the very confusion this feature removes.
- *Ship four `-source` templates.* Rejected as unneeded. `kb-document-template` already has Substance,
  Rules & Decisions Recorded, Gaps, and Provenance.

## R2 — How kb-vault refers and refuses

**Decision**:
- A source of one of the four kinds always produces a source-document row (create, or update of an
  existing source document under kb-vault's normal Step 7 rules). The row's Notes name the owning
  command.
- The report's item 9 ("Sources referred on", `kb-vault.md:474-476`) lists each, with the command.
- Step 7's methodology-only exception (`kb-vault.md:332-338`) is generalised. A singleton is never a
  match candidate at all, for any of the four and whoever wrote it, so no update row can target one.
- When the user directs a create or a redirection at a singleton path, kb-vault answers as it already
  does for out-of-scope destinations (`kb-vault.md:247-260`). It says which agent owns the file, names
  the `-source` destination it will use, and keeps the row there.
- The "may change" list at the gate (`kb-vault.md:409-412`) gains one restriction: a row cannot be
  retargeted at a singleton.
- The `ENGINEERING_METHODOLOGY.md` paragraph after the reserved map (`:300-302`) is removed. It describes
  behaviour that no longer exists.

**Rationale**: Each refusal reuses an existing kb-vault mechanism, so the gate rules ("any change
re-enters the gate", "a subset may be approved") need no new cases.

**Alternatives considered**: *Allow writing a singleton when none exists yet.* Rejected. FR-001 says
"whatever the user asks". Also, an imported file at the singleton path is exactly what domain-analyzer
and test-strategy misread today.

## R3 — How a feeder recognises its own file

**Decision**: All four feeders write `command: speckit.spectra.<agent>` as the first front-matter key, as
methodology already does (`methodology.md:551-556`). A file at the feeder's canonical path is classified
in this order:

1. **Own prior run**: the header has `command: speckit.spectra.<agent>`.
2. **Own prior run from an earlier version**: no `command:` key, but the header has that version's
   command-owned signature:

   | Feeder | Earlier-version signature |
   |---|---|
   | domain-analyzer | a `lenses:` mapping whose keys are domain-analyzer lens slugs, or a `constitution_input:` count; or the pre-1.23.0 checkbox file at `.specify/memory/domain-analysis.md` (already handled) |
   | test-strategy | `amendment_state:` together with a `lenses:` mapping holding `unit` / `integration` |
   | deployment-strategy | `amendment_state:` together with its deployable / class keys |
   | methodology | none needed: it has always written the key |

3. **Another agent's file**: a `command:` key naming a different agent. This cannot happen at a canonical
   path under correct use. Report it and write nothing.
4. **Not written by this feeder**: hand-written, or written by kb-vault before 1.25.0. kb-vault never
   wrote command-owned front matter, because front matter is command-owned and not part of any template
   (`test-strategy-template.md` header comment). Read it as `claimed` evidence. Before the round, outside
   the counted questions, ask for consent to replace it. If consent is declined, or the run is
   non-interactive, write nothing and show the document in the session. This is methodology's rule
   (`methodology.md:209-224`), extended to the other three.

**Rationale**: Recognition never forces a needless consent question on upgrade (case 2), and never
inherits decisions a file did not record (case 4). One key with one meaning across four commands is also
what kb-vault and review-pr can rely on.

**Alternatives considered**: *Key only, no signature fallback.* Rejected by clarification Q4. Every
existing project would see a one-time consent prompt for its own files.

## R4 — The documented-intent label

**Decision**: An imported document is cited with the provenance **`claimed`**, meaning "what a document
says, which the code does not confirm". The word already ships in deployment-strategy's R1
(`deployment-strategy.md:73-86`). Applied per command:

- **deployment-strategy**: no new vocabulary. Its `-source` folder is added to the documents it reads, and
  everything there is `claimed` until the repository confirms it.
- **test-strategy**: R1 grows from three provenances to four: citation, `claimed`, `convention`, `stated`.
  A `claimed` item never moves a measured figure, as R7 already says for answers.
- **domain-analyzer and methodology**: their candidate record keeps its keys and order. An evidence item
  pointing at an imported document is written as `claimed: \`path\``. Current-practice paragraphs label
  such citations the same way. A candidate whose only evidence is `claimed` has basis `aspirational`.

**Rationale**:
- One word across four documents means a reader learns it once.
- Reusing a shipped word means no existing test or document changes meaning.
- Putting the label on the evidence item, rather than adding a key, keeps the candidate record's
  fixed key order, which review-pr and later runs depend on.

**Alternatives considered**: *A new word, "intent".* Rejected: it would leave deployment-strategy with two
words for one idea. *A new `evidence_kind:` key.* Rejected: it changes the command-owned record format
for no reader's benefit.

## R5 — How feeders find imported documents

**Decision**: Each feeder adds one numbered input to its Step 1. It reads:
- **its own `-source` folder** by path: `<root>/domain-analysis-source/`, and so on; and
- **any other document under the artifact root whose Provenance section names kb-vault as its origin**,
  where it touches the feeder's ground.

It lists every one in its consulted inputs. The path read is the reliable one: it does not depend on a
project's template keeping a Provenance heading. The Provenance read catches material kb-vault filed under
another category, such as an `operating-procedures/` document relevant to methodology.

Source documents stay `claimed` for as long as they exist. A feeder never edits, moves, or deletes one.

**Rationale**: It meets FR-006 with no repository-wide search beyond the documentation tree the feeders
already traverse.

**Alternatives considered**: *A machine marker in kb-vault output.* Rejected for now. The path plus
Provenance is enough, and a marker would be a third front-matter contract to keep.

## R6 — The Constitution input format for the two strategies

**Decision**: test-strategy's Steps 12–13 and deployment-strategy's Steps 9–10 keep their embedded /
partial / absent analysis. Three things change.

**1. The goal is stated first.** Each run opens, after the non-interactive announcement, with the same
`Constitution: … Goal: create | update` line domain-analyzer uses (`domain-analyzer.md:72-85`). The
`no constitution` state now means goal **create** (draft the full set) instead of "draft nothing, offer
no gate".

**2. The draft becomes guardrail records.** Each drafted item is a record in a `Constitution input`
section, in domain-analyzer's shape:

```markdown
## Constitution input

Goal: **create** the constitution at `.specify/memory/constitution.md` from the guardrails below.

### <Target constitution section>

- <Guardrail statement, as accepted>
  - id: `ts-<section-slug>-<hash>`
  - placement: add | amends: <Principle name/number>
  - basis: observed | aspirational
```

The full record of every drafted guardrail, accepted or not, sits in the section the template already
has for the amendment, renamed **Constitution input**, before the accepted list. Its keys, in order, are:
statement, id, section, basis, decision, status. IDs follow the domain-analyzer rule (`:214-220`): the
section slug and an 8-character hash of the normalised statement, computed once, then frozen. The
prefixes are `ts-` and `ds-`.

**3. The hand-off is worded for the goal**, with deployment-strategy's line mirroring this:

```text
/speckit-constitution Create the project constitution from the "Constitution input" section of docs/TEST_STRATEGY.md, placing each guardrail in its section
/speckit-constitution Amend the constitution with every guardrail in the "Constitution input" section of docs/TEST_STRATEGY.md, adding each under its section and applying "amends:" items as amendments to the principle they name
```

What stays the same:
- The UAT clause in test-strategy (`test-strategy.md:653-667`) becomes one record like any other.
- deployment-strategy's "invariants only, the document is referenced, environment names never become
  obligations" rule (`:564-566`) is unchanged and now applies to records.
- `amendment_state:` stays in both headers with its values, because tests and the CHANGELOG pin it.
  `none` keeps its meaning (no constitution); the goal now reads `create` alongside it. A
  `constitution_input:` count is added, as domain-analyzer has.

**Rationale**: It matches the shape `/speckit-constitution` and review-pr already consume for the other two
feeders, with the smallest edit to each command.

**Alternatives considered**: *Replace the embedded / partial / absent analysis with suppression and
"amends" only.* Rejected. Embedded and partial are how these two commands quote the governing clause, and
the tests pin it. They map cleanly: embedded means suppress; partial means `amends:` or `add` for the gap.

## R7 — Decisions from the approval gate

**Decision** (clarification Q1): The gate keeps its three paths: approve, modify the strategy first, or
talk it through.
- **Approve** accepts every guardrail shown. The same reply may name guardrails to decline (recorded
  `declined`) or reword (recorded `accepted` with the new wording and the same ID).
- **Declining the gate as a whole** records every guardrail `skipped`, so it is offered again on the
  next run.
- **No answer, or a non-interactive run**, records every guardrail `not_asked`.
- **Modify the strategy first** re-drafts, keeping the IDs of unchanged statements, and returns to the
  gate.

On a re-run:
- a `declined` record is never offered as new;
- a `skipped` or `not_asked` record is offered again;
- an `accepted` record the constitution now asserts becomes `adopted: <principle>` and leaves
  Constitution input. It is never reverted, and drift is reported.

These are domain-analyzer's re-run rules (`:485-511`) word for word.

**Rationale**: It needs no new question (out of scope) and gives per-guardrail control through free text,
the same channel the other feeders use.

## R8 — Migrating the checkbox format

**Decision**: On a re-run that finds a "Proposed constitution amendment" section with `- [ ]` / `- [x]`
items:
- every `- [x]` item becomes `accepted`;
- every `- [ ]` item becomes `not_asked` (undecided), offered again and marked "unticked in the earlier
  version";
- every statement keeps its wording, and its `section:` / `status:` lines map to section / placement;
- IDs are assigned once, from the statement as found;
- the file is rewritten in the new format;
- the report says it was migrated, with counts.

This mirrors domain-analyzer's pre-1.23.0 rule (`domain-analyzer.md:517-521`).

**Rationale**: An unticked box cannot distinguish "rejected" from "never reviewed". Treating it as
declined would bury a guardrail nobody looked at (spec Assumptions).

## R9 — The FR-024 conflict

**Finding**: FR-024 asks kb-vault's template list to include `engineering-methodology-template` and
`deployment-strategy-template`. After R1, kb-vault's reserved map uses no feeder template, so including
them would contradict FR-001/FR-002 and Principle VIII's "first readable layer" rule for what kb-vault
actually resolves.

**Decision**: kb-vault's Step 4 list names exactly the reserved-map templates (`adr-template`,
`brd-template`, `impact-analysis-template`, `defect-rca-template`), and then the `<category>-template` →
`kb-document-template` rule that covers the `-source` folders. A test asserts that the list and the map
agree in both directions. This meets User Story 5's acceptance scenario ("every template the map names
appears in the list and the list names none the map does not use").

**Spec effect**: FR-024's wording needs to change. The user decides that through `/speckit.clarify`; the
plan does not edit the spec (Principle I).

## R10 — The onboarding-sequence documentation

**Decision**: The sequence is hand-written prose: a short numbered procedure plus two explanatory
paragraphs, in a new "Starting on an existing codebase" section in each of `README.md`,
`spectra/README.md`, and `docs/index.html`. It covers:
- kb-vault (optional) → domain-analyzer → constitution (create) → methodology → constitution (amend) →
  test-strategy → constitution (amend) → deployment-strategy → constitution (amend);
- why the constitution runs after each feeder;
- declaring `Artifact root:` in the first constitution run, with the publication-check caveat;
- one line on greenfield: the same order, kb-vault usually skipped.

A new `tests/test_onboarding_sequence.py` extracts the ordered command names from each surface and
asserts:
- all three are identical;
- they match the next-agent order methodology already prints (`methodology.md:690-695`);
- each names `Artifact root:`.

**Rationale**: Principle V's generated-or-written line is drawn at structured listings of agents taken
from the roster. This is a procedure that interleaves a non-roster step (`/speckit-constitution`) and
explains why, so it is written. The landing page rule against hard-coding the roster is not engaged: the
page still renders the roster from `agents-list.json`, and this section is guidance text. The test gives
the consistency a generator would, without adding an ordering field to the roster schema.

**Alternatives considered**: *Add an `onboarding_order` to `agents-list.json` and generate the
sequence.* Rejected: it puts a procedure into a roster schema whose consumers (the CLI and the landing
page) have no use for it, for a list of four.

## R11 — Version and changelog

**Decision**: extension 1.24.0 → 1.25.0 (MINOR), mirrored in `catalog.json`. The command count stays at
14. `[1.25.0]` sections:
- **Changed**: kb-vault routing; the feeders' `claimed` reading; the two strategies' Constitution input,
  create goal, and migration; review-pr accepted-only for the two strategies.
- **Fixed**: kb-vault's template list.
- **Documentation**: the onboarding sequence.

The descriptions in each changed command's front matter, in `extension.yml`, and in the
`docs/index.html` cards are updated where they state changed behaviour. Examples: test-strategy's "draft
the constitution amendment", and kb-vault's reserved map mention.

**Rationale**: Principle VI / Publishing standards. No rename or removal, so the change is not MAJOR.
