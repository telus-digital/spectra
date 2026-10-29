# Research: Consistent Next-Step Suggestions Across the SDLC

Every unknown from the plan's Technical Context, resolved. Sources are the installed Spec Kit (1.2.4,
`~/.local/share/uv/tools/specify-cli`), cached earlier Spec Kit releases, the upstream changelog and tagged
templates, and SPECTRA's own command files and tests.

## R1 — Minimum Spec Kit version (FR-009)

- **Decision**: raise `requires.speckit_version` from `>=0.11.0` to `>=0.11.2`.
- **Rationale**: the upstream changelog lists `feat: add /speckit.converge command (#3001)` under
  `[0.11.2] - 2026-06-18`. The tagged template `templates/commands/converge.md` at `v0.11.2` contains the
  `hooks.after_converge` check, and the same file at `v0.11.1` does not exist. Cached releases agree:
  0.10.1 has no converge command; 0.11.3 onward all do, with the `after_converge` check. `after_clarify` and
  per-event hook lists (needed for the three-entry `after_implement`) predate 0.11.0, which the current
  floor already assumes.
- **Alternatives considered**: `>=0.11.3`, the earliest release inspected locally — rejected, because
  0.11.2 is confirmed from the tagged template and is the true first release. Pinning to the tested 1.2.x —
  rejected: it would lock out every 0.11–1.1 install for no behaviour this feature needs, and the existing
  floor already follows the "first release with what we use" convention.

## R2 — Can an extension hook target a core command? (FR-010)

- **Decision**: yes; register `speckit.converge` under `after_implement` and record the dependency.
- **Rationale**: in 1.2.4, manifest validation checks only that each hook entry is a mapping with a
  `command` and an integer `priority >= 1`; `register_hooks()` copies `command` as given. The alias lift only
  rewrites two-part references whose first part is the extension id (`spectra.x`), so `speckit.converge`
  passes through unchanged. Core templates turn it into `/speckit-converge` by replacing dots with hyphens.
  No code path checks that a hook's command belongs to the registering extension.
- **Caveat**: the extension reference describes `command` as "the extension command the hook is associated
  with", and its examples only show an extension hooking its own commands. So this is current behaviour, not
  a documented contract. The comment beside the entry and the changelog say so, and the edge case in the spec
  names the consequence: the converge offer would vanish, and nothing else would break.

## R3 — What decides the order users see? (FR-003, FR-004)

- **Decision**: list order, with priorities 3 / 5 / 10 for converge / uat / create-pr.
- **Rationale**: the extension reference states that command templates "surface hooks in their configured
  YAML order and do not sort them by `priority`". Only `HookExecutor.get_hooks_for_event()` sorts. Keeping
  the priority values consistent with list order means both paths agree.
- **Cross-extension order**: `register_hooks()` appends an extension's entries to the event list, so
  SPECTRA's entries sit after any extension installed before it (for example git's `after_implement`
  commit). SPECTRA cannot and does not try to control that.

## R4 — Where each closing suggestion attaches in the agents

| Agent | Attach point | Offer condition | No-offer cases |
| --- | --- | --- | --- |
| `defect-rca` | Step 13 — Report, after the existing bullets | a hypothesis reached `validated` | no validated cause; exploration mode writes nothing (no block at all) |
| `impact` | Step 14 — Report, after "Status is draft…" | every run that writes an analysis (conditional wording) | runs that write nothing |
| `flaky-test-detector` | Step 9 — Report; Step 7 decline path | open rows whose outcome is production code, guardrail, or not confident; every open row when Gate 2 is declined | all fixed; nothing proposed (Step 10); Gate 1 declined; rows deleted in review; test not found; evidence gone |

- **Impact** already says "Status is draft. Take it to your stakeholders; record their answer in the front
  matter yourself." The pointer follows that line. Its "never does" row — "Create, reference, or link a
  specification" — still holds, because the pointer writes nothing and the document gains no spec reference.
  The row gains one sentence saying a pointer to `/speckit-specify` in the session report is permitted.
- **defect-rca layer rule**: Step 10 already refuses to promote a layer-2 finding. The offer's prompt states
  the layer of the deepest validated finding, so a fix spec for the immediate technical cause is labelled as
  such.
- **flaky-test-detector outcome reasons** come from the existing Step 8 "When you cannot fix it" table. Three
  of its five reasons (production code, guardrail, not confident) can be acted on by a spec. The other two
  (test not found, evidence gone) can't.

## R5 — Layout of the shared block (FR-011)

- **Decision**: a two-part block, with the contract in `contracts/closing-suggestion.md`.
- **Rationale**: it matches the clarified answer. It's short enough to sit under each agent's existing report
  without displacing required content, and it's stable enough for tests to assert the label and the
  no-offer form.
- **Principle VIII**: the block, and the prompt it carries, are session output that tells the user what to
  run, like `test-plan`'s planning prompt and `adr`'s `/speckit-constitution` prompt. Neither of those is a
  templated deliverable. No template is registered for it.

## R6 — How the change is verified

- **Decision**: one new unittest module, `tests/test_next_step_suggestions.py`, plus targeted edits to the
  two existing hook tests, plus a manual pass recorded in `quickstart.md`.
- **Rationale**: command files are prompts, so the enforceable surface is their text. That's the convention
  every `*_flow.py` test states. Two existing tests slice the manifest by event and will mis-slice once new
  events are added:
  - `test_test_plan_flow.py` reads `after_specify` up to `after_implement:`, which would swallow
    `after_clarify`.
  - `test_uat_flow.py` reads `after_implement` to the end of the `hooks:` block, which would swallow
    `after_converge`.

  Both need to slice to the next event key. `test_every_spectra_hook_is_optional` raises its minimum count
  from 3 to 6.
- **Runtime behaviour** (offers shown in order, nothing runs) can't be proven by text assertions. It's the
  manual pass in `quickstart.md`, consistent with `test/README.md` track 2.

## R7 — Which published text names a hook arrangement (FR-021)

- `agents/test-plan.md`: the manifest line ("offered by an optional hook after specify") and the body line
  in "When to use". Both change to "after specify or clarify". The assertion in `test_test_plan_flow.py`
  that pins the phrase changes with them.
- `agents/uat.md`: the body line "After implement, an optional hook offers it ahead of `create-pr`" becomes
  "after implement, ahead of `create-pr`, and after converge".
- `agents/create-pr.md`: "a hook once `implement` finishes" stays true. No change.
- `docs/getting-started/spectra.html` is hand-written and has no generated region. Two lines change: the
  "For every feature" step after `/speckit-converge` gains "A hook then offers UAT", and the scenario 07 flow
  mentions the converge offer ahead of UAT.
- Generated listings (`spectra/README.md`, `AGENTS_LIST.md`, `docs/getting-started/agents.html`, the
  `description:` lines) pick up these changes from `agents/` through the generator.
