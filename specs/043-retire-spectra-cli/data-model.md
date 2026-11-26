# Data Model: Retire the spectra CLI

This feature has no runtime data. Its "model" is the set of repository artifacts and what happens to each,
plus the few entities the remaining docs and tooling depend on.

## Entities

### Extension (unchanged)

| Field | Source of truth | Rule |
|---|---|---|
| id | `spectra/extension.yml` → `extension.id` | `spectra` |
| version | `spectra/extension.yml` → `extension.version`, mirrored in `catalog.json` | Not bumped by this feature (FR-005); parity enforced by `tools/checks.py catalog-parity` |
| commands | `spectra/commands/*.md`, registered in `extension.yml` | 14 today; the capability brief and README quote this count (SC-008) |
| templates | `spectra/templates/*.md` | 13 today; quoted likewise |
| package | `docs/packages/spectra.zip` | Unchanged; `zip-matches` check |

### Catalog (unchanged)

`catalog.json` at its raw URL. A project registers it with `--install-allowed` so that
`specify extension add spectra` resolves by name. Its `download_url` points at the package above.

### Roster (unchanged file, parser moves)

`agents-list.json`, generated from `agents/`. Read at load time by `docs/agents.html`. Its schema, field names,
and order stay fixed (constitution V). It is validated by `tools/roster.py:parse(strict=True)` during
generation; that parser moves from `spectra_cli/roster.py` with its rules unchanged: the schema major gate,
the slug pattern, the status, type and provider enums, and the required fields.

### Required check

| Field | Value |
|---|---|
| context | job `name` in `ci.yml` (plus a `(x.y)` suffix only when a matrix exists) |
| registry | `.github/required-checks.json` |
| live copy | ruleset "Protect main — tested" (id 23750842) |
| invariant | workflow contexts = registry = live copy (enforced by `tests/test_ci_contract.py` and `tools/ship.py`) |

Lifecycle for this feature: `{CLI installs and runs (3.9), CLI installs and runs (3.12), Catalog…, CodeQL…}`
→ `{Tests pass, Catalog…, CodeQL…}`, moved in the order in
[contracts/required-checks.md](contracts/required-checks.md).

### Release object (retired)

13 GitHub Releases and their bare-semver tags, 3.0.0 to 6.5.1. They are deleted after the merge by the
maintainer (FR-030). Afterwards, Principle VI holds: zero tags and zero Releases.

## File disposition

### Delete

| Path | Why |
|---|---|
| `spectra_cli/` (12 modules, ~4,800 lines) | The CLI (FR-001) |
| `pyproject.toml` | Packaging for `spectra-cli` |
| `VERSION` | CLI version source |
| `.github/workflows/release.yml` | Tag-triggered CLI Release |
| `test/` (`Dockerfile`, `README.md`, `entrypoint.sh`, `run.sh`, `scenarios.sh`) | Clean-room harness for the CLI |
| `tests/test_agent_list.py`, `test_check.py`, `test_cli_surface.py`, `test_cli_update.py`, `test_cli_version.py`, `test_coverage.py`, `test_extension.py`, `test_health.py`, `test_install.py`, `test_net.py`, `test_no_hardcoded_agents.py`, `test_project.py`, `test_uninstall.py`, `test_version_update.py` | Test only the CLI |

### Create

| Path | Content |
|---|---|
| `tools/roster.py` | `spectra_cli/roster.py` without `fetch()` or the `net` import; docstring rewritten for its remaining callers |
| `tests/test_manifest_version.py` | The `parse_manifest_version` cases carried over from `tests/test_extension.py`, now against `tools/checks.py` |

### Modify

| Path | Change |
|---|---|
| `tools/checks.py` | Own `parse_manifest_version` and `_VERSION_LINE`; drop the `spectra_cli` import and the `cli`-job docstring paragraph |
| `tools/generate_agent_docs.py` | Import `roster` from `tools/`; docstrings stop citing `pyproject.toml` and "the parser the CLI itself uses" |
| `tools/build_package.py`, `tools/codeql_gate.py`, `tools/ship.py`, `tools/agent_source.py` | Docstring and comment lines that cite `pyproject.toml`, the CLI, or its Python 3.9 floor |
| `tests/test_roster.py`, `test_roster_data.py`, `test_generator.py`, `test_ci_contract.py`, `test_codeql_gate.py`, `helpers.py` | Repointed or pruned (research R5) |
| `tests/test_document_templates.py` | Docstring only: point at `tools/checks.py`'s manifest reader instead of the CLI's |
| `.github/workflows/ci.yml` | Job `cli` → job `tests` ("Tests pass") |
| `.github/required-checks.json` | Three contexts |
| `.gitignore` | Drop the `pip install .` / `python -m build` block (`build/`, `dist/`, `*.egg-info/`); keep `.venv/` and `__pycache__/` |
| `.specify/memory/constitution.md` | Already 3.0.0; remove the Sync Impact Report comment before commit |
| `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SHIPPING.md`, `README.md` | Research R8 |
| `docs/index.html`, `docs/capability-brief.html`, `docs/getting-started/index.html`, `docs/getting-started/spectra.html`, `docs/getting-started/agents.html`, `docs/agents.html`, `docs/e-learning/*.html` | Research R8 |
| `docs/case-studies/vibe-plan-spectra.html` | Footer line only ("A TELUS Digital platform" → the brief footer line in [contracts/positioning.md](contracts/positioning.md)); the case study body stays as written |

### Leave unchanged

`spectra/` (everything), `agents/`, `catalog.json`, `agents-list.json`, `docs/packages/spectra.zip`,
`AGENTS_LIST.md`, `specs/` (all earlier features), `spectra/CHANGELOG.md`, `docs/ip-audit-findings.md`,
`docs/case-studies/` (except the footer line above), `docs/e-learning/lab-codebase.zip`, `assets/`, `LICENSE`, `NOTICE`, `TRADEMARK.md`,
`.github/CODEOWNERS`.

## Validation rules carried from the spec

- No current doc names a forbidden command or phrase ([contracts/install-commands.md](contracts/install-commands.md),
  [contracts/positioning.md](contracts/positioning.md)), which checks SC-002 and SC-003.
- `git diff main -- spectra/ catalog.json docs/packages/spectra.zip` is empty (SC-006).
- Capability brief and README counts equal the files in `spectra/commands/` and `spectra/templates/` (SC-008).
- No published page fetches `api.github.com/.../releases` (FR-008).
