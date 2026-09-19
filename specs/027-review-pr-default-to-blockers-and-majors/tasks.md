# Tasks: A Default Narrow Enough to Say Yes To

**Input**: [spec.md](./spec.md), [plan.md](./plan.md)

**Branch**: `027-review-pr-default-to-blockers-and-majors`

---

## Phase 0 — Verification of the premise

- [X] T001 Confirm no default is proposed today: `review-pr.md:532` reads "Nothing is pre-selected", and the block at
  `:557` is a read-back of an already-typed selection rather than a proposal.
- [X] T002 Confirm `yes` is not accepted today — absent from the grammar at `:536–547`, and `:552` re-prompts on
  unparseable input.
- [X] T003 Confirm `blockers+major` is discoverable only by reading one row at `:543`, with no recommendation.
- [X] T004 Confirm dropped findings already leave no trace on the PR (`:705`), so no change is needed for that.
- [X] T005 Confirm the verdict is already mechanical (`:508`) and that a proposal holding a blocker can therefore
  never propose approval — the basis for the collapse being safe (D6).
- [X] T006 Locate every published copy of "Nothing is pre-selected" and separate live claims from records. Live:
  `spectra/commands/review-pr.md:21,532`, `AGENTS_LIST.md:245`, `spectra/README.md:347`, `docs/index.html:590`.
  Records that MUST NOT move: `spectra/CHANGELOG.md:816`, `brds/review-pr.md` (BR-18), `specs/008-review-pr/`,
  `specs/015-review-context-and-template/`.
- [X] T006a Confirm `brds/` is historical, not governing, before leaving BR-18 contradicted:
  `.specify/memory/constitution.md:211` and `CONTRIBUTING.md:174` both say so, and BRD-005 is Status Draft 0.1.0.

**Checkpoint**: the reported behaviour is absent, and the reason it matters is already written in the file.

---

## Phase 1 — User Story 1: the quiet answer is the correct one (P1)

- [X] T007 Rewrite the "human is the filter" bullet at `review-pr.md:21–22` so the narrow default is stated as
  principle (FR-001, D1, D2).
- [X] T008 Replace Step 8 at `:530–564` with the proposal-based flow: heading, the reason the default has to be
  right, and the rendered ordinary-case shape (FR-001, FR-002, FR-003, D1).
- [X] T009 In that shape, list "Will publish" with severity, class, and anchor, and name the verdict on the heading
  line (FR-002, FR-003).
- [X] T010 List "Will NOT publish" enumerated by Step 7's numbers, grouped by severity — never a bare count
  (FR-002, D4).
- [X] T011 State the four required elements of the shape as requirements rather than styling: both lists enumerated,
  `all` offered plainly, the verdict riding along, the persistence warning kept (FR-002, FR-005, D4).
- [X] T012 Add `yes`/`confirm`/`confirmed`/`ok` to the grammar, accepting findings *and* verdict (FR-004, D5).
- [X] T013 Rename Step 7's final list item to "The proposal" at `:490–492`, and fix the pre-existing duplicate `10.`
  in the same list.

**Checkpoint**: a one-word answer produces the narrow review.

---

## Phase 2 — User Story 2: everything is still one word away (P1)

- [X] T014 Put `all` inside the proposal itself, in plain language, as a visible peer of the default — not only in
  the grammar table (FR-005, SC-002).
- [X] T015 Keep every existing selection form in the grammar table unchanged: `none`, `all`, ranges, severity groups,
  `except`, `<n>:major`, `<n>:body` (FR-008).
- [X] T016 State that `yes` is the only input carrying a verdict, and that every other selection returns to Step 9
  (FR-009).
- [X] T017 Scope the read-back at `:555` to selections other than `yes`, and say why a bare `yes` needs none.

**Checkpoint**: the default is easy to accept and equally easy to escape.

---

## Phase 3 — User Story 3 and the safety properties (P2)

- [X] T018 Add the no-blockers-or-majors shape: default publishes nothing, `approve` offered explicitly, `all`
  available with a comment-only verdict (FR-007, D7).
- [X] T019 Rewrite the silence paragraph: keep "an empty or absent selection publishes nothing, and that is a
  successful run" verbatim, and add that silence is not `yes` and an unanswered prompt is not a default accepted
  (FR-006, D3).
- [X] T020 Add the skip condition to Step 9 for a `yes` answer, with D6's argument written beside it (FR-004, D6).
- [X] T021 Confirm the self-review and approve-over-blocker rules at `:573–589` are otherwise untouched.
- [X] T022 Add the default threshold to the non-overridable list at `:631` (FR-010, D9).
- [X] T023 Add two edge-case rows: no blockers or majors; reviewer replies `yes` (FR-007, FR-004).

**Checkpoint**: the guarantees that mattered before still hold, and are stated more explicitly than they were.

---

## Phase 4 — Tests

- [X] T024 Replace `test_nothing_is_preselected` in `tests/test_review_pr_flow.py:351` — its literal string will no
  longer exist — with a test that the default proposal is blockers and majors (FR-001).
- [X] T025 Keep `test_an_empty_selection_publishes_nothing` verbatim; add a test that silence is not consent
  (FR-006, D3).
- [X] T026 Assert `yes` carries the verdict and that Step 9 is skipped for it (FR-004).
- [X] T027 Assert `all` appears inside the proposal, not only in the grammar table (FR-005).
- [X] T028 Assert the no-blockers case defaults to publishing nothing and offers `approve` (FR-007).
- [X] T029 Assert the dropped findings are enumerated rather than counted (FR-002, D4).
- [X] T030 Assert dropped findings still never reach the pull request (FR-011, `:705`).

---

## Phase 5 — The published prose (FR-012)

- [X] T031 Update the `<!-- SPECTRA:AGENT id=review-pr -->` prose block in `AGENTS_LIST.md` — hand-written, outside
  the generated markers.
- [X] T032 Update the hand-written `speckit.spectra.review-pr` section in `spectra/README.md`.
- [X] T033 Update the `cdesc` span at `docs/index.html:590`.
- [X] T034 Update the `review-pr` command `description` in `spectra/extension.yml` and the command's own front-matter
  description if either still claims nothing is pre-selected.

---

## Phase 6 — Release (Principle V, one change)

- [X] T035 Bump `extension.version` to `1.18.0` in `spectra/extension.yml` (FR-013).
- [X] T036 Mirror `version` and both `updated_at` fields in `catalog.json`; `provides.commands` stays `11` (FR-013).
- [X] T037 Add the `[1.18.0]` entry to `spectra/CHANGELOG.md` under `### Changed`: what the reviewer now sees, why a
  blank prompt produced the noise it was written to prevent, and an explicit paragraph on what did **not** change —
  empty still publishes nothing, the preview gate is intact, approve-over-blocker keeps its typed confirmation
  (FR-013).
- [X] T038 Rebuild `docs/packages/spectra.zip` with `python3 tools/build_package.py` (FR-013).

---

## Phase 7 — Verification

- [X] T039 `python3 -m unittest discover -s tests` — full suite green.
- [X] T040 `python3 tools/generate_agent_docs.py --check` — no drift; the roster is untouched.
- [X] T041 `grep -rn "pre-selected" spectra/commands/ spectra/README.md docs/index.html AGENTS_LIST.md README.md`
  returns nothing (SC-006).
- [X] T041a Confirm the same grep over `spectra/CHANGELOG.md`, `brds/`, `specs/008-*` and `specs/015-*` **still**
  finds it — a record silently rewritten is worse than one left contradicting the present (FR-012a).
- [X] T042 Rebuild and `diff -r spectra /tmp/unzipped/spectra` — zip in sync.
- [X] T043 Run CI's version, command-count, and description-parity checks locally.
- [X] T044 Confirm the two rendered shapes in Step 8 are internally consistent: the numbers in "Will publish" and
  "Will NOT publish" partition the stated total, and the severities match the counts.
- [X] T044a Keep that check in the suite rather than running it once — `test_the_rendered_proposals_add_up`
  re-derives the partition from the command's own blocks. Mutation-checked both ways: a wrong count and a
  short range each fail it by name.
- [X] T045 Set the spec's **Status** to Implemented.

---

## Dependencies

- T001–T006 precede everything.
- T007 → T008 → T009 → T010 → T011 → T012 (one section, in order); T013 is independent.
- T014–T017 depend on T008.
- T018–T023 depend on Phase 1; T020 depends on T012.
- T024–T030 depend on Phases 1–3.
- T031–T034 depend on T006; T034 also on Phase 1 being final.
- T035–T038 depend on every prose edit being final; T038 depends on T035 and T034.
- T039–T045 last. T041 depends on Phase 5. T042 depends on T038.
