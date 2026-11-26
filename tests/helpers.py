"""Shared fixtures for the Spectra test suite.

Standard library only, like everything else in this repository — `unittest` rather than pytest.

Two kinds of fixture:

* **Manifests** — `manifest_yaml()` builds an `extension.yml` with the exact shape the regex scanners
  in `tools/checks.py` rely on.
* **Rosters** — `roster()` returns a valid roster dict that a test mutates to express the one thing it
  cares about, instead of restating every published entry.

`repo_file()` points at committed artifacts for the tests that assert on them.
"""

from __future__ import annotations

import copy
from pathlib import Path

# The line every published copy of the extension description must carry (FR-051).
DESCRIPTION = "TELUS Digital - Agentic software engineering across the entire SDLC."


# --------------------------------------------------------------------------- #
# Manifests
# --------------------------------------------------------------------------- #

def manifest_yaml(version: str = "1.3.1", *, commands=("adr", "domain-analyzer", "create-pr", "brd")) -> str:
    """An extension manifest with the shape the version scanner relies on.

    Deliberately reproduces the real indentation — `  version: "X.Y.Z"` two spaces deep inside the
    `extension:` block — because that exact shape is what the scanners in `tools/checks.py` match.
    A fixture that "looked close enough" would let a broken scanner pass.
    """
    lines = [
        'schema_version: "1.0"',
        "",
        "extension:",
        '  id: "spectra"',
        '  name: "Spectra"',
        f'  version: "{version}"',
        f'  description: "{DESCRIPTION}"',
        '  category: "workflow"',
        '  effect: "read-write"',
        '  author: "TELUS Digital"',
        "",
        "provides:",
        "  commands:",
    ]
    for name in commands:
        lines += [
            f'    - name: "speckit.spectra.{name}"',
            f'      file: "commands/{name}.md"',
            f'      description: "Does the {name} thing."',
        ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Rosters
# --------------------------------------------------------------------------- #

_ROSTER = {
    "schema_version": "1.0",
    "phases": [
        {"id": "foundation", "title": "Foundation", "aidlc": "Inception"},
        {"id": "requirements-discovery", "title": "Requirements & Discovery", "aidlc": "Inception"},
        {"id": "deployment-operations", "title": "Deployment & Operations", "aidlc": "Operation"},
    ],
    "agents": [
        {
            "id": "constitution",
            "title": "Guardrails",
            "description": "Encode coding, security, and architecture standards once.",
            "status": "available",
            "phase": "foundation",
            "type": "core",
            "provider": "speckit",
            "command": "speckit.constitution",
        },
        {
            "id": "domain-analyzer",
            "title": "Domain Analyzer",
            "description": "Infer the project's domain and propose candidate guardrails.",
            "status": "available",
            "phase": "foundation",
            "type": "add-on",
            "provider": "spectra",
            "command": "speckit.spectra.domain-analyzer",
        },
        {
            "id": "brd",
            "title": "BRD Generator",
            "description": "Turn a raw business requirement into a specify-ready BRD.",
            "status": "available",
            "phase": "requirements-discovery",
            "type": "add-on",
            "provider": "spectra",
            "command": "speckit.spectra.brd",
        },
        {
            "id": "gdpr",
            "title": "GDPR Compliance",
            "description": "Verify data-subject rights, lawful basis, retention, and transfers.",
            "status": "planned",
            "phase": "requirements-discovery",
            "type": "add-on",
            "provider": "spectra",
        },
        {
            "id": "create-pr",
            "title": "Create PR",
            "description": "Open a correctly-targeted GitHub PR for the current spec branch.",
            "status": "available",
            "phase": "deployment-operations",
            "type": "core",
            "provider": "spectra",
            "command": "speckit.spectra.create-pr",
        },
    ],
}


def roster(**overrides) -> dict:
    """A small but structurally complete roster: both statuses, both providers, three phases.

    Deep-copied on every call so a test that mutates the result cannot affect the next one. Keyword
    arguments replace top-level keys, which is how the schema-version tests express themselves.
    """
    data = copy.deepcopy(_ROSTER)
    data.update(overrides)
    return data


def agent(data: dict, agent_id: str) -> dict:
    """The entry with `agent_id`, for tests that want to mutate exactly one agent."""
    for entry in data["agents"]:
        if entry["id"] == agent_id:
            return entry
    raise KeyError(f"no agent {agent_id!r} in this roster fixture")


# --------------------------------------------------------------------------- #
# Repository paths
# --------------------------------------------------------------------------- #

REPO_ROOT = Path(__file__).resolve().parent.parent


def repo_file(*parts) -> Path:
    """A path inside this repository, for the tests that assert on committed artifacts."""
    return REPO_ROOT.joinpath(*parts)
