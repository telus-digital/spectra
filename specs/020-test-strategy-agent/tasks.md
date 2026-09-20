# Tasks: Test Strategy Agent

**Input**: Design documents from `/specs/020-test-strategy-agent/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: Included, and not optional here. This repository enforces Principles V, VII, and VIII with a
Python suite — `tests/test_doc_output_paths.py` and `tests/test_document_templates.py` derive their
checks from per-command registries, and `tests/test_roster_data.py` asserts the roster census. A new
document agent that does not appear in all three is unguarded. Test tasks are in Phase 10.

**Organization**: by user story, in the priority order the spec assigns. One caveat particular to this
project: the runtime deliverable is a **single Markdown file**, so most tasks add a section to
`spectra/commands/test-strategy.md` and are therefore **strictly sequential within a phase**. Genuine
parallelism appears in Phase 9 (publishing, different files) and Phase 10 (tests, different files).

**The one violation to carry through**: FR-042a drops Principle VII's `NNN-` filename numbering. It is
justified in [plan.md](./plan.md) Complexity Tracking, and T060 pins it with an assertion so it stays
deliberate rather than becoming drift.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — different file, no dependency on an incomplete task
- **[Story]**: the user story the task serves (US1–US5)
- Every task names its file and cites the requirements it implements

## Path Conventions

This is a Spec Kit extension, not an application. There is no `src/`.

- Runtime deliverables: `spectra/commands/test-strategy.md`, `spectra/templates/test-strategy-template.md`
- Manifest and catalog: `spectra/extension.yml`, `catalog.json`
- Roster and docs: `agents-list.json`, `README.md`, `AGENTS_LIST.md`, `docs/index.html`, `spectra/README.md`
- Package: `docs/packages/spectra.zip` (built, never hand-edited)
- Tests: `tests/`

---

## Phase 1: Setup

**Purpose**: record what "before" looks like, then create the file with its interface and its one
governing rule.

- [X] T001 Record the pre-implementation baseline from the repository root: `python3 tools/generate_agent_docs.py --check` reads **47 agents / 7 prose blocks / roster and manifest agree**; `python3 tools/build_package.py` followed by `git diff --stat docs/packages/spectra.zip` shows no drift; `spectra/extension.yml` is at **1.12.1** with **7** commands and **5** templates, and `catalog.json` agrees at 1.12.1 / 7; `tests/test_roster_data.py` asserts **47 agents, 16 available, 31 planned, 9 from Spec Kit, 7 Spectra-shipped**; `python3 -m unittest discover -s tests` is green at **828 tests**. Phase 10 asserts these became 48 agents / 8 prose blocks / 1.13.0 / 8 commands / 6 templates / 17 available / 31 planned / 8 Spectra-shipped.
- [X] T002 Create `spectra/commands/test-strategy.md` with YAML front matter carrying a single `description` key in the style of `spectra/commands/impact.md`, an H1 title, and a one-paragraph statement of the job: read this project, classify it greenfield or brownfield from evidence, and write one testing strategy covering unit, integration, API contract, and end-to-end testing plus a coverage floor, then offer to have it baked into the constitution (FR-001, FR-002).
- [X] T003 Add the **User Input** section to `spectra/commands/test-strategy.md` per [contracts/command-interface.md](./contracts/command-interface.md): the whole surface is one optional free-text focus hint passed through the generic arguments placeholder. State that the command runs with **no arguments** and that a hint weights the analysis without narrowing the four mandatory lenses (FR-004). Use no agent's invocation syntax anywhere in the file (FR-003).
- [X] T004 Add the **one rule that governs everything** section to `spectra/commands/test-strategy.md`, stated once and in full: *read this project, propose a testing strategy it can actually hold, write exactly one file inside it, and never edit the constitution — no matter who approves.* Name it as the sentence every later rule narrows, in the style of the equivalent section in `spectra/commands/impact.md`.

**Checkpoint**: the file exists, declares its input surface, and states its limit.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the machinery every story depends on — the prohibitions, the honesty rules, context
reading, and the two resolutions.

**⚠️ CRITICAL**: no user story work can begin until this phase is complete. Every task except T012
edits the same file and they are strictly sequential.

- [X] T005 Add the **prohibition list** to `spectra/commands/test-strategy.md`, reproducing the write-scope table in [contracts/command-interface.md](./contracts/command-interface.md): never write `.specify/memory/constitution.md` in any run, approved or not (FR-032); never modify source, test files, test framework config, coverage config, or CI workflow definitions (FR-047); never create a constitution (FR-030); exactly one file written per run (FR-048); no network request and no repository URL accepted (FR-050); no per-test findings and no test file opened for repair (FR-049). State explicitly that no argument, approval, or instruction in the session enables any of them.
- [X] T006 Add the **rules that never bend** section to `spectra/commands/test-strategy.md` — the honesty rules that are the product, per [contracts/document-contract.md](./contracts/document-contract.md) "What the template does NOT govern": (R1) every recommendation carries a citation or the explicit convention marker, never neither (FR-043); (R2) a claim that something is absent cites what was searched and where (FR-044); (R3) in brownfield the floor never exceeds the baseline (FR-022); (R4) a baseline is labelled `measured`, `reported` with its date, or `unavailable` — never unlabelled (FR-023, FR-026); (R5) no tool is named that the surface's stack cannot run (FR-016); (R6) coverage of the analysis is always stated (FR-013). State that these stay with the command and are **not** part of the template, in the style of `review-pr`'s equivalent clause.
- [X] T007 Add **Step 1 — Read the project before you propose anything** to `spectra/commands/test-strategy.md`: read, where present, the constitution under `.specify/memory/`, specifications under `specs/`, `README*`, `CONTRIBUTING*`, documentation directories, dependency manifests, test framework and coverage configuration, CI workflow definitions, and existing test directories (FR-009). Record every input consulted, and record by name and reason any input expected and not readable (FR-011). Read a prior strategy document where one exists and treat it as an input (FR-012). State that where repository-wide text search is unavailable the run says so and reports reduced coverage rather than narrowing silently (FR-013).
- [X] T008 Add **Step 2 — Classify the project** to `spectra/commands/test-strategy.md`, reproducing the five-signal table from [research.md](./research.md) §1: source volume outside scaffolding, test files present, test/coverage tooling configured, CI definition, and specs/ADRs/constitution. State that the classification is `greenfield`, `brownfield`, or `mixed`; that it is never asked of the user (FR-006); that it rests on these signals and **not** on repository age or commit count (FR-007); and that every signal pointing against the chosen mode is reported as dissenting (FR-008). Do not state a numeric threshold.
- [X] T009 Add **Step 3 — Identify the testable surfaces** to `spectra/commands/test-strategy.md` per [research.md](./research.md) §4: read a workspace declaration where one exists and treat it as authoritative; otherwise identify a surface by the co-location of an independent dependency manifest with source under the same root. State that a single-surface project says so once and does not belabour it, and that surfaces with different baselines each carry their own floor (FR-027).
- [X] T010 Add **Step 4 — Resolve where the strategy will live** to `spectra/commands/test-strategy.md` per [contracts/document-contract.md](./contracts/document-contract.md), reusing the wording pattern of the three shipped document agents: read `Artifact root:` case-insensitively; refuse an absolute root or one containing `..` with a stated reason and fall back to the default; check the publication signals `mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, and a Pages configuration pointing at `docs` **before** defaulting to `docs/`; recommend `documents/` where a signal fires with no declared root; take the non-publishing option where the choice cannot be obtained; and state the declaration line but **never write it** (FR-042). The write target is `<artifact-root>/test-strategy/TEST_STRATEGY.md` — one file, **no sequence number** (FR-042a). The literal strings `Artifact root:`, `never write it`, `documents/`, and all six publication signals must appear, because `tests/test_doc_output_paths.py` matches on them.
- [X] T011 Add **Step 5 — Resolve the document's template** to `spectra/commands/test-strategy.md`: the five layers in priority order — `.specify/templates/overrides/test-strategy-template.md`, the preset layer, `.specify/extensions/spectra/templates/test-strategy-template.md`, `.specify/templates/test-strategy-template.md`, then the command's own inline skeleton — taking the first readable, non-empty layer, with no single path hard-coded (FR-039). Report the resolved path in the session (FR-041). Honour the resolved sections and their order; note rather than reinstate an omitted section (FR-040). Strip guidance comments and `[PLACEHOLDER]` tokens whichever layer supplied it.
- [X] T012 [P] Create `spectra/templates/test-strategy-template.md` declaring the ten sections from [contracts/document-contract.md](./contracts/document-contract.md) in order — classification and evidence; testable surfaces; unit testing; integration testing; API contract testing; end-to-end testing; coverage floor; recommendations summary; proposed constitution amendment; sources consulted and coverage of analysis — in the style of `spectra/templates/impact-analysis-template.md`. Section structure only: carry no honesty rule, no citation rule, and no floor arithmetic, all of which stay with the command (Principle VIII).
- [X] T013 Add the **lens boundary definitions** to `spectra/commands/test-strategy.md` per [research.md](./research.md) §3, defining each of the four lenses by what it proves and what it may assume rather than by a tool or a directory: unit (behaviour in isolation, collaborators substitutable, proves logic not wiring); integration (real components together, proves wiring, may not assume the network); API contract (shape and compatibility at a boundary someone else depends on, verified independently of either side, proves breaking vs non-breaking); end-to-end (one user-visible journey through the assembled system, proves it works and nothing about why it stopped). State that the document records, per project, which lens owns a given behaviour (FR-020).

**Checkpoint**: the prohibitions, the honesty rules, context reading, both resolutions, the shipped
template, and the lens vocabulary are all in place. User story work can begin.

---

## Phase 3: User Story 1 — Get a testing strategy before there is code to test (Priority: P1) 🎯 MVP

**Goal**: a greenfield project with a README, a manifest, and maybe a constitution gets a
project-specific strategy across all four lenses plus a floor, summarised in the session and written to
one file.

**Independent Test**: run in a repository with documentation and manifests but no substantial source;
verify every applicable lens has a concrete approach, every recommendation carries a citation or the
convention marker, and no tool is named that the declared stack cannot run.

- [X] T014 [US1] Add **Step 6 — Work the four lenses** to `spectra/commands/test-strategy.md`: for each of unit, integration, API contract, and end-to-end, produce either `applicable` with a named approach or `not-applicable` with a stated reason — never omitted (FR-014). Add any further lens the evidence warrants, justified from that evidence (FR-015). Record `proves` and `boundary` per lens from T013's definitions, and scope each lens to a surface or to `all` ([data-model.md](./data-model.md) §3).
- [X] T015 [US1] Add the **tool-tier rule** to `spectra/commands/test-strategy.md` per [research.md](./research.md) §9: tier 1 already present in a manifest, lockfile, or config, recommended freely with the manifest entry as evidence; tier 2 ecosystem-standard for a stack the project demonstrably uses, recommended with the stack evidence and marked as a convention; tier 3 anything else, recommended only with an explicit note that the command cannot verify the tool's current state and is offering it from frozen knowledge. State that a tool whose prerequisites the surface does not have appears at **no** tier (FR-016).
- [X] T016 [US1] Add the **end-to-end surface rule** to `spectra/commands/test-strategy.md`: the lens resolves to `browser`, `http`, `cli`, or `none`, matched to the project's real surface, and never defaults to a browser driver (FR-017). State that `none` is a valid and expected outcome for a library, and that a browser driver requires browser evidence in a manifest — which is what makes recommending one to a CLI unreachable rather than merely discouraged.
- [X] T017 [US1] Add the **evidence-or-convention rule** to `spectra/commands/test-strategy.md` as the per-recommendation obligation ([data-model.md](./data-model.md) §5): every recommendation carries either a project-relative citation or the explicit convention marker, and `evidence: convention` is the honest state for most greenfield recommendations rather than a defect (FR-043). An absence claim cites what was searched and where (FR-044).
- [X] T018 [US1] Add the **greenfield floor** rules to `spectra/commands/test-strategy.md` per [research.md](./research.md) §5: with no code there is no baseline, so the floor is a convention, explicitly marked unevidenced, and framed as *hold from the first commit* rather than *reach eventually* — the one thing a greenfield project can do that a brownfield one cannot. State the metric and how it would be measured on this project (FR-021).
- [X] T019 [US1] Add **Step 9 — Write the document** to `spectra/commands/test-strategy.md`: write exactly one file to the resolved target, as the run's final act, with the front matter fields from [data-model.md](./data-model.md) §8 (`mode`, `generated` with time of day, `surfaces`, `template`, `coverage_of_analysis`, `amendment`) and the body sections from the resolved template (FR-037, FR-042). State that the mode and its deciding signals always appear (FR-045).
- [X] T020 [US1] Add **Step 10 — Report** to `spectra/commands/test-strategy.md` per [contracts/chat-output.md](./contracts/chat-output.md) steps 5 and 6: the document path, the resolved template path, the coverage-of-analysis statement, the mode with its deciding signals, then a per-lens summary of the recommendations including the floor, its baseline, and the baseline's provenance. State that this happens **before** the user is asked anything about the constitution (FR-028), and that the session gets the summary while the document gets the detail.

**Checkpoint**: a greenfield project produces a complete, grounded, evidence-marked strategy document
and a session summary. This is the MVP.

---

## Phase 4: User Story 2 — Get a strategy that starts from what the code already does (Priority: P1)

**Goal**: a brownfield project's strategy opens with what is true today, cites it, and proposes a floor
the project can actually hold.

**Independent Test**: run in a repository with existing tests and a committed coverage report showing
31%; verify the document reports current state per lens with citations, the proposed floor is ≤ 31%,
and the ratchet has stated triggers.

- [X] T021 [US2] Extend **Step 1** in `spectra/commands/test-strategy.md` with the brownfield reading obligation: read source code to establish what is tested and what is not, and never derive the current state from documentation alone (FR-010). Cite paths for untested areas, and where the claim is that something is missing, cite what was searched and where (FR-044).
- [X] T022 [US2] Extend **Step 6** in `spectra/commands/test-strategy.md` so each lens in brownfield reports its `current` state with cited evidence **before** proposing an approach, and state that a lens which proposes before reporting is malformed (FR-018).
- [X] T023 [US2] Add the **tool-replacement rule** to `spectra/commands/test-strategy.md`: recommendations build on the frameworks already in use, and any proposal to replace one states the reason and the migration cost rather than simply naming a preferred tool (FR-019).
- [X] T024 [US2] Add **Step 7 — Establish the coverage baseline** to `spectra/commands/test-strategy.md` per [research.md](./research.md) §2, with the three provenances: `measured` only where the command ran the project's coverage tool after an explicit confirmation; `reported` where a figure was read from a committed report or badge, **always with its date**; `unavailable` where no tooling is configured and no report exists (FR-023, FR-026). State that a figure read from a file is `reported`, always — never `measured`.
- [X] T025 [US2] Add the **coverage-run confirmation** to `spectra/commands/test-strategy.md` per [contracts/chat-output.md](./contracts/chat-output.md) step 2: one declinable question that names the exact command it would run and warns that it executes the project's test suite. Declined, unanswered, or non-interactive: continue on `reported` or `unavailable` and say which. State that the command runs **nothing** by default.
- [X] T026 [US2] Add **Step 8 — Derive the floor and the ratchet** to `spectra/commands/test-strategy.md` per [research.md](./research.md) §5: with a baseline, the floor is the baseline rounded **down** to a stated granularity, and the rounding is stated; without one, the floor is `conditional` on the tooling recommended as step one and **no number is asserted** (FR-023). State the invariant plainly — **in brownfield or mixed mode the floor never exceeds the baseline** (FR-022) — and say why: a floor that fails the next build gets deleted, which is worse than proposing none.
- [X] T027 [US2] Add the **ratchet** rules to `spectra/commands/test-strategy.md`: trigger-and-step pairs, never dates — for example, when the floor has held for N consecutive merges raise it by M points, and when a surface's baseline exceeds the floor by more than M raise the floor to the baseline. State the target; do not state a schedule (FR-024). Explain in one line that the command cannot know a team's cadence and a dated plan is stale on arrival.
- [X] T028 [US2] Add the **floor disclaimer and enforcement statement** to `spectra/commands/test-strategy.md`: state what the floor does and does not prove so it is not read as a quality guarantee (FR-025), and give the exact configuration change the team would make to enforce it — stated, never applied (FR-047).
- [X] T029 [US2] Add the **coverage-of-analysis statement** rules to `spectra/commands/test-strategy.md`: what portion of the repository was read out of what is present, and what could not be seen; and where search capability was reduced, say so rather than narrowing silently (FR-013).

**Checkpoint**: a brownfield project gets a strategy grounded in its current state with a floor it can
hold on the next build.

---

## Phase 5: User Story 3 — Decide whether the strategy becomes policy (Priority: P1)

**Goal**: the constitution is checked, the amendment is drafted and shown, approval is taken, and the
handoff is named — with the constitution itself never written.

**Independent Test**: run in a project whose constitution has no testing principle; hash the
constitution, decline, re-hash — identical; run again and approve, re-hash — **still identical**, with
the amendment text in the document and the handoff named.

- [X] T030 [US3] Add **Step 11 — Check the constitution** to `spectra/commands/test-strategy.md` per [contracts/amendment-handoff.md](./contracts/amendment-handoff.md), with the three states from [research.md](./research.md) §6: `embedded` (a principle or standards section states normative testing obligations covering the strategy's core claims — quote the governing clause, draft nothing); `partial` (obligations exist but omit or contradict part of the strategy — quote what exists, draft scoped to the gap); `absent` (no normative testing obligation anywhere — draft a new principle). State that the read is semantic — section heading plus normative keywords plus subject matter — and **never** a string match on the word "test" (FR-029).
- [X] T031 [US3] Add the **no-constitution** branch to `spectra/commands/test-strategy.md`: report that there is nothing to amend, name `/speckit-constitution` as the way to create one, create nothing, and offer no gate (FR-030).
- [X] T032 [US3] Add the **conflict rule** to `spectra/commands/test-strategy.md`: where an existing principle contradicts a recommendation — a mandated 90% floor in a repository measuring 31% is the worked example — surface the contradiction as a finding in its own right, and draft no amendment that silently overrides the existing principle (FR-033).
- [X] T033 [US3] Add the **amendment draft shape** to `spectra/commands/test-strategy.md`, reusing `domain-analyzer`'s handoff format so `/speckit-constitution` consumes one format and not two ([research.md](./research.md) §7): an unchecked checkbox line carrying the statement in the constitution's voice with MUST/SHOULD and a brief rationale, plus `section:` naming the target and `status:` of `add` or `amends: <principle name>` (FR-032b).
- [X] T034 [US3] Add **Step 12 — The amendment gate** to `spectra/commands/test-strategy.md` per [contracts/amendment-handoff.md](./contracts/amendment-handoff.md): show the exact amendment text **before** the user chooses, then offer three paths — approve, modify, discuss (FR-031). Approve records the draft in the document's proposed-amendment section and names the handoff. Modify revises the document in place, re-summarises, and re-offers the same gate (FR-035). Discuss records nothing until one of the other two is taken. Declined or unanswered records nothing.
- [X] T035 [US3] Add the **never-write invariant** to `spectra/commands/test-strategy.md` as a standalone, unmissable statement: this command never writes `.specify/memory/constitution.md` — not on approval, not on a re-run, not when the file is missing, not when the user insists. Approval authorises a paragraph in a document the command was already writing, and nothing else (FR-032). State that `/speckit-constitution` owns the sync impact report, the bump-type judgement, the version lines, and dependent-artifact propagation.
- [X] T036 [US3] Add the **handoff sentence** rules to `spectra/commands/test-strategy.md`: tell the user to run `/speckit-constitution` referencing the strategy document; do **not** invoke it (FR-032a). Give the two reasons in one line each — an agent-agnostic prompt cannot portably invoke another command (Principle III), and chaining would remove the user from their own governance change at the moment they should be looking at it.
- [X] T037 [US3] Add the **template-omission fallback** to `spectra/commands/test-strategy.md`: where the resolved template omits the proposed-amendment section, note the omission, give the amendment text in the session, and still offer the handoff — honour, do not repair (FR-036).
- [X] T038 [US3] Add the **Non-interactive mode** section to `spectra/commands/test-strategy.md`: detect the condition, announce it once up front, attempt no coverage run, write the document, draft the amendment, record it as `not-asked`, and infer no approval (FR-034). Also add the **document-not-writable** branch: report the failure, output the strategy in the session, write nowhere else, and do not proceed to a gate about a document that was never written.

**Checkpoint**: the gate works in both directions and the constitution is provably untouched either
way.

---

## Phase 6: User Story 4 — Re-run it when the project changes (Priority: P2)

**Goal**: a second run treats the prior strategy as a starting point, reports what changed, and leaves
exactly one file behind.

**Independent Test**: run twice with a project change in between; verify one file at one path, the
prior strategy named as an input, an implemented recommendation marked adopted rather than re-proposed,
and a statement of what changed.

- [X] T039 [US4] Add the **re-run semantics** to `spectra/commands/test-strategy.md`: rewrite the same file in place; never create a second strategy file; no sequence number, no supersede marker, no index; and state what changed since the version replaced (FR-037). Note in one line that Git carries the history a filename would otherwise carry.
- [X] T040 [US4] Add the **adoption states** to `spectra/commands/test-strategy.md` per [data-model.md](./data-model.md) §5: a recommendation is `new`, `adopted` (the project has since implemented it — reported, not re-proposed), or `carried` (still outstanding) (FR-012).
- [X] T041 [US4] Add the **baseline movement** rule to `spectra/commands/test-strategy.md`: where the coverage baseline has moved since the prior run, state both figures and whether the ratchet advanced.
- [X] T042 [US4] Add the **user-directed change** rule to `spectra/commands/test-strategy.md`: where the user directs a change that contradicts the evidence, make the change as instructed and record the disagreement in the document rather than arguing in the session (FR-046).

**Checkpoint**: the strategy is refreshable without accumulating files or losing decisions.

---

## Phase 7: User Story 5 — Run it on a project with more than one stack (Priority: P3)

**Goal**: a monorepo gets per-surface lens treatment and per-surface floors inside one document.

**Independent Test**: run in a repository with two distinct stacks; verify each surface has its own
approach and floor and that no recommendation is applied across a surface it does not fit.

- [X] T043 [US5] Extend **Step 6** in `spectra/commands/test-strategy.md` so lenses are treated per surface wherever the surfaces differ, with a shared treatment only for what genuinely applies repository-wide.
- [X] T044 [US5] Extend **Step 8** in `spectra/commands/test-strategy.md` so each surface with its own baseline carries its own floor, rather than one repository-wide number (FR-027).
- [X] T045 [US5] Add the **recommendation scope** rule to `spectra/commands/test-strategy.md`: a recommendation names the surface it applies to, and one that applies to a single surface is never presented as repository-wide policy.

**Checkpoint**: all five stories are functional.

---

## Phase 8: Document Assembly

**Purpose**: the two sections that can only be written once every other section exists.

- [X] T046 Add the **Known limitations, stated in every document** section to `spectra/commands/test-strategy.md`: no tool recommendation was verified against a registry because no network request was made (FR-050, [research.md](./research.md) §9); a `reported` baseline is as old as its report; the classification is a reported judgement with its evidence, not a guarantee; and this command decides policy while the roadmap's `test-coverage` and `test-automation` agents would execute against it (FR-049).
- [X] T047 Add the **Inline template skeleton** section to `spectra/commands/test-strategy.md` (depends on T012 and every section above): a fenced block declaring exactly the ten H2 headings of `spectra/templates/test-strategy-template.md`, **in the same order**. `tests/test_document_templates.py` strips trailing `<!-- … -->` annotations and asserts the two heading lists are equal and ordered, so a divergence here fails the suite.
- [X] T048 Read `spectra/commands/test-strategy.md` end to end against [contracts/command-interface.md](./contracts/command-interface.md) and confirm every row of its refusals-and-degradations table is stated somewhere in the file: empty repository, no text search, unusable declared root, publication signal, no coverage tooling, stale report, tests present but not executing, no constitution, principle conflict, template omission, document not writable, non-interactive, and user-directed contradiction.

**Checkpoint**: the runtime deliverable is complete and internally consistent.

---

## Phase 9: Publishing Surface (Principle V)

**Purpose**: make the command real to a consumer. These touch different files and are the only
genuinely parallel work in the plan — except where a task reads another's output.

- [X] T049 [P] Register both artifacts in `spectra/extension.yml`: add `speckit.spectra.test-strategy` → `commands/test-strategy.md` to `provides.commands` with a description naming the artifact folder, the foundation-phase position, and the fact that it never edits the constitution; add `test-strategy-template` → `templates/test-strategy-template.md` to `provides.templates` with the override path in its description, in the style of the five entries already there; bump `extension.version` 1.12.1 → **1.13.0**; add the tags `test-strategy` and `coverage` (FR-001, FR-051).
- [X] T050 [P] Add a `[1.13.0]` entry to `spectra/CHANGELOG.md` recording the new command and registered template, and the three decisions a reader would otherwise find surprising: the strategy is a **singleton** rewritten in place with no sequence number; the command **never writes the constitution** and hands an approved amendment to `/speckit-constitution`; and it **runs nothing** unless the user confirms a coverage run.
- [X] T051 [P] Add the roster entry to `agents-list.json`: `id: test-strategy`, `title: Test Strategy`, a one-line description, `status: available`, `phase: foundation`, `type: add-on`, `provider: spectra`, `command: speckit.spectra.test-strategy` — matching the shape of the `domain-analyzer` entry. A `command` key is required exactly because the status is `available`. `tests/test_roster_data.py` also asserts titles are unique, so confirm `Test Strategy` collides with none of the 47 existing titles — note that `Testing`, `Test Coverage Analyst`, and `Test Automation Analyst` already exist (FR-005).
- [X] T052 Regenerate every structured listing with `python3 tools/generate_agent_docs.py` (depends on T049, T051): the Agents table in `README.md`, the Spec Kit core and Roadmap sections of `AGENTS_LIST.md`, and the Commands table in `spectra/README.md`. Do not hand-edit anything between the `SPECTRA:GENERATED` markers (FR-052, Principle V).
- [X] T053 Hand-author the prose block in `AGENTS_LIST.md` anchored `<!-- SPECTRA:AGENT id=test-strategy -->` (depends on T051), in the style of the seven blocks already there: what it does, what it will not do — the constitution above all — how greenfield and brownfield differ, where it writes, and what the user is expected to do with the amendment. Automation guarantees the block exists, never what it says (FR-052).
- [X] T054 [P] Add the command to `docs/index.html` in the commands list, with an example invocation matching the seven entries already there. Do not hard-code the version or the description — the page reads those from `catalog.json` and `agents-list.json` at load (Principle V).
- [X] T055 Update the `spectra` entry in `catalog.json` (depends on T049): `version` → 1.13.0, `provides.commands` 7 → **8**, both `updated_at` fields, and the two new tags — the values must match `spectra/extension.yml` exactly or CI's drift job fails.
- [X] T056 Rebuild the package with `python3 tools/build_package.py` (depends on T012, T049, and the finished command file) and confirm `docs/packages/spectra.zip` contains `spectra/commands/test-strategy.md` and `spectra/templates/test-strategy-template.md` under a single top-level `spectra/` folder.
- [X] T057 [P] Add the manual pass rows to `test/README.md` covering the three things only a human can confirm: approving the amendment leaves the constitution byte-identical, a brownfield floor lands at or below the baseline, and a template override drops a section without the command reinstating it.

**Checkpoint**: a consumer running `spectra install` would get the command, and every published surface
agrees with the extension folder.

---

## Phase 10: Validation

**Purpose**: prove the rules survived contact with the file, and that an agent actually follows them.

- [X] T058 [P] Create `tests/test_test_strategy_flow.py` in the style of `tests/test_impact_flow.py`, asserting on the text of `spectra/commands/test-strategy.md`: the constitution write ban stated unconditionally (**SC-005**); the floor-never-exceeds-baseline rule (**SC-003**); the three baseline provenances with `reported` requiring a date; the evidence-or-convention rule with no third option (**SC-002**); the three tool tiers and the no-tier rule for an unsupported stack (**SC-004**); the end-to-end surface set with no default browser driver; the four mandatory lenses each requiring applicable-or-reason; the mode declaration and the coverage-of-analysis statement (**SC-006**); the in-place re-run with no second file (**SC-008**); the `/speckit-constitution` handoff named as a user action rather than an invocation; and the absence of any network, URL, or credential instruction.
- [X] T059 [P] Add `"test-strategy.md": "docs/test-strategy/"` to `CANONICAL` in `tests/test_doc_output_paths.py`. This is what puts the command into `DOCUMENT_COMMANDS` and so inherits the declared-root, publication-signal, `never write it`, lowercase-slug, and no-absolute-path assertions. Verified during planning: the slug regex reads the **folder** segment, so `docs/test-strategy/TEST_STRATEGY.md` yields `test-strategy` and passes, and the `NNN` write-target assertions are per-command for `adr` and `brd` rather than generic — nothing inherits a numbering requirement.
- [X] T060 [P] Add the write-target assertion to `tests/test_doc_output_paths.py` in the style of the two already there, asserting `docs/test-strategy/TEST_STRATEGY.md` appears in the command — and add an assertion that **no sequence-number pattern** accompanies it, so FR-042a's deliberate Principle VII deviation is pinned rather than able to drift back either way.
- [X] T061 [P] Add `"test-strategy.md": "test-strategy-template"` to `COMMAND_TEMPLATE` in `tests/test_document_templates.py`, which asserts registration both ways, heading parity between the shipped template and the command's inline skeleton, all resolution layers present in the command, and no hard-coded template path.
- [X] T062 [P] Update the census in `tests/test_roster_data.py`: 47 → **48** agents and 16 → **17** available in `test_it_carries_the_full_published_roster` and `test_it_splits_into_sixteen_available_and_thirty_one_planned` (rename that method to `..._seventeen_available_...`); **31** planned and **9** from Spec Kit unchanged; and add `"test-strategy"` to the hardcoded id list in `test_spectra_ships_exactly_seven_agents_today`, renaming it to `test_spectra_ships_exactly_eight_agents_today`. That method's list is sorted, so `test-strategy` goes last.
- [X] T063 Run the full gate from the repository root (depends on T049–T062): `python3 -m unittest discover -s tests` green, `python3 tools/generate_agent_docs.py --check` reporting **48 agents and 8 prose blocks** with roster and manifest agreeing, and `python3 tools/build_package.py && git diff --stat docs/packages/spectra.zip` showing no drift.
- [X] T064 Install the working copy into a throwaway Spec Kit project with `specify extension add --dev` per [quickstart.md](./quickstart.md), and run Passes B1 through B11, recording the observed result for each. These passes are where the observable success criteria are actually measured: **SC-001** (one invocation, no arguments), **SC-002** (zero unmarked recommendations), **SC-003** (floor ≤ baseline), **SC-004** (no unusable tool, across at least four stacks including one with no browser), **SC-005** (constitution byte-identical after approval), **SC-006** (mode and coverage legible from the document alone), **SC-007** (override honoured), **SC-008** (re-run reports adopted, one file), **SC-009** (one named command applies the amendment).
  > **Partially executed 2026-09-10.** A throwaway Spec Kit project was created with
  > `specify init --here --force --non-interactive --integration claude` and the working copy installed
  > with `specify extension add --dev`. Registration verified: **8 commands and 6 templates** at the
  > extension layer, and `speckit-spectra-test-strategy` registered as a skill.
  >
  > A brownfield probe was then built — a Python CLI (`click`, `httpx`, `pytest-cov`) with three
  > modules, one test covering one function, a committed `coverage.xml` at `line-rate="0.31"` dated
  > 2026-01-15, a CI workflow running `pytest` but not coverage, and a constitution with two principles
  > and no testing obligation. The command's steps were then followed against it and the document
  > produced. **15 of 15 assertions on the output passed**, covering Passes B2, B4, B8, and the
  > singleton rule: floor **30% ≤ baseline 31%** with the rounding stated; baseline labelled `REPORTED`
  > with its date and nothing claimed as `measured`; ratchet expressed as triggers with no dates; the
  > end-to-end lens resolved to **CLI** with no browser driver named anywhere; one file at
  > `docs/test-strategy/TEST_STRATEGY.md` with no sequence number; section list identical to the
  > resolved template in order with guidance comments and placeholders stripped; all six summary
  > recommendations carrying a citation or a convention marker; four absence claims each citing what was
  > searched; and the coverage and no-network statements present.
  >
  > **Pass B5 (SC-005) passed on the run that matters**: the probe constitution hashed `281d5b36` before
  > the run and `281d5b36` after a run in which the amendment was **approved**. The amendment text is in
  > the document's proposed-amendment section with the `/speckit-constitution` handoff named.
  >
  > **Passes B9 and B8 verified by resolution**: an override at
  > `.specify/templates/overrides/test-strategy-template.md` with *Coverage floor* deleted resolves
  > ahead of the extension copy and yields 9 sections; adding `Artifact root: documents/` to the probe
  > constitution resolves the write target to `documents/test-strategy/TEST_STRATEGY.md`.
  >
  > **Not executed: Passes B1, B3, B6, B7, B10, and B11 as live agent runs** — a greenfield probe, the
  > no-tooling baseline, the embedded/partial/conflicting constitution variants, the re-run, the
  > non-interactive session, and the empty repository. Each needs an interactive agent session with the
  > command registered and the agent restarted, which cannot be driven from inside the session that
  > authored the command. **SC-004 is only partially measured**: one stack (a Python CLI with no browser)
  > rather than the four the criterion asks for.

- [X] T065 Run Pass B5 in this repository itself, which has `docs/index.html` and Pages serving `main` `/docs`: confirm the publication check fires and the choice is surfaced rather than silently defaulting to `docs/test-strategy/`. Then repeat Passes B2, B4, and B5 on a second agent — the floor cap, the browser-driver refusal, and the constitution invariant — because those three are where a prompt-expressed rule is most likely to be quietly ignored by a different model. Record the results in the `test/README.md` rows added by T057.
  > **Half executed 2026-09-10.** The publication-signal half is confirmed structurally in this
  > repository: both `docs/index.html` and `docs/.nojekyll` are present, so the Step 4 check fires here
  > and a run cannot silently default into the published folder. The command was **not** run against
  > this repository to completion, because doing so would write a strategy document into the deliverable
  > itself.
  >
  > **The second-agent repeat of Passes B2, B4, and B5 was not executed.** It needs a different model in
  > an interactive session with the extension installed, which this session cannot provide. This is the
  > one deferred item that matters most: those three rules are prompt-expressed, and a second model
  > ignoring them is exactly the failure `tests/test_test_strategy_flow.py` cannot catch. The manual-pass
  > rows added by T057 are where the result belongs when it is run.


**Checkpoint**: the rules are asserted in the suite, and an agent has been observed following them.

---

## Phase 11: Publish (Constitution Development Workflow step 6)

- [X] T066 Verify the two facts CI will check before pushing: `spectra/extension.yml` and `catalog.json` agree on **1.13.0** and **8** commands, and the committed zip matches the `spectra/` folder.
- [X] T067 Commit the whole set on branch `020-test-strategy-agent`: `spectra/`, `specs/020-test-strategy-agent/`, `agents-list.json`, `catalog.json`, `docs/`, `README.md`, `AGENTS_LIST.md`, `test/README.md`, and `tests/`.
  > **Done 2026-09-10** as commit `51039e8` on branch `020-test-strategy-agent` — 27 files, 3599
  > insertions, 11 deletions. Pushed with `-u`; working tree clean.
- [X] T068 Open the pull request for branch `020-test-strategy-agent` with `speckit.spectra.create-pr` — the extension's own `after_implement` hook — and confirm the body states the 1.13.0 bump, the new `spectra/commands/test-strategy.md` and `spectra/templates/test-strategy-template.md`, the three decisions from T050, and the Principle VII numbering deviation with a pointer to the Complexity Tracking entry that justifies it.
  > **Done 2026-09-10** — **[PR #28](https://github.com/telus-digital/spectra/pull/28)** opened
  > against `main` (27 files, +3599/-11). Composed from the resolved `pr-template.md` following
  > `speckit.spectra.create-pr`'s own steps: gated on `gh` first, repository facts read in one
  > `gh repo view` call, no duplicate PR for the head, base taken from the constitution's
  > documented flow (a spec branch merges back to `main`) which agrees with `defaultBranchRef`,
  > and the Related Issues section deleted rather than filled with a placeholder since no issue
  > was passed. The body states the 1.12.1 → 1.13.0 bump, both new files, the three decisions
  > from T050, and the Principle VII numbering deviation with its Complexity Tracking
  > justification — plus the two deferred validation items and the partial SC-004 measurement,
  > recorded as deferred rather than as done.

---

## Dependencies & Execution Order

### Phase dependencies

- **Phase 1 (Setup)**: no dependencies.
- **Phase 2 (Foundational)**: depends on Phase 1. **Blocks every user story.** T012 is the only
  parallel task; the rest edit one file in sequence.
- **Phases 3–7 (User stories)**: all depend on Phase 2. They edit the same file, so they run in
  priority order rather than in parallel — see below.
- **Phase 8 (Assembly)**: depends on Phases 3–7 and on T012. T047 cannot be written before every
  section exists and the shipped template is final.
- **Phase 9 (Publishing)**: depends on Phase 8 for T056; T049, T050, T051, T054, and T057 can start
  once the command file's identity is fixed at T002.
- **Phase 10 (Validation)**: T058–T062 depend on the finished command file and the Phase 9 registry
  entries. T063 depends on all of them. T064 and T065 depend on T056.
- **Phase 11 (Publish)**: depends on Phase 10.

### User story dependencies

- **US1 (P1)** — the MVP. Depends only on Phase 2. Delivers a complete greenfield strategy.
- **US2 (P1)** — depends on Phase 2. Extends Steps 1 and 6 that US1 created, so it follows US1 in the
  same file even though it is independently testable.
- **US3 (P1)** — depends on Phase 2 and on US1's Step 10 report, which the gate follows.
- **US4 (P2)** — depends on US1 and US2; adoption states need recommendations and a baseline to exist.
- **US5 (P3)** — depends on US1's Step 6 and US2's Step 8, both of which it extends per surface.

Each story remains **independently testable** — the quickstart passes B1, B2, B5, B7, and B4/B8 verify
one story each — but they are not independently *implementable*, because they are sections of one file.

### Within each phase

Tasks edit `spectra/commands/test-strategy.md` in sequence unless marked [P]. Two exceptions: T012
creates the template and T057 edits `test/README.md`.

### Parallel opportunities

- **Phase 2**: T012 runs alongside T005–T011.
- **Phase 9**: T049, T050, T051, T054, and T057 are five different files and run together. T052, T053,
  T055, and T056 read their output and follow.
- **Phase 10**: T058, T059, T060, T061, and T062 are four different files (T059 and T060 share one, so
  they serialize with each other) and otherwise run together.

---

## Parallel Example: Phase 9

```bash
# Five different files, no shared state — run together:
Task: "Register both artifacts and bump to 1.13.0 in spectra/extension.yml"
Task: "Add the [1.13.0] entry to spectra/CHANGELOG.md"
Task: "Add the test-strategy roster entry to agents-list.json"
Task: "Add the command entry to docs/index.html"
Task: "Add the manual pass rows to test/README.md"

# Then, reading their output:
Task: "Regenerate the structured listings with tools/generate_agent_docs.py"
Task: "Update the spectra entry in catalog.json to 1.13.0 / 8 commands"
Task: "Rebuild docs/packages/spectra.zip"
```

---

## Implementation Strategy

### MVP first (US1 only)

1. Complete Phase 1: Setup (T001–T004).
2. Complete Phase 2: Foundational (T005–T013) — **critical, blocks everything**.
3. Complete Phase 3: User Story 1 (T014–T020).
4. **STOP and VALIDATE**: run quickstart Pass B1 in a greenfield scratch project. A strategy document
   with all four lenses, zero unmarked recommendations, and no unusable tool is a shippable increment
   on its own.

### Incremental delivery

1. Setup + Foundational → the file exists with its rules and both resolutions.
2. **+ US1** → greenfield strategies work. Validate with B1 and B4. *(MVP)*
3. **+ US2** → brownfield strategies work. Validate with B2, B3.
4. **+ US3** → the constitution gate works. Validate with B5, B6 — and B5 is the one that matters
   most, because it proves the invariant the whole Q2 decision rests on.
5. **+ US4** → re-runs work. Validate with B7.
6. **+ US5** → monorepos work.
7. Assembly, publishing, validation, publish.

### Parallel team strategy

Limited by design: one Markdown file is the deliverable, so the user-story phases do not parallelize.
Where a second person helps is Phase 9 and Phase 10 — one person finishes the command file while
another prepares the publishing surface (T049, T050, T051, T054, T057) and the test modules
(T058–T062), both of which can be written against the contracts before the command file is final.

---

## Notes

- [P] = different file, no dependency on an incomplete task.
- Every task cites the requirements it implements, so a reviewer can check coverage against
  [spec.md](./spec.md) without re-deriving the mapping.
- The command file is prose. The suite is what stops it drifting — which is why T058–T062 are not
  optional and why T060 exists specifically to pin the one deliberate constitutional deviation.
- Commit after each phase or logical group; stop at any checkpoint to validate.
- Do not hand-edit anything between `SPECTRA:GENERATED` markers, and do not hand-edit the zip.
