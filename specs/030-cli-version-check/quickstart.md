# Quickstart: validating `spectra cli version`

Expected outputs are in [contracts/cli-version-command.md](contracts/cli-version-command.md); outcome
rules in [data-model.md](data-model.md).

## Automated

```bash
python3 -m unittest discover -s tests
python3 tools/ship.py --dry-run
```

The new `tests/test_cli_version.py` covers every outcome in the data model with `version.check_update`,
`version.classify_uninstall`, and `version.read_installed_version` mocked, plus isolation (project
classification patched to raise), the opt-outs (network resolver asserted not called), and help rows.

## Manual, from a working copy

Run from the repo root with the package importable (`python3 -m spectra_cli.cli …`), or after
`uv tool install --from . spectra-cli --force`.

1. **Outside any project, offline**:
   ```bash
   cd "$(mktemp -d)" && SPECTRA_NO_UPDATE_CHECK=1 spectra cli version; echo "exit=$?"; ls -A
   ```
   Expect the SKIPPED line naming the committed `VERSION`, `exit=0`, and an empty `ls`.

2. **Outside any project, online**: same, without the env var. Expect LATEST if the working copy matches
   the newest release, AHEAD if it is newer (a branch with `VERSION` already bumped), exit 0.

3. **Update available**: in a scratch dir, install the previous release
   (`uv tool install spectra-cli --from 'git+https://github.com/telus-digital/spectra@6.3.0' --force`),
   run `spectra cli version`, expect UPDATE_AVAILABLE naming `spectra cli update`. Then
   `spectra cli update --yes` and `spectra cli version` again → LATEST.

4. **Inside a project in a broken state**: in a project with Spectra half-installed, `spectra cli version`
   prints the same thing as step 2 and `git status` shows no change.

5. **Help**: `spectra --help` and `spectra cli` list `cli version` / `version` first among tool commands.

6. **Pointer**: `cd "$(mktemp -d)" && spectra version; echo "exit=$?"` → three lines ending
   `Check just the spectra command: spectra cli version`, `exit=5`. `spectra check` there → two lines.
