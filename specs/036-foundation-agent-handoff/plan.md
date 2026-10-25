# Implementation Plan: Safe Handoffs Between the Foundation Agents

**Branch**: `036-foundation-agent-handoff` | **Date**: 2026-10-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/036-foundation-agent-handoff/spec.md`

## Summary

Five foundation agents get one shared handoff contract. No agent is added and no lens or question changes.

1. **kb-vault stops writing the four constitution-feeder singletons.** It drops four rows from its reserved
   map. An imported domain analysis, methodology, test strategy, or deployment strategy now lands in one of
   four fixed series folders (`<root>/<kind>-source/NNN-<title>.md`). It is shaped by
   `<kind>-source-template` if a project provides one, and by `kb-document-template` otherwise. The plan
   and report refer the user to the owning agent.
2. **The four feeders read that material on purpose.** Each one reads its own `-source` folder by path,
   plus any document under the root whose Provenance section marks it as kb-vault output. Those documents
   are cited with the provenance `claimed`. That word already exists in deployment-strategy and means
   "what a document says". Basis (`observed` / `aspirational`) and adoption are still decided only by
   code, history, configuration, and the team's answers.
3. **test-strategy and deployment-strategy adopt the feeder contract** that domain-analyzer and methodology
   already follow:
   - the goal (create / update) is stated first;
   - a `Constitution input` section replaces the checkbox amendment, with frozen `ts-` / `ds-` IDs, a
     decision for each guardrail, and adoption tracking;
   - the hand-off is worded for the goal;
   - a re-run migrates a checkbox amendment without losing anything.
   The approval gate stays where it is. Free text in the reply declines or rewords individual guardrails.
4. **Ownership is marked the same way everywhere.** All four feeders write
   `command: speckit.spectra.<agent>` in their header. A file from an earlier version is recognised by the
   header fields that version wrote. A file at the path that the feeder did not write is read as `claimed`
   evidence and replaced only with consent. methodology already behaves this way, and the other three now
   do too.
5. **review-pr** applies its accepted-only rule to the two strategies.
6. **Documentation.** The brownfield onboarding sequence goes into `README.md`, `spectra/README.md`, and
   `docs/index.html`, with a test that keeps the three in agreement.

The extension goes from 1.24.0 to 1.25.0. No constitution amendment is needed.

## Technical Context

**Language/Version**: Markdown command prompts and templates; Python 3.9+ for tests and tooling

**Primary Dependencies**: none. Standard library only; the zero-dependency rule covers the whole repository

**Storage**: Markdown files in the consumer's project:
- the four singletons, each with YAML front matter;
- kb-vault source documents under `<root>/<kind>-source/`.

**Testing**:
- `python3 -m unittest discover -s tests`
- `python3 tools/generate_agent_docs.py --check`
- `python3 tools/build_package.py`
- `python3 tools/ship.py --dry-run`

**Target Platform**: any Spec Kit agent, in slash-command or skills mode

**Project Type**: Spec Kit extension (Markdown commands), catalog channel only

**Performance Goals**: no change. The rounds keep their fixed question counts: 7, 10, 5, and 5

**Constraints**:
- Markdown only; no scripts in the package.
- Agent-agnostic.
- Each feeder still writes exactly one file and never writes the constitution.
- kb-vault still writes nothing before approval.
- No network access.
- Earlier-format documents must keep working for every reader.

**Scale/Scope**:
- Edits to six commands: `kb-vault`, `domain-analyzer`, `methodology`, `test-strategy`,
  `deployment-strategy`, `review-pr`.
- Edits to two templates: `test-strategy-template`, `deployment-strategy-template`.
- Edits to the three documentation surfaces.
- The usual version sync.
- Updates to existing test modules, plus one new test module for the onboarding sequence.

## Evidence

| Claim | How it was verified |
|---|---|
| kb-vault routes the four policy kinds to the singletons | `spectra/commands/kb-vault.md:284-294` (reserved map) |
| Only methodology is protected from a kb-vault update | `kb-vault.md:332-338`; `methodology.md:209-224` |
| domain-analyzer treats any `DOMAIN_ANALYSIS.md` as a prior run | `domain-analyzer.md:93-94` |
| test-strategy and deployment-strategy draft nothing without a constitution | `test-strategy.md:631`; `deployment-strategy.md:540` |
| Both use a checkbox "Proposed constitution amendment" and a "checked items" hand-off | `test-strategy.md:645-701`; `deployment-strategy.md:572-609`; their templates (`:193`, `:158`) |
| deployment-strategy already has a `claimed` provenance for what a document says | `deployment-strategy.md:73-86` |
| deployment-strategy already reads siblings' accepted entries only | `deployment-strategy.md:171-178` |
| test-strategy reads no sibling document | `test-strategy.md:120-148` (Step 1 inputs) |
| review-pr filters only the domain analysis and methodology to `accepted` | `review-pr.md:281-291` |
| No reader outside the two commands uses `amendment_state` or the amendment heading | `grep` across `spectra/`, `tools/`, `tests/`: only the two commands, their templates, their tests, the CHANGELOG |
| test-plan and uat read `lenses:` / `ownership:` and the UAT policy, not the amendment | `test-plan.md:181-185`; `uat.md:105-106` |
| The reserved rows are pinned by tests | `tests/test_kb_vault_flow.py:57-63,341-353`; `tests/test_doc_output_paths.py:378-384` |
| The amendment format is pinned by tests | `tests/test_test_strategy_flow.py:612-619,727`; `tests/test_deployment_strategy_flow.py:296-343` |
| The extension is at 1.24.0 | `spectra/extension.yml:6`; `CHANGELOG.md` `[1.24.0]` |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | The user started specify, clarify, plan, tasks, and analyze on `036-foundation-agent-handoff`. The one spec conflict planning found (FR-024) was resolved by the user in a clarify session; the analyze remediations were applied on the user's explicit request (see Spec Reconciliation). No task edits `spec.md` |
| II. Single Self-Contained Extension | ✅ | Only existing files under `spectra/` change. No new command, folder, or dependency |
| III. Agent-Agnostic Commands | ✅ | The edits are prose rules inside existing `$ARGUMENTS` commands. No agent's question tool is named |
| IV. Context-Aware by Default | ✅ | Strengthened: feeders read imported knowledge on purpose and label it honestly. test-strategy now reads its siblings |
| V. Catalog and Package in Sync | ✅ | `extension.yml` 1.25.0, `catalog.json` (version; command count unchanged at 14), `CHANGELOG.md`, `docs/index.html`, rebuilt zip, prose in `README.md` / `spectra/README.md`. The roster is unchanged, so generated regions only need `--check` |
| VI. Two Versioned Channels | ✅ | Extension only. Root `VERSION` untouched; no tag |
| VII. Documents Under One Declared Root | ✅ | The singletons stay owned by the commands Principle VII names; kb-vault no longer writing them **removes** an existing tension. Each `-source` folder holds one artifact type, is a numbered series, and sits under the declared root. No new singleton, so no amendment |
| VIII. Overridable Templates | ✅ | Source documents resolve `<kind>-source-template`, then `kb-document-template`, through the five-layer stack. The strategy templates rename one section. The Constitution input format and front matter stay command-owned |

**Gate result**: PASS.

**Extension version classification**: MINOR, 1.24.0 → 1.25.0. Changed behaviour and output shapes. No
command, argument, flag, or singleton path is renamed or removed. Every earlier-format document is still
read, under FR-016 and FR-020.

**Post-design re-check**: unchanged, all ✅. The Phase 1 contracts add no file beyond those under Source
Code, and no dependency.

## Spec Reconciliation

Planning found one point where the spec contradicts itself. It is decided in [research.md](./research.md)
R9. **Resolved (second clarify session, 2026-10-24)**: the user chose the proposed resolution, FR-024
now says it, and the spec and plan agree. The same session confirmed FR-020a's accepted-only rule for
the strategy bodies. No task edits `spec.md`.

| # | Finding | Proposed resolution | Spec effect |
|---|---|---|---|
| C1 | **FR-024 conflicts with FR-001/FR-002.** FR-024 asks kb-vault's template list to include `engineering-methodology-template` and `deployment-strategy-template`. Once FR-001/FR-002 remove the four feeder rows from the reserved map, kb-vault uses none of the four feeder templates. They have command-owned semantics (Constitution input, frozen IDs) that a source document must not imitate | kb-vault's template list names exactly what the new reserved map uses: `adr-template`, `brd-template`, `impact-analysis-template`, `defect-rca-template`. A source document resolves `<kind>-source-template`, then `kb-document-template`. Its own list names no feeder template | FR-024 reworded: "names exactly the templates its reserved map uses, and no feeder template". User Story 5's acceptance scenario holds as written |

**`/speckit.analyze` remediations (2026-10-24), applied at the user's request:**

| Finding | Resolution | Where |
|---|---|---|
| D1 (CRITICAL, Principle V): AGENTS_LIST.md prose for kb-vault, test-strategy, and deployment-strategy would go stale | New task T042 updates the hand-written prose in AGENTS_LIST.md, and the review-pr prose and cards; T033 checks no stale phrase remains | tasks.md US4 |
| C1: domain-analyzer would read declined strategy records as constraints | domain-analyzer's sibling read becomes accepted-only, as methodology's and deployment-strategy's already are | tasks T009, T013; data-model "Sibling read" |
| I1: this section said FR-024 was still open | Marked resolved above | plan.md |
| T1: "documented intent" (spec) and `claimed` (plan) | FR-007 names the token: documented intent, cited as `claimed` | spec.md FR-007 |
| C2: FR-010's "text addressed to the agent is content" had no test | Asserted in T009–T012 | tasks.md |
| C3: changed-behaviour prose beyond three agents | Folded into T042 (review-pr, domain-analyzer, methodology prose) | tasks.md |
| U1: a checkbox-era strategy with no checked item gives review-pr no standard | Added as a spec edge case, asserted in T020, implemented in T027, checked in quickstart §4 | spec.md Edge Cases; tasks; quickstart.md |
| L2: SC-004 verified only by the manual walkthrough | T041 records each constitution clause's single source id | tasks.md T041 |
| L1, L3 | No change: L1 is the user's verbatim input; L3 is already under Dependencies | — |

## Project Structure

### Documentation (this feature)

```text
specs/036-foundation-agent-handoff/
├── spec.md
├── plan.md              # this file
├── research.md          # Phase 0: R1–R11
├── data-model.md        # Phase 1: singleton, source document, evidence, guardrail record, constitution input
├── contracts/
│   ├── handoff-behaviour.md         # numbered behaviours → FR → test
│   └── ownership-and-evidence.md    # who writes what, who reads what, how each file is recognised
├── quickstart.md        # automated checks, then manual runs
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks, not this command
```

### Source Code (repository root)

```text
spectra/
├── commands/kb-vault.md                 # four rows out of the reserved map; -source routing; refer; refuse singleton paths; template list (R9)
├── commands/domain-analyzer.md          # command: key; prior-run recognition; hand-written consent; reads -source + claimed
├── commands/methodology.md              # reads -source + claimed (it already has the command: key and consent)
├── commands/test-strategy.md            # goal; Constitution input; ts- IDs; decisions; adoption; migration; siblings; command: key; claimed
├── commands/deployment-strategy.md      # goal; Constitution input; ds- IDs; decisions; adoption; migration; command: key; -source read
├── commands/review-pr.md                # accepted-only for TEST_STRATEGY.md and DEPLOYMENT_STRATEGY.md
├── templates/test-strategy-template.md          # "Proposed constitution amendment" → "Constitution input"
├── templates/deployment-strategy-template.md    # same
├── extension.yml                        # 1.25.0
├── CHANGELOG.md                         # [1.25.0]
└── README.md                            # onboarding sequence prose; per-agent prose touched where behaviour changed
catalog.json                             # version 1.25.0
README.md                                # onboarding sequence prose
docs/index.html                          # onboarding sequence; command cards for changed agents
docs/packages/spectra.zip                # rebuilt
tests/test_kb_vault_flow.py              # reserved rows out; -source routing; referral; singleton refusal; template list
tests/test_doc_output_paths.py           # kb-vault RESERVED tuple; feeders' -source reads
tests/test_test_strategy_flow.py         # create goal; Constitution input; ts- IDs; migration; siblings; command key
tests/test_deployment_strategy_flow.py   # same, ds-
tests/test_domain_analyzer_flow.py       # command key; prior-run recognition; consent; claimed
tests/test_methodology_flow.py           # -source read; claimed
tests/test_review_pr_flow.py             # accepted-only for the two strategies
tests/test_document_templates.py         # section rename if pinned
tests/test_onboarding_sequence.py        # NEW: the three surfaces state the same sequence
```

**Structure Decision**: only existing files change, plus one new test module.

## Phase 0 — Research

See [research.md](./research.md):
- R1: the `-source` folders and their template
- R2: how kb-vault refers and refuses
- R3: how a feeder recognises its own file
- R4: the documented-intent label (`claimed`)
- R5: how feeders find imported documents
- R6: the Constitution input format for the two strategies
- R7: decisions from the approval gate
- R8: migrating the checkbox format
- R9: the FR-024 conflict
- R10: the onboarding-sequence documentation and how it stays consistent
- R11: version and changelog

## Phase 1 — Design

- [data-model.md](./data-model.md): entities, allowed values, and transitions.
- [contracts/handoff-behaviour.md](./contracts/handoff-behaviour.md): numbered behaviours, each mapped to
  an FR and to the test that pins it.
- [contracts/ownership-and-evidence.md](./contracts/ownership-and-evidence.md): the ownership and
  recognition table all six commands must agree with.
- [quickstart.md](./quickstart.md): automated checks, then manual runs in a throwaway Spec Kit project.

## Complexity Tracking

No constitution violations. Nothing to justify.
