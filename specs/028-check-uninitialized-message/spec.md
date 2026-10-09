# Feature Specification: One-Step Remedy When the Folder Is Not a Spec Kit Project

**Feature Branch**: `028-check-uninitialized-message`

**Created**: 2026-10-08

**Status**: Implemented

**Input**: User description: "Right now calling `spectra check` on a project that is not initialized gives the following output: `✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.` / `Initialize one:   specify init` / `Then add Spectra: spectra install`. There's no need to say 'Initialize one: specify init' because spectra install will do that anyways. So the message should say: `✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.` / `Initialize Specify and add Spectra: spectra install`"

## Clarifications

### Session 2026-10-08

- Q: Should the remedy line start flush left, as written in the request, or be indented two spaces like Spectra's other remedy lines? → A: Indented two spaces, matching the other project-state remedies.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - One command to get from nothing to a working project (Priority: P1)

A user runs `spectra check` in a folder that has never been set up with Spec Kit. Today Spectra tells
them to run two commands — `specify init`, then `spectra install` — even though `spectra install`
already detects the missing Spec Kit project and offers to initialize it in the same run. The extra
step is redundant, and a user who follows it literally runs `specify init` by hand and then sees
`spectra install` skip straight past the initialization it would have done for them.

After this change the diagnosis stays the same, but the remedy is a single command that does both:
`spectra install`.

**Why this priority**: It is the entire feature — the advice Spectra gives must match what Spectra
actually does, and the shortest correct path is the one to recommend.

**Independent Test**: Run `spectra check` in an empty folder with no `.specify/` directory anywhere
above it, and read the output.

**Acceptance Scenarios**:

1. **Given** a folder with no `.specify/` directory in it or any parent, **When** the user runs
   `spectra check`, **Then** the output is exactly two lines: the unchanged failure line
   `✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.` followed
   by `  Initialize Specify and add Spectra: spectra install` (indented two spaces).
2. **Given** the same folder, **When** the user runs `spectra check`, **Then** the output does not
   mention `specify init` anywhere.
3. **Given** the same folder, **When** the user follows the advice and runs `spectra install`,
   **Then** they are offered Spec Kit initialization and, on accepting, end with Spectra installed —
   no other command needed.
4. **Given** the same folder, **When** `spectra check` reports the problem, **Then** it exits with the
   same project-state exit code it uses today.

---

### User Story 2 - Same advice from every command that hits this state (Priority: P2)

The "not a Spec Kit project" report is shared: `spectra version`, `spectra update`, and
`spectra uninstall` print the same message when run outside a Spec Kit project. They must all give
the new single-step remedy, so the user never sees two different instructions for the same problem.

**Why this priority**: Consistency follows directly from P1, but is a separate thing to verify.

**Independent Test**: Run each of `spectra version`, `spectra update`, and `spectra uninstall` in the
same uninitialized folder and compare their output to `spectra check`'s.

**Acceptance Scenarios**:

1. **Given** a folder that is not a Spec Kit project, **When** the user runs any project-scoped
   command that reports this state, **Then** it prints the same two lines as `spectra check`.

---

### Edge Cases

- **A Spec Kit project without Spectra**: a different state with its own message ("Spectra is not
  installed in this project…"). It is unchanged by this feature.
- **A parent folder is a Spec Kit project**: the command finds it and never reports "not a Spec Kit
  project"; unchanged.
- **The user declines initialization during `spectra install`**: `spectra install` already explains
  that a Spec Kit project is required and how to create one by hand. That fallback guidance is
  unchanged — the hand-run `specify init` is still mentioned there, where it is the right advice.
- **Output without color/styling** (non-terminal or no-color): the text reads the same, with the
  command name unstyled.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: When a project-scoped command finds no `.specify/` directory in the current folder or
  any parent, Spectra MUST print the failure line
  `✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.` unchanged.
- **FR-002**: Directly after the failure line, Spectra MUST print exactly one remedy line:
  `Initialize Specify and add Spectra: spectra install`, indented two spaces to match the other
  project-state remedies, with `spectra install` emphasized the same way commands are emphasized
  elsewhere in Spectra's output.
- **FR-003**: The report MUST NOT recommend running `specify init` as a separate step.
- **FR-004**: The same report MUST be used by every command that detects this state (`check`,
  `version`, `update`, `uninstall`).
- **FR-005**: The exit code for this state MUST NOT change.
- **FR-006**: `spectra install`'s own handling of an uninitialized folder (offer to initialize; manual
  fallback if declined or failed) MUST NOT change.
- **FR-007**: The automated tests covering this state MUST assert the new remedy line and the
  absence of a separate `specify init` instruction.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user in an uninitialized folder needs to run exactly one command (down from two) to
  follow Spectra's advice to a working installation.
- **SC-002**: 100% of the commands that report "not a Spec Kit project" give identical remedy text.
- **SC-003**: The report is two lines long (down from three).
- **SC-004**: Every other project-state message and exit code is byte-for-byte unchanged.

## Assumptions

- "Specify" in the remedy line refers to Spec Kit's `specify` tool; the wording is the user's and is
  used verbatim.
- The change is to the `spectra` CLI only (the `spectra_cli/` channel). It ships under that channel's
  versioning and changelog rules; the Spectra extension (`spectra/`) is not touched and not bumped.
- Recommending `spectra install` from `spectra uninstall` in an uninitialized folder is acceptable:
  there is nothing to uninstall there, and setting up is the only meaningful next step.
