# Feature Specification: Update the spectra Command From Anywhere

**Feature Branch**: `029-cli-self-update`

**Created**: 2026-10-08

**Status**: Implemented

**Input**: User description: "Right now it's not possible to update the SPECTRA CLI on a folder that specify is not initialized. `% spectra update` / `✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.` We need to have a new command \"spectra cli update\" that no matter where we run this from, it will attempt to update the CLI itself without attempting to update spec-kit extensions. This should also be reflected on \"spectra --help\" under \"Tool commands — act on the spectra command itself\""

## Background

In 6.0.0, `spectra cli update` was retired and its job absorbed into `spectra update`, which brings the
whole stack current — the Spec Kit CLI, the core agents, the `spectra` command, and Spectra's agents.
That made the common case one command, but it left a gap: `spectra update` is a *project* command, so
it refuses to run outside a Spec Kit project. A user who only wants a newer `spectra` command — before
running `spectra install` in a fresh folder, on a machine with no projects yet, or from their home
directory — currently has no way to get it short of typing the underlying `uv` command by hand.

This feature reinstates `spectra cli update` with a narrower, location-independent meaning: it updates
**the `spectra` command itself, and nothing else**. It sits beside `spectra cli uninstall` as the second
tool command — the two verbs that act on the machine's copy of the tool rather than on any project.
`spectra update` keeps its meaning and keeps updating the command as part of the stack.

## Clarifications

### Session 2026-10-08

- Q: When a newer version exists, should `spectra cli update` ask before installing, or just go ahead? → A: Ask first; `--yes` skips the prompt; non-interactive without `--yes` refuses and changes nothing — matching `spectra update` and `spectra cli uninstall`.
- Q: Should `spectra update`'s "not a Spec Kit project" failure add a line pointing at `spectra cli update`? → A: Yes, for `spectra update` only; `spectra check`, `spectra version`, and `spectra uninstall` keep feature 028's two-line output.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update the command from a folder that is not a Spec Kit project (Priority: P1)

A user is in a folder with no `.specify/` directory anywhere above it — a fresh folder, their home
directory, a scratch directory. They want the newest `spectra` command, typically so that the
`spectra install` they are about to run uses the latest onboarding flow. They run `spectra cli update`;
it finds the newest released version, confirms with them, updates the command, and tells them which
version they now have.

**Why this priority**: This is the gap the feature exists to close — today there is no way to do this
at all through `spectra`.

**Independent Test**: In a folder with no `.specify/` directory in it or any parent, with an older
`spectra` installed, run `spectra cli update`, accept the prompt, and confirm that the bare `spectra`
banner afterwards reports the newer version.

**Acceptance Scenarios**:

1. **Given** a folder with no `.specify/` directory in it or any parent, and an installed `spectra`
   older than the newest release, **When** the user runs `spectra cli update` and confirms, **Then**
   the command is updated to the newest release and the output names the old and new versions.
2. **Given** the same folder, **When** the user runs `spectra cli update`, **Then** the output never
   says "This is not a Spec Kit project", and never asks the user to initialize anything.
3. **Given** the update succeeded, **When** the command finishes, **Then** it tells the user the new
   version takes effect on their next `spectra` invocation (the process that ran the update is the old
   code).
4. **Given** the installed `spectra` is already the newest release, **When** the user runs
   `spectra cli update`, **Then** it reports that the command is already up to date, changes nothing,
   does not prompt, and exits successfully.

---

### User Story 2 - Update only the command, even inside a project (Priority: P1)

A user is inside a Spec Kit project with Spectra installed, and wants a newer `spectra` command without
touching the project — perhaps because their team has pinned the Spec Kit CLI or the agents, or because
they are mid-change and do not want managed files rewritten. They run `spectra cli update`. Only the
`spectra` command changes; the Spec Kit CLI, the core agents, Spectra's agents, and every file in the
project are left exactly as they were.

**Why this priority**: "Only the CLI, never the extensions" is the explicit contract in the request. It
is what makes the command safe to run anywhere — including somewhere it could have done more.

**Independent Test**: In a Spec Kit project with Spectra installed and every component out of date, run
`spectra cli update`, accept, then confirm that only the `spectra` command's version changed and the
project's working tree is byte-for-byte unchanged.

**Acceptance Scenarios**:

1. **Given** a Spec Kit project where the Spec Kit CLI, the core agents, Spectra's agents, and the
   `spectra` command are all out of date, **When** the user runs `spectra cli update` and confirms,
   **Then** only the `spectra` command is updated; the other three are untouched.
2. **Given** the same project, **When** `spectra cli update` runs, **Then** no file inside the project
   (including everything under `.specify/` and every agent's command directory) is created, modified,
   or deleted.
3. **Given** the same project, **When** `spectra cli update` runs, **Then** its plan and its prompt name
   only the `spectra` command — they do not list, check, or mention the other components.
4. **Given** `spectra cli update` has finished inside a project, **When** the user later runs
   `spectra update`, **Then** it behaves exactly as it does today, reporting the `spectra` command as
   current and offering the remaining components.

---

### User Story 3 - Discover the command from help (Priority: P2)

A user runs `spectra --help` to find out how to update the tool. The **Tool commands — act on the
spectra command itself** panel lists `cli update` alongside `cli uninstall`, with a description that
makes clear it updates the command only and works from anywhere. `spectra cli` (the group, with no
subcommand) lists it too.

**Why this priority**: The command is only useful if users find it; help is where they look first. It
follows directly from P1 but is separately verifiable.

**Independent Test**: Run `spectra --help` and `spectra cli`, and read the Tool commands panel in each.

**Acceptance Scenarios**:

1. **Given** any folder, **When** the user runs `spectra --help`, **Then** the "Tool commands — act on
   the spectra command itself" panel contains a `cli update` row and a `cli uninstall` row, with
   `cli update` listed first.
2. **Given** the `cli update` row, **When** the user reads its description, **Then** it states that it
   updates the `spectra` command to the newest release, works from any folder, and does not touch the
   agents in any project.
3. **Given** any folder, **When** the user runs `spectra cli` with no subcommand, **Then** its Tool
   commands panel lists `update` and `uninstall`, and its introductory text no longer says that
   updating the command requires a top-level command.

---

### User Story 4 - Point the stuck user at the new command (Priority: P3)

A user runs `spectra update` outside a Spec Kit project — exactly the situation in the request. The
failure is still correct (there is no stack here to update), but it now also tells them how to update
just the `spectra` command from where they are.

**Why this priority**: It turns the dead end the user hit into a pointer to the fix, but the feature is
complete and usable without it.

**Independent Test**: Run `spectra update` in a folder with no `.specify/` directory anywhere above it,
and read the output.

**Acceptance Scenarios**:

1. **Given** a folder with no `.specify/` directory in it or any parent, **When** the user runs
   `spectra update`, **Then** the output keeps the existing failure line and its
   `Initialize Specify and add Spectra: spectra install` remedy, and adds one further line naming
   `spectra cli update` as the way to update just the `spectra` command.
2. **Given** the same folder, **When** the user runs `spectra check`, `spectra version`, or
   `spectra uninstall`, **Then** their output is unchanged from today — the extra line appears only for
   `spectra update`, the one command whose intent it answers.
3. **Given** the same folder, **When** `spectra update` reports the problem, **Then** it exits with the
   same project-state exit code it uses today.

---

### Edge Cases

- **Not installed as a uv tool** (running from a source checkout, or installed with pip): the command
  changes nothing, says it cannot update itself in this installation, and names how to update it
  instead. It does not attempt the update and does not prompt.
- **The installer it relies on is missing from the machine**: the command fails without changing
  anything and prints the exact manual command to run.
- **The newest release cannot be determined** (offline, rate-limited, blocked network): the command
  says the update check could not be completed, changes nothing, and exits with the existing
  "published data could not be retrieved" exit code. It never reports "already up to date" in this
  state.
- **The update itself fails partway**: the command reports the failure, states that the installed
  version is unchanged, and prints the manual command to run (including the fresh-shell advice for
  platforms that lock the running executable).
- **Non-interactive session without `--yes`**: the command refuses to update without confirmation,
  explains how to re-run with `--yes`, and exits with the "declined" exit code, as `spectra update`
  does in this situation. With `--yes` it updates without prompting.
- **The user declines the prompt**: nothing changes, and the command exits with the existing
  "declined" exit code.
- **Installed version is newer than the newest release** (a pre-release or local build): treated as
  up to date; the command never offers a downgrade.
- **`--no-update-check` or `SPECTRA_NO_UPDATE_CHECK` is set**: those opt out of the *unprompted*
  start-of-run check. `spectra cli update` is an explicit request to check, so it still runs, and it
  does not additionally trigger the start-of-run nudge.
- **`spectra cli update` inside a project whose Spectra install is incomplete or broken**: irrelevant
  to this command; it updates the `spectra` command and does not report on, or repair, the project.
- **`spectra cli version`**: remains retired and keeps naming `spectra version` as its replacement.
  Only `cli update` is reinstated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a `spectra cli update` command that updates the installed
  `spectra` command to the newest published release.
- **FR-002**: `spectra cli update` MUST behave identically regardless of the current folder — whether
  or not a `.specify/` directory exists in it or any parent — and MUST NOT require, inspect, or report
  on a Spec Kit project.
- **FR-003**: `spectra cli update` MUST NOT check, install, update, or remove the Spec Kit CLI, the
  Spec Kit core agents, or Spectra's agents, and MUST NOT create, modify, or delete any file in the
  current folder or any project.
- **FR-004**: Before updating, the command MUST show the installed version and the version it will
  update to, and MUST ask for confirmation; `--yes` (before or after the subcommand) MUST skip the
  prompt.
- **FR-005**: In a non-interactive session without `--yes`, the command MUST refuse to update, say how
  to re-run with `--yes`, and change nothing.
- **FR-006**: When the installed version is already the newest release (or newer), the command MUST
  say so, change nothing, not prompt, and exit successfully.
- **FR-007**: When the newest release cannot be determined, the command MUST say the check could not be
  completed, change nothing, and exit with the existing "unreachable" exit code — never reporting the
  command as up to date.
- **FR-008**: When the command is not installed in a form it can update itself (source checkout, pip
  install), it MUST change nothing, explain why, and say how to update it instead, without prompting.
- **FR-009**: When the update fails, the command MUST report that the installed version is unchanged
  and print the exact manual command that performs the same update.
- **FR-010**: After a successful update, the command MUST name the new version and tell the user it
  takes effect the next time they run `spectra`.
- **FR-011**: `spectra cli update` MUST run its check even when `--no-update-check` or
  `SPECTRA_NO_UPDATE_CHECK` is set, and MUST NOT additionally show the start-of-run update nudge.
- **FR-012**: `spectra --help` MUST list `cli update` in the "Tool commands — act on the spectra
  command itself" panel, before `cli uninstall`, with a description stating that it updates only the
  `spectra` command and works from any folder.
- **FR-013**: `spectra cli` with no subcommand MUST list `update` alongside `uninstall`, and its
  introductory text MUST no longer state that updating the command requires a top-level command.
- **FR-014**: `spectra cli update` MUST no longer print the "has been retired" message.
  `spectra cli version` MUST continue to print it, naming `spectra version`.
- **FR-015**: `spectra update` MUST keep its current behavior in every project state, including
  updating the `spectra` command as part of the stack.
- **FR-016**: When `spectra update` is run outside a Spec Kit project, its output MUST add one line,
  after the existing remedy, naming `spectra cli update` as the way to update just the `spectra`
  command. The not-a-project output of `spectra check`, `spectra version`, and `spectra uninstall` MUST
  be unchanged.
- **FR-017**: User-facing documentation that describes the tool commands (including the README's
  "Changed in 6.0.0" note, which says `spectra cli update` was retired) MUST be updated to describe the
  reinstated command and its narrower, location-independent meaning.
- **FR-018**: The automated test suite MUST cover: running from a non-project folder, running inside a
  project without touching it, already-current, unreachable, not-uv-managed, declined, non-interactive
  without `--yes`, failed update, and the help listings.

### Key Entities

- **Installed `spectra` command**: the copy of the tool on this machine; has a version and an
  installation kind (updatable by itself, or not).
- **Newest release**: the most recent published release of the `spectra` command, determined from the
  same source `spectra update` and the start-of-run nudge already use.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: From a folder with no Spec Kit project anywhere above it, a user can go from an outdated
  `spectra` command to the newest one with a single command and a single confirmation.
- **SC-002**: In 100% of runs of `spectra cli update` — inside or outside a project — no file outside
  the tool's own installation is created, modified, or deleted.
- **SC-003**: A user reading `spectra --help` for the first time can identify the command that updates
  only the `spectra` tool from the Tool commands panel alone, without reading any other documentation.
- **SC-004**: A user who hits the "not a Spec Kit project" failure from `spectra update` is shown the
  working command in the same output, so they need no further lookup to update the tool.
- **SC-005**: No outcome of `spectra cli update` that left the installed version unchanged (unreachable,
  declined, failed, not updatable) is ever reported as an update or as "already up to date" unless the
  installed version actually is the newest release.

## Assumptions

- Reinstating `spectra cli update` is a deliberate, narrower re-use of a name retired in 6.0.0, not a
  reversal of that decision: `spectra update` remains the whole-stack command, and the retirement's
  reasoning ("a tool-scoped update had nothing left to mean") no longer holds once the tool-scoped
  update is the only one that works outside a project.
- The command uses the same release source, version comparison, and update mechanism that
  `spectra update` and the start-of-run nudge already use for the `spectra` component, so the three
  can never disagree about what "newest" means.
- Confirmation behavior (prompt, `--yes`, refusal when non-interactive) and exit codes match the
  existing confirm-gated commands, `spectra update` and `spectra cli uninstall`.
- `--force` stays scoped to `spectra update`; it has no meaning for `spectra cli update`, which never
  overwrites project files.
- This is an additive change to the CLI channel only (Principle VI): it bumps the root `VERSION` by a
  minor version and does not touch the extension, catalog, or package.
- The extra pointer line in FR-016 (confirmed in Clarifications) deliberately narrows feature 028's
  "exactly two lines" contract for `spectra update` only; `spectra check`, `spectra version`, and
  `spectra uninstall` keep the exact two-line output 028 specified.
