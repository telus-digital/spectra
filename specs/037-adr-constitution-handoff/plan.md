# Implementation Plan: The ADR Agent Hands Off to the Constitution

**Branch**: `037-adr-constitution-handoff` | **Date**: 2026-10-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/037-adr-constitution-handoff/spec.md`

## Summary

`speckit.spectra.adr` becomes the fifth constitution feeder, on the contract the other four already follow.
No agent is added; the ADR's significance test, numbering, location, and template resolution are unchanged.

1. **Step 7 stops editing the constitution.** It still decides whether the decision is significant. When it
   is, it reads the constitution semantically, drafts guardrails as records with frozen `adr-NNN-` IDs, and
   puts them to the user at one approval step with the same five outcomes the siblings use.
2. **The ADR carries the outcome.** Two command-owned sections are appended to the ADR the agent wrote in
   Step 6: **Constitution guardrails** (every record offered, with its decision) and **Constitution input**
   (only the accepted, not-yet-adopted records). A non-significant ADR gets neither.
3. **The handoff is a printed line.** With a constitution and at least one accepted record, the agent prints
   one `/speckit-constitution` amend line naming the ADR's resolved path. With no constitution, it prints no
   line, points to `speckit.spectra.domain-analyzer`, and says the records wait in the ADR for a later amend.
4. **Sibling ground is referred.** The ADR agent drafts only on its own ground: architecture-level choices.
   Testing, deployment, languages / frameworks / dependency policy, the domain, and methodology are named,
   checked for an existing document, and referred.
5. **The map is updated on both sides.** methodology's sibling-ground table gains an ADR row and counts five
   feeders; domain-analyzer states the technology split and cites accepted ADR records before drafting on
   architecture ground (see Spec Reconciliation C1).
6. **Step 8** stops suggesting the constitution file be committed.

The extension goes from 1.25.0 to 1.26.0. No constitution amendment is needed.

## Technical Context

**Language/Version**: Markdown command prompts and templates; Python 3.9+ for tests and tooling

**Primary Dependencies**: none. Standard library only; the zero-dependency rule covers the whole repository

**Storage**: Markdown files in the consumer's project — ADRs under `<artifact-root>/adr/`, gaining two
command-owned sections when significant

**Testing**:
- `python3 -m unittest discover -s tests`
- `python3 tools/generate_agent_docs.py --check`
- `python3 tools/build_package.py`
- `python3 tools/ship.py --dry-run`

**Target Platform**: any Spec Kit agent, in slash-command or skills mode

**Project Type**: Spec Kit extension (Markdown commands), catalog channel only

**Performance Goals**: no change. The ADR agent keeps its five-question limit; the approval step is one
question asked after the ADR is written and does not count against it

**Constraints**:
- Markdown only; no scripts in the package.
- Agent-agnostic; no agent's question tool is named.
- The ADR agent writes the ADR (and, on supersession, the superseded ADR's status line) and nothing else.
- It never writes `.specify/memory/constitution.md` and never invokes `/speckit-constitution`.
- No network access.
- ADRs written before 1.26.0 stay valid: they carry no Constitution sections and nothing reads them as
  missing one.

**Scale/Scope**:
- Edits to three commands: `adr` (Steps 7 and 8, a never-list, a ground statement), `methodology`
  (sibling-ground table, feeder count), `domain-analyzer` (technology split, ADR citation in Lens 4/5).
- No template change (research R4).
- The usual version sync and prose updates for the three agents.
- One new test module (`tests/test_adr_flow.py`) and additions to two existing ones.

## Evidence

| Claim | How it was verified |
|---|---|
| ADR Step 7 edits the constitution on the user's agreement | `spectra/commands/adr.md:191-207` |
| ADR Step 8 suggests staging the constitution file | `adr.md:209-222` |
| The ADR is written in Step 6, before Step 7 runs | `adr.md:150-189` |
| ADR Step 1 already forbids editing the constitution for the artifact root | `adr.md:51-53` |
| The siblings' never-write invariant and its reason | `test-strategy.md:48`, `:796-805`; `domain-analyzer.md:46-47`; `methodology.md:53-54` |
| The record, Constitution input, gate, and handoff formats | `test-strategy.md:701-835` |
| A command writes its Constitution input section even where the template omits it | `domain-analyzer.md:382-384`; `test-strategy.md:762-764` |
| methodology's sibling-ground table and "Four agents feed the constitution" | `methodology.md:264-275` |
| methodology's ordered feeder list after its handoff | `methodology.md:705-713` |
| domain-analyzer Lens 4 already covers layering, module boundaries, integrations | `domain-analyzer.md:229` |
| domain-analyzer Lens 5 covers languages, frameworks, runtimes, dependency policy | `domain-analyzer.md:230` |
| All four feeders read ADRs as evidence | `domain-analyzer.md:112`; `methodology.md:138`; `test-strategy.md:200`; `deployment-strategy.md:174` |
| methodology's sibling-ground owners are pinned by a test | `tests/test_methodology_flow.py:370-389` |
| No test pins ADR Step 7's current wording | `grep` over `tests/`: ADR is asserted only for paths and templates (`test_doc_output_paths.py`, `test_document_templates.py`) |
| The extension is at 1.25.0 and that version is on `main` | `spectra/extension.yml:6`; `catalog.json:13`; `git log` (`1be7750`) |

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | The user started specify and plan on `037-adr-constitution-handoff`; both clarifications were answered by the user. The one spec conflict found in planning (C1) was settled by the user in a clarify session (see Spec Reconciliation). No task edits `spec.md` |
| II. Single Self-Contained Extension | ✅ | Only existing files under `spectra/` change. No new command, folder, or dependency |
| III. Agent-Agnostic Commands | ✅ | Prose rules inside existing `$ARGUMENTS` commands. The approval step names choices, not a tool |
| IV. Context-Aware by Default | ✅ | Strengthened: the ADR agent reads sibling documents' accepted records before drafting |
| V. Catalog and Package in Sync | ✅ | `extension.yml` 1.26.0, `catalog.json` version (command count unchanged), `CHANGELOG.md`, rebuilt zip, `docs/index.html` ADR and domain-analyzer cards, hand-written prose in `AGENTS_LIST.md` for the three agents. The roster is unchanged, so generated regions only need `--check` |
| VI. Two Versioned Channels | ✅ | Extension only. Root `VERSION` untouched; no tag |
| VII. Documents Under One Declared Root | ✅ | The ADR stays in `<artifact-root>/adr/`, one file per decision. The agent writes no new file; the Constitution sections live inside the ADR. No new singleton |
| VIII. Overridable Templates | ✅ | The template is still honoured and not repaired. The two Constitution sections are command-owned, appended after the template's sections, exactly as `domain-analyzer` already does for its Constitution input |

**Gate result**: PASS.

**Extension version classification**: MINOR, 1.25.0 → 1.26.0. Changed behaviour and a new output section;
no command, argument, or path is renamed or removed.

**Post-design re-check**: unchanged, all ✅. The contract adds no file beyond those under Source Code.

## Spec Reconciliation

Planning found one point where the spec, as clarified, collides with an existing agent. It is analysed in
[research.md](./research.md) R2. **Resolved (clarify session, 2026-10-24)**: the user chose the proposed
resolution; FR-019, an edge case, and the Sibling ground entity now say it, and the spec and plan agree.

| # | Finding | Proposed resolution | Spec effect |
|---|---|---|---|
| C1 | **FR-010 overlaps domain-analyzer Lens 4.** Q1's answer gives the ADR agent "service and data boundaries, layering, integration patterns". domain-analyzer's Lens 4 *Architecture & boundaries* already covers "layering, module boundaries and dependency direction, public interfaces, external integrations" and feeds Core Principles. Two agents drafting on the same ground breaks one source per clause | **A recorded decision outranks an inference, clause by clause.** The ADR agent owns architecture-level choices *as decided* (FR-010 unchanged). domain-analyzer keeps Lens 4 for the structure it *observes*, but before drafting there it reads accepted Constitution input records in `<artifact-root>/adr/` and cites them instead of drafting a clause they cover. Whichever agent reaches a clause first is its source; the other cites it, and a later ADR that changes it drafts an `amends:` record (FR-005/FR-006) | FR-019 gains one sentence: domain-analyzer cites accepted ADR records on Lens 4 ground and drafts only what none covers. FR-010 unchanged |

**`/speckit.analyze` remediations (2026-10-24), applied at the user's request:**

| Finding | Resolution | Where |
|---|---|---|
| U1 (HIGH): the clause-by-clause rule covered only Lens 4; an ADR can also land on domain-analyzer's Data sensitivity, Security & trust boundaries, or Reliability & operability lenses | The rule extends to every domain-analyzer lens except Technology & dependency policy, which stays exclusive. The ADR agent's ground adds architectural decisions on security, data handling, or reliability | spec FR-010, FR-019, Key Entities, Edge Cases; research R2; tasks T009–T012 |
| U2: guardrails from a `Superseded` or `Deprecated` ADR could still constrain either agent | Only ADRs whose status is `Proposed` or `Accepted` count; a superseded ADR's records serve only to find the principle a supersession amends | spec FR-009, FR-019, Edge Cases; tasks T009–T012 |
| I1: test strings in T004/T009 did not match the wording T005/T006/T011 prescribe | Assertions aligned to the prescribed sentences; T006 now quotes the three goal lines exactly | tasks T004, T006, T009 |

Rejected alternative: narrowing the ADR agent to datastores, messaging, and architecture style and leaving all
boundary rules to domain-analyzer. That leaves an architect who decides "every service owns its data store"
in an ADR with no route to the constitution except re-running a seven-question analysis — the spec's own
User Story 1 example.

## Project Structure

### Documentation (this feature)

```text
specs/037-adr-constitution-handoff/
├── spec.md
├── plan.md              # this file
├── research.md          # Phase 0: R1–R8
├── data-model.md        # Phase 1: guardrail record, the two sections, the check result, goal states
├── contracts/
│   └── handoff-behaviour.md   # numbered behaviours → FR → test
├── quickstart.md        # automated checks, then manual runs
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks, not this command
```

### Source Code (repository root)

```text
spectra/
├── commands/adr.md              # never-list; own ground; Step 7 rewritten (check, draft, gate, sections, handoff); Step 8
├── commands/methodology.md      # sibling-ground row for adr; "Five agents"; ordered list unchanged
├── commands/domain-analyzer.md  # Lens 4/5 split; read accepted ADR records; cite before drafting
├── extension.yml                # 1.26.0; adr description mentions the handoff
├── CHANGELOG.md                 # [1.26.0]
catalog.json                     # version 1.26.0
AGENTS_LIST.md                   # hand-written prose: adr, domain-analyzer, methodology
docs/index.html                  # adr and domain-analyzer cards
docs/packages/spectra.zip        # rebuilt
tests/test_adr_flow.py           # NEW: invariant, records, gate, sections, handoff, ground, no-constitution, Step 8
tests/test_methodology_flow.py   # OWNERS gains adr; feeder count; adr not in the ordered list
tests/test_domain_analyzer_flow.py  # split stated; ADR records read and cited
```

**Structure Decision**: only existing files change, plus one new test module.

## Phase 0 — Research

See [research.md](./research.md):
- R1: where in the ADR flow the gate runs, and how the sections reach the file
- R2: the ground split with domain-analyzer (C1)
- R3: the record ID
- R4: the two command-owned sections, and why the template does not change
- R5: the goal states, including no constitution
- R6: a `Proposed` ADR
- R7: wording of the handoff line
- R8: version, changelog, and prose

## Phase 1 — Design

- [data-model.md](./data-model.md): the record, the two sections, check results, and goal states.
- [contracts/handoff-behaviour.md](./contracts/handoff-behaviour.md): numbered behaviours, each mapped to an FR
  and the test that pins it.
- [quickstart.md](./quickstart.md): automated checks, then manual runs in a throwaway Spec Kit project.

## Complexity Tracking

No constitution violations. Nothing to justify.
