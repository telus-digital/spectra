#!/usr/bin/env python3
# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""Put a commit on `main`, the only way it can get there.

**Maintainer tooling. Not shipped** — `pyproject.toml` lists its packages explicitly, so nothing under
`tools/` reaches a user's machine.

`main` is gated on CI: the "Protect main — tested" ruleset accepts a push only when the pushed commit
already carries green runs of every required status check, and nobody can bypass it. Check runs attach
to a **commit SHA**, not to a branch, so the way to earn them is to push the commit somewhere else
first::

    python tools/ship.py

    1. refuse a dirty tree, or a HEAD that is not on main
    2. confirm .github/required-checks.json still matches the live ruleset
    3. run the catalog checks, then the full test suite
    4. force-push HEAD to the `ci` branch
    5. wait for every required check to *complete* on that SHA
    6. push the same SHA to main, which the ruleset now accepts

Step 5 waits for completion rather than for green-so-far on purpose. On 2026-09-20 an untested commit
was accepted while a run for a *different* SHA was in flight — the run on it was created one second
after the push that passed — so evaluating the gate while anything is running is not trustworthy.

Step 2 is what keeps the gate from becoming a trap. The required contexts live on GitHub, outside this
repository, so renaming a CI job would leave the ruleset waiting forever for a check that no longer
exists and `main` unpushable with no way to fix it from a push. See SHIPPING.md for the recovery
order, and for the break-glass procedure when Actions itself is down.

`--dry-run` stops after step 3, which is the useful thing to run while still working.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import checks  # noqa: E402

REQUIRED_CHECKS = REPO_ROOT / ".github" / "required-checks.json"

STAGING_BRANCH = "ci"

# Polling. A full CI run is about four minutes; the ceiling is generous enough to absorb a queue and
# short enough that a wedged run fails the command rather than hanging a terminal all afternoon.
POLL_SECONDS = 10
APPEAR_TIMEOUT = 180
COMPLETE_TIMEOUT = 1800

# `git@github.com:owner/repo.git` or `https://github.com/owner/repo(.git)`.
REMOTE = re.compile(r"github\.com[:/]([^/]+/[^/.]+)")


def step(message: str) -> None:
    print(f"==> {message}", flush=True)


def git(*args, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, check=check,
                            capture_output=True, text=True)
    return result.stdout.strip()


def gh_json(*args):
    """A `gh api` call parsed as JSON, or None when gh fails (unauthenticated, offline, 404)."""
    result = subprocess.run(["gh", *args], cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except ValueError:
        return None


def repo_slug():
    match = REMOTE.search(git("remote", "get-url", "origin"))
    return match.group(1) if match else None


def working_tree_is_clean() -> bool:
    return git("status", "--porcelain") == ""


def required_contexts() -> list:
    return sorted(json.loads(REQUIRED_CHECKS.read_text(encoding="utf-8")))


def live_contexts(slug: str):
    """The contexts the live ruleset requires, or None when no ruleset requires any.

    None is not an error here: it is the state this repository is in before the gate is configured,
    and ship.py has to work during its own introduction.
    """
    rulesets = gh_json("api", f"repos/{slug}/rulesets")
    if rulesets is None:
        return None
    for summary in rulesets:
        detail = gh_json("api", f"repos/{slug}/rulesets/{summary['id']}")
        if detail is None:
            continue
        for rule in detail.get("rules", []):
            if rule.get("type") == "required_status_checks":
                contexts = rule["parameters"]["required_status_checks"]
                return sorted(entry["context"] for entry in contexts)
    return None


def check_runs(slug: str, sha: str) -> dict:
    """{context: (status, conclusion)} for every check run attached to the SHA."""
    payload = gh_json("api", f"repos/{slug}/commits/{sha}/check-runs", "--paginate")
    if payload is None:
        return {}
    return {run["name"]: (run["status"], run["conclusion"])
            for run in payload.get("check_runs", [])}


def wait_for_checks(slug: str, sha: str, wanted: list) -> int:
    """Block until every wanted check has completed on the SHA. Returns an exit code."""
    deadline = time.time() + APPEAR_TIMEOUT
    while True:
        seen = check_runs(slug, sha)
        if all(name in seen for name in wanted):
            break
        if time.time() > deadline:
            missing = [name for name in wanted if name not in seen]
            print(f"error: {', '.join(missing)} never started on {sha[:8]}. "
                  f"Is the push trigger still set for the {STAGING_BRANCH!r} branch?",
                  file=sys.stderr)
            return 1
        time.sleep(POLL_SECONDS)

    deadline = time.time() + COMPLETE_TIMEOUT
    while True:
        seen = check_runs(slug, sha)
        pending = [name for name in wanted if seen.get(name, ("", None))[0] != "completed"]
        if not pending:
            break
        if time.time() > deadline:
            print(f"error: still waiting on {', '.join(pending)} after "
                  f"{COMPLETE_TIMEOUT // 60} minutes. Check the run and re-run ship.py.",
                  file=sys.stderr)
            return 1
        step(f"waiting on {len(pending)} check(s): {', '.join(pending)}")
        time.sleep(POLL_SECONDS)

    failed = [name for name in wanted if seen[name][1] != "success"]
    if failed:
        print(f"error: {len(failed)} required check(s) failed on {sha[:8]}:", file=sys.stderr)
        for name in failed:
            print(f"  - {name}: {seen[name][1]}", file=sys.stderr)
        print(f"  Read the run: gh run list --branch {STAGING_BRANCH} --limit 1", file=sys.stderr)
        return 1

    step(f"all {len(wanted)} required checks are green on {sha[:8]}")
    return 0


def preflight() -> int:
    """Everything that can fail locally, so it fails in two minutes rather than in CI."""
    step("running the catalog checks")
    if checks.run(sorted(checks.CHECKS)) != 0:
        return 1

    step("running the test suite")
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                            cwd=REPO_ROOT)
    if result.returncode != 0:
        print("error: the test suite failed; nothing was pushed.", file=sys.stderr)
        return 1
    return 0


def ship(dry_run: bool) -> int:
    # A dry run pushes nothing, so neither refusal applies to it — and insisting on a clean tree
    # would defeat the point, which is to check work that is still in progress.
    if not dry_run:
        if not working_tree_is_clean():
            print("error: the working tree is dirty. Commit or stash first — ship.py pushes HEAD, "
                  "not your uncommitted work.", file=sys.stderr)
            return 1

        branch = git("rev-parse", "--abbrev-ref", "HEAD")
        if branch != "main":
            print(f"error: HEAD is on {branch!r}, not main. ship.py puts commits on main; "
                  "merge or rebase your work onto main first.", file=sys.stderr)
            return 1

    sha = git("rev-parse", "HEAD")
    slug = repo_slug()
    if slug is None:
        print("error: could not work out the GitHub repository from the origin remote.",
              file=sys.stderr)
        return 1

    wanted = required_contexts()
    live = live_contexts(slug)
    if live is None:
        step("no ruleset requires status checks yet — the gate is not configured (see SHIPPING.md)")
    elif live != wanted:
        print("error: .github/required-checks.json and the live ruleset disagree.", file=sys.stderr)
        print(f"  committed: {wanted}", file=sys.stderr)
        print(f"  live:      {live}", file=sys.stderr)
        print("  Fix the ruleset or the file before shipping — a mismatch here is what makes main "
              "unpushable. See SHIPPING.md, 'the rename deadlock'.", file=sys.stderr)
        return 1

    if preflight() != 0:
        return 1
    if dry_run:
        step("dry run: everything local passed, nothing was pushed")
        return 0

    step(f"pushing {sha[:8]} to {STAGING_BRANCH} to earn its checks")
    subprocess.run(["git", "push", "--force", "origin", f"{sha}:refs/heads/{STAGING_BRANCH}"],
                   cwd=REPO_ROOT, check=True)

    if wait_for_checks(slug, sha, wanted) != 0:
        return 1

    step("pushing the same commit to main")
    subprocess.run(["git", "push", "origin", f"{sha}:refs/heads/main"], cwd=REPO_ROOT, check=True)
    print(f"shipped {sha[:8]} to main.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="ship",
        description="Run the checks, earn CI on the staging branch, then push main.",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="run the local checks and stop; push nothing")
    args = parser.parse_args(argv)
    try:
        return ship(dry_run=args.dry_run)
    except subprocess.CalledProcessError as exc:
        print(f"error: {' '.join(exc.cmd)} failed with exit {exc.returncode}.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
