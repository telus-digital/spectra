# Research: Retire the spectra CLI

All findings below were established on 2026-11-25. Spec Kit runs were made with `specify` 1.4.5 in a
throwaway project under the session scratchpad, never in this repository.

## R1. Spec Kit baseline (FR-029)

- **Decision**: The baseline is **Spec Kit 1.4.5**.
- **Rationale**: `gh api repos/github/spec-kit/releases/latest` returns `v1.4.5`, published
  2026-11-25T17:43:41Z, and it is the version installed locally. Per the clarification, every rewritten
  instruction is verified against it. The README states it as the version the instructions were checked
  against. `requires.speckit_version` (`>=0.11.2`) and the `catalog.json` entry (`>=0.11.0`) are left as
  they are (FR-005).
- **Alternatives considered**: Checking against the declared floor 0.11.2, or against both, was rejected at
  clarify. Users following the docs install the latest release, and the floor would need a second
  environment for no user benefit. Raising `requires.speckit_version` was also rejected, because it changes
  `spectra/`.
- **Noted, out of scope**: `catalog.json` (`>=0.11.0`) and `extension.yml` (`>=0.11.2`) disagree, and the
  e-learning course separately needs 1.0.9 or later. FR-005 keeps both files as they are. The course keeps
  its own "1.0.9 or later" prerequisite and now names `specify self check` and `specify self upgrade` to
  meet it.

## R2. Multi-agent registration on 1.4.5 (FR-027, FR-028)

**Experiment** (scratch project; `claude` default, `kiro-cli` installed alongside):

| Step | Command | claude: spectra commands | kiro-cli: spectra commands | registry `registered_commands` keys |
|---|---|---|---|---|
| 1 | `specify init --here --integration claude --script sh --non-interactive` then `specify integration install kiro-cli` | — | — | — |
| 2 | `specify extension catalog add <catalog.json> --name spectra --priority 5 --install-allowed`; `specify extension add spectra` | 14 | **0** | `claude` |
| 3 | `specify integration use kiro-cli` | 14 | 14 | |
| 4 | `specify integration use claude` | 14 | 14 | `claude`, `kiro-cli` |
| 5 | `specify extension update spectra` (already current) | 14 | 14 | unchanged ("Up to date") |
| 6 | Installed copy marked 1.30.0, then `specify extension update spectra` | 14 | **0** | `claude` |
| 7 | `specify integration use kiro-cli`; `specify integration use claude` | 14 | 14 | |
| 8 | `specify extension remove spectra` | 0 | 0 | extension dir gone; default still `claude` |

- **Decision**: The limitation is real on 1.4.5. Installing registers SPECTRA only for the **default**
  integration. A real update (a newer version) strips it from every other integration and re-registers it
  for the default only. An update that finds nothing newer touches nothing. Activation accumulates, so
  `specify integration use <other>` followed by `specify integration use <original>` gives every agent the
  commands and leaves the default as it was. Removal clears every agent.
- **Consequence for the docs** (FR-028): the README and the landing page document the rotation for projects
  with more than one agent. They say to run it after installing and again after any update that actually
  installed a newer version. The exact text is in [contracts/install-commands.md](contracts/install-commands.md).
- **Alternatives considered**: Recommending `specify integration switch`, which replaces the integration,
  or reinstalling per agent. Both were rejected: `use` is the documented "set the default without
  uninstalling" command, and the rotation is exactly what the CLI's coverage step automated.

## R3. The `specify` command surface on 1.4.5

Confirmed present with `--help`:

| Need | Command |
|---|---|
| Install Spec Kit | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` |
| Check for a newer Spec Kit | `specify self check` (read-only) |
| Upgrade Spec Kit | `specify self upgrade` |
| Initialize a project | `specify init --here` (interactive) or `--integration <key>` |
| Bring core agent files current | `specify integration upgrade` |
| Register the SPECTRA catalog | `specify extension catalog add <url> --name spectra --priority 5 --install-allowed` |
| Install SPECTRA | `specify extension add spectra` |
| See what is installed | `specify extension list` |
| Update SPECTRA | `specify extension update spectra` (asks for confirmation; no flag skips it) |
| Remove SPECTRA | `specify extension remove spectra` (`--keep-config`, `--force` available) |
| Set the default agent | `specify integration use <key>` |
| See installed agents and the default | `specify integration status` |

- **Decision**: The docs use exactly these commands (canonical list in
  [contracts/install-commands.md](contracts/install-commands.md)).
- **Considered and not adopted**: `specify init --extension <id>` can install an extension during init, but
  it needs the SPECTRA catalog registered first or a pre-trusted URL. Documenting it would add a second
  install path, which FR-019 rules out.
- **Prerequisites**: Installing Spec Kit as documented needs uv, and uv needs Git to fetch from a
  `git+https` URL. Both stay as prerequisites. Internet access to `github.com` and
  `raw.githubusercontent.com` stays. Nothing is CLI-only, so no prerequisite is removed. The
  "`spectra` offers to create a project" wording goes.

## R4. What maintainer tooling still needs from the CLI (FR-002, FR-003)

| CLI code | Remaining caller | Decision |
|---|---|---|
| `spectra_cli/roster.py` (`parse`, `load`, `RosterError`, `Roster`, `Agent`, `Phase`, schema gate) | `tools/generate_agent_docs.py` (validates the roster it builds); `tests/test_roster.py`, `test_roster_data.py`, `test_generator.py` | Move to **`tools/roster.py`** with behaviour unchanged. Drop `fetch()` and the `spectra_cli.net` import, which only `spectra agent-list` used. Docstrings stop citing the CLI and Principle VI's "installed CLI" promise, and say instead that `docs/agents.html` reads the file. |
| `spectra_cli/extension.py: parse_manifest_version` (+ `_VERSION_LINE`) | `tools/checks.py` (catalog parity); `tests/test_roster_data.py` (via `read_manifest_version`) | Move into **`tools/checks.py`**, its only production caller. `test_roster_data` asserts through `checks`. The scanner cases from `tests/test_extension.py` move to a new `tests/test_manifest_version.py`. |
| everything else in `spectra_cli/` (`cli`, `install`, `health`, `coverage`, `version`, `project`, `net`, `ui`, `exits`, the rest of `extension`) | none | Delete. |

- **Rationale**: One parser per format is the property the generator depends on ("a second parser would be
  a second opinion"). Moving rather than rewriting keeps it, and `tools/` is already on `sys.path` for the
  generator and checks.
- **Alternatives considered**: Folding the roster parser into `tools/generate_agent_docs.py`. Rejected,
  because the generator is already the largest tool and three test modules import the parser on its own.

## R5. Tests (FR-003)

- **Delete** (they test only the CLI): `test_agent_list`, `test_check`, `test_cli_surface`,
  `test_cli_update`, `test_cli_version`, `test_coverage`, `test_extension` (its scanner cases are kept, see
  R4), `test_health`, `test_install`, `test_net`, `test_no_hardcoded_agents` (it scans `spectra_cli/` for a
  hard-coded roster; with no package there is nothing to scan), `test_project`, `test_uninstall`,
  `test_version_update`.
- **Repoint**: `test_roster` (to `tools/roster.py`, dropping its fetch and network cases), `test_roster_data`,
  `test_generator`, `test_ci_contract` (the CI job no longer has a matrix), `test_codeql_gate` (its sample
  file paths name `spectra_cli/cli.py`; switch to a `tools/` path), and `helpers.py` (prune fixtures used
  only by deleted modules; the docstring no longer says "CLI test suite").
- **Keep unchanged**: every `*_flow.py` agent test, `test_agent_source`, `test_doc_output_paths`,
  `test_document_templates`, `test_markdown_subset`, `test_next_step_suggestions`,
  `test_onboarding_sequence`.

## R6. The required check (FR-009 to FR-012)

- **Decision**: Replace job `cli` ("CLI installs and runs", matrix 3.9/3.12) with job **`tests`**, named
  **"Tests pass"**. It checks out, sets up Python with `python-version: '3.x'` through the already-pinned
  `actions/setup-python` commit (the latest stable on the runner), and runs
  `python -m unittest discover -s tests -v`. There is no matrix and no `pip install`.
- **Required contexts after the switch**: `Tests pass`, `Catalog and package stay in sync`,
  `CodeQL finds no high-severity issues` (three, down from four).
- **The live ruleset today** (read-only check): "Protect main — tested" (id 23750842) requires the four
  current contexts. "Protect main — structure" covers deletion and non-fast-forward on the default branch
  only. **No ruleset targets tags**, so deleting tags is not blocked.
- **Rationale**: The 3.9/3.12 matrix protected the CLI's packaging floor. With no shipped Python package,
  one current interpreter tests what runs, and one context is the simplest ruleset edit.
- **Alternatives considered**: Keeping a two-version matrix under a new name. Rejected at clarify.

## R7. Tags and Releases (FR-007, FR-030)

- **Inventory**: 13 GitHub Releases and 13 bare-semver tags: 3.0.0, 4.0.0, 5.0.0, 6.0.0, 6.1.0, 6.2.0,
  6.2.1, 6.2.2, 6.3.0, 6.4.0, 6.4.1, 6.5.0, 6.5.1.
- **Decision**: The maintainer deletes each Release together with its tag after the merge to `main`, deletes
  any remaining remote tags, and then confirms both lists are empty. The commands are in
  [quickstart.md](quickstart.md), Scenario 7. Implementation does not run them.
- **Rationale**: This is permanent and outward-facing (clarify Q2). Doing it after the merge means the
  landing page's Release badge has already been removed from `main`.

## R8. Documentation inventory (FR-016 to FR-026)

| File | What changes |
|---|---|
| `docs/index.html` | `<title>`, meta description, hero lede and eyebrow; remove the "Install with uv · one command" CTA, the "installed as a uv tool" subnote, and the "One command, fully set up" card; "Before you start" keeps uv and Git but drops "`spectra` offers to create it"; Install section becomes one path ([contracts/install-commands.md](contracts/install-commands.md)): install Spec Kit → initialize the project → register the catalog → add SPECTRA → restart the agent, then keep-current, multi-agent and remove blocks; remove the Installer/Manual tabs; remove the `releases/latest` fetch and the `#release` pill, keeping the `catalog.json` "Agents v…" pill; footer tagline |
| `docs/capability-brief.html` | "Markdown only" card: 14 command files and 13 templates, and add that TELUS Digital ships no executable code; "No telemetry" card: SPECTRA makes no network calls of its own, and Spec Kit fetches the public catalog and package; "A TELUS Digital platform" → positioning text ([contracts/positioning.md](contracts/positioning.md)) |
| `docs/getting-started/index.html` | Section 05 gains an "Add SPECTRA" step with the catalog and extension commands, and the closing panel points at it; footer tagline |
| `docs/getting-started/spectra.html`, `docs/getting-started/agents.html`, `docs/agents.html` | Footer tagline (agents page: outside the generated regions) |
| `docs/e-learning/module-3.html` | Install lab rewritten: `specify` install, `specify init`, catalog add, extension add; verification with `specify extension list` and `specify self check`; the roster via the Agent Roster page instead of `spectra agent-list`; the "No SPECTRA?" aside simplified |
| `docs/e-learning/module-4.html` | Prerequisites drop "SPECTRA CLI"; lab setup uses the `specify` steps |
| `docs/e-learning/index.html` | Spec Kit 1.0.9 prerequisite names `specify self check` and `specify self upgrade` |
| `docs/e-learning/assessment.html`, `bugfix.html` | `spectra install` → catalog and extension steps; `spectra version` and `spectra update` → `specify self check` and `specify self upgrade` |
| `docs/e-learning/customization.html` | Catalog-trust passage: SPECTRA's catalog is registered with `specify extension catalog add … --install-allowed`, not by `spectra install`; bundle troubleshooting uses `specify self check` and `upgrade` |
| `docs/e-learning/AI-DLC.html`, `module-1.html`, `module-2.html`, `module-5.html`, `module-6.html` | Positioning pass only; no CLI commands found |
| `README.md` | Tagline (line 9); Supply chain: Markdown-only counts, telemetry bullet (drop `SPECTRA_NO_UPDATE_CHECK` and `--no-update-check`); Installation (lines 193–479) replaced by the single `specify` path, keep-current, multi-agent, and remove, plus the "checked against Spec Kit 1.4.5" statement; delete "Two release channels" and its table-of-contents entry |
| `CLAUDE.md` | Drop the CLI from feature-work scope and the two-channel section; drop "The command surface"; describe one channel (no tags, no Releases); the managed plan pointer is refreshed by the agent-context hook |
| `CONTRIBUTING.md` | Repository layout without `VERSION`, `pyproject.toml`, `spectra_cli/`, release workflow; delete "Release the CLI (`spectra-cli`)" and its subsections; "How users install" uses the canonical commands; line 234 and line 311 drop CLI references |
| `SECURITY.md` | Scope: extension and repository tooling only; supported versions: the extension's latest |
| `SHIPPING.md` | Quick reference without Path B; checks table without the CLI row and the release-tag row; "The four required checks" → three, with the new names; hardening note without `release.yml`; delete Path B and the "Latest" warning; remove "`spectra update`" from text |
| Tooling docstrings | `tools/*.py` lines citing `pyproject.toml lists its packages` → "never shipped: nothing under `tools/` is part of the extension package" |

Search terms used to find every occurrence (and to verify SC-002): `spectra install|check|version|update|
uninstall|agent-list|cli`, `spectra-cli`, `spectra_cli`, `uv tool install spectra`, `spectra command`,
`releases/latest`, `curated catalog`, `TELUS Digital platform`, `SPECTRA_NO_UPDATE_CHECK`,
`--no-update-check`. Matches on other tools' CLIs (`gh`, Claude Code, Kiro, Gemini, Codex, `specify`) and
inside `specs/`, `spectra/CHANGELOG.md`, `docs/ip-audit-findings.md` are excluded.
