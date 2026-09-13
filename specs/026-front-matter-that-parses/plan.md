# Implementation Plan: Front Matter That Parses

**Branch**: `026-front-matter-that-parses` | **Date**: 2026-09-12 | **Spec**: [spec.md](./spec.md)

## Summary

One prose paragraph replaced with a worked example. `test-strategy` described its front matter in sentences —
"the coverage-of-analysis statement", "the amendment state", five questions with four fields each — and a real run
produced two YAML violations: an unquoted scalar containing colon-space, and a key carrying both a scalar and a
nested block. The section becomes a literal YAML block with quoting and enumeration rules, following `impact`, which
has shown rather than described its front matter since it shipped and has never produced this defect. What the front
matter carries is unchanged.

## Technical Context

**Language/Version**: Markdown command prompt; Python 3.9+ for tests

**Primary Dependencies**: unchanged — and notably **no YAML parser**, which the zero-dependency constraint forbids

**Testing**: `python3 -m unittest discover -s tests`; `tools/generate_agent_docs.py --check`

**Constraints**: Markdown only; agent-agnostic; the front matter must keep every field it carries today; the answers
stay in the header because Principle VIII can delete the body's copy

**Scale/Scope**: one step rewritten in one command, one template comment, one new test class with a two-rule checker,
version sync

## Evidence

| Claim | How it was verified |
|---|---|
| Two distinct violations, not one | The reported error is at `amendment_state` (unquoted colon-space); `clarification_round` four lines later carries a scalar *and* a block, which fails independently of it |
| The cause is prose, not the fields | `test-strategy.md:465` names contents in sentences and shows no shape; the run recorded exactly what it was asked for |
| "Terse" was already there and lost | The same paragraph ends "keep the front matter terse", and the run still emitted a three-line `coverage_of_analysis` |
| `impact` is immune for a structural reason | `impact.md:594` is a literal `yaml` block — short scalars, clean nesting, `questions_asked: 4` as a count rather than a narrative |
| `test-plan` has no exposure | Its Step 11 emits a Markdown identifying block; the file contains no front-matter emission |
| No other document command emits YAML | `adr`, `brd`, `defect-rca`, `kb-vault` carry Markdown status lines and document-control sections |
| Defect 1 predates 1.17.0 | `amendment_state` and `coverage_of_analysis` are in 1.16.0's front-matter list; defect 2 arrived with the round |

## Constitution Check

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `026-front-matter-that-parses`. |
| II. Single Self-Contained Extension | ✅ | No files added or removed. |
| III. Agent-Agnostic Commands | ✅ | A YAML block in a prompt is content, not an agent's syntax. |
| IV. Context-Aware by Default | ✅ | Unaffected. |
| V. Catalog and Package in Sync | ✅ | Manifest, catalog, changelog, and zip move together. Roster untouched. |
| VI. Two Versioned Channels | ✅ | Extension channel only: 1.17.1 → 1.17.2. No tag; root `VERSION` untouched. |
| VII. Documents Under One Declared Root | ✅ | Unaffected. |
| VIII. Shaped by Overridable Templates | ✅ | This is VIII respected. The answers stay in front matter *because* an override may delete the body section holding them — the fix reshapes the header rather than relocating the record. |

**Amendment classification**: none.

**Extension version classification**: PATCH — 1.17.1 → 1.17.2. No capability, argument, or section changes; one
rendering failure is removed.

## Phase 0 — Decisions

- **D1 — Show, do not describe.** The prose failed while containing its own corrective ("keep the front matter
  terse"). A worked example removes the judgement call: the reader copies a shape rather than inventing one from a
  list of nouns. This is the entire fix; everything else is the rules that make the example unambiguous.

- **D2 — Copy `impact`, which already works.** Same repository, same problem, no defect in its lifetime, and the only
  structural difference is that it shows a literal block. Adopting a sibling's proven form beats inventing a third.

- **D3 — Enumerate what was a sentence.** `amendment_state` became a paragraph and took a colon with it. It becomes
  one of `embedded | partial | absent | none | not_asked`; `disposition` becomes
  `answered | default_taken | not_asked`. Nothing is lost, because the proposed-amendment section already carries the
  state, the clause, the conflict, and the approval in full — the header was repeating it.

- **D4 — Quote every free-text value.** Not "quote values containing colons", which asks the reader to scan for one.
  A blanket rule needs no judgement and cannot be applied incorrectly.

- **D5 — One key, counts plus a sequence.** `clarification:` holds `asked`, `answered`, and `questions:`. The scalar
  that sat on `clarification_round` alongside its block moves into the counts, where it was always trying to be.

- **D6 — Prose belongs in the body.** `coverage_of_analysis` is a figure in the header and a paragraph in the sources
  section — where it already existed, in full, while the header duplicated it badly.

- **D7 — Check two failure modes, not YAML.** The suite is standard-library only, so there is no parser available and
  writing one would be a much larger, much less honest thing than this fix deserves. The two defects that actually
  occurred are both detectable with a few lines over the command's own example block, which is also the block a
  reader will copy.

## Phase 1 — Design notes

`spectra/commands/test-strategy.md`, Step 10: the prose paragraph is replaced by a `yaml` example carrying every field
the document has today, plus four rules — it must parse; free text is quoted; a key is a scalar or a collection, never
both; anything that would run to a paragraph goes in the body. The "answers are in front matter on purpose" paragraph
stays, because D-VIII's reasoning is unchanged and someone will otherwise try to fix this by deleting the block.

`spectra/templates/test-strategy-template.md`: the "what this template cannot change" comment gains the parse
requirement, since front matter is command-owned and an override must not be read as licence to reshape it.

`tests/test_test_strategy_flow.py`: a `FrontMatterParses` class asserting the rules are stated, plus
`_yaml_defects()` — a checker for exactly two conditions over the example block, with a mutation guard so a
reintroduced paragraph value fails the build.

## Risks

| Risk | Mitigation |
|---|---|
| The example drifts from the fields the document actually carries | The test walks the example block, so a field named in Step 10 and missing from it is visible; the block is the single source of the shape |
| A future editor "fixes" this by removing the answers from front matter | D-VIII's paragraph stays directly beneath the block with its reason, and a test asserts the questions are still there |
| The two-rule checker is mistaken for a YAML validator | Named and documented as a check over two known defects, in the class docstring and in the spec's Assumptions |
| A quoted value containing a quote is emitted unescaped | D4 states the rule as *quoted*, and the edge case is recorded in the spec rather than assumed away |

## Complexity Tracking

> No violations. One paragraph becomes one example block; no field added or removed, no new surface.
