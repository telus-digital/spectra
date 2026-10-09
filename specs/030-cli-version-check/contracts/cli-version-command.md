# Contract: `spectra cli version`

The user-facing surface: invocation, output per outcome (see [data-model.md](../data-model.md)), exit
codes, and help copy. Glyphs are Spectra's `ui` prefixes (`✓` ok, `›` info, `!` warn, `✗` fail); with
`NO_COLOR` or a non-TTY the text is identical, only unstyled. `<installed>` and `<latest>` are bare semver.
Exact wording may be polished in implementation; the **facts each line carries** are the contract.

## Invocation

```text
spectra cli version [--no-update-check] [--yes|-y] [--help|-h]
spectra [--no-update-check] cli version
```

- Identical from any working directory, Spec Kit project or not, in any project state.
- `--yes` is accepted (shared flag) and has no effect — the command never prompts.
- `--no-update-check` / `SPECTRA_NO_UPDATE_CHECK=1` make it offline (outcome SKIPPED).
- `--force` is **not** accepted (usage error, exit 2) — it belongs to `spectra update`.
- No banner, no start-of-run nudge.

## Outputs — every one exits `0`

### LATEST

```text
✓ spectra <installed> is the latest release.
```

### AHEAD (pre-release or local build)

```text
✓ spectra <installed> is the latest — ahead of the newest release (<latest>).
```

### UPDATE_AVAILABLE (uv tool)

```text
› spectra <installed> — a new version <latest> is available.
  Update it with: spectra cli update
```

### UPDATE_AVAILABLE_NOT_UV (source checkout or pip install)

```text
› spectra <installed> — a new version <latest> is available.
  spectra is not installed as a uv tool, so `spectra cli update` cannot update it.
  Source checkout: pull the latest changes. pip install: reinstall with the tool you used.
```

### UPDATE_AVAILABLE_NO_UV (uv not on PATH)

```text
› spectra <installed> — a new version <latest> is available.
  uv was not found on PATH. Update manually with:
    uv tool install spectra-cli --from 'git+https://github.com/telus-digital/spectra@<latest>' --force
```

The hint lines in the two variants above are the same strings `spectra cli update` prints for the same
install kind (shared helper, research R4).

### UNREACHABLE

```text
! spectra <installed> — the newest release could not be checked.
  Check your network connection and try again.
```

Never says "latest" or "available".

### SKIPPED (`--no-update-check` / `SPECTRA_NO_UPDATE_CHECK`)

```text
› spectra <installed> (update check skipped).
```

No network request is made.

### INSTALLED_UNKNOWN

```text
! The installed spectra version could not be determined. The newest release is <latest>.
```

(If `<latest>` is also unknown, the second sentence is omitted and the UNREACHABLE advice line is added.)

## Never

- Prints "This is not a Spec Kit project", "retired", or anything about the Spec Kit CLI, core agents,
  Spectra's agents, or the project.
- Prompts, updates, or creates/modifies/deletes a file.

## Help copy

`spectra --help` → **Tool commands — act on the spectra command itself**, in this order:

| Row | Description |
| --- | --- |
| `cli version` | Show the spectra command's version and whether a newer release exists. Works from any folder; never checks the agents. |
| `cli update` | *(unchanged)* |
| `cli uninstall` | *(unchanged)* |

`spectra cli` (no subcommand) → Tool commands panel lists `version`, `update`, `uninstall`. Its intro keeps
pointing at `spectra version` / `spectra update` for the whole stack.

## `spectra version` outside a Spec Kit project (FR-015)

```text
✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.
  Initialize Specify and add Spectra: spectra install
  Check just the spectra command: spectra cli version
```

Exit `5` (`EXIT_PROJECT_STATE`), unchanged. `spectra check` / `spectra uninstall` keep the two-line form;
`spectra update` keeps its `spectra cli update` line.
