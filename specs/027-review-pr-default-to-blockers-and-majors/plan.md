# Implementation Plan: A Default Narrow Enough to Say Yes To

**Branch**: `027-review-pr-default-to-blockers-and-majors` | **Date**: 2026-09-18 | **Spec**: [spec.md](./spec.md)

## Summary

`review-pr` pre-selects nothing and asks the reviewer to type a selection grammar. Step 8 gains a rendered
**proposal** — blockers and majors, with the verdict that follows from them — plus the findings it will not publish,
enumerated by number, and `all` offered as a visible peer. `yes` accepts the proposal entire and goes straight to the
preview. Everything else in the grammar is unchanged. The safety property that an empty answer publishes nothing is
kept and stated more explicitly than before.

## Technical Context

**Language/Version**: Markdown command prompt; Python 3.9+ for tests

**Primary Dependencies**: unchanged — standard library only

**Testing**: `python3 -m unittest discover -s tests`; `tools/generate_agent_docs.py --check`

**Constraints**: Markdown only; agent-agnostic; the preview gate at Step 10 is untouched; every existing selection
form keeps working; the phrase "Nothing is pre-selected" is published in four places and they move together

**Scale/Scope**: one step rewritten and four touched in one command, one test class reworked, version sync plus the
three hand-written prose copies

## Evidence

| Claim | How it was verified |
|---|---|
| No default is proposed today | `review-pr.md:532` — "Nothing is pre-selected"; the confirm block at `:557` is a read-back of an already-typed selection |
| `yes` is not accepted today | Absent from the grammar table at `:536–547`; `:552` re-prompts on unparseable input |
| `blockers+major` is discoverable only by reading | One row at `:543` of a ten-row table, with no recommendation anywhere |
| The design already calls the outcome a failure | `:21` — "A review that posts thirty findings to bury the two that matter is worse than no review" |
| Dropped findings already leave no trace | `:705` — "Only accepted findings appear. Dropped findings never reach the pull request" |
| The verdict is already mechanical | `:508` — "Any blocker or major finding means request changes" |
| Collapsing cannot reach approve-over-blocker | `:508` forbids proposing approval alongside a blocker, so the `:578` path is reachable only by a typed `approve` |
| The phrase is published in four places | `review-pr.md:21,532`; `AGENTS_LIST.md` prose block; `spectra/README.md`; `docs/index.html:590` |
| The roster does not move | `agents-list.json` title, status, and command for `review-pr` are unchanged, so no generator rerun |

## Constitution Check

| Principle | Status | Note |
|---|---|---|
| I. Spec-Driven Development | ✅ | This spec/plan/tasks set on branch `027-review-pr-default-to-blockers-and-majors`. |
| II. Single Self-Contained Extension | ✅ | No files added or removed. |
| III. Agent-Agnostic Commands | ✅ | A rendered prompt shape is content, not an agent's syntax. |
| IV. Context-Aware by Default | ✅ | Unaffected — the proposal is computed from findings already derived from project context. |
| V. Catalog and Package in Sync | ✅ | Manifest, catalog, changelog, zip, landing page, and both prose copies move together. Roster untouched. |
| VI. Two Versioned Channels | ✅ | Extension channel only: 1.17.2 → 1.18.0. No tag; root `VERSION` untouched. |
| VII. Documents Under One Declared Root | ✅ | Unaffected. |
| VIII. Shaped by Overridable Templates | ✅ | The review template is untouched — the body's *shape* does not change, only which findings are proposed to fill it. The threshold joins the rubric and the grammar as command-owned, for the same stated reason. |

**Amendment classification**: none.

**Extension version classification**: MINOR — 1.17.2 → 1.18.0. Behaviour a user notices changes: a default is
proposed where none was, and `yes` becomes meaningful. No capability, argument, or document section is added.

## Phase 0 — Decisions

- **D1 — Propose, do not pre-select.** The distinction is the whole change. Nothing is selected without an answer;
  something is *shown* as the recommendation. A grammar table documents an option, a rendered proposal offers one,
  and the current file only ever did the former.

- **D2 — The narrow set is the default because the wide set is the failure mode.** The alternative to a narrow
  proposal is not per-finding curation — it is `all`, the only option a reader can act on without first learning a
  syntax. `:21` already names that outcome as worse than no review.

- **D3 — Keep "silence is not consent", and say it louder.** The safety property and the interaction choice were
  sharing one sentence. Splitting them lets the interaction change while the guarantee is restated explicitly: a
  reviewer who says nothing has not said `yes`, and an unanswered prompt is not a default accepted.

- **D4 — Enumerate the dropped findings, never just count them.** The proposal narrows what is *published*; it must
  not narrow what is *shown*. A count hides them, and `1,4,11` is only usable by someone who can see the numbers.

- **D5 — `yes` carries the verdict.** The verdict is derived mechanically at `:508`, so when the proposal holds a
  blocker or major it is not an open question. Two prompts instead of four, and the preview gate — the one that
  matters, because a suggestion block reaches the author's branch in one click — is untouched.

- **D6 — The collapse is safe by construction, not by care.** A proposal containing a blocker can never propose
  approval, so `yes` cannot reach the approve-over-blocker path. That path keeps its typed confirmation and is
  entered only by a reviewer who typed `approve`. This is checkable, which is why it is a decision and not a risk.

- **D7 — No blockers or majors means publish nothing, and say so.** Consistent with `:549`, which already calls an
  empty selection a successful run. `approve` is offered explicitly because approving a clean PR is the ordinary
  case and should not require inventing a syntax.

- **D8 — No `--severity` argument.** `all` at the prompt costs one word and is offered at the moment the reviewer is
  looking at the findings. An argument would demand the threshold be chosen before seeing them.

- **D9 — The threshold is command-owned.** It joins the rubric, the floors, the confidence cap, the anchor rule and
  the verdict derivation at `:630`. A project that could redefine it would break the guarantee that two reviews of
  the same diff agree, in exactly the way redefining Blocker would.

## Phase 1 — Design notes

`spectra/commands/review-pr.md`:

- `:21–22` — the "human is the filter" bullet states the narrow default as principle, so the mechanics in Step 8 are
  read as following from something rather than as an isolated rule.
- `:490–492` — Step 7's final item becomes "The proposal". The pre-existing duplicate `10.` is corrected while the
  list is open: twelve items currently number to eleven.
- `:530–564` — Step 8 replaced. Two rendered shapes (the ordinary case and the no-blockers case), a grammar table
  extended with `yes` and `approve`, the silence-is-not-consent paragraph, and a read-back that now applies only to
  selections other than `yes` — repeating a proposal verbatim back at someone who just accepted it is the ceremony
  that teaches reviewers to stop reading prompts.
- `:568–571` — Step 9 gains a skip condition and D6's reasoning, so a later editor cannot remove the collapse as
  unsafe without first meeting the argument that it is not.
- `:631` — the threshold added to the non-overridable list.
- `:827–861` — two edge-case rows.

`tests/test_review_pr_flow.py`: `test_nothing_is_preselected` asserts a literal string that will no longer exist and
is replaced. `test_an_empty_selection_publishes_nothing` stays verbatim and becomes load-bearing. New assertions
cover the default's composition, silence, the verdict collapse, `all`'s visibility, and the no-blockers shape.

The three published prose copies (`AGENTS_LIST.md`, `spectra/README.md`, `docs/index.html:590`) each carry
"Nothing is pre-selected" as a user-facing claim and each becomes a description of the default. `SC-006`'s grep is
the check that none was missed.

## Risks

| Risk | Mitigation |
|---|---|
| A default is read as consent, and a future edit lets silence publish | D3 splits the two guarantees and states the surviving one twice — in the grammar section and in the proposal's own closing line; a test asserts it by name |
| The collapse is later removed as unsafe by someone who has not checked | D6's argument is written into Step 9 itself, next to the skip, rather than living only here |
| The dropped findings become a count in a future tidy-up | D4 is stated as a required element of the shape, not a stylistic preference, and the enumeration is asserted |
| One of the four published copies of the old phrase is missed | SC-006's grep covers all four paths and runs before the zip rebuild |
| The proposal shape drifts from what Step 7 numbered | Both lists are specified to use Step 7's numbers, and the read-back for non-`yes` selections is unchanged |
| `all` becomes a footnote again as the prompt is edited | FR-005 requires it inside the proposal, and the test asserts its presence there rather than in the grammar table |

## Complexity Tracking

> No violations. One step is rewritten and four are touched; no file, command, argument, template section, or
> dependency is added.
