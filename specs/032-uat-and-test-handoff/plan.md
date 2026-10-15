# Implementation Plan: UAT and Regression Lenses, a Tighter Test Handoff, and a UAT Runner

**Branch**: `032-uat-and-test-handoff` | **Date**: 2026-10-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/032-uat-and-test-handoff/spec.md`

## Summary

This change makes the testing trio one connected flow: `/specify → /test-plan → /plan → /tasks →
/implement → (optional) uat`.

- **test-strategy** gains two lenses, **UAT** and **Regression**, and records them in front matter, so
  test-plan can read applicability without parsing prose. Its drafted constitution amendment carries a
  clause that keeps UAT tasks out of implement.
- **test-plan**:
  - takes its lens *set*, not just its lens *names*, from the strategy;
  - adds two sections, **Suggested UAT scenarios** and **Regression scope**;
  - honours the strategy's ownership map, constraints, risk areas, journeys, per-surface floors and
    provenance, and flags a stale strategy;
  - is now offered by an optional `after_specify` hook;
  - ends with a planning prompt that writes its obligations into `plan.md`, because `plan.md` is what
    the core tasks command actually reads.
- **speckit.spectra.uat**, a new command, runs only on explicit request (directly, or through an optional
  `after_implement` hook ordered before `create-pr`):
  - performs the UAT scenarios the agent can drive;
  - saves evidence beside the spec;
  - ticks only the UAT tasks it saw pass;
  - writes a report shaped by a new `uat-report-template`.

Nothing in Spec Kit core is edited. Because the extension adds a command and changes two, this is a
catalog-channel MINOR (1.20.0 → 1.21.0). It also carries a constitution MINOR (1.10.0 → 1.11.0): with a
second command now writing beside the spec, the Principle VII carve-out that spec 021 argued case by case
becomes explicit.

## Technical Context

**Language/Version**: Markdown command prompts and YAML (the shipped extension). Python 3 stdlib for
tests and tools (`python3` on this machine).

**Primary Dependencies**: Spec Kit ≥ 0.11.0. Per-event hook lists with priority ordering arrived in
0.10.0 (upstream #2798), so the existing floor already covers a second `after_implement` hook. Tested
against specify-cli 1.1.2. No new runtime dependency.

**Storage**: Files only.
- test-plan writes `specs/<feature>/test-plan.md`, as today.
- uat writes `specs/<feature>/uat-report.md` and `specs/<feature>/uat/<run-stamp>/…` evidence, and
  edits only UAT-task lines in `specs/<feature>/tasks.md`.

**Testing**: Standard-library `unittest` asserting on the shipped command text, templates and manifest
(`python3 -m unittest discover -s tests`). The generated-docs check runs via
`python3 tools/generate_agent_docs.py --check`. The end-to-end pass is manual
(`specify extension add --dev`), per [quickstart.md](quickstart.md).

**Target Platform**: Any Spec Kit integration. Commands stay agent-agnostic (Principle III). uat judges
what it can drive from the tools the executing agent actually has in the session, never from a named
agent.

**Project Type**: Spec Kit extension (prompt files) plus repository tooling.

**Performance Goals**: N/A. These are prompts. The only time-bounded behaviour is uat starting a build,
and that is gated on confirmation.

**Constraints**:
- No core command or core template is edited (FR-044).
- No network request beyond what the build under test makes (FR-062).
- No secret is reproduced in evidence (FR-058).
- The CLI channel is untouched (FR-071).

**Scale/Scope**: 3 command files (2 changed, 1 new), 3 templates (2 changed, 1 new), 1 manifest, roster,
catalog, zip, landing page, e-learning pages, 4 test modules changed and 1 new, and 1 constitution
amendment.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design — result below.*

| Principle | Status | How this change meets it |
|---|---|---|
| I. Spec-Driven Development | ✅ | Spec 032 on branch `032-uat-and-test-handoff`; plan → tasks → implement follow. |
| II. Single Self-Contained Extension | ✅ | The new command is `spectra/commands/uat.md`, registered in the one `spectra/extension.yml`. No new extension folder, and no dependency on another extension. |
| III. Agent-Agnostic Commands | ✅ | `speckit.spectra.uat`, `$ARGUMENTS`, front-matter `description`. Hook prompts name commands by id, not by an agent's syntax. "What the agent can drive" is phrased as *the tools available to you in this session*, never a named product. |
| IV. Context-Aware by Default | ✅ | test-plan reads more of the strategy than before (FR-030–036). uat reads `tasks.md`, `test-plan.md`, the strategy's evidence rule, manifests, and the constitution before acting. |
| V. Catalog and Package in Sync | ✅ | Same change: `extension.yml` 1.21.0 and CHANGELOG, `catalog.json` (version, 13 commands, tags), `agents-list.json` (`uat`), zip rebuild, `docs/index.html`, generated listings, and a hand-written `uat` prose block in README / AGENTS_LIST / spectra/README. |
| VI. Two Independent Channels | ✅ | No change under `spectra_cli/`, and `VERSION` is untouched. Not tagged. |
| VII. Documents Under One Declared Root | ⚠️ → ✅ | **Engaged through the `specs/` carve-out, now made explicit by amendment.** `uat-report.md` and its evidence are per-feature, human-read deliverables written beside the spec, the same placement spec 021 argued for `test-plan.md`. A second instance turns a case-by-case argument into a rule, so this change amends VII (see [research.md](research.md) R4). |
| VIII. Overridable Templates | ✅ | New registered `uat-report-template`, resolved through the four-layer stack with an inline skeleton last and the resolved path reported. `test-plan-template` and `test-strategy-template` gain sections and stay overridable. A project override that drops a new section is honoured and noted. |
| Branching / CI gate | ✅ | One branch for this spec; landed only via `tools/ship.py`. |

**Gate result: PASS.** The one ⚠️ is resolved by the amendment carried in this change, not by a
waiver. If the maintainer prefers not to amend, the fallback is spec 021's route: argue it in Complexity
Tracking. That path is recorded below and stays available.

**Post-design re-check (after Phase 1)**: PASS.
- The contracts introduce no write outside `specs/<feature>/`, no core edit, and no network access
  beyond the build under test.
- uat's edits to `tasks.md` are limited to UAT-task lines (contract `uat-command.md`).
- The only first-of-kind behaviour is that uat executes the project's build. It is gated on an explicit
  confirmation, the same gate test-strategy already uses for its coverage run.

## Project Structure

### Documentation (this feature)

```text
specs/032-uat-and-test-handoff/
├── spec.md
├── plan.md              # this file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1 — manual end-to-end pass
├── contracts/
│   ├── strategy-lenses.md       # UAT + Regression lens contract, front matter, amendment clause
│   ├── test-plan-additions.md   # consistency rules, new sections, strategy-honouring rules
│   ├── workflow-wiring.md       # after_specify / after_implement hooks, plan.md handoff prompt
│   └── uat-command.md           # speckit.spectra.uat interface, writes, gates, report
├── checklists/requirements.md
└── tasks.md             # /speckit-tasks — not created here
```

### Source (repository root)

```text
spectra/
├── extension.yml                      # +uat command, +uat-report-template, hooks: after_specify (test-plan),
│                                      #  after_implement list [uat (priority 5), create-pr (10)]; 1.21.0
├── CHANGELOG.md                       # 1.21.0 entry
├── README.md                          # generated region + uat prose block
├── commands/
│   ├── test-strategy.md               # six lenses, front matter `lenses:` + `ownership:`, Q3 widened, UAT clause
│   ├── test-plan.md                   # lens-set consistency, UAT + Regression sections, FR-030–037, hook, handoff
│   └── uat.md                         # NEW
└── templates/
    ├── test-strategy-template.md      # + "UAT" and "Regression testing" sections
    ├── test-plan-template.md          # + "Suggested UAT scenarios" and "Regression scope"
    └── uat-report-template.md         # NEW

.specify/memory/constitution.md        # 1.11.0 — Principle VII states the per-feature carve-out
agents-list.json                       # + uat (testing-quality, add-on, spectra)
catalog.json                           # 1.21.0, 13 commands, tags (uat, regression, acceptance-testing)
README.md, AGENTS_LIST.md              # generated regions + uat prose
CONTRIBUTING.md                        # carve-out wording, if it restates VII
docs/index.html                        # + uat entry; test-plan / test-strategy descriptions
docs/e-learning/{module-6,AI-DLC,customization}.html   # flow and template table
docs/packages/spectra.zip              # rebuilt

tests/
├── test_test_strategy_flow.py         # six lenses, front matter keys, UAT clause
├── test_test_plan_flow.py             # hook assertions inverted; new sections; consistency; handoff
├── test_uat_flow.py                   # NEW
├── test_document_templates.py         # DOCUMENT_COMMANDS += uat.md
└── test_doc_output_paths.py           # uat joins the not-an-artifact-root-document assertion
```

**Structure Decision**: Everything lands in the existing single extension and the existing test suite.
The new command follows the shape of `deployment-strategy` (spec 031) for rules and reporting, and of
`test-plan` (spec 021) for an explicitly required input and writing beside the spec.

## Implementation Notes

1. **Two tests are deliberately inverted.** `test_test_plan_flow.py`'s `test_it_registers_no_hook` and
   `test_no_hook_is_registered_in_the_manifest` encode spec 021's FR-005, which this spec reverses
   (FR-040–042). Replace them with assertions that:
   - the hook exists and is `optional: true`;
   - its prompt says to pass the reported spec path;
   - the command still refuses inference when invoked with no path.

   Update the module docstring's "never a hook" bullet to match. Leave defect-rca's and kb-vault's
   no-hook assertions alone.
2. **The order of hooks after implement is a list order plus a priority.** Declare `after_implement` as a
   list, with `uat` before `create-pr`, and set `priority: 5` on `uat` and `10` on `create-pr`. The core
   implement prompt iterates in file order, and Spec Kit's executor sorts by priority, so both paths put
   UAT first.
3. **Existing projects keep their old strategies.** test-plan detects a pre-032 strategy by the absence
   of the `lenses:` front-matter key (and of UAT and Regression sections), and says so loudly (FR-012).
   No migration is attempted.
4. **The five-question count stays five.** UAT's "which journeys and who signs off" folds into question 3
   (journeys), and "may the agent execute UAT" folds into question 5 (constraints). The announced count,
   and every test that pins it, stay true (research R3).
5. **Prompt text is the implementation**, so every new rule needs an anchor phrase that a test can pin.
   [contracts/](contracts/) list the phrases.

## Complexity Tracking

| Item | Why needed | Simpler alternative rejected because |
|---|---|---|
| uat executes the project's build (first Spectra command to run the user's application) | UAT by the agent is the feature; it cannot be done by reading | Reading-only UAT is not UAT. Gated by an explicit confirmation with the exact command shown, the same pattern as test-strategy's coverage run; non-interactive mode runs nothing |
| A command reversing a prior spec's decision (test-plan becomes hook-offered) | The maintainer wants test-plan in the default SDD flow | Leaving it un-hooked relies on the user remembering; an optional hook only *asks*, and test-plan still refuses to infer its input, so the original risk (a plan against the wrong spec) is unchanged |
| Constitution MINOR in a feature change | Two commands now write per-feature deliverables beside the spec | Re-arguing the carve-out per command (spec 021's route) is still available. Rejected because a rule argued twice is a rule, and leaving it implicit invites a third agent to argue it differently |
