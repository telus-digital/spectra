# Tasks: Front Matter That Parses

**Input**: [spec.md](./spec.md), [plan.md](./plan.md)

**Branch**: `026-front-matter-that-parses`

---

## Phase 0 — Verification of the premise

- [X] T001 Confirm both violations in the reported document: `amendment_state` carries an unquoted scalar containing
  colon-space, and `clarification_round` carries a scalar followed by a nested block. Each fails independently.
- [X] T002 Confirm the cause is the prose at `spectra/commands/test-strategy.md:465` — contents named in sentences,
  no shape shown, and "keep the front matter terse" already present and overridden.
- [X] T003 Confirm `impact.md:594` shows a literal `yaml` block with short scalars and clean nesting, and has never
  produced this defect (D2).
- [X] T004 Confirm `test-plan` has no exposure: Step 11 emits a Markdown identifying block, and the file contains no
  front-matter emission.
- [X] T005 Confirm no other document command emits YAML front matter — `adr`, `brd`, `defect-rca`, `kb-vault` use
  Markdown status lines and document-control sections.

**Checkpoint**: two defects, one command, and a working sibling to copy.

---

## Phase 1 — User Story 1: the document renders (P1)

- [X] T006 Replace the front-matter prose in Step 10 of `spectra/commands/test-strategy.md` with a literal `yaml`
  example block carrying every field the document has today (FR-002, D1, D2).
- [X] T007 State the four rules above the block: it must parse as YAML; every free-text value is quoted; a key takes a
  scalar or a collection, never both; anything that would run to a paragraph goes in the body
  (FR-001, FR-003, FR-004, FR-009, D4, D6).
- [X] T008 Make `amendment_state` an enumerated scalar and say where the explanation lives (FR-005, D3).
- [X] T009 Make `disposition` an enumerated scalar — `answered`, `default_taken`, `not_asked` (FR-006, D3).
- [X] T010 Give the clarification record one key holding counts and a `questions:` sequence with fixed field names, so
  no key carries a scalar beside a block (FR-007, D5).
- [X] T011 Reduce `coverage_of_analysis` to a short quoted value and point at the sources section for the prose
  (FR-009, D6).

**Checkpoint**: the shape is shown, not described, and every rule that makes it unambiguous is stated.

---

## Phase 2 — User Story 2: the record still survives an override (P2)

- [X] T012 Keep the "answers are in front matter on purpose" paragraph directly beneath the block, with its reason, so
  nobody resolves a future parse problem by deleting the record (FR-008, Principle VIII).
- [X] T013 Confirm the example still carries every question, its recommendation, its answer, and its disposition, so
  the header alone remains sufficient (FR-008, SC-003).
- [X] T014 Add the parse requirement to the "what this template cannot change" comment in
  `spectra/templates/test-strategy-template.md`, avoiding the literals the suite asserts are absent from the template.

---

## Phase 3 — Tests (FR-010)

- [X] T015 Add `FrontMatterParses` to `tests/test_test_strategy_flow.py` asserting the four rules are stated and the
  enumerations are present.
- [X] T016 Add `_yaml_defects()` — a checker over the command's own example block for exactly two conditions: an
  unquoted scalar containing colon-space, and a key whose scalar value is followed by a more-indented sequence.
  Document in the class docstring that it is a two-defect check and not a YAML parser (D7).
- [X] T017 Assert the example block itself passes that checker, and that it carries every field Step 10 names.
- [X] T018 Mutation-check: put a paragraph value with a colon back into the example, confirm the suite fails by name,
  then revert. Repeat with a scalar-plus-block key.

---

## Phase 4 — Release (Principle V, one change)

- [X] T019 Bump `extension.version` to `1.17.2` in `spectra/extension.yml` (FR-011).
- [X] T020 Mirror `version` in `catalog.json`; `provides.commands` stays `11` (FR-011).
- [X] T021 Add the `[1.17.2]` entry to `spectra/CHANGELOG.md` under `### Fixed`: the two violations, why prose in a
  machine-readable header produces them, and why the answers stay in the header (FR-011).
- [X] T022 Rebuild `docs/packages/spectra.zip` with `python3 tools/build_package.py` (FR-011).

---

## Phase 5 — Verification

- [X] T023 `python3 -m unittest discover -s tests` — full suite green.
- [X] T024 `python3 tools/generate_agent_docs.py --check` — no drift.
- [X] T025 `python3 tools/build_package.py` then `diff -r spectra /tmp/unzipped/spectra` — zip in sync.
- [X] T026 Run CI's version, command-count, and description-parity checks locally.
- [X] T027 Re-run the checker against the **reported** document's front matter and confirm it reproduces both
  defects — a checker that does not catch the bug that prompted it is not a check.
- [X] T028 Confirm no front-matter value in the example exceeds a short line (SC-004).
- [X] T029 Set the spec's **Status** to Implemented.

---

## Dependencies

- T001–T005 precede everything.
- T006 → T007 → T008 → T009 → T010 → T011 (one section, in order).
- T012–T014 depend on Phase 1.
- T015–T017 depend on Phases 1 and 2; T018 depends on T016 and T017.
- T019–T022 depend on every prose edit being final; T022 depends on T019.
- T023–T029 last. T027 depends on T016.
