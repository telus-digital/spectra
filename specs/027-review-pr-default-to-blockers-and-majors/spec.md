# Feature Specification: A Default Narrow Enough to Say Yes To

**Feature Branch**: `027-review-pr-default-to-blockers-and-majors`

**Created**: 2026-09-18

**Status**: Implemented

**Input**: Maintainer report — published reviews carry too much noise. "I want to make sure only absolute major and
blocker findings are commented about." The reporter believed the command already proposed blockers and majors and
published them on a "yes". It does not.

## Current State (verified against 1.17.2)

The reported belief and the shipped behaviour differ in three of four particulars.

| Believed | `spectra/commands/review-pr.md` |
|---|---|
| The agent lists all findings | **True** — Step 7, item 10 |
| It suggests blockers and majors | **False** — `:532` reads "**Nothing is pre-selected.**" No default is proposed at all |
| The confirmation proposes that set | **False** — the block at `:557` is a read-back of a selection *already typed* |
| "yes" publishes only those | **False** — `yes` is not in the grammar; `:552` re-prompts on unparseable input |

`blockers+major` exists, but only as one row in a ten-row grammar table at `:543` that the reviewer must already know
and type unprompted. So the shipped interaction hands a reviewer sixteen findings and an unfamiliar syntax, with no
recommendation and no default.

**The failure this produces is the one the design was written to prevent.** `:21` states the principle — *"A review
that posts thirty findings to bury the two that matter is worse than no review, because the author learns to skim."*
A blank prompt in front of sixteen findings is answered `all`, because `all` is the only option a reader can act on
without first learning a grammar. The command's own framing calls that outcome worse than no review, and its
interaction design is what produces it.

One thing the report assumed that **is** already guaranteed: `:705` — *"Only accepted findings appear. Dropped
findings never reach the pull request — in the body or on a line."* Dropped findings leave no trace. Nothing in this
change is needed to achieve that.

## The tension, and why this is not a reversal

"Nothing is pre-selected" is stated as a design principle at `:21–22`, repeated at `:532`, and pinned by
`tests/test_review_pr_flow.py:351`. It is load-bearing, and it is published verbatim in three user-facing places.

But two distinct guarantees are wearing one sentence:

1. **Silence is never consent.** An unanswered prompt publishes nothing. This is a safety property and it is kept,
   unchanged, in full.
2. **No set is proposed.** This is an interaction choice, and it is the one that fails — because the alternative to a
   narrow proposal is not careful per-finding curation, it is `all`.

This change separates them: the first is restated more explicitly than before, the second is replaced by a proposal
that is *narrower* than everything. A default the reviewer must actively widen serves the anti-noise principle; a
blank prompt they must actively narrow does not.

## Clarifications

- Q: Should the dropped findings leave a count line in the published review body?
  → A: No. No trace at all. The author sees only the blockers and majors. `:705` already guarantees this and the
  transcript remains the complete record, as the no-persistence rule already says.

- Q: Should `yes` carry the verdict as well as the selection?
  → A: Yes. The verdict is already derived mechanically at `:508` — any blocker or major means request changes — so
  when the proposal contains one, the verdict is not an open question. Collapsing them takes the flow from four
  prompts to two without touching the preview gate.

- Q: Does collapsing the verdict weaken the approve-over-blocker protection at `:578`?
  → A: No, and this is checkable rather than a matter of judgement. A proposal containing a blocker or major can
  never propose approval, because the derivation at `:508` forbids it. So `yes` cannot reach that path. It is
  entered only by a reviewer who typed `approve` themselves, and it keeps its typed confirmation in full.

- Q: Should the threshold be settable by an argument, e.g. `--severity all`?
  → A: No. `all` at the prompt already covers it in one word, at the moment the reviewer is actually looking at the
  findings. An argument would require deciding the threshold *before* seeing them, which is the wrong time.

- Q: What is the default when there are no blockers or majors?
  → A: Publish nothing — consistent with `:549`, which already calls an empty selection a successful run. The
  proposal says so plainly and offers `approve` explicitly, because a clean PR carrying six nits is the ordinary case
  and approving it should not require inventing a syntax.

- Q: `brds/review-pr.md` BR-18 requires "nothing pre-selected". Does this change need the BRD amended?
  → A: No. The constitution records `brds/` as "historical inputs cross-referenced from `specs/`"
  (`.specify/memory/constitution.md:211`) and `CONTRIBUTING.md:174` says the same. BRD-005 is Status **Draft**,
  version 0.1.0, last updated 2026-08-17, and predates specs 015 and 027. It records what was asked for then. The
  live requirement is this spec.

- Q: Why enumerate the dropped findings by number rather than showing a count?
  → A: Because a count hides them, and the reviewer's ability to say `1,4,11` depends on knowing which numbers are on
  the table. The proposal narrows what is *published*; it must not narrow what is *shown*.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The quiet answer is the correct one (Priority: P1)

A reviewer runs the command on a PR with sixteen findings: three blockers/majors and thirteen minors, nits and
questions. The command proposes the three, enumerates the thirteen it will not publish, and offers `all` as a
visible peer. The reviewer types `yes`. Three findings reach the pull request and the verdict is request changes.

**Why P1**: This is the reported defect. The one-word answer must produce the narrow review.

**Acceptance**:
1. The proposal lists exactly the blockers and majors under a "Will publish" heading, with the verdict named.
2. The remaining findings are listed by number, grouped by severity, under "Will NOT publish".
3. `yes` publishes only the proposed set and submits the proposed verdict, with no separate verdict prompt.
4. The published review contains no minor, nit, or question — in the body or on a line.

### User Story 2 - Everything is still one word away (Priority: P1)

The same reviewer, on a different PR, wants the full set. `all` is on screen, in plain language, as a peer of the
default rather than a footnote.

**Why P1**: A default that is hard to escape is a decision taken on the reviewer's behalf, which is what the command
exists not to do.

**Acceptance**:
1. `all` appears in the proposal itself, not only in the grammar table.
2. `all` publishes every finding at every severity, exactly as it does today.
3. A per-finding selection — `1,4`, `blockers`, `all except 9-14` — continues to work unchanged and returns to the
   verdict step.

### User Story 3 - A clean PR is approvable without syntax (Priority: P2)

A PR yields only minors and nits. The default publishes nothing, says so, and offers `approve`.

**Why P2**: Common, and currently requires the reviewer to know that an empty selection is a successful outcome.

**Acceptance**:
1. The proposal states that the default publishes nothing and that this is a successful run.
2. `approve` submits an approval raising nothing.
3. `all` remains available, with a comment-only verdict.

### Edge Cases

- **The reviewer answers nothing at all.** Publishes nothing. Silence is not `yes`; an unanswered prompt is not a
  default accepted. This is the invariant that must survive the change intact.
- **The reviewer is the author.** Unchanged — self-approval is unavailable, the other two verdicts are offered. The
  default proposal never proposes approval, so the collapsed `yes` is unaffected.
- **A blocker and an approval.** Unreachable from `yes`. Only a typed `approve` reaches it, and the typed
  confirmation at `:583` is untouched.
- **Every finding is a blocker or major.** "Will NOT publish" is empty and is stated as empty, not omitted — an
  absent section reads as a section forgotten.
- **No findings at all.** No proposal is needed; the existing empty-diff and no-findings handling applies.
- **A delta re-review (`--since`).** Selection proceeds exactly as in Step 8, so it inherits the default with no
  separate rule.

## Requirements *(mandatory)*

- **FR-001**: The command MUST propose a default selection of blockers and majors only, rather than pre-selecting
  nothing.
- **FR-002**: The proposal MUST show the findings it will publish and the findings it will not, both enumerated by
  the finding numbers assigned in Step 7.
- **FR-003**: The proposal MUST name the verdict that accompanies the default.
- **FR-004**: `yes` (and `confirm`, `confirmed`, `ok`) MUST accept the proposal entire — findings and verdict — and
  proceed directly to the preview.
- **FR-005**: `all` MUST be offered within the proposal itself, in plain language, as a visible peer of the default.
- **FR-006**: An empty or absent response MUST publish nothing. The command MUST state explicitly that silence is not
  `yes` and that an unanswered prompt is not a default accepted.
- **FR-007**: When no blocker or major exists, the default MUST be to publish nothing, and the proposal MUST offer
  `approve` explicitly.
- **FR-008**: Every existing selection form — `none`, `all`, ranges, severity groups, `except`, `<n>:major`,
  `<n>:body` — MUST continue to work unchanged.
- **FR-009**: Any selection other than `yes` MUST continue to the verdict step as it does today.
- **FR-010**: The default threshold MUST NOT be overridable by a project template, for the same reason the severity
  rubric is not.
- **FR-011**: Dropped findings MUST NOT reach the pull request in any form. (Already true at `:705`; asserted so it
  stays true.)
- **FR-012**: The published phrase "Nothing is pre-selected" MUST be replaced on every **live** surface where it
  appears — `spectra/commands/review-pr.md`, `AGENTS_LIST.md`, `spectra/README.md`, and `docs/index.html` — since it
  will no longer describe the behaviour.
- **FR-012a**: Historical records MUST keep it. `spectra/CHANGELOG.md`'s existing entries, `brds/review-pr.md`, and
  `specs/008-review-pr/` and `specs/015-review-context-and-template/` record what was true when written and MUST NOT
  be rewritten to agree with the present.
- **FR-013**: The extension version MUST bump to `1.18.0` — user-visible behaviour change, no capability added — with
  manifest, catalog, changelog, and zip in sync.

## Success Criteria *(mandatory)*

- **SC-001**: A reviewer who answers `yes` publishes only blockers and majors, and answers exactly one prompt before
  the preview.
- **SC-002**: A reviewer who wants everything reaches it with one word, visible on screen without scrolling to a
  grammar table.
- **SC-003**: A reviewer who answers nothing publishes nothing.
- **SC-004**: Every dropped finding is identifiable by number in the transcript, so any of them can be pulled back.
- **SC-005**: No published review contains a minor, nit, or question unless the reviewer asked for it by name or by
  `all`.
- **SC-006**: `grep -rn "pre-selected"` over `spectra/commands/`, `spectra/README.md`, `docs/index.html`,
  `AGENTS_LIST.md`, and `README.md` returns nothing — and the same grep over `spectra/CHANGELOG.md`, `brds/`, and
  `specs/008-*`/`specs/015-*` still finds it, because those are records rather than claims.
- **SC-007**: `python3 -m unittest discover -s tests`, `tools/generate_agent_docs.py --check`, and a
  `tools/build_package.py` rebuild all pass.

## Assumptions

- A command file is a prompt: what it *shows* is followed more reliably than what it *permits*. A grammar table
  documents an option; a rendered proposal offers one. The defect here is entirely the difference between the two.
- Given a list of findings and no recommendation, a reviewer under time pressure selects the option requiring least
  interpretation. That option is `all`. This is the assumption the current design gets wrong, and it is why a blank
  prompt is not a neutral choice.
- Reviewer trust is the scarce resource. An author who learns to skim is not recovered by a better finding; the
  volume has to stay low enough that every comment is read.
