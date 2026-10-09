# Quickstart: validate `spectra cli update`

## Prerequisites

- Repo checked out on `029-cli-self-update`.
- `python3` (there is no `python` on the maintainer's Mac).

## 1. Automated tests

```bash
python3 -m unittest discover -s tests
```

Expected: all pass, including the new `tests/test_cli_update.py` (every outcome in
[contracts/cli-update-command.md](contracts/cli-update-command.md), with the network and `uv` mocked)
and the updated retired-subcommand tests in `tests/test_cli_surface.py`.

## 2. Help surfaces, from a non-project folder

Run from the repo root so `REPO` captures the checkout:

```bash
REPO="$PWD"; cd "$(mktemp -d)" && NO_COLOR=1 PYTHONPATH="$REPO" python3 -m spectra_cli.cli --help
```

Expected: the "Tool commands — act on the spectra command itself" panel lists `cli update` then
`cli uninstall`. Repeat with `cli` instead of `--help`: the group intro says the commands work from any
folder and lists `update` and `uninstall`.

## 3. The command runs outside a project

```bash
REPO="$PWD"; cd "$(mktemp -d)" && NO_COLOR=1 PYTHONPATH="$REPO" python3 -m spectra_cli.cli cli update </dev/null; echo "exit=$?"
```

Expected (source tree, so `VERSION` is the installed version):

- If `VERSION` equals the latest release: `✓ The spectra command is up to date (…)`, `exit=0`.
- If `VERSION` is ahead (unreleased bump on this branch): the same line, `exit=0`.
- Offline: the "could not check" failure, `exit=3`.

Never "This is not a Spec Kit project".

## 4. The pointer line from `spectra update`

```bash
REPO="$PWD"; cd "$(mktemp -d)" && NO_COLOR=1 PYTHONPATH="$REPO" python3 -m spectra_cli.cli update; echo "exit=$?"
```

Expected: the three lines in the contract's "spectra update outside a Spec Kit project" section,
`exit=5`. Repeat with `check`: two lines only.

## 5. Real end-to-end (after release, on a machine with an older uv-installed spectra)

```bash
cd ~ && spectra cli update
```

Accept the prompt; then bare `spectra` reports `cli v6.3.0` (SC-001). Inside a Spectra project, run
`git status` before and after `spectra cli update --yes`: no changes (SC-002).

## 6. Pre-flight

```bash
python3 tools/ship.py --dry-run
```

Expected: checks and tests pass; `VERSION` reads `6.3.0`; `spectra/extension.yml`, `catalog.json`,
and `docs/packages/spectra.zip` are unchanged.
