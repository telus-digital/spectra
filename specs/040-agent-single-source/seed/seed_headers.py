#!/usr/bin/env python3
# Copyright 2026 TELUS Digital
# SPDX-License-Identifier: Apache-2.0
"""One-off seeding for feature 040 (tasks T002–T003). Not maintained tooling; kept as provenance.

Writes `agents/_phases.md` and one header per agent from the hand-edited `agents-list.json` and the
command descriptions in `spectra/extension.yml`, as they stood before `agents/` became the source.
Bodies of shipped agents are written separately (T014–T017).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
AGENTS = REPO / "agents"
ENTRY = re.compile(r'^    - name: "(speckit\.spectra\.[^"]+)"\n      file: "[^"]+"\n'
                   r'      description: "((?:[^"\\]|\\.)*)"$', re.M)


def unescape(value: str) -> str:
    return re.sub(r"\\(.)", r"\1", value)


def block(pairs) -> str:
    return "---\n" + "".join(f"{key}: {value}\n" for key, value in pairs) + "---\n"


def main() -> None:
    roster = json.loads((REPO / "agents-list.json").read_text(encoding="utf-8"))
    manifest = {name: unescape(text) for name, text in
                ENTRY.findall((REPO / "spectra" / "extension.yml").read_text(encoding="utf-8"))}

    AGENTS.mkdir(exist_ok=True)
    phases = "\n".join(block([("id", p["id"]), ("title", p["title"]), ("aidlc", p["aidlc"])])
                       for p in roster["phases"])
    (AGENTS / "_phases.md").write_bytes(phases.encode("utf-8"))

    position = {}
    for agent in roster["agents"]:
        position[agent["phase"]] = position.get(agent["phase"], 0) + 10
        pairs = [("id", agent["id"]), ("title", agent["title"])]
        if "command" in agent:
            pairs.append(("command", agent["command"]))
        pairs += [("provider", agent["provider"]), ("type", agent["type"]),
                  ("phase", agent["phase"]), ("order", str(position[agent["phase"]])),
                  ("status", agent["status"]), ("summary", agent["description"])]
        if agent["provider"] == "spectra" and agent["status"] == "available":
            pairs.append(("manifest", manifest[agent["command"]]))
        (AGENTS / f"{agent['id']}.md").write_bytes(block(pairs).encode("utf-8"))


if __name__ == "__main__":
    main()
