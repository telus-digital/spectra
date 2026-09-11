# Implementation Plan: Defect Root Cause Analysis Agent

**Branch**: `022-defect-rca-agent` | **Date**: 2026-09-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/022-defect-rca-agent/spec.md`

## Summary

A tenth Spectra command, `speckit.spectra.defect-rca`, and the **sixth document agent** — after `adr`,
`brd`, `impact`, `test-strategy`, and `test-plan`. It takes a defect through one of three channels — a
JIRA reference, a GitHub issue URL, or a plain description — reads the constitution, searches the prior
RCA corpus for a recurrence, traces the implicated code, commits, configuration and tests, runs a
hypothesis-driven loop that asks the human only for what the repository cannot yield, and writes one
`NNN-<slug>.md` into `<artifact-root>/defect-rca/` with an index row beside it.

Six properties shape every decision below.

**It is the closest sibling `impact` has, and deliberately so.** Artifact root resolved per run,
publication check before defaulting, three-digit sequence scoped to the folder, write-once-at-the-end,
a rebuilt `README.md` index, secrets located rather than quoted, and a stated non-interactive mode.
Every one of those is a solved problem in `spectra/commands/impact.md`, and this plan reuses the
solution rather than reinventing it. Where the two differ is the subject: `impact` reasons forward from
a proposed change, this one reasons backward from an observed failure.

**It is the first Spectra command that degrades on a tool instead of gating on it.** `create-pr` and
`review-pr` hard-gate on `gh` — no binary, no run. `impact`, `test-strategy` and `test-plan` make no
outbound request at all. This one sits between: `gh` is how BR-16 says a GitHub issue is fetched, but a
missing or unauthenticated `gh` must not stop an analysis that can proceed from a pasted description
(FR-013). The posture is *try, name the failure and its specific remedy, then continue in plain-language
mode* — and it extends to JIRA, which has no `gh` equivalent to gate on in the first place.

**Its JIRA channel is satisfied by the harness, not by an integration.** Spectra ships Markdown only —
no scripts, no binaries, no post-install hooks — and runs inside whatever coding agent the team already
uses, inheriting that agent's reach and its permission model. So the command uses the JIRA access the
host already has, and nothing else. What it must never do is the thing an integration would tempt it
into: prompting for a token (FR-013). A command file that asks for a credential is a phishing surface
that ships in a zip.

**Its central invariant is that the repository answers first.** FR-028 forbids asking the user anything
the command can read, and SC-006 puts a number on it: at least 60% of source-testable hypotheses settled
without a question. This is the opposite of the questionnaire the BRD's problem statement describes, and
it is what makes the layered ladder in FR-026 affordable — the human's attention is spent on runtime
facts nobody can grep for.

**Its most unusual rules are negative ones, and they are what keep the document honest.** Invalidated
hypotheses must appear, not just the surviving one (FR-039a) — recording only confirmations produces
justification, not analysis. A hypothesis must never be marked validated on evidence that cannot settle
it (FR-032). A runtime fact never observed must never be inferred (FR-033). Where nothing was validated,
the document says so rather than promoting a guess (FR-039f). Each of these is a prompt rule, and each
is the failure mode that makes an RCA worse than no RCA.

**It writes two files and is read-only everywhere else.** The document and the index row, both under
`<artifact-root>/defect-rca/`, both as the run's final act (FR-043b). No code fix, no test, no ticket
write-back, no constitution edit, no branch, no commit (FR-055 – FR-058). The hypothesis tree and the
issue trees — the visible bulk of a session — are rendered and never written (FR-036).

The command file is the deliverable. No script and no binary ships: channel detection, root resolution,
recurrence search, hypothesis tracking, numbering, and template resolution are all prompt instructions,
because that is the only form that survives Principle III and the Markdown-only supply chain.

## Technical Context

**Language/Version**: Markdown command prompt in Spec Kit's generic format; Python 3.9+ (standard
library only) for this repository's own tools and tests

**Primary Dependencies**: Spec Kit `>=0.11.0`. `gh` is used for the GitHub issue channel but is
**declared optional and never gated on** — already the manifest's posture at the extension level. JIRA
access, where it exists, comes from the host agent's harness. Neither is required for a run

**Storage**: `<artifact-root>/defect-rca/` in the target project — one `NNN-<slug>.md` per run plus a
rebuilt `README.md` index. Nothing under `.specify/`, no cache, no cross-run state beyond the corpus
itself. The corpus *is* the state: recurrence detection reads documents the command wrote on earlier runs

**Testing**: `python3 -m unittest discover -s tests` (**965 passing at baseline**);
`python3 tools/generate_agent_docs.py --check` (49 agents, 9 prose blocks at baseline); a new
`tests/test_defect_rca_flow.py` (which also asserts the manifest registration, as
`test_impact_flow.py` and `test_test_plan_flow.py` do for theirs); three existing modules gain this
command (`test_doc_output_paths.py` — a **new `CANONICAL` entry**, unlike `test-plan`'s negative
assertion — `test_document_templates.py`, `test_roster_data.py`). Manifest ↔ catalog ↔ zip agreement is
enforced by the `catalog` job in `.github/workflows/ci.yml`, not by the unittest suite; the manual
zip-install pass in `test/README.md` covers the published artifact

**Target Platform**: every coding agent and OS Spec Kit supports. Channel detection, root resolution,
corpus search and numbering are prompt-expressed, so nothing depends on a shell flavour or a named
search tool

**Project Type**: Spec Kit extension command — a prompt file under `spectra/commands/`, a registered
template under `spectra/templates/`, plus the publishing surface Principle V requires

**Performance Goals**: not latency-bound. Two costs are explicitly refused: the command never runs the
project's test suite, and it never scans the codebase exhaustively — FR-017 scopes the scan outward from
the symptom and requires it to state what it did *not* examine, which is the only honest way to bound
the work on a large repository. The recurrence search is bounded by the index (FR-021) with the
documents as the fallback, not the first resort

**Constraints**: Markdown only, no scripts or binaries; agent-agnostic `$ARGUMENTS`; no credential ever
requested, accepted or stored (FR-013); no network beyond ticket and issue retrieval (FR-014); exactly
two files written per run, both in one folder (FR-055); no code fix, patch, config change or test code
(FR-056); no write-back to JIRA or GitHub (FR-057); no constitution edit, branch, stage or commit
(FR-058); no secret reproduced in a committed document (FR-039e); no core Spec Kit command edited and
no hook registered (FR-005)

**Scale/Scope**: 1 new command file; 1 new shipped template; 2 manifest entries; 1 new roster entry; 1
catalog entry; 1 changelog entry; 1 rebuilt zip; ~4 documentation surfaces including a hand-authored
prose block; 1 new test module plus four census/registry updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `022-defect-rca-agent`; the spec carries no unresolved markers and its checklist passed 16/16 in one iteration. |
| II. A Single Self-Contained Extension | ✅ | One new file under the existing `spectra/commands/`, one under `spectra/templates/`. No new extension folder, no dependency on another extension. Reading a prior RCA is reading a file in the user's project, not an extension dependency — FR-023 keeps the run useful on an empty corpus. |
| III. Agent-Agnostic Commands | ✅ | Text only, `$ARGUMENTS` for the defect. No named search tool, no shell flavour, no agent-specific syntax. `gh` appears as a capability the command attempts and degrades from (FR-011, FR-013), not as an invocation the prompt hard-codes into one agent's syntax. |
| IV. Context-Aware by Default | ✅ | The strongest instance on the roster alongside `impact`. FR-015 – FR-019 read the constitution, source, configuration, tests and commit history; FR-020 – FR-024 read the project's own prior analyses and let them change this one. FR-028 forbids asking what the repository answers. |
| V. Catalog and Package in Sync | ✅ | Manifest, roster, catalog, changelog, zip, landing page, generated regions, and a new hand-authored prose block all move in the same change (FR-061 – FR-066). |
| VI. Two Independently-Versioned Channels | ✅ | Extension channel only: 1.14.0 → 1.15.0. `VERSION` untouched, no tag, no Release. |
| VII. Documents Under One Declared Root | ✅ | **Engaged in full, and this is the ordinary case.** `<artifact-root>/defect-rca/`, declared root honoured, publication check before defaulting, non-publishing option taken where the choice cannot be obtained, `NNN-` sequence scoped to the folder, superseded folders read and never touched (FR-040 – FR-043c). Joins `CANONICAL` in `tests/test_doc_output_paths.py`. |
| VIII. Shaped by Overridable Templates | ✅ | **Engaged in full.** New registered `defect-rca-template`, resolved through the four-layer stack, inline skeleton last, resolved path reported (FR-048 – FR-054). |

**Amendment classification**: none required. This plan proposes no change to Spectra's own constitution.

**Extension version classification**: MINOR — 1.14.0 → 1.15.0. A command is added; none is renamed or
removed, and no existing command's behaviour changes. `catalog.json` `provides.commands` goes 9 → 10 and
`provides.templates` gains an eighth entry.

### Where the BRD and the constitution disagreed, and who won

The spec records three departures from `BRD-DEFECTRCA-001 v2.0.0`'s literal text. None is a constitution
violation — each is the constitution being applied to a requirements document written before it was
consulted — so none belongs in Complexity Tracking. They are restated here because a reviewer arriving
from the BRD will look for them.

1. **`docs/defect-rca/` → `<artifact-root>/defect-rca/`.** The BRD hard-codes the path in fifteen
   places. Principle VII makes the root declarable and requires a publication check before defaulting
   into `docs/`. On the overwhelming majority of projects the two produce the identical path; the
   divergence is confined to projects that publish `docs/`, where the BRD's literal instruction would
   serve production stack traces and customer-impact figures to the public web. That is the exact harm
   the check exists to prevent, and the BRD's own sensitive-data risk names it.
2. **Appendix A → a registered, overridable template.** The BRD calls its Appendix A binding. Principle
   VIII requires the structure to ship as an asset resolved through Spec Kit's stack. Appendix A becomes
   the shipped default and stays binding as *Spectra's* answer; a project override replaces it, and the
   command honours the override rather than repairing it (FR-051). What survives any override is the set
   of rules in FR-053, which are the command's, not the template's.
3. **SC-05's 85% completeness → 100%.** In the BRD, completeness was behavioural because the sections
   lived in prose. Here they come from a resolved template the command must honour without omission, so
   a missing element is a command defect rather than a miss in a distribution.

### VII: the index is a directory listing, not a second artifact type

Principle VII says an artifact subfolder "MUST hold exactly one artifact type". `README.md` under
`<artifact-root>/defect-rca/` is not a second one: it holds no analysis, states no root cause, and is
rebuilt from whatever documents are present rather than authored (FR-046). Deleting it loses nothing —
the next run regenerates it. `speckit.spectra.impact` already ships exactly this at
`<artifact-root>/impact-analysis/README.md` and cleared the same gate; this plan follows that precedent
rather than relitigating it.

The index carries functional weight here that it does not carry for `impact`, which is why FR-047 pins
its status explicitly. Recurrence detection (FR-020) has to read the corpus on every single run, and a
one-file read beats N document reads as the corpus grows — that is the BRD's own named mitigation for
its corpus-growth risk. But an index is a cache, and a cache that is trusted as the corpus will
eventually miss a document somebody added by hand. So FR-047 makes the fallback mandatory: nothing found
in the index means read the documents, never means no match exists.

### The `gh` posture, argued

Three postures now exist across the roster and the difference is not stylistic:

- **`create-pr`, `review-pr`** hard-gate. Without `gh` there is no pull request to open or review; the
  command's entire purpose is unreachable, so it stops before doing any other work.
- **`impact`, `test-strategy`, `test-plan`** make no outbound request at all and say so.
- **`defect-rca`** attempts and degrades. A GitHub issue URL is one of three channels, and the other two
  still work — so a missing `gh` costs the user a copy-paste, not the analysis. Stopping would be
  strictly worse for them.

The rule that makes the third posture safe is FR-013's prohibition: name the failure, give the specific
remedy — install versus `gh auth login` — ask for a paste, and never prompt for a credential. A command
that degrades into asking for a token has not degraded, it has escalated.

## Project Structure

### Documentation (this feature)

```text
specs/022-defect-rca-agent/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── command-interface.md
│   ├── document-contract.md
│   ├── recurrence-contract.md
│   ├── index-contract.md
│   └── chat-output.md
├── checklists/
│   └── requirements.md
├── spec.md
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created by /speckit-plan)
```

### Source Code (repository root)

```text
spectra/
├── commands/
│   └── defect-rca.md              # NEW — the deliverable
├── templates/
│   └── defect-rca-template.md     # NEW — BRD Appendix A as a registered asset
├── extension.yml                  # +1 command entry, +1 template entry, version 1.14.0 → 1.15.0
├── CHANGELOG.md                   # +1 entry under 1.15.0
└── README.md                      # generated commands table regenerated

agents-list.json                   # +1 agent in the testing-quality phase
catalog.json                       # version 1.15.0, provides.commands 9 → 10, +tags
docs/
├── index.html                     # command listed (no hard-coded version or description)
└── packages/spectra.zip           # rebuilt by tools/build_package.py

README.md                          # generated agents table regenerated
AGENTS_LIST.md                     # generated regions regenerated + NEW hand-written prose block

tests/
├── test_defect_rca_flow.py        # NEW — the command's invariants
├── test_doc_output_paths.py       # +1 CANONICAL entry: "defect-rca.md": "docs/defect-rca/"
├── test_document_templates.py     # +1 template registered/shipped/resolvable
└── test_roster_data.py            # +1 roster/manifest agreement; census 49 → 50, 18 → 19 available
```

`catalog.json`, `spectra/extension.yml` and the committed zip are held in agreement by the `catalog`
job in `.github/workflows/ci.yml` — there is no unittest for it, so the version bump, the command count
and the rebuilt zip have to move together in the same change or CI fails.

**Structure Decision**: the existing Spec Kit extension layout, unchanged. One command file, one
template file, and the publishing surface Principle V fixes. No new directory anywhere in the
repository; no change to `spectra_cli/`, `VERSION`, or any existing command file.

The one structural choice worth naming is that `defect-rca.md` joins `CANONICAL` in
`tests/test_doc_output_paths.py`, where `test-plan.md` deliberately did not. `test-plan` writes beside
the spec it was handed and has no artifact folder to assert; this command has one, resolves the declared
root, runs the publication check and numbers its output — which is precisely the set of behaviours that
test file exists to pin. Being in `CANONICAL` means the same assertions that hold `adr`, `brd`, `impact`
and `test-strategy` to Principle VII will hold this command too, including the legacy-folder rules,
without a line of new assertion logic.

## Complexity Tracking

> Fill ONLY if Constitution Check has violations that must be justified.

**No violations.** Every principle is satisfied as written; Principles VII and VIII are engaged in full
rather than through a carve-out, which makes this plan simpler on that axis than
`specs/021-test-plan-agent/plan.md`, whose output location needed an argument. The three departures from
the BRD are recorded above and in the spec's Clarifications; they are applications of the constitution,
not deviations from it, and the table is deliberately left empty rather than filled with them.

## Phase 0 — Research

Output: [research.md](./research.md).

The Technical Context carries no `NEEDS CLARIFICATION`. Research is therefore not about resolving
unknowns in the stack — it is fixed by Principles II, III and VIII — but about the questions the spec
answers behaviourally and the command file has to answer *operationally*: how a channel is detected from
an argument, how a recurrence is judged similar enough to surface, how a preventive action's completion
is assessed without asserting it, how the hypothesis ladder is kept from stopping at layer one, and
which of `impact`'s solved mechanics transfer verbatim. Eight decisions, each with rationale and the
alternatives rejected.

## Phase 1 — Design & Contracts

Outputs: [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md).

- **data-model.md** — the nine entities from the spec as the command must actually track them: their
  fields, their legal state transitions (a hypothesis may go open → weakened → invalidated but never
  invalidated → validated without new evidence), and the validation rules the FRs impose.
- **contracts/** — five contracts, because this command has five distinct interfaces: what it accepts
  (`command-interface.md`), what it writes as a document (`document-contract.md`), how it decides a
  prior RCA matches (`recurrence-contract.md`), what the index looks like (`index-contract.md`), and
  what it renders in the session, which is most of what a user sees (`chat-output.md`).
- **quickstart.md** — the runnable validation path: install the working copy into a throwaway project,
  exercise each channel, seed a prior RCA and confirm recurrence, override the root and the template,
  and confirm the negative invariants — nothing written outside the folder, no existing document
  touched, no credential prompt.

## Post-Design Constitution Re-Check

Re-run after the Phase 1 artifacts exist, before `/speckit-tasks`.

| Principle | Status after design | What changed |
|---|---|---|
| I – VI | ✅ | Unchanged. No new file outside the layout above; still one extension, still text-only, still the extension channel alone. |
| VII | ✅ | Strengthened. `document-contract.md` and `index-contract.md` pin the folder, the name, the write-once ordering and the index's cache status, and `CANONICAL` makes the existing assertions apply. |
| VIII | ✅ | Strengthened. `document-contract.md` separates what the template owns (sections, order) from what the command owns (FR-053), which is the distinction that keeps an override from silently disabling a safety rule. |

No principle moved from ✅ and Complexity Tracking remains empty.
