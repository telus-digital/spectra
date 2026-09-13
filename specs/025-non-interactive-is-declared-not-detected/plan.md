# Implementation Plan: Non-Interactive Is Declared, Never Detected

**Branch**: `025-non-interactive-is-declared-not-detected` | **Date**: 2026-09-12 | **Spec**: [spec.md](./spec.md)

## Summary

One sentence replaced in two commands. Both told the reader to detect a session that cannot answer from piped input,
the absence of a terminal, or the identity of the runner — none of which a prompt can observe, so the reader guessed,
and the guess that cannot leave it blocked is *assume nobody is there*. Non-interactivity becomes something that is
**declared**: the `--non-interactive` flag, or a statement in the session. Every consequence of a declared
non-interactive run is unchanged in both files.

## Technical Context

**Language/Version**: Markdown command prompt; Python 3.9+ for tests

**Primary Dependencies**: unchanged

**Testing**: `python3 -m unittest discover -s tests`; `tools/generate_agent_docs.py --check`

**Constraints**: Markdown only; agent-agnostic; FR-034's guarantee preserved in full; no change to either command's
write scope

**Scale/Scope**: one section rewritten in each of two commands, two test classes extended, version sync

## Evidence

| Claim | How it was verified |
|---|---|
| The sentence exists in exactly two commands | `grep -n "piped input\|no terminal\|automated runner" spectra/commands/*.md` returns `test-strategy.md:591` and `test-plan.md:608` and nothing else |
| It predates the round and was inherited unchanged | `git show 1a671e9:spectra/commands/test-strategy.md` line 444 carries it without the flag clause; 1.17.0 appended `or an explicit --non-interactive` and nothing more |
| 1.17.0 raised its cost | The round is gated on it at `test-strategy.md:596`; in 1.16.0 the same switch gated only the coverage run and the amendment |
| The failure is real, not theoretical | Reported from a live interactive run: the announcement fired, all six questions were recorded `not asked`, no flag was passed |
| `test-plan` fails the other way | `test-plan.md:617` — an existing plan is not rewritten, so a false positive reports a diff instead of applying it |
| The graceful path does not depend on the detection | `test-strategy.md` Step 5 already records an unanswered question as not asked, reached without classifying the session |

## Constitution Check

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `025-non-interactive-is-declared-not-detected`. |
| II. Single Self-Contained Extension | ✅ | No files added or removed. |
| III. Agent-Agnostic Commands | ✅ | This is III enforced. The removed criteria were an implicit assumption that the reader is a process with file descriptors; the replacement asks only for what any host can supply — an argument, or something the user said. |
| IV. Context-Aware by Default | ✅ | Unaffected. The session is not project context. |
| V. Catalog and Package in Sync | ✅ | Manifest, catalog, changelog, and zip move together. Roster untouched. |
| VI. Two Versioned Channels | ✅ | Extension channel only: 1.17.0 → 1.17.1. No tag; root `VERSION` untouched. |
| VII. Documents Under One Declared Root | ✅ | Unaffected. |
| VIII. Shaped by Overridable Templates | ✅ | Unaffected; no template changes. |

**Amendment classification**: none.

**Extension version classification**: PATCH — 1.17.0 → 1.17.1. No capability is added or removed and no argument
changes; one silent-failure path is removed. The same classification 1.9.1 took for the same shape of fix.

## Phase 0 — Decisions

- **D1 — Remove the criteria, do not soften them.** There is nothing to soften them into. `isatty()`, pipe state and
  parent process are outside what a command file can observe, so any rewording still resolves to a guess. A criterion
  that cannot be evaluated is worse than none, because it reads as though it can be.

- **D2 — Declared, not surmised.** The flag, or a statement in the session. Both are things a host can actually
  supply, which keeps Principle III honest: the command asks for an argument and for words the user said, not for the
  shape of the process it happens to be running inside.

- **D3 — Keep every consequence.** FR-034's guarantee is about what a non-interactive run *does* — never infer
  approval from silence — not about how it was recognised. Both consequence lists stay exactly as they are, so the
  diff is confined to the trigger.

- **D4 — Write down the asymmetry.** A wrongly-interactive run costs one unanswered question, which the commands
  already handle. A wrongly-non-interactive run costs the whole interaction and then reports its own reasoning as a
  finding. Stating that in the command is what stops the next editor restoring the criteria for tidiness.

- **D5 — Lean on the path that already works.** An unanswered question is already specified to take the recommended
  answer and record as not asked, reached without classifying anything. The detection sentence was never what made
  that safe, and saying so removes the temptation to reintroduce it.

## Phase 1 — Design notes

`spectra/commands/test-strategy.md`, `## Non-interactive mode`: the detection sentence becomes a declaration rule
carrying D1's reason, D4's asymmetry, and an explicit *ask when in doubt*. The consequence list below it is untouched.

`spectra/commands/test-plan.md`, `## Non-interactive mode`: the same replacement, minus the ask-when-in-doubt line,
which has no round to protect. Its "asymmetry is the point" paragraph about creating versus rewriting already sits
below the list and stays — this adds a second, different asymmetry above it, so the two are worded not to collide.

`tests/test_test_strategy_flow.py` and `tests/test_test_plan_flow.py`: each gains the declaration rule, the stated
reason, and a mutation guard over the three removed phrases.

Docs: no roster, template, or landing-page change. The behaviour a user reads about is the behaviour they already
believed they had.

## Risks

| Risk | Mitigation |
|---|---|
| A future editor restores the criteria as a convenience | D1 and D4 are written into both commands as reasons, not rules; a guard test fails the build if any of the three phrases returns |
| A genuinely unattended run now hangs | It cannot: the host resolves an unanswered question, and both commands already proceed on the recommended answer (D5). The bound is one question |
| A host that dispatches to a background agent still cannot ask | Out of the prompt's reach by construction — the honest fix is the flag, and the spec's Assumptions say so rather than leaving it implied |
| The two commands drift apart in wording | Both rewritten in the same change, with the same rule asserted in both suites |

## Complexity Tracking

> No violations. One trigger replaced in two files; every consequence, argument, and write scope unchanged.
