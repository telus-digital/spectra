# Implementation Plan: What a Review Is Measured Against

**Branch**: `033-review-pr-standards-and-intent` | **Date**: 2026-10-16 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/033-review-pr-standards-and-intent/spec.md`

## Summary

`review-pr` is told to judge a change against its spec and the constitution, but not what to do when either
is missing, or when an older spec disagrees with the one the PR ships. This plan makes four changes. Step 4
reads a **fixed standards chain** (constitution and ADRs → Spectra's own supporting documents → codebase
conventions → a seven-principle baseline). Step 5 states that **the authorizing spec is the only traceability
baseline**. Step 5 also gains three **always-on lenses** (blast radius, generation artifacts, test integrity)
plus a no-spec **stated-intent check**. Step 6 gets the severity rules that keep all of this from widening a
review. Everything happens inside one command file. The review template changes only its comment about what
it does not control.

## Technical Context

**Language/Version**: Markdown command prompt; Python 3.9+ for tests

**Primary Dependencies**: unchanged. Standard library only; `gh` at run time, as today

**Storage**: N/A

**Testing**: `python3 -m unittest discover -s tests`; `python3 tools/generate_agent_docs.py --check`;
`python3 tools/build_package.py` then the CI drift check via `python3 tools/ship.py --dry-run`

**Target Platform**: any Spec Kit agent, slash-command or skills mode

**Project Type**: Spec Kit extension (Markdown commands)

**Performance Goals**: the new reads stay inside fixed, declared caps (R3, R4), so a review's `gh` call count
grows by a bounded amount, never in proportion to the repository

**Constraints**: Markdown only; agent-agnostic; no new argument; the blockers-and-majors default, anchor rule,
selection grammar, preview gate and publish flow are untouched (FR-018); judgment stays command-owned (FR-019)

**Scale/Scope**: one command file (Steps 4, 5, 6, 7, 10 and the edge-case table), one comment in one template,
one new test class, version sync, and three hand-written prose copies

## Evidence

| Claim | How it was verified |
|---|---|
| The baseline is referenced but never defined | `review-pr.md:423`: "a named engineering principle". No principle is named anywhere in the file |
| Supporting docs are not read | Step 4's table at `:236–241` lists spec, plan, tasks, constitution and ADRs only |
| Spectra's supporting docs have fixed names | Constitution VII names the singletons `<artifact-root>/TEST_STRATEGY.md`, `DOMAIN_ANALYSIS.md`, `DEPLOYMENT_STRATEGY.md`, and their earlier locations |
| Artifact-root resolution already exists as prose | `test-plan.md:167–173` (constitution line, default `docs/`, earlier location). `uat.md:105` reuses it by reference |
| Nothing ranks the shipped spec over older ones | No occurrence of "older", "previous" or "supersede" in `review-pr.md` |
| No-spec rules are prohibitions only | `:391–402` |
| The lens list says "do not run every lens" | `:345`, which the always-on trio must be reconciled with |
| Suggestion exclusions are an enumerated list | `:761–763`, which the FR-010 and FR-017 findings join |
| The template disclaims judgment by list | `review-template.md`, "Nor does this template decide *judgment*", which the chain and baseline join |
| The roster does not move | The `agents-list.json` title, status and command for `review-pr` are unchanged; the front-matter description stays accurate |
| Three published prose copies describe review context | `AGENTS_LIST.md:244–`, `spectra/README.md:331–`, `docs/index.html:655` |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `033-review-pr-standards-and-intent`. |
| II. Single Self-Contained Extension | ✅ | No files added to or removed from `spectra/`. The baseline lives inside the command (spec Assumptions). |
| III. Agent-Agnostic Commands | ✅ | New reads use `gh` calls the command already makes. No agent syntax. |
| IV. Context-Aware by Default | ✅ | **Strengthened.** The command now reads the documents Spectra's own agents write, rather than ignoring them. |
| V. Catalog and Package in Sync | ✅ | Manifest, catalog, changelog, zip, landing page and the prose copies move together. Roster untouched, so no generator rerun is needed beyond `--check`. |
| VI. Two Versioned Channels | ✅ | Extension channel only: 1.21.0 → 1.22.0. No tag; root `VERSION` untouched. |
| VII. Documents Under One Declared Root | ✅ | Read-only use. The command resolves the artifact root to *read* the singletons and earlier locations exactly as the principle names them, and writes nothing there. |
| VIII. Shaped by Overridable Templates | ✅ | The body's shape is unchanged. Coverage content grows inside the command-emitted "Coverage and limits" section, which the template already says it does not control. The template's judgment disclaimer gains the chain and the baseline. |

**Amendment classification**: none. The command reads what Principle VII defines and does not redefine it.

**Extension version classification**: MINOR, 1.21.0 → 1.22.0. Review output gains new behaviour (new lenses,
a cited baseline, new coverage lines). No argument, prompt, grammar or template section changes, so nothing a
user or an override relies on breaks.

## Project Structure

### Documentation (this feature)

```text
specs/033-review-pr-standards-and-intent/
├── spec.md
├── plan.md              # this file
├── research.md          # Phase 0: R1–R9
├── data-model.md        # Phase 1: tiers, baseline, intent sources, lenses, severity rules
├── contracts/
│   └── review-pr-behaviour.md   # the textual contract the tests pin
├── quickstart.md        # Phase 1: how to validate
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks, not this command
```

### Source Code (repository root)

```text
spectra/
├── commands/review-pr.md          # Steps 4, 5, 6, 7, 10, edge cases
├── templates/review-template.md   # one comment: the judgment disclaimer
├── extension.yml                  # 1.22.0
└── CHANGELOG.md                   # [1.22.0]
catalog.json                       # version mirror
docs/packages/spectra.zip          # rebuilt
docs/index.html                    # review-pr card description (:655)
AGENTS_LIST.md                     # review-pr prose block
spectra/README.md                  # review-pr section prose
tests/test_review_pr_flow.py       # new test class
```

**Structure Decision**: single-command change in the existing extension layout. No new files under
`spectra/`.

## Phase 0 — Research

See [research.md](./research.md). Every open point is resolved there:

- R1 where the chain is read
- R2 how supporting docs are located
- R3 the bounded prior-spec lookup
- R4 the blast-radius reach
- R5 how the always-on lenses fit "do not run every lens"
- R6 what counts as a weakened test
- R7 lint and CI as a suppressor
- R8 where the new severity rules sit
- R9 which prose copies move

No NEEDS CLARIFICATION remains.

## Phase 1 — Design

- **Entities and rules**: [data-model.md](./data-model.md)
- **Behavioural contract** (the phrases and structures the tests assert):
  [contracts/review-pr-behaviour.md](./contracts/review-pr-behaviour.md)
- **Validation**: [quickstart.md](./quickstart.md)

### Edit map — `spectra/commands/review-pr.md`

| Site | Change | FRs |
|---|---|---|
| Step 4 table `:236–241` | Add rows for supporting docs and codebase conventions, both at `baseRefOid` | FR-001, FR-002 |
| Step 4, new subsection after the table: **"The standards chain"** | T1–T4, keep-every-lower-tier rule, artifact-root resolution by reference to Principle VII names (R2), with ADRs located by the same root and kept in T1, and lint/CI as suppressor (R7) | FR-001–003 |
| Step 4 spec location `:245–278` | New paragraph: **"The authorizing spec is the only baseline."** Older specs are not context. One narrow exception, defined in Step 5 | FR-008, FR-009 |
| Step 5 lens selection `:343–351` | Keep the conventional list. Add the always-on trio and the no-spec stated-intent check, each reported run/not-run (R5) | FR-013, FR-013a |
| Step 5 traceability `:353–375` | The traceability table gains a "PR text only" row. A paragraph covers FR-010 | FR-008–011 |
| Step 5, new subsection **"The Spectra baseline"** | B1–B7 table: ID, principle, what it catches. The only valid "named engineering principle" | FR-004 |
| Step 5, new subsection **"Behaviour an older spec defined"** | The bounded lookup (R3), Question-only, both readings stated | FR-016, FR-017 |
| Step 5 "When there is no spec" `:391–402` | Rewritten as what the review *does*: intent order, stated-intent check, prior-spec lookup. The prohibitions stay | FR-011–013 |
| Step 5 guardrail coverage `:404–413` | Generalised from "the constitution" to "the highest tier available". The remedy is named when T1 is absent | FR-006 |
| Step 6 severity `:439–453` | A third floor (weakened test ≥ Major). Ceilings: baseline has no floor; B6/T3 ≤ Minor; PR-text ≤ Minor; prior-spec = Question. Blast radius by rubric, dependency rule (R8) | FR-005, FR-014, FR-015, FR-015a, FR-017 |
| Step 6 severity table, Major row `:434` | "constitution or ADR clause" → "constitution, ADR, or supporting-document clause": eligible for Major, no floor | FR-005 |
| Step 10 "Judgment is not overridable either" `:725` | Add the standards chain and the baseline to the list | FR-019 |
| Step 6 anchor rule `:423` | "a named engineering principle" → "a Spectra baseline ID (B1–B7)" | FR-004 |
| Step 7 item 3 `:480` | Gains the standards tier used | FR-006 |
| Step 7 coverage `:521–523` | "Which context authorized" gains the tier and the intent source. "How much of the constitution applied" becomes per tier | FR-006 |
| Step 10 suggestion exclusions `:761–763` | Add: a finding sourced from a non-authorizing spec, and a stale-spec Minor | FR-010, FR-017 |
| Edge cases `:928–` | Rows for every spec edge case. Replace the "No spec" and "No constitution at all" rows | all |

### Other files

- `review-template.md`: add "the standards chain and the baseline" to the judgment list in the HOW TO USE
  comment. No section changes.
- Prose copies (R9): each states what the review is measured against with no constitution and with no spec.
  The per-agent prose stays hand-written.

## Re-check after design

All eight principles still pass. Design added no file to `spectra/`. Every new read is `gh api … ?ref=<sha>`
or one bounded `gh search code`, both already-sanctioned `gh` use (Principle III). No write location was
introduced (VII). No template section was added (VIII).

## Risks

| Risk | Mitigation |
|---|---|
| The baseline becomes a licence for taste: "B1" cited on everything | The anchor rule still needs a file and line. B6/T3 cap at Minor. A baseline finding has no floor, so it reaches the default proposal only on consequence |
| The prior-spec lookup turns back into "read every old spec", the defect itself | R3 makes it a keyed lookup with a hard cap. FR-009 forbids conforming to a non-authorizing spec; a test asserts it |
| Always-on lenses inflate every review | Their findings run through the same rubric and the unchanged blockers-and-majors default. Only test-integrity has a new floor, and only for a measurable act |
| Blast-radius caller search is slow or rate-limited | R4 caps it and discloses the cap in coverage. A capped search reduces confidence; it never yields a finding |
| Code search sees only the default branch | R3/R4: when base ≠ default branch, coverage says the lookup ran against the default branch. It never reports absence it couldn't check (existing "absent vs unreachable" rule) |
| A supporting doc contradicts the constitution | The constitution wins (spec edge case). The contradiction is a coverage note, not a PR finding |
| One prose copy is left describing the old no-spec behaviour | The quickstart's grep covers all three copies before the zip rebuild |

## Complexity Tracking

> No violations. No file, command, argument, template section, or dependency is added.
