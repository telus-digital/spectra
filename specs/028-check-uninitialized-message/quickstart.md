# Quickstart: validate the one-step remedy

## Prerequisites

- Repo checked out on `028-check-uninitialized-message`.
- `python3` (no `python` on the maintainer's Mac).

## 1. Automated tests

```bash
python3 -m unittest discover -s tests
```

Expected: all pass, including the updated not-a-project tests in `tests/test_check.py`,
`tests/test_version_update.py`, and `tests/test_uninstall.py`.

## 2. Manual check from source

```bash
REPO="$PWD"; cd "$(mktemp -d)" && NO_COLOR=1 PYTHONPATH="$REPO" python3 -m spectra_cli.cli check; echo "exit=$?"
```

Run it from the repo root so `REPO` captures the checkout.

Expected output matches [contracts/not-a-project-output.md](contracts/not-a-project-output.md), with
`exit=` showing the project-state exit code. Repeat with `version`, `update`, and `uninstall` — the two
lines are identical.

## 3. The advice actually works

In the same empty folder run `spectra install`: it offers to initialize Spec Kit, and on acceptance
finishes with Spectra installed (SC-001).

## 4. Pre-flight

```bash
python3 tools/ship.py --dry-run
```

Expected: checks and tests pass; `VERSION` reads `6.2.2`; `spectra/extension.yml` unchanged.
