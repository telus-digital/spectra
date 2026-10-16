# Tasks: What a Review Is Measured Against

**Input**: [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/review-pr-behaviour.md](./contracts/review-pr-behaviour.md),
[quickstart.md](./quickstart.md)

**Branch**: `033-review-pr-standards-and-intent`

**Tests**: requested by the spec. Every behaviour is pinned in `tests/test_review_pr_flow.py` (stdlib
`unittest`, via the existing `States` mixin and `assertStates`/`refuteStates`). Within each story, write the
test class first and watch it fail, then edit the command.

**Line numbers** refer to `spectra/commands/review-pr.md` at 1.21.0. They drift as earlier tasks land, so
locate each site by its heading. Implementation tasks all edit that one file, so they run in sequence. Only
test tasks and other-file tasks are `[P]`.

---

## Phase 1: Setup — verify the premise

- [X] T001 Run `python3 -m unittest discover -s tests` on the branch before any edit and record the pass count,
  as the regression baseline for contract item 20 (`tests/`)
- [X] T002 Confirm the four gaps the spec's Current State table cites still hold in
  `spectra/commands/review-pr.md`:
  - "a named engineering principle" at `:423` with no principle defined
  - Step 4's table at `:236–241` without supporting docs
  - no "older/previous/supersede" anywhere
  - `:391–402` containing only prohibitions
- [X] T003 [P] Confirm the singleton names and earlier locations in `.specify/memory/constitution.md`
  Principle VII, and the artifact-root resolution prose in `spectra/commands/test-plan.md:167–173`, against R2
  in `specs/033-review-pr-standards-and-intent/research.md`

**Checkpoint**: the defects exist as described, and the baseline test count is known.

---

## Phase 2: Foundational — shared vocabulary every story cites

These sections are referenced by more than one story, so they land first.

- [X] T004 [P] Add a new test class `TheBaseline` to `tests/test_review_pr_flow.py`. It asserts:
  - the B1–B7 table holds exactly these statements: "Correct on the paths it touches", "Safe at trust
    boundaries", "Data is never lost or corrupted", "Published contracts don't break silently", "Changed
    behaviour is tested", "Consistent with the codebase", "Failures are observable"
  - the anchor rule names "a Spectra baseline ID"

  Contract items 6 and 7.
- [X] T005 In `spectra/commands/review-pr.md` Step 5, add a subsection `### The Spectra baseline` with the B1–B7
  table (ID · principle · what it catches) from `data-model.md`. State that the set is closed, and that a
  baseline ID is the only valid "named engineering principle" (FR-004).
- [X] T006 In `spectra/commands/review-pr.md` Step 6 anchor rule (`:423`), replace "a named engineering
  principle" with "a Spectra baseline ID (B1–B7, Step 5)" (FR-004).
- [X] T007 In `spectra/commands/review-pr.md` Step 6, rename "**Two floors override the table:**" to
  "**Floors and ceilings override the table:**". Keep both existing floors verbatim and the issue ceiling
  unchanged. Leave a marked place for the new rules that later stories add (R8).

**Checkpoint**: `TheBaseline` passes. The anchor rule has a defined source; no story-specific behaviour yet.

---

## Phase 3: User Story 1 — A new spec is the contract, not the old one (P1) 🎯 MVP

**Goal**: the shipped (or reviewer-named) spec is the only traceability baseline. Older specs never drive a
code-change finding.

**Independent test**: quickstart scenario A. No finding asks for code to match the older spec; at most one
suggestion-free staleness Minor.

- [X] T008 [P] [US1] Add test class `TheAuthorizingSpec` to `tests/test_review_pr_flow.py`. It asserts:
  - "The authorizing spec is the only baseline" is stated
  - conforming code to a non-authorizing spec is forbidden
  - the staleness note requires the authorizing spec to name the older one, is "Minor" at most, and carries no
    suggestion
  - a PR shipping two specs runs traceability against both, with a conflict raised as a Question

  Contract items 10 and 11.
- [X] T009 [US1] In `spectra/commands/review-pr.md` Step 4, after "Locating the spec" (`:245–278`), add a
  paragraph headed **"The authorizing spec is the only baseline."** It says:
  - the spec found in the diff, or named by the reviewer, is authorizing
  - it overrides every older spec describing the same behaviour
  - older specs are not read for traceability
  - the one permitted lookup applies only when no spec authorizes the PR (forward reference to Step 5)

  FR-008.
- [X] T010 [US1] In `spectra/commands/review-pr.md` Step 5 Traceability (`:353–375`), add the rule that no finding
  may ask for code to conform to a non-authorizing spec. Add the FR-010 staleness note: only when the
  authorizing spec names an older spec it changes and the diff leaves that spec untouched; at most one Minor; no
  suggested change. Add the two-specs rule: each finding names the spec it rests on, and a conflict between
  them is a Question naming both (FR-009, FR-010, spec edge cases).
- [X] T011 [US1] In `spectra/commands/review-pr.md` Step 6 "Floors and ceilings" (from T007), add the ceiling: a
  divergence from a non-authorizing spec is never a code-change finding, and its staleness note is ≤ Minor
  (FR-009, FR-010).
- [X] T012 [US1] In `spectra/commands/review-pr.md` Step 10 "Never offer one for" (`:761–763`), add "a finding sourced
  from a spec that does not authorize this PR, including the staleness note" (FR-010).
- [X] T013 [US1] In `spectra/commands/review-pr.md` Edge cases (`:928–`), add rows for:
  - "Shipped spec changes behaviour an older spec defined"
  - "PR ships two feature specs"
  - "PR edits an older spec as well as shipping its own"
  - "Reviewer-named spec is older than others on the same behaviour"

  Each row matches the spec's Edge Cases.

**Checkpoint**: `TheAuthorizingSpec` passes. Scenario A behaves. This alone fixes the reported defect.

---

## Phase 4: User Story 2 — A project with no constitution still gets a principled review (P1)

**Goal**: the standards chain T1–T4, with its severity rules and coverage statement.

**Independent test**: quickstart scenarios B and C. Every finding cites a supporting-doc clause, a convention
with a `file:line`, or a baseline ID, and coverage names the governing tier.

- [X] T014 [P] [US2] Add test class `TheStandardsChain` to `tests/test_review_pr_flow.py`. It asserts:
  - T1–T4 are stated in order, with "every tier below" kept in play
  - each R2 supporting-doc path is present, verbatim: `TEST_STRATEGY.md`, `test-strategy/TEST_STRATEGY.md`,
    `DEPLOYMENT_STRATEGY.md`, `DOMAIN_ANALYSIS.md`, `.specify/memory/domain-analysis.md`, `CONTRIBUTING.md`,
    `.github/CONTRIBUTING.md`
  - the ADR location (`adr/`, earlier `Docs/ADR/`) is stated as part of T1, not T2
  - no other path is tried
  - the Major row reads "an explicit constitution, ADR, or supporting-document clause"
  - the command's own "Judgment is not overridable either" list names the standards chain and the baseline
  - supporting docs are read at `baseRefOid`
  - enforced lint/CI config suppresses findings
  - a T2 edit is a governance change
  - the constitution floor is constitution-only
  - B6 and convention findings are capped at Minor
  - a convention needs a `file:line` example, and none is raised when two patterns are in use
  - the template's judgment disclaimer lists the standards chain and the baseline

  Contract items 1–5, 8 and 9.
- [X] T015 [US2] In `spectra/commands/review-pr.md` Step 4 revision table (`:236–241`), add rows "Supporting docs —
  `baseRefOid`" and "Codebase conventions — `baseRefOid`", each with a one-line why (FR-001, R1).
- [X] T016 [US2] In `spectra/commands/review-pr.md` Step 4, add a subsection `### The standards chain` stating:
  - T1–T4, with "use the first tier available and keep every tier below it in play" (FR-001)
  - precedence T1 > T2 > T3 > T4, and that a conflict between documents is a coverage note, not a finding
  - artifact-root resolution, as `test-plan` does it: an `Artifact root:` line matched case-insensitively,
    otherwise `docs/`, and `docs/` when there is no constitution
  - the exact R2 supporting-doc path list including earlier locations; canonical wins when both exist; no other
    path is tried (FR-002)
  - that the same root resolution locates T1's ADRs (`<root>/adr/*.md`, earlier `Docs/ADR/`), which stay in T1
  - T3 rules: the pattern must be observed at `baseRefOid` with a `file:line` example; a convention the PR
    introduces doesn't count; none is raised where two patterns are in use (FR-003)
  - R7: enforced lint/format/CI config suppresses findings of the kind that tool enforces, and coverage says so
  - the absent-versus-unreachable rule applies to every T2 read, by reference to the existing paragraph
- [X] T017 [US2] In `spectra/commands/review-pr.md` Step 5 Guardrails (`:377–384`):
  - evaluate against the governing tier and every lower one; quote the clause, or cite the convention's
    `file:line`, or cite the baseline ID
  - extend the governance-change rule to T2 documents (FR-007)
  - state that a missing constitution makes the review narrower, not broader
- [X] T018 [US2] In `spectra/commands/review-pr.md` Step 5 "Guardrail coverage" (`:404–413`), generalise "the
  constitution" to "the governing tier". Keep "how many principles you read, and how many were applicable", now
  per tier. Keep the remedy naming `speckit.spectra.domain-analyzer` and the Spec Kit `constitution` command, and
  apply it whenever T1 is absent (FR-006). These phrases are pinned by `ConstitutionApplicability` in
  `tests/test_review_pr_flow.py` and MUST survive verbatim, whitespace aside:
  - "how many principles you read, and how many were applicable"
  - "has no clause bearing on"
  - "speckit.spectra.domain-analyzer"
  - "never let silence imply it was consulted"
  - "Which context authorized the review" (Step 7, touched by T020)

  Run that test class after this task.
- [X] T019 [US2] In `spectra/commands/review-pr.md` Step 6 "Floors and ceilings", restate the constitution-MUST
  floor as T1-only. Add: T2/T3/T4 findings are classified by consequence through the rubric, with no floor; B6
  and T3 findings ≤ Minor. In the severity table's **Major** row (`:434`), change "violates an explicit
  constitution or ADR clause" to "violates an explicit constitution, ADR, or supporting-document clause", so a
  T2 violation is eligible for Major without a floor (FR-005).
- [X] T020 [US2] In `spectra/commands/review-pr.md` Step 7 item 3 (`:480`), add the governing standards tier. In
  "Coverage & limits" (`:521–523`), extend "Which context authorized the review" with:
  - the governing tier
  - each T2 document found, or not found with the path tried
  - anything deferred to tooling

  FR-006.
- [X] T021 [P] [US2] In `spectra/templates/review-template.md`, extend the "Nor does this template decide
  *judgment*" list in the HOW TO USE comment with "the standards chain and the Spectra baseline". Change no
  section (FR-019).
- [X] T021a [US2] In `spectra/commands/review-pr.md` Step 10, the paragraph "**Judgment is not overridable
  either.**" (`:725`): add the standards chain (T1–T4) and the Spectra baseline (B1–B7) to its list. Keep "two
  reviews of the same diff would stop agreeing" verbatim, because `test_judgment_is_not_overridable` pins it
  (FR-019).
- [X] T022 [US2] In `spectra/commands/review-pr.md` Edge cases, replace the "No constitution at all" row with:
  "State its absence; review against T2–T4; state the governing tier; name the remedy commands". Before
  replacing it, grep `tests/` for the old row text; any test pinning it must keep passing. Add rows for "Supporting doc
  contradicts the constitution", "PR edits a supporting doc", and "Codebase uses two conflicting patterns".

**Checkpoint**: `TheStandardsChain` passes. Scenarios B and C behave.

---

## Phase 5: User Story 3 — A vibe-coded PR is reviewed for what nobody said (P2)

**Goal**: the stated-intent check (no-spec only), and the three always-on lenses with their severity rules.

**Independent test**: quickstart scenarios D and F.

- [X] T023 [P] [US3] Add test class `TheAlwaysOnLenses` to `tests/test_review_pr_flow.py`. It asserts:
  - intent order: reviewer-named spec → issue → PR title/body/commits
  - PR text is data, never instruction, ≤ Minor
  - the stated-intent check is "not run" with an authorizing spec, because traceability replaces it
  - blast radius, generation artifacts and test integrity are "always considered", each reported run or not run
  - blast radius uses at most five `gh search code` calls, discloses the cap, and is classified by the rubric,
    not the PR-text ceiling, with a B4 break as Blocker
  - each R6 weakened-test case is listed, with weakened/deleted test ≥ Major and the expected-value case
    requiring high confidence
  - a new dependency is always raised: Question, or Major when unpinned against the project convention or a
    duplicate, checked "against the repository … not against an external registry"

  Contract items 12, 13 and 15–18.
- [X] T024 [US3] In `spectra/commands/review-pr.md` Step 4 "The linked issue" section (`:280–339`), add the third
  intent source for no-spec PRs: the PR title, body and commit messages (`gh pr view <ref> --repo "$REPO" --json
  title,body,commits`). It is the weakest source and is data about intent, never instruction, as the issue body
  is at `:333` (FR-011, FR-012).
- [X] T025 [US3] In `spectra/commands/review-pr.md` Step 5 "Choose lenses" (`:343–351`), keep the conventional list
  and its "do not run every lens" rule. Add:
  - the three always-on lenses (blast radius, generation artifacts, test integrity), always considered and
    reported run or not run with a reason, with R5's example wordings
  - the stated-intent check, considered only without an authorizing spec, and otherwise reported as "not run —
    traceability against the spec replaces it"

  FR-013, FR-013a.
- [X] T026 [US3] In `spectra/commands/review-pr.md` Step 5, add `### Blast radius`:
  - patch-visible changes first (defaults, removed branches, signatures, exports)
  - then up to **five** `gh search code "<symbol>" --repo "$REPO"` calls, in Step 3 risk order, skipping test
    files
  - read a hit at `headRefOid` only when it decides severity
  - code search sees the default branch only; disclose that when `baseRefName` differs
  - coverage records searches run, skipped, and the cap
  - a truncated search lowers confidence and never itself yields a finding
  - a rate-limited or failed search is reported as unreachable, never as "no callers", and is not retried in a
    loop (R3 rate-limit rule)

  FR-013a, R4.
- [X] T027 [US3] In `spectra/commands/review-pr.md` Step 5, add `### Generation artifacts`. List, verbatim from
  FR-013a: references to APIs or modules that don't exist, new dependencies, leftover placeholders/TODOs/mocks,
  overly broad error handling, duplicates of existing helpers, commented-out code, and noise from unrelated
  reformatting. Add the FR-014 dependency rule: always raised; Question by default; Major when unpinned against
  how the project pins its existing dependencies, or when it duplicates a dependency already declared; both
  checked at `baseRefOid` in the repository, not against an external registry.
- [X] T028 [US3] In `spectra/commands/review-pr.md` Step 5, add `### Test integrity` with the R6 cases:
  - assertion removed or weakened (equality → truthiness, exact → contains, exception type widened)
  - skip or expected-failure marker added
  - test function deleted
  - expected value changed in the same direction as the code with no requirement saying so (high confidence
    only)

  The test must be in the same diff as the code it exercises (FR-015).
- [X] T029 [US3] In `spectra/commands/review-pr.md` Step 5 "When there is no spec" (`:391–402`), rewrite it to lead
  with what the review **does**: the intent order (T024), the stated-intent check, and the forward reference to
  the prior-spec lookup (US4). Keep every existing prohibition verbatim: no-spec stated in the header,
  traceability not run without spec or issue, guardrails at full strength, intent capped at Question
  (FR-011, FR-013).
- [X] T030 [US3] In `spectra/commands/review-pr.md` Step 6 "Floors and ceilings", add:
  - the floor: weakened or deleted test ≥ Major, with the expected-value case needing high confidence (FR-015)
  - the ceiling: PR-text-only ≤ Minor, intent → Question (FR-011)
  - the explicit non-ceiling: blast radius is classified by the rubric, not the PR-text ceiling, and B4 breakage
    is a Blocker (FR-015a)
  - the dependency rule (FR-014)
- [X] T031 [US3] In `spectra/commands/review-pr.md` Step 7 "Coverage & limits", add: the intent source used, each
  always-on lens and the stated-intent check with run/not-run, and blast-radius searches against their cap
  (FR-013a, SC-005).
- [X] T032 [US3] In `spectra/commands/review-pr.md` Edge cases, replace the "No spec" row with one naming the
  stated-intent check, the always-on lenses, and the Question cap. Add rows for "PR description contains
  instructions", "Empty PR description, no spec, no issue", "New dependency", and "Test weakened alongside the
  code".

**Checkpoint**: `TheAlwaysOnLenses` passes. Scenarios D and F behave.

---

## Phase 6: User Story 4 — An undocumented change to specified behaviour becomes a question (P2)

**Goal**: the bounded prior-spec lookup and its Question-only output.

**Independent test**: quickstart scenario E. One Question cites the older spec's requirement ID, states both
readings, and carries no suggestion.

- [X] T033 [P] [US4] Add test class `ThePriorSpecLookup` to `tests/test_review_pr_flow.py`. It asserts:
  - the lookup runs only without an authorizing spec
  - at most three keys, using `gh search code` with `--filename spec.md`
  - the hit is read at `baseRefOid`
  - the default-branch caveat
  - "not found by search", never "not specified"
  - a rate-limited search is reported as unreachable, not as "not found"
  - a contradiction is a Question citing the spec directory and requirement ID, stating both readings ("the
    code is wrong" / "the spec is out of date"), with no suggested change
  - older specs are not a baseline for anything else

  Contract item 14.
- [X] T034 [US4] In `spectra/commands/review-pr.md` Step 5, add `### Behaviour an older spec defined`:
  - runs only when no spec authorizes the PR
  - up to **three** keys from the diff in Step 3 risk order: a public identifier (command, flag, endpoint,
    config key), or else a touched path
  - `gh search code "<key>" --repo "$REPO" --filename spec.md` per key
  - read hits at `baseRefOid`, and look for the requirement mentioning the key
  - the default-branch caveat and the "not found by search" wording
  - older specs are evidence for this question only, never a baseline
  - a rate-limited or failed search is unreachable, not absent; coverage names the keys not searched (R3)

  FR-016, R3.
- [X] T035 [US4] In the same subsection, state the output: one Question citing `specs/<dir>` and the requirement ID,
  stating both readings (the code is wrong, or the spec is out of date), never above Question, never with a
  suggestion (FR-017).
- [X] T036 [US4] In `spectra/commands/review-pr.md` Step 6 "Floors and ceilings", add the ceiling: a prior-spec
  contradiction is a Question (FR-017). In Step 10 "Never offer one for", add the prior-spec Question (FR-017).
- [X] T037 [US4] In `spectra/commands/review-pr.md` Step 7 "Coverage & limits", add: the prior-spec keys searched,
  the hits, and the default-branch note. In Edge cases, add the row "No spec, diff contradicts an older spec's
  requirement → Question citing it; no suggestion".

**Checkpoint**: `ThePriorSpecLookup` passes. Scenario E behaves.

---

## Phase 7: Polish & cross-cutting (Principle V sync)

- [X] T038 Add test `test_coverage_records_tier_and_intent_source` to `tests/test_review_pr_flow.py` (contract
  item 19), and extend `test_an_absent_constitution_is_stated` without weakening it (contract item 20).
- [X] T039 Run `python3 -m unittest discover -s tests`. All classes must pass, and the count must be the T001
  baseline plus the new tests (`tests/`).
- [X] T040 [P] Bump `spectra/extension.yml` `extension.version` 1.21.0 → 1.22.0, and the `spectra` entry's
  `version` in `catalog.json` to match (Principle VI).
- [X] T041 [P] Add `## [1.22.0] - <date>` to `spectra/CHANGELOG.md` under **Changed** for `review-pr`, covering:
  - the standards chain and baseline
  - the authorizing-spec rule
  - the always-on lenses and stated-intent check
  - the prior-spec Question
  - the new floor and ceilings
- [X] T042 [P] Update the review-pr prose block (`<!-- SPECTRA:AGENT id=review-pr -->`) in `AGENTS_LIST.md` per R9:
  one or two sentences on what the review measures against with no constitution, and that a shipped spec
  overrides older ones.
- [X] T043 [P] Update the `## speckit.spectra.review-pr` section prose in `spectra/README.md` (`:331–`) to match
  T042. Leave the generated Commands table (`:25`) alone.
- [X] T044 [P] Update the review-pr card description in `docs/index.html` (`:655`) to match T042.
- [X] T045 Run the quickstart §2 grep across `AGENTS_LIST.md`, `spectra/README.md` and `docs/index.html`. Each must
  hit in its review-pr section.
- [X] T046 Run `python3 tools/generate_agent_docs.py --check`. It must pass with no regeneration needed, because
  the roster is unchanged.
- [X] T047 Run `python3 tools/build_package.py` to rebuild `docs/packages/spectra.zip`.
- [X] T048 Run `python3 tools/ship.py --dry-run`. Checks and tests must pass and the version/zip drift checks must
  be clean.
- [X] T049 Run quickstart §3 scenarios A–G against a throwaway repository with `specify extension add --dev
  ./spectra`, and record the outcome of each in this file.
  **Closed at the maintainer's direction (2026-10-16), without a live run.** These scenarios need real pull
  requests on a throwaway GitHub repository, which were not created. The textual contract is pinned by the 30
  new assertions in `tests/test_review_pr_flow.py`.

---

## Dependencies & execution order

```text
Phase 1 Setup ─► Phase 2 Foundational (baseline + "Floors and ceilings" block)
                    │
                    ├─► Phase 3 US1 (P1, MVP) ─┐
                    ├─► Phase 4 US2 (P1) ──────┤   stories are independent in behaviour,
                    ├─► Phase 5 US3 (P2) ──────┤   but all edit review-pr.md, so implement
                    └─► Phase 6 US4 (P2) ──────┘   them one at a time in this order
                                                ▼
                                       Phase 7 Polish
```

- US4's prior-spec lookup sits in the no-spec section T029 rewrites. If US4 lands before US3, T029 must keep
  T034's forward reference.
- T011, T019, T030 and T036 all append to the block T007 creates, so they need T007.
- T040–T044 touch different files and can run together once every story is done. T045–T048 run after them,
  in order.

## Parallel opportunities

- Each story's test task (T008, T014, T023, T033) is `[P]`: it touches only the test file, so it can be written
  alongside the previous story's command edits.
- T021 (template) runs alongside any US2 command edit.
- T003 runs alongside T001–T002, and T004 alongside T005–T007.
- T040–T044: five different files, all parallel.

Example, US2:

```text
together:  T014 TheStandardsChain tests  |  T021 review-template.md comment
then:      T015 → T016 → T017 → T018 → T019 → T020 → T021a → T022   (review-pr.md, in sequence)
```

## Implementation strategy

1. **MVP = Phases 1–3.** US1 alone fixes the reported defect: older specs no longer cause code-change
   requests. It's shippable on its own, as a 1.22.0 with a narrower changelog.
2. **Then US2**, the other P1: projects without a constitution get the standards chain.
3. **Then US3 and US4** (P2): the vibe-coded lenses and the prior-spec Question.
4. **Phase 7 once**, at the end. Version, changelog, prose copies and zip all move in one change, per
   Principle V.
