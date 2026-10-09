# Feature Specification: Check the spectra Command's Version From Anywhere

**Feature Branch**: `030-cli-version-check`

**Created**: 2026-10-08

**Status**: Implemented

**Input**: User description: "right now there's no command to check the CLI's version. Build a new command \"spectra cli version\". This should check the version of the CLI only, never the agents, and similar to \"spectra cli update\", it can be run from anywhere (not just specify project folders). If there's no update, the output simply says we're on the latest, if there's a new version available, the output indicates that says that user can run \"spectra cli update\" to update the cli."

## Background

In 6.0.0, `spectra cli version` was retired: `spectra version` reports all four parts of the stack —
the Spec Kit CLI, the core agents, the `spectra` command, and Spectra's agents — so a tool-scoped
version check seemed to have nothing left to mean. Typing `spectra cli version` today prints a
"has been retired" message pointing at `spectra version`.

That reasoning has the same hole feature 029 found in `spectra update`: `spectra version` is a
*project* command and refuses to run outside a Spec Kit project. Outside one, the only way to learn
the tool's version is to read the bare `spectra` banner, and there is no way at all to learn whether a
newer release exists. Feature 029 reinstated `spectra cli update` as a tool-only, location-independent
update; this feature gives it its natural partner — a tool-only, location-independent check that
answers "which `spectra` do I have, and is there a newer one?" and, when there is, names
`spectra cli update` as the next step.

## Clarifications

### Session 2026-10-08

- Q: Should `spectra version`'s "not a Spec Kit project" failure add a line pointing at `spectra cli version`? → A: Yes, for `spectra version` only; `spectra check` and `spectra uninstall` keep feature 028's two-line output, and `spectra update` keeps its 029 pointer.
- Q: When the newest release cannot be checked, should `spectra cli version` exit 0 or with the "unreachable" code? → A: Exit 0, reporting the installed version and that the newest release could not be checked — matching `spectra version`.
- Q: Should `--no-update-check` / `SPECTRA_NO_UPDATE_CHECK` stop `spectra cli version` from looking up the newest release? → A: Yes — it reports the installed version only and says the check was skipped, matching `spectra version`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Check the command's version from any folder (Priority: P1)

A user is in a folder with no `.specify/` directory anywhere above it — their home directory, a fresh
folder, a scratch directory. They want to know which `spectra` command they have and whether it is the
newest release, typically before running `spectra install`. They run `spectra cli version`. It tells
them their installed version and either that it is the latest, or that a newer version is available
and that `spectra cli update` will install it.

**Why this priority**: This is the gap the feature exists to close — today there is no way to ask
whether a newer `spectra` exists from outside a project.

**Independent Test**: In a folder with no `.specify/` directory in it or any parent, run
`spectra cli version` twice — once with the installed version equal to the newest release, once with
it older — and read the output of each.

**Acceptance Scenarios**:

1. **Given** any folder, and an installed `spectra` that is the newest release, **When** the user runs
   `spectra cli version`, **Then** the output names the installed version and says it is the latest,
   and does not mention `spectra cli update`.
2. **Given** any folder, and an installed `spectra` older than the newest release, **When** the user
   runs `spectra cli version`, **Then** the output names the installed version and the newer version,
   and tells the user they can run `spectra cli update` to update.
3. **Given** a folder with no `.specify/` directory in it or any parent, **When** the user runs
   `spectra cli version`, **Then** the output never says "This is not a Spec Kit project" and never
   asks the user to initialize or install anything.
4. **Given** a newer version is available, **When** `spectra cli version` runs, **Then** it does not
   prompt, does not update anything, and exits successfully — it only reports.

---

### User Story 2 - Check only the command, even inside a project (Priority: P1)

A user is inside a Spec Kit project with Spectra installed — possibly with out-of-date agents, an
out-of-date Spec Kit CLI, or a broken install. They run `spectra cli version` because they only care
about the tool. The output is about the `spectra` command alone: it does not list, check, or mention
the Spec Kit CLI, the core agents, Spectra's agents, or the state of the project.

**Why this priority**: "The CLI only, never the agents" is the explicit contract in the request, and it
is what distinguishes this command from `spectra version`.

**Independent Test**: In a Spec Kit project where every component is out of date, run
`spectra cli version` and confirm the output reports only the `spectra` command and the project's
working tree is unchanged.

**Acceptance Scenarios**:

1. **Given** a Spec Kit project whose Spec Kit CLI, core agents, and Spectra agents are all out of
   date, **When** the user runs `spectra cli version`, **Then** the output reports only the `spectra`
   command's version and update status.
2. **Given** a Spec Kit project whose Spectra install is incomplete or not present, **When** the user
   runs `spectra cli version`, **Then** the output is the same as it would be outside any project —
   no project-state message appears and the exit code is not a project-state code.
3. **Given** any project, **When** `spectra cli version` runs, **Then** no file in the current folder
   or any project is created, modified, or deleted.
4. **Given** the same project, **When** the user runs `spectra version` afterwards, **Then** it behaves
   exactly as it does today.

---

### User Story 3 - Discover the command from help (Priority: P2)

A user runs `spectra --help` or `spectra cli` to find out how to see the tool's version. The
**Tool commands — act on the spectra command itself** panel lists `cli version` alongside `cli update`
and `cli uninstall`, with a description making clear it reports the `spectra` command's version only
and works from any folder.

**Why this priority**: The command is only useful if users find it; it follows directly from P1 but is
separately verifiable.

**Independent Test**: Run `spectra --help` and `spectra cli` and read the Tool commands panel in each.

**Acceptance Scenarios**:

1. **Given** any folder, **When** the user runs `spectra --help`, **Then** the Tool commands panel lists
   `cli version`, `cli update`, and `cli uninstall`, in that order.
2. **Given** the `cli version` row, **When** the user reads its description, **Then** it states that it
   reports the `spectra` command's version and whether a newer release exists, works from any folder,
   and does not check the agents.
3. **Given** any folder, **When** the user runs `spectra cli` with no subcommand, **Then** its Tool
   commands panel lists `version`, `update`, and `uninstall`.
4. **Given** any folder, **When** the user runs `spectra cli version`, **Then** it no longer prints the
   "has been retired" message.

---

### User Story 4 - Point the stuck user at the new command (Priority: P3)

A user runs `spectra version` outside a Spec Kit project. The failure is still correct (there is no
stack here to report on), but it now also tells them how to check just the `spectra` command from where
they are — the same courtesy feature 029 added to `spectra update`.

**Why this priority**: It turns a dead end into a pointer, but the feature is complete without it.

**Independent Test**: Run `spectra version` in a folder with no `.specify/` directory anywhere above it
and read the output.

**Acceptance Scenarios**:

1. **Given** a folder with no `.specify/` directory in it or any parent, **When** the user runs
   `spectra version`, **Then** the output keeps the existing failure line and its
   `spectra install` remedy, and adds one further line naming `spectra cli version` as the way to check
   just the `spectra` command.
2. **Given** the same folder, **When** the user runs `spectra check` or `spectra uninstall`, **Then**
   their output is unchanged; `spectra update` keeps its existing `spectra cli update` pointer.
3. **Given** the same folder, **When** `spectra version` reports the problem, **Then** it exits with the
   same project-state exit code it uses today.

---

### Edge Cases

- **The newest release cannot be determined** (offline, rate-limited, blocked network): the command
  still reports the installed version, says the newest release could not be checked, and never claims
  the command is the latest or that an update is available. It exits 0 (FR-009).
- **Installed version is newer than the newest release** (a pre-release or local build): reported as
  the latest — the user is never told to "update" to an older version. The output may note that the
  installed version is ahead of the newest release.
- **Installed version cannot be determined**: the command says so rather than printing an empty or
  placeholder version as if it were real, and does not claim it is up to date.
- **Not installed as a uv tool** (source checkout, pip install) and a newer version exists: the command
  still reports the newer version, but because `spectra cli update` cannot update this installation,
  it names how to update it instead of (or alongside) `spectra cli update`, so the advice it gives
  actually works.
- **`--no-update-check` or `SPECTRA_NO_UPDATE_CHECK` is set**: the command makes no network request.
  It reports the installed version, says the update check was skipped, and exits 0 — matching
  `spectra version`, so air-gapped and CI runs never go online. It never shows the start-of-run nudge.
- **Non-interactive session** (CI, piped output): the command behaves the same, since it never prompts.
- **Extra arguments or flags meant for other commands** (`--force`, `--yes`): accepted where they are
  shared options and have no effect; the command remains read-only.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a `spectra cli version` command that reports the installed
  version of the `spectra` command and whether a newer published release exists.
- **FR-002**: `spectra cli version` MUST behave identically regardless of the current folder — whether
  or not a `.specify/` directory exists in it or any parent, and whatever state that project is in —
  and MUST NOT require, inspect, or report on a Spec Kit project.
- **FR-003**: `spectra cli version` MUST NOT check or report on the Spec Kit CLI, the core agents, or
  Spectra's agents, and MUST NOT create, modify, or delete any file anywhere.
- **FR-004**: When the installed version is the newest release (or newer), the output MUST name the
  installed version and say it is the latest, and MUST NOT mention `spectra cli update`.
- **FR-005**: When a newer release exists, the output MUST name the installed version and the newer
  version, and MUST tell the user they can run `spectra cli update` to update — except when the
  installation cannot update itself (FR-007).
- **FR-006**: `spectra cli version` MUST NOT prompt and MUST NOT perform any update, under any
  condition.
- **FR-007**: When a newer release exists but the command is not installed in a form `spectra cli
  update` can update (source checkout, pip install), the output MUST say how to update this
  installation instead, consistent with what `spectra cli update` itself says in that situation.
- **FR-008**: When the newest release cannot be determined, the output MUST still name the installed
  version, MUST say the newest release could not be checked, and MUST NOT report the command as the
  latest or as out of date.
- **FR-009**: Every delivered answer — latest, update available, ahead, newest-release unknown, or check
  skipped — MUST
  exit successfully, consistent with `spectra version`, so the command is safe to use in a shell
  without special error handling.
- **FR-010**: When `--no-update-check` or `SPECTRA_NO_UPDATE_CHECK` is set, `spectra cli version`
  MUST NOT contact the network; it MUST report the installed version and state that the update check
  was skipped, without claiming the command is the latest or out of date. It MUST NOT show the
  start-of-run update nudge in any case.
- **FR-011**: `spectra cli version` MUST use the same source for the newest release and the same version
  comparison as `spectra cli update`, `spectra version`, and the start-of-run nudge, so they never
  disagree about whether an update exists.
- **FR-012**: `spectra cli version` MUST no longer print the "has been retired" message.
- **FR-013**: `spectra --help` MUST list `cli version` in the "Tool commands — act on the spectra
  command itself" panel, before `cli update`, with a description stating that it reports only the
  `spectra` command's version and works from any folder. `spectra cli` with no subcommand MUST list
  `version` alongside `update` and `uninstall`.
- **FR-014**: `spectra version` MUST keep its current behavior in every project state, including
  reporting the `spectra` command as one of the four components.
- **FR-015**: When `spectra version` is run outside a Spec Kit project, its output MUST add one line,
  after the existing remedy, naming `spectra cli version` as the way to check just the `spectra`
  command. The not-a-project output of `spectra check` and `spectra uninstall` MUST be unchanged, and
  `spectra update` MUST keep its existing `spectra cli update` line.
- **FR-016**: User-facing documentation that describes the tool commands — including the README's
  "Changed in 6.0.0" note, which says `spectra cli version` is still retired — MUST be updated to
  describe the reinstated command and its narrower, location-independent meaning.
- **FR-017**: The automated test suite MUST cover: running from a non-project folder, running inside a
  project (in each project state) without reporting on or touching it, up to date, update available,
  ahead, newest-release unknown, installed-version unknown, not uv-managed with an update available,
  the update-check opt-outs, and the help listings; and tests that currently assert `cli version` is
  retired MUST be updated accordingly.

### Key Entities

- **Installed `spectra` command**: the copy of the tool on this machine; has a version (possibly
  undeterminable) and an installation kind (updatable by `spectra cli update`, or not).
- **Newest release**: the most recent published release of the `spectra` command, determined from the
  same source the other update and version checks already use; may be undeterminable when offline.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: From any folder, a user can learn their `spectra` version and whether a newer one exists
  with a single command, without being prompted and without needing a Spec Kit project.
- **SC-002**: When an update exists, 100% of outputs name a next step that actually works for the
  user's installation — `spectra cli update` for an installation it can update, the alternative
  otherwise.
- **SC-003**: In 100% of runs of `spectra cli version`, no file anywhere is created, modified, or
  deleted, and nothing about the agents or the Spec Kit CLI appears in the output.
- **SC-004**: No run ever reports "latest" or "update available" unless the newest release was actually
  determined and compared.
- **SC-005**: A user reading `spectra --help` for the first time can identify how to check the tool's
  own version from the Tool commands panel alone.

## Assumptions

- Reinstating `spectra cli version` is a deliberate, narrower re-use of a name retired in 6.0.0,
  following the same reasoning feature 029 used for `spectra cli update`: `spectra version` remains the
  whole-stack report, and a tool-scoped check is the only kind that works outside a project.
- The command is read-only and informational, like `spectra version`: it reports and points at
  `spectra cli update`, but never offers to run it. That keeps a "check" from turning into an action.
- Exit status follows `spectra version`'s rule (confirmed in Clarifications) — a delivered answer
  exits 0, including "could not check" — rather than `spectra cli update`'s, which exits non-zero when unreachable because it was
  asked to *do* something it could not.
- The `spectra version` pointer in FR-015 (User Story 4, confirmed in Clarifications) mirrors feature
  029's `spectra update` pointer and further narrows feature 028's "exactly two lines" not-a-project
  contract for `spectra version` only.
- The bare `spectra` banner keeps showing the installed version; this feature does not change it.
- This is an additive change to the CLI channel only (Principle VI): it bumps the root `VERSION` by a
  minor version and does not touch the extension, catalog, or package.
