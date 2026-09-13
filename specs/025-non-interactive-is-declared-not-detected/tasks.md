# Tasks: Non-Interactive Is Declared, Never Detected

**Input**: [spec.md](./spec.md), [plan.md](./plan.md)

**Branch**: `025-non-interactive-is-declared-not-detected`

---

## Phase 0 — Verification of the premise

- [X] T001 Confirm the sentence exists in exactly two commands and nowhere else in `spectra/`:
  `grep -n "piped input\|no terminal\|automated runner" spectra/commands/*.md`.
- [X] T002 Confirm it was inherited rather than introduced by 1.17.0: `git show 1a671e9` carries it without the flag
  clause, and 1.17.0 appended only `or an explicit --non-interactive`.
- [X] T003 Confirm 1.17.0 raised its cost — the round is gated on it at `test-strategy.md:596`, where 1.16.0 gated
  only the coverage run and the amendment.
- [X] T004 Confirm the graceful path does not depend on the detection: Step 5 already records an unanswered question
  as not asked without classifying the session (D5).
- [X] T005 Note the pinned literals in both suites before editing, so the rewrite does not trip one:
  `tests/test_test_strategy_flow.py` and `tests/test_test_plan_flow.py`.

**Checkpoint**: the defect is understood, its blast radius is two files, and the safe path already exists.

---

## Phase 1 — User Story 1: a real session gets asked (P1)

- [X] T006 Replace the detection sentence in `## Non-interactive mode` of `spectra/commands/test-strategy.md` with a
  declaration rule: interactive unless declared, the two declarations named as the complete set (FR-001, FR-002, D2).
- [X] T007 State why inference is forbidden — the reader cannot observe a terminal, a pipe, or what launched the run —
  and remove `piped input`, `no terminal`, and `automated runner` as criteria rather than rewording them
  (FR-003, FR-004, D1).
- [X] T008 State the asymmetry that justifies the default: one unanswered question against the whole interaction, and
  that a wrong guess explains itself in the document as though it were a finding (FR-005, D4).
- [X] T009 Add the instruction to ask when in doubt (FR-006).
- [X] T010 Point at the unanswered-question path as the reason the default is safe, so nobody reintroduces the
  criteria to protect against hanging (FR-008, D5).
- [X] T011 Apply T006–T008 and T010 to `spectra/commands/test-plan.md`, without the ask-when-in-doubt line, and word
  the new asymmetry so it does not collide with the create-versus-rewrite asymmetry already below the list.

**Checkpoint**: neither command asks the reader to classify a session, and both say why.

---

## Phase 2 — User Story 2: a declared automated run still stays silent (P1)

- [X] T012 Confirm `test-strategy`'s consequence list is untouched: no questions asked, no coverage run, the
  non-publishing root, the document written, the amendment drafted and recorded not asked (FR-007, D3).
- [X] T013 Confirm `test-plan`'s consequence list is untouched, including that an existing plan is not rewritten and
  that its create-versus-rewrite paragraph still reads correctly after T011 (FR-007, D3).
- [X] T014 Confirm the `--non-interactive` flag documentation in both `## User Input` sections is unchanged — the
  argument surface does not move in this change.

---

## Phase 3 — Tests (FR-009)

- [X] T015 Extend `tests/test_test_strategy_flow.py` with the declaration rule, the stated reason, the asymmetry, and
  the ask-when-in-doubt instruction.
- [X] T016 Add the mutation guard to `tests/test_test_strategy_flow.py`: the three removed phrases may appear only as
  prohibitions, so assert the command does not instruct the reader to detect them.
- [X] T017 Extend `tests/test_test_plan_flow.py` with the same declaration rule, reason, and guard.
- [X] T018 Mutation-check both: restore the old detection sentence in each command and confirm the suites fail by
  name, then revert.

---

## Phase 4 — Release (Principle V, one change)

- [X] T019 Bump `extension.version` to `1.17.1` in `spectra/extension.yml`, preserving the two-space indent (FR-010).
- [X] T020 Mirror `version` and both `updated_at` fields in `catalog.json`. `provides.commands` stays `11` (FR-010).
- [X] T021 Add the `[1.17.1]` entry to `spectra/CHANGELOG.md` under `### Fixed`: what the sentence asked for, why a
  prompt cannot supply it, why the guess has a direction, and what replaced it (FR-010).
- [X] T022 Rebuild `docs/packages/spectra.zip` with `python3 tools/build_package.py` (FR-010).

---

## Phase 5 — Verification

- [X] T023 `python3 -m unittest discover -s tests` — full suite green.
- [X] T024 `python3 tools/generate_agent_docs.py --check` — no drift.
- [X] T025 `python3 tools/build_package.py` then `diff -r spectra /tmp/unzipped/spectra` — zip in sync.
- [X] T026 Run CI's version, command-count, and description-parity checks locally.
- [X] T027 Grep `spectra/` for the three removed phrases and confirm every remaining hit is a prohibition, the
  changelog entry, or documentation of them (SC-003).
- [X] T028 Install into a scratch project and confirm the shipped text: v1.17.1 installs, the declaration rule is
  present in both installed skills, and `Detect a session that cannot answer` appears nowhere.
- [ ] T028a **Open — belongs to the reporter.** Run `test-strategy` with no arguments in the harness that reproduced
  the defect and confirm the questions are asked with no non-interactive announcement (SC-001); then run with
  `--non-interactive` and confirm the announcement fires and nothing is asked (SC-002). This cannot be closed from a
  build: whether a given host's agent now reaches the right conclusion is observable only by running it there, which
  is precisely how the defect was found. Claiming it from a passing suite would repeat the error this spec exists to
  fix.
- [X] T029 Set the spec's **Status** to Implemented.

---

## Dependencies

- T001–T005 precede everything.
- T006 → T007 → T008 → T009 → T010 (one section, in order); T011 mirrors them into the second command.
- T012–T014 are confirmations over the result of Phase 1 and depend on it.
- T015–T017 depend on Phases 1 and 2; T018 depends on T015–T017.
- T019–T022 depend on every prose edit being final; T022 depends on T019.
- T023–T029 last. T028 depends on T022.
