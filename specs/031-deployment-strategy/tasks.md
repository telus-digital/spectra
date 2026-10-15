---

description: "Task list for the Deployment Strategist agent"
---

# Tasks: Deployment Strategist Agent

**Input**: Design documents from `/specs/031-deployment-strategy/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Requested — FR-053 requires standard-library `unittest` coverage. A command file is a prompt,
so tests assert the shipped text carries each rule (the pattern of `tests/test_test_strategy_flow.py`
and `tests/test_domain_analyzer_flow.py`). Write each story's tests first and confirm they fail.

**Organization**: by user story. Most story work edits the same command file,
`spectra/commands/deployment-strategy.md`, so tasks touching it are sequential; tests and other files
are marked [P] where they are independent.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1–US6, from spec.md

---

## Phase 1: Setup (Governance prerequisite)

**Purpose**: the constitution must name the singleton before a command may write one (Principle VII).

- [X] T001 Amend Principle VII in `.specify/memory/constitution.md`: add `<artifact-root>/DEPLOYMENT_STRATEGY.md` (`speckit.spectra.deployment-strategy`) as the third shipped singleton in the "standing-policy artifact" paragraph ("The three shipped singletons are …"); add no earlier location to the read-report-leave-alone list; bump version 1.9.0 → 1.10.0 and Last Amended to 2026-10-15; replace the SYNC IMPACT REPORT with one for 1.9.0 → 1.10.0 (MINOR, materially expanded guidance in VII; templates unaffected; dependent files listed per research R6/R9)
- [X] T002 [P] Change `SINGLETON` in `tests/test_doc_output_paths.py` to allow an earlier location of `None`, update the comment above it, make `test_*earlier*` skip `None` entries, and add `"deployment-strategy.md": ("docs/DEPLOYMENT_STRATEGY.md", None)` (research R6)

---

## Phase 2: Foundational (Blocking prerequisites)

**Purpose**: the command file, its template, and their registration exist, so every story has a file
to extend and the suite can find it.

- [X] T003 Create `spectra/commands/deployment-strategy.md` with YAML front matter whose quoted `description` states everything listed in `contracts/command-interface.md` § Front-matter `description`; a title and opening role paragraph ("You are the **Deployment Strategist**…"); "The one rule that governs everything" ("Read this project, propose a deployment strategy it can actually hold, write exactly one file inside it — and never edit the constitution, no matter who approves."); and a "User Input" section with `$ARGUMENTS`, no-arguments behaviour, the focus hint, local document references, URLs never fetched, the single flag `--non-interactive`, and unrecognised flags reported and ignored (FR-001, FR-003, FR-005)
- [X] T004 Add "What this command never does" to `spectra/commands/deployment-strategy.md` as a table carrying every row of `contracts/command-interface.md` § Never-list, each with its reason (FR-007, FR-019, FR-023, FR-024, FR-031, FR-034, FR-047, FR-048, FR-049)
- [X] T005 [P] Create `spectra/templates/deployment-strategy-template.md` with the twelve sections of `contracts/document-contract.md` § Sections, in that order, each with a guidance comment and `[PLACEHOLDER]` tokens; the environments section shows the table columns (environment, proves, audience, deploy method, gate in) and a Mermaid placeholder; the open-questions section shows columns (item, who answers, blocks); no rule text (rules stay in the command, FR-038)
- [X] T006 Register in `spectra/extension.yml`: a `provides.commands` entry `speckit.spectra.deployment-strategy` → `commands/deployment-strategy.md` with a description matching the command's front matter, and a `provides.templates` entry `deployment-strategy-template` → `templates/deployment-strategy-template.md` whose description names the override path `.specify/templates/overrides/deployment-strategy-template.md` and lists the rules that stay with the command (four provenances, never-guess open questions, high-level operability, no secret, diagram bound to table)
- [X] T007 [P] Add `"deployment-strategy.md": "deployment-strategy-template"` to the command→template map in `tests/test_document_templates.py`
- [X] T008 [P] Create `tests/test_deployment_strategy_flow.py` (module docstring in the style of `tests/test_domain_analyzer_flow.py`; `COMMAND`, `TEMPLATE`, `MANIFEST` paths via `helpers`; a `flat()` helper) with a registration class: file exists, manifest registers command and template, front matter has a description, uses `$ARGUMENTS`, runs with no arguments, documents `--non-interactive`, reports unknown flags

**Checkpoint**: `python3 -m unittest tests.test_deployment_strategy_flow tests.test_document_templates` passes.

---

## Phase 3: User Story 1 — Evidence-grounded strategy (Priority: P1) 🎯 MVP

**Goal**: a run reads the project, classifies it, works six lenses with provenance, and writes one file.

**Independent Test**: quickstart scenario A — six lenses present, current state cited before
recommendations, one Mermaid diagram matching the environments table, coverage stated.

### Tests for User Story 1

- [X] T009 [P] [US1] Add to `tests/test_deployment_strategy_flow.py`: the six lens names appear and "never omit a lens"; "not applicable" requires a reason; brownfield reports current state before recommending; the four provenances `verified`, `claimed`, `stated`, `convention` are named with "exactly one"; an absence cites what was searched; an answer never overwrites a repository fact; open questions are never invented; coverage of analysis is stated; operability stays high level and alert definitions need an explicit request; secrets are never reproduced; the command "runs nothing"; no network request; the Mermaid diagram draws only what the table states; `TEST_STRATEGY.md` is cited for which tests exist and its absence is a gap naming `speckit.spectra.test-strategy`; app rollback does not roll back the database; drilled vs assumed

### Implementation for User Story 1

- [X] T010 [US1] Add "The rules that never bend" to `spectra/commands/deployment-strategy.md`: R1 four provenances, exactly one per claim (research R5); R2 absence cited with its search; R3 an answer is an input, never a measurement — conflicts recorded in the document, not argued in session; R4 never invent client/ops values, they go to open questions; R5 state your own coverage; R6 never reproduce a secret (research R12); R7 operability stays high level, deeper only on explicit request, still one file (research R10); state that these rules live in the command, not the template
- [X] T011 [US1] Add "The six lenses, defined" to `spectra/commands/deployment-strategy.md`: a table per lens of what it decides and its boundary (FR-014 to FR-019), plus the conditional lenses and their warranting rule (FR-020)
- [X] T012 [US1] Add "Step 1 — Read the project" to `spectra/commands/deployment-strategy.md`: the input list of FR-004 including `TEST_STRATEGY.md` and `DOMAIN_ANALYSIS.md` at the resolved root, record every input and every unreadable expected input with its reason, reduced-search fallback reported, prior document read as input
- [X] T013 [US1] Add "Step 2 — Classify what ships" to `spectra/commands/deployment-strategy.md`: the six classes with deciding signals and order of authority from research R1, workspaces authoritative, one deployable stated once, never asked; and greenfield/brownfield/mixed from deployment practice with dissenting signals (research R2, FR-010)
- [X] T014 [US1] Add "Step 3 — Resolve where the strategy will live" to `spectra/commands/deployment-strategy.md`, mirroring `spectra/commands/test-strategy.md` Step 4: target `<artifact-root>/DEPLOYMENT_STRATEGY.md`, declared `Artifact root:` line (project-relative, unusable → report and default), every publication signal (`mkdocs.yml`, `docusaurus.config.*`, `docs/_config.yml`, `docs/.nojekyll`, `docs/index.html`, `docs/conf.py`, Pages config), recommend `documents/`, non-publishing option when no choice, offer but never write the declaration, singleton rationale, and "no earlier location exists for this document; there is nothing to migrate" (FR-035, research R6)
- [X] T015 [US1] Add "Step 5 — Resolve the document's template" to `spectra/commands/deployment-strategy.md` with the five-layer stack naming `deployment-strategy-template`, honour-not-repair, strip guidance comments and `[PLACEHOLDER]`, report the path, and the do-not-edit-the-installed-copy note (FR-036, FR-037)
- [X] T016 [US1] Add "Step 6 — Work the lenses" to `spectra/commands/deployment-strategy.md`: applicable/not-applicable per lens per deployable; current state first in brownfield/mixed; exact change where possible; the Mermaid `flowchart LR` rule — nodes and gate labels only from the environments table, recommended environments dashed and labelled, no diagram when not applicable, one per deployable only where promotion differs (research R7); pipeline lens's `TEST_STRATEGY.md` rule and its no-test-strategy fallback (FR-015); data lens's rollback statement (FR-017); rollback lens's drilled-vs-assumed marking (FR-018); operability's list-and-link rule (FR-019)
- [X] T017 [US1] Add "Step 7 — Write the document" to `spectra/commands/deployment-strategy.md`: exactly one file as the final write; the four front-matter rules copied from `spectra/commands/test-strategy.md` Step 10; the example block from `contracts/document-contract.md` (keys `mode`, `generated`, `template`, `run`, `deployables` with `name`/`root`/`class`, `coverage_of_analysis`, `amendment_state`, `clarification`); enumerations exactly: `mode` "`greenfield` \| `brownfield` \| `mixed`", `class` "`service` \| `static-site` \| `library` \| `cli-desktop` \| `mobile` \| `infra`", `amendment_state` "`embedded` \| `partial` \| `absent` \| `none` \| `not_asked`", `disposition` "`answered` \| `default_taken` \| `not_asked`"; every question carried; write failure → output in session, write nowhere else, no gate (FR-039 to FR-041)
- [X] T018 [US1] Add "Step 8 — Report" to `spectra/commands/deployment-strategy.md` with the five report items in the order of `contracts/command-interface.md` § Session report, and "do not paste the document" (FR-043)
- [X] T019 [US1] Add "Known limitations, stated in every document" and the "Inline template skeleton" (the twelve sections of `contracts/document-contract.md` as headings with one-line comments) to the end of `spectra/commands/deployment-strategy.md` (FR-050)

**Checkpoint**: US1 tests pass; scenario A produces a complete document (amendment state may be `not_asked` until US3).

---

## Phase 4: User Story 2 — The five questions (Priority: P1)

**Goal**: one question per turn, each with a recommendation and evidence; all five recorded.

**Independent Test**: quickstart scenarios C and D.

### Tests for User Story 2

- [X] T020 [P] [US2] Add to `tests/test_deployment_strategy_flow.py`: the round is its own step after classification and root resolution; exactly five questions in order (platform, production approval, pre-release environment, availability and RPO/RTO, release cadence); announced once with "use your defaults"; one question per turn; "of 5" numbering; 2–4 options with exactly one recommended and its evidence or "convention"; free text valid; settled questions become confirmations keeping their number; asked once per project, never per deployable, with per-deployable free text; Q4 never recommends an invented number; defaults end the round; a non-answer re-asks; never-ask list (classification, stack, whether CI/manifests exist); non-interactive declared only and never inferred, all five `not_asked`; dispositions recorded in front matter and body

### Implementation for User Story 2

- [X] T021 [US2] Add "Step 4 — The clarification round" to `spectra/commands/deployment-strategy.md` (between Step 3 and Step 5): why it sits here; the never-ask table; the announcement text; the five-question table with each row's recommendation source and confirmation trigger from research R4; "once per project" with the per-deployable rule; Q4's open-question recommendation; the how-to-ask rules; confirm-don't-drop; the three early endings; record every question — all per `contracts/clarification-round.md` (FR-026 to FR-031)
- [X] T022 [US2] Add "Non-interactive mode" to `spectra/commands/deployment-strategy.md`, mirroring `spectra/commands/test-strategy.md`: two declarations only, never inferred, when in doubt ask, announce once, then ask none, take recommendations as `not_asked`, non-publishing root, write normally, amendment `not_asked`, report the amendment text (FR-032)

**Checkpoint**: US1 and US2 tests pass.

---

## Phase 5: User Story 3 — Constitution handoff (Priority: P1)

**Goal**: check the constitution, draft invariants only, gate, never write the constitution, end with
the link and the ready-to-paste line.

**Independent Test**: quickstart scenario H; constitution byte-identical after the run.

### Tests for User Story 3

- [X] T023 [P] [US3] Add to `tests/test_deployment_strategy_flow.py`: never writes `.specify/memory/constitution.md` and the ban is unconditional (approval, re-run, missing file, insistence); does not create a constitution; the four states `embedded`, `partial`, `absent`, `no constitution`; semantic check, not keyword match; contradictions surfaced as findings; draft items unchecked with `section:` and `status: add | amends:`; invariants only, no environment names/platform identifiers/cadences as obligations; the three gate paths; the handoff text contains `/speckit-constitution Adopt the checked items in the "Proposed constitution amendment" section of` and `[DEPLOYMENT_STRATEGY.md](docs/DEPLOYMENT_STRATEGY.md)`; "Do not invoke `/speckit-constitution` yourself"; the manifest description advertises the ban

### Implementation for User Story 3

- [X] T024 [US3] Add "Step 9 — Check the constitution" to `spectra/commands/deployment-strategy.md`: semantic reading (headings, normative keywords, subject matter; never a bare keyword), the four-state table from `contracts/amendment-handoff.md`, and contradictions as their own finding (FR-044, FR-046)
- [X] T025 [US3] Add "Step 10 — The amendment gate and handoff" to `spectra/commands/deployment-strategy.md`: the draft format block; the invariant catalogue from research R8 including the reference-the-document item; the rule that environment names, platform identifiers, cadences, and targets never appear as obligations; the three-path gate; declined/unanswered records nothing; the never-write invariant with its rationale; the handoff block exactly as in `contracts/amendment-handoff.md` with the resolved path, and "Do not invoke `/speckit-constitution` yourself" with the two reasons (FR-045, FR-047, FR-048)

**Checkpoint**: P1 stories complete — the MVP.

---

## Phase 6: User Story 4 — Documents outside the repository (Priority: P2)

**Goal**: referenced documents are read, cited as `claimed`, and can turn a question into a confirmation.

**Independent Test**: quickstart scenario E.

- [X] T026 [P] [US4] Add to `tests/test_deployment_strategy_flow.py`: referenced local documents are inputs; their claims are `claimed`; a claim confirmed in code becomes `verified`; URLs are never fetched and the command says so; an unreadable document is named with its reason; Spectra ships no parser
- [X] T027 [US4] Extend Step 1 and R1 in `spectra/commands/deployment-strategy.md` with the referenced-document rules of research R11 and the claimed→verified promotion of research R5; add to Step 4's recommendation sources that a referenced document can settle a question into a confirmation

---

## Phase 7: User Story 5 — Re-runs (Priority: P2)

**Goal**: same file rewritten; prior answers pre-filled; recommendations marked.

**Independent Test**: quickstart scenario I.

- [X] T028 [P] [US5] Add to `tests/test_deployment_strategy_flow.py`: rewrite in place, never a second file, no sequence number; prior document read first; questions pre-filled with "still true"; prior `not_asked` asked normally; marks `new`, `adopted`, `carried`; state what changed; user-directed contradictions recorded, not argued
- [X] T029 [US5] Add "Re-running on a project you have analysed before" to `spectra/commands/deployment-strategy.md`, mirroring `spectra/commands/test-strategy.md`, without the earlier-location and baseline bullets, with `run` incremented (FR-033, FR-042)

---

## Phase 8: User Story 6 — Non-service deployables (Priority: P3)

**Goal**: lenses adapt to the class; nothing recommends infrastructure the evidence lacks.

**Independent Test**: quickstart scenario B.

- [X] T030 [P] [US6] Add to `tests/test_deployment_strategy_flow.py`: the six classes are named; the adaptation table exists; for a library "deploy" means publish and environments are release channels; mobile store review is an uncontrolled gate; a deployable matching two classes is two deployables; no recommendation names infrastructure absent from the evidence
- [X] T031 [US6] Add the lens-adaptation table of research R3 to "The six lenses, defined" in `spectra/commands/deployment-strategy.md`, with the rule that each lens resolves its meaning against the deployable's class before reporting and that infrastructure absent from the evidence is never recommended (FR-011, SC-004)

---

## Phase 9: Polish & publishing (Principle V)

- [X] T032 [P] Add the reserved-map row `| a deployment strategy | \`<artifact-root>/\` | \`DEPLOYMENT_STRATEGY.md\` | \`deployment-strategy-template\` |` to `spectra/commands/kb-vault.md` beside the test-strategy and domain-analysis rows (research R9)
- [X] T033 [P] Add `"| \`<artifact-root>/\` | \`DEPLOYMENT_STRATEGY.md\` |"` to `RESERVED` in `tests/test_doc_output_paths.py`
- [X] T034 [P] Add the roster entry to `agents-list.json` in the `deployment-operations` agents, after `review-pr`: id `deployment-strategy`, title "Deployment Strategist", a one-sentence description, status `available`, phase `deployment-operations`, type `add-on`, provider `spectra`, command `speckit.spectra.deployment-strategy`
- [X] T035 [P] Add `"deployment-strategy"` to the shipped-agent census in `tests/test_roster_data.py` (alphabetical)
- [X] T036 Bump `spectra/extension.yml` `extension.version` 1.19.0 → 1.20.0 and add tags `deployment`, `deployment-strategy`, `release`, `operations`
- [X] T037 Update the `spectra` entry in `catalog.json`: version 1.20.0, `provides.commands` 11 → 12, the same four tags
- [X] T038 [P] Add a 1.20.0 entry to `spectra/CHANGELOG.md` in the house style: the new command, the template, the kb-vault reserved-map row, and the constitution 1.10.0 amendment
- [X] T039 [P] Write the `<!-- SPECTRA:AGENT id=deployment-strategy -->` prose block in `AGENTS_LIST.md` under the heading "Deployment Strategist", in the style of the test-strategy block: what it reads, the classification, the six lenses, the five questions, the output path, the handoff
- [X] T040 Run `python3 tools/generate_agent_docs.py` to regenerate `README.md`, `AGENTS_LIST.md`, and `spectra/README.md`, then `python3 tools/generate_agent_docs.py --check`
- [X] T041 [P] Add a command card for `speckit.spectra.deployment-strategy` to `docs/index.html` after the domain-analyzer card, in the existing `<span class="name">`/`<span class="cdesc">`/`<pre><code>` structure, invocation `/speckit-spectra-deployment-strategy`
- [X] T042 [P] Add `deployment-strategy-template` → `speckit.spectra.deployment-strategy` to the template table in `docs/e-learning/customization.html`
- [X] T043 [P] Add `<root>/DEPLOYMENT_STRATEGY.md` to the singleton list in `CONTRIBUTING.md`
- [X] T044 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip`
- [X] T045 Run `python3 -m unittest discover -s tests` and `python3 tools/ship.py --dry-run`; fix any failure
- [X] T046 Walk quickstart scenarios A–J in a throwaway project with `specify extension add --dev ./spectra` and record any gap as a follow-up

---

## Dependencies & Execution Order

- **Setup (T001–T002)** first: the constitution must name the singleton before T002's assertion passes.
- **Foundational (T003–T008)** blocks every story: the command file and registration must exist.
- **US1 (T009–T019)** before US2: Step 4 sits between Steps 3 and 5, which US1 writes.
- **US2, US3** sequential after US1 (same file). **US4–US6** each extend sections US1 wrote; any order
  after US1, sequential with each other because they share the command file.
- **Polish (T032–T046)**: T032–T035, T038, T039, T041–T043 in parallel at any point after Foundational;
  T040 after T034 and T039; T044 after every `spectra/` change; T045 after T044; T046 last.

## Parallel Examples

```text
Foundational:  T005 (template)  ‖  T007 (template map test)  ‖  T008 (test module)
Every story:   its test task [P] runs alongside the previous story's implementation
Polish:        T032 ‖ T033 ‖ T034 ‖ T035 ‖ T038 ‖ T039 ‖ T041 ‖ T042 ‖ T043
```

## Implementation Strategy

- **MVP** = Setup + Foundational + US1 + US2 + US3 (all P1): a complete, interactive, handed-off
  strategy for a service. Ship-ready once Polish runs.
- **Increment 2** = US4 + US5 (P2): referenced documents and re-runs.
- **Increment 3** = US6 (P3): non-service deployables. Because the catalog ships from `main`, all three
  increments land in the one 1.20.0 change; the increments order the work, not the release.

---

## Phase 10: Convergence

- [X] T047 Add a row (a deployment strategy → `<artifact-root>/DEPLOYMENT_STRATEGY.md` → `deployment-strategy-template`) after the domain-analysis row of the kb-vault reserved-map table in `spectra/README.md`, then rebuild `docs/packages/spectra.zip` with `python3 tools/build_package.py` per plan: research R9 / Constitution V (partial)
- [X] T048 Add "a deployment strategy" to the list of document kinds kb-vault adopts in the kb-vault prose block of `AGENTS_LIST.md` and in the kb-vault card of `docs/index.html` per plan: research R9 (partial)
- [X] T049 Update the `SingletonOutputPaths` docstring in `tests/test_doc_output_paths.py` to describe three singletons, one of which has no earlier location per plan: research R6 (partial)
