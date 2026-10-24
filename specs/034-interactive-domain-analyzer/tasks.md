# Tasks: An Interactive Domain Analyzer That Feeds the Constitution

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/domain-analyzer-behaviour.md](./contracts/domain-analyzer-behaviour.md),
[quickstart.md](./quickstart.md)

**Branch**: `034-interactive-domain-analyzer`

**Tests**: requested — the spec's SC-006 and the contract pin every behaviour in
`tests/test_domain_analyzer_flow.py` (`F`) and `tests/test_doc_output_paths.py` (`P`), stdlib `unittest`.
Within each story, the test task comes first.

**Working-tree status**: the implementation was written before this spec (plan, Complexity Tracking). Every
task except those marked **OPEN** describes a change already present in the working tree — verify it against
the file and the contract item, then check it off. **OPEN** tasks are real remaining work: T021 and T023–T025
(the FR-020 clarification, contract item 23), T036–T037 (`review-pr` reads only accepted guardrails, FR-022,
contract item 25), and T038 (commit and ship).

**Format**: `- [ ] [ID] [P?] [Story] Description` — `[P]` = different file, no dependency on an incomplete task.

All command edits are in `spectra/commands/domain-analyzer.md`, so command tasks run in sequence; locate each
site by its heading.

---

## Phase 1: Setup — verify the premise

- [X] T001 Confirm the 1.22.0 behaviour the spec's Current State table cites with `git show main:spectra/commands/domain-analyzer.md`: every candidate written `- [ ]`, no fixed lens set, constitution checked only in Step 6
- [X] T002 [P] Confirm `.specify/memory/constitution.md` Principle VII names `<artifact-root>/DOMAIN_ANALYSIS.md` as a singleton and `.specify/memory/domain-analysis.md` as its earlier location (research R1)

**Checkpoint**: the defects exist as described.

---

## Phase 2: Foundational — shared surface every story relies on

- [X] T003 Rewrite the command's front-matter `description`, intro, "The one rule that governs everything", "User Input" (one flag: `--non-interactive`), "What this command never does" table, and rules R1–R4 in `spectra/commands/domain-analyzer.md`
- [X] T004 Keep Step 3 (artifact-root resolution) in `spectra/commands/domain-analyzer.md`: target `<artifact-root>/DOMAIN_ANALYSIS.md`, default `docs/DOMAIN_ANALYSIS.md`, declared root, publication check (asked before the round, outside the eight), non-publishing fallback, earlier location `.specify/memory/domain-analysis.md` read and left alone with the `git rm` command (contract 13–14)
- [X] T005 Rewrite Step 6 (template resolution, five layers, honour-not-repair, report path) in `spectra/commands/domain-analyzer.md`, adding: "If a template omits the Constitution input section, write it anyway as the final section and say so" (FR-021, contract 17)
- [X] T006 [P] Rewrite `spectra/templates/domain-analysis-template.md` with sections: Constitution status and goal; Inferred domain; one `##` per lens (seven); Constitution input; Decisions and sources — and the guidance comment naming what the template cannot change (contract 4)
- [X] T007 [P] Verify the path tests in `P SingletonOutputPaths` pass against the rewritten command in `tests/test_doc_output_paths.py` — `test_each_singleton_names_its_root_level_target`, `test_no_singleton_target_carries_a_sequence_number`, `test_each_singleton_reads_its_earlier_location`. The ready-prompt test in the same class waits for T013

**Checkpoint**: path, template, and guard rails in place.

---

## Phase 3: User Story 1 — Decide guardrails in the session, not in the file (P1) 🎯 MVP

**Goal**: eight questions, one per turn, ≥4 options with recommended and Skip; the file is written once, after.
**Independent test**: quickstart run A — no file until after question 8; file records each answer; Constitution input = accepted.

- [X] T008 [P] [US1] Add test classes `TheClarificationRound` and `TheDocument` to `tests/test_domain_analyzer_flow.py` pinning contract items 7–12, 15–16
- [X] T009 [US1] Write Step 5 "The clarification round" in `spectra/commands/domain-analyzer.md`: announce once; the eight-question table (domain, then lenses 1–7); one question per turn, "Question N of 8"; list candidates numbered `N.M` with basis, confidence, evidence; options Recommended set · Codify only what exists · Full set · Skip, exactly one recommended, coinciding option → Choose individually; free text valid, a reworded candidate keeps its ID (FR-008–FR-010)
- [X] T010 [US1] In Step 5, add the confirmation form for a question with nothing to choose — keeps its number, four options — and the domain question's four options (FR-011)
- [X] T011 [US1] In Step 5, add "Ways the round ends early": use your defaults → `default_taken`; Skip → `skipped`, adopts nothing; unanswered → `not_asked`, adopts nothing; non-answer → answer it and re-ask; and "Record every answer" with decision values `accepted`, `declined`, `skipped`, `not_asked` and how each option maps to them (FR-012, data-model Question)
- [X] T012 [US1] Write Step 7 in `spectra/commands/domain-analyzer.md`: write once "after the round, never before"; YAML front matter rules and shape (`mode`, `constitution`, `goal`, `domain`, `lenses` as `proposed`/`nothing_to_propose`, all eight questions with `disposition`, `constitution_input` count); candidate record with keys in order `id`, `section`, `evidence`, `basis`, `confidence`, `decision`, `status`; Constitution input = "decision is `accepted` and whose status is not `adopted: …`", grouped by section with `placement: add | amends:` and `basis` (FR-013–FR-015)

**Checkpoint**: US1 tests pass; quickstart run A steps 2–5 hold.

---

## Phase 4: User Story 2 — Know the run's goal from its first line (P1)

**Goal**: first output states constitution status and goal; handoff worded for the goal.
**Independent test**: quickstart runs A and B — first line and handoff differ.

- [X] T013 [P] [US2] Add test classes `TheGoalIsStatedFirst` and `TheHandoff` to `tests/test_domain_analyzer_flow.py`, and update `test_the_domain_analyzer_hands_off_with_a_ready_prompt` in `tests/test_doc_output_paths.py` to the create and amend prompts (contract 1–2, 18–20)
- [X] T014 [US2] Write Step 0 "Say what you found, before anything else" in `spectra/commands/domain-analyzer.md`: the two example first lines, version and principle count, empty/unreadable treated as absent, goal `create`/`update` carried to front matter and handoff (FR-001)
- [X] T015 [US2] Write Step 8 "Report and hand off" in `spectra/commands/domain-analyzer.md`: report order; create prompt and amend prompt as ready-to-paste lines linked to the written path; no command when Constitution input is empty; "Do not invoke `/speckit-constitution` yourself" (FR-016–FR-017)

**Checkpoint**: US2 tests pass.

---

## Phase 5: User Story 3 — A fixed set of lenses, honest about the code (P1)

**Goal**: seven lenses always worked; every candidate cited and tagged observed/aspirational; testing and deployment referred.
**Independent test**: a lens with nothing to propose still appears, says what was searched, and gets its question.

- [X] T016 [P] [US3] Add test class `SevenLensesAlwaysWorked` to `tests/test_domain_analyzer_flow.py` pinning contract items 3–6
- [X] T017 [US3] Write Step 1 (read the project, incl. sibling `TEST_STRATEGY.md` / `DEPLOYMENT_STRATEGY.md`; read source on brownfield; classify mode, never ask) and Step 2 (infer domain plus one alternative reading; sparse, ambiguous, regulated cases) in `spectra/commands/domain-analyzer.md`
- [X] T018 [US3] Write Step 4 "Work the seven lenses" in `spectra/commands/domain-analyzer.md`: lens table with what each examines and the constitution section it feeds; "Never omit a lens"; "Testing and deployment are referred, not proposed"; report current practice first on brownfield; candidate fields incl. `basis`; at most five candidates per lens; against an existing constitution — suppress, `amends:`, else `new` (FR-002–FR-007)
- [X] T019 [US3] In Step 5, add "If question 1 changes the domain, revisit every lens's candidates before asking question 2" in `spectra/commands/domain-analyzer.md` (US3 scenario 5)

**Checkpoint**: US3 tests pass.

---

## Phase 6: User Story 4 — Re-runs respect earlier decisions (P2)

**Goal**: pre-filled answers, no re-offered declines, frozen IDs, adopted marking, legacy files read.
**Independent test**: quickstart runs B and C.

- [X] T020 [P] [US4] Add test classes `IdentifiersAreFrozen` and `ReRunsRespectDecisions` to `tests/test_domain_analyzer_flow.py` pinning contract items 21–22
- [X] T021 [P] [US4] **OPEN** — Change `test_a_legacy_checkbox_file_is_read` in `tests/test_domain_analyzer_flow.py` to assert that a `- [x]` item is `accepted`, a `- [ ]` item is undecided and re-offered marked "unticked in the earlier version"; run it and watch it fail (contract 23, FR-020)
- [X] T022 [US4] Write "Re-running on a project you have analysed before" in `spectra/commands/domain-analyzer.md`: rewrite in place; index by recorded `id`; carry forward, never delete; match by ID or same intent in same section against every prior candidate; declined not re-offered (mention count); skipped/`not_asked` re-offered; pre-fill from prior answers; mark adopted, never revert, report drift; report counts (FR-018–FR-019)
- [X] T023 [US4] **OPEN** — In the same section of `spectra/commands/domain-analyzer.md`, replace the legacy bullet so a `- [ ]` item is recorded `not_asked` (undecided, not `declined`) and is offered again in its lens's question marked "unticked in the earlier version", with the reason: the old format cannot tell "reviewed and rejected" from "never reviewed"; keep IDs, wording, and `status`; rewrite in the new format. Make T021 pass
- [X] T024 [P] [US4] **OPEN** — Update the legacy sentence in `spectra/README.md` (domain-analyzer section, "A checkbox file from an earlier version…") to: ticked means accepted, unticked items are asked about again
- [X] T025 [P] [US4] **OPEN** — Update the "Earlier checkbox files are read, not lost" bullet in `spectra/CHANGELOG.md` `[1.23.0]` to: ticked is accepted, unticked is undecided and asked again

- [X] T036 [P] [US4] **OPEN** — Add a test to `tests/test_review_pr_flow.py` asserting `spectra/commands/review-pr.md` says "only accepted guardrails are standards" and that a `declined`, `skipped`, or `not_asked` entry "is never a finding source"; watch it fail (FR-022, contract 25)
- [X] T037 [US4] **OPEN** — Add the paragraph "**From a domain analysis, only accepted guardrails are standards.**" directly after the T2 table in `spectra/commands/review-pr.md` (after the "Contributor guide (T2)" row): cite only entries whose `decision` is `accepted` — the Constitution input section, or an `accepted` record under a lens; a `declined`, `skipped`, or `not_asked` entry is never a finding source; in a pre-1.23.0 checkbox file only `- [x]` items count. Add one sentence about it to `[1.23.0]` in `spectra/CHANGELOG.md`. Make T036 pass

**Checkpoint**: US4 tests pass, including the changed legacy test and the review-pr test.

---

## Phase 7: Polish & cross-cutting

- [X] T026 Write "Non-interactive mode" and the "Inline template skeleton" in `spectra/commands/domain-analyzer.md` (contract 24)
- [X] T027 [P] Add test class `NonInteractive` to `tests/test_domain_analyzer_flow.py`
- [X] T028 [P] Bump `spectra/extension.yml` to `1.23.0` and update the command and `domain-analysis-template` descriptions; mirror the version in `catalog.json`
- [X] T029 [P] Add `[1.23.0] - 2026-10-23` to `spectra/CHANGELOG.md`
- [X] T030 [P] Update the domain-analyzer `description` in `agents-list.json`
- [X] T031 [P] Update prose: `spectra/README.md` domain-analyzer section, `AGENTS_LIST.md` `<!-- SPECTRA:AGENT id=domain-analyzer -->` block, `docs/index.html` command card, `docs/e-learning/module-4.html` "Optional second opinion" note
- [X] T032 [P] Constitution PATCH 1.11.0 → 1.11.1 in `.specify/memory/constitution.md`: Principle VII "an SME ticks" → "an SME decides on", "an SME's ticks" → "an SME's choices"; Sync Impact Report; version and Last Amended lines
- [X] T033 Run `python3 tools/generate_agent_docs.py` then `python3 tools/build_package.py` (rewrites `spectra/README.md` commands table and `docs/packages/spectra.zip`)
- [X] T034 Run quickstart §1: `python3 -m unittest discover -s tests`, `python3 tools/generate_agent_docs.py --check`, `python3 tools/ship.py --dry-run` — all green, nothing pushed
- [X] T035 Run quickstart §2 runs A–D in a throwaway Spec Kit project with `specify extension add --dev`, and record any deviation
- [X] T038 **OPEN** — Commit on `034-interactive-domain-analyzer` (spec artifacts, `spectra/`, `catalog.json`, `agents-list.json`, `docs/`, `README.md`, `AGENTS_LIST.md`, `.specify/memory/constitution.md`, `tests/`), merge into `main` locally, then run `python3 tools/ship.py` — never `git push origin main` (Principle V; Development Workflow step 6; `SHIPPING.md`)

---

## Dependencies & execution order

- Phase 1 → Phase 2 → stories. US1, US2, US3 are all P1 and touch different sections of the same command file, so their command tasks run in sequence (US1 → US2 → US3); their test tasks are `[P]`.
- US4 depends on US1 (decision values) and US3 (candidate fields).
- T023 depends on T021 (test first). T024 and T025 are independent of T023.
- T037 depends on T036 (test first).
- T033 after every edit to `agents-list.json`, `spectra/`, and prose; T034 after T033; T035 after T034; T038 last, after T034 and T035.

### Parallel examples

```text
US1:   T008 (tests)  ‖  T006 (template)
US4:   T021 (test)   ‖  T036 (test)  ‖  T024 (README)  ‖  T025 (CHANGELOG)
Polish: T028 ‖ T029 ‖ T030 ‖ T031 ‖ T032
```

## Implementation strategy

- **MVP**: Phases 1–3 (US1) — the in-session round and the write-once document.
- **Then**: US2 (goal + handoff) and US3 (lenses), which together make the output constitution-ready.
- **Then**: US4 re-run rules, including the OPEN FR-020 change, and Polish.
- **Given the working tree**: verify and check off T001–T020, T022, and T026–T033 against the diff; do T021, T023–T025, T036–T037; then T034, T035, and T038.

## Phase 8: Convergence

- [X] T039 Add the accepted-only rule to `spectra/commands/deployment-strategy.md` input 10 ("Sibling strategy documents"): from `DOMAIN_ANALYSIS.md`, only entries whose `decision` is `accepted` — the Constitution input section, or an `accepted` record under a lens — may shape a gate; a `declined`, `skipped`, or `not_asked` entry never does; in a pre-1.23.0 checkbox file only `- [x]` items count. Pin it with a test in `tests/test_deployment_strategy_flow.py` (or the module that already asserts deployment-strategy inputs), written first, and add the agent to the `[1.23.0]` `review-pr` line in `spectra/CHANGELOG.md` per FR-022 (partial)
