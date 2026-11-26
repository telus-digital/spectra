# Feature Specification: Retire the spectra CLI

**Feature Branch**: `043-retire-spectra-cli`

**Created**: 2026-11-25

**Status**: Implemented

**Input**: User description: "Remove the spectra CLI from the repository entirely, so SPECTRA is distributed and managed only as an extension by TELUS Digital that enhances GitHub Spec Kit, installed, updated and removed with Spec Kit's own specify CLI (specify extension catalog add / extension add / extension update / extension remove). The CLI has no external users and internal users will be told directly, so there is no deprecation release and no legacy-user guidance in the docs. The agents do not change: the spectra/ extension, its commands, templates, package and version stay as they are. Remove the CLI and everything that exists only for it: spectra_cli/, pyproject.toml, VERSION, the release workflow, the CLI-only tests and the test/ Docker harness. Move the roster and manifest-version parsers that tools/ still needs into tools/, and repoint the tests that depend on them. Retire the CLI's git tags and GitHub Releases (3.0.0 to 6.5.1). catalog.json, docs/packages/spectra.zip and agents-list.json stay at their current URLs, because specify installs from the first two and the agents page reads the third. Amend the constitution to a single release channel (the extension, released by merging to main), with no CLI anywhere in it, and state that the repository carries no git tags and no GitHub Releases. Update CLAUDE.md, CONTRIBUTING.md, SECURITY.md and SHIPPING.md to match. SHIPPING.md keeps only the extension and housekeeping paths, with the new required-check names. Replace the required CI checks named 'CLI installs and runs (3.9)' and '(3.12)' with a test job that does not install a package. Follow SHIPPING.md's rename-deadlock procedure so main stays pushable throughout. The live ruleset change is made by the maintainer. Rewrite installation and positioning across README.md and docs/ so SPECTRA consistently reads as an extension by TELUS Digital that enhances GitHub Spec Kit: docs/index.html (one specify-based install path, keep-current and remove steps, the CLI version badge removed, new title, lede and footer); docs/capability-brief.html (trust and telemetry cards reflect that TELUS Digital ships no executable code, stale command and template counts corrected, 'platform' wording replaced); docs/getting-started/index.html (lead from 'Start with Spec Kit' straight into adding SPECTRA); every page under docs/e-learning/ (replace spectra install, check, version, update, agent-list and cli commands with their specify equivalents, including module-3's install lab and module-4's prerequisites); the shared footer tagline on every docs page. Historical records (specs/, spectra/CHANGELOG.md, docs/ip-audit-findings.md) are left unchanged. Open question for clarify: Spec Kit registers an extension's commands only for the active integration, and an update re-registers them for the default only. Verify whether current Spec Kit still behaves this way. If it does, document the manual specify integration use steps for projects with more than one agent installed."

## Clarifications

### Session 2026-11-25

- Q: Which Spec Kit version should the rewritten install, update and e-learning instructions be checked
  against? → A: The latest Spec Kit release at implementation time; its exact version is recorded in the
  plan and the README, and `extension.yml` and `catalog.json` are left as they are. (FR-027, FR-029, SC-007)
- Q: Who deletes the CLI's GitHub Releases and git tags, and when? → A: The maintainer, after the change
  lands on `main`. `tasks.md` carries it as a maintainer step with the exact commands and a check that none
  remain; implementation does not run them. (FR-007, FR-030, SC-004)
- Q: Should the new required test check run on one Python version or on two, as the CLI check does today?
  → A: One version only, the current stable Python the CI runner provides, as a single required check; the
  3.9 minimum is dropped. (FR-009, FR-010)

## Context

SPECTRA reaches users today through two independently versioned channels (constitution Principle VI):

| Channel | What it is | How it is released |
|---|---|---|
| **Catalog** | The `spectra` Spec Kit extension: 14 agent commands, 13 templates, licence, notice, trademark policy, changelog. Markdown and YAML only. | Merging to `main`; served from the raw `catalog.json` and `docs/packages/spectra.zip` URLs. Never tagged. |
| **CLI** | The `spectra` command (`spectra_cli/`, Python): bootstraps Spec Kit, runs `specify init`, registers the catalog, installs the extension, reports and updates the whole stack, and registers the extension for every installed agent integration. | A bare-semver git tag plus a GitHub Release (3.0.0 to 6.5.1). |

Everything the CLI does is a wrapper around `specify` commands that a user can run directly, and the
manual `specify` path is already documented. The CLI has no external users. Keeping it costs a second
release channel, a Python package, a release workflow, two required CI checks, a Docker test harness, and
documentation that presents SPECTRA as a tool to install rather than as what it is: an extension that
enhances GitHub Spec Kit.

This feature retires the CLI completely and makes the extension the only thing SPECTRA ships. Nothing a
user's agent runs changes: the extension's commands, templates, package, and version are untouched.

## Decisions recorded so they are not re-proposed

- **No deprecation or farewell CLI release.** The CLI has no external users; the maintainer tells internal
  users directly. No final version is cut to announce the retirement.
- **No legacy-user guidance in the docs.** The docs describe only the `specify`-based path. They do not
  carry an "if you still have the `spectra` command" section.
- **Tags and Releases are retired, not frozen.** The CLI's git tags and GitHub Releases (3.0.0 to 6.5.1) are
  removed. This supersedes the earlier decision to keep tags.
- **The extension does not change.** No extension version bump, no package rebuild, no `spectra/CHANGELOG.md`
  entry, because nothing under `spectra/` changes.
- **Distribution URLs stay.** `catalog.json` and `docs/packages/spectra.zip` stay where they are because
  `specify` installs from them; `agents-list.json` stays because the roster page reads it.
- **Historical records stay as written.** `specs/`, `spectra/CHANGELOG.md`, and `docs/ip-audit-findings.md`
  describe what was true when they were written and are not rewritten.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - A new user installs SPECTRA with Spec Kit alone (Priority: P1)

A developer who has never used SPECTRA opens the landing page, follows one install path, and ends up with
SPECTRA's commands available in their coding agent. Every step uses Spec Kit's `specify` CLI; no other
tool is installed and no step mentions a `spectra` command.

**Why this priority**: Installation is the first thing every user does. If the documented path still
depends on a tool that no longer exists, SPECTRA cannot be installed at all.

**Independent Test**: In a clean environment with only the documented prerequisites, follow the landing
page's install steps verbatim into a new Spec Kit project, restart the agent, and confirm a
`speckit.spectra.*` command is offered.

**Acceptance Scenarios**:

1. **Given** a machine with the documented prerequisites and no Spec Kit project, **When** the user follows
   the landing page's install steps in order, **Then** the project has Spec Kit initialized, the SPECTRA
   catalog registered as an install-allowed source, and the `spectra` extension installed.
2. **Given** the landing page, **When** a reader looks for how to install SPECTRA, **Then** they find exactly
   one install path, and every command in it is a `specify` command or a prerequisite installer.
3. **Given** an existing Spec Kit project, **When** the user runs only the catalog and extension steps,
   **Then** SPECTRA installs without re-initializing the project.

---

### User Story 2 - Readers understand SPECTRA as an extension that enhances Spec Kit (Priority: P1)

Anyone reading the landing page, the capability brief, the getting-started pages, the e-learning course, or
the README comes away understanding that SPECTRA is an extension by TELUS Digital that enhances GitHub Spec
Kit, installed and managed through Spec Kit, and not a separate tool or platform.

**Why this priority**: The positioning change is the purpose of the feature. A page that still calls
SPECTRA a "curated catalog", a "platform", or something you install with its own command contradicts it.

**Independent Test**: Read each named page and confirm the product description, title, lede, and footer
describe SPECTRA as a Spec Kit extension by TELUS Digital, and that no page names a `spectra` command.

**Acceptance Scenarios**:

1. **Given** any page under `docs/` or the README, **When** it describes what SPECTRA is, **Then** it calls
   SPECTRA an extension by TELUS Digital that enhances GitHub Spec Kit.
2. **Given** the capability brief, **When** a security or compliance reviewer reads its trust section,
   **Then** it states that TELUS Digital ships no executable code (only Markdown command files and
   templates that Spec Kit installs), that SPECTRA itself makes no network calls, and its counts of command
   files and templates match the published extension.
3. **Given** the getting-started overview page, **When** a reader finishes the "Start with Spec Kit" section,
   **Then** the page leads them directly to adding SPECTRA to that Spec Kit project.

---

### User Story 3 - A user keeps SPECTRA current and removes it with Spec Kit (Priority: P2)

A developer with SPECTRA installed finds documented `specify` commands to check what is installed, bring
Spec Kit and SPECTRA up to date, and remove SPECTRA from a project.

**Why this priority**: Day-two operations were the CLI's other main job. Without documented replacements,
users would not know how to update or uninstall.

**Independent Test**: In a project with SPECTRA installed, follow the documented keep-current and remove
steps and confirm each does what the docs say.

**Acceptance Scenarios**:

1. **Given** a project with SPECTRA installed, **When** the user follows the documented update steps,
   **Then** Spec Kit and the SPECTRA extension are brought to their latest published versions.
2. **Given** a project with SPECTRA installed, **When** the user follows the documented remove step,
   **Then** SPECTRA's commands are gone from the project and nothing outside the extension is touched.
3. **Given** a project with more than one agent integration installed, **When** the user follows the docs,
   **Then** the docs state accurately whether SPECTRA's commands reach every installed agent, and if they do
   not by default, give the steps that make them do so and restore the original default agent.

---

### User Story 4 - The e-learning course works without the CLI (Priority: P2)

A learner works through the e-learning course, including the install lab in Module 3 and the prerequisites
of Module 4, using only `specify` commands, and every exercise still runs.

**Why this priority**: The course is the main onboarding route for new teams. A lab that tells learners to
install a tool that no longer exists stops them at the first step.

**Independent Test**: Follow every command in every e-learning page against a current Spec Kit project and
confirm none references a `spectra` command and each works as described.

**Acceptance Scenarios**:

1. **Given** Module 3's install lab, **When** a learner follows it, **Then** they install SPECTRA with
   `specify` commands only and can confirm their agent sees both Spec Kit and SPECTRA commands.
2. **Given** any e-learning page that told the learner to check or update their Spec Kit version, **When**
   they read it now, **Then** it names the `specify` command that does that.
3. **Given** Module 4's prerequisites, **When** a learner reads them, **Then** no SPECTRA CLI is listed.

---

### User Story 5 - The maintainer ships with one release channel (Priority: P3)

The maintainer changes an agent or a doc and lands it exactly as before, through the gated ship process,
but there is now only one thing to version and no tag or Release to cut. The governing documents describe
that single channel and nothing else.

**Why this priority**: The maintainer is the only person affected, and the gate must keep working, but no
end user sees this directly.

**Independent Test**: After the change lands, run the documented ship procedure on a trivial change and
confirm it lands on `main`; read the constitution and contributor docs and confirm no CLI channel, tag, or
Release is described.

**Acceptance Scenarios**:

1. **Given** the change has landed, **When** the maintainer ships any later change, **Then** `main` accepts
   it with the new set of required checks and no step refers to the CLI.
2. **Given** the constitution, `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `SHIPPING.md`, **When**
   the maintainer reads them, **Then** they describe one release channel (the extension, released by merging
   to `main`), state that the repository carries no git tags and no GitHub Releases, and describe no CLI.
3. **Given** the switch of required checks, **When** it is carried out, **Then** there is no point at which
   `main` cannot accept a correctly tested push.

---

### Edge Cases

- **Projects already managed by the CLI.** A project set up by `spectra install` already has the SPECTRA
  catalog registered and the extension installed, so the `specify` update and remove commands work on it
  with no migration. The docs do not need a migration step.
- **Required-check switch out of order.** If the old CI checks are removed before the live ruleset stops
  requiring them, `main` becomes unpushable and the fix cannot be pushed. The switch must follow the
  documented rename procedure, and the maintainer makes the ruleset change.
- **Something still reads a Release.** Once Releases are deleted, any page or script that asks GitHub for
  the latest Release gets nothing. No published page may depend on a Release after this change.
- **The roster page.** `docs/agents.html` reads `agents-list.json` at load time; the file, its URL, and its
  shape stay as they are, even though `spectra agent-list` no longer reads it.
- **Footer inside generated pages.** The agents reference page mixes generated regions with hand-written
  content. The footer tagline is outside the generated regions, and generated content still comes only from
  `agents/`.
- **Words that only look like CLI references.** Mentions of other tools' CLIs (`gh`, Claude Code, Kiro CLI,
  the `specify` CLI itself) and agents that classify a project as "a CLI" are not SPECTRA CLI references and
  stay.
- **Multi-agent behaviour differs by Spec Kit version.** If current Spec Kit already registers an extension
  for every installed integration, the docs say so and give no workaround; if it does not, the docs give the
  manual steps. What the docs say must match the baseline Spec Kit version (FR-029).

## Requirements *(mandatory)*

### Functional Requirements

**Removing the CLI**

- **FR-001**: The repository MUST no longer contain the `spectra` CLI: its source package, its Python
  packaging metadata, its version file, its release workflow, the tests that exist only to test it, and the
  Docker-based clean-room harness that exercises it.
- **FR-002**: Maintainer tooling that currently reuses CLI code (the agent roster parser and the manifest
  version parser) MUST keep working, with that logic owned by the maintainer tooling instead of the CLI.
- **FR-003**: Tests that cover the extension, the generator, the catalog checks, the CI contract, and the
  CodeQL gate MUST keep passing, repointed wherever they referred to CLI code or CLI paths.
- **FR-004**: The repository MUST keep its zero-third-party-dependency rule for everything that remains.
- **FR-005**: Everything under `spectra/` MUST remain unchanged, and the extension version, `catalog.json` entry, and
  `docs/packages/spectra.zip` MUST stay as they are.
- **FR-006**: `catalog.json`, `docs/packages/spectra.zip`, and `agents-list.json` MUST stay at their current
  paths and published URLs.

**Tags and Releases**

- **FR-007**: All of the CLI's GitHub Releases (3.0.0 through 6.5.1) and their git tags MUST be removed from
  the repository.
- **FR-030**: The removal in FR-007 MUST be carried out by the maintainer after the change has landed on
  `main`, not by the implementation run. The task list MUST include it as a maintainer step that gives the
  exact commands and a check that confirms no tag and no Release remain.
- **FR-008**: Published pages MUST NOT read or display a GitHub Release or tag after this change; the
  landing page's CLI version badge MUST be removed, and its extension version badge, read from
  `catalog.json`, MUST stay.

**Continuous integration and shipping**

- **FR-009**: The two required checks "CLI installs and runs (3.9)" and "CLI installs and runs (3.12)" MUST
  be replaced by a single required check that runs the full test suite on one Python version (the current
  stable release the CI runner provides) without installing any package. The Python 3.9 minimum that came
  from the CLI's packaging is no longer enforced.
- **FR-010**: The committed list of required checks, the CI contract test, and the live ruleset MUST agree
  on the new check names when the change lands.
- **FR-011**: The required-check switch MUST follow `SHIPPING.md`'s rename procedure, so that `main`
  accepts a correctly tested push at every point. The live ruleset change is made by the maintainer.
- **FR-012**: The remaining required checks ("Catalog and package stay in sync" and "CodeQL finds no
  high-severity issues") MUST keep their names and their behaviour.

**Governing documents**

- **FR-013**: The constitution MUST describe a single release channel: the `spectra` extension, versioned
  in `spectra/extension.yml`, mirrored into `catalog.json`, and released by merging to `main`.
- **FR-014**: The constitution MUST state that the repository carries no git tags and no GitHub Releases.
- **FR-015**: The constitution MUST NOT mention the CLI anywhere: not in Principle I's definition of feature
  work, not in Principle V's description of `agents-list.json` or of what the landing page reads, not in
  Principle VI, and not in the publishing standards.
- **FR-016**: `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `SHIPPING.md` MUST match the amended
  constitution. `SHIPPING.md` MUST keep only the extension path and the docs/tooling/housekeeping path, MUST
  list the new required-check names, and MUST drop the CLI release path, the release-tag check, the
  "Latest" Release warning, and the CLI smoke test.

**Positioning and installation docs**

- **FR-017**: Wherever a page under `docs/` or the README describes what SPECTRA is, it MUST describe SPECTRA
  as an extension by TELUS Digital that enhances GitHub Spec Kit. The phrases "curated catalog of Spec Kit
  extensions" and "A TELUS Digital platform" MUST no longer appear on any page under `docs/` or in the
  README.
- **FR-018**: The shared footer tagline on every docs page that carries it MUST use the new description.
- **FR-019**: The landing page MUST have a new title, meta description, lede, and footer that match FR-017,
  MUST present exactly one install path made of `specify` commands and prerequisite installers, and MUST
  include keep-current and remove steps that use `specify` commands.
- **FR-020**: The landing page MUST NOT offer an "install with uv, one command" action, describe SPECTRA as
  "installed as a uv tool", or list prerequisites that only the CLI needed.
- **FR-021**: The capability brief's trust section MUST state that TELUS Digital ships no executable code
  and that SPECTRA itself makes no network calls; its counts of command files and templates MUST match the
  published extension (14 command files and 13 templates today); and its "platform" wording MUST be
  replaced.
- **FR-022**: The getting-started overview page MUST lead from its "Start with Spec Kit" section directly
  into adding SPECTRA, giving the `specify` commands that do it.
- **FR-023**: Every page under `docs/e-learning/` MUST replace `spectra install`, `check`, `version`,
  `update`, `agent-list`, and `cli` commands with their `specify` equivalents, including Module 3's install
  lab and Module 4's prerequisites, and every exercise MUST still work with those commands.
- **FR-024**: The README MUST replace its CLI installation, update, and release-channel sections with the
  `specify`-based install, keep-current, multi-agent, and remove steps.
- **FR-025**: Current documentation (README, `docs/`, the constitution, `CLAUDE.md`, `CONTRIBUTING.md`,
  `SECURITY.md`, `SHIPPING.md`) MUST NOT name a `spectra` CLI command, the `spectra-cli` package, or a CLI
  release. Historical records (`specs/`, `spectra/CHANGELOG.md`, `docs/ip-audit-findings.md`) MUST be left
  unchanged.
- **FR-026**: The documentation MUST NOT include guidance aimed at people who still have the `spectra`
  command installed.

**Projects with more than one agent**

- **FR-027**: Whether Spec Kit registers an extension's commands for every installed agent integration, or
  only for the active one (and whether an update re-registers them for the default only), MUST be verified
  against the baseline Spec Kit version defined in FR-029.
- **FR-028**: If that verification shows registration is limited to the active integration, the README and
  the landing page MUST document the `specify integration use` steps that give SPECTRA's commands to each
  other installed agent and then restore the original default, and MUST say that the steps are needed
  again after an update. If it shows every integration is covered, the docs MUST say so and give no
  workaround.

**Spec Kit baseline**

- **FR-029**: Every rewritten install, keep-current, remove, multi-agent, and e-learning instruction MUST be
  verified against one baseline: the latest Spec Kit release at implementation time. Its exact version MUST
  be recorded in the plan and stated in the README as the version the instructions were checked against.
  `requires.speckit_version` in `spectra/extension.yml` and the `catalog.json` entry MUST NOT change as part
  of this feature (FR-005).

### Key Entities

- **The SPECTRA extension**: the only thing SPECTRA ships. Its version lives in `spectra/extension.yml` and
  is mirrored in `catalog.json`; it is installed from the catalog and package URLs. Unchanged by this
  feature.
- **The SPECTRA catalog**: `catalog.json`, which a Spec Kit project registers as an install-allowed source so
  that `specify extension add spectra` resolves by name.
- **The agent roster**: `agents-list.json`, generated from `agents/` and read by the roster page.
- **The required checks**: the CI job names the `main` ruleset requires, kept in step across the workflow,
  the committed list, the contract test, and the live ruleset.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new user following the landing page in a clean environment, on the baseline Spec Kit
  version (FR-029), reaches a working SPECTRA command in their agent using only `specify` commands and
  prerequisite installers, with zero `spectra` commands.
- **SC-002**: A search of current documentation (README, `docs/`, the constitution, `CLAUDE.md`,
  `CONTRIBUTING.md`, `SECURITY.md`, `SHIPPING.md`) finds zero `spectra` CLI commands, zero mentions of the
  `spectra-cli` package, and zero mentions of a CLI release.
- **SC-003**: Every docs page that describes SPECTRA, and the README, describes it as an extension by TELUS
  Digital that enhances GitHub Spec Kit, and no docs page or README uses "curated catalog of Spec Kit extensions" or "A TELUS Digital
  platform".
- **SC-004**: The repository has zero git tags and zero GitHub Releases.
- **SC-005**: The full test suite and all maintainer checks pass, and the first ship after the change lands
  on `main` with every required check green, with no break-glass bypass used.
- **SC-006**: Nothing under `spectra/` differs from before the change, and the published extension version
  is unchanged.
- **SC-007**: Every command in every e-learning exercise runs as described against the baseline Spec Kit
  version (FR-029).
- **SC-008**: The capability brief's counts of command files and templates equal the counts in the
  published extension.

## Assumptions

- The CLI has no external users. The maintainer tells internal users directly to remove the tool and use
  `specify` instead; that communication is outside this feature.
- Projects set up by `spectra install` need no migration: the catalog is already registered there and the
  extension already installed, so the `specify` commands work on them as they are.
- Installing Spec Kit itself still needs uv and Git, so those stay as documented prerequisites; only
  prerequisites that existed solely for the CLI are removed.
- The constitution amendment is made through `/speckit-constitution` on this feature's branch before
  `/speckit-plan` runs, because the plan's Constitution Check would otherwise test this feature against a
  Principle VI that still requires the CLI channel. It reaches `main` in the same merge as the
  implementation, together with the documents that depend on it.
- Tags and Releases are deleted by the maintainer after the code change has landed on `main` (FR-030), so
  no intermediate state has docs pointing at a Release that is already gone.
- The exact name of the new required check is chosen during planning; the spec fixes only that there is
  one such check, on one current Python version, running the full suite without installing a package
  (FR-009).
- The multi-agent behaviour named in FR-027 is a fact about Spec Kit to establish during planning
  research. `/speckit-clarify` may revisit it if the result changes what the docs should promise.
- Mentions of other tools' CLIs (`gh`, Claude Code, Kiro CLI, Gemini CLI, Codex CLI, the `specify` CLI) are
  not in scope.
