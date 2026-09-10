# Implementation Plan: Test Strategy Agent

**Branch**: `020-test-strategy-agent` | **Date**: 2026-09-10 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/020-test-strategy-agent/spec.md`

## Summary

An eighth Spectra command, `speckit.spectra.test-strategy`, and the **fourth document agent** — after
`adr`, `brd`, and `impact`. It reads the project, classifies it greenfield or brownfield from evidence,
and writes one testing strategy to `<artifact-root>/test-strategy/TEST_STRATEGY.md` covering unit,
integration, API contract, and end-to-end testing plus a coverage floor. It then checks whether that
strategy is already in the constitution and, where it is not, drafts the amendment, takes approval, and
hands off to `/speckit-constitution`.

Five properties shape every decision below.

**It is the first singleton document agent.** `adr`, `brd`, and `impact` all produce numbered series;
this one produces exactly one file, rewritten in place. That is a deliberate deviation from Principle
VII's numbering rule and the only Constitution Check item on this plan that needs an argument rather
than a checkmark — it is argued in Complexity Tracking, not waved through.

**It is the first Spectra command to reach toward governance and stop short.** `domain-analyzer`
proposes guardrails and hands off; this one does the same for a strategy it just wrote. The
distinguishing rule is FR-032: it never writes `.specify/memory/constitution.md`, in any run, approved
or not. Approval authorises drafting and handoff, never an edit. That keeps one owner for every
constitution change — `/speckit-constitution` — and keeps the amendment procedure (sync impact report,
bump-type judgement, dependent artifacts) in the one place that already implements it.

**Its honesty rules are the product, and they are about restraint.** The failure mode of a testing-
strategy generator is a plausible document that recommends Playwright to a Python library and a 90%
floor to a repository measuring 31%. Four rules prevent it: every recommendation cites evidence or is
marked as an unevidenced convention (FR-043); no tool is named that the stack cannot run (FR-016); the
brownfield floor never exceeds the baseline (FR-022); and the baseline's provenance — measured,
reported, or unavailable — is always stated (FR-023, FR-026).

**It runs nothing by default.** Research decision R2 settles what the spec left open: the command reads
committed coverage reports and configuration, and executes a coverage run only on an explicit
confirmation, labelling the figure accordingly. This follows `flaky-test-detector`'s never-runs-anything
posture rather than diverging from it, and it keeps a foundation agent from spending twenty minutes and
an unknown amount of network on a stranger's test suite.

**Its recommendations are bounded by a knowledge cutoff, and it says so.** The command makes no network
request, so its knowledge of testing tools is frozen at whatever the host agent knows. R9 turns that
into a rule: prefer what the project's own manifests already contain, and mark any recommendation that
introduces an unfamiliar dependency as lower confidence.

The command file is the deliverable. No script and no binary ships — classification, surface detection,
root resolution, and template resolution are all expressed as prompt instructions, because that is the
only form that survives Principle III and the Markdown-only supply-chain promise.

## Technical Context

**Language/Version**: Markdown command prompt in Spec Kit's generic format; Python 3.9+ (standard
library only) for this repository's own tools and tests

**Primary Dependencies**: Spec Kit `>=0.11.0`. **No runtime tool dependency and no network.** Unlike
`create-pr` and `review-pr` this command must not gate on `git` or `gh`; like `impact` it must state
that it makes no outbound request (FR-050)

**Storage**: the target project's `<artifact-root>/test-strategy/` — exactly one Markdown document,
rewritten in place. Nothing under `.specify/`, no index, no cache, no cross-run state beyond the
document itself

**Testing**: `python3 -m unittest discover -s tests` (828 passing at baseline);
`python3 tools/generate_agent_docs.py --check`; a new `tests/test_test_strategy_flow.py`; three existing
modules gain this command (`test_doc_output_paths.py`, `test_document_templates.py`,
`test_roster_data.py`); the manual zip-install pass in `test/README.md`

**Target Platform**: every coding agent and OS Spec Kit supports. Classification, surface detection, and
file reading are prompt-expressed, so nothing depends on a shell flavour or on a named search tool

**Project Type**: Spec Kit extension command — a prompt file under `spectra/commands/`, a registered
template under `spectra/templates/`, plus the publishing surface Principle V requires

**Performance Goals**: not latency-bound. The one cost that matters is R2's: the command does not run
the project's test suite unless the user says so, because an unbidden coverage run is the single
largest amount of time a foundation agent could spend without being asked

**Constraints**: Markdown only, no scripts or binaries; agent-agnostic `$ARGUMENTS`; no network request
(FR-050); **never writes the constitution** (FR-032); never edits source, tests, test config, coverage
config, or CI (FR-047); exactly one file written per run (FR-048); no per-test findings (FR-049)

**Scale/Scope**: 1 new command file; 1 new shipped template; 2 manifest entries; 1 new roster entry; 1
catalog entry; 1 changelog entry; 1 rebuilt zip; ~4 documentation surfaces including a hand-authored
prose block; 1 new test module plus three census/registry updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `020-test-strategy-agent`; both spec markers resolved in session before planning. |
| II. A Single Self-Contained Extension | ✅ | One new file under the existing `spectra/commands/`, one under `spectra/templates/`. No new extension folder, no dependency on another extension. |
| III. Agent-Agnostic Commands | ✅ | Text only, `$ARGUMENTS` for the optional focus hint. No named search tool, no shell, no agent-specific invocation. The `/speckit-constitution` handoff is named as a command the *user* runs, not one this command invokes — see [research.md](./research.md) §6. |
| IV. Context-Aware by Default | ✅ | FR-009 to FR-013 read the constitution, specs, docs, manifests, test and coverage configuration, CI definitions, and — in brownfield — source. FR-006 makes the project's own maturity change what the strategy may assert, which is the same strength of reading `impact` established with FR-010a. |
| V. Catalog and Package in Sync | ✅ | Manifest, roster, catalog, changelog, zip, landing page, generated regions, and a new hand-authored prose block all move in the same change (FR-051, FR-052). |
| VI. Two Independently-Versioned Channels | ✅ | Extension channel only: 1.12.1 → 1.13.0. `VERSION` untouched, no tag, no Release (FR-053). |
| VII. Documents Under One Declared Root | ⚠️ | **Engaged, with one deviation.** Declared root, dedicated subfolder, one-artifact-type, and the publication check are all honoured. The `NNN-` sequence number is **not**. Argued below and recorded in Complexity Tracking. |
| VIII. Shaped by Overridable Templates | ✅ | **Engaged.** New registered `test-strategy-template`, resolved through the four-layer stack, inline skeleton last, resolved path reported (FR-038 to FR-041). |

**Amendment classification**: none *required*. This plan proposes no change to Spectra's own
constitution. The alternative that would remove the VII deviation — amending Principle VII to carve out
singleton standing-policy artifacts — is recorded in Complexity Tracking as available but not taken.

**Extension version classification**: MINOR — 1.12.1 → 1.13.0. A command is added; none is renamed or
removed, and no existing command's behaviour changes. `catalog.json` `provides.commands` goes 7 → 8 and
`provides.templates` gains a sixth entry.

### VII: the numbering deviation, argued

Principle VII is unambiguous: *"Filenames MUST carry a zero-padded three-digit sequence number scoped to
that subfolder, starting at `001`."* This command writes `TEST_STRATEGY.md`. That is a violation of a
MUST, and Governance is equally clear that a deviation must be justified in Complexity Tracking and
approved before merge. It is justified there rather than reasoned away here.

What matters for the gate is how narrow the deviation is. **Four of Principle VII's five obligations are
honoured in full**: the write target is `<artifact-root>/test-strategy/`, so the declarable root works
and a project that sets `Artifact root: documents/` gets it; the artifact takes its own sibling
subfolder rather than a new top-level folder; that subfolder holds exactly one artifact type; and the
publication check runs before defaulting into `docs/`. Only the filename differs.

**The sequence number exists to serve a property this artifact does not have.** Numbering lets
`ADR-004` supersede `ADR-002` without either losing its identity, and it is why VII also requires
reading superseded locations so a cut-over cannot produce a duplicate `001`. Both are properties of a
decision *log*. A test strategy is a standing policy with exactly one current answer — the same shape as
the constitution, which VII does not govern and does not number. Numbering it would produce a folder
where the current policy is whichever file sorts highest, which is strictly worse for the thing a reader
most needs to do.

**Nothing in the enforcement suite breaks.** `test_doc_output_paths.py` asserts the `NNN` write target
per command (`adr`, `brd`) rather than generically, and its lowercase-kebab check reads the *folder*
slug — `docs/test-strategy/` passes. The new entry in `CANONICAL` therefore adds this command to every
declared-root, publication-check, and absolute-path assertion without inheriting a numbering assertion
that was never generic. The new test module asserts the absence of a sequence number explicitly, so the
deviation is pinned rather than merely tolerated.

### VII: does "producing a document is not a licence to edit governance" forbid the amendment step?

No — and the clause anticipates exactly this case. VII says: *"the one constitution change a Spectra
command may propose is one that is about the decision it just recorded, and even that requires explicit
approval."* The amendment this command drafts is about the strategy it just wrote, and FR-031 requires
explicit approval before anything is offered onward.

The design goes further than the clause requires. VII permits a command to *propose*; this command
proposes and then still does not write, because Q2 settled the applier as `/speckit-constitution`
(FR-032). The existing enforcement assertion — every document command must contain the words `never
write it` about the artifact-root declaration — is satisfied by the same posture that satisfies FR-032,
and the new test module extends it to the constitution file itself.

### VIII: what the template may and may not shape

The document is a durable Markdown deliverable a human reads, so VIII applies in full and the structure
ships as `spectra/templates/test-strategy-template.md`. Two boundaries need recording.

**A team may delete a section, including a lens or the proposed-amendment block.** If an override drops
"API contract testing", the command notes the omission and does not reinstate it. If it drops the
proposed-amendment section, FR-036 says the amendment text goes to the session and the handoff is still
offered — the template shapes the document, not the command's obligations.

**The honesty rules are not part of the template.** The evidence-or-convention marker, the
floor-never-exceeds-baseline rule, the baseline provenance labels, the coverage-of-analysis statement,
and the greenfield/brownfield declaration stay with the command — the same division `review-pr` and
`impact` already use. An override that removed "Sources consulted" removes the section; it cannot make
the command stop knowing what it did not read, and the command still reports coverage in the session.

## Project Structure

### Documentation (this feature)

```text
specs/020-test-strategy-agent/
├── plan.md                          # This file
├── spec.md                          # 56 requirements, 5 stories, 9 clarifications
├── research.md                      # Phase 0 — the decisions behind the command's rules
├── data-model.md                    # Phase 1 — entities, document schema, state
├── quickstart.md                    # Phase 1 — how to prove it works
├── contracts/
│   ├── command-interface.md         # name, arguments, effect, refusals, write scope
│   ├── document-contract.md         # file target, section order, template resolution
│   ├── amendment-handoff.md         # the shape /speckit-constitution consumes
│   └── chat-output.md               # the summary, the gate, and the run report
├── checklists/requirements.md       # spec quality checklist (17/17)
└── tasks.md                         # Phase 2 output — NOT created by this command
```

### Source Code (repository root)

```text
spectra/
├── commands/test-strategy.md                 # NEW — the whole runtime deliverable
├── templates/test-strategy-template.md       # NEW — the document's section structure
├── extension.yml                             # + command, + template; version → 1.13.0; tags
├── CHANGELOG.md                              # [1.13.0]
└── README.md                                 # generated commands table gains a row
agents-list.json                              # NEW entry: test-strategy (foundation, add-on, available)
catalog.json                                  # version → 1.13.0, provides.commands 7 → 8, updated_at
docs/
├── index.html                                # the command's entry on the landing page
└── packages/spectra.zip                      # rebuilt with tools/build_package.py
README.md                                     # generated agents table gains a ✅ available row
AGENTS_LIST.md                                # NEW hand-authored prose block, anchored id=test-strategy
test/README.md                                # manual pass for the gate, the floor, and the singleton
tests/
├── test_test_strategy_flow.py                # NEW — the honesty rules, asserted on the text
├── test_doc_output_paths.py                  # CANONICAL gains test-strategy.md → docs/test-strategy/
├── test_document_templates.py                # COMMAND_TEMPLATE gains test-strategy-template
└── test_roster_data.py                       # census: 47 → 48 agents, 16 → 17 available, 31 planned
```

**Structure Decision**: no new top-level directory and no new module. The runtime artifacts are one
Markdown command and one Markdown template under the folders that already hold seven commands and five
templates; everything else above is the publishing surface Principle V requires to move with them.

**The two existing enforcement modules do most of the constitutional work.** `test_doc_output_paths.py`
derives its checks from a `CANONICAL` dict and `test_document_templates.py` from a `COMMAND_TEMPLATE`
dict. Adding one entry to each converts Principles VII and VIII from reviewed to enforced for this
command: declared-root resolution, the publication check, the lowercase project-relative folder, the
refusal to write the declaration, four-layer template resolution, heading parity between the shipped
template and the inline skeleton, and the absence of a hard-coded template path all become assertions.
What those modules cannot cover — the constitution write ban, the floor-versus-baseline rule, the
absence of a sequence number, and the tool-grounding rule — is what `test_test_strategy_flow.py` is for.

## Complexity Tracking

> Fill ONLY if Constitution Check has violations that must be justified

**One violation, taken deliberately, at the user's direction (spec Clarifications Q1 → A).**

| Violation | Why needed | Simpler alternative rejected because |
|---|---|---|
| **Principle VII: the filename carries no `NNN-` sequence number** (FR-042a) | A test strategy is a standing policy with exactly one current version, not a decision log. A stable path is what lets the constitution, CI, a README, and the amendment handoff all point at "the current strategy" without any of them going stale. Git carries the history that numbering would otherwise carry in filenames. | **Numbering it anyway** (`001-test-strategy.md`) satisfies the letter of VII and makes the current policy "whichever file sorts highest" — the reader's most common question becomes the hardest one, and every inbound reference breaks on the next run. **Amending Principle VII** to carve out singleton standing-policy artifacts is the durable fix and is *not rejected on the merits* — it is deferred because a governance amendment written to accommodate a single command is a principle shaped by its first exception. If a second singleton artifact ever ships, that amendment is the right change and this row is the evidence for it. |

Two further items are recorded because they are new to the roster, not because they breach anything.

| Item | Why it is needed | Why the simpler option was rejected |
|---|---|---|
| **A drafted change to the constitution, handed to another command** (FR-032a, FR-032b) | A strategy that lives only in a document is advice; in the constitution it is checked by the Constitution Check gate on every plan. That is the whole point of a foundation agent, and Principle VII explicitly permits proposing a change about the decision just recorded. | **Writing it directly** would put a second implementation of the amendment procedure — sync impact report, bump-type judgement, dependent-artifact propagation — in a command that is not about governance, and the failure mode is a subtly malformed constitution rather than an obviously broken one. **Not offering it at all** reduces the agent to a document generator and drops the requirement the user opened with. |
| **A conditional, confirmed execution of the project's coverage tool** (R2) | "Measured" and "read from a nine-month-old report" are different claims, and only one of them can be made without running something. The distinction is load-bearing for FR-022's floor cap. | **Never running anything** would make every brownfield floor rest on whatever report happens to be committed, and most projects commit none. **Running by default** would make a foundation agent spend an unbounded amount of time and possibly network on a stranger's suite, unasked — the posture `flaky-test-detector` deliberately refused. A confirmed, labelled run keeps both claims honest. |

**The write scope is the narrowest of any Spectra document agent.** `impact` writes a document, an
index, and two front-matter fields of a third file. `flaky-test-detector` edits files the user wrote.
This one writes exactly one file and touches nothing else — the constitution included, approved or not.

## Phase 0 — Research

Complete. See [research.md](./research.md): nine decisions, each with rationale and rejected
alternatives — classifying project maturity from signals rather than a line count, gating the coverage
run behind a confirmation, expressing lens boundaries without assuming a stack, detecting testable
surfaces without a build graph, deriving a floor and its ratchet from a baseline, detecting whether a
strategy is already embedded in a constitution, the shape of an amendment another command consumes,
reusing rather than re-deriving artifact-root and template resolution, and recommending tools from
behind a knowledge cutoff with no network.

## Phase 1 — Design & Contracts

Complete. [data-model.md](./data-model.md) fixes the seven entities and the document schema, including
the amendment lifecycle the command deliberately does not finish. Four contracts pin the interface, the
document, the handoff, and what the user sees in the session. [quickstart.md](./quickstart.md) gives the
runnable validation passes, including the three easiest to get wrong: a brownfield floor above the
baseline, a browser driver recommended to a project with no browser, and a run that touches the
constitution.

## Post-Design Constitution Re-Check

Re-run after Phase 1. No status changed; the VII deviation is unchanged in scope and now pinned by a
contract and a test.

| Principle | Post-design finding |
|---|---|
| II | Phase 1 added four contract documents and one shipped asset — the template VIII requires. The extension is still one folder, one manifest: eight commands, six templates. |
| III | The contracts are written as capability statements. `contracts/command-interface.md` names the argument in generic form; the only command named anywhere is `/speckit-constitution`, and `contracts/amendment-handoff.md` records it as something the *user* runs, so no invocation is hard-coded into a code path. |
| IV | Design deepened it: `data-model.md` makes the classification and each surface first-class recorded fields, so the project's own maturity is visible in the output rather than implicit in the tone. |
| V | The file list above is the sync obligation, enumerated. `tasks.md` will order it so the zip is rebuilt after the manifest, and the generated regions after the roster. |
| VI | Unchanged — extension channel only. Nothing in Phase 1 touched `VERSION` or `spectra_cli/`. |
| VII | **Deviation unchanged and now bounded by a contract.** `document-contract.md` states the single write target `<artifact-root>/test-strategy/TEST_STRATEGY.md`, states that no other file is ever written, and states the absence of the sequence number as an explicit property with its justification. The `test_doc_output_paths.py` entry asserts the root, subfolder, and publication-check obligations that *are* kept. |
| VIII | Confirmed by design: the template ships with the section structure only; the honesty rules stay in the command, and `document-contract.md` records which sections an override may drop — including the proposed-amendment block — and what the command still does when it does. |
