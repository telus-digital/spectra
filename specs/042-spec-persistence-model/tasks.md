---

description: "Task list for feature 042 — spec persistence model in the methodology agent"
---

# Tasks: Spec Persistence Model in the Methodology Agent

**Input**: Design documents from `/specs/042-spec-persistence-model/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/question-five.md,
contracts/persistence-guardrail.md, quickstart.md

**Tests**: Included. FR-030 requires tests that cover the new behaviour. Command files are prompts, so
tests assert their text (the `*_flow.py` convention in `tests/test_methodology_flow.py`). Write each
story's tests first, confirm they fail, then edit the command.

**Organization**: Tasks are grouped by user story. Every story edits `spectra/commands/methodology.md` and
`tests/test_methodology_flow.py`, so the stories run **in sequence**. `[P]` marks only tasks that touch a
different file from everything else open at that point.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: The user story the task belongs to (US1–US5)

## Path Conventions

Repository root: `spectra/` (extension), `agents/` (agent source), `tests/` (unittest), `docs/` (pages,
package), `tools/` (generator, packager, ship). Line numbers below are from the current `main` and drift
as earlier tasks land; anchor on the quoted text.

---

## Phase 1: Setup

**Purpose**: A test home for the new rules.

- [X] T001 In `tests/test_methodology_flow.py`, add the spec 042 rules to the module docstring's bullet list, in its voice: "**The persistence model is one decision inside lens 4.** Question 5 offers four exclusive models and Skip, the accepted one becomes one guardrail written as phase obligations, and the round still holds ten questions." Add a module constant `MODELS = ("Living Spec", "Flow-Forward", "Flow-Back", "Hybrid")` and an empty class `TheSpecPersistenceModel(unittest.TestCase)` placed after `TheMethodologyStack`. Run `python3 -m unittest tests.test_methodology_flow`; everything still passes.

---

## Phase 2: Foundational (blocking)

**Purpose**: Make room in Step 5 for a third special-shape question without breaking the existing pins.

- [X] T002 In `tests/test_methodology_flow.py`, class `TheClarificationRound`, add `test_question_five_is_excluded_from_the_four_option_shape`: assert `section("## Step 5")` contains `"for questions 3, 4, 6–8 and 10, the four are"` and does not contain `"for questions 3–8 and 10"`. Confirm it fails.
- [X] T003 In `spectra/commands/methodology.md`, Step 5 "How to ask" (around line 443), change "For questions 3–8 and 10, the four are:" to "For questions 3, 4, 6–8 and 10, the four are:". In "The ten questions" table, change row 5's "What it settles" from "How specs stay current and traceable" to "How specs stay current and traceable, and the spec persistence model". Run the module; T002 passes and every existing test still passes.

**Checkpoint**: Step 5 no longer claims question 5 uses the four-option shape.

---

## Phase 3: User Story 1 — Choose a persistence model in question 5 (Priority: P1) 🎯 MVP

**Goal**: Question 5 offers the four models and Skip, one recommended, and records exactly one model
accepted (contracts/question-five.md).

**Independent Test**: Greenfield run, reach question 5, see five options with Hybrid recommended; choose
Flow-Forward; the document shows Flow-Forward `accepted` and the other three `declined`.

### Tests for User Story 1

- [X] T004 [US1] In `TheSpecPersistenceModel`, add tests against `section("## Step 5")`:
  - `test_question_five_has_its_own_shape`: contains `"question 5 has its own shape"` and `"four persistence models exclude each other"`.
  - `test_five_options_in_order`: add a helper `question_five()` returning the slice of `section("## Step 5")` from `"question 5 has its own shape"` to `"**free text is always valid.**"`. Within that slice only (Step 5 already holds four earlier `**Skip**` labels), the option labels `**living spec**`, `**flow-forward**`, `**flow-back**`, `**hybrid (living spec by default)**`, `**skip**` appear, and each one's index is greater than the previous one's.
  - `test_one_model_accepted_the_rest_declined`: contains `"the chosen model is accepted and the other three declined"` and `"other lens 4 candidates take the same decision as the model unless free text excludes them"`.
  - `test_skip_leaves_lens_four_skipped`: contains `"skip leaves every lens 4 candidate `skipped`"`.
  - `test_each_model_states_fit_and_risk`: for each of `"the spec is the contract"`, `"losing implementation rationale"`, `"audit trails"`, `"context spread over several directories"`, `"small teams, fast iteration"`, `"silent drift"`, `"the spec stays authoritative"`, `"the threshold is only as good as the mapping"`, assert it is in `question_five()`.

  In `section("## Step 4")`, add `test_the_models_count_as_one_slot`: contains `"the four persistence models count as one slot"`. Confirm all fail.

### Implementation for User Story 1

- [X] T005 [US1] In `spectra/commands/methodology.md` Step 4, after the "**Lens 3 stops at the format.**" paragraph (around line 293), add a paragraph opening "**Lens 4 settles the spec persistence model.**". It says that lens 4 decides how a behaviour change to a **delivered** feature (one merged to the default branch) is handled, using one of four models, each a candidate: Living Spec, Flow-Forward, Flow-Back, Hybrid (Living Spec by default). Use the one-line descriptions from `contracts/question-five.md`, including "the spec is the contract", "audit trails", "small teams, fast iteration", and "silent drift". Then: "The four persistence models count as one slot against the cap of five, because they are alternatives for one decision and at most one is accepted. That leaves up to four other lens 4 candidates." In the lens table row 4 (around line 252), append to "What it settles": "and which persistence model governs a behaviour change to a delivered feature".
- [X] T006 [US1] In `spectra/commands/methodology.md` Step 5 "How to ask", after the "**Question 9 has its own shape**" bullet (ends around line 491), add a bullet "**Question 5 has its own shape**, because the four persistence models exclude each other and a "Full set" would adopt all four." It lists lens 4's other candidates first (`5.1` … `5.n`), then offers exactly the five numbered options from `contracts/question-five.md` in that order, each with its one-line description, and marks exactly one *(recommended)* with its reason. Then: "The chosen model is accepted and the other three declined. The other lens 4 candidates take the same decision as the model unless free text excludes them; Skip leaves every lens 4 candidate `skipped`." Keep the existing "**Free text is always valid.**" bullet after it.
- [X] T007 [US1] Run `python3 -m unittest tests.test_methodology_flow`; T004's tests pass and no earlier test regresses.

**Checkpoint**: Question 5 asks the right question and records the answer. Nothing yet says what the guardrail contains.

---

## Phase 4: User Story 2 — The constitution tells an agent what to do (Priority: P1)

**Goal**: An accepted model becomes one MUST guardrail whose statement carries the shared preamble and
five phase obligations, verbatim in substance from `contracts/persistence-guardrail.md`.

**Independent Test**: For each model, the canonical statement in the command answers specify, plan,
tasks, implement, and converge with no model name and no agent invocation syntax.

### Tests for User Story 2

- [X] T008 [US2] In `TheSpecPersistenceModel`, add `persistence_rules()`, returning `flat()` of the raw command text from `"**The persistence guardrail.**"` up to `"**Lens 8 is about"`, the existing paragraph that follows the inserted lens 4 paragraphs. Then add tests:
  - `test_preamble_new_capability_and_delivered`: contains `"a new capability must get its own feature directory"` and `"merged to the default branch"`.
  - `test_each_model_names_all_five_phases`: for each model in `MODELS`, the model's block (from its bold label to the next model's) mentions `specify`, `plan`, `tasks`, `implement`, `converge`.
  - `test_divergence_updates_an_artifact_first`: contains `"`spec.md` must be updated first"` (Living Spec) and `"the **new** `spec.md` must be updated first"` (Flow-Forward).
  - `test_cross_link_wording_is_exact`: contains each of `"extends spec nnn"`, `"supersedes spec nnn"`, `"extended by spec nnn"`, `"superseded by spec nnn"`, and `"no other edit is allowed in a completed feature directory"`.
  - `test_flow_back_agrees_before_merge`: contains `"before the pull request carrying the change merges"` and `"analyze phase"`.
  - `test_phases_not_invocations`: asserts `"/speckit-"` and `"$speckit-"` do not appear in `persistence_rules()`.
  - `test_guardrail_is_must_in_lens_four`: contains `"em-spec-lifecycle-traceability-"` and `"strictness is **must**"`.

  Confirm all fail.

### Implementation for User Story 2

- [X] T009 [US2] In `spectra/commands/methodology.md` Step 4, directly after the T005 paragraph, add a paragraph opening "**The persistence guardrail.**". The accepted model yields exactly one candidate with ID `em-spec-lifecycle-traceability-<hash>`, frozen like any other, and strictness is **MUST**. Its basis is `observed` when its brownfield signal was found, `aspirational` otherwise, and it targets lens 4's section. Its statement is the shared preamble plus that model's five phase obligations, written by phase name, never in any agent's invocation syntax. Follow it with the preamble and the four model tables from `contracts/persistence-guardrail.md`, as compact Markdown tables (phase | obligation), with bold labels `**Living Spec**`, `**Flow-Forward**`, `**Flow-Back**`, `**Hybrid**`. State that the existing suppress and `amends:` rules (Step 4, "Against an existing constitution") apply to the persistence guardrail like any other candidate. Include the wording rules: exact cross-link phrases, always naming a spec; `NNN` is the directory's prefix; and the persistence guardrail's implement obligation sits beside an overlay's, never replacing it.
- [X] T010 [US2] In `spectra/commands/methodology.md` Step 5, where the round reports overlay conflicts ("**When two adopted overlays conflict at one phase**", around line 478), append one sentence: "The persistence guardrail's implement obligation is not an overlay and never conflicts with one: it decides which artifact changes first, not when tests are written."
- [X] T011 [US2] Run the module; T008's tests pass and no earlier test regresses.

**Checkpoint**: MVP complete. A team can choose a model and get a guardrail an agent can act on.

---

## Phase 5: User Story 3 — Brownfield evidence drives the recommendation (Priority: P2)

**Goal**: Lens 4 reports the three signals with counts and citations before question 5, and the
recommendation follows research R2 and R3.

**Independent Test**: The command text names all three signals, the first-parent rule, and "exactly one
signal → that model, otherwise Hybrid".

### Tests for User Story 3

- [X] T012 [US3] In `TheSpecPersistenceModel`, add tests against `section("## Step 4")`:
  - `test_three_signals_are_named`: contains `"first-parent"`, `"delivery point"`, `"changes that directory's `spec.md`"`, `"`plan.md` or `tasks.md` while its `spec.md` is unchanged"`, and `"names another spec directory it builds on"`.
  - `test_recommendation_follows_one_signal_or_hybrid`: contains `"exactly one signal"` and `"two or more signals, or none"` near `"hybrid"`.
  - `test_counts_and_citations`: contains `"with a count and up to three citations"`.
  - `test_greenfield_recommends_hybrid`: in the "### In greenfield mode" defaults list, contains `"**spec lifecycle & traceability** — hybrid"`.

  Confirm all fail.

### Implementation for User Story 3

- [X] T013 [US3] In `spectra/commands/methodology.md` Step 4, after the T009 paragraph, add "**Reading current persistence practice (brownfield).**" with research R2 as instructions: read the default branch's first-parent history; a directory's delivery point is the first first-parent commit containing its `spec.md`; the three signals (wording matching T012); report each with a count and up to three citations (short SHA and path), or say where the agent looked. Add research R3: exactly one signal → that model recommended; two or more signals, or none → Hybrid. Note that wording-only edits are reported as such but still count. In Step 1's list of what is read (around line 128), add `git log --first-parent` of the default branch for `specs/` to the history item.
- [X] T014 [US3] In `spectra/commands/methodology.md` "### In greenfield mode" defaults list (around line 316), add the bullet "**Spec lifecycle & traceability** — Hybrid, with Living Spec by default and the proposed per-type mapping." directly after the "**AI collaboration rules**" bullet and before "**Methodology stack**".
- [X] T015 [US3] Run the module; T012's tests pass and no earlier test regresses.

---

## Phase 6: User Story 4 — Hybrid's threshold is decided per change type (Priority: P2)

**Goal**: The Hybrid option shows the proposed mapping inline, free text adjusts it, the guardrail always
carries it, and the mode-choice table gains a Persistence column only under Hybrid.

**Independent Test**: The command text holds the default mapping verbatim, the "no further question"
rule, the always-in-statement rule, and the column rule.

### Tests for User Story 4

- [X] T016 [US4] In `TheSpecPersistenceModel`, add:
  - `test_default_mapping_is_pinned`: `command()` contains `"`feature` → flow-forward"`, `"`fix` → living"`, `"`refactor` → living"`, `"`hotfix` → living"`, `"`docs` → —"`, `"`spike` → —"`.
  - `test_dash_only_where_no_spec_is_required`: contains `"`—` only where the accepted mode-choice table says that change type needs no spec"`.
  - `test_hybrid_needs_no_extra_question`: `section("## Step 5")` contains `"choosing hybrid accepts the mapping as shown"` and `"no further question"`.
  - `test_mapping_always_in_the_statement`: contains `"the hybrid guardrail always carries the mapping in its statement"`.
  - `test_persistence_column_only_under_hybrid`: `section("## Step 7")` contains `"a **persistence** column"` and `"only when hybrid is accepted"`.
  - `test_no_table_means_statement_only`: contains `"when question 3 adopted no mode-choice table"`.
  - `test_defaults_take_hybrid_with_its_mapping`: `section("## Step 5")` contains `"**use your defaults** accepts the recommended model and, for hybrid, the proposed mapping"`.

  Confirm all fail.

### Implementation for User Story 4

- [X] T017 [US4] In `spectra/commands/methodology.md` Step 4, in the T009 `**Hybrid**` block, write a five-row phase table (specify, plan, tasks, implement, converge). Each row gives the Living Spec obligation and the Flow-Forward obligation for `flow-forward` change types, so T008's `test_each_model_names_all_five_phases` holds for Hybrid too. Then add: the decision rule (change within an existing capability → Living Spec; a substantial new increment, meaning a new user journey, a redesign, or a change reviewed as its own unit → Flow-Forward); "The Hybrid guardrail always carries the mapping in its statement"; the proposed default mapping exactly as data-model.md's table (`feature` → flow-forward, `fix` → living, `refactor` → living, `hotfix` → living, `docs` → —, `spike` → —); and the constraint "`—` only where the accepted mode-choice table says that change type needs no spec; when question 3 adopted no mode-choice table, `—` becomes living and the statement alone carries the mapping, and the document says why."
- [X] T018 [US4] In `spectra/commands/methodology.md` Step 5, in the T006 bullet, under option 4, show the proposed mapping inline and add: "Choosing Hybrid accepts the mapping as shown, with no further question; free text adjusts any value — "Hybrid, but refactor is flow-forward". **Use your defaults** accepts the recommended model and, for Hybrid, the proposed mapping."
- [X] T019 [US4] In `spectra/commands/methodology.md` Step 7, in the mode-choice bullet of the always-written references (around line 602), append: "When Hybrid is accepted — and only when Hybrid is accepted — it gains a **Persistence** column holding the accepted mapping."
- [X] T020 [US4] Run the module; T016's tests pass and no earlier test regresses.

---

## Phase 7: User Story 5 — Front matter, reference, re-runs, non-interactive (Priority: P3)

**Goal**: The `persistence` key, the fifth always-written reference, the template guidance, and the
re-run and non-interactive rules (data-model.md).

**Independent Test**: The command text holds the key's four values and absence rule, the reference
rule, and the re-run and non-interactive lines. The template's Spec lifecycle comment describes the
reference.

### Tests for User Story 5

- [X] T021 [US5] In `TheSpecPersistenceModel`, add:
  - `test_front_matter_key`: `section("## Step 7")` contains `"persistence: hybrid"` (the example) and `"`persistence` is `living`, `flow-forward`, `flow-back`, or `hybrid`, and absent when question 5 was skipped or not asked"`.
  - `test_five_references_are_written`: `section("## Step 7")` contains `"five references are always written"` and `"**a persistence reference**"`, and does not contain `"four references are always written"`.
  - `test_reference_when_nothing_accepted`: contains `"no spec persistence model was chosen"`.
  - `test_rerun_offers_prior_model`: `section("## Re-running")` contains `"last run you chose"` near `"persistence"`, and `"a prior document with no `persistence` key"` with `"undecided"`.
  - `test_rerun_declined_model_stays_selectable`: `section("## Re-running")` contains `"a declined model stays selectable"`.
  - `test_non_interactive_asks_no_model`: `section("## Non-interactive mode")` contains `"no `persistence` key"`.
  - `test_template_describes_the_reference`: `flat(TEMPLATE.read_text())` contains `"persistence reference"` in the Spec lifecycle comment (slice from `"## spec lifecycle & traceability"` to the next `"## "`).

  Confirm all fail.

### Implementation for User Story 5

- [X] T022 [US5] In `spectra/commands/methodology.md` Step 7 front-matter example (around line 578), add `persistence: hybrid` after the `autonomy:` line. In the key explanation paragraph (around line 589), add: "`persistence` is `living`, `flow-forward`, `flow-back`, or `hybrid`, and absent when question 5 was skipped or not asked."
- [X] T023 [US5] In `spectra/commands/methodology.md` Step 7, change "Four references are always written" to "Five references are always written". Add the bullet "**A persistence reference** in the spec-lifecycle section: the accepted model; one line on when it applies (once a feature is merged to the default branch); a table, phase → obligation, for specify, plan, tasks, implement, converge; and for Hybrid, the mapping or a pointer to the mode-choice table's Persistence column. With no model accepted, one sentence: no spec persistence model was chosen."
- [X] T024 [US5] In `spectra/commands/methodology.md` "## Re-running on a project you have analysed before", after "**Pre-fill the round from the prior answers.**", add a bullet: "**The persistence model is pre-filled from the `persistence` key**, with "last run you chose **<model>**; still right?", and Hybrid's prior mapping is read back from the accepted Hybrid candidate's statement. A prior document with no `persistence` key leaves the model undecided: question 5 is asked as new. A declined model stays selectable as an option and is named as declined last run, but is never offered as a new candidate."
- [X] T025 [US5] In `spectra/commands/methodology.md` "## Non-interactive mode", extend the bullet "record every candidate and every overlay `not_asked`" with: "including the four persistence models, so the front matter has no `persistence` key".
- [X] T026 [US5] In `spectra/commands/methodology.md` "## Inline template skeleton", change the `## Spec lifecycle & traceability` line's comment to `<!-- persistence reference, then candidate records -->`.
- [X] T027 [P] [US5] In `spectra/templates/engineering-methodology-template.md`, "## Spec lifecycle & traceability" comment (around line 69), append: "Then the persistence reference: the accepted spec persistence model, when it applies (once a feature is merged to the default branch), and a phase → obligation table for specify, plan, tasks, implement, converge; for Hybrid, the per-change-type mapping. With no model accepted, one sentence saying so." Change the placeholder to `[CURRENT PRACTICE, PERSISTENCE REFERENCE, AND CANDIDATE RECORDS]`. In the header's "What this template CANNOT change" list (around line 14), add "the persistence reference's phase obligations" after "the obligations matrix as the closed set of phase obligations". Add no heading; the section list stays identical.
- [X] T028 [US5] Run `python3 -m unittest tests.test_methodology_flow tests.test_document_templates`; T021's tests pass, `test_sections_match_in_order` still passes, and nothing regresses.

---

## Phase 8: Polish & Cross-Cutting (Principle V)

**Purpose**: Listings, versions, package, and the full gate. These touch different files and run after
every story.

- [X] T029 [P] In `agents/methodology.md`: in `manifest:`, change the lens list item "spec lifecycle" to "spec lifecycle and persistence model". In the body's "How it works" step 3, change "spec lifecycle and traceability" to "spec lifecycle and traceability (including the team's spec persistence model: Living Spec, Flow-Forward, Flow-Back, or Hybrid)". In step 5, append: "Question 5 offers the four persistence models and Skip; the chosen one becomes a guardrail that tells each spec-kit phase what to do when a delivered feature's behaviour changes." Keep "nine lenses" and "ten questions" unchanged. Use only the body Markdown subset the generator accepts (no raw HTML, no `###`).
- [X] T030 Run `python3 tools/generate_agent_docs.py` to re-render `spectra/extension.yml` and `spectra/commands/methodology.md` description lines, `AGENTS_LIST.md`, `spectra/README.md`, `docs/getting-started/agents.html`, and `agents-list.json`. Then run `python3 tools/generate_agent_docs.py --check`; it passes.
- [X] T031 [P] In `spectra/extension.yml`, bump `version: "1.30.0"` → `"1.31.0"`. In the `engineering-methodology-template` entry's `description` under `provides.templates` (around line 104), add "the persistence reference" to the list of what stays with the command.
- [X] T032 [P] In `spectra/CHANGELOG.md`, add `## [1.31.0] - <date of landing>` above `[1.30.0]`. Give it a one-paragraph summary: methodology's lens 4 now settles the team's spec persistence model. Under `### Added`: question 5's five options and its recommendation rule (brownfield signals; Hybrid when mixed, none, or greenfield); the per-phase guardrail; Hybrid's per-type mapping and the mode-choice Persistence column; the `persistence` front-matter key and the persistence reference. Under `### Changed`: question 5 no longer uses the four-option shape, and still ten questions, nine lenses, nothing renumbered.
- [X] T033 [P] In `catalog.json`, set the `spectra` entry's `"version"` to `"1.31.0"`. Leave description, tags, command count, and `download_url` unchanged.
- [X] T034 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip` (depends on T027–T032).
- [X] T035 Run `python3 -m unittest discover -s tests` and `python3 tools/ship.py --dry-run`; both pass. Then confirm scope with `git diff --stat main -- . ':!specs/042-spec-persistence-model'`: only the files listed under Source Code in `plan.md`, nothing under `spectra_cli/`, `VERSION` unchanged.
- [X] T036 Walk the manual scenarios 1–4 in `specs/042-spec-persistence-model/quickstart.md` in throwaway projects installed with `specify extension add --dev`. Record each scenario's pass/fail at the bottom of `quickstart.md` under a new `## Results` heading with the date.

---

## Dependencies & Execution Order

### Phase dependencies

- **Phase 1 (T001)** → **Phase 2 (T002–T003)** → **US1 (T004–T007)** → **US2 (T008–T011)** →
  **US3 (T012–T015)** → **US4 (T016–T020)** → **US5 (T021–T028)** → **Polish (T029–T036)**.
- The stories are sequential because each edits `spectra/commands/methodology.md` and
  `tests/test_methodology_flow.py`. Their *behaviour* is independent: US3, US4, and US5 each need only
  US1's question and US2's guardrail block to exist.
- US4's T017 extends the `**Hybrid**` block that US2's T009 creates.
- US5's T024 refers to the Hybrid statement that T017 completes.

### Within each story

Tests first and failing → command edits → run the module.

### Parallel opportunities

- T027 (template) can run alongside T022–T026 (command), since they are different files.
- In Polish, T029, T031, T032, and T033 touch four different files and can run together. T030 must follow
  T029. T034 follows all edits. T035 and T036 come last.

### Parallel example: Polish

```text
Together: T029 agents/methodology.md · T031 spectra/extension.yml · T032 spectra/CHANGELOG.md · T033 catalog.json
Then:     T030 generate_agent_docs.py → T034 build_package.py → T035 full suite + ship --dry-run → T036 quickstart
```

## Implementation Strategy

### MVP (US1 + US2)

Phase 1 → Phase 2 → US1 → US2. At that point a team can choose a model and get a guardrail an agent can
act on. Stop and validate quickstart Scenarios 1 and 2 (greenfield path) before going on. The MVP is not
shippable on its own, because Principle V's Polish phase must land with it, but it is the right place to
review the guardrail wording.

### Incremental delivery

1. US1 + US2: choose a model, get the guardrail.
2. US3: brownfield recommendation.
3. US4: Hybrid mapping and column.
4. US5: front matter, reference, template, re-runs, non-interactive.
5. Polish: listings, version 1.31.0, package, full gate, then land with `python3 tools/ship.py`.

Everything ships together in one change (Principle V). The increments are review points, not releases.

## Phase 9: Convergence

- [X] T037 In `spectra/commands/methodology.md` Step 7 "### Decisions and sources", add that question 5's answer records the accepted model and, for Hybrid, the accepted per-change-type mapping including any free-text adjustment; pin it with an assertion in `TheSpecPersistenceModel` in `tests/test_methodology_flow.py`, then rebuild `docs/packages/spectra.zip` per FR-023 (partial)
