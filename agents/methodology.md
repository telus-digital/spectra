---
id: methodology
title: Methodology Analyst
command: speckit.spectra.methodology
provider: spectra
type: add-on
phase: foundation
order: 30
status: available
summary: Find, choose, and record the team's engineering methodology — spec-driven by default, with test-first or behaviour-first as binding phase obligations — and hand it to the constitution.
manifest: Say whether the project is brownfield or greenfield and whether the constitution will be created or updated, then work nine lenses — methodology stack, work modes, requirements intake, spec lifecycle, branching, review gates, change records, AI collaboration, governance — and ask the team ten questions one at a time, each with at least four options, one recommended, one Skip. Spec-driven development is the fixed base; test-first, behaviour-first, domain-first, contract-first, and ADR-driven overlays enter only as obligations bound to a spec-kit phase. Then write an onboarding-grade methodology with a Constitution input section to <artifact-root>/ENGINEERING_METHODOLOGY.md and hand it to /speckit-constitution to create or update the constitution. Reads documents imported by kb-vault as claimed, never as current practice.
---

Say whether the project is brownfield or greenfield and whether this
run creates or updates the constitution, then read the history, workflow configuration, and sibling
documents and work nine lenses: methodology stack, work modes, requirements intake, spec lifecycle,
branching, review gates, change records, AI collaboration, and governance. Spec-driven development is
the base; test-first, behaviour-first, domain-first, contract-first, and ADR-driven overlays are offered
with their evidence and enter the constitution only as obligations bound to a spec-kit phase. It asks
you ten questions one at a time, then writes an onboarding-grade `docs/ENGINEERING_METHODOLOGY.md` — or
your declared artifact root — with a Constitution input section, and hands you a ready-to-paste
`/speckit-constitution` prompt. Documents imported by kb-vault are read as what they *claim*, never as
what the history shows. It never edits the constitution and adopts nothing you did not choose.

## Arguments

none required. Optionally pass a focus hint, or `--non-interactive` to write the
document without asking anything (and adopt nothing).

## Use it when

bringing an existing codebase onto Spectra and writing down how the team really works,
or agreeing a methodology for a new project — including whether test-first is binding.

## Examples

```
/speckit-spectra-methodology
/speckit-spectra-methodology we are weighing TDD for new code
```

## How it works

1. Says first whether the project is **brownfield** or **greenfield** — from three signals: source
   beyond scaffolding, workflow configuration, and more than 10 commits — and whether this run's goal
   is to **create** the constitution or **update** it. With exactly one signal it asks you to settle
   the reading.
2. Reads `git log` and `git branch -a`, PR and issue templates, `CODEOWNERS`, CI workflows, commit and
   changelog configuration, `CONTRIBUTING.md`, `specs/`, the constitution, and the sibling documents —
   accepted entries only.
3. Works nine lenses: methodology stack, work modes and classification, requirements intake, spec
   lifecycle and traceability, branching and integration, review and merge gates, change records, AI
   collaboration rules, and governance and evolution. In brownfield mode each reports current practice
   with citations before proposing; in greenfield mode each offers defaults.
4. Treats spec-driven development as the base, and offers TDD, BDD/ATDD, DDD, contract-first, and
   ADR-driven as overlays, each with its evidence. An adopted overlay becomes obligations bound to
   specify, plan, tasks, or implement — TDD's implement obligation is checked in `tasks.md` — with a
   strictness (MUST or SHOULD) and a scope you choose.
5. Asks you ten questions, one at a time. Each has at least four options, one recommended and one
   **Skip**, and free text always works.
6. Only after the last answer, writes `docs/ENGINEERING_METHODOLOGY.md` — or `ENGINEERING_METHODOLOGY.md`
   at your declared artifact root — with a mode-choice table, branch-naming and commit-prefix references,
   the obligations matrix, and a **Constitution input** section holding exactly what you accepted. It is
   shaped by `engineering-methodology-template` (override at
   `.specify/templates/overrides/engineering-methodology-template.md`).
7. Ends with a ready-to-paste `/speckit-constitution` prompt, then lists the other constitution-feeding
   agents you have not run yet.

It never edits the constitution, never runs another spec-kit phase, and never proposes in a sibling's
ground: test levels and coverage stay with `test-strategy`, environments and versioning with
`deployment-strategy`, product technology and domain content with `domain-analyzer`. A hand-written
methodology already at the path is read as evidence and replaced only with your consent.

## Re-running and upgrading

Re-running offers your previous answers as each question's proposed answer, keeps every guardrail's ID,
and does not offer a declined one back to you as new. Delivery and workflow decisions made in an earlier
domain analysis are read as prior answers.
