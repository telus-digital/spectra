# Implementation Plan: Test Plan Agent

**Branch**: `021-test-plan-agent` | **Date**: 2026-09-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/021-test-plan-agent/spec.md`

## Summary

A ninth Spectra command, `speckit.spectra.test-plan`, and the **fifth document agent** — after `adr`,
`brd`, `impact`, and `test-strategy`. It takes a required path to a `spec.md`, reads that specification
along with the constitution, the project's test strategy, the existing suite, and the source the feature
touches, and writes one `test-plan.md` beside the specification: scope, risks, traceable test conditions,
environment and data, and exit criteria. Stakeholders approve it; `/speckit-plan` then consumes it.

Five properties shape every decision below.

**It is the first Spectra deliverable written outside the artifact root.** Every document agent so far
resolves `<artifact-root>/<artifact>/` and numbers its output. This one writes to a path it is *given* —
the directory of the spec it was handed. That is Principle VII's Spec Kit carve-out doing its job, but
the carve-out is written for *context* files and this document is also a human deliverable, so the fit
is a reasoned reading rather than an automatic one. It is the single Constitution Check item on this plan
that needs an argument instead of a checkmark, and it is argued in Complexity Tracking.

**It is the first Spectra command with a hard-required argument.** `impact` stops without its intent
paragraph, but everything else runs on empty input. This one stops *and refuses to infer* — no branch
name, no `.specify/feature.json`, no most-recently-modified heuristic (FR-007 to FR-009). The reason is
asymmetric cost: the output gets circulated and signed, and a plan generated against the wrong spec is
undetectably wrong to the person asked to approve it. Spec 017 taught the workflow to find a spec
without a feature record; this command deliberately does not use that.

**It is the first Spectra command to treat another Spectra agent's output as authority.** It reads
`speckit.spectra.test-strategy`'s document and takes its lens names verbatim, so the two artifacts can be
read against each other (FR-035). The precedence is fixed and stated: constitution, then strategy, then
the agent's own judgement, with conflicts reported rather than resolved (FR-013).

**Its central invariant is bidirectional traceability, and it is the product.** Every acceptance
criterion reaches at least one condition; every condition names what it verifies (FR-023, FR-024). Where
that is impossible — an unresolved `[NEEDS CLARIFICATION]`, a requirement too vague to test — the gap is
named and the missing decision is *never invented* (FR-026, FR-027). A fabricated condition for an
ambiguous requirement is the worst available failure here, because it launders a guess into something a
stakeholder signs.

**Its most unusual rule is a negative one: no checkboxes, anywhere.** The attached template in the
description renders exit criteria as a checklist; the shipped template will not (FR-041). This is the
rare prompt rule that is fully testable on the artifacts that ship — a regex over the template and the
inline skeleton pins it — and it exists because an approved, circulated document containing live
checkboxes creates a second apparent source of truth about progress that will disagree with `tasks.md`.

The command file is the deliverable. No script and no binary ships: argument resolution, strategy
lookup, level assignment, coverage detection, and template resolution are all prompt instructions,
because that is the only form that survives Principle III and the Markdown-only supply chain.

## Technical Context

**Language/Version**: Markdown command prompt in Spec Kit's generic format; Python 3.9+ (standard library
only) for this repository's own tools and tests

**Primary Dependencies**: Spec Kit `>=0.11.0`. **No runtime tool dependency and no network.** Like
`impact` and `test-strategy`, and unlike `create-pr` and `review-pr`, it must not gate on `git` or `gh`
and must state that it makes no outbound request (FR-020a)

**Storage**: the directory of the specification it was handed — exactly one Markdown file,
`test-plan.md`, rewritten in place on confirmation. Nothing under `.specify/`, no artifact root, no
index, no cache, no cross-run state beyond the document itself

**Testing**: `python3 -m unittest discover -s tests` (**884 passing at baseline**);
`python3 tools/generate_agent_docs.py --check` (48 agents, 8 prose blocks at baseline); a new
`tests/test_test_plan_flow.py`; two existing modules gain this command
(`test_document_templates.py`, `test_roster_data.py`); `test_doc_output_paths.py` gains a **negative**
assertion rather than a `CANONICAL` entry — see the note under Project Structure; the manual zip-install
pass in `test/README.md`

**Target Platform**: every coding agent and OS Spec Kit supports. Path resolution, strategy lookup, and
coverage detection are prompt-expressed, so nothing depends on a shell flavour or a named search tool

**Project Type**: Spec Kit extension command — a prompt file under `spectra/commands/`, a registered
template under `spectra/templates/`, plus the publishing surface Principle V requires

**Performance Goals**: not latency-bound, and one cost is explicitly refused: the command never runs the
project's test suite. Existing coverage is established by reading test source, which is the same posture
`flaky-test-detector` took and the opposite of `test-strategy`'s confirmed coverage run — this command
has no baseline number to label, so it has nothing to gain from executing anything

**Constraints**: Markdown only, no scripts or binaries; agent-agnostic `$ARGUMENTS`; a **required**
argument with no inference (FR-008); no network request (FR-020a); exactly one file written per run and
the input specification never modified (FR-018); no test code, test config, coverage config, or CI
written (FR-020); no checkbox and no tracking field in the output (FR-041, FR-042); no core Spec Kit
command edited and no hook registered (FR-005)

**Scale/Scope**: 1 new command file; 1 new shipped template; 2 manifest entries; 1 new roster entry; 1
catalog entry; 1 changelog entry; 1 rebuilt zip; ~4 documentation surfaces including a hand-authored
prose block; 1 new test module plus two census/registry updates and one negative assertion

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `021-test-plan-agent`; the spec carries no unresolved markers and its checklist passed 16/16 in one iteration. |
| II. A Single Self-Contained Extension | ✅ | One new file under the existing `spectra/commands/`, one under `spectra/templates/`. No new extension folder; no dependency on another extension — reading `test-strategy`'s output is reading a file in the user's project, not an extension dependency (FR-014 keeps the run useful when it is absent). |
| III. Agent-Agnostic Commands | ✅ | Text only, `$ARGUMENTS` for the required spec path. No named search tool, no shell, no agent-specific syntax. `/speckit-plan` and `/speckit-clarify` are named as commands the **user** runs — the same posture `test-strategy` uses for `/speckit-constitution` — and FR-048 forbids invoking either. |
| IV. Context-Aware by Default | ✅ | The strongest instance on the roster. FR-011 to FR-017 read the specification, constitution, strategy document, test suite, manifests, CI definitions, and the touched source; FR-029 and FR-035 make the project's own tests and its own lens vocabulary change the output. FR-017 forbids asking what the repository answers. |
| V. Catalog and Package in Sync | ✅ | Manifest, roster, catalog, changelog, zip, landing page, generated regions, and a new hand-authored prose block all move in the same change (FR-058 to FR-063). |
| VI. Two Independently-Versioned Channels | ✅ | Extension channel only: 1.13.0 → 1.14.0. `VERSION` untouched, no tag, no Release. |
| VII. Documents Under One Declared Root | ⚠️ | **Engaged through its carve-out, with one reasoned reading.** The output is not an artifact-root document at all: it is written beside the specification it was handed, per FR-021. Argued below and recorded in Complexity Tracking per FR-021a. The command still resolves a declared root — **read-only**, to find the strategy document. |
| VIII. Shaped by Overridable Templates | ✅ | **Engaged in full.** New registered `test-plan-template`, resolved through the four-layer stack, inline skeleton last, resolved path reported (FR-053 to FR-057). |

**Amendment classification**: none *required*. This plan proposes no change to Spectra's own
constitution. The alternative that would make Principle VII's carve-out explicitly cover
stakeholder-facing per-feature artifacts is recorded in Complexity Tracking as available but not taken.

**Extension version classification**: MINOR — 1.13.0 → 1.14.0. A command is added; none is renamed or
removed, and no existing command's behaviour changes. `catalog.json` `provides.commands` goes 8 → 9 and
`provides.templates` gains a seventh entry.

### VII: why the output is not an artifact-root document, argued

Principle VII governs commands producing "a durable Markdown **deliverable** for the user's project" and
sends each to `<artifact-root>/<artifact>/NNN-<name>.md`. It then carves out Spec Kit's own locations:

> *"`.specify/` … and `specs/` belong to Spec Kit, and a command writing there … is writing **context**
> for another command to consume, not a deliverable for a human to read. The rule governs deliverables."*

**The carve-out plainly covers the second half of what this document is for.** `/speckit-plan` consumes
it (FR-047); that is the description's stated purpose and it is exactly the relationship
`domain-analyzer` has with `.specify/memory/domain-analysis.md`. The placement also matches everything
else in a feature directory: `spec.md`, `plan.md`, and `tasks.md` are all read by humans *and* by
commands, all unnumbered, all identified by the directory they sit in rather than by a sequence number.

**Where the fit is imperfect is the first half.** This document is explicitly written to be circulated
and approved by stakeholders, so it *is* a deliverable a human reads, and the carve-out's rationale
speaks of context rather than deliverables. Reading the carve-out as location-scoped — `specs/` is
outside the rule, whatever the file is for — is the reading this plan takes, and it is the only reading
that lets the user's stated requirement be met at all. But it is a reading, so FR-021a makes it visible
in Complexity Tracking rather than letting a ✅ imply the question never arose.

**What the alternative would cost.** Filing the plan at `<artifact-root>/test-plan/NNN-<feature>.md`
satisfies VII literally and breaks the thing that makes the artifact work: a test plan is *about one
feature*, and severing it from that feature's directory means a reader holding `spec.md` cannot find its
plan, `/speckit-plan` must be told a path that has no relationship to the spec it was given, and the
sequence number becomes a second, competing identity for a feature that already has one. The number
would carry no information the directory name does not already carry.

**Four of VII's obligations are simply not engaged**, rather than waived: there is no artifact root to
resolve for the output, so no subfolder, no one-artifact-type rule, no publication check, and no
superseded-location reading applies. FR-022 supplies the guard that replaces them — the resolved
specification must lie inside the project the command was invoked in, or the run stops rather than
writing outside it. That is the write-scope promise VII exists to protect, enforced against a supplied
path instead of a resolved root.

### VII: the declared root is still read, for a different purpose

The command resolves `Artifact root:` (FR-012), but only to **find** `TEST_STRATEGY.md`. This is the
first read-only use of the declaration, and three obligations that attach to *writing* there do not
attach here: there is no publication check (nothing is written to `docs/`), no recommendation of
`documents/`, and no offer of the declaration line. An unusable declared value is reported and the
default is used, and the output destination is unaffected either way.

This matters for the enforcement suite. `tests/test_doc_output_paths.py` keys its declared-root
assertions to `DOCUMENT_COMMANDS = tuple(CANONICAL)`, and every one of them — `never write it`, the six
publication signals, the `documents/` fallback — describes a command that *writes* to the artifact root.
Adding `test-plan.md` to `CANONICAL` would therefore demand three clauses that would be false in this
command, and would assert a write target it does not have. The entry is deliberately **not** added, and
Phase 1 replaces it with a negative assertion so that its absence is pinned rather than merely true.

### VIII: what the template may and may not shape

The document is a durable Markdown deliverable a human reads, so VIII applies in full and the structure
ships as `spectra/templates/test-plan-template.md`. Three boundaries need recording.

**A team may delete a section.** If an override drops the risk table, the command notes the omission and
does not reinstate it (FR-055).

**A team may not reintroduce a checkbox.** This is the one place where the command overrides the
template's *content* rather than merely declining to extend it: FR-041 requires a checkbox construct in
any resolved layer to be rendered as a plain statement instead. The justification is that the
no-checkbox rule is a property of the artifact's purpose — an approval document, not a tracker — and
Principle VIII's own division puts the rules that make output trustworthy in the command. An override
that wants checkboxes is asking for a different artifact, and `tasks.md` already is one.

**The authoring guidance stays in the template and never reaches the output** (FR-044). The optional-
section table tells the *editor of an override* when a section is warranted; emitting it into a document
a stakeholder is asked to approve would be instructing them to author sections nobody asked them for.

## Project Structure

### Documentation (this feature)

```text
specs/021-test-plan-agent/
├── plan.md                          # This file
├── spec.md                          # 66 requirements, 6 stories, 12 clarifications
├── research.md                      # Phase 0 — the decisions behind the command's rules
├── data-model.md                    # Phase 1 — entities, document schema, run states
├── quickstart.md                    # Phase 1 — how to prove it works
├── contracts/
│   ├── command-interface.md         # name, the required argument, effect, refusals, write scope
│   ├── document-contract.md         # write target, section order, template resolution, no-checkbox
│   ├── traceability-contract.md     # the acceptance-criterion ↔ condition invariant
│   ├── plan-handoff.md              # the shape /speckit-plan consumes
│   └── chat-output.md               # the gates, the report, and the refusals
├── checklists/requirements.md       # spec quality checklist (16/16)
└── tasks.md                         # Phase 2 output — NOT created by this command
```

### Source Code (repository root)

```text
spectra/
├── commands/test-plan.md                     # NEW — the whole runtime deliverable
├── templates/test-plan-template.md           # NEW — the document's section structure
├── extension.yml                             # + command, + template; version → 1.14.0; tags
├── CHANGELOG.md                              # [1.14.0]
└── README.md                                 # generated commands table gains a row
agents-list.json                              # NEW entry: test-plan (requirements-discovery, add-on)
catalog.json                                  # version → 1.14.0, provides.commands 8 → 9, updated_at
docs/
├── index.html                                # the command's entry on the landing page
└── packages/spectra.zip                      # rebuilt with tools/build_package.py
README.md                                     # generated agents table gains a ✅ available row
AGENTS_LIST.md                                # NEW hand-authored prose block, anchored id=test-plan
test/README.md                                # manual pass for the argument gate and the traceability
tests/
├── test_test_plan_flow.py                    # NEW — the argument gate, traceability, no-checkbox
├── test_document_templates.py                # DOCUMENT_COMMANDS gains test-plan.md → test-plan-template
├── test_doc_output_paths.py                  # NEW negative assertion; CANONICAL deliberately unchanged
└── test_roster_data.py                       # census: 48 → 49 agents, 17 → 18 available, 31 planned
```

**Structure Decision**: no new top-level directory and no new module. The runtime artifacts are one
Markdown command and one Markdown template under the folders that already hold eight commands and six
templates; everything else above is the publishing surface Principle V requires to move with them.

**One existing enforcement module does most of the Principle VIII work.**
`tests/test_document_templates.py` derives its checks from a `DOCUMENT_COMMANDS` dict. Adding
`"test-plan.md": "test-plan-template"` converts VIII from reviewed to enforced for this command:
registration in the manifest, four-layer resolution named in full, no hard-coded template path, heading
parity between the shipped template and the command's inline skeleton, and no executable asset.

**Principle VII's module is the interesting one, and it moves in the opposite direction.**
`tests/test_doc_output_paths.py` must **not** gain a `CANONICAL` entry, for the reasons argued above.
Five of its assertions already sweep every command file and will apply to `test-plan.md` unchanged —
no write instruction beside a legacy folder, no legacy path outside a legacy clause, no absolute output
path, and every `docs/<slug>/` reference lowercase-kebab. The command will reference
`docs/test-strategy/` when it explains where it looks for the strategy, which satisfies the slug rule
and is the first time one command names another's canonical folder; the absolute-path assertion is the
one an author can trip by writing a leading slash, so the template and command text must keep every
path project-relative. What the module cannot cover — that the write target is the supplied spec's
directory, that `CANONICAL` is deliberately not extended, and that the declared root is read but never
written to — is what the new negative assertion and `test_test_plan_flow.py` are for.

## Complexity Tracking

> Fill ONLY if Constitution Check has violations that must be justified

**One item, taken deliberately, at the user's explicit direction (spec Clarifications Q1 → A).**

| Violation | Why needed | Simpler alternative rejected because |
|---|---|---|
| **Principle VII: the deliverable is written to `specs/<feature>/test-plan.md` rather than `<artifact-root>/test-plan/NNN-<name>.md`** (FR-021, FR-021a) | The artifact is *about one feature* and is consumed by `/speckit-plan`, which is precisely the relationship VII's `specs/` carve-out describes. Its identity is the feature directory, exactly as `spec.md`, `plan.md`, and `tasks.md` have no sequence number because the directory already supplies one. Co-location is what makes it findable by the person holding the spec and passable to the planner. | **Filing it under the artifact root with a number** satisfies VII literally and severs the plan from its feature: a reader with `spec.md` cannot find its test plan, the number becomes a second competing identity, and a re-run after `/speckit-clarify` either overwrites a numbered file (defeating the numbering) or accumulates `001`, `002`, `003` for one feature with no way to tell which is current. **Amending Principle VII** so the carve-out explicitly covers stakeholder-facing per-feature artifacts is the durable fix and is *not rejected on the merits* — it is deferred because the existing carve-out already places `specs/` outside the rule, so the amendment would clarify a rationale rather than change an obligation. If a second per-feature deliverable ships, that amendment is the right change and this row is the evidence for it. |

Three further items are recorded because they are new to the roster, not because they breach anything.

| Item | Why it is needed | Why the simpler option was rejected |
|---|---|---|
| **A required argument with inference explicitly refused** (FR-007 to FR-009) | The output is circulated and approved. A plan silently generated against the wrong specification reads as authoritative and is undetectably wrong to a stakeholder, who has no way to notice that the conditions describe a different feature. | **Inferring from the branch or `.specify/feature.json`** is what spec 017 built for the rest of the workflow and is right there — but it is right for commands whose output is a task list a developer immediately reads. Here the cost of a wrong guess is a signed document. **Offering a picker over `specs/`** was rejected as a second-order version of the same problem: it still asks the user to choose from a list the command assembled, and one wrong keystroke produces the same artifact. |
| **A command that overrides its own template's content in one specific way** (FR-041) | The no-checkbox rule is a property of what the artifact *is* — an approval document rather than a tracker. Principle VIII puts the rules that make output trustworthy in the command, not the template. | **Honouring a checkbox an override reintroduces** would let a template turn the document into a second progress tracker competing with `tasks.md`, which is the failure the rule exists to prevent. **Refusing to run on such an override** would be worse: it makes a formatting choice fatal. Rendering the criterion as a plain statement keeps the team's section and drops only the construct. |
| **Reading another Spectra agent's output as authority** (FR-013, FR-035) | A test plan whose level names disagree with the project's own test strategy forces a reviewer to adjudicate between two documents that both claim to be policy. | **Ignoring the strategy** and always using a fixed vocabulary is simpler and reproduces exactly that conflict. **Depending on the strategy** — refusing to run without one — was rejected because it makes an optional add-on into a prerequisite chain; FR-014 keeps the run useful when it is absent. |

**The write scope ties `test-strategy` for the narrowest on the roster**, and is narrower in one respect:
one file, and *not even the constitution is drafted*. `test-strategy` writes one file and proposes an
amendment; this one writes one file and proposes a command invocation.

## Phase 0 — Research

Complete. See [research.md](./research.md): twelve decisions, each with rationale and rejected
alternatives — resolving the required argument and deciding what counts as usable as a specification,
where the no-checkbox rule is enforced given that runtime output cannot be tested, expressing
traceability without renumbering the spec, resolving the level vocabulary, locating the strategy
document without re-implementing artifact-root logic that does not apply, the shape of the
`/speckit-plan` handoff, keeping the risk table a decision rather than an inventory, deriving condition
priority from the spec's own story priorities, detecting existing coverage by reading tests rather than
running them, re-run and non-interactive semantics, filling "build under test" without inventing a
version, and which optional sections may be added and on what trigger.

## Phase 1 — Design & Contracts

Complete. [data-model.md](./data-model.md) fixes the eleven entities, the document schema, and the run
states including the two gates. Five contracts pin the interface, the document, the traceability
invariant, the handoff, and what the user sees in the session. [quickstart.md](./quickstart.md) gives the
runnable validation passes, including the four easiest to get wrong: an empty invocation that analyzes
the project anyway, an acceptance criterion that reaches no condition, a checkbox surviving into the
output, and a browser level assigned to a project with no browser.

## Post-Design Constitution Re-Check

Re-run after Phase 1. No status changed; the VII reading is unchanged in scope and now pinned by a
contract and two tests.

| Principle | Post-design finding |
|---|---|
| II | Phase 1 added five contract documents and one shipped asset — the template VIII requires. The extension is still one folder, one manifest: nine commands, seven templates. |
| III | The contracts are written as capability statements. `contracts/command-interface.md` names the argument in generic form; `contracts/plan-handoff.md` records `/speckit-plan` as something the **user** runs and fixes the handoff as printed text, so no invocation is hard-coded into a code path. |
| IV | Design deepened it: `data-model.md` makes the resolved level vocabulary, the strategy's provenance, and the existing-coverage citation first-class recorded fields, so what the command inherited from the project is visible in the output rather than implicit in the tone. |
| V | The file list above is the sync obligation, enumerated. `tasks.md` will order it so the zip is rebuilt after the manifest, and the generated regions after the roster. |
| VI | Unchanged — extension channel only. Nothing in Phase 1 touched `VERSION` or `spectra_cli/`. |
| VII | **Reading unchanged and now bounded by a contract.** `document-contract.md` states the single write target as the supplied specification's directory, states the in-project guard of FR-022, states that no artifact root is resolved for output, and states the read-only use of the declaration for strategy lookup. The negative assertion in `test_doc_output_paths.py` pins `CANONICAL`'s deliberate omission, so a future maintainer adding this command to it fails a test that explains why. |
| VIII | Confirmed by design: the template ships the section structure only; the traceability invariant, the no-checkbox rule, the cited-absence rule, the secret prohibition, and the coverage statement stay in the command, and `document-contract.md` records which sections an override may drop and what the command still does when it does. |
