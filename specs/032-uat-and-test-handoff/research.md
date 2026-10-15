# Research: UAT and Regression Lenses, a Tighter Test Handoff, and a UAT Runner

The design decisions for spec 032. Each entry gives the decision, the rationale, and the alternatives
considered.

## R1 — Can one extension register two `after_implement` hooks, in a set order?

- **Decision**: Yes. Declare `hooks.after_implement` as a **list** with `speckit.spectra.uat` first
  (`priority: 5`) and `speckit.spectra.create-pr` second (`priority: 10`).
- **Rationale**:
  - The installed specify-cli 1.1.2 accepts a single mapping or a list per event
    (`coerce_hook_entries`) and dedups by command within the manifest.
  - Upstream added per-event hook lists with priority ordering in **0.10.0** (#2798), which is below
    the manifest's `>=0.11.0` floor, so `requires.speckit_version` does not move.
  - The core implement prompt walks the registry list in order. Registration appends this extension's
    entries in manifest order, so list order and priority agree.
- **Ordering against other extensions' hooks (intended)**: Priority sorts across extensions, so `uat`
  (5) is also offered before the git extension's `after_implement` commit hook (10). That is deliberate.
  UAT runs against the implemented but uncommitted build, so its evidence and its ticks land in the same
  commit as the implementation they accept. A user who wants to commit first declines the uat offer and
  runs uat later.
- **Alternatives**:
  - **Put UAT inside create-pr's hook.** Rejected: it couples two commands, and a PR would be offered
    before UAT.
  - **Use only the `priority` field.** Rejected: the prompt-driven path follows file order, not
    priority.

## R2 — How does the test plan reach the tasks without editing core?

- **Decision**: Through `plan.md`. test-plan's final output is a ready-to-paste planning prompt that
  links the written `test-plan.md` and tells the planner to add a **Testing obligations** section to
  `plan.md`. That section names the test-plan path and four obligations (FR-043). The binding guard for
  UAT tasks is a constitution clause drafted by test-strategy.
- **Rationale**:
  - The core tasks command reads `plan.md`, `spec.md`, the optional design documents, and the
    constitution. It never reads `test-plan.md`.
  - Its "tests are OPTIONAL unless requested" rule is satisfied, because `plan.md` and the approved test
    plan do request them.
  - implement reads the constitution, so a project clause binds it. The labelled phase note in
    `tasks.md` is a fallback, not the guarantee.
- **Alternatives**:
  - **A `before_tasks` hook that injects the test plan.** Rejected: hooks run commands, they do not
    inject context, and it would be a second path to keep correct.
  - **Edit the core tasks template.** Forbidden by FR-044.
  - **Write into `plan.md` from test-plan.** Rejected: `plan.md` does not exist yet when test-plan runs,
    and writing a core artifact breaks the one-file rule.

## R3 — Do the new lenses add clarification questions to test-strategy?

- **Decision**: No. The round stays at **five**. Two existing questions widen instead:
  - **Q3** becomes *which journeys are worth an end-to-end test or a UAT scenario, and who signs UAT
    off*.
  - **Q5** (constraints) explicitly covers *whether an AI agent may execute UAT here, and against which
    environments*.
- **Rationale**:
  - The count is announced up front and pinned by tests, and the five are fixed so the announcement
    stays honest.
  - UAT's two judgment calls are a journey question and a constraint question; the existing slots
    already hold them.
  - Regression needs no question: its gate is read from CI, and "does a fixed defect earn a test"
    defaults to yes by convention, overridable by Q5.
- **Alternatives**:
  - **A sixth question.** Rejected: it breaks the announced count, the "always five" rule, and
    re-run pre-fill for every existing strategy.

## R4 — Where do the UAT report and evidence live, and does Principle VII need amending?

- **Decision**:
  - The report goes to `specs/<feature>/uat-report.md`, beside `test-plan.md`.
  - Evidence goes to `specs/<feature>/uat/<run-stamp>/<scenario-id>-<n>.<ext>`, where `<run-stamp>` is
    `YYYYMMDD-HHMMSS` in local time.
  - Amend Principle VII (1.10.0 → 1.11.0) so its Spec Kit carve-out explicitly admits **per-feature
    deliverables written beside the specification they concern**, named: `test-plan.md` and
    `uat-report.md`.
- **Rationale**:
  - Both documents are *about one feature*, are consumed next to its `tasks.md`, and would be severed
    from it under `<artifact-root>/`.
  - Spec 021 argued this placement once in Complexity Tracking and recorded the amendment as "available
    but not taken". A second command makes it a pattern, and a pattern belongs in the principle.
  - A run-stamped evidence folder means a re-run adds evidence rather than overwriting it (FR-061).
  - The report is rewritten per run but keeps a cumulative run log, so it remains the single current
    statement — the same discipline as test-plan.
- **Alternatives**:
  - **`<artifact-root>/uat/NNN-…`.** Rejected: it severs the report from its feature and invents a
    sequence the feature directory already supplies.
  - **Evidence inside `tasks.md`.** Rejected: binary files, and it bloats a tracker.
  - **Keep arguing per command.** Kept as the documented fallback.

## R5 — How does a UAT task look in `tasks.md`, and how does uat find it?

- **Decision**:
  - The test plan gives each scenario an id `UAT1`, `UAT2`, … scoped to the document, like `T1` for
    conditions.
  - The planning prompt asks for a final phase titled **"Phase N: User Acceptance (UAT) — not executed
    by the implement command"**, with one task per scenario in the form:
    `- [ ] T0xx [UAT] UAT3 (US2-AC1) <journey> — executor: agent|human|either`
  - uat matches a task to its scenario by the `UAT<n>` id, never by wording.
  - When a task passes, uat ticks it and appends ` — evidence: specs/<feature>/uat/<run-stamp>/…`.
- **Rationale**:
  - A stable, document-scoped id survives a reworded task.
  - The `[UAT]` label sits where Spec Kit's `[Story]` label sits, so the core task-format validator
    stays happy.
  - Putting the executor in the line lets a human read the hand-off without opening the plan.
- **Alternatives**:
  - **Match on journey text.** Rejected: brittle.
  - **A separate `uat-tasks.md`.** Rejected: implement and converge would not see it, and the user wants
    UAT inside the normal task list.

## R6 — How does uat decide what it can "drive", and what does it run?

- **Decision**:
  - A scenario is attempted only when two things hold: (a) its executor is `agent` or `either`; and (b)
    the surface it needs is one the session's own tools can operate — a browser-automation tool for
    `browser`, a shell for `cli` and `http`.
  - uat states which tools it relied on.
  - Before starting anything, it shows the exact build or start command (taken from the plan's
    quickstart, the README, or a manifest script) and asks.
  - By default it targets a locally started build. Another environment is used only when the user names
    it in the arguments.
- **Two judgments, two sessions**: This rule is uat's alone. test-plan decides `agent` vs `human` earlier,
  from the *kind* of surface the manifests show (`browser`, `cli`, `http`) and the strategy's executor
  policy — never from its own session's tools, because uat runs later, possibly in a different agent.
  A scenario the plan marked `agent` that this session cannot drive is `awaiting human`, with that reason
  (FR-021, FR-054).
- **Rationale**:
  - This mirrors test-strategy's R5 ("no tool the stack cannot run") at execution time.
  - Agent-agnostic: it asks what tools exist, not which agent this is.
  - Confirmation-before-execute matches the only existing precedent (test-strategy's coverage run).
- **Alternatives**:
  - **Always try, and fail gracefully.** Rejected: an attempted browser scenario with no browser tooling
    produces a false "failed".
  - **Run against staging by default.** Rejected: outward-facing and unbounded.

## R7 — Secrets in screenshots and transcripts

- **Decision**:
  - Before saving a transcript, uat scans it for the secret shapes test-plan already lists and masks
    any matches.
  - Before capturing a screen, uat avoids or crops regions that show credential fields or configuration
    pages where it can.
  - Where it cannot be sure a capture is clean, it saves no image, records the outcome with a text
    description, and notes the withholding.
- **Rationale**: Over-withholding is the correct error (test-plan's existing rule). A committed image
  cannot be recalled.
- **Alternatives**:
  - **Never take screenshots.** Rejected: the user explicitly wants screenshots.

## R8 — Detecting a stale strategy (FR-036)

- **Decision**: Flag the strategy as *possibly stale* when either holds:
  - its front-matter `mode` disagrees with the classification signals test-plan can read (for example,
    the strategy says `greenfield` but tests now exist); or
  - a file the feature touches has a newer Git commit than the strategy's `generated` timestamp, and Git
    history is readable.

  It never blocks; it recommends a re-run.

  **The history lookup is a read, not a run.** It is read-only and counts as reading the repository, the
  same way test-plan already reads the current branch for its identifying block. It executes nothing,
  builds nothing, and touches no test, so test-plan's "run nothing" rule is unaffected. Where history
  cannot be read (no repository, a shallow clone, or no read access), test-plan uses the mode check
  alone and says that the history check was skipped, and why.
- **Rationale**: Both checks are cheap, local, and evidence-based. Neither runs anything beyond reading
  history.
- **Alternatives**:
  - **Age threshold (e.g. 90 days).** Rejected: arbitrary, and the same "no dates" reasoning as the
    ratchet.

## R9 — Machine-readable lens applicability in the strategy

- **Decision**: Add two front-matter keys to `TEST_STRATEGY.md`:
  - `lenses:` — a mapping of lens name to `applicable` or `not_applicable`;
  - `ownership:` — a short mapping of behaviour kind to lens.

  test-plan reads front matter first and falls back to the section headings when the keys are absent,
  which also identifies a pre-032 strategy.
- **Rationale**:
  - Front matter is the strategy's own territory, and it survives a template override (the same
    argument test-strategy already makes for its clarification record).
  - It gives FR-010 and FR-030 something exact to read.
- **Alternatives**:
  - **Parse the body.** Rejected: a project override may rename or reorder sections.
