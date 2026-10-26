---
id: test-strategy
title: Test Strategy
command: speckit.spectra.test-strategy
provider: spectra
type: add-on
phase: foundation
order: 50
status: available
summary: Decide how this project tests itself — and what coverage floor it can actually hold — before the first feature is planned.
manifest: Read the project, classify it greenfield or brownfield from its own evidence, ask five judgment calls the repository cannot settle — where the testing weight should sit, whether an external consumer exists, which journeys justify end-to-end or UAT and who signs UAT off, what has broken before, and what the organisation forbids (including whether an AI agent may execute UAT) — one question at a time, each carrying a recommendation and the evidence behind it, then write one testing strategy to docs/TEST_STRATEGY.md (or TEST_STRATEGY.md at the project's declared artifact root) covering six lenses — unit, integration, API contract, end-to-end, UAT, and regression — recorded in front matter that every test plan inherits, plus a coverage floor the project can actually hold — in brownfield never above the measured baseline, whatever any answer requests. It never asks what it can measure; the mode, the stack, the surfaces, and the coverage figure are read, not requested, and an answer is recorded as stated rather than as evidence. Declining every question produces the document it would have written on its own, and --non-interactive skips the round outright. A foundation-phase agent, run once alongside the constitution. It then drafts the guardrails that would bake the strategy into every work session — including, where UAT applies, the rule that the implement command never executes or ticks UAT tasks — records the team's decision on each under a frozen ts- ID, and hands a Constitution input section to speckit.constitution to create the constitution or update it; it never writes the constitution itself, in any run, approved or not. Reads documents imported by kb-vault as claimed and the accepted guardrails of its sibling documents, so no clause gets two sources. Recommends configuration rather than applying it, runs nothing without an explicit confirmation, and makes no network request.
---

Decide how this project tests itself, once, at the start. It reads
the repository, works out for itself whether this is greenfield or brownfield, and writes one strategy to
`docs/TEST_STRATEGY.md` — or your declared artifact root — covering unit, integration, API
contract, end-to-end, UAT, and regression testing plus a coverage floor. Then it drafts the guardrails that
would hold every future work session to it, records your decision on each, and hands a Constitution input
section to `/speckit-constitution` — to create the constitution when there is none, or to update it.

Before it writes, it asks you five things — one at a time, each arriving with the answer it would have
chosen and the evidence behind it. Where the testing weight should sit, whether anything outside the
repository depends on an interface here, which journeys justify an end-to-end test, what has broken that
your tests did not catch, and what constraints the repository does not show: no container runtime in CI,
a freeze on new dependencies, a compliance rule. That last one is the gap worth closing — it already
refused to name a tool your stack cannot run, but had nothing to say about one your stack can run and
your team may not adopt. **It will not ask you anything it can measure.** Not the mode, not the stack,
not the surfaces, not your coverage figure; those it reads, because a wrong answer would outrank a right
one. And declining is free: say "use your defaults" and you get the document it would have written on its
own, for the cost of one reply. `--non-interactive` skips the round entirely.

It is deliberately hard for it to say something plausible and wrong. Every recommendation either cites a
path in your project, is marked as a convention with no project evidence, or is marked `stated` and names
the question you answered — never neither, and never an answer dressed up as evidence. **An answer never
moves a number**: ask for a 90% floor in a repository measuring 31% and the floor stays at 31%, with the
disagreement recorded in the document rather than argued at you. It will not name a tool your stack
cannot run, so the end-to-end lens resolves to browser, HTTP, CLI, or **none** rather than reaching for a
browser driver; for a published library, `none` is the correct answer and it says so. When it claims
something is missing, it tells you what it searched for and where.

Brownfield is where most of the care went. It reads your source rather than your README, reports what each
lens covers today before proposing anything, and **never proposes a floor above your current baseline** —
a floor that fails the next build gets deleted, and a deleted floor is worth less than none. Coverage
figures carry their provenance: `measured` only if it ran your tool this session after asking permission,
`reported` with the report's date if it read a committed file, `unavailable` if there is nothing to read.
Where the floor sits below the target, the ratchet is written as triggers you can check from the
repository, not as dates it has no way to know.

The last two lenses are policy rather than levels. **UAT** states whether acceptance testing applies,
who may perform it — a human, or an AI agent only on explicit request — and what counts as evidence on
each surface this project actually has: a screenshot for a browser, a transcript for a CLI or an HTTP
call. **Regression** names the suite that must stay green, cites where it runs or says it runs nowhere
automatically, and records whether a fixed defect earns a regression test. Both are marked applicable or
not, with the reason, and both are recorded in the document's front matter — the lens set and which level
owns what — so `test-plan` can read them rather than guess. The drafted guardrails gain one that keeps
UAT out of the implement command's hands.

Two things it will not do. **It never writes your constitution** — not on approval, not on a re-run, not
if you insist. It drafts each guardrail under a frozen `ts-` ID, records whether you accepted, declined,
or skipped it, and tells you the command that applies the accepted ones, because one command should own
constitution edits and the sync impact report that goes with them. A document imported by kb-vault is
read as what it *claims*, never as current practice. And **it never applies configuration**: the exact CI or coverage change
is written out for you to make.

Unlike the other document agents, it produces a **singleton** — one file at a fixed path, rewritten in
place on a re-run, with Git carrying the history. A standing policy has exactly one current answer, and
anything that links to it should not break every time you refresh it.

## Arguments

none required. Optionally pass a focus to weight the analysis; it never narrows the six
mandatory lenses.

## Use it when

setting up a new project before the first feature, or landing Spectra on an
established codebase and wanting a testing baseline that starts from what is already there.

## Examples

```
/speckit-spectra-test-strategy
/speckit-spectra-test-strategy focus on the API contract boundary with the payments service
```

## How it works

1. Reads your project — constitution, specs, docs, dependency manifests, test and coverage
   configuration, CI definitions, and, in a brownfield repository, the source itself.
2. **Classifies the project greenfield, brownfield, or mixed from evidence**, never by asking you, and
   reports the signals that decided it — including any that pointed the other way.
3. Identifies the **testable surfaces**, so a monorepo does not get one answer for three stacks.
4. Asks you its five questions, one at a time.
5. Works six lenses — unit, integration, API contract, end-to-end, UAT, regression — each either
   applicable with a named approach or not applicable with a stated reason.
6. Derives a **coverage floor** from the baseline it could establish, with a ratchet toward the target.
7. Writes one document to `docs/TEST_STRATEGY.md`, or `TEST_STRATEGY.md` at your declared artifact root.
8. Checks whether the strategy is already in your constitution — or whether there is one at all —
   drafts the guardrails it would make binding, records your decision on each, and hands a
   Constitution input section to `/speckit-constitution`.

It runs nothing without your explicit confirmation — not even your coverage tool.

## Re-running and upgrading

On a re-run it marks what the constitution has since adopted, never offers a declined guardrail again
as new, and reads a strategy from before 1.25.0 without losing a ticked decision.

## Change the shape of the strategy

The document's twelve sections are overridable at
`.specify/templates/overrides/test-strategy-template.md`.
