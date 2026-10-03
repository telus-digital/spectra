#!/usr/bin/env python3
# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""Fail the CodeQL job when the scan found something serious.

**Maintainer tooling. Not shipped** — `pyproject.toml` lists its packages explicitly, so nothing under
`tools/` reaches a user's machine.

`github/codeql-action/analyze` succeeds whether or not it finds anything: the findings go to the
Security tab, and the job stays green. That is fine when a pull request's own "Code scanning results"
check does the blocking, but this repository has no pull requests — `main` is gated on required status
checks alone (SHIPPING.md). A green job that found a SQL injection would carry the commit straight
through the gate, so the job needs a step that turns findings into an exit code. This is that step::

    python3 tools/codeql_gate.py <sarif-dir>              # what the CI step runs
    python3 tools/codeql_gate.py <sarif-dir> --threshold 9.0

It reads every `*.sarif` the analyze step wrote and fails on any result whose rule carries a
`security-severity` at or above the threshold. The default, 7.0, is GitHub's own floor for **high**,
so high and critical block and medium and low do not. Quality findings (the `security-and-quality`
suite's non-security queries) carry no `security-severity` at all; they are reported as warnings and
never block — a sole maintainer triaging style nits under a shipping gate is the noise the threshold
exists to avoid.

Dismissing an alert in the Security tab does **not** reach this script: it reads the SARIF the scan
just produced, not GitHub's alert state. A false positive is silenced in the code (a CodeQL
suppression comment) or by excluding the query in the workflow, so the reason lives in the repository
rather than in a UI nobody else can see.

An empty or missing results directory is a failure, not a pass. A gate that silently checks nothing
reads as coverage and provides none.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HIGH = 7.0


def _rules(run: dict) -> dict:
    """{rule id: rule} across the driver and every extension (query pack) in one SARIF run."""
    tool = run.get("tool", {})
    components = [tool.get("driver", {})] + list(tool.get("extensions", []))
    rules = {}
    for component in components:
        for rule in component.get("rules", []):
            if "id" in rule:
                rules[rule["id"]] = rule
    return rules


def _severity(rule: dict):
    """The rule's `security-severity` as a float, or None for a quality-only rule."""
    raw = rule.get("properties", {}).get("security-severity")
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _location(result: dict) -> tuple:
    for location in result.get("locations", []):
        physical = location.get("physicalLocation", {})
        uri = physical.get("artifactLocation", {}).get("uri")
        if uri:
            return uri, physical.get("region", {}).get("startLine", 1)
    return "", 0


def findings(sarif_dir: Path) -> list:
    """Every unsuppressed result in the directory, as dicts carrying its rule's severity."""
    found = []
    for path in sorted(sarif_dir.glob("*.sarif")):
        log = json.loads(path.read_text(encoding="utf-8"))
        for run in log.get("runs", []):
            rules = _rules(run)
            for result in run.get("results", []):
                if result.get("suppressions"):
                    continue
                rule_id = result.get("ruleId") or result.get("rule", {}).get("id", "")
                uri, line = _location(result)
                found.append({
                    "rule": rule_id,
                    "severity": _severity(rules.get(rule_id, {})),
                    "message": (result.get("message", {}).get("text", "").splitlines() or [""])[0],
                    "file": uri,
                    "line": line,
                })
    return found


def _annotate(kind: str, item: dict) -> str:
    where = f" file={item['file']},line={item['line']}" if item["file"] else ""
    severity = "quality" if item["severity"] is None else f"severity {item['severity']}"
    return f"::{kind}{where}::{item['rule']} ({severity}): {item['message']}"


def gate(sarif_dir: Path, threshold: float = HIGH) -> int:
    if not sarif_dir.is_dir() or not any(sarif_dir.glob("*.sarif")):
        print(f"::error::no SARIF files in {sarif_dir}; the scan produced nothing to check.")
        return 1

    found = findings(sarif_dir)
    blocking, advisory = [], []
    for item in found:
        serious = item["severity"] is not None and item["severity"] >= threshold
        (blocking if serious else advisory).append(item)

    for item in advisory:
        print(_annotate("warning", item))
    for item in blocking:
        print(_annotate("error", item))

    if blocking:
        print(f"{len(blocking)} finding(s) at security-severity {threshold} or above; "
              f"{len(advisory)} below it, reported as warnings.")
        return 1
    print(f"No finding at security-severity {threshold} or above; "
          f"{len(advisory)} below it, reported as warnings.")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="codeql_gate",
        description="Fail when CodeQL's SARIF output holds a high or critical security finding.",
    )
    parser.add_argument("sarif_dir", type=Path, help="the directory the analyze step wrote")
    parser.add_argument("--threshold", type=float, default=HIGH,
                        help=f"lowest security-severity that blocks (default {HIGH}, i.e. high)")
    args = parser.parse_args(argv)
    return gate(args.sarif_dir, args.threshold)


if __name__ == "__main__":
    sys.exit(main())
