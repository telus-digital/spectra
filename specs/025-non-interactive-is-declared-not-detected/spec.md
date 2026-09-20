# Feature Specification: Non-Interactive Is Declared, Never Detected

**Feature Branch**: `025-non-interactive-is-declared-not-detected`

**Created**: 2026-09-12

**Status**: Implemented

**Input**: Maintainer report while testing 1.17.0 — a real interactive run of `speckit.spectra.test-strategy`
announced "this session is non-interactive", skipped all six questions, and recorded every one as not asked. The user
passed no flag. "Why does it say this? Is it on the prompt?"

## Current State (verified against 1.17.0)

Two commands carry the same detection sentence, and no others do. `spectra/commands/test-strategy.md:591` and
`spectra/commands/test-plan.md:608`:

```text
Detect a session that cannot answer — piped input, no terminal, an automated runner, or an explicit
`--non-interactive`.
```

Four criteria, only one of which the reader can evaluate. The flag is in `$ARGUMENTS` or it is not. The other three
are **process facts** — `isatty()`, whether standard input is a pipe, what launched the runner — and a command file is
a prompt: the thing reading it has no syscall, no file descriptor, and no parent process to inspect. So it guesses.

The guess is not random. Asked to decide whether anyone will answer, a model reaches for the option that cannot leave
it blocked, and that option is *assume nobody will*. The sentence therefore biases toward the failure it should make
rarest.

**The cost of a wrong guess is no longer small.** The wording arrived in 1.16.0 as FR-034 of
[020-test-strategy-agent](../020-test-strategy-agent/spec.md), when non-interactive mode suppressed the coverage-run
confirmation and the amendment approval — both already declinable, both with graceful defaults, so a false positive was
nearly invisible. 1.17.0 attached the whole clarification round to the same switch. A false positive now silently
disables the feature and then explains itself in the document, which reads as a considered finding rather than a bad
guess. That is the reported failure, verbatim: six questions skipped, each recorded `not asked`, on a session with a
human watching.

`test-plan` fails the other way and more visibly: a wrongly non-interactive run refuses to rewrite an existing plan
and reports what it would have changed. Conservative, recoverable, still wrong.

| Command | Line | What a false positive costs |
|---|---|---|
| `test-strategy` | 591 | All six questions skipped; the round — the reason 1.17.0 exists — never runs |
| `test-plan` | 608 | An existing plan is not rewritten; the run reports a diff instead of applying it |

**Supersession.** This replaces the detection clause of FR-034 in
[020-test-strategy-agent](../020-test-strategy-agent/spec.md) and its counterpart in
[021-test-plan-agent](../021-test-plan-agent/spec.md). What each command *does* once non-interactive is unchanged in
both, including the rule that no approval is ever inferred from silence.

## Clarifications

- Q: Is this a bug in the detection, or in attaching the round to it?
  → A: The detection. Attaching the round was correct — a genuinely automated run must not sit waiting on a question
  nobody will answer. What is wrong is asking a prompt reader to determine something only a process can determine,
  and then acting on the answer as though it were established.

- Q: Why not improve the criteria instead of removing them?
  → A: There is nothing to improve them into. Every signal that would distinguish a piped run from a terminal is
  outside what a command file can observe. A criterion that cannot be evaluated is not a weak criterion; it is an
  invitation to guess, and the guess has a direction.

- Q: Does this weaken the guarantee FR-034 exists to provide?
  → A: No. FR-034's guarantee is that a run which cannot take an answer never infers one — that approval is never read
  out of silence. That guarantee is about **consequences**, and every consequence is kept. What changes is the
  trigger: declared rather than surmised.

- Q: What happens in a genuinely automated run that forgets the flag?
  → A: It asks a question nobody answers, and then proceeds on the recommended answer, because that is already what an
  unanswered question does. The cost of a wrongly-interactive run is bounded at one unanswered question. The cost of a
  wrongly-non-interactive run is the whole feature. The defaults should follow that asymmetry, and today they do not.

- Q: Should an agent that genuinely knows it cannot ask stay silent?
  → A: Yes, and it still can. A runner that knows the session is unattended says so — through the flag, or in the
  session. What is removed is the *inference*, not the honest declaration.

- Q: Do the other nine commands need this?
  → A: No. The sentence appears in exactly two files; no other command asks the reader to classify the session.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A real session gets asked (Priority: P1)

A maintainer runs `test-strategy` in a terminal with no flag, watching the output. They are asked the coverage-run
question and then the five, one at a time, and their answers shape the document.

**Why this priority**: it is the reported defect. Everything else here is the discipline that keeps the fix from
reintroducing the problem from the other side.

**Independent Test**: run the command in an ordinary session with no arguments and confirm the questions are asked
and no non-interactive announcement appears.

**Acceptance Scenarios**:

1. **Given** a session with no flag and no statement that answers are impossible, **When** the run reaches the round,
   **Then** it asks, and makes no announcement about the session being unattended.
2. **Given** a run that asks, **When** a question goes unanswered, **Then** it takes the recommended answer and
   continues — the same disposition as before, reached without classifying the session.
3. **Given** any run, **When** the command's text is read, **Then** it instructs the reader not to infer the session
   type, and says what a wrong inference costs.

### User Story 2 - A declared automated run still stays silent (Priority: P1)

A scheduled job runs `test-plan --non-interactive` against a specification whose plan already exists. Nothing is
asked, the existing plan is not rewritten, and the run reports what it would have changed.

**Why this priority**: the fix is only safe if the honest path is untouched. FR-034's guarantee has to survive it.

**Independent Test**: run each command with the flag and confirm the behaviour is byte-for-byte what 1.17.0 produced
under detection.

**Acceptance Scenarios**:

1. **Given** `--non-interactive`, **When** the run starts, **Then** it announces the condition once and asks nothing.
2. **Given** a runner that states in the session that no answer can be given, **When** the run starts, **Then** it is
   treated exactly as the flag.
3. **Given** a declared non-interactive run, **When** the outputs are compared to 1.17.0's, **Then** every
   consequence is unchanged — no approval inferred, no existing plan rewritten, every question recorded not asked.

### Edge Cases

- **The user says mid-run that they are stepping away** — an honest declaration. Take it, and record the remainder as
  not asked.
- **A question is asked and never answered** — already specified: the recommended answer is taken and recorded. No
  session classification is needed to reach that outcome, which is the point.
- **The flag is supplied alongside a focus hint** — unchanged; the flag is removed and the remainder is the hint.
- **A genuinely unattended run with no flag** — it asks, waits as long as its host allows, then proceeds on the
  recommended answers. One wasted question, not a lost feature.

## Requirements *(mandatory)*

- **FR-001**: Both commands MUST treat a session as interactive unless non-interactivity is **declared**.
- **FR-002**: The only declarations are the `--non-interactive` flag and a statement in the session that no answer can
  be given. Both commands MUST name these as the complete set.
- **FR-003**: Neither command may instruct the reader to infer the session type from piped input, the absence of a
  terminal, or the identity of the runner. Those criteria MUST be removed, not softened.
- **FR-004**: Both commands MUST state **why** inference is forbidden — that the reader cannot observe any of those
  conditions — so the next editor does not restore the criteria as a convenience.
- **FR-005**: Both commands MUST state the asymmetry that justifies the default: a wrongly-interactive run costs one
  unanswered question, a wrongly-non-interactive run costs the whole interaction.
- **FR-006**: `test-strategy` MUST direct the reader to ask when in doubt.
- **FR-007**: Every consequence of a declared non-interactive run MUST be unchanged in both commands, including that
  no approval is inferred from silence and no existing test plan is rewritten.
- **FR-008**: The handling of an unanswered question MUST remain reachable without classifying the session, so the
  graceful path does not depend on the detection that is being removed.
- **FR-009**: The test suite MUST assert the ban on inference in both commands, including a guard that fails if any of
  the three removed criteria returns.
- **FR-010**: The extension version MUST bump to `1.17.1` — no new capability, one silent-failure path removed — with
  manifest, catalog, changelog, and zip in sync.

## Success Criteria *(mandatory)*

- **SC-001**: An ordinary interactive run of either command asks its questions, with no flag required to make it do
  so.
- **SC-002**: A run given the flag behaves exactly as 1.17.0 did, in both commands.
- **SC-003**: The phrases `piped input`, `no terminal`, and `automated runner` appear in `spectra/` only as
  prohibitions, in the changelog, and in the documentation of both.
- **SC-004**: A reader of either command can tell what counts as a declaration without guessing, and can see why
  inference is refused.
- **SC-005**: `python3 -m unittest discover -s tests`, `tools/generate_agent_docs.py --check`, and a
  `tools/build_package.py` rebuild all pass.

## Assumptions

- Command files are prompts: the enforceable surface is their text plus the tests over it. The fix is a change to what
  the reader is told to conclude, which is the only lever a prompt has.
- A host that genuinely cannot relay a question will fail to answer it, and the unanswered-question path already
  handles that outcome correctly. The detection sentence was never what made that safe.
- Where a host dispatches a command to a background agent that cannot reach the user, the honest fix is for that host
  to pass the flag. A prompt cannot detect its own dispatch, and pretending otherwise is what produced this defect.
