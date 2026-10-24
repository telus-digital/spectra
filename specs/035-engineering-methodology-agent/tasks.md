# Tasks: An Engineering Methodology Agent That Feeds the Constitution

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/methodology-behaviour.md](./contracts/methodology-behaviour.md),
[contracts/sibling-boundaries.md](./contracts/sibling-boundaries.md), [quickstart.md](./quickstart.md)

**Branch**: `035-engineering-methodology-agent`

**Tests**: requested. SC-008 and the behaviour contract pin every behaviour (B1–B35, E1–E8) as a text
assertion, in stdlib `unittest`. Within each story the test task comes first and must fail before the command
text it pins is written. Test files are abbreviated below: `M` = `tests/test_methodology_flow.py`,
`D` = `tests/test_domain_analyzer_flow.py`, `P` = `tests/test_doc_output_paths.py`,
`T` = `tests/test_document_templates.py`.

**Format**: `- [ ] [ID] [P?] [Story] Description`. `[P]` means a different file with no dependency on an
incomplete task.

All new command text lives in `spectra/commands/methodology.md`, so command tasks within a story run in
sequence. Each one names the `##` step it writes. The headings mirror `spectra/commands/domain-analyzer.md`
(Step 0 … Step 8, re-runs, non-interactive, inline skeleton), so a reader of one can navigate the other.

---

## Phase 1: Setup — verify the premise

- [X] T001 Confirm the evidence rows in `plan.md` still hold on this branch: `spectra/commands/domain-analyzer.md:192` (lens 7), `spectra/commands/deployment-strategy.md:125` (Release & versioning owns the branching model), `spectra/commands/kb-vault.md:365` (series example), `spectra/commands/review-pr.md:273–284` (T2 table), `spectra/extension.yml` at `1.23.0`, `catalog.json` at 13 commands, constitution at `1.12.0`
- [X] T002 [P] Run `python3 -m unittest discover -s tests` and `python3 tools/generate_agent_docs.py --check` on the unchanged branch and record the baseline pass count in the PR notes, so later failures are attributable. **Baseline (2026-10-24)**: 1471 tests OK; `--check` clean (54 agents, 13 prose blocks)

**Checkpoint**: the premises the plan rests on are true, and the suite is green before any change.

---

## Phase 2: Foundational — shared surface every story relies on

**⚠️ T003 is a user checkpoint.** The implementing agent MUST NOT edit the constitution (Principle VII, and
the agent's own FR-032). It stops, gives the user the prompt below, and resumes once the user has run it.

- [X] T003 **USER RUNS**: `/speckit-constitution Amend Principle VII (MINOR, 1.12.0 → 1.13.0): add <artifact-root>/ENGINEERING_METHODOLOGY.md, written by speckit.spectra.methodology, to the named standing-policy singletons, change "The three shipped singletons" to four, and note it has no earlier location. No rule changes.` Then verify `.specify/memory/constitution.md` contains `<artifact-root>/ENGINEERING_METHODOLOGY.md` and version `1.13.0` (research R10, contract E8)
- [X] T004 [P] Add `"methodology.md": ("docs/ENGINEERING_METHODOLOGY.md", None)` to `SINGLETON` in `tests/test_doc_output_paths.py`, so every singleton rule (root-level target, no sequence number, no earlier location, constitution names it) now covers the new command (B24, B34, E8). It fails until T006 and T008 land
- [X] T005 [P] Add the `methodology` → `engineering-methodology-template` entry to `DOCUMENT_COMMANDS` in `tests/test_document_templates.py` (B27)
- [X] T006 Create `spectra/commands/methodology.md` with:
  - front matter (`description` per research R1, naming nine lenses, ten questions, `ENGINEERING_METHODOLOGY.md`, and the `/speckit-constitution` handoff);
  - the intro;
  - "The one rule that governs everything" (only a human choice adopts a guardrail);
  - "User Input": `$ARGUMENTS` as a focus hint that narrows nothing, and the one flag `--non-interactive`;
  - "What this command never does": edit the constitution, a sibling document, source, CI, or any file but its own; run another spec-kit phase; make a network request; report practice without evidence; propose in sibling ground;
  - "The rules that never bend".

  (B30, B31)
- [X] T007 Write "Step 3 — Resolve where the methodology will live" in `spectra/commands/methodology.md`:
  - target `<artifact-root>/ENGINEERING_METHODOLOGY.md`, default `docs/ENGINEERING_METHODOLOGY.md`;
  - the declared `Artifact root:` line;
  - the publication check (asked before the round, outside the ten);
  - the non-publishing fallback;
  - no earlier location;
  - **research R13**: a file at the canonical path without `command: speckit.spectra.methodology` front matter is read as evidence, replacing it needs the team's consent before the round (outside the ten questions), and otherwise (always when `--non-interactive`) nothing is written and the document is shown in the session with a note that the existing file was left unchanged. No second file is ever written.

  (B24, B34, B35)
- [X] T008 [P] Create `spectra/templates/engineering-methodology-template.md` with the "HOW TO USE THIS TEMPLATE" guidance comment (worded like `spectra/templates/domain-analysis-template.md`) and the 13 `##` sections from research R12, in order: Overview; Methodology stack; Work modes; Requirements intake; Spec lifecycle & traceability; Branching & integration; Review & merge gates; Change records; AI collaboration; Governance & evolution; Related strategies; Constitution input; Decisions and sources (B25, B27)
- [X] T009 Register both in `spectra/extension.yml`:
  - `speckit.spectra.methodology` under `provides.commands`, with `file: commands/methodology.md` and a description matching T006;
  - `engineering-methodology-template` under `provides.templates`, with `file` and `description`.

  (Principle VIII, B27)
- [X] T010 Write "Step 6 — Resolve the document's template" in `spectra/commands/methodology.md`:
  - the five-layer stack, in prose (overrides → presets → extension → core → inline skeleton);
  - first readable, non-empty layer wins;
  - honour-not-repair;
  - strip guidance comments and placeholders;
  - report the resolved path;
  - write Constitution input even if an override omits it, and say so.

  Then add "Inline template skeleton" at the end of the file with the same 13 sections as T008 (B27)
- [X] T011 Create `tests/test_methodology_flow.py`:
  - module docstring in the style of `tests/test_domain_analyzer_flow.py` (rules pinned, spec 035);
  - `COMMAND`/`TEMPLATE` paths, a `LENSES` tuple of the nine lens names, `flat()` and `section()` helpers;
  - a first test class asserting T006's never-does table and the `--non-interactive` flag (B30, B31).

  Run `python3 -m unittest tests.test_methodology_flow tests.test_doc_output_paths tests.test_document_templates`; all pass once T003–T010 are done

**Checkpoint**: the command exists, is registered, resolves its template and output path, and is named by the
constitution. The suite is green. User stories can begin.

---

## Phase 3: User Story 1 — Record a brownfield team's methodology and hand it off (Priority: P1) 🎯 MVP

**Goal**: on an existing repository, state mode and goal, report current practice per lens with citations,
run the round, write the document once, and hand off one `/speckit-constitution` line plus the missing-sibling
list.

**Independent Test**: quickstart §2 steps 1, 3, 4, 5. Run on a repository with history, CI, and a PR
template; no file exists until the last answer; each lens cites current practice; Constitution input holds
exactly the accepted guardrails.

### Tests for User Story 1 ⚠️ (write first, see them fail)

- [X] T012 [US1] Add a test class to `tests/test_methodology_flow.py` asserting:
  - B1: first output names mode, signals, goal, and constitution version;
  - B2: three named signals, the source signal worded "at least one source file with more than 20 non-blank lines changed in more than one commit, or at least five such files when the history has at most one commit (including no history)"; "two or more" → `brownfield`, "none" → `greenfield`, "exactly one" → mixed, asked before lenses;
  - B3: every input listed in FR-003;
  - B4: all nine `LENSES`, and "nothing to propose" says what was searched;
  - B5: section mapping with the R9 defaults;
  - B6: "current practice" before candidates;
  - B7: `observed`/`aspirational`, "at most five";
  - B8: suppression and `amends:`;
  - B9: the six change types and spike rules;
  - B10: `speckit.spectra.brd`;
  - B11: the three autonomy level names as question 9's options, "every phase a human checkpoint" recommended, plus Skip, and tools and secrets candidates riding with the chosen level unless free text excludes them;
  - B35: a hand-written file at the canonical path is read as evidence, replaced only with consent, otherwise shown in the session; the string `.proposed` does not appear in the command.
- [X] T013 [US1] Add a test class asserting:
  - B19: "question 3 of 10" sample, one per turn, announcement with "use your defaults" and "skip";
  - B21: four options, exactly one recommended, Skip, free text;
  - B22: confirmation keeps its number;
  - B23: skip, silence, and non-interactive adopt nothing;
  - B24: no file before the last answer;
  - B26: candidate record fields `id, lens, target section, evidence, basis, decision, status`, a Constitution input heading and format, Decisions and sources;
  - B28: the create and amend `/speckit-constitution` lines;
  - B29: the sibling order `domain-analyzer → methodology → test-strategy → deployment-strategy` and "only siblings whose document does not exist".

  Confirm T012–T013 fail.

### Implementation for User Story 1

- [X] T014 [US1] Write "Step 0 — Say what you found, before anything else" in `spectra/commands/methodology.md`:
  - the three mode signals with research R6 thresholds (`git rev-list --count HEAD` > 10; workflow config = any of `.github/workflows/*`, `.gitlab-ci.yml`, PR/MR template, `CODEOWNERS`, `CONTRIBUTING.md`; source beyond scaffolding = "at least one source file with more than 20 non-blank lines changed in more than one commit, or at least five such files when the history has at most one commit (including no history)", so a squashed import counts);
  - the brownfield/greenfield/mixed rule, with the mixed reading asked and settled before lenses;
  - constitution present/absent/empty with version → goal `create` or `update`;
  - a sample first output.

  (B1, B2)
- [X] T015 [US1] Write "Step 1 — Read the project before you propose anything" in `spectra/commands/methodology.md`:
  - the read list: `git log` and `git branch -a` (read-only), PR and issue templates, `CODEOWNERS`, CI workflows, commitlint, changelog and release config, `CONTRIBUTING.md`, `specs/`, the constitution;
  - sibling documents `DOMAIN_ANALYSIS.md`, `TEST_STRATEGY.md`, `DEPLOYMENT_STRATEGY.md` at the resolved root, accepted entries only;
  - the rule that a doc/history contradiction is reported with history as current practice.

  (B3)
- [X] T016 [US1] Write "Step 4 — Work the nine lenses" in `spectra/commands/methodology.md`:
  - a table of the nine lenses: what each looks at, what it settles, and its R9 default section;
  - "Never omit a lens";
  - brownfield "Current practice" with citations before candidates;
  - "### Each candidate": `em-<lens-slug>-<hash>`, statement in MUST/SHOULD, evidence, basis, at most five per lens;
  - "### Against an existing constitution": suppress what is asserted, mark `amends: <principle>`;
  - lens 2's mode-choice classification of feature, fix, refactor, docs, spike, and hotfix (hotfix as a change type only) and spike rules (timebox, single owner, never merged, findings not code);
  - lens 3's intake, with the BRD format referred to `speckit.spectra.brd` and known-unknowns triage;
  - lens 8's three autonomy levels verbatim from FR-011a, plus AI tools and secret handling.

  (B4–B11)
- [X] T017 [US1] Write "Step 5 — The clarification round" in `spectra/commands/methodology.md`:
  - "### Announce the round, once" (ten questions, the ways out, nothing written until the last answer);
  - "### The ten questions" table per research R2, with questions 1–2 described here and detailed in US2;
  - "### How to ask": one per turn, "Question N of 10", list candidates first numbered `<lens>.<n>`, the four lens options with "Choose individually" replacing a duplicate, free text valid, a reword keeps the ID;
  - question 9 (lens 8) uses its own shape, not the four lens options: **Every phase a human checkpoint** (recommended) / **Human gates at spec approval and PR review** / **Autonomous to PR** / **Skip**; the lens's tools and secrets candidates are listed above the options and take the level's decision unless free text excludes them;
  - "### Where the evidence leaves a question with nothing to choose";
  - "### Ways the round ends early, and what each records": `default_taken`, `skipped`, `not_asked`, a non-answer re-asks;
  - "### Record every answer".

  (B11, B19, B21–B23)
- [X] T018 [US1] Write "Step 7 — Write the document" in `spectra/commands/methodology.md`:
  - written once, after the round, rewritten in place;
  - the command-owned front matter from `data-model.md`;
  - each lens section opening with "Current practice" (brownfield) or "Starting point" (greenfield);
  - the mode-choice table, branch-naming reference, and commit-prefix reference;
  - "### The candidate record";
  - "### The Constitution input section": exactly the accepted, not-adopted candidates, grouped by section, with goal line, `id`, `placement`, `basis`; one sentence when empty;
  - "### Decisions and sources": every question, recommended option, answer, disposition, and inputs read;
  - if the file cannot be written, show it in the session.

  (B24, B25, B26)
- [X] T019 [US1] Write "Step 8 — Report and hand off" in `spectra/commands/methodology.md`:
  - a concise report (mode, goal, counts per decision, template used, path written);
  - the ready-to-paste create line `/speckit-constitution Create the project constitution from the "Constitution input" section of docs/ENGINEERING_METHODOLOGY.md` and the amend line `/speckit-constitution Amend the constitution with every guardrail in the "Constitution input" section of docs/ENGINEERING_METHODOLOGY.md`, with the resolved root substituted;
  - none when nothing was accepted;
  - then the list of sibling agents whose documents do not exist, in the order `speckit.spectra.domain-analyzer → speckit.spectra.methodology → speckit.spectra.test-strategy → speckit.spectra.deployment-strategy`, noting no sibling input is folded into this line.

  (B28, B29)
- [X] T020 [US1] Run `python3 -m unittest tests.test_methodology_flow`; T012–T013 now pass

**Checkpoint**: US1 is fully functional on its own, with the round asking all ten questions. Questions 1–2
are described in US2's terms by T017's table, and fully specified once US2 lands.

---

## Phase 4: User Story 2 — Choose a methodology stack on top of SDD (Priority: P1)

**Goal**: SDD as the fixed base; overlays offered with evidence; adopted overlays recorded as phase-bound
obligations with strictness, scope, and `tasks.md` evidence.

**Independent Test**: quickstart §2 steps 2 and 4. Adopt TDD at MUST for feature and fix, and confirm the
obligations matrix and Constitution input state TDD's per-phase obligations with that strictness, scope, and
the `tasks.md` evidence.

### Tests for User Story 2 ⚠️

- [X] T021 [US2] Add a test class to `tests/test_methodology_flow.py` asserting:
  - B12: "SDD" stated as the base and "never optional"; `TDD`, `BDD`, `DDD`, `contract-first`, `ADR-driven` named with their evidence signals;
  - B13: obligations only from the matrix, each adopted overlay is "one candidate" (`em-overlay-<name>`) so lens 1 holds at most five, and "an overlay that cannot be expressed as such an obligation" never enters Constitution input;
  - B14: the `tasks.md` evidence sentence ("records that it was run and failed before the implementation task is ticked");
  - B15: `aspirational`, and "new and changed code" by default;
  - B16: Scrum, Kanban, Shape Up never in Constitution input;
  - B17: conflict reported and precedence obtained before writing;
  - B20: question 2's four options "Accept all as proposed", "Make every overlay SHOULD", "Choose per row", "Skip".

  Confirm it fails.

### Implementation for User Story 2

- [X] T022 [US2] Add "### The methodology stack (lens 1)" under Step 4 in `spectra/commands/methodology.md`:
  - SDD as the fixed base;
  - the overlay list with brownfield evidence signals (test-before-or-with-code ordering in `git log`, `.feature` files and BDD dependencies, a glossary or context-aligned module layout, contracts committed ahead of handlers, an `adr/` directory);
  - `practised: yes | partial | no`;
  - the recommendation rule;
  - a team-named overlay accepted only with at least one stated phase obligation.

  (B12)
- [X] T023 [US2] Add "### The obligations matrix" under Step 4 in `spectra/commands/methodology.md`, reproducing research R7's table verbatim as the closed set of cells. The implement-phase evidence sentence is required for TDD and BDD. An adopted overlay yields **one** candidate, `em-overlay-<name>`, whose statement lists its obligations phase by phase and shares the overlay's strictness and scope, so lens 1 stays within the five-candidate cap (FR-008, FR-014). Process cadences may appear only in the document body (B13, B14, B16)
- [X] T024 [US2] Detail questions 1 and 2 in Step 5 of `spectra/commands/methodology.md`.
  - Q1 options: Recommended stack / Codify only what is practised / No overlays (SDD only) / Skip.
  - Q2 is one table, a row per adopted overlay, each with proposed `MUST`/`SHOULD`, change types, optional modules, and `new-and-changed` vs `all`.
  - Q2 options are those of FR-021a; free text adjusts any row; it becomes a confirmation when no overlay was adopted.
  - Unpractised overlays default to `aspirational` and `new-and-changed` code.
  - After Q2, detect conflicting obligations at one phase; report them, and ask for a precedence (not counted as a question, does not advance the round) before writing.

  (B15, B17, B20)
- [X] T025 [US2] Make Step 7 in `spectra/commands/methodology.md` render the obligations matrix (overlay × specify/plan/tasks/implement, with strictness and scope) in the "Methodology stack" section and the `overlays:` front-matter list from `data-model.md`. Run `python3 -m unittest tests.test_methodology_flow`; T021 passes

**Checkpoint**: US1 and US2 together produce a document in which test-first (or another overlay) is an
enforceable clause.

---

## Phase 5: User Story 3 — Stay inside its own ground; take over the domain analyzer's workflow lens (Priority: P1)

**Goal**: no clause has two sources across the four constitution-feeding agents
([contracts/sibling-boundaries.md](./contracts/sibling-boundaries.md)), and the readers know the new document.

**Independent Test**: quickstart §2 step 6 and §4. Run this agent and the domain analyzer on one repository;
neither proposes in the other's ground; deployment-strategy cites the methodology for the branching model.

### Tests for User Story 3 ⚠️

- [X] T026 [US3] Add a test class to `tests/test_methodology_flow.py` asserting the B18 referral rule for each sibling-owned row of `contracts/sibling-boundaries.md`:
  - `speckit.spectra.test-strategy` for test levels, coverage floor, ratchet, UAT;
  - `speckit.spectra.deployment-strategy` for environments, promotion, rollback, **versioning scheme, release cut, hotfix promotion**;
  - `speckit.spectra.domain-analyzer` for product languages, frameworks, dependency policy, bounded contexts, invariants, glossary;
  - "cite … if it exists, or name the command".
- [X] T027 [P] [US3] Update `tests/test_domain_analyzer_flow.py`:
  - drop `"Delivery & workflow"` from `LENSES` (six remain);
  - `"question 4 of 8"` → `"question 4 of 7"`;
  - "ask **none** of the eight questions" → "seven";
  - assert `speckit.spectra.methodology` is named for delivery-and-workflow ground (E1);
  - assert the "Handed on to `speckit.spectra.methodology`" rule for prior records (E2);
  - assert the template has no `## Delivery & workflow` and says seven questions (E3).
- [X] T028 [P] [US3] Add to `tests/test_deployment_strategy_flow.py` an assertion that the *Release & versioning* lens no longer lists "the branching model" as a decision and cites `ENGINEERING_METHODOLOGY.md` or names `speckit.spectra.methodology` for it (E5)
- [X] T029 [P] [US3] Add to `tests/test_kb_vault_flow.py` assertions for the reserved-map row `| an engineering methodology | \`<artifact-root>/\` | \`ENGINEERING_METHODOLOGY.md\` | \`engineering-methodology-template\` |`, that `docs/engineering-methodology/001-` no longer appears, that the command states a file with `command: speckit.spectra.methodology` front matter is never updated (left unchanged, `/speckit.spectra.methodology` named), and that Step 12 lists a "Sources referred on" item (E6)
- [X] T030 [P] [US3] Add to `tests/test_review_pr_flow.py` assertions for a T2 row `<root>/ENGINEERING_METHODOLOGY.md`, and a paragraph stating only `accepted` guardrails from it are standards (E7)
- [X] T031 [US3] Confirm T026–T030 fail

### Implementation for User Story 3

- [X] T032 [US3] Add "**Sibling ground is referred, not proposed.**" under Step 4 of `spectra/commands/methodology.md`, with the ownership table from `contracts/sibling-boundaries.md`, the cite-or-name rule, and the clarifications "TDD governs *when* tests are written; test levels and floors are `speckit.spectra.test-strategy`'s" and "DDD records the commitment; contexts, invariants and glossary are `speckit.spectra.domain-analyzer`'s". Lens 7 covers commit convention and changelog only, and refers the versioning scheme to `speckit.spectra.deployment-strategy` (B18, research R3)
- [X] T033 [US3] Edit `spectra/commands/domain-analyzer.md`:
  - front-matter `description`, "seven fixed lenses" → six;
  - Step 4 heading and table without lens 7;
  - referral paragraph adds "workflow — branching, review, commit conventions, governance — belongs to `speckit.spectra.methodology`";
  - Step 5: "Seven questions", the table without row 8, "Question 4 of 7", and the sample "Question 3 of 7";
  - "Non-interactive mode": "none of the seven questions";
  - inline skeleton without `## Delivery & workflow`.

  (E1)
- [X] T034 [US3] Add to "Re-running on a project you have analysed before" in `spectra/commands/domain-analyzer.md`: prior Delivery & workflow records keep their IDs and decisions under "Handed on to `speckit.spectra.methodology`" in Decisions and sources, leave Constitution input, and are never deleted (E2, research R8)
- [X] T035 [P] [US3] Edit `spectra/templates/domain-analysis-template.md`: remove `## Delivery & workflow`, "seven lenses" → six, "The eight questions" → seven, and mention handed-on records in Decisions and sources (E3)
- [X] T036 [P] [US3] Edit `spectra/commands/deployment-strategy.md`:
  - lens table row *Release & versioning* (`:125`) decides "how a release is cut, the versioning scheme, the hotfix promotion path", with the boundary "not the branching model — cite `ENGINEERING_METHODOLOGY.md`, or name `speckit.spectra.methodology`";
  - the `:433` per-lens guidance updated to match;
  - add `ENGINEERING_METHODOLOGY.md` (accepted entries only) to the sibling-documents read at `:171`.

  (E5)
- [X] T037 [P] [US3] Edit `spectra/commands/kb-vault.md`: add the reserved-map row for an engineering methodology (between the domain-analysis and deployment-strategy rows), and replace the `engineering-methodology` example row in the Step 9 plan table with one pointing to `docs/ENGINEERING_METHODOLOGY.md` ("Update — existing file" or "Create"), and add one sentence under the reserved map: a methodology written there has no `speckit.spectra.methodology` front matter, so the next methodology run reads it as evidence of current practice. In Step 7, add the guard: when a match is `<artifact-root>/ENGINEERING_METHODOLOGY.md` and its front matter has `command: speckit.spectra.methodology`, produce no update row — leave the file unchanged, name `/speckit.spectra.methodology` as the way to fold the content in, and refer the source on; a file without that front matter keeps the existing update rules. In Step 12, add a report item "Sources referred on" listing each such source and the command named (E6, FR-019, research R4)
- [X] T038 [P] [US3] Edit `spectra/commands/review-pr.md`: add the T2 row `| Engineering methodology (T2) | \`<root>/ENGINEERING_METHODOLOGY.md\` | — |`, and a paragraph "**From an engineering methodology, only accepted guardrails are standards.**", worded like the domain-analysis paragraph (E7, research R5)
- [X] T039 [US3] Run `python3 -m unittest tests.test_methodology_flow tests.test_domain_analyzer_flow tests.test_deployment_strategy_flow tests.test_kb_vault_flow tests.test_review_pr_flow`; T026–T030 pass

**Checkpoint**: every row of the sibling-boundaries contract holds on both sides.

---

## Phase 6: User Story 4 — Shape a methodology for a greenfield project (Priority: P2)

**Goal**: an empty repository gets an interview with sensible defaults, every candidate `aspirational`.

**Independent Test**: quickstart §3, first two bullets.

- [X] T040 [US4] Add a test class to `tests/test_methodology_flow.py` asserting the greenfield rules:
  - "no practice to report";
  - default candidates tagged `aspirational`;
  - "Codify only what exists" replaced by "Choose individually" in greenfield;
  - the named defaults (trunk-based, short-lived branches, squash merge, Conventional Commits, one approval).

  Confirm it fails
- [X] T041 [US4] Add "### In greenfield mode" under Step 4 of `spectra/commands/methodology.md`: each lens states "no practice to report" and offers default candidates, all `aspirational` (defaults: trunk-based development with short-lived branches; squash-and-merge; Conventional Commits; one approval per PR; autonomy "every phase a human checkpoint"). In Step 5, greenfield replaces "Codify only what exists" with "Choose individually". Run `python3 -m unittest tests.test_methodology_flow`; T040 passes

**Checkpoint**: both modes produce a document.

---

## Phase 7: User Story 5 — Re-run safely and run non-interactively (Priority: P2)

**Goal**: re-runs respect prior decisions, including those carried over from the domain analyzer, and
`--non-interactive` adopts nothing.

**Independent Test**: quickstart §3 third bullet and §4.

- [X] T042 [US5] Add a test class to `tests/test_methodology_flow.py` asserting:
  - B32: frozen `em-` IDs, prior answer prefilled, "not offered as new", "never delete", `adopted` never reverted, drift reported;
  - B33: `--non-interactive` "declared, never inferred", asks none of the ten, `not_asked`, no handoff line;
  - E4: carried-over `da-` records from `DOMAIN_ANALYSIS.md` (accepted → prefilled, declined → not re-offered, adopted → kept, `origin: domain-analyzer`).

  Confirm it fails
- [X] T043 [US5] Write "Re-running on a project you have analysed before" in `spectra/commands/methodology.md`:
  - match by ID, then same intent within the lens;
  - prefill;
  - count declined in the question;
  - mark `adopted: <principle>` when the constitution asserts it, and never revert it;
  - report drift when a principle disappears;
  - never delete a prior candidate.

  Add the domain-analyzer carry-over rule from research R8: read `DOMAIN_ANALYSIS.md` records formerly in Delivery & workflow (or listed under "Handed on to `speckit.spectra.methodology`"), keep their `da-` IDs, and set `origin: domain-analyzer` (B32, E4)
- [X] T044 [US5] Write "Non-interactive mode" in `spectra/commands/methodology.md`:
  - a session is interactive unless `--non-interactive` or the user declares otherwise;
  - ask none of the ten questions;
  - every candidate and overlay `not_asked`;
  - Constitution input says nothing was accepted;
  - no `/speckit-constitution` line;
  - an existing hand-written file → nothing written, the document shown in the session (R13).

  Run `python3 -m unittest tests.test_methodology_flow`; T042 passes

**Checkpoint**: all five stories are complete.

---

## Phase 8: Polish & Cross-Cutting — packaging (Principle V), validation, landing

- [X] T045 [P] Bump `spectra/extension.yml` `extension.version` to `1.24.0`, and refresh the `speckit.spectra.domain-analyzer` command description ("six lenses", "seven questions")
- [X] T046 [P] Add `## [1.24.0]` to `spectra/CHANGELOG.md`:
  - **Added**: `speckit.spectra.methodology` and `engineering-methodology-template`;
  - **Changed**: domain-analyzer hands Delivery & workflow to methodology (six lenses, seven questions, prior records kept as handed on); deployment-strategy no longer proposes the branching model; kb-vault routes an absorbed methodology to `ENGINEERING_METHODOLOGY.md` and refers it on, never updating, when that file was written by the methodology agent; review-pr reads it as a T2 standard, accepted only.
- [X] T047 [P] Update `catalog.json`: `spectra` entry `version` `1.24.0`, `provides.commands` `14`, description and tags mentioning engineering methodology
- [X] T048 [P] Add to `agents-list.json` an entry `{"id": "methodology", "title": "Methodology Analyst", "description": "Find, choose, and record the team's engineering methodology — spec-driven by default, with test-first or behaviour-first as binding phase obligations — and hand it to the constitution.", "status": "available", "phase": "foundation", "type": "add-on", "provider": "spectra", "command": "speckit.spectra.methodology"}`, placed after `domain-analyzer`; refresh the `domain-analyzer` description if it mentions workflow
- [X] T049 [P] Hand-write the `<!-- SPECTRA:AGENT id=methodology -->` prose blocks in `AGENTS_LIST.md` and `spectra/README.md` (what it does in numbered steps, like the domain-analyzer block; overridable at `.specify/templates/overrides/engineering-methodology-template.md`). Update the domain-analyzer prose in both: six lenses, seven questions, workflow handed on
- [X] T050 [P] Add a command card for `speckit.spectra.methodology` to `docs/index.html`, worded like the domain-analyzer card, and update that card's lens count. No hard-coded version or roster (Principle V)
- [X] T051 [P] In `docs/e-learning/module-4.html`, after the domain-analyzer note at `:769` (which states no lens count, so it needs no edit), add a sibling note on `/speckit-spectra-methodology`: it records the team's methodology, including test-first as a binding obligation, in `docs/ENGINEERING_METHODOLOGY.md`, and hands a `/speckit-constitution` prompt
- [X] T052 Run `python3 tools/generate_agent_docs.py` to regenerate `README.md`, `AGENTS_LIST.md`, and `spectra/README.md`, then `python3 tools/generate_agent_docs.py --check`
- [X] T053 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip`
- [X] T054 Run the full suite `python3 -m unittest discover -s tests`. The count must be the T002 baseline plus the new tests, with zero failures
- [X] T055 Follow `quickstart.md` §2–§4 manually: `specify extension add --dev ./spectra` into a throwaway Spec Kit project, then brownfield, greenfield, mixed, non-interactive, and re-run — including a brownfield repository that already keeps a hand-written `docs/ENGINEERING_METHODOLOGY.md`, which must be read as evidence and the produced document cover intake, work modes, spikes, branching, review, commits, AI tooling, and constitution amendment with coverage and environments only linked (SC-006). Record the results in the PR notes
- [X] T056 Set `spec.md` **Status** to `Implemented` only if every task above is `[X]`; otherwise `In Progress` with a `## Deferred` entry per open task
- [X] T057 Run `python3 tools/ship.py --dry-run`. Then, with the user's go-ahead, commit and land with `python3 tools/ship.py` (never `git push origin main`; see `SHIPPING.md`)

---

## Dependencies & Execution Order

- **Phase 1 → Phase 2 → stories.** T003 (the user's constitution amendment) blocks T011's green run, because
  `test_the_constitution_names_every_singleton` fails until it lands. Everything else in Phase 2 can be
  written while waiting.
- **US1 → US2.** Both write Step 4/5/7 of the same file, and US2 details questions 1–2 inside US1's round.
- **US3** depends on Phase 2 only for its sibling edits (T027–T030, T033–T038). Its methodology edit (T032)
  follows US2 because it touches the same Step 4.
- **US4, US5** depend on US1, since they add to Step 4, Step 5, and the re-run section.
- **Phase 8** after all stories. T052 → T053 → T054 are ordered; T045–T051 are parallel.

```text
Setup ─▶ Foundational (T003 user checkpoint) ─▶ US1 ─▶ US2 ─▶ US3(T032) ─▶ US4 ─▶ US5 ─▶ Polish
                                         └──────▶ US3 sibling edits (T027–T038, parallel) ──┘
```

## Parallel Opportunities

- **Phase 2**: T004, T005, T008 alongside T006/T007 (different files).
- **US3 tests**: T027, T028, T029, T030 in parallel.
- **US3 sibling edits**: T035, T036, T037, T038 in parallel, and alongside the US1/US2 command work, since
  they don't touch `methodology.md`.
- **Polish**: T045–T051 in parallel.

```text
# US3, all at once:
T027 tests/test_domain_analyzer_flow.py   T028 tests/test_deployment_strategy_flow.py
T029 tests/test_kb_vault_flow.py          T030 tests/test_review_pr_flow.py
T035 domain-analysis-template.md          T036 deployment-strategy.md
T037 kb-vault.md                          T038 review-pr.md
```

## Implementation Strategy

- **MVP = Phase 1 + Phase 2 + US1.** A brownfield team gets an evidence-backed methodology document and a
  constitution handoff. It is not shippable on its own: US3 must land in the same release, or
  domain-analyzer and this agent both propose workflow clauses.
- **Release scope = all five stories + Polish.** One extension version, 1.24.0. The four sibling edits and the
  constitution amendment ship together with the new command.
- **Stop points**: after each checkpoint the suite is green and the user can review. `implement` stops at
  T003 for the user's `/speckit-constitution` run, and at T057 before landing.
