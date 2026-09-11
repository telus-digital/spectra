# Tasks: Test Plan Agent

**Input**: Design documents from `/specs/021-test-plan-agent/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: Included, and not optional here. FR-063 requires it, and this repository enforces Principles
V and VIII with a Python suite whose checks derive from per-command registries —
`tests/test_document_templates.py` and `tests/test_roster_data.py` — so a new document agent absent from
them is unguarded. Test tasks are in Phase 11.

**Organization**: by user story, in the priority order the spec assigns. One caveat particular to this
project: the runtime deliverable is a **single Markdown file**, so most tasks add a section to
`spectra/commands/test-plan.md` and are therefore **strictly sequential within a phase**. Genuine
parallelism appears in Phase 10 (publishing, different files) and Phase 11 (tests, different files).

**The one item to carry through**: FR-021a records that the deliverable is written to
`specs/<feature>/test-plan.md` rather than under the artifact root — Principle VII's Spec Kit carve-out,
read to cover a document that is also a stakeholder deliverable. It is argued in [plan.md](./plan.md)
Complexity Tracking, and **T075 pins its consequence**: `test-plan.md` must stay out of `CANONICAL` in
`tests/test_doc_output_paths.py`, because every assertion that dict drives describes a command that
*writes* to the artifact root. "Deliberately absent" and "someone forgot" look identical in a dict, so
the omission gets an assertion of its own.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — different file, no dependency on an incomplete task
- **[Story]**: the user story the task serves (US1–US6)
- Every task names its file and cites the requirements it implements

## Path Conventions

This is a Spec Kit extension, not an application. There is no `src/`.

- Runtime deliverables: `spectra/commands/test-plan.md`, `spectra/templates/test-plan-template.md`
- Manifest and catalog: `spectra/extension.yml`, `catalog.json`
- Roster and docs: `agents-list.json`, `README.md`, `AGENTS_LIST.md`, `docs/index.html`, `spectra/README.md`
- Package: `docs/packages/spectra.zip` (built, never hand-edited)
- Tests: `tests/`

**One text constraint applies to every task that writes prose into `spectra/commands/test-plan.md` or
`spectra/templates/test-plan-template.md`**: `tests/test_doc_output_paths.py` sweeps *all* command files
for absolute output paths, matching the literal tokens `` `/docs/ ``, `` `/brds ``, ` /docs/`, and
` /brds/`. Write every path project-relative — `docs/test-strategy/`, never `/docs/test-strategy/` — and
never place a space or a backtick immediately before a leading slash on a path.

---

## Phase 1: Setup

**Purpose**: record what "before" looks like, then create the file with its interface and its one
governing rule.

- [X] T001 Record the pre-implementation baseline from the repository root: `python3 tools/generate_agent_docs.py --check` reads **48 agents / 8 prose blocks / roster and manifest agree**; `python3 tools/build_package.py` followed by `git diff --stat docs/packages/spectra.zip` shows no drift; `spectra/extension.yml` is at **1.13.0** with **8** commands and **6** templates, and `catalog.json` agrees at 1.13.0 / 8; `tests/test_roster_data.py` asserts **48 agents, 17 available, 31 planned, 9 from Spec Kit, 8 Spectra-shipped**; `python3 -m unittest discover -s tests` is green at **884 tests**. Phase 11 asserts these became 49 agents / 9 prose blocks / 1.14.0 / 9 commands / 7 templates / 18 available / 31 planned / 9 Spectra-shipped.
- [X] T002 Create `spectra/commands/test-plan.md` with YAML front matter carrying a single `description` key in the style of `spectra/commands/test-strategy.md`, an H1 title, and a one-paragraph statement of the job: take a specification, read it and the project, and write one stakeholder-facing test plan beside it that `/speckit-plan` can then design around (FR-001, FR-002).
- [X] T003 Add the **User Input** section to `spectra/commands/test-plan.md` per [contracts/command-interface.md](./contracts/command-interface.md): the whole surface is one **required** path passed through the generic arguments placeholder, plus the single `--non-interactive` flag. State that with empty input the command asks for a specification path and stops, reading and writing nothing (FR-004, FR-007). Use no agent's invocation syntax anywhere in the file (FR-003).
- [X] T004 Add the **one rule that governs everything** section to `spectra/commands/test-plan.md`, stated once and in full: *read the specification you were handed and the project around it, then write exactly one file — `test-plan.md`, beside that specification — and never guess which specification was meant.* Name it as the sentence every later rule narrows, in the style of the equivalent section in `spectra/commands/impact.md`.

**Checkpoint**: the file exists, declares its input surface, and states its limit.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the machinery every story depends on — the prohibitions, the honesty rules, argument
resolution, context reading, the lens vocabulary, and template resolution.

**⚠️ CRITICAL**: no user story work can begin until this phase is complete. Every task except T010 edits
the same file and they are strictly sequential.

- [X] T005 Add the **prohibition list** to `spectra/commands/test-plan.md`, reproducing the write-scope table in [contracts/command-interface.md](./contracts/command-interface.md): never infer which specification was meant (FR-008); exactly one file written per run and the input specification never modified (FR-018); never edit the constitution, create a branch, stage, or commit (FR-019); never write test code or modify test framework, coverage, or CI configuration (FR-020); never run, build, or install anything — including the test suite (FR-020, R9); no network request and no repository URL, credential, or token accepted (FR-020a); never edit a core Spec Kit command or register a hook (FR-005); never invoke another command (FR-048); never create or edit a template file (FR-057); never reproduce a secret value (FR-020b). State explicitly that no argument, attachment, or instruction in the session enables any of them.
- [X] T006 Add the **rules that never bend** section to `spectra/commands/test-plan.md` — the rules that are the product, per [contracts/traceability-contract.md](./contracts/traceability-contract.md): (R1) every acceptance criterion reaches a condition or an uncovered item, never neither (FR-023, FR-025); (R2) every condition names the specification item it verifies, using that item's own identifier (FR-024); (R3) never invent a decision the specification does not contain — an ambiguous requirement gets a stated gap, never a fabricated condition (FR-027); (R4) a coverage claim cites a test file and an absence claim cites the search (FR-028, FR-029); (R5) no checkbox and no tracking field, in any section, from any template layer (FR-041, FR-042); (R6) state what portion of the code and tests was read (FR-016). State that these stay with the command and are **not** part of the template, in the style of `review-pr`'s equivalent clause.
- [X] T007 Add **Step 1 — Resolve the specification** to `spectra/commands/test-plan.md` per [contracts/command-interface.md](./contracts/command-interface.md) and [research.md](./research.md) §1: the four-way resolution — empty stops and asks; a readable file becomes a candidate; a directory resolves to the one `spec.md` inside it, stated aloud; a directory with several candidates and no `spec.md` is listed and asked about, never chosen. State the weak usability test (Markdown-like, non-empty, one heading, plus one of a requirements, user-scenario, acceptance-criteria, or success-criteria section under any wording) and state why it is deliberately weak: a project may override its spec template, so requiring exact headings would refuse to run on a supported configuration.
- [X] T008 Add **Step 2 — Read the project** to `spectra/commands/test-plan.md`: read the resolved specification in full, then, where present, `.specify/memory/constitution.md`, the project's test strategy document, existing test directories and test framework configuration, dependency manifests, CI workflow definitions, and the source the specification's behaviour touches (FR-011). Record every input consulted by path, and record by name and reason any input expected and not readable (FR-015). State the coverage of what was read out of what is present, and by what selection method (FR-016). State that a question the specification or the repository already answers is never asked (FR-017), and that where repository-wide text search is unavailable the run says so and reports reduced coverage rather than narrowing silently.
- [X] T009 Add **Step 3 — Resolve the level vocabulary** to `spectra/commands/test-plan.md` per [research.md](./research.md) §4 and §5: resolve `Artifact root:` from the constitution case-insensitively, rejecting a value with a leading slash or a `..` segment with a stated reason and falling back to the default `docs/`, then look for the strategy at `docs/test-strategy/TEST_STRATEGY.md` under the resolved root (FR-012). State the precedence — the strategy's lens names verbatim, else lens names the constitution declares, else `unit` · `integration` · `api-contract` · `end-to-end` · `manual` (FR-035, FR-036) — that `manual` is always appended to an inherited set that omits it, that a constitutional obligation outranks the strategy with the divergence reported (FR-013), and that an absent strategy is stated once and the run continues (FR-014). State explicitly that this resolution is **read-only**: no publication check, no `documents/` recommendation, and no offer of the declaration line, because none of those obligations attach to reading and the output destination is fixed by the input path.
- [X] T010 [P] Create `spectra/templates/test-plan-template.md` declaring the sections from [contracts/document-contract.md](./contracts/document-contract.md) in order — the identifying block, 1. Scope, 2. Risks, 3. Test Conditions, 4. Environment & Data, 5. Exit Criteria — in the style of `spectra/templates/test-strategy-template.md`. **Exit criteria are plain statements, not a checklist**: the file must contain no `- [ ]` and no `- [x]` anywhere (FR-041). Carry the optional-section guidance from [research.md](./research.md) §12 as an HTML comment marked as authoring guidance that never reaches the output (FR-044). Section structure only: carry no traceability rule, no citation rule, and no priority derivation, all of which stay with the command (Principle VIII).
- [X] T011 Add **Step 4 — Resolve the document's template** to `spectra/commands/test-plan.md`: the five layers in priority order — `.specify/templates/overrides/test-plan-template.md`, the preset layer, `.specify/extensions/spectra/templates/test-plan-template.md`, `.specify/templates/test-plan-template.md`, then the command's own inline skeleton — taking the first readable, non-empty layer, with no single path hard-coded (FR-054). Report the resolved path in the session. Honour the resolved sections and their order; note rather than reinstate an omitted section (FR-055). Strip guidance comments and placeholder tokens whichever layer supplied them (FR-043), and never write a template file (FR-057). State the override path once as the supported customization route, and that editing the installed copy under `.specify/extensions/` is not it.
- [X] T012 Add the **no-checkbox override rule** to `spectra/commands/test-plan.md` as the one place the command overrides a template's content rather than declining to extend it: a checkbox construct found in any resolved layer is rendered as a plain statement, the section is kept, the run is not refused, and the count of converted constructs is reported (FR-041). State the reason inline so a future editor reads it before removing it — an approval document containing live checkboxes creates a second apparent source of truth about progress that will disagree with `tasks.md`.

**Checkpoint**: the prohibitions, the never-bend rules, argument resolution, context reading, the lens
vocabulary, both resolutions, and the shipped template are all in place. User story work can begin.

---

## Phase 3: User Story 1 — Agree the tests before writing any code (Priority: P1) 🎯 MVP

**Goal**: a team that has just finished `/speckit-specify` gets one document beside their spec — scope,
risks, traceable conditions, environment, exit criteria — with no checkbox anywhere in it.

**Independent Test**: run against a feature directory containing only `spec.md`; verify `test-plan.md`
appears beside it, every acceptance criterion appears in at least one condition, and the file contains
no checkbox in any section.

- [X] T013 [US1] Add **Step 5 — Derive the test conditions** to `spectra/commands/test-plan.md` per [contracts/traceability-contract.md](./contracts/traceability-contract.md): one row per thing that must be true, each with an identifier scoped to this document, the condition in one line, what it verifies, its level, and its priority (FR-034). State that conditions are things that must be true and **never** test scripts or step sequences (FR-038).
- [X] T014 [US1] Add the **reference forms** to `spectra/commands/test-plan.md`: the specification's own identifier used verbatim where it has one; the composed `USn-ACn` form for an acceptance scenario, because Spec Kit numbers scenarios within a story so a bare `AC1` is ambiguous across stories; a six-to-twelve-word verbatim quotation in quotation marks as the last resort for prose with no identifier. State that the command never mints an identifier for a specification item, never renumbers, and never edits the specification to add one (FR-024, R3).
- [X] T015 [US1] Add the **level assignment** rules to `spectra/commands/test-plan.md`: assign each condition to the **cheapest** level from the resolved vocabulary that can actually verify it, and never name a level or tool the project's dependency manifests cannot support — no browser anywhere means no browser-driven level (FR-037). State that `manual` is available even where the inherited vocabulary omits it, because a plan must be able to place a condition no automated lens will ever cover, and that forcing such a condition into "explicitly not covered" would be false: it is covered, by a person.
- [X] T016 [US1] Add the **priority derivation** to `spectra/commands/test-plan.md` per [research.md](./research.md) §8: a condition inherits the priority of the specification item it verifies — P1/P2/P3 from the story, P2 for a requirement unreachable from any story, **P1** for a prohibition, safety, or data-integrity property regardless of story, and the measured story's priority for a success criterion. State that only P1 conditions gate the exit criteria, and that where the specification carries no priorities the command says so and derives from the risk table's impact axis alone.
- [X] T017 [US1] Add the **uncovered items** rules to `spectra/commands/test-plan.md`: the four reasons and their remedies from [contracts/traceability-contract.md](./contracts/traceability-contract.md) — `unresolved-clarification` naming `/speckit-clarify` as a command the *user* runs (FR-026), `untestable-as-written` naming the missing decision (FR-027), `out-of-scope` naming who covers it, `deferred` naming when or by whom. State the prohibition that makes the section work: never invent the missing decision, because a fabricated condition launders a guess into something a stakeholder approves. Require the section to be present and non-empty or explicitly stated as empty (FR-039).
- [X] T018 [US1] Add **Step 6 — The scope section** to `spectra/commands/test-plan.md`: what is in scope, and what is deliberately out of scope with each out-of-scope item naming who covers it if anyone (FR-031). State why out-of-scope carries more weight than in-scope — it is the line pointed at later when someone asks why a bug was not caught — and give the story titles once here so the `USn-ACn` references in the conditions table are legible to a reader with the spec open.
- [X] T019 [US1] Add **Step 7 — The risk section** to `spectra/commands/test-plan.md` per [research.md](./research.md) §7: two to five rows; impact derived from stated triggers (data loss or corruption, an external contract break, data exposure, or a blocked release → High; wrong behaviour a user or caller notices → Medium; otherwise Low); likelihood derived from whether the touched area has current coverage and whether the change is additive; and a response of deeper coverage, an extra scenario, or **accept** (FR-032). State that `accept` is a first-class answer and must appear where the rating does not justify effort, and that a table rated uniformly High/High is re-derived rather than presented as a prioritization — and if the derivation genuinely produces all-High, that it says so and names why (FR-033).
- [X] T020 [US1] Add **Step 8 — Environment, data, and exit criteria** to `spectra/commands/test-plan.md`: where tests run and what is stubbed versus real; the test data, fixtures, accounts, seed state, and how it is reset; the prerequisites — flags, migrations, access, third-party sandboxes (FR-040). Then exit criteria as **plain declarative statements**, each with its threshold and the role who confirms it, with no checkbox construct (FR-040, FR-041). State the bar for the section: someone else must be able to run these tests from it alone.
- [X] T021 [US1] Add the **secret rule** to `spectra/commands/test-plan.md` in the style of the equivalent clause in `spectra/commands/impact.md`: where a condition depends on a credential, name its kind and where it is configured and state that the value was withheld; never reproduce a secret value in the document or in the session, in whole or in fragment (FR-020b). Name the shapes to watch for, and state that over-withholding is the correct error to make.
- [X] T022 [US1] Add **Step 9 — The identifying block and build under test** to `spectra/commands/test-plan.md` per [research.md](./research.md) §11: the specification as a project-relative path, the build under test, and the author and date (FR-030). Populate the build from the current branch plus a version string only where the project commits one, labelled with its source; state that nothing is inferred and that "the working tree on branch X, no version committed" is a correct answer while a guessed release number is not.
- [X] T023 [US1] Add **Step 10 — Write the document** to `spectra/commands/test-plan.md`: write exactly one file, `test-plan.md`, in the directory of the resolved specification, as the run's final act, following the resolved template's sections in its order (FR-021). State that no artifact root is resolved for the output, no subfolder is created, and no sequence number is assigned — and state the reason, with a pointer to the fact that this document's identity is the feature directory exactly as `spec.md` and `plan.md` have no number because the directory already supplies one.
- [X] T024 [US1] Add the **forbidden output** table to `spectra/commands/test-plan.md` from [contracts/document-contract.md](./contracts/document-contract.md): no checkbox construct, no status or progress or completion field, no unfilled placeholder token or guidance comment, no optional-section guidance list, no minted identifier, no secret value, no unqualified claim of absence, no unrunnable level or tool, and no test script in the condition column (FR-041 to FR-044).
- [X] T025 [US1] Add **Step 12 — Report** to `spectra/commands/test-plan.md` per [contracts/chat-output.md](./contracts/chat-output.md): the written path and whether it was created or rewritten; the traceability count, covered out of found, with the uncovered items and their reasons; the resolved lens vocabulary and its source; the resolved template layer by path and any checkbox constructs converted; what portion of the code and tests was read and by what method; every input expected and not readable, by name and reason; and which optional sections were added and why (FR-049). State that the session gets the summary while the document gets the detail.

**Checkpoint**: a feature directory with a spec produces a complete, traceable, checkbox-free test plan
and a session summary. This is the MVP.

---

## Phase 4: User Story 2 — Inherit the project's testing policy (Priority: P1)

**Goal**: a project that has already run `speckit.spectra.test-strategy` gets a plan in its own lens
vocabulary, respecting its floor, naming only tools its stack can run.

**Independent Test**: run in a project with both a constitutional testing obligation and a
`TEST_STRATEGY.md`; verify the Level column uses the strategy's lens names verbatim, no tool appears
that the manifests cannot support, and the plan cites where each inherited constraint came from.

- [X] T026 [US2] Add the **inherited-constraint reporting** rules to `spectra/commands/test-plan.md`: the resolved lens vocabulary and its provenance — `strategy` with its path, `constitution`, or `default` — appear in both the document and the session report (FR-035, FR-036). State that the strategy's lens names are taken **verbatim**: not normalized, not title-cased, not mapped onto the default set, because a silent translation sits between two artifacts a reviewer is reading side by side and the mapping is a guess about a word the team defined deliberately.
- [X] T027 [US2] Add the **precedence and conflict** rules to `spectra/commands/test-plan.md`: where the constitution carries a testing obligation that differs from the strategy document, the constitution prevails and the conflict is reported in the document rather than silently resolved (FR-013). Where neither exists, the plan is still produced, the default vocabulary is used, and the absence is stated (FR-014).
- [X] T028 [US2] Add the **coverage floor** handling to `spectra/commands/test-plan.md`: where the strategy or the constitution declares a floor, the plan states it as an exit criterion with its metric and the role who confirms it, and never proposes a different one. State that the plan does not measure coverage and does not run a coverage tool — it inherits the number and attributes it.
- [X] T029 [US2] Add the **stack-surface gate** to `spectra/commands/test-plan.md`: identify the project's real surfaces from its dependency manifests — browser, HTTP, CLI, library, or none — and state that a level or tool requiring a surface the project does not have is unreachable rather than merely discouraged (FR-037). Name this as the same failure `speckit.spectra.test-strategy` exists to avoid, reappearing one phase later: a plan that assigns a command-line tool's conditions to a browser driver is that defect with a different filename.

**Checkpoint**: a project with a declared policy gets a plan in its own vocabulary, and one without gets
a stated default. Both are legible.

---

## Phase 5: User Story 3 — Refuse to guess which spec was meant (Priority: P1)

**Goal**: every way of getting the argument wrong produces a stop with a reason, and no run ever picks a
specification for the user.

**Independent Test**: invoke with empty input and verify nothing is read and nothing written and no
listing of `specs/` is offered; repeat with a missing path, a `README.md`, a directory with no `spec.md`,
and a spec in a sibling repository.

- [X] T030 [US3] Add the **inference prohibition** to `spectra/commands/test-plan.md` as a named rule with its reason, per [contracts/command-interface.md](./contracts/command-interface.md): with an empty argument the command MUST NOT consult the current Git branch name, `.specify/feature.json` or any other feature record, file modification times, the contents or listing of `specs/`, or any cache or session history (FR-008). State the reason inline so a future editor reads it before removing it: the output is circulated and approved, and a plan generated against the wrong specification is undetectably wrong to whoever signs it. State that this is deliberately less helpful than the rest of the workflow.
- [X] T031 [US3] Add the **missing-argument response** to `spectra/commands/test-plan.md` per [contracts/chat-output.md](./contracts/chat-output.md): say what to supply, show the shape of the invocation with a path, and state that nothing was read and nothing written (FR-007, FR-009). State explicitly that the response does **not** list the contents of `specs/` — a picker is a second-order version of the same problem, because it still asks the user to choose from a list the command assembled and one wrong keystroke produces the same wrongly-grounded signed document.
- [X] T032 [US3] Add the **stop conditions** to `spectra/commands/test-plan.md`, one line each with what is reported: a path that is missing or unreadable; a readable file that fails the usability test; a directory with no `spec.md`; a directory with several candidates and no `spec.md` (list and ask, never choose) (FR-010). State that each stop names the path and the reason, and that none of them writes anything.
- [X] T033 [US3] Add **the out-of-project gate** to `spectra/commands/test-plan.md` per [contracts/chat-output.md](./contracts/chat-output.md): where the resolved specification's directory lies outside the project the command was invoked in, report the conflict and stop before writing (FR-022). State that this gate takes no answer — it is not a confirmation — and that the command does not relocate the output into the invoking project instead. Name this as the guard that replaces the write-scope protection an artifact root would have given.
- [X] T034 [US3] Add the **flag handling** to `spectra/commands/test-plan.md`: `--non-interactive` is the only defined flag; an unrecognized flag is reported and ignored and never silently becomes part of the path. State that an empty argument stops even in a non-interactive session, because that is a missing input rather than a gate (FR-009, FR-052).

**Checkpoint**: every wrong argument stops with a reason, and no code path selects a specification.

---

## Phase 6: User Story 4 — Hand the agreed plan to the planner (Priority: P2)

**Goal**: a completed run ends with a copyable invocation that tells `/speckit-plan` to design around
the plan, and nothing in the project has been wired to make that happen.

**Independent Test**: complete a run and verify the closing output contains a literal planning-command
invocation naming the written path, that no hook was registered, and that no core command file changed.

- [X] T035 [US4] Add **Step 13 — The handoff** to `spectra/commands/test-plan.md` per [contracts/plan-handoff.md](./contracts/plan-handoff.md): emit a ready-to-copy invocation of the Spec Kit planning command naming the written plan's project-relative path and stating the obligation — that every P1 condition maps to a task which writes the test before the implementation it covers (FR-047). Present it as something the **user** runs; name the Spec Kit command rather than any agent's spelling of it, in the style of the `/speckit-constitution` handoff in `spectra/commands/test-strategy.md`.
- [X] T036 [US4] Add the **handoff prohibitions** to `spectra/commands/test-plan.md`: the command never invokes the planning command or any other (FR-048); registers no hook; writes no marker into `spec.md`; and edits no core Spec Kit command file (FR-005, FR-018). State why a `before_plan` hook was rejected — it would make every project that installs Spectra prompt for a test plan on every feature, which is the opposite of the opt-in add-on this is — and state that `/speckit-plan` works exactly as it does today for anyone who never runs this command.
- [X] T037 [US4] Add the **when the handoff is withheld** rules to `spectra/commands/test-plan.md`: no handoff is emitted when no argument was supplied, when either gate stopped the run, or when an existing plan was not rewritten. A run that wrote nothing never emits a handoff for a file it did not produce.

**Checkpoint**: the handoff is printed on every successful write and withheld on every run that wrote
nothing. Nothing in the project was modified to enable it.

---

## Phase 7: User Story 5 — Re-run after the spec changes (Priority: P2)

**Goal**: a second run reads the existing plan, asks before replacing it with a statement of what would
change, and never silently destroys a decision a human made.

**Independent Test**: generate a plan, edit the spec, re-run; verify the existing plan was read, that
rewriting required confirmation, that declining leaves the file byte-identical, and that a prior
not-covered decision is carried forward or its removal stated.

- [X] T038 [US5] Add **Step 11 — The existence gate** to `spectra/commands/test-plan.md` per [contracts/chat-output.md](./contracts/chat-output.md): where `test-plan.md` already exists beside the resolved specification, read it and treat it as an input (FR-050), then ask before rewriting (FR-051). State that the gate fires **after** the derivation so the request can state what would change — conditions added and removed, decisions carried forward, sections unchanged — and state why: a confirmation request with no information attached is one a user learns to answer reflexively, which is the same as having no gate.
- [X] T039 [US5] Add the **preservation rule** to `spectra/commands/test-plan.md`: any condition the previous plan recorded as *explicitly not covered*, and any accepted risk, is carried forward or its removal is stated in the run report (FR-051). State the reason — the not-covered list is the part most likely to hold a decision a human made deliberately, and no re-read of the specification will recover it.
- [X] T040 [US5] Add the **declined and non-interactive** paths to `spectra/commands/test-plan.md`: declining the gate leaves the file untouched and writes nothing else, and the run says so (FR-051). A session that cannot take an answer may **create** a plan that does not exist but may not rewrite one — it reports that a plan exists and what it would have changed (FR-052). State the asymmetry and its reason: creating is additive and recoverable, while rewriting destroys a document that may already have been circulated and approved.
- [X] T041 [US5] Add the **no-second-file rule** to `spectra/commands/test-plan.md`: the filename is fixed, and the command never writes `test-plan-2.md` or any variant. Two documents with no statement of which is current is the failure numbering was rejected for in the first place.

**Checkpoint**: a re-run is safe, informative, and preserves what a human decided.

---

## Phase 8: User Story 6 — Plan against a codebase that already exists (Priority: P3)

**Goal**: conditions the suite already covers are identified as such with a citation, so nobody is asked
to approve re-testing ground the suite already holds.

**Independent Test**: run against a spec for a change to an existing, tested module; verify already-
covered conditions cite their test file and that every gap cites what was searched for and where.

- [X] T042 [US6] Add **the existing-coverage read** to `spectra/commands/test-plan.md` per [research.md](./research.md) §9: establish what the current suite guarantees by reading test source — test files importing or referencing the touched module, test names describing the behaviour, assertions against the identifiers the specification names. State that the suite is **never executed** and no coverage tool is run, and state the reason: the question here is per-behaviour, and a line-coverage figure answers the repository-level question this command does not ask, so there is nothing to gain from execution and an unbidden test run on a stranger's repository is unbounded in time and may touch the network.
- [X] T043 [US6] Add the **two absence obligations** to `spectra/commands/test-plan.md`: a claim that a behaviour **is** covered cites the test file (FR-029); a claim that it **is not** cites the search — what terms, in what paths (FR-028). State the permitted and forbidden phrasings side by side, in the style of the equivalent rule in `spectra/commands/impact.md`: "no test referencing X found under `<paths>`" is permitted, and "there is no coverage for X" is not, because the first is a fact about a search and the second is a claim about the system.
- [X] T044 [US6] Add the **already-covered marking** to `spectra/commands/test-plan.md`: a condition the suite already covers carries that fact and its citation in the conditions table rather than being dropped, so a reviewer can see it was considered. State that dropping it would make the plan look incomplete and keeping it unmarked would ask for approval to redo work already done.

**Checkpoint**: a brownfield feature's plan distinguishes new coverage from existing coverage, with
citations both ways.

---

## Phase 9: Document Assembly

**Purpose**: the sections that can only be written once every other section exists.

- [X] T045 Add the **optional sections** step to `spectra/commands/test-plan.md` per [research.md](./research.md) §12: the trigger for each section the command may add — non-functional targets when the specification or constitution states a performance, security, or accessibility budget; rollback and migration testing when a schema change, migration, or backfill is implied; roles and responsibilities when a separate QA function or more than one executing team is named; approvals and sign-off when a regulated or audited regime is declared (FR-045). State that schedule and milestones, suspension and resumption criteria, and a test summary report are **never added automatically** and are offered only if the user asks, with the reason: the first two are project management rather than test design and a generator inventing dates produces something a stakeholder may act on, and the third reports an outcome while this document states intent.
- [X] T046 Add the **known limitations, stated in every document** section to `spectra/commands/test-plan.md`: existing coverage was established by reading tests and not by running them, so a test that exists and fails reads as coverage; the conditions rest on the specification as written at the stated date and go stale when it changes; no tool was verified against a registry because no network request was made; and this command states what will be verified while `/speckit-tasks` and `/speckit-implement` produce and write the tests. Name the adjacent agents rather than answering their questions: `speckit.spectra.test-strategy` owns the project-wide policy, and `speckit.spectra.flaky-test-detector` owns tests that already exist.
- [X] T047 Add the **Inline template skeleton** section to `spectra/commands/test-plan.md` (depends on T010 and every section above): a fenced block declaring exactly the H2 headings of `spectra/templates/test-plan-template.md`, **in the same order**. `tests/test_document_templates.py` strips trailing `<!-- … -->` annotations and asserts the two heading lists are equal and ordered, so a divergence here fails the suite. The skeleton must itself contain no checkbox construct.
- [X] T048 Read `spectra/commands/test-plan.md` end to end against [contracts/command-interface.md](./contracts/command-interface.md) and [contracts/chat-output.md](./contracts/chat-output.md) and confirm every refusal and every degradation is stated somewhere in the file: empty argument, missing path, unusable file, directory with no spec, ambiguous directory, out-of-project spec, no constitution, no strategy, unusable declared root, empty template layer, no text search, specification with no identifiers, specification with no priorities, specification with no testable behaviour, existing plan, and non-interactive session.
- [X] T049 Grep `spectra/commands/test-plan.md` and `spectra/templates/test-plan-template.md` for the four absolute-path tokens `tests/test_doc_output_paths.py` matches — `` `/docs/ ``, `` `/brds ``, ` /docs/`, ` /brds/` — and for any `- [ ]` or `- [x]` construct, and confirm both files are clean before Phase 10. This is the one pair of mistakes an author makes by habit rather than by decision.

**Checkpoint**: the runtime deliverable is complete, internally consistent, and clean against the
repository's text assertions.

> **Step numbering as implemented differs from the numbering quoted in the task descriptions**, and the
> difference is deliberate. Two steps were inserted ahead of the derivation — *Step 5, establish what
> this project rules out* (the surfaces and the inherited floor, T028/T029) and *Step 6, establish what
> the suite already covers* (T042–T044) — because choosing a level and filling the already-covered
> column both depend on them. The existence gate moved **before** the write (Step 12, ahead of Step 13)
> because [data-model.md](./data-model.md) §3 requires gate-before-write, and the numbering in T023 and
> T038 would have put the confirmation after the file was already replaced. The shipped order is:
> 1 resolve the specification · 2 read the project · 3 resolve the level vocabulary · 4 resolve the
> template · 5 what the project rules out · 6 existing coverage · 7 derive the conditions · 8 scope ·
> 9 risks · 10 environment, data, exit criteria · 11 identifying block · 12 existence gate · 13 write ·
> 14 report · 15 handoff.

---

## Phase 10: Publishing Surface (Principle V)

**Purpose**: make the command real to a consumer. These touch different files and are the only genuinely
parallel work in the plan — except where a task reads another's output.

- [X] T050 [P] Register both artifacts in `spectra/extension.yml`: add `speckit.spectra.test-plan` → `commands/test-plan.md` to `provides.commands` with a description naming the required spec argument, the write target beside the specification, the no-checkbox property, and the planning-command handoff; add `test-plan-template` → `templates/test-plan-template.md` to `provides.templates` with the override path in its description, in the style of the six entries already there; bump `extension.version` 1.13.0 → **1.14.0**; add the tags `test-plan` and `tdd` (FR-001, FR-058).
- [X] T051 [P] Add a `[1.14.0]` entry to `spectra/CHANGELOG.md` recording the new command and registered template, and the four decisions a reader would otherwise find surprising: the specification argument is **required and never inferred**; the document is written **beside the spec** rather than under the artifact root; it carries **no checkboxes**, exit criteria included, because it is an approval document rather than a tracker; and `/speckit-plan` is handed a printed invocation rather than a hook.
- [X] T052 [P] Add the roster entry to `agents-list.json`: `id: test-plan`, `title: Test Plan`, a one-line description, `status: available`, `phase: requirements-discovery`, `type: add-on`, `provider: spectra`, `command: speckit.spectra.test-plan` — matching the shape of the `impact` entry. A `command` key is required exactly because the status is `available`. `tests/test_roster_data.py` asserts titles are unique; verified during planning that `Test Plan` collides with none of the 48 existing titles, though `Test Strategy`, `Testing`, `Test Coverage Analyst`, `Test Automation Analyst`, and `Flaky Test Detector` all exist (FR-006).
- [X] T053 Regenerate every structured listing with `python3 tools/generate_agent_docs.py` (depends on T050, T052): the Agents table in `README.md`, the Spec Kit core and Roadmap sections of `AGENTS_LIST.md`, and the Commands table in `spectra/README.md`. Do not hand-edit anything between the `SPECTRA:GENERATED` markers (FR-062, Principle V).
- [X] T054 Hand-author the prose block in `AGENTS_LIST.md` anchored `<!-- SPECTRA:AGENT id=test-plan -->` (depends on T052), in the style of the eight blocks already there: what it does, that it will not guess which spec you meant, where it writes and why that is beside the spec, that it carries no checkboxes because it is for approval rather than tracking, how it inherits a project's lens vocabulary, and what the user does with it next. Automation guarantees the block exists, never what it says (FR-062).
- [X] T055 [P] Add the command to `docs/index.html` in the commands list, with an example invocation naming a spec path, matching the eight entries already there. Do not hard-code the version or the description — the page reads those from `catalog.json` and `agents-list.json` at load (FR-061, Principle V).
- [X] T056 Update the `spectra` entry in `catalog.json` (depends on T050): `version` → 1.14.0, `provides.commands` 8 → **9**, both `updated_at` fields, and the two new tags — the values must match `spectra/extension.yml` exactly or CI's drift job fails (FR-059).
- [X] T057 Rebuild the package with `python3 tools/build_package.py` (depends on T010, T050, and the finished command file) and confirm `docs/packages/spectra.zip` contains `spectra/commands/test-plan.md` and `spectra/templates/test-plan-template.md` under a single top-level `spectra/` folder (FR-060).
- [X] T058 [P] Add the manual pass rows to `test/README.md` covering the four things only a human can confirm: an empty invocation reads nothing and lists nothing; a checkbox in a template override does not survive into the output; an acceptance criterion that reaches no condition is reported rather than concealed; and a vague requirement gets a stated gap rather than a fabricated condition.

**Checkpoint**: a consumer running `spectra install` would get the command, and every published surface
agrees with the extension folder.

> **One obligation the task list missed**, found by running the generator rather than by reading it:
> `tools/generate_agent_docs.py --check` also asserts that a shipped agent's **canonical title appears in
> `spectra/README.md`** outside the generated region ("does not mention the canonical title for
> 'test-plan'"). T053 regenerated the Commands table there, but the per-command prose section that the
> eight existing commands each have is hand-written and is not optional — the check fails without it. A
> `## speckit.spectra.test-plan — Test Plan` section was written alongside T054's `AGENTS_LIST.md` block.

---

## Phase 11: Validation

**Purpose**: prove the rules survived contact with the file, and that an agent actually follows them.

- [X] T059 [P] Create `tests/test_test_plan_flow.py` in the style of `tests/test_test_strategy_flow.py`, asserting on the text of `spectra/commands/test-plan.md`: the required argument and the ask-and-stop behaviour (**SC-005**); the inference prohibition naming the branch, the feature record, modification times, and a `specs/` scan as things never consulted; the single write target beside the specification with no sequence number and no artifact subfolder; the out-of-project gate; the traceability invariant in both directions (**SC-002**, **SC-003**); the never-invent-a-decision rule; the cited-absence rule in both forms (**SC-008**); the no-checkbox rule including the override-conversion clause (**SC-004**); the no-tracking-field rule; the level-vocabulary precedence with `manual` always available (**SC-006**); the stack-surface gate; the never-runs-anything posture; the planning-command handoff named as a user action rather than an invocation (**SC-009**); the preservation rule for not-covered decisions (**SC-010**); and the absence of any network, URL, or credential instruction.
- [X] T060 [P] Add a checkbox assertion to `tests/test_test_plan_flow.py` sweeping both `spectra/templates/test-plan-template.md` and the inline skeleton inside `spectra/commands/test-plan.md` for `- [ ]` and `- [x]`, asserting neither appears. This is the only invariant in the feature that can be pinned with an exact match and no false positives, so it is asserted on the artifacts rather than inferred from the prose.
  > **Assertions read whitespace-normalized text.** The command file is hard-wrapped prose, so the first
  > run of `test_test_plan_flow.py` failed on a phrase that straddled a line break — *"Read nothing,
  > analyze nothing, write / nothing."* The module therefore collapses whitespace before matching
  > (`flat()`), so an assertion fails when a **rule** is deleted rather than when a paragraph is
  > re-flowed. The checkbox regex stays **line-anchored** for the opposite reason: only a line-initial
  > bullet renders as a checkbox, and the command has to be able to *name* the construct it forbids
  > without reproducing it.
- [X] T061 [P] Add `"test-plan.md": "test-plan-template"` to `DOCUMENT_COMMANDS` in `tests/test_document_templates.py`, which asserts registration both ways, heading parity between the shipped template and the command's inline skeleton, all four resolution layers present in the command, the override layer named first, the command reporting the template it used, an inline last resort, no hard-coded template path, and no executable asset.
- [X] T062 [P] Add the **negative** assertion to `tests/test_doc_output_paths.py` asserting `"test-plan.md"` is **not** a key of `CANONICAL`, with a failure message carrying the reason: every assertion `DOCUMENT_COMMANDS` drives describes a command that writes into the artifact root — the literal `never write it`, all six publication signals, the `documents/` fallback — and this command writes beside the specification it was handed and reads the declared root only to locate the strategy document. Point the message at [plan.md](./plan.md) Complexity Tracking. Also assert the command does contain `Artifact root:` so the read-only resolution cannot silently disappear.
  > **Verified by violation, per the Notes below.** Adding `"test-plan.md": "docs/test-plan/"` to
  > `CANONICAL` locally made this assertion fail as intended — and, usefully, made **seven others**
  > fail too: the canonical-folder check plus all six publication signals. That is the plan's argument
  > demonstrated rather than asserted: the entry would have required three clauses in the shipped
  > command that are false for it. Restored immediately afterwards.
- [X] T063 [P] Add a write-target assertion to `tests/test_test_plan_flow.py` asserting the command names `test-plan.md` as its output and that **no** artifact-root write target and **no** sequence-number pattern accompanies it, so FR-021's placement stays deliberate rather than drifting in either direction.
- [X] T064 [P] Update the census in `tests/test_roster_data.py`: 48 → **49** agents in `test_it_carries_the_full_published_roster`; 17 → **18** available in `test_it_splits_into_seventeen_available_and_thirty_one_planned`, renaming that method to `..._eighteen_available_...`; **31** planned and **9** from Spec Kit unchanged; and add `"test-plan"` to the id list in `test_spectra_ships_exactly_eight_agents_today`, renaming it to `test_spectra_ships_exactly_nine_agents_today`. That list is sorted, so `"test-plan"` goes immediately before `"test-strategy"`.
- [X] T065 Run the full gate from the repository root (depends on T050–T064): `python3 -m unittest discover -s tests` green, `python3 tools/generate_agent_docs.py --check` reporting **49 agents and 9 prose blocks** with roster and manifest agreeing, and `python3 tools/build_package.py && git diff --stat docs/packages/spectra.zip` showing no drift.
- [X] T066 Install the working copy into a throwaway Spec Kit project with `specify extension add --dev` per [quickstart.md](./quickstart.md), and run Passes 1 through 11, recording the observed result for each. These passes are where the observable success criteria are actually measured: **SC-001** (one invocation from spec to circulable plan), **SC-002** (every acceptance criterion covered or reported), **SC-003** (every condition traces back), **SC-004** (zero checkboxes, including under an override), **SC-005** (empty invocation writes nothing and reads nothing), **SC-006** (every level and tool from the project's own policy or manifests), **SC-007** (a stakeholder can answer the three questions unaided), **SC-008** (every absence claim distinguishable as checked or unchecked), **SC-009** (one printed invocation feeds the planner), **SC-010** (a re-run never silently drops a not-covered decision).
  > **Partially executed 2026-09-11.** A throwaway Spec Kit project was created with
  > `specify init --here --force --non-interactive --integration claude` and the working copy installed
  > with `specify extension add --dev`. Registration verified: **9 commands and 7 templates** at the
  > extension layer, `test-plan-template.md` present under
  > `.specify/extensions/spectra/templates/`, and `speckit-spectra-test-plan` registered as a skill.
  >
  > A brownfield probe was then built — a Python package (`click`, `httpx`, `pytest-cov`) with three
  > modules, one test covering only the *positive* signature path, a CI workflow running `pytest` but
  > not coverage, a constitution with a contract-test obligation and a floor-must-hold principle, and a
  > `TEST_STRATEGY.md` using **deliberately unusual lens names** (`isolated`, `wired`, `contract`,
  > `journey`) so a plan that quietly substituted the default vocabulary would be obvious. The spec
  > carried three prioritized stories, seven requirements including one `MUST NOT`, a planted
  > `[NEEDS CLARIFICATION]` marker on FR-006, and FR-007 phrased too vaguely to test.
  >
  > The command's steps were followed against it and the document produced. **35 of 35 assertions on
  > the output passed**, covering Passes 2, 3, 4, 5, 7, and 10: all four acceptance criteria referenced;
  > FR-006 and FR-007 in the not-covered table with their remedies; **FR-007 given no condition at all**,
  > which is the fabrication check; zero checkboxes with the exit criteria still present; guidance
  > comments, the optional-section list, and placeholder tokens all stripped; all four strategy lens
  > names used verbatim with `manual` appended; the floor carried at 30% against the `REPORTED` 34%
  > baseline and its date, attributed rather than adjusted; the already-covered condition citing
  > `tests/test_verify.py:4`; every absence claim citing its search; the prohibition FR-003 promoted to
  > P1 with the reason stated; four risk rows spanning L/M/H likelihood with one `accept`; the
  > production secret located and withheld; and a re-run touching **only** `test-plan.md`, leaving the
  > spec byte-identical and nothing written under `.specify/` or `docs/`.
  >
  > **One assertion of mine was wrong and the command was right.** An initial check that no browser
  > tool is *named anywhere* failed on five terms — because the plan cites the search it ran for them
  > in *Sources consulted*, which is exactly what FR-028 requires. Scoped to the conditions table and
  > the environment section, where a recommendation would actually live, all five pass. Worth recording:
  > the cited-absence rule and a naive "this word must never appear" check are in direct tension, and
  > the rule wins.
  >
  > **Not executed: Passes 1, 6, 8, 9, and 11 as live agent runs** — the empty-argument gate, the
  > template-override conversion, the re-run confirmation dialogue, the printed handoff, and the
  > published-zip install. Each needs an interactive agent session with the command registered and the
  > agent restarted, which cannot be driven from inside the session that authored the command. Pass 1 is
  > the significant gap: `tests/test_test_plan_flow.py` can prove the instruction is present but not
  > that an agent obeys it, and "asks but reads the project first" is a passing-looking failure.
- [ ] T067 Run Passes 1, 2, and 3 on a **second agent** — the argument gate, the traceability invariant, and the no-fabricated-condition rule — because those three are where a prompt-expressed rule is most likely to be quietly ignored by a different model, and none of them is catchable by `tests/test_test_plan_flow.py`, which can only assert that the *instruction* is present. Record the results in the `test/README.md` rows added by T058.
  > **Not executed, and this is the deferred item that matters most.** It needs a different model in an
  > interactive session with the extension installed, which this session cannot provide. The three
  > behaviours it targets — the argument gate, bidirectional traceability, and the refusal to fabricate
  > a condition — are all prompt-expressed, and a second model ignoring any of them is precisely the
  > failure `tests/test_test_plan_flow.py` cannot catch: it asserts the rule is written down, never that
  > it is followed. The `test/README.md` rows added by T058 are where the result belongs when it is run.

**Checkpoint**: the rules are asserted in the suite, and an agent has been observed following them.

---

## Phase 12: Publish (Constitution Development Workflow step 6)

- [X] T068 Verify the two facts CI will check before pushing: `spectra/extension.yml` and `catalog.json` agree on **1.14.0** and **9** commands, and the committed zip matches the `spectra/` folder.
- [ ] T069 Commit the whole set on branch `021-test-plan-agent`: `spectra/`, `specs/021-test-plan-agent/`, `agents-list.json`, `catalog.json`, `docs/`, `README.md`, `AGENTS_LIST.md`, `test/README.md`, and `tests/`.
- [ ] T070 Open the pull request for branch `021-test-plan-agent` with `speckit.spectra.create-pr` — the extension's own `after_implement` hook — and confirm the body states the 1.14.0 bump, the new `spectra/commands/test-plan.md` and `spectra/templates/test-plan-template.md`, the four decisions from T051, and the Principle VII carve-out reading with a pointer to the Complexity Tracking entry that argues it.

---

## Dependencies & Execution Order

### Phase dependencies

- **Phase 1 (Setup)**: no dependencies.
- **Phase 2 (Foundational)**: depends on Phase 1. **Blocks every user story.**
- **Phases 3–8 (User Stories)**: each depends on Phase 2. They edit the same file, so they are
  sequential in practice even though they are logically independent.
- **Phase 9 (Document Assembly)**: depends on every user story phase — T047 needs T010's headings and
  T048 needs every refusal to exist.
- **Phase 10 (Publishing)**: depends on Phase 9 for the finished command file. Internally parallel
  except T053 (needs T050 and T052), T054 (needs T052), T056 (needs T050), and T057 (needs T010, T050).
- **Phase 11 (Validation)**: T059–T064 depend on the artifacts they assert on; T065 depends on all of
  Phases 10 and 11; T066 and T067 depend on T065.
- **Phase 12 (Publish)**: depends on Phase 11.

### User story dependencies

- **US1 (P1)** — the MVP. Depends only on Phase 2.
- **US2 (P1)** — depends on Phase 2, specifically T009's vocabulary resolution. Independently testable
  against a project with a strategy document.
- **US3 (P1)** — depends on Phase 2, specifically T007's resolution order. Independently testable with
  no project at all, which makes it the cheapest story to verify.
- **US4 (P2)** — depends on US1 having a written path to hand over.
- **US5 (P2)** — depends on US1 producing a document there is a second run of.
- **US6 (P3)** — depends on Phase 2's context reading. Independently testable against any tested module.

### Within each phase

- Tasks editing `spectra/commands/test-plan.md` are **strictly sequential** — same file.
- T010 is the only `[P]` task before Phase 10, because it is the only one touching a different file.
- Phase 11's test modules are independent of each other and all `[P]`.

### Parallel opportunities

- **Phase 10** is the real one: T050, T051, T052, T055, and T058 touch five different files.
- **Phase 11**: T059 through T064 touch four different files and can all run together.
- Nothing in Phases 1–9 parallelizes beyond T010, and pretending otherwise would produce merge
  conflicts in a single Markdown file.

---

## Parallel Example: Phase 10

```bash
# Five different files, no ordering between them:
Task: "T050 Register both artifacts in spectra/extension.yml and bump to 1.14.0"
Task: "T051 Add the [1.14.0] entry to spectra/CHANGELOG.md"
Task: "T052 Add the roster entry to agents-list.json"
Task: "T055 Add the command to docs/index.html"
Task: "T058 Add the manual pass rows to test/README.md"

# Then, in order, the tasks that read their output:
Task: "T053 Regenerate the structured listings"   # needs T050, T052
Task: "T056 Update catalog.json"                  # needs T050
Task: "T057 Rebuild docs/packages/spectra.zip"    # needs T010, T050
```

---

## Implementation Strategy

### MVP first (US1 only)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational) — Phase 2 is the blocking one.
2. Complete Phase 3 (US1).
3. **STOP and VALIDATE**: run Passes 1, 2, 3, and 10 from [quickstart.md](./quickstart.md) against a
   throwaway project. A plan that is written, traceable, and checkbox-free is the whole value
   proposition; everything after US1 sharpens it.
4. The command is not publishable at this point — Phase 10 is what makes it real to a consumer — but it
   is demonstrable.

### Incremental delivery

1. Phases 1–2 → the file exists with its limits stated.
2. Phase 3 (US1) → a plan gets written. **MVP.**
3. Phase 4 (US2) → it speaks the project's own vocabulary.
4. Phase 5 (US3) → every wrong argument fails safely.
5. Phase 6 (US4) → the planner can consume it.
6. Phase 7 (US5) → it survives a `/speckit-clarify` cycle.
7. Phase 8 (US6) → it stops asking for work the suite already did.
8. Phases 9–12 → assembled, published, asserted, shipped.

### Parallel team strategy

Limited by the single-file deliverable. The honest split:

1. One person owns `spectra/commands/test-plan.md` through Phases 1–9.
2. A second person can own `spectra/templates/test-plan-template.md` (T010) from the start, and all of
   Phase 11's test modules once the command file is complete.
3. Phase 10 splits five ways for a short burst.

---

## Notes

- **[P] tasks** = different files, no dependencies. Rare here by nature of the deliverable.
- **[Story] label** maps a task to the user story it serves, for traceability.
- **Tests are in Phase 11**, not per-story, because they assert on the finished text of a single file.
  Writing them earlier would mean asserting on sections that do not exist yet.
- **Verify the negative assertion actually fails when violated** (T062): add `test-plan.md` to
  `CANONICAL` locally, confirm the assertion fires, then remove it. A negative test nobody has seen fail
  is a comment.
- Commit after each task or logical group.
- Stop at any checkpoint to validate independently.
- The four failures most worth hunting are ranked at the end of
  [quickstart.md](./quickstart.md) — an empty invocation that analyzes anyway, a criterion covered by
  nothing and reported by nothing, a fabricated condition for a vague requirement, and a checkbox
  surviving an override. All four produce output that looks correct.
