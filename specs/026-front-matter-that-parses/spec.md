# Feature Specification: Front Matter That Parses

**Feature Branch**: `026-front-matter-that-parses`

**Created**: 2026-09-12

**Status**: Implemented

**Input**: Maintainer report while testing 1.17.1 — a generated `TEST_STRATEGY.md` failed to render. "Failed to parse
frontmatter: Nested mappings are not allowed in compact mappings at line 10, column 18." The document was otherwise
correct; the reader could not display it.

## Current State (verified against 1.17.1)

`spectra/commands/test-strategy.md:465` describes the document's front matter in prose:

> Front matter carries: the mode; a generation timestamp including the time of day; the surfaces; the resolved
> template path; the coverage-of-analysis statement; the amendment state from Step 13; and the answers from Step 5 —
> each question with the answer you recommended, the answer taken, and whether it was **answered**, **default
> taken**, or **not asked**.

Nothing there says the result must parse as YAML, and nothing shows a shape. It asks for a "statement", an "amendment
state", and five questions with four fields each, then adds "keep the front matter terse" — a hint, and hints lose to
the surrounding instruction to record everything. A real run produced two distinct violations:

**1. An unquoted scalar containing a colon.** The reported error, at line 10:

```yaml
amendment_state: PARTIAL - drafted and APPROVED by the user in this session. Not written to the constitution: this command never writes that file.
```

The second `: ` makes YAML read a nested mapping inside a mapping. Any scalar containing colon-space must be quoted,
and a value that is a paragraph will eventually contain one.

**2. A key carrying both a scalar and a block.** Four lines later, and fatal independently:

```yaml
clarification_round: all five answered - the first run of this document for which that is true
  - q: 0
```

A key takes a scalar or a nested collection, never both.

The blast radius is one command. Of the eight document producers:

| Command | Emits | Exposure |
|---|---|---|
| `test-strategy` | YAML front matter, described in prose | **both defects** |
| `impact` | YAML front matter, shown as a literal example block | none — every value is a short scalar, every nested collection is a clean block |
| `test-plan` | a Markdown identifying block, not YAML | none |
| `adr`, `brd`, `defect-rca`, `kb-vault` | Markdown status lines and document-control sections | none |

`impact` is the precedent worth copying and the reason this is a `test-strategy` defect rather than a house one: it
**shows** the front matter instead of describing it, so there is nothing to improvise.

**Provenance.** `amendment_state` and `coverage_of_analysis` were in the 1.16.0 front-matter list, so defect 1 has been
latent since this agent shipped — it needed an amendment state long enough to contain a colon. `clarification_round`
arrived in 1.17.0, and defect 2 is entirely its own.

**Supersession.** This replaces the front-matter clause of FR-039 in
[020-test-strategy-agent](../020-test-strategy-agent/spec.md) and the front-matter addition made by
[024-test-strategy-clarification-round](../024-test-strategy-clarification-round/spec.md). What front matter must
*carry* is unchanged; what changes is its shape and the requirement that it parse.

## Clarifications

- Q: Should the answers move out of front matter and live only in the body?
  → A: No. They are there because Principle VIII lets a project override delete the body section that holds the table,
  and front matter is the only part of the document the command owns. The placement was right; the shape was wrong.

- Q: Why show a literal block rather than tighten the prose?
  → A: Because the prose is what failed. "Keep the front matter terse" was already there and lost to the instruction
  to record five questions with four fields each. A worked example removes the judgement call: the reader copies a
  shape instead of inventing one. `impact` has done it that way since it shipped and has never produced this defect.

- Q: Is a paragraph-valued key ever acceptable?
  → A: Not in front matter. A paragraph belongs in the body, where it can be read. `coverage_of_analysis` became a
  three-line paragraph in a machine-readable header while the same information sat in the sources section — the header
  should carry the figure and let the section carry the prose.

- Q: Does an enumerated `amendment_state` lose information?
  → A: Only from the header, which is not where a human reads it. The proposed-amendment section already carries the
  state, the governing clause, the conflict, and the approval in full. A header field that repeats a paragraph is what
  broke the document.

- Q: The tests are standard-library only. How is YAML validity asserted without a parser?
  → A: By checking the two known failure modes over the command's own example block, not by implementing YAML. A
  targeted check over a closed set of defects is honest; a partial parser pretending to be general is not.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The document renders (Priority: P1)

A maintainer opens `TEST_STRATEGY.md` in any reader that understands front matter — an editor preview, a static site
generator, a documentation pipeline. It renders. The front matter parses, and the fields in it are values a machine
can use.

**Why this priority**: it is the reported defect, and it makes the whole document unreadable in the tools people
actually use to read it. A strategy nobody can open is worth less than one that was never written.

**Independent Test**: generate a document with every question answered and an amendment approved, then parse its front
matter with any YAML reader.

**Acceptance Scenarios**:

1. **Given** a generated document, **When** its front matter is parsed, **Then** it parses.
2. **Given** an amendment state that would previously have been a sentence, **When** the header is read, **Then** it
   carries a short enumerated value and the explanation is in the proposed-amendment section.
3. **Given** five recorded answers, **When** the header is read, **Then** they are a properly nested sequence under a
   single key, with no scalar on that key.
4. **Given** any free-text value, **When** the header is read, **Then** it is quoted.

### User Story 2 - The record still survives a template override (Priority: P2)

A project overrides the template and deletes the sources-and-coverage section. The clarification answers are still
recoverable from the document.

**Why this priority**: it is the reason the answers are in front matter at all, and a fix that quietly dropped them to
protect the parser would trade one silent loss for another.

**Independent Test**: override the template without that section, generate, and confirm every question and disposition
is still present in the header.

**Acceptance Scenarios**:

1. **Given** a template with no sources-and-coverage section, **When** the document is generated, **Then** the header
   still carries every question, its recommendation, the answer, and the disposition.
2. **Given** the header's question entries, **When** they are compared with the body's table, **Then** they agree.

### Edge Cases

- **An answer contains a colon** — quoted, like every other free-text value. This is the common case, not an exotic
  one: a recommendation of the form "integration-heavy: the logic is at the boundaries" is natural phrasing.
- **A question was not asked** — the entry is still present with `disposition: not_asked`. An absent entry and a
  not-asked entry are different claims.
- **No coverage tooling exists, so there was no coverage question** — the counts reflect it and the entry says so.
  There is still no scalar-plus-block.
- **An answer contains a double quote** — the reader escapes it, as YAML requires. The rule is the value is quoted,
  not that it is assumed safe.
- **A value would run to a paragraph** — it belongs in the body. The header takes the short form.

## Requirements *(mandatory)*

- **FR-001**: The command MUST state that the document's front matter has to parse as YAML.
- **FR-002**: The command MUST show the front matter as a literal example block rather than describing its contents in
  prose.
- **FR-003**: Every free-text value MUST be quoted.
- **FR-004**: No key may carry both a scalar value and a nested collection.
- **FR-005**: `amendment_state` MUST be a short enumerated value, with the explanation left to the
  proposed-amendment section.
- **FR-006**: `disposition` MUST be a short enumerated value: answered, default taken, or not asked.
- **FR-007**: The clarification record MUST be a single key holding counts and a sequence of per-question entries with
  fixed field names.
- **FR-008**: The front matter MUST still carry every question and its disposition, so the record survives a template
  override that removes the body's copy.
- **FR-009**: Prose MUST NOT appear as a front-matter value. Where a field would run long, the header carries the
  short form and the body carries the detail.
- **FR-010**: The test suite MUST assert the stated rules and MUST check the command's own example block for both
  known failure modes — an unquoted scalar containing colon-space, and a key with a scalar followed by a nested block.
- **FR-011**: The extension version MUST bump to `1.17.2` — no capability changes, one rendering failure removed —
  with manifest, catalog, changelog, and zip in sync.

## Success Criteria *(mandatory)*

- **SC-001**: A generated strategy document opens in a front-matter-aware reader without error.
- **SC-002**: The command contains a front-matter example that itself passes both failure-mode checks.
- **SC-003**: Every question and disposition remains recoverable from the header alone.
- **SC-004**: No front-matter field in the example is longer than a short line.
- **SC-005**: `python3 -m unittest discover -s tests`, `tools/generate_agent_docs.py --check`, and a
  `tools/build_package.py` rebuild all pass.

## Assumptions

- Command files are prompts: a shape shown is followed more reliably than a shape described, which is the whole
  content of this fix and is what distinguishes `impact` from `test-strategy` today.
- Readers of these documents vary — editor previews, static site generators, documentation pipelines — and the only
  thing they agree on is that front matter is YAML. Emitting valid YAML is therefore not a preference.
- The tests do not need a YAML parser to be useful here. Two known failure modes, checked over a known block, catch
  the regression that actually happens.
