#!/usr/bin/env python3
# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""The catalog-channel drift checks, defined once and run from two places.

**Maintainer tooling. Not shipped** — `pyproject.toml` lists its packages explicitly, so nothing under
`tools/` reaches a user's machine.

Constitution Principle V says `catalog.json`, `docs/index.html`, the generated agent listings and the
published zip must never drift from the `spectra/` folder or from `agents-list.json`. These are the
assertions that enforce it. They used to live as inline shell inside `.github/workflows/ci.yml`, which
meant `tools/ship.py` could only re-check them by reimplementing them — a second definition that would
drift from the first, which is the exact failure mode Principle V exists to prevent. Defining them
here lets the workflow and the pre-flight run the *same* code::

    python tools/checks.py --all              # every check (what ship.py runs)
    python tools/checks.py zip-matches        # one check by name (what a CI step runs)
    python tools/checks.py --list             # the registered names

Each check returns a list of human-readable problems; an empty list means it passed. Adding a check
means adding it to `CHECKS` and adding a step to `ci.yml` — `tests/test_ci_contract.py` fails when
those two disagree, so a check cannot be registered here and silently never run in CI.

The `cli` job's assertions are deliberately **not** here. They need an installed wheel across a Python
matrix, so they are environment setup as much as they are checks, and pretending otherwise would give
a local run a false sense of completeness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_package  # noqa: E402
import generate_agent_docs  # noqa: E402

from spectra_cli import extension as extension_module  # noqa: E402

MANIFEST = REPO_ROOT / "spectra" / "extension.yml"
CATALOG = REPO_ROOT / "catalog.json"
PACKAGE = REPO_ROOT / "docs" / "packages" / "spectra.zip"
LANDING = REPO_ROOT / "docs" / "index.html"

# FR-051/SC-010: the extension description is published in three places and must read identically in
# all of them. `tests/test_ci_contract.py` asserts this string still matches `tests/helpers.py`, so
# the two copies cannot drift apart.
DESCRIPTION = "TELUS Digital - Agentic software engineering across the entire SDLC."

# `  description: "…"` — the `extension:` block's own description, two spaces deep. Anchored to the
# line for the same reason the CLI's version scanner is: a nested `description:` under `provides:`
# must not match. This is a scanner over a shape Spec Kit fixes, not a YAML parser — the repository
# is zero-dependency by constitution and `yaml` is not importable here.
DESCRIPTION_LINE = re.compile(r'^  description: "(.*)"$', re.M)


def check_generated_listings() -> list:
    """The generated agent listings still match `agents-list.json`.

    Delegates to the generator rather than restating any of its rules: it owns the regions, the prose
    anchors, the title containment and the roster/manifest agreement. It prints its own detail, so all
    that is added here is a one-line verdict.
    """
    if generate_agent_docs.run(check=True) == 0:
        return []
    return ["the generated agent listings are out of date or incomplete (detail above). "
            "Run: python tools/generate_agent_docs.py"]


def check_catalog_parity() -> list:
    """`spectra/extension.yml` and `catalog.json` agree on the version and the command count."""
    problems = []
    try:
        manifest_text = MANIFEST.read_text(encoding="utf-8")
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"could not read the manifest or the catalog ({exc})."]

    entry = catalog.get("extensions", {}).get("spectra", {})

    manifest_version = extension_module.parse_manifest_version(manifest_text)
    catalog_version = entry.get("version")
    if manifest_version != catalog_version:
        problems.append(
            f"extension.yml is {manifest_version!r} but catalog.json says {catalog_version!r}.")

    manifest_commands = len(generate_agent_docs.MANIFEST_COMMAND.findall(manifest_text))
    catalog_commands = entry.get("provides", {}).get("commands")
    if manifest_commands != catalog_commands:
        problems.append(
            f"extension.yml declares {manifest_commands} commands but catalog.json says "
            f"{catalog_commands}.")
    return problems


def _packaged_manifest() -> str:
    with zipfile.ZipFile(PACKAGE) as archive:
        return archive.read("spectra/extension.yml").decode("utf-8")


def check_description_parity() -> list:
    """Every published copy of the extension description reads identically.

    The landing page is deliberately excluded from the *copies* and asserted to carry none: it fetches
    the value from `catalog.json` at page load, which is the only way "every copy agrees" stays true
    without anyone having to remember it (Principle V).
    """
    problems = []
    try:
        sources = {
            "spectra/extension.yml": MANIFEST.read_text(encoding="utf-8"),
            "the packaged extension.yml": _packaged_manifest(),
        }
    except (OSError, KeyError, zipfile.BadZipFile) as exc:
        return [f"could not read a published manifest ({exc})."]

    for label, text in sources.items():
        match = DESCRIPTION_LINE.search(text)
        found = match.group(1) if match else None
        if found != DESCRIPTION:
            problems.append(f"{label} describes the extension as {found!r}, expected {DESCRIPTION!r}.")

    try:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return problems + [f"could not read catalog.json ({exc})."]
    catalog_description = catalog.get("extensions", {}).get("spectra", {}).get("description")
    if catalog_description != DESCRIPTION:
        problems.append(
            f"catalog.json describes the extension as {catalog_description!r}, "
            f"expected {DESCRIPTION!r}.")

    try:
        if DESCRIPTION in LANDING.read_text(encoding="utf-8"):
            problems.append(
                "docs/index.html hard-codes the description; it must fetch it from catalog.json.")
    except OSError as exc:
        problems.append(f"could not read docs/index.html ({exc}).")
    return problems


def check_zip_matches() -> list:
    """The committed package is exactly what `build_package.py` would produce right now.

    Compared against `build_package.sources()` rather than by walking `spectra/` directly, so the
    comparison uses the same exclusion rules that built the archive. Walking the folder instead would
    report a local `.DS_Store` as drift even though the builder — and the CI checkout, where the file
    is gitignored and absent — would never include it.
    """
    try:
        with zipfile.ZipFile(PACKAGE) as archive:
            packaged = {name: archive.read(name) for name in archive.namelist()}
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"could not read {PACKAGE.relative_to(REPO_ROOT)} ({exc})."]

    expected = {
        path.relative_to(REPO_ROOT).as_posix(): path.read_bytes()
        for path in build_package.sources()
    }

    problems = []
    for name in sorted(set(expected) - set(packaged)):
        problems.append(f"{name} is in spectra/ but missing from the published zip.")
    for name in sorted(set(packaged) - set(expected)):
        problems.append(f"{name} is in the published zip but not in spectra/.")
    for name in sorted(set(expected) & set(packaged)):
        if expected[name] != packaged[name]:
            problems.append(f"{name} differs between spectra/ and the published zip.")
    if problems:
        problems.append("Rebuild it. Run: python tools/build_package.py")
    return problems


# The registry. `tests/test_ci_contract.py` asserts every name here is invoked by a step in
# `.github/workflows/ci.yml`, and that every invocation there names something registered here.
CHECKS = {
    "generated-listings": check_generated_listings,
    "catalog-parity": check_catalog_parity,
    "description-parity": check_description_parity,
    "zip-matches": check_zip_matches,
}


def run(names) -> int:
    """Run the named checks in order. Returns an exit code; prints the verdict."""
    problems = []
    for name in names:
        problems += [f"{name}: {problem}" for problem in CHECKS[name]()]

    if problems:
        print(f"error: {len(problems)} problem(s) found:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"{len(names)} check(s) passed: {', '.join(names)}.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="checks",
        description="Run the catalog-channel drift checks (Constitution Principle V).",
    )
    parser.add_argument("name", nargs="?", choices=sorted(CHECKS),
                        help="a single check to run; omit with --all to run every check")
    parser.add_argument("--all", action="store_true", help="run every registered check")
    parser.add_argument("--list", action="store_true", help="print the registered check names")
    args = parser.parse_args(argv)

    if args.list:
        for name in sorted(CHECKS):
            print(name)
        return 0
    if args.all:
        return run(sorted(CHECKS))
    if args.name:
        return run([args.name])
    parser.error("give a check name, --all, or --list")


if __name__ == "__main__":
    sys.exit(main())
