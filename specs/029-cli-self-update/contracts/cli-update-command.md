# Contract: `spectra cli update`

The user-facing surface of the command: invocation, output per outcome, and exit codes. Glyphs are
Spectra's `ui` prefixes (`✓` ok, `›` info, `!` warn, `✗` fail); with `NO_COLOR` or a non-TTY the text is
identical, only unstyled. `<installed>` and `<latest>` are bare semver strings.

## Invocation

```text
spectra cli update [--yes|-y] [--no-update-check] [--help|-h]
spectra [--yes|-y] cli update
```

- Runs identically from any working directory, Spec Kit project or not.
- `--yes` is accepted before or after the subcommand.
- `--no-update-check` is accepted (shared flag) and has no effect on this command.
- `--force` is **not** accepted (argparse usage error, exit 2) — it belongs to `spectra update`.

## Outputs

### Update available, uv-managed — prompt

```text
› A new version <latest> is available (you have <installed>).
  This updates the spectra command only. Your projects and their agents are not touched.
Update the spectra command now? [y/N]
```

On **yes** (or `--yes`, which skips the prompt line), after uv's own output:

```text
✓ Updated the spectra command: <installed> → <latest>.
  The new version takes effect the next time you run spectra.
```

Exit `0`.

On **no**:

```text
› Nothing was changed.
```

Exit `1`.

### Non-interactive, no `--yes`

```text
› A new version <latest> is available (you have <installed>).
  This updates the spectra command only. Your projects and their agents are not touched.
  Re-run with --yes to update without being asked.
```

Exit `1`. No prompt is printed and nothing changes.

### Already current (`up_to_date` or `ahead`)

```text
✓ The spectra command is up to date (<installed>).
```

Exit `0`. No prompt. (`ahead` uses the same line; no downgrade is ever offered.)

### Newest release unreachable

```text
✗ Could not check for a newer spectra command — the latest release could not be fetched.
  Nothing was changed. Check your network connection and try again.
```

Exit `3`. Never prints "up to date".

### Not updatable by itself (source checkout or pip install)

```text
› A new version <latest> is available (you have <installed>).
› spectra is not installed as a uv tool, so it cannot update itself.
  Source checkout: pull the latest changes. pip install: reinstall with the tool you used.
```

Exit `0`. No prompt.

### uv not on PATH

```text
✗ uv was not found on PATH, so spectra cannot update itself automatically.
  Update manually with:
    uv tool install spectra-cli --from 'git+https://github.com/telus-digital/spectra@<latest>' --force
```

Exit `4`. No prompt.

### uv ran and failed

```text
✗ Update failed: uv exited with code <n>; your current version is unchanged.
  If you are on Windows, close this command and run:
    uv tool install spectra-cli --from 'git+https://github.com/telus-digital/spectra@<latest>' --force
```

Exit `4`. (Text is `version.UpdateError`'s existing message.)

## Help surfaces

`spectra --help`, "Tool commands — act on the spectra command itself" panel, in this order:

| Command | Description |
| --- | --- |
| `cli update` | Update the spectra command itself to the newest release. Works from any folder; never touches the agents in your projects. |
| `cli uninstall` | Remove the spectra command from this machine. Extensions in your projects are left untouched. *(unchanged)* |

`spectra cli` (no subcommand) — intro, then the same two rows as `update` / `uninstall`:

```text
  Manage the spectra command itself. These work from any folder. To check or update your whole
  stack — Spec Kit, the core agents, and your agents too — use `spectra version` and
  `spectra update` (see `spectra --help`).
```

## Changes to neighbouring commands

### `spectra update` outside a Spec Kit project (FR-016)

```text
✗ This is not a Spec Kit project — no .specify/ directory here or in any parent folder.
  Initialize Specify and add Spectra: spectra install
  Update just the spectra command: spectra cli update
```

Exit `5` (unchanged). `spectra check`, `spectra version`, and `spectra uninstall` keep the first two
lines only — feature 028's contract.

### `spectra cli version` (FR-014)

Unchanged: prints the retirement message naming `spectra version`, exit `2`.
