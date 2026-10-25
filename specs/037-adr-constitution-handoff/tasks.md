# Tasks: The ADR Agent Hands Off to the Constitution

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/handoff-behaviour.md](./contracts/handoff-behaviour.md),
[quickstart.md](./quickstart.md)

**Branch**: `037-adr-constitution-handoff`

**Tests**: requested. The plan and the behaviour contract pin every behaviour (A1–A19, G1–G4, M1–M3, D1–D4,
R1–R4) as a text assertion, in standard-library `unittest`. Within each story the test task comes first and
must fail before the command text it pins is written. Test files are abbreviated as follows:

| Code | File |
|---|---|
| `AD` | `tests/test_adr_flow.py` (new) |
| `EM` | `tests/test_methodology_flow.py` |
| `DA` | `tests/test_domain_analyzer_flow.py` |

**Format**: `- [ ] [ID] [P?] [Story] Description`. `[P]` means a different file, with no dependency on an
incomplete task.

Every `spectra/commands/*.md` edit keeps the file hard-wrapped at the width it already uses. Tests assert on
flattened text (lowercased, whitespace collapsed) where a rule may straddle a line break, using the same
`flat()` / `section()` helpers `EM` and `DA` already define.

---

## Phase 1: Setup (verify the premise)

- [X] T001 Confirm that the Evidence rows in `specs/037-adr-constitution-handoff/plan.md` still hold on this branch:
  - `spectra/commands/adr.md:191-207` (Step 7 edits the constitution) and `:209-222` (Step 8 stages it);
  - `spectra/commands/methodology.md:264-275` (sibling-ground table, "Four agents") and `:705-713` (ordered feeder list);
  - `spectra/commands/domain-analyzer.md:229-230` (Lenses 4 and 5) and `:107-110` (sibling reading);
  - `tests/test_methodology_flow.py:370-389` (`OWNERS`);
  - `spectra/extension.yml` and `catalog.json` at `1.25.0`.

  Correct any line reference in later tasks that has moved.
- [X] T002 [P] Run `python3 -m unittest discover -s tests` and `python3 tools/generate_agent_docs.py --check` on the unchanged branch. Record the baseline pass count here, so later failures can be attributed. **Baseline (2026-10-24)**: 1615 tests OK; `--check` clean (55 agents, 14 prose blocks).

**Checkpoint**: the plan's premises are true, and the suite is green before any change.

---

## Phase 2: Foundational

- [X] T003 Create `tests/test_adr_flow.py` in the house style of `tests/test_methodology_flow.py`: a module docstring listing the rules pinned (spec 037), `COMMAND = h.repo_file("spectra", "commands", "adr.md")`, and the `flat()`, `command()`, and `section(heading)` helpers copied from `EM` (section ends at the next `\n## `). No test classes yet. Every story's test task adds classes to this file, so this blocks US1, US2, and US4.

**Checkpoint**: `python3 -m unittest tests.test_adr_flow` runs (zero tests).

---

## Phase 3: User Story 1 — A significant decision reaches the constitution through `/speckit-constitution` (Priority: P1) 🎯 MVP

**Goal**: The ADR agent never writes `.specify/memory/constitution.md`. A significant ADR gets drafted
guardrail records, one approval step, two command-owned sections, and a printed amend line naming the ADR
(FR-001–FR-004, FR-007, FR-011–FR-016; research R1, R3–R7).

**Independent Test**: quickstart §3 steps 1–2, 5, 7, 8 and §4 rows 1–2: the constitution checksum is unchanged
after every run; a significant ADR ends with both sections and one line; a non-significant ADR has neither.

### Tests for User Story 1

- [X] T004 [US1] In `tests/test_adr_flow.py`, add these classes (A1–A3, A8–A18):
  - `WhatItNeverDoes`: `section("## What this command never does")` contains "write `.specify/memory/constitution.md` — in any run, approved or not" and "`/speckit-constitution` owns that file"; contains "invoke `/speckit-constitution`". `command()` contains none of "offer to make the edit", "only modify `.specify/memory/constitution.md` if the user agrees", "if a constitution update was made" (A1–A3).
  - `TheSignificanceTestIsUnchanged`: Step 7 still names "cross-cutting standard or principle", "contradicts, narrows, or extends an existing constitution principle", "establishes a convention future work is expected to follow" (A4).
  - `TheRecord`: the record block lists `id:`, `section:`, `basis: observed | aspirational`, `decision: accepted | declined | skipped | not_asked`, `status: new | amends: <principle name/number> | adopted: <principle name/number>` in that order (assert ascending `index()`); the ID rule `adr-nnn-<section-slug>-<hash>` with "computed once" / "frozen" and "a reword at the gate keeps the id" (A8).
  - `TheGate`: "show every drafted record"; the five outcomes ("approve", "revise the adr first", "talk it through", "decline", "no answer, or a non-interactive run"); "`skipped`" for decline-all; "`not_asked`" for silence; "silence adopts nothing"; "does not count against the five" (A9, A10).
  - `TheSections`: "## constitution guardrails" with "every drafted record, accepted or not"; "## constitution input" holds "exactly the records whose `decision` is `accepted`" and status not adopted; opens with "constitution check", "adr status at drafting", "goal:"; "where the resolved template places either heading" / "after the template's" and "say so once"; "write no constitution section" for a decision that is not significant; "the adr you wrote in step 6" and no other file (A11–A13).
  - `TheHandoff`: the line template "/speckit-constitution amend the constitution with every guardrail in the \"constitution input\" section of" and "cite adr-nnn as the source"; "resolved root, not the default"; "nothing reaches the constitution until that command runs"; "if nothing was accepted" → no command; "do not invoke it" (A14, A15).
  - `NoConstitution`: "goal: **pending** — no constitution exists; these records are for a later amend."; "give no command"; "speckit.spectra.domain-analyzer" named first; "once a constitution exists" (A16).
  - `AProposedAdr`: "run it once the decision is accepted" (A17).
  - `StepEight`: `section("## Step 8")` does not contain "constitution.md" and does contain "superseded" (A18).

  Run the file and confirm these tests fail.

### Implementation for User Story 1

- [X] T005 [US1] In `spectra/commands/adr.md`, add a `## What this command never does` section after `## User Input`, as a two-column `| Never | Why |` table in the style of `spectra/commands/methodology.md:50-60`, with rows: write `.specify/memory/constitution.md` — in any run, approved or not (`/speckit-constitution` owns that file: its sync impact report, its version, its propagation into dependent templates); invoke `/speckit-constitution` (a portable command cannot rely on one agent's way of calling another, and chaining takes the user out of their own governance change); write any file other than the ADR and, on supersession, the superseded ADR's status line; adopt a guardrail nobody chose (skip, silence, and a non-interactive run adopt nothing). Update the existing sentence at Step 1 item 2 ("the only constitution change you may propose is the one in Step 7") so it says the only constitution input you may draft is the one in Step 7, handed to `/speckit-constitution`.
- [X] T006 [US1] In `spectra/commands/adr.md`, rewrite `## Step 7` as "Check the ADR against the constitution and hand off". Keep the three significance bullets verbatim. Then add, in order, per [data-model.md](./data-model.md):
  - **The constitution check**: read `.specify/memory/constitution.md` semantically (section heading + MUST/SHOULD + subject), never by string match; the states `embedded` (quote the governing clause, draft nothing), `partial` (quote, name the gap, draft `amends:`), `absent` (draft `new`), `no constitution` (draft `new`; goal `pending`), `sibling ground` (US2 fills this in; leave a one-line placeholder rule "draft nothing on another feeder's ground — see Sibling ground" that T011 expands). A contradicted principle is surfaced as a finding and drafted as `amends:`, never a clause that silently overrides it.
  - **Not significant**: say so in one line with the reason, write no Constitution section, print no line, continue to Step 8.
  - **The draft**: each guardrail in the constitution's voice — declarative and testable, MUST or SHOULD, with a brief rationale; the record block exactly as data-model "Guardrail record" with keys in order `id`, `section`, `basis`, `decision`, `status`; the ID rule "`adr-NNN-<section-slug>-<hash>` — `NNN` the ADR's number from Step 3, `<section-slug>` the kebab-cased target section, `<hash>` a short (8-char) hash of the normalized statement (trimmed, lowercased, whitespace-collapsed); computed once, when first drafted, and frozen; a reword at the gate keeps the ID"; `basis` is `observed` where the codebase already holds the rule, else `aspirational`.
  - **The gate**: show every drafted record, then ask once with the five outcomes from data-model "Decision transitions", verbatim in meaning: Approve (named-to-decline → `declined`; named-to-reword → `accepted`, same id); Revise the ADR first (edit the ADR you wrote in Step 6 in place, re-draft, offer the gate again); Talk it through; Decline the whole gate (`skipped`); No answer, or a non-interactive run (`not_asked`) — "Silence adopts nothing". State that this question does not count against the five clarifying questions of Step 2.
  - **The sections**: add to the ADR you wrote in Step 6 — in this run, and no other file — `## Constitution guardrails` (every drafted record, accepted or not) then `## Constitution input` (exactly the records whose `decision` is `accepted` and whose status is not `adopted: …`), opening with the `Constitution check:` line, `ADR status at drafting: <status>`, and the goal line, then records grouped by `### <Target constitution section>` each with `id`, `placement: add | amends: <Principle name/number>`, `basis`. Fill them where the resolved template places either heading; otherwise append them after the template's last section and say so once. The format is this command's; a template cannot change it. If nothing was accepted, the section says so in one sentence and lists nothing.
  - **The goal line** from research R5, quoted exactly: `Goal: **update** the constitution at .specify/memory/constitution.md with the guardrails below.` with records; `Goal: **update** — nothing was accepted.`; `Goal: **pending** — no constitution exists; these records are for a later amend.`
  - **The invariant**, as a block quote: "You never write `.specify/memory/constitution.md`. Not on approval. Not when the file is missing. Not when the user insists." followed by the reason (`/speckit-constitution` owns the sync impact report, the MAJOR/MINOR/PATCH judgement, the version and amendment-date lines, and propagating the change).
  - **The handoff**: with a constitution and at least one accepted record, print the line from research R7 — "Next: run this to update your constitution from [ADR-NNN-<title>.md](<resolved path>):" then `/speckit-constitution Amend the constitution with every guardrail in the "Constitution input" section of <resolved path>, adding each under its section and applying "amends:" items as amendments to the principle they name, and cite ADR-NNN as the source of each change` — using the resolved root, not the default. Then: nothing reaches the constitution until that command runs. **Do not invoke it.** If the ADR's status is `Proposed`, add: run it once the decision is accepted. If nothing was accepted, say so and give no command.
  - **No constitution**: records are still drafted, gated, and written with goal `pending`; give no command; point the user to the foundation agents, `speckit.spectra.domain-analyzer` first; say that once a constitution exists, the accepted records can be amended in from this ADR.
- [X] T007 [US1] In `spectra/commands/adr.md` `## Step 8`, remove "(include the constitution file only if it was edited …)" and the "If a constitution update was made, suggest staging that file in the same commit" sentence. The file list is the ADR, plus the superseded ADR when Step 5 updated its status line. Add one sentence: a constitution change is committed after `/speckit-constitution` runs, as its own change.
- [X] T008 [US1] Run `python3 -m unittest tests.test_adr_flow` and make T004's tests pass. Run the full suite to confirm `tests/test_doc_output_paths.py` and `tests/test_document_templates.py` still pass unchanged (A19).

**Checkpoint**: US1 is shippable alone — the constitution can no longer be edited by the ADR agent, and a significant decision reaches it through `/speckit-constitution`.

---

## Phase 4: User Story 2 — A decision on another agent's ground is referred, not drafted (Priority: P1)

**Goal**: The ADR agent drafts only on its own ground; domain-analyzer states the split from its side and
cites accepted ADR records on architecture ground before drafting (FR-008–FR-010, FR-019; research R2).

**Independent Test**: quickstart §3 steps 3–4 and §4 row 3: no record for a test-strategy / deployment-strategy
decision; the language part of a mixed decision referred; domain-analyzer cites the ADR's accepted record.

### Tests for User Story 2

- [X] T009 [US2] In `tests/test_adr_flow.py`, add class `SiblingGroundIsReferred` (G1–G4):
  - own ground: "architecture-level choices", "datastores", "messaging", "architecture style", "service and data boundaries", "layering", "integration patterns", "security, data handling, or reliability"; "governed clause by clause";
  - an `OWNERS` tuple mirroring `EM`'s: `speckit.spectra.test-strategy` → ("test levels", "coverage floor", "ratchet", "uat"); `speckit.spectra.deployment-strategy` → ("environments", "promotion", "rollback", "versioning scheme", "release cut", "hotfix promotion"); `speckit.spectra.domain-analyzer` → ("languages", "frameworks", "runtimes", "dependency policy", "bounded contexts", "invariants", "glossary"); `speckit.spectra.methodology` → ("methodology overlays", "work modes", "branching", "review gates", "change records"); each owner and ground is named in Step 7;
  - "draft nothing" on sibling ground; "name the owner", "whether its document exists", "re-run"; "read only records whose `decision` is `accepted`" and a contradicted record is named;
  - a mixed decision: "drafts only the architecture-level part";
  - prior ADRs: "`superseded` or `deprecated`" records count "only as the principle a supersession amends".
- [X] T010 [P] [US2] In `tests/test_domain_analyzer_flow.py`, add class `GroundIsSharedWithTheAdrAgentClauseByClause` (D1–D3): Lens 5's ground names "languages, frameworks, and runtimes" and "dependency" and states architecture-level choices belong to `speckit.spectra.adr`; Step 1 reads "`<artifact-root>/adr/`" Constitution input sections, "accepted" records only, from ADRs whose status is "`proposed` or `accepted`", and names "`superseded`" and "`deprecated`" as never constraining; the shared-ground paragraph says "every lens except" "technology & dependency policy", cites an accepted ADR record that covers a clause "instead of drafting" it, may draft what no accepted ADR record covers, and a later change is an `amends:`. Confirm the seven-question count and lens names in the existing classes are untouched (D4).

  Run both test files and confirm the new tests fail.

### Implementation for User Story 2

- [X] T011 [US2] In `spectra/commands/adr.md` Step 7, replace T006's placeholder with a **Sibling ground** subsection: the own-ground statement verbatim from FR-010 ("architecture-level choices — datastores, messaging and eventing infrastructure, architecture style (for example monolith, modular monolith, services), service and data boundaries and ownership, layering, and integration patterns — plus architectural decisions on security, data handling, or reliability (for example mTLS between services, a data-retention mechanism, an observability stack), and conventions future work must follow that no sibling owns. Ground shared with domain-analyzer is governed clause by clause"); the referral table from data-model "Referral" (ground → owner → document checked); rules: draft nothing on a sibling's ground; when reading prior ADRs' Constitution input sections, a `Superseded` or `Deprecated` ADR's records count only as the principle a supersession amends, never as a constraint; for each referred part name the owner, say whether its document exists at the artifact root, suggest re-running it (each reads ADRs as evidence); where the document exists, read only records whose `decision` is `accepted` and name any the decision contradicts; a decision naming a language, framework, or dependency rule is domain-analyzer's even when recorded as an ADR; a mixed decision drafts only the architecture-level part; ground shared with domain-analyzer (every lens except Technology & dependency policy) is governed clause by clause — check the constitution and `DOMAIN_ANALYSIS.md`'s accepted records, and draft `amends:` where a clause already exists. Add the referral to the `Constitution check:` line of the Constitution input section.
- [X] T012 [P] [US2] In `spectra/commands/domain-analyzer.md`:
  - Step 1: add an input item after "Sibling strategies" — **Accepted ADR records**: the `## Constitution input` sections of `<artifact-root>/adr/*.md`; only records whose `decision` is `accepted` constrain you, and only from ADRs whose status line is `Proposed` or `Accepted`; an ADR marked `Superseded` or `Deprecated` never constrains you; a `declined`, `skipped`, or `not_asked` record never does; an ADR without the section (written before 1.26.0, or not significant) is ordinary documentation, cited `claimed`.
  - Step 4 table, Lens 5 "What you look at": keep "Languages, frameworks, and runtimes actually in use; how dependencies are added and pinned".
  - After the "Testing, deployment, and workflow are referred, not proposed" paragraph, add a paragraph **The ADR agent shares this ground, clause by clause**: architecture-level choices — datastores, messaging, architecture style, service and data boundaries, integration patterns — and architectural decisions on security, data handling, or reliability are `speckit.spectra.adr`'s when recorded as a decision. Every lens except Technology & dependency policy still works what the code shows, but before drafting a clause it cites an accepted ADR record that covers it instead of drafting it; a clause no accepted ADR record covers may be drafted from observation; whichever drafts a clause first is its source, and a later ADR that changes it drafts an amendment. Lens 5 stays yours alone: an ADR naming a language, framework, or dependency rule is referred here.
- [X] T013 [US2] Run `python3 -m unittest tests.test_adr_flow tests.test_domain_analyzer_flow` and make T009 and T010 pass.

**Checkpoint**: each constitution clause has one source; US1 + US2 together are the complete ADR-side behaviour.

---

## Phase 5: User Story 3 — The methodology agent knows the ADR agent is a feeder (Priority: P2)

**Goal**: methodology's map of who owns which clause includes the ADR agent (FR-017, FR-018).

**Independent Test**: quickstart §4 row 4; `EM` passes with the ADR row.

### Tests for User Story 3

- [X] T014 [P] [US3] In `tests/test_methodology_flow.py` class `SiblingGroundIsReferred`: add `("speckit.spectra.adr", ("architecture-level choices",))` to `OWNERS`; add `test_five_agents_feed_the_constitution` asserting `section("## Step 4")` contains "five agents feed the constitution" and `command()` contains no "four agents feed"; add `test_the_adr_agent_is_not_in_the_foundation_sequence` asserting the fenced ordered list after "then the other agents that feed the constitution" does not contain "speckit.spectra.adr" (M1–M3). Run and confirm they fail.

### Implementation for User Story 3

- [X] T015 [US3] In `spectra/commands/methodology.md` Step 4: change "Four agents feed the constitution" to "Five agents feed the constitution"; add a table row `| Architecture-level choices recorded as decisions — datastores, messaging, architecture style, service and data boundaries, integration patterns | \`speckit.spectra.adr\` — \`<artifact-root>/adr/\` |`. Leave the ordered list at `methodology.md:705-713` unchanged, and add one sentence after it: the ADR agent also feeds the constitution, one decision at a time, and is not part of this sequence. Search the file for any other "four" feeder count and update it.
- [X] T016 [US3] Run `python3 -m unittest tests.test_methodology_flow` and make T014 pass.

**Checkpoint**: methodology's sibling-ground map matches the five feeders.

---

## Phase 6: User Story 4 — A superseding ADR amends the clause its predecessor created (Priority: P3)

**Goal**: supersession and existing clauses produce amendments, never duplicates (FR-005, FR-006).

**Independent Test**: quickstart §3 step 6: a superseding ADR's record is `amends: <principle>`; an already
stated guardrail is quoted and not drafted.

### Tests for User Story 4

- [X] T017 [US4] In `tests/test_adr_flow.py`, add class `SupersessionAmends` (A5–A7): Step 7 states that where the decision supersedes an ADR whose guardrail the constitution carries, the record is drafted as "`amends:`" against that principle; that a guardrail the constitution already states is `embedded` — "quote the governing clause" and "draft nothing"; that a contradiction is "surfaced" and never "silently overrides". Run and confirm the supersession assertion fails.

### Implementation for User Story 4

- [X] T018 [US4] In `spectra/commands/adr.md` Step 7's constitution check, add: when Step 5 recorded a supersession, find the principle the superseded ADR introduced — by the `adr-NNN-` id in its Constitution input section, or by a citation of that ADR in the constitution's Sync Impact Report or text — and draft the new record as `amends: <that principle>`. Where none can be found, draft against the principle the check matched, or `new`. Cross-reference the supersession rule in `## Step 5` with one sentence pointing to Step 7.
- [X] T019 [US4] Run `python3 -m unittest tests.test_adr_flow` and make T017 pass.

**Checkpoint**: all four stories pass their tests.

---

## Phase 7: Polish & Cross-Cutting Concerns (release surfaces, Principle V)

- [X] T020 [P] Bump `spectra/extension.yml` `version` to `1.26.0` and change the `speckit.spectra.adr` description to "Create a new Architecture Decision Record from a short description, grounded in the codebase and constitution, and hand any constitution change to /speckit-constitution."
- [X] T021 [P] Set the `spectra` entry's `version` in `catalog.json` to `1.26.0` (command count unchanged).
- [X] T022 [P] Add `## [1.26.0] - <date>` to the top of `spectra/CHANGELOG.md` with a one-line summary and a **Changed** list: the ADR agent hands off instead of editing the constitution (records with `adr-NNN-` IDs, one approval step, Constitution guardrails and Constitution input sections, an amend line citing the ADR, `pending` with no constitution, Step 8 no longer stages the constitution); the ADR agent drafts only on architecture ground and refers the rest; methodology lists the ADR agent as a fifth feeder; domain-analyzer cites accepted ADR records on architecture ground.
- [X] T023 [P] Update the hand-written prose in `AGENTS_LIST.md`: the `<!-- SPECTRA:AGENT id=adr -->` block ("flags any constitution update the decision implies" → drafts the constitution change for you to approve and hands it to `/speckit-constitution`; it never edits the constitution); the `id=domain-analyzer` block (one clause: cites accepted ADR decisions on architecture); the `id=methodology` block only if it states a feeder count. Do not touch generated regions.
- [X] T024 [P] Update `docs/index.html`: the `speckit.spectra.adr` card at `:629` (add that a significant decision gets a drafted constitution change and a ready-to-paste `/speckit-constitution` line, and that it never edits the constitution); the `speckit.spectra.domain-analyzer` card at `:636` only if a clause fits naturally. Check `README.md` and `spectra/README.md` hand-written prose for any sentence saying the ADR agent edits the constitution.
- [X] T025 Add class `NoStaleProse` to `tests/test_adr_flow.py` (R4): the `id=adr` block of `AGENTS_LIST.md` and the `speckit.spectra.adr` card in `docs/index.html` contain "/speckit-constitution" and do not contain "flags any constitution update". Run it.
- [X] T026 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip` (after T005–T024).
- [X] T027 Run `python3 tools/generate_agent_docs.py --check`, `python3 -m unittest discover -s tests`, and `python3 tools/ship.py --dry-run`; all must pass. Compare the test count with T002's baseline. **Result (2026-10-24)**: 1653 tests OK (+38: 33 `AD`, 3 `DA`, 2 `EM`); `--check` clean; ship dry-run passed catalog-parity, description-parity, generated-listings, zip-matches.
- [X] T028 Walk [quickstart.md](./quickstart.md) §3–§4 in a throwaway Spec Kit project with `specify extension add --dev /Users/alibahaloo/Projects/spectra/spectra`, recording the constitution checksum before and after each run (SC-001). Note any deviation in this file under the task.
  - **Done (2026-10-24)**: walked by the maintainer in a throwaway Spec Kit project. T024 also updated `spectra/README.md`'s ADR walkthrough (step 4 said it "offers to make" the edit), and `NoStaleProse` covers that surface too.

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)** → **Foundational (Phase 2, T003)** → user stories.
- **US1 (Phase 3)** has no story dependency. It is the MVP.
- **US2 (Phase 4)** depends on US1's T006 (it replaces the placeholder T006 leaves in Step 7). Its domain-analyzer half (T010, T012) does not, and can start after T003.
- **US3 (Phase 5)** has no dependency on any other story: it touches only `methodology.md` and `EM`.
- **US4 (Phase 6)** depends on US1's T006 (it extends the constitution check).
- **Polish (Phase 7)** depends on every story. T026 depends on all edits under `spectra/`.

### Shared files (no `[P]` across these)

- `spectra/commands/adr.md`: T005 → T006 → T007 → T011 → T018.
- `tests/test_adr_flow.py`: T003 → T004 → T009 → T017 → T025.

### Within each story

Test task first and failing → command edit → run tests green.

## Parallel Opportunities

- T002 alongside T001.
- Once T003 is done: US3 (T014–T016) and the domain-analyzer half of US2 (T010, T012) can run alongside US1.
- In Polish: T020, T021, T022, T023, T024 together; then T025 → T026 → T027 → T028.

```text
# After T003:
Track A (adr.md):           T004 → T005 → T006 → T007 → T008 → T009 → T011 → T013 → T017 → T018 → T019
Track B (domain-analyzer):  T010 → T012
Track C (methodology):      T014 → T015 → T016
```

## Implementation Strategy

1. **MVP = Phases 1–3 (US1).** It removes the defect: the ADR agent can no longer write the constitution, and
   significant decisions reach it through `/speckit-constitution`. Stop and run quickstart §3 steps 1–2.
2. **Add US2** before shipping: without it, the ADR agent can draft a clause another feeder owns.
3. **Add US3 and US4.** Both are small; US3 can land in parallel.
4. **Polish once**, at the end: one version bump (1.26.0), one changelog entry, one zip rebuild, then
   `tools/ship.py`.

---

## Phase 8: Convergence

- [X] T029 Replace the stale gate item in `docs/e-learning/customization.html:905` ("If the agent recommended a constitution change, you decided on purpose. It edits the constitution only if you agree.") with the 1.26.0 behaviour: if the decision was significant, you approved, declined, or reworded each drafted guardrail; the ADR ends with Constitution guardrails and Constitution input sections; the agent printed a `/speckit-constitution` line and never edited the constitution. Extend `tests/test_adr_flow.py` `NoStaleProse` to scan this page for "edits the constitution only if you agree" per FR-001 (contradicts)
- [X] T030 Widen the `speckit.spectra.adr` row of the sibling-ground table in `spectra/commands/methodology.md` to the full FR-010 ground — add layering, and architectural decisions on security, data handling, or reliability — and assert "layering" and "security, data handling, or reliability" in `tests/test_methodology_flow.py` `SiblingGroundIsReferred.OWNERS`; then rebuild `docs/packages/spectra.zip` per FR-017 (partial)
