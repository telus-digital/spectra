# Data Model: `spectra cli version`

No persisted data. The command is a pure function of three inputs, evaluated in a fixed order.

## Inputs

| Input | Source | Values |
| --- | --- | --- |
| `installed` | `version.read_installed_version()` | semver string, or `None` (rare: no metadata and no `VERSION` file) |
| `opted_out` | `_update_check_disabled(args)` — `--no-update-check` or `SPECTRA_NO_UPDATE_CHECK` | bool |
| `check` | `version.check_update()` → `{status, installed, latest}` | `up_to_date` / `update_available` / `ahead` / `latest_unknown` |
| `kind` | `version.classify_uninstall()` — **only** evaluated on `update_available` | `UV_MANAGED` / `NOT_INSTALLED` / `PIP_OR_SOURCE` / `UNKNOWN_UV_ABSENT` |

Never read: the current directory, `project.classify()`, `health.*`, `extension.*`, `coverage.*`.

## Outcome resolution

Evaluated top to bottom; the first match wins. Every outcome exits `0` (research R3).

| # | Condition | Outcome | Network | Subprocess |
| --- | --- | --- | --- | --- |
| 1 | `opted_out` | **SKIPPED** — installed version, "update check skipped" | none | none |
| 2 | `check.status == latest_unknown` | **UNREACHABLE** — installed version, "newest release could not be checked" | yes | none |
| 3 | `installed is None` | **INSTALLED_UNKNOWN** — "installed version could not be determined", names `latest` | yes | none |
| 4 | `up_to_date` | **LATEST** | yes | none |
| 5 | `ahead` | **AHEAD** — reported as latest, notes it is ahead of `latest` | yes | none |
| 6 | `update_available`, `kind == UV_MANAGED` | **UPDATE_AVAILABLE** → `spectra cli update` | yes | `uv tool list` |
| 7 | `update_available`, `kind in (NOT_INSTALLED, PIP_OR_SOURCE)` | **UPDATE_AVAILABLE_NOT_UV** → pull / reinstall hint | yes | `uv tool list` (PIP case) |
| 8 | `update_available`, `kind == UNKNOWN_UV_ABSENT` | **UPDATE_AVAILABLE_NO_UV** → pinned manual `uv tool install …` | yes | none |

Row 3 precedes rows 4–8 because `compare_versions()` sorts an unknown installed version below any real
release, which would otherwise surface as a false `update_available` (research R5).

## Invariants

- No outcome prompts, installs, or writes a file (FR-003, FR-006).
- "latest" and "available" appear only in rows 4–8, i.e. only after `latest` was resolved *and*
  `installed` is known (SC-004).
- `spectra cli update` is named only in row 6 (FR-004, FR-007).
