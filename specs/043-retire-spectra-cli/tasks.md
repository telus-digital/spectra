---

description: "Task list for retiring the spectra CLI"
---

# Tasks: Retire the spectra CLI

**Input**: Design documents from `specs/043-retire-spectra-cli/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: The spec asks for no new test-first work. The test tasks below exist because FR-003 requires
the remaining suite to keep passing: they move, repoint, prune or delete existing tests. Verification of the
docs is done by the quickstart scenarios and greps, run at the end of each story.

**Organization**: Tasks are grouped by user story. The CLI removal itself (FR-001 to FR-004, FR-009,
FR-010) is in the Foundational phase: once `spectra_cli/` and `pyproject.toml` are gone, the old CI job
cannot run, so the code, tests and CI job change together, before any doc work.

**Conventions for every task**

- Use `python3`, not `python`, in local commands.
- Canonical `specify` commands: [contracts/install-commands.md](contracts/install-commands.md). Use them
  spelled exactly as written there, and introduce no other command for the same job.
- Product wording, footer tagline, trust-card wording and banned phrases:
  [contracts/positioning.md](contracts/positioning.md). The footer tagline is exactly
  `SPECTRA · a Spec Kit extension by TELUS Digital` (keep each page's existing separator markup, `·` or
  `&middot;`).
- Spec Kit baseline: **1.4.5** (research R1).
- Never touch `spectra/`, `agents/`, `catalog.json`, `agents-list.json`, `docs/packages/spectra.zip`,
  `AGENTS_LIST.md`, `spectra/CHANGELOG.md`, `docs/ip-audit-findings.md`, `docs/e-learning/lab-codebase.zip`,
  or any earlier `specs/` folder (FR-005, FR-025).
- Tasks marked **Maintainer** are outward-facing or change live GitHub settings. `/speckit-implement` does
  not run them; it stops and hands them to the maintainer (FR-011, FR-030).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an unfinished task)
- **[Story]**: The user story the task belongs to (US1 to US5)

---

## Phase 1: Setup

**Purpose**: Confirm the starting point so later checks have something to compare with.

- [X] T001 Confirm the baseline: `specify --version` reports 1.4.5; `python3 -m unittest discover -s tests`, `python3 tools/checks.py --all` and `python3 tools/generate_agent_docs.py --check` all pass on the branch before any change; `ls spectra/commands | wc -l` prints 14 and `ls spectra/templates | wc -l` prints 13 (if either count differs, use the real count everywhere this task list says 14 or 13, per SC-008)
- [X] T002 Record the list of files that name the CLI, so later greps can confirm each was handled: `grep -rlnE 'spectra (install|check|version|update|uninstall|agent-list|cli)\b|spectra-cli|spectra_cli|releases/latest|SPECTRA_NO_UPDATE_CHECK|curated catalog|TELUS Digital platform|pyproject' README.md CLAUDE.md CONTRIBUTING.md SECURITY.md SHIPPING.md docs tools tests .github .gitignore` (expected today: `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`, `SECURITY.md`, `SHIPPING.md`, `docs/index.html`, `docs/agents.html`, `docs/capability-brief.html`, `docs/case-studies/vibe-plan-spectra.html`, `docs/getting-started/{index,spectra,agents}.html`, `docs/e-learning/{assessment,bugfix,customization,index,module-3,module-4}.html`, `docs/ip-audit-findings.md` (left unchanged), `tools/{build_package,checks,codeql_gate,generate_agent_docs,ship}.py`, the tests listed in T008 to T021, `.github/workflows/ci.yml`, `.github/workflows/release.yml`, `.github/required-checks.json`)

---

## Phase 2: Foundational (blocking: remove the CLI, move the parsers, replace the CI job)

**Purpose**: FR-001 to FR-004, FR-009, FR-010, FR-012. After this phase the repository has no CLI code, the
suite passes without it, and CI has one test job named "Tests pass".

**⚠️ CRITICAL**: Do the moves (T003 to T005) before the deletions (T019, T020). No doc work starts until the
checkpoint at T023 passes.

### Move what maintainer tooling still needs

- [X] T003 Create `tools/roster.py` by copying `spectra_cli/roster.py` with its behaviour unchanged: keep `parse` (including `strict=True`), `load`, `RosterError`, `Roster`, `Agent`, `Phase`, the schema-major gate, the slug pattern, the status, type and provider enums, and the required-field rules. Drop `fetch()` and the `spectra_cli.net` import, which only `spectra agent-list` used. Rewrite the module docstring: the roster is generated from `agents/` by `tools/generate_agent_docs.py`, validated by this parser before anything is written, and read at load time by `docs/agents.html`, whose dependence is why the schema, field names and order stay fixed (constitution Principle V). Stdlib only
- [X] T004 In `tools/checks.py`, move `parse_manifest_version` and its `_VERSION_LINE` pattern in from `spectra_cli/extension.py` unchanged, delete `from spectra_cli import extension as extension_module` (line 45) and repoint every `extension_module.` call to the local function; rewrite the line-59 comment so it explains the top-level-only `version:` match without citing "the CLI's version scanner"; replace the line-6 docstring clause about `pyproject.toml` with "never shipped: nothing under `tools/` is part of the extension package"; drop any docstring paragraph about the `cli` CI job
- [X] T005 In `tools/generate_agent_docs.py`, import the roster parser from `tools/roster.py` instead of `spectra_cli` (line 52; `tools/` is already on `sys.path` for this script, so `import roster as roster_module` keeps every call site); rewrite the docstrings at lines 6–8 and 31–32 and the function docstring at line 390 so they say the built roster is passed through `tools/roster.py` before anything is written, without "the parser the CLI itself uses" or `packages = ["spectra_cli"]`; rewrite the comment at line 617 so it no longer cites the `pyproject.toml` 3.9 floor, keeping its deeper reason. Leave `SCHEMA_VERSION` as it is
- [X] T006 [P] In `tools/build_package.py`, `tools/codeql_gate.py` and `tools/ship.py`, replace the line-6 docstring clause "`pyproject.toml` lists its packages explicitly, so nothing under …" with the same "never shipped: nothing under `tools/` is part of the extension package" wording used in T004; change nothing else in those files except a `spectra update` mention in `tools/ship.py` text, if one exists. Also fix `tools/agent_source.py` (its module docstring cites the Python 3.9 floor and its planned-agent comment cites "the CLI's roster parser") and the `agents-list.json` bullet in `tools/generate_agent_docs.py`'s docstring, which says installed CLIs read the roster
- [X] T007 [P] In `tests/test_document_templates.py`, reword the `manifest_templates` docstring (line 84) so it points at `tools/checks.py`'s regex-based manifest reader instead of "the CLI's own manifest reader"

### Repoint and prune the tests (FR-003)

- [X] T008 Create `tests/test_manifest_version.py` holding every `parse_manifest_version` case from `tests/test_extension.py`, unchanged in substance, importing the function from `tools/checks.py` (add `tools/` to `sys.path` the same way `tests/test_generator.py` does)
- [X] T009 [P] Repoint `tests/test_roster.py` to `tools/roster.py`; delete the cases that exercise `fetch()` or mock `spectra_cli.net`; keep every `parse`/`load` case
- [X] T010 [P] Repoint `tests/test_roster_data.py` to `tools/roster.py`, and make its manifest-version assertion go through `tools/checks.py` (`read_manifest_version` / `parse_manifest_version`) instead of `spectra_cli.extension`
- [X] T011 [P] Repoint `tests/test_generator.py` from `spectra_cli.roster` to `tools/roster.py`
- [X] T012 [P] In `tests/test_codeql_gate.py`, change the sample file paths that name `spectra_cli/cli.py` to a file under `tools/` (for example `tools/checks.py`); the assertions stay the same
- [X] T013 [P] In `tests/helpers.py`, delete the fixtures and helpers used only by the modules deleted in T019 (confirm with `grep -n '<name>' tests/*.py` for each one before deleting it), remove its `spectra_cli` imports, and reword the module docstring so it no longer says "CLI test suite"
- [X] T014 Update `tests/test_ci_contract.py` so it derives the expected contexts correctly from a job with no `strategy.matrix` (the context is the bare job `name`, with no `(x.y)` suffix), keeps handling a job that has a matrix, and still asserts that the workflow's contexts equal `.github/required-checks.json`; drop any assertion about the `cli` job's install, banner, version, removed-flag or wheel steps

### Replace the CI job (FR-009, FR-010, FR-012; [contracts/required-checks.md](contracts/required-checks.md))

- [X] T015 In `.github/workflows/ci.yml`, replace job `cli` ("CLI installs and runs", matrix 3.9/3.12, and every step that installs the package or asserts the banner, version, removed flags, `spectra cli` commands or wheel contents) with job `tests`, `name: Tests pass`, `runs-on: ubuntu-latest`, no `strategy`, steps: the existing pinned `actions/checkout` commit; the existing pinned `actions/setup-python` commit with `python-version: '3.x'`; `run: python -m unittest discover -s tests -v`. Keep a short comment saying unittest is used because the repository is zero-dependency and nothing is installed. Leave jobs `catalog` and `codeql`, the triggers, the `ci` branch comment and the top-level `permissions` exactly as they are
- [X] T016 Replace `.github/required-checks.json` with exactly `["Tests pass", "Catalog and package stay in sync", "CodeQL finds no high-severity issues"]` (one entry per line, the file's existing formatting)
- [X] T017 Run `python3 -m unittest discover -s tests` and fix only what T003 to T016 broke in the modules that stay; at this point `spectra_cli/` still exists, so a failure in one of the 14 modules T019 deletes (for example one that read the old `cli` job) is expected and is not fixed

### Delete the CLI (FR-001)

- [X] T018 Confirm nothing that will remain imports the CLI: `grep -rn 'spectra_cli' tools tests .github` lists only the test modules T019 deletes
- [X] T019 Delete the 14 CLI-only test modules: `tests/test_agent_list.py`, `tests/test_check.py`, `tests/test_cli_surface.py`, `tests/test_cli_update.py`, `tests/test_cli_version.py`, `tests/test_coverage.py`, `tests/test_extension.py`, `tests/test_health.py`, `tests/test_install.py`, `tests/test_net.py`, `tests/test_no_hardcoded_agents.py`, `tests/test_project.py`, `tests/test_uninstall.py`, `tests/test_version_update.py` (with `git rm`)
- [X] T020 Delete the CLI and its release machinery with `git rm -r`: `spectra_cli/`, `pyproject.toml`, `VERSION`, `.github/workflows/release.yml`, `test/` (the Docker clean-room harness)
- [X] T021 In `.gitignore`, delete the "Build artifacts from `pip install .` / `python -m build`" block's `build/`, `dist/` and `*.egg-info/` lines; keep `.venv/` (move it under the `# Python` block) and `__pycache__/`; leave the zip rules alone
- [X] T022 Run `grep -rnE 'spectra_cli|pyproject|VERSION file|release\.yml' tools tests .github .gitignore` and confirm it prints nothing except legitimate non-CLI uses (for example `SCHEMA_VERSION`)
- [X] T023 Checkpoint: `python3 -m unittest discover -s tests`, `python3 tools/checks.py --all` and `python3 tools/generate_agent_docs.py --check` all pass; `git diff main --stat -- spectra/ catalog.json docs/packages/spectra.zip agents-list.json` prints nothing (SC-006)

**Checkpoint**: The CLI is gone and the repository is green locally. Doc stories can start.

---

## Phase 3: User Story 1 - A new user installs SPECTRA with Spec Kit alone (Priority: P1) 🎯 MVP

**Goal**: The landing page and README give exactly one install path made of `specify` commands and
prerequisite installers (FR-008, FR-019, FR-020, FR-024, FR-029).

**Independent Test**: [quickstart.md](quickstart.md) Scenario 1: in an empty scratch folder outside the
repository, run the landing page's install commands verbatim on Spec Kit 1.4.5 and confirm `spectra` is
listed by `specify extension list` and 14 `speckit-spectra-*` entries exist in the agent's folder.

- [X] T024 [US1] Rewrite the install section of `docs/index.html` as the single path in [contracts/install-commands.md](contracts/install-commands.md) § Install: (1) install Spec Kit, (2) `specify init --here` (skip if the folder already has `.specify/`), (3) `specify extension catalog add https://raw.githubusercontent.com/telus-digital/spectra/main/catalog.json --name spectra --priority 5 --install-allowed`, (4) `specify extension add spectra`, then restart the agent, with the contract's three required notes (`--install-allowed` is required; commit `.specify/extension-catalogs.yml`; restart, then see the agent reference). Remove the Installer/Manual tabs and their script, the "Install with uv · one command" call to action, the "installed as a uv tool" subnote and the "One command, fully set up" card. Keep "Before you start" with its OS-specific uv and Git checks, internet-access note and Spec Kit project note, but drop the "`spectra` offers to create it" wording
- [X] T025 [US1] In `docs/index.html`, delete the script that fetches `api.github.com/…/releases/latest` and the `#release` version pill it fills; keep the "Agents v…" pill read from `catalog.json` working unchanged (FR-008)
- [X] T026 [US1] Replace the README's Installation material (about lines 193–479 of `README.md`: every `uv tool install spectra-cli`, `spectra install`, `spectra check`, `spectra version`, `spectra update`, `spectra cli …`, uninstall and update-check passage) with the same four-step path and notes as T024, and add one sentence stating the instructions were checked against Spec Kit 1.4.5 (FR-029). Delete the "Two release channels" section and its table-of-contents entry, and fix any table-of-contents anchors the rewrite changes
- [X] T027 [US1] Run [quickstart.md](quickstart.md) Scenario 1 in a scratch folder (for example `"$TMPDIR/spectra-qs"`, never inside this repository) by copying the commands out of the edited `docs/index.html`, and fix the page if any step fails or differs from what the page says. Then start the agent in that project (or restart it if it was already running) and confirm it offers at least one `speckit.spectra.*` command, which is what SC-001 measures; if no agent can run there, say so in the implementation summary instead of marking SC-001 met

**Checkpoint**: A new user can install SPECTRA from the landing page or README with `specify` alone.

---

## Phase 4: User Story 2 - Readers understand SPECTRA as an extension that enhances Spec Kit (Priority: P1)

**Goal**: Every docs page and the README describes SPECTRA as an extension by TELUS Digital that enhances
GitHub Spec Kit; no banned phrase remains; the capability brief's trust claims and counts are right
(FR-017, FR-018, FR-021, FR-022).

**Independent Test**: `grep -rnE 'curated (catalog|set)|TELUS Digital platform|installed as a uv tool|Install with uv|One command installs' README.md docs --include='*.html' --include='*.md' | grep -v docs/ip-audit-findings.md`
prints nothing, and reading each page below shows the three points in
[contracts/positioning.md](contracts/positioning.md): an extension, by TELUS Digital, that enhances GitHub
Spec Kit.

- [X] T028 [US2] In `docs/index.html`, set `<title>` to `SPECTRA — a Spec Kit extension by TELUS Digital`, rewrite the meta description (line 7) and the hero eyebrow and lede (around line 341) from the long-form description in [contracts/positioning.md](contracts/positioning.md), with no "One uv command installs it", and set the footer (line 556) to the footer tagline. Do not type the `catalog.json` description ("TELUS Digital - Agentic software engineering across the entire SDLC.") anywhere in the page: the `description-parity` check in `tools/checks.py` fails if the landing page contains it, because the page fetches it from `catalog.json` (constitution Principle V). Run `python3 tools/checks.py description-parity` after the edit (runs after T024 and T025: same file)
- [X] T029 [P] [US2] In `docs/capability-brief.html`, rewrite the trust cards per [contracts/positioning.md](contracts/positioning.md) § Trust claims: "Markdown only" says the published extension is 14 command files and 13 templates plus its licence, notice, trademark policy and changelog, no scripts, binaries or post-install hooks, and that TELUS Digital ships no executable code (Spec Kit installs the files and the agent you already approved runs them); "No telemetry" says SPECTRA makes no network calls of its own and Spec Kit fetches the public catalog and package when you install or update; "Nothing to grant" and "Auditable & pinnable" stay in substance. Replace the footer (line 1846) with `A TELUS Digital extension for GitHub Spec Kit &middot; Human-gated by design`, and replace any other "platform" wording or `spectra` command on the page
- [X] T030 [P] [US2] In `docs/case-studies/vibe-plan-spectra.html`, replace only the footer line (line 1075, "A TELUS Digital platform &middot; Human-gated by design") with `A TELUS Digital extension for GitHub Spec Kit &middot; Human-gated by design`; leave the case study's body as written. (FR-017 bans the phrase on every page under `docs/`, and the Scenario 5 grep would fail without it)
- [X] T031 [P] [US2] In `docs/getting-started/index.html`, add an "Add SPECTRA" step to Section 05 ("Start with Spec Kit") right after Spec Kit is initialized, giving the catalog-add and `specify extension add spectra` commands from [contracts/install-commands.md](contracts/install-commands.md) § Install with the `--install-allowed` and commit-the-catalog notes; point the closing panel at that step; set the footer (line 299) to the footer tagline (FR-022)
- [X] T032 [P] [US2] Set the footer tagline in `docs/getting-started/spectra.html` (line 430)
- [X] T033 [P] [US2] Set the footer tagline in `docs/getting-started/agents.html` (line 507), which sits outside every `<!-- SPECTRA:GENERATED … -->` region; edit nothing inside those regions
- [X] T034 [P] [US2] Set the footer tagline in `docs/agents.html` (line 234, which uses `&middot;`)
- [X] T035 [US2] In `README.md`, replace the line-9 tagline with the long-form description from [contracts/positioning.md](contracts/positioning.md), and rewrite the Supply chain section: the Markdown-only bullet uses the 14 command files and 13 templates wording with no executable code from TELUS Digital, and the telemetry bullet says SPECTRA makes no network calls of its own, with `SPECTRA_NO_UPDATE_CHECK` and `--no-update-check` removed (runs after T026: same file)
- [X] T036 [US2] Run `python3 tools/generate_agent_docs.py --check`, then the Independent Test grep above, and confirm the counts quoted in `docs/capability-brief.html` and `README.md` equal `ls spectra/commands | wc -l` and `ls spectra/templates | wc -l` (SC-008)

**Checkpoint**: Positioning is consistent across the README and every docs page.

---

## Phase 5: User Story 3 - A user keeps SPECTRA current and removes it with Spec Kit (Priority: P2)

**Goal**: Documented `specify` commands for keeping current, projects with more than one agent, and removal
(FR-019, FR-024, FR-027, FR-028).

**Independent Test**: [quickstart.md](quickstart.md) Scenarios 2 and 3 in the scratch project from T027:
each command does what the docs say, and the multi-agent rotation gives `kiro-cli` its 14 commands and
leaves `claude` as the default.

- [X] T037 [US3] In `docs/index.html`, after the install steps, add three blocks taken from [contracts/install-commands.md](contracts/install-commands.md): "Keep current" (`specify self check`, `specify self upgrade`, `specify integration upgrade`, `specify extension update spectra`, `specify extension list`, each with its one-line purpose); "Projects with more than one agent" (the contract's statement in substance: registration goes to the default agent only, an update that installs a newer version removes it from the others, so make each other agent the default briefly and set your usual default back, after installing and again after any such update; with `specify integration status`, `specify integration use <other-agent>`, `specify integration use <your-default>`); "Remove" (`specify extension remove spectra`, which removes SPECTRA's commands from every agent and leaves Spec Kit, other extensions and the default agent untouched) (runs after T028: same file)
- [X] T038 [US3] Add the same three blocks to the README's new installation material in `README.md` (runs after T035: same file)
- [X] T039 [US3] Run [quickstart.md](quickstart.md) Scenarios 2 and 3 in the scratch project and confirm what you see matches the text added in T037 and T038; if Spec Kit 1.4.5 behaves differently from research R2, change both files to match what you observed (FR-028)

**Checkpoint**: Day-two operations are documented with `specify` and verified.

---

## Phase 6: User Story 4 - The e-learning course works without the CLI (Priority: P2)

**Goal**: Every page under `docs/e-learning/` uses `specify` commands only, and every exercise still runs
(FR-017, FR-023, SC-007).

**Independent Test**: `grep -nE 'spectra (install|check|version|update|uninstall|agent-list|cli)\b|spectra-cli|SPECTRA CLI|curated (catalog|set)|TELUS Digital platform' docs/e-learning/*.html`
prints nothing, and [quickstart.md](quickstart.md) Scenario 4 passes on Spec Kit 1.4.5.

- [X] T040 [P] [US4] Rewrite the install lab in `docs/e-learning/module-3.html`: install Spec Kit, `specify init`, register the catalog and `specify extension add spectra` per [contracts/install-commands.md](contracts/install-commands.md) § Install; verify with `specify extension list` and `specify self check`; replace `spectra agent-list` with a link to the Agent Roster page (`../agents.html`); simplify the "No SPECTRA?" aside to the same `specify` steps. The lab still ends with the agent offering both `/speckit-*` and `/speckit-spectra-*` commands
- [X] T041 [P] [US4] In `docs/e-learning/module-4.html`, remove "SPECTRA CLI" from the prerequisites and make the lab setup use the `specify` install steps
- [X] T042 [P] [US4] In `docs/e-learning/index.html`, keep the "Spec Kit 1.0.9 or later" prerequisite and name `specify self check` to see the installed version and `specify self upgrade` to upgrade, in place of any `spectra` command
- [X] T043 [P] [US4] In `docs/e-learning/assessment.html`, replace `spectra install` with the catalog-add and `specify extension add spectra` steps, and `spectra version` / `spectra update` with `specify self check` / `specify self upgrade` (and `specify extension update spectra` where the page means updating SPECTRA itself)
- [X] T044 [P] [US4] In `docs/e-learning/bugfix.html`, make the same replacements as T043
- [X] T045 [P] [US4] In `docs/e-learning/customization.html`, rewrite the catalog-trust passage so SPECTRA's catalog is registered with `specify extension catalog add … --install-allowed` rather than by `spectra install`, and make the bundle-troubleshooting steps use `specify self check` and `specify self upgrade`
- [X] T046 [P] [US4] Positioning pass on `docs/e-learning/AI-DLC.html`, `module-1.html`, `module-2.html`, `module-5.html` and `module-6.html`: wherever a page describes what SPECTRA is, make it say an extension by TELUS Digital that enhances GitHub Spec Kit, and remove any wording that presents SPECTRA as a tool, installer or platform of its own. Change nothing else
- [X] T047 [US4] Run the Independent Test grep above, then [quickstart.md](quickstart.md) Scenario 4: run every `specify` command in the e-learning labs against a scratch project on 1.4.5 and fix any page whose command fails or whose described output differs

**Checkpoint**: A learner completes the course with `specify` commands only.

---

## Phase 7: User Story 5 - The maintainer ships with one release channel (Priority: P3)

**Goal**: The governing documents describe one release channel, no tags and no Releases, and no CLI
(FR-013 to FR-016). The live switch and Release deletion are listed for the maintainer (FR-011, FR-030).

**Independent Test**: `grep -nE 'spectra (install|check|version|update|uninstall|agent-list|cli)\b|spectra-cli|spectra_cli|VERSION|pyproject|release\.yml|per-channel|(two|both|second|other|each) (release )?channels?|CLI' .specify/memory/constitution.md CLAUDE.md CONTRIBUTING.md SECURITY.md SHIPPING.md`
prints nothing that refers to the SPECTRA CLI (mentions of other tools' CLIs, such as Spec Kit's `specify`
CLI, `gh` or Claude Code, are fine), and each file describes the extension as the only thing released, by
merging to `main`.

- [X] T048 [P] [US5] In `.specify/memory/constitution.md` (already 3.0.0), delete the "Sync Impact Report" HTML comment at the top of the file, and confirm with the grep above that the constitution mentions no CLI, no `VERSION` file and no second channel; change no governance text
- [X] T049 [P] [US5] Update `CLAUDE.md` (sections are named by heading or opening words; line numbers drift): drop "changing how the `spectra` CLI works" from the feature-work list in the opening paragraph; replace the "Two independently-versioned things live in this repo" section (its `spectra/` and `spectra_cli/` bullets) with one paragraph: one extension, versioned in `spectra/extension.yml`, mirrored into `catalog.json`, shipped from `main` over raw URLs, released by merging to `main`, and the repository carries no git tags and no GitHub Releases; keep the "adding or changing a command means updating …" list; delete the "## The command surface" section and "Never bump one channel because the other moved"; in the "How changes land" paragraph that introduces `SHIPPING.md`, change "the per-channel release paths" to "the release path"; point the managed "current plan" line at `specs/043-retire-spectra-cli/plan.md`
- [X] T050 [P] [US5] Update `CONTRIBUTING.md`: the repository-layout listing drops `VERSION`, `pyproject.toml`, `spectra_cli/`, `test/` and `release.yml`, and adds `tools/roster.py`; delete the "Release the CLI (`spectra-cli`)" section and its subsections (from about line 426); "How users install" uses the commands in [contracts/install-commands.md](contracts/install-commands.md) § Install; remove the CLI references at about lines 234 and 311; any test-run instruction is `python3 -m unittest discover -s tests` with nothing installed
- [X] T051 [P] [US5] Update `SECURITY.md`: scope covers the `spectra` extension and the repository's maintainer tooling only (lines 14 and 24 drop the CLI); supported versions is the latest published extension version, from `catalog.json` (line 42); no CLI release or update check is mentioned
- [X] T052 [P] [US5] Update `SHIPPING.md`: the quick reference keeps only the extension path and the docs/tooling/housekeeping path (delete Path B, the CLI release); the checks table drops the CLI row and the release-tag row; "The four required checks" becomes three, named exactly `Tests pass`, `Catalog and package stay in sync`, `CodeQL finds no high-severity issues`; the hardening note drops `release.yml`; delete the "Latest" Release warning and the CLI smoke test; remove every `spectra update` mention; keep the rename-deadlock procedure and the break-glass procedure intact (FR-016)
- [X] T053 [US5] Run the Independent Test grep above and read the five files once end to end for leftover references to tags, Releases, `VERSION` or a second channel

**Checkpoint**: The governing documents match constitution 3.0.0.

---

## Phase 8: Polish & cross-cutting verification

**Purpose**: Prove the whole change before it lands.

- [X] T054 Run [quickstart.md](quickstart.md) Scenario 5 in full: `python3 -m unittest discover -s tests`, `python3 tools/checks.py --all`, `python3 tools/generate_agent_docs.py --check`, the "CLI removed" existence test, the forbidden-commands grep (expect no output), the unchanged-extension diff (expect no output), and the command and template counts
- [X] T055 [P] Confirm no published page reads a Release: `grep -rn 'api.github.com' docs --include='*.html'` finds no `releases` URL (FR-008)
- [X] T056 [P] Open `docs/index.html`, `docs/capability-brief.html`, `docs/getting-started/index.html`, `docs/agents.html` and `docs/e-learning/module-3.html` in a browser (`file://` or a local static server) and confirm each renders without console errors, the landing page shows only the "Agents v…" badge with a version in it, and the roster page still loads `agents-list.json`
- [X] T057 Re-run T002's grep and confirm every file it listed has been handled, with `docs/ip-audit-findings.md` the only expected remaining match. Then check FR-026, which the command grep cannot catch: `grep -rniE 'still (have|has|using|use)|already (have|installed)|previous(ly)? install|migrat|legacy|old (spectra|command|cli)' README.md CLAUDE.md CONTRIBUTING.md SECURITY.md SHIPPING.md docs --include='*.md' --include='*.html' | grep -v docs/ip-audit-findings.md`, and read every match: none may be guidance for people who still have the `spectra` command

---

## Phase 9: Landing and post-merge (Maintainer)

**Purpose**: FR-011 and FR-030. These steps change live GitHub state or are permanent, so
`/speckit-implement` stops before them and the maintainer runs them. Order and commands:
[contracts/required-checks.md](contracts/required-checks.md) § The switch sequence and
[quickstart.md](quickstart.md) Scenarios 6 and 7.

- [ ] T058 **Maintainer**: Commit the branch (no Sync Impact Report comment in the constitution) and merge `043-retire-spectra-cli` into local `main`; confirm `python3 -m unittest discover -s tests` and `python3 tools/checks.py --all` pass on the merge
- [ ] T059 **Maintainer**: `git push --force origin HEAD:refs/heads/ci`, wait for `gh run list --branch ci --limit 1` to complete green, then confirm `gh api repos/telus-digital/spectra/commits/$(git rev-parse HEAD)/check-runs --jq '.check_runs[].name'` lists exactly `Tests pass`, `Catalog and package stay in sync`, `CodeQL finds no high-severity issues`
- [ ] T060 **Maintainer**: Point ruleset "Protect main — tested" (id 23750842) at the three contexts with the script in [contracts/required-checks.md](contracts/required-checks.md) § Ruleset update; confirm `gh api repos/telus-digital/spectra/rulesets/23750842 --jq '[.rules[] | select(.type=="required_status_checks") | .parameters.required_status_checks[].context]'` prints the three. Start no other ship between this step and T061
- [ ] T061 **Maintainer**: `python3 tools/ship.py`; it reports the file and ruleset agree, waits for green on `ci`, and pushes the same SHA to `main` with no bypassed status check (SC-005)
- [ ] T062 **Maintainer**: Delete the 13 CLI Releases with their tags, any remaining remote tags, and local tags:
  `gh release list -R telus-digital/spectra --limit 100 --json tagName --jq '.[].tagName' | while read -r t; do gh release delete "$t" -R telus-digital/spectra --cleanup-tag --yes; done`, then
  `git ls-remote --tags origin | awk '{print $2}' | sed 's#refs/tags/##; s#\^{}##' | sort -u | while read -r t; do git push origin --delete "refs/tags/$t"; done`, then
  `git tag -l | while read -r t; do git tag -d "$t"; done` (FR-007, FR-030)
- [ ] T063 **Maintainer**: Verify none remain (SC-004): `gh release list -R telus-digital/spectra --limit 100` and `git ls-remote --tags origin` print nothing, and `gh api repos/telus-digital/spectra/releases --jq length` prints `0`; then open the published landing page and confirm nothing on it broke
- [ ] T064 **Maintainer**: Tell internal users to uninstall the CLI (`uv tool uninstall spectra-cli`) and use `specify` from now on. Outside the repository; the docs carry no such guidance (FR-026)

---

## Dependencies & Execution Order

### Phase dependencies

- **Setup (Phase 1)**: none.
- **Foundational (Phase 2)**: after Setup. Blocks every story, because the docs describe a repository
  without the CLI and nothing can land until CI has the new job.
- **US1 (Phase 3)** and **US2 (Phase 4)**: after Foundational. Both are P1.
- **US3 (Phase 5)**: after US1 (it extends the install material T024 and T026 write) and after T028 and
  T035 (same files).
- **US4 (Phase 6)**: after Foundational only; independent of US1 to US3.
- **US5 (Phase 7)**: after Foundational only; independent of US1 to US4.
- **Polish (Phase 8)**: after every story.
- **Landing (Phase 9)**: after Polish; maintainer only, strictly in order T058 → T064.

### Shared files (sequential even across stories)

- `docs/index.html`: T024 → T025 → T028 → T037
- `README.md`: T026 → T035 → T038

### Within Foundational

- T003, T004 and T005 before T008 to T013 (the tests import the moved code).
- T014 and T015 before T016 and T017.
- T017 and T018 before T019 and T020 (moves verified before anything is deleted).
- T019, T020 and T021 before T022 and T023.

## Parallel Execution Examples

### Foundational

```text
After T003–T005:  T006, T007, T009, T010, T011, T012, T013 in parallel (different files)
```

### User Story 2

```text
After T028 is queued behind T024/T025:  T029, T030, T031, T032, T033, T034 in parallel
```

### User Story 4

```text
T040, T041, T042, T043, T044, T045, T046 in parallel (one e-learning page each)
```

### User Story 5

```text
T048, T049, T050, T051, T052 in parallel (one governing document each)
```

### Across stories

```text
Once Phase 2 is done: US4 (T040–T047) and US5 (T048–T053) can run alongside US1/US2,
since they touch no file US1 to US3 touch.
```

## Implementation Strategy

### MVP first

1. Phase 1 and Phase 2: the CLI is gone, the suite is green, CI has "Tests pass".
2. Phase 3 (US1): a new user can install SPECTRA with `specify` from the landing page and README.
3. Stop and validate with Scenario 1. This alone does not land: the change ships as one merge, because the
   constitution amendment and its dependent documents must reach `main` together.

### Incremental delivery on the branch

1. Foundational → US1 → US2 (both P1: install and positioning).
2. US3 (keep current, multi-agent, remove), verified against 1.4.5.
3. US4 (e-learning) and US5 (governing docs), in either order or alongside.
4. Polish, then hand Phase 9 to the maintainer.

### One merge to `main`

Everything in Phases 1 to 8 lands in a single merge of `043-retire-spectra-cli`, through the switch
sequence in Phase 9. Releases and tags are deleted only after that merge is on `main`.

## Phase 10: Convergence

- [X] T065 Delete the untracked `build/` directory at the repository root before the T058 commit. It holds a stale `pip` build of the CLI (`build/lib/spectra_cli/*.py`, `build/bdist.*`), and `.gitignore` no longer ignores `build/`, so committing every change would put the CLI source back. Confirm `git status --porcelain build` prints nothing, per FR-001 (contradicts)
- [X] T066 Keep `.claude/launch.json`, the local docs preview server config created during implementation, out of the feature commit: remove it, or leave it untracked and stage files explicitly in T058. It is not part of the spec or plan. Per plan: file disposition (unrequested)
- [X] T067 In the scratch project from T027, start an authenticated agent session and confirm it offers at least one `speckit.spectra.*` command. The implementation run could not do this because `claude -p` failed with "OAuth session expired"; only the 14 installed skill files were checked. Record the result in the implementation summary, per SC-001 (partial)
